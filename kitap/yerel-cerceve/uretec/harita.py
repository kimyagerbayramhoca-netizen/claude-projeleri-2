"""Türkiye Kimya Rotası haritaları: içindekiler sayfasının bilgi haritası ve kapaktaki "gökyüzü haritası".

Taban düzlem `turkiye_veri.py` ile aynıdır: Lambert konik konform, 1 birim = 1 km, Y aşağı, W×H ≈ 1797×865.
`proje(enlem, boylam)` herhangi bir noktayı bu düzleme taşır. Çizimler SVG metni döndürür (yerel-ortak/cizim
kurallarıyla: önekli kimlikler, konturlu yazı yok, filtre yok).
"""
import math
import os
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
ORTAK = os.path.normpath(os.path.join(BURA, "..", "..", "yerel-ortak"))
for _p in (ORTAK, BURA):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import turkiye_veri as T  # noqa: E402
from harita_veri_uret import lcc  # noqa: E402
from cizim.temel import Svg, f, cizgi_d, egri_d, selcuklu_yildizi, yildiz_noktalari, acik, koyu, karis, halolu_yazi, rng as RNG  # noqa: E402

W, H = T.W, T.H
OBS = "#1B1D26"


def proje(enlem, boylam):
    x, y = lcc(boylam, enlem)
    return x - T.X0, T.Y1 - y


def rota_noktalari(y):
    """Yolun çizgi noktaları: duraklar sırasıyla, sonra kale (aynı yerdeyse atlanır)."""
    pts = [proje(d["enlem"], d["boylam"]) for d in y["duraklar"]]
    k = proje(y["kale"]["enlem"], y["kale"]["boylam"])
    if not pts or math.dist(pts[-1], k) > 4:
        pts.append(k)
    return pts


def rota_merkez(y):
    p = rota_noktalari(y)
    return sum(a for a, _ in p) / len(p), sum(b for _, b in p) / len(p)


# dağ simgeleri (resimli harita dokusu): (ad, enlem, boylam, ölçek)
DAGLAR = [("Ağrı", 39.70, 44.30, 1.25), ("Süphan", 38.93, 42.83, .9), ("Nemrut", 38.65, 42.23, .75), ("Erciyes", 38.53, 35.45, 1.0),
          ("Hasan", 38.13, 34.17, .8), ("Uludağ", 40.07, 29.22, .85), ("Kaçkar", 40.83, 41.16, .95), ("Palandöken", 39.80, 41.30, .8),
          ("Aladağlar", 37.83, 35.15, .9), ("Munzur", 39.25, 39.40, .8), ("Bolkar", 37.40, 34.55, .75), ("Ilgaz", 41.05, 33.75, .7),
          ("Cilo", 37.48, 44.00, .95), ("Dedegöl", 37.65, 31.30, .7), ("Murat", 38.95, 29.70, .65)]


def _dag(s, x, y, o, tohum, kar="#FFFFFF", govde="#B9A27E", golge="#8C7458"):
    """Küçük, gölgeli, karlı dağ simgesi (taban merkezi x, y)."""
    r = RNG(tohum)
    w, h = 26 * o, 20 * o
    tepe = (x + r.uniform(-2, 2) * o, y - h)
    sol, sag = (x - w / 2, y), (x + w / 2, y)
    out = (f'<path d="M{f(sol[0])} {f(sol[1])} L{f(tepe[0])} {f(tepe[1])} L{f(sag[0])} {f(sag[1])} Z" fill="{govde}"/>'
           f'<path d="M{f(tepe[0])} {f(tepe[1])} L{f(sag[0])} {f(sag[1])} L{f(x + w * .08)} {f(y)} Z" fill="{golge}"/>')
    k = .38
    out += (f'<path d="M{f(tepe[0] - w / 2 * k)} {f(tepe[1] + h * k)} L{f(tepe[0])} {f(tepe[1])} L{f(tepe[0] + w / 2 * k)} {f(tepe[1] + h * k)} '
            f'L{f(tepe[0] + w * .1)} {f(tepe[1] + h * k * .7)} L{f(tepe[0] - w * .02)} {f(tepe[1] + h * k * 1.05)} L{f(tepe[0] - w * .12)} {f(tepe[1] + h * k * .72)} Z" fill="{kar}"/>')
    out += f'<path d="M{f(sol[0])} {f(sol[1])} L{f(tepe[0])} {f(tepe[1])} L{f(sag[0])} {f(sag[1])}" fill="none" stroke="{koyu(golge, .25)}" stroke-width="{f(.9 * o + .3, 2)}" stroke-linejoin="round"/>'
    return out


