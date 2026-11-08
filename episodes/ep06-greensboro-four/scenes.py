"""Ep06 scenes: the Greensboro Four. One function per narration paragraph, timed with beat(i, phrase)."""
from lib import *

NAVY = (0.16, 0.20, 0.34)
CHAR = (0.25, 0.25, 0.28)
GRAY = (0.80, 0.80, 0.80)
SKIN_LT = (0.93, 0.80, 0.68)
RED = (0.78, 0.14, 0.14)
PAPER = (0.98, 0.95, 0.86)
WOOD = (0.62, 0.48, 0.32)
WOOD_DK = (0.42, 0.31, 0.20)
FISK_BLUE = (0.18, 0.30, 0.58)   # school colour (blue and gold); no logos or seals
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


AT_BLUE = (0.16, 0.26, 0.55)   # school colours (blue and gold); no logos or seals
AT_GOLD = GOLDC
TILE = (0.90, 0.88, 0.80)
RED_S = (0.74, 0.16, 0.16)
FOUR = [  # (name, suit, tie)
    ("Ezell Blair Jr.", (0.25, 0.25, 0.30), MAROON),
    ("David Richmond", (0.30, 0.22, 0.16), AT_GOLD),
    ("Franklin McCain", AT_BLUE, (0.9, 0.9, 0.9)),
    ("Joseph McNeil", (0.18, 0.30, 0.26), RED_S),
]


def store_wall(cr, t, sign=True):
    bg(cr, (0.96, 0.92, 0.82), (0.90, 0.84, 0.72))
    cr.rectangle(0, 700, W, 380); cr.set_source_rgb(*TILE); cr.fill()
    for k in range(0, W, 120):
        cr.move_to(k, 700); cr.line_to(k, H)
    cr.set_source_rgba(0, 0, 0, 0.08); cr.set_line_width(3); cr.stroke()
    cr.rectangle(0, 690, W, 16); cr.set_source_rgb(*WOOD_DK); cr.fill()


def counter(cr, t, y=760, stools=6, x0=260, gap=270):
    for k in range(stools):
        x = x0 + k * gap
        cr.rectangle(x - 8, y + 130, 16, 190); cr.set_source_rgb(0.55, 0.55, 0.58); cr.fill()
        cr.save(); cr.translate(x, y + 125); cr.scale(1, 0.35); cr.arc(0, 0, 62, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*RED_S); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(0, y + 30, W, 80); cr.set_source_rgb(*WOOD); cr.fill()
    cr.rectangle(0, y, W, 44); cr.set_source_rgb(0.95, 0.94, 0.90); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()


def mug(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-20, -40, 40, 40); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.arc(24, -22, 12, -1.5, 1.5); cr.stroke(); cr.restore()


def whites_only_sign(cr, x, y, p, s=1.0):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(0, -10); cr.line_to(0, -90); cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    panel(cr, -230, -310, 460, 220, (1, 1, 1), r=18, lw=6, alpha=p)
    text(cr, "WHITE", 0, -225, 62, RED_S, alpha=p)
    text(cr, "CUSTOMERS ONLY", 0, -150, 46, RED_S, alpha=p)
    cr.restore()


def student_row(cr, t, n, y, s=0.62, x0=420, gap=300, pose="rest", start=0.0, seated=True):
    for k in range(n):
        q = prog(t, start + k * 0.12, 0.4)
        if q <= 0:
            continue
        nm, suit, tie = FOUR[k % 4]
        man(cr, x0 + k * gap, y, s * back_out(q), t + k * 0.5, suit=suit, tie=tie, skin=BLACK, pose=pose)


def tagrow(cr, t, start, x0=420, gap=300, y=1000, step=0.45, size=30):
    for k, (nm, _, _) in enumerate(FOUR):
        p = prog(t, start + k * step, 0.35)
        if p > 0:
            parts = nm.split(" ", 1)
            name_tag(cr, nm, None, x0 + k * gap, y, p, size=size)


