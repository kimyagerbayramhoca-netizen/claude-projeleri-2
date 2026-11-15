"""Manzara parçaları: gökyüzü, güneş, bulut, dağ (gölgeli + karlı), göl (yansıma + parıltı),
ağaçlar (kavak, ceviz), çimen, kaya, martı, inci kefali, tekne, feribot, köy evleri.

Her fonksiyon SVG metni DÖNDÜRÜR (eklemez); gradyanları verilen `Svg` nesnesinin defs'ine yazar.
Böylece aynı parça hem asıl sahnede hem de göldeki yansımada (ters çevrilmiş grupta) kullanılabilir.
Işık yönü `isik`: -1 = güneş solda (sağ yamaçlar gölgede), +1 = güneş sağda.
"""
import math
from .temel import (f, nok, cizgi_d, egri_d, karis, acik, koyu, orta_nokta, deger_gurultusu,
                    daire_noktalari, rng as RNG)

# ------------------------------------------------------------------ gökyüzü temaları
GOK = {
    "safak": [(0, "#4D63B0"), (.38, "#9C8FD0"), (.62, "#F6A9B9"), (.84, "#FFD2A8"), (1, "#FFF0D9")],
    "gun": [(0, "#3D9FE0"), (.55, "#8FD3F0"), (1, "#E3F6FB")],
    "altin": [(0, "#4C9AD6"), (.45, "#A9D4EC"), (.75, "#FBE3B0"), (1, "#FFD99A")],
    "gunbatimi": [(0, "#26245E"), (.22, "#5B3A86"), (.45, "#C9467F"), (.64, "#FF6F6A"), (.82, "#FF9A45"), (1, "#FFD27A")],
    "alaca": [(0, "#141A45"), (.45, "#43346F"), (.78, "#C25E83"), (1, "#FFA978")],
    "gece": [(0, "#070B26"), (.55, "#15224F"), (1, "#2C4A85")],
}


def gokyuzu(s, x, y, w, h, tema="gun", duraklar=None):
    g = s.lin(duraklar or GOK[tema], 0, y, 0, y + h, kull="userSpaceOnUse", ad="gok")
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{g}"/>'


def gunes(s, x, y, r, cekirdek="#FFF7DC", hale="#FFD27A", hale_r=None, guc=.85):
    hr = hale_r or r * 7
    gl = s.rad([(0, hale, guc), (.12, hale, guc * .7), (.35, hale, guc * .28), (.7, hale, guc * .07), (1, hale, 0)],
               x, y, hr, kull="userSpaceOnUse", ad="hale")
    dk = s.rad([(0, "#FFFFFF"), (.55, cekirdek), (1, hale)], x - r * .25, y - r * .25, r * 1.2, kull="userSpaceOnUse", ad="gd")
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(hr)}" fill="{gl}"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{dk}"/>')


def ay(s, x, y, r, renk="#FFF4D6", golge_renk="#15224F"):
    """Hilal ay (gece sahneleri)."""
    gl = s.rad([(0, renk, .45), (.4, renk, .12), (1, renk, 0)], x, y, r * 5, kull="userSpaceOnUse", ad="ayh")
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * 5)}" fill="{gl}"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{renk}"/>'
            f'<circle cx="{f(x + r * .42)}" cy="{f(y - r * .22)}" r="{f(r * .86)}" fill="{golge_renk}"/>')


def yildizlar(s, x, y, w, h, n, tohum, renk="#FFFFFF"):
    r = RNG(tohum)
    out = []
    for _ in range(n):
        px, py = x + r.random() * w, y + (r.random() ** 1.6) * h
        rr = r.choice([1.2, 1.6, 2.2, 3.0])
        op = r.uniform(.45, 1)
        if rr > 2.5:
            out.append(f'<path d="M{f(px)} {f(py - rr * 2.4)} L{f(px + rr * .5)} {f(py - rr * .5)} L{f(px + rr * 2.4)} {f(py)} '
                       f'L{f(px + rr * .5)} {f(py + rr * .5)} L{f(px)} {f(py + rr * 2.4)} L{f(px - rr * .5)} {f(py + rr * .5)} '
                       f'L{f(px - rr * 2.4)} {f(py)} L{f(px - rr * .5)} {f(py - rr * .5)} Z" fill="{renk}" opacity="{f(op, 2)}"/>')
        else:
            out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(rr)}" fill="{renk}" opacity="{f(op, 2)}"/>')
    return "".join(out)


