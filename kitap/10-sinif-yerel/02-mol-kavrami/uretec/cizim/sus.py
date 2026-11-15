"""Süsleme kütüphanesi: Selçuklu yıldızı ve geçmesi, İznik çini bordürleri, tezhip köşebendi,
kilim ayracı, YANLIŞ/DOĞRU yıldız mühürleri, nişan (rozet) çerçeveleri, durak rozeti,
çay bardağı (muhasebe), ikon sembolleri.

CSS'te tekrar eden desenler (çini şeridi, zemin geçmesi) `veri_uri()` ile data-URI'ye çevrilir.
"""
import math
from urllib.parse import quote
from .temel import Svg, f, nok, cizgi_d, egri_d, selcuklu_yildizi, yildiz_noktalari, karis, acik, koyu, rng as RNG
from .renkler import (OBS, GOL, GOL_K, GOL_A, KEH, KEH_K, KEH_A, MER, MER_K, KOB, KOB_K, ALTIN, ALTIN_K,
                      ALTIN_A, LAJVER, ZUMRUT, DERIN, BEYAZ)


def veri_uri(svg):
    return "data:image/svg+xml," + quote(svg, safe=" =:/,;'()")


# ------------------------------------------------------------------ çini şeritleri (CSS desenleri)

def cini_serit_ince():
    """HUD altındaki ince İznik şeridi: kobalt zemin, beyaz Selçuklu yıldızları, turkuaz göbek, mercan nokta.
    Döşeme: 24×8 birim (CSS'te 7.2mm × 2.4mm)."""
    y = selcuklu_yildizi(6, 4, 3.3)
    yi = selcuklu_yildizi(6, 4, 1.5)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 8'>"
            f"<rect width='24' height='8' fill='{KOB_K}'/>"
            f"<path d='M0 .35 H24 M0 7.65 H24' stroke='{ALTIN}' stroke-width='.5'/>"
            f"<path d='{cizgi_d(y, True, 2)}' fill='#FFFFFF'/>"
            f"<path d='{cizgi_d(yi, True, 2)}' fill='{GOL}'/>"
            f"<path d='M14 4 L18 1.6 L22 4 L18 6.4 Z' fill='{GOL}' stroke='#FFFFFF' stroke-width='.45'/>"
            f"<circle cx='18' cy='4' r='.9' fill='{MER}'/>"
            "</svg>")


def cini_serit_genis():
    """Geniş çini bordürü: beyaz zemin, kobalt saz yaprağı, turkuaz lale, mercan karanfil (döşeme 48×16)."""
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 16'>"
            "<rect width='48' height='16' fill='#FFFFFF'/>"
            f"<path d='M0 .8 H48 M0 15.2 H48' stroke='{KOB_K}' stroke-width='1.6'/>"
            f"<path d='M0 2.4 H48 M0 13.6 H48' stroke='{GOL}' stroke-width='.6'/>"
            # saz yaprağı (kıvrık, kobalt)
            f"<path d='M2 12 C6 4 14 3 22 6 C15 6 9 8 5 12 Z' fill='{KOB}' stroke='{KOB_K}' stroke-width='.4'/>"
            f"<path d='M26 4 C30 12 38 13 46 10 C39 10 33 8 29 4 Z' fill='{KOB}' stroke='{KOB_K}' stroke-width='.4'/>"
            # lale (turkuaz)
            f"<path d='M12 11 C10 8 10.5 5.5 12 4 C12.6 5.6 13.4 6 14 6 C14.6 6 15.4 5.6 16 4 C17.5 5.5 18 8 16 11 Z' fill='{GOL}' stroke='{GOL_K}' stroke-width='.4'/>"
            f"<path d='M14 11 V13' stroke='{ZUMRUT}' stroke-width='.8'/>"
            # karanfil (mercan)
            f"<circle cx='36' cy='7.6' r='2.6' fill='{MER}' stroke='{MER_K}' stroke-width='.4'/>"
            f"<path d='M33.6 6.6 l1 -1.4 1 1 1 -1.6 1 1.6 1 -1 1 1.4' fill='none' stroke='#FFFFFF' stroke-width='.5'/>"
            f"<circle cx='24' cy='8' r='1.1' fill='{MER}'/><circle cx='4' cy='5' r='.7' fill='{GOL}'/><circle cx='44' cy='12' r='.7' fill='{GOL}'/>"
            "</svg>")


