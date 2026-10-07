# Parallel-support transfer and sparse paving quotients in a one-sided Merino–Welsh inequality

Carptopus

7 October 2026 · Version 0.1-beta

Preprint. External mathematical review and formal peer review are pending.

## Abstract

Write \(b(M)=T_M(1,1)\) for the number of bases of a finite matroid. We prove a conditional transfer theorem for the specified-side inequality \(T_M(0,2)\ge b(M)\). Let \(M\) be loopless and coloopless, and let \(F\) be a flat spanned by parallel classes of size at least \(k\ge2\). For a nonempty quotient \(Q=M/F\), put \(s=|E(Q)|-r(Q)\) and let \(g(Q)\) be its girth. If \(T_Q(0,2)\ge b(Q)\) and \(2^k-1-k\ge s/g(Q)\), then the same inequality holds for \(M\); strictness of the quotient inequality transfers as well. Neither independence of the parallel directions nor representability is required. We also prove the strict inequality when the flat spanned by all nontrivial parallel classes has corank two and its quotient has two disjoint bases. Together with the previously published corank-at-most-one result, these theorems yield the specified-side inequality whenever a parallel-spanned flat has a loopless, coloopless sparse paving quotient of rank \(c\) and size \(m\ge2c\), for every \(c\ge1\). A classical multitheta graph family shows why a fixed parallel multiplicity cannot suffice for all quotients and calibrates the transfer budget. The results concern these structural classes, not the full Merino–Welsh conjecture.

## 1. Scope and principal results

All matroids in this paper are finite. A *nontrivial parallel class* is a maximal parallel class with at least two elements, and all parallel classes mentioned below are maximal. A flat *spanned by parallel classes of size at least k* means that the union of some such classes spans the flat; the flat may contain additional elements. In particular, the designated classes need not be independent and need not include every nontrivial parallel class of the original matroid. Empty spanning families are allowed and span the empty flat in a loopless matroid.

We use the rank-function definition

\[
T_M(x,y)=\sum_{A\subseteq E(M)}(x-1)^{r(M)-r_M(A)}(y-1)^{|A|-r_M(A)},
\qquad b(M)=T_M(1,1).
\]

The number \(T_M(0,2)\) is nonnegative, as follows, for example, from the nonnegative coefficients of the Tutte polynomial. For a graph's cycle matroid it counts totally cyclic orientations. The focus here is the specified side \(T_M(0,2)\), not an inference of that side from a maximum or a product of the two evaluations \(T_M(2,0)\) and \(T_M(0,2)\).

### Theorem 1.1

Let \(M\) be loopless and coloopless. Let \(F\) be a flat spanned by parallel classes of size at least \(k\ge2\). Suppose that \(Q=M/F\) is nonempty and satisfies \(T_Q(0,2)\ge b(Q)\). Put \(s=|E(Q)|-r(Q)\). If

\[
2^k-1-k\ge\frac{s}{g(Q)}, \tag{1}
\]

then \(T_M(0,2)\ge b(M)\). If \(T_Q(0,2)>b(Q)\), then \(T_M(0,2)>b(M)\). For the empty quotient the same conclusions hold with the non-strict premise \(T_Q(0,2)=b(Q)=1\) and budget zero.

The quotient is loopless because \(F\) is a flat, and is coloopless because contraction preserves absence of coloops. Thus its girth is finite when it is nonempty. The quotient premise in this theorem is indispensable: the numerical budget alone is not asserted to pay for a quotient that fails the specified-side inequality. Nor is strictness claimed merely from strictness of (1) or from \(F\ne\varnothing\); direct sums of copies of \(U_{1,2}\) can have equality.

### Theorem 1.2

Let \(M\) be loopless and coloopless, let \(P\) be the union of all its nontrivial parallel classes, and let \(G=\operatorname{cl}_M(P)\). If \(r(G)=r(M)-2\) and \(M/G\) has two disjoint bases, then

\[
T_M(0,2)>b(M). \tag{2}
\]

### Theorem 1.3

Let \(M\) be loopless and coloopless, and let \(F\) be a flat spanned by nontrivial parallel classes. If \(Q=M/F\) is loopless, coloopless and sparse paving of rank \(c\ge1\), with \(m=|E(Q)|\ge2c\), then \(T_M(0,2)\ge b(M)\).

