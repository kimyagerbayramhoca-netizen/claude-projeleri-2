import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'svg')
U='#9f1239'; UK='#650b23'; UA='#fdeef1'; S='#5d6478'; M='#1d2133'; AMB='#f59e0b'; TEAL='#0f8f84'; IND='#4f46e5'
def w(n,s): open(os.path.join(D,n+'.svg'),'w').write(s)

# ---------- 1) İE1 grafiği Z=1..20
sym="H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca".split()
ie=[1312,2372,520,899,801,1086,1402,1314,1681,2081,496,738,578,786,1012,1000,1251,1521,419,590]
x0,x1,y0,y1=18,174,82,8; ymax=2500
X=lambda z: x0+(z-0.5)*(x1-x0)/20.5
Y=lambda v: y0-(v/ymax)*(y0-y1)
o=[f'<svg viewBox="0 0 180 94" class="grafik"><g font-family="Inter" font-size="4" fill="{S}">']
for (a,b,lab) in [(0.6,2.4,'1.'),(2.6,10.4,'2. periyot'),(10.6,18.4,'3. periyot'),(18.6,20.4,'4.')]:
    o.append(f'<rect x="{X(a):.1f}" y="{y1}" width="{X(b)-X(a):.1f}" height="{y0-y1}" fill="{UA}" opacity=".55"/>')
    o.append(f'<text x="{(X(a)+X(b))/2:.1f}" y="{y1+4}" text-anchor="middle" font-size="3.4" fill="{UK}" font-weight="700">{lab}</text>')
for v in range(0,2501,500):
    o.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="#e5e7f0" stroke-width=".3"/>')
    o.append(f'<text x="{x0-1.5}" y="{Y(v)+1.4:.1f}" text-anchor="end" font-size="3.6">{v}</text>')
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{M}" stroke-width=".5"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1-2}" stroke="{M}" stroke-width=".5"/>')
for z in range(1,21):
    o.append(f'<text x="{X(z):.1f}" y="{y0+4.4}" text-anchor="middle" font-size="3.4">{z}</text>')
o.append(f'<text x="{(x0+x1)/2}" y="{y0+10}" text-anchor="middle" fill="{M}" font-weight="700" font-size="4">Atom numarası (Z)</text>')
o.append(f'<text x="2" y="4.5" fill="{M}" font-weight="700" font-size="4">İE₁ (kJ/mol)</text>')
pts=[(X(z),Y(v)) for z,v in zip(range(1,21),ie)]
o.append('<polyline fill="none" stroke="%s" stroke-width=".8" points="%s"/>'%(U,' '.join(f'{a:.1f},{b:.1f}' for a,b in pts)))
exc={(4,5),(7,8),(12,13),(15,16)}
for (za,zb) in exc:
    (a,b),(c,d)=pts[za-1],pts[zb-1]
    o.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="{AMB}" stroke-width="1.6" stroke-linecap="round"/>')
for i,(a,b) in enumerate(pts):
    z=i+1
    o.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="1.25" fill="{U if sym[i] not in ("He","Ne","Ar") else UK}"/>')
    dy=-2.6 if z not in (3,11,19,5,13,8,16) else 5.4
    o.append(f'<text x="{a:.1f}" y="{b+dy:.1f}" text-anchor="middle" font-size="3.6" font-weight="700" fill="{M}">{sym[i]}</text>')
o.append(f'<rect x="112" y="16" width="56" height="13" rx="2" fill="#fff" stroke="{AMB}" stroke-width=".4"/>')
o.append(f'<line x1="115" y1="20" x2="121" y2="20" stroke="{AMB}" stroke-width="1.6" stroke-linecap="round"/><text x="123" y="21.2" font-size="3.4" fill="{M}">Genel artışa aykırı düşüş</text>')
o.append(f'<text x="115" y="26.4" font-size="3.3" fill="{S}">2A → 3A ve 5A → 6A geçişleri</text>')
o.append('</g></svg>')
w('ie',''.join(o))

