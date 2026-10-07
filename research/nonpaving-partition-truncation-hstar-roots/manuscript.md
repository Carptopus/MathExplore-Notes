# Eventual simple negative roots for rank-four capacity-two partition truncations

Carptopus

Draft date: 2026-10-07  
Status: version 0.1-beta preprint; not peer reviewed

## Abstract

Let \(m_1+\cdots+m_q=n\) be an arbitrary partition into positive integers and let

\[
M(\mathbf m)=\operatorname{trunc}_4\!\left(
  \bigoplus_{i=1}^q U_{\min(2,m_i),m_i}
\right).
\]

For every fixed \(0<\alpha<1/2\), we prove that there is an integer
\(N_\alpha\), independent of the number of blocks and of the particular partition,
such that, whenever \(n\ge N_\alpha\) and \(\max_i m_i\le\alpha n\), the Ehrhart
\(h^*\)-polynomial of the base polytope of \(M(\mathbf m)\) has degree
\(n-\lceil n/4\rceil\) and all of its roots are distinct, real, and strictly
negative.  The number of blocks may grow with \(n\), and blocks of sizes one and
two are allowed.

The proof has three parts.  An exact inclusion--exclusion formula reduces the
Ehrhart numerator to finitely many color levels.  A binomial-tail kernel is shown
to have positive real part after division by \(\cosh\sqrt t\); its even part
therefore has infinitely many simple negative roots.  Finally, a compactification
of decreasing block masses, allowing dust, gives a threshold uniform over all
partitions.  The two moving endpoint regimes are controlled by a cancellation
which uses \(\sum_i m_i=n\), rather than the number of blocks.  The threshold is
not made explicit.  The result does not cover the critical boundary
\(\alpha=1/2\), all small orders, other ranks or capacities, or arbitrary
nonpaving matroids.

## 1. Introduction

For a lattice polytope \(P\) of dimension \(d\), write

\[
  \sum_{\ell\ge0}|\ell P\cap\mathbb Z^N|z^\ell
  =\frac{h_P^*(z)}{(1-z)^{d+1}}.
\]

We study the base polytope of a rank-four truncation of a direct sum of
rank-at-most-two uniform matroids.  If the ground set is partitioned into blocks
\(E_1,\ldots,E_q\), with \(|E_i|=m_i\), then its real base polytope is

\[
P(\mathbf m)=\left\{x\in[0,1]^n:
  \sum_{e=1}^n x_e=4,\quad
  \sum_{e\in E_i}x_e\le2\ \text{for every }i
\right\}. \tag{1.1}
\]

Whenever the rank of the untruncated direct sum is at least four, this is a
rank-four capacity-two weighted multi-hypersimplex.  In particular this condition
holds throughout the eventual range of Theorem 1.1.  The family includes the
ordinary hypersimplex \(\Delta(4,n)\) when every block has size at most two, so it
would be inaccurate to call every member of the family nonpaving.  The object and
several of its counting descriptions belong to established weighted
multi-hypersimplex and split-matroid frameworks.  Our concern is the zero set of
its Ehrhart numerator, uniformly over nonuniform partitions.

### Theorem 1.1

Fix \(0<\alpha<1/2\).  There exists an integer \(N_\alpha\) such that the
following holds.  For every \(n\ge N_\alpha\) and every finite partition

\[
  m_1+\cdots+m_q=n,\qquad m_i\ge1,\qquad \max_i m_i\le\alpha n,
\]

the polynomial \(H_{\mathbf m}(z)=h^*_{P(\mathbf m)}(z)\) has degree

\[
  D=n-\left\lceil\frac n4\right\rceil
\]

and exactly \(D\) distinct roots, all lying on the negative real axis.

The threshold may depend on \(\alpha\), but not on \(q\) or on the partition.
We do not claim an explicit value of \(N_\alpha\), a threshold uniform as
\(\alpha\uparrow1/2\), or a statement at the critical boundary.

Adiprasito--Zhang [7, Theorem 3.1] already prove eventual simple negative
real-rootedness for ordinary fixed-rank hypersimplices.  Their rank-four
specialization covers our uniform subfamily, for which no novelty is claimed.
The increment here is a common threshold over all capacity-two partitions of
bounded maximum block ratio, including nonuniform partitions and a number of
blocks growing with \(n\).  This extends the object scope of that rank-four
specialization, not their theorem for all fixed ranks.  Section 9 records the
comparison with the full text of HAL version v1.

## 2. Degree and exact lattice-point formulas

The first point is that small blocks do not change the eventual degree.

### Lemma 2.1 (dimension and codegree)

For \(n\ge13\), under the hypotheses of Theorem 1.1, the matroid
\(M(\mathbf m)\) is connected and \(P(\mathbf m)\) has dimension \(n-1\).  Its
codegree is

\[
  c_0=\max\left(
    \left\lceil\frac n4\right\rceil,
    \left\lceil\frac{\max_i m_i+1}{2}\right\rceil
  \right). \tag{2.1}
\]

