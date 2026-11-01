"""Ep04 scenes: the Fisk Jubilee Singers (1871) sing their school out of debt.
One function per narration paragraph, timed with beat(i, "phrase")."""
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


def singers(cr, cx, y, s, t, pose="rest", pose_to=None, pose_t=0.0, walking=False, appear=None, gap=150):
    """The nine original singers: five women and four men, alternating."""
    order = ["w", "m", "w", "m", "w", "m", "w", "m", "w"]
    x0 = cx - gap * s * 4
    wi = mi = 0
    for k, kind in enumerate(order):
        q = 1.0 if appear is None else prog(t, appear + k * 0.09, 0.35)
        if q <= 0:
            if kind == "w":
                wi += 1
            else:
                mi += 1
            continue
        x = x0 + k * gap * s
        yy = y - (0 if k % 2 == 0 else 0)
        sc = s * (0.92 if kind == "w" else 0.86) * back_out(q)
        if kind == "w":
            woman(cr, x, yy, sc, t + k * 0.37, dress=DRESSES[wi % 5], pose=pose, pose_to=pose_to, pose_t=pose_t,
                  walking=walking)
            wi += 1
        else:
            man(cr, x, yy, sc, t + k * 0.37, suit=COATS[mi % 4], tie=(0.9, 0.9, 0.9), pose=pose, pose_to=pose_to,
                pose_t=pose_t, walking=walking)
            mi += 1


def note(cr, x, y, s=1.0, col=GOLDC, alpha=1.0, double=False):
    if alpha <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.save(); cr.translate(0, 0); cr.rotate(-0.4); cr.scale(1.3, 1); cr.arc(0, 0, 14, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgba(*col, alpha); cr.fill_preserve(); cr.set_source_rgba(*INK, alpha); cr.set_line_width(3); cr.stroke()
    cr.move_to(16, -4); cr.line_to(16, -70)
    if double:
        cr.line_to(62, -82); cr.line_to(62, -16)
        cr.stroke()
        cr.save(); cr.translate(46, -12); cr.rotate(-0.4); cr.scale(1.3, 1); cr.arc(0, 0, 14, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgba(*col, alpha); cr.fill_preserve(); cr.set_source_rgba(*INK, alpha); cr.stroke()
    else:
        cr.curve_to(30, -50, 44, -48, 40, -24); cr.set_line_width(5); cr.stroke()
    cr.restore()


def notes_rise(cr, x, y, t, start, n=6, spread=700, s=1.0):
    if t < start:
        return
    for k in range(n):
        ph = ((t - start) * 0.45 + k / n) % 1.0
        nx = x - spread / 2 + (k * 137) % spread + math.sin(t * 2 + k) * 20
        ny = y - ph * 380
        a = clamp((t - start) / 0.5) * math.sin(math.pi * ph)
        note(cr, nx, ny, s * (0.9 + 0.3 * (k % 2)), alpha=a, double=k % 3 == 0)


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


def barracks(cr, cx, gy, s=1.0, t=0.0):
    """Long, worn wooden army barracks with crooked boards and a sagging roof."""
    cr.save(); cr.translate(cx, gy); cr.scale(s, s)
    cr.rectangle(-420, -230, 840, 230); cr.set_source_rgb(*WOOD); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for k in range(-400, 420, 42):
        cr.move_to(k, -230); cr.line_to(k + (3 if k % 84 else -4), 0)
    cr.set_source_rgba(*WOOD_DK, 0.8); cr.set_line_width(3); cr.stroke()
    cr.move_to(-450, -225); cr.curve_to(-150, -300, 120, -275, 450, -228); cr.line_to(420, -230); cr.line_to(-420, -230)
    cr.close_path(); cr.set_source_rgb(*WOOD_DK); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for k, wx in enumerate((-320, -160, 160, 320)):
        cr.save(); cr.translate(wx, -130); cr.rotate((-1) ** k * 0.05)
        cr.rectangle(-40, -40, 80, 70); cr.set_source_rgb(0.30, 0.26, 0.22); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
        cr.move_to(-40, -5); cr.line_to(40, -5); cr.move_to(0, -40); cr.line_to(0, 30); cr.stroke()
        cr.restore()
    cr.save(); cr.translate(0, -100); cr.rotate(0.03)
    cr.rectangle(-45, 0, 90, 100); cr.set_source_rgb(*WOOD_DK); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()
    for (px, py, rot) in ((-260, -60, 0.4), (250, -190, -0.3)):  # loose boards
        cr.save(); cr.translate(px, py); cr.rotate(rot); cr.rectangle(-60, -9, 120, 18)
        cr.set_source_rgb(0.72, 0.58, 0.40); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.restore()
    cr.restore()


def money_bag(cr, x, y, s=1.0, label="$", col=(0.20, 0.45, 0.20)):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-30, -110); cr.line_to(30, -110); cr.line_to(18, -80); cr.line_to(-18, -80); cr.close_path()
    cr.set_source_rgb(0.72, 0.58, 0.38); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.arc(0, -20, 70, 0, 2 * math.pi); cr.set_source_rgb(0.80, 0.66, 0.44); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.stroke()
    text(cr, label, 0, 6, 70, col)
    cr.restore()


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


def calendar(cr, x, y, s, l1, l2, l3=None, alpha=1.0):
    if alpha <= 0:
        return
    cr.save(); cr.push_group(); cr.translate(x, y); cr.scale(s, s)
    panel(cr, -170, -190, 340, 380, (1, 1, 1), r=24)
    rounded_rect(cr, -170, -190, 340, 110, 24); cr.set_source_rgb(*MAROON); cr.fill()
    cr.rectangle(-170, -110, 340, 30); cr.fill()
    for dx in (-90, 90):
        cr.rectangle(dx - 10, -215, 20, 55); cr.set_source_rgb(*INK); cr.fill()
    text(cr, l1, 0, -112, 58, GOLDC)
    text(cr, l2, 0, 60, 170, TEXT)
    if l3:
        text(cr, l3, 0, 150, 56, MAROON)
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha); cr.restore()


