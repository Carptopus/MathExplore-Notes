# Domination, component spectra, and sharp augmentation losses in matroid base-intersection graphs

Carptopus

8 October 2026 · Version 0.1-beta · Preprint; external mathematical review and formal peer review are pending

## Abstract

Let J(M) have the bases of a finite matroid M as vertices, with distinct bases adjacent when they intersect. For rank R at least two, we determine the minimum number of bases needed to augment any prescribed nonempty family to at most k components. A coverage-normalization theorem then expresses the global k-component domination number through the sizes and independent partition numbers of cocircuits. It also gives the complete, gap-free component spectrum of minimum dominating families. We distinguish global reoptimization from augmenting the best minimum dominating family, determine the sharp worst-case loss of the latter strategy, and realize it in graphic matroids and in an infinite family of simple binary matroids. Paving matroids and simple Fano-minor-free binary matroids have zero strategy loss. A dynamic program computes the global optimum and constructs an optimal family from an explicit laminar capacity tree. A classical hidden-circuit-hyperplane example explains why that input contract cannot be replaced by an independence oracle without an exponential deterministic query cost. Standard matroid partition, union, density bounds, and rank-two graph endpoints are credited as background; the comparison with prior work is bounded and includes specified unavailable sources.

## 1. Introduction and scope

Connecting a dominating set while retaining its original vertices is different from choosing a new dominating set. In a matroid base-intersection graph these two tasks admit exact formulas, but their optima need not coincide. Even after optimizing over all minimum dominating families, augmentation can be arbitrarily more expensive than global reoptimization.

The central ingredient is a replacement procedure which preserves a covered element set and the number of selected bases, while reducing the number of components one at a time. This leads to a cocircuit optimization formula and a complete spectrum theorem. We then study when the augmentation strategy is optimal, how badly it can fail, and how the formula becomes an algorithm under a specified input representation.

The graph used throughout is neither the usual single-element basis-exchange graph nor the graph in which disjoint bases are adjacent. In particular, coloring results for the latter graph do not by themselves determine our domination parameters. Base-intersection graphs occur in the Hamilton-cycle literature [ZY13, ZC18]; those results concern a different optimization problem.

All results below belong to one unified study. Complete-profile hypergraphs, uniform matroids, and rank-two matroids are explicit specializations, not separate general theorems. The independent partition and union theorems [EF65, FJ18], the paving partition criterion [BSY21], and the Fano-exclusion growth bound [Mur76, McG12, Ox11] are classical inputs. We do not claim new versions of those tools or of the standard hidden-matroid oracle argument [HLL22].

### 1.1 Prior-work and review boundary

The ordinary edge-domination problem in complete multipartite graphs was studied by Song et al. [SM14]. Rank-two ordinary domination and its connected endpoint are therefore not asserted here as new; the latter also follows from classical connected edge-domination interfaces [HM19]. Likewise, the rank-two equality between ordinary and independent domination follows from classical edge-domination results [YG80]. Our general spectrum and normalization results are stated for arbitrary finite matroids, with these endpoints included as examples.

The checked sources have not yielded direct coverage of the coverage-normalization theorem, its general spectrum consequence, or the constrained laminar cocircuit optimization. This is a bounded comparison, not a guarantee of global priority. In particular, the final identity and full text of the work cited in a 2012 matroid-graph chapter as Zhang–Liu, *On Properties of the Intersection Graphs of Matroids*, remain unresolved. The full text of Akkari's packing paper [Akk95], Song et al. [SM14], and certain later versions of adjacent laminar-optimization work have not all been examined. These gaps are listed in Appendix B. We do not represent inaccessible sources as having been excluded.

The manuscript is AI-assisted research. Its mathematical proofs, finite checks, novelty comparison, and external peer-review status are distinct. The manuscript has undergone independent project-level review; this is not a claim of external mathematical approval or formal peer review.

## 2. Definitions and classical tools

Let M be a finite matroid on E, of rank R>=2, with base set B(M) and b=|B(M)|. Loops may be deleted without changing its bases. A cocircuit is the complement of a hyperplane and contains no loop. Write r for the rank function.

For a nonempty family D of distinct bases, let U(D) be its union and c(D) the number of connected components in the induced graph J(M)[D]. Domination uses closed neighborhoods: a selected base dominates itself. Define

$$
q=\gamma(J(M)),\qquad
\gamma_c^k(J(M))=\min\{|D|:D\text{ dominates }J(M),\ c(D)\le k\},
$$

where k is any positive integer. When no ambiguity arises, write gamma_c^k for this parameter.

For a loopless nonempty element set X, let chi(X) be the smallest number of independent sets in a partition of X. Classical matroid partition and union give

$$
\chi(X)=\max_{\varnothing\ne Y\subseteq X}
\left\lceil\frac{|Y|}{r(Y)}\right\rceil,
\qquad
r_{M^{(t)}}(X)=\min_{Y\subseteq X}\{|X\setminus Y|+t r(Y)\}.
$$

