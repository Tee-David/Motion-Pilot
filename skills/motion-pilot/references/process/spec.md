# The SPEC: the film as numbers

Adjectives are where the default look lives. Given "premium, modern, clean", every gap fills with the most common answer: a dark void, a glow, small type in the middle, everything fading in. Each adjective turned into a number is a decision taken back.

Before any scene, write `SPEC.md` at the project root: the picked storyline as a director's brief to yourself, with a number wherever you would have written an adjective. Build from it, review against it, and change it when a review changes the film. The spec serves the story, never the other way round: a look that turns the story's things into abstract shapes has failed, however striking the frame.

## Template

```text
GOAL:    what the viewer feels or does at the end, one sentence
OUTPUT:  W x H at fps, every format and theme that ships, length as a range
TIME:    seconds x fps = frames; BPM and frames per beat if there is music; the voice file if there is one
LOOK:    ground (hex, texture and its amount), ink, one accent and exactly where it may appear;
         display face, weight, size in px and tracking; body face the same;
         the medium (paper and ink, product UI, photographs, glass, construction lines) with its numbers;
         light and depth: shadow offset, blur and opacity, grain %, vignette %
OBJECTS: every thing the viewer must recognise (a phone, a receipt, a pen nib), drawn with the material and
         details that make it read without a label
MOTION:  curves by role (arrive, exit, camera, draw, land) as named beziers; springs by damping;
         durations and staggers in ms or frames; the motion identity from the brand profile
SHOTS:   one line per shot: frame range, the one hero move, what is read and for how long,
         the sound, and how it hands off to the next shot
BANNED:  the calibration list in SKILL.md, plus anything this film must not become
QA:      the frames to check and what each must show
```

## Turning words into numbers

| The word | Becomes |
| --- | --- |
| premium | A material with numbers: satin paper with 2% grain; a product on a seamless sweep with a 0.5 contact shadow; arrivals of 500 to 700 ms with no overshoot |
| modern | A camera and a type system: one 30-frame push on one curve; a display face at 8 to 9% of frame height with -2% tracking |
| clean | A grid and a ration: 12 columns, 6% margins, the accent on one word per shot |
| confident | Holds: titles land and stay still; one hero move per shot; exits at half the entrance |
| dynamic | Cuts on the beat; a layout change every bar; one hero move per shot, never three |
| playful | Springs at damping 0.45 to 0.6 on position and scale, never on opacity or colour; poses exaggerated 10 to 30% |
| cinematic | A lens and a light: a 35 mm framing, a key from upper left, a rim from behind, 6% vignette, long dissolves inside one world |
| friendly | Rounded geometry, 150 to 300 ms pops, a cursor or hand that does the work |
| calm | 2 to 4 s beats, sine ease-in-out on anything ambient, no cut under 1.5 s |

## Composition numbers

- The hero of a shot fills at least 40% of the frame's width or height. A small object in the middle of an empty frame is not a shot: push in, crop, or give it a world.
- One hero move per shot. Secondary moves travel 50 to 70% as far, start 100 to 200 ms after it, and everything else holds.
- Every shot moves the story: something happens that causes the next shot. Lines read as cause and effect, not slogans.
- An information beat (a data card, a definition) has its information on screen within about 2.5 s, then holds, so any paused frame reads as a finished poster.
- Something new every 2 to 4 s; a new layout every bar when there is music.
- Text meant to be read: at least 2.6% of the short side (28 px at 1080), held 0.5 s plus 0.3 s a word. Too many words: cut words, never shrink type.

## A look built from a medium

A look holds together when it is the rules of one medium rather than a palette. Name its parts, what each may carry, and how the medium itself moves. Two worked examples:

**Ink on paper.** Paper: one warm off-white (`#f9f7f4`), no gradient. Ink A: the brand navy for every structural line and every word. Ink B: one orange for the cursor and the nib, one focus per frame. Motion: things are drawn, typed and lifted. A sheet lifts off on a bowed edge with a soft shadow; strokes are written by a pen at a both-ways ease.

**Blueprint.** Ground: the brand navy. Guides: hairlines a few shades lighter than the ground. Construction: circles drawn from twelve o'clock, axes from the centre outward, pen-tool anchors that pop where guides cross. The mark: white. Accent: one orange for the cursor and the nib. Motion: things are constructed. Guides set out, parts swing into place round a centre with a faint trail, guides leave the frame outward when the mark is complete.

Write any look this way: paper and ink, risograph, cut paper, glass, clay, product UI, photographs.

## Motion identity

A brand that moves consistently has three constants. Record them in its profile (`brands/`) and put them in every SPEC:

1. **A signature curve** used for most arrivals (for example `cubic-bezier(.16,1,.3,1)`).
2. **A duration palette** of three values (quick, standard, slow; for example 200, 460 and 680 ms).
3. **A signature entrance or gesture** the brand owns (a cursor that becomes a nib; a window whose panes are listings; a sheet that lifts on a curved edge).

## The BANNED line

Start from the calibration list in `SKILL.md`. After the first render, name every default the frames fell into, from that list or not, add each to this film's BANNED line, and fix them before anything else. The list grows with every film. A brand's own material can lift a ban (a brand whose ground really is navy may use navy) but only in the way the brand uses it.
