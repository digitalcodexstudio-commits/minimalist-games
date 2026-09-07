# -*- coding: utf-8 -*-
"""Assemble the 9 Sudoku-strategy HTML pages from verified diagrams + prose."""
import os, build

import os
SITE = os.path.join(os.path.dirname(__file__), "..", "..", "src", "blog")
BASE = "https://minimalist-games.com"
DATE_ISO = "2026-06-03"
DATE_HUMAN = "June 3, 2026"
DATE_MODIFIED = "2026-09-07"

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
        ("Beginner", "Last Remaining Cell", "#last-remaining-cell",
         "The single missing digit in an almost-full row, column, or box."),
        ("Beginner", "Hidden Singles", "#hidden-singles",
         "A digit with only one legal home in a unit — even when the cell looks busy."),
        ("Beginner", "Cross-Hatching", "#cross-hatching",
         "Scan rows and columns to place a digit inside a box."),
        ("Intermediate", "Naked Pairs", "/blog/sudoku-naked-pairs#naked-pairs",
         "Two cells sharing the same two candidates lock those digits in."),
        ("Intermediate", "Hidden Pairs", "/blog/sudoku-naked-pairs#hidden-pairs",
         "Two digits confined to two cells clear everything else out of them."),
        ("Intermediate", "Naked Triples", "/blog/sudoku-naked-pairs#naked-triples",
         "Three cells, three candidates — and the quads that follow."),
        ("Intermediate", "Pointing Pairs", "/blog/sudoku-pointing-pairs#pointing-pairs",
         "A digit trapped on one line of a box points down that line."),
        ("Intermediate", "Box/Line Reduction", "/blog/sudoku-pointing-pairs#box-line-reduction",
         "The reverse: a line confines a digit to a single box."),
    ]
    grid = "\n".join(
        f'        <li><a href="{u}"><span class="level-tag">{lv}</span>'
        f'<h3>{t}</h3><p>{d}</p></a></li>'
        for lv, t, u, d in cards)
    return f"""      <p class="lede">Most people learn Sudoku by scanning for obvious numbers, then hit a wall on harder boards and assume they need to guess. They don't. Every standard Sudoku is solvable by pure logic — you just need a bigger toolbox. This guide walks through the eight techniques that carry you from beginner to confident solver, each one explained with a worked diagram you can read at a glance.</p>

      <p>The strategies build on each other. The first three place digits directly and need no notes; they are covered in full on this page. The next five work on <strong>pencil marks</strong> — the small candidate numbers you jot into empty cells — and clear those candidates away until placements appear. Those are covered in two companion guides, linked below. Learn them in order and each new technique will feel like a natural extension of the last.</p>

      <p>If you want a board to practise on while you read, open <a href="/games/sudoku">Sudoku Zen</a> in another tab. Its notes mode lets you pencil-mark candidates exactly as the diagrams below show. Brand new to the game? Start with <a href="/blog/how-to-solve-sudoku">how to solve Sudoku for beginners</a> first, then come back here.</p>

      <h2>The eight techniques</h2>
      <ul class="strategy-grid">
{grid}
      </ul>

      <h2>How the techniques fit together</h2>
      <p>Beginner techniques — last remaining cell, hidden singles, and cross-hatching — are about <em>placing</em> digits. They finish easy boards on their own and get you most of the way through a medium one. None of them require notes; you do them by looking. All three are explained below.</p>

      <p>Intermediate techniques are about <em>eliminating</em> candidates so that a placement becomes possible. Naked and hidden pairs, naked triples, pointing pairs, and box/line reduction never put a number on the board by themselves. Instead they shave possibilities off other cells until a hidden single or last remaining cell appears. That two-step rhythm — eliminate, then place — is the whole game at the intermediate level.</p>

      <p>Once these are reflexive, the advanced patterns (X-Wing, Swordfish, XY-Wing) are just the same idea stretched across several rows and columns at once. For now, master the eight here and you'll solve the vast majority of "hard"-rated puzzles without ever guessing.</p>

      <h2 id="last-remaining-cell">The last remaining cell (full house)</h2>
      <p>The last remaining cell — sometimes called a "full house" — is the simplest move in Sudoku. When a row, column, or 3×3 box already contains eight of its nine digits, the empty cell can only be the one that's missing. It's the first technique every solver learns, and it's worth doing deliberately rather than by accident.</p>

      <p>Sudoku's one rule is that every row, every column, and every 3×3 box must contain the digits 1 through 9 exactly once. The last remaining cell is that rule at its most direct: count what's there, name what's missing, write it in.</p>

      {build.dia_last_remaining()}
      {LEGEND_PATTERN}
      <p>In the row above, eight cells are already filled. Reading along, the digits present are 5, 3, 4, 6, 7, 8, 9, and 1 — every digit except 2. Since the row must contain a 2 somewhere and there is only one empty cell left, the 2 goes there. No candidates, no notes, no doubt.</p>

      <p>The same logic applies to columns and boxes. Whenever a unit is down to its last empty cell, you can fill it instantly. These moments cascade: filling one last cell often completes a neighbouring unit, which completes another, and a corner of the board falls in seconds.</p>

      <h3>Where to look for them</h3>
      <p>Last remaining cells appear most often near the end of a solve, but they also show up early in any unit that started with lots of clues. Scan the board for the rows, columns, and boxes that look most crowded — the ones with seven or eight digits already placed. Those are where a single missing number is easiest to spot.</p>

      <p>A practical habit: every time you place a digit anywhere, glance at the three units that cell belongs to (its row, its column, its box). If placing your digit left any of them with exactly one empty cell, fill that cell immediately before moving on. This keeps the cascade going and stops you from re-scanning the same regions.</p>

      <h3>Last remaining cell vs. naked single</h3>
      <p>These two sound alike but come from opposite directions. A <strong>last remaining cell</strong> looks at a whole unit and asks "which digit is missing?" A <a href="/blog/how-to-solve-sudoku">naked single</a> looks at one cell and asks "which digits are still allowed here?" — checking its row, column, and box together. Both leave exactly one answer, but they're found by scanning differently. The last remaining cell is usually the faster of the two to spot because you only have to read one line.</p>

      <p>It's tempting to dismiss the last remaining cell as too obvious to name. But solvers who treat it as a deliberate step — actively hunting for almost-full units — finish easy and medium boards far faster than those who only notice these cells by luck. It costs nothing, and it's the foundation every harder technique is built on.</p>

      <h2 id="hidden-singles">Hidden singles</h2>
      <p>A hidden single is a digit that can legally go in only one cell of a row, column, or box — even though that cell looks like it has several options. It's the most useful beginner technique after basic scanning, and it's the one that quietly solves most of a medium Sudoku. Learning to see hidden singles is the moment Sudoku starts to click.</p>

      <p>The word "hidden" is the key. With a last remaining cell or a naked single, the cell itself obviously has one answer. A hidden single is disguised: the cell carries two or three candidates, so nothing about it stands out. The single only appears when you look at the whole unit and notice that one particular digit has nowhere else to go.</p>

      {build.dia_hidden_single()}
      {LEGEND_PATTERN}
      <p>Look only at the top-right box. Three cells are empty, with candidates {{4, 6}}, {{4, 5}}, and {{4, 6}}. If you judged the middle cell on its own, you couldn't decide between 4 and 5. But scan the box for the digit 5 specifically: it appears in just one of the three cells. The box must contain a 5 somewhere, and there is only one cell that accepts it — so 5 is placed, even though that cell also listed a 4.</p>

      <p>That's the whole technique. Instead of asking "what can go in this cell?", you ask "where in this unit can this digit go?" When the answer is "only here," you have a hidden single.</p>

      <h3>How to hunt for them</h3>
      <p>Work one digit at a time within one unit. Pick a box, then run through the digits it's still missing. For each missing digit, count how many of the box's empty cells could legally hold it — remembering that a digit is blocked if it already appears in that cell's row or column. If exactly one cell survives, place the digit.</p>

      <p>Boxes are the easiest place to start because the 3×3 shape makes the elimination visual, but hidden singles live in rows and columns too. After you've swept the boxes, run the same check along any row or column that still has several gaps.</p>

      <h3>Why they're easy to miss</h3>
      <p>Beginners overlook hidden singles because they scan cell by cell, and a hidden single's cell never looks special — it has the same two or three candidates as its neighbours. The fix is to switch your unit of attention from the cell to the digit. Once you train yourself to ask "where can the 5 go in this box?" the hidden singles light up.</p>

      <p>This is also why pencil marks help. With every cell's candidates written in, a hidden single is visible the moment you notice a digit that appears only once across a unit. On <a href="/games/sudoku">Sudoku Zen</a>, turn on notes mode and the pattern becomes much easier to spot.</p>

      <h2 id="cross-hatching">Cross-hatching (slicing and dicing)</h2>
      <p>Cross-hatching — also called slicing and dicing — is the scanning method that places a digit inside a 3×3 box by reading the rows and columns that pass through it. It's how experienced solvers fill in numbers quickly without writing a single pencil mark, and it's the most efficient way to find hidden singles in a box.</p>

      <p>The idea is simple. A box needs each digit exactly once. If the rows and columns crossing that box already contain a particular digit, they block most of the box's cells. Often they block all but one — and that surviving cell is where the digit must go.</p>

      {build.dia_cross_hatch()}
      {LEGEND_PATTERN}
      <p>We want to place a 1 in the bottom-left box. Look at the rows passing through it: the top two rows of the box already contain a 1 elsewhere on the board (the amber lines), so a 1 can't go in either of those rows inside the box. That leaves only the bottom row. Now look at the columns: the left and right columns of the box already have a 1, leaving only the middle column. The one cell that sits on both the open row and the open column is forced — the 1 goes there.</p>

      <p>"Slicing" refers to the horizontal scan across rows; "dicing" is the vertical scan down columns. Doing both narrows a box from nine cells to one without any notes.</p>

      <h3>How to do it efficiently</h3>
      <p>Pick a digit that already appears several times on the board — a digit with five or six placements gives you the most blocking lines to work with. Then check each box that's still missing it. For every such box, mentally extend the rows and columns that already contain the digit; if they cut the box down to a single open cell, place it.</p>

      <p>Cycle through the digits this way, 1 to 9, and you'll place a surprising number of cells. When a digit stops yielding placements, move to the next. This systematic sweep is the engine of fast solving on easy and medium boards.</p>

      <h3>Cross-hatching vs. hidden singles</h3>
      <p>These are two views of the same logic. A hidden single describes the <em>result</em> — a digit with only one legal cell in a unit. Cross-hatching is the <em>technique</em> you use to find that result inside a box, by scanning the crossing lines. If you prefer working from pencil marks, you'll spot the hidden single in the notes; if you prefer scanning a clean board, you'll cross-hatch your way to the same cell.</p>

      <h2>When scanning runs out</h2>
      <p>Cross-hatching solves easy boards almost entirely and gets you deep into medium ones. When no box can be sliced down to a single cell and no unit is one digit from full, scanning has done its job. That's the moment to start pencil-marking and move to candidate elimination — the techniques that don't place digits directly, but remove possibilities until scanning works again.</p>

      <p>They come in two families, one per guide:</p>
      <ul>
        <li><strong><a href="/blog/sudoku-naked-pairs">Naked and hidden pairs, triples and quads</a></strong> — subsets. A group of cells reserves a group of digits, and everything else in the unit gives those digits up.</li>
        <li><strong><a href="/blog/sudoku-pointing-pairs">Pointing pairs and box/line reduction</a></strong> — intersections. A box and a line overlap, and one confines a digit inside the other.</li>
      </ul>

      <h2>A note on guessing</h2>
      <p>You may have seen "guess and check" listed as a Sudoku method. It works, but it isn't solving — it's brute force, and on a contaminated board it's hard to undo. Every technique in this guide is deductive: each move is forced by the rules, so you can always explain <em>why</em> a digit goes where it does. That's the difference between finishing a puzzle and actually getting better at them.</p>"""

