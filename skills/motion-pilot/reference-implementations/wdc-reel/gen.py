from parts import PATHS, WM
def lockup(X, w, h):
    P=PATHS
    pa=lambda i,f: f'<path fill="{f}" d="{P[i][1]}"/>'
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 2944 944" style="overflow:visible;display:block">
<defs><clipPath id="{X}clipP"><rect id="{X}clip" x="1000" y="-50" width="0" height="1050"/></clipPath></defs>
<g id="{X}icon">
 <g id="{X}hands">{''.join(pa(i,'#ffffff') for i in range(1,7))}</g>
 <g id="{X}top">{pa(0,'#ffffff')}</g>
 <g id="{X}bot">{pa(7,'#ffffff')}</g>
 <g id="{X}nib">{pa(8,'#FF6500')}{pa(9,'#FF6500')}</g>
 <rect id="{X}cur" x="-22" y="-115" width="44" height="230" rx="6" fill="#FF6500"/>
</g>
<g clip-path="url(#{X}clipP)"><g id="{X}wm">{WM}</g></g>
<rect id="{X}sweep" x="1000" y="90" width="36" height="830" rx="6" fill="#FF6500"/>
</svg>'''
t=open('template.html').read()
t=t.replace('__LOCKUP_3__',lockup('l3',1500,481)).replace('__LOCKUP_7__',lockup('l7',1100,353))
open('index.html','w').write(t)
print(len(t))
