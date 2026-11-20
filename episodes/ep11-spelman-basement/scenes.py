"""Ep11 scenes: Spelman College — eleven students in a church basement (1881). One function per paragraph."""
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



# ---------------- ep11 people and props (no logos or seals; school names as text only)
STU_SKINS = [(0.36, 0.24, 0.16), (0.26, 0.17, 0.11), (0.46, 0.32, 0.22), (0.32, 0.21, 0.14), (0.40, 0.27, 0.18)]
QUARLES_SKIN = (0.30, 0.20, 0.14)
HAIR_BR = (0.42, 0.30, 0.20)
LAMP = (1.0, 0.85, 0.45)
SPEL_BLUE = (0.16, 0.30, 0.56)


def packard(cr, x, y, s=1.0, t=0.0, pose="rest", walking=False):
    """Sophia Packard: stylized older woman, dark dress, gray hair (no mouth)."""
    woman(cr, x, y, s, t, dress=(0.20, 0.20, 0.26), skin=SKIN_LT, hair=GRAY, pose=pose, walking=walking)


def giles(cr, x, y, s=1.0, t=0.0, pose="rest", walking=False):
    """Harriet Giles: stylized woman, plum dress, brown hair (no mouth)."""
    woman(cr, x, y, s, t + 1.3, dress=(0.34, 0.20, 0.30), skin=SKIN_LT, hair=HAIR_BR, pose=pose, walking=walking)


def quarles(cr, x, y, s=1.0, t=0.0, pose="rest"):
    if s <= 0.01:
        return
    """Rev. Frank Quarles: stylized pastor, black suit, white collar band, glasses (no mouth)."""
    man(cr, x, y, s, t, suit=(0.12, 0.12, 0.14), tie=(0.95, 0.95, 0.95), skin=QUARLES_SKIN, hair=HAIR_DK, pose=pose)
    glasses(cr, x, head_y(y, s, t), s)


def rockefeller(cr, x, y, s=1.0, t=0.0, pose="rest", walking=False):
    if s <= 0.01:
        return
    """John D. Rockefeller (1880s): stylized man, gray suit, mustache (no mouth)."""
    man(cr, x, y, s, t, suit=(0.30, 0.30, 0.34), tie=(0.12, 0.12, 0.14), skin=SKIN_LT, hair=HAIR_BR, pose=pose,
        walking=walking)
    hy = head_y(y, s, t) if not walking else y + (-385 - abs(math.sin(t * 8)) * 5) * s
    mustache(cr, x, hy, s, col=HAIR_BR, w=24)


def laura(cr, x, y, s=1.0, t=0.0, pose="rest"):
    woman(cr, x, y, s, t + 0.6, dress=SPEL_BLUE, skin=SKIN_LT, hair=HAIR_DK, pose=pose)


def student_w(cr, x, y, s, t, k, pose="rest", walking=False):
    woman(cr, x, y, s, t + k * 0.7, dress=DRESSES[k % len(DRESSES)], skin=STU_SKINS[k % len(STU_SKINS)], pose=pose,
          walking=walking)


def girl(cr, x, y, s, t, walking=False):
    if s <= 0.01:
        return
    kid(cr, x, y, s, dress=(0.60, 0.30, 0.36), girl=True, t=t, walking=walking)


def church_basement(cr, x, gy, s=1.0, lamp=1.0, t=0.0):
    """Cutaway: church above the ground line gy, basement room below it (x = centre)."""
    bg(cr, (0.86, 0.91, 0.97), (0.95, 0.93, 0.88))
    church(cr, x, gy, 0.62 * s)
    cr.rectangle(0, gy, W, H - gy); cr.set_source_rgb(0.56, 0.44, 0.32); cr.fill()
    w = 1000 * s; h = H - gy - 10
    rounded_rect(cr, x - w / 2, gy + 20, w, h - 30, 18); cr.set_source_rgb(0.80, 0.70, 0.56); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.move_to(0, gy); cr.line_to(W, gy); cr.set_line_width(5); cr.stroke()
    if lamp > 0:
        g = cairo.RadialGradient(x, gy + 70, 10, x, gy + 70, 420)
        fl = 0.9 + 0.1 * math.sin(t * 7)
        g.add_color_stop_rgba(0, *LAMP, 0.55 * lamp * fl); g.add_color_stop_rgba(1, *LAMP, 0)
        cr.set_source(g); rounded_rect(cr, x - w / 2, gy + 20, w, h - 30, 18); cr.fill()
        cr.arc(x, gy + 70, 16, 0, 2 * math.pi); cr.set_source_rgb(*LAMP); cr.fill()
    # stairs on the left
    for k in range(6):
        cr.rectangle(x - w / 2 + 10 + k * 26, gy + 30 + k * 55, 120 - k * 18, 14)
        cr.set_source_rgb(*WOOD_DK); cr.fill()