def chairs(cr, x0, y, n, filled, t):
    """Rows of concert chairs; `filled` = indexes with a listener."""
    for k in range(n):
        r, c = divmod(k, 8)
        cx = x0 + c * 130 + r * 40; cy = y + r * 90
        cr.rectangle(cx - 30, cy - 70, 60, 12); cr.rectangle(cx - 30, cy - 120, 10, 60)
        cr.set_source_rgb(*WOOD_DK); cr.fill()
        cr.move_to(cx - 26, cy - 58); cr.line_to(cx - 26, cy); cr.move_to(cx + 26, cy - 58); cr.line_to(cx + 26, cy)
        cr.set_line_width(6); cr.stroke()
        if k in filled:
            cr.arc(cx, cy - 150, 26, 0, 2 * math.pi); cr.set_source_rgb(*BROWN); cr.fill()
            rounded_rect(cr, cx - 28, cy - 125, 56, 60, 12); cr.set_source_rgb(*NAVY); cr.fill()


def white_house(cr, cx, gy, s=1.0):
    """Generic white columned mansion (stylized)."""
    cr.save(); cr.translate(cx, gy); cr.scale(s, s)
    cr.rectangle(-460, -300, 920, 300); cr.set_source_rgb(0.97, 0.97, 0.96); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-190, -330); cr.line_to(0, -430); cr.line_to(190, -330); cr.close_path()
    cr.set_source_rgb(0.97, 0.97, 0.96); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-200, -340, 400, 40); cr.set_source_rgb(0.92, 0.92, 0.90); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for k in range(6):
        cr.rectangle(-175 + k * 66, -300, 22, 300); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    for side in (-1, 1):
        for r in range(2):
            for c in range(3):
                wx = side * (260 + c * 70) - 20; wy = -260 + r * 120
                cr.rectangle(wx, wy, 40, 70); cr.set_source_rgb(0.55, 0.68, 0.80); cr.fill_preserve()
                cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.move_to(-14, -460); cr.line_to(-14, -430); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.restore()


