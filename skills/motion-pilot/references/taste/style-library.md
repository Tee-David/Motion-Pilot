# Style library: 33 references, studied
The reference library behind the house taste: *clean, product-forward, confident, mostly brand-colour or white/black canvases, UI-as-hero, kinetic type, cursor-driven demos, soft shadows, gentle blur-swaps.* The contact sheets are not shipped in the public repository; make your own for any reference with `scripts/analyze_reference.py`, and keep them beside your library. The studio's own preloaders (R30 to R33) are included as `taste/library/wdc-preloaders.jpg`. Measured numbers come from `scripts/analyze_reference.py` (outro cards trimmed). **Cuts are a lower bound** because morphs on one ground do not register as cuts; for R26 onwards the **change events** figure (every cut, morph and big move) is the better measure of rhythm. **Tempo estimates are rough**; loudness, onset density and brightness are reliable.
## How to use this library
1. Ask what mood the client wants, or propose 2-3 families from the table below (show the matching sheets).
2. Take the family's engine template + `styles.json` preset, then adapt: palette from the client's brand, type from `fetch_font.py`, copy from the brief.
3. Borrow *moves*, never copy a reference's brand, layout or footage. These are inspiration, not assets.
## Style families
| Family | References | Signature | Preset | Template |
|---|---|---|---|---|
| Keynote product film | R11, R03, R10 | Typed hook, panel-per-claim, glass/soft-shadow UI, counters | keynote-dark | keynote |
| App promo with pointer | R04, R17, R21, R14, R20 | Brand-colour stage (disc/blob), pointer clicks drive UI, notification toasts, CTA button | app-promo | app |
| Monochrome minimal UI | R05 | Black/white, pill chips + icons, one status line per beat | mono-minimal | app |
| Kinetic type on paper | R06, R19, R25, R13 | Scatter-to-sentence words, blinking underscore cursor, confetti, photo-in-window | kinetic-paper | kinetic |
| Brand-colour floods + word beats | R01, R08, R20 | One word per beat, full-bleed brand colour wipes, highlight-box swap | brand-flood | kinetic |
| Poster / event hype | R02 | Duotone, giant condensed numerals, sunburst, 0.3s cuts | poster-duotone | kinetic (needs custom pieces) |
| Aurora gradient + glass | R18, R23, R12 | Blurred gradient + grain, glass cards, prompt bar, slow ambient sound | aurora-glass | keynote |
| Logo reveal / mark construction | R22, R27, R28, R29, R30, R31 | The mark built from its own parts: drawn, constructed on guides, gathered, morphed or written on | (custom scene) | `craft/logo-construction.md`, `reference-implementations/wdc-preloaders/` |
| Launch montage, worlds that switch | R26 | A new ground every beat (black, white, brand colour), objects carried across cuts, per-word blur titles, bookends | brand-flood | keynote (custom scenes) |
| Page curtain | R32, R33 | The construction, short, between pages; sheet or halves | (web) | `genres/web-motion.md` |
| 3D studio | R09 | Real 3D, light shafts, depth of field | (out of engine scope) | ask for 3D assets or use three.js/Blender |
| Educational grid / Before-After / Making-of | R07, R15, R16, R24, R08, R10 | Formats rather than looks | any | any |

