"""Collect publicly listed startups from the Kerala Startup Mission directory."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://startups.startupmission.in"
DIRECTORY_URL = f"{BASE_URL}/startups"
REQUEST_TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 1
MAX_PAGES = 1_000
CSV_COLUMNS = ["id", "company_name", "location", "ksum_url", "source_page"]
PROFILE_PATH_PATTERN = re.compile(r"^/startups/[A-Za-z0-9_-]+/?$")


def normalize_text(text: str) -> str:
    """Collapse line breaks and repeated whitespace into a single space."""
    return " ".join(text.split())


def is_ksum_profile_url(url: str) -> bool:
    """Return whether *url* is an individual public KSUM startup profile URL."""
    parsed_url = urlparse(url)
    return (
        parsed_url.scheme in {"http", "https"}
        and parsed_url.netloc == "startups.startupmission.in"
        and PROFILE_PATH_PATTERN.fullmatch(parsed_url.path) is not None
    )


def fetch_page(session: requests.Session, page_number: int) -> str | None:
    """Fetch one public directory page, returning HTML or None after an error."""
    print(f"Fetching page {page_number}...")
    try:
        response = session.get(
            DIRECTORY_URL,
            params={"page": page_number},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"Error fetching page {page_number}: {error}", file=sys.stderr)
        return None


def parse_startups(html: str, page_number: int) -> list[dict[str, object]]:
    """Extract valid startup cards from one directory page.

    Each directory card is a profile link whose first two direct div children are
    the company name and location. Using that parent-child relationship avoids
    depending on the page's presentation-oriented CSS class names.
    """
    soup = BeautifulSoup(html, "html.parser")
    records: list[dict[str, object]] = []

    for link in soup.find_all("a", href=True):
        profile_url = urljoin(BASE_URL, link["href"])
        if not is_ksum_profile_url(profile_url):
            continue

        card_fields = link.find_all("div", recursive=False)
        if len(card_fields) < 2:
            print(
                f"Warning: skipped incomplete startup card on page {page_number}: "
                f"{profile_url}",
                file=sys.stderr,
            )
            continue

        company_name = normalize_text(card_fields[0].get_text(" ", strip=True))
        location = normalize_text(card_fields[1].get_text(" ", strip=True))
        record = {
            "company_name": company_name,
            "location": location,
            "ksum_url": profile_url,
            "source_page": page_number,
        }
        if not is_valid_record(record):
            print(
                f"Warning: skipped invalid startup card on page {page_number}: "
                f"{profile_url}",
                file=sys.stderr,
            )
            continue
        records.append(record)

    return records


def is_valid_record(record: dict[str, object]) -> bool:
    """Check the required fields before saving a record."""
    return (
        isinstance(record.get("company_name"), str)
        and bool(record["company_name"])
        and isinstance(record.get("location"), str)
        and bool(record["location"])
        and isinstance(record.get("ksum_url"), str)
        and is_ksum_profile_url(record["ksum_url"])
        and isinstance(record.get("source_page"), int)
    )


def deduplicate_records(records: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    """Keep the first occurrence of each KSUM profile URL and assign final IDs."""
    seen_urls: set[str] = set()
    unique_records: list[dict[str, object]] = []
    for record in records:
        profile_url = str(record["ksum_url"])
        if profile_url in seen_urls:
            continue
        seen_urls.add(profile_url)
        unique_records.append({"id": len(unique_records) + 1, **record})
    return unique_records


def save_csv(records: list[dict[str, object]], filename: Path) -> None:
    """Write a new UTF-8-with-BOM CSV, refusing to replace an existing file."""
    if filename.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing file: {filename}. "
            "Move, rename, or remove it before running again."
        )

    with filename.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(records)


def page_has_next(html: str) -> bool:
    """Use KSUM's rendered pagination control to determine whether another page exists."""
    soup = BeautifulSoup(html, "html.parser")
    next_button = soup.find("button", attrs={"dusk": "nextPage"})
    return next_button is not None and not next_button.has_attr("disabled")


def scrape_pages(page_numbers: Iterable[int]) -> tuple[list[dict[str, object]], list[str]]:
    """Collect specified pages sequentially, with a polite delay between requests."""
    all_records: list[dict[str, object]] = []
    page_html: list[str] = []
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "AI-JobHunt-KSUM-Research/1.0 "
                "(public directory collection; polite sequential requests)"
            ),
            "Accept": "text/html,application/xhtml+xml",
        }
    )

    for request_index, page_number in enumerate(page_numbers):
        if request_index:
            time.sleep(REQUEST_DELAY_SECONDS)
        html = fetch_page(session, page_number)
        if html is None:
            continue
        records = parse_startups(html, page_number)
        print(f"Found {len(records)} companies.")
        all_records.extend(records)
        page_html.append(html)

    return all_records, page_html


def print_and_save(records: list[dict[str, object]], output_file: Path) -> None:
    """Print collection totals and save validated, deduplicated records."""
    unique_records = deduplicate_records(records)
    print(f"Total records found before deduplication: {len(records)}")
    print(f"Unique companies: {len(unique_records)}")
    save_csv(unique_records, output_file)
    print(f"Saved to: {output_file.name}")


def scrape_test_pages() -> None:
    """Run the required initial test against directory pages 1 through 3."""
    records, _ = scrape_pages(range(1, 4))
    print_and_save(records, Path(__file__).with_name("ksum_test.csv"))


def scrape_all_pages() -> None:
    """Collect all available directory pages, stopping at KSUM's last-page control."""
    all_records: list[dict[str, object]] = []
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "AI-JobHunt-KSUM-Research/1.0 "
                "(public directory collection; polite sequential requests)"
            ),
            "Accept": "text/html,application/xhtml+xml",
        }
    )

    for page_number in range(1, MAX_PAGES + 1):
        if page_number > 1:
            time.sleep(REQUEST_DELAY_SECONDS)
        html = fetch_page(session, page_number)
        if html is None:
            print("Stopping after a request failure.", file=sys.stderr)
            break

        records = parse_startups(html, page_number)
        print(f"Found {len(records)} companies.")
        if not records:
            print("Stopping because the page contained no startup records.")
            break
        all_records.extend(records)
        if not page_has_next(html):
            print("Reached the last page according to KSUM pagination.")
            break
    else:
        print(
            f"Stopped at the maximum-page safety guard ({MAX_PAGES}).",
            file=sys.stderr,
        )

    print_and_save(all_records, Path(__file__).with_name("ksum_companies.csv"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect publicly listed Kerala Startup Mission companies."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="collect every page instead of the initial pages 1 through 3 test",
    )
    arguments = parser.parse_args()

    try:
        if arguments.all:
            scrape_all_pages()
        else:
            scrape_test_pages()
    except FileExistsError as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
