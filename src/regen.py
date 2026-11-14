import json,re,sys
DB=json.load(open(sys.argv[1],encoding='utf-8'))
TOP={'說話之島':'ti','銀騎士地區':'skt','妖魔森林':'orc','古魯丁':'gludin','風木':'woodbec','妖精森林':'elf','肯特':'kent','龍之谷':'dv','奇岩':'giran','海音':'heine',
 '冒險洞窟':'ti_adv','古魯丁地監':'gl_dun','海底隧道':'gl_dun','眠龍洞穴':'sleep','騎士洞穴':'skt_dun','龍之谷地監':'dvd','巨蟻洞穴':'ant','奇岩地監':'gi_dun','海音地監':'hn_dun',
 '新手獵場':'ti','北島獵場':'ti','娜魯帕洞穴':'elf','威頓':'werldern','歐瑞':'oren','亞丁':'aden','燃柳':'orc','火龍窟':'fire'}
REG={};RN={};CAT={};unm=[]
def walk(nodes,cat,parent=None):
  for r in nodes:
    nm=r['name'];base=nm.replace(' 獵場','');RN[r['id']]=nm;CAT[r['id']]=cat
    key=next((k for k in sorted(TOP,key=len,reverse=True) if base.startswith(k)),None)
    node=TOP.get(key) if key else None
    lab=base[len(key):].strip() if key and base!=key else nm
    if cat=='個人獵場':lab=(lab if lab!=nm else base)+'（個人獵場）'
    if base=='海底隧道':lab='海底隧道（古魯丁地監內）'
    if nm=='說話之島' and cat=='個人獵場':node=None
    if node and (not r.get('child') or cat=='野外'):REG[r['id']]=[node,lab]
    elif not node and not r.get('child'):unm.append(nm)
    walk(r.get('child',[]),cat,r)
for t in DB['regions']:walk(t.get('child',[]),t['name'])
M=[];IMG={}
for m in DB['monsters']:
  M.append({'k':m['key'],'n':m['name'],'l':m['level'],'u':1 if m['undead'] else 0,'b':1 if m['big'] else 0,'r':[i for i in m['regionIds'] if i in REG or i in RN],'d':[[d['cat'],d['items']] for d in m['drops'] if d['items']]})
  if m.get('img'):IMG[m['key']]=m['img']
used=sorted({i for m in DB['monsters'] for i in m['regionIds']})
rn={str(i):[RN[i],CAT[i]] for i in used if i in RN}
I={x['id']:x for x in DB['items']}
NODE={'娜魯帕洞穴':'elf','妖精森林':'elf','奇岩村':'giran','威頓村':'werldern','說話之島':'ti'}
def nodeof(npc):
  m=re.search(r'[(（](.+?)[)）]',npc);return NODE.get(m.group(1)) if m else None
REC=[]
for c in DB['crafts']:
  mats=[[I[x[0]]['name'] if x[0] in I else x[0],x[1]]+([x[2]] if len(x)>2 else []) for x in c['mats']]
  REC.append([I[c['out']]['name'],c['cnt'],c['npc'],nodeof(c['npc']),0,mats,c.get('prob',100),c.get('outEn',0),c['cat'],c['sub'],c['cls']])
ITEMS={}
for x in DB['items']:
  d={'c':x['cat'],'s':x.get('sub',''),'g':x.get('g'),'k':x.get('kind','')}
  for k in('ac','dmg','safe','w','desc','w2h','noTrade'):
    if x.get(k) not in (None,'',[],0):d[k]=x[k]
  if x.get('opts'):d['o']=x['opts']
  if x.get('cls'):d['cls']=x['cls']
  s=x.get('src',{})
  if s.get('shop'):d['shop']=s['shop']
  if s.get('etc'):d['etc']=s['etc']
  ITEMS[x['name']]=d
icons={k:v for k,v in DB['icons'].items() if any(d.get('g')==k for d in ITEMS.values())}
print('unmapped regions:',unm,file=sys.stderr);print('mobs',len(M),'regions',len(rn),'recipes',len(REC),'items',len(ITEMS),'icons',len(icons),file=sys.stderr)
J=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
p=sys.argv[2];s=open(p,encoding='utf-8').read()
s=re.sub(r'/\*IMG\*/const MOBIMG=.*?;/\*ENDIMG\*/','/*IMG*/const MOBIMG='+J(IMG).replace('\\','\\\\')+';/*ENDIMG*/',s,count=1,flags=re.S)
def sub1(pat,rep):
  global s
  n=len(re.findall(pat,s,flags=re.S));assert n==1,(pat,n);s=re.sub(pat,lambda _:rep,s,count=1,flags=re.S)
sub1(r'const MOBRN=\{.*?\};\n','const MOBRN='+J(rn)+';\n')
sub1(r'const MOBREG=\{.*?\};\n','const MOBREG='+J({str(k):v for k,v in REG.items()})+';\n')
sub1(r'const MOB=\[.*?\];\n','const MOB='+J(M)+';\n')
sub1(r'const RECIPES_BUILTIN=\[.*?\];\nconst ITEMS=\{.*?\};\nconst ITEMICON=\{.*?\};\n(?:const ENHB=\[.*?\];\n)?' if 'const ITEMICON=' in s else r'const RECIPES_BUILTIN=\[.*?\n\];\n','const RECIPES_BUILTIN='+J(REC)+';\nconst ITEMS='+J(ITEMS)+';\nconst ITEMICON='+J(icons)+';\nconst ENHB='+J([{k:e[k] for k in ('kind','name','types','levels') if k in e}|{'item':(I[e['item']]['name'] if e.get('item') in I else '')} for e in DB.get('enh',[])])+';\n')
open(p,'w',encoding='utf-8').write(s)
