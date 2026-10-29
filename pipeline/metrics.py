"""Track progress toward monetization and decide when to alert the owner.

Usage: python3 metrics.py SNAPSHOT.json
SNAPSHOT.json (written by the run from FavStash analytics, numbers are LIFETIME values as of today):
{
  "date": "2026-10-30",
  "accounts": {
    "youtube":   {"subscribers": 12},
    "tiktok":    {"followers": 40},
    "instagram": {"followers": null}
  },
  "videos": [
    {"platform": "youtube", "id": "abc", "kind": "short" | "long", "published": "2026-10-29",
     "views": 1234, "watch_hours": 3.2},          # watch_hours only for long videos (watch_time / 60 if minutes)
    {"platform": "tiktok", "id": "...", "published": "...", "views": 900, "duration_s": 71},
    {"platform": "instagram", "id": "...", "published": "...", "views": 50}
  ]
}
Appends to metrics/snapshots.jsonl, rebuilds metrics/MONETIZATION.md, and prints ALERT lines for thresholds
newly met (already-sent alerts are stored in metrics/alerts.json so each fires once).
Rolling windows use differences between today's lifetime numbers and the snapshot from N days ago
(or the earliest snapshot if history is shorter, which slightly overstates the window and is labelled).
"""
import datetime as dt, json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'metrics')
os.makedirs(ROOT, exist_ok=True)
SNAPS = os.path.join(ROOT, 'snapshots.jsonl'); ALERTS = os.path.join(ROOT, 'alerts.json')
TH = json.load(open(os.path.join(ROOT, 'thresholds.json')))

snap = json.load(open(sys.argv[1]))
today = dt.date.fromisoformat(snap['date'])
hist = [json.loads(l) for l in open(SNAPS)] if os.path.exists(SNAPS) else []
hist = [h for h in hist if h['date'] != snap['date']] + [snap]
hist.sort(key=lambda h: h['date'])
with open(SNAPS, 'w') as f:
    for h in hist:
        f.write(json.dumps(h) + '\n')


def lifetime(h, platform, field, kind=None, min_dur=None):
    tot = 0.0
    for v in h['videos']:
        if v['platform'] != platform or (kind and v.get('kind') != kind):
            continue
        if min_dur and v.get('duration_s', 0) <= min_dur:
            continue
        tot += v.get(field) or 0
    return tot


def window(platform, field, days, kind=None, min_dur=None):
    """Growth of a lifetime total over the last `days` days. Returns (value, exact?)."""
    cutoff = (today - dt.timedelta(days=days)).isoformat()
    older = [h for h in hist if h['date'] <= cutoff]
    now = lifetime(snap, platform, field, kind, min_dur)
    if older:
        return now - lifetime(older[-1], platform, field, kind, min_dur), True
    return now, False   # history shorter than the window: everything so far counts


def acct(platform, key):
    return (snap['accounts'].get(platform) or {}).get(key)


rows, met = [], []


def check(key, label, items):
    """items: list of (name, value, target, exact). Threshold met when all items reach target."""
    ok = all(v is not None and v >= t for _, v, t, _ in items)
    rows.append((label, items, ok))
    if ok:
        met.append((key, label))


yt_active = 'ypp_2027' if today >= dt.date(2027, 2, 1) else 'ypp_2026'
y = TH[yt_active]; f = TH['ypp_fan_funding']
subs = acct('youtube', 'subscribers')
wh, wh_ex = window('youtube', 'watch_hours', 365, kind='long')
sv, sv_ex = window('youtube', 'views', 90, kind='short')
rows.append((f"YouTube fan funding (memberships, Super Chat, Shopping) — {f['subscribers']} subs + "
             f"{f['watch_hours']:,} watch hrs/365d OR {f['shorts_views']:,} Shorts views/90d",
             [('subscribers', subs, f['subscribers'], True), ('watch hours (365d)', wh, f['watch_hours'], wh_ex),
              ('Shorts views (90d)', sv, f['shorts_views'], sv_ex)], None))
fan_ok = subs is not None and subs >= f['subscribers'] and (wh >= f['watch_hours'] or sv >= f['shorts_views'])
if fan_ok:
    met.append(('yt_fan', 'YouTube fan funding'))
rows.append((f"YouTube ad revenue (YPP, {y['label']}) — {y['subscribers']:,} subs + {y['watch_hours']:,} watch hrs/365d OR {y['shorts_views']:,} Shorts views/90d",
             [('subscribers', subs, y['subscribers'], True), ('watch hours (365d)', wh, y['watch_hours'], wh_ex),
              ('Shorts views (90d)', sv, y['shorts_views'], sv_ex)], None))
if subs is not None and subs >= y['subscribers'] and (wh >= y['watch_hours'] or sv >= y['shorts_views']):
    met.append(('yt_ypp_' + yt_active, 'YouTube ad revenue (YPP)'))

t = TH['tiktok_creator_rewards']; tf = acct('tiktok', 'followers')
tv, tv_ex = window('tiktok', 'views', 30, min_dur=60)
check('tt_rewards', f"TikTok Creator Rewards — {t['followers']:,} followers + {t['views_30d']:,} views/30d (videos > 1 min)",
      [('followers', tf, t['followers'], True), ('views on >1-min videos (30d)', tv, t['views_30d'], tv_ex)])
tl = TH['tiktok_live_gifts']
check('tt_live', f"TikTok LIVE gifts — {tl['followers']:,} followers", [('followers', tf, tl['followers'], True)])
ig = acct('instagram', 'followers')
for k, label in (('instagram_gifts', 'Instagram Gifts'), ('instagram_subscriptions', 'Instagram Subscriptions')):
    check(k, f"{label} — {TH[k]['followers']:,} followers", [('followers', ig, TH[k]['followers'], True)])

sent = json.load(open(ALERTS)) if os.path.exists(ALERTS) else {}
new = [(k, l) for k, l in met if k not in sent]
for k, l in new:
    sent[k] = snap['date']
json.dump(sent, open(ALERTS, 'w'), indent=1)


def fmt(v):
    return 'unknown' if v is None else (f'{v:,.1f}' if isinstance(v, float) and v % 1 else f'{int(v):,}')


lines = [f"# Monetization progress\n\nUpdated {snap['date']} by the daily run. Source: FavStash analytics snapshots "
         f"(`metrics/snapshots.jsonl`). Rolling windows marked * have less history than the window so far.\n"]
for label, items, _ in rows:
    lines.append(f"## {label}\n")
    lines.append("| Requirement | Now | Target | Progress |\n|---|---|---|---|")
    for name, v, tgt, exact in items:
        pct = 'unknown' if v is None else f"{min(100, 100 * v / tgt):.1f}%"
        lines.append(f"| {name}{'' if exact else ' *'} | {fmt(v)} | {tgt:,} | {pct} |")
    lines.append("")
lines.append("## Alerts sent\n")
lines += [f"- {k}: {d}" for k, d in sent.items()] or ["- none yet"]
lines.append("\nThresholds: `metrics/thresholds.json` (check the platforms' official pages if they change). "
             "Note: from Feb 1, 2027 YouTube's ad-revenue bar doubles to 8,000 watch hours or 20M Shorts views.")
open(os.path.join(ROOT, 'MONETIZATION.md'), 'w').write("\n".join(lines) + "\n")
for k, l in new:
    print(f"ALERT: eligible for {l}")
print("progress written to metrics/MONETIZATION.md")
