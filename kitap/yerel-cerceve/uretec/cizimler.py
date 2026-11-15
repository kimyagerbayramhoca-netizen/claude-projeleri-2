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
                           ALTIN_A, LAJVER, ZUMRUT, ERGUVAN, GUM, GUM_K, GUM_A, DERIN, KIREC, GOL_AA)

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


# ------------------------------------------------------------------ SAYFA TÜRÜ KÜÇÜK RESİMLERİ (rehber) · viewBox 210×297

def _m_kart(x, y, w, h, dolgu="#FFFFFF", bas=None, r=4, cizgi=OBS, kesik=False):
    o = f'<rect x="{f(x + 1.6)}" y="{f(y + 1.8)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{DERIN}"/>' if not kesik else ""
    kes = ' stroke-dasharray="3 2"' if kesik else ""
    o += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{dolgu}" stroke="{cizgi}" stroke-width="1.1"{kes}/>'
    if bas:
        o += (f'<path d="M{f(x)} {f(y + r)} a{r} {r} 0 0 1 {r} {-r} h{f(w - 2 * r)} a{r} {r} 0 0 1 {r} {r} v{f(7 - r)} h{f(-w)} Z" fill="{bas}" '
              f'stroke="{cizgi}" stroke-width="1.1"/>')
    return o


def _m_satir(x, y, w, n=3, ara=5.2, renk="#C9D3D8", kal=2.2, son=.6):
    return "".join(f'<path d="M{f(x)} {f(y + i * ara)} h{f(w * (son if i == n - 1 else 1))}" stroke="{renk}" stroke-width="{kal}" stroke-linecap="round"/>'
                   for i in range(n))


def _m_yildiz(x, y, R, renk, metin=None, fs=None):
    o = (f'<path d="{cizgi_d(selcuklu_yildizi(x, y, R), True, 1)}" fill="{ALTIN}" stroke="{OBS}" stroke-width=".9"/>'
         f'<path d="{cizgi_d(selcuklu_yildizi(x, y, R * .78), True, 1)}" fill="{renk}" stroke="{OBS}" stroke-width=".6"/>')
    if metin is not None:
        o += f'<text x="{f(x)}" y="{f(y + (fs or R) * .38)}" text-anchor="middle" {B} font-size="{f(fs or R)}" fill="#FFFFFF">{metin}</text>'
    return o


def _m_bant(s, y, h, gok, kara, odak=""):
    g = s.lin([(i / (len(gok) - 1), c) for i, c in enumerate(gok)], 0, y, 0, y + h, kull="userSpaceOnUse", ad="mb")
    o = f'<rect x="0" y="{y}" width="210" height="{h}" fill="{g}"/>'
    o += f'<path d="M0 {f(y + h * .62)} Q60 {f(y + h * .5)} 120 {f(y + h * .64)} T210 {f(y + h * .58)} V{f(y + h)} H0 Z" fill="{kara}"/>'
    o += odak
    o += f'<path d="M0 {f(y + h)} H210" stroke="{OBS}" stroke-width="1.2"/>'
    return o


def _m_levha(x, y, w, h, renk=GOL):
    return (f'<rect x="{f(x + 1.2)}" y="{f(y + 1.4)}" width="{w}" height="{h}" rx="5" fill="{DERIN}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.1"/>'
            + _m_yildiz(x + 11, y + h / 2, 8, renk)
            + f'<path d="M{f(x + 23)} {f(y + h * .36)} h{f(w * .55)}" stroke="{OBS}" stroke-width="4.6" stroke-linecap="round"/>'
            + _m_satir(x + 23, y + h * .64, w * .62, 2, 4.4, "#B8C5CC", 1.8))