# ---------- 2) atom yarıçapı daireleri
rad={(1,1):('H',37),(2,1):('Li',152),(2,2):('Be',112),(2,3):('B',85),(2,4):('C',77),(2,5):('N',75),(2,6):('O',73),(2,7):('F',72),
(3,1):('Na',186),(3,2):('Mg',160),(3,3):('Al',143),(3,4):('Si',118),(3,5):('P',110),(3,6):('S',103),(3,7):('Cl',99),
(4,1):('K',227),(4,2):('Ca',197),(4,3):('Ga',135),(4,4):('Ge',122),(4,5):('As',120),(4,6):('Se',117),(4,7):('Br',114)}
cw,ch=22,21; ox,oy=12,10
o=[f'<svg viewBox="0 0 {ox+7*cw+12} {oy+4*ch+12}" class="grafik"><g font-family="Inter" text-anchor="middle">']
for g in range(1,8):
    o.append(f'<text x="{ox+(g-0.5)*cw}" y="{oy-4}" font-size="4" font-weight="800" fill="{UK}">{g}A</text>')
for p in range(1,5):
    o.append(f'<text x="{ox-6}" y="{oy+(p-0.5)*ch+1.5}" font-size="4" font-weight="800" fill="{UK}">{p}</text>')
for (p,g),(s,r) in rad.items():
    cx=ox+(g-0.5)*cw; cy=oy+(p-0.5)*ch-3
    R=r*0.04
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.2f}" fill="{U}" fill-opacity="{0.25+0.55*r/227:.2f}" stroke="{U}" stroke-width=".35"/>')
    ty = cy+1.5 if r>50 else cy-3
    o.append(f'<text x="{cx}" y="{ty}" font-size="4.2" font-weight="800" fill="{"#fff" if r>140 else M}">{s}</text>')
    o.append(f'<text x="{cx}" y="{oy+p*ch-1.2}" font-size="3.3" fill="{S}">{r}</text>')
X2=ox+7*cw+6
o.append(f'<defs><marker id="ra" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 10 5 0 10z" fill="{AMB}"/></marker></defs>')
o.append(f'<path d="M{X2} {oy+2} V{oy+4*ch-4}" stroke="{AMB}" stroke-width=".9" marker-end="url(#ra)"/>')
o.append(f'<path d="M{ox+7*cw-4} {oy+4*ch+6} H{ox+4}" stroke="{AMB}" stroke-width=".9" marker-end="url(#ra)"/>')
o.append(f'<text x="{ox+3.5*cw}" y="{oy+4*ch+10.5}" font-size="3.4" fill="{S}">yarıçap artar · değerler pm (yaklaşık)</text>')
o.append('</g></svg>')
w('yaricap',''.join(o))

# ---------- 3) elektronegatiflik ısı haritası
en={(1,1):('H',2.2),(2,1):('Li',1.0),(2,2):('Be',1.6),(2,3):('B',2.0),(2,4):('C',2.6),(2,5):('N',3.0),(2,6):('O',3.4),(2,7):('F',4.0),
(3,1):('Na',0.9),(3,2):('Mg',1.3),(3,3):('Al',1.6),(3,4):('Si',1.9),(3,5):('P',2.2),(3,6):('S',2.6),(3,7):('Cl',3.2),
(4,1):('K',0.8),(4,2):('Ca',1.0),(4,7):('Br',3.0)}
nob={1:'He',2:'Ne',3:'Ar',4:'Kr'}
cw,ch=19,15; ox,oy=10,10
def col(v):
    t=(v-0.8)/(4.0-0.8)
    c1=(0xfd,0xee,0xf1); c2=(0x65,0x0b,0x23)
    return '#%02x%02x%02x'%tuple(int(a+(b-a)*t) for a,b in zip(c1,c2))
o=[f'<svg viewBox="0 0 {ox+8*cw+4} {oy+4*ch+16}" class="grafik"><g font-family="Inter" text-anchor="middle">']
for g in range(1,9):
    o.append(f'<text x="{ox+(g-0.5)*cw}" y="{oy-3}" font-size="3.8" font-weight="800" fill="{UK}">{g}A</text>')
for p in range(1,5):
    o.append(f'<text x="{ox-5}" y="{oy+(p-0.5)*ch+1.4}" font-size="3.8" font-weight="800" fill="{UK}">{p}</text>')
