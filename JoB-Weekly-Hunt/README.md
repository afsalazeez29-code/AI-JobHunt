# JobHunt fresh collection cycle

Restart baseline: 19 November 2026, Asia/Kolkata. Use the fresh entry points below; legacy collectors and keyword/profile definitions remain available for compatibility.

```powershell
cd "C:\Users\afsal\OneDrive\Desktop\AI JobHunt\JoB-Weekly-Hunt"
.\.venv\Scripts\python.exe refresh_jobhunt.py
# Independent portals
.\.venv\Scripts\python.exe technopark_fresh_scraper.py
.\.venv\Scripts\python.exe infopark_fresh_scraper.py
.\.venv\Scripts\python.exe -m pytest -q
```

The reset archived 105 generated files outside this project in `../_archives/`; see `data/run_metadata/reset_receipt.json` for the exact ZIP. The manifest contains paths, sizes, modification timestamps and SHA-256 values. ZIP CRC and every manifest checksum were verified before deleting only those exact allowlisted files. Code, tests, environment and dependencies were preserved. **Do not run reset_generated_data.py during ordinary refreshes**: it deliberately starts an empty review cycle.

Official listing sources are https://technopark.in/job-search (verified public paginated API) and https://infopark.in/companies-job (server-rendered table with dynamic pagination). Listing completeness is checked by the reused collectors; incomplete snapshots are archived and reported without replacing latest datasets. Each portal runs independently even if the other fails. Detail requests are sequential, paced by `--delay` (default 0.5 seconds), with timeouts and two transient retries respecting Retry-After. Cache reuse is confined to the same run ID; later runs revalidate details.

`data/technopark/` and `data/infopark/` hold latest listing JSON/CSV, original raw snapshots, enriched JSON, active JSON, separate uncertain/expired/closed files and reports. `data/matched_jobs/<portal>/` holds all candidates in JSON/CSV/Excel plus category workbooks and rejected CSV. The all-candidates view can contain expired or uncertain records, explicitly labelled; **active_jobs.json alone is the primary active vacancy dataset**. Missing deadlines never imply expiry. The `rejected_or_expired` view also includes technically irrelevant active records and uncertain status records; use its explicit status/category fields.

Status is derived from original deadlines and explicit closed wording, independently of recency. A valid deadline today or later supports open status; older postings remain active when their deadline supports it. Recency uses a 14-day window; NEWLY_POSTED specifically means the requested baseline date. Collection timestamps, verification timestamps, run IDs and source dates stay separate. Source modification dates remain null when unavailable.

The full existing title dictionary is imported unchanged. Matching uses title evidence (25), core profile skills (up to 35), development-duty excerpts (25), and junior wording (15). A strong technical match requires 75 points, full text, no recognised missing mandatory skills and no extracted minimum experience above one year. Missing descriptions get no numerical score and remain review candidates. Unrelated sales/marketing titles are excluded. Education and professional experience remain unverified; project work is not treated as employment. Required/preferred and eligibility extraction is deterministic and conservative, with original text/excerpts retained. Unrecognised technologies or phrasing may require manual review. Scores are priorities, not eligibility probabilities.

Review Status and Notes start empty/Not Reviewed for this cycle. Future runs read changes from all editable category workbooks, match by source ID within each portal, and retain removed jobs in review_state.json. Conflicting edits across views stop replacement with an explicit failure. Workbooks are backed up before refresh. Unreadable review state is never silently discarded.

`data/run_metadata/combined_summary.json` and `source_coverage_report.json` record counts and per-portal results; `current_run.json` identifies the last invocation. Portal completeness describes listing coverage; description failures are counted separately. JSON/CSV/Excel candidate counts are reopened and checked. Missing location/campus/application destinations remain null unless extracted; consult original descriptions for details not recognised by the structured parser.
