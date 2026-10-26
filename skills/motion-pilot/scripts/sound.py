#!/usr/bin/env python3
"""Synthesize a sound bed + SFX from the animation's cue list, optionally duck under a voiceover and master to a LUFS target.
  sound.py --cues PROJECT/cues.json --dur 30 --palette clean-tech --out mix.wav [--timemap map.json] [--voice vo.wav] [--music bed.mp3] [--lufs -14]
Palettes: clean-tech bright-pop warm-lofi bold-poster dreamy-glass minimal-ui cinematic none   (see references/sound-design.md)
Cue types (declare with M.cue(t,type) in project.js): type tick click swap pop whoosh riser impact ding hit success notify swipe
All synthesis is royalty-free (numpy/scipy). --music replaces the synthesized bed with YOUR licensed track (it is looped/trimmed and ducked)."""
import argparse, json, os, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR = 48000
rng = np.random.default_rng(7)
hz = lambda n: 440*2**((n-69)/12)
def filt(x, kind, f, o=2):
    f = np.array(f)/(SR/2) if kind == 'bp' else f/(SR/2)
    return sosfilt(butter(o, f, kind, output='sos'), x)
def env(n, a, d):
    t = np.arange(n)/SR; return np.minimum(1, t/max(a, 1e-4))*np.exp(-np.maximum(0, t-a)/d)

# ---------- voices ----------
def kick(g=1., sub=45):
    n = int(.45*SR); t = np.arange(n)/SR; f = sub+110*np.exp(-t/.035)
    s = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.16)+filt(rng.normal(0, 1, n), 'hp', 3000)*np.exp(-t/.004)*.25
    return np.tanh(s*1.6)*g
def hat(open_=False, br=1.):
    n = int((.18 if open_ else .06)*SR); return filt(rng.normal(0, 1, n), 'hp', 7500*br, 4)*env(n, .001, .07 if open_ else .018)
def clap():
    n = int(.3*SR); s = filt(rng.normal(0, 1, n), 'bp', (900, 2600)); e = np.zeros(n)
    for o in (0, .011, .022):
        i = int(o*SR); e[i:] += env(n-i, .001, .012 if o < .02 else .09)
    return s*e
def snap():
    n = int(.12*SR); return filt(rng.normal(0, 1, n), 'bp', (1800, 5500))*env(n, .0005, .03)
def click(br=1.):
    n = int(.03*SR); t = np.arange(n)/SR
    return filt(rng.normal(0, 1, n), 'bp', (2500*br, 6000*br))*env(n, .0005, .006)+np.sin(2*np.pi*1800*br*t)*env(n, .0005, .004)*.4
def tick(br=1.):
    n = int(.02*SR); t = np.arange(n)/SR; return np.sin(2*np.pi*2400*br*t)*env(n, .0003, .004)*.7
def whoosh(d, f0, f1, rev=False):
    n = int(d*SR); x = rng.normal(0, 1, n); out = np.zeros(n)
    for i in range(0, n, 1024):
        f = f0*(f1/f0)**(i/n); out[i:i+1024] = filt(x[i:i+1024], 'bp', (max(80, f*.6), min(20000, f*1.6)), 1)
    t = np.linspace(0, 1, n); return out*((np.sin(np.pi*t)**2) if not rev else t**3*(1-t)**.3)
def riser(d):
    n = int(d*SR); t = np.arange(n)/SR; f = 200*(8**(t/d))
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*.3+whoosh(d, 400, 9000)*.9)*(t/d)**2
def impact(low=38, d=2.2):
    n = int(d*SR); t = np.arange(n)/SR
    return np.tanh((np.sin(2*np.pi*(low+40*np.exp(-t/.08))*t)*np.exp(-t/.6)+filt(rng.normal(0, 1, n), 'lp', 1800)*np.exp(-t/.25)*.6)*1.4)
def ding(f=1318.5, d=1.6):
    n = int(d*SR); t = np.arange(n)/SR
    return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t/(.6/m)) for m, a in ((1, 1), (2.01, .4), (3.02, .18), (4.1, .08)))*env(n, .002, .8)
def pop(br=1.):
    n = int(.12*SR); t = np.arange(n)/SR; return np.sin(2*np.pi*np.cumsum(500*br+900*br*np.exp(-t/.02))/SR)*env(n, .001, .03)
def pluck(f, d=.5):
    n = int(d*SR); t = np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*2*f*t)*np.exp(-t/.08))*env(n, .002, d*.35)
def pad(notes, d, cut=1500, a=.3, wave='saw'):
    n = int(d*SR); t = np.arange(n)/SR; s = np.zeros(n)
    for m in notes:
        for det in (-.08, 0, .08):
            f = hz(m+det); s += ((2*((f*t) % 1)-1) if wave == 'saw' else np.sin(2*np.pi*f*t))*.12
    return filt(s, 'lp', cut)*np.clip(np.minimum(1, t/a)*np.minimum(1, (d-t)/.25), 0, 1)
