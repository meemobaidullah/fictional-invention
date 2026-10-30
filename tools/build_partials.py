"""Copy shared partials into every page.

Each page marks the spot with <!-- header:start --> ... <!-- header:end -->.
Run after editing anything in partials/:  python3 tools/build_partials.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIALS = ["header", "footer"]

for page in sorted(ROOT.glob("*.html")):
    html = page.read_text(encoding="utf-8")
    for name in PARTIALS:
        body = (ROOT / "partials" / f"{name}.html").read_text(encoding="utf-8").rstrip("\n")
        pattern = re.compile(rf"<!-- {name}:start -->.*?<!-- {name}:end -->", re.S)
        html = pattern.sub(lambda _: f"<!-- {name}:start -->\n{body}\n  <!-- {name}:end -->", html)
    page.write_text(html, encoding="utf-8")
    print("updated", page.name)
