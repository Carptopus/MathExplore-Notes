# 一般Wright相位圆：准确索引

2026-10-06。固定r>=5、d=r-1，冻结新候选待独审，内部HOLD。
对象B_r来自本门S1；其LP+/简单根可作为冻结输入，但本页自行重构Phi_d。
目标是B_r的大相位圆准确根数，不宣称实际增长圆传递或实际全轴。

## 1. 主张与记号

    Phi_d(w)=sum_(k>=0) w^k/[k! Gamma(1+k/d)]，
    Psi(T)=从0归一化的连续arg Phi_d(T exp(i pi/d))。

候选Phi_d属LP+、阶d/r<1、有无限负零点（本页不要求它们简单）。
Psi严格增至无穷。对全部充分大的整数j（阈值可依固定d），
唯一T_j>0满足Psi(T_j)=j pi，并有

    B_r在|z|<T_j^d内准确j个简单严格负根，圈周无零。(1)

同时准确连续相位

    Psi(T)=r(T/d)^(d/r) sin(pi/r)-pi/(2r)+O(T^(-d/(2r)))。(2)

不含未定2pi整数偏移；不把每个支模小于主支误作全部支和小于主对。

## 2. Phi_d的LP与全紧域构造

整数Q>=1，R_0(w)=1，

    R_m(w)=(w/d+m)R_(m-1)(w)+(w/d)R'_(m-1)(w)。

沿R_(m-1)各简单负根的符号，0和负无穷端，归纳给R_m有m个简单负根、
R_m(0)=m!；首项正。定义

    Phi_(Q,d)(w)=exp(w/Q^(1/d)) R_(Q-1)(w/Q^(1/d))/(Q-1)!。

它属LP+，且完整系数身份是

    [w^k]Phi_(Q,d)=Gamma(Q+k/d)/
          [Gamma(Q)Gamma(1+k/d)Q^(k/d)k!]。

固定k的Gamma比归一趋1，可用Gamma(Q,1)随机变量的固定矩收敛证明。
全k共同支配：sigma=k/d，ell=floor sigma，m=ceil sigma，sigma0另记。
Lyapunov矩不等式及(Q)_m/Q^m<=(1+m/Q)^m给

    Gamma(Q+sigma)/[Gamma(Q)Q^sigma]<=(ell+2)^sigma。

Gamma(1+sigma)>=e^(-1)ell!，ell>=1时ell!>=(ell/e)^ell，
因此右侧除Gamma(1+sigma)<=3e^3(2e)^ell<=3e^3 2^k（d>=4）。
ell0也由同一粗常数覆盖。故Phi_(Q,d)->Phi_d全复紧域及导数，LP类闭性适用。
Stirling给阶d/r<1，非多项式/genus0给无限负零点；常数1排除0。

genus0乘积Phi_d(w)=product_l(1+w/lambda_l)，lambda_l>0，
sum 1/lambda_l有限，按重数重复因子。由此

    Psi'(T)=sum_l lambda_l sin(pi/d)/|lambda_l+T exp(i pi/d)|²>0。

每因子辐角从0增到pi/d；无限因子使Psi趋无穷，T_j唯一存在。
同一乘积还给固定T时|Phi_d(T exp(i theta))|随|theta|从0到pi非增。

## 3. 主射线及稍扩扇区共同渐近

存在固定epsilon_d>0，小于pi/d，使整个
0<=theta<=pi/d+epsilon_d上，令w=d A^(r/d)exp(i theta)，A趋无穷，有

    Phi_d(w)=sqrt[d/(2pi r A)] exp[-i d theta/(2r)]
              exp[rA exp(i d theta/r)] [1+O(A^(-1/2))]。 (3)

误差对该稍扩闭扇区共同。以下证明扩扇区，不借用只覆盖主射线的渐近。
Gamma Hankel公式，负实轴为xi^(-1/d)支割，轮廓为半径A圆及两条负割线：

    Phi_d(w)=(1/(2pi i)) integral exp(xi+w xi^(-1/d)) dxi/xi。

逐项交换由圆的一致收敛和割线exp(-x)/x支配支付。圆上xi=A exp(i phi)：

    g_theta(phi)=exp(i phi)+d exp(i theta-i phi/d)。

Re g的驻点为

    phi=d theta/r+2pi d k/r，或phi=d(pi-theta+2pi k)/(d-1)。

在0<=theta<=pi/d、-pi<phi<pi仅第一族k0是内部最大，
第二族只在theta=pi/d到达phi=pi，那里是局部最小。
唯一全局峰phi0=d theta/r，值r cos(d theta/r)；端点值不超过d-1，
且r cos(pi/r)>d-1。完整复驻点同为phi0，

    g(phi0)=r exp(i d theta/r)，
    g''(phi0)=-(r/d)exp(i d theta/r)。

