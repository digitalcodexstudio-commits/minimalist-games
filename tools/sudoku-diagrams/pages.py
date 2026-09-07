# -*- coding: utf-8 -*-
"""Assemble the 9 Sudoku-strategy HTML pages from verified diagrams + prose."""
import os, build

import os
SITE = os.path.join(os.path.dirname(__file__), "..", "..", "src", "blog")
BASE = "https://minimalist-games.com"
DATE_ISO = "2026-06-03"
DATE_HUMAN = "June 3, 2026"
DATE_MODIFIED = "2026-08-30"

BRAND_SUFFIX = " — Minimalist Games"
TITLE_MAX = 60


def doc_title(title):
    """Google truncates SERP titles near 60 chars — the brand suffix is what gets cut."""
    full = title + BRAND_SUFFIX
    return full if len(full) <= TITLE_MAX else title

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#4a5fc1">
  <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>
  <link rel="preconnect" href="https://www.googletagmanager.com">
  <link rel="dns-prefetch" href="https://www.google-analytics.com">
  <link rel="dns-prefetch" href="https://googleads.g.doubleclick.net">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1735197115961712" crossorigin="anonymous"></script>
  <link rel="canonical" href="{base}/blog/{slug}">
  <title>{doc_title}</title>
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Minimalist Games">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{base}/blog/{slug}">
  <meta property="og:image" content="{base}/public/og-image.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/public/favicon.svg">
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="apple-touch-icon" href="/public/icon-192.svg">
  <link rel="stylesheet" href="/src/css/global.css">
  <link rel="stylesheet" href="/src/css/blog.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{og_title}",
    "description": "{og_desc}",
    "author": {{ "@type": "Person", "name": "Arnaldo Lima", "url": "https://minimalist-games.com/about#author" }},
    "publisher": {{ "@type": "Organization", "name": "Minimalist Games" }},
    "datePublished": "{date_iso}",
    "dateModified": "{date_modified}",
    "mainEntityOfPage": "{base}/blog/{slug}",
    "image": "{base}/public/og-image.svg"
  }}
  </script>
  <script src="/src/js/analytics.js" defer></script>
  <script src="/src/js/sw-register.js" defer></script>
</head>
<body class="blog">
  <main class="blog-page">
    <header class="blog-header">
      <a href="/blog" class="back-btn" aria-label="Back to blog">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
      </a>
      <span class="blog-nav-label">Blog</span>
    </header>

    <article class="post">
      <p class="post-meta">{date_human} · {read} min read · By <a href="/about#author" rel="author">Arnaldo Lima</a></p>
      <h1 class="post-title">{h1}</h1>
{body}
      <a class="cta" href="/games/sudoku">Play Sudoku Zen — six difficulties</a>

      <section class="related">
        <h3>Related</h3>
        <ul>
{related}
        </ul>
      </section>
    </article>

    <footer class="blog-footer">
      <a href="/">Home</a>
      <span aria-hidden="true">·</span>
      <a href="/blog">Blog</a>
      <span aria-hidden="true">·</span>
      <a href="/privacy">Privacy</a>
      <span aria-hidden="true">·</span>
      <a href="/terms">Terms</a>
    </footer>
  </main>
