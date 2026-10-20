#!/usr/bin/env python3
"""Folds a built dist/ into one self-contained dist/preview.html (CSS, JS and images inlined).

Run after build.py. The result opens from disk without a server, which is how pull-request
previews are shared: the preview workflow attaches it to the PR as an artifact.
"""
import base64, mimetypes, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
OUT = os.path.join(DIST, "preview.html")

def read(rel, mode="r"):
    with open(os.path.join(DIST, rel), mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        return f.read()

def data_uri(rel):
    mime = mimetypes.guess_type(rel)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(read(rel, "rb")).decode()

def main():
    if not os.path.exists(os.path.join(DIST, "index.html")):
        sys.exit("dist/index.html not found: run build.py first")
    html = read("index.html")
    html = re.sub(r'<link rel="stylesheet" href="([^"]+\.css)">',
                  lambda m: "<style>" + read(m.group(1)) + "</style>", html)
    html = re.sub(r'<script([^>]*) src="([^"]+\.js)"([^>]*)></script>',
                  lambda m: f"<script{m.group(1)}{m.group(3)}>" + read(m.group(2)) + "</script>", html)
    # every remaining relative asset reference (img src, inline url()); absolute URLs such as og:image stay
    html = re.sub(r'(?<![\w/])(assets/[\w./-]+)',
                  lambda m: data_uri(m.group(1)) if os.path.exists(os.path.join(DIST, m.group(1))) else m.group(0), html)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT} ({os.path.getsize(OUT) // 1024} KB)")

if __name__ == "__main__":
    main()
