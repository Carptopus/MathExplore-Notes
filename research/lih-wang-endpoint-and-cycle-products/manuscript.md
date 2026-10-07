# Endpoint permanent gates and cycle-forest families for the Lih--Wang chord inequality

Carptopus

Draft date: 2026-10-07  
Status: internal technical draft; not peer reviewed

## Abstract

Let \(J_n\) be the \(n\times n\) matrix whose entries are \(1/n\).  The Lih--Wang
inequality asks whether

\[
\operatorname{per}(tJ_n+(1-t)A)
\le t\operatorname{per}(J_n)+(1-t)\operatorname{per}(A),
\qquad \tfrac12\le t\le1,
\]

holds for every doubly stochastic matrix \(A\).  We prove a sufficient endpoint
criterion which applies to the larger class of nonnegative row-stochastic matrices:
if

\[
\operatorname{per}(A)\ge 2^{2-n},
\]

then the inequality holds throughout the indicated half interval.  The proof combines
a universal one-collision rook envelope, an analytic estimate for \(n\ge32\), and an
exact rational Bernstein certificate for \(2\le n\le31\).

The criterion yields a direct-sum theorem requiring only permanent lower bounds on
the blocks.  We then study matrices obtained by placing weighted directed cycles on a
cycle--element incidence forest.  Entropy gives the required endpoint bound whenever
there are at least two components (counting fixed points).  For a connected incidence
tree we prove the inequality for all \(n\ge64\) by a one-hot negative-dependence
comparison and an exponential lower-tail estimate.  Together with exact results for
single cycles and shared-center cycle families, this gives a unified theorem for a
natural collection of cycle products and cycle forests.  The result does not settle
the full Lih--Wang conjecture, and no optimality claim is made for the endpoint
threshold.

## 1. Introduction

For an \(n\times n\) matrix \(A=(a_{ij})\), write

\[
\operatorname{per}(A)=\sum_{\sigma\in S_n}\prod_{i=1}^n a_{i,\sigma(i)}.
\]

Let \(\Omega_n\) denote the set of doubly stochastic matrices and let
\(J_n=\mathbf1\mathbf1^{\mathsf T}/n\).  Lih and Wang asked whether, for every
\(A\in\Omega_n\),

\[
\operatorname{per}(tJ_n+(1-t)A)
\le t\frac{n!}{n^n}+(1-t)\operatorname{per}(A),
\qquad \tfrac12\le t\le1. \tag{1.1}
\]

The conjecture was proved by Lih and Wang in order three.  Subsequent work contains
several low-order and structurally restricted results.  In particular, the complete
order-four doubly stochastic case and a conditional order-six range appear in the
published work of Divya K. U. and Somasundaram.  Star-matrix results of Arulraj and
Somasundaram and of Divya and Somasundaram cover certain direct sums of \(2\times2\)
blocks, under hypotheses on the comparison matrix and the block parameters.

The present paper develops a different sufficient mechanism.  We fix the comparison
matrix \(J_n\), retain only the half interval in (1.1), allow \(A\) to be merely
row-stochastic, and impose one scalar condition on its permanent.  The main endpoint
gate is the following.

### Theorem 1.1 (endpoint permanent gate)

Let \(n\ge2\), and let \(A\) be a nonnegative row-stochastic \(n\times n\) matrix.  If

\[
p:=\operatorname{per}(A)\ge 2^{2-n}, \tag{1.2}
\]

then, for every \(0\le u\le1/2\),

\[
\operatorname{per}(uA+(1-u)J_n)
\le (1-u)\frac{n!}{n^n}+u\operatorname{per}(A). \tag{1.3}
\]

Here \(u=1-t\), so (1.3) is (1.1) on the original half interval.  The theorem does
not assert that (1.2) is necessary or optimal.

The block consequence is deliberately weaker than a star-matrix theorem: the
comparison endpoint is fixed to \(J_n\), and only the half interval is considered.

### Corollary 1.2 (endpoint-controlled direct sums)

Let

\[
A=I_f\oplus A_1\oplus\cdots\oplus A_b,
\]

where \(A_j\) is a nonnegative row-stochastic matrix of order \(n_j\),
\(\operatorname{per}(A_j)\ge2^{1-n_j}\), and \(b+f\ge2\).  Then \(A\)
satisfies (1.3) for all \(0\le u\le1/2\).

We next turn to cycle-supported matrices.  Let \(C_i\) be directed cycle
permutation matrices, of lengths at least two, and let

\[
A=I+\sum_i a_i(C_i-I), \qquad a_i\ge0. \tag{1.4}
\]

At every element we require the sum of weights of incident cycles to be at most one;
this ensures nonnegativity and row stochasticity.  Form the bipartite incidence graph
whose vertices are the cycles and the underlying elements and whose edges record
membership.  Our broad structural result is as follows.

### Theorem 1.3 (cycle-forest range)

Assume that the cycle--element incidence graph in (1.4) is a forest.  Let \(c\) be
the number of its connected components containing a cycle, and let \(f\) be the number
of additional fixed points.  Then (1.3) holds in each of the following cases:

1. \(c+f\ge2\), for every \(n\);
2. \(n\ge64\), with no restriction on \(c+f\);
3. in the remaining connected range \(c=1,f=0,n<64\), when there is a single cycle,
   or when all cycles share one center and their remaining supports are pairwise
   disjoint.

The theorem does not include incidence graphs containing cycles, and it leaves open
connected multi-center forests of order below \(64\).

Two component theorems used in case 3 are of independent structural interest.  One
allows pairwise disjoint cycle blocks with independent parameters; the other allows
an arbitrary number of cycles sharing one center.

The contribution boundary is important.  Orders three and four have prior general
doubly stochastic coverage, and parts of the \(2\times2\)-block domain overlap
conditional star-matrix results.  We make no global-first or strict-extension claim.
Our precise literature statement is only that, among the original sources examined,
we did not find the combination of the row-stochastic endpoint gate and the full
cycle-forest ranges stated above.  Several older papers are available to us only
through publisher abstracts and reliable later restatements; Section 7 records this
limitation.

## 2. Rook polynomials and the \(J_n\)-mixture

Let the rows of a nonnegative row-stochastic matrix \(A\) choose columns independently,
with row \(r\) choosing \(v\) with probability \(a_{rv}\).  Write \(N_v\) for the
occupancy of column \(v\), and define the rook polynomial