Consequently, for fixed \(\alpha<1/2\) and sufficiently large \(n\),
\(c_0=\lceil n/4\rceil\) and \(\deg H_{\mathbf m}=n-c_0\).

#### Proof

Let \(f\) be the total number of elements in blocks of sizes one or two, and let
\(c\) be the number of blocks of size at least three.  The rank of the untruncated
direct sum is \(f+2c\).  The bound \(\max_i m_i<n/2\) implies \(f+2c\ge5\)
when \(n\ge13\).  Every pair of elements extends to a five-element independent
set in the direct sum; that set becomes a circuit after rank-four truncation.
Thus all elements lie in one matroid component.

An interior lattice point of \(\ell P(\mathbf m)\) satisfies

\[
1\le x_e\le\ell-1,\qquad
\sum_e x_e=4\ell,\qquad
\sum_{e\in E_i}x_e\le2\ell-1. \tag{2.2}
\]

The possible sum over block \(E_i\) is the full integer interval

\[
\left[m_i,\min\{m_i(\ell-1),2\ell-1\}\right]. \tag{2.3}
\]

The lower endpoints sum to \(n\), so \(n\le4\ell\) is necessary.  Nonemptiness
of every interval is equivalent to \(m_i\le2\ell-1\).  Conversely, once these
conditions hold and \(\ell\ge\lceil n/4\rceil\ge4\), the sum of the upper
endpoints is at least \(4\ell\): this follows separately from
\(c\ge3\), \(c=2\), \(c=1\), and \(c=0\), using respectively
\(6\ell-3\), \(5\ell-3\), \(8\ell-7\), and \(n(\ell-1)\) as lower bounds.
The interval-sum property then gives (2.1).  The standard relation
\(\deg h^*=d+1-\operatorname{codeg}P\), with \(d=n-1\), completes the proof.
\(\square\)

We next record the exact coordinate inclusion--exclusion.  Put

\[
C_S(\ell)=\#\left\{y\in\mathbb Z_{\ge0}^n:
\sum_e y_e=(4-|S|)\ell-|S|,
\ \sum_{e\in E_i}y_e\le(2-\mathbf1_{i\in S})\ell-\mathbf1_{i\in S}
\right\}. \tag{2.4}
\]

Negative totals or upper bounds are interpreted as giving zero.

### Lemma 2.2 (finite color inclusion--exclusion)

For every \(\ell\ge0\),

\[
L_{P(\mathbf m)}(\ell)
=\sum_{S\subseteq[q],\ |S|\le3}
  (-1)^{|S|}\left(\prod_{i\in S}m_i\right)C_S(\ell). \tag{2.5}
\]

If

\[
R_S(z)=(1-z)^n\sum_{\ell\ge0}C_S(\ell)z^\ell,
\]

then

\[
H_{\mathbf m}(z)=A(z)-\sum_i m_iR_i(z)
+\sum_{i<j}m_im_jR_{ij}(z)-e_3(\mathbf m)z^3, \tag{2.6}
\]

where \(A=R_\varnothing\).

#### Proof

Apply inclusion--exclusion to the coordinate inequalities \(x_e\le\ell\).
Two selected violating coordinates cannot lie in the same block, since their block
sum would exceed \(2\ell\).  After subtracting \(\ell+1\) from one selected
coordinate in every selected block, one obtains (2.4).  If \(|S|\ge4\), the new
total is negative.  When \(|S|=3\), all block caps are inactive and
\(C_S(\ell)=\binom{\ell+n-4}{n-1}\), whose numerator is \(z^3\).  This proves
(2.5)--(2.6).  \(\square\)

## 3. The binomial-tail kernel

For a decreasing sequence \(p=(p_1,p_2,\ldots)\) with

\[
p_1\le\alpha,\qquad p_i\ge0,\qquad \sum_i p_i\le1,
\]

write \(d=1-\sum_i p_i\) for its dust mass and define

\[
B_m(p)=1-\sum_i\sum_{j=m+1}^{2m}\binom{2m}{j}p_i^j(1-p_i)^{2m-j},
\qquad B_0=1. \tag{3.1}
\]

For a finite probability vector this is the probability that no class receives
more than \(m\) balls in a multinomial experiment with \(2m\) trials.  Dust is
treated as an uncapped class.  Set

\[
G_p(t)=\sum_{m\ge0}B_m(p)\frac{t^m}{(2m)!},\qquad
F_p(z)=\sum_{k\ge0}B_{2k}(p)\frac{z^k}{(4k)!}. \tag{3.2}
\]

Let

\[
\mathcal P_\alpha^*=\{p_1\ge p_2\ge\cdots\ge0:
p_1\le\alpha,\ \sum_i p_i\le1\}. \tag{3.3}
\]

This space is compact in the product topology.  The estimate

\[
\sum_{i>R}\Pr\{\operatorname{Bin}(2m,p_i)>m\}
\le 2^{2m}(R+1)^{-m} \tag{3.4}
\]

