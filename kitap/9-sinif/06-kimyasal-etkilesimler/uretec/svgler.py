"""Kimyasal Etkileşimler ünitesinin SVG'lerini üretir ve Lewis yapılarını denetler.

Çalıştır:  python3 svgler.py      (svg/ klasörüne yazar, denetim raporunu ekrana basar)
Her Lewis yapısında: değerlik elektronu toplamı, oktet/dublet, bağlayıcı ve
ortaklanmamış çift sayıları hesaplanır; beklenen değerle uyuşmazsa betik hata verir.
"""
import math
import os
import random

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg')
os.makedirs(D, exist_ok=True)

U = '#15803d'; UK = '#0d4f26'; UA = '#ecf8f0'
S = '#5d6478'; M = '#1d2133'; AMB = '#f59e0b'; RED = '#e11d48'; IND = '#4f46e5'; TEAL = '#0f8f84'
FONT = 'font-family="Inter"'


def w(ad, s):
    open(os.path.join(D, ad + '.svg'), 'w').write(s)


# ------------------------------------------------------------------ Lewis motoru
DEG = {'H': 1, 'Li': 1, 'Be': 2, 'B': 3, 'C': 4, 'N': 5, 'O': 6, 'F': 7, 'Ne': 8,
       'Na': 1, 'Mg': 2, 'Al': 3, 'Si': 4, 'P': 5, 'S': 6, 'Cl': 7, 'Ar': 8, 'Br': 7, 'K': 1, 'Ca': 2}
HEDEF = {'H': 2, 'B': 6, 'Be': 4}          # dublet / eksik oktet; diğerleri 8

FS = 8.0                                   # sembol yazı boyu
def yari(sym):                             # sembolün yatay yarı genişliği
    return 2.9 if len(sym) == 1 else 4.6
YDIK = 4.0                                 # dikey yarı yükseklik


def kenar(sym, ux, uy):
    """Sembol merkezinden (ux,uy) yönünde sembolün kenarına uzaklık."""
    ax, ay = yari(sym), YDIK
    if abs(ux) < 1e-9:
        return ay
    if abs(uy) < 1e-9:
        return ax
    return min(ax / abs(ux), ay / abs(uy))


def lewis(atomlar, baglar, adim=17, renk_bag=M, renk_cift=U, bag_nokta=False, etiket=None,
          kismi=None, kenar_bosluk=6, beklenen=None, ad=''):
    """atomlar: {id: (sembol, x, y)} ızgara birimi; baglar: [(a, b, derece)].
    Ortaklanmamış çiftler boş yönlere otomatik yerleşir. Denetim sözlüğü döndürür."""
    P = {k: (v[1] * adim, v[2] * adim) for k, v in atomlar.items()}
    bagsay = {k: 0 for k in atomlar}
    yonler = {k: [] for k in atomlar}
    for a, b, d in baglar:
        bagsay[a] += d; bagsay[b] += d
        (xa, ya), (xb, yb) = P[a], P[b]
        L = math.hypot(xb - xa, yb - ya)
        yonler[a].append(((xb - xa) / L, (yb - ya) / L))
        yonler[b].append(((xa - xb) / L, (ya - yb) / L))
    rapor = {'bag_cift': sum(d for _, _, d in baglar), 'ort_cift': 0, 'deg_top': 0}
    cift = {}
    for k, (sym, _, _) in atomlar.items():
        kalan = DEG[sym] - bagsay[k]
        assert kalan >= 0 and kalan % 2 == 0, (ad, k, sym, kalan)
        cift[k] = kalan // 2
        rapor['ort_cift'] += cift[k]
        rapor['deg_top'] += DEG[sym]
        elek = 2 * bagsay[k] + kalan
        assert elek == HEDEF.get(sym, 8), f'{ad}: {sym} çevresinde {elek} elektron'
    assert rapor['deg_top'] == 2 * rapor['bag_cift'] + 2 * rapor['ort_cift'], ad
    if beklenen:
        assert (rapor['bag_cift'], rapor['ort_cift']) == beklenen, (ad, rapor, beklenen)

    o = []
    xs = [p[0] for p in P.values()]; ys = [p[1] for p in P.values()]
    # bağlar
    for a, b, d in baglar:
        (xa, ya), (xb, yb) = P[a], P[b]
        L = math.hypot(xb - xa, yb - ya); ux, uy = (xb - xa) / L, (yb - ya) / L
        ra = kenar(atomlar[a][0], ux, uy) + 1.2; rb = kenar(atomlar[b][0], ux, uy) + 1.2
        x1, y1, x2, y2 = xa + ux * ra, ya + uy * ra, xb - ux * rb, yb - uy * rb
        nx, ny = -uy, ux
        ofs = {1: [0], 2: [-1.25, 1.25], 3: [-2.2, 0, 2.2]}[d]
        if bag_nokta:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            for i in range(d):
                for s in (-1.15, 1.15):
                    cx = mx + nx * s + ux * (i - (d - 1) / 2) * 2.6
                    cy = my + ny * s + uy * (i - (d - 1) / 2) * 2.6 - 0.9
                    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r=".8" fill="{AMB}"/>')
        else:
            for f in ofs:
                o.append(f'<line x1="{x1 + nx*f:.2f}" y1="{y1 + ny*f:.2f}" x2="{x2 + nx*f:.2f}" y2="{y2 + ny*f:.2f}" '
                         f'stroke="{renk_bag}" stroke-width=".7" stroke-linecap="round"/>')
    # ortaklanmamış çiftler
    aday = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for k, (sym, _, _) in atomlar.items():
        n = cift[k]
        if not n:
            continue
        bos = [v for v in aday if all(v[0] * a + v[1] * b < 0.5 for a, b in yonler[k])]
        if len(bos) < n:
            raise ValueError(f'{ad}: {sym} için boş yön yok')
        # zıt yönleri bağın karşısına koymak yerine önce dik yönleri tercih et
        def puan(v):
            if not yonler[k]:
                return 0
            return max(abs(v[0] * a + v[1] * b) for a, b in yonler[k])
        bos.sort(key=puan)
        for vx, vy in bos[:n]:
            x, y = P[k]
            r = kenar(sym, vx, vy) + 1.6
            cx, cy = x + vx * r, y + vy * r + (0.2 if vy == 0 else 0)
            if vy == 0:
                cy -= 0.9  # metin optik merkezi biraz yukarıda
            px, py = -vy, vx
            for s in (-1.15, 1.15):
                o.append(f'<circle cx="{cx + px*s:.2f}" cy="{cy + py*s:.2f}" r=".8" fill="{renk_cift}"/>')
    # semboller
    for k, (sym, _, _) in atomlar.items():
        x, y = P[k]
        o.append(f'<text x="{x:.2f}" y="{y + 2.9:.2f}" text-anchor="middle" font-size="{FS}" font-weight="700" fill="{M}">{sym}</text>')
    # kısmi yükler
    if kismi:
        for k, (txt, dx, dy) in kismi.items():
            x, y = P[k]
            c = RED if '−' in txt else IND
            o.append(f'<text x="{x + dx:.2f}" y="{y + dy:.2f}" text-anchor="middle" font-size="4.6" font-weight="700" fill="{c}">{txt}</text>')
    pad = kenar_bosluk
    x0, x1 = min(xs) - pad - 4, max(xs) + pad + 4
    y0, y1 = min(ys) - pad - 3, max(ys) + pad + 3
    h_ek = 0
    if etiket:
        o.append(f'<text x="{(x0 + x1)/2:.2f}" y="{y1 + 4:.2f}" text-anchor="middle" font-size="4.6" font-weight="700" fill="{UK}">{etiket}</text>')
        h_ek = 6
    vb = f'{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0 + h_ek:.1f}'
    svg = f'<svg viewBox="{vb}" class="lw" style="width:calc(var(--lk, .42mm) * {x1 - x0:.1f})"><g {FONT}>' + ''.join(o) + '</g></svg>'
    return svg, rapor


