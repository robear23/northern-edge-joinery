"""Redraw the Northern Edge Joinery wordmark as outlined SVG paths.

The supplied logo.jpg is a 150x150 raster with a baked-in #3E3C3D background that
fights the design system's #2c2e2c charcoal. This regenerates the mark as pure
vector paths so it inherits currentColor and has no ground of its own.

Text is converted to outlines, so the SVG carries no font dependency and no
font-weight ever reaches the compiled CSS.
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FONT = "../site/assets/fonts/raleway-latin.woff2"


def load(weight):
    f = TTFont(FONT)
    return instantiateVariableFont(f, {"wght": weight}, inplace=False)


def layout(font, text, size, tracking_em, x, baseline, out):
    """Append SVG path data for `text`, return the advance width consumed."""
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    track = tracking_em * size
    pen_x = x
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise SystemExit(f"missing glyph for {ch!r}")
        adv = hmtx[gname][0] * scale
        if ch != " ":
            spen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
            # y is flipped: font units go up, SVG goes down
            tpen = TransformPen(spen, Transform(scale, 0, 0, -scale, pen_x, baseline))
            gs[gname].draw(tpen)
            d = spen.getCommands()
            if d:
                out.append(f'<path d="{d}"/>')
        pen_x += adv + track
    return pen_x - track - x  # trailing track is not part of the mark


def build(w1, w2, path):
    f1, f2 = load(w1), load(w2)

    L1, S1, T1 = "NORTHERN EDGE", 100.0, 0.055
    L2, S2, T2 = "JOINERY LTD", 42.0, 0.30

    # measure first
    probe = []
    w_line1 = layout(f1, L1, S1, T1, 0, 0, probe)
    probe = []
    w_line2 = layout(f2, L2, S2, T2, 0, 0, probe)

    rule_len = 46.0
    rule_gap = 26.0
    line2_block = rule_len + rule_gap + w_line2 + rule_gap + rule_len
    total_w = max(w_line1, line2_block)

    # Keep the viewBox origin at 0,0. A <symbol> with a non-zero minY is
    # placed by <use> at user-space 0,0 and loses everything above it.
    cap_height = 0.72                    # Raleway caps sit at ~0.71em
    baseline1 = S1 * cap_height
    baseline2 = baseline1 + S1 * 0.62    # optical gap between the two lines

    body = []
    layout(f1, L1, S1, T1, (total_w - w_line1) / 2, baseline1, body)
    x2 = (total_w - w_line2) / 2
    layout(f2, L2, S2, T2, x2, baseline2, body)

    # flanking rules, optically centred on the lowercase-x height of line 2
    ry = baseline2 - S2 * 0.30
    rh = 3.0
    body.append(
        f'<rect x="{x2 - rule_gap - rule_len:.2f}" y="{ry - rh / 2:.2f}" '
        f'width="{rule_len:.2f}" height="{rh:.2f}"/>'
    )
    body.append(
        f'<rect x="{x2 + w_line2 + rule_gap:.2f}" y="{ry - rh / 2:.2f}" '
        f'width="{rule_len:.2f}" height="{rh:.2f}"/>'
    )

    vb_h = baseline2 + S2 * 0.06
    inner = "".join(body)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '
        f'{total_w:.2f} {vb_h:.2f}" fill="currentColor" role="img" '
        f'aria-label="Northern Edge Joinery Ltd">{inner}</svg>'
    )
    open(path, "w", encoding="utf8").write(svg)
    print(f"{path}: weights {w1}/{w2}, viewBox 0 0 {total_w:.2f} {vb_h:.2f}, {len(svg)} bytes")
    return svg


if __name__ == "__main__":
    for w in (500, 600, 700):
        build(w, 500, f"logo-{w}.svg")
