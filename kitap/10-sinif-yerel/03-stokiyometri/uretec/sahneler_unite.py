"""Stokiyometri · Dicle Yolu · üniteye özel sahneler, nişan ikonları ve bilgi grafikleri.

kur_ortak bu modüle {{sahne|ad|…}} ve {{info|ad|…}} için ORTAK kütüphaneden (yerel-ortak/cizim) ÖNCE bakar.
Ortak dosyalar değiştirilmez; yeni parçalar burada ortak parçalardan kurulur (TASARIM-SISTEMI.md §6):
  • bant 2100×460 birim (1 birim = 0,1 mm), preserveAspectRatio="xMidYMid slice"
  • sol üst ≈ %55 × %75 gökyüzü/su olarak BOŞ (levha oturur); odak yapı sağ %40'ta
  • ışık yönü bütün çağrılarda aynı; tohum sabit; her Svg öneki benzersiz; konturlu SVG yazısı yok (halolu_yazi)
Yapılar temsilîdir: bugünkü hâlleri (deprem, baraj, restorasyon) hakkında bir şey söylemez.

Yerel parçalar: bazalt_sur (Diyarbakır surları), kemerli_kopru (On Gözlü), malabadi_kopru, rafineri, pompaci,
kazi_alani (Çayönü), kalker_yamac (Hasankeyf), karpuz, cardak, bakir_kap, alaca_kemer (han ve çarşı kemerleri).
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, selcuklu_yildizi, yildiz_noktalari, halolu_yazi, rng as RNG
from cizim import sahne as S, yapilar as Y, molekul as M
from cizim.renkler import OBS, GOL, GOL_K, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ALTIN, ALTIN_K, ALTIN_A, LAJVER, ZUMRUT, GUM, GUM_K, ERGUVAN, ATOM
from cizim.sahneler import W, H, _bitir, _cerceve_golge
from cizim.karakter import turk_bayragi

T = 'font-family="Nunito" font-weight="800"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'

BAZALT = "#3E3B44"
BAZALT_A = "#5B5762"
BAZALT_K = "#26242B"
KALKER = "#E6D3A8"
BAKIR = "#C8743A"

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    "korunum": '<path d="M15 12 H33 V17 H15 Z"/><path d="M17 17 V37 Q17 42 22 42 H26 Q31 42 31 37 V17"/><circle cx="21.5" cy="26" r="3"/><circle cx="27" cy="32" r="3"/><circle cx="21.5" cy="36.5" r="2.4"/><path d="M7 27 h5 M36 27 h5"/>',
    "fidan": '<path d="M24 43 V17"/><path d="M24 27 C16 27 10.5 22 9.5 14 C17 14 22 18.5 24 27 Z"/><path d="M24 27 C32 27 37.5 22 38.5 14 C31 14 26 18.5 24 27 Z"/><path d="M13 43 H35"/><circle cx="24" cy="13" r="2.6"/>',
    "kopru": '<path d="M3 33 Q24 2 45 33"/><path d="M3 33 H45"/><path d="M13 33 Q24 15 35 33"/><path d="M5 41 q4.5 -3 9 0 t9 0 t9 0 t9 0"/>',
    "alev": '<path d="M24 6 C31 15 35 22 33 30 C32 36 28 40 24 40 C20 40 16 36 15 30 C14 24 17.5 20 21 17 C21 22 23 25 25.5 25 C27 19 25.5 13 24 6 Z"/><path d="M13 44 H35"/>',
    "verim": '<path d="M7 33 A17 17 0 0 1 41 33"/><path d="M24 33 L34 21"/><circle cx="24" cy="33" r="2.8"/><path d="M7 33 h4.5 M36.5 33 h4.5 M24 16 v4.5 M12 21 l3.2 3.2 M36 21 l-3.2 3.2"/><path d="M14 41 H34"/>',
    "zincir": '<rect x="3" y="18" width="17" height="12" rx="6"/><rect x="15.5" y="18" width="17" height="12" rx="6"/><rect x="28" y="18" width="17" height="12" rx="6"/>',
}


# ------------------------------------------------------------------ yardımcılar

def kure(s, x, y, r, renk, cizgi=True):
    """Hacimli atom küresi (radyal gradyan + parlama)."""
    if renk.upper() in ("#F3F5F8", "#FFFFFF"):
        st = [(0, "#FFFFFF"), (.4, "#F4F7FA"), (.75, "#C9D3DE"), (1, "#7D8B9C")]
    else:
        st = [(0, acik(renk, .7)), (.3, acik(renk, .22)), (.68, renk), (1, koyu(renk, .5))]
    g = s.rad(st, cx=.5, cy=.5, r=.56, fx=.34, fy=.3, ad="ku")
    c = f' stroke="{koyu(renk, .6) if renk.upper() != "#F3F5F8" else "#5E6B7A"}" stroke-width="{f(max(.6, r * .07), 2)}"' if cizgi else ""
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{g}"{c}/>'
            f'<ellipse cx="{f(x - r * .35)}" cy="{f(y - r * .4)}" rx="{f(r * .26)}" ry="{f(r * .16)}" fill="#FFFFFF" opacity=".85" transform="rotate(-35 {f(x - r * .35)} {f(y - r * .4)})"/>')


def bag(x1, y1, x2, y2, k=4, renk="#8592A3"):
    return f'<path d="M{f(x1)} {f(y1)} L{f(x2)} {f(y2)}" stroke="{OBS}" stroke-width="{f(k + 2.2)}" stroke-linecap="round"/><path d="M{f(x1)} {f(y1)} L{f(x2)} {f(y2)}" stroke="{renk}" stroke-width="{f(k)}" stroke-linecap="round"/>'


def molekul_grup(s, tur, x, y, r=12):
    """Basit tanecik çizimleri (şema için): H2, O2, H2O, CuO, Cu, CO2, CH4."""
    H_, O_, C_, Cu = ATOM["H"], ATOM["O"], ATOM["C"], ATOM["Cu"]
    if tur == "H2":
        return bag(x - r * .7, y, x + r * .7, y, r * .35) + kure(s, x - r * .7, y, r * .8, H_) + kure(s, x + r * .7, y, r * .8, H_)
    if tur == "O2":
        return bag(x - r * .8, y, x + r * .8, y, r * .35, "#E58B7C") + kure(s, x - r * .8, y, r, O_) + kure(s, x + r * .8, y, r, O_)
    if tur == "H2O":
        return (bag(x, y, x - r * 1.05, y + r * .75, r * .3) + bag(x, y, x + r * 1.05, y + r * .75, r * .3)
                + kure(s, x - r * 1.05, y + r * .75, r * .72, H_) + kure(s, x + r * 1.05, y + r * .75, r * .72, H_) + kure(s, x, y, r, O_))
    if tur == "CuO":
        return bag(x - r * .85, y, x + r * .85, y, r * .35, "#D9A07A") + kure(s, x - r * .85, y, r * 1.12, Cu) + kure(s, x + r * .9, y, r * .95, O_)
    if tur == "Cu":
        return kure(s, x, y, r * 1.12, Cu)
    if tur == "CO2":
        return (bag(x - r * 1.5, y, x + r * 1.5, y, r * .35) + kure(s, x - r * 1.5, y, r * .9, O_) + kure(s, x + r * 1.5, y, r * .9, O_) + kure(s, x, y, r * .95, C_))
    return ""


# ------------------------------------------------------------------ yerel moleküller ({{mol}} için: kur.py)

YEREL_MOLEKUL = {
    "H2": ([("H", (-.37, 0, 0)), ("H", (.37, 0, 0))], [(0, 1, 1)]),
    "C4H10": None,   # aşağıda kurulur
}


def _butan():
    A, Bg = [], []
    cs = [(-1.9, -.3, 0), (-.64, .45, 0), (.64, -.3, 0), (1.9, .45, 0)]
    for c in cs:
        A.append(("C", c))
    for i in range(3):
        Bg.append((i, i + 1, 1))
    hidro = [(0, (-2.5, .45, .55)), (0, (-2.5, .45, -.55)), (0, (-1.9, -1.35, 0)),
             (1, (-.64, 1.1, .85)), (1, (-.64, 1.1, -.85)), (2, (.64, -.95, .85)), (2, (.64, -.95, -.85)),
             (3, (2.5, -.25, .55)), (3, (2.5, -.25, -.55)), (3, (1.9, 1.5, 0))]
    for ci, p in hidro:
        A.append(("H", p))
        Bg.append((ci, len(A) - 1, 1))
    return A, Bg


YEREL_MOLEKUL["C4H10"] = _butan()


def yerel_molekul_svg(onek, ad, donus=(0, 0, 0), etiket=False, olcek=40, pay=4):
    s = Svg(onek)
    A, Bg = YEREL_MOLEKUL[ad]
    govde, (x0, y0, x1, y1) = M.molekul_ciz(s, A, Bg, donus, olcek, etiket=etiket)
    s += govde
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(x0 - pay)} {f(y0 - pay)} {f(x1 - x0 + 2 * pay)} {f(y1 - y0 + 2 * pay)}" class="mol">{s.govde()}</svg>'


def _mol_ic(s, ad, donus, olcek):
    """Molekülü çizim içine gömmek için (yer gölgesiz) gövde metni."""
    if ad in YEREL_MOLEKUL:
        A, Bg = YEREL_MOLEKUL[ad]
    else:
        A, Bg = M._geometri(ad)
    return M.molekul_ciz(s, A, Bg, donus, olcek, yer_golgesi=False)[0]


# ------------------------------------------------------------------ yerel yapı parçaları

def bazalt_sur(s, x0, x1, taban, h, burclar=(), tohum=1, renk=BAZALT, isik=-1, ust_isik="#C9A27A", mazgal=True, tas=True):
    """Diyarbakır surları (temsilî): bazalt duvar, mazgallar, yuvarlak/çokgen burçlar. taban: fonksiyon x→y ya da sayı."""
    r = RNG(tohum)
    tb = taban if callable(taban) else (lambda x, _t=taban: _t)
    o = []
    n = max(8, int((x1 - x0) / 24))
    ust = [(x0 + (x1 - x0) * i / n, tb(x0 + (x1 - x0) * i / n) - h) for i in range(n + 1)]
    alt = [(x, tb(x)) for x, _ in reversed(ust)]
    g = s.lin([(0, acik(renk, .14)), (.55, renk), (1, koyu(renk, .25))], 0, min(p[1] for p in ust), 0, max(p[1] for p in alt), kull="userSpaceOnUse", ad="bs")
    o.append(f'<path d="{cizgi_d(ust + alt, True)}" fill="{g}"/>')
    if tas:  # taş sıraları
        for k in range(1, 4):
            hat = [(x, y + h * k / 4) for x, y in ust]
            o.append(f'<path d="{cizgi_d(hat)}" fill="none" stroke="{koyu(renk, .35)}" stroke-width="{f(max(.8, h * .025))}" opacity=".55"/>')
        for i in range(int((x1 - x0) / (h * .5)) + 1):
            x = x0 + i * h * .5 + r.uniform(-4, 4)
            k = r.randint(0, 3)
            y = tb(x) - h + h * k / 4
            o.append(f'<path d="M{f(x)} {f(y)} v{f(h / 4)}" stroke="{koyu(renk, .35)}" stroke-width="{f(max(.7, h * .02))}" opacity=".45"/>')
    o.append(f'<path d="{cizgi_d(ust)}" fill="none" stroke="{ust_isik}" stroke-width="{f(max(1.2, h * .05))}" opacity=".65"/>')
    if mazgal:
        mz = h * .16
        x = x0
        while x < x1 - mz:
            y = tb(x) - h
            o.append(f'<rect x="{f(x)}" y="{f(y - mz)}" width="{f(mz * .85)}" height="{f(mz + 1)}" fill="{acik(renk, .06)}"/>'
                     f'<path d="M{f(x)} {f(y - mz)} h{f(mz * .85)}" stroke="{ust_isik}" stroke-width="{f(max(.8, h * .03))}" opacity=".6"/>')
            x += mz * 1.65
    for bx, bh, bw in burclar:
        y0 = tb(bx)
        gb = s.lin([(0, acik(renk, .22)), (.45, renk), (1, koyu(renk, .38))], 0, 0, 1, 0, ad="bb") if isik < 0 else \
            s.lin([(0, koyu(renk, .38)), (.55, renk), (1, acik(renk, .22))], 0, 0, 1, 0, ad="bb")
        o.append(f'<path d="M{f(bx - bw / 2)} {f(y0)} V{f(y0 - bh)} H{f(bx + bw / 2)} V{f(y0)} Z" fill="{gb}"/>')
        for k in range(1, 5):
            o.append(f'<path d="M{f(bx - bw / 2)} {f(y0 - bh * k / 5)} H{f(bx + bw / 2)}" stroke="{koyu(renk, .35)}" stroke-width="{f(max(.7, bh * .016))}" opacity=".5"/>')
        o.append(f'<path d="M{f(bx - bw / 2 - bw * .05)} {f(y0 - bh)} H{f(bx + bw / 2 + bw * .05)}" stroke="{ust_isik}" stroke-width="{f(max(1.2, bh * .04))}" opacity=".7"/>')
        for k in range(4):
            o.append(f'<rect x="{f(bx - bw / 2 + k * bw * .27)}" y="{f(y0 - bh - bw * .16)}" width="{f(bw * .17)}" height="{f(bw * .17 + 1)}" fill="{acik(renk, .08)}"/>')
        o.append(f'<path d="M{f(bx - bw * .06)} {f(y0 - bh * .62)} v{f(-bh * .14)} q{f(bw * .06)} {f(-bh * .05)} {f(bw * .12)} 0 v{f(bh * .14)} Z" fill="{BAZALT_K}"/>')
        o.append(f'<path d="M{f(bx - bw / 2)} {f(y0 - bh * .3)} H{f(bx + bw / 2)}" stroke="{KALKER}" stroke-width="{f(max(1, bh * .03))}" opacity=".55"/>')
    return "".join(o)


def kemerli_kopru(s, x0, x1, y_ust, y_su, n, tohum=1, renk=BAZALT, sivri=True, ust_isik="#D9B98A", ayak_ok=True):
    """Çok gözlü taş köprü (On Gözlü Köprü esinli, temsilî): korkuluklu yol, n göz, sel yaranlı ayaklar."""
    o = []
    w = x1 - x0
    kal = (y_su - y_ust) * .2
    g = s.lin([(0, acik(renk, .18)), (.5, renk), (1, koyu(renk, .3))], 0, y_ust, 0, y_su, kull="userSpaceOnUse", ad="kk")
    yol = f'M{f(x0)} {f(y_ust)} H{f(x1)} V{f(y_su)} H{f(x0)} Z'
    gozler = []
    acik_w = w / n
    for i in range(n):
        cx = x0 + acik_w * (i + .5)
        aw = acik_w * .36
        yt = y_ust + kal * 1.25
        if sivri:
            gozler.append(f'M{f(cx - aw)} {f(y_su)} V{f(yt + aw * .55)} Q{f(cx - aw)} {f(yt + aw * .05)} {f(cx)} {f(yt)} Q{f(cx + aw)} {f(yt + aw * .05)} {f(cx + aw)} {f(yt + aw * .55)} V{f(y_su)} Z')
        else:
            gozler.append(f'M{f(cx - aw)} {f(y_su)} V{f(yt + aw)} A{f(aw)} {f(aw)} 0 0 1 {f(cx + aw)} {f(yt + aw)} V{f(y_su)} Z')
    kl = s.maske(f'<rect x="{f(x0 - 10)}" y="{f(y_ust - 40)}" width="{f(w + 20)}" height="{f(y_su - y_ust + 80)}" fill="#FFF"/>'
                 + "".join(f'<path d="{d}" fill="#000"/>' for d in gozler), ad="km")
    o.append(f'<path d="{yol}" fill="{g}" mask="{kl}"/>')
    # taş derzleri
    for k in range(1, 3):
        o.append(f'<path d="M{f(x0)} {f(y_ust + kal * .45 * k)} H{f(x1)}" stroke="{koyu(renk, .4)}" stroke-width="1.4" opacity=".5"/>')
    for d in gozler:
        o.append(f'<path d="{d}" fill="none" stroke="{koyu(renk, .45)}" stroke-width="2.4"/>')
    o.append(f'<path d="M{f(x0 - 6)} {f(y_ust)} H{f(x1 + 6)}" stroke="{ust_isik}" stroke-width="3.4" opacity=".75"/>')
    o.append(f'<path d="M{f(x0 - 6)} {f(y_ust - kal * .55)} H{f(x1 + 6)}" stroke="{acik(renk, .1)}" stroke-width="{f(kal * .5)}"/>')
    o.append(f'<path d="M{f(x0 - 6)} {f(y_ust - kal * .78)} H{f(x1 + 6)}" stroke="{ust_isik}" stroke-width="2.2" opacity=".7"/>')
    if ayak_ok:
        for i in range(1, n):
            cx = x0 + acik_w * i
            aw = acik_w * .14
            o.append(f'<path d="M{f(cx - aw)} {f(y_su)} L{f(cx)} {f(y_su - aw * 2.2)} L{f(cx + aw)} {f(y_su)} Z" fill="{koyu(renk, .2)}"/>')
    return "".join(o)


def malabadi_kopru(s, x0, x1, y_su, h, renk="#D3B583", isik=-1):
    """Malabadi Köprüsü esinli (temsilî): sivri büyük ana kemer, yanlarda küçük gözler, kambur (eğimli) yol."""
    o = []
    w = x1 - x0
    cx = x0 + w * .5
    tepe = y_su - h
    g = s.lin([(0, acik(renk, .25)), (.6, renk), (1, koyu(renk, .25))], 0, tepe, 0, y_su, kull="userSpaceOnUse", ad="mk")
    govde = (f'M{f(x0)} {f(y_su)} L{f(x0)} {f(y_su - h * .34)} Q{f(x0 + w * .25)} {f(tepe + h * .06)} {f(cx)} {f(tepe)} '
             f'Q{f(x1 - w * .25)} {f(tepe + h * .06)} {f(x1)} {f(y_su - h * .34)} L{f(x1)} {f(y_su)} Z')
    aw = w * .27
    ana = (f'M{f(cx - aw)} {f(y_su)} V{f(y_su - h * .25)} Q{f(cx - aw)} {f(tepe + h * .3)} {f(cx)} {f(tepe + h * .19)} '
           f'Q{f(cx + aw)} {f(tepe + h * .3)} {f(cx + aw)} {f(y_su - h * .25)} V{f(y_su)} Z')
    kucuk = []
    for sx in (-1, 1):
        kx = cx + sx * w * .41
        kw = w * .045
        kucuk.append(f'M{f(kx - kw)} {f(y_su)} V{f(y_su - h * .2)} Q{f(kx)} {f(y_su - h * .36)} {f(kx + kw)} {f(y_su - h * .2)} V{f(y_su)} Z')
    mk = s.maske(f'<rect x="{f(x0 - 20)}" y="{f(tepe - 40)}" width="{f(w + 40)}" height="{f(h + 60)}" fill="#FFF"/>'
                 + f'<path d="{ana}" fill="#000"/>' + "".join(f'<path d="{d}" fill="#000"/>' for d in kucuk), ad="mm")
    o.append(f'<path d="{govde}" fill="{g}" mask="{mk}"/>')
    # kesme taş sıraları (kemer boyunca)
    for k in range(1, 7):
        t = k / 7
        o.append(f'<path d="M{f(x0)} {f(y_su - h * .34 * t)} H{f(x0 + w * .16)} M{f(x1 - w * .16)} {f(y_su - h * .34 * t)} H{f(x1)}" stroke="{koyu(renk, .3)}" stroke-width="1.6" opacity=".5"/>')
    for k in range(13):
        a = math.pi * (k + .5) / 13
        px = cx - aw * math.cos(a)
        py = (tepe + h * .3) + (y_su - h * .25 - (tepe + h * .3)) * (1 - math.sin(a)) * .0 - h * .1 * math.sin(a)
        o.append(f'<path d="M{f(px)} {f(py + h * .08)} l{f(-math.cos(a) * h * .07)} {f(-math.sin(a) * h * .07)}" stroke="{koyu(renk, .35)}" stroke-width="1.6" opacity=".5"/>')
    o.append(f'<path d="{ana}" fill="none" stroke="{koyu(renk, .4)}" stroke-width="3"/>')
    o.append(f'<path d="{ana}" fill="none" stroke="{acik(renk, .4)}" stroke-width="5" transform="translate(0 -9) scale(1 1)" opacity=".0"/>')
    for d in kucuk:
        o.append(f'<path d="{d}" fill="none" stroke="{koyu(renk, .4)}" stroke-width="2.2"/>')
    # korkuluk ve yol çizgisi
    o.append(f'<path d="M{f(x0 - 30)} {f(y_su - h * .34)} L{f(x0)} {f(y_su - h * .34)} Q{f(x0 + w * .25)} {f(tepe + h * .06)} {f(cx)} {f(tepe)} '
             f'Q{f(x1 - w * .25)} {f(tepe + h * .06)} {f(x1)} {f(y_su - h * .34)} L{f(x1 + 30)} {f(y_su - h * .34)}" fill="none" stroke="{acik(renk, .45)}" stroke-width="5"/>')
    gol = f'<path d="M{f(cx)} {f(tepe)} Q{f(x1 - w * .25)} {f(tepe + h * .06)} {f(x1)} {f(y_su - h * .34)} L{f(x1)} {f(y_su)} L{f(cx + aw)} {f(y_su)} V{f(y_su - h * .25)} Q{f(cx + aw)} {f(tepe + h * .3)} {f(cx)} {f(tepe + h * .19)} Z"'
    o.append(f'<path d={gol} fill="#1B1D26" opacity="{".14" if isik < 0 else "0"}"/>')
    return "".join(o)


def rafineri(s, x, y, o_=1.0, isik=-1, gece=False):
    """Temsilî rafineri: damıtma kuleleri, depolama tankları, borular, meşale (bacadan alev). Kurum logosu YOK."""
    k = o_
    out = []
    metal = s.lin([(0, "#E9EEF2"), (.45, "#B8C3CC"), (1, "#7C8894")], 0, 0, 1, 0, ad="rf")
    tank = s.lin([(0, "#F4F1EA"), (.6, "#D9D3C7"), (1, "#A8A196")], 0, 0, 1, 0, ad="rt")
    # tanklar
    for dx, w_, h_ in ((-260, 150, 70), (-90, 120, 60), (300, 160, 76)):
        tx = x + dx * k
        out.append(f'<rect x="{f(tx - w_ * k / 2)}" y="{f(y - h_ * k)}" width="{f(w_ * k)}" height="{f(h_ * k)}" fill="{tank}" stroke="#5E6670" stroke-width="{f(2 * k)}"/>'
                   f'<ellipse cx="{f(tx)}" cy="{f(y - h_ * k)}" rx="{f(w_ * k / 2)}" ry="{f(10 * k)}" fill="#EDEAE2" stroke="#5E6670" stroke-width="{f(2 * k)}"/>'
                   f'<path d="M{f(tx - w_ * k / 2)} {f(y - h_ * k * .5)} H{f(tx + w_ * k / 2)}" stroke="{MER}" stroke-width="{f(4 * k)}" opacity=".8"/>')
    # kuleler
    for dx, w_, h_ in ((40, 46, 300), (110, 36, 230), (175, 30, 180)):
        kx = x + dx * k
        out.append(f'<rect x="{f(kx - w_ * k / 2)}" y="{f(y - h_ * k)}" width="{f(w_ * k)}" height="{f(h_ * k)}" rx="{f(w_ * k / 2)}" fill="{metal}" stroke="#4E5660" stroke-width="{f(2 * k)}"/>')
        for j in range(1, int(h_ / 46)):
            yy = y - h_ * k + j * 46 * k
            out.append(f'<path d="M{f(kx - w_ * k / 2 - 8 * k)} {f(yy)} h{f(w_ * k + 16 * k)}" stroke="#4E5660" stroke-width="{f(2.4 * k)}"/>')
        out.append(f'<path d="M{f(kx + w_ * k / 2 + 6 * k)} {f(y)} V{f(y - h_ * k + 20 * k)}" stroke="#4E5660" stroke-width="{f(1.6 * k)}" stroke-dasharray="{f(4 * k)} {f(3 * k)}"/>')
    # borular
    for j in range(3):
        yy = y - (24 + j * 18) * k
        out.append(f'<path d="M{f(x - 330 * k)} {f(yy)} H{f(x + 380 * k)}" stroke="{["#9AA6B0", "#C9A86A", "#7C8894"][j]}" stroke-width="{f(5 * k)}"/>')
    # meşale (flare) bacası + alev
    fx = x + 250 * k
    fy = y - 360 * k
    out.append(f'<path d="M{f(fx)} {f(y)} V{f(fy)}" stroke="#5E6670" stroke-width="{f(9 * k)}"/>')
    al = s.rad([(0, "#FFF6C8", .95), (.35, "#FFC14A", .7), (.7, "#FF7A3D", .25), (1, "#FF7A3D", 0)], fx, fy - 30 * k, 90 * k, kull="userSpaceOnUse", ad="al")
    out.append(f'<circle cx="{f(fx)}" cy="{f(fy - 30 * k)}" r="{f(90 * k)}" fill="{al}"/>'
               f'<path d="M{f(fx - 12 * k)} {f(fy)} Q{f(fx - 20 * k)} {f(fy - 40 * k)} {f(fx + 2 * k)} {f(fy - 76 * k)} Q{f(fx + 6 * k)} {f(fy - 46 * k)} {f(fx + 16 * k)} {f(fy - 30 * k)} Q{f(fx + 14 * k)} {f(fy - 10 * k)} {f(fx + 10 * k)} {f(fy)} Z" fill="#FF8A3D"/>'
               f'<path d="M{f(fx - 5 * k)} {f(fy)} Q{f(fx - 8 * k)} {f(fy - 24 * k)} {f(fx + 1 * k)} {f(fy - 44 * k)} Q{f(fx + 7 * k)} {f(fy - 20 * k)} {f(fx + 5 * k)} {f(fy)} Z" fill="#FFE08A"/>')
    # ışıklar
    if gece:
        for j in range(14):
            out.append(f'<circle cx="{f(x + (-300 + j * 48) * k)}" cy="{f(y - (40 + (j % 3) * 60) * k)}" r="{f(3 * k)}" fill="#FFE08A"/>')
    return "".join(out)


def pompaci(x, y, o=1.0, renk="#2E2A33", aci=-8):
    """Petrol kuyusu pompası (temsilî silüet): kaide, A ayak, sallanan kol, at başı, karşı ağırlık."""
    k = o
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(k, 3)})" fill="{renk}" stroke="{renk}">'
            f'<rect x="-46" y="-6" width="92" height="6" stroke="none"/>'
            f'<path d="M-6 -6 L0 -46 L6 -6" fill="none" stroke-width="5"/>'
            f'<g transform="rotate({aci} 0 -46)"><rect x="-44" y="-50" width="88" height="8" rx="2" stroke="none"/>'
            f'<path d="M38 -54 Q50 -46 40 -30 L34 -38 Z" stroke="none"/><path d="M40 -32 V-6" fill="none" stroke-width="2"/></g>'
            f'<path d="M-34 -6 L-30 -26 L-22 -26 L-20 -6 Z" stroke="none"/><circle cx="-26" cy="-26" r="9" stroke="none"/>'
            f'</g>')


def kazi_alani(s, x, y, w, h, tohum=1):
    """Çayönü kazı alanı (temsilî): açık toprak açmalar, ızgara planlı taş temeller, ölçü çubukları, gölgelik."""
    r = RNG(tohum)
    o = []
    gz = s.lin([(0, "#E3C795"), (1, "#C9A06A")], 0, y - h, 0, y, kull="userSpaceOnUse", ad="kz")
    o.append(f'<path d="M{f(x)} {f(y)} L{f(x + w * .08)} {f(y - h)} L{f(x + w * .92)} {f(y - h)} L{f(x + w)} {f(y)} Z" fill="{gz}"/>')
    # açmalar (kareler)
    for i in range(4):
        for j in range(2):
            ax = x + w * (.12 + i * .2) + j * w * .03
            ay = y - h * (.88 - j * .45)
            aw, ah = w * .17, h * .36
            o.append(f'<path d="M{f(ax)} {f(ay)} h{f(aw)} l{f(-w * .012)} {f(ah)} h{f(-aw + w * .024)} Z" fill="#B38452" stroke="#8C643A" stroke-width="2"/>')
            for k in range(3):  # ızgara planlı taş duvar dizileri
                yy = ay + ah * (.25 + k * .25)
                o.append(f'<path d="M{f(ax + aw * .1)} {f(yy)} h{f(aw * .8)}" stroke="#E9E1D2" stroke-width="{f(h * .045)}" stroke-dasharray="{f(h * .05)} {f(h * .02)}" stroke-linecap="round"/>')
    # ölçü çubukları
    for i in range(3):
        px = x + w * (.1 + i * .38)
        o.append(f'<path d="M{f(px)} {f(y - h * .98)} v{f(-h * .5)}" stroke="#F5F2EA" stroke-width="4"/>'
                 f'<path d="M{f(px)} {f(y - h * .98)} v{f(-h * .5)}" stroke="{MER}" stroke-width="4" stroke-dasharray="{f(h * .08)} {f(h * .08)}"/>')
    # gölgelik (çadır bezi)
    gx = x + w * .62
    o.append(f'<path d="M{f(gx - w * .2)} {f(y - h * 1.75)} L{f(gx + w * .2)} {f(y - h * 1.85)} L{f(gx + w * .22)} {f(y - h * 1.62)} L{f(gx - w * .18)} {f(y - h * 1.52)} Z" fill="#F2E7D0" stroke="#8C643A" stroke-width="2"/>'
             f'<path d="M{f(gx - w * .19)} {f(y - h * 1.6)} V{f(y - h * .95)} M{f(gx + w * .21)} {f(y - h * 1.7)} V{f(y - h * 1.0)}" stroke="#6E4A2C" stroke-width="4"/>')
    for _ in range(14):  # toprak yığınları, taşlar
        px = x + r.uniform(.02, .98) * w
        o.append(f'<ellipse cx="{f(px)}" cy="{f(y - r.uniform(0, .1) * h)}" rx="{f(r.uniform(4, 10))}" ry="{f(r.uniform(2, 4))}" fill="{r.choice(["#9C7A54", "#B9935F", "#7E6A58"])}"/>')
    return "".join(o)


def kalker_yamac(s, x0, x1, y_alt, h, tohum=1, renk=KALKER, isik=-1, magara=14):
    """Kireç taşı (kalker) yamacı: tabakalı kaya, kemerli mağara ağızları (temsilî)."""
    r = RNG(tohum)
    o = []
    n = 26
    ust = []
    for i in range(n + 1):
        t = i / n
        yy = y_alt - h * (.62 + .38 * math.sin(math.pi * min(1, t * 1.1)) ** .5) + r.uniform(-h * .03, h * .03)
        ust.append((x0 + (x1 - x0) * t, yy))
    g = s.lin([(0, acik(renk, .2)), (.5, renk), (1, koyu(renk, .25))], 0, y_alt - h, 0, y_alt, kull="userSpaceOnUse", ad="ky")
    o.append(f'<path d="{cizgi_d([(x0, y_alt)] + ust + [(x1, y_alt)], True)}" fill="{g}"/>')
    for k in range(1, 8):  # tabakalar
        yy = y_alt - h * k / 8.5
        o.append(f'<path d="M{f(x0)} {f(yy)} C{f(x0 + (x1 - x0) * .3)} {f(yy - 6)} {f(x0 + (x1 - x0) * .7)} {f(yy + 6)} {f(x1)} {f(yy - 3)}" stroke="{koyu(renk, .22)}" stroke-width="2" fill="none" opacity=".5"/>')
    for i in range(10):  # dikey çatlaklar
        px = x0 + r.uniform(.05, .95) * (x1 - x0)
        o.append(f'<path d="M{f(px)} {f(y_alt - h * r.uniform(.4, .9))} l{f(r.uniform(-8, 8))} {f(h * r.uniform(.15, .35))}" stroke="{koyu(renk, .3)}" stroke-width="2" opacity=".5"/>')
    for _ in range(magara):  # mağara ağızları
        px = x0 + r.uniform(.08, .92) * (x1 - x0)
        py = y_alt - h * r.uniform(.15, .7)
        mw = r.uniform(14, 26)
        o.append(f'<path d="M{f(px - mw / 2)} {f(py)} V{f(py - mw * .5)} A{f(mw / 2)} {f(mw / 2)} 0 0 1 {f(px + mw / 2)} {f(py - mw * .5)} V{f(py)} Z" fill="#4A3B2E"/>'
                 f'<path d="M{f(px - mw / 2 - 2)} {f(py + 1)} h{f(mw + 4)}" stroke="{acik(renk, .3)}" stroke-width="2"/>')
    if isik < 0:
        o.append(f'<path d="{cizgi_d([(x0 + (x1 - x0) * .55, y_alt)] + ust[int(n * .55):] + [(x1, y_alt)], True)}" fill="#3B2A55" opacity=".16"/>')
    return "".join(o)


def karpuz(x, y, r, kesik=False):
    """Diyarbakır karpuzu: koyu yeşil, açık yeşil çizgili; kesik=True dilim."""
    if kesik:
        return (f'<path d="M{f(x - r)} {f(y)} A{f(r)} {f(r * .8)} 0 0 0 {f(x + r)} {f(y)} Z" fill="#2F7A3A"/>'
                f'<path d="M{f(x - r * .9)} {f(y)} A{f(r * .9)} {f(r * .7)} 0 0 0 {f(x + r * .9)} {f(y)} Z" fill="#F4F1D8"/>'
                f'<path d="M{f(x - r * .8)} {f(y)} A{f(r * .8)} {f(r * .62)} 0 0 0 {f(x + r * .8)} {f(y)} Z" fill="#E8434B"/>'
                + "".join(f'<ellipse cx="{f(x + dx * r)}" cy="{f(y + dy * r)}" rx="{f(r * .05)}" ry="{f(r * .08)}" fill="#1B1D26"/>' for dx, dy in ((-.4, .2), (0, .32), (.4, .2), (-.18, .45), (.2, .46))))
    cz = "".join(f'<path d="M{f(x + k * r * .3)} {f(y - r * .55)} Q{f(x + k * r * .42)} {f(y)} {f(x + k * r * .3)} {f(y + r * .55)}" stroke="#7DBE55" stroke-width="{f(r * .1)}" fill="none" opacity=".8"/>' for k in (-2, -1, 0, 1, 2))
    return (f'<ellipse cx="{f(x)}" cy="{f(y + r * .55)}" rx="{f(r * 1.1)}" ry="{f(r * .18)}" fill="#1B1D26" opacity=".2"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r * 1.05)}" ry="{f(r * .62)}" fill="#2E6B34"/>{cz}'
            f'<ellipse cx="{f(x - r * .35)}" cy="{f(y - r * .25)}" rx="{f(r * .3)}" ry="{f(r * .12)}" fill="#FFFFFF" opacity=".3"/>')


def cardak(s, x, y, w, h):
    """Bostan çardağı: dört direk, dal-yaprak örtü."""
    o = [f'<path d="M{f(x - w / 2)} {f(y)} V{f(y - h)} M{f(x + w / 2)} {f(y)} V{f(y - h)} M{f(x - w * .2)} {f(y + 6)} V{f(y - h + 4)} M{f(x + w * .2)} {f(y + 6)} V{f(y - h + 4)}" stroke="#6B4A2E" stroke-width="6"/>',
         f'<path d="M{f(x - w * .62)} {f(y - h)} Q{f(x)} {f(y - h * 1.32)} {f(x + w * .62)} {f(y - h)} L{f(x + w * .55)} {f(y - h * .9)} Q{f(x)} {f(y - h * 1.12)} {f(x - w * .55)} {f(y - h * .9)} Z" fill="#7E9A4A"/>']
    r = RNG(int(x))
    for _ in range(26):
        px = x + r.uniform(-.6, .6) * w
        o.append(f'<ellipse cx="{f(px)}" cy="{f(y - h * r.uniform(.95, 1.16))}" rx="{f(r.uniform(8, 16))}" ry="{f(r.uniform(4, 7))}" fill="{r.choice(["#5E8A3A", "#93B65A", "#6F9A44"])}"/>')
    return "".join(o)


def bakir_kap(s, tur, x, y, h, aci=0):
    """Bakır kaplar (temsilî): kazan, ibrik, sini, tava, cezve. (x, y) taban ortası."""
    g = s.lin([(0, "#8A4A1E"), (.28, "#E8A26A"), (.5, "#F6C79A"), (.72, BAKIR), (1, "#7A3E18")], 0, 0, 1, 0, ad="bk")
    cz = "#5A2E12"
    k = h / 100
    if tur == "kazan":
        d = f'M{f(x - 48 * k)} {f(y - 70 * k)} C{f(x - 56 * k)} {f(y - 10 * k)} {f(x - 30 * k)} {f(y)} {f(x)} {f(y)} C{f(x + 30 * k)} {f(y)} {f(x + 56 * k)} {f(y - 10 * k)} {f(x + 48 * k)} {f(y - 70 * k)} Z'
        return (f'<path d="{d}" fill="{g}" stroke="{cz}" stroke-width="{f(2.4 * k)}"/>'
                f'<ellipse cx="{f(x)}" cy="{f(y - 70 * k)}" rx="{f(50 * k)}" ry="{f(9 * k)}" fill="#7A3E18" stroke="{cz}" stroke-width="{f(2.4 * k)}"/>'
                f'<path d="M{f(x - 46 * k)} {f(y - 66 * k)} Q{f(x)} {f(y - 108 * k)} {f(x + 46 * k)} {f(y - 66 * k)}" fill="none" stroke="#3A2A20" stroke-width="{f(3 * k)}"/>'
                f'<path d="M{f(x - 40 * k)} {f(y - 40 * k)} Q{f(x)} {f(y - 30 * k)} {f(x + 40 * k)} {f(y - 40 * k)}" fill="none" stroke="#F6C79A" stroke-width="{f(2 * k)}" opacity=".7"/>')
    if tur == "ibrik":
        d = (f'M{f(x - 20 * k)} {f(y)} C{f(x - 36 * k)} {f(y - 30 * k)} {f(x - 30 * k)} {f(y - 56 * k)} {f(x - 10 * k)} {f(y - 66 * k)} '
             f'L{f(x - 8 * k)} {f(y - 88 * k)} L{f(x + 8 * k)} {f(y - 88 * k)} L{f(x + 10 * k)} {f(y - 66 * k)} C{f(x + 30 * k)} {f(y - 56 * k)} {f(x + 36 * k)} {f(y - 30 * k)} {f(x + 20 * k)} {f(y)} Z')
        return (f'<path d="M{f(x + 26 * k)} {f(y - 40 * k)} Q{f(x + 50 * k)} {f(y - 60 * k)} {f(x + 54 * k)} {f(y - 90 * k)}" fill="none" stroke="{cz}" stroke-width="{f(6 * k)}" stroke-linecap="round"/>'
                f'<path d="M{f(x + 26 * k)} {f(y - 40 * k)} Q{f(x + 50 * k)} {f(y - 60 * k)} {f(x + 54 * k)} {f(y - 90 * k)}" fill="none" stroke="{BAKIR}" stroke-width="{f(3.4 * k)}" stroke-linecap="round"/>'
                f'<path d="M{f(x - 26 * k)} {f(y - 60 * k)} Q{f(x - 48 * k)} {f(y - 50 * k)} {f(x - 28 * k)} {f(y - 22 * k)}" fill="none" stroke="{cz}" stroke-width="{f(4 * k)}"/>'
                f'<path d="{d}" fill="{g}" stroke="{cz}" stroke-width="{f(2.4 * k)}"/>'
                f'<ellipse cx="{f(x)}" cy="{f(y - 90 * k)}" rx="{f(11 * k)}" ry="{f(4 * k)}" fill="#7A3E18" stroke="{cz}" stroke-width="{f(2 * k)}"/>')
    if tur == "sini":
        return (f'<ellipse cx="{f(x)}" cy="{f(y - 50 * k)}" rx="{f(46 * k)}" ry="{f(46 * k)}" fill="{g}" stroke="{cz}" stroke-width="{f(2.4 * k)}" transform="rotate({aci} {f(x)} {f(y - 50 * k)})"/>'
                f'<ellipse cx="{f(x)}" cy="{f(y - 50 * k)}" rx="{f(34 * k)}" ry="{f(34 * k)}" fill="none" stroke="#7A3E18" stroke-width="{f(2 * k)}"/>'
                f'<path d="{cizgi_d(selcuklu_yildizi(x, y - 50 * k, 22 * k), True)}" fill="none" stroke="#7A3E18" stroke-width="{f(2 * k)}"/>')
    if tur == "tava":
        return (f'<path d="M{f(x - 40 * k)} {f(y - 18 * k)} Q{f(x)} {f(y + 6 * k)} {f(x + 40 * k)} {f(y - 18 * k)} Z" fill="{g}" stroke="{cz}" stroke-width="{f(2.4 * k)}"/>'
                f'<path d="M{f(x + 40 * k)} {f(y - 18 * k)} L{f(x + 80 * k)} {f(y - 26 * k)}" stroke="{cz}" stroke-width="{f(6 * k)}" stroke-linecap="round"/>')
    if tur == "cezve":
        return (f'<path d="M{f(x - 16 * k)} {f(y)} L{f(x - 12 * k)} {f(y - 40 * k)} L{f(x + 12 * k)} {f(y - 40 * k)} L{f(x + 16 * k)} {f(y)} Z" fill="{g}" stroke="{cz}" stroke-width="{f(2.4 * k)}"/>'
                f'<path d="M{f(x + 12 * k)} {f(y - 34 * k)} L{f(x + 48 * k)} {f(y - 50 * k)}" stroke="{cz}" stroke-width="{f(5 * k)}" stroke-linecap="round"/>')
    return ""


def alaca_kemer(s, x, y, w, h, koyu_tas=BAZALT, acik_tas="#EDE3CC", n=11, sivri=True):
    """Alaca (bazalt + kireç taşı dönüşümlü) kemer: Diyarbakır mimarisinin siyah-beyaz taş işçiliği (temsilî)."""
    o = []
    cx = x + w / 2
    rr = w / 2
    yt = y - h
    for i in range(n):
        a0 = math.pi * i / n
        a1 = math.pi * (i + 1) / n
        p = []
        for a in (a0, a1):
            p.append((cx - rr * math.cos(a), yt + rr * .2 - rr * .92 * math.sin(a) ** (1.15 if sivri else 1)))
        q = []
        for a in (a1, a0):
            q.append((cx - (rr + w * .1) * math.cos(a), yt + rr * .2 - (rr * .92 + w * .1) * math.sin(a) ** (1.15 if sivri else 1)))
        o.append(f'<path d="{cizgi_d(p + q, True)}" fill="{koyu_tas if i % 2 else acik_tas}" stroke="{BAZALT_K}" stroke-width="1.6"/>')
    return "".join(o)


# ------------------------------------------------------------------ 1. DURAK · ÇAYÖNÜ (sabah)

def cayonu():
    s = Svg("sd-cay")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#5B6FB8"), (.4, "#A894CF"), (.66, "#F5A8B0"), (.86, "#FFCF9E"), (1, "#FFEBCB")])
    s += S.gunes(s, 1880, 170, 40, cekirdek="#FFF9E8", hale="#FFC98A", hale_r=430, guc=.95)
    s += S.bulut_serit(s, 640, 120, 460, 12, "#FFE1E8", "#F2A9BE", .6)
    s += S.bulut(s, 1260, 128, 230, 11, ust="#FFFFFF", alt="#F6C4CC", op=.92)
    s += S.bulut(s, 980, 78, 150, 12, ust="#FFFFFF", alt="#EED1E6", op=.8)
    d, _ = S.dag(s, 700, 2240, ufuk, 1480, 120, 21, renk="#A48FC6", golge="#7F6AA8", bicim="sivri", kar_y=150, kar="#FFF2F4",
                 kar_golge="#D3C2E3", sis="#F6C2C8", isik=1, sirt=4, puruz=12, kenar_isik="#FFD6C6")
    s += d
    d, _ = S.dag(s, -100, 900, ufuk, 360, 176, 22, renk="#B3A0CF", golge="#8F7DB6", bicim="tepe", sis="#F7CDD6", isik=1, sirt=2, puruz=6)
    s += d
    s += S.tepe_bandi(s, 0, W, ufuk + 26, 30, 23, "#C9B37A", "#A99A5E")[0]
    zem = s.lin([(0, "#BFA866"), (.5, "#9BAA5A"), (1, "#6E8E44")], 0, ufuk + 20, 0, H, kull="userSpaceOnUse", ad="cz")
    s += f'<path d="M0 {ufuk + 44} C400 {ufuk + 30} 900 {ufuk + 52} 1300 {ufuk + 36} C1600 {ufuk + 26} 1900 {ufuk + 30} 2100 {ufuk + 22} V{H} H0 Z" fill="{zem}"/>'
    # höyük (Çayönü Tepesi) ve kazı alanı
    s += f'<path d="M1180 {H} C1260 {ufuk + 60} 1420 {ufuk + 30} 1640 {ufuk + 26} C1860 {ufuk + 22} 2000 {ufuk + 40} 2100 {ufuk + 56} V{H} Z" fill="#B99464"/>'
    s += f'<path d="M1180 {H} C1260 {ufuk + 70} 1420 {ufuk + 44} 1640 {ufuk + 40} L1640 {H} Z" fill="#FFFFFF" opacity=".08"/>'
    s += kazi_alani(s, 1340, ufuk + 132, 640, 90, 24)
    # Boğazçay (dere) ve sazlık
    s += f'<path d="M0 {H - 40} C240 {H - 60} 520 {H - 30} 760 {H - 52} C900 {H - 64} 1040 {H - 40} 1160 {H - 30} L1160 {H} L0 {H} Z" fill="#5DBDC0"/>'
    s += S.dalga_cizgileri(20, H - 50, 1100, 30, 25, n=18, op=.7, k=2)
    s += S.sazlik(0, 300, H, 26, boy=70)
    for i, (x, hh) in enumerate([(1120, 120), (1150, 150), (2050, 140), (2085, 160)]):
        s += S.kavak(s, x, ufuk + 70, hh, 26, 27 + i, renk="#6E9A44", isik=1)
    # ön plan: malakit taşı ve bakır boncuk dizisi
    mx, my = 1790, 438
    s += S.kaya(s, mx, my, 150, 52, 28, renk="#7E7468", isik=1)
    g = s.lin([(0, "#7FD3A2"), (.5, "#1F8A5B"), (1, "#0E5A3A")], 0, 0, 1, 1, ad="ml")
    s += f'<path d="M{mx - 40} {my - 46} q20 -26 52 -14 q24 12 8 34 q-34 18 -60 -20 Z" fill="{g}" stroke="#0E3A26" stroke-width="2"/>'
    for k in range(4):
        s += f'<path d="M{mx - 30 + k * 8} {my - 40 + k * 3} q16 -10 34 -2" stroke="#BFF0D2" stroke-width="2" fill="none" opacity=".7"/>'
    for k in range(9):
        bx = 1880 + k * 17
        by = 432 - 10 * math.sin(k / 8 * math.pi)
        s += kure(s, bx, by, 7, BAKIR)
    s += f'<path d="M1872 430 Q1950 404 2030 430" stroke="#5A3A22" stroke-width="1.6" fill="none"/>'
    s += S.cimen(1180, 2100, H - 2, 29, renk="#6E8E44", renk2="#A0B060", boy=12, cicek=["#E2533D", "#FFFFFF", "#F0A21A"])
    s += S.marti(820, 160, .8, 2, renk="#4A3A6A")
    s += S.marti(880, 182, .55, -1, renk="#4A3A6A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 2. DURAK · HEVSEL BAHÇELERİ (öğle)

def _sur_taban(x):
    return 214 - (x - 1100) * .03 + 10 * math.sin(x / 120)


def hevsel():
    s = Svg("sd-hev")
    s += S.gokyuzu(s, 0, 0, W, 300, "gun")
    s += S.gunes(s, 300, 80, 34, hale="#FFF2C2", hale_r=320, guc=.8)
    for i, (x, y, w) in enumerate([(700, 110, 230), (1040, 70, 180), (420, 170, 140)]):
        s += S.bulut(s, x, y, w, 40 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    d, _ = S.dag(s, -80, 900, 290, 300, 196, 41, renk="#9FB8CE", golge="#7E9EBB", bicim="tepe", sis="#D9ECF4", isik=-1, sirt=2, puruz=5)
    s += d
    s += S.tepe_bandi(s, 0, 1300, 300, 24, 42, "#BFC88A", "#9DB06A")[0]
    # bazalt yarlar + surlar (sağ üst)
    yar = [(1080, 330), (1110, 250), (1200, 226), (1400, 214), (1600, 206), (1800, 196), (2000, 186), (2140, 180), (2140, 330)]
    s += f'<path d="{egri_d(yar[:-1])} L2140 330 Z" fill="{BAZALT_K}"/>'
    s += f'<path d="{egri_d(yar[:-1])}" stroke="{BAZALT_A}" stroke-width="3" fill="none"/>'
    s += bazalt_sur(s, 1150, 2140, _sur_taban, 70, burclar=[(1240, 104, 72), (1480, 112, 76), (1720, 108, 76), (1960, 116, 80)], tohum=43)
    # Hevsel bahçeleri: taraçalar, bostan sıraları, meyve ağaçları
    tar = s.lin([(0, "#8EBF5A"), (1, "#4F8A3C")], 0, 300, 0, H, kull="userSpaceOnUse", ad="tr")
    s += f'<path d="M0 {H} V330 C400 318 900 336 1100 330 C1400 322 1800 318 2100 310 V{H} Z" fill="{tar}"/>'
    r = RNG(44)
    for row in range(4):
        y0 = 342 + row * 22
        for x in range(1040 - row * 60, 2100, 64):
            c = r.choice(["#6FA84A", "#8CC25A", "#5C9A40", "#A7C96A"])
            s += f'<path d="M{x} {y0} l52 -6 l6 12 l-52 6 Z" fill="{c}"/>'
    for i in range(16):
        x = 1100 + i * 64 + r.uniform(-10, 10)
        s += S.agac(s, x, 344 + (i % 3) * 8, 18 + (i % 4) * 2, 45 + i, renk=["#5E9A43", "#7DB955", "#4F8A3C"][i % 3], meyve="#E2533D" if i % 5 == 2 else None)
    for i, (x, hh) in enumerate([(1060, 150), (1090, 176), (1124, 140), (1870, 160), (1905, 186)]):
        s += S.kavak(s, x, 352, hh, 26, 60 + i, renk="#5A9C47")
    # karpuzlar (bostan) ve Dicle
    for i, (x, y, rr) in enumerate([(1500, 412, 16), (1540, 418, 13), (1586, 410, 15), (1640, 420, 12), (1694, 414, 16)]):
        s += karpuz(x, y, rr)
    s += karpuz(1760, 424, 15, kesik=True)
    dg = s.lin([(0, "#7FD3CF"), (1, "#1D7F8C")], 0, 420, 0, H, kull="userSpaceOnUse", ad="dc")
    s += f'<path d="M0 404 C300 396 700 412 1000 402 C1200 396 1300 420 1400 446 L1400 {H} L0 {H} Z" fill="{dg}"/>'
    s += S.dalga_cizgileri(20, 414, 1300, 40, 46, n=24, op=.75, k=2)
    s += S.sazlik(0, 220, H, 47, boy=60)
    for k, (x, y) in enumerate([(820, 160), (870, 182), (1300, 140)]):
        s += S.marti(x, y, .7 - k * .1, 2, renk="#3A3E4A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 3. DURAK · MALABADİ KÖPRÜSÜ (ikindi)

def malabadi():
    s = Svg("sd-mal")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "altin")
    s += S.gunes(s, 360, 120, 36, hale="#FFE0A0", hale_r=380, guc=.85)
    for i, (x, y, w) in enumerate([(760, 110, 240), (1160, 80, 200), (1640, 120, 220)]):
        s += S.bulut(s, x, y, w, 70 + i, ust="#FFFFFF", alt="#F5D9B5", op=.95)
    uzak = ""
    d, _ = S.dag(s, 600, 2240, ufuk, 1500, 70, 71, renk="#8C93B8", golge="#6A709C", bicim="sivri", kar_y=118, kar="#FFFFFF", kar_golge="#D0D4EA",
                 sis="#F2D6B8", isik=-1, sirt=5, puruz=12, kenar_isik="#FFE3C0")
    uzak += d
    d, _ = S.dag(s, -80, 900, ufuk, 300, 196, 72, renk="#A69AB6", golge="#857AA0", bicim="tepe", sis="#F6D9BC", isik=-1, sirt=2, puruz=6)
    uzak += d
    s += uzak
    # boğaz: iki yaka (kayalık yamaçlar)
    sol = s.lin([(0, "#C9A86A"), (1, "#8C6E44")], 0, 260, 0, H, kull="userSpaceOnUse", ad="sy")
    s += f'<path d="M1060 {H} L1080 330 C1140 300 1240 292 1330 300 L1350 {H} Z" fill="{sol}"/>'
    s += f'<path d="M1960 {H} L1950 310 C2010 292 2070 290 2140 296 L2140 {H} Z" fill="{sol}"/>'
    s += S.tepe_bandi(s, 0, 1100, ufuk + 20, 26, 73, "#B9B06A", "#8E9A4C")[0]
    su = s.lin([(0, "#9FE0DA"), (.5, "#3AA6A8"), (1, "#1A6E7A")], 0, 380, 0, H, kull="userSpaceOnUse", ad="bc")
    s += f'<path d="M0 {H} V392 C400 384 900 396 1200 390 C1500 384 1800 392 2140 386 V{H} Z" fill="{su}"/>'
    kopru = malabadi_kopru(s, 1330, 1960, 392, 250)
    s += S.yansima(s, kopru, 392, 1300, 700, 70, op=.3)
    s += kopru
    s += S.dalga_cizgileri(20, 400, 2080, 50, 74, n=30, op=.7, k=2)
    for i, x in enumerate((1110, 1150, 1990, 2030)):
        s += S.kavak(s, x, 330 + (i % 2) * 6, 120 + (i % 2) * 30, 24, 75 + i, renk="#6E9A44")
    s += S.sazlik(0, 240, H, 76, boy=60)
    s += S.marti(900, 190, .8, 2, renk="#4A3A3A")
    s += S.marti(960, 214, .55, -1, renk="#4A3A3A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 4. DURAK · BATMAN · RAMAN (akşamüstü, rafineri)

def batman():
    s = Svg("sd-bat")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3D4A9A"), (.35, "#8E6FB8"), (.6, "#F2928E"), (.82, "#FFB86A"), (1, "#FFE1A0")])
    s += S.gunes(s, 520, 230, 40, hale="#FFC27A", hale_r=420, guc=.9)
    s += S.bulut_serit(s, 300, 140, 520, 13, "#FFD0C4", "#E9849C", .6)
    s += S.bulut_serit(s, 1100, 90, 600, 12, "#FFC9B8", "#E9849C", .55)
    # Raman Dağı (kızıl-kahve tepeler) ve pompalar
    d, sirt = S.dag(s, 900, 2240, ufuk + 10, 1560, 150, 81, renk="#A8786A", golge="#7A5262", bicim="tepe", sis="#F2A88E", isik=-1, sirt=4, puruz=10, kenar_isik="#FFC9A0")
    s += d
    for i, (x, o, a) in enumerate([(1180, .9, -10), (1330, 1.0, 6), (1480, .8, -4), (1960, .9, 8)]):
        yy = min(p[1] for p in sirt if abs(p[0] - x) < 30) + 4 if any(abs(p[0] - x) < 30 for p in sirt) else ufuk
        s += pompaci(x, yy, o * 1.2, renk="#3A2E40", aci=a)
    d2, _ = S.dag(s, -60, 900, ufuk, 340, 214, 82, renk="#B48AA4", golge="#8E6A8C", bicim="tepe", sis="#F7B9A8", isik=-1, sirt=2, puruz=5)
    s += d2
    zem = s.lin([(0, "#D9A86A"), (.5, "#B98E52"), (1, "#7E6A3E")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="bz")
    s += f'<path d="M0 {ufuk + 30} C500 {ufuk + 20} 1000 {ufuk + 36} 1400 {ufuk + 24} C1700 {ufuk + 16} 1900 {ufuk + 22} 2100 {ufuk + 18} V{H} H0 Z" fill="{zem}"/>'
    r = RNG(83)
    for k in range(18):  # buğday tarlaları
        x = r.uniform(0, 1200)
        y = ufuk + 40 + r.uniform(0, 110)
        s += f'<path d="M{f(x)} {f(y)} l{f(r.uniform(90, 160))} -8 l-10 {f(r.uniform(16, 24))} l-{f(r.uniform(90, 160))} 8 Z" fill="{r.choice(["#E3C27A", "#C9A04E", "#B8B062", "#D9B66A"])}" opacity=".7"/>'
    s += rafineri(s, 1640, 420, 1.0, isik=-1)
    s += S.cimen(1200, 2100, H - 2, 84, renk="#8C7A44", renk2="#B8A060", boy=10)
    s += S.cimen(0, 1200, H - 2, 85, renk="#9C8A4A", renk2="#C9B06A", boy=12)
    s += S.marti(900, 170, .7, 2, renk="#3A2E50")
    s += S.marti(960, 192, .5, -2, renk="#3A2E50")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 5. DURAK · HASANKEYF (altın saat, baraj gölü)

def hasankeyf():
    s = Svg("sd-has")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#4F7FC0"), (.4, "#A7C0DC"), (.72, "#F8D9A8"), (1, "#FFC886")])
    s += S.gunes(s, 260, 220, 40, hale="#FFC26B", hale_r=420, guc=.9)
    for i, (x, y, w) in enumerate([(640, 80, 220), (1000, 120, 200), (1420, 70, 230)]):
        s += S.bulut(s, x, y, w, 90 + i, ust="#FFF6E8", alt="#F2C9A0", op=.95)
    uzak = ""
    d, _ = S.dag(s, 400, 1400, ufuk, 860, 210, 91, renk="#B9A4B8", golge="#9887A6", bicim="tepe", sis="#F7D8BC", isik=-1, sirt=2, puruz=5)
    uzak += d
    yamac = kalker_yamac(s, 1240, 2160, ufuk + 40, 250, 92, isik=-1)
    uzak += yamac
    s += uzak
    s += S.gol(s, 0, ufuk + 40, W, H - ufuk - 40, 93, ufuk="#FBD8B0", orta="#4FB0B0", derin="#1E6E7C", gunes_x=260, parilti_renk="#FFE7B0")
    s += S.yansima(s, uzak, ufuk + 40, 0, W, 120, op=.3)
    s += S.tekne(s, 1060, ufuk + 96, 90, govde="#C8442F", ust="#F4E9D8")
    s += S.tekne(s, 820, ufuk + 70, 50, govde="#2B50B5", ust="#F4E9D8")
    s += f'<path d="M1000 {ufuk + 104} q60 8 120 0" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".6"/>'
    # ön sağ: kıyı kayalığı
    kiyi = [(1500, H), (1560, 420), (1700, 404), (1900, 398), (2140, 392), (2140, H)]
    s += f'<path d="{egri_d(kiyi[:-1])} L2140 {H} Z" fill="#C9AE7E"/>'
    s += S.kaya(s, 1650, 438, 150, 50, 94, renk="#BFA27A")
    s += S.kaya(s, 1990, 430, 200, 60, 95, renk="#B39670")
    s += S.cimen(1500, 2140, H - 2, 96, renk="#7E8A44", renk2="#A8B060", boy=10)
    s += S.marti(700, 160, .8, 2, renk="#4A3A3A")
    s += S.marti(760, 180, .6, -1, renk="#4A3A3A")
    s += S.marti(1180, 400, 1.05, 4, ayrintili=True)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 6. DURAK · BAKIRCILAR ÇARŞISI (iç mekân, sıcak ışık)

def bakircilar():
    s = Svg("sd-bak")
    g = s.lin([(0, "#F3E6CC"), (1, "#E2CDA6")], 0, 0, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect width="{W}" height="{H}" fill="{g}"/>'
    # tavan kirişleri
    s += f'<rect width="{W}" height="30" fill="#6E4A2C"/>'
    for x in range(0, W, 140):
        s += f'<rect x="{x}" y="0" width="70" height="30" fill="#7E5634"/>'
    # alaca kemerli dükkânlar (sağ yarı)
    for i, x in enumerate((1180, 1490, 1800)):
        s += f'<rect x="{x}" y="120" width="260" height="300" fill="#4A3426"/>'
        s += alaca_kemer(s, x - 10, 136, 280, 30, n=13)
        s += f'<rect x="{x - 24}" y="120" width="24" height="320" fill="{BAZALT}"/><rect x="{x + 260}" y="120" width="24" height="320" fill="{BAZALT}"/>'
        isik = s.rad([(0, "#FFD27A", .55), (1, "#FFD27A", 0)], x + 130, 220, 180, kull="userSpaceOnUse", ad="ik")
        s += f'<circle cx="{x + 130}" cy="220" r="180" fill="{isik}"/>'
        # asılı bakır kaplar
        for j, (tur, dx, dy, hh) in enumerate([("kazan", 50, 250, 60), ("ibrik", 120, 230, 70), ("tava", 190, 200, 50), ("cezve", 70, 160, 50), ("kazan", 200, 290, 46)]):
            px = x + dx
            s += f'<path d="M{px} 136 V{dy - hh * .9}" stroke="#3A2A20" stroke-width="2"/>'
            s += bakir_kap(s, tur, px, dy, hh)
        s += bakir_kap(s, "sini", x + 130, 410, 80)
    # sol duvar: sade kireç taşı (levha için sakin) + raf
    s += f'<rect x="0" y="360" width="1150" height="10" fill="#B89A6E" opacity=".5"/>'
    # tezgâh, örs, çekiç, ocak (sağ ön)
    s += f'<rect x="1080" y="400" width="1100" height="70" fill="#5A3A22"/><rect x="1080" y="396" width="1100" height="10" fill="#8C5E36"/>'
    s += f'<path d="M1300 396 h90 l-10 -26 h-70 Z M1318 370 h54 l6 -14 h-66 Z" fill="#3A3F4B" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="M1400 360 L1460 300" stroke="#6E4A2C" stroke-width="8" stroke-linecap="round"/><rect x="1440" y="282" width="40" height="22" rx="4" fill="#5E6670" transform="rotate(-40 1460 293)"/>'
    oc = s.rad([(0, "#FFE9A8", .95), (.5, "#FF8A3D", .6), (1, "#E2533D", 0)], 1640, 380, 80, kull="userSpaceOnUse", ad="oc")
    s += f'<rect x="1580" y="370" width="120" height="30" rx="6" fill="#3A2A20"/><circle cx="1640" cy="380" r="80" fill="{oc}"/>'
    s += bakir_kap(s, "kazan", 1640, 372, 58)
    s += f'<rect width="{W}" height="{H}" fill="none"/>'
    s += f'<rect x="0" y="440" width="{W}" height="20" fill="#B89A6E"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ HÜLASA · HASAN PAŞA HANI (akşam, konaklama)

def han_hulasa(h=400):
    s = Svg("sd-hhl")
    s += S.gokyuzu(s, 0, 0, W, 170, duraklar=[(0, "#2E3A80"), (.6, "#8A6AB0"), (1, "#F2A08E")])
    s += S.yildizlar(s, 0, 0, W, 120, 30, 101)
    g = s.lin([(0, "#E9DABB"), (1, "#CDB78E")], 0, 120, 0, h, kull="userSpaceOnUse", ad="hd")
    s += f'<rect x="0" y="120" width="{W}" height="{h - 120}" fill="{g}"/>'
    # iki katlı revak (sağ yarı)
    for kat, (y0, hh) in enumerate(((250, 120), (390, 130))):
        for i in range(6):
            x = 1080 + i * 180
            s += f'<rect x="{x}" y="{y0 - hh + 30}" width="140" height="{hh - 30}" fill="#3A2A24"/>'
            s += alaca_kemer(s, x - 8, y0 - hh + 46, 156, 20, n=11)
            s += f'<rect x="{x - 26}" y="{y0 - hh}" width="26" height="{hh}" fill="{BAZALT}"/>'
            lam = s.rad([(0, "#FFE08A", .9), (1, "#FFE08A", 0)], x + 70, y0 - hh + 70, 70, kull="userSpaceOnUse", ad="lm")
            s += f'<circle cx="{x + 70}" cy="{y0 - hh + 70}" r="70" fill="{lam}"/><circle cx="{x + 70}" cy="{y0 - hh + 66}" r="7" fill="#FFF4C8"/>'
        s += f'<rect x="1040" y="{y0}" width="1100" height="12" fill="#B89A6E"/>'
    for x in range(1040, 2140, 36):  # alaca bant
        s += f'<rect x="{x}" y="120" width="18" height="12" fill="{BAZALT}"/>'
    # avlu: masa, çay, Pamuk kitapla
    s += f'<rect x="0" y="{h - 30}" width="{W}" height="30" fill="#A88A60"/>'
    s += f'<ellipse cx="1500" cy="{h - 20}" rx="220" ry="18" fill="#6E4A2C"/><rect x="1300" y="{h - 52}" width="400" height="16" rx="6" fill="#8C5E36"/>'
    for k, x in enumerate((1360, 1420, 1580, 1640)):
        s += Y.cay_bardak_kucuk(x, h - 52, 24)
    s += Y.semaver(s, 1500, h - 52, 70)
    s += f'<use href="#pamuk-kitap" x="1760" y="{h - 210}" width="170" height="194"/>'
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ MECLİS · DİCLE KIYISI · KARPUZ ÇARDAĞI

def karpuz_meclis():
    s = Svg("sd-mec")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#4C95D6"), (.6, "#A6D8F0"), (1, "#F2EDD6")])
    s += S.gunes(s, 1960, 70, 30, hale="#FFF4CC", hale_r=260, guc=.8)
    s += S.bulut(s, 700, 90, 180, 111, op=.9)
    s += S.bulut(s, 1240, 70, 160, 112, op=.85)
    # uzakta bazalt yar + sur silüeti
    s += f'<path d="M0 {ufuk} L0 196 C200 186 500 180 820 188 L900 {ufuk} Z" fill="#5B5762" opacity=".7"/>'
    s += bazalt_sur(s, 20, 820, lambda x: 190 - (x - 20) * .01, 30, burclar=[(140, 46, 40), (420, 50, 42), (700, 46, 40)], tohum=113, renk="#5E5A66", mazgal=True, tas=False)
    dg = s.lin([(0, "#8FD8D4"), (1, "#2A9FA6")], 0, ufuk, 0, ufuk + 70, kull="userSpaceOnUse", ad="dn")
    s += f'<rect x="0" y="{ufuk}" width="{W}" height="70" fill="{dg}"/>'
    s += S.dalga_cizgileri(0, ufuk + 6, W, 56, 114, n=30, op=.7, k=2)
    kum = s.lin([(0, "#EAD8A8"), (1, "#C9AE7E")], 0, ufuk + 60, 0, H, kull="userSpaceOnUse", ad="km")
    s += f'<path d="M0 {ufuk + 70} C500 {ufuk + 60} 1200 {ufuk + 74} 2100 {ufuk + 58} V{H} H0 Z" fill="{kum}"/>'
    r = RNG(115)
    for k in range(26):
        x = 980 + r.uniform(0, 1100)
        y = ufuk + 110 + r.uniform(0, 80)
        s += f'<path d="M{f(x - 30)} {f(y + 4)} q30 -16 60 0" stroke="#5C9A40" stroke-width="3" fill="none"/>'
    for k, (x, y, rr) in enumerate([(1000, 420, 22), (1080, 436, 18), (1990, 430, 22), (2060, 412, 16), (920, 400, 14)]):
        s += karpuz(x, y, rr)
    s += cardak(s, 1520, 400, 520, 200)
    s += f'<rect x="1330" y="372" width="380" height="14" rx="5" fill="#8C5E36"/><path d="M1350 386 v30 M1690 386 v30" stroke="#6E4A2C" stroke-width="6"/>'
    s += karpuz(1480, 366, 14, kesik=True) + karpuz(1560, 366, 14, kesik=True)
    s += '<use href="#elif-soru" x="1170" y="196" width="240" height="252"/>'
    s += '<use href="#yusuf-anlatan" x="1640" y="196" width="240" height="252"/>'
    s += '<use href="#pamuk-dusunen" x="1440" y="250" width="160" height="183"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ KISSA · ON GÖZLÜ KÖPRÜ (sabah-öğle)

def on_gozlu():
    s = Svg("sd-ong")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3F8FD0"), (.6, "#9FD3EE"), (1, "#E8F6F8")])
    s += S.gunes(s, 1950, 80, 30, hale="#FFF4CC", hale_r=260, guc=.8)
    for i, (x, y, w) in enumerate([(700, 100, 200), (1150, 70, 170), (1600, 120, 180)]):
        s += S.bulut(s, x, y, w, 120 + i, op=.93)
    d, _ = S.dag(s, -80, 1100, ufuk, 400, 190, 121, renk="#9FB8CE", golge="#7E9EBB", bicim="tepe", sis="#D9ECF4", isik=-1, sirt=2, puruz=5)
    s += d
    s += S.tepe_bandi(s, 0, W, ufuk + 10, 22, 122, "#A7C46A", "#7FA352")[0]
    for i in range(18):
        x = 60 + i * 118
        s += S.kavak(s, x, ufuk + 22, 70 + (i % 3) * 20, 16, 123 + i, renk="#5E9A4A")
    su = s.lin([(0, "#A6E0DC"), (.5, "#3AA6A8"), (1, "#1A6E7A")], 0, ufuk + 40, 0, H, kull="userSpaceOnUse", ad="os")
    s += f'<rect x="0" y="{ufuk + 40}" width="{W}" height="{H - ufuk - 40}" fill="{su}"/>'
    kp = kemerli_kopru(s, 1000, 2160, 300, 372, 10, 124)
    s += S.yansima(s, kp, 372, 980, 1180, 80, op=.35)
    s += kp
    s += S.dalga_cizgileri(0, 380, W, 70, 125, n=36, op=.7, k=2)
    s += S.sazlik(0, 260, H, 126, boy=60)
    # balıkçıl
    s += (f'<g transform="translate(860 420)"><path d="M0 0 C-6 -30 -2 -60 14 -76" stroke="#E9EEF2" stroke-width="7" fill="none" stroke-linecap="round"/>'
          f'<ellipse cx="-10" cy="4" rx="26" ry="14" fill="#C9D3DC"/><path d="M14 -76 l26 4 l-24 4 Z" fill="#F0A21A"/>'
          f'<circle cx="12" cy="-78" r="7" fill="#E9EEF2"/><path d="M-6 16 v26 M2 16 v26" stroke="#3A3E4A" stroke-width="3"/></g>')
    s += S.marti(780, 170, .7, 2, renk="#3A3E4A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ ANAHTAR · SURLARIN ETEĞİ (gün batımı)

def sur_etegi():
    s = Svg("sd-ete")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#3A4C9C"), (.4, "#8E7BC0"), (.72, "#F7A6A0"), (1, "#FFD39A")])
    s += S.gunes(s, 880, 250, 40, hale="#FFC27A", hale_r=400, guc=.9)
    s += S.bulut_serit(s, 500, 140, 520, 14, "#FFD0C4", "#F28FA0", .7)
    yar = [(1060, 380), (1120, 260), (1300, 230), (1600, 214), (1900, 206), (2140, 200), (2140, 380)]
    s += f'<path d="{egri_d(yar[:-1])} L2140 380 Z" fill="#2E2B33"/>'
    s += bazalt_sur(s, 1140, 2140, lambda x: 236 - (x - 1140) * .03, 64, burclar=[(1260, 96, 70), (1560, 104, 74), (1880, 100, 74)], tohum=131,
                    renk="#45414C", ust_isik="#FFB27A")
    su = s.lin([(0, "#F7B7A0"), (.4, "#7E7FB0"), (1, "#26306A")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="es")
    s += f'<rect x="0" y="{ufuk}" width="1100" height="{H - ufuk}" fill="{su}"/>'
    s += f'<path d="M1060 380 L1100 {H} L0 {H} L0 380 Z" fill="{su}" opacity="0"/>'
    s += S.gol(s, 0, ufuk, 1180, H - ufuk, 132, ufuk="#F7B7A0", orta="#8E7FB0", derin="#2A3470", gunes_x=880, parilti_renk="#FFE2A8")
    # taş merdiven (yardan surlara)
    for k in range(9):
        x = 1120 + k * 34
        y = 440 - k * 22
        s += f'<rect x="{x}" y="{y}" width="90" height="16" fill="#6E6876" stroke="#26242B" stroke-width="2"/>'
    for k, (x, y) in enumerate([(1150, 420), (1290, 330), (1400, 262)]):
        fen = s.rad([(0, "#FFE9A8", .9), (1, "#FFD27A", 0)], x, y - 30, 50, kull="userSpaceOnUse", ad="fn")
        s += f'<path d="M{x} {y} v-36" stroke="#2E2B33" stroke-width="4"/><circle cx="{x}" cy="{y - 40}" r="50" fill="{fen}"/><rect x="{x - 7}" y="{y - 48}" width="14" height="16" rx="3" fill="#FFE08A" stroke="#2E2B33" stroke-width="2"/>'
    s += f'<rect x="1100" y="440" width="1040" height="20" fill="#2E2B33"/>'
    s += f'<use href="#pamuk-akce" x="1820" y="300" width="140" height="160"/>'
    s += S.marti(1100, 140, .9, 2, renk="#2F2A4A")
    s += S.marti(1170, 168, .6, -2, renk="#2F2A4A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ BÜYÜK İMTİHAN 1 · DİYARBAKIR SURLARI (62 mm)

def kale_sur(h=620):
    s = Svg("sd-kal")
    ufuk = 360
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#2F5DA8"), (.38, "#86A9D6"), (.7, "#F6C99A"), (1, "#FFB46B")])
    s += S.gunes(s, 260, 300, 52, hale="#FFB45A", hale_r=520, guc=.95)
    for i, (x, y, w) in enumerate([(560, 140, 300), (1000, 90, 340), (1500, 150, 280), (1880, 80, 200)]):
        s += S.bulut(s, x, y, w, 140 + i, ust="#FFF4E4", alt="#F0A98A", op=.95)
    d, _ = S.dag(s, -80, 900, ufuk, 320, 260, 141, renk="#A58DAE", golge="#87709A", bicim="tepe", sis="#F6C3AA", isik=-1, sirt=2, puruz=5)
    s += d
    # bazalt yar ve surlar
    yar = [(820, 520), (880, 380), (1000, 330), (1300, 300), (1600, 286), (1900, 270), (2160, 262), (2160, 520)]
    s += f'<path d="{egri_d(yar[:-1])} L2160 520 Z" fill="{BAZALT_K}"/>'
    s += f'<path d="{egri_d(yar[:-1])}" stroke="{BAZALT_A}" stroke-width="4" fill="none"/>'
    tb = lambda x: 318 - (x - 900) * .04 + 8 * math.sin(x / 140)  # noqa: E731
    s += bazalt_sur(s, 900, 2160, tb, 110, burclar=[(1000, 170, 110), (1300, 182, 116), (1600, 176, 112), (1900, 190, 120), (2120, 170, 100)], tohum=142)
    bx = 1600
    by = tb(bx) - 176 - 24
    s += f'<path d="M{bx} {f(by)} v-120" stroke="#3A2E26" stroke-width="7"/>'
    s += turk_bayragi(bx, by - 120, 64, 8)
    # Hevsel bahçeleri ve Dicle
    gz = s.lin([(0, "#9BC062"), (1, "#4E8A3C")], 0, 420, 0, h, kull="userSpaceOnUse", ad="hz")
    s += f'<path d="M0 {h} V470 C400 452 800 470 1000 480 C1400 470 1800 470 2160 460 V{h} Z" fill="{gz}"/>'
    r = RNG(143)
    for k in range(30):
        x = r.uniform(0, 2100)
        s += S.agac(s, x, 500 + r.uniform(0, 40), 16 + r.uniform(0, 8), 144 + k, renk=r.choice(["#5E9A43", "#7DB955", "#4F8A3C"]))
    for k in range(10):
        x = 900 + k * 120
        s += S.kavak(s, x, 520, 130 + (k % 3) * 20, 22, 160 + k, renk="#5A9C47")
    dg = s.lin([(0, "#FFD2A8"), (.4, "#4FAFB4"), (1, "#0F5A6E")], 0, 540, 0, h, kull="userSpaceOnUse", ad="dg")
    s += f'<path d="M0 {h} V548 C500 538 1000 556 1500 546 C1800 540 2000 548 2160 544 V{h} Z" fill="{dg}"/>'
    s += S.dalga_cizgileri(0, 556, W, 60, 145, n=30, op=.7, k=2)
    for k, (x, y, o) in enumerate([(700, 200, 1.0), (780, 236, .7), (1200, 150, .7)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ BÜYÜK İMTİHAN 2 · SUR KAPISI (30 mm)

def sur_kapisi(h=300):
    s = Svg("sd-kap")
    s += S.gokyuzu(s, 0, 0, W, h, duraklar=[(0, "#F7B07A"), (1, "#FFE1B0")])
    g = s.lin([(0, "#55515C"), (1, "#36333C")], 0, 40, 0, h, kull="userSpaceOnUse", ad="sd")
    s += f'<rect x="0" y="60" width="{W}" height="{h - 60}" fill="{g}"/>'
    r = RNG(150)
    for row in range(8):
        y = 60 + row * 32
        off = 0 if row % 2 == 0 else 40
        for x in range(-40 + off, W, 80):
            s += f'<rect x="{x + 2}" y="{y + 2}" width="76" height="28" rx="3" fill="{karis("#5B5762", "#3A3740", r.uniform(0, .7))}" stroke="#26242B" stroke-width="1.6"/>'
    for x in range(0, W, 110):
        s += f'<rect x="{x}" y="20" width="70" height="44" fill="#5B5762" stroke="#26242B" stroke-width="2.4"/>'
    s += f'<rect x="0" y="58" width="{W}" height="10" fill="#C9A27A" opacity=".7"/>'
    cx, ky = 1450, h
    s += alaca_kemer(s, cx - 190, 150, 380, 0, n=15)
    s += f'<path d="M{cx - 140} {ky} V150 Q{cx - 140} 92 {cx} 78 Q{cx + 140} 92 {cx + 140} 150 V{ky} Z" fill="#2A1A10"/>'
    isik = s.rad([(0, "#FFF4C8", .95), (.5, "#FFD27A", .5), (1, "#FFD27A", 0)], cx, 200, 260, kull="userSpaceOnUse", ad="ki")
    s += f'<path d="M{cx - 30} {ky} V100 L{cx + 30} 100 V{ky} Z" fill="#FFE9A8"/><circle cx="{cx}" cy="200" r="260" fill="{isik}"/>'
    for sx in (-1, 1):
        x0 = cx + sx * 30
        x1 = cx + sx * 132
        s += f'<path d="M{x0} {ky} V104 Q{(x0 + x1) / 2} 88 {x1} 132 V{ky} Z" fill="#6E4422" stroke="#3A2614" stroke-width="4"/>'
        for k in range(4):
            yy = 146 + k * 38
            s += f'<path d="M{x0} {yy} H{x1}" stroke="#3A2614" stroke-width="5"/>'
            for j in range(3):
                s += f'<circle cx="{x0 + sx * (24 + j * 34)}" cy="{yy}" r="4" fill="#C9A86A"/>'
    for x in (cx - 240, cx + 240):
        s += f'<rect x="{x - 6}" y="130" width="12" height="60" fill="#3A2614"/>'
        alev = s.rad([(0, "#FFF4C8"), (.5, "#FFB43A"), (1, "#E2533D", .0)], x, 112, 60, kull="userSpaceOnUse", ad="al")
        s += f'<circle cx="{x}" cy="112" r="60" fill="{alev}"/><path d="M{x - 12} 130 Q{x - 14} 104 {x} 86 Q{x + 14} 104 {x + 12} 130 Z" fill="#FF8A3D"/><path d="M{x - 6} 130 Q{x - 6} 112 {x} 100 Q{x + 6} 112 {x + 6} 130 Z" fill="#FFE08A"/>'
    for k, (x, c) in enumerate(((760, "#B23A2E"), (2010, "#13A3A6"))):
        s += f'<path d="M{x - 60} 70 H{x + 60} V230 L{x} 270 L{x - 60} 230 Z" fill="{c}" stroke="#26242B" stroke-width="3"/>'
        s += f'<path d="M{x - 60} 82 H{x + 60}" stroke="{ALTIN}" stroke-width="6"/>'
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x, 160, 40), True)}" fill="{ALTIN}" stroke="#3A2614" stroke-width="2"/><circle cx="{x}" cy="160" r="14" fill="{c}"/>'
    for k in range(4):
        s += f'<rect x="{cx - 220 - k * 30}" y="{h - 14 - k * 14}" width="{440 + k * 60}" height="16" fill="#6E6876" stroke="#26242B" stroke-width="2" transform="translate(0 {k * 14})"/>'
    s += '<use href="#pamuk-akce" x="1690" y="128" width="150" height="171"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ CEVAPLAR · GECE (36 mm)

def gece_dicle(h=360):
    s = Svg("sd-gec")
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 30, 140, 160)
    s += S.ay(s, 1180, 84, 34, golge_renk="#13204A")
    yar = [(1300, ufuk + 10), (1340, 170), (1500, 150), (1800, 140), (2140, 132), (2140, ufuk + 10)]
    yd = f'<path d="{egri_d(yar[:-1])} L2140 {ufuk + 10} Z" fill="#1A1C30"/>'
    sur = bazalt_sur(s, 1360, 2140, lambda x: 158 - (x - 1360) * .03, 46, burclar=[(1460, 74, 56), (1720, 80, 58), (1980, 78, 58)], tohum=161,
                     renk="#2C3050", ust_isik="#7F8CC8", tas=False)
    s += yd + sur
    for (x, y) in ((1470, 100), (1730, 92), (1990, 94)):
        s += f'<rect x="{x}" y="{y}" width="8" height="10" fill="#FFD27A"/>'
    kp = kemerli_kopru(s, 120, 900, ufuk - 18, ufuk + 10, 10, 162, renk="#262B4A", ust_isik="#5E6AA8", ayak_ok=False)
    s += kp
    for k in range(10):
        s += f'<circle cx="{120 + k * 78 + 39}" cy="{ufuk - 30}" r="4" fill="#FFE08A"/>'
    s += S.gol(s, 0, ufuk + 10, W, h - ufuk - 10, 163, ufuk="#3A5A9A", orta="#1D3366", derin="#0B1636", gunes_x=1180, parilti_renk="#FFF0C0", cizgi_renk="#9FB4E8")
    s += S.yansima(s, yd + sur + kp, ufuk + 10, 0, W, 90, op=.3)
    s += S.tekne(s, 1040, ufuk + 60, 70, govde="#1D3A8A", ust="#C9D6EA")
    s += f'<circle cx="1050" cy="{ufuk + 32}" r="16" fill="#FFD27A" opacity=".35"/><circle cx="1050" cy="{ufuk + 32}" r="5" fill="#FFE9A8"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ FİNAL · BAZALT BURÇTA PAMUK (90 mm)

def final_dicle(h=900, nisanlar=None):
    s = Svg("sd-fin")
    ufuk = 520
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    gx, gy = 700, ufuk - 20
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE0A0" opacity=".12"/>'
    s += S.gunes(s, gx, gy, 70, hale="#FFC56B", hale_r=700, guc=.95)
    for i, (x, y, w, k) in enumerate([(200, 260, 520, 22), (1200, 180, 640, 26), (1500, 330, 480, 16), (100, 420, 380, 12)]):
        s += S.bulut_serit(s, x, y, w, k, "#FFC59A", "#FF6F8A", .75)
    uzak = ""
    d, _ = S.dag(s, -100, 900, ufuk, 300, 380, 171, renk="#8A5E8E", golge="#5E3E72", bicim="tepe", sis="#E07A8A", isik=-1, sirt=2, puruz=6)
    uzak += d
    d, _ = S.dag(s, 1100, 2300, ufuk, 1700, 360, 172, renk="#A06E96", golge="#6E4E80", bicim="sivri", kar_y=400, kar="#FFE3EC", kar_golge="#C7A6CF", sis="#F49A8A", isik=-1, sirt=3)
    uzak += d
    s += uzak
    gz = s.lin([(0, "#B07A6A"), (1, "#5E6A3E")], 0, ufuk, 0, 700, kull="userSpaceOnUse", ad="fz")
    s += f'<rect x="0" y="{ufuk}" width="{W}" height="200" fill="{gz}"/>'
    dg = s.lin([(0, "#FFB59A"), (.5, "#C86A9A"), (1, "#2D3A7A")], 0, ufuk + 20, 0, 720, kull="userSpaceOnUse", ad="fd")
    s += f'<path d="M0 {ufuk + 70} C400 {ufuk + 40} 800 {ufuk + 90} 1200 {ufuk + 60} C1600 {ufuk + 30} 1900 {ufuk + 70} 2100 {ufuk + 50} V720 H0 Z" fill="{dg}"/>'
    s += kemerli_kopru(s, 900, 1500, ufuk + 34, ufuk + 62, 10, 173, renk="#3A2E46", ust_isik="#FFB27A", ayak_ok=False)
    for k, (x, y, o) in enumerate([(560, 200, 1.4), (640, 240, 1.0), (1100, 120, .8), (1180, 150, .6), (300, 160, .7)]):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    # ön plan: bazalt sur ve burç
    g = s.lin([(0, "#5E5A66"), (1, "#2C2A31")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    s += f'<rect x="0" y="720" width="{W}" height="{h - 720}" fill="{g}"/>'
    r = RNG(174)
    for row in range(6):
        y = 724 + row * 30
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            s += f'<rect x="{x + 2}" y="{y}" width="86" height="27" rx="3" fill="{karis("#5E5A66", "#34313A", r.uniform(0, .7))}" stroke="#1E1C22" stroke-width="1.6"/>'
    for x in range(0, W, 150):
        s += f'<rect x="{x}" y="660" width="96" height="64" fill="#57535F" stroke="#1E1C22" stroke-width="2.6"/><rect x="{x}" y="660" width="96" height="10" fill="#C9A27A" opacity=".8"/>'
    s.tanim(f'<linearGradient id="{s.onek}-tk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7A7484"/><stop offset=".6" stop-color="#55515C"/><stop offset="1" stop-color="#34313A"/></linearGradient>')
    s += f'<rect x="1560" y="560" width="420" height="{h - 560}" fill="url(#{s.onek}-tk)" stroke="#1E1C22" stroke-width="3"/>'
    for k in range(1, 6):
        s += f'<path d="M1560 {560 + k * 60} H1980" stroke="#26242B" stroke-width="2" opacity=".6"/>'
    s += f'<path d="M1560 640 H1980" stroke="{KALKER}" stroke-width="10" opacity=".7"/>'
    for x in range(1560, 1980, 84):
        s += f'<rect x="{x}" y="510" width="54" height="56" fill="#5E5A66" stroke="#1E1C22" stroke-width="2.6"/>'
    s += f'<path d="M1740 {h} V770 Q1740 730 1770 722 Q1800 730 1800 770 V{h} Z" fill="#1E1C22"/>'
    s += '<use href="#pamuk-bayrak" x="1600" y="150" width="340" height="400"/>'
    s += f'<path d="M260 650 V330" stroke="#3A2E26" stroke-width="10"/><circle cx="260" cy="324" r="10" fill="{ALTIN}"/>'
    s += f'<path d="M260 360 Q900 520 1640 330" stroke="#3A2E26" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .6) / (len(nisanlar) + .2)
            x = (1 - t) ** 2 * 260 + 2 * (1 - t) * t * 900 + t * t * 1640
            y = (1 - t) ** 2 * 360 + 2 * (1 - t) * t * 520 + t * t * 330
            s += f'<path d="M{f(x)} {f(y)} v18" stroke="#3A2E26" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 50)} {f(y + 14)}) rotate({f((k % 2 * 2 - 1) * 5)} 50 60) scale(.82)">{ns}</g>'
    for k in range(60):
        x = r.uniform(300, 1900)
        y = r.uniform(80, 640)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ AÇILIŞ · DİCLE YOLU PANORAMASI (şematik, temsilî harita)

# Şematik konumlar (birim; 2100×1100). Uzaklıklar ölçekli DEĞİL: Diyarbakır büyütülmüştür (temsilî tur haritası).
KONUM = {
    "1": (250, 500), "2": (1005, 770), "3": (1455, 470), "4": (1625, 700), "5": (1905, 905), "6": (560, 760),
    "H": (700, 700), "M": (840, 930), "K": (1050, 915), "A": (985, 612), "V": (590, 600),
}
# (anahtar, üst etiket, ad, sayfa, akçe, tür, dx mm, dy mm) — etiketin sol üst köşesinin rozet merkezine göre yeri
PANORAMA_ETIKET = [
    ("1", "1. DURAK · ÇAYÖNÜ", "Atomlar kaybolmaz", "2", "+100 akçe", "durak", 3.6, -13.4),
    ("2", "2. DURAK · HEVSEL", "Denkleştirme", "3", "+120 akçe", "durak", 4.4, -2.0),
    ("3", "3. DURAK · MALABADİ", "Denklemden hesaba", "4", "+120 akçe", "durak", -24, -13.4),
    ("4", "4. DURAK · BATMAN", "Sınırlayıcı", "5", "+120 akçe", "durak", 4.4, -4.2),
    ("5", "5. DURAK · HASANKEYF", "Verim ve saflık", "6", "+120 akçe", "durak", -38, -13.6),
    ("6", "6. DURAK · BAKIRCILAR", "Karışım ve zincir", "7", "+120 akçe", "durak", -47, 1.0),
    ("H", "HASAN PAŞA HANI", "Hülasa", "8", "+40 akçe", "hulasa", 4.0, -4.0),
    ("M", "DİCLE KIYISI", "Meclis", "9", "+120 akçe", "yan", -32, 2.8),
    ("K", "ON GÖZLÜ KÖPRÜ", "Kıssa", "10", "+120 akçe", "yan", 4.0, 1.6),
    ("A", "SURLARIN ETEĞİ", "Anahtar merdiveni", "11", "+120 akçe", "yan", 4.0, -4.4),
    ("V", "DİYARBAKIR SURLARI", "Büyük İmtihan", "12-13", "+300 akçe", "kale", 4.2, -13.6),
]
DICLE = [(-20, 330), (160, 380), (330, 430), (520, 492), (760, 520), (930, 560), (1040, 640), (1060, 760), (1050, 880), (1110, 960),
         (1330, 990), (1560, 970), (1760, 950), (1900, 960), (2000, 990), (2140, 1010)]
BATMAN_CAYI = [(1400, 340), (1440, 420), (1455, 470), (1470, 560), (1500, 680), (1520, 820), (1540, 975)]


def panorama_dicle(h=1100):
    s = Svg("sd-pan")
    ufuk = 340
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2E3A8A"), (.3, "#6E5AAE"), (.55, "#E0788E"), (.78, "#FFA65E"), (1, "#FFD99A")])
    gx, gy = 1700, ufuk - 40
    for k in range(12):
        a0 = math.pi + .1 + k * (math.pi - .2) / 12
        a1 = a0 + .05
        s += f'<path d="M{gx} {gy} L{f(gx + 2400 * math.cos(a0))} {f(gy + 2400 * math.sin(a0))} L{f(gx + 2400 * math.cos(a1))} {f(gy + 2400 * math.sin(a1))} Z" fill="#FFE4B0" opacity=".08"/>'
    s += S.gunes(s, gx, gy, 50, hale="#FFC56B", hale_r=620, guc=.95)
    for (x, y, w_, k) in ((900, 140, 520, 18), (1300, 90, 560, 20), (240, 230, 360, 12), (620, 270, 380, 10)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC9A0", "#FF6F8A", .75)
    # Güneydoğu Toroslar (kuzey ufku)
    uzak = ""
    for i, (sol, sag, tx, ty, bicim, renk, golge, kar) in enumerate((
            (-120, 760, 300, 200, "sivri", "#9A7AA8", "#73588E", 236), (500, 1500, 1020, 170, "sivri", "#B48AB0", "#86669C", 214),
            (1300, 2240, 1880, 200, "sivri", "#A27AA0", "#7A5A8E", 236))):
        d_, _ = S.dag(s, sol, sag, ufuk + 8, tx, ty, 300 + i, renk=renk, golge=golge, bicim=bicim, kar_y=kar, kar="#FFE6EE", kar_golge="#C6A7D2",
                      sis="#FFA18E", isik=1, sirt=3, puruz=9)
        uzak += d_
    s += uzak
    gk = s.lin([(0, "#C9A27E"), (.15, "#D3B070"), (.5, "#B5B262"), (1, "#7E9A48")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kara")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    r = RNG(310)
    for k in range(90):  # tarlalar (Mezopotamya ovası)
        x = r.uniform(-50, 2100)
        y = r.uniform(ufuk + 20, h)
        sc = .45 + (y - ufuk) / (h - ufuk) * .8
        w_ = r.uniform(70, 170) * sc
        hh = w_ * .3
        c = r.choice(["#D9B66A", "#C9A04E", "#B9B65E", "#E3C27A", "#9FB25A", "#C7B46A"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w_)} {f(-hh * .2)} l{f(-w_ * .2)} {f(hh)} l{f(-w_)} {f(hh * .2)} Z" fill="{c}" opacity=".55"/>'
    # Raman tepeleri (Batman'ın yanı) ve Hasankeyf kalker yamacı
    d_, _ = S.dag(s, 1620, 2020, 650, 1800, 560, 311, renk="#A8786A", golge="#7A5262", bicim="tepe", isik=1, sirt=2, puruz=6)
    s += d_
    s += kalker_yamac(s, 1880, 2140, 905, 120, 312, isik=1, magara=10)
    # Dicle, Batman Çayı, Ilısu gölü
    s += f'<path d="{egri_d(BATMAN_CAYI)}" fill="none" stroke="#2F8FA0" stroke-width="14" stroke-linecap="round" opacity=".7"/>'
    s += f'<path d="{egri_d(BATMAN_CAYI)}" fill="none" stroke="#9FDEE0" stroke-width="6" stroke-linecap="round"/>'
    gol = s.lin([(0, "#7FD3CF"), (1, "#1E7F8C")], 0, 900, 0, h, kull="userSpaceOnUse", ad="il")
    s += f'<path d="M1840 960 C1900 920 2000 930 2140 920 V1100 H1760 C1790 1040 1800 990 1840 960 Z" fill="{gol}"/>'
    s += S.dalga_cizgileri(1800, 960, 300, 120, 313, n=10, op=.7, k=2)
    dd = egri_d(DICLE)
    s += f'<path d="{dd}" fill="none" stroke="#1E6E7C" stroke-width="40" stroke-linecap="round" opacity=".55"/>'
    s += f'<path d="{dd}" fill="none" stroke="#4FB6B8" stroke-width="28" stroke-linecap="round"/>'
    s += f'<path d="{dd}" fill="none" stroke="#BFF0EE" stroke-width="5" stroke-linecap="round" stroke-dasharray="30 26" opacity=".8"/>'
    # Diyarbakır (büyütülmüş): bazalt plato + sur halkası + Hevsel + On Gözlü
    cx, cy, rx, ry = 700, 690, 250, 120
    s += f'<ellipse cx="{cx + 10}" cy="{cy + 30}" rx="{rx + 40}" ry="{ry + 40}" fill="#3A3740" opacity=".55"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#D9C7A2"/>'
    for k in range(40):  # evler (çatı ve avlular)
        a = r.uniform(0, 2 * math.pi)
        dd_ = math.sqrt(r.random()) * .85
        x = cx + rx * dd_ * math.cos(a)
        y = cy + ry * dd_ * math.sin(a)
        s += f'<rect x="{f(x - 12)}" y="{f(y - 8)}" width="24" height="14" fill="{r.choice(["#5B5762", "#E8DCC0", "#C9B48A", "#6E6876"])}" stroke="#3A3740" stroke-width="1.2"/>'
    halka = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in [2 * math.pi * i / 48 for i in range(48)]]
    s += f'<path d="{cizgi_d(halka, True)}" fill="none" stroke="#2C2A31" stroke-width="20"/>'
    s += f'<path d="{cizgi_d(halka, True)}" fill="none" stroke="#5B5762" stroke-width="12"/>'
    for i in range(0, 48, 4):
        x, y = halka[i]
        s += f'<rect x="{f(x - 12)}" y="{f(y - 16)}" width="24" height="24" fill="#4A4752" stroke="#2C2A31" stroke-width="2.4"/>'
    for i, (x, y) in enumerate([(cx - 30, cy - ry - 30), (cx + rx - 10, cy - 70)]):
        s += f'<path d="M{f(x)} {f(y)} v-50" stroke="#3A2E26" stroke-width="4"/>'
        s += turk_bayragi(x, y - 50, 22, 3)
    for k in range(9):  # Hevsel bahçeleri
        x = 930 + (k % 3) * 34
        y = 700 + (k // 3) * 40
        s += f'<path d="M{x} {y} l32 -4 l4 30 l-32 4 Z" fill="{["#6FA84A", "#8CC25A", "#5C9A40"][k % 3]}" stroke="#3E6E2E" stroke-width="1.2"/>'
        s += S.agac(s, x + 16, y + 6, 8, 330 + k, renk="#4F8A3C")
    s += kemerli_kopru(s, 1010, 1095, 900, 920, 10, 331, renk="#4A4752", ust_isik="#D9B98A", ayak_ok=False)
    # Çayönü höyüğü, Malabadi, rafineri, karpuzlar
    s += f'<path d="M200 520 C240 470 360 462 420 500 Z" fill="#B99464"/>'
    s += kazi_alani(s, 230, 512, 170, 22, 332)
    s += malabadi_kopru(s, 1405, 1505, 482, 52)
    s += rafineri(s, 1700, 700, .32)
    for k in range(5):
        s += karpuz(800 + k * 22, 958 + (k % 2) * 6, 7)
    s += cardak(s, 870, 950, 60, 30)
    # rota
    sira = ["1", "2", "3", "4", "5", "6", "H", "M", "K", "A", "V"]
    ara = {("1", "2"): [(520, 560), (880, 600), (960, 700)], ("2", "3"): [(1180, 700), (1350, 560)], ("3", "4"): [(1540, 590)],
           ("4", "5"): [(1800, 790)], ("5", "6"): [(1700, 1040), (1300, 1060), (900, 1040), (520, 960), (440, 860)],
           ("6", "H"): [(620, 730)], ("H", "M"): [(760, 820)], ("M", "K"): [(950, 960)], ("K", "A"): [(1110, 800), (1080, 680)],
           ("A", "V"): [(880, 560), (720, 548)]}
    yol = []
    for i, k in enumerate(sira):
        yol.append(KONUM[k])
        if i + 1 < len(sira):
            yol += ara.get((k, sira[i + 1]), [])
    yd = egri_d(yol, False, .9)
    s += f'<path d="{yd}" fill="none" stroke="#1B1D26" stroke-width="15" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>'
    s += f'<path d="{yd}" fill="none" stroke="#FFF1CF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="3" stroke-dasharray="12 9" stroke-linecap="round"/>'
    for k in sira:
        x, y = KONUM[k]
        if k in "123456":
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 34), True)}" fill="#F0C14A" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 27), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 10)}" text-anchor="middle" {B} font-size="30" fill="#FFFFFF">{k}</text>'
        elif k == "V":
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="32" fill="#E2533D" stroke="#1B1D26" stroke-width="3"/>'
            s += f'<path d="M{f(x - 18)} {f(y + 14)} V{f(y - 6)} h6 v-6 h6 v6 h4 v-6 h6 v6 h4 v-6 h6 v6 h4 V{f(y + 14)} Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
        else:
            renk = "#7B3F8C" if k == "H" else "#F0A21A"
            s += f'<path d="M{f(x)} {f(y - 30)} L{f(x + 30)} {f(y)} L{f(x)} {f(y + 30)} L{f(x - 30)} {f(y)} Z" fill="{renk}" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 9)}" text-anchor="middle" {B} font-size="25" fill="#FFFFFF">{k}</text>'
    x, y = KONUM["1"]
    s += f'<path d="M{f(x - 36)} {f(y + 38)} v-64" stroke="#1B1D26" stroke-width="4"/><path d="M{f(x - 34)} {f(y - 24)} h44 l-10 13 l10 13 h-44 Z" fill="#E2533D" stroke="#1B1D26" stroke-width="2.4"/>'
    # Dicle yazısı
    s += halolu_yazi(f'x="1420" y="1048" text-anchor="middle" {B} font-size="50" transform="rotate(-2 1420 1048)"', "Dicle", "#FFFFFF", "#0A5A66", 1.6)
    s += halolu_yazi(f'x="1600" y="400" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" letter-spacing="1.5"', "BATMAN ÇAYI", "#FFFFFF", "#0A5A66", 1.2)
    for k, (x, y, o) in enumerate(((1000, 200, 1.1), (1066, 232, .8), (520, 150, .7), (580, 176, .5))):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    px, py = 1990, 150
    s += f'<circle cx="{px}" cy="{py}" r="64" fill="#FFFFFF" opacity=".9" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 56, 12, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 28), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="9" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 70}" text-anchor="middle" {B} font-size="28" fill="#FFFFFF">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), dict(KONUM)


# ================================================================== BİLGİ GRAFİKLERİ ({{info|ad|…}})

def korunum_semasi(onek="dc-kor"):
    """Kapalı kapta 2Cu + O2 → 2CuO: atomlar sayılır, terazi aynı kütleyi gösterir (12,8 + 3,2 = 16,0 g)."""
    s = Svg(onek)
    Wd, Hd = 1000, 380
    s += f'<rect width="{Wd}" height="{Hd}" rx="26" fill="#FFF6E6"/>'
    for i, (x0, baslik, ic) in enumerate(((40, "önce", [("Cu", 150, 150), ("Cu", 260, 190), ("O2", 210, 110)]),
                                           (600, "sonra", [("CuO", 690, 130), ("CuO", 790, 200)]))):
        s += f'<path d="M{x0 + 30} 70 h300 v220 q0 26 -26 26 h-248 q-26 0 -26 -26 Z" fill="#EAF7F8" stroke="{OBS}" stroke-width="4"/>'
        s += f'<rect x="{x0 + 20}" y="54" width="320" height="22" rx="8" fill="#9AA6B0" stroke="{OBS}" stroke-width="4"/>'
        for tur, x, y in ic:
            s += molekul_grup(s, tur, x, y, 22)
        s += f'<path d="M{x0} 336 h360" stroke="{OBS}" stroke-width="5"/><rect x="{x0 + 110}" y="318" width="140" height="40" rx="10" fill="#1B1D26"/>'
        s += f'<text x="{x0 + 180}" y="347" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="26" fill="#7FF0B0">16,0 g</text>'
        s += f'<text x="{x0 + 180}" y="40" text-anchor="middle" {T} font-size="28" fill="{GUM_K}">{baslik}</text>'
    s += f'<path d="M440 190 h110" stroke="{OBS}" stroke-width="7" stroke-linecap="round"/><path d="M548 172 l26 18 l-26 18 Z" fill="{OBS}"/>'
    s += f'<text x="495" y="150" text-anchor="middle" {B} font-size="30" fill="{KEH_K}">ısı</text>'
    s += f'<text x="500" y="250" text-anchor="middle" {T} font-size="22" fill="{GUM_K}">2 Cu · 2 O</text>'
    s += f'<text x="500" y="280" text-anchor="middle" {T} font-size="22" fill="{GUM_K}">= 2 Cu · 2 O</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info korunum")


def iki_yaka(onek="dc-iki"):
    """Denkleştirme: Dicle'nin iki yakasında atom sayımı (C3H8 + 5O2 → 3CO2 + 4H2O): C 3 · H 8 · O 10."""
    s = Svg(onek)
    Wd, Hd = 1000, 330
    g = s.lin([(0, "#BFE7E3"), (1, "#5FC2C0")], 0, 0, 0, 1, ad="su")
    s += f'<rect width="{Wd}" height="{Hd}" rx="26" fill="#F4EBD6"/>'
    s += f'<path d="M430 0 C470 120 440 220 470 {Hd} H560 C530 220 560 120 520 0 Z" fill="{g}"/>'
    s += S.dalga_cizgileri(440, 30, 100, 280, 7, n=8, op=.7, k=2)
    satir = [("C", 3, ATOM["C"]), ("H", 8, "#E9EEF2"), ("O", 10, ATOM["O"])]
    for yaka, x0 in (("sol", 40), ("sag", 600)):
        for j, (el, n, renk) in enumerate(satir):
            y = 80 + j * 82
            s += f'<text x="{x0}" y="{y + 12}" {B} font-size="38" fill="{OBS}">{el}</text>'
            for k in range(n):
                s += kure(s, x0 + 56 + k * 30, y, 12, renk)
            s += f'<text x="{x0 + 360}" y="{y + 12}" text-anchor="end" {B} font-size="34" fill="{GOL_K}">{n}</text>'
    s += f'<text x="215" y="40" text-anchor="middle" {B} font-size="28" fill="{OBS}">C<tspan dy="7" font-size="19">3</tspan><tspan dy="-7">H</tspan><tspan dy="7" font-size="19">8</tspan><tspan dy="-7"> + 5O</tspan><tspan dy="7" font-size="19">2</tspan></text>'
    s += f'<text x="790" y="40" text-anchor="middle" {B} font-size="28" fill="{OBS}">3CO<tspan dy="7" font-size="19">2</tspan><tspan dy="-7"> + 4H</tspan><tspan dy="7" font-size="19">2</tspan><tspan dy="-7">O</tspan></text>'
    s += f'<path d="M455 300 L545 300" stroke="{OBS}" stroke-width="6"/><path d="M540 286 l20 14 l-20 14 Z" fill="{OBS}"/>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info iki-yaka")


