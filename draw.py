#!/usr/bin/env python3
"""Draw the news-image-20261122 front page.

Deterministic PIL generator (build time only). Writes entry.png next to
this file. No randomness, no timestamps, no PNG metadata, so repeated
runs produce byte-identical output.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (250, 247, 238)   # off-white newsprint
INK = (18, 18, 18)        # near-black ink
RED = (178, 34, 34)       # single red accent
BLUE = (38, 84, 124)      # flat illustration blue
GREEN = (46, 110, 62)     # flat illustration green
LIGHT = (226, 222, 210)   # panel tint
GREY = (90, 88, 82)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def text_block(d, text, fnt, max_width, max_lines, x, y, fill, leading):
    """Draw wrapped text; raise if it would overflow its budget."""
    lines = wrap(text, fnt, max_width)
    assert len(lines) <= max_lines, (
        "text overflow: %r wrapped to %d lines (max %d)"
        % (text, len(lines), max_lines)
    )
    return draw_lines(d, lines, x, y, fnt, fill, leading)


# ---------------------------------------------------------------- illustrations

def draw_globe(d, x0, y0, x1, y1):
    """Climate globe with a rising sun: hero illustration."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 10
    r = 82
    # sun with rays, top right
    sx, sy, sr = x1 - 42, y0 + 34, 22
    for i in range(8):
        ang = i * 3.14159 / 4
        x_a = sx + int((sr + 6) * math.cos(ang))
        y_a = sy + int((sr + 6) * math.sin(ang))
        x_b = sx + int((sr + 18) * math.cos(ang))
        y_b = sy + int((sr + 18) * math.sin(ang))
        d.line([(x_a, y_a), (x_b, y_b)], fill=RED, width=4)
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=RED)
    # globe
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - 34, cy - r, cx + 34, cy + r], outline=(250, 247, 238), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(250, 247, 238), width=2)
    d.line([(cx - r + 18, cy - 48), (cx + r - 18, cy - 48)],
           fill=(250, 247, 238), width=2)
    d.line([(cx - r + 18, cy + 48), (cx + r - 18, cy + 48)],
           fill=(250, 247, 238), width=2)
    # land blobs
    d.ellipse([cx - 58, cy - 52, cx - 8, cy - 8], fill=GREEN)
    d.ellipse([cx + 6, cy + 6, cx + 58, cy + 52], fill=GREEN)
    d.ellipse([cx + 30, cy - 62, cx + 66, cy - 22], fill=GREEN)


def draw_mast(d, x0, y0, x1, y1):
    """Phone mast with signal arcs and a red ban slash: telecom ban."""
    cx = (x0 + x1) // 2
    base = y1 - 18
    tip_y = y0 + 54
    d.line([(cx - 42, base), (cx, tip_y)], fill=INK, width=5)
    d.line([(cx + 42, base), (cx, tip_y)], fill=INK, width=5)
    d.line([(cx - 26, base - 30), (cx + 26, base - 30)], fill=INK, width=4)
    d.line([(cx - 14, base - 58), (cx + 14, base - 58)], fill=INK, width=4)
    d.ellipse([cx - 7, tip_y - 8, cx + 7, tip_y + 6], fill=RED)
    for rr in (20, 34, 48):
        d.arc([cx - rr, tip_y - rr, cx + rr, tip_y + rr],
              200, 340, fill=BLUE, width=4)
    # red ban circle + slash over the signal
    bx, by, br = cx + 36, y0 + 72, 32
    d.ellipse([bx - br, by - br, bx + br, by + br], outline=RED, width=6)
    d.line([(bx - 22, by + 22), (bx + 22, by - 22)], fill=RED, width=6)


