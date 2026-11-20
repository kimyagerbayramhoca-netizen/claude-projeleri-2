"""Katla sayfaları · çizimler (ortak kütüphaneye taşınabilir: cizim/katla.py).

MEKANİK. Sayfada iki dikey kat çizgisi var: A (x = 70 mm) ve B (x = 140 mm). Öğrenci orta şeridi (70–140) arkaya iter,
A kenarını B kenarına getirir: SOL parça (0–70) ile SAĞ parça (140–210) yan yana gelir. Dört satır aynı iki çizgiyi
paylaşır; tek katlama dördünü birden tamamlar.

KOORDİNATLAR. Sayfa mm cinsindendir (viewBox 0 0 210 297). "Katlı uzay" u ∈ [0, 140], dikiş u = 70:
u < 70 → sayfada x = u (sol parça) · u > 70 → sayfada x = u + 70 (sağ parça).
Dikişi geçen her şey (ok, hale, bölünmüş yazı, ürün kabı) katlı uzayda TEK parça çizilir ve sayfaya iki kez basılır
(Sayfa.dikis): solda x ≤ 70 + TASMA'ya, sağda x ≥ 140 − TASMA'ya kırpılır. Böylece yarımlar kesinlikle hizalıdır;
TASMA (1 mm) orta şeride taşan paydır: ±1 mm kat hatasında dikişte beyaz boşluk kalmaz.

KURALLAR (dogrula.py denetler): dikişi geçen çizgi ≥ 0,6 mm (kılcal çizgi yok) · dikişe komşu ama onu geçmeyen her öge
dikişten ≥ 1,2 mm içeride · ürün adı/formülü hiçbir parçada tam olarak yazılı değil (harf dikişte ikiye bölünür) ·
satır zemini üç parçada da aynı renk (kat hatasında renk sıçraması olmaz) · anlam yalnız renkle verilmez
(sol atomun elektronu ●, sağ atomunki ×, boş yer kesik çember; kat işaretleri A/B harfli şekiller).

Yazı genişlikleri fontTools ile fontun kendi ölçülerinden hesaplanır (bölünen harf tam dikişe ortalanır).
"""
import math
import os

from fontTools.ttLib import TTFont

from cizim.temel import f, cizgi_d
from cizim.renkler import (OBS, OBS2, SOLUK, GOL, GOL_K, GOL_A, GOL_AA, KEH, KEH_K, KEH_A, MER, MER_K, KOB_K, GUM_K, ATOM)
import konu_karakterleri as KK

A_X, B_X = 70.0, 140.0
TASMA = 1.0                 # dikişi geçen şekillerin orta şeride taşma payı (mm)
PAY = 2.25                  # dikişe komşu elektronun merkezinin dikişe uzaklığı (yarıçap 1,05 + 1,2 mm güven payı)
E_R = 1.05                  # elektron yarıçapı
RK = (6.0, 9.4, 12.8)       # K, L, M katman yarıçapları (mm)
ELEKTRON, E_KOYU = "#2B50B5", "#13235E"
FONTLAR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "fontlar"))
_DOSYA = {"baloo": "baloobhaijaan2/static/BalooBhaijaan2-800.ttf", "nunito": "nunito/static/Nunito-800.ttf", "nunito9": "nunito/static/Nunito-900.ttf"}
_AILE = {"baloo": 'font-family="Baloo Bhaijaan 2" font-weight="800"', "nunito": 'font-family="Nunito" font-weight="800"',
         "nunito9": 'font-family="Nunito" font-weight="900"'}
_F = {}
K_ALT = .66


# ------------------------------------------------------------------ yazı (ölçülü)

def _font(ad):
    if ad not in _F:
        t = TTFont(os.path.join(FONTLAR, _DOSYA[ad]))
        _F[ad] = (t.getBestCmap(), t["hmtx"].metrics, t["head"].unitsPerEm)
    return _F[ad]


def _parcalar(metin):
    """'H_2O', 'e^{−}', '_{11}Na' → [(metin, 'n' | 'alt' | 'ust')]"""
    out, buf, i = [], "", 0
    while i < len(metin):
        c = metin[i]
        if c in "_^" and i + 1 < len(metin):
            if buf:
                out.append((buf, "n"))
                buf = ""
            mod = "alt" if c == "_" else "ust"
            if metin[i + 1] == "{":
                j = metin.index("}", i)
                out.append((metin[i + 2:j], mod))
                i = j + 1
            else:
                out.append((metin[i + 1], mod))
                i += 2
        else:
            buf += c
            i += 1
    if buf:
        out.append((buf, "n"))
    return out


def genislik(metin, boy, font="baloo"):
    cmap, hm, upm = _font(font)
    w = 0.0
    for t, m in _parcalar(metin):
        for ch in t:
            g = cmap.get(ord(ch))
            if g is None:
                raise ValueError(f"fontta yok: {ch!r} ({font}) · metin: {metin}")
            w += hm[g][0] / upm * boy * (1 if m == "n" else K_ALT)
    return w


def duz(metin):
    """Ölçülü yazım → düz metin (dogrula için): 'H_2O' → 'H2O', 'e^{−}' → 'e−'."""
    return "".join(t for t, _ in _parcalar(metin))


def yazi(metin, x, y, boy, renk=OBS, font="baloo", hiza="sol"):
    """SVG yazısı (kontur yok). hiza: sol | sag | orta. Dönen: (svg, x0, x1)."""
    w = genislik(metin, boy, font)
    x0 = x if hiza == "sol" else (x - w if hiza == "sag" else x - w / 2)
    o = [f'<text x="{f(x0, 2)}" y="{f(y, 2)}" {_AILE[font]} font-size="{f(boy, 2)}" fill="{renk}">']
    dy = 0.0
    for t, m in _parcalar(metin):
        t = t.replace("&", "&amp;").replace("<", "&lt;")
        if m == "n":
            o.append(f'<tspan dy="{f(-dy, 2)}">{t}</tspan>' if dy else t)
            dy = 0.0
        else:
            hedef = boy * .22 if m == "alt" else -boy * .36
            o.append(f'<tspan dy="{f(hedef - dy, 2)}" font-size="{f(boy * K_ALT, 2)}">{t}</tspan>')
            dy = hedef
    o.append("</text>")
    return "".join(o), x0, x0 + w


