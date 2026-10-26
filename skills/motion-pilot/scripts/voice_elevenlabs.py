#!/usr/bin/env python3
"""ElevenLabs text-to-speech with character timestamps (optional: the usual flow is to generate in the ElevenLabs web app and upload the file).
  export ELEVENLABS_API_KEY=...        voice_elevenlabs.py --voices                      list your voices
  voice_elevenlabs.py script.txt --voice VOICE_ID --out vo.mp3 [--model eleven_v3] [--stability 0.4] [--dry-run]
v3 reads audio tags inline: [confident] [smirking] [chuckles] [whispers] [excited] ... and ellipses for beats. Multilingual v2 ignores tags.
Writes vo.mp3 and vo.alignment.json (per-character timing straight from the API, no Whisper needed).
NOTE: written to the public API shape; I could not call it from the authoring sandbox (no key). Use --dry-run to inspect the request first."""
import argparse, base64, json, os, sys, urllib.request
API = 'https://api.elevenlabs.io/v1'
def call(path, key, body=None):
    req = urllib.request.Request(API+path, data=json.dumps(body).encode() if body else None, headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=120))
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('script', nargs='?'); ap.add_argument('--voice'); ap.add_argument('--out', default='vo.mp3'); ap.add_argument('--model', default='eleven_v3')
    ap.add_argument('--stability', type=float, default=.4); ap.add_argument('--similarity', type=float, default=.75); ap.add_argument('--style', type=float, default=.3)
    ap.add_argument('--voices', action='store_true'); ap.add_argument('--dry-run', action='store_true'); a = ap.parse_args(); key = os.environ.get('ELEVENLABS_API_KEY', '')
    if a.voices:
        for v in call('/voices', key)['voices']: print(v['voice_id'], v['name'], v.get('labels', {}))
        return
    if not (a.script and a.voice): sys.exit('need script file and --voice VOICE_ID')
    body = {'text': open(a.script).read().strip(), 'model_id': a.model, 'voice_settings': {'stability': a.stability, 'similarity_boost': a.similarity, 'style': a.style}}
    if a.dry_run: print(json.dumps(body, indent=1)); return
    if not key: sys.exit('set ELEVENLABS_API_KEY')
    r = call(f'/text-to-speech/{a.voice}/with-timestamps', key, body)
    open(a.out, 'wb').write(base64.b64decode(r['audio_base64'])); json.dump(r.get('alignment'), open(a.out.rsplit('.', 1)[0]+'.alignment.json', 'w'))
    print('wrote', a.out)
if __name__ == '__main__': main()