shows that \(B_m\), hence \(G_p\) and \(F_p\) on compact subsets of the
complex plane, varies continuously with \(p\).

The analytic input is the following theorem.

### Theorem 3.1 (positive-real kernel)

For every \(p\in\mathcal P_\alpha^*\),

\[
\Re\frac{G_p(t)}{\cosh\sqrt t}>0\qquad(\Re t\ge0). \tag{3.5}
\]

Consequently \(G_p\) is Hurwitz stable, and \(F_p\) has infinitely many simple,
strictly negative real zeros.

#### Proof

We give the coefficient gate in detail because its uniformity is essential.  Put
\(N=4k\), \(T=2^{N/2}\), and, for one capped class, define

\[
C_k(x)=(-1)^k\sum_{m=1}^{2k}(-1)^m\binom N{2m}
 \sum_{j=m+1}^{2m}\binom{2m}{j}x^j(1-x)^{2m-j}. \tag{3.6}
\]

Write its degree-\(N\) Bernstein expansion as

\[
C_k((1-h)/2)=\sum_{\ell=0}^{N}U_k(\ell)\binom N\ell
h^\ell(1-h)^{N-\ell}. \tag{3.7}
\]

The scalar gate needed below is

\[
U_k(\ell)\le\left(1-\frac\ell N\right)U_k(0),
\qquad 0\le\ell\le N. \tag{3.8}
\]

We now prove (3.8).  Let

\[
S(u)=(-1)^k(2-u)^{N/2}P_N((2-u)^{-1/2}),\quad
B=S(0),\quad D_0=S'(0), \tag{3.9}
\]

where \(P_N\) is the Legendre polynomial.  Direct differentiation gives

\[
 \frac d{dh}C_k((1-h)/2)=(1-h)S'(h^2),\qquad
 U_k(0)=\frac{T-B}{2}. \tag{3.10}
\]

The Legendre equation, written in Prüfer coordinates between
\(\theta=\pi/4\) and \(\pi/2\), gives the non-asymptotic energy estimate

\[
-D_0\ge\frac{T\sqrt N}{4}. \tag{3.11}
\]

