(function(){
if(typeof cc==='undefined'||!cc.view||!cc.view.setDesignResolutionSize){alert('請在樂園遊戲畫面（linwebtw.com/play）上使用');return}
var V=cc.view,RP=cc.ResolutionPolicy,S=window.__l1land;
if(S){S.panel.style.display=S.panel.style.display==='none'?'':'none';return}
var o=V.getDesignResolutionSize(),op=V.getResolutionPolicy?V.getResolutionPolicy():null;
S=window.__l1land={ow:o.width,oh:o.height,op:op,on:true,H:1280};
function apply(){if(!S.on)return;var f=V.getFrameSize(),W=Math.round(S.H*f.width/f.height);
  if(f.width<=f.height){restore(true);return}
  var d=V.getDesignResolutionSize();if(Math.abs(d.width-W)>1||Math.abs(d.height-S.H)>1)V.setDesignResolutionSize(W,S.H,RP&&RP.FIXED_HEIGHT!=null?RP.FIXED_HEIGHT:4);
  lab.textContent='橫版 '+W+'×'+S.H}
function restore(keepOn){V.setDesignResolutionSize(S.ow,S.oh,S.op!=null?S.op:(RP?RP.SHOW_ALL:0));if(!keepOn){S.on=false;lab.textContent='直版（原始）';tg.textContent='切回橫版'}else lab.textContent='視窗是直的，先用原始直版'}
var p=document.createElement('div');p.style.cssText='position:fixed;z-index:2147483646;left:10px;bottom:10px;display:flex;gap:6px;align-items:center;padding:6px 8px;background:rgba(15,11,7,.88);border:1px solid #e2b04f;border-radius:8px;font:12px sans-serif;color:#f5e8c6;user-select:none';
p.innerHTML='<span></span><button data-k="-">放大介面</button><button data-k="+">縮小介面</button><button data-k="t">還原直版</button><button data-k="x">隱藏</button>';
[].forEach.call(p.querySelectorAll('button'),function(b){b.style.cssText='font:12px sans-serif;padding:3px 8px;border-radius:5px;border:1px solid #7a6230;background:#1d1915;color:#e2b04f;cursor:pointer'});
var lab=p.querySelector('span'),tg=p.querySelector('[data-k=t]');S.panel=p;
p.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var k=b.dataset.k;
  if(k==='x'){p.style.display='none';return}
  if(k==='t'){if(S.on){restore(false)}else{S.on=true;tg.textContent='還原直版';apply()}return}
  if(k==='-')S.H=Math.max(720,S.H-80);if(k==='+')S.H=Math.min(1600,S.H+80);try{localStorage.setItem('l1landH',S.H)}catch(_){}if(S.on)apply()});
try{var h=parseInt(localStorage.getItem('l1landH'));if(h>=720&&h<=1600)S.H=h}catch(_){}
document.body.appendChild(p);
window.addEventListener('resize',function(){setTimeout(apply,50)});
S.timer=setInterval(apply,1500);apply();
})();
