(function () {
  'use strict';

  const SIZE = 9;
  const BOX = 3;
  const CLUES_BY_DIFFICULTY = { easy: 45, medium: 35, hard: 25 };

  function cloneBoard(b) { return b.map(row => row.slice()); }
  function shuffled(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  class SudokuEngine {
    constructor() {
      this.solution = null;
      this.board = null;
      this.clues = null;
    }

    static isValid(b, row, col, num) {
      for (let i = 0; i < SIZE; i++) {
        if (b[row][i] === num) return false;
        if (b[i][col] === num) return false;
      }
      const br = Math.floor(row / BOX) * BOX;
      const bc = Math.floor(col / BOX) * BOX;
      for (let r = br; r < br + BOX; r++) {
        for (let c = bc; c < bc + BOX; c++) {
          if (b[r][c] === num) return false;
        }
      }
      return true;
    }

    fill(b) {
      for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
          if (b[r][c] === 0) {
            for (const n of shuffled([1,2,3,4,5,6,7,8,9])) {
              if (SudokuEngine.isValid(b, r, c, n)) {
                b[r][c] = n;
                if (this.fill(b)) return true;
                b[r][c] = 0;
              }
            }
            return false;
          }
        }
      }
      return true;
    }

    generate(difficulty) {
      const empty = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
      this.fill(empty);
      this.solution = cloneBoard(empty);

      const puzzle = cloneBoard(empty);
      const targetClues = CLUES_BY_DIFFICULTY[difficulty] ?? CLUES_BY_DIFFICULTY.medium;
      const toRemove = SIZE * SIZE - targetClues;

      const positions = shuffled(
        Array.from({ length: SIZE * SIZE }, (_, i) => [Math.floor(i / SIZE), i % SIZE])
      );
      for (let i = 0; i < toRemove; i++) {
        const [r, c] = positions[i];
        puzzle[r][c] = 0;
      }

      this.board = puzzle;
      this.clues = puzzle.map(row => row.map(v => v !== 0));
      return this.board;
    }

    setCell(row, col, num) {
      if (this.clues[row][col]) return false;
      this.board[row][col] = num;
      return true;
    }

    isFilled() {
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) if (this.board[r][c] === 0) return false;
      return true;
    }

    isSolved() {
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) if (this.board[r][c] !== this.solution[r][c]) return false;
      return true;
    }

    getHint() {
      const empties = [];
      for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
          if (this.board[r][c] !== this.solution[r][c]) empties.push([r, c]);
        }
      }
      if (empties.length === 0) return null;
      const [r, c] = empties[Math.floor(Math.random() * empties.length)];
      this.board[r][c] = this.solution[r][c];
      return { row: r, col: c, value: this.solution[r][c] };
    }
  }

  class SudokuUI {
    constructor(root, engine) {
      this.root = root;
      this.engine = engine;
      this.selected = null;
      this.difficulty = 'medium';
      this.errors = 0;
      this.hintsLeft = 3;
      this.startTime = null;
      this.timerId = null;
      this.running = false;

      this.gridEl = root.querySelector('[data-grid]');
      this.timerEl = root.querySelector('[data-timer]');
      this.errorsEl = root.querySelector('[data-errors]');
      this.hintsEl = root.querySelector('[data-hints]');
      this.statusEl = root.querySelector('[data-status]');
      this.modalEl = root.querySelector('[data-modal]');
      this.modalTimeEl = root.querySelector('[data-modal-time]');

      this.bindControls();
      this.bindKeyboard();
      this.renderGrid();
      this.newGame();
    }

    bindControls() {
      this.root.querySelectorAll('[data-difficulty]').forEach(btn => {
        btn.addEventListener('click', () => {
          this.difficulty = btn.dataset.difficulty;
          this.root.querySelectorAll('[data-difficulty]').forEach(b =>
            b.setAttribute('aria-pressed', String(b === btn))
          );
          this.newGame();
        });
      });
      this.root.querySelector('[data-action="new"]').addEventListener('click', () => this.newGame());
      this.root.querySelector('[data-action="check"]').addEventListener('click', () => this.checkSolution());
      this.root.querySelector('[data-action="hint"]').addEventListener('click', () => this.useHint());
      this.root.querySelectorAll('[data-num]').forEach(btn => {
        btn.addEventListener('click', () => {
          const v = btn.dataset.num === 'clear' ? 0 : Number(btn.dataset.num);
          this.inputNumber(v);
        });
      });
      this.root.querySelector('[data-modal-close]').addEventListener('click', () => {
        this.modalEl.hidden = true;
        this.newGame();
      });
    }

    bindKeyboard() {
      document.addEventListener('keydown', (e) => {
        if (!this.selected) return;
        if (e.key >= '1' && e.key <= '9') { this.inputNumber(Number(e.key)); e.preventDefault(); return; }
        if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') { this.inputNumber(0); e.preventDefault(); return; }
        const [r, c] = this.selected;
        const map = { ArrowUp: [-1,0], ArrowDown: [1,0], ArrowLeft: [0,-1], ArrowRight: [0,1] };
        if (map[e.key]) {
          const [dr, dc] = map[e.key];
          const nr = Math.max(0, Math.min(8, r + dr));
          const nc = Math.max(0, Math.min(8, c + dc));
          this.select(nr, nc);
          e.preventDefault();
        }
      });
    }

    renderGrid() {
      this.gridEl.innerHTML = '';
      for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
          const cell = document.createElement('button');
          cell.type = 'button';
          cell.className = 'cell';
          cell.dataset.row = String(r);
          cell.dataset.col = String(c);
          if (c % 3 === 0) cell.classList.add('border-left');
          if (r % 3 === 0) cell.classList.add('border-top');
          if (c === 8) cell.classList.add('border-right');
          if (r === 8) cell.classList.add('border-bottom');
          cell.addEventListener('click', () => this.select(r, c));
          this.gridEl.appendChild(cell);
        }
      }
    }

    select(r, c) {
      this.selected = [r, c];
      this.gridEl.querySelectorAll('.cell').forEach(el => {
        const er = Number(el.dataset.row);
        const ec = Number(el.dataset.col);
        el.classList.toggle('selected', er === r && ec === c);
        el.classList.toggle('peer',
          (er === r || ec === c ||
            (Math.floor(er/3) === Math.floor(r/3) && Math.floor(ec/3) === Math.floor(c/3)))
          && !(er === r && ec === c)
        );
      });
    }

    inputNumber(n) {
      if (!this.selected) return;
      const [r, c] = this.selected;
      if (this.engine.clues[r][c]) return;
      if (n !== 0 && this.engine.solution[r][c] !== n) {
        this.errors++;
        this.errorsEl.textContent = String(this.errors);
      }
      this.engine.setCell(r, c, n);
      this.refreshCell(r, c);
      if (this.engine.isFilled() && this.engine.isSolved()) this.win();
    }

    refreshCell(r, c) {
      const el = this.gridEl.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`);
      const v = this.engine.board[r][c];
      el.textContent = v === 0 ? '' : String(v);
      el.classList.toggle('clue', this.engine.clues[r][c]);
      const wrong = v !== 0 && v !== this.engine.solution[r][c];
      el.classList.toggle('wrong', wrong);
    }

    refreshAll() {
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) this.refreshCell(r, c);
    }

    useHint() {
      if (this.hintsLeft <= 0) return;
      const hint = this.engine.getHint();
      if (!hint) return;
      this.hintsLeft--;
      this.hintsEl.textContent = String(this.hintsLeft);
      this.refreshCell(hint.row, hint.col);
      if (this.engine.isFilled() && this.engine.isSolved()) this.win();
    }

    checkSolution() {
      if (!this.engine.isFilled()) {
        this.setStatus('Grid not complete yet.');
        return;
      }
      if (this.engine.isSolved()) {
        this.win();
      } else {
        this.setStatus('Not quite right — keep trying.');
      }
    }

    setStatus(msg) {
      this.statusEl.textContent = msg;
      clearTimeout(this._statusTimer);
      this._statusTimer = setTimeout(() => (this.statusEl.textContent = ''), 2500);
    }

    newGame() {
      this.engine.generate(this.difficulty);
      this.selected = null;
      this.errors = 0;
      this.hintsLeft = 3;
      this.errorsEl.textContent = '0';
      this.hintsEl.textContent = '3';
      this.setStatus('');
      this.refreshAll();
      this.startTimer();
      this.modalEl.hidden = true;
    }

    startTimer() {
      this.stopTimer();
      this.startTime = Date.now();
      this.running = true;
      this.renderTimer();
      this.timerId = setInterval(() => this.renderTimer(), 1000);
    }

    stopTimer() {
      if (this.timerId) clearInterval(this.timerId);
      this.timerId = null;
      this.running = false;
    }

    renderTimer() {
      const s = Math.floor((Date.now() - this.startTime) / 1000);
      const mm = String(Math.floor(s / 60)).padStart(2, '0');
      const ss = String(s % 60).padStart(2, '0');
      this.timerEl.textContent = `${mm}:${ss}`;
    }

    win() {
      this.stopTimer();
      this.modalTimeEl.textContent = this.timerEl.textContent;
      this.modalEl.hidden = false;
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const root = document.querySelector('[data-sudoku]');
    if (!root) return;
    new SudokuUI(root, new SudokuEngine());
  });
})();
