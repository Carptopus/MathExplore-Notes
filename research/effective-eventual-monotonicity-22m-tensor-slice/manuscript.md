# Effective eventual monotonicity on the $(2,2,m)$ tensor slice

Carptopus  
carptopus@163.com

Draft date: 14 October 2026

Status: manuscript candidate; proof audited internally; not peer reviewed

## Abstract

Let $a(n_1,\ldots,n_p)$ denote the expected number of real critical rank-one
approximations to a standard Gaussian tensor of format
$n_1\times\cdots\times n_p$, in the normalization of Draisma and Horobeţ.
They conjectured that, beyond the boundary format, this expectation does not
increase when the largest format parameter is increased.  We prove an
effective eventual form on the first open infinite slice:

$$
a(2,2,m)<a(2,2,m-1)
\qquad\text{for every integer }m\ge 3\times10^{103}+3.
$$

The proof first converts the Kac--Rice integral into an absolute determinant
of a normalized random walk in $2\times2$ symmetric matrices.  Its exact
three-dimensional moment-generating function permits a weighted Edgeworth
expansion.  We certify positivity of the first even correction by symbolic
reduction and outward-rounded interval integration.  Explicit low-, middle-,
and high-frequency estimates then give a weighted Fourier remainder of order
$r^{-5/2}$ with a numerical constant, yielding the displayed threshold.

This is an effective asymptotic tail theorem.  It does not settle the finite
range below the threshold, including the smallest open comparison, and hence
does not resolve the full monotonicity conjecture.

## 1. Introduction

Draisma and Horobeţ studied the number of real critical points of the distance
from a general tensor to the variety of rank-one tensors [1].  Because the
real count depends on the tensor, they averaged it over the standard Gaussian
distribution.  Their Conjecture 1.3 states that, if

$$
n_p-1>\sum_{i=1}^{p-1}(n_i-1),
$$

then replacing $n_p$ by $n_p-1$ does not decrease the expectation.  The
matrix and several small-format cases are known, while the comparison between
the formats $(2,2,3)$ and $(2,2,4)$ is the smallest case left open in their
paper.

This paper proves monotonicity on an explicit tail of the entire $(2,2,m)$
slice.  The threshold is intentionally conservative: its role is to make the
asymptotic argument completely effective, not to approximate the first true
index of monotonicity.

In the sources checked through 14 October 2026, including the closest complex
count and determinant-asymptotic results [3,4] and the current problem and
preprint indexes [5,6], we found no prior proof of this effective tail
statement.  This is a bounded literature finding, not a claim of exhaustive
global priority.  The random-matrix reduction below is a specialization and
reorganization of the general Kac--Rice formulas in [1,2]; the Edgeworth,
Fourier, Plancherel, and Cauchy tools are standard.

### Theorem 1.1

For every integer

$$
m\ge 3\times10^{103}+3,
$$

one has

$$
a(2,2,m)<a(2,2,m-1).
$$

The theorem leaves every smaller parameter open unless it was already covered
by prior work.  In particular, it says nothing about the comparison
$a(2,2,4)\le a(2,2,3)$.

The proof has four parts.  Section 2 derives one common random-matrix model for
the whole slice.  Sections 3 and 4 identify an exact transform and the positive
first correction in its Edgeworth expansion.  Section 5 makes the Fourier
remainder effective in three frequency regimes.  Section 6 combines the
constants.  Section 7 records the computer-assisted certificates and their
scope.

## 2. A random walk in symmetric matrices

Let

$$
J=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad P=v_0v_0^{\mathsf T},
$$

where $v_0\sim N(0,I_2)$.  Let $(v_i,y_i,z_i)_{i\ge1}$ be independent, with
$v_i\sim N(0,I_2)$ and $y_i,z_i\sim N(0,1)$, and put

$$
K_i=v_iv_i^{\mathsf T}-y_i^2I_2+y_iz_iJ.                 \tag{2.1}
$$

For $r\ge1$ define

$$
I_r=\mathbb E\left|\det\left(P+\sum_{i=1}^rK_i\right)\right|. \tag{2.2}
$$

### Proposition 2.1

For every integer $m\ge3$,

$$
a(2,2,m)=\frac{\pi}{2(m-2)}I_{m-2}.                     \tag{2.3}
$$

#### Proof

