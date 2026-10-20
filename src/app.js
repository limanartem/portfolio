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
  /* ---------- impact explorables: small interactive models of the problem behind an outcome ---------- */
  var LAB = {};
  function labEl(tag, cls, text) { var el = document.createElement(tag); if (cls) el.className = cls; if (text != null) el.textContent = text; return el; }
  function labSeg(opts, cur, onPick) {
    var seg = labEl('div', 'lab-seg');
    opts.forEach(function (o) {
      var b = labEl('button', o[0] === cur ? 'on' : '', o[1]); b.type = 'button';
      b.addEventListener('click', function () { seg.querySelectorAll('button').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); onPick(o[0]); });
      seg.appendChild(b);
    });
    return seg;
  }
  function labRange(text, min, max, val, step, onInput) {
    var l = labEl('label'), r = labEl('input'); r.type = 'range'; r.min = min; r.max = max; r.value = val; r.step = step || 1;
    var t = labEl('span', '', text); l.appendChild(t); l.appendChild(r);
    r.addEventListener('input', function () { onInput(parseFloat(r.value), t); });
    return { el: l, input: r, label: t };
  }
  function labColors() {
    var cs = getComputedStyle(root);
    return { accent: cs.getPropertyValue('--accent').trim(), line: cs.getPropertyValue('--line2').trim(), faint: cs.getPropertyValue('--faint').trim(), text: cs.getPropertyValue('--text2').trim(), muted: cs.getPropertyValue('--muted').trim(),
      mono: (cs.getPropertyValue('--font-mono').trim() || 'monospace') + ', ui-monospace, monospace' };
  }
  function labCanvas(stage) {
    var cv = labEl('canvas'); stage.appendChild(cv);
    var ctx = cv.getContext('2d'), W = 0, H = 0;
    function size() { var r = stage.getBoundingClientRect(), d = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = r.height; cv.width = Math.round(W * d); cv.height = Math.round(H * d); ctx.setTransform(d, 0, 0, d, 0, 0); }
    size(); window.addEventListener('resize', size);
    return { ctx: ctx, w: function () { return W; }, h: function () { return H; }, size: size };
  }
  function seeded(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
  function fmtInt(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

  /* Avira: ~200k zero-knowledge vaults can't be re-encrypted server-side, so each moves when its owner next logs in */
  LAB.migration = function (panel) {
    var N = 240, DAYS = 365, acc = [], R = seeded(42), i;
    for (i = 0; i < N; i++) acc.push({ u: R(), fast: 1 + R() * 13, slow: 30 + R() * 240, ph: R() });
    var st = { strategy: 'login', zk: true, occ: .45, day: 0, playing: false };
    var ctl = labEl('div', 'lab-ctl'), stage = labEl('div', 'lab-stage'), read = labEl('div', 'lab-read mono');
    ctl.appendChild(labSeg([['login', 'Migrate on next login'], ['bulk', 'Bulk re-encrypt overnight']], st.strategy, function (v) { st.strategy = v; st.day = 0; }));
    ctl.appendChild(labSeg([['zk', 'Zero-knowledge'], ['keys', 'Server holds keys']], 'zk', function (v) { st.zk = v === 'zk'; st.day = 0; }));
    var occ = labRange('occasional users 45%', 0, 100, 45, 1, function (v, t) { st.occ = v / 100; t.textContent = 'occasional users ' + v + '%'; });
    ctl.appendChild(occ.el);
    var play = labEl('button', 'lab-play'); play.type = 'button'; play.setAttribute('aria-label', 'Play'); play.innerHTML = '&#9654;';
    play.addEventListener('click', function () { if (st.day >= DAYS) st.day = 0; st.playing = !st.playing; });
    ctl.appendChild(play);
    var scrub = labRange('day 0', 0, DAYS, 0, 1, function (v, t) { st.day = v; st.playing = false; });
    scrub.el.style.flexBasis = '100%'; scrub.input.style.width = '100%'; scrub.input.style.flex = '1';
    ctl.appendChild(scrub.el);
    panel.appendChild(ctl); panel.appendChild(stage); panel.appendChild(read);
    panel.appendChild(labEl('p', 'lab-note', 'Illustrative model. Each square stands for about 800 accounts; login intervals are made up (regular users every 1–14 days, occasional users every 1–9 months), the ~200k total and the months-long tail are real.'));
    var C = labCanvas(stage), last = 0;
    function doneAt(a) { // day the account is migrated, or Infinity
      if (st.strategy === 'bulk') return st.zk ? Infinity : 1;
      var iv = a.u < st.occ ? a.slow : a.fast; return iv * a.ph;
    }
    function frame(now) {
      if (st.playing && !reduce) { st.day = Math.min(DAYS, st.day + (now - last) / 1000 * 70); if (st.day >= DAYS) st.playing = false; }
      last = now; scrub.input.value = st.day; scrub.label.textContent = 'day ' + Math.round(st.day);
      play.innerHTML = st.playing ? '&#10074;&#10074;' : '&#9654;';
      var ctx = C.ctx, W = C.w(), H = C.h(), col = labColors();
      ctx.clearRect(0, 0, W, H);
      var ds = acc.map(doneAt), done = 0;
      /* left: the vault grid */
      var gw = Math.min(W * .52, H * 1.1), cols = 20, rows = N / cols, cell = gw / cols, gx = 18, gy = (H - rows * cell) / 2;
      for (i = 0; i < N; i++) {
        var x = gx + (i % cols) * cell, y = gy + Math.floor(i / cols) * cell, s = cell * .68, m = (cell - s) / 2, ok = ds[i] <= st.day;
        if (ok) done++;
        ctx.fillStyle = ok ? col.accent : col.line; ctx.globalAlpha = ok ? 1 : .9;
        ctx.fillRect(x + m, y + m, s, s);
        if (st.strategy === 'bulk' && st.zk && st.day > 0) { ctx.strokeStyle = col.faint; ctx.globalAlpha = .8; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x + m, y + m); ctx.lineTo(x + m + s, y + m + s); ctx.stroke(); }
      }
      ctx.globalAlpha = 1; ctx.font = '600 11px ' + col.mono; ctx.fillStyle = col.faint; ctx.textAlign = 'left';
      ctx.fillText('ACCOUNTS', gx, gy - 8);
      /* right: cumulative migration curve */
      var px = gx + gw + 28, pw = W - px - 18, py = gy + 6, ph = rows * cell - 24;
      ctx.strokeStyle = col.line; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px, py + ph); ctx.lineTo(px + pw, py + ph); ctx.stroke();
      ctx.fillStyle = col.faint; ctx.fillText('MIGRATED', px, py - 8); ctx.textAlign = 'right'; ctx.fillText('12 MONTHS', px + pw, py + ph + 16); ctx.textAlign = 'left'; ctx.fillText('0', px, py + ph + 16);
      var sorted = ds.slice().sort(function (a, b) { return a - b; });
      ctx.lineWidth = 2;
      [[0, st.day, col.accent, 1], [st.day, DAYS, col.faint, .35]].forEach(function (seg) {
        ctx.strokeStyle = seg[2]; ctx.globalAlpha = seg[3]; ctx.beginPath();
        for (var d = seg[0], f = true; d <= seg[1]; d = Math.min(seg[1], d + 2)) {
          var k = 0; while (k < N && sorted[k] <= d) k++;
          var cx = px + d / DAYS * pw, cy = py + ph - k / N * ph;
          if (f) { ctx.moveTo(cx, cy); f = false; } else ctx.lineTo(cx, cy);
          if (d === seg[1]) break;
        }
        ctx.stroke();
      });
      ctx.globalAlpha = 1;
      var tx = px + st.day / DAYS * pw;
      ctx.strokeStyle = col.faint; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.moveTo(tx, py); ctx.lineTo(tx, py + ph); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = col.accent; ctx.beginPath(); ctx.arc(tx, py + ph - done / N * ph, 4, 0, 6.3); ctx.fill();
      var pct = Math.round(done / N * 100), msg;
      if (st.strategy === 'bulk' && st.zk) msg = st.day > 0 ? '<strong>blocked</strong> · the server never sees a master password, so it has nothing to re-encrypt with' : 'press play to run the overnight job';
      else if (st.strategy === 'bulk') msg = '<strong>' + pct + '%</strong> in one night · but a server that can read vaults is not a password manager';
      else msg = '<strong>' + pct + '%</strong> migrated · ' + (pct < 100 ? 'the tail is the occasional users; nobody is locked out, each vault moves on its own login' : 'done, every vault moved under its own master password');
      read.innerHTML = '<span>day ' + Math.round(st.day) + ' of 365</span><span>' + msg + '</span>';
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  };

  /* Roche: a LIMS whose queries went analytical. Row store vs column store, measured in pages read. */
  LAB.columnstore = function (panel) {
    var COLS = ['id', 'study', 'site', 'donor', 'collected', 'volume', 'temp', 'status', 'box', 'slot', 'consent', 'notes'], PAGE = 64;
    var st = { layout: 'row', query: 'sum', rows: 20000, t0: 0 };
    var ctl = labEl('div', 'lab-ctl'), stage = labEl('div', 'lab-stage'), read = labEl('div', 'lab-read mono');
    ctl.appendChild(labSeg([['row', 'Row store'], ['column', 'Column store']], st.layout, function (v) { st.layout = v; st.t0 = performance.now(); }));
    ctl.appendChild(labSeg([['sum', 'Average volume across all samples'], ['point', 'One sample by id']], st.query, function (v) { st.query = v; st.t0 = performance.now(); }));
    var rows = labRange('samples 20,000', 2, 6, Math.log10(st.rows), .05, function (v, t) { st.rows = Math.round(Math.pow(10, v)); t.textContent = 'samples ' + fmtInt(st.rows); st.t0 = performance.now(); });
    ctl.appendChild(rows.el);
    panel.appendChild(ctl); panel.appendChild(stage); panel.appendChild(read);
    panel.appendChild(labEl('p', 'lab-note', 'Illustrative model: 12 columns per sample, 64 values per page, no indexes or compression. Pages touched is the cost that grows with the archive; HANA’s column store made the study-wide questions cheap at the sizes the LIMS was heading for.'));
    var C = labCanvas(stage);
    function cost(layout, query, n) {
      var pagesAll = Math.ceil(n * COLS.length / PAGE), perCol = Math.ceil(n / PAGE);
      if (layout === 'row') return { all: pagesAll, read: query === 'sum' ? pagesAll : 1 };
      return { all: perCol * COLS.length, read: query === 'sum' ? perCol : COLS.length };
    }
    function frame(now) {
      var ctx = C.ctx, W = C.w(), H = C.h(), col = labColors(), cur = cost(st.layout, st.query, st.rows);
      var sweep = reduce ? 1 : Math.min(1, (now - st.t0) / 1100), ease = sweep * sweep * (3 - 2 * sweep);
      ctx.clearRect(0, 0, W, H);
      /* page blocks: in a column store the pages are laid out one band per column, so a one-column scan is one band */
      var top = 30, barH = 54, gh = H - top - barH - 22, gx = 18, gw = W - 36;
      var bands = st.layout === 'column' ? COLS.length : 1, perBand = Math.ceil(cur.all / bands);
      var bc = W > 640 ? 56 : 36, cw = (gw - (bands > 1 ? 52 : 0)) / bc, ch = cw;
      var br = Math.max(1, Math.min(Math.ceil(perBand / bc), Math.floor(gh / bands / ch)));
      var ox = gx + (bands > 1 ? 52 : 0), oy = top + (gh - bands * br * ch) / 2;
      var scale = Math.max(1, perBand / (bc * br)); // blocks stand for several pages when the archive is big
      var lit = Math.round(cur.read * ease), VOL = COLS.indexOf('volume');
      function isRead(band, k) { // is block k of this band among the pages read so far in the sweep
        var pageNo = k * scale;
        if (st.layout === 'row') return st.query === 'sum' ? pageNo < lit : (k === 0 && lit > 0);
        return st.query === 'sum' ? (band === VOL && pageNo < lit) : (k === 0 && band < lit);
      }
      ctx.font = '600 11px ' + col.mono; ctx.textAlign = 'left'; ctx.fillStyle = col.faint;
      ctx.fillText((st.layout === 'row' ? 'PAGES, EACH HOLDING WHOLE ROWS' : 'PAGES, ONE BAND PER COLUMN') + ' · ' + fmtInt(cur.all) + ' PAGES', gx, 18);
      for (var b = 0; b < bands; b++) for (var r = 0; r < br; r++) for (var c = 0; c < bc; c++) {
        if ((r * bc + c) * scale >= perBand) continue;
        var on = isRead(b, r * bc + c);
        var x = ox + c * cw, y = oy + (b * br + r) * ch, s = Math.max(1, cw - 1.5);
        ctx.fillStyle = on ? col.accent : col.line; ctx.globalAlpha = on ? 1 : .55; ctx.fillRect(x, y, s, Math.max(1, ch - 1.5));
      }
      ctx.globalAlpha = 1;
      if (st.layout === 'column') { ctx.fillStyle = col.faint; ctx.textAlign = 'right'; ctx.font = '500 9px ' + col.mono; for (b = 0; b < bands; b++) if (br * ch >= 8) ctx.fillText(COLS[b], ox - 6, oy + (b + .5) * br * ch + 3); }
      /* the comparison that matters: pages read by each layout for this query at this size */
      var rowC = cost('row', st.query, st.rows), colC = cost('column', st.query, st.rows), mx = Math.max(rowC.read, colC.read), by = H - barH - 4, bw = gw - 110 - 110;
      ctx.font = '600 11px ' + col.mono; ctx.textAlign = 'left';
      [['ROW STORE', rowC.read, 'row'], ['COLUMN STORE', colC.read, 'column']].forEach(function (q, k) {
        var y = by + k * 26, w = Math.max(2, q[1] / mx * bw * (q[2] === st.layout ? ease : 1)), me = q[2] === st.layout;
        ctx.fillStyle = me ? col.text : col.faint; ctx.fillText(q[0], gx, y + 11);
        ctx.fillStyle = me ? col.accent : col.line; ctx.fillRect(gx + 110, y, w, 14);
        ctx.fillStyle = col.text; ctx.fillText(fmtInt(q[1]) + ' pages', gx + 116 + w, y + 11);
      });
      var ratio = rowC.read / colC.read, msg;
      if (st.query === 'sum') msg = 'a study-wide question touches <strong>' + (ratio >= 1.5 ? Math.round(ratio) + '× fewer' : 'about as many') + ' pages</strong> in the column store' + (st.rows >= 100000 ? ', and the gap grows with the archive' : '');
      else msg = 'a single lookup is <strong>cheap either way</strong>: ' + COLS.length + ' pages instead of 1, which is why row stores won while the workload was clerical';
      read.innerHTML = '<span>' + fmtInt(cur.read) + ' of ' + fmtInt(cur.all) + ' pages read</span><span>' + msg + '</span>';
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  };

  document.querySelectorAll('[data-lab]').forEach(function (panel) {
    var kind = panel.getAttribute('data-lab');
    if (LAB[kind]) LAB[kind](panel);
  });
})();
