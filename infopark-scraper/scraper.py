"""Stage 1 collector for public Infopark company-directory cards only."""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag


DIRECTORY_URL = "https://infopark.in/companies"
OUTPUT_FILE = Path(__file__).with_name("infopark_companies.csv")
ERROR_FILE = Path(__file__).with_name("errors.csv")
OUTPUT_COLUMNS = [
    "company_name",
    "phone",
    "website",
    "domain",
    "infopark_profile_url",
    "infopark_job_url",
    "source_url",
    "location",
]
ERROR_COLUMNS = ["timestamp", "page_url", "error_type", "error_message"]
REQUEST_TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 0.75
MAX_PAGE_GUARD = 200


def normalize_text(value: str) -> str:
    """Normalize markup whitespace without changing the displayed company wording."""
    return " ".join(value.split())


def is_directory_url(url: str) -> bool:
    """Allow only normal public Infopark /companies directory pagination links."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc != "infopark.in":
        return False
    if parsed.path.rstrip("/") != "/companies":
        return False
    query = parse_qs(parsed.query, keep_blank_values=True)
    return not query or set(query) == {"page"}


def canonical_directory_url(url: str) -> str:
    """Treat the directory's explicit `?page=1` link as the initial-page URL."""
    parsed = urlparse(url)
    if parse_qs(parsed.query, keep_blank_values=True).get("page") == ["1"]:
        return DIRECTORY_URL
    return url


def is_profile_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc == "infopark.in"
        and parsed.path.startswith("/companies-profile/")
    )


def is_job_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc == "infopark.in"
        and parsed.path.startswith("/jobs/")
    )


def csv_read(path: Path, columns: list[str]) -> list[dict[str, str]]:
    """Read an existing compatible CSV checkpoint."""
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != columns:
                raise ValueError(
                    f"Unexpected columns in {path.name}: {reader.fieldnames}; expected {columns}"
                )
            return list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read {path}: {error}") from error


def atomic_csv_write(records: list[dict[str, str]], path: Path, columns: list[str]) -> None:
    """Persist a complete, durable checkpoint before atomically publishing it."""
    temporary_path = path.with_name(f".{path.name}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(records)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def add_error(
    errors: list[dict[str, str]], page_url: str, error_type: str, error_message: str
) -> None:
    """Record a distinct real error without repeatedly duplicating it on resume."""
    if any(
        error["page_url"] == page_url
        and error["error_type"] == error_type
        and error["error_message"] == error_message
        for error in errors
    ):
        return
    errors.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "page_url": page_url,
            "error_type": error_type,
            "error_message": error_message,
        }
    )


def fetch_directory_page(
    session: requests.Session, page_url: str
) -> tuple[str | None, int | None, str | None]:
    """Fetch one permitted directory page with one conservative transient retry."""
    last_error = "Unknown request failure"
    for attempt in range(1, 3):
        try:
            response = session.get(page_url, timeout=REQUEST_TIMEOUT_SECONDS)
        except (requests.ConnectionError, requests.Timeout) as error:
            last_error = f"{type(error).__name__}: {error}"
            retry = attempt == 1
        except requests.RequestException as error:
            return None, None, f"{type(error).__name__}: {error}"
        else:
            if response.status_code == 429:
                return None, response.status_code, "HTTP 429 rate limited; not retried"
            if 500 <= response.status_code <= 599:
                last_error = f"HTTP {response.status_code} server error"
                retry = attempt == 1
            elif 200 <= response.status_code < 300:
                return response.text, response.status_code, None
            else:
                return None, response.status_code, f"HTTP {response.status_code}"
        if retry:
            time.sleep(REQUEST_DELAY_SECONDS)
    return None, None, last_error


def display_page_number(page_url: str) -> str:
    """Display the site-provided query-page number without constructing URLs."""
    page_values = parse_qs(urlparse(page_url).query).get("page")
    return page_values[0] if page_values else "1"


