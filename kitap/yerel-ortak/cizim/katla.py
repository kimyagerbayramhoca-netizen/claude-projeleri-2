"""Katla sayfaları · çizimler (ORTAK; kaynak: gelistirme/katla/uretec/katla_cizim.py). CSS: stil.css §41.

Yer tutucular (kur_ortak): {{katla|bag}} {{katla|tepkime}} (kat sayfası) · {{film}} {{film-kose}} {{film-kare|k}} (köşe sineması) ·
{{kose-on}} {{kose-arka|…}} {{kose-adimlar|…}} {{kose-harita|…}} (köşeyi katla) · {{kikon|ad}} {{robot}} {{kapi}} (karma sayfa) ·
{{zemin14}} {{cini14}} (kat sayfası zemini ve çini şeridi). Sayfa sırası kuralı: kat sayfası ve köşesi katlanan sayfa TEK
numaralı (sağ) sayfadır; arka yüzleri (karma sayfa / köşe sineması · köşenin sırrı) hemen sonraki çift sayfadır.

MEKANİK. Sayfada iki dikey kat çizgisi var: A (x = 70 mm) ve B (x = 140 mm). Öğrenci orta şeridi (70–140) arkaya iter,
A kenarını B kenarına getirir: SOL parça (0–70) ile SAĞ parça (140–210) yan yana gelir. Dört satır aynı iki çizgiyi
paylaşır; tek katlama dördünü birden tamamlar.

KOORDİNATLAR. Sayfa mm cinsindendir (viewBox 0 0 210 297). "Katlı uzay" u ∈ [0, 140], dikiş u = 70:
u < 70 → sayfada x = u (sol parça) · u > 70 → sayfada x = u + 70 (sağ parça).
Dikişi geçen her şey (ok, hale, bölünmüş yazı, ürün kabı) katlı uzayda TEK parça çizilir ve sayfaya iki kez basılır
(Sayfa.dikis): solda x ≤ 70 + TASMA'ya, sağda x ≥ 140 − TASMA'ya kırpılır. Böylece yarımlar kesinlikle hizalıdır;
TASMA (1 mm) orta şeride taşan paydır: ±1 mm kat hatasında dikişte beyaz boşluk kalmaz.

KURALLAR: dikişi geçen çizgiler kalın (≥ 0,6 mm) ve dikişi yataya yakın keser; dolgular dikişi
serbestçe geçer · dikişe komşu ama onu geçmeyen her öge dikişten ≥ 1,2 mm içeride · ürün formülü ve bağ/tepkime türü
hiçbir parçada tam yazılı değil (bir harf dikişte ikiye bölünür; bölünen harfin ortasında dikey gövde yok: GUVENLI_HARF) ·
satır zemini üç parçada da aynı renk · anlam yalnız renkle verilmez (sol atomun elektronu ●, sağ atomunki ×, boş yer
kesik çember, ortak çift hale; kat işaretleri A/B harfli şekiller).

ÖĞRETMEN NÜSHASI. Orta şeritteki "Önce tahmin et" ve "Aç ve açıkla" satırlarının cevapları <g class="ogr-svg"
data-katla="B1" data-urun="NaCl" data-tur="iyonik"> içinde kırmızı basılır (öğrenci baskısında display:none);
dogrula_ortak.katla_cevaplari(html) bunları okur.

Satırlar (BAG, TEPKIME) ünitenin modülünden değiştirilebilir: sahneler_unite.KATLA_BAG / KATLA_TEPKIME (aynı biçim).
Yazı genişlikleri fontTools ile fontun kendi ölçülerinden hesaplanır (bölünen harf tam dikişe ortalanır; stil.css bu
SVG'lerde harf arası düzeltmeyi ve bitişik harfleri kapatır).
"""
import math
import os

from fontTools.ttLib import TTFont

from cizim.temel import f, cizgi_d, selcuklu_yildizi
from cizim.renkler import (OBS, OBS2, SOLUK, GOL, GOL_K, GOL_A, GOL_AA, KEH, KEH_K, KEH_A, MER, MER_K, KOB_K, GUM, GUM_K, ATOM)
from cizim import konu_karakterleri as KK

A_X, B_X = 70.0, 140.0
TASMA = 1.0                 # dikişi geçen ŞEKİLLERİN orta şeride taşma payı (mm); bölünen YAZI payısız kırpılır (yarım harf saklı kalsın)
PAY = 2.25                  # dikişe bakan elektronun merkezinin dikişe uzaklığı (yarıçap 1,05 + 1,2 mm güven payı)
E_R = 1.05                  # elektron yarıçapı
GUVEN = 1.2                 # dikişe komşu ögelerin en az uzaklığı
RK = (6.0, 9.4, 12.8)       # K, L, M katman yarıçapları (mm)
ELEKTRON, E_KOYU = "#2B50B5", "#13235E"
OGR = "#D3121B"                      # öğretmen kırmızısı (stil.css --ogr)
GUVENLI_HARF = set("aoecgsuOCGHS")     # dikişte bölünebilen harfler (ortasında dikey gövde yok)
FONTLAR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "fontlar"))
_DOSYA = {"baloo": "baloobhaijaan2/static/BalooBhaijaan2-800.ttf", "nunito": "nunito/static/Nunito-800.ttf", "nunito9": "nunito/static/Nunito-900.ttf"}
_AILE = {"baloo": "font-family=\"'Baloo Bhaijaan 2', Nunito\" font-weight=\"800\"", "nunito": 'font-family="Nunito" font-weight="800"',
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


def yazi(metin, x, y, boy, renk=OBS, font="baloo", hiza="sol", en=None):
    """SVG yazısı (kontur yok). hiza: sol | sag | orta. en: sığması gereken en (mm; aşarsa punto küçülür).
    Dönen: (svg, x0, x1)."""
    if not metin:
        return "", x, x
    w = genislik(metin, boy, font)
    if en and w > en:
        boy, w = boy * en / w, en
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
    wk = genislik(kesik, boy, font)
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

    def dikis(self, frag, yazi_mi=False):
        """Katlı uzayda çizilmiş parçayı sola ve sağa (70 mm kaydırıp) kırparak basar. Şekiller TASMA kadar orta şeride
        taşar (kat hatasında boşluk kalmaz); yazı tam dikişte kesilir (taşma payı bölünen harfin öbür yarısını göstermesin)."""
        self.dikis_parcalari.append((frag, yazi_mi))
        k = "0" if yazi_mi else ""
        self.o.append(f'<g clip-path="url(#{self.onek}-kL{k})">{frag}</g>'
                      f'<g transform="translate({f(B_X - A_X)} 0)"><g clip-path="url(#{self.onek}-kR{k})">{frag}</g></g>')

    def cikti(self):
        defs = "".join(f'<clipPath id="{self.onek}-kL{k}"><rect x="-5" y="0" width="{f(A_X + 5 + t)}" height="297"/></clipPath>'
                       f'<clipPath id="{self.onek}-kR{k}"><rect x="{f(A_X - t)}" y="0" width="90" height="297"/></clipPath>' for k, t in (("", TASMA), ("0", 0)))
        defs = f"<defs>{defs}</defs>"
        return f'<svg class="katla-svg" viewBox="0 0 210 297" data-serbest="">{defs}{"".join(self.o)}</svg>'


def zemin14():
    """Kat sayfası zemini: ortak yıldız geçmesinin 14 mm adımlı eşi (70 mm = 5 adım → dikişte desen kesintisiz sürer)."""
    d = []
    for i in range(-1, 17):
        for j in range(-1, 23):
            cx, cy = 7 + i * 14, 7 + j * 14
            d.append(cizgi_d(selcuklu_yildizi(cx, cy, 3.4), True, 2))
            d.append(f"M{f(cx + 5)} {f(cy + 5)} l4 4")
    return (f'<svg class="zemin" viewBox="0 0 210 297" preserveAspectRatio="none"><path d="{" ".join(d)}" fill="none" '
            f'stroke="#DDEEEE" stroke-width=".22" stroke-linejoin="round"/></svg>')


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
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(x1 - x0 + 3.6)}" height="4.3" rx="2.15" fill="{zemin}"/>' + svg, x + x1 - x0 + 3.6


