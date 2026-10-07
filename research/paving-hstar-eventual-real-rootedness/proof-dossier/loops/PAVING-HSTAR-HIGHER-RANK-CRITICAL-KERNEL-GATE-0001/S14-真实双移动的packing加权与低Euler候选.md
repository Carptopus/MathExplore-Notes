# 真实双移动：packing加权与低Euler

2026-10-05，主线程冻结候选，尚未独审。
依赖S11准确全容斥、S12固定中带及S13全秩最高内容移动累计；
S13仍候选，不能把本页写成已证。全部同线内部HOLD。

## 1. 目标与量词

固定r>=4，d=r−1、p=d/r、m=n−1；连通rank-r paving M，
maxH<=D−1、D=n−ceil(n/r)。设t>0、m min(t,1/t)→infinity。
候选在全部实际相位网格n phi_r(t)=j pi统一有

    (−1)^j h*_M(−t^r)/R_r(t)^n >=1/r−o(1)。              (1)

这里共同于M；不支付两个有限缩放端盘根数，仍非完整全轴。
S12已付固定t正紧域，以下只处理t→0和t→infinity。
由超平面(r−1)子集互不重复，

    sum_H binom(s_H,d)<=binom(n,d)，sum_H s_H^d<=C_r n^d。 (2)

不是只使用#H<=n^d来乘一个可能缓慢消失的指数。

## 2. 原端小H的最高Euler加权，不留n前因子

t→0，kappa=mt→infinity。Q0为S11坏cap正计数，
在|x|=t^r<1普通收敛级数内可取绝对值，

    |sum_(small H) K_(r,m,s_H)(−t^r)|
      <=A^n sum_(k>=1) t^(rk) sum_(small H) Q_(0,H)(k)。

固定小delta>0，small表示s<=delta n。取a=(r+1)delta<1。
先1<=k<=delta n，0<=J<=k−1，L=rk−J>=dk+1>d。
Q0内两项为(s)_L/L!及(q)_J/J!（上升阶乘）。
(s)_d<=C_r s^d，剩余L−d因子<=s+L<=(r+1)delta n；
(q)_J<=(2n)^J。因此(2)给

    sum_(small H) Q0(k)
       <=C_r n^(rk) sum_(J=0..k−1) a^(rk−J−d)2^J/(L!J!)
       <=C_r n^(rk) a^(d(k−1)+1) 3^(rk)/(rk)!。

最后用L−d>=d(k−1)+1，a<=1，且sum_J binom(rk,J)2^J<=3^(rk)。
乘t^(rk)并求k得上界
C_r a^(1−d) exp(3 a^(d/r)nt)。
选delta仅依r，使3a^(d/r)<cos(pi/r)/4。
log(R_r/A)/t→cos(pi/r)，故上述部分除R_r^n指数衰减exp(−c_r nt)。

尾k>delta n不再使用上述低k界。所有Q0<=W0=binom(rk+n−1,n−1)，
H数仅多项式，取固定0<a0<1（例如1/2），

    sum_(k>delta n) W0(k)t^(rk)
       <=(t/a0)^(r delta n)(1−a0)^(−n)。

由于t→0，这乘任意固定n多项式最终<=exp(−n)，从而<=exp(−c_r nt)。
两部分共同，全部small H最高内容和/R_r^n趋0；没有n^d exp(−c nt)残留。

## 3. 原端所有低Euler，正计数上界保留shift

h=1..r−2，l=r−h，Q_h求和0<=J<=k−1且
L=lk−h−J>=0；无非负总数时原计数0。系数binom(s,h)<=s^h/h!。
用s^h(s)_L<=(s)_(L+h)。
取固定delta0<1/r，仅先核k<=delta0 n。

若L+h>=d，以(2)抽前d阶，剩余因子<=n+rk<=C_r n，
外部(q)_J亦<=C_r^J n^J。故对每k相应全部H和满足

    sum_H binom(s,h) Q_h(k)
       <=C_r (C_r n)^(lk) 2^(lk−h)/(lk−h)!，             (3)

