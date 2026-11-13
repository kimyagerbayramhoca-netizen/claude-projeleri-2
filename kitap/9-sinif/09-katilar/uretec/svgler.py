"""Katılar ünitesinin SVG çizimlerini üretir (svg/*.svg). Kullanım: python3 svgler.py"""
import math
import os
import random

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg')
os.makedirs(D, exist_ok=True)

U = '#475569'; UK = '#273242'; UA = '#f1f4f8'
S = '#5d6478'; M = '#1d2133'; AMB = '#f59e0b'; TEAL = '#0f8f84'; ROSE = '#e11d48'
KAT = '#7c3aed'      # katyon (Na+, Mg2+)
ANY = '#10b981'      # anyon (Cl-)
CK = '#334155'       # karbon
OK = '#e11d48'       # oksijen
MET = '#94a3b8'      # metal katyonu
IOD = '#8b5cf6'      # iyot


def w(ad, s):
    with open(os.path.join(D, ad + '.svg'), 'w', encoding='utf-8') as f:
        f.write(s)


def ok_marker(id_, renk):
    return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.2" '
            f'markerHeight="4.2" orient="auto"><path d="M0 0 10 5 0 10z" fill="{renk}"/></marker>')


# ------------------------------------------------------------------
# 1) Kristal ve amorf düzen (SiO2 benzeri 2B ağ)
# ------------------------------------------------------------------
def petek(nx, ny, a):
    """Bal peteği: düğümler ve kenarlar"""
    pts = {}
    h = a * math.sqrt(3) / 2
    for j in range(ny):
        for i in range(nx):
            x = i * 1.5 * a
            y = j * 2 * h + (h if i % 2 else 0)
            pts[(i, j, 0)] = (x, y)
            pts[(i, j, 1)] = (x + a, y)
    # kenarları uzaklıkla bul
    keys = list(pts)
    ed = []
    for p in range(len(keys)):
        for q in range(p + 1, len(keys)):
            (x1, y1), (x2, y2) = pts[keys[p]], pts[keys[q]]
            if abs(math.hypot(x1 - x2, y1 - y2) - a) < 1e-6:
                ed.append((keys[p], keys[q]))
    return pts, ed


def ag(pts, ed, ox, oy, jit, seed, clip):
    rnd = random.Random(seed)
    P = {}
    for k, (x, y) in pts.items():
        dx = rnd.uniform(-jit, jit); dy = rnd.uniform(-jit, jit)
        P[k] = (ox + x + dx, oy + y + dy)
    x0, y0, x1, y1 = clip
    ins = lambda p: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
    o = []
    for a_, b_ in ed:
        A, B = P[a_], P[b_]
        if ins(A) and ins(B):
            o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="#94a3b8" stroke-width=".55"/>')
    for a_, b_ in ed:
        A, B = P[a_], P[b_]
        if ins(A) and ins(B):
            mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
            o.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="1.25" fill="{OK}"/>')
    for k, p in P.items():
        if ins(p):
            o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2" fill="{CK}"/>')
    return ''.join(o)