Here M^(t) is the union of t copies of M. Its independent sets are precisely the sets partitionable into at most t independent sets of M. If M has t disjoint bases, its union matroid has rank tR. Consequently every set partitionable into t independent sets extends to the union of t disjoint bases. The original partition need not be retained. These are classical interfaces [EF65, FJ18].

The element–base incidence graph of D has |U(D)|+|D| vertices, R|D| edges, and c(D) components. Its cycle rank beta(D) is therefore

$$
\beta(D)=|D|(R-1)+c(D)-|U(D)|\ge0.                 \tag{2.1}
$$

Finally, D dominates J(M) if and only if E\U(D) contains no base, equivalently

$$
r(E\setminus U(D))<R,
\quad\text{or equivalently }U(D)\text{ contains a cocircuit}.       \tag{2.2}
$$

Indeed an undominated base is exactly a base disjoint from U(D); a set of rank below R extends into a hyperplane. Extending each class of a minimum independent partition of a cocircuit to a base, and conversely assigning covered cocircuit elements to selected bases, proves

$$
q=\min_{C\text{ cocircuit}}\chi(C).                 \tag{2.3}
$$

Deduplication of the extended bases cannot destroy coverage. Equation (2.3) is an application of the classical partition interface, not a new partition theorem.

## 3. Exact augmentation of a prescribed family

**Theorem 3.1.** For every nonempty family D of distinct bases and every k>=1, the minimum number of additional distinct bases required to obtain at most k components is

$$
\tau_k(D)=\max\left\{0,\left\lceil\frac{c(D)-k}{R-1}\right\rceil\right\}.       \tag{3.1}
$$

No domination hypothesis on D is required.

**Proof.** Unions of distinct components are disjoint. A new R-element base meets at most R current components, so each addition decreases their number by at most R−1. This proves the lower bound.

For the upper bound choose a<=R current components, each with a full-rank union. Select one representative element from each union, sequentially preserving independence. Before the i-th selection the chosen set has rank i−1<R; the next full-rank union cannot lie in its closure. Extend the independent representatives to a base. If a>=2 this base meets two current components and hence is not already selected. It merges at least a components. Whenever c>k take a=min(R,c−k+1). Repetition achieves the required bound. Representatives cannot be chosen arbitrarily: their sequential independence is essential. ∎

The matroid hypothesis is substantive. The six consecutive two-element edges on seven elements have intersection graph P_6. Its second and fifth vertices form a dominating set with two components, but retaining both requires adding the third and fourth vertices to connect it. Thus the rank-two-looking formula fails for general uniform hypergraphs.

## 4. Coverage normalization and global optimization

**Theorem 4.1 (coverage normalization).** Suppose a nonempty loopless set C is covered by m distinct bases. The bases can be replaced, preserving their number and coverage of C, so that the final component count is exactly

$$
\max\{1,|C|-m(R-1)\}.                             \tag{4.1}
$$

Each replacement operation below decreases the component count by exactly one until this value is reached.

**Proof.** Equation (2.1) gives |C|<=m(R−1)+c, proving the lower bound. Suppose c>1. Let U_1,U_2 be the disjoint unions of two components.

If U\C is nonempty, first choose e in U\C, let U_1 be the union of its component, and choose any other component union U_2. Simultaneously replace every base B in the first component containing e by B−e+f_B, where f_B is in U_2 but not in the closure of B−e. Such an element exists because U_2 has rank R and B−e has rank R−1. Always choose from the original U_2. The new bases are distinct: their R−1 subsets in U_1 are different; each new base meets both U_1 and U_2, whereas every untouched base lies in a single original component. All elements except e are retained. After deleting the incidence vertex e, every remaining piece of its former component contains a base previously incident with e; each such piece is attached to U_2 by its replacement. Thus exactly these two components merge, the union loses one element, and beta remains unchanged.

Otherwise the union is C. If beta>0, choose a cycle-containing component as U_1 and any other component as U_2, then choose an incidence edge (B,e) on that cycle. Removing that edge leaves the component connected and e still covered. Replace B by B−e+f with f in U_2 outside the closure of B−e. This base is distinct from all other bases, coverage and the union are unchanged, two components merge, and beta decreases by one.

The same second operation is available whenever beta>0, whether or not the union is C. If neither operation is available, the union equals C and beta=0, giving c=|C|−m(R−1). More explicitly the nonnegative potential

$$
\alpha=|U\setminus C|+\beta=c-|C|+m(R-1)
$$

decreases by one at each complete operation. Stop when c=1 or alpha=0. This is exactly (4.1). The simultaneous first operation counts as one operation, not as one component reduction per individual base replacement. ∎

**Theorem 4.2 (cocircuit formula).** For every k>=1,

$$
\gamma_c^k=
\min_{C\text{ cocircuit}}
\max\left\{\chi(C),\left\lceil\frac{|C|-k}{R-1}\right\rceil\right\}.       \tag{4.2}
$$

