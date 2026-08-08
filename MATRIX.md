# Capability Matrix: MIT 18.06 Personal Stack

Legend:

- `PASS` - gate passed with explicit evidence.
- `WATCH` - mostly usable, but needs transfer checks.
- `TRAIN` - needs targeted practice.
- `NEW` - not yet actively reviewed in this stack.

| Capability | Status | Level | Evidence | Next gate |
|---|---:|---:|---|---|
| Row operations, elimination, and LU | WATCH | 3/4 | Lecture 7 review uses elimination, echelon form, rank, and \(U\); earlier lecture PDFs are indexed. | Solve two systems by elimination and explain the row-operation meaning of each pivot. |
| Matrix multiplication, inverses, and transposes | TRAIN | 2/4 | Course sources for Lectures 2-5 are indexed, but no gated personal review is present yet. | Compute products, inverses, and \(A^T\) examples, then connect them to composition and row/column views. |
| Vector spaces and subspaces | PASS | 4/4 | Day 1 submitted work correctly classifies 10 candidate subsets with zero-vector and closure evidence. | Maintain through mixed rank and nullspace tasks. |
| Column space, nullspace, and solvability of \(Ax=b\) | PASS | 4/4 | Day 1 submitted work finds \(C(A)\), \(N(A)\), and solvability conditions for three Gate D matrices. | Maintain the distinction between a solvability condition on \(b\) and one example of \(b\). |
| RREF, rank, free variables, and special solutions | PASS | 4/4 | Day 2 submitted work reduces \(B_1\) and \(B_2\) to RREF, identifies pivot/free variables and rank, and writes special-solution bases for \(N(A)\). | Maintain precise language: rank is the number of pivots and free variables are counted by \(n-r\). |
| Complete solutions of \(Ax=b\) | PASS | 4/4 | Day 3 submitted work checks consistency, finds \(x_p\), writes complete solutions \(x=x_p+x_n\), and classifies the four rank cases. | Maintain the distinction between restrictions on \(b\) and free-variable directions in \(N(A)\). |
| Independence, span, basis, and dimension | WATCH | 3/4 | Day 4 work gets ranks, pivots, dependence, spans, and bases right; claim wording and the row-space distinction need one short repair. | Repair the two count-versus-dimension claims and distinguish preserved row space from changed column space. |
| Four fundamental subspaces | TRAIN | 2/4 | Lecture 10 rough notes exist; no explicit gate is recorded. | For two matrices, compute bases and dimensions for \(C(A)\), \(N(A)\), \(C(A^T)\), and \(N(A^T)\). |
| Orthogonality, projections, least squares, and \(QR\) | NEW | 0/4 | Lectures 14-17 are indexed, but no personal review evidence is recorded. | Solve a projection and least-squares problem and explain the normal equation \(A^TA\hat{x}=A^Tb\). |
| Determinants | NEW | 0/4 | Lectures 18-20 are indexed. | Compute determinants by row operations and cofactors, then explain volume scaling. |
| Eigenvalues, diagonalization, and applications | NEW | 0/4 | Lectures 21-24 are indexed. | Diagonalize a matrix when possible and use \(A^k\) or \(e^{At}\) in one application. |
| Symmetric and positive definite matrices | NEW | 0/4 | Lectures 25 and 27 are indexed. | Check positive definiteness using pivots, eigenvalues, and quadratic forms. |
| Complex matrices and FFT | NEW | 0/4 | Lecture 26 is indexed. | Explain complex inner products and compute one small Fourier matrix example. |
| Similar matrices and Jordan form | NEW | 0/4 | Lecture 28 is indexed. | Identify similarity invariants and describe when a Jordan form is needed. |
| SVD, change of basis, and image compression | NEW | 0/4 | Lectures 29-31 are indexed. | Compute an SVD for a small matrix and explain the rank-\(k\) approximation. |
| Linear transformations and pseudoinverse | NEW | 0/4 | Lectures 30 and 33 are indexed. | Build a matrix from a linear transformation and solve one pseudoinverse problem. |

## Current Conclusion

Gate C and Gate D have explicit Day 1 evidence, Gate E has explicit Day 2 evidence, and Gate F has explicit Day 3 evidence. Day 4 moves Gate G to WATCH: the computations are reliable, while two claim repairs and the row-space distinction remain active. Day 5 begins Gate H with complete four-subspace tables for two matrices.
