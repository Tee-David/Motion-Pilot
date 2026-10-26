# Render pipeline, delivery and QC

## Fast loop
1. `new_project.py DIR --style X` → edit `project.js` (copy, assets, timing).
2. `render.py DIR --w 1920 --h 1080 --dur N --sheet 0.5,2,4,6 --sheet-out s.jpg` → **look at it** (both orientations, both themes).
3. Fix layout, then sound: `sound.py ...` (palette) → listen via measurements (LUFS/peak).
4. Full render, detached: `setsid nohup python scripts/render.py DIR ... > log.txt 2>&1 &` and poll the log. Output parts cache in `DIR/.parts/` so a stopped job resumes.

## Formats
- Always re-layout per aspect ratio (`M.V` flag, `u=Math.min(W,H)/1080`); never crop 16:9 into 9:16.
- Social masters: 1920x1080 and 1080x1920, 30fps, `--sub 2` motion blur, final `-crf 17-18`, AAC 256k, `+faststart`.
- **Website hero:** muted, seamless loop (last frame = first frame), 15-30s, 2.5-4 MB per file (`-crf 26 -maxrate 2200k -bufsize 4400k -g 60`), plus a poster JPG. Design for text zones: no big type where the page headline/buttons sit; bake a dark/light shade where HTML text lands; remove headline-size type from the video (the page has its own). Offer `<video autoplay muted loop playsinline>` with desktop/mobile `<source media>` variants, and a reduced-motion still.
- Hero loop: finish with a circular reveal of the opening frame; check first/last mean diff < 1.
- Light + dark variants: ship both from one build (`?theme=` + tokens). The hero text colour on the site must flip too; tell the developer.

## Hard-won gotchas
- **Background jobs die when the chat turn ends.** Always `setsid nohup`, one script per pipeline, write a `*_ok.txt` after each stage; on resume check what finished.
- **Never run two pipelines on the same outputs** (corrupted MP4s). `render.py` takes a project lock; ffmpeg encodes that write the same file must be sequenced in one script. Never `pkill -f` a pattern that matches your own command.
- **Shell command cap ~300 s:** keep long work in the background and poll.
- **Warm the scene state:** a chunk starting mid-scene works here because scenes are pure functions of time; if you add state, don't.
- **Re-cut by splicing** with ffmpeg `trim`+`concat` filter from CRF 14 masters, then encode once. Inspect frames either side of each join.
- **Fonts/images must be loaded before frame 1** (`M.ready()` does it).
- **Playwright Chrome needs `--allow-file-access` only for some setups;** the renderer opens `file://` pages directly.
- **Next.js `/_next/image` rejects most widths:** fetch originals.
- **Whisper:** pass a numpy array, not a path.
- **Emoji:** don't rely on an emoji font; use inline SVG icons.
- When a transform misbehaves, read back computed values with a debug evaluate instead of guessing.

## QC (every file, before saying done)
`python scripts/qc.py out.mp4 --expect-frames N --expect-dur S --audio [--loop] --sheet 1,3,5,... --black --freeze`
Then look at the sheet: text fits, hook centered, nothing clipped, no tile over a headline, splices clean, correct theme. Say what you checked by measurement and what by eye; you cannot hear the audio. Then run `scripts/review.py` (`process/review.md`).

## Hand-off note (always include)
Files + sizes + durations; what changed; claims/stats in the copy to be confirmed; assets that are recreated rather than real; developer notes for heroes (chapter times if any, theme switching, autoplay attributes).
