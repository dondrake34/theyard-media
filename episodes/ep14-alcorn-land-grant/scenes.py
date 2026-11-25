"""Ep14 scenes: Alcorn State, the oldest public Black land-grant college (1871), and Hiram Revels. One function per paragraph."""
from lib import *

HAIR_DK = (0.10, 0.08, 0.07)
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
    if s <= 0.01:
        return
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
    if s <= 0.01:
        return
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




def mustache(cr, x, hy, s, col=HAIR_DK, w=24):
    """Thin mustache bar under the eyes (no mouth, no lips)."""
    cr.save(); cr.translate(x, hy); cr.scale(s, s)
    rounded_rect(cr, -w, 16, 2 * w, 8, 4); cr.set_source_rgb(*col); cr.fill()
    cr.restore()


def glasses(cr, x, hy, s):
    cr.save(); cr.translate(x, hy); cr.scale(s, s)
    cr.set_source_rgb(*INK); cr.set_line_width(4)
    for dx in (-16, 16):
        cr.arc(dx, -4, 13, 0, 2 * math.pi); cr.stroke()
    cr.move_to(-3, -4); cr.line_to(3, -4); cr.stroke()
    cr.restore()


def grad_cap(cr, x, hy, s):
    cr.save(); cr.translate(x, hy); cr.scale(s, s)
    cr.move_to(-72, -56); cr.line_to(0, -84); cr.line_to(72, -56); cr.line_to(0, -30); cr.close_path()
    cr.set_source_rgb(*BLACK); cr.fill()
    cr.move_to(56, -54); cr.line_to(64, -12); cr.set_source_rgb(*GOLDC); cr.set_line_width(4); cr.stroke()
    cr.restore()


def head_y(y, s, t):
    return y + (-385 + math.sin(t * 2.0) * 2) * s


def street(cr, sky=(0.84, 0.90, 0.97)):
    bg(cr, sky, (0.96, 0.93, 0.86))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.72, 0.70, 0.66); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


def arrow(cr, x0, y0, x1, y1, p, col=MAROON, lw=16):
    if p <= 0:
        return
    xe = x0 + (x1 - x0) * ease(p); ye = y0 + (y1 - y0) * ease(p)
    cr.set_source_rgba(*col, min(1, p * 2)); cr.set_line_width(lw); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x0, y0); cr.line_to(xe, ye); cr.stroke()
    ang = math.atan2(y1 - y0, x1 - x0)
    cr.move_to(xe, ye)
    cr.line_to(xe - 40 * math.cos(ang - 0.5), ye - 40 * math.sin(ang - 0.5))
    cr.line_to(xe - 40 * math.cos(ang + 0.5), ye - 40 * math.sin(ang + 0.5)); cr.close_path(); cr.fill()



WOOD_DK = (0.42, 0.31, 0.20)
def brick(cr, x, y, w=70, h=32, col=BRICK):
    cr.rectangle(x - w / 2, y - h / 2, w, h); cr.set_source_rgb(*col); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()

def money(cr, x, y, label, p, w=420, h=190, col=(0.55, 0.72, 0.50)):
    if p <= 0:
        return
    k = back_out(p)
    cr.save(); cr.translate(x, y); cr.scale(k, k); cr.rotate(-0.05)
    rounded_rect(cr, -w / 2, -h / 2, w, h, 16); cr.set_source_rgb(*col); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    rounded_rect(cr, -w / 2 + 18, -h / 2 + 18, w - 36, h - 36, 10); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()
    text(cr, label, 0, h * 0.2, h * 0.5, (0.12, 0.30, 0.14))
    cr.restore()


AT_BLUE = (0.16, 0.26, 0.55)   # school colours (blue and gold); no logos or seals
AT_GOLD = GOLDC
TILE = (0.90, 0.88, 0.80)
RED_S = (0.74, 0.16, 0.16)
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