def bulut(s, x, y, en, tohum, ust="#FFFFFF", alt="#CFDDEE", n=None, yukseklik=None, op=1.0, isik=-1):
    """Kümülüs bulut: iki sıra kabarık daire + taç; düz ama hafif kavisli taban; ışık tarafında parlak kenar."""
    r = RNG(tohum)
    yk = yukseklik or en * .36
    nb = n or max(4, int(en / 46))
    pf = []
    for i in range(nb):
        t = (i + .5) / nb
        rr = en / nb * .78 * r.uniform(.85, 1.2)
        pf.append((x + en * t + r.uniform(-6, 6), y - rr * .5, rr))
    nt = max(2, nb // 2)
    for i in range(nt):
        t = (i + .5) / nt
        rr = en / nt * .4 * r.uniform(.9, 1.25)
        pf.append((x + en * (.18 + .64 * t) + r.uniform(-8, 8), y - yk * .5 - rr * .2, rr))
    pf.append((x + en * r.uniform(.38, .62), y - yk * .78, en * r.uniform(.15, .2)))
    g = s.lin([(0, ust), (.6, karis(ust, alt, .3)), (1, alt)], 0, y - yk * 1.25, 0, y, kull="userSpaceOnUse", ad="bl")
    kl = s.klip(f'<path d="M{f(x - en)} {f(y - yk * 4)} H{f(x + en * 2)} V{f(y - 2)} Q{f(x + en / 2)} {f(y + 6)} {f(x - en)} {f(y - 2)} Z"/>', ad="blk")
    govde = "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="{f(c)}"/>' for a, b, c in pf)
    isk = "".join(f'<circle cx="{f(a + c * .22 * isik)}" cy="{f(b - c * .24)}" r="{f(c * .7)}"/>' for a, b, c in pf[nb:])
    tab = s.lin([(0, alt, 0), (1, koyu(alt, .12), .55)], 0, y - yk * .3, 0, y, kull="userSpaceOnUse", ad="blt")
    return (f'<g clip-path="{kl}" opacity="{f(op, 2)}"><g fill="{g}">{govde}</g>'
            f'<g fill="#FFFFFF" opacity=".5">{isk}</g>'
            f'<rect x="{f(x - en * .1)}" y="{f(y - yk * .3)}" width="{f(en * 1.2)}" height="{f(yk * .3 + 6)}" fill="{tab}"/></g>')


def bulut_serit(s, x, y, uz, kal, ust, alt, op=.85):
    """Gün batımında uzun ince (stratus) bulut: alt kenarı güneşle aydınlanmış mercek biçimi."""
    g = s.lin([(0, ust), (1, alt)], 0, y - kal, 0, y + kal * .4, kull="userSpaceOnUse", ad="bs")
    d = (f"M{f(x)} {f(y)} C{f(x + uz * .2)} {f(y - kal)} {f(x + uz * .6)} {f(y - kal * 1.1)} {f(x + uz)} {f(y - kal * .1)} "
         f"C{f(x + uz * .7)} {f(y + kal * .45)} {f(x + uz * .3)} {f(y + kal * .4)} {f(x)} {f(y)} Z")
    return f'<path d="{d}" fill="{g}" opacity="{f(op, 2)}"/>'


# ------------------------------------------------------------------ dağ

def _profil(bicim, sol, sag, taban, tx, ty, r, puruz):
    H = taban - ty
    pts = []
    if bicim in ("volkan", "kaldera", "tepe"):
        n = max(24, int((sag - sol) / 8))
        gur = deger_gurultusu(n + 1, 6, r)
        gur2 = deger_gurultusu(n + 1, 2.2, r)
        for i in range(n + 1):
            x = sol + (sag - sol) * i / n
            L = (tx - sol) if x < tx else (sag - tx)
            u = abs(x - tx) / max(L, 1)
            if bicim == "volkan":
                e = .08
                uu = (math.sqrt(u * u + e * e) - e) / (math.sqrt(1 + e * e) - e)
                h = H * (1 - min(uu, 1)) ** 1.75
            elif bicim == "kaldera":
                h = H * min(1, 1.18 * (1 - min(u, 1)) ** 1.25)
                if u < .2:
                    h -= H * .05 * math.cos(u / .2 * math.pi / 2)  # kaldera çanağı: tepede hafif çökme
            else:
                h = H * (.5 + .5 * math.cos(math.pi * min(u, 1)))
            kenar = min(1.0, (1 - min(u, 1)) * 4)  # tabanda gürültü sönsün
            h += (gur[i] * puruz + gur2[i] * puruz * .35) * kenar
            pts.append((x, taban - max(h, 0)))
    else:  # sivri: kontrol noktaları + orta nokta yer değiştirme
        k = [(sol, taban),
             (sol + (tx - sol) * r.uniform(.35, .5), ty + H * r.uniform(.45, .6)),
             (sol + (tx - sol) * r.uniform(.7, .85), ty + H * r.uniform(.12, .25)),
             (tx, ty),
             (tx + (sag - tx) * r.uniform(.15, .3), ty + H * r.uniform(.12, .25)),
             (tx + (sag - tx) * r.uniform(.5, .65), ty + H * r.uniform(.45, .6)),
             (sag, taban)]
        for i in range(len(k) - 1):
            seg = orta_nokta(k[i], k[i + 1], 4, puruz * (abs(k[i + 1][0] - k[i][0]) / max(sag - sol, 1)) * 2.2, r)
            pts += seg[:-1] if i < len(k) - 2 else seg
        pts = pts[1:-1]
    return pts


def _kesisim(p, q, y):
    if q[1] == p[1]:
        return (p[0], y)
    t = (y - p[1]) / (q[1] - p[1])
    return (p[0] + (q[0] - p[0]) * t, y)


def dag(s, sol, sag, taban, tx, ty, tohum, renk="#7A8FB0", golge=None, isik=-1, bicim="sivri",
        puruz=None, kar_y=None, kar="#FFFFFF", kar_golge="#C7D3EA", sis=None, sis_op=.0,
        sirt=4, kenar_isik=None, cizgi=None, cizgi_k=2.2):
    """Gölgeli dağ. renk: aydınlık yamaç; golge: gölgeli yamaç; kar_y: kar çizgisi (y)."""
    r = RNG(tohum)
    H = taban - ty
    puruz = puruz if puruz is not None else H * .06
    golge = golge or koyu(renk, .3)
    sirt_pts = _profil(bicim, sol, sag, taban, tx, ty, r, puruz)
    tepe_i = min(range(len(sirt_pts)), key=lambda i: sirt_pts[i][1])
    tx2, ty2 = sirt_pts[tepe_i]
    poly = [(sol, taban)] + sirt_pts + [(sag, taban)]
    out = []
    gv = s.lin([(0, acik(renk, .08)), (1, karis(renk, sis, .5) if sis else koyu(renk, .08))], 0, ty, 0, taban, kull="userSpaceOnUse", ad="dg")
    out.append(f'<path d="{cizgi_d(poly, True)}" fill="{gv}"/>')
    # gölge yamacı
    if isik < 0:
        dis = sirt_pts[tepe_i:] + [(sag, taban)]
        ic_bas = (tx2 + (sag - tx2) * r.uniform(.04, .22), taban)
    else:
        dis = list(reversed(sirt_pts[:tepe_i + 1])) + [(sol, taban)]
        ic_bas = (tx2 - (tx2 - sol) * r.uniform(.04, .22), taban)
    ic = orta_nokta(ic_bas, (tx2, ty2), 4, H * .05, r)
    golge_poly = dis + ic[:-1]
    gg = s.lin([(0, golge), (1, karis(golge, sis, .45) if sis else golge)], 0, ty, 0, taban, kull="userSpaceOnUse", ad="dgg")
    golge_d = cizgi_d(golge_poly, True)
    out.append(f'<path d="{golge_d}" fill="{gg}"/>')
    # sırt çizgileri (oluk/yamaç dokusu)
    for k in range(sirt):
        if isik < 0:
            j = r.randint(max(1, int(tepe_i * .25)), max(2, tepe_i - 1))
        else:
            j = r.randint(min(len(sirt_pts) - 2, tepe_i + 1), min(len(sirt_pts) - 2, tepe_i + int((len(sirt_pts) - tepe_i) * .75)))
        p = sirt_pts[j]
        dx = (p[0] - tx2) * r.uniform(.25, .6)
        alt_n = (p[0] + dx, taban - (taban - p[1]) * r.uniform(.0, .35))
        hat = orta_nokta(p, alt_n, 3, H * .03, r)
        gen = H * r.uniform(.012, .03)
        hat2 = [(q[0] + gen * (1 - i / len(hat)) * (1 if isik < 0 else -1), q[1]) for i, q in enumerate(hat)]
        out.append(f'<path d="{cizgi_d(hat + list(reversed(hat2)), True)}" fill="{koyu(renk, .18)}" opacity=".45"/>')
    # kar örtüsü
    if kar_y is not None and ty2 < kar_y:
        i0 = tepe_i
        while i0 > 0 and sirt_pts[i0 - 1][1] < kar_y:
            i0 -= 1
        i1 = tepe_i
        while i1 < len(sirt_pts) - 1 and sirt_pts[i1 + 1][1] < kar_y:
            i1 += 1
        sol_k = _kesisim(sirt_pts[i0 - 1], sirt_pts[i0], kar_y) if i0 > 0 else sirt_pts[0]
        sag_k = _kesisim(sirt_pts[i1], sirt_pts[i1 + 1], kar_y) if i1 < len(sirt_pts) - 1 else sirt_pts[-1]
        ust = [sol_k] + sirt_pts[i0:i1 + 1] + [sag_k]
        # kar dili: aşağı uzanan kar parmakları
        alt = []
        n = max(6, int((sag_k[0] - sol_k[0]) / (H * .07 + 4)))
        for i in range(1, n):
            x = sag_k[0] - (sag_k[0] - sol_k[0]) * i / n
            yak = 1 - abs(x - tx2) / max(sag_k[0] - sol_k[0], 1)
            if i % 2:
                y = kar_y + (H * r.uniform(.04, .16) * (.4 + yak))
            else:
                y = kar_y + H * r.uniform(-.03, .03)
            alt.append((x + r.uniform(-3, 3), y))
        kar_poly = ust + alt
        kar_d = cizgi_d(kar_poly, True)
        kg = s.lin([(0, kar), (1, karis(kar, kar_golge, .35))], 0, ty, 0, kar_y + H * .2, kull="userSpaceOnUse", ad="kr")
        out.append(f'<path d="{kar_d}" fill="{kg}"/>')
        kl = s.klip(f'<path d="{kar_d}"/>', ad="krk")
        out.append(f'<path d="{golge_d}" fill="{kar_golge}" clip-path="{kl}"/>')
        # karın içinde ince gölge oluklar
        for k in range(3):
            j = r.randint(i0, i1)
            p = sirt_pts[j]
            q = (p[0] + (p[0] - tx2) * .3 + r.uniform(-6, 6), kar_y + H * r.uniform(.02, .12))
            out.append(f'<path d="M{nok(p)} Q{f((p[0] + q[0]) / 2 + r.uniform(-5, 5))} {f((p[1] + q[1]) / 2)} {nok(q)}" '
                       f'stroke="{kar_golge}" stroke-width="{f(max(1.2, H * .008))}" fill="none" stroke-linecap="round" opacity=".7" clip-path="{kl}"/>')
    if kenar_isik:
        yan = sirt_pts[:tepe_i + 1] if isik < 0 else sirt_pts[tepe_i:]
        out.append(f'<path d="{cizgi_d(yan)}" fill="none" stroke="{kenar_isik}" stroke-width="{f(max(1.5, H * .012))}" stroke-linejoin="round" opacity=".7"/>')
    if cizgi:
        out.append(f'<path d="{cizgi_d(sirt_pts)}" fill="none" stroke="{cizgi}" stroke-width="{f(cizgi_k)}" stroke-linejoin="round"/>')
    return "".join(out), sirt_pts


def tepe_bandi(s, x0, x1, y, genlik, tohum, renk, renk2=None, dalga=5, olcek=None):
    """Yumuşak tepe sırası (orta plan). Altı düz: y + büyük."""
    r = RNG(tohum)
    n = 60
    gur = deger_gurultusu(n + 1, n / dalga, r)
    pts = [(x0 + (x1 - x0) * i / n, y - genlik * (.5 + .5 * gur[i])) for i in range(n + 1)]
    alt = olcek or 2000
    g = s.lin([(0, renk), (1, renk2 or renk)], 0, y - genlik, 0, y + genlik, kull="userSpaceOnUse", ad="tb")
    d = egri_d(pts) + f" L{f(x1)} {f(y + alt)} L{f(x0)} {f(y + alt)} Z"
    return f'<path d="{d}" fill="{g}"/>', pts


# ------------------------------------------------------------------ göl

def gol(s, x, y, w, h, tohum, ufuk="#BFE9E6", orta="#2BB3B1", derin="#0E6A73", parilti=True,
        gunes_x=None, parilti_renk="#FFE6A6", cizgi_renk="#FFFFFF", yogunluk=1.0):
    r = RNG(tohum)
    g = s.lin([(0, ufuk), (.28, orta), (1, derin)], 0, y, 0, y + h, kull="userSpaceOnUse", ad="gol")
    out = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{g}"/>']
    if parilti:
        n = int(w / 18 * yogunluk)
        cz = []
        for _ in range(n):
            t = r.random() ** 1.4
            py = y + 3 + t * (h - 6)
            uz = (10 + 60 * t) * r.uniform(.5, 1.4)
            px = x + r.random() * w
            op = r.uniform(.18, .55) * (1 - .4 * t)
            k = .8 + 2.2 * t
            cz.append(f'<path d="M{f(px)} {f(py)} h{f(uz)}" stroke="{cizgi_renk}" stroke-width="{f(k)}" stroke-linecap="round" opacity="{f(op, 2)}"/>')
        out.append("".join(cz))
    if gunes_x is not None:
        sp = []
        for i in range(int(h / 5)):
            t = i / (h / 5)
            py = y + 2 + i * 5 + r.uniform(-1, 1)
            gen = (8 + 90 * t) * r.uniform(.35, 1.0)
            px = gunes_x + r.uniform(-1, 1) * (6 + 40 * t) - gen / 2
            op = r.uniform(.45, .95) * (1 - .55 * t)
            sp.append(f'<path d="M{f(px)} {f(py)} h{f(gen)}" stroke="{parilti_renk}" stroke-width="{f(1.2 + 2.2 * t)}" stroke-linecap="round" opacity="{f(op, 2)}"/>')
        out.append("".join(sp))
    return "".join(out)


def yansima(s, icerik, y_su, x, w, h, op=.35, renk_ort=None):
    """İçeriği su çizgisinde ters çevirip solarak yansıt. icerik: SVG metni (sahnedeki parçalar)."""
    m = s.lin([(0, "#FFFFFF", 1), (1, "#FFFFFF", 0)], 0, y_su, 0, y_su + h, kull="userSpaceOnUse", ad="ym")
    mk = s.maske(f'<rect x="{f(x)}" y="{f(y_su)}" width="{f(w)}" height="{f(h)}" fill="{m}"/>', ad="ymk")
    ust = f'<rect x="{f(x)}" y="{f(y_su)}" width="{f(w)}" height="{f(h)}" fill="{renk_ort}" opacity=".25"/>' if renk_ort else ""
    return (f'<g mask="{mk}" opacity="{f(op, 2)}"><g transform="translate(0 {f(2 * y_su)}) scale(1 -1)">{icerik}</g>{ust}</g>')


def dalga_cizgileri(x, y, w, h, tohum, renk="#FFFFFF", op=.6, n=10, k=1.6):
    r = RNG(tohum)
    out = []
    for _ in range(n):
        px = x + r.random() * w
        py = y + r.random() * h
        u = r.uniform(14, 34)
        out.append(f'<path d="M{f(px)} {f(py)} q{f(u / 4)} {f(-u / 6)} {f(u / 2)} 0 t{f(u / 2)} 0" stroke="{renk}" stroke-width="{f(k)}" fill="none" stroke-linecap="round" opacity="{f(op * r.uniform(.5, 1), 2)}"/>')
    return "".join(out)


# ------------------------------------------------------------------ bitki örtüsü

def kavak(s, x, y, h, w, tohum, renk="#5DA548", golge=None, isik=-1, gov="#6B5236", grad=None):
    r = RNG(tohum)
    golge = golge or koyu(renk, .35)
    n = 26
    sol, sag = [], []
    cy0, cy1 = y - h * .1, y - h
    for i in range(n + 1):
        v = i / n
        rr = w / 2 * (math.sin(math.pi * min(1, v * 1.05)) ** .75) * (1 - .35 * v) * r.uniform(.86, 1.1)
        py = cy0 + (cy1 - cy0) * v
        sol.append((x - rr, py))
        sag.append((x + rr, py))
    pts = sol + list(reversed(sag))
    if grad is None:
        a, b = (acik(renk, .18), golge) if isik < 0 else (golge, acik(renk, .18))
        grad = s.lin([(0, a), (.45, renk), (1, b)], 0, 0, 1, 0, ad="kv")
    out = [f'<path d="M{f(x - w * .05)} {f(y)} L{f(x - w * .02)} {f(y - h * .3)} L{f(x + w * .02)} {f(y - h * .3)} L{f(x + w * .05)} {f(y)} Z" fill="{gov}"/>',
           f'<path d="{egri_d(pts, True)}" fill="{grad}"/>']
    # yaprak kümeleri: gölge tarafında kısa yaylar
    for _ in range(int(h / 14)):
        v = r.uniform(.1, .9)
        py = cy0 + (cy1 - cy0) * v
        rr = w / 2 * (math.sin(math.pi * v) ** .75) * (1 - .35 * v)
        px = x + rr * r.uniform(-.1, .6) * (-isik)
        out.append(f'<path d="M{f(px - rr * .35)} {f(py)} q{f(rr * .35)} {f(rr * .3)} {f(rr * .7)} 0" fill="none" stroke="{golge}" stroke-width="{f(max(.8, w * .06))}" stroke-linecap="round" opacity=".55"/>')
    return "".join(out)


def agac(s, x, y, r0, tohum, renk="#6CB04F", golge=None, isik=-1, gov="#6B4A2E", meyve=None):
    """Yuvarlak taçlı ağaç (ceviz, elma, kayısı). (x, y) gövde tabanı."""
    r = RNG(tohum)
    golge = golge or koyu(renk, .32)
    cx, cy = x, y - r0 * 1.55
    out = [f'<path d="M{f(x - r0 * .12)} {f(y)} C{f(x - r0 * .1)} {f(y - r0 * .6)} {f(x - r0 * .05)} {f(cy)} {f(x - r0 * .3)} {f(cy - r0 * .3)} '
           f'L{f(x)} {f(cy)} L{f(x + r0 * .3)} {f(cy - r0 * .35)} C{f(x + r0 * .05)} {f(cy)} {f(x + r0 * .1)} {f(y - r0 * .6)} {f(x + r0 * .12)} {f(y)} Z" fill="{gov}"/>']
    g = s.lin([(0, acik(renk, .2)), (.55, renk), (1, golge)], cx - r0 * isik, cy - r0, cx + r0 * isik, cy + r0, kull="userSpaceOnUse", ad="ag")
    dl = []
    for i in range(r.randint(7, 10)):
        a = r.uniform(0, 2 * math.pi)
        d = r0 * r.uniform(.2, .55)
        dl.append((cx + math.cos(a) * d, cy + math.sin(a) * d * .8, r0 * r.uniform(.42, .62)))
    out.append("<g fill=\"" + g + "\">" + "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="{f(c)}"/>' for a, b, c in dl) + "</g>")
    # ışık lekeleri
    isk = "".join(f'<circle cx="{f(a + c * .3 * isik)}" cy="{f(b - c * .35)}" r="{f(c * .45)}"/>' for a, b, c in dl[:4])
    out.append(f'<g fill="{acik(renk, .35)}" opacity=".5">{isk}</g>')
    if meyve:
        for _ in range(6):
            a = r.uniform(0, 2 * math.pi)
            d = r0 * r.uniform(.2, .75)
            out.append(f'<circle cx="{f(cx + math.cos(a) * d)}" cy="{f(cy + math.sin(a) * d * .8)}" r="{f(r0 * .09)}" fill="{meyve}"/>')
    return "".join(out)


def cimen(x0, x1, y, tohum, renk="#4E8F3A", renk2="#7DBE55", yogun=1.0, boy=10, cicek=None):
    r = RNG(tohum)
    out = []
    n = int((x1 - x0) / 7 * yogun)
    for _ in range(n):
        px = r.uniform(x0, x1)
        b = boy * r.uniform(.5, 1.3)
        e = r.uniform(-.4, .4) * b
        c = r.choice([renk, renk2])
        out.append(f'<path d="M{f(px - 1.5)} {f(y)} Q{f(px + e * .3)} {f(y - b * .6)} {f(px + e)} {f(y - b)} Q{f(px + e * .2)} {f(y - b * .4)} {f(px + 1.5)} {f(y)} Z" fill="{c}"/>')
    if cicek:
        for _ in range(int(n / 6)):
            px = r.uniform(x0, x1)
            py = y - r.uniform(2, boy)
            out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r.uniform(1.4, 2.6))}" fill="{r.choice(cicek)}"/>')
    return "".join(out)