# ================= SCENES
def s0(cr, t):  # hook: four freshmen at the lunch counter
    i = 0; a, b = scene_bounds(i)
    store_wall(cr, t)
    counter(cr, t)
    student_row(cr, t, 4, 1075, 1.3, x0=420, gap=370, start=a + 0.2)
    for k in range(4):
        mug(cr, 420 + k * 370 + 165, 772, 1.3)
    pop_text(cr, "4 FRESHMEN", W / 2, 190, 130, t, beat(i, "Four college"), color=AT_BLUE, outline=(1, 1, 1))
    pop_text(cr, "1 LUNCH COUNTER", W / 2, 330, 90, t, beat(i, "lunch counter"), color=TEXT, outline=(1, 1, 1))
    pl = prog(t, beat(i, "refused"), 0.4)
    if pl > 0:
        stamp(cr, "WON'T LEAVE", 1500, 520, pl, col=RED_S, size=64)
    sceneout(cr, t, a, b)


def s1(cr, t):  # the four, North Carolina A&T
    i = 1; a, b = scene_bounds(i)
    bg(cr, (0.80, 0.86, 0.95), (0.96, 0.93, 0.84))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(*GRASS); cr.fill()
    cr.rectangle(260, 420, 1400, 460); cr.set_source_rgb(*BRICK); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for r in range(2):
        for c in range(9):
            cr.rectangle(310 + c * 150, 470 + r * 150, 70, 100); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(880, 740, 160, 140); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    pb = prog(t, beat(i, "North Carolina"), 0.4)
    if pb > 0:
        panel(cr, 330, 100, 1260, 210, AT_BLUE, r=28, alpha=pb)
        text(cr, "NORTH CAROLINA A&T", 960, 200, 84, (1, 1, 1), alpha=pb)
        text(cr, "Greensboro, N.C.", 960, 275, 44, AT_GOLD, alpha=pb)
    for k, (nm, suit, tie) in enumerate(FOUR):
        q = prog(t, a + 0.3 + k * 0.25, 0.4)
        if q > 0:
            man(cr, 420 + k * 360, 1070, 1.1 * back_out(q), t + k, suit=suit, tie=tie, skin=BLACK, pose="rest")
        pn = prog(t, beat(i, ["Ezell", "David", "Franklin", "Joseph"][k]) - 0.1, 0.4)
        name_tag(cr, nm.split()[0], " ".join(nm.split()[1:]), 420 + k * 360, 330, pn, size=40)
    sceneout(cr, t, a, b)


def s2(cr, t):  # Woolworth's store, Feb 1 1960, white customers only
    i = 2; a, b = scene_bounds(i)
    store_wall(cr, t)
    counter(cr, t)
    panel(cr, 520, 90, 880, 150, (1, 1, 1), r=24)
    text(cr, "WOOLWORTH'S", 960, 195, 84, RED_S)
    pop_text(cr, "FEB. 1, 1960", 560, 400, 100, t, beat(i, "February"), color=GOLDC, outline=INK)
    # the four walk in from the left
    for k, (nm, suit, tie) in enumerate(FOUR):
        q = prog(t, beat(i, "they walked") - 0.2 + k * 0.15, 1.6)
        x = -150 + (520 + k * 280) * ease(q)
        man(cr, x, 1060, 1.15, t + k * 0.3, suit=suit, tie=tie, skin=BLACK, pose="rest", walking=q < 1)
    whites_only_sign(cr, 1550, 700, prog(t, beat(i, "white customers"), 0.4), 1.05)
    sceneout(cr, t, a, b)


