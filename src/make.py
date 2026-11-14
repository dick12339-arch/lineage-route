import re, json, urllib.parse, sys
src = open(sys.argv[1], encoding='utf-8').read()
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
body = re.search(r'</style>(.*?)<script>', src, re.S).group(1)
js = re.search(r'<script>(.*?)</script>', src, re.S).group(1)
js_bm = js  # 主程式放在網路上，不受書籤長度限制，保留怪物圖示

# ---- 1) 離線版網頁 ----
standalone = ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
  '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
  + src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
       .replace('<title>亞丁大陸路線指引</title>','<title>亞丁大陸路線指引</title>',1)
  .split('<div class="wrap">')[0]
  + '<style>body{margin:0}[hidden]{display:none!important}</style></head><body><div class="wrap">'
  + src.split('<div class="wrap">',1)[1] + '</body></html>')
open('天堂路線指引.html','w',encoding='utf-8').write(standalone)

# ---- 2) 書籤小工具 v1.3（豎版底部抽屜＋可自由調高度）----
c = css.replace(':root{', ':host{').replace('html,body{', '.l1body{').replace('\nbody{', '\n.l1body{')
c = c.replace('@media (max-aspect-ratio:1/1),(max-width:820px){', '@container l1 (max-width:820px){')
c += """
[hidden]{display:none!important}
.fab{position:fixed;right:calc(16px + env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));width:52px;height:52px;border-radius:50%;
 border:2px solid #1a140a;background:var(--gold);color:#1a140a;font:700 22px/1 var(--f-display);cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.55);touch-action:none;user-select:none;z-index:3}
.fab:focus-visible{outline:3px solid var(--tele);outline-offset:3px}
.win{position:fixed;right:calc(20px + env(safe-area-inset-right,0px));bottom:calc(84px + env(safe-area-inset-bottom,0px));width:440px;height:min(78vh,760px);
 min-width:280px;max-width:calc(100vw - 8px);max-height:calc(100vh - 8px);display:flex;flex-direction:column;background:var(--bg);color:var(--ink);
 border:1px solid var(--gold);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.6);overflow:hidden;resize:both;z-index:2;font-family:var(--f-body);transition:opacity .15s}
.win.sheet{left:0!important;right:0!important;top:auto!important;bottom:0!important;width:auto;max-width:none;min-width:0;border-radius:12px 12px 0 0;border-bottom:0;resize:none;padding-bottom:env(safe-area-inset-bottom,0px)}
.win.ghost{opacity:.4}
.win.ghost .win-c{pointer-events:none}
.bar{position:relative;display:flex;align-items:center;justify-content:space-between;gap:6px;padding:8px 6px 6px 12px;background:var(--panel);border-bottom:1px solid var(--line);cursor:move;touch-action:none;user-select:none;flex:none}
.win.sheet .bar{cursor:ns-resize;padding-top:14px}
.win.sheet .bar::before{content:"";position:absolute;top:5px;left:50%;width:44px;height:4px;margin-left:-22px;border-radius:2px;background:var(--mute);opacity:.7}
.bar b{font-family:var(--f-display);color:var(--gold);letter-spacing:.06em;font-size:14px;white-space:nowrap}
.bar span{display:flex;gap:4px}
.bar button{min-width:34px;height:32px;padding:0 6px;border-radius:6px;border:1px solid var(--line);background:var(--bg);color:var(--ink);font:500 13px var(--f-body);cursor:pointer}
.bar button[aria-pressed="true"]{border-color:var(--gold);color:var(--gold)}
.win-c{flex:1;overflow:auto;container:l1/inline-size;min-height:0}
.l1body{padding-block:10px 16px}
.l1body header{display:none}
.win.nomap .mapbox{display:none}
.stepnav{display:none;align-items:center;justify-content:space-between;gap:8px}
.stepnav button{font:inherit;font-size:14px;padding:6px 14px;border-radius:5px;border:1px solid var(--line);background:var(--bg);color:var(--gold);cursor:pointer}
.stepnav button:disabled{opacity:.35}
.stepnav span{font-size:12px;color:var(--mute);font-variant-numeric:tabular-nums}
.win.compact .l1body{padding-block:6px 8px}
.win.compact .panel{gap:6px;padding:6px 8px;border:0;background:none}
.win.compact #tabRoute{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:6px}
.win.compact #tabRoute[hidden]{display:none}
.win.compact .tabs button{padding:4px;font-size:13px}
.win.compact .destmobs{display:none}
.win.compact .modes,.win.compact .summary,.win.compact .note,.win.compact .field label{display:none}
.win.compact .row{gap:4px}
.win.compact .swap{width:34px;height:38px;font-size:15px}
.win.compact select{font-size:14px;padding:7px 26px 7px 8px;background-position:calc(100% - 14px) 50%,calc(100% - 9px) 50%}
.win.compact ol.steps,.win.compact .stepnav{grid-column:1/-1}
.win.compact .stepnav{display:flex}
.win.compact ol.steps li{display:none;padding:4px 0;border:0}
.win.compact ol.steps li.cur{display:grid}
.win.compact .st-d{font-size:13px}
"""
html = ('<button class="fab" aria-label="展開天堂路線" title="天堂路線（可拖曳）">⚔</button>'
 '<div class="win" role="dialog" aria-label="天堂路線指引"><div class="bar"><b>天堂路線 v2.15</b><span>'
 '<button data-a="size" title="切換大小">小</button>'
 '<button data-a="ghost" aria-pressed="false" title="半透明，可點到後面畫面">透明</button>'
 '<button data-a="min" title="收合成按鈕" aria-label="收合">—</button>'
 '<button data-a="close" title="關閉工具" aria-label="關閉工具">✕</button></span></div>'
 '<div class="win-c"><div class="l1body">' + body + '</div></div></div>')