def sazlik(x0, x1, y, tohum, renk="#5C7F3A", bas="#7A4E2A", boy=40):
    r = RNG(tohum)
    out = []
    for _ in range(int((x1 - x0) / 5)):
        px = r.uniform(x0, x1)
        b = boy * r.uniform(.55, 1.2)
        e = r.uniform(-.15, .15) * b
        out.append(f'<path d="M{f(px)} {f(y)} Q{f(px + e * .2)} {f(y - b * .5)} {f(px + e)} {f(y - b)}" stroke="{renk}" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
        if r.random() < .35:
            out.append(f'<rect x="{f(px + e - 1.8)}" y="{f(y - b - 2)}" width="3.6" height="{f(b * .16)}" rx="1.8" fill="{bas}"/>')
    return "".join(out)


def kaya(s, x, y, w, h, tohum, renk="#6E6A72", isik=-1):
    r = RNG(tohum)
    pts = [(x - w / 2, y)]
    n = 7
    for i in range(1, n):
        t = i / n
        pts.append((x - w / 2 + w * t + r.uniform(-w * .05, w * .05), y - h * math.sin(math.pi * t) ** .6 * r.uniform(.75, 1.05)))
    pts.append((x + w / 2, y))
    tepe = min(pts, key=lambda p: p[1])
    out = [f'<path d="{cizgi_d(pts, True)}" fill="{renk}"/>']
    if isik < 0:
        gp = [tepe] + [p for p in pts if p[0] > tepe[0]] + [(tepe[0] + w * .08, y)]
    else:
        gp = [tepe] + [p for p in reversed(pts) if p[0] < tepe[0]] + [(tepe[0] - w * .08, y)]
    out.append(f'<path d="{cizgi_d(gp, True)}" fill="{koyu(renk, .3)}"/>')
    out.append(f'<path d="{cizgi_d([p for p in pts if (p[0] <= tepe[0]) == (isik < 0)])}" stroke="{acik(renk, .35)}" stroke-width="1.5" fill="none" opacity=".7"/>')
    return "".join(out)


# ------------------------------------------------------------------ canlılar

def marti(x, y, o=1.0, kanat=0.0, renk="#2A2E3A", ayrintili=False):
    """Martı. ayrintili=True → beyaz gövde, gri kanat, siyah uç (yakın plan)."""
    if not ayrintili:
        d = (f"M{f(x - 22 * o)} {f(y - 3 * o + kanat)} Q{f(x - 11 * o)} {f(y - 12 * o + kanat)} {f(x)} {f(y)} "
             f"Q{f(x + 11 * o)} {f(y - 12 * o + kanat)} {f(x + 22 * o)} {f(y - 3 * o + kanat)} "
             f"Q{f(x + 10 * o)} {f(y - 6 * o + kanat * .5)} {f(x)} {f(y + 3 * o)} Q{f(x - 10 * o)} {f(y - 6 * o + kanat * .5)} {f(x - 22 * o)} {f(y - 3 * o + kanat)} Z")
        return f'<path d="{d}" fill="{renk}"/>'
    k = kanat
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">'
            f'<path d="M-30 -2 Q-16 -18 -2 -3 Q-14 -6 -30 -2 Z" fill="#C9D3DC" stroke="#3A4250" stroke-width="1.2" transform="rotate({f(-k)} -2 -3)"/>'
            f'<path d="M-30 -2 Q-27 -6 -22 -7 L-26 -1 Z" fill="#2A2E3A" transform="rotate({f(-k)} -2 -3)"/>'
            f'<ellipse cx="0" cy="0" rx="12" ry="5" fill="#FFFFFF" stroke="#3A4250" stroke-width="1.2"/>'
            f'<circle cx="10" cy="-2" r="4.4" fill="#FFFFFF" stroke="#3A4250" stroke-width="1.2"/>'
            f'<path d="M14 -2 L20 -0.6 L14 0.6 Z" fill="#F0A21A" stroke="#8C5500" stroke-width=".6"/>'
            f'<circle cx="11.2" cy="-3" r=".9" fill="#1B1D26"/>'
            f'<path d="M-11 -1 L-19 2 L-11 2.6 Z" fill="#FFFFFF" stroke="#3A4250" stroke-width="1"/>'
            f'<path d="M30 -2 Q16 -18 2 -3 Q14 -6 30 -2 Z" fill="#DDE4EA" stroke="#3A4250" stroke-width="1.2" transform="rotate({f(k)} 2 -3)"/>'
            f'<path d="M30 -2 Q27 -6 22 -7 L26 -1 Z" fill="#2A2E3A" transform="rotate({f(k)} 2 -3)"/>'
            f'</g>')