def palace(cr, cx, gy, s=1.0):
    """Generic stone palace with flags (stylized, no real building)."""
    cr.save(); cr.translate(cx, gy); cr.scale(s, s)
    cr.rectangle(-480, -280, 960, 280); cr.set_source_rgb(0.86, 0.82, 0.74); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for k in range(-480, 480, 40):
        cr.rectangle(k, -300, 22, 20)
    cr.set_source_rgb(0.86, 0.82, 0.74); cr.fill()
    for r in range(2):
        for c in range(10):
            cr.rectangle(-440 + c * 92, -240 + r * 115, 40, 70); cr.set_source_rgb(0.40, 0.46, 0.58); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    for fx in (-300, 300):
        cr.move_to(fx, -300); cr.line_to(fx, -420); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
        cr.rectangle(fx, -420, 80, 50); cr.set_source_rgb(*MAROON); cr.fill()
    cr.restore()


def jubilee_hall(cr, cx, gy, s=1.0, build=1.0):
    """Tall red-brick Victorian Gothic hall with a centre tower and pointed windows (stylized).
    build in 0..1 raises it floor by floor."""
    if build <= 0:
        return
    cr.save(); cr.translate(cx, gy); cr.scale(s, s)
    top = -560 * ease(build)
    cr.save(); cr.rectangle(-600, top - 260, 1200, -top + 262); cr.clip()
    brick = (0.66, 0.30, 0.24)
    cr.rectangle(-380, -470, 760, 470); cr.set_source_rgb(*brick); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(-90, -620, 180, 620); cr.set_source_rgb(0.60, 0.26, 0.21); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-110, -620); cr.line_to(0, -760); cr.line_to(110, -620); cr.close_path()
    cr.set_source_rgb(0.30, 0.30, 0.34); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-400, -470); cr.line_to(-300, -540); cr.line_to(300, -540); cr.line_to(400, -470); cr.close_path()
    cr.set_source_rgb(0.30, 0.30, 0.34); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()

    def gothic(wx, wy, w=40, h=70):
        cr.move_to(wx - w / 2, wy + h); cr.line_to(wx - w / 2, wy + w / 2); cr.line_to(wx, wy - 4)
        cr.line_to(wx + w / 2, wy + w / 2); cr.line_to(wx + w / 2, wy + h); cr.close_path()
        cr.set_source_rgb(0.98, 0.88, 0.60); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    for r in range(5):
        for c in range(6):
            wx = -330 + c * 52 if c < 3 else 330 - (5 - c) * 52
            gothic(wx + (0 if c < 3 else 0), -450 + r * 88)
            gothic(-wx, -450 + r * 88)
    for r in range(5):
        gothic(0, -590 + r * 100, 50, 76)
    cr.rectangle(-36, -100, 72, 100); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()
    cr.restore()


def badge(cr, x, y, r, l1, l2, p):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(back_out(p), back_out(p)); cr.rotate(-0.08)
    n = 16
    for k in range(n * 2):
        a = k / (n * 2) * 2 * math.pi
        rr = r if k % 2 == 0 else r * 0.88
        cr.line_to(math.cos(a) * rr, math.sin(a) * rr)
    cr.close_path(); cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.arc(0, 0, r * 0.76, 0, 2 * math.pi); cr.set_source_rgb(*MAROON); cr.fill()
    text(cr, l1, 0, -8, r * 0.24, GOLDC)
    text(cr, l2, 0, r * 0.26, r * 0.24, (1, 1, 1))
    cr.restore()


def broken_chain(cr, x, y, s, p):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    sep = 60 * ease(p)
    for side in (-1, 1):
        for k in range(3):
            cx = side * (sep + 50 + k * 70)
            cr.save(); cr.translate(cx, 0); cr.scale(1.4 if k % 2 == 0 else 1, 0.8 if k % 2 == 0 else 1.2)
            cr.arc(0, 0, 26, 0, 2 * math.pi); cr.restore()
            cr.set_source_rgb(0.45, 0.45, 0.50); cr.set_line_width(14); cr.stroke()
    cr.restore()