def discover_pagination_urls(html: str, current_url: str) -> list[str]:
    """Read the website's actual pagination anchors rather than guessing pages."""
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []
    for link in soup.select("ul.pagination a[href], a[rel='next'][href]"):
        candidate = canonical_directory_url(urljoin(current_url, link["href"]))
        if is_directory_url(candidate) and candidate not in urls:
            urls.append(candidate)
    return urls


def first_link_matching(card: Tag, label: str, url_check: object) -> str:
    """Return only a card-provided official link for the requested visible action."""
    for link in card.select(".btn-sec a[href]"):
        link_label = normalize_text(link.get_text(" ", strip=True)).casefold()
        candidate = urljoin(DIRECTORY_URL, link["href"].strip())
        if link_label == label.casefold() or url_check(candidate):
            if url_check(candidate):
                return candidate
    return ""


def joined_text(elements: list[Tag]) -> str:
    """Preserve all separately displayed values with an unambiguous CSV delimiter."""
    values: list[str] = []
    for element in elements:
        value = normalize_text(element.get_text(" ", strip=True))
        if value and value not in values:
            values.append(value)
    return " | ".join(values)


def extract_card(card: Tag) -> dict[str, str] | None:
    """Extract fields from one browser-visible card; never request its links."""
    name_element = card.select_one("h5")
    company_name = normalize_text(name_element.get_text(" ", strip=True)) if name_element else ""
    if not company_name or not any(character.isalnum() for character in company_name):
        return None

    website_element = card.select_one(".address.details .web")
    website = ""
    if website_element is not None:
        website_link = website_element.select_one("a[href]")
        website = (
            website_link["href"].strip()
            if website_link is not None
            else normalize_text(website_element.get_text(" ", strip=True))
        )

    location_element = card.select_one(".location, .park-location, .company-location")
    return {
        "company_name": company_name,
        "phone": joined_text(card.select(".address.details .phone")),
        "website": website,
        "domain": joined_text(card.select(".domain .domain-items > span")),
        "infopark_profile_url": first_link_matching(card, "Company Profile", is_profile_url),
        "infopark_job_url": first_link_matching(card, "Job Openings", is_job_url),
        "source_url": DIRECTORY_URL,
        "location": (
            normalize_text(location_element.get_text(" ", strip=True))
            if location_element is not None
            else ""
        ),
    }


