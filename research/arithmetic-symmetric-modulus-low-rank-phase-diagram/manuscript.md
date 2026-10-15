# Sharp Schatten constants for the arithmetic symmetric modulus: dimension two and rank-two strata

Carptopus  
carptopus@163.com

Public Beta preprint, version 0.1-beta, 15 October 2026. The frozen theorem
package and the complete manuscript have passed separate internal project
reviews. External mathematical review and formal peer review have not been
completed.

## Abstract

For a complex matrix $A$, put

$$
S(A)=\frac{|A|+|A^*|}{2}.
$$

For every integer $m\ge2$ and every $1<p<\infty$, we determine the sharp constant
in dimension two for

$$
\left\|S\!\left(\sum_{j=1}^m A_j\right)\right\|_p
\le c\left\|\sum_{j=1}^m S(A_j)\right\|_p,
\qquad A_j\in M_2(\mathbb C).
$$

The constant is independent of $m$ and is given by an explicit one-variable maximum,

$$
c_p^{\mathrm{sym}}(m,2)=
\max_{0\le y\le1}
\frac{\bigl((1+y-y^p)^p+y^p\bigr)^{1/p}
(1+y^p)^{1/2-1/p}}
{\sqrt{1+2y-y^p}}.
$$

Every interior maximizing value is attained by two real rank-one summands. For $p=2$
the constant is $1.017898490669140\ldots$. We then pass to arbitrary ambient
dimension under the condition that the sum has rank at most two. In that stratum
the exact Frobenius constant is $\sqrt{3\sqrt2}/2$. The same candidate curve does
not extend below the quadratic exponent: for every $1<p<2$ we construct a finite
dimensional rank-two example that exceeds it. At $p=3$ we prove the candidate bound
on two natural strata of the rank-two Gram model: equal nonzero singular values,
and arbitrary singular values with a commuting compressed positive factor. These
results use a common balanced block-positive representation and expose a partial
exponent--dimension--rank phase diagram. They do not determine the high-dimensional
problem at arbitrary rank or the full rank-two problem for finite $p>2$.

**Keywords:** operator symmetric modulus; Schatten norm; sharp triangle inequality;
matrix modulus; block positive matrix; low-rank matrix inequality; extremal matrix
inequality.

## 1. Introduction

The usual modulus $|A|=(A^*A)^{1/2}$ is not invariant under taking adjoints. Its
arithmetic symmetrization

$$
S(A)=\frac{|A|+|A^*|}{2}
\tag{1.1}
$$

is positive and satisfies $S(A)=S(A^*)$, but it does not satisfy the ordinary
triangle inequality with constant one for every unitarily invariant norm. Bourin
and Lee studied triangle inequalities for this modulus [1]. Zhang subsequently
formulated the associated sharp-constant problem and established dimension-free
bounds, endpoint results, and explicit low-dimensional witnesses [2].

For $m\ge2$, $n\ge1$, and $1\le p\le\infty$, write

$$
c_p^{\mathrm{sym}}(m,n)=
\sup_{(A_1,\ldots,A_m)\ne0}
\frac{\left\|S(A_1+\cdots+A_m)\right\|_p}
{\left\|S(A_1)+\cdots+S(A_m)\right\|_p},
\tag{1.2}
$$

where $\|\cdot\|_p$ is the Schatten $p$-norm. We determine (1.2) for $n=2$
and every finite interior exponent, and then determine or separate several natural
rank-two strata in arbitrary ambient dimension.

**Theorem 1.1.** Let $m\ge2$ and $1<p<\infty$. Define

$$
\mathcal C_p(y)=
\frac{\bigl((1+y-y^p)^p+y^p\bigr)^{1/p}
(1+y^p)^{1/2-1/p}}
{\sqrt{1+2y-y^p}},
\qquad 0\le y\le1.
\tag{1.3}
$$

Then

$$
\boxed{
c_p^{\mathrm{sym}}(m,2)=\max_{0\le y\le1}\mathcal C_p(y).}
\tag{1.4}
$$

The value is independent of $m$. Every interior maximizing value of $y$ is
realized by two real rank-one matrices. Endpoint values are obtained by a
degenerate decomposition or by a limit of such decompositions.

For $p=2$, (1.4) simplifies as follows.

**Corollary 1.2.** Let $\rho$ be the unique root in $(0,1)$ of

$$
\rho^3-3\rho^2-\rho+1=0.
$$

Then, for every $m\ge2$,

$$
c_2^{\mathrm{sym}}(m,2)=
\sqrt{\frac{1+\rho^2}
{\rho+\sqrt{\rho^2+(1-\rho)^2}}}
=1.017898490669140\ldots.
\tag{1.5}
$$

Two real rank-one summands attain equality.

Our second main theorem is dimension-stable but rank-restricted.

**Theorem 1.3.** Let $n\ge3$ and $m\ge2$. If
$T=A_1+\cdots+A_m$ has rank at most two, then

$$
\frac{\|S(T)\|_2}{\|S(A_1)+\cdots+S(A_m)\|_2}
\le \frac{\sqrt{3\sqrt2}}2.
\tag{1.6}
$$

The constant is sharp for every such $n$ and $m$.

For other exponents put

$$
L_p=\left(\frac{2^p+2}{2^{p/2+3/2}}\right)^{1/p}.
\tag{1.7}
$$

The value $L_p$ is attained by a two-summand rank-two nilpotent family. Its role
changes at the quadratic exponent.

**Theorem 1.4.** For every fixed $1<p<2$ there are finite integers $n(p),m(p)$
and real rank-one matrices $A_1,\ldots,A_{m(p)}\in M_{n(p)}(\mathbb R)$ such that
$\operatorname{rank}(\sum_jA_j)=2$ and

$$
\frac{\|S(\sum_jA_j)\|_p}{\|\sum_jS(A_j)\|_p}>L_p.
\tag{1.8}
$$

The dimensions in Theorem 1.4 are allowed to depend on $p$; no single finite pair
$(n,m)$ is asserted to work simultaneously for all $p\in(1,2)$.

At $p=3$ we obtain two positive strata. Their clean formulation uses the rank-two
Gram model introduced in Section 6.

**Theorem 1.5.** In the rank-two Gram model at $p=3$, the bound with
$L_3^3=5/4$ holds in each of the following cases:

1. the two nonzero singular values of $T$ are equal, with arbitrary compressed
   positive factor and arbitrary $2\times2$ contraction;
2. the singular values are arbitrary and the compressed positive factor $C$
   commutes with the singular-value matrix $\Sigma$.

The first stratum is sharp. The second condition is a condition on the compressed
factor induced by the decomposition, or on an inner minimizing factor; it is not
an intrinsic normality or commutativity condition on $T$ alone.

