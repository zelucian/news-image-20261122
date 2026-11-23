#!/usr/bin/env python3
"""Draw the news-image-20261122 front page (v2, winner-formula layout).

Deterministic PIL generator (build time only). Writes entry.png next to
this file. No randomness, no timestamps, no PNG metadata, so repeated
runs produce byte-identical output.

Layout follows the dense broadsheet formula: masthead + counts strip,
a UTC timeline of the day, three numbered hero panels, a numbered
12-story grid keyed to a world map, two dense briefs columns, and a
DATE CHECK box listing older stories deliberately left out.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (250, 247, 238)   # off-white newsprint
INK = (18, 18, 18)        # near-black ink
RED = (178, 34, 34)       # single red accent
GREEN = (34, 102, 54)     # CONFIRMED status
RUST = (166, 66, 22)      # REPORTED status
BLUE = (38, 84, 124)      # flat illustration blue
SAND = (214, 205, 182)    # map land fill
LIGHT = (238, 233, 219)   # panel tint
GREY = (90, 88, 82)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_O = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

_fcache = {}


def F(path, size):
    key = (path, size)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(path, size)
    return _fcache[key]


# ---------------------------------------------------------------- data

HEROES = [
    {
        "n": 1, "tag": "GLOBAL · CLIMATE", "art": "globe",
        "headline": "COP31 ends without a deal over fossil fuels",
        "deck": "The \u201cAntalya Pact\u201d fails after the EU, UK and vulnerable "
                "states reject a text omitting fossil fuels. Narrower "
                "decisions pass.",
        "status": ("CONFIRMED", "AFP"),
    },
    {
        "n": 2, "tag": "AFRICA · WAR", "art": "ship",
        "headline": "Sea drones strike Russian corvette at Benghazi",
        "deck": "Libyan officials say six sea drones attacked the corvette "
                "Merkury \u2014 four downed, two hit \u2014 and a second ship "
                "was targeted.",
        "status": ("REPORTED", "LIBYAN OFFICIALS"),
    },
    {
        "n": 3, "tag": "SPACE · SCIENCE", "art": "mercury",
        "headline": "BepiColombo reaches Mercury after eight years",
        "deck": "ESA confirms the Europe\u2013Japan probe in orbit \u2014 only "
                "the second mission to orbit Mercury \u2014 but a glitch cut "
                "its burn short.",
        "status": ("CONFIRMED", "ESA"),
    },
]

GRID = [
    {"n": 4, "tag": "EUROPE · WAR",
     "headline": "Drone partly collapses apartment block near Kyiv",
     "deck": "Block partly collapses; 14 missing, six dead nearby.",
     "status": ("REPORTED", "BBC")},
    {"n": 5, "tag": "AFRICA · WAR",
     "headline": "Drones hit homes and a UN building in Khartoum",
     "deck": "Army accuses Ethiopia; RSF strikes kill civilians.",
     "status": ("REPORTED", "FRANCE 24")},
    {"n": 6, "tag": "MIDDLE EAST · CONFLICT",
     "headline": "Settlers torch vehicles in West Bank villages",
     "deck": "Torched near Ramallah; Eisenkot: \u201cJewish terrorism\u201d.",
     "status": ("REPORTED", "FRANCE 24")},
    {"n": 7, "tag": "MIDDLE EAST · CONFLICT",
     "headline": "Israeli strikes kill three in Gaza",
     "deck": "Two killed by fire; drone strike near Deir al-Balah.",
     "status": ("REPORTED", "MIDDLE EAST EYE")},
    {"n": 8, "tag": "MIDDLE EAST · POLITICS",
     "headline": "Likud and Yashar end coalition talks with no deal",
     "deck": "Talks fail over who leads; Eisenkot has until 6 Dec.",
     "status": ("REPORTED", "AL JAZEERA")},
    {"n": 9, "tag": "MIDDLE EAST · CONFLICT",
     "headline": "Houthis claim attack on Saudi oil refinery",
     "deck": "Coalition says it intercepted a drone and a missile.",
     "status": ("REPORTED", "THE HINDU")},
    {"n": 10, "tag": "MIDDLE EAST · DIPLOMACY",
     "headline": "Trump dares Iran to break the US port blockade",
     "deck": "Trump wants a \u201cpermanent\u201d deal; 14 tankers at Kharg.",
     "status": ("REPORTED", "FOX NEWS")},
    {"n": 11, "tag": "N. AMERICA · POLITICS",
     "headline": "Democrats win largest House majority since 1992",
     "deck": "NC recount takes Democrats to 258 seats; GOP holds 173.",
     "status": ("CONFIRMED", "BBC")},
    {"n": 12, "tag": "ASIA · POLITICS",
     "headline": "Hong Kong Election Committee: record turnout",
     "deck": "Turnout nears 99%; 856 candidates stood for 723 seats.",
     "status": ("CONFIRMED", "SCMP")},
    {"n": 13, "tag": "ASIA · TRADE",
     "headline": "China firmly opposes US FCC telecom vote",
     "deck": "Vote bars Chinese telecom firms from US phone numbers.",
     "status": ("CONFIRMED", "REUTERS")},
    {"n": 14, "tag": "EUROPE · SPORT",
     "headline": "Liverpool thrash Man Utd 4-0 on Pochettino debut",
     "deck": "Yoro sent off at 8 minutes; four scorers; United 19th.",
     "status": ("CONFIRMED", "REUTERS")},
    {"n": 15, "tag": "EUROPE · TECHNOLOGY",
     "headline": "UN talks on AI weapons end with no binding rules",
     "deck": "Only two more years of talks agreed; Red Cross warns.",
     "status": ("REPORTED", "CBC")},
]

BRIEFS_A = [  # Americas · Africa · Middle East · Oceania
    ("US", "ICE agents detain two at Seattle airport; outcry follows"),
    ("US", "FBI probes reported hack of its crime database"),
    ("US", "Man convicted of starting 2025 Palisades fire that killed 12"),
    ("US", "Skubal reportedly agrees $450m, nine-year Mets deal"),
    ("US", "Kansas City Current win first NWSL title, 2-1 over Spirit"),
    ("US", "Trump orders contractors to report congressional requests"),
    ("US", "Democrats win the Senate as well as the House in midterms"),
    ("HAITI", "Haiti, El Salvador agree to build three prisons"),
    ("COLOMBIA", "Boca Juniors win Copa Sudamericana, 2-0 over Mineiro"),
    ("S. AFRICA", "Ex-deputy president Mlambo-Ngcuka dies at 71"),
    ("RWANDA", "Five EU states agree deportation-centre deal"),
    ("ZIMBABWE", "Author cleared of using AI for his prize story"),
    ("IRAN", "Scheduled blackouts resume with the cold season"),
    ("LEBANON", "Aoun links sovereignty to ending occupation, interference"),
    ("GULF OF OMAN", "UK agency reports tanker incident with military forces"),
    ("COOK ISLANDS", "Cyclone Xavier weakens; all on Nassau safe"),
]

BRIEFS_B = [  # Europe · Asia · Science · Culture
    ("ENGLAND", "Leeds win 4-1 at Chelsea, first there since 1999"),
    ("ENGLAND", "UK set to be confirmed as 2035 Women's World Cup host"),
    ("DENMARK", "Russian attach\u00e9 expelled over alleged rapper plot"),
    ("T\u00dcRK\u0130YE", "Thousands march over state takeover of media in Istanbul"),
    ("BELGIUM", "Air controllers join Monday strike; flights to halt"),
    ("ITALY", "Alcaraz wins first ATP Finals title, beating Zverev"),
    ("PORTUGAL", "M\u00e1rquez ties Agostini with eighth MotoGP crown"),
    ("NEPAL", "PM Shah begins first India visit; Modi talks Monday"),
    ("BANGLADESH", "Garment workers clash with police near Dhaka"),
    ("BANGLADESH", "773 arrested in two Dhaka security operations"),
    ("THAILAND", "MP's royal defamation conviction upheld; term cut"),
    ("INDONESIA", "Six body bags found; 36 missing in factory fire"),
    ("JAPAN", "Shuri Castle main hall restored, seven years on"),
    ("S. KOREA", "Education minister quits over AI cheating scandal"),
    ("S. KOREA", "Ateez tops Billboard 200 for the fourth time"),
    ("SCIENCE", "Whale genome sequenced from drone-caught breath"),
    ("SCIENCE", "Earth gains a temporary mini-moon, 2026 QQ8"),
    ("CULTURE", "Miley Cyrus marries Maxx Morando in California"),
]

TIMELINE = [  # (utc hour, label, above?)
    (0.27, "00:16 Trump seeks permanent Iran deal", True),
    (1.95, "01:57 China opposes FCC vote", False),
    (6.00, "06:00 COP31 closing plenary", True),
    (9.52, "09:31 ESA confirms Mercury capture", False),
    (14.00, "14:00 Hull v Brighton kick-off", True),
    (16.50, "16:30 Liverpool v Man Utd kick-off", False),
]

DATECHECK = [
    "ICJ: Myanmar committed genocide vs Rohingya \u2014 Thu 19 Nov",
    "Trump, Xi, Putin meet in Shenzhen summit \u2014 Thu 19 Nov",
    "UK\u2013EU post-Brexit package agreed in Brussels \u2014 Fri 20 Nov",
    "\u201cEl Chapo Isidro\u201d captured in Guasave, Mexico \u2014 Fri 20 Nov",
    "Nigeria boat capsize kills 24 mourners \u2014 Fri 20 Nov",
    "Iranian strike hits Sitra site, Bahrain \u2014 Sat 21 Nov",
    "BepiColombo's Mercury burn fires \u2014 Sat 21 Nov",
    "Voyager 1 passes one light-day from Earth \u2014 Tue 18 Nov",
]
DATECHECK_NEXT = "Not yet: Bulgari funeral, Rome \u2014 Mon 23 Nov"

# map pins: (story number, lon, lat, dx, dy) — dx/dy are small display
# offsets that keep clustered pins (Levant, Beijing/Seoul) legible
PINS = [
    (1, 30.7, 36.9, 0, 0), (2, 20.1, 32.1, -14, 2), (4, 30.5, 50.5, 6, -8),
    (5, 32.5, 15.5, -4, 10), (6, 34.4, 32.8, -2, 14), (7, 36.1, 31.0, 16, 4),
    (8, 39.2, 22.8, 18, 14), (9, 50.3, 29.2, 16, -12),
    (10, -77.0, 38.9, 0, 0), (11, 114.2, 22.3, 0, 6), (12, 116.4, 39.9, -8, -7),
    (13, -3.0, 53.4, -8, -6), (14, 6.1, 46.2, 4, 4), (15, 127.0, 37.6, 7, 3),
]

LAND = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-76, 58), (-70, 62), (-65, 60), (-60, 52), (-65, 45),
     (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26), (-84, 30),
     (-89, 29), (-94, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 14),
     (-83, 9), (-79, 9), (-86, 13), (-92, 15), (-97, 16), (-105, 20),
     (-110, 23), (-114, 29), (-120, 34), (-124, 40), (-124, 47),
     (-130, 54), (-140, 60), (-155, 60), (-165, 60)],
    # South America
    [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -20), (-48, -26), (-52, -33), (-57, -38),
     (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -47),
     (-73, -40), (-72, -32), (-70, -20), (-75, -15), (-79, -8), (-81, -4),
     (-80, 1), (-77, 4)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (34, 28), (35, 24), (38, 21), (40, 15), (43, 12), (48, 11), (51, 12),
     (48, 5), (42, -2), (40, -10), (39, -18), (36, -22), (33, -27),
     (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
     (13, -5), (9, -1), (9, 4), (-2, 5), (-8, 5), (-13, 8), (-17, 12),
     (-17, 15), (-16, 20), (-15, 25), (-13, 28), (-9, 31)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (-2, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64),
     (14, 67), (20, 70), (30, 70), (40, 68), (45, 66), (40, 60), (35, 55),
     (32, 50), (30, 46), (28, 41), (26, 41), (23, 40), (26, 38), (22, 37),
     (19, 40), (15, 40), (16, 38), (12, 42), (10, 44), (7, 44), (3, 43),
     (0, 39), (-2, 37)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-2, 58), (-4, 58), (-6, 56),
     (-8, 54), (-6, 52), (-5, 51)],
    # Asia (incl. Arabia, India, SE Asia)
    [(26, 41), (30, 46), (36, 50), (30, 55), (35, 60), (45, 66), (60, 69),
     (75, 72), (90, 75), (105, 77), (120, 73), (135, 72), (150, 70),
     (162, 69), (178, 66), (178, 64), (162, 60), (158, 52), (150, 45),
     (142, 42), (140, 38), (135, 35), (129, 33), (126, 38), (122, 38),
     (120, 34), (122, 30), (118, 25), (110, 20), (108, 15), (106, 9),
     (103, 6), (100, 8), (98, 14), (94, 17), (92, 16), (89, 22), (86, 20),
     (80, 15), (77, 8), (72, 20), (66, 25), (61, 25), (57, 27), (52, 29),
     (50, 29), (48, 30), (50, 26), (55, 26), (58, 23), (59, 22), (55, 17),
     (52, 15), (45, 12), (43, 12), (42, 15), (39, 21), (35, 28), (34, 31),
     (36, 36), (30, 36), (27, 37)],
    # Indonesia / New Guinea
    [(95, 5), (105, 6), (112, 2), (118, -2), (125, -3), (131, -3),
     (138, -4), (145, -5), (150, -9), (140, -8), (130, -7), (120, -9),
     (112, -7), (105, -6), (98, -2)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (140, 45), (138, 39), (135, 34), (132, 33)],
    # Australia
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -30), (153, -25), (151, -20), (146, -19), (142, -15), (142, -11),
     (137, -12), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (174, -39), (176, -38), (174, -41),
     (171, -44), (168, -46)],
]

TOTAL = len(HEROES) + len(GRID) + len(BRIEFS_A) + len(BRIEFS_B)


# ---------------------------------------------------------------- text helpers

def tw(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, maxw, leading, fill=INK, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def status_line(d, x, y, status):
    word, src = status
    f = F(SANS_B, 9)
    col = GREEN if word == "CONFIRMED" else RUST
    d.text((x, y), word, font=f, fill=col)
    d.text((x + tw(d, word, f) + 4, y), src, font=f, fill=GREY)


def chip(d, cx, cy, n, r=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = F(SANS_B, 12 if n < 10 else 10)
    s = str(n)
    d.text((cx - tw(d, s, f) / 2, cy - (7 if n < 10 else 6)), s,
           font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- art

def art_globe(d, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2, h // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=1)
    d.line([cx - r + 4, cy - r // 2, cx + r - 4, cy - r // 2], fill=BLUE, width=1)
    d.line([cx - r + 4, cy + r // 2, cx + r - 4, cy + r // 2], fill=BLUE, width=1)
    crack = [(cx - 6, cy - r + 3), (cx + 2, cy - 8), (cx - 5, cy + 2),
             (cx + 4, cy + 12), (cx - 2, cy + r - 4)]
    d.line(crack, fill=RED, width=2)


def art_ship(d, x, y, w, h):
    base = y + h - 8
    for i in range(3):
        pts = [(x + 8 + j * 14, base + (4 if j % 2 else 0))
               for j in range(int(w / 14))]
        d.line(pts, fill=BLUE, width=1)
    hull = [(x + 30, base - 14), (x + w - 40, base - 14),
            (x + w - 56, base - 4), (x + 44, base - 4)]
    d.polygon(hull, fill=INK)
    d.rectangle([x + 70, base - 26, x + 118, base - 14], fill=INK)
    d.rectangle([x + 128, base - 34, x + 142, base - 14], fill=INK)
    d.line([x + 160, base - 14, x + 160, base - 30], fill=INK, width=2)
    dx, dy = x + w - 52, y + 8
    d.rectangle([dx - 7, dy - 3, dx + 7, dy + 3], fill=RED)
    for ox, oy in ((-12, -6), (12, -6), (-12, 6), (12, 6)):
        d.ellipse([dx + ox - 4, dy + oy - 2, dx + ox + 4, dy + oy + 2],
                  outline=RED, width=1)


def art_mercury(d, x, y, w, h):
    cx, cy, r = x + w // 2 - 20, y + h // 2, h // 2 - 3
    d.ellipse([cx - 70, cy - 14, cx + 70, cy + 14], outline=GREY, width=1)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SAND, outline=INK, width=1)
    for ox, oy, rr in ((-10, -6, 5), (8, 4, 7), (-2, 12, 4), (14, -10, 3)):
        d.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr],
                  outline=GREY, width=1)
    px, py = cx + 58, cy - 16
    d.rectangle([px - 5, py - 5, px + 5, py + 5], fill=BLUE)
    d.rectangle([px - 16, py - 3, px - 6, py + 3], fill=BLUE)
    d.rectangle([px + 6, py - 3, px + 16, py + 3], fill=BLUE)


ART = {"globe": art_globe, "ship": art_ship, "mercury": art_mercury}


# ---------------------------------------------------------------- sections

def masthead(d):
    f = F(SANS_B, 13)
    d.text((22, 8), "THE WORLD'S NEWS OF ONE DAY", font=f, fill=INK)
    right = f"{TOTAL} STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THIS SUNDAY"
    d.text((1002 - tw(d, right, f), 8), right, font=f, fill=INK)
    d.rectangle([22, 28, 1002, 30], fill=INK)
    d.line([22, 33, 1002, 33], fill=INK, width=1)
    title = "Sunday 22 November 2026"
    ft = F(SERIF_B, 58)
    d.text(((1024 - tw(d, title, ft)) / 2, 38), title, font=ft, fill=INK)
    d.line([22, 102, 1002, 102], fill=INK, width=1)


def timeline(d):
    lab = "THE DAY IN UTC"
    fl = F(SANS_B, 9)
    d.text((1002 - tw(d, lab, fl), 108), lab, font=fl, fill=GREY)
    axis_y = 138
    x0, x1 = 30, 994
    d.line([x0, axis_y, x1, axis_y], fill=INK, width=1)
    for hr in range(0, 25, 3):
        x = x0 + (x1 - x0) * hr / 24
        d.line([x, axis_y - 3, x, axis_y + 3], fill=INK, width=1)
    fs = F(SANS, 8)
    d.text((x0, axis_y + 4), "00:00", font=fs, fill=GREY)
    s = "24:00"
    d.text((x1 - tw(d, s, fs), axis_y + 4), s, font=fs, fill=GREY)
    f = F(SANS, 8.5)
    fb = F(SANS_B, 8.5)
    for hour, label, above in TIMELINE:
        x = x0 + (x1 - x0) * hour / 24
        d.line([x, axis_y - 5, x, axis_y + 5], fill=RED, width=2)
        time, rest = label.split(" ", 1)
        lines = wrap(d, rest, f, 170)
        if above:
            ly = axis_y - 10 - (len(lines) + 1) * 10
            d.text((x + 4, ly), time, font=fb, fill=RED)
            for ln in lines:
                ly += 10
                d.text((x + 4, ly), ln, font=f, fill=INK)
        else:
            ly = axis_y + 6
            d.text((x + 4, ly), time, font=fb, fill=RED)
            for ln in lines:
                ly += 10
                d.text((x + 4, ly), ln, font=f, fill=INK)


def heroes(d):
    y0, hh = 178, 150
    pw, gap = 320, 10
    for i, hro in enumerate(HEROES):
        x = 22 + i * (pw + gap)
        d.rectangle([x, y0, x + pw, y0 + hh], outline=INK, width=1)
        ART[hro["art"]](d, x + 56, y0 + 5, pw - 112, 36)
        chip(d, x + 14, y0 + 14, hro["n"])
        d.text((x + 30, y0 + 7), hro["tag"], font=F(SANS_B, 10), fill=RED)
        y = block(d, x + 10, y0 + 46, hro["headline"], F(SERIF_B, 19),
                  pw - 20, 22, max_lines=2)
        block(d, x + 10, max(y + 2, y0 + 92), hro["deck"], F(SANS, 11.5),
              pw - 20, 14, max_lines=3)
        status_line(d, x + 10, y0 + hh - 14, hro["status"])


def grid(d):
    y0, rh, gap = 336, 84, 8
    cw = (980 - 5 * gap) // 6
    for i, g in enumerate(GRID):
        col, row = i % 6, i // 6
        x = 22 + col * (cw + gap)
        y = y0 + row * (rh + gap)
        d.line([x, y, x + cw, y], fill=INK, width=2)
        chip(d, x + 8, y + 12, g["n"], r=8)
        d.text((x + 20, y + 6), g["tag"], font=F(SANS_B, 7.5), fill=RED)
        yy = block(d, x, y + 18, g["headline"], F(SERIF_B, 12), cw, 14,
                   max_lines=2)
        block(d, x, yy + 1, g["deck"], F(SANS, 9), cw, 11.5, max_lines=2)
        status_line(d, x, y + rh - 11, g["status"])


def world_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=LIGHT, outline=INK, width=1)

    def proj(lon, lat):
        return (x0 + (lon + 170) / 360 * w, y0 + (75 - lat) / 135 * h)

    for poly in LAND:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=SAND)
    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED)
        f = F(SANS_B, 9 if n < 10 else 7.5)
        s = str(n)
        d.text((px - tw(d, s, f) / 2, py - 5), s, font=f,
               fill=(255, 255, 255))
    d.text((x0 + 6, y0 + h - 13), "3 \u00b7 MERCURY \u2014 off this map",
           font=F(SANS_B, 8.5), fill=INK)


def briefs(d, x, y, items, head, count):
    f = F(SANS_B, 11)
    d.text((x, y), head, font=f, fill=INK)
    s = str(count)
    d.text((x + 306 - tw(d, s, f), y), s, font=f, fill=INK)
    d.line([x, y + 16, x + 306, y + 16], fill=INK, width=1)
    fb, fr = F(SANS_B, 10), F(SANS, 10)
    yy = y + 22
    for region, text in items:
        d.text((x, yy), region, font=fb, fill=INK)
        rx = x + tw(d, region, fb) + 5
        lines = wrap(d, text, fr, x + 306 - rx)
        for j, ln in enumerate(lines):
            d.text((rx if j == 0 else x, yy), ln, font=fr, fill=INK)
            yy += 12
        yy += 3
    return yy


def bottom(d):
    d.text((22, 520), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    world_map(d, 22, 540, 330, 184)
    bx, by, bw, bh = 22, 734, 330, 216
    d.rectangle([bx, by, bx + bw, by + bh], outline=RED, width=2)
    d.text((bx + 10, by + 8), "DATE CHECK \u2014 LEFT OUT AS OLDER NEWS",
           font=F(SANS_B, 11.5), fill=RED)
    yy = by + 30
    for ln in DATECHECK:
        yy = block(d, bx + 10, yy, ln, F(SANS, 10), bw - 20, 13.5) + 2.5
    d.text((bx + 10, yy + 3), DATECHECK_NEXT, font=F(SANS_O, 10), fill=GREY)
    briefs(d, 362, 520, BRIEFS_A,
           "AMERICAS \u00b7 AFRICA \u00b7 MIDDLE EAST \u00b7 OCEANIA", len(BRIEFS_A))
    briefs(d, 688, 520, BRIEFS_B,
           "EUROPE \u00b7 ASIA \u00b7 SCIENCE \u00b7 CULTURE", len(BRIEFS_B))


def footer(d):
    d.line([22, 958, 1002, 958], fill=INK, width=1)
    txt = ("Every story here happened, or was first reported, on Sunday "
           "22 November 2026; claims are attributed. Sources: Reuters, "
           "AFP, AP, BBC, Al Jazeera, France 24, Le Monde, Middle East "
           "Eye, The Hindu, SCMP, ESA, Fox News, CBC, RNZ.")
    block(d, 22, 966, txt, F(SANS, 10), 980, 13)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    timeline(d)
    heroes(d)
    grid(d)
    bottom(d)
    footer(d)
    img.save(os.path.join(HERE, "entry.png"))


if __name__ == "__main__":
    main()