def oran_koprusu(onek="dc-kop"):
    """Katsayı köprüsü: verilen → (÷M, ÷N_A) → mol A → × kB/kA (köprü) → mol B → (×M, ×N_A) → istenen."""
    s = Svg(onek)
    Wd, Hd = 1100, 430
    g = s.lin([(0, "#FFE9C4"), (1, "#F7D3A0")], 0, 0, 0, 1, ad="gk")
    s += f'<rect width="{Wd}" height="{Hd}" rx="26" fill="{g}"/>'
    su = s.lin([(0, "#8FD8D4"), (1, "#2A9FA6")], 0, 330, 0, Hd, kull="userSpaceOnUse", ad="su")
    s += f'<path d="M0 340 C300 330 800 350 1100 336 V{Hd - 26} Q1100 {Hd} 1074 {Hd} H26 Q0 {Hd} 0 {Hd - 26} Z" fill="{su}"/>'
    s += malabadi_kopru(s, 330, 770, 352, 210, renk="#D9BC8A")

    def kutu(x, y, w, h_, renk, ust, alt):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h_}" rx="18" fill="{renk}" stroke="{OBS}" stroke-width="4"/>'
                f'<text x="{x + w / 2}" y="{y + 44}" text-anchor="middle" {B} font-size="34" fill="{OBS}">{ust}</text>'
                f'<text x="{x + w / 2}" y="{y + 80}" text-anchor="middle" {T} font-size="24" fill="{GUM_K}">{alt}</text>')
    s += kutu(30, 150, 230, 100, "#FFFFFF", "verilen", "g · tane · mol")
    s += kutu(840, 150, 230, 100, "#FFFFFF", "istenen", "g · tane · mol")
    s += kutu(290, 60, 170, 92, GOL, "mol A", "n")
    s += kutu(640, 60, 170, 92, GOL, "mol B", "n")
    s += f'<path d="M260 200 Q300 200 310 160" stroke="{OBS}" stroke-width="5" fill="none"/><path d="M790 160 Q800 200 840 200" stroke="{OBS}" stroke-width="5" fill="none"/>'
    s += f'<path d="M462 104 H630" stroke="{OBS}" stroke-width="6"/><path d="M626 90 l22 14 l-22 14 Z" fill="{OBS}"/>'
    s += f'<rect x="465" y="18" width="170" height="44" rx="22" fill="{KEH}" stroke="{OBS}" stroke-width="4"/>'
    s += f'<text x="550" y="49" text-anchor="middle" {B} font-size="28" fill="{OBS}">× k<tspan dy="6" font-size="18">B</tspan><tspan dy="-6"> / k</tspan><tspan dy="6" font-size="18">A</tspan></text>'
    s += f'<text x="150" y="290" text-anchor="middle" {T} font-size="23" fill="{OBS}">÷ M<tspan dy="5" font-size="16">A</tspan><tspan dy="-5"> ya da ÷ N</tspan><tspan dy="5" font-size="16">A</tspan></text>'
    s += f'<text x="950" y="290" text-anchor="middle" {T} font-size="23" fill="{OBS}">× M<tspan dy="5" font-size="16">A</tspan><tspan dy="-5"> ya da × N</tspan><tspan dy="5" font-size="16">A</tspan></text>'
    s += f'<text x="550" y="410" text-anchor="middle" {T} font-size="24" fill="#FFFFFF">katsayılar mol köprüsüdür · kütle köprüsü değil</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info kopru")


