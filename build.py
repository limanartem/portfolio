#!/usr/bin/env python3
"""Builds the static portfolio site from ./src into ./dist (index.html + content-hashed assets)."""
import html, os, shutil, json

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = os.path.join(HERE, "dist")
# Absolute site URL, used where crawlers need full URLs (og:image). The Pages workflow passes it in.
SITE_URL = os.environ.get("SITE_URL", "https://limanartem.github.io/portfolio/").rstrip("/") + "/"
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

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

ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
BULLET = '<span class="bullet" aria-hidden="true"></span>'

HERO_PHOTOS = [  # order = slide order; one entry = no slider
 ('assets/hero/hero-1.jpg', 'Portrait of Artem Liman'),
 ('assets/hero/hero-2.jpg', 'Portrait of Artem Liman'),
]

tech_marquee = ['TypeScript','React','Java','Kotlin','Spring Boot','C# / .NET','Node.js','Kubernetes','Kafka','PostgreSQL','AWS','Azure','GraphQL','Docker','GitLab CI/CD','Claude Code']

impact = [
 ('CompuGroup Medical','MVP → Live','Took CGM Praxis into production','Led two teams taking a multi-tenant cloud SaaS for medical practices from MVP to production. Live since 2025 with several dozen practices onboarded. Owned the TI/gematik modules: VSDM, KIM, ePA, eAU, eArztbrief and e-signature.'),
 ('Avira / Gen','~200k accounts','Zero-knowledge backend migration','Moved Avira Password Manager onto Gen’s shared backend. Zero-knowledge encryption ruled out bulk re-encryption, so we designed a migration that moved each account safely on its next login over several months.'),
 ('inhive','Cloud eHealth platform','Built a medical data platform from the ground up','Led development of inhive’s own eHealth platform (web portal, taxonomy API and developer portal), bringing data from on-premise source systems into the cloud securely, with real-time access, cross-system reporting and fully automated CI/CD.'),
 ('Roche Diagnostics','SQL Server → SAP HANA','Re-platformed a biospecimen system','Architecture and development lead on a LIMS release that moved storage to SAP HANA and updated availability and replication, ready for larger datasets, more complex studies and globally distributed samples.'),
 ('Lufthansa Group','3 airlines, 1 platform','Public web platform at airline scale','Led a Scrum team on the group’s public-facing web platform, white-labeled for Lufthansa, SWISS and Austrian Airlines, from requirements to end-to-end delivery and third-party API coordination.'),
 ('Genentech · Merck · Bayer','Global pharma R&D','Architecture advisory in regulated life sciences','Assessed as-is architectures, designed target architectures and ran RFI/RFP vendor selections, including a LIMS for Genentech and a big-data and genome-analysis platform for Merck R&D.'),
]