\[
R_A(z)=\mathbb E\prod_{v=1}^n(1+N_vz)=\sum_{k=0}^n h_kz^k. \tag{2.1}
\]

The coefficient \(h_k\) is the sum of the permanents of all \(k\times k\) submatrices
obtained by choosing \(k\) rows and \(k\) columns.  Expanding the permanent according
to which rows use \(A\) and which use \(J_n\) gives

\[
\operatorname{per}(uA+(1-u)J_n)
=\sum_{k=0}^n u^k(1-u)^{n-k}\frac{(n-k)!}{n^{n-k}}h_k. \tag{2.2}
\]

It is useful to introduce the positive linear functional

\[
\Phi(P)=2^{-n}\sum_{k=0}^n[z^k]P(z)\frac{(n-k)!}{n^{n-k}}. \tag{2.3}
\]

Thus \(\Phi(R_A)=\operatorname{per}((A+J_n)/2)\).  Put

\[
B=1+z,\qquad F_1=(1+2z)B^{n-2},\qquad
c_n=\frac{n!}{n^n},\qquad z_n=2^{1-n}. \tag{2.4}
\]

### Lemma 2.1 (universal one-collision envelope)

If \(p=\operatorname{per}(A)\), then

\[
R_A(z)\preceq pB^n+(1-p)F_1, \tag{2.5}
\]

where \(P\preceq Q\) means coefficientwise domination.

#### Proof

The event that all column occupancies are at most one has probability \(p\), and on
that event \(\prod_v(1+N_vz)=B^n\).  On every remaining outcome, the occupancy vector
has total sum \(n\), at most \(n-1\) occupied columns, and at least one collision.
Among such integer occupancy vectors, every elementary symmetric sum is maximized by
\((2,1,\ldots,1,0)\).  Its generating polynomial is \(F_1\).  Averaging gives (2.5).
\(\square\)

The next lemma is the exact bridge from a midpoint estimate to the full half
interval.

### Lemma 2.2 (midpoint equivalence for large order)

Let \(n\ge32\), let \(A\) be nonnegative and row stochastic, and assume
\(p=\operatorname{per}(A)\ge z_n\).  Then (1.3) holds for every
\(0\le u\le1/2\) if and only if it holds at \(u=1/2\).

#### Proof

Define

\[
\beta_k=\frac{(n-k)!h_k}{n^{n-k}\binom nk},\qquad
\gamma_j=2^{-j}\sum_{k=0}^j\binom jk\beta_k. \tag{2.6}
\]

For every choice of \(k\) rows, the probability that their independently
selected columns are distinct is at most one.  Hence
\(h_k\le\binom nk\), and therefore
\(\gamma_j(A)\le\gamma_j(I_n)\).  If
\(\Phi_I=\operatorname{per}((I_n+J_n)/2)\), direct summation gives

\[
\gamma_{n-1}(I_n)=z_n,\qquad
\gamma_{n-2}(I_n)=g_n:=\frac4{n-1}(\Phi_I-z_n). \tag{2.7}
\]

The sequence \(j\mapsto\gamma_j(I_n)\) is convex on
\(0\le j\le n-2\).  Indeed, if \(T\) has the
\(\operatorname{Gamma}(n+1,1)\) law, then

\[
\gamma_j(I_n)=c_n\,\mathbb E\left[\left(\frac{1+n/T}{2}\right)^j\right],
\]

and its second discrete difference is the expectation of a nonnegative
quantity.  Moreover

\[
2^n\Phi_I\le2+\sqrt{\pi n/2}
\]

To see the displayed bound on \(\Phi_I\), write its \(d\)-th summand as
\(\prod_{h=0}^{d-1}(1-h/n)\).  For \(d\ge1\),

\[
 \prod_{h=0}^{d-1}(1-h/n)
 \le \exp\{-d(d-1)/(2n)\}
 \le \exp\{-(d-1)^2/(2n)\}.
\]

The decreasing Gaussian sum is at most its first term plus its integral,
which gives \(2^n\Phi_I\le2+\sqrt{\pi n/2}\).  Substitution in (2.7)
reduces the second assertion below to
\(8\pi n^3\le(n-1)^2(n-2)^2\).  At \(n=32\) this follows from
\(\pi<22/7\), and
\(n(1-1/n)^2(1-2/n)^2\) is increasing for \(n\ge3\).  Hence, for
\(n\ge32\),

\[
 g_n\le\frac{n-2}{2n}z_n. \tag{2.8}
\]

Convexity between \(j=0\) and \(j=n-2\) therefore proves all Bernstein
layers \(0\le j\le n-2\) of the chord inequality.

It remains to control \(j=n-1\).  From the envelope (2.5),
\[
\gamma_{n-1}(A)\le pz_n+(1-p)g_n.
\]
The difference between the target layer and this upper bound is
\[
D(p)=\frac{n+1}{2n}c_n-g_n
+p\left(\frac{n-1}{2n}-z_n+g_n\right).
\]
Its coefficient of \(p\) is positive, and (2.8) gives
\[
D(p)\ge D(z_n)\ge
\frac{n+1}{2n}c_n+\frac{z_n}{2n}\bigl(1-(n+2)z_n\bigr)>0.
\]
Thus the first \(n\) Bernstein layers are automatic.  The top layer is exactly
\[
\gamma_n(A)=\operatorname{per}\left(\frac{A+J_n}{2}\right),
\]
so its inequality is precisely the midpoint inequality.  Positivity of the
degree-\(n\) Bernstein basis on \(0\le2u\le1\) proves sufficiency.
Necessity is immediate by setting \(u=1/2\).  \(\square\)

### Lemma 2.3 (the finite orders)

For \(2\le n\le31\), the envelope (2.5) implies (1.3) whenever
\(p\ge2^{2-n}\).

#### Proof

For a polynomial \(P\), set
\[
\Gamma_j(P)=2^{-j}\sum_{k=0}^j
\frac{\binom jk}{\binom nk}\frac{(n-k)!}{n^{n-k}}[z^k]P. \tag{2.9}
\]
After the substitution \(x=2u\), the degree-\(n\) Bernstein coefficients
reduce to
\[
s_{n,j}=\frac{j}{2n}-\Gamma_j(B^n)+\Gamma_j(F_1)>0, \tag{2.10}
\]
\[
d_{n,j}=\left(1-\frac{j}{2n}\right)c_n
+\frac{j}{2n}2^{2-n}
-\Gamma_j\!\left(2^{2-n}B^n+(1-2^{2-n})F_1\right)>0. \tag{2.11}
\]
The zeroth layer is an equality.  All 495 remaining pairs
\((n,j)\), \(2\le n\le31\), \(1\le j\le n\), were evaluated in exact
rational arithmetic by the frozen endpoint checker.  The certificate digest is
9b857ec7f67ca6319d3cabc31c2b3f8fd88690766b51898ffbb577c155a9107e.

