# Melhorias AdSense — implementadas

**Data:** 8 de junho de 2026
**Contexto:** resposta à rejeição *Low value content*. Implementação dos fixes estruturais + conteúdo de estratégia ilustrado para os três jogos.

---

## O que mudou

### Páginas estruturais (desbloqueadores P0)

| Item | Antes | Depois |
|---|---|---|
| Homepage (`/`) | 86 palavras (só hero + cartões) | **510 palavras** de conteúdo editorial original + cartões |
| Página About (`/about`) | inexistente | **criada** (~440 palavras, E-E-A-T: quem, missão, como é construído) |
| Página Contact (`/contact`) | inexistente | **criada** (email + motivos de contacto) |
| Footers | só Blog · Privacy · Terms | **About e Contact** adicionados em todas as 29 páginas |

### Conteúdo de estratégia com diagramas (o pedido do utilizador)

Os 10 posts de Sudoku já tinham diagramas SVG. O buraco era Minesweeper e 2048 (1 post cada, sem imagens). Foram criados **6 posts novos**, cada um com diagramas SVG **originais** (gerados por código — sem risco de copyright):

Minesweeper:
- `/blog/minesweeper-1-2-1-pattern` — padrões 1-2-1 e 1-2-2-1 (2 diagramas)
- `/blog/minesweeper-counting` — contagem e subtração 1-2 / 1-1 (2 diagramas)
- `/blog/minesweeper-probability` — 50/50, 1-em-3, contagem global (2 diagramas)

2048:
- `/blog/2048-corner-strategy` — estratégia de canto (1 diagrama)
- `/blog/2048-snake-pattern` — padrão snake (1 diagrama)
- `/blog/2048-endgame` — encadear merges até 2048 (1 diagrama)

### Wiring

- `blog/index.html` — 6 entradas novas adicionadas.
- `sitemap.xml` — 8 URLs novos (about, contact, 6 posts). Total: **29**.
- `firebase.json` — 8 redirects (301 trailing-slash) + 8 rewrites para clean URLs.
- `css/blog.css` — classes genéricas de diagrama (`.diagram`, `.diagram-figure`, `.diagram-legend`).
- `css/games.css` — bloco `.home-content` para o conteúdo da homepage.

### Estado do scan pós-implementação

```
Pages: 29 | total visible words: 15.901
Homepage words: 510
Trust pages: about ✓ · contact ✓ · privacy ✓ · terms ✓
ads.txt: ✓ | HTML lang: en
Privacy disclosure: adsense ✓ · cookies ✓ · third-party ✓ · opt-out ✓
```

---

## Verificação feita

- HTML e SVG balanceados em todas as páginas novas.
- Zero links internos partidos; zero duplicados em footers.
- 9 diagramas renderizados e validados visualmente (lógica correta: mines sob os 1s / safe sob o 2, subtração 1-2, redução 1-1, 50/50 vs. 1-em-3, canto/snake/endgame).
- `firebase.json` valida como JSON; 29 páginas = 29 URLs no sitemap.

---

## Checklist de resubmissão (ordem importa)

- [x] Homepage ≥ 500 palavras de conteúdo original
- [x] Página `/about` criada e ligada em todos os footers
- [x] Página `/contact` criada e ligada em todos os footers
- [x] Conteúdo de estratégia ilustrado para os 3 jogos
- [x] `sitemap.xml`, `firebase.json` e blog index atualizados
- [ ] **Deploy** (`npm run deploy`)
- [ ] Confirmar páginas novas indexadas no Search Console (3–7 dias)
- [ ] Só então: marcar "I confirm I have fixed the issues" → **Request review**

> Não pedir review no mesmo dia do deploy — dá ao revisor uma versão ainda não rastreada.

---

## Pendente / opcional (não bloqueia)

- Expandir o texto de apoio das 3 páginas de jogo (~250 → ~500 palavras) para baixar o futuro rácio anúncio/conteúdo (P1 no relatório original).
- Ao ligar anúncios: máx. 1–2 unidades por página, nunca sobre o tabuleiro; configurar tratamento child-directed (COPPA).
