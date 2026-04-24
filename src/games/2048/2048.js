(function () {
  'use strict';

  const SIZE = 4;
  const STORAGE_BEST = 'minimalist-games.2048.best';

  class Game2048 {
    constructor() {
      this.size = SIZE;
      this.tiles = null;
      this.score = 0;
      this.gameOver = false;
      this.won = false;
    }

    init() {
      this.tiles = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
      this.score = 0;
      this.gameOver = false;
      this.won = false;
      this.spawn();
      this.spawn();
    }

    spawn() {
      const empties = [];
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) {
        if (this.tiles[r][c] === 0) empties.push([r, c]);
      }
      if (empties.length === 0) return null;
      const [r, c] = empties[Math.floor(Math.random() * empties.length)];
      this.tiles[r][c] = Math.random() < 0.9 ? 2 : 4;
      return [r, c];
    }

    // Compress+merge a single row to the left. Returns new row + gained score.
    static slideRow(row) {
      const filtered = row.filter(v => v !== 0);
      let gained = 0;
      for (let i = 0; i < filtered.length - 1; i++) {
        if (filtered[i] === filtered[i + 1]) {
          filtered[i] *= 2;
          gained += filtered[i];
          filtered[i + 1] = 0;
          i++; // skip the merged partner
        }
      }
      const result = filtered.filter(v => v !== 0);
      while (result.length < SIZE) result.push(0);
      return { row: result, gained };
    }

    move(direction) {
      const before = JSON.stringify(this.tiles);
      let gained = 0;

      if (direction === 'left') {
        for (let r = 0; r < SIZE; r++) {
          const { row, gained: g } = Game2048.slideRow(this.tiles[r]);
          this.tiles[r] = row;
          gained += g;
        }
      } else if (direction === 'right') {
        for (let r = 0; r < SIZE; r++) {
          const { row, gained: g } = Game2048.slideRow(this.tiles[r].slice().reverse());
          this.tiles[r] = row.reverse();
          gained += g;
        }
      } else if (direction === 'up') {
        for (let c = 0; c < SIZE; c++) {
          const col = this.tiles.map(row => row[c]);
          const { row, gained: g } = Game2048.slideRow(col);
          for (let r = 0; r < SIZE; r++) this.tiles[r][c] = row[r];
          gained += g;
        }
      } else if (direction === 'down') {
        for (let c = 0; c < SIZE; c++) {
          const col = this.tiles.map(row => row[c]).reverse();
          const { row, gained: g } = Game2048.slideRow(col);
          const back = row.reverse();
          for (let r = 0; r < SIZE; r++) this.tiles[r][c] = back[r];
          gained += g;
        }
      }

      const moved = JSON.stringify(this.tiles) !== before;
      if (moved) {
        this.score += gained;
        this.spawn();
        if (!this.won) {
          for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) {
            if (this.tiles[r][c] >= 2048) { this.won = true; break; }
          }
        }
        if (!this.canMove()) this.gameOver = true;
      }
      return { moved, gained };
    }

    canMove() {
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) {
        if (this.tiles[r][c] === 0) return true;
        const v = this.tiles[r][c];
        if (r + 1 < SIZE && this.tiles[r + 1][c] === v) return true;
        if (c + 1 < SIZE && this.tiles[r][c + 1] === v) return true;
      }
      return false;
    }

    snapshot() {
      return { tiles: this.tiles.map(r => r.slice()), score: this.score, gameOver: this.gameOver, won: this.won };
    }

    restore(s) {
      this.tiles = s.tiles.map(r => r.slice());
      this.score = s.score;
      this.gameOver = s.gameOver;
      this.won = s.won;
    }
  }

  class UI {
    constructor(root, engine) {
      this.root = root;
      this.engine = engine;
      this.history = [];
      this.best = Number(localStorage.getItem(STORAGE_BEST) || 0);

      this.boardEl = root.querySelector('[data-board]');
      this.scoreEl = root.querySelector('[data-score]');
      this.bestEl = root.querySelector('[data-best]');
      this.modalEl = root.querySelector('[data-modal]');
      this.modalTitleEl = root.querySelector('[data-modal-title]');
      this.modalMsgEl = root.querySelector('[data-modal-msg]');
      this.modalScoreEl = root.querySelector('[data-modal-score]');

      this.bindControls();
      this.bindKeyboard();
      this.bindSwipe();
      this.renderBackground();
      this.newGame();
    }

    bindControls() {
      this.root.querySelector('[data-action="new"]').addEventListener('click', () => this.newGame());
      this.root.querySelector('[data-action="undo"]').addEventListener('click', () => this.undo());
      this.root.querySelectorAll('[data-dir]').forEach(btn => {
        btn.addEventListener('click', () => this.tryMove(btn.dataset.dir));
      });
      this.root.querySelector('[data-modal-close]').addEventListener('click', () => {
        this.modalEl.hidden = true;
        this.newGame();
      });
      this.root.querySelector('[data-modal-continue]').addEventListener('click', () => {
        this.modalEl.hidden = true;
      });
    }

    bindKeyboard() {
      document.addEventListener('keydown', (e) => {
        const map = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down',
                      a: 'left', d: 'right', w: 'up', s: 'down',
                      A: 'left', D: 'right', W: 'up', S: 'down' };
        if (map[e.key]) { this.tryMove(map[e.key]); e.preventDefault(); return; }
        if ((e.key === 'z' || e.key === 'Z') && (e.metaKey || e.ctrlKey)) { this.undo(); e.preventDefault(); }
      });
    }

    bindSwipe() {
      let sx = 0, sy = 0, tracking = false;
      this.boardEl.addEventListener('touchstart', (e) => {
        if (e.touches.length !== 1) return;
        sx = e.touches[0].clientX; sy = e.touches[0].clientY; tracking = true;
      }, { passive: true });
      this.boardEl.addEventListener('touchend', (e) => {
        if (!tracking) return;
        tracking = false;
        const t = e.changedTouches[0];
        const dx = t.clientX - sx, dy = t.clientY - sy;
        const absX = Math.abs(dx), absY = Math.abs(dy);
        const THRESHOLD = 24;
        if (Math.max(absX, absY) < THRESHOLD) return;
        if (absX > absY) this.tryMove(dx > 0 ? 'right' : 'left');
        else this.tryMove(dy > 0 ? 'down' : 'up');
      });
    }

    renderBackground() {
      // 16 empty cells behind the real tiles
      const bg = this.root.querySelector('[data-board-bg]');
      bg.innerHTML = '';
      for (let i = 0; i < SIZE * SIZE; i++) {
        const cell = document.createElement('div');
        cell.className = 'bg-cell';
        bg.appendChild(cell);
      }
    }

    renderTiles() {
      this.boardEl.innerHTML = '';
      for (let r = 0; r < SIZE; r++) for (let c = 0; c < SIZE; c++) {
        const v = this.engine.tiles[r][c];
        if (v === 0) continue;
        const tile = document.createElement('div');
        tile.className = `tile t-${v <= 2048 ? v : 'super'}`;
        tile.textContent = String(v);
        tile.style.setProperty('--r', String(r));
        tile.style.setProperty('--c', String(c));
        this.boardEl.appendChild(tile);
      }
    }

    tryMove(dir) {
      if (this.engine.gameOver) return;
      const snap = this.engine.snapshot();
      const { moved } = this.engine.move(dir);
      if (moved) {
        this.history.push(snap);
        if (this.history.length > 20) this.history.shift();
        this.renderTiles();
        this.updateScore();
        if (this.engine.won && !this.wonShown) {
          this.wonShown = true;
          this.showModal('You made 2048!', 'Keep going for a higher score.', false);
        } else if (this.engine.gameOver) {
          this.showModal('Game over', 'No moves left.', true);
        }
      }
    }

    updateScore() {
      this.scoreEl.textContent = String(this.engine.score);
      if (this.engine.score > this.best) {
        this.best = this.engine.score;
        localStorage.setItem(STORAGE_BEST, String(this.best));
      }
      this.bestEl.textContent = String(this.best);
    }

    undo() {
      const s = this.history.pop();
      if (!s) return;
      this.engine.restore(s);
      this.renderTiles();
      this.updateScore();
    }

    newGame() {
      this.engine.init();
      this.history = [];
      this.wonShown = false;
      this.modalEl.hidden = true;
      this.renderTiles();
      this.updateScore();
    }

    showModal(title, msg, gameOver) {
      this.modalTitleEl.textContent = title;
      this.modalMsgEl.textContent = msg;
      this.modalScoreEl.textContent = String(this.engine.score);
      this.root.querySelector('[data-modal-continue]').hidden = gameOver;
      this.root.querySelector('[data-modal-close]').textContent = gameOver ? 'New Game' : 'New Game';
      this.modalEl.hidden = false;
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const root = document.querySelector('[data-2048]');
    if (!root) return;
    new UI(root, new Game2048());
  });
})();
