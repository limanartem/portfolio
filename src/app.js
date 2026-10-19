(function () {
  'use strict';
  var root = document.documentElement;

  /* ---------- theme selector (system / light / dark) ---------- */
  var segButtons = document.querySelectorAll('[data-theme-set]');
  function applyTheme(mode) {
    if (mode) root.setAttribute('data-theme', mode); else root.removeAttribute('data-theme');
    try { if (mode) localStorage.setItem('pf-theme', mode); else localStorage.removeItem('pf-theme'); } catch (e) {}
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
    var hn = hp.length, hi = 0, ht = null, hmanual = false, hhover = false;
    function hgo(i) {
      hi = ((i % hn) + hn) % hn;
      hp.forEach(function (p, k) { p.classList.toggle('on', k === hi); });
      hd.forEach(function (d, k) { d.classList.toggle('on', k === hi); var el = d.querySelector('i'); el.classList.remove('run'); void el.offsetWidth; if (!hmanual && !reduce) el.classList.add('run'); });
      if (hcap) hcap.textContent = (hi + 1 < 10 ? '0' : '') + (hi + 1) + ' / ' + (hn < 10 ? '0' : '') + hn;
    }
    hd.forEach(function (d) { d.addEventListener('click', function () { hmanual = true; hgo(parseInt(d.getAttribute('data-i'), 10)); }); });
    var hx0 = null;
    hero.addEventListener('touchstart', function (ev) { hx0 = ev.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (ev) { if (hx0 === null) return; var dx = ev.changedTouches[0].clientX - hx0; hx0 = null; if (Math.abs(dx) > 40) { hmanual = true; hgo(dx < 0 ? hi + 1 : hi - 1); } }, { passive: true });
    hero.addEventListener('mouseenter', function () { hhover = true; });
    hero.addEventListener('mouseleave', function () { hhover = false; });
    if (hn > 1 && !reduce) ht = setInterval(function () { if (!hmanual && !hhover && !document.hidden) hgo(hi + 1); }, 6000);
    if (hn > 1) hgo(0);
  }

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
      for (var k = 0; k < n; k++) items[k].setAttribute('aria-hidden', k === cur ? 'false' : 'true');
    }
    /* autoplay: only while visible, paused on hover/focus/touch, off after a manual choice */
    var AUTO_MS = 5000, timer = null, visible = false, hovered = false, manual = false;
    function tick() { if (visible && !hovered && !manual && !reduce && n > 1) go(cur + 1); }
    function start() { if (!timer) timer = setInterval(tick, AUTO_MS); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function restart() { stop(); start(); }
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
})();
