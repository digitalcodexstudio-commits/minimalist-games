# Minimalist Games

Minimalist games platform — Sudoku, Minesweeper, 2048. Built with vanilla HTML5 + CSS3 + JavaScript. No frameworks, no build step.

Live at https://minimalist-games.com

## Stack

- HTML5, CSS3, vanilla JavaScript
- Hosting: Firebase Hosting
- Analytics: Google Analytics 4
- Monetization: Google AdSense (placeholders pending approval)

## Status

Week 1 foundation complete. Three games playable, custom domain live, analytics wired, full SEO metadata. AdSense approval pending.

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
