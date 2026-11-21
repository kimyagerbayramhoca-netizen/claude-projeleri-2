"""Hacimli (3B görünümlü) molekül çizimi: radyal gradyanlı küreler, parlama, yer gölgesi,
silindir bağlar (tekli/ikili), yarı bağ tekniği (her bağın yarısı kendi atomunun renginde).

Kullanım:
    molekul_svg("h2o", "H2O", donus=(10, -25, 0), en=40)      # hazır geometri
    cekirdek_svg("c14", p=6, n=8)                              # izotop çekirdeği
    kristal_nacl("tuz")                                         # NaCl kristal küpü

Derinlik sıralaması: atomlar uzaktan yakına çizilir; her atomdan hemen önce onun yarı bağları.
"""
import math
from .temel import Svg, f, karis, acik, koyu
from .renkler import ATOM, ATOM_R, OBS

# ------------------------------------------------------------------ geometriler (Å, yaklaşık)

def _tetra(merkez, uz, yon=1):
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    k = uz / math.sqrt(3)
    return [(merkez[0] + a * k * yon, merkez[1] + b * k, merkez[2] + c * k) for a, b, c in v]


def _geometri(ad):
    A, B = [], []
    if ad == "H2O":
        A = [("O", (0, 0, 0)), ("H", (-.757, -.587, 0)), ("H", (.757, -.587, 0))]
        B = [(0, 1, 1), (0, 2, 1)]
    elif ad == "CO2":
        A = [("C", (0, 0, 0)), ("O", (-1.16, 0, 0)), ("O", (1.16, 0, 0))]
        B = [(0, 1, 2), (0, 2, 2)]
    elif ad == "O2":
        A = [("O", (-.62, 0, 0)), ("O", (.62, 0, 0))]
        B = [(0, 1, 2)]
    elif ad == "N2":
        A = [("N", (-.56, 0, 0)), ("N", (.56, 0, 0))]
        B = [(0, 1, 3)]
    elif ad == "CO":
        A = [("C", (-.57, 0, 0)), ("O", (.57, 0, 0))]
        B = [(0, 1, 3)]
    elif ad == "SO2":
        A = [("S", (0, .2, 0)), ("O", (-1.232, -.53, 0)), ("O", (1.232, -.53, 0))]
        B = [(0, 1, 2), (0, 2, 2)]
    elif ad == "SO3":
        A = [("S", (0, 0, 0))] + [("O", (1.42 * math.cos(a), 1.42 * math.sin(a), 0)) for a in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3, math.pi / 2 + 4 * math.pi / 3)]
        B = [(0, 1, 2), (0, 2, 2), (0, 3, 2)]
    elif ad == "NH3":
        A = [("N", (0, .38, 0))] + [("H", (.94 * math.cos(a), 0, .94 * math.sin(a))) for a in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3, math.pi / 2 + 4 * math.pi / 3)]
        B = [(0, 1, 1), (0, 2, 1), (0, 3, 1)]
    elif ad == "CH4":
        A = [("C", (0, 0, 0))] + [("H", p) for p in _tetra((0, 0, 0), 1.09)]
        B = [(0, i, 1) for i in range(1, 5)]
    elif ad == "C2H6":
        c1, c2 = (-.77, 0, 0), (.77, 0, 0)
        A = [("C", c1), ("C", c2)]
        for i in range(3):
            a = 2 * math.pi * i / 3
            A.append(("H", (c1[0] - .36, 1.03 * math.cos(a), 1.03 * math.sin(a))))
            A.append(("H", (c2[0] + .36, 1.03 * math.cos(a + math.pi / 3), 1.03 * math.sin(a + math.pi / 3))))
        B = [(0, 1, 1)] + [(0, 2 + 2 * i, 1) for i in range(3)] + [(1, 3 + 2 * i, 1) for i in range(3)]
    elif ad == "C2H4":
        A = [("C", (-.67, 0, 0)), ("C", (.67, 0, 0)), ("H", (-1.24, .93, 0)), ("H", (-1.24, -.93, 0)), ("H", (1.24, .93, 0)), ("H", (1.24, -.93, 0))]
        B = [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)]
    elif ad == "C3H8":
        cs = [(-1.27, -.42, 0), (0, .42, 0), (1.27, -.42, 0)]
        A = [("C", c) for c in cs]
        hs = [(-1.27, -1.1, .85), (-1.27, -1.1, -.85), (-2.15, .2, 0), (0, 1.1, .85), (0, 1.1, -.85),
              (1.27, -1.1, .85), (1.27, -1.1, -.85), (2.15, .2, 0)]
        A += [("H", h) for h in hs]
        B = [(0, 1, 1), (1, 2, 1), (0, 3, 1), (0, 4, 1), (0, 5, 1), (1, 6, 1), (1, 7, 1), (2, 8, 1), (2, 9, 1), (2, 10, 1)]
    elif ad == "He":
        A = [("He", (0, 0, 0))]
    elif ad == "C6H12O6":
        # β-glukopiranoz, sandalye biçimi (basitleştirilmiş). Halka: C1..C5 + O5
        hal = []
        for i in range(6):
            a = math.pi / 6 + i * math.pi / 3
            hal.append((1.45 * math.cos(a), .26 * (1 if i % 2 else -1), 1.45 * math.sin(a)))
        ad_hal = ["C", "C", "C", "C", "C", "O"]   # C1 C2 C3 C4 C5 O5
        A = [(e, p) for e, p in zip(ad_hal, hal)]
        B = [(i, (i + 1) % 6, 1) for i in range(6)]

        def disa(p, ek, dz):
            r = math.hypot(p[0], p[2])
            return (p[0] + p[0] / r * ek, p[1] + dz, p[2] + p[2] / r * ek)
        # ekvatoryal OH (C1..C4), C5 üzerinde CH2OH; eksenel H'ler
        for i in range(4):
            p = hal[i]
            yon = 1 if i % 2 else -1
            o = disa(p, 1.25, -.35 * yon)
            A.append(("O", o)); oi = len(A) - 1; B.append((i, oi, 1))
            A.append(("H", disa(o, .75, .25 * (1 if yon < 0 else -1)))); B.append((oi, len(A) - 1, 1))
            A.append(("H", (p[0], p[1] + 1.05 * yon, p[2]))); B.append((i, len(A) - 1, 1))
        p = hal[4]
        c6 = disa(p, 1.35, .35)
        A.append(("C", c6)); ci = len(A) - 1; B.append((4, ci, 1))
        A.append(("H", (p[0], p[1] - 1.05, p[2]))); B.append((4, len(A) - 1, 1))
        o6 = (c6[0] + .7, c6[1] + 1.0, c6[2] + .3)
        A.append(("O", o6)); oi = len(A) - 1; B.append((ci, oi, 1))
        A.append(("H", (o6[0] + .85, o6[1] + .2, o6[2]))); B.append((oi, len(A) - 1, 1))
        A.append(("H", (c6[0] + .2, c6[1] - .55, c6[2] + .9))); B.append((ci, len(A) - 1, 1))
        A.append(("H", (c6[0] + .55, c6[1] - .6, c6[2] - .75))); B.append((ci, len(A) - 1, 1))
    elif ad == "Na2CO3":
        A = [("C", (0, 0, 0))] + [("O", (1.29 * math.cos(a), 1.29 * math.sin(a), 0)) for a in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3, math.pi / 2 + 4 * math.pi / 3)]
        B = [(0, 1, 2), (0, 2, 1), (0, 3, 1)]
        A += [("Na", (-2.75, -1.55, .6)), ("Na", (2.75, -1.55, -.6))]
    elif ad == "NaCl":
        A = [("Na", (-1.4, 0, 0)), ("Cl", (1.4, 0, 0))]
    elif ad == "CaCO3":
        A = [("C", (0, 0, 0))] + [("O", (1.29 * math.cos(a), 1.29 * math.sin(a), 0)) for a in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3, math.pi / 2 + 4 * math.pi / 3)]
        B = [(0, 1, 2), (0, 2, 1), (0, 3, 1)]
        A += [("Ca", (0, -2.9, .2))]
    else:
        raise ValueError(ad)
    return A, B


