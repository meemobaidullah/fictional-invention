/* Google tag (GA4) for ecommeem.com
 * SETUP: paste your Measurement ID below (Google Analytics > Admin > Data streams > Web > "G-...").
 * While it still says G-XXXXXXXXXX nothing loads, so the site works without it.
 * Tracked automatically: page views, WhatsApp / call / email clicks, form leads, pricing orders, chat leads.
 */
(function () {
  var GA_ID = 'G-XXXXXXXXXX';
  if (!/^G-[A-Z0-9]{6,}$/.test(GA_ID) || GA_ID === 'G-XXXXXXXXXX') return;

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_ID);

  // Contact clicks (mark these as Key events in GA4 to count them as conversions)
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href');
    var ev = h.indexOf('wa.me') !== -1 ? 'whatsapp_click' : h.indexOf('tel:') === 0 ? 'call_click' :
             h.indexOf('mailto:') === 0 ? 'email_click' : h.indexOf('zoom.us') !== -1 ? 'booking_click' : null;
    if (ev) gtag('event', ev, { link_url: h, page_location: location.href });
  });

  // Leads fired by main.js after a successful send
  window.addEventListener('ecm:lead', function (e) {
    var d = e.detail || {};
    gtag('event', 'generate_lead', { lead_type: d.type || 'form', value: d.value || 0, currency: 'USD' });
  });
})();