DENETIM = []
def lw(ad, atomlar, baglar, beklenen, **kw):
    svg, r = lewis(atomlar, baglar, beklenen=beklenen, ad=ad, **kw)
    w(ad, svg)
    DENETIM.append((ad, r))
    return svg


# ---------- Moleküller (beklenen: (bağlayıcı çift, ortaklanmamış çift))
lw('cl2', {'a': ('Cl', 0, 0), 'b': ('Cl', 1, 0)}, [('a', 'b', 1)], (1, 6), etiket='Cl–Cl · tekli bağ')
lw('o2', {'a': ('O', 0, 0), 'b': ('O', 1, 0)}, [('a', 'b', 2)], (2, 4), etiket='O=O · ikili bağ')
lw('n2', {'a': ('N', 0, 0), 'b': ('N', 1, 0)}, [('a', 'b', 3)], (3, 2), etiket='N≡N · üçlü bağ')
lw('h2o2', {'h1': ('H', 0, 0), 'o1': ('O', 1, 0), 'o2': ('O', 2, 0), 'h2': ('H', 3, 0)},
   [('h1', 'o1', 1), ('o1', 'o2', 1), ('o2', 'h2', 1)], (3, 4))
lw('hcl_nokta', {'h': ('H', 0, 0), 'c': ('Cl', 1.05, 0)}, [('h', 'c', 1)], (1, 3), bag_nokta=True)
lw('pcl3', {'p': ('P', 0, 0), 'a': ('Cl', -1.1, 0), 'b': ('Cl', 1.1, 0), 'c': ('Cl', 0, 1)},
   [('p', 'a', 1), ('p', 'b', 1), ('p', 'c', 1)], (3, 10))
lw('h2o', {'o': ('O', 0, 0), 'a': ('H', -1, 0), 'b': ('H', 1, 0)}, [('o', 'a', 1), ('o', 'b', 1)], (2, 2))
lw('nh3', {'n': ('N', 0, 0), 'a': ('H', -1, 0), 'b': ('H', 1, 0), 'c': ('H', 0, 1)},
   [('n', 'a', 1), ('n', 'b', 1), ('n', 'c', 1)], (3, 1))
lw('ch4', {'c': ('C', 0, 0), 'a': ('H', -1, 0), 'b': ('H', 1, 0), 'd': ('H', 0, 1), 'e': ('H', 0, -1)},
   [('c', 'a', 1), ('c', 'b', 1), ('c', 'd', 1), ('c', 'e', 1)], (4, 0))
