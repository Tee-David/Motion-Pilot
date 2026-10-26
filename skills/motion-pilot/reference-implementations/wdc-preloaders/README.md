# Studio preloaders: Ink and Blueprint (shipped)

Two logo constructions that play once per visit over a studio website and, short, as the curtain between its pages. Both were approved after several rounds of correction; the lessons are in `references/taste/lessons.md`. Recordings are R30 to R33 in the style library.

- `preloader.css`: the whole choreography, a beat at a time, as CSS animations with delays. Each concept opens with a beat sheet in milliseconds. Read this first.
- `preloader.tsx`: the component. It only switches phases (`enter`, `wait`, `leave`) and repeats the few timings it needs (`TIMES`). It imports the site's logo paths and settings, so it will not run outside that site; read it for the pattern.

## Ink (draw and gather), first load

| ms | Beat |
| --- | --- |
| 0 | The orange cursor fades in where the nib will be and blinks once |
| 220 | Four ink strokes orbit in, one every 45 ms, spiralling from twice the mark's size to the radius of the fingertip each becomes, shortening into dots (680 ms, `.45,0,.2,1`) |
| 850 | The dots pop into fingertips (380 ms, `.2,.7,.3,1`, overshoot to 1.12) |
| 900 | The palm and thumb reach in from the wrist (420 ms, `.34,1.45,.64,1`) |
| 1000 | The hand draws the C: top arc clockwise, bottom arc anticlockwise 60 ms behind (500 ms, `.65,0,.35,1`) |
| 1480 | The cursor squashes (1.5 × 0.55) and the nib pops out of it (340 ms); one orange ring goes out (460 ms) |
| 1760 | The mark slides aside to make room for the name (520 ms, `.16,1,.3,1`) |
| 1880 | The name is typed, 34 ms a letter, with no cursor riding it |
| 2760 | Leave: the lockup rises away (240 ms, `.4,0,1,1`), then the paper sheet lifts on a bowed trailing edge (680 ms, `.77,0,.18,1`) |

Grounds: paper `#f9f7f4` with navy ink in light mode; night `#08081f` with white ink in dark mode. Orange only for the cursor, the nib and the ring.

## Blueprint (construct), first load

| ms | Beat |
| --- | --- |
| 0 | The axes draw out from the mark's centre across the screen (520 ms, `.16,1,.3,1`) |
| 140 | Outer and inner construction circles draw from twelve o'clock (620 and 580 ms, both ways) |
| 360 | Pen-tool anchors pop where the guides cross, the centre first, 35 ms apart (`.34,1.6,.64,1`) |
| 420 | The top arc swings 150° round the centre with a faint trail; the bottom arc follows from the other side 100 ms later (520 ms, `.34,1.4,.64,1`) |
| 760 | The hand slides in along the horizontal axis (440 ms, `.34,1.5,.64,1`) |
| 900 | The fingertips drop in like rivets, 40 ms apart (300 ms) |
| 1080 | The cursor falls down the vertical axis onto the centre anchor (gravity, `.55,0,1,.45`), squashes and becomes the nib with the ring |
| 1440 | The guides leave the frame outward (the dash slides on past the end) |
| 1720 | The mark turns once (rotateY 360°) as it settles from 1.32× into the lockup (520 ms, both ways) |
| 2180 | The name rises out of its baseline in the mute colour, 24 ms a letter; each letter turns white 180 ms after it rises |
| 3000 | Leave: the lockup fades and scales to 0.96 (220 ms), then the navy sheet parts down the middle, top half up, bottom half down (600 ms) |

## Between pages

Ink: the sheet rises over the page with a bowed leading edge (480 ms; on phones it drops from the top instead and lifts back up the same way), the fingertips tap in (260 ms), the hand reaches (300), the C draws (360 and 400), the nib lands (600) and the page's name types under the mark at 20 ms a letter. If the page is not ready at 860 ms, the fingertips keep tapping in turn like a typing indicator.

Blueprint: the halves close (460 ms), guides set out (420), arcs swing (460 and 500), hand (540), rivets (640), nib (720), the page's name rises under the mark in small tracked capitals (600). Built at 960 ms; while waiting, the fingertips drum.

## Rules it keeps

Once per visit (a 30-minute window), decided before first paint by an inline script; `pointer-events: none` and no scroll lock on first load; nothing under reduced motion; not on dashboards, sign-in or document pages, nor for a link to the current page; it never holds the next page back. Transform and opacity only, plus `stroke-dashoffset` and `stroke-dasharray` on a few paths in one small SVG. Every size derives from one custom property.
