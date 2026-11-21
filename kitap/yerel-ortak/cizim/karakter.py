"""Karakterler: Pamuk (Van kedisi; bir gözü mavi, bir gözü kehribar), Elif, Yusuf, Zeynep Hoca.

Her karakter tek bir baş çizimi + ifade parametreleri + poz (gövde/kol) parçalarından kurulur;
bu yüzden her pozda yüz, renk ve kıyafet AYNI kalır (tutarlılık).

`semboller()` bütün pozları <symbol> olarak verir; sayfada bir kez gizli <svg><defs> içine konur,
sonra her yerde <svg viewBox=".."><use href="#pamuk-selam"/></svg> ile çağrılır.

Sembol kimlikleri (viewBox):
  Pamuk  : pamuk-selam, pamuk-dusunen, pamuk-sasiran, pamuk-akce, pamuk-kitap, pamuk-otur (0 0 140 160),
           pamuk-bayrak (0 -40 170 200)
           pamuk-yuzer (0 0 120 80), av-pamuk (0 0 40 40)
  Elif   : elif-soru, elif-dusunen, elif-aha (0 0 200 210), av-elif
  Yusuf  : yusuf-anlatan, yusuf-defter, yusuf-gulen (0 0 200 210), av-yusuf
  Zeynep : zeynep-anlatan, zeynep-kitap (0 0 200 210), av-zeynep
"""
from .temel import Svg, f, halolu_yazi
from .renkler import OBS, GOL, GOL_K, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ALTIN, ALTIN_A, LAJVER, MAVI

CZ = OBS          # çizgi rengi
K = 2.2           # çizgi kalınlığı (100 birimlik baş için)

# ------------------------------------------------------------------ PAMUK

def _pamuk_goz(s, cx, cy, renk, koyu_renk, ifade, sag):
    if ifade == "gulen" or (ifade == "gozkirp" and sag):
        return f'<path d="M{f(cx - 7)} {f(cy + 2)} Q{f(cx)} {f(cy - 7)} {f(cx + 7)} {f(cy + 2)}" fill="none" stroke="{CZ}" stroke-width="2.6" stroke-linecap="round"/>'
    g = s.rad([(0, "#FFFFFF"), (.18, renk), (.8, renk), (1, koyu_renk)], cx=.45, cy=.4, r=.62, ad="pg")
    rx, ry = (8.4, 9.2) if ifade == "sasiran" else (7.6, 8.4)
    px, py = (cx + 1.6, cy - 2.6) if ifade == "dusunen" else (cx + .4, cy + .6)
    pr = (2.2, 2.6) if ifade == "sasiran" else (2.7, 5.2)
    return (f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{rx}" ry="{ry}" fill="{g}" stroke="{CZ}" stroke-width="1.9"/>'
            f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{pr[0]}" ry="{pr[1]}" fill="{CZ}"/>'
            f'<circle cx="{f(cx - 2.6)}" cy="{f(cy - 3.2)}" r="2.3" fill="#FFFFFF"/>'
            f'<circle cx="{f(cx + 2.6)}" cy="{f(cy + 3.4)}" r="1.1" fill="#FFFFFF" opacity=".9"/>')


def pamuk_bas(s, ifade="mutlu"):
    """100×86 kutuda baş (merkez ~50,48). ifade: mutlu, gulen, dusunen, sasiran, gozkirp."""
    kurk = s.rad([(0, "#FFFFFF"), (.62, "#FFFFFF"), (1, "#DCE5EE")], cx=.5, cy=.45, r=.62, ad="pk")
    kulak_ust = -3 if ifade == "sasiran" else 0
    o = []
    # kulaklar
    for sag in (False, True):
        m = (lambda x: 100 - x) if sag else (lambda x: x)
        o.append(f'<path d="M{f(m(20))} 40 C{f(m(15))} 27 {f(m(14))} {14 + kulak_ust} {f(m(17))} {4 + kulak_ust} C{f(m(27))} {8 + kulak_ust} {f(m(37))} 14 {f(m(43))} 22 Z" fill="{kurk}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                 f'<path d="M{f(m(23))} 33 C{f(m(21))} 25 {f(m(20.5))} {17 + kulak_ust} {f(m(22))} {11 + kulak_ust} C{f(m(28))} 14 {f(m(33))} 18 {f(m(37))} 23 Z" fill="#F6B3C1"/>'
                 f'<path d="M{f(m(24))} 27 l{f(3 if not sag else -3)} -6 M{f(m(26))} 30 l{f(4 if not sag else -4)} -5" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round"/>')
    # baş + yanak tüyleri
    o.append(f'<path d="M50 17 C71 17 85 28 87 44 C88.5 53 86.5 61 81 67 L86 70.5 L78.5 71.5 L81 76 L72.5 74.5 C66 78.5 58.5 80.5 50 80.5 '
             f'C41.5 80.5 34 78.5 27.5 74.5 L19 76 L21.5 71.5 L14 70.5 L19 67 C13.5 61 11.5 53 13 44 C15 28 29 17 50 17 Z" '
             f'fill="{kurk}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>')
    o.append('<path d="M44 19.5 L47 24 L50 19 L53 24 L56 19.5" fill="none" stroke="#C3CED8" stroke-width="1.5" stroke-linejoin="round"/>')
    # yanak pembesi
    o.append('<ellipse cx="27.5" cy="58.5" rx="5.6" ry="3.3" fill="#FBC3CD" opacity=".9"/><ellipse cx="72.5" cy="58.5" rx="5.6" ry="3.3" fill="#FBC3CD" opacity=".9"/>')
    # gözler: izleyicinin solundaki mavi, sağındaki kehribar
    o.append(_pamuk_goz(s, 36.5, 46, MAVI, "#1E5BB0", ifade, False))
    o.append(_pamuk_goz(s, 63.5, 46, KEH, "#A8650A", ifade, True))
    # burun + ağız
    o.append(f'<path d="M46.4 54.6 H53.6 L50 58.6 Z" fill="#F2879C" stroke="{CZ}" stroke-width="1.3" stroke-linejoin="round"/>')
    if ifade == "sasiran":
        o.append(f'<ellipse cx="50" cy="64.5" rx="3.2" ry="3.9" fill="#B43B57" stroke="{CZ}" stroke-width="1.5"/>')
    elif ifade in ("gulen", "gozkirp"):
        o.append(f'<path d="M43.5 60.5 Q50 70.5 56.5 60.5 Q50 63.5 43.5 60.5 Z" fill="#B43B57" stroke="{CZ}" stroke-width="1.5" stroke-linejoin="round"/>'
                 '<path d="M47 64.6 Q50 67.6 53 64.6 Q50 63.6 47 64.6 Z" fill="#F2879C"/>')
    elif ifade == "dusunen":
        o.append(f'<path d="M45.5 63 Q49 61.5 50 59 Q51.5 62.5 55.5 62" fill="none" stroke="{CZ}" stroke-width="1.7" stroke-linecap="round"/>')
    else:
        o.append(f'<path d="M50 58.6 Q48.6 62.6 45 61.2 M50 58.6 Q51.4 62.6 55 61.2" fill="none" stroke="{CZ}" stroke-width="1.7" stroke-linecap="round"/>')
    # bıyıklar
    o.append(f'<g stroke="{CZ}" stroke-width="1.1" stroke-linecap="round">'
             '<path d="M23 54 L8 51.5"/><path d="M23 57.5 L7.5 58.5"/><path d="M24 60.5 L10 64.5"/>'
             '<path d="M77 54 L92 51.5"/><path d="M77 57.5 L92.5 58.5"/><path d="M76 60.5 L90 64.5"/></g>')
    return "".join(o)


