"""Periyodik Özellikler · üniteye özel bilgi grafikleri ({{info|ad}} önce buraya bakar).

Grafiklerdeki BÜTÜN sayılar aşağıdaki VERI sözlüğünden gelir; dogrula.py aynı sözlüğü içe aktarıp sorulardaki
sayılarla ve sıralamalarla karşılaştırır (grafik ile soru tek kaynaktan). Değerler klasik ünitenin
(kitap/9-sinif/05-periyodik-ozellikler) değerleridir:
  • atom yarıçapı (pm, yaklaşık) · iyon yarıçapı (pm, yaklaşık)
  • 1. ve ardışık iyonlaşma enerjileri (kJ/mol, yuvarlatılmış ölçüm değerleri)
  • elektronegatiflik: Pauling ölçeği (F = 4,0), birimsiz, bir ondalık
Klasik ünitede olmayan birkaç ardışık İE (Na, Mg İE₃, Ca) aynı ölçüm tablosundan, aynı yuvarlamayla eklendi.
Element adları ve sınıfları (metal · yarı metal · ametal · soy gaz) kitabın periyodik tablosuyla aynıdır
(yerel-cerceve/uretec/elementler.py; dogrula.py bunu denetler).
"""
import math
import re
from cizim.temel import Svg, f, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A, ALTIN,
                           ALTIN_K, ALTIN_A, ERGUVAN, ZUMRUT, GUM, GUM_K, GUM_A, LAJVER, DERIN)

T = 'font-family="Nunito" font-weight="800"'
T9 = 'font-family="Nunito" font-weight="900"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'
DJ = 'font-family="DejaVu Sans" font-weight="700"'     # δ, ok gibi Baloo/Nunito'da olmayan işaretler için gerçek kalın yedek
PAS = "#B5543A"        # Divriği demirinin pas kızılı
PAS_K = "#7A3326"
PAS_A = "#F6DCCF"

# ------------------------------------------------------------------ veri (dogrula.py da bunu kullanır)
VERI = {
    # atom yarıçapı (pm, yaklaşık) — klasik ünite svgler.py 'rad'
    "r": {"H": 37, "Li": 152, "Be": 112, "B": 85, "C": 77, "N": 75, "O": 73, "F": 72,
          "Na": 186, "Mg": 160, "Al": 143, "Si": 118, "P": 110, "S": 103, "Cl": 99,
          "K": 227, "Ca": 197, "Ga": 135, "Ge": 122, "As": 120, "Se": 117, "Br": 114},
    # iyon yarıçapı (pm, yaklaşık) — klasik ünite: izoelektronik seri, Na⁺/Cl⁻, bağlam ve merdiven soruları
    "ri": {"N3-": 146, "O2-": 140, "F-": 133, "Na+": 102, "Mg2+": 72, "Al3+": 54, "Cl-": 181, "K+": 138, "Ca2+": 100, "Li+": 76},
    # 1. iyonlaşma enerjisi (kJ/mol)
    "ie1": {"H": 1312, "He": 2372, "Li": 520, "Be": 899, "B": 801, "C": 1086, "N": 1402, "O": 1314, "F": 1681, "Ne": 2081,
            "Na": 496, "Mg": 738, "Al": 578, "Si": 786, "P": 1012, "S": 1000, "Cl": 1251, "Ar": 1521, "K": 419, "Ca": 590,
            "Rb": 403, "Sr": 549, "Cs": 376},
    # ardışık iyonlaşma enerjileri (kJ/mol)
    "ie": {"C": [1086, 2353, 4621, 6223, 37831], "Rb": [403, 2633, 3860, 5080], "Sr": [549, 1064, 4138, 5500],
           "Al": [578, 1817, 2745, 11577], "Si": [786, 1577, 3232, 4356], "P": [1012, 1907, 2914, 4964, 6274, 21267],
           "B": [801, 2427, 3660, 25026], "O": [1314, 3388, 5301, 7469, 10990, 13327, 71330],
           "Mg": [738, 1451, 7733], "Na": [496, 4562, 6910, 9543], "Ca": [590, 1145, 4912, 6491]},
    # elektronegatiflik · Pauling ölçeği (F = 4,0) — klasik ünite 'en' + bağlam sorusundaki I
    "en": {"H": 2.2, "Li": 1.0, "Be": 1.6, "B": 2.0, "C": 2.6, "N": 3.0, "O": 3.4, "F": 4.0,
           "Na": 0.9, "Mg": 1.3, "Al": 1.6, "Si": 1.9, "P": 2.2, "S": 2.6, "Cl": 3.2, "K": 0.8, "Ca": 1.0, "Br": 3.0, "I": 2.7},
}

# atom numarası ve baş grup yerleri (periyot, A grubu)
Z = {"H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10, "Na": 11, "Mg": 12, "Al": 13, "Si": 14,
     "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20, "Ga": 31, "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Kr": 36,
     "Rb": 37, "Sr": 38, "In": 49, "Sn": 50, "Sb": 51, "Te": 52, "I": 53, "Xe": 54, "Cs": 55, "Ba": 56, "Tl": 81, "Pb": 82,
     "Bi": 83, "Po": 84, "At": 85, "Rn": 86, "Fr": 87, "Ra": 88}
TABLO = [["H", None, None, None, None, None, None, "He"],
         ["Li", "Be", "B", "C", "N", "O", "F", "Ne"],
         ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"],
         ["K", "Ca", "Ga", "Ge", "As", "Se", "Br", "Kr"],
         ["Rb", "Sr", "In", "Sn", "Sb", "Te", "I", "Xe"],
         ["Cs", "Ba", "Tl", "Pb", "Bi", "Po", "At", "Rn"]]
YER = {s: (p + 1, g + 1) for p, satir in enumerate(TABLO) for g, s in enumerate(satir) if s}
# kitabın periyodik tablosuyla aynı sınıflar (elementler.py)
SINIF = {}
for _s in Z:
    SINIF[_s] = ("yari" if _s in {"B", "Si", "Ge", "As", "Sb", "Te"} else "ametal" if _s in {"H", "C", "N", "O", "F", "P", "S", "Cl", "Se", "Br", "I"}
                 else "soy" if _s in {"He", "Ne", "Ar", "Kr", "Xe", "Rn"} else "belirsiz" if _s in {"Po", "At"} else "metal")
