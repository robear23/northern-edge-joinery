"""Emit the final brand assets from the redrawn wordmark.

  site/assets/brand/wordmark.svg   standalone, currentColor
  build/wordmark-symbol.html       <symbol> form for inlining once per page
  site/assets/brand/favicon.svg    square NE monogram, bone on ink
  site/favicon-*.png               raster fallbacks
  site/apple-touch-icon.png

The wordmark is outlined paths, so it carries no font dependency and no
font-weight ever reaches the compiled CSS.
"""
import os, re
from make_logo import build, layout, load

BRAND = "../site/assets/brand"
os.makedirs(BRAND, exist_ok=True)

# ── wordmark ───────────────────────────────────────────────────────────────
svg = build(500, 500, f"{BRAND}/wordmark.svg")

vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
inner = re.sub(r"^<svg[^>]*>|</svg>$", "", svg)
symbol = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" '
    f'style="position:absolute" aria-hidden="true" focusable="false">'
    f'<symbol id="ne-wordmark" viewBox="{vb}" fill="currentColor">{inner}</symbol></svg>'
)
open("wordmark-symbol.html", "w", encoding="utf8").write(symbol)
print(f"symbol: {len(symbol)} bytes, viewBox {vb}")

# ── favicon: NE monogram ───────────────────────────────────────────────────
INK, BONE = "#131413", "#f0eeeb"
f = load(500)
paths = []
size = 190.0
w = layout(f, "NE", size, 0.10, 0, 0, paths)
box = 512.0
baseline = box / 2 + size * 0.72 / 2
paths = []
layout(f, "NE", size, 0.10, (box - w) / 2, baseline, paths)

rule_w, rule_h = w * 0.9, 7.0
ry = baseline + size * 0.38
paths.append(
    f'<rect x="{(box - rule_w) / 2:.2f}" y="{ry:.2f}" '
    f'width="{rule_w:.2f}" height="{rule_h:.2f}"/>'
)

fav = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
    f'<rect width="512" height="512" fill="{INK}"/>'
    f'<g fill="{BONE}">{"".join(paths)}</g></svg>'
)
open(f"{BRAND}/favicon.svg", "w", encoding="utf8").write(fav)
print(f"favicon.svg: {len(fav)} bytes")