def _pamuk_govde(s, poz):
    kurk = s.lin([(0, "#FFFFFF"), (.55, "#F7FAFC"), (1, "#D3DEE8")], 0, 0, 1, .3, ad="pv")
    o = ['<ellipse cx="70" cy="149" rx="46" ry="5.5" fill="#0E2A3A" opacity=".16"/>']
    # kuyruk (arkada): kabarık, tüy uçlu
    if poz not in ("yuzer",):
        o.append(f'<path d="M100 144 C124 146 138 128 134 108 C132 96 124 88 116 90 C109 92 109 100 114 104 C121 110 121 124 110 130 C104 133 98 134 94 134 Z" '
                 f'fill="{kurk}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                 f'<path d="M124 100 l5 -3 M127 112 l6 -1 M125 124 l5 3 M116 134 l3 5" stroke="#C3CED8" stroke-width="1.5" stroke-linecap="round"/>')
    # gövde (armut)
    o.append(f'<path d="M45 82 C31 96 26 122 31 146 L109 146 C114 122 109 96 95 82 Z" fill="{kurk}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>')
    # gövdede tüy dokusu
    o.append('<path d="M38 112 q4 -2 6 2 M100 108 q-4 -2 -6 2 M36 128 q4 -2 6 2 M103 126 q-4 -2 -6 2" fill="none" stroke="#C3CED8" stroke-width="1.4" stroke-linecap="round"/>')
    # arka bacaklar (oturan kalça)
    o.append(f'<path d="M31 146 C21 146 18 129 27 122 C35 116 47 126 46 146 Z" fill="{kurk}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
             f'<path d="M109 146 C119 146 122 129 113 122 C105 116 93 126 94 146 Z" fill="{kurk}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
             f'<path d="M24 141 q3 -3 6 0 M110 141 q3 -3 6 0" fill="none" stroke="{CZ}" stroke-width="1.2" stroke-linecap="round"/>')
    # göğüs yelesi (kabarık)
    o.append('<path d="M46 84 C46 92 48 98 51 102 L55 97 L59 106 L63 99 L66 107 L70 99 L74 107 L77 99 L81 106 L85 97 L89 102 C92 98 94 92 94 84 Z" fill="#FFFFFF"/>'
             '<path d="M51 102 L55 97 L59 106 L63 99 L66 107 L70 99 L74 107 L77 99 L81 106 L85 97 L89 102" fill="none" stroke="#BFCAD5" stroke-width="1.5" stroke-linejoin="round"/>')
    return "".join(o)


def _pati(x, y, r=7.2, aci=0):
    return (f'<g transform="rotate({aci} {f(x)} {f(y)})"><ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r * 1.12)}" ry="{f(r)}" fill="#FFFFFF" stroke="{CZ}" stroke-width="{K}"/>'
            f'<path d="M{f(x - r * .45)} {f(y + r * .1)} v{f(-r * .5)} M{f(x)} {f(y)} v{f(-r * .6)} M{f(x + r * .45)} {f(y + r * .1)} v{f(-r * .5)}" stroke="{CZ}" stroke-width="1.2" stroke-linecap="round"/></g>')


def _on_bacak(x, ust=100, alt=146):
    return (f'<path d="M{f(x - 8.5)} {ust} C{f(x - 9.5)} {ust + 16} {f(x - 10)} {alt - 14} {f(x - 9.5)} {alt - 5} Q{f(x)} {alt + 3} {f(x + 9.5)} {alt - 5} '
            f'C{f(x + 10)} {alt - 14} {f(x + 9.5)} {ust + 16} {f(x + 8.5)} {ust}" fill="#FFFFFF" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
            f'<path d="M{f(x - 3.4)} {alt - 1.5} v-4.5 M{f(x + 3.4)} {alt - 1.5} v-4.5" stroke="{CZ}" stroke-width="1.3" stroke-linecap="round"/>')


def _kol(x0, y0, x1, y1, kx, ky):
    """Kalın tüylü kol: dış çizgi + beyaz iç."""
    return (f'<path d="M{f(x0)} {f(y0)} Q{f(kx)} {f(ky)} {f(x1)} {f(y1)}" fill="none" stroke="{CZ}" stroke-width="17" stroke-linecap="round"/>'
            f'<path d="M{f(x0)} {f(y0)} Q{f(kx)} {f(ky)} {f(x1)} {f(y1)}" fill="none" stroke="#FFFFFF" stroke-width="12.4" stroke-linecap="round"/>')


def _tasma(s):
    gm = s.rad([(0, "#FFFFFF"), (.5, "#E3E9EE"), (1, "#8E9CA8")], cx=.4, cy=.35, r=.7, ad="ak")
    return (f'<path d="M45 83 Q70 93 95 83" fill="none" stroke="{CZ}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M45 83 Q70 93 95 83" fill="none" stroke="{GOL}" stroke-width="4.8" stroke-linecap="round"/>'
            f'<circle cx="70" cy="95" r="6.4" fill="{gm}" stroke="{CZ}" stroke-width="1.8"/>'
            f'<circle cx="70" cy="95" r="3.9" fill="none" stroke="#6C7A86" stroke-width=".9" stroke-dasharray="1.1 .9"/>'
            f'<path d="M70 92.2 L70.9 94.1 L72.8 95 L70.9 95.9 L70 97.8 L69.1 95.9 L67.2 95 L69.1 94.1 Z" fill="#6C7A86"/>')


def akce_sikke(s, cx, cy, r, yazi=None):
    """Gümüş akçe: tırtıklı kenar, iç halka, sekiz köşeli yıldız (yazısız: kutsal metin yok)."""
    g = s.rad([(0, "#FFFFFF"), (.45, "#E7ECF0"), (.85, "#AEB9C3"), (1, "#7E8B97")], cx=.38, cy=.32, r=.75, ad="sk")
    dis = []
    import math
    for i in range(36):
        a = 2 * math.pi * i / 36
        rr = r if i % 2 == 0 else r * .94
        dis.append(f"{f(cx + rr * math.cos(a))} {f(cy + rr * math.sin(a))}")
    from .temel import selcuklu_yildizi, cizgi_d
    y8 = selcuklu_yildizi(cx, cy, r * .5)
    o = (f'<path d="M{" L".join(dis)} Z" fill="{g}" stroke="{CZ}" stroke-width="{f(r * .07)}" stroke-linejoin="round"/>'
         f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * .74)}" fill="none" stroke="#6C7A86" stroke-width="{f(r * .045)}"/>'
         f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * .66)}" fill="none" stroke="#6C7A86" stroke-width="{f(r * .03)}" stroke-dasharray="{f(r * .06)} {f(r * .05)}"/>'
         f'<path d="{cizgi_d(y8, True)}" fill="#C9D2DA" stroke="#5E6C78" stroke-width="{f(r * .04)}" stroke-linejoin="round"/>'
         f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * .14)}" fill="#5E6C78"/>'
         f'<path d="M{f(cx - r * .55)} {f(cy - r * .62)} A{f(r * .8)} {f(r * .8)} 0 0 1 {f(cx + r * .2)} {f(cy - r * .82)}" stroke="#FFFFFF" stroke-width="{f(r * .1)}" fill="none" stroke-linecap="round" opacity=".9"/>')
    if yazi:
        o += f'<text x="{f(cx)}" y="{f(cy + r * .2)}" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="{f(r * .55)}" fill="#3B4652">{yazi}</text>'
    return o


