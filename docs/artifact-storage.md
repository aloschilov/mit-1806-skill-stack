# Artifact Storage

This repo does not store MIT 18.06 videos, PDFs, SRT files, or Obsidian review notes. It stores a local index pointing to the source mirror:

```text
/Users/aloschilov/Obsidian/Math/DeepLearning/Books/18.06-spring-2010
```

The source mirror is expected to contain:

- lecture videos and subtitles in `download/`;
- OCW page and resource metadata in `pages/`, `resources/`, `data.json`, and `content_map.json`;
- PDFs and images in `static_resources/`;
- personal review notes in `review/`.

Regenerate the index with:

```bash
python3 scripts/import_ocw_manifest.py
```

Use the quick check when the mirror location changes or after a fresh download:

```bash
python3 scripts/import_ocw_manifest.py --check
```

Large MP4 files are indexed by path and size. The importer leaves their `sha256` field empty by default to keep routine imports fast. Use `--hash-large` if a full integrity pass is needed.

Generated study materials are small repo-owned artifacts and may be stored here:

```text
artifacts/generated/source/dayNN/  # Markdown sources with PDF front matter
artifacts/generated/tasks/         # printable assignment PDFs
artifacts/generated/answers/       # answer keys and checking accents
artifacts/generated/feedback_self/ # self-review feedback PDFs
artifacts/submissions/dayNN/       # submitted solution PDFs for evidence
```

There is no parent-feedback output folder for this stack. Feedback, when needed, should be self-review oriented and created only from actual completed work.

Generated and submitted files are indexed in `data/artifacts_manifest.csv` alongside source-mirror files. Routine imports keep these rows by scanning `artifacts/generated/` and `artifacts/submissions/`.
