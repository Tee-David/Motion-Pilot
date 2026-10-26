"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect, useId, useRef, useState, useSyncExternalStore } from "react";
import { ACCENT_PATHS, INK_PATHS } from "@/components/brand/logo-paths";
import "./preloader.css";

/**
 * The preloader, and the curtain between pages.
 *
 * ONE COMPONENT, TWO JOBS. On a first visit (or one more than thirty minutes
 * after the last) the full piece plays over the page: the mark is built in
 * front of the reader and lands in the lockup they will see in the header.
 * After that, every move between the public pages goes through a short cut
 * of the same piece: the curtain closes, the mark builds while the next page
 * loads behind it, and the curtain opens on the new page. Same pieces, same
 * order, so the transition reads as the preloader remembering itself rather
 * than as a second animation.
 *
 * TWO CONCEPTS, CHOSEN BEFORE FIRST PAINT. `data-loader` on <html> ("ink" or
 * "blueprint") is set by the pre-paint script in app/layout.tsx, from
 * `?loader=` or the last choice remembered there. Both first-load overlays are
 * in the server HTML and the CSS shows the chosen one, because the server
 * cannot know which one this browser wants and a swap after hydration would
 * show the wrong one first. The path data is written once (the hidden <defs>
 * below) and each concept places it with <use>.
 *
 *   Ink (after the famolus reference): the orange cursor blinks; four ink
 *   strokes orbit in and shrink to dots, and the dots are the hand's
 *   fingertips; the hand reaches in and draws the C out of itself, top arc
 *   one way and bottom arc the other; the cursor squashes into the nib; the
 *   name is typed. The sheet lifts away on a curved edge.
 *
 *   Blueprint (after the KANTIV reference): the mark is constructed on
 *   hairline guides, turns once into the lockup, and the sheet parts down
 *   the middle. See `Blueprint`.
 *
 * WHAT IT NEVER DOES. It never plays under reduced motion, on the admin, the
 * portal or the account and payment pages, or for a link to the page you are
 * on. It never holds the next page back: the curtain opens as soon as the
 * page has arrived and the mark has finished, whichever is later. The first
 * load is `pointer-events: none` and does not lock scrolling, as before.
 */

type Concept = "ink" | "blueprint";
type Phase = "enter" | "wait" | "leave";

/* Every number here is mirrored in preloader.css, where the choreography that
   these phases switch between is written out. Change one, change both. */
const TIMES: Record<Concept, { load: number; loadExit: number; cover: number; built: number; exit: number }> = {
  /* load: when the full piece starts to leave. cover: when the curtain has
     closed and the router may swap the page. built: when the short build has
     finished. exit: how long leaving takes. */
  ink: { load: 2760, loadExit: 680, cover: 520, built: 900, exit: 640 },
  blueprint: { load: 3000, loadExit: 780, cover: 460, built: 960, exit: 760 },
};

/* The public pages the curtain runs between, and what it calls them. The words
   are the header's own, so the label under the mark is the link you pressed.
   Anything not listed (the dashboards, sign-in, documents, forms) navigates
   as it always has. */
const NAMES: Record<string, string> = {
  "": "Home",
  work: "Our Works",
  services: "Services",
  blog: "Blog",
  about: "About Us",
  contact: "Contact Us",
  start: "Start a project",
  meet: "Schedule a meeting",
  tools: "Free tools",
  policies: "Policies",
};
const section = (path: string) => path.split("/")[1] ?? "";
const isPublic = (path: string) => Object.prototype.hasOwnProperty.call(NAMES, section(path));

const noSubscribe = () => () => {};
/* Read once: the pre-paint script decided, and nothing changes it until this
   component says the load piece is over. */
const readPreload = () => document.documentElement.dataset.preload === "play";
const readConcept = (): Concept =>
  document.documentElement.dataset.loader === "blueprint" ? "blueprint" : "ink";

interface Run {
  id: number;
  concept: Concept;
  label: string;
  phase: Phase;
}