def _kale_simge(x, y, renk, o=1.0):
    w = 16 * o
    h = 12 * o
    x0, y0 = x - w / 2, y - h / 2
    d = (f"M{f(x0)} {f(y0 + h)} V{f(y0 + h * .3)} h{f(w * .2)} v{f(-h * .3)} h{f(w * .2)} v{f(h * .3)} h{f(w * .2)} v{f(-h * .3)} "
         f"h{f(w * .2)} v{f(h * .3)} h{f(w * .2)} V{f(y0 + h)} Z")
    return (f'<path d="{d}" fill="#FFFFFF" stroke="{OBS}" stroke-width="{f(1.3 * o, 2)}" stroke-linejoin="round"/>'
            f'<path d="M{f(x - w * .13)} {f(y0 + h)} V{f(y0 + h * .68)} A{f(w * .13)} {f(w * .13)} 0 0 1 {f(x + w * .13)} {f(y0 + h * .68)} V{f(y0 + h)} Z" fill="{renk}"/>')


def rozet(x, y, R, no, renk, renk_k, yazi_boy=None, cizgi=OBS):
    """Yol rozeti: altın Selçuklu yıldızı + Yol renginde iç yıldız + beyaz numara (SVG)."""
    yb = yazi_boy or R * 1.05
    return (f'<path d="{cizgi_d(selcuklu_yildizi(x, y, R), True, 2)}" fill="#F0C14A" stroke="{cizgi}" stroke-width="{f(R * .11, 2)}" stroke-linejoin="round"/>'
            f'<path d="{cizgi_d(selcuklu_yildizi(x, y, R * .8), True, 2)}" fill="{renk}" stroke="{cizgi}" stroke-width="{f(R * .07, 2)}" stroke-linejoin="round"/>'
            f'<text x="{f(x, 2)}" y="{f(y + yb * .36, 2)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" '
            f'font-size="{f(yb, 2)}" fill="#FFFFFF">{no}</text>')


def _bayrak(x, y, o=1.0):
    """Başlangıç bayrağı (mercan flama, direk tabanı x, y)."""
    return (f'<path d="M{f(x)} {f(y)} v{f(-34 * o)}" stroke="{OBS}" stroke-width="{f(2.6 * o, 2)}" stroke-linecap="round"/>'
            f'<path d="M{f(x + 1 * o)} {f(y - 34 * o)} h{f(24 * o)} l{f(-6 * o)} {f(7 * o)} l{f(6 * o)} {f(7 * o)} h{f(-24 * o)} Z" '
            f'fill="#E2533D" stroke="{OBS}" stroke-width="{f(1.6 * o, 2)}" stroke-linejoin="round"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(4.2 * o)}" fill="#FFFFFF" stroke="{OBS}" stroke-width="{f(1.6 * o, 2)}"/>')


def _pusula(s, x, y, R):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R)}" fill="#FFFFFF" fill-opacity=".92" stroke="{OBS}" stroke-width="{f(R * .05, 2)}"/>'
            f'<path d="{cizgi_d(yildiz_noktalari(x, y, R * .88, R * .2, 4, -math.pi / 2), True, 2)}" fill="#1D3A8A" stroke="{OBS}" stroke-width="{f(R * .03, 2)}"/>'
            f'<path d="{cizgi_d(selcuklu_yildizi(x, y, R * .45), True, 2)}" fill="#13A3A6" stroke="{OBS}" stroke-width="{f(R * .03, 2)}"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R * .13)}" fill="#F0A21A" stroke="{OBS}" stroke-width="{f(R * .03, 2)}"/>'
            f'<text x="{f(x)}" y="{f(y - R * 1.08)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="{f(R * .42)}" fill="{OBS}">K</text>')