Specialize [1, Theorem 1.1] to block sizes $1,1,m-1$.  If $t,s$ are
independent standard normal scalars and $x,y$ are independent standard
normal vectors in $\mathbb R^{m-1}$, all mutually independent, the formula is

$$
a(2,2,m)=
\frac{(2\pi)^{3/2}}{2^{(m+4)/2}\Gamma(m/2)}
\mathbb E|\det C_m|,                                    \tag{2.4}
$$

where

$$
C_m=
\begin{pmatrix}
t&s&x^{\mathsf T}\\
s&t&y^{\mathsf T}\\
x&y&tI_{m-1}
\end{pmatrix}.                                           \tag{2.5}
$$

Put $r=m-2$.  Schur complementation, initially for $t\ne0$ and then by
polynomial continuity, gives

$$
\det C_m=t^{r-1}
\det\!\left(t^2I_2+tsJ-GG^{\mathsf T}\right),           \tag{2.6}
$$

where $G$ is the $2\times(r+1)$ matrix with rows $x^{\mathsf T}$ and
$y^{\mathsf T}$.  Tilting a standard normal scalar by $|t|^{r-1}$ makes
$|t|$ chi distributed with $r$ degrees of freedom; its sign remains uniform
and independent.  Hence, for independent standard normal vectors
$u,z\in\mathbb R^r$,

$$
(t^2,ts)\quad\text{under the tilted law}
\ \overset d=\ (\|u\|^2,u\mathbin\cdot z),              \tag{2.7}
$$

where the sign of $t$ is absorbed into $s$.  The columns of $G$ are
$r+1$ independent $N(0,I_2)$ vectors.  Negating the $2\times2$ matrix inside
the determinant does not change its determinant.  Therefore (2.1)--(2.2)
and (2.6)--(2.7) yield

$$
\mathbb E|\det C_m|
=\mathbb E|N(0,1)|^{r-1}I_r
=\frac{2^{(r-1)/2}\Gamma(r/2)}{\sqrt\pi}I_r.            \tag{2.8}
$$

Substituting $m=r+2$ and (2.8) into (2.4) gives
$a(2,2,m)=\pi I_r/(2r)$, which is (2.3).

This is also the Wishart--Hessian decomposition obtained by specializing the
two-dimensional chi-field Kac--Rice formula of [2].  ∎

Consequently Theorem 1.1 is equivalent to the following statement.

### Theorem 2.2

For every integer $r\ge3\times10^{103}$,

$$
\frac{I_{r+1}}{r+1}<\frac{I_r}{r}.                       \tag{2.9}
$$

## 3. Exact transform and whitening

Write a symmetric matrix as $\bigl(\begin{smallmatrix}a&c\\c&b\end{smallmatrix}\bigr)$
and introduce the coordinates

$$
x_0=\frac{a+b}{2\sqrt3},\qquad
x_1=\frac{a-b}{2},\qquad
x_2=\frac c{\sqrt2}.                                    \tag{3.1}
$$

Let $X$ and $R$ be the vectors obtained from a single increment $K_i$ and the
initial matrix $P$ in these coordinates.  For $s=(s_0,s_1,s_2)$ set

$$
\begin{aligned}
d_1(s)&=\left(1-\frac{s_0}{\sqrt3}\right)^2-s_1^2-\frac{s_2^2}{2},\\
d_2(s)&=1+\frac{2s_0}{\sqrt3}-\frac{s_2^2}{2}.
\end{aligned}                                            \tag{3.2}
$$

The Gaussian quadratic-form identity gives

$$
M_X(s)=\{d_1(s)d_2(s)\}^{-1/2},\qquad
M_R(s)=d_1(s)^{-1/2}.                                    \tag{3.3}
$$

Define

$$
Y_r=\frac{R+X_1+\cdots+X_r}{\sqrt r}.
$$

Then

$$
M_{Y_r}(s)=d_1(s/\sqrt r)^{-(r+1)/2}
d_2(s/\sqrt r)^{-r/2}.                                  \tag{3.4}
$$

Moreover, with

$$
q(x)=3x_0^2-x_1^2-2x_2^2,
$$

the coordinate change (3.1) gives

$$
\frac1r\det\left(P+\sum_{i=1}^rK_i\right)=q(Y_r),
\qquad
\frac{I_r}{r}=\mathbb E|q(Y_r)|.                        \tag{3.5}
$$

The order-zero term of the logarithm in (3.4) is
$|s|^2/2$, so the increments are whitened: the limiting covariance is the
identity.

