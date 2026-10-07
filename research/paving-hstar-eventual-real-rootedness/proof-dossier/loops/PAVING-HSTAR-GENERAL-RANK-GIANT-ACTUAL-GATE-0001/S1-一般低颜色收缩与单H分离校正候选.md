# 一般低颜色收缩：单H分离低Euler

2026-10-06，固定r>=5、d=r-1，未独审，内部HOLD。
准确全容斥依赖旧critical-kernel门S11；最高T符号依赖前导MOVING门S8。
本页只有真实单H，不覆盖其他H，不是全根结论。

## 1. 冻结结论和准确单H有限band

M单独有有效超平面大小s=n-q，其真实h*记P_single；
2<=q<n/r，q、n-rq、nh、n/h、Sigma趋无穷。
候选共同有

    P_single(-t^r)-T_(r,n-1,q)(-t^r)=o(M)。         (1)

对j=1,...,r-2，l=r-j、e=l-1=d-j，设

    W_j=sum_(z=0..j)(-1)^z binom(j,z) A^z U_(l,n-z)，
    R_j=sum_(z=0..j)(-1)^z binom(j,z) A^z T_(l,n-1-z,q)。

T_(l,.,q)是同一x的一色最高q项累计，A仍1-x，不把x改为-t^l。
由S11的Q_j有限band及总内容U_l减其最高q项，准确

    P_single-T
       =sum_(j=1..r-2)(-1)^j {
          [binom(n,j)-binom(s,j)] W_j+binom(s,j)R_j}
         +(-1)^d[binom(n,d)-binom(s,d)]x^d。        (2)

原length n-z与cap s-z相减保持最高项数q，不能把q也改为q-z。
最后l=1项单独保留；不制造不存在的非起始一色指标。

## 2. 全低颜色收缩：正规范数替代特殊因式分解

记tau=t^r、D=|1-W|、R=A/D。对2<=l<=d，低色uniform正规矩阵
最大谱模为

    R_l=A/|1-tau^(1/l)exp(i pi/l)|。

S11的指数-角比较对同一tau给R_l<=R_d。
前导全圆几何D<|1-tau^(1/d)exp(i pi/d)|，故R_d<R。
低色一色标记矩阵在准确相似正规基为C_l diag(1,...,v,...,1)，
|v|<=1时其算子范数不超过R_l；这里不要求l=2的非零角严格谱隙。

因此在|lambda|=R上，低色特征式不可能有|v|<=1的根。解出

    Y_e=(1-w)w^e/(w^e+tau)， v_e=1/Y_e，

得到全角|Y_e|<1；w0延拓Y_e0。所有低色真pole位于lambda圆内。
这是准确全角结构，不是采样或仅领先点的比较。

## 3. 原准确圆上的有限J身份

置X=1-w=A/lambda，

    J_(e,q)=Y_e^q/w+sum_(k=1..q-1)Y_e^k。

上述pole内置和n>q+j使lambda0解析；w0为可去。准确

    R_j=(1/(2pi)) integral lambda^n w^j J_(e,q)dphi。

从有限和直接得两种完整身份

    w^j(J_(e,q)-X/w)
      =-tau X w^(j-1)/(w^e+tau) sum_(k=0..q-1)Y_e^k，    (3)
    w^j J_(e,q)
      =X w^d/(w^l+tau)
        +tau X w^(j-1)/(w^l+tau)Y_e^q。                 (4)

(3)被扣基线w^(j-1)X是X的j次多项式，n>j时整圆积分0。
(4)仅在w^l+tau共同离圆时允许分拆，首项整圆恰W_j。
uniform根过滤亦给|W_j|<=C tau^(j/l)R_l^n。

## 4. 小h：相对预算只留N=nh

h在充分小共同阈值，D~1、min|w|>=ch，tau<=C h^d，
|w^e+tau|>=c|w|^e。用(3)和|Y_e|<=1得

    |R_j|/R^n<=C q tau integral |w|^(2j-r)dphi。

该积分：r-2j>1时至多C h^(2j-d)；等于1时至多C log(1/h)；
小于1时共同有界。乘n^j后全部<=C(1+N)^d：
第一类用q h^j<=N，第三类用d>=j+1；第二类d=2j且j>=2，
额外h^(j-1)log(1/h)共同有界。故不会留下log n或n独立幂。

差权重<=Cq n^(j-1)，tau^(j/l)<=C h^j，R_l<R，
对应uniform项亦至多C(1+N)^d R^n。孤立tau^d项同样由N^d支付。
|H|与Sigma^-1共同可比，因H=(1-p)/(dK sqrt(2pi nV))。
完整相对预算至多

    C Sigma(1+N)^d rho^q。                           (5)

K<=1时Sigma与a sqrt(N)可比，q log(1/rho)与Sigma sqrt(N)可比，
Sigma发散吸收全部N幂。K>=1时N=q(rh+dK)<=CqK，Sigma<=CK sqrt(q)，
rho<=(1+K+K²)^(-1/2)，q次幂共同吸收全部固定q/K幂。

## 5. 正紧h

tau、D、w共同有界；tau正下界，Y_e/w的w0延拓共同有界。
有限J、|Y_e|<=1给|w^jJ|<=Cq；所有项及权重只有n固定幂。
K<=1时q~n，Sigma~K sqrt(n)，nK~Sigma sqrt(n)趋无穷，
rho^q<=exp(-c nK)支付全部n幂。K>=1时n<=Cq(1+K)、Sigma<=CK sqrt(q)，
相同q次幂支付全部固定幂。没有在K无穷端遗留n独立变量。

## 6. 大h

n/h发散保证最终h<=n。
K>=1时n=q(r+dK/h)<=Cq(1+K)，tau<=C h^r<=C n^r。
|w|~h，有限J和|Y_e|<=1给每R_j只含q,h固定幂；uniform残数与孤立项
也只有n固定幂。Sigma<=CK sqrt(q)，故rho^q吸收全部固定q/K幂。

K<1时q~n、tau~h^r、|w|~h，

    |Y_e|<=C h^(-j)， |w^l+tau|>=c tau，
    R_l/R<=C h^(-j/l)。

可合法用(4)，将其中W_j与(2)原uniform项合并成binom(n,j)W_j。
W_j振幅、权重、Sigma至多n固定幂，而(C h^(-j/l))^n共同压制它们。
(4)余项至多C R^n h^j(C h^(-j))^q；乘权重后q~n、h<=n，
即使rho^q<=1也由h的q次幂吸收全部n幂。孤立x^d项用R>=c h^d同型支付。
本域不是靠可能很小的qK指数错误支付n幂。

三类h失败子序列反证闭合(1)。依赖前导S8的同一M，尚未单独审计。
下一组件是Sigma有界实际全部M，以及分离域附加H；单H不关闭actual整门。
