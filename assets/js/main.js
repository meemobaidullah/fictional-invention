// Ecommeem homepage interactions: mobile nav, case-study slider,
// workflow tabs, FAQ accordion + load more, audit form.
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Mobile navigation ----
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  function setNav(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = open ? 'Close menu' : 'Open menu';
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  }

  // Submenus: accordion on mobile, click/keyboard fallback for hover on desktop.
  var menuBtns = document.querySelectorAll('.menu-btn');
  menuBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      menuBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.menu-item')) {
      menuBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    }
  });

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setNav(false);
        toggle.focus();
      }
    });
  }

  // ---- Case study slider (native scroll-snap + arrow buttons + dots) ----
  document.querySelectorAll('[data-slider]').forEach(function (slider) {
    var track = slider.querySelector('[data-track]');
    var slides = Array.prototype.slice.call(track.children);
    var dotsWrap = slider.querySelector('[data-dots]');
    var current = 0;

    var dots = slides.map(function (_, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Go to case study ' + (i + 1));
      b.addEventListener('click', function () { go(i); });
      dotsWrap.appendChild(b);
      return b;
    });

    function go(i) {
      current = (i + slides.length) % slides.length;
      track.scrollTo({ left: slides[current].offsetLeft - track.offsetLeft, behavior: reduceMotion ? 'auto' : 'smooth' });
      mark();
    }

    function mark() {
      dots.forEach(function (d, i) { d.setAttribute('aria-current', i === current ? 'true' : 'false'); });
    }

    // Keep dots in sync when the user swipes.
    var t;
    track.addEventListener('scroll', function () {
      clearTimeout(t);
      t = setTimeout(function () {
        current = Math.round(track.scrollLeft / track.clientWidth);
        mark();
      }, 80);
    });

    slider.querySelector('[data-prev]').addEventListener('click', function () { go(current - 1); });
    slider.querySelector('[data-next]').addEventListener('click', function () { go(current + 1); });
    mark();
  });

  // ---- Workflow tabs (auto-advance until the visitor interacts) ----
  document.querySelectorAll('[data-tabs]').forEach(function (wrap) {
    var tabs = Array.prototype.slice.call(wrap.querySelectorAll('[role="tab"]'));
    var arts = wrap.querySelectorAll('.wf-art');
    var count = wrap.querySelector('[data-count]');
    var timer = null;

    function show(i) {
      tabs.forEach(function (tab, n) {
        var on = n === i;
        tab.classList.toggle('is-active', on);
        tab.setAttribute('aria-selected', String(on));
        tab.tabIndex = on ? 0 : -1;
        arts[n].classList.toggle('is-active', on);
      });
      count.textContent = String(i + 1).padStart(2, '0');
    }

    function stop() { clearInterval(timer); timer = null; }

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { stop(); show(i); });
      tab.addEventListener('keydown', function (e) {
        var dir = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
        if (!dir) return;
        e.preventDefault();
        stop();
        var next = (i + dir + tabs.length) % tabs.length;
        show(next);
        tabs[next].focus();
      });
    });

    show(0);
    if (!reduceMotion) {
      var step = 0;
      timer = setInterval(function () { step = (step + 1) % tabs.length; show(step); }, 6000);
    }
  });

  // ---- FAQ: one open at a time + load more ----
  var faq = document.querySelector('[data-faq]');
  if (faq) {
    var items = faq.querySelectorAll('details');
    items.forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (!d.open) return;
        items.forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
    var more = faq.querySelector('[data-load-more]');
    if (more) {
      more.addEventListener('click', function () {
        faq.querySelectorAll('.faq-more').forEach(function (el) { el.hidden = false; });
        more.hidden = true;
      });
    }
  }

  // ---- Audit form (client-side validation; wire to a backend before launch) ----
  var form = document.querySelector('.audit-form');
  if (form) {
    var note = form.querySelector('.form-note');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var invalid = null;
      ['f-name', 'f-email', 'f-store'].forEach(function (id) {
        var input = document.getElementById(id);
        var ok = input.checkValidity() && (!input.required || input.value.trim() !== '');
        input.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !invalid) invalid = input;
      });

      note.classList.remove('is-error', 'is-success');
      if (invalid) {
        note.textContent = 'Please check the highlighted field.';
        note.classList.add('is-error');
        invalid.focus();
        return;
      }

      // TODO: replace with fetch() to your form endpoint.
      note.textContent = "Thanks! We'll be in touch with your audit shortly.";
      note.classList.add('is-success');
      form.reset();
    });
  }

  // ---- Footer year ----
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
