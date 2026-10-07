# 分离附加真实cap：全秩两端及K端层

2026-10-06。固定r>=5，d=r-1。未独审，内部HOLD。
本页支付完整实际坏cap delta_v，不以无坐标上界最高K代替它。
依赖S11准确容斥及本门S1定义；旧秩四S24、S43R1、S44、S45只作推导入口，
下文逐项重新给出一般r的量词与预算。

## 1. 范围和保留的未证区域

连通rank-r paving，最大H0=n-q，p=q/n<1/r。
q、n-rq、nh、n/h、Sigma全部发散；N=nh。
附加H大小v<=q+r-2=q+d-1，完整真多项式满足

    h*_M=P_single-sum_(H!=H0)delta_v。

候选结论 sum |delta_v(-tau)|=o(M)，M=R^n rho^(-q)|H_amplitude|，
只覆盖：h趋0；h趋无穷；h固定正紧且K趋0或无穷。
联合正紧h与正紧K仍未支付，不靠有限点检验或紧性补出该界。

## 2. 一般r的准确次数和高度

对指定v点cap的真实坏计数，外部a0=n-v-1，内部完整坐标上界容斥：

    D_v(k)=sum_(z=0..k-1) binom(z+a0,a0)
      sum_(i=0..d)(-1)^i binom(v,i)
                   binom((r-i)k+v-1-i-z,v-1)。

对内部多项式作Newton展开及外部hockey-stick，准确

    D_v(k)=sum_(j=0..v-1)(-1)^j binom(a0+j,j)
       binom(k+a0,a0+j+1)
       sum_(i=0..d)(-1)^i binom(v,i)
                 binom((r-i)k+v-1-i-j,v-1-j)。

因此次数<=n-1且k=0,-1,...,-a0为零；Euler三角反转给
deg delta_v<=v、delta_v(0)=0，所有合法n,v均成立。
固定v时k<=v的外部数O_v(n^(k-1))，内部有限常数，故
|[x^j]delta_v|<=C_(r,v)n^(j-1)，1<=j<=v。

指定单H截断多面体的h*与uniform的h*各自系数非负；
截断体积不超过hypersimplex体积，后者Eulerian数<=r^(n-1)。
delta作为差不必系数非负，但准确l1高度<=2r^(n-1)。

## 3. 小h：先支付有限小cap

数量<=binom(n,d)-binom(n-q,d)<=C q n^(d-1)。
r<=v<=2r-4只有固定有限种v，用第2节固定v系数界和tau<=C h^d，

    sum_small |delta_v| <= C q n^(d-1) sum_(j=1..2r-4)n^(j-1)tau^j。

令N=nh，则每项除去N^(dj)后的剩余幂为
(q/n)n^(-(d-1)(j-1))<=1。小h有R>=1+c_r h，
故除R^n得到N固定多项式exp(-c_r N)。
准确方差Sigma²=K² N(1-p)(dK+r cos theta)/(rh+dK)²，
K<=1时Sigma<=C sqrt(N)，K>=1时Sigma<=CK sqrt(q)<=CN。
再乘Sigma rho^q<=C(1+N)，完整相对预算趋零。
没有把这批cap藏进外部packing的零权重。

## 4. 小h：其余cap保留外部坐标的d阶packing

v>=2r-3时每个H至少有v-r+2个外部点，任意外部d元组至多属一个H。
因此sum v^d<=C_r q^d。对真实坏计数去掉坐标上界，内部L=rk-J，
外部J<=k-1，所以L-dJ>=r。选择eta,zeta属于(0,1)，
eta^d zeta=tau、eta>=tau^(1/r)，从而eta^L zeta^J>=tau^k。
保留内部至少d个点的Taylor余项并先求packing，eta>zeta时

    sum_(v>=2r-3) sum_k D_v(k)tau^k
      <=C(q eta)^d(1-eta)^(-d)
        (1-eta)^(-(q+d-1))(1-zeta)^(-(n-q-d+1))。       (1)