# ------------------------------------------------------------------ dönüş ve çizim

def _dondur(p, rx, ry, rz):
    x, y, z = p
    a, b, c = math.radians(rx), math.radians(ry), math.radians(rz)
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    x, z = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
    x, y = x * math.cos(c) - y * math.sin(c), x * math.sin(c) + y * math.cos(c)
    return x, y, z


def _kure_gradyan(s, c, ad):
    if c.upper() in ("#F3F5F8", "#FFFFFF"):
        st = [(0, "#FFFFFF"), (.35, "#F4F7FA"), (.72, "#C9D3DE"), (1, "#7D8B9C")]
    else:
        st = [(0, acik(c, .72)), (.28, acik(c, .25)), (.66, c), (1, koyu(c, .5))]
    return s.rad(st, cx=.5, cy=.5, r=.56, fx=.34, fy=.3, ad=ad)


def _silindir_gradyan(s, c, ad):
    if c.upper() in ("#F3F5F8", "#FFFFFF"):
        st = [(0, "#8592A3"), (.32, "#FFFFFF"), (.55, "#E6EBF0"), (1, "#7D8B9C")]
    else:
        st = [(0, koyu(c, .45)), (.3, acik(c, .45)), (.55, acik(c, .1)), (1, koyu(c, .5))]
    return s.lin(st, 0, 0, 0, 1, ad=ad)


