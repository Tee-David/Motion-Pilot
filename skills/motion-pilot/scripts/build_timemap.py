#!/usr/bin/env python3
"""Build a time map (output time -> source/animation time) that pins animation moments to spoken words.
  build_timemap.py words.json beats.json --dur 42.6 --src-dur 20 --out timemap.json
beats.json: [{"src": 2.4, "say": "five seconds", "at": "start", "lead": 0.0}, ...]
  src  = the moment in the ANIMATION (source seconds, as authored in project.js)
  say  = the phrase (matched against words.json, fuzzy); at = "start"|"end" of that phrase; lead = shift in seconds (negative = earlier)
Plain knots are also allowed: {"out": 3.5, "src": 1.66}. First/last knots (0,0) and (dur, src-dur) are added automatically.
Holds: give two beats the same src range spread over a long output span (e.g. src 8.5->9.0 mapped to out 11.0->13.0) and the scene slows there.
Prints warnings for unmatched phrases and for knots dropped because time would run backwards."""
import argparse, difflib, json, re, sys
norm = lambda s: re.sub(r"[^a-z0-9' ]", '', s.lower().replace('’', "'")).split()
def find(words, phrase):
    ph = norm(phrase); tw = [norm(w['w'])[0] if norm(w['w']) else '' for w in words]; best = (0, None)
    for i in range(len(tw)-len(ph)+1):
        r = difflib.SequenceMatcher(None, ph, tw[i:i+len(ph)]).ratio()
        if r > best[0]: best = (r, i)
    return best[1], len(ph), best[0]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('words'); ap.add_argument('beats'); ap.add_argument('--dur', type=float, required=True)
    ap.add_argument('--src-dur', type=float, required=True); ap.add_argument('--out', default='timemap.json'); a = ap.parse_args()
    W = json.load(open(a.words))['words']; knots = [(0., 0.)]
    for b in json.load(open(a.beats)):
        if 'out' in b: knots.append((b['out'], b['src'])); continue
        i, n, r = find(W, b['say'])
        if i is None or r < .7: print(f"WARN no match for {b['say']!r} (best {r:.2f})", file=sys.stderr); continue
        t = (W[i]['start'] if b.get('at', 'start') == 'start' else W[i+n-1]['end'])+b.get('lead', 0.)
        knots.append((round(t, 3), b['src'])); print(f"{b['src']:6.2f} -> {t:6.2f}  {b['say']!r} (match {r:.2f})")
    knots.append((a.dur, a.src_dur)); knots.sort(); clean = [knots[0]]
    for o, s in knots[1:]:
        if o > clean[-1][0]+.01 and s > clean[-1][1]+.001: clean.append((o, s))
        else: print(f'WARN dropped knot out={o} src={s} (not increasing)', file=sys.stderr)
    json.dump({'knots': clean}, open(a.out, 'w'), indent=1); print(f'{len(clean)} knots -> {a.out}')
if __name__ == '__main__': main()
