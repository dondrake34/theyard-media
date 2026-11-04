# The Yard — daily production playbook

Every scheduled run follows this file from top to bottom. It produces and schedules that day's content with
no human in the loop, so quality and accuracy checks are part of the job, not optional.

## Standing setup and authorizations (from the owner, Don, on 2026-10-29)
- Channel: **The Yard**, animated HBCU history and culture. TikTok, Instagram and X: @theyardanimated.
  **YouTube was dropped on 2026-11-02** (owner replaced it with X after every YouTube upload failed). Don't post to YouTube.
- Fully automatic posting is approved. No per-post approval needed.
- Don accepted TikTok's Direct Post terms for all The Yard uploads. Use `acceptTerms: true` (TikTok) on every post.
- Every post carries the AI label where the platform offers one: TikTok `aiGenerated: true`, Instagram `isAiGenerated: true`.
  X has no AI-label setting in the connector. Visibility public.
- Host character: **Bo** (`pipeline/bo.py`, reference `pipeline/bo_reference.png`).
- Voice: ElevenLabs **Terrance – Cinematic Authentic Narrator**, voice_id `IS2y6AW9sjF8fFltBSqN`, model `eleven_v4`.
- Posting: FavStash connector. Always call `list_connected_social_accounts` first. IDs change when an account is reconnected.
- Media hosting: this repo (public). Raw URL pattern:
  `https://raw.githubusercontent.com/dondrake34/theyard-media/main/media/<episode>/<file>`

## Schedule (America/Chicago)
| Day | What this run makes | Posts |
|---|---|---|
| Every day (Sun–Sat) | One standalone Short (62–80 s) | Same day 6:00 PM on **TikTok, Instagram Reel and X, every day** |

**Cadence (owner, 2026-11-04): every platform posts every day.** The day's Short goes to TikTok, Instagram and X at
6:00 PM. If a platform already has a post in that day's slot (e.g. a manual backfill), skip that platform that day.
(Replaces the 2026-11-02 every-other-day X rule.) That's about 30 X posts a month (1 X unit each).