The public arXiv version of [2] gives, in its Section 8, a non-sharp
two-dimensional Frobenius witness of approximately $1.0144$. Formula (1.5)
sharpens that witness, while Theorem 1.1 treats all finite $p$. The version of
record of [2] is identified in the references, but its full text was not publicly
accessible during preparation of this draft. Comparisons in this manuscript are
therefore specifically comparisons with arXiv:2603.01046v1. We make no claim of
global priority, and we do not claim to solve (1.2) for $n\ge3$.

The proof has two layers. Sections 2--5 give the complete two-dimensional theorem:
the balanced block-positive representation, a complex normal form, an exact Pareto
frontier, and the parameter elimination leading to (1.3). Section 6 compresses an
arbitrary ambient-dimensional rank-two sum to a $4\times4$ Gram model and proves
Theorem 1.3. Section 7 proves the dimension-amplification theorem and the scalar
chain transition at $p=2$. Section 8 proves the two $p=3$ strata by reducing a
matrix inequality to the seven vertices of a $2\times2$ partial-matching polytope.
Section 9 collects the resulting phase diagram and the remaining open layers.

## 2. Balanced block-positive decompositions

We first isolate the convex object underlying the denominator. The result is stated
for arbitrary dimension because its proof is no harder in that form.

**Proposition 2.1.** Let $T,D\in M_n(\mathbb C)$ with $D=D^*$, and let $r\ge1$ be
an integer.
The following are equivalent.

1. There are at most $r$ rank-one matrices $A_j$ such that
   $T=\sum_jA_j$ and $D=\sum_jS(A_j)$.
2. There is a Hermitian matrix $H$ with $\operatorname{tr}H=0$ such that

   $$
   B(T,D,H):=
   \begin{pmatrix}D+H&T\\T^*&D-H\end{pmatrix}\succeq0,
   \qquad \operatorname{rank}B(T,D,H)\le r.
   \tag{2.1}
   $$

Without the rank restriction, every block in (2.1) is represented by at most
$2n$ rank-one summands.

**Proof.** Write a rank-one matrix as $A=xy^*$ with $\|x\|=\|y\|$. Then

$$
S(A)=\frac{xx^*+yy^*}{2}.
\tag{2.2}
$$

For a family $(x_j,y_j)$, set

$$
D+H=\sum_jx_jx_j^*,\qquad D-H=\sum_jy_jy_j^*.
$$

The equal-length condition gives $\operatorname{tr}H=0$, and

$$
B(T,D,H)=\sum_j
\binom{x_j}{y_j}\binom{x_j}{y_j}^*.
$$

This proves one direction and the rank bound.

Conversely, factor $B=ZZ^*$ with $Z=\binom XY$ and $r_0=\operatorname{rank}B$
columns. Put $K=X^*X-Y^*Y$. Since $\operatorname{tr}H=0$, one has
$\operatorname{tr}K=0$. By the Schur--Horn theorem [4], there is a unitary $U$
such that $\operatorname{diag}(U^*KU)=0$. If $x_j,y_j$ are the corresponding
columns of $XU,YU$, then $\|x_j\|=\|y_j\|$. Equation (2.2) now recovers $T$
and $D$ from at most $r_0\le2n$ rank-one summands. ∎

When $B$ is real and $r_0\le2$, the reverse construction may be kept real.
Indeed, take a real Gram factorization. The resulting $K$ is real symmetric and
traceless; in an eigenbasis it is $\operatorname{diag}(\lambda,-\lambda)$ (with
the rank-one case immediate), and a $45^\circ$ real orthogonal rotation makes
its diagonal zero. Thus a real rank-two block yields two real rank-one
summands.

An arbitrary matrix summand may be split into its singular-value rank-one terms;
this preserves both its contribution to $T$ and the sum of its contributions to
$D$. Consequently every tuple in (1.2) gives a block of the form (2.1), without
a useful rank bound depending only on the original number $m$. This is sufficient
for our upper bound. The extremizers constructed in Section 5 use two rank-one
summands, so the matching lower bound is available for every $m\ge2$.

Every feasible block also implies the phase envelope

$$
D\succeq\operatorname{Re}(e^{i\theta}T)
\qquad(\theta\in\mathbb R).
\tag{2.3}
$$

Indeed, substitute two phase-related copies of the same vector into the quadratic
form of (2.1); the contributions from $H$ cancel. We use (2.1) to retain the
balance information and (2.3) to eliminate auxiliary variables.

## 3. A two-dimensional spectral gate

We now specialize to $n=2$. Multiplication of $T$ by a scalar phase and simultaneous
unitary conjugation do not change the quotient in (1.2). The identity

$$
S(T)=\frac{T^*T+TT^*+2|\det T|I}{2\|T\|_1}
$$

shows that, after making $\operatorname{tr}T$ nonnegative real, diagonalizing
$S(T)$, and fixing the remaining off-diagonal phase, a dense set of nonzero
matrices has the form

$$
T=\begin{pmatrix}
h+x+ik&b\\-b&h-x-ik
\end{pmatrix},
\qquad h,x,b\ge0,\quad k\in\mathbb R.
\tag{3.1}
$$

Put $q=\|T\|_1/2$. The two-dimensional square-root formula gives

$$
S(T)=\operatorname{diag}\left(q+\frac{hx}{q},q-\frac{hx}{q}\right)
\tag{3.2}
$$

and

$$
(q^2-x^2)(q^2-h^2-b^2)=q^2k^2.
\tag{3.3}
$$

The omitted zero-trace and repeated-eigenvalue cases follow by continuity without
changing the number of original summands. More explicitly, for a fixed tuple
$T=\sum_{j=1}^mA_j$, choose generic $T_\nu\to T$, put
$A_{1,\nu}=A_1+(T_\nu-T)$, and leave the other $A_j$ unchanged. Continuity of
$S$ passes every uniform estimate back to the original tuple. We normalize
$q=1$. Then $0\le h,x\le1$ and, in the interior $x<1$,

$$
b^2=1-h^2-\frac{k^2}{1-x^2},
\qquad k^2\le(1-h^2)(1-x^2).
\tag{3.4}
$$

Let $Q=\operatorname{diag}(1,-1)$. The normal form satisfies $QT^TQ=T$.
If $B(T,D,H)$ is feasible, conjugating entrywise and then exchanging the two
block coordinates with $\begin{psmallmatrix}0&Q\\Q&0\end{psmallmatrix}$ gives
another feasible block for the same $T$, with

$$
D'=Q\overline DQ,
\qquad H'=-Q\overline HQ.
$$

