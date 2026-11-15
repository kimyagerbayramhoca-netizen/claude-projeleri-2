#!/usr/bin/env python3
"""Derişim Birimleri · Göller Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
Göller Yolu panoramasının durak etiketleri ({{panorama-etiket}}) ve final sahnesi ({{final}}: Eğirdir kıyısında
kutlama). Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır; sahneler uretec/sahneler_unite.py'dedir.
"""
import os
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
    1: ('Yola çıkış', 'Göller yolu · yola çıkış', 0),
    2: ('1. durak · <b>Eğirdir Gölü</b>', '1. durak · Derişim ve yüzde', 0),
    3: ('2. durak · <b>Isparta</b>', '2. durak · ppm: milyonda bir', 7),
    4: ('3. durak · <b>Burdur Gölü</b>', '3. durak · Molarite ve iyon derişimi', 18),
    5: ('4. durak · <b>Salda Gölü</b>', '4. durak · Seyreltme, deriştirme, karıştırma', 29),
    6: ('5. durak · <b>Davraz</b>', '5. durak · Koligatif özellikler', 39),
    7: ('Hülasa · <b>Kovada Gölü</b>', 'Hülasa · derişim özeti', 50),
    8: ('Yan yol · <b>Eğirdir</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    9: ('Yan yol · <b>Yeşilada</b>', 'Yan yol 2 · Kıssalar', 61),
    10: ('Yan yol · <b>Eğirdir iskelesi</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    11: ('<b>Eğirdir Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    12: ('<b>Eğirdir Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
    13: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    14: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    15: ('<b>Final</b>', 'Final · yolculuk tamamlandı', 100),
}
# HUD ilerleme noktaları: 5 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 10: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 9, 13: 10, 14: 10, 15: 10}

u = KO.Unite(__file__, SAYFA, SIMDI)
import sahneler_unite as SU  # noqa: E402  (KO.Unite uretec/'i sys.path'e ekledi)


# ------------------------------------------------------------------ açılış panoraması: durak etiketleri (HTML)
def panorama_etiket():
    """Göller Yolu panoramasındaki etiketler. Konumlar sahnenin izdüşümünden (SU.panorama_goller), yerleşim mm
    ofsetiyle (rozet merkezine göre); sayfa numaraları kitapta kayar (YEREL_SAYFA_BASLANGIC)."""
    _, konum = SU.panorama_goller()
    out = []
    for (k, _a, _b, ust, ad, sayfa, akce, tur, (dx, dy)) in SU.PAN_DURAKLAR:
        x, y = konum[k]
        cls = {"durak": "", "hulasa": "hul", "yan": "yan", "kale": "kale"}[tur]
        s_ = "–".join(str(u.sayfa_no(int(p))) for p in sayfa.split("–"))
        out.append(f'<div class="durak-et {cls}" style="left:{f(x / 10 + dx, 2)}mm;top:{f(y / 10 + dy, 2)}mm">'
                   f'<i>{ust} · s.{s_}</i><b>{ad}<small>+{akce} akçe</small></b></div>'.replace('class="durak-et "', 'class="durak-et"'))
    return "".join(out)


# ------------------------------------------------------------------ final: Eğirdir kıyısında kutlama + nişan çelengi
def final():
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
    return SU.final_goller(nisanlar=ns)


u.yer_tutucu("panorama-etiket", panorama_etiket)
u.yer_tutucu("final", final)

if __name__ == "__main__":
    u.calistir()