export default function Preloader() {
  const router = useRouter();
  const path = usePathname();

  /* THE FIRST LOAD. The server renders the overlay (true), and the client
     agrees only when the pre-paint script said "play"; otherwise it unmounts
     an overlay the CSS never showed. */
  const playLoad = useSyncExternalStore(noSubscribe, readPreload, () => true);
  const [load, setLoad] = useState<"on" | "leaving" | "off">("on");

  useEffect(() => {
    if (!playLoad) return;
    const t = TIMES[readConcept()];
    const leave = window.setTimeout(() => setLoad("leaving"), t.load);
    const done = window.setTimeout(() => {
      setLoad("off");
      /* Hands the floating chrome back (globals.css hides it while this says
         "play") and keeps a later remount from replaying. */
      document.documentElement.dataset.preload = "done";
    }, t.load + t.loadExit);
    return () => {
      window.clearTimeout(leave);
      window.clearTimeout(done);
    };
  }, [playLoad]);

  /* BETWEEN PAGES. Refs for everything the click handler and the path effect
     share, so neither has to be re-registered as the run moves along. */
  const [run, setRun] = useState<Run | null>(null);
  const busy = useRef(false);
  const from = useRef("");
  const arrived = useRef(false);
  const built = useRef(false);
  const leaving = useRef(false);
  const timers = useRef<number[]>([]);
  const seq = useRef(0);
  /* `open` lives inside the effect below; the path effect reaches it here. */
  const openRef = useRef<() => void>(() => {});

  useEffect(() => {
    const later = (fn: () => void, ms: number) => timers.current.push(window.setTimeout(fn, ms));

    const finish = () => {
      for (const id of timers.current) window.clearTimeout(id);
      timers.current = [];
      busy.current = false;
      leaving.current = false;
      delete document.documentElement.dataset.curtain;
      setRun(null);
    };

    /* Opens the curtain once BOTH are true: the new page has rendered, and the
       mark has finished building. Two frames first, so the page has painted
       under the curtain before the curtain moves; otherwise the first frames
       of the reveal can show the old page. */
    const open = () => {
      if (leaving.current || !arrived.current || !built.current) return;
      leaving.current = true;
      requestAnimationFrame(() =>
        requestAnimationFrame(() => {
          setRun((r) => (r ? { ...r, phase: "leave" } : r));
          later(finish, TIMES[readConcept()].exit);
        }),
      );
    };
    openRef.current = open;

    const start = (url: URL) => {
      const concept = readConcept();
      const t = TIMES[concept];
      busy.current = true;
      arrived.current = false;
      built.current = false;
      leaving.current = false;
      from.current = window.location.pathname;
      document.documentElement.dataset.curtain = concept;
      const href = url.pathname + url.search + url.hash;
      /* Start fetching now; the swap itself waits for the curtain. */
      router.prefetch(href);
      setLoad("off");
      setRun({ id: ++seq.current, concept, label: NAMES[section(url.pathname)] ?? "", phase: "enter" });
      later(() => router.push(href), t.cover);
      later(() => {
        built.current = true;
        /* The page is not here yet: the fingertips keep tapping, like a
           typing indicator, until it is. */
        if (!arrived.current) setRun((r) => (r ? { ...r, phase: "wait" } : r));
        open();
      }, t.built);
      /* Fail open. A navigation that never commits (a network error, a
         redirect off the site) must not leave the reader behind a curtain. */
      later(() => {
        arrived.current = true;
        built.current = true;
        open();
      }, 10000);
    };

    const onClick = (e: MouseEvent) => {
      if (e.defaultPrevented || e.button !== 0) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = (e.target as Element | null)?.closest?.("a[href]") as HTMLAnchorElement | null;
      if (!a || (a.target && a.target !== "_self") || a.hasAttribute("download")) return;
      /* Links that already run their own transition or open something in
         place (the film-strip menu, the live-site previews) say so. */
      if (a.closest("[data-no-curtain]")) return;
      let url: URL;
      try {
        url = new URL(a.href, window.location.href);
      } catch {
        return;
      }
      if (url.origin !== window.location.origin) return;
      if (!isPublic(window.location.pathname) || !isPublic(url.pathname)) return;
      /* Same page: ScrollReset's job, not a transition. */
      if (url.pathname === window.location.pathname) return;
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      e.preventDefault();
      /* Mid-transition clicks are swallowed rather than queued: the reader
         has already chosen where they are going. */
      if (busy.current) return;
      start(url);
    };

    /* A page restored from the back-forward cache comes back exactly as it
       was left, curtain included. */
    const onShow = (e: PageTransitionEvent) => {
      if (e.persisted) finish();
    };

    document.addEventListener("click", onClick, true);
    window.addEventListener("pageshow", onShow);
    return () => {
      document.removeEventListener("click", onClick, true);
      window.removeEventListener("pageshow", onShow);
      for (const id of timers.current) window.clearTimeout(id);
    };
  }, [router]);

  /* The new page has committed. `from` rather than the target, because a
     redirect lands somewhere else and that still counts as arriving. */
  useEffect(() => {
    if (!busy.current || path === from.current) return;
    arrived.current = true;
    openRef.current();
  }, [path]);

  return (
    <>
      <MarkDefs />
      {playLoad && load !== "off" ? (
        <>
          <Ink mode="load" phase={load === "leaving" ? "leave" : "enter"} />
          <Blueprint mode="load" phase={load === "leaving" ? "leave" : "enter"} />
        </>
      ) : null}
      {run ? (
        run.concept === "ink" ? (
          <Ink key={run.id} mode="route" phase={run.phase} label={run.label} />
        ) : (
          <Blueprint key={run.id} mode="route" phase={run.phase} label={run.label} />
        )
      ) : null}
    </>
  );
}

