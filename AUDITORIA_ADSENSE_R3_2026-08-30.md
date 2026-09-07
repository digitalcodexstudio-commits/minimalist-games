# Auditoria AdSense — minimalist-games.com (3.ª rejeição)

Data: 30 de agosto de 2026
Base: varrimento completo de `src/` (32 páginas), verificação do site em produção, e dados do
Google Search Console (`sc-domain:minimalist-games.com`, conta digitalcodexstudio@gmail.com).

---

## 1. Veredicto

**Não há nada por corrigir no site.** O varrimento não encontra um único bloqueador estrutural:
todas as páginas de confiança existem, a política de privacidade cumpre os requisitos do AdSense,
o `ads.txt` está correcto, não há conteúdo duplicado nem páginas órfãs, e o Search Console não
regista qualquer acção manual.

A causa da 3.ª rejeição é **externa ao conteúdo**: o site tem tráfego orgânico residual
(≈1 clique/dia), **zero links externos**, e um domínio com ~5 meses. Para o filtro automático do
AdSense, esse perfil é indistinguível de um site feito só para monetizar — independentemente da
qualidade do que lá está escrito.

Consequência prática: **carregar em "Request review" agora devolve o mesmo veredicto**, porque o
site está literalmente inalterado desde a submissão de 17 de agosto (mesmas 32 páginas, mesmas
20.144 palavras).

---

## 2. Causa provável — a evidência

### 2.1 Tráfego (Search Console, últimos 90 dias)

| Métrica | Valor | Leitura |
|---|---|---|
| Cliques | 92 | ≈1/dia |
| Impressões | 8.150 | o conteúdo é indexado e mostrado |
| CTR médio | 1,1% | muito baixo |
| Posição média | 22 | página 2–3 dos resultados |

O padrão é claro: **o conteúdo range, mas em posições que ninguém clica.** Não é um problema de
indexação (32/32 páginas indexadas) nem de relevância — é de visibilidade e de CTR.

Piores casos (impressões altas, cliques quase nulos):

| Página | Impressões | Cliques | CTR |
|---|---|---|---|
| `/blog/minesweeper-counting` | 548 | 4 | 0,7% |
| `/blog/sudoku-strategies` | 257 | 3 | 1,2% |
| `/blog/2048-corner-strategy` | 255 | 4 | 1,6% |
| `/blog/2048-endgame` | 250 | 6 | 2,4% |
| query `free puzzle games` | 204 | 0 | 0% |
| `/` (homepage) | 990 | 49 | 4,9% ✅ |

A homepage converte bem (4,9%). Os posts não. Títulos e meta-descriptions são o factor directo.

### 2.2 Links externos: **0**

Relatório de Links do GSC: `External links — Total 0`. 253 links internos, nenhum externo.
Um domínio de 5 meses, sem uma única citação externa, é o sinal de autoridade mais fraco possível.
É provavelmente o factor com mais peso na decisão, e o único que o site sozinho não resolve.

### 2.3 Indexação: sem problemas reais

32 indexadas / 8 não indexadas. As 8 são todas artefactos do redirect `www`→apex
(3 "Page with redirect", 5 "Alternate page with proper canonical tag"). Benignas — já confirmado
em agosto. **Sem acções manuais** (Security & Manual Actions: "No issues detected").

### 2.4 Conteúdo: conforme, mas com um flanco fraco

32 páginas, 20.144 palavras visíveis, homepage com 510 palavras, diagramas SVG originais.
O flanco fraco não é o volume — é a **forma**:

- 12 dos 23 posts são fichas curtas de uma técnica (`sudoku-naked-pairs`, `sudoku-hidden-pairs`,
  `sudoku-pointing-pairs`, `sudoku-naked-triples`, `minesweeper-counting`…), com ~440–600 palavras
  brutas, o que dá ~300–450 palavras de corpo depois de descontar o boilerplate de nav/rodapé.
  Muitas páginas curtas e temáticamente vizinhas, num domínio novo, é exactamente a assinatura que
  os sistemas da Google associam a conteúdo produzido em escala.
- **Nenhum autor humano.** O schema declara `"author": {"@type": "Organization"}` em todos os posts.
  Não há byline, bio, nem `Person`. Para efeitos de E-E-A-T, o site é anónimo — e é precisamente
  o sinal que a Google diz procurar em conteúdo de "how-to".
- `/contact` tem 161 palavras (fina, mas aceitável para o tipo de página).

---

## 3. Varredura completa

