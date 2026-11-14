# NPC 位置資料產生器
# 資料來源：L1J-TW（台版天堂 3.80C 開源伺服器）https://github.com/L1Rj/L1j-TW
#   db/InnoDB_TW/spawnlist_npc.sql、npc.sql、mapids.sql
# 用法：python3 npcgen.py <L1j-TW/db/InnoDB_TW 資料夾> lineage-map-guide.html
import re, sys, json, collections
D = sys.argv[1].rstrip('/') + '/'
P = sys.argv[2]

def rows(f, t):
    for line in open(D + f, encoding='utf-8'):
        if line.startswith('INSERT INTO `' + t + '`'):
            v = re.search(r'VALUES \((.*)\);', line).group(1)
            yield [x.replace("\\'", "'") for x in re.findall(r"'((?:[^'\\]|\\.)*)'", v)]

KANA = re.compile(r'[぀-ヿ]')
NPC = {r[0]: (r[1].strip(), r[4]) for r in rows('npc.sql', 'npc')}
MAPN = {int(r[0]): r[1] for r in rows('mapids.sql', 'mapids')}
KEEP = {'L1Merchant': 'm', 'L1Npc': 'm', 'L1Quest': 'm', 'L1Teleporter': 't', 'L1Dwarf': 'w',
        'L1Guardian': 'g', 'L1Board': 'b', 'L1AuctionBoard': 'b'}

def mapname(i):
    n = MAPN.get(i, '')
    n = re.sub(r'[（(][^）)]*[぀-ヿ][^）)]*[）)]', '', n).replace(':', ' ').strip()
    return n

G = collections.OrderedDict()
for r in rows('spawnlist_npc.sql', 'spawnlist_npc'):
    n = NPC.get(r[3])
    if not n or n[1] not in KEEP:
        continue
    name, impl = n
    mid = int(r[10])
    mn = mapname(mid)
    if not name or KANA.search(name) or not mn or KANA.search(mn) or not re.search(r'[一-鿿]', mn):
        continue
    t = KEEP[impl]
    if '傳送師' in name: t = 't'
    elif '倉庫' in name and '商' not in name: t = 'w'
    k = (name, mid)
    g = G.setdefault(k, [name, t, mid, []])
    xy = [int(r[4]), int(r[5])]
    if all(abs(xy[0] - a) + abs(xy[1] - b) > 6 for a, b in g[3]):  # 同一 NPC 太近的點合併
        g[3].append(xy)

out = list(G.values())
maps = {str(m): mapname(m) for m in sorted({g[2] for g in out})}
print('npc groups', len(out), 'maps', len(maps), collections.Counter(g[1] for g in out), file=sys.stderr)
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
blk = '/*NPC*/const NPCS=' + J(out) + ',NPCMAP=' + J(maps) + ';/*ENDNPC*/'
s = open(P, encoding='utf-8').read()
if '/*NPC*/' in s:
    s = re.sub(r'/\*NPC\*/.*?/\*ENDNPC\*/', lambda _: blk, s, count=1, flags=re.S)
else:
    a = '// ===== 實際出沒點（匯入 lcinfo 資料）====='
    assert s.count(a) == 1
    s = s.replace(a, blk + '\n' + a)
open(P, 'w', encoding='utf-8').write(s)