def _eksen(s, x0, y0, x1, y1, xet, yet, xticks, yticks):
    o = []
    for v, lab in yticks:
        yy = y0 - (y0 - y1) * v
        o.append(f'<path d="M{x0} {f(yy)} H{x1}" stroke="#DCE4E8" stroke-width="2"/><text x="{x0 - 10}" y="{f(yy + 9)}" text-anchor="end" {T} font-size="26">{lab}</text>')
    for v, lab in xticks:
        xx = x0 + (x1 - x0) * v
        o.append(f'<text x="{f(xx)}" y="{y0 + 34}" text-anchor="middle" {T} font-size="26">{lab}</text>')
    o.append(f'<path d="M{x0} {y1 - 14} V{y0} H{x1 + 14}" stroke="{OBS}" stroke-width="4" fill="none"/>')
    o.append(f'<text x="{x1}" y="{y0 + 66}" text-anchor="end" {T} font-size="24" fill="{GUM_K}">{xet}</text>')
    o.append(f'<text x="{x0 - 2}" y="{y1 - 22}" {T} font-size="24" fill="{GUM_K}">{yet}</text>')
    return "".join(o)


# Grafik verileri — çizim ve uretec/dogrula.py aynı sayıları okur: (madde, başlangıç molü, son mol)
MOL_ZAMAN = {"durak": [("X", 3, 1), ("Y", 4, 0), ("Z", 0, 2)],
             "kissa": [("N2", 1.0, .6), ("H2", 1.2, 0), ("NH3", 0, .8)]}
