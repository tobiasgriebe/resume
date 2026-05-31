# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

This is a LaTeX-based CV/resume system for Dr. Tobias Griebe. It is not a software development repository. The primary output is `lebenslauf.pdf` (German) compiled from modular `.tex` source files.

## Build Commands

```bash
# Compile the CV to PDF
pdflatex lebenslauf.tex

# Or with latexmk (handles multiple passes automatically)
latexmk -pdf lebenslauf.tex

# Clean auxiliary files
latexmk -c
```

## Architecture

The system uses a single master file (`lebenslauf.tex`) that controls everything via LaTeX boolean flags. Each section is a standalone `.tex` file included conditionally.

**Master file**: `lebenslauf.tex`
- Declares all boolean flags (e.g., `\newboolean{showBeruf}`)
- Sets their values in one central block (lines ~69–106)
- Includes section files using `\ifaufEnglisch ... \else ... \fi` for language branching

**Language switching**: Set `\setboolean{aufEnglisch}{true}` in `lebenslauf.tex` to switch the entire CV to English. Each section has a German (`beruf.tex`) and English (`beruf-engl.tex`) variant.

**Section files** (each begins with `%!TEX root = lebenslauf.tex`):
- `person.tex` / `person-engl.tex` — personal contact info
- `beruf.tex` / `beruf-engl.tex` — work experience
- `studium.tex` / `studium-engl.tex` — education
- `kenntnisse.tex` / `kenntnisse-engl.tex` — skills/competencies
- `zertifikate.tex` / `zertifikate-engl.tex` — certifications
- `projekte.tex` / `projekte-engl.tex` — project list (includes individual project files conditionally)
- Individual project files: `bofrost.tex`, `uxitergo.tex`, `ambista.tex`, etc.

**Photo**: Controlled by `\setboolean{mitFoto}{true/false}`; uses `portrait_small.pdf`.

**Subdirectories**:
- `bvv/` — application package for BVV Insurance position (PDFs only, no editable source)
- `Bewerbungen/` — compiled application documents for various positions
- `Dokumente/` — reference documents (certificates, employment references)

## Tailoring the CV

To include or exclude a section, flip its boolean in `lebenslauf.tex`:
```latex
\setboolean{showPublikationen}{true}  % show publications
\setboolean{showLehre}{false}         % hide teaching experience
```

Individual projects can be toggled independently:
```latex
\setboolean{showProjektUXITERGO}{false}
```

To add a new project: create a new `.tex` file (follow the pattern of existing project files), add a boolean for it, and reference it in `projekte.tex`.

## Key Content File

`experiences.txt` — unstructured notes on accomplishments and bullet points at sevDesk and Würth Cloud Services, used as a source for drafting CV content.