pts, ed = petek(9, 3, 7)
o = [f'<svg viewBox="0 0 180 53" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(f'<rect x="1" y="1" width="86" height="39" rx="3" fill="{UA}"/>')
o.append(f'<rect x="93" y="1" width="86" height="39" rx="3" fill="#fbf7f0"/>')
o.append(ag(pts, ed, 6, 5, 0, 1, (4, 3, 84, 38)))
o.append(ag(pts, ed, 98, 5, 2.3, 7, (96, 3, 176, 38)))
o.append(f'<text x="44" y="46" font-size="4.4" font-weight="800" fill="{UK}">KRİSTAL (kuvars)</text>')
o.append(f'<text x="44" y="51" font-size="3.4" fill="{S}">Aynı desen her yönde tekrar eder</text>')
o.append(f'<text x="136" y="46" font-size="4.4" font-weight="800" fill="#8a4a03">AMORF (cam)</text>')
o.append(f'<text x="136" y="51" font-size="3.4" fill="{S}">Halkalar bozuk, uzun erimli düzen yok</text>')
o.append('</g></svg>')
w('duzen', ''.join(o))

# ------------------------------------------------------------------
# 2) Isıtma eğrileri: kristal ve amorf
# ------------------------------------------------------------------
o = [f'<svg viewBox="0 0 180 50" class="grafik"><g font-family="Inter" font-size="3.6" fill="{S}">']
for (ox, bas, renk) in [(6, 'Kristal katı', U), (96, 'Amorf katı', '#c26a06')]:
    x0, y0, x1, y1 = ox + 8, 41, ox + 80, 7
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{M}" stroke-width=".45"/>')
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{M}" stroke-width=".45"/>')
    o.append(f'<text x="{(x0 + x1) / 2}" y="{y0 + 5}" text-anchor="middle" fill="{M}" font-weight="700">Zaman (ısı verilir)</text>')
    o.append(f'<text x="{x0 - 2}" y="{y1 - 2}" fill="{M}" font-weight="700" text-anchor="start">Sıcaklık</text>')
    o.append(f'<text x="{x1}" y="{y1 + 1}" text-anchor="end" font-size="4.4" font-weight="800" fill="{renk}">{bas}</text>')
    if ox == 6:
        yp = y0 - 16
        o.append(f'<polyline fill="none" stroke="{renk}" stroke-width="1.1" points="{x0},{y0 - 3} {x0 + 22},{yp} {x0 + 50},{yp} {x0 + 70},{y0 - 30}"/>')
        o.append(f'<line x1="{x0}" y1="{yp}" x2="{x0 + 22}" y2="{yp}" stroke="{renk}" stroke-width=".35" stroke-dasharray="1.2 1"/>')
        o.append(f'<text x="{x0 + 1}" y="{yp - 1.5}" text-anchor="start" font-size="3.3" fill="{UK}" font-weight="700">Erime noktası</text>')
        o.append(f'<text x="{x0 + 36}" y="{yp + 5}" text-anchor="middle" font-size="3.2">katı + sıvı</text>')
        o.append(f'<text x="{x0 + 36}" y="{yp + 9}" text-anchor="middle" font-size="3.2">sıcaklık sabit</text>')
    else:
        o.append(f'<rect x="{x0 + 1}" y="{y0 - 24}" width="{x1 - x0 - 2}" height="11" fill="#fff6e5"/>')
        o.append(f'<text x="{x1 - 1}" y="{y0 - 14.6}" text-anchor="end" font-size="3.2" fill="#8a4a03" font-weight="700">yumuşama aralığı</text>')
        o.append(f'<path d="M{x0},{y0 - 3} C{x0 + 20},{y0 - 14} {x0 + 30},{y0 - 16} {x0 + 40},{y0 - 18} S{x0 + 60},{y0 - 24} {x0 + 70},{y0 - 31}" fill="none" stroke="{renk}" stroke-width="1.1"/>')
        o.append(f'<text x="{x0 + 3}" y="{y0 - 29}" text-anchor="start" font-size="3.2">Düz bölge (plato) yok:</text>')
        o.append(f'<text x="{x0 + 3}" y="{y0 - 25.4}" text-anchor="start" font-size="3.2">giderek akışkanlaşır</text>')
o.append('</g></svg>')
w('isitma', ''.join(o))

# ------------------------------------------------------------------
# 3) NaCl kristal örgüsü (3x3x3 iyon, eğik izdüşüm)
# ------------------------------------------------------------------
def nacl(ox, oy, s, n=3, etiket=True):
    cx, cy = s * 0.5, -s * 0.36
    P = lambda i, j, k: (ox + i * s + k * cx, oy - j * s + k * cy)
    o = []
    for k in range(n - 1, -1, -1):
        sol = 0.55 + 0.45 * (1 - k / (n - 1))
        # çizgiler
        for i in range(n):
            for j in range(n):
                a = P(i, j, k)
                for (di, dj, dk) in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    if i + di < n and j + dj < n and k + dk < n:
                        b = P(i + di, j + dj, k + dk)
                        o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#94a3b8" stroke-width=".4" opacity="{sol:.2f}"/>')
        for j in range(n):
            for i in range(n):
                x, y = P(i, j, k)
                if (i + j + k) % 2 == 0:
                    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s * 0.27:.1f}" fill="{ANY}" stroke="#047857" stroke-width=".3" opacity="{sol:.2f}"/>')
                else:
                    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s * 0.16:.1f}" fill="{KAT}" stroke="#5b21b6" stroke-width=".3" opacity="{sol:.2f}"/>')
    return ''.join(o)