# ================= SCENES
def s0(cr, t):  # hook: 1871, an HBCU about to close; nine students saved it with their voices
    i = 0
    a, b = scene_bounds(i)
    tn = beat(i, "Nine students")
    p1 = 1 - prog(t, tn - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.80, 0.80, 0.82), BG2)
        ground(cr, 900, (0.72, 0.68, 0.60))
        pop_text(cr, "1871", 360, 330, 200, t, a + 0.15, color=MAROON, outline=(1, 1, 1))
        barracks(cr, 1200, 900, 0.95, t)
        pc = prog(t, beat(i, "about to close"), 0.4)
        if pc > 0:
            cr.save(); cr.translate(1200, 560); cr.rotate(-0.06); cr.scale(back_out(pc), back_out(pc))
            rounded_rect(cr, -230, -70, 460, 120, 14); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
            cr.set_source_rgb(*RED); cr.set_line_width(10); cr.stroke()
            text(cr, "CLOSING?", 0, 22, 78, RED)
            cr.restore()
        pop_text(cr, "an HBCU", 360, 470, 80, t, beat(i, "H. B. C. U."), color=TEXT)
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    pb = prog(t, beat(i, "about to close"), 0.4) * (1 - prog(t, tn - 0.1, 0.3))
    if pb > 0:
        cr.save(); cr.push_group()
        bo(cr, 260, 1080, 0.22, t, pose="shrug", wide=0.9, brow=1.0)
        cr.pop_group_to_source(); cr.paint_with_alpha(pb); cr.restore()
    p2 = prog(t, tn, 0.4)
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 900, (0.86, 0.80, 0.70))
        tv = beat(i, "their voices.")
        singers(cr, W / 2, 905, 0.95, t, pose="rest", pose_to="sing", pose_t=prog(t, tv - 0.6, 0.5), appear=tn)
        pop_text(cr, "9 STUDENTS", W / 2, 170, 100, t, tn + 0.1, color=MAROON, outline=(1, 1, 1))
        notes_rise(cr, W / 2, 420, t, tv - 0.6, n=9, spread=1300)
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    fade_edges(cr, t, a, b)


def s1(cr, t):  # Fisk University, Nashville; deep in debt; classes in old Union Army barracks
    i = 1
    a, b = scene_bounds(i)
    td = beat(i, "It was deep")
    tc = beat(i, "and classes")
    p1 = 1 - prog(t, td - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 900, (0.80, 0.74, 0.62))
        pop_text(cr, "FISK UNIVERSITY", W / 2, 330, 120, t, beat(i, "Fisk University"), color=FISK_BLUE, outline=(1, 1, 1))
        pop_text(cr, "Nashville, Tennessee", W / 2, 450, 64, t, beat(i, "Nashville"), color=MAROON)
        for k in range(5):
            kid(cr, 560 + k * 200, 905, 1.6, dress=(FISK_BLUE, MAROON, PURPLE, NAVY, GREEN)[k], girl=k % 2 == 0, t=t + k)
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, td, 0.4) * (1 - prog(t, tc - 0.1, 0.35))
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.92, 0.90, 0.86), BG2)
        money_bag(cr, W / 2, 640, 2.4, label="$", col=(0.2, 0.2, 0.2))
        stamp(cr, "DEEP IN DEBT", W / 2, 300, prog(t, beat(i, "debt,"), 0.35), size=90)
        for k in range(5):
            q = prog(t, td + 0.15 + k * 0.08, 0.4)
            if q > 0:
                cr.save(); cr.translate(380 + k * 300 + (0 if k < 2 else 280) * 0, 830 + (k % 2) * 40)
                cr.rotate((k - 2) * 0.12); cr.scale(back_out(q), back_out(q))
                cr.rectangle(-70, -45, 140, 90); cr.set_source_rgb(*PAPER); cr.fill_preserve()
                cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
                text(cr, "IOU", 0, 16, 44, RED)
                cr.restore()
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    p3 = prog(t, tc, 0.4)
    if p3 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.82, 0.82, 0.84), BG2)
        ground(cr, 900, (0.72, 0.68, 0.60))
        barracks(cr, 1080, 900, 1.25, t)
        kicker(cr, "OLD UNION ARMY BARRACKS", t, beat(i, "Union Army"))
        for k in range(3):
            kid(cr, 220 + k * 110 + 160 * ease(prog(t, tc, 2.5)), 905, 1.4, dress=(FISK_BLUE, MAROON, PURPLE)[k],
                girl=k != 1, t=t + k, walking=True)
        stamp(cr, "FALLING APART", 1500, 280, prog(t, beat(i, "falling apart."), 0.35), col=MAROON, size=60, rot=0.06)
        cr.pop_group_to_source(); cr.paint_with_alpha(p3); cr.restore()
    fade_edges(cr, t, a, b)