</body>
</html>
"""

def page(slug, title, h1, desc, og_title, og_desc, read, body, related):
    rel = "\n".join(
        f'          <li><a href="{u}">{t}</a></li>' for t, u in related)
    return HEAD.format(base=BASE, slug=slug, doc_title=doc_title(title), h1=h1, desc=desc,
                       og_title=og_title, og_desc=og_desc, read=read,
                       date_iso=DATE_ISO, date_human=DATE_HUMAN,
                       date_modified=DATE_MODIFIED,
                       body=body, related=rel)

LEGEND_PATTERN = build.legend([
    ("#edf0fb", "the unit in focus"),
    ("#c97f00", "the pattern"),
    ("#1f9d57", "a placement"),
    ("#d6453d", "an elimination"),
])

# ============================================================ PAGE BODIES
def body_pillar():
    cards = [
        ("Beginner", "Last Remaining Cell", "sudoku-last-remaining-cell",
         "The single missing digit in an almost-full row, column, or box."),
        ("Beginner", "Hidden Singles", "sudoku-hidden-singles",
         "A digit with only one legal home in a unit — even when the cell looks busy."),
        ("Beginner", "Cross-Hatching", "sudoku-cross-hatching",
         "Scan rows and columns to place a digit inside a box."),
        ("Intermediate", "Naked Pairs", "sudoku-naked-pairs",
         "Two cells sharing the same two candidates lock those digits in."),
        ("Intermediate", "Hidden Pairs", "sudoku-hidden-pairs",
         "Two digits confined to two cells clear everything else out of them."),
        ("Intermediate", "Naked Triples", "sudoku-naked-triples",
         "Three cells, three candidates — and the quads that follow."),
        ("Intermediate", "Pointing Pairs", "sudoku-pointing-pairs",
         "A digit trapped on one line of a box points down that line."),
        ("Intermediate", "Box/Line Reduction", "sudoku-box-line-reduction",
         "The reverse: a line confines a digit to a single box."),
    ]
    grid = "\n".join(
        f'        <li><a href="/blog/{s}"><span class="level-tag">{lv}</span>'
        f'<h3>{t}</h3><p>{d}</p></a></li>'
        for lv, t, s, d in cards)
    return f"""      <p class="lede">Most people learn Sudoku by scanning for obvious numbers, then hit a wall on harder boards and assume they need to guess. They don't. Every standard Sudoku is solvable by pure logic — you just need a bigger toolbox. This guide walks through the eight techniques that carry you from beginner to confident solver, each one explained with a worked diagram you can read at a glance.</p>

      <p>The strategies build on each other. The first three place digits directly and need no notes. The next five work on <strong>pencil marks</strong> — the small candidate numbers you jot into empty cells — and clear those candidates away until placements appear. Learn them in order and each new technique will feel like a natural extension of the last.</p>

      <p>If you want a board to practise on while you read, open <a href="/games/sudoku">Sudoku Zen</a> in another tab. Its notes mode lets you pencil-mark candidates exactly as the diagrams below show. Brand new to the game? Start with <a href="/blog/how-to-solve-sudoku">how to solve Sudoku for beginners</a> first, then come back here.</p>

      <h2>The eight techniques</h2>
      <ul class="strategy-grid">
{grid}
      </ul>

      <h2>How the techniques fit together</h2>
      <p>Beginner techniques — last remaining cell, hidden singles, and cross-hatching — are about <em>placing</em> digits. They finish easy boards on their own and get you most of the way through a medium one. None of them require notes; you do them by looking.</p>

      <p>Intermediate techniques are about <em>eliminating</em> candidates so that a placement becomes possible. Naked and hidden pairs, naked triples, pointing pairs, and box/line reduction never put a number on the board by themselves. Instead they shave possibilities off other cells until a hidden single or last remaining cell appears. That two-step rhythm — eliminate, then place — is the whole game at the intermediate level.</p>

      <p>Once these are reflexive, the advanced patterns (X-Wing, Swordfish, XY-Wing) are just the same idea stretched across several rows and columns at once. We'll cover those in a follow-up guide. For now, master the eight below and you'll solve the vast majority of "hard"-rated puzzles without ever guessing.</p>

      <h2>A note on guessing</h2>
      <p>You may have seen "guess and check" listed as a Sudoku method. It works, but it isn't solving — it's brute force, and on a contaminated board it's hard to undo. Every technique in this guide is deductive: each move is forced by the rules, so you can always explain <em>why</em> a digit goes where it does. That's the difference between finishing a puzzle and actually getting better at them.</p>"""

def body_last_remaining():
    return f"""      <p class="lede">The last remaining cell — sometimes called a "full house" — is the simplest move in Sudoku. When a row, column, or 3×3 box already contains eight of its nine digits, the empty cell can only be the one that's missing. It's the first technique every solver learns, and it's worth doing deliberately rather than by accident.</p>

      <p>Sudoku's one rule is that every row, every column, and every 3×3 box must contain the digits 1 through 9 exactly once. The last remaining cell is that rule at its most direct: count what's there, name what's missing, write it in.</p>

      <h2>How it works</h2>
      {build.dia_last_remaining()}
      {LEGEND_PATTERN}
      <p>In the row above, eight cells are already filled. Reading along, the digits present are 5, 3, 4, 6, 7, 8, 9, and 1 — every digit except 2. Since the row must contain a 2 somewhere and there is only one empty cell left, the 2 goes there. No candidates, no notes, no doubt.</p>

      <p>The same logic applies to columns and boxes. Whenever a unit is down to its last empty cell, you can fill it instantly. These moments cascade: filling one last cell often completes a neighbouring unit, which completes another, and a corner of the board falls in seconds.</p>

      <h2>Where to look for them</h2>
      <p>Last remaining cells appear most often near the end of a solve, but they also show up early in any unit that started with lots of clues. Scan the board for the rows, columns, and boxes that look most crowded — the ones with seven or eight digits already placed. Those are where a single missing number is easiest to spot.</p>

      <p>A practical habit: every time you place a digit anywhere, glance at the three units that cell belongs to (its row, its column, its box). If placing your digit left any of them with exactly one empty cell, fill that cell immediately before moving on. This keeps the cascade going and stops you from re-scanning the same regions.</p>

      <h2>Last remaining cell vs. naked single</h2>
      <p>These two sound alike but come from opposite directions. A <strong>last remaining cell</strong> looks at a whole unit and asks "which digit is missing?" A <a href="/blog/how-to-solve-sudoku">naked single</a> looks at one cell and asks "which digits are still allowed here?" — checking its row, column, and box together. Both leave exactly one answer, but they're found by scanning differently. The last remaining cell is usually the faster of the two to spot because you only have to read one line.</p>

      <h2>Why it matters</h2>
      <p>It's tempting to dismiss the last remaining cell as too obvious to name. But solvers who treat it as a deliberate step — actively hunting for almost-full units — finish easy and medium boards far faster than those who only notice these cells by luck. It costs nothing and it's the foundation every harder technique is built on.</p>

      <p>Ready for the next step up? <a href="/blog/sudoku-hidden-singles">Hidden singles</a> find a forced digit even when the cell still has several candidates — the technique that unlocks most medium boards.</p>"""

def body_hidden_singles():
    return f"""      <p class="lede">A hidden single is a digit that can legally go in only one cell of a row, column, or box — even though that cell looks like it has several options. It's the most useful beginner technique after basic scanning, and it's the one that quietly solves most of a medium Sudoku. Learning to see hidden singles is the moment Sudoku starts to click.</p>

      <p>The word "hidden" is the key. With a last remaining cell or a naked single, the cell itself obviously has one answer. A hidden single is disguised: the cell carries two or three candidates, so nothing about it stands out. The single only appears when you look at the whole unit and notice that one particular digit has nowhere else to go.</p>

      <h2>A worked example</h2>
      {build.dia_hidden_single()}
      {LEGEND_PATTERN}
      <p>Look only at the top-right box. Three cells are empty, with candidates {{4, 6}}, {{4, 5}}, and {{4, 6}}. If you judged the middle cell on its own, you couldn't decide between 4 and 5. But scan the box for the digit 5 specifically: it appears in just one of the three cells. The box must contain a 5 somewhere, and there is only one cell that accepts it — so 5 is placed, even though that cell also listed a 4.</p>

      <p>That's the whole technique. Instead of asking "what can go in this cell?", you ask "where in this unit can this digit go?" When the answer is "only here," you have a hidden single.</p>

      <h2>How to hunt for them</h2>
      <p>Work one digit at a time within one unit. Pick a box, then run through the digits it's still missing. For each missing digit, count how many of the box's empty cells could legally hold it — remembering that a digit is blocked if it already appears in that cell's row or column. If exactly one cell survives, place the digit.</p>

      <p>Boxes are the easiest place to start because the 3×3 shape makes the elimination visual, but hidden singles live in rows and columns too. After you've swept the boxes, run the same check along any row or column that still has several gaps.</p>

      <h2>Why they're easy to miss</h2>
      <p>Beginners overlook hidden singles because they scan cell by cell, and a hidden single's cell never looks special — it has the same two or three candidates as its neighbours. The fix is to switch your unit of attention from the cell to the digit. Once you train yourself to ask "where can the 5 go in this box?" the hidden singles light up.</p>

      <p>This is also why pencil marks help. With every cell's candidates written in, a hidden single is visible the moment you notice a digit that appears only once across a unit. On <a href="/games/sudoku">Sudoku Zen</a>, turn on notes mode and the pattern becomes much easier to spot.</p>

      <h2>Next steps</h2>
      <p>Hidden singles pair naturally with <a href="/blog/sudoku-cross-hatching">cross-hatching</a>, which is the visual scanning method for finding them inside a box. Once both feel automatic, move on to <a href="/blog/sudoku-naked-pairs">naked pairs</a> — the first true candidate-elimination technique.</p>"""

def body_cross_hatching():
    return f"""      <p class="lede">Cross-hatching — also called slicing and dicing — is the scanning method that places a digit inside a 3×3 box by reading the rows and columns that pass through it. It's how experienced solvers fill in numbers quickly without writing a single pencil mark, and it's the most efficient way to find hidden singles in a box.</p>

      <p>The idea is simple. A box needs each digit exactly once. If the rows and columns crossing that box already contain a particular digit, they block most of the box's cells. Often they block all but one — and that surviving cell is where the digit must go.</p>

      <h2>Slicing and dicing in action</h2>
      {build.dia_cross_hatch()}
      {LEGEND_PATTERN}
      <p>We want to place a 1 in the bottom-left box. Look at the rows passing through it: the top two rows of the box already contain a 1 elsewhere on the board (the amber lines), so a 1 can't go in either of those rows inside the box. That leaves only the bottom row. Now look at the columns: the left and right columns of the box already have a 1, leaving only the middle column. The one cell that sits on both the open row and the open column is forced — the 1 goes there.</p>

      <p>"Slicing" refers to the horizontal scan across rows; "dicing" is the vertical scan down columns. Doing both narrows a box from nine cells to one without any notes.</p>

      <h2>How to do it efficiently</h2>
      <p>Pick a digit that already appears several times on the board — a digit with five or six placements gives you the most blocking lines to work with. Then check each box that's still missing it. For every such box, mentally extend the rows and columns that already contain the digit; if they cut the box down to a single open cell, place it.</p>

      <p>Cycle through the digits this way, 1 to 9, and you'll place a surprising number of cells. When a digit stops yielding placements, move to the next. This systematic sweep is the engine of fast solving on easy and medium boards.</p>

      <h2>Cross-hatching vs. hidden singles</h2>
      <p>These are two views of the same logic. <a href="/blog/sudoku-hidden-singles">Hidden singles</a> describe the result — a digit with only one legal cell in a unit. Cross-hatching is the technique you use to find that result inside a box, by scanning the crossing lines. If you prefer working from pencil marks, you'll spot the hidden single in the notes; if you prefer scanning a clean board, you'll cross-hatch your way to the same cell.</p>

      <h2>When it runs out</h2>
      <p>Cross-hatching solves easy boards almost entirely and gets you deep into medium ones. When no box can be sliced down to a single cell, it's time to start pencil-marking and move to candidate-elimination techniques like <a href="/blog/sudoku-naked-pairs">naked pairs</a> and <a href="/blog/sudoku-pointing-pairs">pointing pairs</a>. Those don't place digits directly — they remove candidates until cross-hatching works again.</p>"""

def body_naked_pairs():
    return f"""      <p class="lede">A naked pair is two cells in the same row, column, or box that contain exactly the same two candidates — and nothing else. Because those two digits must occupy those two cells between them, they can be eliminated from every other cell in the unit. It's the first real candidate-elimination technique, and the gateway to solving hard puzzles.</p>

      <p>Naked pairs need pencil marks. Once you've filled in candidates and scanning has stalled, this is one of the first patterns to look for. It rarely places a digit by itself, but the candidates it clears away almost always expose a hidden single somewhere nearby.</p>

      <h2>How a naked pair works</h2>
      {build.dia_naked_pair()}
      {LEGEND_PATTERN}
      <p>In this box, two cells both hold exactly {{3, 7}} (amber). We don't know yet which is the 3 and which is the 7 — but we know that between them they will use up both digits. That means no other cell in the box can be a 3 or a 7. So those candidates are struck from every other cell in the box (red). In the cell that had {{3, 4}}, the 3 disappears and it becomes a plain 4 — a placement, handed to you for free.</p>

      <p>The pair doesn't have to be solved to be useful. Its power comes entirely from the fact that two cells are reserved for two digits, locking those digits out of the rest of the unit.</p>

      <h2>What counts as a naked pair</h2>
      <p>Three conditions must all hold. The two cells must share the same unit — a row, a column, or a box. They must contain exactly two candidates each, no more. And those two candidates must be identical in both cells. {{3, 7}} and {{3, 7}} qualify; {{3, 7}} and {{3, 8}} do not, and neither does {{3, 7}} paired with {{3, 7, 9}}.</p>

      <p>If the two cells happen to share more than one unit — say they're in the same row <em>and</em> the same box — then you can eliminate the pair's digits from both units at once. Those overlap cases are where naked pairs cascade fastest.</p>

      <h2>Finding them at the table</h2>
      <p>Scan for cells that have exactly two pencil marks — bivalue cells. Whenever you find one, glance along its row, down its column, and around its box for a twin with the identical pair. Pairs are easiest to catch right after you finish pencil-marking, while the candidate counts are fresh in your mind.</p>

      <p>A naked pair is the mirror image of a <a href="/blog/sudoku-hidden-pairs">hidden pair</a>. The naked version is obvious in the cells but you act on the <em>rest</em> of the unit; the hidden version is disguised among other candidates but you act on the <em>pair cells</em> themselves. Learn both together — they often appear in the same puzzle.</p>

      <h2>Next steps</h2>
      <p>Once naked pairs feel natural, the extension to <a href="/blog/sudoku-naked-triples">naked triples</a> is straightforward: three cells, three shared candidates, same elimination logic. And the <a href="/blog/sudoku-hidden-pairs">hidden pair</a> teaches you to spot the pattern even when it's buried.</p>"""

