"""Moleküller arası etkileşimler ünitesinin SVG şekillerini üretir.
Çıktı: uretec/svg/<ad>.svg  (kur.py bunları sablon.html içine yerleştirir)
Kaynama noktaları (1 atm, °C) yaygın başvuru değerleridir (CRC/NIST, yuvarlatılmış).
"""
import math
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg')
os.makedirs(D, exist_ok=True)

U = '#0369a1'; UK = '#073b5e'; UA = '#eaf5fc'; S = '#5d6478'; M = '#1d2133'; AMB = '#f59e0b'
KIR = '#dc2626'; MAV = '#2563eb'; YES = '#16a34a'; GRI = '#64748b'
O_R = '#ef4444'; H_F = '#ffffff'; H_S = '#94a3b8'; CL = '#4ade80'; CL_S = '#15803d'
F_R = '#bef264'; F_S = '#65a30d'; C_R = '#475569'; N_R = '#3b82f6'

ALT = str.maketrans('0123456789+-', '₀₁₂₃₄₅₆₇₈₉⁺⁻')


def alt(s):
    """SVG içinde formül: rakamlar alt simge (Unicode)."""
    return s.translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))


def sy(v, f='{:.0f}'):
    """Sayıyı eksi işaretiyle (−) ve ondalık virgülle yazar."""
    return f.format(v).replace('-', '−').replace('.', ',')


def w(ad, s):
    open(os.path.join(D, ad + '.svg'), 'w', encoding='utf-8').write(s)


def atom(x, y, r, dolgu, cizgi='#00000033', yazi='', yr='#fff', fs=None, sw=.35):
    o = f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{dolgu}" stroke="{cizgi}" stroke-width="{sw}"/>'
    if yazi:
        fs = fs or r * 0.95
        o += f'<text x="{x:.2f}" y="{y + fs * .36:.2f}" font-size="{fs:.2f}" font-weight="800" fill="{yr}" text-anchor="middle">{yazi}</text>'
    return o


def su(x, y, aci, s=1.0, harf=False):
    """Su molekülü: O (x,y); H'ler aci±52,25° yönünde. (svg, [H1, H2]) döndürür."""
    d = 4.4 * s
    hs = []
    o = atom(x, y, 3.4 * s, O_R, '#b91c1c', 'O' if harf else '', fs=3.4 * s * .9)
    for da in (-52.25, 52.25):
        a = math.radians(aci + da)
        hx, hy = x + d * math.cos(a), y + d * math.sin(a)
        hs.append((hx, hy))
        o += atom(hx, hy, 2.1 * s, H_F, H_S, 'H' if harf else '', yr=M, fs=2.1 * s * 1.05, sw=.3)
    return o, hs


def kesik(x1, y1, x2, y2, renk=AMB, kal=.55, kis=0.0):
    """İki nokta arasında kesikli çizgi; uçlardan kis kadar kısaltılır."""
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    a, b = (x1 + ux * kis, y1 + uy * kis), (x2 - ux * kis, y2 - uy * kis)
    return (f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" '
            f'stroke="{renk}" stroke-width="{kal}" stroke-dasharray="1.1 .8" stroke-linecap="round"/>')


BULUT = ('<radialGradient id="{id}" cx="{cx}" cy="50%" r="55%" fx="{fx}" fy="50%">'
         '<stop offset="0" stop-color="#0ea5e9" stop-opacity=".85"/>'
         '<stop offset=".55" stop-color="#7dd3fc" stop-opacity=".55"/>'
         '<stop offset="1" stop-color="#e0f2fe" stop-opacity=".15"/></radialGradient>')

# ------------------------------------------------------------------ 1) bağ / etkileşim (s.2)
o = ['<svg viewBox="0 0 92 50" class="grafik"><g font-family="Inter">']
w1, h1 = su(16, 27, 52.25, 1.6, True)   # H'lerden biri tam sağa (0°)
w2, h2 = su(41, 27, 0, 1.6, True)       # alıcı O, H'leri sağa bakar
o += [w1, w2]
hx, hy = h1[0]
o.append(kesik(hx, hy, 41, 27, AMB, .9, 3.6))
o.append(f'<path d="M{(16 + hx) / 2:.1f} {hy - 1.2:.1f} L51 12" stroke="{U}" stroke-width=".35" fill="none"/>')
o.append(f'<path d="M{(hx + 41) / 2 + .5:.1f} {hy + 1.2:.1f} L51 40" stroke="{AMB}" stroke-width=".35" fill="none"/>')
o.append(f'<text x="52" y="10" font-size="3.2" font-weight="800" fill="{UK}">O–H kovalent bağı</text>')
o.append(f'<text x="52" y="14.4" font-size="2.9" fill="{S}">molekül içi · ≈ 460 kJ/mol</text>')
o.append(f'<text x="52" y="18.6" font-size="3" font-weight="700" fill="{U}">GÜÇLÜ etkileşim</text>')
o.append(f'<text x="52" y="38" font-size="3.2" font-weight="800" fill="#b45309">Hidrojen bağı</text>')
o.append(f'<text x="52" y="42.4" font-size="2.9" fill="{S}">moleküller arası · ≈ 20 kJ/mol</text>')
o.append(f'<text x="52" y="46.6" font-size="3" font-weight="700" fill="#b45309">ZAYIF etkileşim</text>')
o.append('</g></svg>')
w('bag', ''.join(o))

