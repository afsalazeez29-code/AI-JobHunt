"""Build deterministic seven-day company CSV allocations from verified local data."""

from __future__ import annotations

import csv
import hashlib
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


SOURCE_ROOT = Path(r"C:\Users\afsal\OneDrive\Desktop\AI JobHunt\Kerala IT DB")
WORKSPACE = Path(__file__).resolve().parent
SEED = 20261013
HEADER = ["Company Name", "Company Website"]
DAYS = [f"DAY{number}" for number in range(1, 8)]

ALLOCATIONS = {
    "Techno-Park": [70, 70, 70, 70, 70, 70, 69],
    "InfoPark": [14, 14, 14, 14, 13, 13, 13],
    "KSUM": [74, 74, 74, 73, 73, 73, 73],
    "Cyberpark": [9, 9, 9, 9, 9, 9, 8],
    "Kinfra": [4, 4, 3, 3, 3, 3, 3],
    "SmartCity": [4, 4, 3, 3, 3, 3, 3],
    "UL CyberPark": [6, 6, 6, 6, 6, 6, 6],
}

FILENAMES = {
    "Techno-Park": "techn-opark.csv",
    "InfoPark": "info-park.csv",
    "KSUM": "ksum.csv",
    "Cyberpark": "cyber-park.csv",
    "Kinfra": "kinfra.csv",
    "SmartCity": "smartcity.csv",
    "UL CyberPark": "ulcyberpark.csv",
}

EXPECTED = {pool: sum(counts) for pool, counts in ALLOCATIONS.items()}


class GateError(RuntimeError):
    """A mandatory source or target safety gate failed."""