def kefal(s, x, y, uz, aci=0.0, sirt="#4F7E86", karin="#EEF5F6", cizgi="#1B3C44", isik=True, ad=None):
    """İnci kefali: gümüş karın, yeşilimsi-gri sırt, çatal kuyruk. (x, y) gövde merkezi."""
    o = uz / 100
    g = s.lin([(0, sirt), (.45, karis(sirt, karin, .55)), (.62, karin), (1, acik(karin, .3))], 0, 0, 0, 1, ad="kf")
    govde = ("M-48 0 C-36 -14 -6 -17 16 -13 C30 -10 42 -5 48 -1 C42 4 30 9 14 12 C-6 15 -36 12 -48 0 Z")
    kuyruk = "M-46 0 L-62 -13 Q-58 0 -62 13 Z"
    sirt_yuz = "M-12 -14 Q-2 -24 10 -14 Z"
    karin_yuz = "M-8 12 Q2 19 10 11 Z"
    pul = "".join(f'<path d="M{f(-30 + i * 9)} -4 q3 3 0 6" fill="none" stroke="{cizgi}" stroke-width=".7" opacity=".35"/>' for i in range(7))
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(aci)}) scale({f(o, 3)})">'
            f'<path d="{kuyruk}" fill="{sirt}" stroke="{cizgi}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="{sirt_yuz}" fill="{sirt}" stroke="{cizgi}" stroke-width="1.4"/>'
            f'<path d="{karin_yuz}" fill="{karis(sirt, karin, .5)}" stroke="{cizgi}" stroke-width="1.2"/>'
            f'<path d="{govde}" fill="{g}" stroke="{cizgi}" stroke-width="1.8"/>'
            f'<path d="M-40 1 C-20 -2 10 -2 40 0" fill="none" stroke="{cizgi}" stroke-width=".9" opacity=".45"/>'
            f'{pul}'
            f'<path d="M24 -10 Q30 -2 26 9" fill="none" stroke="{cizgi}" stroke-width="1.2" opacity=".6"/>'
            f'<circle cx="34" cy="-3" r="4" fill="#FFFFFF" stroke="{cizgi}" stroke-width="1.2"/>'
            f'<circle cx="35" cy="-3" r="2.2" fill="#1B1D26"/><circle cx="34.2" cy="-4" r=".8" fill="#FFFFFF"/>'
            + (f'<path d="M-20 -9 C-6 -12 8 -11 22 -7" stroke="#FFFFFF" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".55"/>' if isik else "")
            + '</g>')


