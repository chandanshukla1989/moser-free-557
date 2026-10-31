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

This graph is a reduction of the construction of **Sergi Galán**
([decalion89/chromatic-number-of-the-plane](https://github.com/decalion89/chromatic-number-of-the-plane),
`data/flat852`, 29 September 2026): an 852-vertex Moser-spindle-free
5-chromatic unit-distance graph in the same field Q(zeta_21), with the same
`/7` coordinates and the same 126 unit directions, built from
**J. K. Haugland's** heptagon lattice (arXiv:2608.04542) and its mirror
image. 504 of the 557 vertices here are vertices of Galán's `core852a.json`
(same frame); the rest come from the same point family.

Our contribution is the reduction from 852 to 557 vertices: SAT-verified
vertex elimination (kissat) with batched removals, colouring-guided repair
batches, and combination of independent branches. Every intermediate record
was certified not 4-colourable.

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