# Üstad 3: sabit O2 ile artan Mg; kırılma noktası (Mg g, MgO g) ve x ekseninin sonu (g)
USTAD_GRAFIK = dict(kirilma=(9.6, 16), mg_son=14.4)


def mol_zaman(onek="dc-mz", tur="durak"):
    """Mol–zaman grafiği (veri: MOL_ZAMAN[tur]). durak: X + 2Y → Z; kissa: N2 + 3H2 → 2NH3."""
    s = Svg(onek)
    Wd, Hd = 620, 440
    x0, y0, x1, y1 = 96, 360, 590, 50
    s += f'<rect width="{Wd}" height="{Hd}" rx="18" fill="#FFFFFF"/>'
    if tur == "durak":
        ymax, tick = 4, [(i / 4, str(i)) for i in range(5)]
    else:
        ymax, tick = 1.2, [(i / 6, f"{i * .2:.1f}".replace(".", ",")) for i in range(7)]

    def etiket(ad):
        return ad[:-1] + f'<tspan dy="7" font-size="20">{ad[-1]}</tspan>' if ad[-1].isdigit() else ad
    seri = [(etiket(ad), a, b, c) for (ad, a, b), c in zip(MOL_ZAMAN[tur], (MER, KOB, ZUMRUT))]
    s += _eksen(s, x0, y0, x1, y1, "zaman", "mol", [(0, "0"), (.62, "t")], tick)
    tx = x0 + (x1 - x0) * .62
    s += f'<path d="M{f(tx)} {y0} V{y1}" stroke="{GUM}" stroke-width="2.4" stroke-dasharray="8 7"/>'
    for ad, a, b, c in seri:
        ya = y0 - (y0 - y1) * a / ymax
        yb = y0 - (y0 - y1) * b / ymax
        s += f'<path d="M{x0} {f(ya)} C{f(x0 + (tx - x0) * .45)} {f(ya + (yb - ya) * .8)} {f(tx - 40)} {f(yb)} {f(tx)} {f(yb)} H{x1}" stroke="{c}" stroke-width="6" fill="none"/>'
        s += f'<text x="{x1 - 4}" y="{f(yb - 12)}" text-anchor="end" {B} font-size="30" fill="{c}">{ad}</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info grafik")


