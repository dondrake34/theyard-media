"""Ep09 scenes: Thurgood Marshall (Lincoln University, Howard Law, Charles Hamilton Houston, Murray v. Pearson, Brown, Supreme Court). One function per paragraph."""
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


# ---------------- ep09 props (no logos or seals; school names as text only)
TM_SKIN = (0.40, 0.27, 0.18)       # Marshall: medium brown
HOU_SKIN = (0.36, 0.24, 0.16)      # Houston
MUR_SKIN = (0.30, 0.20, 0.13)      # Donald Murray
HAIR_DK = (0.10, 0.08, 0.07)
LINCOLN_ORANGE = (0.90, 0.45, 0.10)
LINCOLN_BLUE = (0.10, 0.20, 0.45)
HOWARD_BLUE = (0.05, 0.16, 0.38)
HOWARD_RED = (0.78, 0.10, 0.16)
STONE = (0.93, 0.92, 0.88)
ROBE = (0.06, 0.06, 0.07)
WOOD2 = (0.50, 0.33, 0.20)


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


def marshall(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0, cap=False, robe=False,
             walking=False, prop=None):
    """Thurgood Marshall: stylized tall man, gray suit, thin mustache (no mouth)."""
    suit = ROBE if robe else (0.30, 0.32, 0.38)
    man(cr, x, y, s, t, suit=suit, tie=(0.70, 0.12, 0.16) if not robe else (0.95, 0.95, 0.95), skin=TM_SKIN,
        hair=HAIR_DK, pose=pose, pose_to=pose_to, pose_t=pose_t, walking=walking, prop=prop)
    hy = head_y(y, s, t) if not walking else y + (-385 - abs(math.sin(t * 8)) * 5) * s
    mustache(cr, x, hy, s)
    if cap:
        grad_cap(cr, x, hy, s)
    if robe:  # long judicial robe flaring to the floor
        cr.save(); cr.translate(x, y); cr.scale(s, s)
        cr.move_to(-60, -320); cr.line_to(-95, -6); cr.line_to(95, -6); cr.line_to(60, -320); cr.close_path()
        cr.set_source_rgba(*ROBE, 0.92); cr.fill()
        cr.restore()


def houston(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0):
    """Charles Hamilton Houston: stylized man, dark suit, round glasses, mustache (no mouth)."""
    man(cr, x, y, s, t, suit=(0.14, 0.14, 0.18), tie=GOLDC, skin=HOU_SKIN, hair=HAIR_DK,
        pose=pose, pose_to=pose_to, pose_t=pose_t)
    hy = head_y(y, s, t)
    glasses(cr, x, hy, s)
    mustache(cr, x, hy, s, w=18)


def murray(cr, x, y, s=1.0, t=0.0, pose="rest", walking=False):
    """Donald Murray: stylized young man, brown suit (no mouth)."""
    man(cr, x, y, s, t, suit=(0.36, 0.26, 0.18), tie=(0.15, 0.30, 0.55), skin=MUR_SKIN, hair=HAIR_DK,
        pose=pose, walking=walking)


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
        for st in range(3):  # Baltimore white marble steps
            cr.rectangle(x + 100 - st * 10, 880 - (st + 1) * 14, 80 + st * 20, 14)
            cr.set_source_rgb(0.97, 0.97, 0.95); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(2); cr.stroke()
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.70, 0.68, 0.64); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


def street(cr, sky=(0.84, 0.90, 0.97)):
    bg(cr, sky, (0.96, 0.93, 0.86))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.72, 0.70, 0.66); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


