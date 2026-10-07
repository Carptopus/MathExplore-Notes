# 一般秩临界轮廓与共同Gaussian尾门

2026-10-05，主线程一般推导，待独审。阈值允许依赖固定r。
本页不证明全部根性或实际高秩全轴。

## 1. 全部整数缺口的准确轮廓

r>=3整数，b=0..r-1，g>=1，p=(r-1)/r，q=1/r，L=rg+b>=r。
F_(r,b,g)按研究计划定义；G(t)=t^b F(t^r)。令

    a_r(v)=p/v+q v^(r-1)。

任意R>1，对全部复t准确有

    G(t)=1/(2pi i) integral_(|v|=R)
       exp[t a_r(v)] v^(L-1)/(v^r-1) dv。

指数展开中成功数A、失败数B满足A+B=rj+b；留数要求
A-(r-1)B=L-r-rk，k>=0，即B=j-g+1+k。
这正是B>=j-g+1或A<=(r-1)j+b+g-1；总长度模r为b。
双指数展开与分母几何级数在固定R>1绝对收敛，交换合法。
缩至0<R<1后，所有r个单位根残数和为

    t^b V_(r,b)(t^r)=1/r sum_(nu^r=1) nu^b exp(t/nu)。

完整内圆保留原点本质奇点，余项I_L(t)不能删去。
有|I_L(t)|<=R^r/(2pi) integral exp[Re(t a_r(Re^(i theta)))]
                  /|1-R^r e^(ir theta)| dtheta。
这是因为R^L<=R^r；该上界完全不含g。

## 2. 负轴的完整角峰与固定r远弧缺口

取t=T exp(i pi/r)，于是t^r=-T^r；令phi=pi/r。
在单位圆，真实指数/T为

    f(theta)=p cos(phi-theta)+q cos(phi+(r-1)theta)。

导数准确为-2p cos(phi+(r-2)theta/2) sin(r theta/2)。
第一组驻点是theta=2pi k/r，值cos(phi-2pi k/r)；
最大恰由nu=1与exp(2pi i/r)取得，为c_r=cos(pi/r)>0。
第二组满足两cos相反，值至多(r-2)/r。
cos(pi/r)>=1-pi²/(2r²)>1-2/r，因为r>=3>pi²/4。
所以两主峰之外固定闭角集有依赖r的严格正缺口；没有遗漏更大非极点鞍。
两主峰角曲率为-(r-1)c_r<0。

## 3. 固定内移与准确渐近支配

置kappa=sqrt(2)/3，h_r=kappa/sqrt(r-1)，R=exp(-h_r/sqrt(T))。
峰nu附近v=nu exp(w)，w=(-h_r+i y)/sqrt(T)，准确Taylor为

    a_r(nu exp(w))=nu^(-1)[1+(r-1)w²/2+O_r(|w|³)]。

对每固定r，选充分小角窗epsilon_r，径向位移O(T^-1/2)不破坏负角曲率。
三阶余界的纯角项可吸收一部分-y²，混合径向项可由C_r|y|+C_r及
o(1)y²支付，故整个缩放角窗有可积共同Gaussian支配。
准确分母|1-exp(rw)|在该窗大于固定正系数乘r|w|；
规范化T^-1/2测度与分母T^-1/2相消，没有隐藏sqrt(T)因子。
在有界y窗，Taylor余项趋0，分母比趋1；高y由上述支配先截尾再取极限。
两峰外完整远弧有-c_r' T+O_r(sqrt(T))优势，粗分母
>=1-R^r>=C_r T^-1/2使其规范积分仍趋0。
全程在绝对值中先以R^L<=R^r丢弃L，故误差与g、b共同。

以两个主极点绝对振幅之和M_r(T)=2 exp(c_r T)/r规范，得共同上界

    limsup_(T->infinity) sup_(b,g) |I_L(t)|/M_r(T) <= beta_r，

    beta_r=1/(2pi) integral_R
      exp[c_r(kappa²-u²)/2+sin(pi/r) kappa |u|]
          /sqrt(kappa²+u²) du，u=sqrt(r-1)y。

## 4. 领先预算对全部r有严格余量

c_r>=1/2，sin(pi/r)<=sqrt(3)/2。因此与r=3相同kappa的指数相比，
差值不超过(c_r-1/2)kappa²/2<=kappa²/4=1/18；负的u²项和sin差项只改善界。
rank3的对应beta_3即父S15中h=1/3的完整Gaussian上界，小于903/1000。
由exp(1/18)<18/17，

    beta_r< (18/17)(903/1000)=16254/17000<957/1000。

故每固定r存在T0(r)，对全部T>=T0(r)、全部b,g，
完整内圆余项满足|I_L|<(98/100) M_r(T)。
其余r-2个极点相对M_r在固定r时指数消失。
在T_(i,r,b)=pi(i+b/r)/sin(pi/r)处，两主极点和相位为i*pi，
乘去t^b后符号(-1)^i。增大依赖r的共同T0即可让其他极点小于余量，
因此全部g在充分远负轴网格有同一交替符号。

## 5. 本门未完成的义务

领先余量对r共同，不代表T0共同于r，也不表示负轴符号在所有i成立。
负轴尾保号不证明完整复圆准确根数或紧域无非实根；
更不支付真实rank>=4 paving的次数、两端传递、移动中带或巨H。
审计须核完整角峰、径向Gaussian支配、sup_g量词、规范系数及父beta3比较；
任何实质缺口修订，不靠有限r或高精度采样补成一般定理。
