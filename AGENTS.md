# Repo Instructions For Codex

## Source Of Truth

This repo is a personal skill-stack for MIT 18.06 Spring 2010.

- Source mirror: `/Users/aloschilov/Obsidian/Math/DeepLearning/Books/18.06-spring-2010`.
- Treat the source mirror as read-only unless the user explicitly asks to edit Obsidian notes.
- Do not copy large source assets into this repo. Index MP4, PDF, SRT, image, JSON, and review files by absolute path in `data/artifacts_manifest.csv`.
- Store learning progress, gates, generated Markdown, validation scripts, and dashboard output in this repo.

## Math Notation

All new mathematical expressions in Markdown docs, generated materials, prompt templates, and generator-script strings should use LaTeX notation.

- Inline formulas: `\( ... \)`.
- Display formulas:

```tex
\[
...
\]
```

- Prefer `\(Ax=b\)`, `\(A^T\)`, `\(C(A)\)`, `\(N(A)\)`, `\(r=n\)`, `\(QR\)`, `\(\lambda\)`, and `\(\mathbb{R}^n\)`.
- Do not write new user-facing math as plain text such as `Ax=b`, `A^T`, `R^n`, `r=n`, `<=`, `>=`, `->`, or `*`, except when explaining literal syntax or file names.
- Existing Obsidian review notes may use `$...$`; do not rewrite them just to normalize notation.

## Workflow

- Update `MATRIX.md` and `data/capability_matrix.csv` when concept status changes.
- Update `docs/session-notes.md` after a study or review iteration.
- Update `docs/skill-gates.md` and `data/gates.csv` when gate criteria change.
- For printable day packets, use Markdown sources in `artifacts/generated/source/dayNN/` and build PDFs with:

```bash
python3 scripts/build_day_pdfs.py --day NN --update-manifest --render-preview
```

- Day packets in this repo should include learner-facing assignments and answers/checking accents. Do not create parent-feedback PDFs for this MIT 18.06 stack.
- Each day-source Markdown file must have front matter with `title:` and `output:`. The `output:` path must stay inside `artifacts/generated/...`.
- Use `templates/day-material.tex` for PDF rendering. Do not add a separate renderer unless the shared template cannot support the task.
- In generated PDFs, formulas should render as mathematical symbols. Do not deliver PDFs where raw LaTeX markers such as `\(`, `\)`, `\mathbb`, `\Rightarrow`, or `\begin{bmatrix}` are visible in the text layer.
- Regenerate local source indexes with:

```bash
python3 scripts/import_ocw_manifest.py
```

- Regenerate the dashboard with:

```bash
python3 scripts/generate_dashboard.py
```

## Checks

After changing matrix, gate, manifest, prompt, or dashboard code, run:

```bash
python3 scripts/import_ocw_manifest.py --check
python3 scripts/validate_matrix.py
python3 scripts/generate_dashboard.py
git diff --check
```

After generating day PDFs, additionally run:

```bash
python3 scripts/build_day_pdfs.py --day NN --update-manifest --render-preview
pdftotext path/to/file.pdf - | rg '\\\\\(|\\\\\)|\\\\mathbb|\\\\Rightarrow|\\\\begin|\\\\end'
```

The `pdftotext` check should not find raw LaTeX markers. Then visually inspect the PNG previews in `tmp/pdfs/rendered_check/`.
