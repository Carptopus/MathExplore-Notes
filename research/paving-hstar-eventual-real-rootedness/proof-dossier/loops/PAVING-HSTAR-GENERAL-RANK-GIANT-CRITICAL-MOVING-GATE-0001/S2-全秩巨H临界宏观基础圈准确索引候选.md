# 全秩巨H临界宏观核：基础圈准确索引

2026-10-06，固定r>=5,d=r-1，phi=pi/r，固定0<p_min<1/r。
比例p∈[p_min,1/r]；alpha0=1-p，其他alpha_i<=p、sum alpha_i<=p，允许可数谱。
F_full=F_p-sum G_alpha，定义同前导ENDPOINT S3；实tau同伦也允许。
候选某共同J0后全部整数J>=J0，圆

    |z|<R_(p,J)=[J pi/(c_p sin(phi))]^r，
    c_p=r[p(1-p)^d/d^d]^(1/r)

内准确J个简单负根，圆周无零、负端号(-1)^J。包括p=1/r。
实际n传递必须先固定J；本页不宣称增长圈或实际全轴。

## 1. 一般B_r及Euler导数的完整负射线包络

前导ENDPOINT S2稍扩扇区给A=(Y^(1/d)/d)^(d/r)，

    M(A)=sqrt[d/(2pi r A)] exp(-i phi/2)exp[rA exp(i phi)]。

负射线根过滤两主支准确共轭，另外d-2支主角至少2pi/d。
主支插入w xi^(-1/d)的同一Hankel积分，鞍点值d A exp(i phi)，
完整稍扩扇区Gaussian给相对O(A^-1/2)，所以

    B_r(-Y)=(2/d)Re[M(A)(1+O(A^-1/2))]+O(exp[(c_r-epsilon)A])，
    theta B_r(-Y)=(2/d)Re[A exp(i phi)M(A)(1+O(A^-1/2))]
                                      +O(exp[(c_r-epsilon)A])。

这里c_r=r cos(phi)，epsilon>0固定依r，不除以实部。
其他支导数不能从角模单调直接继承；完整支付如下。
取theta_c=pi/d+epsilon_d/2，离其余支角有正距离。
在其他支w周围取相对半径eta|w|的Cauchy盘，eta充分小，
全盘角模至少theta_c，半径最多(1+eta)|w|。
LP角模单调及稍扩扇区包络给其模至多
C exp[r(1+eta)^(d/r)cos(d theta_c/r) A]，选eta使该指数<c_r。
w导数的Cauchy半径正比|w|不增加独立大幂，故所有余支导数共同指数小。
有界Y通过紧性扩常数；theta B_r(0)=0使原端积分可积。

## 2. 准确Beta积分与统一端点/合并层

令L=R^(1/r)，v为积分变量，f(v)=v(1-v)^d、
H(v)=r[f(v)/d^d]^(1/r)，v0=1/r。
准确F_p(-L^r)=1+integral_0^p theta B_r(-L^r f(v))dv/v。
H(v0)=1，H'/H=(1-rv)/(r v(1-v))，
H''/H=-d/[r² v²(1-v)²]<0。
下部v<=p_min/2指数比主端H(p)有固定差；其起点用theta B(0)=0，
整函数包络支付。上部完整复主被积项为

    [2 sqrt(L H(v))/(r sqrt(2pi d) v)]
                      exp(i phi/2)exp[L H(v)exp(i phi)]。 (1)

误差共同相对复包络O(L^-1/2)，余支指数小。
记a=1-rp，c_p=H(p)。

### 2a. a sqrt(L)趋无穷

H'(p)共同与a可比。用y=L H'(p)(p-v)，凹性给Re指数衰减至少cy。
Taylor误差O(y²/(L a²))、振幅变化O(y/(L a))，共同积分为

    F_p(-L^r)=(2/d) w(f(p))Re[M(L c_p/r)(1+o(1))]，
    w(f(p))=(1-p)/(1-rp)。                              (2)

相对误差O(L^-1/2+(L a²)^-1)针对复包络。
基础网格L c_p sin(phi)=J pi，(2)相位J pi-phi/2，号(-1)^J。

### 2b. a sqrt(L)有界

