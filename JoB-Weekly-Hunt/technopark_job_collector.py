#!/usr/bin/env python3
"""Collect all publicly listed Technopark Kerala jobs from the official API.

The JSON API is the source of truth.  The collector intentionally does no
job-profile filtering: every returned record is archived and exported.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import shutil
import sys
import time
from copy import copy
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qs, urlparse
from zipfile import BadZipFile

import requests
from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils.exceptions import InvalidFileException


API_ENDPOINT = "https://technopark.in/api/paginated-jobs"
DETAIL_URL_PREFIX = "https://technopark.in/job-details/"
USER_AGENT = "AI-JobHunt-Technopark-Collector/1.0 (+https://technopark.in/)"
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_DELAY_SECONDS = 0.4
DEFAULT_MAX_RETRIES = 3
STATUS_OPTIONS = ["Not Reviewed", "Apply", "Review", "Skip", "Applied"]

KNOWN_CSV_FIELDS = [
    "job_id",
    "job_listing_id",
    "job_title",
    "posted_date",
    "closing_date",
    "walk_in",
    "is_walk_in",
    "walk_in_start_date",
    "walk_in_start_time",
    "walk_in_end_time",
    "company_id",
    "company_name",
    "company_logo_path",
    "promoted",
    "job_details_url",
]

EXCEL_COLUMNS = [
    ("Review Status", "review_status"),
    ("Job Title", "job_title"),
    ("Company", "company_name"),
    ("Posted Date", "posted_date"),
    ("Closing Date", "closing_date"),
    ("Walk-in", "walk_in"),
    ("Is Walk-in (Original)", "is_walk_in"),
    ("Walk-in Start Date", "walk_in_start_date"),
    ("Walk-in Start Time", "walk_in_start_time"),
    ("Walk-in End Time", "walk_in_end_time"),
    ("Job ID", "job_id"),
    ("Job Listing ID", "job_listing_id"),
    ("Company ID", "company_id"),
    ("Job Details URL", "job_details_url"),
    ("Company Logo Path", "company_logo_path"),
    ("Promoted", "promoted"),
    ("Notes", "notes"),
]


def utc_now() -> str:
    """Return an unambiguous, timezone-aware timestamp."""

    return datetime.now(timezone.utc).isoformat()


def json_default(value: Any) -> str:
    """Fail loudly but readably if a future API value is not JSON-native."""

    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    """Write a text file atomically within its destination directory."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.tmp")
    temporary_path.write_text(text, encoding=encoding, newline="")
    temporary_path.replace(path)


def safe_text(value: Any) -> str:
    """Convert a scalar or structured API value into a CSV/Excel-safe string."""

    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, default=json_default)
    return str(value)


def stable_key(record: dict[str, Any], missing_sequence: int | None = None) -> str | None:
    """Return the documented deduplication key, or a unique missing-ID key."""

    job_id = record.get("id")
    if job_id is not None and not isinstance(job_id, bool) and str(job_id).strip():
        return f"id:{job_id}"
    listing_id = record.get("job_listing_id")
    if listing_id is not None and str(listing_id).strip():
        return f"listing:{str(listing_id).strip()}"
    if missing_sequence is None:
        return None
    return f"missing:{missing_sequence:08d}"


def walk_in_label(value: Any) -> str:
    """Map only recognized source values; unknown values remain explicit."""

    if value == 1 or value == "1":
        return "Yes"
    if value == 0 or value == "0":
        return "No"
    return "Unknown"


def get_page_number(url: str) -> int | None:
    """Extract a positive page query parameter when present."""

    try:
        page_values = parse_qs(urlparse(url).query).get("page", [])
        if len(page_values) != 1:
            return None
        value = int(page_values[0])
        return value if value >= 1 else None
    except (TypeError, ValueError):
        return None


def is_valid_next_url(url: Any) -> bool:
    """Accept only the expected public API host, path, and a valid page number."""

    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    expected = urlparse(API_ENDPOINT)
    return (
        parsed.scheme == "https"
        and parsed.netloc == expected.netloc
        and parsed.path.rstrip("/") == expected.path.rstrip("/")
        and get_page_number(url) is not None
    )


