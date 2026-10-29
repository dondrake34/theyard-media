"""The Yard shared drawing library (1920x1080 scenes).

Episode scenes do `from lib import *`. The episode folder comes from the THEYARD_EP environment
variable and must contain narration.txt, words.tsv and timing.json (see wordsync.py)."""
import json, math, os, random
import cairo
from bo import draw_bo, rounded_rect, ease, INK, BLACK, CREAM, GOLD, GOLD_DK

W, H = 1920, 1080
BG = (0.97, 0.94, 0.88)
BG2 = (0.93, 0.88, 0.80)
MAROON = (0.47, 0.11, 0.16)
MAROON_DK = (0.33, 0.07, 0.11)
GOLDC = (0.89, 0.67, 0.20)
TEXT = (0.13, 0.10, 0.08)
SKY = (0.99, 0.86, 0.68)
GREEN = (0.45, 0.58, 0.36)
PURPLE = (0.36, 0.18, 0.40)
BROWN = (0.55, 0.36, 0.20)
BROWN_LT = (0.74, 0.55, 0.34)

EP = os.environ.get('THEYARD_EP', '.')
PARAS = [p.strip() for p in open(os.path.join(EP, 'narration.txt')).read().split('\n\n') if p.strip()]
TIM = json.load(open(os.path.join(EP, 'timing.json')))
DUR = TIM['duration']
P = TIM['paras']


def scene_bounds(i):
    a = 0.0 if i == 0 else P[i][0] - 0.25
    b = DUR + 1.5 if i == len(P) - 1 else P[i + 1][0] - 0.25
    return a, b


def beat(i, phrase, frac=0.0):
    """Absolute time (s) when `phrase` is spoken in paragraph i (estimated by character position)."""
    txt = PARAS[i]
    k = txt.find(phrase)
    assert k >= 0, phrase
    k += int(len(phrase) * frac)
    if 'token_times' in TIM:  # exact: word timestamps aligned by wordsync.py
        n = len(txt[:k].split())
        tt = TIM['token_times'][i]
        return tt[min(n, len(tt) - 1)]
    if 'para_words' in TIM:  # older format
        n = len(txt[:k].split())
        return WORDS[TIM['para_words'][i][0] + n][0]
    a, b = P[i]
    return a + (b - a) * k / len(txt)


WORDS = [(float(x), float(y), z) for x, y, z in
         (l.rstrip('\n').split('\t') for l in open(os.path.join(EP, 'words.tsv')) if l.strip())]


# ---------------- helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, start, dur=0.5):
    return clamp((t - start) / dur)


def back_out(x):
    x = clamp(x)
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def text(cr, s, x, y, size, color=TEXT, font="Poppins", bold=True, align="center", alpha=1.0,
         scale=1.0, outline=None):
    if alpha <= 0 or scale <= 0:
        return 0
    cr.save()
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    ext = cr.text_extents(s)
    w = ext.x_advance
    cr.translate(x, y)
    cr.scale(scale, scale)
    dx = {"center": -w / 2, "left": 0, "right": -w}[align]
    cr.move_to(dx, 0)
    cr.text_path(s)
    if outline:
        cr.set_source_rgba(*outline, alpha)
        cr.set_line_width(size * 0.16)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke_preserve()
    cr.set_source_rgba(*color, alpha)
    cr.fill()
    cr.restore()
    return w


def pop_text(cr, s, x, y, size, t, start, color=TEXT, **kw):
    p = prog(t, start, 0.45)
    text(cr, s, x, y, size, color, alpha=clamp(p * 2), scale=back_out(p), **kw)


def panel(cr, x, y, w, h, fill=(1, 1, 1), r=26, lw=5, alpha=1.0):
    rounded_rect(cr, x, y, w, h, r)
    cr.set_source_rgba(*fill, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(lw)
    cr.stroke()


def bg(cr, top=BG, bottom=BG2):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bottom)
    cr.set_source(g)
    cr.paint()