def body_subsets():
    return f"""      <p class="lede">Once scanning stalls, Sudoku becomes a game of elimination — and subsets are where that game starts. A subset is a group of cells in one unit that, between them, have a claim on the same group of digits. Two cells and two digits make a pair; three cells and three digits make a triple; four make a quad. This guide covers all of them, naked and hidden, each with a worked diagram.</p>

      <p>Every subset technique needs pencil marks — the small candidate numbers you write into empty cells. Fill them in first, then look for the patterns below. None of these techniques place a digit on their own. What they do is clear candidates away until a <a href="/blog/sudoku-strategies#hidden-singles">hidden single</a> or a <a href="/blog/sudoku-strategies#last-remaining-cell">last remaining cell</a> appears somewhere nearby, and that's what actually fills the board.</p>

      <p>The naked/hidden distinction runs through all of them, and it's worth fixing in your head before you start. A <strong>naked</strong> subset is visible in the cells: those cells contain nothing but the subset's digits, and you act on the <em>rest of the unit</em>. A <strong>hidden</strong> subset is buried among other candidates, and you act on the <em>subset cells themselves</em>. Same logic, opposite target.</p>

      <h2 id="naked-pairs">Naked pairs</h2>
      <p>A naked pair is two cells in the same row, column, or box that contain exactly the same two candidates — and nothing else. Because those two digits must occupy those two cells between them, they can be eliminated from every other cell in the unit. It's the first real candidate-elimination technique, and the gateway to solving hard puzzles.</p>

      {build.dia_naked_pair()}
      {LEGEND_PATTERN}
      <p>In this box, two cells both hold exactly {{3, 7}} (amber). We don't know yet which is the 3 and which is the 7 — but we know that between them they will use up both digits. That means no other cell in the box can be a 3 or a 7. So those candidates are struck from every other cell in the box (red). In the cell that had {{3, 4}}, the 3 disappears and it becomes a plain 4 — a placement, handed to you for free.</p>

      <p>The pair doesn't have to be solved to be useful. Its power comes entirely from the fact that two cells are reserved for two digits, locking those digits out of the rest of the unit.</p>

      <h3>What counts as a naked pair</h3>
      <p>Three conditions must all hold. The two cells must share the same unit — a row, a column, or a box. They must contain exactly two candidates each, no more. And those two candidates must be identical in both cells. {{3, 7}} and {{3, 7}} qualify; {{3, 7}} and {{3, 8}} do not, and neither does {{3, 7}} paired with {{3, 7, 9}}.</p>

      <p>If the two cells happen to share more than one unit — say they're in the same row <em>and</em> the same box — then you can eliminate the pair's digits from both units at once. Those overlap cases are where naked pairs cascade fastest.</p>

      <h3>Finding them at the table</h3>
      <p>Scan for cells that have exactly two pencil marks — bivalue cells. Whenever you find one, glance along its row, down its column, and around its box for a twin with the identical pair. Pairs are easiest to catch right after you finish pencil-marking, while the candidate counts are fresh in your mind.</p>

      <h2 id="hidden-pairs">Hidden pairs</h2>
      <p>A hidden pair is two digits that can only appear in the same two cells of a unit — even though those cells also carry other candidates. When you find one, every <em>other</em> candidate can be wiped from those two cells, leaving just the pair. It's the trickiest of the pair techniques to spot, and one of the most satisfying.</p>

      <p>Where a naked pair announces itself (two cells, two candidates, identical), a hidden pair is camouflaged. The two cells might show three, four, or five candidates each. The pair is "hidden" inside that clutter, and you only find it by tracking where two specific digits are allowed to go.</p>

      {build.dia_hidden_pair()}
      {LEGEND_PATTERN}
      <p>Scan this column for the digits 1 and 3. Both of them can only go in the same two cells (amber) — nowhere else in the column accepts a 1 or a 3. That's the hidden pair. Now reason it through: those two cells must hold the 1 and the 3 between them, so they can't hold anything else. Every other candidate in them — here an 8 in each — is removed (red). The two cells collapse to a clean {{1, 3}}, which is now a naked pair as well.</p>

      <p>Notice the direction of the elimination. A naked pair clears candidates from the <em>rest</em> of the unit. A hidden pair clears candidates from the <em>pair cells themselves</em>. Same family of logic, opposite target.</p>

      <h3>How to find a hidden pair</h3>
      <p>Go through a unit two digits at a time, or watch for digits that are scarce. For each pair of digits, count the cells in the unit where each one can go. If two different digits are both restricted to the same two cells, you've found a hidden pair — regardless of what other candidates those cells contain.</p>

      <p>In practice the shortcut is to look for digits that appear as candidates only twice in a unit. If two such digits share the same two cells, the pattern is there. It takes more searching than a naked pair, which is exactly why beginners miss it.</p>

      <h3>Why it's worth the effort</h3>
      <p>Hidden pairs often appear on hard boards precisely where no other move is available. Because the elimination cleans up the pair cells, it frequently turns one of them into a bivalue cell that feeds a naked pair, a <a href="/blog/sudoku-pointing-pairs#pointing-pairs">pointing pair</a>, or a chain elsewhere. One hidden pair can unstick an entire region.</p>

      <h2 id="naked-triples">Naked triples and quads</h2>
      <p>A naked triple is three cells in a unit that, between them, use only three candidate digits. As with naked pairs, those three digits are reserved for those three cells, so they can be eliminated everywhere else in the unit. Quads extend the same idea to four cells and four digits. These techniques clear candidates in bulk and often crack a stalled hard board.</p>

      <p>The subtlety that trips people up: each of the three cells does <em>not</em> need to contain all three digits. They only need to draw from the same pool of three. {{2, 5}}, {{5, 8}}, and {{2, 8}} form a perfectly valid naked triple even though no single cell shows all of 2, 5, and 8.</p>

      {build.dia_naked_triple()}
      {LEGEND_PATTERN}
      <p>Three cells in this column (amber) hold candidates drawn entirely from {{2, 5, 8}}. Whatever the exact arrangement, those three cells will consume the 2, the 5, and the 8 among themselves. So none of those digits can live anywhere else in the column, and they're struck from every other cell (red). One elimination like this can remove several candidates at once and immediately expose a placement.</p>

      <h3>Recognising the pattern</h3>
      <p>You're looking for any three cells in a unit whose combined candidates total exactly three distinct digits. The valid shapes are:</p>
      <ul>
        <li>Three cells each with the same three candidates: {{2,5,8}}, {{2,5,8}}, {{2,5,8}}.</li>
        <li>A mix of pairs and triples that overlap into three digits: {{2,5}}, {{5,8}}, {{2,8}} or {{2,5,8}}, {{2,5}}, {{5,8}}.</li>
      </ul>
      <p>If the three cells together use a fourth digit, it isn't a triple. Counting the union of candidates is the reliable test: three cells, three digits total.</p>

      <h3>Naked quads</h3>
      <p>A naked quad is the same logic with four cells and four shared candidates. It's genuinely rare in everyday puzzles and tedious to scan for, so most solvers only reach for it on the hardest grids when nothing simpler is available. If you've mastered triples, you already understand quads — just add one cell and one digit.</p>

      <h3>Hidden triples</h3>
      <p>The mirror applies here too. A hidden triple is three digits confined to the same three cells, buried among other candidates — and as with the hidden pair, you clear everything else out of those three cells. It's rarer and harder to see than a hidden pair, and in practice most solvers find the equivalent naked subset first, after other eliminations have thinned the cells down. The logic is identical: find the digits that have nowhere else to go.</p>

      <h2>Which subset to look for first</h2>
      <p>Order matters, because each technique makes the next easier to see. A workable sweep:</p>
      <ol>
        <li><strong>Naked pairs.</strong> Fastest to spot — you're just looking for twin bivalue cells.</li>
        <li><strong>Hidden pairs.</strong> Look for digits that appear only twice in a unit.</li>
        <li><strong>Naked triples.</strong> Easiest right after a round of pair eliminations, because those reduce candidate counts and make the three-cell groupings stand out. Look in units that are about half-solved.</li>
        <li><strong>Quads and hidden triples.</strong> Last resort, on the hardest boards only.</li>
      </ol>

      <p>There's also a counting shortcut worth knowing. In a unit with <em>n</em> unsolved cells, a hidden subset of size <em>k</em> is always accompanied by a naked subset of size <em>n − k</em>, and vice versa. On a nearly-full unit the naked version is smaller and easier to see; on a wide-open unit the hidden version is. Look for whichever is smaller and you'll do less work for the same eliminations.</p>

      <h2>Where subsets lead</h2>
      <p>Subsets work inside a single unit. The other family of intermediate techniques works <em>between</em> units, where a box and a line overlap — that's <a href="/blog/sudoku-pointing-pairs">pointing pairs and box/line reduction</a>, and the two families feed each other constantly on hard boards. For the full picture of how all eight techniques fit together, head back to the <a href="/blog/sudoku-strategies">Sudoku strategies guide</a>.</p>"""

