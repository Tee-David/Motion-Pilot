"""Shared measurements for analyze_reference.py and review.py.

Motion energy is the mean absolute difference between consecutive greyscale frames (0..255) at a
low resolution. Peaks are change events (cuts, morphs, big moves), which a scene-cut detector misses
when a film morphs on one ground. Runs of near-zero energy are holds."""
import json, re, subprocess
import numpy as np
from PIL import Image

def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)

def probe(f):
    o = run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height:format=duration', '-of', 'json', f])
    j = json.loads(o.stdout); v = [s for s in j['streams'] if s.get('codec_type') == 'video'][0]
    return int(v['width']), int(v['height']), float(j['format']['duration']), any(s.get('codec_type') == 'audio' for s in j['streams'])

def energy(f, fps=15, w=160, end=None):
    """Motion energy at a low resolution that keeps the video's aspect ratio (a tall frame squeezed into
    a wide thumbnail hides thin moving lines). About 14,400 pixels whatever the shape."""
    vw, vh, _, _ = probe(f)
    if vh > vw: h_, w_ = w, max(2, int(round(w * vw / vh / 2)) * 2)
    else: w_, h_ = w, max(2, int(round(w * vh / vw / 2)) * 2)
    k = (14400 / (w_ * h_)) ** .5; w_, h_ = int(w_ * k) // 2 * 2, int(h_ * k) // 2 * 2
    cmd = ['ffmpeg', '-v', 'error', '-i', f] + (['-t', str(end)] if end else []) + ['-vf', f'fps={fps},scale={w_}:{h_},format=gray', '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h_, w_).astype(np.float32)
    e = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)) if len(fr) > 1 else np.zeros(0)
    t = (np.arange(len(e)) + 1) / fps
    return t, e

def events(t, e, min_gap=0.25, window=0.4):
    """Change events: local maxima at least 3x the film's median motion that stand clear of their surroundings
    (1.8x the quietest point within `window` seconds either side). Calm films report few events, montages many."""
    if len(e) < 3: return []
    dt = t[1] - t[0]; w = max(1, int(round(window / dt)))
    floor = max(1.5, float(np.median(e)) * 3)
    out = []
    for i in range(1, len(e) - 1):
        if e[i] < floor or e[i] < e[i - 1] or e[i] <= e[i + 1]: continue
        if e[i] < 1.8 * min(e[max(0, i - w):i].min(), e[i + 1:i + 1 + w].min()): continue
        if out and t[i] - out[-1][0] < min_gap:
            if e[i] > out[-1][1]: out[-1] = (float(t[i]), float(e[i]))
            continue
        out.append((float(t[i]), float(e[i])))
    return out

def holds(t, e, still=0.03, min_len=0.4):
    """Spans where nothing moves (energy under `still`; a few typed characters at 1080p measure about 0.03), at least `min_len` seconds long."""
    out, s = [], None
    dt = t[1] - t[0] if len(t) > 1 else 1 / 15
    for i, v in enumerate(e):
        if v < still and s is None: s = t[i] - dt
        if (v >= still or i == len(e) - 1) and s is not None:
            end = t[i] - dt if v >= still else t[i]
            if end - s >= min_len: out.append((round(float(s), 2), round(float(end - s), 2)))
            s = None
    return out

def pacing(f, end=None):
    t, e = energy(f, end=end)
    dur = float(t[-1]) if len(t) else 0.0
    ev = events(t, e); hd = holds(t, e)
    still = sum(l for _, l in hd)
    return {'change_events': len(ev), 'changes_per_10s': round(len(ev) / max(dur, 1e-6) * 10, 1),
            'holds': hd[:12], 'longest_hold_s': max([l for _, l in hd], default=0.0),
            'still_pct': int(round(still / max(dur, 1e-6) * 100)),
            'busiest_s': [round(x, 2) for x, _ in sorted(ev, key=lambda p: -p[1])[:6]]}, (t, e, ev)

def frame_at(f, t, width=480):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t):.3f}', '-i', f, '-frames:v', '1', '-vf', f'scale={width}:-2',
                        '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    from io import BytesIO
    return Image.open(BytesIO(r.stdout)).convert('RGB') if r.stdout else None

def palette(ims, k=6):
    tiles = [im.resize((48, 48)) for im in ims if im is not None]
    mos = Image.new('RGB', (48 * len(tiles), 48))
    for i, tl in enumerate(tiles): mos.paste(tl, (i * 48, 0))
    q = mos.quantize(colors=k, method=Image.Quantize.FASTOCTREE)
    pal = q.getpalette()[:k * 3]; cnt = sorted(q.getcolors(), reverse=True)
    tot = sum(c for c, _ in cnt)
    return [{'hex': '#%02x%02x%02x' % tuple(pal[i * 3:i * 3 + 3]), 'share': round(c / tot, 2)} for c, i in cnt]

def loudness(f, end=None):
    e = run(['ffmpeg', '-nostats', '-i', f] + (['-t', str(end)] if end else []) + ['-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr
    summary = e[e.rfind('Summary:'):] if 'Summary:' in e else e
    g = lambda pat: (lambda m: float(m[-1]) if m else None)(re.findall(pat, summary))
    return {'lufs': g(r'I:\s+(-?\d+\.\d+) LUFS'), 'lra': g(r'LRA:\s+(-?\d+\.\d+) LU'), 'true_peak_dbfs': g(r'Peak:\s+(-?\d+\.\d+) dBFS')}
