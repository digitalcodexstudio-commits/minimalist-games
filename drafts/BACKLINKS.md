# Backlinks — rascunhos para publicares

Preparado a 7 de Setembro de 2026. Objectivo: 3–5 domínios externos a linkar `minimalist-games.com` antes da janela de resubmissão ao AdSense (Novembro). Hoje são **0**.

**Publica tu.** Tudo aqui precisa das tuas contas e da tua voz. Os textos estão em inglês, prontos a copiar.

---

## Antes de começares: o que vale e o que não vale

Quase todos os links que vais conseguir são **nofollow** — Reddit, Hacker News, itch.io, GitHub. Isso não os torna inúteis, mas convém saber porquê valem:

- **Descoberta.** O Google rastreia estes sites constantemente. Um link novo é uma rota nova até ti.
- **Tráfego real.** É o que falta na candidatura ao AdSense: ~1 clique/dia é pouco para qualquer revisor. Um bom post no Reddit faz mais visitas numa tarde do que o site faz num mês.
- **Sinal de existência.** Um site que ninguém menciona parece abandonado. Um site mencionado em cinco sítios credíveis parece um site.

**O que NÃO fazer:** os "directórios de submissão" genéricos que aparecem em qualquer pesquisa (webrankdirectory, postfreedirectory, submitdirs e afins) são esquemas de links. O Google desvaloriza-os há mais de uma década e, em quantidade, são um sinal negativo. Trinta desses links valem menos do que uma menção numa lista curada de sites de Sudoku. **Ignora-os.**

A ordem abaixo é por retorno esperado.

---

## 1. GitHub — 10 minutos, permanente

O repositório já é público. Falta usá-lo.

- Define o **campo "Website"** do repo para `https://minimalist-games.com` (Settings → General, ou o ícone de engrenagem ao lado de "About" na página do repo).
- Adiciona **topics**: `sudoku`, `minesweeper`, `2048`, `puzzle-game`, `browser-game`, `vanilla-javascript`, `pwa`.
- O `README.md` do repo tem 1.102 bytes e não linka o site. Põe o link na primeira linha.

É nofollow, mas é permanente, rastreado constantemente, e o repo é uma prova pública de autoria — exactamente o argumento E-E-A-T que a página About agora faz. Um revisor do AdSense que procure "Arnaldo Lima minimalist games" encontra-o.

---

## 2. Show HN — o de maior potencial

**Regras confirmadas** (news.ycombinator.com/showhn.html): tens de ser o autor, tem de ser algo que as pessoas possam experimentar sem registo (o teu site cumpre na perfeição), o título tem de começar por `Show HN:`, e **não podes pedir upvotes a ninguém**. Publica quando estiveres disponível para responder a comentários durante algumas horas.

O erro a evitar: apresentar "três jogos clássicos" a uma audiência que já viu mil clones. O que é invulgar no teu projecto é o gerador — os diagramas dos guias são renderizados pelo motor solver, de posições verificadas. É esse o ângulo.

**Título** (80 caracteres máx.):

```
Show HN: Sudoku, Minesweeper and 2048 with no ads, accounts, or tracking
```

**Primeiro comentário** (publica-o tu próprio, imediatamente a seguir):

```
I got tired of puzzle sites that want an account before you can play, so I
built three of the classics as static pages: Sudoku with six difficulties,
Minesweeper, and 2048. Vanilla HTML/CSS/JS, no framework, no build step. It's
a PWA, so it works offline, and progress stays in your own browser.

The part I found more interesting to build is the guide diagrams. The blog
explains solving techniques — cross-hatching, hidden singles, pointing pairs
— and every diagram is rendered as SVG directly from the solver engine, from
a position the solver has verified. So a diagram can't drift out of sync with
the text or show an unsolvable board, which is a failure mode I kept hitting
when I tried drawing them by hand. The generator walks candidate grids to
find a position that demonstrates exactly one technique, then renders it.

The Sudoku generator itself guarantees a unique solution reachable by logic
alone, and rates difficulty by which human techniques a puzzle actually
requires rather than by counting clues.

Happy to go into the generator or the difficulty rating if anyone's curious.
```

**Quando publicar:** dias de semana, manhã na costa leste dos EUA (13:00–15:00 em Lisboa). Se afundar sem comentários, não voltes a publicar o mesmo link durante meses.

---

## 3. Reddit — 3 comunidades, 3 textos diferentes

**Verifica as regras de cada subreddit antes de publicar.** Não consegui aceder ao Reddit para as confirmar, e mudam com frequência. Procura sobretudo: dias fixos para auto-promoção, mínimos de karma ou idade de conta, e flair obrigatório. Publicar contra as regras dá remoção e, às vezes, ban — e queimas a comunidade que mais te interessava.

**Não publiques os três no mesmo dia.** Espaça-os por uma semana. E não copies o mesmo texto — o Reddit detecta e os moderadores também.

### r/WebGames

```
Title: Three classic puzzles, no ads, no accounts, works offline

I built minimalist versions of Sudoku, Minesweeper and 2048 because every
site I found wanted a login or buried the board under banners.

No account, no download, nothing to install. Sudoku has six difficulties with
notes and undo, Minesweeper is first-click-safe with a flag mode that works
on mobile, and 2048 saves your best score locally. It's a PWA so it works on
a plane.

Everything runs client-side and your progress never leaves your browser.

https://minimalist-games.com
```

### r/sudoku

Esta é a comunidade mais exigente das três e a que mais valor te dá se correr bem. Não entres a vender o jogo — entra pelos guias, que é onde tens algo genuíno.

