"""Kâğıtta animasyon (barrier grid / scanimation): 6 kare tek resimde, asetat perde ile oynar.

Geçme: şerit genişliği w = 0,6 mm, N = 6 kare, dönem p = N·w = 3,6 mm. Kare k, j. dönemde
[x0 + j·p + k·w, x0 + j·p + (k+1)·w) şeridine basılır (SVG clipPath, vektör). Perde (asetat): siyah çubuklar,
her dönemde 0,6 mm'lik bir yarık; perde sağa w kaydıkça sıradaki kare görünür.

Panel 1 · Gaz tanecikleri (10/04 Gazlar): aynı kapta 8'er tanecik; soğukta yavaş (dörtlü sıralar, kare başına ≈ 5 mm),
sıcakta hızlı (ikili sıra ve sütunlar, kare başına ≈ 7–11 mm). Tanecikler doğrusal gider, duvara ya da birbirine
esnek çarpınca geri döner (her dönüşün bir çarpışma nedeni var); sıcakta duvara çarpma daha sık: basınç büyük.
Panel 2 · Tuz suda çözünür (10/05 Çözeltiler): köşedeki Na⁺ ve kenardaki Cl⁻ kristalden ayrılır; su molekülleri
Na⁺'ya O ucuyla (δ−), Cl⁻'ye H ucuyla (δ+) döner ve iyonu sarar (hidratlaşma). Boyutlar ölçekli değil (Cl⁻ > Na⁺).
"""
import math
import random

N, W = 6, 0.6
P = N * W
X0, X1 = 15.0, 195.0                       # 50 dönem
PANEL_Y = {"gaz": 46.0, "tuz": 126.0}
PANEL_H = 68.0
PERDE_Y = [(44.6, 115.4), (124.6, 195.4)]  # çubuklu bölgeler (asetat)
PERDE_X = (X0 - P, X1 + P)
ARTI = [(12.0, 40.5), (198.0, 40.5), (12.0, 199.5), (198.0, 199.5)]   # hizalama artıları (sayfa ve asetat)
TRI = [0, 1 / 3, 2 / 3, 1, 2 / 3, 1 / 3]

OBS, KAR = "#1B1D26", "#FBFDFD"
SOGUK, SICAK = "#1D3A8A", "#E2533D"
NA, CL, OKS, HID = "#7B3F8C", "#1F8A5B", "#E2533D", "#FBFDFD"
SU, DUVAR = "#DCF3F1", "#343947"
R_G = 3.0
R_NA, R_CL, R_O, R_H, OH, HOH = 2.8, 4.4, 2.3, 1.4, 2.6, 105.0


def _f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ------------------------------------------------------------------ şekil modeli: ("d", x, y, r, dolgu, cizgi, en) · ("c", x1, y1, x2, y2, renk, en) · ("r", x, y, w, h, dolgu)
def _daire(x, y, r, dolgu, cizgi=OBS, en=.35):
    return ("d", x, y, r, dolgu, cizgi, en)


def _isaret(x, y, tur, boy=1.6):
    """iyon yükü: + ya da − (beyaz dikdörtgen; glif yok)."""
    o = [("r", x - boy / 2, y - .28, boy, .56, "#FFFFFF")]
    if tur == "+":
        o.append(("r", x - .28, y - boy / 2, .56, boy, "#FFFFFF"))
    return o


# ------------------------------------------------------------------ PANEL 1 · gaz
KUTU = {"soguk": (6.0, 8.0, 84.0, 62.0), "sicak": (96.0, 8.0, 174.0, 62.0)}


