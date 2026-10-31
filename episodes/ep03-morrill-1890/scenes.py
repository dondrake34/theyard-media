"""Ep03 scenes: the Morrill Acts of 1862 and 1890 and the 19 "1890" land-grant HBCUs.
One function per narration paragraph, timed with beat(i, "phrase")."""
from lib import *

NAVY = (0.16, 0.20, 0.34)
CHAR = (0.25, 0.25, 0.28)
GRAY = (0.80, 0.80, 0.80)
WHEAT = (0.90, 0.72, 0.32)
FIELD = (0.62, 0.74, 0.50)
SKIN_LT = (0.93, 0.80, 0.68)
RED = (0.78, 0.14, 0.14)
PAPER = (0.98, 0.95, 0.86)

MAN_POSES = {  # (elbow, hand) per side (viewer-left, viewer-right), relative to feet
    "rest":  (((-62, -250), (-58, -175)), ((62, -250), (58, -175))),
    "write": (((-62, -250), (-58, -175)), ((90, -230), (140, -215))),
    "hold":  (((-62, -250), (-58, -175)), ((95, -265), (140, -330))),
    "speak": (((-95, -270), (-150, -330)), ((62, -250), (58, -175))),
    "open":  (((-95, -270), (-150, -320)), ((95, -270), (150, -320))),
    "hoe":   (((-70, -260), (-20, -210)), ((70, -250), (40, -200))),
    "book":  (((-62, -250), (-58, -175)), ((70, -240), (30, -275))),
}


def man(cr, x, y, s=1.0, t=0.0, suit=NAVY, tie=MAROON, skin=BLACK, hair=None, pose="rest", pose_to=None,
        pose_t=0.0, walking=False, prop=None, beard=False, hat=False, whiskers=False, work=False, flip=False):
    """Stylized man (no mouth, no lips). skin sets the head colour; beard/hat/whiskers for historical figures."""
    cr.save(); cr.translate(x, y); cr.scale(s * (-1 if flip else 1), s)
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
    if work:  # work shirt with suspenders
        for dx in (-26, 26):
            cr.move_to(dx, -330 + bob); cr.line_to(dx, -165 + bob)
        cr.set_source_rgb(*BROWN); cr.set_line_width(9); cr.stroke()
    else:
        cr.move_to(-24, -330 + bob); cr.line_to(0, -270 + bob); cr.line_to(24, -330 + bob); cr.close_path()
        cr.set_source_rgb(1, 1, 1); cr.fill()
        cr.move_to(-8, -322 + bob); cr.line_to(8, -322 + bob); cr.line_to(11, -280 + bob); cr.line_to(0, -268 + bob)
        cr.line_to(-11, -280 + bob); cr.close_path(); cr.set_source_rgb(*tie); cr.fill()
    pa = MAN_POSES[pose]; pb = MAN_POSES[pose_to] if pose_to else pa
    k = ease(clamp(pose_t)) if pose_to else 0.0
    hands = []
    for side, sx in ((0, -50), (1, 50)):
        (ea, ha), (eb, hb) = pa[side], pb[side]
        e = (ea[0] + (eb[0] - ea[0]) * k, ea[1] + (eb[1] - ea[1]) * k + bob)
        h = (ha[0] + (hb[0] - ha[0]) * k, ha[1] + (hb[1] - ha[1]) * k + bob)
        sh = (sx, -318 + bob)
        for w, col in ((32, INK), (24, suit)):
            cr.move_to(*sh); cr.line_to(*e); cr.line_to(*h)
            cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_line_width(w); cr.set_source_rgb(*col); cr.stroke()
        cr.arc(h[0], h[1], 13, 0, 2 * math.pi); cr.set_source_rgb(*skin); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        hands.append(h)
    if prop == "hoe":
        (lx, ly), (rx, ry) = hands
        cr.move_to(lx - 60, ly - 120); cr.line_to(rx + 70, ry + 200)
        cr.set_source_rgb(*BROWN); cr.set_line_width(10); cr.stroke()
        cr.move_to(rx + 70, ry + 200); cr.line_to(rx + 120, ry + 190)
        cr.set_source_rgb(0.4, 0.4, 0.42); cr.set_line_width(16); cr.stroke()
    elif prop == "pen":
        hx, hy = hands[1]
        cr.move_to(hx, hy); cr.line_to(hx + 30, hy - 60); cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    elif prop == "book":
        hx, hy = hands[1]
        cr.save(); cr.translate(hx - 10, hy - 8); cr.rotate(-0.2)
        cr.rectangle(-34, -46, 68, 92); cr.set_source_rgb(*MAROON); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke(); cr.restore()
    elif prop == "letter":
        hx, hy = hands[1]
        cr.save(); cr.translate(hx + 10, hy - 30); cr.rotate(0.15)
        cr.rectangle(-40, -52, 80, 104); cr.set_source_rgb(*PAPER); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        for ly in (-30, -14, 2, 18):
            cr.move_to(-26, ly); cr.line_to(26, ly)
        cr.set_line_width(2); cr.stroke(); cr.restore()
    # head
    hy = -385 + bob
    cr.rectangle(-14, -345 + bob, 28, 22); cr.set_source_rgb(*skin); cr.fill()
    cr.arc(0, hy, 48, 0, 2 * math.pi); cr.set_source_rgb(*skin); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4 if skin != BLACK else 0.01); cr.stroke()
    if hair:
        cr.arc(0, hy, 48, math.pi * 1.05, math.pi * 1.95); cr.set_source_rgb(*hair); cr.set_line_width(14); cr.stroke()
    if whiskers:  # side whiskers (grey), no mouth
        for dx in (-40, 40):
            cr.save(); cr.translate(dx, hy + 18); cr.scale(0.55, 1)
            cr.arc(0, 0, 26, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*GRAY); cr.fill()
    if beard:  # chin beard with no moustache or mouth
        cr.move_to(-46, hy + 6); cr.curve_to(-40, hy + 70, 40, hy + 70, 46, hy + 6)
        cr.curve_to(30, hy + 36, -30, hy + 36, -46, hy + 6); cr.close_path()
        cr.set_source_rgb(0.15, 0.12, 0.10); cr.fill()
    if hat:  # stovepipe hat
        cr.rectangle(-70, hy - 46, 140, 14); cr.rectangle(-44, hy - 150, 88, 106)
        cr.set_source_rgb(0.10, 0.10, 0.12); cr.fill()
    ph = (t + 0.9) % 3.7
    op = 0.25 if ph < 0.13 else 1.0
    eye_white = (1, 1, 1)
    for dx in (-16, 16):
        cr.save(); cr.translate(dx, hy - 4); cr.scale(1, op); cr.arc(0, 0, 8.5, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*eye_white); cr.fill()
        if skin != BLACK:
            cr.save(); cr.translate(dx, hy - 4); cr.scale(1, op); cr.arc(0, 0, 8.5, 0, 2 * math.pi); cr.restore()
            cr.set_source_rgb(*INK); cr.set_line_width(2); cr.stroke()
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