def body_hidden_pairs():
    return f"""      <p class="lede">A hidden pair is two digits that can only appear in the same two cells of a unit — even though those cells also carry other candidates. When you find one, every <em>other</em> candidate can be wiped from those two cells, leaving just the pair. It's the trickiest of the pair techniques to spot, and one of the most satisfying.</p>

      <p>Where a <a href="/blog/sudoku-naked-pairs">naked pair</a> announces itself (two cells, two candidates, identical), a hidden pair is camouflaged. The two cells might show three, four, or five candidates each. The pair is "hidden" inside that clutter, and you only find it by tracking where two specific digits are allowed to go.</p>

      <h2>A worked example</h2>
      {build.dia_hidden_pair()}
      {LEGEND_PATTERN}
      <p>Scan this column for the digits 1 and 3. Both of them can only go in the same two cells (amber) — nowhere else in the column accepts a 1 or a 3. That's the hidden pair. Now reason it through: those two cells must hold the 1 and the 3 between them, so they can't hold anything else. Every other candidate in them — here an 8 in each — is removed (red). The two cells collapse to a clean {{1, 3}}, which is now a naked pair as well.</p>

      <p>Notice the direction of the elimination. A naked pair clears candidates from the <em>rest</em> of the unit. A hidden pair clears candidates from the <em>pair cells themselves</em>. Same family of logic, opposite target.</p>

      <h2>How to find a hidden pair</h2>
      <p>Go through a unit two digits at a time, or watch for digits that are scarce. For each pair of digits, count the cells in the unit where each one can go. If two different digits are both restricted to the same two cells, you've found a hidden pair — regardless of what other candidates those cells contain.</p>

      <p>In practice the shortcut is to look for digits that appear as candidates only twice in a unit. If two such digits share the same two cells, the pattern is there. It takes more searching than a naked pair, which is exactly why beginners miss it.</p>

      <h2>Why it's worth the effort</h2>
      <p>Hidden pairs often appear on hard boards precisely where no other move is available. Because the elimination cleans up the pair cells, it frequently turns one of them into a bivalue cell that feeds a naked pair, an <a href="/blog/sudoku-pointing-pairs">pointing pair</a>, or a chain elsewhere. One hidden pair can unstick an entire region.</p>

      <p>The same idea scales: a <a href="/blog/sudoku-naked-triples">hidden triple</a> is three digits confined to three cells. It's rarer and harder to see, but the logic is identical — find the digits that have nowhere else to go.</p>"""