# metinde geçen element adları (elementler.py ile aynı yazılış)
AD = {"H": "Hidrojen", "He": "Helyum", "Li": "Lityum", "Be": "Berilyum", "B": "Bor", "C": "Karbon", "N": "Azot", "O": "Oksijen",
      "F": "Flor", "Ne": "Neon", "Na": "Sodyum", "Mg": "Magnezyum", "Al": "Alüminyum", "Si": "Silisyum", "P": "Fosfor",
      "S": "Kükürt", "Cl": "Klor", "Ar": "Argon", "K": "Potasyum", "Ca": "Kalsiyum", "Cr": "Krom", "Fe": "Demir", "Cu": "Bakır",
      "Br": "Brom", "Rb": "Rubidyum", "Sr": "Stronsiyum", "Se": "Selenyum", "Ag": "Gümüş", "I": "İyot", "Cs": "Sezyum",
      "Pb": "Kurşun", "Fr": "Fransiyum"}
SEMBOL_Z = {s: n for s, n in Z.items()}


def _alt(metin, x, y, fs, renk=OBS, anchor="middle", font=B):
    """Yazı içinde _2 → alt simge, ^{…} → üst simge (tspan dy). (10-sinif-yerel/01 deseni; yerel kopya.)"""
    parca = re.split(r"(_\d+|\^\{[^}]*\})", metin)
    o = [f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(fs)}" fill="{renk}">']
    dy = 0
    for p in parca:
        if not p:
            continue
        if p.startswith("_"):
            o.append(f'<tspan dy="{f(fs * .24 - dy)}" font-size="{f(fs * .66)}">{p[1:]}</tspan>')
            dy = fs * .24
        elif p.startswith("^"):
            o.append(f'<tspan dy="{f(-fs * .38 - dy)}" font-size="{f(fs * .62)}">{p[2:-1]}</tspan>')
            dy = -fs * .38
        else:
            o.append(f'<tspan dy="{f(-dy)}">{p}</tspan>' if dy else p)
            dy = 0
    o.append("</text>")
    return "".join(o)


def _ok(x0, y0, x1, y1, renk=OBS, k=5, uc=16):
    a = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - uc * math.cos(a - .45), y1 - uc * math.sin(a - .45))
    p2 = (x1 - uc * math.cos(a + .45), y1 - uc * math.sin(a + .45))
    return (f'<path d="M{f(x0)} {f(y0)} L{f(x1 - uc * .6 * math.cos(a))} {f(y1 - uc * .6 * math.sin(a))}" stroke="{renk}" stroke-width="{f(k)}" stroke-linecap="round"/>'
            f'<path d="M{f(x1)} {f(y1)} L{f(p1[0])} {f(p1[1])} L{f(p2[0])} {f(p2[1])} Z" fill="{renk}"/>')


def _vir(v, h=1):
    """Ondalık virgül: 2.2 → '2,2'."""
    return f"{v:.{h}f}".replace(".", ",")


def _bin(v):
    """Binlik ayıraç ince boşluk: 37831 → '37 831'."""
    s = str(int(v))
    return s if len(s) <= 4 else s[:-3] + " " + s[-3:]


# ================================================================== 1. DURAK · r = d/2

def rd_cizim(onek="m2-rd"):
    """Bağlı iki özdeş atom: çekirdekler arası uzaklık d, yarıçap r = d/2."""
    s = Svg(onek)
    W, H = 560, 250
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFF8F2"/>'
    g = s.rad([(0, PAS, .55), (.7, PAS, .22), (1, PAS, .1)], ad="bl")
    for cx in (165, 305):
        s += f'<circle cx="{cx}" cy="112" r="96" fill="{g}" stroke="{PAS_K}" stroke-width="3"/>'
        s += f'<circle cx="{cx}" cy="112" r="9" fill="{PAS_K}"/>'
    s += f'<path d="M165 112 H305" stroke="{KEH}" stroke-width="6"/>'
    s += f'<path d="M165 112 H235" stroke="{OBS}" stroke-width="3" stroke-dasharray="6 5"/>'
    s += _alt("r", 200, 98, 34, renk=KEH_K)
    s += f'<path d="M165 224 H305 M165 212 V236 M305 212 V236" stroke="{OBS}" stroke-width="3" fill="none"/>'
    s += f'<text x="235" y="218" text-anchor="middle" {B} font-size="30" fill="{OBS}">d</text>'
    s += f'<text x="470" y="104" text-anchor="middle" {B} font-size="46" fill="{PAS_K}">r = d/2</text>'
    s += f'<text x="470" y="146" text-anchor="middle" {T} font-size="21" fill="{GUM_K}">çekirdekler</text>'
    s += f'<text x="470" y="172" text-anchor="middle" {T} font-size="21" fill="{GUM_K}">arası uzaklığın</text>'
    s += f'<text x="470" y="198" text-anchor="middle" {T} font-size="21" fill="{GUM_K}">yarısı</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info rd")


# ================================================================== 1. DURAK · mini tabloda atom yarıçapları

