#!/usr/bin/env python3
"""Generate a local static dashboard for the MIT 18.06 skill-stack."""

from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "docs" / "index.html"

STATUS_CLASS = {
    "PASS": "status-pass",
    "WATCH": "status-watch",
    "TRAIN": "status-train",
    "NEW": "status-new",
}

CAPABILITY_LABELS = {
    "row_operations_elimination_lu": r"Row operations, elimination, and \(LU\)",
    "matrix_multiplication_inverses_transposes": "Matrix multiplication, inverses, and transposes",
    "vector_spaces_subspaces": "Vector spaces and subspaces",
    "column_space_nullspace_solvability": r"Column space, nullspace, and solvability of \(Ax=b\)",
    "rref_rank_free_variables": "RREF, rank, free variables, and special solutions",
    "complete_solutions_axb": r"Complete solutions of \(Ax=b\)",
    "independence_span_basis_dimension": "Independence, span, basis, and dimension",
    "four_fundamental_subspaces": "Four fundamental subspaces",
    "orthogonality_projections_least_squares_qr": r"Orthogonality, projections, least squares, and \(QR\)",
    "determinants": "Determinants",
    "eigenvalues_diagonalization_applications": "Eigenvalues, diagonalization, and applications",
    "symmetric_positive_definite": "Symmetric and positive definite matrices",
    "complex_matrices_fft": "Complex matrices and FFT",
    "similar_matrices_jordan_form": "Similar matrices and Jordan form",
    "svd_change_of_basis_image_compression": "SVD, change of basis, and image compression",
    "linear_transformations_pseudoinverse": "Linear transformations and pseudoinverse",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def file_url(path: str) -> str:
    try:
        rel = Path(path).resolve().relative_to(ROOT)
        return "../" + quote(rel.as_posix())
    except ValueError:
        pass
    # Path.as_uri requires a valid absolute path; quote fallback keeps broken links inspectable.
    try:
        return Path(path).as_uri()
    except ValueError:
        return "file://" + quote(path)


def link(path: str, label: str | None = None) -> str:
    if not path:
        return ""
    text = label or Path(path).name
    return f'<a href="{esc(file_url(path))}">{esc(text)}</a>'


def links(value: str, *, limit: int | None = None) -> str:
    refs = split_refs(value)
    if limit is not None:
        refs = refs[:limit]
    if not refs:
        return '<span class="muted">-</span>'
    return '<span class="links">' + " ".join(link(ref) for ref in refs) + "</span>"


def status_badge(status: str) -> str:
    cls = STATUS_CLASS.get(status, "status-new")
    return f'<span class="status {cls}">{esc(status)}</span>'


def level_bar(level: str) -> str:
    try:
        value = max(0, min(4, int(level)))
    except ValueError:
        value = 0
    width = value * 25
    return (
        '<div class="level"><div class="track">'
        f'<span style="width:{width}%"></span></div><strong>{value}/4</strong></div>'
    )


def render_matrix(matrix: list[dict[str, str]], gates: dict[str, dict[str, str]]) -> str:
    rows: list[str] = []
    for row in matrix:
        gate = gates[row["next_gate"]]
        rows.append(
            "<tr>"
            f"<td><strong>{esc(CAPABILITY_LABELS.get(row['capability'], row['capability']))}</strong></td>"
            f"<td>{status_badge(row['status'])}</td>"
            f"<td>{level_bar(row['level'])}</td>"
            f"<td>{esc(row['evidence'])}</td>"
            f"<td><strong>{esc(row['next_gate'])}</strong><br>{esc(gate['criterion'])}</td>"
            f"<td>{links(row['source_refs'], limit=3)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_course(course: list[dict[str, str]]) -> str:
    rows: list[str] = []
    for row in course:
        rows.append(
            "<tr>"
            f"<td>{esc(row['unit'])}</td>"
            f"<td>{esc(row['topic'])}</td>"
            f"<td>{esc(row['title'])}</td>"
            f"<td>{links(row['video_path'])}</td>"
            f"<td>{links(row['srt_path'])}</td>"
            f"<td>{links(row['lecture_pdf_path'])}</td>"
            f"<td>{links(row['review_path'])}</td>"
            f"<td>{links(row['problem_set_refs'])}</td>"
            f"<td>{links(row['exam_refs'])}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_artifact_summary(artifacts: list[dict[str, str]]) -> str:
    counts = Counter(row["category"] for row in artifacts)
    rows = [
        f"<tr><td>{esc(category)}</td><td>{count}</td></tr>"
        for category, count in sorted(counts.items())
    ]
    return "\n".join(rows)


def render_recent_reviews(artifacts: list[dict[str, str]]) -> str:
    reviews = [row for row in artifacts if row["category"] == "review/markdown"]
    reviews.sort(key=lambda row: row["source_path"])
    rows = [
        "<tr>"
        f"<td>{link(row['source_path'])}</td>"
        f"<td>{esc(row['bytes'])}</td>"
        "</tr>"
        for row in reviews
    ]
    return "\n".join(rows)


def render_generated_materials(artifacts: list[dict[str, str]]) -> str:
    generated = [row for row in artifacts if row["category"].startswith("generated/")]
    generated.sort(key=lambda row: (row["category"], row["source_path"]))
    if not generated:
        return '<tr><td colspan="4" class="muted">No generated day materials yet.</td></tr>'
    rows = [
        "<tr>"
        f"<td>{esc(row['category'])}</td>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{link(row['source_path'])}</td>"
        f"<td>{esc(row['bytes'])}</td>"
        "</tr>"
        for row in generated
    ]
    return "\n".join(rows)


def render_submissions(artifacts: list[dict[str, str]]) -> str:
    submissions = [row for row in artifacts if row["category"].startswith("submission/")]
    submissions.sort(key=lambda row: row["source_path"])
    if not submissions:
        return '<tr><td colspan="3" class="muted">No submitted work yet.</td></tr>'
    rows = [
        "<tr>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{link(row['source_path'])}</td>"
        f"<td>{esc(row['bytes'])}</td>"
        "</tr>"
        for row in submissions
    ]
    return "\n".join(rows)


def build_html() -> str:
    matrix = read_csv("capability_matrix.csv")
    gates = {row["gate_id"]: row for row in read_csv("gates.csv")}
    course = read_csv("course_map.csv")
    artifacts = read_csv("artifacts_manifest.csv")
    status_counts = Counter(row["status"] for row in matrix)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MIT 18.06 Skill Stack</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #1b1f24;
      --muted: #67717f;
      --line: #d9e0e8;
      --panel: #f7f9fb;
      --pass: #1f7a4d;
      --watch: #9a6700;
      --train: #b42318;
      --new: #5b6472;
      --accent: #245f73;
    }}
    body {{
      margin: 0;
      font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: #fff;
    }}
    header {{
      padding: 28px 32px 18px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #f8fbfc 0%, #fff 100%);
    }}
    main {{
      padding: 24px 32px 48px;
      display: grid;
      gap: 28px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }}
    p {{
      max-width: 980px;
      margin: 0;
      color: var(--muted);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: #fff;
      border: 1px solid var(--line);
    }}
    th, td {{
      padding: 10px 12px;
      vertical-align: top;
      border-bottom: 1px solid var(--line);
      text-align: left;
    }}
    th {{
      background: var(--panel);
      color: #354052;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    a {{
      color: var(--accent);
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .summary {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }}
    .pill {{
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 6px;
      padding: 6px 10px;
      color: #354052;
    }}
    .status {{
      display: inline-block;
      min-width: 54px;
      padding: 3px 8px;
      border-radius: 5px;
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      text-align: center;
    }}
    .status-pass {{ background: var(--pass); }}
    .status-watch {{ background: var(--watch); }}
    .status-train {{ background: var(--train); }}
    .status-new {{ background: var(--new); }}
    .level {{
      min-width: 82px;
      display: grid;
      gap: 4px;
    }}
    .track {{
      height: 7px;
      background: #e8edf2;
      border-radius: 999px;
      overflow: hidden;
    }}
    .track span {{
      display: block;
      height: 100%;
      background: var(--accent);
    }}
    .links {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px 10px;
    }}
    .muted {{
      color: var(--muted);
    }}
    .wide {{
      overflow-x: auto;
    }}
  </style>
</head>
<body>
  <header>
    <h1>MIT 18.06 Skill Stack</h1>
    <p>Local-first progress dashboard for the personal Linear Algebra stack. Source assets stay in the Obsidian mirror; this repo tracks gates, matrix status, and links.</p>
    <div class="summary">
      <span class="pill">Capabilities: {len(matrix)}</span>
      <span class="pill">PASS: {status_counts.get('PASS', 0)}</span>
      <span class="pill">WATCH: {status_counts.get('WATCH', 0)}</span>
      <span class="pill">TRAIN: {status_counts.get('TRAIN', 0)}</span>
      <span class="pill">NEW: {status_counts.get('NEW', 0)}</span>
      <span class="pill">Course rows: {len(course)}</span>
      <span class="pill">Artifacts: {len(artifacts)}</span>
    </div>
  </header>
  <main>
    <section>
      <h2>Capability Matrix</h2>
      <div class="wide">
        <table>
          <thead>
            <tr>
              <th>Capability</th>
              <th>Status</th>
              <th>Level</th>
              <th>Evidence</th>
              <th>Next gate</th>
              <th>Source refs</th>
            </tr>
          </thead>
          <tbody>
            {render_matrix(matrix, gates)}
          </tbody>
        </table>
      </div>
    </section>
    <section>
      <h2>Course Map</h2>
      <div class="wide">
        <table>
          <thead>
            <tr>
              <th>Unit</th>
              <th>Topic</th>
              <th>Title</th>
              <th>Video</th>
              <th>SRT</th>
              <th>PDF</th>
              <th>Review</th>
              <th>Problem set</th>
              <th>Exam</th>
            </tr>
          </thead>
          <tbody>
            {render_course(course)}
          </tbody>
        </table>
      </div>
    </section>
    <section>
      <h2>Artifact Summary</h2>
      <table>
        <thead><tr><th>Category</th><th>Count</th></tr></thead>
        <tbody>{render_artifact_summary(artifacts)}</tbody>
      </table>
    </section>
    <section>
      <h2>Generated Materials</h2>
      <table>
        <thead><tr><th>Category</th><th>Title</th><th>Path</th><th>Bytes</th></tr></thead>
        <tbody>{render_generated_materials(artifacts)}</tbody>
      </table>
    </section>
    <section>
      <h2>Submitted Work</h2>
      <table>
        <thead><tr><th>Title</th><th>Path</th><th>Bytes</th></tr></thead>
        <tbody>{render_submissions(artifacts)}</tbody>
      </table>
    </section>
    <section>
      <h2>Review Notes</h2>
      <table>
        <thead><tr><th>Path</th><th>Bytes</th></tr></thead>
        <tbody>{render_recent_reviews(artifacts)}</tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_html(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