Here sparse paving means that both the matroid and its dual are paving; a paving matroid has no circuit smaller than its rank. In particular Theorem 1.3 includes every uniform quotient \(U_{c,m}\) with \(m\ge2c\). It imposes no bound on \(r(M)\), \(r(F)\), parallel multiplicities, or dependencies between the designated directions.

### 1.1. Relationship to earlier work

The earlier parallel-support theorem [1] proves the specified-side inequality when \(r(P)\ge r(M)-1\), with additional strictness and equality information. We use only its non-strict conclusion and cite it as a dependency. Theorem 1.2 addresses the next corank with a two-disjoint-bases hypothesis. It is included with its proof here rather than treated as a separately published dependency. Theorem 1.3 does not subsume all of Theorem 1.2: a rank-two quotient of arbitrary size with two disjoint bases need not be sparse paving. Conversely, Theorem 1.3 treats quotients of every rank, and Theorem 1.1 is a conditional mechanism not restricted to sparse paving quotients. These complementary statements are presented together.

Uniform specified-side inequalities appear in [2]. Paving convexity in [3], the sparse paving Tutte formula in [4], and split-matroid inequalities in [5] already supply relevant quotient endpoints. Parallel-class recurrences are standard; [4] discusses thickening, and [6] gives such recurrences in the Merino–Welsh setting. We do not claim those recurrences, the balanced sparse paving endpoint, or the multitheta graph construction to be new. The contribution claimed here is the transfer through an arbitrary parallel-spanned flat with the explicit quotient budget, together with the structural conclusions for the original matroid in Theorems 1.2 and 1.3.

The hypotheses constrain the quotient and parallel support, not automatically the original matroid's density, circuit lengths, or lattice of cyclic flats. The source comparison underlying this manuscript examined [2]–[7] and related weighted-activity work. It found no direct statement covering the complete transfer or the complete original-matroid class asserted here. This is a bounded prior-art assessment, not a guarantee of global priority or of the absence of an implicit consequence of other literature. No theorem here asserts the full Merino–Welsh conjecture or the specified-side inequality for all matroids with two disjoint bases.

## 2. Parallel-class recurrences and closure facts

For a parallel class \(X\) of size \(t\), choose a representative \(e\) and set

\[
H=M\setminus(X\setminus\{e\}),\qquad D=H\setminus e=M\setminus X,
\qquad C=(M/e)\setminus(X\setminus\{e\}). \tag{3}
\]

The notation \(M/X\) below denotes this last matroid on \(E(M)\setminus X\): contracting the entire class and discarding its elements has exactly this effect. Since the class is maximal, the only loops created by contracting a representative are its remaining copies. Thus \(C\) is loopless. Contraction and subsequent deletion of loops preserve absence of coloops.

If \(e\) is not a coloop of \(H\), repeated deletion–contraction gives

\[
T_M(x,y)=T_D(x,y)+(1+y+\cdots+y^{t-1})T_C(x,y),
\]
\[
T_M(0,2)=T_D(0,2)+(2^t-1)T_C(0,2),
\qquad b(M)=b(D)+t b(C). \tag{4}
\]

Indeed, the contraction term when a new copy is inserted has its other copies as loops, contributing the successive powers of \(y\). The formula also covers a singleton class \(t=1\) when its representative is ordinary. Writing \(\delta(N)=T_N(0,2)-b(N)\), it implies

\[
\delta(M)=\delta(D)+(2^t-1)\delta(C)+(2^t-1-t)b(C). \tag{5}
\]

If \(e\) is a coloop of \(H\), then \(X\) is a cocircuit of \(M\). No circuit can meet \(X\) in just one element; a circuit meeting it in two elements must be that parallel pair. Hence \(X\) is a component and

\[
M=C\oplus U_{1,t},\qquad T_{U_{1,t}}(0,2)=2^t-2,
\qquad b(U_{1,t})=t. \tag{6}
\]

For \(t\ge2\), the factor satisfies \(2^t-2\ge t\). We use (6), not (4), in this branch.