lw('co2', {'c': ('C', 0, 0), 'a': ('O', -1.1, 0), 'b': ('O', 1.1, 0)}, [('c', 'a', 2), ('c', 'b', 2)], (4, 4))
lw('hcn', {'h': ('H', -1, 0), 'c': ('C', 0, 0), 'n': ('N', 1.1, 0)}, [('h', 'c', 1), ('c', 'n', 3)], (4, 1))
lw('c2h4', {'c1': ('C', 0, 0), 'c2': ('C', 1.1, 0), 'h1': ('H', -.7, -.75), 'h2': ('H', -.7, .75),
            'h3': ('H', 1.8, -.75), 'h4': ('H', 1.8, .75)},
   [('c1', 'c2', 2), ('c1', 'h1', 1), ('c1', 'h2', 1), ('c2', 'h3', 1), ('c2', 'h4', 1)], (6, 0))
lw('ch2o', {'c': ('C', 0, 0), 'o': ('O', 1.1, 0), 'h1': ('H', -.75, -.75), 'h2': ('H', -.75, .75)},
   [('c', 'o', 2), ('c', 'h1', 1), ('c', 'h2', 1)], (4, 2))
lw('n2h4', {'n1': ('N', 0, 0), 'n2': ('N', 1.1, 0), 'h1': ('H', -1, 0), 'h2': ('H', 0, 1),
            'h3': ('H', 2.1, 0), 'h4': ('H', 1.1, 1)},
   [('n1', 'n2', 1), ('n1', 'h1', 1), ('n1', 'h2', 1), ('n2', 'h3', 1), ('n2', 'h4', 1)], (5, 2))
lw('bf3', {'b': ('B', 0, 0), 'a': ('F', -1, 0), 'c': ('F', 1, 0), 'd': ('F', 0, 1)},
   [('b', 'a', 1), ('b', 'c', 1), ('b', 'd', 1)], (3, 9))
lw('nf3', {'n': ('N', 0, 0), 'a': ('F', -1, 0), 'c': ('F', 1, 0), 'd': ('F', 0, 1)},
   [('n', 'a', 1), ('n', 'c', 1), ('n', 'd', 1)], (3, 10))
lw('c2h5oh', {'c1': ('C', 0, 0), 'c2': ('C', 1, 0), 'o': ('O', 2, 0), 'h': ('H', 3, 0),
              'a': ('H', -1, 0), 'b': ('H', 0, -1), 'c': ('H', 0, 1), 'd': ('H', 1, -1), 'e': ('H', 1, 1)},
   [('c1', 'c2', 1), ('c2', 'o', 1), ('o', 'h', 1), ('c1', 'a', 1), ('c1', 'b', 1), ('c1', 'c', 1),
    ('c2', 'd', 1), ('c2', 'e', 1)], (8, 2))

# ---------- Atomların Lewis sembolleri (2. periyot)
def nokta_sembol(sym, x, y, n, renk=U):
    """Noktalar önce dört yana birer birer, sonra ikinciler (sağ, üst, sol, alt)."""
    sira = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    say = [0, 0, 0, 0]
    for i in range(n):
        say[i % 4] += 1
    o = [f'<text x="{x}" y="{y + 2.9}" text-anchor="middle" font-size="{FS}" font-weight="700" fill="{M}">{sym}</text>']
    for (vx, vy), k in zip(sira, say):
        if not k:
            continue
        r = kenar(sym, vx, vy) + 1.6
        cx, cy = x + vx * r, y + vy * r - (0.9 if vy == 0 else 0)
        px, py = -vy, vx
        ofs = [0] if k == 1 else [-1.15, 1.15]
        for s in ofs:
            o.append(f'<circle cx="{cx + px*s:.2f}" cy="{cy + py*s:.2f}" r=".8" fill="{renk}"/>')
    tek = sum(1 for k in say if k == 1)
    return ''.join(o), tek


sat = [('Li', 3), ('Be', 4), ('B', 5), ('C', 6), ('N', 7), ('O', 8), ('F', 9), ('Ne', 10)]
o = [f'<svg viewBox="0 0 184 35" class="grafik"><g {FONT}>']
beklenen_tek = {'Li': 1, 'Be': 2, 'B': 3, 'C': 4, 'N': 3, 'O': 2, 'F': 1, 'Ne': 0}
for i, (s, z) in enumerate(sat):
    x = 14 + i * 22.5
    o.append(f'<rect x="{x-10}" y="1" width="20" height="33" rx="2.4" fill="{UA}"/>')
    o.append(f'<text x="{x}" y="6.4" text-anchor="middle" font-size="3.8" fill="{S}">{DEG[s]} e⁻</text>')
    g, tek = nokta_sembol(s, x, 16.5, DEG[s])
    assert tek == beklenen_tek[s], (s, tek)
    o.append(g)
    o.append(f'<text x="{x}" y="30" text-anchor="middle" font-size="3.8" fill="{UK}">tek: <tspan font-weight="800" font-size="4.6">{tek}</tspan></text>')
o.append('</g></svg>')
w('atomlar', ''.join(o))

