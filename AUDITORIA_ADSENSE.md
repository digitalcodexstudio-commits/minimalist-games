# Auditoria AdSense — minimalist-games.com

**Data:** 8 de junho de 2026
**Motivo da rejeição:** *Low value content* (Google Publisher Network — "Your site does not yet meet the criteria of use")
**Âmbito:** varredura completa contra as Google Publisher Policies + diagnóstico do thin content
**Estado do site auditado:** 20 páginas (3 jogos, 14 artigos de blog, 2 legais, homepage)

---

## 1. Veredicto

O site **não tem violações graves de política**. A privacidade, os termos, o `ads.txt` e a qualidade editorial do blog estão acima da média para um site novo. A rejeição **não** é por conteúdo proibido — é a etiqueta genérica *Low value content* que o Google aplica a sites que, no momento da revisão, **parecem demasiado finos, demasiado pequenos ou pouco diferenciados** para justificar monetização.

Por outras palavras: o problema é de **massa e profundidade de conteúdo original**, não de incumprimento. É corrigível sem reescrever o site.

**Probabilidade de aprovação após as correções P0:** alta. O blog já demonstra valor editorial real; falta tornar isso evidente ao revisor logo na primeira página.

---

## 2. Causa provável da rejeição

O revisor do AdSense aterra tipicamente na **homepage** e em 2-3 páginas internas. O que ele vê hoje:

1. **Homepage quase vazia — 86 palavras.** É a página mais importante para a decisão e é essencialmente um menu: título, uma frase, três cartões de jogo, rodapé. Para um classificador automático isto lê-se como *doorway page* / página de navegação sem conteúdo próprio. **Este é, isolado, o sinal mais forte de "low value".**

2. **Site percecionado como uma ferramenta, não uma publicação.** Três jogos interativos + páginas de apoio curtas (~290 palavras cada). Jogos são *aplicações*; o AdSense quer ver **conteúdo de publisher** à volta deles. O blog resolve metade disto, mas não está em evidência.

3. **Ausência de páginas de confiança (E-E-A-T).** Não existe página **About/Sobre** nem **Contacto**. O e-mail está enterrado no fim da Privacy/Terms. O Google valoriza explicitamente saber *quem* está por trás do site — a sua ausência reforça a perceção de site descartável/afiliado.

4. **Site recente e pequeno.** Domínio e conteúdo de abril–junho 2026, ~20 páginas, tráfego orgânico presumivelmente baixo. Sites novos sem histórico recebem frequentemente esta rejeição como filtro por defeito.

O que **não** é a causa (já verificado e conforme): conteúdo ilegal, copiado, sexual, enganoso; idioma (inglês é suportado); `ads.txt`; política de privacidade; densidade de anúncios.

---

## 3. Varredura completa — Google Publisher Policies

Legenda: ✅ conforme · ⚠️ a reforçar · ❌ em falta/violação · ➖ não aplicável

### Content policies

| Política | Estado | Nota |
|---|---|---|
| Illegal content | ✅ | Jogos de puzzle, sem qualquer conteúdo ilegal. |
| Intellectual property abuse | ✅ | Sudoku/Minesweeper/2048 são mecânicas de domínio público; implementação própria em JS vanilla. Texto do blog é original. |
| Dangerous or derogatory | ✅ | Nenhum. |
| Animal cruelty | ➖ | N/A. |
| Misrepresentative content | ✅ | Sem alegações falsas; descrições dos jogos correspondem ao produto. |
| Enabling dishonest behavior | ✅ | Nenhum. |
| Sexually explicit | ✅ | Nenhum; site family-friendly. |
| Compensated sexual acts / Mail order brides | ➖ | N/A. |
| Adult themes in family content | ✅ | Conteúdo coerente com audiência geral. |
| Child sexual abuse | ✅ | Nenhum. |

### Behavioral policies

| Política | Estado | Nota |
|---|---|---|
| Dishonest declarations | ✅ | `ads.txt` correto: `google.com, pub-1735197115961712, DIRECT, f08c47fec0942fa0`. |
| Ads interfering | ✅ | Sem unidades `<ins adsbygoogle>` colocadas ainda (só o loader). Ao implementar, **não** sobrepor ao tabuleiro de jogo nem colar a controlos. |
| **Inventory value — low-value content** | ❌ | **A violação ativa.** Ver §2 e §4. Homepage fina + site percecionado como ferramenta. |
| Replicated content | ✅ | Conteúdo do blog é original e não duplicado entre páginas. |
| More ads than content | ⚠️ | Risco futuro: nas páginas de jogo o conteúdo textual é curto. Se colocares vários anúncios aí, o rácio anúncio/conteúdo dispara. Reforçar texto (P1) mitiga. |
| Unsupported languages | ✅ | Inglês, suportado. |

