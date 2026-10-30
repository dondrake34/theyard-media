"""Ep02 scenes: MLK at Morehouse (entered at 15 in 1944; Benjamin Mays; graduated 1948; Mays' eulogy 1968).
One function per narration paragraph, timed with beat(i, "phrase")."""
from lib import *

NAVY = (0.16, 0.20, 0.34)
CHAR = (0.25, 0.25, 0.28)
OLIVE = (0.40, 0.42, 0.25)
GRAY = (0.80, 0.80, 0.80)

MAN_POSES = {  # (elbow, hand) per side (viewer-left, viewer-right), relative to feet
    "rest":  (((-62, -250), (-58, -175)), ((62, -250), (58, -175))),
    "book":  (((-62, -250), (-58, -175)), ((70, -240), (30, -275))),
    "hold":  (((-62, -250), (-58, -175)), ((95, -265), (140, -330))),
    "think": (((-62, -250), (-58, -175)), ((75, -270), (22, -355))),
    "speak": (((-95, -270), (-150, -330)), ((62, -250), (58, -175))),
    "open":  (((-95, -270), (-150, -320)), ((95, -270), (150, -320))),
}


def man(cr, x, y, s=1.0, t=0.0, suit=NAVY, tie=MAROON, hair=None, pose="rest", pose_to=None, pose_t=0.0,
        walking=False, prop=None, gown=False, flip=False):
    """Stylized man (no mouth, no lips): suit, white shirt, tie, simple arms. hair=GRAY for an older man."""
    cr.save(); cr.translate(x, y); cr.scale(s * (-1 if flip else 1), s)
    cr.save(); cr.scale(1, 0.12); cr.arc(0, 30, 110, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgba(0, 0, 0, 0.12); cr.fill()
    sw = math.sin(t * 8) * 14 if walking else 0
    bob = -abs(math.sin(t * 8)) * 5 if walking else math.sin(t * 2.0) * 2
    # legs
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx, d in ((-22, -sw), (22, sw)):
        cr.move_to(dx, -170 + bob); cr.line_to(dx + d, -8)
        cr.set_source_rgb(*INK); cr.set_line_width(34); cr.stroke()
        cr.move_to(dx, -170 + bob); cr.line_to(dx + d, -8)
        cr.set_source_rgb(*(BLACK if gown else suit)); cr.set_line_width(26); cr.stroke()
        cr.save(); cr.translate(dx + d + 8, 0); cr.scale(1, 0.5); cr.arc(0, 0, 22, math.pi, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*BLACK); cr.fill()
    # torso / gown
    body = BLACK if gown else suit
    if gown:
        cr.move_to(-62, -330 + bob); cr.line_to(62, -330 + bob); cr.line_to(80, -60); cr.line_to(-80, -60)
    else:
        cr.move_to(-58, -330 + bob); cr.line_to(58, -330 + bob); cr.line_to(52, -160 + bob); cr.line_to(-52, -160 + bob)
    cr.close_path(); cr.set_source_rgb(*body); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    # shirt V + tie
    cr.move_to(-24, -330 + bob); cr.line_to(0, -270 + bob); cr.line_to(24, -330 + bob); cr.close_path()
    cr.set_source_rgb(1, 1, 1); cr.fill()
    if gown:
        cr.move_to(-40, -330 + bob); cr.line_to(0, -300 + bob); cr.line_to(40, -330 + bob)
        cr.set_source_rgb(*MAROON); cr.set_line_width(10); cr.stroke()
    else:
        cr.move_to(-8, -322 + bob); cr.line_to(8, -322 + bob); cr.line_to(11, -280 + bob); cr.line_to(0, -268 + bob)
        cr.line_to(-11, -280 + bob); cr.close_path(); cr.set_source_rgb(*tie); cr.fill()
    # arms
    pa = MAN_POSES[pose]; pb = MAN_POSES[pose_to] if pose_to else pa
    k = ease(clamp(pose_t)) if pose_to else 0.0
    hands = []
    for side, sx in ((0, -50), (1, 50)):
        (ea, ha), (eb, hb) = pa[side], pb[side]
        e = (ea[0] + (eb[0] - ea[0]) * k, ea[1] + (eb[1] - ea[1]) * k + bob)
        h = (ha[0] + (hb[0] - ha[0]) * k, ha[1] + (hb[1] - ha[1]) * k + bob)
        sh = (sx, -318 + bob)
        for w, col in ((32, INK), (24, body)):
            cr.move_to(*sh); cr.line_to(*e); cr.line_to(*h)
            cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_line_width(w); cr.set_source_rgb(*col); cr.stroke()
        cr.arc(h[0], h[1], 13, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
        hands.append(h)
    if prop == "book":
        hx, hy = hands[1]
        cr.save(); cr.translate(hx - 10, hy - 8); cr.rotate(-0.2)
        cr.rectangle(-34, -46, 68, 92); cr.set_source_rgb(*MAROON); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke(); cr.restore()
    elif prop == "bible":
        hx, hy = hands[1]
        cr.save(); cr.translate(hx, hy - 20)
        cr.rectangle(-32, -44, 64, 88); cr.set_source_rgb(0.12, 0.10, 0.10); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.move_to(0, -26); cr.line_to(0, 20); cr.move_to(-14, -10); cr.line_to(14, -10)
        cr.set_source_rgb(*GOLDC); cr.set_line_width(5); cr.stroke(); cr.restore()
    elif prop == "diploma":
        hx, hy = hands[1]
        cr.save(); cr.translate(hx, hy - 10); cr.rotate(-0.5)
        cr.rectangle(-60, -14, 120, 28); cr.set_source_rgb(0.98, 0.95, 0.86); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.rectangle(-8, -15, 16, 30); cr.set_source_rgb(*MAROON); cr.fill(); cr.restore()
    # head
    hy = -385 + bob
    cr.rectangle(-14, -345 + bob, 28, 22); cr.set_source_rgb(*BLACK); cr.fill()
    cr.arc(0, hy, 48, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
    if hair:  # grey hair band for an older man
        cr.arc(0, hy, 48, math.pi * 1.05, math.pi * 1.95); cr.set_source_rgb(*hair); cr.set_line_width(14); cr.stroke()
    if gown:  # mortarboard
        cr.move_to(-72, hy - 44); cr.line_to(0, hy - 70); cr.line_to(72, hy - 44); cr.line_to(0, hy - 20); cr.close_path()
        cr.set_source_rgb(*BLACK); cr.fill_preserve(); cr.set_source_rgb(0.3, 0.3, 0.3); cr.set_line_width(3); cr.stroke()
        cr.move_to(0, hy - 45); cr.line_to(60, hy - 20); cr.line_to(62, hy + 20)
        cr.set_source_rgb(*GOLDC); cr.set_line_width(5); cr.stroke()
    ph = (t + 0.9) % 3.7
    op = 0.25 if ph < 0.13 else 1.0
    for dx in (-16, 16):
        cr.save(); cr.translate(dx, hy - 4); cr.scale(1, op); cr.arc(0, 0, 8.5, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(1, 1, 1); cr.fill()
        if op > 0.5:
            cr.arc(dx + 1, hy - 3, 3.8, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
    cr.restore()


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


def campus(cr, cx, gy, s=1.0, label=True, dusk=0.0):
    """Brick college hall with columns and a clock tower (generic, no real building or seal)."""
    cr.save(); cr.translate(cx, gy); cr.scale(s, s)
    brick = (0.66 - 0.25 * dusk, 0.30 - 0.12 * dusk, 0.24 - 0.08 * dusk)
    cr.rectangle(-330, -330, 660, 330); cr.set_source_rgb(*brick); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(-60, -470, 120, 140); cr.set_source_rgb(*brick); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(-75, -470); cr.line_to(0, -560); cr.line_to(75, -470); cr.close_path()
    cr.set_source_rgb(0.30, 0.32, 0.30); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.arc(0, -410, 34, 0, 2 * math.pi); cr.set_source_rgb(0.98, 0.95, 0.86); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.move_to(0, -410); cr.line_to(0, -432); cr.move_to(0, -410); cr.line_to(14, -404); cr.stroke()
    win = (0.98 - 0.0 * dusk, 0.88, 0.60 - 0.1 * dusk)
    for r in range(2):
        for c in range(6):
            if 2 <= c <= 3 and r == 1:
                continue
            wx = -290 + c * 104; wy = -290 + r * 130
            cr.rectangle(wx, wy, 60, 80); cr.set_source_rgb(*win); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    # portico + door
    cr.move_to(-120, -170); cr.line_to(0, -230); cr.line_to(120, -170); cr.close_path()
    cr.set_source_rgb(0.95, 0.93, 0.88); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    for k in range(4):
        cr.rectangle(-105 + k * 64, -170, 18, 170); cr.set_source_rgb(0.95, 0.93, 0.88); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-30, -110, 60, 110); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()
    if label:
        text(cr, "MOREHOUSE COLLEGE", cx, gy + 60 * s + 10, 40 * s + 6, MAROON)


def tree(cr, x, y, s=1.0):
    cr.rectangle(x - 14 * s, y - 160 * s, 28 * s, 160 * s); cr.set_source_rgb(*BROWN); cr.fill()
    for dx, dy, r in ((0, -230, 90), (-70, -180, 70), (70, -180, 70)):
        cr.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi)
    cr.set_source_rgb(*GREEN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()


def soldier(cr, x, y, s, t):
    man(cr, x, y, s, t, suit=OLIVE, tie=OLIVE, walking=True)
    hy = y - 385 * s - abs(math.sin(t * 8)) * 5 * s
    cr.save(); cr.translate(x, hy); cr.scale(s, s)
    cr.arc(0, -10, 54, math.pi, 2 * math.pi); cr.close_path(); cr.set_source_rgb(*OLIVE); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke(); cr.restore()


def podium(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-90, 0); cr.line_to(-70, -200); cr.line_to(70, -200); cr.line_to(90, 0); cr.close_path()
    cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.rectangle(-100, -225, 200, 30); cr.set_source_rgb(*BROWN_LT); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


def pews(cr, y0, n_rows=3, t=0.0, alpha=1.0):
    """Rows of students seen from behind (simple heads over pew backs)."""
    cr.save(); cr.push_group()
    for r in range(n_rows):
        y = y0 + r * 70
        for c in range(14):
            x = 160 + c * 120 + (r % 2) * 50
            cr.arc(x, y - 30 + math.sin(t * 1.5 + c + r) * 2, 30, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
            cr.rectangle(x - 45, y - 5, 90, 60); cr.set_source_rgb(*NAVY if (c + r) % 2 else CHAR); cr.fill()
        cr.rectangle(60, y + 15, 1800, 40); cr.set_source_rgb(*BROWN); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha); cr.restore()


def bubble(cr, x, y, w, h, tail_x, tail_y, alpha=1.0):
    cr.save()
    rounded_rect(cr, x - w / 2, y - h / 2, w, h, 40)
    cr.set_source_rgba(1, 1, 1, alpha); cr.fill_preserve(); cr.set_source_rgba(*INK, alpha); cr.set_line_width(5); cr.stroke()
    for k, r in enumerate((16, 10)):
        u = (k + 1) / 3
        cr.arc(x + (tail_x - x) * (0.55 + u * 0.4), y + h / 2 + (tail_y - y - h / 2) * u, r, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, alpha); cr.fill_preserve(); cr.set_source_rgba(*INK, alpha); cr.stroke()
    cr.restore()


def scales(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.set_source_rgb(*GOLD_DK); cr.set_line_width(8); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(0, 60); cr.line_to(0, -60); cr.move_to(-70, -50); cr.line_to(70, -50); cr.stroke()
    cr.move_to(-40, 60); cr.line_to(40, 60); cr.stroke()
    for dx in (-70, 70):
        cr.set_line_width(3); cr.move_to(dx, -50); cr.line_to(dx - 25, 0); cr.move_to(dx, -50); cr.line_to(dx + 25, 0); cr.stroke()
        cr.arc(dx, 0, 28, 0, math.pi); cr.set_source_rgb(*GOLDC); cr.fill(); cr.set_source_rgb(*GOLD_DK)
    cr.restore()


def doc_bag(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.arc(0, -45, 26, math.pi, 2 * math.pi); cr.set_source_rgb(*INK); cr.set_line_width(8); cr.stroke()
    rounded_rect(cr, -70, -45, 140, 95, 18); cr.set_source_rgb(0.30, 0.20, 0.14); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.rectangle(-8, -20, 16, 50); cr.rectangle(-25, -3, 50, 16); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.restore()


def big_book(cr, x, y, w, h, title, sub, color=MAROON, alpha=1.0, scale=1.0):
    if alpha <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(scale, scale)
    cr.push_group()
    rounded_rect(cr, -w / 2, -h / 2, w, h, 12); cr.set_source_rgb(*color); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.rectangle(-w / 2 + 18, -h / 2, 14, h); cr.set_source_rgba(0, 0, 0, 0.25); cr.fill()
    cr.rectangle(-w / 2 + 50, -h / 2 + 40, w - 90, 4); cr.rectangle(-w / 2 + 50, h / 2 - 44, w - 90, 4)
    cr.set_source_rgb(*GOLDC); cr.fill()
    text(cr, title, 15, -10, min(60, (w - 90) / max(4, len(title)) * 1.6), GOLDC)
    if sub:
        text(cr, sub, 15, 50, 32, (1, 1, 1))
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha); cr.restore()


def wreath(cr, x, y, r, alpha=1.0):
    cr.save(); cr.push_group()
    for k in range(28):
        a = k / 28 * 2 * math.pi
        cr.arc(x + math.cos(a) * r, y + math.sin(a) * r, r * 0.22, 0, 2 * math.pi)
        cr.set_source_rgb(*(GREEN if k % 3 else (0.95, 0.95, 0.92))); cr.fill()
    cr.move_to(x - 40, y + r * 0.9); cr.line_to(x - 70, y + r * 1.6); cr.move_to(x + 40, y + r * 0.9); cr.line_to(x + 70, y + r * 1.6)
    cr.set_source_rgb(*MAROON); cr.set_line_width(22); cr.stroke()
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha); cr.restore()


# ================= SCENES
def s0(cr, t):  # hook: 15-year-old walks onto campus
    i = 0
    a, b = scene_bounds(i)
    bg(cr, SKY, BG)
    cr.arc(1650, 230, 100, 0, 2 * math.pi); cr.set_source_rgba(1, 0.78, 0.35, 0.8); cr.fill()
    ground(cr, 880, (0.62, 0.74, 0.50))
    campus(cr, 1300, 882, 1.0, label=False)
    tree(cr, 760, 882, 1.0)
    text(cr, "SEPTEMBER 1944", 96, 150, 78, MAROON, align="left", alpha=clamp(t / 0.6))
    text(cr, "ATLANTA, GEORGIA", 100, 210, 38, TEXT, align="left", alpha=clamp((t - 0.6) / 0.6))
    tw = beat(i, "A fifteen-year-old")
    pw = prog(t, tw - 0.4, 4.5)
    x = -120 + 1100 * ease(pw)
    man(cr, x, 905, 0.95, t, pose="book", prop="book", walking=0 < pw < 1)
    p15 = prog(t, tw, 0.45)
    th = beat(i, "He hasn't even finished")
    tn = beat(i, "His name?")
    if p15 > 0:
        cr.save(); cr.translate(x, 380); cr.scale(back_out(p15), back_out(p15))
        cr.arc(0, 0, 95, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
        text(cr, "AGE", 0, -18, 34, MAROON); text(cr, "15", 0, 52, 84, MAROON)
        cr.restore()
    ph = prog(t, th, 0.45) * (1 - prog(t, tn - 0.2, 0.3))
    if ph > 0:
        panel(cr, 96, 270, 700, 150, (1, 1, 1), alpha=ph)
        text(cr, "Still in high school", 446, 340, 54, TEXT, alpha=ph)
        text(cr, "(left after 11th grade)", 446, 395, 34, MAROON, alpha=ph)
    pn = prog(t, tn, 0.5)
    if pn > 0:
        cr.set_source_rgba(*MAROON, 0.93 * pn); cr.paint()
        man(cr, 520, 1010, 1.55 * back_out(pn), t, pose="rest", pose_to="book", pose_t=pn, prop="book")
        text(cr, "His name?", 1250, 330, 70, (1, 1, 1), alpha=pn)
        tk = beat(i, "Martin Luther King")
        pop_text(cr, "MARTIN LUTHER", 1250, 500, 110, t, tk, color=GOLDC)
        pop_text(cr, "KING JR.", 1250, 640, 140, t, tk + 0.35, color=GOLDC)
    fade_edges(cr, t, a, b)


def s1(cr, t):  # Morehouse, HBCU, war, early admission, father & grandfather
    i = 1
    a, b = scene_bounds(i)
    bg(cr, SKY, BG)
    ground(cr, 880, (0.62, 0.74, 0.50))
    campus(cr, 960, 882, 1.05)
    man(cr, 520, 905, 0.9, t, pose="book", prop="book")
    th = beat(i, "an H. B. C. U.")
    tw = beat(i, "With so many young men")
    ph = prog(t, th, 0.4) * (1 - prog(t, tw - 0.1, 0.35))
    if ph > 0:
        cr.set_source_rgba(*MAROON, 0.97 * ph); cr.paint()
        text(cr, "H B C U", W / 2, 500, 200, GOLDC, alpha=ph, scale=back_out(prog(t, th, 0.5)))
        text(cr, "Historically Black Colleges & Universities", W / 2, 620, 52, (1, 1, 1), alpha=ph)
    te = beat(i, "Morehouse let younger")
    tf = beat(i, "His father and")
    pw = prog(t, tw, 0.4) * (1 - prog(t, tf - 0.2, 0.35))
    if pw > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.86, 0.86, 0.80), (0.80, 0.80, 0.74))
        ground(cr, 880, (0.70, 0.68, 0.58))
        kicker(cr, "WORLD WAR II", t, tw)
        for k in range(5):
            soldier(cr, 1000 + k * 170 + 900 * prog(t, tw, 6.0), 885, 0.75, t + k * 0.3)
        pe = prog(t, te, 0.4)
        if pe > 0:
            man(cr, 520 + 140 * ease(prog(t, te, 1.2)), 905, 0.9, t, pose="book", prop="book",
                walking=0 < prog(t, te, 1.2) < 1)
            cr.save(); cr.translate(560, 330); cr.rotate(-0.1); sc = 1.5 - 0.5 * ease(pe); cr.scale(sc, sc)
            rounded_rect(cr, -260, -70, 520, 120, 16)
            cr.set_source_rgba(*MAROON, pe); cr.set_line_width(10); cr.stroke()
            text(cr, "EARLY ADMISSION", 0, 12, 56, MAROON, alpha=pe)
            cr.restore()
        cr.pop_group_to_source(); cr.paint_with_alpha(pw); cr.restore()
    pf = prog(t, tf, 0.45)
    if pf > 0:
        cr.set_source_rgba(*BG, 0.96 * pf); cr.paint()
        text(cr, "Three generations of Morehouse men", W / 2, 170, 60, MAROON, alpha=pf)
        figs = [("GRANDFATHER", beat(i, "his grandfather"), GRAY, CHAR, 500),
                ("FATHER", beat(i, "His father"), (0.35, 0.33, 0.33), (0.30, 0.24, 0.20), 960),
                ("MARTIN", tf + 1.6, None, NAVY, 1420)]
        for lab, st, hair, suit, x in figs:
            p = prog(t, st, 0.45)
            if p <= 0:
                continue
            man(cr, x, 880, 1.05 * back_out(p), t, suit=suit, hair=hair, pose="rest")
            name_tag(cr, lab, None, x, 920, clamp(p * 2), 40)
    fade_edges(cr, t, a, b)


def s2(cr, t):  # lawyer or doctor, then Benjamin Mays
    i = 2
    a, b = scene_bounds(i)
    bg(cr)
    ground(cr, 900)
    tp = beat(i, "a preacher")
    tl = beat(i, "a lawyer")
    td = beat(i, "a doctor")
    tm = beat(i, "Then he met")
    out = prog(t, tm - 0.1, 0.4)
    mx = 760 - 330 * ease(prog(t, tm, 0.8))
    man(cr, mx, 920, 1.25, t, pose="think" if t < tm else "rest", prop=None)
    pp = prog(t, a + 0.3, 0.45) * (1 - out)
    if pp > 0:
        bubble(cr, 1320, 290, 620, 200, mx + 60, 420, alpha=pp)
        text(cr, "PREACHER?", 1320, 315, 80, TEXT, alpha=pp)
        px = prog(t, tp + 0.2, 0.35)
        if px > 0:
            cr.save(); cr.set_source_rgba(0.80, 0.15, 0.15, pp); cr.set_line_width(14); cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.move_to(1090, 300); cr.line_to(1090 + 460 * px, 300 - 20 * px); cr.stroke(); cr.restore()
    for st, x, lab, draw in ((tl, 1150, "LAWYER?", scales), (td, 1600, "DOCTOR?", doc_bag)):
        p = prog(t, st, 0.45) * (1 - out)
        if p <= 0:
            continue
        cr.save(); cr.translate(x, 640); cr.scale(back_out(prog(t, st, 0.45)), back_out(prog(t, st, 0.45)))
        panel(cr, -190, -150, 380, 330, (1, 1, 1), alpha=p)
        cr.push_group(); draw(cr, 0, -10, 1.3); cr.pop_group_to_source(); cr.paint_with_alpha(p)
        text(cr, lab, 0, 140, 52, MAROON, alpha=p)
        cr.restore()
    if out > 0:
        tb = beat(i, "Benjamin Mays")
        pb = prog(t, tb - 0.6, 0.6)
        campus(cr, 1500, 902, 0.62, label=False)
        man(cr, 1050, 920, 1.3 * back_out(pb), t, suit=CHAR, tie=(0.20, 0.25, 0.40), hair=GRAY, pose="rest",
            pose_to="open", pose_t=prog(t, tb, 0.6)) if pb > 0 else None
        text(cr, "He met the college president", W / 2, 160, 60, TEXT, alpha=out)
        name_tag(cr, "BENJAMIN MAYS", "President of Morehouse, 1940-1967", 1050, 220, prog(t, tb, 0.5), 58)
    fade_edges(cr, t, a, b)


def s3(cr, t):  # chapel, sensitive to wrongs, Gandhi, nonviolence
    i = 3
    a, b = scene_bounds(i)
    bg(cr, (0.93, 0.88, 0.80), (0.86, 0.80, 0.70))
    # chapel windows
    for k in range(4):
        x = 260 + k * 470
        cr.move_to(x - 60, 520); cr.line_to(x - 60, 260); cr.arc(x, 260, 60, math.pi, 0); cr.line_to(x + 60, 520); cr.close_path()
        cr.set_source_rgb(0.98, 0.88, 0.60); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    kicker(cr, "EVERY WEEK · CHAPEL", t, a + 0.1)
    tg = beat(i, "And he introduced")
    tv = beat(i, "Nonviolence")
    swap = prog(t, tg - 0.1, 0.4)
    podium(cr, 960, 760, 1.0)
    man(cr, 960, 760, 1.05, t, suit=CHAR, tie=(0.20, 0.25, 0.40), hair=GRAY, pose="speak" if (t * 1.1) % 3 < 1.6 else "open")
    podium(cr, 960, 760, 1.0)  # redraw front so it hides his legs
    pews(cr, 900, 3, t)
    ts = beat(i, "He told students")
    ps = prog(t, ts, 0.5) * (1 - swap)
    if ps > 0:
        panel(cr, 1180, 170, 680, 330, (1, 1, 1), alpha=ps)
        text(cr, "Be sensitive to", 1520, 260, 48, TEXT, alpha=ps)
        text(cr, "the wrongs and", 1520, 330, 56, MAROON, alpha=ps)
        text(cr, "injustices of society", 1520, 400, 56, MAROON, alpha=ps)
        text(cr, "(Mays' message to students)", 1520, 460, 28, TEXT, alpha=ps)
    if swap > 0:
        cr.set_source_rgba(*BG, 0.96 * swap); cr.paint()
        ground(cr, 900)
        man(cr, 520, 920, 1.25 * back_out(swap), t, pose="book", prop="book")
        name_tag(cr, "YOUNG MARTIN", None, 520, 950, swap, 40)
        pk = prog(t, beat(i, "the ideas of Gandhi"), 0.5)
        big_book(cr, 1230, 470, 520, 340, "GANDHI", "ideas & philosophy", alpha=pk, scale=back_out(pk) * (1 - 0.25 * prog(t, tv, 0.4)))
        pv = prog(t, tv, 0.45)
        if pv > 0:
            text(cr, "NONVIOLENCE", 1230, 820, 104, MAROON, alpha=pv, scale=back_out(pv), outline=(1, 1, 1))
    fade_edges(cr, t, a, b)


def s4(cr, t):  # Thoreau, ministry, 1948 graduation at 19
    i = 4
    a, b = scene_bounds(i)
    bg(cr)
    ground(cr, 900)
    ts = beat(i, "In his senior year")
    tg = beat(i, "And in nineteen forty-eight")
    p1 = 1 - prog(t, ts - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        kicker(cr, "AT MOREHOUSE", t, a + 0.1)
        # desk + lamp
        cr.rectangle(300, 700, 700, 30); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
        for dx in (330, 940):
            cr.rectangle(dx, 730, 30, 170); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
        man(cr, 560, 920, 1.15, t, pose="book", prop="book")
        pb = prog(t, beat(i, "Thoreau's essay"), 0.5)
        big_book(cr, 1380, 450, 680, 380, "CIVIL DISOBEDIENCE", "Henry David Thoreau", color=(0.20, 0.30, 0.25),
                 alpha=pb, scale=back_out(pb))
        pf = prog(t, beat(i, "first read"), 0.4)
        text(cr, "FIRST READ IT HERE", 1380, 760, 50, MAROON, alpha=pf)
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, ts, 0.4) * (1 - prog(t, tg - 0.1, 0.35))
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.95, 0.91, 0.84), BG2); ground(cr, 900)
        kicker(cr, "SENIOR YEAR", t, ts)
        man(cr, 700, 920, 1.25, t, pose="rest", pose_to="hold", pose_t=prog(t, ts + 0.3, 0.6), prop="bible")
        pop_text(cr, "HE CHOSE THE", 1320, 420, 64, t, beat(i, "he chose"), color=TEXT)
        pop_text(cr, "MINISTRY", 1320, 560, 130, t, beat(i, "the ministry"), color=MAROON)
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    p3 = prog(t, tg, 0.45)
    if p3 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG); ground(cr, 880, (0.62, 0.74, 0.50))
        campus(cr, 1450, 882, 0.75, label=False)
        man(cr, 640, 905, 1.3 * back_out(p3), t, pose="rest", pose_to="hold", pose_t=prog(t, tg + 0.5, 0.5),
            prop="diploma", gown=True)
        # confetti
        for k in range(40):
            u = (t - tg) * 0.5 + k * 0.137
            cx = (k * 197) % 1920; cy = (u % 1.0) * 1000
            cr.rectangle(cx, cy, 14, 22); cr.set_source_rgb(*(GOLDC if k % 2 else MAROON)); cr.fill()
        pop_text(cr, "1948", 1180, 300, 150, t, tg + 0.2, color=MAROON, outline=(1, 1, 1))
        pop_text(cr, "GRADUATED AT 19", 1180, 420, 70, t, beat(i, "at just nineteen"), color=TEXT, outline=(1, 1, 1))
        pop_text(cr, "B.A. in Sociology", 1180, 500, 44, t, beat(i, "he graduated"), color=MAROON, outline=(1, 1, 1))
        cr.pop_group_to_source(); cr.paint_with_alpha(p3); cr.restore()
    fade_edges(cr, t, a, b)


