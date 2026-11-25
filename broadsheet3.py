#!/usr/bin/env python3
"""Broadsheet front page for 24 November 2026, full edition (v5).

Third design iteration for this bounty, built against the current #1
entry's broadsheet: same apparatus (date masthead, region ticker,
day-in-numbers, three illustrated leads, numbered grid, one-line list,
world map with pins, date-check box) at 27 stories, with larger type
than the rival's microtext and stricter claim labelling.

Facts: the verified set from this account's earlier entries (COP31
fallout, Banten toll, Brent $89.37, Gukesh v Sindarov, Ayodhya-Janakpur
express, Alcaraz, Pant 128) plus stories verified in-session on
25 November 2026 against that Tuesday's reporting by reputable
outlets: Hormuz mines claim (IRNA/Tasnim via Reuters), the 96-drone
night and Zaporizhzhia strike (Ukrainian Air Force; Kyiv Independent),
Russia's 699 claim (Russian Defence Ministry via Kurdistan24),
Benghazi confirmation (AP), Korea air-zone incursion (Yonhap; JCS),
Poland airspace incursion (Polish Armed Forces), Dnipro station
strike and DTEK blackouts (DTEK), Gaza strikes (Reuters), Germany
Delta access (Kyiv Independent), China crew with Pakistani astronaut
(AP), Hanoi blast (AP), Cartagena hostages (AP), Pentagon-Canada
(AP), Ituri Ebola responders (UN News), Iraq oilfields (Reuters),
NATO space warning (BBC), Pope Francis diary (AP), Korea AI-exam
rewards (Just Security), Hasina return plan (AP), quasar discovery
(AP). Monday's news is excluded by name in the date-check box.
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
    # smoke plume
    for sx, sy, sr in [(x + 62, y + 12, 7), (x + 70, y + 8, 9), (x + 80, y + 6, 6)]:
        d.ellipse([(sx - sr) * SS, (sy - sr) * SS, (sx + sr) * SS, (sy + sr) * SS],
                  fill=(90, 90, 96))
    # tanker: hull, deck, superstructure, red waterline
    d.polygon([((x + 14) * SS, (y + h - 24) * SS), ((x + w - 40) * SS, (y + h - 24) * SS),
               ((x + w - 24) * SS, (y + h - 10) * SS), ((x + 26) * SS, (y + h - 10) * SS)],
              fill=(52, 52, 60))
    rect(d, x + 34, y + h - 36, w - 110, 12, fill=(52, 52, 60))
    rect(d, x + w - 66, y + h - 46, 16, 22, fill=(52, 52, 60))
    d.line([((x + 20) * SS, (y + h - 24) * SS), ((x + w - 46) * SS, (y + h - 24) * SS)],
           fill=(200, 60, 40), width=2 * SS)
    # flames amidships
    for cx, s in [(x + 58, 16), (x + 76, 12)]:
        cy = y + h - 36
        d.polygon([(cx * SS, (cy - s) * SS), ((cx + 7) * SS, cy * SS),
                   ((cx + 3) * SS, (cy + 7) * SS), ((cx - 3) * SS, (cy + 7) * SS),
                   ((cx - 7) * SS, cy * SS)], fill=(245, 130, 32))
    # escort silhouette astern + waves
    d.polygon([((x + w - 34) * SS, (y + h - 16) * SS), ((x + w - 8) * SS, (y + h - 16) * SS),
               ((x + w - 12) * SS, (y + h - 8) * SS), ((x + w - 30) * SS, (y + h - 8) * SS)],
              fill=(30, 30, 36))
    for wx in range(x + 8, x + w - 16, 26):
        d.line([(wx * SS, (y + h - 5) * SS), ((wx + 12) * SS, (y + h - 5) * SS)],
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


# ------------------------------------------------------------ world map ----
MAP = [
    "........................................................",
    ".....##......................................#..........",
    "...######..............#...........##################...",
    "..########......##...###..........###################...",
    "..#########....#####..##.........##################....",
    "...########.....###..####.......################.......",
    "....######.......##...#####......##############.........",
    ".....#####............#######.....############..........",
    "......####.............#######################..........",
    ".......###..............#####################...........",
    ".......##................##################.............",
    "......###.................################..............",
    ".....####..................##############...............",
    "....#####....................##########.................",
    "...######.....................########..................",
    "...#####.......................######...................",
    "...####.........................####..........##........",
    "...###..........................##..........######......",
    "...##......................................########.....",
    "...#........................................######......",
    "................................................##......",
    "........................................................",
]
# pin: (story number, lon, lat)
PINS = [("1", 56, 26), ("2", 31, 37), ("3", 32, 49), ("4", 107, -6),
        ("5", 38, 56), ("6", 20, 32), ("8", 6, 46), ("9", 127, 37)]


def draw_map(d, x, y, w, h):
    rect(d, x, y, w, h, fill=(233, 238, 244), outline=INK, width=2)
    T(d, (x + 9, y + 5), "WHERE IT HAPPENED", F(SANS, 11), fill=RED)
    T(d, (x + w - 9, y + 6), "pins: stories 1-9", F(SANS, 8), fill=MUT, anchor="ra")
    rows, cols = len(MAP), len(MAP[0])
    gw, gh = w - 16, h - 30
    cell = min(gw / cols, gh / rows)
    gx = x + (w - cols * cell) / 2
    gy = y + 26
    r = max(1.1, cell * 0.30)
    for ri, row in enumerate(MAP):
        for ci, ch in enumerate(row):
            if ch == "#":
                cx, cy = gx + ci * cell, gy + ri * cell
                d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
                          fill=(120, 140, 160))
    for num, lon, lat in PINS:
        px = gx + (lon + 180) / 360 * cols * cell
        py = gy + (78 - lat) / 136 * rows * cell
        d.ellipse([(px - 6) * SS, (py - 6) * SS, (px + 6) * SS, (py + 6) * SS],
                  fill=RED, outline=(255, 255, 255), width=1 * SS)
        T(d, (px, py - 5), num, F(SANS, 8), fill=(255, 255, 255), anchor="ma")


# ---------------------------------------------------------------- cards ----
def card(d, x, y, w, h, num, kicker, kcol, head, head_size, body, body_size,
         status, scol, source, art=None):
    rect(d, x, y, w, h, fill=CARD, outline=INK, width=2)
    cy = y + 7
    if art:
        art(d, x + 7, cy, w - 14, 60)
        cy += 67
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
    strip = "ONE DAY OF WORLD NEWS ON ONE PAGE  ·  27 STORIES  ·  EVERY ONE DATED TUE 24 NOV 2026"
    T(d, (512, 5), strip, fit(SANS, strip, 990, 13), fill=(247, 242, 228), anchor="ma")
    T(d, (512, 34), "Tuesday 24 November 2026",
      fit(SERIF, "Tuesday 24 November 2026", 980, 58), anchor="ma")
    strap = "Iran says tankers hit mines in Hormuz  ·  COP31 fallout  ·  96 drones over Ukraine  ·  Banten toll confirmed"
    T(d, (512, 100), strap, fit(SANS, strap, 980, 15), fill=RED, anchor="ma")
    rect(d, 24, 122, 976, 4, fill=INK)
    tick = "EUROPE 10  ·  MIDDLE EAST 3  ·  ASIA 7  ·  AFRICA 2  ·  AMERICAS 2  ·  OCEANIA 1  ·  WORLD 2"
    T(d, (512, 131), tick, fit(SANS, tick, 980, 13), fill=MUT, anchor="ma")

    # ---- day in numbers ----
    ny = 150
    rect(d, 24, ny, 976, 52, fill=TAN, outline=INK, width=2)
    T(d, (36, ny + 4), "THE DAY IN NUMBERS", F(SANS, 10), fill=RED)
    nums = [("96", "drones fired at Ukraine"), ("73", "downed by 08:00"),
            ("4", "tankers Iran says hit mines"), ("24", "dead in Banten fire"),
            ("$89.37", "Brent crude, 3-mo low")]
    nx = 36
    for val, lab in nums:
        T(d, (nx, ny + 15), val, F(SERIF, 20), fill=INK)
        T(d, (nx, ny + 37), lab, F(SANS, 9), fill=MUT)
        nx += 192

    # ---- leads ----
    ly, lh, lw, gap = 214, 256, 317, 12
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

    # ---- grid ----
    gy, gh, gw = 482, 118, 317
    grid = [
        ("4", "CIKANDE, BANTEN", RED, "Factory fire toll confirmed: 24 dead", 17,
         "About 30 workers still missing in the ruins; DNA tests will name "
         "the dead, safety probe opens into PT Fonusa.", 12,
         "CONFIRMED", GREEN, "Source: AP; Banten officials"),
        ("5", "MOSCOW · WAR", BLUE, "Russia says 699 drones downed", 17,
         "Moscow says 699 Ukrainian drones were intercepted overnight, 355 "
         "bound for the capital; two airports restricted.", 12,
         "CLAIM", RED, "Source: Russian Defence Ministry via Kurdistan24"),
        ("6", "BENGHAZI, LIBYA", BLUE, "Kyiv confirms corvette sunk at Benghazi", 17,
         "Zelenskyy confirms naval drones sank the corvette Merkury at "
         "Benghazi. Strike was Monday's; confirmation Tuesday.", 12,
         "CONFIRMED", GREEN, "Source: AP; Office of the President of Ukraine"),
        ("7", "MARKETS · ENERGY", GOLD, "Brent slides to $89.37", 17,
         "Brent falls to $89.37, lowest since August, as oil flows past the "
         "attacks. Trump eyes Iran strikes; OPEC+ meets Sunday.", 12,
         "REPORTED", GOLD, "Source: Tuesday market close"),
        ("8", "GENEVA · CHESS", BLUE, "World title match opens: Gukesh v Sindarov", 17,
         "Champion D Gukesh of India faces Javokhir Sindarov of Uzbekistan "
         "in Game 1 in Geneva.", 12,
         "OFFICIAL", BLUE, "Source: FIDE match schedule"),
    ]
    for i, args in enumerate(grid):
        card(d, 24 + (i % 3) * (gw + gap), gy + (i // 3) * (gh + gap),
             gw, gh, *args)
    # the sixth grid cell is the map
    draw_map(d, 24 + 2 * (gw + gap), gy + gh + gap, gw, gh)

    # ---- also on Tuesday: three columns, full width ----
    ay = gy + 2 * gh + gap + 6
    T(d, (24, ay), "ALSO ON TUESDAY 24 NOVEMBER", F(SANS, 14), fill=RED)
    rect(d, 24, ay + 20, 976, 2, fill=INK)
    items = [
        ("9", "SEOUL", "Russian jets enter Korea's air zone", "Yonhap"),
        ("10", "GAZA", "Airstrikes kill six, incl. two police", "Reuters"),
        ("11", "BERLIN", "Germany first gains Delta access", "Kyiv Independent"),
        ("12", "CHINA · SPACE", "Crew named; Pakistani astronaut flies", "AP"),
        ("13", "HANOI", "Hot-pot eatery blast kills six", "AP"),
        ("14", "CARTAGENA", "Gunmen hold 25+ hostage in a store", "AP"),
        ("15", "WASHINGTON", "Pentagon rebukes Canada, F-35", "AP"),
        ("16", "ITURI", "Fighting traps Ebola responders", "UN News"),
        ("17", "BAGHDAD", "PM orders ministry to run oil fields", "Reuters"),
        ("18", "NATO", "Rutte vows defence vs space threats", "BBC"),
        ("19", "VATICAN", "Pope Francis's diary published", "AP"),
        ("20", "SEOUL", "$375,000 to catch AI exam cheating", "Just Security"),
        ("21", "POLAND", "Drone 20 km in, 23:49", "Polish Armed Forces"),
        ("22", "DNIPRO", "Station hit; 353,000 homes dark", "DTEK"),
        ("23", "DHAKA", "Hasina plans return home 16 Dec", "AP"),
        ("24", "JANAKPUR", "Modi + Shah flag off the express", "Tuesday"),
        ("25", "TURIN", "Alcaraz wins first ATP Finals title", "Tuesday"),
        ("26", "WELLINGTON", "Pant 128, Test drawn", "Tuesday"),
        ("27", "DEEP SPACE", "Quasar from 630m yrs after Big Bang", "AP"),
    ]
    col_w, row_h = 317, 19
    for i, (num, place, text, src) in enumerate(items):
        cx = 24 + (i % 3) * (col_w + 12)
        cy = ay + 28 + (i // 3) * row_h
        line = f"{num}  {place}: {text} \u00b7 {src}"
        T(d, (cx, cy), line, fit(SANSR, line, col_w - 4, 11), fill=(46, 44, 40))

    # ---- date check ----
    dy = ay + 28 + 7 * row_h + 12
    note = ("Every story on this page happened, or was first reported, on Tuesday 24 November 2026 (UTC or local date). "
            "Left out as Monday's news: Nvidia reinstates Jensen Huang as CEO; the US blacklists Singapore's Megaspeed; "
            "the Benghazi strike itself (Kyiv's confirmation came Tuesday). Unverified claims are labelled CLAIM. "
            "Map and pictures drawn for this page; no photographs.")
    nf = F(SANSR, 11)
    note_lines = wrap(note, nf, 952)
    rect(d, 24, dy, 976, 23 + len(note_lines) * 15 + 9, fill=TAN, outline=RED, width=3)
    T(d, (36, dy + 6), "DATE CHECK", F(SANS, 12), fill=RED)
    cy = dy + 23
    for ln in note_lines:
        T(d, (36, cy), ln, nf, fill=(46, 44, 40))
        cy += 15

    img = img.resize((1024, 1024), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