def bolunmus(sol, kesik, sag, y, boy, renk=OBS, font="baloo"):
    """Dikişte bölünen satır (katlı uzay): 'kesik' harfi tam u = 70'e ortalanır. Dönen: (svg, u0, u1)."""
    wk = genislik(kesik, boy, font) if kesik else 0.0
    u0 = A_X - wk / 2 - genislik(sol, boy, font)
    return yazi(sol + kesik + sag, u0, y, boy, renk, font)


class Sayfa:
    """Bir katla sayfasının tam sayfa SVG'si."""

    def __init__(self, onek):
        self.onek = onek
        self.o = []
        self.dikis_parcalari = []          # dogrula: dikişi geçen parçaların SVG'si

    def ekle(self, s):
        self.o.append(s)

    def dikis(self, frag):
        """Katlı uzayda çizilmiş parçayı sola ve sağa (70 mm kaydırıp) kırparak basar."""
        self.dikis_parcalari.append(frag)
        self.o.append(f'<g clip-path="url(#{self.onek}-kL)">{frag}</g>'
                      f'<g transform="translate({f(B_X - A_X)} 0)"><g clip-path="url(#{self.onek}-kR)">{frag}</g></g>')

    def cikti(self):
        defs = (f'<defs><clipPath id="{self.onek}-kL"><rect x="-5" y="0" width="{f(A_X + 5 + TASMA)}" height="297"/></clipPath>'
                f'<clipPath id="{self.onek}-kR"><rect x="{f(A_X - TASMA)}" y="0" width="90" height="297"/></clipPath></defs>')
        return f'<svg class="katla-svg" viewBox="0 0 210 297" data-serbest="">{defs}{"".join(self.o)}</svg>'


# ------------------------------------------------------------------ küçük parçalar

def _ok(x0, y0, x1, y1, renk=GUM_K, k=.6, uc=1.9):
    a = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - uc * math.cos(a - .45), y1 - uc * math.sin(a - .45))
    p2 = (x1 - uc * math.cos(a + .45), y1 - uc * math.sin(a + .45))
    return (f'<path d="M{f(x0, 2)} {f(y0, 2)} L{f(x1 - uc * .6 * math.cos(a), 2)} {f(y1 - uc * .6 * math.sin(a), 2)}" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"/>'
            f'<path d="M{f(x1, 2)} {f(y1, 2)} L{f(p1[0], 2)} {f(p1[1], 2)} L{f(p2[0], 2)} {f(p2[1], 2)} Z" fill="{renk}"/>')


def _egri_ok(p0, c, p1, renk, k=.9, uc=2.3):
    a = math.atan2(p1[1] - c[1], p1[0] - c[0])
    q1 = (p1[0] - uc * math.cos(a - .5), p1[1] - uc * math.sin(a - .5))
    q2 = (p1[0] - uc * math.cos(a + .5), p1[1] - uc * math.sin(a + .5))
    son = (p1[0] - uc * .6 * math.cos(a), p1[1] - uc * .6 * math.sin(a))
    return (f'<path d="M{f(p0[0], 2)} {f(p0[1], 2)} Q{f(c[0], 2)} {f(c[1], 2)} {f(son[0], 2)} {f(son[1], 2)}" fill="none" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"/>'
            f'<path d="M{f(p1[0], 2)} {f(p1[1], 2)} L{f(q1[0], 2)} {f(q1[1], 2)} L{f(q2[0], 2)} {f(q2[1], 2)} Z" fill="{renk}"/>')


def _nokta_satir(x0, x1, y):
    return f'<path d="M{f(x0)} {f(y)} H{f(x1)}" stroke="{OBS2}" stroke-width=".32" stroke-dasharray=".1 1.15" stroke-linecap="round"/>'


def _cip(x, y, metin, zemin=GOL_A, renk=GOL_K):
    svg, x0, x1 = yazi(metin, x + 1.8, y + 3.05, 2.5, renk, "nunito9")
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(x1 - x0 + 3.6)}" height="4.3" rx="2.15" fill="{zemin}"/>' + svg


def _no(x, y, n, renk=OBS):
    svg, _, _ = yazi(str(n), x, y + 1.25, 3.5, "#FFFFFF", "baloo", "orta")
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="2.9" fill="{renk}"/>' + svg


# ------------------------------------------------------------------ atom (Bohr halkaları; nokta–çarpı elektronlar)

def _elektron(x, y, isaret):
    if isaret == "nokta":
        return f'<circle cx="{f(x, 2)}" cy="{f(y, 2)}" r="{E_R}" fill="{ELEKTRON}" stroke="{E_KOYU}" stroke-width=".3"/>'
    d = E_R * .78
    return (f'<path d="M{f(x - d, 2)} {f(y - d, 2)} L{f(x + d, 2)} {f(y + d, 2)} M{f(x + d, 2)} {f(y - d, 2)} L{f(x - d, 2)} {f(y + d, 2)}" '
            f'stroke="{E_KOYU}" stroke-width=".62" stroke-linecap="round"/>')


def _bos(x, y):
    return f'<circle cx="{f(x, 2)}" cy="{f(y, 2)}" r="{E_R + .1}" fill="#FFFFFF" stroke="{OBS}" stroke-width=".3" stroke-dasharray=".7 .5"/>'


def atom(cx, cy, katman, sembol, yon, deger, bos=(), isaret="nokta"):
    """Tam Bohr çizimi. katman: [2, 8, 1] · yon: +1 dikiş sağda, −1 dikiş solda ·
    deger / bos: dış katmandaki elektronların / boş yerlerin açıları (derece; 0 = dikiş yönü, + = yukarı).
    Dönen: (svg, [(x, y) dış katman elektronları], [(x, y) boş yerler])."""
    renk = ATOM[sembol]
    acik_renk = sembol in ("H",)
    o = ['<g data-tema-sabit="">']
    n = len(katman)
    for k in range(n):
        o.append(f'<circle cx="{f(cx, 2)}" cy="{f(cy, 2)}" r="{RK[k]}" fill="none" stroke="{"#343947" if k == n - 1 else "#9FB2BC"}" stroke-width="{".42" if k == n - 1 else ".3"}"/>')

    def nokta(r, a):
        return cx + yon * r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))
    for k in range(n - 1):                          # iç katmanlar (dolu)
        adet = katman[k]
        for j in range(adet):
            a = (90 if adet == 2 else 22.5) + j * 360 / adet
            o.append(_elektron(*nokta(RK[k], a), isaret))
    dis, bosluk = [nokta(RK[n - 1], a) for a in deger], [nokta(RK[n - 1], a) for a in bos]
    assert len(deger) == katman[-1], (sembol, katman, deger)
    o += [_bos(*p) for p in bosluk] + [_elektron(*p, isaret) for p in dis]
    o.append(f'<circle cx="{f(cx, 2)}" cy="{f(cy, 2)}" r="3.3" fill="{renk}" stroke="#1B1D26" stroke-width=".4"/>')
    svg, _, _ = yazi(sembol, cx, cy + 1.05, 3.0 if len(sembol) > 1 else 3.4, "#1B1D26" if acik_renk or sembol == "Mg" else "#FFFFFF", "baloo", "orta")
    o.append(svg + "</g>")
    return "".join(o), dis, bosluk


