# Technopark and Infopark developer-job reinvestigation

`park_job_reinvestigation.py` is a separate, repeatable enrichment and high-recall matching stage. It reads the existing collector JSON snapshots without modifying them, requests only verified public job-detail URLs at a controlled sequential rate, caches successful descriptions, and writes independent Technopark and Infopark result folders under `data/matched_jobs/`.

## Run

```powershell
cd "C:\Users\afsal\OneDrive\Desktop\AI JobHunt\JoB-Weekly-Hunt"
.\.venv\Scripts\python.exe park_job_reinvestigation.py
.\.venv\Scripts\python.exe park_job_reinvestigation.py --delay 0.10
.\.venv\Scripts\python.exe -m pytest -q
```

`--delay` is the pause between non-cached public detail-page requests. Existing full, partial, and 404 cached responses are reused rather than fetched again. Source paths can be overridden with `--technopark-source` and `--infopark-source`.

## Matching method

The engine includes the complete title dictionary requested for software, frontend, React, Next.js, full-stack, backend, application, QA automation, database, intern, trainee, associate, graduate, and related development titles. It normalizes case, punctuation, hyphens, and whitespace while retaining word boundaries. Additional unfamiliar roles can qualify from their actual description when it contains relevant responsibility and technology signals.

It scores title evidence, demonstrated technical-skill overlap, development duties, junior/fresher wording, and full-description availability. It does not claim that a title alone proves suitability. Categories are Strong Match, Potential Match, Related Developer Role, Manual Review, Expired Relevant Role, and Not Relevant. A stated degree or significant professional-experience condition is `Needs Verification`; missing conditions are `Not Specified` rather than assumed met.

## Outputs

Each portal has a separate directory, containing every current candidate in its own `*_all_matched_jobs.xlsx`, CSV, and JSON, plus category workbooks, rejected-record CSV, description cache, review state, and reports. `cross_source_duplicate_candidates.json` flags title/company coincidences but never merges or deletes source postings.

Each record retains its source portal and ID, original title and URL, description retrieval status, requirements as stated/extracted, matched and missing skills, evidence, status, review state, and notes. The matched workbook freezes headers, filters rows, wraps long text, and has a Review Status dropdown. Existing portal review state is preserved, with compatible migration from the prior combined matching engine where a matching portal+source ID exists.

## Limitations

Descriptions are only as current as the official detail pages and cache. Missing, access-restricted, or failed pages remain explicitly marked; their listings can become Manual Review but are never fabricated into strong evidence. Matching is prioritization for human review, not a claim of employment, degree completion, or professional experience. The reports provide the source-count audit, category and enrichment counts, and failure reasons.