def bass(m, d, drive=1.5):
    n = int(d*SR); t = np.arange(n)/SR; f = hz(m)
    return np.tanh(drive*(np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t)))*env(n, .005, d*.6)

# ---------- palettes ----------
CH_MIN = [[53,57,60,64,67],[50,53,57,60,64],[46,50,53,57,62],[45,52,55,60,64]]
CH_MAJ = [[48,52,55,59,64],[55,59,62,66,69],[45,52,57,60,64],[53,57,60,64,67]]
PAL = {
 'clean-tech':  dict(bpm=120, chords=CH_MIN, pad=dict(cut=1800, wave='saw'), drums='four',  bass=True,  arp=None,    rev=.9, bed=.55, br=1.0, sfx=1.0),
 'bright-pop':  dict(bpm=112, chords=CH_MAJ, pad=dict(cut=2600, wave='saw'), drums='half',  bass=True,  arp=.25,     rev=.6, bed=.5,  br=1.25, sfx=1.1),
 'warm-lofi':   dict(bpm=82,  chords=CH_MIN, pad=dict(cut=900,  wave='sine'),drums='lofi',  bass=True,  arp=None,    rev=.7, bed=.5,  br=.7,  sfx=.8),
 'bold-poster': dict(bpm=128, chords=CH_MIN, pad=dict(cut=1400, wave='saw'), drums='four',  bass=True,  arp=None,    rev=.4, bed=.6,  br=1.1, sfx=1.3, sub=38),
 'dreamy-glass':dict(bpm=80,  chords=CH_MAJ, pad=dict(cut=3200, wave='sine'),drums=None,    bass=False, arp=.5,      rev=1.6,bed=.55, br=1.3, sfx=.8),
 'minimal-ui':  dict(bpm=100, chords=None,   pad=None,                       drums=None,    bass=False, arp=None,    rev=.3, bed=0,   br=1.1, sfx=.9),
 'cinematic':   dict(bpm=90,  chords=CH_MIN, pad=dict(cut=900,  wave='saw'), drums=None,    bass=True,  arp=None,    rev=1.8,bed=.6,  br=.8,  sfx=1.4, sub=30),
 'none':        dict(bpm=100, chords=None,   pad=None,                       drums=None,    bass=False, arp=None,    rev=.0, bed=0,   br=1.0, sfx=1.0)}

