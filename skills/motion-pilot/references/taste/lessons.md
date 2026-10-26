# Lessons from approved work

Every rule in this skill that sounds oddly specific came from a piece that was corrected before it was approved. Each lesson below records what happened, the assumption that caused it, and the rule that prevents it, so it is paid for once. Add a lesson whenever a correction would change how the next piece is made.

Format: **What happened** · **Why** (the wrong assumption or root cause) · **Rule**.

## Story and look

**A construction that only spun.** An early loader rotated the mark. · A spinner says "wait"; it says nothing about the brand. · **Build the mark from its own parts and land on the exact header lockup.** The parts are the story.

**Two openings back to back.** A homepage intro played, then a preloader played over it. · Each was designed alone. · **One full-screen opening per visit.** The second stands down when another has claimed the visit.

**The hook broke onto two lines.** A typed hook wrapped on narrow frames and its size changed between phrases. · Each phrase was fitted on its own. · **Fit the longest phrase, use one size for the set, keep hooks on one line and centred.**

**Website pages inside phones.** A phone mockup showed a responsive website. · Any screen seemed to prove the point. · **Phones show apps.** Recreate the app at the phone's ratio if needed and label it; never repeat one product across several phones.

**Glow in the corners.** Orange light bloomed at the frame's corners for atmosphere. · Glow was standing in for an idea, and the accent lost its meaning. · **One accent event per beat; no coloured glow as decoration.**

**Additive light vanished on paper.** The light versions of ten hero pieces reused the dark versions' glow, scan lines and light trails, which disappeared on a pale ground. · Light and dark were treated as a palette swap. · **Design the light ground as its own medium:** ink lines, solid fills, real shadows, a hairline edge so a finished page does not melt into the ground.

**A hero moment seen edge-on.** A ribbon of cards picked a random post to pop, which was sometimes side-on to the camera. · The pick ignored the camera. · **The hero moment always faces the camera, near the middle of the frame.**

**Things left the stage.** A 3D lattice ran off the frame at some pointer angles and screen sizes. · It was framed for one size and one angle. · **Measure the extent over every angle and size the piece can reach and fit once per size.**

**Seams that cut.** A loop jumped from its last frame to its first. · The loop was cut, not designed. · **End loops on a hold that returns to the first pose;** pieces that hand off share one ground.

**Translucent text failed contrast.** A definition line in translucent lilac passed on one ground and failed on the other. · Opacity was used as a colour. · **Text uses a solid colour that passes 4.5:1 on its ground in both themes.**

**A lavender frame at a cut.** A navy ground crossfaded into a royal blue one and the midpoint frames came out lavender. · An opacity blend of two saturated colours was assumed to stay on brand. · **Never crossfade two saturated grounds.** Cut, wipe with a shape, or carry one object across, and check the midpoint frame.

## Choreography

**The cursor rode the typed name.** After it became the nib, an orange cursor bar kept following the letters of the name. · The cursor was treated as a typing effect rather than a character. · **A character's job ends when its story ends.** The cursor becomes the nib, and the name types clean.

**An orange seam where the sheet parted.** The two halves of a blueprint sheet parted along an orange line. · Accent was added to make the moment feel designed. · **The accent is spent once per piece;** the parting is enough.

**The turning mark swept across the name.** The name began rising while the mark was still turning into place, and the mark passed over the first letters. · The name was timed to the start of the settle, not its end. · **The name waits until the mark has all but stopped moving.**

**A curtain read as a blob on phones.** A rising sheet's bowed leading edge was a dome a third of the screen's width tall on a phone. · The curve was sized to the viewport height alone. · **Size curves against the shorter side** (`min(20vh, 32vw)`) and check them at 390 px.

**Two motions crossing read as a corner.** On a phone, the menu slid away sideways while the curtain rose from the bottom, and the pair read as something arriving from a corner. · Each motion was right alone. · **One motion at a time on a phone:** the menu holds still under the curtain, and the curtain drops from the top and lifts back the way it came, like a blind.

**A ring sat behind the cursor from frame one.** A ring that was meant to burst at 1.5 s was visible from the start. · `animation-fill-mode: both` holds the first keyframe through the delay. · **Make the 0% keyframe invisible** and start the real motion at 1%.

**A dashed ring drew as a solid ring.** A trail drawn with `vector-effect: non-scaling-stroke` rendered its whole circle in one engine. · The property interacts with dash arrays differently across engines. · **Use non-scaling strokes for straight guides only;** give dashed rings a scaling stroke sized in viewBox units.

**The mark was sliced on the left.** The mark's box was sized by hand and `width: auto` did not resolve inside the flex row, so `overflow: hidden` clipped it. · Sizes were set separately. · **Derive every size from one number.**

## Web motion in production

**The preloader painted on the next page.** A grey line appeared across a ticker on first load. It was the preloader's own progress bar, still drawing while the overlay faded over 450 ms. Two wrong fixes were tried first on an unconfirmed diagnosis. · The cause was assumed, not measured. · **Measure before fixing** (sample the overlay's opacity and the element's at each frame) and clear secondary elements in about 120 ms when their parent starts to leave.

**The hero dipped to grey between images.** Remounting each new backdrop meant the incoming one faded in over nothing. · A fade was assumed to be a crossfade. · **Hold the outgoing frame underneath until the new one covers it.**

**The film looked paused on arrival.** The hero's button said Play until the video had been fetched after the whole page loaded. · Button state followed the network, not intent. · **Show Pause from the first paint**; say Play only when the visitor paused, the browser refused, or they asked for less motion or data. Start the film at load or two seconds after hydration, whichever comes first.

**A still with a play button on iPhones.** Low Power Mode rejected autoplay. · Autoplay was assumed to work when muted. · **Treat the first tap, key or click as permission** and try again, unless the visitor paused it themselves.

**A performance pass switched the intro off on phones.** A width check added for a speed score disabled the intro and preloader below 768 px. · Gating rules were changed without checking what they gated. · **Test motion gates at phone width** after any performance change.

**Confetti froze on one browser.** Keyframes that read custom properties ran on the main thread and stuttered. · Custom properties were assumed to be free. · **Animate plain values with the Web Animations API** and remove each piece when it lands.

**The overlay dropped onto content already being read.** The decision to show a preloader ran in an effect after the first paint. · Client-side code was trusted with a first-paint decision. · **Decide in an inline head script before paint** and let CSS show the overlay only when told.
