// Ecommeem homepage interactions: mobile nav, case-study slider,
// workflow tabs, FAQ accordion + load more, stepped audit forms.
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

  // ---- Stepped audit forms: checklist -> store -> contact, sent to ecommeem@gmail.com via FormSubmit ----
  var FORM_ENDPOINT = 'https://formsubmit.co/ajax/ecommeem@gmail.com';
  document.querySelectorAll('.step-form').forEach(function (form) {
    var steps = form.querySelectorAll('[data-fstep]');
    var dots = form.querySelectorAll('.step-dots li');
    var num = form.querySelector('[data-step-num]');
    var back = form.querySelector('[data-back]');
    var next = form.querySelector('[data-next]');
    var submit = form.querySelector('[data-submit]');
    var note = form.querySelector('.form-note');
    var current = 0;

    function show(i) {
      current = i;
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      dots.forEach(function (d, k) { d.classList.toggle('on', k <= i); });
      num.textContent = i + 1;
      back.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      submit.hidden = i !== steps.length - 1;
    }

    function setNote(text, type) {
      note.textContent = text;
      note.classList.remove('is-error', 'is-success');
      if (type) note.classList.add(type);
    }

    // Returns true when the visible step is complete; marks what's missing.
    function valid(i) {
      var step = steps[i];
      var grid = step.querySelector('.check-grid');
      if (grid) {
        var ticked = grid.querySelector('input:checked');
        grid.classList.toggle('is-invalid', !ticked);
        if (!ticked) { setNote('Tick at least one option to continue.', 'is-error'); return false; }
      }
      var bad = null;
      step.querySelectorAll('input:not([type=checkbox])').forEach(function (input) {
        var ok = input.checkValidity() && (!input.required || input.value.trim() !== '');
        input.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !bad) bad = input;
      });
      if (bad) { setNote('Please check the highlighted field.', 'is-error'); bad.focus(); return false; }
      setNote('');
      return true;
    }

    next.addEventListener('click', function () { if (valid(current)) show(current + 1); });
    back.addEventListener('click', function () { setNote(''); show(current - 1); });
    form.addEventListener('change', function (e) {
      if (e.target.type === 'checkbox') e.target.closest('.check-grid').classList.remove('is-invalid');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!valid(current)) return;
      if (form.elements._honey.value) return; // bot

      var data = {
        _subject: form.dataset.subject,
        _template: 'table',
        page: location.href,
        services: Array.prototype.map.call(form.querySelectorAll('input[name=services]:checked'), function (c) { return c.value; }).join(', ')
      };
      ['marketplace', 'store', 'name', 'email', 'whatsapp'].forEach(function (k) {
        if (form.elements[k]) data[k] = form.elements[k].value.trim();
      });
      data._replyto = data.email;
      // Instant confirmation to the visitor, so nobody is left wondering if the message arrived.
      data._autoresponse = "Thanks for contacting eCommeem! We've received your request and a team member will reply soon. " +
        'For a faster answer, WhatsApp us at +880 1731-558195 (https://wa.me/8801731558195).';

      submit.disabled = true;
      setNote('Sending…');
      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data)
      }).then(function (res) {
        if (!res.ok) throw new Error(res.status);
        setNote("Thanks! We've got your request and will reply by email soon.", 'is-success');
        form.reset();
        show(0);
      }).catch(function () {
        setNote('Sorry, that did not send. Please email ecommeem@gmail.com or WhatsApp +880 1731-558195.', 'is-error');
      }).then(function () { submit.disabled = false; });
    });

    show(0);
  });

  // ---- Dark / light mode switch (initial theme is set inline in <head>) ----
  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    var root = document.documentElement;
    var label = function () {
      var dark = root.dataset.theme === 'dark';
      themeBtn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      themeBtn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    };
    themeBtn.addEventListener('click', function () {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', root.dataset.theme); } catch (e) { /* private mode: not remembered */ }
      label();
    });
    label();
  }

  // ---- Footer year ----
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
