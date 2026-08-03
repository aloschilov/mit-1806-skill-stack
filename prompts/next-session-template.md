# Prompt Template For The Next Session

```text
Continue the MIT 18.06 personal skill-stack.

Source mirror:
/Users/aloschilov/Obsidian/Math/DeepLearning/Books/18.06-spring-2010

Use this repo as the progress tracker:
/Users/aloschilov/training-workspace/mit-1806-skill-stack

Task:
1. Inspect the current capability matrix and gates.
2. Pick the next smallest concept gate that should move from TRAIN/WATCH toward PASS.
3. Use the local source mirror and existing review notes as evidence.
4. Create or update Markdown-first study materials in this repo only.
5. Keep all new math in LaTeX notation, for example \(Ax=b\), \(C(A)\), \(N(A)\), \(A^T\), and \(A^TA\hat{x}=A^Tb\).
6. Do not edit the Obsidian source mirror unless explicitly asked.
7. Run:
   python3 scripts/import_ocw_manifest.py --check
   python3 scripts/validate_matrix.py
   python3 scripts/generate_dashboard.py
   git diff --check
```

