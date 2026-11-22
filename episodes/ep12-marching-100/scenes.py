"""Ep12 scenes: William P. Foster and the FAMU Marching 100. One function per paragraph."""
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

def church(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-170, -260, 340, 260); cr.set_source_rgb(0.95, 0.93, 0.88); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-190, -260); cr.line_to(0, -380); cr.line_to(190, -260); cr.close_path()
    cr.set_source_rgb(*MAROON); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-40, -500, 80, 140); cr.set_source_rgb(0.95, 0.93, 0.88); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-55, -500); cr.line_to(0, -580); cr.line_to(55, -500); cr.close_path()
    cr.set_source_rgb(*MAROON); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(0, -640); cr.line_to(0, -585); cr.move_to(-18, -620); cr.line_to(18, -620)
    cr.set_line_width(6); cr.stroke()
    for wx in (-110, 110):
        cr.move_to(wx - 26, -110); cr.line_to(wx - 26, -180); cr.curve_to(wx - 26, -215, wx + 26, -215, wx + 26, -180)
        cr.line_to(wx + 26, -110); cr.close_path(); cr.set_source_rgb(0.98, 0.88, 0.60); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-36, -140, 72, 140); cr.set_source_rgb(*WOOD_DK); cr.fill()
    cr.restore()



def lawn(cr, sky=(0.86, 0.92, 0.98)):
    bg(cr, sky, (0.96, 0.93, 0.86))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(*GRASS); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


# ---------------- ep12 people and props (no logos, seals or team marks; school names as text only)
FAMU_ORANGE = (0.93, 0.47, 0.13)
FAMU_GREEN = (0.05, 0.42, 0.24)
KU_BLUE = (0.20, 0.30, 0.55)
FOSTER_SKIN = (0.34, 0.22, 0.15)
BAND_SKINS = [(0.36, 0.24, 0.16), (0.26, 0.17, 0.11), (0.46, 0.32, 0.22), (0.32, 0.21, 0.14), (0.40, 0.27, 0.18)]
BRASS = (0.93, 0.76, 0.28)
WHITE_SKINS = [(0.93, 0.80, 0.68), (0.90, 0.76, 0.62), (0.95, 0.84, 0.72)]
FR_BLUE = (0.10, 0.25, 0.60)
FR_RED = (0.85, 0.16, 0.20)


def foster(cr, x, y, s=1.0, t=0.0, pose="rest", baton=False, older=False, walking=False, clarinet=False):
    """William P. Foster: stylized man in a dark suit (no mouth). older = gray hair + glasses."""
    if s <= 0.01:
        return
    hair = GRAY if older else HAIR_DK
    man(cr, x, y, s, t, suit=(0.14, 0.14, 0.18), tie=FAMU_ORANGE if older else MAROON, skin=FOSTER_SKIN,
        hair=hair, pose=pose, walking=walking)
    hy = head_y(y, s, t) if not walking else y + (-385 - abs(math.sin(t * 8)) * 5) * s
    if older:
        glasses(cr, x, hy, s)
    if baton and pose in ("point", "hold"):
        hx, hyy = (175, -360) if pose == "point" else (140, -330)
        wob = math.sin(t * 6) * 0.25
        cr.save(); cr.translate(x + hx * s, y + hyy * s); cr.rotate(-0.9 + wob)
        cr.move_to(0, 0); cr.line_to(0, -110 * s); cr.set_source_rgb(1, 1, 1); cr.set_line_width(8 * s)
        cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.stroke(); cr.restore()
    if clarinet:
        cr.save(); cr.translate(x + 10 * s, y - 250 * s); cr.rotate(0.15)
        cr.rectangle(-8 * s, -60 * s, 16 * s, 190 * s); cr.set_source_rgb(0.08, 0.08, 0.08); cr.fill()
        cr.move_to(-8 * s, 130 * s); cr.line_to(-22 * s, 160 * s); cr.line_to(22 * s, 160 * s); cr.line_to(8 * s, 130 * s)
        cr.close_path(); cr.fill(); cr.restore()