def _cift(merkez):
    """Bir çift yuvası: merkez açısının ±13° iki yanı."""
    return [merkez - 13, merkez + 13]


def _hale(u, y, rx=4.9, ry=2.7, aci=0):
    """Ortak çift halesi (katlı uzay; dikişte ikiye bölünür)."""
    return (f'<ellipse cx="{f(u, 2)}" cy="{f(y, 2)}" rx="{rx}" ry="{ry}" transform="rotate({f(aci)} {f(u, 2)} {f(y, 2)})" '
            f'fill="#FFE9A8" stroke="{KEH_K}" stroke-width=".7"/>')


# ------------------------------------------------------------------ satır iskeleti

SATIR_Y0, SATIR_H, SATIR_ARA = 60.0, 49.5, 2.5
BANT = (GOL_AA, "#FFF7E3")


def satir_y(k):
    return SATIR_Y0 + k * (SATIR_H + SATIR_ARA)


def _bant(k):
    y = satir_y(k)
    return f'<rect x="3.5" y="{f(y)}" width="203" height="{SATIR_H}" rx="3.2" fill="{BANT[k % 2]}"/>'


def _orta_kart(y0, y1, cip, satirlar, ipucu=None):
    """Orta şeritteki çalışma kartı (x 76–134). satirlar: ['Ürün:', …] → her biri noktalı çizgi."""
    o = [f'<rect x="76" y="{f(y0)}" width="58" height="{f(y1 - y0)}" rx="2.4" fill="#FFFFFF" stroke="#CFDCE0" stroke-width=".35"/>', _cip(78, y0 + 1.6, cip)]
    y = y0 + 10.6
    for s in satirlar:
        svg, _, x1 = yazi(s, 78.2, y, 3.35, OBS, "nunito")
        o.append(svg + _nokta_satir(x1 + 1.4, 131.6, y + .2))
        y += 5.6
    if ipucu:
        svg, _, x1 = yazi("İPUCU", 78.2, y - .6, 2.4, KEH_K, "nunito9")
        o.append(svg)
        for j, satir in enumerate(ipucu):
            o.append(yazi(satir, x1 + 1.6 if j == 0 else 78.2, y - .6 + j * 3.7, 2.95, SOLUK, "nunito")[0])
    return "".join(o)


def _kat_isaretleri(s):
    """A ve B kat işaretleri: hepsi ORTA şerit tarafında (katlayınca görünmez), harfli dolu şekiller."""
    o = []
    for y in (14.2, 268.6):
        o.append(f'<path d="M70.5 {f(y + 2.8)} L73.5 {f(y)} H80.2 V{f(y + 5.6)} H73.5 Z" fill="{MER}"/>' + yazi("A", 76.9, y + 4.05, 3.7, "#FFFFFF", "baloo", "orta")[0])
        o.append(f'<path d="M139.5 {f(y + 2.8)} L136.5 {f(y)} H129.8 V{f(y + 5.6)} H136.5 Z" fill="{MER}"/>' + yazi("B", 133.1, y + 4.05, 3.7, "#FFFFFF", "baloo", "orta")[0])
    o.append(f'<path d="M70.95 20.4 V268 M139.05 20.4 V268" stroke="{MER}" stroke-width=".3" stroke-dasharray="1.3 1.5" opacity=".75"/>')
    for k in range(5):
        yg = satir_y(k) - SATIR_ARA / 2 if k < 4 else satir_y(3) + SATIR_H + SATIR_ARA / 2
        o.append(f'<path d="M71.2 {f(yg)} l2.1 -1.1 v2.2 Z M138.8 {f(yg)} l-2.1 -1.1 v2.2 Z" fill="{MER_K}"/>')
    s.ekle("".join(o))