def _zincir(kutu, yon, konum, m, psi):
    """m tanecik bir doğru üzerinde duvardan duvara: komşular aynı karede değer. → [(sıra, [6 merkez])], çarpışmalar"""
    x1, y1, x2, y2 = kutu
    a, b = (x1, x2) if yon == "y" else (y1, y2)
    L = ((b - a) - 2 * m * R_G) / m
    out, carp = [], []
    for i in range(m):
        sol = a + i * (L + 2 * R_G) + R_G
        konumlar = []
        for k in range(N):
            u = TRI[(k + psi) % N]
            u = u if i % 2 == 0 else 1 - u
            c = sol + L * u
            konumlar.append((c, konum) if yon == "y" else (konum, c))
        out.append(konumlar)
    for k in range(N):
        for i in range(m):
            c = out[i][k][0] if yon == "y" else out[i][k][1]
            if i == 0 and abs(c - (a + R_G)) < 1e-6:
                carp.append((k, "duvar", (a, konum) if yon == "y" else (konum, a), yon, -1))
            if i == m - 1 and abs(c - (b - R_G)) < 1e-6:
                carp.append((k, "duvar", (b, konum) if yon == "y" else (konum, b), yon, 1))
            if i < m - 1:
                d = (out[i + 1][k][0] - out[i][k][0]) if yon == "y" else (out[i + 1][k][1] - out[i][k][1])
                if abs(d - 2 * R_G) < 1e-6:
                    p = out[i][k]
                    carp.append((k, "tanecik", (p[0] + R_G, p[1]) if yon == "y" else (p[0], p[1] + R_G), yon, 0))
    return out, carp, L


GAZ_ZINCIR = [  # (kutu, yön, konum, tanecik sayısı, faz)
    ("soguk", "y", 21.0, 4, 0), ("soguk", "y", 47.5, 4, 2),
    ("sicak", "y", 19.0, 2, 0), ("sicak", "y", 51.0, 2, 4), ("sicak", "x", 113.0, 2, 5), ("sicak", "x", 157.0, 2, 3)]


def gaz_verisi():
    """→ tanecikler [{kutu, konum[6]}], çarpışmalar, kare başına hızlar."""
    tan, carp, hiz = [], [], {}
    for kutu, yon, konum, m, psi in GAZ_ZINCIR:
        z, c, L = _zincir(KUTU[kutu], yon, konum, m, psi)
        tan += [{"kutu": kutu, "konum": k} for k in z]
        carp += [dict(zip(("kare", "tur", "yer", "yon", "taraf"), x), kutu=kutu) for x in c]
        hiz.setdefault(kutu, []).append(round(L / 3, 2))
    return tan, carp, hiz


def _kivilcim(x, y, yon, taraf, tur):
    """çarpma izi: duvarın dışında üç kısa çizgi ya da iki tanecik arasında iki çizgi."""
    o = []
    if tur == "duvar":
        for d in (-2.2, 0, 2.2):
            if yon == "y":
                xx = x + taraf * 1.2
                o.append(("c", xx, y + d * .9, xx + taraf * 2.2, y + d * 1.5, "#E2533D", .45))
            else:
                yy = y + taraf * 1.2
                o.append(("c", x + d * .9, yy, x + d * 1.5, yy + taraf * 2.2, "#E2533D", .45))
    else:
        for s in (-1, 1):
            if yon == "y":
                o.append(("c", x, y + s * (R_G + .6), x, y + s * (R_G + 2.4), "#F0A21A", .5))
            else:
                o.append(("c", x + s * (R_G + .6), y, x + s * (R_G + 2.4), y, "#F0A21A", .5))
    return o


def gaz_kare(k):
    tan, carp, _ = gaz_verisi()
    o = []
    for t in tan:
        x, y = t["konum"][k]
        o.append(_daire(x, y, R_G, SOGUK if t["kutu"] == "soguk" else SICAK, OBS, .35))
        o.append(_daire(x - .75, y - .75, .7, "#FFFFFF", None, 0))
    for c in carp:
        if c["kare"] == k:
            o += _kivilcim(*c["yer"], c["yon"], c["taraf"], c["tur"])
    return o


def gaz_sabit():
    o = []
    for x1, y1, x2, y2 in KUTU.values():
        o.append(("kutu", x1, y1, x2, y2))
    return o


# ------------------------------------------------------------------ PANEL 2 · tuz çözünmesi
D = 8.0
KRISTAL = [(12.0 + i * D, 58.0 - j * D, "Cl" if (i + j) % 2 == 0 else "Na") for i in range(5) for j in range(4)]
AYRILAN = {"Na": ((44.0, 34.0), (88.0, 15.5)), "Cl": ((44.0, 42.0), (91.0, 52.0))}


def _su(x, y, aci, o):
    """su molekülü: O (kırmızı) + iki H (beyaz), açıortay yönü aci (derece, O'dan H'lere)."""
    for s in (-1, 1):
        a = math.radians(aci + s * HOH / 2)
        o.append(_daire(x + OH * math.cos(a), y + OH * math.sin(a), R_H, HID, OBS, .3))
    o.append(_daire(x, y, R_O, OKS, OBS, .35))