def yaricap_tablosu(onek="m2-yt"):
    """Periyot 1–4 × 1A–7A: daire alanı yarıçapla orantılı (ölçekli), değerler pm. Oklar: büyüme yönü."""
    s = Svg(onek)
    W, H = 930, 560
    x0, y0, cw, ch = 74, 54, 112, 112
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for g in range(7):
        s += f'<text x="{x0 + g * cw + cw / 2}" y="{y0 - 16}" text-anchor="middle" {B} font-size="27" fill="{PAS_K}">{g + 1}A</text>'
    for p in range(4):
        y = y0 + p * ch
        s += f'<rect x="{x0 - 2}" y="{y + 2}" width="{7 * cw + 4}" height="{ch - 4}" rx="14" fill="{["#FFF4EC", "#FBEFE6", "#F6E7DD", "#F1DFD4"][p]}"/>'
        s += f'<text x="{x0 - 30}" y="{y + ch / 2 + 9}" text-anchor="middle" {B} font-size="28" fill="{PAS_K}">{p + 1}</text>'
    k = 50 / 227
    for (p, g), sym in sorted(((v, k_) for k_, v in YER.items() if k_ in VERI["r"]), key=lambda t: t[0]):
        r_pm = VERI["r"][sym]
        cx = x0 + (g - 1) * cw + cw / 2
        cy = y0 + (p - 1) * ch + ch / 2 - 12
        R = r_pm * k
        t = r_pm / 227
        dolgu = karis("#F9C9A8", PAS_K, t ** .9)
        hl = s.rad([(0, acik(dolgu, .45)), (1, dolgu)], .35, .3, .75, ad="kr")
        s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R)}" fill="{hl}" stroke="{PAS_K}" stroke-width="2.4"/>'
        if R > 17:
            s += f'<text x="{f(cx)}" y="{f(cy + 9)}" text-anchor="middle" {B} font-size="{f(min(28, 12 + R * .42))}" fill="{"#FFFFFF" if t > .45 else OBS}">{sym}</text>'
        else:
            s += f'<text x="{f(cx + R + 4)}" y="{f(cy - R + 2)}" text-anchor="start" {B} font-size="22" fill="{OBS}">{sym}</text>'
        s += f'<text x="{f(cx)}" y="{f(y0 + p * ch - 8)}" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">{r_pm}</text>'
    xr = x0 + 7 * cw + 40
    s += _ok(xr, y0 + 10, xr, y0 + 4 * ch - 10, PAS, 7, 22)
    s += f'<text transform="translate({xr + 34} {y0 + 2 * ch}) rotate(90)" text-anchor="middle" {T9} font-size="22" fill="{PAS_K}">GRUPTA AŞAĞI: ARTAR</text>'
    yb = y0 + 4 * ch + 26
    s += _ok(x0 + 7 * cw - 10, yb, x0 + 10, yb, PAS, 7, 22)
    s += f'<text x="{x0 + 3.5 * cw}" y="{yb + 34}" text-anchor="middle" {T9} font-size="22" fill="{PAS_K}">SOLA DOĞRU (PERİYOTTA SAĞA AZALIR)</text>'
    s += f'<text x="{W - 16}" y="{H - 14}" text-anchor="end" {T} font-size="18" fill="{GUM_K}">pm · yaklaşık</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info yt")


# ================================================================== 2. DURAK · atomdan iyona

def _katmanli(s, cx, cy, R, n_kat, renk, kesik_son=False):
    o = []
    g = s.rad([(0, renk, .32), (1, renk, .1)], ad="kb")
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R)}" fill="{g}"/>')
    for i in range(n_kat):
        rr = R * (i + 1) / n_kat
        k = ' stroke-dasharray="8 6"' if (kesik_son and i == n_kat - 1) else ""
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr)}" fill="none" stroke="{renk}" stroke-width="3"{k}/>')
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="8" fill="{koyu(renk, .2)}"/>')
    return "".join(o)


def iyon_donusum(onek="m2-id"):
    """Na → Na⁺ (bir katman gider: 186 → 102 pm) · Cl → Cl⁻ (katman aynı, p/e azalır: 99 → 181 pm)."""
    s = Svg(onek)
    W, H = 920, 300
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    k = .5
    r = VERI["r"]
    ri = VERI["ri"]
    yy = 128
    parcalar = [(108, r["Na"], 3, GOL, "Na", "11p · 11e · 2-8-1", f'{r["Na"]} pm'),
                (330, ri["Na+"], 2, GOL, "Na^{+}", "11p · 10e · 2-8", f'{ri["Na+"]} pm'),
                (568, r["Cl"], 3, MER, "Cl", "17p · 17e · 2-8-7", f'{r["Cl"]} pm'),
                (800, ri["Cl-"], 3, MER, "Cl^{−}", "17p · 18e · 2-8-8", f'{ri["Cl-"]} pm')]
    for cx, rpm, n, renk, ad, alt, deger in parcalar:
        s += _katmanli(s, cx, yy, rpm * k, n, renk)
        s += _alt(ad, cx, 254, 30, renk=OBS)
        s += f'<text x="{cx}" y="{282}" text-anchor="middle" {T} font-size="18" fill="{GUM_K}">{alt} · {deger}</text>'
    s += _ok(212, yy, 270, yy, OBS, 4, 15)
    s += _alt("−1 e^{−}", 240, yy - 18, 22, renk=OBS, font=T)
    s += f'<path d="M449 18 V282" stroke="{GUM}" stroke-width="2.4" stroke-dasharray="6 6"/>'
    s += _ok(626, yy, 702, yy, OBS, 4, 15)
    s += _alt("+1 e^{−}", 664, yy - 18, 22, renk=OBS, font=T)
    s += f'<text x="225" y="30" text-anchor="middle" {T9} font-size="19" fill="{GOL_K}">KATMAN GİDER, KÜÇÜLÜR</text>'
    s += f'<text x="690" y="30" text-anchor="middle" {T9} font-size="19" fill="{MER_K}">ELEKTRON GELİR, BÜYÜR</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info id")


def izoelektronik(onek="m2-iz"):
    """10 elektronlu altı tanecik: proton arttıkça tanecik küçülür (yarıçap ölçekli)."""
    s = Svg(onek)
    W, H = 920, 300
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    seri = [("N", "3−", 7, "N3-"), ("O", "2−", 8, "O2-"), ("F", "−", 9, "F-"), ("Na", "+", 11, "Na+"), ("Mg", "2+", 12, "Mg2+"), ("Al", "3+", 13, "Al3+")]
    k = .5
    toplam = sum(2 * VERI["ri"][a] * k for *_, a in seri) + 5 * 30
    x = (W - toplam) / 2
    for sym, q, p, anah in seri:
        R = VERI["ri"][anah] * k
        cx = x + R
        x += 2 * R + 30
        an = q.endswith("−")
        renk = MER if an else GOL
        g = s.rad([(0, acik(renk, .55)), (1, acik(renk, .15))], .35, .3, .8, ad="iz")
        s += f'<circle cx="{f(cx)}" cy="148" r="{f(R)}" fill="{g}" stroke="{koyu(renk, .25)}" stroke-width="3"/>'
        s += _alt(f"{sym}^{{{q}}}", cx, 158, 30 if R > 30 else 24)
        s += f'<text x="{f(cx)}" y="250" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">p = {p}</text>'
        s += f'<text x="{f(cx)}" y="278" text-anchor="middle" {B} font-size="24" fill="{OBS}">{VERI["ri"][anah]} pm</text>'
    s += f'<text x="{W / 2}" y="40" text-anchor="middle" {T9} font-size="21" fill="{KOB_K}">HEPSİ 10 ELEKTRON (2-8) · PROTON ARTTIKÇA KÜÇÜLÜR</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info iz")