jobs = [
 dict(logo='cgm', period='Jun 2024 – Present', company='CompuGroup Medical', place='Germany', role='Team Leader · CGM Praxis',
      scope='Two teams, 15 engineers in Germany and Romania, 5 direct reports. Multi-tenant cloud SaaS for medical practices.',
      points=['Took CGM Praxis from MVP to production; responsible for TI/gematik modules and TI vendor coordination.',
              'Introduced automated engineering and product KPIs with team dashboards.',
              'Automated release preparation across ~35 repositories and built a signed, notarized macOS installer pipeline on Azure DevOps.',
              'Delivered my teams’ share of the C5 attestation: access automation, vulnerability handling, pentest follow-ups, SOPs.',
              'Hire and onboard engineers, run reviews, goal setting, promotions and calibration; helped introduce CoderPad for screening.',
              'Built agent skills that check implementations against requirements and an AI reviewer for AI-generated code.'],
      tech=['TypeScript','React','Java','Kotlin','Spring Boot','PostgreSQL','Kubernetes','Kafka','GitLab CI/CD','Azure DevOps']),
 dict(logo=['avira', 'gen'], period='Jun 2020 – Feb 2024', company='Avira / NortonLifeLock / Gen', place='Germany', role='Engineering Manager · Browser-Based Applications',
      scope='Team of 7–9 engineers (iOS, Android, web, AWS backend) in Germany and Romania on Avira Password Manager and next-generation products on a unified platform.',
      points=['Led the migration of ~200k Password Manager accounts to Gen’s shared backend under zero-knowledge constraints.',
              'Shipped Avira Security desktop integration, new onboarding, master-password recovery and file attachments.',
              'After the Gen merger, coordinated integration and white-labeling with a team in India.',
              'Won first place in the company hackathon with a Figma-to-code pipeline generating per-platform design assets.',
              'Took over AWS backend and DevOps when needed; set engineering standards, code reviews and CI across web, mobile and backend.'],
      tech=['TypeScript','React','Node.js','C# / .NET Core','Kotlin','Swift','Python','AWS','DynamoDB','Docker','Jenkins','A/B testing']),
 dict(logo='inhive', period='May 2012 – May 2020', company='inhive Group', place='Germany', role='Lead Engineer · Team Lead · Architect',
      scope='Lead and architect roles on healthcare, pharma and aviation projects for Roche, Lufthansa Group, Genentech, Merck and Bayer.',
      points=['Lufthansa Group: led a Scrum team on the white-labeled public web platform for Lufthansa, SWISS and Austrian Airlines.',
              'Roche Diagnostics: architecture and development lead on a biospecimen-management (LIMS) release moving to SAP HANA.',
              'Led inhive’s own eHealth platform (web portal, taxonomy API, developer portal) on Azure and SAP HANA Cloud Platform.',
              'Roche: led the team that took a Confluence-based research collaboration platform from prototype to production.',
              'Genentech, Merck, Bayer: architecture assessments, target architectures, RFI/RFP vendor selection and distributed PoCs.'],
      tech=['.NET','ASP.NET Core','C#','Java','Azure','SAP HANA','SQL Server','Cosmos DB','MongoDB','Atlassian SDK']),
]

earlier = [
 ('verivox','2012','Germany','Senior .NET Developer','Verivox','Germany’s largest independent energy and telecom comparison portal: PDF sign-up features and a standalone importer that brought provider tariffs into the online system.','C# · ASP.NET · SQL Server · NUnit · TDD'),
 ('nix','2009 – 2011','Ukraine','Team Lead / .NET Tech Lead','N-iX','Led 6 developers and 2 QA engineers as Scrum Master for Manodo (Sweden): a web portal to monitor and control energy use across large smart-building estates. Core features, database design, specs and planning.','Silverlight · C# · Prism · WCF · SQL Server'),
 ('edvantis','2007 – 2008','Ukraine','Senior .NET Developer / Team Lead','Edvantis','Led 3–7 developers within a 30-person team building property tax and appraisal software for True Automation (US); owned core logic and the billing module.','.NET 3.5 · C# · SQL Server · Crystal Reports'),
 ('ukeess','2005 – 2007','Ukraine','Senior .NET Developer','UKEESS Software House','Server-side development for Cabconnect’s taxi payment platform: portals for drivers, card holders and cab companies on in-house business and UI frameworks.','.NET 2.0 · C# · ASP.NET · SQL Server'),
 ('leonorm','2001 – 2005','Ukraine','Software Developer','Leonorm','Internal projects for a national standards organisation: database design and Windows Forms applications.','.NET 1.1 · C# · VB.NET · Caché'),
]

def img(src, caption, bg='var(--surface)', pad='20px'): return dict(kind='img', src=asset(src), caption=caption, bg=bg, pad=pad)

