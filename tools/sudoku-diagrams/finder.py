from itertools import combinations
from engine import candidates, givens_from_blanks

def units():
    U = []
    for r in range(9):
        U.append(("row", r, [(r, c) for c in range(9)]))
    for c in range(9):
        U.append(("col", c, [(r, c) for r in range(9)]))
    for b in range(9):
        br, bc = (b // 3) * 3, (b % 3) * 3
        U.append(("box", b, [(br + i, bc + j) for i in range(3) for j in range(3)]))
    return U

def find_naked_pairs(cand):
    res = []
    for kind, idx, cells in units():
        emp = [p for p in cells if p in cand]
        for a, b in combinations(emp, 2):
            if cand[a] == cand[b] and len(cand[a]) == 2:
                elim = [p for p in emp if p not in (a, b) and cand[p] & cand[a]]
                if elim:
                    res.append((kind, idx, a, b, sorted(cand[a]), elim))
    return res

def find_hidden_pairs(cand):
    res = []
    for kind, idx, cells in units():
        emp = [p for p in cells if p in cand]
        for d1, d2 in combinations(range(1, 10), 2):
            holders1 = [p for p in emp if d1 in cand[p]]
            holders2 = [p for p in emp if d2 in cand[p]]
            if len(holders1) == 2 and set(holders1) == set(holders2):
                # hidden pair only interesting if cells have extra candidates
                if any(len(cand[p]) > 2 for p in holders1):
                    res.append((kind, idx, holders1, (d1, d2)))
    return res

def find_naked_triples(cand):
    res = []
    for kind, idx, cells in units():
        emp = [p for p in cells if p in cand and len(cand[p]) in (2, 3)]
        for trio in combinations(emp, 3):
            u = set().union(*(cand[p] for p in trio))
            if len(u) == 3:
                elim = [p for p in cells if p in cand and p not in trio and cand[p] & u]
                if elim:
                    res.append((kind, idx, trio, sorted(u), elim))
    return res

def find_pointing(cand):
    # within a box, a digit confined to one row/col -> eliminate outside box in that line
    res = []
    for b in range(9):
        br, bc = (b // 3) * 3, (b % 3) * 3
        cells = [(br + i, bc + j) for i in range(3) for j in range(3) if (br + i, bc + j) in cand]
        for d in range(1, 10):
            holders = [p for p in cells if d in cand[p]]
            if len(holders) in (2, 3):
                rows = {r for r, c in holders}
                cols = {c for r, c in holders}
                if len(rows) == 1:
                    r = next(iter(rows))
                    elim = [(r, c) for c in range(9) if (r, c) in cand and (c < bc or c >= bc + 3) and d in cand[(r, c)]]
                    if elim:
                        res.append(("row", b, d, holders, elim))
                if len(cols) == 1:
                    c = next(iter(cols))
                    elim = [(r, c) for r in range(9) if (r, c) in cand and (r < br or r >= br + 3) and d in cand[(r, c)]]
                    if elim:
                        res.append(("col", b, d, holders, elim))
    return res

def find_boxline(cand):
    # a digit in a row/col confined to one box -> eliminate from rest of that box
    res = []
    for r in range(9):
        for d in range(1, 10):
            holders = [(r, c) for c in range(9) if (r, c) in cand and d in cand[(r, c)]]
            if holders and len({c // 3 for rr, c in holders}) == 1:
                b = (r // 3) * 3 + (holders[0][1] // 3)
                br, bc = (b // 3) * 3, (b % 3) * 3
                elim = [(i, j) for i in range(br, br+3) for j in range(bc, bc+3)
                        if (i, j) in cand and i != r and d in cand[(i, j)]]
                if elim and len(holders) >= 2:
                    res.append(("row", r, d, holders, elim))
    for c in range(9):
        for d in range(1, 10):
            holders = [(r, c) for r in range(9) if (r, c) in cand and d in cand[(r, c)]]
            if holders and len({rr // 3 for rr, cc in holders}) == 1:
                b = (holders[0][0] // 3) * 3 + (c // 3)
                br, bc = (b // 3) * 3, (b % 3) * 3
                elim = [(i, j) for i in range(br, br+3) for j in range(bc, bc+3)
                        if (i, j) in cand and j != c and d in cand[(i, j)]]
                if elim and len(holders) >= 2:
                    res.append(("col", c, d, holders, elim))
    return res
