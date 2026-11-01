# meemobaidullah.com

Personal site of Meem Obaidullah, kept separate from the eCommeem agency site in this repo.
Own design: deep navy + gold, Space Grotesk headings, Inter body, light and dark mode.

- `tools/content.py`: all page text and SEO metadata, carried over from the live site. Edit text here.
- `tools/build.py`: layout. `python3 tools/build.py` regenerates `public/`.
- `public/`: the files that go into Hostinger `public_html`. See `UPLOAD-GUIDE.txt`.

Every URL of the live sitemap is kept as is, including `/case-stady/` and `/sucess/`.
Draft pages keep `noindex, follow`, as on the live site.

Open items
- `/blog/amazon-fba-complete-guide/` is not rebuilt yet. Put its original article HTML in
  `src/amazon-fba-complete-guide.html` and set the exact live meta description in `content.py`;
  the build then renders it in the new design. Until then the live page stays untouched.
- Contact form: set `FORM_ENDPOINT` in `content.py` to the live Formspree URL. Empty means the
  form opens the visitor's email app addressed to meemobaidullah@gmail.com.
- The live contact page lists a USA number "+1 315 581 95" that is missing digits; it is left out.

Preview locally: `python3 -m http.server 8000 -d public`.