def _no(x, y, n, renk=OBS, r=2.9, boy=3.5):
    return f'<circle cx="{f(x, 2)}" cy="{f(y, 2)}" r="{r}" fill="{renk}"/>' + yazi(str(n), x, y + boy * .36, boy, "#FFFFFF", "baloo", "orta")[0]


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
    assert len(deger) == katman[-1], (sembol, katman, deger)
    dis, bosluk = [nokta(RK[n - 1], a) for a in deger], [nokta(RK[n - 1], a) for a in bos]
    o += [_bos(*p) for p in bosluk] + [_elektron(*p, isaret) for p in dis]
    o.append(f'<circle cx="{f(cx, 2)}" cy="{f(cy, 2)}" r="3.3" fill="{ATOM[sembol]}" stroke="#1B1D26" stroke-width=".4"/>')
    o.append(yazi(sembol, cx, cy + 1.15, 3.0 if len(sembol) > 1 else 3.4, "#1B1D26" if sembol in ("H", "Mg") else "#FFFFFF", "baloo", "orta")[0])
    o.append("</g>")
    return "".join(o), dis, bosluk


def _cift(merkez):
    """Bir elektron çifti yuvası: merkez açısının ±13° iki yanı."""
    return [merkez - 13, merkez + 13]


def _aci(h, r):
    return math.degrees(math.asin(h / r))


def _hale(u, y, rx=4.9, ry=2.7):
    """Ortak çift halesi (katlı uzay; dikişe ortalı yatay elips: dış çizgisi dikişi tam yatay keser)."""
    return f'<ellipse cx="{f(u, 2)}" cy="{f(y, 2)}" rx="{rx}" ry="{ry}" fill="#FFE9A8" stroke="{KEH_K}" stroke-width=".7"/>'


# ------------------------------------------------------------------ sayfa iskeleti

SATIR_Y0, SATIR_H, SATIR_ARA = 60.0, 49.5, 2.5
BANT = (GOL_AA, "#FFF7E3")


def satir_y(k):
    return SATIR_Y0 + k * (SATIR_H + SATIR_ARA)


def _bant(k):
    return f'<rect x="5" y="{f(satir_y(k))}" width="200" height="{SATIR_H}" rx="3.2" fill="{BANT[k % 2]}"/>'


def _orta_kart(y0, y1, cip, satirlar=(), ipucu=None, soru=None):
    """Orta şeritteki çalışma kartı (x 76–134). satirlar: ['Ürün:', …] → her biri noktalı çizgi · soru: çipin yanındaki kısa soru."""
    c, cx1 = _cip(78, y0 + 1.6, cip)
    o = [f'<rect x="76" y="{f(y0)}" width="58" height="{f(y1 - y0)}" rx="2.4" fill="#FFFFFF" stroke="#CFDCE0" stroke-width=".35"/>', c]
    if soru:
        o.append(yazi(soru, cx1 + 1.5, y0 + 4.75, 2.75, OBS2, "nunito", en=132 - cx1 - 1.5)[0] + _nokta_satir(78.2, 131.6, y1 - 2.4))
    y = y0 + 10.6
    for s in satirlar:
        svg, _, x1 = yazi(s, 78.2, y, 3.35, OBS, "nunito")
        o.append(svg + _nokta_satir(x1 + 1.4, 131.6, y + .2))
        y += 5.6
    if ipucu:
        svg, _, x1 = yazi("İPUCU", 78.2, y - .6, 2.5, KEH_K, "nunito9")
        o.append(svg)
        for j, satir in enumerate(ipucu):
            xs = x1 + 1.6 if j == 0 else 78.2
            o.append(yazi(satir, xs, y - .6 + j * 3.7, 2.95, SOLUK, "nunito", en=131.8 - xs)[0])
    return "".join(o)


def _orta_cevap(y0, y1, satirlar=(), cevaplar=(), soru=None, soru_cevap=None):
    """_orta_kart'ın satırlarına öğretmen cevapları (kırmızı; çağıran <g class="ogr-svg"> içine alır)."""
    o = []
    y = y0 + 10.6
    for s_, c in zip(satirlar, cevaplar):
        _, _, x1 = yazi(s_, 78.2, y, 3.35, OBS, "nunito")
        if c:
            o.append(yazi(c, x1 + 1.8, y - .35, 3.35, OGR, "nunito9", en=131.4 - x1 - 1.8)[0])
        y += 5.6
    if soru and soru_cevap:
        o.append(yazi(soru_cevap, 78.6, y1 - 2.95, 3.0, OGR, "nunito9", en=52.6)[0])
    return "".join(o)


def _ogr_grubu(kod, urun, tur, icerik):
    return f'<g class="ogr-svg" data-katla="{kod}" data-urun="{duz(urun)}" data-tur="{duz(tur)}">{icerik}</g>'


def _alt_simge(formul):
    """'H2O' → 'H_2O' (ölçülü yazımda rakamlar alt simge)."""
    import re as _re
    return _re.sub(r"(?<=[A-Za-z)])(\d+)", lambda m: "_{" + m.group(1) + "}", formul)


def _kat_isaretleri(s):
    """A ve B kat işaretleri: uçları kat çizgisinden 0,5 mm içeride, gövdeleri ORTA şeritte (katlayınca görünmez);
    harfli dolu şekiller. Sayfanın içinden kat çizgisi geçmez (kılcal çizgi kalmasın)."""
    o = []
    for y in (14.2, 268.8):
        o.append(f'<path d="M{f(A_X + .5, 2)} {f(y + 2.8)} l3 -2.8 h6.7 v5.6 h-6.7 Z" fill="{MER}"/>' + yazi("A", A_X + 7, y + 4.1, 3.7, "#FFFFFF", "baloo", "orta")[0])
        o.append(f'<path d="M{f(B_X - .5, 2)} {f(y + 2.8)} l-3 -2.8 h-6.7 v5.6 h6.7 Z" fill="{MER}"/>' + yazi("B", B_X - 7, y + 4.1, 3.7, "#FFFFFF", "baloo", "orta")[0])
    for k in range(5):
        yg = satir_y(k) - SATIR_ARA / 2 if k < 4 else satir_y(3) + SATIR_H + SATIR_ARA / 2
        o.append(f'<path d="M{f(A_X + .5, 2)} {f(yg, 2)} l2.1 -1.1 v2.2 Z M{f(B_X - .5, 2)} {f(yg, 2)} l-2.1 -1.1 v2.2 Z" fill="{MER_K}"/>')
    s.ekle("".join(o))


def _nasil_katlanir(s, son):
    """Orta şeridin üstünde üç adımlı katlama çizimi."""
    o = []
    adimlar = (("A ve B’den", "arkaya bük"), ("orta şeridi", "arkaya it"), ("A, B’ye değsin:", "oku!"))
    for i, (a, b) in enumerate(adimlar):
        cx = 86.5 + i * 18.5
        o.append(_no(cx - 7.4, 29.4, i + 1, GOL_K, 2.2, 2.8))
        if i == 0:      # düz sayfa, iki kesik çizgi
            o.append(f'<rect x="{f(cx - 4.4)}" y="29" width="12" height="9.6" rx=".6" fill="#FFFFFF" stroke="{OBS}" stroke-width=".4"/>'
                     f'<path d="M{f(cx - .4)} 29 v9.6 M{f(cx + 3.6)} 29 v9.6" stroke="{MER}" stroke-width=".4" stroke-dasharray=".9 .7"/>')
            o.append(yazi("A", cx - .4, 28.2, 2.3, MER_K, "nunito9", "orta")[0] + yazi("B", cx + 3.6, 28.2, 2.3, MER_K, "nunito9", "orta")[0])
        elif i == 1:    # üstten bakış: orta şerit arkaya (yukarı) kıvrılır, iki parça birbirine yaklaşır
            o.append(f'<path d="M{f(cx - 5.4)} 36.4 H{f(cx - .6)} L{f(cx + 1.6)} 29.6 L{f(cx + 3.8)} 36.4 H{f(cx + 8.6)}" fill="none" stroke="{OBS}" stroke-width=".7" stroke-linejoin="round" stroke-linecap="round"/>')
            o.append(_ok(cx - 5.2, 39, cx - 1.2, 39, MER_K, .5, 1.4) + _ok(cx + 8.4, 39, cx + 4.4, 39, MER_K, .5, 1.4))
        else:           # katlı: iki parça yan yana
            o.append(f'<rect x="{f(cx - 2.4)}" y="29" width="8" height="9.6" rx=".6" fill="#FFFFFF" stroke="{OBS}" stroke-width=".4"/>'
                     f'<path d="M{f(cx + 1.6)} 29.4 v8.8" stroke="{MER}" stroke-width=".4"/>')
            o.append(yazi("A", cx + .5, 28.2, 2.3, MER_K, "nunito9", "orta")[0] + yazi("B", cx + 2.8, 28.2, 2.3, MER_K, "nunito9", "orta")[0])
        o.append(yazi(a, cx + 1.6, 43.6, 2.5, OBS2, "nunito", "orta", en=17.6)[0] + yazi(b, cx + 1.6, 46.9, 2.5, OBS2, "nunito", "orta", en=17.6)[0])
        if i < 2:
            o.append(_ok(cx + 9.8, 33.6, cx + 12, 33.6, GUM_K, .45, 1.2))
    o.append(yazi(son, 105, 54.4, 2.95, GOL_K, "nunito", "orta", en=62)[0])
    s.ekle("".join(o))