def kromit(onek="m2-kr"):
    """Kromit kristali (temsilî, düzlem kesit): büyük O²⁻ iyonları sık dizilir; küçük Fe²⁺ ve Cr³⁺ boşluklara yerleşir."""
    s = Svg(onek)
    W, H = 440, 330
    g = s.lin([(0, "#2E3A33"), (1, "#151B18")], 0, 0, 0, 1, ad="zm")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{g}"/>'
    s += f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="12" fill="none" stroke="#5E7A66" stroke-width="2" stroke-dasharray="6 6"/>'
    R = 34
    oks = s.rad([(0, "#FFFFFF"), (.6, "#E3E8EC"), (1, "#AAB6BF")], .35, .3, .8, ad="ok")
    noktalar = []
    for j in range(4):
        for i in range(6):
            x = 52 + i * 2 * R + (R if j % 2 else 0)
            y = 70 + j * R * 1.732
            if x < W - 30:
                noktalar.append((x, y))
    for x, y in noktalar:
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{R - 1}" fill="{oks}" stroke="#7E8C96" stroke-width="2"/>'
    r = RNG(552)
    bos = []
    for j in range(3):
        for i in range(5):
            x = 52 + R + i * 2 * R + (R if j % 2 else 0) - (R if j % 2 else 0)
            y = 70 + j * R * 1.732 + R * .577
            bos.append((x + (R if j % 2 else 0) - R, y))
    for k, (x, y) in enumerate(bos):
        if not (40 < x < W - 40):
            continue
        cr = k % 3 != 1
        c = "#3FBF6A" if cr else KEH
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{11 if cr else 13}" fill="{c}" stroke="#0E1A12" stroke-width="2"/>'
    s += f'<rect x="18" y="{H - 58}" width="{W - 36}" height="44" rx="10" fill="#FFFFFF" opacity=".92"/>'
    s += f'<circle cx="44" cy="{H - 36}" r="13" fill="#E3E8EC" stroke="#7E8C96" stroke-width="2"/>'
    s += _alt("O^{2−}", 82, H - 28, 21, font=T)
    s += f'<circle cx="138" cy="{H - 36}" r="10" fill="{KEH}" stroke="#0E1A12" stroke-width="2"/>'
    s += _alt("Fe^{2+}", 178, H - 28, 21, font=T)
    s += f'<circle cx="236" cy="{H - 36}" r="9" fill="#3FBF6A" stroke="#0E1A12" stroke-width="2"/>'
    s += _alt("Cr^{3+}", 276, H - 28, 21, font=T)
    s += f'<text x="{W - 30}" y="{H - 28}" text-anchor="end" {T} font-size="17" fill="{GUM_K}">temsilî</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info kr")


# ================================================================== 3. DURAK · İE₁ grafiği (Z = 1–20)

IE_SIRA = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca"]


def ie1_grafik(onek="m2-ie"):
    s = Svg(onek)
    W, H = 1000, 560
    x0, x1, y0, y1 = 96, 980, 470, 40
    vmax = 2500
    X = lambda z: x0 + (z - .5) * (x1 - x0) / 20.2
    Y = lambda v: y0 - v / vmax * (y0 - y1)
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for a, b, et, c in ((.6, 2.4, "1.", "#E8F4F4"), (2.6, 10.4, "2. periyot", "#FFF2E2"), (10.6, 18.4, "3. periyot", "#E9EEFB"), (18.6, 20.4, "4.", "#F3E8F3")):
        s += f'<rect x="{f(X(a))}" y="{y1}" width="{f(X(b) - X(a))}" height="{y0 - y1}" rx="8" fill="{c}"/>'
        s += f'<text x="{f((X(a) + X(b)) / 2)}" y="{y1 + 26}" text-anchor="middle" {T9} font-size="20" fill="{GUM_K}">{et}</text>'
    for v in range(0, 2501, 500):
        s += f'<path d="M{x0} {f(Y(v))} H{x1}" stroke="#DCE4E8" stroke-width="2"/>'
        s += f'<text x="{x0 - 10}" y="{f(Y(v) + 8)}" text-anchor="end" {T} font-size="21" fill="{OBS}">{v}</text>'
    s += f'<path d="M{x0} {y1 - 10} V{y0} H{x1}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    pts = [(X(z), Y(VERI["ie1"][sym])) for z, sym in enumerate(IE_SIRA, 1)]
    s += f'<path d="{cizgi_d(pts)}" fill="none" stroke="{KOB}" stroke-width="5" stroke-linejoin="round"/>'
    for za, zb in ((4, 5), (7, 8), (12, 13), (15, 16)):
        (a, b), (c, d) = pts[za - 1], pts[zb - 1]
        s += f'<path d="M{f(a)} {f(b)} L{f(c)} {f(d)}" stroke="{KEH}" stroke-width="13" stroke-linecap="round" opacity=".85"/>'
    asagi = {"Li", "Na", "K", "B", "Al", "O", "S", "Ca"}
    for (a, b), sym in zip(pts, IE_SIRA):
        soy = sym in ("He", "Ne", "Ar")
        s += f'<circle cx="{f(a)}" cy="{f(b)}" r="{9 if soy else 7}" fill="{MER_K if soy else KOB}" stroke="#FFFFFF" stroke-width="2.5"/>'
        dy = 30 if sym in asagi else -15
        s += f'<text x="{f(a)}" y="{f(b + dy)}" text-anchor="middle" {B} font-size="23" fill="{OBS}">{sym}</text>'
    for z in range(1, 21):
        s += f'<text x="{f(X(z))}" y="{y0 + 28}" text-anchor="middle" {T} font-size="18" fill="{GUM_K}">{z}</text>'
    s += f'<text x="{(x0 + x1) / 2}" y="{y0 + 60}" text-anchor="middle" {T9} font-size="21" fill="{OBS}">atom numarası (Z)</text>'
    s += _alt("İE_1 (kJ/mol)", 18, 30, 24, anchor="start", font=T9)
    bx, by = 620, 92
    s += f'<rect x="{bx}" y="{by}" width="340" height="66" rx="12" fill="#FFFFFF" stroke="{KEH}" stroke-width="3"/>'
    s += f'<path d="M{bx + 18} {by + 24} H{bx + 58}" stroke="{KEH}" stroke-width="13" stroke-linecap="round"/>'
    s += f'<text x="{bx + 72}" y="{by + 31}" {T} font-size="20" fill="{OBS}">genel artışa aykırı düşüş</text>'
    s += f'<text x="{bx + 18}" y="{by + 56}" {T} font-size="19" fill="{GUM_K}">2A’dan 3A’ya ve 5A’dan 6A’ya</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ie")