```
Title: I render my technique diagrams straight from the solver engine

I've been writing up the standard solving techniques — cross-hatching, hidden
singles, naked and hidden pairs, pointing pairs, box/line reduction — and I
wanted the diagrams to be trustworthy.

So instead of drawing them, I have the solver generate them. The engine
searches for a position where exactly one technique applies, verifies it, and
renders the SVG from the actual candidate grid. Every board in the guides is
a real, solvable position, and the highlighted cells are the ones the solver
actually used.

The guides are here if they're useful to anyone:
https://minimalist-games.com/blog/sudoku-strategies

Genuinely interested in corrections. If any of my explanations are wrong or
use the wrong name for a technique, I'd rather know.
```

O convite à correcção não é retórica — nessa comunidade há gente que sabe mais do que qualquer guia online, e um erro apontado e corrigido gera mais boa vontade do que um post perfeito.

### r/Minesweeper

```
Title: Wrote up the 1-2-1 pattern and probability guessing, with a clean
board to practise on

Minesweeper looks like luck until you learn that most "guesses" aren't. I
wrote three short guides — the 1-2-1 pattern, counting and subtraction, and
what to do when you genuinely have to guess and want the best odds.

They're on a Minesweeper I rebuilt without the clutter: first-click safe,
three sizes, long-press to flag on mobile, no ads.

https://minimalist-games.com/blog/minesweeper-1-2-1-pattern
```

---

## 4. Listas curadas de sites de Sudoku — o link mais valioso e o mais lento

Existem páginas do tipo "Best Sudoku Websites 2026" que são actualizadas e rankeiam para pesquisas com intenção. Ser incluído numa vale mais do que vinte directórios, porque é um link editorial num contexto tematicamente idêntico ao teu.

Candidatas encontradas:

- [freepuzzles.net — Best Sudoku Websites 2026](https://www.freepuzzles.net/blog/best-sudoku-websites-online-free-puzzles-2026)
- [sudoku100.com — Top 10 Best Free Online Sudoku Websites 2026](https://www.sudoku100.com/best-sudoku-websites)
- [qoki.app — Best Free Online Sudoku Sites for Minimalist Play](https://qoki.app/en/blog/DLSZ/best-free-online-sudoku-sites-for-minimalist-play-and-daily-challenges) — esta menciona explicitamente "minimalist play", o encaixe é directo

Nota: a [Sudopedia](https://sudopedia.sudocue.net/index.php/Sudoku_Websites) tem uma lista de sites, mas a página não é editada desde Outubro de 2021 e não é abertamente editável. Baixa prioridade.

**Email de contacto** (adapta o primeiro parágrafo a cada site — um email visivelmente genérico é ignorado):

```
Subject: Suggestion for your best Sudoku sites list

Hi,

I came across your roundup of free Sudoku sites while looking at what's out
there, and I think mine might fit the brief — particularly the point you make
about clutter.

minimalist-games.com is a Sudoku (plus Minesweeper and 2048) site I build and
maintain on my own. Six difficulties, pencil notes, undo, hints. No account,
no download, no pop-ups, and it works offline as a PWA. Every puzzle is
generated with a guaranteed unique solution reachable by logic alone, and
difficulty is rated by which solving techniques a puzzle actually needs
rather than by counting clues.

There's also a set of technique guides where the diagrams are rendered
directly by the solver engine, so every board shown is a verified position:
https://minimalist-games.com/blog/sudoku-strategies

No expectations either way — I know these lists are curated. Thanks for
putting yours together.

Arnaldo Lima
Digital Codex Studio
```

Envia do `digitalcodexstudio@gmail.com` para ser coerente com o contacto do site. Espera uma taxa de resposta baixa; três emails destes bem dirigidos valem mais o teu tempo do que trinta submissões a directórios.

---

## 5. Listagens de jogos HTML5 — verificar antes

Encaixam no teu perfil, mas não consegui confirmar as condições de submissão de cada uma. Confirma antes de investir tempo — sobretudo **se a listagem linka para o teu domínio ou se aloja/embebe o jogo no domínio deles**. Se embebe, não te dá backlink nenhum e ainda te tira o tráfego.

- [FreeGameDirectory.com](https://www.freegamedirectory.com/) — posiciona-se como "browser games, no signup, no download", o que é literalmente a tua proposta. Melhor candidata do grupo.
- [iDev.Games](https://idev.games/upload-your-game) — aceita upload de jogos HTML5. Verifica se permite listar com link externo em vez de upload.
- **itch.io** — permite publicar um jogo web como link externo. Perfil com os três jogos e link para o site.

---

## Ordem e calendário sugeridos

| Quando | O quê | Esforço |
|---|---|---|
| Hoje, depois do deploy | GitHub: website, topics, README | 10 min |
| Esta semana | 3 emails às listas curadas | 45 min |
| Semana seguinte | r/sudoku (o de maior valor, faz este primeiro) | 20 min |
| +1 semana | Show HN, a meio da semana, de manhã | 30 min + estar disponível |
| +1 semana | r/WebGames | 15 min |
| +1 semana | r/Minesweeper | 15 min |
| Quando houver tempo | itch.io e FreeGameDirectory | 30 min |

Espaçar não é timidez: uma rajada de menções no mesmo dia parece uma campanha, e várias delas seriam removidas. Espalhado por seis semanas parece um site a ganhar tracção — que é exactamente o que queres que o revisor do AdSense veja em Novembro.

**Como medir:** Search Console → Links → Sites com ligações externas. Está em 0 hoje. A meta para resubmeter são 3–5 domínios distintos. O GSC demora semanas a reportar um link novo, por isso não te assustes com o silêncio das primeiras semanas.