o = ['<svg viewBox="0 0 92 84" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(nacl(14, 66, 22))
o.append(f'<circle cx="10" cy="80" r="2.6" fill="{ANY}"/><text x="14" y="81.4" text-anchor="start" font-size="4" fill="{M}">Cl⁻</text>')
o.append(f'<circle cx="30" cy="80" r="1.6" fill="{KAT}"/><text x="33" y="81.4" text-anchor="start" font-size="4" fill="{M}">Na⁺</text>')
o.append(f'<text x="70" y="81.4" font-size="3.4" fill="{S}">çizgiler: örgü</text>')
o.append('</g></svg>')
w('nacl', ''.join(o))

# ------------------------------------------------------------------
# 4) İyonik katıda kayma: kırılganlık
# ------------------------------------------------------------------
def iyon(x, y, art):
    if art:
        return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{KAT}"/>'
                f'<text x="{x:.1f}" y="{y + 1.6:.1f}" font-size="4.6" font-weight="800" fill="#fff">+</text>')
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{ANY}"/>'
            f'<text x="{x:.1f}" y="{y + 1.6:.1f}" font-size="5" font-weight="800" fill="#fff">−</text>')


o = ['<svg viewBox="0 0 180 50" class="grafik"><g font-family="Inter" text-anchor="middle">', '<defs>' + ok_marker('kk', M) + ok_marker('kr', ROSE) + '</defs>']
for pan, kay in [(0, 0), (1, 1)]:
    ox = 6 + pan * 98
    for r in range(3):
        sh = (9.5 if (r == 0 and kay) else 0)
        for c in range(6):
            o.append(iyon(ox + c * 9.5 + sh, 9 + r * 10, (r + c) % 2 == 0))
    if kay:
        o.append(f'<path d="M{ox + 2} 2.5 H{ox + 14}" stroke="{M}" stroke-width=".6" marker-end="url(#kk)"/>')
        o.append(f'<line x1="{ox - 2}" y1="14" x2="{ox + 66}" y2="14" stroke="{ROSE}" stroke-width=".5" stroke-dasharray="1.6 1"/>')
o.append(f'<text x="38" y="44" font-size="3.8" fill="{M}" font-weight="700">Düzenli dizilim: zıt yükler komşu</text>')
o.append(f'<text x="38" y="48.5" font-size="3.3" fill="{S}">her iyonu zıt yüklüler çevreler</text>')
o.append(f'<path d="M76 20 H96" stroke="{M}" stroke-width=".7" marker-end="url(#kk)"/><text x="86" y="17.5" font-size="3.3" fill="{S}">darbe</text>')
o.append(f'<text x="136" y="44" font-size="3.8" fill="{ROSE}" font-weight="700">Katman kayar: aynı yükler karşı karşıya</text>')
o.append(f'<text x="136" y="48.5" font-size="3.3" fill="{S}">itme kuvveti kristali bu düzlemden ayırır</text>')
o.append('</g></svg>')
w('kayma_iyon', ''.join(o))