def hall(cr, cx, gy, s=1.0, brick=(0.66, 0.30, 0.24), gate=0.0, label=None, label_col=MAROON):
    """Generic brick college hall with a portico (no real building or seal). gate>0 draws closed iron gates."""
    cr.save(); cr.translate(cx, gy); cr.scale(s, s)
    cr.rectangle(-300, -300, 600, 300); cr.set_source_rgb(*brick); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(-320, -300); cr.line_to(0, -400); cr.line_to(320, -300); cr.close_path()
    cr.set_source_rgb(0.95, 0.93, 0.88); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for r in range(2):
        for c in range(5):
            if c == 2 and r == 1:
                continue
            cr.rectangle(-260 + c * 112, -260 + r * 120, 60, 80); cr.set_source_rgb(0.98, 0.88, 0.60); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    for k in range(4):
        cr.rectangle(-95 + k * 56, -150, 18, 150); cr.set_source_rgb(0.95, 0.93, 0.88); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    cr.rectangle(-28, -100, 56, 100); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    if gate > 0:
        cr.save(); cr.push_group()
        cr.rectangle(-420, -190, 840, 10); cr.rectangle(-420, -10, 840, 10)
        cr.set_source_rgb(0.12, 0.12, 0.14); cr.fill()
        for k in range(29):
            gx = -420 + k * 30
            cr.move_to(gx, 0); cr.line_to(gx, -210)
            cr.move_to(gx - 9, -200); cr.line_to(gx, -222); cr.line_to(gx + 9, -200)
        cr.set_source_rgb(0.12, 0.12, 0.14); cr.set_line_width(7); cr.stroke()
        cr.pop_group_to_source(); cr.paint_with_alpha(gate); cr.restore()
    cr.restore()
    if label:
        text(cr, label, cx, gy + 58 * s + 8, 46 * s + 6, label_col)


def mini_hall(cr, x, y, s, alpha=1.0, col=MAROON):
    if alpha <= 0:
        return
    cr.save(); cr.push_group(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-50, -60, 100, 60); cr.set_source_rgb(*col); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.move_to(-60, -60); cr.line_to(0, -95); cr.line_to(60, -60); cr.close_path()
    cr.set_source_rgb(*GOLDC); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-12, -32, 24, 32); cr.set_source_rgb(*PAPER); cr.fill()
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha); cr.restore()