def _baslik(s, sol, sag, orta, alt_sol, alt_sag, rozet_svg, balon):
    """Üst bölüm: katlayınca 'sol + sag' birleşir (ör. “Katla,” + “bağ oluşsun!”); açıkken ortadaki söz araya girer."""
    rozet = rozet_svg.replace('class="durak-rozet"', "", 1).replace("<svg ", '<svg x="7.5" y="13.8" width="15" height="15" ', 1)
    o = [rozet, yazi(sol, A_X - 1.8, 24.6, 8.6, OBS, "baloo", "sag")[0], yazi(sag, B_X + 1.8, 24.6, 8.6, GOL, "baloo", "sol", en=56.5)[0],
         yazi(orta, 105, 24.2, 3.6, SOLUK, "baloo", "orta", en=62)[0]]
    for j, t in enumerate(alt_sol):
        o.append(yazi(t, 8, 33.2 + j * 4.6, 3.35, OBS2 if j else GOL_K, "nunito", en=59)[0])
    for j, t in enumerate(alt_sag):
        o.append(yazi(t, B_X + 2, 33.2 + j * 4.6, 3.35, OBS2 if j else GOL_K, "nunito", en=57)[0])
    o.append(f'<rect x="142" y="43" width="37.4" height="12.8" rx="3" fill="{KEH_A}" stroke="{OBS}" stroke-width=".4" stroke-dasharray="1.2 .9"/>')
    for j, t in enumerate(balon):
        o.append(yazi(t, 144.4, 48.4 + j * 4.5, 3.35, OBS, "nunito", en=33)[0])
    o.append('<use href="#pamuk-selam" x="181.5" y="37.4" width="18.6" height="21.3"/>')
    s.ekle("".join(o))


def _alt_bolum(s, kare_svg, not_sol, not_sag, kare_no):
    o = [yazi(not_sol, 8, 272.8, 2.95, SOLUK, "nunito", en=59)[0], yazi("A ile B buluşunca oku", 105, 272.8, 2.95, GOL_K, "nunito", "orta")[0],
         yazi(not_sag, 142, 272.8, 2.95, MER_K, "nunito", en=40)[0]]
    if kare_svg:
        o.append(kare_svg.replace("<svg ", '<svg x="185" y="266.8" width="14" height="14" ', 1))
        o.append(yazi(f"köşe sineması · {kare_no}/{KARE_SAYISI}", 183.6, 279.8, 2.5, SOLUK, "nunito", "sag")[0])
    s.ekle("".join(o))


# ------------------------------------------------------------------ SAYFA 1 · KATLA, BAĞ OLUŞSUN (9. sınıf)

H_Y = 3.1       # dikişe bakan çift yuvasındaki elektronların dikey ofseti (mm)

BAG = [   # tek doğruluk kaynağı: dogrula.py bu tabloyu yeniden hesaplar (atom düzeyinde bağ oluşumu)
    dict(kod="B1", sol=("Na", [2, 8, 1], "sodyum", "metal · 1 değerlik e^{−}"), sag=("Cl", [2, 8, 7], "klor", "ametal · 7 değerlik e^{−}"),
         tur="iyonik", aktarim=1, ortak=0, denklem=("Na + Cl → N", "a", "Cl"), urun="NaCl", tur_kelime="iyonik",
         neden=("Na 1 e^{−} verir, Cl alır: iy", "o", "nik bağ (Na^{+} ile Cl^{−})"),
         ipucu=["Metal + ametal.", "Değerlik elektronları: 1 ve 7."]),
    dict(kod="B2", sol=("Mg", [2, 8, 2], "magnezyum", "metal · 2 değerlik e^{−}"), sag=("O", [2, 6], "oksijen", "ametal · 6 değerlik e^{−}"),
         tur="iyonik", aktarim=2, ortak=0, denklem=("Mg + O → M", "g", "O"), urun="MgO", tur_kelime="iyonik",
         neden=("Mg 2 e^{−} verir, O alır: iy", "o", "nik bağ (Mg^{2+} ile O^{2−})"),
         ipucu=["Oktet için O’ya 2 e^{−} gerek.", "Mg’nin dış katmanında 2 e^{−} var."]),
    dict(kod="B3", sol=("H", [1], "hidrojen", "ametal · 1 e^{−}"), sag=("H", [1], "hidrojen", "ametal · 1 e^{−}"),
         tur="kovalent", aktarim=0, ortak=1, denklem=("H + H → ", "H", "_2"), urun="H2", tur_kelime="kovalent",
         neden=("Birer e^{−} ortak kullanılır: kov", "a", "lent bağ, 1 ortak çift"),
         ipucu=["İki ametal: e^{−} veren yok.", "K katmanı 2 e^{−} ile dolar."]),
    dict(kod="B4", sol=("O", [2, 6], "oksijen", "ametal · 6 değerlik e^{−}"), sag=("O", [2, 6], "oksijen", "ametal · 6 değerlik e^{−}"),
         tur="kovalent", aktarim=0, ortak=2, denklem=("O + O → ", "O", "_2"), urun="O2", tur_kelime="kovalent",
         neden=("İkişer e^{−} ortak kullanılır: kov", "a", "lent bağ, 2 ortak çift"),
         ipucu=["Oktet için her O’ya 2 e^{−} gerek.", "İki ametal: e^{−} veren yok."]),
]


def _bag_nedeni(b):
    """Öğretmen cevabı · Neden? (kısa): '1 e^{−} aktarımı: Na^{+} ve Cl^{−}' · '2 ortak e^{−} çifti'."""
    import re as _re
    if b["tur"] == "iyonik":
        m = _re.search(r"\((.+?) ile (.+?)\)", "".join(b["neden"]))
        return f'{b["aktarim"]} e^{{−}} aktarımı' + (f": {m.group(1)} ve {m.group(2)}" if m else "")
    return f'{b["ortak"]} ortak e^{{−}} çifti'


