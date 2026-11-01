#!/usr/bin/env python3
"""Build meemobaidullah.com into ../public.

Every URL from the live sitemap is kept exactly (folder + index.html), with the
same <title>, meta description, canonical and robots value as the live page.
Content lives in tools/content.py; this file only holds the layout.

    python3 tools/build.py          # writes public/
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'public'))
SITE = 'https://meemobaidullah.com'
ASSET_VER = '1'
e = html.escape


# ---------------------------------------------------------------- icons
ICON_PATHS = {
    'search':  '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/><path d="m8 12 2-2 2 2 3-3"/>',
    'sliders': '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    'box':     '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    'trend':   '<path d="M3 17 9 11l4 4 8-8"/><path d="M15 7h6v6"/>',
    'cart':    '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11.5L21 7H6"/>',
    'video':   '<rect x="2" y="5" width="15" height="14" rx="2"/><path d="m17 10 5-3v10l-5-3"/>',
    'tag':     '<path d="M20 12 12 20 3 11V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    'store':   '<path d="M3 9 5 4h14l2 5"/><path d="M4 9v11h16V9"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M10 20v-5h4v5"/>',
    'hand':    '<path d="M7 11V6a2 2 0 0 1 4 0v4"/><path d="M11 10V4a2 2 0 0 1 4 0v6"/><path d="M15 10V6a2 2 0 0 1 4 0v8a7 7 0 0 1-7 7h-1a7 7 0 0 1-6-3.4L3 14a2 2 0 0 1 3.4-2L7 13"/>',
    'bag':     '<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    'shield':  '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    'play':    '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="m10 9 5 3-5 3z"/>',
    'award':   '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-3 5 3-1.5-7"/>',
    'globe':   '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    'layers':  '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    'target':  '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    'zap':     '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    'growth':  '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'chat':    '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    'mail':    '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'phone':   '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    'grid':    '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    'flow':    '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7 6h10M6 8l5 8M18 8l-5 8"/>',
    'users':   '<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M22 20a7 7 0 0 0-4-6.3"/>',
}
WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z"/></svg>')


def icon(name):
    return ('<span class="icon-tile" aria-hidden="true"><svg viewBox="0 0 24 24">%s</svg></span>'
            % ICON_PATHS[name])


# ---------------------------------------------------------------- chrome
def services_menu(current):
    items = []
    for s in C.SERVICES:
        href = '/%s/' % s['slug']
        cur = ' aria-current="page"' if current == href else ''
        items.append('<li><a href="%s"%s>%s</a></li>' % (href, cur, e(s['nav'])))
    return ''.join(items)


def header(current):
    def link(href, label):
        cur = ' aria-current="page"' if current == href else ''
        return '<li><a href="%s"%s>%s</a></li>' % (href, cur, label)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="container"><span class="dot" aria-hidden="true"></span><span>Need a full agency team? <a href="{C.AGENCY_URL}" target="_blank" rel="noopener">Visit eCommeem.com →</a></span></div></div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="Meem Obaidullah home">
      <span class="brand-mark" aria-hidden="true">MO</span>
      <span class="brand-text"><span class="brand-name">Meem Obaidullah</span><span class="brand-tag">eCommerce Specialist</span></span>
    </a>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <button class="icon-btn nav-close" type="button" aria-label="Close menu"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
      <ul class="menu">
        {link('/', 'Home')}
        {link('/about/', 'About')}
        <li class="menu-item"><button class="menu-btn" type="button" aria-expanded="false">Services <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
          <ul class="submenu">{services_menu(current)}</ul></li>
        {link('/blog/', 'Blog')}
        {link('/case-stady/', 'Case Studies')}
        {link('/sucess/', 'Success')}
        {link('/contact/', 'Contact')}
      </ul>
      <div class="nav-extra">
        <a class="btn btn-wa" href="{C.WA}" target="_blank" rel="noopener">{WA_SVG} Start a Conversation</a>
        <a class="btn btn-ghost" href="{C.AGENCY_URL}" target="_blank" rel="noopener">eCommeem.com agency ↗</a>
      </div>
    </nav>
    <button class="icon-btn theme-toggle" type="button" aria-label="Switch colour theme">
      <svg class="i-moon" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      <svg class="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
    <a class="btn btn-primary btn-sm header-cta" href="{C.WA}" target="_blank" rel="noopener">Start a Conversation</a>
    <button class="icon-btn nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>
<div class="nav-scrim" aria-hidden="true"></div>'''


def footer():
    svc = ''.join('<li><a href="/%s/">%s</a></li>' % (s['slug'], e(s['nav'])) for s in C.SERVICES)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="/" aria-label="Meem Obaidullah home"><span class="brand-mark" aria-hidden="true">MO</span><span class="brand-text"><span class="brand-name">Meem Obaidullah</span><span class="brand-tag">eCommerce Specialist</span></span></a>
        <p>Meem Obaidullah · E-commerce Operations &amp; Automation</p>
        <div class="btn-row"><a class="btn btn-wa btn-sm" href="{C.WA}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a></div>
      </div>
      <div><h3>Services</h3><ul>{svc}</ul></div>
      <div><h3>Explore</h3><ul>
        <li><a href="/">Home</a></li><li><a href="/about/">About</a></li><li><a href="/blog/">Blog</a></li>
        <li><a href="/case-stady/">Case Studies</a></li><li><a href="/sucess/">Success</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div><h3>Agency</h3><ul>
        <li><a href="{C.AGENCY_URL}" target="_blank" rel="noopener">eCommeem.com</a></li>
        <li><a href="{C.EMAIL_HREF}">{C.EMAIL}</a></li>
        <li><a href="{C.LIVE_CHAT}" target="_blank" rel="noopener">Live Consultation</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 Mo Entrepreneurs. All rights reserved.</span><span><a href="/about/">About</a> · <a href="/contact/">Contact</a></span></div>
  </div>
</footer>
<a class="wa-float" href="{C.WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_SVG}<span>Chat on WhatsApp</span></a>'''


def page(p, body, current, crumbs=None, extra_ld=None):
    """Wrap body in the full document with head meta carried over from the live page."""
    url = SITE + p['path']
    og_img = p.get('og_image') or C.DEFAULT_OG
    ld = [
        {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Meem Obaidullah', 'url': SITE + '/'},
    ]
    if crumbs:
        ld.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + h} for i, (n, h) in enumerate(crumbs)]})
    if extra_ld:
        ld.extend(extra_ld)
    ld_html = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in ld)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<meta name="robots" content="{p.get('robots', 'index, follow')}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{p.get('og_type', 'website')}">
<meta property="og:site_name" content="Meem Obaidullah | eCom Entrepreneurs">
<meta property="og:title" content="{e(p.get('og_title', p['title']))}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(p.get('og_title', p['title']))}">
<meta name="twitter:description" content="{e(p['desc'])}">
<meta name="twitter:image" content="{SITE}{og_img}">
<meta name="theme-color" content="#FBF8F3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B121C" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/v2/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/v2/css/site.css?v={ASSET_VER}">
{ld_html}</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/v2/js/site.js?v={ASSET_VER}" defer></script>
</body>
</html>
'''


def crumbs_html(crumbs):
    out = []
    for i, (name, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            out.append('<li aria-current="page">%s</li>' % e(name))
        else:
            out.append('<li><a href="%s">%s</a></li>' % (href, e(name)))
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">%s</ol></nav>' % ''.join(out)


def cta_block(heading, text=None, buttons=None):
    buttons = buttons or [('Let\'s Talk Investment Scope ↗', '/contact/', 'btn-primary')]
    btns = ''.join('<a class="btn %s" href="%s"%s>%s</a>' % (
        cls, href, ' target="_blank" rel="noopener"' if href.startswith('http') else '', e(lbl)) for lbl, href, cls in buttons)
    para = '<p>%s</p>' % e(text) if text else ''
    return f'''<section class="section"><div class="container"><div class="cta reveal">
  <div><h2>{e(heading)}</h2>{para}</div><div class="btn-row">{btns}</div></div></div></section>'''


def agency_block():
    return f'''<section class="section" style="padding-top:0"><div class="container"><div class="card agency reveal">
  <div class="agency-name">eCom<span>meem</span>.com</div>
  <div><h3>{e(C.AGENCY_HEAD)}</h3><p>{e(C.AGENCY_TEXT)}</p></div>
  <a class="btn btn-ghost" href="{C.AGENCY_URL}" target="_blank" rel="noopener">Visit eCommeem.com ↗</a>
</div></div></section>'''


def steps_block(intro, band=True):
    steps = ''.join(f'''<li class="step reveal"><span class="card-num">STEP 0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'''
                    for i, (t, d) in enumerate(C.STEPS))
    cls = 'section band' if band else 'section'
    return f'''<section class="{cls}"><div class="container">
  <div class="section-head"><span class="eyebrow">Work Process</span><h2>A Simple, Hands-Off Process</h2><p class="lead">{e(intro)}</p></div>
  <ol class="grid grid-4 steps">{steps}</ol></div></section>'''


def service_cards(slugs):
    out = []
    for slug in slugs:
        s = C.SERVICE_BY_SLUG[slug]
        out.append(f'''<article class="card is-link reveal">{icon(s['icon'])}<h3>{e(s['h1'])}</h3><p>{e(s['desc'])}</p>
<a class="more" href="/{slug}/">Learn More ↗</a></article>''')
    return ''.join(out)


# ---------------------------------------------------------------- pages
def build_home():
    p = C.HOME
    h = p['hero']
    chips = ''.join('<li class="chip">%s</li>' % e(x) for x in h['platforms'])
    services = ''.join(f'''<article class="card is-link reveal">{icon(s['icon'])}<span class="card-num">{s['num']}</span>
<h3>{e(s['title'])}</h3><p>{e(s['text'])}</p><a class="more" href="{s['href']}">{e(s['btn'])}</a></article>''' for s in p['services'])
    features = ''.join(f'''<article class="card reveal">{icon(f['icon'])}<h3>{e(f['title'])}</h3><p>{e(f['text'])}</p></article>''' for f in p['assets']['features'])
    channels = ''.join(f'''<li class="channel"><span><small>CHANNEL</small><strong>{e(n)}</strong></span><span class="status">{e(s)}</span></li>''' for n, s in p['assets']['channels'])
    tabs = ''.join('<li class="chip">%s</li>' % e(t) for t in p['assets']['tabs'])
    gallery = ''.join(f'''<figure class="reveal"><img src="{src}" alt="{e(alt)}" loading="lazy" width="800" height="600"><figcaption>{e(alt)}</figcaption></figure>''' for src, alt in p['work']['images'])
    body = f'''
<section class="hero"><div class="container hero-grid">
  <div class="hero-copy">
    <span class="badge"><span class="pulse" aria-hidden="true"></span>{e(h['badge'])}</span>
    <h1>{h['h1_html']}</h1>
    <p class="lead">{e(h['text'])}</p>
    <div class="btn-row">
      <a class="btn btn-wa" href="{C.WA}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a>
      <a class="btn btn-primary" href="/contact/">Meet With MO</a>
      <a class="btn btn-ghost" href="{C.LIVE_CHAT}" target="_blank" rel="noopener">Live Consultation</a>
    </div>
    <div class="hero-stats">{''.join('<div><strong>%s</strong><span>%s</span></div>' % (e(a), e(b)) for a, b in h['stats'])}</div>
    <ul class="platform-row" aria-label="Marketplaces">{chips}</ul>
  </div>
  <div class="portrait">
    <img src="/assets/v2/img/meem-obaidullah.jpg" alt="Meem Obaidullah — E-commerce Entrepreneur" width="800" height="800" fetchpriority="high">
    <div class="portrait-card"><span class="brand-mark" aria-hidden="true">MO</span><div><strong>Meem Obaidullah</strong><span>Top-Rated · Active Status</span></div></div>
  </div>
</div></section>

{steps_block(p['process_intro'])}

<section class="section"><div class="container split">
  <div class="prose reveal"><span class="eyebrow">01 / Freelancing Profile</span><h2>Elite Global Freelancer Credentials</h2>
    <p class="lead">{e(p['credentials'])}</p>
    <div class="btn-row"><a class="btn btn-primary" href="/about/">More About Meem</a></div></div>
  <div class="stats reveal">{''.join('<div class="stat"><strong>%s</strong><span>%s</span></div>' % (e(a), e(b)) for a, b in p['cred_stats'])}</div>
</div></section>

<section class="section" id="services" style="padding-top:0"><div class="container">
  <div class="section-head"><span class="eyebrow">02 / Services</span><h2>Our E-Commerce Services &amp; Management</h2>
    <p class="lead">End-to-End Automation, Store Management &amp; Virtual Assistant Solutions</p></div>
  <div class="grid grid-4">{services}</div>
</div></section>

<section class="section band"><div class="container">
  <div class="section-head"><span class="eyebrow">03 / Asset Management</span><h2>Hands-Free Digital Assets for Global Investors</h2>
    <p class="lead">{e(p['assets']['intro'])}</p><ul class="platform-row">{tabs}</ul></div>
  <div class="grid grid-4">{features}</div>
  <ul class="channels" style="margin-top:28px">{channels}</ul>
  <div class="card reveal" style="margin-top:28px"><span class="card-num">01</span><h3>Live Strategy &amp; Venture Brief</h3>
    <p>{e(p['assets']['brief'])}</p><div class="btn-row"><a class="btn btn-primary" href="/contact/">Start Brief</a></div></div>
</div></section>

<section class="section" id="proof"><div class="container">
  <div class="section-head"><span class="eyebrow">Track Record</span><h2>Selected Work &amp; Store Results</h2><p class="lead">{e(p['work']['intro'])}</p></div>
  <div class="gallery">{gallery}</div>
  <p class="form-note" style="margin-top:18px">{e(p['work']['note'])}</p>
  <div class="btn-row" style="margin-top:18px"><a class="btn btn-ghost" href="/case-stady/">View Case Studies</a></div>
</div></section>

{agency_block()}
'''
    person = {'@context': 'https://schema.org', '@type': 'Person', 'name': 'Meem Obaidullah', 'url': SITE + '/',
              'image': SITE + '/assets/v2/img/meem-obaidullah.jpg', 'jobTitle': 'E-commerce Entrepreneur',
              'email': 'mailto:' + C.EMAIL,
              'worksFor': {'@type': 'Organization', 'name': 'eCommeem', 'url': C.AGENCY_URL},
              'knowsAbout': [s['h1'] for s in C.SERVICES]}
    return page(p, body, '/', extra_ld=[person])


def build_about():
    p = C.ABOUT
    what = ''.join(f'''<a class="card reveal" href="/{slug}/">{icon(C.SERVICE_BY_SLUG[slug]['icon'])}<h3>{e(t)}</h3><p>{e(d)}</p></a>''' for slug, t, d in p['what'])
    rec = ''.join(f'''<article class="card reveal">{icon(ic)}<h3>{e(t)}</h3><p>{e(d)}</p></article>''' for ic, t, d in p['recognition'])
    appr = ''.join(f'''<article class="card reveal">{icon(ic)}<h3>{e(t)}</h3><p>{e(d)}</p></article>''' for ic, t, d in p['approach'])
    stats = ''.join('<div class="stat"><strong>%s</strong><span>%s</span></div>' % (e(a), e(b)) for a, b in p['stats'])
    crumbs = [('Home', '/'), ('About', '/about/')]
    body = f'''
<section class="hero"><div class="container hero-grid">
  <div class="hero-copy">
    {crumbs_html(crumbs)}
    <span class="eyebrow">eCommerce Entrepreneurs</span>
    <h1>eCommerce <span class="swoosh">Entrepreneur</span></h1>
    <p class="lead">{e(p['intro'])}</p>
    <span class="badge"><span class="pulse" aria-hidden="true"></span>Available for Freelance &amp; eCommerce Projects</span>
    <div class="btn-row">
      <a class="btn btn-primary" href="/contact/">Let's Connect</a>
      <a class="btn btn-ghost" href="/#services">Explore Services</a>
      <a class="btn btn-wa" href="{C.WA}" target="_blank" rel="noopener">{WA_SVG} WhatsApp Me</a>
    </div>
  </div>
  <div class="portrait">
    <img src="/assets/v2/img/meem-obaidullah.jpg" alt="Meem Obaidullah - eCommerce Entrepreneur" width="800" height="800" fetchpriority="high">
    <div class="portrait-card"><span class="brand-mark" aria-hidden="true">7+</span><div><strong>7+ Years</strong><span>of Experience</span></div></div>
  </div>
</div></section>

<section class="section band"><div class="container split">
  <div class="prose reveal"><span class="eyebrow">About Me</span><h2>Helping Businesses Grow Online.</h2>
    <p class="lead">{e(p['about'][0])}</p><p class="lead">{e(p['about'][1])}</p></div>
  <div class="stats reveal about-stats">{stats}</div>
</div></section>

<section class="section"><div class="container">
  <div class="section-head"><span class="eyebrow">What I Do</span><h2>eCommerce Operations &amp; Management</h2><p class="lead">{e(p['what_intro'])}</p></div>
  <div class="grid grid-4">{what}</div>
</div></section>

<section class="section" style="padding-top:0"><div class="container">
  <div class="section-head"><span class="eyebrow">Recognition &amp; Experience</span><h2>Built Around Real eCommerce Operations.</h2><p class="lead">{e(p['rec_intro'])}</p></div>
  <div class="grid grid-3">{rec}</div>
</div></section>

<section class="section band"><div class="container">
  <div class="section-head"><span class="eyebrow">My Approach</span><h2>More Than a VA. Your eCommerce Partner.</h2><p class="lead">{e(p['approach_intro'])}</p></div>
  <div class="grid grid-4">{appr}</div>
</div></section>

<section class="section"><div class="container"><div class="cta reveal">
  <div><span class="eyebrow">Let's Work Together</span><h2 style="margin-top:10px">Ready to Grow Your eCommerce Business?</h2><p>{e(p['closing'])}</p></div>
  <div class="btn-row"><a class="btn btn-primary" href="/contact/">Let's Connect</a><a class="btn btn-wa" href="{C.WA}" target="_blank" rel="noopener">{WA_SVG} WhatsApp Me</a></div>
</div></div></section>

{agency_block()}
'''
    person = {'@context': 'https://schema.org', '@type': 'ProfilePage', 'mainEntity': {
        '@type': 'Person', 'name': 'Meem Obaidullah', 'url': SITE + '/about/', 'jobTitle': 'eCommerce Entrepreneur',
        'worksFor': {'@type': 'Organization', 'name': 'eCommeem', 'url': C.AGENCY_URL}}}
    return page(p, body, '/about/', crumbs, [person])


def build_contact():
    p = C.CONTACT
    crumbs = [('Home', '/'), ('Contact', '/contact/')]
    cards = ''.join(f'''<div class="card contact-card">{icon(ic)}<div><small>{e(lbl)}</small><strong>{val}</strong></div></div>''' for ic, lbl, val in p['cards'])
    endpoint = ' data-endpoint="%s"' % C.FORM_ENDPOINT if C.FORM_ENDPOINT else ''
    body = f'''
<section class="page-hero"><div class="container"><div class="hero-copy">
  {crumbs_html(crumbs)}
  <span class="eyebrow">Secure Access Hub</span>
  <h1>Let's Talk <span class="swoosh">Investment</span> Scope</h1>
  <p class="lead">{e(p['intro'])}</p>
</div></div></section>
<section class="section"><div class="container contact-grid">
  <div class="contact-cards">{cards}
    <div class="btn-row">
      <a class="btn btn-wa" href="{C.WA}" target="_blank" rel="noopener">{WA_SVG} Direct WhatsApp Connection</a>
      <a class="btn btn-ghost" href="{C.LIVE_CHAT}" target="_blank" rel="noopener">Launch Real-Time Consult Portal</a>
    </div>
  </div>
  <form class="card form" data-contact data-email="{C.EMAIL}"{endpoint} method="post" novalidate>
    <h2 style="font-size:1.5rem">Venture Brief</h2>
    <div class="field"><label for="f-name">Full Name</label><input id="f-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="f-email">Corporate Email Address</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="f-wa">WhatsApp Number</label><input id="f-wa" name="whatsapp" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="f-msg">Investment Framework / Store Management Needs</label><textarea id="f-msg" name="message" required></textarea></div>
    <input type="hidden" name="_subject" value="New venture brief — meemobaidullah.com">
    <button class="btn btn-primary" type="submit">Submit Encrypted Venture Brief ↗</button>
    <p class="form-status" role="status" aria-live="polite"></p>
    <p class="form-note">Delivered securely via Formspree directly to {C.EMAIL}</p>
  </form>
</div></section>
{agency_block()}
'''
    return page(p, body, '/contact/', crumbs)


def build_service(s):
    crumbs = [('Home', '/'), ('Services', '/#services'), (s['h1'], '/%s/' % s['slug'])]
    others = [x for x in C.OTHER_SERVICES if x != s['slug']][:3]
    body = f'''
<section class="page-hero"><div class="container"><div class="hero-copy">
  {crumbs_html(crumbs)}
  <span class="eyebrow">{e(s['eyebrow'])}</span>
  <h1>{e(s['h1'])}</h1>
  <p class="lead">{e(s['hero'])}</p>
  <div class="btn-row">
    <a class="btn btn-wa" href="{C.WA}" target="_blank" rel="noopener">{WA_SVG} WhatsApp Portal</a>
    <a class="btn btn-primary" href="/contact/">↗ Talk Investment Scope</a>
  </div>
</div></div></section>
{steps_block(C.SERVICE_PROCESS_INTRO)}
<section class="section"><div class="container">
  <div class="section-head"><span class="eyebrow">Explore More</span><h2>Other Services I Manage</h2></div>
  <div class="grid grid-3">{service_cards(others)}</div>
</div></section>
{cta_block(s['cta'])}
'''
    svc_ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': s['h1'], 'description': s['desc'],
              'url': SITE + '/%s/' % s['slug'], 'provider': {'@type': 'Person', 'name': 'Meem Obaidullah', 'url': SITE + '/'},
              'areaServed': 'Worldwide'}
    # crumbs in JSON-LD must point at real pages: drop the "#services" hop there
    return page(s, body, '/%s/' % s['slug'], [crumbs[0], crumbs[2]], [svc_ld])


def draft_item(section, slug, name, live=False):
    href = '/%s/%s/' % (section, slug)
    pill = '<span class="pill live">Published</span>' if live else '<span class="pill">Draft</span>'
    return f'''<a class="card draft-item reveal" href="{href}"><span class="letter" aria-hidden="true">{e(name[0])}</span>
<span class="meta">{pill}<h3>{e(name)}</h3></span><span class="open">Open ↗</span></a>'''


def build_hub(key):
    h = C.HUBS[key]
    crumbs = [('Home', '/'), (h['label'], '/%s/' % key)]
    items = ''.join(draft_item(key, slug, C.stub_name(slug)) for slug in h['items'])
    featured = ''
    if key == 'blog':
        a = C.ARTICLE
        featured = f'''<a class="card featured is-link reveal" href="{a['path']}" style="margin-bottom:28px;text-decoration:none">
  <div style="display:grid;gap:10px"><span class="pill live">Published · Updated 2026</span><h2 style="font-size:clamp(1.5rem,3vw,2rem)">{e(a['h1'])}</h2><p>{e(a['desc'])}</p></div>
  <span class="btn btn-primary">Read the guide ↗</span></a>
  <h2 style="font-size:1.3rem;margin-bottom:16px">Coming soon</h2>'''
    body = f'''
<section class="page-hero"><div class="container"><div class="hero-copy">
  {crumbs_html(crumbs)}
  <span class="eyebrow">{e(h['eyebrow'])}</span>
  <h1>{e(h['h1'])}</h1>
  <p class="lead">{e(h['lead'])}</p>
</div></div></section>
<section class="section"><div class="container">{featured}<div class="draft-list">{items}</div></div></section>
{cta_block('Talk to Meem Directly', None, [('Talk to Meem Directly ↗', '/contact/', 'btn-primary'), ('Start a Conversation', C.WA, 'btn-outline-light')])}
'''
    return page(h, body, '/%s/' % key, crumbs)


def build_stub(key, slug):
    h = C.HUBS[key]
    name = C.stub_name(slug)
    p = C.stub_meta(key, slug)
    crumbs = [('Home', '/'), (h['label'], '/%s/' % key), (name, p['path'])]
    body = f'''
<section class="page-hero"><div class="container"><div class="stub">
  {crumbs_html(crumbs)}
  <span class="pill">In Draft</span>
  <h1>{e(name)}</h1>
  <p class="lead">This page is reserved for <strong>{e(name)}</strong> and is not yet published. {e(h['stub_line'])}</p>
  <p class="slug">Slug: {p['path']}</p>
  <div class="btn-row"><a class="btn btn-ghost" href="/{key}/">← {e(h['label'])}</a><a class="btn btn-primary" href="/contact/">Talk to Meem Directly ↗</a></div>
</div></div></section>
<section class="section"><div class="container">
  <div class="section-head"><span class="eyebrow">Meanwhile</span><h2>Services I Manage</h2></div>
  <div class="grid grid-3">{service_cards(C.OTHER_SERVICES[:3])}</div>
</div></section>
'''
    return page(p, body, p['path'], crumbs)


def build_article():
    """The FBA guide is only rebuilt when its exact original text is in src/."""
    a = C.ARTICLE
    src = os.path.join(os.path.dirname(__file__), '..', 'src', 'amazon-fba-complete-guide.html')
    if not os.path.exists(src):
        return None
    article_html = open(src, encoding='utf-8').read()
    crumbs = [('Home', '/'), ('Blog', '/blog/'), (a['h1'], a['path'])]
    body = f'''
<section class="page-hero"><div class="container"><div class="hero-copy">
  {crumbs_html(crumbs)}<span class="eyebrow">Guide · Updated 2026</span><h1>{e(a['h1'])}</h1>
  <p class="lead">By Meem Obaidullah</p></div></div></section>
<section class="section"><div class="container"><article class="prose article">{article_html}</article></div></section>
{cta_block('Want your FBA account managed day to day?', None, [('See Amazon FBA Management ↗', '/fba-automation/', 'btn-primary')])}
'''
    art_ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': a['h1'],
              'author': {'@type': 'Person', 'name': 'Meem Obaidullah', 'url': SITE + '/about/'},
              'mainEntityOfPage': SITE + a['path'], 'image': SITE + a['og_image']}
    return page(dict(a, og_type='article'), body, a['path'], crumbs, [art_ld])


# ---------------------------------------------------------------- write
def write(path, doc):
    out = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)
    return path


def main():
    built = [write('/', build_home()), write('/about/', build_about()), write('/contact/', build_contact())]
    for s in C.SERVICES:
        built.append(write('/%s/' % s['slug'], build_service(s)))
    for key, h in C.HUBS.items():
        built.append(write('/%s/' % key, build_hub(key)))
        for slug in h['items']:
            built.append(write('/%s/%s/' % (key, slug), build_stub(key, slug)))
    art = build_article()
    skipped = []
    if art:
        built.append(write(C.ARTICLE['path'], art))
    else:
        skipped.append(C.ARTICLE['path'])

    # sitemap: same URL list and lastmod dates as the live sitemap
    urls = ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, path, mod) for path, mod in C.SITEMAP)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)

    expected = {p for p, _ in C.SITEMAP}
    missing = expected - set(built) - set(skipped)
    extra = set(built) - expected
    print('built %d pages; kept-live %s; missing %s; extra %s' % (len(built), skipped, sorted(missing), sorted(extra)))
    if missing or extra:
        sys.exit(1)


if __name__ == '__main__':
    main()
