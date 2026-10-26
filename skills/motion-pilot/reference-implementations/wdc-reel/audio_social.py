import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000
DUR = 42.6
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(3)

def hz(n):  # midi -> hz
    return 440 * 2 ** ((n - 69) / 12)

def put(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    L[i:i + len(s)] += s * np.sqrt((1 - pan) / 2) * 1.414
    R[i:i + len(s)] += s * np.sqrt((1 + pan) / 2) * 1.414

def filt(x, kind, f, order=2):
    if kind == 'bp':
        sos = butter(order, [f[0] / (SR / 2), f[1] / (SR / 2)], 'band', output='sos')
    else:
        sos = butter(order, f / (SR / 2), kind, output='sos')
    return sosfilt(sos, x)

def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d)
    return e

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.16)
    s += filt(rng.normal(0, 1, n), 'hp', 3000) * np.exp(-t / 0.004) * 0.25
    return np.tanh(s * 1.6)

def hat(open_=False):
    n = int((0.18 if open_ else 0.06) * SR)
    s = filt(rng.normal(0, 1, n), 'hp', 7500, 4)
    return s * env(n, 0.001, 0.07 if open_ else 0.018)

def clap():
    n = int(0.3 * SR)
    s = filt(rng.normal(0, 1, n), 'bp', (900, 2600), 2)
    e = np.zeros(n)
    for o in (0, 0.011, 0.022):
        i = int(o * SR); e[i:] += env(n - i, 0.001, 0.012 if o < 0.02 else 0.09)
    return s * e

def click():
    n = int(0.03 * SR)
    s = filt(rng.normal(0, 1, n), 'bp', (2500, 6000), 2) * env(n, 0.0005, 0.006)
    t = np.arange(n) / SR
    s += np.sin(2 * np.pi * 1800 * t) * env(n, 0.0005, 0.004) * 0.4
    return s

def whoosh(d, f0, f1, rev=False):
    n = int(d * SR)
    x = rng.normal(0, 1, n)
    out = np.zeros(n); blk = 1024
    for i in range(0, n, blk):
        p = i / n
        f = f0 * (f1 / f0) ** p
        seg = x[i:i + blk]
        out[i:i + blk] = filt(seg, 'bp', (max(80, f * 0.6), min(20000, f * 1.6)), 1)
    t = np.linspace(0, 1, n)
    e = np.sin(np.pi * t) ** 2 if not rev else t ** 3 * (1 - t) ** 0.3
    return out * e

def riser(d):
    n = int(d * SR); t = np.arange(n) / SR
    f = 200 * (8 ** (t / d))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3
    s += whoosh(d, 400, 9000) * 0.9
    return s * (t / d) ** 2

def impact():
    n = int(2.2 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (38 + 40 * np.exp(-t / 0.08)) * t) * np.exp(-t / 0.6)
    s += filt(rng.normal(0, 1, n), 'lp', 1800) * np.exp(-t / 0.25) * 0.6
    return np.tanh(s * 1.4)

def ding(f=1318.5, d=1.6):
    n = int(d * SR); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / (0.6 / m)) for m, a in ((1, 1), (2.01, .4), (3.02, .18), (4.1, .08)))
    return s * env(n, 0.002, 0.8)

def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 500 + 900 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03)

