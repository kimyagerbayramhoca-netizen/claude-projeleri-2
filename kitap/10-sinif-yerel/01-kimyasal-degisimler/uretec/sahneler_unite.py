"""Kimyasal Değişimler · Kars–Erzurum Yolu · üniteye özel sahneler ve nişan ikonları.

kur_ortak bu modüle {{sahne|ad}} için ortak kütüphaneden ÖNCE bakar. Bantlar 2100×H birim (1 birim = 0,1 mm),
sol üst ≈ %55 × %75 levhaya boş, odak sağda, ışık yönü sabit (isik=−1: güneş solda), tohumlar sabit.
Mevsim: karlı Doğu Anadolu kışı; iç mekânlar sıcak (soba, kompartıman).

Sayfa → sahne: 1 panorama_kars · 2 cildir · 3 kars_mandira · 4 ani · 5 sarikamis · 6 pasinler · 7 erzurum ·
8 palandoken (b40) · 9 tren_ici · 10 cobandede · 11 kars_gari · 12 kars_kalesi (b62) · 13 kale_kapi_bazalt (b30) ·
14 ustad_bandi (ortak) · 15 kars_gece (b36) · 16 final_kars (kur.py {{final}}).
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim import sahne as S, yapilar as Y
from cizim.sahneler import W, H, _bitir, _cerceve_golge
from cizim.renkler import ALTIN
import kars_parcalar as P

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    # buz kristali (Çıldır)
    "buz": "".join(f'<path d="M24 24 L{f(24 + 18 * math.cos(a))} {f(24 + 18 * math.sin(a))}"/>'
                   f'<path d="M{f(24 + 11 * math.cos(a) + 5 * math.cos(a + 1.05))} {f(24 + 11 * math.sin(a) + 5 * math.sin(a + 1.05))} L{f(24 + 11 * math.cos(a))} {f(24 + 11 * math.sin(a))} '
                   f'L{f(24 + 11 * math.cos(a) + 5 * math.cos(a - 1.05))} {f(24 + 11 * math.sin(a) + 5 * math.sin(a - 1.05))}"/>'
                   for a in [math.pi / 2 + k * math.pi / 3 for k in range(6)]) + '<circle cx="24" cy="24" r="3"/>',
    # denklem: iki tanecik + ok + birleşmiş tanecik (Kars)
    "denklem": '<circle cx="9" cy="17" r="5"/><path d="M17 17 h6 M20 14 v6"/><circle cx="31" cy="17" r="5"/>'
               '<path d="M6 33 H30 M25 28 L31 33 L25 38"/><circle cx="38" cy="33" r="4.4"/><circle cx="44" cy="33" r="3"/>',
    # kireç ustası: mala + taş duvar (Ani)
    "kirec": '<path d="M6 42 H42 M6 34 H42 M6 26 H26 M14 26 V34 M30 34 V42 M22 34 V42 M38 26 V34"/>'
             '<path d="M30 22 L42 8 L44 10 L32 24 Z"/><path d="M28 24 L22 30"/>',
    # alev (Sarıkamış ocağı)
    "alev": '<path d="M24 44 C12 44 8 34 12 26 C14 22 18 20 18 14 C24 18 26 22 26 26 C28 22 30 18 30 12 C38 18 40 28 38 34 C36 40 31 44 24 44 Z"/>'
            '<path d="M24 44 C19 44 17 39 19 35 C21 32 23 31 23 28 C27 31 29 35 28 38 C27 41 26 44 24 44 Z"/>',
    # çökelek: beher, dipte çöken taneler (Pasinler)
    "cokelek": '<path d="M12 6 H36 M15 6 V38 Q15 43 20 43 H28 Q33 43 33 38 V6"/><path d="M15 22 H33"/>'
               '<circle cx="20" cy="38" r="2"/><circle cx="26" cy="39" r="2"/><circle cx="23" cy="34" r="2"/><circle cx="29" cy="35" r="1.6"/>'
               '<path d="M24 12 V18 M21 15 L24 18 L27 15"/>',
    # elektron: iki atom arasında ok (Erzurum)
    "elektron": '<circle cx="10" cy="30" r="7"/><circle cx="38" cy="30" r="7"/><path d="M14 16 Q24 6 34 16 M30 12 L34 16 L29 18"/>'
                '<circle cx="24" cy="9" r="3"/><path d="M22.2 9 H25.8"/><path d="M7 30 h6 M35 30 h6 M38 27 v6"/>',
}


# ------------------------------------------------------------------ yardımcılar

def _cerceve(s, h=H):
    return _cerceve_golge(s, h)


def _uzak_daglar(s, ufuk, tohum, tema="kis", isik=-1, renk=("#B6A6D2", "#8F84B8"), sis="#F3D6E2", kar_oran=.46,
                 kar_golge="#A9B6E2", kenar="#FFE6D2", dag=None):
    """Arka planda karlı dağ sırası: tepeler karlı (üst ≈ %46), gölgeli kar mavi-lavanta, etekler doygun renkte."""
    out = ""
    for i, (sol, sag, tx, ty, bicim) in enumerate(dag):
        d, _ = S.dag(s, sol, sag, ufuk, tx, ty, tohum + i, renk=renk[0], golge=renk[1], bicim=bicim,
                     kar_y=ty + (ufuk - ty) * kar_oran, kar="#FFFFFF", kar_golge=kar_golge,
                     sis=sis, isik=isik, sirt=4, puruz=8, kenar_isik=kenar)
        out += d
    return out


# ------------------------------------------------------------------ 1. DURAK · ÇILDIR GÖLÜ (sabah, buz tutmuş göl)

def cildir():
    s = Svg("kz-cil")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "safak")
    s += S.gunes(s, 1790, 150, 40, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=440, guc=.95)
    s += S.bulut_serit(s, 260, 196, 460, 10, "#FFE3EA", "#F6B8C8", .55)
    s += S.bulut_serit(s, 1180, 120, 380, 9, "#FFE8EE", "#F5BACB", .5)
    s += S.bulut(s, 1430, 92, 170, 9, ust="#FFFFFF", alt="#F9D3C4", op=.9)
    s += S.bulut(s, 860, 120, 150, 12, ust="#FFFFFF", alt="#E9D3EC", op=.75)
    uzak = _uzak_daglar(s, ufuk, 31, renk=("#A48CCB", "#6E5EA8"), sis="#F2C6DA",
                        dag=[(260, 1260, 760, 132, "tepe"), (1080, 2240, 1600, 112, "sivri"), (-80, 520, 160, 196, "tepe")])
    s += uzak
    s += P.buz_gol(s, 0, ufuk, W, H - ufuk, 32, ufuk="#FBE6EE", orta="#D7EAF5", derin="#97C2DE", parilti_x=1790)
    s += S.yansima(s, uzak, ufuk, 0, W, 90, op=.12)
    # sağ kıyı: karlı burun, köy evleri, çıplak kavaklar
    kiyi = [(1560, H), (1600, 336), (1700, 312), (1840, 300), (1980, 292), (2100, 288), (2100, H)]
    g = s.lin([(0, "#FFFFFF"), (1, "#DCE7F4")], 0, 290, 0, H, kull="userSpaceOnUse", ad="kk")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {H} Z" fill="{g}"/>'
    for i, (x, h) in enumerate([(1650, 120), (1690, 150), (1960, 160), (2010, 130), (2060, 150)]):
        s += P.ciplak_agac(x, 330 - (x - 1600) * .07, h, 40 + i, renk="#6A5446")
    for i, (x, w, h) in enumerate([(1740, 64, 44), (1820, 56, 40), (1890, 70, 46)]):
        s += P.ev_tas(s, x, 316 - (x - 1700) * .05, w, h, 50 + i, duvar=["#9AA0A8", "#A89C8E", "#8F98A2"][i], cati="#7C8A98", isik_pencere=True)
    for i, x in enumerate((1590, 1630, 1800)):
        s += P.cam(s, x, 336 - (x - 1580) * .06, 58 + (i % 2) * 14, 60 + i, renk="#2E6A4C")
    # buz altı balıkçılığı + atlı kızak (Pamuk yolcu)
    s += P.buz_deligi(1870, 432, 1.15)
    s += P.buz_deligi(1990, 392, .8, balik=False)
    s += P.at_kizak(s, 1520, 420, .82, at="#7C4A2A", yolcu=True)
    s += P.kar_yagisi(0, 0, W, H, 140, 33, op=.75, rmax=3)
    s += S.marti(1080, 150, .8, 2, renk="#5A4A70")
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ 2. DURAK · KARS (öğle, mandıra)

def kars_mandira():
    s = Svg("kz-kar")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gun")
    s += S.gunes(s, 300, 80, 34, hale="#FFF2C2", hale_r=320, guc=.8)
    for i, (x, y, w) in enumerate([(700, 120, 230), (1100, 92, 280), (1560, 140, 220), (1880, 70, 160)]):
        s += S.bulut(s, x, y, w, 70 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    s += _uzak_daglar(s, ufuk, 71, renk=("#6F94C6", "#4A6CA6"), sis="#BFDDF0", kenar="#F4FAFF",
                      dag=[(-60, 900, 380, 170, "tepe"), (700, 1700, 1150, 150, "tepe"), (1400, 2240, 1900, 130, "sivri")])
    # Kars yaylası: karlı geniş düzlük, uzakta kale tepesi
    s += P.kar_zemin(s, 0, W, ufuk + 6, 72, ust="#F7FAFD", alt="#D9E6F4", dalga=8, n=8)
    kale, _ = P.bazalt_kale(s, 1300, 1540, ufuk + 26, 92, 73, bayrak=True)
    s += kale
    for i in range(7):
        x = 1520 + i * 34
        s += P.ev_tas(s, x, ufuk + 26 + (i % 2) * 3, 28, 20, 80 + i, duvar=["#9AA0A8", "#A89C8E"][i % 2], cati="#7C8A98", baca=False)
    for i, x in enumerate((1600, 1660, 1720, 2040, 2080)):
        s += P.cam(s, x, 352, 70 + (i % 3) * 16, 90 + i, renk="#2F6B4C")
    s += P.kar_zemin(s, 1100, W, 342, 74, ust="#FFFFFF", alt="#DCE7F4", dalga=6, n=6)
    s += P.mandira(s, 1640, 410, 300, 128, 75)
    s += P.guguk(s, 1610, 414, 46)
    s += P.guguk(s, 1576, 418, 40)
    # çit
    for k in range(9):
        x = 1970 + k * 18
        s += f'<path d="M{x} 432 V392" stroke="#7A5A3A" stroke-width="5" stroke-linecap="round"/><path d="M{x - 3} 393 h6" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>'
    s += '<path d="M1966 402 H2130 M1966 420 H2130" stroke="#7A5A3A" stroke-width="4"/>'
    s += P.inek(1440, 440, 1.0, yon=1)
    s += P.inek(2040, 452, .9, yon=-1, renk="#8C3420")
    for i, (x, y) in enumerate([(1300, 446), (1336, 452), (1372, 444)]):
        s += P.kaz(x, y, 1.0, yon=1 if i % 2 else -1)
    s += P.kar_yagisi(1100, 0, 1000, 300, 30, 76, op=.6, rmax=2.4)
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ 3. DURAK · ANİ (ikindi, tüf taşı surlar)

def ani():
    s = Svg("kz-ani")
    ufuk = 288
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#4F7FC0"), (.42, "#A9C2DE"), (.76, "#F8D9A8"), (1, "#FFC886")])
    s += S.gunes(s, 230, 210, 40, hale="#FFC26B", hale_r=440, guc=.92)
    for i, (x, y, w) in enumerate([(640, 80, 230), (1020, 116, 260), (1460, 64, 240), (1860, 120, 180)]):
        s += S.bulut(s, x, y, w, 110 + i, ust="#FFF6E8", alt="#F2C9A0", op=.95)
    s += _uzak_daglar(s, ufuk, 111, renk=("#B98AA6", "#7E6296"), sis="#F4C4A8",
                      dag=[(900, 2200, 1700, 150, "tepe"), (380, 1240, 800, 190, "tepe")])
    # Arpaçay vadisi (sağda derin yarık)
    s += f'<path d="M1980 {ufuk + 4} C2010 {ufuk + 40} 2060 {ufuk + 70} 2100 {ufuk + 80} V{ufuk + 4} Z" fill="#7C6A80"/>'
    s += P.kar_zemin(s, 0, W, ufuk + 8, 112, ust="#FFF8F0", alt="#E8DDE6", dalga=6, n=8, golge="#D2C2D6")
    s += P.ani_sur(s, 1190, 2120, 396, 186, 113, isik=-1)
    s += P.kar_zemin(s, 0, W, 392, 114, ust="#FFFFFF", alt="#E4E2EE", dalga=5, n=8, golge="#CBBFD8")
    s += P.kirec_ocagi(s, 1385, 446, 92, 115)
    s += P.harc_teknesi(s, 1960, 452, 150)
    for i, x in enumerate((1880, 2060)):
        s += P.ciplak_agac(x, 400, 120 + i * 20, 116 + i, renk="#6A5446")
    s += S.marti(760, 220, .7, 2, renk="#5A4A70")
    s += S.marti(820, 240, .5, -1, renk="#5A4A70")
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ 4. DURAK · SARIKAMIŞ (akşam, sobalı oda + pencerede sarıçam ormanı)

def sarikamis():
    s = Svg("kz-sar")
    # duvar: sıcak ahşap kaplama
    g = s.lin([(0, "#D9A46C"), (1, "#A8703E")], 0, 0, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect width="{W}" height="{H}" fill="{g}"/>'
    for x in range(0, W, 70):
        s += f'<path d="M{x} 30 V400" stroke="#8C5A30" stroke-width="2.4" opacity=".55"/>'
    s += f'<rect y="0" width="{W}" height="30" fill="#6E4422"/><rect y="30" width="{W}" height="6" fill="#4A2E18"/>'
    # pencere: alacakaranlıkta karlı sarıçam ormanı ve Doğu Ekspresi
    wx, wy, ww, wh = 1240, 58, 420, 210
    pen = Svg("kz-sar-p")
    pen += S.gokyuzu(pen, wx, wy, ww, wh, "alaca")
    pen += S.yildizlar(pen, wx, wy, ww, wh * .4, 18, 41)
    pen += S.ay(pen, wx + ww * .8, wy + 40, 13, golge_renk="#43346F")
    pen += P.kar_zemin(pen, wx, wx + ww, wy + wh * .66, 42, ust="#DCE2F5", alt="#9FAACE", dalga=4, n=5, golge="#8E98C2")
    for i in range(11):
        x = wx + 12 + i * 40
        pen += P.cam(pen, x, wy + wh * .62 + (i % 3) * 3, 70 + (i % 4) * 14, 43 + i, renk="#1E4A3A", golge="#12302A")
    pen += P.tren(pen, wx + 30, wy + wh * .9, 380, n=3, govde="#2B50B5", serit="#F4F1EA", isik_pencere=True)
    pen += P.kar_yagisi(wx, wy, ww, wh, 46, 44, op=.85, rmax=2.6)
    s.defs += pen.defs
    kl = s.klip(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}"/>', ad="pk")
    s += f'<g clip-path="{kl}">{"".join(pen.parca)}</g>'
    s += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#5A3A20" stroke-width="14"/>'
    s += f'<path d="M{wx + ww / 2} {wy} V{wy + wh} M{wx} {wy + wh * .45} H{wx + ww}" stroke="#5A3A20" stroke-width="8"/>'
    s += f'<rect x="{wx - 24}" y="{wy + wh + 4}" width="{ww + 48}" height="14" fill="#7A4E2E"/>'
    s += f'<path d="M{wx + 6} {wy + wh - 6} q{ww * .25} -14 {ww * .5} -6 t{ww * .5 - 12} 0" stroke="#FFFFFF" stroke-width="8" fill="none" opacity=".9"/>'
    for sx, x0 in ((-1, wx - 62), (1, wx + ww + 8)):
        s += (f'<path d="M{x0} 46 h54 C{x0 + 54} 130 {x0 + 30 + sx * 8} 200 {x0 + 46} 272 L{x0 + 8} 272 C{x0 - 6} 200 {x0 + 8} 120 {x0} 46 Z" fill="#B23A2E"/>'
              f'<path d="M{x0 + 14} 54 C{x0 + 16} 130 {x0 + 10} 200 {x0 + 20} 266" stroke="#8E2A22" stroke-width="5" fill="none"/>'
              f'<path d="M{x0} 46 h54" stroke="#F0A21A" stroke-width="7"/>')
    # menfez ve CO dedektörü
    s += P.menfez(1748, 300, 64, 42)
    s += P.co_dedektoru(2030, 168, 64)
    s += f'<path d="M2030 196 v14" stroke="#4A2E18" stroke-width="2"/>'
    # zemin: ahşap döşeme + kilim
    s += f'<rect x="0" y="404" width="{W}" height="{H - 404}" fill="#7A4A26"/>'
    for x in range(-40, W, 90):
        s += f'<path d="M{x} {H} L{x + 30} 404" stroke="#5A3418" stroke-width="2" opacity=".6"/>'
    s += f'<path d="M1180 420 H1760 L1820 {H} H1120 Z" fill="#B23A2E"/>'
    for x in range(1200, 1760, 70):
        s += f'<path d="M{x} 428 l18 14 l-18 14 l-18 -14 Z" fill="#F0C14A"/><rect x="{x - 4}" y="438" width="8" height="8" fill="#253C78"/>'
    s += f'<path d="M1170 424 H1770 M1140 452 H1800" stroke="#253C78" stroke-width="5"/>'
    # soba, çaydanlık, odunluk
    s += P.soba(s, 1890, 416, 168)
    s += P.caydanlik(s, 1890, 254, 66)
    s += f'<path d="M1990 416 l14 -60 h60 l14 60 Z" fill="#8C5A2E" stroke="#4A2E18" stroke-width="3"/>'
    for k in range(4):
        s += f'<rect x="{2004 + k * 15}" y="{350 - (k % 2) * 6}" width="13" height="40" rx="5" fill="#A8743F" stroke="#5A3A20" stroke-width="2"/><circle cx="{2010 + k * 15}" cy="{350 - (k % 2) * 6}" r="5" fill="#E8C49A" stroke="#5A3A20" stroke-width="1.4"/>'
    s += '<use href="#pamuk-otur" x="1500" y="268" width="128" height="146"/>'
    sicak = s.rad([(0, "#FFB45A", .22), (1, "#FFB45A", 0)], 1890, 330, 700, kull="userSpaceOnUse", ad="sk")
    s += f'<rect width="{W}" height="{H}" fill="{sicak}"/>'
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ 5. DURAK · PASİNLER (öğle, kaplıca + Hasankale)

def pasinler():
    s = Svg("kz-pas")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gun")
    s += S.gunes(s, 250, 90, 34, hale="#FFF2C2", hale_r=300, guc=.8)
    for i, (x, y, w) in enumerate([(680, 120, 220), (1060, 80, 260), (1500, 110, 200)]):
        s += S.bulut(s, x, y, w, 130 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    s += _uzak_daglar(s, ufuk, 131, renk=("#5F84B8", "#3E5E96"), sis="#B8DCEE", kenar="#F4FAFF",
                      dag=[(800, 2240, 1560, 70, "sivri"), (-80, 900, 300, 190, "tepe")])
    s += P.kar_zemin(s, 0, W, ufuk + 6, 132, ust="#F6FAFE", alt="#D6E3F2", dalga=8, n=8)
    # Hasankale: tepede kale
    # Hasankale: kayalık tepede, bugün yer yer yıkık kale surları
    tepe = [(1470, 372), (1540, 318), (1620, 278), (1700, 262), (1800, 258), (1890, 270), (1980, 318), (2060, 372)]
    gt = s.lin([(0, "#9A8774"), (.55, "#7E6B5B"), (1, "#5F5046")], 0, 255, 0, 372, kull="userSpaceOnUse", ad="ht")
    s += f'<path d="{egri_d(tepe)} Z" fill="{gt}"/>'
    for (ax, ay, bx_, by_) in ((1560, 330, 1610, 300), (1700, 300, 1760, 290), (1880, 300, 1940, 330), (1640, 340, 1700, 326)):
        s += f'<path d="M{ax} {ay} L{bx_} {by_}" stroke="#4E4138" stroke-width="3" stroke-linecap="round" opacity=".55"/>'
    kar_t = [(1585, 300), (1640, 274), (1700, 262), (1800, 258), (1890, 270), (1950, 300), (1890, 288), (1800, 280), (1700, 284), (1640, 292)]
    s += f'<path d="{egri_d(kar_t)} Z" fill="#FFFFFF" opacity=".92"/>'
    s += P.ani_sur(s, 1630, 1920, 276, 92, 133, kirik=True, kum="#A99379", suslu=False, kapi=False, gedik_yer=(.36, .8))
    for i in range(6):
        x = 1460 + i * 52
        s += P.ev_tas(s, x, 372 + (i % 2) * 4, 40, 28, 140 + i, duvar=["#B8A792", "#A89C8E", "#C2B4A0"][i % 3], cati="#8E5A44", isik_pencere=i % 2 == 0)
    s += P.kar_zemin(s, 1100, W, 384, 134, ust="#FFFFFF", alt="#DCE7F4", dalga=5, n=6)
    s += P.kaplica_havuz(s, 1560, 432, 400, 84, 135)
    s += P.kaplica_havuz(s, 1960, 428, 230, 56, 136)
    for i, x in enumerate((1300, 1350, 2080)):
        s += P.ciplak_agac(x, 410, 130 + i * 15, 137 + i, renk="#6A5446")
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ 6. DURAK · ERZURUM (sabah, Taşhan + Palandöken)

def erzurum():
    s = Svg("kz-erz")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "safak")
    s += S.gunes(s, 1900, 160, 38, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=420, guc=.9)
    s += S.bulut_serit(s, 300, 190, 420, 10, "#FFE3EA", "#F6B8C8", .5)
    s += S.bulut(s, 1280, 110, 200, 150, ust="#FFFFFF", alt="#F6C8D0", op=.9)
    s += _uzak_daglar(s, ufuk + 40, 151, renk=("#A08ACB", "#6A58A4"), sis="#F0C6DA",
                      dag=[(700, 2240, 1520, 60, "sivri"), (-80, 900, 320, 170, "tepe")])
    s += P.kar_zemin(s, 0, W, ufuk + 40, 152, ust="#FBF6FA", alt="#DCDCEC", dalga=6, n=8, golge="#C8C4DE")
    # şehir: karlı damlar, sıcak pencereler
    for i in range(16):
        x = 1120 + i * 62
        hh = 34 + (i % 3) * 10
        s += P.ev_tas(s, x, 336 + (i % 2) * 5, 50, hh, 160 + i, duvar=["#C4B29A", "#B1A08C", "#D2C3AE"][i % 3], cati="#8E5A44", isik_pencere=i % 3 == 1)
    s += P.kar_zemin(s, 1100, W, 360, 153, ust="#FFFFFF", alt="#E2E2EF", dalga=4, n=6)
    s += P.tashan(s, 1380, 452, 560, 196, 154)
    s += P.pasli_kapi(s, 1990, 452, 104, 118, 155)
    s += f'<path d="M1980 452 V320 M2102 452 V320" stroke="#7A6A5A" stroke-width="12"/><rect x="1970" y="310" width="20" height="14" fill="#FFFFFF"/><rect x="2092" y="310" width="20" height="14" fill="#FFFFFF"/>'
    s += P.kar_yagisi(1100, 0, 1000, 340, 40, 156, op=.55, rmax=2.4)
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ HÜLASA · PALANDÖKEN ETEĞİ (b40)

def palandoken(h=400):
    s = Svg("kz-pal")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk, duraklar=[(0, "#3E86CC"), (.55, "#94CBEA"), (1, "#E9F6FA")])
    s += S.gunes(s, 330, 80, 32, hale="#FFF4CC", hale_r=300, guc=.8)
    for i, (x, y, w) in enumerate([(760, 110, 200), (1880, 80, 170)]):
        s += S.bulut(s, x, y, w, 170 + i, op=.95)
    d, sirt = S.dag(s, 640, 2240, ufuk + 60, 1440, 24, 171, renk="#5F84B8", golge="#3E5E96", bicim="sivri", kar_y=ufuk - 90,
                    kar="#FFFFFF", kar_golge="#A9BCE6", sis="#B8DCEE", isik=-1, sirt=6, puruz=12, kenar_isik="#F2F8FF")
    s += d
    # kayak pistleri: ormanın içinden inen beyaz şeritler
    s += P.kar_zemin(s, 0, W, ufuk + 40, 172, ust="#FFFFFF", alt="#D8E5F4", dalga=10, n=8)
    r = RNG(173)
    for i in range(46):
        x = 900 + i * 27 + r.uniform(-8, 8)
        if 1330 < x < 1400 or 1690 < x < 1760:
            continue
        y = ufuk + 80 + r.uniform(-6, 26)
        s += P.cam(s, x, y, 54 + r.uniform(0, 26), 174 + i, renk="#2F6B4C")
    for x0, x1 in ((1330, 1400), (1690, 1760)):
        s += f'<path d="M{x0 + 22} {ufuk + 40} C{x0 + 6} {ufuk + 70} {x0 + 40} {ufuk + 95} {x0} {ufuk + 128} L{x1} {ufuk + 128} C{x1 + 30} {ufuk + 95} {x1 - 6} {ufuk + 70} {x1 - 14} {ufuk + 40} Z" fill="#FFFFFF"/>'
    s += P.telesiyej(1420, ufuk + 110, 1980, ufuk - 40, 9, 175, direk=4)
    s += P.kar_zemin(s, 1100, W, ufuk + 112, 176, ust="#FFFFFF", alt="#E0EAF6", dalga=6, n=6)
    # dağ evi (konaklama)
    s += P.ev_tas(s, 1560, h - 26, 220, 84, 177, duvar="#A8743F", cati="#7A3A2E", isik_pencere=True)
    s += P.ev_tas(s, 1800, h - 20, 120, 60, 178, duvar="#B8834E", cati="#7A3A2E", isik_pencere=True)
    for i, x in enumerate((1500, 1530, 1960, 2000)):
        s += P.cam(s, x, h - 18, 70 + (i % 2) * 18, 190 + i, renk="#2F6B4C")
    s += P.kar_yagisi(1000, 0, 1100, h, 40, 179, op=.6, rmax=2.4)
    s += _cerceve(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ MECLİS · DOĞU EKSPRESİ KOMPARTIMANI (iç mekân)

def tren_ici():
    from cizim.sus import kilim_serit
    s = Svg("kz-tre")
    g = s.lin([(0, "#C98E5A"), (1, "#9C6438")], 0, 0, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect width="{W}" height="{H}" fill="{g}"/>'
    for x in range(0, W, 90):
        s += f'<path d="M{x} 0 V{H}" stroke="#86562E" stroke-width="2" opacity=".5"/>'
    # pencere: karlı yayla, telgraf direkleri, donmuş dere
    wx, wy, ww, wh = 1300, 46, 560, 210
    pen = Svg("kz-tre-p")
    pen += S.gokyuzu(pen, wx, wy, ww, wh, "gun")
    pen += S.bulut(pen, wx + 120, wy + 60, 150, 201, op=.95)
    pd, _ = S.dag(pen, wx - 60, wx + ww + 60, wy + wh * .58, wx + ww * .62, wy + 28, 202, renk="#7C93B5", golge="#55709A",
                  bicim="sivri", kar_y=wy + wh * .5, kar="#FFFFFF", kar_golge="#C9D8EE", sis="#C4E2EE", isik=-1, sirt=4, puruz=8)
    pen += pd
    pen += P.kar_zemin(pen, wx, wx + ww, wy + wh * .58, 203, ust="#FFFFFF", alt="#D6E3F2", dalga=4, n=6)
    pen += f'<path d="M{wx} {wy + wh * .82} C{wx + 160} {wy + wh * .76} {wx + 320} {wy + wh * .9} {wx + ww} {wy + wh * .8} L{wx + ww} {wy + wh * .86} C{wx + 320} {wy + wh * .96} {wx + 160} {wy + wh * .82} {wx} {wy + wh * .88} Z" fill="#A9D8E8"/>'
    for k in range(5):
        px = wx + 40 + k * 120
        pen += f'<path d="M{px} {wy + wh * .7} V{wy + wh * .4} M{px - 10} {wy + wh * .44} h20" stroke="#5A4A3E" stroke-width="3"/>'
    pen += f'<path d="M{wx} {wy + wh * .42} Q{wx + 60} {wy + wh * .47} {wx + 120} {wy + wh * .42} T{wx + 240} {wy + wh * .42} T{wx + 360} {wy + wh * .42} T{wx + 480} {wy + wh * .42} T{wx + 600} {wy + wh * .42}" stroke="#3A3A3A" stroke-width="1.4" fill="none"/>'
    for i in range(8):
        pen += P.cam(pen, wx + 30 + i * 74, wy + wh * .66, 40 + (i % 3) * 8, 204 + i, renk="#2F6B4C")
    s.defs += pen.defs
    kl = s.klip(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="22"/>', ad="pk")
    s += f'<g clip-path="{kl}">{"".join(pen.parca)}</g>'
    s += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="22" fill="none" stroke="#3A3C46" stroke-width="16"/>'
    s += f'<path d="M{wx + 8} {wy + wh * .3} H{wx + ww - 8}" stroke="#3A3C46" stroke-width="6"/>'
    # perde, bagaj rafı
    for x0 in (wx - 40, wx + ww - 16):
        s += f'<path d="M{x0} 34 h56 C{x0 + 54} 110 {x0 + 34} 190 {x0 + 46} 262 L{x0 + 10} 262 C{x0} 190 {x0 + 8} 110 {x0} 34 Z" fill="#253C78"/><path d="M{x0} 34 h56" stroke="#F0A21A" stroke-width="6"/>'
    s += f'<path d="M1100 20 H2100 M1100 34 H2100" stroke="#C9CED6" stroke-width="5"/>'
    s += f'<rect x="1780" y="-10" width="150" height="40" rx="6" fill="#8C3A2E" stroke="#4A1A12" stroke-width="3"/><rect x="1160" y="-6" width="110" height="34" rx="6" fill="#2B50B5" stroke="#1B3584" stroke-width="3"/>'
    # koltuklar (kilim desenli)
    s += f'<rect x="0" y="300" width="{W}" height="{H - 300}" fill="#6E2A22"/>'
    kil = kilim_serit("kz-tre-k", 2100, 60).replace("<svg ", '<svg width="2100" height="60" ')
    s += f'<g transform="translate(0 306)">{kil}</g>'
    s += f'<rect x="0" y="366" width="{W}" height="{H - 366}" fill="#8E2A22"/>'
    for x in range(40, W, 80):
        s += f'<path d="M{x} 380 l16 14 l-16 14 l-16 -14 Z" fill="#D99A2B"/>'
    # katlanır masa + çay
    s += f'<path d="M1440 290 H1720 L1700 304 H1460 Z" fill="#8C5A2E" stroke="#4A2E18" stroke-width="3"/>'
    for k, x in enumerate((1480, 1520, 1660)):
        s += Y.cay_bardak_kucuk(x, 290, 28)
    s += f'<ellipse cx="1590" cy="284" rx="34" ry="10" fill="#C88A3A" stroke="#7A4E1E" stroke-width="3"/><ellipse cx="1590" cy="282" rx="18" ry="5" fill="#8E2A22" opacity=".25"/>'
    for k in range(8):
        a = k * math.pi / 4
        s += f'<circle cx="{f(1590 + 26 * math.cos(a))}" cy="{f(282 + 7 * math.sin(a))}" r="2" fill="#F4E2B8"/>'
    s += '<use href="#elif-soru" x="1275" y="190" width="250" height="262"/>'
    s += '<use href="#yusuf-anlatan" x="1820" y="190" width="250" height="262"/>'
    s += '<use href="#pamuk-dusunen" x="1570" y="214" width="150" height="172"/>'
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ KISSA · ÇOBANDEDE KÖPRÜSÜ (Aras üstünde)

def cobandede():
    s = Svg("kz-cob")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "altin")
    s += S.gunes(s, 300, 170, 36, hale="#FFE0A0", hale_r=380, guc=.88)
    for i, (x, y, w) in enumerate([(760, 110, 230), (1200, 70, 220), (1700, 120, 200)]):
        s += S.bulut(s, x, y, w, 210 + i, ust="#FFFFFF", alt="#F5D9B5", op=.95)
    uzak = _uzak_daglar(s, ufuk, 211, renk=("#A886A8", "#765E92"), sis="#F2CCAE",
                        dag=[(900, 2240, 1580, 110, "sivri"), (-80, 1000, 420, 160, "tepe")])
    s += uzak
    s += P.kar_zemin(s, 0, W, ufuk + 6, 212, ust="#FFF8EE", alt="#E8E0E6", dalga=6, n=8)
    # Aras: geniş ırmak, kenarlarda buz
    su = s.lin([(0, "#BFE6EC"), (.3, "#4FAFB4"), (1, "#16697A")], 0, 360, 0, H, kull="userSpaceOnUse", ad="ar")
    s += f'<path d="M0 372 C500 360 1100 380 1500 366 C1800 356 2000 368 2100 362 V{H} H0 Z" fill="{su}"/>'
    kopru = P.tas_kopru(s, 1060, 2080, 382, 132, [(1150, 80, 62), (1270, 96, 78), (1410, 112, 92), (1590, 160, 122), (1770, 112, 92), (1905, 96, 78), (2025, 74, 58)], tas="#C2AC8C")
    s += S.yansima(s, kopru, 382, 1000, 1100, 80, op=.25)
    s += kopru
    s += S.dalga_cizgileri(0, 392, 2100, 60, 213, n=36, op=.65)
    s += f'<path d="M0 372 C300 366 600 372 900 368 L880 380 C600 386 300 380 0 386 Z" fill="#FFFFFF" opacity=".85"/>'
    for i, (x, h) in enumerate([(980, 150), (1020, 120), (2050, 140)]):
        s += P.ciplak_agac(x, 362, h, 214 + i, renk="#6A5446")
    s += S.marti(820, 210, .7, 2, renk="#5A4A70")
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ ANAHTAR · KARS GARI (gün batımı)

def kars_gari():
    s = Svg("kz-gar")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#3A4C9C"), (.4, "#8E7BC0"), (.72, "#F7A6A0"), (1, "#FFD39A")])
    s += S.gunes(s, 1200, 250, 38, hale="#FFC27A", hale_r=380, guc=.9)
    s += S.bulut_serit(s, 1100, 150, 520, 14, "#FFD0C4", "#F28FA0", .7)
    s += S.bulut_serit(s, 1500, 96, 480, 12, "#FFC9B8", "#E9849C", .6)
    s += _uzak_daglar(s, ufuk, 221, renk=("#9A7AB0", "#6A4E8E"), sis="#F4A8A0", dag=[(-80, 1000, 420, 190, "tepe"), (1300, 2240, 1800, 160, "tepe")])
    s += P.kar_zemin(s, 0, W, ufuk + 4, 222, ust="#FCEEF0", alt="#D8D2E8", dalga=6, n=8, golge="#C2BAD8")
    s += P.istasyon(s, 1360, 392, 560, 150, 223)
    # peron, lambalar, merdiven
    s += f'<rect x="1080" y="392" width="1020" height="18" fill="#9A8F86" stroke="#5E5650" stroke-width="2"/><path d="M1080 392 H2100" stroke="#FFFFFF" stroke-width="5"/>'
    for x in (1240, 1960):
        isik = s.rad([(0, "#FFE7A8", .8), (1, "#FFE7A8", 0)], x, 300, 70, kull="userSpaceOnUse", ad="lm")
        s += f'<circle cx="{x}" cy="300" r="70" fill="{isik}"/><path d="M{x} 392 V300" stroke="#2A2C34" stroke-width="6"/><rect x="{x - 12}" y="288" width="24" height="20" rx="4" fill="#FFE7A8" stroke="#2A2C34" stroke-width="3"/>'
    s += P.tren(s, 1100, 452, 940, n=4, govde="#C8442F", serit="#F4F1EA", isik_pencere=True)
    for k in range(4):
        s += f'<rect x="{2000 + k * 22}" y="{410 + k * 12}" width="80" height="12" fill="#B8A792" stroke="#5E5650" stroke-width="2"/>'
    s += P.kar_yagisi(1000, 0, 1100, 400, 60, 224, op=.75, rmax=2.6)
    s += _cerceve(s)
    return _bitir(s)


# ------------------------------------------------------------------ BÜYÜK İMTİHAN 1 · KARS KALESİ (b62)

def kars_kalesi(h=620):
    s = Svg("kz-kal")
    ufuk = 420
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#2F5DA8"), (.38, "#86A9D6"), (.7, "#F6C99A"), (1, "#FFB46B")])
    s += S.gunes(s, 240, 330, 50, hale="#FFB45A", hale_r=520, guc=.95)
    for i, (x, y, w) in enumerate([(540, 150, 300), (980, 96, 340), (1500, 140, 280), (1860, 70, 220)]):
        s += S.bulut(s, x, y, w, 230 + i, ust="#FFF4E4", alt="#F0A98A", op=.95)
    s += S.bulut_serit(s, 300, 250, 600, 16, "#FFD8B0", "#F08A7A", .6)
    s += _uzak_daglar(s, ufuk, 231, renk=("#B08AA8", "#7A5888"), sis="#F4B8A0",
                      dag=[(1100, 2240, 1760, 230, "sivri"), (-80, 900, 360, 300, "tepe")])
    s += P.kar_zemin(s, 0, W, ufuk + 4, 232, ust="#FFF1EA", alt="#E6D6E2", dalga=8, n=8, golge="#D2BCD2")
    kale, _ = P.bazalt_kale(s, 980, 2130, 540, 380, 233, bayrak=True)
    s += kale
    # Kars Çayı + Taşköprü + taş evler
    su = s.lin([(0, "#F6C9A8"), (.4, "#5FA8B4"), (1, "#1B5A6E")], 0, 548, 0, h, kull="userSpaceOnUse", ad="kc")
    s += f'<path d="M0 556 C600 548 1200 560 2100 548 V{h} H0 Z" fill="{su}"/>'
    kopru = P.tas_kopru(s, 1080, 1420, 560, 56, [(1140, 70, 42), (1250, 86, 50), (1360, 70, 42)], tas="#5A5E6A")
    s += S.yansima(s, kopru, 560, 1000, 500, 60, op=.25)
    s += kopru
    for i in range(9):
        x = 1460 + i * 70
        s += P.ev_tas(s, x, 552 - (i % 2) * 4, 56, 40 + (i % 3) * 6, 240 + i, duvar=["#6E7380", "#7C8290", "#5E6370"][i % 3], cati="#8C99A6", isik_pencere=i % 2 == 0)
    for i, x in enumerate((1020, 1060, 2020, 2070)):
        s += P.ciplak_agac(x, 552, 130 + (i % 2) * 30, 250 + i, renk="#5A4636")
    s += S.dalga_cizgileri(0, 566, 2100, 50, 234, n=40, op=.6)
    s += S.tekne(s, 520, 600, 70, govde="#2B50B5", ust="#F4E9D8")
    for k, (x, y, o) in enumerate([(820, 200, 1.0), (900, 230, .7), (1300, 110, .6)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += P.kar_yagisi(900, 0, 1200, 560, 70, 235, op=.7, rmax=2.8)
    s += _cerceve(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ BÜYÜK İMTİHAN 2 · KALE KAPISI (bazalt, b30)

def kale_kapi_bazalt(h=300):
    s = Svg("kz-kap")
    s += S.gokyuzu(s, 0, 0, W, h, duraklar=[(0, "#F7B07A"), (1, "#FFE1B0")])
    g = s.lin([(0, "#6A6E7C"), (1, "#3A3C46")], 0, 40, 0, h, kull="userSpaceOnUse", ad="sd")
    s += f'<rect x="0" y="60" width="{W}" height="{h - 60}" fill="{g}"/>'
    r = RNG(260)
    for row in range(8):
        y = 60 + row * 32
        off = 0 if row % 2 == 0 else 40
        for x in range(-40 + off, W, 80):
            s += f'<rect x="{x + 2}" y="{y + 2}" width="76" height="28" rx="4" fill="{karis("#6A6E7C", "#3E414C", r.uniform(0, .7))}" stroke="#2A2C34" stroke-width="1.6"/>'
    for x in range(0, W, 110):
        s += f'<rect x="{x}" y="20" width="70" height="44" fill="#5E6270" stroke="#2A2C34" stroke-width="2.4"/><rect x="{x - 2}" y="16" width="74" height="8" rx="4" fill="#FFFFFF"/>'
    s += f'<rect x="0" y="58" width="{W}" height="10" fill="#2E3038"/>'
    cx, ky = 1450, h
    s += f'<path d="M{cx - 170} {ky} V140 Q{cx - 170} 70 {cx} 52 Q{cx + 170} 70 {cx + 170} 140 V{ky} Z" fill="#4A4C58"/>'
    s += f'<path d="M{cx - 140} {ky} V146 Q{cx - 140} 92 {cx} 78 Q{cx + 140} 92 {cx + 140} 146 V{ky} Z" fill="#1E1A16"/>'
    isik = s.rad([(0, "#FFF4C8", .95), (.5, "#FFD27A", .5), (1, "#FFD27A", 0)], cx, 200, 260, kull="userSpaceOnUse", ad="ki")
    s += f'<path d="M{cx - 30} {ky} V96 L{cx + 30} 96 V{ky} Z" fill="#FFE9A8"/>'
    s += f'<path d="M{cx - 30} {ky} L{cx - 400} {ky} L{cx - 30} 120 Z M{cx + 30} {ky} L{cx + 400} {ky} L{cx + 30} 120 Z" fill="#FFE9A8" opacity=".3"/>'
    s += f'<circle cx="{cx}" cy="200" r="260" fill="{isik}"/>'
    for sx in (-1, 1):
        x0, x1 = cx + sx * 30, cx + sx * 132
        s += f'<path d="M{x0} {ky} V100 Q{(x0 + x1) / 2} 84 {x1} 128 V{ky} Z" fill="#6E4422" stroke="#2A1A10" stroke-width="4"/>'
        for k in range(4):
            yy = 140 + k * 40
            s += f'<path d="M{x0} {yy} H{x1}" stroke="#2A1A10" stroke-width="5"/>'
            for j in range(3):
                s += f'<circle cx="{x0 + sx * (24 + j * 34)}" cy="{yy}" r="4" fill="#C9A86A"/>'
    for x in (cx - 230, cx + 230):
        s += f'<rect x="{x - 6}" y="130" width="12" height="60" fill="#2A1A10"/>'
        alev = s.rad([(0, "#FFF4C8"), (.5, "#FFB43A"), (1, "#E2533D", .0)], x, 112, 60, kull="userSpaceOnUse", ad="al")
        s += f'<circle cx="{x}" cy="112" r="60" fill="{alev}"/><path d="M{x - 12} 130 Q{x - 14} 104 {x} 86 Q{x + 14} 104 {x + 12} 130 Z" fill="#FF8A3D"/><path d="M{x - 6} 130 Q{x - 6} 112 {x} 100 Q{x + 6} 112 {x + 6} 130 Z" fill="#FFE08A"/>'
    for k, (x, c) in enumerate(((760, "#B23A2E"), (2000, "#13A3A6"))):
        s += f'<path d="M{x - 60} 70 H{x + 60} V230 L{x} 270 L{x - 60} 230 Z" fill="{c}" stroke="#2A1A10" stroke-width="3"/>'
        s += f'<path d="M{x - 60} 82 H{x + 60}" stroke="{ALTIN}" stroke-width="6"/>'
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x, 160, 40), True)}" fill="{ALTIN}" stroke="#2A1A10" stroke-width="2"/>'
        s += f'<circle cx="{x}" cy="160" r="14" fill="{c}"/>'
    for k in range(4):
        s += f'<rect x="{cx - 220 - k * 30}" y="{h - 14 - k * 14}" width="{440 + k * 60}" height="16" fill="#8E929E" stroke="#3A3C46" stroke-width="2" transform="translate(0 {k * 14})"/>'
    s += f'<path d="M{cx - 260} {h - 2} q60 -10 120 -4 t120 0 t120 -2 t120 4" fill="#FFFFFF" opacity=".9"/>'
    s += P.kar_yagisi(0, 0, W, h, 70, 261, op=.8, rmax=2.4)
    s += '<use href="#pamuk-akce" x="1680" y="128" width="150" height="171"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ CEVAPLAR · KARS'TA GECE (b36)

def kars_gece(h=360):
    s = Svg("kz-gec")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 30, 150, 270)
    s += S.ay(s, 1240, 80, 32, golge_renk="#13204A")
    d, _ = S.dag(s, -60, 900, ufuk, 320, 120, 271, renk="#283565", golge="#1C2650", bicim="tepe", kar_y=150, kar="#C8D2F0", kar_golge="#8F9CC8", isik=1, sirt=2, puruz=5)
    s += d
    kale, _ = P.bazalt_kale(s, 1380, 2120, ufuk + 40, 220, 272, bayrak=True, gece=True)
    isik = s.rad([(0, "#FFD27A", .35), (1, "#FFD27A", 0)], 1750, ufuk - 40, 420, kull="userSpaceOnUse", ad="pj")
    s += f'<circle cx="1750" cy="{ufuk - 40}" r="420" fill="{isik}"/>'
    s += kale
    s += P.kar_zemin(s, 0, W, ufuk + 34, 273, ust="#B8C4E8", alt="#5A6A9E", dalga=6, n=8, golge="#4A5A8E")
    r = RNG(274)
    for k in range(60):
        x = 900 + r.uniform(0, 1150)
        y = ufuk + 40 + r.uniform(0, 60)
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(4, 8))}" height="{f(r.uniform(4, 7))}" fill="#FFD27A" opacity="{f(r.uniform(.6, 1), 2)}"/>'
    su = s.lin([(0, "#2C4A85"), (1, "#0B1636")], 0, h - 50, 0, h, kull="userSpaceOnUse", ad="su")
    s += f'<rect x="0" y="{h - 46}" width="{W}" height="46" fill="{su}"/>'
    for k in range(30):
        x = 1300 + r.uniform(0, 700)
        s += f'<path d="M{f(x)} {f(h - 40 + r.uniform(0, 34))} h{f(r.uniform(10, 40))}" stroke="#FFD27A" stroke-width="2" opacity="{f(r.uniform(.3, .7), 2)}"/>'
    s += P.kar_yagisi(0, 0, W, h, 110, 275, op=.8, rmax=2.6)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ FİNAL · KARS KALESİ BURCU (gün batımı)

def final_kars(h=900, nisanlar=None):
    s = Svg("kz-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    gx, gy = 760, ufuk - 30
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE0A0" opacity=".12"/>'
    s += S.gunes(s, gx, gy, 70, hale="#FFC56B", hale_r=700, guc=.95)
    for (x, y, w, k) in ((200, 260, 520, 22), (1200, 180, 640, 26), (1500, 330, 480, 16), (100, 420, 380, 12)):
        s += S.bulut_serit(s, x, y, w, k, "#FFC59A", "#FF6F8A", .75)
    s += _uzak_daglar(s, ufuk, 281, renk=("#C47AA0", "#6E4C8A"), sis="#FF8E84",
                      dag=[(980, 1900, 1400, 300, "sivri"), (-100, 760, 300, 420, "tepe"), (1750, 2300, 2050, 410, "tepe")])
    s += P.kar_zemin(s, 0, W, ufuk + 4, 282, ust="#FFD9D2", alt="#C89AB8", dalga=8, n=8, golge="#B888AE")
    for i in range(10):
        x = 120 + i * 120
        s += P.ev_tas(s, x, ufuk + 60 + (i % 2) * 6, 70, 46, 290 + i, duvar=["#7C6E86", "#6E6680"][i % 2], cati="#8C7A98", isik_pencere=True)
    for k, (x, y, o) in enumerate([(560, 200, 1.4), (640, 240, 1.0), (1100, 120, .8), (1180, 150, .6), (300, 160, .7)]):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    # bazalt burç (ön plan)
    g = s.lin([(0, "#6E7280"), (1, "#3A3C46")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    s += f'<rect x="0" y="720" width="{W}" height="{h - 720}" fill="{g}"/>'
    r = RNG(283)
    for row in range(6):
        y = 724 + row * 30
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            s += f'<rect x="{x + 2}" y="{y}" width="86" height="27" rx="3" fill="{karis("#6E7280", "#40434E", r.uniform(0, .7))}" stroke="#2A2C34" stroke-width="1.6"/>'
    for x in range(0, W, 150):
        s += f'<rect x="{x}" y="660" width="96" height="64" fill="#5E6270" stroke="#2A2C34" stroke-width="2.6"/><rect x="{x - 3}" y="652" width="102" height="14" rx="6" fill="#FFFFFF"/>'
    s.tanim(f'<linearGradient id="{s.onek}-tk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7C8090"/><stop offset=".6" stop-color="#5A5E6A"/><stop offset="1" stop-color="#3A3C46"/></linearGradient>')
    s += f'<rect x="1560" y="560" width="420" height="{h - 560}" fill="url(#{s.onek}-tk)" stroke="#2A2C34" stroke-width="3"/>'
    for x in range(1560, 1980, 84):
        s += f'<rect x="{x}" y="510" width="54" height="56" fill="#6A6E7C" stroke="#2A2C34" stroke-width="2.6"/><rect x="{x - 3}" y="504" width="60" height="12" rx="6" fill="#FFFFFF"/>'
    s += f'<path d="M1740 {h} V760 Q1740 720 1770 712 Q1800 720 1800 760 V{h} Z" fill="#2A1A10"/>'
    s += '<use href="#pamuk-bayrak" x="1600" y="150" width="340" height="400"/>'
    s += f'<path d="M260 650 V330" stroke="#6B4A2E" stroke-width="10"/><circle cx="260" cy="324" r="10" fill="{ALTIN}"/>'
    s += f'<path d="M260 360 Q900 520 1640 330" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .6) / (len(nisanlar) + .2)
            x = (1 - t) ** 2 * 260 + 2 * (1 - t) * t * 900 + t * t * 1640
            y = (1 - t) ** 2 * 360 + 2 * (1 - t) * t * 520 + t * t * 330
            s += f'<path d="M{f(x)} {f(y)} v18" stroke="#5A3A22" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 52)} {f(y + 14)}) rotate({f((k % 2 * 2 - 1) * 5)} 52 60) scale(.84)">{ns}</g>'
    for k in range(60):
        x = r.uniform(300, 1900)
        y = r.uniform(80, 640)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    s += P.kar_yagisi(0, 0, W, h, 80, 284, op=.6, rmax=3)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ AÇILIŞ · KARS–ERZURUM PANORAMASI + TUR ROTASI

# Stilize tur haritası (temsilî): batıda Erzurum, doğuda Kars ve Ani, kuzeyde Çıldır Gölü. Ana yol (duraklar) ortadan,
# Doğu Ekspresi demiryolu (yan yollar) alttan Kars'a döner. Konumlar panorama birimidir (2100×1100).
DURAKLAR = [  # (anahtar, x, y, tür)
    ("1", 1450, 470, "durak"), ("2", 1470, 612, "durak"), ("3", 1925, 640, "durak"), ("4", 1080, 668, "durak"),
    ("5", 690, 704, "durak"), ("6", 330, 740, "durak"), ("H", 205, 905, "hulasa"), ("M", 560, 935, "yan"),
    ("K", 905, 895, "yan"), ("A", 1400, 915, "yan"), ("V", 1675, 812, "kale"),
]
ROTA_ARA = {("2", "3"): [(1700, 600)], ("3", "4"): [(1820, 730), (1520, 728), (1260, 700)], ("4", "5"): [(880, 700)],
            ("5", "6"): [(500, 730)], ("6", "H"): [(250, 820)], ("H", "M"): [(380, 965)], ("M", "K"): [(740, 935)],
            ("K", "A"): [(1150, 935)], ("A", "V"): [(1550, 890)]}


def panorama_kars(h=1100):
    s = Svg("kz-pan")
    ufuk = 330
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    gx, gy = 1880, ufuk - 60
    for k in range(12):
        a0 = math.pi + .1 + k * (math.pi - .2) / 12
        a1 = a0 + .05
        s += f'<path d="M{gx} {gy} L{f(gx + 2400 * math.cos(a0))} {f(gy + 2400 * math.sin(a0))} L{f(gx + 2400 * math.cos(a1))} {f(gy + 2400 * math.sin(a1))} Z" fill="#FFF0D0" opacity=".08"/>'
    s += S.gunes(s, gx, gy, 48, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=600, guc=.95)
    for (x, y, w_, k) in ((520, 150, 520, 18), (1120, 96, 600, 22), (1560, 200, 420, 14), (80, 230, 360, 12)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFE3EA", "#F6B0C4", .7)
    uzak = _uzak_daglar(s, ufuk + 8, 301, renk=("#A78CCE", "#6C5AA8"), sis="#F2C2D8",
                        dag=[(-120, 820, 330, 150, "tepe"), (560, 1560, 1050, 96, "sivri"), (1300, 2260, 1760, 140, "tepe")])
    s += uzak
    # karlı yayla (bütün zemin): ufukta gün doğumu pembesi, ortada lavanta gölgeler, önde mavi
    gk = s.lin([(0, "#F4C6D6"), (.12, "#EED8EC"), (.45, "#DCE4F6"), (1, "#B9CDEA")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kara")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    r = RNG(302)
    # orta plan tepe sıraları (derinlik)
    for i, (yy, genlik, c1, c2) in enumerate(((ufuk + 30, 26, "#D9B8DA", "#E8D2E6"), (ufuk + 80, 30, "#C8C2E6", "#DDE0F4"), (ufuk + 150, 26, "#BFD0EE", "#D6E2F4"))):
        tb, _ = S.tepe_bandi(s, 0, W, yy, genlik, 303 + i, c1, c2, dalga=6, olcek=40)
        s += tb
    for k in range(70):
        x = r.uniform(0, W)
        y = r.uniform(ufuk + 60, h)
        sc = .4 + (y - ufuk) / (h - ufuk)
        w_ = r.uniform(80, 220) * sc
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w_)}" ry="{f(w_ * .08)}" fill="{r.choice(["#A9BEE0", "#BCC8EA", "#D8C4E0"])}" opacity=".45"/>'
    # Çıldır Gölü (kuzeyde, buz tutmuş)
    cx, cy = 1470, 455
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="250" ry="52" fill="#9CC6E4" stroke="#FFFFFF" stroke-width="6"/>'
    s += f'<ellipse cx="{cx - 20}" cy="{cy - 6}" rx="200" ry="34" fill="#D2E6F6"/>'
    for k in range(6):
        x0 = cx - 180 + k * 60
        s += f'<path d="M{x0} {cy + r.uniform(-20, 20)} l{r.uniform(20, 40)} {r.uniform(-6, 6)} l{r.uniform(20, 30)} {r.uniform(-6, 6)}" stroke="#6E98C2" stroke-width="2" fill="none"/>'
    s += P.at_kizak(s, cx + 150, cy + 20, .3, yolcu=False)
    # ırmaklar: Aras (güney), Kars Çayı, Arpaçay (doğu sınırı)
    aras = [(0, 1020), (300, 990), (620, 1010), (880, 975), (1180, 1000), (1500, 980), (1820, 1010), (2100, 990)]
    s += f'<path d="{egri_d(aras)}" fill="none" stroke="#2E8CA6" stroke-width="24" stroke-linecap="round" opacity=".8"/><path d="{egri_d(aras)}" fill="none" stroke="#8ED6E4" stroke-width="9" stroke-linecap="round"/>'
    arpa = [(2000, 380), (1990, 520), (2030, 660), (2010, 800), (2060, 980)]
    s += f'<path d="{egri_d(arpa)}" fill="none" stroke="#2E8CA6" stroke-width="13" stroke-linecap="round" opacity=".8"/><path d="{egri_d(arpa)}" fill="none" stroke="#8ED6E4" stroke-width="5" stroke-linecap="round"/>'
    karscay = [(1300, 560), (1500, 700), (1640, 760), (1760, 820)]
    s += f'<path d="{egri_d(karscay)}" fill="none" stroke="#3E9CB4" stroke-width="9" stroke-linecap="round" opacity=".85"/>'
    # sarıçam ormanları: Sarıkamış çevresinde koyu yeşil kütle, kuzeyde Allahuekber eteklerinde şerit
    orman = [(860, 1360, 560, 860, 120), (520, 900, 420, 560, 50), (1600, 1900, 400, 520, 24), (60, 300, 430, 600, 22)]
    for oi, (xa, xb, ya, yb, n_) in enumerate(orman):
        for k in range(n_):
            x = r.uniform(xa, xb)
            y = r.uniform(ya, yb)
            if any(math.hypot(x - a, y - b) < 64 for _, a, b, _t in DURAKLAR):
                continue
            sc = .5 + (y - ufuk) / (h - ufuk) * .8
            s += P.cam(s, x, y, r.uniform(50, 74) * sc, 310 + oi * 200 + k, renk=r.choice(["#2F6B4C", "#245A40", "#3A7653"]))
    for k in range(26):
        x = r.uniform(40, 2060)
        y = r.uniform(ufuk + 60, h - 60)
        if any(math.hypot(x - a, y - b) < 110 for _, a, b, _t in DURAKLAR) or (820 < x < 1400 and 540 < y < 880):
            continue
        sc = .45 + (y - ufuk) / (h - ufuk) * .8
        for j in range(3):
            s += P.cam(s, x + j * 20 * sc, y + (j % 2) * 4, 52 * sc, 900 + k * 3 + j, renk="#2F6B4C")
    # köyler (kırmızı damlı, sıcak renk)
    for k, (vx, vy) in enumerate(((620, 520), (1180, 470), (300, 600), (880, 800), (1820, 900))):
        for j in range(4):
            s += P.ev_tas(s, vx + j * 30, vy + (j % 2) * 5, 24, 16, 1000 + k * 4 + j, duvar=["#C9B49A", "#B8A08C"][j % 2], cati="#B8553A", baca=False)
    # simge yapılar
    s += P.ani_sur(s, 1820, 2040, 596, 60, 321, kirik=True)
    kale, _ = P.bazalt_kale(s, 1560, 1790, 790, 118, 322, bayrak=True)
    s += kale
    for i in range(6):
        s += P.ev_tas(s, 1500 + i * 34, 640 + (i % 2) * 6, 26, 18, 330 + i, duvar=["#9AA0A8", "#A89C8E"][i % 2], cati="#7C8A98", baca=False)
    s += P.mandira(s, 1520, 586, 110, 48, 340)
    s += P.telesiyej(1120, 640, 1260, 560, 3, 341, direk=2)
    s += P.kaplica_havuz(s, 760, 680, 110, 26, 342)
    s += P.buhar(s, 760, 660, 90, 343, op=.7, en=1.2)
    for i in range(6):
        s += P.ev_tas(s, 250 + i * 36, 724 + (i % 2) * 6, 30, 22, 350 + i, duvar=["#C4B29A", "#B1A08C"][i % 2], cati="#8E5A44", baca=False)
    # Palandöken (önde, sol alt): karlı kayak tepesi
    d, _ = S.dag(s, 20, 380, 1000, 210, 820, 357, renk="#8199BB", golge="#5A74A0", bicim="sivri", kar_y=880, kar="#FFFFFF",
                 kar_golge="#C6D6EE", isik=-1, sirt=3, puruz=8)
    s += d
    s += P.tas_kopru(s, 840, 980, 992, 26, [(880, 30, 18), (920, 36, 22), (960, 30, 18)], tas="#C2AC8C", kar=True)
    # Doğu Ekspresi demiryolu (alt yol) + tren
    ray = [(330, 760), (300, 860), (420, 975), (740, 945), (1150, 945), (1420, 925), (1560, 880), (1640, 830)]
    rd = egri_d(ray)
    s += f'<path d="{rd}" fill="none" stroke="#5A4A3E" stroke-width="12" stroke-linecap="round"/>'
    s += f'<path d="{rd}" fill="none" stroke="#C8B8A6" stroke-width="7" stroke-dasharray="3 9" stroke-linecap="butt"/>'
    s += P.tren(s, 1120, 958, 210, n=2, govde="#C8442F", isik_pencere=False)
    # rota (ana yol + yan yollar)
    sira = [d_[0] for d_ in DURAKLAR]
    konum = {d_[0]: (d_[1], d_[2]) for d_ in DURAKLAR}
    yol = []
    for i, k in enumerate(sira):
        yol.append(konum[k])
        if i + 1 < len(sira):
            yol += ROTA_ARA.get((k, sira[i + 1]), [])
    yd = egri_d(yol, False, .9)
    s += f'<path d="{yd}" fill="none" stroke="#1B1D26" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
    s += f'<path d="{yd}" fill="none" stroke="#FFF1CF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="3.2" stroke-dasharray="12 9" stroke-linecap="round"/>'
    for k, x, y, tur in DURAKLAR:
        if tur == "durak":
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 36), True)}" fill="#F0C14A" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 29), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 11)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="32" fill="#FFFFFF">{k}</text>'
        elif tur == "kale":
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="34" fill="#E2533D" stroke="#1B1D26" stroke-width="3"/>'
            s += f'<path d="M{f(x - 18)} {f(y + 14)} V{f(y - 6)} h6 v-6 h6 v6 h4 v-6 h6 v6 h4 v-6 h6 v6 h4 V{f(y + 14)} Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
        else:
            renk = "#F0A21A" if tur == "yan" else "#7B3F8C"
            s += f'<path d="M{f(x)} {f(y - 32)} L{f(x + 32)} {f(y)} L{f(x)} {f(y + 32)} L{f(x - 32)} {f(y)} Z" fill="{renk}" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 10)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="27" fill="#FFFFFF">{k}</text>'
    x, y = konum["1"]
    s += f'<path d="M{f(x + 36)} {f(y + 40)} v-64" stroke="#1B1D26" stroke-width="4"/><path d="M{f(x + 38)} {f(y - 22)} h44 l-10 13 l10 13 h-44 Z" fill="#E2533D" stroke="#1B1D26" stroke-width="2.4"/>'
    for k, (x, y, o) in enumerate(((900, 190, 1.1), (966, 222, .8), (1360, 150, .7), (720, 280, .6))):
        s += S.marti(x, y, o, 3 - k, renk="#5A4A70")
    s += P.kar_yagisi(0, 0, W, h, 160, 360, op=.7, rmax=3)
    px, py = 1985, 1010
    s += f'<circle cx="{px}" cy="{py}" r="64" fill="#FFFFFF" opacity=".92" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 56, 12, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 29), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="9" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 70}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="28" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), konum
