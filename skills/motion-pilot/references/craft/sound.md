# Sound

Sound is half of what makes a piece feel like a real commercial, and a silent film is noticed before any frame is judged. Plan it on purpose: choose the bed from the brand's mood, give every visible event that deserves one a sound, duck everything under a voice, and master to the platform.

## When there is sound

- A film over about 15 s that tells something gets a bed and sounds on its visible actions, unless it is made to play muted.
- A website hero loop, a preloader on first load and most UI motion are silent. Design them to work with no sound at all.
- Short pieces (a logo sting, a 6 s bumper) follow the request: often one riser into one impact.
- Each storyline states its sound in one line: the bed's feel and tempo, the one moment the music changes, which actions get effects, or silence and why.

## The clock

- **With a voice, the voice is the clock.** Each beat starts on its anchor word; text lands on the word that says it (`craft/voice.md`).
- **With music only, the music is the clock.** Land the payoff and the mark on strong beats; cuts follow the motion, not every drum.
- Let the sound act the story: the old way sits near silence, the music opens when the brand arrives, holds back before the payoff.

## Beds (`scripts/sound.py --palette`)

| Palette | For | Bed | Drums | Character |
| --- | --- | --- | --- | --- |
| clean-tech | Product films, SaaS, finance, studios | Saw pads, minor ninths, bass, about 120 BPM | Four on the floor from the first impact | Mid |
| bright-pop | Consumer apps, delivery | Major pads and a plucked arpeggio | Half-time kick and snap | Bright |
| warm-lofi | Personal brands, creative | Sine pads, dark | Lazy swung kick and snare | Dark |
| bold-poster | Events, drops | Heavy bass and sub kick | Four on the floor, big impacts | Mid-bright |
| dreamy-glass | AI, wellness, luxury | Long sine pads and a bell arpeggio | None | Bright, long reverb |
| minimal-ui | Minimal, fintech, trust | None | None | Ticks, clicks and soft whooshes only |
| cinematic | Brand films, trailers | Low drones | Hits only | Dark, big risers |
| none | Voice only, silent heroes | None | None | Effects only |

The synthesiser makes clean, usable commercial beds and effects. It is not a composer: for an emotional film a real licensed track beats it, and you should say so when proposing the sound.

## Effects

Few and exact. Every effect has a cause on screen; too many read as a template.

| Cue | Only on |
| --- | --- |
| `click` | A real cursor or finger press on screen |
| `type` | Each typed character (or every second one when typing is fast) |
| `tick` | Light UI changes, a chip landing, a guide drawing |
| `pop` | A badge, dot, rivet or number landing |
| `swap` | A word or stat swapping on one stage |
| `whoosh`, `swipe` | A scene change or a large object moving fast |
| `notify` | A toast or notification arriving |
| `riser` then `impact` | The payoff or the mark, once in a film, twice at most |
| `ding`, `success` | A completed state, sparingly |

- Declare each cue next to the animation that causes it: `M.cue(t, 'pop')`. The time map moves cues with the picture.
- A sound's peak lands one frame after its picture: light arrives before sound, and a sound early feels wrong sooner than one late.
- Rotate two or three variants of a repeated sound; the same whoosh on every cut is the most common tell.
- For social, the first 0.5 s has a hit or a click.
- Over a strong music bed, a typing-heavy film can drop the keys.

## Mix

- Social: about −14 LUFS integrated, true peak at −1 dBTP or lower. Website video that may be heard: −16 to −18 LUFS.
- A voice sits on top. Bed and effects duck 40 to 55% under it with about a 0.3 s envelope; effects under a voice drop another 20 to 30%.
- Each hit sits 3 to 6 dB over the bed. A bed with most of its energy under 150 Hz plays as nothing on a phone speaker.
- Fade the last 0.25 s; give endings 1.5 to 2 s of tail.
- Reverb 0.3 to 0.9 s for UI palettes, 1.5 to 1.8 s for cinematic and glassy ones.
- Measured on references: hooky social ads sit around −7 to −13 LUFS; premium pieces −17 to −20 with wide dynamics; launch films around −13.5 with 3 to 4 onsets a second.

## Real music

`sound.py --music track.mp3` loops or trims a supplied track, fades it in and out and ducks it, with effects on top. Enter at the track's strongest bar, not a quiet intro; end on a bar line with a short fade under the end card. Sync cuts to its beats with `--bpm` and the time map, or find transients with `scripts/analyze_reference.py` (its tempo is rough: check the waveform). Licensing is the client's responsibility: ask for the source. Never use a track lifted from a reference video.

## Per format

- **Hero (muted):** design silent; export a sounded version only if asked.
- **9:16 and 16:9:** the same mix; re-time the picture, never the audio.

## You cannot hear it

Verify duration, loudness, true peak, clipping and where the hits land by measurement (`qc.py --audio`, `review.py`), and say plainly that tone, balance and feel need a human ear.
