"""Review Stage 1C Medium targets using only existing local KSUM datasets."""

from __future__ import annotations

import csv
import hashlib
import os
import sys
from collections import Counter
from pathlib import Path


SOURCE_FILE = Path(__file__).with_name("ksum_kerala_software_it_targets.csv")
MASTER_FILE = Path(__file__).with_name("ksum_companies_enriched.csv")
REFINED_FILE = Path(__file__).with_name("ksum_kerala_software_it_targets_refined.csv")
AUDIT_FILE = Path(__file__).with_name("ksum_kerala_software_it_review.csv")

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
    "target_relevance",
    "target_reason",
]
AUDIT_COLUMNS = [
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
    "previous_relevance",
    "previous_reason",
    "final_classification",
    "final_reason",
]
REFINED_COLUMNS = SOURCE_COLUMNS + ["final_classification", "final_reason"]


# This is an explicit review matrix for every Stage 1C Medium record. Reasons
# refer only to fields already present in the local KSUM CSVs.
MEDIUM_DECISIONS: dict[str, tuple[str, str]] = {
    "4CHAMPZ INNOVATIVE PRIVATE LIMITED": ("HIGH", "Mobile Apps + AI / ML + Platform"),
    "70mm Media Village LLP": ("MEDIUM", "AdTech + Mobile Apps; software core not fully established"),
    "Aasayaa Media Soultions": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ABROADANGELS CONSULTANCY PRIVATE LIMITED": ("EXCLUDE", "Web technologies alone; sector and industry are Other"),
    "ABROBS PRIVATE LIMITED": ("HIGH", "AI / ML + Web technologies + B2B SaaS"),
    "ACCESSIBILITY HUB PRIVATE LIMITED": ("MEDIUM", "AI / ML present, but Manufacturing and Sustainable Construction are also listed"),
    "ACCGUY FINANCIAL SERVICES PRIVATE LIMITED": ("MEDIUM", "Financial Services + Web technologies + Platform; software core unclear"),
    "ADDAY CREATIVE LLP": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ADHYAYA EDUCATIONAL SOLUTIONS PRIVATE LIMITED": ("MEDIUM", "EdTech + Platform + Geographic Information Systems; developer relevance is possible but unclear"),
    "ADOWINGS PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ADPUMB PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ADSFLO WORLDWIDE PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ADWAYGA PRIVATE LIMITED": ("MEDIUM", "Telecom + Web technologies + Internet of Things (IoT)"),
    "AESA SPORTS AND ENTERTAINMENTS PRIVATE LIMITED": ("MEDIUM", "EdTech/Fitness + Mobile Apps + Web technologies; software core unclear"),
    "AEYEGLANCE PRIVATE LIMITED": ("HIGH", "AI / ML + SaaS + Freemium"),
    "AGC ENFORCEMENT SERVICES PRIVATE LIMITED": ("HIGH", "Cyber Security + Mobile Apps + Internet of Things (IoT)"),
    "AGRI ASSIST INNOVATIONS LLP": ("HIGH", "Agri Tech + Mobile Apps + Internet of Things (IoT) + SaaS Platform"),
    "AIBAK VENTURES PRIVATE LIMITED": ("HIGH", "Real Estate Tech / Prop Tech + Mobile Apps + Web technologies + AI / ML + SaaS"),
    "AION CREATIVE WINGS LLP": ("MEDIUM", "Social Media + Web technologies + Freemium; software core unclear"),
    "AKATSA LLP": ("MEDIUM", "Real Estate Tech / Prop Tech + Mobile Apps + Platform; software core unclear"),
    "AKINOZ DIGITAL MEDIA LLP": ("MEDIUM", "AdTech + Mobile Apps; software core not fully established"),
    "ALGORYTHAM TECHNOLOGIES PRIVATE LIMITED": ("HIGH", "AI / ML + Web technologies + Mobile Apps + SaaS Platform"),
    "ALJALEEDI TRADING LLP": ("MEDIUM", "Agri Tech + Blockchain + AI / ML + Internet of Things (IoT); software core unclear"),
    "ALLSCOPE INDIA PRIVATE LIMITED": ("HIGH", "Internet of Things (IoT) + Mobile Apps + Web technologies + B2B SaaS Platform"),
    "ALPHANEX TECHNOLOGIES LLP": ("MEDIUM", "Web technologies + Big data; sector and industry are Other"),
    "ALTIBIX CODELAB PRIVATE LIMITED": ("MEDIUM", "AdTech + Mobile Apps + Web technologies; software core not fully established"),
    "ALTIX PUBLISHER PRIVATE LIMITED": ("EXCLUDE", "Web technologies alone; sector and industry are Other"),
    "AMLIRE PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies + Internet of Things (IoT); software core unclear"),
    "ANK LIFECARE PRIVATE LIMITED": ("EXCLUDE", "Assistive Tech + Manufacturing; software signal is absent"),
    "AONZ AI TECHNOSYS SOLUTIONS PRIVATE LIMITED": ("HIGH", "AI / ML + B2B SaaS"),
    "APP INTEGRITY PRIVATE LIMITED": ("HIGH", "AI / ML + Mobile Apps + B2B SaaS"),
    "APPSTRAY PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ARCHISOFT IT SOLUTIONS PRIVATE LIMITED": ("HIGH", "Web technologies + AI / ML + Mobile Apps + SaaS"),
    "ARKS Enterprises": ("EXCLUDE", "Web technologies alone with D2C business model"),
    "ARTIFEX STUDIOS PRIVATE LIMITED": ("MEDIUM", "AdTech + Mobile Apps; software core not fully established"),
    "ARUNRAJKARTHA PRODUCTIONS PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ASIOS ALLIANCE PRIVATE LIMITED": ("EXCLUDE", "Web technologies alone; sector and industry are Other"),
    "Asta Infotech": ("EXCLUDE", "Web technologies alone; sector and industry are Other"),
    "AT BOTS": ("HIGH", "AI / ML + Drones + Robotics + B2B SaaS"),
    "Atbott Solutions": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "ATHELSTAN TECHNOLABS PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "AUDENTO DIGITAL PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "Augmenta Innovations Private Limited": ("MEDIUM", "EdTech + Augmented Reality (AR) + Virtual Reality (VR); software core unclear"),
    "AURAFINA TECHNOLOGIES PRIVATE LIMITED": ("MEDIUM", "Social Media + Mobile Apps + Web technologies; software core unclear"),
    "AURIX BUSINESS CORP PRIVATE LIMITED": ("EXCLUDE", "Web technologies alone; sector and industry are Other"),
    "AUTOMITHRA INDIA PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "AVARTA IT AND DESIGN SOLUTIONS PRIVATE LIMITED": ("MEDIUM", "AI / ML + Biotechnology + Drones + Platform; software core unclear"),
    "AVB PRECIPRO (OPC) PRIVATE LIMITED": ("EXCLUDE", "3D Printing + AI / ML; software core is not established"),
    "AYALSKILL PRIVATE LIMITED": ("MEDIUM", "Web technologies + Marketplace; sector and industry are Other"),
    "BANZAN VENTURES PRIVATE LIMITED": ("HIGH", "Gaming + Mobile Apps + Web technologies + SaaS Platform"),
    "BE LITTLE THINGS LLP": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "BEFIND SOLUTIONS PRIVATE LIMITED": ("MEDIUM", "AdTech + Mobile Apps + Marketplace; software core unclear"),
    "BENETIZE PRIVATE LIMITED": ("MEDIUM", "Healthcare IT is listed, but Technology is Biotechnology only"),
    "BENLOTEX PRIVATE LIMITED": ("MEDIUM", "AI / ML, Big data, Blockchain, IoT, and Robotics are listed across mixed sectors"),
    "BENLYCOS PRIVATE LIMITED": ("HIGH", "Telecom + Web technologies + Cyber Security"),
    "BESTER ACADEMY STUDY IN INDIA AND ABROAD PRIVATE LIMITED": ("MEDIUM", "EdTech + Geographic Information Systems; software core unclear"),
    "BHARAT WIFI PRIVATE LIMITED": ("HIGH", "AI / ML + Big data + B2B/B2G SaaS"),
    "BIGSLATE MEDIA SOLUTIONS PRIVATE LIMITED": ("MEDIUM", "Social Media + Web technologies; software core unclear"),
    "BILDX TECHNOLOGIES PRIVATE LIMITED": ("HIGH", "Real Estate Tech / Prop Tech + AI / ML + Big data + Virtual Reality (VR) Platform"),
    "BIOTA PRECISION AGRICULTURE PRIVATE LIMITED": ("HIGH", "Agri Tech + Internet of Things (IoT) + Mobile Apps + B2B/B2G SaaS"),
    "BIRAPT MARKETING AND SOLUTIONS PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "BISAURA TECHNOLOGIES PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "BIZATOM UNIVERSAL LOYALTY CARD PRIVATE LIMITED": ("MEDIUM", "FinTech + Internet of Things (IoT) + Security technology; software core unclear"),
    "BLOUNGE CO-WORKING PRIVATE LIMITED": ("EXCLUDE", "Co-working business with Big data only"),
    "BLUSTEAK MEDIA PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "BNKHUB FINSERV PRIVATE LIMITED": ("MEDIUM", "Financial Services + Mobile Apps + Platform; software core unclear"),
    "BOOFIGO ORDERING APP (OPC) PRIVATE LIMITED": ("MEDIUM", "Mobile Apps + Geographic Information Systems + Big data; sector and industry are Other"),
    "BOTCAST INDUSTRIES PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "Brai Ro Tech Private Limited": ("EXCLUDE", "Assistive Tech + Sensors + Manufacturing; software signal is absent"),
    "BRANDFELL TECHNOLOGIES PRIVATE LIMITED": ("MEDIUM", "AdTech/EdTech + Web technologies; software core unclear"),
    "Branding Hut": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "Bridging Dots Media Solutions Private Limited": ("MEDIUM", "Social Media + Web technologies; software core unclear"),
    "BTREE IOT TECHNOLOGIES PRIVATE LIMITED": ("EXCLUDE", "Assistive Tech + Sensors + Manufacturing; software signal is absent"),
    "BUDMORE AGRO INDUSTRIES PRIVATE LIMITED": ("HIGH", "Agri Tech + Internet of Things (IoT) + Mobile Apps + AI / ML + SaaS Platform"),
    "BUFFERBYTES TECHNOLOGIES PRIVATE LIMITED": ("HIGH", "AI / ML + Big data + Mobile Apps + B2B SaaS"),
    "BURSTCODE TECHNOLOGIES PRIVATE LIMITED": ("EXCLUDE", "Assistive Tech + Sensors; software signal is absent"),
    "BYTE7 SERVICES PRIVATE LIMITED": ("MEDIUM", "Social Media + Web technologies; software core unclear"),
    "BYTEDART TECHNOLOGIES PRIVATE LIMITED": ("MEDIUM", "AdTech + Mobile Apps + Web technologies; software core not fully established"),
    "BZOLUTIONS GLOBAL PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "C SCHOOL OF CREATIVE STUDIES LLP": ("MEDIUM", "EdTech/AdTech + AI / ML + Web technologies + Mobile Apps; software core unclear"),
    "Captains Social Foundation": ("EXCLUDE", "Web technologies alone; sector and industry are Other"),
    "CEED EDU SOLUTIONS PRIVATE LIMITED": ("MEDIUM", "EdTech + Internet of Things (IoT); software core unclear"),
    "CENTRE FOR INCLUSION STANDARDS AND PRACTICE PRIVATE LIMITED": ("HIGH", "AI / ML + Big data + Internet of Things (IoT) + SaaS"),
    "CHAMS PHYGITAL MEDIA PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "CHIRAMEL VENTURES PRIVATE LIMITED": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "CIBERA DEFENCE PRIVATE LIMITED": ("HIGH", "Cyber Security + Internet of Things (IoT)"),
    "CINEMACLUBBY BUSINESS SOLUTIONS PRIVATE LIMITED": ("MEDIUM", "Social Media + Web technologies; software core unclear"),
    "CINESENTINEL PRIVATE LIMITED": ("MEDIUM", "AdTech + AI / ML + Security technology; software core unclear"),
    "CIVRA TECH PRIVATE LIMITED": ("HIGH", "Real Estate Tech / Prop Tech + Web technologies + Mobile Apps + SaaS"),
    "CLAZZO INNOVATIONS LLP": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "CLIMAI CLEANTECH PRIVATE LIMITED": ("HIGH", "AI / ML + Big data + Internet of Things (IoT) + B2B SaaS Platform"),
    "CLOCKWELL INTERNATIONAL LLP": ("EXCLUDE", "Web technologies alone; sector and industry are Other"),
    "COCHIN STERILISATION SERVICES PRIVATE LIMITED": ("EXCLUDE", "Biotechnology and IoT are listed, but software core is not established"),
    "CODEACE IT SOLUTIONS LLP": ("MEDIUM", "AdTech + Web technologies; software core not fully established"),
    "CODECARROTS TECHNOLOGIES LLP": ("HIGH", "Mobile Apps + Web technologies + B2B/B2C"),
    "CODX SYSTEMS": ("MEDIUM", "Manufacturing + Robotics + Sensors + AI / ML; software core unclear"),
    "COGNIFLUENZ DEEPTECH PRIVATE LIMITED": ("HIGH", "AI / ML + Drones + Robotics + B2B SaaS"),
    "COMFINITY TECHNOLOGIES PRIVATE LIMITED": ("HIGH", "AI / ML + Big data + Blockchain + Platform"),
}