def zemin_gecme(renk="#E2F1F1"):
    """Sayfa zemini: Selçuklu yıldız-haç geçmesi, çok açık çizgi (döşeme 40×40)."""
    y = selcuklu_yildizi(20, 20, 9.5)
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'>"
            f"<g fill='none' stroke='{renk}' stroke-width='.7' stroke-linejoin='round'>"
            f"<path d='{cizgi_d(y, True, 2)}'/>"
            "<path d='M0 0 L6.2 6.2 M40 0 L33.8 6.2 M0 40 L6.2 33.8 M40 40 L33.8 33.8'/>"
            "<path d='M20 0 V7 M20 33 V40 M0 20 H7 M33 20 H40'/>"
            "</g></svg>")


def dalga_alt(renk1=GOL, renk2=DERIN):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 6'>"
            f"<path d='M0 0 H24 V2 Q18 6 12 2 T0 2 Z' fill='{OBS}'/>"
            f"<path d='M0 2 Q6 6 12 2 T24 2' fill='none' stroke='{renk1}' stroke-width='1.2'/></svg>")


# ------------------------------------------------------------------ tezhip köşebendi

def tezhip_kose(onek, zemin=LAJVER, altin=ALTIN):
    """Köşebent: iç kenarı dilimli (kubbeli) içbükey üçgen; lacivert zemin, altın kontur,
    köşegende hatayi çiçeği, iki yana rumi kıvrımları. Sol üst köşe için; diğerleri CSS ile çevrilir."""
    s = Svg(onek)
    ga = s.lin([(0, "#F7E3A1"), (.45, altin), (1, ALTIN_K)], 0, 0, 1, 1, ad="ta")
    gz = s.rad([(0, acik(zemin, .3)), (1, koyu(zemin, .25))], .15, .15, 1, ad="tz")
    # hipotenüs: (100,0) → (0,100) düz hat üzerinde dışa taşan dilimler (köşeden uzağa)
    n = 5
    pts = [(100 - 100 * i / n, 100 * i / n) for i in range(n + 1)]
    dis = "M0 0 H100"
    for i in range(n):
        q = pts[i + 1]
        rr = math.dist(pts[i], q) / 2
        dis += f" A{f(rr)} {f(rr)} 0 0 1 {nok(q)}"
    dis += " Z"
    s += f'<path d="{dis}" fill="{gz}" stroke="{ga}" stroke-width="4.5" stroke-linejoin="round"/>'
    s += f'<path d="{dis}" fill="none" stroke="{ALTIN_A}" stroke-width="1.1" transform="translate(6 6) scale(.84)"/>'
    # köşegende hatayi çiçeği
    cx, cy = 21, 21
    for i in range(8):
        a = math.pi / 4 * i
        x, y = cx + 8.5 * math.cos(a), cy + 8.5 * math.sin(a)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="6" ry="3.3" transform="rotate({f(math.degrees(a))} {f(x)} {f(y)})" fill="{"#FFFFFF" if i % 2 else GOL}" stroke="{altin}" stroke-width="1"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="5.2" fill="{MER}" stroke="{altin}" stroke-width="1.4"/><circle cx="{cx}" cy="{cy}" r="1.8" fill="{ALTIN_A}"/>'
    # rumi kıvrımlar (iki yana)
    for ayna in (False, True):
        def m(x, y):
            return (y, x) if ayna else (x, y)
        p = [m(32, 14), m(48, 8), m(62, 12), m(66, 20), m(60, 24), m(55, 20)]
        s += f'<path d="M{nok(p[0])} C{nok(p[1])} {nok(p[2])} {nok(p[3])} S{nok(p[4])} {nok(p[5])}" fill="none" stroke="{ga}" stroke-width="3.2" stroke-linecap="round"/>'
        q = [m(62, 12), m(74, 6), m(84, 6), m(92, 3)]
        s += f'<path d="M{nok(q[0])} C{nok(q[1])} {nok(q[2])} {nok(q[3])}" fill="none" stroke="{ga}" stroke-width="2.4" stroke-linecap="round"/>'
        yap = [m(78, 4), m(86, 10), m(80, 12)]
        s += f'<path d="M{nok(yap[0])} Q{nok(yap[1])} {nok(yap[2])} Z" fill="{ALTIN_A}" stroke="{altin}" stroke-width=".9"/>'
        c = m(46, 16)
        s += f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="2.6" fill="#FFFFFF" stroke="{altin}" stroke-width=".9"/>'
        c = m(34, 6)
        s += f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="1.5" fill="{ALTIN_A}"/>'
    return s.cikti("0 0 100 100", cls="tezhip-kose")


