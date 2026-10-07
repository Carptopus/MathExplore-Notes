# 一般秩大端：有界K的完整分离积分候选

2026-10-06，未独审。固定r>=5、d=r-1以及任意有限K0>0。
准确有限J、中央项采用前导S2+R1，一般全圆几何采用S1+R1。
本页不覆盖K无界的大端，不等于整个移动核心或actual h*。

## 1. 冻结域与结论

任意合法序列h=|W|->infinity、0<K<=K0，满足q、n-rq、n/h、Sigma
均趋无穷；nh自动发散。记Jscale=n/h，Sigma=K sqrt(n Re V)。
候选完整T为两中央峰实部加o(M)，主项H、M沿前导准确中央式。
在此域p与1/r共同可比，q与n共同可比，n Re V与Jscale共同可比，
Sigma与K sqrt(Jscale)共同可比，|H|与1/Sigma共同可比。

## 2. 大端极限势函数不是仅有限h非负性的极限

写w=u exp(i psi)，完整w圆|1-w|=D、D²=h²+1-2hC，
u=cos psi+sqrt(D²-sin²psi)，psi∈[0,pi]，C=cos theta。
theta由K=-sin(rtheta)/sin(dtheta)确定，L=|1+K exp(i theta)|。
K在[0,K0]紧化，不先把K当正正常数。

共同C3展开给

    u=h+cos psi-C+O_r(h^(-1))，
    |v|²/rho²-1 = (2/h) P_K(psi)+O_(r,K0)(h^(-2))，
    P_K(psi)=K+rC-d cos psi+L cos(d psi)。           (1)

注意P_K(theta)=0，因为L cos(dtheta)=-K-C。
P_K的唯一最低值为0，直接证明如下：

    P_K'=d[sin psi-L sin(dpsi)]。

psi<pi/r时sin(dpsi)>=sin psi，故下降；
在(pi/r,pi/d)中sin psi/sin(dpsi)严格增1至无穷，
唯一临界为theta，随后直到pi/d严格上升。
psi>=pi/d时

    P_K(psi)>=K+rC-d cos(pi/d)-L=P_K(pi/d)>0。

K=0时theta=pi/r，仍严格唯一；theta<pi/d对所有有限K0保持正距。
准确P_K''(theta)=dC-d²L cos(dtheta)>c_(r,K0)>0。
由紧化，P_K>=c_(r,K0)(psi-theta)²。

不能把(1)的绝对O(h^-2)直接吸收进峰点二次量。令真实归一化
Q_hK=(h/2)(|v|²/rho²-1)，它和P_K连同前三阶psi导数共同收敛。
真实Q_hK(theta)=Q_hK'(theta)=0；二阶系数由前导准确方差共同趋
P_K''(theta)>0。共同Taylor在峰邻域给二次下界，峰外用严格紧性。
lambda角phi与psi满足共同导数绝对值1+O(h^-1)，领先phi_*对应theta。
故存在共同c>0，整个lambda圆

    D_rel>=c Delta²/h， E=q log(|v|/rho)>=c Jscale Delta²。  (2)

共轭给另一峰；这里不是套任意K无界时的错误二峰势函数。

## 3. hK大时整圆可拆B，hK有界时仅近峰拆B

准确J=B v^(-q)-1/(1-v)，或用无假pole有限和。
tau=h^d(h+K)/L、t=tau^(1/r)。h大且K<=K0时t与h共同可比，
uniform根间距与h共同可比；w圆上的|w|亦与h共同可比。

领先uniform根到圆距离与hK共同可比，近峰所有其他uniform根
因固定角距而至少c h。因此固定小领先角邻域内

    |B|<=C/K<=C|B(W)|， |1/(1-v)|<=C/K。             (3)

这对任意hK成立；B(W)与1/K共同可比。可由准确D-D_uniform在K0附近
一阶展开（主项h K cos(pi/r)/r）给领先距离，正紧K则距离ch。
邻域取只依赖r,K0的固定宽度，不包含次要uniform假pole。

另外存在固定M0，使hK>=M0时整个圆都可用(3)。由

    (t/h)^r=(1+K/h)/L， L-1>=c_(r,K0)K，

得h-t>=c hK；取M0足够大，使所有uniform根的|1-omega_j|
均比D小至少c hK。根分解给整圆B高度C/K。
否则hK<=M0时，不在次要pole附近拆分；保留完整J取消。

## 4. 中央以外的真实积分

近峰由(2)、(3)及|B(W)|/|H|与sqrt(Jscale)共同可比，
缓增L中央之外的Gaussian尾积分趋0。背景sqrt(Jscale)rho^q趋0，
因为rho^q<=exp(-c nK)，nK与Sigma*h*sqrt(Jscale)共同可比。
真实中央宽度与1/sqrt(Jscale)共同可比，Sigma发散支付pole分离。

若hK>=M0，(3)整圆成立，(2)在固定峰外给exp(-cJscale)，
同一Gaussian尾控制整个主项；背景同上，得到整个T的o(M)。

若hK<=M0，Sigma与K sqrt(Jscale)共同可比且发散，给
h<=C sqrt(Jscale)（最终），所以n=h Jscale<=C Jscale^(3/2)。
因此可以在固定峰外用准确有限J的粗高度，而非隐含q超过log n：
由于|w|与h共同可比、tau与h^r共同可比，w^d+tau由tau主导，
Y及Y/w共同有界；rho^q J被

    C exp(-(1-1/q)E)+C q[exp(-E)+rho^q]

控制。除|H|的因子至多C sqrt(Jscale)，q<=C Jscale^(3/2)。
峰外E>=c Jscale，主项预算是Jscale固定幂乘exp(-c Jscale)。
背景nK=Sigma*h*sqrt(Jscale)>=c sqrt(Jscale)最终，
故Jscale固定幂乘exp(-c nK)亦趋0。
近峰仍用(3)的尖锐Gaussian尾，不让有限和q高度强迫L超过Sigma。

所有分裂只在没有对应pole的区域使用。全圆J无uniform假pole，
也无w0（D>1且h大）。不需要把lambda=A的基线积分误当A^n；
本证明直接积分原准确J，没有添加或删除baseline。

## 5. 剩余入口

若独审通过，整个分离T已经覆盖小h、正紧h及大h有界K。
真正剩余是h,K共同趋无穷：其他d次角附近会出现多个接近的竞争峰，
不能从本页有界K势函数的严格紧性直接继承共同常数。
另有Sigma有界的累计过渡。下一步应保留这些峰的宽度与相对高度，
不靠增加固定rank或曲线表填补共同速度门。
