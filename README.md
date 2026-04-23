# Minimalist Games

Minimalist games platform — Sudoku, Minesweeper, 2048. Built with vanilla HTML5 + CSS3 + JavaScript. No frameworks, no build step.

## Stack

- HTML5, CSS3, vanilla JavaScript
- Hosting: Firebase Hosting
- Analytics: Google Analytics 4 (added in week 3)
- Monetization: Google AdSense (added in week 3)

## Status

**Week 1 — Foundation.** Project scaffolding complete. Design tokens seeded in `src/css/global.css`. Games not yet implemented (tasks 1.4–1.6).

## Run locally

```bash
npm run dev
# Firebase emulator serves on http://localhost:5000
```

## Deploy

```bash
firebase login            # once
npm run deploy            # requires .firebaserc with real project ID
```

## Setup checklist (one-time)

1. Create project at https://console.firebase.google.com → name `minimalist-games`.
2. Replace `REPLACE_WITH_FIREBASE_PROJECT_ID` in `.firebaserc` with the real project ID.
3. Project Settings → Your apps → Web → register app → copy config into `src/js/firebase-config.js`.

## Structure

See `PLAN.md` §1.1 in the sibling docs folder.
