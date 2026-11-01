"""Copy shared partials into every page.

Each page marks the spot with <!-- header:start --> ... <!-- header:end -->.
Run after editing anything in partials/:  python3 tools/build_partials.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIALS = ["header", "footer"]

# Applies the saved (or system) colour theme before the stylesheet paints, so dark mode never flashes white.
THEME_INIT = (
    "  <script data-theme-init>try{var t=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');"
    "document.documentElement.dataset.theme=t}catch(e){}</script>\n"
)
STYLESHEET = '  <link rel="stylesheet" href="assets/css/styles.css">'
ANALYTICS = '  <script src="assets/js/analytics.js" async></script>\n'

for page in sorted(ROOT.glob("*.html")):
    html = page.read_text(encoding="utf-8")
    for name in PARTIALS:
        body = (ROOT / "partials" / f"{name}.html").read_text(encoding="utf-8").rstrip("\n")
        pattern = re.compile(rf"<!-- {name}:start -->.*?<!-- {name}:end -->", re.S)
        html = pattern.sub(lambda _: f"<!-- {name}:start -->\n{body}\n  <!-- {name}:end -->", html)
    if "data-theme-init" not in html and STYLESHEET in html:
        html = html.replace(STYLESHEET, THEME_INIT + STYLESHEET, 1)
    if "assets/js/analytics.js" not in html and STYLESHEET in html:
        html = html.replace(STYLESHEET, ANALYTICS + STYLESHEET, 1)
    page.write_text(html, encoding="utf-8")
    print("updated", page.name)
