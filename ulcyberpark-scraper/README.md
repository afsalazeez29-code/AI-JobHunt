# UL CyberPark Company Dataset - Internal Audit

Internal-only audit of `ulcyberpark-scraper`. Relevant files: `ulcyberpark_companies.csv`, `ulcyberpark_companies_1.csv`, and `scrape_ul_cyberpark.py` (read as text only). No README previously existed. The two CSVs have 42 rows each and are exact paired copies.

## Schema, counts, and methodology
CSV fields: `company_name`, `website`. Raw company-bearing records: 84; canonical companies: 42; confirmed duplicate groups: 42; duplicate records beyond canonical entries: 42; probable/possible/unresolved identity groups: 0. Each same-name, same-website row is a confirmed duplicate across the two files. No business description, service, industry, or leadership field is present, so IT/ITeS, software development, IT services, other technology, and non-IT classifications remain null for all 42. CEO, managing director, founder, email, phone, address, description, and services are null.

| # | Company | Website | IT/ITeS | Software development | CEO | Services | Sources / duplicate status |
|---:|---|---|---|---|---|---|---|
| 1 | Acodez IT Solutions | http://www.acodez.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 2 | Actionfi Technologies | http://www.actionfi.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 3 | Aerovative Technologies | http://www.aerovative.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 4 | AppSure Software Solutions Pvt. Ltd | http://www.appsure.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 5 | Asterbyte Software Systems Pvt Ltd | http://https://asterbyte.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 6 | Bititude Technologies | http://www.bititude.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 7 | BMS Estimating Private Limited | http://www.michaelsurfacesolutions.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 8 | Buchprufer Consultants LLP | http://www.Buchprufer.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 9 | Charles & Darwish Associates | http://www.cdaaudit.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 10 | Cherrylabs | http://www.cherrylabs.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 11 | Codesap Technologies LLP | http://www.codesap.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 12 | Direct Axis | http://www.directaxistech.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 13 | DM MED CITY HOSPITALS PVT LTD | http://www.asterdmhealthcare.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 14 | GRITSTONE Technologies | http://www.gritstone.io | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 15 | Hexeam Software Solutions | http://hexeam.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 16 | HyperBlox | http://www.hyperblox.io | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 17 | ICT Academy of Kerala | http://www.ictkerala.org | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 18 | ipsr solutions ltd | http://www.ipsrsolutions.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 19 | KAAF Logistics | http://www.kaaflogistics.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 20 | Kerala Startup Mission | http://www.startupmission.kerala.gov.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 21 | LENOK SOLUTIONS PRIVATE LIMITED | http://www.lenoksolutions.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 22 | Meridian Solutions Inc | http://www.meridian.net.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 23 | Mozilor Technologies | http://www.mozilor.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 24 | Netstager Technologies Pvt. Ltd | http://www.netstager.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 25 | nucore | http://www.nucore.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 26 | Oreolabs | http://https://oreolabs.com/ | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 27 | PlaySpots | http://www.playspots.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 28 | Proaims IoT Solutions | http://www.proaims.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 29 | QBURST | http://www.qburst.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 30 | retailcloud | http://www.retailcloud.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 31 | Rybbon Digital rewards India Private Limited | http://www.rybbon.net | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 32 | Sizcom Digital | http://www.sizcomdigital.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 33 | SKYBOOK | http://www.skybookglobal.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 34 | STACKROOTS TECHNOLOGY SOLUTIONS | http://www.stackroots.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 35 | Synosys | http://www.synosys.ae | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 36 | TATA Elxsi | http://www.tataelxsi.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 37 | Tech Tadd | http://www.techtadd.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 38 | Telestation Private Limited | http://www.ashtelgroup.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 39 | Tranetech Software Solutions | http://www.tranetech.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 40 | Trogon Media Pvt Ltd | http://www.trogonmedia.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 41 | UL TECHNOLOGY SOLUTION (P) LTD | http://www.ults.in | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |
| 42 | VIZRU | http://www.vizru.com | null | null | null | null | ulcyberpark_companies.csv; ulcyberpark_companies_1.csv; confirmed paired duplicate |

## Data quality, source-of-truth, and AI JobHunt guidance
The website values for Asterbyte Software Systems Pvt Ltd and Oreolabs are malformed (`http://https://...`) and must not be silently repaired. All other classification/leadership fields remain null because the local data does not establish them. Use one canonical row per paired record, retain both source filenames, preserve null as unknown, and do not infer business activity, vacancies, or current facts. Original CSVs and the scraper script remain the underlying evidence; no external verification was performed. Future authorized updates must recheck both CSVs, preserve originals, recalculate duplicate counts, and document unresolved conflicts.