# ------------------------------------------------------------------ 2) dipol türleri (s.2)
o = ['<svg viewBox="0 0 178 50" class="grafik"><defs>',
     BULUT.format(id='bs', cx='50%', fx='50%'), BULUT.format(id='bk', cx='45%', fx='18%'),
     '<marker id="ok1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 10 5 0 10z" fill="#5d6478"/></marker>',
     '</defs><g font-family="Inter" text-anchor="middle">']
for x0, bas in ((1, 'KALICI DİPOL'), (61, 'ANLIK (GEÇİCİ) DİPOL'), (121, 'İNDÜKLENMİŞ DİPOL')):
    o.append(f'<rect x="{x0}" y="1" width="56" height="48" rx="3" fill="{UA}"/>')
    o.append(f'<text x="{x0 + 28}" y="7.4" font-size="3.4" font-weight="800" fill="{UK}">{bas}</text>')
# panel 1: HCl
o.append(f'<ellipse cx="27" cy="26" rx="15" ry="9.5" fill="url(#bk)" transform="rotate(180 27 26)"/>')
o.append(atom(19.5, 26, 4.2, H_F, H_S, 'H', M, 4))
o.append(atom(30.5, 26, 7.2, CL, CL_S, 'Cl', '#064e3b', 5))
o.append(f'<text x="17" y="16.5" font-size="4" font-weight="800" fill="{MAV}">δ+</text>')
o.append(f'<text x="35" y="15" font-size="4" font-weight="800" fill="{KIR}">δ−</text>')
o.append(f'<text x="29" y="41.5" font-size="3.1" font-weight="700" fill="{M}">HCl · polar molekül</text>')
o.append(f'<text x="29" y="46" font-size="2.9" fill="{S}">Kutuplar sürekli yerinde</text>')
# panel 2: Ar
o.append(f'<circle cx="76" cy="25" r="8.5" fill="url(#bs)"/><circle cx="76" cy="25" r="1.2" fill="{UK}"/>')
o.append(f'<path d="M87 25 H95" stroke="{S}" stroke-width=".5" marker-end="url(#ok1)"/>')
o.append(f'<text x="91" y="21.5" font-size="2.6" fill="{S}">bir an</text>')
o.append(f'<ellipse cx="106" cy="25" rx="9.5" ry="8.5" fill="url(#bk)"/><circle cx="108" cy="25" r="1.2" fill="{UK}"/>')
o.append(f'<text x="100" y="14.5" font-size="4" font-weight="800" fill="{KIR}">δ−</text>')
o.append(f'<text x="113" y="14.5" font-size="4" font-weight="800" fill="{MAV}">δ+</text>')
o.append(f'<text x="89" y="41.5" font-size="3.1" font-weight="700" fill="{M}">Ar · soy gaz atomu</text>')
o.append(f'<text x="89" y="46" font-size="2.9" fill="{S}">Elektron bulutu bir an kayar</text>')
# panel 3: iyon + apolar molekül
o.append(atom(131, 25, 4.6, '#8b5cf6', '#6d28d9', '+', '#fff', 6))
o.append(f'<text x="131" y="17" font-size="2.8" font-weight="700" fill="#6d28d9">katyon</text>')
o.append(f'<ellipse cx="155" cy="25" rx="14" ry="8" fill="url(#bk)"/>')
o.append(f'<circle cx="151" cy="25" r="1.1" fill="{UK}"/><circle cx="160" cy="25" r="1.1" fill="{UK}"/>')
o.append(f'<text x="144" y="15" font-size="4" font-weight="800" fill="{KIR}">δ−</text>')
o.append(f'<text x="167" y="15" font-size="4" font-weight="800" fill="{MAV}">δ+</text>')
o.append(f'<text x="149" y="41.5" font-size="3.1" font-weight="700" fill="{M}">Yük, apolar taneciği kutuplar</text>')
o.append(f'<text x="149" y="46" font-size="2.9" fill="{S}">Elektronlar + yüke doğru çekilir</text>')
o.append('</g></svg>')
w('dipol', ''.join(o))

# ------------------------------------------------------------------ 3) hidratasyon (s.3)
o = ['<svg viewBox="0 0 120 56" class="grafik"><g font-family="Inter" text-anchor="middle">']
for k in range(6):
    a = math.radians(k * 60 + 30)
    s_, _ = su(30 + 13 * math.cos(a), 27 + 13 * math.sin(a), k * 60 + 30, 1.0)
    o.append(s_)
