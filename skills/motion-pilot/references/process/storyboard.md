# Storyboard: approve the stills before anything is timed

A storyboard is the cheapest place to change a film. Once shots are timed and sound is cued, a change of story costs the whole build. Make one for every new film over about 15 s, for every new logo construction, and whenever the client wants to see the direction before the motion.

## Make the stills from the real build

1. Build each shot in the project at its key moment only: real words, real fonts, real colours, the hero big enough to read on a phone. No timing yet; a shot can be a static pose inside its scene's `update` at one `lt`.
2. Render them all at once: `python scripts/render.py DIR --w 1920 --h 1080 --dur N --sheet 1.5,4,7.2,... --sheet-out board-16x9.jpg`, and again at `--w 1080 --h 1920` when the tall cut ships, and with `--theme light` when both themes ship.
3. Look at every still. Fix and re-render until each one reads as what it is to a stranger.
4. Write `STORYBOARD.md` beside the sheets: one heading per frame, `## 01 The hook (0.0 to 3.0 s)`, then one line of what happens, one line of what is read, one line of sound.
5. Show the client the sheet (a web page with the stills and their lines is easiest to comment on) and stop.

## Notes change only their frames

When the client marks a frame, re-pose and re-render only that frame and keep the approved ones as they are. Once they say go, time the film from the approved stills: each still is the pose its shot must pass through.

## What a good board shows

- Frame 0 is already a picture: never black, never the logo alone.
- Each frame names its objects without a caption; an object you would have to explain is a problem now, not later.
- Worlds change across the board (ground, scale, light), and each change has a cause in the frame before.
- The accent appears once per frame at most.
- The tall and wide boards are recomposed, not cropped: stacked vertically on 9:16, side by side on 16:9.
- Covering the words, the pictures still tell the story. Covering the pictures, the words still make the pitch.

## Logo constructions and preloaders

For a mark that builds itself, board the construction as five to eight stills: the first gesture, the parts arriving, the moment the parts become the mark, the mark complete, the lockup, the hold. Show it on both grounds. Agree the order of the reveal (mark first, then the name slides out from behind it; or the name typed beside a finished mark) before timing a single curve.
