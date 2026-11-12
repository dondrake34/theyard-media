"""Ep08 scenes: Cheyney University (Richard Humphreys, Institute for Colored Youth, Fanny Jackson Coppin). One function per paragraph."""
from lib import *

NAVY = (0.16, 0.20, 0.34)
CHAR = (0.25, 0.25, 0.28)
GRAY = (0.80, 0.80, 0.80)
SKIN_LT = (0.93, 0.80, 0.68)
RED = (0.78, 0.14, 0.14)
PAPER = (0.98, 0.95, 0.86)
WOOD = (0.62, 0.48, 0.32)
WOOD_DK = (0.42, 0.31, 0.20)
FISK_BLUE = (0.18, 0.30, 0.58)
DRESSES = [(0.30, 0.20, 0.36), (0.20, 0.24, 0.38), (0.36, 0.16, 0.20), (0.22, 0.30, 0.26), (0.28, 0.22, 0.16)]
COATS = [CHAR, NAVY, (0.30, 0.22, 0.16), (0.18, 0.18, 0.22)]

MAN_POSES = {  # (elbow, hand) per side (viewer-left, viewer-right), relative to feet
    "rest":  (((-62, -250), (-58, -175)), ((62, -250), (58, -175))),
    "hold":  (((-62, -250), (-58, -175)), ((95, -265), (140, -330))),
    "open":  (((-95, -270), (-150, -320)), ((95, -270), (150, -320))),
    "sing":  (((-70, -250), (-30, -235)), ((70, -250), (30, -235))),   # hands clasped at chest
    "point": (((-62, -250), (-58, -175)), ((110, -300), (175, -360))),
}