def sinirlayici_tanecik(onek="dc-sin"):
    """4 H2 + 3 O2 → 4 H2O + 1 O2 artar: sayıca fazla olan H2 sınırlayıcıdır."""
    s = Svg(onek)
    Wd, Hd = 900, 330
    s += f'<rect width="{Wd}" height="{Hd}" rx="24" fill="#FFF6E6"/>'
    for x0, bas in ((30, "başlangıç"), (500, "sonuç")):
        s += f'<rect x="{x0}" y="50" width="370" height="250" rx="20" fill="#FFFFFF" stroke="{OBS}" stroke-width="4"/>'
        s += f'<text x="{x0 + 185}" y="36" text-anchor="middle" {T} font-size="26" fill="{GUM_K}">{bas}</text>'
    for k, (x, y) in enumerate(((100, 110), (210, 100), (110, 200), (220, 190))):
        s += molekul_grup(s, "H2", x, y, 18)
    for k, (x, y) in enumerate(((320, 110), (320, 200), (180, 260))):
        s += molekul_grup(s, "O2", x, y, 18)
    for k, (x, y) in enumerate(((580, 100), (700, 100), (580, 200), (700, 200))):
        s += molekul_grup(s, "H2O", x, y, 20)
    s += molekul_grup(s, "O2", 810, 150, 18)
    s += f'<rect x="760" y="190" width="104" height="40" rx="20" fill="{KEH}" stroke="{OBS}" stroke-width="3"/><text x="812" y="219" text-anchor="middle" {B} font-size="24" fill="{OBS}">artan</text>'
    s += f'<path d="M412 175 h70" stroke="{OBS}" stroke-width="6"/><path d="M478 161 l22 14 l-22 14 Z" fill="{OBS}"/>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info sinir")