STU_SKINS = [BLACK, (0.34, 0.22, 0.15), (0.42, 0.28, 0.19), (0.26, 0.17, 0.12)]
STU_COATS = [CHAR, NAVY, (0.30, 0.22, 0.16), (0.18, 0.30, 0.26), (0.36, 0.16, 0.20)]
def student(cr, k, x, y, s, t, pose="rest", walking=False):
    skin = STU_SKINS[k % len(STU_SKINS)]
    if k % 3 == 1:
        woman(cr, x, y, s, t + k * 0.4, dress=DRESSES[k % len(DRESSES)], skin=skin, pose=pose, walking=walking,
              hair=HAIR_DK)
    else:
        man(cr, x, y, s, t + k * 0.4, suit=STU_COATS[k % len(STU_COATS)], tie=[MAROON, GOLDC, (0.9, 0.9, 0.9)][k % 3],
            skin=skin, hair=HAIR_DK, pose=pose, walking=walking)


def crowd(cr, t, n, x0, gap, y, s, start=0.0, step=0.08, pose="rest", rows=1, dy=-70, ds=0.85):
    for r in range(rows - 1, -1, -1):
        for k in range(n):
            q = prog(t, start + (k + r * n) * step, 0.4)
            if q <= 0:
                continue
            xs = x0 + k * gap + (gap / 2 if r % 2 else 0)
            student(cr, k + r * 3, xs, y + r * dy, s * (ds ** r) * back_out(q), t, pose=pose)


def campus(cr, sky=(0.84, 0.90, 0.97)):
    bg(cr, sky, (0.96, 0.93, 0.86))
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(*GRASS); cr.fill()


def office(cr):
    bg(cr, (0.93, 0.90, 0.84), (0.88, 0.83, 0.74))
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(0.55, 0.42, 0.30); cr.fill()
    cr.rectangle(120, 160, 360, 260); cr.set_source_rgb(0.80, 0.88, 0.96); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.move_to(300, 160); cr.line_to(300, 420); cr.move_to(120, 290); cr.line_to(480, 290); cr.stroke()




# ================= EP14 PROPS AND PEOPLE
ALC_PURPLE = (0.33, 0.16, 0.46)   # Alcorn school colours (purple and gold); no logos or seals
REVELS_SKIN = (0.36, 0.24, 0.17)
EVERS_SKIN = (0.32, 0.21, 0.15)
WHITE_SKIN = (0.93, 0.80, 0.68)
GRAY_HAIR = (0.62, 0.60, 0.58)
CHAPEL_BRICK = (0.70, 0.34, 0.26)
SENATE_RED = (0.55, 0.12, 0.14)
GREEN_MONEY = (0.55, 0.72, 0.50)


def revels(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0, walking=False, book=False):
    """Hiram Revels: stylized man in a black frock suit with a full dark beard (no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t, suit=(0.10, 0.10, 0.12), tie=(0.85, 0.85, 0.85), skin=REVELS_SKIN, hair=HAIR_DK,
        pose=pose, pose_to=pose_to, pose_t=pose_t, walking=walking, beard=HAIR_DK,
        prop="ledger" if book else None)


def gov_alcorn(cr, x, y, s=1.0, t=0.0, pose="rest"):
    """Governor James L. Alcorn: stylized white man with a gray full beard (no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t, suit=(0.22, 0.20, 0.20), tie=(0.15, 0.15, 0.15), skin=WHITE_SKIN, hair=GRAY_HAIR,
        pose=pose, beard=GRAY_HAIR)