def s2(cr, t):  # treasurer George White takes a gamble; Oct 6, 1871 nine singers hit the road; many born enslaved
    i = 2
    a, b = scene_bounds(i)
    to = beat(i, "On October")
    tm = beat(i, "Many of them")
    p1 = 1 - prog(t, to - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.95, 0.92, 0.86), BG2)
        ground(cr, 900, (0.80, 0.72, 0.60))
        man(cr, 620, 905, 1.2, t, suit=CHAR, tie=FISK_BLUE, skin=SKIN_LT, hair=(0.35, 0.25, 0.15),
            whiskers=True, pose="rest", pose_to="hold", pose_t=prog(t, beat(i, "treasurer"), 0.5), prop="ledger")
        name_tag(cr, "GEORGE L. WHITE", "Fisk treasurer", 620, 930, prog(t, beat(i, "George White"), 0.4), 46)
        pg = prog(t, beat(i, "took a gamble."), 0.4)
        if pg > 0:
            money_bag(cr, 1300, 640, 1.8 * back_out(pg))
            text(cr, "A GAMBLE", 1300, 300, 96, MAROON, alpha=pg, outline=(1, 1, 1))
            text(cr, "?", 1500, 520, 140, GOLDC, alpha=pg, outline=INK, scale=back_out(pg))
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, to, 0.4)
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 880, (0.78, 0.70, 0.52))
        cr.move_to(0, 960); cr.line_to(W, 960); cr.set_source_rgba(*WOOD_DK, 0.5); cr.set_line_width(6)
        cr.set_dash([40, 30]); cr.stroke(); cr.set_dash([])
        ts = beat(i, "nine student")
        walk = ease(prog(t, to, 7.0))
        singers(cr, 640 + 480 * walk, 905, 0.72, t, walking=True, appear=to + 0.1, gap=140)
        man(cr, 640 + 480 * walk - 140 * 0.72 * 5.6, 905, 0.72, t + 0.2, suit=CHAR, tie=FISK_BLUE, skin=SKIN_LT,
            hair=(0.35, 0.25, 0.15), whiskers=True, walking=True)
        pop_text(cr, "9 SINGERS", 640 + 480 * walk, 560, 70, t, ts, color=MAROON, outline=(1, 1, 1))
        calendar(cr, 1660, 330, 0.85, "OCT", "6", "1871", alpha=prog(t, to, 0.4) * (1 - prog(t, tm - 0.1, 0.35)))
        pm = prog(t, tm, 0.4)
        if pm > 0:
            panel(cr, 1210, 170, 640, 220, (1, 1, 1), alpha=pm)
            text(cr, "Many were born", 1530, 255, 56, TEXT, alpha=pm)
            text(cr, "into slavery", 1530, 335, 56, MAROON, alpha=pm)
            broken_chain(cr, 400, 230, 0.9, prog(t, beat(i, "slavery."), 0.6))
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    fade_edges(cr, t, a, b)


