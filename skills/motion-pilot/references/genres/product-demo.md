# Product demos and feature films

What people share is real output in a real product. Everything that claims to be the product is the product; one invented button loses everyone who uses it.

## Real screens, never a mockup

1. Get them in this order: the client's recordings or screenshots (ask, naming the screen each beat needs); design files rebuilt as states of one app so the change between two frames is a real click; walking the flow yourself where no sign-in is needed; the feature's own page.
2. A missing screen is a labelled placeholder, said in the reply, or a faithful recreation labelled as recreated. A phone shows an app, not a website; a product is not repeated across three phones.
3. Logos, icons and fonts are the brand's own files.

## The product on screen

- Rebuild only the piece the beat uses (the panel, the field, the row that changes) and show it at 1.6 to 2× its real size; text stays at least 26 px at 1080 after any push. Never a small window in the middle of an empty canvas.
- The camera cycles between the window on its ground, one pane, and a punch-in on one control. Moves take 400 to 600 ms with blur, arrive at the control before the cursor, then hold while the UI acts.
- Containers morph instead of cutting: the button becomes the menu, the message becomes the bubble.
- Pull back to reveal the result playing inside the product, or zoom through the player until the result fills the frame.
- Hold one framing 7 to 10 s while the interface acts; the process runs fast, the payoff plays at normal speed.
- In each verb beat keep only what the cursor touches and what proves the line; remove the rest of the screen.

## Moves for demos

| Move | Recipe |
| --- | --- |
| **Pointer click** | `C.pointer`: a big cursor (4 to 7% of the frame) enters from off screen, eases to the target both ways, presses to scale 0.86, and the UI changes on the click frame. A ripple ring only if the brand's UI has one. |
| **Notification toast** | A card drops in from above on a gentle overshoot, holds about 1.2 s, exits upward faster. Pair with a `notify` cue. |
| **Typing into a field** | Real text, 30 to 45 ms a character, the cursor solid while typing; the field grows if the real one does. As a story step, never as the opening shot alone. |
| **Prompt to result** | A prompt bar types, the pointer sends, the result card scales in from 0.9 with a soft shadow. |
| **Counter** | A real number rolls up over 1.2 to 1.6 s and holds; its label arrives 50 ms after. |
| **Phone as an object** | `C.phone` with the real app screen; yaw about -14°, pitch about 6°, a slow sway of a degree or two; it enters from depth on a gentle overshoot. Keep yaw under 15° while text is read. |
| **Card fan** | Three cards offset about 0.6 of a card's width, rotated ±9°, arriving 100 ms apart on a gentle overshoot. |
| **Chapter bar** | `C.progress`: a segmented bar that fills with the beats, matching a website's chapter UI when the film is a hero. |

## Shape

Usually 20 to 45 s: the beats in `process/storylines.md` §4, with the proof beat as three to six verbs ("paste, pick, watch it build, ship"), one each. A walkthrough of every feature is a manual, not a film: pick the one task that proves the one thing.

## Tells

Typing into a prompt box as the opener; three feature cards; a title over a dimmed screenshot; an invented dashboard; UI tilted so far its text cannot be read; the logo docked in a corner.