## The 25, one by one
### R01  A property platform, 'Fragmented. Structured. Credible.' (studio work in progress)
- **Family:** Brand-colour floods + word beats | 18.7s | 1180x652 | avg detected shot 15.55s | palette #0401f0 #f2f2f7 #6059db #5e605a
- **Look:** White to full brand-blue (#0000F5) floods. One bold word per beat. A single property card morphs: sticky-note chaos, then a clean grid, then ticks appearing, then a logo lockup.
- **Motion:** Slow continuous morph on one object. Tabs along the bottom (Capture / Structure / Verify / Manage) track the story like chapters.
- **Sound (measured):** -12.5 LUFS, loudness range 1.0 LU, 3.3 onsets/s, brightness 1532 Hz, sub-150Hz 22%
- **Steal:** One-word headline beats; colour flood as chapter change; a UI object that cleans itself up as the story progresses.
### R02  'Human by Design' event promo, Lagos (vertical)
- **Family:** Poster / event hype | 25.0s | 1180x1170 | avg detected shot 0.31s | palette #5031e5 #f8ce99 #18122b #261955
- **Look:** Violet #5031E5 + peach #F8CE99 duotone, enormous condensed numerals (OCT 16/17), sunburst rays, wavy pattern fills, speaker cards as portraits-in-circles on 3D boxes.
- **Motion:** Extremely fast: about 0.3s average shot, 70 cuts in 25s. Elements slam, rotate, wipe. Type is the set.
- **Sound (measured):** -10.0 LUFS, loudness range 3.6 LU, 3.9 onsets/s, brightness 1626 Hz, sub-150Hz 40%
- **Steal:** Poster maximalism for events/launches. Needs the 3D-box and sunburst building blocks. Hold one reading beat for dates/venue.
### R03  Fintech savings app (Seed-style)
- **Family:** Keynote product film | 30.9s | 1024x576 | avg detected shot 6.93s | palette #eff4fd #08080a #5e9bf3 #aec9f1
- **Look:** Pale blue #EFF4FD canvas, giant stretched blue type cropped by the frame, white UI cards floating, growth line chart, balance counters.
- **Motion:** Spacious and calm: about 7s per idea. Type scale changes carry the transitions.
- **Sound (measured):** -17.9 LUFS, loudness range 5.6 LU, 2.9 onsets/s, brightness 1860 Hz, sub-150Hz 20%
- **Steal:** Giant cropped type as a wipe; UI cards with soft shadows; counters rolling up; very wide dynamic range in the music.
### R04  Glovo app launch
- **Family:** App promo with pointer | 18.8s | 1024x576 | avg detected shot 1.95s | palette #fcfbfa #17171f #ece0a5 #585856
- **Look:** Brand yellow disc behind a dark UI list, map pins, route line, cursor typing and clicking a search field, food icons.
- **Motion:** Mid pace (about 2s per shot). Pointer clicks drive each UI change. Brand-colour disc is the recurring stage.
- **Sound (measured):** -12.7 LUFS, loudness range 2.7 LU, 4.1 onsets/s, brightness 1552 Hz, sub-150Hz 25%
- **Steal:** Pointer-driven UI demos; yellow disc as spotlight; hand-off from search to map to delivery.
### R05  Uber product teaser (minimal)
- **Family:** Monochrome minimal UI | 14.6s | 928x576 | avg detected shot 2.27s | palette #f0f0f0 #030202 #9e9e9e #656464
- **Look:** Black and white only. Rounded grey cards, pill chips with tiny icons (Courier, Ride), progress bar, status text.
- **Motion:** Quiet, precise. Slow tempo, deep low end, sparse hits.
- **Sound (measured):** -11.8 LUFS, loudness range 3.2 LU, 2.1 onsets/s, brightness 1950 Hz, sub-150Hz 23%
- **Steal:** Restraint: pill UI + one status line per beat. Shows that no colour can be the style.
### R06  Motion designer portfolio (personal brand)
- **Family:** Kinetic type on paper | 30.8s | 720x576 | avg detected shot 2.12s | palette #f9fcf9 #030303 #a1a4a0 #9c6e21
- **Look:** White page, tiny words that scatter then snap into sentences, a webcam-style photo window, glossy red 3D pills ('agencies', 'creators'), 'available for projects'.
- **Motion:** About 2s per beat. Words converge from random positions with blur; 3D glossy objects add depth.
- **Sound (measured):** -18.9 LUFS, loudness range 3.1 LU, 3.0 onsets/s, brightness 1934 Hz, sub-150Hz 25%
- **Steal:** Word-scatter assembly; photo-in-window for the human moment; glossy accent objects.
### R07  '12 Principles of UI in Motion' (Lottie)
- **Family:** Educational grid | 14.3s | 576x720 | avg detected shot 11.1s | palette #19191b #4f5353 #32534d #303648
- **Look:** Dark #19191b grid of small neon/glass objects, each demonstrating a principle (easing, parallax, masking, cloning...).
- **Motion:** A static grid; individual cells animate in sequence. Clear labelling.
- **Sound (measured):** -16.8 LUFS, loudness range 2.6 LU, 2.3 onsets/s, brightness 1383 Hz, sub-150Hz 31%
- **Steal:** Explainer/educational grid format: one concept per cell, labelled, looping.
### R08  Delivri brand identity reel (filmed off an After Effects screen)
- **Family:** Brand-colour floods + word beats | 18.9s | 576x1024 | avg detected shot 7.85s | palette #251a1e #545460 #1ea656 #2f324e
- **Look:** Brand green #1ea656. Wordmark morph, 'Reliable' repeated as stacked rows, rounded video windows floating on green.
- **Motion:** Mid pace; stacked-type repetition as a texture.
- **Sound (measured):** -12.7 LUFS, loudness range 1.7 LU, 2.6 onsets/s, brightness 1840 Hz, sub-150Hz 8%
- **Steal:** Typographic repetition as pattern; rounded media windows; the 'filmed off the timeline' making-of format.
### R09  Amazon delivery concept (3D studio)
- **Family:** 3D studio (needs 3D assets) | 20.8s | 1024x576 | avg detected shot 8.8s | palette #ebebeb #aaa9a8 #dfceae #c9baa4
- **Look:** White studio with volumetric light shafts, 3D box, alarm clock, dice, forklift; orange arrows; a fan of 'My Orders' cards.
- **Motion:** Long, slow shots (about 9s). Camera glides through a 3D scene; real depth of field.
- **Sound (measured):** -17.5 LUFS, loudness range 4.0 LU, 4.0 onsets/s, brightness 1402 Hz, sub-150Hz 36%
- **Steal:** Needs real 3D (Blender/three.js) or rendered assets. CSS 3D can fake the card fan and arrows only.
### R10  Cross-border money app concept (filmed off screen)
- **Family:** Keynote product film | 17.1s | 576x1024 | avg detected shot 6.93s | palette #0c0b0f #a4a6ac #595a61 #d8d9db
- **Look:** Purple-to-blue gradients, phone UI, a headline that repeats as a typographic stack ('Swapp Swapp Swapp').
- **Motion:** Slow reveal of the phone, then quick typographic repetition for emphasis.
- **Sound (measured):** -35.1 LUFS, loudness range 2.3 LU, 3.1 onsets/s, brightness 2135 Hz, sub-150Hz 4%
- **Steal:** Phone + gradient + typographic echo. Reads as a 'concept shot' when filmed from the editing screen.
### R11  '$2600 30-second SaaS keynote intro' (Zami) (your first reference)
- **Family:** Keynote product film | 30.1s | 576x1024 | avg detected shot 6.72s | palette #25201d #5f575d #e0e2e8 #4c4335
- **Look:** A monitor on a desk; pale-blue and deep-blue panels, glass cards, big sans headlines ('One, connected ecosystem', 'Absolute Visibility', 'All Operations.').
- **Motion:** Hook text types with a cursor, icon cloud collapses into a logo, then confident one-line panels. About 3-4 chapters of 6s.
- **Sound (measured):** -14.7 LUFS, loudness range 3.9 LU, 3.3 onsets/s, brightness 1892 Hz, sub-150Hz 25%
- **Steal:** This is the grandparent of the WDC reel. Types well on both light and dark.
### R12  Health/watch concept (jup.creatives)
- **Family:** Aurora gradient + glass | 16.5s | 1024x576 | avg detected shot 2.65s | palette #fcfbfa #f05b8c #151015 #9d9f9e
- **Look:** White canvas, 'Your body is changing.', glassy widgets (heart, rings), a full-bleed alpine photo with floating UI, hot-pink gradient with a heart.
- **Motion:** Mid pace, with a scenic photo as a surprise change of world.
- **Sound (measured):** -18.7 LUFS, loudness range 4.8 LU, 4.2 onsets/s, brightness 2274 Hz, sub-150Hz 19%
- **Steal:** Glass widgets; one photo 'world change' for emotion; pink full-bleed as the end beat.
### R13  Flyer-design motion promo ('How smooth?')
- **Family:** Kinetic type on paper | 14.6s | 576x1024 | avg detected shot 2.85s | palette #040305 #fbf8f9 #989696 #5c5b5a
- **Look:** Black base, a collage of poster designs which become phone content, then logos (Pinterest...).
- **Motion:** Fast reel; designs are the content.
- **Sound (measured):** -16.8 LUFS, loudness range 9.2 LU, 2.5 onsets/s, brightness 945 Hz, sub-150Hz 50%
- **Steal:** Showing real design work as moving collage; ends on a brand.
### R14  Starbucks delivery concept
- **Family:** App promo with pointer | 22.0s | 1024x576 | avg detected shot 3.13s | palette #edf3f0 #192c26 #b5d7c9 #56645b
- **Look:** White with soft green cloud gradients, giant cropped 'Delivery' type, drink carousel cards, 'Out for delivery' rating card.
- **Motion:** About 3s per beat; large-type wipe into UI.
- **Sound (measured):** -6.8 LUFS, loudness range 2.0 LU, 4.4 onsets/s, brightness 2308 Hz, sub-150Hz 11%
- **Steal:** Giant-type wipe into UI; carousel of product cards; loud master (-7 LUFS).
### R15  Before / After wireframe-to-animated UI
- **Family:** Before / After | 14.7s | 576x1024 | avg detected shot 2.88s | palette #101011 #f5f4f4 #676763 #83837a
- **Look:** Dark, a rough sketch phone on the left and the polished animated phone on the right, labelled Before / After.
- **Motion:** Quick cycles through app screens.
- **Sound (measured):** -14.9 LUFS, loudness range 9.5 LU, 1.7 onsets/s, brightness 975 Hz, sub-150Hz 32%
- **Steal:** Before/After split as a proof format.
### R16  'POV: You make motion design for brands' (filmed over a timeline)
- **Family:** Making-of (filmed timeline) | 26.0s | 576x956 | avg detected shot 22.81s | palette #07080c #5d5e61 #8d9092 #5c8491
- **Look:** Pastel UI scenes on a monitor with the After Effects timeline below. Text: 'Every 5 seconds', 'For every budget'.
- **Motion:** One continuous screen recording; the scenes inside are short.
- **Sound (measured):** -20.1 LUFS, loudness range 3.2 LU, 0.8 onsets/s, brightness 2064 Hz, sub-150Hz 13%
- **Steal:** The making-of format and its captions.
### R17  Gojek app ad
- **Family:** App promo with pointer | 16.5s | 1024x576 | avg detected shot 2.67s | palette #f4faf5 #27c24d #9ddeae #b8e5c6
- **Look:** Fresh green #27c24d, 'Meet gojek' wordmark, phone with map, green blob wipe, search field with typing, 'Order Sekarang' CTA button with arrow, logo mark close.
- **Motion:** About 2.7s per beat; blobs wipe between scenes; CTA button is the last image.
- **Sound (measured):** -14.8 LUFS, loudness range 3.4 LU, 2.2 onsets/s, brightness 2676 Hz, sub-150Hz 7%
- **Steal:** Brand-colour blob wipes; CTA button with arrow icon; typed search.
### R18  ChatGPT-style product moment
- **Family:** Aurora gradient + glass | 12.5s | 1024x576 | avg detected shot 4.66s | palette #0e0f12 #aacce6 #5da2f2 #9aaaad
- **Look:** Black with a blue horizon glow, a pill prompt bar typing 'Generate me a lake', a glass card with the image, then a serene photo.
- **Motion:** Calm, 12s. Cursor click triggers the result.
- **Sound (measured):** -11.4 LUFS, loudness range 3.6 LU, 2.3 onsets/s, brightness 2058 Hz, sub-150Hz 17%
- **Steal:** Prompt bar to result; horizon glow; a photo that dissolves into the wordmark.
### R19  'I am Aneke' brand-designer personal intro
- **Family:** Kinetic type on paper | 26.5s | 1024x576 | avg detected shot 1.29s | palette #ededed #020202 #a2a1a1 #5e5e5e
- **Look:** Black then white. Heavy condensed sans, 'brand designer', Nigerian flag green/white band, project thumbnails, confetti, 'Ready when you are.'
- **Motion:** Fast (1.3s avg) with punctuation hits.
- **Sound (measured):** -10.8 LUFS, loudness range 2.0 LU, 3.3 onsets/s, brightness 2301 Hz, sub-150Hz 21%
- **Steal:** Self-intro structure: name, role, origin, proof, promise. Confetti as a laugh.
### R20  Pinterest ad-concept
- **Family:** Brand-colour floods + word beats | 24.8s | 1024x576 | avg detected shot 1.96s | palette #f2f1f1 #bc0e27 #a19d9f #222122
- **Look:** Pinterest red #bc0e27 and white, 'Thousand of Inspirations' with a highlighted word box that swaps ('Motion'), floating image tiles, a create-board modal with a cursor.
- **Motion:** About 2s per beat; highlight-box word swap is the signature.
- **Sound (measured):** -9.7 LUFS, loudness range 2.7 LU, 3.2 onsets/s, brightness 1982 Hz, sub-150Hz 30%
- **Steal:** Highlight-box word swap; UI modal + cursor click for credibility.
### R21  Deliveroo order flow
- **Family:** App promo with pointer | 27.8s | 960x576 | avg detected shot 8.19s | palette #d8d7d9 #42c7b6 #959498 #000000
- **Look:** Teal #42c7b6 kit with grey map backgrounds, notification toasts ('Your Order has arrived'), 'Ready' pill, rider on a route, avatar bubbles.
- **Motion:** Long shots with small UI actions; very loud (-6.8 LUFS).
- **Sound (measured):** -6.7 LUFS, loudness range 4.7 LU, 3.4 onsets/s, brightness 1248 Hz, sub-150Hz 18%
- **Steal:** Notification toasts; route animation; a map as background.
### R22  'Visora' logo reveal and brand guidelines
- **Family:** Logo reveal / vector construct | 21.2s | 1024x576 | avg detected shot 2.26s | palette #0d0e11 #072ccc #f8fcfc #575c63
- **Look:** Black, then a vector outline of the wordmark with pen-tool bezier handles, a chrome 3D glass logo mark, colour cards (Electric Green, Cobalt Blue), website snippet.
- **Motion:** Showpiece: construction-view reveal (outline, anchors, handles) before fill.
- **Sound (measured):** -11.6 LUFS, loudness range 3.6 LU, 2.8 onsets/s, brightness 1376 Hz, sub-150Hz 34%
- **Steal:** Pen-tool construction reveal: SVG stroke-dash on the outline, anchor squares and handles that fade. Great for logo/brand-identity pieces.
### R23  Spotify feature video
- **Family:** Aurora gradient + glass | 19.9s | 1024x576 | avg detected shot 8.34s | palette #121f17 #155a24 #159b34 #12d046
- **Look:** Green gradient with film grain and blur, album tiles tilting in a grid, glass player card, 'Feel every word.' lyrics.
- **Motion:** Very slow: 8s per idea, big dynamic range (about 27 dB swing).
- **Sound (measured):** -10.2 LUFS, loudness range 23.0 LU, 0.4 onsets/s, brightness 1372 Hz, sub-150Hz 28%
- **Steal:** Blurred gradient + grain; glass cards; sparse text. Sound is almost ambient.
### R24  'POV: Pinterest hire me for a short ad' (making-of)
- **Family:** Making-of (filmed timeline) | 19.8s | 576x1024 | avg detected shot 8.29s | palette #1d1d1c #efedee #5d6059 #a3a3a3
- **Look:** Monitor on a desk, white UI slides with the Pinterest wordmark, saved-ideas collages.
- **Motion:** Slow screen-recording pacing with captions.
- **Sound (measured):** -15.3 LUFS, loudness range 4.3 LU, 2.8 onsets/s, brightness 571 Hz, sub-150Hz 40%
- **Steal:** Making-of format; use when the audience is other creatives.
### R25  Zapier product film
- **Family:** Kinetic type on paper | 27.3s | 1024x576 | avg detected shot 2.41s | palette #fbfaf7 #211517 #a09d9b #655d5d
- **Look:** Cream paper, orange underscore wordmark '_zapier', a Copilot prompt box typing, workflow nodes cascading into a diagram, 'Connect 400+ AI tools to 9,000+ everyday apps', 'your_' swap.
- **Motion:** About 2.4s per beat; nodes arrive in rhythm; one dark mid-section for contrast.
- **Sound (measured):** -17.4 LUFS, loudness range 7.4 LU, 1.8 onsets/s, brightness 617 Hz, sub-150Hz 11%
- **Steal:** Prompt-to-workflow storytelling; blinking underscore as brand cursor; node diagrams.

### R26  'Vale' token launch film
- **Family:** Launch montage, worlds that switch | 62.1s | 1920x1080 | 36 change events (5.8/10s), 9 hard cuts, longest hold 0.7s | palette #161715 #f9f9f7 #97fd97 #73f98e
- **Look:** Near-black, white and a mint-to-lime green take turns as the ground. Lens-like green spheres frame the opening and the closing title (bookends). Glass pills with red and green badges, 3D coins, orbit diagrams with coloured planets, a sunburst behind the hero coin, sticker type ("Preferential" with "Access" tucked under its tail; "Bonus" over "Yields" with a 3D emoji badge), a typed web address in a search pill.
- **Motion:** A new world every one to two seconds. Objects carry across cuts: a cube drops into a wave, the wave's peak sends out rings, the rings become a pill. Coins gather in a ring, implode to a streak, and the streak becomes the hero coin flipping onto a sunburst. Per-word blur titles with the key word in brand green. Counters as pills that multiply (5.2%, 6.7%, 22%). Bars fill on a dark ground.
- **Sound (measured):** -13.5 LUFS, loudness range 2.6 LU, 3.7 onsets/s, brightness 1750 Hz, sub-150Hz 11%, tempo roughly 157
- **Steal:** Ground switches as chapter changes; carrying one object across worlds; bookends; sticker type for a consumer brand. Leave the crypto glow and the sunburst unless the brand is that loud.
### R27  'Sun Garden' logo reveal
- **Family:** Logo reveal / mark construction (morph and write-on) | 8.6s | 1180x878 | 4 change events, one continuous take | palette #7ca275 #daddcb
- **Look:** One flat sage ground, cream shapes, a black hand-written wordmark.
- **Motion:** A sun rises from a soft blurred horizon for two calm seconds, swells into a disc, shrinks into a seed under a flower; the parts nest into the mark; the wordmark writes itself as a single line at a hand's pace. No cuts.
- **Sound:** silent recording.
- **Steal:** Morph as a construction grammar; a calm opening that earns its reveal; write-on wordmarks for craft and lifestyle brands.
### R28  'Kantiv' logo reveal
- **Family:** Logo reveal / mark construction (construct and assemble) | 5.6s | 1180x642 | 5 change events, longest hold 1.1s | palette #3c0d9a #ece7f3
- **Look:** One violet ground, a white four-point mark, faint construction guides.
- **Motion:** A shape swoops in on a curved trail, construction lines and a circle draw through it, the quarters snap into a square then split into the star, the mark flips once and settles left, and the name rises letter by letter in a lilac mute that turns white.
- **Sound:** silent recording.
- **Steal:** Construction on guides; one flip as the settle; mute-then-white type. The source grammar of the Blueprint preloader (R31).
### R29  'Famolus' logo reveal
- **Family:** Logo reveal / mark construction (gather) | 2.5s | 1180x872 | finished by 1.5s | palette #1b20f4 white
- **Look:** Electric blue ground, white rounded strokes.
- **Motion:** Loose strokes and dots orbit and spiral inward, then lock into the letterforms of the wordmark in under a second and a half; a short hold.
- **Sound:** silent recording.
- **Steal:** Gathering stray strokes into letters; speed as character. The source of the orbiting strokes in the Ink preloader (R30).
### R30  Studio preloader 'Ink' (shipped)
- **Family:** Logo reveal / mark construction (draw and gather) | 5.3s | 1080x1080 | 3 change events, hold 2.0s | palette #f7f6f2 #0d0d67, orange accent
- **Look:** Paper (#f9f7f4) and navy ink; orange only for the cursor and the nib.
- **Motion:** The cursor blinks; four ink strokes orbit in and shrink to dots that become the hand's fingertips; the hand reaches in and draws the C (top arc clockwise, bottom anticlockwise 60 ms behind); the cursor squashes into the nib with one ring; the mark slides aside and the name is typed at 34 ms a letter; hold; the lockup leaves in 240 ms and the sheet lifts on a bowed edge.
- **Sound (measured on the recording):** -14.0 LUFS, bright UI ticks (centroid 3.5 kHz)
- **Steal:** The full choreography in `reference-implementations/wdc-preloaders/`.
### R31  Studio preloader 'Blueprint' (shipped)
- **Family:** Logo reveal / mark construction (construct) | 5.5s | 1080x1080 | 4 change events, hold 1.8s | palette #010165 white, orange accent
- **Look:** Brand navy, hairline guides a few shades up, the mark in white, a mute (#9d9ec9) for trails and the name's first state.
- **Motion:** Axes draw out from the centre; construction circles draw from twelve o'clock; anchors pop where guides cross; the arcs swing 150 degrees round the centre with trails; the hand slides along the axis; fingertips drop like rivets; the cursor falls down the vertical axis, squashes and becomes the nib; guides leave outward; the mark turns once as it settles; the name rises in mute and turns white letter by letter; the halves part.
- **Sound (measured on the recording):** -14.1 LUFS, bright (centroid 4.0 kHz)
- **Steal:** Construction as a story; guides that leave the frame rather than fade.
### R32  'Ink' page curtain, desktop (earlier draft)
- **Family:** Page curtain | 2.7s | 1918x1196 | palette #f7f6f2 navy
- **Motion:** The short construction between pages, built in about one second, the name typed beside the mark.
- **Note:** This recording still shows the orange cursor riding the typed name. It was removed before approval: the cursor's job ends when it becomes the nib.
### R33  'Blueprint' page curtain, desktop
- **Family:** Page curtain | 3.0s | 1918x1202 | palette #020065 white
- **Motion:** Guides, arcs and rivets at speed, the name rising under the mark, the halves parting onto the next page.

## Reading the sound numbers
- **Loud and hooky** (about -7 to -11 LUFS, 3-4 onsets/s): R14, R21, R20, R02, R19, R04. Social-first, drum-forward, effects stacked on every beat.
- **Mid** (about -12 to -15): R01, R08, R05, R09, R11, R13. Clean pop of UI sound over a steady bed.
- **Quiet and wide** (about -17 to -20 LUFS, big range): R03, R06, R16, R25. Ambient bed, few effects, long breaths; read as premium.
- **Ambient but loud, with a huge dynamic swing** (R23 Spotify: -10.7 LUFS, ~27 dB swing, 0.4 onsets/s): almost no rhythm, then a big swell. Think `dreamy-glass`.
- Brightness 570 Hz to 2.7 kHz: lowest (R24, R25) are warm/muffled beds; highest (R17, R10, R12) are glassy and bright.
- Choose the palette (`sound.py --palette`) from this, not from habit. See `craft/sound.md`.

## Gaps to flag to the client
- **3D scenes (R09, R22 chrome mark):** the engine does CSS 3D (cards, phones, planes), not modelled objects. Ask for a rendered 3D asset or approve a three.js/Blender step.
- **Photoreal scenery (R12):** needs licensed or client-supplied photos.
- **Hand-drawn / illustrated characters (R02 portraits, R06 stickers):** need the client's art or an illustration direction.
