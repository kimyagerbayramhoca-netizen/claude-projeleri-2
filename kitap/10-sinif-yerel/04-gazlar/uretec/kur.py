#!/usr/bin/env python3
"""Gazlar · Kapadokya Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
açılış panoramasının durak etiketleri, mühür alt yazısı ("KAPADOKYA YOLU") ve Kapadokya final sahnesi.
Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır; sahneler uretec/sahneler_unite.py,
bilgi grafikleri uretec/infografik_unite.py.
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
    1: ('Yola çıkış', 'Kapadokya yolu · yola çıkış', 0),
    2: ('1. durak · <b>Erciyes</b>', '1. durak · Gaz ve basınç', 0),
    3: ('2. durak · <b>Göreme</b>', '2. durak · Boyle ve Charles', 7),
    4: ('3. durak · <b>Avanos</b>', '3. durak · Gay-Lussac, Avogadro, birleşik', 18),
    5: ('4. durak · <b>Kızılçukur</b>', '4. durak · Kinetik teori ve ideal gaz', 29),
    6: ('5. durak · <b>Derinkuyu</b>', '5. durak · Yoğunluk ve yayılma', 39),
    7: ('Hülasa · <b>Hasan Dağı</b>', 'Hülasa · Gaz özeti', 50),
    8: ('Yan yol · <b>Güzelyurt</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    9: ('Yan yol · <b>Ihlara</b>', 'Yan yol 2 · Kıssalar', 61),
    10: ('Yan yol · <b>Güvercinlik</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    11: ('<b>Uçhisar Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    12: ('<b>Uçhisar Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
    13: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    14: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    15: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD ilerleme noktaları: 5 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 10: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 9, 13: 10, 14: 10, 15: 10}

u = KO.Unite(__file__, SAYFA, SIMDI)
import sahneler_unite as SU  # noqa: E402  (kur_ortak uretec/ klasörünü sys.path'e ekledi)


# ------------------------------------------------------------------ açılış: Kapadokya panoramasının durak etiketleri
# kur_ortak.yt_rota_etiket'teki açgözlü yerleşimin bu haritaya uyarlanmışı: her etiket için 8 aday yer denenir; harita
# dışına, başlığın, pusulanın, Pamuk'un ya da dağ/ırmak adlarının üstüne, başka bir etikete ya da rozete binmeyen ilk yer seçilir.
YASAK = [(0, 0, 100, 17),        # "Tur haritası" başlığı
         (182, 82, 210, 110),    # pusula
         (2, 87, 16, 101),       # Pamuk
         (30, 25, 51, 32), (164, 21, 192, 28), (24, 102, 43, 108)]   # Erciyes, Hasan Dağı, Kızılırmak yazıları


def panorama_etiket():
    _, konum = SU.kapadokya_panorama()
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

    # geri izlemeli arama: sıradaki etiket için ilk uygun adayı dene, olmazsa bir öncekini değiştir (etiketler arası ≥1 mm)
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
    return SU.kapadokya_panorama()[0]


# ------------------------------------------------------------------ mühür: alt yazı bu yolun adı
def muhur(tur, boy=""):
    return U.muhur(u.yeni("mh"), tur, alt="KAPADOKYA YOLU")


# ------------------------------------------------------------------ final: Kapadokya sahnesi + nişan çelengi (meta.json)
def final():
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="112" height="134" ', 1) for n in u.meta["nisanlar"]]
    return SU.final_kapadokya(nisanlar=ns)


u.yer_tutucu("panorama-etiket", panorama_etiket)
u.yer_tutucu("panorama-kapadokya", panorama)
u.yer_tutucu("muhur", muhur)
u.yer_tutucu("final", final)

if __name__ == "__main__":
    u.calistir()