def molekul_ciz(s, atomlar, baglar, donus=(0, 0, 0), olcek=40, merkez=(0, 0), bag_k=.17, etiket=False,
                yer_golgesi=True, cizgi=True, iyon=None, yariçap=None, parlak=True):
    """atomlar: [(element, (x,y,z))]; baglar: [(i, j, derece)]. SVG metni + sınır kutusu döndürür."""
    P = [(_dondur(p, *donus), e) for e, p in atomlar]
    yc = yariçap or ATOM_R
    pts = []
    for (x, y, z), e in P:
        pts.append((merkez[0] + x * olcek, merkez[1] - y * olcek, z, e, yc[e] * olcek))
    grad, sgrad = {}, {}
    for _, _, _, e, _ in pts:
        c = ATOM[e]
        if e not in grad:
            grad[e] = _kure_gradyan(s, c, "ak")
            sgrad[e] = _silindir_gradyan(s, c, "ab")
    komsu = {i: [] for i in range(len(pts))}
    for i, j, d in baglar:
        komsu[i].append((j, d))
        komsu[j].append((i, d))
    out = []
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    rs = [p[4] for p in pts]
    sol, sag = min(x - r for x, r in zip(xs, rs)), max(x + r for x, r in zip(xs, rs))
    ust, alt = min(y - r for y, r in zip(ys, rs)), max(y + r for y, r in zip(ys, rs))
    if yer_golgesi:
        gg = s.rad([(0, "#0E2A3A", .32), (.6, "#0E2A3A", .12), (1, "#0E2A3A", 0)], ad="yg")
        gw = (sag - sol) * .55 + olcek * .4
        out.append(f'<ellipse cx="{f((sol + sag) / 2)}" cy="{f(alt + olcek * .18)}" rx="{f(gw)}" ry="{f(olcek * .22 + gw * .08)}" fill="{gg}"/>')
    sira = sorted(range(len(pts)), key=lambda i: pts[i][2])
    bk = bag_k * olcek
    for i in sira:
        x, y, z, e, r = pts[i]
        c = ATOM[e]
        for j, d in komsu[i]:
            x2, y2 = pts[j][0], pts[j][1]
            mx, my = (x + x2) / 2, (y + y2) / 2
            L = math.hypot(mx - x, my - y)
            if L < .5:
                continue
            aci = math.degrees(math.atan2(my - y, mx - x))
            offs = [0] if d == 1 else ([-.62, .62] if d == 2 else [-1.05, 0, 1.05])
            kal = bk if d == 1 else bk * (.72 if d == 2 else .58)
            for o in offs:
                out.append(f'<g transform="translate({f(x)} {f(y)}) rotate({f(aci, 2)})">'
                           f'<rect x="0" y="{f(o * kal * 1.25 - kal / 2, 2)}" width="{f(L + kal * .2)}" height="{f(kal, 2)}" '
                           f'fill="{sgrad[e]}"' + (f' stroke="{koyu(c, .55)}" stroke-width="{f(olcek * .018, 2)}"' if cizgi else "") + "/></g>")
        st = f' stroke="{koyu(c, .6) if c != ATOM["H"] else "#5E6B7A"}" stroke-width="{f(max(.4, r * .045), 2)}"' if cizgi else ""
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{grad[e]}"{st}/>')
        if parlak:
            out.append(f'<ellipse cx="{f(x - r * .36)}" cy="{f(y - r * .42)}" rx="{f(r * .26)}" ry="{f(r * .16)}" fill="#FFFFFF" opacity=".85" transform="rotate(-35 {f(x - r * .36)} {f(y - r * .42)})"/>')
            out.append(f'<path d="M{f(x + r * .55)} {f(y + r * .45)} A{f(r * .75)} {f(r * .75)} 0 0 1 {f(x - r * .2)} {f(y + r * .72)}" stroke="#FFFFFF" stroke-width="{f(r * .08)}" fill="none" opacity=".35" stroke-linecap="round"/>')
        if etiket and (e != "H" or etiket == "hepsi"):
            fs = r * (.95 if len(e) == 1 else .78)
            renk = "#FFFFFF" if e not in ("H", "S", "He", "B", "Ca", "Mg") else OBS
            out.append(f'<text x="{f(x)}" y="{f(y + fs * .36)}" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="{f(fs)}" fill="{renk}">{e}</text>')
    return "".join(out), (sol, ust, sag, alt + (olcek * .45 if yer_golgesi else 0))