/* ---------------------------------------------------------------------------
   The mark's pieces, once. Ids are prefixed so nothing else on the page can
   collide with them. Fingertips are numbered top to bottom.
   ------------------------------------------------------------------------- */
const PIECES: [string, string][] = [
  ["top", INK_PATHS[0]],
  ["palm", INK_PATHS[1]],
  ["f1", INK_PATHS[2]],
  ["f2", INK_PATHS[3]],
  ["thumb", INK_PATHS[4]],
  ["f3", INK_PATHS[5]],
  ["f4", INK_PATHS[6]],
  ["bot", INK_PATHS[7]],
  ["nib", ACCENT_PATHS[0]],
  ["bar", ACCENT_PATHS[1]],
];

function MarkDefs() {
  return (
    <svg className="pl-defs" aria-hidden="true" focusable="false">
      <defs>
        {PIECES.map(([id, d]) => (
          <path key={id} id={`pl-${id}`} d={d} />
        ))}
      </defs>
    </svg>
  );
}

const use = (id: string, className: string) => <use href={`#pl-${id}`} className={className} />;

/* The wordmark, a letter at a time. Each letter knows its place in the line
   (`--i`) so the CSS can stagger it; the space is a real character so the
   caret travels across it like a typed one. */
const LINES = ["We Dig", "Creativity"];
function Word({ prefix }: { prefix: string }) {
  let i = 0;
  return (
    <span className={`${prefix}-word`}>
      {LINES.map((line) => (
        <span key={line} className={`${prefix}-line`}>
          {Array.from(line).map((ch) => (
            <span key={i} className={`${prefix}-ch`} style={{ "--i": i++ } as React.CSSProperties}>
              {ch}
            </span>
          ))}
        </span>
      ))}
    </span>
  );
}

function Label({ prefix, text }: { prefix: string; text: string }) {
  return text ? (
    <span className={`${prefix}-label`}>
      {Array.from(text).map((ch, i) => (
        <span key={i} className={`${prefix}-ch`} style={{ "--i": i } as React.CSSProperties}>
          {ch}
        </span>
      ))}
    </span>
  ) : null;
}

/* ---------------------------------------------------------------------------
   Concept 1: Ink.
   ------------------------------------------------------------------------- */

/* The C's geometry, fitted from the traced mark: centre (515, 459), outer
   radius 436, inner 235. The pen runs down the middle of the band (r 335),
   wide enough to cover it, from the hand outwards: the top arc clockwise from
   -165deg to -24deg, the bottom arc anticlockwise from 140deg to 26deg. Both
   run a little past the drawn ends so the round cap clears them. */
const ARC_TOP = "M191.4 372.3A335 335 0 0 1 821 322.7";
const ARC_BOT = "M258.4 674.3A335 335 0 0 0 816.1 605.9";
/* Each swirl stroke orbits on the radius of the fingertip it becomes, and the
   CSS ends its rotation at that fingertip's angle. */
const SWIRL = [429.3, 432.3, 458, 483.2];

