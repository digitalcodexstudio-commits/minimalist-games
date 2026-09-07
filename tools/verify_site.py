import re, json, pathlib, collections

ROOT = pathlib.Path(".")
SRC = pathlib.Path("src")
cfg = json.loads(pathlib.Path("firebase.json").read_text())["hosting"]
rewrites = {r["source"]: r["destination"] for r in cfg.get("rewrites", [])}
redirects = {r["source"]: r["destination"] for r in cfg.get("redirects", [])}

errors, warns = [], []

# ---- rotas: URL público -> ficheiro em disco
route_file = {}
for url, dest in rewrites.items():
    f = ROOT / dest.lstrip("/")
    if not f.exists():
        errors.append(f"rewrite {url} -> {dest} (ficheiro inexistente)")
    else:
        route_file[url] = f

# ---- toda a página em disco tem rota?
html_files = sorted(SRC.rglob("*.html"))
routed = {f.resolve() for f in route_file.values()}
for f in html_files:
    if f.resolve() not in routed:
        errors.append(f"página sem rewrite (inacessível em produção): {f}")

# ---- redirect que aponta para o vazio?
for s, d in redirects.items():
    target = d.split("#")[0]
    if target not in rewrites and target not in redirects and not target.startswith("/public/"):
        errors.append(f"redirect {s} -> {d} (destino sem rota)")

# ---- âncoras disponíveis por URL
anchors = {u: set(re.findall(r'\bid="([^"]+)"', f.read_text(encoding="utf-8")))
           for u, f in route_file.items()}

titles = collections.Counter()
STATIC_OK = ("/src/", "/public/", "/sitemap.xml", "/robots.txt", "/ads.txt",
             "/manifest.webmanifest", "/service-worker.js")

for url, f in sorted(route_file.items()):
    if f.suffix != ".html":
        continue  # rotas não-HTML: ads.txt, robots.txt, sitemap, manifest, service worker
    t = f.read_text(encoding="utf-8")

    m = re.search(r"<title>(.*?)</title>", t, re.S)
    if not m:
        errors.append(f"{url}: sem <title>")
    else:
        ti = m.group(1).strip()
        titles[ti] += 1
        if len(ti) > 60:
            errors.append(f"{url}: título com {len(ti)} caracteres (>60)")

    m = re.search(r'<meta name="description" content="(.*?)"', t, re.S)
    if not m:
        errors.append(f"{url}: sem meta description")
    else:
        d = m.group(1).strip()
        if len(d) > 165:
            errors.append(f"{url}: description com {len(d)} caracteres (>165)")
        elif len(d) < 110:
            warns.append(f"{url}: description curta ({len(d)} caracteres)")

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(block)
        except Exception as e:
            errors.append(f"{url}: JSON-LD inválido — {e}")

    for tag in ("article", "section", "footer", "main", "p", "ul", "ol", "li", "h2", "h3"):
        o = len(re.findall(r"<" + tag + r"[ >]", t))
        c = len(re.findall(r"</" + tag + r">", t))
        if o != c:
            errors.append(f"{url}: <{tag}> desequilibrada ({o} abre, {c} fecha)")

    for href in re.findall(r'href="(/[^"]*)"', t):
        path, _, frag = href.partition("#")
        path = path or url
        if path.startswith(STATIC_OK):
            continue
        if path in route_file:
            if frag and frag not in anchors.get(path, set()):
                errors.append(f"{url}: âncora inexistente -> {href}")
        elif path in redirects:
            warns.append(f"{url}: link interno aponta para um redirect -> {href}")
        else:
            errors.append(f"{url}: link interno quebrado -> {href}")

    if "buymeacoffee" in t:
        errors.append(f"{url}: resíduo de buymeacoffee")

for ti, n in titles.items():
    if n > 1:
        errors.append(f"título duplicado ({n}x): {ti}")

# ---- posts: autoria
posts = [u for u in route_file if u.startswith("/blog/") and u != "/blog"]
for u in posts:
    t = route_file[u].read_text(encoding="utf-8")
    if '"@type": "Person"' not in t and '"@type":"Person"' not in t:
        errors.append(f"{u}: sem autor Person no JSON-LD")
    if 'rel="author"' not in t:
        errors.append(f"{u}: sem byline visível")
    if "dateModified" not in t:
        errors.append(f"{u}: sem dateModified")

# ---- sitemap
sm = pathlib.Path("src/sitemap.xml").read_text()
sm_urls = {re.sub(r"^https://minimalist-games\.com", "", l) or "/" for l in re.findall(r"<loc>(.*?)</loc>", sm)}
for u in sorted(sm_urls - set(route_file)):
    errors.append(f"sitemap: {u} não tem rota")
for u in sorted(set(route_file) - sm_urls):
    if route_file[u].suffix == ".html":
        warns.append(f"página fora do sitemap: {u}")
for u in sorted(sm_urls & set(redirects)):
    errors.append(f"sitemap: {u} é um redirect")

print(f"rotas: {len(route_file)}  |  posts: {len(posts)}  |  sitemap: {len(sm_urls)}  |  redirects: {len(redirects)}")
print()
print("ERROS" if errors else "ERROS: nenhum")
for e in errors:
    print("  x", e)
print()
print("AVISOS" if warns else "AVISOS: nenhum")
for w in warns:
    print("  !", w)
