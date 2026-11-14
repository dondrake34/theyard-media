"""Ep10 scenes: Tuskegee — the student-made bricks, three failed kilns and the pawned watch. One function per paragraph."""
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



# ---------------- ep10 people and props (no logos or seals; school names as text only)
HAIR_DK = (0.10, 0.08, 0.07)
BTW_SKIN = (0.42, 0.29, 0.20)     # Washington
ADAMS_SKIN = (0.30, 0.20, 0.14)   # Lewis Adams
STU_SKINS = [(0.36, 0.24, 0.16), (0.26, 0.17, 0.11), (0.46, 0.32, 0.22), (0.32, 0.21, 0.14)]
WORK = [(0.55, 0.45, 0.32), (0.32, 0.38, 0.50), (0.48, 0.30, 0.24), (0.40, 0.44, 0.32)]
CLAY = (0.72, 0.40, 0.26)
NIGHT = ((0.10, 0.12, 0.24), (0.20, 0.20, 0.32))
SILVER = (0.82, 0.83, 0.86)


def washington(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0, walking=False, prop=None):
    """Booker T. Washington: stylized man, dark suit, short mustache (no mouth)."""
    man(cr, x, y, s, t, suit=(0.18, 0.18, 0.22), tie=(0.12, 0.12, 0.14), skin=BTW_SKIN, hair=HAIR_DK,
        pose=pose, pose_to=pose_to, pose_t=pose_t, walking=walking, prop=prop)
    hy = head_y(y, s, t) if not walking else y + (-385 - abs(math.sin(t * 8)) * 5) * s
    mustache(cr, x, hy, s, w=20)


def adams(cr, x, y, s=1.0, t=0.0, pose="rest"):
    """Lewis Adams: stylized older man, brown coat, gray hair and whiskers (no mouth)."""
    man(cr, x, y, s, t, suit=(0.36, 0.26, 0.18), tie=(0.20, 0.30, 0.22), skin=ADAMS_SKIN, hair=GRAY,
        pose=pose, whiskers=True)


def student(cr, x, y, s, t, k, pose="rest", walking=False):
    if k % 2:
        woman(cr, x, y, s, t, dress=DRESSES[k % len(DRESSES)], skin=STU_SKINS[k % 4], pose=pose, walking=walking)
    else:
        man(cr, x, y, s, t, suit=WORK[k % 4], tie=WORK[(k + 1) % 4], skin=STU_SKINS[k % 4], hair=HAIR_DK,
            pose=pose, walking=walking)


def brick(cr, x, y, w=70, h=32, col=BRICK):
    cr.rectangle(x - w / 2, y - h / 2, w, h); cr.set_source_rgb(*col); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()


def brick_stack(cr, x, y, rows=4, cols=4, p=1.0):
    n = int(rows * cols * clamp(p) + 0.999)
    k = 0
    for r in range(rows):
        for c in range(cols - (r % 2)):
            if k >= n:
                return
            brick(cr, x + (c - (cols - 1) / 2 + (r % 2) * 0.5) * 72, y - 16 - r * 34)
            k += 1