Averaging $(D,H)$ with $(D',H')$ preserves feasibility and $\operatorname{tr}H=0$.
Convexity and unitary invariance give
$\|(D+D')/2\|_p\le(\|D\|_p+\|D'\|_p)/2=\|D\|_p$.
Hence the denominator may be restricted to

$$
D=\begin{pmatrix}d&iy\\-iy&e\end{pmatrix},
\qquad
H=\begin{pmatrix}0&z\\z&0\end{pmatrix},
\qquad d,e,y,z\in\mathbb R.
\tag{3.5}
$$

Write

$$
\tau=\operatorname{tr}D,
\qquad R=\lambda_1(D)-\lambda_2(D),
\qquad u=R/\tau\in[0,1],
\qquad w=d-e.
\tag{3.6}
$$

Thus $|w|\le R$ and

$$
\det D=de-y^2=\frac{\tau^2(1-u^2)}4.
\tag{3.7}
$$

The following lemma is the gate used in the rest of the proof.

**Lemma 3.1.** If (3.1)--(3.5) come from a feasible balanced block, then, for
$0\le h,x<1$,

$$
\frac{\tau^2(1-u^2)}4
\ge
\psi_{h,x}\!\left(\tau\max(h-xu,0)\right),
\tag{3.8}
$$

where

$$
\psi_{h,x}(a)=
\begin{cases}
\displaystyle 1-h^2+\frac{a^2}{4(1-x^2)},
&0\le a\le2(1-x^2),\\[7pt]
a-h^2+x^2,&a\ge2(1-x^2).
\end{cases}
\tag{3.9}
$$

**Proof.** Apply (2.3) to (3.1) and (3.5). If $c=\cos\theta$ and
$s=\sin\theta$, positivity implies, for every point on $c^2+s^2=1$, the
determinant inequality

$$
 [d-c(h+x)+sk][e-c(h-x)-sk]-(y-bs)^2\ge0.
\tag{3.10}
$$

The equality version of the S-lemma [5] applies because
$c^2+s^2-1$ takes both signs. Thus (3.10) is equivalent to the existence of a
scalar multiplier for which

$$
\begin{pmatrix}
A-\lambda I_2&\ell/2\\
\ell^T/2&\det D+\lambda
\end{pmatrix}\succeq0,
$$

where

$$
A=\begin{pmatrix}h^2-x^2&kx\\kx&-b^2-k^2\end{pmatrix},
\qquad
\ell=\binom{-h\tau+xw}{2by-kw}.
$$

Put $L=-\lambda$. The upper-left $2\times2$ principal block $P$ and
(3.4) give the factorization

$$
\det P=
\frac{L+h^2-1}{1-x^2}
\left((1-x^2)(L+h^2-x^2)+k^2x^2\right).
\tag{3.11}
$$

The second factor is strictly positive in the interior. If it vanished, positivity
of $P$ would force $L+h^2-x^2=0$ and $kx=0$. If $k=0$, then
$b^2=1-h^2$ and the other diagonal entry of $P$ equals $x^2-1<0$; if
$x=0$, that entry equals $-1$. Both contradict $P\succeq0$. Hence
$L\ge1-h^2$.
The principal minor using the first and third Gram coordinates gives

$$
\det D\ge
L+\frac{(h\tau-xw)^2}{4(L+h^2-x^2)}.
\tag{3.12}
$$

For $a=|h\tau-xw|$, minimizing the right-hand side over $L\ge1-h^2$
is exactly (3.9). Finally $|w|\le u\tau$ implies

$$
|h\tau-xw|\ge\tau\max(h-xu,0),
$$

and $\psi_{h,x}$ is increasing. Equations (3.7) and (3.12) prove (3.8). ∎

If $h=1$ or $x=1$, (3.4) forces $k=0$. The diagonal part of (2.3) then gives
$d\ge1+hx$ and $e\ge1-hx$. These boundary points already have quotient at most
one and will not affect the sharp constant.

## 4. The balanced point is globally optimal

Put

$$
r=hx,
\qquad 0\le r\le1.
\tag{4.1}
$$

The numerator in (3.2) depends on the normal form only through $r$. The next
proposition shows that, at fixed numerator and fixed denominator spectral ratio,
the least possible trace occurs at $h=x=\sqrt r$.

**Proposition 4.1.** Fix $r\in(0,1)$ and $u\in[0,1)$. Among all
$h,x\in(0,1)$ with $hx=r$ satisfying the gate (3.8), the minimum possible
$\tau$ is attained at $h=x=\sqrt r$.

**Proof.** First suppose that the first contact in (3.8) occurs in the quadratic
branch of (3.9) and $a=h-xu>0$. Solving for the first root gives

$$
\tau_q^2=
\frac{4(1-h^2)(1-x^2)}
{1-h^2-x^2-u^2+2ru}.
\tag{4.2}
$$

Set $z=h^2+x^2\ge2r$. The right-hand side is

$$
4\frac{1-z+r^2}{1-z-u^2+2ru},
$$

whose derivative with respect to $z$ has the sign of $(r-u)^2$. It is therefore
minimal at $z=2r$, or $h=x=\sqrt r$.

If $h-xu\le0$, then $h\le x$ and $u\ge h/x$. The quadratic-branch root is
$2\sqrt{(1-h^2)/(1-u^2)}$. Comparing it with the balanced root reduces to

$$
(1-h^2)(1+u-2r)-(1-r)^2(1+u)\ge0.
\tag{4.3}
$$

At $u=h/x$, the left-hand side equals

$$
-\frac{h^2(x-h)(x^2-1)}x\ge0,
$$

and its derivative in $u$ is

$$
-h\bigl(h(x^2+1)-2x\bigr)\ge0.
$$

Thus the zero-remainder case is also no better than the balanced point.

It remains to rule out a disconnected earlier feasible interval created by the
linear branch. Its first feasible root, whenever first contact genuinely occurs
there, is

$$
\tau_\ell=
\frac{2\bigl(h-xu+|x-hu|\bigr)}{1-u^2}.
\tag{4.4}
$$

One always has

$$
\tau_\ell\ge\frac{4\sqrt r}{1+u}.
\tag{4.5}
$$

For $x\ge hu$ this is the arithmetic--geometric mean inequality. For $x<hu$,
put $v=h/x>1/u$; the difference at $u=x/h$ is

$$
\frac{x(t^2-1)(t-1)^2}{t^2}\ge0,
\qquad t=\sqrt{h/x},
$$

and the difference increases with $u$.

If the balanced point lies in the linear branch, (4.5) proves the claim. Suppose
instead that