def _iyon_konum(ad, k):
    (xa, ya), (xb, yb) = AYRILAN[ad]
    t = k / (N - 1)
    return xa + (xb - xa) * t, ya + (yb - ya) * t


def _kabuk(ad):
    """iyonun etrafındaki 4 su molekülünün son yerleri (iyona göre) ve açıları."""
    out = []
    for i, a in enumerate((20, 110, 200, 290)):
        r = math.radians(a)
        if ad == "Na":   # O ucu iyona: O merkezi r_Na + r_O + 0,3; H'ler dışarı bakar
            d = R_NA + R_O + .35
            out.append((d * math.cos(r), d * math.sin(r), a))
        else:            # bir H iyona değer: H merkezi r_Cl + r_H; O, aynı doğrultuda OH ötede
            dh = R_CL + R_H + .3
            hx, hy = dh * math.cos(r), dh * math.sin(r)
            ox, oy = hx + OH * math.cos(r), hy + OH * math.sin(r)
            out.append((ox, oy, a + 180 - HOH / 2))
    return out


def _su_daireleri(x, y, aci):
    o = []
    _su(x, y, aci, o)
    return [(c[1], c[2], c[3]) for c in o]


def _cakisir(a, b, pay=.25):
    return any(math.hypot(p[0] - q[0], p[1] - q[1]) < p[2] + q[2] + pay for p in a for q in b)


def _su_yolu(bas, ad, i):
    """kabuk molekülünün 6 karedeki (x, y, açı) değerleri."""
    bx, by, ba = bas
    dx, dy, a = _kabuk(ad)[i]
    out = []
    for k in range(N):
        s = (k / (N - 1)) ** .8
        x, y = _iyon_konum(ad, k)
        fark = ((a - ba + 180) % 360) - 180
        out.append((bx + (x + dx - bx) * s, by + (y + dy - by) * s, ba + fark * s))
    return out


def _serbest_yolu(x, y, i):
    out = []
    for k in range(N):
        f = 2 * math.pi * k / N + i * 1.7
        out.append((x + .8 * math.cos(f), y + .8 * math.sin(f), (i * 67 + 14 * math.sin(f)) % 360))
    return out


SERBEST_SU = [(70, 34), (106, 34), (118, 14), (130, 47), (146, 26), (160, 54), (166, 12), (112, 60), (62, 60), (140, 61),
              (78, 6), (152, 39), (128, 30), (170, 34), (100, 46)]
_DUZEN = None


def _tuz_duzen():
    """kabuk sularının başlangıç yerleri ve serbest sular: hiçbir karede çakışma olmayacak biçimde (açgözlü, tohumlu)."""
    global _DUZEN
    if _DUZEN is not None:
        return _DUZEN
    rng = random.Random(11)
    kristal = [(x, y, R_NA if ad == "Na" else R_CL) for x, y, ad in KRISTAL]
    iyon = {k: [(*_iyon_konum(ad, k), R_NA if ad == "Na" else R_CL) for ad in ("Na", "Cl")] for k in range(N)}
    yerlesen = {k: [] for k in range(N)}          # karelere göre su daireleri
    kabuk = {}
    for ad in ("Na", "Cl"):
        for i in range(4):
            for _ in range(3000):
                (xa, ya), (xb, yb) = AYRILAN[ad]
                bas = (rng.uniform(50, 140), rng.uniform(5, 63), rng.uniform(0, 360))
                yol = _su_yolu(bas, ad, i)
                tamam = True
                for k, (x, y, a) in enumerate(yol):
                    d = _su_daireleri(x, y, a)
                    if not all(3.5 < c[0] < 176.5 and 3.5 < c[1] < 64.5 for c in d) or _cakisir(d, kristal) \
                            or _cakisir(d, [c for c in iyon[k]], .1 if k == N - 1 else .2) or _cakisir(d, yerlesen[k]):
                        tamam = False
                        break
                if tamam:
                    kabuk[(ad, i)] = bas
                    for k, (x, y, a) in enumerate(yol):
                        yerlesen[k] += _su_daireleri(x, y, a)
                    break
            else:
                raise RuntimeError(f"kabuk suyu yerleşmedi: {ad} {i}")
    serbest = []
    for i, (x, y) in enumerate(SERBEST_SU):
        yol = _serbest_yolu(x, y, i)
        if all(not _cakisir(_su_daireleri(*v), kristal + iyon[k] + yerlesen[k]) for k, v in enumerate(yol)):
            serbest.append((x, y, i))
            for k, v in enumerate(yol):
                yerlesen[k] += _su_daireleri(*v)
    _DUZEN = {"kabuk": kabuk, "serbest": serbest}
    return _DUZEN


