# Minimalist Games

Sudoku, Minesweeper and 2048, playable instantly in the browser. No account, no download, no pop-ups. Static HTML, CSS and vanilla JavaScript — no framework, no build step.

**Live at [minimalist-games.com](https://minimalist-games.com)**

Built and maintained by [Arnaldo Lima](https://minimalist-games.com/about#author) (Digital Codex Studio), Portugal.

## What's here

Three games and a set of strategy guides that explain how to actually get better at them.

- **Sudoku Zen** — six difficulties, pencil notes, undo, three hints. Every puzzle has a single solution reachable by logic alone; difficulty is rated by which human solving techniques a puzzle actually requires, not by counting clues.
- **Minesweeper** — three board sizes, first-click safe, flag mode that works on touch.
- **2048** — arrow keys or swipe, undo, best score kept locally.

The site is a PWA, so it works offline, and game progress stays in the browser — nothing about how you play is sent anywhere.

## The Sudoku diagram generator

`tools/sudoku-diagrams/` is the part of this repo worth a look.

The blog explains solving techniques — cross-hatching, hidden singles, naked and hidden pairs, pointing pairs, box/line reduction — and each one needs a diagram of a board where that technique applies. Drawing those by hand is how you end up with diagrams that quietly contradict the text, or show a position that isn't actually solvable.

So they aren't drawn. `engine.py` solves and verifies positions, `finder.py` searches for a grid where exactly one technique applies, `sudoku_svg.py` renders the candidate grid to SVG, and `pages.py` assembles the guide pages around them. Every board shown in a guide is a real position the solver has verified, and the highlighted cells are the ones it actually used.

**`pages.py` is the source of truth for the Sudoku guide pages.** Editing that generated HTML by hand loses the edit on the next run:

```bash
cd tools/sudoku-diagrams && python3 pages.py
```

## Verifying the site

```bash
python3 tools/verify_site.py
```

Builds the routing map from `firebase.json` and checks it against what's on disk: every page has a rewrite, every rewrite points at a file that exists, no redirect leads nowhere, internal links and anchors resolve, JSON-LD parses, titles are unique and within 60 characters, meta descriptions within 165, every post carries author, byline and modification date, and HTML tags balance.

The routing check matters most: hosting serves this site through an explicit rewrite per page, so a new page without one is unreachable in production without any error appearing anywhere.

## Local development

```bash
npm run dev     # Firebase emulator on http://localhost:5000
```

## Deploying

Pushing to `main` deploys to production through GitHub Actions. Pull requests get a Firebase preview channel.

To deploy by hand:

```bash
npm run deploy
```

## Structure

```
src/            the site as served
  games/        sudoku, minesweeper, 2048
  blog/         strategy guides
  css/  js/     shared styles and scripts
  legal/        privacy policy, terms
tools/
  sudoku-diagrams/   solver, SVG renderer, page generator
  verify_site.py     pre-deploy checks
firebase.json   hosting config: rewrites, redirects, cache headers
```

## Licence

MIT.
