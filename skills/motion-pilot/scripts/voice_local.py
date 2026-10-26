#!/usr/bin/env python3
"""Offline draft voice (Kokoro ONNX). pip install kokoro-onnx soundfile; download kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases).
  voice_local.py "text or @script.txt" --voice af_heart --speed 1.0 --out vo.wav [--model-dir DIR]
Voices: af_heart af_bella af_nicole af_sarah af_sky (American F), bf_emma bf_isabella bf_alice bf_lily (British F). Draft quality: for timing and animatics."""
import argparse, os, sys
import numpy as np, soundfile as sf
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('text'); ap.add_argument('--voice', default='af_heart'); ap.add_argument('--speed', type=float, default=1.0)
    ap.add_argument('--out', default='vo.wav'); ap.add_argument('--model-dir', default='.'); a = ap.parse_args()
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(a.model_dir, 'kokoro-v1.0.onnx'), os.path.join(a.model_dir, 'voices-v1.0.bin'))
    text = open(a.text[1:]).read() if a.text.startswith('@') else a.text; out = []
    for line in [l.strip() for l in text.splitlines() if l.strip()]:
        au, sr = k.create(line, voice=a.voice, speed=a.speed, lang='en-gb' if a.voice.startswith('b') else 'en-us'); out += [au, np.zeros(int(sr*.4))]
    sf.write(a.out, np.concatenate(out), sr); print('wrote', a.out)
if __name__ == '__main__': main()