def ground(cr, y=900, color=(0.86, 0.80, 0.70)):
    cr.rectangle(0, y, W, H - y)
    cr.set_source_rgb(*color)
    cr.fill()
    cr.move_to(0, y); cr.line_to(W, y)
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()


def kicker(cr, s, t, start, x=96, y=110):
    """Small gold label top-left."""
    p = prog(t, start, 0.4)
    if p <= 0:
        return
    cr.save()
    cr.translate(-(1 - ease(p)) * 60, 0)
    cr.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(34)
    w = cr.text_extents(s).x_advance
    rounded_rect(cr, x - 22, y - 46, w + 44, 64, 14)
    cr.set_source_rgba(*MAROON, p); cr.fill()
    text(cr, s, x, y, 34, GOLDC, align="left", alpha=p)
    cr.restore()


def fade_edges(cr, t, a, b):
    """Short dip at scene start/end for soft cuts."""
    k = max(1 - clamp((t - a) / 0.3), 1 - clamp((b - t) / 0.3))
    if k > 0:
        cr.set_source_rgba(*BG, k * 0.9)
        cr.paint()


def bo(cr, x, y, s, t, **kw):
    draw_bo(cr, x, y, s, t=t, **kw)


# ---------------- props
def house(cr, x, y, s=1.0, door_open=0.0, glow=0.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    # body
    cr.rectangle(-210, -260, 420, 260)
    cr.set_source_rgb(0.80, 0.66, 0.48); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    cr.set_line_width(2.5); cr.set_source_rgba(*INK, 0.35)
    for yy in range(-235, 0, 26):
        cr.move_to(-208, yy); cr.line_to(208, yy)
    cr.stroke()
    # roof
    cr.move_to(-250, -255); cr.line_to(0, -420); cr.line_to(250, -255); cr.close_path()
    cr.set_source_rgb(*MAROON); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    # window
    cr.rectangle(70, -200, 95, 85)
    cr.set_source_rgb(1, 0.85 + 0.1 * glow, 0.5 + 0.3 * glow) if glow else cr.set_source_rgb(0.62, 0.75, 0.82)
    cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(117, -200); cr.line_to(117, -115); cr.move_to(70, -157); cr.line_to(165, -157); cr.stroke()
    # door frame (dark inside)
    cr.rectangle(-120, -180, 95, 180)
    cr.set_source_rgb(0.25, 0.17, 0.10); cr.fill()
    # door panel swings
    dw = 95 * (1 - 0.8 * door_open)
    cr.rectangle(-120, -180, dw, 180)
    cr.set_source_rgb(*BROWN); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.arc(-120 + dw - 14, -90, 6, 0, 2 * math.pi); cr.set_source_rgb(*GOLDC); cr.fill()
    cr.restore()


def dump_pile(cr, x, y, s=1.0, t=0.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-260, 0)
    cr.curve_to(-200, -150, -60, -190, 20, -170)
    cr.curve_to(120, -200, 230, -120, 270, 0)
    cr.close_path()
    cr.set_source_rgb(0.55, 0.50, 0.42); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(6); cr.stroke()
    random.seed(4)
    for _ in range(14):
        px = random.uniform(-200, 210); py = random.uniform(-150, -20)
        w = random.uniform(30, 70); h = random.uniform(16, 40); a = random.uniform(-0.6, 0.6)
        cr.save(); cr.translate(px, py); cr.rotate(a)
        cr.rectangle(-w / 2, -h / 2, w, h)
        cr.set_source_rgb(*random.choice([(0.70, 0.62, 0.50), (0.45, 0.42, 0.38), (0.80, 0.74, 0.62), BROWN_LT]))
        cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
        cr.restore()
    # flies
    for k in range(3):
        fx = math.sin(t * 3 + k * 2) * 90 + k * 30 - 30
        fy = -230 + math.cos(t * 4 + k) * 30
        cr.arc(fx, fy, 4, 0, 2 * math.pi); cr.set_source_rgb(*INK); cr.fill()
    cr.restore()
    text(cr, "CITY DUMP", x, y + 50, 30, (0.45, 0.40, 0.33))


def crate(cr, x, y, w=150, h=100, label=None):
    cr.rectangle(x - w / 2, y - h, w, h)
    cr.set_source_rgb(*BROWN_LT); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.set_line_width(3)
    for k in (1, 2):
        cr.move_to(x - w / 2, y - h + k * h / 3); cr.line_to(x + w / 2, y - h + k * h / 3)
    cr.move_to(x - w / 2, y - h); cr.line_to(x + w / 2, y)
    cr.stroke()


def coin(cr, x, y, r, label="$1.50", spin=0.0):
    sx = abs(math.cos(spin)) * 0.85 + 0.15
    cr.save(); cr.translate(x, y); cr.scale(sx, 1)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLDC); cr.fill_preserve()
    cr.set_source_rgb(*GOLD_DK); cr.set_line_width(r * 0.08); cr.stroke()
    cr.arc(0, 0, r * 0.8, 0, 2 * math.pi); cr.set_line_width(r * 0.03); cr.stroke()
    cr.restore()
    if sx > 0.5:
        text(cr, label, x, y + r * 0.2, r * 0.55, GOLD_DK, alpha=(sx - 0.5) * 2)