**Proof.** A dominating family of m bases covers a cocircuit C. Independent partition and (2.1) give m>=chi(C) and m(R−1)+k>=|C|.

For the reverse inequality fix C and let m be the displayed maximum. Extend an optimal independent partition to distinct covering bases and supplement the family to m distinct bases if necessary; Theorem 4.1 then gives at most k components. Supplementation is legitimate because m<=b. To see this, J(M) is connected: intersecting bases are adjacent, and for two disjoint bases choose independent representatives from both and extend them to a base, obtaining a two-edge path. All b bases thus form a connected family whose union is the nonloops. Equation (2.1) implies |C|<=b(R−1)+1, while chi(C)<=b. Since k>=1, m<=b. ∎

For q<=m<=b put

$$
T_m=\min\{|C|:C\text{ cocircuit},\ \chi(C)\le m\}.
$$

**Corollary 4.3.** Among dominating families of exactly m distinct bases, the minimum component count is max(1,T_m−m(R−1)).

**Proof.** The lower bound is the coverage budget; choose a cocircuit realizing T_m, extend and supplement its partition to m bases, and normalize. ∎

The formula is not an assertion that global cocircuit selection is polynomial-time under every representation. Given a covering family, normalization uses at most m−1 component-reducing operations and O(m²|E|) independence queries, together with polynomial incidence-graph work. This query bound concerns normalization only.

## 5. The complete spectrum of minimum dominating families

**Theorem 5.1.** With

$$
\ell=\max\{1,T_q-q(R-1)\},
$$

the component counts of all minimum dominating families are exactly the integers ell,ell+1,...,q. There is a minimum dominating family of disjoint bases. Consequently the independent domination number of J(M) equals q.

**Proof.** A maximal disjoint base family dominates J(M); otherwise another base could be added to it. Thus the maximum base-packing size is at least q. Choose a cocircuit C realizing T_q. By the classical union-matroid extension interface, C extends to q disjoint bases, because chi(C)=q and the union matroid has rank qR. This is a minimum dominating family with q components. Apply Theorem 4.1 while retaining C: each operation reduces the count by exactly one and retains q bases, ending at ell. Every intermediate integer is realized. Corollary 4.3 supplies the lower bound and q bases supply the upper bound. ∎

The independent domination conclusion does not say every minimum dominating family is independent or every maximal packing has size q.

By Theorem 3.1 the augmentation costs over all minimum families form the entire integer interval

$$
\max\{0,\lceil(\ell-k)/(R-1)\rceil\},\ldots,
\max\{0,\lceil(q-k)/(R-1)\rceil\}.                 \tag{5.1}
$$

Define F_k(M) as the smallest final size obtained by first choosing any size-q dominating family, then only adding bases until there are at most k components. The optimization is over all minimum families; it is not a deliberately bad initial choice. Equations (3.1) and (5.1) give

$$
F_k(M)=\max\left\{q,\left\lceil\frac{T_q-k}{R-1}\right\rceil\right\}.       \tag{5.2}
$$

The difference F_k−gamma_c^k is called the strategy loss. Equation (4.2) shows its source: a cocircuit requiring more than q independent classes can be sufficiently smaller to make global reoptimization preferable.

## 6. Sharp losses and natural structural boundaries

**Theorem 6.1.** Every rank-R matroid satisfies

$$
0\le F_k-\gamma_c^k\le
\max\left\{0,\left\lceil\frac{q-k}{R-1}\right\rceil-1\right\}.          \tag{6.1}
$$

For each R>=3 and q>=2 there is one matroid attaining this bound simultaneously for all positive k. For rank two the strategy loss is always zero.

**Proof of the bound.** Theorem 3.1 gives F_k<=q+max(0,ceil((q−k)/(R−1))). If gamma_c^k=q a minimum family already has at most k components, so F_k=q. Otherwise gamma_c^k>=q+1, yielding (6.1). The rank-two claim follows from Proposition 9.2 below. Sharpness follows from either the next construction or Section 7. ∎

### 6.1 A common truncated-partition construction

Fix R>=3, q>=2, and 1<=a<=R−2. On disjoint sets L,A,P of respective sizes (R−1)q, aq+1, q+R−1−a, truncate the direct sum of U_(R−1,(R−1)q), U_(a,aq+1), and the free matroid on P to rank R. Denote it N_(R,q,a). Independence means

$$
|I|\le R,\quad |I\cap L|\le R-1,\quad |I\cap A|\le a.
$$

Its hyperplanes are exactly L; the sets A union Q with Q an (R−1−a)-subset of L union P; and the (R−1)-element independent sets Q with at most R−2 elements of L and at most a−1 of A. Indeed these exhaust the flats of pretruncation rank R−1: saturating L leaves no rank for another part; saturating A leaves rank R−1−a; without a saturated part closure adds no element.

The complementary cocircuit sizes are respectively

$$
(a+1)q+R-a,\qquad Rq,\qquad (R+a)q+1-a.
$$

