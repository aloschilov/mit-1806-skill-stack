---
title: "День 3. Обратная связь"
subtitle: "MIT 18.06. Complete solutions, consistency, rank cases."
output: "artifacts/generated/feedback_self/day03_feedback.pdf"
footer-left: "MIT 18.06 personal skill-stack"
---

> Итог: День 3 засчитан. Gate F можно считать пройденным: consistency, \(x_p\), \(N(A)\), complete solution и четыре rank cases применены правильно.

# Глоссарий

- Совместность (consistency) - условие, что \(Ax=b\) имеет хотя бы одно решение.
- Частное решение \(x_p\) (particular solution) - одно конкретное решение \(Ax=b\).
- Однородная часть \(x_n\) (homogeneous part) - любой вектор из \(N(A)\).
- Полное решение (complete solution) - запись всех решений как \(x=x_p+x_n\).
- Full column rank - случай \(r=n\), где pivot есть в каждом столбце.
- Full row rank - случай \(r=m\), где pivot есть в каждой строке.

# Что получилось хорошо

- Быстрый ремонт со Дня 2 выполнен: \(n-r=5-2=3\), special solution для \(B_2\) проверен прямым умножением.
- Для \(B_1x=b\) правильно найдены row reduced form, условие совместности \(b_3+b_1-b_2=0\), частное решение \(x_p=(0,0,1,0)\) и полное решение через \(N(B_1)\).
- Для \(B_2x=c\) правильно найдены условия совместности, \(x_p=(1,2,0,0,0)\), basis для \(N(B_2)\) и complete solution.
- No-solution checks сделаны коротко и по делу: правая часть проверяется через условие совместности.
- Таблица четырёх rank cases в целом правильная: где все \(b\) разрешимы, где есть ограничения на \(b\), где одно решение, где бесконечно много.
- Full column rank записан корректно: не все \(b\) разрешимы, решений \(0\) или \(1\), \(\dim N(A)=0\), главный риск - условия на \(b\).
- Замечание, что конкретная правая часть \(b\) для \(B_1\) совпадает со вторым pivot column исходной матрицы, корректно: это сразу показывает \(b\in C(B_1)\) и даёт \(x_p=(0,0,1,0)\).

# Что поправить

1. Когда используешь shortcut \(b\in C(A)\), допиши связку до полного решения:

\[
b\in C(A)\quad\rightarrow\quad x_p\quad\rightarrow\quad N(A)\quad\rightarrow\quad x=x_p+x_n.
\]

2. В rank cases полезно связывать строку "решений \(0\) или \(1\)" с условием \(b\in C(A)\): если \(b\) попадает в column space, решение одно; если нет, решений нет.

# Status gates

Gate C-F: PASS. Следующий фокус: Gate G, то есть independence, span, basis и dimension через rank/nullspace evidence.