## 4. The positive first correction

Let $\phi$ be the standard Gaussian density on $\mathbb R^3$.  Expanding the
exact transform (3.4) through order $r^{-2}$ and translating monomials by
the Fourier--Hermite correspondence gives polynomials
$P_1,P_2,P_3,P_4$ such that formally

$$
p_r(x)=\phi(x)\left(1+\sum_{j=1}^4r^{-j/2}P_j(x)\right)
+\rho_r(x),                                             \tag{4.1}
$$

where $p_r$ is the density of $Y_r$.  The parity of $P_j$ is the parity of
$j$.  Since $|q|\phi$ is even, the odd terms integrate to zero.  Thus

$$
\frac{I_r}{r}=L+\frac Cr+\frac D{r^2}+e_r,              \tag{4.2}
$$

where

$$
L=\int|q|\phi,\qquad
C=\int|q|\phi P_2,\qquad
D=\int|q|\phi P_4.                                     \tag{4.3}
$$

The first even polynomial is

$$
\begin{aligned}
P_2={}&x_0^6/54-x_0^4x_1^2/9-x_0^4/36+x_0^2x_1^4/6
+x_0^2x_1^2/2+7x_0^2x_2^2/12-5x_0^2/4\\
&+x_1^4/12+x_1^2x_2^2/4-17x_1^2/12
+x_2^4/8-4x_2^2/3+121/72.                              \tag{4.4}
\end{aligned}
$$

### Lemma 4.1

The coefficient $C$ satisfies

$$
0.0853526992029<C<0.0864503864561.                       \tag{4.5}
$$

#### Proof

Integrate the Gaussian radial variable in (4.3) exactly.  On the unit sphere,
write $x_0/|x|=u$ and set $t=\sin^2\theta$ in the remaining angular
coordinate.  Since

$$
q(x)/|x|^2=(4+t)u^2-(1+t),
$$

the only zero for $u\in[0,1]$ is
$u_*(t)=\sqrt{(1+t)/(4+t)}$.  Splitting the absolute value at $u_*(t)$ and
integrating in $u$ symbolically yields

$$
C=\frac2\pi\int_0^{\pi/2}H(\sin^2\theta)\,d\theta,      \tag{4.6}
$$

where

$$
\begin{aligned}
H(t)=\frac1{8(t+4)^{7/2}}\bigl(&96t^6\sqrt{t+1}-48t^6\sqrt{t+4}
+1088t^5\sqrt{t+1}-472t^5\sqrt{t+4}\\
&+3360t^4\sqrt{t+1}-1098t^4\sqrt{t+4}
-1488t^3\sqrt{t+1}+1413t^3\sqrt{t+4}\\
&-2896t^2\sqrt{t+1}+4604t^2\sqrt{t+4}
+960t\sqrt{t+1}-2832t\sqrt{t+4}\\
&-192\sqrt{t+4}\bigr).
\end{aligned}                                            \tag{4.7}
$$

An outward-rounded interval Riemann sum over 20,000 equal subintervals of
$[0,\pi/2]$ gives (4.5).  The symbolic calculation verifies that (4.7) is
exactly the reduction of (4.4); the interval calculation supplies the strict
sign.  ∎

## 5. An effective weighted Fourier remainder

We now replace the formal remainder in (4.1) by a fully explicit bound.  All
Fourier transforms use the convention for which inversion has factor
$(2\pi)^{-3}$.

### 5.1. Global modulus bounds

For $u=(a,b,c)$ and $R=|u|$, direct multiplication gives

$$
\operatorname{Re}(d_1(iu)d_2(iu))
=1+R^2+\frac{b^2c^2}{2}+\frac{c^4}{4}-\frac{a^2c^2}{6}. \tag{5.1}
$$

It follows that

$$
|M_X(iu)|\le e^{-23R^2/94}\quad(R\le1),                 \tag{5.2}
$$

and

$$
|M_X(iu)|\le(1+R^2/2)^{-1/4}\quad(R\ge1).              \tag{5.3}
$$

For (5.2), use $a^2c^2\le R^4/4$ in (5.1).  For (5.3),
minimize $|d_1(iu)|^2$ in $a^2$ and split according as
$b^2\ge R^2/2$ or $a^2+c^2\ge R^2/2$.  In both cases the other
determinant factor has modulus at least one.

### 5.2. Low frequencies