projects = [
 dict(id='planner', name='Schiftmanager', kind='Resource & shift planning SaaS', status='Private beta',
      desc='Staff scheduling and management for small businesses such as medical practices: shifts, availability, time off, timesheets and payroll export in one place, with AI assistance built in. Running as a private beta.',
      points=['Coverage analysis: per-position staffing minimums, a weekly health score and understaffing alerts',
              'Week, month and day schedules grouped by position, with labour cost per day and one-click publishing',
              'Time off, leave balances, timesheets, open shifts, announcements, payroll export and compliance checks',
              'Multi-tenant orgs, Google sign-in, public holidays per region, light and dark themes',
              'GraphQL API on Firebase, React + TypeScript front end, OpenAI API, CI/CD on GitHub Actions'],
      tech=['React','TypeScript','Firebase','GraphQL','GitHub Actions','OpenAI API'],
      live=('https://beta.schiftmanager.de','beta.schiftmanager.de'), private=True,
      slides=[img('assets/schift-login.jpg','Sign in with Google or email','#0D0F14','0px'),
              img('assets/schift-schedule.jpg','Weekly schedule grouped by position, with hours per employee and labour cost per day','#F4F5F8','0px'),
              img('assets/schift-coverage.jpg','Coverage view: staffing minimums per position, health score and understaffing alerts','#0D0F14','0px'),
              img('assets/schift-dashboard.jpg','Dashboard: today’s shifts, coverage status, pending requests and quick actions','#0D0F14','0px')]),
 dict(id='training', name='Training App', kind='Mobile fitness app', status='Prototype',
      desc='A mobile fitness app that builds a workout plan around the equipment you actually have: photograph your training space and the AI generates a weekly programme in under a minute, no account needed.',
      points=['Equipment recognition from photos: snap your home gym and get a plan that uses only what is there',
              'AI-generated weekly programme with sets, reps and rest; plans adapt as you progress',
              'Per-exercise detail: target muscles, how-to, pro tips and common mistakes',
              'Localised UI (English, Ukrainian); zero-friction onboarding without sign-up'],
      tech=['Mobile','TypeScript','OpenAI API'], private=True,
      slides=[img('assets/training-1.jpg','Onboarding and equipment scan: photos of the training space feed the plan generator','#0E1013','0px'),
              img('assets/training-2.jpg','Generated weekly programme and exercise detail with today’s target','#0E1013','0px'),
              img('assets/training-3.jpg','Plan ready: days per week, experience level and goal','#0E1013','0px')]),
 dict(id='shop', name='Shop.App', kind='Distributed systems playground', status='Open source',
      desc='A web shop used as a playground for integrating distributed components: polyglot microservices, message-driven order processing and web and mobile clients, all running with a single docker-compose up.',
      points=['Orders flow through RabbitMQ workers (pending → payment → dispatch) with status updates back to the UI',
              'Catalog API in .NET 8 minimal APIs; orders and cart APIs in Node.js with REST and GraphQL',
              'Auth via SuperTokens; MongoDB, MySQL, PostgreSQL and Redis behind a private network',
              'npm-workspaces monorepo with shared packages, CI on GitHub Actions'],
      tech=['React','Redux','MUI','React Native / Expo','Node.js','Express','GraphQL','.NET 8','RabbitMQ','MongoDB','MySQL','PostgreSQL','Redis','Docker'],
      repo='https://github.com/limanartem/Shop.App',
      slides=[img('assets/shop-architecture.png','Architecture: public and private subnets, services and message broker','#FFFFFF','14px'),
              img('assets/shop-logo.png','Shop.App brand mark for web and mobile','var(--surface2)','40px')]),
 dict(id='home', name='Home.App', kind='Micro-frontend dashboard', status='Open source',
      desc='A home dashboard built as micro-frontends with React and Webpack Module Federation. Each widget is an independently built remote, loaded by a host at runtime.',
      points=['Host + remote apps wired with Module Federation','Strongly typed remote components: types generated to @mf-types and pulled by the host at build time','Weather widget built with MUI and MUI X Charts',
              'Runs on a Raspberry Pi 3 under Windows 10 IoT Core with a 10-inch touch screen'],
      tech=['React','TypeScript','Module Federation','Webpack','MUI','MUI X Charts'],
      repo='https://github.com/limanartem/Home.App',
      slides=[img('assets/home-rpi.jpg','Debugging the dashboard on a Raspberry Pi 3 with Windows 10 IoT Core and a 10-inch touch screen','#0E1013','0px'),
              dict(kind='mf', caption='Host loads typed remote widgets at runtime')]),
]

skills = [
 ('Leadership',['Hiring','Onboarding','Performance reviews','Calibration','Mentoring','1:1s','Distributed teams']),
 ('Delivery & practices',['Scrum','Kanban','TDD / BDD','Engineering KPIs','Release automation','Regulated environments']),
 ('Languages & frameworks',['TypeScript','JavaScript','Java','Kotlin','C#','React','Node.js','Spring Boot','.NET','REST','GraphQL']),
 ('Cloud, DevOps & data',['AWS','Azure','Kubernetes','Docker','Kafka','GitLab CI/CD','GitHub Actions','PostgreSQL','SQL Server','MongoDB','DynamoDB','Cosmos DB','SAP HANA']),
 ('Domains',['eHealth','TI / gematik (VSDM, KIM, ePA, eAU)','Zero-knowledge encryption','Life sciences & pharma R&D','Aviation web platforms']),
 ('AI tooling',['Claude Code','GitHub Copilot','Windsurf','OpenCode','Custom agent skills','OpenAI API']),
]