$$
B:=1+u-r(3-u)\ge0,
\qquad
Q:=\frac{2(1-r)}{\sqrt{(1-u)(1+u-2r)}}
\tag{4.6}
$$

is its quadratic first-contact value. The linear-branch entry is
$\tau_b=2(1-x^2)/(h-xu)$. First contact can occur in the linear branch only if
that entry is infeasible. Substitution in (3.8) factors the entry remainder as

$$
(1-u^2)(1-x^2)^2-(h-xu)^2(2-z)
=(z-T_1)(z-T_2)<0,
\tag{4.7}
$$

where

$$
T_1=1+r-u(1-r),\qquad T_2=1-r+u(1+r).
\tag{4.8}
$$

Moreover

$$
T_1-2r=(1-r)(1-u),\quad
T_2-2r=B,\quad
T_1-T_2=2(r-u).
\tag{4.9}
$$

If $r<u$, (4.7)--(4.9) give $z>T_1$. In this case $x\ge hu$ is impossible,
because it would imply $u<h/x\le1/u$ and

$$
z=r(v+v^{-1})\le r(u+u^{-1})<T_1.
$$

Hence $x<hu$ and $\tau_\ell^2=4(z-2r)/(1-u)^2$. With

$$
Z_B=2r+\frac{(1-r)^2(1-u)}{1+u-2r},
$$

we have

$$
T_1-Z_B=
\frac{(1-r)(u-r)(1-u)}{1+u-2r}\ge0.
$$

Thus $z>Z_B$ and $\tau_\ell\ge Q$.

If $r>u$, then $z>T_2$. When $x\ge hu$, one has
$\tau_\ell^2=4(z+2r)/(1+u)^2$. Set

$$
Z_A=\frac{(1-r)^2(1+u)^2}
{(1-u)(1+u-2r)}-2r.
$$

Then

$$
T_2-Z_A=
\frac{(r-u)(1+u)B}{(1-u)(1+u-2r)}\ge0,
$$

so again $\tau_\ell\ge Q$. In the remaining subcase $x<hu$, necessarily
$u>0$ and $v>1/u$. Therefore

$$
\tau_\ell\ge2\sqrt{r/u},
$$

while

$$
\frac ru-\frac{(1-r)^2}{(1-u)(1+u-2r)}
=\frac{(r-u)(1-r(2-u))}
{u(1-u)(1+u-2r)}\ge0.
$$

The final sign follows from $r\le(1+u)/(3-u)\le1/(2-u)$. Hence
$\tau_\ell\ge Q$ in every case. The case $r=u$ follows by continuity. This
exhausts quadratic contact, zero remainder, and genuine linear contact. ∎

## 5. The exact frontier and proof of Theorem 1.1

At the balanced point $h=x=\sqrt r$, solving (3.8) gives the necessary trace
lower bound

$$
\tau_*(r,u)=
\begin{cases}
\displaystyle
\frac{2(1-r)}{\sqrt{(1-u)(1+u-2r)}},
&r(3-u)\le1+u,\\[9pt]
\displaystyle
\frac{4\sqrt r}{1+u},
&r(3-u)\ge1+u.
\end{cases}
\tag{5.1}
$$

This lower bound is the exact frontier of the balanced-block relaxation. To see
this, put

$$
T_r=\begin{pmatrix}2\sqrt r&\sqrt{1-r}\\-\sqrt{1-r}&0\end{pmatrix}.
\tag{5.2}
$$

Then

$$
S(T_r)=\operatorname{diag}(1+r,1-r).
\tag{5.3}
$$

Write $a=\sqrt r$ and $b=\sqrt{1-r}$. In the first branch set

$$
t^2=\frac{1-u}{1+u-2r}.
$$

The branch condition is equivalent to $0<t\le r^{-1/2}$. Define
$D=\operatorname{diag}(d,e)$ and
$H=\begin{psmallmatrix}0&-z\\-z&0\end{psmallmatrix}$, where

$$
e=(1-r)t,\qquad d=t^{-1}+rt,\qquad
z=\sqrt{r(1-r)}\,t.
\tag{5.4}
$$

The block (2.1) is unitarily equivalent to

$$
\begin{pmatrix}d+2\sqrt r&\sqrt{1-r}+z\\
\sqrt{1-r}+z&e\end{pmatrix}
\oplus
\begin{pmatrix}d-2\sqrt r&\sqrt{1-r}-z\\
\sqrt{1-r}-z&e\end{pmatrix}.
\tag{5.5}
$$

Both blocks in (5.5) have determinant zero: their upper-left entries are
$t^{-1}(1\pm at)^2$ and their off-diagonal entries are $b(1\pm at)$.
They are therefore positive semidefinite and rank one for $0<r<1$. The full
block has rank two, and the real form of Proposition 2.1 gives two real rank-one
summands. Moreover

$$
u=\frac{d-e}{d+e},
\qquad d+e=\tau_*(r,u).
$$

For the second branch, necessarily $r\ge1/3$. Set

$$
d=2\sqrt r,
\qquad e=2\sqrt r\,\frac{1-u}{1+u},
\qquad z=\sqrt{1-r},
$$

and again take $D=\operatorname{diag}(d,e)$ and
$H=\begin{psmallmatrix}0&-z\\-z&0\end{psmallmatrix}$. The branch condition is
equivalent to $e\ge(1-r)/\sqrt r$. The two blocks in (5.5) now become

$$
\begin{pmatrix}4\sqrt r&2\sqrt{1-r}\\2\sqrt{1-r}&e\end{pmatrix}
\oplus
\begin{pmatrix}0&0\\0&e\end{pmatrix},
$$

which is positive semidefinite, and its trace is $4\sqrt r/(1+u)$. Thus both
branches of (5.1) are attained in the balanced-block domain. The first branch,
which contains the finite-$p$ norm minimizer below, is attained by two real
rank-one summands.

For a positive $2\times2$ matrix with trace $\tau$ and normalized spectral gap
$u$, one has

$$
\|D\|_p=\frac\tau2
\bigl((1+u)^p+(1-u)^p\bigr)^{1/p}.
\tag{5.6}
$$

Proposition 4.1 and (5.1) therefore give the sharp relaxed lower envelope at fixed
$r$. The finite-$p$ minimizer lies in the attainable rank-two family (5.4). Its
denominator is

$$
\Phi_{p,r}(t)^{1/p},
\qquad
\Phi_{p,r}(t)=(t^{-1}+rt)^p+((1-r)t)^p.
\tag{5.7}
$$

The function is strictly convex on the first branch and has a unique interior
minimum. The second branch has fixed $d=2\sqrt r$ and increasing $e$, so it cannot
improve that minimum. Let

