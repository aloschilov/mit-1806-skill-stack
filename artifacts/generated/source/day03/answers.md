---
title: "День 3. Ответы и акценты"
subtitle: 'MIT 18.06. Gate F: complete solutions of \(Ax=b\).'
output: "artifacts/generated/answers/day03_answers_and_checks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Проверочный акцент: полное решение существует только после проверки совместности. Формат дня: consistency, \(x_p\), \(N(A)\), then \(x=x_p+x_n\).

# Глоссарий

- Расширенная матрица (augmented matrix) - \([A\ b]\), где правая часть редуцируется вместе с \(A\).
- Совместность (consistency) - отсутствие строки вида \([0\ 0\ \cdots\ 0\ |\ d]\) при \(d\ne0\).
- Частное решение \(x_p\) (particular solution) - одно решение \(Ax=b\), обычно при free variables равных \(0\).
- Нуль-пространство \(N(A)\) (nullspace) - все решения \(Ax=0\).
- Полное решение (complete solution) - \(x=x_p+x_n\), где \(x_n\in N(A)\).
- Full column rank и full row rank - случаи \(r=n\) и \(r=m\).

# 0. Быстрый ремонт со Дня 2

Rank равен числу pivot columns, потому что каждый pivot даёт одну независимую строку и одну независимую pivot variable.

У \(B_2\) всего \(n=5\) переменных и \(r=2\) pivot variables, поэтому free variables:

\[
n-r=5-2=3.
\]

Проверка special solution:

\[
B_2
\begin{bmatrix}
-2\\
1\\
1\\
0\\
0
\end{bmatrix}
=
\begin{bmatrix}
0\\
0\\
0\\
0
\end{bmatrix}.
\]

# 1. \(B_1x=b\)

\[
B_1=
\begin{bmatrix}
1 & 2 & 1 & 0\\
2 & 4 & 3 & 1\\
1 & 2 & 2 & 1
\end{bmatrix},
\qquad
b=
\begin{bmatrix}
1\\
3\\
2
\end{bmatrix}.
\]

Для произвольной правой части \((b_1,b_2,b_3)\):

\[
\left[
\begin{array}{cccc|c}
1&2&1&0&b_1\\
2&4&3&1&b_2\\
1&2&2&1&b_3
\end{array}
\right]
\sim
\left[
\begin{array}{cccc|c}
1&2&0&-1&3b_1-b_2\\
0&0&1&1&b_2-2b_1\\
0&0&0&0&b_3+b_1-b_2
\end{array}
\right].
\]

Условие совместности:

\[
b_3+b_1-b_2=0,
\qquad
\text{то есть}
\qquad
b_3=b_2-b_1.
\]

Для \(b=(1,3,2)\) условие выполнено, потому что \(2=3-1\). Значит:

\[
\left[
\begin{array}{cccc|c}
1&2&0&-1&0\\
0&0&1&1&1\\
0&0&0&0&0
\end{array}
\right].
\]

Пусть \(x_2=s\), \(x_4=t\). Тогда:

\[
x_1=-2s+t,
\qquad
x_3=1-t.
\]

Частное решение при \(s=0,t=0\):

\[
x_p=
\begin{bmatrix}
0\\
0\\
1\\
0
\end{bmatrix}.
\]

Полное решение:

\[
x=
\begin{bmatrix}
0\\
0\\
1\\
0
\end{bmatrix}
+s
\begin{bmatrix}
-2\\
1\\
0\\
0
\end{bmatrix}
+t
\begin{bmatrix}
1\\
0\\
-1\\
1
\end{bmatrix}.
\]

Проверки:

\[
B_1x_p=b,
\qquad
B_1
\begin{bmatrix}
-2\\
1\\
0\\
0
\end{bmatrix}
=0,
\qquad
B_1
\begin{bmatrix}
1\\
0\\
-1\\
1
\end{bmatrix}
=0.
\]

# 2. \(B_2x=c\)

