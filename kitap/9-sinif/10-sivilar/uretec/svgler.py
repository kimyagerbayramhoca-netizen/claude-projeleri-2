"""Sıvılar ünitesinin SVG çizimlerini üretir (uretec/svg/*.svg).

Buhar basıncı değerleri Antoine denkleminden (mmHg, °C) hesaplanır:
  su      A=8.07131 B=1730.63 C=233.426 (1–100 °C), A=8.14019 B=1810.94 C=244.485 (100 °C üstü)
  etanol  A=8.20417 B=1642.89 C=230.3
  dietil eter A=6.92032 B=1064.07 C=228.8
"""
import math
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg')
os.makedirs(D, exist_ok=True)
U = '#7c2d12'; UK = '#4a1a0a'; UA = '#fcf1ec'; S = '#5d6478'; M = '#1d2133'
AMB = '#f59e0b'; TEAL = '#0f8f84'; IND = '#4f46e5'
SU = '#dbeafe'; SUK = '#3b82f6'; SUD = '#1d4ed8'
CAM = '#94a3b8'


def w(n, s):
    open(os.path.join(D, n + '.svg'), 'w', encoding='utf-8').write(s)


def pw(T):
    A, B, C = (8.07131, 1730.63, 233.426) if T <= 100 else (8.14019, 1810.94, 244.485)
    return 10 ** (A - B / (C + T))


def tw(P):
    A, B, C = (8.07131, 1730.63, 233.426) if P <= 760 else (8.14019, 1810.94, 244.485)
    return B / (A - math.log10(P)) - C


pe = lambda T: 10 ** (8.20417 - 1642.89 / (230.3 + T))
pd = lambda T: 10 ** (6.92032 - 1064.07 / (228.8 + T))


def ok(renk, id_, w_=4):
    return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{w_}" markerHeight="{w_}" '
            f'orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="{renk}"/></marker>')