$$
y=e/d\in(0,1)
\tag{5.8}
$$

at the minimizing point. The first-order condition in (5.7) is equivalent to

$$
2ry=(1-r)(1-y^p).
\tag{5.9}
$$

The left side is strictly increasing and the right side strictly decreasing, so
the solution is unique. Solving for $r$ gives

$$
r=\frac{1-y^p}{1+2y-y^p},\qquad
1-r=\frac{2y}{1+2y-y^p}.
\tag{5.10}
$$

At the same point,

$$
d=\frac{2}{\sqrt{(1+2y-y^p)(1+y^p)}},
\qquad e=yd.
\tag{5.11}
$$

Substituting (5.10)--(5.11) into

$$
\frac{\|\operatorname{diag}(1+r,1-r)\|_p}
{\|\operatorname{diag}(d,e)\|_p}
$$

gives exactly $\mathcal C_p(y)$ in (1.3). As $y$ runs from $0$ to $1$,
(5.10) runs continuously from $r=1$ to $r=0$. The upper bound follows from
Proposition 4.1 and the exact frontier; the matching lower bound follows from
(5.2)--(5.5). This proves Theorem 1.1.

For $p=2$, direct differentiation before eliminating $r$ gives

$$
F(r)=\frac{1+r^2}{r+\sqrt{r^2+(1-r)^2}}.
$$

Its unique critical point in $(0,1)$ satisfies
$r^3-3r^2-r+1=0$, and the endpoints give value one. This proves Corollary 1.2.

## 6. Rank-two compression and the exact Frobenius constant

We now allow arbitrary ambient dimension but assume that the sum has rank at most
two. The first step is a compression that retains all relative geometry of the
left and right singular subspaces.

Let

$$
T=U\Sigma V^*,\qquad U^*U=V^*V=I_2,\qquad
\Sigma=\operatorname{diag}(\sigma_1,\sigma_2)>0,
\qquad K=U^*V.
\tag{6.1}
$$

Thus $K$ is an arbitrary $2\times2$ contraction. Refining the original summands
by singular value decomposition leaves both $T$ and the denominator unchanged.
Consequently there are positive matrices

$$
P=\sum_k t_ku_ku_k^*,\qquad
Q=\sum_k t_kv_kv_k^*
\tag{6.2}
$$

such that

$$
\begin{pmatrix}P&T\\T^*&Q\end{pmatrix}\succeq0,\qquad
\sum_jS(A_j)=\frac{P+Q}{2}.
\tag{6.3}
$$

The generalized Schur complement gives
$Q\succeq T^*P^\dagger T$. Put

$$
C=(U^*P^\dagger U)^{-1}>0.
\tag{6.4}
$$

Compression to the range of $U$ yields

$$
P\succeq UCU^*,\qquad
Q\succeq V\Sigma C^{-1}\Sigma V^*.
\tag{6.5}
$$

Hence, with

$$
D_C=\frac{UCU^*+V\Sigma C^{-1}\Sigma V^*}{2},
\tag{6.6}
$$

we have $D\succeq D_C$ and $\|D\|_p\ge\|D_C\|_p$. This implication is
one-directional: a point in the compressed model need not itself satisfy the
trace-balance condition, but an upper bound proved for every $C>0$ is sufficient
for every original decomposition.

It is useful to record the equivalent four-dimensional form. Set

$$
Y=(U\Sigma^{1/2}\quad V\Sigma^{1/2}),\qquad
H=\Sigma^{-1/2}C\Sigma^{-1/2},
\tag{6.7}
$$

and

$$
G=\frac12Y^*Y
=\frac12\begin{pmatrix}
\Sigma&\Sigma^{1/2}K\Sigma^{1/2}\\
\Sigma^{1/2}K^*\Sigma^{1/2}&\Sigma
\end{pmatrix},
\qquad
W_H=\begin{pmatrix}H&0\\0&H^{-1}\end{pmatrix}.
\tag{6.8}
$$

The nonzero spectra of $YY^*$ and $Y^*Y$ agree, as do those of
$YW_HY^*$ and $W_H^{1/2}Y^*YW_H^{1/2}$. Therefore

$$
\|S(T)\|_p=\|G\|_p,\qquad
\|D_C\|_p=\|W_H^{1/2}GW_H^{1/2}\|_p.
\tag{6.9}
$$

For $p=2$ the required lower bound for the compressed denominator follows from
the next lemma.

**Lemma 6.1.** Let $\Sigma,C$ be positive $2\times2$ matrices and let $K$ be a
contraction. Define

$$
\begin{aligned}
a&=\operatorname{tr}\Sigma^2,
&z&=\operatorname{tr}(\Sigma K\Sigma K^*),\\
A&=\operatorname{tr}C^2,
&B&=\operatorname{tr}(\Sigma C^{-1}\Sigma)^2,\\
X&=\operatorname{tr}(CK\Sigma C^{-1}\Sigma K^*).
\end{aligned}
\tag{6.10}
$$

Then, with $\alpha=3\sqrt2/4$,

$$
a+z\le\alpha\bigl(\sqrt{AB}+X\bigr).
\tag{6.11}
$$

**Proof.** By continuity it is enough to take $\Sigma>0$. Let

$$
H=\Sigma^{-1/2}C\Sigma^{-1/2},\qquad
L=\Sigma^{1/2}K\Sigma^{1/2}.
\tag{6.12}
$$

Scaling $H$ does not change $X$ or $\sqrt{AB}$. In an eigenbasis of $H$ its
eigenvalues may therefore be written as $\sqrt\kappa,\kappa^{-1/2}$, where
$\kappa\ge1$. Write

$$
\Sigma=\begin{pmatrix}q&r\\\bar r&s\end{pmatrix},\qquad h=|r|^2,
\qquad U_0=\frac{q^2+s^2}{qs}\ge2,\qquad H_0=\frac h{qs}\ge0.
\tag{6.13}
$$

If $L=(\ell_{ij})$, then

$$
\alpha X-z
=\sum_{i,j}\left(\alpha\frac{\lambda_i}{\lambda_j}-1\right)
|\ell_{ij}|^2.
\tag{6.14}
$$

For $\kappa\le\alpha$ every coefficient in (6.14) is nonnegative. Direct
expansion also gives

$$
AB-a^2=(qs)^2\left[
(\kappa-\kappa^{-1})^2+
2H_0U_0(\kappa+\kappa^{-1}-2)\right]\ge0,
\tag{6.15}
$$

and (6.11) follows.

Suppose $\kappa\ge\alpha$. Only the $\ell_{21}$ coefficient can be negative.
Since $K$ is a contraction,

