# Domination, component spectra, and sharp augmentation losses in matroid base-intersection graphs

Author: Carptopus · Version 0.1-beta · 8 October 2026

This is one unified manuscript, combining the complete-profile starting examples with arbitrary-matroid structure, laminar optimization, paving boundaries, and graphic/simple-binary sharpness. It is not a proof of a general hypergraph domination conjecture.

- [Manuscript](manuscript.md)
- [PDF](paper/main.pdf) · [LaTeX source](paper/main.tex) · [BibTeX](CITATION.bib)
- [Bounded verification and environment](verification/README.md)
- [Artifact checks](paper/ARTIFACT-CHECK.md) · [Build instructions](paper/README.md) · [File hashes](SHA256SUMS.txt)
- Prior-work comparisons and unavailable sources: manuscript Section 1.1 and Appendix B.

## Results and boundaries

The graph has **all bases as vertices**, with adjacency by **nonempty intersection**; it is not a basis-exchange graph or a disjointness graph. For every finite matroid of rank R at least two and every positive k:

1. A prescribed nonempty family with c components needs exactly max(0,ceil((c-k)/(R-1))) added bases to reach at most k components.
2. Allowing replacement while preserving coverage gives a cocircuit formula for the global k-component domination number and the exact base-count/component frontier.
3. All minimum dominating families have a gap-free component spectrum. Optimizing over the starting minimum family can still leave an arbitrarily large augmentation-strategy loss.
4. The loss bound is sharp in graphic matroids for every allowed rank and ordinary domination number, and in an infinite simple binary family. It vanishes for paving and simple Fano-minor-free binary matroids, including simple regular matroids.
5. An explicit laminar capacity tree admits polynomial-time value computation and construction of an optimal base family. The value complexity is separated from output complexity. A credited classical oracle example explains the input boundary.

Classic partition/union tools, ordinary rank-two endpoints, density bounds, tree-DP techniques and the hidden-instance method are not claimed as new. This does not classify all zero-loss matroids, cover weighted selection, or provide a global polynomial algorithm for arbitrary matrix/oracle inputs. The binary family does not establish the minimum possible rank for positive loss.

## Review status

The constituent frozen proofs have writing-preparation audit records. The unified manuscript has passed a separate fresh-context review and targeted rechecks of the repaired final hash. The public verification package has passed its independent fixed-scope guard, including positive, negative and disabled-assertion controls. The accompanying artifact report records source-to-TeX fidelity and full-page PDF inspection separately; neither replaces proof or novelty review. This is the prepared preprint version, not an externally peer-reviewed result.

Prior-work comparison is bounded. Three important gaps remain: the final identity/full text of a Zhang–Liu work cited as forthcoming in a 2012 chapter; Akkari's 1995 packing paper; and the full later versions of adjacent Weninger–Fukasawa work. These are not represented as excluded coverage, and no global-priority guarantee is asserted.

AI tools assisted with research, literature comparison, verification and writing. Carptopus is the responsible author. External mathematical review and formal peer review are pending.

Manuscript/documentation and fixed data: [CC BY 4.0](LICENSE.md). Code: [MIT](verification/LICENSE-CODE-MIT.txt).

Keywords: matroid; base-intersection graph; domination; connected domination; cocircuit; matroid partition; laminar matroid; paving matroid; binary matroid; graphic matroid.