def t(x, y, s, fs=3.6, anc='middle', fw='400', fill=M, extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" text-anchor="{anc}" font-weight="{fw}" fill="{fill}" {extra}>{s}</text>'


def alt(base, sub, fs):
    """P<sub>buhar</sub> benzeri SVG yazımı."""
    return f'{base}<tspan font-size="{fs*0.68:.2f}" dy="{fs*0.25:.2f}">{sub}</tspan><tspan dy="{-fs*0.25:.2f}"> </tspan>'


def mol(x, y, r=2.2, fill='#93c5fd', stroke=SUD):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width=".35"/>'


# =========================================================
# 1) Buharlaşma: yüzeyden kopan hızlı tanecikler
# =========================================================
o = ['<svg viewBox="0 0 130 80" class="grafik"><defs>' + ok(AMB, 'bh-a') + ok('#ef4444', 'bh-k') + '</defs><g font-family="Inter">']
o.append(f'<rect x="22.5" y="40" width="67" height="35.6" fill="{SU}"/>')
o.append(f'<path d="M22 22 V72 Q22 76 26 76 H86 Q90 76 90 72 V22" fill="none" stroke="{CAM}" stroke-width="1.1"/>')
o.append(f'<line x1="22.5" y1="40" x2="89.5" y2="40" stroke="{SUK}" stroke-width=".5"/>')
import random
random.seed(7)
yuzey_hizli = [(47, 43.2), (72, 43.4)]
for j, yy in enumerate([43.4, 50, 56.6, 63.2, 69.8]):
    for i in range(10):
        xx = 27 + i * 6.4 + (3.2 if j % 2 else 0) + random.uniform(-.7, .7)
        if xx > 86:
            continue
        if any(abs(xx - a) < 3.5 and abs(yy - b) < 2 for a, b in yuzey_hizli):
            continue
        o.append(mol(xx, yy + random.uniform(-.6, .6)))
for a, b in yuzey_hizli:
    o.append(mol(a, b, fill='#fcd34d', stroke='#b45309'))
# kopan tanecikler
for (a, b) in [(56, 30), (66, 18), (40, 13)]:
    o.append(mol(a, b, fill='#fcd34d', stroke='#b45309'))
    o.append(f'<path d="M{a-1.6} {b+4.2} L{a-3} {b+9}" stroke="{AMB}" stroke-width=".6" marker-start="url(#bh-a)"/>')
o.append(f'<path d="M47 39.8 V33.6" stroke="{AMB}" stroke-width=".6" marker-end="url(#bh-a)"/>')
o.append(f'<path d="M72 39.8 V33.6" stroke="{AMB}" stroke-width=".6" marker-end="url(#bh-a)"/>')
# ısı
for x in (36, 56, 76):
    o.append(f'<path d="M{x} 79.6 q1.2 -1 0 -2 q-1.2 -1 0 -2" fill="none" stroke="#ef4444" stroke-width=".55" marker-end="url(#bh-k)"/>')
o.append(t(97, 15, 'Buhar fazı', 4, 'start', '700', UK))
o.append(t(97, 20, 'yüzeyi terk eden', 3.3, 'start', '400', S))
o.append(t(97, 24, 'tanecikler', 3.3, 'start', '400', S))
o.append(f'<circle cx="99" cy="37" r="2" fill="#fcd34d" stroke="#b45309" stroke-width=".35"/>')
o.append(t(103, 38.2, 'kinetik enerjisi', 3.3, 'start'))
o.append(t(103, 42.2, 'yeterli olan', 3.3, 'start'))
o.append(t(103, 46.2, 'yüzey taneciği', 3.3, 'start'))
o.append(mol(99, 58, 2))
o.append(t(103, 59.2, 'çekim kuvvetini', 3.3, 'start'))
o.append(t(103, 63.2, 'yenemeyen', 3.3, 'start'))
o.append(t(103, 67.2, 'tanecikler', 3.3, 'start'))
o.append(t(56, 7, 'Sıvı(s) + ısı → Buhar(g)', 4, 'middle', '700', U))
o.append('</g></svg>')
w('buharlasma', ''.join(o))

# =========================================================
# 2) Kinetik enerji dağılımı: iki sıcaklık
# =========================================================
x0, x1, y0, y1 = 14, 114, 56, 8
Emax = 8.0
Ea = 4.0


def f(E, kT):
    return 2 / math.sqrt(math.pi) * kT ** -1.5 * math.sqrt(E) * math.exp(-E / kT)


fmax = max(f(i / 100, 1.0) for i in range(1, 800))
X = lambda E: x0 + E / Emax * (x1 - x0)
Y = lambda v: y0 - v / fmax * (y0 - y1) * 0.92
o = ['<svg viewBox="0 0 120 66" class="grafik"><defs>' + ok(M, 'en-o', 3) + '</defs><g font-family="Inter">']
for kT, renk, op in [(1.8, AMB, .35), (1.0, U, .45)]:
    pts = [(X(i / 50), Y(f(i / 50, kT))) for i in range(1, 401)]
    alan = [(X(Ea), y0)] + [(a, b) for a, b in pts if a >= X(Ea)] + [(X(Emax), y0)]
    o.append('<polygon fill="%s" fill-opacity="%s" points="%s"/>' % (renk, op, ' '.join(f'{a:.1f},{b:.1f}' for a, b in alan)))
    o.append('<polyline fill="none" stroke="%s" stroke-width=".8" points="%s"/>' % (renk if renk != AMB else '#d97706', ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)))
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1+2}" y2="{y0}" stroke="{M}" stroke-width=".5" marker-end="url(#en-o)"/>')
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1-3}" stroke="{M}" stroke-width=".5" marker-end="url(#en-o)"/>')
o.append(f'<line x1="{X(Ea):.1f}" y1="{y0}" x2="{X(Ea):.1f}" y2="{y1+4}" stroke="{M}" stroke-width=".45" stroke-dasharray="1.4 1"/>')
o.append(t(X(Ea) + 1.5, y1 + 6, 'Buhar fazına geçmek için', 3.2, 'start', '700'))
o.append(t(X(Ea) + 1.5, y1 + 10, 'gereken en az enerji', 3.2, 'start', '700'))
o.append(t(X(0.9), Y(f(0.5, 1.0)) - 2, 'Düşük sıcaklık', 3.3, 'start', '700', U))
o.append(t(X(2.6), Y(f(2.6, 1.8)) - 3.2, 'Yüksek sıcaklık', 3.3, 'start', '700', '#b45309'))
o.append(t(X(5.6), y0 - 6, 'Yeterli enerjili', 3, 'middle', '400', S))
o.append(t(X(5.6), y0 - 2.6, 'tanecikler', 3, 'middle', '400', S))
o.append(t((x0 + x1) / 2, y0 + 5.5, 'Taneciklerin kinetik enerjisi', 3.4, 'middle', '700'))
o.append(t(x0 - 2.5, (y0 + y1) / 2, 'Tanecik sayısı', 3.4, 'middle', '700', M, f'transform="rotate(-90 {x0-2.5} {(y0+y1)/2})"'))
o.append('</g></svg>')
w('enerji', ''.join(o))

# =========================================================
# 3) Buharlaşma hızının üç etkeni
# =========================================================


def kap(cx, gen, ust, renk_s, n, etiket, alt_et, idm):
    s = []
    alt_y = 38
    s.append(f'<rect x="{cx-gen/2+.4:.1f}" y="{ust}" width="{gen-.8:.1f}" height="{alt_y-ust-.4:.1f}" fill="{renk_s}"/>')
    s.append(f'<path d="M{cx-gen/2:.1f} {ust-4} V{alt_y-1.5} Q{cx-gen/2:.1f} {alt_y} {cx-gen/2+1.5:.1f} {alt_y} H{cx+gen/2-1.5:.1f} Q{cx+gen/2:.1f} {alt_y} {cx+gen/2:.1f} {alt_y-1.5} V{ust-4}" fill="none" stroke="{CAM}" stroke-width=".7"/>')
    for i in range(n):
        xx = cx - (n - 1) * 2.6 + i * 5.2
        yy = ust - 6 - (i % 2) * 3.4
        s.append(mol(xx, yy, 1.3, '#fcd34d', '#b45309'))
        s.append(f'<path d="M{xx:.1f} {ust-.6:.1f} V{yy+2.2:.1f}" stroke="{AMB}" stroke-width=".45" marker-end="url(#{idm})"/>')
    s.append(t(cx, alt_y + 4.2, etiket, 3.2, 'middle', '700'))
    s.append(t(cx, alt_y + 8, alt_et, 3, 'middle', '400', S))
    return ''.join(s)


o = ['<svg viewBox="0 0 180 56" class="grafik"><defs>' + ok(AMB, 'et-a', 3) + '</defs><g font-family="Inter">']
paneller = [
    ('1 · Sıvının cinsi', [(15, 16, 26, SU, 2, 'Su', '20 °C · S'), (43, 16, 26, '#fde7d9', 5, 'Aseton', '20 °C · S')], 'Etkileşim zayıf → hız büyük'),
    ('2 · Yüzey alanı', [(73, 12, 26, SU, 2, 'Su', '20 °C · S'), (103, 28, 26, SU, 5, 'Su', '20 °C · 2S')], 'Alan büyük → hız büyük'),
    ('3 · Sıcaklık', [(135, 16, 26, SU, 2, 'Su', '20 °C · S'), (163, 16, 26, '#fecaca', 5, 'Su', '50 °C · S')], 'Sıcaklık yüksek → hız büyük'),
]
bx = [(1, 57), (61, 119), (123, 179)]
for (bas, kaplar, sonuc), (a, b) in zip(paneller, bx):
    o.append(f'<rect x="{a}" y="1" width="{b-a}" height="54" rx="2.4" fill="#fff" stroke="#ead7cf" stroke-width=".4"/>')
    o.append(t((a + b) / 2, 7, bas, 3.6, 'middle', '800', U))
    for k in kaplar:
        o.append(kap(*k, 'et-a'))
    o.append(f'<rect x="{a+3}" y="47.6" width="{b-a-6}" height="5.4" rx="1.4" fill="{UA}"/>')
    o.append(t((a + b) / 2, 51.4, sonuc, 3.1, 'middle', '700', UK))
o.append('</g></svg>')
w('etkenler', ''.join(o))

# =========================================================
# 4) Kapalı kapta denge + hız-zaman grafiği
# =========================================================
o = ['<svg viewBox="0 0 180 54" class="grafik"><defs>' + ok(AMB, 'dg-a', 3) + ok(TEAL, 'dg-t', 3) + ok(M, 'dg-o', 3) + '</defs><g font-family="Inter">']
durumlar = [(20, 28, 0, 3, 0, 'Kap kapatıldı', 'yalnızca buharlaşma'),
            (60, 29.5, 4, 3, 1, 'Buharlaşma > yoğuşma', 'sıvı azalıyor'),
            (100, 30.5, 8, 3, 3, 'Denge', 'buharlaşma = yoğuşma')]
random.seed(3)
for cx, sev, nb, up, dn, e1, e2 in durumlar:
    l, r, top, bot = cx - 15, cx + 15, 6, 40
    o.append(f'<rect x="{l+.4}" y="{sev}" width="{r-l-.8}" height="{bot-sev-.4}" fill="{SU}"/>')
    o.append(f'<rect x="{l}" y="{top}" width="{r-l}" height="{bot-top}" rx="1.6" fill="none" stroke="{CAM}" stroke-width=".8"/>')
    o.append(f'<rect x="{l-1.5}" y="{top-2.4}" width="{r-l+3}" height="2.4" rx=".8" fill="{U}"/>')
    for i in range(nb):
        o.append(mol(l + 4 + (i * 7.3) % 22 + random.uniform(-1, 1), top + 3.5 + (i * 11) % 13 + random.uniform(0, 1.5), 1.2, '#fcd34d', '#b45309'))
    for i in range(up):
        xx = l + 6 + i * 9
        o.append(f'<path d="M{xx} {sev-1} V{sev-8}" stroke="{AMB}" stroke-width=".55" marker-end="url(#dg-a)"/>')
    for i in range(dn):
        xx = l + 10.5 + i * 9 - (4.5 if dn == 1 else 0) + (0 if dn == 1 else -4.5)
        o.append(f'<path d="M{xx} {sev-8} V{sev-1}" stroke="{TEAL}" stroke-width=".55" marker-end="url(#dg-t)"/>')
    o.append(t(cx, 45, e1, 3.2, 'middle', '700', UK))
    o.append(t(cx, 49.4, e2, 3, 'middle', '400', S))
# grafik
gx0, gx1, gy0, gy1 = 128, 176, 38, 6
o.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx1+1}" y2="{gy0}" stroke="{M}" stroke-width=".45" marker-end="url(#dg-o)"/>')
o.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx0}" y2="{gy1-2}" stroke="{M}" stroke-width=".45" marker-end="url(#dg-o)"/>')
o.append(f'<line x1="{gx0}" y1="15" x2="{gx1-2}" y2="15" stroke="{AMB}" stroke-width=".9"/>')
pts = [(gx0 + i, 15 + (gy0 - 15) * math.exp(-i / 6.5)) for i in range(0, 47)]
o.append('<polyline fill="none" stroke="%s" stroke-width=".9" points="%s"/>' % (TEAL, ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)))
o.append(f'<line x1="156" y1="{gy0}" x2="156" y2="9" stroke="{S}" stroke-width=".35" stroke-dasharray="1 .8"/>')
o.append(t(157, 8.5, 'denge', 3, 'start', '700', S))
o.append(t(gx0 + 2, 12.6, 'buharlaşma hızı', 3, 'start', '700', '#b45309'))
o.append(t(gx0 + 5, 29, 'yoğuşma hızı', 3, 'start', '700', TEAL))
o.append(t(gx0 - 1.5, gy1 + 1, 'hız', 3.2, 'end', '700'))
o.append(t(gx1, gy0 + 4.4, 'zaman', 3.2, 'end', '700'))
o.append(t(152, 45, 'Sabit sıcaklıkta hızlar', 3, 'middle', '700', UK))
o.append(t(152, 49.4, 'eşitlenince sıvı miktarı sabit', 3, 'middle', '400', S))
o.append('</g></svg>')
w('denge', ''.join(o))