def _nasil_katlanir(s):
    """Orta şeridin üstünde üç adımlı çizim."""
    o = []
    adimlar = (("A ve B’den", "arkaya bük"), ("orta şeridi", "arkaya it"), ("A, B’ye değsin:", "oku!"))
    for i, (a, b) in enumerate(adimlar):
        cx = 86.5 + i * 18.5
        o.append(_no(cx - 7.2, 28.6, i + 1, GOL_K).replace('r="2.9"', 'r="2.3"').replace('font-size="3.5"', 'font-size="2.9"'))
        if i == 0:      # düz sayfa, iki kesik çizgi, arkaya bükme okları
            o.append(f'<rect x="{f(cx - 5.4)}" y="28.2" width="12" height="9.6" rx=".6" fill="#FFFFFF" stroke="{OBS}" stroke-width=".4"/>'
                     f'<path d="M{f(cx - 1.4)} 28.2 v9.6 M{f(cx + 2.6)} 28.2 v9.6" stroke="{MER}" stroke-width=".4" stroke-dasharray=".9 .7"/>')
            o.append(yazi("A", cx - 1.4, 27.5, 2.2, MER_K, "nunito9", "orta")[0] + yazi("B", cx + 2.6, 27.5, 2.2, MER_K, "nunito9", "orta")[0])
        elif i == 1:    # üstten bakış: orta şerit arkaya (yukarı) kıvrılır, iki parça birbirine yaklaşır
            o.append(f'<path d="M{f(cx - 6.4)} 36.6 H{f(cx - 1.6)} L{f(cx + .6)} 29.6 L{f(cx + 2.8)} 36.6 H{f(cx + 7.6)}" fill="none" stroke="{OBS}" stroke-width=".7" stroke-linejoin="round" stroke-linecap="round"/>')
            o.append(_ok(cx - 6.2, 39.2, cx - 2.4, 39.2, MER_K, .5, 1.4) + _ok(cx + 7.4, 39.2, cx + 3.6, 39.2, MER_K, .5, 1.4))
            o.append(yazi("üstten", cx + .6, 28.4, 2.0, SOLUK, "nunito", "orta")[0])
        else:           # katlı: iki parça yan yana
            o.append(f'<rect x="{f(cx - 3.4)}" y="28.2" width="8" height="9.6" rx=".6" fill="#FFFFFF" stroke="{OBS}" stroke-width=".4"/>'
                     f'<path d="M{f(cx + .6)} 28.6 v8.8" stroke="{MER}" stroke-width=".4"/>')
            o.append(yazi("A", cx - .5, 27.5, 2.2, MER_K, "nunito9", "orta")[0] + yazi("B", cx + 1.8, 27.5, 2.2, MER_K, "nunito9", "orta")[0])
            o.append(f'<path d="M{f(cx + 7)} 30.4 l.7 1.7 1.7 .7 -1.7 .7 -.7 1.7 -.7 -1.7 -1.7 -.7 1.7 -.7 Z" fill="{KEH}" stroke="{OBS}" stroke-width=".25"/>')
        o.append(yazi(a, cx + .6, 43.4, 2.5, OBS2, "nunito", "orta")[0] + yazi(b, cx + .6, 46.7, 2.5, OBS2, "nunito", "orta")[0])
        if i < 2:
            o.append(_ok(cx + 8.6, 33, cx + 11, 33, GUM_K, .45, 1.2))
    o.append(yazi("Sonra aç; orta şeridi doldur.", 105, 54.2, 2.95, GOL_K, "nunito", "orta")[0])
    s.ekle("".join(o))


def _baslik(s, sol, sag, alt_sol, alt_sag, rozet_svg, balon, boy=8.6):
    """Üst bölüm: katlayınca 'sol + sag' birleşir (ör. “Katla,” + “bağ oluşsun!”)."""
    o = [rozet_svg.replace("<svg ", '<svg x="7.5" y="13.6" width="15.4" height="15.4" ', 1)]
    o.append(yazi(sol, A_X - 1.8, 24.6, boy, OBS, "baloo", "sag")[0])
    o.append(yazi(sag, B_X + 1.8, 24.6, boy, GOL, "baloo", "sol")[0])
    o.append(yazi("önce tahmin et, sonra", 105, 23.4, 4.0, SOLUK, "baloo", "orta")[0])
    for j, t in enumerate(alt_sol):
        o.append(yazi(t, 8, 32.4 + j * 4.6, 3.35, OBS2 if j else GOL_K, "nunito")[0])
    for j, t in enumerate(alt_sag):
        o.append(yazi(t, B_X + 2, 32.4 + j * 4.6, 3.35, OBS2 if j else GOL_K, "nunito")[0])
    # sağ alt: Pamuk ve balonu
    o.append(f'<rect x="142" y="42.2" width="38" height="13.6" rx="3" fill="{KEH_A}" stroke="{OBS}" stroke-width=".4" stroke-dasharray="1.2 .9"/>')
    for j, t in enumerate(balon):
        o.append(yazi(t, 144.4, 47.6 + j * 4.5, 3.35, OBS, "nunito")[0])
    o.append('<use href="#pamuk-selam" x="181.5" y="37.4" width="18.6" height="21.3"/>')
    s.ekle("".join(o))


def _alt_bolum(s, kare_svg, not_sol):
    o = [yazi(not_sol, 8, 272.6, 2.95, SOLUK, "nunito")[0],
         yazi("A ile B buluşunca oku", 105, 272.6, 2.95, GOL_K, "nunito", "orta")[0]]
    if kare_svg:
        o.append(kare_svg.replace("<svg ", '<svg x="185" y="266.6" width="14" height="14" ', 1))
    s.ekle("".join(o))


# ------------------------------------------------------------------ SAYFA 1 · KATLA, BAĞ OLUŞSUN (9. sınıf)

H_Y = 3.1       # dikişe bakan çift yuvasındaki elektronların dikey ofseti (mm)


def _aci(h, r):
    return math.degrees(math.asin(h / r))


BAG = [   # tek doğruluk kaynağı: dogrula.py bu tabloyu yeniden hesaplar
    dict(kod="B1", sol=("Na", [2, 8, 1], "sodyum", "metal · 1 değerlik e^{−}"), sag=("Cl", [2, 8, 7], "klor", "ametal · 7 değerlik e^{−}"),
         tur="iyonik", aktarim=1, denklem=("Na + Cl → N", "a", "Cl"), urun="NaCl",
         neden=("Na 1 e^{−} verir, Cl alır: iy", "o", "nik bağ; zıt yükler çekişir"),
         ipucu=["Metal + ametal.", "Değerlik elektronları: 1 ve 7."]),
    dict(kod="B2", sol=("Mg", [2, 8, 2], "magnezyum", "metal · 2 değerlik e^{−}"), sag=("O", [2, 6], "oksijen", "ametal · 6 değerlik e^{−}"),
         tur="iyonik", aktarim=2, denklem=("Mg + O → M", "g", "O"), urun="MgO",
         neden=("Mg 2 e^{−} verir, O alır: iy", "o", "nik bağ; Mg^{2+} ile O^{2−}"),
         ipucu=["O’nun oktete 2 e^{−} eksiği var.", "Mg’nin dış katmanında 2 e^{−}."]),
    dict(kod="B3", sol=("H", [1], "hidrojen", "ametal · 1 e^{−}"), sag=("H", [1], "hidrojen", "ametal · 1 e^{−}"),
         tur="kovalent", ortak=1, denklem=("H + H → ", "H", "_2"), urun="H2",
         neden=("Birer e^{−} ortak kullanılır: kov", "a", "lent bağ, 1 ortak çift"),
         ipucu=["İki ametal: kimse e^{−} vermez.", "K katmanı 2 e^{−} ile dolar."]),
    dict(kod="B4", sol=("H", [1], "2 hidrojen", "ametal · birer e^{−}"), sag=("O", [2, 6], "oksijen", "ametal · 6 değerlik e^{−}"),
         tur="kovalent", ortak=2, denklem=("2H + O → H", "_2", "O"), urun="H2O",
         neden=("O, iki H ile e^{−} ortaklaşır: kov", "a", "lent bağ, 2 ortak çift"),
         ipucu=["O’nun oktete 2 e^{−} eksiği var.", "Her H 1 e^{−} ortaklaşır."]),
]
SU_ACI = 104.5      # H–O–H açısı (derece); çizim bu açıyla kurulur


