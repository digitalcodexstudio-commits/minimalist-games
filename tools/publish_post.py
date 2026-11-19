"""Publish a post that is waiting in drafts/.

    python3 tools/publish_post.py <slug>            # publish
    python3 tools/publish_post.py <slug> --check    # dry run: show what would change

Each draft lives in drafts/<slug>/ with:
  index.html   the finished post (datePublished already set)
  meta.json    {"date": "YYYY-MM-DD", "after": "<slug of the blog-index entry to insert after>",
                "list_title": "...", "list_blurb": "..."}
  also/        optional: files to copy over the repo at publish time, at their repo paths
               (e.g. also/src/blog/minesweeper-openings/index.html for a related post updated
               to link to the new one)

Publishing moves the post into src/blog/, adds its rewrite to firebase.json, its entry to the
blog index and to the sitemap, copies anything in also/, and runs tools/verify_site.py.
It never commits or pushes: the git commands to finish are printed at the end.
"""
import json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def fail(msg):
    print(f"x {msg}")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        fail(__doc__)
    slug, dry = sys.argv[1], "--check" in sys.argv
    draft = ROOT / "drafts" / slug
    if not (draft / "index.html").exists():
        fail(f"drafts/{slug}/index.html not found")
    meta = json.loads((draft / "meta.json").read_text())
    dest = ROOT / "src" / "blog" / slug / "index.html"
    if dest.exists():
        fail(f"src/blog/{slug} already exists — already published?")

    url = f"/blog/{slug}"
    fb_path = ROOT / "firebase.json"
    fb = fb_path.read_text()
    if f'"source": "{url}"' in fb:
        fail(f"firebase.json already has a rewrite for {url}")
    # insert the rewrite after the last one, keeping the file's formatting
    m = list(re.finditer(r'\n      \}\n    \],\n    "headers"', fb))
    if len(m) != 1:
        fail("could not find the end of the rewrites list in firebase.json")
    i = m[0].start() + len("\n      }")
    entry = (',\n      {\n        "source": "%s",\n        "destination": "/src/blog/%s/index.html"\n      }'
             % (url, slug))
    fb_new = fb[:i] + entry + fb[i:]
    json.loads(fb_new)  # still valid JSON

    idx_path = ROOT / "src" / "blog" / "index.html"
    idx = idx_path.read_text()
    anchor = f'href="/blog/{meta["after"]}"'
    a = idx.find(anchor)
    if a < 0:
        fail(f'blog index has no entry for {meta["after"]}')
    li_end = idx.find("</li>", a) + len("</li>")
    item = ('\n      <li>\n        <a class="post-link" href="%s">\n          <h2>%s</h2>\n'
            '          <p>%s</p>\n        </a>\n      </li>' % (url, meta["list_title"], meta["list_blurb"]))
    idx_new = idx[:li_end] + item + idx[li_end:]

    sm_path = ROOT / "src" / "sitemap.xml"
    sm = sm_path.read_text()
    sm_item = ('  <url>\n    <loc>https://minimalist-games.com%s</loc>\n    <lastmod>%s</lastmod>\n'
               '    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n' % (url, meta["date"]))
    sm_new = sm.replace("</urlset>", sm_item + "</urlset>")

    also = draft / "also"
    extra = sorted(p for p in also.rglob("*") if p.is_file()) if also.exists() else []

    print(f"Publishing {url} (dated {meta['date']})")
    print(f"  + src/blog/{slug}/index.html")
    print("  ~ firebase.json (rewrite)")
    print(f"  ~ src/blog/index.html (after {meta['after']})")
    print("  ~ src/sitemap.xml")
    for p in extra:
        print(f"  ~ {p.relative_to(also)}")
    if dry:
        print("\n(dry run — nothing changed)")
        return

    dest.parent.mkdir(parents=True)
    shutil.copy2(draft / "index.html", dest)
    fb_path.write_text(fb_new)
    idx_path.write_text(idx_new)
    sm_path.write_text(sm_new)
    for p in extra:
        target = ROOT / p.relative_to(also)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
    shutil.rmtree(draft)

    print("\nRunning tools/verify_site.py ...\n")
    out = subprocess.run([sys.executable, "tools/verify_site.py"], cwd=ROOT, capture_output=True, text=True).stdout
    print(out)
    if "ERROS: nenhum" not in out:
        fail("verify_site.py reported errors — fix them before committing")

    print("All good. To put it live:\n")
    print(f'  git add -A && git commit -m "content: publish {slug}" && git push\n')
    print(f"Then in Search Console: URL inspection -> https://minimalist-games.com{url} -> Request indexing.")


if __name__ == "__main__":
    main()