def draw_ballot(d, x0, y0, x1, y1):
    """Ballot box with a paper going in and a red check: Hong Kong vote."""
    cx = (x0 + x1) // 2
    top = y0 + 58
    # paper slip above the slot
    d.polygon([(cx - 26, y0 + 6), (cx + 26, y0 + 6),
               (cx + 26, top - 4), (cx - 26, top - 4)], fill=(255, 255, 255),
              outline=INK)
    d.line([(cx - 18, y0 + 18), (cx + 18, y0 + 18)], fill=INK, width=2)
    d.line([(cx - 18, y0 + 28), (cx + 18, y0 + 28)], fill=INK, width=2)
    # box
    d.rectangle([x0 + 8, top, x1 - 8, y1 - 14], fill=BLUE, outline=INK, width=3)
    d.rectangle([cx - 34, top - 2, cx + 34, top + 8], fill=INK)
    d.text((cx - 52, top + 34), "VOTE", font=font(SANS_BOLD, 26), fill=PAPER)
    # red check mark
    d.line([(x1 - 52, y1 - 62), (x1 - 34, y1 - 40), (x1 - 2, y1 - 84)],
           fill=RED, width=8)


def draw_treaty(d, x0, y0, x1, y1):
    """Document with a radiation trefoil seal: nuclear deal."""
    cx = (x0 + x1) // 2
    # radiation trefoil, fully inside the panel (was clipped by the top edge)
    tx, ty, tr = cx, y0 + 30, 20
    d.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=INK)
    for start in (270, 30, 150):
        d.pieslice([tx - tr, ty - tr, tx + tr, ty + tr], start, start + 55,
                   fill=INK)
    # document
    d.rectangle([x0 + 14, y0 + 56, x1 - 14, y1 - 12], fill=(255, 255, 255),
                outline=INK, width=3)
    d.polygon([(x1 - 14, y0 + 56), (x1 - 40, y0 + 56), (x1 - 14, y0 + 82)],
              fill=LIGHT, outline=INK)
    for i, yy in enumerate((y0 + 104, y0 + 120, y0 + 136)):
        d.line([(x0 + 28, yy), (x1 - 28, yy)], fill=INK, width=3)
    # red seal
    d.ellipse([x1 - 52, y1 - 52, x1 - 16, y1 - 16], fill=RED, outline=INK, width=2)


def draw_football(d, x0, y0, x1, y1):
    """Goal posts and a football: Sunday sport."""
    # goal
    d.line([(x0 + 16, y0 + 26), (x0 + 16, y1 - 60)], fill=INK, width=6)
    d.line([(x1 - 16, y0 + 26), (x1 - 16, y1 - 60)], fill=INK, width=6)
    d.line([(x0 + 16, y0 + 26), (x1 - 16, y0 + 26)], fill=INK, width=6)
    # ball
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2 + 18, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=INK, width=3)
    d.polygon([(cx, cy - 16), (cx + 15, cy - 5), (cx + 9, cy + 13),
               (cx - 9, cy + 13), (cx - 15, cy - 5)], fill=INK)
    for (ax, ay, bx, by) in ((cx, cy - 16, cx, cy - r),
                             (cx + 15, cy - 5, cx + r - 6, cy - 18),
                             (cx + 9, cy + 13, cx + 26, cy + r - 8),
                             (cx - 9, cy + 13, cx - 26, cy + r - 8),
                             (cx - 15, cy - 5, cx - r + 6, cy - 18)):
        d.line([(ax, ay), (bx, by)], fill=INK, width=3)
    d.line([(x0 + 8, y1 - 14), (x1 - 8, y1 - 14)], fill=GREEN, width=6)


# ---------------------------------------------------------------- layout

