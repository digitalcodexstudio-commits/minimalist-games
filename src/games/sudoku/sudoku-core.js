/* Sudoku core: generator, solution counter and human-technique rater.
 * Shared by the game (window.SudokuCore) and by the analysis scripts (Node).
 * Every puzzle it returns has exactly one solution and can be finished by
 * logic alone using the techniques up to its difficulty level. */
(function (root) {
  'use strict';

  const ALL = 0x1FF;
  const UNITS = [];      // 27 houses, each a list of 9 cell indices
  const PEERS = [];      // 20 peers per cell
  const CELL_UNITS = []; // [row, col, box] unit indices per cell
  for (let r = 0; r < 9; r++) UNITS.push([...Array(9)].map((_, c) => r * 9 + c));
  for (let c = 0; c < 9; c++) UNITS.push([...Array(9)].map((_, r) => r * 9 + c));
  for (let b = 0; b < 9; b++) {
    const br = Math.floor(b / 3) * 3, bc = (b % 3) * 3, u = [];
    for (let i = 0; i < 9; i++) u.push((br + Math.floor(i / 3)) * 9 + bc + (i % 3));
    UNITS.push(u);
  }
  for (let i = 0; i < 81; i++) {
    const r = Math.floor(i / 9), c = i % 9, b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
    CELL_UNITS.push([r, 9 + c, 18 + b]);
    const s = new Set();
    for (const u of CELL_UNITS[i]) for (const j of UNITS[u]) if (j !== i) s.add(j);
    PEERS.push([...s]);
  }
  const POP = new Uint8Array(512);
  for (let m = 1; m < 512; m++) POP[m] = POP[m >> 1] + (m & 1);
  const bit = d => 1 << (d - 1);
  const digitOf = m => 32 - Math.clz32(m); // for single-bit masks

  // Techniques in the order a human tries them. Level = index + 1.
  // Pairs come before locked candidates to match the difficulty ladder the
  // site describes: Hard = pairs, Expert = pointing / box-line, Master =
  // triples, Extreme = X-Wing.
  const TECHNIQUES = [
    'hidden single', 'naked single', 'pair',
    'locked candidates', 'triple', 'x-wing'
  ];
  const LEVELS = { easy: 1, medium: 2, hard: 3, expert: 4, master: 5, extreme: 6 };
  // Easy boards stay generous so beginners have room to scan; the rest go as
  // low as the technique budget allows.
  const MIN_CLUES = { easy: 36, medium: 30 };

  function makeRng(seed) {
    if (seed == null) return Math.random;
    let s = seed >>> 0 || 1;
    return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
  }
  function shuffle(a, rnd) {
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }

  // ---- complete grid -------------------------------------------------------
  function solvedGrid(rnd) {
    const g = new Array(81).fill(0);
    const fill = (i) => {
      if (i === 81) return true;
      const used = PEERS[i].reduce((m, j) => (g[j] ? m | bit(g[j]) : m), 0);
      for (const d of shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9], rnd)) {
        if (used & bit(d)) continue;
        g[i] = d;
        if (fill(i + 1)) return true;
      }
      g[i] = 0;
      return false;
    };
    fill(0);
    return g;
  }

  // ---- input validation ------------------------------------------------------
  // A grid is well-formed when it has 81 cells in 0..9 and no digit repeats in
  // any row, column or box. Without this check the search below can run for
  // minutes on contradictory givens instead of answering "0 solutions".
  function isConsistent(grid) {
    if (!Array.isArray(grid) || grid.length !== 81) return false;
    for (let i = 0; i < 81; i++) {
      const v = grid[i];
      if (!Number.isInteger(v) || v < 0 || v > 9) return false;
      if (v && PEERS[i].some(j => grid[j] === v)) return false;
    }
    return true;
  }

  // ---- solution counting (stops at `limit`) --------------------------------
  // Returns the number of solutions, capped at `limit` (0 for an inconsistent grid).
  function countSolutions(grid, limit = 2) {
    if (!isConsistent(grid)) return 0;
    const g = grid.slice();
    let count = 0;
    const rec = () => {
      let best = -1, bestMask = 0, bestN = 10;
      for (let i = 0; i < 81; i++) {
        if (g[i]) continue;
        let used = 0;
        for (const j of PEERS[i]) if (g[j]) used |= bit(g[j]);
        const m = ALL & ~used, n = POP[m];
        if (n === 0) return;
        if (n < bestN) { best = i; bestMask = m; bestN = n; if (n === 1) break; }
      }
      if (best < 0) { count++; return; }
      for (let m = bestMask; m && count < limit; m &= m - 1) {
        g[best] = digitOf(m & -m);
        rec();
      }
      g[best] = 0;
    };
    rec();
    return count;
  }

  // ---- human-style solver ----------------------------------------------------
  // Returns { solved, level, steps: {technique: count}, grid }.
  // `maxLevel` stops the solver from using techniques above that level.
  function rate(grid, maxLevel = TECHNIQUES.length) {
    if (!isConsistent(grid)) return { solved: false, level: TECHNIQUES.length + 1, steps: {}, grid: grid.slice(), candidates: [] };
    const g = grid.slice();
    const cand = new Array(81).fill(0);
    for (let i = 0; i < 81; i++) {
      if (g[i]) continue;
      let used = 0;
      for (const j of PEERS[i]) if (g[j]) used |= bit(g[j]);
      cand[i] = ALL & ~used;
    }
    const steps = {};
    let level = 0, filled = g.filter(Boolean).length;
    const note = (lv) => { const t = TECHNIQUES[lv - 1]; steps[t] = (steps[t] || 0) + 1; if (lv > level) level = lv; };
    const place = (i, d) => {
      g[i] = d; cand[i] = 0; filled++;
      for (const j of PEERS[i]) cand[j] &= ~bit(d);
    };
    const broken = () => { for (let i = 0; i < 81; i++) if (!g[i] && !cand[i]) return true; return false; };

    const hiddenSingle = () => {
      for (const u of UNITS) {
        for (let d = 1; d <= 9; d++) {
          let where = -1, n = 0;
          for (const i of u) { if (g[i] === d) { n = -1; break; } if (cand[i] & bit(d)) { where = i; n++; } }
          if (n === 1) { place(where, d); return true; }
        }
      }
      return false;
    };
    const nakedSingle = () => {
      for (let i = 0; i < 81; i++) if (!g[i] && POP[cand[i]] === 1) { place(i, digitOf(cand[i])); return true; }
      return false;
    };
    const lockedCandidates = () => {
      let changed = false;
      for (let b = 18; b < 27; b++) {
        for (let d = 1; d <= 9; d++) {
          const cells = UNITS[b].filter(i => cand[i] & bit(d));
          if (cells.length < 2) continue;
          for (const k of [0, 1]) { // 0 = row, 1 = column
            const line = CELL_UNITS[cells[0]][k];
            if (!cells.every(i => CELL_UNITS[i][k] === line)) continue;
            for (const j of UNITS[line]) if (CELL_UNITS[j][2] !== b && (cand[j] & bit(d))) { cand[j] &= ~bit(d); changed = true; }
          }
        }
      }
      if (changed) return true;
      for (let l = 0; l < 18; l++) { // claiming / box-line reduction
        for (let d = 1; d <= 9; d++) {
          const cells = UNITS[l].filter(i => cand[i] & bit(d));
          if (cells.length < 2) continue;
          const box = CELL_UNITS[cells[0]][2];
          if (!cells.every(i => CELL_UNITS[i][2] === box)) continue;
          for (const j of UNITS[box]) if (!UNITS[l].includes(j) && (cand[j] & bit(d))) { cand[j] &= ~bit(d); changed = true; }
        }
      }
      return changed;
    };
    const subsets = (size) => {
      const open = new Array(9);
      for (const u of UNITS) {
        let n = 0;
        for (const i of u) if (!g[i]) open[n++] = i;
        if (n <= size) continue;
        // naked subsets: `size` cells whose candidates together are `size` digits
        const pick = (start, depth, mask, used) => {
          if (depth === size) {
            if (POP[mask] !== size) return false;
            let changed = false;
            for (let x = 0; x < n; x++) {
              const j = open[x];
              if (!(used & (1 << x)) && (cand[j] & mask)) { cand[j] &= ~mask; changed = true; }
            }
            return changed;
          }
          for (let x = start; x < n; x++) {
            const m = mask | cand[open[x]];
            if (POP[m] > size) continue;
            if (pick(x + 1, depth + 1, m, used | (1 << x))) return true;
          }
          return false;
        };
        if (pick(0, 0, 0, 0)) return true;
        // hidden subsets: `size` digits confined to `size` cells
        const where = new Array(10).fill(0);
        for (let x = 0; x < n; x++) for (let d = 1; d <= 9; d++) if (cand[open[x]] & bit(d)) where[d] |= 1 << x;
        const pickD = (start, depth, cells, dmask) => {
          if (depth === size) {
            if (POP[cells] !== size) return false;
            let changed = false;
            for (let x = 0; x < n; x++) {
              if (!(cells & (1 << x))) continue;
              const j = open[x];
              if (cand[j] & ~dmask) { cand[j] &= dmask; changed = true; }
            }
            return changed;
          }
          for (let d = start; d <= 9; d++) {
            const w = where[d];
            if (!w || POP[w] > size) continue;
            const c = cells | w;
            if (POP[c] > size) continue;
            if (pickD(d + 1, depth + 1, c, dmask | bit(d))) return true;
          }
          return false;
        };
        if (pickD(1, 0, 0, 0)) return true;
      }
      return false;
    };
    const xWing = () => {
      for (const k of [0, 1]) { // base on rows (k=0) or columns (k=1)
        for (let d = 1; d <= 9; d++) {
          const lines = [];
          for (let l = 0; l < 9; l++) {
            const pos = [];
            for (let x = 0; x < 9; x++) { const i = k ? x * 9 + l : l * 9 + x; if (cand[i] & bit(d)) pos.push(x); }
            if (pos.length === 2) lines.push([l, pos[0], pos[1]]);
          }
          for (let a = 0; a < lines.length; a++) for (let b = a + 1; b < lines.length; b++) {
            if (lines[a][1] !== lines[b][1] || lines[a][2] !== lines[b][2]) continue;
            let changed = false;
            for (const x of [lines[a][1], lines[a][2]]) for (let l = 0; l < 9; l++) {
              if (l === lines[a][0] || l === lines[b][0]) continue;
              const cell = k ? x * 9 + l : l * 9 + x;
              if (cand[cell] & bit(d)) { cand[cell] &= ~bit(d); changed = true; }
            }
            if (changed) return true;
          }
        }
      }
      return false;
    };
    const tech = [hiddenSingle, nakedSingle, () => subsets(2), lockedCandidates, () => subsets(3), xWing];

    while (filled < 81) {
      if (broken()) break;
      let progressed = false;
      for (let t = 0; t < Math.min(maxLevel, tech.length); t++) {
        if (tech[t]()) { note(t + 1); progressed = true; break; }
      }
      if (!progressed) break;
    }
    return { solved: filled === 81, level: filled === 81 ? level : TECHNIQUES.length + 1, steps, grid: g, candidates: cand };
  }

  // ---- puzzle generation -----------------------------------------------------
  // Removes clues one at a time; a removal is kept only if the puzzle stays
  // solvable by logic using techniques up to `level` (which also guarantees a
  // single solution). Accepts the board only if it actually needs `level`.
  function generate(difficulty = 'medium', opts = {}) {
    const rnd = makeRng(opts.seed);
    const target = LEVELS[difficulty] || LEVELS.medium;
    const maxAttempts = opts.maxAttempts || 400;
    let best = null;
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      const solution = solvedGrid(rnd);
      const puzzle = solution.slice();
      const floor = MIN_CLUES[difficulty] || 17;
      let clues = 81;
      for (const i of shuffle([...Array(81).keys()], rnd)) {
        if (clues <= floor) break;
        const keep = puzzle[i];
        puzzle[i] = 0;
        if (rate(puzzle, target).solved) clues--; else puzzle[i] = keep;
      }
      const r = rate(puzzle, target);
      // Safety net, independent of the human solver: the board MUST have one solution.
      if (countSolutions(puzzle, 2) !== 1) continue;
      const result = {
        puzzle, solution, level: r.level, target, reachedTarget: r.level === target,
        clues: puzzle.filter(Boolean).length, attempts: attempt, steps: r.steps
      };
      if (result.reachedTarget) return result;
      if (!best || r.level > best.level) best = result;
    }
    // Closest found (never above the requested level). Callers must check
    // `reachedTarget` before labelling the board with the requested difficulty.
    return best;
  }

  // Relabels digits and shuffles rows, columns, bands and stacks (and maybe
  // transposes). The result is a different-looking board with exactly the
  // same logical structure, so its difficulty rating is unchanged.
  function transform(puzzle, solution, rnd = Math.random) {
    const digits = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9], rnd);
    const perm = () => {
      const out = [];
      for (const band of shuffle([0, 1, 2], rnd)) for (const k of shuffle([0, 1, 2], rnd)) out.push(band * 3 + k);
      return out;
    };
    const rows = perm(), cols = perm(), flip = rnd() < 0.5;
    const map = (g) => {
      const out = new Array(81);
      for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) {
        const sr = flip ? cols[c] : rows[r], sc = flip ? rows[r] : cols[c];
        const v = g[sr * 9 + sc];
        out[r * 9 + c] = v ? digits[v - 1] : 0;
      }
      return out;
    };
    return { puzzle: map(puzzle), solution: map(solution) };
  }

  const api = { generate, isConsistent, transform, MIN_CLUES, rate, countSolutions, solvedGrid, TECHNIQUES, LEVELS, makeRng };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SudokuCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
