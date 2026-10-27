# moser-free-791

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23686997.svg)](https://doi.org/10.5281/zenodo.23686997)

Archived at Zenodo: https://doi.org/10.5281/zenodo.23686997 (concept DOI for all versions: 10.5281/zenodo.23686996)

A unit-distance graph in the plane with **791 vertices**, **4180 edges**,
**chromatic number 5**, and **no Moser spindle** as a subgraph.

Coordinates are exact elements of Q(zeta_21): each point is
`(sum_{k=0}^{11} a_k zeta_21^k) / 7` with the integer vector `a` given in
`graph791.json` (`exact_coordinates`). Float coordinates are included for
convenience only; all verification is exact.

## Verify

    python3 verify.py graph791.json

Checks in exact integer arithmetic: every listed edge has squared length
exactly 1, no other pair does, the graph contains no Moser spindle, and the
included 5-colouring is proper.

    python3 verify.py graph791.json --cnf four.cnf
    kissat four.cnf          # reports UNSATISFIABLE
    kissat four.cnf proof.drat && drat-trim four.cnf proof.drat   # s VERIFIED

UNSAT of `four.cnf` means no proper 4-colouring exists, so the chromatic
number is exactly 5.