# ---------- CaF2 oluşumu (Lewis gösterimiyle)
o = [f'<svg viewBox="0 0 176 34" class="grafik"><g {FONT}>']
g, _ = nokta_sembol('F', 12, 16, 7); o.append(g)
o.append(f'<text x="22" y="18.5" text-anchor="middle" font-size="6" fill="{S}">+</text>')
g, _ = nokta_sembol('Ca', 36, 16, 2, renk=AMB); o.append(g)
o.append(f'<text x="49" y="18.5" text-anchor="middle" font-size="6" fill="{S}">+</text>')
g, _ = nokta_sembol('F', 60, 16, 7); o.append(g)
o.append(f'<defs><marker id="caok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 10 5 0 10z" fill="{U}"/></marker></defs>')
o.append(f'<path d="M72 16 H90" stroke="{U}" stroke-width=".8" marker-end="url(#caok)"/>')
o.append(f'<text x="81" y="12" text-anchor="middle" font-size="4" fill="{UK}">2 e⁻ verir</text>')
# eğri oklar: Ca'dan F'lere
o.append(f'<path d="M33 10 Q24 2 15 9" fill="none" stroke="{AMB}" stroke-width=".5" stroke-dasharray="1 .8" marker-end="url(#caok)"/>')
o.append(f'<path d="M40 10 Q49 2 58 9" fill="none" stroke="{AMB}" stroke-width=".5" stroke-dasharray="1 .8" marker-end="url(#caok)"/>')
def koseli(x, y, gen, sym, n, yuk, renk_n=U, ek_amb=0):
    s = []
    s.append(f'<path d="M{x-gen/2+1.5} {y-9} H{x-gen/2} V{y+9} H{x-gen/2+1.5}" fill="none" stroke="{M}" stroke-width=".5"/>')
    s.append(f'<path d="M{x+gen/2-1.5} {y-9} H{x+gen/2} V{y+9} H{x+gen/2-1.5}" fill="none" stroke="{M}" stroke-width=".5"/>')
    g, _ = nokta_sembol(sym, x, y, n, renk=renk_n)
    s.append(g)
    s.append(f'<text x="{x+gen/2+1}" y="{y-6.5}" font-size="4.2" font-weight="700" fill="{RED if "−" in yuk else IND}">{yuk}</text>')
    return ''.join(s)
o.append(koseli(104, 16, 18, 'F', 8, '−'))
o.append(koseli(130, 16, 16, 'Ca', 0, '2+'))
o.append(koseli(158, 16, 18, 'F', 8, '−'))
o.append(f'<text x="131" y="32.5" text-anchor="middle" font-size="4.2" fill="{S}">katyon : anyon = 1 : 2</text>')
o.append('</g></svg>')
w('caf2', ''.join(o))


# ---------- Katman modeli: Na + Cl -> Na+ + Cl-
def katman(cx, cy, p, dag, etiket, renkler=None, ek=None):
    s = [f'<circle cx="{cx}" cy="{cy}" r="4.6" fill="{RED}" fill-opacity=".85"/>',
         f'<text x="{cx}" y="{cy+1.3}" text-anchor="middle" font-size="3.4" font-weight="800" fill="#fff">{p}p⁺</text>']
    for i, n in enumerate(dag):
        r = 8 + i * 4.6
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#b9c1d4" stroke-width=".35"/>')
        for j in range(n):
            a = -math.pi / 2 + 2 * math.pi * j / n + (0.2 if i == 2 else 0)
            c = M
            if ek and (i, j) in ek:
                c = ek[(i, j)]
            s.append(f'<circle cx="{cx + r*math.cos(a):.2f}" cy="{cy + r*math.sin(a):.2f}" r="1" fill="{c}"/>')
    s.append(f'<text x="{cx}" y="{cy + 8 + (len(dag)-1)*4.6 + 6.5}" text-anchor="middle" font-size="4.8" font-weight="700" fill="{UK}">{etiket}</text>')
    return ''.join(s)

o = [f'<svg viewBox="0 0 188 64" class="grafik"><g {FONT}>']
o.append(f'<defs><marker id="kok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 10 5 0 10z" fill="{AMB}"/></marker>'
         f'<marker id="kok2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 10 5 0 10z" fill="{U}"/></marker></defs>')
o.append(katman(22, 28, 11, [2, 8, 1], 'Na  (2-8-1)', ek={(2, 0): AMB}))
o.append(katman(70, 28, 17, [2, 8, 7], 'Cl  (2-8-7)'))
o.append(f'<path d="M24 10.6 Q46 6 63 9.6" fill="none" stroke="{AMB}" stroke-width=".6" marker-end="url(#kok)"/>')
o.append(f'<text x="44" y="5.2" text-anchor="middle" font-size="4.4" fill="#a16207" font-weight="700">1 e⁻</text>')
o.append(f'<path d="M94 28 H106" stroke="{U}" stroke-width=".8" marker-end="url(#kok2)"/>')
o.append(katman(124, 28, 11, [2, 8], 'Na⁺  (2-8)'))
o.append(katman(166, 28, 17, [2, 8, 8], 'Cl⁻  (2-8-8)', ek={(2, 7): AMB}))
o.append(f'<text x="124" y="7" text-anchor="middle" font-size="4.2" fill="{IND}" font-weight="700">katyon · küçülür</text>')
o.append(f'<text x="166" y="5" text-anchor="middle" font-size="4.2" fill="{RED}" font-weight="700">anyon · büyür</text>')
o.append('</g></svg>')
w('nacl_aktarim', ''.join(o))


