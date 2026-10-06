"""Collect public KSUM profile fields in a five-company test or resumable full run."""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://startups.startupmission.in"
INPUT_FILE = Path(__file__).with_name("ksum_companies.csv")
TEST_OUTPUT_FILE = Path(__file__).with_name("ksum_enrichment_test.csv")
FULL_OUTPUT_FILE = Path(__file__).with_name("ksum_companies_enriched.csv")
ERROR_OUTPUT_FILE = Path(__file__).with_name("ksum_enrichment_errors.csv")
TEST_COMPANY_COUNT = 5
REQUEST_TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 1
MAX_FETCH_ATTEMPTS = 2
INPUT_COLUMNS = ["id", "company_name", "location", "ksum_url", "source_page"]
OUTPUT_COLUMNS = [
    "id",
    "company_name",
    "location",
    "ksum_url",
    "website",
    "sector",
    "industry",
    "technology",
    "business_model",
    "founders",
]
ERROR_COLUMNS = ["id", "company_name", "ksum_url", "error", "timestamp"]


def normalize_text(text: str) -> str:
    """Collapse repeated whitespace while preserving meaningful punctuation."""
    return " ".join(text.split())


def is_valid_http_url(value: str) -> bool:
    """Check that a displayed website value is an absolute HTTP(S) URL."""
    parsed_url = urlparse(value)
    return parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)


def is_valid_ksum_url(value: str) -> bool:
    """Check that an input URL is a public KSUM startup-profile URL."""
    parsed_url = urlparse(value)
    return (
        is_valid_http_url(value)
        and parsed_url.netloc == "startups.startupmission.in"
        and parsed_url.path.startswith("/startups/")
        and parsed_url.path != "/startups/"
    )


def load_input_companies(filename: Path) -> list[dict[str, str]]:
    """Load and validate the Stage 1A master CSV without modifying it."""
    try:
        with filename.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames != INPUT_COLUMNS:
                raise ValueError(
                    f"Unexpected input columns: {reader.fieldnames}. "
                    f"Expected: {INPUT_COLUMNS}"
                )
            companies = list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read {filename}: {error}") from error

    for company in companies:
        if (
            not company["id"]
            or not company["company_name"]
            or not company["location"]
            or not is_valid_ksum_url(company["ksum_url"])
        ):
            raise ValueError(f"Invalid input record: {company}")
    return companies


def load_test_companies(filename: Path) -> list[dict[str, str]]:
    """Select exactly the first five Stage 1A records without changing their values."""
    print(f"Loading {filename.name}...")
    all_companies = load_input_companies(filename)
    if len(all_companies) < TEST_COMPANY_COUNT:
        raise ValueError(
            f"{filename.name} contains fewer than {TEST_COMPANY_COUNT} records."
        )
    companies = all_companies[:TEST_COMPANY_COUNT]
    if len({company["ksum_url"] for company in companies}) != TEST_COMPANY_COUNT:
        raise ValueError("The first five input records do not have unique KSUM URLs.")

    print(f"Selected {len(companies)} companies for testing.")
    return companies


def fetch_profile(
    session: requests.Session, company: dict[str, str]
) -> tuple[str | None, str | None]:
    """Fetch one profile with one conservative retry for transient failures."""
    print("Fetching KSUM profile...")
    last_error = "Unknown request failure"
    for attempt in range(1, MAX_FETCH_ATTEMPTS + 1):
        try:
            response = session.get(company["ksum_url"], timeout=REQUEST_TIMEOUT_SECONDS)
        except (requests.ConnectionError, requests.Timeout) as error:
            last_error = f"{type(error).__name__}: {error}"
            should_retry = attempt < MAX_FETCH_ATTEMPTS
        except requests.RequestException as error:
            last_error = f"{type(error).__name__}: {error}"
            should_retry = False
        else:
            if response.status_code == 429:
                last_error = "HTTP 429 rate limited; not retried"
                should_retry = False
            elif 500 <= response.status_code <= 599:
                last_error = f"HTTP {response.status_code} server error"
                should_retry = attempt < MAX_FETCH_ATTEMPTS
            elif 200 <= response.status_code < 300:
                print("Success.")
                return response.text, None
            else:
                last_error = f"HTTP {response.status_code}"
                should_retry = False

        if should_retry:
            print(
                f"Temporary failure; retrying once after {REQUEST_DELAY_SECONDS} second...",
                file=sys.stderr,
            )
            time.sleep(REQUEST_DELAY_SECONDS)

    print(
        f"Failed: {company['company_name']} | {company['ksum_url']} | {last_error}",
        file=sys.stderr,
    )
    return None, last_error


