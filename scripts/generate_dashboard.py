#!/usr/bin/env python3
"""Generate the static MIT 18.06 learning dashboard."""

from __future__ import annotations

import csv
import html
import re
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
    "row_operations_elimination_lu": r"Row operations, elimination и \(LU\)",
    "matrix_multiplication_inverses_transposes": "Matrix multiplication, inverses и transposes",
    "vector_spaces_subspaces": "Vector spaces и subspaces",
    "column_space_nullspace_solvability": r"Column space, nullspace и solvability of \(Ax=b\)",
    "rref_rank_free_variables": "RREF, rank, free variables и special solutions",
    "complete_solutions_axb": r"Complete solutions of \(Ax=b\)",
    "independence_span_basis_dimension": "Independence, span, basis и dimension",
    "four_fundamental_subspaces": "Four fundamental subspaces",
    "orthogonality_projections_least_squares_qr": r"Orthogonality, projections, least squares и \(QR\)",
    "determinants": "Determinants",
    "eigenvalues_diagonalization_applications": "Eigenvalues, diagonalization и applications",
    "symmetric_positive_definite": "Symmetric и positive definite matrices",
    "complex_matrices_fft": "Complex matrices и FFT",
    "similar_matrices_jordan_form": "Similar matrices и Jordan form",
    "svd_change_of_basis_image_compression": "SVD, change of basis и image compression",
    "linear_transformations_pseudoinverse": "Linear transformations и pseudoinverse",
}

FOCUS_BY_DAY = {
    5: {
        "title": "День 5: ремонт Gate G + Gate H",
        "summary": (
            "Закрепить две count-versus-dimension формулировки, затем построить "
            r"bases и dimensions для \(C(A)\), \(N(A)\), \(C(A^T)\) и \(N(A^T)\)."
        ),
    },
    6: {
        "title": "День 6: matrix spaces и rank one",
        "summary": (
            "Закрепить смысл left nullspace, затем найти bases и dimensions для "
            r"matrix subspaces, исследовать \(S\cap U\), \(S+U\) и factorization \(uv^T\)."
        ),
    },
}

MATERIAL_LABELS = {
    "generated/tasks": "Задания",
    "generated/answers": "Ответы",
    "generated/feedback_self": "Обратная связь",
    "generated/source": "Markdown source",
}

DAY_RE = re.compile(r"day(\d+)", re.IGNORECASE)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def repo_relative(path: str) -> Path | None:
    try:
        return Path(path).resolve().relative_to(ROOT)
    except ValueError:
        return None


def file_url(path: str) -> str:
    rel = repo_relative(path)
    if rel is not None:
        return "../" + quote(rel.as_posix())
    try:
        return Path(path).as_uri()
    except ValueError:
        return "file://" + quote(path)


def link(path: str, label: str | None = None) -> str:
    if not path:
        return ""
    text = label or Path(path).name
    if repo_relative(path) is not None:
        return f'<a class="file-link" href="{esc(file_url(path))}">{esc(text)}</a>'
    return (
        f'<a class="local-link" href="{esc(file_url(path))}" data-local-only="true" '
        f'title="Доступно только на локальной машине: {esc(path)}">'
        f'{esc(text)}<span class="local-badge">LOCAL</span></a>'
    )


def links(value: str, *, limit: int | None = None) -> str:
    refs = split_refs(value)
    if limit is not None:
        refs = refs[:limit]
    if not refs:
        return '<span class="muted">Нет</span>'
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
        f'<div class="level" aria-label="Уровень {value} из 4">'
        '<div class="track" aria-hidden="true">'
        f'<span style="width:{width}%"></span></div><strong>{value}/4</strong></div>'
    )


def format_size(raw_bytes: str) -> str:
    try:
        size = int(raw_bytes)
    except ValueError:
        return esc(raw_bytes)
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MiB"
    if size >= 1024:
        return f"{size / 1024:.1f} KiB"
    return f"{size} B"


def artifact_day(row: dict[str, str]) -> int | None:
    match = DAY_RE.search(row["source_path"])
    return int(match.group(1)) if match else None


def generated_pdfs(artifacts: list[dict[str, str]]) -> list[dict[str, str]]:
    categories = {
        "generated/tasks",
        "generated/answers",
        "generated/feedback_self",
    }
    return [row for row in artifacts if row["category"] in categories]