def body_intersections():
    return f"""      <p class="lede">Pointing pairs and box/line reduction are the two intersection techniques — sometimes filed together as "locked candidates." Both exploit the same fact: every 3×3 box overlaps three rows and three columns, so a digit confined within one of those units tells you something about the other. Learn both together, because they are the same insight read from opposite ends.</p>

      <p>Unlike the <a href="/blog/sudoku-naked-pairs">subset techniques</a>, which work inside a single unit, these look at the three cells where a box and a line cross. That overlap is the whole mechanism. If a digit is stuck inside the overlap, whichever unit did the confining, the <em>other</em> unit loses that candidate everywhere outside it.</p>

      <h2 id="pointing-pairs">Pointing pairs and triples</h2>
      <p>A pointing pair (or pointing triple) is an interaction between a box and a line. When a digit's only possible cells inside a box all sit in the same row or column, that digit must end up in the box somewhere along that line — so it can be eliminated from the rest of that row or column outside the box. It's one of the most common intermediate eliminations and a staple of hard-puzzle solving.</p>

      <p>The technique is sometimes called "locked candidates, type 1." The candidates are locked because, although you don't yet know which cell of the box holds the digit, you know it lies on one particular line. That's enough to clear that line elsewhere.</p>

      {build.dia_pointing()}
      {LEGEND_PATTERN}
      <p>Inside the top-middle box, the digit 3 can only go in two cells (amber) — and both lie in the same row. We don't know which of the two will be the 3, but we know the box's 3 is somewhere on that row. Since that row can contain only one 3 in total, no cell elsewhere in the row can be a 3. The candidate is removed from the cell to the left, outside the box (red).</p>

      <p>If the digit had been confined to two cells sharing a column instead, the same logic would point down the column. Three confined cells in a line make a pointing triple; the effect is identical.</p>

      <h3>How to spot it</h3>
      <p>For each box, take a digit it still needs and look at which of the box's empty cells can hold it. If all of those cells fall in a single row, or a single column, you have a pointing pattern. Then follow that line out of the box and erase the digit from every cell it touches.</p>

      <p>The cue to watch for is a digit whose candidates within a box are squeezed onto one line. This happens constantly on medium and hard boards, so it pays to check after every few placements.</p>

      <h2 id="box-line-reduction">Box/line reduction (claiming)</h2>
      <p>Box/line reduction — also called claiming or "locked candidates, type 2" — is the reverse of a pointing pair. When a digit's only possible cells in a row or column all fall inside a single 3×3 box, that digit is claimed by the line and can be eliminated from the rest of that box.</p>

      <p>The name captures the logic: the line "claims" the digit. You don't know which cell of the line will hold it, but you know it sits inside one particular box — so the other cells of that box can't.</p>

      {build.dia_box_line()}
      {LEGEND_PATTERN}
      <p>Look at the highlighted row. The digit 1 can only go in two of its cells (amber), and both of those cells happen to lie inside the same box. The row must contain a 1, so the 1 is somewhere in those two cells — which means it's definitely inside that box, on that row. Therefore no <em>other</em> cell in the box can be a 1, and the candidate is removed from the cell above (red), elsewhere in the same box.</p>

      <p>The elimination lands inside the box, not along the line — that's the difference from a pointing pair, where the elimination runs out along the line.</p>

      <h3>Spotting the pattern</h3>
      <p>Work line by line. For a row or column, pick a digit it still needs and find every cell on that line that can hold it. If all of those cells sit within one box, you have a box/line reduction. Then clear that digit from the box's other cells — the ones not on the original line.</p>

      <p>It helps to scan with pencil marks in place: you're hunting for a digit that appears as a candidate two or three times on a line, with all those appearances clustered in one box.</p>

      <h2>Telling the two apart</h2>
      <p>This is the most common mix-up at the intermediate level, so it's worth a clear rule. Ask: <em>which unit confines the digit?</em></p>
      <ul>
        <li>If a <strong>box</strong> confines the digit to one line, it's a <strong>pointing pair</strong>, and you eliminate along the line, outside the box.</li>
        <li>If a <strong>line</strong> confines the digit to one box, it's <strong>box/line reduction</strong>, and you eliminate inside the box, off the line.</li>
      </ul>

      <p>A useful way to hold it in your head: the elimination always happens in the unit that did <em>not</em> do the confining, and always outside the overlap. The three cells where the box and the line cross are never touched — they're the cells you've just proven the digit lives in.</p>

      <p>Both rely on the same overlap between a box and a line; they just read it from opposite ends. If you find yourself unsure which one you're looking at, name the unit you counted the candidates in. That unit is the one doing the confining, and the elimination goes in the other.</p>

      <h2>Scanning for both in one pass</h2>
      <p>Because the two techniques share a mechanism, it's efficient to hunt for them together rather than in separate sweeps. Pick a digit — say the 4 — and work through the board once with only that digit in mind:</p>
      <ol>
        <li>For each box still missing a 4, check whether its candidate cells share a row or a column. If so, clear the 4 from the rest of that line.</li>
        <li>For each row and column still missing a 4, check whether its candidate cells all sit in one box. If so, clear the 4 from the rest of that box.</li>
        <li>Move to the next digit.</li>
      </ol>

      <p>One digit at a time is the key. Trying to watch all nine at once is what makes these techniques feel hard; restricting your attention to a single digit turns them into a mechanical check that takes seconds per box.</p>

      <h2>The same overlap, read both ways</h2>
      <p>It helps to see the two techniques on one piece of board. Take the top-left box and the top row of the grid. They share exactly three cells — call them the overlap — and each unit has six cells of its own outside it.</p>

      <p>Now suppose you are chasing the digit 7. Two different observations are possible, and they lead in opposite directions:</p>
      <ul>
        <li><strong>You count the 7s inside the box</strong> and find that every cell able to hold one lies in the overlap. The box's 7 is therefore on the top row. The box is satisfied either way, so nothing changes inside it — but the row now has its 7 accounted for, and you clear the candidate from the row's six other cells. That's a pointing pair.</li>
        <li><strong>You count the 7s along the row</strong> and find that every cell able to hold one lies in the overlap. The row's 7 is therefore inside the top-left box. The row is satisfied either way — but the box now has its 7 accounted for, and you clear the candidate from the box's six other cells. That's box/line reduction.</li>
      </ul>

      <p>Same three cells, same digit, two completely different eliminations. What decides which one you get is simply which unit you counted in and found the digit confined. Nothing about the overlap itself tells you; the answer is in the six cells you looked at outside it.</p>

      <h3>The mistake to avoid</h3>
      <p>The error almost everyone makes at least once is eliminating in the wrong direction — spotting a pointing pair and then clearing candidates inside the box rather than along the line. It produces a contradiction several moves later, by which point the cause is hard to trace.</p>

      <p>The guard against it is to say the deduction out loud before you erase anything: "the box's 7 is on this row, so the row's other cells lose it." If the sentence doesn't end with the unit you're about to erase from, stop and re-read the pattern. Both halves of the sentence matter, and getting them the right way round is the entire technique.</p>

      <h2>Why intersections matter</h2>
      <p>Intersection eliminations rarely solve a cell directly. What they do is thin out a line or a box just enough to reveal a <a href="/blog/sudoku-strategies#hidden-singles">hidden single</a>, or to set up a <a href="/blog/sudoku-naked-pairs#naked-pairs">naked pair</a> that clears more candidates in turn. On hard boards, a couple of well-spotted pointing pairs are often the difference between flow and frustration.</p>

      <p>They also mark the ceiling of intermediate play. Combined with the subset techniques, pointing and claiming resolve a large share of hard puzzles before you ever need advanced patterns like the X-Wing — which, when you get there, is recognisably the same idea stretched across two rows and two columns at once. For the full picture of how all eight techniques fit together, head back to the <a href="/blog/sudoku-strategies">Sudoku strategies guide</a>.</p>"""