# =========================================================
# 5) Manometre ile buhar basıncı
# =========================================================
o = ['<svg viewBox="0 0 120 80" class="grafik"><g font-family="Inter">']
# kap
o.append(f'<rect x="10.4" y="52" width="35.2" height="21.6" fill="{SU}"/>')
o.append(f'<rect x="10" y="20" width="36" height="54" rx="2" fill="none" stroke="{CAM}" stroke-width=".9"/>')
random.seed(11)
for i in range(7):
    o.append(mol(15 + (i * 9.1) % 27, 25 + (i * 7) % 23, 1.2, '#fcd34d', '#b45309'))
o.append(t(28, 64, 'Sıvı', 3.6, 'middle', '700', SUD))
o.append(t(22, 17, 'Buhar', 3.6, 'middle', '700', '#b45309'))
# borular
o.append(f'<path d="M40 20 V8 H68 V70 A9 9 0 0 0 86 70 V12" fill="none" stroke="#e2e8f0" stroke-width="5.2" stroke-linejoin="round"/>')
o.append(f'<path d="M28 20 V8 H68 V70 A9 9 0 0 0 86 70 V12" fill="none" stroke="{CAM}" stroke-width=".35" stroke-dasharray="0" opacity=".0"/>')
o.append(f'<path d="M68 52 V70 A9 9 0 0 0 86 70 V32" fill="none" stroke="#6b7280" stroke-width="4.2"/>')
o.append(f'<rect x="83.2" y="10.6" width="5.6" height="1.6" fill="{CAM}"/>')
o.append(t(97, 16.5, 'vakum', 3.3, 'start', '700', S))
o.append(f'<line x1="89" y1="15.4" x2="96" y2="15.4" stroke="{S}" stroke-width=".3"/>')
o.append(f'<path d="M92 32 H95 V52 H92" fill="none" stroke="{U}" stroke-width=".5"/>')
o.append(f'<line x1="62" y1="52" x2="95" y2="52" stroke="{U}" stroke-width=".3" stroke-dasharray="1 .8"/>')
o.append(t(97, 43.5, 'h', 4.4, 'start', '800', U))
o.append(t(77, 76.2, 'Hg', 3.4, 'middle', '700', '#374151'))
o.append(t(60, 4.4, 'Kap önce vakumlanır, sonra sıvı eklenir', 3.2, 'middle', '400', S))
o.append('</g></svg>')
w('manometre', ''.join(o))