def turk_bayragi(x, y, G, dalga=0.0):
    """Türk bayrağı (Bayrak Kanunu oranları): boy 1,5G, en G. (x, y) sol üst köşe (gönder tarafı).
    dalga: 0 düz; >0 ise hafif dalgalı alt/üst kenar."""
    import math
    L = 1.5 * G
    # dış hilal merkezi gönderden 0,5G; dış çap 0,5G; iç çap 0,4G; merkezler arası 0,0625G
    # yıldızın çevrel çember çapı 0,25G; iç hilalden yıldız çemberine 1/3 G
    cy = y + G / 2
    dx = x + G / 30 + .5 * G
    R1 = .25 * G
    ix = dx + .0625 * G
    R2 = .2 * G
    sx = ix + R2 + G / 3 + .125 * G
    Ry = .125 * G
    from .temel import yildiz_noktalari, cizgi_d
    yd = yildiz_noktalari(sx, cy, Ry, Ry * .382, 5, math.pi)  # bir köşesi gönder yönünü göstermez: yatay eksen
    d = dalga
    kenar = (f"M{f(x)} {f(y)} C{f(x + L * .3)} {f(y - d)} {f(x + L * .6)} {f(y + d)} {f(x + L)} {f(y)} "
             f"L{f(x + L)} {f(y + G)} C{f(x + L * .6)} {f(y + G + d)} {f(x + L * .3)} {f(y + G - d)} {f(x)} {f(y + G)} Z")
    return (f'<path d="{kenar}" fill="#E30A17"/>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(G / 30)}" height="{f(G)}" fill="#FFFFFF"/>'
            f'<circle cx="{f(dx)}" cy="{f(cy)}" r="{f(R1)}" fill="#FFFFFF"/>'
            f'<circle cx="{f(ix)}" cy="{f(cy)}" r="{f(R2)}" fill="#E30A17"/>'
            f'<path d="{cizgi_d(yd, True, 2)}" fill="#FFFFFF"/>')