@dataclass
class FetchResult:
    """One request outcome, retained for the audit report."""

    page_number: int
    url: str
    success: bool
    payload: dict[str, Any] | None = None
    attempts: int = 0
    status_code: int | None = None
    error: str | None = None
    received_at: str = field(default_factory=utc_now)

    def report_entry(self) -> dict[str, Any]:
        return {
            "page_number": self.page_number,
            "url": self.url,
            "success": self.success,
            "attempts": self.attempts,
            "status_code": self.status_code,
            "error": self.error,
            "records_received": len(self.payload.get("data", [])) if self.payload else 0,
            "received_at": self.received_at,
        }


@dataclass
class CollectionResult:
    """The complete in-memory result of one collection attempt."""

    raw_records: list[dict[str, Any]]
    page_results: list[FetchResult]
    first_payload: dict[str, Any] | None
    observed_pagination: list[dict[str, Any]]
    warnings: list[str]
    interrupted: bool = False


class TechnoparkCollector:
    """Sequential, retrying client for the official paginated jobs API."""

    def __init__(
        self,
        output_dir: Path,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        delay: float = DEFAULT_DELAY_SECONDS,
        max_retries: int = DEFAULT_MAX_RETRIES,
        archive_raw: bool = True,
    ) -> None:
        self.output_dir = output_dir
        self.timeout = timeout
        self.delay = delay
        self.max_retries = max_retries
        self.archive_raw = archive_raw
        self.raw_dir = output_dir / "raw"
        self.logger = logging.getLogger("technopark_collector")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
        self.warnings: list[str] = []
        self.raw_archive_info: dict[str, Any] = {"enabled": archive_raw, "stale_files_moved": []}

    def prepare_raw_archive(self, run_stamp: str) -> None:
        """Move only stale collector page files aside before writing this run's pages."""

        if not self.archive_raw:
            return
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        stale_pages = sorted(self.raw_dir.glob("page_[0-9]*.json"))
        if not stale_pages:
            return
        archive_dir = self.raw_dir / "previous_runs" / run_stamp
        archive_dir.mkdir(parents=True, exist_ok=True)
        for page_file in stale_pages:
            target = archive_dir / page_file.name
            suffix = 1
            while target.exists():
                target = archive_dir / f"{page_file.stem}_{suffix}{page_file.suffix}"
                suffix += 1
            shutil.move(str(page_file), str(target))
            self.raw_archive_info["stale_files_moved"].append(str(target))

    def fetch_page(self, url: str, page_number: int) -> FetchResult:
        """Fetch and validate one JSON API page with bounded transient retries."""

        last_error: str | None = None
        status_code: int | None = None
        for attempt in range(1, self.max_retries + 2):
            try:
                response = self.session.get(url, timeout=(10, self.timeout))
                status_code = response.status_code
                if response.status_code == 429 or response.status_code >= 500:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        wait_seconds = min(float(retry_after), 60.0)
                    else:
                        wait_seconds = min(2 ** (attempt - 1), 30.0)
                    last_error = f"HTTP {response.status_code}"
                    if attempt <= self.max_retries:
                        self.logger.warning("Page %s: %s; retrying in %.1fs", page_number, last_error, wait_seconds)
                        time.sleep(wait_seconds)
                        continue
                    break
                if not response.ok:
                    last_error = f"HTTP {response.status_code}: {response.reason}"
                    break
                content_type = response.headers.get("Content-Type", "")
                try:
                    payload = response.json()
                except ValueError as exc:
                    last_error = f"Invalid JSON response ({content_type or 'unknown content type'}): {exc}"
                    break
                if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
                    last_error = "JSON response does not contain a list-valued 'data' field"
                    break
                result = FetchResult(page_number, url, True, payload, attempt, status_code)
                self.logger.info("Received %s records from page %s.", len(payload["data"]), page_number)
                return result
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt <= self.max_retries:
                    wait_seconds = min(2 ** (attempt - 1), 30.0)
                    self.logger.warning("Page %s: %s; retrying in %.1fs", page_number, last_error, wait_seconds)
                    time.sleep(wait_seconds)
                    continue
                break
            except requests.RequestException as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                break
        self.logger.error("Page %s failed after %s attempt(s): %s", page_number, attempt, last_error)
        return FetchResult(page_number, url, False, None, attempt, status_code, last_error)

    def archive_page(self, payload: dict[str, Any], page_number: int, padding: int) -> None:
        """Archive the literal successful API response for the current run."""

        if not self.archive_raw:
            return
        path = self.raw_dir / f"page_{page_number:0{padding}d}.json"
        atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2, default=json_default) + "\n")

    @staticmethod
    def pagination_snapshot(payload: dict[str, Any], requested_page: int) -> dict[str, Any]:
        return {
            "requested_page": requested_page,
            "current_page": payload.get("current_page"),
            "last_page": payload.get("last_page"),
            "next_page_url": payload.get("next_page_url"),
            "total": payload.get("total"),
            "per_page": payload.get("per_page"),
        }

    def collect(self, run_stamp: str) -> CollectionResult:
        """Walk pagination defensively, retaining every successful source record."""

        page_results: list[FetchResult] = []
        raw_records: list[dict[str, Any]] = []
        observed: list[dict[str, Any]] = []
        first_payload: dict[str, Any] | None = None
        seen_urls: set[str] = set()
        requested_pages: set[int] = set()
        current_url = f"{API_ENDPOINT}?page=1"
        expected_last_page: int | None = None
        padding = 2
        interrupted = False
        self.prepare_raw_archive(run_stamp)

        try:
            while current_url:
                page_number = get_page_number(current_url)
                if page_number is None:
                    self.warnings.append(f"Refused pagination URL without a valid page number: {current_url}")
                    break
                if current_url in seen_urls or page_number in requested_pages:
                    self.warnings.append(f"Detected repeated pagination request; stopped safely at {current_url}")
                    break
                seen_urls.add(current_url)
                requested_pages.add(page_number)
                display_total = expected_last_page if expected_last_page else "?"
                self.logger.info("Fetching page %s/%s...", page_number, display_total)
                fetched = self.fetch_page(current_url, page_number)
                page_results.append(fetched)
                if not fetched.success or fetched.payload is None:
                    break

                payload = fetched.payload
                if first_payload is None:
                    first_payload = payload
                observed.append(self.pagination_snapshot(payload, page_number))
                raw_records.extend(item for item in payload["data"] if isinstance(item, dict))
                non_dicts = len(payload["data"]) - sum(isinstance(item, dict) for item in payload["data"])
                if non_dicts:
                    self.warnings.append(f"Page {page_number} contained {non_dicts} non-object record(s), which were retained only in its raw archive.")

                payload_page = payload.get("current_page")
                if isinstance(payload_page, int) and payload_page != page_number:
                    self.warnings.append(f"Requested page {page_number} reported current_page={payload_page}.")
                last_page = payload.get("last_page")
                if isinstance(last_page, int) and last_page >= 1:
                    if expected_last_page is not None and last_page != expected_last_page:
                        self.warnings.append(f"API last_page changed during collection: {expected_last_page} to {last_page}.")
                    expected_last_page = last_page
                    padding = max(2, len(str(last_page)))
                self.archive_page(payload, page_number, padding)

                next_url = payload.get("next_page_url")
                if next_url is not None and not is_valid_next_url(next_url):
                    self.warnings.append(f"Ignored unsafe or malformed next_page_url from page {page_number}: {next_url!r}")
                    next_url = None
                if isinstance(next_url, str):
                    next_number = get_page_number(next_url)
                    if next_number is not None and expected_last_page is not None and next_number > expected_last_page:
                        self.warnings.append(f"next_page_url requested page {next_number} beyond reported last_page {expected_last_page}.")
                        break
                    current_url = next_url
                elif expected_last_page is not None and page_number < expected_last_page:
                    current_url = f"{API_ENDPOINT}?page={page_number + 1}"
                else:
                    current_url = ""
                if current_url and self.delay:
                    time.sleep(self.delay)
        except KeyboardInterrupt:
            interrupted = True
            self.warnings.append("Collection interrupted by user; no completeness claim is made.")
            self.logger.warning("Collection interrupted by user.")

        return CollectionResult(raw_records, page_results, first_payload, observed, self.warnings.copy(), interrupted)