# =========================================================
# 6) Buhar basıncı – sıcaklık grafiği (eter, etanol, su)
# =========================================================
x0, x1, y0, y1 = 20, 172, 80, 6
Tmax, Pmax = 110, 1000
X = lambda T: x0 + T / Tmax * (x1 - x0)
Y = lambda P: y0 - P / Pmax * (y0 - y1)
o = ['<svg viewBox="0 0 180 92" class="grafik"><g font-family="Inter">']
for T in range(0, 111, 10):
    o.append(f'<line x1="{X(T):.1f}" y1="{y0}" x2="{X(T):.1f}" y2="{y1}" stroke="#eef0f5" stroke-width=".3"/>')
    o.append(t(X(T), y0 + 4.2, str(T), 3.3, 'middle', '400', S))
for P in range(0, 1001, 200):
    o.append(f'<line x1="{x0}" y1="{Y(P):.1f}" x2="{x1}" y2="{Y(P):.1f}" stroke="#eef0f5" stroke-width=".3"/>')
    o.append(t(x0 - 1.6, Y(P) + 1.2, str(P), 3.3, 'end', '400', S))
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{M}" stroke-width=".5"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{M}" stroke-width=".5"/>')
o.append(f'<line x1="{x0}" y1="{Y(760):.1f}" x2="{x1}" y2="{Y(760):.1f}" stroke="{U}" stroke-width=".55" stroke-dasharray="2 1.2"/>')
o.append(t(X(42), Y(760) - 1.5, '1 atm = 760 mmHg', 3.3, 'start', '700', U))
egriler = [('Dietil eter', pd, '#d97706'), ('Etanol', pe, TEAL), ('Su', pw, SUK)]
for ad, fn, renk in egriler:
    pts = []
    T = 0.0
    while T <= Tmax:
        P = fn(T)
        if P > Pmax:
            break
        pts.append((X(T), Y(P)))
        T += 0.5
    o.append('<polyline fill="none" stroke="%s" stroke-width="1" points="%s"/>' % (renk, ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)))
kn = [(34.6, '#d97706', '34,6'), (78.3, TEAL, '78,3'), (100.0, SUK, '100')]
for T, renk, et in kn:
    o.append(f'<line x1="{X(T):.1f}" y1="{Y(760):.1f}" x2="{X(T):.1f}" y2="{y0}" stroke="{renk}" stroke-width=".4" stroke-dasharray="1 .8"/>')
    o.append(f'<circle cx="{X(T):.1f}" cy="{Y(760):.1f}" r="1.3" fill="{renk}"/>')
    o.append(f'<rect x="{X(T)-5.2:.1f}" y="{y0-6.2}" width="10.4" height="4.6" rx="1" fill="#fff" stroke="{renk}" stroke-width=".35"/>')
    o.append(t(X(T), y0 - 2.7, et, 3.1, 'middle', '800', renk))
o.append(t(X(41.5), Y(930), 'Dietil eter', 3.6, 'start', '800', '#b45309'))
o.append(t(X(86), Y(700), 'Etanol', 3.6, 'start', '800', TEAL))
o.append(t(X(92), Y(330), 'Su', 3.6, 'end', '800', SUK))
# 20 °C kesiti
o.append(f'<line x1="{X(20):.1f}" y1="{y0}" x2="{X(20):.1f}" y2="{Y(560):.1f}" stroke="{M}" stroke-width=".35" stroke-dasharray=".8 .8"/>')
for fn, renk in [(pd, '#d97706'), (pe, TEAL), (pw, SUK)]:
    o.append(f'<circle cx="{X(20):.1f}" cy="{Y(fn(20)):.1f}" r=".9" fill="{renk}"/>')