def molekul_svg(onek, ad, donus=(0, 0, 0), en=None, yuk=None, etiket=False, pay=4, cls="mol", yer_golgesi=True,
                olcek=40, iyon_etiket=False):
    s = Svg(onek)
    A, B = _geometri(ad)
    govde, (x0, y0, x1, y1) = molekul_ciz(s, A, B, donus, olcek, etiket=etiket, yer_golgesi=yer_golgesi)
    s += govde
    if iyon_etiket and ad == "Na2CO3":
        # iyon yükleri
        P = [(_dondur(p, *donus), e) for e, p in A]
        for (x, y, z), e in P:
            if e == "Na":
                X, Y = x * olcek + ATOM_R["Na"] * olcek * .7, -y * olcek - ATOM_R["Na"] * olcek * .75
                s += f'<circle cx="{f(X)}" cy="{f(Y)}" r="{f(olcek * .2)}" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.2"/><path d="M{f(X - olcek * .11)} {f(Y)} h{f(olcek * .22)} M{f(X)} {f(Y - olcek * .11)} v{f(olcek * .22)}" stroke="{OBS}" stroke-width="2"/>'
        s += (f'<path d="M{f(-1.95 * olcek)} {f(-1.95 * olcek)} q-8 0 -8 10 v{f(3.2 * olcek)} q0 10 8 10" fill="none" stroke="{OBS}" stroke-width="2" opacity=".55"/>'
              f'<path d="M{f(1.95 * olcek)} {f(-1.95 * olcek)} q8 0 8 10 v{f(3.2 * olcek)} q0 10 -8 10" fill="none" stroke="{OBS}" stroke-width="2" opacity=".55"/>'
              f'<text x="{f(1.95 * olcek + 12)}" y="{f(-1.7 * olcek)}" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="{f(olcek * .42)}" fill="{OBS}">2−</text>')
        x0, x1 = min(x0, -2.3 * olcek), max(x1, 2.4 * olcek + 30)
        y0 = min(y0, -2.1 * olcek)
    vb = f"{f(x0 - pay)} {f(y0 - pay)} {f(x1 - x0 + 2 * pay)} {f(y1 - y0 + 2 * pay)}"
    w = f' width="{en}"' if en else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" class="{cls}"{w}>{s.govde()}</svg>'