def tree(cr, x, y, s=1.0):
    cr.rectangle(x - 14 * s, y - 160 * s, 28 * s, 160 * s); cr.set_source_rgb(*BROWN); cr.fill()
    for dx, dy, r in ((0, -230, 90), (-70, -180, 70), (70, -180, 70)):
        cr.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi)
    cr.set_source_rgb(*GREEN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()


def scroll(cr, x, y, w, h, l1, l2=None, alpha=1.0, scale=1.0, seal=True):
    """Parchment law document."""
    if alpha <= 0 or scale <= 0:
        return
    cr.save(); cr.translate(x, y); cr.scale(scale, scale); cr.push_group()
    cr.rectangle(-w / 2, -h / 2, w, h); cr.set_source_rgb(*PAPER); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for dy in (-h / 2, h / 2):
        cr.save(); cr.translate(0, dy); cr.scale(1, 0.35)
        rounded_rect(cr, -w / 2 - 20, -40, w + 40, 80, 40); cr.restore()
        cr.set_source_rgb(0.90, 0.82, 0.62); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    text(cr, l1, 0, -h / 2 + 95, min(64, w / max(6, len(l1)) * 1.45), MAROON)
    if l2:
        text(cr, l2, 0, -h / 2 + 165, min(50, w / max(6, len(l2)) * 1.6), TEXT)
    for k in range(4):
        ly = -h / 2 + 215 + k * 34
        if ly < h / 2 - 60:
            cr.move_to(-w / 2 + 50, ly); cr.line_to(w / 2 - 50 - (k % 2) * 60, ly)
    cr.set_source_rgba(*INK, 0.35); cr.set_line_width(4); cr.stroke()
    if seal:
        cr.arc(w / 2 - 70, h / 2 - 70, 36, 0, 2 * math.pi); cr.set_source_rgb(*MAROON); cr.fill()
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha); cr.restore()


def desk(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-220, -150, 440, 30); cr.set_source_rgb(*BROWN_LT); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    for dx in (-200, 170):
        cr.rectangle(dx, -120, 30, 120); cr.set_source_rgb(*BROWN); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


def land_grid(cr, x0, y0, cols, rows, cw, ch, p, t):
    """Parcels of land appearing one by one (green/wheat squares)."""
    n = cols * rows
    for k in range(n):
        q = clamp(p * n * 1.1 - k)
        if q <= 0:
            continue
        r, c = divmod(k, cols)
        x = x0 + c * cw; y = y0 + r * ch
        cr.save(); cr.translate(x + cw / 2, y + ch / 2); cr.scale(back_out(q), back_out(q))
        cr.rectangle(-cw / 2 + 4, -ch / 2 + 4, cw - 8, ch - 8)
        cr.set_source_rgb(*(FIELD if (r + c) % 2 else WHEAT)); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.restore()


def sale_sign(cr, x, y, s=1.0, alpha=1.0):
    if alpha <= 0:
        return
    cr.save(); cr.push_group(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-8, -40, 16, 160); cr.set_source_rgb(*BROWN); cr.fill()
    rounded_rect(cr, -110, -120, 220, 90, 10); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    text(cr, "FOR SALE", 0, -60, 42, RED)
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha); cr.restore()


def wheat(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    for a in (-0.3, 0, 0.3):
        cr.save(); cr.rotate(a)
        cr.move_to(0, 0); cr.line_to(0, -120); cr.set_source_rgb(*GOLD_DK); cr.set_line_width(6); cr.stroke()
        for k in range(5):
            for sd in (-1, 1):
                cr.save(); cr.translate(sd * 10, -70 - k * 16); cr.rotate(sd * 0.5); cr.scale(0.5, 1)
                cr.arc(0, 0, 12, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*WHEAT); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(2); cr.stroke()
        cr.restore()
    cr.restore()


def gear(cr, x, y, r, rot=0.0):
    cr.save(); cr.translate(x, y); cr.rotate(rot)
    n = 10
    for k in range(n * 2):
        a = k / (n * 2) * 2 * math.pi
        rr = r if k % 2 == 0 else r * 0.78
        a2 = (k + 1) / (n * 2) * 2 * math.pi
        cr.line_to(math.cos(a) * rr, math.sin(a) * rr); cr.line_to(math.cos(a2) * rr, math.sin(a2) * rr)
    cr.close_path(); cr.set_source_rgb(0.55, 0.57, 0.62); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.arc(0, 0, r * 0.3, 0, 2 * math.pi); cr.set_source_rgb(*BG); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


def money_bag(cr, x, y, s=1.0, label="$"):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-30, -110); cr.line_to(30, -110); cr.line_to(18, -80); cr.line_to(-18, -80); cr.close_path()
    cr.set_source_rgb(0.72, 0.58, 0.38); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.arc(0, -20, 70, 0, 2 * math.pi); cr.set_source_rgb(0.80, 0.66, 0.44); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.stroke()
    text(cr, label, 0, 6, 70, (0.20, 0.45, 0.20))
    cr.restore()