\[
B_2=
\begin{bmatrix}
1 & 0 & 2 & -1 & 3\\
0 & 1 & -1 & 2 & 1\\
1 & 1 & 1 & 1 & 4\\
2 & 1 & 3 & 0 & 7
\end{bmatrix},
\qquad
c=
\begin{bmatrix}
1\\
2\\
3\\
4
\end{bmatrix}.
\]

Для произвольной правой части \((c_1,c_2,c_3,c_4)\) условия совместности читаются из зависимостей строк:

\[
c_3=c_1+c_2,
\qquad
c_4=2c_1+c_2.
\]

Для \(c=(1,2,3,4)\) оба условия выполнены:

\[
3=1+2,
\qquad
4=2\cdot1+2.
\]

Тогда row reduced system:

\[
\left[
\begin{array}{ccccc|c}
1&0&2&-1&3&1\\
0&1&-1&2&1&2\\
0&0&0&0&0&0\\
0&0&0&0&0&0
\end{array}
\right].
\]

Пусть \(x_3=s\), \(x_4=t\), \(x_5=u\). Тогда:

\[
x_1=1-2s+t-3u,
\qquad
x_2=2+s-2t-u.
\]

Частное решение при \(s=t=u=0\):

\[
x_p=
\begin{bmatrix}
1\\
2\\
0\\
0\\
0
\end{bmatrix}.
\]

Полное решение:

\[
x=
\begin{bmatrix}
1\\
2\\
0\\
0\\
0
\end{bmatrix}
+s
\begin{bmatrix}
-2\\
1\\
1\\
0\\
0
\end{bmatrix}
+t
\begin{bmatrix}
1\\
-2\\
0\\
1\\
0
\end{bmatrix}
+u
\begin{bmatrix}
-3\\
-1\\
0\\
0\\
1
\end{bmatrix}.
\]

# 3. No-solution check

Для \(\tilde b=(1,3,1)\):

\[
\tilde b_3+\tilde b_1-\tilde b_2=1+1-3=-1\ne0.
\]

Значит, в расширенной матрице появляется строка вида \([0\ 0\ 0\ 0\ |\ -1]\), и решения нет.

Для \(\tilde c=(1,2,3,5)\):

\[
\tilde c_3=\tilde c_1+\tilde c_2,
\qquad
\tilde c_4\ne2\tilde c_1+\tilde c_2,
\]

потому что \(5\ne4\). Значит, решения нет.

# 4. Четыре случая ранга

1. Square invertible: \(r=m=n\).
Все \(b\) разрешимы. Решение одно. \(\dim N(A)=0\). Главный признак: \(A^{-1}\) существует.

2. Full column rank: \(r=n<m\).
Не все \(b\) разрешимы. Если система совместна, решение одно. \(\dim N(A)=0\). Главный риск: \(b\) может не лежать в \(C(A)\).

3. Full row rank: \(r=m<n\).
Все \(b\) разрешимы. Решений бесконечно много. \(\dim N(A)=n-r\). Главный признак: pivot есть в каждой строке, но есть free variables.

4. Rank deficient: \(r<m\) и \(r<n\).
Не все \(b\) разрешимы. Если система совместна, решений бесконечно много. \(\dim N(A)=n-r\). Главный риск: одновременно есть ограничения на \(b\) и free variables.

# 5. Concept check

1. Строка \([0\ 0\ \cdots\ 0\ |\ d]\) с \(d\ne0\) означает уравнение \(0=d\), поэтому система несовместна.
2. Если \(x_p\) - одно решение \(Ax=b\), то для любого \(x_n\in N(A)\):

\[
A(x_p+x_n)=Ax_p+Ax_n=b+0=b.
\]

3. При full column rank \(r=n\), поэтому все \(n\) переменных pivot variables и free variables нет.
4. При full row rank \(r=m\) pivot есть в каждой строке, поэтому после редукции не может появиться zero row с ненулевой правой частью.
5. Обычно удобно сначала найти \(R\) и условия совместности, затем \(x_p\), а \(N(A)\) читать из той же \(R\). Так одна редукция обслуживает обе задачи.