def bag_sayfasi(onek, rozet_svg, kare_svg="", kare_no=1, satirlar=None, rota="Yol 6 · Tuz Gölü–Aksaray"):
    """Katla, bağ oluşsun! satirlar: BAG biçiminde 4 satır (verilmezse BAG). Dönen: (Sayfa, satır bilgileri)."""
    satirlar = satirlar or BAG
    s = Sayfa(onek)
    _kat_isaretleri(s)
    _baslik(s, "Katla,", "bağ oluşsun!", "(ama önce tahmin et!)", [rota, "Dört satır, tek katlama."],
            ["Atomlar yaklaşınca ne olur?", "4 tahmin · +40 akçe"], rozet_svg, ["Önce tahmin et,", "sonra katla!"])
    _nasil_katlanir(s, "Önce yaz, sonra katla; aç ve açıkla.")
    s.ekle('<g data-tema-sabit="">' + _elektron(10, 44.4, "nokta") + _elektron(10, 49.2, "carpi") + _bos(10, 54) + "</g>"
           + yazi("sol atomun elektronu", 13, 45.5, 2.95, OBS2, "nunito")[0] + yazi("sağ atomun elektronu", 13, 50.3, 2.95, OBS2, "nunito")[0]
           + yazi("boş yer", 13, 55.1, 2.95, OBS2, "nunito")[0] + _hale(40, 54, 3.6, 2.0) + yazi("ortak çift", 45.4, 55.1, 2.95, OBS2, "nunito")[0])
    bilgi = []
    for k, b in enumerate(satirlar):
        y0 = satir_y(k)
        s.ekle(_bant(k) + _no(9.4, y0 + 6.2, k + 1))
        (ss, sk, sad, snot), (gs, gk, gad, gnot) = b["sol"], b["sag"]
        cy = y0 + 19.2
        r1, r2 = RK[len(sk) - 1], RK[len(gk) - 1]
        cx1, cx2 = A_X - PAY - r1, B_X + PAY + r2
        kayit = dict(kod=b["kod"], cy=cy, cx=(cx1, cx2), r=(r1, r2), oklar=0, haleler=0)
        if b["tur"] == "iyonik":
            n = b["aktarim"]
            hl = [H_Y] if n == 1 else [H_Y, -H_Y]
            svg1, d1, _ = atom(cx1, cy, sk, ss, +1, [_aci(h, r1) for h in hl])
            kalan = [-_aci(H_Y, r2)] if n == 1 else []          # Cl: dikiş yuvasında 1 elektron + 1 boş yer
            svg2, d2, b2 = atom(cx2, cy, gk, gs, -1, kalan + _cift(90) + _cift(180) + _cift(270), bos=[_aci(h, r2) for h in hl], isaret="carpi")
            s.ekle(svg1 + svg2)
            for j, (x1, y1) in enumerate(d1):                  # aktarım okları: dikişi tepe noktasında (yatay) geçer
                u2, y2 = b2[j][0] - (B_X - A_X), b2[j][1]
                yuk = -1 if y1 < cy else 1
                s.dikis(_egri_ok((x1 + .3, y1 + yuk * 1.5), (A_X, y1 + yuk * 6.6), (u2 - .2, y2 + yuk * 1.6), MER_K))
                kayit["oklar"] += 1
            kayit.update(sol_e=d1, sag_e=d2, sag_bos=b2)
        else:
            n = b["ortak"]
            hl = [0.0] if n == 1 else [H_Y, -H_Y]
            yalniz = [] if len(sk) == 1 else _cift(125) + _cift(235)
            for h in hl:
                s.dikis(_hale(A_X, cy - h, 4.9, 2.7 if n == 1 else 2.45))
                kayit["haleler"] += 1
            svg1, d1, _ = atom(cx1, cy, sk, ss, +1, [_aci(h, r1) for h in hl] + yalniz)
            svg2, d2, _ = atom(cx2, cy, gk, gs, -1, [_aci(h, r2) for h in hl] + yalniz, isaret="carpi")
            s.ekle(svg1 + svg2)
            kayit.update(sol_e=d1, sag_e=d2, sag_bos=[])
        # girenlerin künyesi (açıkta: verilen bilgi)
        s.ekle(yazi(sad, 15, y0 + 7.6, 4.3, OBS, "baloo")[0] + yazi(f"_{{{sum(sk)}}}{ss}: " + " · ".join(str(v) for v in sk), 8, cy + 3.4, 3.1, KOB_K, "nunito9")[0]
               + yazi(snot, 8, cy + 7.6, 2.75, OBS2, "nunito")[0])
        s.ekle(yazi(gad, 202, y0 + 7.6, 4.3, OBS, "baloo", "sag")[0] + yazi(f"_{{{sum(gk)}}}{gs}: " + " · ".join(str(v) for v in gk), 202, cy + 3.4, 3.1, KOB_K, "nunito9", "sag")[0]
               + yazi(gnot, 202, cy + 7.6, 2.75, OBS2, "nunito", "sag")[0])
        # denklem ve neden (dikişte bölünür)
        d_svg, du0, du1 = bolunmus(*b["denklem"], y0 + 43.0, 4.3)
        n_svg, nu0, nu1 = bolunmus(*b["neden"], y0 + 47.7, 3.35, OBS2, "nunito")
        s.dikis(d_svg + n_svg, yazi_mi=True)
        kayit.update(denklem_u=(du0, du1), neden_u=(nu0, nu1))
        bilgi.append(kayit)
        # orta şerit: çalışma alanı
        s.ekle(_orta_kart(y0 + 2.5, y0 + 30.5, "ÖNCE TAHMİN ET", ["Ürün:", "Bağ türü:"], b["ipucu"]))
        s.ekle(_orta_kart(y0 + 32.5, y0 + 47.2, "AÇ VE AÇIKLA", ["Neden?"]))
        urun = b["denklem"][0].split("→")[-1].strip() + b["denklem"][1] + b["denklem"][2]
        s.ekle(_ogr_grubu(b["kod"], urun, b["tur"],
                          _orta_cevap(y0 + 2.5, y0 + 30.5, ["Ürün:", "Bağ türü:"], [urun, f'{b["tur"]} bağ'])
                          + _orta_cevap(y0 + 32.5, y0 + 47.2, ["Neden?"], [b.get("cevap_neden") or _bag_nedeni(b)])))
    _alt_bolum(s, kare_svg, "Kat izini tırnağınla keskinleştir.", "", kare_no)
    return s, bilgi


# ------------------------------------------------------------------ SAYFA 2 · KATLA, TEPKİME OLSUN (10. sınıf)

TEPKIME = [   # tek doğruluk kaynağı: dogrula.py denkliği, yükleri ve şeritleri yeniden hesaplar
    dict(kod="T1", durak="Pasinler", girenler=[(1, "AgNO3", "suda"), (1, "NaCl", "suda")], urunler=[(1, "AgCl", "k"), (1, "NaNO3", "suda")],
         tur="çözünme–çökelme", ana_urun="AgCl", serit=("Ag", ["NO_3", "+", "Na"], "Cl"), serit_katli="AgCl",
         gizli="Na^{+} ve NO_3^{−} çözeltide kalır (seyirci iyonlar).",
         satirlar=[("AgNO_3(suda) + NaCl(suda) → Ag", "C", "l(k)"), ("+ NaN", "O", "_3(suda)")],
         neden=("Ag^{+} ile Cl^{−} suda birlikte kalamaz: çök", "e", "lek (beyaz katı)"), tur_kelime="çökelek",
         kap=(("AgNO_3(suda)", "renksiz çözelti", "#EAF2F6"), ("NaCl(suda)", "renksiz çözelti", "#EAF2F6")), ipucu="AgCl suda çözünmez."),
    dict(kod="T2", durak="Ani", girenler=[(1, "HCl", "suda"), (1, "NaOH", "suda")], urunler=[(1, "NaCl", "suda"), (1, "H2O", "s")],
         tur="asit–baz (nötralleşme)", ana_urun="H2O", serit=("H", ["Cl", "+", "Na"], "OH"), serit_katli="HOH",
         gizli="Na^{+} ve Cl^{−} çözeltide kalır (seyirci iyonlar).",
         satirlar=[("HCl(suda) + NaOH(suda) → Na", "C", "l(suda)"), ("+ ", "H", "_2O(s)")],
         neden=("H^{+} ile OH^{−} su oluşturur: nötr", "a", "lleşme, renk yeşile döner"), tur_kelime="nötralleşme",
         kap=(("HCl(suda)", "bromtimol mavisiyle sarı", "#F2D43D"), ("NaOH(suda)", "bromtimol mavisiyle mavi", "#3D7BE8")), ipucu="Asit ile baz: tuz ve su."),
    dict(kod="T3", durak="Erzurum", girenler=[(1, "Fe", "k"), (1, "CuSO4", "suda")], urunler=[(1, "FeSO4", "suda"), (1, "Cu", "k")],
         tur="yer değiştirme (elektron alışverişi)", ana_urun="FeSO4", serit=("Fe", ["", "+", "Cu"], "SO_4"), serit_katli="FeSO4",
         gizli="Cu^{2+} 2 e^{−} alır, Cu(k) olarak çiviyi kaplar.",
         satirlar=[("Fe(k) + CuSO_4(suda) → FeS", "O", "_4(suda)"), ("+ ", "C", "u(k)")],
         neden=("Fe, Cu^{2+}’ye 2 e^{−} verir: çivi b", "a", "kırla kaplanır, mavi solar"), tur_kelime="bakırla",
         kap=(("Fe(k)", "demir çivi", None), ("CuSO_4(suda)", "mavi çözelti", "#3D9FE0")), ipucu="Fe, Cu’dan daha aktif."),
    dict(kod="T4", durak="Sarıkamış", girenler=[(2, "Mg", "k"), (1, "O2", "g")], urunler=[(2, "MgO", "k")],
         tur="yanma (sentez)", ana_urun="MgO", serit=("Mg", ["", "+", "O="], "O"), serit_katli="MgO",
         gizli="Öteki O atomu ikinci Mg ile birleşir: 2Mg + O_2.",
         satirlar=[("2Mg(k) + O_2(g) → 2M", "g", "O(k)")],
         neden=("Mg, O_2 ile birleşir: göz alıcı bir al", "e", "vle yanar, beyaz kül kalır"), tur_kelime="alevle",
         kap=(("Mg(k)", "şerit; tutuşturulur", None), ("O_2(g)", "havadaki oksijen", None)), ipucu="Yanma: O_2 ile birleşme."),
]


