# Timing and easing

The numbers behind the principles. Defaults, not laws: a brand profile, a reference the client gave, or a moment that does otherwise on purpose wins for its own beat.

## Curves by role

| Role | Curve | Engine | Notes |
| --- | --- | --- | --- |
| Arrive, land, settle | `cubic-bezier(.16,1,.3,1)` | `M.ease.arrive` | The long tail. Most arrivals in a calm, confident piece. |
| Snappy entrance | `cubic-bezier(.22,1,.36,1)` | `M.eo5` | Quicker settle for small things. |
| Exit, leave | `cubic-bezier(.4,0,1,1)` | `M.ease.exit` | Accelerates away; 40 to 60% of the entrance's length. |
| Travel across the frame, camera | `cubic-bezier(.65,0,.35,1)` | `M.ease.travel` | Both ends eased. |
| Sheet, curtain, full-screen wipe | `cubic-bezier(.77,0,.18,1)` | `M.ease.sheet` | Strong both ways; feels weighty. |
| A pen drawing a stroke | `cubic-bezier(.65,0,.35,1)` | `M.ease.travel` | A hand starts and ends a stroke gently. |
| Gravity, a fall | `cubic-bezier(.55,0,1,.45)` | `M.ease.fall` | Then a squash on contact. |
| Pop, a dot becoming a shape | `cubic-bezier(.2,.7,.3,1)` | `M.ease.pop` | Pair with a keyframed overshoot (scale .35 → 1.12 → 1). |
| Reach, a hand arriving | `cubic-bezier(.34,1.45,.64,1)` | `M.ease.reach` | Built-in overshoot. |
| Rivet, something landing hard | `cubic-bezier(.34,1.6,.64,1)` | `M.ease.rivet` | More overshoot, shorter. |
| Ambient loop | sine in-out | `M.ease.sine` | For things that breathe on purpose (rare). |
| Colour flood, circular reveal | exponential in-out | `M.xio` | Fast middle, so the flood reads as a decision. |
| Implosion, zoom through | exponential in | `M.xi` | Accelerates into the next world. |

The same `ease-out` at 500 ms on everything is the flat default that makes a piece look generated. Mirror curves across a seam: an element that leaves on an ease-in hands over to one that arrives on the matching ease-out, so the speed carries across the cut.

## Durations

| Element | Duration |
| --- | --- |
| Micro feedback (a press, a tick) | 80 to 150 ms |
| An icon or chip changing state | 150 to 250 ms |
| A card or panel arriving | 250 to 400 ms |
| A sheet or curtain across the screen | 460 to 680 ms |
| A camera move or colour flood | 400 to 700 ms |
| A stroke drawn | 340 to 620 ms, longer for longer paths |
| A logo's construction, complete | 1.4 to 2.2 s, then the lockup and the name |
| A dramatic reveal | 0.6 to 1.2 s |

**Distance scales duration.** At 100 px of travel use the base; at 200 px about 1.3×; at 400 px about 1.6×. **Size scales duration.** Small things move faster than big ones. **Frequency scales duration.** The more often a person triggers something, the shorter and quieter it must be; something triggered dozens of times a day should be instant (see `genres/web-motion.md`).

**Exits are 40 to 60% of entrances.** A lockup that arrived over 500 ms leaves in 240 ms, then the sheet behind it lifts.

## Staggers and overlap

| Pattern | Step | Whole stagger |
| --- | --- | --- |
| Letters typed | 20 to 34 ms | Under about 400 ms for a name |
| Letters rising | 18 to 24 ms | Under about 400 ms |
| Words | 60 to 120 ms | Under about 600 ms |
| List items, cards | 40 to 80 ms | Under about 500 ms |
| Parts of a mark (fingertips, rivets) | 30 to 45 ms | Under about 200 ms |
| Blocks of a page arriving | 60 to 80 ms | Head first, then blocks |

The next element starts when the previous is a third to a half done. Stagger in reading order, or from the cause outward (from the click, from the centre of the mark).

## Springs

Name a spring by its damping ratio:

