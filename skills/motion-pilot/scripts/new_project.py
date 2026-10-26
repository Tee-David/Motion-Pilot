#!/usr/bin/env python3
"""Scaffold a self-contained motion project.
  new_project.py DIR --style keynote-dark [--list]   styles: see engine/styles.json
Creates DIR/{index.html, engine/, tokens.js, project.js, fonts/, assets/} and the decision files facts.md,
STORYLINES.md and SPEC.md (see references/process/). Fill those first, then edit project.js, then:
  render.py DIR --w 1920 --h 1080 --dur 9 --sheet 0.5,2,4,6,8 --sheet-out sheet.jpg   (fast look)
  render.py DIR --w 1920 --h 1080 --dur 9 --out out.mp4                                (full render)"""
import argparse, json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('dir',nargs='?'); ap.add_argument('--style',default='keynote-dark'); ap.add_argument('--list',action='store_true'); a = ap.parse_args()
    styles = json.load(open(f'{ROOT}/engine/styles.json')); styles.pop('_readme',None)
    if a.list or not a.dir:
        for k,v in styles.items(): print(f'{k:16} {v["label"]}  [template: {v["template"]}, sound: {v["sound"]}]')
        return
    s = styles.get(a.style) or sys.exit(f'unknown style {a.style}; use --list')
    d = a.dir; os.makedirs(d+'/assets',exist_ok=True); os.makedirs(d+'/engine',exist_ok=True)
    for f in ('motion.js','components.js'): shutil.copy(f'{ROOT}/engine/{f}',f'{d}/engine/{f}')
    subprocess.run([sys.executable,f'{ROOT}/scripts/fetch_font.py',s['display'],s['body'],'--dir',d+'/fonts'],check=True,capture_output=True)
    open(d+'/index.html','w').write('<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="fonts/fonts.css"></head><body>\n'
        '<script src="engine/motion.js"></script><script src="engine/components.js"></script>\n<script src="tokens.js"></script><script src="project.js"></script>\n</body></html>\n')
    tok = {k:s[k] for k in ('dark','light')}
    open(d+'/tokens.js','w').write(f'/* generated from styles.json: {a.style} */\nM.TOK={json.dumps(tok,indent=1)};\nM.T=M.TOK[M.theme]||M.TOK.dark;\n'
        f'M.F={{display:{json.dumps(chr(39)+s["display"]+chr(39))},body:{json.dumps(chr(39)+s["body"]+chr(39))}}};   // single quotes on purpose: double quotes break style="" attributes\nM.SOUND={json.dumps(s["sound"])};\n')
    shutil.copy(f'{ROOT}/templates/{s["template"]}.js',d+'/project.js')
    docs = {
        'facts.md': '# Facts\nEvery claim, number, name and quote that may appear on screen, with its source. Nothing goes on screen without a line here.\n\n| Fact | Exact wording on screen | Source |\n| --- | --- | --- |\n',
        'STORYLINES.md': '# Storylines\nBrief: format, length range, aspect ratios, themes, voice or not, music or not, assumptions.\n\nRecommendation: <A, B or C> because <one clause>.\n\n'
            + ''.join(f'## {k}: <name>\n- Device and form:\n- What the viewer sees and feels:\n- First two seconds:\n- Beats: hook → … → end card\n- Look:\n- Sound:\n- Assets and risk:\n\n' for k in 'ABC'),
        'SPEC.md': '# SPEC\n```text\nGOAL:\nOUTPUT:\nTIME:\nLOOK:\nOBJECTS:\nMOTION:\nSHOTS:\nBANNED:  the calibration list in SKILL.md, plus\nQA:\n```\n',
    }
    for name, body in docs.items():
        if not os.path.exists(f'{d}/{name}'): open(f'{d}/{name}', 'w').write(body)
    print(f'created {d}  (style {a.style}, template {s["template"]}, suggested sound palette {s["sound"]})')
if __name__=='__main__': main()
