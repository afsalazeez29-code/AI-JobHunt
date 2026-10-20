# Cover Letter Maker

Generate local, company-specific PDF cover letters from the unchanged LaTeX master in Naga_Cover_Letter_Package.

## Manual multiple-application workflow

From this folder, run:

    py -3 scripts\generate_cover_letters.py --interactive

Enter a custom output-folder name such as October_Applications, then enter each application's short company name, full company name, job role, date, and optional local resume-PDF path. Review the list and type y to generate it.

company_name controls the output folder and filenames. company_full_name remains in the cover-letter content.

## JSON workflow

Edit data\applications.json, then run:

    py -3 scripts\generate_cover_letters.py --input data\applications.json --batch-name October_Applications

Use a different custom --batch-name for every batch. The generator never overwrites an existing output folder.

## Validate without output

    py -3 scripts\generate_cover_letters.py --input data\applications.json --batch-name October_Applications --dry-run

Generated files are saved under output\<custom-folder>\<company_name>\. Each successful company folder contains <company_name>_CL.tex, <company_name>_CL.pdf, and Resume.pdf only when a valid local resume PDF was supplied.

Open a completed batch in Windows File Explorer:

    explorer output\October_Applications
