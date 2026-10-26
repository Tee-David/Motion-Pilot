/* KINETIC-TYPE template: words scatter & assemble (+confetti) -> highlight-box word swap -> card fan -> wordmark with blinking underscore cursor.
 * (personal-brand / portfolio / Zapier-Pinterest word-beat family; also the base for poster-duotone and brand-flood). Times are SOURCE seconds. */
const T=M.T,F=M.F,W=M.W,H=M.H,V=M.V,u=Math.min(W,H)/1080;
const {P,eo,ei,eio,xo,xi,xio,back,spring,lerp,clamp,tf,swap,typed,rnd}=M;
M.cfg.bg=T.bg; M.cfg.fonts=[`800 100px ${F.display}`,`500 30px ${F.body}`];
const COPY={lines:['I bring','ideas','to life'],pre:'Thousands of',box:['Inspirations','Motion','Brands','Ideas'],post:'is here',
  cards:['Brand','Web','Motion'],capt:'Made to be noticed.',word:'yourbrand',url:'yourbrand.com'};
const DCSS=`font-family:${F.display};font-weight:800;letter-spacing:-0.035em;white-space:pre`;

M.scene('words',0,3.4,{pad:.3,
 build(root,c){
  root.style.background=T.bg; const sz=[150,330,150].map(s=>Math.round(s*u)); const widest=M.measure(COPY.lines[1],DCSS+`;font-size:${sz[1]}px`);
  const k=Math.min(1,W*.86/widest); c.sz=sz.map(s=>Math.round(s*k)); c.lines=[]; c.spans=[];
  let y=H/2-(c.sz[0]*1.05+c.sz[1]*.95+c.sz[2]*1.05)/2;
  COPY.lines.forEach((l,i)=>{const t=C.text(root,{y,size:c.sz[i],font:F.display,weight:800,color:i==1?T.accent:T.ink,lh:1,text:''}); c.spans.push(M.words(t.el,l)); c.lines.push(t); y+=c.sz[i]*(i==1?.95:1.05);});
  c.conf=C.confetti(root,{x:W/2,y:H/2,n:46,speed:1100*u,colors:[T.accent,T.ink,T.mute,'#FFB020','#4D7CFE']});
 },
 update(lt,t,c){
  let n=0; c.spans.forEach((sp,li)=>sp.forEach((s,wi)=>{const i=n++, k=back(P(lt,-.25+i*.14,.4+i*.14),1.25), q=1-clamp(k,0,1.2);
    tf(s,{x:(rnd(i+1)-.5)*W*.9*q,y:(rnd(i+7)-.5)*H*.8*q,rz:(rnd(i+3)-.5)*60*q,s:lerp(.6,1,clamp(k,0,1.1)),o:clamp(P(lt,-.25+i*.14,-.05+i*.14)),b:Math.abs(q)*10});}));
  c.conf.update(lt-1.0);
  c.lines.forEach((l,i)=>l.tf(swap(1,P(lt,2.8+i*.05,3.0+i*.05),{dist:50})));  // leave before the next scene's ground arrives
 }});
M.cue(.15,'whoosh'); M.cue(.85,'riser',{gain:.5}); M.cue(1.05,'impact'); M.cue(1.05,'pop'); M.cue(2.85,'swap');

M.scene('swapbox',3.0,5.8,{pad:0,
 build(root,c){
  root.style.background=T.bg2; c.fs=Math.round(120*u);
  const css=DCSS+`;font-size:${c.fs}px`; c.wp=M.measure(COPY.pre,css)+c.fs*.3; c.pad=c.fs*.3;
  c.wb=COPY.box.map(b=>M.measure(b,css)+2*c.pad); const maxTot=c.wp+Math.max(...c.wb); if(maxTot>W*.9){c.fs=Math.floor(c.fs*W*.9/maxTot);}
  const css2=DCSS+`;font-size:${c.fs}px`; c.wp=M.measure(COPY.pre,css2)+c.fs*.3; c.pad=c.fs*.3; c.wb=COPY.box.map(b=>M.measure(b,css2)+2*c.pad);
  c.pre=C.text(root,{text:COPY.pre,size:c.fs,font:F.display,weight:800,color:T.ink,align:'left',w:W});
  c.box=M.el(root,`position:absolute;left:0;top:0;height:${c.fs*1.25}px;background:${T.accent};border-radius:${c.fs*.18}px;overflow:hidden`);
  c.words=COPY.box.map(b=>M.el(c.box,`position:absolute;left:0;top:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-family:${F.display};font-weight:800;font-size:${c.fs}px;letter-spacing:-0.035em;color:${T.brandInk};white-space:nowrap`,b));
  c.post=C.text(root,{text:COPY.post,y:H/2+c.fs*.3,size:c.fs,font:F.display,weight:800,color:T.ink,w:W});
 },
 update(lt,t,c){
  const sw=[.45,1.2,1.95]; let idx=0; sw.forEach((s,i)=>{if(lt>=s) idx=i+1;});
  let wcur=c.wb[0]; sw.forEach((s,i)=>{const e=eio(P(lt,s-.05,s+.3)); if(e>0) wcur=lerp(c.wb[i],c.wb[i+1],e);});
  const tot=c.wp+wcur, x0=(W-tot)/2, y=H/2-c.fs*1.05;
  c.pre.tf({x:x0,y:y-0+0,...swap(P(lt,0,.25),P(lt,2.6,2.75),{dist:40}),o:clamp(P(lt,0,.2))*(1-P(lt,2.6,2.75))});
  c.box.style.width=wcur+'px'; tf(c.box,{x:x0+c.wp,y:y+c.fs*.03,s:Math.max(0,back(P(lt,.05,.4),1.5)),o:1-P(lt,2.6,2.75)});
  c.words.forEach((w,i)=>{const s=i==0?.0:sw[i-1], pin=i==0?P(lt,.1,.35):P(lt,s,s+.22), pout=i<c.words.length-1?P(lt,sw[i],sw[i]+.12):0; tf(w,swap(pin,pout,{dist:40,blur:10}));});
  c.post.tf(swap(P(lt,.3,.55),P(lt,2.6,2.75),{dist:40}));
 }});