The smallest margin occurs at \((n,j)=(31,1)\) and is
\[
\frac{550476113801152858212168551495168251918862401}
{18327886165296381817380980351835033630345588173537542144}>0.
\]
This certifies a finite symbolic complement, not a sampling of matrices or
parameters.  \(\square\)

## 3. Proof of the endpoint gate

We prove Theorem 1.1.  The finite range \(2\le n\le31\) follows from
Lemma 2.3, since \(p\ge2^{2-n}\).

Now assume \(n\ge32\), and set

\[
\Phi_I=\operatorname{per}\left(\frac{I_n+J_n}{2}\right),
\qquad C_n=2+\sqrt{\frac{\pi n}{2}}. \tag{3.1}
\]

Direct evaluation gives

\[
0\le\Phi(F_1)
=z_n-\frac{\Phi_I-z_n}{n-1}\le z_n,
\qquad \Phi_I\le2^{-n}C_n. \tag{3.2}
\]

The lower inequality \(\Phi_I\ge z_n\) also follows directly from

\[
2^n\Phi_I=\sum_{d=0}^n\prod_{h=0}^{d-1}\left(1-\frac hn\right)\ge2. \tag{3.3}
\]

At \(u=1/2\), subtracting the envelope (2.5) from the chord yields the margin

\[
G(p)=\frac{c_n}{2}-\Phi(F_1)
+p\left(\frac12-\Phi_I+\Phi(F_1)\right). \tag{3.4}
\]

For \(n\ge32\), \(\Phi_I<1/1024\), so \(G\) is increasing in \(p\).  Hence

\[
G(p)\ge G(2z_n)
\ge\frac{c_n}{2}-2z_n\Phi_I
\ge\frac{c_n}{2}-4\cdot4^{-n}C_n. \tag{3.5}
\]

The last quantity is positive.  Indeed, the integral bound
\(\log(n!)\ge n\log n-n+1\) gives \(c_n>3^{-n}\), since \(e<3\).  It is therefore
enough that \((4/3)^n\ge8C_n\).  At \(n=32\), \(C_{32}<10\) and
\((4/3)^{32}>80\); moreover

\[
\frac{C_{n+1}}{C_n}\le\sqrt{\frac{n+1}{n}}<\frac43,
\]

so the inequality persists for all larger \(n\).  Lemma 2.2 now recovers the
entire interval \(0\le u\le1/2\).  This proves Theorem 1.1.  \(\square\)

### Proof of Corollary 1.2

Let \(n=f+\sum_jn_j\).  Multiplicativity of the permanent under direct sums gives

\[
\operatorname{per}(A)=\prod_{j=1}^b\operatorname{per}(A_j)
\ge2^{b+f-n}\ge2^{2-n}.
\]

Apply Theorem 1.1.  Notice that no local chord inequality is assumed for any block.
\(\square\)

## 4. Independent cycle blocks and shared-center families

We record the two low-component inputs used later.

### Theorem 4.1 (independent cycle product)

Let \(C_1,\ldots,C_r\) be pairwise disjoint cycle permutation blocks of
lengths \(\ell_i\ge2\), let \(f\ge0\), and put
\[
n=f+\sum_i\ell_i
\]
and

\[
A=I_f\oplus\bigoplus_{i=1}^r\bigl((1-s_i)I_{\ell_i}+s_iC_i\bigr),
\qquad 0\le s_i\le1.
\]

Then \(A\) satisfies (1.3) for all \(0\le u\le1/2\).

#### Proof

Set \(y_i=(1-2s_i)^2\), and define

\[
c_\ell(v)=2^{1-\ell}\sum_{q=0}^{\lfloor\ell/2\rfloor}\binom\ell{2q}v^q.
\]

The rook polynomial is

\[
R(z;\mathbf y)=(1+z)^n\prod_{i=1}^r
c_{\ell_i}\!\left(\frac{1+2z+y_iz^2}{(1+z)^2}\right). \tag{4.1}
\]

For the coefficient polynomial of \(y^q\) in a single block, write

\[
F_{\ell,q}(z)=[y^q](1+z)^\ell
c_\ell\!\left(\frac{1+2z+yz^2}{(1+z)^2}\right),
\qquad a_{\ell,q}=[z^\ell]F_{\ell,q}.
\]

Define \(H_0=1\) and \(H_m=F_{m,0}/2^{1-m}\) for \(m\ge1\).  If

\[
X=1+z+\sqrt{1+2z},\qquad Y=1+z-\sqrt{1+2z},
\]

then \(XY=z^2\) and \(H_m=(X^m+Y^m)/2\).  Consequently

\[
H_aH_b=\frac12\left(H_{a+b}+z^{2b}H_{a-b}\right)\preceq H_{a+b}
\qquad(a\ge b), \tag{4.2}
\]

and

\[
[z^{m-d}]H_m=2^d\frac{m}{m+d}\binom{m+d}{2d}. \tag{4.3}
\]

For \(q\ge1\), a nonnegative Taylor expansion gives

\[
\frac{F_{\ell,q}}{a_{\ell,q}}
\preceq z^{2q}H_{\ell-2q}\preceq z^2H_{\ell-2}\preceq H_\ell. \tag{4.4}
\]

Combining (4.2)--(4.4), every nonconstant monomial
\(\mathbf y^\alpha\) in the rook expansion satisfies, for \(1\le d\le n-2\),

\[
\frac{[\mathbf y^\alpha]h_{n-d}}
{[\mathbf y^\alpha]h_n}
\le 2^d\frac{n-2}{n-2+d}\binom{n-2+d}{2d}
\le\frac{n-d}{n}\frac{n^d\binom nd}{d!}. \tag{4.5}
\]

The last inequality follows after taking the ratio of the two sides and using the
central-binomial estimate
\(\binom{2d}{d}/2^d\ge2^d/(2d+1)\), with \(d=1,2,3,4,5\) checked directly and
monotonicity thereafter.

Equation (4.5), inserted into (2.2), gives for every \(\alpha\ne0\)

