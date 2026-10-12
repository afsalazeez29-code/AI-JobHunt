"""Collect only public company-list data from Cyberpark's Companies At Park page."""

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


SOURCE_URL = "https://cyberparks.in/companies-at-park/"
LOCATION = "Kozhikode, Kerala"
OUTPUT_FILE = Path(__file__).with_name("cyberpark_companies.csv")
ERROR_FILE = Path(__file__).with_name("errors.csv")
REQUEST_TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 1
MAX_PAGE_GUARD = 100
OUTPUT_COLUMNS = [
    "company_name",
    "website",
    "cyberpark_listing_url",
    "source_url",
    "location",
]
ERROR_COLUMNS = ["timestamp", "url", "error_type", "error_message"]


def normalize_text(value: str) -> str:
    """Collapse whitespace while retaining Cyberpark's displayed punctuation."""
    return " ".join(value.split())


def normalized_company_key(company_name: str, website: str) -> tuple[str, str]:
    """Create the specified fallback deduplication key without altering saved values."""
    return normalize_text(company_name).casefold(), website.strip().casefold()


def record_key(record: dict[str, str]) -> tuple[str, ...]:
    """Prefer a Cyberpark listing URL; otherwise use normalized name and website."""
    if record["cyberpark_listing_url"]:
        return "listing", record["cyberpark_listing_url"].casefold()
    return "fallback", *normalized_company_key(record["company_name"], record["website"])


def is_cyberpark_listing_url(url: str) -> bool:
    """Check that a recorded listing URL is an individual Cyberpark listing."""
    parsed = urlparse(url)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc == "cyberparks.in"
        and parsed.path.startswith("/listings/")
        and parsed.path != "/listings/"
    )


def load_csv(path: Path, expected_columns: list[str]) -> list[dict[str, str]]:
    """Load an existing CSV checkpoint with an exact compatible header."""
    try:
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames != expected_columns:
                raise ValueError(
                    f"Unexpected columns in {path.name}: {reader.fieldnames}. "
                    f"Expected: {expected_columns}"
                )
            return list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read {path}: {error}") from error


def load_existing_records() -> list[dict[str, str]]:
    """Load valid records already saved by a prior run, without overwriting them."""
    if not OUTPUT_FILE.exists():
        return []
    records = load_csv(OUTPUT_FILE, OUTPUT_COLUMNS)
    for record in records:
        validate_record(record)
    return records


def load_existing_errors() -> list[dict[str, str]]:
    """Preserve a prior error log if it exists."""
    if not ERROR_FILE.exists():
        return []
    return load_csv(ERROR_FILE, ERROR_COLUMNS)


def write_csv_atomically(
    records: list[dict[str, str]], path: Path, fieldnames: list[str]
) -> None:
    """Write a full temporary CSV, then atomically publish it."""
    temporary_path = path.with_name(f".{path.name}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8-sig", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
            csv_file.flush()
            os.fsync(csv_file.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def add_error(
    errors: list[dict[str, str]], url: str, error_type: str, error_message: str
) -> None:
    """Record a real failure once; optional blank card fields are not errors."""
    if any(
        error["url"] == url
        and error["error_type"] == error_type
        and error["error_message"] == error_message
        for error in errors
    ):
        return
    errors.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "url": url,
            "error_type": error_type,
            "error_message": error_message,
        }
    )


def fetch_directory_page(session: requests.Session, url: str) -> tuple[str | None, str | None]:
    """Fetch an official directory page with one conservative transient retry."""
    last_error = "Unknown request failure"
    for attempt in range(1, 3):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        except (requests.ConnectionError, requests.Timeout) as error:
            last_error = f"{type(error).__name__}: {error}"
            retry = attempt == 1
        except requests.RequestException as error:
            return None, f"{type(error).__name__}: {error}"
        else:
            if response.status_code == 429:
                return None, "HTTP 429 rate limited; not retried"
            if 500 <= response.status_code <= 599:
                last_error = f"HTTP {response.status_code} server error"
                retry = attempt == 1
            elif 200 <= response.status_code < 300:
                return response.text, None
            else:
                return None, f"HTTP {response.status_code}"
        if retry:
            print("Temporary failure; retrying once after 1 second...", file=sys.stderr)
            time.sleep(REQUEST_DELAY_SECONDS)
    return None, last_error


def has_meaningful_company_name(company_name: str) -> bool:
    """Reject blank or placeholder-only names without inferring a replacement."""
    return bool(company_name) and any(character.isalnum() for character in company_name)


def extract_card_record(card: object, source_url: str) -> dict[str, str] | None:
    """Extract only fields present in a directory card; never request its links."""
    name_element = card.select_one(".comp_name")
    company_name = normalize_text(name_element.get_text(" ", strip=True)) if name_element else ""
    if not has_meaningful_company_name(company_name):
        return None

    website = ""
    listing_url = ""
    for link in card.select(".comp_web a[href]"):
        href = link.get("href", "").strip()
        label = normalize_text(link.get_text(" ", strip=True)).casefold()
        absolute_url = urljoin(source_url, href)
        if label == "details" or is_cyberpark_listing_url(absolute_url):
            if is_cyberpark_listing_url(absolute_url):
                listing_url = absolute_url
            continue
        if label == "website" and not website:
            website = href

    return {
        "company_name": company_name,
        "website": website,
        "cyberpark_listing_url": listing_url,
        "source_url": SOURCE_URL,
        "location": LOCATION,
    }


