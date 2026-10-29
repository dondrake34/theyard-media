"""Bo character rig, drawn with cairo. Local origin = point between the feet on the ground.
Units follow the 1024x1536 reference sheet (Bo is ~1450 units tall)."""
import math
import cairo

INK = (0.13, 0.10, 0.08)          # outline
BLACK = (0.07, 0.065, 0.06)       # skin / pants
CREAM = (0.95, 0.91, 0.83)        # sweater
CREAM_SH = (0.88, 0.82, 0.72)     # sweater shade
SHOE = (0.97, 0.95, 0.90)
GOLD = (0.89, 0.67, 0.20)
GOLD_DK = (0.70, 0.50, 0.12)
WHITE = (1, 1, 1)

LW = 6


def _rgb(c, a=1.0):
    return (*c, a)


def fill_stroke(cr, fill, lw=LW, stroke=INK):
    cr.set_source_rgb(*fill)
    cr.fill_preserve()
    cr.set_source_rgb(*stroke)
    cr.set_line_width(lw)
    cr.stroke()


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_pt(p, q, t):
    return (lerp(p[0], q[0], t), lerp(p[1], q[1], t))


# ---- arm poses: (elbow, hand, hand_visible) per side; side = -1 (viewer left) / +1 (viewer right)
POSES = {
    "pockets": {-1: ((-205, -905), (-150, -762), False), 1: ((205, -905), (148, -762), False)},
    "point":   {-1: ((-205, -905), (-150, -762), False), 1: ((285, -985), (395, -1105), True)},
    "present": {-1: ((-255, -900), (-330, -905), True), 1: ((255, -900), (330, -905), True)},
    "wave":    {-1: ((-205, -905), (-150, -762), False), 1: ((290, -1060), (300, -1250), True)},
    "think":   {-1: ((-205, -905), (-150, -762), False), 1: ((250, -930), (95, -1110), True)},
    "shrug":   {-1: ((-265, -960), (-345, -1040), True), 1: ((265, -960), (345, -1040), True)},
    "hold":    {-1: ((-205, -905), (-150, -762), False), 1: ((260, -900), (230, -1000), True)},
}


def blend_pose(a, b, t):
    pa, pb = POSES[a], POSES[b]
    out = {}
    for s in (-1, 1):
        ea, ha, va = pa[s]
        eb, hb, vb = pb[s]
        vis = (va if t < 0.5 else vb) if va != vb else va
        out[s] = (lerp_pt(ea, eb, t), lerp_pt(ha, hb, t), vis)
    return out


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def draw_shoe(cr, side):
    # side -1 left shoe (toe points left), +1 right shoe
    s = side
    cr.save()
    cr.scale(s, 1)
    # base x from inner (heel/leg) to outer (toe); coordinates for right shoe
    cr.new_path()
    cr.move_to(40, 12)
    cr.line_to(235, 12)
    cr.curve_to(262, 12, 262, -35, 240, -48)
    cr.curve_to(205, -70, 170, -78, 140, -112)
    cr.line_to(128, -150)
    cr.curve_to(105, -168, 70, -168, 52, -152)
    cr.curve_to(40, -110, 34, -50, 40, 12)
    cr.close_path()
    fill_stroke(cr, SHOE)
    # gold sole stripe
    cr.new_path()
    cr.move_to(42, 12)
    cr.line_to(236, 12)
    cr.curve_to(250, 12, 256, 0, 254, -12)
    cr.line_to(44, -12)
    cr.close_path()
    fill_stroke(cr, GOLD, lw=4)
    # toe cap seam
    cr.new_path()
    cr.move_to(170, -12)
    cr.curve_to(175, -40, 205, -58, 238, -46)
    cr.set_source_rgb(*INK)
    cr.set_line_width(3)
    cr.stroke()
    # gold heel tab (no logos)
    cr.new_path()
    cr.rectangle(60, -150, 34, 30)
    fill_stroke(cr, GOLD, lw=3)
    # laces
    cr.set_line_width(4)
    for i in range(4):
        y = -128 + i * 18
        cr.move_to(108 + i * 8, y)
        cr.line_to(150 + i * 10, y + 10)
    cr.set_source_rgb(*CREAM_SH)
    cr.stroke()
    cr.restore()


