---
title: "День 2. Обратная связь"
subtitle: "MIT 18.06. RREF, rank, free variables, special solutions."
output: "artifacts/generated/feedback_self/day02_feedback.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Итог: День 2 засчитан. Gate E можно считать пройденным: RREF, rank, pivot/free variables и special solutions применены к двум прямоугольным матрицам.

# Глоссарий

- Приведённая ступенчатая форма RREF (reduced row echelon form) - форма, где pivot positions, free variables и zero rows видны сразу.
- Ранг \(r\) (rank) - число pivot columns в RREF.
- Опорный столбец (pivot column) - столбец с pivot; для \(C(A)\) берётся из исходной матрицы.
- Свободная переменная (free variable) - переменная без pivot, которую задают параметром.
- Специальное решение (special solution) - базисный вектор \(N(A)\), полученный из одной выбранной free variable.
- Проверка размерности (dimension check) - сравнение \(\dim N(A)\) с \(n-r\).

# Что получилось хорошо

- Быстрый ремонт со Дня 1 выполнен правильно: три правые части проверены через условие на последовательные разности.
- Для \(B_1\) RREF найден верно:

\[
R_1=
\begin{bmatrix}
1 & 2 & 0 & -1\\
0 & 0 & 1 & 1\\
0 & 0 & 0 & 0
\end{bmatrix}.
\]

- Для \(B_1\) правильно указаны pivot variables \(x_1,x_3\), free variables \(x_2,x_4\), rank \(r=2\), а также базис \(N(B_1)\).
- Для \(B_2\) RREF, pivot variables \(x_1,x_2\), free variables \(x_3,x_4,x_5\), rank \(r=2\) и три special solutions совпали с ключом.
- Concept check в целом сильный: особенно идея, что pivot columns для \(C(A)\) надо брать из исходной матрицы, потому что row operations меняют сами столбцы.

# Что поправить

1. Rank лучше определять не как "размер единичной матрицы", а как число pivots:

\[
r=\#\{\text{pivot columns}\}.
\]

2. Для числа free variables каждый раз пиши общий принцип:

\[
\#\{\text{free variables}\}=n-r.
\]

Например, для \(B_2\): \(n=5\), \(r=2\), значит \(5-2=3\).

3. Для \(N(A)\) самый чистый формат - через span:

\[
N(A)=\operatorname{span}\{v_1,v_2,\ldots\}.
\]

Запись через параметры тоже верна, но span сразу показывает базис.

4. В special solutions явно называй, какая free variable выбрана равной \(1\). Это помогает не терять знаки в длинных матрицах.

# Status gates

- Gate C: PASS.
- Gate D: PASS.
- Gate E: PASS.
- Следующий фокус: Gate F, то есть complete solutions of \(Ax=b\), \(x=x_p+x_n\), совместность и четыре rank cases.
