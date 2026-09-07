# Publicação faseada dos posts — guião

O post 1 (**How Sudoku Puzzles Are Generated**) já está integrado em `src/blog/` — sai no próximo deploy.
Os posts 2 e 3 estão prontos nesta pasta `drafts/`, com data de publicação já escrita no HTML. O `firebase.json` já tem os redirects/rewrites dos três; só falta, em cada data, mover a pasta e acrescentar as entradas no blog index e no sitemap.

Em cada data, o mais simples é pedir ao Claude: *"publica o post minesweeper-openings"* — os passos abaixo são o equivalente manual.

---

## Post 2 — Minesweeper Openings · publicar a 11 de agosto de 2026

**1. Mover:**
```bash
cd /Users/alima/Documents/Claude/Projects/minimalist-games
mv drafts/minesweeper-openings src/blog/
```

**2. `src/blog/index.html`** — na secção **Minesweeper**, a seguir ao item `minesweeper-strategy`, inserir:
```html
      <li>
        <a class="post-link" href="/blog/minesweeper-openings">
          <h2>Minesweeper Openings: Where to Click First</h2>
          <p>Corners open more often, centers open bigger — where to put the first click, and how to squeeze the frontier the flood hands you.</p>
        </a>
      </li>
```

**3. `src/sitemap.xml`** — antes de `</urlset>`, inserir:
```xml
  <url>
    <loc>https://minimalist-games.com/blog/minesweeper-openings</loc>
    <lastmod>2026-08-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
```

**4.** `npm run deploy` → Search Console: Request indexing de `/blog/minesweeper-openings`.

---

## Post 3 — 2048: When to Break the Snake · publicar a 15 de agosto de 2026

**1. Mover:**
```bash
cd /Users/alima/Documents/Claude/Projects/minimalist-games
mv drafts/2048-breaking-the-snake src/blog/
```

**2. `src/blog/index.html`** — na secção **2048**, a seguir ao item `2048-endgame`, inserir:
```html
      <li>
        <a class="post-link" href="/blog/2048-breaking-the-snake">
          <h2>2048: When to Break the Snake</h2>
          <p>When the forbidden direction is free, how to survive a forced break, and how to dissolve a tile wedged in your anchor row.</p>
        </a>
      </li>
```

**3. `src/sitemap.xml`** — antes de `</urlset>`, inserir:
```xml
  <url>
    <loc>https://minimalist-games.com/blog/2048-breaking-the-snake</loc>
    <lastmod>2026-08-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
```

**4.** `npm run deploy` → Search Console: Request indexing de `/blog/2048-breaking-the-snake`.

---

## Depois do post 3

Resubmissão AdSense: janela **12–19 de agosto**, cumprindo a checklist do `AUDITORIA_ADSENSE_DELTA_2026-07-02.md` (crawl das páginas alteradas confirmado no Search Console com data posterior ao deploy → checkbox → Request review).