def damla_sicrama(x, y, o=1.0, renk="#FFFFFF"):
    """Balığın sudan çıkışındaki sıçrama damlaları."""
    out = []
    for dx, dy, rr in ((-10, -6, 2.2), (-4, -12, 1.6), (6, -9, 2), (12, -4, 1.4), (0, -16, 1.2)):
        out.append(f'<circle cx="{f(x + dx * o)}" cy="{f(y + dy * o)}" r="{f(rr * o)}" fill="{renk}" opacity=".85"/>')
    out.append(f'<path d="M{f(x - 16 * o)} {f(y)} q{f(16 * o)} {f(-8 * o)} {f(32 * o)} 0" stroke="{renk}" stroke-width="{f(1.6 * o)}" fill="none" opacity=".8"/>')
    return "".join(out)


# ------------------------------------------------------------------ tekne, feribot, ev

def tekne(s, x, y, uz, govde="#C8442F", ust="#F4E9D8", yelken=None, cizgi="#1B1D26", ayrinti=True):
    o = uz / 100
    out = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">']
    if yelken:
        out.append(f'<path d="M2 -6 L2 -78" stroke="{cizgi}" stroke-width="2.4"/>'
                   f'<path d="M4 -74 Q34 -40 40 -10 L4 -10 Z" fill="{yelken}" stroke="{cizgi}" stroke-width="2"/>'
                   f'<path d="M0 -70 Q-22 -40 -26 -12 L0 -12 Z" fill="{acik(yelken, .45)}" stroke="{cizgi}" stroke-width="2"/>')
    out.append(f'<path d="M-50 -10 L50 -10 L40 8 Q0 14 -40 8 Z" fill="{govde}" stroke="{cizgi}" stroke-width="2.4" stroke-linejoin="round"/>'
               f'<path d="M-47 -4 L47 -4" stroke="{ust}" stroke-width="3"/>')
    if ayrinti and not yelken:
        out.append(f'<rect x="-18" y="-26" width="30" height="16" rx="2" fill="{ust}" stroke="{cizgi}" stroke-width="2"/>'
                   f'<rect x="-13" y="-22" width="8" height="7" fill="#9FD9E6" stroke="{cizgi}" stroke-width="1.2"/>'
                   f'<rect x="-1" y="-22" width="8" height="7" fill="#9FD9E6" stroke="{cizgi}" stroke-width="1.2"/>')
    out.append("</g>")
    return "".join(out)