function Ink({ mode, phase, label = "" }: { mode: "load" | "route"; phase: Phase; label?: string }) {
  const id = useId().replace(/:/g, "");
  return (
    <div className="pl pl-ink" data-mode={mode} data-phase={phase} aria-hidden="true">
      <div className="ink-sheet" />
      <div className="ink-stage">
        <div className="ink-lockup">
          <svg className="ink-mark" viewBox="0 0 904 944" focusable="false">
            <defs>
              <mask id={`${id}t`} maskUnits="userSpaceOnUse" x="-100" y="-100" width="1104" height="1144">
                <path className="ink-pen ink-pen--top" d={ARC_TOP} pathLength={1} />
              </mask>
              <mask id={`${id}b`} maskUnits="userSpaceOnUse" x="-100" y="-100" width="1104" height="1144">
                <path className="ink-pen ink-pen--bot" d={ARC_BOT} pathLength={1} />
              </mask>
            </defs>
            {mode === "load" ? (
              <g className="ink-swirl">
                {SWIRL.map((r, k) => (
                  <circle key={k} className={`ink-s ink-s--${k + 1}`} cx="515" cy="459" r={r} pathLength={1} />
                ))}
              </g>
            ) : null}
            <g className="ink-hand">
              {use("palm", "ink-palm")}
              {use("thumb", "ink-thumb")}
            </g>
            {use("f1", "ink-f ink-f--1")}
            {use("f2", "ink-f ink-f--2")}
            {use("f3", "ink-f ink-f--3")}
            {use("f4", "ink-f ink-f--4")}
            <g mask={`url(#${id}t)`}>{use("top", "ink-arc")}</g>
            <g mask={`url(#${id}b)`}>{use("bot", "ink-arc")}</g>
            <circle className="ink-ring" cx="525" cy="452" r="150" />
            {mode === "load" ? <rect className="ink-caret" x="508" y="352" width="34" height="206" rx="12" /> : null}
            {use("nib", "ink-nib")}
            {use("bar", "ink-bar")}
          </svg>
          {mode === "load" ? <Word prefix="ink" /> : null}
        </div>
        {mode === "route" ? <Label prefix="ink" text={label} /> : null}
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------------------
   Concept 2: Blueprint (after the KANTIV reference).

   The mark is constructed rather than drawn. Hairline axes and the C's two
   construction circles are set out first, with pen-tool anchors where they
   cross; the arcs swing into place round the centre, each with a faint trail
   behind it; the hand slides in along the horizontal axis and the fingertips
   drop like rivets; the cursor falls down the vertical axis onto the centre
   anchor and becomes the nib. The guides leave the frame, the mark turns
   once as it settles into the lockup, and the name rises out of a baseline
   in the brand's mute before it turns white. The sheet parts down the
   middle, top half up and bottom half down, the way the C opens.
   ------------------------------------------------------------------------- */

/* Axis lines run from the C's centre outwards, far enough to cross any
   screen at the smallest mark size (12000 units is about 1500px there). */
const AXES = ["M515 459H-11485", "M515 459H12515", "M515 459V-11541", "M515 459V12459"];
/* Where the axes cross the construction circles, and the centre itself,
   which is where the cursor lands. */
const ANCHORS: [number, number][] = [
  [515, 459],
  [79, 459], [951, 459], [515, 23], [515, 895],
  [280, 459], [750, 459], [515, 224], [515, 694],
];

function BpWord() {
  return (
    <span className="bp-word">
      <Word prefix="bpm" />
      <Word prefix="bpw" />
    </span>
  );
}

function Blueprint({ mode, phase, label = "" }: { mode: "load" | "route"; phase: Phase; label?: string }) {
  return (
    <div className="pl pl-bp" data-mode={mode} data-phase={phase} aria-hidden="true">
      <div className="bp-half bp-half--top" />
      <div className="bp-half bp-half--bot" />
      <div className="bp-stage">
        <div className="bp-lockup">
          <svg className="bp-mark" viewBox="0 0 904 944" focusable="false">
            <g className="bp-guides">
              {AXES.map((d, k) => (
                <path key={k} className={`bp-axis bp-axis--${k + 1}`} d={d} pathLength={1} />
              ))}
              {/* Circles start at twelve o'clock (the attribute rotation),
                  so both draw from the top, clockwise. */}
              <circle className="bp-circle bp-circle--outer" cx="515" cy="459" r="436" pathLength={1} transform="rotate(-90 515 459)" />
              <circle className="bp-circle bp-circle--inner" cx="515" cy="459" r="235" pathLength={1} transform="rotate(-90 515 459)" />
              {ANCHORS.map(([x, y], k) => (
                <rect key={k} className={`bp-anchor bp-anchor--${k}`} x={x - 18} y={y - 18} width="36" height="36" style={{ "--k": k } as React.CSSProperties} />
              ))}
            </g>
            <circle className="bp-trail bp-trail--top" cx="515" cy="459" r="335" pathLength={1} />
            <circle className="bp-trail bp-trail--bot" cx="515" cy="459" r="335" pathLength={1} />
            {use("top", "bp-arc bp-arc--top")}
            {use("bot", "bp-arc bp-arc--bot")}
            <g className="bp-hand">
              {use("palm", "bp-palm")}
              {use("thumb", "bp-thumb")}
            </g>
            {use("f1", "bp-f bp-f--1")}
            {use("f2", "bp-f bp-f--2")}
            {use("f3", "bp-f bp-f--3")}
            {use("f4", "bp-f bp-f--4")}
            <circle className="bp-ring" cx="525" cy="452" r="150" />
            {mode === "load" ? <rect className="bp-caret" x="508" y="352" width="34" height="206" rx="12" /> : null}
            {use("nib", "bp-nib")}
            {use("bar", "bp-bar")}
          </svg>
          {mode === "load" ? <BpWord /> : null}
        </div>
        {mode === "route" && label ? (
          <span className="bp-label">
            <Label prefix="bpm" text={label} />
            <Label prefix="bpw" text={label} />
          </span>
        ) : null}
      </div>
    </div>
  );
}