def file_hash(path: Path) -> str:
    """Return a content hash so source files can be verified as unchanged."""
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_csv(path: Path, expected_columns: list[str]) -> list[dict[str, str]]:
    """Load a UTF-8 CSV and require the expected column order."""
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


def write_csv_atomically(
    records: list[dict[str, str]], path: Path, fieldnames: list[str]
) -> None:
    """Write a complete replacement file before atomically publishing it."""
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


def location_group(location: str) -> str:
    """Return the requested Kerala-region summary category."""
    value = location.casefold()
    if "thiruvananthapuram" in value or "trivandrum" in value:
        return "Thiruvananthapuram"
    if "kochi" in value or "cochin" in value or "ernakulam" in value:
        return "Kochi/Ernakulam"
    if "kozhikode" in value or "calicut" in value:
        return "Kozhikode"
    if "thrissur" in value:
        return "Thrissur"
    return "Other Kerala"


def build_review(
    targets: list[dict[str, str]]
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Make one explicit final decision for each Stage 1C Medium record."""
    previous_high = [row for row in targets if row["target_relevance"] == "High"]
    medium_rows = [row for row in targets if row["target_relevance"] == "Medium"]
    if len(previous_high) != 431 or len(medium_rows) != 98:
        raise ValueError(
            f"Expected 431 High and 98 Medium rows, found "
            f"{len(previous_high)} High and {len(medium_rows)} Medium."
        )

    medium_names = {row["company_name"] for row in medium_rows}
    if len(medium_names) != len(medium_rows):
        raise ValueError("Medium company names are not unique; review map cannot be applied safely.")
    if set(MEDIUM_DECISIONS) != medium_names:
        missing = sorted(medium_names - set(MEDIUM_DECISIONS))
        extra = sorted(set(MEDIUM_DECISIONS) - medium_names)
        raise ValueError(f"Review matrix mismatch. Missing: {missing}; extra: {extra}")

    audit_records: list[dict[str, str]] = []
    accepted_medium_rows: list[dict[str, str]] = []
    for row in medium_rows:
        final_classification, final_reason = MEDIUM_DECISIONS[row["company_name"]]
        if final_classification not in {"HIGH", "MEDIUM", "EXCLUDE"}:
            raise ValueError(f"Invalid final classification for {row['company_name']}")
        audit_records.append(
            {
                **{column: row[column] for column in SOURCE_COLUMNS[:10]},
                "previous_relevance": row["target_relevance"],
                "previous_reason": row["target_reason"],
                "final_classification": final_classification,
                "final_reason": final_reason,
            }
        )
        if final_classification != "EXCLUDE":
            accepted_medium_rows.append(
                {
                    **row,
                    "final_classification": final_classification,
                    "final_reason": final_reason,
                }
            )

    refined_high_rows = [
        {
            **row,
            "final_classification": "HIGH",
            "final_reason": "Preserved Stage 1C High classification",
        }
        for row in previous_high
    ]
    return refined_high_rows + accepted_medium_rows, audit_records


def validate(
    targets: list[dict[str, str]],
    refined: list[dict[str, str]],
    audit: list[dict[str, str]],
    master_rows: list[dict[str, str]],
) -> None:
    """Validate preservation, complete review coverage, and URL uniqueness."""
    previous_high = [row for row in targets if row["target_relevance"] == "High"]
    medium_rows = [row for row in targets if row["target_relevance"] == "Medium"]
    if len(audit) != len(medium_rows) or {row["ksum_url"] for row in audit} != {
        row["ksum_url"] for row in medium_rows
    }:
        raise ValueError("Every Medium row must appear exactly once in the audit CSV.")
    if any(row["final_classification"] not in {"HIGH", "MEDIUM", "EXCLUDE"} for row in audit):
        raise ValueError("Audit contains an invalid final classification.")
    if any(row["final_classification"] == "EXCLUDE" for row in refined):
        raise ValueError("Refined output must not contain EXCLUDE records.")

    refined_urls = [row["ksum_url"] for row in refined]
    if len(refined_urls) != len(set(refined_urls)):
        raise ValueError("Refined output contains duplicate KSUM URLs.")
    if not {row["ksum_url"] for row in previous_high}.issubset(set(refined_urls)):
        raise ValueError("One or more existing High records were not preserved.")

    master_by_url = {row["ksum_url"]: row for row in master_rows}
    source_fields = SOURCE_COLUMNS[:10]
    for row in refined:
        master_row = master_by_url.get(row["ksum_url"])
        if master_row is None or any(row[field] != master_row[field] for field in source_fields):
            raise ValueError(f"Source values were not preserved for {row['ksum_url']}")


def print_summary(
    refined: list[dict[str, str]], audit: list[dict[str, str]]
) -> None:
    """Print requested outcome metrics and every concise Medium decision."""
    review_counts = Counter(row["final_classification"] for row in audit)
    final_counts = Counter(row["final_classification"] for row in refined)
    unique_urls = len({row["ksum_url"] for row in refined})
    locations = Counter(location_group(row["location"]) for row in refined)
    sectors = Counter(row["sector"] or "(blank)" for row in refined)

    print("\n========================================")
    print("KSUM STAGE 1C.1 REVIEW COMPLETE")
    print("========================================")
    print("Previous High:              431")
    print(f"Medium reviewed:             {len(audit)}")
    print(f"Medium -> High:              {review_counts['HIGH']}")
    print(f"Medium -> Medium:            {review_counts['MEDIUM']}")
    print(f"Medium -> Exclude:           {review_counts['EXCLUDE']}")
    print(f"Final High:                  {final_counts['HIGH']}")
    print(f"Final Medium:                {final_counts['MEDIUM']}")
    print(f"Final Target Companies:      {len(refined)}")
    print(f"Unique KSUM URLs:            {unique_urls}")
    print(f"Duplicate URLs:              {len(refined) - unique_urls}")
    print(f"Output: {REFINED_FILE.name}")
    print(f"Audit: {AUDIT_FILE.name}")

    print("\nFinal location breakdown:")
    for name in ("Thiruvananthapuram", "Kochi/Ernakulam", "Kozhikode", "Thrissur", "Other Kerala"):
        print(f"{name}: {locations[name]}")

    print("\nTop sectors in final target list:")
    for sector, count in sectors.most_common(10):
        print(f"{sector}: {count}")

    print("\nMedium review decisions:")
    for row in audit:
        print(
            f"- {row['company_name']} | {row['location']} | "
            f"{row['previous_relevance']} -> {row['final_classification']} | "
            f"{row['final_reason']}"
        )


def main() -> None:
    try:
        source_hash_before = file_hash(SOURCE_FILE)
        master_hash_before = file_hash(MASTER_FILE)
        targets = load_csv(SOURCE_FILE, SOURCE_COLUMNS)
        master_rows = load_csv(MASTER_FILE, SOURCE_COLUMNS[:10])
        refined, audit = build_review(targets)
        validate(targets, refined, audit, master_rows)
        write_csv_atomically(refined, REFINED_FILE, REFINED_COLUMNS)
        write_csv_atomically(audit, AUDIT_FILE, AUDIT_COLUMNS)

        if source_hash_before != file_hash(SOURCE_FILE):
            raise RuntimeError("Stage 1C source CSV changed during review.")
        if master_hash_before != file_hash(MASTER_FILE):
            raise RuntimeError("Master CSV changed during review.")
        print_summary(refined, audit)
        print("Source datasets unchanged: yes")
    except (FileExistsError, OSError, RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