def pamuk_poz(s, poz):
    """140×160 kutuda tam boy Pamuk."""
    o = ['<g transform="translate(0 6)">']
    ifade = {"selam": "gulen", "dusunen": "dusunen", "sasiran": "sasiran", "akce": "gozkirp", "kitap": "mutlu", "bayrak": "gulen"}.get(poz, "mutlu")
    o.append(_pamuk_govde(s, poz))
    if poz == "selam":
        o.append(_on_bacak(56))
        o.append(_kol(84, 98, 112, 52, 106, 86))
        o.append(_pati(113, 47, 7.6, -15))
        o.append(f'<path d="M124 36 q5 -4 4 -10 M129 46 q6 -1 8 -6 M121 28 q2 -5 0 -9" fill="none" stroke="{GOL}" stroke-width="2.4" stroke-linecap="round"/>')
    elif poz == "dusunen":
        o.append(_on_bacak(84))
        o.append(_kol(56, 100, 60, 80, 46, 92))
        o.append(_pati(61, 79, 6.8, 20))
    elif poz == "sasiran":
        o.append(_kol(52, 98, 30, 70, 34, 92))
        o.append(_pati(28, 66, 6.8, -30))
        o.append(_kol(88, 98, 110, 70, 106, 92))
        o.append(_pati(112, 66, 6.8, 30))
        o.append(f'<path d="M14 40 l-6 -6 M10 54 l-8 0 M126 40 l6 -6 M130 54 l8 0" stroke="{MER}" stroke-width="2.6" stroke-linecap="round"/>')
    elif poz == "akce":
        o.append(_kol(52, 100, 58, 116, 46, 112))
        o.append(_kol(88, 100, 82, 116, 94, 112))
        o.append(akce_sikke(s, 70, 118, 19))
        o.append(_pati(53, 117, 6.6, -10))
        o.append(_pati(87, 117, 6.6, 10))
    elif poz == "kitap":
        # tezhipli açık kitap
        gk = s.lin([(0, "#FFFDF4"), (1, "#F1E6C8")], 0, 0, 0, 1, ad="kt")
        o.append(f'<path d="M30 112 Q50 104 70 112 Q90 104 110 112 L110 142 Q90 134 70 142 Q50 134 30 142 Z" fill="{LAJVER}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                 f'<path d="M33 110 Q51 103 70 110 L70 139 Q51 132 33 139 Z" fill="{gk}" stroke="{CZ}" stroke-width="1.6"/>'
                 f'<path d="M107 110 Q89 103 70 110 L70 139 Q89 132 107 139 Z" fill="{gk}" stroke="{CZ}" stroke-width="1.6"/>'
                 f'<path d="M37 113 Q51 108 66 113 L66 135 Q51 130 37 135 Z" fill="none" stroke="{ALTIN}" stroke-width="1.4"/>'
                 f'<path d="M103 113 Q89 108 74 113 L74 135 Q89 130 103 135 Z" fill="none" stroke="{ALTIN}" stroke-width="1.4"/>'
                 + "".join(f'<path d="M41 {118 + i * 4} Q51 {115 + i * 4} 62 {118 + i * 4}" stroke="#8C7A5A" stroke-width="1" fill="none" opacity=".7"/>' for i in range(4))
                 + f'<circle cx="88.5" cy="122" r="6" fill="{GOL}" stroke="{ALTIN}" stroke-width="1.4"/><path d="M88.5 117 l1.5 3.5 3.5 1.5 -3.5 1.5 -1.5 3.5 -1.5 -3.5 -3.5 -1.5 3.5 -1.5 Z" fill="{ALTIN_A}"/>'
                 + f'<path d="M80 131 Q88.5 128 97 131" stroke="#8C7A5A" stroke-width="1" fill="none" opacity=".7"/>')
        o.append(_pati(34, 120, 6.4, -20))
        o.append(_pati(106, 120, 6.4, 20))
    elif poz == "bayrak":
        o.append(_on_bacak(56))
        o.append(f'<path d="M110 150 L110 -30" stroke="#6B4A2E" stroke-width="4.4" stroke-linecap="round"/>'
                 f'<circle cx="110" cy="-32" r="3.6" fill="{ALTIN}" stroke="{CZ}" stroke-width="1.2"/>'
                 f'<g>{turk_bayragi(112, -28, 30, 3)}</g>')
        o.append(_kol(86, 98, 107, 74, 104, 92))
        o.append(_pati(108, 72, 7.2, 0))
    else:
        o.append(_on_bacak(56))
        o.append(_on_bacak(84))
    o.append(_tasma(s))
    rot = {"dusunen": -7, "sasiran": 0, "selam": 4, "bayrak": 3}.get(poz, 0)
    o.append(f'<g transform="translate(20 4) rotate({rot} 50 60)">{pamuk_bas(s, ifade)}</g>')
    if poz == "dusunen":
        o.append(f'<circle cx="126" cy="14" r="12" fill="#FFFFFF" stroke="{CZ}" stroke-width="1.8"/><circle cx="114" cy="30" r="3" fill="#FFFFFF" stroke="{CZ}" stroke-width="1.4"/>'
                 f'<text x="126" y="20.5" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="18" fill="{GOL_K}">?</text>')
    if poz == "sasiran":
        o.append(f'<text x="122" y="22" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="22" fill="{MER}">!</text>')
    o.append("</g>")
    return "".join(o)


