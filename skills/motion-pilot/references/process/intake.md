# The brief: ask, gather, then make

Good motion is made with someone, not for them. This skill never produces a film from one sentence and hopes. It asks for what would make the piece theirs: the brand, the material, a reference they love, how they picture it flowing. Then it fills every gap itself, says what it assumed, and gets on with the work.

Every ask is an offer, not a gate. Each one is optional, explained in one line by what it improves, and paired with what happens without it. Someone who answers nothing still gets a considered piece; someone who brings a brand guide, three references and a voice file gets a far better one. Never make the person feel tested.

## 1. Read the person first

Within the first message, judge two things and adapt:

- **How technical they are.** A designer says "ease-out on the arrivals, 9:16, no VO". Someone else says "make my logo move nicely for Instagram". Match their language. With a non-specialist, never use a term without its plain meaning beside it ("a hold, a moment where everything stays still so it can be read").
- **How much they already decided.** If they bring a script, a storyboard or a reference film, follow theirs and ask only what is missing. If they bring a single sentence, offer more help.

## 2. Research before asking

Do this quietly, so the questions are sharp and few.

- **Their website**, if there is one: `python scripts/brand_probe.py URL --out probe --pages /about,/services` returns real colours ranked by on-screen area, fonts, headlines, logo files and screenshots. Look at the screenshots: light or dark, dense or airy, photographic or flat, serious or playful.
- **Anything attached.** Logos (SVG first), brand guides (law for colour and type, advice for the rest), flyers, posts, decks and past videos, which say more about mood than any website.
- **Their references.** Run `python scripts/analyze_reference.py ref.mp4 --out refs` on each: a contact sheet, the pace (change events per 10 s), the holds, the palette by share, loudness. Write down the grammar you will borrow and mark what you measured apart from what you guessed.

## 3. The first reply: one short message

Open with what you understood in one or two lines, then ask. Keep it to one message the person can answer in a minute, with options they can tap where the host offers a question tool. Ask at most five things, in order of value, and skip any the research already answered:

1. **Where it will play, and for how long.** Instagram or TikTok (tall, 9:16), YouTube or a website (wide, 16:9), a square post, a website's background video, a loading animation on a site, a presentation. 6, 15, 30 or 60 seconds.
2. **How it should feel.** Calm and premium, confident and clean, friendly and upbeat, loud and exciting. Offer two or three looks from the style library with a picture each; a person who cannot name a feeling can always point at one.
3. **What the viewer should remember, and do.** The one thing, in their words, and the one action (visit, download, book, follow).
4. **A voice, music, or neither.** See section 6 for the options to offer.
5. **What they can share.** See section 4: offer the list, not a demand.

Then one line of assumptions you will make if they would rather not answer ("If you'd like me to choose: 30 seconds, tall and wide, light and dark, music with no voice, your site's colours"), so "just go" is always a valid reply.

## 4. Materials worth asking for

Offer this as a menu. Each line says what it adds.

| Material | What it improves | Without it |
| --- | --- | --- |
| Logo as SVG (colour, white, icon alone) | The logo can build itself from its own parts, sharp at any size | A PNG is traced as a last resort, and you say so |
| Brand guide, or colours and fonts | A faithful palette and type | Taken from their site and confirmed with them |
| Real screens, photos, past work, product clips | The real product as the hero; real proof | Screens are recreated and labelled as recreated; no stock photos posing as their work |
| References they love (videos, links, screenshots) | The fastest way to agree on a feel | The style library and your recommendation |
| How they picture it flowing ("starts with the problem, ends on the logo", a rough sketch, a list of scenes) | Their story, not a template's | Three storylines for them to choose from |
| A script or key lines | Their voice and claims | You write it and mark every claim to confirm |
| Real numbers, client names, awards | Proof that is true | Left out; never invented |
| A voice file or a voice preference | Timing built round real speech | See section 6 |
| A music track and its licence | Real music | A synthesised bed, or silence |

Ask for exactly what the chosen piece needs and no more. A logo reveal needs the SVG and a feeling; it does not need a script.

## 5. Where to find references (optional)

If they have no reference but would like to find one, suggest a few places and how to use them. A reference is a picture of a feeling: it saves rounds of "not quite".

