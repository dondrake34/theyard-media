"""Align the narration script to ElevenLabs word timestamps.

Usage: python3 wordsync.py EP_DIR WORDS_JSON AUDIO
  WORDS_JSON: the transcript's words (list of {text, start, end, type}) or a words.tsv.
Writes EP_DIR/words.tsv and EP_DIR/timing.json with:
  duration, paras [[start, end], ...], token_times [[t_start per script token], ...] per paragraph.
Script tokens are whitespace-split words of each paragraph, so lib.beat(i, phrase) maps exactly.
"""
import difflib, json, os, re, subprocess, sys

ep, wj, audio = sys.argv[1:4]
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

if wj.endswith('.tsv'):
    W = [(float(a), float(b), t) for a, b, t in (l.rstrip('\n').split('\t') for l in open(wj) if l.strip())]
else:
    raw = json.load(open(wj))
    raw = raw.get('words', raw) if isinstance(raw, dict) else raw
    W = [(float(w['start']), float(w['end']), w['text']) for w in raw if w.get('type', 'word') == 'word']
with open(os.path.join(ep, 'words.tsv'), 'w') as f:
    for a, b, t in W:
        f.write(f"{a}\t{b}\t{t}\n")

paras = [p.strip() for p in open(os.path.join(ep, 'narration.txt')).read().split('\n\n') if p.strip()]
script = [(pi, tok) for pi, p in enumerate(paras) for tok in p.split()]
A = [norm(t) for _, t in script]
B = [norm(w[2]) for w in W]
sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
amap = {}
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        amap[blk.a + k] = blk.b + k
matched = len(amap) / max(1, len(A))
# time for every script token; unmatched tokens are interpolated between matched neighbours
times = [None] * len(A)
ends = [None] * len(A)
for ai, bi in amap.items():
    times[ai] = W[bi][0]; ends[ai] = W[bi][1]
known = [i for i, x in enumerate(times) if x is not None]
for i in range(len(A)):
    if times[i] is None:
        lo = max([k for k in known if k < i], default=None)
        hi = min([k for k in known if k > i], default=None)
        if lo is None:
            times[i] = ends[i] = W[0][0]
        elif hi is None:
            times[i] = ends[i] = ends[lo]
        else:
            f = (i - lo) / (hi - lo)
            times[i] = ends[i] = ends[lo] + (times[hi] - ends[lo]) * f
token_times, bounds = [], []
for pi in range(len(paras)):
    idx = [k for k, (p, _) in enumerate(script) if p == pi]
    token_times.append([round(times[k], 3) for k in idx])
    bounds.append([round(times[idx[0]], 3), round(ends[idx[-1]], 3)])
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', audio]))
json.dump({"duration": dur, "paras": bounds, "token_times": token_times, "match_ratio": round(matched, 3)},
          open(os.path.join(ep, 'timing.json'), 'w'), indent=1)
print(f"matched {matched:.1%} of script words; duration {dur:.2f}s")
for i, b in enumerate(bounds):
    print(i, b)
if matched < 0.85:
    print("WARNING: transcript differs a lot from the script; check the audio before publishing")
