# 全部附加依赖：亚线性外部数的完整lambda紧域预算

2026-10-04，主线程冻结待独审；不再只检查第一系数。
对象沿本case：s>=6、q>=2、N=s+1>=2(q−1)，m=q−1，lambda²=N²m。
记Delta_n(x)=sum_K delta_(n,|K|)(x)。

## 1. 完整函数的共同可求和界

令beta=q/N<=1。对全部固定R>0，候选显式界

    sup_(|z|<=R)|Delta_n(z/lambda²)|
       <=exp(nR/lambda²) beta² (1024R)
            sum_(k>=0) (1024 beta R)^k/(3k)!。          (1)

因此任意q/N→0的序列，其总校正在每个lambda²尺度复紧域一致趋0，
包括任意固定q和任意亚线性增长q；任意固定阶缩放z导数也趋0。
不对原x导数作无权趋零主张。

证明：每个K的坏点外部和z0<=t−1，内部和I=3t−z0>=2t+1。
盒上界使至少三个K坐标为正；选一个三子集，先给它们各1，再放弃内部上界，
给有效的并集上界

    D_h(t)<=binom(h,3) sum_(z0=0..t−1)
        binom(z0+n−h−1,z0) binom(3t−z0+h−4,3t−z0−3)。

因为h<=q+1，S1外部点对packing给sum binom(h,3)<=q(q²−1)/6。
对1<=t<=q+1，有n+t<=3N、3t+h−4<=4q，故

    sum_K D_(h_K)(t)
      <=q³/6 sum_(z0=0..t−1)
          (3N)^z0 (4q)^(3t−z0−3)/[z0!(3t−z0−3)!]。

使用m>=q/2，除lambda^(2t)，每项至多

    128^t beta^(2t−z0)/[z0!(3t−z0−3)!]。

beta<=1且z0<=t−1，因此beta^(2t−z0)<=beta^(t+1)。
有限倒阶乘和不超过2^(3t−3)/(3t−3)!（t=1也成立），得到

    sum_K D_(h_K)(t)/lambda^(2t)
      <=1024^t beta^(t+1)/(3t−3)!。                  (2)

Delta次数<=q+1由S0A。其第l系数是D总和与(1−x)^n的有限卷积；
对l<=q+1只需(2)的t<=q+1，并用binom(n,j)<=n^j/j!。
绝对系数和遂不超过exp(nR/lambda²)
乘sum_(t>=1)1024^t beta^(t+1)R^t/(3t−3)!，即(1)。
不把截断的D界用于无限t；使用的是Delta已知有限次数。
beta→0时n/lambda²=(N+m)/(N²m)→0，(1)在固定R为O_R(beta²)。
缩放导数由稍大固定盘及Cauchy给出。

## 2. q增长、beta→0时实际原端的非退化极限

当m→∞且m/N→0，父S9的临界统一支配给
P_abs(w/lambda)→B_0(w)，复紧域一致；B_0∈LP+、B_0(0)=1、阶<=2/3，

    B_0(w)=sum_(l>=0) w^l/[l! Gamma(1+l/2)]。

它非多项式、genus0且负根无限。令

    E_0(z)=[B_0(sqrt(z))+B_0(−sqrt(z))]/2，

由偶幂定义整函数，阶<=1/3。父J根筛中
(1±sqrt(z)/lambda)^n→1、q sqrt(z)/lambda→0，
故J(z/lambda²)→E_0(z)。
父S7显式R_single缩放界也适用lambda²：
令其z_parent=z n³/lambda²，原界中的|z_parent|/n
=|z|n²/lambda²=O_R(1/m)。其第一项为O_R(1/m)，
第二项O_R(n²/lambda^4)=O_R(1/(N²m²))，故R_single趋0。
加上(1)，真实全部依赖h*(z/lambda²)→E_0(z)，连同固定阶z导数。

## 3. E_0全部简单严格负根

写B_0(w)=prod_j(1+w/a_j)，a_j>0，sum 1/a_j<∞。
有限截断的偶部只负根：在w=iy，phase=sum atan(y/a_j)严格增，
终phase等于因子数pi/2，相位网格与准确偶部次数耗尽根数。
有限偶部趋E_0，Hurwitz排除非负/非实根；常数1、正系数排除0及正轴。

无穷乘积在iy处非零，

    E_0(−y²)=|B_0(iy)| cos(Psi(y))，
    Psi'(y)=sum_j a_j/(a_j²+y²)>0。

固定y局部绝对收敛由sum1/a_j支付。Psi(y)→∞由无限因子及单调收敛给出，
每次cos零点的y导数非零，故z=−y²零点严格负且简单，且无限。
不从紧域有限简单根自动推出极限简单，而是用上述严格phase支付。

## 4. 全q范围的lambda固定紧域统一候选

对每固定R，候选全对象统一最终h*(z/lambda²)盘内全部根简单严格负，
并[-R,0]上的|p|+|p'|存在统一正界。
反证序列分三种：

- q有界：取q固定子列；父FIXED-OUTSIDE S2 §4.1给N²尺度g_m简单负，
  lambda²=mN²只作固定正缩放，完整附加依赖校正趋0。
- q→∞且m/N→0：本页§2–3的E_0简单负。
- q→∞且m/N→kappa∈(0,1/2]：lambda²/n³→kappa/(1+kappa)^3>0，
  本case S2的巨H完整宏观谱只作固定正缩放，非退化且简单负。

每种均有复紧域C^1收敛；局部Rouche与共轭性、函数/导数共同零矛盾
给统一阈值和分离界。此§4须S2完整新范围审计成立，不能继承r>=4标签。

## 5. 仍未支付全轴

比n³固定紧域更强：即使q=o(n)，也能检查实际非退化lambda²原端。
但R仍固定；不排除|lambda² rho_n|→∞的非实或多重根。
(1)的可求和界在R增长时可能巨大；不能把O_R(beta²)说成全y统一小。
下一步应分析P_abs的有限尺度模增长与delta增长域预算，
而不是继续增加固定参数或将本页原端候选包装为全轴成果。
