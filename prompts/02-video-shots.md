# Video Prompt Library

**Status: not yet generated.** Every image-to-video model available on the connected
accounts was either subscription-gated or a human-avatar lip-sync tool that cannot
animate a vehicle. These prompts are written and ready — run them the moment you have
video credits.

## Universal negative prompt (use on every shot)

```
morphing, warping, distorted shapes, melting, extra wheels, extra eyes, extra
headlights, changing colors, flickering, jitter, text, letters, watermark, fast
motion, camera shake, zoom, scary, dark, gloomy, blurry, low quality
```

## Universal settings

- **Aspect ratio:** 16:9 for main content, 9:16 for Shorts
- **Duration:** 8–10s per shot. Shorter shots morph less.
- **Start frame:** always feed an approved still (e.g. `hero-01.png`). Text-to-video
  will not hold your character design.
- **Camera:** locked off, or a very slow push-in. Never a fast move.

---

## Shot A — Hero drive (the workhorse loop)

Start frame: `assets/generated/hero-01.png`

```
The cheerful green cartoon bus drives slowly and steadily toward the camera down the
sunny street, bouncing gently up and down on its springy suspension in a happy rhythm.
Its purple wheels spin smoothly and continuously. The bus blinks its big round eyes
once, slowly, and its smile widens warmly. Fluffy white clouds drift gently across the
bright blue sky behind it, and the green trees sway very slightly in a soft breeze.
The camera is locked off and completely steady. Smooth, gentle, slow, looping motion
suitable for a preschool cartoon for toddlers. The bus keeps exactly the same shape,
colors and face throughout.
```

## Shot B — Side-scroll travelling shot

Use for verses. Loops seamlessly and is the cheapest footage to reuse.

```
Side view of the cheerful green cartoon bus driving from left to right across the
frame at a steady gentle pace, wheels spinning smoothly, body bouncing lightly on its
suspension. The colourful cartoon buildings and green trees in the background scroll
smoothly past from right to left in a continuous parallax loop. The camera tracks
alongside the bus and keeps it centred in frame. Bright sunny day, smooth gentle
looping motion, consistent character design throughout.
```

## Shot C — Face close-up (for the 0:00–0:03 hook)

```
Extreme close-up on the cartoon bus's face, filling the frame. It blinks slowly twice,
then its smile widens into a big happy grin. Its eyes sparkle. The body bounces very
gently up and down. The camera holds completely still. Warm sunny light, bright
saturated colours, smooth gentle motion, consistent character design.
```

## Shot D — The wave goodbye (end card)

```
The cheerful green cartoon bus sits still in the centre of the sunny street, bouncing
gently, and blinks slowly at the camera with a warm closed-mouth smile. It tilts
slightly from side to side as if waving goodbye. Fluffy clouds drift slowly behind it.
Camera locked off and steady. Calm, slow, gentle motion for the end of a preschool
song.
```

## Shot E — Bus arrives at a stop

```
The cheerful green cartoon bus rolls slowly in from the right side of the frame and
comes to a gentle stop in the centre, rocking back slightly on its suspension as it
halts. Its doors fold open. It blinks and smiles at the camera. Bright sunny cartoon
street. Camera locked off. Smooth, slow, gentle motion, consistent character design.
```

## Shot F — Night / bedtime version

Start frame: a night-time still of the bus.

```
The green cartoon bus drives very slowly along a quiet night-time street, its warm
yellow headlights glowing softly. Its eyelids are half closed and sleepy. Stars twinkle
gently in the deep blue sky above and the streetlamps glow warm. Everything moves
slowly and calmly. Camera locked off and completely still. Very slow, soothing,
gentle motion for a bedtime lullaby video.
```

---

## Practical notes

- **Generate one shot, check it, then batch.** Character drift is the main failure
  mode; catch it on shot one.
- **Build a shot bank, not one-off clips.** Ten reusable 10-second loops will cover
  most of a 3-minute song when cut to the music.
- **Cut on the beat.** Even simple loops feel produced when the cuts land on the
  downbeat of the chorus.
- **If a model keeps morphing the bus**, shorten the duration and simplify the
  prompt to a single action. Two instructions per shot is the safe maximum.