# ------------------------------------------------------------------
# 5) Moleküler kristaller: buz (H bağları) ve iyot (London)
# ------------------------------------------------------------------
def buz(ox, oy, a, nx, ny, clip):
    h = a * math.sqrt(3) / 2
    # sivri uçlu petek: A ve B alt örgüleri
    A = []
    for j in range(ny):
        for i in range(nx):
            x = ox + i * 2 * h + (h if j % 2 else 0)
            y = oy + j * 1.5 * a
            A.append((x, y))
    dirs = [(0, a), (h, -a / 2), (-h, -a / 2)]  # A -> B yönleri
    x0, y0, x1, y1 = clip
    ins = lambda p: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
    cov, hb, Hs, Os, outH = [], [], [], set(), []
    for (x, y) in A:
        for d, (dx, dy) in enumerate(dirs):
            B = (round(x + dx, 3), round(y + dy, 3))
            Ap = (round(x, 3), round(y, 3))
            if not (ins(Ap) and ins(B)):
                continue
            Os.add(Ap); Os.add(B)
            own, oth = (Ap, B) if d in (1, 2) else (B, Ap)
            hx = own[0] + (oth[0] - own[0]) * 0.34
            hy = own[1] + (oth[1] - own[1]) * 0.34
            cov.append((own, (hx, hy)))
            hb.append(((hx, hy), oth))
            Hs.append((hx, hy))
    # B düğümlerinin düzlem dışı H'si
    for (x, y) in A:
        B = (round(x, 3), round(y + a, 3))
        if B in Os:
            outH.append((B[0] + 1.6, B[1] + 1.1))
            cov.append((B, (B[0] + 1.6, B[1] + 1.1)))
    o = []
    for (p, q) in hb:
        o.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{TEAL}" stroke-width=".55" stroke-dasharray="1 .8"/>')
    for (p, q) in cov:
        o.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#64748b" stroke-width=".8"/>')
    for (x, y) in Os:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="{OK}"/>')
    for (x, y) in Hs + outH:
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.15" fill="#fff" stroke="#64748b" stroke-width=".35"/>')
    return ''.join(o)