def feribot(s, x, y, uz, govde="#F4F1EA", serit="#C8442F", serit2="#13A3A6", cizgi="#1B1D26", vagon=True):
    """Tatvan–Van tren feribotu esinli: uzun gövde, güvertede vagonlar, köprü üstü."""
    o = uz / 300
    out = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">',
           f'<path d="M-150 -18 L150 -18 L138 10 Q0 18 -140 10 Z" fill="{govde}" stroke="{cizgi}" stroke-width="3" stroke-linejoin="round"/>',
           f'<path d="M-147 -6 L146 -6" stroke="{serit}" stroke-width="6"/><path d="M-143 3 L142 3" stroke="{serit2}" stroke-width="3"/>']
    if vagon:
        for i in range(4):
            vx = -128 + i * 52
            out.append(f'<rect x="{vx}" y="-40" width="46" height="22" rx="3" fill="{["#7A4E8C", "#2B50B5", "#C8742F", "#1F8A5B"][i]}" stroke="{cizgi}" stroke-width="2.4"/>'
                       f'<path d="M{vx + 6} -33 h34" stroke="#FFFFFF" stroke-width="2" opacity=".6"/>')
    out.append(f'<path d="M86 -18 L86 -52 L128 -52 L134 -18 Z" fill="{govde}" stroke="{cizgi}" stroke-width="2.6" stroke-linejoin="round"/>'
               f'<path d="M90 -46 h36" stroke="{cizgi}" stroke-width="2"/>'
               + "".join(f'<rect x="{92 + i * 9}" y="-42" width="6" height="7" fill="#9FD9E6" stroke="{cizgi}" stroke-width="1.2"/>' for i in range(4))
               + f'<rect x="100" y="-68" width="12" height="16" fill="{serit}" stroke="{cizgi}" stroke-width="2.4"/>'
               + f'<path d="M100 -64 h12" stroke="#FFFFFF" stroke-width="2.4"/>'
               + "</g>")
    return "".join(out)


