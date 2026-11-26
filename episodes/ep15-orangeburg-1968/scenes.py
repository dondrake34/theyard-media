"""Ep15 scenes: the Orangeburg Massacre at South Carolina State (Feb 8, 1968). One function per paragraph."""
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





WHITE_SKIN = (0.93, 0.80, 0.68)
ALC_PURPLE = (0.50, 0.10, 0.16)  # timeline year colour (garnet here)

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




# ================= EP15 PROPS AND PEOPLE
GARNET = (0.50, 0.10, 0.16)       # SC State colours (garnet and blue); no logos or seals
SCS_BLUE = (0.10, 0.24, 0.52)
NIGHT_TOP = (0.06, 0.08, 0.16)
NIGHT_BOT = (0.14, 0.15, 0.24)
KHAKI = (0.55, 0.50, 0.36)
HELMET = (0.30, 0.30, 0.30)
WHITE = (1, 1, 1)
CANDLE = (0.97, 0.95, 0.88)
FLAME = (1.0, 0.70, 0.20)
HAMMOND_SKIN = (0.30, 0.20, 0.14)
SMITH_SKIN = (0.38, 0.25, 0.17)
MIDDLETON_SKIN = (0.26, 0.17, 0.12)
SELLERS_SKIN = (0.34, 0.22, 0.15)


def night(cr, grass=True):
    bg(cr, NIGHT_TOP, NIGHT_BOT)
    rnd = random.Random(7)
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 520)
        cr.arc(x, y, rnd.uniform(1.5, 3.2), 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.55); cr.fill()
    if grass:
        cr.rectangle(0, 860, W, 220); cr.set_source_rgb(0.12, 0.20, 0.14); cr.fill()


def patrolman(cr, k, x, y, s, t, pose="rest"):
    """1968 state highway patrolman: khaki uniform, helmet (no weapon drawn, no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t + k * 0.5, suit=KHAKI, tie=(0.20, 0.20, 0.20), skin=WHITE_SKIN, hair=HAIR_DK, pose=pose)
    hy = head_y(y, s, t + k * 0.5)
    cr.save(); cr.translate(x, hy); cr.scale(s, s)
    cr.arc(0, -8, 54, math.pi, 2 * math.pi); cr.close_path(); cr.set_source_rgb(*HELMET); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(-66, -12, 132, 12); cr.set_source_rgb(*HELMET); cr.fill()
    cr.restore()


def patrol_line(cr, t, n, x0, gap, y, s, start=0.0, step=0.06):
    for k in range(n):
        q = prog(t, start + k * step, 0.4)
        if q > 0:
            patrolman(cr, k, x0 + k * gap, y, s * back_out(q), t)


def flashes(cr, t, start, x0, x1, y, dur=1.6):
    """Abstract gunfire: brief white streaks and a screen flash. No wounds shown."""
    if t < start or t > start + dur:
        return
    rnd = random.Random(int((t - start) * 12))
    for _ in range(7):
        x = rnd.uniform(x0, x1); yy = y + rnd.uniform(-60, 60)
        cr.move_to(x, yy); cr.line_to(x - rnd.uniform(220, 420), yy + rnd.uniform(-20, 20))
        cr.set_source_rgba(1, 0.95, 0.75, 0.85); cr.set_line_width(5); cr.stroke()
    k = 1 - (t - start) / dur
    cr.set_source_rgba(1, 1, 1, 0.22 * k * (0.5 + 0.5 * math.sin((t - start) * 40))); cr.paint()


def bonfire(cr, x, y, s, t, alpha=1.0):
    if alpha <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.save(); cr.scale(1, 0.3); cr.arc(0, 0, 420, 0, 2 * math.pi); cr.restore()
    g = cairo.RadialGradient(0, -120, 20, 0, -120, 520)
    g.add_color_stop_rgba(0, 1, 0.75, 0.3, 0.45 * alpha); g.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
    cr.set_source(g); cr.paint()
    for ang in (-0.35, 0.35):
        cr.save(); cr.rotate(ang); cr.rectangle(-150, -22, 300, 44); cr.restore()
        cr.set_source_rgba(*WOOD_DK, alpha); cr.fill()
    for j, col in enumerate(((1.0, 0.45, 0.10), (1.0, 0.70, 0.20), (1.0, 0.92, 0.55))):
        f = 1 + 0.08 * math.sin(t * 9 + j)
        hh = (230 - j * 60) * f; ww = 120 - j * 30
        cr.move_to(-ww, -10); cr.curve_to(-ww, -hh * 0.5, -20, -hh * 0.7, 0, -hh)
        cr.curve_to(20, -hh * 0.7, ww, -hh * 0.5, ww, -10); cr.close_path()
        cr.set_source_rgba(*col, alpha); cr.fill()
    cr.restore()


def candle(cr, x, y, s, t, p=1.0):
    if p <= 0:
        return
    k = back_out(p)
    cr.save(); cr.translate(x, y); cr.scale(s * k, s * k)
    g = cairo.RadialGradient(0, -170, 5, 0, -170, 120)
    g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.5); g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
    cr.set_source(g); cr.arc(0, -170, 120, 0, 2 * math.pi); cr.fill()
    rounded_rect(cr, -26, -130, 52, 130, 8); cr.set_source_rgb(*CANDLE); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    f = 1 + 0.1 * math.sin(t * 11)
    cr.move_to(0, -132); cr.curve_to(-16, -150, -6, -175 * f, 0, -190 * f); cr.curve_to(6, -175 * f, 16, -150, 0, -132)
    cr.set_source_rgb(*FLAME); cr.fill()
    cr.restore()


def young_man(cr, x, y, s, t, skin, coat, pose="rest", pose_to=None, pose_t=0.0, walking=False):
    """1968 student: sweater/jacket, short hair (no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t, suit=coat, tie=(0.92, 0.92, 0.92), skin=skin, hair=HAIR_DK, pose=pose,
        pose_to=pose_to, pose_t=pose_t, walking=walking)


