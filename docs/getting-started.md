# Getting started

## 1. Install the skill

```bash
npx skills add Tee-David/Motion-Pilot
```

The CLI asks which agents to install for and copies `skills/motion-pilot` into each one's skills folder (for example `.claude/skills/motion-pilot/` or `.agents/skills/motion-pilot/`). To install by hand, copy that folder there yourself.

Restart your agent so it picks up the new skill.

## 2. Ask for something

Motion Pilot loads when you ask for motion of any kind; you do not need to name it. Start with what you want and anything you already have:

> Make a 30 second brand film for my studio. Site: example.com. Logo attached. I like the pace of this: <link>.

It replies with what it understood and up to five short questions, each with options. Answer what you like, or say "just go".

## 3. Install the render tools (when you want files)

Planning, storylines, the spec and written storyboards need nothing. Rendering needs:

```bash
pip install -r requirements.txt
python -m playwright install chromium
# and ffmpeg: brew install ffmpeg | sudo apt install ffmpeg | winget install ffmpeg
```

Optional:

| Tool | For |
| --- | --- |
| `pip install faster-whisper` | Aligning a voiceover to the picture |
| `pip install kokoro-onnx soundfile` and its model files | A free local voice for drafts |
| `ELEVENLABS_API_KEY` in your environment | Generating the voice with ElevenLabs |

## 4. The commands your agent will run (from the skill folder)

```bash
python scripts/new_project.py my-film --style keynote-dark        # scaffold; --list shows the presets
python scripts/render.py my-film --w 1920 --h 1080 --dur 12 \
  --sheet 1,3,5,7,9,11 --sheet-out board.jpg                      # a storyboard sheet
python scripts/sound.py --cues my-film/cues.json --dur 12 --palette clean-tech --out mix.wav
python scripts/render.py my-film --w 1920 --h 1080 --dur 12 --audio mix.wav --out film.mp4
python scripts/qc.py film.mp4 --expect-frames 360 --expect-dur 12 --audio --black --freeze
python scripts/review.py film.mp4 --out review/
```

Long renders run detached and resume from cached parts if stopped.

## 5. Study a reference

```bash
python scripts/analyze_reference.py reference.mp4 --out refs/
```

You get a contact sheet, change events per 10 seconds, the holds, the palette and the loudness. Drop the reference into the conversation and Motion Pilot will borrow its grammar, never its content.

## 6. Teach it your brand

Copy `references/brands/README.md`'s template into `references/brands/<your-brand>.md`: colours with their roles, fonts, the logo files, and a motion identity (one signature curve, three durations, the one gesture your brand owns). Every piece for that brand starts from it.
