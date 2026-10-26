#!/usr/bin/env python3
"""Word-level timestamps for a voiceover file (the sync backbone). Works on any audio (ElevenLabs download, recording, local TTS).
  align_voice.py voice.mp3 --out words.json [--prompt "Brand names, SEO, product terms"] [--model base.en]
Output: {"duration":..,"words":[{"w","start","end"}],"sentences":[{"text","start","end"}]}
Notes: pass a numpy array to faster-whisper (file paths can crash on some PyAV builds). Whisper may mis-spell brand words; the
prompt helps. Cross-check sentence starts against silence gaps; do not trust silencedetect alone."""
import argparse, json, subprocess, sys
import numpy as np
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('--out', default='words.json'); ap.add_argument('--prompt', default=''); ap.add_argument('--model', default='base.en'); a = ap.parse_args()
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.audio, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    au = np.frombuffer(raw, dtype=np.float32)
    try: from faster_whisper import WhisperModel
    except ImportError: sys.exit('pip install faster-whisper --break-system-packages')
    m = WhisperModel(a.model, device='cpu', compute_type='int8'); segs, _ = m.transcribe(au, word_timestamps=True, initial_prompt=a.prompt or None)
    words = [{'w': w.word.strip(), 'start': round(w.start, 2), 'end': round(w.end, 2)} for s in segs for w in s.words]
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if w['w'].endswith(('.', '?', '!')): sents.append({'text': ' '.join(x['w'] for x in cur), 'start': cur[0]['start'], 'end': w['end']}); cur = []
    if cur: sents.append({'text': ' '.join(x['w'] for x in cur), 'start': cur[0]['start'], 'end': cur[-1]['end']})
    json.dump({'duration': round(len(au)/16000, 2), 'words': words, 'sentences': sents}, open(a.out, 'w'), indent=1)
    for s in sents: print(f"{s['start']:6.2f}-{s['end']:6.2f}  {s['text']}")
if __name__ == '__main__': main()
