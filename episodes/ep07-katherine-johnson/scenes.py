"""Ep07 scenes: Katherine Johnson (West Virginia State, NASA). One function per narration paragraph, timed with beat(i, phrase)."""
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


WV_GOLD = GOLDC                    # West Virginia State colours (old gold and black); no logos or seals
KJ_DRESS = (0.20, 0.32, 0.52)
SUIT_SILVER = (0.78, 0.80, 0.84)
SPACE = (0.07, 0.09, 0.20)
CHALK = (0.16, 0.30, 0.24)


def katherine(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0, walking=False, medal=False, cap=False):
    """Katherine Johnson: stylized woman with glasses (no mouth)."""
    woman(cr, x, y, s, t, dress=KJ_DRESS, skin=BLACK, pose=pose, pose_to=pose_to, pose_t=pose_t, walking=walking)
    bob = math.sin(t * 2.0) * 2.5 if not walking else -abs(math.sin(t * 8)) * 5
    hy = y + (-380 + bob - 4) * s
    cr.save(); cr.translate(x, hy); cr.scale(s, s)
    for dx in (-16, 16):
        cr.arc(dx, 0, 14, 0, 2 * math.pi)
        cr.set_source_rgb(*GOLDC); cr.set_line_width(4); cr.stroke()
    cr.move_to(-2, 0); cr.line_to(2, 0); cr.stroke()
    if cap:  # graduation cap
        cr.move_to(-70, -52); cr.line_to(0, -78); cr.line_to(70, -52); cr.line_to(0, -28); cr.close_path()
        cr.set_source_rgb(*BLACK); cr.fill()
        cr.move_to(55, -50); cr.line_to(62, -10); cr.set_source_rgb(*GOLDC); cr.set_line_width(4); cr.stroke()
    cr.restore()
    if medal:
        my = y + (-300 + bob) * s
        cr.move_to(x - 30 * s, y + (-330 + bob) * s); cr.line_to(x, my); cr.line_to(x + 30 * s, y + (-330 + bob) * s)
        cr.set_source_rgb(0.20, 0.30, 0.62); cr.set_line_width(10 * s); cr.stroke()
        cr.arc(x, my + 16 * s, 20 * s, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()


def astronaut(cr, x, y, s, t, pose="rest", hair=(0.45, 0.32, 0.20)):
    man(cr, x, y, s, t, suit=SUIT_SILVER, tie=(0.85, 0.20, 0.20), skin=SKIN_LT, hair=hair, pose=pose)


def chalkboard(cr, x, y, w, h, lines, p=1.0):
    panel(cr, x, y, w, h, CHALK, r=10, lw=8)
    for k, ln in enumerate(lines):
        q = clamp(p * len(lines) - k)
        if q > 0:
            text(cr, ln, x + w / 2, y + 80 + k * 70, 50, (0.95, 0.95, 0.90), alpha=q, bold=False)


def rocket(cr, x, y, s=1.0, flame=0.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    if flame > 0:
        cr.move_to(-30, 0); cr.line_to(0, 80 + 50 * flame * (0.8 + 0.2 * math.sin(flame * 40))); cr.line_to(30, 0)
        cr.close_path(); cr.set_source_rgb(1.0, 0.62, 0.15); cr.fill()
    cr.move_to(-40, 0); cr.line_to(-40, -260); cr.curve_to(-40, -330, 0, -380, 0, -380)
    cr.curve_to(0, -380, 40, -330, 40, -260); cr.line_to(40, 0); cr.close_path()
    cr.set_source_rgb(0.96, 0.96, 0.96); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for sx in (-1, 1):
        cr.move_to(sx * 40, -70); cr.line_to(sx * 80, 10); cr.line_to(sx * 40, 0); cr.close_path()
        cr.set_source_rgb(0.80, 0.18, 0.18); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.arc(0, -220, 16, 0, 2 * math.pi); cr.set_source_rgb(0.55, 0.75, 0.92); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


def earth(cr, x, y, r):
    cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(0.25, 0.50, 0.80); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for dx, dy, rr in ((-0.35, -0.2, 0.3), (0.3, 0.25, 0.25), (0.1, -0.45, 0.15)):
        cr.arc(x + dx * r, y + dy * r, rr * r, 0, 2 * math.pi); cr.set_source_rgb(0.40, 0.66, 0.36); cr.fill()


def stars(cr, t):
    rnd = random.Random(7)
    for _ in range(90):
        sx, sy = rnd.uniform(0, W), rnd.uniform(0, H); tw = 0.5 + 0.5 * math.sin(t * 3 + sx)
        cr.arc(sx, sy, rnd.uniform(1.5, 3.5), 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.4 + 0.5 * tw); cr.fill()


def space_bg(cr, t):
    cr.set_source_rgb(*SPACE); cr.paint(); stars(cr, t)


def computer_box(cr, x, y, w=420, h=520, t=0.0):
    panel(cr, x, y, w, h, (0.70, 0.72, 0.74), r=12, lw=6)
    for k in range(2):
        cx = x + w * (0.3 + 0.4 * k); cy = y + 130
        cr.arc(cx, cy, 70, 0, 2 * math.pi); cr.set_source_rgb(0.25, 0.25, 0.28); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
        a = t * (2 + k)
        cr.move_to(cx, cy); cr.line_to(cx + 55 * math.cos(a), cy + 55 * math.sin(a)); cr.set_source_rgb(0.8, 0.8, 0.8); cr.stroke()
    rnd = random.Random(int(t * 4))
    for r in range(4):
        for c in range(6):
            on = rnd.random() > 0.5
            cr.arc(x + 60 + c * (w - 120) / 5, y + 280 + r * 55, 12, 0, 2 * math.pi)
            cr.set_source_rgb(*((1.0, 0.75, 0.2) if on else (0.45, 0.45, 0.45))); cr.fill()


def desk(cr, x, y, w=420):
    cr.rectangle(x - w / 2, y, w, 26); cr.set_source_rgb(*WOOD); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    for dx in (-w / 2 + 20, w / 2 - 40):
        cr.rectangle(x + dx, y + 26, 20, 150); cr.set_source_rgb(*WOOD_DK); cr.fill()
    # desk calculator
    cr.rectangle(x - 70, y - 70, 140, 70); cr.set_source_rgb(0.30, 0.34, 0.40); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.stroke()
    for r in range(2):
        for c in range(5):
            cr.arc(x - 50 + c * 25, y - 48 + r * 26, 8, 0, 2 * math.pi); cr.set_source_rgb(0.92, 0.92, 0.88); cr.fill()
    # papers
    cr.rectangle(x + 90, y - 12, 100, 12); cr.set_source_rgb(1, 1, 1); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()


def orbit_path(cr, cx, cy, rx, ry, p, col=GOLDC):
    if p <= 0:
        return
    cr.save(); cr.translate(cx, cy); cr.scale(rx, ry)
    cr.arc(0, 0, 1, -math.pi / 2, -math.pi / 2 + 2 * math.pi * p); cr.restore()
    cr.set_source_rgb(*col); cr.set_dash([18, 14]); cr.set_line_width(6); cr.stroke(); cr.set_dash([])


# ================= SCENES
def s0(cr, t):  # hook: astronaut asks one woman to check the math; learned at an HBCU
    i = 0; a, b = scene_bounds(i)
    space_bg(cr, t)
    earth(cr, 960, 1500, 640)
    rocket(cr, 1620, 760, 0.9, flame=t)
    pk = prog(t, a + 0.2, 0.5)
    katherine(cr, 820, 1040, 1.35 * back_out(pk), t)
    pc = prog(t, beat(i, "check the math"), 0.5)
    if pc > 0:
        panel(cr, 240, 420, 420, 250, (1, 1, 1), r=20, alpha=pc)
        for k, ln in enumerate(("x = v·t", "r = 6,371 km", "✓")):
            text(cr, ln, 450, 495 + k * 70, 46, INK, alpha=pc, bold=k == 2)
    pop_text(cr, "CHECK THE MATH", W / 2, 170, 120, t, a + 0.3, color=GOLDC, outline=INK)
    pop_text(cr, "LEARNED AT AN HBCU", W / 2, 300, 76, t, beat(i, "She learned"), color=(1, 1, 1), outline=INK)
    sceneout(cr, t, a, b)


def campus(cr):
    bg(cr, (0.80, 0.86, 0.95), (0.96, 0.93, 0.84))
    cr.rectangle(0, 880, W, 200); cr.set_source_rgb(*GRASS); cr.fill()
    cr.rectangle(160, 470, 1600, 410); cr.set_source_rgb(*BRICK); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for c in range(10):
        cr.rectangle(210 + c * 155, 530, 70, 100); cr.set_source_rgb(0.98, 0.90, 0.66); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()


def s1(cr, t):  # Katherine Johnson at West Virginia State; Claytor adds courses
    i = 1; a, b = scene_bounds(i)
    campus(cr)
    pb = prog(t, beat(i, "West Virginia"), 0.4)
    if pb > 0:
        panel(cr, 360, 90, 1200, 190, BLACK, r=26, alpha=pb)
        text(cr, "WEST VIRGINIA STATE", 960, 190, 84, WV_GOLD, alpha=pb)
        text(cr, "Institute, W. Va.", 960, 255, 40, (1, 1, 1), alpha=pb)
    pk = prog(t, a + 0.2, 0.4)
    katherine(cr, 470, 1060, 1.15 * back_out(pk), t)
    name_tag(cr, "Katherine Johnson", None, 470, 320, prog(t, beat(i, "Katherine"), 0.4), size=40)
    pc = prog(t, beat(i, "W. W."), 0.4)
    if pc > 0:
        man(cr, 1450, 1060, 1.15 * back_out(pc), t, suit=(0.25, 0.22, 0.20), tie=WV_GOLD, skin=BLACK,
            pose="point" if t > beat(i, "added") else "rest")
        name_tag(cr, "Prof. W. W. Claytor", "math professor", 1450, 320, pc, size=40)
    ps = prog(t, beat(i, "new math courses"), 0.4)
    if ps > 0:
        stamp(cr, "NEW COURSES, JUST FOR HER", 960, 720, ps, col=(1, 1, 1), size=44)
    sceneout(cr, t, a, b)


def s2(cr, t):  # 1937, age 18, highest honors, math + French
    i = 2; a, b = scene_bounds(i)
    campus(cr)
    katherine(cr, 520, 1060, 1.3, t, pose="hold", cap=True)
    pop_text(cr, "1937", 1250, 230, 170, t, beat(i, "nineteen"), color=WV_GOLD, outline=INK)
    pop_text(cr, "AGE 18", 1250, 380, 100, t, beat(i, "eighteen"), color=TEXT, outline=(1, 1, 1))
    ph = prog(t, beat(i, "highest"), 0.4)
    if ph > 0:
        stamp(cr, "HIGHEST HONORS", 1250, 520, ph, col=MAROON, size=64)
    pd = prog(t, beat(i, "mathematics"), 0.4)
    if pd > 0:
        panel(cr, 980, 640, 540, 180, (1, 1, 1), r=22, alpha=pd)
        text(cr, "MATH", 1250, 715, 64, BLACK, alpha=pd)
        text(cr, "+ FRENCH", 1250, 790, 54, MAROON, alpha=prog(t, beat(i, "French"), 0.3))
    sceneout(cr, t, a, b)


def s3(cr, t):  # Langley 1953, human computer, West Area Computing; Shepard 1961
    i = 3; a, b = scene_bounds(i)
    ts = beat(i, "She worked")
    if t < ts:
        bg(cr, (0.93, 0.93, 0.90), (0.86, 0.86, 0.82))
        cr.rectangle(0, 860, W, 220); cr.set_source_rgb(0.72, 0.70, 0.66); cr.fill()
        chalkboard(cr, 1060, 400, 720, 380, ["y = v₀t − ½gt²", "θ = 32.5°", "t = 15:22"], prog(t, a, 3.0))
        desk(cr, 560, 860, 520)
        katherine(cr, 560, 1060, 1.05, t, pose="hold")
        pl = prog(t, beat(i, "Langley"), 0.4)
        if pl > 0:
            panel(cr, 140, 90, 1000, 170, MAROON, r=24, alpha=pl)
            text(cr, "LANGLEY LAB, VIRGINIA", 640, 175, 64, (1, 1, 1), alpha=pl)
            text(cr, "1953", 640, 235, 46, GOLDC, alpha=pl)
        pop_text(cr, "HUMAN COMPUTER", 1420, 320, 80, t, beat(i, "human computer"), color=TEXT, outline=(1, 1, 1))
        pw = prog(t, beat(i, "West Area"), 0.4)
        if pw > 0:
            stamp(cr, "WEST AREA COMPUTING", 1420, 860, pw, col=MAROON, size=50)
    else:
        space_bg(cr, t)
        earth(cr, 960, 1500, 640)
        pp = prog(t, ts, 2.5)
        cr.move_to(300, 900)
        cr.curve_to(600, 200, 1300, 200, 1650, 900)
        cr.set_source_rgba(*GOLDC, 0.9); cr.set_dash([18, 14]); cr.set_line_width(6); cr.stroke(); cr.set_dash([])
        u = ease(pp); bx = (1 - u) ** 3 * 300 + 3 * (1 - u) ** 2 * u * 600 + 3 * (1 - u) * u * u * 1300 + u ** 3 * 1650
        by = (1 - u) ** 3 * 900 + 3 * (1 - u) ** 2 * u * 200 + 3 * (1 - u) * u * u * 200 + u ** 3 * 900
        rocket(cr, bx, by, 0.35, flame=t)
        katherine(cr, 300, 1060, 0.85, t, pose="point")
        pa = prog(t, beat(i, "Alan"), 0.4)
        if pa > 0:
            astronaut(cr, 1600, 1060, 0.85 * back_out(pa), t)
            name_tag(cr, "Alan Shepard", "first American in space", 1600, 560, pa, size=40)
        pop_text(cr, "FLIGHT PATH", 960, 140, 100, t, beat(i, "flight path"), color=GOLDC, outline=INK)
        pop_text(cr, "1961", 960, 270, 90, t, beat(i, "nineteen sixty-one"), color=(1, 1, 1), outline=INK)
    sceneout(cr, t, a, b)


def s4(cr, t):  # Bo: part nobody hears; Glenn 1962, electronic computers, Katherine checks; 3 orbits
    i = 4; a, b = scene_bounds(i)
    tg = beat(i, "For John")
    to = beat(i, "She checked")
    if t < tg:
        bg(cr)
        bo(cr, 960, 1040, 0.62, t, pose="think", talk=True)
        pop_text(cr, "THE PART NOBODY HEARS", W / 2, 160, 90, t, a + 0.2, color=MAROON, outline=(1, 1, 1))
    elif t < to:
        bg(cr, (0.93, 0.93, 0.90), (0.86, 0.86, 0.82))
        cr.rectangle(0, 860, W, 220); cr.set_source_rgb(0.72, 0.70, 0.66); cr.fill()
        pc = prog(t, beat(i, "electronic"), 0.4)
        if pc > 0:
            computer_box(cr, 120, 340, 380, 520, t)
            text(cr, "ELECTRONIC COMPUTER", 310, 310, 34, TEXT, alpha=pc)
        astronaut(cr, 760, 1060, 1.1, t, pose="point" if t > beat(i, "Glenn still") else "rest", hair=(0.55, 0.40, 0.25))
        name_tag(cr, "John Glenn", "1962", 760, 160, prog(t, tg, 0.4), size=46)
        pk = prog(t, beat(i, "wanted Katherine"), 0.5)
        if pk > 0:
            desk(cr, 1450, 860, 460)
            katherine(cr, 1450, 1060, 1.05 * back_out(pk), t, pose="hold")
            name_tag(cr, "Katherine Johnson", None, 1450, 300, pk, size=40)
        pg = prog(t, beat(i, "If she"), 0.4)
        if pg > 0:
            stamp(cr, "CHECK THE NUMBERS", 1100, 560, prog(t, beat(i, "check their"), 0.4), col=MAROON, size=54)
            pop_text(cr, "✓ READY TO GO", 1080, 440, 70, t, beat(i, "ready to go"), color=(0.15, 0.50, 0.25), outline=(1, 1, 1))
        elif t > beat(i, "check their"):
            stamp(cr, "CHECK THE NUMBERS", 1100, 560, prog(t, beat(i, "check their"), 0.4), col=MAROON, size=54)
    else:
        space_bg(cr, t)
        earth(cr, 960, 600, 260)
        p = prog(t, to + 0.3, max(0.5, b - to - 1.2))
        n = 3 * p
        for k in range(3):
            orbit_path(cr, 960, 600, 420 + k * 40, 200 + k * 25, clamp(n - k))
        ang = -math.pi / 2 + 2 * math.pi * n; kk = min(2, int(n))
        rocket(cr, 960 + (420 + kk * 40) * math.cos(ang), 600 + (200 + kk * 25) * math.sin(ang), 0.18)
        pop_text(cr, "3 ORBITS", W / 2, 1000, 110, t, beat(i, "three times"), color=GOLDC, outline=INK)
        katherine(cr, 230, 1060, 0.75, t, pose="point")
        astronaut(cr, 1700, 1060, 0.75, t, pose="rest", hair=(0.55, 0.40, 0.25))
    sceneout(cr, t, a, b)


def s5(cr, t):  # 2015 Medal of Freedom; lived to 101
    i = 5; a, b = scene_bounds(i)
    bg(cr, (0.94, 0.92, 0.98), (0.88, 0.86, 0.94))
    pm = t > beat(i, "Presidential")
    katherine(cr, 640, 1060, 1.4, t, medal=pm, pose="rest")
    pop_text(cr, "2015", 1350, 220, 150, t, beat(i, "twenty fifteen"), color=MAROON, outline=(1, 1, 1))
    pf = prog(t, beat(i, "Presidential"), 0.4)
    if pf > 0:
        panel(cr, 1000, 320, 700, 200, (0.20, 0.30, 0.62), r=24, alpha=pf)
        text(cr, "PRESIDENTIAL", 1350, 405, 62, (1, 1, 1), alpha=pf)
        text(cr, "MEDAL OF FREEDOM", 1350, 480, 54, GOLDC, alpha=pf)
    pl = prog(t, beat(i, "one hundred"), 0.4)
    if pl > 0:
        stamp(cr, "LIVED TO 101", 1350, 700, pl, col=MAROON, size=70)
    sceneout(cr, t, a, b)


def s6(cr, t):  # outro: Bo hosts
    i = 6; a, b = scene_bounds(i)
    bg(cr)
    bo(cr, 420, 1020, 0.6, t, pose="point", pose_to="wave", pose_t=prog(t, beat(i, "Tell us"), 0.5), talk=t < P[i][1])
    pop_text(cr, "HBCU → ORBIT", 1250, 260, 120, t, a + 0.3, color=MAROON, outline=GOLDC)
    text(cr, "Which HBCU scientist", 1250, 440, 70, TEXT)
    text(cr, "should we cover next?", 1250, 530, 66, MAROON)
    pop_text(cr, "Tell us in the comments", 1250, 700, 56, t, beat(i, "Tell us"))
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()
    sceneout(cr, t, a, 1e9)


def thumb_hero(cr, x, y, r):
    """Hero object: a small rocket on an orbit ring."""
    s = r / 150.0
    cr.save(); cr.translate(x, y)
    cr.save(); cr.scale(1.0, 0.45); cr.arc(0, 0, 150 * s, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgb(*GOLDC); cr.set_line_width(8 * s); cr.stroke()
    cr.restore()
    rocket(cr, x, y + 100 * s, 0.5 * s, flame=0.6)


SCENES = [s0, s1, s2, s3, s4, s5, s6]