def hammond(cr, x, y, s, t, **kw):
    young_man(cr, x, y, s, t, HAMMOND_SKIN, GARNET, **kw)


def smith(cr, x, y, s, t, **kw):
    young_man(cr, x, y, s, t + 0.6, SMITH_SKIN, SCS_BLUE, **kw)


def middleton(cr, x, y, s, t, **kw):
    young_man(cr, x, y, s, t + 1.2, MIDDLETON_SKIN, (0.24, 0.36, 0.30), **kw)


def sellers(cr, x, y, s, t, **kw):
    """Cleveland Sellers: stylized man in a denim jacket, short hair and thin mustache (no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t, suit=(0.24, 0.32, 0.46), tie=(0.24, 0.32, 0.46), skin=SELLERS_SKIN, hair=HAIR_DK, **kw)
    mustache(cr, x, head_y(y, s, t), s)


def hodges(cr, x, y, s, t, **kw):
    """Gov. Jim Hodges (2001): stylized white man in a dark suit, glasses (no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t, suit=(0.16, 0.18, 0.24), tie=MAROON, skin=WHITE_SKIN, hair=(0.40, 0.30, 0.20), **kw)
    glasses(cr, x, head_y(y, s, t), s)


def protest_sign(cr, x, y, s, label, rot=0.0):
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(s, s)
    cr.rectangle(-6, 0, 12, 170); cr.set_source_rgb(*WOOD_DK); cr.fill()
    rounded_rect(cr, -120, -110, 240, 120, 10); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    lines = label.split("\n")
    for j, ln in enumerate(lines):
        text(cr, ln, 0, -50 + (j - (len(lines) - 1) / 2) * 44 + 14, 38, GARNET)
    cr.restore()