We will repeatedly use the following closure facts. If a flat is spanned by designated large parallel classes, contraction of an internal maximal class, followed by removal of its loops, leaves a flat spanned by the images of the remaining designated classes. Classes not parallel to the contracted direction do not become loops; merges only increase their sizes. The quotient by the resulting flat is unchanged. If an internal class is redundant relative to the designated spanning classes, deleting the entire class preserves the flat's rank and quotient. The remaining designated classes provide a replacement for every internal element in a basis of the flat. With a coloopless quotient, this also excludes coloops in the deletion: internal elements have replacements within the flat, and any external coloop would induce a quotient coloop. The marked flat after deletion is its intersection with the remaining ground set, not the original set with deleted elements still attached.

## 3. Proof of the conditional transfer theorem

### Proof

We prove Theorem 1.1 by strong induction on \(|E(M)|\), including the assertion that strictness of the quotient inequality transfers. If \(F=\varnothing\), the result is the quotient premise itself. Fix designated classes of size at least \(k\) spanning \(F\). Contracting any internal maximal class as in (3) preserves the quotient and its parameters \(s,g(Q)\), and yields a smaller loopless, coloopless matroid satisfying the hypotheses. This proves the required non-strict or strict inequality for \(C\) by induction.

Suppose first that \(F\) contains a maximal class \(X\) not among the designated classes; its size \(t\) can be one. The designated classes still span after deleting all of \(X\). The deletion \(D\) is loopless and coloopless and has the same quotient, by the closure facts in Section 2. In particular, \(X\) is not a cocircuit and (5) applies. Both smaller minors satisfy the induction hypotheses; \(2^t-1-t\ge0\). Consequently (5) proves the assertion, and if the quotient inequality is strict, the positive coefficient of \(\delta(C)\) preserves strictness.

After these extra classes have been removed, if the remaining designated directions are dependent, choose a direction in a circuit of their simplification and delete its whole class. The other designated classes still span the marked flat. The same deletion argument and (5) apply. Thus it remains to prove the assertion when the marked flat consists solely of independent parallel classes of size at least \(k\).

Choose one such class \(X\), of size \(t\ge k\). If it is a cocircuit, (6) and the induction hypothesis for \(C\) prove the assertion, including quotient strictness. Otherwise \(e\) is not a coloop of \(H\), and \(r(D)=r(H)=r(M)\). Put \(L=E(M)\setminus F\), \(m=|L|\) and \(c=r(Q)\), so \(s=m-c\).

For a basis \(B\) of \(D\), let \(\Gamma\) be the fundamental circuit of \(e\) in \(B\cup\{e\}\) in \(H\). The internal classes are independent, and the other internal directions have rank \(r(F)-1\), so \(\Gamma\) cannot lie entirely in \(F\). Its internal part \(\Gamma_F=\Gamma\cap F\) is a proper subset of a circuit and hence independent. Submodularity applied to \(F\) and \(\Gamma\) yields

\[
r_H(F\cup\Gamma_L)\le r_H(F)+r_H(\Gamma)-r_H(\Gamma_F)
=r_H(F)+|\Gamma_L|-1,
\quad \Gamma_L=\Gamma\setminus F. \tag{7}
\]

Thus \(\Gamma_L\) is dependent in \(Q\), and \(|\Gamma_L|\ge g(Q)\). For every \(j\in\Gamma_L\), \(B\setminus\{j\}\) is a basis of \(C\). The map

\[
(B,j)\longmapsto(B\setminus\{j\},j)
\]

is injective. Each basis of \(C\) uses at least \(c\) elements of \(L\), because its internal elements have rank at most \(r(F)-1\). There are at most \(s\) unused elements of \(L\). Counting these pairs gives

\[
g(Q)b(D)\le s b(C). \tag{8}
\]

Importantly, this count is used only in the independent terminal configuration. Its deletion \(D\) has internal flat rank \(r(F)-1\), and its quotient is not asserted to be \(Q\). No induction on this terminal deletion with the original quotient is used.

By (4), the complete difference is

\[
\delta(M)=T_D(0,2)-b(D)+(2^t-1)\delta(C)
+(2^t-1-t)b(C).
\]

