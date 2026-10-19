# Artem Liman — portfolio

Static portfolio site, hosted with GitHub Pages.

- `index.html` — the page
- `styles.css`, `app.js` — styling, theme selector, scroll reveal, project sliders
- `assets/` — portrait, project images, favicon
- `.nojekyll` — tells GitHub Pages to serve the files as they are

## Editing

- Text and content live directly in `index.html`.
- Project screenshots: put the image in `assets/` and replace a placeholder `<div class="slide">…</div>` block
  inside the project's `.slides` container with
  `<div class="slide"><div class="slide-img" style="background:#fff;padding:14px"><img src="assets/your-file.png" alt="…" loading="lazy"></div></div>`;
  update the matching entry in that project's `data-captions` attribute.
- Accent colour and theme palettes are the CSS variables at the top of `styles.css`.