o.append(t(X(20) - 1.4, Y(600), '20 °C', 3.1, 'middle', '700', M))
o.append(t(X(1), Y(440) - 2, '≈ 440', 2.9, 'start', '700', '#b45309'))
o.append(t((x0 + x1) / 2, y0 + 9.4, 'Sıcaklık (°C)', 3.6, 'middle', '700'))
o.append(t(3, (y0 + y1) / 2, 'Buhar basıncı (mmHg)', 3.6, 'middle', '700', M, f'transform="rotate(-90 3 {(y0+y1)/2})"'))
o.append('</g></svg>')
w('bbgrafik', ''.join(o))

# =========================================================
# 7) Kaynama: kabarcık içinde P_buhar = P_dış
# =========================================================
o = ['<svg viewBox="0 0 124 80" class="grafik"><defs>' + ok(U, 'kb-u', 3.2) + ok(SUD, 'kb-s', 3.2) + '</defs><g font-family="Inter">']
o.append(f'<rect x="10.4" y="22" width="43.2" height="43.6" fill="{SU}"/>')
o.append(f'<path d="M10 12 V62 Q10 66 14 66 H50 Q54 66 54 62 V12" fill="none" stroke="{CAM}" stroke-width=".9"/>')
for (a, b, r) in [(18, 58, 1.2), (24, 47, 2.0), (33, 60, 1.0), (38, 38, 2.6), (45, 54, 1.6), (29, 30, 3.0), (46, 28, 1.4), (20, 36, 1.1)]:
    o.append(f'<circle cx="{a}" cy="{b}" r="{r}" fill="#fff" stroke="{SUK}" stroke-width=".4"/>')
o.append(f'<path d="M22 70 q3 -6 0 -9 q5 3 4 9z M32 70 q3 -7 0 -10 q6 4 4 10z M42 70 q3 -6 0 -9 q5 3 4 9z" fill="{AMB}" opacity=".9"/>')
o.append(f'<rect x="14" y="70" width="36" height="2" rx="1" fill="{S}"/>')
o.append(f'<line x1="41" y1="36" x2="76" y2="24" stroke="{S}" stroke-width=".3" stroke-dasharray="1 .8"/>')
o.append(f'<line x1="41" y1="40.5" x2="76" y2="58" stroke="{S}" stroke-width=".3" stroke-dasharray="1 .8"/>')
o.append(f'<circle cx="95" cy="41" r="21" fill="{SU}" stroke="{CAM}" stroke-width=".5"/>')
o.append(f'<circle cx="95" cy="41" r="9.5" fill="#fff" stroke="{SUK}" stroke-width=".6"/>')
random.seed(5)
for i in range(5):
    ang = i * 1.3
    o.append(mol(95 + 4.6 * math.cos(ang), 41 + 4.6 * math.sin(ang), 1.1, '#fcd34d', '#b45309'))
for ang in (0, 90, 180, 270):
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    o.append(f'<path d="M{95+6.2*c:.1f} {41+6.2*s_:.1f} L{95+12.5*c:.1f} {41+12.5*s_:.1f}" stroke="{U}" stroke-width=".8" marker-end="url(#kb-u)"/>')
for ang in (45, 135, 225, 315):
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    o.append(f'<path d="M{95+19*c:.1f} {41+19*s_:.1f} L{95+11*c:.1f} {41+11*s_:.1f}" stroke="{SUD}" stroke-width=".8" marker-end="url(#kb-s)"/>')
o.append(t(95, 14.6, alt('P', 'buhar', 4) + '(dışa iter)', 3.6, 'middle', '800', U))
o.append(t(95, 69.6, alt('P', 'dış', 4) + '(içe iter)', 3.6, 'middle', '800', SUD))
o.append(t(32, 7.5, 'Kabarcıklar her yerde', 3.3, 'middle', '700', UK))
o.append(t(62, 78, 'Kabarcık ancak buhar basıncı dış basınca ulaşınca büyüyebilir.', 3.1, 'middle', '400', S))
o.append('</g></svg>')
w('kabarcik', ''.join(o))

# =========================================================
# 8) Suyun buhar basıncı eğrisi üzerinde kaynama noktası okuma
# =========================================================
x0, x1, y0, y1 = 22, 126, 64, 5
Ta, Tb, Pmax = 60, 125, 1700
X = lambda T: x0 + (T - Ta) / (Tb - Ta) * (x1 - x0)
Y = lambda P: y0 - P / Pmax * (y0 - y1)
o = ['<svg viewBox="0 0 180 74" class="grafik"><g font-family="Inter">']
for T in range(60, 126, 10):
    o.append(f'<line x1="{X(T):.1f}" y1="{y0}" x2="{X(T):.1f}" y2="{y1}" stroke="#eef0f5" stroke-width=".3"/>')
    o.append(t(X(T), y0 + 4.2, str(T), 3.3, 'middle', '400', S))
for P in range(0, 1601, 400):
    o.append(f'<line x1="{x0}" y1="{Y(P):.1f}" x2="{x1}" y2="{Y(P):.1f}" stroke="#eef0f5" stroke-width=".3"/>')
    o.append(t(x0 - 1.6, Y(P) + 1.2, str(P), 3.3, 'end', '400', S))
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{M}" stroke-width=".5"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{M}" stroke-width=".5"/>')
pts = []
T = 60.0
while T <= 125:
    pts.append((X(T), Y(pw(T))))
    T += 0.5
