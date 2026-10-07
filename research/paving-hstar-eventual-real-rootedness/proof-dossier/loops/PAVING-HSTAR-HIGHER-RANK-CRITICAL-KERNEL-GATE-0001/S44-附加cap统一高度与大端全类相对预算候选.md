# 附加 cap 统一高度与大端全部校正

2026-10-06，冻结候选待独审。不同于小端正级数，本页只处理 r->infinity；
不要求 cap 校正各系数非负，不覆盖正紧 r、端盘或根数。

## 1. 冻结范围

连通秩四 paving，最大 H0 大小 n−q，附加 H 大小 v<=q+2。
沿 S39 参数：q、n−4q、nr、n/r、Sigma 全部趋无穷，另 r->infinity。
令 delta_v 是准确完整坏 cap Euler 校正，主张

    sum_(H!=H0) |delta_|H|(−t^4)|
                         =o(R^n rho^(−q)|H|)。           (1)

允许全部附加 H，包括四点；振幅 |H|~Sigma^(-1)。

## 2. 所有 v 的统一系数高度

对每个 4<=v<=n−2，只有一个指定 v 点有效超平面的 paving Matroid 存在：
基为全部不包含于指定 H 的四元组。其基多面体 P_v 正是 hypersimplex
Delta(4,n) 再加 sum_(i in H)y_i<=3 的截断，S11 真计数给

    delta_v(x)=h*_(Delta(4,n))(x)−h*_(P_v)(x)。

两个都是整数多面体，Ehrhart h* 系数非负；其系数和为同一格点归一化体积。
P_v包含于Delta(4,n)，故 vol(P_v)<=vol(Delta(4,n))。
均匀 hypersimplex 的体积为 Eulerian 数 A(n−1,3)<=4^(n−1)。
最后界也可由排列的四个递增 run 编码为每个元素所属 run 得到注入。
所以，不需要 delta_v 非负，仍有

    sum_j |[x^j]delta_v|<=2*4^(n−1)。                 (2)

S24§1的准确 Newton 多项式和负整数零点，逐个合法 n,v 均适用，
不是其仅固定 Q 的后续渐近常数。它给 deg delta_v<=v，常数0。
具体是坏cap计数次数<=n−1，且 k=0,−1,...,−(n−v−1)皆为零；
Euler 反转得到 delta_v 的次数<=v。该纯代数量词可独立核对。
因此 u=t^4>=1 时

    |delta_v(−u)|<=2*4^(n−1)u^v。                    (3)

不得从(2)错误推断 delta_v 各系数非负；也未用 C_v 随 v 增大的固定参数高度。

## 3. 大 r 的共同谱预算

u=r³(r+K)/S，S~1+K，d=|1−r exp(i theta)|~r，R=(1+u)/d。
r>=2 时共同有

    c r³<=u<=C r^4，R>=c u/r。

因 n/r->infinity，最终 r<=n。驻点关系 n=q(4+3K/r) 给 K<=nr/(3q)<=n²。
准确方差（沿 S42/S43R1）为

    Sigma²=K² nr(1−p)(3K+4cos theta)/(4r+3K)²
              <=C nr(1+K)<=Cn^4。

三元 packing 给附加 H 数量<=binom(n,3)<=Cn³，且 v<=q+2。
由(3)，除以 R^n rho^(-q)|H|，用 rho^q<=1、Sigma<=Cn² 得

    相对误差<=C n^5 u² [4u^p/R]^n
       <=C n^13 [C r u^(p−1)]^n
       <=C n^13 [C r^(-5/4)]^n ->0，                  (4)

因为 p=q/n<1/4、u>=cr³，故 u^(p−1)<=u^(-3/4)<=Cr^(-9/4)。
任意 r->infinity 的 n 次谱比共同支付固定 n 幂；不需要 q>=log n，
不靠可能接近一的 rho^q 支付多项式数量。

## 4. 接合与未付范围

(4)证明(1)，与 S38/S39 的单 H 分离式接合后可支付整个 M 的大端增长中带。
这项接合只能在本页独审通过并由主线程核依赖后登记。
正紧 r 的全部附加 H、宏观原端（nr有界）与倒端有限盘（n/r有界）及准确根数
均不包含在本页。统一系数高度不自动支付正紧 r 的相对预算。
全部 INTERNAL_HOLD，无写作、Git 或发布。
