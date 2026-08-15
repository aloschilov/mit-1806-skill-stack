---
title: "День 6. Пространства матриц и rank-one matrices"
subtitle: "MIT 18.06. Lecture 11. Время: 90-120 минут."
output: "artifacts/generated/tasks/day06_tasks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Цель дня: рассматривать сами матрицы как векторы, находить sum и intersection подпространств и распознавать rank-one matrices в форме \(uv^T\).

# Глоссарий

- Matrix space (пространство матриц) - векторное пространство, элементами которого являются матрицы одного размера.
- Symmetric matrix (симметричная матрица) - матрица \(A\), для которой \(A^T=A\).
- Upper triangular matrix (верхнетреугольная матрица) - матрица с нулями ниже главной диагонали.
- Diagonal matrix (диагональная матрица) - матрица с нулями вне главной диагонали.
- Intersection (пересечение) - \(S\cap U\), элементы, принадлежащие одновременно \(S\) и \(U\).
- Sum of subspaces (сумма подпространств) - \(S+U=\{s+u:s\in S,\ u\in U\}\).
- Rank-one matrix (матрица ранга 1) - ненулевая матрица, которую можно записать как \(uv^T\).
- Outer product (внешнее произведение) - произведение столбца \(u\) на строку \(v^T\).

Опора по курсу: Lecture 11 рассматривает пространство всех матриц, symmetric и upper triangular subspaces, формулу dimensions для sum/intersection и представление rank-one matrix как \(uv^T\).

# 0. Короткий ремонт со Дня 5

1. Для матрицы \(A\) из Дня 5 объясни одной строкой смысл

\[
y=\begin{bmatrix}-1\\0\\1\end{bmatrix}\in N(A^T).
\]

2. Заверши доказательство: ненулевые строки RREF образуют basis row space, потому что они одновременно … и … .

# 1. Пространство всех матриц \(2\times2\)

Пусть \(M=M_{2\times2}\) - пространство всех вещественных матриц размера \(2\times2\).

1. Запиши произвольный элемент \(M\) через четыре параметра.
2. Построй standard basis \(E_{11},E_{12},E_{21},E_{22}\).
3. Укажи \(\dim M\).
4. Объясни, почему координатами матрицы в этом basis являются её четыре entries.

# 2. Symmetric, upper triangular и diagonal

Внутри \(M_{2\times2}\) рассмотрим

\[
S=\left\{
\begin{bmatrix}a&b\\b&d\end{bmatrix}:a,b,d\in\mathbb{R}
\right\},
\qquad
U=\left\{
\begin{bmatrix}a&b\\0&d\end{bmatrix}:a,b,d\in\mathbb{R}
\right\}.
\]

1. Построй basis и найди dimension для \(S\) и \(U\).
2. Найди \(S\cap U\), его basis и dimension.
3. Покажи, что \(S\cup U\) не является subspace: подбери две матрицы из union, сумма которых не лежит в union.
4. Покажи, что \(S+U=M_{2\times2}\). Достаточно получить все четыре standard basis matrices из элементов \(S\) и \(U\).
5. Проверь формулу

\[
\dim S+\dim U
=
\dim(S\cap U)+\dim(S+U).
\]

# 3. Размерности в \(M_{3\times3}\)

Без длинного elimination ответь для вещественных матриц размера \(3\times3\).

1. Какова dimension пространства всех матриц?
2. Какова dimension symmetric subspace? Перечисли позиции свободных entries.
3. Какова dimension upper triangular subspace?
4. Какова dimension diagonal subspace?
5. Проверь формулу dimensions для symmetric и upper triangular subspaces.

# 4. Rank-one factorization

Рассмотри матрицу из Lecture 11:

\[
R=
\begin{bmatrix}
1&4&5\\
2&8&10
\end{bmatrix}.
\]

1. Представь \(R\) в виде \(uv^T\).
2. Найди basis для \(C(R)\), \(C(R^T)\), \(N(R)\) и \(N(R^T)\).
3. Укажи dimensions четырёх пространств и проверь rank-nullity.
4. Покажи, что множество всех rank-one matrices не является subspace. Используй две матрицы размера \(2\times2\), каждая rank one, сумма которых имеет rank two.
5. Для

\[
u=\begin{bmatrix}2\\-1\\3\end{bmatrix},
\qquad
v=\begin{bmatrix}1\\0\\-2\end{bmatrix}
\]

вычисли \(uv^T\) и объясни, почему все его столбцы лежат на одной линии.

# 5. Nullspace как подпространство

Пусть

\[
H=\{x\in\mathbb{R}^4:x_1+x_2+x_3+x_4=0\}.
\]

1. Запиши \(H\) как nullspace одной матрицы.
2. Найди basis и dimension для \(H\).
3. Объясни, почему описание одним homogeneous linear equation сразу гарантирует, что \(H\) является subspace.

# 6. Короткий мост к function spaces

Проверь, что все функции

\[
y(x)=c_1\cos x+c_2\sin x
\]

решают \(y''+y=0\). Укажи basis и dimension этого solution space.