| Área | Estado | Nota |
|---|---|---|
| Homepage | Conforme | 510 palavras, prosa editorial real |
| About | Conforme | Quem, porquê, como é feito, quem está por trás |
| Contact | Conforme | Email real, 161 palavras |
| Privacy | Conforme | Divulga AdSense, cookies, terceiros e opt-out |
| Terms | Conforme | Presente |
| `ads.txt` | Conforme | `pub-1735197115961712, DIRECT, f08c47fec0942fa0` |
| Idioma | Conforme | `lang="en"`, idioma suportado |
| Densidade de anúncios | Conforme | 0 ad units colocadas (só o loader) |
| Duplicação / scraping | Conforme | Conteúdo original, diagramas SVG próprios |
| Acções manuais | Conforme | Nenhuma |
| Indexação | Conforme | 32/32 páginas indexadas |
| Autoria / E-E-A-T | **A reforçar** | Sem autor humano, sem byline, schema `Organization` |
| Profundidade dos posts | **A reforçar** | 12 posts com ~300–450 palavras de corpo |
| CTR / posição | **A reforçar** | 1,1% @ posição 22 |
| Autoridade externa | **Em falta** | 0 links externos |
| Idade do domínio | **Em falta** | ~5 meses — só resolve com tempo |

---

## 4. Plano de acção

### P0 — Não fazer (evitar queimar um ciclo)

1. **Não carregar em "Request review" agora.** O site é byte a byte o mesmo de 17 de agosto.
2. **Não escrever mais 10 posts curtos.** Mais páginas do mesmo formato reforça o sinal errado.
3. **Não mexer na estrutura** (nav, trust pages, privacy) — está conforme.

### P1 — O que muda o resultado (2–4 semanas de trabalho)

1. **Reescrever títulos e meta-descriptions das 10 páginas com mais impressões.**
   O ganho é imediato e não depende de conteúdo novo: 548 impressões a 0,7% de CTR são ~30 cliques
   perdidos por trimestre numa só página. Alvo: passar de 1,1% para 3–4% de CTR médio.
   Prioridade: `minesweeper-counting`, `sudoku-strategies`, `2048-corner-strategy`, `2048-endgame`,
   e a query `free puzzle games` (204 impressões, 0 cliques).

2. **Dar um autor humano ao site.**
   - Byline visível em cada post ("por <nome>"), com data de publicação e de actualização.
   - Página `/about` com o nome real de quem escreve e uma bio curta (2–3 frases: quem é, porque
     percebe de puzzles).
   - Trocar `"author": {"@type": "Organization"}` por `Person`, e adicionar `datePublished` /
     `dateModified` no JSON-LD.
   Este é o único reforço de E-E-A-T que ainda está por fazer e é barato.

3. **Consolidar os posts finos em guias profundos.**
   Fundir as fichas de técnica de Sudoku (naked pairs, hidden pairs, pointing pairs, naked triples,
   box/line reduction, cross-hatching, hidden singles, last remaining cell) em 2–3 guias de
   1.500–2.000 palavras, com redirect 301 dos URLs antigos para as secções novas.
   Menos páginas, mais substância: inverte a assinatura de "conteúdo em escala".

4. **Conseguir os primeiros links externos.**
   O item de maior peso e o mais lento. Caminhos realistas para um site de puzzles:
   subreddits de Sudoku/Minesweeper, Hacker News ("Show HN"), diretórios de jogos web,
   comunidades de minimalismo/PWA, e um post técnico sobre como o gerador de Sudoku foi construído
   (já existe conteúdo base em `/blog/how-sudoku-puzzles-are-generated`).
   Meta mínima: 3–5 domínios distintos a apontar para o site.

### P2 — Timing da 4.ª submissão

Resubmeter quando **duas** destas condições estiverem verificadas:

- cliques orgânicos ≥ 3/dia (≈270 por 90 dias, contra os 92 actuais);
- pelo menos 3 domínios externos a linkar;
- domínio com ≥ 8 meses (≈novembro de 2026);
- as alterações de P1 deployadas há ≥ 3 semanas e confirmadas no recrawl.

Janela realista: **novembro de 2026**. Resubmeter antes disso, sem estas mudanças, é repetir o
mesmo resultado pela quarta vez.

### P3 — Se aprovado

Máx. 1–2 ad units por página, nunca sobre o tabuleiro de jogo, sem anúncios em `/contact` nem nas
páginas legais, e configurar o tratamento child-directed (COPPA).

---

## 5. Pendente de confirmação

A conta AdSense que detém `pub-1735197115961712` **não é** nenhuma das três sessões Google activas
no Chrome (arnaldo.a.lima, digitalcodexstudio, emergeimport) — todas devolvem "Access denied".
Confirmar em que conta está, para futuras verificações do painel.

---

## 6. Checklist pré-resubmissão (4.ª tentativa)

- [ ] Títulos/metas reescritos nas 10 páginas com mais impressões
- [ ] Byline + bio de autor humano em todos os posts
- [ ] Schema `Person` + `datePublished`/`dateModified`
- [ ] Posts de técnica de Sudoku consolidados em 2–3 guias longos, com 301s
- [ ] ≥ 3 domínios externos a linkar (confirmado no relatório de Links do GSC)
- [ ] Deploy feito e confirmado no recrawl (URL Inspection) há ≥ 3 semanas
- [ ] Cliques orgânicos ≥ 3/dia nos 28 dias anteriores
- [ ] Só então: "I confirm I have fixed the issues" → Request review