def draw_legs(cr, step=0.0):
    # step: walking offset -1..1 shifts legs slightly
    for side in (-1, 1):
        sh = side * step * 18
        cr.new_path()
        if side < 0:
            cr.move_to(-128, -770)
            cr.line_to(-10, -770)
            cr.line_to(-18 + sh, -690)
            cr.line_to(-45 + sh, -105)
            cr.line_to(-140 + sh, -105)
            cr.line_to(-138, -600)
        else:
            cr.move_to(10, -770)
            cr.line_to(128, -770)
            cr.line_to(138, -600)
            cr.line_to(140 + sh, -105)
            cr.line_to(45 + sh, -105)
            cr.line_to(18 + sh, -690)
        cr.close_path()
        fill_stroke(cr, BLACK)
        # crease
        cr.move_to(side * 75, -700)
        cr.line_to(side * 92 + sh, -170)
        cr.set_source_rgba(0.25, 0.22, 0.2, 0.7)
        cr.set_line_width(3)
        cr.stroke()
    # waist band
    cr.rectangle(-128, -782, 256, 26)
    fill_stroke(cr, BLACK, lw=4)


def draw_torso(cr, breathe=0.0):
    b = breathe * 4
    cr.new_path()
    cr.move_to(-62, -1108)
    cr.curve_to(-120, -1100, -165, -1085, -178, -1040)
    cr.curve_to(-185, -960, -168, -860, -158, -770 + b)
    cr.line_to(158, -770 + b)
    cr.curve_to(168, -860, 185, -960, 178, -1040)
    cr.curve_to(165, -1085, 120, -1100, 62, -1108)
    cr.close_path()
    fill_stroke(cr, CREAM)
    # rib lines
    cr.set_line_width(2)
    cr.set_source_rgba(*CREAM_SH, 0.9)
    for x in range(-140, 150, 22):
        cr.move_to(x, -1060 if abs(x) < 120 else -1020)
        cr.line_to(x * 0.97, -800)
    cr.stroke()
    # hem band
    cr.new_path()
    cr.move_to(-160, -805 + b)
    cr.line_to(160, -805 + b)
    cr.line_to(158, -770 + b)
    cr.line_to(-158, -770 + b)
    cr.close_path()
    fill_stroke(cr, CREAM, lw=4)
    cr.set_line_width(2)
    cr.set_source_rgb(*CREAM_SH)
    for x in range(-150, 160, 10):
        cr.move_to(x, -803 + b)
        cr.line_to(x, -773 + b)
    cr.stroke()