def eyes(cr, hy, t, skin, off=0.9):
    ph = (t + off) % 3.7
    op = 0.25 if ph < 0.13 else 1.0
    for dx in (-16, 16):
        cr.save(); cr.translate(dx, hy - 4); cr.scale(1, op); cr.arc(0, 0, 8.5, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(1, 1, 1); cr.fill()
        if skin != BLACK:
            cr.save(); cr.translate(dx, hy - 4); cr.scale(1, op); cr.arc(0, 0, 8.5, 0, 2 * math.pi); cr.restore()
            cr.set_source_rgb(*INK); cr.set_line_width(2); cr.stroke()
        if op > 0.5:
            cr.arc(dx + 1, hy - 3, 3.8, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()


def arms(cr, pose, pose_to, pose_t, bob, col, skin, sh_y=-318, sh_x=50):
    pa = MAN_POSES[pose]; pb = MAN_POSES[pose_to] if pose_to else pa
    k = ease(clamp(pose_t)) if pose_to else 0.0
    hands = []
    for side, sx in ((0, -sh_x), (1, sh_x)):
        (ea, ha), (eb, hb) = pa[side], pb[side]
        e = (ea[0] + (eb[0] - ea[0]) * k, ea[1] + (eb[1] - ea[1]) * k + bob)
        h = (ha[0] + (hb[0] - ha[0]) * k, ha[1] + (hb[1] - ha[1]) * k + bob)
        for w, c in ((32, INK), (24, col)):
            cr.move_to(sx, sh_y + bob); cr.line_to(*e); cr.line_to(*h)
            cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_line_width(w); cr.set_source_rgb(*c); cr.stroke()
        cr.arc(h[0], h[1], 13, 0, 2 * math.pi); cr.set_source_rgb(*skin); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        hands.append(h)
    return hands


def man(cr, x, y, s=1.0, t=0.0, suit=NAVY, tie=MAROON, skin=BLACK, hair=None, pose="rest", pose_to=None,
        pose_t=0.0, walking=False, beard=None, whiskers=False, prop=None):
    """Stylized man (no mouth, no lips). beard = colour for a full beard (Grant)."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.save(); cr.scale(1, 0.12); cr.arc(0, 30, 110, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgba(0, 0, 0, 0.12); cr.fill()
    sw = math.sin(t * 8) * 14 if walking else 0
    bob = -abs(math.sin(t * 8)) * 5 if walking else math.sin(t * 2.0) * 2
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx, d in ((-22, -sw), (22, sw)):
        cr.move_to(dx, -170 + bob); cr.line_to(dx + d, -8)
        cr.set_source_rgb(*INK); cr.set_line_width(34); cr.stroke()
        cr.move_to(dx, -170 + bob); cr.line_to(dx + d, -8)
        cr.set_source_rgb(*suit); cr.set_line_width(26); cr.stroke()
        cr.save(); cr.translate(dx + d + 8, 0); cr.scale(1, 0.5); cr.arc(0, 0, 22, math.pi, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*BLACK); cr.fill()
    cr.move_to(-58, -330 + bob); cr.line_to(58, -330 + bob); cr.line_to(52, -160 + bob); cr.line_to(-52, -160 + bob)
    cr.close_path(); cr.set_source_rgb(*suit); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-24, -330 + bob); cr.line_to(0, -270 + bob); cr.line_to(24, -330 + bob); cr.close_path()
    cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.move_to(-8, -322 + bob); cr.line_to(8, -322 + bob); cr.line_to(11, -280 + bob); cr.line_to(0, -268 + bob)
    cr.line_to(-11, -280 + bob); cr.close_path(); cr.set_source_rgb(*tie); cr.fill()
    hands = arms(cr, pose, pose_to, pose_t, bob, suit, skin)
    if prop == "ledger":
        hx, hy = hands[1]
        cr.save(); cr.translate(hx - 6, hy - 10); cr.rotate(-0.2)
        cr.rectangle(-40, -50, 80, 100); cr.set_source_rgb(*FISK_BLUE); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.rectangle(-28, -36, 56, 14); cr.set_source_rgb(*GOLDC); cr.fill(); cr.restore()
    hy = -385 + bob
    cr.rectangle(-14, -345 + bob, 28, 22); cr.set_source_rgb(*skin); cr.fill()
    cr.arc(0, hy, 48, 0, 2 * math.pi); cr.set_source_rgb(*skin); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4 if skin != BLACK else 0.01); cr.stroke()
    if hair:
        cr.arc(0, hy, 48, math.pi * 1.05, math.pi * 1.95); cr.set_source_rgb(*hair); cr.set_line_width(14); cr.stroke()
    if whiskers:
        for dx in (-40, 40):
            cr.save(); cr.translate(dx, hy + 18); cr.scale(0.55, 1); cr.arc(0, 0, 24, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*(hair or GRAY)); cr.fill()
    if beard:  # full beard covering the jaw; no mouth
        cr.move_to(-48, hy - 2); cr.curve_to(-46, hy + 70, 46, hy + 70, 48, hy - 2)
        cr.curve_to(30, hy + 22, -30, hy + 22, -48, hy - 2); cr.close_path()
        cr.set_source_rgb(*beard); cr.fill()
    eyes(cr, hy, t, skin)
    cr.restore()


def woman(cr, x, y, s=1.0, t=0.0, dress=DRESSES[0], skin=BLACK, pose="rest", pose_to=None, pose_t=0.0,
          walking=False, hair=BLACK, crown=False, veil=False):
    """Stylized woman in a long 1870s dress (no mouth, no lips). crown/veil for Queen Victoria."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.save(); cr.scale(1, 0.12); cr.arc(0, 30, 140, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgba(0, 0, 0, 0.12); cr.fill()
    bob = -abs(math.sin(t * 8)) * 5 if walking else math.sin(t * 2.0) * 2.5
    sway = math.sin(t * 8) * 6 if walking else 0
    cr.move_to(-105 + sway, 0); cr.curve_to(-88, -150, -62, -260, -52, -330 + bob)
    cr.line_to(52, -330 + bob); cr.curve_to(62, -260, 88, -150, 105 + sway, 0); cr.close_path()
    cr.set_source_rgb(*dress); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-62, -240 + bob); cr.line_to(62, -240 + bob)
    cr.set_source_rgba(0, 0, 0, 0.35); cr.set_line_width(10); cr.stroke()
    arms(cr, pose, pose_to, pose_t, bob, dress, skin, sh_y=-315, sh_x=52)
    cr.move_to(-30, -330 + bob); cr.line_to(0, -300 + bob); cr.line_to(30, -330 + bob); cr.close_path()
    cr.set_source_rgb(1, 1, 1); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    hy = -380 + bob
    if veil:
        cr.move_to(-60, hy - 40); cr.curve_to(-80, hy + 40, -70, hy + 90, -62, hy + 110)
        cr.line_to(62, hy + 110); cr.curve_to(70, hy + 90, 80, hy + 40, 60, hy - 40); cr.close_path()
        cr.set_source_rgb(0.96, 0.96, 0.96); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.arc(0, hy - 46, 26, 0, 2 * math.pi); cr.set_source_rgb(*hair); cr.fill()
    cr.arc(0, hy, 49, 0, 2 * math.pi); cr.set_source_rgb(*skin); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4 if skin != BLACK else 0.01); cr.stroke()
    if skin != BLACK:
        cr.arc(0, hy, 49, math.pi * 1.0, math.pi * 2.0); cr.set_source_rgb(*hair); cr.set_line_width(16); cr.stroke()
    if crown:
        cr.move_to(-26, hy - 44); cr.line_to(-26, hy - 74); cr.line_to(-13, hy - 58); cr.line_to(0, hy - 82)
        cr.line_to(13, hy - 58); cr.line_to(26, hy - 74); cr.line_to(26, hy - 44); cr.close_path()
        cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    eyes(cr, hy, t, skin, off=1.7)
    cr.restore()


