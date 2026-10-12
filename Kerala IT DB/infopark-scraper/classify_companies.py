"""Stage 1.1 offline classification using only saved Infopark directory card data."""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path


INPUT_FILE = Path(__file__).with_name("infopark_companies.csv")
OUTPUT_FILE = Path(__file__).with_name("infopark_companies_classified.csv")
REVIEW_FILE = Path(__file__).with_name("infopark_software_review.csv")
INPUT_COLUMNS = [
    "company_name",
    "phone",
    "website",
    "domain",
    "infopark_profile_url",
    "infopark_job_url",
    "source_url",
    "location",
]
CLASSIFICATION_COLUMNS = [
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
OUTPUT_COLUMNS = [*INPUT_COLUMNS, *CLASSIFICATION_COLUMNS]
REVIEW_COLUMNS = [
    "company_name",
    "domain",
    "it_relevance",
    "developer_relevance",
    "priority",
    "job_match_reason",
    "notes",
    "infopark_profile_url",
]
RATINGS = {"High", "Medium", "Low"}
RESEARCH_STATUS = "Stage 1.1 Classified"


def normalize_text(value: str) -> str:
    """Normalize whitespace only; source values themselves are never rewritten."""
    return " ".join(value.split())


def read_csv(path: Path, expected_columns: list[str]) -> list[dict[str, str]]:
    """Read a UTF-8 CSV only when its schema matches exactly."""
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != expected_columns:
                raise ValueError(
                    f"Unexpected columns in {path.name}: {reader.fieldnames}; "
                    f"expected {expected_columns}"
                )
            return list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read {path}: {error}") from error


def atomic_write(records: list[dict[str, str]], path: Path, columns: list[str]) -> None:
    """Atomically publish complete deterministic CSV results."""
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


def has_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def classify(record: dict[str, str]) -> tuple[dict[str, str], bool]:
    """Classify using domain field text only; company names and URLs are not signals."""
    domain = record["domain"]
    text = domain.casefold()
    domain_items = {normalize_text(item).casefold() for item in domain.split("|")}
    result = dict(record)
    areas: list[str] = []
    roles: list[str] = []
    notes: list[str] = []

    if not normalize_text(domain):
        result.update(
            {
                "it_relevance": "Low",
                "developer_relevance": "Low",
                "primary_technology_area": "Unknown",
                "relevant_roles": "Unknown",
                "priority": "Low",
                "job_match_reason": (
                    "No domain information is available in the Infopark directory, so "
                    "software-development relevance cannot be established."
                ),
                "email_angle": "Not a developer target",
                "research_status": RESEARCH_STATUS,
                "notes": "Domain field is blank; developer relevance is uncertain from available directory data.",
            }
        )
        return result, True

    explicit_development = has_any(
        text,
        (
            "software development",
            "web development",
            "web application",
            "mobile application development",
            "mobile app development",
            "application development",
            "game development",
            "metaverse development",
        ),
    )
    software_testing = "software testing" in text
    mobile = has_any(text, ("mobile application", "mobile app"))
    ai_or_data = has_any(
        text, ("artificial intelligence", "machine learning", "data science", "analytics")
    ) or "ai" in domain_items
    cloud_or_infra = has_any(text, ("cloud computing", "networking", "it infrastructure"))
    cybersecurity = "cybersecurity" in text
    consulting = has_any(text, ("it consulting", "digital trasformation consulting"))
    ui_ux = "ui/ux" in text
    ecommerce = "e-commerce" in text or "ecommerce" in text
    technical_other = has_any(
        text, ("internet of things", "robotics", "automation", "open source")
    ) or "erp" in domain_items
    clear_nonsoftware = has_any(
        text,
        (
            "bpo",
            "back office",
            "customer support",
            "finance & accounting services",
            "digital marketing",
            "management consulting",
            "bim (building information modeling)",
            "mep",
            "brand identity design",
        ),
    )

    if explicit_development:
        append_unique(areas, "Software Development")
    if "web development" in text or "web application" in text:
        append_unique(areas, "Web Development")
    if mobile:
        append_unique(areas, "Mobile Development")
    if ai_or_data:
        append_unique(
            areas,
            "AI / Machine Learning"
            if "artificial intelligence" in text or "machine learning" in text or "ai" in domain_items
            else "Data / Analytics",
        )
        if "data science" in text or "analytics" in text:
            append_unique(areas, "Data / Analytics")
    if cloud_or_infra:
        append_unique(areas, "Cloud / Infrastructure")
    if cybersecurity:
        append_unique(areas, "Cybersecurity")
    if consulting:
        append_unique(areas, "Technology Consulting")
    if ui_ux or "digital marketing" in text:
        append_unique(areas, "Digital Technology")
    if ecommerce:
        append_unique(areas, "E-commerce Technology")
    if technical_other and not areas:
        append_unique(areas, "Other")

    if explicit_development:
        result["it_relevance"] = "High"
        result["developer_relevance"] = "High"
        result["priority"] = "High"
        append_unique(roles, "Software Developer")
        append_unique(roles, "Software Engineer")
        append_unique(roles, "Application Developer")
        if "web development" in text or "web application" in text:
            append_unique(roles, "Web Developer")
            append_unique(roles, "Frontend Developer")
            append_unique(roles, "Backend Developer")
            append_unique(roles, "Full-Stack Developer")
        if mobile:
            append_unique(roles, "Mobile Developer")
        if ai_or_data:
            append_unique(roles, "Data / AI Engineer")
        if cloud_or_infra:
            append_unique(roles, "DevOps / Cloud Engineer")
        if software_testing:
            append_unique(roles, "QA / Software Tester")
        reason = "Available Infopark domain information explicitly includes software or application development."
        email_angle = "Developer / Software Engineer application"
        review_required = False
    elif ai_or_data or cloud_or_infra or cybersecurity or consulting or software_testing or technical_other:
        result["it_relevance"] = "High"
        result["developer_relevance"] = "Medium"
        result["priority"] = "Medium"
        if ai_or_data:
            append_unique(roles, "Data / AI Engineer")
        if cloud_or_infra:
            append_unique(roles, "DevOps / Cloud Engineer")
        if software_testing:
            append_unique(roles, "QA / Software Tester")
        if not roles:
            append_unique(roles, "Other Technical Role")
        reason = (
            "Available Infopark domain information indicates a technology-focused business, "
            "but does not clearly establish software-development work."
        )
        email_angle = "Technical role inquiry"
        notes.append("Developer relevance uncertain from available directory data.")
        review_required = True
    elif ui_ux or ecommerce:
        result["it_relevance"] = "Medium"
        result["developer_relevance"] = "Medium"
        result["priority"] = "Medium"
        append_unique(roles, "Other Technical Role")
        reason = (
            "Available Infopark domain information indicates digital or e-commerce work, "
            "but does not clearly establish software-development work."
        )
        email_angle = "General technology job inquiry"
        notes.append("Developer relevance uncertain from available directory data.")
        review_required = True
    elif clear_nonsoftware:
        result["it_relevance"] = "Low"
        result["developer_relevance"] = "Low"
        result["priority"] = "Low"
        append_unique(areas, "Other")
        append_unique(roles, "Unknown")
        reason = "Available Infopark domain information indicates non-software business activity."
        email_angle = "Not a developer target"
        notes.append("Clearly non-software business based on available directory data.")
        review_required = False
    else:
        result["it_relevance"] = "Low"
        result["developer_relevance"] = "Low"
        result["priority"] = "Low"
        append_unique(areas, "Unknown")
        append_unique(roles, "Unknown")
        reason = (
            "Available Infopark domain information does not clearly indicate a software-development focus."
        )
        email_angle = "Not a developer target"
        notes.append("Developer relevance uncertain from available directory data.")
        review_required = True

    result.update(
        {
            "primary_technology_area": " / ".join(areas) if areas else "Unknown",
            "relevant_roles": ", ".join(roles) if roles else "Unknown",
            "job_match_reason": reason,
            "email_angle": email_angle,
            "research_status": RESEARCH_STATUS,
            "notes": " ".join(notes),
        }
    )
    return result, review_required


def validate(input_records: list[dict[str, str]], output_records: list[dict[str, str]]) -> None:
    """Enforce exact one-to-one preservation and controlled classification values."""
    if len(input_records) != len(output_records):
        raise ValueError("Output row count does not match frozen Stage 1 input.")
    seen_names: set[str] = set()
    for source, output in zip(input_records, output_records):
        if any(output[column] != source[column] for column in INPUT_COLUMNS):
            raise ValueError(f"An original Stage 1 field changed for {source['company_name']}.")
        name_key = normalize_text(output["company_name"]).casefold()
        if not name_key:
            raise ValueError("Output contains a blank company name.")
        if name_key in seen_names:
            raise ValueError(f"Duplicate company name in output: {output['company_name']}")
        seen_names.add(name_key)
        if output["it_relevance"] not in RATINGS:
            raise ValueError(f"Invalid IT relevance for {output['company_name']}")
        if output["developer_relevance"] not in RATINGS:
            raise ValueError(f"Invalid developer relevance for {output['company_name']}")
        if output["priority"] not in RATINGS:
            raise ValueError(f"Invalid priority for {output['company_name']}")
        if output["research_status"] != RESEARCH_STATUS:
            raise ValueError(f"Invalid research status for {output['company_name']}")
        if any(not output[column] for column in CLASSIFICATION_COLUMNS[:-1]):
            raise ValueError(f"A required classification field is blank for {output['company_name']}")


def print_summary(records: list[dict[str, str]], review_records: list[dict[str, str]]) -> None:
    """Print the requested auditable local-only classification counts."""
    def count(field: str, value: str) -> int:
        return sum(record[field] == value for record in records)

    print("Infopark Stage 1.1 Summary")
    print("--------------------------")
    print(f"Total companies: {len(records)}")
    for field, label in (
        ("it_relevance", "IT relevance"),
        ("developer_relevance", "Developer relevance"),
        ("priority", "Priority"),
    ):
        for value in ("High", "Medium", "Low"):
            print(f"{label} {value}: {count(field, value)}")
    print(f"Review-required: {len(review_records)}")
    print(f"Duplicates: {len(records) - len({normalize_text(record['company_name']).casefold() for record in records})}")
    print(f"Missing company names: {sum(not record['company_name'] for record in records)}")
    print("External requests: 0")
    print(f"Output: {OUTPUT_FILE.name}")
    print(f"Review output: {REVIEW_FILE.name}")


def main() -> None:
    try:
        input_records = read_csv(INPUT_FILE, INPUT_COLUMNS)
        if len(input_records) != 401:
            raise ValueError(f"Expected 401 frozen Stage 1 rows; found {len(input_records)}")
        output_records: list[dict[str, str]] = []
        review_records: list[dict[str, str]] = []
        for record in input_records:
            classified, review_required = classify(record)
            output_records.append(classified)
            if review_required:
                review_records.append({column: classified[column] for column in REVIEW_COLUMNS})

        validate(input_records, output_records)
        atomic_write(output_records, OUTPUT_FILE, OUTPUT_COLUMNS)
        atomic_write(review_records, REVIEW_FILE, REVIEW_COLUMNS)
        print_summary(output_records, review_records)
    except (OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