for (p,g),(s,v) in en.items():
    x=ox+(g-1)*cw; y=oy+(p-1)*ch
    fc='#fff' if v>=2.4 else M
    o.append(f'<rect x="{x+.6}" y="{y+.6}" width="{cw-1.2}" height="{ch-1.2}" rx="1.6" fill="{col(v)}"/>')
    o.append(f'<text x="{x+cw/2}" y="{y+6.4}" font-size="4.4" font-weight="800" fill="{fc}">{s}</text>')
    o.append(f'<text x="{x+cw/2}" y="{y+11.6}" font-size="3.6" fill="{fc}">{str(v).replace(".",",")}</text>')
for p,s in nob.items():
    x=ox+7*cw; y=oy+(p-1)*ch
    o.append(f'<rect x="{x+.6}" y="{y+.6}" width="{cw-1.2}" height="{ch-1.2}" rx="1.6" fill="#fff" stroke="#c9ccd8" stroke-width=".35" stroke-dasharray="1 .8"/>')
    o.append(f'<text x="{x+cw/2}" y="{y+6.4}" font-size="4.4" font-weight="800" fill="{S}">{s}</text><text x="{x+cw/2}" y="{y+11.6}" font-size="3.6" fill="{S}">—</text>')
yy=oy+4*ch+5
for i in range(40):
    o.append(f'<rect x="{ox+20+i*2.2:.1f}" y="{yy}" width="2.3" height="3.2" fill="{col(0.8+3.2*i/39)}"/>')
o.append(f'<text x="{ox+18}" y="{yy+2.8}" font-size="3.4" text-anchor="end" fill="{S}">düşük</text><text x="{ox+20+88+2}" y="{yy+2.8}" font-size="3.4" text-anchor="start" fill="{S}">yüksek</text>')
o.append(f'<text x="{ox+8*cw/2}" y="{yy+8.6}" font-size="3.2" fill="{S}">Pauling ölçeği (F = 4,0) · soy gazlara değer verilmez</text>')
o.append('</g></svg>')
w('en',''.join(o))

# ---------- 4) izoelektronik seri
ions=[('N','3−',7,146),('O','2−',8,140),('F','−',9,133),('Na','+',11,102),('Mg','2+',12,72),('Al','3+',13,54)]
o=[f'<svg viewBox="0 0 172 52" class="grafik"><g font-family="Inter" text-anchor="middle">']
x=8
for s,q,z,r in ions:
    R=r*0.105
    cx=x+R; x+=2*R+5
    an = q.endswith('−')
    o.append(f'<circle cx="{cx:.1f}" cy="24" r="{R:.1f}" fill="{U if an else TEAL}" fill-opacity=".22" stroke="{U if an else TEAL}" stroke-width=".5"/>')
    o.append(f'<text x="{cx:.1f}" y="25.6" font-size="5.2" font-weight="800" fill="{M}">{s}<tspan font-size="3.6" dy="-2.2">{q}</tspan></text>')
    o.append(f'<text x="{cx:.1f}" y="44.5" font-size="4.2" fill="{S}">p = {z}</text><text x="{cx:.1f}" y="50" font-size="4.2" fill="{M}" font-weight="700">{r} pm</text>')
o.append(f'<text x="86" y="5" font-size="4.4" font-weight="700" fill="{UK}">10 elektron (2-8) · proton arttıkça tanecik küçülür</text>')
o.append('</g></svg>')
w('izoel',''.join(o))

# ---------- 5) Na -> Na+, Cl -> Cl-
def atom(cx,cy,shells,R,label,sub,clr,dashedlast=False):
    s=[]
    n=len(shells)
    for i,e in enumerate(shells):
        rr=R*(i+1)/n
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="{clr}" stroke-width=".4"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{clr}"/>')
    s.append(f'<text x="{cx}" y="35" font-size="4.4" font-weight="800" fill="{M}">{label}</text>')
    s.append(f'<text x="{cx}" y="40" font-size="3.4" fill="{S}">{sub}</text>')
    return ''.join(s)