$$
|\ell_{21}|^2\le qs,
\qquad
\alpha X-z\ge-\left(1-\frac\alpha\kappa\right)qs.
\tag{6.16}
$$

It remains to prove

$$
\alpha\sqrt{AB}-a\ge
\left(1-\frac\alpha\kappa\right)qs.
\tag{6.17}
$$

Put $\beta=\alpha^{-1}=2\sqrt2/3$. After division by $\alpha qs$, (6.17)
is

$$
\sqrt\Phi\ge\beta(U_0+2H_0)+\beta-\kappa^{-1},
\tag{6.18}
$$

where

$$
\Phi=U_0^2+(\kappa+\kappa^{-1})^2-4
+2H_0U_0(\kappa+\kappa^{-1})+4H_0^2.
\tag{6.19}
$$

Both sides are nonnegative. Let $F$ be the left side squared minus the right
side squared. A direct differentiation gives

$$
\frac{\partial F}{\partial H_0}\ge
\frac{4(3\kappa^2-8\kappa+3+2\sqrt2)}{3\kappa}>0;
\tag{6.20}
$$

the quadratic numerator has discriminant $28-24\sqrt2<0$. Thus it suffices to
put $H_0=0$. The resulting quadratic in $U_0$ has vertex
$8-6\sqrt2/\kappa$. If $\alpha\le\kappa\le\sqrt2$, its minimum on
$U_0\ge2$ is

$$
F(2,0)=\frac{\kappa^3-6\kappa+4\sqrt2}{\kappa}\ge0.
\tag{6.21}
$$

If $\kappa\ge\sqrt2$, the value at the vertex is

$$
F(8-6\sqrt2/\kappa,0)
=(\kappa-\kappa^{-1})^2-(2\sqrt2-3\kappa^{-1})^2\ge0.
\tag{6.22}
$$

This proves (6.17), and (6.11) follows from (6.16). ∎

**Proof of Theorem 1.3.** Expanding the two Frobenius norms gives

$$
\|S(T)\|_2^2=\frac{a+z}{2},\qquad
\|D_C\|_2^2=\frac{A+B+2X}{4}
\ge\frac{\sqrt{AB}+X}{2}.
\tag{6.23}
$$

Lemma 6.1 and $D\succeq D_C$ imply

$$
\frac{\|S(T)\|_2^2}{\|D\|_2^2}
\le\frac{a+z}{\sqrt{AB}+X}
\le\frac{3\sqrt2}{4}.
\tag{6.24}
$$

The rank-one boundary follows from the same one-dimensional compression or by
continuity. To prove sharpness in the original decomposition problem, take in
$\mathbb R^3$

$$
U=(e_1\ e_2),\qquad V=(e_2\ e_3),\qquad
\Sigma=I_2,\qquad
K=U^*V=\begin{pmatrix}0&0\\1&0\end{pmatrix},
\tag{6.25}
$$

and put

$$
C=\operatorname{diag}(2^{1/4},2^{-1/4}),\qquad
P=UCU^*,\qquad Q=VC^{-1}V^*.
\tag{6.26}
$$

Then $\operatorname{tr}P=\operatorname{tr}Q$, and

$$
\begin{pmatrix}P&T\\T^*&Q\end{pmatrix}\succeq0,
\qquad T=U\Sigma V^*,
\tag{6.27}
$$

because $Q=T^*P^\dagger T$ on the relevant ranges. The block matrix is real
and has rank two. Proposition 2.1 therefore gives a decomposition of $T$ into
two real rank-one summands with denominator $D=(P+Q)/2$. Directly,

$$
\|S(T)\|_2^2=\frac32,
\qquad
\|D\|_2^2=\frac{\sqrt2}{2}+\frac1{\sqrt2}=\sqrt2.
\tag{6.28}
$$

Thus the squared ratio is $3\sqrt2/4$. Orthogonal embeddings and zero summands
preserve the ratio, proving sharpness for all $n\ge3$ and $m\ge2$.
∎

## 7. Dimension amplification below the quadratic exponent

The nilpotent equality family in Theorem 1.3 extends to every finite exponent
and gives the lower curve $L_p$ in (1.7). We now show that this curve ceases to
be sharp below $p=2$.

Consider the weighted three-chain

$$
T_t=e_1e_3^*+t e_2e_1^*,\qquad t>0.
\tag{7.1}
$$

For a diagonal positive factor $\operatorname{diag}(x,y)$, the numerator and
the unbalanced core denominator have $p$th powers

$$
N_p(t)=2^{-p}\bigl((1+t)^p+1+t^p\bigr),
\tag{7.2}
$$

$$
D_p(t;x,y)=2^{-p}\left((x+t^2/y)^p+y^p+x^{-p}\right).
\tag{7.3}
$$

The objective is geodesically convex and diverges at the boundary. Its unique
critical point is

$$
x_p(t)=(1+t^{2p/(p+1)})^{-(p-1)/(2p)},
\tag{7.4}
$$

$$
y_p(t)=t^{2/(p+1)}
(1+t^{2p/(p+1)})^{(p-1)/(2p)}.
\tag{7.5}
$$

Substitution gives the exact unbalanced ratio

$$
R_p(t)^p=
\frac{(1+t)^p+1+t^p}
{2(1+t^{2p/(p+1)})^{(p+1)/2}}.
\tag{7.6}
$$

At $t=1$, this is $L_p^p$. Put $t=e^s$ and
$f_p(s)=\log R_p(e^s)^p$. Then $f_p$ is even and

$$
f_p''(0)=
\frac{p(2p-2^p)(p-1)}
{4(2^p+2)(p+1)}.
\tag{7.7}
$$

Since $\log(2p)-p\log2$ is strictly concave on $[1,2]$ and vanishes at both
endpoints, $2^p<2p$ for $1<p<2$. Thus $t=1$ is a strict local minimum of
$R_p$ for every such $p$.

Fix $p\in(1,2)$ and choose $t=t(p)\ne1$ close enough to $1$ that
$R_p(t)>L_p$. The minimizing unbalanced core has trace defect

$$
\Delta_p(t)=x_p(t)+y_p(t)-x_p(t)^{-1}-t^2y_p(t)^{-1}.
\tag{7.8}
$$

Add positive semidefinite slack of total trace $|\Delta_p(t)|$ to the smaller
diagonal block and distribute it uniformly over $d$ new orthogonal directions.
Its contribution to the denominator $p$th power is

$$
\left(\frac{|\Delta_p(t)|}{2}\right)^p d^{1-p}.
\tag{7.9}
$$

