"""Filter the KSUM master dataset into Kerala software/IT job targets."""

from __future__ import annotations

import csv
import hashlib
import os
import sys
from collections import Counter
from pathlib import Path


INPUT_FILE = Path(__file__).with_name("ksum_companies_enriched.csv")
OUTPUT_FILE = Path(__file__).with_name("ksum_kerala_software_it_targets.csv")
EXPECTED_INPUT_COUNT = 1_000
SOURCE_COLUMNS = [
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
OUTPUT_COLUMNS = SOURCE_COLUMNS + ["target_relevance", "target_reason"]

KERALA_LOCATION_TERMS = (
    "kerala",
    "thiruvananthapuram",
    "trivandrum",
    "kochi",
    "cochin",
    "ernakulam",
    "kozhikode",
    "calicut",
    "kollam",
    "thrissur",
    "kottayam",
    "kannur",
    "alappuzha",
    "palakkad",
    "malappuram",
    "kasaragod",
    "pathanamthitta",
    "idukki",
    "wayanad",
)

STRONG_INDUSTRY_TERMS = (
    "enterprise applications",
    "enterprise infrastructure",
    "healthcare it",
    "fintech",
    "edtech",
    "adtech",
    "consumer apps",
    "social media",
    "mobile",
    "assistive tech",
)

HIGH_VALUE_TECH_TERMS = (
    "web technolog",
    "mobile app",
    "ai / ml",
    "artificial intelligence",
    "machine learning",
    "cyber security",
    "cybersecurity",
    "cloud",
    "big data",
    "blockchain",
    "devops",
    "api",
)

SUPPORTING_TECH_TERMS = (
    "internet of things",
    "iot",
    "augmented reality",
    "virtual reality",
    "robotics",
)

NEGATIVE_SECTOR_TERMS = (
    "agriculture",
    "construction",
    "food processing",
    "consumer goods",
    "aerospace",
    "defense",
    "retail",
    "mobility",
    "media and entertainment",
    "education",
    "healthcare",
    "banking",
    "financial services",
    "energy",
    "climate",
)

STRONGLY_NEGATIVE_SECTOR_TERMS = ("media and entertainment",)

NEGATIVE_INDUSTRY_TERMS = (
    "food & food tech",
    "construction",
    "waste management",
    "agriculture",
    "architecture",
    "military",
    "consumer goods",
    "fmcg",
    "tourism",
    "fitness & wellness",
    "auto",
    "medical devices",
    "life sciences",
    "retail",
    "entertainment & media",
    "logisitics & transport",
    "logistics & transport",
)


def normalize(value: str) -> str:
    """Normalize only for classification; saved source values remain unchanged."""
    return " ".join(value.casefold().split())


def contains_any(value: str, terms: tuple[str, ...]) -> bool:
    normalized_value = normalize(value)
    return any(term in normalized_value for term in terms)


def file_hash(path: Path) -> str:
    """Return a content hash used to confirm the master file was not changed."""
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_master(filename: Path) -> list[dict[str, str]]:
    """Read the Stage 1B master CSV without writing to it."""
    try:
        with filename.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames != SOURCE_COLUMNS:
                raise ValueError(
                    f"Unexpected master columns: {reader.fieldnames}. "
                    f"Expected: {SOURCE_COLUMNS}"
                )
            companies = list(reader)
    except (OSError, csv.Error) as error:
        raise RuntimeError(f"Could not read {filename}: {error}") from error

    if len(companies) != EXPECTED_INPUT_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_INPUT_COUNT} master records, found {len(companies)}."
        )
    urls = [company["ksum_url"] for company in companies]
    if not all(urls) or len(urls) != len(set(urls)):
        raise ValueError("The master dataset has missing or duplicate KSUM URLs.")
    return companies


def is_kerala_location(location: str) -> bool:
    """Recognize an explicit Kerala state or a known Kerala city in the source field."""
    return contains_any(location, KERALA_LOCATION_TERMS)


def classify_company(company: dict[str, str]) -> tuple[str, str] | None:
    """Return a deterministic relevance and factual reason, or None to exclude.

    An IT/ITeS sector is a high-confidence direct signal. Other sectors require
    a strong KSUM technology or industry signal that remains meaningful after
    clear non-software-sector penalties are applied.
    """
    sector = company["sector"]
    industry = company["industry"]
    technology = company["technology"]
    business_model = company["business_model"]

    is_it_sector = "it/ites" in normalize(sector) or "it/ite" in normalize(sector)
    strong_industry = contains_any(industry, STRONG_INDUSTRY_TERMS)
    high_value_technology = contains_any(technology, HIGH_VALUE_TECH_TERMS)
    supporting_technology = contains_any(technology, SUPPORTING_TECH_TERMS)
    has_saas = "saas" in normalize(business_model)
    has_platform = "platform" in normalize(business_model)

    positive_score = 0
    if is_it_sector:
        positive_score += 6
    if strong_industry:
        positive_score += 4
    if high_value_technology:
        positive_score += 3
    elif supporting_technology:
        positive_score += 2
    if has_saas:
        positive_score += 2
    elif has_platform and (is_it_sector or strong_industry or high_value_technology):
        positive_score += 1

    negative_score = 0
    if contains_any(sector, NEGATIVE_SECTOR_TERMS):
        negative_score += (
            2 if contains_any(sector, STRONGLY_NEGATIVE_SECTOR_TERMS) else 1
        )
    if contains_any(industry, NEGATIVE_INDUSTRY_TERMS):
        negative_score += 3

    relevance_score = positive_score - negative_score
    has_direct_software_signal = is_it_sector or strong_industry or high_value_technology

    if is_it_sector:
        relevance = "High"
    elif has_direct_software_signal and relevance_score >= 3:
        relevance = "High" if relevance_score >= 6 else "Medium"
    else:
        return None

    reason_parts: list[str] = []
    if is_it_sector:
        reason_parts.append(f"Sector: {sector}")
    if strong_industry:
        reason_parts.append(f"Industry: {industry}")
    if high_value_technology or supporting_technology:
        reason_parts.append(f"Technology: {technology}")
    if has_saas and len(reason_parts) < 3:
        reason_parts.append(f"Business model: {business_model}")
    if not reason_parts:
        return None
    return relevance, "; ".join(reason_parts[:3])


