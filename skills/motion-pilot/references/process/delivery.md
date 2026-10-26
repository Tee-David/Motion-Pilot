# Delivery

## Before saying "done"

1. `python scripts/qc.py out.mp4 --expect-frames N --expect-dur S --audio --sheet 1,3,5,... --black --freeze` passes, plus `--loop` for anything that loops.
2. `python scripts/review.py out.mp4 --out review/` has no open P0.
3. Every format and theme promised has been rendered and checked, not only the first one.
4. File sizes fit where they are going (a website hero 2.5 to 4 MB per file; social platforms' limits; email never carries video).

## The delivery note

Write `REVIEW.md` in the project and put its short form in the reply:

- **Files**: each file with its format, theme, duration and size.
- **The calls you made**: the storyline you built and, if you chose, the other two in one line each.
- **Measured and looked at**: what QC and review measured (frames, duration, loudness, true peak, loop seam, first frame) and what you only looked at. The sound was measured, not heard.
- **To confirm**: every claim, number and name on screen; every recreated screen labelled as such; any licence (music, fonts, footage).
- **The weakest shot**, and what you would change with more time.
- **For a developer** (heroes, preloaders, web motion): chapter timestamps, poster frames, autoplay attributes, the theme switch, reduced-motion behaviour, where text sits over the video.

## Handing over a web piece

- The video element: `<video autoplay muted loop playsinline preload="none" poster="…">` with a wide and a tall source chosen by orientation, attached after the page has loaded, never under `prefers-reduced-motion: reduce` or Save-Data, paused off screen and in a hidden tab.
- A preloader or page curtain: the CSS, the component's phase switch (enter, wait, leave), the timings it needs repeated in code, the reduced-motion rule, and the non-blocking rule (see `genres/web-motion.md`).
- Posters cut by a committed script at the exact frame the film starts from, so the poster is never a picture of an old cut.

## Keep the decisions

Settled wording, numbers, colours and rejected ideas go in a `HANDOFF.md` in the project, and any lesson that should change how the next piece is made goes in `taste/lessons.md` in the lesson format. A brand's second film should start from everything its first one taught.
