"""Stage 2: enrich Cyberpark directory companies from official listing pages only."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag


DIRECTORY_URL = "https://cyberparks.in/companies-at-park/"
INPUT_FILE = Path(__file__).with_name("cyberpark_companies.csv")
OUTPUT_FILE = Path(__file__).with_name("cyberpark_company_enriched.csv")
ERROR_FILE = Path(__file__).with_name("cyberpark_enrichment_errors.csv")
REQUEST_TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 0.75

INPUT_COLUMNS = [
    "company_name",
    "website",
    "cyberpark_listing_url",
    "source_url",
    "location",
]
OUTPUT_COLUMNS = [
    "company_name",
    "address",
    "pincode",
    "phone",
    "email",
    "website",
    "contact_name",
    "designation",
    "company_description",
    "domain_expertise",
    "cyberpark_listing_url",
    "source_url",
    "it_relevance",
    "developer_relevance",
    "primary_technology_area",
    "relevant_roles",
    "priority",
    "job_match_reason",
    "email_angle",
    "research_status",
    "notes",
]
ERROR_COLUMNS = ["timestamp", "url", "error_type", "error_message"]


def normalize_text(value: str) -> str:
    """Retain the source wording while normalizing presentation whitespace."""
    return " ".join(value.split())


def empty_output_record(input_record: dict[str, str]) -> dict[str, str]:
    """Start an output row without altering the Stage 1 company identity."""
    record = {column: "" for column in OUTPUT_COLUMNS}
    record["company_name"] = input_record["company_name"]
    record["cyberpark_listing_url"] = input_record["cyberpark_listing_url"]
    record["source_url"] = input_record["source_url"]
    return record


def read_csv(path: Path, expected_columns: list[str]) -> list[dict[str, str]]:
    """Read a UTF-8 CSV only when its schema exactly matches expectations."""
    try:
        with path.open(encoding="utf-8-sig", newline="") as file_handle:
            reader = csv.DictReader(file_handle)
            if reader.fieldnames != expected_columns:
                raise ValueError(
                    f"Unexpected columns in {path.name}: {reader.fieldnames}; "
                    f"expected {expected_columns}"
                )
            return list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read {path}: {error}") from error


def write_csv_atomically(
    records: list[dict[str, str]], path: Path, columns: list[str]
) -> None:
    """Publish a complete checkpoint only after the temporary CSV is durable."""
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        with temporary.open("w", encoding="utf-8-sig", newline="") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(records)
            file_handle.flush()
            os.fsync(file_handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def is_listing_url(url: str) -> bool:
    """Accept only the public Cyberpark listing URLs supplied by Stage 1."""
    parsed = urlparse(url)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc == "cyberparks.in"
        and parsed.path.startswith("/listings/")
        and parsed.path != "/listings/"
    )


def validate_input(records: list[dict[str, str]]) -> None:
    """Protect Stage 2 from malformed or duplicate Stage 1 input."""
    if not records:
        raise ValueError("Stage 1 input has no records.")
    listing_urls: set[str] = set()
    names: set[str] = set()
    for record in records:
        if not normalize_text(record["company_name"]):
            raise ValueError("Stage 1 input contains a blank company name.")
        if not is_listing_url(record["cyberpark_listing_url"]):
            raise ValueError(
                f"Stage 1 input has an invalid listing URL: {record['cyberpark_listing_url']}"
            )
        listing_key = record["cyberpark_listing_url"].casefold()
        name_key = normalize_text(record["company_name"]).casefold()
        if listing_key in listing_urls:
            raise ValueError(f"Duplicate listing URL in Stage 1 input: {record['cyberpark_listing_url']}")
        if name_key in names:
            raise ValueError(f"Duplicate company name in Stage 1 input: {record['company_name']}")
        listing_urls.add(listing_key)
        names.add(name_key)


def output_key(record: dict[str, str]) -> str:
    return record["cyberpark_listing_url"].casefold()


def validate_existing_output(
    records: list[dict[str, str]], input_by_url: dict[str, dict[str, str]]
) -> dict[str, dict[str, str]]:
    """Load only compatible checkpoints and verify they still map to Stage 1."""
    indexed: dict[str, dict[str, str]] = {}
    for record in records:
        key = output_key(record)
        input_record = input_by_url.get(key)
        if input_record is None:
            raise ValueError(f"Checkpoint has a listing URL absent from Stage 1 input: {key}")
        if key in indexed:
            raise ValueError(f"Duplicate listing URL in Stage 2 checkpoint: {key}")
        if record["company_name"] != input_record["company_name"]:
            raise ValueError(
                "Checkpoint company name differs from its Stage 1 input; "
                "the original company name must be preserved."
            )
        indexed[key] = record
    return indexed


def load_errors() -> list[dict[str, str]]:
    if not ERROR_FILE.exists():
        return []
    return read_csv(ERROR_FILE, ERROR_COLUMNS)


def add_error(
    errors: list[dict[str, str]], url: str, error_type: str, error_message: str
) -> None:
    """Keep a stable, deduplicated error log across resume runs."""
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


def fetch_listing(session: requests.Session, url: str) -> tuple[str | None, str | None]:
    """Fetch one permitted official listing with one conservative transient retry."""
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
            time.sleep(REQUEST_DELAY_SECONDS)
    return None, last_error


def li_value(item: Tag, title: str) -> str:
    """Get text after a listing label without rewriting the supplied value."""
    full_text = normalize_text(item.get_text(" ", strip=True))
    if full_text.casefold().startswith(title.casefold()):
        return normalize_text(full_text[len(title) :].lstrip(" :"))
    return full_text


def append_field(record: dict[str, str], field: str, value: str) -> None:
    """Retain all source-present values when a page presents a field repeatedly."""
    value = normalize_text(value)
    if not value:
        return
    if not record[field]:
        record[field] = value
    elif value.casefold() not in {item.casefold() for item in record[field].split(" | ")}:
        record[field] = f"{record[field]} | {value}"


def extract_listing(input_record: dict[str, str], html: str) -> dict[str, str]:
    """Extract raw values exactly from a Cyberpark listing; do not request linked sites."""
    record = empty_output_record(input_record)
    soup = BeautifulSoup(html, "html.parser")
    profile = soup.select_one(".profile")
    if profile is None:
        raise ValueError("The listing did not contain the expected Cyberpark .profile panel.")

    listed_name = ""
    for item in profile.select(".profile_main .list-sx > li"):
        title_element = item.find("div", class_="tit", recursive=False)
        if title_element is None:
            continue
        title = normalize_text(title_element.get_text(" ", strip=True))
        title_key = title.casefold().strip(" :")
        value = li_value(item, title)
        if title_key == "company name":
            listed_name = value
        elif title_key in {"address", "pincode", "phone"}:
            append_field(record, title_key, value)
        elif title_key == "email":
            mail_link = item.select_one("a[href^='mailto:']")
            append_field(record, "email", mail_link["href"].split(":", 1)[1] if mail_link else value)
        elif title_key == "website":
            website_link = item.select_one("a[href]")
            append_field(record, "website", website_link["href"].strip() if website_link else value)
        elif title and value:
            append_field(record, "designation", title.strip(" :"))
            append_field(record, "contact_name", value)

    information_panels = [
        panel
        for panel in profile.find_all("div", recursive=False)
        if panel.select_one("h2") is not None
    ]
    if information_panels:
        panel = information_panels[0]
        descriptions = {
            normalize_text(paragraph.get_text(" ", strip=True))
            for paragraph in panel.find_all("p")
            if normalize_text(paragraph.get_text(" ", strip=True))
        }
        if descriptions:
            record["company_description"] = max(descriptions, key=len)
        domain_element = panel.find(["h7", "h6"])
        if domain_element is not None:
            domain_text = normalize_text(domain_element.get_text(" ", strip=True))
            match = re.match(r"domain\s+expertise\s*:\s*(.*)", domain_text, flags=re.IGNORECASE)
            record["domain_expertise"] = normalize_text(match.group(1)) if match else domain_text

    notes: list[str] = []
    listed_name_key = normalize_text(listed_name).rstrip(" .").casefold()
    directory_name_key = normalize_text(record["company_name"]).rstrip(" .").casefold()
    if listed_name and listed_name_key != directory_name_key:
        notes.append("Listing-displayed company name differs from the preserved Stage 1 directory name.")
    assign_research_status(record, notes)
    return record


def contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def classify_record(record: dict[str, str]) -> None:
    """Derive job-fit fields from Cyberpark's own description and expertise only."""
    source_text = " ".join(
        value for value in (record["company_description"], record["domain_expertise"]) if value
    ).casefold()
    areas: list[str] = []

    def add_area(area: str, phrases: tuple[str, ...]) -> bool:
        if contains_any(source_text, phrases):
            areas.append(area)
            return True
        return False

    web = add_area("Web Development", ("web development", "web application", "web solution"))
    mobile = add_area("Mobile Development", ("mobile app", "mobile application", "mobile development"))
    ecommerce = add_area("E-commerce", ("e-commerce", "ecommerce", "marketplace"))
    software = add_area(
        "Software Development",
        ("software development", "custom software", "application development", "software solution"),
    )
    full_stack = add_area("Full-Stack Development", ("full stack", "full-stack"))
    add_area("SaaS", ("saas", "software as a service"))
    add_area("AI/ML", ("artificial intelligence", "machine learning", " ai ", " ai-"))
    add_area("Cloud/DevOps", ("cloud", "devops", "infrastructure as a service"))
    security = add_area("Cybersecurity", ("cybersecurity", "cyber security", "information security"))
    add_area("FinTech", ("fintech", "financial technology"))
    add_area("EdTech", ("edtech", "e-learning", "education technology"))
    add_area("Healthcare IT", ("healthcare", "health care", "medical software"))
    enterprise = add_area("Enterprise Software", ("enterprise software", "enterprise solution"))
    if not enterprise and re.search(r"\berp\b", source_text):
        areas.append("Enterprise Software")
    digital = add_area("Digital Solutions", ("digital solution", "digital transformation", "digital branding"))
    consulting = add_area("IT Consulting", ("it consulting", "technology consulting", "software consulting"))
    it_services = add_area(
        "IT Services",
        ("it services", "it service", "technology service", "it outsourcing", "software services"),
    )
    product = add_area("Software Product", ("software product", "product development"))

    developer_evidence = web or mobile or ecommerce or software or full_stack or product
    it_evidence = developer_evidence or any(
        area in areas
        for area in (
            "SaaS",
            "AI/ML",
            "Cloud/DevOps",
            "Cybersecurity",
            "FinTech",
            "EdTech",
            "Healthcare IT",
            "Enterprise Software",
            "Digital Solutions",
            "IT Consulting",
            "IT Services",
        )
    )

    record["it_relevance"] = "High" if developer_evidence else "Medium" if it_evidence else "Low"
    record["developer_relevance"] = (
        "High" if developer_evidence else "Medium" if it_evidence else "Low"
    )
    record["priority"] = "High" if developer_evidence else "Medium" if it_evidence else "Low"
    record["primary_technology_area"] = " / ".join(areas) if areas else "Other"

    roles: list[str] = []
    if web or ecommerce or full_stack:
        roles.extend(["Full-Stack Developer", "Web Developer", "Frontend Developer", "Backend Developer"])
    if software or product or full_stack:
        roles.extend(["Software Developer", "Software Engineer"])
    if mobile:
        roles.append("Mobile Developer")
    record["relevant_roles"] = ", ".join(dict.fromkeys(roles))

    if developer_evidence:
        evidence = " and ".join(areas[:3]) if areas else "software development"
        record["job_match_reason"] = (
            f"Strong match because Cyberpark describes the company’s work as {evidence}, "
            "which aligns with full-stack software development."
        )
        record["email_angle"] = (
            f"Your stated work in {evidence} aligns closely with my full-stack software development experience."
        )
    elif it_evidence:
        evidence = " and ".join(areas[:3]) if areas else "technology services"
        record["job_match_reason"] = (
            f"Technology-relevant match because Cyberpark lists {evidence}, though direct "
            "software-development activity is not clearly stated."
        )
        record["email_angle"] = (
            f"I’m interested in your stated work in {evidence} and its possible overlap with software development."
        )
    else:
        record["job_match_reason"] = (
            "Cyberpark’s listing does not provide enough stated software-development activity "
            "to establish a strong match."
        )
        record["email_angle"] = "Cyberpark’s listing does not provide a specific software-development outreach angle."


