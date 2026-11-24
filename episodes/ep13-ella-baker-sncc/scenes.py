"""Ep13 scenes: Ella Baker, Shaw University and the founding of SNCC (1960). One function per paragraph."""
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




# ================= EP13 PROPS AND PEOPLE
SHAW_GARNET = (0.50, 0.10, 0.16)   # Shaw school colours (garnet and white); no logos or seals
BAKER_SKIN = (0.36, 0.24, 0.17)
KING_SKIN = (0.30, 0.20, 0.14)
BAKER_DRESS = (0.20, 0.26, 0.40)
STU_SKINS = [BLACK, (0.34, 0.22, 0.15), (0.42, 0.28, 0.19), (0.26, 0.17, 0.12)]
STU_COATS = [CHAR, NAVY, (0.30, 0.22, 0.16), (0.18, 0.30, 0.26), (0.36, 0.16, 0.20)]
BUS = (0.86, 0.86, 0.84)


def baker(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0, walking=False, cap=False):
    """Ella Baker: stylized woman in a 1960 navy dress, short dark hair (no mouth)."""
    if s <= 0.01:
        return
    woman(cr, x, y, s, t, dress=BAKER_DRESS, skin=BAKER_SKIN, pose=pose, pose_to=pose_to, pose_t=pose_t,
          walking=walking, hair=HAIR_DK)
    hy = y + (-380 + (-abs(math.sin(t * 8)) * 5 if walking else math.sin(t * 2.0) * 2.5)) * s
    cr.save(); cr.translate(x, hy); cr.scale(s, s)           # short hair cap over the top of the head
    cr.arc(0, 0, 52, math.pi * 1.08, math.pi * 1.92); cr.set_source_rgb(*HAIR_DK); cr.set_line_width(18); cr.stroke()
    cr.restore()
    if cap:
        grad_cap(cr, x, hy, s)


def king(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0):
    """Dr. King: stylized man in a dark suit with a thin mustache (no mouth)."""
    if s <= 0.01:
        return
    man(cr, x, y, s, t, suit=(0.12, 0.12, 0.15), tie=(0.25, 0.25, 0.30), skin=KING_SKIN, hair=HAIR_DK,
        pose=pose, pose_to=pose_to, pose_t=pose_t)
    mustache(cr, x, head_y(y, s, t), s)


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


