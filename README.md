# MathExplore Notes

MathExplore Notes is a collection of AI-assisted mathematical research results,
including manuscripts and reproducible verification materials.

## Research index

| Entry | Areas | Contribution | Status |
| --- | --- | --- | --- |
| [Proper transposed sesqui arrays at all Sylvester--Hadamard powers](research/proper-sesqui-all-powers/README.md) | Combinatorial designs, finite fields, finite geometry, algebraic curves | Constructs an exact-parameter proper transposed sesqui array for every power of two | Internally verified candidate proof; external review pending |

### Current entry: proper transposed sesqui arrays

For every \(t=2^k\), \(k\geq2\), the current manuscript constructs

$$
SA^{\mathsf T}(4t-2,t,-,t-1,t:(2t-1)\times2t).
$$

It combines the classical Sylvester--Hadamard trace design with a compatible
proper ordering, using finite-field maps, Subiaco geometry, algebraic curves,
Hasse--Weil estimates, resultants, and finite certificates.

- [Manuscript overview and files](research/proper-sesqui-all-powers/README.md)
- [Verification code, certificates, and reproduction instructions](research/proper-sesqui-all-powers/verification/README.md)

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
An entry may contain:

- a focused README describing the question, result, methods, and status;
- a manuscript or technical note;
- source files and references;
- verification code, frozen inputs, certificates, and reproduction steps;
- entry-specific licensing and provenance information.

The root README serves only as the repository-wide introduction and index.
Detailed mathematical claims belong in the corresponding research directory.

## Licensing and attribution

Licenses are declared per research entry because manuscripts, source code, and
data may use different terms. For the current entry, the manuscript and
documentation use CC BY 4.0, Python verification code uses the MIT License, and
JSON data and certificates use CC0 1.0.

Unless an entry states otherwise, the responsible author is **Carptopus**.
Contact: [carptopus@163.com](mailto:carptopus@163.com).

## Repository-level keywords

Mathematical exploration; experimental mathematics; computer-assisted
mathematics; reproducible mathematics; exact computation; constructive
mathematics; combinatorics; combinatorial designs; finite geometry; finite
fields; algebraic combinatorics; algebraic curves over finite fields;
cross-disciplinary mathematical methods.