def assign_research_status(record: dict[str, str], notes: list[str]) -> None:
    """Set a source-extraction status before derived fields are populated."""
    source_detail = any(
        record[field]
        for field in (
            "address",
            "pincode",
            "phone",
            "email",
            "website",
            "contact_name",
            "designation",
            "company_description",
            "domain_expertise",
        )
    )
    public_contact = any(record[field] for field in ("phone", "email", "contact_name"))
    if not source_detail:
        record["research_status"] = "partial"
        notes.append("Listing profile was found but did not expose extractable company detail fields.")
    elif not public_contact:
        record["research_status"] = "no_public_contact"
    elif not record["company_description"] and not record["domain_expertise"]:
        record["research_status"] = "partial"
        notes.append("Listing has contact detail but no company description or domain expertise.")
    else:
        record["research_status"] = "success"
    record["notes"] = " ".join(notes)


def failed_record(input_record: dict[str, str], message: str) -> dict[str, str]:
    record = empty_output_record(input_record)
    record["research_status"] = "failed"
    record["notes"] = message
    classify_record(record)
    return record


def ordered_records(
    input_records: list[dict[str, str]], saved_by_url: dict[str, dict[str, str]]
) -> list[dict[str, str]]:
    """Keep output deterministic and in Stage 1 directory order."""
    return [
        saved_by_url[output_key(record)]
        for record in input_records
        if output_key(record) in saved_by_url
    ]