\[
[\mathbf y^\alpha]\operatorname{per}(uA+(1-u)J_n)
\le u[\mathbf y^\alpha]\operatorname{per}(A). \tag{4.6}
\]

It remains to justify the constant monomial.  We record the required
common-parameter theorem rather than treating it as a black box.  If
\(P,Q\) are permutation matrices and
\(A_s=(1-s)P+sQ\), then \(A_s\) satisfies (1.3).  After multiplying by
permutation matrices, take \(P=I\), and write the nontrivial cycles of
\(Q\) as lengths \(a_1,\ldots,a_r\).  For
\[
c_m(v)=2^{1-m}\sum_q\binom m{2q}v^q
\]
we first prove the one-cycle base used by the induction.  Suppose that \(Q\)
has one nontrivial cycle of length \(\ell\ge2\), all other points are fixed,
and \(A_s=(1-s)I+sQ\).  Set \(y=(1-2s)^2\), expand the rook
coefficients as \(h_k(y)=\sum_qh_{k,q}y^q\), and put

\[
 \beta_{k,q}=\frac{(n-k)!h_{k,q}}
 {n^{n-k}\binom nk},\qquad p=h_{n,0}=2^{1-\ell}.
\]

The case \(n=2\) is separate: then \(\ell=2\),
\(c_2(y)=(1+y)/2\), and
\[
 (B_0,B_1,B_2)=\left(\frac12,\frac12,c_2(y)\right),
 \qquad
 \Phi_2=\frac12+\frac y2u^2
 \le \frac12+\frac y2u
 \quad(0\le u\le1).
\]
Thus both the chord inequality and the auxiliary coefficient bound hold in
dimension two.  In the rest of the one-cycle argument assume \(n\ge3\).

The Bernstein transform in (2.6) shows that it is enough to prove

\[
 \beta_{k,q}\le\frac{k}{n}h_{n,q}\quad(q\ge1),
 \qquad
 \beta_{k,0}\le c_n+(p-c_n)
 \frac{k(k-1)}{(n-1)(n-2)}. \tag{4.7}
\]

For the first inequality begin with the full cycle \(\ell=n\).  If
\(N=n-2q\), \(a_r=h_{2q+r,q}\), and \(A_0=2n-2q-1\),
two Chu--Vandermonde sums give

\[
 \frac{a_{r+1}}{a_r}
 =\frac{N-r}{r+1}\frac{A_0-2r}{A_0-r}.
\]

Thus, with \(d=n-k\) and
\(T_d=\beta_{n-d,q}/h_{n,q}\),

\[
 \frac{T_d}{T_{d-1}}
 =\frac{d(N-d+1)(n+d-1)}
 {n(n-d+1)(2q+2d-1)}
 \le\frac{n-d}{n-d+1}.
\]

Indeed, \(N-d+1\le n-d\) and
\(d(n+d-1)\le n(2q+2d-1)\).  Since \(T_0=1\), induction proves
the first inequality in (4.7).  Adding one fixed point multiplies the rook
polynomial by \(1+z\); if \(B_{n,D,q}=\beta_{n-D,q}\), then

\[
 B_{n+1,D,q}=\frac{D^2n^{D-1}}{(n+1)^{D+1}}B_{n,D-1,q}
 +\frac{n+1-D}{n+1}\left(\frac n{n+1}\right)^D B_{n,D,q}.
\]

Substitution of the already proved bounds leaves
\(n^2((n+1)^D-n^D)+D(n-D)n^D\ge0\), so the first inequality
persists with any number of fixed points.

For the constant term in the full-cycle case, write
\(\rho=2^{n-1}c_n\), \(R_d=\beta_{n-d,0}/p\), and

\[
 Q_d=\rho+(1-\rho)
 \frac{(n-d)(n-d-1)}{(n-1)(n-2)}.
\]

The even-cycle matching formula gives

\[
 R_d=\frac{2^dn(d!)^2(n+d-1)!}{n^dn!(2d)!},
 \qquad
 \frac{R_{d+1}}{R_d}=\frac{(d+1)(n+d)}{n(2d+1)}.
\]

After clearing positive denominators, the comparison with
\(Q_{d+1}/Q_d\) has the sign of

\[
 E_d=(1-\rho)[-d^3+(2n-1)d^2+2n]
 +d[-n^2+5n-\rho(2n+2)].
\]

The bounds \(\rho\le4(n-1)/n^2\) for \(n\ge3\) and
\(\rho<3n/(n^2+2)\) for \(n\ge7\) show that \(E_d\) first decreases
and then increases, with \(E_1\le0\) and \(E_{n-2}\ge0\); the cases
\(3\le n\le6\) follow by direct substitution.  Starting from
\(R_1=Q_1=1\) before the sign change and from
\(R_{n-1}=Q_{n-1}=\rho\) after it proves \(R_d\le Q_d\).

The fixed-point recurrence reduces the remaining comparison to an affine
function of \(c_n/p\in[0,1]\).  At its two endpoints it is respectively

\[
 (n+1)^{D+1}(n-2)
 \ge n^D[n(n-1)-D(n-D)]
\]

and

\[
 L+\left(\frac n{n+1}\right)^n(1-L)
 \ge\left(\frac n{n+1}\right)^D H,
\]

where \(L=(n+1-D)(n-D)/(n(n-1))\) and
\(H=(n(n+1-D)+D^2)/(n(n+1))\).  Bernoulli's inequality proves both.
This establishes the second inequality in (4.7), including \(\ell=2\)
after the direct \(n=3\) base case.  Averaging (4.7) against the binomial
weights in (2.6) proves the chord inequality for one cycle and arbitrary
fixed points.

