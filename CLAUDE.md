# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Static single-page portfolio. No framework, no package manager, no tests: `build.py` renders `src/` into `dist/`, and the GitHub Actions workflow deploys `dist/` to GitHub Pages on every push to `main`.

## Commands

- Build and preview: `python3 build.py && python3 -m http.server -d dist 8000`, then open `http://localhost:8000`.
- Fetch company logos: `python3 fetch_logos.py` (add `--force` to refetch). This needs network access, and Pillow for `.ico` → `.png`. CI runs it before every build.
- `SITE_URL` (env) sets the absolute URLs in the OpenGraph tags. It defaults to `https://limanartem.github.io/portfolio/`. CI sets it from the Pages config.

## How the build works

- `build.py` is the whole site generator. The content data (`HERO_PHOTOS`, `projects`, jobs, `SECTIONS`, `ICON_PATHS`, links) sits at the top. Small HTML helper functions follow, then a single f-string `page` template that writes `dist/index.html`. Edit content in those data lists, not in generated HTML.
- `dist/` is wiped on every build and is never committed.
- Assets are shipped only if they're referenced through `asset('<path relative to src>')` (or `img(...)`, which calls it). `asset()` copies the file to `dist/` under a content-hashed name (`styles.<hash>.css`) and returns that path. A file dropped into `src/` without an `asset()` reference isn't published. `app.js` and `styles.css` load the same way. Only `robots.txt` and `CNAME` are copied verbatim.
- Escape any text interpolated into the template with `e()` (`html.escape`). Strings that are already HTML (e.g. `TITLE` with `&amp;`) are inserted raw.
- Company logos: `fetch_logos.py` writes `src/assets/logos/<slug>.svg|png`, and `build.py`'s `logo()` uses one when present, else falls back to the `MONOGRAM` text. Slugs must match in both files (`COMPANIES` in `fetch_logos.py`, `MONOGRAM` in `build.py`). Existing logo files are never overwritten without `--force`, so a hand-placed logo wins.
- Tech-chip icons come from `src/icons.json` (name → SVG path), with `ICON_ALIAS` mapping variant names (e.g. `ASP.NET`) to one icon.
- Project screenshot slides: `img('assets/<file>', 'caption', bg, pad)`. The background and padding default to the project's `slide_bg=(bg, padding)`. Mobile screenshots: `phones(['assets/<a>', 'assets/<b>'], 'caption')` shows one or more single-screen images side by side in a CSS phone frame (crop composites into one screen per file first).

## Front end

- `src/app.js` is a plain ES5 IIFE, with no build step or dependencies. It finds behaviour hooks by `data-*` attributes that `build.py` emits (`data-carousel`, `data-captions`, `data-reveal`, `data-hero`, `data-lb-*`, `data-theme-set`). If you rename one, change both files.
- Theming: the dark palette is the `:root` default in `src/styles.css`. Light mode applies via `prefers-color-scheme` unless `[data-theme="dark"]` is set. The theme toggle in `app.js` stores the choice in `localStorage` (`pf-theme`) and sets `data-theme` on `<html>`. Colours, fonts and spacing are CSS variables at the top of `styles.css`.
