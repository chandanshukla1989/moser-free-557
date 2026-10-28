#!/usr/bin/env python3
"""Verification for the graph JSON in this repository.

Checks, in exact integer arithmetic over Q(zeta_21):
  1. every listed edge has squared length exactly 1;
  2. no unlisted pair has squared length 1 (the edge list is the full
     unit-distance graph on the point set);
  3. the graph contains no Moser spindle as a subgraph;
  4. the included 5-colouring is proper and uses 5 colours.

With --cnf FILE it also writes a 4-colourability CNF (one-hot encoding,
one triangle pinned for symmetry breaking); any SAT solver reports it
UNSATISFIABLE, hence chromatic number 5.

Usage: python3 verify.py graph767.json [--cnf four.cnf]
"""
import json
import sys

# Phi_21(x), the minimal polynomial of zeta_21 (monic, degree 12)
PHI21 = [1, -1, 0, 1, -1, 0, 1, 0, -1, 1, 0, -1, 1]  # x^12-x^11+x^9-x^8+x^6-x^4+x^3-x+1


def reduce_mod_phi(c):
    """Reduce an integer polynomial (list of coeffs, low degree first) mod Phi_21."""
    c = list(c)
    for d in range(len(c) - 1, 11, -1):
        q = c[d]
        if q:
            for i, p in enumerate(PHI21):
                c[d - 12 + i] -= q * p
    return c[:12]


def norm_sq_49(a, b):
    """49*|p-q|^2 for points p,q given by coefficient vectors a,b (degree<12).

    d = a-b as a polynomial in zeta. |p-q|^2 = d(zeta)*d(zeta^-1)/49.
    zeta^-1 = zeta^20, so conj(d) has coefficient of zeta^((21-k)%21) from d_k.
    The product is a cyclic convolution mod 21, then reduced mod Phi_21.
    Returns the reduced coefficient vector of 49*|p-q|^2 (should be [49,0,...]).
    """
    d = [x - y for x, y in zip(a, b)]
    conj = [0] * 21
    for k, v in enumerate(d):
        conj[(21 - k) % 21] += v
    prod = [0] * 21
    for i, di in enumerate(d):
        if di:
            for j, cj in enumerate(conj):
                if cj:
                    prod[(i + j) % 21] += di * cj
    return reduce_mod_phi(prod)


def main():
    g = json.load(open(sys.argv[1]))
    n = g['vertices']
    ex = g['exact_coordinates']
    edges = {tuple(sorted(e)) for e in g['edges']}
    assert len(ex) == n and len(edges) == g['edges_count']

    ONE = [49] + [0] * 11
    unit_pairs = set()
    for i in range(n):
        for j in range(i + 1, n):
            if norm_sq_49(ex[i], ex[j]) == ONE:
                unit_pairs.add((i, j))
    assert unit_pairs == edges, 'edge list differs from exact unit-distance pairs'
    print(f'exact unit-distance check: {len(edges)} edges, all pairs scanned: OK')

    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # Moser spindle: two rhombi (apex u; v,w adjacent to u and each other;
    # x adjacent to v,w) sharing the apex, with the far tips adjacent.
    spindles = 0
    for u in range(n):
        nu = sorted(adj[u])
        rhombi = []
        for ii, v in enumerate(nu):
            for w in nu[ii + 1:]:
                if w in adj[v]:
                    for x in (adj[v] & adj[w]) - {u}:
                        rhombi.append((v, w, x))
        for ii in range(len(rhombi)):
            s1 = set(rhombi[ii])
            for jj in range(ii + 1, len(rhombi)):
                if s1.isdisjoint(rhombi[jj]) and rhombi[jj][2] in adj[rhombi[ii][2]]:
                    spindles += 1
    assert spindles == 0, f'{spindles} Moser spindles found'
    print('Moser spindle search: none found: OK')

    col = g['five_colouring']
    assert all(col[u] != col[v] for u, v in edges) and sorted(set(col)) == [0, 1, 2, 3, 4]
    print('5-colouring: proper, 5 colours: OK')

    if '--cnf' in sys.argv:
        path = sys.argv[sys.argv.index('--cnf') + 1]
        def lit(v, c):
            return 4 * v + c + 1
        cl = [[lit(v, c) for c in range(4)] for v in range(n)]
        for u, v in edges:
            for c in range(4):
                cl.append([-lit(u, c), -lit(v, c)])
        tri = next((u, v, w) for u in range(n) for v in sorted(adj[u]) if v > u
                   for w in sorted(adj[u] & adj[v]) if w > v)
        cl += [[lit(tri[0], 0)], [lit(tri[1], 1)], [lit(tri[2], 2)]]
        with open(path, 'w') as f:
            f.write(f'p cnf {4 * n} {len(cl)}\n')
            f.writelines(' '.join(map(str, c)) + ' 0\n' for c in cl)
        print(f'wrote {path}; a SAT solver reports UNSAT (no 4-colouring)')


if __name__ == '__main__':
    main()
