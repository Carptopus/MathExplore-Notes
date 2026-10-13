# S42：低频指数化与四阶加权 Plancherel 门

案例：`TR16-22M-SLICE-ASSAULT-0001`

状态：严格引理已证。S35 的对数余项已升级为特征函数本身的显式低频
`r^{-5/2}` 余项；S6A 的加权反演从八阶导数 `L1` 门降为四阶导数 `L2` 门。
尚缺四阶导数、以及中频和高频的显式 `L2` 常数汇总。

## 1. 四个指数修正多项式

令 `epsilon=r^{-1/2}`、`R=|xi|`。把 S35 的截断指数写成

\[
T_R(\epsilon\xi)+rT_X(\epsilon\xi)
=-\frac{R^2}{2}+\sum_{j=1}^4\epsilon^j A_j(\xi).       \tag{1}
\]

由 S35 的 `z_2,z_3,z_4` 和初始项 `ell,h` 逐齐次次数收集，可取以下统一模界：

\[
\begin{aligned}
|A_1|&\le R^3+\frac{R}{\sqrt3},\\
|A_2|&\le \frac34R^4+\frac56R^2,\\
|A_3|&\le R^5+\frac{13}{9\sqrt3}R^3,\\
|A_4|&\le \frac53R^6+\frac{41}{36}R^4.                 \tag{2}
\end{aligned}
\]

例如增量的四个界依次来自
`|z_3|/2`、`|z_4|/2+z_2^2/4`、`|z_2z_3|/2` 和
`|z_3|^2/4+|z_2z_4|/2+z_2^3/6`；初始项直接从
`-log(1+ell+h)/2` 的齐次次数得到。这里没有使用数值拟合。

若

\[
r\ge2^{16},\qquad R\le r^{1/16},                         \tag{3}
\]

则 `epsilon<=1/256` 且 `epsilon R<=1/128`。对线性项使用

\[
\frac{\epsilon R}{\sqrt3}
\le\frac{R^2}{128}+\frac{32}{3}\epsilon^2,
\]

再代入 `(2)`，得到

\[
q:=\sum_{j=1}^4\epsilon^j|A_j|
\le\frac{R^2}{60}+\frac1{5000}.                          \tag{4}
\]

## 2. 指数化截断的显式余项

置

\[
g(t)=\sum_{j=1}^4t^j\epsilon^jA_j(\xi),
\qquad E_4(\xi)=\sum_{k=0}^4\frac1{k!}
\left.\frac{d^k}{dt^k}e^{g(t)}\right|_{t=0}.             \tag{5}
\]

`E_4` 正是 Edgeworth 特征函数中截至 `epsilon^4` 的有限多项式。由 `(2)`，
每个 `A_j` 都满足

\[
|A_j|\le3(1+R)^6.
\]

在 `(3)` 下，对 `1<=k<=4` 有

\[
|g^{(k)}(t)|\le73\epsilon^k(1+R)^6\qquad(0\le t\le1).
\]

五阶完全 Bell 多项式各项的系数和小于 `52`，Taylor 积分余项遂给出

\[
\left|e^{g(1)}-E_4(\xi)\right|
\le\frac{13}{30}\epsilon^5
\{73(1+R)^6\}^5e^q.                                     \tag{6}
\]

另一方面，S35 的精确对数余项 `delta` 满足

\[
|\delta|\le\epsilon^5(3R^5+4R^7)\le\frac1{5000}         \tag{7}
\]

（最后一步使用 `(3)`）。S34 又给出完整特征函数的模界
`exp(-23R^2/94)`。由 `(4)--(7)` 和
`|e^z-1|<=|z|e^{|z|}`，得到低频显式界

\[
\boxed{
\begin{aligned}
\left|\widehat p_r(\xi)-e^{-R^2/2}E_4(\xi)\right|
\le{}&\epsilon^5e^{-23R^2/94+1/5000}\\
&\times\left[
7(1+R)^7+\frac{13}{30}73^5(1+R)^{30}
\right]
\end{aligned}}                                           \tag{8}
\]

对全部 `(3)` 中的 `xi` 成立。常数很保守，但 `(8)` 已是可积的完全显式
`r^{-5/2}` 包络，不再含 `O`、`o` 或未指定邻域。

## 3. 加权 Plancherel 只需四阶导数

S6A 为推出

\[
\int_{\mathbb R^3}|q(z)|\,|\rho_r(z)|\,dz
\]

曾用 `(1-Delta_xi)^4` 的 `L1` 反演，因而要求八阶导数。该门不是必要的。
因为 `|q(z)|<=3|z|^2`，Cauchy--Schwarz 与 Plancherel 直接给出

\[
\begin{aligned}
\int |q|\,|\rho_r|
&\le3\left(\int_{\mathbb R^3}
\frac{|z|^4}{(1+|z|^2)^4}\,dz\right)^{1/2}
\left\|(1+|z|^2)^2\rho_r\right\|_2\\
&=\boxed{\frac{3\sqrt5}{8\sqrt\pi}
\left\|(1-\Delta_\xi)^2\widehat\rho_r\right\|_2}.     \tag{9}
\end{aligned}
\]

这里使用 Fourier 逆变换常数 `(2pi)^{-3}`，并且

\[
\int_{\mathbb R^3}\frac{|z|^4}{(1+|z|^2)^4}\,dz
=\frac{5\pi^2}{8}.                                       \tag{10}
\]

因此有效化 S6A 只需控制 `widehat rho_r` 的四阶以内导数的 `L2` 范数；八阶
`L1` 门可以删除。这没有改变峰顶或误差阶，只缩小了所需 Fourier 账本。

## 4. 对峰顶的推进与下一义务

式 `(8)` 闭合了零阶低频指数化，式 `(9)` 把剩余导数义务从八阶降到四阶。
它们仍没有给出最终整数阈值，因为必须对 `(8)` 的四阶导数建立同型显式包络，
并与 S34 的中频、高频 `L2` 尾合并。

下一步固定为：对 `|alpha|<=4` 建立低频导数包络；再分别积分
`r^{1/16}<|xi|<=sqrt(r)` 和 `|xi|>=sqrt(r)` 的显式导数尾，汇总成
`||(1-Delta)^2 widehat rho_r||_2<=B r^{-5/2}`。只有得到数值 `B` 后，才把
它与 S6A 的正主余量 `C` 比较并求安全尾阈值。

精确展开、常数账本、式 `(8)` 的破坏性抽样与式 `(10)` 的符号积分见
[check_s42_effective_low_frequency.py](../verification/check_s42_effective_low_frequency.py)。
