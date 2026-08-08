---
title: "День 5. Ответы и акценты"
subtitle: "MIT 18.06. Gate H: four fundamental subspaces."
output: "artifacts/generated/answers/day05_answers_and_checks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Проверочный акцент: column space и left nullspace находятся в \(\mathbb{R}^m\); row space и nullspace находятся в \(\mathbb{R}^n\).

# Глоссарий

- \(C(A)\) - column space, basis из pivot columns исходной \(A\).
- \(N(A)\) - nullspace, basis из special solutions системы \(Ax=0\).
- \(C(A^T)\) - row space, basis из ненулевых строк \(R\).
- \(N(A^T)\) - left nullspace, basis из решений \(A^Ty=0\).
- Rank-nullity - разложение общей dimension на rank и nullity.

# 0. Быстрый ремонт со Дня 4

1. Больше \(m\) векторов в \(\mathbb{R}^m\) обязательно dependent, но они могут породить всё пространство. Пример: \(e_1,e_2,e_3,e_1+e_2\) в \(\mathbb{R}^3\).
2. Меньше \(m\) векторов в \(\mathbb{R}^m\) не могут породить всё пространство, но могут быть independent. Пример: \(e_1,e_2\) в \(\mathbb{R}^3\).
3. Row operations сохраняют row space и обычно меняют column space.
4. Row operations меняют сами столбцы, поэтому basis \(C(A)\) берём из исходной \(A\). Новые строки являются обратимыми линейными комбинациями старых, поэтому row space сохраняется и его basis можно читать из \(R\).

# 1. Карта четырёх пространств

1. \(C(A)\subset\mathbb{R}^m\), dimension \(r\), basis из pivot columns исходной \(A\).
2. \(N(A)\subset\mathbb{R}^n\), dimension \(n-r\), basis из special solutions системы \(Ax=0\).
3. \(C(A^T)\subset\mathbb{R}^n\), dimension \(r\), basis из ненулевых строк \(R\).
4. \(N(A^T)\subset\mathbb{R}^m\), dimension \(m-r\), basis из решений \(A^Ty=0\).

# 2. Матрица из Lecture 10

Матрица \(A\) имеет размер \(3\times4\), поэтому \(m=3\), \(n=4\).

\[
A\sim
R=
\begin{bmatrix}
1&0&1&1\\
0&1&1&0\\
0&0&0&0
\end{bmatrix}.
\]

Pivot columns: \(1,2\). Rank: \(r=2\).

## Column space \(C(A)\subset\mathbb{R}^3\)

\[
\operatorname{basis}C(A)=
\left\{
\begin{bmatrix}1\\1\\1\end{bmatrix},
\begin{bmatrix}2\\1\\2\end{bmatrix}
\right\},
\qquad
\dim C(A)=2.
\]

## Nullspace \(N(A)\subset\mathbb{R}^4\)

Из \(R x=0\):

\[
x_1=-x_3-x_4,
\qquad
x_2=-x_3.
\]

\[
\operatorname{basis}N(A)=
\left\{
\begin{bmatrix}-1\\-1\\1\\0\end{bmatrix},
\begin{bmatrix}-1\\0\\0\\1\end{bmatrix}
\right\},
\qquad
\dim N(A)=2.
\]

## Row space \(C(A^T)\subset\mathbb{R}^4\)

\[
\operatorname{basis}C(A^T)=
\left\{
\begin{bmatrix}1\\0\\1\\1\end{bmatrix},
\begin{bmatrix}0\\1\\1\\0\end{bmatrix}
\right\},
\qquad
\dim C(A^T)=2.
\]

## Left nullspace \(N(A^T)\subset\mathbb{R}^3\)

Первая и третья строки \(A\) совпадают, поэтому:

\[
\operatorname{basis}N(A^T)=
\left\{
\begin{bmatrix}-1\\0\\1\end{bmatrix}
\right\},
\qquad
\dim N(A^T)=1.
\]

Проверки:

\[
r+(n-r)=2+2=4=n,
\qquad
r+(m-r)=2+1=3=m.
\]

# 3. Вторая полная таблица

Матрица \(B\) имеет размер \(4\times3\), поэтому \(m=4\), \(n=3\).

\[
B\sim
R=
\begin{bmatrix}
1&0&1\\
0&1&1\\
0&0&0\\
0&0&0
\end{bmatrix}.
\]

Pivot columns: \(1,2\). Rank: \(r=2\).

## Column space \(C(B)\subset\mathbb{R}^4\)

\[
\operatorname{basis}C(B)=
\left\{
\begin{bmatrix}1\\0\\1\\1\end{bmatrix},
\begin{bmatrix}0\\1\\1\\-1\end{bmatrix}
\right\},
\qquad
\dim C(B)=2.
\]

## Nullspace \(N(B)\subset\mathbb{R}^3\)

\[
\operatorname{basis}N(B)=
\left\{
\begin{bmatrix}-1\\-1\\1\end{bmatrix}
\right\},
\qquad
\dim N(B)=1.
\]

## Row space \(C(B^T)\subset\mathbb{R}^3\)

\[
\operatorname{basis}C(B^T)=
\left\{
\begin{bmatrix}1\\0\\1\end{bmatrix},
\begin{bmatrix}0\\1\\1\end{bmatrix}
\right\},
\qquad
\dim C(B^T)=2.
\]

## Left nullspace \(N(B^T)\subset\mathbb{R}^4\)

\[
\operatorname{basis}N(B^T)=
\left\{
\begin{bmatrix}-1\\-1\\1\\0\end{bmatrix},
\begin{bmatrix}-1\\1\\0\\1\end{bmatrix}
\right\},
\qquad
\dim N(B^T)=2.
\]

Проверки:

\[
r+(n-r)=2+1=3=n,
\qquad
r+(m-r)=2+2=4=m.
\]

# 4. Смысловые проверки

1. Каждая новая строка получается как линейная комбинация старых, а элементарные row operations обратимы. Поэтому старые и новые строки порождают одно пространство.
2. Ненулевые строки \(R\) independent из-за разных pivot positions и порождают row space, которое row operations сохранили.
3. Pivot columns исходной \(A\) дают \(r\) basis vectors для \(C(A)\), а ненулевые строки \(R\) дают \(r\) basis vectors для \(C(A^T)\).
4. Вектор \(y\in N(A^T)\) задаёт зависимость строк: \(y^TA=0^T\).
5. В \(Ax=0\) вектор \(x\) имеет \(n\) компонент. В \(A^Ty=0\) вектор \(y\) имеет \(m\) компонент.