def _su_geometri(cy):
    """Su satırı: O sağda, iki H solda; her H, O'ya dikiş üstündeki T noktasında teğet. Bağ yönleri arasındaki açı SU_ACI."""
    yari = math.radians(SU_ACI / 2)
    Ro, Rh = RK[1], 5.6
    ox = B_X + Ro * math.cos(yari)                  # O merkezi (sayfa x); halkası dikişi T± noktalarında keser
    T = [cy - Ro * math.sin(yari), cy + Ro * math.sin(yari)]
    hx = A_X - Rh * math.cos(yari)
    hy = [T[0] - Rh * math.sin(yari), T[1] + Rh * math.sin(yari)]
    aH = math.degrees(math.acos((A_X - PAY - hx) / Rh))       # H elektronu: halka üstünde, dikişten PAY içeride
    aO = math.degrees(math.acos((ox - (B_X + PAY)) / Ro))     # O elektronu: halka üstünde, dikişten PAY içeride
    return dict(Ro=Ro, Rh=Rh, ox=ox, T=T, hx=hx, hy=hy, aH=aH, aO=aO)


def bag_sayfasi(onek, rozet_svg, kare_svg=""):
    s = Sayfa(onek)
    _kat_isaretleri(s)
    _baslik(s, "Katla,", "bağ oluşsun!", ["Yol 6 · Kimyasal etkileşimler", "Dört satır, tek katlama."],
            ["Atomlar yaklaşınca ne olur?", "4 tahmin · +40 akçe"], rozet_svg, ["Önce tahmin et,", "sonra katla! Miyav!"])
    _nasil_katlanir(s)
    # sol üst: nokta–çarpı açıklaması
    ac = [_elektron(10, 44.4, "nokta") + yazi("sol atomun elektronu", 13, 45.5, 2.95, OBS2, "nunito")[0],
          _elektron(10, 49.2, "carpi") + yazi("sağ atomun elektronu", 13, 50.3, 2.95, OBS2, "nunito")[0],
          _bos(10, 54) + yazi("boş yer", 13, 55.1, 2.95, OBS2, "nunito")[0],
          _hale(44, 54, 3.6, 2.0) + yazi("ortak çift", 49.4, 55.1, 2.95, OBS2, "nunito")[0]]
    s.ekle("".join(ac))
    bilgi = []
    for k, b in enumerate(BAG):
        y0 = satir_y(k)
        s.ekle(_bant(k))
        s.ekle(_no(9.4, y0 + 6.2, k + 1))
        (ss, sk, sad, snot), (gs, gk, gad, gnot) = b["sol"], b["sag"]
        cy = y0 + (20.4 if b["kod"] == "B4" else 19.2)
        dikis = []
        if b["kod"] == "B4":
            g = _su_geometri(cy)
            for j in (0, 1):
                a = -g["aH"] if j == 0 else g["aH"]
                svg, dis, _ = atom(g["hx"], g["hy"][j], [1], "H", +1, [a])
                s.ekle(svg)
                dikis.append(dis[0])
            svg, dis, _ = atom(g["ox"], cy, [2, 6], "O", -1, [g["aO"], -g["aO"]] + _cift(125) + _cift(235), isaret="carpi")
            s.ekle(svg)
            for j in (0, 1):                            # ortak çift haleleri: T± çevresinde, çift eksenine döndürülmüş
                hu, hyy = dikis[j]
                ou, oy = dis[j][0] - (B_X - A_X), dis[j][1]
                s.dikis(_hale((hu + ou) / 2, (hyy + oy) / 2, 4.9, 2.5, math.degrees(math.atan2(oy - hyy, ou - hu))))
            sol_x1 = g["hx"] - g["Rh"] - 2.5
            sag_x0 = g["ox"] + g["Ro"] + 3
            bilgi.append(dict(kod=b["kod"], geo=g, cy=cy))
        else:
            r1, r2 = RK[len(sk) - 1], RK[len(gk) - 1]
            cx1, cx2 = A_X - PAY + E_R - .0 - r1 - (PAY - E_R) * 0, B_X + PAY + r2
            cx1 = A_X - PAY - r1
            if b["tur"] == "iyonik":
                n = b["aktarim"]
                hl = [H_Y] if n == 1 else [H_Y, -H_Y]
                svg1, d1, _ = atom(cx1, cy, sk, ss, +1, [_aci(h, r1) for h in hl])
                kalan = ([-_aci(H_Y, r2)] if n == 1 else [])        # Cl: dikiş yuvasında 1 elektron + 1 boş yer
                svg2, d2, b2 = atom(cx2, cy, gk, gs, -1, kalan + _cift(90) + _cift(180) + _cift(270), bos=[_aci(h, r2) for h in hl], isaret="carpi")
                s.ekle(svg1 + svg2)
                for j, (x1, y1) in enumerate(d1):         # aktarım okları (dikişi geçer; kalın)
                    u2, y2 = b2[j][0] - (B_X - A_X), b2[j][1]
                    yuk = -1 if y1 < cy else 1
                    s.dikis(_egri_ok((x1 + .3, y1 + yuk * 1.5), (A_X, y1 + yuk * 6.2), (u2 - .2, y2 + yuk * 1.6), MER_K))
                bilgi.append(dict(kod=b["kod"], sol_e=d1, sag_bos=b2, cx=(cx1, cx2), cy=cy))
            else:
                svg1, d1, _ = atom(cx1, cy, sk, ss, +1, [0])
                svg2, d2, _ = atom(cx2, cy, gk, gs, -1, [0], isaret="carpi")
                s.dikis(_hale(A_X, cy))
                s.ekle(svg1 + svg2)
                bilgi.append(dict(kod=b["kod"], sol_e=d1, sag_e=d2, cx=(cx1, cx2), cy=cy))
            sol_x1, sag_x0 = cx1 - r1 - 2.5, cx2 + r2 + 3
        # girenlerin künyesi (açıkta: verilen bilgi)
        dizi = " · ".join(str(v) for v in sk)
        dizi2 = " · ".join(str(v) for v in gk)
        z1, z2 = sum(sk), sum(gk)
        s.ekle(yazi(sad, 15, y0 + 7.6, 4.3, OBS, "baloo")[0] + yazi(f"_{{{z1}}}{ss} · {dizi}", 8, cy + 3.4, 3.1, KOB_K, "nunito9")[0]
               + yazi(snot, 8, cy + 7.6, 2.75, OBS2, "nunito")[0])
        s.ekle(yazi(gad, 202, y0 + 7.6, 4.3, OBS, "baloo", "sag")[0] + yazi(f"_{{{z2}}}{gs} · {dizi2}", 202, cy + 3.4, 3.1, KOB_K, "nunito9", "sag")[0]
               + yazi(gnot, 202, cy + 7.6, 2.75, OBS2, "nunito", "sag")[0])
        # denklem ve neden (dikişte bölünür)
        d_svg, du0, du1 = bolunmus(*b["denklem"], y0 + 43.0, 4.3)
        n_svg, nu0, nu1 = bolunmus(*b["neden"], y0 + 47.7, 3.35, OBS2, "nunito")
        s.dikis(d_svg + n_svg)
        bilgi[-1].update(denklem_u=(du0, du1), neden_u=(nu0, nu1))
        # orta şerit: çalışma alanı
        s.ekle(_orta_kart(y0 + 2.5, y0 + 30.5, "ÖNCE TAHMİN ET", ["Ürün:", "Bağ türü:"], b["ipucu"]))
        s.ekle(_orta_kart(y0 + 32.5, y0 + 47.2, "AÇ VE AÇIKLA", ["Neden?"]))
    _alt_bolum(s, kare_svg, "Kat izini tırnağınla keskinleştir.")
    return s, bilgi


