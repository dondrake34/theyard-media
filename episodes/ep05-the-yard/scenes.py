"""Ep05 scenes: "The Yard" via Howard University. One function per narration paragraph, timed with beat(i, phrase)."""
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


HOWARD_BLUE = (0.14, 0.24, 0.50)
BRICK = (0.66, 0.30, 0.24)
GRASS = (0.52, 0.68, 0.40)
GRASS_DK = (0.42, 0.58, 0.33)


def lawn(cr, y=700, sky_top=(0.62, 0.82, 0.95), sky_bot=(0.97, 0.93, 0.80)):
    g = cairo.LinearGradient(0, 0, 0, y)
    g.add_color_stop_rgb(0, *sky_top); g.add_color_stop_rgb(1, *sky_bot)
    cr.set_source(g); cr.rectangle(0, 0, W, y); cr.fill()
    cr.rectangle(0, y, W, H - y); cr.set_source_rgb(*GRASS); cr.fill()
    for k in range(0, W, 120):
        cr.move_to(k, y + 40 + (k % 240) / 4); cr.line_to(k + 60, y + 40 + (k % 240) / 4)
    cr.set_source_rgb(*GRASS_DK); cr.set_line_width(6); cr.stroke()


def tree(cr, x, y, s=1.0, letters=None, t=0.0, lp=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-22, -230, 44, 230); cr.set_source_rgb(*BROWN); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for cx, cy, r in ((0, -330, 120), (-90, -270, 85), (90, -270, 85)):
        cr.arc(cx, cy, r, 0, 2 * math.pi); cr.set_source_rgb(0.30, 0.50, 0.30); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    if letters and lp > 0:  # painted Greek-letter sign on the trunk
        rounded_rect(cr, -75, -190, 150, 70, 14); cr.set_source_rgba(*HOWARD_BLUE, lp); cr.fill_preserve()
        cr.set_source_rgba(*GOLDC, lp); cr.set_line_width(5); cr.stroke()
        text(cr, letters, 0, -140, 48, (1, 1, 1), alpha=lp)
    cr.restore()


def founders_library(cr, cx, gy, s=1.0, build=1.0):
    """Stylized brick Georgian library with white columns, pediment and cupola (generic, not a portrait)."""
    if build <= 0:
        return
    cr.save(); cr.translate(cx, gy); cr.scale(s, s)
    cr.rectangle(-560, -300, 1120, 300); cr.set_source_rgb(*BRICK); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for side in (-1, 1):
        for r in range(2):
            for c in range(4):
                wx = side * (250 + c * 75) - 20 * (1 if side > 0 else 1)
                wy = -250 + r * 120
                cr.rectangle(wx - 20, wy, 40, 76); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
                cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-190, -330, 380, 330); cr.set_source_rgb(0.97, 0.96, 0.92); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for k in range(5):
        cr.rectangle(-165 + k * 76, -300, 24, 300); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.move_to(-215, -330); cr.line_to(0, -430); cr.line_to(215, -330); cr.close_path()
    cr.set_source_rgb(0.97, 0.96, 0.92); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(-60, -520, 120, 100); cr.set_source_rgb(1, 1, 1); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-75, -520); cr.line_to(0, -600); cr.line_to(75, -520); cr.close_path()
    cr.set_source_rgb(*HOWARD_BLUE); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-30, -120, 60, 120); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


