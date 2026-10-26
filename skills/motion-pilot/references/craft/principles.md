# Principles, in an animator's terms

The classic principles of animation and the working habits of keyframe animators, translated into what they mean for brand motion and how to do each one in this engine or in CSS. Read this when a piece is technically correct and still feels lifeless.

## The principles

**Timing and spacing.** Timing is how long a move takes; spacing is how the frames are distributed inside it. Close spacing at the ends and wide in the middle is an ease. Two moves of the same length feel completely different with different spacing, which is why choosing a curve is never a detail. Heavy things take longer and start slowly; light things are quick and settle fast.

**Slow in and slow out.** Almost nothing in the world starts or stops instantly. Ease both ends of anything that travels across the frame; ease only the landing of anything that arrives; ease only the start of anything that leaves. Linear motion is for rotation, progress bars and things whose constant speed is the point.

**Anticipation.** A small move in the opposite direction before the main one tells the eye where to look. A cursor squashes before it becomes a nib; a card dips 4 px before it lifts; a word pulls back a few percent before it slams. Keep anticipation short (60 to 150 ms) and small (3 to 8% of the move).

**Follow-through and overlapping action.** Parts of a thing do not all stop at once. The shadow lands after its card, the label after its chip, the fingertips after the hand. Offset child layers by 30 to 80 ms and let them settle on their own curve. This one habit separates professional motion from generated motion more than any other.

**Squash and stretch.** A thing under force changes shape while keeping its volume: scale X up while scale Y comes down. Use it for impacts, landings and transformations (a cursor squashing to 1.5 × 0.55 before it pops into a nib), never on type or on a logo at rest.

**Arcs.** Living things move along curves. Swing a part round a pivot rather than sliding it in a straight line: arcs that come 150° round the centre of a mark read as construction; arcs that slide in straight read as a slide deck. Give travelling objects a slight curve in their path (a 10 px offset at the midpoint is enough).

**Secondary action.** A smaller action supports the main one without competing: rings ripple from the point where a nib lands, a trail follows a swinging arc, guides leave the frame when the construction is complete. It is always quieter than the primary action and finishes before the next primary action begins.

**Staging.** Make one thing the subject of each moment and give the eye nowhere else to go. Contrast of value, size, motion and colour all stage. If two things move at once with equal weight, one of them is wrong.

**Exaggeration.** Push a pose further than real life so it reads at speed: an overshoot of 6 to 14% on scale, a reach that starts 160 px away and 10° rotated. Exaggerate the action, never the brand: logos, type and colours stay true.

**Solid form.** Objects keep consistent light, shadow and perspective from shot to shot. One light direction for the whole film. A contact shadow under anything that sits on a surface. On paper, real shadows; on dark grounds, rim light rather than glow.

**Appeal.** Shapes and movement that are pleasant to watch: clean silhouettes, readable poses, curves with character. A mark that moves with appeal makes people want to watch it again.

**Pose to pose.** Plan the key poses first (the storyboard stills), then time the moves between them. Straight-ahead animation, frame after frame, is for organic effects only (ink, smoke, liquid), and even then inside a planned pose.

## Keyframe habits, translated

| Habit | What it means here |
| --- | --- |
| Value graph and speed graph | A curve shapes how a value changes (value graph) and how fast it moves (speed graph). Look at speed: one smooth hill per move, its peak where the move is fastest. Two hills means two moves glued together. |
| Influence | A keyframe ease handle's influence maps to a bezier. For a move that starts and ends at rest, outgoing influence `a` and incoming influence `b` give `cubic-bezier(a, 0, 1-b, 1)`. The default "easy ease" (33% each) is `cubic-bezier(.33,0,.67,1)`: a starting point, never a finish. A long-tailed arrival is about 10% out and 80 to 90% in: `cubic-bezier(.1,0,.15,1)`, close to `cubic-bezier(.16,1,.3,1)`. |
| Hold keyframes | A value that should snap, not tween: a typed letter appearing, a cut, a colour switch on the click frame. In the engine, a step: `t < t0 ? a : b`. In CSS, a 1 ms animation with `forwards`, or `steps(1)`. |
| Motion blur | Fast moves smear in camera. Render with `--sub 2` or more and `--shutter 0.5` (a 180° shutter). For one fast element in a web piece, a horizontal `blur()` peaking at the fastest frame (6 to 12 px for type, 15 to 20 px for full-frame moves). |
| Parenting and nulls | Move a group by moving its parent: a camera wrapper that pushes everything, a mark whose parts are children of the mark. In the DOM, nest elements and transform the wrapper; never animate the same property on parent and child to fake one move. |
| Precompositions | A scene is a precomposition: its own clock (`lt`), its own root, mounted for its time window. Build complex parts once inside a scene and reuse them. |
| Masks and track mattes | Reveal through a shape: `clip-path` (`inset()`, `circle()`, `polygon()`), or `overflow: hidden` on a line so type rises out of its own baseline. Pad the clip for ascenders and descenders and give the space back with negative margin. |
| Trim paths | Draw a stroke on: `pathLength="1"`, `stroke-dasharray: 1 2`, `stroke-dashoffset` from 1 to 0. Draw it off by sliding the dash on past the end (`0` to `-1`), so a line leaves rather than shrinking back. A dash of nearly zero length with round caps is a dot. |
| Shape morph | Interpolate between two paths with the same number of points, or cross-dissolve two shapes inside a shared mask. A circle that becomes a lens becomes a logo is a match cut. |
| Repeaters and echo | Trails and echoes: copies of an element at a delay, fading. One faint trail behind a swinging arc reads as speed; many read as a screensaver. |
| Offset and sequence layers | Staggers. Compute each item's start from its index (`t0 + i * step`), never by adding a rounded step repeatedly. |
| Time remap | Map output time to source time to hold, slow or skip. This is how a film is fitted to a voice file (`craft/voice.md`). |
| Wiggle | Organic jitter from seeded noise (`M.rnd(i)`), never `Math.random()`. Use it on hand-drawn lines (boiling about 12 times a second) and almost nowhere else. |
| Loop out | A loop must return to its first frame exactly. Design the last second to arrive at the first pose, then check the seam (`qc.py --loop`). |
| 3D layers and camera | CSS `perspective` and `rotateX/Y` for planes: phones, cards, browser windows. Keep yaw under about 15° when screen text must stay readable. Modelled objects need real 3D assets. |
| Adjustment layers | Grain, grade and vignette over everything, at low strength: grain 4 to 7%, vignette 4 to 8%. |
