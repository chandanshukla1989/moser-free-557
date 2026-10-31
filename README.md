# moser-free-557

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23686996.svg)](https://doi.org/10.5281/zenodo.23686996)

Archived at Zenodo (concept DOI for all versions): https://doi.org/10.5281/zenodo.23686996

A unit-distance graph in the plane with **557 vertices**, **2811 edges**,
**chromatic number 5**, and **no Moser spindle** as a subgraph.

Coordinates are exact elements of Q(zeta_21): each point is
`(sum_{k=0}^{11} a_k zeta_21^k) / 7` with the integer vector `a` given in
`graph557.json` (`exact_coordinates`). Float coordinates are included for
convenience only; all verification is exact. A Moser spindle needs
sqrt(-11), which is not in Q(zeta_21), so no unit-distance graph on these
points can contain one; `verify.py` also checks this directly.

## Credit and provenance

The 126 unit directions used here are the same as in **Sergi Galán's**
852-vertex Moser-spindle-free 5-chromatic graph
([decalion89/chromatic-number-of-the-plane](https://github.com/decalion89/chromatic-number-of-the-plane),
`data/flat852`, September 2026), which come from **J. K. Haugland's**
heptagon lattice (arXiv:2608.04542) and its mirror image. Our configuration
(2967 vertices) was built and reduced independently to 557 vertices by
SAT-verified vertex elimination (kissat; single and batched removals,
combination of independent branches). Both graphs live in the same lattice,
so many points coincide. The smallest published spindle-free example has
1441 vertices; Haugland's explicit example has 2131.

## Verify

    python3 verify.py graph557.json

Checks in exact integer arithmetic: every listed edge has squared length
exactly 1, no other pair does, the graph contains no Moser spindle, and the
included 5-colouring is proper.

    python3 verify.py graph557.json --cnf four.cnf
    kissat four.cnf          # reports UNSATISFIABLE

UNSAT of `four.cnf` means no proper 4-colouring exists, so the chromatic
number is exactly 5.

A DRAT certificate is attached to the GitHub release `v557`
(`graph557.cnf`, a 4-colouring CNF with one triangle pinned, and
`proof557.drat.xz`):

    xz -d proof557.drat.xz
    drat-trim graph557.cnf proof557.drat     # s VERIFIED