# ---------- Elektron denizi: Na ve Mg
def deniz(x0, y0, yuk, e_basina, etiket, tohum):
    rnd = random.Random(tohum)
    s = [f'<rect x="{x0}" y="{y0}" width="78" height="46" rx="3" fill="#eef6ff" stroke="#c9d6ee" stroke-width=".4"/>']
    noktalar = []
    for i in range(5):
        for j in range(3):
            cx = x0 + 10 + i * 14.5 + (7 if j % 2 else 0) - (0 if j % 2 else 0)
            cy = y0 + 9 + j * 13
            if cx > x0 + 72:
                continue
            noktalar.append((cx, cy))
    toplam_e = len(noktalar) * e_basina
    for cx, cy in noktalar:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="4.3" fill="{U}" fill-opacity=".85"/>')
        s.append(f'<text x="{cx}" y="{cy+1.4}" text-anchor="middle" font-size="3.6" font-weight="800" fill="#fff">{yuk}</text>')
    yer = 0
    while yer < toplam_e:
        ex = x0 + 3 + rnd.random() * 72; ey = y0 + 3 + rnd.random() * 40
        if all(math.hypot(ex - a, ey - b) > 5.6 for a, b in noktalar):
            s.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r=".9" fill="{AMB}"/>')
            yer += 1
    s.append(f'<text x="{x0+39}" y="{y0+52}" text-anchor="middle" font-size="4.6" font-weight="700" fill="{UK}">{etiket}</text>')
    return ''.join(s), len(noktalar), toplam_e

o = [f'<svg viewBox="0 0 176 62" class="grafik"><g {FONT}>']
g1, n1, e1 = deniz(2, 2, '+', 1, 'Na: her atom 1 e⁻ verir', 3)
g2, n2, e2 = deniz(96, 2, '2+', 2, 'Mg: her atom 2 e⁻ verir', 7)
assert e1 == n1 and e2 == 2 * n2
o += [g1, g2]
o.append('</g></svg>')
w('deniz', ''.join(o))

# ---------- Erime noktası çubuk grafiği (gerçek veriler, °C)
veri = [('Li', 181, '1A'), ('Na', 98, '1A'), ('K', 63, '1A'), (None, 0, ''), ('Na', 98, '3. per.'), ('Mg', 650, '3. per.'), ('Al', 660, '3. per.')]
x0, y0, yt = 20, 58, 8; ymax = 700
o = [f'<svg viewBox="0 0 150 72" class="grafik"><g {FONT}>']
for v in range(0, 701, 175):
    y = y0 - v / ymax * (y0 - yt)
    o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="146" y2="{y:.1f}" stroke="#e5e7f0" stroke-width=".3"/>')
    o.append(f'<text x="{x0-1.5}" y="{y+1.3:.1f}" text-anchor="end" font-size="3.4" fill="{S}">{v}</text>')
o.append(f'<line x1="{x0}" y1="{y0}" x2="146" y2="{y0}" stroke="{M}" stroke-width=".45"/>')
x = x0 + 6
for s_, v, gr in veri:
    if s_ is None:
        x += 8; continue
    h = v / ymax * (y0 - yt)
    c = U if gr == '1A' else TEAL
    o.append(f'<rect x="{x}" y="{y0-h:.1f}" width="12" height="{h:.1f}" rx="1" fill="{c}"/>')
    o.append(f'<text x="{x+6}" y="{y0-h-1.4:.1f}" text-anchor="middle" font-size="3.6" font-weight="700" fill="{M}">{v}</text>')
    o.append(f'<text x="{x+6}" y="{y0+4.6}" text-anchor="middle" font-size="3.8" font-weight="700" fill="{M}">{s_}</text>')
    x += 17
o.append(f'<text x="{x0+6+25}" y="{y0+10}" text-anchor="middle" font-size="3.4" fill="{U}" font-weight="700">1A grubu (aşağı doğru)</text>')
o.append(f'<text x="{x0+6+51+8+25}" y="{y0+10}" text-anchor="middle" font-size="3.4" fill="{TEAL}" font-weight="700">3. periyot (sağa doğru)</text>')
o.append(f'<text x="2" y="4.5" font-size="3.8" font-weight="700" fill="{M}">Erime noktası (°C)</text>')
o.append('</g></svg>')
w('erime', ''.join(o))

# ---------- Bağlam sorusu: alkali metaller erime noktası
veri = [('Li', 181), ('Na', 98), ('K', 64), ('Rb', 39), ('Cs', 28)]
x0, y0, yt = 18, 50, 6; ymax = 200
o = [f'<svg viewBox="0 0 130 62" class="grafik"><g {FONT}>']
for v in range(0, 201, 50):
    y = y0 - v / ymax * (y0 - yt)
    o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="126" y2="{y:.1f}" stroke="#e5e7f0" stroke-width=".3"/>')
    o.append(f'<text x="{x0-1.5}" y="{y+1.3:.1f}" text-anchor="end" font-size="3.4" fill="{S}">{v}</text>')