def tuz_kare(k):
    o = []
    duzen = _tuz_duzen()
    for ad in ("Na", "Cl"):
        x, y = _iyon_konum(ad, k)
        for i in range(4):
            _su(*_su_yolu(duzen["kabuk"][(ad, i)], ad, i)[k], o)
        r = R_NA if ad == "Na" else R_CL
        o.append(_daire(x, y, r, NA if ad == "Na" else CL, OBS, .4))
        o += _isaret(x, y, "+" if ad == "Na" else "−", 1.5 if ad == "Na" else 2.0)
    for x, y, i in duzen["serbest"]:
        _su(*_serbest_yolu(x, y, i)[k], o)
    return o


def tuz_sabit():
    o = [("r", 2.0, 2.0, 176.0, 64.0, SU)]
    for x, y, ad in KRISTAL:
        if any(abs(x - a[0][0]) < 1e-6 and abs(y - a[0][1]) < 1e-6 for a in AYRILAN.values()):
            continue
        o.append(_daire(x, y, R_NA if ad == "Na" else R_CL, NA if ad == "Na" else CL, OBS, .4))
        o += _isaret(x, y, "+" if ad == "Na" else "−", 1.5 if ad == "Na" else 2.0)
    return o


KARE = {"gaz": gaz_kare, "tuz": tuz_kare}
SABIT = {"gaz": gaz_sabit, "tuz": tuz_sabit}


# ------------------------------------------------------------------ SVG
def _svg(sekiller):
    o = []
    for s in sekiller:
        if s[0] == "d":
            _, x, y, r, dolgu, cizgi, en = s
            c = f' stroke="{cizgi}" stroke-width="{_f(en)}"' if cizgi else ""
            o.append(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(r)}" fill="{dolgu}"{c}/>')
        elif s[0] == "c":
            _, x1, y1, x2, y2, renk, en = s
            o.append(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="{renk}" stroke-width="{_f(en)}" stroke-linecap="round"/>')
        elif s[0] == "r":
            _, x, y, w, h, dolgu = s
            rx = ' rx="3"' if w > 50 else ""
            o.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}"{rx} fill="{dolgu}"/>')
        elif s[0] == "kutu":
            _, x1, y1, x2, y2 = s
            o.append(f'<rect x="{_f(x1 - .6)}" y="{_f(y1 - .6)}" width="{_f(x2 - x1 + 1.2)}" height="{_f(y2 - y1 + 1.2)}" rx="1.2" fill="#FFFFFF" '
                     f'stroke="{DUVAR}" stroke-width="1.2"/>')
    return "".join(o)


def _gecme(ad, oy):
    """bir panelin geçmeli resmi: önce sabit parçalar, sonra her kare kendi şeritlerinde."""
    y0 = PANEL_Y[ad]
    o = [f'<g transform="translate({_f(X0)} {_f(y0)})" data-panel="{ad}">', _svg(SABIT[ad]())]
    n_donem = int(round((X1 - X0) / P))
    for k in range(N):
        rect = "".join(f'<rect x="{_f(j * P + k * W)}" y="-1" width="{_f(W)}" height="{_f(PANEL_H + 2)}"/>' for j in range(n_donem))
        o.append(f'<clipPath id="{oy}-{ad}-{k}">{rect}</clipPath>')
        o.append(f'<g clip-path="url(#{oy}-{ad}-{k})" data-kare="{k}">{_svg(KARE[ad](k))}</g>')
    o.append('</g>')
    return "".join(o)


def _artilar(renk="#1B1D26"):
    return "".join(f'<path d="M{_f(x - 3)} {_f(y)} H{_f(x + 3)} M{_f(x)} {_f(y - 3)} V{_f(y + 3)}" stroke="{renk}" stroke-width=".3"/>'
                   f'<circle cx="{_f(x)}" cy="{_f(y)}" r="1.4" fill="none" stroke="{renk}" stroke-width=".25"/>' for x, y in ARTI)