If \(S'(h^2)=\sum_{j\ge0}a_jh^{2j}\), the differentiated
hypergeometric equation gives

\[
2(j+2)(j+1)a_{j+2}+(j+1)(N-11/2-3j)a_{j+1}
+(j-(N-2)/2)(j-(N-3)/2)a_j=0. \tag{3.12}
\]

Besides \(a_0=D_0\), direct coefficient comparison gives

\[
\frac{a_1}{D_0}
=-\frac{N-5/2}{2}+\frac{N(N-1)B}{8(-D_0)}.
\]

The same energy estimate implies \(-D_0\ge NB/3\) for \(N\ge8\), and hence
\(-N/2<a_1/D_0\le(7-N)/8\le0\).  Thus
\(|a_1|<N(-D_0)/2\); the remaining case \(N=4\) has
\(a_1=-3/4\) and satisfies the same absolute bound.  Starting from these two
initial coefficients, induction in (3.12) yields

\[
|a_j|\le(-D_0)\frac{(3N/4)^j}{j!}. \tag{3.13}
\]

After conversion back to Bernstein increments, (3.13) proves (3.8) for

\[
0\le\ell\le\left\lfloor\frac{2(N-2)}{3\sqrt N}\right\rfloor. \tag{3.14}
\]

For the remaining prefix put \(e=N^{-1/2}\), \(a=\ell N^{-1/2}\),
\(v=e^2\), \(\rho=NB/(-D_0)\), and
\(b_j=a_jj!/(D_0N^j)\).  Equation (3.12) becomes

\[
\begin{aligned}
b_0&=1,\\
b_1&=-\frac12+\frac54v+\frac18(1-v)\rho,\\
b_{j+2}&=-\frac12\{[1-(3j+11/2)v]b_{j+1}
 +[1/4-(j+5/4)v+(j+1)(j+3/2)v^2]b_j\}.
\end{aligned} \tag{3.15}
\]

The same Prüfer phase gives

\[
\frac4{1+(\sqrt2-1)+(\sqrt2-1)/(2N)}
\le\rho\le
\frac4{1+(\sqrt2-1)+(\sqrt2-2)/(2N)}. \tag{3.16}
\]

Integrating (3.10) and converting to Bernstein form gives

\[
U_k(0)-U_k(\ell)=(-D_0)\sum_jb_j\frac{N^j}{j!}Q_j, \tag{3.17}
\]

where

\[
Q_j=\frac{\binom\ell{2j+1}}{(2j+1)\binom N{2j+1}}
-\frac{\binom\ell{2j+2}}{(2j+2)\binom N{2j+2}}. \tag{3.18}
\]

For \(N\ge256\) and
\(13\sqrt N/20\le\ell\le49\sqrt N/16\), outward rational interval
evaluation of (3.15)--(3.18), followed by

\[
\operatorname{Tail}_J\le
\frac{x^{J+1}}{(J+1)!(2J+3)}\frac1{1-x/(J+2)},
\qquad x=\frac{3a^2}{4(1-2v)^2}, \tag{3.19}
\]

proves \(U_k(0)-U_k(\ell)>(-D_0)\ell/(2N)\).  The 2403
certified interval leaves cover this entire compact rectangle, not a point grid.
Together with (3.11) and the overlap in (3.14), this closes the prefix through
\(\ell_0=\lceil3\sqrt N\rceil\).

For \(\ell_0\le\ell\le N/3\), let \(\operatorname{Pos}(f)\) denote the
sum of the strictly positive-power coefficients of a finite Laurent polynomial
\(f\).  The exact Laurent representation

\[
U_k(\ell)=(-1)^k\Re\operatorname{Pos}
\left[\left(1+\frac{i}{2}(z+z^{-1})\right)^{N-\ell}
(1+i/z)^\ell\right] \tag{3.20}
\]

and a coefficient Cauchy integral give

\[
|U_k(s+1)-U_k(s)|
\le\frac{5T}{8\sqrt N}e^{-3s^2/(16N)}. \tag{3.21}
\]

The tail beyond \(3\sqrt N\) is less than \(T/8\), so
\(U_k(0)-U_k(\ell)>T/4>(\ell/N)U_k(0)\) on this band.  For
\(\ell\ge\lceil N/3\rceil\), write \(r=N-\ell\),
\(K(z)=1+i(z+z^{-1})/2\), and \(L(z)=1+i/z\).  Cauchy's formula gives

\[
 |U_k(\ell)|\le
 \frac{\max_{|z|=R}|K(z)|^r|L(z)|^\ell}{R-1}. \tag{3.20a}
\]

On each of sixteen rational subintervals of \(s=\sin(\arg z)\in[-1,1]\),
exact Bernstein certificates prove

\[
 A^2B<7,\quad AB^3<13\quad(R=8/5),
 \qquad AB^3<8\quad(R=3), \tag{3.20b}
\]

where \(A=|K|^2\) and \(B=|L|^2\).  Interpolation in
\(\lambda=\ell/N\) therefore yields, for \(N\ge160\),

\[
 |U_k(\ell)|\le \frac53T
 \max\{(7/8)^{N/6},(13/16)^{N/8}\}<\frac{T}{16}
 \quad (N/3\le\ell\le3N/4),
\]

and

\[
 |U_k(\ell)|\le\frac12T(8/9)^{N/2}<\frac{T}{2N}
 \quad (3N/4\le\ell\le N-2).
\]

Together with \(T/4<U_k(0)<T/2\), these are (3.8); the last two indices
\(\ell=N-1,N\) vanish exactly.  For \(N=4,8,\ldots,156\), the remaining
2028 pairs \(\lceil N/3\rceil\le\ell\le N-2\) are closed by an independent
integer Laurent-recurrence certificate, including the three continuous
certificates in (3.20b).  Separately, the remaining
\(N<256\), \(1\le\ell<\lceil N/3\rceil\) comprise exactly 2646 integer
pairs; a second certificate reconstructs their Bernstein numerators from
(3.12) and checks (3.8) exactly.  The analytic bands and these two finite
complements cover every index and overlap at their joins.

Writing \(h=1-2x\), (3.8) gives

\[
C_k(x)\le U_k(0)\sum_{\ell=0}^N
\left(1-\frac\ell N\right)\binom N\ell h^\ell(1-h)^{N-\ell}
=2xU_k(0). \tag{3.22}
\]

Two classes cannot both receive more than half of the trials.  Therefore the bad
events are pairwise disjoint, and summing (3.22) over all classes uses only
\(\sum_i p_i\le1\).  The exact product identity on the boundary ray
\(w=x(1+i)\) then yields

\[
\Re\!\left(G_p(w^2)\overline{\cosh w}\right)
=1+\sum_{k\ge1}A_k(p)\frac{4^kx^{4k}}{(4k)!}>0. \tag{3.23}
\]

Indeed,

\[
A_k(p)\ge B_k:=(-1)^k2^{2k}P_{4k}(1/\sqrt2)>0. \tag{3.24}
\]

For the last sign, the continuous Legendre Prüfer phase at
\(\theta=\pi/4\) lies strictly between
\(k\pi+\pi/8\) and \(k\pi+3\pi/8\).

To pass from the boundary to the half-plane, use the signed arcsine measures
\(\mu_{p_i}\) for the binomial tails.  They give the exact identity

\[
 G_p(w^2)=\cosh w-
 \sum_i\int \cosh(w\sqrt{x})\,d\mu_{p_i}(x),
 \qquad
 \operatorname{supp}\mu_{p_i}\subseteq[0,4p_i(1-p_i)]. \tag{3.25a}
\]

Their total variations are

\[
 v(x)=1-\frac4\pi\arctan\sqrt{1-2x},\qquad 0\le x\le1/2. \tag{3.25}
\]

The function \(v\) is convex, \(v(0)=0\), \(v(1/2)=1\), and \(v(x)\le2x\).
Thus \(\sum_i v(p_i)\le2\), including countably many coordinates.  If
\(|\arg w|\le\pi/4\), then
\(|\cosh(a w)|\le|\cosh w|\) for \(0\le a\le1\); the support bound in
(3.25a) has \(\sqrt{x}\le1\).  Consequently the quotient in (3.5) is
analytic and bounded in the right half-plane, by three in modulus.
Its boundary real part is strictly positive by (3.23).  Mapping the half-plane to
the disk and applying the Poisson formula, with the point at infinity having zero
harmonic measure, proves (3.5).

Since \(G_p(0)=1\), has order at most \(1/2\), and is not a polynomial, its
genus-zero product has all zeros in the open left half-plane.  For every finite
canonical-product truncation, Hermite--Biehler places the zeros of its even part
on the negative real axis and interlaces them with those of the odd part.
The products and their first derivatives converge uniformly on compact sets, so
Hurwitz passes the location statement to the limit.  If
\(\theta_p(y)=\arg G_p(iy)\), the product gives

\[
 \theta_p'(y)=\sum_j\Re\frac1{\zeta_j+iy}>0. \tag{3.25b}
\]

where \(-\zeta_j\) are the zeros of \(G_p\).  Because
\(F_p(-y^2)=\Re G_p(iy)\), every zero is simple.  Positivity of the constant term
excludes zero.  \(\square\)

Moreover, if \(r=\sqrt{4\alpha(1-\alpha)}<1\) and \(u=\Re w>0\), then

\[
\left|\frac{G_p(w^2)}{\cosh w}-1\right|
\le \frac{4e^{-(1-r)u}}{1-e^{-2u}}. \tag{3.26}
\]

It follows that the phase and any fixed initial collection of zeros of \(F_p\)
are uniform over \(\mathcal P_\alpha^*\).  More precisely, take the continuous
phase

\[
\theta_p(y)=\arg G_p(iy),\qquad \theta_p(0)=0.
\]

The bound (3.26) gives, uniformly in \(p\),

\[
\theta_p(T^2)=T/\sqrt2+o(1). \tag{3.27}
\]

Consequently, for every sufficiently large fixed integer \(j\), the radius
\(T_j=\sqrt2\pi j\) contains exactly \(j\) zeros of \(F_p\) in
\((-T_j^4,0)\), and

\[
\operatorname{sign}F_p(-T_j^4)=(-1)^j. \tag{3.28}
\]

This is an exact root count, not merely the existence of \(j\) negative roots.

## 4. The two endpoint limits

Let \(c_0=\lceil n/4\rceil\), \(b=4c_0-n\in\{0,1,2,3\}\), and
\(D=n-c_0\).

### Lemma 4.1 (small-root limit)

If \(p^{(n)}=(m_1/n,m_2/n,\ldots)\), padded by zeros and ordered decreasingly,
then, uniformly over all allowed partitions,

\[
H_{\mathbf m}(z/n^4)-F_{p^{(n)}}(z)\longrightarrow0 \tag{4.1}
\]

on every compact subset of \(\mathbb C\).

#### Proof

For fixed \(k\), the leading \(0/1\) contribution counts allocations of \(4k\)
distinct elements with no block used more than \(2k\) times.  Sampling with
replacement differs from sampling distinct elements with probability
\(O_k(n^{-1})\), uniformly in the partition.  Contributions supported on at most
\(4k-1\) elements are \(O_k(n^{4k-1})\).  The lower Ehrhart-to-\(h^*\)
convolution terms disappear after normalization, while nonnegativity and removal of
all constraints gives a common factorial majorant.  Coefficientwise convergence
therefore upgrades to (4.1).  \(\square\)

Fix a sufficiently large \(J\).  For each parameter \(p\), isolate the first
\(J\) simple roots from (3.28) by disjoint conjugation-invariant circles and
choose an outer circle on which \(F_p\) is nonzero.  Compact convergence and
simple-root continuity preserve these circles on a neighborhood of \(p\).
Finitely many such neighborhoods cover the compact space
\(\mathcal P_\alpha^*\).  Applying (4.1) and Rouché's theorem on each member of
this finite cover shows that, for all sufficiently large \(n\),
\(H_{\mathbf m}\) has exactly \(J\) roots in the corresponding scaled initial
region.  Conjugation symmetry and the parameter-local isolated real roots force
the actual roots to be simple and negative.  A single outer circle, obtained
from the uniform far-right bound (3.26), gives the common root count and the
fixed initial grid point inherits the sign \((-1)^J\).

### Lemma 4.2 (reciprocal endpoint)

Define

\[
Q_n(z)=n^{-b}(z/n^4)^D H_{\mathbf m}(n^4/z).
\]

Uniformly over all allowed partitions,

\[
Q_n(z)\longrightarrow V_{4,b}(z):=
\sum_{k\ge0}\frac{z^k}{(4k+b)!} \tag{4.2}
\]

on compact subsets of \(\mathbb C\).  Each \(V_{4,b}\) has infinitely many
simple, strictly negative zeros.  This is the residue function \(E_b\) of
Adiprasito--Zhang [7, Section 3.3], with \(k=4\); its zero property is prior
work.  The uniform convergence over capacity-two partitions is the assertion
needed here.  The multiplier-sequence argument below records an alternative
derivation of the known zero property, not a novelty claim.

#### Proof

At dilation \(c_0+k\), subtract one from every interior coordinate.  For fixed
\(k\), the residual total is \(b+4k\), whereas every coordinate cap and every
block cap tends uniformly to infinity because \(\max_i m_i\le\alpha n\) with
\(\alpha<1/2\).  Thus the interior lattice-point count is exactly
\(\binom{n+b+4k-1}{b+4k}\) for all sufficiently large \(n\), uniformly in the
partition.  Ehrhart reciprocity and a factorial majorant give (4.2).

The gamma multiplication formula writes

\[
V_{4,b}(z)=\frac1{b!}\sum_{k\ge0}
\frac{(z/256)^k}
{k!\prod_{\gamma\in A_b}(\gamma)_k},\qquad
A_b=\left\{\frac{b+1}4,\frac{b+2}4,\frac{b+3}4,\frac{b+4}4\right\}
\setminus\{1\}. \tag{4.3}
\]

Every remaining parameter is positive, and the reciprocal Pochhammer sequences
are classical nonnegative multiplier sequences.  Hence \(V_{4,b}\) belongs to
the Laguerre--Pólya class.  To exclude multiplicities, retain one factor
\(1/(\gamma)_k\) until last and shift it to \(1/(\gamma+m)_k\).
Reversing that shift applies successively the positive Euler operators
\(1+\vartheta/(\gamma+r)\), each of which reduces the multiplicity of every
nonzero old root by one.  The shifted inputs converge locally to a positive
constant as \(m\to\infty\), so a fixed multiple root is impossible.  The
positive constant term excludes the origin.

The signs and counts used below are exact.  Put

\[
T_{k,b}=\sqrt2\pi(k+b/4).
\]

Apply the four-root-of-unity filter on the sector
\(0\le\arg w\le\pi/4\) and write

\[
 W(w):=4e^{-w}w^bV_{4,b}(w^4)=1+\lambda(w)+E(w),
\]

where

\[
 \lambda(w)=e^{2ib\pi/4}e^{w(e^{-i\pi/2}-1)}
\]

and the two remaining root-of-unity terms form
\(E(w)=O(e^{-cT_{k,b}})\), uniformly on the half-sector.  Put
\(w=T_{k,b}e^{i\psi}\) and \(\delta=\pi/4-\psi\).  Then

\[
 |\lambda|=e^{-\sqrt2T_{k,b}\sin\delta},\qquad
 \arg\lambda=-2k\pi+\sqrt2T_{k,b}(1-\cos\delta).
\]

When \(\delta\le T_{k,b}^{-2/3}\), the angle between \(1\) and
\(\lambda\) tends uniformly to zero; on the complementary interval
\(|\lambda|\) is exponentially small.  Hence, for all sufficiently large
\(k\), \(\Re W>1/2\) on the entire half-sector.  In particular the boundary
has no zero and the continuous argument of \(W\) returns to zero at the two
endpoints.  The factor \(4e^{-w}w^b\) contributes exactly \(-k\pi\) on the
upper semicircle, so \(V_{4,b}(w^4)\) contributes \(k\pi\); conjugation gives
the same increment below.  The argument principle therefore gives

\[
\#\{z:V_{4,b}(z)=0,\ |z|<T_{k,b}^4\}=k,\qquad
\operatorname{sign}V_{4,b}(-T_{k,b}^4)=(-1)^k. \tag{4.4}
\]

At \(w=T_{k,b}e^{i\pi/4}\), both endpoint factors are real, and the same
continuous-argument computation gives the sign in (4.4).  The four values of
\(b\) have a common lower bound on \(k\).  \(\square\)

For each fixed \(K\) beyond this common bound, the relation
\[
\phi(t)=\frac{3\pi}{4}-\frac1{\sqrt2\,t}+O(t^{-2})
\]
implies \(n/t_{n,D-K}\to T_{K,b}\).  Compact convergence in (4.2) on
the corresponding moving outer circle and (4.4) therefore transfer exactly
\(K\) roots to the reciprocal end of \(H_{\mathbf m}\), again simple and
negative.  At the terminal grid point,
\[
\operatorname{sign}H_{\mathbf m}(-t_{n,D-K}^4)=(-1)^{D-K}. \tag{4.5}
\]

The two lemmas give fixed, uniform numbers of simple negative roots near the two
ends of the negative axis.  It remains to fill the moving middle without losing
uniformity when \(q\) grows.

## 5. A block-count-free moving-cap estimate

Put \(x=-t^4\), \(A=1+t^4\), and let
\(W_{n-1}^{(2,2)}(u,x)\) denote the two-marker transfer polynomial arising from
one active block cap in (2.6).  For a block of size \(h\), its cumulative cap term
is

\[
K_h=\frac1{2\pi i}\int_{|u|=\rho}
W_{n-1}^{(2,2)}(u,-t^4)\frac{u^{-h}}{1-u}\,du. \tag{5.1}
\]

### Lemma 5.1 (uniform moving caps)

For every fixed \(\alpha<1/2\), every partition with
\(\sum_i h_i=n\) and \(1\le h_i\le\alpha n\), and every sequence
\(t\to0\) with \(T=nt\to\infty\),

\[
\frac{\sum_i|K_{h_i}|}{R_4(t)^n}\longrightarrow0, \tag{5.2}
\]

where \(R_4(t)\) is the dominant four-color spectral radius.

#### Proof

The integrals of \(W/(1-u)\) and of the zero-jump term
\(A^nu^{n-1}/(1-u)\) vanish.  Therefore

\[
K_h=\frac1{2\pi i}\int
(W-A^nu^{n-1})\frac{u^{-h}-1}{1-u}\,du. \tag{5.3}
\]

With \(\rho=e^{-\eta t}\),

\[
\sum_i\left|\frac{u^{-h_i}-1}{1-u}\right|
\le n\rho^{-\alpha n}. \tag{5.4}
\]

On the near arc \(|\arg u|\le Lt\), the Schur expansion gives

\[
\frac{|W-A^nu^{n-1}|}{R_4^n}
\le C_L(1+T)^3e^{-\beta\eta T}+Ce^{-c_\star T}, \tag{5.5}
\]

for \(\alpha<\beta<1/2\), where one may take the fixed spectral-gap constant
\(c_\star=1/(4\sqrt2)\).  Equations (5.4)--(5.5) are exponentially small after
integration.

On the complementary arc, the two spectral branches solve

\[
(\lambda-A)(\lambda-Au)=z\lambda^2,
\qquad z=it^2\ \text{or}\ -it^2. \tag{5.6}
\]

They are analytic about \(z=0\).  Taylor expansion of the paired values at
\(\pm it^2\) cancels the linear term.  Uniform implicit-derivative bounds give

\[
\frac{|W-A^nu^{n-1}|}{R_4^n}
\le Ct^4(\delta^{-4}+n\delta^{-3}+n^2\delta^{-2})e^{-c_\star T},
\quad \delta=|1-u|. \tag{5.7}
\]

After (5.4) and integration, the far contribution is at most

\[
C_L(T+T^2+T^3)e^{-(c_\star-\eta\alpha)T}.
\]

Choose \(\eta\alpha<c_\star\).  This proves (5.2).  The cancellation between the
two signs in (5.6), together with \(\sum_i h_i=n\), is what removes any factor
depending on the number of blocks.  \(\square\)

## 6. Uniform signs on the complete root grid

Let

\[
\mu(t)=\frac{1+t^4}{1-te^{\pi i/4}}
=R_4(t)e^{i\phi(t)}.
\]

The phase \(\phi\) increases strictly from \(0\) to \(3\pi/4\).  Define the
grid \(t_{n,j}>0\) by

\[
n\phi(t_{n,j})=j\pi. \tag{6.1}
\]

The two-branch phase grid and its assembly with direct and reciprocal
endpoints follow the ordinary-hypersimplex architecture of [7, Sections
3.4--3.5].  The partition corrections, cancellation uniform in the number
of blocks, and compactification with dust provide the additional controls
for the present family.

### Proposition 6.1 (middle-grid signs)

For every fixed \(\alpha<1/2\), there are fixed integers \(J,K\) and a common
threshold such that, for all allowed partitions and
\(J\le j\le D-K\), the signed values of
\(H_{\mathbf m}(-t_{n,j}^4)/R_4(t_{n,j})^n\) alternate with \(j\) and are
nonzero.

#### Proof

Use (2.6) and split any hypothetical failure sequence according to the limit of
\(t_{n,j}\).

On a fixed compact subinterval of \((0,\infty)\), the four-color term has a
uniform spectral gap.  Each highest cap is exponentially small; summing at most
\(n\) of them is harmless.  The lower color levels carry the multiplicities
\(e_s(\mathbf m)\le n^s/s!\), \(s=1,2,3\), and within each \(C_S\)
there are at most \(q\le n\) single-cap corrections.  Thus their total
prefactor is at worst \(O(n^4)\), which is still absorbed by the uniform
spectral gap.

If \(t\to\infty\) while \(n/t\to\infty\), the same transfer spectrum gives the
large-end moving estimate; polynomial factors from the first three color levels
are absorbed by the exponential gap.  If \(t\to0\) while \(nt\to\infty\), the
highest caps are controlled by Lemma 5.1, the lower levels by
\(C T^s e^{-cT}\), and the three-color term by
\(CT^3t^9e^{-cT}\).  In all three moving regimes, the normalized signed value
tends to \(1/2\).

The remaining possibilities have bounded initial index or bounded terminal index.
They are excluded respectively by Lemma 4.1 together with Theorem 3.1, and by
Lemma 4.2.  Compactness of \(\mathcal P_\alpha^*\) allows passage to a convergent
subsequence even when the number of blocks diverges or mass turns into dust.  The
fixed endpoint values need only retain the nonzero signs supplied by their kernels;
they are not asserted to converge to \(1/2\).  This exhausts every failure
sequence.  \(\square\)

## 7. Proof of Theorem 1.1

Choose \(J,K\) large enough that the two endpoint kernels give, uniformly over
\(\mathcal P_\alpha^*\), exactly \(J\) simple negative roots at the small-root
end and exactly \(K\) simple negative roots at the reciprocal end.  Increase the
common threshold so that Proposition 6.1 applies.

The consecutive grid signs in the middle yield \(D-J-K\) distinct negative roots.
Together with the endpoint roots this gives

\[
J+(D-J-K)+K=D
\]

distinct negative roots.  Lemma 2.1 says that \(H_{\mathbf m}\) has degree
exactly \(D\); hence these roots exhaust the full complex zero set and all are
simple.  \(\square\)

## 8. Reproducibility

The frozen prewrite proof package consists of 37 source and certificate files.  Its
path-and-SHA-256 manifest is

`loops/NONPAVING-HSTAR-PUBLICATION-PREP-0001/A1-证明依赖闭包.sha256`.

The finite scalar certificates supporting the gate (3.8) are checked in exact
rational arithmetic.  One closes the 2028 large-index pairs
\(N=4,8,\ldots,156\), together with the three continuous Bernstein
certificates in (3.20b); the other closes 2403 interval boxes and the 2646
small-order prefix pairs.  The public package, if released, must use the
non-optimized project interpreter because the checkers deliberately use
assertions, and must include hard input-size gates and the frozen certificate
digests.  These finite calculations close stated finite complements inside a
general proof; they are not empirical evidence for Theorem 1.1.

## 9. Prior work and limitations

Lam--Postnikov weighted multi-hypersimplices, elementary split matroids, cuspidal
matroids, and subsequent multi-hypersimplex formulas supply object descriptions and
Ehrhart-counting precedents.  We do not claim these as new.  The sufficient
conditions stated in Li's arXiv v1 for zonotopal and saturated settings do not,
as currently stated, automatically cover all polytopes in (1.1), and they do not
give the simple-root conclusion used here.

Adiprasito and Zhang [7, Theorem 3.1] prove eventual simple negative
real-rootedness for ordinary hypersimplices of each fixed rank \(k\ge3\).
Its \(k=4\) specialization includes the uniform degeneration of our family.
We checked the full text of HAL version v1: it contains no weighted
multi-hypersimplex or general perturbation theorem covering the nonuniform
partitions of Theorem 1.1.  The increment relative to that rank-four
specialization is the common threshold over all capacity-two partitions of
bounded maximum block ratio.  This does not assert a theorem for other
ranks, or establish global priority over all other or unindexed work.
The residue-function and phase-grid prototypes in its Sections 3.3--3.5
are explicitly treated as prior mechanisms, not as new results here.

The following are not proved here:

- the critical boundary \(\max_i m_i=n/2\);
- a common theorem for every small \(n\);
- an explicit or \(\alpha\)-uniform threshold;
- other ranks, block capacities, or arbitrary nonpaving matroids;
- any global priority claim.

## References

1. T. Lam and A. Postnikov, *Alcoved polytopes I*, Discrete & Computational
   Geometry 38 (2007), 453--478.
2. K. Bérczi, T. Király, T. Schwarcz, Y. Yamaguchi, and Y. Yokoi,
   *Hypergraph characterization of split matroids*, 2022 preprint.
3. L. Ferroni and B. Schröter, *Valuative invariants for large classes of
   matroids*, 2022 preprint, revised 2024.
4. J. McGinnis, *Ehrhart theory of panhandle matroids and related
   multi-hypersimplices*, 2023 preprint.
5. G.-N. Han and M. Josuat-Vergès, *Flag statistics from the Ehrhart
   \(h^*\)-polynomial of multi-hypersimplices*, Electronic Journal of
   Combinatorics 23 (2016), Paper 1.55.
6. S. Li, *Real-rootedness from zonotopal positivity*, arXiv:2609.24917v1,
   2026.
7. K. Adiprasito and M. Zhang, *Eventual unimodality of the hypersimplex*,
   HAL preprint hal-05747878v1, submitted 12 September 2026;
   Theorem 3.1 and Sections 3.3--3.5.

## AI-assisted research disclosure

The research, proof development, checking, and writing were conducted with
substantial AI assistance.  Carptopus is the human author and assumes responsibility
for the mathematical claims and any released version.
