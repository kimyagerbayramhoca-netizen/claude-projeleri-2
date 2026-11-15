"""Kitap çerçevesine özgü çizimler (ortak kütüphaneye eklenmedi; yerel-ortak/cizim parçalarını içe aktarır).

  semboller()            gizli <symbol>'ler (sayfa türü ikonları vb.)
  nisan_boyama()         boyama kitabı çizgisiyle nişan (albüm): renksiz çerçeve + göbekte ikon
  ustad_muhru_boyama()   her yolun Üstad Mührü (boyanacak)
  yol_rozeti()           Yol numaralı Selçuklu yıldızı (harita, içindekiler, albüm)
  mini_sayfa()           rehberdeki sayfa türü küçük resimleri (şematik A4)
  zaman_ikonu()          Medeniyetimizden zaman şeridinin madalyon resimleri
"""
import math
import os
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
ORTAK = os.path.normpath(os.path.join(BURA, "..", "..", "yerel-ortak"))
for _p in (ORTAK, BURA):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cizim.temel import Svg, f, nok, cizgi_d, egri_d, selcuklu_yildizi, yildiz_noktalari, acik, koyu, karis, halolu_yazi, rng as RNG  # noqa: E402
from cizim import sus as U  # noqa: E402
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A, ALTIN, ALTIN_K,  # noqa: E402
                           ALTIN_A, LAJVER, ZUMRUT, ERGUVAN, GUM, GUM_K, GUM_A, DERIN, KIREC)

B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'
N9 = 'font-family="Nunito" font-weight="900"'


def semboller():
    return ""


def yol_rozeti(onek, no, renk, renk_k, cls="yol-rozet"):
    """Yol numaralı rozet (100×100): altın Selçuklu yıldızı + yol renginde iç yıldız + beyaz göbek + numara."""
    s = Svg(onek)
    ga = s.lin([(0, "#F6DE95"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="ya")
    gr = s.rad([(0, acik(renk, .3)), (.65, renk), (1, renk_k)], .4, .35, .75, ad="yr")
    s += f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 48), True)}" fill="{ga}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 40), True)}" fill="{gr}" stroke="{OBS}" stroke-width="2" stroke-linejoin="round"/>'
    s += f'<circle cx="50" cy="50" r="24" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.2"/>'
    boy = 32 if no < 10 else 27
    s += f'<text x="50" y="{f(50 + boy * .36)}" text-anchor="middle" {B} font-size="{boy}" fill="{OBS}">{no}</text>'
    return s.cikti("0 0 100 100", cls=cls)


# ------------------------------------------------------------------ KAPAK SAHNESİ (210×297 mm → 2100×2970 birim)

from cizim import sahne as S, yapilar as Y  # noqa: E402

KAPAK_TEMA = {
    # 10. sınıf: gün batımı (Doğu'dan Batı'ya: güneş batıya iner)
    "aksam": {"gok": [(0, "#191744"), (.22, "#2E2468"), (.42, "#6A3489"), (.6, "#C9467F"), (.76, "#FF6F6A"), (.9, "#FF9A45"), (1, "#FFD27A")],
              "gunes": (1480, 2085, "#FFC56B"), "bulut": ("#FFC59A", "#FF6F8A"), "dag": ("#C98AA8", "#7E5A92", "#FFE3EC", "#FFB0A0"),
              "dag2": ("#6B4C86", "#4E3A6E"), "gol": ("#FFB59A", "#C86A9A", "#2D3A7A"), "parilti": "#FFE3A0",
              "kara": ("#7E8F48", "#3E6B3A"), "on": ("#4E8A3E", "#24502E"), "kale": ("#E6C79A", "#A07E5C", "#F0D7AA"), "marti": "#3A2550"},
    # 9. sınıf: şafak (sabah, yolculuğun başı)
    "safak": {"gok": [(0, "#14275E"), (.25, "#2F4C9A"), (.48, "#6E78C4"), (.66, "#C69AD0"), (.8, "#F6A9B9"), (.92, "#FFD2A8"), (1, "#FFF0D9")],
              "gunes": (1180, 2140, "#FFD9A0"), "bulut": ("#FFF0E6", "#F7A8C0"), "dag": ("#9FA4D6", "#6A6FAE", "#FFFFFF", "#F3B9C8"),
              "dag2": ("#5F6AA8", "#454E8C"), "gol": ("#FFD2C0", "#7FB8D8", "#1F4E8A"), "parilti": "#FFF1C8",
              "kara": ("#86A95A", "#3F7240"), "on": ("#5C9A48", "#2A5A34"), "kale": ("#E9D2AE", "#A88E6C", "#F3E2C2"), "marti": "#2E3466"},
}