o = ['<svg viewBox="0 0 180 62" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(f'<rect x="1" y="1" width="96" height="50" rx="3" fill="#f0fbfa"/>')
o.append(buz(11, 8, 8.2, 7, 4, (3, 3, 95, 49)))
o.append(f'<rect x="102" y="1" width="77" height="50" rx="3" fill="#f6f3ff"/>')
for r in range(3):
    for c in range(4):
        x = 112 + c * 18 + (9 if r % 2 else 0) * 0
        y = 10 + r * 15
        ang = 35 if (r + c) % 2 == 0 else -35
        dx, dy = 2.6 * math.cos(math.radians(ang)), 2.6 * math.sin(math.radians(ang))
        o.append(f'<circle cx="{x - dx:.1f}" cy="{y - dy:.1f}" r="3.4" fill="{IOD}" stroke="#5b21b6" stroke-width=".3"/>')
        o.append(f'<circle cx="{x + dx:.1f}" cy="{y + dy:.1f}" r="3.4" fill="{IOD}" stroke="#5b21b6" stroke-width=".3"/>')
o.append(f'<text x="49" y="56" font-size="4.2" font-weight="800" fill="#0b6b62">Buz, H₂O(k)</text>')
o.append(f'<text x="49" y="61" font-size="3.3" fill="{S}">kesikli çizgi: hidrojen bağı · boşluklu altıgen halkalar</text>')
o.append(f'<text x="140.5" y="56" font-size="4.2" font-weight="800" fill="#5b21b6">İyot, I₂(k)</text>')
o.append(f'<text x="140.5" y="61" font-size="3.3" fill="{S}">molekülleri London kuvvetleri tutar</text>')
o.append('</g></svg>')
w('molekuler', ''.join(o))

# ------------------------------------------------------------------
# 6) Elmas birim hücresi (izdüşüm)
# ------------------------------------------------------------------
def rot(p, ay, ax):
    x, y, z = p
    c, s = math.cos(ay), math.sin(ay)
    x, z = c * x + s * z, -s * x + c * z
    c, s = math.cos(ax), math.sin(ax)
    y, z = c * y - s * z, s * y + c * z
    return x, y, z


fcc = [(0, 0, 0), (0, 2, 2), (2, 0, 2), (2, 2, 0)]
atoms = set()
for bx in range(-1, 3):
    for by in range(-1, 3):
        for bz in range(-1, 3):
            for (a, b, c) in fcc:
                for off in [(0, 0, 0), (1, 1, 1)]:
                    p = (a + 4 * bx + off[0], b + 4 * by + off[1], c + 4 * bz + off[2])
                    if all(0 <= t <= 4 for t in p):
                        atoms.add(p)
atoms = sorted(atoms)
bonds = [(p, q) for i, p in enumerate(atoms) for q in atoms[i + 1:]
         if abs(sum((p[k] - q[k]) ** 2 for k in range(3)) - 3) < 1e-9]


def elmas(ox, oy, sc):
    ay, ax = math.radians(28), math.radians(-18)
    R = {p: rot((p[0] - 2, p[1] - 2, p[2] - 2), ay, ax) for p in atoms}
    Pj = lambda p: (ox + R[p][0] * sc, oy - R[p][1] * sc)
    o = []
    # küp kenarları
    kose = [(x, y, z) for x in (0, 4) for y in (0, 4) for z in (0, 4)]
    for i, p in enumerate(kose):
        for q in kose[i + 1:]:
            if sum(p[k] != q[k] for k in range(3)) == 1:
                rp = rot((p[0] - 2, p[1] - 2, p[2] - 2), ay, ax); rq = rot((q[0] - 2, q[1] - 2, q[2] - 2), ay, ax)
                o.append(f'<line x1="{ox + rp[0] * sc:.1f}" y1="{oy - rp[1] * sc:.1f}" x2="{ox + rq[0] * sc:.1f}" y2="{oy - rq[1] * sc:.1f}" stroke="#cbd5e1" stroke-width=".35" stroke-dasharray="1.2 1"/>')
    items = []
    for (p, q) in bonds:
        z = (R[p][2] + R[q][2]) / 2
        items.append((z, 'b', p, q))
    for p in atoms:
        items.append((R[p][2], 'a', p, None))
    items.sort(key=lambda t: t[0])
    for z, t, p, q in items:
        f = 0.55 + 0.45 * (z + 3) / 6
        if t == 'b':
            A, B = Pj(p), Pj(q)
            o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="#64748b" stroke-width="1.1" opacity="{f:.2f}"/>')
        else:
            A = Pj(p)
            ic = all(0 < t_ < 4 for t_ in p)
            o.append(f'<circle cx="{A[0]:.1f}" cy="{A[1]:.1f}" r="{2.5 + 0.35 * z:.2f}" fill="{"#0ea5e9" if ic else CK}" opacity="{min(1, f + .1):.2f}"/>')
    return ''.join(o)


def grafit(ox, oy, a, katman=3, ara=17):
    o = []
    h = a * math.sqrt(3) / 2
    pts, ed = petek(6, 3, a)
    sx, sy = 1.0, 0.36  # yatay düzlem, basık
    sh = 0.35 * a
    for L in range(katman - 1, -1, -1):
        dx = (a if L % 2 else 0)
        P = {k: (ox + (x + dx) * sx + y * 0.55, oy - L * ara + y * sy) for k, (x, y) in pts.items()}
        sol = 1.0 if L == 0 else 0.85
        for (p, q) in ed:
            A, B = P[p], P[q]
            o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="#64748b" stroke-width=".9" opacity="{sol}"/>')
        for k, (x, y) in P.items():
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.45" fill="{CK}" opacity="{sol}"/>')
    return ''.join(o)


o = ['<svg viewBox="0 0 180 64" class="grafik"><g font-family="Inter" text-anchor="middle">']
o.append(f'<rect x="1" y="1" width="72" height="51" rx="3" fill="{UA}"/>')
o.append(elmas(37, 26.5, 6.6))
o.append(f'<rect x="78" y="1" width="101" height="51" rx="3" fill="{UA}"/>')
o.append(grafit(86, 35, 7.0, 3, 12))
o.append(f'<line x1="172" y1="12" x2="172" y2="40" stroke="{AMB}" stroke-width=".5" stroke-dasharray="1 .8"/>')
o.append(f'<text x="170" y="22" font-size="3.2" fill="#b45309" text-anchor="end" font-weight="700">zayıf</text>')
o.append(f'<text x="170" y="26" font-size="3.2" fill="#b45309" text-anchor="end">katmanlar</text>')
o.append(f'<text x="170" y="30" font-size="3.2" fill="#b45309" text-anchor="end">arası</text>')
o.append(f'<text x="37" y="57" font-size="4.2" font-weight="800" fill="{UK}">Elmas</text>')
o.append(f'<text x="37" y="62" font-size="3.3" fill="{S}">her C, 4 C ile bağlı (düzgün dörtyüzlü)</text>')
o.append(f'<text x="128.5" y="57" font-size="4.2" font-weight="800" fill="{UK}">Grafit</text>')
o.append(f'<text x="128.5" y="62" font-size="3.3" fill="{S}">her C, 3 C ile bağlı; altıgen katmanlar üst üste</text>')
o.append('</g></svg>')
w('karbon', ''.join(o))

# ------------------------------------------------------------------
# 7) Metalik bağ: elektron denizi + kayma
# ------------------------------------------------------------------
def metal(ox, oy, nx, ny, d, seed, kay=0):
    rnd = random.Random(seed)
    o = [f'<rect x="{ox - 5}" y="{oy - 5}" width="{(nx - 1) * d + 10 + kay}" height="{(ny - 1) * d + 10}" rx="3" fill="#fff7e6"/>']
    for _ in range(int(nx * ny * 1.6)):
        x = ox - 3 + rnd.uniform(0, (nx - 1) * d + 6 + kay); y = oy - 3 + rnd.uniform(0, (ny - 1) * d + 6)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r=".7" fill="{AMB}"/>')
    for r in range(ny):
        for c in range(nx):
            x = ox + c * d + (kay if r == 0 else 0); y = oy + r * d
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{d * 0.32:.1f}" fill="{MET}" stroke="#64748b" stroke-width=".3"/>'
                     f'<text x="{x:.1f}" y="{y + 1.4:.1f}" font-size="3.8" font-weight="800" fill="#fff">+</text>')
    return ''.join(o)