BRICK = (0.66, 0.30, 0.24)
GRASS = (0.52, 0.68, 0.40)


def sceneout(cr, t, a, b):
    k = max(0, (t - (b - 0.5)) / 0.5)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    k0 = 1 - clamp((t - a) / 0.3)
    if k0 > 0:
        cr.set_source_rgba(*BG, k0 * 0.9); cr.paint()


def name_tag(cr, s1, s2, x, y, alpha, size=42):
    if alpha <= 0:
        return
    cr.save(); cr.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size); w1 = cr.text_extents(s1).x_advance
    cr.set_font_size(size * 0.7); w2 = cr.text_extents(s2).x_advance if s2 else 0
    w = max(w1, w2) + 50; h = size * 1.25 + (size * 0.95 if s2 else 0)
    cr.restore()
    panel(cr, x - w / 2, y, w, h, MAROON, r=16, lw=4, alpha=alpha)
    text(cr, s1, x, y + size * 1.02, size, GOLDC, alpha=alpha)
    if s2:
        text(cr, s2, x, y + size * 1.9, size * 0.7, (1, 1, 1), alpha=alpha)


def stamp(cr, s, x, y, p, col=RED, size=70, rot=-0.08):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.rotate(rot)
    k = 1.5 - 0.5 * ease(p); cr.scale(k, k)
    cr.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); cr.set_font_size(size)
    w = cr.text_extents(s).x_advance
    rounded_rect(cr, -w / 2 - 30, -size * 0.95, w + 60, size * 1.35, 14)
    cr.set_source_rgba(*col, p); cr.set_line_width(10); cr.stroke()
    text(cr, s, 0, 0, size, col, alpha=p)
    cr.restore()



# ---------------- ep08 props (Cheyney colours: blue and white; no logos or seals)
CU_BLUE = (0.10, 0.25, 0.55)
COAT_GRAY = (0.42, 0.42, 0.45)
HAIR_GRAY = (0.80, 0.80, 0.80)
PARCH = (0.97, 0.92, 0.78)
FANNY_DRESS = (0.22, 0.16, 0.32)
AUNT_DRESS = (0.36, 0.22, 0.16)
FARM_BROWN = (0.40, 0.28, 0.18)


