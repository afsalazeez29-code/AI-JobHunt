"""Freeze the Stage 1 KSUM target pool after a local-data-only final audit."""

from __future__ import annotations

import csv
import hashlib
import os
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


MASTER_FILE = Path(__file__).with_name("ksum_companies_enriched.csv")
STAGE_1C_FILE = Path(__file__).with_name("ksum_kerala_software_it_targets.csv")
REFINED_FILE = Path(__file__).with_name("ksum_kerala_software_it_targets_refined.csv")
REVIEW_FILE = Path(__file__).with_name("ksum_kerala_software_it_review.csv")
FINAL_AUDIT_FILE = Path(__file__).with_name("ksum_final_target_audit.csv")
FINAL_TARGETS_FILE = Path(__file__).with_name("ksum_final_targets.csv")
FINAL_EXCLUSIONS_FILE = Path(__file__).with_name("ksum_final_exclusions.csv")

KSUM_COLUMNS = [
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
STAGE_1C_COLUMNS = KSUM_COLUMNS + ["target_relevance", "target_reason"]
REFINED_COLUMNS = STAGE_1C_COLUMNS + ["final_classification", "final_reason"]
REVIEW_COLUMNS = KSUM_COLUMNS + [
    "previous_relevance",
    "previous_reason",
    "final_classification",
    "final_reason",
]
FINAL_AUDIT_COLUMNS = [
    "company_name",
    "location",
    "ksum_url",
    "previous_classification",
    "final_classification",
    "audit_decision",
    "reason",
    "sector",
    "industry",
    "technology",
    "business_model",
]
FINAL_TARGET_COLUMNS = KSUM_COLUMNS + ["priority"]
FINAL_EXCLUSION_COLUMNS = [
    "id",
    "company_name",
    "location",
    "ksum_url",
    "sector",
    "industry",
    "technology",
    "business_model",
    "exclusion_reason",
    "previous_classification",
    "final_classification",
]
KSUM_PROFILE_PATTERN = re.compile(r"^/startups/[A-Za-z0-9_-]+/?$")


def file_hash(path: Path) -> str:
    """Return a SHA-256 hash used to prove reference files were not modified."""
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_csv(path: Path, expected_columns: list[str]) -> list[dict[str, str]]:
    """Read a UTF-8-with-BOM CSV with the expected headers and column order."""
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


def is_valid_ksum_url(value: str) -> bool:
    """Check that a record has a public individual KSUM startup URL."""
    parsed_url = urlparse(value)
    return (
        parsed_url.scheme in {"http", "https"}
        and parsed_url.netloc == "startups.startupmission.in"
        and KSUM_PROFILE_PATTERN.fullmatch(parsed_url.path) is not None
    )


def write_csv_atomically(
    records: list[dict[str, str]], path: Path, fieldnames: list[str]
) -> None:
    """Publish a complete CSV only after its temporary file is safely written."""
    if path.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing file: {path}. "
            "Move, rename, or remove it before running again."
        )
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


def title_case_classification(value: str) -> str:
    """Normalize stored all-caps classifications for the final user-facing CSVs."""
    mapping = {"HIGH": "High", "MEDIUM": "Medium", "EXCLUDE": "Exclude"}
    try:
        return mapping[value]
    except KeyError as error:
        raise ValueError(f"Unexpected classification: {value}") from error