langs = [('Ukrainian','Native',100),('Russian','Native',100),('English','C1',85),('German','B2',68)]

ICONS = json.load(open(os.path.join(SRC, "icons.json")))
def ico(name, size=14, cls=""):
    """Inline monochrome brand mark (Simple Icons, CC0); empty string when the brand has none."""
    p = ICONS.get(name)
    if not p: return ""
    vb, d = (p["vb"], p["d"]) if isinstance(p, dict) else ("0 0 24 24", p)
    return f'<svg class="ico {cls}" width="{size}" height="{size}" viewBox="{vb}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></svg>'
# Where brand marks appear on chips: "all" = every chip that has one; "projects" = only side-project chips; "none" = text only.
CHIP_ICONS = "all"
ICON_ALIAS = {'ASP.NET': '.NET', 'ASP.NET Core': '.NET', '.NET 3.5': '.NET', '.NET 2.0': '.NET', '.NET 1.1': '.NET', 'VB.NET': '.NET', 'NUnit': '.NET', 'C# / .NET Core': '.NET', 'Prism': '.NET', 'WCF': '.NET'}
for _a, _b in ICON_ALIAS.items(): ICONS.setdefault(_a, ICONS.get(_b))

MONOGRAM = {'cgm': 'CGM', 'avira': 'AV', 'gen': 'GEN', 'inhive': 'IH', 'verivox': 'VX', 'nix': 'NX', 'edvantis': 'ED', 'ukeess': 'UK', 'leonorm': 'LN'}
def logo(slugs, name):
    """Company mark(s): src/assets/logos/<slug>.svg|png when present, else a monogram. Several slugs = several tiles."""
    out = []
    for slug in ([slugs] if isinstance(slugs, str) else slugs):
        for ext in ("svg", "png"):
            rel = f"assets/logos/{slug}.{ext}"
            if os.path.exists(os.path.join(SRC, rel)):
                out.append(f'<span class="clogo"><img src="{asset(rel)}" alt="" loading="lazy"></span>'); break
        else:
            out.append(f'<span class="clogo mono" aria-hidden="true">{e(MONOGRAM.get(slug, name[:2].upper()))}</span>')
    return f'<span class="clogos">{"".join(out)}</span>'

def chips(items, icons=False):
    use = CHIP_ICONS == "all" or (CHIP_ICONS == "projects" and icons)
    return ''.join(f'<span class="chip">{ico(t) if use else ""}{e(t)}</span>' for t in items)
def bullets(items, cls='pt'): return ''.join(f'<li class="{cls}">{BULLET}<span>{e(p)}</span></li>' for p in items)

def slide_html(s):
    if s['kind']=='img':
        return f'<div class="slide"><div class="slide-img" style="background:{s["bg"]};padding:{s["pad"]}"><button type="button" class="zoom" aria-label="View full size: {e(s["caption"])}"><img src="{s["src"]}" alt="{e(s["caption"])}" loading="lazy"><span class="zoom-hint" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3M11 8v6M8 11h6"/></svg></span></button></div></div>'
    if s['kind']=='mf':
        return '''<div class="slide"><div class="slide-mf">
<div class="mf-host"><div class="mono mf-k">host</div><div class="disp mf-name">home.app.host</div><div class="mono mf-k">Webpack Module Federation</div></div>
<div class="mf-link" aria-hidden="true"></div>
<div class="mf-grid">
<div class="mf-remote"><div class="mono mf-k">remote</div><div class="mf-r">weather</div><div class="mono mf-k">MUI · X Charts</div></div>
<div class="mf-remote ghost"><div class="mono mf-k">remote</div><div class="mf-r">next widget</div></div>
<div class="mf-remote ghost"><div class="mono mf-k">remote</div><div class="mf-r">next widget</div></div>
</div>
<div class="mono mf-foot">typed remotes via @module-federation/typescript → @mf-types</div></div></div>'''
    raise ValueError(f"unknown slide kind: {s['kind']!r}")

