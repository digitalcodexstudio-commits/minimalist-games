# -*- coding: utf-8 -*-
"""Generate the 9 Sudoku-strategy blog pages with verified inline-SVG diagrams."""
import os
from engine import SOLUTION, candidates, givens_from_blanks
from examples import EX, cand_for
import sudoku_svg as S

SITE = "/sessions/gracious-nifty-ptolemy/mnt/minimalist-games/src/blog"

# ---------------------------------------------------------------- helpers
def unit_cells(kind, idx):
    if kind == "row":
        return [(idx, c) for c in range(9)]
    if kind == "col":
        return [(r, idx) for r in range(9)]
    br, bc = (idx // 3) * 3, (idx % 3) * 3
    return [(br + i, bc + j) for i in range(3) for j in range(3)]

def givens_of(name):
    blanks = set(EX[name]["blanks"])
    return {(r, c): SOLUTION[r][c] for r in range(9) for c in range(9)
            if (r, c) not in blanks}

def cands_of(name, cells):
    c = cand_for(name)
    return {p: sorted(c[p]) for p in cells if p in c}

LEGEND_COLORS = {
    "blue": "#edf0fb", "green": "#1f9d57", "red": "#d6453d",
    "amber": "#c97f00", "amber_bg": "#fdf3da", "green_bg": "#e3f5ea",
}

def legend(items):
    li = "".join(
        f'<li><i style="background:{col}"></i>{label}</li>'
        for col, label in items)
    return f'<ul class="sudoku-legend">{li}</ul>'

def figure(svg, caption):
    return f'<figure class="sudoku-figure">{svg}<figcaption>{caption}</figcaption></figure>'

def pair(svg1, cap1, svg2, cap2):
    return ('<div class="sudoku-pair">'
            f'<figure class="sudoku-figure">{svg1}<figcaption>{cap1}</figcaption></figure>'
            f'<figure class="sudoku-figure">{svg2}<figcaption>{cap2}</figcaption></figure>'
            '</div>')

# ---------------------------------------------------------------- diagrams
def dia_last_remaining():
    g = givens_of("last_remaining")
    bg = {p: "blue" for p in unit_cells("row", 0)}
    bg[(0, 8)] = "green"
    return figure(
        S.grid(givens=g, placed={(0, 8): 2}, cell_bg=bg,
               title="Row with eight cells filled; the ninth must be 2"),
        "Row 1 already holds eight digits. Only 2 is missing, so it goes in the empty cell — a last remaining cell (full house).")

def dia_hidden_single():
    name = "hidden_single"
    g = givens_of(name)
    box = unit_cells("box", 2)
    show = [p for p in box]
    cands = cands_of(name, show)
    bg = {p: "blue" for p in box}
    # before: highlight the only 5
    style = {(2, 6): {5: "green"}}
    before = S.grid(givens=g, cands=cands, cand_style=style, cell_bg=bg,
                    title="In this box, 5 fits only one cell")
    bg2 = {p: "blue" for p in box}; bg2[(2, 6)] = "green"
    cands2 = {p: v for p, v in cands.items() if p != (2, 6)}
    after = S.grid(givens=g, cands=cands2, placed={(2, 6): 5}, cell_bg=bg2,
                   title="5 placed")
    return pair(before,
                "Pencil marks for the top-right box. The digit 5 appears as a candidate in just one cell, even though that cell also allows 4.",
                after,
                "Because 5 has nowhere else to go in the box, it is placed — a hidden single.")

def dia_cross_hatch():
    name = "cross_hatch"
    g = givens_of(name)
    box = unit_cells("box", 3)
    bg = {p: "blue" for p in box}
    # tint the crossing lines (rows 3,4 and cols 0,2) and mark existing 1s amber
    for r in (3, 4):
        for c in range(9):
            bg.setdefault((r, c), "amber")
    for c in (0, 2):
        for r in range(9):
            bg.setdefault((r, c), "amber")
    bg[(5, 1)] = "green"
    # existing 1s on those lines -> amber digit via cand_style trick won't work on givens;
    # instead draw dashed guide arrows from each existing 1 across into the box.
    ones = [(3, 5), (4, 8), (2, 0), (6, 2)]
    arrows = [(3, 5, 3, 1), (4, 8, 4, 1), (2, 0, 4, 0), (6, 2, 4, 2)]
    svg = S.grid(givens=g, placed={(5, 1): 1}, cell_bg=bg, arrows=arrows,
                 title="Cross-hatching places a 1 in the bottom-left box")
    return figure(svg,
        "Rows 4 and 5 already contain a 1 (amber lines), and so do columns 1 and 3. Inside the bottom-left box that rules out every cell except one — the 1 must sit there.")

def dia_naked_pair():
    name = "naked_pair"
    g = givens_of(name)
    box = unit_cells("box", 3)
    show = [p for p in box if p in cand_for(name)]
    cands = cands_of(name, show)
    bg = {p: "blue" for p in box}
    bg[(5, 0)] = "amber"; bg[(5, 2)] = "amber"
    style_before = {(5, 0): {3: "amber", 7: "amber"},
                    (5, 2): {3: "amber", 7: "amber"}}
    before = S.grid(givens=g, cands=cands, cand_style=style_before, cell_bg=bg,
                    title="Two cells share the candidates 3 and 7")
    # after: eliminate 3,7 from other box cells
    c = cand_for(name)
    style_after = {}
    cands_after = {}
    for p in show:
        vals = sorted(c[p])
        if p in [(5, 0), (5, 2)]:
            cands_after[p] = vals
        else:
            mark = {d: "red" for d in (3, 7) if d in c[p]}
            style_after[p] = mark
            cands_after[p] = vals
    after = S.grid(givens=g, cands=cands_after, cand_style=style_after, cell_bg=bg,
                   title="3 and 7 removed from the rest of the box")
    return pair(before,
        "Two cells in this box both hold exactly {3, 7} — a naked pair. Between them they will use up both the 3 and the 7.",
        after,
        "So 3 and 7 can be struck from every other cell in the box (shown in red).")

def dia_hidden_pair():
    name = "hidden_pair"
    g = givens_of(name)
    col = unit_cells("col", 4)
    show = [p for p in col if p in cand_for(name)]
    cands = cands_of(name, show)
    bg = {p: "blue" for p in col}
    bg[(6, 4)] = "amber"; bg[(7, 4)] = "amber"
    style_before = {(6, 4): {1: "amber", 3: "amber"},
                    (7, 4): {1: "amber", 3: "amber"}}
    before = S.grid(givens=g, cands=cands, cand_style=style_before, cell_bg=bg,
                    title="1 and 3 appear in only two cells of this column")
    style_after = {(6, 4): {8: "red"}, (7, 4): {8: "red"}}
    after = S.grid(givens=g, cands=cands, cand_style=style_after, cell_bg=bg,
                   title="Other candidates removed from the pair cells")
    return pair(before,
        "Across this whole column, the digits 1 and 3 can only go in these two cells — a hidden pair, buried among other pencil marks.",
        after,
        "That locks the pair: every other candidate (here the 8) is removed from both cells, leaving {1, 3}.")

def dia_naked_triple():
    name = "naked_triple"
    g = givens_of(name)
    col = unit_cells("col", 4)
    show = [p for p in col if p in cand_for(name)]
    cands = cands_of(name, show)
    bg = {p: "blue" for p in col}
    trio = [(4, 4), (5, 4), (8, 4)]
    for p in trio:
        bg[p] = "amber"
    style_before = {p: {d: "amber" for d in cand_for(name)[p]} for p in trio}
    before = S.grid(givens=g, cands=cands, cand_style=style_before, cell_bg=bg,
                    title="Three cells share the candidates 2, 5 and 8")
    c = cand_for(name)
    style_after = {}
    for p in show:
        if p not in trio:
            mark = {d: "red" for d in (2, 5, 8) if d in c[p]}
            if mark:
                style_after[p] = mark
    after = S.grid(givens=g, cands=cands, cand_style=style_after, cell_bg=bg,
                   title="2, 5 and 8 removed from the rest of the column")
    return pair(before,
        "Three cells in this column between them use only the digits 2, 5 and 8 — a naked triple. No cell needs all three; together they fill all three.",
        after,
        "So 2, 5 and 8 can be eliminated from every other cell in the column.")

def dia_pointing():
    name = "pointing"
    g = givens_of(name)
    box = unit_cells("box", 1)
    show = [p for p in box if p in cand_for(name)]
    cands = cands_of(name, show)
    # also show the elimination target candidates
    elim_cells = cands_of(name, [(2, 1)])
    cands.update(elim_cells)
    bg = {p: "blue" for p in box}
    bg[(2, 3)] = "amber"; bg[(2, 5)] = "amber"
    style = {(2, 3): {3: "amber"}, (2, 5): {3: "amber"}, (2, 1): {3: "red"}}
    arrows = [(2, 3, 2, 1)]
    svg = S.grid(givens=g, cands=cands, cand_style=style, cell_bg=bg, arrows=arrows,
                 title="A pointing pair eliminates a 3 along the row")
    return figure(svg,
        "In the top-middle box, the digit 3 can only sit in two cells — both in row 3. That “points” along the row, so 3 is removed from the cell to the left (red), outside the box.")

def dia_box_line():
    name = "box_line"
    g = givens_of(name)
    row = unit_cells("row", 5)
    show = [p for p in row if p in cand_for(name)]
    cands = cands_of(name, show)
    elim_cells = cands_of(name, [(3, 2)])
    cands.update(elim_cells)
    bg = {p: "blue" for p in row}
    bg[(5, 1)] = "amber"; bg[(5, 2)] = "amber"
    style = {(5, 1): {1: "amber"}, (5, 2): {1: "amber"}, (3, 2): {1: "red"}}
    arrows = [(5, 2, 3, 2)]
    svg = S.grid(givens=g, cands=cands, cand_style=style, cell_bg=bg, arrows=arrows,
                 title="Box/line reduction eliminates a 1 inside the box")
    return figure(svg,
        "In row 6 the digit 1 can only go inside the bottom-left box. So 1 is “claimed” by that row and can be removed from the rest of the box (red) — the cell above.")

DIAGRAMS = {
    "last": dia_last_remaining,
    "hidden_single": dia_hidden_single,
    "cross": dia_cross_hatch,
    "naked_pair": dia_naked_pair,
    "hidden_pair": dia_hidden_pair,
    "naked_triple": dia_naked_triple,
    "pointing": dia_pointing,
    "box_line": dia_box_line,
}

if __name__ == "__main__":
    # smoke test: render every diagram
    for k, fn in DIAGRAMS.items():
        html = fn()
        assert "<svg" in html, k
        print(f"{k}: {html.count('<svg')} svg, {len(html)} chars")
    print("diagrams OK")