The first cocircuit has partition number q+1: A forces that lower bound, and partitioning A into q+1 classes of at most a elements and distributing P into unused rank-R capacity gives the upper bound. The second has partition number q: it has Rq elements, none in A, and at least q elements of P, so partition it into q R-element sets each containing a P element. The third has more than Rq elements, hence partition number at least q+1.

Thus q=gamma and every size-q dominating family exactly covers a second-type cocircuit and consists of disjoint bases. The first-type cocircuit has size at most (q+1)(R−1)+1, since the difference is (R−a−2)q+a>=0. Theorem 4.1 therefore gives q+1 connected dominating bases. Consequently

$$
\gamma_c^k=\begin{cases}q+1,&k<q,\\q,&k\ge q,\end{cases}
\qquad F_k=q+\max\{0,\lceil(q-k)/(R-1)\rceil\}.       \tag{6.2}
$$

This proves sharpness in (6.1). The girth is a+1, from a circuit in A. Taking a=R−2 gives girth R−1. Taking a=2 gives a simple example for every R>=4. Thus simple rank two and three have zero loss, whereas each higher rank permits the full sharp loss. Not every parameter has positive loss: the right side of (6.1) is positive only when q−k>=R.

### 6.2 Paving matroids

**Theorem 6.2.** If M is paving, R>=2, and s is its smallest cocircuit size, then T_q=s and T_m=s for all m>=q. In particular

$$
\gamma_c^k=F_k=\max\{q,\lceil(s-k)/(R-1)\rceil\}.       \tag{6.3}
$$

**Proof.** Distinct hyperplanes of a paving matroid meet in at most R−2 elements. The classical partition criterion reduces to

$$
\chi(C)\le m\ \Longleftrightarrow\ |C|\le mR
\text{ and }|C\cap B|\le m(R-1)\text{ for every hyperplane }B.       \tag{6.4}
$$

Indeed lower-rank subsets are independent, and rank-R−1 subsets lie in hyperplanes [BSY21].

If q=1 an independent cocircuit C_0 exists and s<=R. For s<R every shortest cocircuit is independent; for s=R, C_0 itself is shortest. Hence T_1=s.

Let q>=2, let C_0=E−H satisfy chi(C_0)=q, and choose a largest hyperplane A. Then |E−A|<=|C_0|<=qR. Suppose another hyperplane B has |B−A|>=q(R−1)+1. H cannot equal A, by (6.4). B cannot equal H either, since |A|>=|H| would imply |A−H|>=|H−A|>q(R−1), again violating (6.4). Thus H,A,B are distinct and

$$
|C_0|\ge |(A\cup B)\setminus H|
\ge 2q(R-1)+2-2(R-2)>qR,
$$

a contradiction. All hyperplane constraints in (6.4) hold for E−A, so this shortest cocircuit is q-partitionable. Monotonicity gives T_m=s for m>=q, and (4.2),(5.2) give (6.3). ∎

Zero strategy loss does not imply gamma_c^k=q. The girth-R−1 examples in Section 6.1 show that the universal paving guarantee cannot be extended even one girth level below R. They do not give an individual-matroid characterization of zero loss.

## 7. Graphic and simple binary sharpness

### 7.1 Graphic matroids

**Theorem 7.1.** For every R>=3 and q>=2, a graphic matroid of rank R satisfies (6.2), and hence attains (6.1) for every k.

**Proof.** Take A={a_0,a_1} and B={b_1,...,b_(R−1)}. Let the crossing tree consist of a_0b_1 and a_1b_i for 1<=i<=R−1, each with q parallel copies. Inside the parts take a_0a_1 and the path b_1...b_(R−1), each with q+1 parallel copies. The graph is connected on R+1 vertices.

Its bond C=delta(A) contains Rq edges and partitions into q spanning trees, one copy of each crossing edge per tree. Any other bond contains all q+1 copies of some internal edge: if it cuts no internal edge, the connected internal graphs force its shores to be A and B. No q spanning trees cover such a bond. Thus gamma=q and every minimum dominating family must cover C exactly, making its trees pairwise disjoint.

Put e=a_0b_1, h=a_0a_1, and let Q contain one fixed copy of each a_1b_i for 2<=i<=R−1. For 1<=i<=q take Q union {h_i,e_i}, and additionally Q union {h_(q+1),e_1}. These q+1 distinct spanning trees cover delta(a_0) and share the nonempty set Q. They form a connected dominating family, proving (6.2). ∎

Parallel edges are allowed. This result does not contradict the simple regular corollary below.

### 7.2 A simple binary family

**Lemma 7.2 (classical affine partition and packing interface).** A full affine hyperplane A not containing zero in GF(2)^rho has N=2^(rho−1) points, independent partition number ceil(N/rho), and t disjoint bases whenever t rho<=N.

**Proof.** A rank-j subset has at most 2^(j−1) points, and 2^(j−1)/j is nondecreasing for j>=1. Matroid partition gives the first assertion. For j>=1, any rank-j subset X satisfies