We now merge cycles.  For \(a\ge b\ge2\),
\[
c_a(v)c_b(v)=c_{a+b}(v)+\lambda_b(1-v)^bd_{a,b}(v), \tag{4.7a}
\]
where
\[
(\lambda_b,d_{a,b})=
\begin{cases}
(4^{-b},c_{a-b}),&a>b,\\
(2\cdot4^{-b},1),&a=b.
\end{cases}
\]
The first term has one fewer cycle.  For the second, if \(D\) is the
lower-dimensional remaining cycle polynomial and \(m=n-2b\), the rook
polynomial satisfies
\[
R_{(1-v)^bD}^{(n)}(z,y)
=(1-y)^bz^{2b}R_D^{(m)}(z,y). \tag{4.7b}
\]
Here, for a cycle polynomial \(F\) in dimension \(N\), write
\[
 R_F^{(N)}(z,y)=\sum_{k=0}^Nh_k(y)z^k,
 \qquad
 B_k^{(N)}(F;y)=
 \frac{(N-k)!h_k(y)}{N^{N-k}\binom Nk},
\]
and
\[
 \Phi_N(F;u,y)=\sum_{k=0}^N\binom Nk
 B_k^{(N)}(F;y)u^k(1-u)^{N-k}.
\]
If \(m=0\), (4.7b) gives
\(R_{(1-v)^b}^{(2b)}=(1-y)^bz^{2b}\); hence every coefficient below
degree \(2b\) vanishes, the top coefficient is \((1-y)^b\), and
\[
 \Phi_{2b}((1-v)^b;u,y)=u^{2b}(1-y)^b
 \le u(1-y)^b.
\]
This proves both required properties directly.  Assume henceforth that
\(m\ge1\).  For \(k=2b+r\), (4.7b) also gives the exact lift
\[
 B_{2b+r}^{(n)}((1-v)^bD;y)
 =(1-y)^b B_r^{(m)}(D;y)
 \left(\frac mn\right)^{m-r}
 \frac{\binom mr}{\binom n{2b+r}}, \tag{4.7c}
\]
while the left side is zero for \(k<2b\).  The product of the last two
factors is at most one because
\(\binom mr=\binom m{m-r}\le\binom n{m-r}=\binom n{2b+r}\).
Consequently the lower-dimensional bound
\(B_r^{(m)}(D;y)\le D(y)\) lifts to the corresponding bound in dimension
\(n\).

For the chord property, the case \(u=0\) is immediate.  For \(u>0\), write
\(\rho=u+m(1-u)/n\) and \(v=u/\rho\).  Termwise substitution in the
Bernstein sum gives
\[
\Phi_n((1-y)^bD;u,y)
=(1-y)^bu^{2b}\rho^m\Phi_m(D;v,y). \tag{4.7d}
\]
The simultaneously maintained coefficient bound makes
\(\Phi_m(D;v,y)\) a Bernstein convex combination bounded by \(D(y)\) for
all \(0\le v\le1\), and
\(u^{2b}\rho^m\le u\) for \(0\le u\le1/2\).
Equations (4.7a)--(4.7d) therefore merge two cycles while preserving both
the chord inequality and the auxiliary coefficient bound.  The base cases are
the one-cycle result just proved and the identity matrix.  Strong induction on
\(r\) proves the common-parameter theorem.

The coefficient of \(\mathbf y^0\) in the present independent-parameter
problem is exactly that common-parameter case.  Since
\(0\le y_i\le1\), summing it with (4.6) over all nonconstant monomials
completes the proof.  \(\square\)

### Theorem 4.2 (shared-center cycle simplex)

Suppose \(r\ge2\) cycles \(C_i\) of lengths \(\ell_i\ge2\) share
exactly one common center and have pairwise disjoint private supports.  Allow
\(f\ge0\) additional fixed points, put
\[
n=1+f+\sum_i(\ell_i-1),
\]
and assume \(a_i\ge0\) and \(\sum_i a_i\le1\).  If

\[
A=I+\sum_{i=1}^r a_i(C_i-I),
\]

then \(A\) satisfies (1.3) for every \(n\ge3\) and every
\(0\le u\le1/2\).

#### Proof

Put \(m_i=\ell_i-1\), \(M=\sum_i m_i\), \(c=1-\sum_i a_i\), and
\(d_i=1-a_i\).  The only supported permutation terms are
\(I,C_1,\ldots,C_r\), whence
\[
p=\prod_i d_i^{m_i}
\left(c+\sum_i a_i(a_i/d_i)^{m_i}\right). \tag{4.10}
\]
Weighted AM--GM, followed by the binary entropy bound, gives
\[
p\ge\prod_i[a_i^{a_i}d_i^{d_i}]^{m_i}\ge2^{-M}\ge2^{1-n}. \tag{4.11}
\]
Boundary cases in which a displayed quotient is undefined follow by continuity.

We first handle \(n\ge32\).  For the independent row experiment let
\(p\) be the probability of no collision and \(q\) the probability of exactly
one lost occupied column.  Splitting overloaded columns coefficientwise gives
\[
R_A\preceq pB^n+qF_1+(1-p-q)F_2,\qquad
F_2=(1+2z)^2B^{n-4}. \tag{4.12}
\]
Let \(D\) count the double occupancies in private columns.  The conflict graph
of these events is the line graph of a subdivided star.  The weighted tree
determinant therefore factors its probability generating function as
\[
\mathbb Ex^D=\prod_j(1-\lambda_j^2+\lambda_j^2x),\qquad
0\le\lambda_j^2\le1,
\]
and
\[
\mu=\mathbb ED=\sum_i m_i a_i(1-a_i). \tag{4.13}
\]
Consequently, for \(\mu\ge1\),
\[
q\le\Pr(D\le1)\le\mu e^{1-\mu}. \tag{4.14}
\]
If \(p\ge2\Phi_I-c_n\), convexity of the unit-matrix radial permanent
already closes the chord.  Otherwise (4.10), the entropy estimate, and
\(2^n\Phi_I\le C_n=2+\sqrt{\pi n/2}\) give
\[
\mu>\frac{n-1}{4}-\frac12\log C_n.
\]
For \(n\ge32\), (4.14) implies \(q<1/32\).  Exact evaluation of the
positive functional \(\Phi\) gives
\[
0\le\Phi(F_1)\le z_n,\qquad
0\le\Phi(F_2)<\frac7{16}z_n,\qquad
\Phi_I<\frac1{1024}.
\]
The midpoint margin in (4.12) is therefore greater than
\[
z_n\left(\frac12-\frac1{1024}-\frac7{16}-\frac1{32}\right)
=\frac{31}{1024}z_n.
\]
Lemma 2.2 restores the whole half interval.

For \(16\le n\le31\), use the following Bernoulli-splitting lemma.  If
\(X\) is a finite sum of independent Bernoulli variables with
\(\mu=\mathbb EX\ge2\), then

\[
 \Pr(X\le1)\le(1+\mu)e^{-\mu}. \tag{4.14a}
\]