def s5(cr, t):  # the part most people never hear: 1968, Mays' eulogy
    i = 5
    a, b = scene_bounds(i)
    bg(cr, (0.90, 0.92, 0.95), (0.95, 0.93, 0.90))
    tt = beat(i, "Twenty years later")
    ph = prog(t, a + 0.1, 0.4) * (1 - prog(t, tt - 0.1, 0.35))
    if ph > 0:
        bo(cr, 960, 1000, 0.55, t, pose="shrug", wide=0.7, brow=0.9)
        text(cr, "The part most people never hear...", W / 2, 180, 70, MAROON, alpha=ph)
    pt = prog(t, tt, 0.5)
    if pt > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.55, 0.45, 0.55), (0.85, 0.65, 0.55))
        ground(cr, 880, (0.45, 0.52, 0.38))
        campus(cr, 1300, 882, 1.0, label=False, dusk=0.7)
        text(cr, "MOREHOUSE COLLEGE", 1300, 950, 46, (1, 1, 1))
        tm = beat(i, "And the man")
        pw = prog(t, beat(i, "the final service"), 0.6)
        wreath(cr, 360, 560, 120 * back_out(pw), alpha=clamp(pw * 2))
        pop_text(cr, "1968", 360, 200, 140, t, beat(i, "nineteen sixty-eight"), color=(1, 1, 1), outline=INK)
        pf = prog(t, beat(i, "the final service"), 0.5) * (1 - prog(t, tm - 0.2, 0.3))
        if pf > 0:
            panel(cr, 760, 120, 1080, 170, (1, 1, 1), alpha=pf)
            text(cr, "Final service of Dr. King's funeral", 1300, 195, 46, TEXT, alpha=pf)
            text(cr, "held on the Morehouse campus", 1300, 255, 46, MAROON, alpha=pf)
        pm = prog(t, tm, 0.5)
        if pm > 0:
            podium(cr, 760, 880, 1.0)
            man(cr, 760, 880, 1.15 * back_out(pm), t, suit=CHAR, tie=(0.20, 0.25, 0.40), hair=GRAY, pose="open")
            podium(cr, 760, 880, 1.0)
            text(cr, "Who gave the eulogy?", 1300, 200, 60, (1, 1, 1), alpha=pm, outline=INK)
            name_tag(cr, "BENJAMIN MAYS", "his college mentor", 760, 900, prog(t, beat(i, "Benjamin Mays."), 0.4), 54)
        cr.pop_group_to_source(); cr.paint_with_alpha(pt); cr.restore()
    fade_edges(cr, t, a, b)


