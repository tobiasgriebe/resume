# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

CV/resume system for Dr. Tobias Griebe. Content lives in modular Markdown files under `content/`. Build pipeline: `build.py` assembles selected content blocks, renders to HTML via pandoc, then prints to PDF via Chrome headless. No LaTeX.

## Build Commands

```bash
# Build a specific profile (produces .html + .pdf)
python3 build.py profiles/engineering-director-de.yaml

# HTML preview only (fast, no Chrome)
python3 build.py profiles/engineering-director-de.yaml --html-only

# Custom output path
python3 build.py profiles/engineering-director-de.yaml output.pdf
```

**Available profiles** (`profiles/`):
- `engineering-director-de.yaml` — focused DE CV, current role
- `engineering-director-en.yaml` — focused EN CV, current role
- `default-de.yaml` — full DE CV with all experience and projects
- `default-en.yaml` — full EN CV

## Architecture

### Content (`content/`)
All source content in Markdown with YAML frontmatter. Each file has a `## de` and `## en` section.

```
content/
  personal.md                  — contact info
  certifications.md            — certifications
  publications.md              — peer-reviewed publications
  teaching.md                  — university teaching
  zivildienst.md               — community service
  experience/                  — one file per role (sorted by start: date)
    cloudfactory-head-of-consulting.md
    sevdesk-director.md
    wuerth-head-of-dev.md
    ...
  education/
    phd.md
    diplom.md
    school.md
  skills/
    leadership.md
    engineering-management.md
    agile-methods.md
    technologies-cloud.md
    technologies-backend.md
    technologies-mobile.md
    languages.md
  projects/                    — one file per project
    bofrost-mobile-pos.md
    ambista.md
    ...
```

### Profiles (`profiles/`)
YAML files that select which content blocks to include and in which language.

```yaml
name: Dr. Tobias Griebe
subtitle: "Engineering Director · IT-Abteilungsleitung"
contact: "Goethestraße 10 · 15345 Eggersdorf · 0159 06303187 · griebe.tobias@gmail.com"
photo: portrait.png
lang: de         # de or en

sections:
  - experience:
      include:
        - sevdesk-director
        - wuerth-head-of-dev
  - education:
      include: [phd, diplom]
  - skills:
      include: all
  - certifications
  - projects:
      include: [bofrost-mobile-pos, ambista]
```

Sections with `include: all` auto-sort by `start:` date descending.

### Template (`templates/cv.html`)
Pandoc HTML5 template. Uses variables: `$title$`, `$subtitle$`, `$contact$`, `$photo$`, `$lang$`, `$body$`.

## Adding Content

**New experience entry**: create `content/experience/<id>.md` with `type: experience`, `start:`, `end:` frontmatter and `## de` / `## en` sections. Add the id to any profiles that should include it.

**New project**: create `content/projects/<id>.md` and add the id to profile `projects.include` lists.

**New profile**: copy an existing profile YAML and adjust `sections`, `lang`, `name`, `subtitle`.

## Key Reference File

`experiences.txt` — unstructured notes on accomplishments at sevDesk and Würth Cloud Services, used as a drafting source.

## Subdirectories

- `bvv/` — application package for BVV Insurance (PDFs + HTML, no editable source)
- `Bewerbungen/` — compiled application documents for various positions
- `Dokumente/` — reference documents (certificates, employment references)
