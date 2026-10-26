/* motion-pilot components: small, composable builders. Each returns a controller; all state comes from time. */
(function(){
const C = window.C = {}, {el,tf,clamp,lerp,P,eo,eio,back} = M;

/* Background. {css|color, blobs:[{c:'rgba(..)',x,y,r,ax,ay,sp,ph}]} -> {update(t)} (animated aurora blobs) */
C.bg = (root,s={})=>{
  root.style.background = s.css || s.color || '#000';
  const R = Math.max(M.W,M.H);
  const blobs=(s.blobs||[]).map((b,i)=>{
    const d=el(root,`position:absolute;border-radius:50%;pointer-events:none;width:${b.r*R*2}px;height:${b.r*R*2}px;background:radial-gradient(circle,${b.c} 0%,${b.c.replace(/[\d.]+\)$/,'0)')} 68%)`);
    return {d,b,i};});
  return {update(t){blobs.forEach(({d,b,i})=>{const sp=b.sp||.35, ph=b.ph??i;
    d.style.left=(M.W*(b.x+(b.ax??.06)*Math.sin(t*sp+ph))-b.r*R)+'px'; d.style.top=(M.H*(b.y+(b.ay??.05)*Math.cos(t*sp*.8+ph))-b.r*R)+'px';});}};
};

/* Text block. {text,x,y,w,size,weight,font,color,align,ls,lh,wrap} -> {el,set(html),tf(o)} */
C.text = (root,o)=>{
  const e=el(root,`position:absolute;left:${o.x??0}px;top:${o.y??0}px;width:${o.w??M.W}px;text-align:${o.align||'center'};font-family:${o.font||'inherit'};font-weight:${o.weight||700};font-size:${o.size||120}px;line-height:${o.lh||1.05};letter-spacing:${o.ls??-0.03}em;color:${o.color||'#fff'};white-space:${o.wrap?'normal':'nowrap'}`,o.text||'');
  return {el:e,set:h=>{e.innerHTML=h;},tf:p=>tf(e,p)};
};

/* Pill/chip. {label,icon,dot,bg,color,size,font,weight,px,py} -> {el,set(label),tf}  (positioned with tf x,y) */
C.pill = (root,o)=>{
  const sz=o.size||30;
  const e=el(root,`position:absolute;left:0;top:0;display:flex;align-items:center;gap:${o.gap??14}px;padding:${o.py??18}px ${o.px??30}px;border-radius:999px;background:${o.bg||'#fff'};color:${o.color||'#111'};font-family:${o.font||'inherit'};font-weight:${o.weight||500};font-size:${sz}px;white-space:nowrap;box-shadow:${o.shadow??'0 20px 50px rgba(0,0,0,.22)'}`,
    (o.dot?`<b style="width:${sz*.45}px;height:${sz*.45}px;border-radius:50%;background:${o.dot};display:block"></b>`:'')+(o.icon?`<span style="font-size:${sz*1.15}px;line-height:1">${o.icon}</span>`:'')+`<span class="pl">${o.label||''}</span>`);
  return {el:e,set:l=>{e.querySelector('.pl').innerHTML=l;},tf:p=>tf(e,p),w:()=>e.offsetWidth,h:()=>e.offsetHeight};
};

/* Card. {w,h,img|html,radius,bg,shadow,fit} */
C.card = (root,o)=>{
  const e=el(root,`position:absolute;left:0;top:0;width:${o.w}px;height:${o.h}px;border-radius:${o.radius??26}px;overflow:hidden;background:${o.bg||'#fff'};box-shadow:${o.shadow??'0 40px 80px rgba(0,0,0,.35)'}`,
    o.img?`<img src="${o.img}" style="width:100%;height:100%;object-fit:${o.fit||'cover'};display:block">`:(o.html||''));
  return {el:e,tf:p=>tf(e,p)};
};

/* Phone mockup. {w=310,img|html,bg} -> {el,screen,tf}. Screen is (w-24)x(h-24); design app UIs at 286x626 for w=310. */
C.phone = (root,o={})=>{
  const w=o.w??310,h=Math.round(w*650/310),sw=w-24,sh=h-24;
  const e=el(root,`position:absolute;left:0;top:0;width:${w}px;height:${h}px;border-radius:${w*.168}px;background:#0b0b16;padding:12px;box-shadow:0 40px 90px rgba(0,0,0,.5)`);
  const scr=el(e,`position:relative;width:${sw}px;height:${sh}px;border-radius:${w*.135}px;overflow:hidden;background:${o.bg||'#fff'}`);
  if(o.img) el(scr,`position:absolute;left:0;top:36px;width:${sw}px;height:${sh-36}px;object-fit:contain;object-position:50% 0`,'', 'img').src=o.img;   // keep a status strip, never crop tab bars
  if(o.html) scr.innerHTML=o.html;
  el(e,`position:absolute;left:${w*.37}px;top:22px;width:${w*.258}px;height:24px;border-radius:12px;background:#0b0b16`);
  return {el:e,screen:scr,w,h,tf:p=>tf(e,p)};
};

/* Browser window with scrolling page. {w,h,img,url,dark} -> {el,scroll(p,px),tf} */
C.browser = (root,o)=>{
  const e=el(root,`position:absolute;left:0;top:0;width:${o.w}px;height:${o.h}px;border-radius:20px;overflow:hidden;background:#0a0a3a;box-shadow:0 40px 80px rgba(0,0,0,.4)`);
  el(e,'height:56px;background:#e9e9f1;display:flex;align-items:center;gap:10px;padding:0 22px',`<b style="width:14px;height:14px;border-radius:50%;background:#ff5f57"></b><b style="width:14px;height:14px;border-radius:50%;background:#febc2e"></b><b style="width:14px;height:14px;border-radius:50%;background:#28c840"></b><div style="margin-left:24px;height:34px;flex:1;border-radius:17px;background:#fff;display:flex;align-items:center;padding:0 18px;font:19px sans-serif;color:#565678">${o.url||''}</div>`);
  const vp=el(e,`position:absolute;left:0;top:56px;width:${o.w}px;height:${o.h-56}px;overflow:hidden`);
  const im=el(vp,`width:${o.w}px;display:block`,'','img'); im.src=o.img;
  return {el:e,scroll:(p,px)=>{im.style.transform=`translateY(${-p*px}px)`;},tf:p=>tf(e,p)};
};

/* Pointer (mouse arrow) with click ripple. at(x,y,press 0..1,ripple 0..1) */
C.pointer = (root,o={})=>{
  const sz=o.size||44;
  const rip=el(root,`position:absolute;left:0;top:0;width:90px;height:90px;border-radius:50%;border:4px solid ${o.ripple||'#fff'};opacity:0;pointer-events:none;z-index:49`);
  const e=el(root,`position:absolute;left:0;top:0;width:${sz}px;height:${sz}px;pointer-events:none;z-index:50;filter:drop-shadow(0 6px 10px rgba(0,0,0,.3))`,
    `<svg width="${sz}" height="${sz}" viewBox="0 0 24 24"><path d="M4 2l15 9-6.5 1.6L9.5 19z" fill="${o.fill||'#111'}" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>`);
  return {el:e,at:(x,y,press=0,r=0)=>{tf(e,{x,y,s:1-press*.14,origin:'4px 2px'});tf(rip,{x:x-39,y:y-41,s:.2+r*1.3,o:r>0&&r<1?(1-r)*.8:0});}};
};

/* Text cursor bar (the signature typing cursor). at(x,y,h,visible) */
C.bar = (root,o={})=>{const e=el(root,`position:absolute;left:0;top:0;width:${o.w||12}px;background:${o.color||'#FF6500'};border-radius:2px;display:none`);
  return {el:e,at:(x,y,h,vis=true)=>{e.style.display=vis?'block':'none';e.style.height=h+'px';tf(e,{x,y});}};};

/* Segmented progress bar. {n,x,y,w,gap,h,color,track} -> set(frac 0..1 over all segments) */
C.progress = (root,o)=>{
  const segs=[...Array(o.n)].map((_,i)=>{const t=el(root,`position:absolute;left:${o.x+i*(o.w+(o.gap??12))}px;top:${o.y}px;width:${o.w}px;height:${o.h??6}px;border-radius:3px;background:${o.track||'rgba(255,255,255,.16)'};overflow:hidden`);
    return el(t,`height:100%;width:0;background:${o.color||'#FF6500'}`);});
  return {set:f=>segs.forEach((s,i)=>{s.style.width=(clamp(f*o.n-i)*100)+'%';})};
};

/* Orbit: items [{html,w,h}] on an ellipse with depth blur/scale. update(angle,{radius,coll,blur,lo}) coll 0..1 collapses to centre */
C.orbit = (root,o)=>{
  const nodes=o.items.map(it=>({d:el(root,`position:absolute;left:0;top:0;width:${it.w}px;height:${it.h}px`,it.html),w:it.w,h:it.h}));
  return {nodes,update:(ang,u={})=>{const rad=u.radius??1,coll=u.coll??0;
    nodes.forEach((n,i)=>{const th=i/nodes.length*Math.PI*2+ang+(o.phase||0), s=Math.sin(th), c=Math.cos(th), f=(c+1)/2;
      const x=o.cx+s*o.rx*rad*(1-coll), y=o.cy+c*o.ry*rad*(1-coll)+(o.jit?Math.sin(i*1.9+ang*2)*o.jit:0);
      const sc=lerp(o.smin??.55,1,f)*(1-coll*.9);
      tf(n.d,{x:x-n.w/2,y:y-n.h/2,s:sc,rz:s*(o.tilt??3),b:((1-f)*(u.blur??4.5))+coll*8,o:lerp(.5,1,f)*(1-P(coll,.85,1)),zi:f*1000,br:lerp(.55,1,f)});});}};
};

/* Colour flood: circular reveal from a point. set(p,x,y) */
C.flood = (root,color)=>{const e=el(root,`position:absolute;left:0;top:0;width:${M.W}px;height:${M.H}px;background:${color};display:none;z-index:40`);
  return {el:e,set:(p,x=M.W/2,y=M.H/2)=>{e.style.display=p>0?'block':'none';e.style.clipPath=`circle(${p*Math.hypot(M.W,M.H)}px at ${x}px ${y}px)`;}};};

/* Deterministic confetti burst from (x,y). update(lt) with lt seconds since burst */
C.confetti = (root,o)=>{
  const cols=o.colors||['#FF4D6D','#FFB020','#4D7CFE','#3DDC97','#B15CFF'], n=o.n||40;
  const ps=[...Array(n)].map((_,i)=>{const a=-Math.PI/2+(M.rnd(i)-.5)*2.4, v=o.speed||900*(.5+M.rnd(i+9)), w=10+M.rnd(i+3)*14;
    return {d:el(root,`position:absolute;left:0;top:0;width:${w}px;height:${w*.5}px;background:${cols[i%cols.length]};display:none;z-index:30`),vx:Math.cos(a)*v,vy:Math.sin(a)*v,spin:(M.rnd(i+5)-.5)*900};});
  return {update:lt=>ps.forEach(p=>{const on=lt>0&&lt<(o.life||1.8); p.d.style.display=on?'block':'none'; if(!on) return;
    tf(p.d,{x:o.x+p.vx*lt,y:o.y+p.vy*lt+.5*1900*lt*lt,rz:p.spin*lt,o:clamp(1-(lt-(o.life||1.8)*.6)/((o.life||1.8)*.4))});})};
};

/* Logo parts: assemble an SVG from pieces. parts:[{d,fill,from:{rot,x,y},t0,t1,ox,oy}] -> set(lt) */
C.logoParts = (root,o)=>{
  const svg=el(root,`position:absolute;left:${o.x}px;top:${o.y}px;overflow:visible`,'','div');
  svg.innerHTML=`<svg width="${o.w}" height="${o.h}" viewBox="${o.viewBox}" style="overflow:visible;display:block">${o.parts.map((p,i)=>`<g id="lp${i}"><path d="${p.d}" fill="${p.fill}"/></g>`).join('')}</svg>`;
  const gs=o.parts.map((p,i)=>svg.querySelector('#lp'+i));
  return {el:svg,set:lt=>o.parts.forEach((p,i)=>{const k=back(P(lt,p.t0,p.t1),p.s??1.5), f=p.from||{};
    gs[i].setAttribute('transform',`translate(${(1-k)*(f.x||0)} ${(1-k)*(f.y||0)}) rotate(${(1-k)*(f.rot||0)} ${p.ox||0} ${p.oy||0})`);
    gs[i].style.opacity=clamp(P(lt,p.t0,p.t0+.12));})};
};
})();