This tends to zero, so some finite $d=d(p)$ preserves the strict advantage.
The resulting balanced real symmetric block has rank at most $d+2$. The real
Schur--Horn theorem supplies a real orthogonal change of basis with zero
diagonal for the associated trace-zero matrix; the reverse construction in
Proposition 2.1 therefore gives real vectors $x_j,y_j$ and real rank-one
summands $A_j=x_jy_j^T$. We may take $m=d+2$ and $n=d+3$. This proves
Theorem 1.4.

For completeness, the scalar chain points in the opposite direction above the
quadratic exponent.

**Proposition 7.1.** If $p>2$, then $R_p(t)\le R_p(1)=L_p$ for every $t>0$,
with equality only at $t=1$.

**Proof.** Differentiating with respect to $\log t$ reduces monotonicity for
$t>1$ to

$$
(t^a-t)(1+t)^{p-1}\ge t^p-t^a,
\qquad a=\frac{2p}{p+1}.
\tag{7.10}
$$

Put $r=p-1$, $z=t^{(p-1)/(p+1)}$ and $c=(p+1)/(p-1)$. Then (7.10) becomes

$$
(1+z^c)^r\ge z\,\frac{z^p-1}{z-1}.
\tag{7.11}
$$

The integral representation of the difference quotient and Minkowski's
inequality give

$$
\left(\frac{z^p-1}{z-1}\right)^{1/r}
\le p^{1/r}+z-1.
\tag{7.12}
$$

The strictly convex function

$$
z^{-1/r}+z^{1+1/r}-z+1-p^{1/r}
\tag{7.13}
$$

has derivative zero at $z=1$ and positive value there because
$2^r>r+1=p$. Hence the right side of (7.12) is strictly less than
$z^{-1/r}(1+z^c)$ for $z\ge1$, proving strict decrease for $t>1$.
The identity $R_p(t^{-1})=R_p(t)$ completes the proof. ∎

## 8. Two sharp strata at the cubic exponent

We now specialize the four-dimensional model (6.8) to $p=3$. The following
rank-one lemma will dispose of the single-edge vertices appearing below.

**Lemma 8.1.** Let $H=\operatorname{diag}(h_1,h_2)>0$ and let
$K=E_{ij}$ be one of the four $2\times2$ matrix units. With

$$
B=\begin{pmatrix}I&K\\K^*&I\end{pmatrix},
\qquad W=\operatorname{diag}(H,H^{-1}),
\tag{8.1}
$$

one has

$$
\operatorname{tr}(BW)^3\ge8
=\frac45\operatorname{tr}B^3.
\tag{8.2}
$$

For a nondiagonal matrix unit the constant is sharp.

**Proof.** Direct block multiplication gives, when $i=j$,

$$
\operatorname{tr}(BW)^3
=\sum_{k=1}^2(h_k^3+h_k^{-3})+3(h_i+h_i^{-1})\ge10.
\tag{8.3}
$$

For $i\ne j$, relabeling the two coordinates if necessary gives

$$
\operatorname{tr}(BW)^3
=(h_i+h_j^{-1})^3+h_j^3+h_i^{-3}.
\tag{8.4}
$$

Set $y=h_j$, $z=h_i^{-1}$, and $s=y+z$. Then

$$
h_i+h_j^{-1}=z^{-1}+y^{-1}=\frac{s}{yz}\ge\frac4s,
\qquad y^3+z^3\ge\frac{s^3}{4}.
\tag{8.5}
$$

Consequently

$$
\operatorname{tr}(BW)^3
\ge\frac{64}{s^3}+\frac{s^3}{4}\ge8.
\tag{8.6}
$$

Equality holds when $y=z=2^{1/3}$, equivalently
$h_j=2^{1/3}$ and $h_i=2^{-1/3}$. Finally,
$\operatorname{tr}B^3=10$ for every matrix unit, proving (8.2). ∎

We first take equal nonzero singular values. Scaling them to one, set

$$
B=2G=\begin{pmatrix}I&K\\K^*&I\end{pmatrix},
\qquad W=\operatorname{diag}(H,H^{-1}).
\tag{8.7}
$$

A common unitary diagonalizes $H=\operatorname{diag}(h_1,h_2)$ without
restricting the contraction $K$. Put $x_{ij}=|K_{ij}|^2$ and
$s=\sum x_{ij}$. Then

$$
N:=\operatorname{tr}B^3=4+6s,
\tag{8.8}
$$

while

$$
D:=\operatorname{tr}(BW)^3
=\sum_i(h_i^3+h_i^{-3})
+\sum_{i,j}3\left(\frac{h_i^2}{h_j}
+\frac{h_i}{h_j^2}\right)x_{ij}.
\tag{8.9}
$$

The matrix $X=(x_{ij})$ has every row and column sum at most one. The
$2\times2$ partial doubly stochastic polytope has seven vertices: the zero
matrix, four single matrix units, and two permutation matrices. Since
$D-\frac45N$ is affine in $X$, it suffices to check these vertices. The zero
vertex follows from $h^3+h^{-3}\ge2$. The single vertices follow from
Lemma 8.1. For the identity permutation,

$$
D=\sum_i(h_i^3+h_i^{-3}+3h_i+3h_i^{-1})\ge16.
\tag{8.10}
$$

For the transposition,

$$
D=\sum_i(h_i^3+h_i^{-3})+
3\left(\frac{h_1^2}{h_2}+\frac{h_2}{h_1^2}
+\frac{h_1}{h_2^2}+\frac{h_2^2}{h_1}\right)\ge16.
\tag{8.11}
$$

At either perfect matching $N=16$, so both inequalities are stronger than
$D\ge(4/5)N$. This proves Theorem 1.5(1), and the nilpotent single-edge
construction proves sharpness.

For the second stratum, let

$$
\Sigma=\operatorname{diag}(\sigma_1,\sigma_2)>0,\qquad
C=\operatorname{diag}(c_1,c_2),\qquad
Q=\Sigma C^{-1}\Sigma=\operatorname{diag}(q_1,q_2).
\tag{8.12}
$$

Thus $[C,\Sigma]=0$ and $c_iq_i=\sigma_i^2$. After removing the common
factor $2^{-3}$, the cubic traces are

$$
N=2\sum_i\sigma_i^3+
3\sum_{i,j}\sigma_i\sigma_j(\sigma_i+\sigma_j)x_{ij},
\tag{8.13}
$$

$$
D=\sum_i(c_i^3+q_i^3)+
3\sum_{i,j}(c_i^2q_j+c_iq_j^2)x_{ij}.
\tag{8.14}
$$