o.append(atom(30, 27, 5, '#8b5cf6', '#6d28d9', 'Na⁺', '#fff', 3.6))
for k in range(6):
    a = math.radians(k * 60)
    s_, _ = su(90 + 15 * math.cos(a), 27 + 15 * math.sin(a), k * 60 + 180, 1.0)
    o.append(s_)
o.append(atom(90, 27, 7, CL, CL_S, 'Cl⁻', '#064e3b', 3.8))
o.append(f'<text x="30" y="51" font-size="3.1" font-weight="700" fill="{M}">Katyonu suyun δ− ucu (O) sarar</text>')
o.append(f'<text x="90" y="51" font-size="3.1" font-weight="700" fill="{M}">Anyonu suyun δ+ ucu (H) sarar</text>')
o.append(f'<text x="60" y="55.5" font-size="2.7" fill="{S}">● O (kırmızı) · ○ H (beyaz) · iyonlar ölçekli değildir</text>')
o.append('</g></svg>')
w('hidratasyon', ''.join(o))

# ------------------------------------------------------------------ 4) dipol-dipol (s.3)
o = ['<svg viewBox="0 0 92 46" class="grafik"><g font-family="Inter" text-anchor="middle">']
xs = (10, 38, 66)
cizgiler = []
for k, x in enumerate(xs):
    if k < len(xs) - 1:
        cizgiler.append(kesik(x + 7, 12, x + 28, 12, AMB, .6, 6.5))  # Cl -> sağdaki H
        cizgiler.append(kesik(x + 7, 33, x + 28, 33, AMB, .6, 4.5))  # alt H -> sağdaki alt Cl
    cizgiler.append(kesik(x, 12, x, 33, AMB, .6, 3.8))           # H -> alttaki Cl
    cizgiler.append(kesik(x + 7, 12, x + 7, 33, AMB, .6, 4.5))   # Cl -> alttaki H
o += cizgiler
for x in xs:
    o.append(atom(x, 12, 3.2, H_F, H_S, 'H', M, 3.0))
    o.append(atom(x + 7, 12, 5.4, CL, CL_S, 'Cl', '#064e3b', 3.6))
    o.append(atom(x, 33, 5.4, CL, CL_S, 'Cl', '#064e3b', 3.6))
    o.append(atom(x + 7, 33, 3.2, H_F, H_S, 'H', M, 3.0))
o.append(f'<text x="46" y="44.5" font-size="3" font-weight="700" fill="{M}">δ+ uç (H) komşunun δ− ucunu (Cl) çeker</text>')
o.append('</g></svg>')
w('dipoldipol', ''.join(o))

# ------------------------------------------------------------------ 5) London mekanizması (s.4)
o = ['<svg viewBox="0 0 92 34" class="grafik"><defs>',
     BULUT.format(id='lk', cx='45%', fx='18%'),
     '</defs><g font-family="Inter" text-anchor="middle">']
# A: δ- solda, δ+ sağda ; B: δ- solda (A'nın δ+ ucuna bakar)
for cx in (22, 62):
    o.append(f'<ellipse cx="{cx}" cy="15" rx="11" ry="9" fill="url(#lk)"/><circle cx="{cx + 2}" cy="15" r="1.2" fill="{UK}"/>')
    o.append(f'<text x="{cx - 7}" y="4.5" font-size="3.6" font-weight="800" fill="{KIR}">δ−</text>')
    o.append(f'<text x="{cx + 8}" y="4.5" font-size="3.6" font-weight="800" fill="{MAV}">δ+</text>')
o.append(kesik(33, 15, 51, 15, AMB, .8, 0))
o.append(f'<text x="42" y="12.6" font-size="2.8" font-weight="700" fill="#b45309">çekim</text>')
o.append(f'<text x="22" y="28.5" font-size="3" font-weight="700" fill="{M}">1 · Anlık dipol</text>')
o.append(f'<text x="62" y="28.5" font-size="3" font-weight="700" fill="{M}">2 · İndüklenmiş dipol</text>')
o.append(f'<text x="42" y="33" font-size="2.7" fill="{S}">Anlık kutup komşuyu kutuplar; zıt kutuplar birbirini çeker.</text>')
o.append('</g></svg>')
w('london', ''.join(o))

# ------------------------------------------------------------------ 6) halojenler (s.4)
hal = [('F2', 18, -188.1, 'gaz'), ('Cl2', 34, -34.0, 'gaz'), ('Br2', 70, 58.8, 'sıvı'), ('I2', 106, 184.3, 'katı')]
renk_hal = {'gaz': '#bae6fd', 'sıvı': '#38bdf8', 'katı': U}
x0, x1, ytop, ybot = 16, 88, 6, 46
Y = lambda v: ybot - (v + 200) / 400 * (ybot - ytop)
o = ['<svg viewBox="0 0 92 62" class="grafik"><g font-family="Inter" font-size="3" fill="' + S + '">']
for v in (-200, -100, 0, 100, 200):
    o.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="#e5e7f0" stroke-width=".3"/>')
    o.append(f'<text x="{x0 - 1.5}" y="{Y(v) + 1:.1f}" text-anchor="end">{sy(v)}</text>')
