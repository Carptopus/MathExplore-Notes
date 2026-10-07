# 有界Sigma：一般秩真实全部M

2026-10-06，固定r>=5、d=r-1，未独审，内部HOLD。
冻结对象与移动核心见本门研究计划；依赖准确S11全容斥、S13全r内容CDF，
S14低Euler和small-H加权子证明，以及前导MOVING有效S7+R1+R2的尺度连接。
不从S14的总maxH限制标签直接继承新量词。

## 1. 主张及准确分解

M_n为任意连通rank-r paving，最大有效H0大小s0=n-q，2<=q<n/r，
q、n-rq、nh、n/h发散；Sigma留任意固定有界窗。候选共同于全部M_n：

    h*_M(-t^r)-T_(r,n-1,q)(-t^r)=o(R_r(t)^n)。      (1)

准确全容斥S11给

    h*_M=U_(r,n)-sum_H K_(r,n-1,s_H)+L_M，
    T=U_(r,n)-K_(r,n-1,s0)。

所以只需支付L_M及sum_(H!=H0)K_H。
此处R_r是uniform领先模，不是分离驻点R；不可外推为o(M)。

## 2. 低Euler子证明没有使用maxH上界

任意连通paving所有有效H都有packing

    sum_H binom(s_H,d)<=binom(n,d)， sum_H s_H^d<=C_r n^d。

S14 §3低Euler证明只用该式和s_H<=n，不用maxH<=D-1；其§4半幅
步骤才用该上界。提取§3、§5低Euler部分与S11紧域式，得到

    L_M(-t^r)=o(R_r^n)

沿任意n min(t,1/t)发散序列，共同于M。具体支付如下，不只凭旧标题：

- 正紧t：全部低色谱比<=eta<1，完整band和权重给C n^(2r)eta^n。
- 小t：移除j=1,...,r-2坐标后l=r-j，低计数L=lk-j-J，J<=k-1。
  L+j>=d时抽packing前d阶，完整n幂只有lk，保留(lk-j)!；
  求和是Z_l^j exp(Z_l)，Z_l=C n t^(r/l)=o(nt)。
  L+j<d的有限k/J用C n^d和外部n^J，指数rk-d-J>=1，
  留下多项式(nt)/n，而不是不可支付n独立幂。高k固定比例尾用a0
  完整W0上界支付exp(-n)。最后一色x^d按实际tau^d与packing系数支付。
- 大t：低色谱比O(t^(-1/d))、起止向量及全部band只留n,t固定幂，
  C n^(2r)t^C(C t^(-1/d))^n趋0，一色孤立项同型。

有界Sigma前导尺度给h/t趋1，故本门nh、n/h支付n min(t,1/t)发散。
没有把整个S14最高项半幅结论用于巨H。

## 3. 其他H的范围与packing

不同有效H交至多r-2，所以s_H<=q+r-2。前导有界Sigma给q/n趋1/r，
因而所有H!=H0最终共同满足s_H<=2n/r。
这是与d(n-1)/r的固定间隙（d>2），无需各H选择不同门。

选固定充分小delta>0。s_H>delta n的H数量由packing有固定上界
C_r delta^(-d)；不能把每项o(1)乘最多n^d个H。
small表示s_H<=delta n，与H0无关。

## 4. 小t附加最高项，权重先相消

S14 §2 small-H正计数上界实际没有使用maxH。a=(r+1)delta<1，
1<=k<=delta n时原cap外部J<=k-1、内部L=rk-J>=dk+1；
packing抽前d阶后n总幂只有rk，得到

    sum_small Q0(k)
       <=C n^(rk) a^(d(k-1)+1) 3^(rk)/(rk)!。

乘t^(rk)求和至多C a^(1-d)exp(3a^(d/r)nt)。
选delta使3a^(d/r)<cos(pi/r)/4，除R_r^n指数消失。
k>delta n尾由固定a0完整W0支付exp(-n)，全部多项式H数亦吸收。
因此small附加K总和=o(R_r^n)，不是n^d exp(-cnt)粗界。

有限个大H全部s_H<=2n/r，有d色CDF变量

    xi_H=(s_H-d(n-1)/r)sqrt(t/(n-1)) <= -c_r sqrt(nt)->-infinity。

S13全r、全s的完整非中心移动尾给每项o(R_r^n)，固定数量允许求和。
这里使用全非中心尾，而不是只用一个固定有界xi窗口。

## 5. 大t与正紧t

small-H真实Euler系数非负，degree K<=s_H、K(1)<=r^(n-1)。
R_r~t^d；取delta<d/(2r)，全部small项总和满足

    sum_small |K|/R_r^n<=n^d(C t^(r delta-d))^n ->0。

大H数量仍固定，其xi_H趋负无穷，S13完整非中心移动尾支付。
正紧t上同一固定正常累计间隙，由S12的固定径向内圆/谱界给
K_H/R_r^n<=C n^C exp(-c n)，可乘n^d数量。未把这个紧域界移到小t。

三类t子序列接合为(1)，与低Euler无maxH提取、准确最高T身份绑定。
前导有界Sigma profile因此接回真实全部M，实部可以0。
本页不支付Sigma发散相对M或两端根数。
