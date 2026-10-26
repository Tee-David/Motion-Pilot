#!/usr/bin/env python3
"""Download Google Fonts (OFL) TTFs into DIR and write DIR/fonts.css with @font-face rules.
Usage: fetch_font.py "Inter" "DM Sans" --dir fonts      (offline: falls back to bundled Space Grotesk / Outfit)"""
import argparse, os, shutil, sys, urllib.request, urllib.parse
REG = {  # family -> repo path under google/fonts/ofl   ('[wght]' files are variable: weight range 100-900)
 'Space Grotesk':'spacegrotesk/SpaceGrotesk[wght].ttf','Outfit':'outfit/Outfit[wght].ttf','Inter':'inter/Inter[opsz,wght].ttf',
 'DM Sans':'dmsans/DMSans[opsz,wght].ttf','Manrope':'manrope/Manrope[wght].ttf','Plus Jakarta Sans':'plusjakartasans/PlusJakartaSans[wght].ttf',
 'Sora':'sora/Sora[wght].ttf','Syne':'syne/Syne[wght].ttf','Bricolage Grotesque':'bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf',
 'Instrument Serif':'instrumentserif/InstrumentSerif-Regular.ttf','Bebas Neue':'bebasneue/BebasNeue-Regular.ttf','Anton':'anton/Anton-Regular.ttf',
 'Unbounded':'unbounded/Unbounded[wght].ttf','Figtree':'figtree/Figtree[wght].ttf',
 'JetBrains Mono':'jetbrainsmono/JetBrainsMono[wght].ttf','DM Mono':'dmmono/DMMono-Medium.ttf'}
BUNDLED = os.path.join(os.path.dirname(__file__),'..','fonts')
def fetch(family, d):
    path = REG.get(family)
    if not path: sys.exit(f'Unknown family {family!r}. Known: {", ".join(REG)}. Add it to REG (path under google/fonts/ofl).')
    fn = os.path.basename(path).replace('[','').replace(']','').replace(',','_'); dst = os.path.join(d,fn)
    if not os.path.exists(dst):
        url = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'+urllib.parse.quote(path,safe='/,')
        try: urllib.request.urlretrieve(url,dst)
        except Exception as e:
            b = os.path.join(BUNDLED,fn.replace('wght',''))
            for cand in (os.path.join(BUNDLED,fn), os.path.join(BUNDLED,fn.split('_')[0]), os.path.join(BUNDLED,family.replace(' ','')+'.ttf')):
                if os.path.exists(cand): shutil.copy(cand,dst); break
            else: sys.exit(f'Could not download {family}: {e}')
    w = '100 900' if '[' in path else '400'
    return f'@font-face{{font-family:"{family}";src:url("{fn}");font-weight:{w};font-display:block}}\n'
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('families',nargs='+'); ap.add_argument('--dir',default='fonts'); a = ap.parse_args()
    os.makedirs(a.dir,exist_ok=True); css = ''.join(fetch(f,a.dir) for f in dict.fromkeys(a.families))
    open(os.path.join(a.dir,'fonts.css'),'w').write(css); print(css)
if __name__=='__main__': main()
