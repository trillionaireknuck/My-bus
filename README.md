# My Bus — Toddler Content Kit

Production kit for a preschool bus-cartoon channel aimed at **ages 1–5**, built from
your existing bus character and benchmarked against the top-performing bus videos on
YouTube.

## What's here

| | |
|---|---|
| **`assets/reference/bus-original.png`** | Your original bus, unchanged |
| **`assets/generated/hero-01.png`** | ⭐ The redesigned hero. Thumbnail base + video first frame |
| **`assets/generated/turnaround-01.png`** | 4-view turnaround. Feed this to any generator for consistency |
| **`assets/generated/bus-family-01.png`** | 4-bus cast lineup for "Different Types of Buses" |
| **`docs/`** | The strategy: audience, formats, packaging, songs, publishing |
| **`prompts/`** | Copy-paste prompt library for images and video |

## Start here

1. **`docs/01-character-bible.md`** — what changed about the bus and why, plus the
   exact hex palette sampled from the hero render.
2. **`docs/02-audience-and-format.md`** — how this niche actually works. Read this one
   even if you skip the rest.
3. **`docs/03-episode-formats.md`** — the four formats to make.
4. **`docs/04-thumbnails-and-titles.md`** — packaging, which is most of the game.
5. **`docs/05-song-library.md`** — public-domain melodies plus original lyrics written
   for Benny.
6. **`docs/06-publishing-checklist.md`** — Made-for-Kids rules and what they cost you.

## The three things that matter most

1. **Saturation and eye size.** Your bus was pastel with small eyes. Both were working
   against you — pastel disappears in a thumbnail grid, and small eyes do not read at
   120px. That is the change in `hero-01.png`.
2. **Length is the product.** The videos you benchmarked are 40 and 65 minutes. Make
   2–4 minute songs, then compile them. Every song should end up in five or more
   compilations.
3. **Show the face in the first 3 seconds.** No logo sting at the start. This is the
   most common fatal mistake on new channels in this niche.

## Status

- ✅ Hero redesign, turnaround sheet, and cast lineup generated
- ⛔ **Video not generated** — every image-to-video model on the connected accounts was
  either subscription-gated or a human-avatar lip-sync tool that cannot animate a
  vehicle. Prompts are written and ready in `prompts/02-video-shots.md`.
- Generation budget is currently exhausted (OpenArt 0 credits; Artlist free image used;
  Artlist free video unusable on available models).

## A note on the benchmark

The reference videos have 2.5M and 6.1M views and come from funded operations with
years of catalogue and distribution inside the YouTube Kids app. A new channel does not
match that with one upload. What compounds here is catalogue depth, consistent
packaging, and reusable assets — which is what this kit is built to give you.

---

## Zero-budget update

Paid AI video turned out to be closed on all connected accounts (every model group
probed, including Grok, returned a subscription wall). So the video in
`assets/video/` was **rendered locally at $0** — no AI service involved.

- `tools/render_clip.py` composites the cut-out bus sprite over a parallax cartoon
  street using Pillow + ffmpeg, and produces seamlessly looping clips.
- `assets/sprites/` holds transparent PNG cut-outs of all four bus views, extracted
  from the turnaround sheet. These are reusable forever.
- See **`docs/08-zero-budget-pipeline.md`** for the full free stack and workflow.

```bash
python3 tools/render_clip.py --seconds 10 --out assets/video/benny-drive-16x9.mp4
python3 tools/render_clip.py --vertical --seconds 10 --out assets/video/benny-drive-9x16.mp4
```

---

## Episode 1

**"The Wheels on Benny's Bus"** — 3:43, traditional melody (public domain).

- **Script + timing map:** `docs/episodes/ep01-wheels-on-bennys-bus.md`
- **Picture lock:** `assets/video/ep01-picture-lock.mp4` — silent, cut to length
- **Shot bank:** `assets/video/shots/` — seamless loops in day, rain, night, sunset,
  park, plus two face closeups

The picture is finished. The vocal is the only piece left, and it's the one piece
that needs a human.

```bash
# re-render any shot at any length or orientation
python3 tools/render_clip.py --scene night --seconds 12 --out shot.mp4
python3 tools/render_clip.py --scene day --framing closeup --seconds 8 --out hook.mp4

# rebuild the episode after changing shots or timing
python3 tools/assemble_episode.py --out assets/video/ep01-picture-lock.mp4
```

Scenes: `day`, `rain`, `night`, `sunset`, `park`. Framings: `wide`, `closeup`.
Add `--vertical` for a 1080x1920 Shorts cut.