def brim_hat(cr, x, hy, s, col=BLACK):
    """Broad-brimmed plain hat (Quaker style), centred on head at (x, hy)."""
    cr.save(); cr.translate(x, hy); cr.scale(s, s)
    cr.save(); cr.translate(0, -34); cr.scale(1, 0.22); cr.arc(0, 0, 92, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgb(*col); cr.fill()
    rounded_rect(cr, -46, -96, 92, 66, 12); cr.fill()
    cr.restore()


def humphreys(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0):
    """Richard Humphreys: stylized Quaker man, plain gray coat, broad hat (no mouth)."""
    man(cr, x, y, s, t, suit=COAT_GRAY, tie=(0.95, 0.95, 0.95), skin=SKIN_LT, hair=HAIR_GRAY,
        pose=pose, pose_to=pose_to, pose_t=pose_t, whiskers=False)
    bob = math.sin(t * 2.0) * 2
    brim_hat(cr, x, y + (-385 + bob) * s, s)


def cheyney_farmer(cr, x, y, s=1.0, t=0.0, pose="rest"):
    """George Cheyney: stylized farmer, brown coat, broad hat (no mouth)."""
    man(cr, x, y, s, t, suit=FARM_BROWN, tie=(0.85, 0.80, 0.70), skin=SKIN_LT, hair=(0.50, 0.40, 0.30), pose=pose)
    bob = math.sin(t * 2.0) * 2
    brim_hat(cr, x, y + (-385 + bob) * s, s, col=(0.30, 0.22, 0.14))


def fanny(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0, cap=False):
    woman(cr, x, y, s, t, dress=FANNY_DRESS, skin=BLACK, pose=pose, pose_to=pose_to, pose_t=pose_t)
    if cap:
        bob = math.sin(t * 2.0) * 2.5
        hy = y + (-380 + bob) * s
        cr.save(); cr.translate(x, hy); cr.scale(s, s)
        cr.move_to(-72, -56); cr.line_to(0, -84); cr.line_to(72, -56); cr.line_to(0, -30); cr.close_path()
        cr.set_source_rgb(*BLACK); cr.fill()
        cr.move_to(56, -54); cr.line_to(64, -12); cr.set_source_rgb(*GOLDC); cr.set_line_width(4); cr.stroke()
        cr.restore()


def will_doc(cr, x, y, s=1.0, p=1.0, amount_p=0.0, rot=-0.05):
    """Parchment will with '$10,000' line. p = appear, amount_p = highlight."""
    if p <= 0:
        return
    k = back_out(p)
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(s * k, s * k)
    panel(cr, -200, -260, 400, 520, PARCH, r=12, lw=6)
    for yy in (-260, 260):  # scroll rolls
        rounded_rect(cr, -220, yy - 18, 440, 36, 18)
        cr.set_source_rgb(0.85, 0.76, 0.56); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    text(cr, "LAST WILL", 0, -175, 52, TEXT, font="Georgia")
    cr.set_source_rgba(*INK, 0.35); cr.set_line_width(4)
    for k2 in range(5):
        yy = -110 + k2 * 40
        cr.move_to(-150, yy); cr.line_to(150 - (k2 % 2) * 60, yy)
    cr.stroke()
    if amount_p > 0:
        rounded_rect(cr, -165, 110, 330, 86, 14); cr.set_source_rgba(*GOLDC, 0.9 * amount_p); cr.fill()
    text(cr, "$10,000", 0, 175, 66, MAROON if amount_p > 0 else TEXT, font="Georgia")
    cr.restore()


def tenth_pie(cr, x, y, r, p):
    if p <= 0:
        return
    cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgba(0.80, 0.78, 0.74, p); cr.fill_preserve()
    cr.set_source_rgba(*INK, p); cr.set_line_width(5); cr.stroke()
    a0 = -math.pi / 2
    cr.move_to(x, y); cr.arc(x, y, r, a0, a0 + 2 * math.pi * 0.1 * ease(p)); cr.close_path()
    cr.set_source_rgba(*GOLDC, p); cr.fill_preserve(); cr.set_source_rgba(*INK, p); cr.stroke()


def row_houses(cr):
    bg(cr, (0.82, 0.88, 0.96), (0.96, 0.92, 0.84))
    for k in range(7):
        x = -40 + k * 290
        h = 420 + (k % 3) * 40
        cr.rectangle(x, 880 - h, 280, h); cr.set_source_rgb(*BRICK); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
        for r in range(3):
            for c in range(2):
                cr.rectangle(x + 50 + c * 120, 880 - h + 50 + r * 120, 64, 80)
                cr.set_source_rgb(0.95, 0.90, 0.72); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.70, 0.68, 0.64); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


def checklist(cr, x, y, items, times, t, p):
    if p <= 0:
        return
    panel(cr, x, y, 620, 120 + 110 * len(items), PARCH, r=18, alpha=p)
    text(cr, "THE WILL ASKED FOR:", x + 310, y + 75, 42, MAROON, alpha=p)
    for k, (s, ts) in enumerate(zip(items, times)):
        q = prog(t, ts, 0.35)
        if q > 0:
            text(cr, "✓", x + 70, y + 170 + k * 110, 64, (0.15, 0.50, 0.25), alpha=q, scale=back_out(q))
            text(cr, s, x + 130, y + 170 + k * 110, 58, TEXT, align="left", alpha=q)