$$
|A\setminus X|\ge N-2^{j-1}\ge N(\rho-j)/\rho\ge t(\rho-j).
$$

For j=0 the same final bound holds because X is empty. The classical union rank formula therefore has value t rho, giving t disjoint bases. ∎

**Theorem 7.3.** For every d>=5, set R=d+2, m=ceil(2^(d−1)/d), q=m−1. There is a simple binary rank-R matroid satisfying (6.2) and attaining (6.1) for all k. At d=8, R=10 and q=15, the connected strategy loss is one.

**Proof.** Use coordinates (z,y_1,...,y_(d+1)) in GF(2)^(d+2). Put H={z=0}, H_A={z=0,y_(d+1)=0}, H_B={z=0,y_d=0}, and w=y_d. The ground set's internal part consists of all nonzero vectors in H_A union H_B, without repeats. Each subspace has dimension d and their sum is H.

The affine set E_0={z=1,y_d=0} has 2^d points and rank d+1. Since q<2^(d−1)/d, q(d+1)<2^d. Lemma 7.2 provides q disjoint bases S_i of K=ker(w) from E_0. Choose q distinct vectors e_i with z=1,y_d=1, and append C=(union S_i) union {e_i} to the internal ground set. Every S_i union {e_i} is a full base. Thus the resulting matroid is simple binary of rank R, and C has qR elements.

The internal part spans H, so C is a cocircuit. Any other cocircuit is a minimal nonzero linear-functional support whose functional is nonzero on H and hence on at least one of H_A,H_B. It contains a full rank-d affine hyperplane of that subspace, with partition number m. Therefore C is the only cocircuit coverable by q bases. Its size forces every minimum dominating family to consist of q disjoint bases.

The support D={x:w(x)=1} consists of the full affine hyperplane A' in H_A and the q points e_i. Its complement spans K, since it contains S_1, so D is a cocircuit. Partition A' into m independent classes I_i, attach one e_i to each of the first q classes, and leave the last without an extra point. These sets are independent because each e_i lies outside H_A. Moreover chi(D)=m by the affine lower bound.

Choose a in H_B−H_A. It is outside the span of each augmented class: a combination landing in H must have coefficient zero on its possible e_i, leaving a combination in H_A. Add a to each class and extend it to a full base. The resulting m bases cover D and share a. They must be distinct, since fewer than m covering bases would contradict chi(D)=m. They form a connected dominating family of size q+1. The minimum-family argument and Theorem 3.1 give (6.2). ∎

The family has 3·2^(d−1)−1+qR elements and contains a Fano restriction; it is not regular. It does not realize every rank and q, nor establish the minimum rank for positive loss. Its contribution is sharpness without parallel elements, not a new affine packing theorem.

### 7.3 Zero-loss binary classes

**Corollary 7.4.** Every simple binary matroid of rank R>=2 with no F_7 minor has zero strategy loss for all k. In particular this holds for all simple regular matroids.

**Proof.** The classical Fano-exclusion growth theorem bounds the size of every rank-j restriction by j(j+1)/2 [Mur76, McG12, Ox11]. Hence |X|/r(X)<=(R+1)/2 for every nonempty X. Matroid partition covers the entire ground set with at most p=ceil((R+1)/2)<=R independent classes, which extend to a dominating family. Thus q<=R and the right side of (6.1) is zero. Regular matroids have no F_7 minor by the classical excluded-minor characterization. ∎

The proof does not require or establish an independent cocircuit in every simple regular matroid.

**Corollary 7.5.** Simple binary matroids of ranks two through six have zero strategy loss. Positive loss in a simple binary matroid therefore requires rank at least seven.

**Proof.** Every cocircuit is an affine functional-one support. Its rank-j subsets have at most 2^(j−1) points, so chi(C)<=ceil(2^(R−1)/R). For R=2,...,6 this upper bound is 1,2,2,4,6, respectively, and is at most R. Apply (6.1). ∎

Neither corollary is an if-and-only-if classification. A Fano minor alone is not sufficient for positive loss, and the rank-ten example is not claimed minimal.

## 8. Optimization from an explicit laminar capacity tree

Suppose M is given by an explicit laminar family of capacity constraints |I intersection A|<=b_A, with nonnegative integer capacities b_A. Delete loops, add the ground-set root and singleton leaves, and complete each internal node's children to a partition of its elements. Root capacity is the true rank R; other capacities may be capped by R and their set sizes. Let n be the nonloop element count and p the number of tree nodes. Elements are explicit, not binary-encoded multiplicities.

**Theorem 8.1.** From this tree, the value gamma_c^k is computable in O(pR² log(n+1)) integer max/add operations, in addition to input preprocessing. An optimal family of distinct bases is constructible in polynomial time in the explicit input and output lengths. The faster displayed bound is for the value, not the entire output procedure.