def columned(cr, x, y, w, h, color=STONE, ncol=6, label=None, label_col=TEXT, pediment=True):
    """Classical columned building (law school / court). label is plain text on the frieze."""
    cr.save()
    cr.rectangle(x - w / 2 - 30, y - 30, w + 60, 30); cr.set_source_rgb(*color); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(x - w / 2, y - h, w, h - 30); cr.set_source_rgb(*[c * 0.92 for c in color]); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.stroke()
    cw = w / (ncol * 2 - 1)
    for k in range(ncol):
        cx = x - w / 2 + k * 2 * cw
        cr.rectangle(cx, y - h + 70, cw, h - 100); cr.set_source_rgb(*color); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(x - w / 2 - 20, y - h, w + 40, 70); cr.set_source_rgb(*color); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    if pediment:
        cr.move_to(x - w / 2 - 30, y - h); cr.line_to(x, y - h - 120); cr.line_to(x + w / 2 + 30, y - h); cr.close_path()
        cr.set_source_rgb(*color); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()
    if label:
        text(cr, label, x, y - h + 50, 36, label_col)


def gavel(cr, x, y, s=1.0, rot=-0.5):
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(s, s)
    rounded_rect(cr, -14, -20, 28, 260, 12); cr.set_source_rgb(*WOOD2); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    rounded_rect(cr, -110, -90, 220, 90, 26); cr.set_source_rgb(*WOOD2); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.stroke()
    for dx in (-70, 70):
        cr.rectangle(dx - 8, -90, 16, 90); cr.set_source_rgb(*GOLDC); cr.fill()
    cr.restore()


def diploma(cr, x, y, s=1.0, p=1.0):
    if p <= 0:
        return
    k = back_out(p)
    cr.save(); cr.translate(x, y); cr.scale(s * k, s * k); cr.rotate(-0.25)
    rounded_rect(cr, -110, -26, 220, 52, 26); cr.set_source_rgb(*PAPER); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(-12, -28, 24, 56); cr.set_source_rgb(*RED); cr.fill()
    cr.restore()


def courtroom(cr):
    bg(cr, (0.90, 0.86, 0.80), (0.84, 0.78, 0.70))
    for k in range(0, W, 240):  # wood panelling
        cr.rectangle(k + 20, 200, 200, 560); cr.set_source_rgba(*WOOD2, 0.25); cr.fill()
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.55, 0.40, 0.28); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


def counsel_table(cr, x, y, w=900):
    rounded_rect(cr, x - w / 2, y - 200, w, 36, 8); cr.set_source_rgb(*WOOD2); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(x - w / 2 + 30, y - 164, 26, 164); cr.rectangle(x + w / 2 - 56, y - 164, 26, 164)
    cr.set_source_rgb(*WOOD2); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()


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