def big_x(cr, x, y, r, p):
    if p <= 0:
        return
    cr.save(); cr.translate(x, y); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    q1 = clamp(p * 2); q2 = clamp(p * 2 - 1)
    cr.move_to(-r, -r); cr.line_to(-r + 2 * r * q1, -r + 2 * r * q1)
    if q2 > 0:
        cr.move_to(r, -r); cr.line_to(r - 2 * r * q2, -r + 2 * r * q2)
    cr.set_source_rgb(*RED); cr.set_line_width(r * 0.28); cr.stroke()
    cr.restore()


def balance(cr, x, y, s, tilt, left_col, right_col):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-60, 0); cr.line_to(60, 0); cr.move_to(0, 0); cr.line_to(0, -300)
    cr.set_source_rgb(*GOLD_DK); cr.set_line_width(14); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.stroke()
    cr.save(); cr.translate(0, -300); cr.rotate(tilt)
    cr.move_to(-260, 0); cr.line_to(260, 0); cr.set_source_rgb(*GOLD_DK); cr.set_line_width(12); cr.stroke()
    pans = []
    for dx in (-260, 260):
        cr.move_to(dx, 0); cr.line_to(dx - 70, 150); cr.move_to(dx, 0); cr.line_to(dx + 70, 150)
        cr.set_line_width(4); cr.stroke()
        cr.arc(dx, 150, 90, 0, math.pi); cr.set_source_rgb(*GOLDC); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke(); cr.set_source_rgb(*GOLD_DK)
    cr.restore()
    cr.arc(0, -300, 18, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill()
    cr.restore()
    # pan centres in scene coordinates
    for dx, col in ((-260, left_col), (260, right_col)):
        px = x + s * (dx * math.cos(tilt)); py = y + s * (-300 + dx * math.sin(tilt) + 150)
        mini_hall(cr, px, py, s * 0.9, col=col)


# ================= SCENES
def s0(cr, t):  # hook: 19 HBCU land-grant universities, a law from 1890, story starts 1862
    i = 0
    a, b = scene_bounds(i)
    bg(cr, SKY, BG)
    t19 = beat(i, "Nineteen")
    tl = beat(i, "It all traces")
    ts = beat(i, "But the story")
    p1 = prog(t, t19, 0.4) * (1 - prog(t, tl - 0.1, 0.3))
    if p1 > 0:
        cr.save(); cr.push_group()
        pop_text(cr, "19", 400, 560, 380, t, t19 + 0.05, color=GOLDC, outline=INK)
        pop_text(cr, "HBCUs", 400, 720, 110, t, beat(i, "H. B. C. U."), color=MAROON)
        pop_text(cr, "LAND-GRANT", 400, 840, 70, t, beat(i, "land-grant"), color=TEXT)
        pop_text(cr, "UNIVERSITIES", 400, 920, 70, t, beat(i, "universities."), color=TEXT)
        for k in range(19):
            r, c = divmod(k, 5)
            q = prog(t, t19 + 0.3 + k * 0.1, 0.35)
            mini_hall(cr, 900 + c * 210, 300 + r * 200, 1.25 * back_out(q), alpha=clamp(q * 2))
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    # Bo reacts small in the corner during the hook
    pb = prog(t, t19 + 0.8, 0.4) * (1 - prog(t, tl - 0.1, 0.3))
    if pb > 0:
        cr.save(); cr.push_group()
        bo(cr, 1780, 1080, 0.22, t, pose="point", wide=0.8, brow=1.0)
        cr.pop_group_to_source(); cr.paint_with_alpha(pb); cr.restore()
    p2 = prog(t, tl, 0.4) * (1 - prog(t, ts - 0.1, 0.3))
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, BG, BG2)
        scroll(cr, W / 2, 540, 760, 620, "AN ACT OF CONGRESS", "1890", scale=back_out(prog(t, tl, 0.5)))
        pop_text(cr, "ONE LAW", W / 2, 150, 90, t, beat(i, "a law"), color=MAROON)
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    p3 = prog(t, ts, 0.4)
    if p3 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.86, 0.84, 0.78), (0.80, 0.78, 0.72))
        ty = beat(i, "eighteen sixty-two.")
        k = prog(t, ty - 0.3, 1.0)
        yr = int(1890 - 28 * ease(k))
        panel(cr, W / 2 - 330, 300, 660, 420, (1, 1, 1))
        cr.rectangle(W / 2 - 330, 300, 660, 110); cr.set_source_rgb(*MAROON); cr.fill()
        text(cr, "REWIND", W / 2, 378, 60, GOLDC)
        text(cr, str(yr), W / 2, 640, 220, TEXT)
        text(cr, "where the story starts", W / 2, 840, 54, MAROON, alpha=clamp((t - ty) / 0.4))
        cr.pop_group_to_source(); cr.paint_with_alpha(p3); cr.restore()
    fade_edges(cr, t, a, b)


