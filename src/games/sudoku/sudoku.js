(function () {
  'use strict';

  const SIZE = 9;
  const BOX = 3;
  const CLUES_BY_DIFFICULTY = {
    easy: 45, medium: 38, hard: 32, expert: 28, master: 25, extreme: 22
  };
  const MISTAKES_LIMIT = 3;

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
      this.notes = null;
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
      this.notes = Array.from({ length: SIZE }, () =>
        Array.from({ length: SIZE }, () => new Set())
      );
      return this.board;
    }

    isFilled() {
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) if (this.board[r][c] === 0) return false;
      return true;
    }

    isSolved() {
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) if (this.board[r][c] !== this.solution[r][c]) return false;
      return true;
    }

    findHintCell() {
      const empties = [];
      for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
          if (this.board[r][c] !== this.solution[r][c]) empties.push([r, c]);
        }
      }
      if (empties.length === 0) return null;
      const [r, c] = empties[Math.floor(Math.random() * empties.length)];
      return { row: r, col: c, value: this.solution[r][c] };
    }
  }

  class SudokuUI {
    constructor(root, engine) {
      this.root = root;
      this.engine = engine;
      this.selected = null;
      this.difficulty = 'easy';
      this.mistakes = 0;
      this.hintsLeft = 3;
      this.notesMode = false;
      this.paused = false;
      this.history = [];
      this.startTime = null;
      this.elapsed = 0;
      this.timerId = null;
      this.gameOver = false;

      this.gridEl = root.querySelector('[data-grid]');
      this.timerEl = root.querySelector('[data-timer]');
      this.mistakesEl = root.querySelector('[data-mistakes]');
      this.counterEl = root.querySelector('[data-counter]');
      this.hintsEl = root.querySelector('[data-hints-left]');
      this.modalEl = root.querySelector('[data-modal]');
      this.modalTitleEl = root.querySelector('[data-modal-title]');
      this.modalMsgEl = root.querySelector('[data-modal-msg]');
      this.modalTimeEl = root.querySelector('[data-modal-time]');
      this.pauseOverlay = root.querySelector('[data-pause-overlay]');
      this.notesBtn = root.querySelector('[data-action="notes"]');
      this.notesIndicator = root.querySelector('[data-notes-state]');
      this.pauseBtn = root.querySelector('[data-action="pause"]');

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
            b.classList.toggle('is-active', b === btn)
          );
          this.newGame();
        });
      });
      this.root.querySelector('[data-action="new"]').addEventListener('click', () => this.newGame());
      this.root.querySelector('[data-action="undo"]').addEventListener('click', () => this.undo());
      this.root.querySelector('[data-action="erase"]').addEventListener('click', () => this.eraseSelected());
      this.root.querySelector('[data-action="notes"]').addEventListener('click', () => this.toggleNotes());
      this.root.querySelector('[data-action="hint"]').addEventListener('click', () => this.useHint());
      this.root.querySelector('[data-action="pause"]').addEventListener('click', () => this.togglePause());
      this.root.querySelectorAll('[data-num]').forEach(btn => {
        btn.addEventListener('click', () => this.inputNumber(Number(btn.dataset.num)));
      });
      this.root.querySelector('[data-modal-close]').addEventListener('click', () => {
        this.modalEl.hidden = true;
        this.newGame();
      });
    }

    bindKeyboard() {
      document.addEventListener('keydown', (e) => {
        if (this.paused || this.gameOver) return;
        if (e.key === 'n' || e.key === 'N') { this.toggleNotes(); e.preventDefault(); return; }
        if (e.key === 'p' || e.key === 'P') { this.togglePause(); e.preventDefault(); return; }
        if (e.key === 'z' && (e.metaKey || e.ctrlKey)) { this.undo(); e.preventDefault(); return; }
        if (!this.selected) return;
        if (e.key >= '1' && e.key <= '9') { this.inputNumber(Number(e.key)); e.preventDefault(); return; }
        if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') { this.eraseSelected(); e.preventDefault(); return; }
        const [r, c] = this.selected;
        const map = { ArrowUp: [-1,0], ArrowDown: [1,0], ArrowLeft: [0,-1], ArrowRight: [0,1] };
        if (map[e.key]) {
          const [dr, dc] = map[e.key];
          this.select(Math.max(0, Math.min(8, r + dr)), Math.max(0, Math.min(8, c + dc)));
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
          const boxIdx = Math.floor(r / 3) * 3 + Math.floor(c / 3);
          if (boxIdx % 2 === 1) cell.classList.add('box-alt');
          if (c % 3 === 0 && c !== 0) cell.classList.add('bx-left');
          if (r % 3 === 0 && r !== 0) cell.classList.add('bx-top');

          const value = document.createElement('span');
          value.className = 'cell-value';
          cell.appendChild(value);

          const notes = document.createElement('span');
          notes.className = 'cell-notes';
          for (let n = 1; n <= 9; n++) {
            const dot = document.createElement('span');
            dot.className = 'cell-note';
            dot.dataset.note = String(n);
            notes.appendChild(dot);
          }
          cell.appendChild(notes);

          cell.addEventListener('click', () => this.select(r, c));
          this.gridEl.appendChild(cell);
        }
      }
    }

    select(r, c) {
      if (this.paused || this.gameOver) return;
      this.selected = [r, c];
      const selVal = this.engine.board[r][c];
      this.gridEl.querySelectorAll('.cell').forEach(el => {
        const er = Number(el.dataset.row);
        const ec = Number(el.dataset.col);
        const same = er === r && ec === c;
        const peer =
          er === r || ec === c ||
          (Math.floor(er/3) === Math.floor(r/3) && Math.floor(ec/3) === Math.floor(c/3));
        el.classList.toggle('selected', same);
        el.classList.toggle('peer', peer && !same);
        const v = this.engine.board[er][ec];
        el.classList.toggle('same-value', selVal !== 0 && v === selVal && !same);
      });
    }

    inputNumber(n) {
      if (this.paused || this.gameOver || !this.selected) return;
      const [r, c] = this.selected;
      if (this.engine.clues[r][c]) return;

      if (this.notesMode) {
        const set = this.engine.notes[r][c];
        const snapshot = { type: 'note', r, c, before: new Set(set) };
        if (this.engine.board[r][c] !== 0) {
          snapshot.prevValue = this.engine.board[r][c];
          this.engine.board[r][c] = 0;
        }
        if (set.has(n)) set.delete(n); else set.add(n);
        this.history.push(snapshot);
        this.refreshCell(r, c);
        return;
      }

      const prev = this.engine.board[r][c];
      const prevNotes = new Set(this.engine.notes[r][c]);
      this.engine.board[r][c] = n;
      this.engine.notes[r][c].clear();
      this.history.push({ type: 'value', r, c, prev, prevNotes });

      const wrong = this.engine.solution[r][c] !== n;
      if (wrong) {
        this.mistakes++;
        this.updateMistakes();
        if (this.mistakes >= MISTAKES_LIMIT) {
          this.refreshCell(r, c);
          this.loseGame();
          return;
        }
      }
      this.refreshCell(r, c);
      this.select(r, c);
      this.updateCounter();
      if (this.engine.isFilled() && this.engine.isSolved()) this.win();
    }

    eraseSelected() {
      if (this.paused || this.gameOver || !this.selected) return;
      const [r, c] = this.selected;
      if (this.engine.clues[r][c]) return;
      const prev = this.engine.board[r][c];
      const prevNotes = new Set(this.engine.notes[r][c]);
      if (prev === 0 && prevNotes.size === 0) return;
      this.engine.board[r][c] = 0;
      this.engine.notes[r][c].clear();
      this.history.push({ type: 'erase', r, c, prev, prevNotes });
      this.refreshCell(r, c);
      this.select(r, c);
      this.updateCounter();
    }

    undo() {
      if (this.paused || this.gameOver) return;
      const m = this.history.pop();
      if (!m) return;
      if (m.type === 'note') {
        this.engine.notes[m.r][m.c] = new Set(m.before);
        if (m.prevValue !== undefined) this.engine.board[m.r][m.c] = m.prevValue;
      } else {
        this.engine.board[m.r][m.c] = m.prev;
        this.engine.notes[m.r][m.c] = new Set(m.prevNotes);
      }
      this.refreshCell(m.r, m.c);
      this.updateCounter();
    }

    toggleNotes() {
      this.notesMode = !this.notesMode;
      this.notesBtn.classList.toggle('is-active', this.notesMode);
      if (this.notesIndicator) this.notesIndicator.textContent = this.notesMode ? 'ON' : 'OFF';
    }

    useHint() {
      if (this.paused || this.gameOver || this.hintsLeft <= 0) return;
      const hint = this.engine.findHintCell();
      if (!hint) return;
      const { row, col, value } = hint;
      const prev = this.engine.board[row][col];
      const prevNotes = new Set(this.engine.notes[row][col]);
      this.engine.board[row][col] = value;
      this.engine.notes[row][col].clear();
      this.history.push({ type: 'value', r: row, c: col, prev, prevNotes });
      this.hintsLeft--;
      this.hintsEl.textContent = String(this.hintsLeft);
      this.refreshCell(row, col);
      this.updateCounter();
      if (this.engine.isFilled() && this.engine.isSolved()) this.win();
    }

    togglePause() {
      if (this.gameOver) return;
      this.paused = !this.paused;
      if (this.paused) {
        this.stopTimer();
        this.pauseOverlay.hidden = false;
        this.pauseBtn.classList.add('is-active');
      } else {
        this.pauseOverlay.hidden = true;
        this.pauseBtn.classList.remove('is-active');
        this.resumeTimer();
      }
    }

    refreshCell(r, c) {
      const el = this.gridEl.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`);
      const v = this.engine.board[r][c];
      const valueEl = el.querySelector('.cell-value');
      const notesEl = el.querySelector('.cell-notes');
      if (v === 0) {
        valueEl.textContent = '';
        notesEl.hidden = false;
        const set = this.engine.notes[r][c];
        notesEl.querySelectorAll('.cell-note').forEach(dot => {
          dot.textContent = set.has(Number(dot.dataset.note)) ? dot.dataset.note : '';
        });
      } else {
        valueEl.textContent = String(v);
        notesEl.hidden = true;
      }
      el.classList.toggle('clue', this.engine.clues[r][c]);
      const wrong = v !== 0 && !this.engine.clues[r][c] && v !== this.engine.solution[r][c];
      el.classList.toggle('wrong', wrong);
    }

    refreshAll() {
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) this.refreshCell(r, c);
    }

    updateMistakes() {
      this.mistakesEl.textContent = `${this.mistakes}/${MISTAKES_LIMIT}`;
    }

    updateCounter() {
      let remaining = 0;
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) if (this.engine.board[r][c] === 0) remaining++;
      if (this.counterEl) this.counterEl.textContent = String(remaining);
    }

    newGame() {
      this.engine.generate(this.difficulty);
      this.selected = null;
      this.mistakes = 0;
      this.hintsLeft = 3;
      this.notesMode = false;
      this.paused = false;
      this.gameOver = false;
      this.history = [];
      this.notesBtn.classList.remove('is-active');
      this.pauseBtn.classList.remove('is-active');
      if (this.notesIndicator) this.notesIndicator.textContent = 'OFF';
      this.pauseOverlay.hidden = true;
      this.updateMistakes();
      this.hintsEl.textContent = '3';
      this.refreshAll();
      this.updateCounter();
      this.startTimer();
      this.modalEl.hidden = true;
    }

    startTimer() {
      this.stopTimer();
      this.elapsed = 0;
      this.startTime = Date.now();
      this.renderTimer();
      this.timerId = setInterval(() => this.renderTimer(), 1000);
    }

    resumeTimer() {
      this.stopTimer();
      this.startTime = Date.now();
      this.renderTimer();
      this.timerId = setInterval(() => this.renderTimer(), 1000);
    }

    stopTimer() {
      if (this.timerId) {
        this.elapsed += Date.now() - this.startTime;
        clearInterval(this.timerId);
      }
      this.timerId = null;
      this.startTime = null;
    }

    renderTimer() {
      const totalMs = this.elapsed + (this.startTime ? Date.now() - this.startTime : 0);
      const s = Math.floor(totalMs / 1000);
      const mm = String(Math.floor(s / 60)).padStart(2, '0');
      const ss = String(s % 60).padStart(2, '0');
      this.timerEl.textContent = `${mm}:${ss}`;
    }

    elapsedLabel() {
      return this.timerEl.textContent;
    }

    win() {
      this.gameOver = true;
      this.stopTimer();
      this.modalTitleEl.textContent = 'Solved!';
      this.modalMsgEl.textContent = 'Nice work.';
      this.modalTimeEl.textContent = this.elapsedLabel();
      this.modalEl.hidden = false;
    }

    loseGame() {
      this.gameOver = true;
      this.stopTimer();
      this.modalTitleEl.textContent = 'Game over';
      this.modalMsgEl.textContent = `You reached ${MISTAKES_LIMIT} mistakes.`;
      this.modalTimeEl.textContent = this.elapsedLabel();
      this.modalEl.hidden = false;
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const root = document.querySelector('[data-sudoku]');
    if (!root) return;
    new SudokuUI(root, new SudokuEngine());
  });
})();