o.append('<polyline fill="none" stroke="%s" stroke-width="1.1" points="%s"/>' % (SUK, ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)))
seviyeler = [(250, 'Everest zirvesi', '≈ 250 mmHg', '#64748b'), (596, '≈ 2000 m yayla', '≈ 600 mmHg', TEAL),
             (760, 'Deniz seviyesi', '760 mmHg', U), (1490, 'Düdüklü tencere', '≈ 1490 mmHg (≈ 2 atm)', '#b45309')]
for P, ad, pet, renk in seviyeler:
    T = tw(P)
    o.append(f'<line x1="{x0}" y1="{Y(P):.1f}" x2="{x1}" y2="{Y(P):.1f}" stroke="{renk}" stroke-width=".45" stroke-dasharray="1.6 1"/>')
    o.append(f'<line x1="{X(T):.1f}" y1="{Y(P):.1f}" x2="{X(T):.1f}" y2="{y0}" stroke="{renk}" stroke-width=".45" stroke-dasharray="1 .8"/>')
    o.append(f'<circle cx="{X(T):.1f}" cy="{Y(P):.1f}" r="1.3" fill="{renk}"/>')
    o.append(f'<rect x="{X(T)-5.4:.1f}" y="{y0-6.4}" width="10.8" height="4.6" rx="1" fill="#fff" stroke="{renk}" stroke-width=".35"/>')
    o.append(t(X(T), y0 - 2.9, f'{round(T)}', 3.1, 'middle', '800', renk))
    dy = {760: -4.6, 596: 3.4}.get(P, -.2)
    o.append(t(x1 + 2.4, Y(P) + dy, ad, 3.3, 'start', '800', renk))
    o.append(t(x1 + 2.4, Y(P) + dy + 3.7, pet, 3, 'start', '400', S))
o.append(t(X(64), Y(1150), 'Suyun buhar basıncı', 3.4, 'start', '800', SUK))
o.append(t((x0 + x1) / 2, y0 + 9, 'Sıcaklık (°C)', 3.6, 'middle', '700'))
o.append(t(3, (y0 + y1) / 2, 'Basınç (mmHg)', 3.6, 'middle', '700', M, f'transform="rotate(-90 3 {(y0+y1)/2})"'))
o.append('</g></svg>')
w('suegrisi', ''.join(o))

