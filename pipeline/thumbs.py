"""Thumbnails: 3 YouTube variants (1280x720 JPG) + vertical Short cover (1080x1920 PNG/JPG).

Usage: python3 thumbs.py EP_DIR
Reads EP_DIR/thumbs.json:
  {
    "variants": [["NEXT TO", "A DUMP"], ["INTO A", "COLLEGE?"], ["5 GIRLS.", "1 COLLEGE."]],  # first = main
    "hero_text": "$1.50",                       # text on the default glowing coin
    "cover": ["SHE BUILT", "A COLLEGE", "WITH"] # vertical cover: 2 white lines + 1 gold line above the hero
  }
If the episode's scenes.py defines thumb_hero(cr, x, y, r), that draws the hero object instead of the coin
(e.g. a book, a trophy, a building). Keep it ONE bold object that reads at phone size.

Design rules (from CTR research, see PIPELINE.md): Bo big and shocked (wide eyes, raised brows, gold shock
lines; NEVER a mouth), one hero object, 3-5 words that tease rather than repeat the title, navy + gold +
white, nothing important bottom-right (duration stamp), must read at 168x94.
"""
import importlib.util, json, math, os, sys

EP = os.path.abspath(sys.argv[1])
os.environ['THEYARD_EP'] = EP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('ep_scenes', os.path.join(EP, 'scenes.py'))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import cairo  # noqa: E402
from PIL import Image  # noqa: E402
from bo import draw_bo  # noqa: E402
from lib import text, coin, INK  # noqa: E402

CFG = json.load(open(os.path.join(EP, 'thumbs.json')))
NAVY = (0.05, 0.09, 0.22); NAVY2 = (0.10, 0.17, 0.38); NEON = (1.0, 0.80, 0.12)


def backdrop(cr, w, h, cx, cy):
    g = cairo.RadialGradient(cx, cy, 30, cx, cy, max(w, h) * 0.75)
    g.add_color_stop_rgb(0, *NAVY2); g.add_color_stop_rgb(1, *NAVY)
    cr.set_source(g); cr.paint()
    cr.save(); cr.translate(cx, cy)
    for _ in range(24):
        cr.rotate(math.pi / 12)
        cr.move_to(0, 0); cr.line_to(2200, -110); cr.line_to(2200, 110); cr.close_path()
    cr.set_source_rgba(1, 0.85, 0.3, 0.07); cr.fill(); cr.restore()


def hero(cr, x, y, r):
    for k in range(10, 0, -1):
        cr.arc(x, y, r + k * 9, 0, 2 * math.pi); cr.set_source_rgba(1, 0.8, 0.2, 0.035); cr.fill()
    if hasattr(mod, 'thumb_hero'):
        mod.thumb_hero(cr, x, y, r); return
    coin(cr, x, y, r, label="")
    t = CFG.get('hero_text', '')
    text(cr, t, x, y + r * 0.2, r * (0.6 if len(t) <= 5 else 3.0 / max(5, len(t))), (0.30, 0.16, 0.04))
    cr.save(); cr.arc(x, y, r * 0.92, 0, 2 * math.pi); cr.clip()
    cr.move_to(x - r, y - r * 0.2); cr.line_to(x - r * 0.2, y - r); cr.line_to(x + r * 0.05, y - r)
    cr.line_to(x - r, y + r * 0.05); cr.close_path(); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill(); cr.restore()


def shocked_bo(cr, x, y, s, pose="point"):
    draw_bo(cr, x, y, s, t=0.0, pose=pose, wide=1.0, brow=1.6, look=(0.6, -0.4), blink=0.0, bob=False, shadow=False)
    hx, hy, r = x - 2 * s, y - 1282 * s, 153 * s
    cr.set_source_rgb(*NEON); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_width(9 * s)
    for ang in (-2.35, -1.95, -1.57, -1.19, -0.79):
        cr.move_to(hx + math.cos(ang) * (r + 25 * s), hy + math.sin(ang) * (r + 25 * s))
        cr.line_to(hx + math.cos(ang) * (r + 75 * s), hy + math.sin(ang) * (r + 75 * s))
    cr.stroke()


def fit(s, size, maxw):
    return size if len(s) * size * 0.62 <= maxw else maxw / (len(s) * 0.62)


def yt(k, top, big):
    W, H = 1920, 1080
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cr = cairo.Context(s)
    backdrop(cr, W, H, 1330, 700)
    hero(cr, 1330, 700, 260)
    shocked_bo(cr, 300, 2900, 1.85)
    text(cr, top, 1330, 165, fit(top, 110, 1100), (1, 1, 1), outline=INK)
    text(cr, big, 1330, 320, fit(big, 140, 1100), NEON, outline=INK)
    png = os.path.join(EP, f'thumb_{k}.png'); s.write_to_png(png)
    Image.open(png).convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(EP, f'thumb_{k}.jpg'), quality=92)


def cover():
    W, H = 1080, 1920
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cr = cairo.Context(s)
    backdrop(cr, W, H, 540, 820)
    l1, l2, l3 = CFG['cover']
    text(cr, l1, 540, 250, fit(l1, 120, 980), (1, 1, 1), outline=INK)
    text(cr, l2, 540, 380, fit(l2, 120, 980), (1, 1, 1), outline=INK)
    text(cr, l3, 540, 490, fit(l3, 80, 980), NEON, outline=INK)
    hero(cr, 540, 760, 210)
    shocked_bo(cr, 540, 2700, 1.12, pose="shrug")
    png = os.path.join(EP, 'cover_short.png'); s.write_to_png(png)
    Image.open(png).convert('RGB').save(os.path.join(EP, 'cover_short.jpg'), quality=92)


if __name__ == '__main__':
    for k, (top, big) in enumerate(CFG['variants']):
        yt('ABC'[k], top, big)
    cover()
    ims = [Image.open(os.path.join(EP, f'thumb_{c}.jpg')) for c in 'ABC'[:len(CFG['variants'])]]
    sheet = Image.new('RGB', (1280 + 200 + 420, 560 * len(ims)), 'white')
    for k, im in enumerate(ims):
        sheet.paste(im.resize((960, 540)), (0, k * 560)); sheet.paste(im.resize((168, 94)), (980, k * 560 + 20))
    sheet.paste(Image.open(os.path.join(EP, 'cover_short.jpg')).resize((405, 720)), (1180 + 260, 0))
    sheet.save(os.path.join(EP, 'thumb_sheet.png'))
    print('thumbnails written; check thumb_sheet.png')
