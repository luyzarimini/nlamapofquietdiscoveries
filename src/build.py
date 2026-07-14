"""Build index.html from template.html.

Inlines the two handwriting fonts (Caveat, Reenie Beanie) as base64 data URIs
and wraps the page in a standalone HTML skeleton, so index.html is a single
self-contained file with no external requests.

Usage:  python src/build.py   (run from the repo root or from src/)
"""
import base64
import pathlib
import re

SRC = pathlib.Path(__file__).parent
ROOT = SRC.parent

def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

html = (SRC / "template.html").read_text(encoding="utf-8")
html = html.replace("__CAVEAT__", b64(SRC / "fonts" / "caveat.woff2"))
html = html.replace("__REENIE__", b64(SRC / "fonts" / "reenie.woff2"))

# template.html is body-content (the claude.ai artifact host wraps it);
# for a standalone page we lift the <title> into a proper <head>.
m = re.search(r"<title>(.*?)</title>\s*", html, re.S)
title = m.group(1) if m else "The Netherlands — A Map of Quiet Discoveries"
body = html[m.end():] if m else html

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
</head>
<body>
{body}
</body>
</html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"wrote {ROOT / 'index.html'} ({len(page):,} bytes)")
