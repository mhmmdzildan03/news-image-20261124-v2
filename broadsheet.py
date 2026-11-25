#!/usr/bin/env python3
"""Broadsheet front page for 24 November 2026 world news (v3 design).

One page, hierarchically organized: the date is the biggest type on the
page, three illustrated lead stories, a disciplined grid of secondary
stories, a day-in-numbers strip, a status chip and basis line on every
story, and a date-check box. Facts are ONLY the verified 24 Nov 2026 set
carried by this account's earlier entries for the day:

  COP31 Antalya fallout (no deal; Guterres "deeply disappointed"; EU:
  hijacked by oil states; Panama: "petroleum mafia"; island nations
  refused to sign) - Cikande candy-factory fire, Banten: 24 dead
  confirmed, ~30 missing, DNA tests, safety probe into PT Fonusa -
  Brent crude $89.37, lowest since August, oil flowing past Hormuz
  attacks, Trump eyes Iran strikes after New Year, OPEC+ meets Sunday -
  fresh drone and missile strikes on Kyiv region; block search, missing
  feared dead; Sparta II still burning - World Chess Championship opens
  in Geneva, Game 1: Gukesh v Sindarov - Modi + Shah flag off the
  Ayodhya-Janakpur Saryu-Kamala Express - Alcaraz beats Zverev in Turin
  for his first ATP Finals title - Pant 128, Wellington Test drawn.

Rendered with Pillow at 2x supersampling; entry.png is 1024x1024.
"""
import os

from PIL import Image, ImageDraw, ImageFont

SS = 2
W = H = 1024 * SS
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANSR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 242, 228)
CARD = (255, 253, 246)
INK = (24, 24, 28)
MUT = (96, 92, 82)
RED = (178, 32, 28)
BLUE = (36, 78, 158)
GOLD = (150, 112, 14)
GREEN = (38, 110, 66)
LINE = (24, 24, 28)


def F(path, size):
    return ImageFont.truetype(path, size * SS)


def T(d, xy, s, fnt, fill=INK, anchor="la", spacing=3):
    d.text((xy[0] * SS, xy[1] * SS), s, font=fnt, fill=fill,
           anchor=anchor, spacing=spacing * SS)


def fit(path, s, max_w, start, floor=12):
    size = start
    while size > floor:
        f = F(path, size)
        if f.getlength(s) / SS <= max_w:
            return f
        size -= 1
    return F(path, floor)


def wrap(s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) / SS <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rect(d, x, y, w, h, fill=None, outline=None, width=2):
    d.rectangle([x * SS, y * SS, (x + w) * SS, (y + h) * SS],
                fill=fill, outline=outline, width=width * SS)


# ------------------------------------------------------------- mini art ----
def art_globe(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(16, 44, 74))
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 10
    d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
              fill=(30, 100, 160))
    for dx, dy, rx, ry in [(-.45, -.35, .26, .16), (.05, -.45, .3, .15),
                           (.35, -.05, .2, .2), (.0, .18, .2, .24),
                           (.48, .38, .18, .11)]:
        d.ellipse([(cx + (dx - rx) * r) * SS, (cy + (dy - ry) * r) * SS,
                   (cx + (dx + rx) * r) * SS, (cy + (dy + ry) * r) * SS],
                  fill=(52, 168, 92))
    pts = [(cx - .2 * r, cy - .95 * r), (cx - .02 * r, cy - .55 * r),
           (cx - .18 * r, cy - .25 * r), (cx + .06 * r, cy + .05 * r),
           (cx - .08 * r, cy + .4 * r), (cx + .02 * r, cy + .95 * r)]
    d.line([(px * SS, py * SS) for px, py in pts], fill=(255, 170, 60),
           width=5 * SS, joint="curve")