def bandsman(cr, x, y, s, t, k=0, uni=FAMU_GREEN, trim=FAMU_ORANGE, skin=None, step=True, inst="horn", plume=True,
             phase=0.0):
    """Marching band member: shako + plume, uniform, instrument, high-step legs (no mouth)."""
    if s <= 0.01:
        return
    skin = skin or BAND_SKINS[k % len(BAND_SKINS)]
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.save(); cr.scale(1, 0.12); cr.arc(0, 30, 90, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgba(0, 0, 0, 0.12); cr.fill()
    ph = t * 4.2 + phase + k * 0.0
    lift = max(0, math.sin(ph * math.pi)) if step else 0
    lift2 = max(0, -math.sin(ph * math.pi)) if step else 0
    bob = -6 * (lift + lift2)
    cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for dx, l in ((-20, lift), (20, lift2)):
        knee = (dx + 40 * l, -95 - 60 * l + bob)
        foot = (dx + 10 * l, -8 - 60 * l)
        for w, c in ((32, INK), (24, uni)):
            cr.move_to(dx, -170 + bob); cr.line_to(*knee); cr.line_to(*foot)
            cr.set_line_width(w); cr.set_source_rgb(*c); cr.stroke()
        cr.save(); cr.translate(foot[0] + 8, foot[1]); cr.scale(1, 0.5); cr.arc(0, 0, 21, math.pi, 2 * math.pi); cr.restore()
        cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.move_to(-54, -325 + bob); cr.line_to(54, -325 + bob); cr.line_to(50, -160 + bob); cr.line_to(-50, -160 + bob)
    cr.close_path(); cr.set_source_rgb(*uni); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for yy in (-290, -250, -210):
        cr.move_to(-30, yy + bob); cr.line_to(30, yy + bob); cr.set_source_rgb(*trim); cr.set_line_width(8); cr.stroke()
    cr.move_to(-50, -335 + bob); cr.line_to(50, -175 + bob); cr.set_source_rgb(*trim); cr.set_line_width(14); cr.stroke()
    hy = -380 + bob
    cr.rectangle(-13, -345 + bob, 26, 22); cr.set_source_rgb(*skin); cr.fill()
    cr.arc(0, hy, 44, 0, 2 * math.pi); cr.set_source_rgb(*skin); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-38, hy - 118, 76, 86); cr.set_source_rgb(*uni); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(-44, hy - 38, 88, 12); cr.set_source_rgb(*INK); cr.fill()
    cr.rectangle(-38, hy - 70, 76, 10); cr.set_source_rgb(*trim); cr.fill()
    if plume:
        sw = math.sin(t * 5 + k) * 6
        cr.move_to(0, hy - 118); cr.curve_to(-20 + sw, hy - 150, -10 + sw, hy - 200, 6 + sw, hy - 215)
        cr.curve_to(18 + sw, hy - 190, 14, hy - 150, 0, hy - 118); cr.set_source_rgb(*(trim if uni != FAMU_GREEN else (1, 1, 1)))
        cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(2.5); cr.stroke()
    for dx in (-15, 15):
        cr.arc(dx, hy - 4, 7.5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
        cr.arc(dx + 1, hy - 3, 3.4, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
    if inst == "horn":
        cr.move_to(20, hy + 34); cr.line_to(120, hy + 20); cr.set_source_rgb(*BRASS); cr.set_line_width(12); cr.stroke()
        cr.move_to(110, hy - 10); cr.line_to(160, hy - 28); cr.line_to(160, hy + 70); cr.line_to(110, hy + 50); cr.close_path()
        cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.arc(30, hy + 70, 14, 0, 2 * math.pi); cr.set_source_rgb(*skin); cr.fill()
    elif inst == "drum":
        cr.save(); cr.translate(0, -215 + bob); cr.scale(1, 0.45); cr.arc(0, 0, 62, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(0.95, 0.95, 0.95); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.rectangle(-62, -215 + bob, 124, 70); cr.set_source_rgb(*trim); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
        hit = abs(math.sin(t * 8.4 + k))
        for dx in (-30, 30):
            cr.move_to(dx, -240 + bob - 40 * hit); cr.line_to(dx * 0.3, -222 + bob)
            cr.set_source_rgb(0.95, 0.90, 0.80); cr.set_line_width(7); cr.stroke()
    elif inst == "clarinet":
        cr.move_to(0, hy + 30); cr.line_to(20, hy + 170); cr.set_source_rgb(0.08, 0.08, 0.08); cr.set_line_width(14); cr.stroke()
    cr.restore()


def band_block(cr, x0, y0, cols, rows, s, t, dx=110, dy=48, uni=FAMU_GREEN, trim=FAMU_ORANGE, n=None, p=1.0,
               skins=None, step=True):
    """Rows drawn back to front so nearer rows overlap farther ones."""
    count = 0
    total = n if n is not None else cols * rows
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if idx >= total:
                continue
            pk = clamp(p * total - idx) if p < 1 else 1
            if pk <= 0:
                continue
            k = idx
            inst = "drum" if r == rows - 1 and rows > 1 else ("clarinet" if c % 4 == 1 else "horn")
            sk = skins[k % len(skins)] if skins else None
            sc = s * (0.8 + 0.2 * (r + 1) / rows)
            bandsman(cr, x0 + c * dx + (r % 2) * dx * 0.5, y0 + r * dy, sc * back_out(pk), t, k=k, uni=uni, trim=trim,
                     skin=sk, inst=inst, step=step, phase=(c % 2) * 0.5)
            count += 1
    return count


def eiffel(cr, x, y, s=1.0, col=(0.45, 0.35, 0.30)):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-230, 0); cr.curve_to(-120, -220, -60, -480, -22, -760); cr.line_to(22, -760)
    cr.curve_to(60, -480, 120, -220, 230, 0); cr.line_to(150, 0); cr.curve_to(80, -110, -80, -110, -150, 0); cr.close_path()
    cr.set_source_rgb(*col); cr.fill()
    for yy, w in ((-300, 130), (-520, 70)):
        cr.rectangle(-w, yy, 2 * w, 20); cr.fill()
    cr.move_to(0, -760); cr.line_to(0, -840); cr.set_line_width(8); cr.stroke()
    cr.restore()


def tricolor(cr, x, y, w, h, t, p=1.0):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(back_out(p), back_out(p))
    cr.move_to(0, 0); cr.line_to(0, h * 2.2); cr.set_source_rgb(*INK); cr.set_line_width(8); cr.stroke()
    for k, c in enumerate((FR_BLUE, (1, 1, 1), FR_RED)):
        for j in range(8):
            xx = k * w / 3 + j * w / 24
            wv = math.sin(t * 4 + xx * 0.02) * 8
            cr.rectangle(xx, wv, w / 24 + 1, h); cr.set_source_rgb(*c); cr.fill()
    cr.restore()


def us_flag(cr, x, y, w, h, t, p=1.0):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(back_out(p), back_out(p))
    cr.move_to(0, 0); cr.line_to(0, h * 2.2); cr.set_source_rgb(*INK); cr.set_line_width(8); cr.stroke()
    for j in range(24):
        xx = j * w / 24; wv = math.sin(t * 4 + xx * 0.02) * 8
        for r in range(7):
            cr.rectangle(xx, wv + r * h / 7, w / 24 + 1, h / 7 / 2 + 0.5); cr.set_source_rgb(0.78, 0.12, 0.16); cr.fill()
            cr.rectangle(xx, wv + r * h / 7 + h / 14, w / 24 + 1, h / 14 + 0.5); cr.set_source_rgb(1, 1, 1); cr.fill()
        if xx < w * 0.42:
            cr.rectangle(xx, wv, w / 24 + 1, h * 0.54); cr.set_source_rgb(0.12, 0.20, 0.45); cr.fill()
    cr.restore()


def gate(cr, x, y, p, label="BAND"):
    """Closed gate in front of a practice field."""
    cr.save(); cr.translate(x, y)
    for k in range(9):
        cr.rectangle(-260 + k * 62, -300, 14, 300); cr.set_source_rgb(0.30, 0.30, 0.34); cr.fill()
    for yy in (-260, -60):
        cr.rectangle(-270, yy, 540, 16); cr.fill()
    cr.restore()


def stadium(cr, t, night=True):
    top = (0.10, 0.12, 0.25) if night else (0.86, 0.91, 0.97)
    bg(cr, top, (0.20, 0.22, 0.32) if night else (0.95, 0.93, 0.88))
    cr.move_to(0, 520); cr.curve_to(500, 380, 1420, 380, W, 520); cr.line_to(W, 760); cr.line_to(0, 760); cr.close_path()
    cr.set_source_rgb(0.28, 0.28, 0.36); cr.fill()
    rnd = random.Random(4)
    for k in range(260):
        xx = rnd.uniform(0, W); yy = rnd.uniform(470, 750)
        if yy < 520 - 140 * math.sin(math.pi * xx / W) + 0:
            continue
        flick = 0.5 + 0.5 * math.sin(t * 6 + k)
        cr.arc(xx, yy, 5, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 0.8, 0.25 + 0.5 * flick * (k % 3 == 0)); cr.fill()
    for lx in (220, 1700):
        cr.rectangle(lx - 6, 160, 12, 360); cr.set_source_rgb(0.5, 0.5, 0.55); cr.fill()
        rounded_rect(cr, lx - 80, 110, 160, 70, 10); cr.set_source_rgb(1, 1, 0.9); cr.fill()
    cr.rectangle(0, 760, W, H - 760); cr.set_source_rgb(0.28, 0.56, 0.30); cr.fill()
    for k in range(10):
        xx = 96 + k * 192
        cr.move_to(xx, 760); cr.line_to(xx - 40, H); cr.set_source_rgba(1, 1, 1, 0.6); cr.set_line_width(5); cr.stroke()


def counter(cr, n, x, y, size, col=MAROON, alpha=1.0):
    text(cr, str(n), x, y, size, col, alpha=alpha, outline=(1, 1, 1))


def college_hall(cr, x, y, s=1.0, p=1.0):
    """Generic brick college hall with a cupola (no seal, no logo)."""
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(s * back_out(p), s * back_out(p))
    cr.rectangle(-380, -340, 760, 340); cr.set_source_rgb(0.72, 0.36, 0.28); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.move_to(-410, -340); cr.line_to(0, -470); cr.line_to(410, -340); cr.close_path()
    cr.set_source_rgb(0.30, 0.28, 0.30); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-50, -560, 100, 110); cr.set_source_rgb(0.97, 0.96, 0.92); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-66, -560); cr.line_to(0, -620); cr.line_to(66, -560); cr.close_path()
    cr.set_source_rgb(*FAMU_GREEN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for r in range(2):
        for c in range(6):
            if r == 1 and c in (2, 3):
                continue
            wx = -320 + c * 128; wy = -300 + r * 140
            cr.rectangle(wx - 28, wy, 56, 84); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-60, -150, 120, 150); cr.set_source_rgb(*WOOD_DK); cr.fill()
    for cx in (-110, -60, 60, 110):
        cr.rectangle(cx - 9, -170, 18, 170); cr.set_source_rgb(0.97, 0.96, 0.92); cr.fill()
    cr.restore()


