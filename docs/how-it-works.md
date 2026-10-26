# How Motion Pilot works

## A steering document, then depth on demand

`SKILL.md` is short on purpose. It sets the stance (a motion director whose client has rejected generated-looking work), the house taste, the principles as numbers, the tells of generated motion, the process and the engine contract. Everything else is in `references/`, loaded only when the request needs it: a logo reveal reads the logo playbook and the construction craft; a preloader reads the web motion rules; a review reads the defect table.

## Decide twice, then build

Generated motion goes wrong in the same places: no story, adjectives instead of decisions, and nobody looking at the frames. Motion Pilot puts a decision before each:

1. **Storylines.** Three different films in words, each pairing a device (what the story is) with a form (how the camera carries it). The person picks.
2. **The SPEC.** The picked film as numbers: hex values and where the accent may appear, type sizes, easing curves by role, every shot with its hero move and hand-off, and a BANNED line of defaults this film must not fall into.
3. **The storyboard.** Stills from the real build, approved before any timing.

## Deterministic rendering

Every frame is a pure function of time: `M.render(t)` never depends on a previous call. That makes any frame renderable on its own, renders resumable after a stop, splices clean, and the same film reproducible next month. The renderer drives a headless Chromium frame by frame, blends sub-frames for motion blur, and encodes with ffmpeg. A time map fits a film to a voiceover without stretching the voice.

## One set of curves for film and web

The engine's named curves (`M.ease.arrive`, `exit`, `travel`, `sheet`, `reach` and more) are the same cubic-beziers a website uses in CSS, so a brand's film and its site move alike. A spring is named by its damping ratio, and zooms interpolate in log space so they do not appear to slow as they grow.

## Measured review

`review.py` measures what a contact sheet hides: whether the first frame is empty, every change event and the strips around it, holds and dead stretches, blends whose midpoint shows a colour neither shot owns, and loudness and true peak. The agent then judges the frames against a defect table, writes notes as `t=4.2s · where · problem → exact change · what stays`, ranks them P0 to P2, and fixes every P0 before delivery. It says plainly that sound was measured, not heard.

## Taste with a memory

`references/taste/lessons.md` records every correction that turned a draft into approved work: what happened, the wrong assumption, and the rule that prevents it. `references/taste/style-library.md` holds 33 studied references with measured pacing, palette and loudness. Add your own lessons and references; the skill gets better at your taste with use.
