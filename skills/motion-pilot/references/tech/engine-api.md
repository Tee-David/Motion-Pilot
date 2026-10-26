# Engine API (engine/motion.js + engine/components.js)

**Core rule:** `M.render(t, frame, rt)` must be a pure function of time. No CSS animations, no timers, no state carried between frames. That makes any frame renderable alone, chunks resumable, and splices safe.

## Project anatomy (made by `new_project.py`)
`index.html` loads `engine/motion.js`, `engine/components.js`, `tokens.js` (palette + fonts from the chosen style), `project.js` (your scenes). Open in a browser with `?w=1920&h=1080&theme=dark` to scrub by calling `M.render(t)` in the console.

## Globals
`M.W M.H M.V(portrait?) M.T(tokens for theme) M.F(fonts) M.RT(real output time) M.cfg{bg,grain,fonts}`

## Easing & helpers
`M.P(t,a,b)` progress 0..1 · `M.lerp` · `M.clamp` · `M.eo eo5 ei eio xo xi xio back spring` · `M.rnd(i)` deterministic noise · `M.blink()` real-time cursor blink · `M.typed(str,t,t0,dt)`.

**Curves shared with the web.** `M.bez(x1,y1,x2,y2)` turns any CSS cubic-bezier into an easing function, so a film and a site use the same curve. `M.ease.arrive exit travel sheet fall pop reach rivet orbit sine` are the named curves from `craft/timing-and-easing.md`. `M.seg(t,t0,dur,ease)` is the eased progress of one move (the building block of every choreography). `M.springD(x,damping)` is a closed-form spring named by damping ratio. `M.pscale(a,b,p)` interpolates scale in log space for zooms. `M.poster(t,step,fps)` holds every n-th frame for a stepped, hand-made look.

```js
// a mark part that reaches in with overshoot, 900 ms in, over 420 ms
const k = M.seg(lt, .90, .42, M.ease.reach);
M.tf(hand, {x: (1-k)*-160, y: (1-k)*40, rz: (1-k)*-10, o: M.P(lt,.90,.90+.42*.35)});
```
`M.swap(pin,pout,{dist,blur})` → `{dy,b,o}`; spread into `tf`. `pin=1` means fully entered (passing 0 hides the element).

## DOM
`M.el(parent,css,html,tag)` · `M.tf(el,{x,y,dy,z,rx,ry,rz,s,sx,sy,o,b,br,origin,zi})` · `M.measure(html,css)` width · `M.fit(html,css,maxW,size)` largest size that fits · `M.words(el,text)` / `M.letters(el,text)` return spans for per-word / per-letter animation.

## Scenes and cues
```js
M.scene('name', t0, t1, { pad:.3, z:5,
  build(root, ctx){ /* create elements once */ },
  update(lt, t, ctx, root){ /* lt = t - t0; set styles from lt only */ } });
M.cue(t,'impact',{gain:.8,pan:-.3});  M.cueTyping(t0,n,dt);
```
Times are **source seconds** (the animation's own clock). A time map (see `craft/voice.md`) converts output time to source time, and `sound.py` maps cues through it.
Cue types: `type tick click swap pop whoosh riser impact hit ding success notify swipe`.

## Components (`C.*`)
`bg` (gradient + drifting blobs) · `text` · `pill` (label/icon/dot) · `card` · `phone` (w, img|html; design UIs at 286x626 CSS px, scale with `(w-24)/286`) · `browser` (scrolling page image) · `pointer` (mouse arrow + click ripple) · `bar` (typing cursor) · `progress` (segmented chapter bar) · `orbit` (3D ellipse of items with depth blur) · `flood` (circular colour reveal) · `confetti` · `logoParts` (assemble an SVG from pieces).

## Patterns
- **Centered rotating phrase:** measure every variant with `M.measure`, `M.fit` to the widest, position each row from its *full* width so typing never shifts, and animate the row's x while the old phrase fades.
- **Reveal circle:** `root.style.clipPath='circle(r at x y)'` with `xio`; add a ring `div` the same radius for the orange edge.
- **Time-sync a count-up:** `Math.round(n*M.eo(M.P(lt,a,b)))`.
- **Phone with real app screen:** `C.phone(root,{w,img:'assets/app.png',bg:'#...'})` keeps a status strip; for recreated UIs pass `html`.
- **Fonts inside HTML strings:** use `font-family:'Name'` with single quotes (double quotes break `style=""`).

## Rendering
`render.py PROJECT --w 1920 --h 1080 --dur 9 --out out.mp4` (add `--sub 2` motion blur, `--timemap map.json`, `--audio mix.wav`, `--theme light`). `--sheet 0.5,2,4 --sheet-out s.jpg` for a fast contact sheet (always do this first). Parts cache in `.parts/` and resume.
