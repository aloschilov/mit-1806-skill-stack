---
title: "День 6. Ответы и акценты"
subtitle: "MIT 18.06. Matrix spaces, intersections, sums, rank one."
output: "artifacts/generated/answers/day06_answers_and_checks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Проверочный акцент: matrix space подчиняется тем же правилам basis и dimension, что и \(\mathbb{R}^n\); rank-one matrix связывает column space и row space формулой \(uv^T\).

# Глоссарий

- Matrix space - векторное пространство матриц фиксированного размера.
- Intersection \(S\cap U\) - общая часть двух subspaces.
- Sum \(S+U\) - все суммы \(s+u\).
- Rank-one factorization - запись ненулевой матрицы rank one в виде \(uv^T\).
- Outer product - матрица, чей \((i,j)\)-entry равен \(u_i v_j\).

# 0. Короткий ремонт со Дня 5

1. Равенство \(A^Ty=0\) эквивалентно

\[
-\operatorname{row}_1(A)+\operatorname{row}_3(A)=0.
\]

Иными словами, первая и третья строки \(A\) совпадают.

2. Ненулевые строки RREF independent из-за разных pivot positions и span исходный row space, потому что обратимые row operations сохраняют его.

# 1. Пространство всех матриц \(2\times2\)

Любая матрица имеет вид

\[
\begin{bmatrix}a&b\\c&d\end{bmatrix}
=aE_{11}+bE_{12}+cE_{21}+dE_{22},
\]

где

\[
E_{11}=\begin{bmatrix}1&0\\0&0\end{bmatrix},
\quad
E_{12}=\begin{bmatrix}0&1\\0&0\end{bmatrix},
\quad
E_{21}=\begin{bmatrix}0&0\\1&0\end{bmatrix},
\quad
E_{22}=\begin{bmatrix}0&0\\0&1\end{bmatrix}.
\]

Эти четыре матрицы independent и span всё \(M_{2\times2}\), поэтому

\[
\dim M_{2\times2}=4.
\]

Координатный вектор матрицы в указанном порядке basis равен \((a,b,c,d)^T\).

# 2. Symmetric, upper triangular и diagonal

Для symmetric subspace:

\[
\operatorname{basis}S=
\left\{
E_{11},
E_{12}+E_{21},
E_{22}
\right\},
\qquad
\dim S=3.
\]

Для upper triangular subspace:

\[
\operatorname{basis}U=
\{E_{11},E_{12},E_{22}\},
\qquad
\dim U=3.
\]

Матрица одновременно symmetric и upper triangular только тогда, когда она diagonal. Поэтому

\[
S\cap U=
\left\{
\begin{bmatrix}a&0\\0&d\end{bmatrix}
\right\},
\quad
\operatorname{basis}(S\cap U)=\{E_{11},E_{22}\},
\quad
\dim(S\cap U)=2.
\]

Для union возьмём

\[
X=E_{12}+E_{21}\in S,
\qquad
Y=E_{12}\in U.
\]

Тогда

\[
X+Y=
\begin{bmatrix}0&2\\1&0\end{bmatrix}
\]

не является ни symmetric, ни upper triangular. Значит, \(S\cup U\) не замкнуто относительно сложения.

Матрицы \(E_{11},E_{12},E_{22}\) уже лежат в \(U\), а

\[
E_{21}=(E_{12}+E_{21})-E_{12}\in S+U.
\]

Следовательно, \(S+U=M_{2\times2}\), \(\dim(S+U)=4\), и

\[
\dim S+\dim U=3+3=2+4
=\dim(S\cap U)+\dim(S+U).
\]

# 3. Размерности в \(M_{3\times3}\)

- Все matrices: девять свободных entries, dimension \(9\).
- Symmetric matrices: три diagonal entries и три entries выше диагонали; entries ниже диагонали определяются симметрией. Dimension \(6\).
- Upper triangular matrices: три diagonal entries и три entries выше диагонали. Dimension \(6\).
- Diagonal matrices: три diagonal entries. Dimension \(3\).

Intersection symmetric и upper triangular subspaces состоит из diagonal matrices, а их sum равен всему \(M_{3\times3}\). Поэтому

\[
6+6=3+9.
\]

# 4. Rank-one factorization

Матрица \(R\) раскладывается как

\[
R=
\begin{bmatrix}1\\2\end{bmatrix}
\begin{bmatrix}1&4&5\end{bmatrix}
=uv^T.
\]

Отсюда сразу видны column space и row space:

\[
\operatorname{basis}C(R)=
\left\{\begin{bmatrix}1\\2\end{bmatrix}\right\},
\qquad
\operatorname{basis}C(R^T)=
\left\{\begin{bmatrix}1\\4\\5\end{bmatrix}\right\}.
\]

Так как \(Rx=u(v^Tx)\), nullspace задаётся уравнением

\[
x_1+4x_2+5x_3=0.
\]

Один basis:

\[
\operatorname{basis}N(R)=
\left\{
\begin{bmatrix}-4\\1\\0\end{bmatrix},
\begin{bmatrix}-5\\0\\1\end{bmatrix}
\right\}.
\]

А \(R^Ty=v(u^Ty)\), поэтому

\[
\operatorname{basis}N(R^T)=
\left\{\begin{bmatrix}-2\\1\end{bmatrix}\right\}.
\]

Dimensions равны \(1,2,1,1\) для \(C(R)\), \(N(R)\), \(C(R^T)\), \(N(R^T)\). Проверки:

\[
1+2=3,
\qquad
1+1=2.
\]

Множество rank-one matrices не является subspace. Например,

\[
P=E_{11},
\qquad
Q=E_{22}
\]

имеют rank one, но \(P+Q=I_2\) имеет rank two.

Для данных \(u\) и \(v\):

\[
uv^T=
\begin{bmatrix}
2&0&-4\\
-1&0&2\\
3&0&-6
\end{bmatrix}.
\]

Каждый столбец равен скаляру, умноженному на \(u\): соответственно \(u\), \(0u\), \(-2u\). Поэтому column space является одной линией.

# 5. Nullspace как подпространство

\[
H=N\!\left(\begin{bmatrix}1&1&1&1\end{bmatrix}\right).
\]

Из \(x_1=-x_2-x_3-x_4\) получаем

\[
\operatorname{basis}H=
\left\{
\begin{bmatrix}-1\\1\\0\\0\end{bmatrix},
\begin{bmatrix}-1\\0\\1\\0\end{bmatrix},
\begin{bmatrix}-1\\0\\0\\1\end{bmatrix}
\right\},
\qquad
\dim H=3.
\]

Nullspace любой матрицы является subspace: нулевой вектор решает homogeneous equation, а линейные комбинации решений снова являются решениями.

# 6. Короткий мост к function spaces

Для \(y=c_1\cos x+c_2\sin x\):

\[
y''=-c_1\cos x-c_2\sin x=-y.
\]

Значит, \(y''+y=0\). Solution space имеет basis \(\{\cos x,\sin x\}\) и dimension \(2\).

