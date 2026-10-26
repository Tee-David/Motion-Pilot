# Composition, depth and the camera

## Safe areas

| Format | Keep everything inside | Words inside |
| --- | --- | --- |
| 16:9 (1920 × 1080) | 5% action-safe margin | 10% title-safe margin |
| 9:16 (1080 × 1920) | 8% side margins | Between 168 px and 1330 px from the top; nothing under the right-hand action rail; below 1330 px only texture |
| 1:1 (1080 × 1080) | 6% margin | 10% margin |
| 4:5 (1080 × 1350) | 6% margin | Clear of the bottom 15% on feeds that overlay captions |
| Website hero | Where the page's own headline and buttons sit, nothing busy | No headline-size type in the video; the page supplies it |

Recompose for each format; never crop 16:9 into 9:16. On 16:9 a feature beat often reads left-aligned text with the object on the right; on 9:16 the same beat stacks, text above the object.

## The frame

- **The hero fills at least 40%** of the frame's width or height. Push in, crop, or give a small object a world.
- **One focal point per moment.** Contrast of value, size, motion and colour decides it. Two things moving with equal weight split the eye.
- **Centred is a choice.** Hooks, logo lockups and calls to action centre. Everything centred, all the time, is a tell.
- **Fill with intent.** Empty space is fine when it frames the hero; a dark void with small things floating in it is not a composition.
- **Keep the 1/3 rule for travel.** Nothing travels more than about a third of the frame in one move without a change of direction or a cut. With three or more elements, no more than a third of them move at once.

## Depth

Build three planes: ground, subject, foreground accents. Move them at different rates for parallax (ground 0.3×, subject 1×, foreground 1.3×). Give anything that sits on a surface a contact shadow. Keep one light direction for the whole film: a key from the upper left, a soft rim from behind on dark grounds.

CSS 3D carries planes well: phones, cards, browser windows, rings. A phone presented as an object may yaw and pitch (about -14° and 6°) with a slow sway; keep yaw under about 15° whenever its screen text must be read. Modelled objects (a 3D coin, a product) need real renders with alpha, or an honest 2D alternative.

## The camera

- **Push in** 1.0 → 1.08 over a shot for slow emphasis; a **punch-in** to 1.6 to 2× on one control of a UI, 400 to 600 ms with blur, then hold while it acts.
- **Pull back** to reveal that the result was playing inside the product.
- **Counter-motion:** when the hero moves right, let the ground drift left at 20 to 30% of its speed.
- **Follow the action:** the camera arrives at the control before the cursor clicks it, never after.
- The camera is a wrapper. Move the wrapper; never animate the same property on a parent and its child to fake one move.

## Grounds

- Change the ground between worlds (dark, light, brand colour) and always through a cause (`craft/transitions.md`).
- Every piece has a light and a dark version. On paper, ink, solid fills and real shadows; on dark, white and rim light. Additive glow disappears on a light ground and turns muddy in compression.
- Pieces that hand off to each other (a reel of loops, a hero that cycles pieces) share one ground, so the hand-off never flashes.
- Full-screen linear gradients on dark grounds band under H.264: use a radial gradient, a solid, or a solid with a local glow, and grain at 4 to 7%.
- An accent at 5% opacity vanishes in compression: 15 to 25% for atmosphere, full strength for the focal element.

## Hero video and page text

When a film plays behind a website's copy, the film is the ground and the page owns the words. Keep the film's action out of the copy zone (the right half on desktop, the top third on a phone), keep headline-size type out of the film, and design a light version that needs no veil or shade over it. If a shade is needed for contrast, hang it off the copy block rather than percentages of the screen, so the text keeps its contrast at every height.
