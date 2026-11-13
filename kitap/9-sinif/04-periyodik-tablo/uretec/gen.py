import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-claude-projeleri-2/5ddfcba7-b4cc-56c1-846b-3986e6fab901/scratchpad/pt')
from elem import *

BLOK = {'s':('#fbcfe8','#be185d'),'p':('#cfe3ff','#1d4ed8'),'d':('#fde7a8','#b45309'),'f':('#c9f2d6','#15803d')}

def buyuk_tablo():
    W, H, G = 9.4, 9.8, 0.45
    X0, Y0 = 8, 9
    def xy(p, g):
        return X0 + (g-1)*(W+G), Y0 + (p-1)*(H+G)
    o = []
    o.append('<svg viewBox="0 0 186 113" style="width:100%;height:auto">')
    o.append('<g font-family="Inter" text-anchor="middle">')
    # grup başlıkları
    for g in range(1,19):
        x, _ = xy(1, g)
        o.append(f'<text x="{x+W/2:.2f}" y="3.6" font-size="3.3" font-weight="800" fill="#7a0f3c">{g}</text>')
        o.append(f'<text x="{x+W/2:.2f}" y="7.4" font-size="2.9" font-weight="700" fill="#5d6478">{ab(g)}</text>')
    for p in range(1,8):
        _, y = xy(p, 1)
        o.append(f'<text x="3" y="{y+H/2+1.2:.2f}" font-size="3.4" font-weight="800" fill="#7a0f3c">{p}</text>')
    def hucre(x, y, z, renk):
        dol, cz = renk
        o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W}" height="{H}" rx="1" fill="{dol}" stroke="{cz}" stroke-width=".25"/>')
        o.append(f'<text x="{x+1.0:.2f}" y="{y+2.7:.2f}" font-size="2.3" text-anchor="start" fill="#3b4256">{z}</text>')
        o.append(f'<text x="{x+W/2:.2f}" y="{y+7.6:.2f}" font-size="4.1" font-weight="800" fill="#1d2133">{SEMBOL[z-1]}</text>')
    for z in range(1,119):
        p, g, b = yer(z)
        if g is None: continue
        x, y = xy(p, g)
        hucre(x, y, z, BLOK[b])
    # grup 3 yer tutucular
    for p, t in ((6,'57–71'),(7,'89–103')):
        x, y = xy(p, 3)
        o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W}" height="{H}" rx="1" fill="#c9f2d6" stroke="#15803d" stroke-width=".25" stroke-dasharray="1 .6"/>')
        o.append(f'<text x="{x+W/2:.2f}" y="{y+4.6:.2f}" font-size="2.3" font-weight="700" fill="#15803d">{t}</text>')
        o.append(f'<text x="{x+W/2:.2f}" y="{y+7.6:.2f}" font-size="2.3" fill="#15803d">f bloku</text>')
    # f satırları
    yF = Y0 + 7*(H+G) + 3.2
    for r, (bas, ad) in enumerate(((57,'Lantanitler'),(89,'Aktinitler'))):
        y = yF + r*(H+G)
        x_ad, _ = xy(1,1)
        o.append(f'<text x="{x_ad + 2*(W+G) - 1.2:.2f}" y="{y+H/2-0.4:.2f}" font-size="2.9" font-weight="800" text-anchor="end" fill="#15803d">{ad}</text>')
        o.append(f'<text x="{x_ad + 2*(W+G) - 1.2:.2f}" y="{y+H/2+3.1:.2f}" font-size="2.6" text-anchor="end" fill="#15803d">{6+r}. periyot</text>')
        for k in range(15):
            z = bas + k
            x, _ = xy(1, 3+k)
            hucre(x, y, z, BLOK['f'])
    # ilk üç periyottaki boşluğa açıklama
    x2, y1 = xy(1, 3)
    o.append(f'<text x="{x2+5*(W+G):.2f}" y="{y1+4.4:.2f}" font-size="2.9" fill="#5d6478">1–3. periyotlarda geçiş elementi yoktur:</text>')
    o.append(f'<text x="{x2+5*(W+G):.2f}" y="{y1+8.4:.2f}" font-size="2.9" fill="#5d6478">2A’dan sonra doğrudan 3A gelir.</text>')
    # blok etiketleri (lejant)
    yL = yF + 2*(H+G) + 2.4
    lx = X0
    for b, ad in (('s','s bloku'),('d','d bloku'),('p','p bloku'),('f','f bloku (iç geçiş)')):
        dol, cz = BLOK[b]
        o.append(f'<rect x="{lx}" y="{yL}" width="5" height="3.6" rx=".8" fill="{dol}" stroke="{cz}" stroke-width=".3"/>')
        o.append(f'<text x="{lx+6.2}" y="{yL+2.9}" font-size="3.1" text-anchor="start" font-weight="700" fill="{cz}">{ad}</text>')
        lx += 26
    o.append(f'<text x="183" y="{yL+2.9}" font-size="2.8" text-anchor="end" fill="#5d6478">Üst: IUPAC no · Alt: A/B adı</text>')
    o.append('</g></svg>')
    return '\n'.join(o), yL+5