def sayfa_svg():
    """s5: iki geçmeli panel + hizalama artıları (tam sayfa SVG, mm)."""
    return (f'<svg class="anim-svg" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">'
            f'{_gecme("gaz", "an")}{_gecme("tuz", "an")}{_artilar()}</svg>')


def perde_svg():
    """s6 (asetat): siyah çubuklar, 0,6 mm yarıklar; yarık j: [x0 + j·p, x0 + j·p + w)."""
    o = ['<svg class="perde-svg" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg" data-tema-sabit>']
    for y1, y2 in PERDE_Y:
        cubuk = []
        j = -1
        while True:
            x = X0 + j * P + W
            if x >= PERDE_X[1]:
                break
            xa, xb = max(x, PERDE_X[0]), min(x + P - W, PERDE_X[1])
            if xb > xa:
                cubuk.append(f'<rect data-cubuk="{j}" x="{_f(xa)}" y="{_f(y1)}" width="{_f(xb - xa)}" height="{_f(y2 - y1)}"/>')
            j += 1
        o.append(f'<g fill="#000000">{"".join(cubuk)}</g>')
        o.append(f'<rect x="{_f(PERDE_X[0])}" y="{_f(y1)}" width="{_f(PERDE_X[1] - PERDE_X[0])}" height="{_f(y2 - y1)}" fill="none" stroke="#000000" stroke-width=".3"/>')
    o.append(_artilar("#000000"))
    o.append('</svg>')
    return "".join(o)


def kare_seridi(ad):
    """öykü şeridi: 6 kare yan yana (geçmesiz), sabit + hareketli parçalar."""
    ara = 8.0
    o = [f'<svg class="kare-seridi" viewBox="0 0 {_f(N * 180 + (N - 1) * ara)} {_f(PANEL_H + 12)}" xmlns="http://www.w3.org/2000/svg">']
    for k in range(N):
        x = k * (180 + ara)
        o.append(f'<g transform="translate({_f(x)} 0)"><rect x="0" y="0" width="180" height="{_f(PANEL_H)}" rx="4" fill="#FFFFFF" stroke="{OBS}" stroke-width="1"/>'
                 f'{_svg(SABIT[ad]())}{_svg(KARE[ad](k))}'
                 f'<text x="90" y="{_f(PANEL_H + 10.5)}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="10" fill="{OBS}">{k + 1}</text></g>')
    o.append('</svg>')
    return "".join(o)


# ------------------------------------------------------------------ benzetim ve kare temizliği (basılacak PDF'ten)
DPI = 25.4 * 10 / W          # 423,33 dpi: bir şerit tam 10 piksel
PX = 10


def _beklenen(ad, k, bolge, boyut):
    """kare k'nın mürekkep maskesi (analitik): sabit parçalar + o karenin hareketli parçaları."""
    from PIL import Image, ImageDraw
    im = Image.new("L", boyut, 0)
    d = ImageDraw.Draw(im)
    kx, ky = DPI / 25.4, DPI / 25.4
    ox, oy = X0 - bolge[0], PANEL_Y[ad] - bolge[1]
    for s in SABIT[ad]() + KARE[ad](k):
        if s[0] == "d" and s[4] != HID:
            _, x, y, r, *_ = s
            r += .2
            d.ellipse(((ox + x - r) * kx, (oy + y - r) * ky, (ox + x + r) * kx, (oy + y + r) * ky), fill=255)
        elif s[0] == "c":
            _, x1, y1, x2, y2, _r, en = s
            d.line(((ox + x1) * kx, (oy + y1) * ky, (ox + x2) * kx, (oy + y2) * ky), fill=255, width=max(2, int(en * kx)))
        elif s[0] == "kutu":
            _, x1, y1, x2, y2 = s
            d.rectangle(((ox + x1 - 1.2) * kx, (oy + y1 - 1.2) * ky, (ox + x2 + 1.2) * kx, (oy + y2 + 1.2) * ky), outline=255, width=int(1.3 * kx))
    import numpy as np
    return np.asarray(im) > 0


def _kaydir(m, px):
    import numpy as np
    out = np.zeros_like(m)
    if px >= 0:
        out[:, px:] = m[:, :m.shape[1] - px]
    else:
        out[:, :px] = m[:, -px:]
    return out