def bowling_alley(cr, x, y, s=1.0, sign_alpha=1.0):
    """Generic 1960s strip-mall bowling alley (stylized, not a portrait of the real building)."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-560, -360, 1120, 360); cr.set_source_rgb(0.86, 0.82, 0.74); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(-580, -390, 1160, 40); cr.set_source_rgb(0.30, 0.42, 0.56); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for dx in (-380, 380):                       # windows
        cr.rectangle(dx - 130, -280, 260, 170); cr.set_source_rgb(0.70, 0.82, 0.92); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-90, -250, 180, 250); cr.set_source_rgb(0.45, 0.30, 0.20); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    # pin on the roof
    cr.save(); cr.translate(0, -520)
    cr.move_to(0, -120); cr.curve_to(40, -120, 40, -60, 22, -40); cr.curve_to(60, 0, 50, 90, 30, 120)
    cr.line_to(-30, 120); cr.curve_to(-50, 90, -60, 0, -22, -40); cr.curve_to(-40, -60, -40, -120, 0, -120)
    cr.set_source_rgb(1, 1, 1); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(-26, -50, 52, 10); cr.rectangle(-30, -32, 60, 10); cr.set_source_rgb(0.80, 0.15, 0.15); cr.fill()
    cr.restore()
    cr.restore()
    if sign_alpha > 0:
        panel(cr, x - 400 * s, y - 470 * s, 800 * s, 90 * s, (0.80, 0.15, 0.15), r=14, lw=4, alpha=sign_alpha)
        text(cr, "ALL STAR BOWLING LANES", x, y - 470 * s + 64 * s, 50 * s, WHITE, alpha=sign_alpha)


def courtroom(cr):
    bg(cr, (0.90, 0.86, 0.78), (0.84, 0.78, 0.68))
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(0.45, 0.32, 0.22); cr.fill()
    cr.rectangle(0, 560, W, 30); cr.set_source_rgb(*WOOD_DK); cr.fill()


def jail_bars(cr, x, y, w, h, p):
    if p <= 0:
        return
    cr.set_source_rgba(0.25, 0.25, 0.28, p)
    n = 6
    for k in range(n + 1):
        cr.rectangle(x + k * w / n - 7, y, 14, h * ease(p)); cr.fill()
    cr.rectangle(x - 7, y, w + 14, 16); cr.fill()


def podium(cr, x, y):
    cr.move_to(x - 120, y); cr.line_to(x - 90, y - 230); cr.line_to(x + 90, y - 230); cr.line_to(x + 120, y); cr.close_path()
    cr.set_source_rgb(*WOOD); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(x - 110, y - 250, 220, 24); cr.set_source_rgb(*WOOD_DK); cr.fill()


def three(cr, t, y, s, start, xs=(420, 960, 1500), poses=("rest", "rest", "rest"), step=0.5):
    fns = (hammond, smith, middleton)
    for j in range(3):
        q = prog(t, start[j] if isinstance(start, (list, tuple)) else start + j * step, 0.5)
        if q > 0:
            fns[j](cr, xs[j], y, s * back_out(q), t, pose=poses[j])


# ================= SCENES
def s0(cr, t):  # hook: Feb 8 1968, patrolmen opened fire on unarmed students at an HBCU in SC; three young men never went home
    i = 0; a, b = scene_bounds(i)
    tf = beat(i, "opened fire")
    t3 = beat(i, "Three young")
    if t < t3:
        night(cr)
        crowd(cr, t, 4, 170, 200, 1040, 0.62, start=a + 0.2, rows=2)
        patrol_line(cr, t, 4, 1240, 170, 1040, 0.62, start=beat(i, "state highway"))
        flashes(cr, t, tf, 1180, 1700, 700)
        pop_text(cr, "FEB. 8, 1968", 960, 170, 130, t, a + 0.15, color=GOLDC, outline=INK)
        pop_text(cr, "ORANGEBURG, S.C.", 960, 290, 64, t, beat(i, "South Carolina"), color=WHITE, outline=INK)
        pop_text(cr, "UNARMED STUDENTS", 450, 420, 56, t, beat(i, "unarmed"), color=WHITE, outline=INK)
    else:
        night(cr, grass=False)
        for j, x in enumerate((560, 960, 1360)):
            candle(cr, x, 900, 1.25, t + j, prog(t, t3 + j * 0.25, 0.5))
        pq = prog(t, beat(i, "never went"), 0.5)
        text(cr, "3 YOUNG MEN", 960, 260, 120, WHITE, alpha=prog(t, t3, 0.4))
        text(cr, "NEVER WENT HOME", 960, 380, 80, GOLDC, alpha=pq)
    sceneout(cr, t, a, b)


def s1(cr, t):  # bowling alley turned Black customers away; SC State + Claflin students protested; some arrested
    i = 1; a, b = scene_bounds(i)
    ts = beat(i, "Students from")
    campus(cr, (0.84, 0.90, 0.97))
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(0.62, 0.62, 0.60); cr.fill()
    if t < ts:
        bowling_alley(cr, 960, 880, 1.0, sign_alpha=prog(t, beat(i, "All Star"), 0.4))
        pop_text(cr, "ORANGEBURG, 1968", 960, 120, 76, t, beat(i, "Orangeburg"), color=TEXT, outline=WHITE)
        stamp(cr, "WHITES ONLY", 960, 760, prog(t, beat(i, "turned"), 0.4), col=RED, size=70)
    else:
        bowling_alley(cr, 1380, 880, 0.75)
        for k, (lab, rot) in enumerate((("EQUAL\nRIGHTS", -0.06), ("OPEN\nTO ALL", 0.05), ("END JIM\nCROW", -0.03))):
            q = prog(t, beat(i, "protest") + k * 0.2, 0.4)
            if q > 0:
                protest_sign(cr, 180 + k * 220, 560, 0.9 * back_out(q), lab, rot)
        crowd(cr, t, 4, 180, 220, 1050, 0.66, start=ts)
        pq = prog(t, ts, 0.4)
        if pq > 0:
            panel(cr, 60, 60, 900, 150, GARNET, r=24, alpha=pq)
            text(cr, "SC STATE + CLAFLIN", 510, 138, 60, GOLDC, alpha=pq)
            text(cr, "STUDENTS", 510, 192, 40, WHITE, alpha=pq)
        stamp(cr, "ARRESTS", 1380, 260, prog(t, beat(i, "arrested"), 0.4), col=RED, size=80)
    sceneout(cr, t, a, b)


def s2(cr, t):  # two nights later: bonfire on campus; officers came to put it out; then patrolmen fired into the crowd
    i = 2; a, b = scene_bounds(i)
    to = beat(i, "Officers")
    tf = beat(i, "fired")
    night(cr)
    bonfire(cr, 820, 900, 0.9, t, alpha=prog(t, beat(i, "bonfire"), 0.6))
    crowd(cr, t, 4, 160, 190, 1050, 0.6, start=beat(i, "students gathered"), rows=2)
    if t >= to:
        q = prog(t, to, 1.4)
        patrol_line(cr, t, 5, 1260 + 200 * (1 - ease(q)), 140, 1050, 0.6, start=to)
    flashes(cr, t, tf, 1200, 1800, 680)
    pop_text(cr, "TWO NIGHTS LATER", 960, 140, 92, t, a + 0.15, color=GOLDC, outline=INK)
    pop_text(cr, "SC STATE CAMPUS", 960, 250, 56, t, beat(i, "South Carolina State"), color=WHITE, outline=INK)
    if t >= tf:
        stamp(cr, "PATROLMEN FIRED", 960, 420, prog(t, tf, 0.4), col=(0.95, 0.30, 0.25), size=80)
    sceneout(cr, t, a, b)


def s3(cr, t):  # Hammond and Smith, SC State students; Delano Middleton, high school student, mother worked on campus; Hammond shot in back; ~30 wounded
    i = 3; a, b = scene_bounds(i)
    tm = beat(i, "Delano")
    tb = beat(i, "Hammond was")
    tw = beat(i, "Nearly thirty")
    if t < tw:
        bg(cr, (0.92, 0.89, 0.84), (0.86, 0.82, 0.76))
        three(cr, t, 1070, 1.35, [a + 0.1, beat(i, "Henry"), tm])
        for x, s1_, s2_, ts in ((420, "SAMUEL HAMMOND", "SC State student", a + 0.2),
                                (960, "HENRY SMITH", "SC State student", beat(i, "Henry")),
                                (1500, "DELANO MIDDLETON", "high school student", tm)):
            name_tag(cr, s1_, s2_, x, 90, prog(t, ts, 0.4), size=44)
        pop_text(cr, "MOTHER WORKED ON CAMPUS", 1500, 330, 34, t, beat(i, "whose mother"), color=TEXT, outline=WHITE)
        if t >= tb:
            pq = prog(t, tb, 0.4)
            panel(cr, 220, 370, 400, 80, MAROON, r=16, alpha=pq)
            text(cr, "SHOT IN THE BACK", 420, 424, 40, WHITE, alpha=pq)
    else:
        bg(cr, (0.92, 0.89, 0.84), (0.86, 0.82, 0.76))
        rows = 3; n = 10
        for r in range(rows):
            for k in range(n):
                q = prog(t, tw + (r * n + k) * 0.02, 0.3)
                if q > 0 and r * n + k < 28:
                    cx = 260 + k * 156 + (78 if r % 2 else 0); cy = 520 + r * 150
                    cr.arc(cx, cy, 40 * back_out(q), 0, 2 * math.pi); cr.set_source_rgb(*GARNET); cr.fill()
                    cr.arc(cx, cy - 70 * back_out(q), 22 * back_out(q), 0, 2 * math.pi); cr.fill()
        pop_text(cr, "NEARLY 30 WOUNDED", 960, 220, 110, t, tw, color=MAROON, outline=WHITE)
    sceneout(cr, t, a, b)


def s4(cr, t):  # Bo: part nobody tells you; 9 patrolmen charged in federal court, acquitted; only person imprisoned: Cleveland Sellers (wounded), inciting a riot; pardoned 1993
    i = 4; a, b = scene_bounds(i)
    tn = beat(i, "Nine patrolmen")
    ts = beat(i, "The only person")
    tp = beat(i, "The state pardoned")
    if t < tn:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY TELLS YOU", W / 2, 140, 84, t, a + 0.15, color=MAROON, outline=WHITE)
    elif t < ts:
        courtroom(cr)
        for k in range(9):
            q = prog(t, tn + k * 0.06, 0.4)
            if q > 0:
                patrolman(cr, k, 180 + k * 195, 1070 - (k % 2) * 50, 0.8 * back_out(q), t)
        pop_text(cr, "9 PATROLMEN CHARGED", 960, 130, 84, t, tn + 0.1, color=TEXT, outline=WHITE)
        pop_text(cr, "FEDERAL COURT", 960, 230, 56, t, beat(i, "federal"), color=MAROON, outline=WHITE)
        stamp(cr, "ACQUITTED", 960, 430, prog(t, beat(i, "acquitted"), 0.4), col=RED, size=96)
    else:
        courtroom(cr)
        sellers(cr, 520, 1070, 1.4, t, pose="rest")
        jail_bars(cr, 280, 300, 480, 780, prog(t, beat(i, "prison"), 0.5) * (1 - prog(t, tp, 0.6)))
        name_tag(cr, "CLEVELAND SELLERS", "activist, wounded that night", 520, 90, prog(t, beat(i, "Cleveland"), 0.4), size=48)
        pop_text(cr, "ONLY ONE SENT TO PRISON", 1360, 360, 58, t, ts + 0.1, color=TEXT, outline=WHITE)
        stamp(cr, "INCITING A RIOT", 1360, 500, prog(t, beat(i, "convicted"), 0.4), col=RED, size=66)
        if t >= tp:
            pq = prog(t, tp, 0.4)
            panel(cr, 1010, 700, 700, 170, (0.18, 0.45, 0.26), r=24, alpha=pq)
            text(cr, "PARDONED", 1360, 780, 74, WHITE, alpha=pq)
            text(cr, "1993", 1360, 845, 52, GOLDC, alpha=prog(t, beat(i, "nineteen ninety"), 0.4))
    sceneout(cr, t, a, b)


def s5(cr, t):  # 2001 Gov. Jim Hodges apologized for SC; two years before Kent State; few know these names
    i = 5; a, b = scene_bounds(i)
    tk = beat(i, "It happened")
    tf = beat(i, "yet few")
    if t < tk:
        bg(cr, (0.90, 0.92, 0.96), (0.84, 0.86, 0.92))
        hodges(cr, 560, 1060, 1.3, t, pose="open")
        podium(cr, 560, 1070)
        name_tag(cr, "GOV. JIM HODGES", None, 560, 90, prog(t, beat(i, "Governor"), 0.4), size=56)
        pop_text(cr, "2001", 1360, 330, 140, t, a + 0.15, color=SCS_BLUE, outline=WHITE)
        pq = prog(t, beat(i, "apologized"), 0.4)
        if pq > 0:
            panel(cr, 940, 430, 840, 170, SCS_BLUE, r=24, alpha=pq)
            text(cr, "STATE APOLOGY", 1360, 510, 72, WHITE, alpha=pq)
            text(cr, "South Carolina", 1360, 570, 44, GOLDC, alpha=pq)
    else:
        bg(cr)
        timeline(cr, t, [(0.1, "1968", "ORANGEBURG", tk), (0.9, "1970", "KENT STATE", beat(i, "Kent"))], 480, start=tk)
        pop_text(cr, "2 YEARS EARLIER", 960, 170, 90, t, beat(i, "two years"), color=MAROON, outline=WHITE)
        pq = prog(t, tf, 0.5)
        if pq > 0:
            panel(cr, 380, 760, 1160, 150, GARNET, r=24, alpha=pq)
            text(cr, "FEW KNOW THESE NAMES", 960, 860, 72, WHITE, alpha=pq)
    sceneout(cr, t, a, b)


def s6(cr, t):  # say their names; CTA
    i = 6; a, b = scene_bounds(i)
    tq = beat(i, "Which")
    if t < tq:
        night(cr, grass=False)
        for j, (x, nm, ts) in enumerate(((420, "SAMUEL HAMMOND", beat(i, "Samuel")), (960, "HENRY SMITH", beat(i, "Henry")),
                                         (1500, "DELANO MIDDLETON", beat(i, "Delano")))):
            candle(cr, x, 880, 1.2, t + j, prog(t, ts, 0.5))
            text(cr, nm, x, 990, 50, WHITE, alpha=prog(t, ts, 0.4))
        text(cr, "SAY THEIR NAMES", 960, 230, 110, GOLDC, alpha=prog(t, a + 0.1, 0.4))
    else:
        bg(cr)
        bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, tq + 0.8, 0.5), talk=False)
        text(cr, "Which HBCU story", 1250, 420, 74, TEXT, alpha=prog(t, tq, 0.4))
        text(cr, "should we tell next?", 1250, 515, 66, GARNET, alpha=prog(t, tq, 0.4))
        pop_text(cr, "Tell us in the comments", 1250, 680, 56, t, tq + 0.6)
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    sceneout(cr, t, a, 1e9)


def thumb_hero(cr, x, y, r):
    """Hero object: a memorial candle."""
    candle(cr, x, y + r * 0.6, r / 150, 0.0, 1.0)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