def _beher(cx, yb, w, h, sivi, doluluk=.62, k=.5):
    x0, yt, ys = cx - w / 2, yb - h, yb - h * doluluk
    govde = f"V{f(yb - 1.4)} Q{f(x0)} {f(yb)} {f(x0 + 1.4)} {f(yb)} H{f(x0 + w - 1.4)} Q{f(x0 + w)} {f(yb)} {f(x0 + w)} {f(yb - 1.4)}"
    o = f'<path d="M{f(x0)} {f(ys)} {govde} V{f(ys)} Z" fill="{sivi}"/>' if sivi else ""
    return o + (f'<path d="M{f(x0 - .9)} {f(yt)} H{f(x0)} {govde} V{f(yt)} H{f(x0 + w + .9)}" fill="none" stroke="#1B1D26" stroke-width="{k}" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')


def _urun_resmi(kod, yb, satir=None):
    """Ürün kabı (katlı uzay, dikiş u = 70'te ikiye bölünür). Kalın çizgiler; renkler fiziksel (palet değiştirmez).
    T1–T4 örnek tepkimelerin resmidir; başka satırda satir["urun_resmi"](yb) ya da satir["urun_renk"] renkli çözelti."""
    satir = satir or {}
    if callable(satir.get("urun_resmi")):
        return '<g data-tema-sabit="">' + satir["urun_resmi"](yb) + "</g>"
    o = ['<g data-tema-sabit="">']
    if kod not in ("T1", "T2", "T3", "T4"):
        o.append(_beher(A_X, yb, 26, 18, satir.get("urun_renk", "#EAF2F6"), .7, .8))
    elif kod == "T1":       # beyaz çökelek
        o.append(_beher(A_X, yb, 26, 18, "#DCEAF2", .7, .8))
        o.append(f'<path d="M57.6 {f(yb - .5)} Q63 {f(yb - 7.4)} 70 {f(yb - 7.9)} Q77 {f(yb - 7.4)} 82.4 {f(yb - .5)} Z" fill="#FFFFFF" stroke="#5F6F7B" stroke-width=".7" stroke-linejoin="round"/>')
        for dx, dy in ((-7.5, -9.6), (-3.8, -11.4), (3.8, -11.4), (7.5, -9.6), (-9.6, -6.4), (9.6, -6.4)):
            o.append(f'<circle cx="{f(A_X + dx)}" cy="{f(yb + dy)}" r=".85" fill="#FFFFFF" stroke="#5F6F7B" stroke-width=".35"/>')
    elif kod == "T2":     # nötr: bromtimol mavisi yeşil
        o.append(_beher(A_X, yb, 26, 18, "#63B95A", .7, .8))
    elif kod == "T3":     # çivinin çözeltideki kısmı bakırla kaplanır; çözelti soluk yeşile döner
        o.append(_beher(A_X, yb, 26, 18, "#CFE8D2", .7, .8))
        p0, p1 = (56.0, yb - 20.5), (78.0, yb - 3.4)
        t = (p0[1] - (yb - 18 * .7)) / (p0[1] - p1[1])           # çözelti yüzeyi
        j = (p0[0] + (p1[0] - p0[0]) * t, yb - 18 * .7)
        o.append(f'<path d="M{f(p0[0])} {f(p0[1])} L{f(j[0], 2)} {f(j[1], 2)}" stroke="#8E9CA8" stroke-width="2.4" stroke-linecap="round"/>'
                 f'<path d="M{f(p0[0] - 1.3)} {f(p0[1] + 1.6)} L{f(p0[0] + 1.3)} {f(p0[1] - 1.6)}" stroke="#5C6A76" stroke-width="1.5" stroke-linecap="round"/>'
                 f'<path d="M{f(j[0], 2)} {f(j[1], 2)} L{f(p1[0])} {f(p1[1])}" stroke="#B5622A" stroke-width="3.1" stroke-linecap="round"/>')
    else:                 # T4: göz alıcı beyaz alev, beyaz kül
        pts = []
        for i in range(20):
            a = i * math.pi / 10
            rr = 9.2 if i % 2 == 0 else 4.6
            pts.append((A_X + rr * math.cos(a), yb - 12.4 + rr * math.sin(a)))
        o.append(f'<path d="{cizgi_d(pts, True, 2)}" fill="#FFFDF0" stroke="#F0A21A" stroke-width=".9" stroke-linejoin="round"/>')
        o.append(f'<path d="M59 {f(yb - 3.4)} H81 L78.4 {f(yb)} H61.6 Z" fill="#B9C5CE" stroke="#1B1D26" stroke-width=".8" stroke-linejoin="round"/>'
                 f'<path d="M63 {f(yb - 3.4)} Q70 {f(yb - 8.2)} 77 {f(yb - 3.4)} Z" fill="#FFFFFF" stroke="#5F6F7B" stroke-width=".7" stroke-linejoin="round"/>')
    o.append("</g>")
    return "".join(o)


def _giren_kabi(kod, yan, cx, yb, renk):
    """Giren madde resmi (sayfa koordinatı; bir parçanın tamamen içinde)."""
    o = ['<g data-tema-sabit="">']
    if kod == "T3" and yan == 0:        # demir çivi
        o.append(f'<path d="M{f(cx - 6)} {f(yb - 2.6)} L{f(cx + 5)} {f(yb - 11.4)}" stroke="#8E9CA8" stroke-width="2.4" stroke-linecap="round"/>'
                 f'<path d="M{f(cx + 3.2)} {f(yb - 13.2)} L{f(cx + 6.8)} {f(yb - 9.6)}" stroke="#5C6A76" stroke-width="1.5" stroke-linecap="round"/>')
    elif kod == "T4" and yan == 0:      # magnezyum şerit
        o.append(f'<path d="M{f(cx - 6.5)} {f(yb - 4)} q3.2 -5 6.5 0 t6.5 0" fill="none" stroke="#1B1D26" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="M{f(cx - 6.5)} {f(yb - 4)} q3.2 -5 6.5 0 t6.5 0" fill="none" stroke="#C3CED8" stroke-width="2" stroke-linecap="round"/>')
    elif kod == "T4":                   # O₂: gaz kavanozu, iki molekül
        o.append(_beher(cx, yb, 15, 13.4, None))
        o.append(KK.kullan("kk-gaz-o2", cx - 6.6, yb - 12.6, 7.6) + KK.kullan("kk-gaz-o2", cx - .8, yb - 6.6, 7.6))
    else:
        o.append(_beher(cx, yb, 13, 13.4, renk))
    o.append("</g>")
    return "".join(o)


SERIT_BOY, SERIT_PAY = 5.8, .6           # büyük harf şeridi: harf kenarı dikişe 0,6 mm (katlayınca "AgCl" bitişik okunsun)