def draw_neck_collar(cr):
    cr.rectangle(-32, -1160, 64, 60)
    cr.set_source_rgb(*BLACK)
    cr.fill()
    # collar rib ring
    cr.save()
    cr.translate(0, -1104)
    cr.scale(1, 0.32)
    cr.new_path()
    cr.arc(0, 0, 80, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgb(*CREAM)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(5)
    cr.stroke()
    cr.save()
    cr.translate(0, -1108)
    cr.scale(1, 0.26)
    cr.new_path()
    cr.arc(0, 0, 50, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgb(*BLACK)
    cr.fill()


def draw_chain(cr, swing=0.0):
    px = swing * 6
    cr.set_source_rgb(*GOLD_DK)
    cr.set_line_width(7)
    cr.move_to(-44, -1110)
    cr.curve_to(-40, -1060, -15 + px, -1030, px, -1018)
    cr.move_to(44, -1110)
    cr.curve_to(40, -1060, 15 + px, -1030, px, -1018)
    cr.stroke()
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(4)
    cr.move_to(-44, -1110)
    cr.curve_to(-40, -1060, -15 + px, -1030, px, -1018)
    cr.move_to(44, -1110)
    cr.curve_to(40, -1060, 15 + px, -1030, px, -1018)
    cr.stroke()
    cr.new_path()
    rounded_rect(cr, px - 17, -1015, 34, 54, 5)
    fill_stroke(cr, GOLD, lw=4, stroke=GOLD_DK)
    cr.rectangle(px - 9, -1006, 18, 36)
    cr.set_source_rgba(1, 0.9, 0.55, 0.5)
    cr.fill()


def rounded_rect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def draw_arm(cr, side, elbow, hand, visible, wave_rot=0.0):
    sh = (side * 158, -1045)
    pts = [sh, elbow, hand]
    # outline then fill
    for w, col in ((98, INK), (86, CREAM)):
        cr.new_path()
        cr.move_to(*pts[0])
        cr.line_to(*pts[1])
        cr.line_to(*pts[2])
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_width(w)
        cr.set_source_rgb(*col)
        cr.stroke()
    # sleeve fold
    cr.set_source_rgb(*CREAM_SH)
    cr.set_line_width(3)
    mx, my = lerp_pt(elbow, hand, 0.55)
    cr.move_to(mx - 22, my - 6)
    cr.line_to(mx + 22, my + 6)
    cr.stroke()
    if visible:
        dx, dy = hand[0] - elbow[0], hand[1] - elbow[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        hx, hy = hand[0] + ux * 40, hand[1] + uy * 40
        cr.new_path()
        cr.arc(hx, hy, 30, 0, 2 * math.pi)
        fill_stroke(cr, BLACK, lw=4)
        # thumb
        cr.new_path()
        cr.arc(hx - uy * 26 * side, hy + ux * 26 * side, 12, 0, 2 * math.pi)
        fill_stroke(cr, BLACK, lw=3)
    if side == -1:
        # gold watch at the cuff
        wx, wy = lerp_pt(elbow, hand, 0.92)
        cr.new_path()
        cr.arc(wx, wy, 27, 0, 2 * math.pi)
        fill_stroke(cr, GOLD, lw=4, stroke=GOLD_DK)
        cr.new_path()
        cr.arc(wx, wy, 17, 0, 2 * math.pi)
        fill_stroke(cr, WHITE, lw=2, stroke=GOLD_DK)
        cr.set_source_rgb(*INK)
        cr.set_line_width(2)
        cr.move_to(wx, wy)
        cr.line_to(wx, wy - 11)
        cr.move_to(wx, wy)
        cr.line_to(wx + 8, wy)
        cr.stroke()


def draw_head(cr, blink=0.0, look=(0.0, 0.0), brow=0.0, wide=0.0, tilt=0.0, mouth=None):
    cr.save()
    cr.translate(0, -1160)
    cr.rotate(tilt)
    cr.translate(0, 1160)
    hx, hy, r = -2, -1282, 153
    cr.new_path()
    cr.arc(hx, hy, r, 0, 2 * math.pi)
    fill_stroke(cr, BLACK, lw=5)
    # soft highlight
    g = cairo.RadialGradient(hx + 25, hy - 95, 5, hx + 25, hy - 95, 90)
    g.add_color_stop_rgba(0, 0.35, 0.30, 0.27, 0.55)
    g.add_color_stop_rgba(1, 0.35, 0.30, 0.27, 0.0)
    cr.arc(hx, hy, r - 3, 0, 2 * math.pi)
    cr.set_source(g)
    cr.fill()
    # eyes
    lid_base = 0.45 - 0.35 * wide   # fraction of eye covered by lid (half-lidded default)
    lid = lid_base + (1 - lid_base) * blink
    for side, ex in ((-1, -66), (1, 66)):
        ey = -1240
        ew, eh = 52, 40
        cr.save()
        cr.translate(ex, ey)
        cr.scale(ew, eh)
        cr.new_path()
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.save()
        cr.clip_preserve()
        cr.set_source_rgb(*WHITE)
        cr.fill()
        # pupil
        px = ex + look[0] * 20 + (10 if side < 0 else -10)
        py = ey + 6 + look[1] * 10
        cr.new_path()
        cr.arc(px, py, 15, 0, 2 * math.pi)
        cr.set_source_rgb(*BLACK)
        cr.fill()
        cr.new_path()
        cr.arc(px + 5, py - 5, 4, 0, 2 * math.pi)
        cr.set_source_rgb(*WHITE)
        cr.fill()
        # lid (skin colour) covering top part
        top = ey - eh
        ly = top + 2 * eh * lid
        cr.new_path()
        cr.rectangle(ex - ew - 4, top - 4, 2 * ew + 8, ly - top + 4)
        cr.set_source_rgb(*BLACK)
        cr.fill()
        cr.restore()
        # lid line
        cr.new_path()
        cr.move_to(ex - ew + 4, ly)
        cr.line_to(ex + ew - 4, ly)
        cr.set_source_rgb(0.02, 0.02, 0.02)
        cr.set_line_width(7)
        cr.stroke()
        # eye outline
        cr.save()
        cr.translate(ex, ey)
        cr.scale(ew, eh)
        cr.new_path()
        cr.arc(0, 0, 1, math.asin(max(-1, min(1, (ly - ey) / eh))), math.pi - math.asin(max(-1, min(1, (ly - ey) / eh))))
        cr.restore()
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.set_line_width(3)
        cr.stroke()
    if mouth == "o":  # shocked open mouth (thumbnails)
        cr.save(); cr.translate(0, -1172); cr.scale(30, 38)
        cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(0.45, 0.10, 0.12); cr.fill_preserve()
        cr.set_source_rgb(0.30, 0.27, 0.25); cr.set_line_width(5); cr.stroke()
        cr.save(); cr.translate(0, -1158); cr.scale(18, 12)
        cr.arc(0, 0, 1, 0, math.pi); cr.restore()
        cr.set_source_rgb(0.85, 0.35, 0.38); cr.fill()
    # brows (dark grey so they read on black)
    cr.set_source_rgb(0.30, 0.27, 0.25)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    by = -1322 - brow * 22
    cr.set_line_width(7)
    cr.move_to(-112, by + 4)
    cr.curve_to(-85, by - 12, -45, by - 12, -20, by + 2)
    cr.stroke()
    cr.set_line_width(12)
    cr.move_to(28, by + 22 - brow * 8)
    cr.curve_to(55, by + 4, 90, by + 2, 115, by + 14)
    cr.stroke()
    cr.restore()


def draw_bo(cr, x, y, scale, t=0.0, pose="pockets", pose_to=None, pose_t=0.0,
            blink=None, look=(0.0, 0.0), brow=0.0, wide=0.0, tilt=0.0, bob=True,
            talk=False, flip=False, step=0.0, shadow=True, mouth=None):
    """Draw Bo with feet at (x, y). t (seconds) drives idle motion."""
    cr.save()
    cr.translate(x, y)
    cr.scale(scale * (-1 if flip else 1), scale)
    if shadow:
        cr.save()
        cr.scale(1, 0.12)
        cr.arc(0, 30, 330, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(0, 0, 0, 0.12)
        cr.fill()
    breathe = math.sin(t * 2.2) * 0.5 + 0.5
    if blink is None:
        # natural blinks every ~3.7 s
        ph = (t + 0.9) % 3.7
        blink = max(0.0, 1 - abs(ph - 0.08) / 0.08) if ph < 0.16 else 0.0
    bob_y = -abs(math.sin(t * 5.0)) * 6 if (talk and bob) else (math.sin(t * 2.2) * 3 if bob else 0)
    tilt_total = tilt + (math.sin(t * 1.3) * 0.025 if bob else 0) + (math.sin(t * 3.1) * 0.02 if talk else 0)

    if pose_to is not None:
        arms = blend_pose(pose, pose_to, ease(pose_t))
    else:
        arms = {s: POSES[pose][s] for s in (-1, 1)}
    # waving motion
    wave_amt = 0.0
    if (pose == "wave" and pose_to is None) or (pose_to == "wave" and pose_t >= 1):
        wave_amt = math.sin(t * 9) * 45
        e, h, v = arms[1]
        arms[1] = (e, (h[0] + wave_amt, h[1] + abs(wave_amt) * 0.15), v)

    draw_legs(cr, step)
    cr.save(); cr.translate(10, 0); cr.scale(0.78, 0.85); draw_shoe(cr, -1); cr.restore()
    cr.save(); cr.translate(-10, 0); cr.scale(0.78, 0.85); draw_shoe(cr, 1); cr.restore()
    cr.save()
    cr.translate(0, bob_y)
    draw_torso(cr, breathe)
    draw_neck_collar(cr)
    draw_chain(cr, math.sin(t * 2.2))
    for s in (-1, 1):
        e, h, v = arms[s]
        draw_arm(cr, s, e, h, v)
    draw_head(cr, blink=blink, look=look, brow=brow, wide=wide, tilt=tilt_total, mouth=mouth)
    cr.restore()
    cr.restore()
