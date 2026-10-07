# 小索引的有符号 erf 过渡

2026-10-06，主线程解析候选，尚未独审。
沿S15/S17准确U定义，不改变全非临界目标。本页拟支付任何固定K的
全部1<=l<=K sqrt N、充分大N；N0(K)非显式，不声称全l。

## 1. 首端差额的准确身份

记K(z)=1+i(z+z^-1)/2、L(z)=1+i/z、T=2^(N/2)，N=4k。
S17 U身份及L-K=-(i/2)(z-z^-1)给

    U_(s+1)-U_s=(-1)^k/2 * Im [z^1] K(z)^(N-1-s)L(z)^s。   (J)

证明：F_(s+1)-F_s=-(i/2)(z-z^-1)K^(N-1-s)L^s。
除以z(z-1)后抽留数为-(i/2)([z^1]+[z^0])；
常数系数实数，实部只剩(J)。每个N固定的s范围0<=s<=N-1。
不能假设每个增量负，后文主项本身可振荡。

## 2. 双鞍点：保持相位，不以模代符号

取任意固定K0>0，0<=s<=K0 sqrt N，kappa=s/sqrt N。
准确Fourier系数

    a_(N,s)=(1/(2pi)) integral_-pi^pi
        [1+i cos theta]^(N-1-s)[1+i exp(-i theta)]^s exp(-i theta) dtheta。

两鞍点为theta=0,pi。0附近的复对数（取连续局部分支）：

    log((1+i cos theta)/(1+i))=-(1+i)theta²/4+O(theta^4)，
    log((1+i exp(-i theta))/(1+i))=(1-i)theta/2-theta²/4+O(theta³)。

令y=sqrt N theta，提取(1+i)^(N-1)，局部指数为

    -(1+i)y²/4+(1-i)kappa*y/2+error。

0鞍点准确Gaussian主积分为

    I_(N,s)=(-1)^k*T/[(1+i)^(3/2)sqrt(pi N)]
                           *exp[-(1+i)kappa²/4]。

这是复Gaussian积分，线性项平方给-(1+i)kappa²/4；
不得把相位丢掉变成普通概率尾。
pi鞍点在变量theta=pi-v下恰为0鞍点的负共轭，
因为exp(-i theta)=-exp(i v)。所以

    a_(N,s)=I_(N,s)-conj(I_(N,s))+O_K0(T/N)。

只保留一个鞍点会漏因子2，不能用单峰近似。

### 共同误差与全部小s

固定足够小角delta，两个邻域外
|1+i cos theta|<=sqrt2*(1-c_delta)，而第二因子至多2，
s<=K0 sqrt N只贡献exp(O_K0(sqrt N))，外段共同指数小。
邻域内绝对值用exp(-c y²+C_K0|y|)支配：
K对数余项N theta^4=O(y^4/N)，L余项及二者二次差
为O_K0(y²/sqrt N+|y|³/N)，exp(-i theta)误差O(|y|/sqrt N)。
先取小delta再取N充分大，可把高次余项吸收入高斯；
用|exp(u)-1|<=|u|exp(|u|)积分，局部归一误差O_K0(1/sqrt N)，
加外段后得到上述O_K0(T/N)。这是统一绝对误差，
包括s=0、固定s、s/sqrt N趋0以及区间内任意移动速度。

## 3. 累积相消的正向预算

由(J)，精确相位给

    (U_s-U_(s+1))/T
      =exp(-kappa²/4) sin(3pi/8+kappa²/4)
         /[2^(3/4)sqrt(pi N)] +O_K0(1/N)。

累加s=0,...,l-1，Riemann和误差也为O_K0(l/N)，
因为归一主项在固定kappa区间导数有界。因此

    |(U0-U_l)/T - (1/2)Re erf(q*l/sqrt N)| <= C_K0*l/N，
    q=2^(-3/4)exp(-i*pi/8)，0<=l<=K0 sqrt N。    (E)

积分身份由exp[-(1-i)u²/4]的原函数直接验证：
相位e^(i3pi/8)/sqrt(1-i)=2^(-1/4)i，故留下Re erf而非Im。

S3已独审的erf正实引理在|arg q|<=pi/8给Re erf(q*x)>0对x>0。
紧区间[0,K0]上Re erf(q*x)/x连续延拓且严格正；
令其最小值m_K0>0，原点值2Re(q)/sqrt pi>0。
由(E)，N充分大时

    (U0-U_l)/T >=(m_K0/4)*l/sqrt N > l/(2N)。

U0<T/2，因此U0-U_l>(l/N)U0，支付全部该区间(L)。
充分门可选sqrt N>=4C_K0/m_K0且sqrt N>2/m_K0，
同时N需满足局部误差估计和K0 sqrt N<=N-1。N0依赖K0，非显式。

## 4. 没有被支付的范围

(E)只对固定K0的共同N0(K0)，不允许把K0换成sqrt(log N)
而保持常数不变。S18需kappa约sqrt(log N)才消除Cauchy前因子，
两者之间仍有增长的过渡区；有限N<N0(K0)也未由本页封闭。
下一义务：给(J)中央系数共同积分尾预算，控制s>=K0 sqrt N的
有符号余量，从固定K0的erf差额接到S18，而不逐l扩表。
CONTINUE，全部内部HOLD；整个全l充分门及实际全比例目标仍未证明。