def project_html(p, i):
    rev = ' reverse' if i % 2 else ''
    links = ''
    if p.get('live'): links += f'<a class="btn btn-primary sm" href="{p["live"][0]}" target="_blank" rel="noopener">{e(p["live"][1])}{ARROW}</a>'
    if p.get('repo'): links += f'<a class="btn btn-ghost sm" href="{p["repo"]}" target="_blank" rel="noopener">{ico('GitHub', 15)}View on GitHub</a>'
    if p.get('private'): links += '<span class="mono private"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>Private repository</span>'
    dots = ''.join(f'<button type="button" class="dothit" data-go="{k}" aria-label="Go to slide {k+1}"><span class="dot{" on" if k==0 else ""}"></span></button>' for k in range(len(p['slides'])))
    captions = json.dumps([s['caption'] for s in p['slides']])
    return f'''<article class="project{rev}" data-carousel data-captions='{e(captions)}'>
<div class="pr-media" data-reveal="{'right' if i % 2 else 'left'}">
<div class="carousel" role="region" aria-roledescription="carousel" aria-label="{e(p["name"])} screenshots">
<div class="slides">{''.join(slide_html(s) for s in p['slides'])}</div>
<div class="car-ui"><span class="mono counter">01 / {len(p['slides']):02d}</span>
<div class="car-btns"><button type="button" class="sbtn" data-prev aria-label="Previous slide"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button>
<button type="button" class="sbtn" data-next aria-label="Next slide"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></button></div></div>
</div>
<div class="car-foot"><span class="caption">{e(p['slides'][0]['caption'])}</span><div class="dots">{dots}</div></div>
</div>
<div class="pr-text" data-reveal style="--d:.15s">
<div class="pr-meta"><span class="mono status">{e(p['status'])}</span><span class="mono kind">{e(p['kind'])}</span></div>
<h3 class="disp">{e(p['name'])}</h3>
<p class="pr-desc">{e(p['desc'])}</p>
<ul class="pts">{bullets(p['points'], 'pt small')}</ul>
<div class="chips">{chips(p['tech'], icons=True)}</div>
<div class="pr-links">{links}</div>
</div>
</article>'''

def job_html(j, current=False):
    return f'''<li class="tl-item{' current' if current else ''}" data-reveal>
<div class="tl-left"><span class="mono period">{e(j['period'])}</span><span class="company-row">{logo(j['logo'], j['company'])}<span class="disp company">{e(j['company'])}</span></span><span class="place">{e(j['place'])}</span></div>
<div class="tl-dot" aria-hidden="true"></div>
<div class="tl-body"><h3 class="disp">{e(j['role'])}</h3><p class="scope">{e(j['scope'])}</p>
<ul class="pts">{bullets(j['points'])}</ul><div class="chips">{chips(j['tech'])}</div></div>
</li>'''

