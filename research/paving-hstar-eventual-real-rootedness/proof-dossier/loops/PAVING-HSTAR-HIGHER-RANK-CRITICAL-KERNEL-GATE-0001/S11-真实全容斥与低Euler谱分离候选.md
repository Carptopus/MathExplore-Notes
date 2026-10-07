# 真实paving全容斥与低Euler谱分离

2026-10-05，主线程一般推导冻结候选，尚未独审。
S10+S10R1仅作为准确内容身份依赖，不继承实际根性。

## 1. 对象与形式约定

固定整数r>=4，连通rank-r paving M有n个元素；m=n−1，n充分大。
有效超平面H大小s>=r，外部q=n−s>=2；不同H交至多r−2。
无有效H为uniform。令A=1−x。
所有Euler和先按形式x级数建立，经有理约分得到多项式，
再在x=−t^r、t>0评价；不数值求和x<=−1的发散级数。
二项式上标可为整数变量，下标非负，按下降乘积多项式；下标0恒为1。
在实际非负计数中上指标非负但不足下标时取0。

定义最高完整项

    U_(l,n)(x)=A^n sum_(k>=0) binom(lk+n−1,n−1)x^k，l>=1。

对l>=2，取S10的l色矩阵（a任一非0），B_m^(l)(u,x)=e0^T M_l(u,x)^m 1，
K_(l,m,s)=sum_(a=0..s−1)[u^a]B_m^(l)，s<=m。
S10谱严格间隙只用于l>=3；l2的准确GF与酉范数仍可用。

## 2. 无坐标上界的真实cap身份

先取n个非负整数总和rk，要求指定s个坐标之和<= (r−1)k。
此保留计数准确为

    L_A(k)=sum_(a=s..m) binom((r−1)k+a,a)binom(k+m−a−1,m−a)。   (1)

证明不靠秩三插值。k>=1时，把第s+1个坐标从外部移入内部，
相邻保留集的差要求原内部和c<= (r−1)k、新内部和超阈值。
固定c，剩余q−1个外部坐标之和y<=k−1；被移坐标由总和唯一确定。
两次hockey-stick给该差恰
binom((r−1)k+s,s)binom(k+q−2,q−1)，即式(1)的a=s项。
最终s=m时仅一个外部坐标，其保留数为binom((r−1)k+m,m)，完成望远镜。
s0以空内部计数或Vandermonde成立；k0仅a=m贡献1，亦准确。
因此最高Euler保留项是U_(r,n)−K_(r,m,s)。

## 3. 所有坐标上界的低阶shift身份

原始真实计数来自Hanely等的paving基多面体约束及有限容斥，
准确父接口见 ../PAVING-HSTAR-FINITE-MACRO-BRIDGE-0001/S4-全Euler的固定秩尾概率接口.md。
对h=0..r−1，设l=r−h，

    W_h(k)=binom(lk+m−h,m)，
    Q_h(k)=sum_(J=0..k−1)binom(J+q−1,q−1)binom(lk−h−J+s−1,s−1)。

所有坐标减k+1；总和lk−h；若选外部越界坐标，则坏cap外部和<k不可能。
于是单H坏cap经上界容斥为sum_h (−1)^h binom(s,h)Q_h。
不同坏cap在坐标<=k域不相交：两H同时内部和>(r−1)k将迫使
总和>2(r−1)k−(r−2)k=rk，矛盾。故多H可准确相加。
真实Euler h*为

    h*_M= sum_(h=0..r−1)(−1)^h binom(n,h) E(W_h)
       −sum_H sum_(h=0..r−1)(−1)^h binom(s_H,h) E(Q_(h,H))，   (2)

其中E(f)=A^n sum_(k>=0) f(k)x^k。

对0<=h<=r−2，准确有

    Q_h(k)=sum_(a=0..s−1)
       binom((l−1)k−h+a,a)binom(k+m−a−1,m−a)。              (3)

当(l−1)k−h>=0，按第2节同一阈值望远镜取坏cap补集。
当该量为−c<0，1<=c<=h<s，第一二项式仅a<c可非零；
整a0..m的Vandermonde和就是W_h，因此截断a<s已等于全和。
此时总和lk−h<k，Q_h确等于W_h；若总和为负则W_h=0（m>=h），
并由上述多项式求和相消为0，而不把负试验数解释为概率。
k0两个实际量皆0(h>0)，式(3)亦0；h0的Q0为空。

形式长度/内容GF准确为

    sum_m sum_a E(f_(h,a,m)) u^a y^m
      = A(1−Ay)(1−Auy)^(r−2)
         /[(1−Ay)(1−Auy)^(l−1)−x]
      = (1−Auy)^h sum_m B_m^(l)(u,x)y^m。

推导先展开第一二项式为(1−Auy)^(h−(l−1)k−1)，
第二为(1−Ay)^(−k)，再取x几何和；这里只求非负m/a且a<=m。
因此准确有限band身份

    E(Q_h)=sum_(j=0..h)(−1)^j binom(h,j) A^j K_(l,m−j,s−j)，
    E(W_h)=sum_(j=0..h)(−1)^j binom(h,j) A^j U_(l,n−j)。      (4)

n大于r、s>=r保证下标有效。h=r−1即l1时Q_h=W_h，
E(W_h)=x^(r−1)，单独保留，不调用不存在的非0一色指标。
由(2)-(4)，真实h*=U_(r,n)−sum_H K_(r,m,s_H)+低Euler有限band，
而不是只比较一个删掉坐标上界的模型。

## 4. 全秩较低颜色谱严格分离

x=−t^r。对2<=l<r，写tau=t^(r/l)，

    R_l(t)=A/sqrt(1−2tau cos(pi/l)+tau²)，
    R_r(t)=A/sqrt(1−2t cos(pi/r)+t²)。

准确R_l<R_r，所有t>0。令phi=pi/r，a=log t，
F(v)=1−2exp(va)cos(v phi)+exp(2va)，1<=v<=r/2。
若a>=0，F'(v)>0显然。若a<0，y=−va>=0、theta=v phi∈(0,pi/2]，

    v F'(v)/(2exp(va))=theta sin theta−y(exp(−y)−cos theta)>0。

理由：y exp(−y)<=1−exp(−y)，且exp(−y)+y cos theta>=cos theta
（y<=1用exp(−y)>=1−y，y>=1用y cos theta>=cos theta），
故第二项<=1−cos theta<theta sin theta。取v=r/l给严格比较。

固定t正紧区间上谱比有共同eta<1。单位u圆的D_a(u)酉，
相似正规矩阵范数等于R_l，即使l2无非零角严格隙也足以得
|[u^a]B_(m−j)^(l)|<=C R_l^(m−j)，C不依a,n,s。
累计至多n项；式(4)仅h+1项。完整U_l也由单位根过滤有同界。
H数量<=binom(n,r−1)，各binom(s,h)<=n^h，因此低Euler全项在紧t域满足

    |h*_M−U_(r,n)+sum_H K_(r,m,s_H)|/R_r^n
       <=C n^(2r) eta^n。                              (5)

其中孤立x^(r−1)项用min R_r>1支付：t<=1时2t cos(phi)−t²>0，
t>=1时2t^r−t²>0，故A²−(1−2t cos(phi)+t²)>0。
常数依固定r和紧区间，不依对象/H数。不是两个移动端的量化界。

## 5. 结论边界

本页候选支付真实单/多H全容斥与固定中轴低Euler指数预算。
尚未由本页证明最高K的临界累计保号、移动端点或全根性。
所有新材料内部HOLD；与既有同线结果合并，不写稿/提交/发布。