Indeed, replacing a Bernoulli parameter \(t\) by two independent parameters
\(t/2\) changes the tail by
\((t^2/4)(\Pr(Y=1)-\Pr(Y=0))\ge0\).  If \(\Pr(Y=0)>0\), then
\[
 \frac{\Pr(Y=1)}{\Pr(Y=0)}=
 \sum_r\frac{s_r}{1-s_r}\ge\sum_rs_r=\mathbb EY\ge1;
\]
if \(\Pr(Y=0)=0\), the comparison is immediate.  Iterating the split and
passing to the Poisson limit proves
(4.14a).  In the low-permanent region, (4.11) and
\(2^n\Phi_I\le2+\sqrt{\pi n/2}\) imply
\(\mu>11/4\), already at \(n=16\), and hence
\(q\le(1+\mu)e^{-\mu}<1/4\).

For a polynomial \(P\) define

\[
 \Gamma_j(P)=2^{-j}\sum_{k=0}^j
 \frac{\binom jk}{\binom nk}\frac{(n-k)!}{n^{n-k}}[z^k]P.
\]

Applying this positive transform to (4.12), the derivative of the layer
margin with respect to \(p\) is
\(j/(2n)-\Gamma_j(B^n)+\Gamma_j(F_2)>0\): convexity of the unit-matrix
sequence gives \(\Gamma_j(B^n)\le\Phi_I<1/1024\), whereas
\(j/(2n)\ge1/62\).  Thus the worst admissible values are
\(p=z_n\) and \(q=1/4\), and every Bernstein layer reduces to
\[
\left(1-\frac{j}{2n}\right)c_n+\frac{j}{2n}z_n
-\Gamma_j\!\left(z_nB^n+\frac14F_1+
  (3/4-z_n)F_2\right)>0. \tag{4.15}
\]
All 376 rational inequalities (4.15) are verified exactly by the certificate
described in the supplement.

For \(8\le n\le15\), keep the endpoint and collision mean coupled:
\[
p\ge z_n\exp\{(n-1)/2-2\mu\}. \tag{4.16}
\]
An extremal argument for a Bernoulli sum gives, for \(\mu\ge3/2\),
\[
q\le\max\{e^{1-\mu},(1+\mu)e^{-\mu}\}. \tag{4.17}
\]

To prove this bound, maximize \(\Pr(X\le1)\) on the closed fixed-mean
cube section and choose a maximizer with the fewest interior coordinates.
Varying two such coordinates at fixed sum shows that all remaining interior
coordinates are equal; the others are zero or one.  One deterministic one
gives \(e^{1-\mu}\).  With no deterministic one, the equal-parameter
tail is
\[
 f_N=(1-\mu/N)^{N-1}(1+\mu-\mu/N).
\]
For \(\mu<N\), the negative power series for \(\log(1-x)\) gives
\[
 \log\frac{f_N}{(1+\mu)e^{-\mu}}
 \le\frac{\mu^2}{N}\left[
 \frac1{1+\mu}-\frac{N-1}{2N}
 -\frac{(N-1)\mu}{3N^2}
 -\frac{(N-1)\mu^2}{4N^3}\right]. \tag{4.17a}
\]
The bracket decreases with \(\mu\).  For \(N\ge5\), its first two terms
already give a nonpositive bound when \(\mu\ge3/2\).  For \(N=3,4\),
including the cubic term gives respectively \(-2/45\) and \(-11/160\) at
\(\mu=3/2\); for \(N=2\), including the quartic term gives \(-29/640\).
The endpoint \(\mu=N\) follows by continuity.  Thus the tail is at most
\((1+\mu)e^{-\mu}\).  Two
deterministic ones give zero.  This proves (4.17).

For each transformed layer put

\[
\begin{aligned}
A_j&=(1-j/(2n))c_n-\Gamma_j(F_2),\\
B_j&=j/(2n)-\Gamma_j(B^n)+\Gamma_j(F_2),\\
C_j&=\Gamma_j(F_1)-\Gamma_j(F_2).
\end{aligned} \tag{4.18}
\]

The margin is at least \(A_j+pB_j-qC_j\).  Exact scalar algebra gives
\(B_j>0\) and \(2z_nB_j\ge C_j\).  If \(\mu\le3/2\), (4.16) and
\(q\le1\) leave the gate

\[
A_j+z_nB_jE_{12}((n-1)/2-3)-C_j>0,
\]

where \(E_{12}(x)=\sum_{k=0}^{12}x^k/k!\).  If
\(3/2\le\mu\le(n-1)/4\), the two expressions obtained from (4.17),

\[
 A_j+z_nB_je^{(n-1)/2-2\mu}-C_je^{1-\mu},
\]

and

\[
 A_j+z_nB_je^{(n-1)/2-2\mu}-C_j(1+\mu)e^{-\mu},
\]

are nonincreasing in \(\mu\), precisely because
\(2z_nB_j\ge C_j\).  It is therefore enough to check the endpoint
\(\mu=(n-1)/4\).  Using the rational lower bound \(E_{12}\le e^x\), and
\(e<11/4\le1+(n-1)/4\) for \(n\ge8\), so that at the terminal point the
pure-exponential tail is no larger than the Poisson tail,
the full continuous domain reduces to the four exact rational gates

\[
 B_j>0,\quad 2z_nB_j\ge C_j,\quad
 A_j+z_nB_jE_{12}((n-1)/2-3)-C_j>0,
\]

\[
 A_j+z_nB_j-C_j\frac{1+(n-1)/4}{E_{12}((n-1)/4)}>0. \tag{4.19}
\]

All four gates for the 92 layers are checked exactly by the certificate in
the supplement; the preceding reduction, rather than the computation alone,
covers every continuous weight and every \(u\in[0,1/2]\).

It remains to treat \(3\le n\le7\).  For fixed long branches, fixed
total weight of length-two branches, and fixed \(u\), the actual chord
margin is affine in the product of any two short-branch weights.  At a
minimum on the short-branch simplex, all positive short-branch weights may
therefore be taken equal; otherwise one moves along a fixed-sum line until a
weight vanishes without increasing the margin.  All-transposition stars are
then covered for \(3\le n\le6\) by ten exact continuous certificates.  For
\(n=7\), the same equal-weight reduction gives the exact minimum

\[
 p\ge q_6:=\frac{5^5}{6^6}>\frac1{32}=2^{2-7}.
\]