def early_html(slug, p, pl, r, c, b, t):
    return f'''<li class="tl-item compact" data-reveal>
<div class="tl-left"><span class="mono period">{e(p)}</span><span class="company-row">{logo(slug, c)}<span class="disp company">{e(c)}</span></span><span class="place">{e(pl)}</span></div>
<div class="tl-dot" aria-hidden="true"></div>
<details class="tl-body">
<summary><span class="disp role">{e(r)}</span><span class="plus" aria-hidden="true">+</span></summary>
<p class="scope">{e(b)}</p><div class="chips">{chips(t.split(' · '))}</div>
</details>
</li>'''

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Artem Liman · Engineering Manager &amp; Team Lead</title>
<meta name="description" content="Artem Liman, Engineering Manager and Team Lead in eHealth. 20+ years in software, 10 leading teams. Portfolio, career and side projects.">
<meta property="og:title" content="Artem Liman · Engineering Manager &amp; Team Lead">
<meta property="og:description" content="20+ years building software, 10 of them leading teams. Portfolio, career and side projects.">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE_URL}{asset(HERO_PHOTOS[0][0])}">
<meta property="og:url" content="{SITE_URL}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{asset("assets/favicon.svg")}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{asset("styles.css")}">
<script>
try{{var t=localStorage.getItem('pf-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}
document.documentElement.setAttribute('data-js','');
</script>
</head>
<body>

<header class="top">
<nav aria-label="Main">
<a href="#top" class="brand disp"><span class="brand-mark">AL</span><span>Artem Liman</span></a>
<div class="navlinks">
<a class="navlink" href="#about">About</a><a class="navlink" href="#impact">Impact</a><a class="navlink" href="#experience">Career</a><a class="navlink" href="#projects">Projects</a><a class="navlink" href="#skills">Skills</a>
</div>
<div class="nav-right">
<div class="seg" role="group" aria-label="Colour theme">
<button type="button" class="segbtn" data-theme-set="" title="System" aria-label="Follow system theme"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/></svg></button>
<button type="button" class="segbtn" data-theme-set="light" title="Light" aria-label="Light theme"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
<button type="button" class="segbtn" data-theme-set="dark" title="Dark" aria-label="Dark theme"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>
</div>
<a class="btn btn-primary sm nav-contact" href="#contact">Contact</a>
<button type="button" class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
<svg class="i-open" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
<svg class="i-close" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>
</button>
</div>
</nav>
<div id="mobile-menu" class="mobile-menu" hidden>
<a href="#about">About</a><a href="#impact">Impact</a><a href="#experience">Career</a><a href="#projects">Projects</a><a href="#skills">Skills</a>
<a href="#contact" class="btn btn-primary">Contact</a>
<div class="mm-links"><a href="https://www.linkedin.com/in/artem-liman" target="_blank" rel="noopener">{ico('LinkedIn', 16)}LinkedIn</a><a href="https://github.com/limanartem" target="_blank" rel="noopener">{ico('GitHub', 16)}GitHub</a></div>
</div>
<div class="progress" aria-hidden="true"></div>
</header>

<main>
<section id="top" class="hero" data-hero>
{''.join(f'<div class="hero-photo{" on" if i == 0 else ""}" style="background-image:url({asset(src)})" role="img" aria-label="{e(alt)}"></div>' for i, (src, alt) in enumerate(HERO_PHOTOS))}
<div class="hero-shade" aria-hidden="true"></div>
<div class="dotgrid hero-dots" aria-hidden="true"></div>
<div class="wrap hero-wrap">
<div class="hero-text">
<div class="in mono badge"><span class="pulse"></span>Team Lead at CompuGroup Medical</div>
<h1 class="disp"><span class="line"><span>Artem</span></span><span class="line l2"><span class="accent">Liman</span></span></h1>
<p class="in d1 disp tagline">Engineering Manager &amp; Team Lead who still reads the diff.</p>
<p class="in d2 lede">20+ years building software, 10 of them leading teams. Today I run two product teams at CompuGroup Medical shipping CGM Praxis, a cloud SaaS for medical practices in Germany.</p>
<div class="in d3 btns hero-btns">
<a class="btn btn-primary" href="https://www.linkedin.com/in/artem-liman" target="_blank" rel="noopener">{ico('LinkedIn', 16)}LinkedIn</a>
<a class="btn btn-ghost" href="https://github.com/limanartem" target="_blank" rel="noopener">{ico('GitHub', 16)}GitHub</a>
<a class="btn btn-ghost" href="#projects">Side projects</a>
</div>
<div class="in d4 mono hero-meta"><span>Walldorf, Germany</span><span>EN C1 · DE B2 · UA/RU native</span></div>
</div>
</div>
{'' if len(HERO_PHOTOS) < 2 else '<div class="hctl"><span class="mono hcap">01 / ' + f'{len(HERO_PHOTOS):02d}' + '</span><div class="hdots">' + ''.join(f'<button type="button" class="hdot{" on" if i == 0 else ""}" data-i="{i}" aria-label="Photo {i + 1}"><i></i></button>' for i in range(len(HERO_PHOTOS))) + '</div></div>'}
</section>

<div class="stats-strip">
<div class="wrap stats">
<div class="stat"><span class="disp n">20<span class="accent">+</span></span><span class="l">years in software engineering</span></div>
<div class="stat"><span class="disp n">10</span><span class="l">years leading teams</span></div>
<div class="stat"><span class="disp n">15</span><span class="l">engineers in two teams, DE &amp; RO</span></div>
<div class="stat"><span class="disp n">4</span><span class="l">industries: eHealth, security, life sciences, aviation</span></div>
</div>
</div>

<div class="marquee" aria-label="Technologies"><div class="track disp">{''.join(f'<span>{ico(t, 26)}{e(t)}<i aria-hidden="true">◆</i></span>' for t in tech_marquee*2)}</div></div>

<section id="about" class="sec">
<div class="wrap"><div class="sticky-label"><span class="eyebrow">01 / About</span></div></div>
<div class="wrap two-col">
<div class="col-l" data-reveal="left"><h2 class="disp">Leading people, staying close to the code.</h2></div>
<div class="col-r prose">
<p data-reveal>At <strong>CompuGroup Medical</strong> I lead two cross-functional product teams, 15 engineers across Germany and Romania, building <strong>CGM Praxis</strong>, a multi-tenant cloud SaaS for medical practices with deep TI/gematik integration. I own delivery, engineering practices and people development for both teams.</p>
<p data-reveal style="--d:.1s">Before that I managed the <strong>Avira Password Manager</strong> team through its integration into Gen, and spent eight years at <strong>inhive</strong> as lead engineer, team lead and architect on healthcare, life sciences and aviation projects for Roche, Lufthansa Group, Genentech, Merck and Bayer.</p>
<p data-reveal style="--d:.2s">I care about teams that ship steadily and engineers who keep growing. I stay hands-on with architecture reviews, CI/CD and automation, and use side projects to try new tools and AI workflows before bringing them to a team.</p>
<dl class="facts" data-reveal>
<div class="fact"><dt class="mono">Domain</dt><dd>eHealth · TI/gematik</dd></div>
<div class="fact"><dt class="mono">Also shipped in</dt><dd>Security · Life sciences · Aviation</dd></div>
<div class="fact"><dt class="mono">Works in</dt><dd>Regulated, distributed teams</dd></div>
</dl>
</div>
</div>
</section>

<section id="impact" class="sec pt0">
<div class="wrap stack">
<div class="sticky-label"><span class="eyebrow">02 / Selected impact</span></div>
<div data-reveal><h2 class="disp">Outcomes I'm proud of</h2></div>
<div class="grid-3">
{''.join(f'<div data-reveal style="--d:{(k%3)*0.12:.2f}s"><article class="card impact"><div class="card-top mono"><span>{e(w)}</span><span>{k+1:02d}</span></div><div class="disp metric">{e(m)}</div><h3 class="disp">{e(t)}</h3><p>{e(b)}</p></article></div>' for k,(w,m,t,b) in enumerate(impact))}
</div>
</div>
</section>

<section id="experience" class="sec alt">
<div class="wrap stack">
<div class="sticky-label"><span class="eyebrow">03 / Career</span></div>
<div data-reveal><h2 class="disp">Career path</h2></div>
<ol class="timeline">
<li class="tl-mark" aria-hidden="true"><span class="mono">today</span></li>
{''.join(job_html(j, i == 0) for i, j in enumerate(jobs))}
<li class="tl-era" data-reveal><span class="mono">2001 – 2012 · Earlier roles</span></li>
{''.join(early_html(*row) for row in earlier)}
<li class="tl-mark end" aria-hidden="true"><span class="mono">2001 · first commit</span></li>
</ol>
</div>
</section>

<section id="projects" class="sec">
<div class="wrap stack big">
<div class="sticky-label"><span class="eyebrow">04 / Side projects</span></div>
<div class="sec-head" data-reveal>
<div><h2 class="disp">Where I keep my hands on the keyboard</h2><p class="lede">Products and playgrounds I build after hours to try architectures, tools and AI workflows before I bring them to a team.</p></div>
<a class="btn btn-ghost" href="https://github.com/limanartem" target="_blank" rel="noopener">{ico('GitHub', 16)}All repositories</a>
</div>
{''.join(project_html(p,i) for i,p in enumerate(projects))}
</div>
</section>

<section id="skills" class="sec alt">
<div class="wrap stack">
<div class="sticky-label"><span class="eyebrow">05 / Toolbox</span></div>
<div data-reveal><h2 class="disp">Skills &amp; stack</h2></div>
<div class="grid-3">
{''.join(f'<div data-reveal style="--d:{(k%3)*0.1:.2f}s"><div class="card skill"><h3 class="disp">{e(t)}</h3><div class="chips">{chips(items)}</div></div></div>' for k,(t,items) in enumerate(skills))}
</div>
<div class="grid-3 meta">
<div class="meta-col" data-reveal><span class="mono accent">Education</span>
<div><div class="r">M.Sc., Power Engineering</div><div class="b">Lviv Polytechnic National University · 2003 – 2005</div></div>
<div><div class="r">B.Sc., Electric Networks and Systems</div><div class="b">Lviv Polytechnic Institute · 2000 – 2003</div></div></div>
<div class="meta-col" data-reveal style="--d:.1s"><span class="mono accent">Certifications &amp; training</span>
<div><div class="r">Developing Winning Teams</div><div class="b">troodi leadership training · 2026</div></div>
<div><div class="r">Certified ScrumMaster (CSM)</div><div class="b">Scrum Alliance · 2010</div></div>
<div><div class="r">AWS training</div><div class="b">Architecting, Developing, Advanced Developing, Serverless Solutions</div></div>
<div><div class="r">Microsoft MCPD &amp; MCTS</div><div class="b">ASP.NET Developer 3.5 · .NET Framework 3.5 ASP.NET Applications</div></div></div>
<div class="meta-col" data-reveal style="--d:.2s"><span class="mono accent">Languages</span>
{''.join(f'<div class="lang"><div class="lang-h"><span class="r">{e(n)}</span><span class="mono">{e(l)}</span></div><div class="bar"><div style="width:{p}%"></div></div></div>' for n,l,p in langs)}
</div>
</div>
</div>
</section>

<section id="contact" class="sec contact">
<div class="dotgrid flip" aria-hidden="true"></div>
<div class="wrap stack">
<div class="sticky-label"><span class="eyebrow">06 / Contact</span></div>
<h2 class="disp huge" data-reveal style="--d:.1s">Let's talk <span class="accent">engineering.</span></h2>
<p class="lede" data-reveal style="--d:.2s">Happy to connect about engineering leadership, eHealth, distributed systems or AI-assisted development. LinkedIn is the best way to reach me.</p>
<div class="btns contact-btns" data-reveal style="--d:.3s">
<a class="btn btn-primary" href="https://www.linkedin.com/in/artem-liman" target="_blank" rel="noopener">{ico('LinkedIn', 16)}Connect on LinkedIn</a>
<a class="btn btn-ghost" href="https://github.com/limanartem" target="_blank" rel="noopener">{ico('GitHub', 16)}github.com/limanartem</a>
</div>
<footer><span class="mono">© 2026 Artem Liman · Walldorf, Germany</span>
<span class="foot-links"><a href="https://www.linkedin.com/in/artem-liman" target="_blank" rel="noopener" aria-label="LinkedIn">{ico('LinkedIn', 18)}</a><a href="https://github.com/limanartem" target="_blank" rel="noopener" aria-label="GitHub">{ico('GitHub', 18)}</a><a href="#top" class="mono uline">Back to top ↑</a></span></footer>
</div>
</section>
</main>
<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Image viewer">
<button type="button" class="lb-btn lb-close" data-lb-close aria-label="Close"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
<button type="button" class="lb-btn lb-prev" data-lb-prev aria-label="Previous image"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg></button>
<div class="lb-stage"><img src="" alt=""></div>
<button type="button" class="lb-btn lb-next" data-lb-next aria-label="Next image"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg></button>
<div class="lb-foot"><span class="lb-cap"></span><span class="mono lb-count"></span></div>
</div>
<script src="{asset("app.js")}"></script>
</body>
</html>
'''

with open(os.path.join(OUT, "index.html"), "w") as f: f.write(page)
with open(os.path.join(OUT, ".nojekyll"), "w") as f: f.write("")
for extra in ("robots.txt", "CNAME"):
    if os.path.exists(os.path.join(SRC, extra)): shutil.copy(os.path.join(SRC, extra), os.path.join(OUT, extra))
print("built", OUT); print("\n".join(f"  {k} -> {v}" for k, v in _assets.items()))
