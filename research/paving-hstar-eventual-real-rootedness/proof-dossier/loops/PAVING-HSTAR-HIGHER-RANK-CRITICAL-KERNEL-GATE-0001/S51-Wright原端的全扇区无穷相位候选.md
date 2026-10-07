# Wright原端：全扇区无穷相位

2026-10-06，主线程冻结解析候选，待独立复核。
承接S50的Phi(w)=sum w^k/[k!Gamma(1+k/3)]。
本页仅证明该整个函数的相位尾，不宣称真实h*的全部根数已经闭合。

## 1. 主张与连续相位

写w=3A^(4/3)exp(i theta)，A>0、0<=theta<=pi/3。候选共同渐近为

    Phi(w)=sqrt(3/(8pi A)) exp(-3i theta/8)
             exp(4A exp(3i theta/4)) [1+O(A^(-1/2))]。       (1)

误差对整个闭扇区共同。Phi在该扇区无零，由S50的LP+及Phi(0)=1，
存在从0归一化的解析log。故在theta=pi/3射线，其连续辐角准确为

    Psi(T)=4(T/3)^(3/4)/sqrt(2)-pi/8+O(T^(-3/8))。          (2)

这里没有未定的2pi整数偏移；第5节显式支付它。

## 2. 精确Hankel表示

以负实轴为xi^(-1/3)的支割，H_A由下侧负轴从负无穷至-A、
半径A圆从arg=-pi到pi，以及上侧负轴从-A返回负无穷组成。
准确有

    Phi(w)=(1/(2pi i)) integral_(H_A)
                   exp(xi+w xi^(-1/3)) dxi/xi。              (3)

逐项展开exp(w xi^(-1/3))，Hankel倒Gamma式给1/Gamma(1+k/3)。
交换在圆上由一致收敛、在射线上由|xi|>=A且exp(-|xi|)/|xi|可积支付，
因为w固定且|w xi^(-1/3)|<=|w|A^(-1/3)。
因此(3)不是仅形式的积分；也不需要穿过原点本性奇点。

圆上令xi=Aexp(i phi)，圆积分恰为

    (1/(2pi)) integral_(-pi..pi) exp(A g_theta(phi)) dphi，
    g_theta(phi)=exp(i phi)+3exp(i theta-i phi/3)。           (4)

## 3. 共同唯一主峰与割线指数缺口

圆上的实部h=cos(phi)+3cos(theta-phi/3)。
驻点方程h'=0即sin(phi)=sin(theta-phi/3)，全部解为

    phi=3theta/4+3pi k/2，或phi=3pi/2-3theta/2+3pi k。

theta在[0,pi/3]时，(-pi,pi)中唯一解phi0=3theta/4；
第二族仅在theta=pi/3到达端点pi，第一族其余解不在圆弧内部。
h'在左端正、过phi0后负（theta=pi/3的右端导数为0但不反向）。
于是唯一全局最大值h(phi0)=4cos(3theta/4)。

完整复驻点也在phi0：

    g'(phi0)=0，g(phi0)=4exp(3i theta/4)，
    g''(phi0)=-(4/3)exp(3i theta/4)。                        (5)

Re(-g'')>=(4/3)/sqrt(2)。固定小epsilon>0后，
闭参数集的紧性给|phi-phi0|>=epsilon时共同严格指数缺口；
局部则有h(phi)<=h(phi0)-c(phi-phi0)^2，c>0共同。

上侧割线上xi=-x、x>=A，实指数

    -x+3A^(4/3)x^(-1/3)cos(theta-pi/3)

在x=A至多2A，导数<=-1。
下侧对应cos(theta+pi/3)在[-1/2,1/2]，
起点指数至多A/2；其导数<=-1/2（负cos时用x>=A）。
因此两条射线积分绝对值<=Cexp(2A)/A，
而主峰实部至少2sqrt(2)A，具有共同正指数缺口。
割线项不改变(1)的振幅或相位。

## 4. 圆的复Gaussian与误差

置v=sqrt(A)(phi-phi0)。Taylor余项在共同小邻域满足

    A[g(phi)-g(phi0)]=-(2/3)exp(3i theta/4)v²
                           +O(A^(-1/2)|v|³)。               (6)

缩小epsilon后，余项的实部不超过主二次衰减的一半。
用exp差的积分恒等式比较两指数，被积差共同受
C A^(-1/2)|v|³exp(-c v²)控制。
积分给局部Gaussian相对O(A^(-1/2))；截断Gaussian和其余圆弧由
第3节共同指数缺口支付。准确全实线Gaussian为

    integral exp(-(2/3)exp(3i theta/4)v²)dv
                =sqrt(3pi/2)exp(-3i theta/8)。               (7)

此平方根从theta=0的正实根连续延伸，Re二次系数始终正。
将(7)乘(4)的1/(2pi sqrt(A))，恰得到(1)。

## 5. 消除连续arg的整数债务

固定充分大A，定义整个扇区上的比值

    E_A(theta)=Phi(3A^(4/3)e^(i theta))
      /[sqrt(3/(8pi A))e^(-3i theta/8)e^(4A e^(3i theta/4))]。

由(1)，E_A在以1为中心的半径1/2圆盘内。可取该盘的单值log，
且theta=0时比值严格正，log实。
Phi的LP+乘积定义的log在正轴为实，所以沿theta连续时两log准确相等，
不存在2pi i整数跳变。取theta=pi/3虚部就得到(2)，
而沿射线从0定义的Psi与扇区log相同。

## 6. 本页边界与下一连接

S50若通过，则每固定j的相位圆准确根数已付；本页补相位的无穷尾常数。
要给实际原端和新中带相同整数标签，仍须在可选重叠序列上比较
S49的准确lambda/v/H振幅相位与(2)，保留共同误差和半周期偏移。
宏观原端以及倒端/有界Sigma计数仍不可由本页直接外推。
全部内部HOLD，无写稿、Git或公开交付。
