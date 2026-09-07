"""Candidate engine + canonical solution helpers (for verification)."""

# Canonical valid solved Sudoku
SOLUTION = [
    [5,3,4, 6,7,8, 9,1,2],
    [6,7,2, 1,9,5, 3,4,8],
    [1,9,8, 3,4,2, 5,6,7],
    [8,5,9, 7,6,1, 4,2,3],
    [4,2,6, 8,5,3, 7,9,1],
    [7,1,3, 9,2,4, 8,5,6],
    [9,6,1, 5,3,7, 2,8,4],
    [2,8,7, 4,1,9, 6,3,5],
    [3,4,5, 2,8,6, 1,7,9],
]


def candidates(givens):
    """givens: {(r,c): d}. Return {(r,c): set(...)} for every empty cell."""
    grid = [[givens.get((r, c), 0) for c in range(9)] for r in range(9)]
    def used(r, c):
        s = set()
        for k in range(9):
            s.add(grid[r][k]); s.add(grid[k][c])
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                s.add(grid[i][j])
        s.discard(0)
        return s
    cand = {}
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cand[(r, c)] = set(range(1, 10)) - used(r, c)
    return cand


def givens_from_blanks(blanks):
    """Take the canonical SOLUTION, blank the listed (r,c) cells -> givens dict.
    Guarantees an internally consistent board whose candidates always contain
    the true solution digit."""
    blanks = set(blanks)
    return {(r, c): SOLUTION[r][c]
            for r in range(9) for c in range(9) if (r, c) not in blanks}