def barn(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-180, -260, 360, 260); cr.set_source_rgb(0.68, 0.20, 0.16); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.move_to(-210, -255); cr.line_to(-120, -380); cr.line_to(120, -380); cr.line_to(210, -255); cr.close_path()
    cr.set_source_rgb(0.30, 0.22, 0.20); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-70, -170, 140, 170); cr.set_source_rgb(0.96, 0.94, 0.88); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-70, -170); cr.line_to(70, 0); cr.move_to(70, -170); cr.line_to(-70, 0); cr.stroke()
    cr.restore()


def farm_bg(cr):
    bg(cr, (0.78, 0.88, 0.98), (0.95, 0.94, 0.86))
    cr.move_to(0, 700); cr.curve_to(500, 600, 1100, 720, W, 640); cr.line_to(W, H); cr.line_to(0, H); cr.close_path()
    cr.set_source_rgb(0.62, 0.76, 0.46); cr.fill()
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(*GRASS); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for k in range(0, W, 120):  # fence
        cr.rectangle(k, 820, 16, 70); cr.set_source_rgb(*WOOD); cr.fill()
    cr.rectangle(0, 835, W, 10); cr.rectangle(0, 860, W, 10); cr.set_source_rgb(*WOOD); cr.fill()


CHALK = (0.16, 0.30, 0.24)


def chalkboard(cr, x, y, w, h, lines, p=1.0):
    panel(cr, x, y, w, h, CHALK, r=10, lw=8)
    for k, ln in enumerate(lines):
        q = clamp(p * len(lines) - k)
        if q > 0:
            text(cr, ln, x + w / 2, y + 140 + k * 100, 72, (0.95, 0.95, 0.90), alpha=q, bold=False)


