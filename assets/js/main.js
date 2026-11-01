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
        window.dispatchEvent(new CustomEvent('ecm:lead', { detail: { type: form.dataset.subject || 'form' } }));
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

/* Testimonials filter: show only reviews for the chosen service. */
(function () {
  var grid = document.querySelector('[data-tgrid]');
  if (!grid) return;
  var btns = document.querySelectorAll('[data-filter]');
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter');
      btns.forEach(function (x) { x.classList.toggle('is-active', x === b); x.setAttribute('aria-pressed', x === b); });
      grid.querySelectorAll('.t-card').forEach(function (c) { c.hidden = f !== 'all' && c.dataset.cat !== f; });
    });
  });
})();

/* Mega menu: hovering or focusing a platform shows its two service columns. */
(function () {
  var tabs = document.querySelectorAll('[data-mega]');
  if (!tabs.length) return;
  function show(key) {
    tabs.forEach(function (t) { t.classList.toggle('is-active', t.dataset.mega === key); });
    document.querySelectorAll('[data-mega-pane]').forEach(function (p) { p.hidden = p.dataset.megaPane !== key; });
  }
  tabs.forEach(function (t) {
    t.addEventListener('mouseenter', function () { show(t.dataset.mega); });
    t.addEventListener('focus', function () { show(t.dataset.mega); });
  });
})();