def s1(cr, t):  # 1862: Lincoln signs the Morrill Act; land sold to fund colleges (farming + mechanic arts)
    i = 1
    a, b = scene_bounds(i)
    bg(cr, (0.95, 0.92, 0.86), BG2)
    ts = beat(i, "States got")
    tm = beat(i, "and the money")
    p1 = 1 - prog(t, ts - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        ground(cr, 900, (0.80, 0.72, 0.60))
        text(cr, "1862", 140, 170, 90, MAROON, align="left")
        tp = beat(i, "President Abraham Lincoln")
        man(cr, 700, 905, 1.15, t, suit=(0.10, 0.10, 0.12), tie=(0.10, 0.10, 0.12), skin=SKIN_LT, beard=True,
            hat=True, pose="rest", pose_to="write", pose_t=prog(t, beat(i, "signed"), 0.5), prop="pen")
        desk(cr, 860, 905, 1.0)
        name_tag(cr, "ABRAHAM LINCOLN", "16th U.S. president", 700, 930, prog(t, tp, 0.4), 44)
        pd = prog(t, beat(i, "the Morrill Act."), 0.5)
        scroll(cr, 1420, 470, 560, 520, "MORRILL ACT", "July 2, 1862", alpha=clamp(pd * 2), scale=back_out(pd))
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, ts, 0.4) * (1 - prog(t, tm - 0.1, 0.35))
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        kicker(cr, "FEDERAL LAND", t, ts)
        land_grid(cr, 260, 260, 8, 4, 150, 140, prog(t, ts, 1.4), t)
        sale_sign(cr, 1600, 700, 1.2, alpha=prog(t, beat(i, "to sell,"), 0.3))
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    p3 = prog(t, tm, 0.4)
    if p3 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 880, FIELD)
        money_bag(cr, 300, 700, 1.3 * back_out(prog(t, tm, 0.4)))
        cr.move_to(420, 640); cr.line_to(640, 640); cr.set_source_rgb(*INK); cr.set_line_width(10); cr.stroke()
        cr.move_to(640, 610); cr.line_to(690, 640); cr.line_to(640, 670); cr.close_path(); cr.fill()
        ph = prog(t, beat(i, "built colleges"), 0.5)
        if ph > 0:
            cr.save(); cr.translate(1060, 882); cr.scale(back_out(ph), back_out(ph)); hall(cr, 0, 0, 0.95); cr.restore()
            text(cr, "LAND-GRANT COLLEGE", 1060, 960, 46, MAROON, alpha=ph)
        pf = prog(t, beat(i, "farming"), 0.4)
        if pf > 0:
            wheat(cr, 1600, 520, 1.1 * back_out(pf))
            text(cr, "FARMING", 1600, 600, 48, TEXT, alpha=pf)
        pa = prog(t, beat(i, "mechanic arts."), 0.4)
        if pa > 0:
            gear(cr, 1600, 730, 70 * back_out(pa), rot=t)
            text(cr, "MECHANIC ARTS", 1600, 850, 48, TEXT, alpha=pa)
        cr.pop_group_to_source(); cr.paint_with_alpha(p3); cr.restore()
    fade_edges(cr, t, a, b)


def s2(cr, t):  # across the South most colleges shut Black students out; those who worked the land
    i = 2
    a, b = scene_bounds(i)
    tp = beat(i, "The people who")
    p1 = 1 - prog(t, tp - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.90, 0.88, 0.84), BG2)
        ground(cr, 880, (0.70, 0.70, 0.60))
        text(cr, "ACROSS THE SOUTH", 120, 150, 64, MAROON, align="left")
        hall(cr, 1250, 882, 1.0, gate=prog(t, beat(i, "shut"), 0.3))
        for k, (dx, girl) in enumerate(((260, False), (420, True), (580, False))):
            if girl:
                kid(cr, dx, 905, 1.7, dress=PURPLE, girl=True, t=t)
            else:
                man(cr, dx, 905, 0.85, t + k, suit=NAVY if k else CHAR, pose="book", prop="book")
        pb = prog(t, beat(i, "Black students out."), 0.5)
        big_x(cr, 1250, 640, 120, pb)
        if pb > 0:
            panel(cr, 120, 200, 640, 120, (1, 1, 1), alpha=pb)
            text(cr, "Black students shut out", 440, 278, 46, TEXT, alpha=pb)
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, tp, 0.4)
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 860, (0.62, 0.50, 0.32))
        for r in range(4):
            cr.move_to(0, 900 + r * 45); cr.line_to(W, 900 + r * 45)
        cr.set_source_rgba(*INK, 0.25); cr.set_line_width(4); cr.stroke()
        for k, x in enumerate((420, 820, 1220)):
            man(cr, x, 905, 0.9, t + k * 0.7, suit=(0.45, 0.40, 0.32) if k % 2 else (0.35, 0.38, 0.45), work=True,
                pose="hoe", prop="hoe")
        text(cr, "Worked the land the longest", W / 2, 200, 66, TEXT, alpha=prog(t, beat(i, "worked the land"), 0.4))
        pop_text(cr, "...but couldn't study there", W / 2, 300, 58, t, beat(i, "couldn't"), color=MAROON)
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    fade_edges(cr, t, a, b)


