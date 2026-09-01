/* recruit-motion.js — 採用ページのスクロール演出（2026-09-01）
   リビールは IntersectionObserver、視差と進み具合バーは scroll ハンドラ直で回す。
   requestAnimationFrame は使わない（ヘッドレス検証で回らないため）。 */
(function () {
  'use strict';

  var reduce = window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function tag(el, kind, delay) {
    if (!el || el.hasAttribute('data-rv')) return;
    el.setAttribute('data-rv', kind);
    if (delay) el.style.setProperty('--rv-d', delay.toFixed(2) + 's');
  }
  function kids(sel, childSel) {
    var box = document.querySelector(sel);
    if (!box) return [];
    return Array.prototype.filter.call(box.children, function (c) {
      return !childSel || c.matches(childSel);
    });
  }
  function each(sel, fn) {
    Array.prototype.forEach.call(document.querySelectorAll(sel), fn);
  }

  /* ---------- 1. どの部品を、いつ動かすか ---------- */
  function assign() {
    each('.sec-head', function (h) {
      tag(h.querySelector('h2'), 'lead', 0);
      tag(h.querySelector('p'), 'part', 0.10);
    });

    each('.num-grid', function (grid) {
      Array.prototype.forEach.call(grid.children, function (card, i) {
        var b = i * 0.10;
        tag(card, 'part', b);
        tag(card.querySelector('.num'), 'part', b + 0.12);
        tag(card.querySelector('.label'), 'part', b + 0.20);
        tag(card.querySelector('.sub'), 'part', b + 0.26);
      });
    });

    each('.approach-grid, .job-grid', function (grid) {
      Array.prototype.forEach.call(grid.children, function (card, i) {
        var b = i * 0.09;
        tag(card, 'part', b);
        tag(card.querySelector('h3'), 'part', b + 0.08);
        tag(card.querySelector('p'), 'part', b + 0.14);
      });
    });

    each('.target-list', function (list) {
      Array.prototype.forEach.call(list.children, function (li, i) {
        var b = i * 0.08;
        tag(li, 'part', b);
        tag(li.querySelector('.step-badge'), 'tag', b + 0.04);
        tag(li.querySelector('.step-body'), 'part', b + 0.10);
      });
    });

    each('.ladder', function (lad) {
      Array.prototype.forEach.call(lad.children, function (row, i) {
        var b = i * 0.09;
        tag(row, 'part', b);
        tag(row.querySelector('.lr-stage'), 'tag', b + 0.04);
        tag(row.querySelector('.lr-body'), 'part', b + 0.08);
        tag(row.querySelector('.lr-pay'), 'pay', b + 0.18);
      });
    });

    each('.tl-list', function (list) {
      Array.prototype.forEach.call(list.children, function (row, i) {
        var b = i * 0.09;
        tag(row, 'part', b);
        tag(row.querySelector('.tl-min'), 'tag', b + 0.04);
        tag(row.children[1], 'part', b + 0.10);
      });
    });

    each('.chip-grid', function (grid) {
      Array.prototype.forEach.call(grid.children, function (c, i) {
        tag(c, 'chip', i * 0.06);
      });
    });

    each('.flow-row', function (row) {
      Array.prototype.forEach.call(row.children, function (n, i) {
        tag(n, 'part', i * 0.12);
      });
    });

    each('.fit-grid', function (grid) {
      Array.prototype.forEach.call(grid.children, function (col, i) {
        var b = i * 0.12;
        tag(col, 'part', b);
        tag(col.querySelector('h3'), 'part', b + 0.08);
        Array.prototype.forEach.call(col.querySelectorAll('li'), function (li, j) {
          tag(li, 'part', b + 0.14 + j * 0.06);
        });
      });
    });

    each('.band-note, .hours-table, .req-card, .approach-final, .sub-nav, .ladder-note', function (el) {
      tag(el, 'wide', 0);
    });

    /* ヒーローは折り返しの上にあるので、読み込み直後に順に出す */
    var hero = document.querySelector('.page-hero .hero-text');
    if (hero) {
      Array.prototype.forEach.call(hero.children, function (el, i) {
        tag(el, 'part', i * 0.09);
      });
    }
  }

  /* ---------- 2. 見えたら出す ---------- */
  function reveal() {
    var items = document.querySelectorAll('[data-rv]');
    if (reduce || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(items, function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
        if (e.target.classList.contains('num')) count(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0 });
    Array.prototype.forEach.call(items, function (el) { io.observe(el); });
  }

  /* ---------- 3. 数字を数え上げる ---------- */
  function count(el) {
    var node = el.firstChild;
    if (!node || node.nodeType !== 3) return;
    var raw = node.nodeValue.trim();
    var m = /^(\D*)([0-9]+(?:\.[0-9]+)?)$/.exec(raw);
    if (!m) return;
    var prefix = m[1], target = parseFloat(m[2]);
    var dec = (m[2].split('.')[1] || '').length;
    if (!(target > 0) || reduce) return;

    var dur = 900, t0 = Date.now();
    node.nodeValue = prefix + (0).toFixed(dec);
    var timer = setInterval(function () {
      var k = (Date.now() - t0) / dur;
      if (k >= 1) {
        clearInterval(timer);
        node.nodeValue = raw;
        return;
      }
      var e = 1 - Math.pow(1 - k, 3);
      node.nodeValue = prefix + (target * e).toFixed(dec);
    }, 16);
    setTimeout(function () { clearInterval(timer); node.nodeValue = raw; }, dur + 400);
  }

  /* ---------- 4. 視差と進み具合バー ---------- */
  function track() {
    var hero = document.querySelector('.page-hero');
    var bar = document.createElement('div');
    bar.className = 'rd-bar';
    bar.setAttribute('aria-hidden', 'true');
    bar.innerHTML = '<i></i>';
    document.body.appendChild(bar);
    var fill = bar.firstChild;

    function onScroll() {
      var de = document.documentElement;
      var max = de.scrollHeight - de.clientHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, de.scrollTop / max)) : 0;
      fill.style.width = (p * 100).toFixed(2) + '%';

      if (hero && !reduce) {
        var r = hero.getBoundingClientRect();
        if (r.bottom > 0 && r.top < de.clientHeight) {
          var shift = Math.max(-22, Math.min(22, -r.top * 0.08));
          hero.style.setProperty('--hero-shift', shift.toFixed(1) + 'px');
        }
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    onScroll();
  }

  function boot() { assign(); reveal(); track(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();