/* Pricing page: add services to an order, keep it in localStorage, send it by email (FormSubmit) or WhatsApp. */
(function () {
  var dataEl = document.getElementById('price-data');
  var cart = document.querySelector('[data-cart]');
  if (!dataEl || !cart) return;
  var ITEMS = JSON.parse(dataEl.textContent);
  var KEY = 'ecm-order';
  var WA = '8801731558195';
  var order = {};
  try { order = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { order = {}; }
  Object.keys(order).forEach(function (id) { if (!ITEMS[id]) delete order[id]; });

  var lines = cart.querySelector('[data-cart-lines]');
  var empty = cart.querySelector('[data-cart-empty]');
  var fab = document.querySelector('[data-cart-fab]');
  var form = cart.querySelector('[data-cart-form]');
  var note = form.querySelector('.form-note');
  var money = function (n) { return '$' + n.toLocaleString('en-US'); };

  function save() { try { localStorage.setItem(KEY, JSON.stringify(order)); } catch (e) { /* private mode */ } }
  function totals() {
    var m = 0, o = 0;
    Object.keys(order).forEach(function (id) { m += ITEMS[id].m * order[id]; o += ITEMS[id].o * order[id]; });
    return { m: m, o: o, due: m + o };
  }
  function priceText(it) {
    if (it.m && it.o) return money(it.m) + '/mo + ' + money(it.o) + ' setup';
    if (it.m) return money(it.m) + '/mo';
    return money(it.o) + ' ' + it.u.replace('from, ', '');
  }
  function summary() {
    var t = totals();
    var rows = Object.keys(order).map(function (id) {
      var it = ITEMS[id];
      return '- ' + it.n + (order[id] > 1 ? ' x' + order[id] : '') + ' (' + priceText(it) + ')';
    });
    rows.push('Monthly: ' + money(t.m) + ' | One-time: ' + money(t.o) + ' | Due to start: ' + money(t.due));
    return rows.join('\n');
  }

  function render() {
    var ids = Object.keys(order);
    lines.innerHTML = '';
    ids.forEach(function (id) {
      var it = ITEMS[id];
      var li = document.createElement('li');
      li.innerHTML = '<div><strong></strong><small></small></div>' +
        '<input class="cart-qty" type="number" min="1" max="99" aria-label="Quantity">' +
        '<button type="button" class="cart-rm" aria-label="Remove">&times;</button>';
      li.querySelector('strong').textContent = it.n;
      li.querySelector('small').textContent = priceText(it);
      var q = li.querySelector('.cart-qty');
      q.value = order[id];
      q.addEventListener('change', function () { order[id] = Math.min(99, Math.max(1, parseInt(q.value, 10) || 1)); save(); render(); });
      li.querySelector('.cart-rm').addEventListener('click', function () { delete order[id]; save(); render(); });
      lines.appendChild(li);
    });
    empty.hidden = ids.length > 0;
    var t = totals();
    cart.querySelector('[data-tot-m]').textContent = money(t.m);
    cart.querySelector('[data-tot-o]').textContent = money(t.o);
    cart.querySelector('[data-tot-due]').textContent = money(t.due);
    document.querySelectorAll('[data-add]').forEach(function (b) {
      var on = !!order[b.dataset.add];
      b.classList.toggle('is-added', on);
      b.setAttribute('aria-pressed', on);
      if (!b.dataset.label) b.dataset.label = b.textContent;
      b.textContent = on ? '✓ Added' : b.dataset.label;
    });
    if (fab) {
      fab.hidden = ids.length === 0;
      fab.querySelector('[data-fab-count]').textContent = ids.length;
      fab.querySelector('[data-fab-total]').textContent = money(t.due);
    }
  }

  document.querySelectorAll('[data-add]').forEach(function (b) {
    b.addEventListener('click', function () {
      var id = b.dataset.add;
      if (order[id]) delete order[id]; else order[id] = 1;
      save(); render();
    });
  });

  // Filters: search + category + billing type
  var grid = document.querySelector('[data-svc-grid]');
  var none = document.querySelector('[data-svc-empty]');
  var state = { q: '', cat: 'all', bill: 'all' };
  function filter() {
    var shown = 0;
    grid.querySelectorAll('.svc-card').forEach(function (c) {
      var ok = (state.cat === 'all' || c.dataset.cat === state.cat) &&
               (state.bill === 'all' || c.dataset.bill === state.bill) &&
               (!state.q || c.dataset.name.indexOf(state.q) !== -1);
      c.hidden = !ok;
      if (ok) shown++;
    });
    none.hidden = shown > 0;
  }
  function chipGroup(attr, key) {
    var btns = document.querySelectorAll('button[' + attr + ']');
    btns.forEach(function (b) {
      if (b.closest('.svc-card')) return;
      b.addEventListener('click', function () {
        btns.forEach(function (x) { x.classList.toggle('is-active', x === b); });
        state[key] = b.getAttribute(attr); filter();
      });
    });
  }
  chipGroup('data-cat', 'cat');
  chipGroup('data-bill', 'bill');
  var search = document.querySelector('[data-psearch]');
  search.addEventListener('input', function () { state.q = search.value.trim().toLowerCase(); filter(); });

  function setNote(text, type) {
    note.textContent = text;
    note.classList.remove('is-error', 'is-success');
    if (type) note.classList.add(type);
  }
  function check(needEmail) {
    if (!Object.keys(order).length) { setNote('Add at least one package or service first.', 'is-error'); return false; }
    var bad = null;
    ['name', 'email', 'store'].forEach(function (k) {
      var el = form.elements[k];
      if (k === 'email' && !needEmail) return;
      var ok = el.checkValidity() && (!el.required || el.value.trim() !== '');
      el.setAttribute('aria-invalid', ok ? 'false' : 'true');
      if (!ok && !bad) bad = el;
    });
    if (bad) { setNote('Please check the highlighted field.', 'is-error'); bad.focus(); return false; }
    setNote('');
    return true;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!check(true) || form.elements._honey.value) return;
    var t = totals();
    var data = {
      _subject: 'New order from pricing page: ' + money(t.due) + ' to start',
      _template: 'table',
      _replyto: form.elements.email.value.trim(),
      _autoresponse: "Thanks for your order with eCommeem! We'll reply within one business day with your scope and payment link. " +
        'Your order:\n' + summary() + '\nQuestions? WhatsApp +880 1731-558195 (https://wa.me/8801731558195).',
      name: form.elements.name.value.trim(),
      email: form.elements.email.value.trim(),
      whatsapp: form.elements.whatsapp.value.trim(),
      store: form.elements.store.value.trim(),
      notes: form.elements.notes.value.trim(),
      order: summary(),
      monthly_total: money(t.m),
      one_time_total: money(t.o),
      due_to_start: money(t.due),
      page: location.href
    };
    var btn = form.querySelector('[data-cart-submit]');
    btn.disabled = true;
    setNote('Sending your order…');
    fetch('https://formsubmit.co/ajax/ecommeem@gmail.com', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data)
    }).then(function (res) {
      if (!res.ok) throw new Error(res.status);
      setNote("Order sent! Check your inbox for a copy. We'll reply within one business day.", 'is-success');
      window.dispatchEvent(new CustomEvent('ecm:lead', { detail: { type: 'pricing_order', value: t.due } }));
      order = {}; save(); render(); form.reset();
    }).catch(function () {
      setNote('Sorry, that did not send. Use "Send Order on WhatsApp" or email ecommeem@gmail.com.', 'is-error');
    }).then(function () { btn.disabled = false; });
  });

  form.querySelector('[data-cart-wa]').addEventListener('click', function () {
    if (!check(false)) return;
    var who = [form.elements.name.value.trim(), form.elements.email.value.trim(), form.elements.store.value.trim()].filter(Boolean).join(' | ');
    var msg = 'Hi eCommeem, I would like to order:\n' + summary() + (who ? '\n\nMe: ' + who : '') +
      (form.elements.notes.value.trim() ? '\nNotes: ' + form.elements.notes.value.trim() : '');
    window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
  });

  render();
})();