# ================= SCENES
def s0(cr, t):  # hook: 1941, Black musician graduates from Kansas; the school's marching band kept him out
    i = 0; a, b = scene_bounds(i)
    tk = beat(i, "The school's")
    lawn(cr, (0.86, 0.91, 0.98))
    if t < tk:
        college_hall_ku(cr, 1420, 880, 0.75)
        pf = prog(t, a + 0.2, 0.5)
        foster(cr, 560, 1050, 1.15 * back_out(pf), t, pose="open" if t > beat(i, "graduated") else "rest")
        if pf > 0 and t > beat(i, "graduated"):
            grad_cap(cr, 560, head_y(1050, 1.15, t), 1.15 * back_out(prog(t, beat(i, "graduated"), 0.4)))
        pop_text(cr, "1941", 560, 170, 130, t, a + 0.1, color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "UNIVERSITY OF KANSAS", 1420, 160, 66, t, beat(i, "University"), color=TEXT, outline=(1, 1, 1))
    else:
        tm = (t - tk)
        off = -400 + (tm * 260) % 2600
        band_block(cr, 1950 - off, 980, 6, 2, 0.62, t, dx=120, dy=60, uni=KU_BLUE, trim=(0.95, 0.95, 0.95),
                   skins=WHITE_SKINS)
        gate(cr, 1000, 1000, 1)
        foster(cr, 330, 1050, 1.1, t, pose="rest", clarinet=True)
        pop_text(cr, "MARCHING BAND", 1300, 170, 70, t, beat(i, "marching band"), color=TEXT, outline=(1, 1, 1))
        stamp(cr, "KEPT OUT", 1000, 400, prog(t, beat(i, "kept him out"), 0.4), col=MAROON, size=110, rot=-0.08)
        pop_text(cr, "BECAUSE OF HIS SKIN COLOR", 1000, 560, 56, t, beat(i, "color of"), color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def college_hall_ku(cr, x, y, s):
    """Generic stone hall with a tower (no seal, no logo)."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-360, -320, 720, 320); cr.set_source_rgb(0.86, 0.82, 0.74); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.rectangle(-90, -620, 180, 300); cr.set_source_rgb(0.86, 0.82, 0.74); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-110, -620); cr.line_to(0, -740); cr.line_to(110, -620); cr.close_path()
    cr.set_source_rgb(0.45, 0.25, 0.22); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for r in range(2):
        for c in range(6):
            if c in (2, 3):
                continue
            wx = -300 + c * 120; wy = -280 + r * 130
            cr.rectangle(wx - 26, wy, 52, 80); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-45, -520, 90, 90); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-55, -150, 110, 150); cr.set_source_rgb(*WOOD_DK); cr.fill()
    cr.restore()


def s1(cr, t):  # His name: William P. Foster; told no jobs for Black conductors; set out to build his own band
    i = 1; a, b = scene_bounds(i)
    tt = beat(i, "He was told")
    ts = beat(i, "So he")
    bg(cr)
    if t < tt:
        pf = prog(t, a + 0.1, 0.5)
        foster(cr, W / 2, 1050, 1.5 * back_out(pf), t, pose="rest")
        name_tag(cr, "William P. Foster", "KU class of 1941", W / 2, 90, prog(t, beat(i, "William"), 0.4), size=64)
    elif t < ts:
        foster(cr, 520, 1050, 1.35, t, pose="rest")
        ps = prog(t, tt, 0.4)
        if ps > 0:
            panel(cr, 900, 260, 900, 380, (1, 1, 1), r=26, alpha=ps)
            text(cr, "JOBS FOR", 1350, 370, 70, TEXT, alpha=ps)
            text(cr, "BLACK CONDUCTORS", 1350, 460, 70, TEXT, alpha=ps)
        stamp(cr, "NONE", 1350, 590, prog(t, beat(i, "no jobs"), 0.4), col=MAROON, size=100, rot=-0.1)
    else:
        lawn(cr)
        foster(cr, 480, 1050, 1.3, t, pose="point", baton=True)
        pp = prog(t, beat(i, "build"), 0.6)
        for k in range(4):
            bandsman(cr, 1000 + k * 190, 1050, 0.75 * back_out(clamp(pp * 4 - k)), t, k=k, step=False,
                     inst="drum" if k == 3 else "horn")
        pop_text(cr, "BUILD HIS OWN BAND", 1290, 180, 80, t, ts, color=MAROON, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s2(cr, t):  # 1946: Florida A&M hired him as director of bands; he found just sixteen members
    i = 2; a, b = scene_bounds(i)
    tf = beat(i, "He found")
    lawn(cr, (0.88, 0.93, 0.98))
    if t < tf:
        college_hall(cr, 1400, 880, 0.75)
        foster(cr, 520, 1050, 1.25, t, pose="open")
        pop_text(cr, "1946", 520, 170, 130, t, a + 0.1, color=MAROON, outline=(1, 1, 1))
        ps = prog(t, beat(i, "Florida"), 0.4)
        if ps > 0:
            panel(cr, 1000, 110, 800, 120, FAMU_GREEN, r=24, alpha=ps)
            text(cr, "FLORIDA A&M", 1400, 195, 70, FAMU_ORANGE, alpha=ps)
        pop_text(cr, "DIRECTOR OF BANDS", 1400, 330, 60, t, beat(i, "director"), color=TEXT, outline=(1, 1, 1))
    else:
        foster(cr, 260, 1050, 1.05, t, pose="hold", baton=True)
        pw = prog(t, tf + 0.1, 1.4)
        n = int(min(16, pw * 16 + 0.999)) if pw > 0 else 0
        band_block(cr, 560, 820, 8, 2, 0.5, t, dx=165, dy=150, n=16, p=pw, step=False)
        ps = prog(t, beat(i, "sixteen"), 0.4)
        if ps > 0:
            panel(cr, 760, 60, 700, 170, MAROON, r=24, alpha=ps)
            text(cr, "JUST 16 MEMBERS", 1110, 175, 72, GOLDC, alpha=ps)
    sceneout(cr, t, a, b)


def s3(cr, t):  # Bo: part nobody tells you; 16 -> Marching 100 -> hundreds; high steps, big sound
    i = 3; a, b = scene_bounds(i)
    tf = beat(i, "Foster turned")
    tg = beat(i, "and the band grew")
    th = beat(i, "famous for")
    if t < tf:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY TELLS YOU", W / 2, 140, 84, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    elif t < tg:
        lawn(cr)
        band_block(cr, 170, 620, 10, 4, 0.42, t, dx=170, dy=120, n=40, p=prog(t, tf, 1.6))
        pc = prog(t, beat(i, "Marching One Hundred"), 0.45)
        if pc > 0:
            panel(cr, 560, 60, 800, 150, FAMU_GREEN, r=24, alpha=pc)
            text(cr, "MARCHING 100", W / 2, 165, 90, FAMU_ORANGE, alpha=pc)
        pop_text(cr, "FROM 16 PLAYERS", W / 2, 300, 64, t, tf, color=MAROON, outline=(1, 1, 1))
    elif t < th:
        lawn(cr, (0.86, 0.92, 0.98))
        band_block(cr, 90, 560, 16, 6, 0.33, t, dx=115, dy=88)
        ps = prog(t, beat(i, "hundreds"), 0.4)
        if ps > 0:
            panel(cr, 440, 50, 1040, 150, MAROON, r=24, alpha=ps)
            text(cr, "HUNDREDS OF PLAYERS", W / 2, 150, 72, GOLDC, alpha=ps)
    else:
        lawn(cr)
        for k in range(5):
            bandsman(cr, 300 + k * 330, 1050, 1.0, t, k=k, inst="drum" if k == 2 else "horn", phase=(k % 2) * 0.5)
        pop_text(cr, "HIGH STEPS", 620, 170, 96, t, beat(i, "high steps"), color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "BIG SOUND", 1320, 170, 96, t, beat(i, "big sound"), color=FAMU_GREEN, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s4(cr, t):  # 1989: France's bicentennial; Bastille Day parade in Paris; Marching 100 chosen to represent the U.S.
    i = 4; a, b = scene_bounds(i)
    tp = beat(i, "For the Bastille")
    bg(cr, (0.84, 0.90, 0.98), (0.95, 0.93, 0.88))
    eiffel(cr, 1560, 880, 0.95)
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.78, 0.74, 0.68); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    if t < tp:
        tricolor(cr, 300, 330, 420, 260, t, prog(t, beat(i, "France"), 0.5))
        pop_text(cr, "1989", 510, 180, 130, t, a + 0.1, color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "200 YEARS SINCE", 760, 720, 70, t, beat(i, "two hundred"), color=TEXT, outline=(1, 1, 1))
        pop_text(cr, "THE FRENCH REVOLUTION", 760, 810, 70, t, beat(i, "revolution"), color=MAROON, outline=(1, 1, 1))
    else:
        tm = t - tp
        off = (tm * 170)
        band_block(cr, -700 + off, 880, 9, 2, 0.5, t, dx=130, dy=95)
        ps = prog(t, tp, 0.4)
        if ps > 0:
            panel(cr, 140, 50, 1000, 130, (1, 1, 1), r=24, alpha=ps)
            text(cr, "BASTILLE DAY PARADE · PARIS", 640, 138, 56, TEXT, alpha=ps)
        pr = prog(t, beat(i, "represent"), 0.45)
        us_flag(cr, 1060, 300, 300, 170, t, pr)
        if pr > 0:
            panel(cr, 140, 220, 820, 150, MAROON, r=24, alpha=pr)
            text(cr, "REPRESENTING", 550, 285, 50, (1, 1, 1), alpha=pr)
            text(cr, "THE UNITED STATES", 550, 350, 62, GOLDC, alpha=pr)
    sceneout(cr, t, a, b)


def s5(cr, t):  # 2007 Super Bowl halftime show in Miami; Foster led it 52 years, until 1998
    i = 5; a, b = scene_bounds(i)
    tf = beat(i, "Foster led")
    if t < tf:
        stadium(cr, t)
        band_block(cr, 120, 800, 14, 3, 0.4, t, dx=125, dy=90)
        pop_text(cr, "2007", W / 2, 170, 120, t, a + 0.1, color=GOLDC, outline=INK)
        ps = prog(t, beat(i, "Super Bowl"), 0.4)
        if ps > 0:
            panel(cr, 510, 230, 900, 130, (1, 1, 1), r=24, alpha=ps)
            text(cr, "SUPER BOWL HALFTIME", W / 2, 318, 66, TEXT, alpha=ps)
        pop_text(cr, "MIAMI", W / 2, 450, 70, t, beat(i, "Miami"), color=GOLDC, outline=INK)
    else:
        lawn(cr)
        foster(cr, 560, 1050, 1.3, t, pose="point", baton=True, older=True)
        band_block(cr, 1000, 820, 6, 2, 0.5, t, dx=150, dy=110, step=True)
        pop_text(cr, "52 YEARS", 1350, 170, 120, t, beat(i, "fifty-two"), color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "1946–1998", 1350, 300, 80, t, beat(i, "until"), color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s6(cr, t):  # kept out of one band -> built a band the world asked for; CTA
    i = 6; a, b = scene_bounds(i)
    tq = beat(i, "Which")
    if t < tq:
        lawn(cr)
        foster(cr, 330, 1050, 1.1, t, pose="point", baton=True, older=True)
        band_block(cr, 680, 760, 9, 3, 0.45, t, dx=135, dy=100)
        stamp(cr, "KEPT OUT", 520, 200, prog(t, a + 0.1, 0.4), col=(0.45, 0.45, 0.45), size=64, rot=-0.08)
        arrow(cr, 780, 200, 960, 200, prog(t, beat(i, "built"), 0.4))
        pop_text(cr, "A BAND THE WORLD ASKED FOR", 1430, 175, 60, t, beat(i, "whole world"), color=MAROON, outline=(1, 1, 1))
    else:
        bg(cr)
        bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=False)
        text(cr, "Which HBCU band is", 1250, 420, 70, TEXT, alpha=prog(t, tq, 0.4))
        text(cr, "the best in the land?", 1250, 510, 70, MAROON, alpha=prog(t, tq, 0.4))
        pop_text(cr, "Tell us in the comments", 1250, 680, 56, t, beat(i, "Tell us"))
        k = max(0, (t - (b - 0.8)) / 0.8)
        if k > 0:
            cr.set_source_rgba(*BG, k); cr.paint()
        sceneout(cr, t, a, 1e9)
        return
    sceneout(cr, t, a, b)


def thumb_hero(cr, x, y, r):
    """Hero object: a drum major's baton crossed over a brass bell."""
    cr.save(); cr.translate(x, y)
    cr.move_to(-r * 0.2, -r * 0.1); cr.line_to(r * 0.75, -r * 0.55); cr.line_to(r * 0.75, r * 0.55); cr.line_to(-r * 0.2, r * 0.1)
    cr.close_path(); cr.set_source_rgb(*BRASS); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.move_to(-r * 0.8, 0); cr.line_to(-r * 0.2, 0); cr.set_source_rgb(*BRASS); cr.set_line_width(r * 0.14); cr.stroke()
    cr.save(); cr.rotate(-0.8)
    cr.move_to(0, -r); cr.line_to(0, r); cr.set_source_rgb(1, 1, 1); cr.set_line_width(r * 0.1); cr.stroke()
    cr.arc(0, -r, r * 0.12, 0, 2 * math.pi); cr.set_source_rgb(*FAMU_ORANGE); cr.fill()
    cr.restore()
    cr.restore()


SCENES = [s0, s1, s2, s3, s4, s5, s6]
