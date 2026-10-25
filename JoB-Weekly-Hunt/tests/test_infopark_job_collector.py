import csv
import json
from pathlib import Path

import pytest
from openpyxl import load_workbook

from infopark_job_collector import FIELDS, InfoparkCollector


FIXTURES = Path(__file__).parent / "fixtures"


def listing_html(rows: str, pagination: str = "") -> str:
    return f"""<div id='job-list'><table><thead><tr>
    <th>Date of Posting</th><th>Job Title</th><th>Company Name</th><th>Last Date to Apply</th><th></th>
    </tr></thead><tbody>{rows}</tbody></table></div>{pagination}"""


def valid_row(url: str = "/company-jobs/details/12/987") -> str:
    return f"""<tr><td>01-01-2026</td><td>Data Engineer</td><td>Example &amp; Co.</td>
    <td>31 Jan 2026</td><td><a href='{url}'>Details</a></td></tr>"""


def record(url: str, **changes: str) -> dict[str, str]:
    value = {field: "" for field in FIELDS}
    value.update({"job_id": InfoparkCollector.job_id_from_url(url), "job_title": "Data Engineer",
                  "company_name": "Example Co.", "job_details_url": url, "source_portal": "Infopark",
                  "source_page": "1", "collected_at": "2026-01-01T00:00:00+00:00"})
    value.update(changes)
    return value


def test_parse_live_listing_fixture_extracts_expected_fields():
    html = (FIXTURES / "listing_page_live_sample.html").read_text(encoding="utf-8")
    parsed = InfoparkCollector.parse_listing_page(html, 1, "2026-01-01T00:00:00+00:00", "test")
    assert len(parsed.records) == 20
    first = parsed.records[0]
    assert first["job_title"] == "Legal Content Specialist (LLB)"
    assert first["company_name"] == "Mozilor Technologies Pvt. Ltd."
    assert first["date_posted"] == "25-10-2026"
    assert first["application_deadline"] == "26 Oct 2026"
    assert first["job_id"] == "26372"
    assert parsed.max_page == 21


def test_parse_listing_finds_pagination_and_normalizes_relative_link():
    html = listing_html(valid_row(), "<ul class='pagination'><li><a href='/companies-job?page=8'>8</a></li><li><a rel='next' href='?page=2'>Next</a></li></ul>")
    parsed = InfoparkCollector.parse_listing_page(html, 1, "now", "run")
    assert parsed.max_page == 8
    assert parsed.has_next
    assert parsed.records[0]["job_details_url"] == "https://infopark.in/company-jobs/details/12/987"


def test_empty_and_malformed_rows_are_reported():
    html = listing_html("<tr><td></td></tr><tr><td>a</td><td>b</td></tr>" + valid_row())
    parsed = InfoparkCollector.parse_listing_page(html, 3, "now", "run")
    assert len(parsed.records) == 1
    assert any("empty row" in warning for warning in parsed.warnings)
    assert any("malformed row" in warning for warning in parsed.warnings)


def test_missing_listing_table_raises_clear_error():
    with pytest.raises(ValueError, match="job-list table"):
        InfoparkCollector.parse_listing_page("<html><body>Unavailable</body></html>", 1, "now", "run")


def test_deduplicate_only_by_canonical_detail_url():
    url = "https://infopark.in/company-jobs/details/12/987"
    unique, duplicates = InfoparkCollector.deduplicate([record(url), record(url), record("https://infopark.in/company-jobs/details/12/988")])
    assert len(unique) == 2
    assert duplicates == 1


def test_failed_initial_request_reports_incomplete(monkeypatch, tmp_path):
    collector = InfoparkCollector(tmp_path, delay=0)
    monkeypatch.setattr(collector, "get_text", lambda _: (_ for _ in ()).throw(RuntimeError("network down")))
    report = collector.collect_all_pages("run")
    assert not report["complete_collection_success"]
    assert report["failed_pages"][0]["page"] == 1


def test_write_outputs_creates_csv_json_workbook_and_preserves_manual_values(tmp_path):
    collector = InfoparkCollector(tmp_path, delay=0)
    data_dir = tmp_path / "data" / "infopark"
    old = record("https://infopark.in/company-jobs/details/12/987", my_decision="Apply", notes="Send portfolio")
    collector._write_csv(data_dir / "infopark_all_jobs.csv", [old])
    report = {"collection_started_at": "now", "collection_finished_at": "now", "source_url": "source",
              "pagination": {"pages_expected": 1, "terminal_page": 1, "terminal_page_verified": True, "safety_limit": 2},
              "pages_attempted": [1], "pages_successful": [1], "failed_pages": [], "raw_row_count": 1,
              "unique_vacancy_count": 1, "duplicate_count": 0, "malformed_row_count": 0,
              "records_missing_required_fields": 0, "unexpected_empty_pages": [], "validation_warnings": [], "pagination_completion_verified": True,
              "complete_collection_success": True, "records": [record("https://infopark.in/company-jobs/details/12/987")]}
    outputs = collector.write_outputs(report)
    with open(outputs["csv"], encoding="utf-8-sig", newline="") as handle:
        current = next(csv.DictReader(handle))
    assert current["my_decision"] == "Apply"
    assert current["notes"] == "Send portfolio"
    assert json.loads(Path(outputs["json"]).read_text(encoding="utf-8"))[0]["job_title"] == "Data Engineer"
    workbook = load_workbook(outputs["xlsx"])
    assert workbook["All Jobs"].freeze_panes == "A2"
    assert workbook["All Jobs"].auto_filter.ref == "A1:P2"
    assert workbook["All Jobs"].data_validations.count == 1


def test_partial_run_preserves_primary_dataset(tmp_path):
    collector = InfoparkCollector(tmp_path, delay=0)
    data_dir = tmp_path / "data" / "infopark"
    primary = data_dir / "infopark_all_jobs.csv"
    collector._write_csv(primary, [record("https://infopark.in/company-jobs/details/1/1", job_title="Existing")])
    report = {"collection_started_at": "now", "collection_finished_at": "now", "source_url": "source",
              "pagination": {"pages_expected": 2, "terminal_page": 2, "terminal_page_verified": False, "safety_limit": 2},
              "pages_attempted": [1, 2], "pages_successful": [1], "failed_pages": [{"page": 2, "url": "x", "error": "bad"}],
              "raw_row_count": 1, "unique_vacancy_count": 1, "duplicate_count": 0, "malformed_row_count": 0,
              "records_missing_required_fields": 0, "unexpected_empty_pages": [], "validation_warnings": [], "pagination_completion_verified": False,
              "complete_collection_success": False, "records": [record("https://infopark.in/company-jobs/details/1/2", job_title="Partial")]}
    outputs = collector.write_outputs(report)
    assert "csv" not in outputs
    assert "Existing" in primary.read_text(encoding="utf-8-sig")
    assert Path(outputs["snapshot_csv"]).exists()


def test_detail_fixture_has_relevant_content():
    text = (FIXTURES / "detail_page_live_sample.html").read_text(encoding="utf-8")
    assert "RESPONSIBILITIES" in text