def _yazi_aralikli(x, y, metin, boy, renk, op=1.0, aralik=.32, anchor="middle", aile="Nunito", kalin=900, don=0):
    t = f' transform="rotate({don} {f(x)} {f(y)})"' if don else ""
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" font-family="{aile}" font-weight="{kalin}" font-size="{f(boy)}" '
            f'letter-spacing="{f(boy * aralik, 2)}" fill="{renk}" fill-opacity="{f(op, 2)}"{t}>{metin}</text>')


def _rota_cizgisi(pts, renk, kal=1.0, parlama=None):
    d = egri_d(pts, False, .85)
    out = ""
    if parlama:
        out += f'<path d="{d}" fill="none" stroke="{parlama}" stroke-opacity=".35" stroke-width="{f(16 * kal)}" stroke-linecap="round" stroke-linejoin="round"/>'
    out += (f'<path d="{d}" fill="none" stroke="{OBS}" stroke-width="{f(7.6 * kal)}" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".9"/>'
            f'<path d="{d}" fill="none" stroke="#FFF6DE" stroke-width="{f(5 * kal)}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{renk}" stroke-width="{f(2.6 * kal)}" stroke-dasharray="{f(7 * kal)} {f(4.5 * kal)}" stroke-linecap="round"/>')
    return out


def _yolculuk(s, merkezler, renk="#1B1D26", op=.45, kal=1.6):
    """Yolların sırası: Van'dan başlayıp her yolun merkezine kavisli, ince noktalı yay."""
    out = ""
    for (a, b) in zip(merkezler, merkezler[1:]):
        (x1, y1), (x2, y2) = a, b
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        kv = min(.22 * L, 120)
        cx, cy = mx - dy / L * kv, my + dx / L * kv * (-1 if dx > 0 else 1)
        out += (f'<path d="M{f(x1)} {f(y1)} Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}" fill="none" stroke="{renk}" stroke-opacity="{op}" '
                f'stroke-width="{f(kal)}" stroke-dasharray="1 {f(kal * 3.2)}" stroke-linecap="round"/>')
    return out


# ------------------------------------------------------------------ içindekiler sayfasının bilgi haritası

