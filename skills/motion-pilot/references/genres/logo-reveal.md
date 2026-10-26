# Logo reveals, stings and end cards

A logo reveal is three to eight seconds in which the brand shows what it is made of. The construction is the story (`craft/logo-construction.md`); this file is the shape of the piece around it.

## Lengths and uses

| Use | Length | Sound |
| --- | --- | --- |
| Sting before or after a film | 3 to 5 s | A riser into one impact, or a short signature motif |
| Social bumper | 4 to 6 s | A bed with one hit |
| End card | The last 5 to 10% of a film | The film's final hit, then the call to action holds 1.5 to 3 s |
| Preloader | 2.5 to 5 s, once per visit | Silent (`genres/web-motion.md`) |
| Page curtain | About 1 s to built | Silent |

## The shape

1. **A first gesture** on frame 0 or within 0.2 s: a cursor, an axis, a dot, a sun on the horizon. Never a black frame for long.
2. **The construction** in the brand's grammar, with one secondary action.
3. **The accent event** once, when the mark completes.
4. **The lockup**: mark first, then the name beside it, sliding out from behind the tile, typed, or rising from its baseline.
5. **The hold**, dead still, 1.2 to 1.5 s (longer as an end card with a call to action).
6. **The exit**, or a cut to black for a sting.

## Variations to offer

Always build the mark-first version: icon and tile finished, then the name slides out from behind the tile as the mark glides aside. Offer a second order (the name typed beside a finished mark, or the collision where the mark's box opening pushes the name into place) and let the client pick. Build both themes.

## Reference grammar in the library

- **R27 Sun Garden** (morph and write-on, 8.6 s): a sun rises over a soft horizon on one sage ground, shrinks into a seed, the flower mark settles above it, and the wordmark writes itself as one hand-drawn line. One continuous take, no cuts, a calm 2 s rise before anything else happens.
- **R28 Kantiv** (construct and assemble, 5.6 s): a shape swoops in on a curved trail, construction lines and a circle draw through it, the quarters snap, the mark flips once, settles left, and the name rises letter by letter with a mute-then-white treatment.
- **R29 Famolus** (gather, 2.5 s): loose strokes and dots orbit and lock into the letterforms of a wordmark. Fast and organic, finished in under 2 s.
- **R30 to R33** (draw and construct): the shipped studio preloaders, with their page-curtain versions (`reference-implementations/wdc-preloaders/`).

## Checks specific to reveals

- The final lockup matches the brand's real lockup to the pixel (overlay a frame on the SVG).
- No part of the mark clips at any size; the mark never sweeps across the name while the name arrives.
- The accent appears once.
- The hold is long enough to read the name: about 1.2 s at least.
- On a phone the construction's shapes stay small enough to read as parts, not blobs.
