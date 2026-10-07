# 全秩宏观巨H：准确原端圆索引

2026-10-06。固定r>=5，d=r-1；S1根性与S2大相位圆为冻结依赖。
这是极限核/固定圆的索引，不是actual全轴，不支付增长圆或倒端。
本页一般化rank4 S53 §§1—3，重新支付全d幂次、全部可数附加H和实权LP门。

## 1. 冻结范围及准确积分

固定p_max<1/r；0<p<=p_max，P=p(1-p)^d。定义

    F_p(z)=sum_(k>=0) Pr[Bin(rk,p)>=k] z^k/(rk)!，
    G_alpha(z)=sum_(k>=1) Pr[Bin(rk,alpha)>=dk+1] z^k/(rk)!。

其他宏观H比例alpha_i>0为有限或可数列，alpha_i<=p，sum alpha_i<=p。
定义F_(p,tau)=F_p-tau sum_i G_alpha_i，0<=tau<=1；空列允许。
候选：全部F_(p,tau)属LP+，无限简单严格负根；
对S2全部充分大j，归一F_(p,tau)(z/P)在|z|<Y_j=T_j^d内准确j根，
圈周无零，负端值符号(-1)^j。j阈值共同于p<=p_max、tau及全部合法比例列。
p0的归一延伸定义为B_r。

二项尾准确为I_p(k,dk+1)，故k>=1时逐系数给

    F_p(z)=1+integral_0^p theta B_r(z t(1-t)^d)dt/t。

令v=t(1-t)^d，v'=(1-t)^(d-1)(1-rt)>0，
w(v)=(1-t(v))/(1-rt(v))，w(0)=1，得准确分部积分

    F_p(z/P)=w(P) B_r(z)-integral_0^1 W_p'(h)B_r(zh)dh， (1)
    W_p(h)=w(Ph)。

交换由整函数在有限区间一致收敛支付。
在p<=p_max<1/r，w>=1、w(P)及W_p'共同有界，W_p'非负；
p0时W_0=1。于是(1)给归一族到B_r的复紧域连续性。

## 2. B_r负射线的共同包络与单巨H圆索引

S2 LP角模单调、稍扩扇区与准确根过滤给全部T>=0，A=(T/d)^(d/r)：

    |B_r(-T^d)|<=C_r(1+A)^(-1/2)exp[c_r A]，
    c_r=r cos(pi/r)。                                      (2)

因为根过滤各支的主角绝对值至少pi/d，单支模均不超过该主射线模。
在S2 Psi(T_j)=j pi的准确相位点，主对同号、余支共同指数小，故

    (-1)^j B_r(-Y_j)>=c A_j^(-1/2)exp[c_r A_j]。             (3)

积分(1)中h<=1/2给固定指数缺口；h>=1/2用
1-h^(1/r)>=(1-h)/r，得到积分绝对值
<=C A_j^(-3/2)exp[c_r A_j]。
与(3)比为O(1/A_j)，共同于p<=p_max，包括p0。
所以全部足够大固定j，F_p(-Y_j/P)符号(-1)^j。

单巨H F_p=F_(alpha=1-p,r)由SINGLE-MACRO S9及R4完整依赖属LP+且简单。
归一族p0=B_r，p连续到p_max；只有负轴可能与相位圆相交，
负端符号排除该点。零点数在整个p同伦不变，故准确j，不只至少j。

## 3. 实权附加谱：LP必须单独证明

tau实数不能由两端LP凸组合推出LP。这里重新用TWO-MACRO S2/S3的准确
折叠及签名BV证明。令低支t、高支y满足

    t^d(1-t)=y^d(1-y)，0<t<d/r<y<1，
    h(y)=y/(ry-d)，f(t)=t/(d-rt)。

单巨H alpha0=1-p>d/r的支撑终点高支为y=alpha0，
对应低支t_a>p（(1-p)^d p>p^d(1-p)，且低支严格增）。
该支撑内单巨H折叠权重h(y)从1严格增加到有限正终端。
全部其他alpha_i<=p<t_a，不切去高支。完整实权是

    H_tau(s)=h(y)-tau f(t)N(t)，N(t)=#{i:alpha_i>t}。       (4)