# ================================================================== 4. DURAK · karbonun ardışık İE'leri (kırık eksen)

def karbon_ie(onek="m2-ci"):
    s = Svg(onek)
    W, H = 600, 440
    x0, y0, yt = 92, 352, 70
    vmax = 7000
    Y = lambda v: y0 - v / vmax * (y0 - yt)
    v = VERI["ie"]["C"]
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for t in range(0, 7001, 2000):
        s += f'<path d="M{x0} {f(Y(t))} H{W - 20}" stroke="#DCE4E8" stroke-width="2"/>'
        s += f'<text x="{x0 - 10}" y="{f(Y(t) + 7)}" text-anchor="end" {T} font-size="19" fill="{OBS}">{t}</text>'
    s += f'<path d="M{x0} {yt - 30} V{y0} H{W - 20}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    bw, ara = 62, 32
    for i, val in enumerate(v):
        x = x0 + 26 + i * (bw + ara)
        if i < 4:
            g = s.lin([(0, "#6FD3D2"), (1, GOL_K)], 0, 0, 0, 1, ad="cb")
            s += f'<rect x="{x}" y="{f(Y(val))}" width="{bw}" height="{f(y0 - Y(val))}" rx="6" fill="{g}" stroke="{OBS}" stroke-width="2.4"/>'
            s += f'<text x="{x + bw / 2}" y="{f(Y(val) - 10)}" text-anchor="middle" {B} font-size="22" fill="{OBS}">{_bin(val)}</text>'
        else:
            g = s.lin([(0, "#FFB59F"), (1, MER_K)], 0, 0, 0, 1, ad="cs")
            top = yt - 34
            s += f'<rect x="{x}" y="{top}" width="{bw}" height="{y0 - top}" rx="6" fill="{g}" stroke="{OBS}" stroke-width="2.4"/>'
            s += f'<path d="M{x - 8} {top + 84} l{bw + 16} -18 M{x - 8} {top + 100} l{bw + 16} -18" stroke="#FFFFFF" stroke-width="9"/>'
            s += f'<path d="M{x - 8} {top + 84} l{bw + 16} -18 M{x - 8} {top + 100} l{bw + 16} -18" stroke="{OBS}" stroke-width="2.4"/>'
            s += halolu_yazi(f'x="{x + bw / 2}" y="{top + 150}" text-anchor="middle" {B} font-size="23"', _bin(val), "#FFFFFF", MER_K, 1.6)
        s += _alt(f"İE_{i + 1}", x + bw / 2, y0 + 30, 22, font=T)
        if i:
            oran = v[i] / v[i - 1]
            xm = x - ara / 2
            renk = MER_K if oran >= 3 else GUM_K
            s += f'<text x="{f(xm)}" y="{f(Y(min(v[i - 1], 6400)) - 46)}" text-anchor="middle" {B} font-size="{26 if oran >= 3 else 20}" fill="{renk}">×{_vir(oran)}</text>'
    s += f'<text x="{W / 2 + 20}" y="{H - 22}" text-anchor="middle" {T9} font-size="19" fill="{MER_K}">4 ELEKTRON GÖRECE KOLAY · 5.Sİ İÇ KATMANDAN: 4A</text>'
    s += f'<text x="20" y="34" {T9} font-size="20" fill="{OBS}">kJ/mol · ₆C (2-4)</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ci")


# ================================================================== 5. DURAK · elektronegatiflik ısı haritası

def _en_renk(v):
    t = (v - .8) / (4.0 - .8)
    if t < .5:
        return karis("#DFF4F2", "#F6C26B", t / .5)
    return karis("#F6C26B", MER_K, (t - .5) / .5)


def en_tablosu(onek="m2-en"):
    s = Svg(onek)
    W, H = 940, 500
    x0, y0, cw, ch = 70, 50, 104, 86
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for g in range(8):
        s += f'<text x="{x0 + g * cw + cw / 2}" y="{y0 - 14}" text-anchor="middle" {B} font-size="26" fill="{KOB_K}">{g + 1}A</text>'
    for p in range(4):
        s += f'<text x="{x0 - 28}" y="{y0 + p * ch + ch / 2 + 9}" text-anchor="middle" {B} font-size="27" fill="{KOB_K}">{p + 1}</text>'
        for g in range(8):
            sym = TABLO[p][g]
            x, y = x0 + g * cw, y0 + p * ch
            if not sym:
                continue
            if SINIF.get(sym) == "soy":
                s += f'<rect x="{x + 4}" y="{y + 4}" width="{cw - 8}" height="{ch - 8}" rx="10" fill="#FFFFFF" stroke="#B8C3CC" stroke-width="2.4" stroke-dasharray="7 6"/>'
                s += f'<text x="{x + cw / 2}" y="{y + 38}" text-anchor="middle" {B} font-size="28" fill="{GUM_K}">{sym}</text>'
                s += f'<text x="{x + cw / 2}" y="{y + 68}" text-anchor="middle" {T} font-size="22" fill="{GUM_K}">—</text>'
                continue
            if sym not in VERI["en"]:
                s += f'<rect x="{x + 4}" y="{y + 4}" width="{cw - 8}" height="{ch - 8}" rx="10" fill="#F4F6F8" stroke="#DCE2E6" stroke-width="2"/>'
                s += f'<text x="{x + cw / 2}" y="{y + 52}" text-anchor="middle" {B} font-size="24" fill="#B8C3CC">{sym}</text>'
                continue
            v = VERI["en"][sym]
            yazi = "#FFFFFF" if v >= 2.6 else OBS
            s += f'<rect x="{x + 4}" y="{y + 4}" width="{cw - 8}" height="{ch - 8}" rx="10" fill="{_en_renk(v)}" stroke="{OBS}" stroke-width="2"/>'
            s += f'<text x="{x + cw / 2}" y="{y + 38}" text-anchor="middle" {B} font-size="29" fill="{yazi}">{sym}</text>'
            s += f'<text x="{x + cw / 2}" y="{y + 68}" text-anchor="middle" {T} font-size="23" fill="{yazi}">{_vir(v)}</text>'
    yy = y0 + 4 * ch + 26
    for i in range(48):
        s += f'<rect x="{f(190 + i * 11)}" y="{yy}" width="11.6" height="20" fill="{_en_renk(.8 + 3.2 * i / 47)}"/>'
    s += f'<rect x="190" y="{yy}" width="528" height="20" fill="none" stroke="{OBS}" stroke-width="2"/>'
    s += f'<text x="178" y="{yy + 17}" text-anchor="end" {T} font-size="20" fill="{GUM_K}">düşük</text>'
    s += f'<text x="730" y="{yy + 17}" {T} font-size="20" fill="{GUM_K}">yüksek</text>'
    s += f'<text x="{W / 2}" y="{yy + 52}" text-anchor="middle" {T9} font-size="19" fill="{KOB_K}">PAULING ÖLÇEĞİ (F = 4,0) · BİRİMSİZ · SOY GAZLARA DEĞER VERİLMEZ</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info en")


