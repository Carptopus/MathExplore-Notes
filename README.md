# MathExplore Notes

MathExplore Notes is a collection of AI-assisted mathematical research results,
including manuscripts and reproducible verification materials.

## Research index

| Entry | Areas | Contribution | Status |
| --- | --- | --- | --- |
| [Proper transposed sesqui arrays at all Sylvester--Hadamard powers](research/proper-sesqui-all-powers/README.md) | Combinatorial designs, finite fields, finite geometry, algebraic curves | Constructs an exact-parameter proper transposed sesqui array for every power of two | Internally verified candidate proof; external review pending |
| [Paley two-edge switching for proper transposed sesqui arrays](research/paley-two-edge-switching/README.md) | Combinatorial designs, finite fields, elliptic curves | Constructs an exact-parameter proper transposed sesqui array for every odd prime power \(q\equiv3\pmod4\), \(q\geq11\) | Internally verified candidate proof; external review pending |

## Current results

### Sylvester--Hadamard powers

For every \(t=2^k\), \(k\geq2\), the first manuscript constructs

$$
SA^{\mathsf T}(4t-2,t,-,t-1,t:(2t-1)\times2t).
$$

It combines the classical Sylvester--Hadamard column design with a compatible
proper ordering based on finite-field maps, finite geometry, algebraic curves,
and exact certificates.

- [Manuscript and verification materials](research/proper-sesqui-all-powers/README.md)

### Paley two-edge switching

For every odd prime power \(q\equiv3\pmod4\), \(q\geq11\), the second
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

Licenses are declared per research entry. The current entries use CC BY 4.0
for manuscripts and documentation, the MIT License for Python verification
code, and CC0 1.0 for JSON results, certificates, and manifests.

Unless an entry states otherwise, the responsible author is **Carptopus**.
Contact: [carptopus@163.com](mailto:carptopus@163.com).

## Repository-level keywords

AI-assisted mathematics; mathematical exploration; experimental mathematics;
computer-assisted mathematics; reproducible mathematics; exact computation;
constructive mathematics; combinatorics; combinatorial designs; row-column
designs; transposed sesqui arrays; finite geometry; finite fields; Paley
designs; quadratic characters; edge switching; algebraic combinatorics;
algebraic curves over finite fields; elliptic curves; Hasse and Hasse--Weil
bounds; cross-disciplinary mathematical methods.
