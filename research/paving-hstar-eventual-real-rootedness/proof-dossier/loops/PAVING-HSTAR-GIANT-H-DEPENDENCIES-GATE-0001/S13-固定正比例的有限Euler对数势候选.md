# 固定正比例：有限Euler的全裂平面对数势候选

2026-10-05，主线程冻结待独审。不是实际h*根性，也没有证明附加Q0中带。
沿父准确A/Pabs：N>=2m、m趋无穷、m/N趋kappa∈(0,1/2]。
Pabs(z)=prod_i(1+sigma_i*z)，sigma_i>0。
本页为固定非零z提取真实有限Pabs的增长率，不从固定缩放盘外推。

## 1. 所有生成阶l的Newton夹逼

记A0(t)=binom(m+t,m)。父有限Newton定义，对所有整数l>=0有

    A(l/2)/A0(l/2)
      =sum_(j=0..min(m,l))
         (m)_fall_j*(l)_fall_j/[(N)_rise_j*(1+l/2)_rise_j]。

每项非负，且至多(2m/N)^j<=1。
注意此处l不限制在Pabs次数内：下降因子在j>l时为0。
故1<=A(l/2)/A0(l/2)<=m+1。

对0<z<1，无上限Euler生成身份的各项为正，设

    W_Nm(z)=(1−z)^(N+m)
       sum_(l>=0) binom(N+l−1,l)*binom(m+l/2,m)*z^l，

则W_Nm(z)<=Pabs(z)<=(m+1)W_Nm(z)。
这里比较的是正实生成值，不声称同一复数上的模夹逼。

## 2. 一个严格单峰的实鞍点

令b=l/N。有限Stirling给生成求和项的每N对数极限

    g_kappa(b;z)=(1+b)log(1+b)−b log b
      +(kappa+b/2)log(kappa+b/2)−kappa log kappa
      −(b/2)log(b/2)+b log z。

其导数为

    g'=log((1+b)/b)+1/2 log((2kappa+b)/b)+log z，
    g''=−1/[b(1+b)]−kappa/[b(2kappa+b)]<0。

g'(0+)=infinity，g'(infinity)=log z<0，故唯一b=b_kappa(z)>0，满足

    z=b^(3/2)/[(1+b)*sqrt(2kappa+b)]。              (1)

对kappa紧正范围，l<=BN的Stirling误差O(log N)，b=0用连续约定；
下界取最接近Nb的整数项，上界有限BN项乘多项式数量。
尾部不用无限阶Stirling外推：相邻项比对l>=BN至多

    z*(1+N/l)*exp(m/l)<=z*(1+1/B)*exp(kappa_max/B)。

选固定B大到此数<rho<1，则尾部几何可和；并将B置于鞍点之后。
因此正实完整求和的log/N极限为max g。
代(1)化简max g=log(1+b)+kappa log(1+b/(2kappa))，所以

    L_kappa(z)=(1+kappa)log(1−z)+log(1+b)
                  +kappa log(1+b/(2kappa))，0<z<1。 (2)

Newton夹逼m+1的对数除N趋0，(2)亦为log Pabs(z)/N。

## 3. 到固定虚轴的解析延拓，不对复数使用正项夹逼

在D=C\(−infinity,0]逐因子取principal log，

    L_N(w)=N^−1 sum_i log(1+sigma_i*w)。

各项在D解析，紧集K的|log(1+u*w)|<=C_K log(1+u)对u>=0成立。
父S9的有限粗系数支配给

    Pabs(1)<=sum_(l>=0)(l+1)*(3lambda/sqrt(2))^l/
                                [l!*Gamma(1+l/2)]，lambda=N*sqrt(m)。

Stirling的鞍点上界log右端=O(lambda^(2/3))=O(N)，
故L_N局部有界。由正轴(2)、正常族及恒等原理，L_N在D内局部一致
收敛到唯一解析函数L_kappa；其在0<z<1取(2)的值。
这也定义(2)的正确延拓分支，不自行挑选代数方程的任意根。
在D\{1}令

    b(z)=z*(L'_kappa(z)+(1+kappa)/(1−z))，

正轴上等于(1)的根，故恒等延拓给
z²*(1+b)²*(2kappa+b)=b³。z=1处允许b为极点，L本身解析。

固定y>0时，父epsilon趋0给P=Pabs−qz与Pabs模的比趋1，因而

    log M(y)/n → Re L_kappa(iy)/(1+kappa)+1/2 log(1+y²)。 (3)

没有从Pabs的固定缩放紧域极限偷渡到固定非零y。

## 4. 临界比例的显式表达

kappa=1/2时(1)化为z=(b/(1+b))^(3/2)，所以

    L_(1/2)(z)=3/2 log((1−z)/(1−z^(2/3)))。

在D用从正轴延续的对数，z=1为可去点；实部不依赖对数书写歧义。
因此临界固定y的完整幅度速率为

    log M(y)/n → log(1+y²)
                      −1/2 log(1−y^(2/3)+y^(4/3))。 (4)

例如y=1的速率log2来自表达式，不是数值拟合。
本页仍不证明其他K的Q0比(3)小，更不解决实际整类全轴。
下一步是将S4联动轮廓的最大指数与(3)比较；若界失败，只关闭该比较界。
全部内部HOLD，不写稿、Git或发布。
