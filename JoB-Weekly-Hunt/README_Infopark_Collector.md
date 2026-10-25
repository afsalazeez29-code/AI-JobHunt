# Infopark complete job collector

This project collects every publicly accessible vacancy on Infopark Kerala's **All Parks** page, without filtering any job category. It uses the server-rendered official listing at `https://infopark.in/companies-job`, so no browser automation is required.

## Set up (Windows PowerShell)

Python 3.10+ is required. From this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the virtual environment's interpreter directly in every command:

```powershell
.\.venv\Scripts\python.exe infopark_job_collector.py
```

## Run it

```powershell
# Complete, unfiltered listing collection
.\.venv\Scripts\python.exe infopark_job_collector.py

# Inspect first/terminal pagination pages only
.\.venv\Scripts\python.exe infopark_job_collector.py --discover-pages

# Retry only pages which failed in the prior run
.\.venv\Scripts\python.exe infopark_job_collector.py --retry-failed

# Also fetch each official detail page (much slower)
.\.venv\Scripts\python.exe infopark_job_collector.py --include-details
```

The standard run throttles requests to at least one second apart, retries transient failures up to three times, respects HTTP `429 Retry-After`, and requests only listing/detail pages. Useful controls are `--delay`, `--retries`, `--timeout`, and `--max-pages`.

## How completeness is checked

The collector verifies the `#job-list table` and named source headers before accepting a page. It derives the highest displayed number from the live pagination markup rather than assuming a fixed number of pages. It fetches every expected page, checks the terminal page has no next link, and uses a bounded sequential fallback if the visible pagination expands. A run is **complete** only if every expected page was attempted successfully and the terminal page was verified. Any known failure produces a partial timestamped snapshot; it does not replace the last verified primary dataset.

## Extracted fields and duplicates

The primary fields are `job_id`, job title, company, original posting/deadline text, canonical official detail URL, source page, timestamp, `my_decision`, and `notes`. The portal's final numeric detail-path component is used as `job_id` only for the verified `/company-jobs/details/<company>/<job-id>` URL pattern. Deduplication is by canonical official detail URL, never by a similar title or company.

`--include-details` adds the visible detail text and an external application URL when available. A detail failure is recorded but never removes a listing.

## Output layout

All data stays in `data/infopark/`:

- `infopark_all_jobs.csv` — latest fully verified dataset, Excel-friendly UTF-8 CSV.
- `infopark_all_jobs.json` — same verified dataset as UTF-8 JSON.
- `infopark_jobs_review.xlsx` — **All Jobs** sheet with filters, frozen header, editable notes, and an Apply/Review/Skip dropdown; **Instructions** sheet explains review.
- `raw/` — immutable timestamped successful or partial snapshots, plus a workbook backup before each safe refresh.
- `reports/infopark_collection_report.json` — coverage, pagination, warning, failure, and integrity counts.
- `reports/infopark_failed_pages.json` — failures used by `--retry-failed`.
- `logs/infopark_collector.log` — operational log without credentials, cookies, or environment values.

## Manual decisions are protected

Before refreshing the review workbook, the collector reads `my_decision` and `notes` from the current CSV and workbook, matches jobs by verified job ID (falling back to canonical detail URL), and carries these values forward. A backup of an existing workbook is retained in `raw/` before replacement. New vacancies begin blank. Jobs not present in a current verified collection are listed as `listings_disappeared_from_current_portal` in the report and remain in historical snapshots; their disappearance is not labelled as closure.

## Troubleshooting and limitations

- Run `--discover-pages` first if the portal has changed. A missing listing table or unexpected source headers is treated as an error, not as an empty job list.
- If a run is partial, inspect `reports/infopark_collection_report.json`, then run `--retry-failed`. The primary CSV/JSON/XLSX will remain unchanged until complete collection is verified.
- A persistent access denial, CAPTCHA, or authentication requirement is reported; the collector does not bypass it.
- The portal can change structure at any time. Unit tests use a captured live listing fixture plus synthetic malformed examples, but a new portal design may need parser updates.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The tests cover current table parsing, pagination discovery, malformed/missing tables, canonical duplicate handling, failed requests, safe partial runs, CSV/JSON/XLSX creation, and manual-decision preservation.
