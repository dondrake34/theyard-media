"""Build the vertical 1080x1920 Short from an episode's 16:9 scenes.

Usage: python3 make_short.py EP_DIR OUT.mp4 [--stills PNG]
Reads EP_DIR/short.json:
  {
    "header": ["SHE BUILT A COLLEGE", "WITH $1.50"],   # 2 lines; line 2 in gold
    "paras": [0, 1, 3, 7],                              # paragraphs to include, or "all"
    "end_card": ["Full story on YouTube", "THE YARD", "Which HBCU founder is next?"],
    "display": [["nineteen-oh-four", "1904"], ["H. B. C. U.", "HBCU."]],   # caption text swaps
    "cover": "cover_short.png"                          # optional 1 s cover frame appended (TikTok cover)
  }
Captions are timed from timing.json token_times (word-accurate).
"""
import importlib.util, json, math, os, re, subprocess, sys

EP = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2])
os.environ['THEYARD_EP'] = EP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('ep_scenes', os.path.join(EP, 'scenes.py'))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import cairo  # noqa: E402
from bo import draw_bo  # noqa: E402
from lib import text, back_out, prog, clamp, BG, MAROON, MAROON_DK, GOLDC, INK  # noqa: E402

CFG = json.load(open(os.path.join(EP, 'short.json')))
P, PARAS, TIM = mod.P, mod.PARAS, mod.TIM
USED = list(range(len(P))) if CFG.get('paras', 'all') == 'all' else CFG['paras']
SEGS = []
for k, i in enumerate(USED):
    a = 0.0 if i == 0 else P[i][0] - 0.1
    b = P[i][1] + (0.45 if k == len(USED) - 1 else 0.35)
    if SEGS and abs(SEGS[-1][1] - a) < 0.8:   # consecutive paragraphs: keep one continuous segment
        SEGS[-1] = (SEGS[-1][0], b)
    else:
        SEGS.append((a, b))
END_CARD = 2.5
VW, VH, FPS = 1080, 1920, 30
DISPLAY = [tuple(x) for x in CFG.get('display', [])] + [("H. B. C. U.", "HBCU.")]


def captions():
    out = []
    for i in USED:
        toks = PARAS[i].split(); tt = TIM['token_times'][i]
        sents, cur = [], []
        for k, t in enumerate(toks):
            cur.append(k)
            nxt = toks[k + 1] if k + 1 < len(toks) else ""
            letter = re.fullmatch(r"[A-Z]\.", t) is not None
            if t[-1] in ".?!" and not (letter and re.fullmatch(r"[A-Z]\.", nxt or "x")) and not (t == "D." and nxt):
                sents.append(cur); cur = []
        if cur:
            sents.append(cur)

        def split(g):
            s = " ".join(toks[j] for j in g)
            if len(s) <= 34 or len(g) < 4:
                return [g]
            best, bs = 2, 1e9
            for c in range(2, len(g) - 1):
                l, r = " ".join(toks[j] for j in g[:c]), " ".join(toks[j] for j in g[c:])
                sc = abs(len(l) - len(r)) - (12 if l.endswith(",") else 0)
                if sc < bs:
                    best, bs = c, sc
            return split(g[:best]) + split(g[best:])

        groups = [p for g in sents for p in split(g)]
        caps = []
        for g in groups:
            s = " ".join(toks[j] for j in g)
            for x, y in DISPLAY:
                s = s.replace(x, y)
            caps.append([tt[g[0]], s])
        for k, (st, s) in enumerate(caps):
            end = caps[k + 1][0] if k + 1 < len(caps) else P[i][1] + 0.3
            out.append((st, end, s))
    return out


CAPS = captions()


def wrap(cr, s, size, maxw):
    cr.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if cr.text_extents(t).x_advance > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    return lines


def caption(cr, t):
    for a, b, s in CAPS:
        if a <= t < b:
            p = prog(t, a, 0.18)
            for k, ln in enumerate(wrap(cr, s.upper(), 70, 960)):
                text(cr, ln, VW / 2, 1470 + k * 86, 70, (1, 1, 1), outline=INK, scale=0.9 + 0.1 * back_out(p),
                     alpha=clamp(p * 2))
            return


def scene_index(t):
    for i in range(len(mod.SCENES)):
        a, b = mod.scene_bounds(i)
        if a <= t < b:
            return i
    return len(mod.SCENES) - 1


SCALE, SY = 0.62, 560
SX = (VW - mod.W * SCALE) / 2
TOTAL = sum(b - a for a, b in SEGS) + END_CARD


