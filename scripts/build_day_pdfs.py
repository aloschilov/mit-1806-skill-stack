#!/usr/bin/env python3
"""Build MIT 18.06 day PDFs from Markdown with Pandoc and XeLaTeX."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "artifacts" / "generated" / "source"
TEMPLATE = ROOT / "templates" / "day-material.tex"
MANIFEST = ROOT / "data" / "artifacts_manifest.csv"
PREVIEW_ROOT = ROOT / "tmp" / "pdfs" / "rendered_check"
RAW_LATEX_RE = re.compile(
    r"\\\(|\\\)|\\\[|\\\]|\\(?:mathbb|operatorname|Rightarrow|begin|end|cdot|le|ge)"
)
MANIFEST_FIELDS = [
    "category",
    "source_path",
    "bytes",
    "sha256",
    "title",
    "learning_resource_types",
]


@dataclass(frozen=True)
class SourceDoc:
    source: Path
    output: Path
    metadata: dict[str, str]


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required tool is missing: {name}")


def parse_front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path.relative_to(ROOT)}: missing YAML front matter")

    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise SystemExit(
                f"{path.relative_to(ROOT)}: unsupported front matter line: {line!r}"
            )
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        values[key.strip()] = value
    return values


def source_dir_for_day(day: int) -> Path:
    padded = SOURCE_ROOT / f"day{day:02d}"
    if padded.is_dir():
        return padded
    unpadded = SOURCE_ROOT / f"day{day}"
    if unpadded.is_dir():
        return unpadded
    raise SystemExit(f"Source directory not found: {padded.relative_to(ROOT)}")


def source_docs_for_day(day: int) -> list[SourceDoc]:
    day_dir = source_dir_for_day(day)
    docs: list[SourceDoc] = []
    for source in sorted(day_dir.glob("*.md")):
        metadata = parse_front_matter(source)
        raw_output = metadata.get("output")
        if not raw_output:
            raise SystemExit(f"{source.relative_to(ROOT)}: front matter must define output")
        output = (ROOT / raw_output).resolve()
        try:
            output.relative_to(ROOT)
        except ValueError as exc:
            raise SystemExit(
                f"{source.relative_to(ROOT)}: output must stay inside repo"
            ) from exc
        if not output.suffix.lower() == ".pdf":
            raise SystemExit(f"{source.relative_to(ROOT)}: output must be a PDF")
        docs.append(SourceDoc(source=source, output=output, metadata=metadata))
    if not docs:
        raise SystemExit(f"No Markdown sources found in {day_dir.relative_to(ROOT)}")
    return docs


def build_pdf(doc: SourceDoc) -> None:
    doc.output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "pandoc",
        str(doc.source),
        "--standalone",
        "--from",
        "markdown+tex_math_single_backslash+fenced_divs",
        "--template",
        str(TEMPLATE),
        "--pdf-engine=xelatex",
        "--output",
        str(doc.output),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def pdf_text(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def assert_rendered_formulas(paths: list[Path]) -> None:
    failed = False
    for path in paths:
        text = pdf_text(path)
        match = RAW_LATEX_RE.search(text)
        if match:
            print(
                f"FAIL raw LaTeX marker remains in {path.relative_to(ROOT)}: "
                f"{match.group(0)!r}",
                file=sys.stderr,
            )
            failed = True
        else:
            print(f"OK no raw LaTeX markers: {path.relative_to(ROOT)}")
    if failed:
        raise SystemExit(1)


def assert_pdf_has_pages(paths: list[Path]) -> None:
    for path in paths:
        result = subprocess.run(
            ["pdfinfo", str(path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
        if not match or int(match.group(1)) < 1:
            raise SystemExit(f"{path.relative_to(ROOT)}: PDF has no pages")
        print(f"OK pages={match.group(1)}: {path.relative_to(ROOT)}")


def render_previews(paths: list[Path]) -> None:
    PREVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    for path in paths:
        prefix = PREVIEW_ROOT / path.stem
        subprocess.run(
            ["pdftoppm", "-png", "-r", "120", str(path), str(prefix)],
            cwd=ROOT,
            check=True,
        )
        print(f"Rendered preview: {prefix.name}-*.png")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_category(path: Path) -> str | None:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if parts[:3] == ("artifacts", "generated", "tasks"):
        return "generated/tasks"
    if parts[:3] == ("artifacts", "generated", "answers"):
        return "generated/answers"
    if parts[:3] == ("artifacts", "generated", "feedback_self"):
        return "generated/feedback_self"
    if parts[:3] == ("artifacts", "generated", "source"):
        return "generated/source"
    return None


def learning_resource_type(category: str, path: Path) -> str:
    if category == "generated/tasks":
        return "Generated assignment PDF"
    if category == "generated/answers":
        return "Generated answer key PDF"
    if category == "generated/feedback_self":
        return "Generated self-review PDF"
    if path.suffix.lower() == ".md":
        return "Generated source Markdown"
    return "Generated artifact"


def title_for_path(path: Path, metadata_by_output: dict[Path, dict[str, str]]) -> str:
    if path.suffix.lower() == ".md":
        return parse_front_matter(path).get("title") or path.stem
    metadata = metadata_by_output.get(path.resolve(), {})
    return metadata.get("title") or path.stem


def manifest_row(
    path: Path, metadata_by_output: dict[Path, dict[str, str]]
) -> dict[str, str]:
    category = manifest_category(path)
    if category is None:
        raise SystemExit(f"No manifest category rule for {path.relative_to(ROOT)}")
    return {
        "category": category,
        "source_path": str(path.resolve()),
        "bytes": str(path.stat().st_size),
        "sha256": sha256(path),
        "title": title_for_path(path, metadata_by_output),
        "learning_resource_types": learning_resource_type(category, path),
    }


def update_manifest(docs: list[SourceDoc]) -> None:
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST.relative_to(ROOT)}")
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != MANIFEST_FIELDS:
            raise SystemExit(
                f"{MANIFEST.relative_to(ROOT)}: expected header {MANIFEST_FIELDS}, "
                f"found {reader.fieldnames}"
            )
        rows = list(reader)

    metadata_by_output = {doc.output.resolve(): doc.metadata for doc in docs}
    paths = [doc.source for doc in docs] + [doc.output for doc in docs]
    updates = {
        str(path.resolve()): manifest_row(path, metadata_by_output) for path in paths
    }

    next_rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        source_path = row["source_path"]
        if source_path in updates:
            next_rows.append(updates[source_path])
            seen.add(source_path)
        else:
            next_rows.append(row)
    for source_path in sorted(set(updates) - seen):
        next_rows.append(updates[source_path])

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(next_rows)
    print(f"Updated manifest: {MANIFEST.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", type=int, required=True, help="day number to build")
    parser.add_argument(
        "--update-manifest",
        action="store_true",
        help="update data/artifacts_manifest.csv for sources and outputs",
    )
    parser.add_argument(
        "--render-preview",
        action="store_true",
        help="render PNG previews to tmp/pdfs/rendered_check for visual QA",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for tool in ["pandoc", "xelatex", "pdftotext", "pdfinfo"]:
        require_tool(tool)
    if args.render_preview:
        require_tool("pdftoppm")

    docs = source_docs_for_day(args.day)
    for doc in docs:
        print(
            f"Building {doc.output.relative_to(ROOT)} "
            f"from {doc.source.relative_to(ROOT)}"
        )
        build_pdf(doc)

    outputs = [doc.output for doc in docs]
    assert_pdf_has_pages(outputs)
    assert_rendered_formulas(outputs)

    if args.render_preview:
        render_previews(outputs)
    if args.update_manifest:
        update_manifest(docs)


if __name__ == "__main__":
    main()