y25 = y0 - 25 / ymax * (y0 - yt)
o.append(f'<line x1="{x0}" y1="{y25:.1f}" x2="126" y2="{y25:.1f}" stroke="{RED}" stroke-width=".45" stroke-dasharray="1.6 1"/>')
o.append(f'<text x="125" y="{y25-1.2:.1f}" text-anchor="end" font-size="3.2" fill="{RED}" font-weight="700">25 °C</text>')
o.append(f'<line x1="{x0}" y1="{y0}" x2="126" y2="{y0}" stroke="{M}" stroke-width=".45"/>')
for i, (s_, v) in enumerate(veri):
    x = x0 + 6 + i * 20.5
    h = v / ymax * (y0 - yt)
    o.append(f'<rect x="{x}" y="{y0-h:.1f}" width="11" height="{h:.1f}" rx="1" fill="{U}" fill-opacity="{1 - i*0.13:.2f}"/>')
    o.append(f'<text x="{x+5.5}" y="{y0-h-1.4:.1f}" text-anchor="middle" font-size="3.6" font-weight="700" fill="{M}">{v}</text>')
    o.append(f'<text x="{x+5.5}" y="{y0+4.6}" text-anchor="middle" font-size="3.8" font-weight="700" fill="{M}">{s_}</text>')
o.append(f'<text x="{(x0+126)/2}" y="{y0+10}" text-anchor="middle" font-size="3.4" fill="{S}">1A grubunda yukarıdan aşağıya</text>')
o.append(f'<text x="2" y="3.6" font-size="3.6" font-weight="700" fill="{M}">Erime noktası (°C)</text>')
o.append('</g></svg>')
w('alkali', ''.join(o))

# ---------- NaCl kristali (izometrik)
o = [f'<svg viewBox="2 4 82 76" class="grafik"><g {FONT}>']
top = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            top.append((i, j, k))
def proj(i, j, k):
    return 10 + i * 20 + j * 9, 64 - k * 20 - j * 5
top.sort(key=lambda t: (-t[1], t[2], t[0]))
# çizgiler
for i, j, k in top:
    for di, dj, dk in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        a, b, c = i + di, j + dj, k + dk
        if a < 3 and b < 3 and c < 3:
            x1, y1 = proj(i, j, k); x2, y2 = proj(a, b, c)
            o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#b9c1d4" stroke-width=".35"/>')
for i, j, k in top:
    x, y = proj(i, j, k)
    if (i + j + k) % 2 == 0:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="{U}" stroke="#fff" stroke-width=".4"/>')
    else:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{AMB}" stroke="#fff" stroke-width=".4"/>')
o.append(f'<circle cx="56" cy="75" r="2.6" fill="{U}"/><text x="60" y="76.3" font-size="3.8" fill="{M}">Cl⁻</text>')
o.append(f'<circle cx="71" cy="75" r="1.6" fill="{AMB}"/><text x="74" y="76.3" font-size="3.8" fill="{M}">Na⁺</text>')
o.append('</g></svg>')
w('nacl_kristal', ''.join(o))

# ---------- Bağ türleri ağacı
o = [f'<svg viewBox="0 0 126 46" class="grafik"><g {FONT} text-anchor="middle">']
o.append(f'<rect x="18" y="1" width="90" height="10" rx="3" fill="{U}"/><text x="63" y="7.6" font-size="4.6" font-weight="800" fill="#fff">GÜÇLÜ ETKİLEŞİM = KİMYASAL BAĞ</text>')
kol = [(21, 'METALİK', 'metal + metal', 'Fe, Cu, pirinç'),
       (63, 'İYONİK', 'metal + ametal', 'NaCl, MgO'),
       (105, 'KOVALENT', 'ametal + ametal', 'H₂, H₂O, CO₂')]
for x, a, b, c in kol:
    o.append(f'<path d="M63 11 V14.5 H{x} V18" fill="none" stroke="{UK}" stroke-width=".45"/>')
    o.append(f'<rect x="{x-20}" y="18" width="40" height="27" rx="3" fill="{UA}" stroke="{U}" stroke-width=".4"/>')
    o.append(f'<text x="{x}" y="25.5" font-size="4.8" font-weight="800" fill="{UK}">{a}</text>')
    o.append(f'<text x="{x}" y="32.5" font-size="4.2" fill="{M}">{b}</text>')
    o.append(f'<text x="{x}" y="40" font-size="4" fill="{S}">{c}</text>')
o.append('</g></svg>')
w('agac', ''.join(o))

# ---------- H–H ve H–Cl elektron bulutu
o = [f'<svg viewBox="4 0 142 35" class="grafik"><g {FONT} text-anchor="middle">']
o.append('<defs><radialGradient id="eb1" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#86efac"/><stop offset="1" stop-color="#86efac" stop-opacity=".15"/></radialGradient>'
         '<radialGradient id="eb2" cx="68%" cy="50%" r="55%"><stop offset="0" stop-color="#86efac"/><stop offset="1" stop-color="#86efac" stop-opacity=".12"/></radialGradient></defs>')
o.append('<ellipse cx="34" cy="16" rx="24" ry="11" fill="url(#eb1)"/>')
o.append(f'<circle cx="24" cy="16" r="1.4" fill="{M}"/><circle cx="44" cy="16" r="1.4" fill="{M}"/>')
o.append(f'<text x="24" y="11" font-size="4.6" font-weight="700" fill="{M}">H</text><text x="44" y="11" font-size="4.6" font-weight="700" fill="{M}">H</text>')
o.append(f'<text x="34" y="32" font-size="4.6" font-weight="700" fill="{UK}">apolar: eşit paylaşım</text>')
o.append('<ellipse cx="112" cy="16" rx="30" ry="12" fill="url(#eb2)"/>')
o.append(f'<circle cx="96" cy="16" r="1.4" fill="{M}"/><circle cx="122" cy="16" r="2" fill="{M}"/>')
o.append(f'<text x="96" y="11" font-size="4.6" font-weight="700" fill="{M}">H</text><text x="122" y="10.5" font-size="4.6" font-weight="700" fill="{M}">Cl</text>')
o.append(f'<text x="88" y="18" font-size="4.4" font-weight="700" fill="{IND}">δ+</text><text x="138" y="18" font-size="4.4" font-weight="700" fill="{RED}">δ−</text>')
o.append(f'<text x="112" y="32" font-size="4.6" font-weight="700" fill="{UK}">polar: elektronlar Cl’ye kayar</text>')
o.append('</g></svg>')
w('bulut', ''.join(o))

