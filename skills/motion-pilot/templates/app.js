/* APP-PROMO template: brand intro -> rotating feature chips -> phone demo with pointer click -> CTA. (Glovo / Gojek / Deliveroo family)
 * Brand colour floods are the transitions. Times are SOURCE seconds. Icons are inline SVG (no emoji font needed). */
const T=M.T,F=M.F,W=M.W,H=M.H,V=M.V,u=Math.min(W,H)/1080;
const {P,eo,ei,eio,xo,xi,xio,back,spring,lerp,clamp,tf,swap,typed}=M;
M.cfg.bg=T.bg; M.cfg.fonts=[`800 100px ${F.display}`,`500 30px ${F.body}`];
const COPY={brand:'Brandly',intro:'Introducing',lead:'Need something?',chips:['Courier','Ride','Food'],sub:'One app. Everything you need.',
  stores:['Java House','Naivas','KFC'],btn:'Place order',done:'Ordered  ✓',cta:'Order now',tag:'Fast. Reliable. Yours.',bubbles:['12 min','Free delivery','★ 4.8']};
const IC={pin:(s,c)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z" fill="${c}"/><circle cx="12" cy="10" r="2.6" fill="#fff"/></svg>`,
 bag:(s,c)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24"><rect x="4" y="8" width="16" height="13" rx="3" fill="${c}"/><path d="M8 8V7a4 4 0 0 1 8 0v1" stroke="${c}" stroke-width="2" fill="none"/></svg>`,
 car:(s,c)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24"><path d="M3 14l2-6h14l2 6v5H3z" fill="${c}"/><circle cx="7.5" cy="19" r="2" fill="#fff" stroke="${c}" stroke-width="1.5"/><circle cx="16.5" cy="19" r="2" fill="#fff" stroke="${c}" stroke-width="1.5"/></svg>`,
 bike:(s,c)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24"><circle cx="6" cy="16" r="3.5" fill="none" stroke="${c}" stroke-width="2"/><circle cx="18" cy="16" r="3.5" fill="none" stroke="${c}" stroke-width="2"/><path d="M6 16l4-8h5l3 8M10 8l3 8" stroke="${c}" stroke-width="2" fill="none"/></svg>`};
const ICONS=[IC.bike,IC.car,IC.bag];
const DCSS=`font-family:${F.display};font-weight:800;letter-spacing:-0.03em`;
const circ=(root,lt,x,y,dur=.45)=>{const p=xio(P(lt,0,dur));root.style.clipPath=p>=1?'none':`circle(${p*Math.hypot(W,H)}px at ${x}px ${y}px)`;return p;};

M.scene('intro',0,2.0,{pad:.4,
 build(root,c){
  root.style.background=T.brand; c.L=Math.round(210*u);
  c.t1=C.text(root,{text:COPY.intro,y:H*.17,size:Math.round(56*u),weight:600,font:F.body,color:T.brandInk,ls:0});
  c.logo=C.card(root,{w:c.L,h:c.L,radius:c.L*.28,bg:T.brandInk,shadow:'0 30px 60px rgba(0,0,0,.25)',html:`<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center">${IC.pin(c.L*.55,T.brand)}</div>`});
  c.name=C.text(root,{y:H*.60,size:Math.round(112*u),font:F.display,weight:800,color:T.brandInk});
 },
 update(lt,t,c){
  tf(c.logo.el,{x:(W-c.L)/2,y:H*.40-c.L/2,s:Math.max(0,back(P(lt,.25,.75),2.2)),rz:(1-eo(P(lt,.25,.8)))*-20});
  c.t1.tf(swap(P(lt,0,.3),P(lt,1.7,1.85))); c.name.set(typed(COPY.brand,lt,.9,.07));
 }});
M.cue(.3,'pop'); M.cueTyping(.9,COPY.brand.length,.07,.8); M.cue(1.6,'whoosh');

M.scene('chips',1.7,4.6,{pad:.3,
 build(root,c){
  c.bg=C.bg(root,{css:`linear-gradient(180deg,${T.bg2},${T.bg})`});
  c.lead=C.text(root,{text:COPY.lead,y:H*(V?.27:.2),size:Math.round(96*u),font:F.display,weight:800,color:T.ink});
  c.chips=COPY.chips.map((l,i)=>C.pill(root,{label:l,icon:ICONS[i](Math.round(78*u),T.surfaceInk),bg:T.surface,color:T.surfaceInk,size:Math.round(74*u),font:F.display,weight:800,px:Math.round(56*u),py:Math.round(34*u),gap:Math.round(24*u)}));
  c.sub=C.text(root,{text:COPY.sub,y:H*(V?.62:.68),size:Math.round(44*u),weight:500,font:F.body,color:T.mute,ls:0});
 },
 update(lt,t,c,root){
  circ(root,lt,W/2,H*.40); c.bg.update(lt); c.lead.tf(swap(P(lt,.25,.5),0));
  c.chips.forEach((ch,i)=>{const s0=.6+i*.85,pin=P(lt,s0,s0+.25),pout=i<2?P(lt,s0+.7,s0+.85):0,sw=swap(pin,pout,{dist:70});
    ch.tf({x:(W-ch.w())/2,y:H*(V?.44:.46)-ch.h()/2+sw.dy,b:sw.b,o:sw.o,s:lerp(.9,1,eo(pin))});});
  c.sub.tf(swap(P(lt,2.0,2.3),0,{dist:30}));
 }});
for(let i=0;i<3;i++) M.cue(2.3+i*.85,'swap'); M.cue(1.72,'whoosh');

const UI=pw=>`<div style="width:286px;height:626px;transform:scale(${(pw-24)/286});transform-origin:0 0;font-family:${F.body};color:#111;padding:50px 16px 0;box-sizing:border-box;background:#F6F6F8;position:relative">
 <div style="font-weight:800;font-size:19px;font-family:${F.display}">Select the store</div>
 ${COPY.stores.map((s,i)=>`<div style="margin-top:10px;background:#fff;border-radius:16px;padding:12px;display:flex;align-items:center;gap:12px;${i==0?'outline:2px solid '+T.accent:''}"><div style="width:34px;height:34px;border-radius:50%;background:${T.accent};display:flex;align-items:center;justify-content:center">${IC.bag(18,'#111')}</div><div style="flex:1;font-weight:700;font-size:14px">${s}</div><div style="font-size:12px;color:#666">★ 4.${8-i}</div></div>`).join('')}
 <div id="btn" style="position:absolute;left:16px;right:16px;bottom:34px;height:50px;border-radius:25px;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px">${COPY.btn}</div></div>`;
M.scene('demo',4.3,7.1,{pad:.3,
 build(root,c){
  c.bg=C.bg(root,{css:`linear-gradient(180deg,${T.bg},${T.bg2})`});
  c.disc=M.el(root,`position:absolute;left:0;top:0;border-radius:50%;background:${T.brand}`);
  c.pw=Math.round((V?380:340)*u); c.ph=C.phone(root,{w:c.pw,bg:'#F6F6F8',html:UI(c.pw)}); c.btn=c.ph.screen.querySelector('#btn');
  c.ptr=C.pointer(root,{ripple:T.accent}); c.bub=COPY.bubbles.map(b=>C.pill(root,{label:b,bg:T.surface,color:T.surfaceInk,size:Math.round(32*u),font:F.display,weight:800,px:Math.round(26*u),py:Math.round(16*u)}));
 },
 update(lt,t,c,root){
  c.bg.update(lt); const cx=W/2, cy=V?H*.5:H*.52, D=Math.round((V?900:760)*u);
  const dk=Math.max(0,back(P(lt,0,.6),1.3)); c.disc.style.width=c.disc.style.height=D+'px'; tf(c.disc,{x:cx-D/2,y:cy-D/2,s:dk});
  const pin=Math.max(0,back(P(lt,.15,.75),1.5)); tf(c.ph.el,{x:cx-c.ph.w/2,y:cy-c.ph.h/2+(1-pin)*H*.5,s:1});
  const sc=(c.pw-24)/286, bx=cx-c.ph.w/2+12+143*sc, by=cy-c.ph.h/2+12+567*sc;
  const m=eio(P(lt,.9,1.65)), px=lerp(W*.82,bx,m), py=lerp(H*.92,by,m), press=P(lt,1.7,1.8)-P(lt,1.8,1.95)*.9, rip=P(lt,1.75,2.25);
  c.ptr.at(px,py,Math.max(0,press),rip);
  const clicked=lt>1.8; c.btn.style.background=clicked?T.accent:'#111'; c.btn.style.color=clicked?'#111':'#fff'; c.btn.innerHTML=clicked?COPY.done:COPY.btn;
  const pos=V?[[W*.06,H*.28],[W*.60,H*.22],[W*.56,H*.78]]:[[cx-D*.58,cy-D*.28],[cx+D*.34,cy-D*.42],[cx+D*.40,cy+D*.30]];
  c.bub.forEach((b,i)=>{const s0=.8+i*.18,k=Math.max(0,back(P(lt,s0,s0+.4),2.2)); b.tf({x:pos[i][0],y:pos[i][1]+Math.sin(lt*2.4+i*2)*8,s:k,o:clamp(P(lt,s0,s0+.1))});});
 }});
M.cue(4.5,'swap'); M.cue(4.9,'pop'); M.cue(5.95,'click'); M.cue(6.05,'ding'); for(let i=0;i<3;i++) M.cue(5.1+i*.18,'pop',{gain:.7});

M.scene('cta',6.9,8.9,{pad:0,
 build(root,c){
  root.style.background=T.brandInk; const S=Math.round(120*u);
  c.btn=C.pill(root,{label:COPY.cta,bg:T.brand,color:T.brandInk,size:S,font:F.display,weight:800,px:Math.round(90*u),py:Math.round(54*u),gap:Math.round(40*u),shadow:'0 30px 80px rgba(0,0,0,.4)'});
  c.arrow=M.el(c.btn.el,`width:${S*1.2}px;height:${S*1.2}px;border-radius:50%;background:${T.brandInk};display:flex;align-items:center;justify-content:center`,`<svg width="${S*.6}" height="${S*.6}" viewBox="0 0 24 24" fill="none" stroke="${T.brand}" stroke-width="3" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`);
  c.tag=C.text(root,{text:COPY.tag,y:H*.64,size:Math.round(54*u),weight:600,font:F.body,color:T.brand,ls:0});
 },
 update(lt,t,c,root){
  circ(root,lt,W/2,H*.5,.5); const k=Math.max(0,back(P(lt,.3,.7),1.8)); const pr=1-.05*(P(lt,1.2,1.3)-P(lt,1.3,1.45));
  c.btn.tf({x:(W-c.btn.w())/2,y:H*.44-c.btn.h()/2,s:k*pr,o:clamp(P(lt,.3,.4))}); c.tag.tf(swap(P(lt,.8,1.1),0,{dist:30}));
 }});
M.cue(6.92,'impact'); M.cue(7.25,'pop'); M.cue(8.1,'click');