def evers(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0):
    """Medgar Evers: stylized man in a 1950s gray suit, short hair (no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t, suit=(0.36, 0.38, 0.42), tie=(0.12, 0.12, 0.16), skin=EVERS_SKIN, hair=HAIR_DK,
        pose=pose, pose_to=pose_to, pose_t=pose_t)


def senator(cr, k, x, y, s, t, pose="rest"):
    """Background 1870 senators (white men, varied suits, some beards)."""
    man(cr, x, y, s, t + k * 0.7, suit=[(0.20, 0.20, 0.22), (0.28, 0.22, 0.18), (0.18, 0.20, 0.26)][k % 3],
        tie=(0.1, 0.1, 0.1), skin=WHITE_SKIN, hair=[GRAY_HAIR, HAIR_DK, (0.45, 0.32, 0.20)][k % 3], pose=pose,
        beard=GRAY_HAIR if k % 3 == 0 else None)


def senate_room(cr):
    bg(cr, (0.94, 0.90, 0.82), (0.88, 0.82, 0.72))
    for k in range(5):                                       # tall windows
        x = 140 + k * 400
        rounded_rect(cr, x, 120, 180, 420, 90); cr.set_source_rgb(0.80, 0.88, 0.96); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(*SENATE_RED); cr.fill()


def desk(cr, x, y, w=260):
    cr.rectangle(x - w / 2, y - 120, w, 120); cr.set_source_rgb(*WOOD); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(x - w / 2 - 10, y - 132, w + 20, 18); cr.set_source_rgb(*WOOD_DK); cr.fill()


def chapel(cr, x, y, s=1.0, sign="OAKLAND COLLEGE", sign_col=(0.35, 0.33, 0.36), boarded=0.0):
    """Generic 1830s brick chapel with white columns and a cupola (stylized, not a portrait)."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-420, -420, 840, 420); cr.set_source_rgb(*CHAPEL_BRICK); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-470, -420); cr.line_to(0, -560); cr.line_to(470, -420); cr.close_path()
    cr.set_source_rgb(0.96, 0.95, 0.92); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-55, -680, 110, 130); cr.set_source_rgb(0.96, 0.95, 0.92); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-70, -680); cr.line_to(0, -760); cr.line_to(70, -680); cr.close_path()
    cr.set_source_rgb(0.35, 0.33, 0.36); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for c in range(6):                                       # white columns
        cx = -350 + c * 140
        cr.rectangle(cx - 22, -410, 44, 410); cr.set_source_rgb(0.97, 0.96, 0.93); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-60, -170, 120, 170); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    if boarded > 0:
        cr.set_source_rgba(*WOOD, boarded)
        for k, ang in enumerate((0.35, -0.35)):
            cr.save(); cr.translate(0, -90); cr.rotate(ang); cr.rectangle(-95, -14, 190, 28); cr.restore()
            cr.fill()
    cr.restore()
    if sign:
        cr.save(); cr.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(50 * s); w = cr.text_extents(sign).x_advance + 60 * s; cr.restore()
        panel(cr, x - w / 2, y - 500 * s - 30, w, 70 * s + 20, sign_col, r=14, lw=4)
        text(cr, sign, x, y - 500 * s + 22 * s + 2, 50 * s, (1, 1, 1))


def document(cr, x, y, s, p, title="MORRILL ACT", sub="LAND-GRANT FUNDS"):
    if p <= 0:
        return
    k = back_out(p)
    cr.save(); cr.translate(x, y); cr.scale(s * k, s * k); cr.rotate(-0.05)
    rounded_rect(cr, -170, -220, 340, 440, 12); cr.set_source_rgb(*PAPER); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    text(cr, title, 0, -140, 42, TEXT)
    text(cr, sub, 0, -95, 26, MAROON)
    for r in range(6):
        cr.move_to(-120, -40 + r * 40); cr.line_to(120, -40 + r * 40)
    cr.set_source_rgb(0.6, 0.6, 0.6); cr.set_line_width(3); cr.stroke()
    cr.arc(80, 170, 30, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill()
    cr.restore()


def money_bag(cr, x, y, r, p, label="$"):
    if p <= 0:
        return
    k = back_out(p)
    cr.save(); cr.translate(x, y); cr.scale(k, k)
    cr.arc(0, 0, r, 0, 2 * math.pi); cr.set_source_rgb(0.80, 0.70, 0.50); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-r * 0.35, -r * 0.9); cr.line_to(-r * 0.5, -r * 1.4); cr.line_to(r * 0.5, -r * 1.4); cr.line_to(r * 0.35, -r * 0.9)
    cr.close_path(); cr.set_source_rgb(0.80, 0.70, 0.50); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-r * 0.4, -r * 0.92); cr.line_to(r * 0.4, -r * 0.92); cr.set_source_rgb(*BROWN); cr.set_line_width(10); cr.stroke()
    text(cr, label, 0, r * 0.32, r * 0.9, (0.12, 0.30, 0.14))
    cr.restore()