def s3(cr, t):  # small crowds; renamed the Jubilee Singers (year of jubilee); they sing spirituals
    i = 3
    a, b = scene_bounds(i)
    tn = beat(i, "So White gave")
    tb = beat(i, "after the Bible's")
    ts = beat(i, "And they sang")
    p1 = 1 - prog(t, tn - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.86, 0.84, 0.80), BG2)
        cr.rectangle(0, 620, W, 460); cr.set_source_rgb(0.80, 0.72, 0.58); cr.fill()
        chairs(cr, 260, 760, 24, {3, 10, 17}, t)
        pop_text(cr, "SMALL CROWDS", W / 2, 260, 110, t, beat(i, "the crowds"), color=MAROON, outline=(1, 1, 1))
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, tn, 0.4) * (1 - prog(t, tb - 0.1, 0.35))
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 900, (0.86, 0.80, 0.70))
        man(cr, 300, 905, 1.0, t, suit=CHAR, tie=FISK_BLUE, skin=SKIN_LT, hair=(0.35, 0.25, 0.15), whiskers=True,
            pose="rest", pose_to="point", pose_t=prog(t, tn, 0.5))
        text(cr, "GEORGE L. WHITE", 300, 980, 38, MAROON)
        pj = prog(t, beat(i, "the Jubilee Singers,"), 0.5)
        if pj > 0:
            cr.save(); cr.translate(1150, 450); cr.scale(back_out(pj), back_out(pj))
            panel(cr, -520, -200, 1040, 400, PAPER, r=20, lw=6)
            text(cr, "THE", 0, -90, 60, TEXT)
            text(cr, "JUBILEE", 0, 30, 150, MAROON)
            text(cr, "SINGERS", 0, 140, 96, FISK_BLUE)
            cr.restore()
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    p3 = prog(t, tb, 0.4) * (1 - prog(t, ts - 0.1, 0.35))
    if p3 > 0:
        cr.save(); cr.push_group()
        bg(cr, BG, BG2)
        cr.save(); cr.translate(W / 2 - 360, 560)
        panel(cr, -300, -260, 600, 520, PAPER, r=20)
        text(cr, "THE YEAR OF", 0, -150, 56, TEXT)
        text(cr, "JUBILEE", 0, -60, 110, MAROON)
        text(cr, "Leviticus 25", 0, 30, 48, TEXT)
        cr.set_source_rgba(*INK, 0.3); cr.set_line_width(4)
        for k in range(3):
            cr.move_to(-220, 100 + k * 40); cr.line_to(220 - (k % 2) * 60, 100 + k * 40)
        cr.stroke(); cr.restore()
        pf = prog(t, beat(i, "set free."), 0.5)
        broken_chain(cr, 1400, 520, 1.3, prog(t, beat(i, "when the enslaved"), 1.0))
        pop_text(cr, "SET FREE", 1400, 760, 110, t, beat(i, "set free."), color=GOLDC, outline=INK)
        cr.pop_group_to_source(); cr.paint_with_alpha(p3); cr.restore()
    p4 = prog(t, ts, 0.4)
    if p4 > 0:
        cr.save(); cr.push_group()
        g = cairo.RadialGradient(W / 2, 420, 50, W / 2, 420, 1100)
        g.add_color_stop_rgb(0, 0.98, 0.88, 0.62); g.add_color_stop_rgb(1, 0.33, 0.07, 0.11)
        cr.set_source(g); cr.paint()
        cr.rectangle(0, 900, W, 180); cr.set_source_rgb(*WOOD_DK); cr.fill()
        singers(cr, W / 2, 905, 0.95, t, pose="sing")
        notes_rise(cr, W / 2, 440, t, ts, n=10, spread=1400)
        pop_text(cr, "SPIRITUALS", W / 2, 150, 100, t, beat(i, "spirituals"), color=GOLDC, outline=INK)
        cr.pop_group_to_source(); cr.paint_with_alpha(p4); cr.restore()
    fade_edges(cr, t, a, b)