def verim_saati(onek="dc-ver", yuzde=80):
    """Verim göstergesi: gerçek / teorik."""
    s = Svg(onek)
    Wd, Hd = 520, 330
    cx, cy, R = 260, 250, 190
    s += f'<rect width="{Wd}" height="{Hd}" rx="22" fill="#FFFFFF"/>'
    for i in range(10):
        a0 = math.pi + math.pi * i / 10
        a1 = math.pi + math.pi * (i + 1) / 10
        c = karis("#E2533D", "#1F8A5B", i / 9)
        s += (f'<path d="M{f(cx + R * math.cos(a0))} {f(cy + R * math.sin(a0))} A{R} {R} 0 0 1 {f(cx + R * math.cos(a1))} {f(cy + R * math.sin(a1))} '
              f'L{f(cx + (R - 46) * math.cos(a1))} {f(cy + (R - 46) * math.sin(a1))} A{R - 46} {R - 46} 0 0 0 {f(cx + (R - 46) * math.cos(a0))} {f(cy + (R - 46) * math.sin(a0))} Z" fill="{c}" stroke="#FFFFFF" stroke-width="3"/>')
    for v in (0, 50, 100):
        a = math.pi + math.pi * v / 100
        s += f'<text x="{f(cx + (R + 26) * math.cos(a))}" y="{f(cy + (R + 26) * math.sin(a) + 10)}" text-anchor="middle" {T} font-size="24">%{v}</text>'
    a = math.pi + math.pi * yuzde / 100
    s += f'<path d="M{cx} {cy} L{f(cx + (R - 30) * math.cos(a))} {f(cy + (R - 30) * math.sin(a))}" stroke="{OBS}" stroke-width="9" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="16" fill="{KEH}" stroke="{OBS}" stroke-width="4"/>'
    s += f'<text x="{cx}" y="{cy - 60}" text-anchor="middle" {B} font-size="54" fill="{OBS}">%{yuzde}</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info verim")


