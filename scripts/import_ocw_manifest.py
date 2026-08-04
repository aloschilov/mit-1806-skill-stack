#!/usr/bin/env python3
"""Import local MIT 18.06 mirror metadata into repo CSV indexes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
GENERATED_ROOT = REPO_ROOT / "artifacts" / "generated"
SUBMISSIONS_ROOT = REPO_ROOT / "artifacts" / "submissions"
DEFAULT_SOURCE_ROOT = Path(
    "/Users/aloschilov/Obsidian/Math/DeepLearning/Books/18.06-spring-2010"
)
COURSE_MAP = DATA_DIR / "course_map.csv"
ARTIFACTS_MANIFEST = DATA_DIR / "artifacts_manifest.csv"
DEFAULT_MAX_HASH_BYTES = 50 * 1024 * 1024

COURSE_MAP_FIELDS = [
    "unit",
    "lecture",
    "title",
    "topic",
    "video_path",
    "srt_path",
    "lecture_pdf_path",
    "review_path",
    "problem_set_refs",
    "exam_refs",
]

ARTIFACT_FIELDS = [
    "category",
    "source_path",
    "bytes",
    "sha256",
    "title",
    "learning_resource_types",
]

CALENDAR_ROWS = [
    (1, "The geometry of linear equations", ""),
    (2, "Elimination with matrices", ""),
    (3, "Matrix operations and inverses", ""),
    (4, r"\(LU\) and \(LDU\) factorization", ""),
    (5, "Transposes and permutations", "Problem set 1 due"),
    (6, "Vector spaces and subspaces", ""),
    (7, r"The nullspace: solving \(Ax=0\)", ""),
    (8, r"Rectangular \(PA=LU\) and \(Ax=b\)", "Problem set 2 due"),
    (9, "Row reduced echelon form", ""),
    (10, "Basis and dimension", ""),
    (11, "The four fundamental subspaces", "Problem set 3 due"),
    (12, "Exam 1: Chapters 1 to 3.4", "Exam 1"),
    (13, "Graphs and networks", ""),
    (14, "Orthogonality", "Problem set 4 due"),
    (15, "Projections and subspaces", ""),
    (16, "Least squares approximations", ""),
    (17, r"Gram-Schmidt and \(A=QR\)", "Problem set 5 due"),
    (18, "Properties of determinants", ""),
    (19, "Formulas for determinants", ""),
    (20, "Applications of determinants", "Problem set 6 due"),
    (21, "Eigenvalues and eigenvectors", ""),
    (22, "Diagonalization", ""),
    (23, "Markov matrices", "Problem set 7 due"),
    (24, "Review for exam 2", ""),
    (25, "Exam 2: Chapters 1-5, 6.1-6.2, 8.2", "Exam 2"),
    (26, "Differential equations", ""),
    (27, "Symmetric matrices", ""),
    (28, "Positive definite matrices", ""),
    (29, "Matrices in engineering", "Problem set 8 due"),
    (30, "Similar matrices", ""),
    (31, "Singular value decomposition", "Problem set 9 due"),
    (32, "Fourier series, FFT, complex matrices", ""),
    (33, "Linear transformations", ""),
    (34, "Choice of basis", "Problem set 10 due"),
    (35, "Linear programming", ""),
    (36, "Course review", ""),
    (37, "Exam 3: Chapters 1-8", "Exam 3"),
    (38, "Numerical linear algebra", ""),
    (39, "Computational science", ""),
    (40, "Final exam", "Final exam"),
]

PSET_DUE_BY_UNIT = {
    5: 1,
    8: 2,
    11: 3,
    14: 4,
    17: 5,
    20: 6,
    23: 7,
    29: 8,
    31: 9,
    34: 10,
}

EXAM_BY_UNIT = {
    12: "exam1",
    25: "exam2",
    37: "exam3",
    40: "final",
}


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def maybe_hash(path: Path, *, hash_large: bool, max_hash_bytes: int) -> str:
    size = path.stat().st_size
    if not hash_large and size > max_hash_bytes:
        return ""
    return sha256(path)


def csv_write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def file_metadata_by_basename(source_root: Path) -> dict[str, dict[str, str]]:
    metadata: dict[str, dict[str, str]] = {}
    for data_file in sorted((source_root / "resources").glob("*/data.json")):
        try:
            data = read_json(data_file)
        except (OSError, json.JSONDecodeError):
            continue
        file_value = data.get("file") or ""
        if not file_value:
            continue
        basename = Path(file_value).name
        metadata[basename] = {
            "title": str(data.get("title") or basename),
            "learning_resource_types": ";".join(data.get("learning_resource_types") or []),
        }
    return metadata


def lecture_titles(source_root: Path) -> dict[int, str]:
    titles: dict[int, str] = {}
    for data_file in sorted((source_root / "resources").glob("lecture-*/data.json")):
        match = re.search(r"lecture-(\d+)-", str(data_file.parent.name))
        if not match:
            continue
        lecture = int(match.group(1))
        data = read_json(data_file)
        titles[lecture] = str(data.get("title") or f"Lecture {lecture}")
    return titles


def latexize_title(title: str) -> str:
    replacements = [
        ("A = LU", r"\(A=LU\)"),
        ("A = QR", r"\(A=QR\)"),
        ("Ax = 0", r"\(Ax=0\)"),
        ("Ax = b", r"\(Ax=b\)"),
        ("exp(At)", r"\(e^{At}\)"),
        ("R^n", r"\(\mathbb{R}^n\)"),
        (" form R", r" form \(R\)"),
    ]
    normalized = title
    for old, new in replacements:
        normalized = normalized.replace(old, new)
    return normalized


def lecture_pdf_paths(source_root: Path) -> dict[int, Path]:
    paths: dict[int, Path] = {}
    pattern = re.compile(r"MIT18_06S10_L(\d{2})\.pdf$", re.IGNORECASE)
    for pdf in sorted((source_root / "static_resources").glob("*.pdf")):
        match = pattern.search(pdf.name)
        if match:
            paths[int(match.group(1))] = pdf
    return paths


def problem_set_paths(source_root: Path) -> dict[int, Path]:
    paths: dict[int, Path] = {}
    pattern = re.compile(r"pset(\d+)_s10_soln?\.pdf$", re.IGNORECASE)
    for pdf in sorted((source_root / "static_resources").glob("*.pdf")):
        match = pattern.search(pdf.name)
        if match:
            paths[int(match.group(1))] = pdf
    return paths


def exam_paths(source_root: Path) -> dict[str, list[Path]]:
    exams = {"exam1": [], "exam2": [], "exam3": [], "final": []}
    for pdf in sorted((source_root / "static_resources").glob("*.pdf")):
        lower = pdf.name.lower()
        if "exam1" in lower:
            exams["exam1"].append(pdf)
        elif "exam2" in lower:
            exams["exam2"].append(pdf)
        elif "exam3" in lower:
            exams["exam3"].append(pdf)
        elif "final" in lower:
            exams["final"].append(pdf)
    return exams


def review_paths_for_unit(source_root: Path, unit: int) -> list[Path]:
    review_root = source_root / "review"
    paths: list[Path] = []
    main = review_root / f"Lecture {unit}.md"
    if main.exists():
        paths.append(main)
    segmented_readme = review_root / f"Lecture {unit}" / "README.md"
    if segmented_readme.exists():
        paths.append(segmented_readme)
    return paths


def join_paths(paths: list[Path]) -> str:
    return ";".join(str(path) for path in paths)


def build_course_map(source_root: Path) -> list[dict[str, str]]:
    titles = lecture_titles(source_root)
    lecture_pdfs = lecture_pdf_paths(source_root)
    psets = problem_set_paths(source_root)
    exams = exam_paths(source_root)
    rows: list[dict[str, str]] = []

    for unit, topic, _key_date in CALENDAR_ROWS:
        video = source_root / "download" / f"{unit:02d}.mp4"
        srt = source_root / "download" / f"{unit:02d}.srt"
        lecture_pdf = lecture_pdfs.get(unit)
        pset = psets.get(PSET_DUE_BY_UNIT.get(unit, -1))
        exam_refs = exams.get(EXAM_BY_UNIT.get(unit, ""), [])
        rows.append(
            {
                "unit": str(unit),
                "lecture": str(unit) if unit <= 34 else "",
                "title": latexize_title(titles.get(unit, f"Session {unit}: {topic}")),
                "topic": topic,
                "video_path": str(video) if video.exists() else "",
                "srt_path": str(srt) if srt.exists() else "",
                "lecture_pdf_path": str(lecture_pdf) if lecture_pdf else "",
                "review_path": join_paths(review_paths_for_unit(source_root, unit)),
                "problem_set_refs": str(pset) if pset else "",
                "exam_refs": join_paths(exam_refs),
            }
        )
    return rows


def artifact_category(path: Path, source_root: Path) -> str:
    rel = path.relative_to(source_root)
    if rel.parts[0] == "download" and path.suffix == ".mp4":
        return "download/video"
    if rel.parts[0] == "download" and path.suffix == ".srt":
        return "download/subtitle"
    if rel.parts[0] == "static_resources" and path.suffix.lower() == ".pdf":
        lower = path.name.lower()
        if "pset" in lower:
            return "static/pdf/problem-set-solution"
        if "exam" in lower or "final" in lower:
            return "static/pdf/exam"
        if "mit18_06s10_l" in lower:
            return "static/pdf/lecture-transcript"
        return "static/pdf/other"
    if rel.parts[0] == "static_resources" and path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
        return "static/image"
    if rel.parts[0] == "review" and path.suffix.lower() == ".md":
        return "review/markdown"
    if path.suffix.lower() == ".json":
        return "metadata/json"
    return "other"


def iter_manifest_files(source_root: Path) -> list[Path]:
    files: list[Path] = []
    files.extend(sorted((source_root / "download").glob("*.mp4")))
    files.extend(sorted((source_root / "download").glob("*.srt")))
    files.extend(sorted((source_root / "static_resources").glob("*.pdf")))
    files.extend(sorted((source_root / "static_resources").glob("*.jpg")))
    files.extend(sorted((source_root / "static_resources").glob("*.jpeg")))
    files.extend(sorted((source_root / "static_resources").glob("*.png")))
    files.extend(sorted((source_root / "review").rglob("*.md")))
    for rel in [
        "data.json",
        "content_map.json",
        "pages/calendar/data.json",
        "pages/assignments/data.json",
        "pages/exams/data.json",
    ]:
        path = source_root / rel
        if path.exists():
            files.append(path)
    return files


def build_manifest(
    source_root: Path, *, hash_large: bool, max_hash_bytes: int
) -> list[dict[str, str]]:
    file_meta = file_metadata_by_basename(source_root)
    rows: list[dict[str, str]] = []
    for path in iter_manifest_files(source_root):
        basename = path.name
        metadata = file_meta.get(basename, {})
        rows.append(
            {
                "category": artifact_category(path, source_root),
                "source_path": str(path),
                "bytes": str(path.stat().st_size),
                "sha256": maybe_hash(
                    path, hash_large=hash_large, max_hash_bytes=max_hash_bytes
                ),
                "title": metadata.get("title", basename),
                "learning_resource_types": metadata.get("learning_resource_types", ""),
            }
        )
    rows.extend(build_generated_manifest())
    rows.extend(build_submission_manifest())
    return rows


def parse_generated_front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
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


def generated_category(path: Path) -> str | None:
    rel = path.relative_to(REPO_ROOT)
    parts = rel.parts
    if parts[:3] == ("artifacts", "generated", "source") and path.suffix == ".md":
        return "generated/source"
    if parts[:3] == ("artifacts", "generated", "tasks") and path.suffix == ".pdf":
        return "generated/tasks"
    if parts[:3] == ("artifacts", "generated", "answers") and path.suffix == ".pdf":
        return "generated/answers"
    if parts[:3] == ("artifacts", "generated", "feedback_self") and path.suffix == ".pdf":
        return "generated/feedback_self"
    return None


def generated_learning_resource_type(category: str) -> str:
    return {
        "generated/source": "Generated source Markdown",
        "generated/tasks": "Generated assignment PDF",
        "generated/answers": "Generated answer key PDF",
        "generated/feedback_self": "Generated self-review PDF",
    }.get(category, "Generated artifact")


def iter_generated_manifest_files() -> list[Path]:
    if not GENERATED_ROOT.exists():
        return []
    files: list[Path] = []
    files.extend(sorted((GENERATED_ROOT / "source").glob("day*/*.md")))
    for name in ["tasks", "answers", "feedback_self"]:
        folder = GENERATED_ROOT / name
        if folder.exists():
            files.extend(sorted(folder.glob("*.pdf")))
    return files


def generated_output_titles() -> dict[Path, str]:
    titles: dict[Path, str] = {}
    source_root = GENERATED_ROOT / "source"
    if not source_root.exists():
        return titles
    for source in sorted(source_root.glob("day*/*.md")):
        metadata = parse_generated_front_matter(source)
        output = metadata.get("output")
        title = metadata.get("title")
        if not output or not title:
            continue
        titles[(REPO_ROOT / output).resolve()] = title
    return titles


def build_generated_manifest() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    output_titles = generated_output_titles()
    for path in iter_generated_manifest_files():
        category = generated_category(path)
        if category is None:
            continue
        metadata = parse_generated_front_matter(path) if path.suffix == ".md" else {}
        title = metadata.get("title") or output_titles.get(path.resolve()) or path.stem
        rows.append(
            {
                "category": category,
                "source_path": str(path.resolve()),
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
                "title": title,
                "learning_resource_types": generated_learning_resource_type(category),
            }
        )
    return rows


def build_submission_manifest() -> list[dict[str, str]]:
    if not SUBMISSIONS_ROOT.exists():
        return []
    rows: list[dict[str, str]] = []
    for path in sorted(SUBMISSIONS_ROOT.glob("day*/*.pdf")):
        rows.append(
            {
                "category": "submission/pdf",
                "source_path": str(path.resolve()),
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
                "title": path.stem,
                "learning_resource_types": "Submitted solution PDF",
            }
        )
    return rows


def count_files(source_root: Path) -> dict[str, int]:
    static = source_root / "static_resources"
    download = source_root / "download"
    review = source_root / "review"
    return {
        "videos": len(list(download.glob("*.mp4"))),
        "subtitles": len(list(download.glob("*.srt"))),
        "pdfs": len(list(static.glob("*.pdf"))),
        "pset_solutions": len(list(static.glob("*pset*.pdf"))),
        "exam_pdfs": len(
            [
                path
                for path in static.glob("*.pdf")
                if "exam" in path.name.lower() or "final" in path.name.lower()
            ]
        ),
        "review_markdown": len(list(review.rglob("*.md"))),
    }


def check_source(source_root: Path) -> None:
    required = [
        source_root / "data.json",
        source_root / "content_map.json",
        source_root / "pages" / "calendar" / "data.json",
        source_root / "pages" / "assignments" / "data.json",
        source_root / "pages" / "exams" / "data.json",
        source_root / "download",
        source_root / "static_resources",
        source_root / "review",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing required source paths:\n" + "\n".join(map(str, missing)))

    course = read_json(source_root / "data.json")
    if course.get("primary_course_number") != "18.06":
        raise SystemExit("source data.json is not MIT 18.06")
    if course.get("course_title") != "Linear Algebra":
        raise SystemExit("source data.json is not the expected Linear Algebra course")

    counts = count_files(source_root)
    expected = {
        "videos": 34,
        "subtitles": 34,
        "pdfs": 104,
        "pset_solutions": 10,
        "review_markdown": 60,
    }
    for key, value in expected.items():
        if counts[key] != value:
            raise SystemExit(f"{key}: expected {value}, found {counts[key]}")
    for exam_key in ["exam1", "exam2", "exam3", "final"]:
        if not exam_paths(source_root)[exam_key]:
            raise SystemExit(f"missing files for {exam_key}")

    print(
        "OK: source mirror has "
        f"{counts['videos']} videos, {counts['subtitles']} SRT files, "
        f"{counts['pdfs']} PDFs, {counts['pset_solutions']} pset solutions, "
        f"{counts['exam_pdfs']} exam/final PDFs, "
        f"{counts['review_markdown']} review Markdown files"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--check", action="store_true", help="validate source mirror only")
    parser.add_argument(
        "--hash-large",
        action="store_true",
        help="hash files larger than --max-hash-bytes, including MP4 files",
    )
    parser.add_argument(
        "--max-hash-bytes",
        type=int,
        default=DEFAULT_MAX_HASH_BYTES,
        help="maximum file size to hash unless --hash-large is set",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_root = args.source_root.expanduser().resolve()
    check_source(source_root)
    if args.check:
        return

    course_rows = build_course_map(source_root)
    manifest_rows = build_manifest(
        source_root,
        hash_large=args.hash_large,
        max_hash_bytes=args.max_hash_bytes,
    )
    csv_write(COURSE_MAP, COURSE_MAP_FIELDS, course_rows)
    csv_write(ARTIFACTS_MANIFEST, ARTIFACT_FIELDS, manifest_rows)
    print(f"Wrote {COURSE_MAP.relative_to(REPO_ROOT)} ({len(course_rows)} rows)")
    print(f"Wrote {ARTIFACTS_MANIFEST.relative_to(REPO_ROOT)} ({len(manifest_rows)} rows)")


if __name__ == "__main__":
    main()