### Privacy-related policies

| Política | Estado | Nota |
|---|---|---|
| Personalized advertising | ✅ | Não há segmentação por categorias sensíveis. |
| **Privacy disclosures** | ✅ | Política exemplar: divulga cookies de terceiros, AdSense, opt-out (Ads Settings / aboutads.info), GA4, IP anonimizado. Cumpre a obrigação de disclosure. |
| Cookies on Google domains | ✅ | Não manipula cookies de domínios Google. |
| Identifying users | ✅ | Não envia PII; GA4 pseudonimizado. |
| Device/location data | ✅ | Apenas região aproximada; divulgado. |
| COPPA | ⚠️ | Declara "não recolhe de <13". Como o conteúdo (puzzles) atrai menores, **não ativar anúncios personalizados a público infantil**. Não é bloqueador da aprovação. |

### Requirements and other standards

| Política | Estado | Nota |
|---|---|---|
| Spam policies (Search) | ⚠️ | Sem cloaking/doorways intencionais, MAS a homepage de 86 palavras aproxima-se de "página com pouco ou nenhum conteúdo". Corrigir (P0). |
| Abusive experiences | ✅ | Sem redireccionamentos enganosos ou pop-ups abusivos. |
| Malware / unwanted software | ✅ | Estático, sem downloads. |
| Better Ads Standards | ✅ | Sem formatos proibidos planeados. Evitar interstitials e anúncios sticky pesados. |
| Authorized inventory (ads.txt) | ✅ | Presente e correto. |
| Sanctions compliance | ✅ | N/A (Portugal/EU). |

**Resumo:** 1 violação ativa (low-value content) + 3 pontos a reforçar (rácio anúncio/conteúdo, homepage fina vs. spam, COPPA na configuração de anúncios). Tudo o resto conforme.

---

## 4. Plano de ação priorizado

### P0 — Bloqueadores da aprovação (fazer antes de pedir review)

1. **Reescrever a homepage com conteúdo substancial (≥ 500 palavras de texto original).**
   Manter os três cartões de jogo, mas acrescentar, abaixo deles, secções editoriais: o que é o projeto, porquê "minimalist", uma introdução a cada jogo com ligação ao artigo de blog correspondente, e uma secção "porquê jogar puzzles". Conteúdo pronto em **§5.1**.

2. **Criar página About / Sobre.**
   Quem faz o site, missão (puzzles limpos, sem contas, sem clutter), como os jogos são construídos, o compromisso de conteúdo gratuito. Sinal de E-E-A-T direto. Conteúdo em **§5.2**.

3. **Criar página de Contacto.**
   Página dedicada com o e-mail `digitalcodexstudio@gmail.com` e o propósito de contacto. O AdSense procura ativamente uma forma de contacto. Conteúdo em **§5.3**.

4. **Adicionar About e Contact ao menu/rodapé de todas as páginas** e ao `sitemap.xml`. Sem links, as páginas não contam.

### P1 — Reforço de qualidade (alta recomendação antes do review)

5. **Expandir o texto de apoio nas 3 páginas de jogo** dos atuais ~290 para ~500-600 palavras: secção de estratégia rápida, FAQ curta (2-3 perguntas), ligação cruzada para os artigos de blog relevantes. Aumenta valor por página e baixa o futuro rácio anúncio/conteúdo.

6. **Destacar o blog na homepage** (já incluído em §5.1): mostrar que existe corpo editorial real é o argumento mais forte contra "low value".

7. **Ligações cruzadas internas** entre jogos ↔ artigos (ex.: a página do Sudoku já liga ao guia de estratégia — replicar em Minesweeper e 2048).

### P2 — Antes de ligar os anúncios (depois de aprovado)

8. **Colocar unidades de anúncio com critério:** máximo 1-2 por página, nunca sobre o tabuleiro, nunca coladas aos botões de jogo (política *Ads interfering*). Em páginas de jogo, colocar abaixo do conteúdo textual.