def read_csv(relative_path: str) -> list[dict[str, str]]:
    path = SOURCE_ROOT / relative_path
    if not path.is_file():
        raise GateError(f"Required source is missing: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def require_columns(rows: list[dict[str, str]], columns: set[str], source: Path) -> None:
    actual = set(rows[0]) if rows else set()
    if not rows or not columns.issubset(actual):
        raise GateError(
            f"Unsupported source schema: {source}; "
            f"required={sorted(columns)}, actual={sorted(actual)}"
        )


def normal_name(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip()).casefold().rstrip(".")


def normal_domain(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    candidate = raw if "://" in raw else f"//{raw}"
    hostname = urlparse(candidate).hostname
    if not hostname or hostname.casefold() in {"http", "https"} or "." not in hostname:
        return ""
    return hostname.casefold().removeprefix("www.")


def record(name: str, website: str, source: str, index: int) -> dict[str, object]:
    cleaned_name = (name or "").strip()
    if not cleaned_name:
        raise GateError(f"Blank company name in {source}, record {index}")
    return {
        "name": cleaned_name,
        "website": (website or "").strip(),
        "source": source,
        "index": index,
    }


def assert_unique_names(pool: str, records: list[dict[str, object]]) -> None:
    seen: dict[str, dict[str, object]] = {}
    for item in records:
        key = normal_name(str(item["name"]))
        if key in seen:
            first = seen[key]
            raise GateError(
                f"{pool} has an undocumented duplicate canonical name: "
                f"{first['source']} record {first['index']} and "
                f"{item['source']} record {item['index']}"
            )
        seen[key] = item


def deduplicate_ul_pair(records: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[str]]:
    """Keep the first exact paired-source record using the required normalized key."""
    unique: list[dict[str, object]] = []
    removed: list[str] = []
    seen: dict[tuple[str, str], dict[str, object]] = {}
    for item in records:
        domain = normal_domain(str(item["website"]))
        key = ("domain", domain) if domain else ("name", normal_name(str(item["name"])))
        if key in seen:
            first = seen[key]
            if normal_name(str(first["name"])) != normal_name(str(item["name"])):
                raise GateError(
                    "UL CyberPark records share a website domain but have different "
                    f"names: {first['name']!r} and {item['name']!r}."
                )
            removed.append(
                f"UL CyberPark removed {item['source']} record {item['index']} "
                f"as duplicate of {first['source']} record {first['index']} "
                f"by {key[0]}={key[1]!r}."
            )
        else:
            seen[key] = item
            unique.append(item)
    return unique, removed


def load_pools() -> tuple[dict[str, list[dict[str, object]]], dict[str, dict[str, object]], list[str]]:
    reports: dict[str, dict[str, object]] = {}
    duplicate_log: list[str] = []

    tech_path = "Techno-Park/technopark-contacts.csv"
    tech_rows = read_csv(tech_path)
    require_columns(tech_rows, {"Company Name", "Website"}, SOURCE_ROOT / tech_path)
    tech = [record(row["Company Name"], row["Website"], tech_path, index)
            for index, row in enumerate(tech_rows, 2)]
    assert_unique_names("Techno-Park", tech)
    reports["Techno-Park"] = {
        "paths": [tech_path], "input_rows": len(tech_rows), "filtered": len(tech),
        "duplicates": 0, "rule": "README: one matched contact row per canonical normalized name.",
    }

    info_path = "infopark-scraper/infopark_companies_classified.csv"
    info_rows = read_csv(info_path)
    require_columns(info_rows, {"company_name", "website", "it_relevance"}, SOURCE_ROOT / info_path)
    info_filtered = [row for row in info_rows if row["it_relevance"] in {"High", "Medium"}]
    info = [record(row["company_name"], row["website"], info_path, index)
            for index, row in enumerate(info_filtered, 2)]
    assert_unique_names("InfoPark", info)
    reports["InfoPark"] = {
        "paths": [info_path], "input_rows": len(info_rows), "filtered": len(info),
        "duplicates": 0,
        "rule": "README: confirmed IT/ITeS membership is it_relevance High or Medium.",
    }

    ksum_path = "ksum-scraper/ksum_final_targets.csv"
    ksum_rows = read_csv(ksum_path)
    require_columns(ksum_rows, {"company_name", "website", "priority"}, SOURCE_ROOT / ksum_path)
    ksum_filtered = [row for row in ksum_rows if row["priority"] in {"A", "B"}]
    ksum = [record(row["company_name"], row["website"], ksum_path, index)
            for index, row in enumerate(ksum_filtered, 2)]
    assert_unique_names("KSUM", ksum)
    reports["KSUM"] = {
        "paths": [ksum_path], "input_rows": len(ksum_rows), "filtered": len(ksum),
        "duplicates": 0,
        "rule": "README: frozen final A/B-priority target pool.",
    }

    cyber_path = "cyberpark-scraper/cyberpark_companies.csv"
    cyber_readme_path = SOURCE_ROOT / "cyberpark-scraper/README.md"
    cyber_rows = read_csv(cyber_path)
    require_columns(cyber_rows, {"company_name", "website"}, SOURCE_ROOT / cyber_path)
    if not cyber_readme_path.is_file():
        raise GateError(f"Required source is missing: {cyber_readme_path}")
    cyber_readme = cyber_readme_path.read_text(encoding="utf-8")
    member_names: set[str] = set()
    for match in re.finditer(
        r"^### (?P<name>[^\r\n]+)\r?\n(?P<body>.*?)(?=^### |\Z)",
        cyber_readme,
        re.MULTILINE | re.DOTALL,
    ):
        if re.search(r"IT/ITeS:\s*Yes", match.group("body")):
            member_names.add(normal_name(match.group("name")))
    if len(member_names) != 62:
        raise GateError(
            f"Cyberpark README membership extraction returned {len(member_names)}, expected 62."
        )
    cyber = [
        record(row["company_name"], row["website"], cyber_path, index)
        for index, row in enumerate(cyber_rows, 2)
        if normal_name(row["company_name"]) in member_names
    ]
    if {normal_name(str(item["name"])) for item in cyber} != member_names:
        raise GateError("Cyberpark README IT/ITeS names do not map exactly to the base CSV.")
    assert_unique_names("Cyberpark", cyber)
    reports["Cyberpark"] = {
        "paths": [cyber_path, "cyberpark-scraper/README.md"],
        "input_rows": len(cyber_rows), "filtered": len(cyber), "duplicates": 0,
        "rule": "README IT/ITeS=Yes profile membership joined to base CSV website records.",
    }

    kinfra_path = "kinfra/kinfra_software_it_companies.csv"
    kinfra_rows = read_csv(kinfra_path)
    require_columns(kinfra_rows, {"company_name", "website"}, SOURCE_ROOT / kinfra_path)
    kinfra = [record(row["company_name"], row["website"], kinfra_path, index)
              for index, row in enumerate(kinfra_rows, 2)]
    assert_unique_names("Kinfra", kinfra)
    reports["Kinfra"] = {
        "paths": [kinfra_path], "input_rows": len(kinfra_rows), "filtered": len(kinfra),
        "duplicates": 0, "rule": "README: canonical 23-row source dataset.",
    }

    smartcity_path = "smartcity/smartcity_kochi_it_ites_companies.csv"
    smartcity_rows = read_csv(smartcity_path)
    require_columns(smartcity_rows, {"company_name", "website"}, SOURCE_ROOT / smartcity_path)
    smartcity = [record(row["company_name"], row["website"], smartcity_path, index)
                 for index, row in enumerate(smartcity_rows, 2)]
    assert_unique_names("SmartCity", smartcity)
    reports["SmartCity"] = {
        "paths": [smartcity_path], "input_rows": len(smartcity_rows), "filtered": len(smartcity),
        "duplicates": 0, "rule": "README: canonical 23-row source dataset.",
    }

    ul_paths = [
        "ulcyberpark-scraper/ulcyberpark_companies.csv",
        "ulcyberpark-scraper/ulcyberpark_companies_1.csv",
    ]
    ul_raw: list[dict[str, object]] = []
    for path in ul_paths:
        rows = read_csv(path)
        require_columns(rows, {"company_name", "website"}, SOURCE_ROOT / path)
        ul_raw.extend(record(row["company_name"], row["website"], path, index)
                      for index, row in enumerate(rows, 2))
    ul, ul_removed = deduplicate_ul_pair(ul_raw)
    duplicate_log.extend(ul_removed)
    reports["UL CyberPark"] = {
        "paths": ul_paths, "input_rows": len(ul_raw), "filtered": len(ul_raw),
        "duplicates": len(ul_removed),
        "rule": "README: combine exact paired CSV copies and retain first canonical row.",
    }

    pools = {
        "Techno-Park": tech, "InfoPark": info, "KSUM": ksum, "Cyberpark": cyber,
        "Kinfra": kinfra, "SmartCity": smartcity, "UL CyberPark": ul,
    }
    for pool, rows in pools.items():
        reports[pool]["final"] = len(rows)
        if len(rows) != EXPECTED[pool]:
            report = reports[pool]
            raise GateError(
                f"{pool} final count mismatch: source={report['paths']}; "
                f"input={report['input_rows']}; filtered={report['filtered']}; "
                f"duplicates={report['duplicates']}; final={len(rows)}; "
                f"expected={EXPECTED[pool]}."
            )
    return pools, reports, duplicate_log


def target_safety_gate() -> None:
    required_names = set(FILENAMES.values())
    conflicts: list[str] = []
    for day in DAYS:
        folder = WORKSPACE / day
        if folder.exists():
            for path in folder.glob("*.csv"):
                if path.name not in required_names:
                    conflicts.append(f"Unexpected CSV in target folder: {path}")
        for filename in required_names:
            path = folder / filename
            if not path.exists():
                continue
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle))
            data_rows = max(0, len(rows) - 1)
            if data_rows:
                conflicts.append(f"Target already has {data_rows} data rows: {path}")
            elif rows and rows[0] != HEADER:
                conflicts.append(f"Header-only target has incorrect header: {path}")
    if conflicts:
        raise GateError("Target-file safety gate failed:\n" + "\n".join(conflicts))


