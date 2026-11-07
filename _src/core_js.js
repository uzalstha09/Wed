
(function(){
var $=function(i){return document.getElementById(i)},T=C.T,NE=C.lang==='ne';
function dv(s){s=String(s);return NE?s.replace(/[0-9]/g,function(d){return '०१२३४५६७८९'[d]}):s}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function cm(u){try{var x=new URL(u);if(/(^|\.)goo\.gl$/.test(x.hostname))x.search='';return x.toString()}catch(e){return u}}
var q=new URLSearchParams(location.search);
var g=(q.get('to')||q.get('name')||q.get('n')||'').replace(/[<>]/g,'').replace(/\s+/g,' ').trim().slice(0,40);
if(g){document.body.classList.add('named');$('tagn').textContent=g;$('dearn').textContent=T.dear+' '+g;$('rn').value=g}
var CFGURL='https://raw.githubusercontent.com/uzalstha09/Wed/config/config.json',KEY={j:'wedding',r:'reception'};
var BASE=JSON.parse(JSON.stringify(C.ev));
function urlOv(){C.ev.forEach(function(e){var t=(q.get(e.k+'t')||'').trim().slice(0,40),v=(q.get(e.k+'v')||'').trim().slice(0,60),m=(q.get(e.k+'m')||'').trim();if(t)e.time=t;if(v)e.venue=v;if(/^https?:\/\//i.test(m)&&!/qLXXtzq6119MEdBVA|nJAhKrkYgUaogWYY9|Rose\+Party\+Palace|0x3996842b4da06a89/.test(m))e.map=m.slice(0,600)});}
var RS='';function applyCfg(cfg){C.ev=JSON.parse(JSON.stringify(BASE));if(cfg&&typeof cfg.rsvp_url==='string'&&/^https:\/\/script\.google(usercontent)?\.com\//.test(cfg.rsvp_url))RS=cfg.rsvp_url;if(cfg)C.ev.forEach(function(e){var c=cfg[KEY[e.k]];if(!c)return;var L=NE?'ne':'en';if(typeof c.map==='string'&&/^https?:\/\//i.test(c.map))e.map=c.map;if(typeof c['time_'+L]==='string')e.time=c['time_'+L];if(typeof c['venue_'+L]==='string')e.venue=c['venue_'+L]});urlOv()}
function D(e){return new Date(e.date+'T00:00:00')}
function fd(d){return dv(d.getDate())+' '+T.months[d.getMonth()]+' '+dv(d.getFullYear())}
function render(){
var ev=$('evs');ev.className='evg rv'+(C.ev.length>1?' n2':'');
ev.innerHTML=C.ev.map(function(e){var d=D(e);return '<div class="ec"><div class="cap">'+esc(e.label)+'</div><div class="d1">'+T.wd[d.getDay()]+'<br>'+fd(d)+'</div><div class="bs">'+esc(e.bs)+'</div>'+(e.time?'<div class="tm">'+esc(e.time)+'</div>':'')+(e.venue?'<div class="vn">'+esc(e.venue)+'</div>':'')+(e.map?'<a class="lk" href="'+esc(cm(e.map))+'" rel="noopener"><svg width="9" height="12" viewBox="0 0 12 15" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6 14s5-4.6 5-8.2A5 5 0 0 0 1 5.8C1 9.4 6 14 6 14z"/><circle cx="6" cy="6" r="1.8"/></svg>'+esc(T.viewloc)+'</a>':'')+'</div>'}).join('');
if(window.fitWin)fitWin();
}
applyCfg(null);render();
try{var cc=localStorage.getItem('wcfg');if(cc){applyCfg(JSON.parse(cc));render();if(RS){var sb0=document.querySelector('#rf .send');if(sb0)sb0.textContent=T.send2}}}catch(e){}
try{fetch(CFGURL+'?t='+Math.floor(Date.now()/60000),{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(cfg){if(!cfg)return;try{localStorage.setItem('wcfg',JSON.stringify(cfg))}catch(e){}applyCfg(cfg);render();if(RS){var sb=document.querySelector('#rf .send');if(sb)sb.textContent=T.send2}}).catch(function(){})}catch(e){}
var tgt=D(C.ev[0]);
$('cd').innerHTML=T.units.map(function(u){return '<div><b>00</b><span>'+esc(u)+'</span></div>'}).join('');
window.fitWin=function(){var w=$('win');if(!w)return;w.style.transform='none';var vw=Math.min(innerWidth,460),k=Math.min(1,innerHeight*.84/w.offsetHeight,vw*.80/w.offsetWidth);w.style.transform='scale('+k.toFixed(3)+')'};fitWin();addEventListener('resize',fitWin);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fitWin);
var rm=$('rmodal');$('ropen').onclick=function(){rm.classList.add('on');rm.setAttribute('aria-hidden','false')};function rcl(){rm.classList.remove('on');rm.setAttribute('aria-hidden','true')}$('rclose').onclick=rcl;rm.addEventListener('click',function(e){if(e.target===rm)rcl()});
var cb=$('cd').querySelectorAll('b');
function tick(){var s=Math.max(0,Math.floor((tgt-new Date())/1000)),v=[Math.floor(s/86400),Math.floor(s%86400/3600),Math.floor(s%3600/60),s%60];for(var i=0;i<4;i++)cb[i].textContent=dv(String(v[i]).padStart(2,'0'))}
tick();setInterval(tick,1000);
function wa(){var n=($('rn').value||g||'').trim();$('wa').href='https://wa.me/'+C.wa+(n?'?text='+encodeURIComponent(T.wamsg.replace('{n}',n)):'')}
wa();$('rn').addEventListener('input',wa);
$('rf').addEventListener('submit',function(ev){ev.preventDefault();var f=this,b=f.querySelector('.send'),m=$('rmsg');
 for(var i=0;i<C.ev.length;i++){if(!f.querySelector('input[name="attend-'+C.ev[i].k+'"]:checked')){m.textContent=T.need;return}}
 var n=($('rn').value||'').trim();if(!n){$('rn').focus();return}
 var lines=[T.rsvpw+' — '+n];C.ev.forEach(function(e){var v=f.querySelector('input[name="attend-'+e.k+'"]:checked').value;lines.push(e.label+': '+(v==='yes'?T.yesw:T.now))});lines.push(T.gw+': '+dv($('rg').value));
 if(RS){var body=new URLSearchParams();body.append('name',n);C.ev.forEach(function(e){body.append('attend-'+e.k,f.querySelector('input[name="attend-'+e.k+'"]:checked').value)});body.append('guests',$('rg').value);body.append('page',location.pathname);body.append('lang',C.lang);if(g)body.append('link-name',g);
  b.disabled=true;var old=b.textContent;b.textContent=T.sending2;m.textContent='';
  fetch(RS,{method:'POST',mode:'no-cors',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body.toString()}).then(function(){m.textContent=T.ok2;f.querySelectorAll('input,select,button').forEach(function(x){x.disabled=true});b.textContent='✓'}).catch(function(){m.textContent=T.err;b.disabled=false;b.textContent=old});return}
 m.textContent=T.ok;location.href='https://wa.me/'+C.wa+'?text='+encodeURIComponent(lines.join('\n'))});
/* reveal */
var secs=document.querySelectorAll('.sec');
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.2}):null;
/* scroll-linked lace trims (parallax) */
var trims=[].slice.call(document.querySelectorAll('.trim')),tk=false;
function par(){tk=false;var vh=innerHeight;trims.forEach(function(t){var r=t.parentNode.getBoundingClientRect(),p=(r.top+r.height/2-vh/2)/vh;var y=Math.max(-1,Math.min(1,p))*10;t.style.transform=(t.classList.contains('bt')?'scaleY(-1) ':'')+'translate3d(0,'+(t.classList.contains('bt')?-y:y).toFixed(1)+'px,0)'})}
addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(par)}},{passive:true});
/* sound */
var ac=null;function whoosh(){try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();var t0=ac.currentTime;
 var n=ac.sampleRate*.08,bf=ac.createBuffer(1,n,ac.sampleRate),d=bf.getChannelData(0);for(var i=0;i<n;i++){var k=i/n;d[i]=(Math.random()*2-1)*Math.pow(1-k,4)}
 var s=ac.createBufferSource();s.buffer=bf;var hp=ac.createBiquadFilter();hp.type='highpass';hp.frequency.value=1500;var g1=ac.createGain();g1.gain.value=.55;s.connect(hp);hp.connect(g1);g1.connect(ac.destination);s.start(t0);
 var n2=ac.sampleRate*1.4,b2=ac.createBuffer(1,n2,ac.sampleRate),d2=b2.getChannelData(0);for(var i=0;i<n2;i++)d2[i]=Math.random()*2-1;
 var s2=ac.createBufferSource();s2.buffer=b2;var bp=ac.createBiquadFilter();bp.type='bandpass';bp.Q.value=.7;bp.frequency.setValueAtTime(500,t0+.15);bp.frequency.exponentialRampToValueAtTime(2200,t0+1.1);var g2=ac.createGain();g2.gain.setValueAtTime(0,t0+.15);g2.gain.linearRampToValueAtTime(.12,t0+.6);g2.gain.linearRampToValueAtTime(0,t0+1.5);s2.connect(bp);bp.connect(g2);g2.connect(ac.destination);s2.start(t0+.15)}catch(e){}}
/* music */
var bgm=$('bgm'),mute=$('mute'),muted=false;
if(bgm){mute.classList.add('on');mute.onclick=function(e){e.stopPropagation();muted=!muted;bgm.muted=muted;mute.textContent=muted?'×':'♪';if(!muted&&bgm.paused)bgm.play().catch(function(){})}}
function startMusic(){if(bgm&&!muted&&bgm.paused){bgm.volume=.5;bgm.play().catch(function(){})}}
['pointerdown','touchstart','keydown'].forEach(function(t){addEventListener(t,function(){startMusic()},{once:true,passive:true})});
