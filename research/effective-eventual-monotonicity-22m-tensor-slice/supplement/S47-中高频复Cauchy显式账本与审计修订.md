# S47：中高频复 Cauchy 显式账本与审计修订

案例：`TR16-22M-TAIL-PREWRITE-0001`

状态：修订候选。本文补齐 S44 式 (1)、(5) 的复邻域账本，并记录写作前审计的
两个数值修订。它不改变主定理、阈值或完整猜想仍开放的边界。

沿用 S34--S44，写

\[
d_1(s)=\left(1-\frac{s_0}{\sqrt3}\right)^2-s_1^2-\frac{s_2^2}{2},
\qquad
d_2(s)=1+\frac{2s_0}{\sqrt3}-\frac{s_2^2}{2},
\]

以及 `D=d_1d_2`。精确特征函数为

\[
\widehat p_r(\xi)=d_1(i\xi/\sqrt r)^{-1/2}
D(i\xi/\sqrt r)^{-r/2}.                                  \tag{1}
\]

所有复幂取从实轴基点连续延拓的解析支。下面的非消失界同时证明这些局部支合法。

## 1. 中频复多圆盘

设

\[
r\ge2^{128},\qquad r^{1/16}<R=|\xi|\le\sqrt r,
\qquad |\eta_j|\le\rho_m:=\frac1{64\sqrt r}.
\]

置 `w=i(ξ+η)/sqrt(r)`。从实轴点 `iu=iξ/sqrt(r)` 到 `w` 的逐坐标位移至多

\[
\delta_m=\frac1{64r}.
\]

在整条线段上每个坐标的模小于 `1+1/(64r)`。直接对上述二次式求导得到

\[
\sum_j|\partial_jd_1|<5,
\qquad
\sum_j|\partial_jd_2|<3.                                 \tag{2}
\]

S34 在实轴上给出 `|d_1|>=1`、`|d_2|>=1`。由 `(2)` 和积分中值公式，线段上

\[
|d_1|\ge1-5\delta_m>\frac12,
\qquad
|d_2|\ge1-3\delta_m>\frac12.                             \tag{3}
\]

故对连续对数支有

\[
|\Delta\log d_1|\le10\delta_m,
\qquad
|\Delta\log d_2|\le6\delta_m.
\]

由 `(1)`，复位移的总对数模损失至多

\[
\frac{r+1}{2}10\delta_m+\frac r2 6\delta_m
=\frac{16r+10}{128r}<\frac14.                            \tag{4}
\]

结合 S34 的实轴界，

\[
\sup_{|\eta_j|\le\rho_m}|\widehat p_r(\xi+\eta)|
\le e^{1/4}e^{-23R^2/94}.                                \tag{5}
\]

对 Edgeworth 项 `g_r(ζ)=e^{-ζ·ζ/2}E_4(ζ)`，S42 的系数绝对值估计对复变量仍成立。
由于 `|η|<=sqrt(3)/(64sqrt(r))`，有

\[
|E_4(\xi+\eta)|\le2\cdot10^4(1+R)^8,
\]

且

\[
\operatorname{Re}\!\left(-\frac{(\xi+\eta)\cdot(\xi+\eta)}2\right)
\le-\frac{R^2}{2}+\frac1{32}.
\]

因此

\[
\sup|g_r(\xi+\eta)|
\le3\cdot10^4(1+R)^8e^{-23R^2/94}.                       \tag{6}
\]

多变量 Cauchy 估计、`|alpha|<=4`、`alpha!<=24` 给出

\[
|\partial^\alpha(\widehat p_r-g_r)(\xi)|
\le24\,64^4r^2\{e^{1/4}+3\cdot10^4(1+R)^8\}
e^{-23R^2/94}.                                            \tag{7}
\]

`(1-Delta)^2` 的各项绝对系数和为 `16`。式 `(7)` 的右端严格小于

\[
10^{30}r^6(1+R)^{40}e^{-23R^2/94},                       \tag{8}
\]

