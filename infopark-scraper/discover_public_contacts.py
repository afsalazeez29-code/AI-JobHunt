"""Stage 2 public-business-contact discovery for frozen Infopark targets."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup, Tag


INPUT_FILE = Path(__file__).with_name("infopark_final_targets.csv")
CONTACT_FILE = Path(__file__).with_name("infopark_stage2_contacts.csv")
STATUS_FILE = Path(__file__).with_name("infopark_stage2_company_status.csv")
AUDIT_FILE = Path(__file__).with_name("infopark_stage2_audit.csv")
ERROR_FILE = Path(__file__).with_name("infopark_stage2_errors.csv")
# A short bounded wait keeps an unreachable public site from stalling the
# complete, checkpointed target set.  Transient failures still receive one
# polite retry below; the official Infopark profile remains the fallback.
REQUEST_TIMEOUT_SECONDS = 5
REQUEST_DELAY_SECONDS = 0.25
MAX_RELEVANT_LINKS = 1
EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}(?![\w.-])", re.IGNORECASE)

TARGET_COLUMNS = [
    "company_name", "phone", "website", "domain", "infopark_profile_url", "infopark_job_url",
    "source_url", "location", "it_relevance", "developer_relevance", "primary_technology_area",
    "relevant_roles", "priority", "job_match_reason", "email_angle", "research_status", "notes",
    "final_priority", "final_review_reason", "stage1_2_status",
]
CONTACT_COLUMNS = [
    *TARGET_COLUMNS,
    "contact_name", "designation", "email", "email_category", "contact_priority",
    "contact_source_url", "source_type", "source_context", "source_confidence", "contact_quality",
    "discovery_status", "stage2_research_status", "research_notes",
]
STATUS_COLUMNS = [
    "company_name", "website", "infopark_profile_url", "final_priority", "public_email_found",
    "email_count", "primary_email", "primary_email_category", "research_status",
    "research_source_count", "notes",
]
AUDIT_COLUMNS = [
    "company_name", "final_priority", "researched", "email_found", "email_count", "primary_email",
    "primary_email_category", "source_type", "contact_source_url", "discovery_status", "audit_result", "notes",
]
ERROR_COLUMNS = ["company_name", "url", "error_type", "error_message", "timestamp", "status"]
FUNCTIONAL_LOCALS = {
    "hr", "careers", "career", "jobs", "job", "recruitment", "recruiter", "hiring", "talent",
    "talentacquisition", "talent-acquisition", "info", "contact", "hello", "enquiries", "enquiry",
    "admin", "office", "support", "sales", "marketing", "accounts", "accounting", "finance",
    "business", "partnerships", "operations", "team", "help", "service", "services", "webmaster",
}
HIRE_CATEGORIES = ("Recruitment", "Hiring", "Careers", "HR", "Talent Acquisition")


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def read_csv(path: Path, columns: list[str]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != columns:
                raise ValueError(f"Unexpected columns in {path.name}: {reader.fieldnames}; expected {columns}")
            return list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read {path}: {error}") from error


def atomic_write(records: list[dict[str, str]], path: Path, columns: list[str]) -> None:
    # OneDrive can independently handle/reconcile a predictable hidden .tmp
    # name.  Give every checkpoint a visible, process-unique sibling instead.
    temporary_path = path.with_name(
        f"{path.stem}.checkpoint-{os.getpid()}-{time.time_ns()}{path.suffix}"
    )
    try:
        with temporary_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(records)
            handle.flush()
            os.fsync(handle.fileno())
        for attempt in range(1, 6):
            try:
                os.replace(temporary_path, path)
                break
            except PermissionError:
                if attempt == 5:
                    raise
                time.sleep(0.25 * attempt)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def normalize_email(value: str) -> str:
    return value.strip().strip("<>()[]{}.,;:'\"").casefold()


def valid_business_email(email: str) -> bool:
    """Retain only functional business inboxes, never inferred personal addresses."""
    if not EMAIL_PATTERN.fullmatch(email):
        return False
    local = email.partition("@")[0].casefold()
    normalized = re.sub(r"[._-]", "", local)
    return local in FUNCTIONAL_LOCALS or normalized in {item.replace("-", "") for item in FUNCTIONAL_LOCALS}


def website_start_url(value: str) -> str:
    """Make a fetch URL from a source-displayed website without changing the saved field."""
    value = value.strip()
    if not value:
        return ""
    if not urlparse(value).scheme:
        value = f"https://{value}"
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", "", ""))


def same_site(candidate: str, root_url: str) -> bool:
    candidate_host = urlparse(candidate).netloc.casefold().removeprefix("www.")
    root_host = urlparse(root_url).netloc.casefold().removeprefix("www.")
    return bool(candidate_host) and candidate_host == root_host


def is_public_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def classify_page_type(url: str, official_infopark: bool = False) -> str:
    if official_infopark:
        return "Official Infopark Directory"
    path = urlparse(url).path.casefold()
    if any(word in path for word in ("career", "jobs", "hiring")):
        return "Official Careers Page"
    if any(word in path for word in ("recruit", "talent")):
        return "Official Recruitment Page"
    if any(word in path for word in ("contact", "support")):
        return "Official Contact Page"
    if any(word in path for word in ("about", "team")):
        return "Official About/Team Page"
    return "Official Website"


def fetch(session: requests.Session, url: str) -> tuple[str | None, str | None, str | None]:
    """Fetch a normal public page once, retrying just one transient failure."""
    last_error = "Unknown request failure"
    for attempt in range(1, 3):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS, allow_redirects=True)
        except (requests.ConnectionError, requests.Timeout) as error:
            last_error = f"{type(error).__name__}: {error}"
            retry = attempt == 1
        except requests.RequestException as error:
            return None, None, f"{type(error).__name__}: {error}"
        else:
            if response.status_code == 429:
                return None, None, "HTTP 429 rate limited; not retried"
            if 500 <= response.status_code <= 599:
                last_error = f"HTTP {response.status_code} server error"
                retry = attempt == 1
            elif 200 <= response.status_code < 300:
                content_type = response.headers.get("content-type", "").casefold()
                if "html" not in content_type:
                    return None, None, f"Unsupported content type: {content_type or 'unknown'}"
                return response.text, response.url, None
            else:
                return None, None, f"HTTP {response.status_code}"
        if retry:
            time.sleep(REQUEST_DELAY_SECONDS)
    return None, None, last_error


def page_emails(soup: BeautifulSoup, scope: Tag | BeautifulSoup | None = None) -> list[str]:
    """Extract only published functional business inboxes from visible HTML and mailto links."""
    content = scope or soup
    candidates: set[str] = set()
    for link in content.select("a[href^='mailto:']"):
        candidates.add(normalize_email(link["href"].split(":", 1)[1].split("?", 1)[0]))
    for match in EMAIL_PATTERN.finditer(content.get_text(" ", strip=True)):
        candidates.add(normalize_email(match.group(0)))
    return sorted(email for email in candidates if valid_business_email(email))


def relevant_links(soup: BeautifulSoup, current_url: str, root_url: str) -> list[str]:
    """Follow at most two same-site contact/careers links exposed by normal navigation."""
    scored: list[tuple[int, str]] = []
    seen: set[str] = set()
    for link in soup.select("a[href]"):
        label = normalize_text(link.get_text(" ", strip=True)).casefold()
        candidate = urljoin(current_url, link["href"]).split("#", 1)[0]
        if not is_public_http_url(candidate) or not same_site(candidate, root_url):
            continue
        path = urlparse(candidate).path.casefold()
        combined = f"{label} {path}"
        if not any(term in combined for term in ("career", "jobs", "hiring", "recruit", "talent", "contact", "about", "team")):
            continue
        if candidate == current_url or candidate in seen:
            continue
        score = 3
        if any(term in combined for term in ("career", "jobs", "hiring", "recruit", "talent")):
            score = 0
        elif "contact" in combined:
            score = 1
        elif any(term in combined for term in ("about", "team")):
            score = 2
        seen.add(candidate)
        scored.append((score, candidate))
    return [url for _, url in sorted(scored)[:MAX_RELEVANT_LINKS]]


def category_for_email(email: str, page_text: str) -> str:
    local = email.partition("@")[0].casefold()
    # Classify from the published mailbox itself.  A generic inbox on a careers
    # page remains General unless its local part actually indicates recruitment.
    context = local
    if "talentacquisition" in context or "talent-acquisition" in context:
        return "Talent Acquisition"
    if "recruit" in context:
        return "Recruitment"
    if "hiring" in context:
        return "Hiring"
    if "career" in context or local in {"jobs", "job"}:
        return "Careers"
    if local == "hr" or local.startswith("hr.") or local.startswith("hr_") or "humanresources" in context:
        return "HR"
    if local in {"info", "contact", "hello", "enquiries", "enquiry", "admin", "office", "business", "team"}:
        return "General"
    if local in {"sales", "support", "marketing", "accounts", "accounting", "finance", "service", "services", "help"}:
        return "Other"
    return "Business Contact"


def contact_fields(email: str, category: str) -> tuple[str, str, str]:
    if category in HIRE_CATEGORIES:
        return "Primary", "Hiring Relevant", "High"
    if category == "General":
        return "General", "General Business", "High"
    if category in {"Business Contact", "Other"}:
        return "Secondary", "Other Business", "High"
    return "Secondary", "Unclear", "High"


def contact_row(
    target: dict[str, str], email: str, page_url: str, source_type: str, page_text: str,
    discovery_status: str, research_status: str, notes: str,
) -> dict[str, str]:
    category = category_for_email(email, page_text)
    priority, quality, confidence = contact_fields(email, category)
    row = dict(target)
    row.update(
        {
            "contact_name": "",
            "designation": "",
            "email": email,
            "email_category": category,
            "contact_priority": priority,
            "contact_source_url": page_url,
            "source_type": source_type,
            "source_context": "Publicly published functional business email on this page.",
            "source_confidence": confidence,
            "contact_quality": quality,
            "discovery_status": discovery_status,
            "stage2_research_status": research_status,
            "research_notes": notes,
        }
    )
    return row


def no_email_row(target: dict[str, str], discovery_status: str, research_status: str, notes: str) -> dict[str, str]:
    row = dict(target)
    row.update(
        {
            "contact_name": "", "designation": "", "email": "", "email_category": "",
            "contact_priority": "", "contact_source_url": "", "source_type": "", "source_context": "",
            "source_confidence": "", "contact_quality": "", "discovery_status": discovery_status,
            "stage2_research_status": research_status, "research_notes": notes,
        }
    )
    return row


def add_error(errors: list[dict[str, str]], company_name: str, url: str, error_type: str, message: str, status: str) -> None:
    if any(error["company_name"] == company_name and error["url"] == url and error["error_type"] == error_type for error in errors):
        return
    errors.append({
        "company_name": company_name, "url": url, "error_type": error_type,
        "error_message": message, "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"), "status": status,
    })


def source_rank(row: dict[str, str]) -> tuple[int, int, str]:
    category_rank = {"Recruitment": 0, "Hiring": 1, "Careers": 2, "HR": 3, "Talent Acquisition": 4, "General": 5, "Business Contact": 6, "Other": 7}
    source_rank_value = 0 if row["source_type"].startswith("Official") else 1
    return category_rank.get(row["email_category"], 99), source_rank_value, row["email"]


def ordered_by_target(
    targets: list[dict[str, str]], items_by_profile: dict[str, list[dict[str, str]]]
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for target in targets:
        output.extend(items_by_profile.get(target["infopark_profile_url"], []))
    return output


def status_row(target: dict[str, str], contacts: list[dict[str, str]], status: str, source_count: int, notes: str) -> dict[str, str]:
    email_contacts = [row for row in contacts if row["email"]]
    primary = min(email_contacts, key=source_rank) if email_contacts else None
    return {
        "company_name": target["company_name"], "website": target["website"],
        "infopark_profile_url": target["infopark_profile_url"], "final_priority": target["final_priority"],
        "public_email_found": "Yes" if primary else "No", "email_count": str(len(email_contacts)),
        "primary_email": primary["email"] if primary else "", "primary_email_category": primary["email_category"] if primary else "",
        "research_status": status, "research_source_count": str(source_count), "notes": notes,
    }


def audit_row(status: dict[str, str], contacts: list[dict[str, str]]) -> dict[str, str]:
    primary = min((row for row in contacts if row["email"]), key=source_rank, default=None)
    if status["research_status"] == "Research Failed":
        result = "Research Failed"
    elif primary is None:
        result = "No Contact"
    elif any(row["contact_quality"] == "Hiring Relevant" for row in contacts):
        result = "Valid"
    else:
        result = "Needs Review"
    return {
        "company_name": status["company_name"], "final_priority": status["final_priority"], "researched": "Yes",
        "email_found": status["public_email_found"], "email_count": status["email_count"],
        "primary_email": status["primary_email"], "primary_email_category": status["primary_email_category"],
        "source_type": primary["source_type"] if primary else "", "contact_source_url": primary["contact_source_url"] if primary else "",
        "discovery_status": primary["discovery_status"] if primary else ("Research Failed" if result == "Research Failed" else "No Public Email Found"),
        "audit_result": result, "notes": status["notes"],
    }


def validate(targets: list[dict[str, str]], contacts: list[dict[str, str]], statuses: list[dict[str, str]], audits: list[dict[str, str]]) -> None:
    if len(targets) != 394:
        raise ValueError(f"Expected 394 frozen targets; found {len(targets)}")
    target_profiles = {row["infopark_profile_url"] for row in targets}
    if len(target_profiles) != len(targets):
        raise ValueError("Frozen target input has duplicate profile URLs.")
    status_profiles = [row["infopark_profile_url"] for row in statuses]
    audit_names = [row["company_name"] for row in audits]
    if len(statuses) != len(targets) or set(status_profiles) != target_profiles or len(set(status_profiles)) != len(status_profiles):
        raise ValueError("Company-status dataset does not represent every target exactly once.")
    if len(audits) != len(targets) or len(set(audit_names)) != len(audit_names):
        raise ValueError("Audit dataset does not represent every target exactly once.")
    seen_company_email: set[tuple[str, str]] = set()
    targets_by_profile = {row["infopark_profile_url"]: row for row in targets}
    for contact in contacts:
        target = targets_by_profile.get(contact["infopark_profile_url"])
        if target is None:
            raise ValueError(f"Contact belongs to a non-target company: {contact['company_name']}")
        if any(contact[column] != target[column] for column in TARGET_COLUMNS):
            raise ValueError(f"Frozen target field changed for {contact['company_name']}")
        if contact["email"]:
            key = contact["infopark_profile_url"], contact["email"]
            if key in seen_company_email:
                raise ValueError(f"Duplicate company+email record: {contact['company_name']} {contact['email']}")
            seen_company_email.add(key)
            if not all(contact[column] for column in ("email_category", "contact_source_url", "source_type", "discovery_status")):
                raise ValueError(f"Sourced email has incomplete metadata: {contact['email']}")
            if contact["discovery_status"] not in {"Email Found", "Multiple Public Emails Found"}:
                raise ValueError(f"Email record has invalid discovery status: {contact['email']}")
        elif contact["discovery_status"] not in {"No Public Email Found", "Source Unavailable", "Research Failed"}:
            raise ValueError(f"Blank-email contact row has invalid status: {contact['company_name']}")
    for status in statuses:
        if status["public_email_found"] not in {"Yes", "No"}:
            raise ValueError(f"Invalid company email status: {status['company_name']}")
        if status["research_status"] not in {"Completed - Email Found", "Completed - No Public Email", "Research Failed"}:
            raise ValueError(f"Invalid research status: {status['company_name']}")
        if status["public_email_found"] == "Yes" and not status["primary_email"]:
            raise ValueError(f"Company marked Email Found without a primary email: {status['company_name']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover public functional business emails for frozen Infopark targets.")
    parser.add_argument("--limit", type=int, default=0, help="process at most this many unfinished companies")
    parser.add_argument("--force", action="store_true", help="re-research completed companies deliberately")
    arguments = parser.parse_args()
    if arguments.limit < 0:
        parser.error("--limit must be zero or positive")
    try:
        targets = read_csv(INPUT_FILE, TARGET_COLUMNS)
        if len(targets) != 394:
            raise ValueError(f"Expected 394 frozen target records; found {len(targets)}")
        statuses = read_csv(STATUS_FILE, STATUS_COLUMNS) if STATUS_FILE.exists() else []
        contacts = read_csv(CONTACT_FILE, CONTACT_COLUMNS) if CONTACT_FILE.exists() else []
        errors = read_csv(ERROR_FILE, ERROR_COLUMNS) if ERROR_FILE.exists() else []
        target_by_profile = {row["infopark_profile_url"]: row for row in targets}
        status_by_profile = {row["infopark_profile_url"]: row for row in statuses}
        contacts_by_profile: dict[str, list[dict[str, str]]] = {}
        for row in contacts:
            contacts_by_profile.setdefault(row["infopark_profile_url"], []).append(row)
        if set(status_by_profile) - set(target_by_profile):
            raise ValueError("Existing Stage 2 status includes a non-target company.")

        session = requests.Session()
        session.headers.update({
            "User-Agent": "Kerala-JobHunt-Infopark-Research/3.0 (public business-contact discovery; no login or email verification)",
            "Accept": "text/html,application/xhtml+xml",
        })
        requests_made = 0
        processed = 0
        for target in targets:
            profile = target["infopark_profile_url"]
            existing = status_by_profile.get(profile)
            if existing and not arguments.force:
                continue
            if arguments.limit and processed >= arguments.limit:
                break
            print(f"Researching public contacts: {target['company_name']}")
            discovered: dict[str, dict[str, str]] = {}
            notes: list[str] = []
            source_count = 0
            accessible_source_count = 0
            research_failed = False
            root_url = website_start_url(target["website"])
            pages: list[tuple[str, str, bool]] = []
            if root_url:
                pages.append((root_url, classify_page_type(root_url), False))
            else:
                notes.append("No usable website URL in frozen target data.")

            page_index = 0
            while page_index < len(pages):
                page_url, source_type, official_infopark = pages[page_index]
                page_index += 1
                if requests_made:
                    time.sleep(REQUEST_DELAY_SECONDS)
                html, final_url, error = fetch(session, page_url)
                requests_made += 1
                source_count += 1
                if html is None:
                    add_error(errors, target["company_name"], page_url, "HTTP_ERROR", error or "Public page request failed", "Research Failed")
                    notes.append(f"Could not access {page_url}: {error}")
                    research_failed = True
                    continue
                accessible_source_count += 1
                actual_url = final_url or page_url
                soup = BeautifulSoup(html, "html.parser")
                page_text = normalize_text(soup.get_text(" ", strip=True))
                for email in page_emails(soup):
                    if email not in discovered:
                        discovered[email] = {"url": actual_url, "source_type": classify_page_type(actual_url), "text": page_text}
                if page_index == 1 and root_url:
                    for candidate in relevant_links(soup, actual_url, root_url):
                        pages.append((candidate, classify_page_type(candidate), False))

            # The official Infopark profile is a permitted fallback source only when
            # website research did not expose an eligible public functional inbox.
            if not discovered and target["infopark_profile_url"]:
                profile_url = target["infopark_profile_url"]
                if requests_made:
                    time.sleep(REQUEST_DELAY_SECONDS)
                html, final_url, error = fetch(session, profile_url)
                requests_made += 1
                source_count += 1
                if html is None:
                    add_error(errors, target["company_name"], profile_url, "HTTP_ERROR", error or "Official profile request failed", "Research Failed")
                    notes.append(f"Could not access official Infopark profile: {error}")
                    research_failed = True
                else:
                    accessible_source_count += 1
                    soup = BeautifulSoup(html, "html.parser")
                    page_text = normalize_text(soup.get_text(" ", strip=True))
                    # The Infopark profile footer has Infopark's own contact email;
                    # only the company-specific profile block is eligible evidence.
                    profile_scope = soup.select_one(".company-detail .carer-box")
                    for email in page_emails(soup, profile_scope):
                        if email not in discovered:
                            discovered[email] = {"url": final_url or profile_url, "source_type": "Official Infopark Directory", "text": page_text}

            if discovered:
                email_status = "Multiple Public Emails Found" if len(discovered) > 1 else "Email Found"
                research_status = "Completed - Email Found"
                company_contacts = [
                    contact_row(target, email, evidence["url"], evidence["source_type"], evidence["text"], email_status, research_status, " ".join(notes))
                    for email, evidence in sorted(discovered.items())
                ]
            elif accessible_source_count == 0:
                email_status = "Research Failed"
                research_status = "Research Failed"
                company_contacts = [no_email_row(target, email_status, research_status, " ".join(notes))]
            else:
                email_status = "No Public Email Found"
                research_status = "Completed - No Public Email"
                if research_failed:
                    notes.append("At least one permitted public source was unavailable; no eligible public business email was found on accessible sources.")
                company_contacts = [no_email_row(target, email_status, research_status, " ".join(notes))]

            contacts_by_profile[profile] = company_contacts
            status_by_profile[profile] = status_row(target, company_contacts, research_status, source_count, " ".join(notes))
            processed += 1
            all_contacts = ordered_by_target(targets, contacts_by_profile)
            all_statuses = [status_by_profile[row["infopark_profile_url"]] for row in targets if row["infopark_profile_url"] in status_by_profile]
            audits = [audit_row(status_by_profile[row["infopark_profile_url"]], contacts_by_profile.get(row["infopark_profile_url"], [])) for row in targets if row["infopark_profile_url"] in status_by_profile]
            atomic_write(all_contacts, CONTACT_FILE, CONTACT_COLUMNS)
            atomic_write(all_statuses, STATUS_FILE, STATUS_COLUMNS)
            atomic_write(audits, AUDIT_FILE, AUDIT_COLUMNS)
            if errors:
                atomic_write(errors, ERROR_FILE, ERROR_COLUMNS)

        all_contacts = ordered_by_target(targets, contacts_by_profile)
        all_statuses = [status_by_profile[row["infopark_profile_url"]] for row in targets if row["infopark_profile_url"] in status_by_profile]
        audits = [audit_row(status_by_profile[row["infopark_profile_url"]], contacts_by_profile.get(row["infopark_profile_url"], [])) for row in targets if row["infopark_profile_url"] in status_by_profile]
        if len(all_statuses) == len(targets):
            validate(targets, all_contacts, all_statuses, audits)
        print("\nInfopark Stage 2 progress")
        print("-------------------------")
        print(f"Target companies: {len(targets)}")
        print(f"Companies researched: {len(all_statuses)}")
        print(f"Research requests this run: {requests_made}")
        print(f"Checkpointed contact rows: {len(all_contacts)}")
    except (OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