def kapak_sahnesi(onek, tema="aksam"):
    """Kapak arka planı: gökyüzü (haritanın asılı durduğu), Van Gölü ufku, Van Kalesi, ön planda yol arkadaşları."""
    t = KAPAK_TEMA[tema]
    s = Svg(onek)
    W, H = 2100, 2970
    ufuk = 2180
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=t["gok"])
    s += S.yildizlar(s, 0, 0, W, 900, 70 if tema == "aksam" else 40, 811, "#FFFFFF")
    gx, gy, hale = t["gunes"]
    for k in range(16):
        a0 = math.pi + .05 + k * (math.pi - .1) / 16
        a1 = a0 + .045
        s += (f'<path d="M{gx} {gy} L{f(gx + 2600 * math.cos(a0))} {f(gy + 2600 * math.sin(a0))} '
              f'L{f(gx + 2600 * math.cos(a1))} {f(gy + 2600 * math.sin(a1))} Z" fill="#FFE8B8" opacity=".07"/>')
    # haritanın arkasındaki yumuşak ışık
    gl = s.rad([(0, "#FFFFFF", .34), (.45, "#FFFFFF", .12), (1, "#FFFFFF", 0)], 1050, 1300, 1150, kull="userSpaceOnUse", ad="hl")
    s += f'<ellipse cx="1050" cy="1300" rx="1250" ry="760" fill="{gl}"/>'
    s += S.gunes(s, gx, gy, 95, hale=hale, hale_r=950, guc=.95)
    bu, ba = t["bulut"]
    for (x, y, w, k) in ((-120, 1880, 760, 26), (1350, 1820, 900, 30), (420, 2010, 560, 18), (1650, 1990, 520, 16), (980, 1930, 420, 14)):
        s += S.bulut_serit(s, x, y, w, k, bu, ba, .8)
    # uzak dağlar: Süphan (volkan, karlı) ve Nemrut (kaldera)
    dr, dg, dk, ds = t["dag"]
    uzak = ""
    d, _ = S.dag(s, 120, 1340, ufuk + 6, 700, 1760, 851, renk=dr, golge=dg, bicim="volkan", kar_y=1850, kar=dk,
                 kar_golge=acik(dg, .45), sis=ds, isik=1 if tema == "safak" else -1, sirt=6, puruz=10, kenar_isik="#FFE0C8")
    uzak += d
    d2r, d2g = t["dag2"]
    d, _ = S.dag(s, 1250, 2300, ufuk + 6, 1820, 1930, 852, renk=d2r, golge=d2g, bicim="kaldera", sis=ds, isik=-1, sirt=3, puruz=7)
    uzak += d
    s += uzak
    gu, go, gd = t["gol"]
    s += S.gol(s, 0, ufuk, W, H - ufuk, 853, ufuk=gu, orta=go, derin=gd, gunes_x=gx, parilti_renk=t["parilti"])
    tas, tg, sur = t["kale"]
    vk, _ = Y.van_kalesi(s, 1220, 2180, ufuk + 150, 250, 854, tas=tas, golge=tg, sur=sur, isik=-1, ayrinti=1.1, bayrak=True)
    s += S.yansima(s, uzak + vk, ufuk + 150, 0, W, 260, op=.26)
    s += vk
    # karşı kıyı: kavak ve köy evleri (kale önü)
    k1, k2 = t["kara"]
    zem = [(1120, H), (1150, ufuk + 190), (1500, ufuk + 176), (1800, ufuk + 186), (2100, ufuk + 170), (2100, H)]
    gz = s.lin([(0, k1), (1, k2)], 0, ufuk + 160, 0, ufuk + 420, kull="userSpaceOnUse", ad="kz")
    s += f'<path d="{egri_d(zem[:-1])} L2100 {H} Z" fill="{gz}"/>'
    r = RNG(855)
    for k in range(10):
        s += S.kavak(s, 1180 + k * 96 + r.uniform(-20, 20), ufuk + 236 + r.uniform(0, 26), r.uniform(120, 170), 26, 856 + k, renk="#6E9A44", isik=-1)
    for k in range(6):
        s += S.ev(1240 + k * 140 + r.uniform(-20, 20), ufuk + 262 + r.uniform(0, 20), 46, 32, 870 + k, duvar="#F3E2C6", cati="#C2563A", isik=-1)
    s += S.tekne(s, 1010, ufuk + 70, 84, govde="#2B50B5", yelken="#FFF1DE")
    s += S.tekne(s, 300, ufuk + 40, 60, govde="#C8442F", yelken="#FFF1DE")
    for k, (x, y, o) in enumerate(((300, 1660, 1.3), (380, 1700, .9), (1720, 1560, .9), (1790, 1600, .7), (1020, 1760, .6))):
        s += S.marti(x, y, o, 3 - k, renk=t["marti"])
    return s, ufuk