这就是 S44 式 (1)。

## 2. 高频复多圆盘

令 `R=|xi|=sqrt(r)u`、`u>=1`，并取

\[
|\eta_j|\le\rho_h:=\frac1{4096\sqrt r(1+u)^2},
\qquad
\delta_h:=\frac1{4096r(1+u)^2}.                          \tag{9}
\]

在对应线段上 `|w_j|<=u+delta_h<2u`。直接求导并向外放大得到

\[
\sum_j|\partial_jd_1|\le8(1+u),
\qquad
\sum_j|\partial_jd_2|\le2(1+u).                         \tag{10}
\]

仍由实轴 `|d_1|,|d_2|>=1`，式 `(10)` 的总位移小于 `1/2`，故线段上两个因子
均不为零且模至少 `1/2`。于是

\[
|\Delta\log d_1|\le16(1+u)\delta_h,
\qquad
|\Delta\log d_2|\le4(1+u)\delta_h.
\]

代入 `(1)`，总对数模损失至多

\[
\{10r+8\}(1+u)\delta_h
\le\frac{10+8/2^{128}}{8192}<\frac1{512}.               \tag{11}
\]

S34 的实轴尾界遂给出

\[
\sup|\widehat p_r(\xi+\eta)|
\le e^{1/512}(1+u^2/2)^{-r/4}.                           \tag{12}
\]

S42 的齐次系数估计在该复多圆盘上给出

\[
|E_4(\xi+\eta)|
\le2\cdot10^4r^4(1+u)^{24}.                             \tag{13}
\]

又有

\[
\operatorname{Re}\!\left(-\frac{(\xi+\eta)\cdot(\xi+\eta)}{2}\right)
\le-\frac{ru^2}{2}+\frac1{4096},
\qquad
e^{-ru^2/2}\le(1+u^2/2)^{-r/4}.                         \tag{14}
\]

以半径 `(9)` 作四阶 Cauchy 估计，

\[
\begin{aligned}
|\partial^\alpha(\widehat p_r-g_r)(\xi)|
\le{}&24\,4096^4r^2(1+u)^8\\
&\times\left[e^{1/512}+2\cdot10^4e^{1/4096}
r^4(1+u)^{24}\right](1+u^2/2)^{-r/4}.
\end{aligned}                                             \tag{15}
\]

再乘 `(1-Delta)^2` 的绝对系数和 `16`，式 `(15)` 严格小于

\[
10^{30}r^6(1+u)^{40}(1+u^2/2)^{-r/4},                    \tag{16}
\]

即 S44 式 (5)。

## 3. 审计指出的数值修订

S44 高频相对 `r^{-5/2}` 界的对数导数应包含三维 Jacobian 开平方后的 `3/4`：

\[
\frac d{d\log r}\log\frac{\text{高频上界}}{r^{-5/2}}
=\frac{37}{4}-\frac r4\log(3/2),                         \tag{17}
\]

而不是原验证器中的 `8.5-r log(3/2)/4`。对 `r>=2^128`，修正后的 `(17)` 仍严格
为负。S43、S44 的最终小数门改用 `mpmath.iv` 外向区间复算；主阈值不变。

显式梯度、复位移损失、Cauchy 常数和式 `(17)` 的账本见
[check_s47_complex_cauchy_ledger.py](../verification/check_s47_complex_cauchy_ledger.py)。

## 4. 原参数索引

`MATH-DIR-0106/S1` 的统一 Kac--Rice 归一化为

\[
a(2,2,m)=\frac{\pi}{2(m-2)}I_{m-2}\qquad(m\ge3).         \tag{18}
\]

因此令 `r=m-3`，S44 的相邻不等式正好对应

\[
a(2,2,m)<a(2,2,m-1).
\]

尾部 `r>=3*10^103` 对应 `m>=3*10^103+3`。这一索引只翻译主结果，不扩大其范围。
