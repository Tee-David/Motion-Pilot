# Review: see it as the viewer will, then fix what is weak

You built the timeline, so you know what happens. The viewer sees it once, at full speed, often on a phone, often muted. Review is how you see it their way: as a harsh motion director, not a proud author. QC (`scripts/qc.py`) finds what is broken; review finds what is weak. Run it on every new piece and on any edit that changes timing or layout, before you reply or render the final.

Review mode also works on things you did not make: a client's existing film, a reference, a live preloader. The method is the same; the notes become recommendations.

## 1. Measure, then look

1. `python scripts/review.py out.mp4 --out review/` writes:
   - `sheet.jpg`: frames across the film with timestamps;
   - `phone.jpg`: the same frames at 360 px wide, to judge what can be read on a phone;
   - `cut-NN.jpg`: seven frames around every change event (−0.2 s to +0.2 s), to catch pops, flashes of the old scene and jumps;
   - `report.md` and `report.json`: first-frame check, change events per 10 s, holds and their lengths, dead stretches over 3 s, frames where a blend shows colours the film's palette does not own, and loudness when there is audio.
2. For a web piece, record it first: a Playwright video or a screen recording at 60 fps, then the same command.
3. Open every sheet. A clipped label or a 0.6 s line looks fine on a contact sheet; trust the numbers where they disagree with your eye.
4. You cannot hear. The audio figures are measured; tone, accent and feel need a human ear. Say so.

## 2. What to look for

First describe each beat frame in one sentence as a stranger would, naming every object. An object you would have to explain ("those bars are listings") is a P0. Read the frames in order: does each cause the next? Compare each with its shot in `SPEC.md`. Then name every tell from the calibration list in `SKILL.md` the frames show, add it to the BANNED line and fix it before anything else.

Then go through the sheets once per question:

| Question | What it catches |
| --- | --- |
| Does it read as what it is? | A shape that reads as another object, a product screen that reads as a mockup, a mark that reads as a blob |
| Does the subject separate? | Subject and ground too close in value, two focal points in one frame, the eye with nowhere to go |
| Framing and contact | Crops, text at the edge or under platform UI, collisions at a seam, things floating that should touch |
| Timing as a first-time viewer | A read shorter than its words, something that pops on with no move, a jump at a cut, everything moving at once on one curve |
| Accent and colour | More than one accent event per beat; a blend midpoint in a colour the brand does not own; glow standing in for light |
| Both grounds | The light version uses ink and shadow, not additive glow; every word passes 4.5:1 on its ground in both |
| The pictures alone | With the words covered, the beat frames still tell the story |
| The phone sheet | Every line meant to be read can be read at 360 px |
| Loops and seams | The last frame returns to the first on a hold; no jump in position or colour |

## 3. Defects that cap a piece

Each row gets PASS or FAIL with evidence: the file and the time (`cut-04 @ +0.10 s`, `phone 05 at 14.2 s`). A row without evidence counts as FAIL.

| # | Defect | Where |
| --- | --- | --- |
| D1 | Text overlapping text during a swap, a transition or a list build | cut strips, sheet |
| D2 | A line meant to be read cannot be read on a phone | phone sheet |
| D3 | Nothing striking and readable by 2 s (social and films) | sheet, first frames |
| D4 | A dead stretch: nothing new for more than 4 s that is not a deliberate hold | report, sheet |
| D5 | A blank frame that is not a beat, or a stutter at a cut | cut strips |
| D6 | Something pops in fully formed, or slides at constant speed where it should ease or spring | cut strips |
| D7 | A tell from the calibration list | sheet |
| D8 | Copy covered or cropped by shapes, or under platform UI on 9:16 | sheet, phone sheet |
| D9 | A name, number or claim that differs from `facts.md`, or one number shown two ways | sheet, `facts.md` |
| D10 | An off-palette blend, or two accent events in one beat | report, sheet |
| D11 | A near-silent section in a film with sound, clipping, or more than two impacts | report |

## 4. Notes and fixes

Write each problem as one line: `t=4.2s · where · problem → exact change · what stays`. Rank them:

- **P0** breaks the read or the contract: unreadable, wrong, broken, a tell in the hero shot, any FAIL above.
- **P1** weakens the piece: a dead stretch, a soft payoff, a seam that jumps.
- **P2** polish.

Fix every P0 and the P1s worth their time: text first, then timing, then detail. Re-render only what changed and review it once. A second full pass only when a P0 is still open. Never score a piece out of ten: a score finds nothing to fix. When a fix does not hold, compare the frames either side of the problem, list every difference, and change only the line that causes it.

A fresh pair of eyes helps when the host can start a separate reviewer: give it only this file, the sheets, `SPEC.md` and `facts.md`, never your build notes or opinion, and ask for P0 and P1 lines in the format above.

## Requests, translated

| The client says | Change |
| --- | --- |
| "Too fast" | Slow every camera move and travel to about 0.7× of its speed; leave cuts and pops alone |
| "Speed it up" | Shorten holds and the beat by the same amount; later beats move up; leave the curves alone |
| "The titles move" | Land them, then hold them dead still until they leave |
| "It feels like slides" | Enter the next scene through an object on screen; cut a move mid-flight; change the ground between worlds |
| "It feels cheap" | Remove a third of the motion, give the arrivals longer tails, add a real shadow or material, cut the glow |
| "Make it pop" | One stronger hero move and one accent event, not more effects |
| "It's boring" | Check for dead stretches and identical entrances; vary the transition kinds; add a payoff that plays at full speed |