def parse_directory_page(
    html: str, source_url: str
) -> tuple[list[dict[str, str]], int, int]:
    """Parse directory cards using their structural card/name relationship."""
    soup = BeautifulSoup(html, "html.parser")
    # The directory has two equally valid wrappers: ``grid col-300 fit`` and
    # ``grid col-300``.  Selecting the stable card body captures both without
    # depending on presentation-only wrapper classes.
    cards = soup.select(".companies .cmpny-detail")
    records: list[dict[str, str]] = []
    missing_names = 0
    for card in cards:
        record = extract_card_record(card, source_url)
        if record is None:
            missing_names += 1
            continue
        records.append(record)
    return records, len(cards), missing_names


def print_diagnostics(html: str, records: list[dict[str, str]], total_cards: int) -> None:
    """Report the collection mechanism and the original-selector discrepancy."""
    soup = BeautifulSoup(html, "html.parser")
    legacy_cards = len(soup.select(".grid.col-300.fit .cmpny-detail"))
    plain_grid_cards = len(soup.select(".grid.col-300 .cmpny-detail"))
    pagination_urls = discover_pagination_urls(html, SOURCE_URL)
    search_form = soup.select_one("form[name='frm_search']")
    form_method = (search_form.get("method", "GET").upper() if search_form else "not present")
    unique_names = {normalize_text(record["company_name"]).casefold() for record in records}
    unique_records = {record_key(record) for record in records}
    listing_urls = [record["cyberpark_listing_url"] for record in records if record["cyberpark_listing_url"]]
    website_urls = [record["website"] for record in records if record["website"]]
    print("\nCyberpark directory diagnostics")
    print("-------------------------------")
    print(f"Initial rendered directory cards: {total_cards}")
    print(f"Cards matched by the old '.grid.col-300.fit' selector: {legacy_cards}")
    print(f"Cards matched by the inclusive '.grid.col-300' wrapper: {plain_grid_cards}")
    print(f"Records after required public request(s): {len(records)}")
    print(f"Unique company names: {len(unique_names)}")
    print(f"Unique company records: {len(unique_records)}")
    print(f"Listing URLs: {len(listing_urls)} (unique: {len(set(listing_urls))})")
    print(f"Website URLs: {len(website_urls)} (unique: {len(set(website_urls))})")
    print(f"Requests made: GET {SOURCE_URL}")
    print("HTTP methods used: GET")
    print(f"Directory search form method: {form_method} (not used; no filtering is required)")
    print("POST required: no")
    print("AJAX / JavaScript loading required: no; cards are present in the initial HTML")
    print("Filtering required: no")
    print(f"Pagination required: no (pagination links discovered: {len(pagination_urls)})")


def discover_pagination_urls(html: str, current_url: str) -> list[str]:
    """Find official directory pagination links, excluding card and unrelated links."""
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []
    pagination_selectors = ".pagination a[href], .wp-pagenavi a[href], a[rel='next'][href]"
    for link in soup.select(pagination_selectors):
        candidate = urljoin(current_url, link["href"])
        parsed = urlparse(candidate)
        if parsed.netloc == "cyberparks.in" and parsed.path.rstrip("/") == "/companies-at-park":
            if candidate not in urls:
                urls.append(candidate)
    return urls


def validate_record(record: dict[str, str]) -> None:
    """Validate mandatory fields and optional URLs before saving."""
    if not has_meaningful_company_name(record["company_name"]):
        raise ValueError("Company name cannot be blank or a punctuation-only placeholder.")
    if record["source_url"] != SOURCE_URL:
        raise ValueError(f"Unexpected source URL: {record['source_url']}")
    if record["location"] != LOCATION:
        raise ValueError(f"Unexpected location: {record['location']}")
    if record["cyberpark_listing_url"] and not is_cyberpark_listing_url(
        record["cyberpark_listing_url"]
    ):
        raise ValueError(f"Invalid Cyberpark listing URL: {record['cyberpark_listing_url']}")


def merge_records(
    existing_records: list[dict[str, str]],
    new_records: list[dict[str, str]],
    errors: list[dict[str, str]],
) -> tuple[list[dict[str, str]], int, int]:
    """Deduplicate by listing URL or fallback key, retaining the first record."""
    combined: list[dict[str, str]] = []
    seen: dict[tuple[str, ...], dict[str, str]] = {}
    source_duplicates_removed = 0
    checkpoint_matches = 0
    for is_new_record, record in [
        *[(False, record) for record in existing_records],
        *[(True, record) for record in new_records],
    ]:
        validate_record(record)
        key = record_key(record)
        existing = seen.get(key)
        if existing is None:
            seen[key] = record
            combined.append(record)
            continue
        if is_new_record and key in {record_key(item) for item in existing_records}:
            checkpoint_matches += 1
        else:
            source_duplicates_removed += 1
        if existing != record:
            add_error(
                errors,
                record["source_url"],
                "DUPLICATE",
                f"Conflicting duplicate retained first record for {record['company_name']}",
            )
    listing_urls = [record["cyberpark_listing_url"] for record in combined if record["cyberpark_listing_url"]]
    if len(listing_urls) != len(set(listing_urls)):
        raise ValueError("Duplicate Cyberpark listing URLs remain after deduplication.")
    return combined, source_duplicates_removed, checkpoint_matches


