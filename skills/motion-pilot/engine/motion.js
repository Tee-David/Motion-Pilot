/* motion-pilot engine core.
 * RULE: everything on screen must be a PURE FUNCTION of time. render(t) may not depend on previous calls.
 * That is what makes frames reproducible, chunk-resumable and splice-able. No CSS animations, no timers. */
(function(){
const M = window.M = {};
const q = new URLSearchParams(location.search);
M.W = +q.get('w') || 1920; M.H = +q.get('h') || 1080;
M.V = M.H > M.W;                       // portrait?
M.theme = q.get('theme') || 'dark';
M.RT = 0;                              // real (output) time, for things that must hit a spoken word or blink in real time
M.scenes = []; M.cues = []; M.globals = [];
M.cfg = { grain: 0.06, bg: '#000', fonts: [] };

/* ---------- math & easing ---------- */
const clamp = (x,a=0,b=1)=>Math.min(b,Math.max(a,x));
M.clamp = clamp; M.lerp = (a,b,x)=>a+(b-a)*x; M.P = (t,a,b)=>clamp((t-a)/(b-a));
M.eo  = x=>1-Math.pow(1-x,3);                       // default ease-out
M.eo5 = x=>1-Math.pow(1-x,5);                       // snappy entrances
M.ei  = x=>x*x*x;                                   // exits
M.eio = x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;     // camera moves, re-centering
M.xo  = x=>x>=1?1:1-Math.pow(2,-10*x);              // reveals / fly-ins
M.xi  = x=>x<=0?0:Math.pow(2,10*x-10);              // implosions / zoom-ins
M.xio = x=>x<=0?0:x>=1?1:x<.5?Math.pow(2,20*x-10)/2:(2-Math.pow(2,-20*x+10))/2; // circular wipes
M.back = (x,s=1.70158)=>{const c=s+1;return 1+c*Math.pow(x-1,3)+s*Math.pow(x-1,2)};  // overshoot
M.spring = x=>x<=0?0:x>=1?1:1-Math.exp(-7*x)*Math.cos(11*x);                         // springy settle
M.rnd = i=>{const x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)};       // deterministic noise
/* bez(x1,y1,x2,y2): a CSS cubic-bezier as an easing function of x 0..1, so the film and the website share one curve. */
M.bez = (x1,y1,x2,y2)=>{
  const cx=3*x1, bx=3*(x2-x1)-cx, ax=1-cx-bx, cy=3*y1, by=3*(y2-y1)-cy, ay=1-cy-by;
  const X=s=>((ax*s+bx)*s+cx)*s, Y=s=>((ay*s+by)*s+cy)*s, dX=s=>(3*ax*s+2*bx)*s+cx;
  return x=>{ if(x<=0) return 0; if(x>=1) return 1; let s=x;
    for(let i=0;i<8;i++){const e=X(s)-x, d=dX(s); if(Math.abs(e)<1e-6) break; if(Math.abs(d)<1e-6) break; s-=e/d;}
    if(s<0||s>1||Math.abs(X(s)-x)>1e-4){let a=0,b=1; s=x; for(let i=0;i<30;i++){ if(X(s)<x) a=s; else b=s; s=(a+b)/2; }}
    return Y(s); };
};
/* Named curves by role (see references/craft/timing-and-easing.md). */
M.ease = {
  arrive: M.bez(.16,1,.3,1),  exit: M.bez(.4,0,1,1),    travel: M.bez(.65,0,.35,1), sheet: M.bez(.77,0,.18,1),
  fall: M.bez(.55,0,1,.45),   pop: M.bez(.2,.7,.3,1),   reach: M.bez(.34,1.45,.64,1), rivet: M.bez(.34,1.6,.64,1),
  orbit: M.bez(.45,0,.2,1),   sine: x=>-(Math.cos(Math.PI*x)-1)/2,
};
/* springD(x, damping): a closed-form spring settling at x=1, named by damping ratio (1 = no overshoot, .7-.85 premium,
   .4-.6 playful). Pure function of x, so any frame renders on its own. */
M.springD = (x,z=.75)=>{ if(x<=0) return 0; if(x>=1) return 1; const w=12, t=x;
  if(z>=1) return 1-(1+w*t)*Math.exp(-w*t);
  const wd=w*Math.sqrt(1-z*z); return 1-Math.exp(-z*w*t)*(Math.cos(wd*t)+(z*w/wd)*Math.sin(wd*t)); };
/* pscale(a,b,p): interpolate scale in log space so a zoom does not appear to slow as it grows. */
M.pscale = (a,b,p)=>Math.exp(Math.log(Math.max(a,1e-4))+(Math.log(Math.max(b,1e-4))-Math.log(Math.max(a,1e-4)))*p);
/* poster(t,fps): hold every n-th frame for a hand-made, stepped look (a choice, never an accident). */
M.poster = (t,step=2,fps=30)=>Math.floor(t*fps/step)*step/fps;
/* seg(t,t0,dur,ease): progress of a segment that starts at t0 and lasts dur, eased. The building block of every move. */
M.seg = (t,t0,dur,ease=M.ease.arrive)=>ease(M.P(t,t0,t0+dur));
M.blink = (rate=3.6)=>(Math.floor(M.RT*rate)%2)===0;
M.typed = (s,t,t0,dt)=>s.slice(0,clamp(Math.floor((t-t0)/dt),0,s.length));

/* ---------- DOM helpers ---------- */
M.el = (parent,css='',html='',tag='div')=>{const e=document.createElement(tag); if(css) e.style.cssText=css; if(html) e.innerHTML=html; (parent||document.body).appendChild(e); return e;};
/* tf: set transform/opacity/blur in one call. x,y,z px; rx,ry deg (3D); rz deg; s or sx,sy; o opacity; b blur px; br brightness */
M.tf = (e,o={})=>{
  const t=[];
  if(o.x!==undefined||o.y!==undefined||o.z!==undefined||o.dy!==undefined) t.push(`translate3d(${o.x||0}px,${(o.y||0)+(o.dy||0)}px,${o.z||0}px)`);   // dy = relative offset (from swap), never overwrites y
  if(o.rx!==undefined) t.push(`rotateX(${o.rx}deg)`); if(o.ry!==undefined) t.push(`rotateY(${o.ry}deg)`); if(o.rz!==undefined) t.push(`rotate(${o.rz}deg)`);
  if(o.sx!==undefined||o.sy!==undefined) t.push(`scale(${o.sx??1},${o.sy??1})`); else if(o.s!==undefined) t.push(`scale(${o.s})`);
  e.style.transform=t.join(' ');
  if(o.o!==undefined) e.style.opacity=o.o;
  const f=[]; if(o.b!==undefined&&o.b>0.05) f.push(`blur(${o.b.toFixed(2)}px)`); if(o.br!==undefined) f.push(`brightness(${o.br})`);
  e.style.filter=f.length?f.join(' '):'none';
  if(o.origin) e.style.transformOrigin=o.origin; if(o.zi!==undefined) e.style.zIndex=Math.round(o.zi);
};
/* swap: the signature blur-swap. pin 0..1 = entering, pout 0..1 = leaving. returns {y,b,o} to spread into tf() */
M.swap = (pin,pout=0,o={})=>{const d=o.dist??60, bl=o.blur??14, a=M.eo(pin), b=M.ei(pout);
  return {dy:(1-a)*d-b*d, b:(1-a)*bl+b*bl, o:a*(1-b)};};   // spread into tf(): tf(el,{x,y,...M.swap(pin,pout)}). pin=1 means fully entered.
M.measure = (html,css='')=>{ if(!M._m) M._m=M.el(document.body,'position:absolute;left:-9999px;top:0;visibility:hidden;white-space:nowrap');
  M._m.style.cssText='position:absolute;left:-9999px;top:0;visibility:hidden;white-space:nowrap;'+css; M._m.innerHTML=html; return M._m.offsetWidth; };
M.fit = (html,css,maxW,size)=>{const w=M.measure(html,css+`;font-size:${size}px`); return w>maxW?Math.floor(size*maxW/w):size;};
M.words = (el,text,css='')=>{ el.innerHTML=''; return text.split(' ').map(w=>M.el(el,'display:inline-block;white-space:pre;'+css,w+'&nbsp;','span')); };
M.letters = (el,text,css='')=>{ el.innerHTML=''; return [...text].map(c=>M.el(el,'display:inline-block;white-space:pre;'+css,c===' '?'&nbsp;':c,'span')); };

/* ---------- scenes ---------- */
/* M.scene(name, t0, t1, {build(root,ctx), update(lt,t,ctx,root), pad, z}) — times in SOURCE seconds.
 * lt = local time since t0. pad lets a scene stay alive across a transition. Scenes stack in definition order. */
M.scene = (name,t0,t1,def)=>{const s={name,t0,t1,def,root:null,ctx:{}}; M.scenes.push(s); return s;};
/* M.cue(t,type,opts): declare a sound event next to the animation that causes it. Export with M.exportCues(). */
M.cue = (t,type,o={})=>{M.cues.push({t:+t.toFixed(4),type,...o});};
M.cueTyping = (t0,n,dt,gain=1,skip=0)=>{for(let i=skip;i<n;i++) M.cue(t0+i*dt,'type',{gain});};
M.exportCues = ()=>M.cues.slice().sort((a,b)=>a.t-b.t);
M.global = f=>M.globals.push(f);

M.init = ()=>{
  M.stage = M.el(document.body,`position:absolute;left:0;top:0;width:${M.W}px;height:${M.H}px;overflow:hidden;background:${M.cfg.bg}`);
  document.body.style.cssText=`margin:0;width:${M.W}px;height:${M.H}px;overflow:hidden;background:#000`;
  M.scenes.forEach((s,i)=>{
    s.root=M.el(M.stage,`position:absolute;left:0;top:0;width:${M.W}px;height:${M.H}px;overflow:hidden;display:none;z-index:${s.def.z??(1+i)}`);
    s.root.style.display='block'; s.def.build&&s.def.build(s.root,s.ctx,s); s.root.style.display='none';   // visible during build so offsetWidth works
  });
  if(M.cfg.grain>0){
    const c=document.createElement('canvas'); c.width=c.height=256; const g=c.getContext('2d'), d=g.createImageData(256,256);
    for(let i=0;i<256*256;i++){const v=128+(M.rnd(i)-.5)*110; d.data[i*4]=d.data[i*4+1]=d.data[i*4+2]=v; d.data[i*4+3]=255;}
    g.putImageData(d,0,0);
    M.grainEl=M.el(M.stage,`position:absolute;left:0;top:0;width:${M.W}px;height:${M.H}px;z-index:999;pointer-events:none;mix-blend-mode:overlay;opacity:${M.cfg.grain};background:url(${c.toDataURL()})`);
  }
};
M.ready = async()=>{
  await Promise.all((M.cfg.fonts||[]).map(f=>document.fonts.load(f)));   // fonts MUST be loaded before any frame
  await document.fonts.ready;
  M.init();
  await Promise.all([...document.images].map(i=>i.decode().catch(()=>0)));
  return true;
};
/* render(t, frame, rt): t = SOURCE time (after the time map), rt = real OUTPUT time */
M.render = (t,frame=0,rt)=>{
  M.RT = rt===undefined?t:rt;
  for(const s of M.scenes){
    const pad=s.def.pad??0, on=t>=s.t0-pad&&t<s.t1+pad;
    s.root.style.display=on?'block':'none';
    if(on&&s.def.update) s.def.update(t-s.t0,t,s.ctx,s.root,s);
  }
  M.globals.forEach(f=>f(t,frame));
  if(M.grainEl) M.grainEl.style.backgroundPosition=`${Math.floor(M.rnd(frame*3+1)*256)}px ${Math.floor(M.rnd(frame*7+2)*256)}px`;
};
})();
