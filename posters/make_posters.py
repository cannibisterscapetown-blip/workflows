#!/usr/bin/env python3
"""Cannibisters house-rules posters: pool table + arcade machine.
Gilded Apothecary style — dark charcoal, aged gold, candle-cream.
A4 portrait @ 300dpi."""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 2480, 3508
CX = W // 2

BG      = (39, 37, 34)      # warm charcoal
BG_HI   = (48, 45, 41)      # glow centre
GOLD    = (198, 154, 74)    # aged gold
GOLD_HI = (232, 196, 116)   # bright gold (emblem numerals)
CREAM   = (235, 226, 208)   # candle-cream
SMOKE   = (152, 143, 128)   # hushed asides
FRAME   = (120, 98, 58)     # dim gold frame

FD = "/root/.claude/skills/synced/canvas-design/canvas-fonts"
def F(name, size):
    return ImageFont.truetype(f"{FD}/{name}", size)

# ---------------------------------------------------------------- leaf emblem
def extract_leaf():
    im = Image.open("/home/user/workflows/Canni Logo.png").convert("RGB")
    a = np.array(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    goldish = (r > b + 18) & (r > 70)
    maxc = a.max(axis=2)
    alpha = np.clip((maxc - 40) * 3.2, 0, 255)
    alpha[~goldish] = 0
    rgba = np.dstack([a, alpha]).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    ys, xs = np.nonzero(alpha)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    return out.crop(box)

LEAF = extract_leaf()

def tint(img, color):
    """Recolor leaf luminance into a gold ramp toward `color`."""
    a = np.array(img).astype(float)
    lum = (a[..., :3].max(axis=2)) / 255.0
    out = a.copy()
    for i in range(3):
        out[..., i] = np.clip(lum * color[i] * 1.12, 0, 255)
    return Image.fromarray(out.astype(np.uint8), "RGBA")

# ---------------------------------------------------------------- text helpers
def tracked_w(draw, text, font, tr):
    return sum(draw.textlength(c, font=font) for c in text) + tr * (len(text) - 1)

def tracked(draw, xy, text, font, fill, tr, anchor="c"):
    x, y = xy
    w = tracked_w(draw, text, font, tr)
    if anchor == "c":
        x -= w / 2
    for c in text:
        draw.text((x, y), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + tr
    return w

def diamond(draw, x, y, r, fill, outline=None, w=2):
    pts = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)]
    draw.polygon(pts, fill=fill, outline=outline, width=w)

def px_cluster(draw, x, y, s, fill):
    """2x2 tessera cluster (arcade motif)."""
    for dx, dy in ((-s, -s), (0, -s), (-s, 0), (0, 0)):
        draw.rectangle([x + dx + 1, y + dy + 1, x + dx + s - 2, y + dy + s - 2], fill=fill)

def ornament_divider(draw, y, half=330, motif="diamond"):
    draw.line([CX - half, y, CX - 30, y], fill=FRAME, width=2)
    draw.line([CX + 30, y, CX + half, y], fill=FRAME, width=2)
    if motif == "diamond":
        diamond(draw, CX, y, 11, None, GOLD, 2)
        diamond(draw, CX, y, 4, GOLD)
    else:
        px_cluster(draw, CX, y, 10, GOLD)

# ---------------------------------------------------------------- background
def base_canvas():
    # radial glow, centre-upper
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    d = np.sqrt((xx - CX) ** 2 + ((yy - H * 0.32) * 1.15) ** 2)
    t = np.clip(d / (H * 0.85), 0, 1)
    img = np.zeros((H, W, 3))
    for i in range(3):
        img[..., i] = BG_HI[i] * (1 - t) + BG[i] * t
    # vignette
    dv = np.sqrt(((xx - CX) / (W * 0.72)) ** 2 + ((yy - H / 2) / (H * 0.72)) ** 2)
    vig = 1 - 0.16 * np.clip(dv, 0, 1) ** 2
    img *= vig[..., None]
    return Image.fromarray(img.astype(np.uint8), "RGB")

def add_grain(img):
    a = np.array(img).astype(float)
    noise = np.random.default_rng(7).normal(0, 3.2, a.shape)
    return Image.fromarray(np.clip(a + noise, 0, 255).astype(np.uint8), "RGB")