Using (8) and \(T_D(0,2)\ge0\), we obtain

\[
\delta(M)\ge T_D(0,2)+(2^t-1)\delta(C)
+\left(2^t-1-t-\frac{s}{g(Q)}\right)b(C)\ge0. \tag{9}
\]

Here \(2^t-1-t\) increases for integer \(t\ge2\), and the induction hypothesis gives \(\delta(C)\ge0\). A strict quotient gives \(\delta(C)>0\), and its coefficient is positive.

When \(Q\) is empty, \(F=E(M)\). The same redundant-class reductions apply with budget zero. In the independent terminal configuration every internal class is a rank-one component, so (6) finishes the argument. This proves all assertions. ∎

## 4. The general corank-two structural theorem

We use the previously published theorem [1]: if a loopless, coloopless matroid \(N\) has parallel-support rank at least \(r(N)-1\), then \(T_N(0,2)\ge b(N)\). This section proves Theorem 1.2 without assuming its conclusion as a dependency.

### Proof

Use strong induction on the ground-set size in the class of Theorem 1.2. Write \(h=r(G)\), \(Q=M/G\). When an internal nontrivial class \(X\) is contracted as in (3), the remaining original heavy classes span \(G/X\), of rank \(h-1\). The rank of all new heavy classes is at least \(h-1\). If it is larger, the contracted matroid falls within [1]; if it equals \(h-1\), its heavy closure is precisely \(G/X\), and its quotient is \(Q\). It therefore falls within the current corank-two induction. In either case \(T_C(0,2)\ge b(C)>0\). A cocircuit class is a component and (6) preserves the strict induction conclusion for \(C\), whose rank-two quotient is unchanged.

For a class that is not a cocircuit, reducing its multiplicity to two gives a smaller matroid in the same class, with the same parallel-support rank and quotient. By (4), increasing multiplicity from \(j\) to \(j+1\) changes \(\delta\) by

\[
2^j T_C(0,2)-b(C)>0\quad(j\ge2). \tag{10}
\]

Thus it suffices to treat the case where all nontrivial classes are pairs. Designated copies of a basis of \(G\) provide two disjoint bases of \(G\), and these lift with two disjoint quotient bases to two disjoint bases of \(M\).

If \(G\) contains a singleton \(e\), deleting it retains the two lifted bases and the original parallel support and quotient. Contracting it creates no loops; its original heavy support has rank \(h-1\), so the contraction is controlled by [1] or by the same corank-two induction as above. Deletion–contraction then gives strictness. We may therefore assume that \(G\) consists only of the heavy pairs.

If \(Q\) has more than four elements, fix its two disjoint bases and choose an element \(e\) outside their union. It is an external singleton in \(M\). Deleting it preserves those bases and the corank-two hypothesis; contracting it is loopless and coloopless and leaves the original heavy support of rank \(h=r(M/e)-1\), so [1] applies. Again the sum is strict. We may assume there are exactly four external singletons.

If the simplified heavy directions are dependent, delete an entire class whose direction belongs to a circuit. The other heavy classes still span \(G\), with the same quotient and two lifted bases. The deletion has a strictly positive difference by induction; the contraction has a nonnegative difference as already shown. Equation (5) proves strictness. Hence only the independent heavy-direction configuration remains.

Let \(N\) be the simplification of this terminal matroid, with ground set \(A\sqcup L\), where \(|A|=h\), \(|L|=4\), and \(r(N)=h+2\). Its dual \(K=N^*\) has rank two. All possible coloop representatives in \(A\) have already been treated by the component branch, and external elements cannot be coloops since the two lifted bases avoid each element. Thus \(K\) is loopless.

Number the parallel classes of \(K\), and let \(a_i,l_i\) be their numbers of elements from \(A,L\). Then \(\sum_i a_i=h\), \(\sum_i l_i=4\). The identity \(K|L=(N/A)^*=Q^*\), and the two complementary quotient bases, imply \(l_i\le2\). The nonzero light-class patterns are therefore

\[
(2,2),\qquad(2,1,1),\qquad(1,1,1,1).
\]

Let \(t=2,3,4\) denote the number of light-containing classes. A basis of \(K\) consists of two elements in distinct classes. Its complement is a basis of \(N\); every retained heavy representative lifts in two ways. It follows that