def art_fire(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(52, 30, 26))
    # factory silhouette, low in the box so the flames fit above it
    rect(d, x + 18, y + h - 28, w - 36, 20, fill=(16, 14, 14))
    rect(d, x + 30, y + h - 42, 14, 16, fill=(16, 14, 14))
    rect(d, x + 56, y + h - 42, 14, 16, fill=(16, 14, 14))
    for i in range(5):
        rect(d, x + 30 + i * 26, y + h - 20, 9, 8, fill=(255, 190, 80))
    # flames: bases on the roof line, tips stay inside the box
    for cx, s, col in [(x + w // 2 - 22, 22, (232, 62, 42)),
                       (x + w // 2 + 14, 27, (245, 130, 32)),
                       (x + w // 2 - 2, 17, (255, 200, 80))]:
        cy = y + h - 42
        d.polygon([(cx * SS, (cy - s) * SS), ((cx + s * .42) * SS, (cy + 3) * SS),
                   ((cx + s * .18) * SS, (cy + 11) * SS), ((cx - s * .2) * SS, (cy + 11) * SS),
                   ((cx - s * .42) * SS, (cy + 3) * SS)], fill=col)


def art_kyiv(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(14, 24, 48))
    # skyline
    for bx, bh in [(16, 44), (52, 62), (96, 38), (132, 56), (176, 42),
                   (216, 60), (258, 40)]:
        if bx < w - 20:
            rect(d, x + bx, y + h - 18 - bh, 30, bh, fill=(8, 12, 24))
    # streaks + bursts
    for sx, sy, ex, ey in [(30, 16, 84, 52), (120, 10, 168, 46), (210, 18, 250, 50)]:
        if ex < w:
            d.line([( (x + sx) * SS, (y + sy) * SS), ((x + ex) * SS, (y + ey) * SS)],
                   fill=(255, 205, 90), width=4 * SS)
            d.ellipse([((x + ex) - 8) * SS, ((y + ey) - 8) * SS,
                       ((x + ex) + 8) * SS, ((y + ey) + 8) * SS], fill=(255, 120, 50))
    d.line([(x * SS, (y + h - 16) * SS), ((x + w) * SS, (y + h - 16) * SS)],
           fill=(255, 205, 90), width=3 * SS)


# ---------------------------------------------------------------- cards ----
def chip(d, x, y, label, col):
    f = F(SANS, 13)
    w = int(f.getlength(label) / SS) + 14
    rect(d, x, y, w, 20, fill=col)
    T(d, (x + 7, y + 3), label, f, fill=(255, 255, 255))
    return w


def story_card(d, x, y, w, h, num, kicker, kcol, head, head_size, body,
               status, scol, basis, art=None):
    rect(d, x, y, w, h, fill=CARD, outline=LINE, width=2)
    cy = y + 8
    if art:
        art(d, x + 8, cy, w - 16, 86)
        cy += 94
    # kicker row: number + region, fitted so it never reaches the chip
    cf = F(SANS, 12)
    cw = int(cf.getlength(status) / SS) + 12
    T(d, (x + 10, cy), f"{num}  {kicker}",
      fit(SANS, f"{num}  {kicker}", w - cw - 30, 13), fill=kcol)
    rect(d, x + w - 10 - cw, cy - 1, cw, 19, fill=scol)
    T(d, (x + w - 10 - cw + 6, cy + 2), status, cf, fill=(255, 255, 255))
    cy += 24
    hf = fit(SERIF, head, w - 20, head_size)
    for ln in wrap(head, hf, w - 20):
        T(d, (x + 10, cy), ln, hf)
        cy += int(head_size * 1.12)
    cy += 2
    bf = F(SANSR, 15)
    for ln in wrap(body, bf, w - 20):
        T(d, (x + 10, cy), ln, bf, fill=(46, 44, 40))
        cy += 19
    T(d, (x + 10, y + h - 20), basis, fit(SANS, basis, w - 20, 11),
      fill=MUT)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip + masthead: the date is the biggest type on the page --
    rect(d, 0, 0, 1024, 30, fill=INK)
    T(d, (512, 6), "ONE DAY OF WORLD NEWS ON ONE PAGE  ·  8 STORIES  ·  EVERY ONE DATED TUE 24 NOV 2026",
      fit(SANS, "ONE DAY OF WORLD NEWS ON ONE PAGE  ·  8 STORIES  ·  EVERY ONE DATED TUE 24 NOV 2026", 980, 15),
      fill=(247, 242, 228), anchor="ma")
    T(d, (512, 44), "Tuesday 24 November 2026",
      fit(SERIF, "Tuesday 24 November 2026", 980, 74), anchor="ma")
    T(d, (512, 128), "COP31 fallout leads the day  ·  Banten toll confirmed  ·  Oil slides  ·  Kyiv struck  ·  Chess title match opens",
      fit(SANS, "COP31 fallout leads the day  ·  Banten toll confirmed  ·  Oil slides  ·  Kyiv struck  ·  Chess title match opens", 980, 16),
      fill=RED, anchor="ma")
    rect(d, 24, 156, 976, 4, fill=INK)
    T(d, (512, 166), "ANTALYA 1 · BANTEN 1 · KYIV 1 · HORMUZ 1 · GENEVA 1 · JANAKPUR 1 · TURIN 1 · WELLINGTON 1",
      fit(SANS, "ANTALYA 1 · BANTEN 1 · KYIV 1 · HORMUZ 1 · GENEVA 1 · JANAKPUR 1 · TURIN 1 · WELLINGTON 1", 980, 14),
      fill=MUT, anchor="ma")

    # ---- day in numbers ----
    ny = 190
    rect(d, 24, ny, 976, 72, fill=(238, 231, 210), outline=LINE, width=2)
    T(d, (36, ny + 5), "THE DAY IN NUMBERS", F(SANS, 11), fill=RED)
    nums = [("24", "dead in Banten fire"), ("~30", "still missing"),
            ("$89.37", "Brent crude, 3-mo low"), ("128", "Pant's runs, Wellington"),
            ("1", "game played, Geneva")]
    nx = 36
    for val, lab in nums:
        T(d, (nx, ny + 20), val, F(SERIF, 25), fill=INK)
        T(d, (nx, ny + 50), lab, F(SANS, 10), fill=MUT)
        nx += 192

    # ---- three leads ----
    ly, lh, lw, gap = 274, 328, 317, 12
    story_card(d, 24, ly, lw, lh, "1", "ANTALYA · CLIMATE", RED,
               "COP31 ends with no deal; the world reacts in anger", 25,
               "Fury after the longest summit ever. Guterres: \u201cdeeply "
               "disappointed\u201d. The EU: hijacked by oil states. Panama: the "
               "world is held hostage by the \u201cpetroleum mafia\u201d. Island "
               "nations refused to sign.",
               "CONFIRMED", GREEN, "Basis: statements in Antalya, day two",
               art=art_globe)
    story_card(d, 24 + lw + gap, ly, lw, lh, "2", "CIKANDE, BANTEN", RED,
               "Factory fire toll confirmed: 24 dead, 30 missing", 25,
               "The 24 dead are confirmed in the candy factory blaze; about 30 "
               "workers are still missing in the ruins. DNA tests will name the "
               "dead, and a safety probe opens into PT Fonusa.",
               "CONFIRMED", GREEN, "Basis: Banten toll as confirmed Tuesday",
               art=art_fire)
    story_card(d, 24 + 2 * (lw + gap), ly, lw, lh, "3", "KYIV REGION · WAR", BLUE,
               "Fresh drone and missile strikes hit Kyiv region", 25,
               "Fresh drone and missile strikes hit the Kyiv region. The block "
               "search goes on and the missing are feared dead. At sea, the "
               "Sparta II cargo ship still burns.",
               "REPORTED", GOLD, "Basis: Tuesday strike reports, Kyiv",
               art=art_kyiv)

    # ---- secondary grid: 3 + 2 + date-check ----
    sy, sh, sw = 614, 176, 317
    story_card(d, 24, sy, sw, sh, "4", "STRAIT OF HORMUZ", GOLD,
               "Oil slides: Brent falls to $89.37", 21,
               "Brent falls to $89.37, its lowest since August, as oil flows "
               "past the attacks. Trump eyes new strikes on Iran after New "
               "Year; OPEC+ meets on Sunday.",
               "REPORTED", GOLD, "Basis: Tuesday market close")
    story_card(d, 24 + sw + gap, sy, sw, sh, "5", "GENEVA · CHESS", BLUE,
               "World title match opens: Gukesh v Sindarov", 21,
               "The World Chess Championship opens today: champion D Gukesh "
               "of India faces Javokhir Sindarov of Uzbekistan in Game 1 "
               "in Geneva.",
               "OFFICIAL", BLUE, "Basis: FIDE match schedule, Game 1")
    story_card(d, 24 + 2 * (sw + gap), sy, sw, sh, "6", "INDIA–NEPAL · RAIL", GREEN,
               "Modi + Shah flag off Ayodhya–Janakpur express", 21,
               "Modi and Shah flag off the Saryu-Kamala Express, linking "
               "Ayodhya and Janakpur across the India–Nepal border.",
               "OFFICIAL", BLUE, "Basis: Tuesday flag-off, Ayodhya")
    sy2 = sy + sh + gap
    story_card(d, 24, sy2, sw, sh, "7", "TURIN · TENNIS", GREEN,
               "Alcaraz wins his first ATP Finals title", 21,
               "Alcaraz beats Zverev in Turin to win his first ATP Finals "
               "title.",
               "CONFIRMED", GREEN, "Basis: Tuesday final, Turin")
    story_card(d, 24 + sw + gap, sy2, sw, sh, "8", "WELLINGTON · CRICKET", GREEN,
               "Pant hits 128 as the Test ends drawn", 21,
               "Rishabh Pant hits 128 as India draw with New Zealand at "
               "Wellington.",
               "CONFIRMED", GREEN, "Basis: Tuesday close, Wellington")
    # date-check box as the sixth cell
    bx = 24 + 2 * (sw + gap)
    rect(d, bx, sy2, sw, sh, fill=(238, 231, 210), outline=RED, width=3)
    T(d, (bx + 10, sy2 + 8), "DATE CHECK", F(SANS, 15), fill=RED)
    bf = F(SANSR, 13)
    note = ("Every story on this page happened, or was first reported, on "
            "Tuesday 24 November 2026. Where a story began earlier — the "
            "Antalya summit, the Cikande fire — only Tuesday's news is "
            "stated: the reactions, the confirmed toll, the day's strikes. "
            "Monday's news is left out.")
    cy = sy2 + 32
    for ln in wrap(note, bf, sw - 20):
        T(d, (bx + 10, cy), ln, bf, fill=(46, 44, 40))
        cy += 17

    img = img.resize((1024, 1024), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
