"""Render an episode's 16:9 video and mux the voiceover.

Usage: python3 render_long.py EP_DIR OUT.mp4 [scene indices...]
EP_DIR needs narration.txt, words.tsv, timing.json, scenes.py (SCENES list) and vo.mp3.
Renders one file per scene to EP_DIR/build/, joins them with -c copy, then adds loudness-normalised audio.
"""
import importlib.util, os, subprocess, sys
from multiprocessing import Pool

EP = os.path.abspath(sys.argv[1]); OUT = os.path.abspath(sys.argv[2])
os.environ['THEYARD_EP'] = EP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('ep_scenes', os.path.join(EP, 'scenes.py'))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import cairo  # noqa: E402

FPS = 30
BUILD = os.path.join(EP, 'build')


def render_scene(i):
    a, b = mod.scene_bounds(i)
    n = round((b - a) * FPS)
    tmp = os.path.join(BUILD, f'scene{i:02d}.tmp.mp4'); fin = os.path.join(BUILD, f'scene{i:02d}.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s',
                          f'{mod.W}x{mod.H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                          '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, mod.W, mod.H)
    for f in range(n):
        cr = cairo.Context(s); mod.SCENES[i](cr, a + f / FPS); s.flush()
        p.stdin.write(bytes(s.get_data()))
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, fin)
    return i, n


if __name__ == '__main__':
    os.makedirs(BUILD, exist_ok=True)
    idx = [int(x) for x in sys.argv[3:]] or list(range(len(mod.SCENES)))
    with Pool(min(len(idx), os.cpu_count() or 1)) as pool:
        for r in pool.imap_unordered(render_scene, idx):
            print('scene done', r, flush=True)
    lst = os.path.join(BUILD, 'list.txt')
    with open(lst, 'w') as f:
        for i in range(len(mod.SCENES)):
            f.write(f"file 'scene{i:02d}.mp4'\n")
    vid = os.path.join(BUILD, 'video.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
    tmp = OUT + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vid, '-i', os.path.join(EP, 'vo.mp3'), '-map', '0:v',
                    '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11,apad', '-c:a', 'aac',
                    '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, OUT)
    print('wrote', OUT)