M.cue(3.1,'pop'); M.cue(3.45,'swap'); M.cue(4.2,'swap'); M.cue(4.95,'swap');

M.scene('cards',5.6,7.7,{pad:.3,
 build(root,c){
  root.style.background=T.bg; const cw=Math.round((V?420:380)*u), ch=Math.round(cw*1.3);
  const grads=[`linear-gradient(135deg,${T.accent},${T.mute})`,`linear-gradient(135deg,${T.ink},${T.mute})`,`linear-gradient(135deg,${T.mute},${T.accent})`];
  c.cw=cw; c.ch=ch; c.cards=COPY.cards.map((l,i)=>C.card(root,{w:cw,h:ch,radius:36*u,bg:grads[i%3],shadow:'0 40px 80px rgba(0,0,0,.28)',
    html:`<div style="padding:${34*u}px;font-family:${F.display};font-weight:800;font-size:${72*u}px;color:${i==1?T.bg:'#fff'};letter-spacing:-0.03em">${l}</div>`}));
  c.capt=C.text(root,{text:COPY.capt,y:H*(V?.78:.80),size:Math.round(72*u),font:F.display,weight:800,color:T.ink});
 },
 update(lt,t,c){
  const cx=W/2, cy=V?H*.45:H*.44;
  c.cards.forEach((cd,i)=>{const o=i-1,k=Math.max(0,back(P(lt,.1+i*.1,.7+i*.1),1.4)),fan=eo(P(lt,.5,1.1));
    cd.tf({x:cx-c.cw/2+o*c.cw*.62*fan,y:cy-c.ch/2+(1-k)*H*.7+Math.abs(o)*26*fan,rz:o*9*fan,o:clamp(P(lt,.1+i*.1,.25+i*.1)),s:k>0?1:0,zi:10-Math.abs(o)});});
  c.capt.tf(swap(P(lt,1.0,1.3),P(lt,1.85,1.98),{dist:40}));
 }});
for(let i=0;i<3;i++) M.cue(5.75+i*.1,'pop',{gain:.7}); M.cue(5.65,'whoosh');

M.scene('wordmark',7.5,9.6,{pad:0,
 build(root,c){
  root.style.background=T.brand; c.S=M.fit(COPY.word+'_',DCSS,W*.82,Math.round(200*u)); const css=DCSS+`;font-size:${c.S}px`; c.w=M.measure(COPY.word+'_',css); c.css=css;
  c.t=C.text(root,{x:(W-c.w)/2,w:c.w+40,align:'left',y:H*.40,size:c.S,font:F.display,weight:800,color:T.brandInk,text:''});
  c.cur=C.bar(root,{color:T.accent==T.brand?T.brandInk:T.accent,w:c.S*.5,}); c.url=C.text(root,{text:COPY.url,y:H*.40+c.S*1.35,size:Math.round(48*u),weight:500,font:F.body,color:T.brandInk,ls:0});
 },
 update(lt,t,c,root){
  const p=xio(P(lt,0,.5)); root.style.clipPath=p>=1?'none':`circle(${p*Math.hypot(W,H)}px at ${W/2}px ${H/2}px)`;
  const s=typed(COPY.word,lt,.5,.06); c.t.set(s); const x=(W-c.w)/2+M.measure(s,c.css);
  const typing=s.length<COPY.word.length; c.cur.el.style.height=(c.S*.12)+'px'; c.cur.el.style.display=(lt>.45&&(typing||M.blink()))?'block':'none'; tf(c.cur.el,{x:x+c.S*.04,y:H*.40+c.S*.9});
  c.url.tf(swap(P(lt,1.1,1.4),0,{dist:30}));
 }});
M.cue(7.52,'impact'); M.cueTyping(8.0,COPY.word.length,.06,.8); M.cue(8.7,'ding');