def kid(cr, x, y, s=1.0, dress=MAROON, girl=True, t=0.0, walking=False):
    """Simple stylized child figure (no detailed features)."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    sw = math.sin(t * 9) * 12 if walking else 0
    cr.set_source_rgb(*BLACK)
    cr.set_line_width(14); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(-14, -70); cr.line_to(-14 - sw, 0)
    cr.move_to(14, -70); cr.line_to(14 + sw, 0)
    cr.stroke()
    if girl:
        cr.move_to(-40, -60); cr.line_to(-22, -170); cr.line_to(22, -170); cr.line_to(40, -60); cr.close_path()
    else:
        cr.rectangle(-28, -170, 56, 100)
    cr.set_source_rgb(*dress); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.arc(0, -205, 36, 0, 2 * math.pi)
    cr.set_source_rgb(*BLACK); cr.fill()
    if girl:
        for dx in (-30, 30):
            cr.arc(dx, -232, 13, 0, 2 * math.pi); cr.fill()
    cr.arc(-12, -208, 7, 0, 2 * math.pi); cr.arc(12, -208, 7, 0, 2 * math.pi)
    cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.restore()


MARY_POSES = {  # (elbow, hand) for viewer-left / viewer-right arm, relative to her origin (feet)
    "rest":    (((-70, -230), (-20, -180)), ((70, -230), (20, -180))),
    "welcome": (((-110, -250), (-175, -300)), ((110, -250), (175, -300))),
    "hold":    (((-70, -230), (-20, -180)), ((105, -280), (160, -370))),
    "think":   (((-70, -230), (-20, -180)), ((80, -260), (25, -335))),
    "knock":   (((-70, -230), (-20, -180)), ((110, -290), (150, -330))),
}
DRESS = (0.24, 0.17, 0.27)


def mary(cr, x, y, s=1.0, t=0.0, pose="rest", pose_to=None, pose_t=0.0, letter=False, knock=False, label=False,
         label_alpha=1.0, flip=False):
    """Stylized Mary McLeod Bethune: long dark dress, white collar, hair bun, simple arms."""
    cr.save(); cr.translate(x, y); cr.scale(s * (-1 if flip else 1), s)
    cr.save(); cr.scale(1, 0.12); cr.arc(0, 30, 150, 0, 2 * math.pi); cr.restore()
    cr.set_source_rgba(0, 0, 0, 0.12); cr.fill()
    bob = math.sin(t * 2.0) * 3
    # dress
    cr.move_to(-100, 0); cr.curve_to(-85, -150, -62, -260, -55, -330 + bob)
    cr.line_to(55, -330 + bob); cr.curve_to(62, -260, 85, -150, 100, 0); cr.close_path()
    cr.set_source_rgb(*DRESS); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    # waist band
    cr.move_to(-62, -240 + bob); cr.line_to(62, -240 + bob)
    cr.set_source_rgb(0.12, 0.08, 0.14); cr.set_line_width(10); cr.stroke()
    # shoes
    for dx in (-45, 45):
        cr.save(); cr.translate(dx, 2); cr.scale(1, 0.5); cr.arc(0, 0, 26, math.pi, 2 * math.pi); cr.restore()
        cr.set_source_rgb(*BLACK); cr.fill()
    # arms
    pa = MARY_POSES[pose]; pb = MARY_POSES[pose_to] if pose_to else pa
    k = ease(pose_t) if pose_to else 0.0
    for side, sx in ((0, -55), (1, 55)):
        (ea, ha), (eb, hb) = pa[side], pb[side]
        e = (ea[0] + (eb[0] - ea[0]) * k, ea[1] + (eb[1] - ea[1]) * k + bob)
        h = [ha[0] + (hb[0] - ha[0]) * k, ha[1] + (hb[1] - ha[1]) * k + bob]
        if knock and side == 1:
            h[0] += abs(math.sin(t * 10)) * 18
        sh = (sx, -315 + bob)
        for w, col in ((40, INK), (30, DRESS)):
            cr.move_to(*sh); cr.line_to(*e); cr.line_to(*h)
            cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_line_width(w); cr.set_source_rgb(*col); cr.stroke()
        cr.arc(h[0], h[1], 15, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
        if letter and side == 1:
            cr.save(); cr.translate(h[0], h[1] - 30); cr.rotate(-0.15)
            cr.rectangle(-36, -26, 72, 52); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
            cr.move_to(-36, -26); cr.line_to(0, 4); cr.line_to(36, -26); cr.stroke()
            cr.restore()
    # collar
    cr.move_to(-34, -330 + bob); cr.line_to(0, -296 + bob); cr.line_to(34, -330 + bob); cr.close_path()
    cr.set_source_rgb(1, 1, 1); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    # head + bun
    hy = -380 + bob
    cr.arc(0, hy - 48, 27, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
    cr.arc(0, hy, 50, 0, 2 * math.pi); cr.fill()
    # eyes with blink
    ph = (t + 1.7) % 4.1
    open_ = 0.25 if ph < 0.14 else 1.0
    for dx in (-17, 17):
        cr.save(); cr.translate(dx, hy - 2); cr.scale(1, open_); cr.arc(0, 0, 9, 0, 2 * math.pi); cr.restore()
        cr.set_source_rgb(1, 1, 1); cr.fill()
        if open_ > 0.5:
            cr.arc(dx + 1, hy - 1, 4, 0, 2 * math.pi); cr.set_source_rgb(*BLACK); cr.fill()
    # small smile
    cr.arc(0, hy + 16, 14, 0.2 * math.pi, 0.8 * math.pi)
    cr.set_source_rgb(0.45, 0.40, 0.38); cr.set_line_width(4); cr.stroke()
    cr.restore()
    if label:
        text(cr, "MARY McLEOD BETHUNE", x, y + 55, 34, MAROON, alpha=label_alpha)


def building(cr, x, y, w, h, color, label=None, cols=3):
    cr.rectangle(x - w / 2, y - h, w, h)
    cr.set_source_rgb(*color); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.move_to(x - w / 2 - 20, y - h); cr.line_to(x, y - h - 90); cr.line_to(x + w / 2 + 20, y - h); cr.close_path()
    cr.set_source_rgb(*MAROON); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    for r in range(2):
        for c in range(cols):
            wx = x - w / 2 + (c + 0.5) * w / cols - 22
            wy = y - h + 40 + r * 90
            cr.rectangle(wx, wy, 44, 56)
            cr.set_source_rgb(0.98, 0.88, 0.60); cr.fill_preserve()
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.stroke()
    if label:
        text(cr, label, x, y + 52, 34, TEXT)


def capitol(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    c = (0.96, 0.95, 0.92)
    def box(a, b, w, h):
        cr.rectangle(a, b, w, h); cr.set_source_rgb(*c); cr.fill_preserve()
        cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    box(-420, -150, 840, 150)
    for k in range(-400, 410, 50):
        cr.move_to(k, -140); cr.line_to(k, -10)
    cr.set_line_width(3); cr.stroke()
    box(-150, -240, 300, 90)
    box(-110, -330, 220, 90)
    cr.arc(0, -330, 120, math.pi, 0); cr.close_path()
    cr.set_source_rgb(*c); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    box(-16, -500, 32, 50)
    cr.arc(0, -505, 14, 0, 2 * math.pi); cr.set_source_rgb(*c); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.restore()


def statue(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    m = (0.93, 0.92, 0.90)
    cr.rectangle(-110, -120, 220, 120); cr.set_source_rgb(0.80, 0.78, 0.74); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    # robed figure in marble
    cr.move_to(-90, -120); cr.curve_to(-80, -260, -60, -380, -55, -440)
    cr.line_to(55, -440); cr.curve_to(60, -380, 80, -260, 90, -120); cr.close_path()
    cr.set_source_rgb(*m); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    cr.rectangle(-70, -560, 140, 22); cr.fill_preserve() if False else None
    cr.arc(0, -490, 48, 0, 2 * math.pi); cr.set_source_rgb(*m); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    # mortarboard
    cr.move_to(-75, -548); cr.line_to(0, -573); cr.line_to(75, -548); cr.line_to(0, -523); cr.close_path()
    cr.set_source_rgb(*m); cr.fill_preserve(); cr.set_source_rgb(*INK); cr.stroke()
    # rose in hand
    cr.move_to(40, -300); cr.line_to(70, -360); cr.set_source_rgb(0.3, 0.45, 0.3); cr.set_line_width(5); cr.stroke()
    cr.arc(72, -368, 14, 0, 2 * math.pi); cr.set_source_rgb(0.15, 0.12, 0.12); cr.fill()
    cr.restore()


def envelope(cr, x, y, s=1.0, rot=0.0):
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(s, s)
    cr.rectangle(-70, -45, 140, 90); cr.set_source_rgb(1, 1, 1); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.move_to(-70, -45); cr.line_to(0, 10); cr.line_to(70, -45); cr.stroke()
    cr.arc(0, 8, 10, 0, 2 * math.pi); cr.set_source_rgb(*MAROON); cr.fill()
    cr.restore()


def pie(cr, x, y, r=70):
    cr.save(); cr.translate(x, y); cr.scale(1, 0.45)
    cr.arc(0, 0, r, 0, 2 * math.pi); cr.set_source_rgb(0.85, 0.65, 0.40); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(8); cr.stroke()
    cr.arc(0, -6, r * 0.78, 0, 2 * math.pi); cr.set_source_rgb(0.86, 0.45, 0.18); cr.fill()
    cr.restore()


def subscribe_btn(cr, x, y, t, start):
    p = back_out(prog(t, start, 0.5))
    if p <= 0:
        return
    pressed = t > start + 1.4
    cr.save(); cr.translate(x, y); cr.scale(p, p)
    rounded_rect(cr, -230, -60, 460, 120, 60)
    cr.set_source_rgb(*((0.5, 0.5, 0.5) if pressed else (0.82, 0.12, 0.12))); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    text(cr, "SUBSCRIBED" if pressed else "SUBSCRIBE", 0, 18, 50, (1, 1, 1))
    cr.restore()


