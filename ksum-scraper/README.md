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

## Stage 1C - Kerala software/IT target filter

Run the Stage 1C filter from this folder:

```powershell
python filter_targets.py
```

It reads `ksum_companies_enriched.csv` and creates
`ksum_kerala_software_it_targets.csv`. The master dataset is read only and is
never modified. The filter retains explicit Kerala locations and applies
explainable sector, industry, technology, and business-model signals to identify
companies that are plausible software/IT developer job targets. The output adds
`target_relevance` and `target_reason` after the preserved Stage 1B columns.

Stage 1C does not visit company websites, search the web, or collect contact,
email, LinkedIn, careers, or recruitment information.

## Stage 1C.1 - Medium-target review

Run the review from this folder:

```powershell
python review_medium_targets.py
```

It reviews only the Stage 1C rows marked `Medium`, using the existing local
KSUM CSV fields. It creates `ksum_kerala_software_it_targets_refined.csv` with
the preserved Stage 1C High records plus reviewed High and Medium records, and
`ksum_kerala_software_it_review.csv` with every Medium decision, including
excluded records and the factual reason. The Stage 1B master and Stage 1C source
CSV are read only and never modified. No external sources are accessed.

## Stage 1D - Final target audit and freeze

Run the final KSUM-data-only audit from this folder:

```powershell
python final_target_audit.py
```

It reads the Stage 1B master, Stage 1C target list, Stage 1C.1 refined list,
and Stage 1C.1 review audit without modifying them. It confirms the 57 current
Medium targets and 15 exclusions against their existing KSUM fields, then creates:

- `ksum_final_targets.csv`: frozen Stage 2 input, containing 457 High-priority
  (`A`) and 57 Medium-priority (`B`) targets.
- `ksum_final_target_audit.csv`: the 72 final Medium/Exclude audit decisions.
- `ksum_final_exclusions.csv`: the 15 permanently excluded companies and reasons.

The script validates unique profile URLs, valid KSUM URLs, priority values,
field preservation, no exclusion leakage, and unchanged reference datasets.
Stage 1 target selection is now frozen. Stage 2 will use
`ksum_final_targets.csv` as its authoritative input. No external website,
contact, email, LinkedIn, or careers-page research occurs in Stage 1D.