def kiln(cr, x, y, s=1.0, fire=0.0, collapse=0.0, label=None, t=0.0):
    """Dome-shaped brick kiln. fire 0..1 glow at the arch; collapse 0..1 slumps it into rubble."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    if collapse > 0.6:
        rng = random.Random(7)
        for k in range(26):
            bx = rng.uniform(-200, 200); by = -rng.uniform(0, 70) * (1 - abs(bx) / 260)
            cr.save(); cr.translate(bx, by - 16); cr.rotate(rng.uniform(-0.8, 0.8))
            brick(cr, 0, 0, 60, 28, BRICK if k % 3 else CLAY); cr.restore()
        cr.restore(); return
    sq = 1 - 0.5 * ease(collapse / 0.6)
    cr.scale(1 + 0.25 * (1 - sq), sq)
    cr.move_to(-190, 0); cr.curve_to(-190, -300, 190, -300, 190, 0); cr.close_path()
    cr.set_source_rgb(*CLAY); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.save(); cr.move_to(-190, 0); cr.curve_to(-190, -300, 190, -300, 190, 0); cr.close_path(); cr.clip()
    cr.set_source_rgba(*INK, 0.35); cr.set_line_width(3)
    for r in range(8):
        yy = -r * 32
        cr.move_to(-200, yy); cr.line_to(200, yy); cr.stroke()
        for c in range(-4, 5):
            xx = c * 60 + (r % 2) * 30
            cr.move_to(xx, yy); cr.line_to(xx, yy - 32); cr.stroke()
    cr.restore()
    cr.move_to(-60, 0); cr.curve_to(-60, -110, 60, -110, 60, 0); cr.close_path()
    cr.set_source_rgb(0.12, 0.08, 0.06); cr.fill()
    if fire > 0:
        fl = 0.85 + 0.15 * math.sin(t * 13)
        cr.move_to(-46, 0); cr.curve_to(-40, -70 * fl, -10, -40, 0, -95 * fl)
        cr.curve_to(10, -40, 40, -70 * fl, 46, 0); cr.close_path()
        cr.set_source_rgba(1.0, 0.55, 0.12, fire); cr.fill()
        cr.move_to(-24, 0); cr.curve_to(-20, -40, 0, -30, 0, -60 * fl); cr.curve_to(0, -30, 20, -40, 24, 0)
        cr.close_path(); cr.set_source_rgba(1.0, 0.86, 0.3, fire); cr.fill()
    cr.restore()
    if label:
        text(cr, label, x, y + 60 * s, 40 * s, TEXT, outline=(1, 1, 1))


def x_mark(cr, x, y, p, r=90, col=RED):
    if p <= 0:
        return
    cr.save(); cr.set_source_rgba(*col, 0.9); cr.set_line_width(22); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    k = ease(clamp(p * 2)); cr.move_to(x - r, y - r); cr.line_to(x - r + 2 * r * k, y - r + 2 * r * k); cr.stroke()
    k = ease(clamp(p * 2 - 1))
    if k > 0:
        cr.move_to(x + r, y - r); cr.line_to(x + r - 2 * r * k, y - r + 2 * r * k); cr.stroke()
    cr.restore()


def check_mark(cr, x, y, p, r=90, col=(0.15, 0.55, 0.25)):
    if p <= 0:
        return
    cr.save(); cr.set_source_rgba(*col, 0.95); cr.set_line_width(26); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    k = ease(clamp(p))
    pts = [(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)]
    cr.move_to(*pts[0])
    if k < 0.4:
        q = k / 0.4; cr.line_to(pts[0][0] + (pts[1][0] - pts[0][0]) * q, pts[0][1] + (pts[1][1] - pts[0][1]) * q)
    else:
        q = (k - 0.4) / 0.6; cr.line_to(*pts[1])
        cr.line_to(pts[1][0] + (pts[2][0] - pts[1][0]) * q, pts[1][1] + (pts[2][1] - pts[1][1]) * q)
    cr.stroke(); cr.restore()


def pocket_watch(cr, x, y, r=60, t=0.0, alpha=1.0, swing=0.0):
    if alpha <= 0:
        return
    cr.save(); cr.translate(x, y); cr.rotate(swing)
    cr.push_group()
    cr.move_to(0, -r - 18); cr.line_to(0, -r - 70); cr.set_source_rgb(*GOLDC); cr.set_line_width(6); cr.stroke()
    cr.arc(0, -r - 10, 14, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.arc(0, 0, r, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.arc(0, 0, r * 0.8, 0, 2 * math.pi); cr.set_source_rgb(*PAPER); cr.fill()
    for k in range(12):
        a = k * math.pi / 6
        cr.move_to(math.cos(a) * r * 0.66, math.sin(a) * r * 0.66); cr.line_to(math.cos(a) * r * 0.76, math.sin(a) * r * 0.76)
    cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    for ang, ln, w in ((t * 0.5, 0.42, 6), (t * 6, 0.62, 3)):
        cr.move_to(0, 0); cr.line_to(math.sin(ang) * r * ln, -math.cos(ang) * r * ln)
        cr.set_line_width(w); cr.stroke()
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha)
    cr.restore()


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


def shanty(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-240, 0); cr.line_to(-240, -230); cr.line_to(250, -250); cr.line_to(240, 0); cr.close_path()
    cr.set_source_rgb(0.60, 0.50, 0.38); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for k in range(-200, 240, 48):
        cr.move_to(k, -2); cr.line_to(k + 2, -235); cr.set_line_width(2.5); cr.set_source_rgba(*INK, 0.5); cr.stroke()
    cr.move_to(-280, -220); cr.line_to(0, -330); cr.line_to(290, -240); cr.close_path()
    cr.set_source_rgb(0.42, 0.36, 0.32); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for hx, hy in ((-120, -275), (90, -282), (180, -258)):   # holes in the roof
        cr.arc(hx, hy, 12, 0, 2 * math.pi); cr.set_source_rgb(0.15, 0.12, 0.10); cr.fill()
    cr.rectangle(-40, -150, 80, 150); cr.set_source_rgb(0.30, 0.22, 0.16); cr.fill()
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


def umbrella(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(0, 0); cr.line_to(0, 190); cr.set_source_rgb(*INK); cr.set_line_width(7); cr.stroke()
    cr.arc(-14, 190, 14, 0, math.pi); cr.stroke()
    cr.move_to(-150, 20); cr.curve_to(-150, -110, 150, -110, 150, 20)
    for k in range(5, -1, -1):
        xx = -150 + k * 60
        cr.curve_to(xx + 45, 0, xx + 15, 0, xx, 20) if False else cr.line_to(xx, 20)
    cr.close_path(); cr.set_source_rgb(0.15, 0.15, 0.20); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.restore()


def rain(cr, t, alpha=1.0):
    if alpha <= 0:
        return
    rng = random.Random(3)
    cr.set_source_rgba(0.45, 0.55, 0.75, 0.55 * alpha); cr.set_line_width(4); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(90):
        x0 = rng.uniform(0, W + 200); sp = rng.uniform(900, 1300); ph = rng.uniform(0, 2)
        yy = ((t + ph) * sp) % (H + 100) - 50
        xx = x0 - yy * 0.18
        cr.move_to(xx, yy); cr.line_to(xx - 8, yy + 40); cr.stroke()


def field(cr, sky=(0.84, 0.90, 0.97), night=False):
    if night:
        bg(cr, *NIGHT)
        rng = random.Random(5)
        for k in range(40):
            cr.arc(rng.uniform(0, W), rng.uniform(0, 600), rng.uniform(1.5, 3.5), 0, 2 * math.pi)
            cr.set_source_rgba(1, 1, 0.9, 0.8); cr.fill()
        cr.arc(1650, 170, 60, 0, 2 * math.pi); cr.set_source_rgb(0.98, 0.95, 0.80); cr.fill()
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.22, 0.26, 0.20); cr.fill()
    else:
        bg(cr, sky, (0.96, 0.92, 0.84))
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.70, 0.56, 0.40); cr.fill()
    cr.move_to(0, 880); cr.line_to(W, 880); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


def brick_building(cr, x, y, w, h, p=1.0, label=None):
    """Brick hall that rises row by row with p."""
    hh = h * clamp(p)
    if hh <= 0:
        return
    cr.save(); cr.rectangle(x - w / 2, y - hh, w, hh); cr.clip()
    cr.rectangle(x - w / 2, y - h, w, h); cr.set_source_rgb(*BRICK); cr.fill()
    cr.set_source_rgba(*INK, 0.3); cr.set_line_width(2)
    for r in range(int(h / 22)):
        yy = y - r * 22; cr.move_to(x - w / 2, yy); cr.line_to(x + w / 2, yy); cr.stroke()
    for r in range(2):
        for c in range(4):
            wx = x - w / 2 + (c + 0.5) * w / 4 - 24; wy = y - h + 50 + r * 120
            cr.rectangle(wx, wy, 48, 70); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.restore()
    cr.rectangle(x - w / 2, y - hh, w, hh); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    if p >= 1:
        cr.move_to(x - w / 2 - 20, y - h); cr.line_to(x, y - h - 80); cr.line_to(x + w / 2 + 20, y - h); cr.close_path()
        cr.set_source_rgb(0.30, 0.26, 0.24); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    if label:
        text(cr, label, x, y + 52, 34, TEXT)


def pawn_shop(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-300, -480, 600, 480); cr.set_source_rgb(0.62, 0.52, 0.42); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(-250, -300, 300, 200); cr.set_source_rgb(0.86, 0.92, 0.96); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(110, -260, 110, 260); cr.set_source_rgb(*WOOD_DK); cr.fill_preserve(); cr.stroke()
    rounded_rect(cr, -240, -450, 480, 100, 12); cr.set_source_rgb(*PAPER); cr.fill_preserve(); cr.stroke()
    cr.restore()
    text(cr, "PAWN SHOP", x, y - 382 * s, 60 * s, TEXT)
    for k, dx in enumerate((-60, 0, 60)):   # three-ball pawn sign
        cr.arc(x + 330 * s + dx * 0.5 * s, y - 420 * s + (k % 2) * 50 * s, 26 * s, 0, 2 * math.pi)
        cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()


# ================= SCENES
def s0(cr, t):  # hook: three kilns failed; Washington pawned his watch to try again
    i = 0; a, b = scene_bounds(i)
    tw = beat(i, "So Booker")
    if t < tw:
        field(cr)
        for k, kx in enumerate((520, 1000, 1480)):
            pk = prog(t, a + 0.1 + k * 0.25, 0.4)
            if pk > 0:
                kiln(cr, kx, 880, 0.9 * back_out(pk), fire=0.0)
                x_mark(cr, kx, 760, prog(t, beat(i, "failed") + k * 0.2, 0.4), r=80)
        pop_text(cr, "3 KILNS. 3 FAILURES.", W / 2, 170, 96, t, beat(i, "Three"), color=MAROON, outline=(1, 1, 1))
        bo(cr, 230, 1060, 0.34, t, pose="shrug", wide=0.9, brow=0.8, talk=False)
    else:
        bg(cr, (0.96, 0.92, 0.84), (0.90, 0.84, 0.74))
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.70, 0.56, 0.40); cr.fill()
        pw = prog(t, tw, 0.45)
        washington(cr, 640, 1050, 1.25 * back_out(pw), t, pose="hold")
        name_tag(cr, "Booker T. Washington", None, 640, 110, prog(t, beat(i, "Booker"), 0.4), size=54)
        pp = prog(t, beat(i, "pawned"), 0.4)
        pocket_watch(cr, 640 + 150 * 1.25, 1050 - 345 * 1.25, 62, t, alpha=pp, swing=math.sin(t * 3) * 0.15)
        pop_text(cr, "PAWNED HIS WATCH", 1330, 420, 72, t, beat(i, "pawned"), color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "TO TRY AGAIN", 1330, 530, 72, t, beat(i, "try again"), color=TEXT, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s1(cr, t):  # Alabama lawmakers: $2,000, teachers only; nothing for land or buildings
    i = 1; a, b = scene_bounds(i)
    tn = beat(i, "Nothing")
    if t < tn:
        street(cr, (0.84, 0.90, 0.97))
        capitol(cr, 1300, 880, 0.8)
        for k, lx in enumerate((300, 520)):
            man(cr, lx, 1050, 0.95, t + k, suit=COATS[k], tie=MAROON, skin=SKIN_LT, hair=(0.45, 0.35, 0.25) if k else GRAY,
                pose="hold" if k else "rest", prop="ledger" if k else None)
        pop_text(cr, "ALABAMA LAWMAKERS", 470, 170, 56, t, a + 0.2, color=TEXT, outline=(1, 1, 1))
        money(cr, 1300, 200, "$2,000", prog(t, beat(i, "two thousand"), 0.45))
        pop_text(cr, "for a new Black school in Tuskegee", 1300, 360, 46, t, beat(i, "Black school"), color=TEXT, outline=(1, 1, 1))
        stamp(cr, "TEACHERS' PAY ONLY", 1300, 470, prog(t, beat(i, "only pay"), 0.4), col=MAROON, size=62)
    else:
        field(cr)
        cr.rectangle(560, 860, 800, 30); cr.set_source_rgba(0.45, 0.35, 0.25, 0.6); cr.fill()
        for k, px in enumerate((560, 1360)):
            cr.rectangle(px - 6, 760, 12, 120); cr.set_source_rgb(*WOOD_DK); cr.fill()
        pl = prog(t, beat(i, "land"), 0.35)
        if pl > 0:
            panel(cr, 360, 330, 520, 150, (1, 1, 1), r=22, alpha=pl)
            text(cr, "LAND", 620, 430, 80, TEXT, alpha=pl)
            x_mark(cr, 620, 405, prog(t, beat(i, "land") + 0.2, 0.4), r=70)
        pb = prog(t, beat(i, "buildings"), 0.35)
        if pb > 0:
            panel(cr, 1040, 330, 520, 150, (1, 1, 1), r=22, alpha=pb)
            text(cr, "BUILDINGS", 1300, 430, 76, TEXT, alpha=pb)
            x_mark(cr, 1300, 405, prog(t, beat(i, "buildings") + 0.2, 0.4), r=70)
        pop_text(cr, "NOTHING FOR...", W / 2, 200, 90, t, tn, color=MAROON, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s2(cr, t):  # Lewis Adams, formerly enslaved, pushed for it; hired Washington from Hampton, born enslaved too
    i = 2; a, b = scene_bounds(i)
    th = beat(i, "They hired")
    field(cr, (0.90, 0.92, 0.96))
    if t < th:
        pa = prog(t, a + 0.1, 0.45)
        adams(cr, 760, 1050, 1.25 * back_out(pa), t, pose="point" if t > beat(i, "helped") else "rest")
        name_tag(cr, "Lewis Adams", "had been enslaved", 760, 100, prog(t, beat(i, "Lewis"), 0.4), size=56)
        pop_text(cr, "PUSHED FOR", 1450, 380, 76, t, beat(i, "helped push"), color=TEXT, outline=(1, 1, 1))
        pop_text(cr, "THE SCHOOL", 1450, 480, 76, t, beat(i, "push for"), color=MAROON, outline=(1, 1, 1))
    else:
        adams(cr, 420, 1050, 1.0, t, pose="open")
        text(cr, "ADAMS", 420, 560, 38, TEXT, outline=(1, 1, 1))
        pw = prog(t, th, 1.1)
        washington(cr, 1700 - 520 * ease(pw), 1050, 1.15, t, pose="rest", walking=0 < pw < 1)
        name_tag(cr, "Booker T. Washington", "teacher from Hampton", 1180, 100, prog(t, beat(i, "Booker"), 0.4), size=50)
        stamp(cr, "BORN ENSLAVED TOO", 1180, 330, prog(t, beat(i, "born enslaved"), 0.4), col=MAROON, size=56, rot=-0.04)
    sceneout(cr, t, a, b)


def s3(cr, t):  # July 4, 1881: ~30 students in a shanty beside a church; student held umbrella in the rain
    i = 3; a, b = scene_bounds(i)
    tr = beat(i, "When it rained")
    if t < tr:
        field(cr, (0.86, 0.92, 0.98))
        church(cr, 1600, 880, 0.9)
        shanty(cr, 980, 880, 1.0)
        text(cr, "church", 1600, 940, 34, TEXT, alpha=prog(t, beat(i, "church"), 0.4))
        pw = prog(t, beat(i, "Washington"), 0.45)
        washington(cr, 520, 1050, 1.0 * back_out(pw), t, pose="open" if t > beat(i, "opened") else "rest")
        ps = prog(t, beat(i, "thirty"), 0.6)
        for k in range(6):
            pk = clamp(ps * 6 - k)
            if pk > 0:
                student(cr, 120 + (k % 3) * 120 if k < 3 else 1240 + (k - 3) * 115, 1060, 0.62 * back_out(pk), t + k, k)
        pop_text(cr, "JULY 4, 1881", W / 2, 150, 110, t, beat(i, "July"), color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "~30 STUDENTS", 520, 360, 64, t, beat(i, "thirty"), color=TEXT, outline=(1, 1, 1))
        pop_text(cr, "IN A SHANTY", 980, 470, 58, t, beat(i, "shanty"), color=TEXT, outline=(1, 1, 1))
    else:
        bg(cr, (0.62, 0.66, 0.74), (0.74, 0.74, 0.76))
        cr.rectangle(0, 880, W, 200); cr.set_source_rgb(0.50, 0.44, 0.36); cr.fill()
        washington(cr, 760, 1050, 1.15, t, pose="open")
        pu = prog(t, beat(i, "student held"), 0.5)
        student(cr, 1080, 1050, 1.05, t, 0, pose="point")
        if pu > 0:
            umbrella(cr, 900, 1050 - 520 * 1.1 - 40 + 200 * (1 - ease(pu)), 1.3)
        for k in range(4):
            student(cr, 1380 + k * 140, 1060, 0.6, t + k, k + 1)
        rain(cr, t, prog(t, tr, 0.4))
        pop_text(cr, "WHEN IT RAINED...", 520, 200, 76, t, tr, color=(1, 1, 1), outline=INK)
    sceneout(cr, t, a, b)


def s4(cr, t):  # students make bricks; first kiln failed, second failed, third collapsed in the night
    i = 4; a, b = scene_bounds(i)
    tf = beat(i, "Washington wrote")
    t3 = beat(i, "The third")
    if t < tf:
        field(cr)
        for k in range(3):
            student(cr, 330 + k * 300, 1050, 0.95, t + k, k, pose="hold")
            brick(cr, 330 + k * 300 + 140 * 0.95, 1050 - 340 * 0.95)
        brick_stack(cr, 1450, 880, rows=6, cols=6, p=prog(t, a + 0.3, (tf - a) * 0.9))
        pop_text(cr, "MAKE YOUR OWN BRICKS", W / 2, 170, 88, t, beat(i, "make their"), color=MAROON, outline=(1, 1, 1))
    elif t < t3:
        field(cr)
        kiln(cr, 600, 880, 1.2, fire=1.0 - prog(t, beat(i, "failed"), 0.5), t=t, label="KILN 1")
        x_mark(cr, 600, 700, prog(t, beat(i, "failed"), 0.4))
        p2 = prog(t, beat(i, "So did"), 0.4)
        if p2 > 0:
            kiln(cr, 1300, 880, 1.2 * back_out(p2), fire=1.0 - prog(t, beat(i, "second"), 0.5), t=t, label="KILN 2")
            x_mark(cr, 1300, 700, prog(t, beat(i, "second"), 0.4))
        pop_text(cr, "KILN 1 FAILED. THEN KILN 2.", W / 2, 170, 76, t, beat(i, "first"), color=MAROON, outline=(1, 1, 1))
        text(cr, "from Washington's memoir, Up From Slavery", W / 2, 240, 38, MAROON, alpha=prog(t, tf, 0.4), outline=(1, 1, 1))
    else:
        field(cr, night=True)
        pc = prog(t, beat(i, "collapsed"), 0.9)
        kiln(cr, W / 2, 880, 1.4, fire=0.8 * (1 - pc), collapse=pc, t=t, label=None)
        x_mark(cr, W / 2 + 330, 520, prog(t, beat(i, "night"), 0.4), r=70)
        pop_text(cr, "KILN 3: COLLAPSED", W / 2, 170, 90, t, beat(i, "collapsed"), color=GOLDC, outline=INK)
        pop_text(cr, "IN THE NIGHT", W / 2, 280, 64, t, beat(i, "night"), color=(1, 1, 1), outline=INK)
    sceneout(cr, t, a, b)


def s5(cr, t):  # Bo: part nobody tells you; pawned watch in Montgomery for $15; fourth try worked; watch gone
    i = 5; a, b = scene_bounds(i)
    tm = beat(i, "With no money")
    t4 = beat(i, "The fourth")
    if t < tm:
        bg(cr)
        bo(cr, 960, 1050, 0.56, t, pose="think", talk=False, brow=0.6)
        pop_text(cr, "THE PART NOBODY TELLS YOU", W / 2, 140, 84, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
    elif t < t4:
        street(cr, (0.88, 0.90, 0.96))
        pawn_shop(cr, 1300, 880, 1.0)
        washington(cr, 560, 1050, 1.15, t, pose="hold")
        pg = prog(t, beat(i, "pawned"), 0.8)
        wx = 560 + 150 * 1.15 + (1150 - 560 - 150 * 1.15) * ease(pg); wy = 1050 - 345 * 1.15 + 120 * ease(pg)
        pocket_watch(cr, wx, wy, 58, t, alpha=1.0, swing=math.sin(t * 3) * 0.12)
        pop_text(cr, "MONTGOMERY", 1300, 300, 60, t, beat(i, "Montgomery"), color=TEXT, outline=(1, 1, 1))
        money(cr, 1300, 160, "$15", prog(t, beat(i, "fifteen"), 0.45), w=300, h=150)
        pop_text(cr, "NO MONEY LEFT", 560, 160, 64, t, tm, color=MAROON, outline=(1, 1, 1))
    else:
        field(cr)
        tn = beat(i, "He never")
        if t < tn:
            kiln(cr, 760, 880, 1.3, fire=1.0, t=t, label="TRY #4")
            check_mark(cr, 1100, 620, prog(t, beat(i, "worked"), 0.5), r=90)
            brick_stack(cr, 1450, 880, rows=5, cols=5, p=prog(t, beat(i, "worked"), 1.2))
            pop_text(cr, "THE FOURTH TRY WORKED", W / 2, 170, 90, t, t4, color=(0.15, 0.50, 0.25), outline=(1, 1, 1))
            student(cr, 260, 1050, 0.85, t, 2, pose="open")
        else:
            washington(cr, 760, 1050, 1.15, t, pose="rest")
            pocket_watch(cr, 1250, 520, 90, t, alpha=1 - prog(t, beat(i, "again"), 0.9))
            pop_text(cr, "NEVER SAW IT AGAIN", 1250, 230, 76, t, tn, color=MAROON, outline=(1, 1, 1))
    sceneout(cr, t, a, b)


def s6(cr, t):  # students raised buildings with own bricks; 1915: ~1,500 students, 100+ buildings; outro
    i = 6; a, b = scene_bounds(i)
    td = beat(i, "When Washington")
    tq = beat(i, "Which")
    if t < td:
        field(cr, (0.86, 0.92, 0.98))
        brick_building(cr, 1250, 880, 820, 420, p=prog(t, a + 0.2, td - a - 0.4))
        for k in range(3):
            student(cr, 220 + k * 170, 1050, 0.8, t + k, k, pose="hold")
            brick(cr, 220 + k * 170 + 140 * 0.8, 1050 - 340 * 0.8)
        pop_text(cr, "BUILT WITH THEIR OWN BRICKS", W / 2, 150, 76, t, beat(i, "bricks they"), color=MAROON, outline=(1, 1, 1))
    elif t < tq:
        field(cr, (0.86, 0.92, 0.98))
        for k, (bx, bw, bh) in enumerate(((330, 460, 300), (960, 560, 380), (1600, 460, 320))):
            brick_building(cr, bx, 880, bw, bh, p=1.0)
        washington(cr, 1305, 1060, 0.75, t, pose="open")
        pop_text(cr, "1915", 330, 160, 120, t, beat(i, "nineteen"), color=MAROON, outline=(1, 1, 1))
        ps = prog(t, beat(i, "fifteen hundred"), 0.4)
        if ps > 0:
            panel(cr, 540, 60, 640, 140, MAROON, r=24, alpha=ps)
            text(cr, "~1,500 STUDENTS", 860, 155, 60, GOLDC, alpha=ps)
        pb = prog(t, beat(i, "over one"), 0.4)
        if pb > 0:
            panel(cr, 1220, 60, 560, 140, MAROON, r=24, alpha=pb)
            text(cr, "100+ BUILDINGS", 1500, 155, 58, GOLDC, alpha=pb)
    else:
        bg(cr)
        bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=False)
        brick_stack(cr, 1250, 330, rows=3, cols=5, p=1.0)
        text(cr, "Which HBCU founder", 1250, 470, 70, TEXT, alpha=prog(t, tq, 0.4))
        text(cr, "should we cover next?", 1250, 560, 66, MAROON, alpha=prog(t, tq, 0.4))
        pop_text(cr, "Tell us in the comments", 1250, 720, 56, t, beat(i, "Tell us"))
        k = max(0, (t - (b - 0.8)) / 0.8)
        if k > 0:
            cr.set_source_rgba(*BG, k); cr.paint()
        sceneout(cr, t, a, 1e9)
        return
    sceneout(cr, t, a, b)


def thumb_hero(cr, x, y, r):
    """Hero object: Washington's pocket watch."""
    pocket_watch(cr, x, y + r * 0.15, r * 0.8, 1.3)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
