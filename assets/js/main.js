// Ecommeem homepage interactions: mobile nav, scroll reveal, audit form.
(function () {
  'use strict';

  document.documentElement.classList.add('js');

  // ---- Mobile navigation ----
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  function setNav(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = open ? 'Close menu' : 'Open menu';
    nav.classList.toggle('is-open', open);
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    // Close after choosing a link or pressing Escape.
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

  // ---- Reveal sections on scroll ----
  var revealTargets = document.querySelectorAll(
    '.section-head, .case-card, .feature, .service, .step, .faq details, .stat'
  );
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    revealTargets.forEach(function (el) {
      el.classList.add('reveal');
      io.observe(el);
    });
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