def blackboard(cr, x, y, w=300, h=170, txt=None):
    rounded_rect(cr, x - w / 2, y - h / 2, w, h, 8); cr.set_source_rgb(0.16, 0.26, 0.20); cr.fill_preserve()
    cr.set_source_rgb(*WOOD_DK); cr.set_line_width(10); cr.stroke()
    if txt:
        text(cr, txt, x, y + 18, 54, (0.95, 0.95, 0.90), bold=False)


def doc(cr, x, y, p, title="DEBT", stamp_p=0.0, rot=-0.05):
    if p <= 0:
        return
    k = back_out(p)
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(k, k)
    rounded_rect(cr, -170, -220, 340, 440, 10); cr.set_source_rgb(*PAPER); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    text(cr, title, 0, -140, 58, TEXT)
    cr.set_source_rgba(*INK, 0.35); cr.set_line_width(4)
    for r in range(6):
        cr.move_to(-120, -80 + r * 46); cr.line_to(120 - (r % 3) * 30, -80 + r * 46); cr.stroke()
    cr.restore()
    stamp(cr, "PAID", x, y + 30, stamp_p, col=(0.15, 0.50, 0.25), size=90, rot=-0.2)


def barracks(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-260, -170, 520, 170); cr.set_source_rgb(0.70, 0.62, 0.50); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-285, -170); cr.line_to(0, -250); cr.line_to(285, -170); cr.close_path()
    cr.set_source_rgb(0.40, 0.36, 0.34); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for wx in (-190, -95, 95, 190):
        cr.rectangle(wx - 24, -130, 48, 56); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-30, -110, 60, 110); cr.set_source_rgb(*WOOD_DK); cr.fill()
    cr.restore()


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
    cr.set_source_rgb(*SPEL_BLUE); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
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


def lawn(cr, sky=(0.86, 0.92, 0.98)):
    bg(cr, sky, (0.96, 0.93, 0.86))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(*GRASS); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


# ================= SCENES
def s0(cr, t):  # hook: April 11, 1881; eleven students into a church basement in Atlanta -> Spelman College
    i = 0; a, b = scene_bounds(i)
    tb = beat(i, "That basement")
    church_basement(cr, 1000, 560, 1.0, lamp=prog(t, beat(i, "basement"), 0.6), t=t)
    n = 11
    pw = prog(t, a - 0.6, tb - a)
    for k in range(n):
        pk = clamp(pw * n - k * 0.8)
        xx = 620 + k * 72 if k < 10 else 1380
        yy = 1010
        if k == 10:
            girl(cr, 1400, yy, 0.7 * back_out(pk) if pk > 0 else 0, t, walking=0 < pk < 1)
        elif pk > 0:
            student_w(cr, xx, yy, 0.52 * back_out(pk), t, k)
    pop_text(cr, "APRIL 11, 1881", 430, 150, 96, t, a + 0.1, color=MAROON, outline=(1, 1, 1))
    pop_text(cr, "11 STUDENTS", 430, 260, 70, t, beat(i, "Eleven"), color=TEXT, outline=(1, 1, 1))
    pop_text(cr, "ATLANTA", 1560, 150, 64, t, beat(i, "Atlanta"), color=TEXT, outline=(1, 1, 1))
    ps = prog(t, tb + 0.3, 0.45)
    if ps > 0:
        panel(cr, 1210, 220, 640, 130, MAROON, r=24, alpha=ps)
        text(cr, "SPELMAN COLLEGE", 1530, 307, 62, GOLDC, alpha=ps)
        bo(cr, 220, 1060, 0.3, t, pose="shrug", wide=0.9, brow=0.8, talk=False)
    sceneout(cr, t, a, b)