def halat(onek="m2-ht"):
    """Su molekülündeki O–H bağı bir halat çekme: bağ elektronları O'ya kayar (δ⁻ O, δ⁺ H)."""
    s = Svg(onek)
    W, H = 600, 300
    g = s.lin([(0, "#E6F6FA"), (1, "#BFE6EE")], 0, 0, 0, 1, ad="zm")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{g}"/>'
    s += f'<path d="M0 232 C150 222 300 240 600 226 V282 Q600 300 582 300 H18 Q0 300 0 282 Z" fill="#7FC9D8" opacity=".55"/>'
    # halat
    s += f'<path d="M150 140 C250 150 330 132 450 140" stroke="#8C6A3A" stroke-width="16" fill="none" stroke-linecap="round"/>'
    for k in range(17):
        x = 158 + k * 17.5
        s += f'<path d="M{f(x)} 131 l9 18" stroke="#5E4422" stroke-width="2.6"/>'
    # bağ elektron çifti (düğüm), O'ya yakın
    s += f'<circle cx="374" cy="139" r="22" fill="{KEH}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<circle cx="366" cy="139" r="5" fill="{OBS}"/><circle cx="382" cy="139" r="5" fill="{OBS}"/>'
    s += f'<path d="M300 186 V200 M300 193 H374 M374 186 V200" stroke="{GUM_K}" stroke-width="2.4" fill="none"/>'
    s += f'<text x="337" y="222" text-anchor="middle" {T} font-size="18" fill="{GUM_K}">orta</text>'
    # atomlar
    hg = s.rad([(0, "#FFFFFF"), (1, "#D9E1E7")], .35, .3, .8, ad="hh")
    og = s.rad([(0, "#FF9C86"), (1, MER_K)], .35, .3, .8, ad="oo")
    s += f'<circle cx="112" cy="140" r="44" fill="{hg}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<text x="112" y="152" text-anchor="middle" {B} font-size="38" fill="{OBS}">H</text>'
    s += f'<circle cx="500" cy="140" r="64" fill="{og}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<text x="500" y="154" text-anchor="middle" {B} font-size="44" fill="#FFFFFF">O</text>'
    s += f'<text x="112" y="74" text-anchor="middle" {DJ} font-size="32" fill="{GOL_K}">δ+</text>'
    s += f'<text x="500" y="60" text-anchor="middle" {DJ} font-size="32" fill="{MER_K}">δ−</text>'
    s += f'<text x="112" y="214" text-anchor="middle" {T} font-size="21" fill="{OBS}">EN 2,2</text>'
    s += f'<text x="500" y="234" text-anchor="middle" {T} font-size="21" fill="#FFFFFF">EN 3,4</text>'
    s += f'<text x="300" y="{H - 16}" text-anchor="middle" {T9} font-size="18" fill="{DERIN}">FARK 1,2 · BAĞ ELEKTRONLARI O’YA KAYAR</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ht")


# ================================================================== 6. DURAK · metalik / ametalik karakter haritası

SINIF_RENK = {"metal": ("#CFE3F7", "#3A6EA8"), "yari": ("#E3D6F4", "#6B4BA0"), "ametal": ("#FFE0C2", "#B5541A"),
              "soy": ("#E6EEF1", "#586874"), "belirsiz": ("#EEEEEE", "#8A8A8A")}