def bilgi_haritasi(onek, yollar, baslangic, etiketler=None, kirp=(0, 40, W, H - 30), en_mm=210):
    """Okunaklı rota haritası. etiketler: {yol: (x_mm, y_mm)} etiket kutularının çapası (öncü çizgi için).
    Döndürür: (svg, konum) — konum[yol] = rota merkezinin mm cinsinden yeri (HTML etiketleri için)."""
    s = Svg(onek)
    x0, y0, x1, y1 = kirp
    w, h = x1 - x0, y1 - y0
    olcek = en_mm / w           # mm / birim

    deniz = s.lin([(0, "#B8E6EC"), (.55, "#93D5DF"), (1, "#7BC9D6")], 0, y0, 0, y1, kull="userSpaceOnUse", ad="dz")
    s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="{deniz}"/>'
    r = RNG(77)
    dalga = []
    for _ in range(150):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        u = r.uniform(10, 22)
        dalga.append(f"M{f(x)} {f(y)} q{f(u / 4)} {f(-3)} {f(u / 2)} 0 t{f(u / 2)} 0")
    s += f'<path d="{" ".join(dalga)}" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="1.3" stroke-linecap="round"/>'
    s += f'<path d="{T.KARA}" fill="#F6F0E2" stroke="#D3C5A8" stroke-width="1.2" stroke-linejoin="round"/>'
    s += f'<path d="{T.TURKIYE}" fill="#0E4C5A" fill-opacity=".28" transform="translate(5 7)"/>'
    kara = s.lin([(0, "#E6F2C8"), (.5, "#DDEDBA"), (1, "#F1E6BE")], 0, 120, 0, 760, kull="userSpaceOnUse", ad="tr")
    s += f'<path d="{T.TURKIYE}" fill="{kara}"/>'
    # hafif yükselti lekeleri (iç bölgeler)
    lek = s.rad([(0, "#C9DB98", .55), (1, "#C9DB98", 0)], .5, .5, .5, ad="lk")
    for (en, bo, rx, ry) in ((39.3, 35.5, 260, 120), (39.5, 41.5, 230, 110), (37.6, 31.8, 160, 70), (40.6, 37.0, 200, 50)):
        x, y = proje(en, bo)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{rx}" ry="{ry}" fill="{lek}"/>'
    s += "".join(f'<path d="{d}" fill="none" stroke="#5BB7D8" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".9"/>'
                 for d in T.NEHIRLER.values())
    # dağlar (bir durağa çok yakınsa çizilmez)
    duraklar = [proje(d["enlem"], d["boylam"]) for y in yollar for d in y["duraklar"]]
    for i, (ad, en, bo, o) in enumerate(DAGLAR):
        x, y = proje(en, bo)
        if any(math.dist((x, y), p) < 26 for p in duraklar):
            continue
        s += _dag(s, x, y + 8 * o, o * 1.05, 900 + i)
    s += f'<path d="{T.TURKIYE}" fill="none" stroke="{OBS}" stroke-width="2.4" stroke-linejoin="round"/>'
    gol = s.lin([(0, "#6FD0DA"), (1, "#1C97A8")], 0, 0, 0, 1, ad="gl")
    s += "".join(f'<path d="{d}" fill="{gol}" stroke="#0A6C74" stroke-width="1.1" stroke-linejoin="round"/>' for d in T.GOLLER.values())
    # deniz adları
    for (metin, en, bo, boy, don) in (("KARADENİZ", 42.3, 33.7, 30, 0), ("AKDENİZ", 35.55, 31.2, 30, 0),
                                      ("EGE", 38.2, 25.5, 22, -90), ("MARMARA", 40.72, 28.05, 12, 0)):
        x, y = proje(en, bo)
        s += _yazi_aralikli(x, y, metin, boy, "#1F7F90", .62, .38, don=don)
    # yolculuk sırası: Van → Yol 1 → Yol 2 …
    v = proje(baslangic["enlem"], baslangic["boylam"])
    merk = [v] + [rota_merkez(y) for y in yollar]
    s += _yolculuk(s, merk, "#0E4C5A", .5 if len(yollar) <= 6 else .38, 2.2)
    # rotalar
    konum = {}
    for y in yollar:
        pts = rota_noktalari(y)
        s += _rota_cizgisi(pts, y["renk"], 1.3)
    for y in yollar:
        pts = rota_noktalari(y)
        for d in y["duraklar"]:
            x, yy = proje(d["enlem"], d["boylam"])
            s += f'<circle cx="{f(x)}" cy="{f(yy)}" r="5.6" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.7"/>'
            s += f'<circle cx="{f(x)}" cy="{f(yy)}" r="2.3" fill="{y["renk"]}"/>'
        kx, ky = proje(y["kale"]["enlem"], y["kale"]["boylam"])
        s += _kale_simge(kx, ky - 3, y["renk"], 1.25)
        mx, my = rota_merkez(y)
        konum[y["yol"]] = ((mx - x0) * olcek, (my - y0) * olcek)
        if etiketler and y["yol"] in etiketler:
            ex, ey = etiketler[y["yol"]]
            ex, ey = ex / olcek + x0, ey / olcek + y0
            s += (f'<path d="M{f(mx)} {f(my)} L{f(ex)} {f(ey)}" stroke="{OBS}" stroke-width="1.4" stroke-dasharray="3 2.4" stroke-opacity=".8"/>'
                  f'<circle cx="{f(mx)}" cy="{f(my)}" r="3" fill="{OBS}"/>')
    # başlangıç: Van
    s += _bayrak(v[0] + 6, v[1] + 4, 1.05)
    konum["van"] = ((v[0] - x0) * olcek, (v[1] - y0) * olcek)
    s += _pusula(s, x0 + 70, y1 - 72, 40)
    vb = f"{f(x0)} {f(y0)} {f(w)} {f(h)}"
    return s.cikti(vb, cls="harita-svg"), konum, (w * olcek, h * olcek)