def print_test_records(records: list[dict[str, str]]) -> None:
    """Print the required first-three-card selector verification."""
    print("Cyberpark Stage 1 selector test (first 3 cards):")
    for index, record in enumerate(records[:3], start=1):
        print(f"{index}.")
        for field in OUTPUT_COLUMNS:
            print(f"{field}: {record[field] or '(blank)'}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect official Cyberpark Companies At Park directory cards only."
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="run the three-card selector test without creating/updating the CSV",
    )
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="report card counts and request mechanics without creating/updating the CSV",
    )
    arguments = parser.parse_args()

    errors: list[dict[str, str]] = []
    try:
        existing_records = load_existing_records()
        errors = load_existing_errors()
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Kerala-JobHunt-Cyberpark-Research/1.0 "
                    "(official public directory collection; no profile requests)"
                ),
                "Accept": "text/html,application/xhtml+xml",
            }
        )

        requested_urls: list[str] = []
        page_records: list[dict[str, str]] = []
        pending_urls = [SOURCE_URL]
        discovered_urls: set[str] = set()
        first_successful_html: str | None = None
        cards_found = 0
        failed_requests = 0

        while pending_urls:
            if len(requested_urls) >= MAX_PAGE_GUARD:
                raise RuntimeError(f"Stopped at the {MAX_PAGE_GUARD}-page safety guard.")
            page_url = pending_urls.pop(0)
            if page_url in discovered_urls:
                continue
            if requested_urls:
                time.sleep(REQUEST_DELAY_SECONDS)
            print(f"Fetching directory page: {page_url}")
            html, fetch_error = fetch_directory_page(session, page_url)
            requested_urls.append(page_url)
            discovered_urls.add(page_url)
            if html is None:
                failed_requests += 1
                add_error(errors, page_url, "HTTP_ERROR", fetch_error or "Directory request failed")
                continue

            if first_successful_html is None:
                first_successful_html = html

            records, page_card_count, missing_names = parse_directory_page(html, page_url)
            cards_found += page_card_count
            if missing_names:
                add_error(errors, page_url, "MISSING_COMPANY_NAME", f"{missing_names} card(s) skipped")
            if not records:
                add_error(errors, page_url, "PARSE_ERROR", "No company cards found")
            page_records.extend(records)
            for pagination_url in discover_pagination_urls(html, page_url):
                if pagination_url not in discovered_urls and pagination_url not in pending_urls:
                    pending_urls.append(pagination_url)

        if not page_records:
            raise RuntimeError("No valid company records were found; no output was written.")
        # The directory is currently a single server-rendered page.  Print this
        # once from the initial response, even if it later gains pagination.
        if first_successful_html is not None:
            print_diagnostics(first_successful_html, page_records, cards_found)
        print_test_records(page_records)
        if arguments.test_only or arguments.diagnose:
            return

        all_records, duplicates_removed, checkpoint_matches = merge_records(
            existing_records, page_records, errors
        )
        write_csv_atomically(all_records, OUTPUT_FILE, OUTPUT_COLUMNS)
        if errors:
            write_csv_atomically(errors, ERROR_FILE, ERROR_COLUMNS)

        with OUTPUT_FILE.open(encoding="utf-8-sig", newline="") as csv_file:
            saved_records = list(csv.DictReader(csv_file))
        if len(saved_records) != len(all_records):
            raise RuntimeError("Saved CSV row count does not match validated records.")
        for record in saved_records:
            validate_record(record)

        with_website = sum(bool(record["website"]) for record in all_records)
        with_listing_url = sum(bool(record["cyberpark_listing_url"]) for record in all_records)
        website_values = [record["website"] for record in all_records if record["website"]]
        duplicate_website_urls = len(website_values) - len(
            {website.casefold() for website in website_values}
        )
        print("\nCyberpark Stage 1 Summary")
        print("-------------------------")
        print(f"Source: {SOURCE_URL}")
        print(f"Pages requested: {len(requested_urls)}")
        print(f"Company cards found: {cards_found}")
        print(f"Unique companies: {len(all_records)}")
        print(f"Duplicates removed: {duplicates_removed}")
        print(f"Existing checkpoint records matched: {checkpoint_matches}")
        print(f"Companies with website: {with_website}")
        print(f"Companies without website: {len(all_records) - with_website}")
        print(f"Companies with listing URL: {with_listing_url}")
        print(f"Companies without listing URL: {len(all_records) - with_listing_url}")
        print(f"Duplicate nonblank website URLs: {duplicate_website_urls}")
        print(f"Failed requests: {failed_requests}")
        print(f"Output: {OUTPUT_FILE.name}")
    except (OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