def load_audio(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--cues', required=True); ap.add_argument('--dur', type=float, required=True)
    ap.add_argument('--palette', default='clean-tech', choices=list(PAL)); ap.add_argument('--out', default='mix.wav')
    ap.add_argument('--timemap'); ap.add_argument('--voice'); ap.add_argument('--voice-delay', type=float, default=0)
    ap.add_argument('--music'); ap.add_argument('--bpm', type=float); ap.add_argument('--drop', type=float, help='time drums/bass enter (default: first impact cue or 25%%)')
    ap.add_argument('--duck', type=float, default=.5, help='0..1 how much bed+sfx dip under voice'); ap.add_argument('--lufs', type=float, default=-14)
    ap.add_argument('--sfx-gain', type=float, default=1.0); ap.add_argument('--no-bed', action='store_true'); a = ap.parse_args()
    P = PAL[a.palette]; N = int(a.dur*SR); L = np.zeros(N); R = np.zeros(N)
    out_t = (lambda s: s)
    if a.timemap:
        k = json.load(open(a.timemap)); k = k['knots'] if isinstance(k, dict) else k
        TM_O = np.array([x for x, _ in k], float); TM_S = np.array([y for _, y in k], float); out_t = lambda s: float(np.interp(s, TM_S, TM_O))
    cues = sorted(json.load(open(a.cues)), key=lambda c: c['t'])
    def put(sig, t, g=1., pan=0.):
        i = int(t*SR)
        if i >= N or i < -len(sig): return
        s = sig[max(0, -i):N-i]*g; i = max(0, i)
        L[i:i+len(s)] += s*np.sqrt((1-pan)/2)*1.414; R[i:i+len(s)] += s*np.sqrt((1+pan)/2)*1.414
    bpm = a.bpm or P['bpm']; beat = 60/bpm; br = P['br']; sg = P['sfx']*a.sfx_gain
    drop = a.drop if a.drop is not None else next((out_t(c['t']) for c in cues if c['type'] in ('impact', 'hit')), a.dur*.25)
    # ---- bed ----
    bed_on = P['bed'] > 0 and not a.no_bed and not a.music
    if bed_on:
        bar = beat*4; ch = P['chords']; i = 0; t = 0.
        pads = np.zeros(N)
        while t < a.dur:
            c = ch[i % len(ch)]; d = bar*(1 if bpm >= 100 else 2)
            p = pad(c, d+.3, a=.3 if t else .6, **P['pad']); j = int(t*SR); pads[j:j+len(p)] += p[:N-j]
            if P['bass'] and t >= drop - bar:
                for b in range(int(d/beat)):
                    bt = t+b*beat
                    if bt >= drop-1e-6 and bt < a.dur: put(bass(c[0]-12 if c[0] > 40 else c[0], beat*.9), bt, .3)
            if P['arp']:
                st = beat*P['arp']; k = 0; at = t
                while at < t+d and at < a.dur:
                    put(pluck(hz(c[(k*2) % len(c)]+12), .5), at, .16, (-.5, .5)[k % 2]); at += st; k += 1
            t += d; i += 1
        pads[-int(1.5*SR):] *= np.linspace(1, 0, int(1.5*SR))
        L += pads*P['bed']; R += pads*P['bed']
        if P['drums']:
            K = kick(1., P.get('sub', 45)); H = hat(False, br); HO = hat(True, br); C = clap(); SN = snap(); t = drop; k = 0
            while t < a.dur-beat:
                pat = P['drums']
                if pat == 'four':
                    put(K, t, .85); put(HO if k % 4 == 3 else H, t+beat/2, .18, .3)
                    if k % 2 == 1: put(C, t, .3)
                elif pat == 'half':
                    if k % 2 == 0: put(K, t, .75)
                    if k % 2 == 1: put(SN, t, .45)
                    put(H, t+beat/2, .12, .3)
                elif pat == 'lofi':
                    if k % 4 in (0, 2): put(K, t+(beat*.12 if k % 4 == 2 else 0), .6)
                    if k % 4 == 3: put(SN, t, .35)
                    put(H, t+beat/2+beat*.08, .1, .3)
                t += beat; k += 1
    elif a.music:
        m = load_audio(a.music); m = np.tile(m, int(np.ceil(N/len(m)))+1)[:N]; m *= np.minimum(1, np.minimum(np.arange(N)/SR/.5, (N-np.arange(N))/SR/1.5))
        L += m*.6; R += m*.6
    # ---- sfx from cues ----
    S_ = dict(type=lambda: click(br), tick=lambda: tick(br), click=lambda: click(br), swap=lambda: whoosh(.22, 800*br, 4000*br)*.8, pop=lambda: pop(br),
              whoosh=lambda: whoosh(.45, 300, 6000*br), riser=lambda: riser(.9), impact=lambda: impact(P.get('sub', 38)), hit=lambda: impact(P.get('sub', 38), .8),
              ding=lambda: ding(1318.5*(1.2 if br > 1.2 else 1)), success=lambda: ding(1568)+ding(2093)*.6, notify=lambda: ding(1760, .9), swipe=lambda: whoosh(.18, 1500, 6000))
    base = dict(type=.3, tick=.3, click=.35, swap=.3, pop=.14, whoosh=.45, riser=.45, impact=.9, hit=.7, ding=.3, success=.3, notify=.25, swipe=.25)
    for c in cues:
        f = S_.get(c['type'])
        if f: put(f(), out_t(c['t'])+c.get('offset', 0), base[c['type']]*c.get('gain', 1.)*sg, c.get('pan', 0.))
    # ---- reverb ----
    if P['rev'] > 0:
        n = int(P['rev']*SR); ir = rng.normal(0, 1, n)*np.exp(-np.arange(n)/SR/(P['rev']*.3)); ir = filt(ir, 'lp', 5000); ir /= np.abs(ir).sum()**.5*30
        L2 = L+fftconvolve(L, ir)[:N]*.9; R2 = R+fftconvolve(R, ir[::-1].copy())[:N]*.9
    else: L2, R2 = L, R
    st = np.stack([L2, R2], 1); st /= np.abs(st).max()+1e-9
    if a.voice:
        v = load_audio(a.voice); v = np.concatenate([np.zeros(int(a.voice_delay*SR)), v])[:N]; v = np.pad(v, (0, N-len(v)))
        ve = np.convolve((np.abs(v) > .015).astype(float), np.ones(int(.3*SR))/(.3*SR), 'same')
        st = st*(1-a.duck*np.clip(ve*2.5, 0, 1))[:, None]*.55+np.stack([v, v], 1)/(np.abs(v).max()+1e-9)*.8
    st = np.tanh(st*1.5)/np.tanh(1.5); fo = int(.25*SR); st[-fo:] *= np.linspace(1, 0, fo)[:, None]
    tmp = a.out+'.raw.wav'; wavfile.write(tmp, SR, (st*.89*32767).astype(np.int16))
    if a.lufs is not None: subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', f'loudnorm=I={a.lufs}:TP=-1.0:LRA=11', '-ar', str(SR), a.out], check=True); os.remove(tmp)
    else: os.replace(tmp, a.out)
    print(f'{a.out}  palette={a.palette} bpm={bpm:.0f} drop={drop:.2f}s cues={len(cues)} voice={"yes" if a.voice else "no"}')
if __name__ == '__main__': main()