# ------------------------------------------------------------------ SAYFA 2 · KATLA, TEPKİME OLSUN (10. sınıf)

TEPKIME = [   # tek doğruluk kaynağı: dogrula.py denkliği ve yükleri yeniden hesaplar
    dict(kod="T1", girenler=[(1, "AgNO3", "suda"), (1, "NaCl", "suda")], urunler=[(1, "AgCl", "k"), (1, "NaNO3", "suda")], tur="çözünme–çökelme",
         serit=("Ag", ["NO_3", "+", "Na"], "Cl"), net=("Ag+ + Cl- -> AgCl", "seyirci: Na^{+} ve NO_3^{−}"),
         satirlar=[("AgNO_3(suda) + NaCl(suda) → Ag", "C", "l(k)"), ("+ NaN", "O", "_3(suda)")],
         neden=("Ag^{+} ile Cl^{−} birleşir, çözünmez: çö", "k", "elek oluşur (beyaz katı)"),
         kap=(("AgNO_3(suda)", "renksiz", "#EAF2F6"), ("NaCl(suda)", "renksiz", "#EAF2F6")), ipucu=["AgCl suda çözünmez."]),
    dict(kod="T2", girenler=[(1, "HCl", "suda"), (1, "NaOH", "suda")], urunler=[(1, "NaCl", "suda"), (1, "H2O", "s")], tur="asit–baz (nötralleşme)",
         serit=("H", ["Cl", "+", "Na"], "OH"), net=("H+ + OH- -> H2O", "seyirci: Na^{+} ve Cl^{−}"),
         satirlar=[("HCl(suda) + NaOH(suda) → Na", "C", "l(suda)"), ("+ H", "_2", "O(s)")],
         neden=("H^{+} ile OH^{−} birleşir, su olur: nötr", "a", "lleşme; renk yeşile döner"),
         kap=(("HCl(suda)", "bromtimol mavisiyle sarı", "#F2D43D"), ("NaOH(suda)", "bromtimol mavisiyle mavi", "#3D7BE8")), ipucu=["Asit + baz → tuz + su."]),
    dict(kod="T3", girenler=[(1, "Fe", "k"), (1, "CuSO4", "suda")], urunler=[(1, "FeSO4", "suda"), (1, "Cu", "k")], tur="yer değiştirme (elektron alışverişi)",
         serit=("Fe", ["", "", "+ Cu"], "SO_4"), net=("Fe + Cu2+ -> Fe2+ + Cu", "seyirci: SO_4^{2−}"),
         satirlar=[("Fe(k) + CuSO_4(suda) → FeS", "O", "_4(suda)"), ("+ ", "C", "u(k)")],
         neden=("Fe, Cu^{2+}’ye 2 e^{−} verir: çivi ba", "k", "ırla kaplanır, mavi açılır"),
         kap=(("Fe(k)", "demir çivi", None), ("CuSO_4(suda)", "mavi çözelti", "#3D9FE0")), ipucu=["Fe, Cu’dan daha aktif."]),
    dict(kod="T4", girenler=[(2, "Mg", "k"), (1, "O2", "g")], urunler=[(2, "MgO", "k")], tur="yanma (sentez)",
         serit=("Mg", ["", "", "+ O="], "O"), net=None,
         satirlar=[("2Mg(k) + O_2(g) → 2M", "g", "O(k)")],
         neden=("Mg, O_2 ile birleşir: parlak a", "l", "evle yanar, beyaz kül kalır"),
         kap=(("Mg(k)", "şerit; tutuşturulur", None), ("O_2(g)", "havadaki oksijen", None)), ipucu=["Yanma: O_2 ile birleşme."]),
]


def _beher(cx, yb, w, h, sivi, doluluk=.62, k=.5):
    x0, yt, ys = cx - w / 2, yb - h, yb - h * doluluk
    govde = f"V{f(yb - 1.4)} Q{f(x0)} {f(yb)} {f(x0 + 1.4)} {f(yb)} H{f(x0 + w - 1.4)} Q{f(x0 + w)} {f(yb)} {f(x0 + w)} {f(yb - 1.4)}"
    o = f'<path d="M{f(x0)} {f(ys)} {govde} V{f(ys)} Z" fill="{sivi}"/>' if sivi else ""
    return o + (f'<path d="M{f(x0 - .9)} {f(yt)} H{f(x0)} {govde} V{f(yt)} H{f(x0 + w + .9)}" fill="none" stroke="#1B1D26" stroke-width="{k}" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')