def pamuk_yuzer(s):
    o = [f'<g transform="translate(10 -4) scale(.82)">{pamuk_bas(s, "gulen")}</g>',
         _pati(24, 66, 6, -30), _pati(96, 66, 6, 30),
         '<path d="M0 66 Q7.5 60 15 66 T30 66 T45 66 T60 66 T75 66 T90 66 T105 66 T120 66 V80 H0 Z" fill="#7FD3CF" stroke="#0A6C74" stroke-width="1.6"/>',
         '<path d="M8 73 q6 -4 12 0 M48 74 q6 -4 12 0 M90 73 q6 -4 12 0" fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round"/>']
    return "".join(o)


def av_pamuk(s):
    return (f'<circle cx="20" cy="20" r="19" fill="#FFF0CF" stroke="{CZ}" stroke-width="1.4"/>'
            f'<g transform="translate(3 6) scale(.34)">{pamuk_bas(s, "mutlu")}</g>')


# ------------------------------------------------------------------ İNSANLAR (yarım boy, 200×210)

TEN = {"elif": "#F6D2B5", "yusuf": "#E2B18C", "zeynep": "#F1CDB0"}


def _goz(cx, cy, ifade, yon=0.0):
    if ifade in ("gulen",):
        return f'<path d="M{f(cx - 6)} {f(cy + 1.5)} Q{f(cx)} {f(cy - 5)} {f(cx + 6)} {f(cy + 1.5)}" fill="none" stroke="{CZ}" stroke-width="2.6" stroke-linecap="round"/>'
    ry = 6.2 if ifade == "sasiran" else 5.4
    return (f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="4.6" ry="{ry}" fill="#2A211F"/>'
            f'<circle cx="{f(cx - 1.4 + yon)}" cy="{f(cy - 2)}" r="1.8" fill="#FFFFFF"/>'
            f'<circle cx="{f(cx + 1.6 + yon)}" cy="{f(cy + 2)}" r=".8" fill="#FFFFFF"/>')


def _agiz(ifade, cx=100, cy=104):
    if ifade == "gulen" or ifade == "aha":
        return (f'<path d="M{f(cx - 9)} {f(cy - 2)} Q{f(cx)} {f(cy + 11)} {f(cx + 9)} {f(cy - 2)} Q{f(cx)} {f(cy + 1)} {f(cx - 9)} {f(cy - 2)} Z" fill="#A8323E" stroke="{CZ}" stroke-width="1.8" stroke-linejoin="round"/>'
                f'<path d="M{f(cx - 4)} {f(cy + 4)} Q{f(cx)} {f(cy + 7)} {f(cx + 4)} {f(cy + 4)} Q{f(cx)} {f(cy + 2.5)} {f(cx - 4)} {f(cy + 4)} Z" fill="#F08A96"/>')
    if ifade == "sasiran":
        return f'<ellipse cx="{f(cx)}" cy="{f(cy + 2)}" rx="4" ry="5" fill="#A8323E" stroke="{CZ}" stroke-width="1.8"/>'
    if ifade == "dusunen":
        return f'<path d="M{f(cx - 6)} {f(cy + 2)} Q{f(cx)} {f(cy)} {f(cx + 6)} {f(cy - 1)}" fill="none" stroke="{CZ}" stroke-width="2.2" stroke-linecap="round"/>'
    if ifade == "soru":
        return f'<path d="M{f(cx - 5)} {f(cy + 1)} Q{f(cx)} {f(cy + 5)} {f(cx + 5)} {f(cy + 1)}" fill="none" stroke="{CZ}" stroke-width="2.2" stroke-linecap="round"/>'
    return f'<path d="M{f(cx - 7)} {f(cy)} Q{f(cx)} {f(cy + 7)} {f(cx + 7)} {f(cy)}" fill="none" stroke="{CZ}" stroke-width="2.2" stroke-linecap="round"/>'


def _kas(ifade, renk):
    if ifade == "sasiran":
        return f'<path d="M78 70 Q86 64 94 69 M106 69 Q114 64 122 70" fill="none" stroke="{renk}" stroke-width="2.8" stroke-linecap="round"/>'
    if ifade == "dusunen":
        return f'<path d="M78 74 Q86 71 94 74 M106 71 Q114 67 122 70" fill="none" stroke="{renk}" stroke-width="2.8" stroke-linecap="round"/>'
    if ifade == "soru":
        return f'<path d="M78 73 Q86 69 94 72 M106 70 Q114 66 122 71" fill="none" stroke="{renk}" stroke-width="2.8" stroke-linecap="round"/>'
    return f'<path d="M78 73 Q86 69 94 73 M106 73 Q114 69 122 73" fill="none" stroke="{renk}" stroke-width="2.8" stroke-linecap="round"/>'