def kapak_on_plan(onek, tema="aksam"):
    """Ön plan: yol arkadaşlarının durduğu çimenli tepe (karakterler bu katmanın ARKASINA konur)."""
    t = KAPAK_TEMA[tema]
    s = Svg(onek)
    W, H = 2100, 2970
    o1, o2 = t["on"]
    g = s.lin([(0, o1), (1, o2)], 0, 2600, 0, H, kull="userSpaceOnUse", ad="op")
    pts = [(-40, 2655), (300, 2615), (700, 2640), (1050, 2700), (1400, 2780), (1800, 2830), (2140, 2850)]
    s += f'<path d="{egri_d(pts)} L2140 {H + 10} L-40 {H + 10} Z" fill="{g}"/>'
    s += f'<path d="{egri_d(pts)}" fill="none" stroke="{acik(o1, .35)}" stroke-width="6" stroke-opacity=".8"/>'
    s += S.cimen(-20, 1300, 2660, 861, renk=koyu(o1, .1), renk2=acik(o1, .2), boy=22,
                 cicek=["#FFFFFF", "#F0A21A", "#E2533D", "#FF5C8A"])
    return s


def sinif_rozeti(onek, sinif, tema="aksam"):
    """Kapaktaki büyük sınıf rozeti: 16 köşeli altın çerçeve + Selçuklu yıldızı + sınıf numarası."""
    s = Svg(onek)
    ana, koyu_ = (MER, MER_K) if tema == "aksam" else (KOB, KOB_K)
    ga = s.lin([(0, "#FFF0B8"), (.45, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="sa")
    gr = s.rad([(0, acik(ana, .35)), (.6, ana), (1, koyu_)], .4, .35, .75, ad="sr")
    s += f'<circle cx="104" cy="106" r="92" fill="#1B1D26" opacity=".35"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(100, 100, 98, 84, 16, -math.pi / 2), True)}" fill="{ga}" stroke="{OBS}" stroke-width="3.4" stroke-linejoin="round"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(100, 100, 80), True)}" fill="{gr}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
    for k in range(8):
        a = -math.pi / 2 + math.pi / 4 * k
        s += f'<circle cx="{f(100 + 66 * math.cos(a))}" cy="{f(100 + 66 * math.sin(a))}" r="4" fill="{ALTIN_A}"/>'
    s += f'<circle cx="100" cy="100" r="52" fill="#FFFFFF" stroke="{OBS}" stroke-width="3.4"/>'
    s += f'<circle cx="100" cy="100" r="45" fill="none" stroke="{ana}" stroke-width="2" stroke-dasharray="4 3"/>'
    s += f'<text x="100" y="81" text-anchor="middle" {N9} font-size="12.5" letter-spacing="2.4" fill="{koyu_}">SINIF</text>'
    s += f'<text x="100" y="{128 if sinif < 10 else 126}" text-anchor="middle" {B} font-size="{60 if sinif < 10 else 54}" fill="{OBS}">{sinif}</text>'
    return s.cikti("0 0 200 200", cls="sinif-rozet")


# ------------------------------------------------------------------ REHBER BANDI: göl kıyısında yol ayrımı tabelası (2100×460)

def _tabela(x, y, metin, renk, yon=1, uz=300, boy=54, yazi=30):
    """Ok biçimli tabela levhası: (x, y) direğe bağlandığı nokta, yon=+1 sağa, −1 sola."""
    uc = 34
    if yon > 0:
        d = f"M{f(x)} {f(y)} h{f(uz)} l{f(uc)} {f(boy / 2)} l{f(-uc)} {f(boy / 2)} h{f(-uz)} Z"
        tx = x + uz / 2 + 6
    else:
        d = f"M{f(x)} {f(y)} h{f(-uz)} l{f(-uc)} {f(boy / 2)} l{f(uc)} {f(boy / 2)} h{f(uz)} Z"
        tx = x - uz / 2 - 6
    return (f'<path d="{d}" fill="{renk}" stroke="{OBS}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="2" transform="translate(0 3)"/>'
            f'<text x="{f(tx)}" y="{f(y + boy / 2 + yazi * .36)}" text-anchor="middle" {B} font-size="{yazi}" letter-spacing="1" fill="#FFFFFF">{metin}</text>')


def rehber_bandi(onek="rh-bant"):
    s = Svg(onek)
    W, H = 2100, 460
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "altin")
    s += S.gunes(s, 1010, 120, 42, hale="#FFD27A", hale_r=420, guc=.8)
    for i, (x, y, w) in enumerate([(1180, 70, 300), (1700, 110, 240), (600, 60, 260)]):
        s += S.bulut(s, x, y, w, 610 + i, ust="#FFFFFF", alt="#F3D9C2", op=.95)
    uzak = ""
    d, _ = S.dag(s, 1060, 1900, ufuk + 4, 1480, 160, 612, renk="#9AA8CE", golge="#7181AE", bicim="volkan", kar_y=196,
                 kar="#FFFFFF", kar_golge="#CFD8EE", sis="#F6D9B8", isik=-1, sirt=5)
    uzak += d
    d, _ = S.dag(s, -60, 700, ufuk + 4, 260, 230, 613, renk="#A9B6D6", golge="#8592BE", bicim="tepe", sis="#F6D9B8", isik=-1, sirt=2, puruz=4)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, H - ufuk, 614, ufuk="#BFE9E6", orta="#2BB3B1", derin="#0E6A73", gunes_x=1010)
    s += S.yansima(s, uzak, ufuk, 0, W, 120, op=.22)
    # sağda kıyı tepesi
    zem = [(1080, H), (1150, ufuk + 60), (1400, ufuk + 34), (1700, ufuk + 26), (2100, ufuk + 40), (2100, H)]
    gz = s.lin([(0, "#8DBE5A"), (1, "#4E8A3E")], 0, ufuk + 20, 0, H, kull="userSpaceOnUse", ad="rz")
    s += f'<path d="{egri_d(zem[:-1])} L2100 {H} Z" fill="{gz}"/>'
    r = RNG(615)
    for k in range(8):
        s += S.kavak(s, 1240 + k * 110 + r.uniform(-20, 20), ufuk + 60 + r.uniform(0, 10), r.uniform(110, 150), 24, 616 + k, renk="#5E9A4A", isik=-1)
    # yol: sağ alttan tabelaya, oradan ufka
    yol = [(2140, 470), (1900, 430), (1680, 392), (1520, 360), (1380, 338), (1240, 330)]
    yd = egri_d(yol)
    s += f'<path d="{yd}" fill="none" stroke="#1B1D26" stroke-width="34" stroke-linecap="round" opacity=".85"/>'
    s += f'<path d="{yd}" fill="none" stroke="#F3E2C6" stroke-width="26" stroke-linecap="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="5" stroke-dasharray="18 14" stroke-linecap="round"/>'
    # tabela direği ve levhalar
    px, py = 1640, 395
    s += f'<rect x="{px - 9}" y="{py - 250}" width="18" height="252" rx="4" fill="#8A5A34" stroke="{OBS}" stroke-width="4"/>'
    s += _tabela(px + 9, py - 238, "YOL 1", MER, +1, 230)
    s += _tabela(px - 9, py - 172, "DURAKLAR", GOL, -1, 300)
    s += _tabela(px + 9, py - 106, "KALE", KOB, +1, 200)
    s += f'<circle cx="{px}" cy="{py - 252}" r="12" fill="{ALTIN}" stroke="{OBS}" stroke-width="4"/>'
    s += '<use href="#pamuk-kitap" x="1840" y="214" width="180" height="206"/>'
    s += S.cimen(1100, 2100, H - 2, 617, renk="#4E8A3E", renk2="#8DBE5A", boy=18, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    for k, (x, y, o) in enumerate([(820, 150, 1.0), (880, 176, .7), (1950, 60, .6)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    g = s.lin([(0, "#0E2A3A", 0), (1, "#0E2A3A", .22)], 0, H - 70, 0, H, kull="userSpaceOnUse", ad="cg")
    s += f'<rect x="0" y="{H - 70}" width="{W}" height="70" fill="{g}"/>'
    return s.cikti(f"0 0 {W} {H}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ BOYANACAK NİŞAN (albüm) + ÜSTAD MÜHRÜ

def nisan_boyama(onek, ikon_svg=None, kurdele=True, bos=False, cls="nisan-boya"):
    """Boyama kitabı çizgisiyle nişan: nişanın bütün parçaları beyaz, yalnız siyah çizgi. bos=True → ad bilinmiyor:
    göbek kesik çizgili boş yuva (nişan uydurulmaz)."""
    s = Svg(onek)
    c = OBS
    y16 = yildiz_noktalari(50, 50, 49, 41, 16, -math.pi / 2)
    if kurdele:
        s += (f'<path d="M28 66 L18 112 L30 105 L37 117 L48 74 Z" fill="#FFFFFF" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
              f'<path d="M72 66 L82 112 L70 105 L63 117 L52 74 Z" fill="#FFFFFF" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
              f'<path d="M31 80 L42 84 M69 80 L58 84" stroke="{c}" stroke-width="1.2" stroke-opacity=".6"/>')
    s += f'<path d="{cizgi_d(y16, True)}" fill="#FFFFFF" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 40), True)}" fill="#FFFFFF" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>'
    for k in range(8):
        a = -math.pi / 2 + math.pi / 4 * k
        s += f'<circle cx="{f(50 + 33 * math.cos(a))}" cy="{f(50 + 33 * math.sin(a))}" r="2.2" fill="#FFFFFF" stroke="{c}" stroke-width="1"/>'
    if bos:
        s += f'<circle cx="50" cy="50" r="26" fill="#FFFFFF" stroke="{c}" stroke-width="1.6" stroke-dasharray="4 3"/>'
        s += f'<text x="50" y="57" text-anchor="middle" {B} font-size="20" fill="#B9C6CC">?</text>'
    else:
        s += f'<circle cx="50" cy="50" r="26" fill="#FFFFFF" stroke="{c}" stroke-width="2"/>'
        if ikon_svg:
            s += f'<g transform="translate(30 30) scale(.8333)" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ikon_svg}</g>'
    return s.cikti("0 0 100 120" if kurdele else "0 0 100 100", cls=cls)


def ustad_ikonu():
    """Üstad Mührü göbek ikonu: ortak kütüphanede varsa onu (sus.NISAN_IKON['ustad']), yoksa mühür."""
    ik = U.NISAN_IKON.get("ustad")
    if ik:
        return ik
    return (f'<circle cx="24" cy="7.5" r="4"/><path d="M21.2 11 H26.8 L26 18 H22 Z"/><path d="M13 18 H35 L37.5 25 H10.5 Z"/>'
            f'<path d="M9 25 H39 V28.5 H9 Z"/><path d="{cizgi_d(selcuklu_yildizi(24, 38.5, 7.6), True)}"/><circle cx="24" cy="38.5" r="2"/>')


def nisan_ikonu(ad):
    """meta.json'daki ikon adı → 48×48 çizgi ikon. Bilinmeyen ikon için sade Selçuklu yıldızı (ad uydurulmaz)."""
    if ad == "ustad":
        return ustad_ikonu()
    if ad in U.NISAN_IKON:
        return U.NISAN_IKON[ad]
    return f'<path d="{cizgi_d(selcuklu_yildizi(24, 24, 14), True)}"/><circle cx="24" cy="24" r="4"/>'
