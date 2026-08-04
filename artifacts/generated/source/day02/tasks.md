---
title: "День 2. RREF, rank и free variables"
subtitle: "MIT 18.06. Время: 70-100 минут."
output: "artifacts/generated/tasks/day02_tasks.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Цель дня: превратить интуицию про \(C(A)\) и \(N(A)\) в вычислительный алгоритм через RREF. Это прямой заход на Gate E.

# Глоссарий

- Приведённая ступенчатая форма RREF (reduced row echelon form) - форма после допустимых операций со строками.
- Ранг \(r\) (rank) - число pivot columns, то есть число опорных столбцов.
- Опорная переменная (pivot variable) - переменная в pivot column.
- Свободная переменная (free variable) - переменная без pivot; ей можно задавать параметр.
- Специальное решение (special solution) - решение \(Ax=0\), полученное выбором одной free variable равной \(1\), а остальных free variables равными \(0\).
- Дефектность (nullity) - размерность \(N(A)\), равная \(n-r\).

Опора по курсу: Lecture 7 вводит pivot variables, free variables и special solutions для \(Ax=0\); Lecture 8 явно вводит row reduced form \(R\) для задач \(Ax=b\). В этом листке RREF-проход соединяет эти две идеи.

# 0. Быстрый ремонт со Дня 1

Для лекционной матрицы

\[
A=
\begin{bmatrix}
1 & 1 & 2\\
2 & 1 & 3\\
3 & 1 & 4\\
4 & 1 & 5
\end{bmatrix}
\]

проверь, разрешимы ли \(Ax=b\) для трёх правых частей:

1. \(b=(4,6,8,10)\).
2. \(b=(1,2,4,8)\).
3. \(b=(0,1,2,3)\).

В каждом случае используй условие:

\[
b_2-b_1=b_3-b_2=b_4-b_3.
\]

# 1. RREF-проход: матрица \(B_1\)

\[
B_1=
\begin{bmatrix}
1 & 2 & 1 & 0\\
2 & 4 & 3 & 1\\
1 & 2 & 2 & 1
\end{bmatrix}.
\]

Сделай:

1. Приведи \(B_1\) к RREF \(R_1\).
2. Укажи pivot columns и free columns.
3. Назови pivot variables и free variables.
4. Найди rank \(r\).
5. Выпиши special solutions и базис \(N(B_1)\).
6. Проверь размерность: \(\dim N(B_1)=n-r\).

# 2. RREF-проход: матрица \(B_2\)

\[
B_2=
\begin{bmatrix}
1 & 0 & 2 & -1 & 3\\
0 & 1 & -1 & 2 & 1\\
1 & 1 & 1 & 1 & 4\\
2 & 1 & 3 & 0 & 7
\end{bmatrix}.
\]

Сделай те же шесть пунктов:

1. RREF \(R_2\).
2. Pivot columns и free columns.
3. Pivot variables и free variables.
4. Rank \(r\).
5. Special solutions и базис \(N(B_2)\).
6. Проверка \(\dim N(B_2)=n-r\).

# 3. Concept check

Ответь коротко:

1. Почему pivot columns для \(C(A)\) надо брать из исходной матрицы, а не из \(R\)?
2. Почему число свободных переменных равно \(n-r\)?
3. Что означает special solution?
4. Если у матрицы \(m\times n\) rank равен \(n\), каким будет \(N(A)\)?
5. Если rank меньше \(n\), почему в \(N(A)\) обязательно есть ненулевые решения?

# 4. Формат результата

Минимальный состав:

- два RREF-вычисления;
- таблица по \(B_1,B_2\): rank, pivot variables, free variables, базис \(N(A)\);
- ответы на пять concept-check вопросов;
- один отдельный список ошибок, если на каком-то шаге пришлось откатиться.
