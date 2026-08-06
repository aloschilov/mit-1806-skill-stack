---
title: "День 4. Ответы и акценты"
subtitle: "MIT 18.06. Gate G: independence, span, basis, dimension."
output: "artifacts/generated/answers/day04_answers_and_checks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Проверочный акцент: векторы ставим столбцами, считаем rank, затем читаем independence, span, basis и dimension.

# Глоссарий

- Linear independence (линейная независимость) - \(Ax=0\) имеет только \(x=0\).
- Linear dependence (линейная зависимость) - \(N(A)\) содержит ненулевой вектор.
- Span (линейная оболочка) - все линейные комбинации столбцов.
- Basis (базис) - independent set, который spans нужное пространство.
- Dimension (размерность) - число pivot columns в basis.
- Ambient space (объемлющее пространство) - пространство, где живут векторы, например \(\mathbb{R}^3\).

# 0. Быстрый ремонт со Дня 3

При full column rank \(r=n\), поэтому pivot есть в каждом столбце. Значит, free variables нет.

Да, zero rows могут быть, если \(m>n\). Например, у tall matrix с full column rank после elimination будет \(m-n\) zero rows. Это не создаёт free variables.

Общий шаблон:

\[
x=x_p+x_n,
\qquad
x_n\in N(A).
\]

# 1. Один matrix pass

\[
A=
\begin{bmatrix}
1 & 0 & 1 & 1\\
0 & 1 & 1 & 1\\
1 & 1 & 2 & 0
\end{bmatrix}
\sim
R=
\begin{bmatrix}
1 & 0 & 1 & 0\\
0 & 1 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}.
\]

Pivot columns: \(1,2,4\). Free column: \(3\).

Из RREF видно, что:

\[
a_3=a_1+a_2.
\]

Эквивалентная нулевая комбинация:

\[
-a_1-a_2+a_3=0.
\]

Rank:

\[
r=3.
\]

Четыре столбца dependent, потому что есть nonzero relation.

Столбцы span-ят \(\mathbb{R}^3\), потому что rank равен \(3\), то есть \(r=m\).

Basis для \(C(A)\) из исходных столбцов:

\[
\left\{
\begin{bmatrix}1\\0\\1\end{bmatrix},
\begin{bmatrix}0\\1\\1\end{bmatrix},
\begin{bmatrix}1\\1\\0\end{bmatrix}
\right\}.
\]

Dimension:

\[
\dim C(A)=3.
\]

# 2. Пять наборов векторов

## \(S_1\)

\[
v_3=v_1+v_2.
\]

Rank \(=2\). Набор dependent. Он не spans \(\mathbb{R}^3\). Не basis для \(\mathbb{R}^3\). Dimension of span равна \(2\).

Basis for span:

\[
\left\{
\begin{bmatrix}1\\0\\1\end{bmatrix},
\begin{bmatrix}0\\1\\1\end{bmatrix}
\right\}.
\]

## \(S_2\)

Rank \(=3\). Набор independent. Он spans \(\mathbb{R}^3\). Это basis для \(\mathbb{R}^3\). Dimension равна \(3\).

## \(S_3\)

\[
\begin{bmatrix}2\\4\end{bmatrix}
=
2
\begin{bmatrix}1\\2\end{bmatrix}.
\]

Rank \(=1\). Набор dependent. Он не spans \(\mathbb{R}^2\). Не basis для \(\mathbb{R}^2\). Dimension of span равна \(1\).

## \(S_4\)

Rank \(=3\). Набор dependent, потому что четыре вектора в \(\mathbb{R}^3\) не могут быть independent. Он spans \(\mathbb{R}^3\). Не basis, потому что basis не должен иметь лишний dependent vector. Dimension равна \(3\).

Один basis:

\[
\left\{
\begin{bmatrix}1\\0\\0\end{bmatrix},
\begin{bmatrix}0\\1\\0\end{bmatrix},
\begin{bmatrix}0\\0\\1\end{bmatrix}
\right\}.
\]

## \(S_5\)

Rank \(=3\). Набор independent. Он не spans \(\mathbb{R}^4\), потому что \(r=3<4\). Не basis для \(\mathbb{R}^4\). Dimension of span равна \(3\). Сам набор является basis for its span.

# 3. Claim repair

1. Исправление: если векторов больше, чем dimension ambient space, они не могут быть independent. Но они могут span-ить пространство. Counterexample: \(S_4\) имеет четыре вектора в \(\mathbb{R}^3\) и spans \(\mathbb{R}^3\).

2. Исправление: если векторов меньше, чем dimension ambient space, они не могут span-ить всё пространство. Но они могут быть independent. Counterexample: \(S_5\) имеет три independent vectors в \(\mathbb{R}^4\).

# 4. Выбери basis

1. Для \(C(A)\):

\[
\{a_1,a_2,a_4\}.
\]

2. Для \(S_4\):

\[
\left\{
\begin{bmatrix}1\\0\\0\end{bmatrix},
\begin{bmatrix}0\\1\\0\end{bmatrix},
\begin{bmatrix}0\\0\\1\end{bmatrix}
\right\}.
\]

3. Для \(\operatorname{span}(S_1)\):

\[
\left\{
\begin{bmatrix}1\\0\\1\end{bmatrix},
\begin{bmatrix}0\\1\\1\end{bmatrix}
\right\}.
\]

# 5. Concept check

1. Dependence видна через \(N(A)\): если \(Ax=0\) имеет nonzero solution, то столбцы dependent.
2. Столбцы span-ят \(\mathbb{R}^m\), если rank равен \(m\), то есть pivot есть в каждой строке.
3. Набор является basis для \(\mathbb{R}^m\), если он independent и spans \(\mathbb{R}^m\). Эквивалентно: ровно \(m\) векторов и rank \(m\).
4. Dimension of column space равна rank, потому что pivot columns образуют basis для \(C(A)\), а их число равно \(r\).
5. Pivot columns надо брать из исходной матрицы, потому что row operations меняют сами column vectors. RREF помогает выбрать номера pivot columns, но basis vectors берутся из \(A\).
