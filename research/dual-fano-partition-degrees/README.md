# Partition-representation degrees of the dual Fano matroid

## Manuscript

- [Read or download the PDF](dual-fano-partition-degrees.pdf)
- [LaTeX source](dual-fano-partition-degrees.tex)
- [BibTeX citation](CITATION.bib)
- DOI: [10.5281/zenodo.22083219](https://doi.org/10.5281/zenodo.22083219)
- [Finite calibration](verification/README.md)
- [SHA-256 checksums](SHA256SUMS.txt)
- Author: Carptopus
- Contact: [carptopus@163.com](mailto:carptopus@163.com)
- Version: v0.1.1-beta (24 August 2026)
- Licenses: manuscript and documentation under CC BY 4.0; Python calibration code under MIT
- Status: internally verified candidate proof; external mathematical review pending.

## Main results

For a finite matroid $M$, let $\chi(M)$ be its set of partition-representation
degrees. The manuscript proves the complete classification

$$
\chi(F_7^*)=\{2^k:k\geq1\}.
$$

It then derives two fixed-alphabet consequences for all finite matroids:

1. a finite matroid is 6-entropic if and only if it is regular;
2. among all integers $v\geq2$, the class of $v$-entropic matroids equals the
   class of regular matroids if and only if $v=6$.

## Proof mechanism

After fixing one coordinate fibre of a partition representation of $F_7^*$,
the contraction is an $M(K_4)$ group slice. The remaining three circuit
equations propagate that local normal form to every fibre and force every
element of the finite group to be an involution. The group is therefore
elementary abelian of order $2^k$. The converse follows from a characteristic-2
linear representation.

The degree-six classification combines this spectrum with the excluded minors
$U_{2,4}$, $F_7$, and $F_7^*$ for regular matroids and the complete existence
theorem for pairs of orthogonal Latin squares.

## Verification boundary

The proof is theoretical. The Python script in `verification/` checks the full
$F_7^*$ variable-strength orthogonal-array conditions for elementary abelian
2-groups of orders 2, 4, and 8, and confirms the predicted last-circuit failure
for several groups containing non-involutions. It is a multiplication-order
calibration and does not replace the general proof.

## Prior-work and review status

Matúš classified the $M(K_4)$ group slice and the degree set of $F_7$; Abbe and
Spirkl and later Chen, Cheng, and Bai established the degree-three obstruction
for $F_7^*$. A recent degree-four characterization uses the same adjacent group
slice. The manuscript distinguishes these ingredients from its propagation
argument and global consequences. The public-source comparison found no direct
statement of the three results above; this is not a claim of absolute global
priority.

## AI-assisted research disclosure

Carptopus is the responsible author. OpenAI Codex was used extensively for
AI-assisted literature search, proof exploration, adversarial auditing, finite
calibration, and manuscript preparation. The paper contains the complete
disclosure and responsibility statement.

## Keywords

dual Fano matroid; entropic matroid; partition representation;
variable-strength orthogonal array; regular matroid; excluded minors; finite
groups; orthogonal Latin squares; matroid theory; information theory.