def tepkime_sayfasi(onek, rozet_svg, kare_svg="", kare_no=2, satirlar=None, rota="Yol 1 · Kars–Erzurum"):
    """Katla, tepkime olsun! satirlar: TEPKIME biçiminde 4 satır (verilmezse TEPKIME; yeni satırda ürün kabı rengi
    "urun_renk", resim gerekiyorsa "urun_resmi": fonksiyon(yb) → SVG). Dönen: (Sayfa, satır bilgileri)."""
    satirlar = satirlar or TEPKIME
    s = Sayfa(onek)
    _kat_isaretleri(s)
    _baslik(s, "Katla,", "tepkime olsun!", "(ama önce tahmin et!)", [rota, "Dört satır, tek katlama."],
            ["İki madde karşılaşınca ne olur?", "4 tahmin · +40 akçe"], rozet_svg, ["Önce tahmin et,", "sonra katla!"])
    _nasil_katlanir(s, "Önce yaz, sonra katla; aç ve açıkla.")
    s.ekle(yazi("Büyük harflere bak: katlayınca", 8, 45.5, 2.95, GOL_K, "nunito")[0] + yazi("ortadaki parça gizlenir,", 8, 49.6, 2.95, OBS2, "nunito")[0]
           + yazi("kalan harfler ürünü yazar.", 8, 53.7, 2.95, OBS2, "nunito")[0])
    bilgi = []
    for k, t in enumerate(satirlar):
        y0 = satir_y(k)
        yb = y0 + 21.4
        s.ekle(_bant(k) + _no(9.4, y0 + 6.2, k + 1))
        for yan, (ad, notu, renk) in enumerate(t["kap"]):       # girenler (açıkta) ve dökme okları
            cx = 22 if yan == 0 else 188
            s.ekle(_giren_kabi(t["kod"], yan, cx, yb - 3.4, renk))
            s.ekle(yazi(ad, cx, yb + 2.2, 3.5, OBS, "baloo", "orta")[0] + yazi(notu, cx, yb + 5.8, 2.6, OBS2, "nunito", "orta", en=34)[0])
            if yan == 0:
                s.ekle(_egri_ok((31.5, yb - 13), (42, yb - 18.6), (52.5, yb - 14.6), GUM_K, .6, 1.9))
            else:
                s.ekle(_egri_ok((178.5, yb - 13), (168, yb - 18.6), (157.5, yb - 14.6), GUM_K, .6, 1.9))
        s.dikis(_urun_resmi(t["kod"], yb, t))
        # büyük harf şeridi: açıkken girenler okunur, katlayınca ürün (orta şeritteki parça gizlenir)
        ys = y0 + 33.4
        sol, orta, sag = t["serit"]
        sv1, sx0, sx1 = yazi(sol, A_X - SERIT_PAY, ys, SERIT_BOY, OBS, "baloo", "sag")
        sv2, gx0, gx1 = yazi(sag, B_X + SERIT_PAY, ys, SERIT_BOY, OBS, "baloo", "sol")
        s.ekle(sv1 + sv2)
        orta_x = []
        for parca, x, hiza in ((orta[0], A_X + SERIT_PAY, "sol"), (orta[1], 105, "orta"), (orta[2], B_X - SERIT_PAY, "sag")):
            if parca:
                sv, ox0, ox1 = yazi(parca, x, ys, SERIT_BOY, SOLUK, "baloo", hiza)
                s.ekle(sv)
                orta_x.append((ox0, ox1))
        # denklem (ürün başına bir satır: her ürün dikişte bölünür) ve neden
        parca, uclar = [], []
        for j, (a, b, c) in enumerate(t["satirlar"]):
            svg, u0, u1 = bolunmus(a, b, c, y0 + (38.9 + j * 4.5 if len(t["satirlar"]) > 1 else 41.2), 3.7)
            parca.append(svg)
            uclar.append((u0, u1))
        svg, u0, u1 = bolunmus(*t["neden"], y0 + 47.9, 3.35, OBS2, "nunito")
        s.dikis("".join(parca) + svg, yazi_mi=True)
        bilgi.append(dict(kod=t["kod"], satir_u=uclar, neden_u=(u0, u1), serit_x=((sx0, sx1), (gx0, gx1)), orta_x=orta_x))
        s.ekle(_orta_kart(y0 + 2.5, y0 + 26.6, "ÖNCE TAHMİN ET", ["Ürün:", "Tepkime türü:"], [t["ipucu"]]))
        s.ekle(_orta_kart(y0 + 36.2, y0 + 47.4, "AÇ VE AÇIKLA", soru="Gizlenen parçaya ne oldu?"))
        urun = _alt_simge(t["ana_urun"])
        s.ekle(_ogr_grubu(t["kod"], urun, t["tur"],
                          _orta_cevap(y0 + 2.5, y0 + 26.6, ["Ürün:", "Tepkime türü:"], [urun, t["tur"]])
                          + _orta_cevap(y0 + 36.2, y0 + 47.4, soru="Gizlenen parçaya ne oldu?", soru_cevap=t["gizli"])))
    _alt_bolum(s, kare_svg, "Deneyleri yalnız öğretmeninle yap.", "Mg alevine doğrudan bakma!", kare_no)
    return s, bilgi


# ------------------------------------------------------------------ SAYFA KÖŞESİ ÇİZGİ FİLMİ (24 kare)

KARE_SAYISI = 24
ENERJI = {n: -13.6 / n ** 2 for n in (1, 2, 3)}             # H atomu, eV
_Y1, _Y3 = 86.0, 42.0                                          # n = 1 ve n = 3 basamaklarının üstü (kare birimi)
_EL, _FOT = 34, 38                                             # elektron ve foton genişliği (kare birimi)
_P = {n: (x, round(_Y1 - (ENERJI[n] - ENERJI[1]) / (ENERJI[3] - ENERJI[1]) * (_Y1 - _Y3), 1)) for n, x in ((1, 22), (2, 54), (3, 82))}
FILM = [(1, 4, "Mor ötesi bir foton yaklaşır."), (5, 6, "Elektron fotonu soğurur."), (7, 12, "n = 1’den n = 3’e sıçrar."),
        (13, 15, "Uyarılmış hâl kısa sürer."), (16, 22, "n = 3’ten n = 2’ye iner: kırmızı foton (656 nm)."),
        (23, 24, "n = 2’den n = 1’e iner: mor ötesi foton (122 nm).")]


def kare(i, onek="kr"):
    """i. kare (0…23), viewBox 0 0 100 100: elektron foton soğurur, n = 3'e çıkar, inerken kırmızı foton yayar.
    Basamak yükseklikleri enerjiyle orantılı (E_n = −13,6/n² eV)."""
    i = int(i) % KARE_SAYISI
    y2, y3 = _P[2][1], _P[3][1]
    o = [f'<path d="M4 95 V{f(_Y1)} H40 V{f(y2)} H68 V{f(y3)} H96 V95 Z" fill="#F0E2C2" stroke="#1B1D26" stroke-width="2.2" stroke-linejoin="round"/>']
    for n, (x, y) in _P.items():
        o.append(f'<text x="{x}" y="{f(y + (7.6 if n == 1 else 10))}" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="{7.5 if n == 1 else 9}" fill="#8A6212">n={n}</text>')

    def el(x, y, tur=""):
        return KK.kullan("kk-elektron" + (f"-{tur}" if tur else ""), x - _EL / 2, y - _EL * 25 / 26, _EL)

    def fot(kimlik, cx, cy, w=_FOT, ayna=False):
        return KK.kullan(kimlik, cx - w / 2, cy - w * 50 / 92 / 2, w, ayna=ayna)

    def ara(a, b, t, kavis):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t - kavis * math.sin(math.pi * t))
    if i <= 3:                        # UV foton yukarıdan gelir
        o.append(el(*_P[1]))
        o.append(fot("kk-foton-uv", 22, -8 + 15 * i))
    elif i <= 5:                      # soğurma: parlama
        pts = []
        for k in range(16):
            a = k * math.pi / 8
            rr = (19 if i == 4 else 13) * (1 if k % 2 == 0 else .5)
            pts.append((22 + rr * math.cos(a), 70 + rr * math.sin(a)))
        o.append(f'<path d="{cizgi_d(pts, True)}" fill="#FFE27A" stroke="#1B1D26" stroke-width="1.6" stroke-linejoin="round"/>')
        o.append(el(_P[1][0], _P[1][1] - (0 if i == 4 else 4), "heyecan"))
    elif i <= 11:                     # n = 1 → n = 3 sıçrayışı
        o.append(el(*ara(_P[1], _P[3], (i - 5) / 7, 18), "heyecan"))
    elif i <= 14:                     # uyarılmış hâl
        o.append(el(_P[3][0] + (0, 1.8, -1.8)[i - 12], _P[3][1], "heyecan"))
    elif i <= 17:                     # n = 3 → n = 2 inişi; kırmızı foton çıkar
        o.append(el(*ara(_P[3], _P[2], (i - 14) / 4, 5), "sasiran"))
        if i == 17:
            o.append(fot("kk-foton-656", 76, 22))
    elif i <= 21:                     # n = 2'de; foton sağa uçar
        o.append(el(*_P[2], "sakin"))
        o.append(fot("kk-foton-656", 84 + 8 * (i - 18), 22 - 2 * (i - 18)))
    else:                             # n = 2 → n = 1 (UV foton sola gider)
        o.append(el(*ara(_P[2], _P[1], (i - 21) / 2, 4), "" if i == 23 else "sakin"))
        o.append(fot("kk-foton-uv", 40 - 20 * (i - 22), 18 - 8 * (i - 22), ayna=True))
    return (f'<svg class="kare" viewBox="0 0 100 100" data-kare="{i + 1}"><defs><clipPath id="{onek}{i}"><rect x="3" y="3" width="94" height="94" rx="7.5"/></clipPath></defs>'
            f'<rect x="1.5" y="1.5" width="97" height="97" rx="9" fill="#FFFFFF"/><g data-tema-sabit="" clip-path="url(#{onek}{i})">{"".join(o)}</g>'
            f'<rect x="1.5" y="1.5" width="97" height="97" rx="9" fill="none" stroke="#1B1D26" stroke-width="3"/></svg>')