# ================= SCENES
def s0(cr, t):  # hook: oldest HBCU started with a will and $10,000 (Bo reacts)
    i = 0; a, b = scene_bounds(i)
    bg(cr)
    tw = beat(i, "will,")
    bo(cr, 400, 1040, 0.58, t, pose="think" if t < tw else "point", wide=1.0 if t > tw else 0.3,
       brow=0.8 if t > tw else 0.2, talk=False)
    pop_text(cr, "AMERICA'S OLDEST HBCU", 1220, 170, 92, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    pc = prog(t, beat(i, "campus"), 0.4)
    pb = prog(t, a + 0.4, 0.45)
    if pb > 0 and t < tw:
        cr.save(); cr.translate(1220, 880); cr.scale(back_out(pb), back_out(pb)); cr.translate(-1220, -880)
        building(cr, 1220, 880, 560, 320, CU_BLUE)
        cr.restore()
        pop_text(cr, "A CAMPUS?", 1220, 330, 70, t, a + 0.6, color=TEXT, outline=(1, 1, 1)) if pc <= 0 else None
    if pc > 0 and t < tw:
        cr.set_source_rgba(*RED, pc); cr.set_line_width(22); cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(900, 460); cr.line_to(900 + 640 * pc, 460 + 420 * pc)
        cr.move_to(1540, 460); cr.line_to(1540 - 640 * pc, 460 + 420 * pc); cr.stroke()
        pop_text(cr, "NO CAMPUS", 1220, 330, 70, t, beat(i, "campus"), color=RED, outline=(1, 1, 1))
    if t >= tw:
        will_doc(cr, 1220, 600, 0.95, prog(t, tw, 0.45), amount_p=prog(t, beat(i, "ten thousand"), 0.4))
        pop_text(cr, "JUST A WILL", 1220, 300, 70, t, tw, color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s1(cr, t):  # Richard Humphreys, Quaker in Philadelphia; $10,000, 1/10 of estate, school for Black youth
    i = 1; a, b = scene_bounds(i)
    row_houses(cr)
    pr = prog(t, a + 0.15, 0.45)
    humphreys(cr, 520, 1050, 1.2 * back_out(pr), t, pose="hold" if t > beat(i, "He left") else "rest")
    name_tag(cr, "Richard Humphreys", "Quaker · Philadelphia", 520, 120, prog(t, beat(i, "Richard"), 0.4), size=48)
    tl = beat(i, "He left")
    if t > tl:
        will_doc(cr, 1300, 560, 0.75, prog(t, tl, 0.45), amount_p=prog(t, beat(i, "ten thousand"), 0.4))
    pt = prog(t, beat(i, "one tenth"), 0.5)
    if pt > 0:
        tenth_pie(cr, 1690, 330, 120, pt)
        panel(cr, 1480, 470, 420, 70, (1, 1, 1), r=16, lw=4, alpha=pt)
        text(cr, "1/10 OF HIS ESTATE", 1690, 520, 38, TEXT, alpha=pt)
    ps = prog(t, beat(i, "school for Black"), 0.4)
    if ps > 0:
        stamp(cr, "A SCHOOL FOR BLACK YOUTH", 1300, 990, ps, col=MAROON, size=54)
    sceneout(cr, t, a, b)


def s2(cr, t):  # will: trades, farming, teachers; 1837 founded; Institute for Colored Youth
    i = 2; a, b = scene_bounds(i)
    t37 = beat(i, "In eighteen")
    if t < t37:
        row_houses(cr)
        cr.set_source_rgba(*BG, 0.55); cr.paint()
        humphreys(cr, 360, 1050, 1.0, t, pose="hold")
        checklist(cr, 760, 230, ["TRADES", "FARMING", "TEACHERS"],
                  [beat(i, "trades"), beat(i, "farming"), beat(i, "teachers")], t, prog(t, a + 0.1, 0.4))
        will_doc(cr, 1630, 620, 0.55, 1.0, amount_p=1.0, rot=0.06)
    else:
        bg(cr, (0.82, 0.88, 0.96), (0.96, 0.92, 0.84))
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.70, 0.68, 0.64); cr.fill()
        building(cr, 960, 880, 760, 330, BRICK, cols=4)
        pk = prog(t, t37 + 0.3, 2.5)
        for k in range(5):
            kx = 200 + k * 120 + ease(pk) * 300
            kid(cr, kx, 1010, 0.9, dress=DRESSES[k % len(DRESSES)], girl=k % 2 == 0, t=t + k, walking=pk < 1)
        pop_text(cr, "1837", 960, 210, 170, t, beat(i, "eighteen"), color=MAROON, outline=(1, 1, 1))
        pi_ = prog(t, beat(i, "Institute"), 0.4)
        if pi_ > 0:
            panel(cr, 360, 270, 1200, 120, CU_BLUE, r=22, alpha=pi_)
            text(cr, "INSTITUTE FOR COLORED YOUTH", 960, 350, 60, (1, 1, 1), alpha=pi_)
    sceneout(cr, t, a, b)


def s3(cr, t):  # Bo: part nobody hears; 1869 Fanny Jackson Coppin head principal; born enslaved; aunt; Oberlin
    i = 3; a, b = scene_bounds(i)
    t69 = beat(i, "In eighteen")
    if t < t69:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY HEARS", W / 2, 140, 90, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    else:
        bg(cr, (0.95, 0.92, 0.98), (0.90, 0.86, 0.94))
        tg = beat(i, "graduate")
        pf = prog(t, t69 + 0.1, 0.45)
        fanny(cr, 640, 1050, 1.3 * back_out(pf), t, pose="hold" if t > tg else "rest", cap=t > tg)
        name_tag(cr, "Fanny Jackson Coppin", None, 640, 120, prog(t, beat(i, "Fanny"), 0.4), size=50)
        tb = beat(i, "She was born")
        if t < tb:
            pop_text(cr, "1869", 1400, 330, 170, t, beat(i, "eighteen"), color=MAROON, outline=(1, 1, 1))
            ph = prog(t, beat(i, "head principal"), 0.4)
            if ph > 0:
                stamp(cr, "HEAD PRINCIPAL", 1400, 560, ph, col=CU_BLUE, size=70)
        elif t < tg:
            stamp(cr, "BORN ENSLAVED", 1400, 300, prog(t, tb, 0.4), col=RED, size=70)
            pa = prog(t, beat(i, "Her aunt"), 0.45)
            if pa > 0:
                woman(cr, 1280, 1050, 1.0 * back_out(pa), t, dress=AUNT_DRESS, pose="open")
                text(cr, "HER AUNT", 1280, 560, 44, TEXT, alpha=pa, outline=(1, 1, 1))
                pop_text(cr, "BOUGHT HER FREEDOM", 1400, 440, 64, t, beat(i, "bought"), color=(0.15, 0.50, 0.25),
                         outline=(1, 1, 1))
        else:
            po = prog(t, beat(i, "Oberlin"), 0.4)
            if po > 0:
                panel(cr, 1050, 330, 700, 210, MAROON, r=24, alpha=po)
                text(cr, "OBERLIN COLLEGE", 1400, 420, 64, GOLDC, alpha=po)
                text(cr, "graduate", 1400, 495, 46, (1, 1, 1), alpha=po)
    sceneout(cr, t, a, b)


def s4(cr, t):  # led the school 30+ years training teachers; Coppin State University, Baltimore
    i = 4; a, b = scene_bounds(i)
    bg(cr, (0.93, 0.93, 0.90), (0.86, 0.86, 0.82))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.72, 0.62, 0.48); cr.fill()
    td = beat(i, "Today")
    if t < td:
        chalkboard(cr, 860, 150, 920, 380, ["TEACHERS FOR", "BLACK CLASSROOMS"], prog(t, a + 0.3, 1.2))
        fanny(cr, 470, 1050, 1.15, t, pose="point")
        for k in range(4):
            kid(cr, 900 + k * 230, 1040, 1.0, dress=DRESSES[k % len(DRESSES)], girl=k % 2 == 1, t=t + k)
        pop_text(cr, "30+ YEARS", 470, 200, 110, t, beat(i, "thirty"), color=MAROON, outline=(1, 1, 1))
    else:
        fanny(cr, 560, 1050, 1.3, t, pose="open")
        pc = prog(t, beat(i, "Coppin State"), 0.45)
        if pc > 0:
            panel(cr, 960, 260, 820, 260, (0.12, 0.22, 0.55), r=26, alpha=pc)
            text(cr, "COPPIN STATE", 1370, 370, 84, GOLDC, alpha=pc)
            text(cr, "UNIVERSITY", 1370, 460, 64, (1, 1, 1), alpha=pc)
        pop_text(cr, "BALTIMORE", 1370, 640, 70, t, beat(i, "Baltimore"), color=TEXT, outline=(1, 1, 1))
        pn = prog(t, beat(i, "carries her name"), 0.4)
        if pn > 0:
            stamp(cr, "NAMED FOR HER", 1370, 820, pn, col=MAROON, size=60)
    sceneout(cr, t, a, b)