def report(records: list[dict[str, str]], input_count: int) -> None:
    """Print the requested final integrity and job-relevance summary."""
    def count(field: str, value: str) -> int:
        return sum(record[field] == value for record in records)

    print("\nCyberpark Stage 2 Summary")
    print("-------------------------")
    print(f"Input companies: {input_count}")
    print(f"Output companies: {len(records)}")
    print(f"Successfully processed: {count('research_status', 'success')}")
    print(f"Partial: {count('research_status', 'partial')}")
    print(f"No public contact: {count('research_status', 'no_public_contact')}")
    print(f"Failed: {count('research_status', 'failed')}")
    print(f"Companies with email: {sum(bool(record['email']) for record in records)}")
    print(f"Companies with phone: {sum(bool(record['phone']) for record in records)}")
    print(f"Companies with contact person: {sum(bool(record['contact_name']) for record in records)}")
    print(f"Companies with domain expertise: {sum(bool(record['domain_expertise']) for record in records)}")
    print(f"Companies with descriptions: {sum(bool(record['company_description']) for record in records)}")
    for field, label in (("it_relevance", "IT relevance"), ("developer_relevance", "Developer relevance"), ("priority", "Priority")):
        for value in ("High", "Medium", "Low"):
            print(f"{label} {value}: {count(field, value)}")
    listing_urls = [record["cyberpark_listing_url"] for record in records]
    names = [normalize_text(record["company_name"]).casefold() for record in records]
    print(f"Duplicate companies: {len(names) - len(set(names))}")
    print(f"Duplicate Cyberpark URLs: {len(listing_urls) - len(set(listing_urls))}")
    print(f"Missing Cyberpark URLs: {sum(not url for url in listing_urls)}")
    print(f"Output: {OUTPUT_FILE.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enrich Stage 1 Cyberpark records from official listing pages only."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="process at most this many not-yet-checkpointed records (for a safe test)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="re-fetch checkpointed records; use only when deliberately refreshing source data",
    )
    parser.add_argument(
        "--reclassify",
        action="store_true",
        help="recompute derived fields from saved raw Cyberpark data without network requests",
    )
    arguments = parser.parse_args()
    if arguments.limit < 0:
        parser.error("--limit must be zero or positive")

    try:
        input_records = read_csv(INPUT_FILE, INPUT_COLUMNS)
        validate_input(input_records)
        input_by_url = {output_key(record): record for record in input_records}
        existing_records = read_csv(OUTPUT_FILE, OUTPUT_COLUMNS) if OUTPUT_FILE.exists() else []
        saved_by_url = validate_existing_output(existing_records, input_by_url)
        errors = load_errors()

        if arguments.reclassify:
            for record in saved_by_url.values():
                classify_record(record)
            final_records = ordered_records(input_records, saved_by_url)
            write_csv_atomically(final_records, OUTPUT_FILE, OUTPUT_COLUMNS)
            report(final_records, len(input_records))
            return

        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Kerala-JobHunt-Cyberpark-Research/2.0 "
                    "(official listing extraction; no company-website requests)"
                ),
                "Accept": "text/html,application/xhtml+xml",
            }
        )

        processed_this_run = 0
        request_count = 0
        for input_record in input_records:
            key = output_key(input_record)
            if key in saved_by_url and not arguments.refresh:
                continue
            if arguments.limit and processed_this_run >= arguments.limit:
                break
            if request_count:
                time.sleep(REQUEST_DELAY_SECONDS)
            print(f"Fetching official listing: {input_record['cyberpark_listing_url']}")
            html, fetch_error = fetch_listing(session, input_record["cyberpark_listing_url"])
            request_count += 1
            if html is None:
                message = fetch_error or "Official listing request failed"
                add_error(errors, input_record["cyberpark_listing_url"], "HTTP_ERROR", message)
                record = failed_record(input_record, message)
            else:
                try:
                    record = extract_listing(input_record, html)
                    classify_record(record)
                except ValueError as error:
                    message = str(error)
                    add_error(errors, input_record["cyberpark_listing_url"], "PARSE_ERROR", message)
                    record = failed_record(input_record, message)
            saved_by_url[key] = record
            processed_this_run += 1
            write_csv_atomically(ordered_records(input_records, saved_by_url), OUTPUT_FILE, OUTPUT_COLUMNS)
            if errors:
                write_csv_atomically(errors, ERROR_FILE, ERROR_COLUMNS)

        final_records = ordered_records(input_records, saved_by_url)
        if len(final_records) == len(input_records):
            if len({output_key(record) for record in final_records}) != len(input_records):
                raise ValueError("Stage 2 output has duplicate Cyberpark listing URLs.")
            if any(record["company_name"] != input_by_url[output_key(record)]["company_name"] for record in final_records):
                raise ValueError("Stage 2 output changed a Stage 1 company name.")
        report(final_records, len(input_records))
    except (OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
