#!/usr/bin/env python3
"""Broadsheet front page for 24 November 2026, expanded edition (v4).

Same discipline as broadsheet.py -- date as the biggest type, three
illustrated leads, status chip and named source on every story, a
day-in-numbers strip and a date-check box -- but with the story count
expanded using items verified in-session on 25 Nov from reputable
outlets' 24 November 2026 reporting:

  Hormuz mines claim (IRNA/Tasnim via Reuters; The Business Standard)
  Zaporizhzhia flats strike + 96-drone night (Ukrainian Air Force;
  Kyiv Independent; Just Security/AP) - Russia's 699-drone claim
  (Russian Defence Ministry via Kurdistan24; Meduza) - Benghazi
  corvette confirmation (AP; Office of the President of Ukraine) -
  Russian aircraft in Korea's air-defence zone (South Korea JCS via
  Just Security; Yonhap) - Gaza airstrikes kill six (Reuters) -
  Germany gets Ukraine's Delta system (Kyiv Independent) - China
  names crew, Pakistani astronaut to fly (AP) - Hanoi eatery blast
  kills six (AP) - Cartagena supermarket hostages (AP) - Pentagon
  rebukes Canada (AP) - Ituri fighting traps Ebola responders
  (UN News/WHO) - Iraqi PM oilfields order (Reuters) - NATO space
  warning (BBC) - Pope Francis diary published (AP) - Korea offers
  $375k rewards over AI exam cheating (Just Security).
Plus the verified set carried from this account's earlier entries:
COP31 fallout, Banten fire toll, Brent $89.37, Kyiv region strikes,
Gukesh v Sindarov, Ayodhya-Janakpur express, Alcaraz, Pant 128.
Monday's news (Nvidia's Huang reinstatement, the Megaspeed blacklist)
is excluded in the date-check box, as is the Benghazi strike itself --
only Kyiv's Tuesday confirmation is carried.
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
TAN = (238, 231, 210)


def F(path, size):
    return ImageFont.truetype(path, size * SS)


def T(d, xy, s, fnt, fill=INK, anchor="la", spacing=3):
    d.text((xy[0] * SS, xy[1] * SS), s, font=fnt, fill=fill,
           anchor=anchor, spacing=spacing * SS)


def fit(path, s, max_w, start, floor=10):
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
def art_tanker(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(16, 44, 74))
    # tanker hull + superstructure
    d.polygon([((x + 14) * SS, (y + h - 26) * SS), ((x + w - 30) * SS, (y + h - 26) * SS),
               ((x + w - 14) * SS, (y + h - 12) * SS), ((x + 26) * SS, (y + h - 12) * SS)],
              fill=(52, 52, 60))
    rect(d, x + 34, y + h - 38, w - 90, 12, fill=(52, 52, 60))
    rect(d, x + w - 52, y + h - 48, 16, 22, fill=(52, 52, 60))
    d.line([((x + 20) * SS, (y + h - 26) * SS), ((x + w - 36) * SS, (y + h - 26) * SS)],
           fill=(200, 60, 40), width=2 * SS)
    # fire on the waterline + waves
    for cx, s in [(x + 70, 15), (x + 92, 11)]:
        cy = y + h - 30
        d.polygon([(cx * SS, (cy - s) * SS), ((cx + 7) * SS, cy * SS),
                   ((cx + 3) * SS, (cy + 7) * SS), ((cx - 3) * SS, (cy + 7) * SS),
                   ((cx - 7) * SS, cy * SS)], fill=(245, 130, 32))
    for wx in range(x + 8, x + w - 16, 26):
        d.line([(wx * SS, (y + h - 6) * SS), ((wx + 12) * SS, (y + h - 6) * SS)],
               fill=(84, 169, 255), width=2 * SS)


def art_globe(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(16, 44, 74))
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 6
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
           width=4 * SS, joint="curve")


def art_kyiv(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(14, 24, 48))
    for bx, bh in [(14, 30), (48, 42), (90, 26), (124, 38), (164, 30),
                   (200, 40), (240, 28)]:
        if bx < w - 18:
            rect(d, x + bx, y + h - 12 - bh, 26, bh, fill=(8, 12, 24))
    for sx, sy, ex, ey in [(26, 10, 72, 34), (110, 6, 150, 30), (196, 12, 232, 34)]:
        if ex < w:
            d.line([((x + sx) * SS, (y + sy) * SS), ((x + ex) * SS, (y + ey) * SS)],
                   fill=(255, 205, 90), width=3 * SS)
            d.ellipse([((x + ex) - 6) * SS, ((y + ey) - 6) * SS,
                       ((x + ex) + 6) * SS, ((y + ey) + 6) * SS], fill=(255, 120, 50))


# ---------------------------------------------------------------- cards ----
def card(d, x, y, w, h, num, kicker, kcol, head, head_size, body, body_size,
         status, scol, source, art=None):
    rect(d, x, y, w, h, fill=CARD, outline=INK, width=2)
    cy = y + 7
    if art:
        art(d, x + 7, cy, w - 14, 62)
        cy += 69
    cf = F(SANS, 11)
    cw = int(cf.getlength(status) / SS) + 11
    T(d, (x + 9, cy), f"{num}  {kicker}",
      fit(SANS, f"{num}  {kicker}", w - cw - 26, 12), fill=kcol)
    rect(d, x + w - 9 - cw, cy - 1, cw, 17, fill=scol)
    T(d, (x + w - 9 - cw + 5, cy + 2), status, cf, fill=(255, 255, 255))
    cy += 21
    hf = fit(SERIF, head, w - 18, head_size)
    for ln in wrap(head, hf, w - 18):
        T(d, (x + 9, cy), ln, hf)
        cy += int(head_size * 1.1)
    cy += 1
    bf = F(SANSR, body_size)
    for ln in wrap(body, bf, w - 18):
        T(d, (x + 9, cy), ln, bf, fill=(46, 44, 40))
        cy += body_size + 4
    T(d, (x + 9, y + h - 17), source, fit(SANS, source, w - 18, 10), fill=MUT)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    rect(d, 0, 0, 1024, 26, fill=INK)
    strip = "ONE DAY OF WORLD NEWS ON ONE PAGE  ·  23 STORIES  ·  EVERY ONE DATED TUE 24 NOV 2026"
    T(d, (512, 5), strip, fit(SANS, strip, 990, 13), fill=(247, 242, 228), anchor="ma")
    T(d, (512, 36), "Tuesday 24 November 2026",
      fit(SERIF, "Tuesday 24 November 2026", 980, 62), anchor="ma")
    strap = "Iran says tankers hit mines in Hormuz  ·  COP31 fallout  ·  96 drones over Ukraine  ·  Banten toll confirmed"
    T(d, (512, 106), strap, fit(SANS, strap, 980, 15), fill=RED, anchor="ma")
    rect(d, 24, 130, 976, 4, fill=INK)

    # ---- day in numbers ----
    ny = 142
    rect(d, 24, ny, 976, 54, fill=TAN, outline=INK, width=2)
    T(d, (36, ny + 4), "THE DAY IN NUMBERS", F(SANS, 10), fill=RED)
    nums = [("96", "drones fired at Ukraine"), ("73", "downed by 08:00"),
            ("4", "tankers Iran says hit mines"), ("24", "dead in Banten fire"),
            ("$89.37", "Brent crude, 3-mo low")]
    nx = 36
    for val, lab in nums:
        T(d, (nx, ny + 16), val, F(SERIF, 21), fill=INK)
        T(d, (nx, ny + 39), lab, F(SANS, 9), fill=MUT)
        nx += 192

    # ---- leads ----
    ly, lh, lw, gap = 208, 264, 317, 12
    card(d, 24, ly, lw, lh, "1", "STRAIT OF HORMUZ · SHIPPING", RED,
         "Iran says tankers hit mines in Hormuz", 22,
         "Iran's Guards say three oil tankers struck naval mines and caught "
         "fire despite a US escort; a fourth was reported by Tuesday "
         "afternoon. The ships are unnamed and the claim is unverified; "
         "US Central Command has not responded.", 13,
         "CLAIM", RED, "Source: IRNA / Tasnim via Reuters", art=art_tanker)
    card(d, 24 + lw + gap, ly, lw, lh, "2", "ANTALYA · CLIMATE", RED,
         "COP31 ends with no deal; the world reacts in anger", 22,
         "Fury after the longest summit ever. Guterres: \u201cdeeply "
         "disappointed\u201d. The EU: hijacked by oil states. Panama: held "
         "hostage by the \u201cpetroleum mafia\u201d. Island nations refused "
         "to sign.", 13,
         "CONFIRMED", GREEN, "Source: statements in Antalya, day two", art=art_globe)
    card(d, 24 + 2 * (lw + gap), ly, lw, lh, "3", "UKRAINE · WAR", BLUE,
         "Russia fires 96 drones; Zaporizhzhia flats hit", 22,
         "Russia attacked overnight with 96 drones; air defences downed 73 "
         "by 08:00. In Zaporizhzhia a strike tore open a five-storey block: "
         "two dead, about 40 wounded, four of them children.", 13,
         "OFFICIAL", BLUE, "Source: Ukrainian Air Force; Kyiv Independent", art=art_kyiv)

    # ---- grid: six secondary stories ----
    gy, gh, gw = 484, 124, 317
    grid = [
        ("4", "CIKANDE, BANTEN", RED, "Factory fire toll confirmed: 24 dead", 17,
         "About 30 workers still missing in the ruins; DNA tests will name "
         "the dead and a safety probe opens into PT Fonusa.", 12,
         "CONFIRMED", GREEN, "Source: AP; Banten officials"),
        ("5", "MOSCOW · WAR", BLUE, "Russia says 699 drones downed", 17,
         "Moscow says 699 Ukrainian drones were intercepted overnight, 355 "
         "of them bound for the capital; two airports restricted flights.", 12,
         "CLAIM", RED, "Source: Russian Defence Ministry via Kurdistan24"),
        ("6", "BENGHAZI, LIBYA", BLUE, "Kyiv confirms corvette sunk at Benghazi", 17,
         "Zelenskyy confirms naval drones sank the Russian corvette Merkury "
         "at Benghazi. The strike itself was Monday's; the confirmation "
         "came Tuesday.", 12,
         "CONFIRMED", GREEN, "Source: AP; Office of the President of Ukraine"),
        ("7", "MARKETS · ENERGY", GOLD, "Brent slides to $89.37", 17,
         "Brent falls to $89.37, its lowest since August, as oil flows past "
         "the attacks. Trump eyes new strikes on Iran after New Year; "
         "OPEC+ meets Sunday.", 12,
         "REPORTED", GOLD, "Source: Tuesday market close"),
        ("8", "GENEVA · CHESS", BLUE, "World title match opens: Gukesh v Sindarov", 17,
         "Champion D Gukesh of India faces Javokhir Sindarov of Uzbekistan "
         "in Game 1 of the World Chess Championship in Geneva.", 12,
         "OFFICIAL", BLUE, "Source: FIDE match schedule"),
        ("9", "SEOUL · SECURITY", BLUE, "Russian jets enter Korea's air zone", 17,
         "South Korea's Joint Chiefs say several Russian aircraft flew "
         "inside the Korea air-defence identification zone on Tuesday.", 12,
         "OFFICIAL", BLUE, "Source: Yonhap; South Korea JCS"),
    ]
    for i, args in enumerate(grid):
        card(d, 24 + (i % 3) * (gw + gap), gy + (i // 3) * (gh + gap),
             gw, gh, *args)

    # ---- also on Tuesday: the rest of the day, one line each ----
    ay = gy + 2 * gh + gap + 8
    T(d, (24, ay), "ALSO ON TUESDAY 24 NOVEMBER", F(SANS, 14), fill=RED)
    rect(d, 24, ay + 20, 976, 2, fill=INK)
    items = [
        ("10", "GAZA", "Israeli airstrikes kill at least six Palestinians, incl. two police officers", "Reuters"),
        ("11", "BERLIN", "Germany first to gain access to Ukraine's Delta battlefield system", "Kyiv Independent"),
        ("12", "CHINA · SPACE", "China names new station crew; a Pakistani astronaut will fly", "AP"),
        ("13", "HANOI", "Blast at a hot-pot eatery kills six, injures more than a dozen", "AP"),
        ("14", "CARTAGENA", "Armed men seize a supermarket, hold at least 25 hostage", "AP"),
        ("15", "WASHINGTON", "Pentagon sharply rebukes Canada over defence spending, F-35 review", "AP"),
        ("16", "ITURI, DR CONGO", "Fighting near a hospital traps Ebola responders", "UN News"),
        ("17", "BAGHDAD", "Iraqi PM orders oil ministry to run fields in Kurdish-held areas", "Reuters"),
        ("18", "NATO", "Rutte vows defence against space threats after nuclear-satellite reports", "BBC"),
        ("19", "VATICAN", "Pope Francis's private diary, describing a spiritual crisis, is published", "AP"),
        ("20", "SEOUL · EXAMS", "Korea offers up to $375,000 to catch AI exam cheating", "Just Security"),
        ("21", "JANAKPUR", "Modi + Shah flag off Ayodhya\u2013Janakpur express", "Tuesday flag-off"),
        ("22", "TURIN", "Alcaraz beats Zverev, first ATP Finals title", "Tuesday final"),
        ("23", "WELLINGTON", "Pant 128 as India draw Test with New Zealand", "Tuesday close"),
    ]
    col_w, row_h = 482, 20
    for i, (num, place, text, src) in enumerate(items):
        cx = 24 + (i % 2) * (col_w + 12)
        cy = ay + 30 + (i // 2) * row_h
        line = f"{num}  {place}: {text} \u00b7 {src}"
        T(d, (cx, cy), line, fit(SANSR, line, col_w - 8, 12), fill=(46, 44, 40))

    # ---- date check ----
    dy = ay + 30 + 7 * row_h + 10
    rect(d, 24, dy, 976, 1024 - dy - 16, fill=TAN, outline=RED, width=3)
    T(d, (36, dy + 7), "DATE CHECK", F(SANS, 13), fill=RED)
    note = ("Every story on this page happened, or was first reported, on Tuesday 24 November 2026 (UTC or local date). "
            "Left out as Monday's news: Nvidia reinstates Jensen Huang as CEO; the US blacklists Singapore's Megaspeed; "
            "the Benghazi strike itself (Kyiv's confirmation came Tuesday). Iran's tanker claim is labelled CLAIM \u2014 unverified.")
    nf = F(SANSR, 12)
    cy = dy + 26
    for ln in wrap(note, nf, 952):
        T(d, (36, cy), ln, nf, fill=(46, 44, 40))
        cy += 16

    img = img.resize((1024, 1024), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
