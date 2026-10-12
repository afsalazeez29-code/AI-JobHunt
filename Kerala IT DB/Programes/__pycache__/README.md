# Cyberpark company-list scraper — Stage 1

This scraper collects company-list data only from the official Cyberpark
Companies At Park directory:

`https://cyberparks.in/companies-at-park/`

Run it from this folder:

```powershell
python scraper.py
```

For selector verification without creating or changing a CSV:

```powershell
python scraper.py --test-only
```

For a read-only explanation of the request mechanism and card counts:

```powershell
python scraper.py --diagnose
```

## Data collected

`cyberpark_companies.csv` uses UTF-8 with BOM and contains these columns:

- `company_name`: name displayed on the official directory card.
- `website`: website href displayed in the card, if available.
- `cyberpark_listing_url`: Cyberpark `Details` listing URL present in the card,
  if available.
- `source_url`: the official Companies At Park directory URL.
- `location`: `Kozhikode, Kerala` for this directory.

The current directory page is server-rendered: the 7 October 2026 diagnostic
found 76 card bodies in the initial response and 75 valid named records. The
previous 19-row result came from a presentation-specific selector that required
the `fit` wrapper class; 57 valid cards use the otherwise equivalent
`grid col-300` wrapper without that class. No pagination or directory
load-more mechanism was present. The scraper still checks for official
pagination links and makes sequential, polite requests if they later appear.

## Safety and limits

Stage 1 collects only company-list data from the official Cyberpark Companies
At Park directory. Individual company listing pages are reserved for Stage 2.
The scraper records a card's listing URL but never requests it. It also never
visits company websites, searches external sources, or collects emails, phone
numbers, addresses, or personnel details. The directory's optional POST search
form is not used because the unfiltered full list is already present in the
initial GET response; no AJAX request is required.

Records are deduplicated first by listing URL and then by normalized company
name plus website. Existing compatible output is retained on reruns, and CSV
writes use a temporary file plus atomic replace. `errors.csv` is created only
when actual request, parsing, or conflicting-duplicate errors occur; a card
with no meaningful displayed company name is logged and skipped rather than
having a name inferred from its logo, URL, or website.

## Stage 2: listing enrichment and job-fit classification

Stage 2 reads the unchanged Stage 1 CSV and requests only its official
Cyberpark listing URLs. It creates `cyberpark_company_enriched.csv`, keeping
raw listing fields separate from derived job-hunting relevance fields.

```powershell
python enrich_companies.py
```

The enrichment script writes an atomic checkpoint after every listing, so a
later run resumes the remaining URLs without re-requesting completed records.
Use `--limit 3` for a small checkpoint test, or `--refresh` only when a
deliberate source refresh is required. It never requests company websites,
LinkedIn, search engines, or third-party directories.