YARI = {'B','Si','Ge','As','Sb','Te'}
AMETAL = {'H','C','N','O','F','P','S','Cl','Se','Br','I'}
SOY = {'He','Ne','Ar','Kr','Xe','Rn','Og'}
BELIRSIZ = {'Po','At','Nh','Fl','Mc','Lv','Ts'}
SINIF = {'metal':('#fbd3e4','#be185d'),'ametal':('#cdeafe','#0369a1'),'yari':('#fde68a','#a16207'),'soy':('#dcfce7','#15803d'),'belirsiz':('#eceef3','#8a90a3')}
def sinif(s):
    if s in YARI: return 'yari'
    if s in AMETAL: return 'ametal'
    if s in SOY: return 'soy'
    if s in BELIRSIZ: return 'belirsiz'
    return 'metal'

def metal_harita():
    W, H, G = 6.2, 6.2, 0.4
    X0, Y0 = 1, 1
    o = ['<svg viewBox="0 0 120 63" style="width:100%;height:auto">','<g font-family="Inter" text-anchor="middle">']
    def xy(p,g): return X0+(g-1)*(W+G), Y0+(p-1)*(H+G)
    for z in range(1,119):
        p,g,b = yer(z)
        s = SEMBOL[z-1]
        if g is None:
            continue
        x,y = xy(p,g); dol,cz = SINIF[sinif(s)]
        o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W}" height="{H}" rx=".7" fill="{dol}" stroke="{cz}" stroke-width=".2"/>')
        o.append(f'<text x="{x+W/2:.2f}" y="{y+4.3:.2f}" font-size="2.9" font-weight="700" fill="#1d2133">{s}</text>')
    for p in (6,7):
        x,y = xy(p,3); dol,cz = SINIF['metal']
        o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W}" height="{H}" rx=".7" fill="{dol}" stroke="{cz}" stroke-width=".2" stroke-dasharray=".8 .5"/>')
        o.append(f'<text x="{x+W/2:.2f}" y="{y+4.1:.2f}" font-size="2.6" font-weight="700" fill="{cz}">*</text>')
    # merdiven çizgisi (metal/ametal sınırı): B-Si-As-Te-At sağ-üst ile metal arasına kalın çizgi
    pts = []
    # sınır: her periyotta yarı metallerin sol kenarı
    stairs = [(2,13),(3,14),(4,14),(5,15),(6,16)]
    path = []
    for i,(p,g) in enumerate(stairs):
        x,y = xy(p,g)
        if i == 0: path.append(f'M{x-G/2:.2f} {y-G/2:.2f}')
        else: path.append(f'H{x-G/2:.2f}')
        path.append(f'V{y+H+G/2:.2f}')
    o.append(f'<path d="{" ".join(path)}" fill="none" stroke="#1d2133" stroke-width=".7"/>')
    # f satırları özet
    yF = Y0 + 7*(H+G) + 1.6
    for r,bas in enumerate((57,89)):
        y = yF + r*(H+G)
        for k in range(15):
            z = bas+k; x,_ = xy(1,3+k); dol,cz = SINIF['metal']
            o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W}" height="{H}" rx=".7" fill="{dol}" stroke="{cz}" stroke-width=".2"/>')
            o.append(f'<text x="{x+W/2:.2f}" y="{y+4.3:.2f}" font-size="2.9" font-weight="700" fill="#1d2133">{SEMBOL[z-1]}</text>')
        o.append(f'<text x="{xy(1,3)[0]-1:.2f}" y="{y+4.3:.2f}" font-size="2.6" font-weight="700" text-anchor="end" fill="#be185d">*</text>')
    o.append('</g></svg>')
    return '\n'.join(o)