def book_stack(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    for k, (w, col) in enumerate(((220, MAROON), (190, HOWARD_BLUE), (205, GOLDC))):
        cr.rectangle(-w / 2, -40 * (k + 1), w, 40); cr.set_source_rgb(*col); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.restore()


def crowd(cr, y, t, n=7, x0=200, gap=250, s=0.55, start=0.0):
    for k in range(n):
        q = prog(t, start + k * 0.08, 0.35)
        if q <= 0:
            continue
        x = x0 + k * gap
        if k % 2:
            woman(cr, x, y, s * back_out(q), t + k * 0.4, dress=DRESSES[k % 5], pose="rest")
        else:
            man(cr, x, y, s * 0.95 * back_out(q), t + k * 0.4, suit=COATS[k % 4], tie=(0.9, 0.9, 0.9), pose="rest")


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


# ================= SCENES
def s0(cr, t):  # hook: the quad vs. the Yard
    i = 0; a, b = scene_bounds(i)
    lawn(cr, 640)
    tree(cr, 260, 760, 0.9, t=t); tree(cr, 1660, 760, 0.9, t=t)
    crowd(cr, 880, t, n=5, x0=420, gap=240, s=0.5, start=beat(i, "But on many"))
    pq = prog(t, a + 0.2, 0.4)
    swap = prog(t, beat(i, "The Yard."), 0.35)
    if swap < 1:
        pop_text(cr, "THE QUAD", W / 2, 260, 150, t, a + 0.2, color=TEXT, outline=(1, 1, 1))
        if prog(t, beat(i, "But on many"), 0.3) > 0:
            cr.set_source_rgba(0.8, 0.1, 0.1, 1 - swap); cr.set_line_width(14)
            cr.move_to(W / 2 - 330, 235); cr.line_to(W / 2 + 330, 215); cr.stroke()
    if swap > 0:
        pop_text(cr, "THE YARD", W / 2, 290, 190, t, beat(i, "The Yard."), color=HOWARD_BLUE, outline=GOLDC)
    bo(cr, 1720, 1075, 0.5, t, pose="point", talk=t < P[i][1])
    sceneout(cr, t, a, b)


def s1(cr, t):  # students meet between classes; Howard, Washington D.C.
    i = 1; a, b = scene_bounds(i)
    lawn(cr, 600)
    capitol(cr, 1500, 600, 0.55)
    tree(cr, 180, 760, 0.8, t=t)
    crowd(cr, 900, t, n=7, x0=300, gap=240, s=0.6, start=a + 0.2)
    pop_text(cr, "BETWEEN CLASSES", 760, 190, 90, t, beat(i, "meet between"), color=TEXT, outline=(1, 1, 1))
    ph = prog(t, beat(i, "And at Howard"), 0.4)
    if ph > 0:
        panel(cr, 330, 280, 780, 200, HOWARD_BLUE, r=24, alpha=ph)
        text(cr, "HOWARD UNIVERSITY", 720, 370, 66, (1, 1, 1), alpha=ph)
        text(cr, "Washington, D.C.", 720, 445, 46, GOLDC, alpha=ph)
    sceneout(cr, t, a, b)


def s2(cr, t):  # Founders Library, 1939
    i = 2; a, b = scene_bounds(i)
    lawn(cr, 760)
    tree(cr, 150, 900, 0.8, t=t); tree(cr, 1780, 900, 0.8, t=t)
    founders_library(cr, W / 2, 800, 0.95, prog(t, a, 0.3))
    pop_text(cr, "FOUNDERS LIBRARY", W / 2, 130, 90, t, beat(i, "Founders Library"), color=TEXT, outline=(1, 1, 1))
    pop_text(cr, "1939", 330, 440, 140, t, beat(i, "nineteen"), color=GOLDC, outline=INK)
    pi_ = prog(t, beat(i, "modeled"), 0.4)
    if pi_ > 0:
        panel(cr, 1330, 230, 480, 120, (1, 1, 1), r=22, alpha=pi_)
        text(cr, "Modeled on", 1570, 285, 36, TEXT, alpha=pi_)
        text(cr, "Independence Hall", 1570, 330, 42, MAROON, alpha=pi_)
    sceneout(cr, t, a, b)


def s3(cr, t):  # law school in the library; Thurgood Marshall; Brown v. Board
    i = 3; a, b = scene_bounds(i)
    bg(cr, (0.90, 0.86, 0.78), (0.80, 0.72, 0.60))
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(*WOOD_DK); cr.fill()
    for k in range(5):  # bookshelf wall
        cr.rectangle(80 + k * 130, 200, 110, 560); cr.set_source_rgb(*WOOD); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
        for r in range(4):
            for c in range(4):
                cr.rectangle(90 + k * 130 + c * 24, 220 + r * 135, 18, 100)
                cr.set_source_rgb(*[MAROON, HOWARD_BLUE, GOLDC, GREEN][(r + c + k) % 4]); cr.fill()
    pop_text(cr, "HOWARD LAW SCHOOL", 1100, 140, 70, t, beat(i, "law"), color=TEXT, outline=(1, 1, 1))
    man(cr, 1050, 930, 1.05, t, suit=CHAR, tie=MAROON, skin=BLACK, pose="hold" if t > beat(i, "Inside") else "rest")
    book_stack(cr, 1330, 930, 1.0)
    pn = prog(t, beat(i, "Thurgood"), 0.4)
    name_tag(cr, "Thurgood Marshall", None, 1050, 960, pn, size=44)
    pc = prog(t, beat(i, "Brown versus"), 0.4)
    if pc > 0:
        panel(cr, 1300, 330, 560, 200, (1, 1, 1), r=24, alpha=pc)
        text(cr, "BROWN v. BOARD", 1580, 420, 54, MAROON, alpha=pc)
        text(cr, "of Education", 1580, 480, 40, TEXT, alpha=pc)
    ps = prog(t, beat(i, "struck"), 0.4)
    if ps > 0:
        stamp(cr, "SEGREGATED SCHOOLS ENDED", 1500, 640, ps, size=34)
    sceneout(cr, t, a, b)


def s4(cr, t):  # 2001 National Historic Landmark
    i = 4; a, b = scene_bounds(i)
    lawn(cr, 700)
    founders_library(cr, 1330, 760, 0.7, 1.0)
    pop_text(cr, "2001", 560, 250, 200, t, beat(i, "two"), color=GOLDC, outline=INK)
    pb = prog(t, beat(i, "National"), 0.4)
    if pb > 0:
        panel(cr, 140, 380, 820, 220, HOWARD_BLUE, r=26, alpha=pb)
        text(cr, "NATIONAL", 550, 470, 70, (1, 1, 1), alpha=pb)
        text(cr, "HISTORIC LANDMARK", 550, 560, 66, GOLDC, alpha=pb)
    pt = prog(t, beat(i, "three of"), 0.4)
    if pt > 0:
        text(cr, "The Yard + 3 buildings", 550, 680, 48, TEXT, alpha=pt)
    sceneout(cr, t, a, b)


def s5(cr, t):  # culture: Divine Nine letters, homecoming 1924, Yardfest
    i = 5; a, b = scene_bounds(i)
    lawn(cr, 620)
    for k, (x, L) in enumerate(((220, "ΑΚΑ"), (620, "ΩΨΦ"), (1020, "ΔΣΘ"), (1420, "ΦΒΣ"), (1760, "ΖΦΒ"))):
        tree(cr, x, 850, 0.7, letters=L, t=t, lp=prog(t, beat(i, "Five of") + k * 0.15, 0.35))
    crowd(cr, 1030, t, n=8, x0=180, gap=230, s=0.5, start=a + 0.3)
    pop_text(cr, "5 OF THE DIVINE 9", 960, 130, 90, t, beat(i, "Five of"), color=HOWARD_BLUE, outline=(1, 1, 1))
    ph = prog(t, beat(i, "Howard's homecoming"), 0.4)
    if ph > 0:
        panel(cr, 90, 190, 560, 110, GOLDC, r=22, alpha=ph)
        text(cr, "HOMECOMING SINCE 1924", 370, 262, 40, INK, alpha=ph)
    py = prog(t, beat(i, "Yardfest"), 0.4)
    if py > 0:
        panel(cr, 1270, 190, 560, 110, MAROON, r=22, alpha=py)
        text(cr, "YARDFEST", 1550, 265, 56, GOLDC, alpha=py)
    sceneout(cr, t, a, b)


def s6(cr, t):  # outro: Bo hosts
    i = 6; a, b = scene_bounds(i)
    bg(cr)
    bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=t < P[i][1])
    pop_text(cr, "THE YARD", 1250, 260, 130, t, a + 0.3, color=GOLDC, outline=INK)
    text(cr, "What do you call", 1250, 440, 70, TEXT)
    text(cr, "the heart of your campus?", 1250, 530, 66, MAROON)
    pop_text(cr, "Tell us in the comments", 1250, 700, 56, t, beat(i, "Tell us"))
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    sceneout(cr, t, a, 1e9)


def thumb_hero(cr, x, y, r):
    """Hero object: a tree with painted Greek letters (the Yard)."""
    s = r / 150.0
    tree(cr, x, y + 150 * s, s * 0.7, letters="ΑΩ", lp=1.0)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
