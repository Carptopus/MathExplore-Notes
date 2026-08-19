# MathExplore Notes

MathExplore Notes is a collection of AI-assisted mathematical research results,
including manuscripts and reproducible verification materials.

## Research index

| Entry | Areas | Contribution | Public version | Status |
| --- | --- | --- | --- | --- |
| [Proper transposed sesqui arrays at all Sylvester--Hadamard powers](research/proper-sesqui-all-powers/README.md) | Combinatorial designs, finite fields, finite geometry, algebraic curves | Constructs an exact-parameter proper transposed sesqui array for every power of two | v0.2-beta | Internally verified candidate proof; external review pending |
| [Paley two-edge switching for proper transposed sesqui arrays](research/paley-two-edge-switching/README.md) | Combinatorial designs, finite fields, elliptic curves | Constructs an exact-parameter proper transposed sesqui array for every odd prime power $q\equiv3\pmod4$, $q\geq11$ | v0.2-beta | Internally verified candidate proof; external review pending |
| [Spectral separation and the nSSP for looped double paths](research/nssp-looped-double-paths/README.md) | Inverse eigenvalue problems, graph patterns, Jacobi matrices | Classifies exactly which looped double paths allow the non-symmetric strong spectral property | v0.1-beta | Internally verified candidate proof; external review pending |
| [An exact nSSP criterion for root-loop spider matrices](research/nssp-root-loop-spiders/README.md) | Inverse eigenvalue problems, generalized stars, matrix patterns | Characterizes the nSSP of every fixed root-loop bidirected spider matrix by pairwise coprimality of its arm polynomials | v0.1-beta | Internally verified candidate proof; external review pending |
| [A recursive nSSP criterion for root-loop tree matrices](research/nssp-root-loop-trees/README.md) | Inverse eigenvalue problems, rooted trees, matrix patterns | Characterizes the nSSP of every fixed root-loop bidirected tree matrix by recursive sibling-subtree coprimality | v0.1-beta | Internally verified candidate proof; external review pending |

## Current results

### Sylvester--Hadamard powers

For every $t=2^k$, $k\geq2$, the first manuscript constructs

$$
SA^{\mathsf T}(4t-2,t,-,t-1,t:(2t-1)\times2t).
$$

It combines the classical Sylvester--Hadamard column design with a compatible
proper ordering based on finite-field maps, finite geometry, algebraic curves,
and exact certificates.

- [Manuscript and verification materials](research/proper-sesqui-all-powers/README.md)

### Paley two-edge switching

For every odd prime power $q\equiv3\pmod4$, $q\geq11$, the second
manuscript constructs

$$
SA^{\mathsf T}\!\left(
2q,\frac{q+1}{2},-,\frac{q-1}{2},\frac{q+1}{2}:q\times(q+1)
\right).
$$

It converts a classical Paley matching into a proper array by a two-edge
switch, with existence proved through exact character counts and the Hasse
bound for elliptic curves.

- [Manuscript and verification materials](research/paley-two-edge-switching/README.md)

### Spectral separation for looped double paths

For the double path $P_{n,L}$ with loops at the vertices in $L$, the third
manuscript proves

$$
P_{n,L}\text{ allows the nSSP}
\quad\Longleftrightarrow\quad
L\ne\varnothing\text{ and }(n\text{ is even or }L\text{ contains an odd vertex}).
$$

Its main structural tool is a spectral-separation criterion for a symmetric
irreducible tridiagonal matrix with one nonzero diagonal entry: nSSP is
equivalent to disjoint spectra of the two Jacobi arms.

- [Manuscript and verification materials](research/nssp-looped-double-paths/README.md)

### Root-loop spider matrices

For a spider with at least three arms, consider an arbitrary real matrix whose
nonzero off-diagonal positions are exactly both directed entries on every tree
edge, with a single nonzero diagonal entry at the root. If $P_j$ is the
characteristic polynomial of arm $j$ after deleting the root, the fourth
manuscript proves

$$
A\text{ has the nSSP}
\quad\Longleftrightarrow\quad
P_1,\ldots,P_m\text{ are pairwise coprime}.
$$

This fixed-matrix criterion allows arbitrary non-symmetric real weights,
negative edge products, repeated roots within an arm, and nonreal shared-root
witnesses. It extends the two-arm spectral mechanism while leaving the earlier
arbitrary-loop double-path classification independent.

- [Manuscript and verification materials](research/nssp-root-loop-spiders/README.md)

### Recursive root-loop tree matrices

For an arbitrary finite rooted tree, consider a real matrix whose nonzero
off-diagonal positions are exactly both directed entries on every tree edge,
with a single nonzero diagonal entry at the root. For each child of every
vertex, form the characteristic polynomial of its complete descendant
subtree. The fifth manuscript proves

$$
A\text{ has the nSSP}
\quad\Longleftrightarrow\quad
\text{the child-subtree polynomials are pairwise coprime at every vertex}.
$$

This fixed-matrix theorem allows arbitrary non-symmetric real weights,
negative edge products, nonreal or repeated subtree roots, and arbitrarily
many nested branch vertices. It strictly extends the preceding fixed-matrix
double-path and spider criteria while leaving the earlier arbitrary-loop
double-path pattern classification independent.

- [Manuscript and verification materials](research/nssp-root-loop-trees/README.md)

## Status and review policy

Entries are research records, not automatically peer-reviewed publications.
Each directory states its own claim and status. The labels used here mean:

- **Exploration:** an investigated direction without a retained theorem claim.
- **Candidate result:** a precise claim with supporting argument or evidence,
  still undergoing internal checks.
- **Internally verified:** the written proof and supplied computations have
  passed the repository's internal checks; independent mathematical review may
  still be pending.
- **Externally reviewed:** outside mathematical feedback has been received and
  its disposition is recorded by the entry.

Corrections, counterexamples, equivalent prior results, and independent
reproductions are welcome. A status label is a record of the review stage, not
a substitute for reading the proof.

## Repository organization

Each research topic lives under [`research/`](research/) in its own directory.
An entry may contain a focused README, manuscript and source, verification
programs, generated evidence, checksums, and entry-specific licensing.

## Licensing and attribution

Licenses are declared per research entry. Manuscripts and documentation
typically use CC BY 4.0, while Python verification code typically uses the MIT
License. Some entries separately place specified JSON results, certificates,
or manifests under CC0 1.0; the declaration inside each entry is authoritative.

Unless an entry states otherwise, the responsible author is **Carptopus**.
Contact: [carptopus@163.com](mailto:carptopus@163.com).

## Repository-level keywords

AI-assisted mathematics; mathematical exploration; experimental mathematics;
computer-assisted mathematics; reproducible mathematics; exact computation;
constructive mathematics; combinatorics; combinatorial designs; row-column
designs; transposed sesqui arrays; finite geometry; finite fields; Paley
designs; quadratic characters; edge switching; algebraic combinatorics;
algebraic curves over finite fields; elliptic curves; Hasse and Hasse--Weil
bounds; cross-disciplinary mathematical methods; inverse eigenvalue problems;
graph patterns; non-symmetric strong spectral property; Jacobi matrices;
tridiagonal matrices; spectral separation;
root-loop spiders; spider matrices; generalized stars; bidirected trees; arm
characteristic polynomials; rooted tree matrices; recursive subtree
polynomials; pairwise coprimality; spectral collisions; centralizer witnesses.