# ------------------------------------------------------------------ izotop çekirdeği

def cekirdek_ciz(s, cx, cy, R, p, n, tohum=1, proton="#E2533D", notron="#9AA8B6", etiket_p=False):
    """p proton + n nötron: Fibonacci küresi üzerinde sıkı küme; uzaktan yakına sıralı."""
    import random
    r = random.Random(tohum)
    N = p + n
    tur = ["p"] * p + ["n"] * n
    r.shuffle(tur)
    altin = math.pi * (3 - math.sqrt(5))
    pts = []
    for i in range(N):
        yy = 1 - 2 * (i + .5) / N
        rad = math.sqrt(max(0, 1 - yy * yy))
        a = altin * i
        k = (.35 + .65 * ((i % 3) / 2)) if N > 4 else .6
        pts.append((math.cos(a) * rad * k, yy * k, math.sin(a) * rad * k, tur[i]))
    kr = R / (N ** (1 / 3) * .95 + .6)
    gp = _kure_gradyan(s, proton, "pp")
    gn = _kure_gradyan(s, notron, "nn")
    out = []
    for x, y, z, t in sorted(pts, key=lambda q: q[2]):
        X, Y = cx + x * (R - kr), cy + y * (R - kr)
        out.append(f'<circle cx="{f(X)}" cy="{f(Y)}" r="{f(kr)}" fill="{gp if t == "p" else gn}" stroke="{koyu(proton if t == "p" else notron, .55)}" stroke-width="{f(kr * .06, 2)}"/>'
                   f'<ellipse cx="{f(X - kr * .35)}" cy="{f(Y - kr * .4)}" rx="{f(kr * .25)}" ry="{f(kr * .15)}" fill="#FFF" opacity=".75" transform="rotate(-35 {f(X - kr * .35)} {f(Y - kr * .4)})"/>')
    return "".join(out)


def kristal_nacl(onek, n=3, en=None, donus=(-24, 32, 0), olcek=34):
    """NaCl (kaya tuzu) kristali: n×n×n küçük küp, Na⁺ küçük mor, Cl⁻ büyük yeşil."""
    s = Svg(onek)
    A = []
    h = (n - 1) / 2
    for i in range(n):
        for j in range(n):
            for k in range(n):
                e = "Na" if (i + j + k) % 2 == 0 else "Cl"
                A.append((e, ((i - h) * 1.25, (j - h) * 1.25, (k - h) * 1.25)))
    B = []
    idx = {}
    for t, (e, p) in enumerate(A):
        idx[(round(p[0], 2), round(p[1], 2), round(p[2], 2))] = t
    for t, (e, p) in enumerate(A):
        for d in ((1.25, 0, 0), (0, 1.25, 0), (0, 0, 1.25)):
            q = (round(p[0] + d[0], 2), round(p[1] + d[1], 2), round(p[2] + d[2], 2))
            if q in idx:
                B.append((t, idx[q], 1))
    yc = dict(ATOM_R)
    yc["Na"], yc["Cl"] = .36, .55
    govde, (x0, y0, x1, y1) = molekul_ciz(s, A, B, donus, olcek, bag_k=.07, yariçap=yc)
    s += govde
    vb = f"{f(x0 - 4)} {f(y0 - 4)} {f(x1 - x0 + 8)} {f(y1 - y0 + 8)}"
    w = f' width="{en}"' if en else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" class="mol"{w}>{s.govde()}</svg>'