# ============================================================ PAGE TABLE
PAGES = [
  dict(slug="sudoku-strategies", read=10,
       title="Sudoku Strategies: A Visual Guide",
       h1="Sudoku Strategies, Explained with Diagrams",
       desc="Eight Sudoku strategies, from last remaining cell to box/line reduction, each explained with a worked diagram. Solve hard puzzles by logic, not guesswork.",
       og_title="Sudoku Strategies, Explained with Diagrams",
       og_desc="Eight Sudoku techniques from beginner to intermediate, each with a worked diagram. Solve hard puzzles by logic, not guesswork.",
       body=body_pillar(),
       related=[("How to Solve Sudoku for Beginners", "/blog/how-to-solve-sudoku"),
                ("Naked and Hidden Pairs, Triples and Quads", "/blog/sudoku-naked-pairs"),
                ("Pointing Pairs and Box/Line Reduction", "/blog/sudoku-pointing-pairs")]),

  dict(slug="sudoku-naked-pairs", read=9,
       title="Naked and Hidden Pairs, Triples and Quads",
       h1="Naked and Hidden Pairs, Triples and Quads",
       desc="Naked pairs, hidden pairs, naked triples and quads explained with worked diagrams. The subset techniques that clear candidates and unlock hard Sudoku puzzles.",
       og_title="Sudoku Subsets: Naked and Hidden Pairs, Triples and Quads",
       og_desc="Two cells, two digits — and everything that follows. The complete guide to Sudoku subset techniques, with diagrams.",
       body=body_subsets(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Pointing Pairs and Box/Line Reduction", "/blog/sudoku-pointing-pairs"),
                ("How to Solve Sudoku for Beginners", "/blog/how-to-solve-sudoku")]),

  dict(slug="sudoku-pointing-pairs", read=8,
       title="Pointing Pairs and Box/Line Reduction",
       h1="Pointing Pairs and Box/Line Reduction",
       desc="The two Sudoku intersection techniques, explained side by side with worked diagrams — when a box confines a digit to a line, and when a line confines it to a box.",
       og_title="Pointing Pairs and Box/Line Reduction in Sudoku",
       og_desc="Locked candidates, both directions. Learn the box-line interaction with worked diagrams.",
       body=body_intersections(),
       related=[("Sudoku Strategies guide", "/blog/sudoku-strategies"),
                ("Naked and Hidden Pairs, Triples and Quads", "/blog/sudoku-naked-pairs"),
                ("How Sudoku Puzzles Are Generated", "/blog/how-sudoku-puzzles-are-generated")]),
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