\[
b(M)=2^h\sum_{i<j} w_iw_j,\qquad w_i=l_i+\frac{a_i}{2}. \tag{11}
\]

The subset expansion at \((0,2)\), aggregating the three nonempty selections in each heavy pair, gives

\[
T_M(0,2)=\sum_{S\subseteq A,\ Z\subseteq L}
3^{|S|}(-1)^{r(N)-r_N(S\cup Z)}.
\]

For \(Y=(A\sqcup L)\setminus(S\cup Z)\), duality changes the exponent to \(|Y|-r_K(Y)\). Give heavy elements weight \(-1/3\) and light elements weight \(-1\). Rank-one nonempty subsets are exactly the subsets contained in one parallel class; rank-zero is the empty subset; all other subsets have rank two. The sum of all subset weights is zero because of the light elements. Correcting the signs of rank-one subsets thus gives

\[
T_M(0,2)=2\,3^h\left[t+\sum_{l_i=0}\left(1-(2/3)^{a_i}\right)\right]. \tag{12}
\]

For completeness, the correction is minus twice the sum, over classes, of their nonempty subset weights. A light-containing class has total nonempty weight \(-1\); a pure-heavy class has total nonempty weight \((2/3)^{a_i}-1\). This proves (12) without representability assumptions.

The three light patterns satisfy \(\sum_{i<j}l_i l_j=t+2\). Expanding (11),

\[
\sum_{i<j}w_iw_j
=t+2+\frac12\sum_i a_i(4-l_i)+\frac{h^2-\sum_i a_i^2}{8}
\le t+2+2h+\frac{h^2}{8}. \tag{13}
\]

By (12), \(T_M(0,2)/2^h\ge2t(3/2)^h\). For \(h\ge2\),

\[
4(3/2)^h>4+2h+h^2/8. \tag{14}
\]

At \(h=2\) the difference is \(1/2\). Its successive increment is \(2(3/2)^h-2-(2h+1)/8\), positive at \(h=2\) and increasing since its own increment is \((3/2)^h-1/4>0\). Increasing \(t\) above two raises the left bound by more than the right bound, so (13)–(14) prove strictness for every \(t\).

For \(h=1\) and \(t\ge3\), the same bounds are strict directly. If \(h=1,t=2\), placing the heavy element in a light-containing class gives normalized values \(b(M)/2^h=5\) and \(T_M(0,2)/2^h=6\). Placing it in a pure-heavy class gives 6 and 7. Finally, \(h=0\) leaves a simple rank-two matroid on four elements, namely \(U_{2,4}\), with \(8>6\). These exhaust the terminal configurations and finish the induction. ∎

## 5. Sparse paving quotients of every rank and size

### 5.1. The balanced endpoint

Let \(Q\) be loopless and coloopless sparse paving of rank \(c\) on \(2c\) elements. For \(c\ge2\), let \(\ell\) be the number of its circuit-hyperplanes. The standard sparse paving formula [4] is

\[
T_Q(x,y)=T_{U_{c,2c}}(x,y)+\ell(xy-x-y). \tag{15}
\]

Indeed only those nonbasis \(c\)-subsets have ranks differing from the uniform matroid; each contributes \((x-1)(y-1)-1=xy-x-y\). The uniform polynomial has no mixed terms and is self-dual. Since \(T_{U_{c,2c}}(2,2)=2^{2c}\), it follows that

\[
b(Q)=\binom{2c}{c}-\ell,
\qquad T_Q(0,2)=2^{2c-1}-2\ell. \tag{16}
\]

Different circuit-hyperplanes intersect in at most \(c-2\) elements, so every \((c-1)\)-subset belongs to at most one. Therefore

\[
\ell\le\frac1c\binom{2c}{c-1}=\frac{1}{c+1}\binom{2c}{c}.
\]

For integers \(c\ge2\),

\[
2^{2c-1}\ge\frac{c+2}{c+1}\binom{2c}{c}. \tag{17}
\]

To check this, put \(R_c=2\binom{2c}{c}(c+2)/((c+1)4^c)\). Then \(R_2=1\) and

