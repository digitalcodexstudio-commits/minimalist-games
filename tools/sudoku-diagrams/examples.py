"""Verified strategy examples. Each entry's blanks are applied to the canonical
SOLUTION; candidates are computed and the named pattern is asserted to hold.
Run `python3 examples.py` to re-prove every example."""
from engine import SOLUTION, candidates, givens_from_blanks

EX = {
    "last_remaining": dict(blanks=[(0, 8)], box=0, unit=("row", 0),
                           place={(0, 8): 2}),
    "hidden_single":  dict(blanks=[(1, 0), (1, 7), (2, 4), (2, 6), (2, 7), (3, 6)],
                           box=2, digit=5, place={(2, 6): 5}),
    "cross_hatch":    dict(blanks=[(3, 2), (4, 0), (4, 1), (5, 1), (5, 2)],
                           box=3, digit=1, place={(5, 1): 1},
                           drows=[3, 4], dcols=[0, 2]),
    "naked_pair":     dict(blanks=[(4, 0), (4, 5), (5, 0), (5, 2), (7, 2), (8, 0)],
                           unit=("box", 3), pair=[3, 7],
                           cells=[(5, 0), (5, 2)], elim=[(4, 0)]),
    "hidden_pair":    dict(blanks=[(6, 2), (6, 4), (6, 7), (7, 1), (7, 4), (7, 7), (8, 4)],
                           unit=("col", 4), pair=[1, 3], cells=[(6, 4), (7, 4)]),
    "naked_triple":   dict(blanks=[(0, 4), (0, 5), (4, 1), (4, 4), (5, 4), (5, 7), (8, 3), (8, 4)],
                           unit=("col", 4), triple=[2, 5, 8],
                           cells=[(4, 4), (5, 4), (8, 4)], elim=[(0, 4)]),
    "pointing":       dict(blanks=[(0, 1), (0, 8), (2, 1), (2, 3), (2, 5), (4, 5)],
                           box=1, digit=3, line=("row", 2),
                           cells=[(2, 3), (2, 5)], elim=[(2, 1)]),
    "box_line":       dict(blanks=[(3, 2), (3, 4), (3, 5), (5, 1), (5, 2), (6, 2)],
                           box=3, digit=1, line=("row", 5),
                           cells=[(5, 1), (5, 2)], elim=[(3, 2)]),
}


def cand_for(name):
    return candidates(givens_from_blanks(EX[name]["blanks"]))


def _verify():
    # last remaining
    c = cand_for("last_remaining")
    assert c[(0, 8)] == {2}, c[(0, 8)]

    # hidden single: 5 only in (2,6) among box-2 empties, cell not naked
    c = cand_for("hidden_single")
    box2 = [(r, cc) for r in range(0, 3) for cc in range(6, 9) if (r, cc) in c]
    holders = [p for p in box2 if 5 in c[p]]
    assert holders == [(2, 6)] and len(c[(2, 6)]) >= 2, (holders, c.get((2, 6)))

    # cross hatch: 1 only in (5,1) among box-3 empties
    c = cand_for("cross_hatch")
    box3 = [(r, cc) for r in range(3, 6) for cc in range(0, 3) if (r, cc) in c]
    holders = [p for p in box3 if 1 in c[p]]
    assert holders == [(5, 1)], holders

    # naked pair {3,7} at (5,0),(5,2) in box 3, eliminating 3/7 from (4,0)
    c = cand_for("naked_pair")
    assert c[(5, 0)] == {3, 7} and c[(5, 2)] == {3, 7}, (c[(5, 0)], c[(5, 2)])
    assert c[(4, 0)] & {3, 7}, c[(4, 0)]

    # hidden pair {1,3} confined to (6,4),(7,4) in col 4, both with extras
    c = cand_for("hidden_pair")
    col4 = [(r, 4) for r in range(9) if (r, 4) in c]
    for d in (1, 3):
        h = [p for p in col4 if d in c[p]]
        assert set(h) == {(6, 4), (7, 4)}, (d, h)
    assert len(c[(6, 4)]) > 2 and len(c[(7, 4)]) > 2, (c[(6, 4)], c[(7, 4)])

    # naked triple {2,5,8} over (4,4),(5,4),(8,4) in col 4, eliminating from (0,4)
    c = cand_for("naked_triple")
    u = set()
    for p in [(4, 4), (5, 4), (8, 4)]:
        u |= c[p]
        assert c[p] <= {2, 5, 8}, (p, c[p])
    assert u == {2, 5, 8}
    assert c[(0, 4)] & {2, 5, 8}, c[(0, 4)]

    # pointing: 3 in box 1 confined to row 2 -> eliminate from (2,1)
    c = cand_for("pointing")
    box1 = [(r, cc) for r in range(0, 3) for cc in range(3, 6) if (r, cc) in c]
    h = [p for p in box1 if 3 in c[p]]
    assert {r for r, _ in h} == {2}, h
    assert 3 in c[(2, 1)]

    # box-line: 1 in row 5 confined to box 3 -> eliminate from (3,2)
    c = cand_for("box_line")
    h = [(5, cc) for cc in range(9) if (5, cc) in c and 1 in c[(5, cc)]]
    assert {cc // 3 for _, cc in h} == {0}, h
    assert 1 in c[(3, 2)]

    print("All 8 examples verified OK.")


if __name__ == "__main__":
    _verify()
