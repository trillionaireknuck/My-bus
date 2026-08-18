# Character Bible — "Ella the Bus" (working name)

> **Why "Ella" works.** Two syllables with the stress on the first (EL-la) — a trochee,
> which is the dominant stress pattern in English child-directed speech and among the
> easiest shapes for a toddler to reproduce. It is also a real, widely familiar name
> rather than an invented one, which helps parents remember it.
>
> It also reads as feminine, and that is a genuine differentiator: almost every
> vehicle character in this niche is male-coded. A girl bus stands out in a search
> results page full of boy trucks and trains.
>
> **Before you commit, search YouTube for the name** — you do not want to launch into
> an existing channel's brand. Pick something you can also get as a channel handle.
>
> Ella's pronouns are your call — the songs and scripts are written so they never
> need one ("The wheels on Ella go round and round"), so you can decide later without
> rewriting anything.

## The design change, and why

Your original bus was a soft pastel toy. The version in `assets/generated/hero-01.png`
keeps that character but changes two things that matter for this audience:

| | Original | Now | Why |
|---|---|---|---|
| **Saturation** | Soft pastel | Vivid, high contrast | A developing visual system resolves bold saturated colour far more easily. Pastel also disappears in a thumbnail grid next to saturated competitors. |
| **Eyes** | Small, dark, no sclera | Large, white sclera, dark pupils, sparkle catchlights, direct gaze | Eye contact is the single strongest attention hook for under-3s. Small eyes do not read at thumbnail size. |
| **Mouth** | Tiny closed smile | Wide open smile | Reads as friendly from across a room and at 120px wide. |

Everything else — the chunky rounded body, the roof shape, the colour relationships —
is unchanged. It is still recognisably your bus.

## Palette

Sampled directly from the approved hero render, so these are the real values:

| Part | Hex | Notes |
|---|---|---|
| Body green (base) | `#43C455` | The signature colour. Never desaturate it. |
| Body green (lit) | `#7AF68A` | Sunlit front surfaces |
| Roof yellow | `#FFF091` | Warm cream-yellow, not lemon |
| Trim / bumpers coral | `#FF854F` | Window frames, bumpers, hubcaps |
| Wheels purple | `#5A2A8F` | Deep violet — the accent that makes it distinctive |
| Sky blue | `#00C5FC` | Standard background sky |

The green + coral + purple combination is genuinely distinctive in this niche — most
competitors are red, yellow, or blue. **Keep it.** It is the cheapest brand asset you
have.

## Proportions and construction

- Chunky, rounded, toy-like. No sharp edges anywhere. Everything reads as moulded plastic.
- Body roughly 2 to 2.5 times as long as it is tall. Do not stretch it into a realistic coach.
- Roof is a soft rounded cap that overhangs slightly at the front.
- Four visible wheels, purple with coral hubcaps.
- Two round headlights, white/cream, sitting low on the front like cheeks.

## Face rules (the important part)

The face lives on the **front** of the bus:

- **Eyes fill the windshield.** Two large circles, big white sclera, large dark pupils.
- **Always two catchlight sparkles** in each eye — one large, one small. This is what
  makes the eyes look alive rather than dead.
- **Direct gaze at the camera** in every hero shot and every thumbnail.
- **Rosy blush cheeks** on the body either side, soft and semi-transparent.
- **Mouth below the windshield**, on the grille area — a wide open curved smile.
- Headlights sit low, below and outside the mouth.

### Expressions to keep in the kit
Happy (default), Surprised (eyes wide, mouth small O), Sleepy (eyelids half down),
Excited (eyes squinted into upward arcs, big open smile). Four expressions cover
almost every song.

## Direction of travel

Ella drives **screen-left to screen-right**, in the **near lane** — below the dashed
centre line, on the side of the road closest to camera.

That combination is not arbitrary. On a right-hand-drive road the near lane carries
traffic moving left to right, so this is the only pairing that reads as legal driving
to an American viewer. Two things have to agree for it to work:

1. **The front of the bus leads.** The turnaround sprite faces screen-left, so the
   renderer mirrors it. If you ever swap the sprite, check the front still points
   the way the world is scrolling.
2. **The background scrolls right to left.** That is what sells motion to the right.

Get one of these backwards and the bus looks like it is driving in reverse, or in the
oncoming lane. Both read as "wrong" even to viewers who could not say why.

## Hard rules — do not break these

1. **Never** put the face anywhere but the front.
2. **Never** desaturate back to pastel. This was the whole point of the redesign.
3. **Never** give the bus arms or legs. It is a bus. It bounces and it drives.
4. **Never** add teeth. A tongue and lower lip is fine; teeth read as aggressive.
5. **Never** copy another channel's character. A cute stylised bus is a genre; the
   specific red double-decker and the buses in that YouTube screenshot are somebody's
   IP. Stay in your own palette and your own silhouette and you are fine.

## The cast

`assets/generated/bus-family-01.png` establishes three companions in the same style —
a yellow school bus, a red double-decker, and a small blue minibus. That directly
unlocks the "Different Types of Buses" format, which is one of the highest-performing
formats in this niche.

Keep Ella as the hero — same size advantage, always front and centre. Companions are
supporting cast, not co-leads. A channel with one recognisable face beats a channel
with four interchangeable ones.

> Note: the lineup render drifted back toward the softer pastel palette and smaller
> eyes. Treat it as a composition and cast reference, not as the final colour target.
> When you regenerate it with credits, push it back to the hero palette above.