# ------------------------------------------------------------------ kilim ayracı

def kilim_serit(onek, en=1880, boy=60, renkler=None):
    """Dokuma kilim şeridi: basamaklı baklava (göz), koçboynuzu, elibelinde; viewBox en×boy."""
    k = renkler or {"kok": "#B23A2E", "civit": "#253C78", "asi": "#D99A2B", "zemin": "#F5E8D0", "cam": "#1E8A86"}
    s = Svg(onek)
    s += f'<rect width="{en}" height="{boy}" fill="{k["zemin"]}"/>'
    s += f'<rect width="{en}" height="6" fill="{k["civit"]}"/><rect y="{boy - 6}" width="{en}" height="6" fill="{k["civit"]}"/>'
    # üst/alt dişli kenar
    dis = "".join(f'<path d="M{x} 6 l5 5 l5 -5 Z M{x} {boy - 6} l5 -5 l5 5 Z" fill="{k["kok"]}"/>' for x in range(0, en, 10))
    s += dis
    adim = 92
    i = 0
    for x in range(0, en + adim, adim):
        cx, cy = x + adim / 2, boy / 2
        if i % 2 == 0:
            # basamaklı göz (baklava)
            for r, c in ((22, k["kok"]), (15, k["asi"]), (8, k["civit"])):
                st = []
                for (dx, dy) in ((0, -r), (r, 0), (0, r), (-r, 0)):
                    st.append((cx + dx, cy + dy))
                s += f'<path d="M{nok(st[0])} L{nok(st[1])} L{nok(st[2])} L{nok(st[3])} Z" fill="{c}"/>'
            s += f'<rect x="{f(cx - 2)}" y="{f(cy - 2)}" width="4" height="4" fill="{k["zemin"]}"/>'
        else:
            # koçboynuzu (iki kıvrık boynuz)
            s += (f'<path d="M{f(cx - 26)} {f(cy + 13)} V{f(cy - 9)} H{f(cx - 12)} V{f(cy + 4)} H{f(cx - 19)} V{f(cy - 2)} '
                  f'M{f(cx + 26)} {f(cy + 13)} V{f(cy - 9)} H{f(cx + 12)} V{f(cy + 4)} H{f(cx + 19)} V{f(cy - 2)}" fill="none" stroke="{k["cam"]}" stroke-width="6" stroke-linejoin="miter"/>'
                  f'<rect x="{f(cx - 5)}" y="{f(cy - 15)}" width="10" height="30" fill="{k["kok"]}"/>'
                  f'<rect x="{f(cx - 2)}" y="{f(cy - 9)}" width="4" height="18" fill="{k["asi"]}"/>')
        i += 1
    return s.cikti(f"0 0 {en} {boy}", cls="kilim", par="xMidYMid slice")


# ------------------------------------------------------------------ mühürler

