# 一般秩：发散巨H倒端与准确圆

2026-10-06，固定r>=5、d=r-1，重新支付旧rank4 S22/S52的全d量词。
候选内部HOLD；只给实际倒端紧域及固定圆，不由此宣布全轴。

## 1. 精确实际参数及codegree

连通rank-r paving，n个元素，最大H0大小s=n-q，q>=2，q<n/r。
取

    c=ceil((s+1)/d)，b=rc-n，a=dc-s-1 in{0,...,d-1}，D=n-c。

假设b趋无穷（等价于n-rq趋无穷），所以最终c>=ceil(n/r)。
准确s=dc-a-1，q=c+a+1-b，q+b=c+a+1；s,q+b与n共同同阶。
每个其他有效H大小v<=q+d-1，交H0至多d-1。

内部点层必须l>=ceil(n/r)，且d l>=s+1，所以l>=c。
在c层把全部坐标置1，额外b单位置于q个外部坐标；
每外部坐标额外上界c-2，最终q(c-2)>=b：
q(c-2)-b=(q-1)c-q-a-1>=c-a-5，q>=2且c趋无穷。
H0和=s<dc；其他H和<=v+b<=c+a+d<dc。
所以该层内部点存在，codegree准确c、degree准确D，顶系数A0>0。
没有假设存在b个不同外部坐标。

## 2. 全实际固定j计数

令L_j=L_M^circ(c+j)、A_j=[x^(D-j)]h*_M。
H0额外和u<=dj+a；固定j时H0坐标上界最终失活。
全部其他H同时失活，因其和<=v+b+rj<=c+a+d+rj<d(c+j)。
忽略外部坐标上界的完整数是

    Ltilde_j=sum_(u=0..dj+a) binom(s+u-1,u)
                         binom(q+b+rj-u-1,b+rj-u)。       (1)

顶项u=dj+a占优，相邻往下比O_j(1/b)，因为内部比O_j(1/s)、
外部比O_j((q+b)/b)，(q+b)/s共同有界。
顶项为binom(s+dj+a-1,dj+a)binom(q+b+j-a-1,b+j-a)。

一个外部坐标越界需额外>=c+j-1，移除后残额

    b+rj-u-(c+j-1)=a+2-q+dj-u。

只有q<=a+2+dj（固定有界q）时可能；完整越界数O_j(1)。
此时基准外部binom至少常数倍b^(q-1)，q>=2，因此全部相对扣除趋0。
所以L_j/顶项趋1，共同于全部q速度与合法附加H配置。

取Lambda=s^d(q+b)/b，固定j给

    L_j/(L0 Lambda^j)->a!/(dj+a)!。

准确内部Ehrhart卷积A_j=sum_(ell=0..j)(-1)^ell binom(n,ell)L_(j-ell)，
额外项归一化含(n/Lambda)^ell=O((b/n^d)^ell)->0。
定义整个互反多项式

    Q_n(z)=(z/Lambda)^D h*_M(Lambda/z)/A0。

候选Q_n(z)->a! V_(d,a)(z)，V_(d,a)=sum z^j/(dj+a)!。
a有有限d种，先取常值子列即可；所有有限阈值最大给全序列结论。

## 3. 全k支配及紧域，不只逐项

非负h*给0<=A_j<=L_j，j<=D=O(n)。L0最终至少顶项一半。
用(1)上界，置u=dj+a-v；内部相对基准至少a次阶乘后给

    C_a a! (C s)^(dj-v)/(dj+a-v)!，

外部相对基准增量j+v给[C(q+b)/b]^(j+v)。
若dj-v负，至多a的有限负指数由同一Gamma比及s>=1吸收，
常数统一；j<=D、s/q+b与n同阶确保全部乘积因子为C n。
除Lambda^j并吸收(q+b)/s的共同界，得到

    A_j/(A0 Lambda^j)
      <=C_a C^j sum_(v=0..dj+a) (C0/b)^v/(dj+a-v)!。       (2)

v0=ceil(dj/2)，b>=2C0；v<v0部分至多2/[floor(dj/2)!]，
v>=v0部分至多e(C0/b)^ceil(dj/2)。
任意固定复盘R，先b足够大使CR(C0/b)^(d/2)<1/2，
尾由共同可求和阶乘及几何2^(-j)支付。
固定系数加此共同尾给整个复紧域与全部固定阶导数收敛。

## 4. V_(d,a)根性及准确大圆，不欠整数索引

Gauss给

    V_(d,a)(z)=a!^(-1)sum (z/d^d)^j /
                       prod_(ell=1..d)((a+ell)/d)_j。

ell=d-a的参数准确1。其他全为正逆Pochhammer乘子，保留1/j!给
R4阶乘严格化，故V属LP+、无限简单严格负根，阶1/d<1。

令phi=pi/d，T_k=pi(k+a/d)/sin(phi)，全部充分大整数k（阈值依d,a），
候选|z|<T_k^d准确k根、圈周无零。
直接全上半圆证明：取z=T_k^d exp(i vartheta)，w=T_k exp(i vartheta/d)，

    d w^a V_(d,a)(z)=sum_(ell=0..d-1)omega^(-a ell)exp(omega^ell w)，
    omega=exp(2pi i/d)。

除主项exp(w)，相邻项比值

    E=omega^a exp[(omega^(-1)-1)w]。

delta=pi-vartheta时，准确

    |E|=exp[-2T_k sin(phi)sin(delta/d)]，
    arg E=-2[T_k sin(phi)-a phi]
           +2T_k sin(phi)(1-cos(delta/d))。

delta<=1/T_k时arg E=O(1/T_k)模2pi，Re E>=0；
delta>=1/T_k时|E|<=eta_d<1，利用sin(delta/d)>=c_d delta。
其余d-2支主角绝对值>=2pi/d，主项角<=pi/d，
余量/主项<=C_d exp[-T_k(cos(pi/d)-cos(2pi/d))]。
所以完整比值d w^a V/exp(w)位于严格右半平面。
vartheta0及pi端比值均正实（后者主项/w^a相位为k pi）。
V的连续arg负端准确T_k sin(phi)-a phi=k pi；
LP+ genus0逐因子相位给准确k根，没有人工T^a零点计入V。
只声称全部充分大k，不对小k逐条扩表。

## 5. 实际准确固定圈与未证门

上述紧域及简单性把任意固定足够大k圆传给Q_n准确k简单负根。
对应原h*的|x|>Lambda/T_k^d准确k简单负根，边界符号(-1)^(D-k)，
因为A0>0，互反乘因子负端号为(-1)^D。
内部盘与外部盘准确计数不等于中带全部degree覆盖。
下一步在一般r的lambda_*^n v_*^(-q)H连续相位中重新支付两端标签，
包括宏观p固定时n(pi/d-theta)的有限修正，不沿用p趋0时丢项。
新颖性UNKNOWN；本页没有固定q的原端，也没有证明实际全轴。