def ev(x, y, w, h, tohum, duvar="#E9D3B0", cati="#B8553A", duz=False, cizgi=None, pencere="#5B4636", isik=-1):
    """Köy evi: Van yöresinde düz damlı kerpiç ya da kiremit çatılı taş ev."""
    r = RNG(tohum)
    out = []
    st = f' stroke="{cizgi}" stroke-width="{f(max(1, w * .03))}"' if cizgi else ""
    out.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{duvar}"{st}/>')
    gx = x + w * .62 if isik < 0 else x
    out.append(f'<rect x="{f(gx)}" y="{f(y - h)}" width="{f(w * .38)}" height="{f(h)}" fill="#000" opacity=".12"/>')
    if duz:
        out.append(f'<rect x="{f(x - w * .05)}" y="{f(y - h - h * .12)}" width="{f(w * 1.1)}" height="{f(h * .14)}" fill="{koyu(duvar, .25)}"{st}/>')
    else:
        out.append(f'<path d="M{f(x - w * .08)} {f(y - h)} L{f(x + w / 2)} {f(y - h - h * .55)} L{f(x + w * 1.08)} {f(y - h)} Z" fill="{cati}"{st}/>')
    for i in range(r.randint(1, 2)):
        px = x + w * (.18 + .42 * i)
        out.append(f'<rect x="{f(px)}" y="{f(y - h * .7)}" width="{f(w * .18)}" height="{f(h * .28)}" fill="{pencere}"/>')
    return "".join(out)
