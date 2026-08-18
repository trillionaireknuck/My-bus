# Jayden the Train — Assessment

Reviewed from the 15-second clip you shared (720×1280 vertical, 24fps, sunset
sunflower-field scene). A sample frame is saved at
`assets/reference/jayden-frame.png`.

## The honest read

Jayden is **better crafted than it is targeted.** The rendering is lovely — the
sage-and-dusty-rose palette is distinctive, the composition is considered, the light
is warm. It looks like a high-end storybook illustration or a greeting card.

That is precisely the problem. It is designed to the taste of an adult art director,
not to the perceptual system of a two-year-old. It has the same two issues your bus
had, plus three of its own.

## What to fix, in priority order

### 1. The eyes are far too small (biggest issue)

Jayden's eyes are small dots on the front of the boiler. At the size a phone thumbnail
renders, they effectively disappear. Eye contact is the strongest attention hook for
under-3s, and it is the thing the competitor videos lean on hardest.

**Fix:** the same treatment the bus got — eyes 3–4× larger, big white sclera, large
dark pupils, two sparkle catchlights each, looking straight down the lens. Compare
`assets/reference/bus-original.png` against `assets/generated/hero-01.png` to see the
exact change.

### 2. The palette is too desaturated

Sage green, dusty pink, mauve. Sophisticated and muted. A developing visual system
resolves saturated colour far more easily, and muted tones vanish in a thumbnail grid
next to saturated competitors.

**Fix:** keep the colour *relationships* — the green/pink/purple identity is genuinely
distinctive and worth protecting — but push saturation hard, exactly as the bus was
pushed.

### 3. The background is doing too much

This is the issue unique to Jayden and it is severe. Thousands of individually rendered
poppies and sunflowers, detailed rolling hills, a textured gradient sky. For a
1–3 year old this is visual noise, and Jayden is competing with it for attention rather
than sitting in front of it.

Look at the competitor frames: simple flat buildings, plain blue sky, a handful of
clouds. That emptiness is deliberate — it makes the character the only thing to look at.

**Fix:** flatten and simplify the background dramatically. Fewer, larger, simpler
shapes. Let Jayden be the only detailed thing in frame.

### 4. Sunset lighting reads as "bedtime"

The dusk palette is low-contrast and signals wind-down. That is a great fit for a
bedtime/lullaby video and a poor one for daytime engagement content.

**Fix:** make the default Jayden scene bright midday with a vivid blue sky. Keep the
sunset version — it is genuinely good — but file it as your bedtime variant.

### 5. It is vertical

720×1280 is Shorts format. Per `docs/02-audience-and-format.md`, Shorts are a
discovery tool on kids content; they monetise poorly and build little watch time. The
main product needs to be **16:9 long-form**.

**Fix:** produce Jayden in 16:9 for the catalogue, and cut vertical Shorts from it.

## Minor notes

- Jayden appears to grow a small arm/hand around the 4–6 second mark. Decide
  deliberately whether he has arms; inconsistency between shots reads as sloppy.
  For vehicles in this genre the usual answer is no arms — they bounce and they move.
- The clip is nearly static, with a slow camera track. That is fine for B-roll but
  Jayden needs a signature *motion* — a bounce, a chuff, a whistle — the way the bus
  bounces on its suspension.

## The bigger question: two characters or one?

You now have a bus and a train. A word of caution: a new channel grows fastest with
**one** recognisable face. Two half-built characters compete with each other for the
catalogue depth that actually drives growth.

The most efficient path is to pick one as the hero and let the other be recurring
supporting cast — Jayden as the train Benny waves to at the level crossing, say. That
gives you crossover content and variety without splitting your identity.

Both characters share the same green-plus-warm-accent palette family, so they already
look like they belong to the same world. That is an asset. Use it.

## Ready-to-run fix prompt

Attach a Jayden frame as the reference image:

```
Restyle this cute cartoon train character for a preschool nursery-rhyme cartoon aimed
at toddlers.

KEEP THE SAME CHARACTER IDENTITY: same rounded toy-train body shape, same friendly
face placement, and the same colour identity — sage-green locomotive with pink and
purple carriages, gold funnel trim, pink cowcatcher.

CHANGE THESE THINGS:
1. COLOR: push saturation much higher. Vivid spring-green locomotive, bright candy-pink
   and violet carriages, warm gold trim. Candy-bright, high-contrast, glossy colours —
   NOT dusty, NOT muted, NOT pastel.
2. FACE: make the eyes dramatically bigger — two huge round eyes on the front of the
   locomotive with large white sclera, big dark glossy pupils and bright sparkle
   catchlights, looking directly at the camera. Add rosy blush cheeks and a wide open
   happy smile.
3. BACKGROUND: replace the detailed flower field with a very simple, clean cartoon
   landscape — a few large simple rolling green hills, three or four big simple
   flowers, a vivid blue sky with large fluffy white clouds. Keep it uncluttered and
   flat so the train clearly pops in front of it.
4. LIGHTING: bright midday sunshine, not sunset.
5. SHOT: three-quarter front view, low camera angle looking slightly up at the train.
6. STYLE: glossy smooth 3D animation render, soft rounded plastic toy surfaces, thick
   clean shapes, high contrast, cheerful preschool cartoon look.

No text, no letters, no logos, no watermark. 16:9.
```
