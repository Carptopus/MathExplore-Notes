# Technical proof dossier for *Eventual real-rootedness in paving-matroid base polytopes*

This dossier is part of the manuscript, not a historical bibliography.  The main
paper gives the definitions, exact theorem statements, and assembly arguments;
the long uniform contour estimates and endpoint kernel arguments are supplied by
the frozen proof records listed below.  Publication artifacts must contain this
file, every listed record, and the ordered 216-file SHA-256 manifest
`loops/PAVING-HSTAR-PUBLICATION-PREP-0001/A1-证明依赖闭包.sha256`.
Changing any listed byte invalidates the manuscript audit.

The labels `PASS`, `candidate`, and `HOLD` appearing in the dated records are
historical workflow metadata.  They are not mathematical hypotheses and are not
used in the proofs.  Only the displayed identities, estimates, certificates,
and quantifiers are used.

## D1. Exact Ehrhart correction formula

- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S10-全秩内容矩阵的准确谱与复方差入口.md`
- its frozen revision `S10R1`
- `S11-真实全容斥与低Euler谱分离候选.md`

These records prove the common-denominator formula (2.1)--(2.9), including the
full inclusion--exclusion over every effective hyperplane and every lower Euler
layer.  They are the algebraic input to all analytic estimates below.

## D2. Fixed-rank central and bounded-excess estimates

- `loops/PAVING-HSTAR-CROSS-RANK-FACT-GATE-0001/S18-中间小t区的解析谱隙桥.md`
- `loops/PAVING-HSTAR-CROSS-RANK-FACT-GATE-0001/S14-增长秩紧中带的定量谱隙与真实保号.md`
- `loops/PAVING-HSTAR-CROSS-RANK-FACT-GATE-0001/S15-增长秩倒端移动保号的双区定量桥.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S90-全部固定秩全缺口临界核联合候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S59-全固定秩非负临界超额带实际全轴候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S91-全固定秩有界临界超额的真实全轴联合候选.md`

The S91 proof is independent of Proposition 3.1 outside its stated density
range.  In the band (D_u\le s\le D_u+C), it uses the exact fixed increment
parameters

\[
 b_u=r\lceil n/r\rceil-n,
 \quad \ell=\left\lceil\frac{\delta+1-b_u}{r-1}\right\rceil,
 \quad c=\lceil n/r\rceil+\ell,
 \quad b=b_u+r\ell,
 \quad a=(r-1)\ell+b_u-\delta-1,
\]

and proves directly that the bounded shift of the highest cutoff changes the
two-moving local expansion by (\exp(O(\sigma))-1=o(1)), while the lower-Euler
and packing errors remain (o(1/r)).  This is the input used in Lemma 5.1.

## D3. Fixed complement and rank-three interfaces

- `loops/PAVING-HSTAR-FIXED-OUTSIDE-GATE-0001/S1-固定外部数二项式矩与完整候选.md`
- `loops/PAVING-HSTAR-FIXED-OUTSIDE-GATE-0001/S2-秩三真实校正与两端极限候选.md`
- `loops/PAVING-HSTAR-MOVING-CRITICAL-GATE-0001/S22-秩三最终全类的联合候选与证据门.md`
- its mathematical revision `S22R1-巨H正因子依赖绑定.md`
- `S24-最终秩三自然整类结算与跨秩接口.md`
- `loops/PAVING-HSTAR-GIANT-H-DEPENDENCIES-GATE-0001/S9-全部亚线性整类与近一宏观范围全轴候选.md`
- its dependency revision `S9R1-全部亚线性完整包依赖修订.md`
- `loops/PAVING-HSTAR-GIANT-H-DEPENDENCIES-GATE-0001/S16-临界邻域整类全轴同伦候选.md`
- `loops/PAVING-HSTAR-GIANT-H-DEPENDENCIES-GATE-0001/S19-全正比例双端点间隙完整候选.md`
- its mathematical revision `S19R1-大域正因子与双端点证书修订.md`
- `loops/PAVING-HSTAR-GIANT-H-DEPENDENCIES-GATE-0001/S20-全部巨H依赖整类统一实际全轴候选.md`

For each fixed outside size (q\ge2), S1 proves the rank-(r\ge4) theorem by
an exact finite binomial-moment expansion and a three-region homotopy.  S2 gives
the separate rank-three proof; it does not invoke the false (k=2) general
perturbation box.  S20 supplies the all-attached-hyperplanes giant-region
theorem.  S22 supplies the remaining rank-three failure-sequence exhaustion,
including the continuous negative-axis certificate and the exact complex-
circle counts.

## D4. Giant-hyperplane middle and endpoint estimates

- `loops/PAVING-HSTAR-TWO-MACRO-GATE-0001/S3-秩至少四全部宏观谱统一候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-GEOMETRY-GATE-0001/S1-一般秩全圆最小模的角区排除候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-GEOMETRY-GATE-0001/S2-一般秩准确累计积分与移动中央预算候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-MOVING-GATE-0001/S3-一般秩小端分离累计完整积分候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-MOVING-GATE-0001/S4-一般秩正紧驻点模完整积分候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-MOVING-GATE-0001/S5-一般秩大端有界K的完整积分候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-MOVING-GATE-0001/S6-大端共同无界多峰相对尾候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-MOVING-GATE-0001/S7-一般秩有界累计窗与分离域接合候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-MOVING-GATE-0001/S8-全一般秩分离累计的联合量词候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-MOVING-GATE-0001/S9-最高累计全移动两域接合候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-ACTUAL-GATE-0001/S6-圆盘极化直接排除多标记谱候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-ACTUAL-GATE-0001/S7-全部实际移动两域联合候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-ACTUAL-GATE-0001/S8-实际移动中带结算与端层入口.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-ENDPOINT-GATE-0001/S2-一般Wright相位圆准确索引候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-ENDPOINT-GATE-0001/S4-一般秩发散巨H倒端与准确圆候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-ENDPOINT-GATE-0001/S5-一般秩巨H双端连续相位接合候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-ENDPOINT-GATE-0001/S6-一般秩亚临界巨H实际全轴联合候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-CRITICAL-MOVING-GATE-0001/S1-全秩临界与分离基础相位符号候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-CRITICAL-MOVING-GATE-0001/S2-全秩巨H临界宏观基础圈准确索引候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-CRITICAL-MOVING-GATE-0001/S3-全秩慢发散临界倒端准确相位候选.md`
- `loops/PAVING-HSTAR-GENERAL-RANK-GIANT-CRITICAL-MOVING-GATE-0001/S4-全秩临界移动实际全轴联合候选.md`

Together these records prove the four-parameter finite gate in Proposition 3.4,
the exact Wright/Beta direct circles, the reciprocal factorial circles, and the
continuity/first-hit assembly.  In particular, the endpoint counts are full
complex-circle argument-principle counts, not deductions from a single
negative-axis sign.

## D5. Rank-four exhaustion

- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S50-稀外部原端B核的准确三支相位索引候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S51-Wright原端的全扇区无穷相位候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S52-稀外部实际全轴的准确双端计数候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S53-巨H固定宏观比例的原端索引与实际全轴候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S54-临界与分离共同基础相位符号门候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S55-全部巨H宏观比例的基础圆准确索引候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S56-移动临界巨H的准确全轴计数候选.md`
- `loops/PAVING-HSTAR-HIGHER-RANK-CRITICAL-KERNEL-GATE-0001/S57-完整秩四自然整类的联合穷尽候选.md`