def build_enriched_record(company: dict[str, str], html: str) -> dict[str, str]:
    """Combine preserved Stage 1A values with fields parsed from a fetched profile."""
    return {
        "id": company["id"],
        "company_name": company["company_name"],
        "location": company["location"],
        "ksum_url": company["ksum_url"],
        **extract_profile_fields(html, company["ksum_url"]),
    }


def write_csv_atomically(
    records: list[dict[str, str]], filename: Path, fieldnames: list[str]
) -> None:
    """Replace a CSV only after its complete replacement file has been written."""
    temporary_file = filename.with_name(f".{filename.name}.tmp")
    try:
        with temporary_file.open("w", encoding="utf-8-sig", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
            csv_file.flush()
            os.fsync(csv_file.fileno())
        os.replace(temporary_file, filename)
    finally:
        if temporary_file.exists():
            temporary_file.unlink()


def load_existing_enriched_records(filename: Path) -> list[dict[str, str]]:
    """Load the successful checkpoint records used to skip completed profile URLs."""
    if not filename.exists():
        return []
    try:
        with filename.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames != OUTPUT_COLUMNS:
                raise ValueError(
                    f"Unexpected checkpoint columns: {reader.fieldnames}. "
                    f"Expected: {OUTPUT_COLUMNS}"
                )
            records = list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read checkpoint {filename}: {error}") from error

    urls = [record.get("ksum_url", "") for record in records]
    if len(urls) != len(set(urls)):
        raise ValueError(
            f"Checkpoint contains duplicate KSUM URLs: {filename}. "
            "Resolve them before resuming."
        )
    for record in records:
        if not is_valid_ksum_url(record.get("ksum_url", "")):
            raise ValueError(f"Checkpoint has invalid KSUM URL: {record.get('ksum_url', '')}")
        if record.get("website", "") and not is_valid_http_url(record["website"]):
            raise ValueError(f"Checkpoint has invalid website URL: {record['website']}")
    return records


def record_error(company: dict[str, str], error_message: str) -> None:
    """Atomically append a failed profile to the error log, creating it only when needed."""
    existing_errors: list[dict[str, str]] = []
    if ERROR_OUTPUT_FILE.exists():
        try:
            with ERROR_OUTPUT_FILE.open(encoding="utf-8-sig", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                if reader.fieldnames != ERROR_COLUMNS:
                    raise ValueError(
                        f"Unexpected error-log columns: {reader.fieldnames}. "
                        f"Expected: {ERROR_COLUMNS}"
                    )
                existing_errors = list(reader)
        except (OSError, csv.Error, ValueError) as error:
            print(f"Could not update error log: {error}", file=sys.stderr)
            return

    existing_errors.append(
        {
            "id": company["id"],
            "company_name": company["company_name"],
            "ksum_url": company["ksum_url"],
            "error": error_message,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    )
    try:
        write_csv_atomically(existing_errors, ERROR_OUTPUT_FILE, ERROR_COLUMNS)
    except (OSError, ValueError) as error:
        print(
            f"Could not save failure details for {company['company_name']}: {error}",
            file=sys.stderr,
        )


def find_labeled_values(soup: BeautifulSoup, label: str) -> str:
    """Return values beside the first matching KSUM structured-field label.

    KSUM renders field labels and values as sibling elements. This relationship
    is more durable than depending on the presentation class names around them.
    """
    desired_label = label.casefold()
    for text_node in soup.find_all(string=True):
        if normalize_text(str(text_node)).casefold() != desired_label:
            continue

        label_element = text_node.parent
        field_group = label_element.parent
        values: list[str] = []
        for child in field_group.find_all(recursive=False):
            if child is label_element:
                continue
            value = normalize_text(child.get_text(" ", strip=True))
            if value and value.casefold() != desired_label and value not in values:
                values.append(value)
        if values:
            return " | ".join(values)
    return ""


def find_website(soup: BeautifulSoup, profile_url: str) -> str:
    """Return the URL from KSUM's visible 'Visit website' link, if present."""
    for link in soup.find_all("a", href=True):
        link_text = normalize_text(link.get_text(" ", strip=True)).casefold()
        if link_text != "visit website":
            continue
        website = urljoin(profile_url, link["href"])
        if is_valid_http_url(website):
            return website
        print(f"Warning: ignored invalid displayed website URL: {website}", file=sys.stderr)
    return ""


def find_founders(soup: BeautifulSoup) -> str:
    """Extract names from KSUM founder cards without capturing avatar initials."""
    founder_names: list[str] = []
    founder_labels = {"founder", "founders", "co-founder", "cofounder"}
    for text_node in soup.find_all(string=True):
        if normalize_text(str(text_node)).casefold() not in founder_labels:
            continue
        role_element = text_node.parent
        name_element = role_element.find_previous_sibling()
        if name_element is None:
            continue
        founder_name = normalize_text(name_element.get_text(" ", strip=True))
        if founder_name and founder_name not in founder_names:
            founder_names.append(founder_name)

    if founder_names:
        return " | ".join(founder_names)
    return find_labeled_values(soup, "Founders")


def extract_profile_fields(html: str, profile_url: str) -> dict[str, str]:
    """Extract only publicly displayed, relevant KSUM profile fields."""
    soup = BeautifulSoup(html, "html.parser")
    return {
        "website": find_website(soup, profile_url),
        "sector": find_labeled_values(soup, "Sector"),
        "industry": find_labeled_values(soup, "Industry"),
        "technology": find_labeled_values(soup, "Technology"),
        "business_model": find_labeled_values(soup, "Business model"),
        "founders": find_founders(soup),
    }


def validate_output_records(
    selected_companies: list[dict[str, str]], output_records: list[dict[str, str]]
) -> None:
    """Ensure saved records preserve Stage 1A values and valid displayed URLs."""
    selected_by_url = {company["ksum_url"]: company for company in selected_companies}
    output_urls = [record["ksum_url"] for record in output_records]
    if len(output_urls) != len(set(output_urls)):
        raise ValueError("Output contains duplicate KSUM URLs.")

    for record in output_records:
        source_record = selected_by_url.get(record["ksum_url"])
        if source_record is None:
            raise ValueError(f"Output URL was not in the selected input: {record['ksum_url']}")
        for key in ("id", "company_name", "location", "ksum_url"):
            if record[key] != source_record[key]:
                raise ValueError(f"Output changed {key} for {record['ksum_url']}")
        if record["website"] and not is_valid_http_url(record["website"]):
            raise ValueError(f"Invalid website URL: {record['website']}")


def save_test_csv(records: list[dict[str, str]], filename: Path) -> None:
    """Save the reviewable test CSV without silently overwriting prior results."""
    if filename.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing file: {filename}. "
            "Move, rename, or remove it before running again."
        )
    write_csv_atomically(records, filename, OUTPUT_COLUMNS)


def print_field_summary(records: list[dict[str, str]]) -> None:
    """Print a compact, reviewable summary of the fields extracted for each company."""
    print("\nExtracted profile fields:")
    for record in records:
        print(f"- {record['company_name']}")
        for field in OUTPUT_COLUMNS[4:]:
            print(f"  {field}: {record[field] or '(blank)'}")


def create_session() -> requests.Session:
    """Create the shared, descriptive session used for sequential KSUM requests."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "AI-JobHunt-KSUM-Research/1.0 "
                "(public KSUM profile enrichment; polite sequential requests)"
            ),
            "Accept": "text/html,application/xhtml+xml",
        }
    )
    return session


def run_test() -> None:
    """Run the original five-company review test."""
    companies = load_test_companies(INPUT_FILE)
    session = create_session()
    output_records: list[dict[str, str]] = []
    failed_count = 0

    for index, company in enumerate(companies, start=1):
        if index > 1:
            time.sleep(REQUEST_DELAY_SECONDS)
        print(f"[{index}/{len(companies)}] {company['company_name']}")
        html, _ = fetch_profile(session, company)
        if html is None:
            failed_count += 1
            continue
        try:
            output_records.append(build_enriched_record(company, html))
        except Exception as error:
            failed_count += 1
            print(
                f"Failed to parse {company['company_name']}: {error}",
                file=sys.stderr,
            )

    validate_output_records(companies, output_records)
    save_test_csv(output_records, TEST_OUTPUT_FILE)
    print(f"\nCompanies attempted: {len(companies)}")
    print(f"Successfully fetched: {len(output_records)}")
    print(f"Failed: {failed_count}")
    print(f"Records saved: {len(output_records)}")
    print(f"Saved to: {TEST_OUTPUT_FILE.name}")
    print_field_summary(output_records)


def run_all() -> None:
    """Run the resumable full enrichment, checkpointing every successful profile."""
    print(f"Loading {INPUT_FILE.name}...")
    companies = load_input_companies(INPUT_FILE)
    output_records = load_existing_enriched_records(FULL_OUTPUT_FILE)
    validate_output_records(companies, output_records)

    completed_urls = {record["ksum_url"] for record in output_records}
    already_enriched = sum(
        company["ksum_url"] in completed_urls for company in companies
    )
    if not FULL_OUTPUT_FILE.exists():
        write_csv_atomically(output_records, FULL_OUTPUT_FILE, OUTPUT_COLUMNS)

    session = create_session()
    seen_input_urls: set[str] = set()
    actual_requests = 0
    newly_successful = 0
    failed_count = 0

    for index, company in enumerate(companies, start=1):
        profile_url = company["ksum_url"]
        if profile_url in completed_urls:
            print(f"[{index}/{len(companies)}] SKIP: Already enriched - {company['company_name']}")
            continue
        if profile_url in seen_input_urls:
            print(f"[{index}/{len(companies)}] SKIP: Duplicate input URL - {company['company_name']}")
            continue
        seen_input_urls.add(profile_url)

        if actual_requests:
            time.sleep(REQUEST_DELAY_SECONDS)
        actual_requests += 1
        print(f"[{index}/{len(companies)}] Enriching: {company['company_name']}")
        html, fetch_error = fetch_profile(session, company)
        if html is None:
            failed_count += 1
            record_error(company, fetch_error or "Profile request failed")
            continue

        try:
            record = build_enriched_record(company, html)
            validate_output_records([company], [record])
        except Exception as error:
            failed_count += 1
            error_message = f"Profile parsing failed: {type(error).__name__}: {error}"
            print(f"FAILED: {company['company_name']} - {error_message}", file=sys.stderr)
            record_error(company, error_message)
            continue

        output_records.append(record)
        try:
            write_csv_atomically(output_records, FULL_OUTPUT_FILE, OUTPUT_COLUMNS)
        except OSError as error:
            output_records.pop()
            raise RuntimeError(
                f"Could not save checkpoint after {company['company_name']}: {error}"
            ) from error
        completed_urls.add(profile_url)
        newly_successful += 1

    validate_output_records(companies, output_records)
    total_output_records = len(output_records)
    unique_output_urls = len({record["ksum_url"] for record in output_records})
    duplicate_count = total_output_records - unique_output_urls

    print("\n========================================")
    print("KSUM STAGE 1B ENRICHMENT COMPLETE")
    print("========================================")
    print(f"Input companies:       {len(companies)}")
    print(f"Already enriched:      {already_enriched}")
    print(f"Newly processed:       {actual_requests}")
    print(f"Successful:            {newly_successful}")
    print(f"Failed:                {failed_count}")
    print(f"Total output records:  {total_output_records}")
    print(f"Unique KSUM URLs:      {unique_output_urls}")
    print(f"Duplicate URLs:        {duplicate_count}")
    print(f"Output: {FULL_OUTPUT_FILE.name}")
    if failed_count:
        print(f"Failed profiles: {ERROR_OUTPUT_FILE.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect public KSUM profile fields in test or resumable full mode."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="enrich all Stage 1A companies with resumable checkpointing",
    )
    arguments = parser.parse_args()

    try:
        if arguments.all:
            run_all()
        else:
            run_test()
    except (FileExistsError, OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