Again the difference is affine on the same seven-vertex polytope. At the zero
vertex, $D\ge2\sum_i\sigma_i^3=N$. At a diagonal single edge, the active
terms form $(c_i+q_i)^3$, so $D\ge N$. A nondiagonal single edge is exactly
the weighted chain of Section 7 and satisfies $D\ge(4/5)N$. The identity
matching gives $\sum_i(c_i+q_i)^3\ge N$. Finally, at the transposition,

$$
D=(c_1+q_2)^3+(c_2+q_1)^3,
\tag{8.15}
$$

and

$$
(c_1+q_2)(c_2+q_1)
\ge(\sigma_1+\sigma_2)^2.
\tag{8.16}
$$

Therefore $D\ge2(\sigma_1+\sigma_2)^3=N$, completing the seven checks and
proving Theorem 1.5(2).

For an original decomposition, the factor in Theorem 1.5(2) is not arbitrary:
with $P$ from (6.2), it is

$$
C=(U^*P^\dagger U)^{-1}.
\tag{8.17}
$$

Accordingly, the theorem applies when this induced compressed factor commutes
with $\Sigma$, or when an inner minimizing factor for fixed $(\Sigma,K)$ can be
chosen to commute. It does not assert that normality of $T$, commutativity of
$|T|$ and $|T^*|$, or the existence of an unrelated commuting matrix is
sufficient.

## 9. The partial exponent--dimension--rank phase diagram

The preceding results yield the following rigorous picture.

- In dimension two, every finite interior exponent is solved exactly by
  Theorem 1.1.
- In arbitrary ambient dimension with rank-two sum, the quadratic exponent is
  solved exactly by Theorem 1.3.
- For every $1<p<2$, the nilpotent curve $L_p$ fails in some finite dimension;
  the true sharp constant is not determined here.
- For $p=3$, the equal-singular-value stratum and the commuting compressed-factor
  stratum satisfy the candidate bound, but the simultaneous non-scalar,
  noncommuting stratum remains open.
- The operator-norm endpoint $c_\infty^{\rm sym}(m,n)=\sqrt2$ for $n\ge3$ is
  previously known from Zhang and is used only as background.

This is not a complete rank-two Schatten phase diagram. In particular, no
interpolation argument presently upgrades the two cubic strata to all finite
$p>2$, and the compressed-factor condition in Theorem 1.5(2) is not intrinsic
to $T$. At arbitrary rank, even the complete three-dimensional Frobenius problem
remains outside the present results.

## 10. Scope, checks, and limitations

Theorem 1.1 determines the complete $n=2$ layer of (1.2) for
$1<p<\infty$. Its one-variable maximum is an exact formula; it is not a claim that
the maximizing point has an elementary radical expression for every real $p$.
Theorem 1.3 determines the Frobenius constant in arbitrary ambient dimension only
under the hypothesis $\operatorname{rank}T\le2$. It does not settle the complete
three-dimensional Frobenius problem or any arbitrary-rank higher-dimensional layer.

Theorem 1.4 is a separation theorem rather than a sharp-constant theorem. For each
fixed $1<p<2$ it gives some finite-dimensional example above $L_p$, with dimensions
that may depend on $p$; it neither identifies the true constant nor supplies one
finite pair $(n,m)$ valid for the entire interval. Theorem 1.5 proves the cubic
candidate bound only on the two stated Gram strata. In particular, the simultaneous
non-scalar, noncommuting rank-two core remains open, as does the full finite-$p>2$
rank-two problem. The known operator-norm endpoint from [2] is not claimed as a new
result here. Nor do we assert a single constant simultaneously sharp for all
unitarily invariant norms.

The internal research record contains separate symbolic and numerical regression
checks for the two-dimensional frontier and elimination, the rank-two Gram
compression, the Frobenius outer inequality, the subquadratic dimension-amplification
construction, the weighted-chain transition, and the two cubic strata. These checks
include positive controls, destructive controls, and bounded counterexample searches.
They guard the displayed formulas and proof reductions; they are not substitutes for
the general arguments in Sections 2--8. In particular, finite searches and the
unpublished analysis of the remaining noncommuting cubic core support no claim in
this manuscript.

The literature comparison used the public sources listed below, including
arXiv:2603.01046v1, both available Bourin--Lee preprints [1,6], the
Aouichaoui--Lee preprint [7], and the public MI-09 record [3]. No direct coverage of
Theorems 1.1, 1.3, 1.4, or 1.5 was found in those accessible versions. This is a
bounded source statement, not a proof of worldwide priority. The full texts of the
version of record of [2] and the Proceedings version of [1] were not accessible
during preparation. Their possible differences from the public preprints remain a
source risk to be revisited when an author manuscript or accessible version becomes
available. Accordingly, this manuscript makes no global-priority claim and does not
claim a complete solution of MI-09.

## AI-assisted research and writing

Carptopus used OpenAI Codex to assist with mathematical exploration, proof checking,
literature comparison, computational regression checks, and manuscript preparation.
Carptopus is responsible for the statements, source attribution, and final manuscript.
This preprint has not undergone external peer review.

## References

1. Jean-Christophe Bourin and Eun-Young Lee, *Triangle inequalities for the
   operator symmetric modulus*, arXiv:2602.19607v1, 23 February 2026;
   *Proceedings of the American Mathematical Society* (2026),
   DOI 10.1090/proc/17861. https://doi.org/10.1090/proc/17861
2. Teng Zhang, *Operator symmetric moduli and sharp triangle inequalities*,
   arXiv:2603.01046v1, 1 March 2026; *Journal of the London Mathematical Society*
   **114**(2) (2026), e70672. https://doi.org/10.1112/jlms.70672
3. Open Problems in Numerical Linear Algebra, MI-09, *Arithmetic symmetric
   modulus: optimal constants for Schatten norms*, public problem record,
   accessed 14 October 2026.
   https://github.com/ajt60gaibb/OpenProblemsInNLA/tree/main/matrix-inequalities-and-norms/MI-09
4. Alfred Horn, *Doubly stochastic matrices and the diagonal of a rotation
   matrix*, *American Journal of Mathematics* **76** (1954), 620--630.
   https://doi.org/10.2307/2372705
5. Yong Xia, Shu Wang, and Ruey-Lin Sheu, *S-lemma with equality and its
   applications*, *Mathematical Programming* **156** (2016), 513--547.
   https://doi.org/10.1007/s10107-015-0907-0
6. Jean-Christophe Bourin and Eun-Young Lee, *Some hybrid matrix triangle
   inequalities*, arXiv:2606.29188v1, 28 June 2026.
   https://arxiv.org/abs/2606.29188
7. Mohamed Amine Aouichaoui and Eun-Young Lee, *Solutions to some open problems
   in matrix analysis*, arXiv:2609.20094v2, 21 September 2026.
   https://arxiv.org/abs/2609.20094


