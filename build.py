#!/usr/bin/env python3
"""
CV builder — assembles content blocks selected by a profile YAML,
renders to HTML via pandoc, then prints to PDF via Chrome headless.

By default a profile produces both DE and EN outputs.
Force a single language with --lang de  or  --lang en.

Usage:
    python build.py profiles/onepager-modern.yaml
    python build.py profiles/onepager-modern.yaml --lang de
    python build.py profiles/onepager-modern.yaml --html-only
    python build.py profiles/onepager-modern.yaml --lang en output.pdf
    python build.py --all                   # build every profile in profiles/
    python build.py --all --html-only
    python build.py --all --lang de
"""

import shutil
import sys
import re
import subprocess
from datetime import date
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
HTML_DIR = OUTPUT_DIR / "html"
PDF_DIR = OUTPUT_DIR / "pdf"

SECTION_LABELS = {
    "personal":                {"de": "Persönliche Informationen", "en": "Personal Information"},
    "summary":                   {"de": "Executive Profil",                                    "en": "Executive Profile"},
    "core-competencies":         {"de": "Kernkompetenzen",                                       "en": "Core Competencies"},
    "core-competencies-short":   {"de": "Kernkompetenzen",                                       "en": "Core Competencies"},
    "executive-competencies":    {"de": "Strategische Führungskompetenzen auf Executive-Level",  "en": "Leadership Competencies at Executive Level"},
    "experience":              {"de": "Berufstätigkeit",           "en": "Work Experience"},
    "earlier-positions":       {"de": "Frühere Positionen",         "en": "Earlier Positions"},
    "education":               {"de": "Studium",                   "en": "Education"},
    "skills":                  {"de": "Kenntnisse",                "en": "Skills"},
    "certifications":          {"de": "Zertifizierungen",          "en": "Certifications"},
    "projects":                {"de": "Projekte",                  "en": "Projects"},
    "teaching":                {"de": "Lehre",                     "en": "Teaching"},
    "publications":            {"de": "Publikationen",             "en": "Publications"},
    "zivildienst":             {"de": "Zivildienst",               "en": "Community Service"},
}

SINGLE_FILE_SECTIONS = {
    "personal", "certifications", "teaching", "publications", "zivildienst",
    "summary", "core-competencies", "core-competencies-short", "executive-competencies",
    "earlier-positions",
}

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium-browser",
    "chromium",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        p = Path(c)
        if p.exists():
            return str(p)
        found = shutil.which(c)
        if found:
            return found
    sys.exit("Chrome/Chromium not found. Install Google Chrome.")