可数时tN(t)->0，故H_tau(0)=1。跨每个alpha_i向上跳tau f(alpha_i)。
非跳点负变差不超过tau integral N(t) f'(t)dt，Tonelli给

    V_- <=tau sum_i f(alpha_i)
        <=p/(d-rp)<=p_max/(d-rp_max)<1/[r(d-1)]<1/2。       (5)

另有f(t)N(t)<=sum_i alpha_i/(d-rp)<=p/(d-rp)，
H_tau>=1-p/(d-rp)>0。终端N=0，值A=h(alpha0)>1；
可数跳跃总质量有限，且支撑外截断不是内部下降。

F_(p,tau)系数为F_p与F_(p,1)的凸组合，仅用来给正系数（不是证明LP）。
F_(p,1)的多类抽样尾互斥且存在k次外部、dk次H0命中事件，全部k系数严格正。
校正求和由sum alpha_i<=p及二项尾最低alpha^(dk+1)幂紧域绝对收敛支付。
令C_tau系数为F_(p,tau)系数除gamma_k=(2k)!/[(dk)!k!]，
则C_tau(0)=1、正系数、阶<=1/2。
准确折叠为C_tau(-x²)=1-x integral_0^S H_tau(s)sin(xs)ds。
分部积分为A cos(Sx)-integral cos(sx)dH_tau，
||dH_tau||=A-1+2V_-<A。TWO-MACRO S2 §5的竖/横线矩形Rouche
完整全平面优势给全部零点实；本页H终端有限，不需无界截顶。
C_tau由Hadamard属LP+；SINGLE-MACRO S9 §§3—4精确全d gamma乘子
和保留1/k!的R4严格化给F_(p,tau)无限简单负根。
本页引用的是上述明确工具义务，不继承整数谱审计标签到实tau。

## 4. 附加谱全部尾和在准确圆共同指数小

0<alpha<=p<1/r，令gamma=d(1-alpha)/alpha>1。
Markov准确给

    Pr[Bin(rk,alpha)>=dk+1]
        <=gamma^(-1)[r^r alpha^d(1-alpha)/d^d]^k。

xi_alpha=r alpha^(d/r)(1-alpha)^(1/r)/d^(d/r)随alpha<d/r增加，
gamma^(-1)<=C_r alpha，故

    |G_alpha(z)|<=C_r alpha exp(xi_alpha |z|^(1/r))。

归一z=-Y/P并对全部i求和，得到

    sum_i |G_alpha_i(-Y/P)|
      <=C_r p exp{[r/d^(d/r)] [p/(1-p)]^((d-1)/r) Y^(1/r)}。 (6)

主包络(3)指数为[r/d^(d/r)]cos(pi/r)Y^(1/r)。
即使p上取1/r，校正指数比项<=d^(-(d-1)/(d+1))<1/2<cos(pi/r)：
d>=4、(d-1)/(d+1)>=3/5，4^(-3/5)<1/2。
于是(6)共同指数小于(3)，全部tau和可数比例列均保留负端符号(-1)^j。
固定p时tau同伦由§3 LP排除其他圈周零点、符号排除负端零点，
准确j根完整传递；所有充分大j阈值只依固定r,p_max。

## 5. 真实对象传递及未证连接

对q/n趋固定p0 in(0,1/r)，抽全部附加H宏观比例序列；
packing和交集<=d-1给alpha_i<=p0、sum alpha_i<=p0。
TWO-MACRO S5真实复紧域给h*_M(z/n^r)->F_(p0,1)(z)。
令P_n=(q/n)(1-q/n)^d，固定足够大j的圈

    |x|=Y_j/(P_n n^r)

准确j简单负根并负端符号(-1)^j最终传到真实M。
共同性用任意坏序列抽比例谱子列及上述全谱共同圈门；不让j随n增长。
p0=0须用S1的Z=n^d q，P_n n^r/Z=(1-q/n)^d->1，同样固定圈传递。

原端与移动中带连续相位仍须另核，尤其常数-pi/(2r)及索引偏移。
倒端准确圈、degree和有界q仍未由本页证明；不得凭端盘+中带宣布全轴。
新颖性UNKNOWN，全部内部HOLD。