# =========================================================
# 9) Saf su ve tuzlu su ısıtma eğrisi
# =========================================================
x0, x1, y0, y1 = 16, 116, 46, 8
X = lambda tt: x0 + tt / 10 * (x1 - x0)
Y = lambda T: y0 - (T - 20) / (112 - 20) * (y0 - y1)
o = ['<svg viewBox="0 0 120 54" class="grafik"><defs>' + ok(M, 'is-o', 3) + '</defs><g font-family="Inter">']
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1+2}" y2="{y0}" stroke="{M}" stroke-width=".5" marker-end="url(#is-o)"/>')
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1-3}" stroke="{M}" stroke-width=".5" marker-end="url(#is-o)"/>')
o.append(f'<line x1="{x0}" y1="{Y(100):.1f}" x2="{x1}" y2="{Y(100):.1f}" stroke="{S}" stroke-width=".3" stroke-dasharray="1 .8"/>')
o.append(t(x0 - 1.4, Y(100) + 1.2, '100', 3.2, 'end', '700'))
o.append(t(x0 - 1.4, Y(20) + 1.2, '20', 3.2, 'end', '400', S))
saf = [(X(0), Y(20)), (X(4.6), Y(100)), (X(10), Y(100))]
tuz = [(X(0), Y(20)), (X(4.9), Y(102.5))] + [(X(4.9 + i * 0.1), Y(102.5 + 4.2 * (i / 51) ** 1.3)) for i in range(1, 52)]
o.append('<polyline fill="none" stroke="%s" stroke-width="1" points="%s"/>' % (SUK, ' '.join(f'{a:.1f},{b:.1f}' for a, b in saf)))
o.append('<polyline fill="none" stroke="%s" stroke-width="1" points="%s"/>' % (U, ' '.join(f'{a:.1f},{b:.1f}' for a, b in tuz)))
o.append(t(x1, Y(100) + 5.2, 'Saf su: kaynarken sıcaklık sabit', 2.9, 'end', '700', SUD))
o.append(t(x1, Y(107) - 6.2, 'Tuzlu su: kaynarken sıcaklık artar', 2.9, 'end', '700', U))
o.append(t((x0 + x1) / 2, y0 + 5.4, 'Isıtma süresi', 3.4, 'middle', '700'))
o.append(t(4, (y0 + y1) / 2, 'Sıcaklık (°C)', 3.4, 'middle', '700', M, f'transform="rotate(-90 4 {(y0+y1)/2})"'))
o.append('</g></svg>')
w('isitma', ''.join(o))

# =========================================================
# 10) Bilye deneyi: viskozite karşılaştırması
# =========================================================
o = ['<svg viewBox="0 0 120 74" class="grafik"><g font-family="Inter">']
sv = [(20, SU, 54, 'Su', '≈ 1'), (60, '#f3e3a0', 37, 'Zeytinyağı', '≈ 80'), (100, '#efe9dc', 22, 'Gliserin', '≈ 1400')]
for cx, renk, by, ad, eta in sv:
    o.append(f'<rect x="{cx-10.6}" y="14" width="21.2" height="45.6" fill="{renk}"/>')
    o.append(f'<path d="M{cx-11} 8 V58 Q{cx-11} 60 {cx-9} 60 H{cx+9} Q{cx+11} 60 {cx+11} 58 V8" fill="none" stroke="{CAM}" stroke-width=".8"/>')
    for k in range(1, 6):
        o.append(f'<line x1="{cx+7}" y1="{14+k*8}" x2="{cx+11}" y2="{14+k*8}" stroke="{CAM}" stroke-width=".3"/>')
    o.append(f'<circle cx="{cx}" cy="11" r="2.4" fill="none" stroke="{S}" stroke-width=".35" stroke-dasharray=".8 .6"/>')
    o.append(f'<line x1="{cx}" y1="13.6" x2="{cx}" y2="{by-3}" stroke="{S}" stroke-width=".3" stroke-dasharray=".8 .8"/>')
    o.append(f'<circle cx="{cx}" cy="{by}" r="2.6" fill="#6b7280" stroke="#374151" stroke-width=".4"/>')
    o.append(t(cx, 65.5, ad, 3.6, 'middle', '800'))
    o.append(t(cx, 70.4, eta + ' mPa·s', 3.2, 'middle', '400', S))
o.append(t(60, 4.4, 'Aynı anda bırakılan özdeş bilyeler · aynı süre sonra · 20 °C', 3.2, 'middle', '700', UK))
o.append('</g></svg>')
w('bilye', ''.join(o))

# =========================================================
# 11) Yüzey gerilimi: yüzeydeki ve içteki tanecik
# =========================================================
o = ['<svg viewBox="0 0 100 58" class="grafik"><defs>' + ok(U, 'yz-u', 3) + '</defs><g font-family="Inter">']
o.append(f'<rect x="4" y="16" width="92" height="40" rx="2" fill="{SU}"/>')
o.append(f'<line x1="4" y1="16" x2="96" y2="16" stroke="{SUK}" stroke-width=".6"/>')
for j, yy in enumerate([19.5, 27, 34.5, 42, 49.5]):
    for i in range(12):
        xx = 8 + i * 7.6 + (3.8 if j % 2 else 0)
        if xx > 93:
            continue
        hl = (j == 0 and i == 3) or (j == 3 and i == 8)
        o.append(mol(xx, yy, 2.1, '#fcd34d' if hl else '#93c5fd', '#b45309' if hl else SUD))
for (a, b, dirs) in [(30.8, 19.5, (0, 180, 60, 120)), (72.6, 42, (0, 60, 120, 180, 240, 300))]:
    for ang in dirs:
        c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        o.append(f'<path d="M{a+2.4*c:.1f} {b+2.4*s_:.1f} L{a+6.6*c:.1f} {b+6.6*s_:.1f}" stroke="{U}" stroke-width=".55" marker-end="url(#yz-u)"/>')
o.append(t(30.8, 6.4, 'Yüzeydeki tanecik', 3.4, 'middle', '800', UK))
o.append(t(30.8, 11.2, 'net çekim içe doğru', 3.1, 'middle', '400', S))
o.append(t(72.6, 6.4, 'İçteki tanecik', 3.4, 'middle', '800', UK))
o.append(t(72.6, 11.2, 'çekimler dengede', 3.1, 'middle', '400', S))
o.append('</g></svg>')
w('yuzey', ''.join(o))

# =========================================================
# 12) Menisküs ve kılcallık: su ve cıva
# =========================================================


def tup(cx, gen, sv_y, renk, kenar, bukey):
    """Cam boru içinde sıvı sütunu. bukey>0: çukur (su), <0: tümsek (cıva)."""
    s = []
    l, r = cx - gen / 2, cx + gen / 2
    s.append(f'<rect x="{l:.1f}" y="6" width="{gen:.1f}" height="46" fill="#fff"/>')
    s.append(f'<path d="M{l:.1f} {sv_y-bukey:.1f} Q{cx:.1f} {sv_y+bukey:.1f} {r:.1f} {sv_y-bukey:.1f} V52 H{l:.1f}Z" fill="{renk}"/>')
    s.append(f'<path d="M{l:.1f} {sv_y-bukey:.1f} Q{cx:.1f} {sv_y+bukey:.1f} {r:.1f} {sv_y-bukey:.1f}" fill="none" stroke="{kenar}" stroke-width=".5"/>')
    s.append(f'<line x1="{l-.4:.1f}" y1="6" x2="{l-.4:.1f}" y2="54" stroke="{CAM}" stroke-width=".7"/>')
    s.append(f'<line x1="{r+.4:.1f}" y1="6" x2="{r+.4:.1f}" y2="54" stroke="{CAM}" stroke-width=".7"/>')
    return ''.join(s)


o = ['<svg viewBox="0 0 180 70" class="grafik"><g font-family="Inter">']
for (ox_, renk, kenar, ad, h_gen, h_dar, buk, bas1, bas2) in [
        (0, SU, SUK, 'Su', -9, -20, 1.6, 'Su · cam', 'adezyon &gt; kohezyon · menisküs çukur'),
        (92, '#cbd5e1', '#475569', 'Cıva', 5, 10, -1.6, 'Cıva · cam', 'kohezyon &gt; adezyon · menisküs tümsek')]:
    yuz = 40
    o.append(f'<rect x="{ox_+8}" y="{yuz}" width="72" height="16" fill="{renk}"/>')
    o.append(f'<path d="M{ox_+8} 30 V56 H{ox_+80} V30" fill="none" stroke="{CAM}" stroke-width=".8"/>')
    o.append(f'<line x1="{ox_+8}" y1="{yuz}" x2="{ox_+80}" y2="{yuz}" stroke="{kenar}" stroke-width=".4"/>')
    o.append(tup(ox_ + 30, 9, yuz + h_gen, renk, kenar, buk))
    o.append(tup(ox_ + 56, 4, yuz + h_dar, renk, kenar, buk * 0.6))
    o.append(f'<line x1="{ox_+20}" y1="{yuz}" x2="{ox_+66}" y2="{yuz}" stroke="{kenar}" stroke-width=".3" stroke-dasharray="1 .8"/>')
    o.append(t(ox_ + 30, 3.8, 'geniş boru', 3.8, 'middle', '400', S))
    o.append(t(ox_ + 56, 3.8, 'dar boru', 3.8, 'middle', '400', S))
    o.append(t(ox_ + 44, 62.5, bas1, 4.6, 'middle', '800', UK))
    o.append(t(ox_ + 44, 68.4, bas2, 3.9, 'middle', '700', U))
o.append('</g></svg>')
w('kilcal', ''.join(o))

# =========================================================
# 13) Test sorusu: X, Y, Z buhar basıncı eğrileri
# =========================================================
x0, x1, y0, y1 = 14, 112, 52, 6
X = lambda T: x0 + T / 130 * (x1 - x0)
Pm = 1000
Y = lambda P: y0 - P / Pm * (y0 - y1)
o = ['<svg viewBox="0 0 120 62" class="grafik"><defs>' + ok(M, 'tb-o', 3) + '</defs><g font-family="Inter">']
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1+2}" y2="{y0}" stroke="{M}" stroke-width=".5" marker-end="url(#tb-o)"/>')
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1-3}" stroke="{M}" stroke-width=".5" marker-end="url(#tb-o)"/>')
o.append(f'<line x1="{x0}" y1="{Y(760):.1f}" x2="{x1}" y2="{Y(760):.1f}" stroke="{U}" stroke-width=".4" stroke-dasharray="1.4 1"/>')
o.append(t(x0 - 1.4, Y(760) + 1.2, '760', 3.2, 'end', '700', U))
for ad, Tb, renk in [('X', 40, '#d97706'), ('Y', 70, TEAL), ('Z', 110, SUK)]:
    Tk = Tb + 273
    pts = []
    for i in range(0, 261):
        T = i / 2
        P = 760 * math.exp(4200 * (1 / Tk - 1 / (T + 273)))
        if P > Pm:
            break
        pts.append((X(T), Y(P)))
    o.append('<polyline fill="none" stroke="%s" stroke-width=".9" points="%s"/>' % (renk, ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)))
    a, b = pts[-1]
    o.append(t(a + 1.5, b + 3, ad, 3.8, 'start', '800', renk))
    o.append(f'<line x1="{X(Tb):.1f}" y1="{Y(760):.1f}" x2="{X(Tb):.1f}" y2="{y0}" stroke="{renk}" stroke-width=".35" stroke-dasharray="1 .8"/>')
    o.append(t(X(Tb), y0 + 4.2, str(Tb), 3.2, 'middle', '700', renk))