def panel(d, x0, y0, x1, y1, kicker, headline, deck, art):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    tx = x0 + 14
    tw = 288
    y = y0 + 12
    d.text((tx, y), kicker, font=font(SANS_BOLD, 14), fill=RED)
    y += 22
    y = text_block(d, headline, font(SANS_BOLD, 20), tw, 2,
                   tx, y, INK, 26)
    y += 6
    text_block(d, deck, font(SANS, 16), tw, 4, tx, y, INK, 21)
    art(d, x0 + 312, y0 + 12, x1 - 12, y1 - 12)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    X1 = W - M

    # ---- masthead
    d.text((M, 22), "THE WORLD TODAY", font=font(SERIF_BOLD, 62), fill=INK)
    d.text((M, 96), "SUNDAY 22 NOVEMBER 2026",
           font=font(SANS_BOLD, 34), fill=RED)
    d.text((M, 136), "World news in one page  |  Verified from wire reports",
           font=font(SANS, 15), fill=GREY)
    d.rectangle([M, 158, X1, 162], fill=RED)

    # ---- hero: COP31
    hx0, hy0, hx1, hy1 = M, 172, X1, 444
    d.rectangle([hx0, hy0, hx1, hy1], outline=INK, width=2)
    tx = hx0 + 16
    y = hy0 + 14
    d.text((tx, y), "CLIMATE  —  ANTALYA, TURKEY",
           font=font(SANS_BOLD, 16), fill=RED)
    y += 26
    y = text_block(d, "COP31 NEARS A DEAL AFTER SECOND DAY OF OVERTIME",
                   font(SANS_BOLD, 36), 590, 3, tx, y, INK, 44)
    y += 8
    text_block(
        d,
        "A new draft deal was put to nearly 200 nations early on Sunday, "
        "with a vote to approve it at 06:00 GMT. Fossil fuels and finance "
        "are the sticking points.",
        font(SANS, 19), 590, 3, tx, y, INK, 25)
    draw_globe(d, hx0 + 640, hy0 + 16, hx1 - 16, hy1 - 16)

    # ---- row 2
    panel(d, M, 458, M + 466, 654, "TECH  —  WASHINGTON",
          "CHINA HITS BACK AT US TELECOM BAN",
          "Beijing said on Sunday it firmly opposes a US vote barring "
          "Chinese telecom firms from direct access to US phone numbers.",
          draw_mast)
    panel(d, M + 486, 458, X1, 654, "ASIA  —  HONG KONG",
          "HONG KONG VOTES FOR ELECTION COMMITTEE",
          "Polls opened at 9am on Sunday, with 856 candidates contesting "
          "723 seats on the body that picks the city's leader.",
          draw_ballot)

    # ---- row 3
    panel(d, M, 668, M + 466, 864, "DIPLOMACY  —  WASHINGTON",
          "TRUMP SEEKS 'PERMANENT' IRAN DEAL",
          "Trump told Fox News on Saturday he wants a lasting deal to stop "
          "Iran ever getting a nuclear weapon. Talks are stalled.",
          draw_treaty)
    panel(d, M + 486, 668, X1, 864, "SPORT  —  LONDON",
          "LIVERPOOL v MAN UTD TODAY",
          "Liverpool host Manchester United at 16:30 GMT in Mauricio "
          "Pochettino's first game as United manager.",
          draw_football)

    # ---- ALSO TODAY strip (2 x 2)
    sx0, sy0 = M, 878
    d.text((sx0, sy0), "ALSO TODAY", font=font(SANS_BOLD, 16), fill=RED)
    d.rectangle([sx0, sy0 + 24, X1, sy0 + 26], fill=INK)
    items = [
        ("ADDIS ABABA — ", "Next year's climate summit is set for "
         "Ethiopia's capital in November 2027."),
        ("ROME — ", "Funeral of jeweller Paolo Bulgari, 89, to be held "
         "on Monday."),
        ("BAYELSA — ", "24 dead after a boat carrying mourners capsized "
         "on Friday."),
        ("SINALOA — ", "FBI most-wanted 'El Chapo Isidro' captured on "
         "Friday night; 11 died in the fighting."),
    ]
    col_w = 466
    y = sy0 + 34
    for row in range(2):
        max_h = 0
        for col in range(2):
            label, text = items[row * 2 + col]
            x = sx0 + col * (col_w + 20)
            d.text((x, y), label, font=font(SANS_BOLD, 16), fill=RED)
            lx = x + font(SANS_BOLD, 16).getlength(label)
            lines = wrap(text, font(SANS, 16), col_w - (lx - x))
            assert len(lines) <= 2, "strip overflow: %r" % text
            yy = draw_lines(d, lines, lx, y, font(SANS, 16), INK, 19)
            max_h = max(max_h, yy - y)
        y += max_h + 6

    # ---- footer
    d.text((M, 1002),
           "Compiled early on Sunday 22 November 2026 from wire reports. "
           "Later events are not covered.",
           font=font(SANS, 14), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    return out


if __name__ == "__main__":
    print(build())
