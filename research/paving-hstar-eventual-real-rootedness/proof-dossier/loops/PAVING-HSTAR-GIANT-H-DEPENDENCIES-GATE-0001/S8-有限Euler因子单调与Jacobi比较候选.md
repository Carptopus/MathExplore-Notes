# 有限Euler因子：参数单调与全部根的粗尺度下界候选

2026-10-04，主线程新冻结候选，待独核。不是实际h*根性；只支付父Pabs模下界。
沿N趋无穷、m趋无穷、m/N趋0，最终N>=24m，m>=2。

## 1. 插入一个因子的严格单调

对d个参数gamma_i>1/N，定义

    F(z)=(1−z)^(N+d) prod_i(1+gamma_i Theta_z)(1−z)^(-N)。

串行Euler门给F恰d次、常数1、全部简单负根，写根为−a_j，a_j>0。
再插gamma=1/phi>1/N（0<phi<N），新多项式为

    T_gamma F=(1−z)F+gamma[z(1−z)F'+(N+d)z F]。

在负轴非旧根处，根方程准确为

    phi + H(x)=0，
    H(x)=xF'(x)/F(x)+(N+d)x/(1−x)，
    H'(x)=sum_j a_j/(x+a_j)^2+(N+d)/(1−x)^2>0。       (1)

最左区间H(−infinity)=−N，右端趋+infinity；每个内部极点区间
H由−infinity增至+infinity；最右负区间由−infinity增至H(0)=0。
0<phi<N使每段有唯一简单根。gamma增加即phi下降，−phi增加，
每个根向右移动。因此按次序排列的根是每个gamma_i的严格递增函数。
删除任一参数后再插回允许证明逐坐标单调；乘算子本来可交换，
无需维持特定插入顺序。

## 2. 真正父Pabs的比较方向

父A(t)=prod_(i=1..m)(1+w_i t)，第i个根在(−i,−i+1)，故w_i>1/i。
父Pabs使用gamma_i=w_i/2。比较gamma_i先降至1/(2i)，再降至1/(m+i)：
因2i<=m+i，两个变化都只使各根向左移动。
N>2m支付全部参数大于1/N的条件。

于是Pabs的每个负根均在Q的对应根右侧，其中

    Q(z)=(1−z)^(N+m)
         prod_(i=1..m)(1+Theta_z/(m+i))(1−z)^(-N)
        =2F1(−m,m+1−N;m+1;z)。                     (2)

身份可由无上限第l系数
(N)^[l](2m+1)^[l]/[(m+1)^[l]l!]，随后Euler变换直接核。
Q常数1。其参数识别是既有经典工具，不认领新Jacobi理论。

## 3. Jacobi三对角矩阵给根的粗上界

令t=z/(z−1)。Pfaff变换给

    Q(z)=(1−z)^m 2F1(−m,N;m+1;t)，

后一个多项式为P_m^(alpha,b)(1−2t)的正归一，
alpha=m、b=N−2m−1。它在t的权重t^alpha(1−t)^b下正交。
经典身份来源：[DLMF18.5.7](https://dlmf.nist.gov/18.5.E7)；
三项递推来源：[DLMF18.9.2](https://dlmf.nist.gov/18.9.E2)。
不依赖来源中的现代定理，下面显示所用矩阵元及界。

该m阶实对称Jacobi矩阵的对角j=0,...,m−1为

    b_j=1/2+(alpha²−b²)/[2d_j(d_j+2)]，d_j=2j+alpha+b，

副对角j=1,...,m−1为

    a_j=sqrt(j(j+alpha)(j+b)(j+alpha+b))
          /[d_j sqrt(d_j²−1)]。                    (3)

其特征值就是m个t根。N>=24m、m>=2使b>=alpha、d_j>=N−m−1>1。
因为

    d_j²+alpha²−b² <= (2j+2alpha)d_j，

所以b_j<=(j+alpha+1)/(d_j+2)<=2m/(N−m+1)<=3m/N。
又j+b<=d_j、j+alpha+b<=d_j，且j(j+alpha)<=2m²，故

    a_j<=sqrt(2)m/sqrt(d_j²−1)<=2m/N。

最后一步可由d_j>=N−m−1及N>=24m、m>=2平方核验。
行和/Gershgorin给每个t根<=7m/N；为避免优化常数，仅保留<=12m/N<=1/2。
原z根的绝对值t/(1−t)<=24m/N。

由§2逐根比较，父Pabs=prod_(i=1..m)(1+sigma_i z)满足

    sigma_i >= N/(24m)，
    |Pabs(iy)| >= [1+(Ny/(24m))²]^(m/2)。            (4)

## 4. 准确用途

(4)在y/(q/N)有正下界时提供exp(c*m)模优势，不要求有限根分布收敛。
但y/(q/N)趋0时，该界单独仍不足；那里另需增长原端的模估计。
此文件不支付Delta，不证明全部实际根，不审新颖性，不写稿/Git/发布。
