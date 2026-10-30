# eCommeem website

Homepage for eCommeem, a full-service Amazon agency. Plain HTML, CSS and JavaScript with no build step.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Structure

```
index.html            Homepage (SEO meta, JSON-LD, all sections)
assets/css/styles.css Styles (mobile-first)
assets/js/main.js     Mobile nav, scroll reveal, audit form validation
assets/img/           Favicon and images
```

## Before launch

Values highlighted in orange on the page (class `ph`) and `PLACEHOLDER` / `TODO` comments in the code still need real data:

- **Domain**: canonical, Open Graph and JSON-LD URLs assume `https://www.ecommeem.com/`.
- **Email**: `hello@ecommeem.com` in the footer and JSON-LD.
- **Social image & icons**: add `assets/img/og-image.png` (1200×630), `assets/img/logo.svg`, `assets/img/apple-touch-icon.png` (180×180) and a root `favicon.ico`.
- **Twitter/X handle**: `twitter:site` assumes `@ecommeem`.
- **Partner badges & accreditations**: hero badge row and the Recognitions section. Show only programs eCommeem actually holds.
- **Client logos**: the 10 logo tiles under the hero (only with client permission).
- **Case study slider**: four `XX%` metrics, client quotes, names and "Read The Success Story" links.
- **Why eCommeem / stats**: "XX+ Stores Managed", the three numbers in the black stats panel, and "XX+ Years" in the hero art.
- **Audit turnaround**: "within X business days" in the audit section.
- **Audit form**: point the form at a backend (Formspree, HubSpot, etc.) and replace the demo submit in `main.js`.
- **Analytics**: no tracking is installed. Add your own GA4/GTM ID if needed.
- **Social profiles**: add URLs to `sameAs` in the Organization JSON-LD.
- Keep the FAQ JSON-LD in `<head>` in sync with the `#faq` section when you edit questions.

## Pages and shared parts

- `index.html`: homepage
- `help-me-launch.html`: Amazon launch service page
- `partials/header.html`, `partials/footer.html`: the shared menu and footer. Edit them there, then run `python3 tools/build_partials.py` to copy them into every page.

## Logo files

`assets/img/logo/` holds the eCommeem.com logo as SVG, PNG (transparent) and JPG, in a dark-text version for light backgrounds and a white-text version for dark backgrounds, plus a square rocket icon (512px PNG/JPG) for social profiles.