def frame(vcr, hs, t_orig, t_short):
    vcr.set_source_rgb(*BG); vcr.paint()
    hcr = cairo.Context(hs)
    mod.SCENES[scene_index(t_orig)](hcr, t_orig); hs.flush()
    vcr.save(); vcr.translate(SX, SY); vcr.scale(SCALE, SCALE)
    vcr.set_source_surface(hs, 0, 0); vcr.get_source().set_filter(cairo.FILTER_GOOD)
    vcr.rectangle(0, 0, mod.W, mod.H); vcr.fill(); vcr.restore()
    vcr.rectangle(0, SY, VW, mod.H * SCALE); vcr.set_source_rgb(*INK); vcr.set_line_width(6); vcr.stroke()
    g = cairo.LinearGradient(0, 0, 0, SY)
    g.add_color_stop_rgb(0, *MAROON_DK); g.add_color_stop_rgb(1, *MAROON)
    vcr.rectangle(0, 0, VW, SY); vcr.set_source(g); vcr.fill()
    text(vcr, "THE YARD", VW / 2, 150, 40, GOLDC)
    h1, h2 = CFG['header']
    text(vcr, h1, VW / 2, 300, 82 if len(h1) <= 20 else 66, (1, 1, 1))
    text(vcr, h2, VW / 2, 410, 110 if len(h2) <= 12 else 84, GOLDC, scale=1 + 0.03 * math.sin(t_short * 3))
    y2 = SY + mod.H * SCALE
    g2 = cairo.LinearGradient(0, y2, 0, VH)
    g2.add_color_stop_rgb(0, *MAROON); g2.add_color_stop_rgb(1, *MAROON_DK)
    vcr.rectangle(0, y2, VW, VH - y2); vcr.set_source(g2); vcr.fill()
    caption(vcr, t_orig)
    vcr.rectangle(0, VH - 14, VW * t_short / TOTAL, 14); vcr.set_source_rgb(*GOLDC); vcr.fill()


def end_card(vcr, t):
    g = cairo.LinearGradient(0, 0, 0, VH)
    g.add_color_stop_rgb(0, *MAROON); g.add_color_stop_rgb(1, *MAROON_DK)
    vcr.set_source(g); vcr.paint()
    l1, l2, l3 = CFG.get('end_card', ["Follow for daily HBCU history", "THE YARD", "What should we cover next?"])
    draw_bo(vcr, VW / 2, 1500, 0.62, t=t + 5, pose="pockets", pose_to="wave", pose_t=clamp(t / 0.4), shadow=False)
    text(vcr, l1, VW / 2, 300, 70 if len(l1) <= 24 else 54, (1, 1, 1), alpha=clamp(t / 0.3))
    text(vcr, l2, VW / 2, 420, 100, GOLDC, scale=back_out(prog(t, 0.2, 0.5)))
    text(vcr, l3, VW / 2, 1680, 56 if len(l3) <= 28 else 46, (1, 1, 1), alpha=clamp((t - 0.5) / 0.3))


def render():
    build = os.path.join(EP, 'build'); os.makedirs(build, exist_ok=True)
    v = os.path.join(build, 'short_v.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{VW}x{VH}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                          '-pix_fmt', 'yuv420p', v + '.tmp.mp4'], stdin=subprocess.PIPE)
    vs = cairo.ImageSurface(cairo.FORMAT_ARGB32, VW, VH); hs = cairo.ImageSurface(cairo.FORMAT_ARGB32, mod.W, mod.H)
    ts = 0.0
    for a, b in SEGS:
        n = round((b - a) * FPS)
        for f in range(n):
            frame(cairo.Context(vs), hs, a + f / FPS, ts + f / FPS); vs.flush()
            p.stdin.write(bytes(vs.get_data()))
        ts += n / FPS
    for f in range(round(END_CARD * FPS)):
        end_card(cairo.Context(vs), f / FPS); vs.flush()
        p.stdin.write(bytes(vs.get_data()))
    cover = CFG.get('cover')
    if cover:  # 1 s cover frame at the end, so TikTok can use it as the cover
        cs = cairo.ImageSurface.create_from_png(os.path.join(EP, cover))
        for f in range(FPS):
            c = cairo.Context(vs); c.set_source_surface(cs, 0, 0); c.paint(); vs.flush()
            p.stdin.write(bytes(vs.get_data()))
    p.stdin.close(); assert p.wait() == 0
    os.replace(v + '.tmp.mp4', v)
    parts = ''.join(f'[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{k}];' for k, (a, b) in enumerate(SEGS))
    cat = ''.join(f'[a{k}]' for k in range(len(SEGS)))
    fc = parts + f'{cat}concat=n={len(SEGS)}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,apad[aout]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-i', os.path.join(EP, 'vo.mp3'), '-filter_complex', fc,
                    '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-shortest', '-movflags', '+faststart', OUT + '.tmp.mp4'], check=True)
    os.replace(OUT + '.tmp.mp4', OUT)
    dur = TOTAL + (1 if cover else 0)
    print(f'wrote {OUT} ({dur:.1f}s); cover frame at {int((TOTAL + 0.5) * 1000)} ms' if cover else f'wrote {OUT}')


if __name__ == '__main__':
    if '--stills' in sys.argv:
        from PIL import Image
        outp = sys.argv[sys.argv.index('--stills') + 1]
        vs = cairo.ImageSurface(cairo.FORMAT_ARGB32, VW, VH); hs = cairo.ImageSurface(cairo.FORMAT_ARGB32, mod.W, mod.H)
        picks, ts = [], 0.0
        for a, b in SEGS:
            picks += [(a + (b - a) * q, ts + (b - a) * q) for q in (0.3, 0.8)]
            ts += b - a
        ims = []
        for to, tsh in picks[:8]:
            frame(cairo.Context(vs), hs, to, tsh); vs.write_to_png('/tmp/_v.png')
            ims.append(Image.open('/tmp/_v.png').convert('RGB').resize((270, 480)))
        end_card(cairo.Context(vs), 1.5); vs.write_to_png('/tmp/_v.png')
        ims.append(Image.open('/tmp/_v.png').convert('RGB').resize((270, 480)))
        sh = Image.new('RGB', (270 * len(ims), 480), 'white')
        for k, im in enumerate(ims):
            sh.paste(im, (k * 270, 0))
        sh.save(outp)
        for c in CAPS:
            print(round(c[0], 2), round(c[1], 2), c[2])
    else:
        render()