- **Dribbble** and **Behance**: search "logo animation", "motion design", "product promo"; strong for logo reveals, UI motion and brand systems.
- **Pinterest**: search a feeling plus "motion graphics" ("minimal motion graphics", "kinetic typography"); good for building a mood board quickly.
- **Vimeo**: search "brand film", "explainer", "title sequence"; the Staff Picks are a reliable bar for craft.
- **YouTube**: brand launch films, product keynotes and "motion design reel" searches.
- **Instagram and TikTok**: their own saved posts are often the truest reference; screen-record the one they like.
- **Awwwards** and **Godly**: website heroes, preloaders and page transitions in their real context.
- **Mobbin**: real app screens and flows, for product demos.
- **Their competitors and heroes**: the brands they admire, or the ones they want to stand apart from.

A screen recording, a link, or a screenshot is enough. Borrow the grammar of a reference (pace, how things arrive, the palette's roles), never its content or its brand.

## 6. Voice and sound: offer the options plainly

Many pieces need no voice: logo reveals, website loops, loading animations and most short social clips. Offer a voice only where the story is spoken.

| Option | What they need | Notes |
| --- | --- | --- |
| No voice | Nothing | Type and pictures carry it; the default for short and muted pieces |
| A recorded voice | A phone recording or a voice actor's file | The most human result; the pipeline aligns any clean recording |
| ElevenLabs | Their API key (`ELEVENLABS_API_KEY`) or a file they generate in the web app | Natural, expressive, many accents; `scripts/voice_elevenlabs.py` and a paste-ready prompt in `craft/voice.md` |
| Another text-to-speech service or the voice built into their AI app | A file exported from it | Fine for many uses; check the service's terms for commercial use |
| A free local voice | `kokoro-onnx` and its model files | Good for draft timing and some finals; `scripts/voice_local.py` |

For sound, offer: a synthesised music bed and effects made by the pipeline (no licence needed); their own licensed track; free music libraries (YouTube Audio Library, Pixabay Music) or paid ones (Artlist, Epidemic Sound, Musicbed), checked for commercial use; sound effects from Freesound or Pixabay with each licence noted; or silence. Free tools that help: ffmpeg for everything, Audacity for a quick listen and trim. Licensing stays with the person: ask where a track came from, and never use one lifted from a reference video.

## 7. Variants

Offer variants where a choice is genuinely open, never as padding:

- three storylines in words before anything is built (`process/storylines.md`);
- two orders for a logo lockup (mark first then the name, or the name typed beside the mark);
- light and dark, tall and wide, as standard deliverables;
- two or three stills of a key frame in different looks, when the look is undecided.

Variants are cheap as words and stills, and expensive as finished films. Decide early.

## 8. Push back, kindly

Say it plainly, offer two or three options and recommend one, when the brief packs too much into the length (a 30 s film holds five or six beats), a line reads as a guarantee, invented numbers are asked for, the assets are too small or the wrong shape, the screen and the voice would say different sentences at once, the look needs 3D or illustration the engine cannot make, or motion is asked for on something people use dozens of times a day.

## 9. Mood and feel

Use this to choose a direction and say why. A brand profile in `brands/` overrides it.

| Feeling | Palette | Type | Physics | Sound |
| --- | --- | --- | --- | --- |
| Trusted, expert (finance, law, health) | Deep navy or ink, one bright accent, generous white | Grotesk 600 to 700, tight tracking | No overshoot; long ease-outs; steady 2 to 4 s beats | Minimal UI ticks, a quiet bed |
| Friendly app, delivery | One saturated brand colour with the product's UI | Rounded geometric 700 to 800 | Springs at damping 0.5 to 0.7; pointer clicks; pops | Bright and plucked |
| Creative studio, personal brand | Paper and ink with one hot accent | Heavy grotesk, big scale contrast | Construction, scatter and snap, small overshoot | Warm, clean-tech |
| Premium, luxury | Near-black or warm stone, metallic, serif accents | An elegant serif with a thin sans | Slow; long dissolves inside one world; few cuts | Sparse, cinematic or glassy |
| Event, hype | Duotone, giant condensed type | Condensed 800 and up | Hard cuts every 0.3 to 0.8 s; slams | Heavy bass, hits on cuts |
| AI and modern product | The product's own ground; one horizon of light | A clean sans | Typing as a story step, soft reveals | Glassy, airy |

## 10. What intake leaves behind

- `facts.md`: every fact, number, name and claim that may appear, each with its source. Nothing goes on screen without a line here.
- The brief at the top of `STORYLINES.md`: format, length as a range, ratios, themes, voice or not, music or not, the materials received, and every assumption in one line each.
