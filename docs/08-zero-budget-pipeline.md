# The $0 Production Pipeline

You have no budget. That rules out AI video generation entirely on the connected
accounts — but it does **not** rule out making this channel. Here is what is actually
free, what is not, and the pipeline that works with nothing.

## What I tested, and what it costs

Every AI service connected to this project was checked directly:

| Service | State | Verdict |
|---|---|---|
| **Artlist** — images | Free image generation **used** (produced the turnaround) | Spent |
| **Artlist** — video | 1 free generation still unspent, but **every** video model is subscription-gated | Unusable |
| **OpenArt** | 0 credits (40 spent on the hero + cast art) | Empty |
| **Higgsfield** | 0.5 credits, no free "unlim" allowance available | Empty |

On the video side specifically I probed every model group: Kling 1.6, Kling 2.5 Turbo,
Seedance 2.0 Mini, **Grok Imagine** (both groups), plus the Veo / Sora / Hailuo /
LTX / Wan tiers. All returned "needs an Artlist subscription." The only video models
flagged free-eligible were Heygen Avatar4 and Omnihuman — both human-avatar lip-sync
tools that cannot animate a vehicle.

**Conclusion: paid AI video is closed to you right now, and no amount of retrying
changes that.** So the pipeline below does not use it.

## The insight that makes this work

You do not need AI video. You need **art assets** plus **motion**, and those are two
separate problems.

You already have the art — the hero render, the turnaround, and the cast lineup. The
turnaround in particular is a gift, because it was rendered on a plain background,
which means the bus can be cut out into a transparent sprite and reused forever.

Motion is then just compositing, and compositing is free.

## The renderer

`tools/render_clip.py` turns the sprites into finished, seamlessly looping video. It
uses only Pillow and ffmpeg — both free, both already installed here.

```bash
# 10-second landscape clip for the main catalogue
python3 tools/render_clip.py --seconds 10 --out assets/video/benny-drive-16x9.mp4

# vertical cut for Shorts
python3 tools/render_clip.py --vertical --seconds 10 --out assets/video/benny-drive-9x16.mp4
```

What it produces: a parallax cartoon street (drifting clouds, scrolling buildings,
trees, and a dashed road), with Benny bouncing on his suspension and a contact shadow
that shrinks as he lifts. Every layer travels a whole number of tiles across the clip,
so **frame 1 and the last frame match exactly** — you can loop it end to end forever
with no visible seam.

That single property is what makes this economical: one 10-second loop covers 30
seconds of a verse, or three minutes if you cut it against the music.

The flat, uncluttered background is deliberate, not a limitation — it is exactly what
`docs/02-audience-and-format.md` calls for. Busy backgrounds compete with the character
for a toddler's attention.

## The rest of the stack, all free

| Job | Tool | Notes |
|---|---|---|
| Record vocals | **Audacity** | Free, cross-platform. A phone in a quiet room is fine to start. |
| Write the melody | **MuseScore** | Free notation, exports audio. Good for arranging public-domain tunes. |
| Backing track | **LMMS**, or **GarageBand** on Mac | Ukulele, glockenspiel, light percussion — keep it simple. |
| Edit the video | **DaVinci Resolve** (free tier) or **CapCut** | Resolve is professional-grade at $0. Its Fusion page can do keyframed animation too. |
| Touch up art | **GIMP** or **Krita** | Free. Use for thumbnails and sprite tweaks. |
| Vector / titles | **Inkscape** | Free. |
| Go deeper on 3D | **Blender** | Free, steep learning curve, but it is what the big channels effectively use. |

## Making a full song video at $0

1. **Record the audio first.** Vocals in Audacity over a simple backing track. The
   audio drives everything; never cut picture first.
2. **Render 4–6 loop clips** with `render_clip.py` — vary the seconds and the
   orientation to get variety.
3. **Cut the loops to the music in Resolve.** Change clip on the downbeat of each
   chorus. Hold each shot 3–5 seconds.
4. **Drop in still images** between loops — the hero render and the cast lineup work
   as held shots with a slow push-in (the "Ken Burns" move). A still with slow motion
   on it is completely standard in this genre.
5. **Add the end card** — wave goodbye, subscribe prompt, last 15 seconds.
6. **Export 1080p**, upload, mark Made for Kids, add chapters.

That is a complete song video with no money spent.

## Where free AI credits may come back

Not a plan, but worth checking every so often — some free tiers replenish:

- **OpenArt** free plan credits have historically refreshed periodically. Check the
  balance before assuming it is empty.
- New services routinely launch with free trials. The prompts in `prompts/` are
  portable — they are plain text and work on any image or video model.

Treat any of that as a bonus. The pipeline above does not depend on it.

## Priorities if you only do three things

1. **Record one song properly.** Audio quality is the thing viewers notice most and
   the thing that costs nothing but time.
2. **Render loops and cut them to that song.** You have unlimited clips available now.
3. **Make the thumbnail carefully.** Crop `hero-01.png` to 1280×720, face large, add a
   runtime badge. Packaging is most of the game and it is entirely free.
