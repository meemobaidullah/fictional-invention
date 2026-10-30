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
- **Contact**: ecommeem@gmail.com, +880 1731-558195 and +880 1309-012476 live in `partials/header.html`, `partials/footer.html` and the Organization JSON-LD.
- **Social image & icons**: add `assets/img/og-image.png` (1200×630), `assets/img/logo.svg`, `assets/img/apple-touch-icon.png` (180×180) and a root `favicon.ico`.
- **Twitter/X handle**: `twitter:site` assumes `@ecommeem`.
- **Partner badges & accreditations**: hero "Platforms we manage" row, the homepage Recognitions section and the Programs & Certifications chips on `about.html`. Swap the text chips for the official badge files.
- **Client logos**: the 10 logo tiles under the hero (real clients only, with their permission).
- **Case study slider**: four remaining `XX%` metrics, client quotes in the clients' own words, names and "Read The Success Story" links.
- **Service page stats**: the three numbers in the stats panel on the launch, brand management and Storefront pages.
- **Portfolio tiles**: before/after images on the brand management page and Storefront screenshots on the Storefront page.
- **Founder photo**: `assets/img/team/meem-obaidullah*.jpg` (cropped from the supplied poster). Swap for a plain studio shot any time.
- **Dark mode**: colours live in tokens at the top of `styles.css`; the dark values are in the `[data-theme="dark"]` block at the end. The header switch remembers each visitor's choice.
- **Forms**: every form is a 3-step checklist that posts to `https://formsubmit.co/ajax/ecommeem@gmail.com` (set in `assets/js/main.js`). The first submission from the live domain sends an activation email to ecommeem@gmail.com; click it once and messages start arriving.
- **Analytics**: no tracking is installed. Add your own GA4/GTM ID if needed.
- **Social profiles**: add URLs to `sameAs` in the Organization JSON-LD.
- Keep the FAQ JSON-LD in `<head>` in sync with the `#faq` section when you edit questions.

## Pages and shared parts

- `index.html`: homepage
- `help-me-launch.html`: Amazon launch service page
- `amazon-brand-management-services.html`: brand management service page
- `amazon-brand-storefront-design.html`: Storefront design service page
- `free-amazon-audit.html`: free store audit page
- `about.html`: about eCommeem and founder Meem Obaidullah
- `partials/header.html`, `partials/footer.html`: the shared menu and footer. Edit them there, then run `python3 tools/build_partials.py` to copy them into every page.

## Logo files

`assets/img/logo/` holds the eCommeem.com logo as SVG, PNG (transparent) and JPG, in a dark-text version for light backgrounds and a white-text version for dark backgrounds, plus a square rocket icon (512px PNG/JPG) for social profiles.