o = ['<svg viewBox="0 0 180 47" class="grafik"><g font-family="Inter" text-anchor="middle">', '<defs>' + ok_marker('mk', M) + '</defs>']
o.append(metal(10, 9, 6, 3, 9, 3))
o.append(f'<path d="M70 18 H90" stroke="{M}" stroke-width=".7" marker-end="url(#mk)"/><text x="80" y="15.5" font-size="3.3" fill="{S}">darbe</text>')
o.append(metal(105, 9, 6, 3, 9, 5, kay=9))
o.append(f'<path d="M104 2.4 H116" stroke="{M}" stroke-width=".6" marker-end="url(#mk)"/>')
o.append(f'<text x="35" y="37" font-size="3.8" fill="{M}" font-weight="700">Katyonlar + serbest elektronlar</text>')
o.append(f'<text x="35" y="41.5" font-size="3.3" fill="{S}">elektronlar tek bir atoma ait değildir</text>')
o.append(f'<text x="138" y="37" font-size="3.8" fill="{TEAL}" font-weight="700">Katman kayar, bağ kopmaz</text>')
o.append(f'<text x="138" y="41.5" font-size="3.3" fill="{S}">elektron denizi katyonları yine bir arada tutar</text>')
o.append(f'<circle cx="62" cy="45.6" r=".9" fill="{AMB}"/><text x="64" y="46.8" font-size="3.2" fill="{S}" text-anchor="start">elektron</text>')
o.append(f'<circle cx="86" cy="45.6" r="1.6" fill="{MET}"/><text x="89" y="46.8" font-size="3.2" fill="{S}" text-anchor="start">metal katyonu</text>')
o.append('</g></svg>')
w('metal', ''.join(o))

# ------------------------------------------------------------------
# 8) Erime noktası karşılaştırma çubukları (katı türüne göre)
# ------------------------------------------------------------------
veri = [
    ('Moleküler', U, [('Kuru buz*', -78.5), ('Buz', 0), ('Naftalin', 80), ('İyot', 114)]),
    ('Metalik', '#c26a06', [('Sodyum', 98), ('Alüminyum', 660), ('Demir', 1538), ('Tungsten', 3422)]),
    ('İyonik', KAT, [('KCl', 770), ('NaCl', 801), ('CaF₂', 1418), ('MgO', 2852)]),
    ('Kovalent ağ', TEAL, [('Silisyum', 1414), ('Kuvars', 1713), ('SiC*', 2730), ('Grafit*', 3650)]),
]
x0, xs = 25, 72 / 3800
X = lambda t: x0 + t * xs
o = [f'<svg viewBox="0 0 110 118" class="grafik"><g font-family="Inter" font-size="3.4" fill="{S}">']
for t in range(0, 3801, 1000):
    o.append(f'<line x1="{X(t):.1f}" y1="2" x2="{X(t):.1f}" y2="106" stroke="#e5e7f0" stroke-width=".3"/>')
    o.append(f'<text x="{X(t):.1f}" y="110" text-anchor="middle">{t}</text>')