def saflik_tasi(onek="dc-saf"):
    """Kireç taşı örneği: %75 CaCO3, %25 kil-kum (saflık)."""
    s = Svg(onek)
    Wd, Hd = 520, 330
    s += f'<rect width="{Wd}" height="{Hd}" rx="22" fill="#FFFFFF"/>'
    pts = [(70, 250), (100, 110), (220, 70), (360, 90), (430, 200), (390, 270), (200, 290)]
    g = s.lin([(0, "#F3E7C8"), (1, "#C9B48A")], 0, 0, 1, 1, ad="ts")
    s += f'<path d="{cizgi_d(pts, True)}" fill="{g}" stroke="{OBS}" stroke-width="4" stroke-linejoin="round"/>'
    r = RNG(9)
    for _ in range(30):
        x = r.uniform(120, 380)
        y = r.uniform(110, 260)
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(3, 7))}" fill="{r.choice(["#9C7A54", "#7E6A58", "#B98E5A"])}" opacity=".8"/>'
    s += f'<rect x="40" y="300" width="440" height="22" rx="11" fill="#9C7A54" stroke="{OBS}" stroke-width="3"/>'
    s += f'<rect x="40" y="300" width="330" height="22" rx="11" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    s += f'<text x="205" y="40" text-anchor="middle" {B} font-size="34" fill="{OBS}">%75 CaCO<tspan dy="7" font-size="22">3</tspan></text>'
    s += f'<text x="440" y="40" text-anchor="middle" {T} font-size="24" fill="{GUM_K}">%25 kil</text>'
    return s.cikti(f"0 0 {Wd} {Hd + 6}", cls="info saflik")


