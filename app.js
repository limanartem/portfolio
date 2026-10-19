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
    car.querySelector('[data-prev]').addEventListener('click', function () { go(cur - 1); });
    car.querySelector('[data-next]').addEventListener('click', function () { go(cur + 1); });
    car.querySelectorAll('[data-go]').forEach(function (b) {
      b.addEventListener('click', function () { go(parseInt(b.getAttribute('data-go'), 10)); });
    });
    /* touch swipe */
    var x0 = null;
    slides.addEventListener('touchstart', function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
    slides.addEventListener('touchend', function (ev) {
      if (x0 === null) return;
      var dx = ev.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) go(dx < 0 ? cur + 1 : cur - 1);
    }, { passive: true });
    go(0);
  });
})();