\[
\frac{R_{c+1}}{R_c}=\frac{(2c+1)(c+3)}{2(c+2)^2}<1.
\]

Equations (16)–(17) imply \(T_Q(0,2)\ge b(Q)\), strictly for \(c\ge3\). For \(c=1\), \(Q=U_{1,2}\) and both evaluations are two. These endpoint inequalities are known consequences of earlier results, including [3] combined with (15); the calculation is included to make the side used in Theorem 1.1 explicit.

For \(c\ge2\), \(g(Q)\ge c\), while \(s=c\). Thus \(s/g(Q)\le1=2^2-1-2\); for \(c=1\) the ratio is \(1/2\). Theorem 1.1 applies with \(k=2\), proving Theorem 1.3 when \(m=2c\).

### 5.2. Low-rank endpoints and minor closure

We now prove Theorem 1.3 by strong induction on \(|E(M)|\). For \(c=1\), the union of all original heavy classes has rank at least \(r(F)=r(M)-1\), so [1] applies.

For \(c=2\), let \(G\) be the flat spanned by all original nontrivial parallel classes. It contains \(F\) and has rank at least \(r(M)-2\). If its rank is larger, [1] applies. Otherwise the inclusion of flats with equal rank gives \(G=F\). A coloopless paving matroid of rank \(c\) and size at least \(2c\) has two disjoint bases, by [3, Theorem 4.1]. Thus the rank-two quotient satisfies Theorem 1.2. This argument includes the empty-flat case and does not assume that arbitrary contraction preserves two disjoint bases.

Take \(c\ge3\). The balanced case was proved in Section 5.1, so suppose \(m>2c\). Sparse paving matroids are minor-closed: deletion of a paving matroid remains paving, and contraction cannot create a circuit smaller than the new rank; apply duality to get both properties for both minors. Here \(g(Q)\ge c\ge3\) and its cogirth is at least \(m-c\ge c+1\ge4\). Thus \(Q\) is simple and has no two-element cocircuit. For any external element \(e\), the minors \(Q\setminus e\) and \(Q/e\) are loopless and coloopless, are sparse paving, and have respectively rank/size

\[
(c,m-1),\qquad(c-1,m-1),
\]

both satisfying the required size-at-least-twice-rank condition.

Set \(D=M\setminus e\), \(C=M/e\). Simplicity of \(Q\) implies that \(e\) is a singleton class in \(M\), so \(C\) is loopless; it is coloopless by contraction. The flat \(F\) retains its rank in \(D\). The surviving heavy classes give internal replacements, and any external coloop of \(D\) would induce a coloop of \(Q\setminus e\); hence \(D\) is also coloopless.

Because \(e\notin\operatorname{cl}_M(F)=F\), contracting \(e\) leaves the rank function on subsets of \(F\) unchanged. The designated classes continue to span \(F\) in \(C\), and the quotient \(Q/e\) being loopless ensures that \(F\) is still a flat. In \(D\) the same spanning and flat conditions hold. We have

\[
D/F=Q\setminus e,\qquad C/F=Q/e.
\]

Both original minors have smaller ground sets and satisfy the induction hypotheses. Ordinary deletion–contraction adds their nonnegative differences and proves Theorem 1.3. ∎

## 6. A classical graph family calibrating the budget

Let \(k\ge2\), \(c\ge2\). Form a graph with \(k\) parallel edges between vertices \(u,v\) and \(c\) internally disjoint paths \(u,w_i,v\), each of length two. Let \(M\) be its cycle matroid and \(F\) its \(u,v\) parallel class. Then \(F\) is a flat, and

\[
Q=M/F=\bigoplus_{i=1}^{c}U_{1,2},\qquad s=c,\quad g(Q)=2,
\quad T_Q(0,2)=b(Q)=2^c.
\]

The spanning trees either use one parallel edge and one edge from every path, or use no parallel edge and one whole path. Consequently

\[
b(M)=k2^c+c2^{c-1}=(2k+c)2^{c-1}. \tag{18}
\]

In a totally cyclic orientation, every length-two path is consistently directed between \(u,v\). Mixed parallel-edge directions give \((2^k-2)2^c\) orientations; uniform parallel-edge directions require at least one oppositely directed path, giving \(2(2^c-1)\). Therefore

