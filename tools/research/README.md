# Research simulations

The numbers in the blog's data posts come from these programs. Each one runs the
exact rules of the game on minimalist-games.com, so anyone can re-run them.

## Minesweeper — `minesweeper/minesweeper_sim.c`

A bot that never makes a logical mistake: certain moves first, then full enumeration
of every mine arrangement consistent with the board and the global mine count, and
only then a guess on the cell with the lowest exact mine probability. First click and
its eight neighbours are always safe, as in the game.

```bash
cd tools/research/minesweeper && gcc -O2 -o sim minesweeper_sim.c -lm
./sim 9 9 10 100000 center 11      # rows cols mines games first-click(corner|edge|center) seed
./sim 16 16 40 100000 center 12
./sim 16 30 99 50000 center 13
```

Used in: *How Much of Minesweeper Is Luck?* (`/blog/minesweeper-luck-vs-skill`).

## 2048 — `2048/2048_sim.c`

Six players, from random to a two-move expectimax search. Spawns are 2 (90%) or 4 (10%).

```bash
cd tools/research/2048 && gcc -O3 -march=native -o sim 2048_sim.c -lm
./sim 0 100000 100       # strategy games seed [depth]
./sim 4 300 204 2        # 0 random, 1 corner recipe, 2 down-right spam, 3 greedy,
./sim 5 300 205 2        # 4 lookahead, 5 lookahead without up unless forced
```

One line per game: strategy, max tile, score, moves, moves to 1024, moves to 2048,
up/down/left/right counts, max tile in a corner at the end, moves with the max tile in
a corner, corner changes, score at 2048.

Used in: *We Tested Every 2048 Strategy* (`/blog/2048-strategies-tested`).

## Sudoku — `sudoku/`

All three scripts use the game's own generator and rater, `src/games/sudoku/sudoku-core.js`.

```bash
cd tools/research/sudoku
node classic.js 4000 99 > classic.jsonl   # minimal puzzles, rated by technique
node levels.js                            # clue counts of the game's own levels
node bank.js master 150 1 && node bank.js extreme 150 7 && node build_bank.js
```

Used in: *Fewer Clues Doesn't Mean a Harder Sudoku* (`/blog/sudoku-difficulty-clue-count`).
