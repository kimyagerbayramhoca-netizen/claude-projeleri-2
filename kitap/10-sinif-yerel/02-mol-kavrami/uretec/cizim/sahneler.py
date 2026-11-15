"""Sayfa sahneleri: her durağın başlık bandı (2100×460 birim = 210×46 mm) ve büyük sahneler
(açılış panoraması, Van Kalesi, final). Hepsi koddan üretilir; aynı fonksiyonlar başka ünitede
farklı tohum/renkle yeniden kullanılabilir.

Kompozisyon kuralı (başlık bantları): sol üst ~%48 × %70 alan GÖKYÜZÜ olarak boş bırakılır;
oraya HTML'deki başlık levhası (.levha) oturur. Simge yapılar sağ yarıda ve alt şeritte durur.
"""
import math
from .temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, rng as RNG
from . import sahne as S
from . import yapilar as Y
from .renkler import OBS, GOL, GOL_K, KEH, MER, KOB, ALTIN

W, H = 2100, 460


def _bitir(s, h=H, cls="sahne"):
    return s.cikti(f"0 0 {W} {h}", cls=cls, par="xMidYMid slice")


def _cerceve_golge(s, h=H):
    """Bandın alt kenarına hafif koyulaşma (yazı levhası ve içerikle ayrım)."""
    g = s.lin([(0, "#0E2A3A", 0), (1, "#0E2A3A", .22)], 0, h - 70, 0, h, kull="userSpaceOnUse", ad="cg")
    return f'<rect x="0" y="{h - 70}" width="{W}" height="70" fill="{g}"/>'


# ------------------------------------------------------------------ 1. DURAK · EDREMİT (sabah)

def edremit():
    s = Svg("sh-edr")
    ufuk = 268
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "safak")
    s += S.gunes(s, 1830, 150, 42, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=420, guc=.95)
    s += S.bulut(s, 1250, 140, 260, 4, ust="#FFFFFF", alt="#F6C8D0", op=.95)
    s += S.bulut(s, 1540, 96, 170, 9, ust="#FFFFFF", alt="#F9D3C4", op=.9)
    s += S.bulut(s, 840, 118, 150, 12, ust="#FFFFFF", alt="#E9D3EC", op=.75)
    s += S.bulut_serit(s, 300, 200, 420, 10, "#FFE3EA", "#F6B8C8", .55)
    # uzak kıyı: Süphan (uzakta, sisli) + Nemrut silüeti + Akdamar adası
    uzak = ""
    d, _ = S.dag(s, 380, 1180, ufuk, 760, 120, 21, renk="#B9A9D6", golge="#9286BC", bicim="volkan", kar_y=170,
                 kar="#FFFFFF", kar_golge="#D9D2EE", sis="#F4D3DE", isik=1, sirt=3, puruz=6)
    uzak += d
    d, _ = S.dag(s, -60, 520, ufuk, 160, 190, 22, renk="#A99BCB", golge="#8E83B8", bicim="kaldera", sis="#F2CFE0", isik=1, sirt=2, puruz=5)
    uzak += d
    d, _ = S.dag(s, 1080, 1700, ufuk, 1380, 196, 23, renk="#AE9FCC", golge="#9387BC", bicim="tepe", sis="#F6D6DC", isik=1, sirt=2, puruz=6)
    uzak += d
    s += uzak
    ada = f'<path d="M560 {ufuk + 14} C600 {ufuk - 12} 650 {ufuk - 20} 690 {ufuk - 6} C720 {ufuk + 2} 740 {ufuk + 10} 760 {ufuk + 14} Z" fill="#7F86A8"/>'
    s += S.gol(s, 0, ufuk, W, H - ufuk, 31, ufuk="#FBD9CF", orta="#56C2C0", derin="#0E7480", gunes_x=1830,
               parilti_renk="#FFF1C4", yogunluk=1.2)
    s += S.yansima(s, uzak, ufuk, 0, W, 150, op=.28)
    s += ada
    s += S.tekne(s, 1240, ufuk + 40, 60, govde="#2B50B5", ust="#F4E9D8", yelken="#FFF6E6")
    s += S.tekne(s, 1520, ufuk + 26, 40, govde="#C8442F")
    # sağ kıyı: kavaklar, bahçeler, evler
    kiyi = [(1560, H), (1580, 362), (1660, 340), (1780, 330), (1900, 318), (2000, 312), (2100, 302), (2100, H)]
    g = s.lin([(0, "#8DBA5C"), (1, "#4E8A3E")], 0, 300, 0, H, kull="userSpaceOnUse", ad="kiyi")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {H} Z" fill="{g}"/>'
    for i, (x, h) in enumerate([(1640, 120), (1668, 142), (1696, 116), (1830, 150), (1860, 128), (1892, 160), (2040, 150), (2072, 170)]):
        s += S.kavak(s, x, 356 - (x - 1600) * .05, h, 26, 40 + i, renk="#5FA548", isik=1)
    for i, x in enumerate((1745, 1785, 1985)):
        s += S.agac(s, x, 344 - (x - 1600) * .04, 28, 60 + i, renk="#78B651", isik=1, meyve="#E2533D" if i % 2 else None)
    for i, x in enumerate((1925,)):
        s += S.ev(x, 326, 50, 36, 70 + i, duvar="#EFD9B6", cati="#C2563A", isik=1)
    # ön plan: ahşap çay iskelesi + masa + semaver + bardaklar
    s += Y.iskele(s, 1300, 1620, 398, 18, 3, ahsap="#A8743F", merdiven=False)
    s += f'<rect x="1330" y="352" width="140" height="8" rx="3" fill="#8C5A2E"/><path d="M1344 360 v34 M1456 360 v34" stroke="#6E4422" stroke-width="6"/>'
    s += f'<path d="M1322 352 h156" stroke="#F5E8D0" stroke-width="3"/>'
    s += Y.semaver(s, 1375, 352, 70)
    s += Y.cay_bardak_kucuk(1420, 352, 19)
    s += Y.cay_bardak_kucuk(1446, 352, 19)
    # sol alt: sazlık + su
    s += S.sazlik(0, 260, 460, 5, boy=70)
    s += S.marti(1100, 150, 1.0, 2)
    s += S.marti(1160, 175, .7, -2)
    s += S.marti(560, 130, .6, 3)
    s += S.marti(1180, 420, 1.15, 6, ayrintili=True)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 2. DURAK · GEVAŞ (öğle, Halime Hatun Kümbeti)