# ------------------------------------------------------------------ kapak: gökyüzündeki harita

def kapak_haritasi(onek, yollar, baslangic, tema="aksam"):
    """Kapak için parlak "gökyüzü haritası": yarı saydam Türkiye, ışıyan rotalar, numaralı yıldız rozetleri."""
    s = Svg(onek)
    if tema == "aksam":
        kara_ust, kara_alt, kenar, isik, desen = "#FFF7EA", "#FFD2B8", "#FFFFFF", "#FFE7A8", "#E9A86A"
    else:
        kara_ust, kara_alt, kenar, isik, desen = "#F6FCFF", "#CFE6F7", "#FFFFFF", "#FFFFFF", "#8FB3DA"
    g = s.lin([(0, kara_ust, .96), (1, kara_alt, .93)], 0, 100, 0, 800, kull="userSpaceOnUse", ad="kk")
    s += f'<path d="{T.TURKIYE}" fill="#1B1D26" fill-opacity=".22" transform="translate(9 12)"/>'
    s += f'<path d="{T.TURKIYE}" fill="{g}"/>'
    # iç doku: hafif Selçuklu yıldızları (tek path)
    yd = []
    for i in range(0, int(W), 46):
        for j in range(0, int(H), 46):
            yd.append(cizgi_d(selcuklu_yildizi(i + (23 if (j // 46) % 2 else 0), j, 8), True, 1))
    kl = s.klip(f'<path d="{T.TURKIYE}"/>', ad="tk")
    s += f'<g clip-path="{kl}"><path d="{" ".join(yd)}" fill="none" stroke="{desen}" stroke-opacity=".5" stroke-width="1.7"/></g>'
    for i, (ad, en, bo, o) in enumerate(DAGLAR):
        x, y = proje(en, bo)
        s += _dag(s, x, y + 9 * o, o * 1.15, 950 + i, kar="#FFFFFF", govde="#D9B7C9" if tema == "aksam" else "#B9CDE6",
                  golge="#A985A8" if tema == "aksam" else "#8AA3C8")
    s += f'<path d="{T.TURKIYE}" fill="none" stroke="#1B1D26" stroke-opacity=".8" stroke-width="5.2" stroke-linejoin="round"/>'
    s += f'<path d="{T.TURKIYE}" fill="none" stroke="{kenar}" stroke-width="2.4" stroke-linejoin="round"/>'
    gol = s.lin([(0, "#7EE0E6"), (1, "#13A3A6")], 0, 0, 0, 1, ad="gl")
    s += "".join(f'<path d="{d}" fill="{gol}" stroke="#0A6C74" stroke-width="1.6"/>' for d in T.GOLLER.values())
    v = proje(baslangic["enlem"], baslangic["boylam"])
    if len(yollar) <= 6:
        s += _yolculuk(s, [v] + [rota_merkez(y) for y in yollar], "#1B1D26", .6, 3)
    for y in yollar:
        s += _rota_cizgisi(rota_noktalari(y), y["renk"], 2.0, parlama=isik)
    for y in yollar:
        for d in y["duraklar"]:
            x, yy = proje(d["enlem"], d["boylam"])
            s += f'<circle cx="{f(x)}" cy="{f(yy)}" r="7.5" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.4"/>'
    konum = {}
    for y in yollar:
        mx, my = rota_merkez(y)
        konum[y["yol"]] = (mx, my)
    s += _bayrak(v[0] + 8, v[1] + 6, 1.6)
    return s, konum, v