\[
T_M(0,2)=2^{k+c}-2,
\quad \delta(M)=(2^{k+1}-2k-c)2^{c-1}-2. \tag{19}
\]

Put \(A=2^{k+1}-2k\). The sufficient condition (1) allows \(c\le A-2\). This family satisfies the inequality exactly for \(c\le A-1\), and fails it strictly for \(c\ge A\). Indeed at \(c=A-1\) the difference is \(2^{A-2}-2\ge0\), whereas for \(c\ge A\) it is negative; for smaller \(c\ge2\) it remains nonnegative. Thus the sufficient cutoff and this family's failure cutoff differ by one intermediate integer value of \(c\), or an additive constant in the budget \(s/g\). This does not prove a universally optimal cutoff.

For every fixed \(k\) the family has failing examples at sufficiently large \(c\); a uniform guarantee for all such quotients therefore needs at least logarithmic growth of the permitted multiplicity as a function of \(c\). The graph has two-element cocircuits, so it is not a cosimple counterexample to the hypothesis in [2, Conjecture 4.2]. Nor does failure of this specified side contradict the graph maximum formulation: directly \(T_M(2,0)=2\cdot3^c\). The construction is classical and serves here as a boundary check, not a claimed new graph family.

## 7. Verification and limitations

The general quantifiers in Theorems 1.1–1.3 are justified by the proofs, not by enumeration. Supplementary Python checks evaluate seven fixed small represented matroids directly from their rank functions, testing parallel-support hypotheses and the Tutte evaluations. They use the earlier, more conservative budget \(2^k-1-k\ge s/2\), rather than testing the full girth refinement. They include positive cases and the \(k=2,c=4\) multitheta negative control with \(T_M(0,2)=62<64=b(M)\), which rules out dropping the budget altogether. The supplementary scripts document their own finite coverage and resource limits; no finite absence of counterexamples is used as a general existence or nonexistence statement.

The assertions leave several boundaries open. Theorem 1.1 needs a separately justified quotient inequality. Theorem 1.3 does not cover all paving quotients, arbitrary rank-two quotients unless Theorem 1.2 applies, or unrestricted two-base matroids. The graph family calibrates but does not establish the best universal transfer threshold. Independent project audits are distinct from external expert verification and formal peer review.

## AI-assisted research disclosure

AI tools assisted with proof exploration, adversarial checking, literature comparison, computational verification, and manuscript preparation. Carptopus is the responsible author. The statements and limitations above define the scope of the preprint.

## References

[1] Carptopus. *Parallel-support rank and a one-sided Merino–Welsh inequality*. Version 0.1-beta, 2026. https://doi.org/10.5281/zenodo.22296382

[2] M. Ibañez, C. Merino, and M. G. Rodríguez. *A note on some inequalities for the Tutte polynomial of a matroid*. Author manuscript, 2008. https://www.matem.unam.mx/~merino/online_papers/inequal_matroid.pdf

[3] L. E. Chávez-Lomelí, C. Merino, S. D. Noble, and M. Ramírez-Ibáñez. *Some inequalities for the Tutte polynomial*. European Journal of Combinatorics 32 (2011), 422–433. https://arxiv.org/abs/1004.2639

[4] C. Merino, M. Ramírez-Ibáñez, and G. Rodríguez Sánchez. *The Tutte polynomial of some matroids*. arXiv:1203.0090, 2012. https://arxiv.org/abs/1203.0090

[5] L. Ferroni and B. Schröter. *The Merino–Welsh conjecture for split matroids*. Annals of Combinatorics 27 (2023), 737–748. https://doi.org/10.1007/s00026-022-00628-w

[6] K. Knauer, L. Martínez-Sandoval, and C. Merino. *Merino–Welsh inequalities for matroids with controlled lattices of cyclic flats*. arXiv:2609.38047v1, 2026. https://arxiv.org/abs/2609.38047

[7] J. P. S. Kung. *Inconsequential results on the Merino–Welsh conjecture for Tutte polynomials*. Australasian Journal of Combinatorics 79 (2021), 12–15. https://arxiv.org/abs/2105.01825