def bakir_zinciri(onek="dc-zin"):
    """Ardışık tepkimeler: malakit → CuO → Cu; Cu atomu zincir boyunca korunur (0,2 → 0,4 → 0,4 mol)."""
    s = Svg(onek)
    Wd, Hd = 1000, 300
    s += f'<rect width="{Wd}" height="{Hd}" rx="24" fill="#FFF6E6"/>'
    halka = [(170, "malakit", "#1F8A5B", "0,2 mol"), (500, "CuO", "#3A3F4B", "0,4 mol"), (830, "Cu", BAKIR, "0,4 mol")]
    for i, (x, ad, renk, mol) in enumerate(halka):
        s += f'<rect x="{x - 130}" y="80" width="260" height="130" rx="65" fill="none" stroke="{OBS}" stroke-width="22"/>'
        s += f'<rect x="{x - 130}" y="80" width="260" height="130" rx="65" fill="none" stroke="{acik(renk, .25)}" stroke-width="12"/>'
        s += f'<circle cx="{x}" cy="145" r="44" fill="{renk}" stroke="{OBS}" stroke-width="4"/>'
        s += f'<text x="{x}" y="250" text-anchor="middle" {B} font-size="32" fill="{OBS}">{ad}</text>'
        s += f'<text x="{x}" y="52" text-anchor="middle" {B} font-size="30" fill="{KEH_K}">{mol}</text>'
    s += f'<text x="335" y="290" text-anchor="middle" {T} font-size="22" fill="{GUM_K}">ısı</text><text x="665" y="290" text-anchor="middle" {T} font-size="22" fill="{GUM_K}">+ karbon</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info zincir")


def lpg_tupu(onek="dc-lpg"):
    """Tüp gaz: propan + bütan karışımı (temsilî)."""
    s = Svg(onek)
    Wd, Hd = 420, 360
    s += f'<rect width="{Wd}" height="{Hd}" rx="22" fill="#FFFFFF"/>'
    g = s.lin([(0, "#F07A5A"), (.4, "#E2533D"), (1, "#A12817")], 0, 0, 1, 0, ad="tp")
    s += f'<rect x="90" y="60" width="240" height="270" rx="80" fill="{g}" stroke="{OBS}" stroke-width="5"/>'
    s += f'<rect x="170" y="24" width="80" height="44" rx="10" fill="#9AA6B0" stroke="{OBS}" stroke-width="4"/>'
    s += f'<rect x="110" y="150" width="200" height="140" rx="22" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    p = _mol_ic(s, "C3H8", (10, 25, 0), 22)
    b = _mol_ic(s, "C4H10", (10, 15, 0), 20)
    s += f'<g transform="translate(160 190)">{p}</g><g transform="translate(250 250)">{b}</g>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info lpg")


def mg_denemeleri(onek="dc-mg"):
    """Üç deney tüpünde magnezyum şerit + HCl; kabarcıklar (temsilî)."""
    s = Svg(onek)
    Wd, Hd = 520, 330
    s += f'<rect width="{Wd}" height="{Hd}" rx="20" fill="#FFFFFF"/>'
    s += f'<rect x="40" y="250" width="440" height="20" rx="6" fill="#9A6B42" stroke="{OBS}" stroke-width="3"/>'
    r = RNG(5)
    for i, x in enumerate((130, 260, 390)):
        s += f'<path d="M{x - 34} 60 V230 Q{x - 34} 262 {x} 262 Q{x + 34} 262 {x + 34} 230 V60" fill="#EAF7F8" stroke="{OBS}" stroke-width="4"/>'
        s += f'<path d="M{x - 30} 140 V230 Q{x - 30} 258 {x} 258 Q{x + 30} 258 {x + 30} 230 V140 Z" fill="#BFE7EF"/>'
        s += f'<path d="M{x - 8} 236 l16 -50" stroke="#9AA6B0" stroke-width="7" stroke-linecap="round"/>'
        for _ in range(7):
            s += f'<circle cx="{f(x + r.uniform(-20, 20))}" cy="{f(r.uniform(150, 230))}" r="{f(r.uniform(3, 6))}" fill="#FFFFFF" stroke="#5FB3C2" stroke-width="1.6"/>'
        s += f'<text x="{x}" y="310" text-anchor="middle" {B} font-size="34" fill="{OBS}">{i + 1}</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info mg")


def ustad_grafik(onek="dc-ust"):
    """Sabit 6,4 g O2 ile artan kütlede Mg yakılıyor: oluşan MgO kütlesi – alınan Mg kütlesi (kırılma 9,6 g; 16 g)."""
    s = Svg(onek)
    Wd, Hd = 560, 420
    x0, y0, x1, y1 = 110, 340, 530, 50
    s += f'<rect width="{Wd}" height="{Hd}" rx="16" fill="#FFFFFF"/>'
    s += _eksen(s, x0, y0, x1, y1, "Mg kütlesi (g)", "MgO (g)", [(0, "0"), (1 / 3, "4,8"), (2 / 3, "9,6"), (1, "14,4")],
                [(0, "0"), (.25, "4"), (.5, "8"), (.75, "12"), (1, "16")])
    (mg_k, mgo_k), mg_son = USTAD_GRAFIK["kirilma"], USTAD_GRAFIK["mg_son"]
    xa = x0 + (x1 - x0) * mg_k / mg_son
    y1 = y0 - (y0 - y1) * mgo_k / 16
    s += f'<path d="M{x0} {y0} L{f(xa)} {f(y1)} H{x1}" stroke="{LAJVER}" stroke-width="6" fill="none"/>'
    s += f'<path d="M{f(xa)} {y0} V{f(y1)}" stroke="{ALTIN}" stroke-width="2.6" stroke-dasharray="8 7"/>'
    s += f'<circle cx="{f(xa)}" cy="{f(y1)}" r="10" fill="#FFFFFF" stroke="{LAJVER}" stroke-width="5"/>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info ugraf")


def cezeri_duzenek(onek="dc-cez"):
    """el-Cezerî esinli su düzeneği (temsilî): hazne, şamandıra, ip-makara, dişliler. Eserin birebir kopyası DEĞİL."""
    s = Svg(onek)
    Wd, Hd = 400, 360
    g = s.rad([(0, "#FFF7E0"), (1, "#F2DFB0")], .5, .45, .7, ad="cz")
    s += f'<rect width="{Wd}" height="{Hd}" rx="18" fill="{g}"/>'
    pir = s.lin([(0, "#F7E3A1"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="pr")
    s += f'<rect x="40" y="150" width="130" height="170" rx="10" fill="#BFE7EF" stroke="{OBS}" stroke-width="4"/>'
    s += f'<rect x="44" y="210" width="122" height="106" fill="#5FB3C2" opacity=".6"/>'
    s += f'<rect x="78" y="196" width="54" height="26" rx="8" fill="{pir}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M105 196 V70 H250" stroke="{OBS}" stroke-width="3" fill="none"/>'
    for cx, cy, R, n in ((250, 90, 46, 12), (318, 160, 34, 9)):
        dis = []
        for k in range(n * 2):
            a = math.pi * k / n
            rr = R if k % 2 == 0 else R * .8
            dis.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        s += f'<path d="{cizgi_d(dis, True)}" fill="{pir}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="{R * .3}" fill="#FFF7E0" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M318 194 V300" stroke="{OBS}" stroke-width="5"/><rect x="290" y="300" width="56" height="20" rx="6" fill="{pir}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M105 120 q-14 -16 0 -32" stroke="#5FB3C2" stroke-width="5" fill="none"/>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info cezeri")