def temizlik(pdf):
    """her panel ve her kare için: görünen (yarık) pikseller hangi kareyle örtüşüyor? → dict"""
    import numpy as np
    import onizle as O
    sonuc = {}
    for ad, (y1, y2) in zip(("gaz", "tuz"), PERDE_Y):
        bolge = (X0 - P, y1 + 1.0, X1 - X0 + 2 * P, y2 - y1 - 2.0)
        sayfa = np.asarray(O.sayfa_raster(pdf, 5, DPI, bolge)).astype(np.float64) / 255
        perde = np.asarray(O.sayfa_raster(pdf, 6, DPI, bolge).convert("L")) < 128
        h, w = perde.shape
        lum = sayfa @ np.array([.2126, .7152, .0722])
        murekkep = lum < .55
        bek = [_beklenen(ad, j, bolge, (w, h)) for j in range(N)]
        kareler = []
        for k in range(N):
            for kayma, etiket in ((k * PX, "tam"), (k * PX + 2, "+0,12 mm")):
                gor = ~_kaydir(perde, kayma)
                gor[:, :int(P / 25.4 * DPI)] = False          # sol kenarda kaydırma boşluğu
                ink = murekkep & gor
                iou = []
                for j in range(N):
                    e = bek[j] & gor
                    iou.append(float((ink & e).sum() / max(1, (ink | e).sum())))
                hayalet = float((ink & ~bek[k] & np.any([bek[j] for j in range(N) if j != k], 0)).sum() / max(1, ink.sum()))
                kareler.append({"kare": k + 1, "perde": etiket, "iou": [round(v, 3) for v in iou], "en_iyi": int(np.argmax(iou)) + 1,
                                "hayalet": round(hayalet, 4)})
        sonuc[ad] = kareler
    return sonuc


def onizleme(pdf, hedef):
    """asetat kaydırılınca: üstte gerçek görünüm (çubuklar), altta yalnız yarıklardan görülen şeritler (dönem boyunca uzatılmış)."""
    import json
    import os
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import onizle as O
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fnt = ImageFont.truetype(os.path.join(kok, "..", "..", "fontlar", "nunito", "static", "Nunito-800.ttf"), 22)
    for ad, (y1, y2) in zip(("gaz", "tuz"), PERDE_Y):
        bolge = (X0 - P, y1, X1 - X0 + 2 * P, y2 - y1)
        sayfa = np.asarray(O.sayfa_raster(pdf, 5, DPI, bolge)).astype(np.float64)
        perde = np.asarray(O.sayfa_raster(pdf, 6, DPI, bolge).convert("L")) < 128
        h, w = perde.shape
        x0 = int(round(P / 25.4 * DPI))
        kareler = []
        for k in range(N):
            gor = ~_kaydir(perde, k * PX)
            gercek = np.where(gor[..., None], sayfa, 12.0)
            yeni = sayfa.copy()
            for j in range((w - x0) // (N * PX)):
                a = x0 + j * N * PX + k * PX
                yeni[:, x0 + j * N * PX: x0 + (j + 1) * N * PX] = np.repeat(sayfa[:, a + PX // 2:a + PX // 2 + 1], N * PX, 1)
            ust = Image.fromarray(gercek.astype(np.uint8)).resize((720, int(720 * h / w)), Image.LANCZOS)
            alt = Image.fromarray(yeni.astype(np.uint8)).resize((720, int(720 * h / w)), Image.LANCZOS)
            kare = Image.new("RGB", (720, ust.height + alt.height + 70), (255, 255, 255))
            kare.paste(ust, (0, 30))
            kare.paste(alt, (0, ust.height + 66))
            dd = ImageDraw.Draw(kare)
            dd.text((8, 2), f"Asetat altından · kare {k + 1}/6", fill=(27, 29, 38), font=fnt)
            dd.text((8, ust.height + 36), "Yalnız yarıklardaki şeritler (çubuksuz)", fill=(86, 99, 110), font=fnt)
            kareler.append(kare)
        kareler[0].save(os.path.join(hedef, f"animasyon-{ad}.gif"), save_all=True, append_images=kareler[1:], duration=170, loop=0, optimize=True)
    with open(os.path.join(hedef, "animasyon-temizlik.json"), "w", encoding="utf-8") as fp:
        json.dump(temizlik(pdf), fp, ensure_ascii=False, indent=1)
    print("animasyon: GIF'ler ve kare temizliği yazıldı")