def s4(cr, t):  # It worked: 1872 President Grant at the White House; 1873 Queen Victoria in England
    i = 4
    a, b = scene_bounds(i)
    tg = beat(i, "In eighteen seventy-two")
    tq = beat(i, "The next year")
    p0 = 1 - prog(t, tg - 0.05, 0.3)
    if p0 > 0:
        cr.save(); cr.push_group()
        bg(cr, MAROON_DK, MAROON)
        pop_text(cr, "IT WORKED.", W / 2, 600, 190, t, a + 0.1, color=GOLDC, outline=INK)
        cr.pop_group_to_source(); cr.paint_with_alpha(p0); cr.restore()
    p1 = prog(t, tg, 0.3) * (1 - prog(t, tq - 0.1, 0.35))
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.80, 0.88, 0.96), (0.94, 0.95, 0.96))
        ground(cr, 900, (0.55, 0.70, 0.45))
        white_house(cr, 1250, 900, 0.95)
        text(cr, "1872", 140, 170, 100, MAROON, align="left")
        tp = beat(i, "President Ulysses")
        man(cr, 520, 905, 1.15, t, suit=(0.12, 0.12, 0.16), tie=(0.12, 0.12, 0.16), skin=SKIN_LT,
            hair=(0.30, 0.20, 0.12), beard=(0.30, 0.20, 0.12), pose="rest", pose_to="open", pose_t=prog(t, tp + 0.6, 0.5))
        name_tag(cr, "ULYSSES S. GRANT", "U.S. president", 520, 930, prog(t, tp, 0.4), 44)
        singers(cr, 1250, 905, 0.5, t, pose="sing", gap=130)
        notes_rise(cr, 1250, 640, t, tg + 0.4, n=6, spread=600, s=0.8)
        pop_text(cr, "THE WHITE HOUSE", 1250, 300, 64, t, beat(i, "the White House."), color=NAVY)
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, tq, 0.4)
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.84, 0.86, 0.90), (0.94, 0.93, 0.90))
        ground(cr, 900, (0.55, 0.66, 0.48))
        palace(cr, 1250, 900, 0.9)
        text(cr, "1873", 140, 170, 100, MAROON, align="left")
        pop_text(cr, "ENGLAND", 1250, 300, 64, t, beat(i, "in England,"), color=NAVY)
        tv = beat(i, "Queen Victoria.")
        woman(cr, 520, 905, 1.15, t, dress=(0.08, 0.08, 0.10), skin=SKIN_LT, hair=(0.35, 0.28, 0.22),
              crown=True, veil=True)
        name_tag(cr, "QUEEN VICTORIA", "of Britain", 520, 930, prog(t, tv, 0.4), 44)
        singers(cr, 1250, 905, 0.5, t, pose="sing", gap=130)
        notes_rise(cr, 1250, 640, t, tq + 0.3, n=6, spread=600, s=0.8)
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    fade_edges(cr, t, a, b)


