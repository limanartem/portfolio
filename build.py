#!/usr/bin/env python3
"""Builds the static portfolio site from ./src into ./dist (index.html + content-hashed assets).

Content lives in content.py (or the file named by the CONTENT env var); this file only renders it.
Sections are rendered in the order of content.SECTIONS, each by the renderer for its `type`.
"""
import html, os, shutil, json, importlib.util, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = os.path.join(HERE, "dist")
# Absolute site URL, used where crawlers need full URLs (og:image). The Pages workflow passes it in.
SITE_URL = os.environ.get("SITE_URL", "https://limanartem.github.io/portfolio/").rstrip("/") + "/"

def _hash(path):
    import hashlib
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:10]

_assets = {}
def asset(name):
    """Return the hashed public path for a source asset, copying it into dist on first use."""
    if name not in _assets:
        src = os.path.join(SRC, name)
        stem, ext = os.path.splitext(name)
        out = f"{stem}.{_hash(src)}{ext}"
        os.makedirs(os.path.dirname(os.path.join(OUT, out)), exist_ok=True)
        shutil.copy(src, os.path.join(OUT, out))
        _assets[name] = out
    return _assets[name]

def e(s): return html.escape(s, quote=True)

# slide helpers, imported by content files
def img(src, caption, bg=None, pad=None): return dict(kind='img', src=src, caption=caption, bg=bg, pad=pad)
def phones(srcs, caption, bg=None, pad=None):
    """One or more mobile screenshots shown side by side in a phone frame."""
    return dict(kind='phones', srcs=list(srcs), caption=caption, bg=bg, pad=pad)

# Stroke icons on a 24x24 grid; svg() wraps them in the shared outline attributes.
ICON_PATHS = {
 'arrow': '<path d="M7 17 17 7M8 7h9v9"/>',
 'zoom': '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3M11 8v6M8 11h6"/>',
 'lock': '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 'prev': '<path d="M15 18l-6-6 6-6"/>',
 'next': '<path d="M9 18l6-6-6-6"/>',
 'system': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
 'light': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 'dark': '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'close': '<path d="M6 6l12 12M18 6 6 18"/>',
 'link': '<path d="M10 14a3.5 3.5 0 0 0 5 0l4-4a3.5 3.5 0 0 0-5-5l-.5.5M14 10a3.5 3.5 0 0 0-5 0l-4 4a3.5 3.5 0 0 0 5 5l.5-.5"/>',
}
def svg(name, size=16, sw=2, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON_PATHS[name]}</svg>'

ARROW = svg('arrow', sw=2.2)
BULLET = '<span class="bullet" aria-hidden="true"></span>'

def ext(href, inner, cls='', label=''):
    """Link that opens in a new tab."""
    c = f' class="{cls}"' if cls else ''
    a = f' aria-label="{label}"' if label else ''
    return f'<a{c} href="{href}" target="_blank" rel="noopener"{a}>{inner}</a>'


def main():
    content_path = os.environ.get("CONTENT", os.path.join(HERE, "content.py"))
    spec = importlib.util.spec_from_file_location("content", content_path)
    C = importlib.util.module_from_spec(spec); sys.modules["content"] = C; spec.loader.exec_module(C)
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    page = render(C)
    with open(os.path.join(OUT, "index.html"), "w") as f: f.write(page)
    with open(os.path.join(OUT, ".nojekyll"), "w") as f: f.write("")
    for extra in ("robots.txt", "CNAME"):
        if os.path.exists(os.path.join(SRC, extra)): shutil.copy(os.path.join(SRC, extra), os.path.join(OUT, extra))
    print("built", OUT, "from", os.path.relpath(content_path, HERE)); print("\n".join(f"  {k} -> {v}" for k, v in _assets.items()))


