"""Generate local, company-specific cover letters from the existing LaTeX master.

This program never contacts external services, sends messages, or changes the
master template/class files.  It creates a fresh working TeX copy per valid
application record and compiles it only when a local LaTeX compiler is present.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = PROJECT_ROOT / "Naga_Cover_Letter_Package"
MASTER_TEMPLATE = PACKAGE_DIR / "coverletter-template.tex"
MASTER_CLASS = PACKAGE_DIR / "coverletter-clss.cls"
OUTPUT_ROOT = PROJECT_ROOT / "output"

REQUIRED_FIELDS = ("company_full_name", "company_name", "job_role", "date")
PLACEHOLDERS = (
    '"JOB-ROLE"',
    '"DATE"',
    '"COMPANY-FULL-NAME"',
    '"COMPANY NAME"',
)
LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


@dataclass
class Application:
    index: int
    company_full_name: str
    company_name: str
    job_role: str
    date: str
    resume_path: str = ""


@dataclass
class Result:
    index: int
    company_full_name: str
    job_role: str
    valid: bool
    output_folder: str = ""
    pdf_generated: bool = False
    resume_copied: bool = False
    resume_issue: str = ""
    compilation_error: str = ""
    unresolved_placeholders: list[str] = field(default_factory=list)
    page_count: int | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class GeneratorError(RuntimeError):
    """Raised for errors that should produce a clear batch result."""


def latex_escape(value: str) -> str:
    """Escape user-provided display text without modifying template commands/URLs."""
    return "".join(LATEX_ESCAPES.get(character, character) for character in value)


def normalized_company_part(value: str) -> str:
    """Return a safe, readable folder/file stem derived only from company_name."""
    normalized = re.sub(r"\s+", " ", value.strip())
    if not normalized:
        raise GeneratorError("company_name cannot be blank.")
    if len(normalized) > 72:
        raise GeneratorError("company_name is too long for a safe output folder name.")
    if (
        normalized in {".", ".."}
        or normalized.endswith((" ", "."))
        or re.search(r'[<>:"/\\|?*\x00-\x1f]', normalized)
    ):
        raise GeneratorError(
            f"company_name {value!r} cannot be used safely as a Windows folder/file name."
        )
    return normalized


def validate_batch_name(value: str | None) -> str:
    """Require a user-chosen, single safe output-directory component."""
    if value is None or not value.strip():
        raise GeneratorError(
            "Choose a custom output folder with --batch-name, or use --interactive."
        )
    name = value.strip()
    if (
        name in {".", ".."}
        or len(name) > 100
        or name.endswith((" ", "."))
        or re.search(r'[<>:"/\\|?*\x00-\x1f]', name)
    ):
        raise GeneratorError(
            "Output folder name must be one safe Windows folder name, without path separators."
        )
    return name


def is_google_drive_url(value: str) -> bool:
    lowered = value.strip().casefold()
    return "drive.google.com" in lowered or "docs.google.com" in lowered


def validate_pdf(path: Path) -> bool:
    try:
        return path.is_file() and path.stat().st_size > 4 and path.read_bytes()[:4] == b"%PDF"
    except OSError:
        return False


def local_latex_engine() -> tuple[str, str] | None:
    pdflatex = shutil.which("pdflatex")
    if pdflatex:
        return ("pdflatex", pdflatex)
    latexmk = shutil.which("latexmk")
    if latexmk:
        return ("latexmk", latexmk)
    return None


def read_master_template() -> str:
    if not MASTER_TEMPLATE.is_file():
        raise GeneratorError(f"Master template is missing: {MASTER_TEMPLATE}")
    if not MASTER_CLASS.is_file():
        raise GeneratorError(f"Master class file is missing: {MASTER_CLASS}")
    template = MASTER_TEMPLATE.read_text(encoding="utf-8")
    required_commands = (
        r"\clname", r"\clrole", r"\clcontact", r"\cldate", r"\clsubject",
        r"\clrecipient", r"\makecoverletterhead", r"\makecoverletterdetails",
    )
    missing = [command for command in required_commands if command not in template]
    if missing:
        raise GeneratorError(f"Master template lacks required commands: {', '.join(missing)}")
    if r"\documentclass{resume}" not in template:
        raise GeneratorError(
            "Expected document class declaration '\\documentclass{resume}' was not found. "
            "Review the template/class compatibility before generating."
        )
    class_text = MASTER_CLASS.read_text(encoding="utf-8")
    if r"\ProvidesClass{coverletter}" not in class_text:
        raise GeneratorError(
            "The supplied coverletter-clss.cls does not declare the coverletter class."
        )
    return template


def load_applications(input_path: Path) -> tuple[list[Application], list[Result]]:
    try:
        raw = json.loads(input_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise GeneratorError(f"Input JSON does not exist: {input_path}") from error
    except json.JSONDecodeError as error:
        raise GeneratorError(f"Input JSON is invalid: {error}") from error
    if not isinstance(raw, dict) or not isinstance(raw.get("applications"), list):
        raise GeneratorError('Input JSON must contain an "applications" array.')

    applications: list[Application] = []
    invalid: list[Result] = []
    for index, item in enumerate(raw["applications"], start=1):
        result = Result(index=index, company_full_name="", job_role="", valid=False)
        if not isinstance(item, dict):
            result.errors.append("Record must be a JSON object.")
            invalid.append(result)
            continue
        values: dict[str, str] = {}
        for field_name in REQUIRED_FIELDS:
            value = item.get(field_name, "")
            if not isinstance(value, str) or not value.strip():
                result.errors.append(f'Missing required non-empty field: "{field_name}".')
            else:
                values[field_name] = value.strip()
        result.company_full_name = values.get("company_full_name", "")
        result.job_role = values.get("job_role", "")
        resume_path = item.get("resume_path", "")
        if resume_path is None:
            resume_path = ""
        if not isinstance(resume_path, str):
            result.errors.append('"resume_path" must be a string when provided.')
            resume_path = ""
        if result.errors:
            invalid.append(result)
            continue
        applications.append(
            Application(
                index=index,
                company_full_name=values["company_full_name"],
                company_name=values["company_name"],
                job_role=values["job_role"],
                date=values["date"],
                resume_path=resume_path.strip(),
            )
        )
    return applications, invalid


def make_tex(template: str, application: Application) -> tuple[str, list[str]]:
    """Replace only the four quoted placeholder tokens in a fresh template copy."""
    values = {
        '"JOB-ROLE"': latex_escape(application.job_role),
        '"DATE"': latex_escape(application.date),
        '"COMPANY-FULL-NAME"': latex_escape(application.company_full_name),
        '"COMPANY NAME"': latex_escape(application.company_name),
    }
    output = template
    for placeholder, value in values.items():
        output = output.replace(placeholder, value)

    # The master references resume.cls, while its supplied class declares
    # coverletter.  Only generated working copies receive this correction.
    output = output.replace(r"\documentclass{resume}", r"\documentclass{coverletter}", 1)
    unresolved = [placeholder for placeholder in PLACEHOLDERS if placeholder in output]
    return output, unresolved


def inspect_resume(application: Application) -> tuple[Path | None, str]:
    if not application.resume_path:
        return None, ""
    if is_google_drive_url(application.resume_path):
        return None, (
            "Google Drive links are not supported. Download the resume manually "
            "and provide its local PDF path."
        )
    path = Path(application.resume_path).expanduser()
    if not path.is_absolute():
        return None, "Resume path must be an absolute local path."
    if not path.is_file():
        return None, f"Resume file does not exist: {path}"
    if not validate_pdf(path):
        return None, f"Resume is not a readable PDF: {path}"
    return path, ""


def compile_pdf(tex_path: Path, build_dir: Path) -> tuple[Path | None, str]:
    engine = local_latex_engine()
    if engine is None:
        return None, (
            "No local LaTeX compiler was found. Install MiKTeX or TeX Live, ensure "
            "latexmk or pdflatex is on PATH, then rerun this batch."
        )
    engine_name, executable = engine
    build_dir.mkdir(parents=True, exist_ok=True)
    working_tex = build_dir / "Cover_Letter.tex"
    working_class = build_dir / "coverletter.cls"
    shutil.copy2(tex_path, working_tex)
    shutil.copy2(MASTER_CLASS, working_class)
    if engine_name == "latexmk":
        command = [
            executable, "-pdf", "-interaction=nonstopmode", "-halt-on-error",
            "-outdir=" + str(build_dir), str(working_tex),
        ]
        passes = 1
    else:
        command = [
            executable, "-interaction=nonstopmode", "-halt-on-error",
            "-output-directory=" + str(build_dir), str(working_tex),
        ]
        passes = 2
    messages: list[str] = []
    for _ in range(passes):
        completed = subprocess.run(
            command,
            cwd=build_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        messages.append((completed.stdout + "\n" + completed.stderr).strip())
        if completed.returncode != 0:
            log_path = build_dir / "Cover_Letter.log"
            if log_path.is_file():
                messages.append(log_path.read_text(encoding="utf-8", errors="replace"))
            diagnostic = "\n".join(messages)[-4000:]
            return None, f"{engine_name} failed:\n{diagnostic}"
    pdf_path = build_dir / "Cover_Letter.pdf"
    if not validate_pdf(pdf_path):
        return None, f"{engine_name} exited successfully but did not create a valid PDF."
    return pdf_path, ""


def page_count_if_available(pdf_path: Path) -> int | None:
    try:
        from pypdf import PdfReader  # type: ignore[import-not-found]
    except ImportError:
        return None
    try:
        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        return None


def write_reports(batch_dir: Path, summary: dict[str, Any]) -> None:
    (batch_dir / "generation_report.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "Cover Letter Generation Report",
        "=" * 30,
        f"Selected application records: {summary['selected_records']}",
        f"Valid records: {summary['valid_records']}",
        f"PDFs generated: {summary['pdfs_generated']}",
        f"PDF compilation failures: {summary['pdf_failures']}",
        f"Resumes copied: {summary['resumes_copied']}",
        f"Missing/invalid resumes: {summary['resume_issues']}",
        f"Unresolved placeholders: {summary['unresolved_placeholders']}",
        f"Multipage-PDF warnings: {summary['multipage_warnings']}",
        "",
    ]
    for result in summary["results"]:
        lines.append(
            f"[{result['index']}] {result['company_full_name'] or 'Invalid record'} "
            f"— PDF={result['pdf_generated']} — {result['output_folder']}"
        )
        for message in result["errors"] + result["warnings"]:
            lines.append(f"  - {message}")
        if result["resume_issue"]:
            lines.append(f"  - Resume: {result['resume_issue']}")
        if result["compilation_error"]:
            lines.append(f"  - Compilation: {result['compilation_error']}")
    (batch_dir / "generation_report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_zip(batch_dir: Path, results: list[Result]) -> Path:
    zip_path = batch_dir.with_suffix(".zip")
    if zip_path.exists():
        raise GeneratorError(f"Refusing to overwrite existing batch ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for result in results:
            if not result.pdf_generated or not result.output_folder:
                continue
            folder = Path(result.output_folder)
            for path in folder.iterdir():
                if path.is_file() and (
                    path.name == "Resume.pdf"
                    or path.name.endswith("_CL.tex")
                    or path.name.endswith("_CL.pdf")
                ):
                    archive.write(path, path.relative_to(batch_dir))
    return zip_path


def batch_directory(name: str | None) -> Path:
    requested = validate_batch_name(name)
    path = OUTPUT_ROOT / requested
    if path.exists():
        raise GeneratorError(
            f"Refusing to overwrite an existing batch: {path}. Choose --batch-name with a new value."
        )
    return path


def run_self_test() -> int:
    template = read_master_template()
    test = Application(
        index=1,
        company_full_name="A&B_#% Co.",
        company_name="A&B",
        job_role="C# Developer",
        date="21 October 2026",
    )
    generated, unresolved = make_tex(template, test)
    expected_fragments = (r"\documentclass{coverletter}", r"A\&B\_\#\% Co.", r"C\# Developer")
    if unresolved or any(fragment not in generated for fragment in expected_fragments):
        print("SELF-TEST: FAIL")
        return 1
    if r"\href{https://afzyl.vercel.app/}{Portfolio}" not in generated:
        print("SELF-TEST: FAIL (master hyperlink was not preserved)")
        return 1
    print("SELF-TEST: PASS")
    print("Verified placeholder replacement, LaTeX special-character escaping, class correction, and hyperlink preservation.")
    return 0


def validate_company_output_names(applications: list[Application]) -> dict[int, str]:
    """Prevent two records from resolving to the same company folder/file stem."""
    resolved: dict[int, str] = {}
    seen: dict[str, Application] = {}
    for application in applications:
        stem = normalized_company_part(application.company_name)
        key = stem.casefold()
        if key in seen:
            other = seen[key]
            raise GeneratorError(
                "Duplicate normalized company output name: "
                f"{other.company_name!r} (record {other.index}) and "
                f"{application.company_name!r} (record {application.index})."
            )
        seen[key] = application
        resolved[application.index] = stem
    return resolved


def collect_interactive_applications(batch_name: str | None) -> tuple[str, list[Application]]:
    """Collect a manually selected, reviewable batch without writing any files."""
    chosen_batch = batch_name or input("Output folder name: ").strip()
    validate_batch_name(chosen_batch)
    applications: list[Application] = []
    while True:
        number = len(applications) + 1
        print(f"\nCompany {number}")
        values: dict[str, str] = {}
        for field_name, prompt in (
            ("company_name", "Company name"),
            ("company_full_name", "Company full name"),
            ("job_role", "Job role"),
            ("date", "Date"),
        ):
            while not values.get(field_name):
                values[field_name] = input(f"{prompt}: ").strip()
                if not values[field_name]:
                    print(f"{prompt} is required.")
        resume_path = input("Resume PDF (optional local path): ").strip()
        applications.append(Application(index=number, resume_path=resume_path, **values))
        add_more = input("Add another application? [y/N]: ").strip().casefold()
        if add_more not in {"y", "yes"}:
            break
    print("\nReview")
    for application in applications:
        print(
            f"{application.index}. {application.company_name} | "
            f"{application.company_full_name} | {application.job_role} | {application.date}"
        )
    if input("Generate this batch? [y/N]: ").strip().casefold() not in {"y", "yes"}:
        raise GeneratorError("Generation cancelled before any files were created.")
    return chosen_batch, applications


def run_batch(
    applications: list[Application],
    invalid_results: list[Result],
    batch_name: str | None,
    dry_run: bool,
) -> int:
    template = read_master_template()
    selected = len(applications) + len(invalid_results)
    if not applications and not invalid_results:
        raise GeneratorError("No application records selected. Add records to the input JSON first.")
    if not applications:
        raise GeneratorError("No valid application records are available to generate.")
    output_names = validate_company_output_names(applications)
    engine = local_latex_engine()
    print("Compatibility correction for generated copies: resume -> coverletter; copied class: coverletter-clss.cls -> coverletter.cls.")
    print("LaTeX compiler:", f"{engine[0]} ({engine[1]})" if engine else "not found")
    print(f"Selected records: {selected}; valid records: {len(applications)}; invalid records: {len(invalid_results)}")

    prepared: list[tuple[Application, str, list[str], Path | None, str]] = []
    for application in applications:
        tex, unresolved = make_tex(template, application)
        resume, resume_issue = inspect_resume(application)
        prepared.append((application, tex, unresolved, resume, resume_issue))
        status = "PASS" if not unresolved else "FAIL"
        print(f"[{application.index}] {application.company_full_name}: placeholder check {status}")
        if resume_issue:
            print(f"  Resume warning: {resume_issue}")
    if dry_run:
        print("DRY RUN: no batch folder, TeX, PDF, resume copy, report, or ZIP was created.")
        return 0 if not invalid_results and all(not unresolved for _, _, unresolved, _, _ in prepared) else 1

    batch_dir = batch_directory(batch_name)
    batch_dir.mkdir(parents=True)
    results = list(invalid_results)
    for application, tex, unresolved, resume, resume_issue in prepared:
        company_stem = output_names[application.index]
        app_dir = batch_dir / company_stem
        app_dir.mkdir()
        tex_path = app_dir / f"{company_stem}_CL.tex"
        tex_path.write_text(tex, encoding="utf-8")
        result = Result(
            index=application.index,
            company_full_name=application.company_full_name,
            job_role=application.job_role,
            valid=True,
            output_folder=str(app_dir),
            unresolved_placeholders=unresolved,
            resume_issue=resume_issue,
        )
        if unresolved:
            result.errors.append("Generated TeX contains unresolved application placeholders.")
        else:
            compiled_pdf, compilation_error = compile_pdf(
                tex_path, batch_dir / ".build" / company_stem
            )
            if compiled_pdf:
                final_pdf = app_dir / f"{company_stem}_CL.pdf"
                shutil.copy2(compiled_pdf, final_pdf)
                result.pdf_generated = validate_pdf(final_pdf)
                result.page_count = page_count_if_available(final_pdf)
                if result.page_count and result.page_count > 1:
                    result.warnings.append(f"PDF has {result.page_count} pages; inspect the preserved layout.")
            else:
                result.compilation_error = compilation_error
        if resume:
            destination = app_dir / "Resume.pdf"
            try:
                shutil.copy2(resume, destination)
                result.resume_copied = validate_pdf(destination)
                if not result.resume_copied:
                    result.resume_issue = "Resume copy was created but failed PDF validation."
            except OSError as error:
                result.resume_issue = f"Could not copy resume: {error}"
        results.append(result)

    summary = {
        "selected_records": selected,
        "valid_records": len(applications),
        "pdfs_generated": sum(result.pdf_generated for result in results),
        "pdf_failures": sum(
            result.valid and not result.pdf_generated for result in results
        ),
        "resumes_copied": sum(result.resume_copied for result in results),
        "resume_issues": sum(bool(result.resume_issue) for result in results),
        "unresolved_placeholders": sum(bool(result.unresolved_placeholders) for result in results),
        "multipage_warnings": sum(
            bool(result.page_count and result.page_count > 1) for result in results
        ),
        "latex_engine": engine[0] if engine else None,
        "results": [asdict(result) for result in results],
    }
    write_reports(batch_dir, summary)
    successful = [result for result in results if result.pdf_generated]
    if successful:
        zip_path = make_zip(batch_dir, results)
        print(f"Created ZIP: {zip_path}")
    else:
        print("No ZIP created because no compiled PDF passed validation.")
    print(json.dumps({key: value for key, value in summary.items() if key != "results"}, indent=2))
    print(f"Open the completed batch in File Explorer: explorer \"{batch_dir}\"")
    return 0 if summary["pdf_failures"] == 0 and not invalid_results else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate local LaTeX cover letters from JSON.")
    parser.add_argument(
        "--input",
        default=str(PROJECT_ROOT / "data" / "applications.json"),
        help="Path to the application JSON file.",
    )
    parser.add_argument(
        "--batch-name",
        help="Required custom output folder name for JSON mode, e.g. October_Applications.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter a custom folder name and multiple application records manually.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate records and template without creating output.")
    parser.add_argument("--self-test", action="store_true", help="Run a no-output substitution and compatibility test.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.self_test:
            return run_self_test()
        if args.interactive:
            batch_name, applications = collect_interactive_applications(args.batch_name)
            return run_batch(applications, [], batch_name, args.dry_run)
        applications, invalid_results = load_applications(Path(args.input).expanduser())
        return run_batch(applications, invalid_results, args.batch_name, args.dry_run)
    except GeneratorError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