def shaw_hall(cr, x, y, s=1.0, label=True, banner=None, pb=0.0):
    """Generic red-brick college hall with a clock-less cupola (not a real building portrait)."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-520, -420, 1040, 420); cr.set_source_rgb(*BRICK); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-560, -420); cr.line_to(0, -560); cr.line_to(560, -420); cr.close_path()
    cr.set_source_rgb(0.35, 0.33, 0.36); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-50, -640, 100, 110); cr.set_source_rgb(0.96, 0.94, 0.88); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-65, -640); cr.line_to(0, -700); cr.line_to(65, -640); cr.close_path()
    cr.set_source_rgb(0.35, 0.33, 0.36); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for r in range(2):
        for c in range(7):
            if r == 1 and c == 3:
                continue
            cr.rectangle(-460 + c * 135, -370 + r * 170, 70, 110); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-70, -150, 140, 150); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()
    if label:
        panel(cr, x - 330 * s, y - 470 * s - 10, 660 * s, 70 * s + 20, SHAW_GARNET, r=14, lw=4)
        text(cr, "SHAW UNIVERSITY", x, y - 470 * s + 45 * s + 8, 52 * s, (1, 1, 1))
    if banner and pb > 0:
        panel(cr, x - 380, y - 330 * s, 760, 120, (1, 1, 1), r=18, lw=5, alpha=pb)
        text(cr, banner, x, y - 330 * s + 80, 54, SHAW_GARNET, alpha=pb)


def campus(cr, sky=(0.84, 0.90, 0.97)):
    bg(cr, sky, (0.96, 0.93, 0.86))
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(*GRASS); cr.fill()


def office(cr):
    bg(cr, (0.93, 0.90, 0.84), (0.88, 0.83, 0.74))
    cr.rectangle(0, 860, W, 220); cr.set_source_rgb(0.55, 0.42, 0.30); cr.fill()
    cr.rectangle(120, 160, 360, 260); cr.set_source_rgb(0.80, 0.88, 0.96); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.move_to(300, 160); cr.line_to(300, 420); cr.move_to(120, 290); cr.line_to(480, 290); cr.stroke()


def bus(cr, x, y, s=1.0, t=0.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    rounded_rect(cr, -420, -300, 840, 260, 40); cr.set_source_rgb(*BUS); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.rectangle(-420, -150, 840, 30); cr.set_source_rgb(0.20, 0.34, 0.60); cr.fill()
    for k in range(6):
        cr.rectangle(-380 + k * 125, -270, 100, 90); cr.set_source_rgb(0.70, 0.84, 0.95); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
        hx, hy = -330 + k * 125, -205 + math.sin(t * 3 + k) * 3   # a rider in each window
        cr.save(); cr.rectangle(-380 + k * 125, -270, 100, 90); cr.clip()
        cr.arc(hx, hy, 30, 0, 2 * math.pi); cr.set_source_rgb(*STU_SKINS[k % 4]); cr.fill()
        cr.arc(hx, hy - 14, 30, math.pi * 1.1, math.pi * 1.9); cr.set_source_rgb(*HAIR_DK); cr.set_line_width(10); cr.stroke()
        for dx in (-10, 10):
            cr.arc(hx + dx, hy - 2, 6, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
            cr.arc(hx + dx + 1, hy - 1, 2.8, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
        cr.restore()
    for wx in (-260, 260):
        cr.arc(wx, -40, 62, 0, 2 * math.pi); cr.set_source_rgb(0.12, 0.12, 0.12); cr.fill()
        cr.arc(wx, -40, 26, 0, 2 * math.pi); cr.set_source_rgb(0.7, 0.7, 0.7); cr.fill()
    cr.restore()


def clipboard(cr, x, y, s=1.0, p=1.0):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(s * back_out(p), s * back_out(p)); cr.rotate(0.06)
    rounded_rect(cr, -150, -200, 300, 400, 18); cr.set_source_rgb(*WOOD); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(-120, -160, 240, 340); cr.set_source_rgb(1, 1, 1); cr.fill()
    rounded_rect(cr, -55, -220, 110, 50, 10); cr.set_source_rgb(0.6, 0.6, 0.62); cr.fill()
    text(cr, "VOTER", 0, -95, 44, TEXT); text(cr, "REGISTRATION", 0, -50, 30, TEXT)
    for k in range(4):
        cr.move_to(-95, 10 + k * 42); cr.line_to(95, 10 + k * 42)
    cr.set_source_rgb(0.6, 0.6, 0.6); cr.set_line_width(3); cr.stroke()
    cr.restore()


def hamburger(cr, x, y, r):
    cr.save(); cr.translate(x, y)
    cr.arc(0, -r * 0.15, r, math.pi, 2 * math.pi); cr.close_path(); cr.set_source_rgb(0.85, 0.58, 0.28); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(max(3, r * 0.05)); cr.stroke()
    for sx, sy in ((-0.4, -0.6), (0.1, -0.75), (0.45, -0.5), (-0.1, -0.4)):
        cr.save(); cr.translate(sx * r, sy * r); cr.scale(1, 0.5); cr.arc(0, 0, r * 0.06, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(0.98, 0.94, 0.80); cr.fill()
    rounded_rect(cr, -r * 1.05, -r * 0.12, r * 2.1, r * 0.14, r * 0.07); cr.set_source_rgb(0.40, 0.68, 0.30); cr.fill()
    rounded_rect(cr, -r, r * 0.02, r * 2, r * 0.26, r * 0.12); cr.set_source_rgb(0.42, 0.24, 0.14); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-r, r * 0.30); cr.line_to(r, r * 0.30); cr.line_to(r * 0.95, r * 0.55); cr.line_to(-r * 0.95, r * 0.55)
    cr.close_path(); cr.set_source_rgb(0.85, 0.58, 0.28); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


# ================= SCENES
def s0(cr, t):  # hook: 1960, an HBCU in Raleigh; one woman helps students keep their movement their own; Dr. King hoped otherwise
    i = 0; a, b = scene_bounds(i)
    campus(cr)
    shaw_hall(cr, 960, 860, 0.85, label=False)
    crowd(cr, t, 6, 640, 150, 1060, 0.62, start=a + 0.4, rows=2)
    baker(cr, 300, 1060, 1.0, t, pose="rest", pose_to="open", pose_t=prog(t, beat(i, "keep their"), 0.5))
    tk = beat(i, "Doctor King")
    pk = prog(t, tk, 0.5)
    if pk > 0:
        king(cr, 1700, 1060, 0.95 * back_out(pk), t, pose="open")
        pop_text(cr, "KING'S PLAN", 1700, 520, 50, t, beat(i, "into his"), color=TEXT, outline=(1, 1, 1))
    pop_text(cr, "1960", 360, 200, 150, t, a + 0.2, color=SHAW_GARNET, outline=(1, 1, 1))
    pop_text(cr, "RALEIGH, N.C.", 360, 300, 56, t, beat(i, "Raleigh"), color=TEXT, outline=(1, 1, 1))
    pop_text(cr, "THEIR MOVEMENT", 1060, 170, 90, t, beat(i, "keep their"), color=SHAW_GARNET, outline=(1, 1, 1))
    pop_text(cr, "THEIR OWN", 1060, 280, 70, t, beat(i, "own"), color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s1(cr, t):  # her name: Ella Baker; 1927 graduated from Shaw University, top of her class
    i = 1; a, b = scene_bounds(i)
    campus(cr)
    shaw_hall(cr, 1200, 880, 0.9)
    tg = beat(i, "she graduated")
    baker(cr, 480, 1060, 1.25, t, pose="rest" if t < tg else "open", cap=t >= tg)
    name_tag(cr, "ELLA BAKER", None, 480, 140, prog(t, beat(i, "Ella"), 0.4), size=64)
    pop_text(cr, "CLASS OF 1927", 1200, 150, 84, t, beat(i, "nineteen twenty-seven"), color=SHAW_GARNET, outline=(1, 1, 1))
    stamp(cr, "TOP OF HER CLASS", 1200, 1000, prog(t, beat(i, "top of"), 0.4), col=GOLDC, size=62, rot=-0.06)
    sceneout(cr, t, a, b)


def s2(cr, t):  # Feb 1960 Greensboro lunch counter; sit-ins spread; Baker working for Dr. King's group; a movement born
    i = 2; a, b = scene_bounds(i)
    tb = beat(i, "Baker was")
    if t < tb:
        store_wall(cr, t)
        counter(cr, t)
        for k in range(4):
            q = prog(t, a + 0.2 + k * 0.15, 0.4)
            if q > 0:
                man(cr, 420 + k * 370, 1075, 1.3 * back_out(q), t + k * 0.5, suit=COATS[k % 4], tie=MAROON,
                    skin=STU_SKINS[k], hair=HAIR_DK)
            mug(cr, 420 + k * 370 + 165, 772, 1.3)
        pop_text(cr, "FEB. 1960", 480, 170, 100, t, beat(i, "February"), color=AT_BLUE, outline=(1, 1, 1))
        pop_text(cr, "GREENSBORO", 480, 290, 70, t, beat(i, "Greensboro"), color=TEXT, outline=(1, 1, 1))
        ps = prog(t, beat(i, "sit-ins spread"), 0.4)
        if ps > 0:
            stamp(cr, "SIT-INS SPREAD", 1400, 250, ps, col=RED_S, size=72)
            text(cr, "across the South", 1400, 380, 50, TEXT, alpha=prog(t, beat(i, "across"), 0.4))
    else:
        office(cr)
        baker(cr, 760, 1060, 1.15, t, pose="rest", pose_to="hold", pose_t=prog(t, beat(i, "she saw"), 0.5))
        king(cr, 1450, 1060, 1.1, t, pose="rest")
        name_tag(cr, "DR. KING'S GROUP", "Southern Christian Leadership Conf.", 1450, 120, prog(t, beat(i, "King's"), 0.4), size=50)
        name_tag(cr, "ELLA BAKER", "on staff", 760, 170, prog(t, tb, 0.4), size=44)
        pop_text(cr, "A MOVEMENT IS BORN", 1100, 450, 66, t, beat(i, "movement being"), color=SHAW_GARNET, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s3(cr, t):  # about $800; invited sit-in leaders to Shaw, Easter weekend, April 15-17
    i = 3; a, b = scene_bounds(i)
    tv = beat(i, "then invited")
    if t < tv:
        office(cr)
        baker(cr, 520, 1060, 1.2, t, pose="hold")
        money(cr, 1250, 520, "$800", prog(t, beat(i, "eight hundred"), 0.5), w=560, h=250)
        pop_text(cr, "ABOUT", 1250, 300, 64, t, beat(i, "about"), color=TEXT, outline=(1, 1, 1))
    else:
        campus(cr)
        shaw_hall(cr, 1150, 860, 0.85, banner="WELCOME, SIT-IN LEADERS", pb=prog(t, beat(i, "sit-in leaders"), 0.4))
        baker(cr, 330, 1060, 1.0, t, pose="open")
        for k in range(6):
            q = prog(t, tv + 0.2 + k * 0.25, 2.2)
            if q > 0:
                student(cr, k, 2050 - (1290 - k * 170) * ease(q), 1060, 0.7, t, walking=q < 1)
        pe = prog(t, beat(i, "Easter"), 0.4)
        if pe > 0:
            panel(cr, 560, 30, 800, 120, GOLDC, r=22, alpha=pe)
            text(cr, "EASTER WEEKEND", 960, 115, 66, INK, alpha=pe)
        pop_text(cr, "APRIL 15-17, 1960", 960, 230, 70, t, beat(i, "April"), color=SHAW_GARNET, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s4(cr, t):  # Bo: part nobody tells you; King hoped for a youth branch; Baker urged independence
    i = 4; a, b = scene_bounds(i)
    tk = beat(i, "Doctor King")
    if t < tk:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY TELLS YOU", W / 2, 140, 84, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    else:
        campus(cr, (0.90, 0.92, 0.96))
        king(cr, 330, 1060, 1.05, t, pose="open")
        pk = prog(t, beat(i, "youth branch"), 0.4)
        if pk > 0:
            panel(cr, 90, 150, 520, 170, (1, 1, 1), r=26, alpha=pk)
            text(cr, "KING'S HOPE:", 350, 215, 40, TEXT, alpha=pk)
            text(cr, "A YOUTH BRANCH", 350, 285, 52, AT_BLUE, alpha=pk)
        tb = beat(i, "Baker urged")
        baker(cr, 960, 1060, 1.05, t, pose="rest", pose_to="point", pose_t=prog(t, tb, 0.5))
        crowd(cr, t, 4, 1260, 170, 1060, 0.7, start=tk + 0.3)
        name_tag(cr, "ELLA BAKER", None, 960, 460, prog(t, tb, 0.4), size=40)
        pop_text(cr, "STAY INDEPENDENT", 1300, 190, 80, t, beat(i, "independent"), color=SHAW_GARNET, outline=(1, 1, 1))
        pop_text(cr, "RUN IT YOURSELVES", 1300, 300, 60, t, beat(i, "run their"), color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s5(cr, t):  # they formed SNCC; Freedom Rides 1961; Mississippi voter registration, Freedom Summer 1964
    i = 5; a, b = scene_bounds(i)
    tf = beat(i, "It joined")
    tm = beat(i, "and it helped")
    if t < tf:
        campus(cr)
        crowd(cr, t, 8, 220, 210, 1060, 0.72, start=a, rows=2, pose="open")
        baker(cr, 1780, 1060, 0.85, t, pose="open")
        pf = prog(t, beat(i, "formed"), 0.45)
        if pf > 0:
            panel(cr, 260, 70, 1400, 300, SHAW_GARNET, r=30, alpha=pf)
            text(cr, "SNCC", 960, 200, 120, GOLDC, alpha=pf)
            text(cr, "Student Nonviolent Coordinating Committee", 960, 300, 50, (1, 1, 1),
                 alpha=prog(t, beat(i, "Student Nonviolent"), 0.4))
        pop_text(cr, "THEY DID.", 960, 520, 70, t, a + 0.1, color=TEXT, outline=(1, 1, 1))
    elif t < tm:
        bg(cr, (0.86, 0.92, 0.98), (0.96, 0.93, 0.86))
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.40, 0.40, 0.42); cr.fill()
        cr.rectangle(0, 970, W, 14); cr.set_source_rgb(0.95, 0.85, 0.30); cr.fill()
        q = prog(t, tf, 2.4)
        bus(cr, 2200 - 1300 * ease(q), 940, 1.0, t)
        pop_text(cr, "FREEDOM RIDES", 960, 170, 100, t, beat(i, "Freedom Rides"), color=AT_BLUE, outline=(1, 1, 1))
        pop_text(cr, "1961", 960, 290, 80, t, beat(i, "sixty-one"), color=SHAW_GARNET, outline=(1, 1, 1))
    else:
        street(cr)
        for k in range(5):
            student(cr, k + 1, 230 + k * 190, 1060, 0.78, t)
        clipboard(cr, 1450, 560, 1.0, prog(t, beat(i, "voter registration"), 0.4))
        pop_text(cr, "MISSISSIPPI", 700, 170, 90, t, beat(i, "Mississippi"), color=TEXT, outline=(1, 1, 1))
        ps = prog(t, beat(i, "Freedom Summer"), 0.4)
        if ps > 0:
            panel(cr, 1120, 860, 680, 150, GOLDC, r=24, alpha=ps)
            text(cr, "FREEDOM SUMMER 1964", 1460, 960, 52, INK, alpha=ps)
    sceneout(cr, t, a, b)


def s6(cr, t):  # "bigger than a hamburger"; CTA
    i = 6; a, b = scene_bounds(i)
    tq = beat(i, "Which")
    if t < tq:
        bg(cr)
        baker(cr, 420, 1060, 1.2, t, pose="open")
        hamburger(cr, 1250, 640, 150 * back_out(prog(t, beat(i, "hamburger") - 0.6, 0.5)) + 0.01)
        pop_text(cr, "BIGGER THAN", 1250, 230, 110, t, beat(i, "bigger"), color=SHAW_GARNET, outline=(1, 1, 1))
        pop_text(cr, "A HAMBURGER", 1250, 360, 90, t, beat(i, "hamburger"), color=TEXT, outline=(1, 1, 1))
        text(cr, "Ella Baker, 1960", 1250, 900, 44, TEXT, alpha=prog(t, a + 0.3, 0.4))
    else:
        bg(cr)
        bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=False)
        text(cr, "Which HBCU leader", 1250, 420, 70, TEXT, alpha=prog(t, tq, 0.4))
        text(cr, "should we cover next?", 1250, 510, 66, MAROON, alpha=prog(t, tq, 0.4))
        pop_text(cr, "Tell us in the comments", 1250, 680, 56, t, beat(i, "Tell us"))
        k = max(0, (t - (b - 0.8)) / 0.8)
        if k > 0:
            cr.set_source_rgba(*BG, k); cr.paint()
        sceneout(cr, t, a, 1e9)
        return
    sceneout(cr, t, a, b)


def thumb_hero(cr, x, y, r):
    """Hero object: a hamburger ("bigger than a hamburger")."""
    hamburger(cr, x, y + r * 0.1, r * 0.85)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