Put $\varepsilon=r^{-1/2}$.  If $|u|\le1/4$, the logarithm of the increment
transform has a degree-six truncation $T_X$ satisfying

$$
|\log M_X(iu)-T_X(u)|\le4|u|^7.                         \tag{5.4}
$$

The initial factor has a degree-four truncation $T_R$ satisfying

$$
|\log M_R(iu)-T_R(u)|\le3|u|^5.                         \tag{5.5}
$$

Hence, for $|\xi|\le\sqrt r/4$,

$$
\left|\log M_R(i\xi/\sqrt r)+r\log M_X(i\xi/\sqrt r)
-T_R(\xi/\sqrt r)-rT_X(\xi/\sqrt r)\right|
\le r^{-5/2}(3|\xi|^5+4|\xi|^7).                      \tag{5.6}
$$

Exponentiating through order $\varepsilon^4$ and using (5.2) yields an
explicit $r^{-5/2}$ Gaussian envelope.  A complex-polydisc Cauchy estimate
with radius $1/[64(1+|\xi|)]$ upgrades it to all derivatives of order at most
four.  For $r\ge2^{16}$,

$$
\left\|(1-\Delta)^2\widehat\rho_r\right\|_{L^2(
|\xi|\le r^{1/16})}
\le B_{\rm low}r^{-5/2},                                \tag{5.7}
$$

where

$$
B_{\rm low}<1.220\times10^{50}.                         \tag{5.8}
$$

One explicit ledger is

$$
\begin{aligned}
B_{\rm low}&=3.2\times10^{19}\sqrt J,\\
J&=4\pi2^{67}\left[\frac12(0.94)^{-3/2}\Gamma(3/2)
+\frac12(0.94)^{-71/2}\Gamma(71/2)\right].             \tag{5.9}
\end{aligned}
$$

### 5.3. Middle and high frequencies

Let $A=r^{1/16}$.  For $A<|\xi|\le\sqrt r$, a complex polydisc of radius
$1/(64\sqrt r)$ remains in the zero-free region of both determinant factors.
The logarithmic displacement is below $1/4$.  Cauchy's estimate and (5.2)
therefore give

$$
|(1-\Delta)^2\widehat\rho_r(\xi)|
\le10^{30}r^6(1+|\xi|)^{40}e^{-23|\xi|^2/94}.           \tag{5.10}
$$

For $|\xi|=\sqrt r\,u$ with $u\ge1$, use a polydisc of radius
$1/[4096\sqrt r(1+u)^2]$.  Its logarithmic displacement is below $1/512$,
and (5.3) gives

$$
|(1-\Delta)^2\widehat\rho_r(\xi)|
\le10^{30}r^6(1+u)^{40}(1+u^2/2)^{-r/4}.                \tag{5.11}
$$

The gradient, zero-free, branch, and Cauchy-radius bounds leading to
(5.10)--(5.11) are finite polynomial inequalities; they are included in the
verification package.  Integrating (5.10) and (5.11) gives, for
$r\ge2^{128}$,

$$
\left\|(1-\Delta)^2\widehat\rho_r\right\|_{L^2(
A<|\xi|\le\sqrt r)}\le r^{-5/2},                        \tag{5.12}
$$

and

$$
\left\|(1-\Delta)^2\widehat\rho_r\right\|_{L^2(
|\xi|\ge\sqrt r)}\le r^{-5/2}.                         \tag{5.13}
$$

For example, after squaring (5.11),

$$
\int_1^\infty u^2(1+u)^{80}(1+u^2/2)^{-r/2}\,du
\le(3/2)^{-(r/2-43)}\frac{2^{123}}3.                   \tag{5.14}
$$

The logarithmic derivative of the resulting high-frequency bound relative to
$r^{-5/2}$ is

$$
\frac{37}{4}-\frac r4\log(3/2)<0                       \tag{5.15}
$$

throughout this range.

### 5.4. From Fourier space to the weighted expectation

Cauchy--Schwarz and Plancherel give

$$
\int_{\mathbb R^3}|q(x)|\,|\rho_r(x)|\,dx
\le\frac{3\sqrt5}{8\sqrt\pi}
\left\|(1-\Delta)^2\widehat\rho_r\right\|_2.          \tag{5.16}
$$

Here we used $|q(x)|\le3|x|^2$ and

$$
\int_{\mathbb R^3}\frac{|x|^4}{(1+|x|^2)^4}\,dx
=\frac{5\pi^2}{8}.
$$