def extract_lang_section(text: str, lang: str) -> str:
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    pattern = rf"^## {re.escape(lang)}\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, body, re.DOTALL | re.MULTILINE)
    if m:
        return m.group(1).strip()
    # For variant keys like "de-short", fall back to base lang, then to "de"
    if "-" in lang:
        base = lang.split("-")[0]
        m = re.search(rf"^## {re.escape(base)}\n(.*?)(?=^## |\Z)", body, re.DOTALL | re.MULTILINE)
        if m:
            return m.group(1).strip()
    if not lang.startswith("de"):
        m = re.search(r"^## de\n(.*?)(?=^## |\Z)", body, re.DOTALL | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return body.strip()


def frontmatter_field(path: Path, field: str) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return ""
    try:
        fm = yaml.safe_load(m.group(1))
        return str(fm.get(field, ""))
    except Exception:
        return ""


def resolve_files(section_type: str, include) -> list[Path]:
    if section_type in SINGLE_FILE_SECTIONS:
        candidate = CONTENT_DIR / f"{section_type}.md"
        return [candidate] if candidate.exists() else []

    subdir = CONTENT_DIR / section_type
    if not subdir.is_dir():
        candidate = CONTENT_DIR / f"{section_type}.md"
        return [candidate] if candidate.exists() else []

    if include == "all":
        files = list(subdir.glob("*.md"))
        files.sort(key=lambda p: frontmatter_field(p, "start"), reverse=True)
        return files
    if isinstance(include, list):
        files = []
        for name in include:
            p = subdir / f"{name}.md"
            if p.exists():
                files.append(p)
            else:
                print(f"  warning: {p} not found, skipping", file=sys.stderr)
        return files
    files = list(subdir.glob("*.md"))
    files.sort(key=lambda p: frontmatter_field(p, "start"), reverse=True)
    return files


def assemble(profile: dict, lang: str) -> str:
    parts: list[str] = []
    compact_exp = profile.get("experience_compact", False)
    label_overrides = profile.get("section_label_overrides", {})

    for section in profile.get("sections", []):
        if isinstance(section, str):
            section_type = section
            include = "all"
        else:
            section_type = next(iter(section))
            cfg = section[section_type]
            include = cfg.get("include", "all") if isinstance(cfg, dict) else "all"

        override = label_overrides.get(section_type)
        if override:
            label = override.get(lang, section_type.title()) if isinstance(override, dict) else str(override)
        else:
            base_type = section_type.split("-")[0]
            label = (SECTION_LABELS.get(section_type) or SECTION_LABELS.get(base_type, {})).get(lang, section_type.title())
        parts.append(f"\n## {label}\n")

        extract_lang = f"{lang}-short" if (compact_exp and section_type == "experience") else lang
        for f in resolve_files(section_type, include):
            content = extract_lang_section(f.read_text(encoding="utf-8"), extract_lang)
            if content:
                parts.append(content + "\n")

    return "\n".join(parts)


def resolve_variable(profile: dict, key: str, lang: str, default: str = "") -> str:
    """Return a profile variable, supporting lang-keyed dicts."""
    val = profile.get(key, default)
    if isinstance(val, dict):
        return val.get(lang, val.get("de", default))
    return str(val) if val else default


def render_html(markdown: str, profile: dict, lang: str, html_path: Path) -> None:
    title   = resolve_variable(profile, "name",     lang, "Dr. Tobias Griebe")
    subtitle = resolve_variable(profile, "subtitle", lang)
    contact  = resolve_variable(profile, "contact",  lang)
    photo_raw = resolve_variable(profile, "photo", lang)
    photo    = str((BASE_DIR / photo_raw).resolve()) if photo_raw else ""
    compact  = profile.get("compact", False)
    template_name = profile.get("template", "cv.html")

    template = TEMPLATES_DIR / template_name
    if not template.exists():
        sys.exit(f"HTML template not found: {template}")

    HTML_DIR.mkdir(parents=True, exist_ok=True)
    tmp_md = BASE_DIR / f"_assembled-{lang}.md"
    tmp_md.write_text(markdown, encoding="utf-8")

    cmd = [
        "pandoc",
        str(tmp_md),
        "--to=html5",
        f"--template={template}",
        "--standalone",
        f"--variable=title:{title}",
        f"--variable=lang:{lang}",
        "-o", str(html_path),
    ]
    if photo:
        cmd += [f"--variable=photo:{photo}"]
    if subtitle:
        cmd += [f"--variable=subtitle:{subtitle}"]
    if contact:
        cmd += [f"--variable=contact:{contact}"]
    if compact:
        cmd += ["--variable=compact:true"]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BASE_DIR))
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(f"pandoc failed (exit {result.returncode})")
    print(f"  HTML → output/html/{html_path.name}")


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()
    cmd = [
        chrome,
        "--headless=new",
        f"--print-to-pdf={pdf_path.resolve()}",
        "--no-pdf-header-footer",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"file://{html_path.resolve()}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(f"Chrome headless failed (exit {result.returncode})")
    print(f"  PDF  → output/pdf/{pdf_path.name}")


def determine_langs(profile: dict, lang_override: Optional[str]) -> list[str]:
    if lang_override:
        return [lang_override]
    lang = profile.get("lang", "both")
    if lang in ("de", "en"):
        return [lang]
    return ["de", "en"]


def build(
    profile_path: Path,
    output_path: Optional[Path] = None,
    html_only: bool = False,
    lang_override: Optional[str] = None,
) -> None:
    print(f"Profile: {profile_path.name}")
    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    langs = determine_langs(profile, lang_override)
    stem = profile_path.stem

    today = date.today().strftime("%Y-%m-%d")

    for lang in langs:
        markdown = assemble(profile, lang)
        if output_path and len(langs) == 1:
            pdf_path = output_path
            html_path = HTML_DIR / f"{output_path.stem}.html"
            latest_path = None
        else:
            base = f"{stem}-{lang}"
            pdf_path = PDF_DIR / f"{base}_{today}.pdf"
            html_path = HTML_DIR / f"{base}.html"
            latest_path = PDF_DIR / f"{base}_latest.pdf"

        render_html(markdown, profile, lang, html_path)
        if not html_only:
            render_pdf(html_path, pdf_path)
            if latest_path:
                shutil.copy2(pdf_path, latest_path)
                print(f"  copy → output/pdf/{latest_path.name}")

    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    html_only_flag = "--html-only" in sys.argv
    lang_flag = None
    for i, a in enumerate(sys.argv[1:], 1):
        if a == "--lang" and i + 1 < len(sys.argv):
            lang_flag = sys.argv[i + 1]

    if sys.argv[1] == "--all":
        profiles = sorted((BASE_DIR / "profiles").glob("*.yaml"))
        for p in profiles:
            build(p, html_only=html_only_flag, lang_override=lang_flag)
        sys.exit(0)

    profile_arg = Path(sys.argv[1])
    if not profile_arg.exists():
        profile_arg = BASE_DIR / "profiles" / sys.argv[1]

    output_arg = None
    for i, a in enumerate(sys.argv[2:], 2):
        if not a.startswith("--") and a not in ("de", "en"):
            output_arg = Path(a)

    build(profile_arg, output_arg, html_only=html_only_flag, lang_override=lang_flag)
