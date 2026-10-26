# Technopark complete job collector

`technopark_job_collector.py` collects every public job record returned by the official Technopark Kerala JSON API, without role, category, experience, or company filtering. It is a collection stage only; suitability decisions belong in the Excel review workflow.

Official source: `https://technopark.in/api/paginated-jobs?page=1`.

## Setup and normal use

The project virtual environment already contains the two runtime dependencies: `requests` and `openpyxl`. From this project folder in Windows PowerShell:

```powershell
cd "C:\Users\afsal\OneDrive\Desktop\AI JobHunt\JoB-Weekly-Hunt"
.\.venv\Scripts\python.exe technopark_job_collector.py
```

The complete help and optional controls are available with:

```powershell
.\.venv\Scripts\python.exe technopark_job_collector.py --help
```

Options are `--output-dir PATH`, `--timeout SECONDS`, `--delay SECONDS`, `--max-retries COUNT`, `--no-excel`, and `--no-raw-archive`. Values are validated. `--no-excel` still produces JSON, CSV, and a report; `--no-raw-archive` does not write or move the raw responses.

## Collection workflow and completeness

The collector starts on page 1, reads `current_page`, `last_page`, `next_page_url`, `total`, and `per_page`, then requests pages sequentially. It follows `next_page_url` only if it is HTTPS on `technopark.in`, has the expected `/api/paginated-jobs` path, and contains a positive `page` parameter. When an acceptable next URL is absent but `last_page` says another page is expected, it constructs the next official API page URL. Repeated URLs/pages, malformed metadata, unsafe URLs, page failures, and changing metadata are logged and reported instead of silently being accepted.

Requests use a descriptive User-Agent, separate connection/response timeouts, a short delay, retryable handling for timeouts, connection errors, HTTP 429, and HTTP 5xx, exponential backoff, and `Retry-After` where available. Requests are intentionally sequential.

Collection status definitions:

- **COMPLETE** — page 1 succeeded; every page from 1 through the reported final page succeeded; the terminal page has no next page; and the final unique-record count equals the latest reported API total.
- **PARTIAL** — some usable records were received, but a request failed, pagination could not be fully verified, source metadata changed, a count disagreed, or collection was interrupted.
- **FAILED** — page 1 could not be collected or an output-integrity check failed.

The script compares raw and unique counts with the reported total. It never manufactures records or marks a mismatch complete.

## Outputs

All generated data is under `data/technopark/`:

- `technopark_all_jobs.json` is the authoritative UTF-8 export. Its `jobs` array contains original API records, including the complete nested `company` object and any future fields; `collection_metadata` is separate.
- `technopark_all_jobs.csv` is a UTF-8-with-BOM normalized export. Standard fields are readable columns, company fields are flattened, and unrecognized source/company values get deterministic `source_*` / `company_*` columns. Structured future values are JSON text only where a single CSV cell is necessary.
- `technopark_jobs_review.xlsx` contains every exported job on **Technopark Jobs**, with filters, frozen headers, wrapped text, date formatting, conditional status colors, verified detail hyperlinks, and an **Instructions** sheet.
- `raw/page_01.json`, `raw/page_02.json`, and so on are literal successful API responses from the latest archived run. Before writing a new archived run, older files matching only `raw/page_*.json` are moved to `raw/previous_runs/<UTC-run-timestamp>/`; unrelated files are untouched. Failed responses are never archived as pages.
- `reports/collection_report.json` contains timestamped request results, failures, observed pagination, counts, duplicates, URL validation, outputs, warnings, and output-validation results.
- `logs/technopark_collector.log` is the operational log.

## Fields, identifiers, and duplicate policy

JSON retains source values exactly. CSV and Excel expose Job ID, Job Listing ID, title, dates, original `is_walk_in`, a `Walk-in` value (`Yes`, `No`, or `Unknown`), company name/ID/logo path, promoted value, and verified job details URL. The workbook also has the editable **Review Status** and **Notes** columns.

Deduplication uses numeric `id`; only when that is unavailable, nonblank `job_listing_id` is used. The first source occurrence is retained deterministically. Repeated identifiers are counted; differing duplicates are listed in the report. Records with neither identifier are retained (not deduplicated) and reported. Titles and company names are never deduplication keys.

## Excel review workflow

Review Status has a dropdown: `Not Reviewed`, `Apply`, `Review`, `Skip`, or `Applied`. New jobs begin as **Not Reviewed** with a blank Notes cell. Before rebuilding an existing workbook, the collector makes a timestamped copy under `raw/workbook_backups/`, reads statuses and notes, and matches them by Job ID, falling back to Job Listing ID only when Job ID is missing. It then refreshes source fields but preserves the matching user values. Corrupt/unreadable workbooks are backed up and reported before replacement; no title-based transfer occurs.

## Detail URLs

The collector tests up to two actual collected IDs against the official detail-page path `https://technopark.in/job-details/<numeric job id>`. It enables the hyperlink column only when every representative page returns successfully and contains the matching source ID and title. The validation samples and result are in the report. If Technopark changes this behavior or it cannot be verified, links are intentionally blank; collection continues.

## Troubleshooting and verification

Open `data/technopark/reports/collection_report.json` first after every run. Confirm `collection_status`, `reported_api_total`, `pages_successfully_fetched`, `pages_failed`, `raw_records_received`, `unique_records_exported`, and `validation.passed`. A partial run is useful evidence but not a claim of a complete current portal snapshot; inspect `failed_pages` and rerun the normal command after the service recovers.

If the API returns HTML, malformed JSON, a new schema, rate limiting, or an error, the failure is recorded. The collector does not bypass access controls, CAPTCHAs, or authentication. New API fields remain intact in JSON but may require a future layout enhancement to gain a dedicated Excel column.

Run the local checks with:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The test suite covers URL safety, dynamic pagination/fallback, duplicate policy, output reopening, review preservation, malformed responses, and non-complete status on failed pages. The production run additionally reopens JSON, CSV, and Excel to validate the written files.