def body_naked_triples():
    return f"""      <p class="lede">A naked triple is three cells in a unit that, between them, use only three candidate digits. As with naked pairs, those three digits are reserved for those three cells, so they can be eliminated everywhere else in the unit. Quads extend the same idea to four cells and four digits. These techniques clear candidates in bulk and often crack a stalled hard board.</p>

      <p>The subtlety that trips people up: each of the three cells does <em>not</em> need to contain all three digits. They only need to draw from the same pool of three. {{2, 5}}, {{5, 8}}, and {{2, 8}} form a perfectly valid naked triple even though no single cell shows all of 2, 5, and 8.</p>

      <h2>How a naked triple works</h2>
      {build.dia_naked_triple()}
      {LEGEND_PATTERN}
      <p>Three cells in this column (amber) hold candidates drawn entirely from {{2, 5, 8}}. Whatever the exact arrangement, those three cells will consume the 2, the 5, and the 8 among themselves. So none of those digits can live anywhere else in the column, and they're struck from every other cell (red). One elimination like this can remove several candidates at once and immediately expose a placement.</p>

      <h2>Recognising the pattern</h2>
      <p>You're looking for any three cells in a unit whose combined candidates total exactly three distinct digits. The valid shapes are:</p>
      <ul>
        <li>Three cells each with the same three candidates: {{2,5,8}}, {{2,5,8}}, {{2,5,8}}.</li>
        <li>A mix of pairs and triples that overlap into three digits: {{2,5}}, {{5,8}}, {{2,8}} or {{2,5,8}}, {{2,5}}, {{5,8}}.</li>
      </ul>
      <p>If the three cells together use a fourth digit, it isn't a triple. Counting the union of candidates is the reliable test: three cells, three digits total.</p>

      <h2>Naked quads</h2>
      <p>A naked quad is the same logic with four cells and four shared candidates. It's genuinely rare in everyday puzzles and tedious to scan for, so most solvers only reach for it on the hardest grids when nothing simpler is available. If you've mastered triples, you already understand quads — just add one cell and one digit.</p>

      <h2>A practical tip</h2>
      <p>Naked triples are easiest to find right after a round of <a href="/blog/sudoku-naked-pairs">naked pair</a> eliminations, because those reduce candidate counts and make the three-cell groupings stand out. Look in units that are about half-solved, where several cells carry just two or three candidates. And remember the mirror: a hidden triple hides three digits among extra candidates, the same way a <a href="/blog/sudoku-hidden-pairs">hidden pair</a> does — act on the three cells themselves rather than the rest of the unit.</p>"""