| Damping | Reads as | Use |
| --- | --- | --- |
| 1.0 | No overshoot | Type, logos at rest, anything serious |
| 0.7 to 0.85 | Premium, controlled | UI, cards, a hand arriving |
| 0.4 to 0.6 | Playful | Consumer apps, pops, stickers |
| below 0.3 | Cartoon | Characters only |

Position and scale may overshoot; opacity and colour never do. A closed-form spring of time keeps every frame renderable on its own: `M.springD(x, damping)` in the engine. In CSS, a `linear()` easing sampled from the same function, or a cubic-bezier with an overshoot (`.34,1.45,.64,1`) as a cheap approximation.

## Holds

| What | Hold |
| --- | --- |
| A line to be read | 0.5 s plus 0.3 s a word |
| A one or two word chapter line | 0.4 s minimum |
| The film's last line | At least 2 s |
| A logo lockup in a preloader | About 1.2 to 1.5 s, then leave |
| An end card with a call to action | 1.5 to 3 s |
| Before a payoff | 0.3 to 0.75 s of stillness, then the payoff at full speed |

A landed title is dead still. If something must keep moving, move the next element, the camera, or the world behind it.

## Motion personality

Pick one per brand and keep it everywhere. Record it in the brand profile.

| Personality | Durations | Curves | Overshoot | For |
| --- | --- | --- | --- | --- |
| Calm and trusted | 400 to 700 ms | Long ease-outs, sine | 0% | Finance, law, health |
| Premium | 350 to 600 ms | `.16,1,.3,1`; slow both-ways | 0 to 3% | Luxury, considered products |
| Confident and clean | 250 to 500 ms | `.16,1,.3,1` arrivals, `.4,0,1,1` exits | 3 to 8% on parts, 0% on type | Studios, product brands |
| Friendly | 150 to 350 ms | Springs at 0.6 | 8 to 15% | Consumer apps, delivery |
| Energetic | 100 to 250 ms | Exponential out, hard cuts | 15 to 30% | Events, launches, hype |

## Easing by material

A thing's material sets its physics. Rigid things (metal, stone, glass) take about 1.2× the time with no overshoot. Paper and cards take the base time with 3 to 5% overshoot and a soft shadow that lags. Elastic things (rubber, gel) take 0.8× with 15 to 25% overshoot. Fluids (ink, water, paint) take 1.5× with a small settle. Gas (smoke, fog) takes 2× and never overshoots.

## Scale, perception and frame rate

- Scale is perceived logarithmically: a linear tween from 0.1 to 1 seems to slow down as it grows. Interpolate scale in log space (`M.pscale(a, b, p)`) for zooms and growing objects.
- Never scale from 0 for an arrival: start from 0.3 to 0.9 depending on the drama. Dots that grow into shapes are the exception.
- Posterised motion (holding every second or third frame) is a stylistic choice for hand-made looks, never an accident.
- At 30 fps one frame is 33 ms; at 60 fps, 17 ms. Express short staggers in frames when rendering video so they stay on whole frames.

## Beats and the grid

Frames per beat = fps × 60 / BPM. Compute each beat from its index and round it (`round(i * fpb)`); never add a rounded beat repeatedly (at 128 BPM and 30 fps that drifts two frames in 32 beats). Cut on the beat; change the layout on the bar. A move that must land on a hit starts 40 to 190 ms early; a reaction starts 0 to 45 ms after it; the hit itself is a step, not an ease.

## A worked timing: a studio preloader

The approved construction preloaders in `reference-implementations/wdc-preloaders/` show these numbers working together: a cursor blinks (0 to 200 ms), four strokes orbit in staggered by 45 ms over 680 ms on `.45,0,.2,1`, become fingertips with a 380 ms pop, a hand reaches over 420 ms with overshoot, a pen draws the mark's two arcs over 500 ms each, 60 ms apart, the cursor squashes into a nib (340 ms, overshoot 1.14), a ring goes out once (460 ms), the mark slides aside (520 ms), the name types at 34 ms a letter, holds, the lockup leaves in 240 ms and the sheet lifts on a bowed edge over 680 ms. Read the file for the full choreography.