Indeed, for \(k\) positive equal weights \(a\le1/k\),
\(p_k(a)=(1-a)^{k-1}(1-(k+1)a+2ka^2)\) decreases on that interval and
has minimum \(q_k=(k-1)^{k-1}/k^k\); \(q_k\) decreases with \(k\), so
\(k\le6\) gives the displayed bound.  Theorem 1.1 now closes the whole chord
for \(n=7\).  If at least one branch is
longer, integer partitions of \(\sum_i(\ell_i-1)\le6\) leave exactly 32
support structures.  The stick-breaking substitution
\[
b_i=x_i\prod_{j<i}(1-x_j),\qquad u=y/2,
\qquad 0\le x_i,y\le1,
\]
maps a unit box onto each complete weight simplex.  Exact Bernstein
subdivision proves the margin nonnegative on all 318 leaf boxes.  An
independent checker reconstructs every coefficient from the original matrix,
and the complete propositions and hashes appear in the supplement.

The ranges \(3\le n\le7\), \(8\le n\le15\),
\(16\le n\le31\), and \(n\ge32\) are disjoint and exhaustive.
They include zero weights, \(\sum_i a_i=1\), and all \(f\ge0\).
This proves the theorem.  \(\square\)

## 5. Cycle--element incidence forests

We now prove Theorem 1.3.

### 5.1 Compatible cycle selections and an entropy endpoint

The incidence-forest hypothesis implies that every nontrivial directed cycle in the
support is one of the original \(C_i\): a simple directed cycle crossing two blocks
would have to revisit a cut element.  Thus a permanent term is specified by a set of
pairwise element-disjoint original cycles.

Let \(B_i\in\{0,1\}\) record whether cycle \(i\) is selected.  At an element \(v\),
the local variables are mutually exclusive, with probabilities \(a_i\) for incident
cycles and residual probability

\[
d_v=1-\sum_{i\ni v}a_i.
\]

In every component choose one element vertex as root.  Direct every incidence
edge away from it.  Each cycle vertex owns all its child elements; because the
incidence graph is a tree, a cycle of length \(\ell_i\) owns exactly
\(\ell_i-1\) elements, while the remaining root element accounts for the
component itself.  The local marginals have a compatible joint law.  Propagate
away from the root: if a parent cycle is active, every child cycle at the next
element is inactive; if it is inactive, choose one child \(j\) with conditional
probability \(a_j/(1-a_{\rm parent})\), or choose none with probability
\(d_v/(1-a_{\rm parent})\).  The resulting law \(q\) satisfies

\[
q(B)=\frac{\prod_v\mu_v(B_{\mathrm{inc}(v)})}
{\prod_i\mu_i(B_i)^{\ell_i-1}}. \tag{5.1}
\]

The Gibbs variational inequality
\(\log\sum_Bw_B\ge H(q)+\mathbb E_q\log w_B\)
then yields

\[
p:=\operatorname{per}(A)
\ge\exp\!\left(-\sum_i(\ell_i-1)h(a_i)\right)
\ge2^{-M}, \tag{5.2}
\]

where \(M=\sum_i(\ell_i-1)\) and
\(h(a)=-a\log a-(1-a)\log(1-a)\).  Since \(n=c+f+M\), if \(c+f\ge2\) then
\(p\ge2^{2-n}\).  Theorem 1.1 proves the first part of Theorem 1.3.

We shall also use the strengthened endpoint--mean relation

\[
p\ge\exp\left(-M\log2+\frac M2-2\mu\right),
\qquad
\mu=\sum_i(\ell_i-1)a_i(1-a_i). \tag{5.3}
\]

It follows from \(\log2-h(a)\ge2(a-1/2)^2\).  Boundary weights follow by
continuity.

### 5.2 A real collision statistic

Use the ownership just defined.  Each non-root element \(v\) has a unique parent
cycle \(i(v)\); let \(p(v)\) be the predecessor row of \(v\) along that
directed cycle.  For independently chosen rows define

\[
D=\sum_v\mathbf1_{\{X_{p(v)}=v\}}(N_v-1). \tag{5.4}
\]

If \(d=\sum_v(N_v-1)_+\) is the total collision deficit, then
\(0\le D\le d\), and \(\Pr(d=1)\le\Pr(D\le1)\).  For a child
element owned by cycle \(i\), the event
\(X_{p(v)}=v\) has probability \(a_i\), while the expected number of other
rows entering \(v\) is \(1-a_i\).  Row independence therefore gives

\[
\mathbb ED=\sum_i(\ell_i-1)a_i(1-a_i)=\mu. \tag{5.5}
\]

### 5.3 One-hot decorrelation

We need a tail estimate which does not falsely treat the collision indicators as
independent.

### Lemma 5.1

Suppose each row independently selects exactly one column.  If \(f_v\) is positive,
depends only on the indicators entering column \(v\), and is decreasing in every
coordinate, then

\[
\mathbb E\prod_vf_v\le\prod_v\mathbb Ef_v. \tag{5.6}
\]

#### Proof

Condition on all but one row.  Write the local values as \(a_v\le b_v\) according as
the row selects \(v\) or not, and put \(\delta_v=1-a_v/b_v\).  The conditional
expectation under the one-hot row equals

\[
\left(\prod_vb_v\right)\left(1-\sum_vp_v\delta_v\right).
\]

Replacing the row indicators by independent Bernoulli variables with the same
marginals gives

\[
\left(\prod_vb_v\right)\prod_v(1-p_v\delta_v),
\]

which is larger because \(\prod_v(1-y_v)\ge1-\sum_vy_v\).  Replace rows one at a
time.  At the end the column families are independent, giving (5.6).  \(\square\)

Apply the lemma to \(f_v=x^{D_v}\), \(0<x<1\), where
\(D_v=\mathbf1_{\{X_{p(v)}=v\}}(N_v-1)\).
For each owned column, conditioning on the parent-row event and using
\(1-y\le e^{-y}\) together with \(1-e^{-b}\ge b/2\) for
\(0\le b\le1\), gives
\[
\mathbb E x^{D_v}\le
\exp\left(-\frac12a_i(1-a_i)(1-x)\right).
\]
Multiplying over the \(\ell_i-1\) owned columns of every cycle gives

\[
\mathbb Ex^D\le\exp\left(-\frac\mu2(1-x)\right). \tag{5.7}
\]

Writing \(\nu=\mu/2\), assume \(\nu\ge1\) and choose \(x=1/\nu\).  Then

\[
q:=\Pr(d=1)\le\Pr(D\le1)\le\nu e^{1-\nu}. \tag{5.8}
\]

### 5.4 The large-order chord estimate

Assume \(n\ge64\).  Let