def parse_cards(html: str) -> tuple[list[dict[str, str]], int]:
    """Parse the current page's `.company-profile .compy` card structure."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".company-profile .compy")
    records: list[dict[str, str]] = []
    missing_names = 0
    for card in cards:
        record = extract_card(card)
        if record is None:
            missing_names += 1
        else:
            records.append(record)
    return records, missing_names


def record_key(record: dict[str, str]) -> tuple[str, ...]:
    """Use profile identity first and a name/location fallback only when necessary."""
    if record["infopark_profile_url"]:
        return "profile", record["infopark_profile_url"].casefold()
    return "fallback", normalize_text(record["company_name"]).casefold(), record["location"].casefold()


def validate_record(record: dict[str, str]) -> None:
    """Validate mandatory fields and card-provided Infopark links before saving."""
    if not record["company_name"] or not any(char.isalnum() for char in record["company_name"]):
        raise ValueError("Company name is blank or a punctuation-only placeholder.")
    if record["source_url"] != DIRECTORY_URL:
        raise ValueError(f"Unexpected source URL: {record['source_url']}")
    if record["infopark_profile_url"] and not is_profile_url(record["infopark_profile_url"]):
        raise ValueError(f"Invalid Infopark profile URL: {record['infopark_profile_url']}")
    if record["infopark_job_url"] and not is_job_url(record["infopark_job_url"]):
        raise ValueError(f"Invalid Infopark job URL: {record['infopark_job_url']}")


def load_checkpoint() -> tuple[dict[tuple[str, ...], dict[str, str]], list[tuple[str, ...]]]:
    """Load a valid existing output so interrupted page processing can resume safely."""
    if not OUTPUT_FILE.exists():
        return {}, []
    records = csv_read(OUTPUT_FILE, OUTPUT_COLUMNS)
    index: dict[tuple[str, ...], dict[str, str]] = {}
    order: list[tuple[str, ...]] = []
    for record in records:
        validate_record(record)
        key = record_key(record)
        if key in index:
            raise ValueError(f"Duplicate checkpoint identity: {key}")
        index[key] = record
        order.append(key)
    return index, order


def checkpoint_records(
    checkpoint: dict[tuple[str, ...], dict[str, str]], order: list[tuple[str, ...]]
) -> list[dict[str, str]]:
    return [checkpoint[key] for key in order if key in checkpoint]


def print_diagnostics(
    page_results: list[tuple[str, int, int]],
    records: list[dict[str, str]],
    raw_cards: int,
    source_duplicates: int,
    requested_urls: list[str],
    initial_status: int | None,
) -> None:
    """Print all required mechanism and extraction observations from official pages."""
    website_count = sum(bool(record["website"]) for record in records)
    domain_count = sum(bool(record["domain"]) for record in records)
    profile_count = sum(bool(record["infopark_profile_url"]) for record in records)
    job_count = sum(bool(record["infopark_job_url"]) for record in records)
    unique_names = {normalize_text(record["company_name"]).casefold() for record in records}
    print("\nInfopark Stage 1 diagnostics")
    print("-----------------------------")
    print(f"Initial page URL: {DIRECTORY_URL}")
    print(f"Initial page HTTP status: {initial_status if initial_status is not None else 'failed'}")
    print("Pagination mechanism: public GET links in ul.pagination using the page query parameter")
    print(f"Number of pages discovered: {len(requested_urls)}")
    for page_url, card_count, missing_names in page_results:
        message = f"Page {display_page_number(page_url)} -> {card_count} valid cards"
        if missing_names:
            message += f"; {missing_names} missing-name card(s) skipped and logged"
        print(message)
    print(f"Total raw company cards: {raw_cards}")
    print(f"Unique company names: {len(unique_names)}")
    print(f"Unique company records: {len(records)}")
    print(f"Duplicate records removed: {source_duplicates}")
    print(f"Websites found: {website_count}")
    print(f"Domain values found: {domain_count}")
    print(f"Profile URLs found: {profile_count}")
    print(f"Job URLs found: {job_count}")
    print("HTTP methods used: GET")
    print("AJAX required: no")
    print("POST required: no")
    print("Requests made:")
    for page_url in requested_urls:
        print(f"GET {page_url}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect all public Infopark directory cards without following card links."
    )
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="inspect all official directory pages and print counts without writing a CSV",
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="inspect the first three current cards without writing a CSV",
    )
    arguments = parser.parse_args()

    errors = csv_read(ERROR_FILE, ERROR_COLUMNS) if ERROR_FILE.exists() else []
    try:
        checkpoint, checkpoint_order = load_checkpoint()
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Kerala-JobHunt-Infopark-Research/1.0 "
                    "(official public directory collection; no profile/job/site requests)"
                ),
                "Accept": "text/html,application/xhtml+xml",
            }
        )

        pending_urls = [DIRECTORY_URL]
        seen_urls: set[str] = set()
        requested_urls: list[str] = []
        page_results: list[tuple[str, int, int]] = []
        source_records: dict[tuple[str, ...], dict[str, str]] = {}
        raw_cards = 0
        source_duplicates = 0
        failed_pages = 0
        initial_status: int | None = None

        while pending_urls:
            if len(requested_urls) >= MAX_PAGE_GUARD:
                raise RuntimeError(f"Stopped at the {MAX_PAGE_GUARD}-page safety guard.")
            page_url = pending_urls.pop(0)
            if page_url in seen_urls:
                continue
            if requested_urls:
                time.sleep(REQUEST_DELAY_SECONDS)
            print(f"Fetching directory page: {page_url}")
            html, status_code, fetch_error = fetch_directory_page(session, page_url)
            requested_urls.append(page_url)
            seen_urls.add(page_url)
            if initial_status is None:
                initial_status = status_code
            if html is None:
                failed_pages += 1
                add_error(errors, page_url, "HTTP_ERROR", fetch_error or "Directory request failed")
                if errors and not arguments.diagnose and not arguments.test_only:
                    atomic_csv_write(errors, ERROR_FILE, ERROR_COLUMNS)
                continue

            records, missing_names = parse_cards(html)
            raw_cards += len(records) + missing_names
            page_results.append((page_url, len(records), missing_names))
            if missing_names:
                add_error(
                    errors,
                    page_url,
                    "MISSING_COMPANY_NAME",
                    f"{missing_names} card(s) skipped because the card had no usable displayed company name",
                )
            if not records:
                add_error(errors, page_url, "PARSE_ERROR", "No visible company cards were found")

            for record in records:
                validate_record(record)
                key = record_key(record)
                prior_source = source_records.get(key)
                if prior_source is not None:
                    source_duplicates += 1
                    if prior_source != record:
                        add_error(
                            errors,
                            page_url,
                            "DUPLICATE",
                            f"Conflicting duplicate card retained first source record for {record['company_name']}",
                        )
                    continue
                source_records[key] = record
                if key not in checkpoint:
                    checkpoint_order.append(key)
                checkpoint[key] = record

            for pagination_url in discover_pagination_urls(html, page_url):
                if pagination_url not in seen_urls and pagination_url not in pending_urls:
                    pending_urls.append(pagination_url)

            if not arguments.diagnose and not arguments.test_only:
                atomic_csv_write(checkpoint_records(checkpoint, checkpoint_order), OUTPUT_FILE, OUTPUT_COLUMNS)
                if errors:
                    atomic_csv_write(errors, ERROR_FILE, ERROR_COLUMNS)

        if not source_records:
            raise RuntimeError("No valid company cards were found; no output was written.")
        source_values = list(source_records.values())
        print_diagnostics(
            page_results,
            source_values,
            raw_cards,
            source_duplicates,
            requested_urls,
            initial_status,
        )
        print("\nFirst three parsed cards:")
        for number, record in enumerate(source_values[:3], start=1):
            print(f"{number}. {record['company_name']} | {record['phone'] or '(no phone)'} | {record['website'] or '(no website)'}")
        if arguments.diagnose or arguments.test_only:
            return

        saved_records = checkpoint_records(checkpoint, checkpoint_order)
        if len({record_key(record) for record in saved_records}) != len(saved_records):
            raise RuntimeError("Duplicate company identity remains in the saved CSV.")
        for record in saved_records:
            validate_record(record)

        print("\nInfopark Stage 1 Summary")
        print("-------------------------")
        print(f"Pages discovered: {len(requested_urls)}")
        print(f"Pages successfully processed: {len(page_results)}")
        print(f"Total raw company cards: {raw_cards}")
        print(f"Unique companies: {len(saved_records)}")
        print(f"Duplicates removed: {source_duplicates}")
        print(f"Companies with phone: {sum(bool(record['phone']) for record in saved_records)}")
        print(f"Companies with website: {sum(bool(record['website']) for record in saved_records)}")
        print(f"Companies with domain: {sum(bool(record['domain']) for record in saved_records)}")
        print(f"Companies with profile URL: {sum(bool(record['infopark_profile_url']) for record in saved_records)}")
        print(f"Companies with job URL: {sum(bool(record['infopark_job_url']) for record in saved_records)}")
        print(f"Missing company names: {sum(not record['company_name'] for record in saved_records)}")
        print(f"Failed pages: {failed_pages}")
        print(f"Output: {OUTPUT_FILE.name}")
    except (OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
