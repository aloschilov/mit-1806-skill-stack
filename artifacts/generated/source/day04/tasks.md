---
title: "День 4. Independence, span, basis, dimension"
subtitle: "MIT 18.06. Время: 75-105 минут."
output: "artifacts/generated/tasks/day04_tasks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Цель дня: научиться классифицировать наборы векторов через rank: independent или dependent, span или не span, basis или не basis, и какая dimension у span.

# Глоссарий

- Линейная независимость (linear independence) - только нулевая линейная комбинация даёт нулевой вектор.
- Линейная зависимость (linear dependence) - есть ненулевая линейная комбинация, которая даёт нулевой вектор.
- Span (линейная оболочка) - все линейные комбинации заданных векторов.
- Basis (базис) - набор, который одновременно independent и spans the space.
- Dimension (размерность) - число векторов в любом basis данного пространства.
- Rank test (проверка через rank) - если векторы стоят столбцами матрицы, их span имеет dimension \(r\).

Опора по курсу: Lecture 9 вводит independence, spanning, basis и dimension, а также связывает эти понятия с pivot columns, rank и nullspace.

# 0. Быстрый ремонт со Дня 3

Ответь коротко:

1. Почему при full column rank нет free variables?
2. Может ли при full column rank быть zero row после elimination, если \(m>n\)?
3. Запиши общий шаблон complete solution:

\[
x=\_\_\_+\_\_\_.
\]

# 1. Один matrix pass

Пусть столбцы матрицы \(A\) - это \(a_1,a_2,a_3,a_4\):

\[
A=
\begin{bmatrix}
1 & 0 & 1 & 1\\
0 & 1 & 1 & 1\\
1 & 1 & 2 & 0
\end{bmatrix}.
\]

Задания:

1. Приведи \(A\) к RREF \(R\).
2. Укажи pivot columns и free columns.
3. Найди одну линейную зависимость между \(a_1,a_2,a_3,a_4\).
4. Найди rank \(r\).
5. Являются ли четыре столбца independent?
6. Span-ят ли эти столбцы всё \(\mathbb{R}^3\)?
7. Выбери basis для \(C(A)\) из исходных столбцов \(A\).
8. Чему равна dimension \(C(A)\)?

# 2. Пять наборов векторов

Для каждого набора:

- поставь векторы столбцами матрицы;
- найди rank;
- реши: independent или dependent;
- реши: spans ambient space или нет;
- реши: basis или нет;
- запиши dimension of span.

## \(S_1\subset\mathbb{R}^3\)

\[
S_1=
\left\{
\begin{bmatrix}1\\0\\1\end{bmatrix},
\begin{bmatrix}0\\1\\1\end{bmatrix},
\begin{bmatrix}1\\1\\2\end{bmatrix}
\right\}.
\]

## \(S_2\subset\mathbb{R}^3\)

\[
S_2=
\left\{
\begin{bmatrix}1\\0\\0\end{bmatrix},
\begin{bmatrix}0\\1\\0\end{bmatrix},
\begin{bmatrix}0\\0\\1\end{bmatrix}
\right\}.
\]

## \(S_3\subset\mathbb{R}^2\)

\[
S_3=
\left\{
\begin{bmatrix}1\\2\end{bmatrix},
\begin{bmatrix}2\\4\end{bmatrix}
\right\}.
\]

## \(S_4\subset\mathbb{R}^3\)

\[
S_4=
\left\{
\begin{bmatrix}1\\0\\0\end{bmatrix},
\begin{bmatrix}0\\1\\0\end{bmatrix},
\begin{bmatrix}0\\0\\1\end{bmatrix},
\begin{bmatrix}1\\1\\1\end{bmatrix}
\right\}.
\]

## \(S_5\subset\mathbb{R}^4\)

\[
S_5=
\left\{
\begin{bmatrix}1\\0\\1\\0\end{bmatrix},
\begin{bmatrix}0\\1\\1\\0\end{bmatrix},
\begin{bmatrix}0\\0\\0\\1\end{bmatrix}
\right\}.
\]

# 3. Claim repair

Исправь две фразы так, чтобы они стали точными:

1. "Если векторов больше, чем координат, они не могут span-ить пространство."
2. "Если векторов меньше, чем координат, они всегда dependent."

Для каждой фразы дай один короткий counterexample или объяснение.

# 4. Выбери basis

1. Из набора \(\{a_1,a_2,a_3,a_4\}\) из раздела 1 выбери basis для \(C(A)\).
2. Из \(S_4\) выбери три вектора, которые всё ещё span-ят \(\mathbb{R}^3\).
3. Из \(S_1\) выбери basis для \(\operatorname{span}(S_1)\).

# 5. Concept check

Ответь коротко:

1. Как увидеть dependence через \(N(A)\)?
2. Как увидеть, что столбцы span-ят \(\mathbb{R}^m\)?
3. Когда набор векторов является basis для \(\mathbb{R}^m\)?
4. Почему dimension of column space равна rank?
5. Почему pivot columns для basis надо брать из исходной матрицы, а не из \(R\)?

# 6. Формат результата

Минимальный состав:

- RREF для матрицы \(A\);
- классификация пяти наборов \(S_1,\ldots,S_5\);
- три выбранных basis в разделе 4;
- ответы на пять concept-check вопросов;
- список ошибок, если где-то пришлось исправлять rank, pivots или зависимость.