**Proof.** For any set D, chi(D)<=m exactly when |D intersection A|<=m b_A at every node. Necessity follows by adding capacities over the independent classes. For sufficiency order leaves by depth-first traversal, list D in that order, and assign colors cyclically modulo m. Each node occupies an interval, so each color occurs at most ceil(|D intersection A|/m)<=b_A times.

It is enough to optimize over all D with r(E−D)<R rather than only cocircuits: such D contains a cocircuit, whose size and partition number cannot be larger. Put H=E−D. The color constraints become |H intersection A|>=|A|−m b_A. The rank recursion is

$$
r_A(H\cap A)=\min\{b_A,\sum_{B\text{ child of }A}r_B(H\cap B)\}.
$$

For each node A and 0<=t<=b_A, store F_A(t), the greatest possible size of H intersection A with local rank exactly t and all descendant lower bounds satisfied. Infeasible states have value negative infinity. At a leaf initialize rank-zero size zero and rank-one size one, then filter by its lower bound. At an internal node start G(0)=0 and convolve its children: a pair of states s,t updates the state min(b_A,s+t) by the maximum of its current value and G(s)+F_B(t). Filter states with retained size below |A|−m b_A.

Keeping only the greatest size at a fixed rank is safe: ancestor constraints are size lower bounds and ancestor ranks use only child ranks. Once a partial rank saturates b_A, further nonnegative child ranks cannot undo saturation. This proves the dynamic program's completeness inductively.

At the root let W_m=max_(t<R) F_E(t). If infeasible set T_m=+infinity; otherwise T_m=n−W_m. The complement of a feasible H contains a cocircuit. Conversely every m-partitionable cocircuit has a feasible complement, proving this equality. A maximum-size feasible H must be a hyperplane: if its rank is too small or it is not closed, an element can be added without reaching rank R, preserving every lower bound.

By (4.2), the optimum is the smallest m such that T_m is finite and T_m<=m(R−1)+k. Feasibility is monotone in m, and m=n is sufficient. Binary search requires O(log(n+1)) dynamic programs, each with O(pR²) arithmetic work. Traceback gives a feasible hyperplane and cocircuit, which certify an upper bound; optimality follows from completeness or an infeasibility table at m−1, not from that witness alone.

For output, cyclically partition the cocircuit and extend the nonempty classes to bases. Deduplicate, then supplement to m bases. Distinct-base generation can use include/exclude prefix search: an independent prefix I is extendible using the remaining elements precisely when their union with I has rank R. Every live subtree contains a base, yielding polynomial delay. At most m already selected outputs need be skipped. Finally apply Theorem 4.1. All ranks and independence tests are computable from the tree in polynomial time, completing the output claim. ∎

The truncated-partition sharp examples in Section 6 are laminar. Thus this algorithm does not merely solve instances where every strategy is already optimal.

### 8.1 Why the input representation matters

On 2R elements let U=U_(R,2R), and for each R-set H let M_H have all the bases of U except H. It is the laminar matroid defined by |I|<=R and |I intersection H|<=R−1, and is paving. The complement C=E−H is a base dominating J(M_H), so gamma_c^k(J(M_H))=1 for every k. In U each base has a disjoint complement, but two intersecting bases differing in one element dominate; hence gamma_c^k(J(U))=2.

The independence and rank oracles of U and M_H differ only at the query H. A deterministic exact algorithm on the U transcript must query all binom(2R,R) R-sets; otherwise an unqueried H yields the same transcript with a different answer. This is exponential in n=2R, even under the promise of laminar and paving input. The hidden instance and indistinguishability technique are classical [HLL22]; here they calibrate this particular parameter and the tree-input contract. No randomized, approximation, or explicit-input NP-hardness statement is made.

## 9. Explicit specializations and degeneracies

### 9.1 Complete-profile hypergraphs

Partition the elements into t parts of sizes n_j>=d_j>=1 and select exactly d_j elements in every part. These edges are the bases of the direct sum of uniform matroids, of rank R=sum d_j, and their line graph is J(M). A family dominates precisely when some part has fewer than d_j uncovered elements. Thus q=min_j floor(n_j/d_j).

If t>=2, choose q disjoint d_j-subsets in a minimizing part and a fixed subset in every other part. They form a clique dominating family, so gamma_c^k=q for every k. Every component count 1,...,q is realizable by a different construction: retain the disjoint subsets in the minimizing part, group the q edges into c nonempty groups and, in another part l, share one group-specific element while keeping the other selected elements private. In every remaining part choose q pairwise disjoint subsets of its required size; thus no remaining part connects different groups. The shared part uses q(d_l−1)+c<=q d_l<=n_l elements, the other disjoint choices are feasible since q d_i<=n_i, and the edges remain distinct in the minimizing part.

For t=1, write N=qR+s_0, 0<=s_0<R. All cocircuits have size N−R+1 and partition number q. Hence

$$
\gamma_c^k=\max\{q,\lceil(N-R+1-k)/(R-1)\rceil\}.
$$