def s5(cr, t):  # part most people never hear: the money built Jubilee Hall; landmark; Jubilee Day every Oct 6
    i = 5
    a, b = scene_bounds(i)
    tm = beat(i, "The money")
    tl = beat(i, "It still stands")
    td = beat(i, "And every October")
    p0 = prog(t, a + 0.1, 0.4) * (1 - prog(t, tm - 0.1, 0.35))
    if p0 > 0:
        cr.save(); cr.push_group()
        bg(cr)
        bo(cr, 960, 1020, 0.55, t, pose="think", wide=0.6, brow=0.8)
        text(cr, "The part most people never hear...", W / 2, 180, 70, MAROON)
        cr.pop_group_to_source(); cr.paint_with_alpha(p0); cr.restore()
    p1 = prog(t, tm, 0.4) * (1 - prog(t, td - 0.1, 0.35))
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 940, (0.55, 0.70, 0.45))
        tb = beat(i, "built Jubilee Hall")
        pm = prog(t, tm, 0.4) * (1 - prog(t, tb + 0.4, 0.5))
        jubilee_hall(cr, 1060, 942, 0.95, prog(t, tb, 1.6))
        if pm > 0:
            cr.push_group()
            for k in range(3):
                money_bag(cr, 300 + k * 180 + 400 * ease(prog(t, tb - 0.2, 0.8)), 860 - 300 * ease(prog(t, tb - 0.2, 0.8)),
                          1.0 * (1 - 0.6 * ease(prog(t, tb, 0.6))))
            cr.pop_group_to_source(); cr.paint_with_alpha(pm)
        name_tag(cr, "JUBILEE HALL", "Fisk's first permanent building", 1060, 140,
                 prog(t, beat(i, "first permanent"), 0.4) * (1 - prog(t, tl - 0.1, 0.3)), 50)
        badge(cr, 1600, 330, 190, "NATIONAL", "LANDMARK", prog(t, beat(i, "National Historic"), 0.5))
        pop_text(cr, "STILL STANDING", 420, 250, 76, t, beat(i, "still stands"), color=MAROON, outline=(1, 1, 1))
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, td, 0.4)
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.95, 0.90, 0.80), BG2)
        calendar(cr, 560, 560, 1.15, "OCTOBER", "6", "every year")
        pop_text(cr, "JUBILEE", 1320, 480, 150, t, beat(i, "Jubilee Day."), color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "DAY", 1320, 650, 150, t, beat(i, "Jubilee Day.") + 0.15, color=GOLDC, outline=INK)
        notes_rise(cr, 1320, 900, t, td + 0.3, n=6, spread=700, s=0.8)
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    fade_edges(cr, t, a, b)


def s6(cr, t):  # outro: still singing; which HBCU choir or band next? (Bo hosts)
    i = 6
    a, b = scene_bounds(i)
    tq = beat(i, "Which H. B. C. U.")
    p1 = 1 - prog(t, tq - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        g = cairo.RadialGradient(W / 2, 420, 50, W / 2, 420, 1100)
        g.add_color_stop_rgb(0, 0.98, 0.88, 0.62); g.add_color_stop_rgb(1, 0.18, 0.30, 0.58)
        cr.set_source(g); cr.paint()
        cr.rectangle(0, 900, W, 180); cr.set_source_rgb(*WOOD_DK); cr.fill()
        singers(cr, W / 2, 905, 0.95, t, pose="sing")
        notes_rise(cr, W / 2, 440, t, a, n=10, spread=1400)
        pop_text(cr, "STILL SINGING", W / 2, 170, 110, t, beat(i, "still singing."), color=GOLDC, outline=INK)
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, tq, 0.4)
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr)
        bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5),
           talk=t < P[i][1])
        text(cr, "Which HBCU", 1220, 330, 80, TEXT)
        text(cr, "choir or band", 1220, 440, 80, MAROON)
        text(cr, "should we cover next?", 1220, 540, 64, TEXT)
        pop_text(cr, "Tell us in the comments", 1220, 680, 56, t, beat(i, "Tell us"))
        pop_text(cr, "THE YARD", 1220, 830, 90, t, beat(i, "Tell us") + 0.5, color=GOLDC, outline=INK)
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    else:
        k0 = 1 - clamp((t - a) / 0.3)
        if k0 > 0:
            cr.set_source_rgba(*BG, k0 * 0.9); cr.paint()


def thumb_hero(cr, x, y, r):
    """Hero object for thumbnails: one big gold music note."""
    s = r / 62.0
    cr.save(); cr.translate(x - 25 * s, y + 39 * s)
    cr.scale(s, s)
    cr.save(); cr.rotate(-0.4); cr.scale(1.3, 1); cr.arc(0, 0, 16, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.save(); cr.translate(48, -10); cr.rotate(-0.4); cr.scale(1.3, 1); cr.arc(0, 0, 16, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(14, -82, 8, 80); cr.rectangle(62, -94, 8, 82)
    cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(2); cr.stroke()
    cr.move_to(14, -82); cr.line_to(70, -94); cr.line_to(70, -78); cr.line_to(14, -66); cr.close_path()
    cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


SCENES = [s0, s1, s2, s3, s4, s5, s6]