def iskelet(harfler, w=100):
    """harfler: {(p,g): 'X'}  — sadece 1-4. periyot iskeleti"""
    W, H, G = 5.2, 5.2, 0.35
    X0, Y0 = 6, 6
    o = [f'<svg viewBox="0 0 108 30" style="width:100%;height:auto">','<g font-family="Inter" text-anchor="middle">']
    def xy(p,g): return X0+(g-1)*(W+G), Y0+(p-1)*(H+G)
    for z in range(1,37):
        p,g,b = yer(z); x,y = xy(p,g)
        h = harfler.get((p,g))
        o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W}" height="{H}" rx=".5" fill="{"#fdeef5" if h else "#fff"}" stroke="#9aa3b8" stroke-width=".22"/>')
        if h: o.append(f'<text x="{x+W/2:.2f}" y="{y+3.9:.2f}" font-size="3.6" font-weight="800" fill="#7a0f3c">{h}</text>')
    for g in (1,2,13,14,15,16,17,18):
        x,_ = xy(1,g); o.append(f'<text x="{x+W/2:.2f}" y="4.3" font-size="2.4" font-weight="700" fill="#5d6478">{ab(g)}</text>')
    for p in range(1,5):
        _,y = xy(p,1); o.append(f'<text x="2.6" y="{y+3.7:.2f}" font-size="2.6" font-weight="700" fill="#5d6478">{p}</text>')
    o.append('</g></svg>')
    return '\n'.join(o)

if __name__ == '__main__':
    t, h = buyuk_tablo(); print('buyuk yukseklik', h)
    open('buyuk.svg','w').write(t)
    open('metal.svg','w').write(metal_harita())
    open('test10.svg','w').write(iskelet({(2,1):'X',(4,8):'Y',(3,17):'Z',(4,2):'T',(2,18):'Q'}))

def kapak_desen():
    W, G = 5.6, 0.7
    X0, Y0 = 89, 34
    o = []
    alfa = {'s':.34,'p':.18,'d':.12,'f':.24}
    for z in range(1,119):
        p,g,b = yer(z)
        if g is None:
            k = z-57 if z < 89 else z-89; r = 0 if z < 89 else 1
            x = X0+(2+k)*(W+G); y = Y0+7*(W+G)+3+r*(W+G)
        else:
            x = X0+(g-1)*(W+G); y = Y0+(p-1)*(W+G)
        renk = '#fbbf24' if SEMBOL[z-1] in ('H','He') else '#ffffff'
        a = .9 if renk != '#ffffff' else alfa[b]
        o.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W}" height="{W}" rx=".9" fill="{renk}" fill-opacity="{a}"/>')
    return '\n'.join(o)

def enjekte(yol):
    import re
    t, h = buyuk_tablo()
    parca = {'buyuk': t, 'metal': metal_harita(), 'test10': iskelet({(2,1):'X',(4,8):'Y',(3,17):'Z',(4,2):'T',(2,18):'Q'}),
             'kapak': kapak_desen()}
    s = open(yol, encoding='utf-8').read()
    for k, v in parca.items():
        s = re.sub(rf'<!--BAS:{k}-->.*?<!--SON:{k}-->', lambda m: f'<!--BAS:{k}-->\n{v}\n<!--SON:{k}-->', s, flags=re.S)
    open(yol, 'w', encoding='utf-8').write(s)
    print('enjekte edildi')

if len(sys.argv) > 1:
    enjekte(sys.argv[1])
