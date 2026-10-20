# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Static single-page portfolio. No framework, no package manager, no tests: `build.py` renders `src/` into `dist/`, and the GitHub Actions workflow deploys `dist/` to GitHub Pages on every push to `main`.

## Making a site for another person

Follow the skill in `.claude/skills/portfolio-site-from-cv/SKILL.md` (discovery, module choice, design direction, copy rules, rebrand, verification). The content goes in `content.py`. The previous owner also has to be removed from the README, this file, the `SITE_URL` default, the favicon, `fetch_logos.py` and `src/assets/` (skill step 5).

## Commands

- Build and preview: `python3 build.py && python3 -m http.server -d dist 8000`, then open `http://localhost:8000`.
- Single-file preview: `python3 build.py && python3 preview.py` writes `dist/preview.html` with CSS, JS and images inlined, so it opens from disk. `.github/workflows/preview.yml` builds it on every pull request, uploads it as an artifact and keeps one comment on the PR with the download link.
- Fetch company logos: `python3 fetch_logos.py` (add `--force` to refetch). This needs network access, and Pillow for `.ico` → `.png`. CI runs it before every build.
- `SITE_URL` (env) sets the absolute URLs in the OpenGraph tags. It defaults to `https://limanartem.github.io/portfolio/`. CI sets it from the Pages config.

## How the build works

- `content.py` holds everything about the person (`PERSON`, `THEME`, `SECTIONS`, `HERO_PHOTOS`, `STATS`, `MARQUEE`, `IMPACT`, `JOBS`, `EARLIER`, `PROJECTS`, `GALLERY`, `PUBLICATIONS`, `SKILLS`, `EDUCATION`, `CERTIFICATIONS`, `LANGS`, `MONOGRAM`, `FOOTER`). `build.py` renders it: `render(C)` builds the page from `C.SECTIONS`, one renderer per section `type` in `RENDERERS`. Edit content in `content.py`, never in generated HTML; add a new section type by adding a renderer and CSS, not by special-casing the template.
- `CONTENT=<path> python3 build.py` renders another content file (see `examples/`). A section listed in `SECTIONS` whose data is empty fails the build; remove it from the list instead.
- `THEME` is emitted as an inline `<style>` after `styles.css` (accent per scheme, `--font-display/--font-body/--font-mono`) plus `data-default-theme` on `<html>`; the inline script applies it on first visit unless the visitor chose a theme (`pf-theme` in localStorage, `system` stored explicitly).
- `dist/` is wiped on every build and is never committed.
- Assets are shipped only if they're referenced through `asset('<path relative to src>')` (or `img(...)`, which calls it). `asset()` copies the file to `dist/` under a content-hashed name (`styles.<hash>.css`) and returns that path. A file dropped into `src/` without an `asset()` reference isn't published. `app.js` and `styles.css` load the same way. Only `robots.txt` and `CNAME` are copied verbatim.
- Escape any text interpolated into the template with `e()` (`html.escape`). Strings that are already HTML (e.g. `TITLE` with `&amp;`) are inserted raw.
- Company logos: `fetch_logos.py` writes `src/assets/logos/<slug>.svg|png`, and `build.py`'s `logo()` uses one when present, else falls back to the `MONOGRAM` text. Slugs must match in both files (`COMPANIES` in `fetch_logos.py`, `MONOGRAM` in `build.py`). Existing logo files are never overwritten without `--force`, so a hand-placed logo wins.
- Tech-chip icons come from `src/icons.json` (name → SVG path), with `ICON_ALIAS` mapping variant names (e.g. `ASP.NET`) to one icon. `ico()` emits `<svg><use href="#i-<slug>"></svg>` and collects each distinct path once into a hidden sprite at the top of `<body>`, so an icon repeated across chips is shipped once.
- Project screenshot slides: `img('assets/<file>', 'caption', bg, pad)` (paths are resolved through `asset()` at render time). The background and padding default to the project's `slide_bg=(bg, padding)`. Mobile screenshots: `phones(['assets/<a>', 'assets/<b>'], 'caption')` shows one or more single-screen images side by side in a CSS phone frame (crop composites into one screen per file first).

## Section types

`about` (heading, paragraphs, facts), `impact` (IMPACT cards: `dict(where, metric, title, body, tags=[])`; a metric written as `before → after` renders as an arrow that draws itself on reveal, numbers in it count up, and cards get a pointer spotlight and tilt on desktop), `experience` (JOBS timeline + EARLIER compact stops, `era_label`, `start_label`), `projects` (PROJECTS with sliders, `intro`, `cta`), `gallery` (GALLERY tiles, `wide`/`tall` spans, lightbox), `publications` (PUBLICATIONS rows), `skills` (SKILLS groups + EDUCATION, CERTIFICATIONS, LANGS), `contact` (heading, text, buttons, FOOTER). Hero without `HERO_PHOTOS` renders the text-only variant.

## Front end

- `src/app.js` is a plain ES5 IIFE, with no build step or dependencies. It finds behaviour hooks by `data-*` attributes that `build.py` emits (`data-carousel`, `data-captions`, `data-reveal`, `data-count`, `data-tilt`, `data-hero`, `data-lb-*`, `data-theme-set`). If you rename one, change both files.
- Theming: the dark palette is the `:root` default in `src/styles.css`. Light mode applies via `prefers-color-scheme` unless `[data-theme="dark"]` is set. The theme toggle in `app.js` stores the choice in `localStorage` (`pf-theme`) and sets `data-theme` on `<html>`. Colours, fonts and spacing are CSS variables at the top of `styles.css`.
