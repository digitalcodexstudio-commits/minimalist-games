// Re-rates bank-master.json / bank-extreme.json (written by bank.js) and writes
// src/games/sudoku/sudoku-bank.js with the boards that still rate at their level.
const S = require("../../../src/games/sudoku/sudoku-core.js"); const fs = require("fs");
const out = {};
for (const lv of ["master", "extreme"]) {
  out[lv] = require(`./bank-${lv}.json`)
    .filter(e => { const p = [...e.p].map(Number); const r = S.rate(p); return r.level === S.LEVELS[lv] && S.countSolutions(p) === 1 && r.grid.join("") === e.s; })
    .map(e => [e.p, e.s]);
  console.log(lv, out[lv].length);
}
fs.writeFileSync("../../../src/games/sudoku/sudoku-bank.js",
  "/* Master and Extreme boards, built offline by sudoku-core.js (tools/research/sudoku/bank.js).\n" +
  " * Each entry is [puzzle, solution] as 81-digit strings; the game relabels and reshuffles\n" +
  " * a random entry before showing it, so the same board never looks the same twice. */\n" +
  "window.SUDOKU_BANK = " + JSON.stringify(out) + ";\n");
