"""Extract public company names and website URLs from UL CyberPark's directory."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


SOURCE_URL = "https://www.ulcyberpark.com/companies"
OUTPUT_BASENAME = "ulcyberpark_companies.csv"
TIMEOUT_SECONDS = 20
HEADERS = {
    "User-Agent": "Kerala-JobHunt-ULCyberPark-Directory/1.0 (public directory research; no login)",
    "Accept": "text/html,application/xhtml+xml",
}


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def valid_website(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def safe_output_path(directory: Path, requested_name: str) -> Path:
    """Avoid overwriting an existing CSV by choosing the next numbered name."""
    requested = directory / requested_name
    if not requested.exists():
        return requested
    for number in range(1, 10_000):
        candidate = directory / f"{requested.stem}_{number}{requested.suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError("Could not find an unused CSV output filename.")


def discover_linked_directory_pages(soup: BeautifulSoup, current_url: str) -> list[str]:
    """Return explicitly linked pagination pages only; never construct guessed URLs."""
    candidates: list[str] = []
    seen: set[str] = {current_url}
    pagination_selectors = (
        ".pagination a[href], .pager a[href], nav[aria-label*='pagination' i] a[href], "
        "a[rel='next'][href], a[aria-label*='next' i][href]"
    )
    for link in soup.select(pagination_selectors):
        href = (link.get("href") or "").strip()
        if not href:
            continue
        url = urljoin(current_url, href)
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or url in seen:
            continue
        seen.add(url)
        candidates.append(url)
    return candidates


def dynamic_loading_indicators(soup: BeautifulSoup) -> list[str]:
    """Detect visible directory controls that ordinary linked-page discovery cannot follow."""
    indicators: list[str] = []
    for element in soup.select("[data-load-more], .load-more, .load_more, button[id*='load' i], button[class*='load' i]"):
        label = normalize_whitespace(element.get_text(" ", strip=True)) or element.name
        indicators.append(label)
    return indicators


def extract_records(soup: BeautifulSoup) -> tuple[list[tuple[str, str]], int, int]:
    """Return valid directory records, card count, and incomplete-card count."""
    records: list[tuple[str, str]] = []
    # The page also uses a.com_link for alphabetical jump links.  A company
    # record must contain the nested visual card described by the directory.
    cards = [link for link in soup.select("a.com_link") if link.select_one(".card.com_card, .com_card")]
    invalid = 0
    for card in cards:
        website = (card.get("href") or "").strip()
        title = card.select_one(".card-title")
        company_name = normalize_whitespace(title.get_text(" ", strip=True)) if title else ""
        if not company_name or not valid_website(website):
            invalid += 1
            continue
        records.append((company_name, website))
    return records, len(cards), invalid


def dedupe_key(company_name: str, website: str) -> tuple[str, str]:
    return normalize_whitespace(company_name).casefold(), website.strip().casefold()


def write_csv(path: Path, records: list[tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["company_name", "website"])
        writer.writerows(records)


def validate_csv(path: Path, expected_rows: int) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header != ["company_name", "website"]:
            raise ValueError(f"Unexpected CSV header: {header!r}")
        rows = list(reader)
    if len(rows) != expected_rows:
        raise ValueError(f"CSV contains {len(rows)} rows; expected {expected_rows}.")
    if any(len(row) != 2 or not row[0].strip() or not row[1].strip() for row in rows):
        raise ValueError("CSV contains an incomplete data row.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=OUTPUT_BASENAME, help="CSV filename to create in this script directory")
    arguments = parser.parse_args()

    script_directory = Path(__file__).resolve().parent
    requested_output = Path(arguments.output)
    if requested_output.name != arguments.output or requested_output.suffix.casefold() != ".csv":
        parser.error("--output must be a CSV filename, not a path")
    output_path = safe_output_path(script_directory, requested_output.name)

    session = requests.Session()
    session.headers.update(HEADERS)
    pages_to_fetch = [SOURCE_URL]
    fetched_pages: set[str] = set()
    records: list[tuple[str, str]] = []
    seen_records: set[tuple[str, str]] = set()
    card_count = 0
    invalid_count = 0
    duplicate_count = 0
    dynamic_indicators: list[str] = []

    try:
        while pages_to_fetch:
            page_url = pages_to_fetch.pop(0)
            if page_url in fetched_pages:
                continue
            response = session.get(page_url, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").casefold()
            if "html" not in content_type:
                raise RuntimeError(f"Directory returned unsupported content type: {content_type or 'unknown'}")
            fetched_pages.add(response.url)
            soup = BeautifulSoup(response.text, "html.parser")
            page_records, page_cards, page_invalid = extract_records(soup)
            card_count += page_cards
            invalid_count += page_invalid
            dynamic_indicators.extend(dynamic_loading_indicators(soup))

            for discovered_page in discover_linked_directory_pages(soup, response.url):
                if discovered_page not in fetched_pages and discovered_page not in pages_to_fetch:
                    pages_to_fetch.append(discovered_page)

            for company_name, website in page_records:
                key = dedupe_key(company_name, website)
                if key in seen_records:
                    duplicate_count += 1
                    continue
                seen_records.add(key)
                records.append((company_name, website))
    except requests.RequestException as error:
        print(f"Directory request failed: {error}", file=sys.stderr)
        return 1
    except RuntimeError as error:
        print(f"Directory processing failed: {error}", file=sys.stderr)
        return 1

    if not records:
        print("No valid company records were extracted. The directory HTML may have changed.", file=sys.stderr)
        print(f"Source URL: {SOURCE_URL}", file=sys.stderr)
        print(f"Company cards discovered: {card_count}", file=sys.stderr)
        return 1

    try:
        write_csv(output_path, records)
        validate_csv(output_path, len(records))
    except (OSError, ValueError) as error:
        print(f"CSV output or validation failed: {error}", file=sys.stderr)
        return 1

    print("UL CyberPark directory extraction")
    print(f"Source URL: {SOURCE_URL}")
    print(f"Directory pages processed: {len(fetched_pages)}")
    print(f"Company cards discovered: {card_count}")
    print(f"Valid unique records: {len(records)}")
    print(f"Duplicate records skipped: {duplicate_count}")
    print(f"Invalid or incomplete records skipped: {invalid_count}")
    print(f"Pagination links detected: {'Yes' if len(fetched_pages) > 1 else 'No'}")
    print(f"Dynamic loading indicators detected: {'Yes' if dynamic_indicators else 'No'}")
    if dynamic_indicators:
        print("Dynamic loading limitation: indicators were found, but only ordinary linked public pages were fetched.")
    if output_path.name != requested_output.name:
        print(f"Existing output was preserved; wrote safe alternative: {output_path}")
    else:
        print(f"Output CSV: {output_path}")
    print(f"CSV validation: passed ({len(records)} data rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
