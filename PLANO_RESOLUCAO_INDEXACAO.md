# Plano de Resolução: Problema de Indexação no Google Search Console

**Projeto:** minimalist-games.com  
**Data:** 1 de maio de 2026  
**Objetivo:** Resolver o aviso de indexação: "Alternate page with proper canonical tag" (2 páginas afetadas)

---

## 📋 Resumo Executivo

Este plano contém todos os passos para resolver o problema de indexação através do Claude Code. Serão feitas:

1. ✅ Modificações no `firebase.json` (adicionar redirecionamentos 301)
2. ✅ Validação das alterações
3. ✅ Deploy para Firebase Hosting (produção)
4. ✅ Resubmissão no Google Search Console

**Duração estimada:** 30-45 minutos  
**Risco:** Muito baixo (as alterações são reversíveis)

---

## 🎯 Passo 1: Preparação

### 1.1 Verificar o ambiente

Confirme que tem acesso ao projeto:

```bash
cd /Users/alima/Documents/Claude/Projects/minimalist-games
ls -la firebase.json
```

**Resultado esperado:** Deve ver o ficheiro `firebase.json` listado.

### 1.2 Verificar credenciais Firebase

```bash
firebase list
```

**Resultado esperado:** Deve ver `minimalist-games` na lista de projetos.

Se não estiver autenticado:

```bash
firebase login
```

---

## 🔧 Passo 2: Modificar o firebase.json

### 2.1 Análise do ficheiro atual

O ficheiro atual tem a seguinte estrutura:

```json
{
  "hosting": {
    "public": ".",
    "cleanUrls": true,
    "trailingSlash": false,
    "rewrites": [ ... ],
    "headers": [ ... ]
  }
}
```

### 2.2 Adicionar regras de redirecionamento

Na raiz do objeto `"hosting"` (após `"trailingSlash": false`), adicione:

```json
"redirects": [
  {
    "source": "/**",
    "destination": "/:1",
    "type": 301
  }
]
```

**O que isto faz:** Redireciona qualquer URL com slash final para a versão sem slash (ex: `/games/sudoku/` → `/games/sudoku`).

### 2.3 Resultado esperado

O seu `firebase.json` deve ter esta estrutura:

```json
{
  "hosting": {
    "public": ".",
    "cleanUrls": true,
    "trailingSlash": false,
    "redirects": [
      {
        "source": "/**",
        "destination": "/:1",
        "type": 301
      }
    ],
    "rewrites": [ ... ],
    "headers": [ ... ]
  }
}
```

---

## ✅ Passo 3: Validação das Alterações

### 3.1 Validar sintaxe JSON

```bash
# Verifique se o JSON é válido
node -e "console.log(JSON.stringify(require('./firebase.json'), null, 2))"
```

**Resultado esperado:** Deve imprimir o JSON formatado sem erros.

### 3.2 Teste local (opcional)

Para testar as alterações localmente antes de fazer deploy:

```bash
firebase serve
```

Depois visite `http://localhost:5000/games/sudoku/` (com slash final) e verifique se redireciona para `http://localhost:5000/games/sudoku` (sem slash).

**Pressione `Ctrl+C` para parar o servidor local.**

---

## 🚀 Passo 4: Deploy para Produção

### 4.1 Confirmar alterações no git (recomendado)

```bash
git status
```

Deve mostrar `firebase.json` como modificado.

Se quiser fazer commit:

```bash
git add firebase.json
git commit -m "fix: adicionar redirecionamentos 301 para resolver problema de indexação"
```

### 4.2 Fazer deploy no Firebase Hosting

```bash
firebase deploy --only hosting
```

**Aguarde a conclusão:** O processo leva tipicamente 1-2 minutos.

**Resultado esperado:**

```
✓  Deploy complete!
✓  Hosting URL: https://minimalist-games.com
```

### 4.3 Verificar se o deploy foi bem-sucedido

Teste as URLs diretamente:

```bash
# Teste com slash final (deve redirecionar com 301)
curl -I https://minimalist-games.com/games/sudoku/

# Teste sem slash (deve servir a página)
curl -I https://minimalist-games.com/games/sudoku
```

