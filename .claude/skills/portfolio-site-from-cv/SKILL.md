---
name: portfolio-site-from-cv
description: Build a modern single-page portfolio site for any profession from a CV plus optional repos, work samples and photos, using this repository as the chassis: discovery, section modules chosen per person, a design direction per person, content.py, GitHub Pages deploy, verification and known pitfalls.
---

# Portfolio site from a CV

A portfolio page is an *extended* CV for one person: who they are, what they have done, and proof. This method separates what is fixed (the chassis: build, deploy, navigation, theming, motion, verification) from what varies per person (which sections exist, what they contain, and how the page looks). Never carry over another person's sections, copy or palette by default.

The chassis is this repository (template: https://github.com/limanartem/portfolio). Read `CLAUDE.md` and `README.md` first. `build.py` renders a content file into `dist/` with content-hashed assets; GitHub Actions deploys `dist/` to Pages on every push to `main`. Everything about the person lives in `content.py`; `examples/content-designer.py` is a second, creative-profile example. The default `content.py` is one engineering manager's site: an instance, not the standard.

## 0. Prerequisites

- A repo made from the template ("Use this template"), attached to the session so branches and PRs can be pushed. Pages source set to **GitHub Actions**.
- The CV (latest; older versions add detail), portrait photo(s) if a photo hero is wanted, proof material (screenshots, work samples, repo or live links, publication links), employer or client domains for logos.
- Answers to the discovery questions below, or a willingness to answer them in the first exchange.

## 1. Discovery (before any design or code)

Settle these with the person; propose defaults they can veto, ask only what the material does not answer:

- **Audience and purpose**: recruiters, clients, peers, students? Always-on presence or a campaign? Never add "open to work" wording unless asked.
- **Profession archetype** (sets default modules and design range):
  - *Engineer / engineering manager*: career timeline, selected outcomes, skills with brand marks, side projects with screenshot sliders.
  - *Designer / illustrator / photographer / architect*: gallery or case studies first, short bio, clients, tools, press, contact; no timeline or outcomes unless wanted; text chips.
  - *Writer / researcher / academic*: publications or talks first, topics, long-form bio; typographic, few images.
  - *Consultant / manager / founder*: outcomes and clients first, focus areas, compact timeline, real testimonials only.
  - Mixed: dominant archetype plus one borrowed module.
- **Modules** (each opt-in; nothing is padded to fill a module): hero (always) · about · impact (only if they want to name outcomes) · experience (full, compact or none) · projects · gallery · publications · skills (with education, certifications, languages) · contact.
- **Privacy**: no phone, address or email unless wanted; contact via the networks of their field (LinkedIn, Behance, Dribbble, ArtStation, ORCID, Scholar).
- **Identity**: existing logo, brand colours, the look of their own work. These override any default direction.

Write the agreed section list and a one-paragraph positioning statement back to the person before building.

## 2. Design direction (per person)

Commit to one nameable direction and state it; offer two or three low-fi candidates only when the person has no preference.

- Range: dark technical (default content.py), editorial light with a serif display, gallery-first near-white (the designer example), bold colour-block, quiet monochrome.
- `THEME` in content.py: `scheme` (`system`, `light`, `dark` for the first visit), `accent_dark`/`accent_light` (must pass 4.5:1 on their grounds), `display_font`/`body_font`/`mono_font` plus the matching `google_fonts` query. Avoid Inter, Roboto, Arial.
- Hero: `HERO_PHOTOS` with a studio-style portrait cropped to the subject (frame ends just past the shoulder, face upper right, watermark removed); several photos make a slider. No good portrait: leave `HERO_PHOTOS` empty for the text-only hero. Never a placeholder box.
- `STATS` and `MARQUEE`: only when real numbers or a real tool stack exist; empty lists hide them.
- Brand marks on chips (`CHIP_ICONS`): `all` or `projects` for technical profiles, `none` otherwise.
- Motion is already restrained and disabled under `prefers-reduced-motion`; do not add more.

## 3. Copy rules (everyone)

- Lead with what the person does for others, in plain words. Every line is sourced from the CV, their material or a confirmation; missing facts become visible placeholders, never inventions.
- `IMPACT`, if used: a handful of large, concrete results, each `dict(where, metric, title, body, tags=[])`. Write the metric as `before → after` where there is a real shift (it animates), keep numbers in it (they count up), and use 2–3 short tags. Process metrics and compliance work belong in job bullets.
- No em dashes; commas, colons, full stops, brackets instead. En dash for ranges. No filler, no superlatives the person did not use.
- Projects and gallery captions: what it is and for whom first, how it was made second. Drop images that look AI-generated unless they are the person's own work.
- Section labels are numbered automatically ("01 / About"); headings plain.

## 4. Build

- Write `content.py` from the template's shape: `PERSON`, `THEME`, `HERO_PHOTOS`, `STATS`, `MARQUEE`, `SECTIONS` (ordered, each with `type`), then the data each type reads (`IMPACT`, `JOBS`, `EARLIER`, `PROJECTS`, `GALLERY`, `PUBLICATIONS`, `SKILLS`, `EDUCATION`, `CERTIFICATIONS`, `LANGS`, `MONOGRAM`, `CHIP_ICONS`, `ICON_ALIAS`, `FOOTER`). A section listed without data fails the build on purpose: remove it from `SECTIONS`.
- Assets go in `src/assets/` and are referenced via `img(...)`, `phones([...])` or gallery `src`; unreferenced files are not published. Mobile screenshots: crop status and nav bars, use `phones()`.
- Company logos: fill `COMPANIES` in `fetch_logos.py` with verified domains (search; include the current parent company); CI fetches them. A hand-placed `src/assets/logos/<slug>.svg|png` wins. The sandbox usually cannot fetch images itself.
- Preview: `python3 build.py && python3 -m http.server -d dist 8000`. Another content file: `CONTENT=path python3 build.py`.
- New section type needed: add a renderer in `build.py`'s `RENDERERS`, CSS in `styles.css`, docs in `CLAUDE.md`; do not special-case the template.

## 5. Verify before handing over

Headless Chromium at 1440, 390 and 375x667, dark and light. Scroll with `behavior:'instant'` so reveals fire. Check: no failed requests; sticky bar pinned deep in the page; hero autoplay advances with the pointer parked over it; lightbox opens and closes (sliders and gallery); no horizontal overflow; hero subject in the right third on desktop and fully in frame on phones; every `SECTIONS` entry appears in nav and page. Report what was checked; never claim untested behaviour.

## 6. Deploy

Push a branch, open a PR, merge to `main`; the workflow builds and deploys. If a README renders instead of the site, Pages source is still "branch" or a legacy build won: set the source to GitHub Actions and re-run the workflow. Custom domain goes in `src/CNAME`. `index.html` is cached by Pages for up to 10 minutes; assets are hashed, so nothing else is stale.

## 7. Pitfalls

- `overflow-x: hidden/clip` on `body` or the page root breaks `position: sticky` on iOS Safari; clip on `main` only.
- Full-screen hero: no hover pause on autoplay (the pointer is always over it).
- Cross-fading two photos dims the hero mid-way; the chassis dissolves the outgoing photo on top of an instantly placed incoming one. Keep it.
- A landscape photo in a portrait box is always zoomed; the phone hero box is deliberately short.
- Blurred copies plus masked sharp layers read as a cut-out; one gradual gradient only.
- Placeholder replacement inside HTML that contains base64 data needs unique tokens.
- Private repos are not readable unless attached; ask for README and screenshots instead of guessing.
- A legacy branch Pages build can finish after the Actions deploy and overwrite it; re-run the workflow.