def gevas():
    s = Svg("sh-gev")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gun")
    s += S.gunes(s, 260, 70, 34, hale="#FFF2C2", hale_r=320, guc=.8)
    for i, (x, y, w) in enumerate([(700, 120, 230), (1080, 96, 280), (1500, 140, 200), (380, 180, 150)]):
        s += S.bulut(s, x, y, w, 30 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    # Artos dağı (arka) + gölün öte yakası
    uzak = ""
    d, _ = S.dag(s, 900, 2200, ufuk, 1620, 70, 41, renk="#6F9AC2", golge="#4F79A8", bicim="sivri", kar_y=118,
                 kar="#FFFFFF", kar_golge="#C9DAEE", sis="#BFE0F0", isik=-1, sirt=5)
    uzak += d
    d, _ = S.dag(s, -80, 760, ufuk, 300, 190, 42, renk="#8FB4D2", golge="#7099C0", bicim="tepe", sis="#D6ECF5", isik=-1, sirt=2, puruz=5)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, H - ufuk, 43, ufuk="#C8EEF0", orta="#22AEB0", derin="#0B6B78", yogunluk=1.2)
    s += S.yansima(s, uzak, ufuk, 0, W, 140, op=.25)
    # Akdamar adası (yalnız ada; ağaçlı tepecik)
    s += f'<path d="M520 {ufuk + 22} C560 {ufuk - 14} 640 {ufuk - 30} 700 {ufuk - 12} C740 {ufuk} 770 {ufuk + 12} 800 {ufuk + 22} Z" fill="#6E8F5C"/>'
    s += f'<path d="M600 {ufuk - 18} C640 {ufuk - 34} 690 {ufuk - 30} 720 {ufuk - 8} L690 {ufuk + 4} Z" fill="#88A86A"/>'
    for i, x in enumerate((600, 630, 660, 700)):
        s += S.kavak(s, x, ufuk - 4 + (abs(x - 650) * .15), 40, 9, 300 + i, renk="#4E7D45")
    s += S.tekne(s, 900, ufuk + 60, 80, govde="#F4E9D8", yelken="#E2533D")
    # ön kıyı ve kümbet
    kiyi = [(1100, H), (1180, 350), (1400, 330), (1700, 326), (1950, 334), (2100, 340), (2100, H)]
    g = s.lin([(0, "#A9C76B"), (1, "#5F9442")], 0, 320, 0, H, kull="userSpaceOnUse", ad="gk")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {H} Z" fill="{g}"/>'
    for i, (x, h) in enumerate([(1230, 150), (1265, 170), (1300, 140), (2000, 190), (2040, 160), (2075, 175)]):
        s += S.kavak(s, x, 352, h, 28, 310 + i, renk="#5A9C47")
    s += Y.kumbet(s, 1640, 360, 270, 5, tas="#D7A47B", cati="#B9825E")
    for i, x in enumerate((1450, 1820, 1890)):
        s += S.agac(s, x, 352, 32, 330 + i, renk="#7DB955", meyve="#E2533D" if i == 1 else None)
    s += S.cimen(1100, 2100, 420, 7, renk="#5C9A40", renk2="#86C25A", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += S.sazlik(0, 220, 460, 8, boy=60)
    s += S.marti(1000, 140, .9, 2)
    s += S.marti(1060, 160, .6, -1)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 3. DURAK · TATVAN (ikindi, Nemrut kalderası, feribot)

def tatvan():
    s = Svg("sh-tat")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "altin")
    s += S.gunes(s, 520, 110, 36, hale="#FFE0A0", hale_r=360, guc=.85)
    for i, (x, y, w) in enumerate([(820, 120, 240), (1180, 92, 200), (300, 200, 150)]):
        s += S.bulut(s, x, y, w, 50 + i, ust="#FFFFFF", alt="#F5D9B5", op=.95)
    # Nemrut: geniş kalderalı volkan (sağ yarı, büyük)
    d, sirt = S.dag(s, 980, 2240, ufuk + 10, 1620, 96, 61, renk="#7A6E86", golge="#4F4560", bicim="kaldera",
                    sis="#E8C9A4", isik=-1, sirt=6, puruz=10, kenar_isik="#F8D6A8")
    s += d
    # kaldera gölü parıltısı (tepede)
    s += f'<path d="M1500 {104} Q1620 {92} 1740 {104} Q1620 {112} 1500 {104} Z" fill="#7FD3CF" opacity=".75"/>'
    d2, _ = S.dag(s, -60, 820, ufuk, 340, 200, 62, renk="#9C8FA6", golge="#7E7190", bicim="tepe", sis="#F3D9B8", isik=-1, sirt=2, puruz=5)
    s += d2
    s += S.gol(s, 0, ufuk, W, H - ufuk, 63, ufuk="#F6E1C0", orta="#3AB3B0", derin="#0B6170", gunes_x=520, parilti_renk="#FFF0C0")
    s += S.yansima(s, d + d2, ufuk, 0, W, 150, op=.25)
    # Tatvan kasabası (Nemrut eteği)
    for i in range(14):
        x = 1180 + i * 52 + (i % 3) * 7
        yy = ufuk + 6 - (i % 4) * 3
        s += S.ev(x, yy, 38 + (i % 3) * 6, 26 + (i % 2) * 6, 400 + i, duvar=["#F1E1C6", "#E7CDA6", "#F6EBDA"][i % 3], cati="#B8553A", duz=i % 2 == 0)
    # feribot (vagonlu)
    s += f'<path d="M1180 {ufuk + 92} q130 10 260 0 q130 -10 260 0" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".6"/>'
    s += S.feribot(s, 1420, ufuk + 80, 400)
    # ön plan: obsidyenli kayalık (sağ alt)
    kiyi = [(1500, H), (1560, 400), (1700, 380), (1900, 372), (2100, 366), (2100, H)]
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {H} Z" fill="#4A4552"/>'
    s += S.kaya(s, 1640, 420, 140, 60, 70, renk="#5A5463")
    s += S.kaya(s, 1980, 410, 180, 70, 71, renk="#4E4858")
    s += Y.obsidyen(s, 1780, 430, 120, 70, 72)
    s += Y.obsidyen(s, 1880, 440, 90, 50, 73)
    s += S.cimen(1500, 2100, 455, 74, renk="#6E7A3E", renk2="#94A055", boy=10)
    s += S.marti(760, 200, .8, 2)
    s += S.marti(830, 220, .55, -1)
    s += S.kefal(s, 1240, 430, 60, -30)
    s += S.damla_sicrama(1212, 448, .8)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 4. DURAK · AHLAT (altın saat, Selçuklu mezar taşları)

def ahlat():
    s = Svg("sh-ahl")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#4F7FC0"), (.4, "#A7C0DC"), (.75, "#F8D9A8"), (1, "#FFCB86")])
    s += S.gunes(s, 140, 200, 40, hale="#FFC26B", hale_r=420, guc=.9)
    for i, (x, y, w) in enumerate([(600, 70, 220), (980, 110, 260), (1400, 60, 220)]):
        s += S.bulut(s, x, y, w, 80 + i, ust="#FFF6E8", alt="#F2C9A0", op=.95)
    uzak = ""
    d, _ = S.dag(s, 1100, 2000, ufuk, 1540, 90, 81, renk="#C9A8B6", golge="#8F7CA0", bicim="volkan", kar_y=150,
                 kar="#FFF1E6", kar_golge="#CDBCDC", sis="#F6D2B8", isik=-1, sirt=4, kenar_isik="#FFE3C8")
    uzak += d
    d, _ = S.dag(s, 400, 1260, ufuk, 820, 196, 82, renk="#B9A4B8", golge="#9887A6", bicim="tepe", sis="#F7D8BC", isik=-1, sirt=2, puruz=5)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, 80, 83, ufuk="#FBD8B0", orta="#6BBFC0", derin="#2A7F8C", gunes_x=140, parilti_renk="#FFE7B0")
    s += S.yansima(s, uzak, ufuk, 0, W, 80, op=.28)
    # mezarlık arazisi (sarı-yeşil bozkır)
    zem = [(0, 342), (300, 330), (700, 338), (1100, 326), (1500, 334), (1900, 322), (2100, 330)]
    g = s.lin([(0, "#D8C077"), (1, "#8E9A4C")], 0, 320, 0, H, kull="userSpaceOnUse", ad="az")
    s += f'<path d="{egri_d(zem)} L2100 {H} L0 {H} Z" fill="{g}"/>'
    # Ulu Kümbet ve kavaklar (arka)
    for i, x in enumerate((1370, 1400, 1890, 1920, 1955)):
        s += S.kavak(s, x, 336, 140 + (i % 2) * 30, 26, 90 + i, renk="#7AA04A", isik=-1)
    s += Y.kumbet(s, 1560, 340, 220, 7, tas="#B97A55", cati="#9C6243", kenar=12)
    # mezar taşları: üç sıra, perspektif
    r = RNG(86)
    sira = [(352, .55, 20), (392, .78, 16), (440, 1.0, 11)]
    k = 0
    for yb, olc, n in sira:
        xs = [1020 + i * (1080 / n) + r.uniform(-12, 12) for i in range(n)]
        for x in xs:
            h = r.uniform(120, 190) * olc
            s += Y.mezar_tasi(s, x, yb + r.uniform(-4, 4), h * r.uniform(.3, .38), h, 100 + k,
                              renk=r.choice(["#B8673E", "#A8593A", "#C27A4E", "#9C5A3C"]), egim=r.uniform(-7, 7), isik=-1,
                              sade=olc < .6)
            k += 1
        s += S.cimen(980, 2100, yb + 4, 200 + k, renk="#8C9A48", renk2="#B8B862", boy=10 * olc + 4, yogun=.6)
    s += S.marti(700, 200, .7, 2)
    s += S.marti(760, 222, .5, -1)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 5. DURAK · ADİLCEVAZ (Süphan + kıyı kalesi)

