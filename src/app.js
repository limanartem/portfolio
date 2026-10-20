(function () {
  'use strict';
  var root = document.documentElement;

  /* ---------- theme selector (system / light / dark) ---------- */
  var segButtons = document.querySelectorAll('[data-theme-set]');
  function applyTheme(mode) {
    if (mode) root.setAttribute('data-theme', mode); else root.removeAttribute('data-theme');
    try { localStorage.setItem('pf-theme', mode || 'system'); } catch (e) {}
    segButtons.forEach(function (b) {
      var on = (b.getAttribute('data-theme-set') || '') === mode;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }
  segButtons.forEach(function (b) {
    b.addEventListener('click', function () { applyTheme(b.getAttribute('data-theme-set') || ''); });
  });
  applyTheme(root.getAttribute('data-theme') || '');

  /* ---------- compact sticky bar after scrolling ---------- */
  var top = document.querySelector('.top');
  if (top) {
    var onTop = function () { var on = window.scrollY > 48; top.classList.toggle('compact', on); root.style.setProperty('--bar-h', on ? '54px' : '66px'); };
    window.addEventListener('scroll', onTop, { passive: true }); onTop();
  }

  /* ---------- mobile menu ---------- */
  var burger = document.querySelector('.burger'), menu = document.getElementById('mobile-menu');
  function setMenu(open) {
    if (!burger || !menu) return;
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.documentElement.classList.toggle('menu-open', open);
    if (open) menu.removeAttribute('hidden'); else menu.setAttribute('hidden', '');
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') setMenu(false); });
    window.matchMedia('(min-width: 761px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  /* ---------- highlight the nav link of the section in view ---------- */
  var spyLinks = document.querySelectorAll('.navlinks a[href^="#"], #mobile-menu a[href^="#"]');
  var spyIds = [], spySeen = {};
  spyLinks.forEach(function (a) { var id = a.getAttribute('href').slice(1); if (id && !(id in spySeen) && document.getElementById(id)) { spySeen[id] = false; spyIds.push(id); } });
  function spySet(id) {
    spyLinks.forEach(function (a) {
      var on = a.getAttribute('href') === '#' + id;
      a.classList.toggle('on', on);
      if (on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }
  if (spyIds.length && 'IntersectionObserver' in window) {
    /* a section is "current" while it crosses a thin band about a third of the way down the viewport */
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { spySeen[en.target.id] = en.isIntersecting; });
      var cur = null;
      spyIds.forEach(function (id) { if (spySeen[id]) cur = id; });
      spySet(cur);
    }, { rootMargin: '-35% 0px -60% 0px' });
    spyIds.forEach(function (id) { spy.observe(document.getElementById(id)); });
  }

  /* ---------- scroll reveal ---------- */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var targets = document.querySelectorAll('[data-reveal]');
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.setAttribute('data-shown', ''); obs.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(function (el) { el.setAttribute('data-shown', ''); });
  }

  /* ---------- reading progress (fallback for browsers without scroll-timeline) ---------- */
  var bar = document.querySelector('.progress');
  if (bar && !(CSS && CSS.supports && CSS.supports('animation-timeline: scroll()'))) {
    var onScroll = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- lightbox ---------- */
  var lb = document.querySelector('.lightbox');
  var lbImg = lb && lb.querySelector('img');
  var lbCap = lb && lb.querySelector('.lb-cap');
  var lbCount = lb && lb.querySelector('.lb-count');
  var lbSet = [], lbIdx = 0, lbReturn = null;
  function lbShow(i) {
    lbIdx = ((i % lbSet.length) + lbSet.length) % lbSet.length;
    var it = lbSet[lbIdx];
    lbImg.src = it.src; lbImg.alt = it.alt;
    lbCap.textContent = it.alt;
    lbCount.textContent = (lbIdx + 1) + ' / ' + lbSet.length;
    lb.querySelectorAll('[data-lb-prev],[data-lb-next]').forEach(function (b) { b.style.display = lbSet.length > 1 ? '' : 'none'; });
  }
  function lbOpen(set, i, from) {
    if (!lb) return;
    lbSet = set; lbReturn = from;
    lbShow(i);
    lb.classList.add('open'); lb.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    lb.querySelector('[data-lb-close]').focus();
  }
  function lbClose() {
    if (!lb || !lb.classList.contains('open')) return;
    lb.classList.remove('open'); lb.setAttribute('hidden', '');
    document.body.style.overflow = '';
    if (lbReturn) lbReturn.focus();
  }
  if (lb) {
    lb.querySelector('[data-lb-close]').addEventListener('click', lbClose);
    lb.querySelector('[data-lb-prev]').addEventListener('click', function () { lbShow(lbIdx - 1); });
    lb.querySelector('[data-lb-next]').addEventListener('click', function () { lbShow(lbIdx + 1); });
    lb.addEventListener('click', function (ev) { if (ev.target === lb || ev.target.classList.contains('lb-stage')) lbClose(); });
    document.addEventListener('keydown', function (ev) {
      if (!lb.classList.contains('open')) return;
      if (ev.key === 'Escape') lbClose();
      else if (ev.key === 'ArrowLeft') lbShow(lbIdx - 1);
      else if (ev.key === 'ArrowRight') lbShow(lbIdx + 1);
    });
  }

  /* ---------- hero photo slider ---------- */
  var hero = document.querySelector('[data-hero]');
  if (hero) {
    var hp = hero.querySelectorAll('.hero-photo'), hd = hero.querySelectorAll('.hdot'), hcap = hero.querySelector('.hcap');
    var HERO_MS = 9000, hn = hp.length, hi = 0, hmanual = false;
    hero.style.setProperty('--dot-ms', HERO_MS + 'ms');
    function hgo(i) {
      hi = ((i % hn) + hn) % hn;
      hp.forEach(function (p, k) {
        if (k === hi) { p.classList.remove('out'); p.classList.add('on'); }
        else if (p.classList.contains('on')) { p.classList.remove('on'); p.classList.add('out'); setTimeout(function () { p.classList.remove('out'); }, 1900); }
        else { p.classList.remove('on', 'out'); }
      });
      hd.forEach(function (d, k) { d.classList.toggle('on', k === hi); var el = d.querySelector('i'); el.classList.remove('run'); void el.offsetWidth; if (!hmanual && !reduce) el.classList.add('run'); });
      if (hcap) hcap.textContent = (hi + 1 < 10 ? '0' : '') + (hi + 1) + ' / ' + (hn < 10 ? '0' : '') + hn;
    }
    hd.forEach(function (d) { d.addEventListener('click', function () { hmanual = true; hgo(parseInt(d.getAttribute('data-i'), 10)); }); });
    var hx0 = null;
    hero.addEventListener('touchstart', function (ev) { hx0 = ev.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (ev) { if (hx0 === null) return; var dx = ev.changedTouches[0].clientX - hx0; hx0 = null; if (Math.abs(dx) > 40) { hmanual = true; hgo(dx < 0 ? hi + 1 : hi - 1); } }, { passive: true });
    if (hn > 1 && !reduce) setInterval(function () { if (!hmanual && !document.hidden) hgo(hi + 1); }, HERO_MS);
    if (hn > 1) hgo(0);
  }

  /* ---------- gallery tiles open the lightbox as one set ---------- */
  document.querySelectorAll('[data-gallery]').forEach(function (gal) {
    var btns = Array.prototype.slice.call(gal.querySelectorAll('.zoom'));
    var set = btns.map(function (b) { var im = b.querySelector('img'); return { src: im.getAttribute('src'), alt: im.getAttribute('alt') || '' }; });
    btns.forEach(function (b, i) { b.addEventListener('click', function () { lbOpen(set, i, b); }); });
  });

  /* ---------- carousels ---------- */
  document.querySelectorAll('[data-carousel]').forEach(function (car) {
    var slides = car.querySelector('.slides');
    var items = slides.children;
    var n = items.length;
    var captions = [];
    try { captions = JSON.parse(car.getAttribute('data-captions') || '[]'); } catch (e) {}
    var counter = car.querySelector('.counter');
    var caption = car.querySelector('.caption');
    var dots = car.querySelectorAll('.dot');
    var cur = 0;
    function pad(x) { return (x < 10 ? '0' : '') + x; }
    function go(i) {
      cur = ((i % n) + n) % n;
      slides.style.transform = 'translateX(' + (-cur * 100) + '%)';
      if (counter) counter.textContent = pad(cur + 1) + ' / ' + pad(n);
      if (caption && captions[cur]) caption.textContent = captions[cur];
      dots.forEach(function (d, k) { d.classList.toggle('on', k === cur); });
      /* inert keeps off-screen slides out of the tab order and the accessibility tree */
      for (var k = 0; k < n; k++) items[k].toggleAttribute('inert', k !== cur);
    }
    /* autoplay: only while visible, paused on hover/focus/touch, off after a manual choice */
    var AUTO_MS = 5000, timer = null, visible = false, hovered = false, manual = false;
    car.style.setProperty('--dot-ms', AUTO_MS + 'ms');
    function tick() { if (visible && !hovered && !manual && !reduce && n > 1) go(cur + 1); }
    function start() { if (!timer) timer = setInterval(tick, AUTO_MS); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        visible = en[0].isIntersecting;
        if (visible) start(); else stop();
      }, { threshold: 0.2 }).observe(car);
    } else { visible = true; start(); }
    car.addEventListener('mouseenter', function () { hovered = true; });
    car.addEventListener('mouseleave', function () { hovered = false; });
    car.addEventListener('focusin', function () { hovered = true; });
    car.addEventListener('focusout', function () { hovered = false; });
    document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else if (visible) start(); });
    function userGo(i) { manual = true; go(i); }

    car.querySelector('[data-prev]').addEventListener('click', function () { userGo(cur - 1); });
    car.querySelector('[data-next]').addEventListener('click', function () { userGo(cur + 1); });
    car.querySelectorAll('[data-go]').forEach(function (b) {
      b.addEventListener('click', function () { userGo(parseInt(b.getAttribute('data-go'), 10)); });
    });
    car.classList.add('auto');
    /* click a screenshot to open it full size (all images of this slider, starting at the clicked one) */
    var zoomables = Array.prototype.slice.call(car.querySelectorAll('.slide-img img'));
    zoomables.forEach(function (im) {
      var btn = im.closest('.zoom');
      if (!btn) return;
      btn.addEventListener('click', function () {
        manual = true;
        var set = zoomables.map(function (x) { return { src: x.getAttribute('src'), alt: x.getAttribute('alt') || '' }; });
        lbOpen(set, zoomables.indexOf(im), btn);
      });
    });
    /* touch swipe */
    var x0 = null;
    slides.addEventListener('touchstart', function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
    slides.addEventListener('touchend', function (ev) {
      if (x0 === null) return;
      var dx = ev.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) userGo(dx < 0 ? cur + 1 : cur - 1);
    }, { passive: true });
    /* progress bar under the active dot restarts on every slide change */
    var _go = go;
    go = function (i) { _go(i); var d = car.querySelector('.dot.on'); if (d) { d.classList.remove('run'); void d.offsetWidth; if (!manual && !reduce) d.classList.add('run'); } };
    go(0);
  });
  /* ---------- impact scenes: particles re-enact each outcome as its step scrolls past ---------- */
  document.querySelectorAll('[data-scenes]').forEach(function (box) {
    var stage = box.querySelector('.scn-stage'), cv = stage && stage.querySelector('canvas');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d');
    var steps = Array.prototype.slice.call(box.querySelectorAll('.scn-step'));
    var ticks = Array.prototype.slice.call(stage.querySelectorAll('.scn-ticks i'));
    var hudN = stage.querySelector('.scn-n');
    var stacked = window.matchMedia('(max-width: 900px)');
    var N = window.innerWidth < 700 ? 800 : 1600, n = steps.length;
    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    function rng(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
    function disk(R, cx, cy, r) { var a = R() * 6.2832, d = Math.sqrt(R()) * r; return [cx + Math.cos(a) * d, cy + Math.sin(a) * d]; }
    function rect(R, x, y, w, h) { return [x + R() * w, y + R() * h]; }
    function inCloud(x, y) {
      function c(cx, cy, r) { return (x - cx) * (x - cx) + (y - cy) * (y - cy) < r * r; }
      return c(.37, .4, .12) || c(.52, .31, .16) || c(.66, .41, .11) || (y > .4 && y < .52 && x > .3 && x < .72);
    }
    /* each scene: [before, after] point generators in a unit square, label positions, and whether groups keep their own tone */
    var SCENES = {
      assemble: { f: [function (i, R) { return disk(R, .5, .5, .07 + .06 * R()); },
                      function (i, R) { var t = i % 36, c = t % 6, r = (t / 6) | 0, s = .13, z = .085; return rect(R, .5 + (c - 2.5) * s - z / 2, .47 + (r - 2.5) * s - z / 2, z, z); }],
                  l: [[.5, .68], [.5, .93]] },
      migrate:  { f: [function (i, R) { return disk(R, .26, .5, .17); }, function (i, R) { return disk(R, .74, .5, .17); }],
                  l: [[.26, .77], [.74, .77]] },
      lift:     { f: [function (i, R) { return rect(R, .1 + (i % 3) * .3, .72, .2, .13); },
                      function (i, R) { var x, y; do { x = .22 + R() * .56; y = .14 + R() * .4; } while (!inCloud(x, y)); return [x, y]; }],
                  l: [[.5, .94], [.5, .64]] },
      pivot:    { f: [function (i, R, u) { return [.14 + u * .72, .18 + (i % 9) * .075 + (R() - .5) * .008]; },
                      function (i, R, u) { return [.14 + (i % 9) * .09 + (R() - .5) * .008, .18 + u * .6]; }],
                  l: [[.5, .9], [.5, .9]] },
      merge:    { f: [function (i, R) { return disk(R, .2 + (i % 3) * .3, .5, .12); }, function (i, R) { return rect(R, .12, .43, .76, .14); }],
                  l: [[.5, .69], [.5, .67]], tint: 1 },
      order:    { f: [function (i, R) { return [.06 + R() * .88, .08 + R() * .76]; },
                      function (i, R) { var t = i % 12; return rect(R, .1 + (t % 4) * .21, .23 + ((t / 4) | 0) * .22, .17, .1); }],
                  l: [[.5, .95], [.5, .88]] }
    };
    var P = [], g, i;
    var Rp = rng(7);
    for (i = 0; i < N; i++) P.push({ x: 0, y: 0, u: Rp(), d: Rp(), ph: Rp() * 6.28, sg: Rp() < .5 ? -1 : 1, z: 1.8 + Rp() * 1.9, g: i % 3 });
    var groups = [[], [], []];
    P.forEach(function (p, k) { groups[p.g].push(k); });
    /* keyframes along the scroll position s (step k is centred at s = k): arrive at "before", play the change, hold "after" */
    var kfs = [], labels = [];
    steps.forEach(function (st, k) {
      var kind = st.getAttribute('data-scene'), sc = SCENES[kind] || SCENES.order, R = rng(101 + k * 977);
      var A = new Float32Array(N * 2), B = new Float32Array(N * 2), tint = sc.tint || 0;
      for (i = 0; i < N; i++) {
        var a = sc.f[0](i, R, P[i].u), b = sc.f[1](i, R, P[i].u);
        A[i * 2] = a[0]; A[i * 2 + 1] = a[1]; B[i * 2] = b[0]; B[i * 2 + 1] = b[1];
      }
      var mig = kind === 'migrate';
      kfs.push({ s: k - .3, p: A, tint: tint, st: .35, arc: .06, mig: false });
      kfs.push({ s: k + .12, p: B, tint: tint, st: mig ? .8 : .5, arc: mig ? -.26 : .05, mig: mig });
      kfs.push({ s: k + .35, p: B, tint: tint, st: 0, arc: 0, mig: false });
      labels.push({ k: k, a: st.getAttribute('data-from'), b: st.getAttribute('data-to'), la: sc.l[0], lb: sc.l[1] });
    });

    var col = ['#000', '#000', '#000'], faint = '#888', accent = '#0a0', mono = 'monospace', rgb = {};
    var probe = document.createElement('canvas').getContext('2d');
    function toRgb(c) { probe.fillStyle = '#000'; probe.fillStyle = c; var h = probe.fillStyle; if (h.charAt(0) !== '#') return [128, 128, 128]; return [parseInt(h.substr(1, 2), 16), parseInt(h.substr(3, 2), 16), parseInt(h.substr(5, 2), 16)]; }
    function readColors() {
      var cs = getComputedStyle(root);
      accent = cs.getPropertyValue('--accent').trim(); faint = cs.getPropertyValue('--faint').trim();
      mono = (cs.getPropertyValue('--font-mono').trim() || 'monospace') + ', ui-monospace, monospace';
      rgb = { a: toRgb(accent), t: toRgb(cs.getPropertyValue('--text2').trim()), m: toRgb(cs.getPropertyValue('--muted').trim()) };
    }
    function mix(c1, c2, t, al) { return 'rgba(' + Math.round(c1[0] + (c2[0] - c1[0]) * t) + ',' + Math.round(c1[1] + (c2[1] - c1[1]) * t) + ',' + Math.round(c1[2] + (c2[2] - c1[2]) * t) + ',' + al + ')'; }
    readColors();
    new MutationObserver(readColors).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', readColors);

    var W = 0, H = 0, dpr = 1;
    function size() {
      var r = stage.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); first = true;
    }
    size(); window.addEventListener('resize', size);

    var ptr = null;
    if (!reduce) {
      stage.addEventListener('pointermove', function (ev) { var r = stage.getBoundingClientRect(); ptr = { x: ev.clientX - r.left, y: ev.clientY - r.top }; });
      stage.addEventListener('pointerleave', function () { ptr = null; });
    }

    function scrollPos() {
      var vh = window.innerHeight;
      var anchor = stacked.matches ? (stage.getBoundingClientRect().bottom + vh) / 2 : vh * .5;
      var c = steps.map(function (st) { var r = st.getBoundingClientRect(); return r.top + r.height / 2; });
      if (n === 1) return 0;
      if (anchor < c[0]) return (anchor - c[0]) / (c[1] - c[0]);
      for (var k = 0; k < n - 1; k++) if (anchor < c[k + 1]) return k + (anchor - c[k]) / (c[k + 1] - c[k]);
      return n - 1 + (anchor - c[n - 1]) / (c[n - 1] - c[n - 2]);
    }

    var first = true, active = -1, running = false;
    function frame(now) {
      if (!running) return;
      var s = scrollPos(), j = 0;
      if (s <= kfs[0].s) j = 0; else if (s >= kfs[kfs.length - 1].s) j = kfs.length - 2;
      else while (j < kfs.length - 2 && s >= kfs[j + 1].s) j++;
      var a = kfs[j], b = kfs[j + 1], t = clamp((s - a.s) / (b.s - a.s));
      var tint = a.tint + (b.tint - a.tint) * t, st = b.st, arc = b.arc;
      var S = Math.min(W, H - 34) * .94, ox = (W - S) / 2, oy = (H - 34 - S) / 2;
      var amb = reduce ? 0 : S * .004, chase = reduce || first ? 1 : .14, tm = now * .0011;
      for (i = 0; i < N; i++) {
        var p = P[i], ti = st ? clamp((t - p.d * st) / (1 - st)) : t, e = ti * ti * (3 - 2 * ti);
        var ax = a.p[i * 2], ay = a.p[i * 2 + 1], bx = b.p[i * 2], by = b.p[i * 2 + 1];
        var x = ax + (bx - ax) * e, y = ay + (by - ay) * e;
        if (arc) { var lift = Math.sin(Math.PI * ti) * arc * (b.mig ? .5 + p.u : p.sg); x -= (by - ay) * lift; y += (bx - ax) * lift; }
        var tx = ox + x * S + Math.sin(tm * (.6 + p.u) + p.ph) * amb, ty = oy + y * S + Math.cos(tm * (.7 + p.d) + p.ph) * amb;
        if (ptr) { var dx = tx - ptr.x, dy = ty - ptr.y, dd = dx * dx + dy * dy; if (dd < 6400) { var f = (80 - Math.sqrt(dd)) / 80 * 30 / (Math.sqrt(dd) + 1); tx += dx * f; ty += dy * f; } }
        p.x += (tx - p.x) * chase; p.y += (ty - p.y) * chase;
      }
      first = false;
      /* fade the previous frame instead of clearing it, so moving particles leave short trails */
      ctx.globalCompositeOperation = 'destination-out'; ctx.fillStyle = 'rgba(0,0,0,' + (reduce ? 1 : .42) + ')'; ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'source-over';
      var fills = [mix(rgb.a, rgb.a, 0, 1), mix(rgb.a, rgb.t, tint, .72 + .28 * tint), mix(rgb.a, rgb.m, tint, .5 + .5 * tint)];
      for (g = 0; g < 3; g++) {
        ctx.fillStyle = fills[g];
        var ids = groups[g];
        for (var q = 0; q < ids.length; q++) { var pp = P[ids[q]]; ctx.fillRect(pp.x - pp.z / 2, pp.y - pp.z / 2, pp.z, pp.z); }
      }
      ctx.font = '600 12px ' + mono; ctx.textAlign = 'center';
      labels.forEach(function (L) {
        var k = L.k;
        var aA = clamp((s - (k - .65)) / .3) * (1 - clamp((s - (k - .2)) / .3));
        var aB = clamp((s - (k - .02)) / .15) * (1 - clamp((s - (k + .42)) / .2));
        if (aA > .01) { ctx.globalAlpha = aA; ctx.fillStyle = faint; ctx.fillText(L.a.toUpperCase(), ox + L.la[0] * S, oy + L.la[1] * S); }
        if (aB > .01) { ctx.globalAlpha = aB; ctx.fillStyle = accent; ctx.fillText(L.b.toUpperCase(), ox + L.lb[0] * S, oy + L.lb[1] * S); }
      });
      ctx.globalAlpha = 1;
      var on = Math.max(0, Math.min(n - 1, Math.round(s)));
      if (on !== active) {
        active = on;
        steps.forEach(function (st, k) { st.classList.toggle('on', k === on); });
        if (hudN) hudN.textContent = (on < 9 ? '0' : '') + (on + 1) + ' / ' + (n < 10 ? '0' : '') + n;
      }
      ticks.forEach(function (tk, k) { tk.style.setProperty('--p', clamp(s - k + .5).toFixed(3)); });
      requestAnimationFrame(frame);
    }
    function start() { if (!running) { running = true; requestAnimationFrame(frame); } }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { if (en[0].isIntersecting) start(); else running = false; }, { rootMargin: '200px 0px' }).observe(box);
    } else start();
  });
})();