def ozellik_haritasi(onek="m2-oh"):
    """Baş gruplar (1–6. periyot): sınıf renkleri kitabın tablosundaki gibi; oklar eğilimleri gösterir."""
    s = Svg(onek)
    W, H = 940, 640
    x0, y0, cw, ch = 96, 92, 88, 68
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    # üst ok: periyotta sağa
    s += _ok(x0 + 6, 42, x0 + 8 * cw - 6, 42, MER, 7, 22)
    s += f'<text x="{x0 + 4 * cw}" y="30" text-anchor="middle" {T9} font-size="19" fill="{MER_K}">İE₁ · ELEKTRONEGATİFLİK · AMETALİK KARAKTER ARTAR</text>'
    s += _ok(x0 + 8 * cw - 6, y0 + 6 * ch + 28, x0 + 6, y0 + 6 * ch + 28, KOB, 7, 22)
    s += f'<text x="{x0 + 4 * cw}" y="{y0 + 6 * ch + 64}" text-anchor="middle" {T9} font-size="19" fill="{KOB_K}">ATOM YARIÇAPI · METALİK KARAKTER ARTAR</text>'
    s += _ok(x0 - 52, y0 + 6, x0 - 52, y0 + 6 * ch - 6, KOB, 7, 22)
    s += f'<text transform="translate({x0 - 72} {y0 + 3 * ch}) rotate(-90)" text-anchor="middle" {T9} font-size="18" fill="{KOB_K}">YARIÇAP · METALİK ARTAR</text>'
    s += _ok(x0 + 8 * cw + 34, y0 + 6 * ch - 6, x0 + 8 * cw + 34, y0 + 6, MER, 7, 22)
    s += f'<text transform="translate({x0 + 8 * cw + 56} {y0 + 3 * ch}) rotate(90)" text-anchor="middle" {T9} font-size="18" fill="{MER_K}">İE₁ · EN · AMETALİK ARTAR</text>'
    for g in range(8):
        s += f'<text x="{x0 + g * cw + cw / 2}" y="{y0 - 10}" text-anchor="middle" {B} font-size="22" fill="{OBS}">{g + 1}A</text>'
    for p in range(6):
        for g in range(8):
            sym = TABLO[p][g]
            if not sym:
                continue
            x, y = x0 + g * cw, y0 + p * ch
            zm, cz = SINIF_RENK[SINIF[sym]]
            s += f'<rect x="{x + 3}" y="{y + 3}" width="{cw - 6}" height="{ch - 6}" rx="9" fill="{zm}" stroke="{cz}" stroke-width="2.2"/>'
            s += f'<text x="{x + cw / 2}" y="{y + ch / 2 + 10}" text-anchor="middle" {B} font-size="28" fill="{koyu(cz, .25)}">{sym}</text>'
    # vurgular: Cs (en metalik bölge) ve F (en ametalik)
    xc, yc = x0 + cw / 2, y0 + 5 * ch + ch / 2
    s += f'<circle cx="{xc}" cy="{yc}" r="40" fill="none" stroke="{KOB}" stroke-width="5"/>'
    xf, yf = x0 + 6 * cw + cw / 2, y0 + ch + ch / 2
    s += f'<circle cx="{xf}" cy="{yf}" r="40" fill="none" stroke="{MER}" stroke-width="5"/>'
    # Keban: kurşun
    xp, yp = x0 + 3 * cw, y0 + 5 * ch
    s += f'<path d="{cizgi_d(selcuklu_yildizi(xp + cw - 12, yp + 12, 13), True)}" fill="{KEH}" stroke="{OBS}" stroke-width="2"/>'
    ly = y0 + 6 * ch + 86
    for k, (ad, sin) in enumerate((("metal", "metal"), ("yarı metal", "yari"), ("ametal", "ametal"), ("soy gaz", "soy"), ("sınıfı değişen", "belirsiz"))):
        lx = 40 + k * 178
        zm, cz = SINIF_RENK[sin]
        s += f'<rect x="{lx}" y="{ly}" width="30" height="24" rx="6" fill="{zm}" stroke="{cz}" stroke-width="2.2"/>'
        s += f'<text x="{lx + 38}" y="{ly + 20}" {T} font-size="20" fill="{OBS}">{ad}</text>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(W - 236, ly - 34, 11), True)}" fill="{KEH}" stroke="{OBS}" stroke-width="2"/>'
    s += f'<text x="{W - 220}" y="{ly - 27}" {T} font-size="19" fill="{OBS}">Keban: gümüşlü kurşun</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info oh")


# ================================================================== KISSA 3 · alkali metallerin İE₁'i

def alkali_ie(onek="m2-al"):
    s = Svg(onek)
    W, H = 520, 330
    x0, y0, yt = 80, 262, 46
    Y = lambda v: y0 - v / 600 * (y0 - yt)
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for t in range(0, 601, 200):
        s += f'<path d="M{x0} {f(Y(t))} H{W - 16}" stroke="#DCE4E8" stroke-width="2"/>'
        s += f'<text x="{x0 - 10}" y="{f(Y(t) + 7)}" text-anchor="end" {T} font-size="20" fill="{OBS}">{t}</text>'
    s += f'<path d="M{x0} {yt - 16} V{y0} H{W - 16}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    for i, sym in enumerate(("Li", "Na", "K", "Rb", "Cs")):
        v = VERI["ie1"][sym]
        x = x0 + 24 + i * 82
        c = karis("#9FDCDB", GOL_K, i / 4)
        s += f'<rect x="{x}" y="{f(Y(v))}" width="52" height="{f(y0 - Y(v))}" rx="6" fill="{c}" stroke="{OBS}" stroke-width="2.2"/>'
        s += f'<text x="{x + 26}" y="{f(Y(v) - 8)}" text-anchor="middle" {B} font-size="22" fill="{OBS}">{v}</text>'
        s += f'<text x="{x + 26}" y="{y0 + 30}" text-anchor="middle" {B} font-size="25" fill="{OBS}">{sym}</text>'
    s += _alt("İE_1 (kJ/mol)", 16, 30, 21, anchor="start", font=T9)
    s += f'<text x="{W - 16}" y="{H - 10}" text-anchor="end" {T} font-size="18" fill="{GUM_K}">1A grubu, yukarıdan aşağı</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik al")


# ================================================================== İMTİHAN 11 · ardışık beş element (P S Cl Ar K)

TEST5 = [("X", "P"), ("Y", "S"), ("Z", "Cl"), ("T", "Ar"), ("Q", "K")]


def test5_grafik(onek="m2-t5"):
    s = Svg(onek)
    W, H = 470, 310
    x0, y0, yt = 60, 250, 40
    Y = lambda v: y0 - v / 1700 * (y0 - yt)
    s += f'<rect width="{W}" height="{H}" rx="16" fill="#FFFFFF"/>'
    s += f'<path d="M{x0} {yt - 10} V{y0} H{W - 14}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    pts = []
    for i, (h, sym) in enumerate(TEST5):
        v = VERI["ie1"][sym]
        x = x0 + 50 + i * 82
        pts.append((x, Y(v)))
        s += f'<path d="M{x} {y0} V{f(Y(v))}" stroke="#DCE4E8" stroke-width="2.4" stroke-dasharray="6 5"/>'
        s += f'<text x="{x}" y="{y0 + 32}" text-anchor="middle" {B} font-size="28" fill="{OBS}">{h}</text>'
    s += f'<path d="{cizgi_d(pts)}" fill="none" stroke="{KOB}" stroke-width="4.5"/>'
    for (x, y), (h, sym) in zip(pts, TEST5):
        v = VERI["ie1"][sym]
        s += f'<circle cx="{x}" cy="{f(y)}" r="7" fill="{KOB}" stroke="#FFFFFF" stroke-width="2"/>'
        if v < 600:
            s += f'<text x="{x - 14}" y="{f(y + 7)}" text-anchor="end" {B} font-size="22" fill="{KOB_K}">{v}</text>'
        else:
            s += f'<text x="{x}" y="{f(y - 14)}" text-anchor="middle" {B} font-size="22" fill="{KOB_K}">{v}</text>'
    s += _alt("İE_1", 14, 28, 21, anchor="start", font=T9)
    s += f'<text x="{W - 14}" y="{H - 8}" text-anchor="end" {T} font-size="17" fill="{GUM_K}">atom numarası ardışık</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik t5")