def adilcevaz():
    s = Svg("sh-adi")
    ufuk = 296
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gun")
    s += S.gunes(s, 230, 120, 34, hale="#FFF2C2", hale_r=300, guc=.8)
    for i, (x, y, w) in enumerate([(560, 120, 200), (1900, 60, 160)]):
        s += S.bulut(s, x, y, w, 120 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    d, _ = S.dag(s, 760, 2180, ufuk, 1480, 34, 121, renk="#7C93B5", golge="#55709A", bicim="volkan", kar_y=150,
                 kar="#FFFFFF", kar_golge="#C9D8EE", sis="#C4E2EE", isik=-1, sirt=7, puruz=9, kenar_isik="#EAF4FF")
    s += d
    d2, _ = S.dag(s, -80, 900, ufuk, 300, 220, 122, renk="#9DB8CF", golge="#7E9EBB", bicim="tepe", sis="#D6ECF5", isik=-1, sirt=2, puruz=5)
    s += d2
    # yamaç ormanı / bahçeler (Süphan eteği)
    s += S.tepe_bandi(s, 700, 2100, ufuk + 6, 34, 123, "#7FA35A", "#5F8A44")[0]
    for i in range(16):
        x = 820 + i * 80
        s += S.agac(s, x, ufuk + 8 + (i % 3) * 4, 18 + (i % 4) * 3, 130 + i, renk="#6FA34B", isik=-1)
    s += S.gol(s, 0, ufuk + 8, W, H - ufuk - 8, 124, ufuk="#C8EEF0", orta="#22AEB0", derin="#0B6B78")
    s += S.yansima(s, d, ufuk + 8, 0, W, 140, op=.22)
    # kıyı (sağdan uzanan burun) + kıyı kalesi
    kiyi = [(1380, H), (1420, ufuk + 92), (1560, ufuk + 70), (1800, ufuk + 62), (2100, ufuk + 48), (2100, H)]
    gk = s.lin([(0, "#9DBB62"), (1, "#5F8A44")], 0, ufuk + 40, 0, H, kull="userSpaceOnUse", ad="ak")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {H} Z" fill="{gk}"/>'
    s += f'<path d="M1400 {ufuk + 96} q120 -10 260 -24" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".7"/>'
    s += Y.kucuk_kale(s, 1640, ufuk + 76, 300, 190, 125, tas="#C9A57A")
    s += S.cimen(1400, 2100, ufuk + 150, 126, renk="#5C9A40", renk2="#86C25A", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += S.agac(s, 2010, 430, 58, 140, renk="#5E9A43", isik=-1, meyve="#7A4E2A")
    s += S.tekne(s, 1150, ufuk + 80, 80, govde="#C8442F", yelken="#FFF6E6")
    s += S.tekne(s, 1300, ufuk + 110, 60, govde="#2B50B5")
    s += S.sazlik(0, 240, 460, 9, boy=60)
    s += S.marti(1100, 200, .8, 2)
    s += S.marti(1180, 230, .6, -2)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ HÜLASA · SÜPHAN ETEĞİ (yayla)

def suphan():
    s = Svg("sh-sup")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk, duraklar=[(0, "#3E86CC"), (.55, "#94CBEA"), (1, "#E9F6FA")])
    s += S.gunes(s, 330, 90, 32, hale="#FFF4CC", hale_r=300, guc=.8)
    for i, (x, y, w) in enumerate([(700, 120, 200), (1840, 100, 170)]):
        s += S.bulut(s, x, y, w, 160 + i, op=.95)
    d, _ = S.dag(s, 620, 2240, ufuk + 20, 1360, 26, 161, renk="#8199BB", golge="#5A74A0", bicim="volkan", kar_y=170,
                 kar="#FFFFFF", kar_golge="#C6D6EE", sis="#D3EAF3", isik=-1, sirt=8, puruz=10, kenar_isik="#F2F8FF")
    s += d
    s += S.tepe_bandi(s, 0, 2100, ufuk + 40, 40, 162, "#9CC66A", "#79AA52")[0]
    s += S.tepe_bandi(s, 0, 2100, ufuk + 92, 36, 163, "#86BC5A", "#5E9A44")[0]
    # göl parıltısı (sol uzakta)
    s += f'<path d="M0 {ufuk + 26} C200 {ufuk + 14} 420 {ufuk + 18} 560 {ufuk + 32} L560 {ufuk + 44} L0 {ufuk + 50} Z" fill="#3DB7B5"/>'
    s += f'<path d="M30 {ufuk + 32} h120 M220 {ufuk + 30} h90 M380 {ufuk + 36} h70" stroke="#FFFFFF" stroke-width="3" opacity=".6"/>'
    # dere
    s += f'<path d="M1180 {ufuk + 56} C1150 {ufuk + 90} 1260 {ufuk + 110} 1200 {ufuk + 160} L1260 {ufuk + 160} C1320 {ufuk + 110} 1210 {ufuk + 90} 1230 {ufuk + 56} Z" fill="#6CCFD0"/>'
    # çadır, koyun sürüsü, çiçekler
    s += Y.cadir(s, 1560, ufuk + 112, 150, 110, renk="#9E2F28")
    s += Y.cadir(s, 1720, ufuk + 100, 110, 80, renk="#253C78", serit="#F0A21A")
    r = RNG(170)
    for k in range(18):
        x = 820 + r.uniform(0, 680)
        y = ufuk + 70 + r.uniform(0, 80)
        s += Y.koyun(x, y, 1.0 + (y - ufuk - 70) / 80 * .8, r.choice([1, -1]))
    s += S.cimen(0, 2100, H - 4, 171, renk="#4E8F3A", renk2="#7DBE55", boy=16, yogun=1.3,
                 cicek=["#FFFFFF", "#F0A21A", "#E2533D", "#B07CD8", "#FFD24A"])
    s += S.cimen(700, 2100, ufuk + 150, 172, renk="#5C9A40", renk2="#86C25A", boy=12, yogun=.8,
                 cicek=["#FFFFFF", "#F0A21A", "#E2533D", "#B07CD8"])
    s += S.marti(1000, 150, .7, 2, renk="#3A3E4A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ MECLİS · ERCİŞ (köy odası, iç mekân)

def ercis():
    from .sus import kilim_serit
    s = Svg("sh-erc")
    g = s.lin([(0, "#F7E7CB"), (1, "#EBD3AC")], 0, 0, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect width="{W}" height="{H}" fill="{g}"/>'
    s += f'<rect y="0" width="{W}" height="34" fill="#7A4E2E"/><rect y="34" width="{W}" height="8" fill="#5E3A20"/>'
    for x in range(0, W, 120):
        s += f'<rect x="{x}" y="0" width="60" height="34" fill="#8C5A35"/>'
    # pencere: göl ve Süphan (sağda) — sedir yastığının (y=246) üstünde biter
    wx, wy, ww, wh = 1360, 52, 440, 180
    pen = Svg("sh-erc-p")
    pen += S.gokyuzu(pen, wx, wy, ww, wh * .6, "gun")
    pd, _ = S.dag(pen, wx - 40, wx + ww + 40, wy + wh * .6, wx + ww * .55, wy + 22, 181, renk="#7C93B5", golge="#55709A",
                  bicim="volkan", kar_y=wy + 66, kar="#FFFFFF", kar_golge="#C9D8EE", sis="#C4E2EE", isik=-1, sirt=4, puruz=6)
    pen += pd
    pen += S.gol(pen, wx, wy + wh * .6, ww, wh * .4, 182, ufuk="#C8EEF0", orta="#22AEB0", derin="#0B6B78")
    pen += S.tekne(pen, wx + 110, wy + wh * .8, 40, govde="#C8442F", yelken="#FFF6E6")
    pen += S.marti(wx + 310, wy + 40, .6, 2)
    s.defs += pen.defs
    kl = s.klip(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}"/>', ad="pk")
    s += f'<g clip-path="{kl}">{"".join(pen.parca)}</g>'
    s += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#6E4422" stroke-width="14"/>'
    s += f'<path d="M{wx + ww / 2} {wy} V{wy + wh} M{wx} {wy + wh * .45} H{wx + ww}" stroke="#6E4422" stroke-width="8"/>'
    s += f'<rect x="{wx - 22}" y="{wy + wh + 2}" width="{ww + 44}" height="12" fill="#8C5A35"/>'
    for sx, x0 in ((-1, wx - 58), (1, wx + ww + 6)):
        s += (f'<path d="M{x0} 46 h52 C{x0 + 52} 120 {x0 + 26 + sx * 9} 190 {x0 + 42} 240 L{x0 + 8} 240 C{x0 - 8} 186 {x0 + 8} 116 {x0} 46 Z" fill="#B23A2E"/>'
              f'<path d="M{x0 + 15} 54 C{x0 + 17} 124 {x0 + 11} 192 {x0 + 20} 236" stroke="#8E2A22" stroke-width="5" fill="none"/>'
              f'<path d="M{x0} 46 h52" stroke="#F0A21A" stroke-width="7"/>')
        for k in range(4):
            s += f'<circle cx="{x0 + 12 + k * 8}" cy="{92 + k * 40}" r="3.6" fill="#F0A21A" opacity=".9"/>'
    # duvarda kilim (en sağ, sedirin üstünde biter)
    s += f'<g transform="translate(1912 52)"><rect width="168" height="168" fill="#F5E8D0" stroke="#6E4422" stroke-width="4"/>'
    s += f'<rect x="8" y="8" width="152" height="152" fill="#B23A2E"/>'
    for k in range(2):
        cy = 48 + k * 72
        s += f'<path d="M84 {cy - 30} L124 {cy} L84 {cy + 30} L44 {cy} Z" fill="#253C78"/><path d="M84 {cy - 17} L106 {cy} L84 {cy + 17} L62 {cy} Z" fill="#D99A2B"/><rect x="79" y="{cy - 5}" width="10" height="10" fill="#F5E8D0"/>'
        s += f'<path d="M22 {cy - 18} v36 M146 {cy - 18} v36" stroke="#1E8A86" stroke-width="9"/>'
    s += "".join(f'<path d="M{6 + k * 17} 168 v14" stroke="#F5E8D0" stroke-width="4"/>' for k in range(10)) + '</g>'
    # sol duvar: raf, kitaplar, semaver (levhanın arkasında kalsa da doku verir)
    s += f'<rect x="760" y="150" width="260" height="12" fill="#7A4E2E"/>'
    for k, (c, h) in enumerate([("#2B50B5", 60), ("#E2533D", 70), ("#13A3A6", 54), ("#F0A21A", 66), ("#1D3A8A", 60), ("#7B3F8C", 72)]):
        s += f'<rect x="{770 + k * 26}" y="{150 - h}" width="22" height="{h}" fill="{c}" stroke="#1B1D26" stroke-width="2"/>'
    s += Y.semaver(s, 960, 150, 80)
    # sedir ve minderler
    s += f'<rect x="0" y="322" width="{W}" height="62" fill="#8E2A22"/>'
    kil = kilim_serit("sh-erc-k", 2100, 60).replace("<svg ", '<svg width="2100" height="60" ')
    s += f'<g transform="translate(0 324)">{kil}</g>'
    # sedirin sırt yastığı: kesintisiz uzun minder (yer yer örtülse de tek parça okunur) + kilim deseni
    s += f'<rect x="-20" y="246" width="{W + 40}" height="84" rx="26" fill="#253C78" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<rect x="-20" y="258" width="{W + 40}" height="60" fill="#2E4A8E"/>'
    s += f'<path d="M-20 262 H{W + 20} M-20 314 H{W + 20}" stroke="#D99A2B" stroke-width="4"/>'
    for x in range(30, W, 72):
        s += f'<path d="M{x} 266 L{x + 22} 288 L{x} 310 L{x - 22} 288 Z" fill="#B23A2E" stroke="#F5E8D0" stroke-width="2.4"/><rect x="{x - 4}" y="284" width="8" height="8" fill="#F5E8D0"/>'
    for x in range(66, W, 72):
        s += f'<path d="M{x} 280 l8 8 l-8 8 l-8 -8 Z" fill="#D99A2B"/>'
    s += f'<path d="M0 384 H{W} V{H} H0 Z" fill="#7A2A22"/>'
    s += f'<path d="M80 394 H{W - 80} L{W} {H} H0 Z" fill="#B23A2E"/>'
    for x in range(120, W - 100, 90):
        s += f'<path d="M{x} 406 l20 14 l-20 14 l-20 -14 Z" fill="#D99A2B"/>'
    # meclistekiler (sağdaki sahne alanında) + sini
    s += '<use href="#elif-soru" x="1290" y="178" width="260" height="273"/>'
    s += '<use href="#yusuf-anlatan" x="1790" y="178" width="260" height="273"/>'
    s += f'<ellipse cx="1676" cy="440" rx="130" ry="20" fill="#C9A86A" stroke="#7A5A2A" stroke-width="4"/>'
    for k, x in enumerate((1606, 1648, 1690, 1732)):
        s += Y.cay_bardak_kucuk(x, 440, 26)
    s += '<use href="#pamuk-dusunen" x="1580" y="236" width="180" height="206"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ KISSA · MURADİYE (şelale, asma köprü, kefaller)

def muradiye():
    s = Svg("sh-mur")
    s += S.gokyuzu(s, 0, 0, W, 300, duraklar=[(0, "#4C95D6"), (.6, "#A6D8F0"), (1, "#E6F6F8")])
    s += S.gunes(s, 1960, 70, 30, hale="#FFF4CC", hale_r=260, guc=.8)
    s += S.bulut(s, 1380, 96, 170, 190, op=.95)
    s += S.bulut(s, 700, 80, 160, 191, op=.9)
    d, _ = S.dag(s, 1100, 2150, 250, 1700, 110, 192, renk="#8FAAC4", golge="#6E8AAE", bicim="sivri", sis="#D2EAF4", isik=-1, sirt=3, puruz=12)
    s += d
    s += S.tepe_bandi(s, 0, 2100, 262, 50, 193, "#6E9E4E", "#4E7E3A")[0]
    for k in range(22):
        x = 40 + k * 95
        s += S.agac(s, x, 262 + (k % 3) * 6, 26 + (k % 4) * 4, 194 + k, renk=["#4E8A3E", "#5FA048", "#3F7A36"][k % 3])
    # bazalt uçurum (sütunlu) + geniş perde şelale (sağ yarı)
    cx = 1680
    kaya = [(cx - 300, H), (cx - 290, 300), (cx - 240, 252), (cx - 140, 226), (cx, 222), (cx + 140, 228), (cx + 240, 254), (cx + 290, 300), (cx + 300, H)]
    gk = s.lin([(0, "#535866"), (1, "#24262E")], 0, 220, 0, H, kull="userSpaceOnUse", ad="bz")
    s += f'<path d="{egri_d(kaya, True)}" fill="{gk}"/>'
    r = RNG(195)
    for k in range(30):
        x = cx - 288 + k * 19.5
        top = 236 + abs(x - cx) * .16 + r.uniform(-4, 8)
        s += f'<path d="M{f(x)} {f(top)} l8 -5 l8 5 V{H} h-16 Z" fill="{["#3A3E4A", "#454A57", "#30333D"][k % 3]}" opacity=".85"/>'
    s += Y.selale(s, cx, 232, 404, 330, 196, kaya="#2F3340")
    g = s.lin([(0, "#BDEBEC"), (1, "#2A9FA6")], 0, 390, 0, H, kull="userSpaceOnUse", ad="nh")
    s += f'<path d="M0 410 C400 396 900 404 1200 398 C1500 392 1800 400 2100 396 V{H} H0 Z" fill="{g}"/>'
    s += S.dalga_cizgileri(0, 410, 2100, 50, 197, n=40, op=.7)
    s += Y.gokkusagi(s, cx, 400, 230, 9, op=.5)
    s += Y.asma_kopru(s, cx - 330, cx + 330, 300, 26, 56)
    for k, (x, y, a) in enumerate([(1500, 404, -38), (1760, 398, -30), (1890, 412, -42), (1280, 422, -26), (900, 430, -30)]):
        s += S.kefal(s, x, y, 54, a)
        s += S.damla_sicrama(x - 22, y + 16, .7)
    for k, x in enumerate((1290, 1325, 1360, 2020, 2055, 2090)):
        s += S.kavak(s, x, 400, 150 + (k % 3) * 20, 26, 200 + k, renk="#4F8F45")
    s += S.cimen(1200, 2100, 404, 201, renk="#3F7A36", renk2="#6EA84E", boy=12)
    s += S.marti(1450, 170, .7, 2, renk="#3A3E4A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ ANAHTAR · VAN İSKELESİ (akşamüstü)

def iskele():
    s = Svg("sh-isk")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#3A4C9C"), (.4, "#8E7BC0"), (.72, "#F7A6A0"), (1, "#FFD39A")])
    s += S.gunes(s, 1370, 236, 38, hale="#FFC27A", hale_r=380, guc=.9)
    s += S.bulut_serit(s, 1200, 150, 520, 14, "#FFD0C4", "#F28FA0", .7)
    s += S.bulut_serit(s, 1500, 96, 480, 12, "#FFC9B8", "#E9849C", .6)
    uzak = ""
    d, _ = S.dag(s, -60, 900, ufuk, 340, 196, 210, renk="#8E7BA8", golge="#6E5C8E", bicim="tepe", sis="#F6B8A8", isik=1, sirt=2, puruz=5)
    uzak += d
    vk, _ = Y.van_kalesi(s, 1640, 2100, ufuk, 110, 211, tas="#9C7F8E", golge="#7A6070", sur="#A98C9A", ayrinti=.5)
    uzak += vk
    s += uzak
    s += S.gol(s, 0, ufuk, W, H - ufuk, 212, ufuk="#FBC9A8", orta="#5E8FB0", derin="#1D3F6A", gunes_x=1370, parilti_renk="#FFE2A8")
    s += S.yansima(s, uzak, ufuk, 0, W, 120, op=.28)
    s += S.feribot(s, 1930, ufuk + 56, 300, govde="#F4F1EA")
    # iskele (perspektif: aşağı doğru genişler)
    x0u, x1u = 1450, 1630
    s += f'<path d="M{x0u} {ufuk + 50} L{x1u} {ufuk + 50} L{x1u + 120} {H} L{x0u - 220} {H} Z" fill="#9A6B42"/>'
    for k in range(14):
        t = k / 14
        y = ufuk + 50 + (H - ufuk - 50) * t ** 1.3
        s += f'<path d="M{f(x0u - 220 * t ** 1.3)} {f(y)} H{f(x1u + 120 * t ** 1.3)}" stroke="#6E4A2C" stroke-width="{f(1 + 2 * t)}"/>'
    for k, (x, y, h) in enumerate([(x0u + 8, ufuk + 50, 28), (x1u - 8, ufuk + 50, 28), (x0u - 60, ufuk + 110, 44), (x1u + 30, ufuk + 110, 44), (x0u - 150, ufuk + 160, 60)]):
        s += f'<rect x="{x - h * .12}" y="{y - h}" width="{h * .24}" height="{h}" fill="#5A3A22"/>'
        s += f'<circle cx="{x}" cy="{y - h}" r="{h * .14}" fill="#FFD27A"/>'
    for k in range(6):
        s += f'<rect x="{x1u + 40 + k * 16}" y="{ufuk + 96 + k * 22}" width="70" height="12" fill="#B07C4A" stroke="#5A3A22" stroke-width="2"/>'
    s += Y.fener(s, (x0u + x1u) / 2, ufuk + 44, 130)
    s += f'<path d="M{x0u - 120} {H - 16} q60 30 120 0" stroke="#E8D3A8" stroke-width="6" fill="none"/>'
    s += S.marti(1250, 140, 1.0, 2, renk="#2F2A4A")
    s += S.marti(1310, 168, .7, -2, renk="#2F2A4A")
    s += S.marti(1180, 410, 1.1, 4, ayrintili=True)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ BÜYÜK İMTİHAN · VAN KALESİ (büyük, 62 mm)

def kale_buyuk(h=620):
    s = Svg("sh-kal")
    ufuk = 430
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#2F5DA8"), (.38, "#86A9D6"), (.7, "#F6C99A"), (1, "#FFB46B")])
    s += S.gunes(s, 230, 330, 52, hale="#FFB45A", hale_r=520, guc=.95)
    for i, (x, y, w) in enumerate([(520, 150, 300), (980, 96, 360), (1500, 150, 280), (1850, 80, 220)]):
        s += S.bulut(s, x, y, w, 220 + i, ust="#FFF4E4", alt="#F0A98A", op=.95)
    s += S.bulut_serit(s, 300, 250, 600, 16, "#FFD8B0", "#F08A7A", .6)
    uzak = ""
    d, _ = S.dag(s, 1200, 2240, ufuk, 1820, 230, 223, renk="#B78FA8", golge="#8C6A92", bicim="sivri", kar_y=268,
                 kar="#FFE8E4", kar_golge="#D2B6CC", sis="#F7C2A8", isik=-1, sirt=4, kenar_isik="#FFD9C0")
    uzak += d
    d, _ = S.dag(s, -80, 760, ufuk, 300, 330, 224, renk="#A58DAE", golge="#87709A", bicim="tepe", sis="#F6C3AA", isik=-1, sirt=2, puruz=5)
    uzak += d
    s += uzak
    # göl (sol yarı) ve kıyı
    s += S.gol(s, 0, ufuk, W, h - ufuk, 225, ufuk="#FFD2A8", orta="#4FAFB4", derin="#0F5A6E", gunes_x=230, parilti_renk="#FFE3A8")
    # kale kayası
    vk, ust = Y.van_kalesi(s, 700, 2060, ufuk + 70, 330, 226, tas="#D9BE92", golge="#9C7E5E", sur="#E6CFA4", isik=-1, ayrinti=1.2, bayrak=True)
    s += S.yansima(s, uzak + vk, ufuk + 70, 600, W - 600, 130, op=.25)
    s += vk
    # eski şehir kalıntıları ve kavaklar (kaya önü)
    zem = [(640, h), (700, ufuk + 90), (1000, ufuk + 80), (1500, ufuk + 86), (2100, ufuk + 76), (2100, h)]
    gz = s.lin([(0, "#B8A86A"), (1, "#6E8A44")], 0, ufuk + 70, 0, h, kull="userSpaceOnUse", ad="kz")
    s += f'<path d="{egri_d(zem[:-1])} L2100 {h} Z" fill="{gz}"/>'
    r = RNG(227)
    for k in range(9):
        x = 760 + k * 150 + r.uniform(-20, 20)
        yy = ufuk + 110 + r.uniform(0, 30)
        ww = r.uniform(60, 120)
        s += f'<path d="M{f(x)} {f(yy)} v{f(-r.uniform(20, 40))} h{f(ww * .3)} v{f(r.uniform(8, 16))} h{f(ww * .4)} v{f(-r.uniform(10, 20))} h{f(ww * .3)} V{f(yy)} Z" fill="#C9A87A" stroke="#8C6E4A" stroke-width="2"/>'
    for k in range(12):
        x = 680 + k * 120 + r.uniform(-30, 30)
        s += S.kavak(s, x, ufuk + 140 + r.uniform(0, 20), r.uniform(120, 180), 26, 228 + k, renk="#6E9A44", isik=-1)
    s += S.cimen(640, 2100, h - 4, 229, renk="#5E8A3E", renk2="#8DB85A", boy=16, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    # ön plan sol: kıyı sazlığı + tekneler
    s += S.tekne(s, 300, ufuk + 110, 90, govde="#2B50B5", yelken="#FFF1DE")
    s += S.tekne(s, 520, ufuk + 150, 70, govde="#C8442F")
    s += S.sazlik(0, 400, h, 230, boy=90)
    for k, (x, y, o) in enumerate([(820, 200, 1.1), (900, 236, .8), (1300, 120, .7), (1360, 150, .5)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ BÜYÜK İMTİHAN 2 · KALE KAPISI (30 mm)

def kale_kapi(h=300):
    s = Svg("sh-kap")
    s += S.gokyuzu(s, 0, 0, W, h, duraklar=[(0, "#F7B07A"), (1, "#FFE1B0")])
    # sur duvarı (taş örgü)
    g = s.lin([(0, "#E3C79A"), (1, "#B8946A")], 0, 40, 0, h, kull="userSpaceOnUse", ad="sd")
    s += f'<rect x="0" y="60" width="{W}" height="{h - 60}" fill="{g}"/>'
    r = RNG(240)
    for row in range(8):
        y = 60 + row * 32
        off = 0 if row % 2 == 0 else 40
        for x in range(-40 + off, W, 80):
            s += f'<rect x="{x + 2}" y="{y + 2}" width="76" height="28" rx="3" fill="{karis("#E3C79A", "#B8946A", r.uniform(0, .6))}" stroke="#8C6E4A" stroke-width="1.6"/>'
    # mazgallar
    for x in range(0, W, 110):
        s += f'<rect x="{x}" y="20" width="70" height="44" fill="#E3C79A" stroke="#8C6E4A" stroke-width="2.4"/>'
    s += f'<rect x="0" y="58" width="{W}" height="10" fill="#9C7E5E"/>'
    # kapı (sivri kemer) + aralık ışık
    cx, ky = 1450, h
    s += f'<path d="M{cx - 170} {ky} V140 Q{cx - 170} 70 {cx} 52 Q{cx + 170} 70 {cx + 170} 140 V{ky} Z" fill="#8C6E4A"/>'
    s += f'<path d="M{cx - 140} {ky} V146 Q{cx - 140} 92 {cx} 78 Q{cx + 140} 92 {cx + 140} 146 V{ky} Z" fill="#3A2614"/>'
    isik = s.rad([(0, "#FFF4C8", .95), (.5, "#FFD27A", .5), (1, "#FFD27A", 0)], cx, 200, 260, kull="userSpaceOnUse", ad="ki")
    s += f'<path d="M{cx - 30} {ky} V96 L{cx + 30} 96 V{ky} Z" fill="#FFE9A8"/>'
    s += f'<path d="M{cx - 30} {ky} L{cx - 400} {ky} L{cx - 30} 120 Z M{cx + 30} {ky} L{cx + 400} {ky} L{cx + 30} 120 Z" fill="#FFE9A8" opacity=".35"/>'
    s += f'<circle cx="{cx}" cy="200" r="260" fill="{isik}"/>'
    for sx in (-1, 1):
        x0 = cx + sx * 30
        x1 = cx + sx * 132
        s += f'<path d="M{x0} {ky} V100 Q{(x0 + x1) / 2} 84 {x1} 128 V{ky} Z" fill="#6E4422" stroke="#3A2614" stroke-width="4"/>'
        for k in range(4):
            yy = 140 + k * 40
            s += f'<path d="M{x0} {yy} H{x1}" stroke="#3A2614" stroke-width="5"/>'
            for j in range(3):
                s += f'<circle cx="{x0 + sx * (24 + j * 34)}" cy="{yy}" r="4" fill="#C9A86A"/>'
    # meşaleler
    for x in (cx - 230, cx + 230):
        s += f'<rect x="{x - 6}" y="130" width="12" height="60" fill="#5A3A22"/>'
        alev = s.rad([(0, "#FFF4C8"), (.5, "#FFB43A"), (1, "#E2533D", .0)], x, 112, 60, kull="userSpaceOnUse", ad="al")
        s += f'<circle cx="{x}" cy="112" r="60" fill="{alev}"/><path d="M{x - 12} 130 Q{x - 14} 104 {x} 86 Q{x + 14} 104 {x + 12} 130 Z" fill="#FF8A3D"/><path d="M{x - 6} 130 Q{x - 6} 112 {x} 100 Q{x + 6} 112 {x + 6} 130 Z" fill="#FFE08A"/>'
    # sancaklar (sekiz köşeli yıldızlı)
    from .temel import selcuklu_yildizi
    for k, (x, c) in enumerate(((760, "#B23A2E"), (2000, "#13A3A6"))):
        s += f'<path d="M{x - 60} 70 H{x + 60} V230 L{x} 270 L{x - 60} 230 Z" fill="{c}" stroke="#3A2614" stroke-width="3"/>'
        s += f'<path d="M{x - 60} 82 H{x + 60}" stroke="{ALTIN}" stroke-width="6"/>'
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x, 160, 40), True)}" fill="{ALTIN}" stroke="#3A2614" stroke-width="2"/>'
        s += f'<circle cx="{x}" cy="160" r="14" fill="{c}"/>'
    # basamaklar
    for k in range(4):
        s += f'<rect x="{cx - 220 - k * 30}" y="{h - 14 - k * 14}" width="{440 + k * 60}" height="16" fill="#C9AE84" stroke="#8C6E4A" stroke-width="2" transform="translate(0 {k * 14 - 0})"/>'
    s += '<use href="#pamuk-akce" x="1680" y="128" width="150" height="171"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ CEVAPLAR · GECE (28 mm)

def gece(h=360):
    s = Svg("sh-gec")
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 30, 140, 250)
    s += S.ay(s, 1330, 84, 34, golge_renk="#13204A")
    vk, _ = Y.van_kalesi(s, 1450, 2080, ufuk + 6, 150, 251, tas="#3A3F66", golge="#262A48", sur="#454B78", ayrinti=.6, bayrak=False)
    s += vk
    d, _ = S.dag(s, -60, 900, ufuk, 320, 110, 252, renk="#283565", golge="#1C2650", bicim="volkan", kar_y=140, kar="#C8D2F0", kar_golge="#8F9CC8", isik=1, sirt=2, puruz=5)
    s += d
    s += S.gol(s, 0, ufuk, W, h - ufuk, 253, ufuk="#3A5A9A", orta="#1D3366", derin="#0B1636", gunes_x=1300, parilti_renk="#FFF0C0", cizgi_renk="#9FB4E8")
    s += S.yansima(s, d + vk, ufuk, 0, W, 80, op=.3)
    r = RNG(254)
    for k in range(40):
        x = 900 + r.uniform(0, 1150)
        s += f'<circle cx="{f(x)}" cy="{f(ufuk + r.uniform(-4, 6))}" r="{f(r.uniform(1.4, 3))}" fill="#FFD27A" opacity="{f(r.uniform(.6, 1), 2)}"/>'
    for (x, y) in ((1560, ufuk - 86), (1700, ufuk - 100), (1880, ufuk - 94)):
        s += f'<rect x="{x}" y="{y}" width="8" height="10" fill="#FFD27A"/>'
    s += S.tekne(s, 600, ufuk + 50, 70, govde="#1D3A8A", ust="#C9D6EA")
    s += f'<circle cx="610" cy="{ufuk + 22}" r="16" fill="#FFD27A" opacity=".35"/><circle cx="610" cy="{ufuk + 22}" r="5" fill="#FFE9A8"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ FİNAL · KALE BURCUNDA PAMUK (90 mm)

def final(h=900, nisanlar=None):
    s = Svg("sh-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    # güneş ışınları
    gx, gy = 760, ufuk - 30
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE0A0" opacity=".12"/>'
    s += S.gunes(s, gx, gy, 70, hale="#FFC56B", hale_r=700, guc=.95)
    for i, (x, y, w, k) in enumerate([(200, 260, 520, 22), (1200, 180, 640, 26), (1500, 330, 480, 16), (100, 420, 380, 12)]):
        s += S.bulut_serit(s, x, y, w, k, "#FFC59A", "#FF6F8A", .75)
    uzak = ""
    d, _ = S.dag(s, 980, 1900, ufuk, 1400, 300, 261, renk="#D08AA6", golge="#7E5A92", bicim="volkan", kar_y=380,
                 kar="#FFE3EC", kar_golge="#C7A6CF", sis="#FF9A8A", isik=-1, sirt=4, kenar_isik="#FFD3B8")
    uzak += d
    d, _ = S.dag(s, -100, 760, ufuk, 300, 430, 262, renk="#6B4C86", golge="#4E3A6E", bicim="kaldera", sis="#E07A8A", isik=-1, sirt=2, puruz=6)
    uzak += d
    d, _ = S.dag(s, 1750, 2300, ufuk, 2050, 420, 263, renk="#9A6FA6", golge="#6E5288", bicim="tepe", sis="#F49A8A", isik=-1, sirt=2, puruz=6)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, h - ufuk, 264, ufuk="#FFB59A", orta="#C86A9A", derin="#2D3A7A", gunes_x=gx, parilti_renk="#FFE3A0")
    s += S.yansima(s, uzak, ufuk, 0, W, 200, op=.3)
    s += S.tekne(s, 420, ufuk + 80, 80, govde="#2B50B5", yelken="#FFF1DE")
    for k, (x, y, o) in enumerate([(560, 200, 1.4), (640, 240, 1.0), (1100, 120, .8), (1180, 150, .6), (300, 160, .7)]):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    # kale burcu (ön plan): mazgallı sur + sağda kule
    g = s.lin([(0, "#E8C998"), (1, "#A9845A")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    s += f'<rect x="0" y="720" width="{W}" height="{h - 720}" fill="{g}"/>'
    r = RNG(265)
    for row in range(6):
        y = 724 + row * 30
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            s += f'<rect x="{x + 2}" y="{y}" width="86" height="27" rx="3" fill="{karis("#E8C998", "#B08B60", r.uniform(0, .6))}" stroke="#8C6E4A" stroke-width="1.6"/>'
    for x in range(0, W, 150):
        s += f'<rect x="{x}" y="660" width="96" height="64" fill="#E2C292" stroke="#8C6E4A" stroke-width="2.6"/>'
        s += f'<rect x="{x}" y="660" width="96" height="10" fill="#F2DCB4"/>'
    # kule (sağ)
    s += f'<rect x="1560" y="560" width="420" height="{h - 560}" fill="url(#{s.onek}-tk)" stroke="#8C6E4A" stroke-width="3"/>'
    s.tanim(f'<linearGradient id="{s.onek}-tk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F2D7A8"/><stop offset=".6" stop-color="#D9B482"/><stop offset="1" stop-color="#A9845A"/></linearGradient>')
    for x in range(1560, 1980, 84):
        s += f'<rect x="{x}" y="510" width="54" height="56" fill="#E8C998" stroke="#8C6E4A" stroke-width="2.6"/>'
    s += f'<path d="M1740 {h} V760 Q1740 720 1770 712 Q1800 720 1800 760 V{h} Z" fill="#5A3A22"/>'
    # Pamuk burçta, bayrakla
    s += '<use href="#pamuk-bayrak" x="1600" y="150" width="340" height="400"/>'
    # nişan çelengi (iki direk arasında ip)
    s += f'<path d="M260 650 V330" stroke="#6B4A2E" stroke-width="10"/><circle cx="260" cy="324" r="10" fill="{ALTIN}"/>'
    s += f'<path d="M260 360 Q900 520 1640 330" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .6) / (len(nisanlar) + .2)
            x = (1 - t) ** 2 * 260 + 2 * (1 - t) * t * 900 + t * t * 1640
            y = (1 - t) ** 2 * 360 + 2 * (1 - t) * t * 520 + t * t * 330
            s += f'<path d="M{f(x)} {f(y)} v18" stroke="#5A3A22" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 62)} {f(y + 14)}) rotate({f((k % 2 * 2 - 1) * 5)} 62 70)">{ns}</g>'
    # konfeti / akçe parıltıları
    for k in range(60):
        x = r.uniform(300, 1900)
        y = r.uniform(80, 640)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ AÇILIŞ · VAN GÖLÜ PANORAMASI + TUR ROTASI

# yaklaşık coğrafi noktalar (enlem, boylam) — stilize harita için
GOL_KIYI = [(38.505, 42.28), (38.60, 42.33), (38.70, 42.42), (38.75, 42.49), (38.79, 42.60), (38.80, 42.73),
            (38.84, 42.90), (38.90, 43.05), (38.97, 43.22), (39.03, 43.34), (39.00, 43.43), (38.90, 43.40),
            (38.80, 43.36), (38.70, 43.40), (38.60, 43.36), (38.52, 43.33), (38.44, 43.27), (38.37, 43.19),
            (38.30, 43.10), (38.31, 42.98), (38.36, 42.80), (38.42, 42.60), (38.47, 42.42)]

DURAKLAR = [  # (anahtar, enlem, boylam, etiket-üst, etiket-ad, alt, tür, etiket yönü)
    ("1", 38.425, 43.30, "1. DURAK · EDREMİT", "Neden mol?", "s.2 · +100 akçe", "durak", "sag"),
    ("2", 38.265, 43.11, "2. DURAK · GEVAŞ", "Atomun kütlesi", "s.3 · +150 akçe", "durak", "alt"),
    ("3", 38.49, 42.21, "3. DURAK · TATVAN", "Mol ile tanecik", "s.4 · +150 akçe", "durak", "sol"),
    ("4", 38.78, 42.43, "4. DURAK · AHLAT", "Mol ile kütle", "s.5 · +150 akçe", "durak", "sol"),
    ("5", 38.845, 42.70, "5. DURAK · ADİLCEVAZ", "Karışımlar", "s.6 · +150 akçe", "durak", "ust"),
    ("H", 38.90, 42.88, "SÜPHAN ETEĞİ", "Hülasa", "s.7 · +40 akçe", "hulasa", "ust"),
    ("M", 39.06, 43.30, "ERCİŞ", "Meclis: Kim haklı?", "s.8 · +120 akçe", "yan", "ust"),
    ("K", 39.00, 43.62, "MURADİYE", "Kıssa", "s.9 · +120 akçe", "yan", "sag"),
    ("A", 38.62, 43.43, "VAN İSKELESİ", "Anahtar merdiveni", "s.10 · +120 akçe", "yan", "sag"),
    ("V", 38.50, 43.40, "VAN KALESİ", "Büyük İmtihan", "s.11–12 · +300 akçe", "kale", "sag"),
]
ROTA_ARA = {  # duraklar arası kıyı boyunca ara noktalar (rota yumuşak kıvrılsın)
    ("1", "2"): [(38.36, 43.22)],
    ("2", "3"): [(38.29, 42.95), (38.35, 42.75), (38.41, 42.52), (38.46, 42.33)],
    ("3", "4"): [(38.60, 42.27), (38.70, 42.36)],
    ("4", "5"): [(38.82, 42.56)],
    ("5", "H"): [],
    ("H", "M"): [(38.93, 43.02), (39.00, 43.18)],
    ("M", "K"): [(39.07, 43.45)],
    ("K", "A"): [(38.86, 43.52), (38.73, 43.47)],
    ("A", "V"): [],
}


def _proje(enl, boy, W_=W, ufuk=372, alt=1150):
    u = (boy - 42.12) / (43.80 - 42.12)
    v = (enl - 38.20) / (39.12 - 38.20)
    k = 1.8
    z = 1 + v * k
    Wm = 2750
    X = W_ / 2 + (u - .5) * Wm / z + 10
    t = (1 / z - 1 / (1 + k)) / (1 - 1 / (1 + k))
    Y = (ufuk + 26) + (alt - ufuk - 26) * t
    return X, Y, 1 / z


def panorama(h=1100):
    s = Svg("sh-pan")
    ufuk = 372
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gunbatimi")
    gx, gy = 300, ufuk - 46
    for k in range(12):
        a0 = math.pi + .1 + k * (math.pi - .2) / 12
        a1 = a0 + .05
        s += f'<path d="M{gx} {gy} L{f(gx + 2400 * math.cos(a0))} {f(gy + 2400 * math.sin(a0))} L{f(gx + 2400 * math.cos(a1))} {f(gy + 2400 * math.sin(a1))} Z" fill="#FFE4B0" opacity=".09"/>'
    s += S.gunes(s, gx, gy, 52, hale="#FFC56B", hale_r=640, guc=.95)
    for (x, y, w_, k) in ((620, 150, 520, 18), (1260, 96, 640, 22), (1700, 210, 420, 14), (120, 230, 360, 12), (900, 260, 380, 10)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC9A0", "#FF6F8A", .78)
    # uzak dağlar: Nemrut (sol, güneşin önünde), Süphan (orta-sol, karlı), Erek (sağ)
    P = _proje
    nx, ny, nz = P(38.65, 42.23)
    sx_, sy_, sz = P(38.93, 42.83)
    ex, ey, ez = P(38.47, 43.62)
    uzak = ""
    d, _ = S.dag(s, sx_ - 520, sx_ + 560, ufuk + 8, sx_, 92, 301, renk="#D394B0", golge="#7F5C96", bicim="volkan", kar_y=196,
                 kar="#FFE6EE", kar_golge="#C6A7D2", sis="#FFA18E", isik=-1, sirt=6, puruz=9, kenar_isik="#FFD7C2")
    uzak += d
    d, _ = S.dag(s, 1480, 2240, ufuk + 8, 1900, 210, 302, renk="#A2789F", golge="#74578C", bicim="sivri", kar_y=246,
                 kar="#FFE0E6", kar_golge="#C3A3CC", sis="#FFA18E", isik=-1, sirt=4)
    uzak += d
    s += uzak
    # kara (bütün zemin): sıcak yeşil-toprak, uzakta sisli
    gk = s.lin([(0, "#B98A8E"), (.12, "#C79A72"), (.45, "#9DAA5E"), (1, "#5E8E40")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kara")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    # Nemrut (sol orta plan, büyük kaldera)
    d, _ = S.dag(s, -200, 700, ny + 40, 240, ny - 150, 303, renk="#6E4E7E", golge="#4A3560", bicim="kaldera", sis="#C98A8E", isik=1, sirt=4, puruz=8, kenar_isik="#FFB27A")
    s += d
    s += f'<path d="M150 {f(ny - 152)} Q240 {f(ny - 166)} 330 {f(ny - 150)} Q240 {f(ny - 140)} 150 {f(ny - 152)} Z" fill="#6FC6C4" opacity=".8"/>'
    # tarlalar (yamalar)
    r = RNG(304)
    for k in range(70):
        enl = r.uniform(38.2, 39.12)
        boy = r.uniform(42.1, 43.85)
        x, y, sc = P(enl, boy)
        w_ = r.uniform(60, 160) * sc
        hh = w_ * .35 * (.4 + sc)
        c = r.choice(["#B9B65E", "#8FB24E", "#D3B86A", "#7AA84A", "#C9A04E", "#A8C46A"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w_)} {f(-hh * .2)} l{f(-w_ * .2)} {f(hh)} l{f(-w_)} {f(hh * .2)} Z" fill="{c}" opacity=".55"/>'
    # göl
    kiyi = []
    rk = RNG(305)
    for i, (a, b) in enumerate(GOL_KIYI):
        a2, b2 = GOL_KIYI[(i + 1) % len(GOL_KIYI)]
        for t in (0, .5):
            aa, bb = a + (a2 - a) * t, b + (b2 - b) * t
            if t:
                aa += rk.uniform(-.012, .012)
                bb += rk.uniform(-.015, .015)
            kiyi.append(P(aa, bb)[:2])
    gg = s.lin([(0, "#FFB59A"), (.18, "#E58FA0"), (.42, "#4DB6B8"), (1, "#0D6E7C")], 0, ufuk + 20, 0, 1000, kull="userSpaceOnUse", ad="gol")
    gol_d = egri_d(kiyi, True, .9)
    s += f'<path d="{gol_d}" fill="#F3E0B8" transform="translate(0 6) scale(1 1.004)"/>'
    s += f'<path d="{gol_d}" fill="{gg}"/>'
    kl = s.klip(f'<path d="{gol_d}"/>', ad="gk")
    ic = []
    ic.append(S.yansima(s, uzak, ufuk + 26, 0, W, 300, op=.22))
    for k in range(70):
        y = ufuk + 30 + (r.random() ** 1.5) * 600
        x = r.uniform(300, 1800)
        uz = (14 + (y - ufuk) * .18) * r.uniform(.5, 1.4)
        ic.append(f'<path d="M{f(x)} {f(y)} h{f(uz)}" stroke="#FFFFFF" stroke-width="{f(1 + (y - ufuk) / 220)}" stroke-linecap="round" opacity="{f(r.uniform(.25, .6), 2)}"/>')
    for k in range(60):
        t = k / 60
        y = ufuk + 34 + t * 560
        gen = (10 + 160 * t) * r.uniform(.4, 1)
        x = 520 + 420 * t + r.uniform(-1, 1) * (8 + 60 * t) - gen / 2
        ic.append(f'<path d="M{f(x)} {f(y)} h{f(gen)}" stroke="#FFE6A8" stroke-width="{f(1.4 + 3 * t)}" stroke-linecap="round" opacity="{f(r.uniform(.5, .95) * (1 - .4 * t), 2)}"/>')
    s += f'<g clip-path="{kl}">{"".join(ic)}</g>'
    s += f'<path d="{gol_d}" fill="none" stroke="#FFF3D6" stroke-width="5" opacity=".85"/>'
    # Akdamar adası
    ax, ay, asc = P(38.34, 43.03)
    s += f'<ellipse cx="{f(ax)}" cy="{f(ay)}" rx="{f(46 * asc * 2)}" ry="{f(14 * asc * 2)}" fill="#6E8F5C"/>'
    s += f'<ellipse cx="{f(ax - 6)}" cy="{f(ay - 6)}" rx="{f(30 * asc * 2)}" ry="{f(10 * asc * 2)}" fill="#8BAA68"/>'
    # simge yapılar (perspektif ölçekli)
    def yer(enl, boy):
        return P(enl, boy)
    x, y, sc = yer(38.80, 42.73)
    s += Y.kucuk_kale(s, x + 30, y + 8, 120 * sc * 2, 90 * sc * 2, 310, tas="#D9B48C")
    x, y, sc = yer(38.76, 42.47)
    for k in range(6):
        s += Y.mezar_tasi(s, x - 40 + k * 14, y + 4 + (k % 2) * 4, 9, 30, 320 + k, sade=True, likan=False)
    x, y, sc = yer(38.28, 43.13)
    s += Y.kumbet(s, x + 60, y + 30, 110, 330, tas="#E2B48C", cati="#C08A62")
    x, y, sc = yer(38.495, 43.36)
    vk, _ = Y.van_kalesi(s, x + 20, x + 330, y + 46, 120, 331, tas="#E0C49A", golge="#A07E5C", sur="#ECD5AA", ayrinti=.6, bayrak=True)
    s += vk
    x, y, sc = yer(38.60, 43.40)
    s += Y.iskele(s, x - 150, x - 30, y + 10, 8, 332, merdiven=False, direk_n=4)
    s += Y.fener(s, x - 160, y + 4, 54)
    x, y, sc = yer(39.0, 43.62)
    s += Y.selale(s, x + 40, y - 40, y + 10, 70, 333)
    x, y, sc = yer(38.89, 42.88)
    s += Y.cadir(s, x + 70, y - 4, 50, 38, renk="#9E2F28")
    for k in range(6):
        s += Y.koyun(x + 120 + k * 16, y + (k % 2) * 5, .7)
    # kıyı kavakları ve köyler
    for k in range(70):
        i = r.randrange(len(GOL_KIYI))
        a, b = GOL_KIYI[i]
        a2, b2 = GOL_KIYI[(i + 1) % len(GOL_KIYI)]
        t = r.random()
        enl, boy = a + (a2 - a) * t, b + (b2 - b) * t
        cx_, cy_ = 38.66, 42.86
        enl += (enl - cx_) * .06
        boy += (boy - cy_) * .04
        x, y, sc = P(enl, boy)
        if r.random() < .7:
            s += S.kavak(s, x, y, 70 * sc * 1.8, 13 * sc * 1.8, 400 + k, renk="#5E9A4A", isik=-1)
        else:
            s += S.ev(x, y, 22 * sc * 2, 16 * sc * 2, 500 + k, duvar="#F3E2C6", cati="#C2563A", isik=-1)
    # yakın plan arazi: ekran üzerinde boş kara alanlarına bahçe, kavak sırası, köy (göl ve etiket alanı dışı)
    def gol_icinde(px, py):
        ic_ = False
        n_ = len(kiyi)
        for i_ in range(n_):
            x1_, y1_ = kiyi[i_]
            x2_, y2_ = kiyi[(i_ + 1) % n_]
            if (y1_ > py) != (y2_ > py) and px < (x2_ - x1_) * (py - y1_) / (y2_ - y1_ + 1e-9) + x1_:
                ic_ = not ic_
        return ic_
    yasak = [(0, 560, 520, 900), (1530, 560, 2100, 1100), (1180, 900, 1560, 1100), (1820, 860, 2100, 1100)]
    rb = RNG(306)
    k = 0
    for _ in range(400):
        x = rb.uniform(20, 2080)
        y = rb.uniform(560, 1080)
        if gol_icinde(x, y) or gol_icinde(x, y - 60) or any(a_ <= x <= c_ and b_ <= y <= d_ for a_, b_, c_, d_ in yasak):
            continue
        sc = .35 + (y - 400) / 700 * .9
        tur = rb.random()
        if tur < .45:
            for j in range(3):
                s += S.agac(s, x + j * 30 * sc, y + (j % 2) * 6, 14 * sc, 600 + k * 3 + j, renk=rb.choice(["#6FAA4E", "#5E9A43", "#7DB955"]), meyve="#E2533D" if j == 1 and tur < .2 else None)
        elif tur < .8:
            for j in range(4):
                s += S.kavak(s, x + j * 16 * sc, y, 66 * sc, 12 * sc, 700 + k * 4 + j, renk="#5E9A4A")
        else:
            for j in range(3):
                s += S.ev(x + j * 28 * sc, y + (j % 2) * 5, 24 * sc, 17 * sc, 800 + k * 5 + j, duvar="#F3E2C6", cati="#C2563A", isik=-1)
        k += 1
        if k > 34:
            break
    # Tatvan feribotu ve tekneler
    x, y, sc = P(38.55, 42.55)
    s += S.feribot(s, x, y, 260 * sc * 1.4)
    x, y, sc = P(38.62, 43.05)
    s += S.tekne(s, x, y, 70 * sc * 1.5, govde="#C8442F", yelken="#FFF1DE")
    x, y, sc = P(38.75, 42.95)
    s += S.tekne(s, x, y, 50 * sc * 1.5, govde="#2B50B5", yelken="#FFF1DE")
    # rota: duraklar + ara noktalar
    sira = [d_[0] for d_ in DURAKLAR]
    yol_pts = []
    konum = {d_[0]: P(d_[1], d_[2])[:2] for d_ in DURAKLAR}
    for i, k in enumerate(sira):
        yol_pts.append(konum[k])
        if i + 1 < len(sira):
            for a, b in ROTA_ARA.get((k, sira[i + 1]), []):
                yol_pts.append(P(a, b)[:2])
    yd = egri_d(yol_pts, False, .9)
    s += f'<path d="{yd}" fill="none" stroke="#1B1D26" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
    s += f'<path d="{yd}" fill="none" stroke="#FFF1CF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="3.2" stroke-dasharray="12 9" stroke-linecap="round"/>'
    # durak rozetleri
    from .temel import selcuklu_yildizi as _y8, yildiz_noktalari as _yn
    for (k, a, b, *_r) in DURAKLAR:
        x, y = konum[k]
        tur = _r[3]
        if tur == "durak":
            s += f'<path d="{cizgi_d(_y8(x, y, 36), True)}" fill="#F0C14A" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<path d="{cizgi_d(_y8(x, y, 29), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 11)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="32" fill="#FFFFFF">{k}</text>'
        elif tur == "kale":
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="34" fill="#E2533D" stroke="#1B1D26" stroke-width="3"/>'
            s += f'<path d="M{f(x - 18)} {f(y + 14)} V{f(y - 6)} h6 v-6 h6 v6 h4 v-6 h6 v6 h4 v-6 h6 v6 h4 V{f(y + 14)} Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
        else:
            renk = "#F0A21A" if tur == "yan" else "#7B3F8C"
            s += f'<path d="M{f(x)} {f(y - 32)} L{f(x + 32)} {f(y)} L{f(x)} {f(y + 32)} L{f(x - 32)} {f(y)} Z" fill="{renk}" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 10)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="27" fill="#FFFFFF">{k}</text>'
    # başlangıç bayrağı
    x, y = konum["1"]
    s += f'<path d="M{f(x + 36)} {f(y + 40)} v-64" stroke="#1B1D26" stroke-width="4"/><path d="M{f(x + 38)} {f(y - 22)} h44 l-10 13 l10 13 h-44 Z" fill="#E2533D" stroke="#1B1D26" stroke-width="2.4"/>'
    # Van Gölü yazısı
    x, y, _ = P(38.62, 42.86)
    s += (f'<text x="{f(x)}" y="{f(y + 70)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="76" fill="#FFFFFF" stroke="#0A5A66" stroke-width="2" paint-order="stroke" opacity=".96">Van Gölü</text>'
          f'<text x="{f(x)}" y="{f(y + 108)}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="25" letter-spacing="1.5" fill="#FFFFFF" opacity=".95">SODALI GÖL · pH ≈ 9,5–10</text>')
    # gölde inci kefalleri + yüzen Pamuk
    for k, (a, b, aci) in enumerate(((38.43, 42.98, -20), (38.40, 43.06, -32), (38.47, 42.62, -14))):
        x, y, sc = P(a, b)
        s += S.kefal(s, x, y, 70 * sc * 1.6, aci)
        s += S.damla_sicrama(x - 24 * sc, y + 14 * sc, sc * 1.3)
    x, y, sc = P(38.40, 42.80)
    s += f'<use href="#pamuk-yuzer" x="{f(x - 70)}" y="{f(y - 50)}" width="140" height="93"/>'
    # martılar
    for k, (x, y, o) in enumerate(((1000, 200, 1.2), (1070, 236, .9), (1500, 150, .8), (1550, 176, .6), (820, 300, .7))):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    s += S.marti(1480, 1010, 1.5, 6, ayrintili=True)
    # pusula gülü (çini yıldız)
    from .temel import selcuklu_yildizi, yildiz_noktalari
    px, py = 1960, 960
    s += f'<circle cx="{px}" cy="{py}" r="74" fill="#FFFFFF" opacity=".9" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 66, 14, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 34), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="10" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 76}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), konum