def frame(draw, motif):
    m1, m2 = 92, 124
    draw.rectangle([m1, m1, W - m1, H - m1], outline=FRAME, width=4)
    draw.rectangle([m2, m2, W - m2, H - m2], outline=FRAME, width=2)
    # corner marks
    for cx0, cy0 in ((m2, m2), (W - m2, m2), (m2, H - m2), (W - m2, H - m2)):
        if motif == "diamond":
            diamond(draw, cx0, cy0, 14, BG)
            diamond(draw, cx0, cy0, 10, GOLD)
        else:
            draw.rectangle([cx0 - 12, cy0 - 12, cx0 + 12, cy0 + 12], fill=BG)
            px_cluster(draw, cx0, cy0, 11, GOLD)
    # rail sights / tesserae along inner frame
    def sights(n, horiz, fixed):
        span = (W if horiz else H) - 2 * m2
        for i in range(1, n + 1):
            p = m2 + span * i / (n + 1)
            x, y = (p, fixed) if horiz else (fixed, p)
            if motif == "diamond":
                diamond(draw, x, y, 7, BG)
                diamond(draw, x, y, 6, GOLD)
            else:
                draw.rectangle([x - 8, y - 8, x + 8, y + 8], fill=BG)
                px_cluster(draw, x, y, 7, GOLD)
    sights(3, True, m2)
    sights(3, True, H - m2)
    sights(5, False, m2)
    sights(5, False, W - m2)

# ---------------------------------------------------------------- poster
def poster(path, title_lines, rules, motif, numeral_style):
    img = base_canvas()
    draw = ImageDraw.Draw(img)
    frame(draw, motif)

    # --- masthead
    leaf_h = 470
    leaf = LEAF.resize((int(LEAF.width * leaf_h / LEAF.height), leaf_h), Image.LANCZOS)
    leaf = tint(leaf, GOLD_HI)
    img.paste(leaf, (CX - leaf.width // 2, 252), leaf)
    draw = ImageDraw.Draw(img)

    tracked(draw, (CX, 790), "CANNIBISTERS", F("Gloock-Regular.ttf", 148), CREAM, 30)
    tracked(draw, (CX, 985), "HERBAL APOTHECARY", F("Italiana-Regular.ttf", 60), GOLD, 34)
    ornament_divider(draw, 1122, motif=motif)

    # --- title
    tracked(draw, (CX, 1195), "HOUSE RULES OF", F("Italiana-Regular.ttf", 56), SMOKE, 30)
    size = 218
    tf = F("Gloock-Regular.ttf", size)
    while tracked_w(draw, title_lines, tf, 16) > 1900:
        size -= 4
        tf = F("Gloock-Regular.ttf", size)
    tracked(draw, (CX, 1290 + (218 - size) // 2), title_lines, tf, GOLD_HI, 16)

    # --- rules
    y0, y1 = 1660, 3170
    if numeral_style == "roman":
        num_font = F("Gloock-Regular.ttf", 64)
        numerals = ["I", "II", "III", "IV", "V", "VI"]
    else:
        num_font = F("Silkscreen-Regular.ttf", 52)
        numerals = ["01", "02", "03", "04", "05", "06"]
    main_font = F("CrimsonPro-Regular.ttf", 88)
    sub_font  = F("CrimsonPro-Italic.ttf", 58)

    n = len(rules)
    block_h = [64 + 20 + 96 + 10 + 62 for _ in rules]     # numeral + gaps + line + sub
    total = sum(block_h)
    gap = (y1 - y0 - total) / (n - 1)
    y = y0
    for i, (main, sub) in enumerate(rules):
        tracked(draw, (CX, y), numerals[i], num_font, GOLD, 8)
        y += 64 + 22
        draw.text((CX, y), main, font=main_font, fill=CREAM, anchor="ma")
        y += 96 + 12
        draw.text((CX, y), sub, font=sub_font, fill=SMOKE, anchor="ma")
        y += 62 + gap

    # --- footer
    ornament_divider(draw, 3244, half=240, motif=motif)
    tracked(draw, (CX, 3278), "PLAY KINDLY  ·  THE CANNIBISTERS FAMILY",
            F("Italiana-Regular.ttf", 44), SMOKE, 20)

    img = add_grain(img)
    img.save(path, dpi=(300, 300))
    print("saved", path)
    return img

OUT = "/tmp/claude-0/-home-user-workflows/8848fb0b-549d-543d-8909-89a475fe9f5d/scratchpad"

pool = poster(
    f"{OUT}/pool_table_rules.png",
    "THE POOL TABLE",
    [
        ("Winner stays on.", "take the frame, and the table is yours to keep."),
        ("No ashtrays on the table.", "ash and baize are old enemies."),
        ("No drinks on the table.", "the felt drinks nothing."),
        ("Kindly leave the chalk.", "it lives here — let it stay."),
    ],
    motif="diamond", numeral_style="roman",
)

arc = poster(
    f"{OUT}/arcade_rules.png",
    "THE ARCADE",
    [
        ("Share the machine.", "no hogging — high scores are earned in turns."),
        ("If staff ask you to stop playing,", "please do so with good grace."),
        ("No ashtrays on the machine.", "there is delicate circuitry beneath."),
        ("No drinks on the machine.", "spills end games faster than GAME OVER."),
        ("Treat it kindly.", "it is only visiting — help us convince it to stay."),
    ],
    motif="pixel", numeral_style="pixel",
)

# combined print-ready PDF
pool.convert("RGB").save(f"{OUT}/cannibisters_house_rules_posters.pdf",
                         save_all=True, append_images=[arc.convert("RGB")],
                         resolution=300)
print("saved pdf")
