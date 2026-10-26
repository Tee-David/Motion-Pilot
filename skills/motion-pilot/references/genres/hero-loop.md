# Website hero loops

A hero film is the ground of the homepage, not a commercial. It plays muted behind the page's own headline and buttons, loops forever, and has to make the brand legible to someone who reads only the headline.

## Rules

- **Muted, with no headline-size type.** The page supplies the words; the film supplies the world. Small labels inside product screens are fine.
- **Keep the copy zone quiet.** Action in the right half on desktop and in the top third on a phone, so the page's copy sits on calm ground. Design the tall cut separately.
- **Seamless loop.** The last frame equals the first: end on a hold that returns to the opening pose (a ring closing back to the first ring, an iris reopening on the opening frame). `qc.py --loop` checks the mean difference across the seam is under 1.
- **Both themes.** A dark film and a light film. The light film sits on a true white ground with no veil or shade over it; the page's text colour flips with the theme.
- **Chapters.** When the film walks through services, give the developer chapter times so the page can name each service as the film reaches it (a chapter bar, story bars on a phone).
- **Length** 15 to 30 s. Shorter loops repeat too visibly; longer ones are rarely watched to the end.

## Files

- 1920 × 1080 and 1080 × 1920, 30 fps, about 2.5 to 4 MB each: `-crf 26 -maxrate 2200k -bufsize 4400k -g 60 -movflags +faststart`.
- A poster per file, cut by a committed script at the exact frame the film starts from, 40 to 70 KB, art-directed per shape. The poster is the first paint and the LCP.
- New file names when a film changes (`-v2`), because caches and service workers rarely revalidate media.

## On the page

The page attaches the video after load when idle, picks the cut by orientation, never loads it under reduced motion or Save-Data, pauses it off screen and in a hidden tab, and starts it on the first tap when a browser refuses autoplay. See `genres/web-motion.md`.

## A shape that works (30 s)

The approved studio hero film: an orange cursor blinks; a ring goes out; a cloud of separate vendors churns; the mark builds; the work arrives service by service in its own world (a brand board, a search result, a website, apps on phones, a dashboard, social posts); the work gathers into a wall; everything collapses to one orange point; the mark again; the ring that opens the loop.
