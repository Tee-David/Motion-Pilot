#!/usr/bin/env python3
"""Study a reference video: contact sheet + pacing (cuts) + dominant palette + audio stats.
Usage: analyze_reference.py VIDEO [VIDEO...] [--out DIR] [--frames 12] [--trim-end 3.2]
--trim-end ignores the last N seconds (TikTok/IG outro cards) for cuts/palette/audio.
Writes DIR/<name>_sheet.jpg and DIR/analysis.json. Audio tempo is a ROUGH estimate (octave errors);
loudness / onset density / brightness are reliable. `cuts` counts hard scene cuts only; `pacing` counts every change event
(cuts, morphs and big moves on one ground) and lists the holds, which is the better measure of rhythm."""
import argparse, glob, json, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import stft
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motionlib

def run(cmd): return subprocess.run(cmd, capture_output=True, text=True)
def probe(f):
    o = run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height:format=duration','-of','json',f])
    j = json.loads(o.stdout); return int(j['streams'][0]['width']), int(j['streams'][0]['height']), float(j['format']['duration'])

def frames(f, dur, n, tmp):
    for p in glob.glob(f'{tmp}/*.jpg'): os.remove(p)
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-vf',f'fps={n/dur:.5f},scale=-2:360','-frames:v',str(n),f'{tmp}/%02d.jpg'])
    return [Image.open(p).convert('RGB') for p in sorted(glob.glob(f'{tmp}/*.jpg'))]

def sheet(ims, vertical, label):
    cw,ch,cols = (160,284,len(ims)) if vertical else (320,180,6)
    rows = 1 if vertical else (len(ims)+cols-1)//cols
    cv = Image.new('RGB',(cols*cw,rows*ch),(25,25,30))
    for k,im in enumerate(ims):
        im = im.copy(); im.thumbnail((cw,ch)); cv.paste(im,((k%cols)*cw,(k//cols)*ch))
    d = ImageDraw.Draw(cv); d.rectangle([0,0,150,16],fill=(0,0,0)); d.text((3,2),label,fill=(255,200,0))
    return cv

def palette(ims, k=6):
    tiles = [im.resize((48,48)) for im in ims]
    mos = Image.new('RGB',(48*len(tiles),48))
    for i,t in enumerate(tiles): mos.paste(t,(i*48,0))
    q = mos.quantize(colors=k, method=Image.Quantize.FASTOCTREE)
    pal = q.getpalette()[:k*3]; cnt = sorted(q.getcolors(), reverse=True)
    tot = sum(c for c,_ in cnt)
    return [{'hex':'#%02x%02x%02x'%tuple(pal[i*3:i*3+3]),'share':round(c/tot,2)} for c,i in cnt]

def cuts(f, end, thr=0.28):
    r = run(['ffmpeg','-nostats','-i',f,'-t',str(end),'-vf',f"select='gt(scene,{thr})',showinfo",'-f','null','-'])
    return [float(x) for x in re.findall(r'pts_time:([\d.]+)', r.stderr)]

def audio(f, end):
    r = subprocess.run(['ffmpeg','-v','error','-i',f,'-t',str(end),'-vn','-ac','1','-ar','22050','-f','f32le','-'],capture_output=True)
    a = np.frombuffer(r.stdout,dtype=np.float32)
    if len(a) < 22050*3: return None
    e = run(['ffmpeg','-nostats','-i',f,'-t',str(end),'-af','ebur128=peak=true','-f','null','-']).stderr
    I = re.findall(r'I:\s+(-?\d+\.\d+) LUFS',e); LRA = re.findall(r'LRA:\s+(-?\d+\.\d+) LU',e)
    fr,_,Z = stft(a,fs=22050,nperseg=1024,noverlap=512); S = np.abs(Z)
    cent = (S*fr[:,None]).sum(0)/(S.sum(0)+1e-9); low = S[fr<150].sum(0)/(S.sum(0)+1e-9)
    flux = np.maximum(0,np.diff(S,axis=1)).sum(0); flux /= flux.max()+1e-9
    thr = flux.mean()+1.2*flux.std()
    idx = [i for i in range(1,len(flux)-1) if flux[i]>thr and flux[i]>=flux[i-1] and flux[i]>flux[i+1]]
    x = flux-flux.mean(); ac = np.correlate(x,x,'full')[len(x)-1:]; hop = 512/22050
    best = max(((b, ac[int(round(60/b/hop))]+0.5*ac[min(len(ac)-1,2*int(round(60/b/hop)))]) for b in range(70,181)), key=lambda t:t[1])
    return {'lufs':float(I[-1]) if I else None,'lra':float(LRA[-1]) if LRA else None,'onsets_per_s':round(len(idx)/(len(a)/22050),1),
            'centroid_hz':int(np.median(cent)),'sub150_pct':int(low.mean()*100),'tempo_rough_bpm':best[0]}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('videos',nargs='+'); ap.add_argument('--out',default='analysis')
    ap.add_argument('--frames',type=int,default=12); ap.add_argument('--trim-end',type=float,default=0.0)
    a = ap.parse_args(); os.makedirs(a.out,exist_ok=True); res = {}
    for f in a.videos:
        w,h,dur = probe(f); end = max(2.0, dur-a.trim_end); name = os.path.splitext(os.path.basename(f))[0]
        with tempfile.TemporaryDirectory() as tmp:
            ims = frames(f,end,a.frames,tmp)
        sheet(ims, h>w*1.2, f'{name[:18]} {dur:.0f}s').save(f'{a.out}/{name}_sheet.jpg',quality=82)
        c = cuts(f,end)
        res[name] = {'size':[w,h],'duration':round(dur,1),'cuts':len(c),'avg_shot_s':round(end/(len(c)+1),2),
                     'cuts_per_10s':round(len(c)/end*10,1),'pacing':motionlib.pacing(f,end)[0],'palette':palette(ims),'audio':audio(f,end)}
        pc = res[name]['pacing']; print(name, 'cuts', len(c), '| change events', pc['change_events'], f"({pc['changes_per_10s']}/10s)", '| longest hold', pc['longest_hold_s'], 's', flush=True)
    json.dump(res,open(f'{a.out}/analysis.json','w'),indent=1)
if __name__=='__main__': main()