o=[f'<svg viewBox="0 0 180 42" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(f'<defs><marker id="ok5" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 10 5 0 10z" fill="{S}"/></marker></defs>')
o.append(atom(20,16,[2,8,1],13,'Na','11p · 11e · 2-8-1',TEAL))
o.append(f'<path d="M37 16 H51" stroke="{S}" stroke-width=".6" marker-end="url(#ok5)"/><text x="44" y="12.5" font-size="3.4" fill="{S}">−1e⁻</text>')
o.append(atom(66,16,[2,8],7.2,'Na⁺','11p · 10e · 2-8',TEAL))
o.append(f'<line x1="90" y1="2" x2="90" y2="40" stroke="#e5e7f0" stroke-width=".4"/>')
o.append(atom(114,16,[2,8,7],7,'Cl','17p · 17e · 2-8-7',U))
o.append(f'<path d="M129 16 H143" stroke="{S}" stroke-width=".6" marker-end="url(#ok5)"/><text x="136" y="12.5" font-size="3.4" fill="{S}">+1e⁻</text>')
o.append(atom(160,16,[2,8,8],12.7,'Cl⁻','17p · 18e · 2-8-8',U))
o.append('</g></svg>')
w('iyon',''.join(o))

# ---------- 6) r = d/2
o=[f'<svg viewBox="0 0 100 40" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(f'<circle cx="30" cy="18" r="14" fill="{U}" fill-opacity=".18" stroke="{U}" stroke-width=".5"/><circle cx="58" cy="18" r="14" fill="{U}" fill-opacity=".18" stroke="{U}" stroke-width=".5"/>')
o.append(f'<circle cx="30" cy="18" r="1.4" fill="{UK}"/><circle cx="58" cy="18" r="1.4" fill="{UK}"/>')
o.append(f'<line x1="30" y1="18" x2="58" y2="18" stroke="{AMB}" stroke-width=".7"/>')
o.append(f'<line x1="30" y1="35" x2="58" y2="35" stroke="{M}" stroke-width=".4"/><line x1="30" y1="33" x2="30" y2="37" stroke="{M}" stroke-width=".4"/><line x1="58" y1="33" x2="58" y2="37" stroke="{M}" stroke-width=".4"/>')
o.append(f'<text x="44" y="39.5" font-size="3.6" fill="{M}" font-weight="700">d (çekirdekler arası)</text>')
o.append(f'<text x="37" y="15.6" font-size="4" font-weight="800" fill="#b45309">r</text>')
o.append(f'<text x="86" y="20" font-size="5" font-weight="800" fill="{UK}">r = d/2</text>')
o.append('</g></svg>')
w('rd',''.join(o))

# ---------- 7) Si ardışık İE çubukları
vals=[1086,2353,4621,6223,37831]
o=[f'<svg viewBox="0 0 100 70" class="grafik"><g font-family="Inter" text-anchor="middle">']
bx,by,bh=16,58,48
for v in range(0,40001,10000):
    yv=by-v/37831*bh
    o.append(f'<line x1="{bx-2}" y1="{yv:.1f}" x2="96" y2="{yv:.1f}" stroke="#e5e7f0" stroke-width=".3"/><text x="{bx-3}" y="{yv+1.2:.1f}" font-size="3.2" text-anchor="end" fill="{S}">{v}</text>')
for i,v in enumerate(vals):
    h=v/37831*bh; x=bx+3+i*16
    c = U if i<4 else AMB
    o.append(f'<rect x="{x}" y="{by-h:.1f}" width="10" height="{h:.1f}" rx="1" fill="{c}"/>')
    o.append(f'<text x="{x+5}" y="{by-h-1.4:.1f}" font-size="3.3" fill="{M}" font-weight="700">{v}</text>')
    o.append(f'<text x="{x+5}" y="{by+4.4}" font-size="3.4" fill="{S}">İE{"₁₂₃₄₅"[i]}</text>')
o.append(f'<line x1="{bx-2}" y1="{by}" x2="96" y2="{by}" stroke="{M}" stroke-width=".4"/>')
o.append(f'<text x="50" y="68" font-size="3.5" fill="{UK}" font-weight="700">Karbon: 4 elektron görece kolay, 5. çok zor → 4A</text>')
o.append(f'<text x="2" y="5" font-size="3.4" text-anchor="start" fill="{M}" font-weight="700">kJ/mol</text>')
o.append('</g></svg>')
w('karbon',''.join(o))

# ---------- 8) trend haritası
o=[f'<svg viewBox="0 0 124 80" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(f'<defs><marker id="tm" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto"><path d="M0 0 10 5 0 10z" fill="{U}"/></marker><marker id="tm2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto"><path d="M0 0 10 5 0 10z" fill="{TEAL}"/></marker></defs>')
gx,gy,c=22,9,10
for p in range(5):
    for g in range(8):
        if p==0 and g not in (0,7): continue
        t=(g/7+(4-p)/4)/2
        o.append(f'<rect x="{gx+g*c+.4}" y="{gy+p*c+.4}" width="{c-.8}" height="{c-.8}" rx="1" fill="{U}" fill-opacity="{0.06+0.5*t:.2f}" stroke="#e8b9c4" stroke-width=".3"/>')
for g in range(8):
    o.append(f'<text x="{gx+g*c+c/2}" y="{gy-2}" font-size="3.4" font-weight="700" fill="{UK}">{g+1}A</text>')
o.append(f'<text x="{gx+7*c+c/2}" y="{gy+c/2+1.4}" font-size="3.8" font-weight="800" fill="{UK}">He</text>')
o.append(f'<text x="{gx+6*c+c/2}" y="{gy+c+c/2+1.4}" font-size="3.8" font-weight="800" fill="#fff">F</text>')
o.append(f'<text x="{gx+c/2}" y="{gy+4*c+c/2+1.4}" font-size="3.8" font-weight="800" fill="{TEAL}">Cs</text>')
o.append(f'<text x="{gx+c/2}" y="{gy+c/2+1.4}" font-size="3.8" font-weight="800" fill="{M}">H</text>')
W=8*c; H=5*c
o.append(f'<path d="M{gx} {gy+H+4} H{gx+W}" stroke="{U}" stroke-width=".8" marker-end="url(#tm)"/>')
o.append(f'<text x="{gx+W/2}" y="{gy+H+9}" font-size="3.6" fill="{U}" font-weight="700">İE₁ · elektronegatiflik · ametalik karakter artar</text>')
o.append(f'<path d="M{gx+W} {gy+H+13} H{gx}" stroke="{TEAL}" stroke-width=".8" marker-end="url(#tm2)"/>')
o.append(f'<text x="{gx+W/2}" y="{gy+H+18}" font-size="3.6" fill="{TEAL}" font-weight="700">atom yarıçapı · metalik karakter artar</text>')
o.append(f'<path d="M{gx+W+5} {gy+H} V{gy}" stroke="{U}" stroke-width=".8" marker-end="url(#tm)"/>')
o.append(f'<text transform="translate({gx+W+10} {gy+H/2}) rotate(90)" font-size="3.4" fill="{U}" font-weight="700">İE₁ · EN · ametalik artar</text>')
o.append(f'<path d="M{gx-5} {gy} V{gy+H}" stroke="{TEAL}" stroke-width=".8" marker-end="url(#tm2)"/>')
o.append(f'<text transform="translate({gx-8} {gy+H/2}) rotate(-90)" font-size="3.4" fill="{TEAL}" font-weight="700">yarıçap · metalik artar</text>')
o.append('</g></svg>')
w('trend',''.join(o))

# ---------- 9) alkali İE1 çubukları (bağlam)
al=[('Li',520),('Na',496),('K',419),('Rb',403),('Cs',376)]
o=[f'<svg viewBox="0 0 110 50" class="grafik"><g font-family="Inter" text-anchor="middle">']
bx,by,bh=18,40,31
for v in range(0,601,200):
    yv=by-v/600*bh
    o.append(f'<line x1="{bx-2}" y1="{yv:.1f}" x2="106" y2="{yv:.1f}" stroke="#e5e7f0" stroke-width=".3"/><text x="{bx-3}" y="{yv+1.2:.1f}" font-size="3.3" text-anchor="end" fill="{S}">{v}</text>')
for i,(s,v) in enumerate(al):
    h=v/600*bh; x=bx+4+i*17
    o.append(f'<rect x="{x}" y="{by-h:.1f}" width="10" height="{h:.1f}" rx="1" fill="{U}" fill-opacity="{0.45+0.12*i:.2f}"/>')
    o.append(f'<text x="{x+5}" y="{by-h-1.4:.1f}" font-size="3.3" font-weight="700" fill="{M}">{v}</text><text x="{x+5}" y="{by+4.6}" font-size="3.8" font-weight="800" fill="{M}">{s}</text>')
o.append(f'<line x1="{bx-2}" y1="{by}" x2="106" y2="{by}" stroke="{M}" stroke-width=".4"/>')
o.append(f'<text x="2" y="5" font-size="3.4" text-anchor="start" fill="{M}" font-weight="700">İE₁ (kJ/mol)</text>')
o.append(f'<text x="62" y="49" font-size="3.4" fill="{S}">1A grubu, yukarıdan aşağıya</text>')
o.append('</g></svg>')
w('alkali',''.join(o))

# ---------- 10) test grafiği ardışık 5 element (P,S,Cl,Ar,K) harfli
v5=[1012,1000,1251,1521,419]; L5='XYZTQ'
o=[f'<svg viewBox="0 0 90 52" class="grafik"><g font-family="Inter" text-anchor="middle">']
bx,by=12,42
Xs=lambda i: bx+8+i*16; Ys=lambda v: by-v/1700*34
o.append(f'<line x1="{bx}" y1="{by}" x2="88" y2="{by}" stroke="{M}" stroke-width=".4"/><line x1="{bx}" y1="{by}" x2="{bx}" y2="4" stroke="{M}" stroke-width=".4"/>')
o.append('<polyline fill="none" stroke="%s" stroke-width=".7" points="%s"/>'%(U,' '.join(f'{Xs(i)},{Ys(v):.1f}' for i,v in enumerate(v5))))
for i,v in enumerate(v5):
    o.append(f'<circle cx="{Xs(i)}" cy="{Ys(v):.1f}" r="1.2" fill="{U}"/><text x="{Xs(i)}" y="{by+4.6}" font-size="3.8" font-weight="800" fill="{M}">{L5[i]}</text>')
    o.append(f'<line x1="{Xs(i)}" y1="{by}" x2="{Xs(i)}" y2="{Ys(v):.1f}" stroke="#e5e7f0" stroke-width=".3" stroke-dasharray="1 .8"/>')
    o.append(f'<text x="{Xs(i)-(3.2 if v<600 else 0)}" y="{Ys(v)-2.2 if v>=600 else Ys(v)+1.2:.1f}" font-size="3.4" fill="{UK}" font-weight="700" text-anchor="{"end" if v<600 else "middle"}">{v}</text>')
o.append(f'<text x="2" y="3.5" font-size="3.2" text-anchor="start" fill="{M}" font-weight="700">İE₁</text><text x="60" y="50.5" font-size="3.2" fill="{S}">atom numarası (ardışık) →</text>')
o.append('</g></svg>')
w('test5',''.join(o))

# ---------- 11) H–Cl kısmi yük
o=[f'<svg viewBox="0 0 100 40" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(f'<defs><radialGradient id="eb" cx="65%" cy="50%" r="60%"><stop offset="0" stop-color="{U}" stop-opacity=".55"/><stop offset="1" stop-color="{U}" stop-opacity=".05"/></radialGradient></defs>')
o.append(f'<ellipse cx="46" cy="19" rx="34" ry="13" fill="url(#eb)"/>')
o.append(f'<circle cx="26" cy="19" r="6" fill="#fff" stroke="{S}" stroke-width=".4"/><text x="26" y="20.8" font-size="5" font-weight="800" fill="{M}">H</text>')
o.append(f'<circle cx="58" cy="19" r="10" fill="#fff" fill-opacity=".85" stroke="{U}" stroke-width=".5"/><text x="58" y="20.8" font-size="5.4" font-weight="800" fill="{UK}">Cl</text>')
o.append(f'<text x="26" y="9" font-size="4.6" font-weight="800" fill="{TEAL}">δ+</text><text x="58" y="6" font-size="4.6" font-weight="800" fill="{U}">δ−</text>')
o.append(f'<text x="45" y="38" font-size="3.4" fill="{S}">2,2 &lt; 3,2 · bağ elektronları Cl tarafına kayar</text>')
o.append('</g></svg>')
w('hcl',''.join(o))
print('ok')
