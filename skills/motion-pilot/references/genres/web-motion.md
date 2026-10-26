# Web motion: preloaders, page curtains, hero motion and UI

Motion on a website is watched by people who came to do something else. It earns its place by explaining what changed, by giving a wait a shape, or by making the brand's one gesture memorable, and it never stands between a person and the page. The craft is the same as in film; the rules are stricter.

## The rules that keep it polite

1. **Never block.** A first-load preloader has `pointer-events: none` and no scroll lock: the page under it is live and scrollable from the first frame, so anyone who knows the site scrolls straight through. A page curtain between pages may take clicks for the second it is up, so a second click cannot land on a page that is leaving.
2. **The frequency gate.** The more often something plays, the less it may animate. A once-per-visit preloader may take three to five seconds. A page curtain, played on every navigation, builds in about one second. A control used dozens of times a day changes instantly. Anything triggered from the keyboard never animates.
3. **Once per visit.** A first-load preloader plays once per session or within a window (for example 30 minutes), not on every page. A second full-screen opening right after another one (an intro and then a preloader) is one too many: the second stands down.
4. **Decide before first paint.** Whether the overlay plays depends on browser-only facts (session storage, the motion preference, whether another opening has claimed the visit). Decide them in a tiny inline script in the head that writes a data attribute on the root element, and let CSS show the overlay only when it says play. Deciding in an effect lets the page paint first and drops the overlay onto content the reader has begun. Server and client render the same markup.
5. **Nothing under reduced motion.** `@media (prefers-reduced-motion: reduce)` removes the overlay entirely, stops loops and replaces arrivals with the final state. A fade is acceptable for a state change; a construction is not.
6. **Transform and opacity.** Animate only `transform` and `opacity`, with the drawing itself (`stroke-dashoffset`, `stroke-dasharray` on a few paths in one small SVG) as the only exception. Never animate layout properties.
7. **Pause what nobody sees.** Loops stop off screen and in a hidden tab. `content-visibility: auto` stops a pure-CSS loop off screen; an intersection observer stops one the component already watches.
8. **Mobile is native.** No smooth-scroll interception, custom cursors or scroll writers on touch devices. One owner for scroll position; a curtain that lands the reader at the top of the next page must be the only thing that moves the scroll.
9. **The page owns its chrome.** While a curtain or preloader owns the screen, floating buttons (chat, accessibility, back to top) step out, and come back when it leaves.
10. **Exits answer entrances, in context.** On a phone, a curtain that meets a menu sliding sideways reads as something arriving from a corner. Keep the menu still under the curtain, and let the curtain enter and leave on the same edge.

## Preloader anatomy

Three phases, switched by the component; the choreography lives in CSS with delays, so the first load can start before any JavaScript runs.

| Phase | What happens |
| --- | --- |
| `enter` | The construction plays (see `craft/logo-construction.md`): 2 to 3 s to a built lockup. |
| `wait` | Only if the page is still not ready: a small idle that reads as working (parts tapping in turn like a typing indicator), never a spinner. |
| `leave` | The lockup leaves first and fast (about 240 ms, `.4,0,1,1`), then the ground leaves (a sheet lifts on a bowed edge, halves part) over 600 to 700 ms on `.77,0,.18,1`. |

Write every timing in the stylesheet in milliseconds from the start of its phase, as a beat sheet in a comment at the top. Repeat only the numbers the component needs (when to leave, when the curtain has closed, when the build is done) in one constant in code, with a comment pointing back.

**The `both` fill trap.** `animation-fill-mode: both` holds the first keyframe through the delay. A ring that starts at full opacity sits behind the cursor from the first frame; make its 0% keyframe invisible and its 1% keyframe the real start.

**One number sizes it.** Derive the mark, the gap and the wordmark from one custom property clamped to the viewport (`clamp(66px, 13vmin, 120px)`), and reserve the wordmark's width for the widest fallback font.

**Both themes.** Light: the brand's paper and ink. Dark: a lifted night and white ink, still a distinct sheet against the dark page.

## Page curtains

The same construction, short, between pages:

- The ground closes over the leaving page (480 to 520 ms).
- The mark builds while the next page loads (about 1 s to built), with the next page's name in a small label under it (typed at about 20 ms a letter, or rising).
- If the page is not ready, the idle plays. When it is, the curtain leaves onto the top of the next page.
- Same-page links, dashboards and reduced motion get no curtain.

## Arrival choreography for app screens

When a dashboard or app screen loads: the head, then each block, a beat apart (60 to 80 ms), rising a few pixels and fading in on the arrival curve. Figures count up over about one second, bars grow from the baseline, timelines and steppers draw on. Transform and opacity only, `backwards` fill so nothing is left behind, nothing under reduced motion, and the server always renders the real figure, so without JavaScript the number is simply there and screen readers hear it once.

Exits play before the element leaves (about 200 ms): sheets slide out, menus shrink toward their button, toasts drop.

## Controls

| State | Motion |
| --- | --- |
| Hover (pointer devices only) | 120 to 200 ms colour or lift; never the only way to see information |
| Press | 80 to 150 ms, scale 0.97 to 0.98 or 1 px down |
| Focus-visible | Instant ring; no animation on the ring itself |
| Loading | The button keeps its size; a progress element inside it, a message after a few seconds ("Still opening the payment window. Nothing has been charged yet.") |
| Success | A short draw of a tick, the label changes to the past tense of the action |

One celebratory moment is allowed where it means something (a payment completing, a deck cleared): confetti of 40 to 70 pieces in the brand palette for about three seconds, removed when the last piece lands, never under reduced motion.

## Hero motion on a page

See `genres/hero-loop.md` for the film itself. On the page: the poster is the first paint and the LCP; the video attaches after load when the browser is idle, picks the wide or tall cut by orientation, never loads under reduced motion or Save-Data, pauses off screen and in a hidden tab, and starts on the first tap when a browser refuses autoplay. The pause control shows "Pause" from the first paint.

## Building and checking

- Prototype the choreography in the engine or in a single HTML page with the real SVG, then port it to CSS keyframes: each engine segment becomes an animation with a duration, a delay and the same bezier.
- Drive it with Playwright: record the overlay at 60 fps, and assert the behaviour, not only the look: scrolling during the overlay moves the page; a second route in the same session skips the preloader; reduced motion shows nothing; the overlay unmounts.
- Run `scripts/review.py` on the recording for the sheets and the holds, on both themes and at 390 px and 1440 px.
- Capture gallery thumbnails with a committed script, never by hand.

## Worked example

`reference-implementations/wdc-preloaders/` is a shipped pair of preloaders and page curtains (Ink and Blueprint) with the full stylesheet, the beat sheets and the reasoning, including the corrections made before approval.