o.append(f'<line x1="{x0}" y1="{ybot}" x2="{x1}" y2="{ybot}" stroke="{M}" stroke-width=".4"/>')
o.append(f'<line x1="{x0}" y1="{ybot}" x2="{x0}" y2="{ytop - 2}" stroke="{M}" stroke-width=".4"/>')
o.append(f'<text x="1" y="3" fill="{M}" font-weight="700" font-size="3">KN (°C)</text>')
bw = 11
for i, (f, e, kn, hal_) in enumerate(hal):
    cx = x0 + 10 + i * 18
    o.append(f'<rect x="{cx - bw / 2}" y="{Y(kn):.1f}" width="{bw}" height="{ybot - Y(kn):.1f}" rx="1" fill="{renk_hal[hal_]}"/>')
    o.append(f'<text x="{cx}" y="{Y(kn) - 1.3:.1f}" text-anchor="middle" font-weight="700" fill="{M}">{sy(kn)}</text>')
    o.append(f'<text x="{cx}" y="{ybot + 4.2}" text-anchor="middle" font-weight="800" fill="{M}" font-size="3.6">{alt(f)}</text>')
    o.append(f'<text x="{cx}" y="{ybot + 8.2}" text-anchor="middle" font-size="2.8">{e} e⁻</text>')
    o.append(f'<text x="{cx}" y="{ybot + 12}" text-anchor="middle" font-size="2.8" font-weight="700" fill="{UK}">{hal_}</text>')
ya = Y(25)
o.append(f'<line x1="{x0}" y1="{ya:.1f}" x2="{x1}" y2="{ya:.1f}" stroke="{KIR}" stroke-width=".45" stroke-dasharray="1.4 .9"/>')
o.append(f'<text x="{x0 + 1}" y="{ya - 1.2:.1f}" font-size="2.6" fill="{KIR}" font-weight="700">25 °C</text>')
o.append('</g></svg>')
w('halojen', ''.join(o))

# ------------------------------------------------------------------ 7) izomerler / temas yüzeyi (s.4)
o = ['<svg viewBox="0 0 92 40" class="grafik"><g font-family="Inter" text-anchor="middle">']
def zincir(x, y):
    p = []
    for k in range(5):
        p.append((x + k * 5.6, y + (0 if k % 2 == 0 else -3.2)))
    s_ = ''.join(f'<line x1="{p[k][0]:.1f}" y1="{p[k][1]:.1f}" x2="{p[k + 1][0]:.1f}" y2="{p[k + 1][1]:.1f}" stroke="{C_R}" stroke-width="1"/>' for k in range(4))
    s_ += ''.join(atom(a, b, 2.3, C_R, '#1e293b') for a, b in p)
    return s_, p
z1, p1 = zincir(6, 12)
z2, p2 = zincir(6, 23)
for a, b in zip(p1, p2):
    o.append(kesik(a[0], a[1], b[0], b[1], AMB, .5, 2.6))
o += [z1, z2]
def top(x, y):
    s_ = ''
    for dx, dy in ((-4.6, 0), (4.6, 0), (0, -4.6), (0, 4.6)):
        s_ += f'<line x1="{x}" y1="{y}" x2="{x + dx}" y2="{y + dy}" stroke="{C_R}" stroke-width="1"/>'
    for dx, dy in ((-4.6, 0), (4.6, 0), (0, -4.6), (0, 4.6), (0, 0)):
        s_ += atom(x + dx, y + dy, 2.3, C_R, '#1e293b')
    return s_
o.append(top(62, 17))
o.append(top(78.4, 17))
o.append(kesik(67, 17, 73.6, 17, AMB, .5, .8))
o.append(f'<text x="17" y="33" font-size="3.1" font-weight="800" fill="{M}">n-pentan · KN 36 °C</text>')
o.append(f'<text x="17" y="37.4" font-size="2.7" fill="{S}">uzun zincir · geniş temas</text>')
o.append(f'<text x="70" y="33" font-size="3.1" font-weight="800" fill="{M}">neopentan · KN 9,5 °C</text>')
o.append(f'<text x="70" y="37.4" font-size="2.7" fill="{S}">küresel · dar temas</text>')
o.append('</g></svg>')
w('izomer', ''.join(o))

# ------------------------------------------------------------------ 8) hidrojen bağı ağı (s.5)
o = ['<svg viewBox="0 0 120 56" class="grafik"><g font-family="Inter" text-anchor="middle">']
s = 1.3
d = 4.4 * s
cx, cy = 34, 28
parcalar = []
hb = []
# merkez: H'ler aşağı (90°)
w0, h0 = su(cx, cy, 90, s, True)
# alıcılar (merkezin H'lerinin karşısında)
for (hx, hy), ang in zip(h0, (37.75, 142.25)):
    a = math.radians(ang)
    ox, oy = hx + 11 * math.cos(a), hy + 11 * math.sin(a)
    ws, _ = su(ox, oy, ang - 40 if ang < 90 else ang + 40, s, True)
    parcalar.append(ws)
    hb.append(kesik(hx, hy, ox, oy, AMB, .7, 2.6))
