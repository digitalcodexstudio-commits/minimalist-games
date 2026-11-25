/** @jest-environment jsdom */
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', '..', 'src', 'games', 'sudoku');
const read = f => fs.readFileSync(path.join(dir, f), 'utf8');

function boot() {
  const html = read('index.html');
  document.body.innerHTML = html.slice(html.indexOf('<body>') + 6, html.indexOf('<script src="/src/games/sudoku/sudoku-core.js'));
  (0, eval)(read('sudoku-core.js'));
  (0, eval)(read('sudoku-bank.js'));
  // expose the UI instance for white-box assertions
  (0, eval)(read('sudoku.js').replace('new SudokuUI(root, new SudokuEngine());', 'window.__ui = new SudokuUI(root, new SudokuEngine());'));
  document.dispatchEvent(new Event('DOMContentLoaded'));
  return window.__ui;
}
const key = (k, o = {}) => document.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true, ...o }));

beforeEach(() => { jest.useFakeTimers(); window.mgTrack = jest.fn(); });
afterEach(() => { jest.useRealTimers(); });

test('game boots and renders 81 cells with a valid, unique puzzle', () => {
  const ui = boot();
  expect(document.querySelectorAll('[data-grid] > *').length).toBe(81);
  const flat = ui.engine.board.flat();
  expect(window.SudokuCore.countSolutions(flat, 2)).toBe(1);
});

test('BUG L151: pressing P twice does not resume (keyboard cannot un-pause)', () => {
  const ui = boot();
  key('p'); expect(ui.paused).toBe(true);
  key('p');
  expect(ui.paused).toBe(false); // FAILS today: handler returns early while paused
});

test('BUG L400-403: a WRONG digit counts towards hiding that pad button', () => {
  const ui = boot();
  const d = 5, B = ui.engine.board, S = ui.engine.solution;
  // place the 8 other copies correctly + one wrong 5 in another cell
  let placed = 0;
  for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (B[r][c] === d) placed++;
  const empties = [];
  for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (B[r][c] === 0) empties.push([r, c]);
  for (const [r, c] of empties) { if (placed >= 8) break; if (S[r][c] === d) { B[r][c] = d; placed++; } }
  const wrongCell = empties.find(([r, c]) => B[r][c] === 0 && S[r][c] !== d);
  B[wrongCell[0]][wrongCell[1]] = d; // wrong 5 -> board now shows nine 5s
  ui.updateCounter();
  const btn = document.querySelector(`[data-num="${d}"]`);
  expect(btn.classList.contains('is-hidden')).toBe(false); // FAILS today: button vanishes though one 5 is still missing
});

test('Sudoku page does not persist anything although the copy says it does', () => {
  boot();
  const spy = jest.spyOn(Storage.prototype, 'setItem');
  const ui = window.__ui;
  ui.select(0, 0); key('1'); key('2'); jest.advanceTimersByTime(5000);
  const claims = /remembers your game locally|Your current game, statistics and settings are stored locally/.test(read('index.html'));
  expect(claims).toBe(true);
  expect(spy).not.toHaveBeenCalled(); // documents the mismatch copy <-> code
});

test('three wrong digits end the game and fire game_lose', () => {
  const ui = boot();
  const cells = [];
  for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (!ui.engine.clues[r][c]) cells.push([r, c]);
  for (let i = 0; i < 3; i++) { const [r, c] = cells[i]; ui.select(r, c); ui.inputNumber(ui.engine.solution[r][c] % 9 + 1); }
  expect(ui.gameOver).toBe(true);
  expect(window.mgTrack).toHaveBeenCalledWith('game_lose', expect.any(Object));
});

test('solving the board fires game_win', () => {
  const ui = boot();
  for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (!ui.engine.clues[r][c]) { ui.select(r, c); ui.inputNumber(ui.engine.solution[r][c]); }
  expect(ui.gameOver).toBe(true);
  expect(window.mgTrack).toHaveBeenCalledWith('game_win', expect.any(Object));
});

test.each(['easy', 'medium', 'hard', 'expert', 'master', 'extreme'])('%s: newGame yields a unique-solution board', d => {
  const ui = boot();
  document.querySelector(`[data-difficulty="${d}"]`).click();
  expect(window.SudokuCore.countSolutions(ui.engine.board.flat(), 2)).toBe(1);
});