def s3(cr, t):  # Justin Morrill's second law (Aug 30, 1890): no money if race barred; unless separate college
    i = 3
    a, b = scene_bounds(i)
    bg(cr, (0.95, 0.92, 0.86), BG2)
    tn = beat(i, "No federal money")
    tu = beat(i, "Unless the state")
    p1 = 1 - prog(t, tn - 0.1, 0.35)
    if p1 > 0:
        cr.save(); cr.push_group()
        ground(cr, 900, (0.80, 0.72, 0.60))
        man(cr, 560, 905, 1.15, t, suit=CHAR, tie=(0.20, 0.25, 0.40), skin=SKIN_LT, hair=GRAY, whiskers=True,
            pose="rest", pose_to="hold", pose_t=prog(t, beat(i, "a second law,"), 0.5), prop="letter")
        name_tag(cr, "JUSTIN MORRILL", "of Vermont", 560, 930, prog(t, beat(i, "Justin Morrill"), 0.4), 46)
        pd = prog(t, beat(i, "a second law,"), 0.5)
        scroll(cr, 1330, 470, 640, 560, "SECOND MORRILL ACT", "Aug. 30, 1890", alpha=clamp(pd * 2), scale=back_out(pd))
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, tn, 0.4) * (1 - prog(t, tu - 0.1, 0.35))
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 880, FIELD)
        hall(cr, 1300, 882, 0.9, gate=1.0)
        money_bag(cr, 520, 640, 1.6)
        big_x(cr, 520, 610, 150, prog(t, beat(i, "by race."), 0.4))
        text(cr, "NO FEDERAL MONEY", 520, 230, 66, MAROON)
        text(cr, "if a college bars students by race", 520, 300, 40, TEXT, alpha=prog(t, beat(i, "turned students"), 0.4))
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    p3 = prog(t, tu, 0.4)
    if p3 > 0:
        cr.save(); cr.push_group()
        bg(cr, SKY, BG)
        ground(cr, 880, FIELD)
        text(cr, "...UNLESS", W / 2, 150, 80, MAROON)
        hall(cr, 480, 882, 0.75, brick=(0.70, 0.66, 0.60))
        ps = prog(t, beat(i, "a separate college"), 0.5)
        if ps > 0:
            cr.save(); cr.translate(1400, 882); cr.scale(back_out(ps), back_out(ps)); hall(cr, 0, 0, 0.75); cr.restore()
        text(cr, "a separate college", 1400, 950, 42, MAROON, alpha=ps)
        text(cr, "for Black students", 1400, 1005, 42, MAROON, alpha=prog(t, beat(i, "for Black students."), 0.4))
        if ps > 0:
            for k in range(3):
                kid(cr, 1180 + k * 70 + 80 * ease(prog(t, beat(i, "for Black students."), 1.0)), 905, 1.0,
                    dress=(PURPLE, NAVY, MAROON)[k], girl=k != 1, t=t + k, walking=True)
        cr.pop_group_to_source(); cr.paint_with_alpha(p3); cr.restore()
    fade_edges(cr, t, a, b)


SCHOOLS = ["Alabama A&M", "Alcorn State", "Delaware State", "Florida A&M", "Fort Valley State",
           "Kentucky State", "Langston", "Lincoln (Mo.)", "NC A&T", "Prairie View A&M", "SC State",
           "Southern", "Tennessee State", "Tuskegee", "UAPB", "UMES", "Virginia State", "West Virginia State",
           "Central State"]