FILM_KARE = 27.0
FILM_X = (11, 40, 76, 107, 143, 172)            # 3 sütun grubu: kat yerleri (70, 140) sütun aralığına denk gelir
FILM_Y = (40, 76, 112, 148)


def film_yerleri():
    """24 karenin sayfadaki sol üst köşeleri (mm), sırayla."""
    return [(x, y) for y in FILM_Y for x in FILM_X]


def film_izgara(onek="fz"):
    o = []
    for i, (x, y) in enumerate(film_yerleri()):
        o.append(kare(i, onek).replace("<svg ", f'<svg x="{x}" y="{y}" width="{FILM_KARE}" height="{FILM_KARE}" ', 1))
        o.append(_no(x + FILM_KARE / 2, y + FILM_KARE + 3.4, i + 1, GOL_K, 2.3, 2.8))
    return f'<svg class="film-svg" viewBox="0 0 210 297" data-serbest="">{"".join(o)}</svg>'


# ------------------------------------------------------------------ KÖŞEYİ KATLA (ön yüz sağ alt köşe ↔ arka yüz sol alt köşe)

KOSE_A = 64.0       # kat çizgisinin köşeden uzaklığı (mm): çizgi (W − a, H) ile (W, H − a) noktalarından geçer
KOSE_CEVAP = ("CEVAP", "V_2 = 3 L", "260 K → 300 K")


def kose_on(a=KOSE_A):
    """Ön yüz, sağ alt köşe (a × a mm; yerel koordinat: kare [W − a, W] × [H − a, H]). Üst-sol üçgen: katlanınca cevabın
    örttüğü yer · alt-sağ üçgen: öne katlanacak köşe."""
    m, k = a / 2, 1 / math.sqrt(2)
    o = [f'<path d="M0 0 H{f(a)} L0 {f(a)} Z" fill="#FFFFFF"/><path d="M{f(a)} 0 V{f(a)} H0 Z" fill="{KEH_A}"/>',
         f'<path d="M.3 {f(a - .3)} V.3 H{f(a - .3)}" fill="none" stroke="{GUM}" stroke-width=".35" stroke-dasharray="1 1.1"/>',
         f'<path d="M0 {f(a)} L{f(a)} 0" stroke="{MER}" stroke-width=".55" stroke-dasharray="2.2 1.5"/>',
         yazi("Köşeyi katlayınca", 4, 7.5, 2.95, SOLUK, "nunito")[0], yazi("cevap burada belirir.", 4, 11.6, 2.95, SOLUK, "nunito")[0]]
    for uz, metin, boy, renk, font in ((6.5, "KÖŞEYİ ÖNE KATLA", 3.35, MER_K, "nunito9"), (11.4, "cevap arka yüzde", 2.95, OBS2, "nunito")):
        o.append(f'<g transform="translate({f(m + uz * k, 2)} {f(m + uz * k, 2)}) rotate(-45)">{yazi(metin, 0, 0, boy, renk, font, "orta")[0]}</g>')
    o.append(_ok(m + 27 * k, m + 27 * k, m + 17.5 * k, m + 17.5 * k, MER_K, 1.1, 3.4))
    return f'<svg class="kose-svg on" viewBox="0 0 {f(a)} {f(a)}" data-serbest="">{"".join(o)}</svg>'


def kose_cevap_ici(a=KOSE_A, cevap=KOSE_CEVAP):
    """Cevap, katlı görünüm koordinatında (p sağa, q aşağı; dik açı sol üstte, p + q ≤ a)."""
    return [f'<path d="M0 0 H{f(a)} L0 {f(a)} Z" fill="{KEH_A}"/>', _cip(7, 7, cevap[0], KEH, OBS)[0],
            yazi(cevap[1], 7, 20.4, 6.2, OBS, "baloo")[0], yazi(cevap[2], 7, 26.8, 3.2, OBS2, "baloo")[0],
            '<use href="#pamuk-bas-gulen" x="7" y="30" width="10" height="9.76"/>']


def kose_arka(a=KOSE_A, cevap=KOSE_CEVAP):
    """Arka yüz, sol alt köşe (a × a mm; yerel koordinat: kare [0, a] × [H − a, H]). Cevap katlı görünüm koordinatında
    çizilir ve translate(0 a) rotate(-90) ile basılır: (p, q) → (q, a − p). Arka yüzde saat yönünün tersine 90° dönük
    durur; köşe öne katlanınca düz okunur (türetme: README ve dogrula.py)."""
    return (f'<svg class="kose-svg arka" viewBox="0 0 {f(a)} {f(a)}" data-serbest=""><g transform="translate(0 {f(a)}) rotate(-90)">{"".join(kose_cevap_ici(a, cevap))}</g>'
            f'<path d="M0 0 L{f(a)} {f(a)}" stroke="{MER}" stroke-width=".55" stroke-dasharray="2.2 1.5"/></svg>')


def kose_adimlar(cevap="3 L"):
    """Üç adımlı köşe katlama çizimi (viewBox 0 0 168 44). cevap: 3. adımdaki katlı köşede görünen kısa cevap."""
    o = []
    for i, (metin, alt) in enumerate((("Soruyu çöz,", "cevabını yaz."), ("Sağ alt köşeyi", "çizgiden öne katla."), ("Cevap düz okunur:", "karşılaştır, geri aç."))):
        x = 4 + i * 58
        o.append(_no(x + 3, 6, i + 1, GOL_K) + yazi(metin, x + 8, 7.2, 3.35, OBS, "nunito")[0] + yazi(alt, x + 8, 11.4, 3.35, OBS2, "nunito")[0])
        px, py, w, h, c = x + 6, 15, 20, 27, 9.0
        if i == 0:
            o.append(f'<path d="M{px} {py} h{w} v{h} h{-w} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width=".5" stroke-linejoin="round"/>'
                     f'<path d="M{px + w - c} {py + h} L{px + w} {py + h - c}" stroke="{MER}" stroke-width=".5" stroke-dasharray="1.2 .9"/>')
        else:
            o.append(f'<path d="M{px} {py} h{w} v{h - c} l{-c} {c} h{-(w - c)} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width=".5" stroke-linejoin="round"/>')
            if i == 1:      # köşe havada: yarı katlı üçgen ve ok
                o.append(f'<path d="M{px + w - c} {py + h} L{px + w} {py + h - c} L{px + w - 2.4} {py + h - 2.4} Z" fill="{KEH_A}" stroke="{OBS}" stroke-width=".5" stroke-linejoin="round"/>')
                o.append(_egri_ok((px + w + 3, py + h - 1), (px + w + 3, py + h - c - 5), (px + w - c + 1.5, py + h - c - 3.4), MER_K, .7, 2))
            else:           # katlı: arka yüzün köşesi görünür
                o.append(f'<path d="M{px + w - c} {py + h} L{px + w} {py + h - c} H{px + w - c} Z" fill="{KEH_A}" stroke="{OBS}" stroke-width=".5" stroke-linejoin="round"/>')
                o.append(yazi(cevap, px + w - c + .6, py + h - c + 3.6, 2.7, OBS, "baloo", en=c - 1)[0])
        for j in range(4):
            o.append(f'<path d="M{px + 3} {py + 5 + j * 3.6} h{(w - 6) if j < 3 else 8}" stroke="{GUM}" stroke-width=".5" stroke-linecap="round"/>')
        if i < 2:
            o.append(_ok(x + 40, 28, x + 50, 28, GUM_K, .7, 2.2))
    return f'<svg class="kose-adimlar" viewBox="0 0 168 44">{"".join(o)}</svg>'


