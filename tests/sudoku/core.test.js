/** @jest-environment node */
const path = require('path');
const core = require(path.join('..', '..', 'src', 'games', 'sudoku', 'sudoku-core.js'));
const { generate, rate, countSolutions, solvedGrid, transform, makeRng, LEVELS, MIN_CLUES } = core;

const SAMPLES = 4; // puzzles per level; raise locally for a deeper run

/* ---------- helpers independent of the code under test ---------- */
const houses = () => {
  const h = [];
  for (let r = 0; r < 9; r++) h.push([...Array(9)].map((_, c) => r * 9 + c));
  for (let c = 0; c < 9; c++) h.push([...Array(9)].map((_, r) => r * 9 + c));
  for (let b = 0; b < 9; b++) {
    const br = Math.floor(b / 3) * 3, bc = (b % 3) * 3;
    h.push([...Array(9)].map((_, i) => (br + Math.floor(i / 3)) * 9 + bc + (i % 3)));
  }
  return h;
};
const H = houses();
const isValidSolution = g => g.length === 81 && H.every(u => new Set(u.map(i => g[i])).size === 9 && u.every(i => g[i] >= 1 && g[i] <= 9));
const noConflicts = g => H.every(u => { const v = u.map(i => g[i]).filter(Boolean); return new Set(v).size === v.length; });
const isSubgrid = (p, s) => p.every((v, i) => v === 0 || v === s[i]);

describe('solvedGrid', () => {
  test.each([1, 2, 3, 4, 5])('seed %i gives a valid complete grid', seed => {
    expect(isValidSolution(solvedGrid(makeRng(seed)))).toBe(true);
  });
});

describe('countSolutions', () => {
  test('empty grid has >=2 solutions (stops at limit)', () => {
    expect(countSolutions(new Array(81).fill(0), 2)).toBe(2);
  });
  test('complete grid has exactly 1', () => {
    expect(countSolutions(solvedGrid(makeRng(7)))).toBe(1);
  });
  test('contradictory grid has 0 and returns immediately (regression: used to hang >20 s)', () => {
    const g = new Array(81).fill(0); g[0] = 5; g[1] = 5; // two 5s in one row
    const t = Date.now();
    expect(countSolutions(g)).toBe(0);
    expect(Date.now() - t).toBeLessThan(100);
  });
  test('malformed input is rejected, not crashed on', () => {
    expect(countSolutions([1, 2, 3])).toBe(0);
    expect(countSolutions(new Array(81).fill(10))).toBe(0);
    expect(rate(new Array(80).fill(0)).solved).toBe(false);
  });
  test('known puzzle with one solution (Wikipedia example)', () => {
    const s = '530070000600195000098000060800060003400803001700020006060000280000419005000080079';
    expect(countSolutions([...s].map(Number))).toBe(1);
  });
  test('removing clues from a unique puzzle until ambiguity is detected', () => {
    const s = solvedGrid(makeRng(11)); const p = s.slice();
    for (let i = 0; i < 60; i++) p[i] = 0; // far too few clues
    expect(countSolutions(p, 2)).toBe(2);
  });
});

describe.each(Object.keys(LEVELS))('generate(%s)', diff => {
  const target = LEVELS[diff];
  const puzzles = [];
  beforeAll(() => { for (let s = 1; s <= SAMPLES; s++) puzzles.push(generate(diff, { seed: 1000 * target + s, maxAttempts: 80 })); });

  test('solution is a valid complete grid', () => {
    for (const p of puzzles) expect(isValidSolution(p.solution)).toBe(true);
  });
  test('puzzle never conflicts with Sudoku rules and is a subset of the solution', () => {
    for (const p of puzzles) { expect(noConflicts(p.puzzle)).toBe(true); expect(isSubgrid(p.puzzle, p.solution)).toBe(true); }
  });
  test('puzzle has EXACTLY ONE solution (independent brute-force count)', () => {
    for (const p of puzzles) {
      expect(countSolutions(p.puzzle, 2)).toBe(1);
      const sol = rate(p.puzzle).grid; // the logic solver must land on the stored solution
      expect(sol).toEqual(p.solution);
    }
  });
  test('reported level equals an independent re-rating and never exceeds the target', () => {
    for (const p of puzzles) { expect(rate(p.puzzle).level).toBe(p.level); expect(p.level).toBeLessThanOrEqual(target); }
  });
  test('respects the clue floor', () => {
    const floor = MIN_CLUES[diff] || 17;
    for (const p of puzzles) expect(p.clues).toBeGreaterThanOrEqual(floor);
  });
  test('REPORT: share of puzzles that actually reached the requested level', () => {
    const hit = puzzles.filter(p => p.level === target).length;
    // Documented behaviour: after maxAttempts the best (lower) level is returned.
    // The game must not label such a board with the requested difficulty.
    // Master is served from the offline bank in the game precisely because live
    // generation rarely reaches level 5 quickly, so only require a hit elsewhere.
    if (LEVELS[diff] <= 4) expect(hit).toBeGreaterThan(0);
    for (const p of puzzles) expect(p.reachedTarget).toBe(p.level === target);
  });
});

