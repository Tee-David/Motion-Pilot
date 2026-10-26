# Logo construction

A logo that builds itself from its own parts is the most ownable moment a brand can have in motion: no other brand can play it. A logo that spins, bounces or fades in is the opposite. This file is how to take a mark apart and choreograph it back together, for logo reveals, end cards, preloaders and page curtains.

## 1. Take the mark apart

Work from the SVG. List every part with its role: arcs, counters, a hand, a nib, panes of a window, a tile behind the mark, each letter of the wordmark. Note the mark's centre of rotation (usually the centre of its main circle or bowl, not its bounding box), its aspect ratio, and the lockup's exact proportions in the brand's header: mark height, gap, wordmark size and its line breaks. The construction must land on that lockup to the pixel, because the viewer is about to see it in the corner of every page.

Size everything from one number. Derive the mark's width, the wordmark's size, the gap and the reserved wordmark width from the mark's height, so the lockup is identical at every screen size and nothing clips (setting the width and height by hand is how the left of a mark gets sliced off by an `overflow: hidden` box).

## 2. Choose a construction grammar

Pick the grammar from what the brand is and what its mark is made of.

| Grammar | What happens | Suits | Seen in |
| --- | --- | --- | --- |
| **Draw** | A pen writes the mark's strokes: trim paths at a both-ways ease, the hand of the logo drawing the part it holds | Studios, makers, writing, design | Ink |
| **Construct** | Guides set out from the centre, construction circles draw from twelve o'clock, pen-tool anchors pop where guides cross, parts swing into place round the centre with a faint trail, guides leave the frame outward | Engineering, architecture, finance, precision | Blueprint, Kantiv |
| **Gather** | Loose strokes, dots or particles orbit, spiral inward and lock into the parts | Organic, friendly, playful | Ink's fingertips, Famolus |
| **Assemble** | Pieces (quarters, panes, tiles) fly in and snap together with a small overshoot | Systems, platforms, modular products | A property platform's quarters |
| **Morph** | One simple shape becomes the mark through a chain of shapes (a sun rising becomes a seed becomes the mark) | Calm, natural, lifestyle | Sun Garden |
| **From the content** | The brand's own content becomes the mark: listings become the panes of a window, posts become the tiles | Products with a strong content unit | A property platform's listings |
| **Write-on** | The wordmark writes itself as a single hand-drawn line | Craft, food, personal brands | Sun Garden's wordmark |

Two grammars can combine (gather into the parts, then draw the rest), but one leads.

## 3. Choreograph the order

A dependable shape for a 3 to 5 s construction:

| Phase | Time | What happens |
| --- | --- | --- |
| First gesture | 0 to 0.4 s | One small thing establishes the world: a cursor blinks, an axis draws, a dot appears. Never an empty frame for long. |
| Parts arrive | 0.2 to 1.5 s | The grammar plays. Overlapping staggers; one secondary action (a trail, guides). |
| The mark completes | 1.4 to 1.8 s | The one accent event: the cursor squashes into a nib, a ring goes out once from that point. |
| Settle | 1.7 to 2.3 s | Guides leave outward; the mark settles to its lockup size, perhaps turning once (`rotateY` 360° with perspective) as it shrinks. |
| The name | 1.9 to 3.0 s | The name arrives beside the mark: typed, or rising from its baseline, or sliding out from behind the tile. Wait until the mark has stopped moving, or the moving mark sweeps across the first letters. |
| Hold | about 1.2 to 1.5 s | Dead still. |
| Exit | 0.25 s, then 0.6 to 0.7 s | The lockup leaves first and fast; then the ground leaves (a sheet lifts, halves part, an iris opens). |

**Mark first, then the name.** The cleanest lockups finish the icon and its tile, then slide the name out from behind the tile as the mark glides aside. The other dependable version is a collision: the mark's box opens from zero width and that opening is what pushes the wordmark into place, so the two halves meet as one lockup rather than animating in separately.

**The accent is one event.** In most marks the accent colour is one part (a nib, a dot, a cursor). Let it be the cursor at the start and the part at the end, and let it do nothing else. No accent cursor riding along the typed name; no accent seam where the ground parts.

## 4. Craft details that decide whether it reads

- **Rotate round the mark's centre.** Set `transform-box: view-box` and the origin to the mark's real centre in viewBox units for parts that swing round it; `transform-box: fill-box` for parts that pop in place.
- **A dot is a zero-length dash.** A stroke with round caps whose dash shrinks to nothing as it lands becomes a dot; that dot can become a fingertip, a rivet or a pixel.
- **Trails sit just behind the part.** A faint dash on the part's centre line, kept a fixed angle behind its trailing end through the whole swing, fading as the part lands.
- **Gravity, then a squash.** A thing that falls onto the centre accelerates (`.55,0,1,.45`), squashes about 1.6 × 0.45 on contact, and becomes the next thing.
- **Shapes scale with the frame.** A bowed edge or a ring sized in viewport units becomes a blob on a phone; cap it against the shorter side (`min(20vh, 32vw)`).
- **Guides are hairlines.** One device pixel, a few shades off the ground, `vector-effect: non-scaling-stroke` for straight guides (but not for dashed rings, which some engines then draw solid).
- **Clip padding.** A line that rises out of a clip needs padding for ascenders and the descenders of g and y, given back with negative margin.
- **Both grounds.** On paper the mark is the brand's ink and shadows are real; on the dark ground the mark is white and nothing glows.

## 5. Between pages

The same construction, short (about 1 s to built), carries page transitions: the ground closes (a sheet rises or drops, halves close), the mark builds at speed while the next page loads, the page's name appears under it in a small label, and the ground leaves. If the page is not ready when the build ends, the mark waits with a small idle that reads as "working" (fingertips tapping in turn like a typing indicator), never a spinner. See `genres/web-motion.md` for the rules that keep this polite.

## 6. Worked examples

`reference-implementations/wdc-preloaders/` holds two approved constructions, Ink (draw and gather) and Blueprint (construct), with every timing and curve and the reasoning for each, plus the page-transition versions. Read them before building a new construction: they show how small the numbers are and how much overlap there is.