def muhur(onek, tur="yanlis", ust="✶ MÜHÜR ✶", alt=None, boy=None):
    """Sekiz köşeli yıldız mühür. tur: 'yanlis' (mercan) | 'dogru' (çini yeşili-turkuaz)."""
    renk = "#B4262C" if tur == "yanlis" else "#11807A"
    yazi = "YANLIŞ" if tur == "yanlis" else "DOĞRU"
    alt = alt or "VAN GÖLÜ TURU"
    s = Svg(onek)
    r = RNG(7 if tur == "yanlis" else 11)
    y8 = selcuklu_yildizi(50, 50, 47)
    y8i = selcuklu_yildizi(50, 50, 40)
    yaz_yol = s.kid("yol")
    yaz_yol2 = s.kid("yol")
    s.tanim(f'<path id="{yaz_yol}" d="M26 50 A24 24 0 0 1 74 50"/>')
    s.tanim(f'<path id="{yaz_yol2}" d="M23.4 50 A26.6 26.6 0 0 0 76.6 50"/>')
    # mürekkep dokusu: rastgele boşluklar (maske)
    bos = "".join(f'<circle cx="{f(r.uniform(5, 95))}" cy="{f(r.uniform(5, 95))}" r="{f(r.uniform(.4, 1.6))}" fill="#000"/>' for _ in range(34))
    mk = s.maske(f'<rect width="100" height="100" fill="#FFF"/>{bos}', ad="mk")
    s += (f'<g mask="{mk}">'
          f'<path d="{cizgi_d(y8, True)}" fill="{acik(renk, .9)}" fill-opacity=".55" stroke="{renk}" stroke-width="3.6" stroke-linejoin="round"/>'
          f'<path d="{cizgi_d(y8i, True)}" fill="none" stroke="{renk}" stroke-width="1.1" stroke-linejoin="round"/>'
          f'<circle cx="50" cy="50" r="30.5" fill="none" stroke="{renk}" stroke-width="1.8"/>'
          f'<path d="M30 42 H70 M30 58.6 H70" stroke="{renk}" stroke-width=".9"/>'
          f'<text font-family="Reem Kufi" font-weight="700" font-size="6.2" letter-spacing="1.1" fill="{renk}"><textPath href="#{yaz_yol}" startOffset="50%" text-anchor="middle">{ust}</textPath></text>'
          f'<text font-family="Reem Kufi" font-weight="700" font-size="5.6" letter-spacing="1" fill="{renk}"><textPath href="#{yaz_yol2}" startOffset="50%" text-anchor="middle">{alt}</textPath></text>'
          f'<text x="50" y="54.4" text-anchor="middle" font-family="Reem Kufi" font-weight="700" font-size="{12.6 if tur == "yanlis" else 13.4}" fill="{renk}">{yazi}</text>'
          f'</g>')
    w = f' width="{boy}"' if boy else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="muhur {tur}"{w}>{s.govde()}</svg>'


# ------------------------------------------------------------------ rozetler

def durak_rozeti(onek, metin, ust="DURAK", renk=GOL, renk2=GOL_K, altin=ALTIN, cls="durak-rozet"):
    s = Svg(onek)
    g = s.rad([(0, acik(renk, .35)), (.6, renk), (1, renk2)], .4, .35, .75, ad="dr")
    ga = s.lin([(0, "#F6DE95"), (.5, altin), (1, ALTIN_K)], 0, 0, 1, 1, ad="da")
    s += f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 48), True)}" fill="{ga}" stroke="{OBS}" stroke-width="2.4" stroke-linejoin="round"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 41), True)}" fill="{g}" stroke="{OBS}" stroke-width="1.6" stroke-linejoin="round"/>'
    s += f'<circle cx="50" cy="50" r="27" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
    s += f'<circle cx="50" cy="50" r="23.5" fill="none" stroke="{renk}" stroke-width="1.2" stroke-dasharray="2 1.6"/>'
    if ust:
        s += f'<text x="50" y="38" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="7.4" letter-spacing="1.2" fill="{renk2}">{ust}</text>'
        s += f'<text x="50" y="67" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="31" fill="{OBS}">{metin}</text>'
    else:
        s += metin
    return s.cikti("0 0 100 100", cls=cls)