def shuffle_and_split(pool: str, rows: list[dict[str, object]]) -> list[list[dict[str, object]]]:
    shuffled = list(rows)
    pool_seed = int.from_bytes(
        hashlib.sha256(f"{SEED}:{pool}".encode("utf-8")).digest()[:8], "big"
    )
    random.Random(pool_seed).shuffle(shuffled)
    batches: list[list[dict[str, object]]] = []
    start = 0
    for expected in ALLOCATIONS[pool]:
        batches.append(shuffled[start:start + expected])
        start += expected
    if start != len(shuffled):
        raise GateError(f"{pool} split lost or repeated records.")
    combined = [item for batch in batches for item in batch]
    if len({(item["source"], item["index"]) for item in combined}) != len(combined):
        raise GateError(f"{pool} split assigned a source record more than once.")
    return batches


def write_outputs(batches: dict[str, list[list[dict[str, object]]]]) -> None:
    for day_index, day in enumerate(DAYS):
        folder = WORKSPACE / day
        folder.mkdir(parents=True, exist_ok=True)
        for pool, filename in FILENAMES.items():
            path = folder / filename
            with path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(HEADER)
                writer.writerows(
                    [item["name"], item["website"]]
                    for item in batches[pool][day_index]
                )


def verify_outputs(batches: dict[str, list[list[dict[str, object]]]]) -> tuple[dict[str, int], dict[str, int]]:
    pool_totals = Counter()
    day_totals = Counter()
    required_names = set(FILENAMES.values())
    for day_index, day in enumerate(DAYS):
        folder = WORKSPACE / day
        actual_names = {path.name for path in folder.glob("*.csv")}
        missing = required_names - actual_names
        if missing:
            raise GateError(f"{folder} missing target CSVs: {sorted(missing)}")
        for pool, filename in FILENAMES.items():
            path = folder / filename
            raw = path.read_bytes()
            bom_ok = raw.startswith(b"\xef\xbb\xbf")
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle))
            expected = ALLOCATIONS[pool][day_index]
            actual = len(rows) - 1
            header_ok = bool(rows) and rows[0] == HEADER
            names_ok = all(len(row) == 2 and row[0].strip() for row in rows[1:])
            expected_rows = [
                [str(item["name"]), str(item["website"])]
                for item in batches[pool][day_index]
            ]
            duplicate_ok = len({tuple(row) for row in rows[1:]}) == actual
            status = "PASS" if (
                actual == expected and header_ok and names_ok and duplicate_ok
                and bom_ok and rows[1:] == expected_rows
            ) else "FAIL"
            print(
                f"{day} | {filename} | expected={expected} | actual={actual} | "
                f"headers={header_ok} | duplicates={duplicate_ok} | bom={bom_ok} | {status}"
            )
            if status != "PASS":
                raise GateError(f"Post-generation validation failed: {path}")
            pool_totals[pool] += actual
            day_totals[day] += actual
    if sum(pool_totals.values()) != 1248 or sum(day_totals.values()) != 1248:
        raise GateError("Generated total is not 1,248 records.")
    return dict(pool_totals), dict(day_totals)