# vericiler (merkezin O'suna H gönderir)
for yon in (-125, -55):
    a = math.radians(yon)
    ox, oy = cx + 16.7 * math.cos(a), cy + 16.7 * math.sin(a)
    ic = yon + 180
    ws, hh = su(ox, oy, ic + 52.25 if yon < -90 else ic - 52.25, s, True)
    parcalar.append(ws)
    hx, hy = hh[0] if yon < -90 else hh[1]
    hb.append(kesik(hx, hy, cx, cy, AMB, .7, 2.6))
o += hb + parcalar + [w0]
# HF zinciri
fpts = [(76, 22), (92, 30), (108, 22)]
for k, (fx, fy) in enumerate(fpts):
    if k < 2:
        nx, ny = fpts[k + 1]
        L = math.hypot(nx - fx, ny - fy)
        hx, hy = fx + (nx - fx) / L * 5.2, fy + (ny - fy) / L * 5.2
        o.append(kesik(hx, hy, nx, ny, AMB, .7, 2.4))
        o.append(atom(fx, fy, 3.8, F_R, F_S, 'F', '#365314', 3.4))
        o.append(atom(hx, hy, 2.4, H_F, H_S, 'H', M, 2.4))
    else:
        o.append(atom(fx, fy, 3.8, F_R, F_S, 'F', '#365314', 3.4))
        a = math.radians(-30)
        o.append(atom(fx + 5.2 * math.cos(a), fy + 5.2 * math.sin(a), 2.4, H_F, H_S, 'H', M, 2.4))
o.append(f'<text x="92" y="44" font-size="3.1" font-weight="800" fill="{M}">HF zinciri</text>')
o.append(f'<text x="92" y="48.4" font-size="2.7" fill="{S}">F–H ··· F–H ··· F–H</text>')
o.append(f'<text x="34" y="54.5" font-size="3" font-weight="700" fill="{M}">Sudaki hidrojen bağları (- - -)</text>')
o.append('</g></svg>')
w('hbag', ''.join(o))

# ------------------------------------------------------------------ 9) hidrür grafiği (s.6)
grup = [
    ('4A', GRI, ['CH4', 'SiH4', 'GeH4', 'SnH4'], [-161.5, -111.9, -88.5, -51.8]),
    ('5A', MAV, ['NH3', 'PH3', 'AsH3', 'SbH3'], [-33.3, -87.7, -62.5, -17.0]),
    ('6A', KIR, ['H2O', 'H2S', 'H2Se', 'H2Te'], [100.0, -60.3, -41.3, -2.2]),
    ('7A', YES, ['HF', 'HCl', 'HBr', 'HI'], [19.5, -85.1, -66.8, -35.4]),
]
x0, x1, yt, yb = 20, 116, 8, 74
Xp = lambda p: x0 + 12 + (p - 2) * 26
Yv = lambda v: yb - (v + 180) / 300 * (yb - yt)
o = [f'<svg viewBox="0 0 120 86" class="grafik"><g font-family="Inter" font-size="3.1" fill="{S}">']
for v in range(-180, 121, 30):
    o.append(f'<line x1="{x0}" y1="{Yv(v):.1f}" x2="{x1}" y2="{Yv(v):.1f}" stroke="#e5e7f0" stroke-width=".3"/>')
    if v % 60 == 0:
        o.append(f'<text x="{x0 - 1.5}" y="{Yv(v) + 1:.1f}" text-anchor="end">{sy(v)}</text>')
o.append(f'<line x1="{x0}" y1="{Yv(0):.1f}" x2="{x1}" y2="{Yv(0):.1f}" stroke="#cbd5e1" stroke-width=".4"/>')
o.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{M}" stroke-width=".45"/>')
o.append(f'<line x1="{x0}" y1="{yb}" x2="{x0}" y2="{yt - 3}" stroke="{M}" stroke-width=".45"/>')
for p in (2, 3, 4, 5):
    o.append(f'<text x="{Xp(p)}" y="{yb + 4.4}" text-anchor="middle">{p}</text>')
o.append(f'<text x="{(x0 + x1) / 2}" y="{yb + 9.5}" text-anchor="middle" fill="{M}" font-weight="700">Periyot</text>')
o.append(f'<text x="1" y="4" fill="{M}" font-weight="700">Kaynama noktası (°C)</text>')
o.append(f'<rect x="{Xp(2) - 6}" y="{yt - 1}" width="12" height="{Yv(-45) - yt + 1:.1f}" rx="2" fill="{AMB}" fill-opacity=".14" stroke="{AMB}" stroke-width=".35" stroke-dasharray="1 .7"/>')
etk = {'CH4': (5.5, 1.2), 'NH3': (-6.2, -1.8), 'H2O': (6.5, 1.2), 'HF': (5, 1.5),
       'SnH4': (5.2, 4), 'SbH3': (5.2, 1.6), 'H2Te': (5.6, -1.2), 'HI': (4.4, 1.5)}