/* Chat assistant: answers common questions from a small knowledge base and hands off to a human on WhatsApp or email. */
(function () {
  var panel = document.querySelector('[data-chat]');
  var openBtn = document.querySelector('[data-chat-open]');
  if (!panel || !openBtn) return;
  var log = panel.querySelector('[data-chat-log]');
  var form = panel.querySelector('[data-chat-form]');
  var input = form.querySelector('input');
  var WA = 'https://wa.me/8801731558195?text=';
  var transcript = [];
  var started = false;

  var link = function (href, text) { return '<a href="' + href + '"' + (href.indexOf('http') === 0 ? ' target="_blank" rel="noopener"' : '') + '>' + text + '</a>'; };
  // Each entry: keywords (any match) -> answer HTML and follow-up chips
  var KB = [
    { w: 0.4, k: ['price', 'pricing', 'cost', 'package', 'plan', 'how much', 'fee', 'dam', 'koto', 'taka', 'rate'],
      a: 'Our Amazon packages are <b>Starter Care $499/mo</b>, <b>Growth Booster $999/mo</b> and <b>Premium Seller Protection $1,999/mo</b>. Single services start at $99. You can pick services and send an order on our ' + link('/pricing', 'pricing page') + '.',
      q: ['PPC', 'Account suspended', 'Talk to a human'] },
    { k: ['ppc', 'ads', 'advertis', 'sponsored', 'acos', 'campaign'],
      a: 'PPC &amp; advertising management is <b>$499/month</b>. We build and tune Sponsored Products, Brands and Display campaigns weekly against your ACoS target. More: ' + link('/amazon-ppc-management', 'Amazon PPC management') + '.',
      q: ['Free audit', 'Pricing', 'Talk to a human'] },
    { k: ['suspend', 'reinstat', 'appeal', 'deactivat', 'banned', 'blocked', 'plan of action', 'poa'],
      a: 'Sorry to hear that. Account reinstatement is <b>$2,500 per case</b> and we work on it 24/7: root-cause review, Plan of Action and appeal. For an urgent case, message us now on ' + link(WA + encodeURIComponent('Hi eCommeem, my account is suspended and I need help.'), 'WhatsApp') + '. Details: ' + link('/amazon-account-reinstatement', 'reinstatement service') + '.',
      q: ['Talk to a human', 'Pricing'] },
    { k: ['listing', 'seo', 'keyword', 'title', 'bullet', 'optimi'],
      a: 'Listing creation &amp; SEO is <b>$250 per listing</b>: keyword research, title, bullets, description and backend terms. See ' + link('/amazon-listing-optimization', 'listing optimization') + '.',
      q: ['A+ Content', 'Pricing'] },
    { k: ['a+', 'aplus', 'storefront', 'brand store', 'brand registry', 'trademark', 'hijack'],
      a: 'A+ Content &amp; Storefront design is <b>$249 one-time</b>. Brand Registry &amp; Brand Protection starts at <b>$799 one-time</b>. See ' + link('/amazon-brand-management-services', 'brand management') + '.',
      q: ['Pricing', 'Free audit'] },
    { k: ['walmart', 'wfs'],
      a: 'Walmart Marketplace account management is <b>$1,200/month + $1,200 setup</b>, covering catalog, WFS and Sponsored Products. See ' + link('/walmart-marketplace-management', 'Walmart management') + '.',
      q: ['Pricing', 'Talk to a human'] },
    { k: ['tiktok'], a: 'Yes, we set up and manage TikTok Shop: catalog, affiliates and ads. See ' + link('/tiktok-shop-management', 'TikTok Shop management') + '.', q: ['Pricing', 'Talk to a human'] },
    { k: ['temu'], a: 'We help sellers launch and grow on Temu. See ' + link('/temu-seller-management', 'Temu seller management') + '.', q: ['Pricing', 'Talk to a human'] },
    { k: ['ebay'], a: 'We manage eBay stores end to end. See ' + link('/ebay-store-management', 'eBay store management') + '.', q: ['Pricing'] },
    { k: ['etsy'], a: 'We run Etsy shops: listings, SEO and ads. See ' + link('/etsy-store-management', 'Etsy store management') + '.', q: ['Pricing'] },
    { k: ['mercari'], a: 'We handle Mercari setup, listings and smart pricing. See ' + link('/mercari-seller-management', 'Mercari seller management') + '.', q: ['Talk to a human'] },
    { k: ['shopify', 'woocommerce', 'ecommerce store'], a: 'A full ecommerce store build starts at <b>$2,499 one-time</b>. See ' + link('/shopify-store-management', 'Shopify management') + '.', q: ['Website', 'Pricing'] },
    { k: ['website', 'web site', 'web dev', 'landing'], a: 'Website development starts at <b>$799 one-time</b>; SEO is $499/month. See ' + link('/website-development', 'website development') + '.', q: ['App', 'Pricing'] },
    { k: ['app', 'android', 'ios', 'mobile'], a: 'We build mobile apps for stores and brands. Tell us your idea and we will quote it: ' + link('/app-development', 'app development') + '.', q: ['Get a quote'] },
    { k: ['audit', 'free', 'review my store', 'check my store'], a: 'Our store audit is free. Share your store link and we send a short report with quick wins: ' + link('/free-amazon-audit', 'get a free audit') + '.', q: ['Book a call'] },
    { k: ['call', 'meeting', 'consult', 'book', 'zoom', 'schedule'], a: 'You can book a free 30-minute call with Meem here: ' + link('/book-a-consultation', 'book a consultation') + '.', q: ['Talk to a human'] },
    { k: ['quote', 'proposal', 'custom'], a: 'For a custom plan, use ' + link('/get-a-quote', 'Get a Quote') + ' or ' + link('/request-a-proposal', 'Request a Proposal') + '. We reply within one business day.', q: ['Talk to a human'] },
    { k: ['pay', 'payment', 'invoice', 'payoneer', 'card', 'bank'], a: 'We send an invoice after agreeing the scope. You can pay by bank transfer, card or Payoneer. Monthly plans are billed at the start of each month.', q: ['Pricing'] },
    { k: ['cancel', 'contract', 'refund', 'commit'], a: 'Monthly plans have no long-term contract. You can cancel at the end of any billing cycle.', q: ['Pricing'] },
    { k: ['review', 'testimonial', 'result', 'case stud', 'proof', 'client'], a: 'We have managed 266+ stores. Read what clients say on our ' + link('/testimonials', 'testimonials page') + '.', q: ['Free audit'] },
    { k: ['who', 'about', 'meem', 'team', 'where', 'location', 'bangladesh', 'founder'], a: 'eCommeem is a remote ecommerce agency led by Meem Obaidullah, serving sellers worldwide. More on our ' + link('/about', 'about page') + '.', q: ['Book a call'] },
    { k: ['human', 'agent', 'person', 'talk', 'whatsapp', 'contact', 'email', 'phone', 'support', 'help'],
      a: 'Happy to connect you with the team. ' + link(WA + encodeURIComponent('Hi eCommeem, I came from your website chat.'), 'Chat on WhatsApp') + ' (fastest), email ' + link('mailto:ecommeem@gmail.com', 'ecommeem@gmail.com') + ', or type your email here and we will write back.',
      q: [] },
    { k: ['hi', 'hello', 'hey', 'salam', 'assalam', 'hlw'], a: 'Hi! How can I help with your store today?', q: ['Pricing', 'PPC', 'Account suspended', 'Free audit'] }
  ];
  var CHIP = { 'Pricing': 'pricing', 'PPC': 'ppc', 'Account suspended': 'suspended', 'Talk to a human': 'talk to a human', 'Free audit': 'free audit',
    'A+ Content': 'aplus storefront', 'Website': 'website', 'App': 'app', 'Get a quote': 'quote', 'Book a call': 'book a call' };

  function add(html, who, chips) {
    log.querySelectorAll('.chat-quick').forEach(function (r) { r.remove(); });
    var div = document.createElement('div');
    div.className = 'chat-msg ' + who;
    if (who === 'me') div.textContent = html; else div.innerHTML = html;
    log.appendChild(div);
    transcript.push((who === 'me' ? 'Visitor: ' : 'Bot: ') + div.textContent);
    if (chips && chips.length) {
      var row = document.createElement('div');
      row.className = 'chat-quick';
      chips.forEach(function (c) {
        var b = document.createElement('button');
        b.type = 'button'; b.textContent = c;
        b.addEventListener('click', function () { row.remove(); ask(c, CHIP[c] || c); });
        row.appendChild(b);
      });
      log.appendChild(row);
    }
    log.scrollTop = log.scrollHeight;
  }

  function answer(text) {
    var t = ' ' + text.toLowerCase() + ' ';
    var email = text.match(/[^\s@]+@[^\s@]+\.[^\s@]+/);
    if (email) {
      fetch('https://formsubmit.co/ajax/ecommeem@gmail.com', {
        method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ _subject: 'Website chat lead', _template: 'table', email: email[0], _replyto: email[0], page: location.href, chat: transcript.join('\n') })
      }).then(function () { window.dispatchEvent(new CustomEvent('ecm:lead', { detail: { type: 'chat' } })); }).catch(function () {});
      return { a: 'Thanks! We have your email (' + email[0].replace(/</g, '') + ') and the team will reply soon. For a faster answer, ' + link(WA + encodeURIComponent('Hi eCommeem, I just left my email in the website chat.'), 'message us on WhatsApp') + '.', q: [] };
    }
    var best = null, score = 0;
    KB.forEach(function (e) {
      var s = 0;
      e.k.forEach(function (k) { if (k.length <= 3 ? new RegExp('\\b' + k.replace('+', '\\+') + '\\b').test(t) : t.indexOf(k) !== -1) s += k.length; });
      s *= e.w || 1;
      if (s > score) { score = s; best = e; }
    });
    if (best) return best;
    return { a: "I'm not sure about that one, but a real person can help. " + link(WA + encodeURIComponent('Hi eCommeem, question from your website: ' + text), 'Ask the team on WhatsApp') + ' or leave your email here.', q: ['Pricing', 'Talk to a human'] };
  }

  function ask(shown, query) {
    add(shown, 'me');
    var typing = document.createElement('div');
    typing.className = 'chat-typing'; typing.textContent = 'Assistant is typing…';
    log.appendChild(typing); log.scrollTop = log.scrollHeight;
    setTimeout(function () { typing.remove(); var r = answer(query || shown); add(r.a, 'bot', r.q); }, 450);
  }

  function toggle(open) {
    panel.hidden = !open;
    openBtn.setAttribute('aria-expanded', open);
    if (open && !started) {
      started = true;
      add('Hi, I\'m the eCommeem assistant. Ask me about pricing, PPC, suspensions, listings or any marketplace. A human is one tap away on WhatsApp.', 'bot',
          ['Pricing', 'PPC', 'Account suspended', 'Free audit', 'Talk to a human']);
    }
    if (open) input.focus();
  }
  openBtn.addEventListener('click', function () { toggle(panel.hidden); });
  panel.querySelector('[data-chat-close]').addEventListener('click', function () { toggle(false); openBtn.focus(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { toggle(false); openBtn.focus(); } });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value.trim();
    if (!v) return;
    input.value = '';
    ask(v);
  });
})();
