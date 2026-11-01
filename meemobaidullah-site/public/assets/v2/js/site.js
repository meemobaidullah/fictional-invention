/* meemobaidullah.com — small, dependency-free behaviour layer.
   Theme is set inline in <head> before paint; this file wires the switch,
   the mobile menu, the Services dropdown, scroll reveal and the contact form. */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');

  // ---- Dark / light switch ----
  var themeBtn = document.querySelector('.theme-toggle');
  function currentTheme() {
    return root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }
  function syncThemeBtn() {
    if (!themeBtn) return;
    var dark = currentTheme() === 'dark';
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    themeBtn.setAttribute('aria-pressed', dark ? 'true' : 'false');
  }
  if (themeBtn) {
    syncThemeBtn();
    themeBtn.addEventListener('click', function () {
      root.dataset.theme = currentTheme() === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', root.dataset.theme); } catch (e) { /* private mode */ }
      syncThemeBtn();
    });
  }

  // ---- Mobile menu ----
  var body = document.body;
  var openBtn = document.querySelector('.nav-toggle');
  var closeBtn = document.querySelector('.nav-close');
  var scrim = document.querySelector('.nav-scrim');
  function setNav(open) {
    body.classList.toggle('nav-open', open);
    if (openBtn) openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open && closeBtn) closeBtn.focus();
    if (!open && openBtn) openBtn.focus();
  }
  if (openBtn) openBtn.addEventListener('click', function () { setNav(true); });
  if (closeBtn) closeBtn.addEventListener('click', function () { setNav(false); });
  if (scrim) scrim.addEventListener('click', function () { setNav(false); });

  // ---- Services dropdown (click on all sizes, hover-friendly on desktop) ----
  var menuBtns = document.querySelectorAll('.menu-btn');
  function closeMenus(except) {
    menuBtns.forEach(function (b) { if (b !== except) b.setAttribute('aria-expanded', 'false'); });
  }
  menuBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = btn.getAttribute('aria-expanded') === 'true';
      closeMenus(btn);
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.menu-item')) closeMenus();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    closeMenus();
    if (body.classList.contains('nav-open')) setNav(false);
  });

  // ---- Reveal on scroll ----
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  // ---- Contact form ----
  // Posts to the Formspree endpoint in data-endpoint. With no endpoint set,
  // it opens the visitor's email app with the brief filled in instead.
  var form = document.querySelector('form[data-contact]');
  if (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var endpoint = form.dataset.endpoint;
      var data = new FormData(form);
      if (!endpoint) {
        var lines = [];
        data.forEach(function (v, k) { if (k.charAt(0) !== '_') lines.push(k + ': ' + v); });
        window.location.href = 'mailto:' + form.dataset.email +
          '?subject=' + encodeURIComponent('Venture brief from ' + (data.get('name') || 'website')) +
          '&body=' + encodeURIComponent(lines.join('\n'));
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      status.className = 'form-status';
      status.textContent = 'Sending…';
      fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); })
        .then(function () {
          form.reset();
          status.className = 'form-status ok';
          status.textContent = 'Thanks — your brief is in my inbox. I\'ll reply directly.';
        })
        .catch(function () {
          status.className = 'form-status err';
          status.textContent = 'Could not send right now. Please use WhatsApp or email instead.';
        })
        .finally(function () { btn.disabled = false; });
    });
  }
})();