def s5(cr, t):  # early 1900s: moved to George Cheyney's farm west of Philadelphia -> Cheyney University
    i = 5; a, b = scene_bounds(i)
    farm_bg(cr)
    barn(cr, 1450, 880, 1.0)
    kicker(cr, "EARLY 1900s", t, a + 0.2)
    pw = prog(t, beat(i, "west of"), 0.5) * (1 - prog(t, beat(i, "Cheyney University") - 0.3, 0.3))
    if pw > 0:
        panel(cr, 520, 180, 760, 110, (1, 1, 1), r=20, alpha=pw)
        text(cr, "← WEST OF PHILADELPHIA", 900, 255, 50, TEXT, alpha=pw)
    pg = prog(t, beat(i, "George"), 0.45)
    if pg > 0:
        cheyney_farmer(cr, 560, 1050, 1.15 * back_out(pg), t, pose="open" if t > beat(i, "That's") else "rest")
        name_tag(cr, "George Cheyney", "owned the farm", 560, 340, pg, size=46)
    pu = prog(t, beat(i, "Cheyney University"), 0.45)
    if pu > 0:
        panel(cr, 860, 150, 1000, 200, CU_BLUE, r=26, alpha=pu)
        text(cr, "CHEYNEY UNIVERSITY", 1360, 245, 80, (1, 1, 1), alpha=pu)
        text(cr, "OF PENNSYLVANIA", 1360, 315, 50, GOLDC, alpha=pu)
    sceneout(cr, t, a, b)


def s6(cr, t):  # outro: Bo hosts
    i = 6; a, b = scene_bounds(i)
    bg(cr)
    bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=False)
    pop_text(cr, "1 WILL → OLDEST HBCU", 1250, 260, 96, t, a + 0.3, color=MAROON, outline=GOLDC)
    text(cr, "Which HBCU founder", 1250, 440, 70, TEXT)
    text(cr, "should we cover next?", 1250, 530, 66, MAROON)
    pop_text(cr, "Tell us in the comments", 1250, 700, 56, t, beat(i, "Tell us"))
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    sceneout(cr, t, a, 1e9)


def thumb_hero(cr, x, y, r):
    """Hero object: the parchment will with $10,000."""
    will_doc(cr, x, y, r / 260.0, 1.0, amount_p=1.0)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
