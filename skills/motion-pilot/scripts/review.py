#!/usr/bin/env python3
"""Review a rendered piece (or any video) the way a viewer will see it. See references/process/review.md.
  review.py VIDEO --out DIR [--frames 12] [--max-cuts 24]
Writes DIR/sheet.jpg (frames across the piece), DIR/phone.jpg (the same frames 360 px wide), DIR/cut-NN.jpg
(seven frames from -0.2 s to +0.2 s around every change event), DIR/report.json and DIR/report.md.
The report flags: an empty or black first frame, dead stretches (nothing moving for 3 s or more), blends whose
midpoint shows a colour neither neighbouring shot owns, and loudness and true peak when there is audio.
Everything here is measured; the judging is yours (the defect table in process/review.md)."""
import argparse, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motionlib as ml

def font(size):
    try: return ImageFont.load_default(size=size)
    except TypeError: return ImageFont.load_default()

def label(im, text, size=14):
    d = ImageDraw.Draw(im); f = font(size)
    w = d.textlength(text, font=f) if hasattr(d, 'textlength') else 8 * len(text)
    d.rectangle([0, 0, w + 10, size + 8], fill=(0, 0, 0)); d.text((5, 3), text, fill=(255, 200, 0), font=f)
    return im

def grid(ims, cols, bg=(22, 22, 30), gap=6):
    cw, ch = ims[0].size; rows = (len(ims) + cols - 1) // cols
    cv = Image.new('RGB', (cols * cw + (cols - 1) * gap, rows * ch + (rows - 1) * gap), bg)
    for i, im in enumerate(ims): cv.paste(im, ((i % cols) * (cw + gap), (i // cols) * (ch + gap)))
    return cv

def colours(im, k=6, min_share=.15):
    q = im.resize((96, 96)).quantize(colors=k, method=Image.Quantize.FASTOCTREE)
    pal = q.getpalette()[:k * 3]; cnt = q.getcolors(); tot = sum(c for c, _ in cnt)
    return [(np.array(pal[i * 3:i * 3 + 3], float), c / tot) for c, i in cnt if c / tot >= min_share]

def owned(rgb, im):
    q = np.asarray(im.resize((96, 96)), float).reshape(-1, 3)
    return float(np.min(np.linalg.norm(q - rgb, axis=1)))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--out', default='review')
    ap.add_argument('--frames', type=int, default=12); ap.add_argument('--max-cuts', type=int, default=24)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    w, h, dur, has_audio = ml.probe(a.video)
    pace, (t, e, ev) = ml.pacing(a.video)
    vertical = h > w * 1.2
    # sheet and phone sheet
    ts = [min(dur - .05, .05 + i * (dur - .1) / max(1, a.frames - 1)) for i in range(a.frames)]
    big = [ml.frame_at(a.video, x, 480 if not vertical else 270) for x in ts]
    big = [label(im, f'{x:.2f}s') for im, x in zip(big, ts) if im is not None]
    grid(big, 4 if not vertical else 6).save(f'{a.out}/sheet.jpg', quality=85)
    phone = [ml.frame_at(a.video, x, 360) for x in ts]
    phone = [label(im, f'{x:.1f}s', 11) for im, x in zip(phone, ts) if im is not None]
    grid(phone, 3 if not vertical else 4).save(f'{a.out}/phone.jpg', quality=85)
    # strips around change events
    cuts = []
    for n, (tc, mag) in enumerate(ev[:a.max_cuts]):
        fr = [ml.frame_at(a.video, tc + d, 320 if not vertical else 180) for d in np.linspace(-.2, .2, 7)]
        fr = [label(im, f'{tc + d:+.2f}s' if False else f'{tc + d:.2f}s', 11) for im, d in zip(fr, np.linspace(-.2, .2, 7)) if im is not None]
        if fr: grid(fr, 7, gap=3).save(f'{a.out}/cut-{n + 1:02d}.jpg', quality=82)
        # blend check: does the frame at the event show a large colour neither neighbour owns?
        mid = ml.frame_at(a.video, tc, 160); pre = ml.frame_at(a.video, max(0, tc - .5), 160); post = ml.frame_at(a.video, min(dur - .05, tc + .5), 160)
        off = []
        if mid and pre and post:
            for rgb, share in colours(mid):
                dist = min(owned(rgb, pre), owned(rgb, post))
                if dist > 60: off.append({'rgb': '#%02x%02x%02x' % tuple(int(c) for c in rgb), 'share': round(share, 2), 'distance': round(dist)})
        cuts.append({'n': n + 1, 't': round(tc, 2), 'strength': round(mag, 1), 'off_palette': off})
    # first frame
    f0 = ml.frame_at(a.video, 0, 320); arr = np.asarray(f0.convert('L'), float) if f0 else np.zeros((1, 1))
    first = {'mean_luma': round(float(arr.mean()), 1), 'detail': round(float(arr.std()), 1)}
    first['empty'] = bool(first['detail'] < 4 or first['mean_luma'] < 10)
    dead = [hd for hd in pace['holds'] if hd[1] >= 3]
    audio = ml.loudness(a.video) if has_audio else None
    rep = {'video': a.video, 'size': [w, h], 'duration': round(dur, 2), 'pacing': pace, 'first_frame': first,
           'dead_stretches': dead, 'cuts': cuts, 'audio': audio}
    json.dump(rep, open(f'{a.out}/report.json', 'w'), indent=1)
    L = [f'# Review of {os.path.basename(a.video)}', '', f'{w} x {h}, {dur:.2f} s.', '',
         '## Measured', '',
         f'- First frame: mean luma {first["mean_luma"]}, detail {first["detail"]}' + (' **flat or black: fine for a preloader that starts on its ground, a D3 fail for social and films**' if first['empty'] else ''),
         f'- Change events: {pace["change_events"]} ({pace["changes_per_10s"]} per 10 s); busiest at {", ".join(str(x) for x in pace["busiest_s"])} s',
         f'- Holds (start s, length s): {", ".join(f"({s}, {l})" for s, l in pace["holds"]) or "none"}; longest {pace["longest_hold_s"]} s; still {pace["still_pct"]}% of the time',
         f'- Dead stretches of 3 s or more: {", ".join(f"{s} s for {l} s" for s, l in dead) or "none"}' + (' **check D4: deliberate holds only**' if dead else ''),
         ]
    offs = [c for c in cuts if c['off_palette']]
    L.append(f'- Off-palette blends: ' + ('; '.join(f'cut-{c["n"]:02d} at {c["t"]} s shows ' + ', '.join(f'{o["rgb"]} ({int(o["share"] * 100)}%)' for o in c['off_palette']) for c in offs) + ' **check D10**' if offs else 'none'))
    if audio: L.append(f'- Audio: {audio["lufs"]} LUFS integrated, true peak {audio["true_peak_dbfs"]} dBFS, range {audio["lra"]} LU' + (' **true peak above -1 dBFS**' if audio['true_peak_dbfs'] is not None and audio['true_peak_dbfs'] > -1 else ''))
    else: L.append('- Audio: none')
    L += ['', '## Look at', '', '- `sheet.jpg`: describe each frame as a stranger would; name every object.',
          '- `phone.jpg`: can every line meant to be read be read at 360 px?',
          f'- `cut-01.jpg` to `cut-{len(cuts):02d}.jpg`: pops, flashes of the old shot, jumps, text over text.',
          '- Then the defect table in references/process/review.md: PASS or FAIL with evidence, notes ranked P0 to P2.',
          '- The sound was measured, not heard.']
    open(f'{a.out}/report.md', 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L[4:11])); print(f'-> {a.out}/')

if __name__ == '__main__': main()