o.append(t(x1, y0 + 8.6, 'Sıcaklık (°C)', 3.2, 'end', '700'))
o.append(t(x0 + 1.5, y1 - .6, 'Buhar basıncı (mmHg)', 3.2, 'start', '700'))
o.append('</g></svg>')
w('testbb', ''.join(o))

# =========================================================
# 14) Bağlam: rakım – kaynama noktası
# =========================================================
x0, x1, y0, y1 = 18, 114, 48, 7
X = lambda h: x0 + h / 5000 * (x1 - x0)
Y = lambda T: y0 - (T - 80) / 22 * (y0 - y1)
o = ['<svg viewBox="0 0 120 60" class="grafik"><g font-family="Inter">']
for T in range(80, 101, 5):
    o.append(f'<line x1="{x0}" y1="{Y(T):.1f}" x2="{x1}" y2="{Y(T):.1f}" stroke="#eef0f5" stroke-width=".3"/>')
    o.append(t(x0 - 1.4, Y(T) + 1.2, str(T), 4, 'end', '400', S))
o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{M}" stroke-width=".5"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{M}" stroke-width=".5"/>')
pts = []
for h in range(0, 5001, 1000):
    P = 760 * (1 - 2.25577e-5 * h) ** 5.25588
    pts.append((h, tw(P)))
    o.append(t(X(h), y0 + 4.8, f'{h}', 3.8, 'middle', '400', S))
o.append('<polyline fill="none" stroke="%s" stroke-width="1" points="%s"/>' % (U, ' '.join(f'{X(h):.1f},{Y(T):.1f}' for h, T in pts)))
for h, T in pts:
    o.append(f'<circle cx="{X(h):.1f}" cy="{Y(T):.1f}" r="1.1" fill="{U}"/>')
    o.append(t(X(h) + (1.6 if h < 5000 else -1.6), Y(T) - 2.2, f'{T:.0f}', 4, 'start' if h < 5000 else 'end', '700', UK))
o.append(t((x0 + x1) / 2, y0 + 10.4, 'Deniz seviyesinden yükseklik (m)', 4, 'middle', '700'))
o.append(t(3, (y0 + y1) / 2, 'KN (°C)', 4, 'middle', '700', M, f'transform="rotate(-90 3 {(y0+y1)/2})"'))
o.append('</g></svg>')
w('rakim', ''.join(o))

if __name__ == '__main__':
    print('rakım:', [(h, round(T, 1)) for h, T in pts])
    for P in (250, 600, 760, 1520):
        print(P, 'mmHg ->', round(tw(P), 1), '°C')
    print('20 °C:', round(pd(20)), round(pe(20), 1), round(pw(20), 1))