def body_pointing():
    return f"""      <p class="lede">A pointing pair (or pointing triple) is an interaction between a box and a line. When a digit's only possible cells inside a box all sit in the same row or column, that digit must end up in the box somewhere along that line — so it can be eliminated from the rest of that row or column outside the box. It's one of the most common intermediate eliminations and a staple of hard-puzzle solving.</p>

      <p>The technique is sometimes called "locked candidates, type 1." The candidates are locked because, although you don't yet know which cell of the box holds the digit, you know it lies on one particular line. That's enough to clear that line elsewhere.</p>

      <h2>How pointing works</h2>
      {build.dia_pointing()}
      {LEGEND_PATTERN}
      <p>Inside the top-middle box, the digit 3 can only go in two cells (amber) — and both lie in the same row. We don't know which of the two will be the 3, but we know the box's 3 is somewhere on that row. Since that row can contain only one 3 in total, no cell elsewhere in the row can be a 3. The candidate is removed from the cell to the left, outside the box (red).</p>

      <p>If the digit had been confined to two cells sharing a column instead, the same logic would point down the column. Three confined cells in a line make a pointing triple; the effect is identical.</p>

      <h2>How to spot it</h2>
      <p>For each box, take a digit it still needs and look at which of the box's empty cells can hold it. If all of those cells fall in a single row, or a single column, you have a pointing pattern. Then follow that line out of the box and erase the digit from every cell it touches.</p>

      <p>The cue to watch for is a digit whose candidates within a box are squeezed onto one line. This happens constantly on medium and hard boards, so it pays to check after every few placements.</p>

      <h2>Pointing vs. box/line reduction</h2>
      <p>Pointing pairs and <a href="/blog/sudoku-box-line-reduction">box/line reduction</a> are the two halves of the same box-line relationship, run in opposite directions. Pointing starts inside the box ("this digit is stuck on one line of the box, so clear the line") and eliminates along the line. Box/line reduction starts on the line ("this digit on the line can only be in one box, so clear the box") and eliminates inside the box. Solvers often confuse the two; the trick is to ask which unit is doing the confining.</p>

      <h2>Why it's useful</h2>
      <p>Pointing eliminations rarely solve a cell directly, but they thin out a line just enough to reveal a <a href="/blog/sudoku-hidden-singles">hidden single</a> or set up a <a href="/blog/sudoku-naked-pairs">naked pair</a>. On hard boards, a couple of well-spotted pointing pairs are often the difference between flow and frustration.</p>"""

