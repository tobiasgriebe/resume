#!/usr/bin/env python3
"""
CV builder — assembles content blocks selected by a profile YAML and
renders to PDF via pandoc.

Usage:
    python build.py profiles/engineering-director-en.yaml
    python build.py profiles/engineering-director-en.yaml output.pdf
"""

import sys
import re
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = BASE_DIR / "templates"

SECTION_LABELS = {
    "personal":       {"de": "Persönliche Informationen", "en": "Personal Information"},
    "experience":     {"de": "Berufstätigkeit",           "en": "Work Experience"},
    "education":      {"de": "Studium",                   "en": "Education"},
    "skills":         {"de": "Kenntnisse",                "en": "Skills"},
    "certifications": {"de": "Zertifizierungen",          "en": "Certifications"},
    "projects":       {"de": "Projekte",                  "en": "Projects"},
    "teaching":       {"de": "Lehre",                     "en": "Teaching"},
    "publications":   {"de": "Publikationen",             "en": "Publications"},
}

SINGLE_FILE_SECTIONS = {"personal", "certifications", "teaching", "publications"}


def extract_lang_section(text: str, lang: str) -> str:
    """Return the body of the ## <lang> section, falling back to 'de'."""
    # Strip YAML frontmatter
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    # Try requested language
    pattern = rf"^## {re.escape(lang)}\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, body, re.DOTALL | re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Fallback to German
    if lang != "de":
        m = re.search(r"^## de\n(.*?)(?=^## |\Z)", body, re.DOTALL | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return body.strip()


def frontmatter_start(path: Path) -> str:
    """Return the 'start' date string from a file's YAML frontmatter, or ''."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return ""
    try:
        fm = yaml.safe_load(m.group(1))
        return str(fm.get("start", ""))
    except Exception:
        return ""


def resolve_files(section_type: str, include) -> list[Path]:
    if section_type in SINGLE_FILE_SECTIONS:
        candidate = CONTENT_DIR / f"{section_type}.md"
        return [candidate] if candidate.exists() else []

    subdir = CONTENT_DIR / section_type
    if not subdir.is_dir():
        return []

    if include == "all":
        # Sort by 'start' date descending (most recent first)
        files = list(subdir.glob("*.md"))
        files.sort(key=frontmatter_start, reverse=True)
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
    files.sort(key=frontmatter_start, reverse=True)
    return files


def assemble(profile_path: Path) -> tuple[str, dict]:
    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    lang = profile.get("lang", "de")
    title = profile.get("name", "Lebenslauf" if lang == "de" else "Curriculum Vitae")

    parts: list[str] = []

    for section in profile.get("sections", []):
        if isinstance(section, str):
            section_type = section
            include = "all"
        else:
            section_type = next(iter(section))
            cfg = section[section_type]
            include = cfg.get("include", "all") if isinstance(cfg, dict) else "all"

        label = SECTION_LABELS.get(section_type, {}).get(lang, section_type.title())
        parts.append(f"\n## {label}\n")

        for f in resolve_files(section_type, include):
            content = extract_lang_section(f.read_text(encoding="utf-8"), lang)
            if content:
                parts.append(content + "\n")

    return "\n".join(parts), profile


def build(profile_path: Path, output_path: Path | None = None) -> None:
    markdown, profile = assemble(profile_path)
    lang = profile.get("lang", "de")
    title = profile.get("name", "Lebenslauf" if lang == "de" else "Curriculum Vitae")
    photo = profile.get("photo", "")

    if output_path is None:
        output_path = BASE_DIR / (profile_path.stem + ".pdf")

    # Write assembled markdown for inspection
    tmp_md = BASE_DIR / "_assembled.md"
    tmp_md.write_text(markdown, encoding="utf-8")
    print(f"Assembled markdown written to {tmp_md}")

    template = TEMPLATES_DIR / "cv.latex"
    if not template.exists():
        sys.exit(f"Template not found: {template}")

    babel_lang = "ngerman" if lang == "de" else "english"

    cmd = [
        "pandoc",
        str(tmp_md),
        "--pdf-engine=pdflatex",
        f"--template={template}",
        f"--variable=title:{title}",
        f"--variable=lang:{lang}",
        f"--variable=babel-lang:{babel_lang}",
        "-o", str(output_path),
    ]
    if photo:
        cmd += [f"--variable=photo:{photo}"]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(f"pandoc failed (exit {result.returncode})")

    print(f"Built: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    profile_arg = Path(sys.argv[1])
    if not profile_arg.exists():
        profile_arg = BASE_DIR / "profiles" / profile_arg

    output_arg = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(profile_arg, output_arg)
