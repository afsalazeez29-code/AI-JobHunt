# Kerala job matching engine

`kerala_job_matching_engine.py` is a separate, deterministic shortlist generator. It does not collect jobs, modify either portal dataset, apply for jobs, or infer qualifications/employment history. It reads the existing complete source files, classifies only potentially relevant junior web/software opportunities, and writes its results under `data/job_matching/`.

## Sources and discovery

By default the engine discovers:

- `data/technopark/technopark_all_jobs.json` — the collector's `{collection_metadata, jobs}` structure.
- `data/infopark/infopark_all_jobs.json` — the Infopark collector's list of records.

Use `--technopark-source PATH` and `--infopark-source PATH` when an alternate JSON snapshot is intentional. A missing or malformed source makes the run `PARTIAL` (or `FAILED` if neither can load); it is never reported as a complete two-portal analysis.

## Candidate profile and matching

The built-in profile is **Afsal A Azeez project evidence v1**. Primary roles are frontend, React, Next.js, JavaScript, TypeScript, web, full-stack, and MERN development. Related roles include junior software/application/Node/Express/UI development. Python, AI application, UI/UX implementation, cloud-development, and graduate-trainee roles are conditional. Senior/lead/architect listings are deprioritized for Manual Review unless the source explicitly states an incompatible mandatory requirement; a title alone is not proof of ineligibility.

The explicit alias configuration at the top of the script maps forms such as ReactJS → React, NextJS → Next.js, NodeJS → Node.js, Express → Express.js, Mongo → MongoDB, and Postgres → PostgreSQL. The project-evidence notes are intentionally limited to Recipe.IO, JailMeet 2.0, and HUE.ai as supplied. They are not treated as professional employment or proof of a degree.

The configured scoring weights are Role 25, Technical 30, Experience 15, Project 15, Education 10, and Practical Constraints 5 (total 100). Strong is 75+ with enough detailed evidence and no conflict; Related is 55–74 with detailed evidence; otherwise promising but incomplete roles become Manual Review. Clearly unrelated roles are excluded from the main shortlist.

Required skills are only recognised from source wording such as “required”, “must have”, or “mandatory”; “preferred”, “nice to have”, and “bonus” remain separate. Experience and education are `Appears Eligible`, `Needs Verification`, or `Not Specified`; no missing field is treated as a completed credential.

## Evidence, deadlines, and current source limitation

Evidence Coverage records whether title, description, requirement skills, experience, and education information were actually available. `Title-Based` results are low confidence and cannot become a Strong Match merely because the title looks attractive. `Mixed` is used when a description is available.

Closing dates are parsed from the source and evaluated in the Asia/Kolkata timezone. `Closing Soon` means 0–3 days remaining; earlier dates are `Expired`, later dates are `Open`, and unparsable/missing dates are `Unknown`. Expired relevant jobs remain available in the clearly labelled **Expired - Past Deadline** worksheet.

## Outputs and review preservation

The engine writes:

- `data/job_matching/kerala_jobs_resume_matched.xlsx`
- `data/job_matching/kerala_jobs_resume_matched.csv`
- `data/job_matching/kerala_jobs_resume_matched.json`
- `data/job_matching/reports/job_matching_report.json`
- `data/job_matching/review_state.json`

The workbook contains Strong Matches, Related Matches, Manual Review, Expired - Past Deadline, All Shortlisted Jobs, and Summary. It has filters, frozen header rows, wrapped content, hyperlink cells where the source supplied a verified URL, deadline/classification formatting, and the `Not Reviewed` / `Apply` / `Review` / `Skip` / `Applied` dropdown.

Before refresh, the engine backs up the workbook in `data/job_matching/review_backups/`, reads Review Status and Notes by `Source Portal + Original Job ID`, and merges those choices into `review_state.json`. The state file retains review values for jobs no longer in the current shortlist, so they can reconnect if a posting returns. New jobs start as Not Reviewed. No title/company-only transfer occurs.

JSON retains `original_source_record`; CSV is a deliberately flat shortlist. The report records source counts, exclusions, possible cross-source duplicates (flagged but never merged), source/eligibility limitations, classifications, date status, outputs, and validation results.

## Run and validate

```powershell
cd "C:\Users\afsal\OneDrive\Desktop\AI JobHunt\JoB-Weekly-Hunt"
.\.venv\Scripts\python.exe kerala_job_matching_engine.py
.\.venv\Scripts\python.exe kerala_job_matching_engine.py --help
.\.venv\Scripts\python.exe -m pytest -q
```

Each production run reopens JSON, CSV, and the workbook, checking shortlist counts, required worksheets, filters, frozen pane, and review validation. The tests cover both schema loaders, missing-field-safe title matching, aliases, required vs preferred skills, score/conflict behavior, evidence coverage, deadline handling, cross-source duplicate flagging, and workbook review preservation.

Inspect `job_matching_report.json` after each run. In particular, review `execution_status`, input source paths, `records_without_descriptions`, `title_based_assessments`, eligibility uncertainty, and validation. Descriptions are limited to what the collectors provide; running Infopark with its optional detail collection in the future can produce richer source evidence, but this engine does not scrape additional pages itself.