The Saturday long video was discontinued on 2026-11-02 with YouTube (owner's choice). Saturdays make a normal Short;
prefer a topic with a story arc. The long-video steps below (render_long.py, YouTube titles/chapters) are kept for reference only.

- Convert to UTC with `zoneinfo` (daylight saving changes). Never hard-code the offset.
- Before making anything, call `list_social_posts` and check that slot isn't already filled. Never double-post.
- Run order matters: make sure the 6 PM post is scheduled well before 6 PM. If the run starts after 5:30 PM,
  schedule for the next free 6 PM slot instead and say so in the summary.

## Limits: pause and pick up after the reset (owner's instruction, 2026-10-29)
When a tool limit is reached, don't ration or give up. Finish what can be finished, park the rest,
and pick it up automatically on the first run after the limit resets.

- **FavStash posts** (`maxPostsPerMonth`, check `get_account_plan_and_usage` before scheduling; each platform post
  counts as 1). Platform daily caps (e.g. Instagram's `quota` in `get_social_publishing_options`) work the same way.
  X also has its own monthly allowance (`maxXPostUnitsPerMonth`; a video post costs 1 unit, a post containing a URL costs 10,
  so never put links in X captions). Schedule the Short in this order until a limit is reached: **TikTok, Instagram, X**. Anything that didn't fit goes into the **Pending posts** table in `episodes.md`
  (episode, platform, media URLs, caption/title/tags ready to paste into `create_social_post`).
- **ElevenLabs credits** (or any generation limit): if voice or transcription fails for quota, stop production for the day.
  Leave the topic unchecked in `topics.md`, note the pause in `episodes.md`, and continue on the next run.
- **Start of every run:** check `get_account_plan_and_usage` and the Pending posts table. If there's room again
  (e.g. a new month), schedule pending posts first, oldest first, each into the next free 6:00 PM slot for that platform
  Never put two Shorts in the same slot on one platform. Remove each from
  the table once it's `QUEUE`. Then do today's normal job.
- Mention any paused or pending items in the summary message, with the date the limit resets
  (`analyticsResetAt` / start of next month for FavStash).

## Steps

### 0. Set up the workspace
```bash
git clone https://github.com/dondrake34/theyard-media && cd theyard-media
pip install --break-system-packages -q pycairo pillow
fc-list | grep -qi poppins || echo "Poppins font missing: install fonts-poppins or use Inter"
```
Read `episodes.md` (what's been made), `topics.md` (backlog), `insights.md` (what's working).
Look at `episodes/ep01-bethune-cookman/scenes.py`. It's the worked example for scene code.

### 0b. Track metrics and monetization (every run, before production)
Owner asked to be alerted the moment any account becomes eligible to monetize.
1. `get_social_account_analytics` for each account (TikTok gives `followers`; X followers if offered; Instagram followers
   if offered) and `analyze_social_content_performance` per account (`days: 30`, `limit: 25`, sort by views) to get each
   video's **lifetime** views.
2. Write `/tmp/snapshot.json` in the format documented in `pipeline/metrics.py` (one entry per video: platform, id,
   published date, lifetime views, `duration_s` for TikTok; accounts `x: {followers}`), keeping videos from older snapshots that dropped out of the 30-day list
   (carry their last known numbers forward).
3. `python3 pipeline/metrics.py /tmp/snapshot.json` → updates `metrics/snapshots.jsonl` and `metrics/MONETIZATION.md`.
4. Any `ALERT:` line = a threshold newly met. Put it at the **top** of the summary message in bold, with what it unlocks
   and how to apply (TikTok → Creator tools → Creator Rewards; Instagram → Professional dashboard → Monetization;
   X → Settings → Monetization). X Creator Revenue Sharing needs Premium + 500 *verified* followers + 5M organic impressions
   in 3 months (help.x.com, checked 2026-11-02); the connector can't see impressions or verified followers, so it never auto-alerts. Before alerting, confirm the current requirement on the platform's official help page.
5. If an analytics call fails, note it in the summary: the owner may need to
   reconnect that account in FavStash. Use what's available; never guess numbers.
6. On Sundays, include a one-line progress line per program from `MONETIZATION.md` in the summary.

### 1. Pick the topic
- Take the next unused topic in `topics.md`, unless `insights.md` says a category is outperforming. Then pick from that category.
- Vary categories day to day. Never repeat a covered topic (check `episodes.md`).
- Saturdays: pick a topic with a real story arc (founder story, turning point, legacy).
- Episode folder: `episodes/epNN-short-slug/` (next number in `episodes.md`).

### 2. Research and fact-check (non-negotiable)
- Every factual claim (dates, numbers, names, "firsts") needs **two independent reputable sources**:
  the university's own history page, state archives, Smithsonian/NMAAHC, Library of Congress, NPS, major news outlets.
- If sources disagree, use the cautious wording or leave the claim out. Never invent quotes, numbers or scenes.
- Use present-tense search for anything current (enrollment, rankings, current presidents).
- Stay neutral on politics. Present history factually, no editorializing about current figures or parties.
- Write sources into `meta.md` in the episode folder.

### 3. Write the script → `narration.txt`
- **Short:** 165–200 words, 5–7 paragraphs (narration ≥ 62 s; TikTok only pays on videos longer than 1 minute). **Long:** 420–520 words, 8–10 paragraphs.
- Blank line between paragraphs. **Each paragraph becomes one scene.**
- The first sentence is the hook: a surprising fact, a stake or a question. No "In this video".
- End with a question CTA that invites comments (e.g. "Which HBCU should we cover next?").
- **Always write HBCU as `H. B. C. U.`** in the narration (it must be spoken as four letters: AITCH-BEE-SEE-YOU).
- Write numbers and dates as they're spoken ("nineteen twenty-three", "a dollar fifty").
- Voice: storyteller for history, warm second-person "you" for culture topics. Short sentences.

### 4. Voiceover
- `creative_create_flow` first, then `creative_generate_speech` on that flow with voice `IS2y6AW9sjF8fFltBSqN`,
  model `eleven_v4`, `generations_count: 1` (credits cost money; never retry a generation call blindly).
- Poll `creative_get_flow_run_status` until complete, then `curl -sS -o vo.mp3 "<content_url>"` into the episode folder.

### 5. Word timing and pronunciation check
- `creative_transcribe_audio` (model `eleven_scribe_v1`) on the same flow with `connect_from` = the speech node.
  Poll, then `curl -sS -o words.json "<words_download_url>"`.
- `python3 pipeline/wordsync.py EP words.json EP/vo.mp3` → writes `words.tsv`, `timing.json`.
- **Pronunciation check:** in `words.tsv`, every HBCU must appear as separate `H.` `B.` `C.` `U.` words.
  Also check the match ratio is ≥ 85%. If either fails, regenerate the voice once (adjust the text) and repeat.

### 6. Scenes → `scenes.py`
Write one scene function per paragraph with `from lib import *`, ending with `SCENES = [s0, s1, ...]`.
Use `beat(i, "exact phrase from paragraph i")` for timing, `scene_bounds(i)`, `fade_edges` at the end of each scene.
Helpers in `pipeline/lib.py`: `text`, `pop_text`, `panel`, `kicker`, `bg`, `ground`, `house`, `building`,
`capitol`, `statue`, `crate`, `coin`, `pie`, `envelope`, `kid`, `mary` (stylized woman: poses rest/welcome/hold/think/knock),
`subscribe_btn`, and Bo via `bo(cr, x, y, scale, t, pose=..., talk=True)`.
Add new props to the episode's `scenes.py` (or to `lib.py` if they're reusable).

**Visual rules (the owner set these):**
- **Whoever the narrator is talking about is on screen.** When the script mentions a person, show that person.
  Never show Bo in a person's place.
- Bo is the host only: hook reactions, "here's the part nobody tells you" moments, the outro/CTA.
- **Bo never has a mouth.** No red or pink lips on any dark-skinned character (it reads as blackface caricature).
  Express emotion with eyes, brows, poses and shock lines.
- Real people are drawn as simple stylized figures (like `mary()`), not realistic portraits. No photos.
- No brand logos, no copyrighted characters, no university logos or seals. School names in text are fine;
  school colors are fine.
- Text on screen is short (keywords, numbers, dates) and never covers the subject.
- Check: render stills at the busiest moments of each scene, look at them, fix overlaps and empty frames.
  ```python
  # quick stills: import scenes with THEYARD_EP set, draw SCENES[i](cr, t) to a cairo surface, save PNG
  ```

### 7. Render
- Short: `short.json` (header 2 lines: line 1 ≤ 20 chars white, line 2 ≤ 12 chars gold; `"paras": "all"`;
  end card; caption `display` swaps like `["nineteen twenty-three","1923"]`; `"cover": "cover_short.png"`).
  For a standalone Short, the 16:9 scenes are the same as long-form. `make_short.py` puts them in the vertical frame.
- `python3 pipeline/thumbs.py EP` (needs `thumbs.json`) **before** `make_short.py` (the cover frame comes from it).
- `python3 pipeline/make_short.py EP EP/short.mp4`; `--stills EP/short_sheet.png` to preview and print captions.
- Long (Saturday): `python3 pipeline/render_long.py EP EP/long.mp4`, then a Short cut with chosen paragraphs.
- Encoding is already set (H.264 veryfast CRF 20, AAC 192k, -14 LUFS).

### 8. Thumbnails (research-backed, see thumbs.py docstring)
- `thumbs.py` is still required: it makes `cover_short.png/jpg` (Instagram cover, TikTok cover frame). The 3 16:9 variants
  were for YouTube and are no longer posted; keep `thumbs.json` variants short anyway. The cover must tease, not repeat, the caption.
- One hero object (coin by default; define `thumb_hero` in `scenes.py` for a custom object).
- Look at `thumb_sheet.png`, including the 168×94 phone-size preview. Text must read at that size.

### 9. QA before anything is uploaded
- Sample frames from the final MP4s (ffmpeg `-ss`) and look at them: sync, overlaps, empty scenes, typos.
- Captions match the audio. HBCU shows as "HBCU" in captions.
- Durations: Short 62–90 s (must be over 60 s for TikTok Creator Rewards; X accepts up to 2:20 without Premium).
- If anything is wrong, fix and re-render. If it can't be fixed, **don't post**; explain in the summary.

### 10. Upload media
Copy `short.mp4` and `cover_short.jpg` into `media/epNN-slug/`,
then commit and push (see Logging), then `import_post_media` on each raw URL to get FavStash CDN URLs.

### 11. Captions, titles, hashtags and tags (research-backed playbook)
Research summary (Oct 2026): hashtags are classification signals now, not reach multipliers. Captions and on-screen
words drive search. Instagram caps posts at **5 hashtags** (more gets reduced reach). TikTok works best with **3–5**
accurate tags. YouTube tags play a minor role but still help as context. Use 7–15, specific to broad.
#fyp/#viral do nothing.

- **First line of every caption = searchable keywords**: "HBCU history: <person/school> <what happened>".
- **TikTok (3–5):** `#HBCU` + `#HBCUHistory` (or `#HBCULife` for culture) + 1 school/person tag
  (e.g. `#BethuneCookman`, `#FAMU`, `#HowardUniversity`) + `#BlackHistory` + 1 format tag (`#HistoryTok` or `#LearnOnTikTok`).
- **Instagram (exactly 5 max):** `#HBCU` `#HBCUHistory` (or `#HBCUPride`/`#HBCULife`) + school/person tag + `#BlackHistory` + 1 topic tag.
- **X:** caption **≤ 280 characters including hashtags** (FavStash enforces it; an emoji counts as 2). Keyword first line,
  then the CTA question, then 2–3 hashtags: `#HBCU #BlackHistory` + school/person tag. No links (10× cost). Add `altText`
  describing the video on the media item.
- *(Retired with YouTube, kept for reference)* **YouTube Short:** title ≤ 70 chars with the main keyword first, ending in `#Shorts`; description: 1–2 keyword
  sentences + 3 hashtags (`#HBCU #BlackHistory #Shorts`); tags 8–12.
- **YouTube long:** title ≤ 60 chars, curiosity + keyword ("She Built a College With $1.50 and 5 Girls"); description
  first line keyword-rich, then story summary, chapters (start 0:00, each ≥ 10 s, from `timing.json` paragraph
  starts), CTA question, sources, then 3 hashtags (shown above the title): `#HBCU #BlackHistory #<Person/School>`;
  tags 10–15 (≤ 500 chars total): topic → school → person → category (`HBCU history`, `Black history`,
  `historically black colleges`, `animated history`, `The Yard`) → 1–2 common misspellings.
- Culture topics may add `#HBCULife`, `#HBCUPride`, `#HBCUHomecoming`, Greek-letter tags (`#Divine9`) when relevant.
- Never use unrelated trending tags.

### 12. Schedule (FavStash `create_social_post`)
One call per publish time. Use a new `clientRequestId` such as `theyard-epNN-short-YYYYMMDD`.
- TikTok target: `settings: {postingMethod: "DIRECT_POST", privacy: "PUBLIC_TO_EVERYONE", allowComments: true,
  allowDuets: true, allowStitches: true, aiGenerated: true, commercialContent: false, acceptTerms: true}`,
  media `{url, kind: "video", durationSeconds, thumbnailTimestampMs: <cover frame ms printed by make_short>}`.
- Instagram target: `settings: {contentType: "reel", shareToFeed: true, isAiGenerated: true}`, media with `thumbnailUrl` = cover.
- X target: no `settings` needed; media `{url, kind: "video", durationSeconds, altText}`. If X fails with
  `HTTP 402 credits depleted`, the X API pay-per-use balance behind the connection is empty: don't retry, leave X for that
  day, and tell the owner to top up / contact FavStash.
- *(Retired)* YouTube target: `settings: {title, visibility: "public", madeForKids: false, uploadCertified: true,
  containsSyntheticMedia: true, notifySubscribers: true, tags: [...]}` (no `contentType` key; YouTube detects Shorts),
  media with `thumbnailUrl` (main thumbnail for long, cover for Short).
- Verify with `get_social_post` that each post is `QUEUE` with the right time.

### 13. Logging (keeps the next run informed)
- `episodes.md`: add a row (number, date, topic, type, titles, post IDs, sources count).
- `topics.md`: mark the topic used (`[x]`), add new ideas found during research.
- Delete `build/` and large intermediates (keep `narration.txt`, `scenes.py`, configs, `timing.json`, `words.tsv`,
  `meta.md`, `vo.mp3`). Commit and push:
  `git add -A && git commit -m "epNN: <topic>" && git push`.
  End commit messages with the attribution lines from the session's system reminder.

### 14. Sunday extra: weekly review
On Sunday's run, also call `analyze_social_content_performance` across all three accounts (TikTok, Instagram, X) for the last 7–30 days.
Write what worked (topics, hooks, lengths, platforms) into `insights.md` with numbers, and adjust the next week's
topic order in `topics.md`. Comments can't be replied to through the connector, so note frequent comment
requests/questions as topic ideas.

### 15. Summary message
End with a short summary: what was made, the topic, where and when it posts, post IDs, sources,
any skipped platform or problem. Send it with `SendUserMessage` (the owner reads it on his phone).
