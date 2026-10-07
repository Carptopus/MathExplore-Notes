# S43 修订：保留外部坐标的三阶 packing

2026-10-06。原 S43 冻结不改；本页修订其第5节，而非追认原尺度推理。
有效候选组合为 S43 的§1–§4、§6及本页替换§5。
目标与量词不变，尚待定向独立复核。

## 1. 原缺陷

S43§5误写 Sigma<=CK sqrt(N0) 并据此推断 n=o(N0^(3/2))。
准确公式是

    Re V=p²(1−p)(3K+4cos theta)/r，
    Sigma²=K²N0(1−p)(3K+4cos theta)/(4r+3K)²。

在 p>=delta、K=ar/(3p)=O_delta(r) 下，Sigma~(K/r)sqrt(N0)，
不含上述额外 r 因子。合法 p=1/8、r=(log n)/n 即反驳原 n 幂转换。
Sigma 发散不能支付任意 n³exp(−cN0) 包络。
原主张不是由此被反驳；需重新支付数量前因子。

## 2. 三阶余项保留真实外部 n−v

沿 S43 的正级数，真实内部总和 L>=4。每个 v>=5 的坏 cap 正级数满足

    sum_k Q_v(k)u^k
      <= C v³ eta³(1−eta)^(-v−3)(1−zeta)^(-(n−v))，   (1)

因为内部 L>=3 的三阶 Taylor 余项给 Cv³eta³(1−eta)^(-v−3)，
外部仍有 n−v 个坐标，不把它粗增为 n。
外部 packing 给 sum v³<=Cq³。eta>zeta 时，
(1−eta)^(-v)(1−zeta)^(-(n−v)) 随 v 单调增，v<=q+2，故

    sum_(v>=5) sum_k Q_v(k)u^k
      <= C(q eta)^3(1−eta)^(-3)
                      (1−eta)^(-(q+2))(1−zeta)^(-(n−q−2))。 (2)

准确坏 cap 的 Euler 绝对值再乘 A^n；除 R^n 是乘 d^n。
这仍是整个无限级数上界，没有引入有限 k 试探或坐标上界遗漏。

## 3. 替换原§5的完整预算

固定 delta<=p<1/4，r->0，K=O_delta(r)。沿原合法标记

    eta=t[3(1−p)/p]^(1/4)，zeta=u/eta³，

eta>zeta、eta>t，两者均 O_delta(r)。
式(2)指数仍精确为

    n[p eta+(1−p)zeta]+O_delta(nr²+r)
      =N0[4sqrt(p(1−p))/3+O_delta(r)]。

log d=−r/sqrt(2)+O_delta(r²)，且
4sqrt(p(1−p))/3<=1/sqrt(3)<1/sqrt(2)，故严格总衰减<=exp(−c_delta N0)。

前因子现为 (q eta)^3(1−eta)^(-3)<=C_delta N0³，
准确方差给 Sigma<=C sqrt(N0)，rho^q<=1。
因此相对误差至多

    C_delta N0^(7/2)exp(−c_delta N0)->0。              (3)

无需也不宣称 n 与 N0 的任何多项式关系；允许 N0=log n、loglog n 或其他
任意缓慢发散速度。修订只删除错误数量预算，不改变原严格指数间隙。

原§3的 K>=1 与§4的 K<1、p<delta 没有使用错误尺度转换，保持原证明；
两者 Sigma<=CKsqrt(q) 和 Sigma<=Csqrt(N0) 由上面的准确方差直接得出。
本页与原§1–§4合并仍只是小端>=5相对校正，不含紧r、大r、端盘和根数。
全部 INTERNAL_HOLD，无写作、Git 或发布。