# ---------- Molekül polarlığı panosu (2B şekiller, bağ dipolleri)
def ok(x1, y1, x2, y2, c, gen=.6):
    # dipol oku: + ucu küçük çizgi, uç ok başı
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = -uy, ux
    s = f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2 - ux*1.6:.2f}" y2="{y2 - uy*1.6:.2f}" stroke="{c}" stroke-width="{gen}"/>'
    s += f'<path d="M{x2:.2f} {y2:.2f} L{x2 - ux*2.2 + nx*1.1:.2f} {y2 - uy*2.2 + ny*1.1:.2f} L{x2 - ux*2.2 - nx*1.1:.2f} {y2 - uy*2.2 - ny*1.1:.2f}z" fill="{c}"/>'
    px, py = x1 + ux * 1.2, y1 + uy * 1.2
    s += f'<line x1="{px + nx*1.1:.2f}" y1="{py + ny*1.1:.2f}" x2="{px - nx*1.1:.2f}" y2="{py - ny*1.1:.2f}" stroke="{c}" stroke-width="{gen}"/>'
    return s

def panel(x0, y0, baslik, merkez, cevre, lp_yon, sonuc, polar, net=None):
    """cevre: [(sembol, açı derece, uzunluk, bağ derecesi)] ; lp_yon: merkez çiftlerinin açıları"""
    G, Y = 42, 47
    s = [f'<rect x="{x0}" y="{y0}" width="{G}" height="{Y}" rx="3" fill="{"#fff1f3" if polar else UA}" stroke="{RED if polar else U}" stroke-width=".4"/>']
    s.append(f'<text x="{x0+G/2}" y="{y0+6.4}" text-anchor="middle" font-size="5" font-weight="800" fill="{M}">{baslik}</text>')
    cx, cy = x0 + G/2 + 2, y0 + 24
    s.append(f'<text x="{cx}" y="{cy+2.1}" text-anchor="middle" font-size="5.8" font-weight="800" fill="{M}">{merkez}</text>')
    en = {'H': 2.2, 'C': 2.6, 'N': 3.0, 'O': 3.4, 'F': 4.0, 'Cl': 3.2, 'B': 2.0, 'S': 2.6}
    for sym, a, L, der in cevre:
        r = math.radians(a); ux, uy = math.cos(r), -math.sin(r)
        nx, ny = -uy, ux
        ex, ey = cx + ux * L, cy + uy * L
        uc = 2.9 + (1.6 if len(sym) == 2 and abs(ux) > .5 else 0)
        for f in {1: [0], 2: [-.8, .8]}[der]:
            s.append(f'<line x1="{cx + ux*3.6 + nx*f:.2f}" y1="{cy + uy*3.6 + ny*f:.2f}" x2="{ex - ux*uc + nx*f:.2f}" y2="{ey - uy*uc + ny*f:.2f}" stroke="{M}" stroke-width=".45"/>')
        s.append(f'<text x="{ex:.2f}" y="{ey+1.9:.2f}" text-anchor="middle" font-size="5.2" font-weight="700" fill="{M}">{sym}</text>')
        d = en[sym] - en[merkez]
        if abs(d) > 0.05:  # bağ dipolü: elektronegatif uca doğru
            k = 2.9 if der == 1 else 3.4
            a1, a2 = (0.30, 0.80) if d > 0 else (0.80, 0.30)
            s.append(ok(cx + ux*L*a1 + nx*k, cy + uy*L*a1 + ny*k, cx + ux*L*a2 + nx*k, cy + uy*L*a2 + ny*k, IND, .42))
    for a in lp_yon:
        r = math.radians(a); ux, uy = math.cos(r), -math.sin(r)
        px, py = -uy, ux
        mx, my = cx + ux * 5.6, cy + uy * 5.6 - 0.4
        for t in (-1.0, 1.0):
            s.append(f'<circle cx="{mx + px*t:.2f}" cy="{my + py*t:.2f}" r=".7" fill="{U}"/>')
    if net:
        s.append(ok(net[0] + x0, net[1] + y0, net[2] + x0, net[3] + y0, RED, .8))
    s.append(f'<text x="{x0+G/2}" y="{y0+Y-2.6}" text-anchor="middle" font-size="4" font-weight="800" fill="{RED if polar else UK}">{sonuc}</text>')
    return ''.join(s)

