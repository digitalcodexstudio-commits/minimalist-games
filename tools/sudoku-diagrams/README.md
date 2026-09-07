# Sudoku strategy diagram generator

Reproducible source for the inline-SVG diagrams in the `/blog/sudoku-*` strategy posts.

- `engine.py`   — canonical solved grid + candidate computation
- `finder.py`   — pattern detectors (naked/hidden pairs, triples, pointing, box/line)
- `examples.py` — the 8 verified examples; run `python3 examples.py` to re-prove every one
- `sudoku_svg.py` — inline-SVG grid renderer (site theme colours)
- `build.py`    — builds each diagram from the verified examples
- `pages.py`    — assembles the 9 HTML pages into `src/blog/`

Regenerate all pages:  `python3 pages.py`
Re-verify the logic:   `python3 examples.py`