def _yuz(s, kim, ifade):
    ten = TEN[kim]
    tg = s.rad([(0, "#FFF4EA"), (.55, ten), (1, "#D9A584" if kim != "yusuf" else "#C9936E")], cx=.42, cy=.38, r=.7, ad="tn")
    o = [f'<ellipse cx="57" cy="88" rx="6" ry="8" fill="{ten}" stroke="{CZ}" stroke-width="{K}"/>',
         f'<ellipse cx="143" cy="88" rx="6" ry="8" fill="{ten}" stroke="{CZ}" stroke-width="{K}"/>',
         f'<path d="M100 44 C127 44 142 60 142 86 C142 110 124 124 100 124 C76 124 58 110 58 86 C58 60 73 44 100 44 Z" fill="{tg}" stroke="{CZ}" stroke-width="{K}"/>',
         '<ellipse cx="74" cy="98" rx="7" ry="4.2" fill="#F59C9C" opacity=".55"/><ellipse cx="126" cy="98" rx="7" ry="4.2" fill="#F59C9C" opacity=".55"/>',
         _goz(86, 86, ifade, 1 if ifade == "dusunen" else 0), _goz(114, 86, ifade, 1 if ifade == "dusunen" else 0),
         f'<path d="M98.5 92 Q101 97 98 99" fill="none" stroke="#B5785A" stroke-width="1.8" stroke-linecap="round"/>',
         _agiz(ifade)]
    return o


