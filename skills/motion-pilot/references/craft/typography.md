# Type in motion

In most brand motion, type is the voice the viewer reads. It should arrive like a thought, hold still while it is read, and leave cleanly. Treat the type treatment as part of the design, not a delivery vehicle for words.

## Rules

1. **One line, one size.** A title stays on one line. Measure every variant (`M.measure`), fit the longest (`M.fit`), and use that size for the whole set. Never break a title onto two lines because it is long: cut words or reduce the size for all.
2. **Readable or decorative, never in between.** A line meant to be read is at least 2.6% of the frame's short side and holds 0.5 s plus 0.3 s a word. Decorative type (a giant cropped word) may be unreadable on purpose.
3. **Size with intent.** Titles at 4 to 9% of the frame height; quiet lines at 2.5 to 4%; hero words may fill 60 to 90% of the width.
4. **Sentence case, no full stops.** Punctuation only where it changes meaning (a real question). Caps only for small, tracked labels, and sparingly.
5. **Stress with weight or a move, not with a second colour.** One highlighted word per film moment at most, and only when it carries the meaning.
6. **Tabular figures** for anything that counts, so a count-up does not jitter.
7. **Centred rotating phrases stay centred.** Position each phrase from its own full width so typing never shifts it, and slide the row's x while the old phrase fades.
8. **Land and stay still.** A landed title is dead still until it leaves. No drifting, breathing or creeping scale.
9. **Vary the entrance.** Within a film, no two consecutive titles arrive the same way.

## Entrances

| Treatment | Recipe |
| --- | --- |
| **Typed** | Letters appear on hold keyframes, 20 to 45 ms apart. A cursor is solid while typing and blinks about 3.6 times a second when idle (`M.blink()`, in real output time). Decide whether the cursor rides the text: often cleaner without it once the cursor has done its story job. |
| **Rise from the baseline** | Each line clips its own letters (`overflow: hidden`, padded for ascenders and descenders, margin given back); letters rise 115% → 0 on a long ease-out, 18 to 24 ms apart. |
| **Mute, then ink** | Two copies of the line: a muted copy rises, then the full-ink copy fades in over each letter about 180 ms behind. Feels like the text is being confirmed. |
| **Per-word blur** | Each word from `blur(6px)` and opacity 0 to sharp in about 130 ms, 60 to 70 ms apart, no translate. |
| **Grey to ink** | Each word from light grey to full ink, 70 to 100 ms apart, no position change. Good for a voice reading along. |
| **Whole-line blur** | The whole line from 8 px blur to sharp in 130 to 200 ms. |
| **Letter by letter for a name** | Opacity 0.3 → 1 with a slight blur, 100 ms apart. |
| **Scatter to sentence** | Words start at random offsets, rotations and blur and land on a gentle overshoot (`back(1.25)`), 140 ms apart; optional confetti on the last word. Playful brands only. |
| **Slot roll** | One word in the sentence rolls through options like a slot machine, about 100 ms a roll, landing on the answer. |
| **Highlight box swap** | A filled box behind one word; the word changes while the box width tweens to fit (both ways). |
| **Sticker type** | Heavy display type with a contrasting smaller second word set at an angle, overlapping the first ("Preferential" with "Access" tucked under its tail); a small icon badge pops beside it. Consumer and launch films. |
| **Hand-written** | The wordmark is written on as a single stroke (trim path) with a slight boil, at a hand's pace. Organic and craft brands. |
| **Giant cropped type** | A word larger than the frame, cropped, sliding through as a wipe. |
| **Counter roll** | `round(n * ease(p))` over 1.2 to 1.6 s, then hold; the label arrives 50 ms after the number. |

## Exits

Faster than the entrance: a blur-out and fade of 130 to 250 ms, word by word or all at once, or with the scene's own move. A line never shrinks or slides back the way it came unless the whole frame does.

## Fonts in practice

- Use the brand's own faces; fetch Google families with `scripts/fetch_font.py`; ship only the weights the brand uses, or 600 and 700 render as fake bold.
- Fonts load before frame 1 (`M.ready()`). Inside HTML strings write `font-family:'Name'` with single quotes.
- Reserve the width of the widest fallback for any line that animates letter by letter, so a late font swap cannot shift it.
- Display faces that read well in motion: tight grotesks at 600 to 700 with -2 to -3.5% tracking; a characterful serif for premium; a condensed 800 for hype. Body faces stay simple.
