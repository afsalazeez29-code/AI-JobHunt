# Infopark company-directory scraper — Stage 1

This scraper uses only the public Infopark Companies directory:

`https://infopark.in/companies`

Run the diagnostic before a collection when you want to inspect the current
pagination and card counts without changing output:

```powershell
python scraper.py --diagnose
```

Run the Stage 1 collector:

```powershell
python scraper.py
```

The official directory exposes normal `GET` pagination through `ul.pagination`
links using the `page` query parameter. The scraper discovers those links from
the source HTML; it does not assume a page count or construct company data.

`infopark_companies.csv` is UTF-8 with BOM and contains:

- `company_name`
- `phone`
- `website`
- `domain`
- `infopark_profile_url`
- `infopark_job_url`
- `source_url`
- `location`

Only card-provided values are recorded. The scraper does not request company
profiles, job-opening pages, company websites, or any third-party sources.
It uses atomic output checkpoints after each processed directory page. Existing
compatible output is preserved if a run is interrupted, and `errors.csv` is
created only when a real request or parsing error occurs.

## Stage 1.1: offline company classification

Stage 1.1 reads the frozen `infopark_companies.csv` locally and makes no
network requests. It creates a complete, classification-augmented dataset and
a separate human-review queue:

```powershell
python classify_companies.py
```

The output `infopark_companies_classified.csv` preserves every Stage 1 column
unchanged, then appends controlled relevance, target-role, priority, and
outreach-angle fields. `infopark_software_review.csv` contains only records
whose available directory domain information is insufficient or ambiguous for
a developer-relevance decision. The script does not use company names as a
technology signal and never follows profile, job, or website URLs.

## Stage 1.2 — Software Target Review

Stage 1.2 reviews all 401 saved Stage 1.1 records—not just the earlier review
queue—to create an auditable, final software-job target pool. It uses only the
local `infopark_companies.csv`, `infopark_companies_classified.csv`, and
`infopark_software_review.csv` files.

```powershell
python review_software_targets.py
```

The review assigns each company one final value: `High`, `Medium`, or
`Excluded`. Explicit software/application-development evidence remains High.
Technology-adjacent or insufficient evidence remains Medium for later human
review; a blank domain is not a reason to exclude a company. Exclusions are
limited to records whose stated domain clearly indicates non-software work.

Outputs are:

- `infopark_stage1_2_review_audit.csv` — all 401 decisions and their rationale.
- `infopark_final_targets.csv` — High and Medium targets only; the frozen Stage
  2 input after validation.
- `infopark_final_exclusions.csv` — excluded records and their audit rationale.

The validated current result contains 70 High targets, 324 Medium targets, and
7 exclusions (394 final targets). Stage 1.2 uses only previously collected
Infopark directory/classification data. No external websites, company profiles,
job pages, search engines, LinkedIn, or third-party sources are accessed.

## Stage 2 — Public contact and email discovery

Stage 2 uses the frozen 394-row `infopark_final_targets.csv` as its only
target input. It preserves every target field unchanged and checks each
company's public website first, following at most one normal same-site careers,
recruitment, contact, about, or team link. If no eligible functional inbox is
published there, it uses the official Infopark company profile as a fallback.
It does not use job-vacancy data, logins, CAPTCHA bypasses, email guessing,
email verification, or personal/named inboxes.

```powershell
python discover_public_contacts.py
```

The job is resumable and writes checkpointed outputs after each company. It
uses unique temporary checkpoint names to avoid OneDrive synchronization races.
Run without `--force` to continue an interrupted job; use `--limit N` only for
a deliberately bounded checkpoint test.

Outputs are:

- `infopark_stage2_contacts.csv` — every target has a record; each published
  functional business email has its exact source-page URL and provenance.
- `infopark_stage2_company_status.csv` — one research status per target.
- `infopark_stage2_audit.csv` — one audit row per target.
- `infopark_stage2_errors.csv` — public-source access errors encountered during
  research; it is an audit log, not a list of excluded targets.

The completed run covers all 394 targets: 313 companies have one or more
published functional business emails (419 sourced email records; 59 companies
have multiple), 81 have no eligible public email found, and none failed
research. All sourced email rows have a source URL and source metadata.
