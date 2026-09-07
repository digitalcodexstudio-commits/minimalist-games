# Auditoria AdSense (delta) — minimalist-games.com

**Data:** 2 de julho de 2026
**Contexto:** 2ª rejeição *Low value content*, após as correções de 8 de junho (homepage 510 palavras, About, Contact, 6 posts ilustrados). Revisão pedida 1–2 dias após o deploy, com indexação confirmada no Search Console.
**Âmbito:** delta face à auditoria de 8 de junho — só o que mudou e o que ainda falta.

---

## 1. Veredicto

O site continua **sem violações de política**. A 2ª rejeição não invalida o trabalho de junho — reduziu drasticamente os sinais negativos, mas deixou três resíduos que, combinados num domínio com ~10 semanas de vida, mantêm o classificador do lado do "não": **páginas de jogo finas**, **blog index só-navegação com 8 posts órfãos**, e **resubmissão demasiado rápida**. Os dois primeiros ficaram corrigidos hoje. O terceiro corrige-se com paciência.

Probabilidade após este ciclo: boa, mas o fator que já não controlas é idade/massa do domínio — se houver 3ª rejeição, a resposta é publicar mais 2–4 guias e esperar mais, não mexer na estrutura.

## 2. Porque falhou a 2ª revisão (diagnóstico)

O percurso típico do revisor é homepage → clique num jogo. Em junho a homepage ficou resolvida (510 palavras), mas o clique seguinte aterrava numa **aplicação com ~250 palavras de apoio e o loader do AdSense presente** — exatamente o perfil "inventory value: ads em ecrãs sem conteúdo de publisher" das Publisher Policies. As 3 páginas de jogo eram, no momento da revisão, as páginas mais visitadas e as mais fracas do site.

Sinais secundários: o blog index (289 palavras) era uma lista de links sem prosa editorial — lê-se como ecrã de navegação — e **listava só 12 dos 20 posts** (os 8 guias de técnicas de Sudoku estavam fora do índice, invisíveis para um revisor que navegue pelo site). Por fim, a revisão foi pedida 1–2 dias após o deploy: mesmo com indexação confirmada via URL Inspection, o snapshot usado pela revisão AdSense pode ser anterior — o intervalo recomendado é 2–3 semanas num site que já foi rejeitado duas vezes.

Nota menor (não bloqueante): `www.minimalist-games.com` serve conteúdo com HTTP 200 em vez de redirecionar 301 para o apex. O canonical mitiga, mas ver P1.

## 3. O que foi alterado hoje (já no repo, falta deploy)

| Página | Antes | Depois | Conteúdo novo |
|---|---|---|---|
| `/games/sudoku` | 252 palavras | **733** | O que distingue o Sudoku Zen, significado dos 6 níveis (com links para os guias de técnicas), história breve, FAQ (4 perguntas) |
| `/games/minesweeper` | 246 | **730** | "Parece sorte, não é", guia de escolha de tabuleiro, história breve, FAQ (4) |
| `/games/2048` | 256 | **778** | Porque é mais difícil do que parece, 3 hábitos que corrigem a maioria dos jogos, história (Cirulli, 2014), FAQ (4 — fiel ao jogo real: undo ilimitado, "Keep going") |
| `/blog` | 289 | **621** | Intro editorial + 4 secções por tema com intro cada + **8 posts de Sudoku adicionados ao índice** (estavam órfãos) |
| `css/blog.css` | — | — | Estilos para `.blog-section-title`, `.blog-section-intro` e intro do índice |

Verificação feita: HTML balanceado nas 4 páginas alteradas; todos os links internos novos apontam para posts existentes; FAQ do 2048 corrigida à funcionalidade real (undo ilimitado, continuar após 2048); scan pós-edição: **0 páginas finas relevantes** (só `/contact` com 161 palavras, normal e aceitável para página de contacto), total do site 15.901 → **17.720 palavras**.

## 4. Varredura de políticas (estado atual)

| Área | Estado | Nota |
|---|---|---|
| Conteúdo proibido / IP / misrepresentation | conforme | Jogos de domínio público, implementação e texto próprios; páginas entregam o que os títulos prometem |
| Inventory value (low value content) | **conforme após deploy** | Era o ponto fraco; homepage 510 + jogos 730–778 + blog index editorial |
| Trust pages (E-E-A-T) | conforme | About, Contact, Privacy, Terms em todos os footers |
| Privacy disclosures | conforme | Cookies, terceiros, opt-out, AdSense — tudo presente |
| ads.txt | conforme | `pub-1735197115961712` DIRECT |
| Rácio anúncios/conteúdo | conforme | Loader presente, 0 ad units — correto pré-aprovação |
| Idioma | conforme | `lang="en"` consistente |
| Idade/massa do domínio | **a reforçar** | ~10 semanas, 29 páginas — o único fator que só o tempo resolve |
| www → apex | a reforçar | www serve 200; recomendado 301 (P1) |

## 5. Plano de ação

**P0 — antes de resubmeter**

1. Deploy: `npm run deploy` (equivale a `firebase deploy --only hosting`, definido no `package.json`).
2. No Search Console, URL Inspection → Request indexing para as 4 páginas alteradas (`/games/sudoku`, `/games/minesweeper`, `/games/2048`, `/blog`).
3. **Esperar 2–3 semanas** — não 1–2 dias. Confirmar no relatório de indexação que as versões novas foram rastreadas (a data de rastreio na URL Inspection deve ser posterior ao deploy). Num site com duas rejeições, o custo de esperar é baixo e o custo de um 3º ciclo falhado é alto (cada ciclo consome ~2–4 semanas).
4. Só então: "I confirm I have fixed the issues" → Request review.

**P1 — durante a espera (aumenta a probabilidade, aproveita o tempo morto)**

5. Publicar 2–3 posts novos durante as 2–3 semanas de espera (sinal de site vivo + massa). Candidatos rápidos com o padrão já estabelecido: "How Sudoku puzzles are generated" (E-E-A-T técnico forte), "Minesweeper openings: where to click first", "2048: when to break the snake".
6. Configurar redirect 301 `www` → apex no Firebase Hosting (domínio www como redirect, não como segundo host a servir conteúdo).
7. Adicionar data de publicação e byline visíveis nos posts (sinal de frescura e autoria).

**P2 — pós-aprovação**

8. Máx. 1–2 ad units por página; nunca sobre o tabuleiro; nada de anúncios em `/contact` ou páginas legais.
9. Tratamento child-directed (COPPA) na configuração de anúncios — sites de puzzles atraem menores.

## 6. Checklist pré-resubmissão

- [x] Homepage ≥ 500 palavras
- [x] Páginas de jogo ≥ 700 palavras cada
- [x] Blog index editorial + 20/20 posts indexados no índice
- [x] Trust pages completas e ligadas
- [x] ads.txt, privacy disclosures, lang
- [ ] Deploy
- [ ] Request indexing das 4 páginas alteradas
- [ ] 2–3 semanas de espera + rastreio confirmado (data de crawl > data de deploy)
- [ ] (P1) 2–3 posts novos publicados
- [ ] Request review

---

*Nota: isto descreve os sinais a que um revisor reage e as probabilidades associadas — a decisão final é do Google e nenhuma correção garante aprovação.*