# ================= SCENES
def s0(cr, t):  # hook: hometown law school refused Black students; Marshall -> HBCU -> beat them in court
    i = 0; a, b = scene_bounds(i)
    street(cr)
    tm = beat(i, "So Thurgood")
    tc = beat(i, "came back")
    if t < tm:
        bo(cr, 330, 1040, 0.5, t, pose="think" if t < beat(i, "wouldn't") else "shrug",
           wide=0.9 if t > beat(i, "wouldn't") else 0.2, brow=0.8, talk=False)
        pb = prog(t, a + 0.2, 0.45)
        cr.save(); cr.translate(1240, 880); s_ = back_out(pb); cr.scale(s_, s_); cr.translate(-1240, -880)
        columned(cr, 1240, 880, 720, 470, label="LAW SCHOOL")
        cr.restore()
        pop_text(cr, "HIS HOMETOWN LAW SCHOOL", 1240, 150, 64, t, a + 0.3, color=TEXT, outline=(1, 1, 1))
        stamp(cr, "NO BLACK STUDENTS", 1240, 640, prog(t, beat(i, "wouldn't"), 0.4), col=RED, size=70)
    elif t < tc:
        street(cr, (0.88, 0.92, 0.98))
        pm = prog(t, tm, 0.45)
        marshall(cr, 640, 1050, 1.25 * back_out(pm), t, pose="hold", prop="ledger")
        name_tag(cr, "Thurgood Marshall", None, 640, 110, prog(t, beat(i, "Thurgood"), 0.4), size=54)
        pop_text(cr, "WENT TO AN HBCU", 1350, 450, 96, t, beat(i, "H. B. C. U."), color=MAROON, outline=(1, 1, 1))
    else:
        courtroom(cr)
        marshall(cr, 600, 1050, 1.2, t, pose="point")
        gavel(cr, 1350, 640, 1.2 * back_out(prog(t, tc, 0.45)), rot=-0.5 + 0.4 * math.sin(clamp((t - tc) * 3) * math.pi))
        pop_text(cr, "...AND BEAT THEM IN COURT", 1240, 180, 74, t, tc, color=MAROON, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s1(cr, t):  # grew up in Baltimore; 1930 graduated Lincoln University (PA), founded before the Civil War (1854)
    i = 1; a, b = scene_bounds(i)
    t30 = beat(i, "In nineteen")
    if t < t30:
        row_houses(cr)
        marshall(cr, 760, 1050, 1.15 * back_out(prog(t, a + 0.15, 0.45)), t, pose="rest")
        name_tag(cr, "Thurgood Marshall", "grew up in Baltimore", 760, 110, prog(t, a + 0.3, 0.4), size=50)
        pop_text(cr, "BALTIMORE", 1500, 260, 90, t, beat(i, "Baltimore"), color=MAROON, outline=(1, 1, 1))
    else:
        street(cr, (0.96, 0.88, 0.76))
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(*GRASS); cr.fill()
        building(cr, 1380, 880, 760, 250, (0.80, 0.62, 0.46), cols=4)
        tg = beat(i, "graduated")
        marshall(cr, 560, 1050, 1.2, t, pose="hold" if t > tg else "rest", cap=t > tg)
        if t > tg:
            diploma(cr, 560 + 140 * 1.2, 1050 - 330 * 1.2, 1.0, prog(t, tg, 0.4))
        pop_text(cr, "1930", 560, 160, 130, t, beat(i, "nineteen"), color=MAROON, outline=(1, 1, 1))
        pl = prog(t, beat(i, "Lincoln"), 0.4)
        if pl > 0:
            panel(cr, 960, 170, 840, 200, LINCOLN_BLUE, r=26, alpha=pl)
            text(cr, "LINCOLN UNIVERSITY", 1380, 265, 70, LINCOLN_ORANGE, alpha=pl)
            text(cr, "PENNSYLVANIA · an HBCU", 1380, 335, 42, (1, 1, 1), alpha=pl)
        pf = prog(t, beat(i, "founded"), 0.4)
        if pf > 0:
            stamp(cr, "FOUNDED 1854", 1380, 435, pf, col=MAROON, size=58)
            text(cr, "before the Civil War", 1380, 505, 40, TEXT, alpha=pf, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s2(cr, t):  # University of Maryland law school closed to Black students -> Howard law school in Washington
    i = 2; a, b = scene_bounds(i)
    th = beat(i, "So he went")
    street(cr)
    if t < th:
        columned(cr, 1220, 880, 820, 500, label="UNIV. OF MARYLAND LAW")
        marshall(cr, 420, 1050, 1.1, t, pose="rest")
        stamp(cr, "CLOSED TO BLACK STUDENTS", 1220, 620, prog(t, beat(i, "closed"), 0.4), col=RED, size=58)
        pop_text(cr, "CLOSE TO HOME", 1220, 140, 70, t, beat(i, "close to home"), color=TEXT, outline=(1, 1, 1))
    else:
        pw = prog(t, th, 1.2)
        building(cr, 1300, 880, 760, 330, (0.86, 0.80, 0.70), cols=4)
        marshall(cr, 300 + 380 * ease(pw), 1050, 1.1, t, pose="hold", prop="ledger", walking=pw < 1)
        ph = prog(t, beat(i, "Howard"), 0.4)
        if ph > 0:
            panel(cr, 900, 150, 800, 200, HOWARD_BLUE, r=26, alpha=ph)
            text(cr, "HOWARD UNIVERSITY", 1300, 240, 66, (1, 1, 1), alpha=ph)
            text(cr, "SCHOOL OF LAW", 1300, 315, 46, HOWARD_RED if False else GOLDC, alpha=ph)
        pop_text(cr, "WASHINGTON, D.C.", 1300, 980, 56, t, beat(i, "Washington"), color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s3(cr, t):  # mentor: dean Charles Hamilton Houston; law to change society; 1933 first in class
    i = 3; a, b = scene_bounds(i)
    bg(cr, (0.93, 0.93, 0.90), (0.86, 0.86, 0.82))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.72, 0.62, 0.48); cr.fill()
    t33 = beat(i, "In nineteen")
    if t < t33:
        ph = prog(t, a + 0.15, 0.45)
        houston(cr, 520, 1050, 1.2 * back_out(ph), t, pose="point" if t > beat(i, "Houston taught") else "rest")
        name_tag(cr, "Charles Hamilton Houston", "Dean, Howard Law", 520, 110, prog(t, beat(i, "Charles"), 0.4), size=46)
        marshall(cr, 1580, 1050, 1.05, t, pose="hold", prop="ledger")
        text(cr, "MARSHALL", 1580, 560, 40, TEXT, outline=(1, 1, 1), alpha=prog(t, a + 0.4, 0.4))
        pt = prog(t, beat(i, "Houston taught"), 0.4)
        if pt > 0:
            chalk = (0.16, 0.30, 0.24)
            panel(cr, 820, 260, 560, 300, chalk, r=10, lw=8, alpha=pt)
            text(cr, "THE LAW", 1100, 370, 64, (0.95, 0.95, 0.90), alpha=pt)
            text(cr, "↓", 1100, 440, 56, GOLDC, alpha=pt)
            text(cr, "CHANGE SOCIETY", 1100, 515, 56, (0.95, 0.95, 0.90), alpha=prog(t, beat(i, "change"), 0.4))
    else:
        marshall(cr, 760, 1050, 1.3, t, pose="hold", cap=True)
        diploma(cr, 760 + 140 * 1.3, 1050 - 330 * 1.3, 1.1, prog(t, t33, 0.4))
        pop_text(cr, "1933", 1400, 280, 150, t, beat(i, "nineteen"), color=MAROON, outline=(1, 1, 1))
        pf = prog(t, beat(i, "first"), 0.4)
        if pf > 0:
            stamp(cr, "#1 IN HIS CLASS", 1400, 560, pf, col=HOWARD_BLUE, size=72)
    sceneout(cr, t, a, b)


def s4(cr, t):  # Bo: part nobody hears; 1935 sued that same Maryland law school for Donald Murray; won, admitted
    i = 4; a, b = scene_bounds(i)
    t35 = beat(i, "In nineteen")
    tw = beat(i, "They won")
    if t < t35:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY HEARS", W / 2, 140, 90, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    elif t < tw:
        courtroom(cr)
        pop_text(cr, "1935", 1640, 170, 120, t, beat(i, "nineteen"), color=MAROON, outline=(1, 1, 1))
        marshall(cr, 420, 1050, 1.05, t, pose="point")
        houston(cr, 760, 1050, 1.0, t, pose="rest")
        text(cr, "MARSHALL", 420, 560, 36, TEXT, outline=(1, 1, 1))
        text(cr, "HOUSTON", 760, 590, 36, TEXT, outline=(1, 1, 1))
        pm = prog(t, beat(i, "Donald"), 0.45)
        if pm > 0:
            murray(cr, 1320, 1050, 1.0 * back_out(pm), t)
            name_tag(cr, "Donald Murray", "student", 1320, 420, pm, size=44)
        counsel_table(cr, 870, 1060, 1500)
        pc = prog(t, beat(i, "took that same"), 0.4) * (1 - prog(t, beat(i, "Donald") - 0.2, 0.3))
        if pc > 0:
            panel(cr, 980, 240, 820, 130, (1, 1, 1), r=20, alpha=pc)
            text(cr, "VS. UNIV. OF MARYLAND LAW", 1390, 325, 48, TEXT, alpha=pc)
    else:
        street(cr)
        columned(cr, 1400, 880, 760, 500, label="UNIV. OF MARYLAND LAW")
        pa = prog(t, beat(i, "Murray was"), 1.4)
        murray(cr, 260 + 780 * ease(pa), 1050, 1.0, t, walking=0 < pa < 1)
        stamp(cr, "THEY WON", 560, 230, prog(t, tw, 0.4), col=(0.15, 0.50, 0.25), size=90)
        pop_text(cr, "MURRAY ADMITTED", 560, 400, 66, t, beat(i, "admitted"), color=MAROON, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s5(cr, t):  # 1954 Brown v. Board; segregated public schools unconstitutional; 1967 first Black justice
    i = 5; a, b = scene_bounds(i)
    t67 = beat(i, "In nineteen sixty")
    bg(cr, (0.84, 0.90, 0.98), (0.95, 0.93, 0.88))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.80, 0.78, 0.74); cr.fill()
    columned(cr, 1300, 880, 900, 560, ncol=8, label="SUPREME COURT")
    if t < t67:
        marshall(cr, 470, 1050, 1.2, t, pose="open" if t > beat(i, "Supreme") else "point")
        pop_text(cr, "1954", 470, 150, 130, t, beat(i, "nineteen"), color=MAROON, outline=(1, 1, 1))
        pb = prog(t, beat(i, "Brown"), 0.4)
        if pb > 0:
            panel(cr, 880, 120, 840, 140, MAROON, r=24, alpha=pb)
            text(cr, "BROWN v. BOARD OF EDUCATION", 1300, 212, 50, GOLDC, alpha=pb)
        ps = prog(t, beat(i, "segregated"), 0.4)
        if ps > 0:
            panel(cr, 880, 560, 840, 200, (1, 1, 1), r=24, alpha=ps)
            text(cr, "SEGREGATED PUBLIC SCHOOLS:", 1300, 640, 44, TEXT, alpha=ps)
            stamp(cr, "UNCONSTITUTIONAL", 1300, 720, prog(t, beat(i, "unconstitutional"), 0.4), col=RED, size=58, rot=-0.03)
    else:
        marshall(cr, 1300, 1050, 1.25 * back_out(prog(t, t67, 0.45)), t, pose="open", robe=True)
        pop_text(cr, "1967", 420, 200, 150, t, beat(i, "sixty"), color=MAROON, outline=(1, 1, 1))
        pf = prog(t, beat(i, "first Black"), 0.4)
        if pf > 0:
            panel(cr, 90, 360, 680, 300, MAROON, r=26, alpha=pf)
            text(cr, "FIRST BLACK", 430, 460, 66, GOLDC, alpha=pf)
            text(cr, "JUSTICE", 430, 545, 66, GOLDC, alpha=pf)
            text(cr, "U.S. Supreme Court", 430, 615, 40, (1, 1, 1), alpha=pf)
    sceneout(cr, t, a, b)


def s6(cr, t):  # outro: Bo hosts
    i = 6; a, b = scene_bounds(i)
    bg(cr)
    bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=False)
    pop_text(cr, "LINCOLN → HOWARD", 1250, 200, 90, t, beat(i, "Howard"), color=MAROON, outline=GOLDC)
    pop_text(cr, "→ SUPREME COURT", 1250, 310, 90, t, beat(i, "highest"), color=MAROON, outline=GOLDC)
    text(cr, "Which HBCU legend", 1250, 470, 70, TEXT, alpha=prog(t, beat(i, "Which"), 0.4))
    text(cr, "should we cover next?", 1250, 560, 66, MAROON, alpha=prog(t, beat(i, "Which"), 0.4))
    pop_text(cr, "Tell us in the comments", 1250, 720, 56, t, beat(i, "Tell us"))
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    sceneout(cr, t, a, 1e9)


def thumb_hero(cr, x, y, r):
    """Hero object: a judge's gavel."""
    gavel(cr, x + r * 0.1, y + r * 0.2, r / 200.0, rot=-0.6)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