def mini_sayfa(onek, tur):
    """Bir sayfa türünün şematik küçük resmi (210×297 birimlik A4)."""
    s = Svg(onek)
    o = [f'<rect x="0" y="0" width="210" height="297" fill="{KIREC if tur == "ustad" else "#FBFDFD"}"/>',
         f'<rect x="0" y="0" width="210" height="10" fill="{OBS}"/>',
         f'<path d="M0 11 H210" stroke="{KOB_K}" stroke-width="2.4"/><path d="M2 11 H210" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="1.4 5"/>']
    o += [f'<circle cx="{150 + i * 5}" cy="5" r="1.6" fill="{GOL if i < 3 else "none"}" stroke="#8FA3AD" stroke-width=".6"/>' for i in range(6)]
    o.append(f'<rect x="10" y="3.5" width="30" height="3" rx="1.5" fill="#FFFFFF" opacity=".85"/>')
    if tur == "acilis":
        o.append(f'<path d="M12 28 h70" stroke="{GOL}" stroke-width="13" stroke-linecap="round"/><path d="M90 28 h50" stroke="{OBS}" stroke-width="13" stroke-linecap="round"/>')
        o.append(_m_satir(12, 45, 120, 1, 0, "#9AA8B0", 3))
        o.append(f'<circle cx="180" cy="34" r="16" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.2"/><circle cx="174" cy="32" r="2.4" fill="{MAVI_G}"/><circle cx="186" cy="32" r="2.4" fill="{KEH}"/>')
        g = s.lin([(0, "#5B3A86"), (.5, "#FF6F6A"), (1, "#9DAA5E")], 0, 58, 0, 168, kull="userSpaceOnUse", ad="mp")
        o.append(f'<rect x="0" y="58" width="210" height="110" fill="{g}"/>')
        o.append(f'<path d="M40 120 C60 92 140 88 170 112 C178 130 150 150 100 148 C60 146 34 138 40 120 Z" fill="#2BB3B1" stroke="#FFF3D6" stroke-width="2"/>')
        o.append(f'<path d="M44 124 C60 96 140 92 166 112 C172 132 140 146 100 144" fill="none" stroke="#FFF1CF" stroke-width="3.4" stroke-dasharray="5 3"/>')
        for i, (x, y) in enumerate(((44, 124), (78, 102), (122, 98), (160, 110), (150, 140))):
            o.append(_m_yildiz(x, y, 6, GOL))
        for i in range(6):
            o.append(_m_yildiz(22 + i * 33, 186, 9, [GOL, KOB, GOL, MER, ERGUVAN, KEH][i]))
        o.append(_m_kart(10, 204, 92, 48) + _m_satir(18, 218, 74, 5, 6))
        o.append(_m_kart(108, 204, 92, 48) + _m_satir(116, 218, 74, 5, 6))
        o.append(_m_kart(10, 258, 190, 16, "#EEF9F8"))
    elif tur == "durak":
        o.append(_m_bant(s, 12, 46, ["#86C8F0", "#E3F6FB"], "#5E9A4A", f'<rect x="150" y="30" width="22" height="20" fill="#C99E74" stroke="{OBS}" stroke-width=".8"/><path d="M148 30 L161 18 L174 30 Z" fill="#B8553A" stroke="{OBS}" stroke-width=".8"/>'))
        o.append(_m_levha(10, 18, 112, 34))
        o.append(_m_kart(10, 64, 96, 66))
        for i, c in enumerate((MER_A, GOL_A, KEH_A, MER_A)):
            o.append(f'<rect x="{18 if i % 2 else 30}" y="{72 + i * 14}" width="66" height="11" rx="4" fill="{c}" stroke="{OBS}" stroke-width=".7"/>')
        o.append(_m_kart(112, 64, 88, 66, KOB_A) + _m_satir(120, 78, 70, 6, 7.5))
        o.append(_m_kart(10, 136, 190, 50) + _m_satir(18, 150, 54, 4, 8) + f'<path d="M84 160 H190" stroke="{GOL}" stroke-width="5" stroke-linecap="round"/>')
        o.append(_m_kart(10, 192, 64, 80, MER_A, bas=MER) + _m_satir(18, 214, 46, 6, 7.5))
        o.append(_m_kart(80, 192, 58, 36, kesik=True) + _m_yildiz(92, 210, 8, KEH) + _m_satir(104, 204, 26, 3, 6))
        o.append(_m_kart(80, 234, 58, 38, GOL_AA) + _m_satir(88, 246, 42, 4, 6))
        o.append(_m_kart(144, 192, 56, 80, KEH_A) + _m_satir(152, 208, 40, 6, 7.5))
    elif tur == "hulasa":
        o.append(_m_bant(s, 12, 36, ["#86C8F0", "#E3F6FB"], "#5E9A4A", f'<path d="M120 40 L150 18 L180 40 Z" fill="#9AA8CE"/><path d="M143 23 L150 18 L157 23 L150 25 Z" fill="#FFFFFF"/>'))
        o.append(_m_levha(10, 16, 100, 28, ERGUVAN))
        r = RNG(41)
        for i in range(22):
            o.append(f'<circle cx="{f(r.uniform(0, 210))}" cy="{f(r.uniform(52, 156))}" r="{f(r.uniform(10, 26))}" fill="{r.choice([MER, KEH, GOL, ERGUVAN, "#FF8A3D", "#FF5C8A"])}" opacity=".55"/>')
        for i in range(6):
            x, y = 10 + (i % 3) * 65, 58 + (i // 3) * 50
            o.append(_m_kart(x, y, 60, 44, [DERIN, GOL_AA, "#FFFFFF", KEH_A, MER_A, "#FFFFFF"][i]) + _m_satir(x + 7, y + 12, 44, 4, 7, "#FFFFFF" if i == 0 else "#C9D3D8"))
        o.append(_m_kart(10, 164, 190, 30, KEH_A))
        for i in range(10):
            o.append(f'<rect x="{16 + (i % 5) * 37}" y="{170 + (i // 5) * 12}" width="33" height="9" rx="2" fill="#FFFFFF" stroke="{OBS}" stroke-width=".6" stroke-dasharray="2 1.4"/>')
        o.append(_m_kart(10, 200, 134, 72) + _m_satir(18, 216, 80, 7, 7.4))
        for i in range(7):
            for j in range(3):
                o.append(f'<path d="M{110 + j * 11} {f(212 + i * 7.4)} l2 6 h4 l2 -6 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width=".6"/>')
        o.append(_m_kart(150, 200, 50, 72) + _m_satir(157, 214, 36, 5, 7))
    elif tur == "meclis":
        kil = "".join(f'<path d="M{x} 28 l9 -9 l9 9 l-9 9 Z" fill="{["#B23A2E", "#253C78", "#D99A2B"][i % 3]}"/>' for i, x in enumerate(range(118, 210, 18)))
        o.append(_m_bant(s, 12, 44, ["#F5E8D0", "#F5E8D0"], "#B23A2E", f'<rect x="118" y="12" width="92" height="30" fill="#F5E8D0"/>{kil}'))
        o.append(_m_levha(10, 17, 100, 32, KEH))
        for i, (h, c) in enumerate((("A", GOL), ("Z", MER), ("M", KOB), ("R", KEH))):
            x, y = 10 + (i % 2) * 97, 62 + (i // 2) * 92
            o.append(_m_kart(x, y, 93, 86) + f'<circle cx="{x + 11}" cy="{y + 11}" r="6.5" fill="{c}" stroke="{OBS}" stroke-width=".8"/>'
                     f'<text x="{x + 11}" y="{y + 14}" text-anchor="middle" {B} font-size="9" fill="#FFFFFF">{h}</text>'
                     + _m_satir(x + 22, y + 11, 50, 1, 0, OBS, 3) + f'<rect x="{x + 7}" y="{y + 24}" width="79" height="26" rx="3" fill="#FFFFFF" stroke="{OBS}" stroke-width=".7"/>'
                     + _m_satir(x + 16, y + 31, 60, 3, 7) + f'<rect x="{x + 7}" y="{y + 58}" width="79" height="20" rx="3" fill="none" stroke="{GOL_K}" stroke-width=".7" stroke-dasharray="2 1.4"/>')
        o.append(_m_kart(10, 248, 120, 26, KIREC, cizgi=LAJVER) + _m_kart(136, 248, 64, 26, KEH_A))
    elif tur == "kissa":
        o.append(_m_bant(s, 12, 44, ["#9ED6EE", "#E3F6FB"], "#4E8A3E", f'<path d="M160 20 h14 v30 h-14 Z" fill="#DDF4F6" stroke="{OBS}" stroke-width=".8"/>'))
        o.append(_m_levha(10, 17, 100, 32, KOB))
        for i in range(4):
            x, y = 10 + (i % 2) * 97, 62 + (i // 2) * 106
            o.append(_m_kart(x, y, 93, 100, bas=[KOB, KEH, GOL, MER][i]) + _m_satir(x + 7, y + 18, 78, 5, 7))
            for j in range(5):
                o.append(f'<rect x="{x + 7 + (j % 2) * 40}" y="{y + 58 + (j // 2) * 12}" width="36" height="9" rx="4" fill="#FFFFFF" stroke="{OBS}" stroke-width=".6"/>')
    elif tur == "merdiven":
        o.append(_m_bant(s, 12, 44, ["#5B3A86", "#FF9A6A"], "#0E4C5A", f'<rect x="150" y="34" width="40" height="5" fill="#9A6B42"/><path d="M178 34 v-14" stroke="#FFFFFF" stroke-width="3"/>'))
        o.append(_m_levha(10, 17, 100, 32, KEH))
        for i in range(3):
            y = 64 + i * 72
            o.append(_m_kart(10, y, 92, 64) + _m_satir(18, y + 12, 74, 5, 8))
            for j in range(3):
                o.append(_m_kart(108 + j * 10, y + j * 16, 92 - j * 10, 16, [GOL_AA, GOL_A, KEH_A][j]) + f'<circle cx="{116 + j * 10}" cy="{y + 8 + j * 16}" r="3.4" fill="{KEH}"/>')
    elif tur == "imtihan":
        duvar = "".join(f'<rect x="{x}" y="22" width="12" height="10" fill="#E6CFA4" stroke="#8C6E4A" stroke-width=".6"/>' for x in range(96, 210, 18))
        o.append(_m_bant(s, 12, 50, ["#2F5DA8", "#FFB46B"], "#D9BE92", f'<rect x="90" y="30" width="120" height="22" fill="#D9BE92"/>{duvar}'
                                                                          f'<path d="M150 22 v-12" stroke="{OBS}" stroke-width="1"/><rect x="150" y="10" width="10" height="7" fill="{MER}"/>'))
        o.append(_m_levha(10, 18, 104, 38, MER))
        for i in range(6):
            x, y = 10 + (i // 3) * 97, 68 + (i % 3) * 70
            o.append(_m_kart(x, y, 93, 64) + _m_yildiz(x + 10, y + 10, 6.5, MER, str(i + 1 if i < 3 else i + 1), 7)
                     + _m_satir(x + 20, y + 10, 50, 2, 6, OBS, 2.4) + f'<rect x="{x + 7}" y="{y + 22}" width="79" height="18" rx="3" fill="none" stroke="#B8C5CC" stroke-width=".7" stroke-dasharray="2 1.4"/>')
            for j in range(5):
                o.append(f'<rect x="{x + 7 + (j % 3) * 27}" y="{y + 44 + (j // 3) * 9}" width="24" height="7" rx="3" fill="#FFFFFF" stroke="{OBS}" stroke-width=".6"/>')
    elif tur == "ustad":
        yild = "".join(f'<path d="{cizgi_d(selcuklu_yildizi(x, y, r), True, 1)}" fill="{ALTIN}" opacity=".85"/>' for x, y, r in ((150, 24, 5), (176, 34, 3.6), (196, 20, 4.4), (128, 40, 3)))
        o.append(_m_bant(s, 12, 44, ["#0F1A45", "#1D3A8A"], "#13285E", yild))
        o.append(f'<rect x="10" y="17" width="100" height="32" rx="5" fill="#FFFFFF" stroke="{LAJVER}" stroke-width="1.2"/>' + _m_yildiz(21, 33, 8, LAJVER)
                 + f'<path d="M33 27 h55" stroke="{OBS}" stroke-width="4.6" stroke-linecap="round"/>' + _m_satir(33, 38, 60, 2, 4.4, "#B8C5CC", 1.8))
        for i in range(6):
            x, y = 10 + (i // 3) * 97, 62 + (i % 3) * 66
            o.append(f'<rect x="{x}" y="{y}" width="93" height="60" rx="3" fill="{KIREC}" stroke="{LAJVER}" stroke-width="1.2"/>'
                     f'<rect x="{x + 2}" y="{y + 2}" width="89" height="56" rx="2" fill="none" stroke="{ALTIN}" stroke-width=".7"/>'
                     + _m_yildiz(x + 10, y + 10, 6, LAJVER, str(i + 1), 7) + _m_satir(x + 20, y + 10, 60, 4, 6.5))
        o.append(f'<rect x="10" y="262" width="190" height="14" rx="3" fill="{KIREC}" stroke="{LAJVER}" stroke-width="1.2"/>' + _m_yildiz(20, 269, 6, ALTIN))
    elif tur == "cevaplar":
        o.append(_m_bant(s, 12, 34, ["#070B26", "#2C4A85"], "#15224F", f'<circle cx="160" cy="24" r="7" fill="#FFF4D6"/><circle cx="163" cy="22" r="6" fill="#15224F"/>'
                                                                       + "".join(f'<circle cx="{x}" cy="{y}" r="1" fill="#FFFFFF"/>' for x, y in ((130, 18), (180, 30), (196, 16), (120, 30)))))
        o.append(_m_levha(10, 16, 104, 26, GOL))
        o.append(_m_kart(10, 52, 190, 34))
        for i in range(12):
            o.append(f'<rect x="{16 + i * 15.2}" y="58" width="13" height="22" rx="2.4" fill="#FFFFFF" stroke="{OBS}" stroke-width=".7"/>'
                     f'<text x="{f(22.5 + i * 15.2)}" y="72" text-anchor="middle" {B} font-size="8" fill="{GOL_K}">{"DCBEACCDBECD"[i]}</text>')
        o.append(_m_kart(10, 92, 190, 136) + _m_satir(18, 104, 82, 15, 8) + _m_satir(110, 104, 82, 15, 8))
        o.append(_m_kart(10, 234, 90, 38, KEH_A) + _m_kart(106, 234, 94, 38))
    elif tur == "final":
        o.append(_m_bant(s, 12, 64, ["#26245E", "#C9467F", "#FFD27A"], "#E8C998",
                         f'<path d="M20 30 Q100 52 180 26" fill="none" stroke="#5A3A22" stroke-width="1"/>'
                         + "".join(_m_yildiz(40 + i * 26, 36 + abs(i - 2.5) * -2 + 6, 6.5, [GOL, KOB, GOL, MER, ERGUVAN, KEH][i]) for i in range(6))))
        o.append(_m_kart(10, 84, 190, 26))
        g = s.lin([(0, GUM), (.5, GOL), (1, KEH)], 20, 0, 190, 0, kull="userSpaceOnUse", ad="fr")
        o.append(f'<rect x="20" y="96" width="170" height="6" rx="3" fill="{g}" stroke="{OBS}" stroke-width=".6"/>')
        for i in range(4):
            o.append(_m_kart(10 + i * 48, 116, 44, 34, KEH_A if i == 3 else "#FFFFFF") + _m_yildiz(32 + i * 48, 128, 7, [GUM, GOL, DERIN, KEH][i]))
        o.append(_m_kart(10, 156, 104, 116) + _m_satir(18, 170, 64, 11, 9) + "".join(f'<rect x="88" y="{164 + i * 9}" width="18" height="6" rx="1.5" fill="#FFFFFF" stroke="{OBS}" stroke-width=".5"/>' for i in range(11)))
        o.append(_m_kart(120, 156, 80, 40) + "".join(_m_yildiz(130 + i * 12, 172, 5, [GOL, KOB, GOL, MER, ERGUVAN, KEH][i]) for i in range(6)))
        o.append(_m_kart(120, 202, 80, 32) + _m_kart(120, 240, 80, 32, GOL_AA))
    # altbilgi
    o.append(f'<path d="M12 286 h40 M86 286 h40" stroke="{GOL_K}" stroke-width="2.4" stroke-linecap="round"/>' + _m_yildiz(196, 286, 5, GOL))
    o.append(f'<rect x="0" y="292" width="210" height="5" fill="#BFE7E3"/><path d="M0 292 H210" stroke="{OBS}" stroke-width=".8"/>')
    kl = s.klip('<rect x="0" y="0" width="210" height="297"/>', ad="mk")
    s += f'<g clip-path="{kl}">{"".join(o)}</g><rect x=".5" y=".5" width="209" height="296" fill="none" stroke="{OBS}" stroke-width="1.2"/>'
    return s.cikti("0 0 210 297", cls="mini-sayfa")


MAVI_G = "#3A8CF2"


# ------------------------------------------------------------------ ÇİNİ PANO BANDI (rehber 2): İznik karoları, açık vektör

def cini_pano_bandi(onek="cp-bant", h=360, palet=None):
    s = Svg(onek)
    W = 2100
    a = 120
    zemin_r, yildiz_r, gobek_r, nokta_r, yaprak_r = palet or (KOB_K, KOB, GOL, MER, ZUMRUT)
    zem = s.lin([(0, "#FFFFFF"), (1, "#EAF4F6")], 0, 0, 0, 1, ad="cz")
    o = [f'<rect width="{W}" height="{h}" fill="{zemin_r}"/>']
    r = RNG(77)
    for j in range(-1, h // a + 1):
        for i in range(-1, W // a + 1):
            x, y = i * a + (a / 2 if j % 2 else 0), j * a + 10
            o.append(f'<rect x="{f(x + 3)}" y="{f(y + 3)}" width="{a - 6}" height="{a - 6}" rx="6" fill="{zem}"/>')
            cx, cy = x + a / 2, y + a / 2
            o.append(f'<path d="{cizgi_d(selcuklu_yildizi(cx, cy, 40), True, 1)}" fill="{yildiz_r}" stroke="{zemin_r}" stroke-width="2"/>')
            o.append(f'<path d="{cizgi_d(selcuklu_yildizi(cx, cy, 25), True, 1)}" fill="{gobek_r}" stroke="#FFFFFF" stroke-width="3"/>')
            o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="8" fill="{nokta_r}" stroke="#FFFFFF" stroke-width="2.4"/>')
            for dx, dy in ((0, 0), (a, 0), (0, a), (a, a)):
                o.append(f'<circle cx="{f(x + dx)}" cy="{f(y + dy)}" r="15" fill="{nokta_r}" stroke="#FFFFFF" stroke-width="3"/>'
                         f'<circle cx="{f(x + dx)}" cy="{f(y + dy)}" r="5" fill="{ALTIN_A}"/>')
            # lale yaprakları (köşegenlerde)
            for k in range(4):
                ang = math.pi / 4 + k * math.pi / 2
                px, py = cx + 47 * math.cos(ang), cy + 47 * math.sin(ang)
                o.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="9" ry="4.4" transform="rotate({f(math.degrees(ang))} {f(px)} {f(py)})" fill="{yaprak_r}"/>')
    g = s.lin([(0, "#0E2A3A", 0), (1, "#0E2A3A", .25)], 0, h - 70, 0, h, kull="userSpaceOnUse", ad="cg")
    o.append(f'<rect x="0" y="{h - 70}" width="{W}" height="70" fill="{g}"/>')
    s += "".join(o)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ ZAMAN ŞERİDİ MADALYONLARI (100×100; lacivert zemin, altın çizgi)

_ZI = {
    "imbik": ('<path d="M30 70 C22 70 18 60 22 52 C26 44 36 42 40 46 L42 34 H52 L52 46 C58 46 62 54 60 62 C58 70 48 72 40 70 Z"/>'
              '<path d="M50 38 C60 30 70 32 78 40 L80 44"/><path d="M80 46 v8"/><circle cx="80" cy="60" r="2.6" fill="{a}"/>'
              '<path d="M26 60 h30"/>'),
    "cebir": ('<path d="M50 24 V70 M34 76 H66 M22 34 H78"/><path d="M22 34 L14 52 H30 Z M78 34 L70 52 H86 Z"/>'
              '<rect x="16" y="54" width="12" height="9" rx="1.5"/><text x="22" y="61.5" text-anchor="middle" font-family="Baloo Bhaijaan 2" '
              'font-weight="800" font-size="9" fill="{a}" stroke="none">x</text><circle cx="74" cy="58" r="3"/><circle cx="82" cy="58" r="3"/>'),
    "gul": ('<circle cx="40" cy="44" r="15"/><path d="M40 32 C48 38 46 50 38 52 C30 50 30 40 40 36 C44 40 42 46 38 46"/>'
            '<path d="M40 59 C40 66 42 74 44 80 M41 66 C34 62 28 64 26 68 M42 72 C48 68 54 70 56 74"/>'
            '<path d="M68 30 C68 30 60 42 60 48 C60 53 64 56 68 56 C72 56 76 53 76 48 C76 42 68 30 68 30 Z"/>'),
    "razi": ('<path d="M14 58 H46 L42 74 H18 Z"/><path d="M30 58 L40 36" stroke-width="4"/>'
             '<path d="M62 30 h12 M66 30 V44 C58 48 56 58 58 66 C60 74 68 78 74 76 C82 74 86 66 84 58 C82 50 78 46 72 44 V30"/><path d="M59 62 H83"/>'),
    "goz": ('<path d="M22 54 C34 38 66 38 78 54 C66 70 34 70 22 54 Z"/><circle cx="50" cy="54" r="9"/><circle cx="50" cy="54" r="3.4" fill="{a}"/>'
            '<path d="M80 22 L60 42 M88 34 L66 46 M68 16 L56 36"/>'),
    "ozgul": ('<path d="M18 42 L30 30 H50 L62 42 L40 70 Z"/><path d="M18 42 H62 M30 30 L36 42 L40 70 L44 42 L50 30 M36 42 H44"/>'
              '<path d="M68 34 V70 C68 76 86 76 86 70 V34"/><path d="M68 52 H86"/><path d="M64 34 H90"/>'),
    "sina": ('<path d="M18 66 C28 62 40 62 50 68 C60 62 72 62 82 66 V34 C72 30 60 30 50 36 C40 30 28 30 18 34 Z"/><path d="M50 36 V68"/>'
             '<path d="M30 26 L36 14 L42 26 Z M60 24 L66 10 L72 24 Z M42 24 L48 18 L52 24"/>'),
    "terazi": ('<path d="M50 18 V76 M36 80 H64 M16 30 H84"/><circle cx="50" cy="18" r="3"/><path d="M16 30 L10 50 H22 Z M84 30 L78 50 H90 Z"/>'
               '<path d="M50 30 L50 30"/><path d="M38 30 L34 46 H42 Z"/><path d="M62 30 L58 46 H66 Z"/>'),
    "cark": ('<circle cx="42" cy="54" r="16"/><circle cx="42" cy="54" r="5"/>'
             + "".join(f'<path d="M{f(42 + 16 * math.cos(a))} {f(54 + 16 * math.sin(a))} L{f(42 + 23 * math.cos(a))} {f(54 + 23 * math.sin(a))}" stroke-width="5"/>' for a in [i * math.pi / 4 for i in range(8)])
             + '<path d="M72 22 C72 22 64 34 64 40 C64 45 68 48 72 48 C76 48 80 45 80 40 C80 34 72 22 72 22 Z"/><path d="M72 52 V64"/>'),
    "rasat": ('<circle cx="50" cy="46" r="24"/><ellipse cx="50" cy="46" rx="24" ry="9"/><ellipse cx="50" cy="46" rx="9" ry="24"/>'
              '<path d="M30 30 L70 62"/><circle cx="50" cy="46" r="3.4" fill="{a}"/><path d="M50 70 V80 M38 82 H62"/>'),
    "yildiz": ('<path d="M18 76 A58 58 0 0 1 76 18"/><path d="M18 76 L76 18" stroke-dasharray="3 3"/>'
               + "".join(f'<path d="M{f(18 + 58 * math.cos(-a))} {f(76 + 58 * math.sin(-a))} l{f(-6 * math.cos(-a))} {f(-6 * math.sin(-a))}"/>' for a in [i * math.pi / 16 for i in range(1, 8)])
               + f'<path d="{cizgi_d(yildiz_noktalari(70, 64, 9, 3.6, 5, -math.pi / 2), True)}" fill="{{a}}"/>'
               + f'<path d="{cizgi_d(yildiz_noktalari(56, 44, 5, 2, 5, -math.pi / 2), True)}" fill="{{a}}"/>'),
    "saat": ('<circle cx="46" cy="50" r="24"/><circle cx="46" cy="50" r="2.6" fill="{a}"/><path d="M46 50 V34 M46 50 L58 56"/>'
             + "".join(f'<path d="M{f(46 + 20 * math.cos(a))} {f(50 + 20 * math.sin(a))} L{f(46 + 23 * math.cos(a))} {f(50 + 23 * math.sin(a))}"/>' for a in [i * math.pi / 6 for i in range(12)])
             + '<path d="M70 22 L80 14 M74 30 L86 26"/><path d="M38 76 L34 84 M54 76 L58 84"/>'),
    "kure": ('<circle cx="46" cy="44" r="22"/><path d="M24 44 H68 M46 22 C36 32 36 56 46 66 M46 22 C56 32 56 56 46 66"/>'
             '<path d="M28 32 C40 36 52 36 64 32 M28 56 C40 52 52 52 64 56"/><path d="M14 80 C30 74 46 74 52 80 C58 74 74 74 88 80"/>'),
    "marifet": ('<path d="M16 72 C28 68 40 68 50 74 C60 68 72 68 84 72 V44 C72 40 60 40 50 46 C40 40 28 40 16 44 Z"/><path d="M50 46 V74"/>'
                '<circle cx="50" cy="22" r="6"/><ellipse cx="50" cy="22" rx="18" ry="6"/><circle cx="68" cy="22" r="2.4" fill="{a}"/>'),
    "dna": ("".join(f'<path d="M{f(30 + 22 * math.sin(t / 6))} {f(14 + t * 2.4)} L{f(30 - 22 * math.sin(t / 6) + 40)} {f(14 + t * 2.4)}" stroke-width="2.2"/>'
                    for t in range(2, 30, 4))
            + '<path d="M30 14 C52 28 52 42 30 50 C8 58 8 72 30 86" transform="translate(20 0)"/>'
            + '<path d="M70 14 C48 28 48 42 70 50 C92 58 92 72 70 86" transform="translate(-20 0)"/>'),
    "sifa": ('<path d="M22 80 V44 C22 26 78 26 78 44 V80"/><path d="M34 80 V50 C34 38 66 38 66 50 V80"/><path d="M16 80 H84"/>'
             f'<path d="{cizgi_d(selcuklu_yildizi(50, 30, 7), True)}" fill="{{a}}"/><path d="M42 58 H58 M50 50 V66"/>'),
}


def zaman_ikonu(onek, ad, kucuk=False):
    """Zaman şeridi madalyonu: lacivert daire, altın halka, altın-beyaz çizgi resim."""
    s = Svg(onek)
    g = s.rad([(0, "#2D4FA8"), (1, LAJVER)], .4, .35, .7, ad="zm")
    ga = s.lin([(0, "#F6DE95"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="za")
    s += f'<circle cx="50" cy="50" r="48" fill="{ga}" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<circle cx="50" cy="50" r="41" fill="{g}" stroke="{OBS}" stroke-width="1.6"/>'
    for k in range(16):
        a = 2 * math.pi * k / 16
        s += f'<circle cx="{f(50 + 44.6 * math.cos(a))}" cy="{f(50 + 44.6 * math.sin(a))}" r="1.3" fill="{ALTIN_A}"/>'
    ic = _ZI.get(ad, _ZI["sifa"]).replace("{a}", ALTIN_A)
    s += f'<g transform="translate(14 14) scale(.72)" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">{ic}</g>'
    return s.cikti("0 0 100 100", cls="zaman-ikon")


# ------------------------------------------------------------------ MEDENİYETİMİZDEN BANDI (2100×h): lacivert gece, altın aletler

def medeniyet_bandi(onek="md-bant", h=420, sag_odak="rasat"):
    s = Svg(onek)
    W = 2100
    g = s.lin([(0, "#0B1440"), (.6, "#1D3A8A"), (1, "#2D4FA8")], 0, 0, 0, h, kull="userSpaceOnUse", ad="mg")
    s += f'<rect width="{W}" height="{h}" fill="{g}"/>'
    # altın Selçuklu geçmesi (soluk)
    yd = []
    for j in range(-1, h // 90 + 2):
        for i in range(-1, W // 90 + 2):
            yd.append(cizgi_d(selcuklu_yildizi(i * 90 + (45 if j % 2 else 0), j * 90, 20), True, 1))
    s += f'<path d="{" ".join(yd)}" fill="none" stroke="{ALTIN}" stroke-opacity=".22" stroke-width="2"/>'
    s += S.yildizlar(s, 0, 0, W, h * .8, 60, 431, "#FFF4D6")
    ga = s.lin([(0, "#FFF0B8"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="ma")
    if sag_odak == "rasat":
        # halkalı küre (armiller) + kitap yığını + imbik silueti
        cx, cy, R = 1660, 205, 130
        s += f'<circle cx="{cx}" cy="{cy}" r="{R + 40}" fill="#FFE7A8" opacity=".08"/>'
        for rx, ry, don in ((R, R, 0), (R, R * .36, -20), (R * .36, R, 0), (R, R * .36, 40)):
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="{f(rx)}" ry="{f(ry)}" transform="rotate({don} {cx} {cy})" fill="none" stroke="{ga}" stroke-width="9"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="16" fill="#13A3A6" stroke="{OBS}" stroke-width="3"/>'
        s += f'<path d="M{cx} {cy + R} V{h - 36} M{cx - 70} {h - 30} H{cx + 70}" stroke="{ga}" stroke-width="14" stroke-linecap="round"/>'
        for i, (w_, c) in enumerate(((240, "#E2533D"), (210, "#13A3A6"), (250, "#F0A21A"))):
            y0 = h - 40 - (i + 1) * 30
            s += f'<rect x="{1260 - w_ / 2}" y="{y0}" width="{w_}" height="28" rx="5" fill="{c}" stroke="{OBS}" stroke-width="3"/>'
            s += f'<path d="M{1260 - w_ / 2 + 12} {y0 + 8} h{w_ - 24}" stroke="#FFFFFF" stroke-opacity=".6" stroke-width="3"/>'
        s += f'<rect x="1150" y="{h - 40}" width="220" height="12" rx="4" fill="{ALTIN_K}"/>'
    else:
        # mekanik saat + yıldız kadranı
        cx, cy, R = 1660, 210, 120
        s += f'<circle cx="{cx}" cy="{cy}" r="{R + 40}" fill="#FFE7A8" opacity=".08"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{LAJVER}" stroke="{ga}" stroke-width="12"/>'
        for k in range(12):
            a = k * math.pi / 6
            s += f'<path d="M{f(cx + (R - 30) * math.cos(a))} {f(cy + (R - 30) * math.sin(a))} L{f(cx + (R - 12) * math.cos(a))} {f(cy + (R - 12) * math.sin(a))}" stroke="{ALTIN_A}" stroke-width="7" stroke-linecap="round"/>'
        s += f'<path d="M{cx} {cy} V{cy - 80} M{cx} {cy} L{cx + 56} {cy + 30}" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="12" fill="{ALTIN}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<path d="M1180 {h - 40} A260 260 0 0 1 1440 {h - 300}" fill="none" stroke="{ga}" stroke-width="10"/>'
        s += f'<path d="M1180 {h - 40} L1440 {h - 300}" stroke="{ALTIN_A}" stroke-width="4" stroke-dasharray="10 8"/>'
    gk = s.lin([(0, "#000000", 0), (1, "#000000", .25)], 0, h - 70, 0, h, kull="userSpaceOnUse", ad="mk")
    s += f'<rect x="0" y="{h - 70}" width="{W}" height="70" fill="{gk}"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ NİŞAN ALBÜMÜ BANDI (2100×h): gün batımında nişan çelengi

def album_bandi(onek="al-bant", h=300):
    s = Svg(onek)
    W = 2100
    ufuk = h - 70
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    s += S.gunes(s, 520, ufuk - 10, 46, hale="#FFC56B", hale_r=480, guc=.95)
    for (x, y, w_, k) in ((140, 90, 420, 14), (1260, 70, 520, 16), (1700, 150, 360, 12)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC59A", "#FF6F8A", .75)
    d, _ = S.dag(s, 900, 1700, ufuk + 4, 1300, 110, 701, renk="#D08AA6", golge="#7E5A92", bicim="volkan", kar_y=150,
                 kar="#FFE3EC", kar_golge="#C7A6CF", sis="#FF9A8A", isik=-1, sirt=4)
    s += d
    s += S.gol(s, 0, ufuk, W, h - ufuk, 702, ufuk="#FFB59A", orta="#C86A9A", derin="#2D3A7A", gunes_x=520, parilti_renk="#FFE3A0")
    # çelenk ipi + boyanmış nişanlar (sağ yarı)
    x0, x1 = 1060, 2140
    s += f'<path d="M{x0} 40 Q{(x0 + x1) / 2} 150 {x1} 30" fill="none" stroke="#5A3A22" stroke-width="5"/>'
    renk = [(GOL, GOL_K), (KOB, KOB_K), (MER, MER_K), (ERGUVAN, "#4E2760"), (KEH, KEH_K), (LAJVER, "#13285E")]
    ik = ["deste", "izotop", "mizan", "karisim", "kale", "ustad"]
    for i in range(6):
        t = (i + .7) / 6.4
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + x1) / 2 + t * t * x1
        y = (1 - t) ** 2 * 40 + 2 * (1 - t) * t * 150 + t * t * 30
        ns = U.nisan(f"{onek}n{i}", nisan_ikonu(ik[i]), renk[i][0], renk[i][1], kurdele="#E2533D")
        ns = ns.replace("<svg ", f'<svg x="{f(x - 62)}" y="{f(y + 6)}" width="124" height="148" ', 1)
        s += f'<path d="M{f(x)} {f(y)} v12" stroke="#5A3A22" stroke-width="3"/>' + ns
    r = RNG(703)
    for k in range(40):
        x, y = r.uniform(900, 2080), r.uniform(10, h - 60)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 11))}" height="{f(r.uniform(3, 5))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")
