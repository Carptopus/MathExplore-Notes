# S43：复邻域 Cauchy 与低频四阶 `L2` 常数

案例：`TR16-22M-SLICE-ASSAULT-0001`

状态：严格引理已证。S42 的零阶低频余项已经统一提升到四阶导数，并得到
`(1-Delta)^2` 低频 `L2` 误差的显式常数。常数很粗，只是有效性证书；中频和
高频仍未汇总。

## 1. 实点周围的统一复多圆盘

沿用 S42，设

\[
r\ge2^{16},\qquad R=|\xi|\le r^{1/16},
\qquad s_R=\frac1{64(1+R)}.                               \tag{1}
\]

对复向量 `eta` 满足每个 `|eta_j|<=s_R`，置 `zeta=xi+eta`。于是

\[
\|\eta\|_2\le\frac{\sqrt3}{64(1+R)},qquad
\|\zeta\|_2\le R+\frac{\sqrt3}{64}.                      \tag{2}
\]

并且 `epsilon||zeta||_2<1/120`。因此 S35 使用的两个对数支在整个多圆盘
内解析；增量的 `|z_2+z_3+z_4|` 和初始项的 `|ell+h|` 都严格小于其级数
收敛半径。

把 S42 式 `(2)` 原样用于复变量的欧氏模，使用
`epsilon||zeta||<=1/120`、`epsilon<=1/256`，得到更松但统一的

\[
\sum_{j=1}^4\epsilon^j|A_j(\zeta)|
\le\frac{\|\zeta\|_2^2}{50}+\frac1{1000}.                \tag{3}
\]

S35 的复解析余项同样满足

\[
|\delta(\zeta)|
\le\epsilon^5\left(3\|\zeta\|_2^5+4\|\zeta\|_2^7\right)
<\frac1{1000}.                                             \tag{4}
\]

## 2. 复圆盘上的零阶包络

由 `(2)`，

\[
\operatorname{Re}\left(-\frac{\zeta\cdot\zeta}{2}\right)
\le-\frac{R^2}{2}+\frac{\sqrt3}{64}+\frac3{2\cdot64^2}.
\]

再把 `(3)` 中的 `||zeta||^2/50` 展开，并用一次 Young 不等式吸收关于
`R` 的线性项，可得总指数不超过

\[
-\frac{47}{100}R^2+\frac1{25}.                            \tag{5}
\]

S42 的 Bell 多项式余项证明在复圆盘内不变；且
`1+||zeta||<=(1+sqrt(3)/64)(1+R)`。把全部固定数字向外放大，得到

\[
\sup_{|\eta_j|\le s_R}
\left|\widehat p_r(\xi+\eta)-
e^{-(\xi+\eta)\cdot(\xi+\eta)/2}E_4(\xi+\eta)\right|
\le4\cdot10^9\epsilon^5(1+R)^{30}e^{-47R^2/100}.          \tag{6}
\]

## 3. Cauchy 导数与 `L2` 汇总

令 `widehat rho_r` 为 `(6)` 中的差。多变量 Cauchy 估计给出：若
`|alpha|=k<=4`，则

\[
|\partial^\alpha\widehat\rho_r(\xi)|
\le\alpha!\,s_R^{-k}\sup|\widehat\rho_r|
\le2\cdot10^{18}\epsilon^5(1+R)^{34}e^{-47R^2/100}.       \tag{7}
\]

因为 `(1-Delta)^2` 的各项绝对系数和为

\[
1+2\cdot3+3+2\cdot3=16,
\]

式 `(7)` 给出低频点态界

\[
|(1-\Delta)^2\widehat\rho_r(\xi)|
\le3.2\cdot10^{19}\epsilon^5(1+R)^{34}e^{-47R^2/100}.    \tag{8}
\]

将积分域扩大到全部 `R^3`，并使用

\[
(1+R)^{68}\le2^{67}(1+R^{68}),
\]

得到完全显式的低频账本

\[
\boxed{
\left\|(1-\Delta)^2\widehat\rho_r\right\|_{L^2(R\le r^{1/16})}
\le B_{\rm low}\,r^{-5/2}},                               \tag{9}
\]

其中

\[
\begin{aligned}
B_{\rm low}:={}&3.2\cdot10^{19}\sqrt{J},\\
J:={}&4\pi\,2^{67}\left[
\frac12(0.94)^{-3/2}\Gamma(3/2)
+\frac12(0.94)^{-71/2}\Gamma(71/2)
\right].                                                   \tag{10}
\end{aligned}
\]

数值上 `J<1.452e61`、`B_low<1.220e50`。这是有意保守的存在性常数，不代表
预计真实阈值；它的作用是证明低频部分已经完全有效化，并暴露常数优化的真实
量级。

## 4. 对峰顶的推进与边界

S42 的四阶加权 Plancherel 门与 `(9)` 合并后，低频不再含任何未指定常数。
剩余 R1 义务只在：

1. `r^{1/16}<R<=sqrt(r)` 的中频四阶 `L2` 尾；
2. `R>=sqrt(r)` 的高频四阶 `L2` 尾；
3. 两段与 `B_low`、S6A 的 `C` 及二阶系数 `D` 的最终阈值汇总。

`B_low` 很大意味着直接使用当前粗 Cauchy 常数可能得到不可处理的阈值；这不
否定 R1，但最终汇总后必须与已有 endpoint fallback 比较，不能因“阈值有限”
就声称接近完整峰顶。

复邻域尺度、常数不等式和 Gamma 积分账本见
[check_s43_low_frequency_derivatives.py](../verification/check_s43_low_frequency_derivatives.py)。