o.append(f'<line x1="{X(0):.1f}" y1="2" x2="{X(0):.1f}" y2="106" stroke="{M}" stroke-width=".45"/>')
o.append(f'<text x="{X(1900):.1f}" y="115.5" text-anchor="middle" fill="{M}" font-weight="700" font-size="3.6">Erime noktası (°C, 1 atm)</text>')
y = 3
for grup, renk, liste in veri:
    o.append(f'<text x="{x0 + 1}" y="{y + 1.4}" font-weight="800" fill="{renk}" font-size="3.6">{grup}</text>')
    y += 5
    for ad, t in liste:
        o.append(f'<text x="{x0 - (3.4 if t < 0 else 1.2):.1f}" y="{y + 1.3:.1f}" text-anchor="end" fill="{M}" font-size="3.3">{ad}</text>')
        if t < 0:
            o.append(f'<rect x="{X(t):.1f}" y="{y - 1.6:.1f}" width="{-t * xs:.1f}" height="3.6" fill="{renk}" opacity=".85"/>')
        else:
            o.append(f'<rect x="{X(0):.1f}" y="{y - 1.6:.1f}" width="{max(t * xs, .5):.1f}" height="3.6" fill="{renk}" opacity=".85"/>')
        etk = f'{t:g}'.replace('.', ',')
        o.append(f'<text x="{X(max(t, 0)) + 1.2:.1f}" y="{y + 1.3:.1f}" fill="{M}" font-size="3.1" font-weight="700">{etk}</text>')
        y += 4.6
    y += 1.6
o.append('</g></svg>')
w('erime', ''.join(o))

# ------------------------------------------------------------------
# 9) Katı türünü tanıma akış şeması
# ------------------------------------------------------------------
o = ['<svg viewBox="0 0 120 100" class="grafik"><g font-family="Inter" text-anchor="middle">', '<defs>' + ok_marker('ak', '#64748b') + '</defs>']


def soru(x, y, t1, t2):
    s = f'<rect x="{x - 31}" y="{y - 6.5}" width="62" height="13" rx="2.5" fill="#fff" stroke="{U}" stroke-width=".5"/>'
    s += f'<text x="{x}" y="{y - 1}" font-size="3.5" font-weight="700" fill="{UK}">{t1}</text><text x="{x}" y="{y + 3.6}" font-size="3.5" font-weight="700" fill="{UK}">{t2}</text>'
    return s


def sonuc(x, y, w_, t, renk, alt=None):
    s = f'<rect x="{x - w_ / 2}" y="{y - 6}" width="{w_}" height="12" rx="6" fill="{renk}"/>'
    if alt:
        s += f'<text x="{x}" y="{y - .4}" font-size="3.6" font-weight="800" fill="#fff">{t}</text><text x="{x}" y="{y + 3.6}" font-size="3.1" fill="#fff">{alt}</text>'
    else:
        s += f'<text x="{x}" y="{y + 1.3}" font-size="3.8" font-weight="800" fill="#fff">{t}</text>'
    return s


def ok_(x1, y1, x2, y2, et=None, ex=0, ey=0, anc='middle'):
    s = f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#64748b" stroke-width=".55" fill="none" marker-end="url(#ak)"/>'
    if et:
        s += f'<text x="{(x1 + x2) / 2 + ex}" y="{(y1 + y2) / 2 + ey}" font-size="2.9" font-weight="800" fill="{S}" text-anchor="{anc}">{et}</text>'
    return s


xq, xr = 33, 97
satir = [(9, 'Belirli bir erime', 'noktası var mı?', 'HAYIR', 'AMORF KATI', '#c26a06', 'cam, mum, plastik'),
         (32, 'Katı hâlde elektrik', 'akımını iletir mi?', 'EVET', 'METALİK', '#c26a06', 'parlak, işlenebilir'),
         (55, 'Eriyiği ya da sulu', 'çözeltisi iletir mi?', 'EVET', 'İYONİK', KAT, 'sert ama kırılgan'),
         (78, 'Erime noktası çok', 'yüksek mi? (≳1000 °C)', 'EVET', 'KOVALENT AĞ', TEAL, 'elmas, kuvars, SiC')]