def _urun_resmi(kod, yb):
    """Ürün kabı (katlı uzay, dikiş u = 70'te ikiye bölünür). Kalın çizgiler; renkler fiziksel (tema değiştirmez)."""
    o = ['<g data-tema-sabit="">']
    if kod == "T1":       # beyaz çökelek
        o.append(_beher(A_X, yb, 26, 18, "#EAF2F6", .7, .8))
        o.append(f'<path d="M57.6 {f(yb - .5)} Q63 {f(yb - 7.4)} 70 {f(yb - 7.9)} Q77 {f(yb - 7.4)} 82.4 {f(yb - .5)} Z" fill="#FFFFFF" stroke="#7C8C98" stroke-width=".7" stroke-linejoin="round"/>')
        for dx, dy in ((-7.5, -9.6), (-3.8, -11.4), (3.8, -11.4), (7.5, -9.6), (-9.6, -6.4), (9.6, -6.4)):
            o.append(f'<circle cx="{f(A_X + dx)}" cy="{f(yb + dy)}" r=".85" fill="#FFFFFF" stroke="#7C8C98" stroke-width=".35"/>')
    elif kod == "T2":     # nötr: bromtimol mavisi yeşil
        o.append(_beher(A_X, yb, 26, 18, "#63B95A", .7, .8))
    elif kod == "T3":     # çivi bakırla kaplanır; çözelti açık yeşile döner
        o.append(_beher(A_X, yb, 26, 18, "#CFE8D2", .7, .8))
        o.append(f'<path d="M62.4 {f(yb - 21.4)} L69 {f(yb - 12)}" stroke="#8E9CA8" stroke-width="2.6" stroke-linecap="round"/>'
                 f'<path d="M60.4 {f(yb - 20)} L64.6 {f(yb - 23)}" stroke="#6C7A86" stroke-width="1.5" stroke-linecap="round"/>'
                 f'<path d="M69 {f(yb - 12)} L76.2 {f(yb - 2.4)}" stroke="#B5622A" stroke-width="3" stroke-linecap="round"/>')
    else:                 # T4: parlak beyaz alev, beyaz kül
        pts = []
        for i in range(20):
            a = i * math.pi / 10
            rr = 9.2 if i % 2 == 0 else 4.6
            pts.append((A_X + rr * math.cos(a), yb - 12.4 + rr * math.sin(a)))
        o.append(f'<path d="{cizgi_d(pts, True, 2)}" fill="#FFFDF0" stroke="#F0A21A" stroke-width=".9" stroke-linejoin="round"/>')
        o.append(f'<path d="M59 {f(yb - 3.4)} H81 L78.4 {f(yb)} H61.6 Z" fill="#B9C5CE" stroke="#1B1D26" stroke-width=".8" stroke-linejoin="round"/>'
                 f'<path d="M63 {f(yb - 3.4)} Q70 {f(yb - 8.2)} 77 {f(yb - 3.4)} Z" fill="#FFFFFF" stroke="#7C8C98" stroke-width=".7" stroke-linejoin="round"/>')
    o.append("</g>")
    return "".join(o)


def _giren_kabi(kod, yan, cx, yb, renk):
    """Giren madde resmi (sayfa koordinatı; bir parçanın tamamen içinde)."""
    o = ['<g data-tema-sabit="">']
    if kod == "T3" and yan == 0:        # demir çivi
        o.append(f'<path d="M{f(cx - 6)} {f(yb - 2.6)} L{f(cx + 5)} {f(yb - 11.4)}" stroke="#8E9CA8" stroke-width="2.4" stroke-linecap="round"/>'
                 f'<path d="M{f(cx + 3.2)} {f(yb - 13.2)} L{f(cx + 6.8)} {f(yb - 9.6)}" stroke="#6C7A86" stroke-width="1.5" stroke-linecap="round"/>')
    elif kod == "T4" and yan == 0:      # magnezyum şerit
        o.append(f'<path d="M{f(cx - 6.5)} {f(yb - 3)} q3.2 -4.6 6.5 0 t6.5 0" fill="none" stroke="#1B1D26" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="M{f(cx - 6.5)} {f(yb - 3)} q3.2 -4.6 6.5 0 t6.5 0" fill="none" stroke="#C3CED8" stroke-width="2" stroke-linecap="round"/>')
    elif kod == "T4":                   # O₂: gaz kavanozu, iki molekül
        o.append(_beher(cx, yb, 14, 13.4, None))
        o.append(KK.kullan("kk-gaz-o2", cx - 6, yb - 12.4, 7.4) + KK.kullan("kk-gaz-o2", cx - 1.2, yb - 6.6, 7.4))
    else:
        o.append(_beher(cx, yb, 13, 13.4, renk))
    o.append("</g>")
    return "".join(o)