ui = r"""
var fab=r.querySelector('.fab'),win=r.querySelector('.win'),bar=r.querySelector('.bar'),sizeBtn=r.querySelector('[data-a=size]'),ghostBtn=r.querySelector('[data-a=ghost]');
var S={};try{S=JSON.parse(localStorage.getItem('l1fab2')||'{}')}catch(e){}
function keep(){try{localStorage.setItem('l1fab2',JSON.stringify(S))}catch(e){}}
var mq=matchMedia('(orientation:portrait) and (max-width:900px)');
function isSheet(){return mq.matches}
var MINH=150;
function presets(){var vh=innerHeight;return isSheet()?[210,Math.round(vh*.48),Math.round(vh*.86)]:[220,Math.round(Math.min(vh*.62,560)),Math.round(Math.min(vh*.9,820))]}
function clampH(hh){return Math.max(MINH,Math.min(hh,innerHeight-(isSheet()?40:16)))}
function setH(hh){win.style.height=clampH(hh)+'px';classify()}
function classify(){var hh=win.offsetHeight||parseInt(win.style.height)||300;win.classList.toggle('compact',hh<270);win.classList.toggle('nomap',hh<420);
 var p=presets(),i=hh<(p[0]+p[1])/2?0:hh<(p[1]+p[2])/2?1:2;sizeBtn.textContent=['小','中','大'][i];sizeBtn.dataset.i=i;}
function place(el,pt){if(!pt)return;el.style.left=Math.max(4,Math.min(pt.x,innerWidth-el.offsetWidth-4))+'px';el.style.top=Math.max(4,Math.min(pt.y,innerHeight-el.offsetHeight-4))+'px';el.style.right='auto';el.style.bottom='auto';}
function mode(){var sh=isSheet();win.classList.toggle('sheet',sh);setH(sh?(S.hs||210):(S.hd||presets()[1]));if(!sh)place(win,S.win);fab.hidden=sh&&!win.hidden;place(fab,S.fab);}
function setOpen(o){win.hidden=!o;fab.hidden=o&&isSheet();fab.textContent='⚔';S.open=o;keep();if(o)classify();}
function saveH(){var hh=win.offsetHeight;if(isSheet())S.hs=hh;else S.hd=hh;keep();}
function drag(handle,onMove,onEnd,onTap){var sx,sy,id=null,moved=false;
 handle.addEventListener('pointerdown',function(e){if(e.target.closest('.bar button'))return;id=e.pointerId;moved=false;sx=e.clientX;sy=e.clientY;handle.setPointerCapture(id);onMove(0,0,true);});
 handle.addEventListener('pointermove',function(e){if(e.pointerId!==id)return;var dx=e.clientX-sx,dy=e.clientY-sy;if(!moved&&Math.hypot(dx,dy)<6)return;moved=true;onMove(dx,dy,false);});
 handle.addEventListener('pointerup',function(e){if(e.pointerId!==id)return;id=null;if(moved)onEnd();else if(onTap)onTap();});
 handle.addEventListener('pointercancel',function(){id=null});}
var fo,wo,h0;
drag(fab,function(dx,dy,st){if(st){var b=fab.getBoundingClientRect();fo={x:b.left,y:b.top};return}place(fab,{x:fo.x+dx,y:fo.y+dy})},function(){var b=fab.getBoundingClientRect();S.fab={x:b.left,y:b.top};keep()},function(){setOpen(win.hidden)});
drag(bar,function(dx,dy,st){if(st){var b=win.getBoundingClientRect();wo={x:b.left,y:b.top};h0=b.height;return}
 if(isSheet())setH(h0-dy);else place(win,{x:wo.x+dx,y:wo.y+dy})},function(){if(isSheet())saveH();else{var b=win.getBoundingClientRect();S.win={x:b.left,y:b.top};keep()}});
fab.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();setOpen(win.hidden)}});
bar.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var a=b.dataset.a;
 if(a==='min')setOpen(false);else if(a==='close')h.remove();
 else if(a==='ghost'){var g=!win.classList.contains('ghost');win.classList.toggle('ghost',g);ghostBtn.setAttribute('aria-pressed',g);S.ghost=g;keep();}
 else{var p=presets(),i=((+sizeBtn.dataset.i||0)+1)%3;setH(p[i]);saveH();}});
r.addEventListener('l1nav',function(){if(win.hidden)setOpen(true);if(win.offsetHeight<560){setH(Math.max(560,presets()[2]));saveH();}});if(window.ResizeObserver)new ResizeObserver(function(){classify()}).observe(win);
win.addEventListener('mouseup',function(){if(!isSheet()&&Math.abs(win.offsetHeight-(S.hd||0))>4)saveH()});
var stepsEl=r.getElementById('steps'),nav=document.createElement('div');nav.className='stepnav';
nav.innerHTML='<button type="button" data-s="-1">◀ 上一步</button><span></span><button type="button" data-s="1">下一步 ▶</button>';
stepsEl.after(nav);var cur=0;
function showStep(){var li=stepsEl.querySelectorAll('li');cur=Math.max(0,Math.min(cur,li.length-1));li.forEach(function(x,i){x.classList.toggle('cur',i===cur)});
 nav.querySelector('span').textContent=li.length?('第 '+(cur+1)+' / '+li.length+' 步'):'';nav.querySelector('[data-s="-1"]').disabled=cur<=0;nav.querySelector('[data-s="1"]').disabled=cur>=li.length-1;}
nav.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;cur+=+b.dataset.s;showStep()});
new MutationObserver(function(){cur=0;showStep()}).observe(stepsEl,{childList:true});showStep();
if(S.ghost){win.classList.add('ghost');ghostBtn.setAttribute('aria-pressed','true')}
mode();setOpen(S.open!==false);
(mq.addEventListener?mq.addEventListener('change',mode):mq.addListener(mode));addEventListener('resize',function(){setH(win.offsetHeight);place(fab,S.fab)});
"""
loader = (
 "(()=>{var o=document.getElementById('l1rg-host');if(o){o.remove();return}"
 "var h=document.createElement('div');h.id='l1rg-host';"
 "h.style.cssText='all:initial;position:fixed;top:0;left:0;width:0;height:0;z-index:2147483647';"
 "var r=h.attachShadow({mode:'open'});"
 "r.innerHTML='<style>'+" + json.dumps(c) + "+'</style>'+" + json.dumps(html) + ";"
 "document.documentElement.appendChild(h);"
 "var D={getElementById:function(i){return r.getElementById(i)},"
 "addEventListener:function(a,b,c){r.addEventListener(a,b,c)},"
 "createElementNS:function(a,b){return document.createElementNS(a,b)},"
 "createRange:function(){return document.createRange()}};"
 "var getSelection=function(){return window.getSelection()};"
 "(function(document){" + js_bm + "})(D);" + ui.replace('\n','') + "})()"
)
open('build/l1.js','w',encoding='utf-8').write(loader)
bm_full = 'javascript:' + urllib.parse.quote(loader, safe="()!*';,/?:@=+$-_.~")
bm = "javascript:(function(){var u=['https://dick12339-arch.github.io/lineage-route/l1.js?v='+(Date.now()/36e5|0),'https://cdn.jsdelivr.net/gh/dick12339-arch/lineage-route@main/l1.js'],i=0;function go(){var s=document.createElement('script');s.src=u[i];s.onerror=function(){s.remove();if(++i<u.length)go();else alert('天堂路線載入失敗')};document.documentElement.appendChild(s)}go()})()"
bm = 'javascript:' + urllib.parse.quote(bm[11:], safe="()!*';,/?:@=+$-_.~{}|")
open('build/bookmarklet.txt','w',encoding='utf-8').write(bm)
print(len(bm))

# ---- 3) 安裝頁 ----
inst = open('build/install_tpl.html',encoding='utf-8').read().replace('__BM__', bm.replace('&','&amp;').replace('"','&quot;')).replace('__LAND__', open('build/game-land.js',encoding='utf-8').read() and __import__('urllib.parse').parse.quote('javascript:'+open('build/game-land.js',encoding='utf-8').read().replace('\n',''),safe="()!*';,/?:@=+$-_.~{}|&[]<>").replace('javascript%3A','javascript:').replace('&','&amp;').replace('<','&lt;'))
open('安裝天堂書籤.html','w',encoding='utf-8').write(inst)