只需对满足L+h>=d的J项使用右端。这里L+h+J=lk；
保留了−h shift，不能换成rk再遗漏t的额外幂。
同样binom(n,h)W_h(k)有(C_r n)^(lk)/(lk−h)!上界。
乘t^(rk)，令Z_l=C_r n t^(r/l)，对应整项和<=C_r Z_l^h exp(Z_l)。
Z_l/(nt)=C_r t^(h/l)→0，故除R_r^n并乘A^n后
至多C_r(1+(nt)^h)exp(−c_r nt)，无n前因子。

若L+h<d，则(l−1)k+1<=L+h<d，k<=d−2，仅有限k/J。
全部H和以sum s^d<=C_r n^d支付，外部因子<=C_r n^J。
于是乘t^(rk)后<=C_r(nt)^(rk)n^(d+J−rk)；
d+J<=d+k−1、rk−d−k+1=d(k−1)+1>=1，至多多项式(nt)/n。
除R_r^n并乘A^n后仍被exp(−c_r nt)支付。
这些有限例不能按非整数负下标阶乘合并入(3)。

k>delta0 n的全部低Euler尾：容斥/H权重至多n的固定幂，
Q_h,W_h<=W0。按第2节固定a0尾界共同支付为exp(−n)。
h=r−1的一色孤立项，系数至多C_r n^d、项x^d，
其绝对值/R_r^n<=C_r (nt)^d t^((r−1)d)exp(−c_r nt)→0。
综上完整低Euler共同消失，不需nt比log n更快发散。

## 4. 原端大H：只对有限个调用完整CDF

s>delta n的H数量由(2)有固定上界C_r delta^(−d)。
仍取alpha_*=(p+1/2)/2>1/2。
若无H超过alpha_* n，所有大H有固定subcritical间隙；
否则至多一个超过alpha_* n，其他H大小<=n−s+r−2，亦与p留固定间隙。
对非临界大H，S13的xi<=(−epsilon m)sqrt(t/m)=−epsilon sqrt(mt)→−infinity，
完整非中心累计给每个o(1)，数量固定后仍o(1)。
唯一可能临界H因s<pm以S13的半幅界支付<=1/r+o(1)。
Uniform主两分支为2/r，其他分支gap exp(−c nt)，
结合§2–3真实校正给原端(1)。没有将多项式数量个o(1)直接累加。

## 5. 倒端：低Euler谱与小H次数预算

t→infinity、m/t→infinity。S11低颜色R_l/R_r=O(t^(−h/l))，
固定l的相似起止向量范数、有限band的A^j及所有权重至多
n的固定幂乘t的固定幂，因此全部低Euler/R_r^n为

    <=C_r n^(2r) t^(C_r)(C_r t^(−1/(r−1)))^n →0。

一色x^d也按相同型支付。此处n log t吸收log n和log t，
与原端“nt缓慢发散”不同，不偷用固定紧域常数。

取固定delta<p/2。S10矩阵在正x的全部内容/Euler系数非负；
每内容a<m的计数多项式含k=−1,...,−(m−a−1)零点，
Euler互反给degree [u^a]B_m<=a+1，因此degree K_(r,m,s)<=s。
该次数界也可按矩阵下降次数解释；不以有限插值获得。
x1时M0全1，B_m(u,1)=(1+d u)^m，
所以K(1)=sum_(a<s)binom(m,a)d^a<=r^m。
t>=1给|K(−t^r)|<=t^(rs)K(1)。
small s<=delta n的全部H经#H<=n^d，有

    sum_(small H)|K|/R_r^n
       <=n^d(C_r t^(r delta−d))^n →0。

剩余大H数量固定，按§4与S13移动CDF处理；非临界xi<=−epsilon sqrt(mt)→−infinity，
唯一临界者半幅<=1/r+o(1)。Uniform其他r−2支gap exp(−c n/t)，
故倒端(1)成立。固定域由S12，三种子列覆盖全部移动序列。

## 6. 剩余边界

本页即使PASS，也只付m min(t,1/t)发散区的实际保号。
有限nt原端、有限n/t倒端的共同根计数/盘与网格匹配仍需接合；
rank4可使用S9四次全缺口及真实固定盘，但不可未经联合审计写全轴。
巨H、全部小n、全部r>=5倒端有限缺口、新颖性均不由此继承。