def s1(cr, t):  # Packard and Giles, Baptist missionaries from New England; came south to teach; almost no money
    i = 1; a, b = scene_bounds(i)
    tm = beat(i, "They had almost")
    lawn(cr, (0.88, 0.92, 0.97))
    if t < tm:
        pw = prog(t, a + 0.1, 1.2)
        packard(cr, 1500 - 760 * ease(pw), 1050, 1.1, t, walking=0 < pw < 1)
        giles(cr, 1780 - 760 * ease(pw), 1050, 1.1, t, walking=0 < pw < 1)
        name_tag(cr, "Sophia Packard", None, 740, 60, prog(t, beat(i, "Sophia"), 0.4), size=48)
        name_tag(cr, "Harriet Giles", None, 1300, 60, prog(t, beat(i, "Harriet"), 0.4), size=48)
        pop_text(cr, "MISSIONARIES FROM NEW ENGLAND", W / 2, 230, 58, t, beat(i, "missionaries"), color=MAROON,
                 outline=(1, 1, 1))
        pc = prog(t, beat(i, "They came"), 0.4)
        if pc > 0:
            for k in range(3):
                student_w(cr, 180 + k * 150, 1060, 0.62 * back_out(pc), t, k + 2)
            girl(cr, 640 * 0 + 160 + 3 * 150, 1060, 0.62 * back_out(pc), t)
            pop_text(cr, "TO TEACH BLACK WOMEN AND GIRLS", 520, 520, 46, t, beat(i, "teach"), color=TEXT,
                     outline=(1, 1, 1))
    else:
        packard(cr, 700, 1050, 1.15, t, pose="open")
        giles(cr, 1000, 1050, 1.15, t, pose="open")
        pe = prog(t, tm, 0.4)
        if pe > 0:
            coin(cr, 1500, 480, 110 * back_out(pe), label="$")
        stamp(cr, "ALMOST NO MONEY", 1500, 230, prog(t, beat(i, "no money"), 0.4), col=MAROON, size=64)
    sceneout(cr, t, a, b)


def s2(cr, t):  # Quarles offered his basement; first class ten women and one girl; some born enslaved
    i = 2; a, b = scene_bounds(i)
    tf = beat(i, "The first class")
    if t < tf:
        church_basement(cr, 1250, 560, 0.8, lamp=0.6, t=t)
        pq = prog(t, a + 0.1, 0.45)
        quarles(cr, 380, 1050, 1.2 * back_out(pq), t, pose="point" if t > beat(i, "offered") else "rest")
        name_tag(cr, "Rev. Frank Quarles", "Friendship Baptist Church", 420, 60, prog(t, beat(i, "Frank"), 0.4), size=48)
        pop_text(cr, "\"USE MY BASEMENT\"", 1250, 180, 64, t, beat(i, "basement"), color=MAROON, outline=(1, 1, 1))
    else:
        church_basement(cr, W / 2, 470, 1.4, lamp=1.0, t=t)
        blackboard(cr, W / 2 + 330, 640, 320, 160, "A B C")
        pw = prog(t, tf, 1.0)
        for k in range(10):
            pk = clamp(pw * 11 - k)
            if pk > 0:
                student_w(cr, 360 + k * 108 + (54 if k >= 5 else 0) * 0, 1050 if k % 2 else 1000, 0.5 * back_out(pk), t, k)
        pg = clamp(pw * 11 - 10)
        if pg > 0:
            girl(cr, 1500, 1050, 0.75 * back_out(pg), t)
        pn = prog(t, beat(i, "ten women"), 0.4)
        if pn > 0:
            panel(cr, 560, 30, 800, 130, MAROON, r=24, alpha=pn)
            text(cr, "10 WOMEN + 1 GIRL", W / 2, 118, 66, GOLDC, alpha=pn)
        stamp(cr, "SOME BORN ENSLAVED", W / 2, 300, prog(t, beat(i, "born enslaved"), 0.4), col=MAROON, size=60, rot=-0.04)
    sceneout(cr, t, a, b)