def body_box_line():
    return f"""      <p class="lede">Box/line reduction — also called claiming or "locked candidates, type 2" — is the reverse of a pointing pair. When a digit's only possible cells in a row or column all fall inside a single 3×3 box, that digit is claimed by the line and can be eliminated from the rest of that box. It's an essential intermediate technique for unlocking hard Sudoku.</p>

      <p>The name captures the logic: the line "claims" the digit. You don't know which cell of the line will hold it, but you know it sits inside one particular box — so the other cells of that box can't.</p>

      <h2>How box/line reduction works</h2>
      {build.dia_box_line()}
      {LEGEND_PATTERN}
      <p>Look at the highlighted row. The digit 1 can only go in two of its cells (amber), and both of those cells happen to lie inside the same box. The row must contain a 1, so the 1 is somewhere in those two cells — which means it's definitely inside that box, on that row. Therefore no <em>other</em> cell in the box can be a 1, and the candidate is removed from the cell above (red), elsewhere in the same box.</p>

      <p>The elimination lands inside the box, not along the line — that's the difference from a pointing pair, where the elimination runs out along the line.</p>

      <h2>Spotting the pattern</h2>
      <p>Work line by line. For a row or column, pick a digit it still needs and find every cell on that line that can hold it. If all of those cells sit within one box, you have a box/line reduction. Then clear that digit from the box's other cells — the ones not on the original line.</p>

      <p>It helps to scan with pencil marks in place: you're hunting for a digit that appears as a candidate two or three times on a line, with all those appearances clustered in one box.</p>

      <h2>Telling it apart from pointing</h2>
      <p>This is the most common mix-up at the intermediate level, so it's worth a clear rule. Ask: <em>which unit confines the digit?</em></p>
      <ul>
        <li>If a <strong>box</strong> confines the digit to one line, it's a <a href="/blog/sudoku-pointing-pairs">pointing pair</a>, and you eliminate along the line.</li>
        <li>If a <strong>line</strong> confines the digit to one box, it's box/line reduction, and you eliminate inside the box.</li>
      </ul>
      <p>Both rely on the same overlap between a box and a line; they just read it from opposite ends.</p>

      <h2>Where it leads</h2>
      <p>Box/line reduction clears candidates inside a box, which frequently produces a <a href="/blog/sudoku-hidden-singles">hidden single</a> or tidies a box down to a <a href="/blog/sudoku-naked-pairs">naked pair</a>. Combined with pointing pairs, it resolves a large share of hard puzzles before you ever need advanced patterns like the X-Wing. To see how all eight techniques fit together, head back to the <a href="/blog/sudoku-strategies">Sudoku strategies guide</a>.</p>"""