def render(C):
    P, T = C.PERSON, C.THEME
    sections = list(C.SECTIONS)
    ids = [s['id'] for s in sections]
    get = lambda name, default: getattr(C, name, default)

    # ---- icons and chips
    ICONS = json.load(open(os.path.join(SRC, "icons.json")))
    for a, b in get('ICON_ALIAS', {}).items(): ICONS.setdefault(a, ICONS.get(b))
    chip_icons = get('CHIP_ICONS', 'all')
    def ico(name, size=14, cls=""):
        p = ICONS.get(name)
        if not p: return ""
        vb, d = (p["vb"], p["d"]) if isinstance(p, dict) else ("0 0 24 24", p)
        return f'<svg class="ico {cls}" width="{size}" height="{size}" viewBox="{vb}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></svg>'
    def chips(items, icons=False):
        use = chip_icons == "all" or (chip_icons == "projects" and icons)
        return ''.join(f'<span class="chip">{ico(t) if use else ""}{e(t)}</span>' for t in items)
    def bullets(items, cls='pt'): return ''.join(f'<li class="{cls}">{BULLET}<span>{e(p)}</span></li>' for p in items)
    def link_btn(label, href, icon, cls):
        inner = (ico(icon, 16) if icon else '') + e(label)
        return ext(href, inner, cls) if href.startswith('http') else f'<a class="{cls}" href="{href}">{inner}</a>'

    # ---- nav and section labels
    def nav(cls=''):
        c = f' class="{cls}"' if cls else ''
        return ''.join(f'<a{c} href="#{s["id"]}">{e(s["nav"])}</a>' for s in sections if s.get('nav'))
    def eyebrow(sid):
        k = ids.index(sid) + 1
        return f'<span class="eyebrow">{k:02d} / {e(next(s["label"] for s in sections if s["id"] == sid))}</span>'
    def sticky(sid): return f'<div class="sticky-label">{eyebrow(sid)}</div>'

    # ---- company logos
    monogram = get('MONOGRAM', {})
    def logo(slugs, name):
        out = []
        for slug in ([slugs] if isinstance(slugs, str) else slugs):
            for ext_ in ("svg", "png"):
                rel = f"assets/logos/{slug}.{ext_}"
                if os.path.exists(os.path.join(SRC, rel)):
                    out.append(f'<span class="clogo"><img src="{asset(rel)}" alt="" loading="lazy"></span>'); break
            else:
                out.append(f'<span class="clogo mono" aria-hidden="true">{e(monogram.get(slug, name[:2].upper()))}</span>')
        return f'<span class="clogos">{"".join(out)}</span>'

    # ---- slides and projects
    def zoom_btn(src, caption, cls='zoom'):
        return f'<button type="button" class="{cls}" aria-label="View full size: {e(caption)}"><img src="{src}" alt="{e(caption)}" loading="lazy"><span class="zoom-hint" aria-hidden="true">{svg("zoom", 16)}</span></button>'
    def slide_html(s, default_bg):
        bg, pad = s['bg'] or default_bg[0], s['pad'] or default_bg[1]
        if s['kind'] == 'img':
            return f'<div class="slide"><div class="slide-img" style="background:{bg};padding:{pad}">{zoom_btn(asset(s["src"]), s["caption"])}</div></div>'
        if s['kind'] == 'phones':
            return f'<div class="slide"><div class="slide-img slide-phones" style="background:{bg};padding:{pad}">' + ''.join(zoom_btn(asset(src), s['caption'], 'zoom phone') for src in s['srcs']) + '</div></div>'
        raise ValueError(f"unknown slide kind: {s['kind']!r}")
    def project_html(p, i):
        rev = ' reverse' if i % 2 else ''
        links = ''
        if p.get('live'): links += ext(p['live'][0], e(p['live'][1]) + ARROW, 'btn btn-primary sm')
        if p.get('repo'): links += ext(p['repo'], ico('GitHub', 15) + 'View on GitHub', 'btn btn-ghost sm')
        if p.get('private'): links += f'<span class="mono private">{svg("lock", 14)}Private repository</span>'
        dots = ''.join(f'<button type="button" class="dothit" data-go="{k}" aria-label="Go to slide {k+1}"><span class="dot{" on" if k==0 else ""}"></span></button>' for k in range(len(p['slides'])))
        captions = json.dumps([s['caption'] for s in p['slides']])
        meta = ''.join(f'<span class="mono {c}">{e(v)}</span>' for c, v in (('status', p.get('status')), ('kind', p.get('kind'))) if v)
        return f'''<article class="project{rev}" data-carousel data-captions='{e(captions)}'>
<div class="pr-head" data-reveal>
<div class="pr-meta">{meta}</div>
<h3 class="disp">{e(p['name'])}</h3>
</div>
<div class="pr-media" data-reveal="{'right' if i % 2 else 'left'}">
<div class="carousel" role="region" aria-roledescription="carousel" aria-label="{e(p["name"])} screenshots">
<div class="slides">{''.join(slide_html(s, p.get('slide_bg', ('var(--surface)', '20px'))) for s in p['slides'])}</div>
<div class="car-ui"><span class="mono counter">01 / {len(p['slides']):02d}</span>
<div class="car-btns"><button type="button" class="sbtn" data-prev aria-label="Previous slide">{svg("prev", 18)}</button>
<button type="button" class="sbtn" data-next aria-label="Next slide">{svg("next", 18)}</button></div></div>
</div>
<div class="car-foot"><span class="caption">{e(p['slides'][0]['caption'])}</span><div class="dots">{dots}</div></div>
</div>
<div class="pr-body" data-reveal style="--d:.15s">
<p class="pr-desc">{e(p['desc'])}</p>
{('<ul class="pts">' + bullets(p['points'], 'pt small') + '</ul>') if p.get('points') else ''}
{('<div class="chips">' + chips(p['tech'], icons=True) + '</div>') if p.get('tech') else ''}
<div class="pr-links">{links}</div>
</div>
</article>'''

    # ---- timeline
    def tl_left(period, slugs, company, place):
        return f'<div class="tl-left"><span class="mono period">{e(period)}</span><span class="company-row">{logo(slugs, company)}<span class="disp company">{e(company)}</span></span><span class="place">{e(place)}</span></div>'
    def job_html(j, current=False):
        return f'''<li class="tl-item{' current' if current else ''}" data-reveal>
{tl_left(j['period'], j['logo'], j['company'], j['place'])}
<div class="tl-dot" aria-hidden="true"></div>
<div class="tl-body"><h3 class="disp">{e(j['role'])}</h3><p class="scope">{e(j['scope'])}</p>
{('<ul class="pts">' + bullets(j['points']) + '</ul>') if j.get('points') else ''}{('<div class="chips">' + chips(j['tech']) + '</div>') if j.get('tech') else ''}</div>
</li>'''
    def early_html(slug, p, pl, r, c, b, t):
        return f'''<li class="tl-item compact" data-reveal>
{tl_left(p, slug, c, pl)}
<div class="tl-dot" aria-hidden="true"></div>
<details class="tl-body">
<summary><span class="disp role">{e(r)}</span><span class="plus" aria-hidden="true">+</span></summary>
<p class="scope">{e(b)}</p>{('<div class="chips">' + chips(t.split(' · ')) + '</div>') if t else ''}
</details>
</li>'''

    # ---- section renderers (one per type)
    def sec_about(s):
        facts = ''.join(f'<div class="fact"><dt class="mono">{e(k)}</dt><dd>{v}</dd></div>' for k, v in s.get('facts', []))
        paras = ''.join(f'<p data-reveal style="--d:{k*0.1:.1f}s">{p}</p>' for k, p in enumerate(s['paragraphs']))
        return f'''<section id="{s['id']}" class="sec">
<div class="wrap">{sticky(s['id'])}</div>
<div class="wrap two-col">
<div class="col-l" data-reveal="left"><h2 class="disp">{s['heading']}</h2></div>
<div class="col-r prose">{paras}{('<dl class="facts" data-reveal>' + facts + '</dl>') if facts else ''}</div>
</div>
</section>'''

    SCENES = ('assemble', 'migrate', 'lift', 'pivot', 'merge', 'order')

    def sec_impact(s):
        items = get('IMPACT', [])
        if not items: return ''
        if s.get('style') == 'scenes':
            return impact_scenes(s, items)
        cards = ''.join(f'<div data-reveal style="--d:{(k%3)*0.12:.2f}s"><article class="card impact"><div class="card-top mono"><span>{e(w)}</span><span>{k+1:02d}</span></div><div class="disp metric">{e(m)}</div><h3 class="disp">{e(t)}</h3><p>{e(b)}</p></article></div>' for k, (w, m, t, b, *_) in enumerate(items))
        return f'''<section id="{s['id']}" class="sec pt0">
<div class="wrap stack">{sticky(s['id'])}<div data-reveal><h2 class="disp">{s['heading']}</h2></div>
<div class="grid-3">{cards}</div>
</div>
</section>'''

    def impact_scenes(s, items):
        """Scroll-driven particle stage: each item's 5th field (scene, from-label, to-label) is re-enacted on a canvas."""
        n = len(items)
        steps = []
        for k, it in enumerate(items):
            if len(it) < 5 or it[4][0] not in SCENES:
                raise ValueError(f"impact style 'scenes' needs (kind, from, to) as the 5th field, kind in {SCENES}: {it[0]!r}")
            w, m, t, b, (kind, frm, to) = it
            steps.append(f'<li class="scn-step" data-scene="{kind}" data-from="{e(frm)}" data-to="{e(to)}"><article class="scn-card">'
                         f'<div class="card-top mono"><span>{e(w)}</span><span>{k+1:02d} / {n:02d}</span></div>'
                         f'<div class="disp metric">{e(m)}</div><h3 class="disp">{e(t)}</h3><p>{e(b)}</p></article></li>')
        ticks = ''.join('<i></i>' for _ in items)
        return f'''<section id="{s['id']}" class="sec pt0">
<div class="wrap stack">{sticky(s['id'])}<div data-reveal><h2 class="disp">{s['heading']}</h2></div>
<div class="scenes" data-scenes>
<div class="scn-stage" aria-hidden="true"><canvas></canvas><div class="scn-hud mono"><span class="scn-n">01 / {n:02d}</span><span class="scn-ticks">{ticks}</span></div></div>
<ol class="scn-steps">{''.join(steps)}</ol>
</div>
</div>
</section>'''

    def sec_experience(s):
        jobs, earlier = get('JOBS', []), get('EARLIER', [])
        era = f'<li class="tl-era" data-reveal><span class="mono">{e(s["era_label"])}</span></li>' if earlier and s.get('era_label') else ''
        end = f'<li class="tl-mark end" aria-hidden="true"><span class="mono">{e(s["start_label"])}</span></li>' if s.get('start_label') else ''
        return f'''<section id="{s['id']}" class="sec alt">
<div class="wrap stack">{sticky(s['id'])}<div data-reveal><h2 class="disp">{s['heading']}</h2></div>
<ol class="timeline">
<li class="tl-mark" aria-hidden="true"><span class="mono">today</span></li>
{''.join(job_html(j, i == 0) for i, j in enumerate(jobs))}
{era}
{''.join(early_html(*row) for row in earlier)}
{end}
</ol>
</div>
</section>'''

    def sec_projects(s):
        projects = get('PROJECTS', [])
        if not projects: return ''
        cta = link_btn(*s['cta'], 'btn btn-ghost') if s.get('cta') else ''
        intro = f'<p class="lede">{e(s["intro"])}</p>' if s.get('intro') else ''
        return f'''<section id="{s['id']}" class="sec">
<div class="wrap stack big">{sticky(s['id'])}
<div class="sec-head" data-reveal><div><h2 class="disp">{s['heading']}</h2>{intro}</div>{cta}</div>
{''.join(project_html(p, i) for i, p in enumerate(projects))}
</div>
</section>'''

    def sec_gallery(s):
        """Work samples as a responsive grid; every tile opens the lightbox. Items: dict(src, caption, wide=False, tall=False)."""
        items = get('GALLERY', [])
        if not items: return ''
        tiles = ''.join(f'<figure class="gal-item{" wide" if g.get("wide") else ""}{" tall" if g.get("tall") else ""}" data-reveal style="--d:{(k%4)*0.08:.2f}s">{zoom_btn(asset(g["src"]), g["caption"], "zoom gal")}<figcaption>{e(g["caption"])}</figcaption></figure>' for k, g in enumerate(items))
        intro = f'<p class="lede">{e(s["intro"])}</p>' if s.get('intro') else ''
        cta = link_btn(*s['cta'], 'btn btn-ghost') if s.get('cta') else ''
        return f'''<section id="{s['id']}" class="sec">
<div class="wrap stack">{sticky(s['id'])}
<div class="sec-head" data-reveal><div><h2 class="disp">{s['heading']}</h2>{intro}</div>{cta}</div>
<div class="gallery" data-gallery>{tiles}</div>
</div>
</section>'''

    def sec_publications(s):
        """Writing, talks, papers: dict(title, venue, year, href=None, note=None)."""
        items = get('PUBLICATIONS', [])
        if not items: return ''
        def row(p, k):
            title = f'<a href="{p["href"]}" target="_blank" rel="noopener">{e(p["title"])}{svg("link", 14, cls="pub-link")}</a>' if p.get('href') else e(p['title'])
            note = f'<p class="pub-note">{e(p["note"])}</p>' if p.get('note') else ''
            return f'<li class="pub" data-reveal style="--d:{(k%3)*0.08:.2f}s"><span class="mono pub-year">{e(str(p["year"]))}</span><div><h3 class="disp pub-title">{title}</h3><span class="pub-venue">{e(p["venue"])}</span>{note}</div></li>'
        intro = f'<p class="lede">{e(s["intro"])}</p>' if s.get('intro') else ''
        return f'''<section id="{s['id']}" class="sec alt">
<div class="wrap stack">{sticky(s['id'])}
<div class="sec-head" data-reveal><div><h2 class="disp">{s['heading']}</h2>{intro}</div></div>
<ol class="pubs">{''.join(row(p, k) for k, p in enumerate(items))}</ol>
</div>
</section>'''

    def sec_skills(s):
        groups = get('SKILLS', [])
        edu, cert, langs = get('EDUCATION', []), get('CERTIFICATIONS', []), get('LANGS', [])
        cards = ''.join(f'<div data-reveal style="--d:{(k%3)*0.1:.2f}s"><div class="card skill"><h3 class="disp">{e(t)}</h3><div class="chips">{chips(items)}</div></div></div>' for k, (t, items) in enumerate(groups))
        cols = []
        if edu: cols.append('<div class="meta-col" data-reveal><span class="mono accent">Education</span>' + ''.join(f'<div><div class="r">{r}</div><div class="b">{b}</div></div>' for r, b in edu) + '</div>')
        if cert: cols.append('<div class="meta-col" data-reveal style="--d:.1s"><span class="mono accent">Certifications &amp; training</span>' + ''.join(f'<div><div class="r">{r}</div><div class="b">{b}</div></div>' for r, b in cert) + '</div>')
        if langs: cols.append('<div class="meta-col" data-reveal style="--d:.2s"><span class="mono accent">Languages</span>' + ''.join(f'<div class="lang"><div class="lang-h"><span class="r">{e(n)}</span><span class="mono">{e(l)}</span></div><div class="bar"><div style="width:{p}%"></div></div></div>' for n, l, p in langs) + '</div>')
        if not (groups or cols): return ''
        return f'''<section id="{s['id']}" class="sec alt">
<div class="wrap stack">{sticky(s['id'])}<div data-reveal><h2 class="disp">{s['heading']}</h2></div>
{('<div class="grid-3">' + cards + '</div>') if cards else ''}
{('<div class="grid-3 meta">' + ''.join(cols) + '</div>') if cols else ''}
</div>
</section>'''

    def sec_contact(s):
        btns = ''.join(link_btn(l, h, i, 'btn btn-primary' if k == 0 else 'btn btn-ghost') for k, (l, h, i) in enumerate(s.get('buttons', [])))
        foot_links = ''.join(ext(h, ico(i, 18) if i else e(l), label=l) for l, h, i in P['links'])
        return f'''<section id="{s['id']}" class="sec contact">
<div class="dotgrid flip" aria-hidden="true"></div>
<div class="wrap stack">{sticky(s['id'])}
<h2 class="disp huge" data-reveal style="--d:.1s">{s['heading']}</h2>
<p class="lede" data-reveal style="--d:.2s">{e(s['text'])}</p>
<div class="btns contact-btns" data-reveal style="--d:.3s">{btns}</div>
<footer><span class="mono">{get('FOOTER', '')}</span>
<span class="foot-links">{foot_links}<a href="#top" class="mono uline">Back to top ↑</a></span></footer>
</div>
</section>'''

    RENDERERS = dict(about=sec_about, impact=sec_impact, experience=sec_experience, projects=sec_projects,
                     gallery=sec_gallery, publications=sec_publications, skills=sec_skills, contact=sec_contact)
    rendered = []
    for s in sections:
        if s['type'] not in RENDERERS: raise ValueError(f"unknown section type {s['type']!r} for #{s['id']}")
        rendered.append(RENDERERS[s['type']](s))
    if any(not r for r in rendered):
        empty = [s['id'] for s, r in zip(sections, rendered) if not r]
        raise ValueError(f"sections with no content, remove them from SECTIONS: {empty}")

    # ---- hero
    hero_photos = get('HERO_PHOTOS', [])
    photos = ''.join(f'<div class="hero-photo{" on" if i == 0 else ""}" style="background-image:url({asset(src)})" role="img" aria-label="{e(alt)}"></div>' for i, (src, alt) in enumerate(hero_photos))
    hctl = '' if len(hero_photos) < 2 else '<div class="hctl"><span class="mono hcap">01 / ' + f'{len(hero_photos):02d}' + '</span><div class="hdots">' + ''.join(f'<button type="button" class="hdot{" on" if i == 0 else ""}" data-i="{i}" aria-label="Photo {i + 1}"><i></i></button>' for i in range(len(hero_photos))) + '</div></div>'
    hero_btns = ''.join(link_btn(l, h, i, 'btn btn-primary' if k == 0 else 'btn btn-ghost') for k, (l, h, i) in enumerate(P['links']))
    if P.get('hero_cta'): hero_btns += f'<a class="btn btn-ghost" href="{P["hero_cta"][1]}">{e(P["hero_cta"][0])}</a>'
    badge = f'<div class="in mono badge"><span class="pulse"></span>{e(P["badge"])}</div>' if P.get('badge') else ''
    meta = ''.join(f'<span>{m}</span>' for m in P.get('meta', []))
    stats = get('STATS', [])
    stats_html = ('<div class="stats-strip"><div class="wrap stats">' + ''.join(f'<div class="stat"><span class="disp n">{e(n)}{("<span class=\"accent\">" + e(x) + "</span>") if x else ""}</span><span class="l">{l}</span></div>' for n, x, l in stats) + '</div></div>') if stats else ''
    marquee = get('MARQUEE', [])
    marquee_html = ('<div class="marquee" aria-label="Technologies"><div class="track disp">' + ''.join(f'<span>{ico(t, 26)}{e(t)}<i aria-hidden="true">◆</i></span>' for t in marquee * 2) + '</div></div>') if marquee else ''
    first_link = P['links'][0] if P.get('links') else None
    mm_links = ''.join(ext(h, (ico(i, 16) if i else '') + e(l)) for l, h, i in P['links'])
    og_image = f'{SITE_URL}{asset(hero_photos[0][0])}' if hero_photos else ''
    hero_class = 'hero' if hero_photos else 'hero hero-text-only'
    contact_id = next((s['id'] for s in sections if s['type'] == 'contact'), None)
    contact_btn = f'<a class="btn btn-primary sm nav-contact" href="#{contact_id}">Contact</a>' if contact_id else ''
    mm_contact = f'<a href="#{contact_id}" class="btn btn-primary">Contact</a>' if contact_id else ''

    scheme = T.get('scheme', 'system')
    theme_vars = f":root{{--accent:{T['accent_dark']};--font-display:'{T['display_font']}';--font-body:'{T['body_font']}';--font-mono:'{T['mono_font']}'}}" \
                 f":root[data-theme=\"light\"]{{--accent:{T['accent_light']}}}@media (prefers-color-scheme: light){{:root:not([data-theme=\"dark\"]){{--accent:{T['accent_light']}}}}}"

    return f'''<!doctype html>
<html lang="en" data-default-theme="{scheme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{P['title']}</title>
<meta name="description" content="{P['description']}">
<meta property="og:title" content="{P['title']}">
<meta property="og:description" content="{P['description']}">
<meta property="og:type" content="website">
{f'<meta property="og:image" content="{og_image}">' if og_image else ''}
<meta property="og:url" content="{SITE_URL}">
<meta name="twitter:card" content="{'summary_large_image' if og_image else 'summary'}">
<link rel="icon" href="{asset("assets/favicon.svg")}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{T['google_fonts']}&display=swap">
<link rel="stylesheet" href="{asset("styles.css")}">
<style>{theme_vars}</style>
<script>
try{{var t=localStorage.getItem('pf-theme');var d=document.documentElement.getAttribute('data-default-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);else if(t!=='system'&&(d==='light'||d==='dark'))document.documentElement.setAttribute('data-theme',d);}}catch(e){{}}
document.documentElement.setAttribute('data-js','');
</script>
</head>
<body>

<header class="top">
<nav aria-label="Main">
<a href="#top" class="brand disp"><span class="brand-mark">{e(P['initials'])}</span><span>{e(P['name'])}</span></a>
<div class="navlinks">
{nav("navlink")}
</div>
<div class="nav-right">
<div class="seg" role="group" aria-label="Colour theme">
<button type="button" class="segbtn" data-theme-set="" title="System" aria-label="Follow system theme">{svg("system", 16)}</button>
<button type="button" class="segbtn" data-theme-set="light" title="Light" aria-label="Light theme">{svg("light", 16)}</button>
<button type="button" class="segbtn" data-theme-set="dark" title="Dark" aria-label="Dark theme">{svg("dark", 16)}</button>
</div>
{contact_btn}
<button type="button" class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
{svg("menu", 20, cls="i-open")}
{svg("close", 20, cls="i-close")}
</button>
</div>
</nav>
<div id="mobile-menu" class="mobile-menu" hidden>
{nav()}
{mm_contact}
<div class="mm-links">{mm_links}</div>
</div>
<div class="progress" aria-hidden="true"></div>
</header>

<main>
<section id="top" class="{hero_class}" data-hero>
{photos}
<div class="hero-shade" aria-hidden="true"></div>
<div class="dotgrid hero-dots" aria-hidden="true"></div>
<div class="wrap hero-wrap">
<div class="hero-text">
{badge}
<h1 class="disp"><span class="line"><span>{e(P['first'])}</span></span><span class="line l2"><span class="accent">{e(P['last'])}</span></span></h1>
<p class="in d1 disp tagline">{P['tagline']}</p>
<p class="in d2 lede">{P['lede']}</p>
<div class="in d3 btns hero-btns">{hero_btns}</div>
<div class="in d4 mono hero-meta">{meta}</div>
</div>
</div>
{hctl}
</section>

{stats_html}
{marquee_html}

{''.join(rendered)}
</main>
<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Image viewer">
<button type="button" class="lb-btn lb-close" data-lb-close aria-label="Close">{svg("close", 20)}</button>
<button type="button" class="lb-btn lb-prev" data-lb-prev aria-label="Previous image">{svg("prev", 22)}</button>
<div class="lb-stage"><img src="" alt=""></div>
<button type="button" class="lb-btn lb-next" data-lb-next aria-label="Next image">{svg("next", 22)}</button>
<div class="lb-foot"><span class="lb-cap"></span><span class="mono lb-count"></span></div>
</div>
<script src="{asset("app.js")}"></script>
</body>
</html>
'''


if __name__ == "__main__":
    main()