def s4(cr, t):  # the 1890 universities: 19 today, Alabama A&M to Virginia State, and Tuskegee
    i = 4
    a, b = scene_bounds(i)
    bg(cr, (0.33, 0.07, 0.11), MAROON)
    pop_text(cr, "THE 1890 UNIVERSITIES", W / 2, 150, 84, t, a + 0.2, color=GOLDC)
    tt = beat(i, "Today there are")
    named = {"Alabama A&M": beat(i, "Alabama"), "Virginia State": beat(i, "Virginia State,"),
             "Tuskegee": beat(i, "Tuskegee.")}
    for k, name in enumerate(SCHOOLS):
        r, c = divmod(k, 4)
        x = 300 + c * 440; y = 270 + r * 150
        q = prog(t, tt + 0.08 * k, 0.3)
        if q <= 0:
            continue
        hl = name in named and t >= named[name]
        sc = back_out(q) * (1.12 if hl else 1.0)
        cr.save(); cr.translate(x, y + 55); cr.scale(sc, sc)
        panel(cr, -205, -55, 410, 110, GOLDC if hl else (1, 1, 1), r=20, lw=4)
        mini_hall(cr, -158, 32, 0.6)
        cr.save(); cr.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(40); tw = cr.text_extents(name).x_advance; cr.restore()
        fs = min(40, 40 * 300 / tw)
        text(cr, name, 40, 14, fs, MAROON if hl else TEXT)
        cr.restore()
    pn = prog(t, beat(i, "nineteen,"), 0.4)
    if pn > 0:
        text(cr, "19", 1820, 1040, 120, GOLDC, align="right", outline=INK, scale=back_out(pn))
    fade_edges(cr, t, a, b)


def s5(cr, t):  # the part most people never hear: "equitably divided"; 2023 letters; $12B+ gap 1987-2020
    i = 5
    a, b = scene_bounds(i)
    bg(cr, (0.90, 0.92, 0.95), (0.95, 0.93, 0.90))
    tl = beat(i, "The law said")
    ty = beat(i, "In twenty twenty-three,")
    tg = beat(i, "A gap of")
    p0 = prog(t, a + 0.1, 0.4) * (1 - prog(t, tl - 0.1, 0.35))
    if p0 > 0:
        cr.save(); cr.push_group()
        bo(cr, 960, 1020, 0.55, t, pose="shrug", wide=0.7, brow=0.9)
        text(cr, "The part most people never hear...", W / 2, 180, 70, MAROON)
        cr.pop_group_to_source(); cr.paint_with_alpha(p0); cr.restore()
    p1 = prog(t, tl, 0.4) * (1 - prog(t, ty - 0.1, 0.35))
    if p1 > 0:
        cr.save(); cr.push_group()
        bg(cr, BG, BG2)
        scroll(cr, 470, 540, 600, 640, "THE 1890 ACT", "funds \"equitably divided\"", seal=False)
        balance(cr, 1350, 930, 1.0, 0.0, (0.70, 0.66, 0.60), MAROON)
        pop_text(cr, "EQUITABLY", 1350, 200, 90, t, beat(i, "equitably."), color=MAROON)
        cr.pop_group_to_source(); cr.paint_with_alpha(p1); cr.restore()
    p2 = prog(t, ty, 0.4) * (1 - prog(t, tg - 0.1, 0.35))
    if p2 > 0:
        cr.save(); cr.push_group()
        bg(cr, (0.92, 0.93, 0.96), BG)
        ground(cr, 900, (0.80, 0.80, 0.78))
        text(cr, "2023", 140, 170, 100, MAROON, align="left")
        tc = beat(i, "two U.S. cabinet")
        for k, (x, suit) in enumerate(((330, NAVY), (560, CHAR))):
            man(cr, x, 905, 0.95, t + k, suit=suit, skin=SKIN_LT if k else BROWN_LT, pose="rest", pose_to="hold",
                pose_t=prog(t, tc, 0.5), prop="letter")
        text(cr, "Education + Agriculture", 445, 990, 40, TEXT, alpha=prog(t, tc, 0.4))
        text(cr, "secretaries", 445, 1040, 40, TEXT, alpha=prog(t, tc, 0.4))
        t16 = beat(i, "sixteen governors")
        for k in range(16):
            r, c = divmod(k, 4)
            q = prog(t, t16 + k * 0.06, 0.5)
            if q <= 0:
                continue
            sx, sy = 700, 600
            ex, ey = 1000 + c * 200, 300 + r * 150
            envelope(cr, sx + (ex - sx) * ease(q), sy + (ey - sy) * ease(q) - 80 * math.sin(math.pi * q), 0.9)
        pop_text(cr, "16 GOVERNORS", 1300, 200, 70, t, t16, color=MAROON)
        ps = prog(t, beat(i, "shortchanged."), 0.4)
        if ps > 0:
            cr.save(); cr.translate(1300, 960); cr.rotate(-0.06); cr.scale(1.4 - 0.4 * ease(ps), 1.4 - 0.4 * ease(ps))
            rounded_rect(cr, -280, -60, 560, 110, 16); cr.set_source_rgba(*RED, ps); cr.set_line_width(10); cr.stroke()
            text(cr, "SHORTCHANGED", 0, 18, 64, RED, alpha=ps)
            cr.restore()
        cr.pop_group_to_source(); cr.paint_with_alpha(p2); cr.restore()
    p3 = prog(t, tg, 0.4)
    if p3 > 0:
        cr.save(); cr.push_group()
        bg(cr, BG, BG2)
        text(cr, "STATE FUNDING GAP", W / 2, 150, 64, TEXT)
        pb = ease(prog(t, tg, 1.2))
        base = 860
        cr.rectangle(560, base - 560 * pb, 260, 560 * pb); cr.set_source_rgb(0.70, 0.66, 0.60); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
        cr.rectangle(1100, base - 300 * pb, 260, 300 * pb); cr.set_source_rgb(*MAROON); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.stroke()
        cr.move_to(400, base); cr.line_to(1520, base); cr.set_line_width(6); cr.stroke()
        text(cr, "other land-grant", 690, base + 60, 38, TEXT, alpha=pb)
        text(cr, "1890 HBCUs", 1230, base + 60, 38, MAROON, alpha=pb)
        pm = prog(t, beat(i, "twelve billion"), 0.5)
        if pm > 0:
            cr.move_to(1230, base - 300 * pb - 20); cr.line_to(1230, base - 560 * pb + 20)
            cr.set_source_rgb(*RED); cr.set_line_width(8); cr.set_dash([18, 12]); cr.stroke(); cr.set_dash([])
            text(cr, "$12 BILLION+", 1610, 470, 74, RED, outline=(1, 1, 1), scale=back_out(pm))
        pop_text(cr, "1987-2020", 1610, 570, 60, t, beat(i, "from nineteen eighty-seven"), color=TEXT)
        cr.pop_group_to_source(); cr.paint_with_alpha(p3); cr.restore()
    fade_edges(cr, t, a, b)


