# KSUM startup-directory scraper

This Stage 1A scraper collects publicly accessible company-list information from
the Kerala Startup Mission (KSUM) startup directory. It only collects the
company name, location, KSUM profile URL, and source page.

## Requirements

- Python 3.11+
- `requests`
- `beautifulsoup4`

Install the packages:

```powershell
pip install requests beautifulsoup4
```

## Initial three-page test

Run the initial test from this folder:

```powershell
python scraper.py
```

It makes sequential requests for pages 1, 2, and 3, with a one-second polite
delay between requests. The output is created as `ksum_test.csv` in this folder.
The script refuses to overwrite an existing CSV; rename, move, or remove it
before rerunning.

## Full collection

After reviewing the test CSV, collect every available directory page with:

```powershell
python scraper.py --all
```

This creates `ksum_companies.csv` in this folder. It reads KSUM's rendered
pagination state, stops on an empty page, and includes a maximum-page safety
guard.

## CSV columns

- `id`: sequential identifier assigned after URL-based deduplication.
- `company_name`: company name displayed on the KSUM directory card.
- `location`: location displayed on the KSUM directory card.
- `ksum_url`: public KSUM startup profile URL; used as the unique key.
- `source_page`: KSUM directory page number where the record was found.

The scraper uses ordinary public HTTP GET requests, a descriptive User-Agent,
and sequential polite request delays. It does not collect contact information,
emails, LinkedIn profiles, or company-profile details.

## Stage 1B — KSUM profile enrichment

Run the five-company enrichment test from this folder:

```powershell
python enrich_profiles.py
```

It reads only the first five records in `ksum_companies.csv` and visits only
their public KSUM profile URLs. It writes `ksum_enrichment_test.csv` in this
folder, preserving the Stage 1A company details and adding publicly displayed
KSUM profile fields: website, sector, industry, technology, business model,
and founders when labelled by KSUM. `industry` is included because KSUM
displays it as a structured startup-identification field.

After the test output has been reviewed, start or resume the full enrichment:

```powershell
python enrich_profiles.py --all
```

This creates `ksum_companies_enriched.csv`. It uses that file as a checkpoint:
after every successful profile, it atomically saves the complete successful
record set. A later `--all` run skips every KSUM profile URL already in that
file and requests only remaining URLs. Failed profiles are not treated as
complete, so they can be retried on a future run. If failures occur, their
details are written to `ksum_enrichment_errors.csv`.

It does not collect emails, LinkedIn data, careers information, contact-page
information, or data from external websites. As with the Stage 1A CSVs, it
uses sequential requests with a polite delay. The five-company test output is
never silently overwritten; the full-run checkpoint is safely updated in place
only after each successful profile is saved.