for ad, renk, fs_, kn in grup:
    pts = [(Xp(p), Yv(v)) for p, v in zip((2, 3, 4, 5), kn)]
    o.append('<polyline fill="none" stroke="%s" stroke-width=".8" points="%s"/>' % (renk, ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)))
    for (a, b), f in zip(pts, fs_):
        o.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="1.1" fill="{renk}"/>')
        if f in etk:
            dx, dy = etk[f]
            o.append(f'<text x="{a + dx:.1f}" y="{b + dy:.1f}" text-anchor="middle" font-size="2.9" font-weight="800" fill="{renk}">{alt(f)}</text>')
# lejant
for k, (ad, renk, fs_, kn) in enumerate(grup):
    yy = 13 + k * 4.4
    o.append(f'<line x1="66" y1="{yy - 1}" x2="71" y2="{yy - 1}" stroke="{renk}" stroke-width="1"/>')
    o.append(f'<text x="73" y="{yy}" font-size="2.8" fill="{M}"><tspan font-weight="800">{ad}</tspan> {alt(fs_[0])} → {alt(fs_[3])}</text>')
o.append(f'<text x="{Xp(2)}" y="{Yv(-45) + 3.6:.1f}" text-anchor="middle" font-size="2.6" font-weight="800" fill="#b45309">H bağı</text>')
o.append('</g></svg>')
w('hidrur', ''.join(o))

# ------------------------------------------------------------------ 10) 18 elektronlu tanecikler (s.6)
on8 = [('F2', -188.1, 'L'), ('Ar', -185.8, 'L'), ('HCl', -85.1, 'D'), ('H2S', -60.3, 'D'), ('CH3OH', 64.7, 'H')]
rk = {'L': '#7dd3fc', 'D': AMB, 'H': KIR}
x0, x1, yt, yb = 15, 90, 6, 44
Y = lambda v: yb - (v + 200) / 300 * (yb - yt)
o = [f'<svg viewBox="0 0 92 58" class="grafik"><g font-family="Inter" font-size="3" fill="{S}">']
for v in (-200, -150, -100, -50, 0, 50, 100):
    o.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="#e5e7f0" stroke-width=".3"/>')
    if v % 100 == 0:
        o.append(f'<text x="{x0 - 1.5}" y="{Y(v) + 1:.1f}" text-anchor="end">{sy(v)}</text>')
o.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{M}" stroke-width=".4"/><line x1="{x0}" y1="{yb}" x2="{x0}" y2="{yt - 2}" stroke="{M}" stroke-width=".4"/>')
o.append(f'<text x="1" y="3" fill="{M}" font-weight="700">KN (°C)</text>')
for i, (f, kn, t) in enumerate(on8):
    cx = x0 + 8.5 + i * 15
    o.append(f'<rect x="{cx - 5}" y="{Y(kn):.1f}" width="10" height="{yb - Y(kn):.1f}" rx="1" fill="{rk[t]}"/>')
    o.append(f'<text x="{cx}" y="{Y(kn) - 1.2:.1f}" text-anchor="middle" font-weight="700" fill="{M}">{sy(kn)}</text>')
    o.append(f'<text x="{cx}" y="{yb + 4.2}" text-anchor="middle" font-weight="800" fill="{M}" font-size="3.3">{alt(f)}</text>')
for k, (t, ad) in enumerate((('L', 'London'), ('D', 'Dipol–dipol'), ('H', 'Hidrojen bağı'))):
    xx = 6 + k * 30
    o.append(f'<rect x="{xx}" y="{yb + 8}" width="4" height="3" rx=".6" fill="{rk[t]}"/><text x="{xx + 5.5}" y="{yb + 10.5}" font-size="2.9" fill="{M}">{ad}</text>')
o.append('</g></svg>')
w('onsekiz', ''.join(o))

# ------------------------------------------------------------------ 11) etkileşim matrisi (s.7)
bas = [('İyon', 'Na⁺, Cl⁻, Mg²⁺…', '#8b5cf6'), ('Polar molekül', 'kalıcı dipol: H₂O, HCl…', U),
       ('Apolar molekül / soy gaz', 'anlık dipol: CH₄, I₂, Ar…', GRI)]