def s6(cr, t):  # outro / CTA with Bo
    i = 6
    a, b = scene_bounds(i)
    bg(cr)
    tq = beat(i, "and tell us which")
    bo(cr, 420, 1020, 0.6, t, pose="pockets", pose_to="point" if t < tq else "wave",
       pose_t=prog(t, a + 0.2, 0.5) if t < tq else prog(t, tq, 0.5), talk=t < P[i][1])
    pd = prog(t, a + 0.2, 0.5) * (1 - prog(t, tq - 0.2, 0.3))
    if pd > 0:
        text(cr, "Is your school", 1220, 360, 80, TEXT, alpha=pd)
        text(cr, "an 1890?", 1220, 520, 150, GOLDC, alpha=pd, outline=INK, scale=back_out(prog(t, beat(i, "an eighteen-ninety?"), 0.5)))
        pop_text(cr, "Tell us in the comments", 1220, 680, 56, t, beat(i, "Tell us in"))
    pq = prog(t, tq, 0.5)
    if pq > 0:
        text(cr, "Which HBCU", 1220, 330, 80, TEXT, alpha=pq)
        text(cr, "should we cover next?", 1220, 440, 76, MAROON, alpha=pq)
        pop_text(cr, "THE YARD", 1220, 640, 90, t, tq + 0.6, color=GOLDC, outline=INK)
    k = max(0, (t - (b - 0.8)) / 0.8)
    if k > 0:
        cr.set_source_rgba(*BG, k); cr.paint()


def thumb_hero(cr, x, y, r):
    """Hero object for thumbnails: a parchment law scroll stamped 1890."""
    cr.save(); cr.translate(x, y)
    w, h = r * 1.5, r * 1.8
    cr.rectangle(-w / 2, -h / 2, w, h); cr.set_source_rgb(*PAPER); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(r * 0.05); cr.stroke()
    for dy in (-h / 2, h / 2):
        cr.save(); cr.translate(0, dy); cr.scale(1, 0.3)
        rounded_rect(cr, -w / 2 - r * 0.12, -r * 0.3, w + r * 0.24, r * 0.6, r * 0.3); cr.restore()
        cr.set_source_rgb(0.90, 0.82, 0.62); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    text(cr, "1890", 0, -h * 0.05, r * 0.55, MAROON)
    cr.set_source_rgba(*INK, 0.35); cr.set_line_width(r * 0.04)
    for k in range(3):
        cr.move_to(-w * 0.35, h * 0.12 + k * r * 0.16); cr.line_to(w * 0.35, h * 0.12 + k * r * 0.16)
    cr.stroke()
    cr.arc(w * 0.3, h * 0.36, r * 0.16, 0, 2 * math.pi); cr.set_source_rgb(*MAROON); cr.fill()
    cr.restore()


SCENES = [s0, s1, s2, s3, s4, s5, s6]
