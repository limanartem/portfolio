# Artem Liman — portfolio

Static portfolio site, built by `build.py` and deployed to GitHub Pages by the workflow in `.github/workflows/pages.yml`.

```
build.py                 builds src/ → dist/ (index.html + content-hashed assets)
src/styles.css           styling, light/dark themes
src/app.js               theme selector, scroll reveal, sliders (autoplay)
src/assets/              portrait, project screenshots, favicon
src/robots.txt           copied to the site root as-is (CNAME too, if present)
```

## How deployment works

Every push to `main` runs the workflow: it executes `build.py` and publishes `dist/` to GitHub Pages.
`dist/` is never committed.

The build renames every CSS, JS and image file with a hash of its content
(`styles.4cee8c9ff1.css`, `assets/portrait.2689783f89.jpg`, …) and references those names from `index.html`.
A changed file gets a new name, so browsers and the Pages CDN fetch it fresh; an unchanged file keeps its name
and stays cached. Only `index.html` itself keeps a fixed name, and GitHub Pages caches it for up to 10 minutes.

## One-time setup

1. Push this repository.
2. GitHub → Settings → Pages → *Build and deployment* → Source: **GitHub Actions**.
3. The first run of the "Build and deploy to GitHub Pages" workflow publishes the site; its URL appears in the workflow summary and in the Pages settings.

For a custom domain, enter it in the Pages settings and add a file `src/CNAME` containing the domain, so it survives every deploy.

## Company logos

`fetch_logos.py` downloads a mark for each employer into `src/assets/logos/` (from the company's site icon),
and the Pages workflow runs it on every build, so logos appear without any manual step. A file you place there
yourself (`<slug>.svg` or `.png`; slugs are listed in the script) is never overwritten, so swap in a proper
brand asset whenever an icon looks poor. To refresh everything: `python3 fetch_logos.py --force`.

## Editing

- Text and content: `build.py` (data lists at the top; the HTML template below them).
- Project screenshots: drop the image in `src/assets/` and reference it as `img('assets/<file>', 'caption', bg, padding)` in that project's `slides` list.
- Colours, fonts, spacing: the CSS variables at the top of `src/styles.css`.
- Preview locally: `python3 build.py && python3 -m http.server -d dist 8000`, then open `http://localhost:8000`.