The S50--S56 records prove, respectively, the sparse-outside direct endpoint,
Wright-sector phase, sparse-outside full axis, fixed macroscopic profile,
critical/separated sign gate, macroscopic endpoint index, and moving-critical
full-axis theorem.  S57 gives the exhaustive subsequence argument and the
disconnected classification used in Theorem 1.1.

## D6. Growing-rank window

- `loops/PAVING-HSTAR-CROSS-RANK-FACT-GATE-0001/S4-增长秩真实倒端定量桥候选.md`
- `loops/PAVING-HSTAR-CROSS-RANK-FACT-GATE-0001/S15-增长秩倒端移动保号的双区定量桥.md`
- `loops/PAVING-HSTAR-CROSS-RANK-FACT-GATE-0001/S19-显式增长秩下的渐近全实根候选.md`
- `loops/PAVING-HSTAR-CROSS-RANK-FACT-GATE-0001/S20-S17门下的完整原端保号.md`

S19 gives the complete arithmetic assembly: the direct grid contributes
(D-K-J) roots, the reciprocal disk contributes (K-1), and the last sign
gap contributes one.  The reciprocal estimate is a uniform Rouché inequality
on the whole circle, as recorded in S4; no finite negative-axis test substitutes
for that estimate.

## D7. Finite exact guards

The manifest contains six frozen certificate programs and their exact outputs.  They
certify only the rational inequalities and continuous box covers stated in
their headers.  Each includes its prescribed positive, negative, or destructive
control.  The analytic deductions from those inequalities remain in D1--D6.

