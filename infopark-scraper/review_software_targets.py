"""Stage 1.2 offline consistency review for the frozen Infopark company dataset."""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path


STAGE1_FILE = Path(__file__).with_name("infopark_companies.csv")
CLASSIFIED_FILE = Path(__file__).with_name("infopark_companies_classified.csv")
REVIEW_FILE = Path(__file__).with_name("infopark_software_review.csv")
AUDIT_FILE = Path(__file__).with_name("infopark_stage1_2_review_audit.csv")
TARGET_FILE = Path(__file__).with_name("infopark_final_targets.csv")
EXCLUSION_FILE = Path(__file__).with_name("infopark_final_exclusions.csv")

STAGE1_COLUMNS = [
    "company_name",
    "phone",
    "website",
    "domain",
    "infopark_profile_url",
    "infopark_job_url",
    "source_url",
    "location",
]
STAGE1_1_COLUMNS = [
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
CLASSIFIED_COLUMNS = [*STAGE1_COLUMNS, *STAGE1_1_COLUMNS]
AUDIT_COLUMNS = [
    "company_name",
    "domain",
    "stage1_it_relevance",
    "stage1_developer_relevance",
    "stage1_priority",
    "stage1_primary_technology_area",
    "stage1_relevant_roles",
    "stage1_job_match_reason",
    "final_priority",
    "review_decision",
    "review_reason",
    "review_status",
    "infopark_profile_url",
]
TARGET_COLUMNS = [
    *STAGE1_COLUMNS,
    *STAGE1_1_COLUMNS,
    "final_priority",
    "final_review_reason",
    "stage1_2_status",
]
EXCLUSION_COLUMNS = [
    "company_name",
    "domain",
    "infopark_profile_url",
    "stage1_it_relevance",
    "stage1_developer_relevance",
    "stage1_priority",
    "final_priority",
    "final_review_reason",
    "stage1_2_status",
]
FINAL_PRIORITIES = {"High", "Medium", "Excluded"}
STATUS = "Stage 1.2 Reviewed"


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def read_csv(path: Path, expected_columns: list[str]) -> list[dict[str, str]]:
    """Read a compatible UTF-8 CSV without mutating the source data."""
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
    """Publish each complete review artifact atomically."""
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


def is_clearly_nonsoftware_domain(domain: str) -> bool:
    """Identify only stated non-software domains, never from company-name wording."""
    items = {normalize_text(item).casefold() for item in domain.split("|") if item.strip()}
    nonsoftware_items = {
        "mep",
        "bim (building information modeling) solutions",
        "structural & sustainability",
        "finance & accounting services",
    }
    return bool(items) and items <= nonsoftware_items


def review_record(record: dict[str, str]) -> tuple[str, str, str]:
    """Issue a fully offline final decision based on saved Stage 1/1.1 evidence."""
    domain = normalize_text(record["domain"])
    domain_text = domain.casefold()
    original_priority = record["priority"]
    it_relevance = record["it_relevance"]
    developer_relevance = record["developer_relevance"]

    if it_relevance == "High" and developer_relevance == "High":
        return (
            "High",
            "Kept High",
            "Stage 1.1 identifies explicit software, web, mobile, or application-development evidence in the Infopark domain field.",
        )

    if is_clearly_nonsoftware_domain(domain):
        return (
            "Excluded",
            "Excluded",
            "The stated Infopark domain is limited to engineering/BIM/MEP or finance-accounting activity and does not indicate software-development work.",
        )

    if original_priority == "Medium":
        return (
            "Medium",
            "Kept Medium",
            "The Infopark domain indicates technology-related work, but the saved evidence does not clearly establish central software-development work.",
        )

    if not domain:
        return (
            "Medium",
            "Promoted to Medium",
            "The Infopark card has no domain information. It is retained as a lower-confidence target rather than excluded without evidence.",
        )

    if any(
        phrase in domain_text
        for phrase in (
            "communication platform service provider",
            "edtech",
            "digital marketing",
            "enterprise solutions",
        )
    ):
        return (
            "Medium",
            "Promoted to Medium",
            "The stated Infopark domain is technology-adjacent or digital, but direct software-development work is not clearly established.",
        )

    return (
        "Medium",
        "Promoted to Medium",
        "The available Infopark domain information is insufficient to exclude the company confidently, so it is retained for later human review.",
    )


def audit_row(record: dict[str, str], final_priority: str, decision: str, reason: str) -> dict[str, str]:
    return {
        "company_name": record["company_name"],
        "domain": record["domain"],
        "stage1_it_relevance": record["it_relevance"],
        "stage1_developer_relevance": record["developer_relevance"],
        "stage1_priority": record["priority"],
        "stage1_primary_technology_area": record["primary_technology_area"],
        "stage1_relevant_roles": record["relevant_roles"],
        "stage1_job_match_reason": record["job_match_reason"],
        "final_priority": final_priority,
        "review_decision": decision,
        "review_reason": reason,
        "review_status": STATUS,
        "infopark_profile_url": record["infopark_profile_url"],
    }


def target_row(record: dict[str, str], final_priority: str, reason: str) -> dict[str, str]:
    row = dict(record)
    row.update(
        {
            "final_priority": final_priority,
            "final_review_reason": reason,
            "stage1_2_status": STATUS,
        }
    )
    return row


def exclusion_row(record: dict[str, str], final_priority: str, reason: str) -> dict[str, str]:
    return {
        "company_name": record["company_name"],
        "domain": record["domain"],
        "infopark_profile_url": record["infopark_profile_url"],
        "stage1_it_relevance": record["it_relevance"],
        "stage1_developer_relevance": record["developer_relevance"],
        "stage1_priority": record["priority"],
        "final_priority": final_priority,
        "final_review_reason": reason,
        "stage1_2_status": STATUS,
    }


def validate(
    stage1_records: list[dict[str, str]],
    classified_records: list[dict[str, str]],
    audit_records: list[dict[str, str]],
    target_records: list[dict[str, str]],
    exclusion_records: list[dict[str, str]],
) -> None:
    """Validate exact partitioning, source preservation, controlled values, and duplicates."""
    if len(stage1_records) != 401 or len(classified_records) != 401:
        raise ValueError("Stage 1 and Stage 1.1 inputs must each contain exactly 401 records.")
    if len(audit_records) != len(stage1_records):
        raise ValueError("Audit does not account for every original company.")
    if len(target_records) + len(exclusion_records) != len(stage1_records):
        raise ValueError("Targets and exclusions do not partition all original companies.")

    stage1_by_profile = {row["infopark_profile_url"]: row for row in stage1_records}
    classified_by_profile = {row["infopark_profile_url"]: row for row in classified_records}
    if len(stage1_by_profile) != len(stage1_records) or len(classified_by_profile) != len(classified_records):
        raise ValueError("Duplicate profile URL in a Stage 1 input dataset.")
    if set(stage1_by_profile) != set(classified_by_profile):
        raise ValueError("Stage 1 and Stage 1.1 profile URL coverage differs.")
    for profile_url, source in stage1_by_profile.items():
        classified = classified_by_profile[profile_url]
        if any(classified[column] != source[column] for column in STAGE1_COLUMNS):
            raise ValueError(f"Stage 1 field changed in Stage 1.1 for {source['company_name']}.")

    audit_profiles = [row["infopark_profile_url"] for row in audit_records]
    target_profiles = [row["infopark_profile_url"] for row in target_records]
    exclusion_profiles = [row["infopark_profile_url"] for row in exclusion_records]
    if len(set(audit_profiles)) != len(audit_profiles):
        raise ValueError("Duplicate audit decision found.")
    if len(set(target_profiles)) != len(target_profiles):
        raise ValueError("Duplicate final target found.")
    if len(set(exclusion_profiles)) != len(exclusion_profiles):
        raise ValueError("Duplicate final exclusion found.")
    if set(target_profiles) & set(exclusion_profiles):
        raise ValueError("A company appears in both final targets and exclusions.")
    if set(audit_profiles) != set(stage1_by_profile):
        raise ValueError("Audit profile coverage differs from Stage 1 input.")
    if set(target_profiles) | set(exclusion_profiles) != set(stage1_by_profile):
        raise ValueError("Final partition profile coverage differs from Stage 1 input.")

    for audit in audit_records:
        if audit["final_priority"] not in FINAL_PRIORITIES or audit["review_status"] != STATUS:
            raise ValueError(f"Invalid audit decision for {audit['company_name']}.")
        if not audit["company_name"]:
            raise ValueError("Audit contains a blank company name.")
    for target in target_records:
        if target["final_priority"] not in {"High", "Medium"}:
            raise ValueError(f"Excluded record leaked into targets: {target['company_name']}")
        if target["stage1_2_status"] != STATUS:
            raise ValueError(f"Invalid target review status: {target['company_name']}")
        source = stage1_by_profile[target["infopark_profile_url"]]
        if any(target[column] != source[column] for column in STAGE1_COLUMNS):
            raise ValueError(f"Stage 1 field changed in final target: {target['company_name']}")
    for exclusion in exclusion_records:
        if exclusion["final_priority"] != "Excluded" or exclusion["stage1_2_status"] != STATUS:
            raise ValueError(f"Invalid final exclusion: {exclusion['company_name']}")


def print_summary(
    stage1_records: list[dict[str, str]],
    audit_records: list[dict[str, str]],
    target_records: list[dict[str, str]],
    exclusion_records: list[dict[str, str]],
) -> None:
    """Print the exact final-stage handoff summary requested by the project."""
    def count_priority(value: str) -> int:
        return sum(row["final_priority"] == value for row in audit_records)

    promoted = sum(row["review_decision"].startswith("Promoted") for row in audit_records)
    downgraded = sum(row["review_decision"].startswith("Downgraded") for row in audit_records)
    unchanged = sum(row["review_decision"].startswith("Kept") for row in audit_records)
    names = [normalize_text(row["company_name"]).casefold() for row in audit_records]
    profile_urls = [row["infopark_profile_url"].casefold() for row in stage1_records if row["infopark_profile_url"]]
    websites = [row["website"].casefold() for row in stage1_records if row["website"]]
    job_urls = [row["infopark_job_url"].casefold() for row in stage1_records if row["infopark_job_url"]]
    print("INFOPARK STAGE 1.2 COMPLETE")
    print("----------------------------")
    print(f"Input companies: {len(audit_records)}")
    print(f"Final High: {count_priority('High')}")
    print(f"Final Medium: {count_priority('Medium')}")
    print(f"Final Excluded: {count_priority('Excluded')}")
    print(f"Final Target Pool: {len(target_records)}")
    print(f"Reviewed: {len(audit_records)}")
    print(f"Promoted: {promoted}")
    print(f"Downgraded: {downgraded}")
    print(f"Unchanged: {unchanged}")
    print(f"Duplicates: {len(names) - len(set(names))}")
    print(f"Duplicate profile URLs: {len(profile_urls) - len(set(profile_urls))}")
    print(f"Duplicate nonblank websites: {len(websites) - len(set(websites))}")
    print(f"Duplicate nonblank job URLs: {len(job_urls) - len(set(job_urls))}")
    print(f"Missing company names: {sum(not row['company_name'] for row in audit_records)}")
    print(f"Excluded leakage: {sum(row['final_priority'] == 'Excluded' for row in target_records)}")
    print("Unresolved classification: 0")
    print("External requests: 0")
    print("Original Stage 1 dataset modified: NO")
    print(f"Audit: {AUDIT_FILE.name}")
    print(f"Final targets: {TARGET_FILE.name}")
    print(f"Final exclusions: {EXCLUSION_FILE.name}")


def main() -> None:
    try:
        stage1_records = read_csv(STAGE1_FILE, STAGE1_COLUMNS)
        classified_records = read_csv(CLASSIFIED_FILE, CLASSIFIED_COLUMNS)
        # Read the existing review queue to ensure it remains a valid historical input,
        # but use the complete classification dataset for every final decision.
        review_records = read_csv(
            REVIEW_FILE,
            [
                "company_name",
                "domain",
                "it_relevance",
                "developer_relevance",
                "priority",
                "job_match_reason",
                "notes",
                "infopark_profile_url",
            ],
        )
        review_profiles = [row["infopark_profile_url"] for row in review_records]
        classified_profiles = {row["infopark_profile_url"] for row in classified_records}
        if len(review_profiles) != len(set(review_profiles)):
            raise ValueError("Stage 1.1 review input contains duplicate profile URLs.")
        if not set(review_profiles) <= classified_profiles:
            raise ValueError("Stage 1.1 review input contains a profile absent from the full classified dataset.")

        audit_records: list[dict[str, str]] = []
        target_records: list[dict[str, str]] = []
        exclusion_records: list[dict[str, str]] = []
        for record in classified_records:
            final_priority, decision, reason = review_record(record)
            audit_records.append(audit_row(record, final_priority, decision, reason))
            if final_priority == "Excluded":
                exclusion_records.append(exclusion_row(record, final_priority, reason))
            else:
                target_records.append(target_row(record, final_priority, reason))

        validate(
            stage1_records,
            classified_records,
            audit_records,
            target_records,
            exclusion_records,
        )
        atomic_write(audit_records, AUDIT_FILE, AUDIT_COLUMNS)
        atomic_write(target_records, TARGET_FILE, TARGET_COLUMNS)
        atomic_write(exclusion_records, EXCLUSION_FILE, EXCLUSION_COLUMNS)
        print_summary(stage1_records, audit_records, target_records, exclusion_records)
    except (OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