# ============================================================ PAGE TABLE
PILLAR_REL = [("How to Solve Sudoku for Beginners", "/blog/how-to-solve-sudoku"),
              ("Play Sudoku Zen", "/games/sudoku"),
              ("Best Free Puzzle Games Online", "/blog/free-puzzle-games")]

PAGES = [
  dict(slug="sudoku-strategies", read=7,
       title="Sudoku Strategies: A Visual Guide",
       h1="Sudoku Strategies, Explained with Diagrams",
       desc="Eight Sudoku strategies, from last remaining cell to box/line reduction, each explained with a worked diagram. Solve hard puzzles by logic, not guesswork.",
       og_title="Sudoku Strategies, Explained with Diagrams",
       og_desc="Eight Sudoku techniques from beginner to intermediate, each with a worked diagram. Solve hard puzzles by logic, not guesswork.",
       body=body_pillar(),
       related=[("How to Solve Sudoku for Beginners", "/blog/how-to-solve-sudoku"),
                ("Naked Pairs in Sudoku", "/blog/sudoku-naked-pairs"),
                ("Hidden Singles in Sudoku", "/blog/sudoku-hidden-singles")]),

  dict(slug="sudoku-last-remaining-cell", read=4,
       title="Last Remaining Cell (Full House) in Sudoku",
       h1="The Last Remaining Cell (Full House)",
       desc="The last remaining cell is Sudoku's simplest move: when a row, column, or box has eight digits, the ninth is forced. Learn to spot full houses with a clear diagram.",
       og_title="Sudoku Last Remaining Cell, Explained",
       og_desc="When a unit has eight of nine digits, the last cell is forced. A worked diagram of the full house technique.",
       body=body_last_remaining(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Hidden Singles in Sudoku", "/blog/sudoku-hidden-singles"),
                ("How to Solve Sudoku for Beginners", "/blog/how-to-solve-sudoku")]),

  dict(slug="sudoku-hidden-singles", read=5,
       title="Hidden Singles in Sudoku",
       h1="Hidden Singles in Sudoku",
       desc="A hidden single is a digit with only one legal cell in its unit, even when that cell holds other candidates. The technique that solves most of a medium board.",
       og_title="Hidden Singles in Sudoku, Explained",
       og_desc="Find the digit that can only go in one cell of a unit. A clear, diagram-led guide to hidden singles.",
       body=body_hidden_singles(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Cross-Hatching (Slicing and Dicing)", "/blog/sudoku-cross-hatching"),
                ("Last Remaining Cell", "/blog/sudoku-last-remaining-cell")]),

  dict(slug="sudoku-cross-hatching", read=5,
       title="Cross-Hatching (Slicing and Dicing) in Sudoku",
       h1="Cross-Hatching: Slicing and Dicing",
       desc="Cross-hatching places a digit in a box by scanning the rows and columns that cross it. Learn the slicing-and-dicing technique with a step-by-step diagram.",
       og_title="Sudoku Cross-Hatching, Explained",
       og_desc="Scan rows and columns to place a digit inside a box. A visual guide to slicing and dicing.",
       body=body_cross_hatching(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Hidden Singles in Sudoku", "/blog/sudoku-hidden-singles"),
                ("Naked Pairs in Sudoku", "/blog/sudoku-naked-pairs")]),

  dict(slug="sudoku-naked-pairs", read=5,
       title="Naked Pairs in Sudoku",
       h1="Naked Pairs in Sudoku",
       desc="Two cells sharing the same two candidates lock those digits out of the rest of the unit. The first candidate-elimination technique, with a worked diagram.",
       og_title="Naked Pairs in Sudoku, Explained",
       og_desc="Two cells, two shared candidates — and the eliminations they unlock. A diagram-led guide.",
       body=body_naked_pairs(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Hidden Pairs in Sudoku", "/blog/sudoku-hidden-pairs"),
                ("Naked Triples and Quads", "/blog/sudoku-naked-triples")]),

  dict(slug="sudoku-hidden-pairs", read=5,
       title="Hidden Pairs in Sudoku",
       h1="Hidden Pairs in Sudoku",
       desc="A hidden pair is two digits confined to the same two cells, hidden among other candidates. Learn to find them and clear the clutter — with a step-by-step diagram.",
       og_title="Hidden Pairs in Sudoku, Explained",
       og_desc="Two digits with only two homes in a unit. Spot the hidden pair and clean out the rest.",
       body=body_hidden_pairs(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Naked Pairs in Sudoku", "/blog/sudoku-naked-pairs"),
                ("Pointing Pairs and Triples", "/blog/sudoku-pointing-pairs")]),

  dict(slug="sudoku-naked-triples", read=5,
       title="Naked Triples and Quads in Sudoku",
       h1="Naked Triples and Quads",
       desc="Three cells using only three candidates between them clear those digits from the rest of the unit. Naked triples and quads, with a worked diagram.",
       og_title="Naked Triples in Sudoku, Explained",
       og_desc="Three cells, three candidates — bulk candidate elimination explained with a diagram.",
       body=body_naked_triples(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Naked Pairs in Sudoku", "/blog/sudoku-naked-pairs"),
                ("Hidden Pairs in Sudoku", "/blog/sudoku-hidden-pairs")]),

  dict(slug="sudoku-pointing-pairs", read=5,
       title="Pointing Pairs and Triples in Sudoku",
       h1="Pointing Pairs and Triples",
       desc="A pointing pair eliminates a digit along a row or column when it's locked to one line inside a box. Learn this box-line interaction with a clear diagram.",
       og_title="Pointing Pairs in Sudoku, Explained",
       og_desc="When a digit is stuck on one line of a box, it points down that line. A diagram-led guide.",
       body=body_pointing(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Box/Line Reduction (Claiming)", "/blog/sudoku-box-line-reduction"),
                ("Naked Pairs in Sudoku", "/blog/sudoku-naked-pairs")]),

  dict(slug="sudoku-box-line-reduction", read=5,
       title="Box/Line Reduction (Claiming) in Sudoku",
       h1="Box/Line Reduction (Claiming)",
       desc="Box/line reduction eliminates a digit from a box when a row or column confines it there. The reverse of a pointing pair — explained with a step-by-step diagram.",
       og_title="Box/Line Reduction in Sudoku, Explained",
       og_desc="When a line confines a digit to one box, clear it from the rest of the box. A diagram-led guide.",
       body=body_box_line(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Pointing Pairs and Triples", "/blog/sudoku-pointing-pairs"),
                ("Hidden Singles in Sudoku", "/blog/sudoku-hidden-singles")]),
]

if __name__ == "__main__":
    for pg in PAGES:
        html = page(pg["slug"], pg["title"], pg["h1"], pg["desc"],
                    pg["og_title"], pg["og_desc"], pg["read"], pg["body"],
                    pg["related"])
        d = os.path.join(SITE, pg["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(html)
        print("wrote", pg["slug"], len(html), "bytes")
    print("DONE", len(PAGES), "pages")