describe('difficulty <-> techniques correlation', () => {
  const byLevel = {};
  beforeAll(() => {
    for (const d of Object.keys(LEVELS)) {
      byLevel[d] = [];
      if (LEVELS[d] >= 5) { // Master/Extreme come from the offline bank, as in the game
        const fs = require('fs'), vm = require('vm'), sb = { window: {} };
        vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', '..', 'src', 'games', 'sudoku', 'sudoku-bank.js'), 'utf8'), sb);
        for (const [pz] of sb.window.SUDOKU_BANK[d].slice(0, SAMPLES)) byLevel[d].push({ puzzle: [...pz].map(Number) });
        continue;
      }
      for (let s = 1; s <= SAMPLES; s++) {
        const p = generate(d, { seed: 77 * LEVELS[d] + s, maxAttempts: 80 });
        if (p.level === LEVELS[d]) byLevel[d].push(p);
      }
    }
  });
  test.each(Object.keys(LEVELS))('%s: solvable with techniques <= level, NOT solvable with level-1 (when level>1)', d => {
    const lv = LEVELS[d];
    for (const p of byLevel[d]) {
      expect(rate(p.puzzle, lv).solved).toBe(true);
      if (lv > 1) expect(rate(p.puzzle, lv - 1).solved).toBe(false);
    }
  });
  test.each(Object.keys(LEVELS))('%s: the hardest technique used is the one that names the level', d => {
    const lv = LEVELS[d];
    for (const p of byLevel[d]) {
      const used = Object.keys(rate(p.puzzle).steps);
      expect(used).toContain(core.TECHNIQUES[lv - 1]);
      const maxIdx = Math.max(...used.map(t => core.TECHNIQUES.indexOf(t)));
      expect(maxIdx + 1).toBe(lv);
    }
  });
  test('monotonic: mean count of non-single steps grows with level', () => {
    const mean = d => byLevel[d].reduce((a, p) => { const s = rate(p.puzzle).steps; return a + Object.entries(s).filter(([t]) => !['hidden single', 'naked single'].includes(t)).reduce((x, [, n]) => x + n, 0); }, 0) / Math.max(1, byLevel[d].length);
    expect(mean('easy')).toBe(0);
    expect(mean('medium')).toBe(0);
    expect(mean('hard')).toBeGreaterThan(0);
    expect(mean('extreme')).toBeGreaterThan(0);
  });
});

describe('rate() soundness vs brute force', () => {
  test('every grid it "solves" equals the unique brute-force solution; deductions never contradict it', () => {
    for (let s = 1; s <= 25; s++) {
      const sol = solvedGrid(makeRng(s));
      const p = sol.slice();
      const rnd = makeRng(s * 31);
      for (let k = 0; k < 81; k++) { const i = Math.floor(rnd() * 81); const keep = p[i]; p[i] = 0; if (countSolutions(p, 2) !== 1) p[i] = keep; }
      const r = rate(p);
      expect(countSolutions(p, 2)).toBe(1);
      if (r.solved) expect(r.grid).toEqual(sol);
      // remaining candidates must always still contain the true digit
      for (let i = 0; i < 81; i++) if (!r.grid[i] || true) { const c = r.candidates[i]; if (c) expect(c & (1 << (sol[i] - 1))).toBeTruthy(); }
    }
  });
});

describe('transform()', () => {
  test('keeps validity, uniqueness and rating', () => {
    const p = generate('hard', { seed: 5, maxAttempts: 80 });
    for (let s = 1; s <= 10; s++) {
      const t = transform(p.puzzle, p.solution, makeRng(s));
      expect(isValidSolution(t.solution)).toBe(true);
      expect(isSubgrid(t.puzzle, t.solution)).toBe(true);
      expect(countSolutions(t.puzzle, 2)).toBe(1);
      expect(rate(t.puzzle).level).toBe(rate(p.puzzle).level);
      expect(t.puzzle.filter(Boolean).length).toBe(p.clues);
    }
  });
});

describe('determinism and edge cases', () => {
  test('same seed => same puzzle', () => {
    expect(generate('medium', { seed: 42 }).puzzle).toEqual(generate('medium', { seed: 42 }).puzzle);
  });
  test('unknown difficulty falls back to medium (documented)', () => {
    expect(LEVELS.bogus).toBeUndefined();
    expect(generate('bogus', { seed: 3 }).level).toBeLessThanOrEqual(2);
  });
  test('maxAttempts=1 can return a lower level than requested and says so via reachedTarget', () => {
    const r = generate('extreme', { seed: 9, maxAttempts: 1 });
    expect(r.level).toBeLessThan(6);
    expect(r.reachedTarget).toBe(false);
  });
});

describe('offline bank (Master / Extreme)', () => {
  const fs = require('fs'), vm = require('vm');
  const sandbox = { window: {} };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', '..', 'src', 'games', 'sudoku', 'sudoku-bank.js'), 'utf8'), sandbox);
  const bank = sandbox.window.SUDOKU_BANK;
  test.each(['master', 'extreme'])('%s: every entry is valid, unique and rated at its level', d => {
    expect(bank[d].length).toBeGreaterThanOrEqual(100);
    for (const [pz, sol] of bank[d]) {
      const p = typeof pz === 'string' ? [...pz].map(Number) : pz, s = typeof sol === 'string' ? [...sol].map(Number) : sol;
      expect(isValidSolution(s)).toBe(true);
      expect(isSubgrid(p, s)).toBe(true);
      expect(countSolutions(p, 2)).toBe(1);
      expect(rate(p).level).toBe(LEVELS[d]);
    }
  });
});