def s3(cr, t):  # outgrew the basement; 1882 founders went north; met Rockefeller in Cleveland
    i = 3; a, b = scene_bounds(i)
    tn = beat(i, "In eighteen eighty-two")
    tc = beat(i, "In Cleveland")
    if t < tn:
        church_basement(cr, W / 2, 470, 1.4, lamp=1.0, t=t)
        for k in range(22):
            xx = 330 + (k % 11) * 115 + (k // 11) * 50
            student_w(cr, xx, 1000 + (k // 11) * 60, 0.42 if k // 11 == 0 else 0.48, t, k)
        pop_text(cr, "OUTGREW THE BASEMENT", W / 2, 150, 90, t, beat(i, "outgrown"), color=MAROON, outline=(1, 1, 1))
    elif t < tc:
        bg(cr, (0.88, 0.92, 0.97), (0.95, 0.93, 0.88))
        pop_text(cr, "1882", W / 2, 200, 130, t, tn, color=MAROON, outline=(1, 1, 1))
        panel(cr, 180, 640, 380, 120, (1, 1, 1), r=20)
        text(cr, "ATLANTA", 370, 720, 58, TEXT)
        pm = prog(t, beat(i, "went north"), 1.0)
        arrow(cr, 560, 700, 1340, 420, pm)
        pop_text(cr, "NORTH", 1500, 440, 70, t, beat(i, "north"), color=MAROON, outline=(1, 1, 1))
        packard(cr, 560 + 700 * ease(pm), 1050, 0.75, t, walking=0 < pm < 1)
        giles(cr, 720 + 700 * ease(pm), 1050, 0.75, t, walking=0 < pm < 1)
        pop_text(cr, "TO RAISE MONEY", 1450, 560, 60, t, beat(i, "raise money"), color=TEXT, outline=(1, 1, 1))
    else:
        street(cr, (0.86, 0.88, 0.94))
        church(cr, 1550, 880, 0.75)
        pop_text(cr, "CLEVELAND", 1550, 150, 80, t, tc, color=MAROON, outline=(1, 1, 1))
        packard(cr, 300, 1050, 1.0, t, pose="open")
        giles(cr, 540, 1050, 1.0, t)
        pr = prog(t, beat(i, "John D."), 0.45)
        rockefeller(cr, 1000, 1050, 1.2 * back_out(pr), t, pose="rest")
        name_tag(cr, "John D. Rockefeller", None, 1000, 260, pr, size=54)
    sceneout(cr, t, a, b)


def s4(cr, t):  # Bo: part nobody tells you; 1884 Rockefeller visited, paid off debt on campus; former Union barracks
    i = 4; a, b = scene_bounds(i)
    tv = beat(i, "In eighteen eighty-four")
    tp = beat(i, "He paid")
    if t < tv:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY TELLS YOU", W / 2, 140, 84, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    elif t < tp:
        lawn(cr)
        for k, bx in enumerate((1250, 1700)):
            barracks(cr, bx, 880, 0.8)
        pr = prog(t, beat(i, "Rockefeller"), 0.8)
        rockefeller(cr, -100 + 600 * ease(pr), 1050, 1.15, t, walking=0 < pr < 1)
        pop_text(cr, "1884", 420, 180, 130, t, tv, color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "HE VISITED", 1450, 330, 70, t, beat(i, "visited"), color=TEXT, outline=(1, 1, 1))
    else:
        tl = beat(i, "land that")
        lawn(cr)
        rockefeller(cr, 360, 1050, 1.1, t, pose="hold")
        if t < tl:
            doc(cr, 960, 520, prog(t, tp, 0.4), "DEBT", stamp_p=prog(t, beat(i, "paid off"), 0.4))
            pop_text(cr, "DEBT ON THE NEW CAMPUS", 1240, 140, 66, t, beat(i, "debt"), color=MAROON, outline=(1, 1, 1))
        else:
            for k, bx in enumerate((900, 1500)):
                barracks(cr, bx, 880, 0.95)
            ps = prog(t, tl, 0.4)
            if ps > 0:
                panel(cr, 660, 150, 1080, 200, (1, 1, 1), r=24, alpha=ps)
                text(cr, "ONCE UNION ARMY", 1200, 235, 66, TEXT, alpha=ps)
                text(cr, "BARRACKS", 1200, 320, 70, MAROON, alpha=ps)
    sceneout(cr, t, a, b)


def s5(cr, t):  # renamed Spelman Seminary for Laura Spelman Rockefeller and her antislavery parents; 1901; 1924
    i = 5; a, b = scene_bounds(i)
    t1 = beat(i, "In nineteen oh one")
    t2 = beat(i, "In nineteen twenty-four")
    lawn(cr)
    if t < t1:
        ps = prog(t, a + 0.1, 0.45)
        if ps > 0:
            panel(cr, 560, 40, 800, 130, MAROON, r=24, alpha=ps)
            text(cr, "SPELMAN SEMINARY", W / 2, 128, 64, GOLDC, alpha=ps)
        pl = prog(t, beat(i, "after his wife"), 0.45)
        laura(cr, 560, 1050, 1.15 * back_out(pl), t, pose="open")
        name_tag(cr, "Laura Spelman Rockefeller", None, 560, 230, prog(t, beat(i, "Laura"), 0.4), size=44)
        pp = prog(t, beat(i, "her parents"), 0.45)
        if pp > 0:
            man(cr, 1240, 1050, 1.0 * back_out(pp), t, suit=(0.22, 0.22, 0.26), tie=(0.12, 0.12, 0.14), skin=SKIN_LT,
                hair=GRAY, whiskers=True)
            woman(cr, 1520, 1050, 1.0 * back_out(pp), t + 0.4, dress=(0.26, 0.22, 0.28), skin=SKIN_LT, hair=GRAY)
            name_tag(cr, "Harvey & Lucy Spelman", "her parents", 1380, 230, pp, size=44)
        stamp(cr, "FOUGHT SLAVERY", 1380, 420, prog(t, beat(i, "fought slavery"), 0.4), col=MAROON, size=58, rot=-0.05)
    elif t < t2:
        college_hall(cr, 1380, 880, 0.8)
        for k, gx in enumerate((520, 820)):
            woman(cr, gx, 1050, 1.1, t + k, dress=(0.12, 0.12, 0.14), skin=STU_SKINS[k], pose="open" if k else "rest")
            grad_cap(cr, gx, head_y(1050, 1.1, t + k), 1.1)
        pop_text(cr, "1901", 670, 170, 120, t, t1, color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "FIRST COLLEGE DEGREES", 670, 290, 60, t, beat(i, "first college"), color=TEXT, outline=(1, 1, 1))
    else:
        college_hall(cr, W / 2, 880, 1.0, p=prog(t, t2, 0.5))
        pop_text(cr, "1924", W / 2, 140, 110, t, t2, color=MAROON, outline=(1, 1, 1))
        ps = prog(t, beat(i, "became Spelman"), 0.4)
        if ps > 0:
            panel(cr, 520, 770, 880, 140, MAROON, r=24, alpha=ps)
            text(cr, "SPELMAN COLLEGE", W / 2, 865, 72, GOLDC, alpha=ps)
    sceneout(cr, t, a, b)


def s6(cr, t):  # eleven students in a basement -> a college known around the world; CTA
    i = 6; a, b = scene_bounds(i)
    tq = beat(i, "Which")
    if t < tq:
        lawn(cr)
        college_hall(cr, 1350, 880, 0.85)
        for k in range(5):
            student_w(cr, 180 + k * 125, 1050, 0.6, t, k)
        girl(cr, 180 + 5 * 125, 1050, 0.6, t)
        pop_text(cr, "11 STUDENTS", 480, 180, 80, t, a + 0.1, color=TEXT, outline=(1, 1, 1))
        arrow(cr, 820, 300, 1080, 300, prog(t, beat(i, "became"), 0.5))
        pop_text(cr, "KNOWN WORLDWIDE", 1350, 180, 72, t, beat(i, "known"), color=MAROON, outline=(1, 1, 1))
    else:
        bg(cr)
        bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=False)
        text(cr, "Which HBCU founder story", 1250, 420, 66, TEXT, alpha=prog(t, tq, 0.4))
        text(cr, "should we tell next?", 1250, 510, 66, MAROON, alpha=prog(t, tq, 0.4))
        pop_text(cr, "Tell us in the comments", 1250, 680, 56, t, beat(i, "Tell us"))
        k = max(0, (t - (b - 0.8)) / 0.8)
        if k > 0:
            cr.set_source_rgba(*BG, k); cr.paint()
        sceneout(cr, t, a, 1e9)
        return
    sceneout(cr, t, a, b)


def thumb_hero(cr, x, y, r):
    """Hero object: the basement oil lamp."""
    cr.save(); cr.translate(x, y)
    g = cairo.RadialGradient(0, 0, 5, 0, 0, r * 1.2)
    g.add_color_stop_rgba(0, *LAMP, 0.9); g.add_color_stop_rgba(1, *LAMP, 0)
    cr.set_source(g); cr.arc(0, 0, r * 1.2, 0, 2 * math.pi); cr.fill()
    cr.move_to(-r * 0.45, r * 0.6); cr.line_to(r * 0.45, r * 0.6); cr.line_to(r * 0.3, r * 0.25); cr.line_to(-r * 0.3, r * 0.25)
    cr.close_path(); cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.save(); cr.translate(0, -r * 0.05); cr.scale(0.55, 1); cr.arc(0, 0, r * 0.45, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgba(1, 1, 1, 0.6); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(0, r * 0.2); cr.curve_to(-r * 0.15, 0, -r * 0.05, -r * 0.15, 0, -r * 0.3)
    cr.curve_to(r * 0.05, -r * 0.15, r * 0.15, 0, 0, r * 0.2); cr.set_source_rgb(1.0, 0.6, 0.15); cr.fill()
    cr.restore()


SCENES = [s0, s1, s2, s3, s4, s5, s6]
