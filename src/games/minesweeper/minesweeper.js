(function () {
  'use strict';

  const DIFFICULTIES = {
    beginner:     { rows: 9,  cols: 9,  mines: 10 },
    intermediate: { rows: 16, cols: 16, mines: 40 },
    expert:       { rows: 16, cols: 30, mines: 99 }
  };

  class MinesweeperEngine {
    constructor() {
      this.rows = 0; this.cols = 0; this.mineCount = 0;
      this.board = null;      // number of adjacent mines, or -1 for mine
      this.state = null;      // 'hidden' | 'revealed' | 'flagged'
      this.minesPlaced = false;
      this.revealedCount = 0;
      this.flagCount = 0;
      this.gameState = 'idle'; // 'idle' | 'playing' | 'won' | 'lost'
      this.exploded = null;
    }

    init(difficulty) {
      const { rows, cols, mines } = DIFFICULTIES[difficulty] ?? DIFFICULTIES.beginner;
      this.rows = rows; this.cols = cols; this.mineCount = mines;
      this.board = Array.from({ length: rows }, () => Array(cols).fill(0));
      this.state = Array.from({ length: rows }, () => Array(cols).fill('hidden'));
      this.minesPlaced = false;
      this.revealedCount = 0;
      this.flagCount = 0;
      this.gameState = 'idle';
      this.exploded = null;
    }

    placeMines(safeR, safeC) {
      const safe = new Set();
      for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
        safe.add(`${safeR + dr},${safeC + dc}`);
      }
      const positions = [];
      for (let r = 0; r < this.rows; r++) for (let c = 0; c < this.cols; c++) {
        if (!safe.has(`${r},${c}`)) positions.push([r, c]);
      }
      for (let i = positions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [positions[i], positions[j]] = [positions[j], positions[i]];
      }
      const pick = positions.slice(0, Math.min(this.mineCount, positions.length));
      for (const [r, c] of pick) this.board[r][c] = -1;

      for (let r = 0; r < this.rows; r++) {
        for (let c = 0; c < this.cols; c++) {
          if (this.board[r][c] === -1) continue;
          let n = 0;
          for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
            const nr = r + dr, nc = c + dc;
            if (nr < 0 || nc < 0 || nr >= this.rows || nc >= this.cols) continue;
            if (this.board[nr][nc] === -1) n++;
          }
          this.board[r][c] = n;
        }
      }
      this.minesPlaced = true;
    }

    reveal(r, c) {
      if (this.gameState === 'won' || this.gameState === 'lost') return { changes: [] };
      if (!this.minesPlaced) {
        this.placeMines(r, c);
        this.gameState = 'playing';
      }
      if (this.state[r][c] !== 'hidden') return { changes: [] };

      if (this.board[r][c] === -1) {
        this.state[r][c] = 'revealed';
        this.exploded = [r, c];
        this.gameState = 'lost';
        return { changes: [[r, c]], exploded: [r, c] };
      }

      const changes = [];
      const stack = [[r, c]];
      while (stack.length) {
        const [cr, cc] = stack.pop();
        if (this.state[cr][cc] !== 'hidden') continue;
        this.state[cr][cc] = 'revealed';
        this.revealedCount++;
        changes.push([cr, cc]);
        if (this.board[cr][cc] === 0) {
          for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
            const nr = cr + dr, nc = cc + dc;
            if (nr < 0 || nc < 0 || nr >= this.rows || nc >= this.cols) continue;
            if (this.state[nr][nc] === 'hidden' && this.board[nr][nc] !== -1) {
              stack.push([nr, nc]);
            }
          }
        }
      }

      if (this.revealedCount === this.rows * this.cols - this.mineCount) {
        this.gameState = 'won';
      }
      return { changes };
    }

    flag(r, c) {
      if (this.gameState === 'won' || this.gameState === 'lost') return false;
      if (this.state[r][c] === 'revealed') return false;
      if (this.state[r][c] === 'flagged') {
        this.state[r][c] = 'hidden';
        this.flagCount--;
      } else {
        this.state[r][c] = 'flagged';
        this.flagCount++;
      }
      return true;
    }

    allMines() {
      const out = [];
      for (let r = 0; r < this.rows; r++) for (let c = 0; c < this.cols; c++) {
        if (this.board[r][c] === -1) out.push([r, c]);
      }
      return out;
    }
  }

  class MinesweeperUI {
    constructor(root, engine) {
      this.root = root;
      this.engine = engine;
      this.difficulty = 'beginner';
      this.flagMode = false;
      this.paused = false;
      this.startTime = null;
      this.elapsed = 0;
      this.timerId = null;
      this.longPressTimer = null;

      this.gridEl = root.querySelector('[data-grid]');
      this.timerEl = root.querySelector('[data-timer]');
      this.minesCountEl = root.querySelector('[data-mines-left]');
      this.statusEl = root.querySelector('[data-status]');
      this.pauseOverlay = root.querySelector('[data-pause-overlay]');
      this.flagBtn = root.querySelector('[data-action="flag"]');
      this.pauseBtn = root.querySelector('[data-action="pause"]');
      this.modalEl = root.querySelector('[data-modal]');
      this.modalTitleEl = root.querySelector('[data-modal-title]');
      this.modalMsgEl = root.querySelector('[data-modal-msg]');
      this.modalTimeEl = root.querySelector('[data-modal-time]');

      this.bindControls();
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
      this.flagBtn.addEventListener('click', () => this.toggleFlagMode());
      this.pauseBtn.addEventListener('click', () => this.togglePause());
      this.root.querySelector('[data-modal-close]').addEventListener('click', () => {
        this.modalEl.hidden = true;
        this.newGame();
      });
    }

    renderGrid() {
      this.gridEl.innerHTML = '';
      this.gridEl.style.setProperty('--rows', String(this.engine.rows));
      this.gridEl.style.setProperty('--cols', String(this.engine.cols));
      for (let r = 0; r < this.engine.rows; r++) {
        for (let c = 0; c < this.engine.cols; c++) {
          const cell = document.createElement('button');
          cell.type = 'button';
          cell.className = 'ms-cell hidden';
          cell.dataset.row = String(r);
          cell.dataset.col = String(c);
          cell.addEventListener('click', (e) => this.handleClick(r, c, e));
          cell.addEventListener('contextmenu', (e) => { e.preventDefault(); this.handleFlag(r, c); });
          cell.addEventListener('touchstart', (e) => this.startLongPress(r, c, e), { passive: true });
          cell.addEventListener('touchend', () => this.cancelLongPress());
          cell.addEventListener('touchmove', () => this.cancelLongPress());
          cell.addEventListener('touchcancel', () => this.cancelLongPress());
          this.gridEl.appendChild(cell);
        }
      }
    }

    startLongPress(r, c, e) {
      this.cancelLongPress();
      this.longPressTimer = setTimeout(() => {
        this.handleFlag(r, c);
        this.longPressTimer = 'fired';
      }, 500);
    }

    cancelLongPress() {
      if (this.longPressTimer && this.longPressTimer !== 'fired') {
        clearTimeout(this.longPressTimer);
      }
      setTimeout(() => { this.longPressTimer = null; }, 0);
    }

    handleClick(r, c, e) {
      if (this.paused || this.engine.gameState === 'won' || this.engine.gameState === 'lost') return;
      // Swallow click that followed a long-press flag
      if (this.longPressTimer === 'fired') return;
      if (this.flagMode) { this.handleFlag(r, c); return; }
      if (this.engine.state[r][c] === 'flagged') return;
      const result = this.engine.reveal(r, c);
      if (this.engine.gameState === 'playing' && !this.timerId) this.startTimer();
      this.applyChanges(result.changes);
      if (result.exploded) this.loseGame(result.exploded);
      else if (this.engine.gameState === 'won') this.winGame();
    }

    handleFlag(r, c) {
      if (this.paused || this.engine.gameState === 'won' || this.engine.gameState === 'lost') return;
      if (this.engine.flag(r, c)) {
        this.refreshCell(r, c);
        this.updateMinesLeft();
        if (!this.timerId && this.engine.minesPlaced) this.startTimer();
      }
    }

    applyChanges(changes) {
      for (const [r, c] of changes) this.refreshCell(r, c);
    }

    refreshCell(r, c) {
      const el = this.gridEl.querySelector(`.ms-cell[data-row="${r}"][data-col="${c}"]`);
      const state = this.engine.state[r][c];
      const val = this.engine.board[r][c];
      el.className = 'ms-cell';
      el.textContent = '';
      if (state === 'flagged') {
        el.classList.add('flagged');
        el.innerHTML = '<svg viewBox="0 0 24 24" width="60%" height="60%" fill="currentColor" aria-hidden="true"><path d="M5 3v18h2v-7h10l-2-4 2-4H7V3H5z"/></svg>';
      } else if (state === 'revealed') {
        el.classList.add('revealed');
        if (val === -1) {
          el.classList.add('mine');
          if (this.engine.exploded && this.engine.exploded[0] === r && this.engine.exploded[1] === c) {
            el.classList.add('exploded');
          }
          el.innerHTML = '<svg viewBox="0 0 24 24" width="60%" height="60%" fill="currentColor" aria-hidden="true"><circle cx="12" cy="12" r="6"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1" stroke="currentColor" stroke-width="2" fill="none"/></svg>';
        } else if (val > 0) {
          el.textContent = String(val);
          el.classList.add('n' + val);
        }
      } else {
        el.classList.add('hidden');
      }
    }

    updateMinesLeft() {
      this.minesCountEl.textContent = String(this.engine.mineCount - this.engine.flagCount);
    }

    toggleFlagMode() {
      this.flagMode = !this.flagMode;
      this.flagBtn.classList.toggle('is-active', this.flagMode);
    }

    togglePause() {
      if (this.engine.gameState === 'won' || this.engine.gameState === 'lost') return;
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

    newGame() {
      this.engine.init(this.difficulty);
      this.flagMode = false;
      this.paused = false;
      this.flagBtn.classList.remove('is-active');
      this.pauseBtn.classList.remove('is-active');
      this.pauseOverlay.hidden = true;
      this.modalEl.hidden = true;
      this.stopTimer();
      this.elapsed = 0;
      this.startTime = null;
      this.renderTimer();
      this.renderGrid();
      this.updateMinesLeft();
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

    revealAllMines() {
      for (const [r, c] of this.engine.allMines()) {
        if (this.engine.state[r][c] !== 'revealed' && this.engine.state[r][c] !== 'flagged') {
          this.engine.state[r][c] = 'revealed';
          this.refreshCell(r, c);
        }
      }
    }

    loseGame(exploded) {
      this.stopTimer();
      this.revealAllMines();
      this.modalTitleEl.textContent = 'Boom!';
      this.modalMsgEl.textContent = 'You hit a mine.';
      this.modalTimeEl.textContent = this.timerEl.textContent;
      this.modalEl.hidden = false;
    }

    winGame() {
      this.stopTimer();
      this.modalTitleEl.textContent = 'Cleared!';
      this.modalMsgEl.textContent = 'All safe cells revealed.';
      this.modalTimeEl.textContent = this.timerEl.textContent;
      this.modalEl.hidden = false;
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const root = document.querySelector('[data-minesweeper]');
    if (!root) return;
    new MinesweeperUI(root, new MinesweeperEngine());
  });
})();