o = [f'<svg viewBox="0 0 265 49" class="grafik"><g {FONT}>']
o.append(panel(1, 1, 'CO₂', 'C', [('O', 180, 12.5, 2), ('O', 0, 12.5, 2)], [], 'APOLAR · μ = 0', False))
o.append(panel(45, 1, 'BF₃', 'B', [('F', 90, 12, 1), ('F', 210, 12, 1), ('F', 330, 12, 1)], [], 'APOLAR · μ = 0', False))
o.append(panel(89, 1, 'CCl₄', 'C', [('Cl', 90, 11, 1), ('Cl', 270, 11, 1), ('Cl', 180, 13, 1), ('Cl', 0, 13, 1)], [], 'APOLAR · μ = 0', False))
o.append(panel(133, 1, 'H₂O', 'O', [('H', 215, 12, 1), ('H', 325, 12, 1)], [60, 120], 'POLAR · μ ≠ 0', True, net=(4.5, 32, 4.5, 15)))
o.append(panel(177, 1, 'NH₃', 'N', [('H', 180, 12, 1), ('H', 0, 12, 1), ('H', 270, 11, 1)], [90], 'POLAR · μ ≠ 0', True, net=(4.5, 32, 4.5, 15)))
o.append(panel(221, 1, 'CHCl₃', 'C', [('H', 90, 11, 1), ('Cl', 270, 11, 1), ('Cl', 180, 13, 1), ('Cl', 0, 13, 1)], [], 'POLAR · μ ≠ 0', True, net=(4.5, 15, 4.5, 32)))
o.append('</g></svg>')
w('polarlik', ''.join(o))

# ---------- Polarlık karar şeması
o = [f'<svg viewBox="0 0 132 96" class="grafik"><g {FONT} text-anchor="middle">']
def kutu(x, y, gen, yuk, t1, t2='', renk=UA, cer=U, tc=M, kalin=False):
    s = f'<rect x="{x-gen/2}" y="{y}" width="{gen}" height="{yuk}" rx="2.4" fill="{renk}" stroke="{cer}" stroke-width=".4"/>'
    s += f'<text x="{x}" y="{y + (yuk/2 + 1.3 if not t2 else yuk/2 - 1.2)}" font-size="3.7" font-weight="{800 if kalin else 600}" fill="{tc}">{t1}</text>'
    if t2:
        s += f'<text x="{x}" y="{y + yuk/2 + 3.4}" font-size="3.7" font-weight="{800 if kalin else 600}" fill="{tc}">{t2}</text>'
    return s
def cizgi(x1, y1, x2, y2, et='', ex=0, ey=0):
    s = f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{S}" stroke-width=".4"/>'
    if et:
        s += f'<text x="{ex}" y="{ey}" font-size="3.3" font-weight="700" fill="{S}">{et}</text>'
    return s
o.append(kutu(66, 1, 64, 9, 'Molekül kaç atomlu?', kalin=True, renk='#fff', cer=UK))
o.append(cizgi(44, 10, 24, 19, 'iki', 30, 14)); o.append(cizgi(88, 10, 92, 19, 'üç ve fazlası', 104, 14))
o.append(kutu(24, 19, 40, 9, 'Atomlar aynı mı?'))
o.append(cizgi(14, 28, 12, 38, 'evet', 8, 33.5)); o.append(cizgi(34, 28, 36, 38, 'hayır', 41, 33.5))
o.append(kutu(12, 38, 22, 12, 'APOLAR', 'H₂, N₂, O₂', renk='#fff', cer=U, tc=UK, kalin=True))
o.append(kutu(36, 38, 22, 12, 'POLAR', 'HCl, CO', renk='#fff1f3', cer=RED, tc=RED, kalin=True))
o.append(kutu(92, 19, 64, 13, 'Merkez atomda ortaklanmamış', 'elektron çifti var mı?'))
o.append(cizgi(112, 32, 118, 42, 'var', 120, 37)); o.append(cizgi(80, 32, 82, 42, 'yok', 76, 37.5))
o.append(kutu(118, 42, 24, 12, 'POLAR', 'H₂O, NH₃', renk='#fff1f3', cer=RED, tc=RED, kalin=True))
o.append(kutu(82, 42, 44, 13, 'Merkeze bağlı atomlar', 'hepsi aynı mı?'))
o.append(cizgi(72, 55, 66, 66, 'evet', 64, 60.5)); o.append(cizgi(92, 55, 104, 66, 'hayır', 104, 60.5))
o.append(kutu(66, 66, 36, 12, 'APOLAR', 'CO₂, BF₃, CH₄', renk='#fff', cer=U, tc=UK, kalin=True))
o.append(kutu(108, 66, 36, 12, 'POLAR', 'CH₃Cl, HCN', renk='#fff1f3', cer=RED, tc=RED, kalin=True))
o.append(f'<text x="66" y="88" font-size="3.4" fill="{S}">Yalnızca C ve H içeren moleküller (hidrokarbonlar)</text>')
o.append(f'<text x="66" y="92.6" font-size="3.4" fill="{S}">apolar kabul edilir: CH₄, C₂H₆, C₃H₈ …</text>')
o.append('</g></svg>')
w('karar', ''.join(o))

# ------------------------------------------------------------------ denetim raporu
for ad, r in DENETIM:
    print(f'{ad:8s} değerlik e⁻ toplamı {r["deg_top"]:2d} · bağlayıcı çift {r["bag_cift"]} · ortaklanmamış çift {r["ort_cift"]} (= {2*r["ort_cift"]} e⁻)')
print('Tüm Lewis yapıları oktet/dublet denetiminden geçti.')
