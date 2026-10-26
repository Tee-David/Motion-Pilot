(function(){
 window.LIGHT=true;
 const NAVY='#000065', MUTE='#565678';
 const bgL='radial-gradient(ellipse at 60% 40%,#ffffff 0%,#f6f5fa 55%,#ecebf3 100%)';
 const set=(id,prop,v)=>{const e=document.getElementById(id); if(e) e.style[prop]=v;};
 ['s2','s3','s5'].forEach(id=>set(id,'background',bgL));
 if(window.HERO){ ['s1','s4','s6','s7'].forEach(id=>set(id,'background',bgL)); }
 set('s7n','background','radial-gradient(circle at 50% 40%,#ffffff 0%,#f6f5fa 50%,#ecebf3 100%)');
 set('s7sweep','background','radial-gradient(ellipse 600px 400px at 50% 50%,rgba(80,80,255,.08),rgba(0,0,0,0))');
 set('s5g1','background','radial-gradient(circle,rgba(60,60,255,.16) 0%,rgba(60,60,255,.05) 40%,rgba(246,245,250,0) 70%)');
 set('s2h','color',NAVY); set('s2h','textShadow','0 0 40px #f6f5fa,0 0 20px #f6f5fa');
 ['s3tag','s7tag','s5idx'].forEach(id=>set(id,'color',MUTE));
 document.querySelectorAll('.lab').forEach(e=>e.style.color=NAVY);
 document.querySelectorAll('.desc').forEach(e=>e.style.color=MUTE);
 document.querySelectorAll('#s5prog > div').forEach(e=>e.style.background='rgba(0,0,101,.12)');
 document.querySelectorAll('.tile').forEach(e=>{e.style.boxShadow='0 18px 40px rgba(20,20,80,.14)';e.style.border='1px solid #e6e6ef'});
 document.querySelectorAll('#lock3 path[fill="#ffffff"],#lock7 path[fill="#ffffff"],#lock3 g[fill="#ffffff"],#lock7 g[fill="#ffffff"]').forEach(p=>p.setAttribute('fill',NAVY));
 set('s3ring','borderColor',NAVY);
 set('s7pill','background',NAVY); set('s7url','color','#ffffff');
 const sh=document.getElementById('hshade'); if(sh){ sh.style.background=sh.style.background.split('rgba(3, 3, 24,').join('rgba(246, 245, 250,'); }
 document.querySelectorAll('.card').forEach(e=>e.style.boxShadow='0 30px 60px rgba(20,20,80,.18)');
})();
