"""Kimyasal Değişimler · üniteye özel sahneler, nişan ikonları ve bilgi grafikleri.

kur_ortak bu modüle {{sahne|ad|arg…}} ve {{info|ad|arg…}} için ORTAK kütüphaneden (yerel-ortak/cizim) ÖNCE bakar.
Ortak dosyaları değiştirme; yeni çizimleri burada ortak parçalardan kur (TASARIM-SISTEMI.md §6):
  • bant 2100×460 birim (1 birim = 0,1 mm), preserveAspectRatio="xMidYMid slice"
  • sol üst ≈ %55 × %75 gökyüzü/su olarak BOŞ (levha oturur); odak yapı sağ %40'ta; ufuk y ≈ 260–300
  • ışık yönü (isik) bütün çağrılarda aynı; tohum sabit → her kurulumda aynı resim
  • her Svg öneki benzersiz (aynı önek iki farklı çizimde kullanılırsa renkler bozulur)
  • konturlu (stroke) SVG yazısı yok: hale gerekiyorsa temel.halolu_yazi
"""
from cizim.temel import Svg, f, egri_d  # noqa: F401
from cizim import sahne as S, yapilar as Y  # noqa: F401
from cizim.sahneler import W, H, _bitir, _cerceve_golge

# Üniteye özel nişan ikonları: 48×48 çizgi SVG (dolgu yok; öğrenci boyar). meta.json nisanlar[].ikon bu adları kullanabilir.
NISAN_IKON = {
    # "cini": '<circle cx="24" cy="24" r="16"/><path d="M24 8 V40 M8 24 H40"/>',
}


def ornek_sahne(tema="gun", tohum="1"):
    """ÖRNEK durak bandı (ortak parçalardan): gökyüzü + güneş/ay + bulut + uzak dağlar + ova + kavaklar + sağda kümbet.
    Şablonda: {{sahne|ornek_sahne|safak|1}}. tema: safak gun altin gunbatimi alaca gece (sahne.GOK).
    Bunu kopyalayıp durağın gerçek yerini çiz (ör. kumbet yerine Y.van_kalesi, Y.kucuk_kale, Y.iskele, Y.selale …)."""
    t = int(tohum)
    s = Svg(f"un-{tema}-{t}")
    ufuk = 286
    gece = tema in ("gece", "alaca")
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, tema)
    if gece:
        s += S.yildizlar(s, 0, 0, W, ufuk, 90, t)
        s += S.ay(s, 1500, 90, 26)
    else:
        s += S.gunes(s, 1820, 96, 34, hale="#FFF2C2", hale_r=330, guc=.8)
        for i, (x, y, w) in enumerate([(820, 120, 230), (1180, 92, 280), (1560, 150, 200)]):
            s += S.bulut(s, x, y, w, t * 10 + i, ust="#FFFFFF", alt="#CFE3F1", op=.92)
    uzak = ""
    d, _ = S.dag(s, 980, 2240, ufuk, 1640, 84, t * 7 + 1, renk="#6F9AC2", golge="#4F79A8", bicim="sivri", kar_y=128,
                 kar="#FFFFFF", kar_golge="#C9DAEE", sis="#BFE0F0", isik=-1, sirt=4)
    uzak += d
    d, _ = S.dag(s, -80, 820, ufuk, 320, 196, t * 7 + 2, renk="#8FB4D2", golge="#7099C0", bicim="tepe", sis="#D6ECF5", isik=-1, sirt=2, puruz=5)
    uzak += d
    s += uzak
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 34, 26, t * 7 + 3, "#B7CF7A", "#7FAE52")
    s += tb
    ova = s.lin([(0, "#A9C76B"), (1, "#5F9442")], 0, ufuk + 40, 0, H, kull="userSpaceOnUse", ad="ova")
    s += f'<path d="M0 {ufuk + 52} C500 {ufuk + 40} 1200 {ufuk + 64} 2100 {ufuk + 48} V{H} H0 Z" fill="{ova}"/>'
    for i, (x, h_) in enumerate([(1290, 140), (1322, 165), (1354, 130), (2010, 180), (2046, 150), (2080, 170)]):
        s += S.kavak(s, x, 372, h_, 26, t * 50 + i, renk="#5A9C47")
    s += Y.kumbet(s, 1660, 380, 250, t, tas="#D7A47B", cati="#B9825E")
    for i, x in enumerate((1460, 1840, 1900)):
        s += S.agac(s, x, 372, 30, t * 60 + i, renk="#7DB955", meyve="#E2533D" if i == 1 else None)
    s += S.cimen(1100, 2100, 430, t, renk="#5C9A40", renk2="#86C25A", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += _cerceve_golge(s)
    return _bitir(s)
