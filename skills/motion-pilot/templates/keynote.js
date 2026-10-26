/* KEYNOTE template: hook (typed + cursor) -> chaos (orbiting problems implode) -> product (3D phone + counter) -> end (brand flood + URL).
 * Replace COPY, keep the structure. Times are SOURCE seconds. Sound cues are declared next to the animation. */
const T=M.T,F=M.F,W=M.W,H=M.H,V=M.V,u=Math.min(W,H)/1080;
const {P,eo,ei,eio,xo,xi,xio,back,lerp,clamp,tf,swap,typed}=M;
M.cfg.bg=T.bg; M.cfg.fonts=[`700 100px ${F.display}`,`500 30px ${F.body}`];
/* No invented numbers: stat stays 0 until the client gives a real figure (facts.md). */
const COPY={hook1:'What if your brand',hook2:['made itself?','sold itself?'],chaos:'Five vendors. One headache.',
  tiles:['Designer','Developer','SEO guy','Social manager','Ads manager','Copywriter','Photographer','Printer','Hosting','Another WhatsApp group'],
  stat:'0+',statLabel:'[CLIENT TO CONFIRM] a real figure',end:'Your Brand',url:'yourbrand.com'};
const DCSS=`font-family:${F.display};font-weight:700;letter-spacing:-0.035em;white-space:pre`;
const GRAD=`radial-gradient(ellipse at 50% 50%,${T.bg2} 0%,${T.bg} 72%)`, SH={wipe:{x:W/2,y:H/2}};
const reveal=(root,lt,o,dur=.45)=>{const p=xio(P(lt,0,dur));root.style.clipPath=p>=1?'none':`circle(${p*Math.hypot(W,H)}px at ${o.x}px ${o.y}px)`;return p;};

M.scene('hook',0,2.7,{pad:.5,
 build(root,c){
  c.bg=C.bg(root,{css:GRAD}); const S0=Math.round(136*u), chev='&gt;&nbsp;';
  const cand=[COPY.hook1,...COPY.hook2.map(s=>chev+s)];
  const widest=cand.reduce((a,b)=>M.measure(a,DCSS+`;font-size:${S0}px`)>M.measure(b,DCSS+`;font-size:${S0}px`)?a:b);
  c.S=M.fit(widest,DCSS,W*.84,S0); const css=DCSS+`;font-size:${c.S}px`, w=s=>M.measure(s,css);
  c.w1=w(COPY.hook1); c.w2=COPY.hook2.map(s=>w(chev+s)); c.css=css; c.y0=H/2-c.S*1.1;
  const base={size:c.S,font:F.display,color:T.ink,align:'left',lh:1.1,w:W};
  c.r1=C.text(root,{...base,x:(W-c.w1)/2,y:c.y0});
  c.r2=COPY.hook2.map((s,i)=>C.text(root,{...base,x:(W-c.w2[i])/2,y:c.y0+c.S*1.1,text:`<span style="color:${T.accent}">${chev}</span>${s}`}));
  c.cur=C.bar(root,{color:T.accent,w:Math.max(8,c.S*.09)});
  SH.wipe={x:(W+c.w2[1])/2,y:c.y0+c.S*1.1+c.S*.5};
 },
 update(lt,t,c){
  c.bg.update(lt); const chev=`<span style="color:${T.accent}">&gt;&nbsp;</span>`;
  const s1=typed(COPY.hook1,lt,.2,.045); c.r1.set(s1);
  const s2=typed(COPY.hook2[0],lt,1.0,.04); c.r2[0].set(chev+s2);
  const out=P(lt,1.84,1.94); c.r2[0].tf({o:lt>=1.0?1-out:0,y:-M.ei(out)*50,b:M.ei(out)*14});
  c.r2[1].tf(swap(P(lt,1.9,2.12),0));
  let x,y; const rowY=c.y0+(lt<1.0?0:c.S*1.1)+c.S*.12;
  if(lt<1.0){x=(W-c.w1)/2+M.measure(s1,c.css);}
  else if(lt<1.9){x=(W-c.w2[0])/2+M.measure('&gt;&nbsp;'+s2,c.css);}
  else{x=(W+c.w2[1])/2-c.S*.15;}
  const typing=lt<(.2+COPY.hook1.length*.045)||(lt>1&&lt<1+COPY.hook2[0].length*.04+.05);
  c.cur.at(x+c.S*.04,rowY,c.S*.86,lt<2.3&&(typing||M.blink()));
 }});
M.cueTyping(.2,COPY.hook1.length,.045,.9); M.cueTyping(1.0,COPY.hook2[0].length,.04,.9); M.cue(1.9,'swap'); M.cue(2.38,'whoosh');

