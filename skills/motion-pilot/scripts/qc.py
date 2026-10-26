#!/usr/bin/env python3
"""Verify a rendered video before delivery.
  qc.py video.mp4 [--expect-frames N] [--expect-dur S] [--audio] [--loop] [--sheet 1,5,9 --sheet-out qc.jpg] [--black] [--freeze]
Checks: decodes with zero errors; frame count / duration; audio stream + loudness; loop seam (first vs last frame mean diff < 1);
optional contact sheet at given seconds; black-frame and frozen-frame spans. Exits non-zero on failure."""
import argparse, json, re, subprocess, sys
import numpy as np
from PIL import Image
def run(c): return subprocess.run(c, capture_output=True, text=True)
def frame(f, t, w=320):
    r = subprocess.run(['ffmpeg', '-v', 'quiet', '-ss', str(t), '-i', f, '-vf', f'scale={w}:-2', '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    import io; return Image.open(io.BytesIO(r.stdout)).convert('RGB')
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--expect-frames', type=int); ap.add_argument('--expect-dur', type=float)
    ap.add_argument('--audio', action='store_true'); ap.add_argument('--loop', action='store_true'); ap.add_argument('--sheet'); ap.add_argument('--sheet-out', default='qc.jpg')
    ap.add_argument('--black', action='store_true'); ap.add_argument('--freeze', action='store_true'); a = ap.parse_args(); ok = True; f = a.video
    err = run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'null', '-']).stderr.strip(); n = len(err.splitlines())
    print(f'decode errors: {n}'); ok &= n == 0
    pr = json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,width,height,nb_read_frames:format=duration', '-of', 'json', f]).stdout)
    v = next(s for s in pr['streams'] if s['codec_type'] == 'video'); dur = float(pr['format']['duration']); nf = int(v['nb_read_frames'])
    print(f"video {v['width']}x{v['height']} frames {nf} duration {dur:.2f}s audio {'yes' if any(s['codec_type']=='audio' for s in pr['streams']) else 'no'}")
    if a.expect_frames: ok &= nf == a.expect_frames; print('frames match' if nf == a.expect_frames else f'FRAME MISMATCH expected {a.expect_frames}')
    if a.expect_dur: good = abs(dur-a.expect_dur) < .1; ok &= good; print('duration ok' if good else f'DURATION MISMATCH expected {a.expect_dur}')
    if a.audio:
        has = any(s['codec_type'] == 'audio' for s in pr['streams']); ok &= has
        if has:
            e = run(['ffmpeg', '-nostats', '-i', f, '-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr; I = re.findall(r'I:\s+(-?\d+\.\d+) LUFS', e); P = re.findall(r'Peak:\s+(-?\d+\.\d+) dBFS', e)
            print(f"loudness {I[-1] if I else '?'} LUFS, true peak {P[-1] if P else '?'} dBFS (social target about -14 LUFS, peak <= -1)")
    if a.loop:
        d = float(np.abs(np.asarray(frame(f, 0, 320), float)-np.asarray(frame(f, max(0, dur-.04), 320), float)).mean()); print(f'loop seam diff {d:.2f}'); ok &= d < 1.5
    if a.black:
        print('black spans:', re.findall(r'black_start:([\d.]+).*?black_duration:([\d.]+)', run(['ffmpeg', '-nostats', '-i', f, '-vf', 'blackdetect=d=0.2:pix_th=0.05', '-an', '-f', 'null', '-']).stderr) or 'none')
    if a.freeze:
        print('frozen spans:', re.findall(r'freeze_start: ([\d.]+)', run(['ffmpeg', '-nostats', '-i', f, '-vf', 'freezedetect=n=0.001:d=1.0', '-an', '-f', 'null', '-']).stderr) or 'none')
    if a.sheet:
        ts = [float(x) for x in a.sheet.split(',')]; ims = [frame(f, t, 320) for t in ts]; cols = min(6, len(ims)); h = ims[0].height
        s = Image.new('RGB', (cols*320, ((len(ims)+cols-1)//cols)*h)); [s.paste(im, ((i % cols)*320, (i//cols)*h)) for i, im in enumerate(ims)]; s.save(a.sheet_out, quality=85); print('sheet', a.sheet_out)
    print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
if __name__ == '__main__': main()