For a size-q family put delta=qR−|U|. It is dominating exactly when delta<=R−s_0−1. Its nontrivial components involve at most 2delta bases, since a component of h>=2 bases consumes at least h−1 units of delta. This describes a bounded overlap core, not a list of isomorphism types.

### 9.2 All rank-two matroids

Delete loops and let the parallel class sizes be n_1>=...>=n_p>=1, p>=2. Put N=sum n_i and T=N−n_1. The bases are the edges of K_(n_1,...,n_p).

**Proposition 9.2.** For p=2, q=n_2, gamma_c^k=q, and the minimum-family component spectrum is 1,...,q. For p>=3,

$$
q=\max\{\lceil T/2\rceil,n_2\},\qquad
\gamma_c^k=F_k=\max\{q,T-k\},
$$

and the minimum-family component spectrum is T−q,...,q.

**Proof.** The bipartite case follows from Section 9.1. For p>=3, cocircuits are complements of parallel classes. Removing a largest class minimizes both total size and the largest remaining class size. The remaining complete multipartite graph has matching number min(floor(T/2),T−n_2): match all outside vertices when one part exceeds half; otherwise order parts consecutively and pair opposite halves, deleting one vertex first if T is odd. Its independent partition number is therefore max(ceil(T/2),n_2)=q. Equation (2.3) gives q and T_q=T. Every cocircuit has size at least T and partition number at least q; (4.2) is minimized at this one, giving the formula. Theorem 5.1 gives the spectrum, and (5.2) gives F_k. ∎

The ordinary domination endpoint is prior work [SM14], and connected edge domination has classical graph interfaces [HM19]. Their inclusion here provides a transparent check of the general theory, not a new ordinary edge-domination claim.

### 9.3 Rank one and empty families

Rank one is excluded from every formula dividing by R−1. Its bases are singleton nonloops and J(M) is edgeless. All its b vertices must be selected to dominate; a k-component dominating family exists if and only if k>=b. Theorem 3.1 assumes a nonempty prescribed family. Rank-zero matroids and empty starting families are outside the main statements.

## 10. Verification and limitations

General results rest on the proofs, not on finite computations. The accompanying bounded Windows verification checks separate the laminar dynamic program from a finite subset-rank and base-family enumeration reference; they include positive controls for both normalization operations and deliberately corrupted controls. A larger rank-four witness is checked for feasibility, coverage, distinctness, and connectivity without enumerating all base families. Its optimum uses the general proof, not an independent exhaustive computation.

The simple binary controls at d=5 and d=8 verify matrix rank, all nonzero-functional supports, cocircuit identification, covering bases, shared elements, and four deliberate corruptions using an independent row-reduction implementation. They do not independently enumerate the whole base-intersection graph or prove the general sharpness theorem by computation. Implementation size and resource gates do not restrict the mathematical quantifiers.

The paper does not classify all individual zero-loss matroids, solve the corresponding problem for arbitrary uniform hypergraphs, cover weighted base costs, or supply a global polynomial algorithm for arbitrary matrix representations. Formula (4.2) is an exact reduction, not a claim that all its subproblems are easy. Full external review and a comprehensive priority assessment remain separate from internal proof and code checking.

## Appendix A. Optimal-family incidence budget

For any m-base family covering a cocircuit C,

$$
|U\setminus C|+\beta+(k-c)=m(R-1)+k-|C|.
$$

If c<=k all left terms are nonnegative. Conversely domination means coverage of some cocircuit and the component condition is c<=k. At m=gamma_c^k this gives an incidence-budget characterization of optimal families, not a canonical isomorphism classification. For U_(R,N), the branch gamma_c^k>q has budget at most R−2; if its budget is zero its incidence graph is a forest with exactly k components. The incidence identity itself is standard graph theory.

## Appendix B. Bounded source comparison

The checked 2013 and 2018 Hamilton-cycle papers [ZY13, ZC18] use nonempty-intersection adjacency in their bodies and do not state the domination formulas proved here. The 2018 abstract's contrary adjacency wording is not used as a definition.

The following gaps remain explicit rather than being turned into evidence of absence:

- Zhang–Liu's work cited as forthcoming in reference 18 of the 2012 chapter *The Properties of Graphs of Matroids* [LL12]: final identity and full text unresolved. This is not a paper authored by the chapter authors Li–Liu.
- Akkari [Akk95]: accessible description concerns extension of retained partial base packings under additional assumptions; its full text and possible intermediate lemmas have not been excluded against Theorem 4.1.
- Song et al. [SM14]: ordinary rank-two endpoint treated as prior work irrespective of missing full text.
- Weninger–Fukasawa [WF24]: the checked 2024 version studies minimum-cost cocircuit/interdiction interfaces, not the independent-partition constraint of Section 8; the full later published version and the associated 2026 dissertation have not all been compared.
- Later budgeted-laminar independent-set work, Vega's 2020 thesis, and Jensen–Korte's original property-query paper have only partial source coverage. No new generic tree-DP or oracle technique is claimed.
- Murty's original synopsis [Mur76] has not been fully examined; the density theorem used in Corollary 7.4 is a classical result reproduced in [McG12, Ox11], not a novelty claim.