def tepkime_sayfasi(onek, rozet_svg, kare_svg=""):
    s = Sayfa(onek)
    _kat_isaretleri(s)
    _baslik(s, "Katla,", "tepkime olsun!", ["Yol 1 · Kimyasal değişimler", "Dört satır, tek katlama."],
            ["İki kap birleşince ne olur?", "4 tahmin · +40 akçe"], rozet_svg, ["Önce tahmin et,", "sonra katla! Miyav!"], boy=7.5)
    _nasil_katlanir(s)
    s.ekle(yazi("Büyük yazıya bak:", 8, 45.5, 2.95, GOL_K, "nunito")[0] + yazi("katlayınca gizlenen iyonlar", 8, 49.6, 2.95, OBS2, "nunito")[0]
           + yazi("çözeltide kalır (seyirci iyonlar).", 8, 53.7, 2.95, OBS2, "nunito")[0])
    bilgi = []
    for k, t in enumerate(TEPKIME):
        y0 = satir_y(k)
        yb = y0 + 21.4
        s.ekle(_bant(k) + _no(9.4, y0 + 6.2, k + 1))
        # girenler (açıkta) ve dökme okları
        for yan, (ad, notu, renk) in enumerate(t["kap"]):
            cx = 21 if yan == 0 else 189
            s.ekle(_giren_kabi(t["kod"], yan, cx, yb - 3.4, renk))
            s.ekle(yazi(ad, cx, yb + 2.2, 3.5, OBS, "baloo", "orta")[0] + yazi(notu, cx, yb + 5.8, 2.6, OBS2, "nunito", "orta")[0])
            if yan == 0:
                s.ekle(_egri_ok((30.5, yb - 13), (41, yb - 19), (52.5, yb - 14.6), GUM_K, .6, 1.9))
            else:
                s.ekle(_egri_ok((179.5, yb - 13), (169, yb - 19), (157.5, yb - 14.6), GUM_K, .6, 1.9))
        s.dikis(_urun_resmi(t["kod"], yb))
        # büyük iyon şeridi: açıkken girenler okunur, katlayınca ürün (orta şeritteki seyirciler gizlenir)
        ys = y0 + 33.4
        sol, orta, sag = t["serit"]
        sv1, _, sx1 = yazi(sol, A_X - 1.6, ys, 5.8, OBS, "baloo", "sag")
        sv2, sx0, _ = yazi(sag, B_X + 1.6, ys, 5.8, OBS, "baloo", "sol")
        s.ekle(sv1 + sv2)
        if orta[0]:
            s.ekle(yazi(orta[0], A_X + 1.6, ys, 5.8, SOLUK, "baloo", "sol")[0])
        if orta[1]:
            s.ekle(yazi(orta[1], 105, ys, 5.8, SOLUK, "baloo", "orta")[0])
        if orta[2]:
            s.ekle(yazi(orta[2], B_X - 1.6, ys, 5.8, SOLUK, "baloo", "sag")[0])
        # denklem (ürün başına bir satır: her ürün dikişte bölünür) ve neden
        parca, uclar = [], []
        for j, (a, b, c) in enumerate(t["satirlar"]):
            svg, u0, u1 = bolunmus(a, b, c, y0 + 38.9 + j * 4.5, 3.7)
            parca.append(svg)
            uclar.append((u0, u1))
        svg, u0, u1 = bolunmus(*t["neden"], y0 + 47.9, 3.35, OBS2, "nunito")
        s.dikis("".join(parca) + svg)
        bilgi.append(dict(kod=t["kod"], satir_u=uclar, neden_u=(u0, u1), serit_x=(sx1, sx0)))
        s.ekle(_orta_kart(y0 + 2.5, y0 + 27.2, "ÖNCE TAHMİN ET", ["Ürün:", "Tepkime türü:"], t["ipucu"]))
        s.ekle(_orta_kart(y0 + 35.6, y0 + 47.2, "AÇ VE AÇIKLA", []).replace("</rect>", "</rect>") + _nokta_satir(101, 131.6, y0 + 44.4))
    _alt_bolum(s, kare_svg, "Deneyi yalnız öğretmeninle yap.")
    return s, bilgi


# ------------------------------------------------------------------ SAYFA KÖŞESİ ÇİZGİ FİLMİ (24 kare)

KARE_SAYISI = 24
_P = {1: (22, 80), 2: (53, 60), 3: (81, 44)}        # basamakların üstü: elektronun ayak noktası


def kare(i):
    """i. kare (0…23), viewBox 0 0 100 100: elektron foton soğurur, n = 3'e çıkar, inerken kırmızı foton yayar."""
    i = int(i) % KARE_SAYISI
    o = ['<rect x="1.5" y="1.5" width="97" height="97" rx="9" fill="#FFFFFF" stroke="#1B1D26" stroke-width="3"/>',
         '<path d="M6 94 V80 H38 V60 H68 V44 H94 V94 Z" fill="#F0E2C2" stroke="#1B1D26" stroke-width="2.2" stroke-linejoin="round"/>']
    for n, (x, y) in _P.items():
        o.append(f'<text x="{x}" y="{y + 11}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="9" fill="#8A6212">{n}</text>')

    def el(x, y, tur=""):
        return KK.kullan("kk-elektron" + (f"-{tur}" if tur else ""), x - 13, y - 25, 26)

    def ara(a, b, t, kavis):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t - kavis * math.sin(math.pi * t))
    if i <= 3:                        # UV foton soldan gelir
        o.append(el(*_P[1]))
        o.append(KK.kullan("kk-foton-uv", -34 + 11 * i, 34 + 4 * i, 34))
    elif i <= 5:                      # soğurma: parlama
        pts = []
        for k in range(16):
            a = k * math.pi / 8
            rr = (15 if i == 4 else 10) * (1 if k % 2 == 0 else .45)
            pts.append((22 + rr * math.cos(a), 62 + rr * math.sin(a)))
        o.append(f'<path d="{cizgi_d(pts, True)}" fill="#FFE27A" stroke="#1B1D26" stroke-width="1.6" stroke-linejoin="round"/>')
        o.append(el(_P[1][0], _P[1][1] - (0 if i == 4 else 5), "heyecan"))
    elif i <= 11:                     # n = 1 → n = 3 sıçrayışı
        o.append(el(*ara(_P[1], _P[3], (i - 5) / 7, 26), "heyecan"))
    elif i <= 14:                     # uyarılmış hâl
        o.append(el(_P[3][0] + (0, 1.6, -1.6)[i - 12], _P[3][1], "heyecan"))
    elif i <= 17:                     # n = 3 → n = 2 inişi; kırmızı foton çıkar
        o.append(el(*ara(_P[3], _P[2], (i - 14) / 4, 8), "sasiran"))
        if i >= 16:
            o.append(KK.kullan("kk-foton-656", 56 + 8 * (i - 16), 20 - 3 * (i - 16), 34))
    elif i <= 21:                     # n = 2'de; foton sağa uçar
        o.append(el(*_P[2], "sakin"))
        o.append(KK.kullan("kk-foton-656", 72 + 10 * (i - 18), 14 - 3 * (i - 18), 34))
    else:                             # n = 2 → n = 1 (UV foton sola gider)
        o.append(el(*ara(_P[2], _P[1], (i - 21) / 2, 6), "" if i == 23 else "sakin"))
        o.append(KK.kullan("kk-foton-uv", 30 - 22 * (i - 22), 26 - 12 * (i - 22), 30, ayna=True))
    return f'<svg class="kare" viewBox="0 0 100 100" data-kare="{i + 1}">{"".join(o)}</svg>'