def deduplicate_records(records: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Keep the first source occurrence by stable key; retain ID-less records."""

    unique: list[dict[str, Any]] = []
    seen: dict[str, dict[str, Any]] = {}
    duplicate_count = 0
    conflicts: list[str] = []
    missing_identifiers: list[dict[str, Any]] = []
    for occurrence, record in enumerate(records, start=1):
        key = stable_key(record)
        if key is None:
            missing_identifiers.append({"raw_occurrence": occurrence, "job_title": record.get("job_title")})
            unique.append(record)
            continue
        existing = seen.get(key)
        if existing is None:
            seen[key] = record
            unique.append(record)
            continue
        duplicate_count += 1
        if json.dumps(existing, sort_keys=True, default=json_default) != json.dumps(record, sort_keys=True, default=json_default):
            conflicts.append(key)
    return unique, {
        "duplicate_occurrences": duplicate_count,
        "duplicate_conflicting_identifiers": sorted(set(conflicts)),
        "missing_stable_identifier_records": missing_identifiers,
        "deduplication_rule": "First source occurrence wins by numeric id; job_listing_id is used only when id is missing. ID-less records are retained.",
    }


def normalize_record(record: dict[str, Any], detail_url: str) -> dict[str, Any]:
    """Create export fields without mutating the original source record."""

    company = record.get("company") if isinstance(record.get("company"), dict) else {}
    normalized: dict[str, Any] = {
        "job_id": record.get("id"),
        "job_listing_id": record.get("job_listing_id"),
        "job_title": record.get("job_title"),
        "posted_date": record.get("posted_date"),
        "closing_date": record.get("closing_date"),
        "walk_in": walk_in_label(record.get("is_walk_in")),
        "is_walk_in": record.get("is_walk_in"),
        "walk_in_start_date": record.get("walk_in_start_date"),
        "walk_in_start_time": record.get("walk_in_start_time"),
        "walk_in_end_time": record.get("walk_in_end_time"),
        "company_id": record.get("company_id", company.get("id")),
        "company_name": company.get("company"),
        "company_logo_path": company.get("logo"),
        "promoted": record.get("promoted"),
        "job_details_url": detail_url,
    }
    for key, value in record.items():
        if key not in {"id", "company", *KNOWN_CSV_FIELDS}:
            normalized[f"source_{key}"] = value
    for key, value in company.items():
        if key not in {"id", "company", "logo"}:
            normalized[f"company_{key}"] = value
    return normalized


def make_normalized(records: list[dict[str, Any]], detail_urls: dict[str, str]) -> list[dict[str, Any]]:
    """Normalize source records in stable API order."""

    normalized: list[dict[str, Any]] = []
    for occurrence, record in enumerate(records, start=1):
        key = stable_key(record, occurrence)
        normalized.append(normalize_record(record, detail_urls.get(key or "", "")))
    return normalized


def validate_detail_urls(records: list[dict[str, Any]], session: requests.Session, timeout: float) -> dict[str, Any]:
    """Verify the public detail path using up to two live source records."""

    candidates = [r for r in records if r.get("id") is not None and str(r.get("id")).strip()]
    samples = candidates[:2]
    result: dict[str, Any] = {
        "pattern": f"{DETAIL_URL_PREFIX}<numeric job id>",
        "validated": False,
        "samples": [],
        "reason": "No records with numeric job IDs were available for validation.",
    }
    if not samples:
        return result
    all_valid = True
    for record in samples:
        job_id = record["id"]
        url = f"{DETAIL_URL_PREFIX}{job_id}"
        sample: dict[str, Any] = {"job_id": job_id, "url": url}
        try:
            response = session.get(url, timeout=(10, timeout), headers={"Accept": "text/html"})
            content = response.text
            title = safe_text(record.get("job_title"))
            matches = str(job_id) in content and (not title or title.casefold() in content.casefold())
            sample.update({"status_code": response.status_code, "matches_source_record": matches})
            if not (response.ok and matches):
                all_valid = False
        except requests.RequestException as exc:
            sample.update({"error": f"{type(exc).__name__}: {exc}", "matches_source_record": False})
            all_valid = False
        result["samples"].append(sample)
    result["validated"] = all_valid
    result["reason"] = (
        "Two representative official detail pages returned the matching source job ID and title."
        if all_valid and len(samples) == 2
        else "One or more representative official detail pages could not be verified against the source record."
    )
    return result


def csv_columns(normalized: list[dict[str, Any]]) -> list[str]:
    """Keep common fields first and future API fields deterministically afterward."""

    additional = sorted({key for row in normalized for key in row} - set(KNOWN_CSV_FIELDS))
    return KNOWN_CSV_FIELDS + additional


def write_json(path: Path, metadata: dict[str, Any], jobs: list[dict[str, Any]]) -> None:
    """Write the authoritative original-record export."""

    atomic_write_text(path, json.dumps({"collection_metadata": metadata, "jobs": jobs}, ensure_ascii=False, indent=2, default=json_default) + "\n")


def write_csv(path: Path, normalized: list[dict[str, Any]]) -> list[str]:
    """Write a spreadsheet-friendly normalized CSV with UTF-8 BOM."""

    headers = csv_columns(normalized)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.tmp")
    with temporary_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in normalized:
            writer.writerow({header: safe_text(row.get(header)) for header in headers})
    temporary_path.replace(path)
    return headers


def read_existing_reviews(path: Path, backup_dir: Path, run_stamp: str) -> tuple[dict[str, tuple[str, str]], list[str]]:
    """Safely extract user review fields from a previous workbook before refresh."""

    reviews: dict[str, tuple[str, str]] = {}
    warnings: list[str] = []
    if not path.exists():
        return reviews, warnings
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"technopark_jobs_review_before_refresh_{run_stamp}.xlsx"
    shutil.copy2(path, backup_path)
    try:
        workbook = load_workbook(path, read_only=True, data_only=False)
        worksheet = next((ws for ws in workbook.worksheets if "Job ID" in [cell.value for cell in ws[1]]), None)
        if worksheet is None:
            warnings.append("Existing workbook was backed up but does not contain a 'Job ID' header; no review values were imported.")
            return reviews, warnings
        headers = {str(cell.value).strip(): index for index, cell in enumerate(worksheet[1], start=1) if cell.value is not None}
        status_index = headers.get("Review Status")
        notes_index = headers.get("Notes")
        job_id_index = headers.get("Job ID")
        listing_index = headers.get("Job Listing ID")
        for values in worksheet.iter_rows(min_row=2, values_only=True):
            job_id = values[job_id_index - 1] if job_id_index else None
            listing_id = values[listing_index - 1] if listing_index else None
            key = stable_key({"id": job_id, "job_listing_id": listing_id})
            if key is None:
                continue
            status = safe_text(values[status_index - 1]) if status_index else ""
            notes = safe_text(values[notes_index - 1]) if notes_index else ""
            if key in reviews:
                warnings.append(f"Existing workbook had duplicate review key {key}; first review value was preserved.")
            else:
                reviews[key] = (status, notes)
        workbook.close()
    except (OSError, ValueError, KeyError, BadZipFile, InvalidFileException) as exc:
        warnings.append(f"Existing workbook could not be read safely; a backup was created at {backup_path}: {type(exc).__name__}: {exc}")
    return reviews, warnings


def excel_value(field: str, value: Any) -> Any:
    """Use genuine Excel dates where safe while retaining exact source values elsewhere."""

    if field in {"posted_date", "closing_date", "walk_in_start_date"} and isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return value
    return value if isinstance(value, (int, float)) or value is None else safe_text(value)


def write_workbook(
    path: Path,
    normalized: list[dict[str, Any]],
    original_records: list[dict[str, Any]],
    existing_reviews: dict[str, tuple[str, str]],
) -> None:
    """Build the review workbook and carry statuses/notes over by stable ID."""

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Technopark Jobs"
    additional_keys = sorted({key for row in normalized for key in row} - {field for _, field in EXCEL_COLUMNS})
    headers = [header for header, _ in EXCEL_COLUMNS] + [f"Additional: {key}" for key in additional_keys]
    worksheet.append(headers)
    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        alignment = copy(cell.alignment)
        alignment.wrap_text = True
        alignment.vertical = "center"
        cell.alignment = alignment
    worksheet.row_dimensions[1].height = 32

    for index, (record, row) in enumerate(zip(original_records, normalized), start=2):
        key = stable_key(record, index - 1) or ""
        if key in existing_reviews:
            review_status, previous_notes = existing_reviews[key]
        else:
            review_status, previous_notes = "Not Reviewed", ""
        values: list[Any] = []
        for _, field_name in EXCEL_COLUMNS:
            if field_name == "review_status":
                values.append(review_status)
            elif field_name == "notes":
                values.append(previous_notes)
            else:
                values.append(excel_value(field_name, row.get(field_name)))
        values.extend(excel_value(key, row.get(key)) for key in additional_keys)
        worksheet.append(values)
        url_column = next(i for i, (header, _) in enumerate(EXCEL_COLUMNS, start=1) if header == "Job Details URL")
        url = row.get("job_details_url")
        if isinstance(url, str) and url:
            cell = worksheet.cell(index, url_column)
            cell.hyperlink = url
            cell.style = "Hyperlink"

    last_row = max(2, worksheet.max_row)
    status_validation = DataValidation(type="list", formula1='"' + ",".join(STATUS_OPTIONS) + '"', allow_blank=False)
    status_validation.error = "Choose a value from the Review Status list."
    status_validation.errorTitle = "Invalid review status"
    worksheet.add_data_validation(status_validation)
    status_validation.add(f"A2:A{last_row}")
    worksheet.auto_filter.ref = f"A1:{worksheet.cell(1, len(headers)).coordinate}{last_row}"
    worksheet.freeze_panes = "A2"

    widths = {
        "A": 16, "B": 32, "C": 30, "D": 13, "E": 13, "F": 11, "G": 17,
        "H": 16, "I": 16, "J": 16, "K": 12, "L": 20, "M": 12, "N": 46,
        "O": 34, "P": 11, "Q": 42,
    }
    for column, width in widths.items():
        worksheet.column_dimensions[column].width = width
    for column in range(18, len(headers) + 1):
        worksheet.column_dimensions[worksheet.cell(1, column).column_letter].width = 22
    for row_cells in worksheet.iter_rows(min_row=2):
        for cell in row_cells:
            alignment = copy(cell.alignment)
            alignment.vertical = "top"
            alignment.wrap_text = True
            cell.alignment = alignment
        for column_index in (4, 5, 8):
            if column_index <= len(row_cells):
                cell = row_cells[column_index - 1]
                if isinstance(cell.value, date):
                    cell.number_format = "yyyy-mm-dd"
    green = PatternFill("solid", fgColor="C6EFCE")
    yellow = PatternFill("solid", fgColor="FFEB9C")
    red = PatternFill("solid", fgColor="FFC7CE")
    blue = PatternFill("solid", fgColor="BDD7EE")
    status_range = f"A2:A{last_row}"
    worksheet.conditional_formatting.add(status_range, CellIsRule(operator="equal", formula=['"Apply"'], fill=green))
    worksheet.conditional_formatting.add(status_range, CellIsRule(operator="equal", formula=['"Review"'], fill=yellow))
    worksheet.conditional_formatting.add(status_range, CellIsRule(operator="equal", formula=['"Skip"'], fill=red))
    worksheet.conditional_formatting.add(status_range, CellIsRule(operator="equal", formula=['"Applied"'], fill=blue))

    instructions = workbook.create_sheet("Instructions")
    instructions.append(["Technopark Job Review Workbook"])
    instructions["A1"].font = Font(bold=True, size=14)
    instructions.append(["Use Review Status to track a decision. Status and Notes are preserved on the next refresh when Job ID (or Job Listing ID if no Job ID) matches."])
    instructions_alignment = copy(instructions["A2"].alignment)
    instructions_alignment.wrap_text = True
    instructions_alignment.vertical = "top"
    instructions["A2"].alignment = instructions_alignment
    instructions.column_dimensions["A"].width = 110
    instructions.freeze_panes = "A2"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.tmp")
    workbook.save(temporary_path)
    workbook.close()
    temporary_path.replace(path)


def validate_outputs(json_path: Path, csv_path: Path, workbook_path: Path, expected_count: int) -> dict[str, Any]:
    """Re-open all output formats and report concrete integrity checks."""

    results: dict[str, Any] = {"passed": True, "checks": [], "errors": []}
    try:
        loaded = json.loads(json_path.read_text(encoding="utf-8"))
        assert isinstance(loaded.get("jobs"), list)
        assert len(loaded["jobs"]) == expected_count
        results["checks"].append("JSON reopened and job count matches export.")
    except (OSError, ValueError, AssertionError) as exc:
        results["errors"].append(f"JSON validation failed: {exc}")
    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        assert len(rows) == expected_count
        assert set(KNOWN_CSV_FIELDS).issubset(set(reader.fieldnames or []))
        results["checks"].append("CSV reopened with expected headers and row count.")
    except (OSError, csv.Error, AssertionError) as exc:
        results["errors"].append(f"CSV validation failed: {exc}")
    try:
        workbook = load_workbook(workbook_path, data_only=False)
        worksheet = workbook["Technopark Jobs"]
        headers = [cell.value for cell in worksheet[1]]
        assert worksheet.max_row - 1 == expected_count
        assert worksheet.freeze_panes == "A2"
        assert worksheet.auto_filter.ref
        assert "Review Status" in headers and "Notes" in headers and "Job ID" in headers
        assert any("Not Reviewed" in str(dv.formula1) for dv in worksheet.data_validations.dataValidation)
        job_id_column = headers.index("Job ID") + 1
        job_ids = [worksheet.cell(row, job_id_column).value for row in range(2, worksheet.max_row + 1)]
        non_blank_ids = [value for value in job_ids if value not in (None, "")]
        assert len(non_blank_ids) == len(set(map(str, non_blank_ids)))
        workbook.close()
        results["checks"].append("Excel workbook reopened with rows, filters, frozen header, validation, and unique nonblank IDs.")
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        results["errors"].append(f"Excel validation failed: {exc}")
    results["passed"] = not results["errors"]
    return results


def compute_status(result: CollectionResult, unique_count: int) -> tuple[str, list[str]]:
    """Classify collection completeness conservatively."""

    reasons: list[str] = []
    if result.first_payload is None:
        return "FAILED", ["The initial API page was not successfully fetched."]
    if result.interrupted:
        reasons.append("The collection was interrupted.")
    failed = [item for item in result.page_results if not item.success]
    if failed:
        reasons.append(f"{len(failed)} page request(s) failed permanently.")
    latest = result.observed_pagination[-1] if result.observed_pagination else {}
    last_page = latest.get("last_page")
    fetched_pages = {item.page_number for item in result.page_results if item.success}
    if not isinstance(last_page, int) or last_page < 1:
        reasons.append("The API did not provide a valid final page number.")
    elif not set(range(1, last_page + 1)).issubset(fetched_pages):
        reasons.append(f"Not every page from 1 through reported last_page {last_page} was fetched successfully.")
    if isinstance(last_page, int) and result.observed_pagination:
        terminal_next = result.observed_pagination[-1].get("next_page_url")
        if terminal_next:
            reasons.append("The final fetched page still advertised a next_page_url.")
    totals = [snapshot["total"] for snapshot in result.observed_pagination if isinstance(snapshot.get("total"), int)]
    if totals and unique_count != totals[-1]:
        reasons.append(f"Unique exported records ({unique_count}) do not match the latest API-reported total ({totals[-1]}).")
    if len(set(totals)) > 1:
        reasons.append(f"API total changed during collection: {totals}.")
    if result.warnings:
        reasons.extend(result.warnings)
    return ("COMPLETE" if not reasons else "PARTIAL"), reasons


def configure_logging(output_dir: Path) -> None:
    """Send concise operational logs to console and the collector's own folder."""

    logger = logging.getLogger("technopark_collector")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    log_dir = output_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "technopark_collector.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(file_handler)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect every public Technopark Kerala API job listing without filtering.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "data" / "technopark", help="Directory for Technopark outputs.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="Per-response timeout in seconds (positive).")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SECONDS, help="Delay between API page requests in seconds (zero or greater).")
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES, help="Retries after the initial request for transient failures (zero or greater).")
    parser.add_argument("--no-excel", action="store_true", help="Skip Excel generation; JSON, CSV, raw archive, and report still run.")
    parser.add_argument("--no-raw-archive", action="store_true", help="Do not write or move raw API page archives for this run.")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if args.delay < 0:
        parser.error("--delay must be zero or greater")
    if args.max_retries < 0:
        parser.error("--max-retries must be zero or greater")
    return args


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    configure_logging(output_dir)
    logger = logging.getLogger("technopark_collector")
    start = utc_now()
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print("=" * 50)
    print("TECHNOPARK JOB COLLECTOR")
    print("=" * 50)
    logger.info("Connecting to the official API...")
    collector = TechnoparkCollector(output_dir, args.timeout, args.delay, args.max_retries, not args.no_raw_archive)
    result = collector.collect(run_stamp)
    unique_records, dedupe = deduplicate_records(result.raw_records)
    if dedupe["duplicate_conflicting_identifiers"]:
        collector.warnings.append("Conflicting duplicate source records were detected for: " + ", ".join(dedupe["duplicate_conflicting_identifiers"]))

    detail_validation = validate_detail_urls(unique_records, collector.session, args.timeout) if unique_records else {
        "pattern": f"{DETAIL_URL_PREFIX}<numeric job id>", "validated": False, "samples": [], "reason": "No collected records were available."
    }
    detail_urls: dict[str, str] = {}
    if detail_validation["validated"]:
        for occurrence, record in enumerate(unique_records, start=1):
            key = stable_key(record, occurrence)
            if key and record.get("id") is not None:
                detail_urls[key] = f"{DETAIL_URL_PREFIX}{record['id']}"
    else:
        collector.warnings.append("Job detail URL pattern was not verified; Job Details URL cells were left blank.")
    normalized = make_normalized(unique_records, detail_urls)
    status, status_reasons = compute_status(result, len(unique_records))

    json_path = output_dir / "technopark_all_jobs.json"
    csv_path = output_dir / "technopark_all_jobs.csv"
    workbook_path = output_dir / "technopark_jobs_review.xlsx"
    report_path = output_dir / "reports" / "collection_report.json"
    output_paths = {
        "json": str(json_path), "csv": str(csv_path), "excel": None if args.no_excel else str(workbook_path),
        "raw_archive_directory": None if args.no_raw_archive else str(collector.raw_dir), "report": str(report_path),
    }
    metadata = {
        "collection_started_at": start,
        "collection_completed_at": utc_now(),
        "official_api_endpoint": API_ENDPOINT,
        "collection_status": status,
        "raw_records_received": len(result.raw_records),
        "unique_records_exported": len(unique_records),
        "pagination_observed": result.observed_pagination,
        "job_details_url_validation": detail_validation,
    }
    write_json(json_path, metadata, unique_records)
    csv_headers = write_csv(csv_path, normalized)
    workbook_warnings: list[str] = []
    if not args.no_excel:
        existing_reviews, workbook_warnings = read_existing_reviews(workbook_path, collector.raw_dir / "workbook_backups", run_stamp)
        write_workbook(workbook_path, normalized, unique_records, existing_reviews)
    validation = validate_outputs(json_path, csv_path, workbook_path, len(unique_records)) if not args.no_excel else {
        "passed": True, "checks": ["JSON and CSV reopened; Excel generation was disabled by --no-excel."], "errors": []
    }
    if args.no_excel:
        # Still validate the two exports when Excel is intentionally suppressed.
        try:
            loaded = json.loads(json_path.read_text(encoding="utf-8"))
            with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                csv_rows = list(csv.DictReader(handle))
            if len(loaded.get("jobs", [])) != len(unique_records) or len(csv_rows) != len(unique_records):
                raise ValueError("exported row count mismatch")
        except (OSError, ValueError, csv.Error) as exc:
            validation["passed"] = False
            validation["errors"].append(f"JSON/CSV validation failed: {exc}")
    if not validation["passed"]:
        status = "FAILED"
        status_reasons.append("One or more required output validation checks failed.")
    completed = utc_now()
    first = result.first_payload or {}
    report = {
        "collection_started_at": start,
        "collection_completed_at": completed,
        "official_api_endpoint": API_ENDPOINT,
        "collection_status": status,
        "status_reasons_and_warnings": status_reasons + workbook_warnings,
        "pages_discovered": first.get("last_page"),
        "pages_successfully_fetched": len([page for page in result.page_results if page.success]),
        "pages_failed": len([page for page in result.page_results if not page.success]),
        "page_requests": [page.report_entry() for page in result.page_results],
        "failed_pages": [page.report_entry() for page in result.page_results if not page.success],
        "raw_records_received": len(result.raw_records),
        "unique_records_exported": len(unique_records),
        "duplicate_record_count": dedupe["duplicate_occurrences"],
        "duplicate_conflicting_identifiers": dedupe["duplicate_conflicting_identifiers"],
        "records_missing_stable_identifiers": dedupe["missing_stable_identifier_records"],
        "deduplication_rule": dedupe["deduplication_rule"],
        "reported_api_total": first.get("total"),
        "reported_page_size": first.get("per_page"),
        "reported_last_page": first.get("last_page"),
        "pagination_metadata_observed": result.observed_pagination,
        "raw_archive_policy": {
            "policy": "Before an archived run, only raw/page_*.json files from earlier collector runs are moved to raw/previous_runs/<run timestamp>; unrelated raw files are not deleted or altered.",
            **collector.raw_archive_info,
        },
        "job_details_url_validation": detail_validation,
        "output_files": output_paths,
        "csv_headers": csv_headers,
        "validation": validation,
    }
    atomic_write_text(report_path, json.dumps(report, ensure_ascii=False, indent=2, default=json_default) + "\n")
    logger.info("Raw records received: %s", len(result.raw_records))
    logger.info("Unique jobs collected: %s", len(unique_records))
    logger.info("Duplicate records detected: %s", dedupe["duplicate_occurrences"])
    logger.info("Collection status: %s", status)
    logger.info("JSON export saved: %s", json_path)
    logger.info("CSV export saved: %s", csv_path)
    if not args.no_excel:
        logger.info("Excel review workbook saved: %s", workbook_path)
    logger.info("Collection report saved: %s", report_path)
    logger.info("All operations finished.")
    return 0 if status == "COMPLETE" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("[ERROR] Interrupted before the collector could finish reporting.", file=sys.stderr)
        raise SystemExit(130)