**Resultado esperado para URL com slash:**

```
HTTP/2 301
location: https://minimalist-games.com/games/sudoku
```

**Resultado esperado para URL sem slash:**

```
HTTP/2 200
content-type: text/html; charset=UTF-8
```

---

## 📊 Passo 5: Resubmissão no Google Search Console

### 5.1 Aceder ao Search Console

1. Abra [Google Search Console](https://search.google.com/search-console)
2. Selecione a propriedade `minimalist-games.com`
3. Navegue até **Indexação > Páginas**

### 5.2 Identificar as páginas afetadas

No relatório de indexação, pode ver quais são as 2 páginas com o aviso "Alternate page with proper canonical tag".

Comum serem:
- `/games/sudoku`
- `/games/minesweeper`
- `/games/2048`
- `/blog` ou artigos específicos

### 5.3 Solicitar reindexação

Para cada página afetada:

1. Clique em **Inspeção de URL** (URL Inspection)
2. Digite a URL (ex: `https://minimalist-games.com/games/sudoku`)
3. Clique em **Solicitar indexação** (Request indexing)
4. Aguarde o resultado

**Faça isto para as 2 páginas identificadas no Search Console.**

### 5.4 Monitorizar o progresso

Após solicitar indexação:

1. Volte a **Indexação > Páginas**
2. Aguarde 2-3 dias para o Google re-rastrear
3. Verifique se o número de páginas com o aviso diminuiu

---

## 🔍 Passo 6: Verificação e Validação

### 6.1 Checklist de conclusão

- [ ] Ficheiro `firebase.json` modificado com sucesso
- [ ] Deploy realizado sem erros (`firebase deploy --only hosting`)
- [ ] URLs com slash final redirecionam com código 301
- [ ] URLs sem slash servem a página normalmente (código 200)
- [ ] Reindexação solicitada no Search Console para as 2 páginas
- [ ] Aguardou pelo menos 2-3 dias

### 6.2 Sinais de sucesso esperados

Após 2-3 dias:

- ✅ Número de páginas não indexadas diminui
- ✅ Aviso "Alternate page with proper canonical tag" desaparece
- ✅ Todas as páginas aparecem como "Indexada e servida da rede" no Search Console

### 6.3 Se o problema persistir

Se após 5-7 dias o aviso continuar:

1. **Verificar se há outras fontes de URLs alternativas:**
   - Parâmetros UTM em links (ex: `?utm_source=...`)
   - Protocolos mistos (HTTP vs HTTPS)
   - Versões WWW vs non-WWW

2. **Adicionar ao Search Console:**
   - Vá a **Configuração > Definições do site**
   - Selecione a versão preferida (https://minimalist-games.com, sem www)

3. **Contactar Suporte Google:**
   - Se o problema persistir após as medidas acima, contacte o suporte do Google Search Console

---

## 📝 Ficheiro de Referência: firebase.json Completo

Aqui está como o seu `firebase.json` deve ficar após as alterações:

```json
{
  "hosting": {
    "public": ".",
    "cleanUrls": true,
    "trailingSlash": false,
    "redirects": [
      {
        "source": "/**",
        "destination": "/:1",
        "type": 301
      }
    ],
    "ignore": [
      "firebase.json",
      ".firebaserc",
      "package.json",
      "package-lock.json",
      "README.md",
      ".git/**",
      ".github/**",
      ".gitignore",
      ".firebase/**",
      "node_modules/**",
      ".idea/**",
      ".vscode/**"
    ],
    "rewrites": [
      {
        "source": "/",
        "destination": "/src/index.html"
      },
      {
        "source": "/games/sudoku",
        "destination": "/src/games/sudoku/index.html"
      },
      {
        "source": "/games/minesweeper",
        "destination": "/src/games/minesweeper/index.html"
      },
      {
        "source": "/games/2048",
        "destination": "/src/games/2048/index.html"
      },
      {
        "source": "/privacy",
        "destination": "/src/legal/privacy.html"
      },
      {
        "source": "/terms",
        "destination": "/src/legal/terms.html"
      },
      {
        "source": "/blog",
        "destination": "/src/blog/index.html"
      },
      {
        "source": "/blog/how-to-solve-sudoku",
        "destination": "/src/blog/how-to-solve-sudoku/index.html"
      },
      {
        "source": "/blog/minesweeper-strategy",
        "destination": "/src/blog/minesweeper-strategy/index.html"
      },
      {
        "source": "/blog/2048-tips",
        "destination": "/src/blog/2048-tips/index.html"
      },
      {
        "source": "/blog/free-puzzle-games",
        "destination": "/src/blog/free-puzzle-games/index.html"
      },
      {
        "source": "/blog/minimalist-game-design",
        "destination": "/src/blog/minimalist-game-design/index.html"
      },
      {
        "source": "/sitemap.xml",
        "destination": "/src/sitemap.xml"
      },
      {
        "source": "/robots.txt",
        "destination": "/src/robots.txt"
      },
      {
        "source": "/ads.txt",
        "destination": "/src/ads.txt"
      },
      {
        "source": "/manifest.webmanifest",
        "destination": "/src/manifest.webmanifest"
      },
      {
        "source": "/service-worker.js",
        "destination": "/src/service-worker.js"
      }
    ],
    "headers": [
      {
        "source": "**/*.@(css|js)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "public, max-age=2592000, must-revalidate"
          }
        ]
      },
      {
        "source": "**/*.@(svg|jpg|jpeg|png|woff2)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "public, max-age=2592000, must-revalidate"
          }
        ]
      },
      {
        "source": "/",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      },
      {
        "source": "/games/**",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      },
      {
        "source": "/privacy",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      },
      {
        "source": "/terms",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      },
      {
        "source": "/blog{,/**}",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      },
      {
        "source": "**/*.html",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      },
      {
        "source": "/service-worker.js",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      },
      {
        "source": "/manifest.webmanifest",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "public, max-age=3600"
          },
          {
            "key": "Content-Type",
            "value": "application/manifest+json"
          }
        ]
      }
    ]
  }
}
```

---

## ⏱️ Cronograma Esperado

| Passo | Duração | Quando |
|-------|---------|--------|
| Preparação | 5 min | Agora |
| Modificar firebase.json | 10 min | Após preparação |
| Validação local | 10 min | Após modificação |
| Deploy | 5 min | Após validação |
| Resubmissão Search Console | 10 min | Após deploy bem-sucedido |
| **Monitorização** | **2-3 dias** | **Após resubmissão** |
| **Verificação final** | **5 min** | **Após 3 dias** |

---

## 🆘 Troubleshooting

### Problema: JSON inválido após edição

**Solução:** Verifique a sintaxe JSON usando uma ferramenta online ou o comando `node -e` listado acima.

### Problema: Deploy falha

**Solução:** Certifique-se de que:
- Está autenticado: `firebase login`
- Está no diretório correto: `cd /Users/alima/Documents/Claude/Projects/minimalist-games`
- Tem credenciais para o projeto: `firebase list`

### Problema: URLs ainda redirecionam com 302 em vez de 301

**Solução:** Limpe a cache do navegador e tente novamente em alguns minutos.

### Problema: Search Console ainda mostra o aviso após 5 dias

**Solução:** Contacte o suporte do Google Search Console com detalhes técnicos.

---

## ✨ Notas Importantes

1. **As alterações são reversíveis:** Se algo der errado, pode reverter o `firebase.json` para a versão anterior.
2. **Sem risco de perda de dados:** Estas alterações apenas afetam redirecionamentos, não alteram conteúdo.
3. **Compatibilidade:** Os redirecionamentos 301 são a forma padrão recomendada pelo Google para este tipo de problema.
4. **Monitorização:** Após o deploy, o Google pode levar até 7 dias para reprocessar todas as páginas.

---

## 📞 Próximas Etapas

Quando estiver pronto para executar este plano:

1. Abra o Claude Code
2. Siga os passos 1-6 acima em ordem
3. Depois de completar, aguarde 2-3 dias antes de verificar o Search Console

**Sucesso!** 🎉

