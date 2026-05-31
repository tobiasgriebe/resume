# CV — Dr. Tobias Griebe

Modular CV system. Content lives in Markdown files under `content/`. Profiles select which blocks to include. The build pipeline assembles them, renders HTML via pandoc, and prints to PDF via Chrome headless.

---

## Quick Start

```bash
# Build all profiles at once
python3 build.py --all

# Build a single profile — produces DE and EN PDFs in output/pdf/
python3 build.py profiles/extended-modern.yaml

# HTML preview only (no Chrome needed, fast)
python3 build.py --all --html-only
python3 build.py profiles/extended-modern.yaml --html-only

# Force a single language
python3 build.py --all --lang de
python3 build.py profiles/extended-modern.yaml --lang de

# Custom output path (single profile, single language only)
python3 build.py profiles/extended-modern.yaml --lang de output/pdf/my-cv.pdf
```

Output always lands in `output/html/` and `output/pdf/`.

---

## Profiles

| Profile | Template | Length | Use case |
|---|---|---|---|
| `full.yaml` | modern | unlimited | Complete CV — every entry, project, publication |
| `extended-modern.yaml` | modern | 3–4 pages | All key roles + select projects; modern dark header |
| `extended-conservative.yaml` | conservative | 3–4 pages | Same content; traditional white-header styling |
| `onepager-modern.yaml` | modern | ~1 page | Top 4 roles only; compact layout |
| `onepager-conservative.yaml` | conservative | ~1 page | Same content; traditional styling |

Each profile generates both `*-de.pdf` and `*-en.pdf` by default.

---

## Directory Layout

```
build.py                    build script
profiles/                   YAML files controlling what each CV contains
templates/
  cv.html                   modern template (dark navy header)
  cv-conservative.html      conservative template (white header, clean lines)
content/
  experience/               one .md file per role
  education/                one .md file per degree
  skills/                   one .md file per skill area
  projects/                 one .md file per project
  certifications.md
  publications.md
  teaching.md
  zivildienst.md
output/
  html/                     intermediate HTML files (pandoc output)
  pdf/                      final PDF files (Chrome headless output)
```

---

## Content Files

Every file under `content/` uses YAML frontmatter and two language sections:

```markdown
---
type: experience
id: my-company-role
company: My Company
start: 2023-01
end: 2025-12
---

## de

01/2023 – 12/2025
:   **Job Title** — My Company, City

    Description text here.

    - Bullet point one
    - Bullet point two

## en

01/2023 – 12/2025
:   **Job Title** — My Company, City

    Description text here.

    - Bullet point one
    - Bullet point two
```

Experience and education entries use pandoc's definition list syntax (`term\n:\n    definition`), which renders as `<dl><dt><dd>` — the date label floats left, the content indents right.

Multi-file sections (`experience/`, `education/`, `skills/`, `projects/`) sort automatically by the `start:` frontmatter field, newest first. Single-file sections (`certifications.md`, `publications.md`, `teaching.md`, `zivildienst.md`) are included as-is.

---

## Profiles

A profile YAML controls the entire output:

```yaml
name: Dr. Tobias Griebe
subtitle:
  de: "Engineering Director · IT-Abteilungsleitung"
  en: "Engineering Director · IT Department Head"
contact: "Street · City · Phone · email@example.com"
photo: portrait.png
template: cv.html       # cv.html or cv-conservative.html
compact: true           # optional — tighter layout for onepagers

sections:
  - experience:
      include:
        - sevdesk-director       # matches content/experience/sevdesk-director.md
        - wuerth-head-of-dev
  - education:
      include: all               # includes every file in content/education/, sorted by start:
  - skills:
      include:
        - leadership
        - engineering-management
  - certifications               # single-file section, no include key needed
  - projects:
      include:
        - bofrost-mobile-pos
```

`subtitle` and `contact` can be plain strings (used for both languages) or `{de: "...", en: "..."}` dicts.

If `lang:` is omitted the profile produces both DE and EN. Set `lang: de` or `lang: en` to restrict to one language.

---

## Adding Content

**New experience entry:**
1. Create `content/experience/<id>.md` with `type: experience`, `start:` (YYYY-MM), `end:` frontmatter, and `## de` / `## en` sections.
2. Add `<id>` to the `include` list of any profiles that should show it.

**New project:**
1. Create `content/projects/<id>.md`.
2. Add `<id>` to `projects.include` in the relevant profiles.

**New profile:**
1. Copy an existing profile YAML from `profiles/`.
2. Adjust `sections`, `template`, `compact`, `subtitle`.

---

## Dependencies

- **Python 3.10+** with `pyyaml` (`pip install pyyaml`)
- **pandoc** — `brew install pandoc`
- **Google Chrome** — for headless PDF printing
