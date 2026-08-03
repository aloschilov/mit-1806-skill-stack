#!/usr/bin/env python3
"""Validate MIT 18.06 skill-stack CSV files."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ALLOWED_STATUS = {"PASS", "WATCH", "TRAIN", "NEW"}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

MATRIX_FIELDS = [
    "capability",
    "status",
    "level",
    "evidence",
    "next_gate",
    "source_refs",
]
GATE_FIELDS = ["gate_id", "capability", "criterion", "required_output", "source_refs"]
COURSE_FIELDS = [
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
MANIFEST_FIELDS = [
    "category",
    "source_path",
    "bytes",
    "sha256",
    "title",
    "learning_resource_types",
]


def read_csv(path: Path, expected_fields: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected_fields:
            raise SystemExit(
                f"{path.relative_to(ROOT)}: expected header {expected_fields}, "
                f"found {reader.fieldnames}"
            )
        return list(reader)


def split_refs(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def check_unique(rows: list[dict[str, str]], key: str, label: str) -> None:
    seen: set[str] = set()
    for row in rows:
        value = row[key]
        if not value:
            raise SystemExit(f"{label}: empty {key}")
        if value in seen:
            raise SystemExit(f"{label}: duplicate {key} {value!r}")
        seen.add(value)


def check_paths(values: list[str], label: str, *, skip: bool) -> None:
    if skip:
        return
    for value in values:
        if value and not Path(value).exists():
            raise SystemExit(f"{label}: source path does not exist: {value}")


def validate_matrix(skip_source_paths: bool) -> None:
    matrix = read_csv(DATA / "capability_matrix.csv", MATRIX_FIELDS)
    gates = read_csv(DATA / "gates.csv", GATE_FIELDS)
    course = read_csv(DATA / "course_map.csv", COURSE_FIELDS)
    manifest = read_csv(DATA / "artifacts_manifest.csv", MANIFEST_FIELDS)

    if not matrix:
        raise SystemExit("capability_matrix.csv is empty")
    if not gates:
        raise SystemExit("gates.csv is empty")

    check_unique(matrix, "capability", "capability_matrix.csv")
    check_unique(gates, "gate_id", "gates.csv")

    gates_by_id = {row["gate_id"]: row for row in gates}
    capabilities = {row["capability"] for row in matrix}

    for i, row in enumerate(matrix, start=2):
        status = row["status"]
        if status not in ALLOWED_STATUS:
            raise SystemExit(f"capability_matrix.csv line {i}: invalid status {status!r}")
        try:
            level = int(row["level"])
        except ValueError as exc:
            raise SystemExit(f"capability_matrix.csv line {i}: level must be int") from exc
        if not 0 <= level <= 4:
            raise SystemExit(f"capability_matrix.csv line {i}: level must be between 0 and 4")
        gate = gates_by_id.get(row["next_gate"])
        if gate is None:
            raise SystemExit(
                f"capability_matrix.csv line {i}: unknown gate {row['next_gate']!r}"
            )
        if gate["capability"] != row["capability"]:
            raise SystemExit(
                f"capability_matrix.csv line {i}: gate {row['next_gate']} belongs to "
                f"{gate['capability']}, not {row['capability']}"
            )
        check_paths(split_refs(row["source_refs"]), "capability_matrix.csv", skip=skip_source_paths)

    for i, row in enumerate(gates, start=2):
        if row["capability"] not in capabilities:
            raise SystemExit(f"gates.csv line {i}: unknown capability {row['capability']!r}")
        check_paths(split_refs(row["source_refs"]), "gates.csv", skip=skip_source_paths)

    for i, row in enumerate(course, start=2):
        try:
            unit = int(row["unit"])
        except ValueError as exc:
            raise SystemExit(f"course_map.csv line {i}: unit must be int") from exc
        if not 1 <= unit <= 40:
            raise SystemExit(f"course_map.csv line {i}: unit must be between 1 and 40")
        for field in [
            "video_path",
            "srt_path",
            "lecture_pdf_path",
            "review_path",
            "problem_set_refs",
            "exam_refs",
        ]:
            check_paths(split_refs(row[field]), "course_map.csv", skip=skip_source_paths)

    for i, row in enumerate(manifest, start=2):
        if not row["category"]:
            raise SystemExit(f"artifacts_manifest.csv line {i}: empty category")
        try:
            size = int(row["bytes"])
        except ValueError as exc:
            raise SystemExit(f"artifacts_manifest.csv line {i}: bytes must be int") from exc
        if size < 0:
            raise SystemExit(f"artifacts_manifest.csv line {i}: bytes must be non-negative")
        if row["sha256"] and not SHA_RE.match(row["sha256"]):
            raise SystemExit(f"artifacts_manifest.csv line {i}: invalid sha256")
        check_paths([row["source_path"]], "artifacts_manifest.csv", skip=skip_source_paths)

    print(
        "OK: "
        f"{len(matrix)} capabilities, {len(gates)} gates, "
        f"{len(course)} course rows, {len(manifest)} artifacts"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-source-paths",
        action="store_true",
        help="skip absolute source path existence checks for CI environments",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_matrix(skip_source_paths=args.skip_source_paths)


if __name__ == "__main__":
    main()

