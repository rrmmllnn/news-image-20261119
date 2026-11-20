#!/usr/bin/env python3
"""Draw the news-image-20261119 front page (1024x1024) with Pillow.

Layout: navy masthead naming Thursday 19 November 2026, a lead panel on
the Trump-Xi-Putin Shenzhen summit, two rows of two story panels (ICJ
Myanmar ruling, Kerch Bridge, Gaza/Riyadh, Anthropic IPO), and a footer
strip with four more stories. All art is flat vector-style shapes drawn
here; all text is rendered by Pillow so it stays legible.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (20, 38, 74)
GOLD = (201, 162, 39)
PAPER = (250, 248, 242)
INK = (24, 24, 24)
GREY = (90, 90, 90)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width in pixels, word by word."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def panel(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=(255, 255, 255), outline=(200, 200, 200), width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)


def headline_block(draw, x, y, w, title, caption, title_size=30, cap_size=19):
    tf, cf = font(FB, title_size), font(FR, cap_size)
    ty = y
    for line in wrap(draw, title, tf, w):
        draw.text((x, ty), line, font=tf, fill=INK)
        ty += title_size + 6
    ty += 2
    for line in wrap(draw, caption, cf, w):
        draw.text((x, ty), line, font=cf, fill=(60, 60, 60))
        ty += cap_size + 5
    return ty


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 118], fill=GOLD)
    d.text((512, 18), "THE WORLD IN ONE DAY", font=font(FB, 52),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 80), "THURSDAY 19 NOVEMBER 2026  •  THE DAY IN SIX STORIES",
           font=font(FB, 20), fill=(214, 226, 240), anchor="ma")

    # --- lead panel: Shenzhen summit ---
    px, py, pw, ph = 20, 130, 984, 268
    panel(d, px, py, pw, ph, GOLD)
    # sky + skyline
    d.rectangle([px + 2, py + 10, px + pw - 2, py + 135], fill=(190, 216, 235))
    d.polygon([(px + 60, py + 135), (px + 60, py + 80), (px + 110, py + 80),
               (px + 110, py + 135)], fill=(70, 90, 120))
    d.polygon([(px + 130, py + 135), (px + 130, py + 55), (px + 150, py + 40),
               (px + 170, py + 55), (px + 170, py + 135)], fill=(50, 70, 100))
    d.rectangle([px + 190, py + 95, px + 260, py + 135], fill=(70, 90, 120))
    d.rectangle([px + 280, py + 70, px + 330, py + 135], fill=(50, 70, 100))
    d.rectangle([px + 350, py + 105, px + 430, py + 135], fill=(70, 90, 120))
    # three flag roundels: US, China, Russia
    cx = px + pw - 330
    for i, (cols, label) in enumerate([
            ([(178, 34, 52), (255, 255, 255), (60, 59, 110)], "USA"),
            ([(222, 41, 16)], "CHINA"),
            ([(255, 255, 255), (0, 57, 166), (213, 0, 50)], "RUSSIA")]):
        x0 = cx + i * 105
        d.ellipse([x0, py + 30, x0 + 88, py + 118], outline=NAVY, width=3, fill=(255, 255, 255))
        if label == "USA":
            d.rectangle([x0 + 8, py + 47, x0 + 80, py + 101], fill=(178, 34, 52))
            for yy in (58, 74, 90):
                d.rectangle([x0 + 8, py + yy, x0 + 80, py + yy + 6], fill=(255, 255, 255))
            d.rectangle([x0 + 8, py + 47, x0 + 38, py + 73], fill=(60, 59, 110))
        elif label == "CHINA":
            d.rectangle([x0 + 8, py + 47, x0 + 80, py + 101], fill=(222, 41, 16))
            d.text((x0 + 44, py + 74), "★", font=font(FB, 34), fill=(255, 222, 0), anchor="mm")
        else:
            for j, c in enumerate(cols):
                d.rectangle([x0 + 8, py + 47 + j * 18, x0 + 80, py + 65 + j * 18], fill=c)
        d.text((x0 + 44, py + 127), label, font=font(FB, 15), fill=INK, anchor="ma")
    d.text((px + 24, py + 152), "SHENZHEN  •  APEC SUMMIT", font=font(FB, 16), fill=GREY)
    headline_block(d, px + 24, py + 176, pw - 48,
                   "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                   "First three-way summit issues a peace declaration on nuclear risks.",
                   title_size=30, cap_size=19)

    # --- row 2 ---
    # ICJ panel
    x, y, w, h = 20, 412, 484, 252
    panel(d, x, y, w, h, (0, 90, 120))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 118], fill=(214, 232, 238))
    # courthouse: pediment + columns
    d.polygon([(x + 150, y + 58), (x + 330, y + 58), (x + 240, y + 30)], fill=(0, 90, 120))
    for cx0 in (165, 215, 265, 315):
        d.rectangle([cx0, y + 62, cx0 + 14, y + 112], fill=(240, 240, 240))
    d.rectangle([x + 150, y + 112, x + 330, y + 118], fill=(0, 90, 120))
    d.text((x + 24, y + 126), "THE HAGUE", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 144, w - 48,
                   "UN COURT: MYANMAR COMMITTED GENOCIDE",
                   "ICJ rules against Myanmar over the Rohingya crackdown; orders inquiry and compensation.",
                   title_size=26, cap_size=18)

    # Kerch Bridge panel
    x = 520
    panel(d, x, y, w, h, (150, 60, 40))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 118], fill=(200, 220, 235))
    # sea + broken bridge
    d.rectangle([x + 2, y + 88, x + w - 2, y + 118], fill=(60, 110, 160))
    d.rectangle([x + 20, y + 48, x + 200, y + 62], fill=(90, 90, 90))
    d.polygon([(x + 200, y + 48), (x + 215, y + 78), (x + 200, y + 92)], fill=(90, 90, 90))
    d.rectangle([x + 265, y + 48, x + 460, y + 62], fill=(90, 90, 90))
    d.polygon([(x + 265, y + 48), (x + 250, y + 78), (x + 265, y + 92)], fill=(90, 90, 90))
    for bx in (60, 150, 300, 400):
        d.rectangle([x + bx, y + 62, x + bx + 10, y + 92], fill=(70, 70, 70))
    d.text((x + 24, y + 126), "CRIMEA  •  BLACK SEA", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 144, w - 48,
                   "KERCH BRIDGE HIT A THIRD TIME",
                   "Ukraine strikes the rail section; trains halted. Russian strikes kill at least five.",
                   title_size=26, cap_size=18)

    # --- row 3 ---
    y = 678
    # Gaza / Riyadh panel
    x, w, h = 20, 484, 252
    panel(d, x, y, w, h, (120, 40, 40))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 118], fill=(238, 214, 200))
    # tower with smoke
    d.rectangle([x + 90, y + 45, x + 150, y + 118], fill=(90, 70, 60))
    d.polygon([(x + 150, y + 45), (x + 190, y + 70), (x + 150, y + 95)], fill=(120, 120, 120))
    d.ellipse([x + 170, y + 25, x + 260, y + 70], fill=(160, 160, 160))
    d.rectangle([x + 300, y + 70, x + 380, y + 118], fill=(110, 90, 80))
    d.text((x + 24, y + 126), "MIDDLE EAST", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 144, w - 48,
                   "GAZA PUSH AND A STRIKE ON RIYADH",
                   "Israeli tanks move into central Gaza; a Houthi missile damages a tower in Riyadh.",
                   title_size=26, cap_size=18)

    # Anthropic IPO panel
    x = 520
    panel(d, x, y, w, h, (30, 120, 80))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 118], fill=(210, 238, 220))
    # rising chart
    pts = [(x + 40, y + 100), (x + 120, y + 88), (x + 200, y + 92),
           (x + 280, y + 60), (x + 360, y + 42), (x + 440, y + 24)]
    d.line(pts, fill=(20, 110, 70), width=6, joint="curve")
    d.polygon([(x + 440, y + 24), (x + 415, y + 24), (x + 440, y + 48)], fill=(20, 110, 70))
    for px0, py0 in pts:
        d.ellipse([px0 - 5, py0 - 5, px0 + 5, py0 + 5], fill=(20, 110, 70))
    d.text((x + 24, y + 126), "TECH  •  AI", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 144, w - 48,
                   "ANTHROPIC IPO SETS A RECORD",
                   "The Claude maker raises about $81bn at $83 a share — the biggest AI listing yet.",
                   title_size=26, cap_size=18)

    # --- footer strip ---
    d.rectangle([0, 944, W, H], fill=NAVY)
    d.text((512, 954), "ALSO TODAY", font=font(FB, 15), fill=GOLD, anchor="ma")
    footer = ("CYCLONE AKVAN nears the India coast  •  BANGLADESH: Yunus home torched, 4 dead  •  "
              "N. KOREA expands uranium enrichment  •  DENMARK approves Greenland deal 109–0")
    for i, line in enumerate(wrap(d, footer, font(FR, 16), W - 48)):
        d.text((512, 976 + i * 20), line, font=font(FR, 16),
               fill=(220, 228, 240), anchor="ma")

    img.save("/home/hatch/workspace/makefun/news-image-20261119/entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
