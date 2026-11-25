#!/usr/bin/env python3
"""Poster generator for 24 November 2026 world news (v2, hero-led design).

Draws one 1024x1024 PNG at 2x supersampling with Pillow:
one dominant visual idea -- a cracked Earth under a giant COP31 headline --
over a disciplined band of four high-contrast story tiles.

Facts (all reported 24 Nov 2026, same verified set as the v1 entry):
  - COP31 in Antalya ended with no deal; the world reacted in anger on day
    two: Guterres "deeply disappointed", the EU said the summit was hijacked
    by oil states, Panama charged a "petroleum mafia", island nations
    refused to sign.
  - Cikande candy-factory fire, Banten: toll confirmed at 24 dead, about 30
    workers still missing.
  - Brent crude slid to $89.37, its lowest since August, as oil kept flowing
    past the Hormuz attacks.
  - Fresh drone and missile strikes hit Ukraine's Kyiv region.
  - World Chess Championship title match opened in Geneva: champion
    D Gukesh (India) vs Javokhir Sindarov (Uzbekistan).
  - Also: Modi + Shah flagged off the Ayodhya-Janakpur express; Alcaraz won
    his first ATP Finals title in Turin; Pant hit 128 in the drawn
    Wellington Test.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SS = 2                      # supersampling factor
W = 1024 * SS
H = 1024 * SS

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (10, 17, 32)           # deep ink navy
PANEL = (19, 30, 52)        # tile background
WHITE = (245, 247, 250)
MUTED = (168, 182, 205)
RED = (232, 62, 42)
AMBER = (245, 166, 35)
SKY = (84, 169, 255)
GREEN = (64, 178, 106)
VIOLET = (178, 132, 255)


def font(path, size):
    return ImageFont.truetype(path, size * SS)


def text(d, xy, s, fnt, fill, anchor="la", spacing=4):
    d.text((xy[0] * SS, xy[1] * SS), s, font=fnt, fill=fill,
           anchor=anchor, spacing=spacing * SS)


def fit_font(path, s, max_w, start):
    """Largest bold font size (<= start) whose text fits max_w px."""
    size = start
    while size > 10:
        f = font(path, size)
        if f.getlength(s) / SS <= max_w:
            return f
        size -= 2
    return font(path, 10)


# ---------------------------------------------------------------- globe ----
def draw_globe(img, cx, cy, r):
    """A bright Earth on the dark ground, split by a glowing crack."""
    glow = Image.new("RGB", img.size, (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([(cx - r * 1.25) * SS, (cy - r * 1.25) * SS,
                (cx + r * 1.25) * SS, (cy + r * 1.25) * SS], fill=(28, 60, 96))
    glow = glow.filter(ImageFilter.GaussianBlur(60 * SS))
    img.paste(Image.blend(img, Image.blend(img, glow, 0.9), 0.55),
              (0, 0))

    d = ImageDraw.Draw(img, "RGBA")
    # ocean
    d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
              fill=(23, 92, 148))
    # continents: rough hand-placed blobs, clipped to the disc below
    land = Image.new("L", img.size, 0)
    ld = ImageDraw.Draw(land)
    blobs = [
        # (dx, dy, rx, ry) relative to centre, in units of r -- kept apart
        # by visible ocean gaps so the landmasses read as continents
        (-0.55, -0.45, 0.24, 0.15), (-0.46, -0.13, 0.13, 0.17),  # N/S America
        (-0.40, 0.22, 0.09, 0.13),
        (0.00, -0.52, 0.26, 0.13),                               # Europe
        (0.38, -0.38, 0.26, 0.17), (0.60, -0.08, 0.15, 0.14),    # Asia
        (0.04, 0.10, 0.17, 0.22),                                # Africa
        (0.55, 0.38, 0.17, 0.11),                                # Oceania
    ]
    for dx, dy, rx, ry in blobs:
        ld.ellipse([(cx + (dx - rx) * r) * SS, (cy + (dy - ry) * r) * SS,
                    (cx + (dx + rx) * r) * SS, (cy + (dy + ry) * r) * SS],
                   fill=255)
    disc = Image.new("L", img.size, 0)
    ImageDraw.Draw(disc).ellipse(
        [(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=255)
    land = Image.composite(land, Image.new("L", img.size, 0), disc)
    green = Image.new("RGB", img.size, (52, 168, 92))
    img.paste(green, (0, 0), land)
    d = ImageDraw.Draw(img, "RGBA")
    # rim + shading arc
    d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
              outline=(190, 225, 255), width=5 * SS)
    d.arc([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
          start=100, end=250, fill=(8, 30, 55, 120), width=26 * SS)
    # the crack: jagged lightning split, hot core over a red glow
    pts = [(cx - 0.30 * r, cy - 0.98 * r), (cx - 0.10 * r, cy - 0.62 * r),
           (cx - 0.26 * r, cy - 0.34 * r), (cx + 0.02 * r, cy - 0.08 * r),
           (cx - 0.12 * r, cy + 0.22 * r), (cx + 0.10 * r, cy + 0.52 * r),
           (cx - 0.02 * r, cy + 0.98 * r)]
    branches = [[pts[2], (cx - 0.52 * r, cy - 0.18 * r)],
                [pts[4], (cx + 0.38 * r, cy + 0.30 * r)]]
    sp = [(x * SS, y * SS) for x, y in pts]
    for wdt, col in [(17, (255, 90, 30, 90)), (10, (255, 120, 40, 170)),
                     (5, (255, 214, 120, 255))]:
        d.line(sp, fill=col, width=wdt * SS, joint="curve")
        for br in branches:
            d.line([(x * SS, y * SS) for x, y in br], fill=col,
                   width=max(2, wdt - 6) * SS)
    # sparks
    for dx, dy, rr in [(-0.62, -0.55, 7), (0.55, -0.42, 6), (0.66, 0.18, 8),
                       (-0.58, 0.52, 6), (0.30, 0.78, 5)]:
        d.ellipse([(cx + dx * r - rr) * SS, (cy + dy * r - rr) * SS,
                   (cx + dx * r + rr) * SS, (cy + dy * r + rr) * SS],
                  fill=(255, 150, 60, 220))


# ---------------------------------------------------------------- icons ----
def icon_flame(d, cx, cy, s, col):
    pts = [(cx, cy - s), (cx + 0.42 * s, cy - 0.05 * s),
           (cx + 0.30 * s, cy + 0.52 * s), (cx + 0.05 * s, cy + 0.72 * s),
           (cx - 0.30 * s, cy + 0.52 * s), (cx - 0.44 * s, cy - 0.02 * s),
           (cx - 0.16 * s, cy - 0.34 * s)]
    d.polygon([(x * SS, y * SS) for x, y in pts], fill=col)
    inner = [(cx, cy + 0.05 * s), (cx + 0.18 * s, cy + 0.34 * s),
             (cx + 0.02 * s, cy + 0.60 * s), (cx - 0.18 * s, cy + 0.34 * s)]
    d.polygon([(x * SS, y * SS) for x, y in inner], fill=(255, 205, 90))


def icon_barrel(d, cx, cy, s, col):
    x0, y0, x1, y1 = cx - 0.62 * s, cy - 0.62 * s, cx + 0.02 * s, cy + 0.62 * s
    d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS],
                        radius=9 * SS, fill=col)
    for fy in (-0.28, 0.24):
        d.line([(x0 * SS, (cy + fy * s) * SS), (x1 * SS, (cy + fy * s) * SS)],
               fill=(10, 17, 32), width=5 * SS)
    # falling price arrow, clear diagonal with a triangular head
    ax, ay = cx + 0.22 * s, cy - 0.58 * s
    bx, by = cx + 0.80 * s, cy + 0.42 * s
    d.line([(ax * SS, ay * SS), (bx * SS, by * SS)], fill=RED, width=10 * SS)
    d.polygon([((bx - 0.34 * s) * SS, (by - 0.06 * s) * SS),
               ((bx - 0.04 * s) * SS, (by - 0.34 * s) * SS),
               (bx * SS, by * SS)], fill=RED)


def icon_burst(d, cx, cy, s, col):
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        x1 = cx + 0.78 * s * math.cos(a)
        y1 = cy + 0.78 * s * math.sin(a)
        d.line([(cx * SS, cy * SS), (x1 * SS, y1 * SS)], fill=col,
               width=8 * SS)
    d.ellipse([(cx - 0.30 * s) * SS, (cy - 0.30 * s) * SS,
               (cx + 0.30 * s) * SS, (cy + 0.30 * s) * SS], fill=(255, 205, 90))
    d.ellipse([(cx - 0.15 * s) * SS, (cy - 0.15 * s) * SS,
               (cx + 0.15 * s) * SS, (cy + 0.15 * s) * SS], fill=RED)


def icon_king(d, cx, cy, s, col):
    # chess king drawn from the DejaVu chess glyph
    f = ImageFont.truetype(FONT_REG, int(1.9 * s * SS))
    d.text((cx * SS, cy * SS), "\u265a", font=f, fill=col, anchor="mm")


# ---------------------------------------------------------------- tiles ----
def tile(d, x, y, w, h, accent, icon_fn, head, line1, line2):
    d.rounded_rectangle([x * SS, y * SS, (x + w) * SS, (y + h) * SS],
                        radius=14 * SS, fill=PANEL)
    d.rectangle([x * SS, y * SS, (x + w) * SS, (y + 10) * SS], fill=accent)
    icon_fn(d, x + 52, y + 62, 34, accent)
    fh = fit_font(FONT_BOLD, head, w - 108, 37)
    text(d, (x + 96, y + 34), head, fh, WHITE)
    f1 = fit_font(FONT_BOLD, line1, w - 24, 30)
    text(d, (x + 12, y + 108), line1, f1, accent)
    f2 = fit_font(FONT_REG, line2, w - 24, 24)
    text(d, (x + 12, y + 146), line2, f2, MUTED)


def render():
    img = Image.new("RGB", (W, H), BG)

    # ---- hero visual first: its glow blend must not wash out the type ----
    draw_globe(img, 824, 402, 168)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- top band: the date is the second-loudest thing on the page ----
    text(d, (48, 34), "THE WORLD IN ONE IMAGE", font(FONT_BOLD, 27), AMBER)
    text(d, (976, 34), "TUESDAY", font(FONT_BOLD, 27), MUTED, anchor="ra")
    text(d, (48, 66), "24 NOVEMBER 2026", font(FONT_BOLD, 66), WHITE)
    d.rectangle([48 * SS, 152 * SS, 976 * SS, 158 * SS], fill=RED)

    # ---- hero headline: the day's biggest story ----
    text(d, (48, 196), "ANTALYA, TURKIYE", font(FONT_BOLD, 26), SKY)
    text(d, (44, 224), "COP31", font(FONT_BOLD, 148), WHITE)
    f_col = fit_font(FONT_BOLD, "COLLAPSES", 636, 104)
    text(d, (44, 372), "COLLAPSES", f_col, RED)
    text(d, (48, 492), "NO DEAL. THE WORLD", font(FONT_BOLD, 41), WHITE)
    text(d, (48, 540), "REACTS IN ANGER.", font(FONT_BOLD, 41), WHITE)
    text(d, (48, 596), "Guterres: \u201cdeeply disappointed\u201d \u00b7 EU: hijacked",
         font(FONT_REG, 25), MUTED)
    text(d, (48, 628), "by oil states \u00b7 Island nations refuse to sign",
         font(FONT_REG, 25), MUTED)

    # ---- story band: four tiles, one fact each, readable at a glance ----
    ty, th, tw, gap = 692, 196, 226, 12
    tiles = [
        (RED, icon_flame, "FACTORY FIRE", "24 DEAD, 30 MISSING",
         "Candy factory, Banten"),
        (AMBER, icon_barrel, "OIL SLIDES", "BRENT $89.37",
         "Lowest since August"),
        (SKY, icon_burst, "KYIV STRUCK", "DRONES + MISSILES",
         "Fresh strikes, Kyiv region"),
        (VIOLET, icon_king, "CHESS FINAL", "GUKESH v SINDAROV",
         "Title match opens, Geneva"),
    ]
    for i, (accent, fn, head, l1, l2) in enumerate(tiles):
        tile(d, 48 + i * (tw + gap), ty, tw, th, accent, fn, head, l1, l2)

    # ---- footer: the rest of the day in one line ----
    d.rectangle([48 * SS, 916 * SS, 976 * SS, 919 * SS], fill=(52, 68, 98))
    foot = ("ALSO TODAY:  MODI + SHAH FLAG OFF AYODHYA\u2013JANAKPUR EXPRESS  \u00b7  "
            "ALCARAZ WINS FIRST ATP FINALS TITLE  \u00b7  PANT 128, WELLINGTON TEST DRAWN")
    ff = fit_font(FONT_BOLD, foot, 928, 21)
    text(d, (512, 938), foot, ff, MUTED, anchor="ma")
    text(d, (512, 972), "ANTALYA \u00b7 BANTEN \u00b7 HORMUZ \u00b7 KYIV \u00b7 GENEVA \u00b7 TURIN \u00b7 WELLINGTON",
         font(FONT_BOLD, 19), (110, 124, 152), anchor="ma")

    img = img.resize((1024, 1024), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
