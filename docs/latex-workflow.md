# LaTeX PDF Workflow

Printable day packets are generated from Markdown through Pandoc and XeLaTeX. This is the preferred path for new MIT 18.06 study packets.

## Structure

```text
artifacts/generated/source/dayNN/
├── feedback_self.md
├── tasks.md
└── answers.md
```

Each file starts with front matter:

```yaml
---
title: "День NN. Задания"
subtitle: "MIT 18.06. Время: 60-90 минут."
output: "artifacts/generated/tasks/dayNN_tasks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---
```

Do not create parent-feedback PDFs in this repo. The standard daily packet is assignments plus answers/checking accents. Add `feedback_self.md` only after there is actual completed work to review.

Each learner-facing or review PDF source should start, after the opening goal callout, with a compact `# Глоссарий` section. Include the main Russian term, the corresponding English term in parentheses, and one short definition. Keep it concise enough that the first page still reaches the first real exercise or feedback section.

## Formulas

- Inline formulas: `\( ... \)`.
- Display formulas:

```tex
\[
...
\]
```

- In final PDFs, formulas must render as mathematical symbols, not as raw LaTeX markers.
- Do not use Markdown backticks around formulas in user-facing PDF sources.

## Build

```bash
python3 scripts/build_day_pdfs.py --day NN --update-manifest --render-preview
```

The builder:

- reads every `*.md` source from `artifacts/generated/source/dayNN/`;
- uses `templates/day-material.tex`;
- writes each PDF to the `output:` path from front matter;
- checks that every output PDF has at least one page;
- checks that raw LaTeX markers did not survive in the PDF text layer;
- optionally renders PNG previews under `tmp/pdfs/rendered_check/`;
- optionally updates `data/artifacts_manifest.csv`.

After building, visually inspect the PNG previews and run:

```bash
python3 scripts/import_ocw_manifest.py --check
python3 scripts/validate_matrix.py
python3 scripts/generate_dashboard.py
git diff --check
```