def s3(cr, t):  # they sat, refused, stayed until closing
    i = 3; a, b = scene_bounds(i)
    store_wall(cr, t)
    counter(cr, t)
    student_row(cr, t, 4, 1075, 1.3, x0=420, gap=370, start=a)
    for k in range(4):
        mug(cr, 420 + k * 370 + 165, 772, 1.3)
    pr = prog(t, beat(i, "They were refused"), 0.4)
    if pr > 0:
        stamp(cr, "REFUSED", 1450, 330, pr, col=RED_S, size=90)
    # clock: store closing
    pc = prog(t, beat(i, "until the store"), 0.5)
    cx, cy = 260, 300
    cr.arc(cx, cy, 90, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    ang = -math.pi / 2 + 2 * math.pi * (0.25 + 0.5 * pc)
    cr.move_to(cx, cy); cr.line_to(cx + 65 * math.cos(ang), cy + 65 * math.sin(ang)); cr.set_line_width(8); cr.stroke()
    cr.move_to(cx, cy); cr.line_to(cx, cy - 45); cr.stroke()
    pop_text(cr, "STAYED SEATED", 960, 150, 100, t, beat(i, "stayed in"), color=AT_BLUE, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s4(cr, t):  # more students join, spread
    i = 4; a, b = scene_bounds(i)
    store_wall(cr, t)
    counter(cr, t, stools=7, x0=200, gap=250)
    student_row(cr, t, 7, 1075, 1.05, x0=230, gap=250, start=a)
    pop_text(cr, "DAY 2: MORE JOIN", 960, 150, 100, t, beat(i, "The next day"), color=AT_BLUE, outline=(1, 1, 1))
    ps = prog(t, beat(i, "Within days"), 0.5)
    if ps > 0:
        panel(cr, 1180, 230, 640, 230, (1, 1, 1), r=26, alpha=ps)
        text(cr, "SIT-INS SPREAD", 1500, 320, 54, MAROON, alpha=ps)
        for k, c in enumerate(("Durham", "Winston-Salem")):
            pc = prog(t, beat(i, ["popping", "North Carolina"][k]), 0.4)
            text(cr, c, 1500, 385 + k * 55, 40, TEXT, alpha=pc * ps)
    pst = prog(t, beat(i, "Soon"), 0.4)
    if pst > 0:
        stamp(cr, "OTHER STATES", 1500, 560, pst, col=AT_BLUE, size=60)
    sceneout(cr, t, a, b)


def s5(cr, t):  # Bo: the part nobody tells you; calm and peaceful; July 25, 1960
    i = 5; a, b = scene_bounds(i)
    store_wall(cr, t)
    counter(cr, t)
    student_row(cr, t, 4, 1075, 1.1, x0=720, gap=340, start=a + 0.1)
    bo(cr, 230, 1000, 0.45, t, pose="point", talk=t < beat(i, "It all"))
    pop_text(cr, "CALM. PEACEFUL.", 1060, 150, 100, t, beat(i, "calm"), color=AT_BLUE, outline=(1, 1, 1))
    pj = prog(t, beat(i, "On July"), 0.4)
    if pj > 0:
        panel(cr, 1050, 230, 720, 190, AT_GOLD, r=26, alpha=pj)
        text(cr, "JULY 25, 1960", 1410, 330, 76, INK, alpha=pj)
        text(cr, "the counter served everyone", 1410, 390, 38, INK, alpha=prog(t, beat(i, "finally"), 0.4))
    sceneout(cr, t, a, b)


def s6(cr, t):  # outro: Bo hosts
    i = 6; a, b = scene_bounds(i)
    bg(cr)
    bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=t < P[i][1])
    pop_text(cr, "ONE SEAT.", 1250, 260, 130, t, a + 0.3, color=AT_BLUE, outline=GOLDC)
    text(cr, "Which HBCU story", 1250, 440, 70, TEXT)
    text(cr, "should we tell next?", 1250, 530, 66, MAROON)
    pop_text(cr, "Tell us in the comments", 1250, 700, 56, t, beat(i, "Tell us"))
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    sceneout(cr, t, a, 1e9)


def thumb_hero(cr, x, y, r):
    """Hero object: a lunch-counter stool and mug."""
    s = r / 150.0
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-8, 20, 16, 120); cr.set_source_rgb(0.55, 0.55, 0.58); cr.fill()
    cr.save(); cr.translate(0, 10); cr.scale(1, 0.4); cr.arc(0, 0, 110, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgb(*RED_S); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.restore()


SCENES = [s0, s1, s2, s3, s4, s5, s6]
