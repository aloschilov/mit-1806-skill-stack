---
title: "День 2. Ответы и акценты"
subtitle: "MIT 18.06. Gate E: RREF, rank, free variables."
output: "artifacts/generated/answers/day02_answers_and_checks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Проверочный акцент: сначала RREF, затем rank, затем свободные переменные, затем special solutions. Не наоборот.

# 0. Быстрый ремонт со Дня 1

Для лекционной матрицы условие разрешимости:

\[
b_2-b_1=b_3-b_2=b_4-b_3.
\]

1. \(b=(4,6,8,10)\): да, потому что \(2=2=2\).
2. \(b=(1,2,4,8)\): нет, потому что \(1,2,4\) не одинаковы.
3. \(b=(0,1,2,3)\): да, потому что \(1=1=1\).

# 1. Матрица \(B_1\)

\[
B_1=
\begin{bmatrix}
1 & 2 & 1 & 0\\
2 & 4 & 3 & 1\\
1 & 2 & 2 & 1
\end{bmatrix}.
\]

RREF:

\[
R_1=
\begin{bmatrix}
1 & 2 & 0 & -1\\
0 & 0 & 1 & 1\\
0 & 0 & 0 & 0
\end{bmatrix}.
\]

Pivot columns: \(1,3\). Free columns: \(2,4\).

Pivot variables: \(x_1,x_3\). Free variables: \(x_2,x_4\).

Rank:

\[
r=2.
\]

Из \(R_1x=0\):

\[
x_1+2x_2-x_4=0,
\qquad
x_3+x_4=0.
\]

Пусть \(x_2=s\), \(x_4=t\). Тогда:

\[
x=
s
\begin{bmatrix}-2\\1\\0\\0\end{bmatrix}
+t
\begin{bmatrix}1\\0\\-1\\1\end{bmatrix}.
\]

Значит:

\[
N(B_1)=
\operatorname{span}\left\{
\begin{bmatrix}-2\\1\\0\\0\end{bmatrix},
\begin{bmatrix}1\\0\\-1\\1\end{bmatrix}
\right\}.
\]

Проверка размерности:

\[
\dim N(B_1)=2=4-2=n-r.
\]

# 2. Матрица \(B_2\)

\[
B_2=
\begin{bmatrix}
1 & 0 & 2 & -1 & 3\\
0 & 1 & -1 & 2 & 1\\
1 & 1 & 1 & 1 & 4\\
2 & 1 & 3 & 0 & 7
\end{bmatrix}.
\]

RREF:

\[
R_2=
\begin{bmatrix}
1 & 0 & 2 & -1 & 3\\
0 & 1 & -1 & 2 & 1\\
0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0
\end{bmatrix}.
\]

Pivot columns: \(1,2\). Free columns: \(3,4,5\).

Pivot variables: \(x_1,x_2\). Free variables: \(x_3,x_4,x_5\).

Rank:

\[
r=2.
\]

Из \(R_2x=0\):

\[
x_1+2x_3-x_4+3x_5=0,
\qquad
x_2-x_3+2x_4+x_5=0.
\]

Пусть \(x_3=s\), \(x_4=t\), \(x_5=u\). Тогда:

\[
x=
s
\begin{bmatrix}-2\\1\\1\\0\\0\end{bmatrix}
+t
\begin{bmatrix}1\\-2\\0\\1\\0\end{bmatrix}
+u
\begin{bmatrix}-3\\-1\\0\\0\\1\end{bmatrix}.
\]

Значит:

\[
N(B_2)=
\operatorname{span}\left\{
\begin{bmatrix}-2\\1\\1\\0\\0\end{bmatrix},
\begin{bmatrix}1\\-2\\0\\1\\0\end{bmatrix},
\begin{bmatrix}-3\\-1\\0\\0\\1\end{bmatrix}
\right\}.
\]

Проверка размерности:

\[
\dim N(B_2)=3=5-2=n-r.
\]

# 3. Concept check

1. Pivot columns для \(C(A)\) надо брать из исходной матрицы, потому что row operations меняют column space. Они сохраняют зависимости между столбцами, но не сами столбцы.
2. Свободных переменных \(n-r\), потому что всего \(n\) переменных, а pivot variables ровно \(r\).
3. Special solution - это решение \(Ax=0\), где одна free variable равна \(1\), остальные free variables равны \(0\).
4. Если rank равен \(n\), свободных переменных нет, поэтому \(N(A)=\{0\}\).
5. Если rank меньше \(n\), есть хотя бы одна свободная переменная. Положив её равной \(1\), получаем ненулевое решение в \(N(A)\).
