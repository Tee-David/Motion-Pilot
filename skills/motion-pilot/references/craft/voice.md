# Voiceover workflow (ElevenLabs first, local fallback)

## Who does what
The client (or you, when given an API key) generates the voice, usually in ElevenLabs v3 or with a recorded actor, and supplies the file; the toolkit aligns it, builds the time map, rebuilds the visuals around it, and mixes it with the sound bed. The video is exactly as long as the audio. **Never time-stretch the voice.**


A voice can come from ElevenLabs, a recorded person, another text-to-speech service, the voice built into an AI app, or a free local model. All of them end as an audio file and go through the same alignment. Offer the options plainly, as in `process/intake.md` §6; many pieces need no voice at all.

## 1. Script for the ear
- 2.3-2.8 spoken words/second for a calm, charismatic read; 30s ≈ 70-80 words. Leave a beat after punchlines.
- Short sentences. Questions pull the viewer in. Contrast pairs ("Five vendors. One headache.").
- Don't read what the screen already shows; add meaning. Anchor moments where voice and screen coincide (hook words, service names, the closing line); between anchors the screen shows images.
- Spell brand and acronym pronunciations in the script (`S-E-O`, `Ny-kah`); say "twenty-five", not `25`.

## 2. ElevenLabs v3 prompt (give the client a paste-ready block)
```
[confident, playful] Line one.
[smirking] Line two... with a beat.
[mischievous] Setup. [chuckles] Punchline.
[warm] ...   [teasing] ...   [proud] Brand name. [beat] Tagline.
```
Tags that work well: `[confident] [playful] [smirking] [mischievous] [chuckles] [teasing] [warm] [proud] [whispers] [excited]`. Ellipses make natural pauses. Keep tags to the start of a line; don't stack more than two.
Voice direction template: *"Female/male, accent, age range, warm/confident/cheeky/calm, conversational never announcer, smile in the voice, slightly slower on the last line, total length N seconds."*
Export: WAV 48kHz (or best MP3), voice only, no music. Generate 3-4 takes; AI voices vary a lot between takes.
Accents: ElevenLabs offers many (including Nigerian English) in its voice library; mention it if the brand is local. A generated voice is not a human actor: for flagship work recommend a recorded actor and run the same pipeline.

## 3. Align the file
```
python scripts/align_voice.py vo.mp3 --out words.json --prompt "Brand names, SEO, product terms"
```
Prints each sentence with start/end. Check the transcript matches the script; fix prompt words if Whisper misspells the brand. Cross-check starts against silence gaps.
(Optional) `voice_elevenlabs.py script.txt --voice ID` calls the API and returns per-character timing directly (written to the public API shape; untested from the authoring sandbox: use `--dry-run` first).

## 4. Time map
Write `beats.json` linking animation moments to words:
```json
[{"src":0.2,"say":"five seconds","at":"start","lead":-0.05},
 {"src":2.5,"say":"building a brand","at":"start"},
 {"src":4.0,"say":"fire them all","at":"start","lead":-0.1}]
```
`python scripts/build_timemap.py words.json beats.json --dur <audio seconds> --src-dur <animation seconds> --out timemap.json`
Rules: knots must strictly increase on both axes; map reading moments to **long output spans over short source spans** (a hold); skip a scene by jumping source time inside a full-colour frame; entrances stay at 1x speed (give the first 0.4s of a beat a 1:1 knot).

## 5. Rebuild the visuals around the voice
Remove on-screen sentences that duplicate the voice; keep short anchor words (the hook, service names, the close). Roles/lists named by the voice should *appear on their word* (use per-word knots). Use `rt` (real output time) for text that must land on a word.

## 6. Mix
`python scripts/sound.py --cues project/cues.json --timemap timemap.json --voice vo.wav --dur <audio s> --palette clean-tech --out mix.wav` then `render.py ... --timemap timemap.json --audio mix.wav`.
If the voice file starts with silence you want to keep (cold open), keep it: the video begins with motion + effects, then the voice enters.

## Local fallback (no ElevenLabs)
`scripts/voice_local.py "text" --voice af_heart --out vo.wav` (Kokoro ONNX; needs `pip install kokoro-onnx soundfile` and the model files; American/British voices). Good for draft timing and animatics; disclose it is a draft voice. The model cannot truly laugh; use pauses for humour.

## Audio you cannot hear
You cannot listen. Verify duration, loudness, clipping and word timing by measurement, and say plainly that tone, accent and delivery need a human ear.
