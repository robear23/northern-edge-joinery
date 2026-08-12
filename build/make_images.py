"""Grade and derive the responsive image set for the Northern Edge Joinery site.

One grade is applied to every photograph so the page reads as a single shoot:
warm, low-contrast, natural light. Images sit at reduced brightness in CSS and
animate to brightness(1) on hover, so the grade stays deliberately restrained
here rather than baking the darkening in.

Outputs WebP + JPEG at each width into site/assets/img/.
"""
import os
from PIL import Image, ImageEnhance

SRC = "hires"
OUT = "../site/assets/img"

# ── the grade ──────────────────────────────────────────────────────────────
SATURATION = 0.86     # pull back the colour so timber reads as tone, not hue
CONTRAST = 0.92       # low-contrast, natural light
WARM = (1.045, 1.005, 0.955)   # per-channel gain: warm the highlights
LIFT = (10, 8, 6)     # lift the blacks toward warm ink rather than pure black
LIFT_STRENGTH = 0.82  # how much of the original range survives the lift


def grade(im):
    im = im.convert("RGB")
    im = ImageEnhance.Color(im).enhance(SATURATION)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)
    # per-channel warm gain + lifted blacks, as a single LUT per channel
    lut = []
    for ch in range(3):
        gain, lift = WARM[ch], LIFT[ch]
        lut += [
            min(255, max(0, round((v * LIFT_STRENGTH + lift) * gain)))
            for v in range(256)
        ]
    return im.point(lut)


def crop_to(im, ratio, y_bias=0.5, x_bias=0.5):
    """Crop to `ratio` (w/h). The bias pair shifts the crop window within the frame."""
    w, h = im.size
    if w / h > ratio:
        nw, nh = round(h * ratio), h
    else:
        nw, nh = w, round(w / ratio)
    x = round((w - nw) * x_bias)
    y = round((h - nh) * y_bias)
    return im.crop((x, y, x + nw, y + nh))


def emit(im, name, widths, quality=(80, 82)):
    """Write WebP + JPEG at each width. Returns the list of files written."""
    os.makedirs(OUT, exist_ok=True)
    written = []
    for w in widths:
        if w > im.width:
            continue
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        p_webp, p_jpg = f"{OUT}/{name}-{w}.webp", f"{OUT}/{name}-{w}.jpg"
        r.save(p_webp, "WEBP", quality=quality[0], method=6)
        r.save(p_jpg, "JPEG", quality=quality[1], optimize=True, progressive=True)
        written += [p_webp, p_jpg]
    return written


# ── the manifest ───────────────────────────────────────────────────────────
HERO = ("8146203", "hero", 16 / 9, 0.5, [768, 1200, 1600, 1920])

SERVICES = [
    ("16433564", "service-joinery", 0.5),
    ("6585750", "service-wardrobes", 0.5),
    ("24245782", "service-furniture", 0.5),
]

PORTFOLIO = [
    # id, name, y_bias, x_bias
    ("23541111", "work-01", 0.40, 0.50),
    ("33744583", "work-02", 0.50, 0.50),
    ("13865080", "work-03", 0.45, 0.50),
    ("16804490", "work-04", 0.45, 0.50),
    ("20705886", "work-05", 0.50, 0.50),
    ("6580380",  "work-06", 0.50, 0.50),
    ("7045321",  "work-07", 0.50, 0.62),
    ("6585757",  "work-08", 0.50, 0.72),
    ("1907784",  "work-09", 0.45, 0.50),
    ("6758782",  "work-10", 0.50, 0.50),
    ("19955716", "work-11", 0.45, 0.50),
    ("6908561",  "work-12", 0.45, 0.55),
]

SERVICE_RATIO = 4 / 3
WORK_RATIO = 4 / 5

if __name__ == "__main__":
    total = 0

    sid, name, ratio, bias, widths = HERO
    im = grade(Image.open(f"{SRC}/{sid}.jpg"))
    total += len(emit(crop_to(im, ratio, bias), name, widths, quality=(78, 80)))
    # OpenGraph card, cropped from the same frame
    og = crop_to(im, 1200 / 630, 0.5).resize((1200, 630), Image.LANCZOS)
    og.save(f"{OUT}/og-northern-edge-joinery.jpg", "JPEG", quality=84, optimize=True)
    total += 1

    for sid, name, bias in SERVICES:
        im = grade(Image.open(f"{SRC}/{sid}.jpg"))
        total += len(emit(crop_to(im, SERVICE_RATIO, bias), name, [560, 860, 1200]))

    for sid, name, y_bias, x_bias in PORTFOLIO:
        im = grade(Image.open(f"{SRC}/{sid}.jpg"))
        total += len(emit(crop_to(im, WORK_RATIO, y_bias, x_bias), name, [400, 760, 1100]))
        # lightbox uses a larger, less-cropped frame
        total += len(emit(crop_to(im, 3 / 4, y_bias, x_bias), f"{name}-lg", [1400]))

    print(f"wrote {total} files to {OUT}")