9. **Configurar tratamento child-directed** no AdSense/Search Console para não servir anúncios personalizados a tráfego potencialmente infantil (COPPA).

10. **Continuar a publicar:** 1-2 artigos novos por mês mantém o site "fresh" — fator que o próprio guia do AdSense menciona.

### Sequência recomendada

P0 (1-4) → deploy → esperar reindexação (3-7 dias, confirmar no Search Console) → **só então** "I confirm I have fixed the issues" → Request review. Não pedir review no mesmo dia do deploy: dá ao revisor uma versão ainda não rastreada.

---

## 5. Conteúdo pronto a publicar

Texto em **inglês (EN-US)** para coincidir com o site. Colar no HTML existente mantendo a estrutura/classes atuais.

### 5.1 Homepage — secções editoriais a acrescentar (abaixo dos cartões de jogo)

> **Free puzzle games, the way they should be**
>
> Minimalist Games is a small collection of classic logic puzzles you can play instantly in your browser — no account, no download, no install, no clutter. Just open a game and start thinking. Every game here is built to load in under a second, work offline, and stay out of your way. No pop-ups begging you to sign up, no tutorials you can't skip, no progress locked behind a login. The puzzle is the product.
>
> We focus on three games that have stood the test of time, and we try to do each one really well.
>
> **Sudoku Zen — pure logic, six difficulties**
> Sudoku is the most popular logic puzzle in the world for a reason: one simple rule, endless depth. Fill a 9×9 grid so every row, column, and box contains the digits 1–9. Our version gives you six difficulty levels from Easy to Extreme, pencil-mark notes, undo, and up to three hints per game — and every puzzle is guaranteed to have a single solution reachable by logic alone, never guesswork. New to it? Start with our [beginner's guide](/blog/how-to-solve-sudoku). Ready for hard boards? Read the [strategy guide with diagrams](/blog/sudoku-strategies). [Play Sudoku →](/games/sudoku)
>
> **Minesweeper — counting under pressure**
> The Windows classic, rebuilt clean. Clear the board without detonating a mine, using the numbers as clues to deduce where the mines hide. Three board sizes, from a quick coffee-break grid to a proper challenge. It looks like luck, but the best players win on logic — learn how in our [Minesweeper strategy guide](/blog/minesweeper-strategy). [Play Minesweeper →](/games/minesweeper)
>
> **2048 — slide, merge, chase the tile**
> Deceptively simple: slide numbered tiles, merge matching pairs, and try to build the 2048 tile before the board fills up. One of the most addictive puzzle games ever made. There's real strategy underneath the swipes — the corner method, why you should never slide up — and we break it down in [2048 tips and tricks](/blog/2048-tips). [Play 2048 →](/games/2048)
>
> **Why puzzles?**
> A few minutes of Sudoku or Minesweeper is a genuinely good break: it's focused, low-stakes, and asks something of your attention without overwhelming it. No timers forcing panic, no ads interrupting your train of thought mid-game, no dark patterns. That's the whole idea behind "minimalist" — fewer features, done with more care.
>
> **From the blog**
> We write about how to actually get better at these games — not filler, but the techniques that move the needle. Recent guides: [Sudoku Strategies Explained with Diagrams](/blog/sudoku-strategies), [How to Solve Sudoku for Beginners](/blog/how-to-solve-sudoku), [Best Minesweeper Strategies](/blog/minesweeper-strategy), [2048 Tips and Tricks](/blog/2048-tips), and [Why Minimalist Game Design Wins](/blog/minimalist-game-design). [Visit the blog →](/blog)

*(≈ 470 palavras de texto novo; com o conteúdo existente a homepage passa folgadamente os 500.)*

### 5.2 Página About / Sobre — `/about` (novo ficheiro `src/about/index.html`)

> **About Minimalist Games**
>
> Minimalist Games is an independent project with one goal: make the classic puzzle games genuinely pleasant to play on the web again. No accounts. No downloads. No clutter. You open a page and the game is already there.
>
> **Why we built it**
> Most "free game" sites bury a thirty-second game under a minute of pop-ups, cookie walls, autoplay video, and forced sign-ups. We wanted the opposite: games that load instantly, run offline, remember your progress locally, and never get in your way. The design philosophy is in the name — strip everything that isn't the puzzle, and polish what's left.
>
> **What we make**
> We currently offer three games, each rebuilt from scratch in plain HTML, CSS, and JavaScript — no frameworks, no tracking-heavy third-party widgets:
> - **Sudoku Zen** — six difficulty levels, notes, hints, single-solution puzzles.
> - **Minesweeper** — three board sizes, the clean version of the Windows classic.
> - **2048** — the addictive sliding-tile game, with smooth controls.
>
> Alongside the games we publish a small blog of genuinely useful strategy guides — how to read a Sudoku board, how to think in probabilities in Minesweeper, the corner method in 2048 — written for players who want to actually improve, not just rank for keywords.
>
> **How it's built**
> The whole site is static and hosted on Firebase Hosting. It works offline as a Progressive Web App, loads in under a second, and stores your game progress only in your own browser — nothing about your play is sent to us. We use Google Analytics (IP-anonymized) only to understand which games people enjoy, and Google AdSense to keep the site completely free. Full details are in our [Privacy Policy](/privacy).
>
> **Who's behind it**
> Minimalist Games is made by Digital Codex Studio, an independent developer based in Portugal. It's a labor of love, maintained and updated regularly with new puzzles and guides. Got feedback, found a bug, or want to suggest a game? We'd like to hear from you — see the [Contact](/contact) page.

### 5.3 Página de Contacto — `/contact` (novo ficheiro `src/contact/index.html`)

> **Contact**
>
> Minimalist Games is run by an independent developer, and real people read every message. We'd genuinely like to hear from you if you:
> - found a bug or a puzzle that doesn't behave correctly,
> - have a feature idea or a game you'd like us to add,
> - want to report an ad that violates [Google's policies](https://support.google.com/adsense/answer/9335564),
> - or have a privacy request regarding your data.
>
> **Email:** digitalcodexstudio@gmail.com
>
> We aim to reply within a few business days. For privacy-related requests, please see our [Privacy Policy](/privacy) for what data we do (and don't) hold. For the rules of using the site, see our [Terms of Service](/terms).
>
> *Minimalist Games — Digital Codex Studio, Portugal.*

### 5.4 Nota de implementação

- Reaproveitar o `<head>`, CSS e o cabeçalho/rodapé das páginas legais existentes (`src/legal/privacy.html`) como template para About e Contact — garante consistência visual e metadados.
- Acrescentar **About** e **Contact** ao rodapé de **todas** as páginas (atualmente só `Blog · Privacy · Terms`) e ao `src/sitemap.xml`.
- Adicionar JSON-LD `AboutPage` / `ContactPage` (opcional, reforça SEO).
- Garantir que os novos URLs (`/about`, `/contact`) têm `rewrite` no `firebase.json` tal como os jogos.

---

## 6. Checklist pré-resubmissão

- [ ] Homepage reescrita com ≥ 500 palavras de conteúdo original (§5.1)
- [ ] Página `/about` criada e ligada no rodapé de todas as páginas (§5.2)
- [ ] Página `/contact` criada e ligada no rodapé de todas as páginas (§5.3)
- [ ] Texto de apoio das 3 páginas de jogo expandido para ~500+ palavras (P1)
- [ ] Ligações cruzadas jogo ↔ blog em todas as páginas de jogo
- [ ] `sitemap.xml` atualizado com `/about` e `/contact`
- [ ] `firebase.json` com rewrites para os novos URLs
- [ ] Deploy feito (`npm run deploy`)
- [ ] Páginas novas rastreadas/indexadas (confirmar no Search Console, 3-7 dias)
- [ ] Só então: marcar "I confirm I have fixed the issues" → **Request review**

---

## 7. Oportunidade de automação

Este tipo de auditoria (rastrear estrutura → contar palavras por página → cruzar com checklist de políticas → gerar plano) é **bom candidato a Claude Skill reutilizável** — aplicável a qualquer site teu que submetas ao AdSense ou ao Search Console. Se vais lançar mais sites neste modelo (parece ser o caso, dado o `Digital Codex Studio`), vale a pena formalizá-la. Diz e eu monto a skill.

---

*Fontes: [Google Publisher Policies](https://support.google.com/adsense/answer/9335564), [AdSense content and user experience](https://support.google.com/adsense/answer/10015918), [Webmaster guidelines — thin content / manual actions](https://support.google.com/webmasters/answer/9044175). Auditoria baseada nos ficheiros em `src/` (estado de 8 jun 2026).*
