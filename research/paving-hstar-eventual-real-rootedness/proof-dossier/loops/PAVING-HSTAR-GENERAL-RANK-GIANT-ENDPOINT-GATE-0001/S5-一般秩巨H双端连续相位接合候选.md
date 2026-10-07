# 一般秩巨H：双端准确连续相位

2026-10-06。固定r>=5，d=r-1；p=q/n<=p_max<1/r，q趋无穷，
连通paving，最大H s=n-q。S1—S4固定端圈及实际中带为明确依赖。
本页只重构准确相位标签和尺度，不从两个局部式自动宣布全轴。

## 1. 准确n/q及角支

a0=1-rp>0（区别于整数端点a_n），W=h exp(i theta)，
theta∈(pi/r,pi/d)，领先驻点满足

    (1-p)W^r+a0 tau W+dp tau=0，tau=t^r，
    v_*=dp/(dp+a0 W)，lambda_*=(1+tau)/(1-W)，
    V=p(1-p)(a0+rp/W)，H=p(1-p)/(a0 W sqrt(2pi nV))。

这和GENERAL-RANK-GIANT-ACTUAL S7的同一长度m=n-1、指数lambda^n、
累计v^-q一致。平方根Re正；arg(1-W)取负连续支，
dp+a0W及rp+a0W在右上象限。完整连续相位准确为

    chi_n(t)=n[-arg(1-W)+p arg(dp+a0W)]
                    -theta/2-(1/2)arg(rp+a0W)。             (1)

最后两项是完整振幅H的相位，不可删除或用m代n。
固定p时S92的领先分支证明使h随tau严格增加：K=a0h/(dp)严格随theta增，
正系数a_s=a0 tau/(1-p)=h^d[-sin(rtheta)/sin(theta)]亦严格增。
因此两端间nh>=左端nh、n/h>=右端n/h；chi连续即可，不要求其完整严格单调。

## 2. 原端：全部p0∈[0,p_max]及准确j标签

令P_n=p(1-p)^d，固定足够大S2相位圆Y_j=T_j^d，取

    tau_L=Y_j/(P_n n^r)。

乘驻点式以n^r：

    (1-p)(nW)^r+[a0Y_j/(P_n n^(r-1))](nW)+dpY_j/P_n=0。

沿p趋p0，线性系数O(1/(q n^(r-2)))趋0。
唯一领先分支于是

    nW -> d^(1/r)Y_j^(1/r)/(1-p0) exp(i pi/r)。           (2)

q趋无穷使W/p=O(1/q)，包括p0=0。n log(1+tau)=o(1)，
所以n log lambda_*=nW+o(1)，
-q log v_*=a0 nW/d+o(1)，误差q|W/p|²=O(1/q)。
rp+a0W的辐角趋0，theta趋pi/r。由d+a0=r(1-p)，(1)给

    chi_n(t_L) -> [r/d^(d/r)]Y_j^(1/r)sin(pi/r)-pi/(2r)。 (3)

S2准确连续Psi(T_j)=j pi，Wright展开使(3)距j pi为O(A_j^-1/2)，
A_j=(T_j/d)^(d/r)。选择固定足够大j即可小于pi/8。
该选择共同于p0∈[0,p_max]；真实圈与符号来自S1或S3+R1，先固定j。
同时nh_L趋d^(1/r)Y_j^(1/r)/(1-p0)，随j可任意增大。

## 3. 倒端：不能丢n(pi/d-theta)项

整数参数c=ceil((s+1)/d)，b=rc-n，a_n=dc-s-1∈0..d-1，D=n-c。
p<=p_max给b~n a0/d趋无穷，S4尺度Lambda=s^d(q+b)/b满足

    Lambda/n^d ->(1-p0)^r/(1-rp0)。

固定a_n取子列，令T=T_(a_n,k)=pi(k+a_n/d)/sin(pi/d)，取

    tau_U=Lambda/T^d。

K=a0h/(dp)，rho=sin(dtheta)/sin(theta)，tau=h^d(h+K)rho。
大h时K趋无穷、K rho趋1、theta趋pi/d，因此

    h/n ->(1-p0)/T，n/h->T/(1-p0)。                      (4)

设epsilon=pi/d-theta。由角K式的Taylor，共同于p<=p_max、h大：

    epsilon=sin(pi/d)/(dK)+O(K^-2)
           =p sin(pi/d)/(a0h)+O(p²/h²)。

不能在p0>0时扔掉n epsilon有限项。准确展开

    -arg(1-W)=pi-theta-sin(theta)/h+O(h^-2)，
    arg(dp+a0W)=theta-dp sin(theta)/(a0h)+O(p²/h²)，
    arg H=-theta+O(p/h)。

所以

    chi_n=[n(d-1)+q-1]pi/d
          +(n-q+1)epsilon-n sin(theta)/h
          -q dp sin(theta)/(a0h)+o(1)。

第一个整数项准确D pi+a_n pi/d；有限1/h系数

    (1-p)p/a0-1-dp²/a0=p-1，

给最后完整标签

    chi_n(t_U)=D pi+a_n pi/d-T sin(pi/d)+o(1)
              =(D-k)pi+o(1)。                            (5)

该式包括p0=0，n epsilon此时趋0；没有未知整数偏移。
倒端准确k根及边界符号(-1)^(D-k)须用S4真实计数，不由(5)本身推出。

## 4. 中带资源门的准确衔接

Sigma=K sqrt(n Re V)，准确

    Sigma²=n a0² h(1-p)(dK+r cos(theta))/d²。

p<=p_max<1/r使a0有正下界、cos(theta)>=cos(pi/d)>0，
所以Sigma²>=c_(r,p_max) nh。
两端间nh和n/h分别受(2)、(4)控制，由固定大j,k可任意提高下界。
q、n-rq随n趋无穷。实际中带的联合序列o(Mscale)可转为有限L门：
五指标q,n-rq,nh,n/h,Sigma均>=L时，绝对误差<Mscale；
否则按L选失败序列，违背已证全部增长域共同o门。
在chi=ell pi的网格，实际值符号(-1)^ell；不除以相消的两峰实部。

本页至此只建立可执行的连接。准确degree、端盘根数和有序网格的
整体联合量词另在S6冻结；S4若未验收，不提前登记actual全轴PASS。