def timeline(cr, t, items, y, x0=220, x1=1700, start=0.0):
    """items: list of (x_frac, year, label, t_show)."""
    pl = prog(t, start, 0.6)
    if pl <= 0:
        return
    cr.move_to(x0, y); cr.line_to(x0 + (x1 - x0) * ease(pl), y)
    cr.set_source_rgb(*INK); cr.set_line_width(10); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.stroke()
    for fx, year, label, ts in items:
        q = prog(t, ts, 0.4)
        if q <= 0:
            continue
        x = x0 + (x1 - x0) * fx
        cr.arc(x, y, 26 * back_out(q), 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
        text(cr, year, x, y - 60, 72, ALC_PURPLE, alpha=q)
        for j, line in enumerate(label.split("\n")):
            text(cr, line, x, y + 85 + j * 52, 44, TEXT, alpha=q)


# ================= SCENES
def s0(cr, t):  # hook: 1870, first Black U.S. senator, from Mississippi; a year later left Washington to lead a new HBCU
    i = 0; a, b = scene_bounds(i)
    ty = beat(i, "A year later")
    if t < ty:
        bg(cr, (0.84, 0.90, 0.97), (0.96, 0.93, 0.86))
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(*GRASS); cr.fill()
        capitol(cr, 1300, 900, 1.3)
        revels(cr, 470, 1060, 1.2, t, pose="rest", pose_to="open", pose_t=prog(t, beat(i, "Senate"), 0.5))
        pop_text(cr, "1870", 470, 200, 150, t, a + 0.15, color=ALC_PURPLE, outline=(1, 1, 1))
        pq = prog(t, beat(i, "first Black"), 0.4)
        if pq > 0:
            panel(cr, 820, 40, 960, 150, MAROON, r=24, alpha=pq)
            text(cr, "FIRST BLACK U.S. SENATOR", 1300, 135, 62, GOLDC, alpha=pq)
        pop_text(cr, "FROM MISSISSIPPI", 1300, 1010, 62, t, beat(i, "Mississippi"), color=TEXT, outline=(1, 1, 1))
    else:
        campus(cr)
        chapel(cr, 1350, 860, 0.85, sign="A NEW HBCU", sign_col=ALC_PURPLE)
        q = prog(t, ty, 2.2)
        revels(cr, 200 + 520 * ease(q), 1060, 1.05, t, walking=q < 1)
        pop_text(cr, "1871", 420, 200, 130, t, ty + 0.1, color=ALC_PURPLE, outline=(1, 1, 1))
        pop_text(cr, "LEAVES WASHINGTON", 420, 320, 54, t, beat(i, "Washington"), color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s1(cr, t):  # Hiram Revels, minister and teacher; oath Feb 25 1870 after opponents spent days trying to keep him out
    i = 1; a, b = scene_bounds(i)
    to = beat(i, "He took")
    if t < to:
        campus(cr, (0.92, 0.90, 0.86))
        revels(cr, 640, 1060, 1.3, t, pose="hold", book=True)
        name_tag(cr, "HIRAM REVELS", None, 640, 120, prog(t, beat(i, "Hiram"), 0.4), size=64)
        pop_text(cr, "MINISTER", 1350, 420, 90, t, beat(i, "minister"), color=ALC_PURPLE, outline=(1, 1, 1))
        pop_text(cr, "+ TEACHER", 1350, 560, 90, t, beat(i, "teacher"), color=TEXT, outline=(1, 1, 1))
    else:
        senate_room(cr)
        tp = beat(i, "after opponents")
        for k in range(3):
            q = prog(t, tp + k * 0.15, 0.4)
            if q > 0:
                senator(cr, k, 1100 + k * 230, 1060, 0.9 * back_out(q), t, pose="point" if k != 1 else "rest")
                if k != 1:
                    pop_text(cr, "NO!", 1100 + k * 230 + 110, 520, 64, t, tp + k * 0.15 + 0.2, color=RED, outline=(1, 1, 1))
        desk(cr, 480, 1060, 300)
        revels(cr, 480, 1060, 1.15, t, pose="rest", pose_to="hold", pose_t=prog(t, beat(i, "oath"), 0.5))
        pop_text(cr, "FEB. 25, 1870", 600, 160, 96, t, beat(i, "February"), color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "SWORN IN", 600, 270, 64, t, beat(i, "oath"), color=TEXT, outline=(1, 1, 1))
        stamp(cr, "DAYS OF DELAY", 1430, 200, prog(t, beat(i, "spent days"), 0.4), col=RED, size=66)
    sceneout(cr, t, a, b)


def s2(cr, t):  # Mississippi bought Oakland College (Presbyterian, closed by the Civil War); 1871 became Alcorn University for Black students; named for Gov. Alcorn
    i = 2; a, b = scene_bounds(i)
    tn = beat(i, "In eighteen seventy-one")
    tg = beat(i, "named for")
    campus(cr, (0.90, 0.90, 0.88) if t < tn else (0.84, 0.90, 0.97))
    if t < tn:
        chapel(cr, 960, 880, 0.95, sign="OAKLAND COLLEGE", boarded=prog(t, beat(i, "closed by"), 0.4))
        pop_text(cr, "PRESBYTERIAN SCHOOL", 960, 150, 66, t, beat(i, "Presbyterian"), color=TEXT, outline=(1, 1, 1))
        stamp(cr, "CLOSED BY THE CIVIL WAR", 960, 980, prog(t, beat(i, "closed by"), 0.4), col=RED, size=58)
        stamp(cr, "BOUGHT BY MISSISSIPPI", 1500, 330, prog(t, beat(i, "bought"), 0.4), col=ALC_PURPLE, size=50, rot=0.08)
    else:
        cx = 1250 if t >= tg else 960
        chapel(cr, cx, 880, 0.9, sign="ALCORN UNIVERSITY", sign_col=ALC_PURPLE)
        crowd(cr, t, 5, cx - 380, 190, 1060, 0.6, start=beat(i, "a college for"))
        pop_text(cr, "1871", cx, 150, 110, t, tn + 0.1, color=ALC_PURPLE, outline=(1, 1, 1))
        pg = prog(t, tg, 0.5)
        if pg > 0:
            gov_alcorn(cr, 470, 1060, 1.15 * back_out(pg), t)
            name_tag(cr, "GOV. JAMES L. ALCORN", None, 470, 170, pg, size=44)
    sceneout(cr, t, a, b)


def s3(cr, t):  # Senate term ended 1871; Revels became Alcorn's first president
    i = 3; a, b = scene_bounds(i)
    tr = beat(i, "Revels became")
    campus(cr)
    if t < tr:
        capitol(cr, 1350, 900, 1.0)
        q = prog(t, a + 0.2, 2.5)
        revels(cr, 1000 - 600 * ease(q), 1060, 1.1, t, walking=q < 1)
        stamp(cr, "TERM ENDS: 1871", 1350, 200, prog(t, beat(i, "term ended"), 0.4), col=MAROON, size=72)
    else:
        chapel(cr, 1250, 880, 0.9, sign="ALCORN UNIVERSITY", sign_col=ALC_PURPLE)
        revels(cr, 470, 1060, 1.25, t, pose="open")
        pf = prog(t, beat(i, "first president"), 0.4)
        if pf > 0:
            panel(cr, 90, 110, 760, 190, ALC_PURPLE, r=26, alpha=pf)
            text(cr, "FIRST PRESIDENT", 470, 195, 72, GOLDC, alpha=pf)
            text(cr, "Hiram Revels", 470, 265, 46, (1, 1, 1), alpha=pf)
    sceneout(cr, t, a, b)


def s4(cr, t):  # Bo: part nobody tells you; federal land-grant money (Morrill Act); oldest public Black land-grant; ~20 yrs before 1890
    i = 4; a, b = scene_bounds(i)
    tm = beat(i, "Mississippi gave")
    tt = beat(i, "That makes")
    tl = beat(i, "nearly twenty")
    if t < tm:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY TELLS YOU", W / 2, 140, 84, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    elif t < tt:
        campus(cr)
        chapel(cr, 1450, 880, 0.75, sign="ALCORN", sign_col=ALC_PURPLE)
        document(cr, 380, 520, 1.1, prog(t, beat(i, "Morrill"), 0.5))
        pa = prog(t, beat(i, "share of"), 0.9)
        if pa > 0:
            bx = 620 + 450 * ease(pa)
            money_bag(cr, bx, 560 - 120 * math.sin(math.pi * ease(pa)), 90, min(1, pa * 3))
        pop_text(cr, "FEDERAL LAND-GRANT MONEY", 960, 140, 70, t, beat(i, "land-grant"), color=ALC_PURPLE, outline=(1, 1, 1))
    elif t < tl:
        bg(cr)
        chapel(cr, 960, 1000, 0.62, sign=None)
        pp = prog(t, tt, 0.5)
        if pp > 0:
            panel(cr, 210, 70, 1500, 330, ALC_PURPLE, r=30, alpha=pp)
            text(cr, "OLDEST PUBLIC BLACK", 960, 200, 90, GOLDC, alpha=pp)
            text(cr, "LAND-GRANT COLLEGE", 960, 320, 90, (1, 1, 1), alpha=pp)
        pop_text(cr, "IN AMERICA", 960, 520, 64, t, beat(i, "in America"), color=TEXT, outline=(1, 1, 1))
    else:
        bg(cr)
        timeline(cr, t, [(0.1, "1871", "ALCORN", tl), (0.9, "1890", "MOST OF\nTHE OTHERS", beat(i, "eighteen ninety"))],
                 560, start=tl)
        pop_text(cr, "NEARLY 20 YEARS FIRST", 960, 180, 84, t, tl + 0.2, color=MAROON, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s5(cr, t):  # Alcorn A&M 1878, Alcorn State 1974; Medgar Evers studied there, NAACP's first Mississippi field secretary
    i = 5; a, b = scene_bounds(i)
    te = beat(i, "Medgar")
    if t < te:
        bg(cr)
        timeline(cr, t, [(0.0, "1871", "ALCORN\nUNIVERSITY", a), (0.5, "1878", "ALCORN A&M\nCOLLEGE", beat(i, "A and M")),
                         (1.0, "1974", "ALCORN STATE\nUNIVERSITY", beat(i, "nineteen seventy-four"))], 520, x0=300, x1=1620, start=a)
        pop_text(cr, "NEW NAMES", 960, 160, 84, t, a + 0.2, color=TEXT, outline=(1, 1, 1))
    else:
        campus(cr)
        chapel(cr, 1400, 880, 0.75, sign="ALCORN", sign_col=ALC_PURPLE)
        evers(cr, 560, 1060, 1.25, t, pose="rest", pose_to="point", pose_t=prog(t, beat(i, "first field"), 0.5))
        name_tag(cr, "MEDGAR EVERS", "Alcorn alumnus", 560, 110, prog(t, te, 0.4), size=60)
        pn = prog(t, beat(i, "N. A. A. C. P."), 0.4)
        if pn > 0:
            panel(cr, 960, 260, 860, 220, (1, 1, 1), r=26, alpha=pn)
            text(cr, "NAACP'S FIRST", 1390, 340, 62, MAROON, alpha=pn)
            text(cr, "MISSISSIPPI FIELD SECRETARY", 1390, 420, 48, TEXT, alpha=prog(t, beat(i, "field"), 0.4))
    sceneout(cr, t, a, b)


def s6(cr, t):  # CTA
    i = 6; a, b = scene_bounds(i)
    bg(cr)
    bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=False)
    text(cr, "Which HBCU first", 1250, 420, 74, TEXT, alpha=prog(t, a + 0.1, 0.4))
    text(cr, "should we cover next?", 1250, 515, 66, ALC_PURPLE, alpha=prog(t, a + 0.1, 0.4))
    pop_text(cr, "Tell us in the comments", 1250, 680, 56, t, beat(i, "Tell us"))
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    sceneout(cr, t, a, 1e9)


def thumb_hero(cr, x, y, r):
    """Hero object: the college hall with a purple ALCORN sign."""
    sc = r / 420
    chapel(cr, x, y + 330 * sc, sc, sign="ALCORN", sign_col=ALC_PURPLE)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