def kose_harita(cevap="3 L"):
    """Arka yüz baskısının neden 90° döndüğünü gösteren üçlü çizim (viewBox 0 0 176 62). cevap: köşedeki kısa cevap."""
    o = []
    for i, (bas, alt) in enumerate((("Ön yüz", "köşe sağ altta"), ("Arka yüz", "aynı köşe sol altta"), ("Köşe katlanınca", "arka yüz öne gelir"))):
        x = 4 + i * 60
        o.append(yazi(bas, x + 2, 6, 3.35, OBS, "baloo")[0] + yazi(alt, x + 2, 10.4, 2.95, OBS2, "nunito")[0])
        px, py, w, h, c = x + 4, 14, 30, 42, 14.0
        if i < 2:
            o.append(f'<path d="M{px} {py} h{w} v{h} h{-w} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width=".5"/>')
            if i == 0:
                o.append(f'<path d="M{px + w - c} {py + h} L{px + w} {py + h - c} V{py + h} Z" fill="{KEH_A}"/>'
                         f'<path d="M{px + w - c} {py + h} L{px + w} {py + h - c}" stroke="{MER}" stroke-width=".5" stroke-dasharray="1.2 .9"/>')
            else:           # arka yüz: cevap sol altta, 90° sola dönük ("3 L" aşağıdan yukarı okunur)
                o.append(f'<path d="M{px} {py + h - c} L{px + c} {py + h} H{px} Z" fill="{KEH_A}"/>'
                         f'<path d="M{px} {py + h - c} L{px + c} {py + h}" stroke="{MER}" stroke-width=".5" stroke-dasharray="1.2 .9"/>')
                o.append(f'<g transform="translate({px + 4.6} {py + h - 1.6}) rotate(-90)">{yazi(cevap, 0, 0, 3.6, OBS, "baloo", en=c - 2)[0]}</g>')
        else:
            o.append(f'<path d="M{px} {py} h{w} v{h - c} l{-c} {c} h{-(w - c)} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width=".5" stroke-linejoin="round"/>'
                     f'<path d="M{px + w - c} {py + h} L{px + w} {py + h - c} H{px + w - c} Z" fill="{KEH_A}" stroke="{OBS}" stroke-width=".5" stroke-linejoin="round"/>')
            o.append(yazi(cevap, px + w - c + .8, py + h - c + 4.6, 3.6, OBS, "baloo", en=c - 1.6)[0])
        if i < 2:
            o.append(_ok(x + 39, 35, x + 59, 35, GUM_K, .7, 2.2))
    o.append(yazi("çevir", 52, 33, 2.75, GUM_K, "nunito", "orta")[0] + yazi("katla", 112, 33, 2.75, GUM_K, "nunito", "orta")[0])
    return f'<svg class="kose-harita" viewBox="0 0 176 62">{"".join(o)}</svg>'


# ------------------------------------------------------------------ karma sayfa ikonları

def ikon(ad):
    """Çizgi ikonlar (ortak ikonlarla aynı dil: 24 × 24, currentColor)."""
    ic = {
        "kapi": '<path d="M5 22 V10 a7 7 0 0 1 14 0 V22 Z"/><path d="M12 3 V22"/><circle cx="9.3" cy="14" r=".9"/><circle cx="14.7" cy="14" r=".9"/><path d="M3 22 H21"/>',
        "rontgen": '<rect x="3" y="3" width="13" height="16" rx="2"/><path d="M6.5 7.5 h6 M6.5 11 h6 M6.5 14.5 h3.5"/><circle cx="16.5" cy="16.5" r="3.6"/><path d="M19.2 19.2 L22 22"/>',
        "robot": '<rect x="4.5" y="8" width="15" height="11" rx="3"/><path d="M12 8 V4.5"/><circle cx="12" cy="3.4" r="1.2"/><circle cx="9" cy="12.6" r="1.3"/><circle cx="15" cy="12.6" r="1.3"/><path d="M9 16 h6 M2.5 12 v3.5 M21.5 12 v3.5"/>',
        "heybe": '<path d="M4 6.5 H20"/><path d="M3.5 6.5 h7.5 v8.5 a3.75 3.75 0 0 1 -7.5 0 Z"/><path d="M13 6.5 h7.5 v8.5 a3.75 3.75 0 0 1 -7.5 0 Z"/><path d="M3.5 10.5 h7.5 M13 10.5 h7.5 M7.2 18.8 v2.4 M16.8 18.8 v2.4"/>',
        "nine": '<path d="M5 21 c0 -5 2.5 -7.2 7 -7.2 s7 2.2 7 7.2"/><circle cx="12" cy="8.6" r="4"/><path d="M6.8 9.4 c-.2 -5 2.4 -7.2 5.2 -7.2 s5.4 2.2 5.2 7.2"/>',
        "film": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4 v16 M17 4 v16 M3 9 h4 M3 15 h4 M17 9 h4 M17 15 h4"/><path d="M10.4 9.4 v5.2 l4 -2.6 Z"/>',
        "kose": '<path d="M4 3 h16 v11 l-7 7 H4 Z"/><path d="M20 14 h-7 v7"/>',
        "katla": '<path d="M3 5 h6 v14 H3 Z M15 5 h6 v14 h-6 Z"/><path d="M9 7 l3 -2 l3 2 M9 17 l3 2 l3 -2"/>',
    }[ad]
    return f'<svg class="ikon" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{ic}</g></svg>'


def robot():
    """KimyaBot: kurgusal yapay zekâ (viewBox 0 0 60 60; el yok)."""
    return (f'<svg class="robot" viewBox="0 0 60 60"><path d="M30 12 V6" stroke="{OBS}" stroke-width="2" stroke-linecap="round"/><circle cx="30" cy="5" r="2.8" fill="{MER}" stroke="{OBS}" stroke-width="1.4"/>'
            f'<rect x="4" y="24" width="6" height="12" rx="2.5" fill="{GUM}" stroke="{OBS}" stroke-width="1.6"/><rect x="50" y="24" width="6" height="12" rx="2.5" fill="{GUM}" stroke="{OBS}" stroke-width="1.6"/>'
            f'<rect x="9" y="12" width="42" height="34" rx="9" fill="{GOL_A}" stroke="{OBS}" stroke-width="2"/>'
            f'<circle cx="21.5" cy="26" r="6" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6"/><circle cx="38.5" cy="26" r="6" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6"/>'
            f'<circle cx="22.6" cy="26.6" r="2.6" fill="{OBS}"/><circle cx="39.6" cy="26.6" r="2.6" fill="{OBS}"/>'
            f'<rect x="21" y="36" width="18" height="5.4" rx="2" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.4"/><path d="M25.5 36 v5.4 M30 36 v5.4 M34.5 36 v5.4" stroke="{OBS}" stroke-width="1.1"/>'
            f'<path d="M22 46 h16 v4 h-16 Z" fill="{GUM}" stroke="{OBS}" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 58 q0 -8 9 -8 h18 q9 0 9 8 Z" fill="{GOL}" stroke="{OBS}" stroke-width="2" stroke-linejoin="round"/></svg>')


def kapi():
    """Şifreli Kapı: kemerli kapı ve asma kilit (viewBox 0 0 44 50)."""
    yil = cizgi_d(selcuklu_yildizi(22, 14, 6.4), True, 2)
    return (f'<svg class="kapi" viewBox="0 0 44 50"><path d="M4 49 V20 A18 18 0 0 1 40 20 V49 Z" fill="{KEH_A}" stroke="{OBS}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M9 49 V21 A13 13 0 0 1 35 21 V49 Z" fill="{GOL}" stroke="{OBS}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M22 8 V49" stroke="{OBS}" stroke-width="1.2"/><path d="{yil}" fill="{KEH}" stroke="{OBS}" stroke-width="1"/>'
            f'<path d="M17.5 31 v-3.2 a4.5 4.5 0 0 1 9 0 V31" fill="none" stroke="{OBS}" stroke-width="1.8"/>'
            f'<rect x="15" y="30.5" width="14" height="11" rx="2" fill="{KEH}" stroke="{OBS}" stroke-width="1.5"/><circle cx="22" cy="35" r="1.5" fill="{OBS}"/><path d="M22 35.5 v3" stroke="{OBS}" stroke-width="1.3"/></svg>')