def filter_targets(companies: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    """Keep unique Kerala companies that meet the explainable software/IT rules."""
    target_records: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    kerala_count = 0

    for company in companies:
        if not is_kerala_location(company["location"]):
            continue
        kerala_count += 1
        classification = classify_company(company)
        if classification is None or company["ksum_url"] in seen_urls:
            continue
        relevance, reason = classification
        seen_urls.add(company["ksum_url"])
        target_records.append(
            {
                **company,
                "target_relevance": relevance,
                "target_reason": reason,
            }
        )

    return target_records, kerala_count


def save_csv(records: list[dict[str, str]], filename: Path) -> None:
    """Create the target CSV atomically without overwriting an existing result."""
    if filename.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing file: {filename}. "
            "Move, rename, or remove it before running again."
        )

    temporary_file = filename.with_name(f".{filename.name}.tmp")
    try:
        with temporary_file.open("w", encoding="utf-8-sig", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(records)
            csv_file.flush()
            os.fsync(csv_file.fileno())
        os.replace(temporary_file, filename)
    finally:
        if temporary_file.exists():
            temporary_file.unlink()


def location_group(location: str) -> str:
    """Return a compact Kerala-region group for the requested summary."""
    normalized_location = normalize(location)
    if "thiruvananthapuram" in normalized_location or "trivandrum" in normalized_location:
        return "Thiruvananthapuram"
    if "kochi" in normalized_location or "cochin" in normalized_location or "ernakulam" in normalized_location:
        return "Kochi/Ernakulam"
    if "kozhikode" in normalized_location or "calicut" in normalized_location:
        return "Kozhikode"
    if "thrissur" in normalized_location:
        return "Thrissur"
    return "Other Kerala"


def print_summary(
    companies: list[dict[str, str]], targets: list[dict[str, str]], kerala_count: int
) -> None:
    """Print auditable counts and a small sample for manual review."""
    unique_urls = len({target["ksum_url"] for target in targets})
    duplicate_count = len(targets) - unique_urls
    locations = Counter(location_group(target["location"]) for target in targets)
    sectors = Counter(target["sector"] or "(blank)" for target in targets)

    print("\n========================================")
    print("KSUM STAGE 1C FILTER COMPLETE")
    print("========================================")
    print(f"Input companies:                 {len(companies)}")
    print(f"Kerala companies:                {kerala_count}")
    print(f"Software/IT target companies:    {len(targets)}")
    print(f"Excluded:                        {len(companies) - len(targets)}")
    print(f"Output records:                  {len(targets)}")
    print(f"Unique KSUM URLs:                {unique_urls}")
    print(f"Duplicate URLs:                  {duplicate_count}")
    print(f"Output: {OUTPUT_FILE.name}")

    print("\nLocation breakdown:")
    for name in ("Thiruvananthapuram", "Kochi/Ernakulam", "Kozhikode", "Thrissur", "Other Kerala"):
        print(f"{name}: {locations[name]}")

    print("\nTop sectors in target list:")
    for sector, count in sectors.most_common(10):
        print(f"{sector}: {count}")

    print("\nSample targets:")
    for target in targets[:15]:
        print(
            f"- {target['company_name']} | {target['location']} | "
            f"{target['target_relevance']} | {target['target_reason']}"
        )


def main() -> None:
    try:
        master_hash_before = file_hash(INPUT_FILE)
        companies = load_master(INPUT_FILE)
        targets, kerala_count = filter_targets(companies)
        if not targets:
            raise ValueError("The filter produced no targets; no output was created.")
        if any(not is_kerala_location(target["location"]) for target in targets):
            raise ValueError("Validation failed: output contains a non-Kerala location.")
        if len(targets) != len({target["ksum_url"] for target in targets}):
            raise ValueError("Validation failed: output contains duplicate KSUM URLs.")

        save_csv(targets, OUTPUT_FILE)
        master_hash_after = file_hash(INPUT_FILE)
        if master_hash_before != master_hash_after:
            raise RuntimeError("The master dataset changed during filtering.")
        print_summary(companies, targets, kerala_count)
        print("Master dataset unchanged: yes")
    except (FileExistsError, OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
