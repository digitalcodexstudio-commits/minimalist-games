# Publicação faseada dos posts — guião

Três posts de investigação original, prontos nesta pasta `drafts/` (que o Firebase não serve).
Cada um tem a data de publicação já escrita no HTML. Publicar = um comando + push.

| Data | Slug | Post |
|---|---|---|
| **25 nov 2026** | `minesweeper-luck-vs-skill` | How Much of Minesweeper Is Luck? We Played 750,000 Games |
| **10 dez 2026** | `2048-strategies-tested` | We Tested Every 2048 Strategy. Here's What Actually Wins |
| **30 dez 2026** | `sudoku-difficulty-clue-count` | Fewer Clues Doesn't Mean a Harder Sudoku: What 4,000 Puzzles Show |

## Em cada data

```bash
cd /Users/alima/Documents/Claude/Projects/minimalist-games
python3 tools/publish_post.py <slug>
git add -A && git commit -m "content: publish <slug>" && git push
```

O script move o post para `src/blog/`, acrescenta o rewrite ao `firebase.json`, a entrada no blog index e no sitemap, aplica os ficheiros de `drafts/<slug>/also/` e corre o `verify_site.py`. Se o verificador der erros, pára antes de mudares alguma coisa no git. `--check` mostra o que faria sem mexer em nada.

Depois do push: Search Console → URL inspection → `https://minimalist-games.com/blog/<slug>` → **Request indexing**.

## O que cada publicação também actualiza (pasta `also/`)

- **minesweeper-luck-vs-skill** → corrige `minesweeper-openings`: deixa de recomendar o canto e passa a recomendar o centro (com as regras do nosso jogo, clique inicial + 8 vizinhos seguros, o centro ganha em todos os níveis — ver os dados no post).
- **2048-strategies-tested** → acrescenta em `2048-tips` uma frase com link para o novo post, na secção "Never swipe up".
- **sudoku-difficulty-clue-count** → acrescenta em `how-sudoku-puzzles-are-generated` o link para o novo post.

Estes ficheiros são cópias completas das páginas. **Se editares um desses três posts antes da data, edita também a cópia em `also/`**, senão a publicação substitui a tua edição.

## Não publicar antes da data

O objectivo é mostrar ao AdSense publicação regular ("ongoing curation"). Os três de uma vez, ou fora de ordem, estragam isso.

## De onde vêm os números

Todos os dados foram gerados pelos programas em `tools/research/` (ver o README dessa pasta), com as regras exactas dos jogos do site. Os posts têm link para essa pasta no GitHub.