在该闭theta区间，峰外固定弧有共同严格缺口，峰附近实二次导数共同负。
由这些严格量的连续性，选择足够小epsilon_d>0，扩大到pi/d+epsilon_d，
峰仍唯一且有共同缺口，Re(-g'')>0；进入右端附近的第二驻点仍是局部最小。
同时缩小epsilon_d使cos(theta+pi/d)>=-1/2、主峰实部共同大于d-1。

割线xi=-x、x>=A的实指数为

    -x+d A^(r/d)x^(-1/d)cos(theta∓pi/d)。

在x=A至多(d-1)A，导数<=-1/2，所以割线积分<=C exp((d-1)A)/A，
相对主峰共同指数小。圆上共同Taylor/复Gaussian给相对O(A^(-1/2))；
Gaussian平方根从theta0的正实根延伸，得到(3)。

Phi_d在整个稍扩扇区无零（LP+及角度<pi）。(3)的比值在1的半径1/2盘，
theta0比值正实；盘的单值log与Phi_d从正轴延伸的log匹配。
因此没有整数相位债务，取theta=pi/d即给(2)。

## 4. 全上半圆的相位控制，不依赖有限Q同伦

根过滤准确

    d B_r(z)=sum_(k=0..d-1)Phi_d(omega^k w)，
    omega=exp(2pi i/d)，w^d=z。

取z=T_j^d exp(i vartheta)、0<=vartheta<=pi，w=T_j exp(i vartheta/d)。
主项Phi_d(w)，相邻项Phi_d(omega^(-1)w)。其余d-2项的主辐角绝对值
至少2pi/d；利用§2的角模单调及§3稍扩角theta_c=pi/d+epsilon_d，
它们除以主项之和绝对值<=C exp(-c_d A)，A=(T_j/d)^(d/r)。
这里主项模最小在pi/d，(3)使theta_c的模与该最小模仍有固定指数差。

定义

    E(vartheta)=Phi_d(omega^(-1)w)/Phi_d(w)，delta=pi-vartheta。

LP乘积给|E|<1，vartheta<pi；在vartheta=pi，准确
E=exp(-2i Psi(T_j))=1。不能只凭|E|<1说1+E共同远离0，须付近端：

- 0<=delta<=1/A：两射线都在稍扩扇区，(3)给连续相位
  arg E=-2Psi(T_j)+O(A delta²)+O(A^(-1/2))=O(A^(-1/2)) mod 2pi。
  用正实幅值表达E，足够大A使Re E>=0，所以Re(1+E)>=1。
- 1/A<=delta<=d epsilon_d：由(3)

      |E|=exp[-2rA sin(pi/r)sin(delta/r)] [1+O(A^(-1/2))]
           <=eta_d<1，

  常数eta_d可固定，利用A delta>=1及小固定delta的sin(delta/r)>=c_d delta。
- delta>=d epsilon_d：相邻射线绝对角至少theta_c，角模单调再次给
  |E|<=C exp(-c_d A)。

于是对整个上半圆，1+E加其余d-2项的共同指数小余量始终在严格右半平面。
在vartheta0比值dB_r/Phi_d正实；在vartheta pi该比值也正实，
因为Phi_d(w)相位j pi且B_r负实轴值为实，而比值实部已严格正。
因此其连续arg在两端均为0，沿弧无额外2pi跳变，准确

    从正轴起的连续arg B_r(-T_j^d)=Psi(T_j)=j pi。   (4)

## 5. 从准确连续arg到准确根数

本门S1的B_r属LP+、阶1/r<1、B_r(0)=1，所以genus0无指数因子。
取其负根按重数的乘积product(1+z/a_l)。沿上述上半圆，一个因子
在终点贡献连续arg pi，当a_l<T_j^d；贡献0，当a_l>T_j^d。
根过滤的共同右半平面比值已排除终点零，LP+排除其他圆周点零。
故(4)准确等于圈内根数乘pi，得到(1)。简单性来自S1，不从渐近继承。

这个论证只需全部充分大j，不主张每个小j；不需把有限Q的相位模优势
错误地认为对Q共同，也没有从d-2个逐项优势推出和优势。

## 6. 真实端点接口与未证门

S1实际紧域若成立，每个上述固定j圈可传真实准确j根。
本页圈可以先随j研究，但实际n极限时必须先固定j；尚未支付j随n增长。
与增长中带连接仍须准确比较lambda_*/v_*及H的相位，包括-pi/(2r)常数。
固定正比例宏观核与全部附加宏观H的同伦索引仍需另核，不自动引用rank4S53。
新颖性UNKNOWN；本页若PASS仍只是准确一般端核索引，不是实际全轴定理。