def nisan(onek, ikon_svg, renk=GOL, renk2=GOL_K, kurdele=None):
    """Boyanacak nişan: altın-çini yıldız çerçeve + beyaz göbekte çizgi ikon (öğrenci boyar)."""
    s = Svg(onek)
    ga = s.lin([(0, "#F6DE95"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="na")
    gr = s.rad([(0, acik(renk, .3)), (1, renk2)], .4, .35, .8, ad="nr")
    y16 = yildiz_noktalari(50, 50, 49, 41, 16, -math.pi / 2)
    if kurdele:
        s += (f'<path d="M28 66 L18 112 L30 105 L37 117 L48 74 Z" fill="{kurdele}" stroke="{OBS}" stroke-width="1.8" stroke-linejoin="round"/>'
              f'<path d="M72 66 L82 112 L70 105 L63 117 L52 74 Z" fill="{koyu(kurdele, .15)}" stroke="{OBS}" stroke-width="1.8" stroke-linejoin="round"/>')
    s += f'<path d="{cizgi_d(y16, True)}" fill="{ga}" stroke="{OBS}" stroke-width="2" stroke-linejoin="round"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 40), True)}" fill="{gr}" stroke="{OBS}" stroke-width="1.6" stroke-linejoin="round"/>'
    for k in range(8):
        a = -math.pi / 2 + math.pi / 4 * k
        s += f'<circle cx="{f(50 + 33 * math.cos(a))}" cy="{f(50 + 33 * math.sin(a))}" r="2" fill="{ALTIN_A}"/>'
    s += f'<circle cx="50" cy="50" r="26" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
    s += f'<g transform="translate(30 30) scale(.8333)" fill="none" stroke="{OBS}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ikon_svg}</g>'
    return s.cikti("0 0 100 120" if kurdele else "0 0 100 100", cls="nisan-svg")


# nişan göbek ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    "deste": '<rect x="8" y="26" width="32" height="12" rx="2"/><rect x="11" y="16" width="26" height="10" rx="2"/><rect x="14" y="8" width="20" height="8" rx="2"/><path d="M14 32 h20 M17 21 h14"/>',
    "izotop": '<circle cx="20" cy="20" r="11"/><path d="M28 28 L40 40" stroke-width="4"/><circle cx="17" cy="18" r="3"/><circle cx="23" cy="21" r="3"/><circle cx="18" cy="24" r="2.6"/>',
    "kefal": '<path d="M6 24 C12 15 26 13 36 20 C38 22 40 23 42 24 C40 25 38 26 36 28 C26 35 12 33 6 24 Z"/><path d="M6 24 L1 17 M6 24 L1 31"/><circle cx="34" cy="22" r="1.6"/><path d="M14 9 h6 M17 6 v6 M28 40 h6"/>',
    "mizan": '<path d="M24 8 V40 M14 40 h20 M8 14 H40"/><path d="M8 14 L3 28 H13 Z M40 14 L35 28 H45 Z"/><circle cx="24" cy="8" r="2.4"/>',
    "karisim": '<path d="M12 8 h8 M16 8 V20 L8 38 C7 41 9 43 12 43 H20 C23 43 25 41 24 38 L16 20"/><path d="M30 8 h8 M34 8 V20 L26 38 C25 41 27 43 30 43 H38 C41 43 43 41 42 38 L34 20"/><path d="M10 33 H22 M28 33 H40"/>',
    "kale": '<path d="M6 42 V18 H12 V12 H18 V18 H22 V12 H26 V18 H30 V12 H36 V18 H42 V42 Z"/><path d="M19 42 V32 A5 5 0 0 1 29 32 V42"/><path d="M12 24 h4 M32 24 h4"/>',
}


def cay_bardagi(onek, seviye=1.0, bos_cizgi=False, boy=None):
    """İnce belli çay bardağı + tabak. seviye 0..1. bos_cizgi=True → boyanacak boş bardak (kesik seviye çizgisi)."""
    s = Svg(onek)
    cay = s.lin([(0, "#E8742A"), (.5, "#C2401C"), (1, "#8E2410")], 0, 0, 1, 0, ad="cy")
    cam = s.lin([(0, "#FFFFFF", .9), (.3, "#E9F4F6", .5), (1, "#C9DDE2", .7)], 0, 0, 1, 0, ad="cm")
    # bardak profili (lale biçimi), viewBox 0 0 40 52
    sol = [(8.2, 5), (9.6, 13), (13.4, 23), (12.6, 30), (9.6, 38), (11.2, 44)]
    sag = [(40 - x, y) for x, y in reversed(sol)]
    d = egri_d(sol, False) + " L" + nok(sag[0]) + egri_d(sag, False, bas_m=False)[0:] + " Z"
    d = egri_d(sol + sag, True, gerginlik=.9)
    kl = s.klip(f'<path d="{d}"/>', ad="ck")
    s += f'<ellipse cx="20" cy="47" rx="17" ry="3.6" fill="#F2F5F7" stroke="{OBS}" stroke-width="1.4"/>'
    s += f'<path d="M5 46.6 Q20 51.6 35 46.6" fill="none" stroke="{ALTIN}" stroke-width="1"/>'
    s += f'<path d="{d}" fill="{cam}"/>'
    if seviye > 0 and not bos_cizgi:
        yy = 44 - 36 * seviye
        s += f'<rect x="0" y="{f(yy)}" width="40" height="{f(44 - yy + 2)}" fill="{cay}" clip-path="{kl}"/>'
        s += f'<ellipse cx="20" cy="{f(yy)}" rx="{f(9 + 3 * (1 - abs(seviye - .55)))}" ry="1.2" fill="#F39A54" clip-path="{kl}"/>'
    if bos_cizgi:
        s += f'<path d="M10.5 {f(44 - 36 * .5)} H29.5" stroke="{GOL_K}" stroke-width=".8" stroke-dasharray="1.4 1.2" clip-path="{kl}"/>'
    s += f'<path d="{d}" fill="none" stroke="{OBS}" stroke-width="1.5" stroke-linejoin="round"/>'
    s += '<path d="M12.6 10 Q11.6 16 14.4 22" fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" opacity=".9"/>'
    if seviye >= .95 and not bos_cizgi:
        s += f'<path d="M15 4 q-2 -2 0 -4 M20 3.4 q-2 -2 0 -4 M25 4 q-2 -2 0 -4" fill="none" stroke="#9AAAB4" stroke-width="1" stroke-linecap="round" transform="translate(0 -1)"/>'
    w = f' width="{boy}"' if boy else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -4 40 56" class="cay"{w}>{s.govde()}</svg>'


# ------------------------------------------------------------------ ikon sembolleri (24×24 çizgi)

IKON = {
    "hedef": '<circle cx="12" cy="12" r="9.5" fill="#fff"/><circle cx="12" cy="12" r="6" fill="none" stroke="currentColor"/><circle cx="12" cy="12" r="2.4" fill="currentColor" stroke="none"/>',
    "anahtar": '<circle cx="7" cy="12" r="4.2"/><path d="M11.2 12 H22 M18 12 v3.6 M21 12 v2.6"/>',
    "kilit": '<rect x="5" y="10.5" width="14" height="10.5" rx="2"/><path d="M8 10.5 V8 a4 4 0 0 1 8 0 V10.5"/><circle cx="12" cy="15.6" r="1.4" fill="currentColor"/>',
    "tuzak": '<path d="M12 3 L22 20.5 H2 Z" fill="#fff"/><path d="M12 9.5 V14.5"/><circle cx="12" cy="17.5" r=".9" fill="currentColor"/>',
    "hazine": '<rect x="3" y="10" width="18" height="10.5" rx="1.6"/><path d="M3 10 C3 5.5 21 5.5 21 10"/><path d="M3 13.5 H21"/><rect x="10" y="11.5" width="4" height="4.6" rx=".8" fill="currentColor"/>',
    "hulasa": '<path d="M6 3.5 H18 V20.5 H6 Z"/><path d="M9 8 H15 M9 11.5 H15 M9 15 H13"/><path d="M4 3.5 H8 M16 20.5 H20"/>',
    "kale": '<path d="M3 21 V9 H6 V6 H9 V9 H11 V6 H13 V9 H15 V6 H18 V9 H21 V21 Z"/><path d="M10 21 V16.5 A2 2 0 0 1 14 16.5 V21"/>',
    "meclis": '<path d="M3 5 H14 V12.5 H8 L5 15 V12.5 H3 Z"/><path d="M10 14.5 V16.5 H16 L19 19 V16.5 H21 V9 H16"/>',
    "kissa": '<path d="M3 5.5 C6 4.5 9 4.5 12 6.5 C15 4.5 18 4.5 21 5.5 V19 C18 18 15 18 12 20 C9 18 6 18 3 19 Z"/><path d="M12 6.5 V20"/>',
    "makas": '<circle cx="6" cy="17" r="3"/><circle cx="6" cy="7" r="3"/><path d="M8.6 15.4 L21 5 M8.6 8.6 L21 19"/>',
    "medeniyet": '<circle cx="12" cy="13" r="8"/><path d="M12 5 V3 M9.5 3 H14.5"/><path d="M12 13 L16.5 8.5"/><path d="M5.5 13 H18.5 M12 6.5 V19.5"/><circle cx="12" cy="13" r="1.4" fill="currentColor"/>',
    "akce": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5.6" stroke-dasharray="1.4 1.2"/><path d="M12 8.6 l1 2.4 2.4 1 -2.4 1 -1 2.4 -1 -2.4 -2.4 -1 2.4 -1 Z" fill="currentColor" stroke="none"/>',
    "dogru": '<circle cx="12" cy="12" r="9.5" fill="currentColor" stroke="none"/><path d="M7.4 12.4 L10.6 15.6 L16.8 8.6" stroke="#fff" stroke-width="2.4"/>',
    "harita": '<path d="M3 6 L9 4 L15 6 L21 4 V18 L15 20 L9 18 L3 20 Z"/><path d="M9 4 V18 M15 6 V20"/>',
    "dalga": '<path d="M2 9 Q5 6 8 9 T14 9 T20 9 M2 15 Q5 12 8 15 T14 15 T20 15"/>',
    "bayrak": '<path d="M5 21 V3"/><path d="M5 4 H19 L16 8.5 L19 13 H5"/>',
    "kitap": '<path d="M4 4 H11 C12 4 12 5 12 6 V20 C12 19 11 18.5 10 18.5 H4 Z M20 4 H13 C12 4 12 5 12 6 V20 C12 19 13 18.5 14 18.5 H20 Z"/>',
    "terazi": '<path d="M12 4 V20 M7 20 H17 M4 7 H20"/><path d="M4 7 L1.5 13 H6.5 Z M20 7 L17.5 13 H22.5 Z"/>',
    "cay": '<path d="M7 4 C6.5 7 9 10 8.6 13 C8.3 15.5 7 17 7.6 19 H16.4 C17 17 15.7 15.5 15.4 13 C15 10 17.5 7 17 4 Z"/><path d="M4 20.5 H20"/>',
    "isik": '<path d="M9 18 H15 M10 21 H14"/><path d="M12 3 C8 3 5.5 6 5.5 9.4 C5.5 12.4 8 13.6 8.8 16 H15.2 C16 13.6 18.5 12.4 18.5 9.4 C18.5 6 16 3 12 3 Z"/>',
}


def ikon_sembolleri():
    out = []
    for ad, ic in IKON.items():
        out.append(f'<symbol id="i-{ad}" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{ic}</g></symbol>')
    return "".join(out)