devam = ['EVET', 'HAYIR', 'HAYIR', 'HAYIR']
for i, (y, t1, t2, et, ad, renk, alt) in enumerate(satir):
    o.append(soru(xq, y, t1, t2))
    o.append(ok_(64, y, 74, y, et, 0, -1.6))
    o.append(sonuc(xr, y, 44, ad, renk, alt))
    yalt = 78 + 6.5 if i == 3 else y + 6.5
    if i < 3:
        o.append(ok_(xq, y + 6.5, xq, y + 16.3, devam[i], 2, 1, 'start'))
o.append(ok_(xq, 84.5, xq, 88.7, None))
o.append(sonuc(xq, 94, 56, 'MOLEKÜLER KATI', U, 'buz, iyot, kuru buz, şeker'))
o.append(f'<text x="{xq + 2}" y="87.8" font-size="2.9" font-weight="800" fill="{S}" text-anchor="start">HAYIR</text>')
o.append('</g></svg>')
w('akis', ''.join(o))

# ------------------------------------------------------------------
# 10) Bağlam sorusu: fırın malzemesi grafiği
# ------------------------------------------------------------------
mal = [('Alüminyum', 660, 'm'), ('NaCl', 801, 'i'), ('Bakır', 1085, 'm'), ('CaF₂', 1418, 'i'),
       ('Demir', 1538, 'm'), ('Al₂O₃', 2072, 'i'), ('MgO', 2852, 'i'), ('Tungsten', 3422, 'm')]
x0, x1 = 26, 112
Y0, Y1 = 64, 6
Yt = lambda t: Y0 - t * (Y0 - Y1) / 3600
o = [f'<svg viewBox="0 0 116 80" class="grafik"><g font-family="Inter" font-size="3.4" fill="{S}">']
for t in range(0, 3601, 600):
    o.append(f'<line x1="{x0}" y1="{Yt(t):.1f}" x2="{x1}" y2="{Yt(t):.1f}" stroke="#e5e7f0" stroke-width=".3"/>')
    o.append(f'<text x="{x0 - 1.5}" y="{Yt(t) + 1.2:.1f}" text-anchor="end">{t}</text>')
o.append(f'<line x1="{x0}" y1="{Yt(1800):.1f}" x2="{x1}" y2="{Yt(1800):.1f}" stroke="{ROSE}" stroke-width=".55" stroke-dasharray="1.6 1"/>')
o.append(f'<text x="{x0 + 1}" y="{Yt(1800) - 1.2:.1f}" fill="{ROSE}" font-weight="700" font-size="3.2">fırın sıcaklığı 1800 °C</text>')
bw = (x1 - x0) / len(mal)
for i, (ad, t, tur) in enumerate(mal):
    x = x0 + i * bw + 1.6
    renk = '#c26a06' if tur == 'm' else KAT
    o.append(f'<rect x="{x:.1f}" y="{Yt(t):.1f}" width="{bw - 3.2:.1f}" height="{Y0 - Yt(t):.1f}" fill="{renk}" opacity=".85"/>')
    o.append(f'<text x="{x + (bw - 3.2) / 2:.1f}" y="{Yt(t) - 1:.1f}" text-anchor="middle" fill="{M}" font-size="2.9" font-weight="700">{t}</text>')
    o.append(f'<text transform="translate({x + (bw - 3.2) / 2 + 1.1:.1f},{Y0 + 2.2}) rotate(-40)" text-anchor="end" fill="{M}" font-size="3.1">{ad}</text>')
o.append(f'<line x1="{x0}" y1="{Y0}" x2="{x1}" y2="{Y0}" stroke="{M}" stroke-width=".45"/><line x1="{x0}" y1="{Y0}" x2="{x0}" y2="{Y1 - 2}" stroke="{M}" stroke-width=".45"/>')
o.append(f'<text x="2" y="3.4" fill="{M}" font-weight="700">Erime noktası (°C)</text>')
o.append(f'<rect x="70" y="0.6" width="3" height="3" fill="#c26a06"/><text x="74.5" y="3.2" font-size="3">metal</text>')
o.append(f'<rect x="88" y="0.6" width="3" height="3" fill="{KAT}"/><text x="92.5" y="3.2" font-size="3">iyonik</text>')
o.append('</g></svg>')
w('firin', ''.join(o))

print('Tamam:', sorted(os.listdir(D)))