def pad(notes, d, cutoff=1400, a=0.25):
    n = int(d * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for det in (-0.08, 0.0, 0.08):
            f = hz(m + det)
            s += (2 * ((f * t) % 1) - 1) * 0.12
    s = filt(s, 'lp', cutoff, 2)
    e = np.minimum(1, t / a) * np.minimum(1, (d - t) / 0.25)
    return s * np.clip(e, 0, 1)

def bass(m, d):
    n = int(d * SR); t = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return np.tanh(1.5 * s) * env(n, 0.005, d * 0.6)


from timemap_social import out
def at(s): return out(s)
Fmaj9=[53,57,60,64,67]; Dm9=[50,53,57,60,64]; Bbmaj7=[46,50,53,57,62]; Am7=[45,52,55,60,64]; C7=[48,52,55,58,64]
prog=[(0,4.99,Fmaj9,900,41),(4.99,4.6,Dm9,800,38),(9.59,4.6,Bbmaj7,900,34),(14.19,1.1,C7,1200,36),(15.3,3.3,Fmaj9,1900,41),
      (18.6,3.4,Fmaj9,2000,41),(22.0,1.9,Am7,2000,45),(23.9,2.5,Dm9,2000,38),(26.4,2.2,Bbmaj7,2000,34),(28.6,2.7,Fmaj9,2100,41),(31.3,3.3,Am7,2100,45),
      (34.6,1.6,Dm9,2000,38),(36.2,1.5,Bbmaj7,2000,34),(37.7,0.47,C7,2200,36),(38.17,4.43,Fmaj9,2400,41)]
pads=np.zeros(N)
for st,d,ch,cut,root in prog:
    p=pad(ch,d+0.3,cut,0.3 if st>0 else 0.6); i=int(st*SR); pads[i:i+len(p)]+=p[:N-i]
tl=np.linspace(1,0,int(1.8*SR)); pads[-len(tl):]*=tl
put(pads,0,0.5)
def beats(a,b,step=0.5):
    x=a
    while x<b-1e-6: yield round(x,4); x+=step
K=kick(); H=hat(); HO=hat(True); Cl=clap()
for t in beats(4.99,13.0,1.0): put(K,t,0.7)
for t in beats(15.3,37.6): put(K,t,0.85)
for t in beats(15.8,37.6,1.0): put(Cl,t,0.28)
for t in beats(15.55,37.6): put(HO if int((t-15.55)*2)%4==3 else H,t,0.17,0.3)
for t in beats(18.6,34.6,0.25): put(H,t,0.06,-0.3)
for st,d,ch,cut,root in prog[5:13]:
    for t in beats(st,st+d): put(bass(root,0.42),t,0.3)
CL=click(); P_=pop()
for k in range(10): put(CL,at(0.22+k*0.045),0.3,rng.uniform(-.3,.3))
for k in range(15): put(CL,at(1.22+k*0.018),0.24,rng.uniform(-.3,.3))
put(whoosh(0.25,800,4000),3.42,0.28)
put(whoosh(0.45,300,6000),4.5,0.55)
for T in (4.99,11.48,13.62): put(impact()[:int(0.4*SR)],T,0.32)
for i,T in enumerate([6.67,7.61,8.63,9.85]): put(P_,T,0.38,(-1)**i*0.4); put(ding(1567.98+i*200,0.5),T,0.08)
for i in range(8): put(P_,11.48+i*0.09,0.16,rng.uniform(-.7,.7))
put(riser(1.18),13.0,0.45)
put(whoosh(1.1,6000,200,rev=True),14.18,0.5)
put(impact(),15.25,0.9)
for s0,amt in ((4.5,-0.4),(4.58,0.4)): put(whoosh(0.35,500,3000),at(s0),0.3,amt)
put(whoosh(0.3,300,1500),at(4.76),0.3,-0.6); put(whoosh(0.25,4000,900),at(4.86),0.28)
put(ding(1318.5),at(5.1),0.3); put(ding(1975.5),at(5.13),0.15)
put(whoosh(0.45,600,5000),at(5.6),0.28,0.5)
put(riser(0.3),18.0,0.4); put(impact(),18.3,0.6)
for C in (22.0,23.9,26.4,28.6,31.3): put(whoosh(0.3,700,5000),C-0.15,0.28,0.3)
for k in range(12): put(CL,at(9.55+k*0.034),0.18)
put(ding(1567.98,1.0),at(10.0),0.22)
for i in range(3): put(P_,at(13.85+i*0.1),0.26,(i-1)*0.5)
put(whoosh(0.4,300,4000),34.35,0.45); put(whoosh(0.6,3000,300),34.6,0.3)
for s0,n_ in ((14.72,14),(15.42,12),(16.1,10)):
    for k in range(n_): put(CL,at(s0)+k*0.03,0.12,0.2)
    put(ding(1046.5,0.6),at(s0+0.4),0.1)
put(whoosh(0.4,6000,300,rev=True),37.62,0.4); put(P_,at(16.88),0.35)
put(impact(),38.17,0.9); put(whoosh(0.5,200,3000),38.2,0.35)
put(whoosh(0.35,500,3000),at(17.3),0.28,-0.4); put(whoosh(0.35,500,3000),at(17.36),0.28,0.4)
put(ding(1318.5,2.2),at(17.7),0.3); put(ding(1975.5,2.0),at(17.73),0.15)
put(whoosh(0.4,600,5000),at(17.72),0.22,0.5)
put(P_,at(18.28),0.3)
for k in range(22): put(CL,at(18.42+k*0.032),0.2,rng.uniform(-.2,.2))
# ---------- voice + ducking ----------
import subprocess, soundfile as sf
subprocess.run(['ffmpeg','-v','error','-y','-i','/mnt/user-data/uploads/ElevenLabs_2026-10-04T12_49_52__s50_v4.mp3','-ar','48000','-ac','1','vo48.wav'])
vo,_=sf.read('vo48.wav'); vo=np.pad(vo,(0,max(0,N-len(vo))))[:N]
# ---------- reverb + master ----------
ir_n = int(1.6 * SR)
ir = rng.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR / 0.45)
ir = filt(ir, 'lp', 5000); ir /= np.abs(ir).sum() ** 0.5 * 30
wetL = fftconvolve(L, ir)[:N]; wetR = fftconvolve(R, ir[::-1].copy())[:N]
L2 = L + wetL * 0.9; R2 = R + wetR * 0.9
st = np.stack([L2, R2], 1)
st /= np.abs(st).max()+1e-9
venv=np.convolve((np.abs(vo)>0.015).astype(float),np.ones(int(0.3*SR))/(0.3*SR),'same')
duck=1-0.5*np.clip(venv*2.5,0,1)
st = st*duck[:,None]*0.55 + np.stack([vo,vo],1)/(np.abs(vo).max()+1e-9)*0.8
st = filt(st.T, 'hp', 28).T if False else st
st /= np.abs(st).max() + 1e-9
st = np.tanh(st * 1.6) / np.tanh(1.6)
fade = np.ones(N); fl = int(0.25 * SR); fade[-fl:] = np.linspace(1, 0, fl) ** 1.5
st *= fade[:, None] * 0.89
wavfile.write('/home/claude/build/social_mix.wav', SR, (st * 32767).astype(np.int16))
print('ok', st.shape, np.abs(st).max())