# ================================================================== İMTİHAN 12 · periyodik tablo kesiti

KESIT = {"X": (2, 1), "Y": (2, 5), "Z": (2, 7), "T": (3, 1), "Q": (3, 6)}


def tablo_kesit(onek="m2-tk"):
    s = Svg(onek)
    W, H = 480, 230
    x0, y0, cw, ch = 50, 50, 52, 72
    s += f'<rect width="{W}" height="{H}" rx="16" fill="#FFFFFF"/>'
    for g in range(8):
        s += f'<text x="{x0 + g * cw + cw / 2}" y="{y0 - 12}" text-anchor="middle" {B} font-size="20" fill="{GUM_K}">{g + 1}A</text>'
    for p in range(2):
        s += f'<text x="{x0 - 22}" y="{y0 + p * ch + ch / 2 + 8}" text-anchor="middle" {B} font-size="22" fill="{GUM_K}">{p + 2}</text>'
        for g in range(8):
            x, y = x0 + g * cw, y0 + p * ch
            harf = next((h for h, (pp, gg) in KESIT.items() if pp == p + 2 and gg == g + 1), "")
            s += f'<rect x="{x + 2}" y="{y + 2}" width="{cw - 4}" height="{ch - 4}" rx="6" fill="{KOB_A if harf else "#FFFFFF"}" stroke="{OBS}" stroke-width="2"/>'
            if harf:
                s += f'<text x="{x + cw / 2}" y="{y + ch / 2 + 11}" text-anchor="middle" {B} font-size="30" fill="{KOB_K}">{harf}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik tk")


# ================================================================== ÜSTAD 2 · sekiz ardışık elementin İE₁'i

USTAD8 = ["N", "O", "F", "Ne", "Na", "Mg", "Al", "Si"]


def ustad_ie_grafik(onek="m2-u8"):
    s = Svg(onek)
    W, H = 520, 340
    x0, y0, yt = 70, 270, 40
    Y = lambda v: y0 - v / 2200 * (y0 - yt)
    s += f'<rect width="{W}" height="{H}" rx="16" fill="#FFFFFF"/>'
    for t in range(0, 2201, 500):
        s += f'<path d="M{x0} {f(Y(t))} H{W - 14}" stroke="#E4EAEE" stroke-width="2"/>'
        s += f'<text x="{x0 - 8}" y="{f(Y(t) + 7)}" text-anchor="end" {T} font-size="18" fill="{OBS}">{t}</text>'
    s += f'<path d="M{x0} {yt - 12} V{y0} H{W - 14}" stroke="{OBS}" stroke-width="3.6" fill="none"/>'
    pts = []
    for i, sym in enumerate(USTAD8):
        x = x0 + 34 + i * 55
        pts.append((x, Y(VERI["ie1"][sym])))
        s += f'<text x="{x}" y="{y0 + 28}" text-anchor="middle" {B} font-size="24" fill="{LAJVER}">{i + 1}</text>'
    s += f'<path d="{cizgi_d(pts)}" fill="none" stroke="{LAJVER}" stroke-width="4"/>'
    for (x, y), sym in zip(pts, USTAD8):
        s += f'<circle cx="{x}" cy="{f(y)}" r="7" fill="{ALTIN}" stroke="{LAJVER}" stroke-width="2.4"/>'
    s += _alt("İE_1 (kJ/mol)", 12, 26, 19, anchor="start", font=T9)
    s += f'<text x="{W - 14}" y="{H - 10}" text-anchor="end" {T} font-size="17" fill="{GUM_K}">atom numaraları ardışık</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ustad-graf u8")


# ================================================================== MEDENİYETİMİZDEN · Divriği Darüşşifası (temsilî)

def darussifa(onek="m2-ds"):
    """Selçuklu taç kapısı esinli temsilî çizim: sivri kemer, yıldız geçmeli bordür, 1228 yazısı. Belirli bir cephe değildir."""
    s = Svg(onek)
    W, H = 300, 380
    g = s.lin([(0, "#F7E9D2"), (1, "#E6C9A3")], 0, 0, 0, 1, ad="ts")
    s += f'<rect width="{W}" height="{H}" rx="16" fill="#FFF7E6"/>'
    s += f'<rect x="30" y="40" width="240" height="310" rx="6" fill="{g}" stroke="{ALTIN_K}" stroke-width="4"/>'
    # bordür: tekrarlanan sekiz köşeli yıldızlar
    d = []
    for k in range(9):
        for x in (48, 252):
            d.append(cizgi_d(selcuklu_yildizi(x, 64 + k * 34, 12), True))
    for k in range(6):
        d.append(cizgi_d(selcuklu_yildizi(82 + k * 27.2, 60, 10), True))
    s += f'<path d="{" ".join(d)}" fill="{ALTIN_A}" stroke="{ALTIN_K}" stroke-width="2"/>'
    # sivri kemerli niş + mukarnas izleri
    s += f'<path d="M84 350 V170 Q84 92 150 78 Q216 92 216 170 V350 Z" fill="#C99C6E" stroke="{ALTIN_K}" stroke-width="4"/>'
    for k in range(4):
        y = 104 + k * 22
        w = 40 + k * 22
        s += f'<path d="M{150 - w} {y + 20} Q{150 - w / 2} {y} 150 {y + 8} Q{150 + w / 2} {y} {150 + w} {y + 20}" fill="none" stroke="#8A6242" stroke-width="3"/>'
    s += f'<path d="M108 350 V214 Q108 176 150 168 Q192 176 192 214 V350 Z" fill="#5A3A26"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(150, 266, 30), True)}" fill="{ALTIN}" stroke="#F6E7BF" stroke-width="3"/>'
    s += f'<circle cx="150" cy="266" r="10" fill="{GOL}"/>'
    s += f'<text x="150" y="32" text-anchor="middle" {B} font-size="28" fill="{ALTIN_K}">1228</text>'
    s += f'<text x="150" y="374" text-anchor="middle" {T} font-size="17" fill="{GUM_K}">temsilî</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ds")
