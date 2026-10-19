#!/usr/bin/env python3
"""Downloads company marks into src/assets/logos/ for the career timeline.

Run it once locally (python3 fetch_logos.py) and commit the result, or let the
Pages workflow run it at build time. Existing files are kept unless --force is
passed, so a hand-picked logo dropped into src/assets/logos/<slug>.svg|png wins.

Sources, in order: Google's favicon service (256 px), then DuckDuckGo's. Both
return the site's icon, which is usually the brand mark. Pass --force to refetch.
"""
import os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "src", "assets", "logos")

# slug -> candidate domains, tried in order (the slug must match build.py)
COMPANIES = {
    "cgm": ["cgm.com"],
    "avira": ["avira.com"],
    "gen": ["gendigital.com"],
    "inhive": ["inhive.global", "de.inhive.group", "inhive.group"],
    "verivox": ["verivox.de"],
    "nix": ["n-ix.com"],
    "edvantis": ["edvantis.com"],
    "ukeess": ["ukeess.com"],
    "leonorm": ["leonorm.com.ua", "leonorm.lviv.ua"],
}

SOURCES = [
    "https://www.google.com/s2/favicons?domain={d}&sz=256",
    "https://icons.duckduckgo.com/ip3/{d}.ico",
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (portfolio build)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    return data, ctype

def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    for slug, domains in COMPANIES.items():
        existing = [f for f in os.listdir(OUT) if f.startswith(slug + ".")]
        if existing and not force:
            print(f"  {slug}: keeping {existing[0]}")
            continue
        for domain, src in [(d, s) for d in domains for s in SOURCES]:
            url = src.format(d=domain)
            try:
                data, ctype = fetch(url)
            except Exception as ex:
                print(f"  {slug}: {url} failed ({ex})")
                continue
            if len(data) < 300:  # Google returns a 16 px globe placeholder for unknown domains
                print(f"  {slug}: {url} returned a placeholder, trying next source")
                continue
            ext = "svg" if "svg" in ctype else ("ico" if "icon" in ctype or url.endswith(".ico") else "png")
            if ext == "ico":
                # convert .ico to png so <img> sizing is predictable
                try:
                    from PIL import Image
                    import io
                    im = Image.open(io.BytesIO(data)); im = im.convert("RGBA")
                    buf = io.BytesIO(); im.save(buf, "PNG"); data = buf.getvalue(); ext = "png"
                except Exception:
                    pass
            for old in existing:  # --force: drop the previous file so build.py picks up the new one
                os.remove(os.path.join(OUT, old))
            path = os.path.join(OUT, f"{slug}.{ext}")
            with open(path, "wb") as f: f.write(data)
            print(f"  {slug}: saved {os.path.basename(path)} ({len(data)} bytes) from {domain}")
            break
        else:
            print(f"  {slug}: no logo found, the monogram stays")

if __name__ == "__main__":
    main()
