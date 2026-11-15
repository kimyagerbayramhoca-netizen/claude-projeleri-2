#!/usr/bin/env python3
"""Periyodik Tablo · Maden Yolu I · Batı Anadolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
açılış panoramasının çakışmasız durak etiketleri, mühür alt yazısı ("MADEN YOLU I"), Kütahya final sahnesi ve iki küçük
yerel düzeltme (üç haneli hazine rozeti, kesme yaprağının üst satırı). Hazine kartları, nişanlar ve duraklar
uretec/meta.json'dadır; sahneler uretec/sahneler_unite.py, bilgi grafikleri uretec/infografik_unite.py.
"""
import os
import re
import sys


def _ortak():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "kur_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak/kur_ortak.py bulunamadı")


sys.path.insert(0, _ortak())
import kur_ortak as KO  # noqa: E402
from cizim import sus as U  # noqa: E402
from cizim.temel import f  # noqa: E402

# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / 1400
SAYFA = {
    1: ('Yola çıkış', 'Maden Yolu I · yola çıkış', 0),
    2: ('1. durak · <b>Seydişehir</b>', '1. durak · Tablonun hikâyesi ve yapısı', 0),
    3: ('2. durak · <b>Kütahya</b>', '2. durak · Elektron diziliminden yer bulma', 7),
    4: ('3. durak · <b>Gümüşköy</b>', '3. durak · Kısa yollar ve özel durumlar', 18),
    5: ('4. durak · <b>Kırka</b>', '4. durak · Metal, ametal, yarı metal, soy gaz', 29),
    6: ('5. durak · <b>Bandırma</b>', '5. durak · Grup adları ve iyonlar', 39),
    7: ('Hülasa · <b>Kuşcenneti</b>', 'Hülasa · periyodik tablo özeti', 50),
    8: ('Yan yol · <b>Bigadiç</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    9: ('Yan yol · <b>Emet</b>', 'Yan yol 2 · Kıssalar', 61),
    10: ('Yan yol · <b>Germiyan Sokağı</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    11: ('<b>Kütahya Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    12: ('<b>Kütahya Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
    13: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    14: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    15: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD ilerleme noktaları: 5 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 10: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 9, 13: 10, 14: 10, 15: 10}

u = KO.Unite(__file__, SAYFA, SIMDI)
import sahneler_unite as SU  # noqa: E402  (kur_ortak uretec/ klasörünü sys.path'e ekledi)

# ------------------------------------------------------------------ açılış: panoramanın durak etiketleri
# Her etiket için aday yerler denenir; harita dışına, başlığın, pusulanın ya da harita yazılarının üstüne, başka bir
# etikete ya da rozete binmeyen bir yerleşim geri izlemeli aramayla seçilir (Gazlar ünitesindeki yöntemin uyarlaması).
YASAK = [(0, 0, 112, 16),          # "Tur haritası" başlığı ve alt satırı
         (193, 69, 207, 83),       # pusula
         (8, 36, 34, 42),          # MARMARA
         (60, 34, 80, 41),         # ULUDAĞ
         (137, 38, 163, 44),       # ESKİŞEHİR
         (180, 102, 208, 108)]     # TOROSLAR


def panorama_etiket():
    _, konum = SU.maden_panorama()
    rozet = {k: (x / 10, y / 10) for k, (x, y) in konum.items()}

    def carpisir(a, b, pay=0.0):
        return not (a[2] + pay <= b[0] or b[2] + pay <= a[0] or a[3] + pay <= b[1] or b[3] + pay <= a[1])

    ogeler = []
    for (k, _x, _y, ust, ad, alt_, tur) in SU.DURAKLAR:
        x, y = rozet[k]
        cls = {"durak": "", "hulasa": "hul", "yan": "yan", "kale": "kale"}[tur]
        sayfa, akce = alt_.split(" · ")
        sayfa = re.sub(r"\d+", lambda m: str(u.sayfa_no(int(m.group()))), sayfa)
        ust_tam = f"{ust} · {sayfa}"
        w = max(len(ust_tam) * 1.53, len(ad) * 1.62 + len(akce) * 1.4 + 1) + 4.2
        h = 8.4
        adaylar = [(x + 4.6, y - h / 2), (x - 4.6 - w, y - h / 2), (x - w / 2, y + 4.6), (x - w / 2, y - 4.6 - h),
                   (x + 3, y + 3.4), (x + 3, y - 3.4 - h), (x - w - 3, y + 3.4), (x - w - 3, y - 3.4 - h),
                   (x - w + 6, y + 4.6), (x - 6, y + 4.6), (x - w + 6, y - 4.6 - h), (x - 6, y - 4.6 - h)]
        uygun = []
        for lx, ly in adaylar:
            kutu = (lx, ly, lx + w, ly + h)
            if kutu[0] < 2 or kutu[1] < 2 or kutu[2] > 208 or kutu[3] > 108:
                continue
            if any(carpisir(kutu, y_) for y_ in YASAK):
                continue
            if any(kk != k and kutu[0] - 4 < rx < kutu[2] + 4 and kutu[1] - 4 < ry < kutu[3] + 4 for kk, (rx, ry) in rozet.items()):
                continue
            uygun.append(kutu)
        ogeler.append((k, cls, ust_tam, ad, akce, uygun))

    def ara(i, secilen):
        if i == len(ogeler):
            return secilen
        for kutu in ogeler[i][5]:
            if not any(carpisir(kutu, s_, 1.0) for s_ in secilen):
                r = ara(i + 1, secilen + [kutu])
                if r:
                    return r
        return None

    secim = ara(0, [])
    if not secim:
        raise SystemExit("panorama: etiketler için çakışmasız yerleşim bulunamadı")
    out = []
    for (k, cls, ust_tam, ad, akce, _), kutu in zip(ogeler, secim):
        out.append(f'<div class="durak-et {cls}" style="left:{f(kutu[0], 2)}mm;top:{f(kutu[1], 2)}mm"><i>{ust_tam}</i>'
                   f'<b>{ad}<small>{akce}</small></b></div>'.replace('class="durak-et "', 'class="durak-et"'))
    return "".join(out)


def panorama():
    return SU.maden_panorama()[0]


# ------------------------------------------------------------------ mühür: alt yazı bu yolun adı
def muhur(tur, boy=""):
    return U.muhur(u.yeni("mh"), tur, alt="MADEN YOLU I")


# ------------------------------------------------------------------ final: Kütahya Kalesi burcu + nişan çelengi (meta.json)
def final():
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
    return SU.final_kutahya(nisanlar=ns)


# ------------------------------------------------------------------ yerel düzeltmeler (ortak kütüphaneye öneri: README)
def _rozet_duzelt(html):
    """Ortak hazine rozetinde yazı boyu sabit (30): üç haneli kod (H10) dairenin dışına taşar. Burada küçültülür."""
    return re.sub(r'<text x="50" y="60" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">(H\d\d)</text>',
                  r'<text x="50" y="58" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="23" fill="#1B1D26">\1</text>', html)


_html_kur = u.html_kur
u.html_kur = lambda: _rozet_duzelt(_html_kur())
import hazine_yapragi as _HY  # noqa: E402  (hazine-kartlari.html de aynı rozeti kullanır)
_yaprak = _HY.yaprak_html
# kesme yaprağının üst satırına uzun rota adı sığmıyor: "Yol 4 · Maden Yolu I"
_HY.yaprak_html = lambda birim: (_rozet_duzelt(_yaprak(birim))
                                 .replace("<span>Yol 4 · Maden Yolu I · Batı Anadolu</span>", "<span>Yol 4 · Maden Yolu I</span>"))

u.yer_tutucu("panorama", panorama)
u.yer_tutucu("panorama-etiket", panorama_etiket)
u.yer_tutucu("muhur", muhur)
u.yer_tutucu("final", final)

if __name__ == "__main__":
    u.calistir()