def render_matrix(matrix: list[dict[str, str]], gates: dict[str, dict[str, str]]) -> str:
    rows: list[str] = []
    for row in matrix:
        gate = gates[row["next_gate"]]
        gate_label = row["next_gate"].replace("_", " ").upper()
        rows.append(
            '<tr class="capability-row">'
            f'<td class="capability-name" data-label="Навык"><strong>{esc(CAPABILITY_LABELS.get(row["capability"], row["capability"]))}</strong></td>'
            f'<td data-label="Статус">{status_badge(row["status"])}</td>'
            f'<td data-label="Уровень">{level_bar(row["level"])}</td>'
            f'<td data-label="Evidence">{esc(row["evidence"])}</td>'
            f'<td data-label="Следующий gate"><strong>{esc(gate_label)}</strong><br>{esc(gate["criterion"])}</td>'
            f'<td data-label="Источники">{links(row["source_refs"], limit=3)}</td>'
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
    return "\n".join(
        f"<tr><td>{esc(category)}</td><td>{count}</td></tr>"
        for category, count in sorted(counts.items())
    )


def render_recent_reviews(artifacts: list[dict[str, str]]) -> str:
    reviews = [row for row in artifacts if row["category"] == "review/markdown"]
    reviews.sort(key=lambda row: row["source_path"])
    return "\n".join(
        "<tr>"
        f"<td>{link(row['source_path'])}</td>"
        f"<td>{format_size(row['bytes'])}</td>"
        "</tr>"
        for row in reviews
    )


def render_generated_materials(
    artifacts: list[dict[str, str]], *, latest_day_count: int | None = None
) -> str:
    generated = generated_pdfs(artifacts)
    if latest_day_count is not None:
        days = sorted(
            {day for row in generated if (day := artifact_day(row)) is not None},
            reverse=True,
        )
        generated = [row for row in generated if artifact_day(row) in days[:latest_day_count]]
    generated.sort(
        key=lambda row: (artifact_day(row) or -1, row["category"]), reverse=True
    )
    if not generated:
        return '<tr><td colspan="5" class="muted">Материалы ещё не созданы.</td></tr>'
    return "\n".join(
        "<tr>"
        f"<td><strong>День {artifact_day(row)}</strong></td>"
        f"<td>{esc(MATERIAL_LABELS.get(row['category'], row['category']))}</td>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{link(row['source_path'], 'Открыть PDF')}</td>"
        f"<td>{format_size(row['bytes'])}</td>"
        "</tr>"
        for row in generated
    )


def render_source_materials(artifacts: list[dict[str, str]]) -> str:
    generated = [row for row in artifacts if row["category"] == "generated/source"]
    generated.sort(key=lambda row: (artifact_day(row) or -1, row["source_path"]), reverse=True)
    return "\n".join(
        "<tr>"
        f"<td>День {artifact_day(row)}</td>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{link(row['source_path'])}</td>"
        f"<td>{format_size(row['bytes'])}</td>"
        "</tr>"
        for row in generated
    )


def render_submissions(artifacts: list[dict[str, str]]) -> str:
    submissions = [row for row in artifacts if row["category"].startswith("submission/")]
    submissions.sort(key=lambda row: artifact_day(row) or -1, reverse=True)
    if not submissions:
        return '<tr><td colspan="3" class="muted">Решений пока нет.</td></tr>'
    return "\n".join(
        "<tr>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{link(row['source_path'], 'Открыть решение')}</td>"
        f"<td>{format_size(row['bytes'])}</td>"
        "</tr>"
        for row in submissions
    )


def focus_link(
    artifacts: list[dict[str, str]], category: str, day: int, label: str
) -> str:
    for row in artifacts:
        if row["category"] == category and artifact_day(row) == day:
            return link(row["source_path"], label)
    return f'<span class="muted">{esc(label)} пока недоступен</span>'


def render_focus(artifacts: list[dict[str, str]]) -> str:
    task_days = [artifact_day(row) for row in artifacts if row["category"] == "generated/tasks"]
    latest_day = max((day for day in task_days if day is not None), default=0)
    focus = FOCUS_BY_DAY.get(
        latest_day,
        {
            "title": f"День {latest_day}",
            "summary": "Продолжить текущую последовательность gates и зафиксировать решение.",
        },
    )
    feedback_day = max(0, latest_day - 1)
    actions = [
        focus_link(artifacts, "generated/tasks", latest_day, "Открыть задания"),
        focus_link(artifacts, "generated/answers", latest_day, "Свериться с ответами"),
        focus_link(
            artifacts,
            "generated/feedback_self",
            feedback_day,
            f"Обратная связь за День {feedback_day}",
        ),
    ]
    return (
        '<section class="focus" aria-labelledby="focus-title">'
        '<div class="focus-copy">'
        '<span class="eyebrow">Сейчас в работе</span>'
        f'<h2 id="focus-title">{esc(focus["title"])}</h2>'
        f'<p>{esc(focus["summary"])}</p>'
        '</div><nav class="focus-actions" aria-label="Материалы текущего дня">'
        + "".join(actions)
        + "</nav></section>"
    )


def build_html() -> str:
    matrix = read_csv("capability_matrix.csv")
    gates = {row["gate_id"]: row for row in read_csv("gates.csv")}
    course = read_csv("course_map.csv")
    artifacts = read_csv("artifacts_manifest.csv")
    status_counts = Counter(row["status"] for row in matrix)

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Прогресс, gates и материалы личного курса MIT 18.06 Linear Algebra.">
  <title>MIT 18.06 Skill Stack</title>
  <script>
    window.MathJax = {{
      tex: {{ inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] }},
      options: {{ skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  <style>
    :root {{
      color-scheme: light;
      --ink: #182026;
      --muted: #5f6b75;
      --line: #d7dee3;
      --panel: #f5f7f8;
      --panel-strong: #eaf0f2;
      --pass: #26734d;
      --watch: #8a6200;
      --train: #a6362a;
      --new: #58636d;
      --accent: #17677a;
      --accent-dark: #104f5e;
      --focus: #d6a400;
    }}
    * {{ box-sizing: border-box; }}
    html {{ overflow-x: hidden; }}
    body {{
      margin: 0;
      font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: #fff;
      overflow-wrap: anywhere;
    }}
    a {{ color: var(--accent-dark); text-decoration-thickness: 1px; text-underline-offset: 3px; }}
    a:hover {{ color: var(--accent); }}
    a:focus-visible, summary:focus-visible {{ outline: 3px solid var(--focus); outline-offset: 3px; }}
    .skip-link {{ position: absolute; left: 16px; top: -80px; background: #fff; padding: 10px; z-index: 10; }}
    .skip-link:focus {{ top: 16px; }}
    .page-shell {{ width: min(100%, 1480px); margin: 0 auto; min-width: 0; }}
    header {{ padding: 28px 32px 20px; border-bottom: 1px solid var(--line); background: var(--panel); }}
    h1, h2 {{ letter-spacing: 0; }}
    h1 {{ margin: 0 0 6px; font-size: 28px; line-height: 1.2; }}
    h2 {{ margin: 0 0 12px; font-size: 19px; line-height: 1.3; }}
    p {{ margin: 0; color: var(--muted); }}
    main {{ padding: 24px 32px 48px; display: grid; gap: 30px; min-width: 0; }}
    main > section, main > details {{ min-width: 0; }}
    .summary {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }}
    .pill {{ border: 1px solid var(--line); background: #fff; border-radius: 6px; padding: 5px 9px; color: #33414b; }}
    .focus {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 24px;
      align-items: center;
      padding: 20px 22px;
      border-left: 5px solid var(--accent);
      background: var(--panel-strong);
    }}
    .focus h2 {{ margin: 2px 0 5px; font-size: 22px; }}
    .eyebrow {{ color: var(--accent-dark); font-size: 12px; font-weight: 800; text-transform: uppercase; }}
    .focus-actions {{ display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 9px; max-width: 560px; }}
    .focus-actions a {{ display: inline-flex; align-items: center; min-height: 38px; padding: 8px 11px; border: 1px solid #9eb2b9; border-radius: 6px; background: #fff; font-weight: 700; text-decoration: none; }}
    .section-intro {{ margin: -6px 0 12px; }}
    .legend {{ display: flex; flex-wrap: wrap; gap: 8px 14px; margin: 0 0 12px; color: var(--muted); font-size: 13px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid var(--line); }}
    th, td {{ padding: 10px 11px; vertical-align: top; border-bottom: 1px solid var(--line); text-align: left; }}
    th {{ background: var(--panel); color: #34424c; font-size: 11px; text-transform: uppercase; }}
    tbody tr:last-child td {{ border-bottom: 0; }}
    .table-scroll {{ max-width: 100%; min-width: 0; overflow-x: auto; overscroll-behavior-inline: contain; }}
    .matrix-table {{ table-layout: fixed; }}
    .matrix-table th:nth-child(1) {{ width: 19%; }}
    .matrix-table th:nth-child(2) {{ width: 7%; }}
    .matrix-table th:nth-child(3) {{ width: 8%; }}
    .matrix-table th:nth-child(4) {{ width: 25%; }}
    .matrix-table th:nth-child(5) {{ width: 27%; }}
    .matrix-table th:nth-child(6) {{ width: 14%; }}
    .archive-table {{ min-width: 760px; }}
    .course-table {{ min-width: 1220px; }}
    .status {{ display: inline-block; min-width: 54px; padding: 3px 7px; border-radius: 5px; color: #fff; font-size: 11px; font-weight: 800; text-align: center; }}
    .status-pass {{ background: var(--pass); }}
    .status-watch {{ background: var(--watch); }}
    .status-train {{ background: var(--train); }}
    .status-new {{ background: var(--new); }}
    .level {{ min-width: 70px; display: grid; gap: 4px; }}
    .track {{ height: 7px; background: #e4eaee; border-radius: 999px; overflow: hidden; }}
    .track span {{ display: block; height: 100%; background: var(--accent); }}
    .links {{ display: flex; flex-wrap: wrap; gap: 6px 9px; }}
    .local-link {{ display: inline-flex; align-items: baseline; gap: 5px; }}
    .local-link[aria-disabled="true"] {{ color: var(--muted); cursor: help; text-decoration: none; }}
    .local-badge {{ border: 1px solid #aab4bc; border-radius: 4px; padding: 0 4px; color: #4e5a64; font-size: 9px; font-weight: 800; text-decoration: none; }}
    .muted {{ color: var(--muted); }}
    details {{ border-top: 1px solid var(--line); padding-top: 14px; }}
    details + details {{ margin-top: -14px; }}
    summary {{ cursor: pointer; color: var(--ink); font-size: 18px; font-weight: 750; }}
    details[open] summary {{ margin-bottom: 14px; }}
    .archive-grid {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 2fr); gap: 22px; }}
    .archive-full {{ grid-column: 1 / -1; }}
    mjx-container {{ overflow-x: auto; overflow-y: hidden; max-width: 100%; }}
    @media (max-width: 900px) {{
      .focus {{ grid-template-columns: 1fr; }}
      .focus-actions {{ justify-content: flex-start; max-width: none; }}
      .archive-grid {{ grid-template-columns: 1fr; }}
      .matrix-table {{ border: 0; background: transparent; }}
      .matrix-table thead {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }}
      .matrix-table tbody, .matrix-table tr, .matrix-table td {{ display: block; width: 100%; }}
      .matrix-table tr {{ margin-bottom: 12px; border: 1px solid var(--line); border-radius: 6px; background: #fff; overflow: hidden; }}
      .matrix-table td {{ display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 10px; padding: 8px 10px; border-bottom: 1px solid #e8ecef; }}
      .matrix-table td::before {{ content: attr(data-label); color: var(--muted); font-size: 11px; font-weight: 800; text-transform: uppercase; }}
      .matrix-table .capability-name {{ display: block; padding: 12px 10px; background: var(--panel); }}
      .matrix-table .capability-name::before {{ content: none; }}
    }}
    @media (max-width: 600px) {{
      header {{ padding: 22px 18px 18px; }}
      main {{ padding: 20px 18px 40px; gap: 24px; }}
      h1 {{ font-size: 25px; }}
      .focus {{ padding: 17px 16px; gap: 16px; }}
      .focus h2 {{ font-size: 20px; }}
      .focus-actions {{ display: grid; grid-template-columns: 1fr; }}
      .focus-actions a {{ width: 100%; }}
      .matrix-table td {{ grid-template-columns: 96px minmax(0, 1fr); }}
    }}
  </style>
</head>
<body>
  <a class="skip-link" href="#main-content">К основному содержанию</a>
  <header>
    <div class="page-shell">
      <h1>MIT 18.06 Skill Stack</h1>
      <p>Личная панель прогресса по Linear Algebra: текущий gate, проверенные материалы и полный индекс курса.</p>
      <div class="summary" aria-label="Сводка прогресса">
        <span class="pill">Навыки: {len(matrix)}</span>
        <span class="pill">PASS: {status_counts.get('PASS', 0)}</span>
        <span class="pill">WATCH: {status_counts.get('WATCH', 0)}</span>
        <span class="pill">TRAIN: {status_counts.get('TRAIN', 0)}</span>
        <span class="pill">NEW: {status_counts.get('NEW', 0)}</span>
        <span class="pill">Дней: {max((artifact_day(row) or 0 for row in generated_pdfs(artifacts)), default=0)}</span>
      </div>
    </div>
  </header>
  <main id="main-content" class="page-shell">
    {render_focus(artifacts)}
    <section aria-labelledby="materials-title">
      <h2 id="materials-title">Последние материалы</h2>
      <p class="section-intro">PDF за два последних дня; самые новые находятся сверху.</p>
      <div class="table-scroll">
        <table class="archive-table">
          <thead><tr><th>День</th><th>Тип</th><th>Название</th><th>Файл</th><th>Размер</th></tr></thead>
          <tbody>{render_generated_materials(artifacts, latest_day_count=2)}</tbody>
        </table>
      </div>
    </section>
    <section aria-labelledby="matrix-title">
      <h2 id="matrix-title">Прогресс по навыкам</h2>
      <div class="legend" aria-label="Обозначения статусов">
        <span>PASS - gate пройден</span><span>WATCH - нужен короткий ремонт</span><span>TRAIN - активная практика</span><span>NEW - ещё не начато</span>
      </div>
      <div class="table-scroll">
        <table class="matrix-table">
          <thead><tr><th>Навык</th><th>Статус</th><th>Уровень</th><th>Evidence</th><th>Следующий gate</th><th>Источники</th></tr></thead>
          <tbody>{render_matrix(matrix, gates)}</tbody>
        </table>
      </div>
    </section>
    <details>
      <summary>Course Map · {len(course)} занятий</summary>
      <p class="section-intro">Локальные материалы отмечены как LOCAL и доступны только на этой машине.</p>
      <div class="table-scroll">
        <table class="course-table">
          <thead><tr><th>Unit</th><th>Topic</th><th>Title</th><th>Video</th><th>SRT</th><th>PDF</th><th>Review</th><th>Problem set</th><th>Exam</th></tr></thead>
          <tbody>{render_course(course)}</tbody>
        </table>
      </div>
    </details>
    <details>
      <summary>Архив материалов и решений</summary>
      <div class="archive-grid">
        <section class="archive-full" aria-labelledby="pdf-archive-title">
          <h2 id="pdf-archive-title">Все PDF по дням</h2>
          <div class="table-scroll">
            <table class="archive-table">
              <thead><tr><th>День</th><th>Тип</th><th>Название</th><th>Файл</th><th>Размер</th></tr></thead>
              <tbody>{render_generated_materials(artifacts)}</tbody>
            </table>
          </div>
        </section>
        <section aria-labelledby="submissions-title">
          <h2 id="submissions-title">Submitted Work</h2>
          <div class="table-scroll">
            <table class="archive-table">
              <thead><tr><th>Название</th><th>Файл</th><th>Размер</th></tr></thead>
              <tbody>{render_submissions(artifacts)}</tbody>
            </table>
          </div>
        </section>
        <section aria-labelledby="sources-title">
          <h2 id="sources-title">Generated Sources</h2>
          <div class="table-scroll">
            <table class="archive-table">
              <thead><tr><th>День</th><th>Название</th><th>Файл</th><th>Размер</th></tr></thead>
              <tbody>{render_source_materials(artifacts)}</tbody>
            </table>
          </div>
        </section>
      </div>
    </details>
    <details>
      <summary>Технический инвентарь</summary>
      <div class="archive-grid">
        <section aria-labelledby="summary-title">
          <h2 id="summary-title">Artifact Summary</h2>
          <table><thead><tr><th>Категория</th><th>Количество</th></tr></thead><tbody>{render_artifact_summary(artifacts)}</tbody></table>
        </section>
        <section aria-labelledby="reviews-title">
          <h2 id="reviews-title">Review Notes</h2>
          <div class="table-scroll">
            <table class="archive-table"><thead><tr><th>Файл</th><th>Размер</th></tr></thead><tbody>{render_recent_reviews(artifacts)}</tbody></table>
          </div>
        </section>
      </div>
    </details>
  </main>
  <script>
    if (location.protocol === 'http:' || location.protocol === 'https:') {{
      document.querySelectorAll('[data-local-only="true"]').forEach((item) => {{
        item.removeAttribute('href');
        item.setAttribute('aria-disabled', 'true');
      }});
    }}
  </script>
</body>
</html>
"""


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_html(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