def s6(cr, t):  # outro / CTA with Bo
    i = 6
    a, b = scene_bounds(i)
    bg(cr)
    tq = beat(i, "Which H. B. C. U.")
    bo(cr, 420, 1020, 0.6, t, pose="pockets", pose_to="point" if t < tq else "wave",
       pose_t=prog(t, a + 0.2, 0.5) if t < tq else prog(t, tq, 0.5), talk=t < P[i][1])
    pd = prog(t, a + 0.2, 0.5) * (1 - prog(t, tq - 0.2, 0.3))
    if pd > 0:
        text(cr, "A lot of that dream", 1220, 380, 76, TEXT, alpha=pd)
        text(cr, "started on", 1220, 480, 76, TEXT, alpha=pd)
        text(cr, "THE YARD", 1220, 640, 140, GOLDC, alpha=pd, outline=INK, scale=back_out(prog(t, beat(i, "The Yard"), 0.5)))
    pq = prog(t, tq, 0.5)
    if pq > 0:
        text(cr, "Which HBCU legend", 1220, 330, 76, TEXT, alpha=pq)
        text(cr, "should we cover next?", 1220, 430, 76, MAROON, alpha=pq)
        pop_text(cr, "Tell us in the comments", 1220, 560, 52, t, beat(i, "Tell us"))
        pop_text(cr, "THE YARD", 1220, 760, 72, t, beat(i, "Tell us") + 0.5, color=GOLDC, outline=INK)
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()


def thumb_hero(cr, x, y, r):
    """Hero object for thumbnails: a gold 'AGE 15' badge with a mortarboard."""
    cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(r * 0.05); cr.stroke()
    text(cr, "AGE", x, y - r * 0.05, r * 0.30, MAROON)
    text(cr, "15", x, y + r * 0.62, r * 0.75, MAROON)
    cr.save(); cr.translate(x, y - r * 0.82)
    cr.move_to(-r * 0.6, 0); cr.line_to(0, -r * 0.25); cr.line_to(r * 0.6, 0); cr.line_to(0, r * 0.25); cr.close_path()
    cr.set_source_rgb(*BLACK); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.move_to(0, 0); cr.line_to(r * 0.5, r * 0.2); cr.line_to(r * 0.52, r * 0.55)
    cr.set_source_rgb(*MAROON); cr.set_line_width(r * 0.05); cr.stroke()
    cr.restore()


SCENES = [s0, s1, s2, s3, s4, s5, s6]