\[
\Phi_I=\operatorname{per}\left(\frac{I_n+J_n}{2}\right),
\quad S_n=2^n\Phi_I,
\quad C_n=2+\sqrt{\frac{\pi n}{2}}.
\]

If \(p\ge2\Phi_I-c_n\), then
\[
\operatorname{per}(uA+(1-u)J_n)
\le\operatorname{per}(uI_n+(1-u)J_n)
\]
by the coefficientwise unit-matrix envelope.  Convexity of the right-hand side
on \(0\le u\le1/2\) bounds it by the chord joining \(c_n\) and
\(\Phi_I\), which is below the chord joining \(c_n\) and \(p\).
Thus this high-permanent range is closed.  Otherwise, (5.3) and
\(S_n\le C_n\) imply

\[
\mu>L_n:=\frac{n-1}{4}-\frac12\log C_n. \tag{5.9}
\]

The function \(L_n\) is increasing, and \(L_{64}>13\), so \(\nu>13/2\).  Hence

\[
q<\frac{13}{2}e^{-11/2}<\frac1{32}. \tag{5.10}
\]

Use the two-collision envelope

\[
R_A\preceq pB^n+qF_1+(1-p-q)F_2,
\qquad F_2=(1+2z)^2B^{n-4}. \tag{5.11}
\]

For \(n\ge32\), direct scalar estimates give

\[
0\le\Phi(F_2)<\frac7{16}z_n,\qquad
0\le\Phi(F_1)\le z_n,\qquad
\Phi_I<\frac1{1024}. \tag{5.12}
\]

For reference, direct summation yields
\[
\frac{\Phi(F_2)}{z_n}
=\frac{(4n^2-n-6)S_n-2n(8n-11)}
{2(n-1)(n-2)(n-3)}.
\]
Using \(S_n\le2+\sqrt{\pi n/2}\) gives the stated
\(7z_n/16\) bound.  The midpoint chord margin therefore satisfies

\[
G>z_n\left(\frac12-\frac1{1024}-\frac7{16}-\frac1{32}\right)
=\frac{31}{1024}z_n>0. \tag{5.13}
\]

The positive Bernstein reduction restores the full interval.  This proves Theorem
1.3 for \(n\ge64\).  The remaining single-cycle and shared-center cases are Theorems
4.1 and 4.2.  \(\square\)

## 6. Reproducibility and finite certificates

The proof has three finite exact components:

1. the 495 endpoint layers for \(2\le n\le31\);
2. the 376 Poisson-boundary layers and 92 coupled small-mean layers used in the
   shared-center theorem;
3. the 32 small support structures, 318 Bernstein leaf boxes, ten low-degree star
   certificates, and 255 reconstructed exact coefficients.

All use rational arithmetic.  Independent checkers reconstruct the relevant rook
polynomials and Bernstein leaves from the original matrices; destructive controls
are included for the star certificates.  The precise proposition certified by
each computation, the distinction between discovery and independent checkers,
the commands, and the frozen SHA-256 values are recorded in
[the finite-certificate supplement](supplement.md).  The complete internal
dependency manifest is recorded in
loops/LIH-WANG-PUBLICATION-PREP-0001/A1-写作前审计包.md.

These calculations certify finite symbolic leaves.  They do not test a finite sample
of matrices as a substitute for a general argument.

## 7. Relation to prior work and limitations

The original Lih--Wang conjecture concerns all doubly stochastic matrices.  Theorem
1.1 instead gives a sufficient scalar gate, while allowing the larger row-stochastic
domain.  These are different kinds of statements.  Likewise, star matrices are
required to satisfy a convexity inequality against every doubly stochastic comparison
matrix over the full unit interval.  A necessary permanent lower bound for a star is
not, by itself, a sufficient star criterion; Theorem 1.1 should not be read that way.

Goldwasser's direct-sum theorem concerns radial monotonicity of all-order
subpermanents under stronger blockwise hypotheses.  At order \(n\), radial
monotonicity gives an endpoint comparison rather than the chord upper bound (1.3).
Corollary 1.2 is therefore not a reformulation of that theorem.

Known direct overlaps include the original order-three result, the complete
order-four doubly stochastic half interval, a conditional order-six range, and
several \(2\times2\)-block star subdomains.  We exclude these from any novelty claim.
The exact cycle-forest ranges in Theorem 1.3 were not found in the original sources
examined, but this statement is bounded by the available literature: the full texts
of Lih--Wang (1982), Chang (1983), Goldwasser (1992), and
Subramanian--Somasundaram (2016) were not all available to us.  Publisher
abstracts and later exact restatements were used to bound their main theorems.
Accordingly, we do not claim global priority.

The following remain open here:

- the full Lih--Wang conjecture;
- optimality or necessity of \(2^{2-n}\);
- connected multi-center cycle forests below order \(64\);
- incidence structures containing a cycle;
- an unconditional direct-sum transfer theorem.

## References

1. S. M. Arulraj and K. Somasundaram, *Star Matrices: Properties and Conjectures*,
   Applied Mathematics E-Notes 7 (2007), 42--49.
2. K. U. Divya and K. Somasundaram, *Direct sum of star matrices*, Journal of
   Analysis and Applications 20 (2022), 69--80.
3. K. U. Divya and K. Somasundaram, *Lih Wang and Dittert's Conjectures on
   Permanents*, Special Matrices 12 (2024), article 2024-0006,
   DOI: `10.1515/spma-2024-0006`.
4. K.-W. Lih and E. T. H. Wang, *A convexity inequality on the permanent of doubly
   stochastic matrices*, Congressus Numerantium 36 (1982), 189--198.
5. D. K. Chang, *Notes on permanents of doubly stochastic matrices*, Linear and
   Multilinear Algebra 14 (1983), 349--356.
6. J. L. Goldwasser, *Monotonicity of permanents of direct sums of doubly stochastic
   matrices*, Linear and Multilinear Algebra 33 (1992), 185--188.
7. P. Subramanian and K. Somasundaram, *Some Conjectures on Permanents of Doubly
   Stochastic Matrices*, Journal of Discrete Mathematical Sciences and Cryptography
   19 (2016), 997--1011.
8. L. I. Troanca, *Permanents of Doubly Stochastic Matrices*, M.Sc. thesis,
   University of Manitoba, 2008.

## AI-assisted research disclosure

The research, proof development, checking, and writing were conducted with substantial
AI assistance.  Carptopus is the human author and assumes responsibility for the
mathematical claims and the released version.
