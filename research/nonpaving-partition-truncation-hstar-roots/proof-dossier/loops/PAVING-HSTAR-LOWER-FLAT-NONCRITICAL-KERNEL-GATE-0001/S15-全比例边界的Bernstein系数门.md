# 全比例边界：Bernstein 系数门

2026-10-06，S14全比例共同远区独审PASS后，有限核区域的异质解析入口。
本页仍L3探索，核心离散不等式未证；不得登记全域稳定。

## 1. 与全稳定有关的准确正性接口

在边界w=x(1+i)，写

    A_k(p)=(-1)^k sum_{m=0}^{2k} (-1)^m binom(4k,2m)*b_m(p)。

准确指数母函数乘法给

    Re[g_p(w)*conj(cosh w)]
      =1+sum_{k>=1} A_k(p)*(4^k*x^(4k))/(4k)!。        (P)

级数绝对收敛，b_m<=1支付乘积换序。若全部A_k>=0，则边界实部>=1，
cosh无扇区零，Re(g/C)>0。S14支付共同大圆上的正性，
对t=w²右半盘使用调和最小值原理即可支付整个扇区正性。
之后G/F、相位、全部固定alpha紧K真实接合与此前相同。
这是充分门，不宣称系数正性为全稳定必要条件。

## 2. 单变量 Bernstein 阻碍的准确降维

令h_i=1-2p_i>=0、sumh=1，N=4k。定义

    C_k(p)=(-1)^k sum_{m=1}^{2k} (-1)^m binom(N,2m)
                    sum_{j=m+1}^{2m} binom(2m,j)*p^j*(1-p)^(2m-j)。

互斥二项尾及完整cosh乘积准确给

    A_k(p)=2^(2k)-sum_i C_k(p_i)。

把C_k((1-h)/2)写成N次一元Bernstein形式

    C_k((1-h)/2)=sum_{l=0}^N U_k(l)*binom(N,l)*h^l*(1-h)^(N-l)。

若普通幂系数为d_j，准确转换为

    U_k(l)=sum_{j=0}^l d_j*binom(l,j)/binom(N,j)。

将上述表达齐次化于H=sumh，A_k三变量的alpha单项式系数
（sumalpha=N）除以多项式系数binom(N;alpha)，准确为

    2^(2k)-U_k(alpha1)-U_k(alpha2)-U_k(alpha3)。       (B)

所以一个与复杂零点等式不同的可检验桥梁是

    U_k(l)<=(1-l/N)*U_k(0)，forall k>=1,0<=l<=N。   (L)

若(L)成立，(B)>=2^(2k)-2U_k(0)=B_k，其中

    B_k=(-1)^k sum_m (-1)^m binom(4k,2m)*binom(2m,m)/4^m。

本桥梁不是把原全稳定换记号：它是更强的单变量离散系数上界，
若失败只关闭这一充分路线，不能关闭原目标。

## 3. B_k 正性：可独立证明的经典 Legendre 连接

标准Legendre展开（亦可直接比二项式系数）给

    B_k=(-1)^k*2^(2k)*P_(4k)(1/sqrt2)。

下面支付它的符号，而不把有限k检查当全k证明。
设N=4k、lambda=N+1/2，v(theta)=sqrt(sin theta)*P_N(cos theta)。
Legendre方程准确变为

    v''+[lambda²+1/(4 sin²theta)]v=0。

用连续Prüfer相位tan(phi)=lambda*v/v'、phi(0)=0（v~sqrt theta），
其导数为

    phi'=lambda+sin²phi/[4lambda sin²theta]，
    delta=phi-lambda*theta 因而不减。

P_N恰有N个简单(-1,1)零（标准正交多项式零点定理），N偶，
theta∈(0,pi/2)恰有N/2个零；且v'(pi/2)=0。
因此phi(pi/2)=N*pi/2+pi/2，delta(pi/2)=pi/4。
在theta=pi/4，

    k*pi+pi/8 <=phi(pi/4)<=k*pi+3pi/8。

故P_(4k)(1/sqrt2)符号为(-1)^k，严格非零，B_k>0。
此经典连接不主张新Legendre定理；原始方程与零点输入应在成稿时引用。

## 4. 当前核心缺口与已失败快捷路径

(L)尚未证明。有限有理校准k<=8支持(B)的最小值在(0,0,N)顶点，
三变量展开k<=4全部系数正；只作反证/校准，不支付全k。
规模不到一千个有理系数、串行内存校验，没有扩大实际n或Jensen表。

不能直接用C_k(p)全区间凸性：k=2的

    C_2'(p)=-56p*(5p^6-15p^5+45p^4-65p^3+45p²-15p+1)，
    C_2''(0)=-56<0。

所以凸性快捷前提有严格反例；不否定(L)或条件三块和的上界。
唯一下一步：从准确二项尾/ Bernstein 公式推导U_k(l)的统一界或
找到(L)的严格反例，不继续扩有限k表来宣称正性。
内部HOLD，连续普通研究；全非临界目标仍未完成。