M.scene('chaos',2.4,5.3,{pad:.2,
 build(root,c){
  c.bg=C.bg(root,{css:GRAD,blobs:[{c:'rgba(36,36,180,.35)',x:.75,y:.2,r:.5},{c:'rgba(20,20,130,.3)',x:.2,y:.8,r:.45}]});
  const fs=Math.round(36*u);
  c.orb=C.orbit(root,{items:COPY.tiles.map(l=>({w:Math.round(l.length*fs*.52+90*u),h:Math.round(fs*2.1),
    html:`<div style="width:100%;height:100%;border-radius:999px;background:${T.surface};color:${T.surfaceInk};display:flex;align-items:center;justify-content:center;font-family:${F.body};font-weight:500;font-size:${fs}px;box-shadow:0 18px 40px rgba(0,0,0,.35);white-space:nowrap">${l}</div>`})),
    cx:W/2,cy:H/2,rx:W*(V?.34:.40),ry:H*(V?.33:.30),jit:12});
  c.size=M.fit(COPY.chaos,DCSS,W*.82,Math.round(104*u));
  c.title=C.text(root,{text:COPY.chaos,y:H/2-c.size*.6,size:c.size,font:F.display,color:T.ink,w:W,lh:1.1});
  c.ring=M.el(root,`position:absolute;left:0;top:0;border-radius:50%;border:${8*u}px solid ${T.accent};display:none;z-index:60`);
 },
 update(lt,t,c,root){
  c.bg.update(lt); const o=SH.wipe,R=Math.hypot(W,H),p=reveal(root,lt,o);
  c.ring.style.display=p>0&&p<1?'block':'none'; c.ring.style.width=c.ring.style.height=(2*p*R+8)+'px'; tf(c.ring,{x:o.x-p*R-4,y:o.y-p*R-4});
  const coll=xi(P(lt,1.95,2.45)); c.orb.update(lt*.32+.4,{coll,blur:5});
  c.title.tf(swap(P(lt,.3,.5),P(lt,1.85,1.98)));
 }});
for(let i=0;i<COPY.tiles.length;i++) M.cue(2.7+i*.12,'pop',{gain:.6}); M.cue(4.3,'riser'); M.cue(4.85,'impact');

const UI=pw=>`<div style="width:286px;height:626px;transform:scale(${(pw-24)/286});transform-origin:0 0;font-family:${F.body};color:#0e0e2c;padding:48px 14px 0;box-sizing:border-box">
 <div style="font-weight:700;font-size:20px;font-family:${F.display}">Overview</div>
 <div style="margin-top:10px;background:${T.accent};color:#fff;border-radius:18px;padding:16px"><div style="font-size:11px;opacity:.9">This month</div><div style="font-size:32px;font-weight:700;font-family:${F.display}">+00%</div>
 <svg width="230" height="46" viewBox="0 0 230 46"><path d="M0 40 C30 38 40 20 70 24 S120 10 150 14 S200 4 230 2" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/></svg></div>
 ${[1,2,3,4].map(i=>`<div style="margin-top:10px;background:#fff;border-radius:14px;padding:13px;display:flex;justify-content:space-between;font-size:12px"><span>Campaign ${i}</span><b>${i*37+12}%</b></div>`).join('')}</div>`;
M.scene('product',4.9,7.3,{pad:.3,
 build(root,c){
  root.style.perspective='1800px';
  c.bg=C.bg(root,{css:GRAD,blobs:[{c:'rgba(36,36,180,.35)',x:.8,y:.25,r:.5},{c:'rgba(20,20,130,.3)',x:.15,y:.85,r:.4}]});
  const pw=Math.round((V?340:360)*u); c.ph=C.phone(root,{w:pw,bg:'#EEF0F6',html:UI(pw)});
  c.num=parseInt(COPY.stat); c.suf=COPY.stat.replace(/^\d+/,''); const ts=Math.round((V?210:260)*u);
  const L=V?{x:0,w:W,al:'center'}:{x:W*.07,w:W*.46,al:'left'}, y0=V?H*.12:H*.34;
  c.stat=C.text(root,{x:L.x,y:y0,w:L.w,align:L.al,size:ts,font:F.display,color:T.ink});
  c.lab=C.text(root,{x:L.x,y:y0+ts*1.1,w:L.w,align:L.al,size:Math.round(46*u),weight:500,font:F.body,color:T.mute,ls:0,text:COPY.statLabel});
 },
 update(lt,t,c){
  c.bg.update(lt); const cx=V?W/2:W*.70, cy=V?H*.66:H*.52, pin=back(P(lt,.1,.7),1.3);
  tf(c.ph.el,{x:cx-c.ph.w/2,y:cy-c.ph.h/2+(1-pin)*H*.6,ry:-14+Math.sin(lt*1.4)*2,rx:6,rz:-3,o:clamp(P(lt,.1,.25))});
  c.stat.set(Math.round(c.num*eo(P(lt,.35,1)))+c.suf); c.stat.tf(swap(P(lt,.25,.45),0)); c.lab.tf(swap(P(lt,.4,.6),0,{dist:30}));
 }});
M.cue(5.0,'whoosh'); M.cue(5.5,'ding'); 

M.scene('end',6.9,9.4,{
 build(root,c){
  root.style.background=T.brand; const S=M.fit(COPY.end,DCSS,W*.8,Math.round(190*u));
  c.name=C.text(root,{text:COPY.end,y:H*.36,size:S,font:F.display,color:T.brandInk});
  c.pill=C.pill(root,{label:'x',bg:T.surface,color:T.surfaceInk,size:Math.round(44*u),font:F.display,weight:600,py:Math.round(24*u),px:Math.round(52*u),shadow:'0 24px 60px rgba(0,0,0,.3)'});
 },
 update(lt,t,c,root){
  reveal(root,lt,{x:W/2,y:H/2},.5); c.name.tf(swap(P(lt,.4,.65),0));
  const s=typed(COPY.url,lt,.9,.035), cur=(s.length<COPY.url.length||M.blink())?`<span style="display:inline-block;width:.09em;height:.85em;background:${T.accent};margin-left:.08em;vertical-align:-.05em"></span>`:'';
  c.pill.set(s+cur); const k=Math.max(0,back(P(lt,.85,1.15),1.8));
  c.pill.tf({x:(W-c.pill.w())/2,y:H*.6,s:k,o:clamp(P(lt,.85,.95))});
 }});
M.cue(6.92,'impact'); M.cue(7.3,'ding'); M.cueTyping(7.8,COPY.url.length,.035,.7);