def insan_bas(s, kim, ifade="normal"):
    o = []
    if kim == "elif":
        sac, sac2 = "#4A2C22", "#6E3F2C"
        o.append(f'<path d="M58 84 C52 112 54 150 66 168 L86 160 C76 140 74 110 76 92 Z" fill="{sac}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                 f'<path d="M142 84 C148 112 146 150 134 168 L114 160 C124 140 126 110 124 92 Z" fill="{sac}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>')
        o += _yuz(s, kim, ifade)
        o.append(_kas(ifade, "#3B231B"))
        o.append(f'<path d="M57 86 C54 56 72 38 100 38 C128 38 146 56 143 86 C138 72 126 62 112 60 C104 70 90 74 74 72 C66 74 60 79 57 86 Z" fill="{sac}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                 f'<path d="M78 52 Q96 42 116 48 M70 64 Q76 54 88 50" stroke="{sac2}" stroke-width="3" fill="none" stroke-linecap="round"/>'
                 f'<path d="M62 64 Q100 30 138 64" fill="none" stroke="{CZ}" stroke-width="8.4" stroke-linecap="round"/>'
                 f'<path d="M62 64 Q100 30 138 64" fill="none" stroke="{KEH}" stroke-width="5" stroke-linecap="round"/>')
    elif kim == "yusuf":
        sac = "#221C1B"
        o += _yuz(s, kim, ifade)
        o.append(_kas(ifade, "#221C1B"))
        o.append(f'<path d="M58 82 C54 54 74 38 100 38 C128 38 147 52 142 82 C138 70 132 63 124 60 C112 66 96 64 84 58 C76 62 64 68 58 82 Z" fill="{sac}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                 '<path d="M86 46 Q104 40 124 50" stroke="#4A403C" stroke-width="3" fill="none" stroke-linecap="round"/>')
        # gözlük
        o.append(f'<g fill="none" stroke="{CZ}" stroke-width="2.6"><circle cx="86" cy="87" r="10.5" fill="#FFFFFF" fill-opacity=".18"/><circle cx="114" cy="87" r="10.5" fill="#FFFFFF" fill-opacity=".18"/>'
                 '<path d="M96.5 86 Q100 83 103.5 86"/><path d="M75.5 85 L60 82 M124.5 85 L140 82"/></g>'
                 '<path d="M79 82 l4 -3 M107 82 l4 -3" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity=".8"/>')
    elif kim == "zeynep":
        sac = "#5A3B2C"
        o.append(f'<circle cx="100" cy="34" r="15" fill="{sac}" stroke="{CZ}" stroke-width="{K}"/>'
                 f'<path d="M90 30 Q100 24 110 30" stroke="#7A5440" stroke-width="2.4" fill="none"/>')
        o += _yuz(s, kim, ifade)
        o.append(_kas(ifade, "#4A2F22"))
        o.append(f'<path d="M58 84 C55 56 74 42 100 42 C126 42 145 56 142 84 C136 66 120 56 100 56 C82 56 66 64 58 84 Z" fill="{sac}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                 '<path d="M74 54 Q100 46 126 54" stroke="#7A5440" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
        o.append(f'<g fill="none" stroke="{KOB}" stroke-width="2.8"><rect x="74" y="79" width="22" height="16" rx="5" fill="#FFFFFF" fill-opacity=".2"/><rect x="104" y="79" width="22" height="16" rx="5" fill="#FFFFFF" fill-opacity=".2"/>'
                 '<path d="M96 85 Q100 82 104 85"/><path d="M74 84 L60 82 M126 84 L140 82"/></g>')
    return "".join(o)


def _govde_insan(s, kim):
    if kim == "elif":
        g = s.lin([(0, "#F06A50"), (1, MER_K)], 0, 0, 1, 1, ad="ek")
        return (f'<path d="M92 128 h16 v20 h-16 z" fill="{TEN["elif"]}" stroke="{CZ}" stroke-width="{K}"/>'
                f'<path d="M30 210 C30 168 52 146 100 146 C148 146 170 168 170 210 Z" fill="{g}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                f'<path d="M86 146 L100 168 L114 146" fill="#FFF3E2" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                f'<path d="M100 168 V210" stroke="{CZ}" stroke-width="1.6"/>'
                f'<circle cx="122" cy="176" r="5" fill="{KEH}" stroke="{CZ}" stroke-width="1.5"/>')
    if kim == "yusuf":
        g = s.lin([(0, "#2DBDBF"), (1, GOL_K)], 0, 0, 1, 1, ad="yk")
        return (f'<path d="M92 128 h16 v20 h-16 z" fill="{TEN["yusuf"]}" stroke="{CZ}" stroke-width="{K}"/>'
                f'<path d="M30 210 C30 168 52 146 100 146 C148 146 170 168 170 210 Z" fill="{g}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                f'<path d="M82 146 L100 160 L118 146 L112 142 L100 152 L88 142 Z" fill="#FFFFFF" stroke="{CZ}" stroke-width="1.8" stroke-linejoin="round"/>'
                f'<path d="M58 176 h10 M132 176 h10" stroke="#FFFFFF" stroke-width="2" opacity=".5"/>'
                f'<path d="M124 170 l6 0 l3 6 l-3 6 l-6 0 l-3 -6 z" fill="{KEH}" stroke="{CZ}" stroke-width="1.4"/>')
    if kim == "zeynep":
        g = s.lin([(0, "#FFFFFF"), (1, "#DCE3EC")], 0, 0, 1, 1, ad="zk")
        return (f'<path d="M92 128 h16 v20 h-16 z" fill="{TEN["zeynep"]}" stroke="{CZ}" stroke-width="{K}"/>'
                f'<path d="M30 210 C30 168 52 146 100 146 C148 146 170 168 170 210 Z" fill="{g}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>'
                f'<path d="M84 146 L100 176 L116 146 Z" fill="{KOB}" stroke="{CZ}" stroke-width="1.8" stroke-linejoin="round"/>'
                f'<path d="M84 146 L94 186 M116 146 L106 186" stroke="{CZ}" stroke-width="1.8"/>'
                f'<path d="M126 180 h18 v18 h-18 z" fill="none" stroke="#AEB8C4" stroke-width="1.6"/><path d="M131 172 v12" stroke="{KOB}" stroke-width="3" stroke-linecap="round"/>')
    return ""


def _el(x, y, ten, r=11, aci=0, isaret=False):
    """El. isaret=True: açık avuç (dört parmak + başparmak), "söz istiyorum / anlatıyorum" jesti.
    Tek parmaklı yumruk kullanılmaz: küçük boyutta yanlış bir el işareti gibi okunabilir."""
    if not isaret:
        return (f'<g transform="rotate({aci} {f(x)} {f(y)})"><ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r * 1.05)}" '
                f'fill="{ten}" stroke="{CZ}" stroke-width="{K}"/></g>')
    k = r / 11
    parca = []
    # dört parmak (orta ikisi daha uzun), avucun üstünden çıkar
    uclar = ((-6.4, -17.0), (-2.15, -19.6), (2.15, -19.2), (6.4, -16.2))
    for px, ust in uclar:
        parca.append(f'<rect x="{f(x + (px - 2.15) * k, 2)}" y="{f(y + ust * k, 2)}" width="{f(4.3 * k, 2)}" '
                     f'height="{f((-ust - 1) * k, 2)}" rx="{f(2.15 * k, 2)}"/>')
    # başparmak: gövdeye dönük yanda, yukarı-dışa açık
    parca.append(f'<rect x="{f(x - 14.6 * k, 2)}" y="{f(y - 8.4 * k, 2)}" width="{f(4.6 * k, 2)}" height="{f(11.5 * k, 2)}" '
                 f'rx="{f(2.3 * k, 2)}" transform="rotate(-38 {f(x - 12.3 * k, 2)} {f(y - 2.6 * k, 2)})"/>')
    parca.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r * 1.05)}"/>')
    sekil = "".join(parca)
    # parmak araları: uçlardaki çentikten avuca doğru ince çizgi
    ara = "".join(f'<path d="M{f(x + px * k, 2)} {f(y + (max(u1, u2) + 3.2) * k, 2)} V{f(y - 7.6 * k, 2)}"/>'
                  for px, u1, u2 in ((-4.25, -17.0, -19.6), (0, -19.6, -19.2), (4.25, -19.2, -16.2)))
    return (f'<g transform="rotate({aci} {f(x)} {f(y)})">'
            f'<g fill="{ten}" stroke="{CZ}" stroke-width="{f(K * 2, 2)}" stroke-linejoin="round">{sekil}</g>'
            f'<g fill="{ten}">{sekil}</g>'
            f'<g stroke="{CZ}" stroke-width="{f(K * .55, 2)}" stroke-linecap="round" fill="none">{ara}</g>'
            f'</g>')


def _insan_kol(x0, y0, x1, y1, kx, ky, renk, kal=26):
    return (f'<path d="M{f(x0)} {f(y0)} Q{f(kx)} {f(ky)} {f(x1)} {f(y1)}" fill="none" stroke="{CZ}" stroke-width="{kal}" stroke-linecap="round"/>'
            f'<path d="M{f(x0)} {f(y0)} Q{f(kx)} {f(ky)} {f(x1)} {f(y1)}" fill="none" stroke="{renk}" stroke-width="{kal - 4.6}" stroke-linecap="round"/>')


KOL_RENK = {"elif": "#E85A44", "yusuf": "#1FAFB1", "zeynep": "#F2F5F9"}


def insan_poz(s, kim, poz):
    ten = TEN[kim]
    kr = KOL_RENK[kim]
    ifade = {"soru": "soru", "dusunen": "dusunen", "aha": "aha", "anlatan": "normal", "defter": "gulen", "gulen": "gulen",
             "kitap": "normal", "sasiran": "sasiran"}.get(poz, "normal")
    o = [_govde_insan(s, kim)]
    on = []
    if poz in ("soru", "aha"):
        on.append(_insan_kol(150, 168, 168, 96, 172, 140, kr))
        on.append(_el(168, 90, ten, 11, 10, isaret=True))
    elif poz == "dusunen":
        on.append(_insan_kol(70, 172, 100, 140, 66, 150, kr))
        on.append(_el(104, 134, ten, 10.5, 20))
    elif poz == "anlatan":
        on.append(_insan_kol(150, 170, 182, 132, 178, 166, kr))
        on.append(_el(186, 128, ten, 11, -30, isaret=True))
    elif poz in ("defter", "kitap"):
        kapak = {"elif": MER, "yusuf": "#F0A21A", "zeynep": LAJVER}[kim]
        on.append(f'<g transform="rotate(-8 100 186)"><rect x="66" y="166" width="68" height="44" rx="4" fill="{kapak}" stroke="{CZ}" stroke-width="{K}"/>'
                  f'<rect x="72" y="171" width="56" height="34" rx="2" fill="none" stroke="{ALTIN if kim == "zeynep" else "#FFFFFF"}" stroke-width="1.6" opacity=".9"/>'
                  + (f'<path d="M100 176 l3 7 7 3 -7 3 -3 7 -3 -7 -7 -3 7 -3 Z" fill="{ALTIN}"/>' if kim == "zeynep" else
                     f'<path d="M86 182 h28 M86 190 h20" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"/>')
                  + "</g>")
        on.append(_el(70, 190, ten, 10.5, 0))
        on.append(_el(132, 186, ten, 10.5, 0))
    o.append(insan_bas(s, kim, ifade))
    o += on
    if poz == "soru":
        o.append(halolu_yazi('x="30" y="58" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="34"', "?", KEH, CZ, 1.1))
    if poz == "aha":
        o.append(f'<path d="M30 40 l8 8 M24 60 h12 M34 24 l4 10" stroke="{KEH}" stroke-width="3.4" stroke-linecap="round"/>'
                 f'<circle cx="30" cy="76" r="9" fill="#FFF6C8" stroke="{CZ}" stroke-width="1.6"/><path d="M27 86 h6" stroke="{CZ}" stroke-width="2"/>')
    if poz == "dusunen":
        o.append(f'<circle cx="170" cy="42" r="15" fill="#FFFFFF" stroke="{CZ}" stroke-width="1.8"/><circle cx="154" cy="62" r="4" fill="#FFFFFF" stroke="{CZ}" stroke-width="1.6"/>'
                 f'<text x="170" y="50" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="22" fill="{GOL_K}">?</text>')
    return "".join(o)


def avatar(s, kim, zemin):
    kl = s.klip('<circle cx="100" cy="105" r="95"/>', ad="avk")
    return (f'<circle cx="100" cy="105" r="96" fill="{zemin}"/>'
            f'<g clip-path="{kl}"><g transform="translate(0 6)">{_govde_insan(s, kim)}{insan_bas(s, kim, "normal")}</g></g>'
            f'<circle cx="100" cy="105" r="96" fill="none" stroke="{CZ}" stroke-width="6"/>')


# ------------------------------------------------------------------ sembol kütüphanesi

def semboller():
    s = Svg("kr")
    sy = []
    for poz in ("selam", "dusunen", "sasiran", "akce", "kitap", "otur"):
        sy.append(f'<symbol id="pamuk-{poz}" viewBox="0 0 140 160">{pamuk_poz(s, poz)}</symbol>')
    sy.append(f'<symbol id="pamuk-bayrak" viewBox="0 -40 170 200">{pamuk_poz(s, "bayrak")}</symbol>')
    sy.append(f'<symbol id="pamuk-bas" viewBox="8 2 84 82">{pamuk_bas(s, "mutlu")}</symbol>')
    sy.append(f'<symbol id="pamuk-bas-gulen" viewBox="8 2 84 82">{pamuk_bas(s, "gulen")}</symbol>')
    sy.append(f'<symbol id="pamuk-bas-sasiran" viewBox="8 -2 84 86">{pamuk_bas(s, "sasiran")}</symbol>')
    sy.append(f'<symbol id="pamuk-yuzer" viewBox="0 0 120 80">{pamuk_yuzer(s)}</symbol>')
    sy.append(f'<symbol id="av-pamuk" viewBox="0 0 40 40">{av_pamuk(s)}</symbol>')
    for kim, pozlar in (("elif", ("soru", "dusunen", "aha", "sasiran")), ("yusuf", ("anlatan", "defter", "gulen")), ("zeynep", ("anlatan", "kitap"))):
        for poz in pozlar:
            sy.append(f'<symbol id="{kim}-{poz}" viewBox="0 0 200 210">{insan_poz(s, kim, poz)}</symbol>')
    for kim, zem in (("elif", "#FDE7E1"), ("yusuf", "#DCF3F1"), ("zeynep", "#E6ECFB")):
        sy.append(f'<symbol id="av-{kim}" viewBox="0 0 200 210">{avatar(s, kim, zem)}</symbol>')
    sy.append(f'<symbol id="akce" viewBox="0 0 40 40">{akce_sikke(s, 20, 20, 18)}</symbol>')
    return s.govde() + "".join(sy)