这里保留真实外部n-v，没有额外n^d数量前因子。
真实Euler绝对值乘A^n；除R^n相当于再乘D^n，D=|1-W|。
小h共同log D<=-c0 h，c0>0固定。

- K>=1：取充分小固定eta=epsilon，zeta=tau/epsilon^d。
  q<=N/d、n tau/N<=C h^(d-1)，指数损失<=c0 N/2；
  (q eta)^d<=C N^d、Sigma<=CN，rho^q<=1。
- K<1且p<delta：eta=(tau/p)^(1/r)、zeta=p eta。
  准确t/h=[(1-p)/(dpL)]^(1/r)，其中L=1/rho>=1。
  q eta/N<=C p^((r-2)/r)，eta<=C h^((r-2)/r)趋0。
  先取delta充分小，(1)指数<=c0 N/2+o(1)；前因子<=C N^d。
- p>=delta：K=O_delta(h)，theta趋pi/r、L趋1。
  取eta=t[d(1-p)/p]^(1/r)，zeta=p eta/[d(1-p)]。
  两者O_delta(h)，eta>zeta、eta>t。完整指数除N为

      (r/d)p^((r-2)/r)(1-p)^(2/r)+O_delta(h)
        <=d^(-(r-2)/r)+O_delta(h)。

  在p<=1/r时最大值在1/r；r>=4给
  d^(-(r-2)/r)<=1/sqrt(3)<cos(pi/r)。
  而log D=-h cos(pi/r)+O_delta(h²)，所以有共同严格衰减exp(-c_delta N)。
  packing前因子(q eta)^d<=C_delta N^d，Sigma<=C sqrt(N)。

三类都直接支付任意缓慢N发散；没有用Sigma发散推出n与N的错误幂关系。
结合第3节得到全部附加cap的小h相对结论。

## 5. 大h：统一高度与次数

tau=h^d(h+K)/L，共同c h^d<=tau<=C h^r；D可比h、R>=c tau/h。
n/h发散使h<=n，K<=Cnh/q<=Cn²，准确Sigma<=Cn²。
第2节l1与次数界、#H<=Cn^d、v<=q+d-1，给相对预算

    C n^(d+2+r(d-1)) [C h tau^(p-1)]^n
       <=C n^(d+2+r(d-1)) [C h^(-(d²/r-1))]^n ->0。

因d²/r-1=r-3+1/r>0，h任意慢速趋无穷亦压制固定n幂。
不需要rho^q额外支付，也不要求delta系数非负。

## 6. 正紧h的K两端

K趋0：p趋1/r、t/h趋1。附加v<=q+d-1与最高d色均值d(n-1)/r
留固定间隙。旧S12紧域Cauchy加全部低Euler有限band的绝对谱界给
sum |delta_v|<=C n^(2r)exp(-cn)R_r(t)^n。
R_r/R趋1，不把其n次幂误写为1；Sigma<=C sqrt(n)、rho^q<=1，
因此exp[-cn+n o(1)]支付共同相对预算。

K趋无穷：p趋0，v<=q+d-1=o(n)。第2节准确次数与Euler卷积，
D_v(k)<=binom(n+rv-1,rv)、k<=v，给

    log sum_j |[x^j]delta_v|<=C_r v log(en/v)+C_r log n=o(n)，

共同于r<=v<=q+d-1。紧h使tau有上下界，乘max(1,tau^v)并求H和仍exp(o(n))。
R趋(1+h^d)/|1-h exp(i pi/d)|>1，紧h给共同R>=1+c。
严格大于1可直接比较平方：h<=1时2h cos(pi/d)-h²>0；
h>=1时2h^d-h²>0。Sigma<=CK sqrt(q)<=Cn，故相对预算趋零。

## 7. 唯一未付接口

任一未消失附加cap的失败子序列只能进一步落在h与K的联合正紧域。
下一步须证明d标记内容矩阵的复圆共同谱预算或独立的同量纲界，
不是把正实标记或有限点检查当整个复圆证明。
本页若通过仍只是全actual门的一部分，根数与新颖性不在范围内。