An OpenAI/math directory screen forms one additional collision check, not a proof that no unindexed or concurrent result exists. The final review record will distinguish source refresh, proof review, finite verification, and artifact checks.

## References

[EF65] J. Edmonds and D. R. Fulkerson, *Transversals and matroid partition*, Journal of Research of the National Bureau of Standards 69B (1965), 147–153. [Original paper](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn3p147_A1b.pdf).

[FJ18] G. Fan, H. Jiang, P. Li, D. B. West, D. Yang, and X. Zhu, *Extensions of matroid covering and packing*, author manuscript dated 11 June 2018. [Author manuscript](https://dwest.web.illinois.edu/pubs/matrunc.pdf).

[ZY13] Y. Zhang, B. Yu, and G. Liu, *Edge Disjoint Hamilton Cycles in Intersection Graphs of Bases of Matroids*, Utilitas Mathematica 90 (2013), 327–334. [Author copy](https://yu.trubox.ca/wp-content/uploads/sites/2481/2021/03/67_Edge-disjoint-H-cycle-in-matroidUM2013Zhang-Yu.pdf).

[ZC18] Y. Zhang and H. Chi, *Hamilton Cycles in Intersection Graphs of Bases of Matroids*, MMSA (2018), 331–334. [DOI](https://doi.org/10.2991/mmsa-18.2018.73).

[SM14] W. Song, L. Miao, H. Wang, and Y. Zhao, *Maximal matching and edge domination in complete multipartite graphs*, International Journal of Computer Mathematics 91(5) (2014), 857–862. [DOI](https://doi.org/10.1080/00207160.2013.818668). Full-text comparison incomplete.

[YG80] M. Yannakakis and F. Gavril, *Edge Dominating Sets in Graphs*, SIAM Journal on Applied Mathematics 38(3) (1980), 364–372. [DOI](https://doi.org/10.1137/0138030).

[HM19] D. Hermelin, M. Mnich, E. J. van Leeuwen, and G. J. Woeginger, *Domination When the Stars Are Out*, ACM Transactions on Algorithms 15(2) (2019), article 25. [Author copy](https://dspace.library.uu.nl/bitstream/handle/1874/382146/a25_hermelin.pdf?sequence=1).

[BSY21] K. Bérczi, T. Schwarcz, and Y. Yamaguchi, *List Coloring of Two Matroids through Reduction to Partition Matroids*, SIAM Journal on Discrete Mathematics 35(3) (2021), 2192–2209. [DOI](https://doi.org/10.1137/20M1385615).

[FO17] T. Fife and J. Oxley, *Laminar matroids*, author manuscript (2017). Classical presentation and closure constructions.

[DA23] I. Doron-Arad, A. Kulik, and H. Shachnai, *An FPTAS for Budgeted Laminar Matroid Independent Set*, arXiv:2304.13984v1 (2023). [Version checked](https://arxiv.org/abs/2304.13984v1).

[WF24] N. Weninger and R. Fukasawa, *Interdiction of minimum spanning trees and other matroid bases*, arXiv:2407.14906v1 (2024). [Version checked](https://arxiv.org/abs/2407.14906v1). Later-version comparison incomplete.

[HLL22] X. Huang, J. Luo, and L. Li, *Quantum Speedup and Limitations on Matroid Property Problems*, arXiv:2111.12900v2 (2022). [Version checked](https://arxiv.org/abs/2111.12900v2). Classical hidden-instance overlap is expressly credited.

[Mur76] U. S. R. Murty, *Extremal Matroids with Forbidden Restrictions and Minors (Synopsis)*, Congressus Numerantium XVII (1976), 463–468. Original full text not examined.

[McG12] S. McGuinness, *An Erdős–Gallai Theorem for Matroids*, Annals of Combinatorics 16 (2012), 107–119, Theorem 1.4. [DOI](https://doi.org/10.1007/s00026-011-0123-4).

[Ox11] J. Oxley, *Matroid Theory*, second edition, Oxford University Press (2011), including Proposition 14.10.3. The cited theorem is checked through available reproductions; the entire book was not audited.

[Akk95] S. Akkari, *Random packing by matroid bases and triangles*, Discrete Mathematics 145 (1995), 1–9. [DOI](https://doi.org/10.1016/0012-365X(94)00050-S). Full-text comparison incomplete.

[LL12] P. Li and G. Liu, *The Properties of Graphs of Matroids*, IntechOpen chapter (2012), reference 18. [DOI](https://doi.org/10.5772/35778). Its forthcoming Zhang–Liu reference remains unresolved.

## Author and assistance disclosure

AI tools assisted with research, literature comparison, verification, and writing. Carptopus is the responsible author. No external peer-review endorsement is implied.
