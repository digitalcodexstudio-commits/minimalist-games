"""Inline-SVG Sudoku diagram generator for the Minimalist Games blog.

All diagrams share the site theme:
  dark text   #1b2545
  blue        #4a5fc1   blue tint #edf0fb
  green       #1f9d57   green tint #e3f5ea   (placements / targets)
  red         #d6453d   red tint   #fbe7e6   (eliminations)
  amber       #d99100   amber tint #fdf3da   (pattern cells)
  muted grey  #8891aa                        (pencil candidates)
"""

CELL = 56
MARGIN = 8
SIZE = CELL * 9 + MARGIN * 2

C = {
    "text": "#1b2545", "grid": "#1b2545", "thin": "#c7cede",
    "blue": "#4a5fc1", "blue_bg": "#edf0fb",
    "green": "#1f9d57", "green_bg": "#e3f5ea",
    "red": "#d6453d", "red_bg": "#fbe7e6",
    "amber": "#c97f00", "amber_bg": "#fdf3da",
    "muted": "#8891aa",
}

# sub-cell positions for candidates 1..9 inside a cell (3x3)
def _cand_xy(x0, y0, n):
    col = (n - 1) % 3
    row = (n - 1) // 3
    cx = x0 + CELL * (col + 0.5) / 3
    cy = y0 + CELL * (row + 0.5) / 3
    return cx, cy


def grid(givens=None, placed=None, cands=None, cand_style=None,
         cell_bg=None, title="", arrows=None):
    """Return an inline <svg> string.

    givens     : {(r,c): digit}        black bold clues
    placed     : {(r,c): digit}        green bold (a placement the technique makes)
    cands      : {(r,c): [digits]}     pencil marks (muted)
    cand_style : {(r,c): {digit: kind}} kind in {'green','red','amber','blue'}
                 overrides colour of a single candidate (e.g. 'red' = eliminate)
    cell_bg    : {(r,c): kind}         kind in {'blue','green','red','amber'} tint
    arrows     : list of (r1,c1,r2,c2) faint blue connector lines (centre-to-centre)
    """
    givens = givens or {}
    placed = placed or {}
    cands = cands or {}
    cand_style = cand_style or {}
    cell_bg = cell_bg or {}
    arrows = arrows or []

    p = []
    p.append(
        f'<svg viewBox="0 0 {SIZE} {SIZE}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" class="sudoku-diagram"'
        + (f' aria-label="{title}"' if title else "")
        + ">"
    )
    if title:
        p.append(f"<title>{title}</title>")
    p.append(f'<rect x="0" y="0" width="{SIZE}" height="{SIZE}" fill="#ffffff"/>')

    # cell backgrounds
    bgmap = {"blue": C["blue_bg"], "green": C["green_bg"],
             "red": C["red_bg"], "amber": C["amber_bg"]}
    for (r, c), kind in cell_bg.items():
        x0 = MARGIN + c * CELL
        y0 = MARGIN + r * CELL
        p.append(f'<rect x="{x0}" y="{y0}" width="{CELL}" height="{CELL}" '
                 f'fill="{bgmap.get(kind, C["blue_bg"])}"/>')

    # thin grid lines
    for i in range(10):
        if i % 3 == 0:
            continue
        x = MARGIN + i * CELL
        p.append(f'<line x1="{x}" y1="{MARGIN}" x2="{x}" y2="{MARGIN + 9*CELL}" '
                 f'stroke="{C["thin"]}" stroke-width="1"/>')
        y = MARGIN + i * CELL
        p.append(f'<line x1="{MARGIN}" y1="{y}" x2="{MARGIN + 9*CELL}" y2="{y}" '
                 f'stroke="{C["thin"]}" stroke-width="1"/>')
    # thick box lines
    for i in range(0, 10, 3):
        x = MARGIN + i * CELL
        p.append(f'<line x1="{x}" y1="{MARGIN}" x2="{x}" y2="{MARGIN + 9*CELL}" '
                 f'stroke="{C["grid"]}" stroke-width="2.5"/>')
        y = MARGIN + i * CELL
        p.append(f'<line x1="{MARGIN}" y1="{y}" x2="{MARGIN + 9*CELL}" y2="{y}" '
                 f'stroke="{C["grid"]}" stroke-width="2.5"/>')

    stylemap = {"green": C["green"], "red": C["red"],
                "amber": C["amber"], "blue": C["blue"]}

    for r in range(9):
        for c in range(9):
            x0 = MARGIN + c * CELL
            y0 = MARGIN + r * CELL
            cx = x0 + CELL / 2
            cy = y0 + CELL / 2
            if (r, c) in givens:
                p.append(
                    f'<text x="{cx}" y="{cy}" text-anchor="middle" '
                    f'dominant-baseline="central" font-family="Arial,Helvetica,sans-serif" '
                    f'font-size="32" font-weight="700" fill="{C["text"]}">{givens[(r,c)]}</text>')
            elif (r, c) in placed:
                p.append(
                    f'<text x="{cx}" y="{cy}" text-anchor="middle" '
                    f'dominant-baseline="central" font-family="Arial,Helvetica,sans-serif" '
                    f'font-size="32" font-weight="700" fill="{C["green"]}">{placed[(r,c)]}</text>')
            elif (r, c) in cands:
                cstyle = cand_style.get((r, c), {})
                for n in cands[(r, c)]:
                    ccx, ccy = _cand_xy(x0, y0, n)
                    kind = cstyle.get(n)
                    fill = stylemap.get(kind, C["muted"])
                    weight = "700" if kind else "400"
                    extra = ""
                    if kind == "red":
                        extra = (f'<line x1="{ccx-7}" y1="{ccy}" x2="{ccx+7}" y2="{ccy}" '
                                 f'stroke="{C["red"]}" stroke-width="1.6"/>')
                    if kind in ("green", "amber", "blue"):
                        p.append(f'<circle cx="{ccx}" cy="{ccy}" r="9" fill="none" '
                                 f'stroke="{fill}" stroke-width="1.6"/>')
                    p.append(
                        f'<text x="{ccx}" y="{ccy}" text-anchor="middle" '
                        f'dominant-baseline="central" font-family="Arial,Helvetica,sans-serif" '
                        f'font-size="13" font-weight="{weight}" fill="{fill}">{n}</text>')
                    p.append(extra)

    for (r1, c1, r2, c2) in arrows:
        x1 = MARGIN + c1 * CELL + CELL / 2
        y1 = MARGIN + r1 * CELL + CELL / 2
        x2 = MARGIN + c2 * CELL + CELL / 2
        y2 = MARGIN + r2 * CELL + CELL / 2
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{C["blue"]}" stroke-width="2" stroke-dasharray="5 4" '
                 f'opacity="0.7"/>')

    p.append("</svg>")
    return "".join(p)