hucre = {
    (0, 0): ('İyonik bağ', 'güçlü etkileşim (Bölüm 1)', '#f1f5f9', S),
    (0, 1): ('İyon–dipol', 'tuzun suda çözünmesi', '#ede9fe', '#5b21b6'),
    (0, 2): ('İyon–indüklenmiş dipol', 'iyon apolar taneciği kutuplar', '#f5f3ff', '#6d28d9'),
    (1, 1): ('Dipol–dipol', 'H–F, H–O, H–N varsa: hidrojen bağı', '#e0f2fe', UK),
    (1, 2): ('Dipol–indüklenmiş dipol', 'O₂ gazının suda çözünmesi', '#f0f9ff', U),
    (2, 2): ('London kuvvetleri', 'I₂ – CCl₄, Ar – Ar', '#f1f5f9', '#334155'),
}
cw, ch, lx, ty = 50, 15, 28, 13
o = ['<svg viewBox="0 0 178 63" class="grafik"><g font-family="Inter" text-anchor="middle">']
for j, (a, b, r) in enumerate(bas):
    x = lx + j * cw + cw / 2
    o.append(f'<rect x="{lx + j * cw + .6}" y=".5" width="{cw - 1.2}" height="11" rx="2" fill="{r}"/>')
    o.append(f'<text x="{x}" y="5.4" font-size="3.3" font-weight="800" fill="#fff">{a}</text>')
    o.append(f'<text x="{x}" y="9.4" font-size="2.6" fill="#fff" fill-opacity=".9">{b}</text>')
    y = ty + j * ch + ch / 2
    o.append(f'<rect x=".5" y="{ty + j * ch + .6}" width="{lx - 1.5}" height="{ch - 1.2}" rx="2" fill="{r}"/>')
    kel = a.split(' ')
    if len(kel) == 1:
        o.append(f'<text x="{lx / 2}" y="{y + 1.2}" font-size="3.3" font-weight="800" fill="#fff">{a}</text>')
    elif len(kel) == 2:
        o.append(f'<text x="{lx / 2}" y="{y - .6}" font-size="3.1" font-weight="800" fill="#fff">{kel[0]}</text><text x="{lx / 2}" y="{y + 3.2}" font-size="3.1" font-weight="800" fill="#fff">{kel[1]}</text>')
    else:
        o.append(f'<text x="{lx / 2}" y="{y - 2.2}" font-size="3" font-weight="800" fill="#fff">Apolar</text><text x="{lx / 2}" y="{y + 1.3}" font-size="3" font-weight="800" fill="#fff">molekül /</text><text x="{lx / 2}" y="{y + 4.8}" font-size="3" font-weight="800" fill="#fff">soy gaz</text>')
for i in range(3):
    for j in range(3):
        a, b = (i, j) if i <= j else (j, i)
        t, alt_, bg, fg = hucre[(a, b)]
        x, y = lx + j * cw, ty + i * ch
        op = '1' if i <= j else '.45'
        o.append(f'<g opacity="{op}"><rect x="{x + .6}" y="{y + .6}" width="{cw - 1.2}" height="{ch - 1.2}" rx="2" fill="{bg}" stroke="{fg}" stroke-opacity=".35" stroke-width=".3"/>')
        o.append(f'<text x="{x + cw / 2}" y="{y + 6.6}" font-size="3.5" font-weight="800" fill="{fg}">{t}</text>')
        o.append(f'<text x="{x + cw / 2}" y="{y + 11}" font-size="2.7" fill="{S}">{alt_}</text></g>')
o.append(f'<text x="89" y="62" font-size="2.8" fill="{S}">Soluk kutular simetrik eşleri tekrarlar. Bütün tanecik çiftlerinde ayrıca London kuvvetleri de vardır.</text>')
o.append('</g></svg>')
w('matris', ''.join(o))

# ------------------------------------------------------------------ 12) kapak deseni
o = ['<g opacity=".9">']
sw_ = []
pts = []
import random
random.seed(7)
merkez = [(156, 46, 90), (182, 64, 30), (136, 70, 150), (166, 86, 75), (190, 102, 120), (194, 34, 250), (150, 110, 20)]
for (x, y, a) in merkez:
    s_, hh = su(x, y, a, 2.2)
    sw_.append(s_)
    pts.append(((x, y), hh))
# yakın O–H çiftleri arasında kesikli hidrojen bağları
cz = []
for i, ((ox, oy), hh) in enumerate(pts):
    for (hx, hy) in hh:
        best = None
        for j, ((px, py), _) in enumerate(pts):
            if j == i:
                continue
            dd = math.hypot(px - hx, py - hy)
            if dd < 22 and (best is None or dd < best[0]):
                best = (dd, px, py)
        if best:
            cz.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{best[1]:.1f}" y2="{best[2]:.1f}" stroke="#fbbf24" stroke-opacity=".75" stroke-width=".7" stroke-dasharray="1.6 1.2"/>')
o += cz + sw_
o.append('</g>')
w('kapak', ''.join(o).replace(O_R, '#38bdf8').replace('#b91c1c', '#e0f2fe').replace(H_F, '#ffffff').replace(H_S, '#bae6fd'))

# ------------------------------------------------------------------ 13) test: 6A hidrürleri
o = [f'<svg viewBox="0 0 84 48" class="grafik"><g font-family="Inter" font-size="3" fill="{S}">']
x0, x1, yt, yb = 16, 80, 5, 38
Y = lambda v: yb - (v + 100) / 220 * (yb - yt)
for v in (-100, -50, 0, 50, 100):
    o.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="#e5e7f0" stroke-width=".3"/><text x="{x0 - 1.5}" y="{Y(v) + 1:.1f}" text-anchor="end">{sy(v)}</text>')