def cross_pool_overlaps(pools: dict[str, list[dict[str, object]]]) -> list[str]:
    locations: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for pool, rows in pools.items():
        for item in rows:
            locations[normal_name(str(item["name"]))].append((pool, str(item["name"])))
    return [
        f"{name}: " + ", ".join(f"{pool} ({display})" for pool, display in entries)
        for name, entries in sorted(locations.items())
        if len({pool for pool, _ in entries}) > 1
    ]


def main() -> int:
    try:
        pools, reports, duplicate_log = load_pools()
        print("POOL SOURCE AND FILTER REPORT")
        print("Pool | Selected source path | Input | Filtered | Duplicates | Final | Expected | Status")
        for pool in FILENAMES:
            report = reports[pool]
            print(
                f"{pool} | {' + '.join(report['paths'])} | {report['input_rows']} | "
                f"{report['filtered']} | {report['duplicates']} | {report['final']} | "
                f"{EXPECTED[pool]} | PASS"
            )
        print("DUPLICATES REMOVED")
        if duplicate_log:
            for line in duplicate_log:
                print(line)
        else:
            print("None.")

        target_safety_gate()
        batches = {pool: shuffle_and_split(pool, rows) for pool, rows in pools.items()}
        write_outputs(batches)
        print("PER-FILE VERIFICATION")
        pool_totals, day_totals = verify_outputs(batches)

        print("ALLOCATION TOTALS")
        for pool in FILENAMES:
            print(f"{pool}: {pool_totals[pool]}")
        for day in DAYS:
            print(f"{day}: {day_totals[day]}")
        print(f"TOTAL: {sum(pool_totals.values())}")
        print("BLANK WEBSITE COUNTS")
        for pool, rows in pools.items():
            print(f"{pool}: {sum(not str(item['website']).strip() for item in rows)}")
        print("CROSS-POOL OVERLAPS")
        overlaps = cross_pool_overlaps(pools)
        if overlaps:
            for line in overlaps:
                print(line)
        else:
            print("None.")
        print("RESULT: PASS")
        return 0
    except GateError as error:
        print(f"RESULT: INCOMPLETE\n{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
