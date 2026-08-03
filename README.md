# mit-1806-skill-stack

Repo-first personal learning stack for MIT 18.06 Spring 2010, based on the local course mirror:

```text
/Users/aloschilov/Obsidian/Math/DeepLearning/Books/18.06-spring-2010
```

The mirror stays read-only. This repo tracks concept gates, progress, study notes, local source inventory, and a local dashboard.

## Current Focus

The existing Obsidian review work is strongest around Lectures 6-8: vector spaces, subspaces, \(C(A)\), \(N(A)\), rank, free variables, special solutions, and complete solutions of \(Ax=b\). Lectures 9-10 have rough review notes and should be converted into gated understanding next: independence, span, basis, dimension, and the four fundamental subspaces.

## Structure

```text
mit-1806-skill-stack/
├── AGENTS.md
├── MATRIX.md
├── data/
│   ├── artifacts_manifest.csv
│   ├── capability_matrix.csv
│   ├── course_map.csv
│   └── gates.csv
├── docs/
│   ├── assignments/
│   ├── latex-workflow.md
│   ├── artifact-storage.md
│   ├── index.html
│   ├── session-notes.md
│   └── skill-gates.md
├── prompts/
│   └── next-session-template.md
└── scripts/
    ├── build_day_pdfs.py
    ├── generate_dashboard.py
    ├── import_ocw_manifest.py
    └── validate_matrix.py
```

## Status Model

- `PASS` - the concept passes its explicit gate.
- `WATCH` - the concept is mostly usable but still needs checked transfer.
- `TRAIN` - the concept needs deliberate short practice.
- `NEW` - the concept is not yet actively reviewed in this stack.

## Local Dashboard

Build the dashboard after imports or matrix edits:

```bash
python3 scripts/import_ocw_manifest.py
python3 scripts/validate_matrix.py
python3 scripts/generate_dashboard.py
```

Then open:

```text
docs/index.html
```

## Printable Packets

Daily printable packets are generated from Markdown through Pandoc and XeLaTeX:

```bash
python3 scripts/build_day_pdfs.py --day 1 --update-manifest --render-preview
```

Sources live in `artifacts/generated/source/dayNN/`; PDFs live in `artifacts/generated/tasks/`, `artifacts/generated/answers/`, and when there is checked work, `artifacts/generated/feedback_self/`. This MIT 18.06 stack intentionally does not generate parent-feedback PDFs.

## Source Inventory

The importer indexes local assets and review notes without copying them:

```bash
python3 scripts/import_ocw_manifest.py
```

The quick source check expects the current mirror shape: 34 lecture videos, 34 SRT files, 104 PDFs, 10 problem-set solution PDFs, exam/final files, and 39 review Markdown files.