o.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{M}" stroke-width=".4"/><line x1="{x0}" y1="{yb}" x2="{x0}" y2="{yt - 2}" stroke="{M}" stroke-width=".4"/>')
dat = [('H2O', 100.0), ('H2S', -60.3), ('H2Se', -41.3), ('H2Te', -2.2)]
pts = [(x0 + 9 + k * 16, Y(v)) for k, (_, v) in enumerate(dat)]
o.append('<polyline fill="none" stroke="%s" stroke-width=".8" points="%s"/>' % (U, ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)))
for (a, b), (f, v) in zip(pts, dat):
    o.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="1.1" fill="{U}"/>')
    o.append(f'<text x="{a:.1f}" y="{yb + 4.3}" text-anchor="middle" font-weight="800" fill="{M}" font-size="3.2">{alt(f)}</text>')
o.append(f'<text x="{(x0 + x1) / 2}" y="{yb + 8.8}" text-anchor="middle" fill="{M}" font-weight="700">Molekül kütlesi artar →</text>')
o.append(f'<text x="1" y="2.6" fill="{M}" font-weight="700">KN (°C)</text>')
o.append('</g></svg>')
w('test5', ''.join(o))

# ------------------------------------------------------------------ 14) bağlam: O2 çözünürlüğü
dat = [(0, 14.6), (10, 11.3), (20, 9.1), (30, 7.6), (40, 6.4)]
x0, x1, yt, yb = 14, 88, 5, 44
X = lambda t: x0 + 4 + t / 40 * (x1 - x0 - 8)
Y = lambda v: yb - v / 16 * (yb - yt)
o = [f'<svg viewBox="0 0 92 56" class="grafik"><g font-family="Inter" font-size="3" fill="{S}">']
for v in (0, 4, 8, 12, 16):
    o.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="#e5e7f0" stroke-width=".3"/><text x="{x0 - 1.5}" y="{Y(v) + 1:.1f}" text-anchor="end">{v}</text>')
for t, _ in dat:
    o.append(f'<text x="{X(t):.1f}" y="{yb + 4.2}" text-anchor="middle">{t}</text>')
o.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{M}" stroke-width=".4"/><line x1="{x0}" y1="{yb}" x2="{x0}" y2="{yt - 2}" stroke="{M}" stroke-width=".4"/>')
o.append('<polyline fill="none" stroke="%s" stroke-width=".9" points="%s"/>' % (U, ' '.join(f'{X(t):.1f},{Y(v):.1f}' for t, v in dat)))
for t, v in dat:
    o.append(f'<circle cx="{X(t):.1f}" cy="{Y(v):.1f}" r="1.1" fill="{U}"/><text x="{X(t) + 1.5:.1f}" y="{Y(v) - 1.6:.1f}" font-weight="700" fill="{M}">{str(v).replace(".", ",")}</text>')
o.append(f'<text x="{(x0 + x1) / 2}" y="{yb + 9}" text-anchor="middle" fill="{M}" font-weight="700">Su sıcaklığı (°C)</text>')
o.append(f'<text x="1" y="2.6" fill="{M}" font-weight="700">Çözünmüş O₂ (mg/L)</text>')
o.append('</g></svg>')
w('oksijen', ''.join(o))

# ------------------------------------------------------------------ 15) bağlam: damlalar
o = ['<svg viewBox="0 0 92 30" class="grafik"><defs><linearGradient id="dm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7dd3fc"/><stop offset="1" stop-color="#0284c7"/></linearGradient></defs><g font-family="Inter" text-anchor="middle">']
o.append(f'<rect x="3" y="17" width="40" height="3" rx=".6" fill="#cbd5e1" stroke="#94a3b8" stroke-width=".3"/>')
o.append('<path d="M8 17 Q23 11.5 38 17 Z" fill="url(#dm)"/>')
o.append(f'<rect x="49" y="17" width="40" height="3" rx=".6" fill="#fde68a" stroke="#d97706" stroke-width=".3"/>')
o.append('<path d="M63.2 17 A6.6 6.6 0 1 1 74.8 17 Z" fill="url(#dm)"/>')
o.append(f'<text x="23" y="25.5" font-size="3.1" font-weight="800" fill="{M}">Temiz cam</text><text x="23" y="29" font-size="2.6" fill="{S}">damla yayılır</text>')
o.append(f'<text x="69" y="25.5" font-size="3.1" font-weight="800" fill="{M}">Parafin (mum) kaplı yüzey</text><text x="69" y="29" font-size="2.6" fill="{S}">damla boncuk gibi toplanır</text>')
o.append('</g></svg>')
w('damla', ''.join(o))

print('SVG üretildi:', sorted(os.listdir(D)))
