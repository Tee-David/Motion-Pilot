# Transitions with a cause

A transition is a sentence that joins two ideas. When something on screen causes it, the film reads as one continuous thought. When nothing does, it reads as the next slide. Use three to five kinds in a film, chosen for what each joins. At most a third of the seams between beats are hard cuts, and two worlds never crossfade into each other.

## Rules

- **Cause.** Every transition starts from something already on screen: a click, a cursor, an object, the edge of a sheet, the mark itself.
- **Cut on the fastest frame.** A cut hidden inside fast motion, with matching direction and speed on both sides, disappears. Mirror the curves across the seam (the outgoing move eases in, the incoming one eases out).
- **No saturated crossfades.** An opacity blend of two strong grounds passes through a colour neither owns (navy into royal blue makes lavender). Cut, wipe with a shaped mask, or carry one object across. When a blend is unavoidable, check its midpoint frame (`scripts/review.py` flags off-palette blends).
- **Never reveal the edge of the world.** A whip or slide that shows a gap at the frame's edge reads as "next page". Overscan the moving layer or move the camera, not the world.
- **Leave by moving, not by fading.** An object that passes the camera leaves by sliding past the lens, not by turning translucent over the next shot.
- **Exits answer entrances.** A sheet that came down from the top goes back up the same way; a curtain that closed from the middle opens from the middle.
- **Vary them.** The same spin, zoom, light leak or whoosh on every cut is a template, however expensive it looks.

## The catalogue

| Transition | How it is built | Good for |
| --- | --- | --- |
| **Iris from the cause** | `clip-path: circle()` opens from the clicked point, the nib or the dot onto the next world, 150 to 450 ms on exponential in-out, with a thin ring of the accent at its edge | A click that opens something; the end of a construction |
| **Object becomes the world** | A pill, card or tile grows past the frame (650 ms, both ways), its radius shrinking; what was around it blurs about 15 px and fades; the new content fades in while it still grows | Entering the product; a chip that becomes a page |
| **Morph** | One container widens into the next (an icon card into a prompt box, 110 to 880 px in about 200 ms) with a horizontal blur 12 → 0 | UI states; one thing turning into the next |
| **Carry across** | The result shrinks 1 → 0.6 with blur peaking mid-move and lands inside the next scene as it builds around it | Output travelling into the next tool |
| **Colour flood** | The hero object stays while the whole ground changes colour in about 400 ms both ways | A chapter change; brand colour arriving |
| **The sheet** | A full-screen sheet of the ground rises or drops over the frame (480 to 520 ms on `.77,0,.18,1`), its leading edge bowed by an ellipse of the same colour that flattens as it lands; after the hold the trailing edge bows as it lifts away (640 to 680 ms) | Page transitions; a calm studio cut |
| **Halves part** | Two halves of the ground close from top and bottom (460 ms) and part again (600 ms), no seam colour | A blueprint or technical brand |
| **Cursor wipe** | The text cursor grows to full height (both ways), widens to full width (exponential in), then exits, uncovering the next scene | A typed hook handing over to the story |
| **Giant type wipe** | A word set at two or three times the frame's width slides through and uncovers the next scene | Word-beat films, launches |
| **Gather and implode** | A cloud of items (vendors, coins, chips) orbits with rising jitter, then collapses to a point with exponential in, scale to 0.1 and blur; the point becomes the next object | "Many things become one"; a hero object arrives |
| **Match cut** | One shape holds while everything around it changes: a ring becomes a lens becomes the logo; a dot becomes a planet becomes a button | Bookends; rhymes between worlds |
| **Whip** | A smear of 130 to 300 ms along the move's axis; the arriving element lands blurred and sharpens in about 130 ms | Energy, montage |
| **Blur swap on one stage** | Out: fade with about 8 px of blur in 130 to 200 ms. In: blur to 0 in about 130 ms. The ground never cuts | Rotating words or stats on one stage |
| **Dip cut** | The outgoing frame darkens about 40% for three frames before a hard cut, so the cut reads as meant | Hard cuts in a calm film |
| **Zoom through** | The camera tracks to a button (600 ms with blur), then the button scales from about 8% to 250% of the frame in 350 ms, strong ease-in; its fill becomes the next frame | One per film at most |

## Hard cuts

Hard cuts belong inside a scene (a punch-in on a detail, a reframe) and on the beat in a montage. Between worlds, a hard cut needs a reason: a sound hit on the cut, matched motion across it, or a dip. Never hard-cut between two saturated grounds without one.

## Durations, at a glance

Full-screen sheets and floods 400 to 700 ms. Irises 150 to 450 ms. Morphs and carries 200 to 650 ms. Whips 130 to 300 ms. A transition shorter than about 120 ms reads as a glitch unless it is on a hard beat.