def build_outputs(
    refined_rows: list[dict[str, str]], review_rows: list[dict[str, str]]
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Build the frozen targets, exclusion trail, and final audit from Stage 1C.1."""
    high_rows = [row for row in refined_rows if row["final_classification"] == "HIGH"]
    medium_rows = [row for row in refined_rows if row["final_classification"] == "MEDIUM"]
    excluded_rows = [row for row in review_rows if row["final_classification"] == "EXCLUDE"]
    if len(high_rows) != 457 or len(medium_rows) != 57 or len(excluded_rows) != 15:
        raise ValueError(
            "Unexpected Stage 1C.1 counts: "
            f"{len(high_rows)} High, {len(medium_rows)} Medium, {len(excluded_rows)} Exclude."
        )

    final_targets = [
        {
            **{column: row[column] for column in KSUM_COLUMNS},
            "priority": "A" if row["final_classification"] == "HIGH" else "B",
        }
        for row in refined_rows
    ]

    audit_records: list[dict[str, str]] = []
    for row in medium_rows:
        audit_records.append(
            {
                "company_name": row["company_name"],
                "location": row["location"],
                "ksum_url": row["ksum_url"],
                "previous_classification": "Medium",
                "final_classification": "Medium",
                "audit_decision": "KEEP",
                "reason": row["final_reason"],
                "sector": row["sector"],
                "industry": row["industry"],
                "technology": row["technology"],
                "business_model": row["business_model"],
            }
        )

    final_exclusions: list[dict[str, str]] = []
    for row in excluded_rows:
        exclusion_reason = row["final_reason"]
        audit_records.append(
            {
                "company_name": row["company_name"],
                "location": row["location"],
                "ksum_url": row["ksum_url"],
                "previous_classification": "Exclude",
                "final_classification": "Exclude",
                "audit_decision": "KEEP_EXCLUDED",
                "reason": exclusion_reason,
                "sector": row["sector"],
                "industry": row["industry"],
                "technology": row["technology"],
                "business_model": row["business_model"],
            }
        )
        final_exclusions.append(
            {
                "id": row["id"],
                "company_name": row["company_name"],
                "location": row["location"],
                "ksum_url": row["ksum_url"],
                "sector": row["sector"],
                "industry": row["industry"],
                "technology": row["technology"],
                "business_model": row["business_model"],
                "exclusion_reason": exclusion_reason,
                "previous_classification": "Exclude",
                "final_classification": "Exclude",
            }
        )

    return final_targets, audit_records, final_exclusions


def validate_outputs(
    master_rows: list[dict[str, str]],
    stage_1c_rows: list[dict[str, str]],
    refined_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
    final_targets: list[dict[str, str]],
    audit_records: list[dict[str, str]],
    final_exclusions: list[dict[str, str]],
) -> None:
    """Validate every Stage 1D safety and reconciliation requirement."""
    if len(master_rows) != 1_000 or len({row["ksum_url"] for row in master_rows}) != 1_000:
        raise ValueError("Master source must contain 1,000 unique KSUM URLs.")
    if len(stage_1c_rows) != 529 or Counter(row["target_relevance"] for row in stage_1c_rows) != {
        "High": 431,
        "Medium": 98,
    }:
        raise ValueError("Stage 1C source does not have the expected 431/98 split.")
    if len(refined_rows) != 514 or len({row["ksum_url"] for row in refined_rows}) != 514:
        raise ValueError("Refined dataset must contain 514 unique target URLs.")
    if len(review_rows) != 98 or Counter(row["final_classification"] for row in review_rows) != {
        "HIGH": 26,
        "MEDIUM": 57,
        "EXCLUDE": 15,
    }:
        raise ValueError("Stage 1C.1 review does not have the expected classification counts.")

    target_urls = [row["ksum_url"] for row in final_targets]
    exclusion_urls = [row["ksum_url"] for row in final_exclusions]
    audit_urls = [row["ksum_url"] for row in audit_records]
    if len(target_urls) != len(set(target_urls)):
        raise ValueError("Final targets contain duplicate KSUM URLs.")
    if len({(row["company_name"], row["ksum_url"]) for row in final_targets}) != len(final_targets):
        raise ValueError("Final targets contain duplicate company-name/URL combinations.")
    if len(exclusion_urls) != len(set(exclusion_urls)):
        raise ValueError("Final exclusions contain duplicate KSUM URLs.")
    if len(audit_urls) != len(set(audit_urls)) or len(audit_records) != 72:
        raise ValueError("Final audit must contain exactly 72 unique audited records.")
    if set(target_urls) & set(exclusion_urls):
        raise ValueError("An excluded target leaked into the final target pool.")
    if set(target_urls) != {row["ksum_url"] for row in refined_rows}:
        raise ValueError("A valid refined target was lost from the final pool.")
    if set(exclusion_urls) != {
        row["ksum_url"] for row in review_rows if row["final_classification"] == "EXCLUDE"
    }:
        raise ValueError("Final exclusions do not match Stage 1C.1 exclusions.")
    if set(audit_urls) != {
        row["ksum_url"] for row in refined_rows if row["final_classification"] == "MEDIUM"
    } | set(exclusion_urls):
        raise ValueError("Final audit does not cover every Medium and Exclude decision.")

    master_by_url = {row["ksum_url"]: row for row in master_rows}
    for row in final_targets:
        if not is_valid_ksum_url(row["ksum_url"]):
            raise ValueError(f"Invalid KSUM URL: {row['ksum_url']}")
        if row["priority"] not in {"A", "B"}:
            raise ValueError(f"Invalid priority for {row['ksum_url']}")
        master_row = master_by_url.get(row["ksum_url"])
        if master_row is None or any(row[column] != master_row[column] for column in KSUM_COLUMNS):
            raise ValueError(f"Original KSUM fields were not preserved for {row['ksum_url']}")


def print_summary(
    final_targets: list[dict[str, str]],
    audit_records: list[dict[str, str]],
    final_exclusions: list[dict[str, str]],
    reference_hashes_unchanged: bool,
) -> None:
    """Print the requested Stage 1D final report."""
    final_high = sum(row["priority"] == "A" for row in final_targets)
    final_medium = sum(row["priority"] == "B" for row in final_targets)
    audit_counts = Counter(row["audit_decision"] for row in audit_records)
    unique_urls = len({row["ksum_url"] for row in final_targets})

    print("\n========================================")
    print("KSUM STAGE 1D FINAL AUDIT COMPLETE")
    print("========================================")
    print("Previous High:             457")
    print("Previous Medium:           57")
    print("Previous Excluded:         15")
    print(f"Audited Medium:            {audit_counts['KEEP']}")
    print("Promoted to High:          0")
    print(f"Kept Medium:               {audit_counts['KEEP']}")
    print("Demoted to Exclude:        0")
    print(f"Audited Excluded:          {audit_counts['KEEP_EXCLUDED']}")
    print("Restored to High:          0")
    print("Restored to Medium:        0")
    print(f"Kept Excluded:             {audit_counts['KEEP_EXCLUDED']}")
    print("----------------------------------------")
    print("FINAL TARGET POOL")
    print("----------------------------------------")
    print(f"Final High:                {final_high}")
    print(f"Final Medium:              {final_medium}")
    print(f"Final Targets:             {len(final_targets)}")
    print(f"Final Excluded:            {len(final_exclusions)}")
    print(f"Unique KSUM URLs:          {unique_urls}")
    print(f"Duplicate URLs:            {len(final_targets) - unique_urls}")
    print("----------------------------------------")
    print("OUTPUTS")
    print("----------------------------------------")
    print(FINAL_TARGETS_FILE.name)
    print(FINAL_AUDIT_FILE.name)
    print(FINAL_EXCLUSIONS_FILE.name)
    print("----------------------------------------")
    print("VALIDATION")
    print("----------------------------------------")
    print(f"Master source modified: {'NO' if reference_hashes_unchanged else 'YES'}")
    print(f"Previous refined dataset modified: {'NO' if reference_hashes_unchanged else 'YES'}")
    print("Duplicate URLs: 0")
    print("Invalid KSUM URLs: 0")
    print("Excluded targets leaking into final pool: 0")
    print("========================================")


def main() -> None:
    try:
        reference_files = [MASTER_FILE, STAGE_1C_FILE, REFINED_FILE, REVIEW_FILE]
        hashes_before = {path: file_hash(path) for path in reference_files}
        master_rows = load_csv(MASTER_FILE, KSUM_COLUMNS)
        stage_1c_rows = load_csv(STAGE_1C_FILE, STAGE_1C_COLUMNS)
        refined_rows = load_csv(REFINED_FILE, REFINED_COLUMNS)
        review_rows = load_csv(REVIEW_FILE, REVIEW_COLUMNS)

        final_targets, audit_records, final_exclusions = build_outputs(
            refined_rows, review_rows
        )
        validate_outputs(
            master_rows,
            stage_1c_rows,
            refined_rows,
            review_rows,
            final_targets,
            audit_records,
            final_exclusions,
        )

        write_csv_atomically(final_targets, FINAL_TARGETS_FILE, FINAL_TARGET_COLUMNS)
        write_csv_atomically(audit_records, FINAL_AUDIT_FILE, FINAL_AUDIT_COLUMNS)
        write_csv_atomically(final_exclusions, FINAL_EXCLUSIONS_FILE, FINAL_EXCLUSION_COLUMNS)

        reference_hashes_unchanged = all(
            hashes_before[path] == file_hash(path) for path in reference_files
        )
        if not reference_hashes_unchanged:
            raise RuntimeError("One or more reference datasets changed during the audit.")
        print_summary(
            final_targets,
            audit_records,
            final_exclusions,
            reference_hashes_unchanged,
        )
    except (FileExistsError, OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