u=sqrt(L)(v-v0)，H(v)=1-r²(v-v0)²/(2d)+O(|v-v0|³)。
负二阶与凹性给共同Gaussian支配；(1)在v0的准确前因子
2 sqrt(L)/sqrt(2pi d) exp(i phi/2)。截断u<=-a sqrt(L)/r给

    F_p(-L^r)=(1/r)Re[exp(L exp(i phi))erfc(z)]
                                    +o(exp[L cos(phi)])，
    z=a sqrt(L/(2d))exp(i phi/2)。                      (3)

c_p=1-a²/(2d)+O(a³)，L a³趋0，且z²=L a² exp(i phi)/(2d)，
所以(3)准确改写为

    (1/r)exp[L c_p cos(phi)]
          Re[exp(i L c_p sin(phi))E(z)]+o(exp[L c_p cos(phi)])。

E=exp(z²)erfc(z)的锥由本门S1 §3准确积分给Re E>0、
每固定有界z窗正常数下界；a0时E1。基础网格同样号(-1)^J。
任意J趋无穷的符号失败序列可抽2a或2b，均矛盾；得共同J0。

## 3. 准确J计数，不只符号下界

先取一个固定p_c∈[p_min,1/r)作为同伦起点。
该基础圈的B变量Y_base=f(p_c)R_(p_c,J)满足

    A_base=J pi/[r sin(phi)]，Psi(Y_base^(1/d))=J pi-phi/2+o(1)。

前导ENDPOINT S2准确J圈的Psi=J pi；Psi严格增。
两个圈之间的整段主相位处于J pi-phi/2+o(1)至J pi，
主实部有共同正相对下界；§1余支指数小，前导S3积分校正相对O(1/A)。
所以该段归一F_(p_c)负轴无零，基础圈与准确J圈根数相同。
F_p所有p（包括1/r）LP+、简单性来自完整宏观核及严格化。
R_(p,J)随p连续，§2排除负轴边界根、LP排除其他边界根，
从p_c到1/r同伦准确J根保持。

## 4. 实tau/全部附加谱的临界端点

前导S3权重H_tau=h(y)-tau f_low(t)N(t)，
f_low=t/(d-rt)。p=1/r时单巨H支持延至最大点，终端h(y)发散，
但只是可积逆平方根奇性；所有其他alpha_i<=1/r<d/r，校正在终端前已消失。
初值1、正权重、内部向上跳、负变差

    V_-<=sum_i f_low(alpha_i)<=p/(d-rp)<=1/[r(d-1)]<1/2。

有限/可数BV与积分交换同前导全谱证明。
无界终端取min(H_tau,M)，M>=1，不增加负变差、初值1、终端M；
签名余弦全平面Rouche及可积L1/Hurwitz给C_tau LP+，
全d gamma乘子及正确严格化给F_(p,tau)无限简单负根。
不能从LP凸组合推出，实tau完整门在此重新支付。

Markov指数相对c_p为

    xi_p/c_p=[p/(1-p)]^((d-1)/r)<=d^(-(d-1)/r)<1/2<cos(phi)。

全部其他谱之和<=C p exp(xi_p L)，所以对§2两层主包络共同指数小。
主包络2a至少常数exp(L c_p cos(phi))/sqrt(L)，
2b在每个固定有界窗有正常数因子；任何共同符号失败序列同样抽两层排除。
因此实tau边界仍号(-1)^J，LP/可数复紧域连续性保持准确J根。

## 5. 真实临界原端接口

沿实际q/n趋1/r，先固定足够大J，TWO-MACRO S5抽全部比例谱及真实复紧域，
在x_L=-R_(p_n,J)/n^r圈内最终准确J简单负根，边界号(-1)^J。
R_(p_n,J)趋[J pi/sin(phi)]^r，p仍是实际q/n，不改成1/r提前计算。
归一驻点式给nW趋R_(1/r,J)^(1/r)exp(i phi)，
a0趋0使-q log v趋0，因此基础U_n(t_L)趋J pi，nh_L与J同阶。
尚未付临界倒端有限角相消及degree整体接合，不因此宣称实际全轴。
新颖性UNKNOWN、内部HOLD。