Combining (5.7), (5.12), and (5.13), and rounding outward, gives

$$
|e_r|\le Kr^{-5/2},\qquad K<5.78\times10^{49}.          \tag{5.17}
$$

The exact second even Edgeworth polynomial has 51 monomials, all even and of
total degree at most twelve.  Termwise Gaussian moment bounds give

$$
|D|\le\frac{540373}{144}<3753.                           \tag{5.18}
$$

## 6. Proof of the main theorem

From (4.2), (4.5), (5.17), and (5.18),

$$
\frac{I_r}{r}-\frac{I_{r+1}}{r+1}
\ge \frac{C}{2r^2}-\frac{3|D|}{r^3}-\frac{2K}{r^{5/2}}. \tag{6.1}
$$

The right-hand side is positive whenever both inequalities

$$
r>\frac{12|D|}{C},\qquad
\sqrt r>\frac{8K}{C}.                                  \tag{6.2}
$$

The strict numerical margins below verify these inequalities at the chosen
integer threshold and therefore at every larger integer.

Outward-rounded interval arithmetic gives

$$
\frac{12|D|}{C}<5.28\times10^5,
\qquad
\left(\frac{8K}{C}\right)^2
<2.94\times10^{103}<3\times10^{103}.                   \tag{6.3}
$$

Therefore (2.9) holds for every integer
$r\ge3\times10^{103}$.  Proposition 2.1 with $r=m-3$ translates this into
Theorem 1.1.  ∎

## 7. Computer-assisted certificates

The proof uses exact symbolic computation and outward-rounded interval
arithmetic at three finite interfaces:

1. exact Gaussian quadratic-form determinants, whitening, and the two even
   Edgeworth polynomials;
2. symbolic reduction of $C$ to (4.6)--(4.7), followed by a 20,000-interval
   outward enclosure;
3. finite constant ledgers for the Cauchy bounds, Gaussian moments, and the
   threshold (6.3).

The archived verification package is described in `verification/README.md`;
`MANIFEST.sha256` fixes all nine checks, their shared exact Edgeworth generator,
the pinned environment, and the analytic ledgers in `supplement/`.  The package
also contains a destructive control showing that removing the initial
rank-one factor changes the first correction, together with fixed-seed
regression probes for the explicit analytic bounds.  Numerical quadrature
used to calibrate $I_1$ and $I_2$ is excluded from the proof.

The interval implementation uses `mpmath.iv` endpoints without conversion to
binary64 in the strict comparisons.  The proof does not infer a general
statement from a finite parameter search.

## 8. Scope and remaining problem

The threshold in Theorem 1.1 is a safe effective bound produced by deliberately
coarse global constants.  Improving those constants by a few orders of
magnitude would not address the main remaining difficulty: the interval

$$
1\le r<3\times10^{103}
$$

is still far beyond direct enumeration.  A full solution of the $(2,2,m)$
slice will require a structural comparison, a propagation theorem, or a much
stronger finite-core reduction.  No such statement is claimed here.

## References

[1] J. Draisma and E. Horobeţ, *The average number of critical rank-one
approximations to a tensor*, Linear and Multilinear Algebra 64(12)
(2016), 2498--2518. <https://doi.org/10.1080/03081087.2016.1164660>

[2] D. Marinucci and M. Stecconi, *Critical points of chi-fields*,
arXiv:2409.20129; ALEA 22 (2025), article 29.
<https://doi.org/10.30757/ALEA.v22-29>

[3] S. Friedland and G. Ottaviani, *The number of singular vector tuples and
uniqueness of best rank-one approximation of tensors*, Foundations of
Computational Mathematics 14 (2014), 1209--1242.
<https://doi.org/10.1007/s10208-014-9194-z>

[4] T. Tao and V. Vu, *A central limit theorem for the determinant of a Wigner
matrix*, Advances in Mathematics 231 (2012), 74--101.
<https://doi.org/10.1016/j.aim.2012.05.006>

[5] OpenProblemsInNLA, *TR-16: Expected number of critical rank-one
approximations of a Gaussian tensor*, status checked 14 October 2026.
<https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/tensor-computations/TR-16>

[6] OpenAI, *math* public preprint index, commit
`1581d4cbdd69a0faf34b2089614fe2a814316a6a`, checked 14 October 2026.
<https://github.com/openai/math>
