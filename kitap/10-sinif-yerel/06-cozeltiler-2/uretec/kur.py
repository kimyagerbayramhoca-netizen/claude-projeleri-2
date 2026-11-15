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
# duraklar meta.json'dan; yan yollar ve kale burada. Yerleşim: her etiket için tercih sırasıyla 8 aday yer denenir;
# harita dışına, başlık/pusula üstüne, başka etikete ya da rozete binmeyen ilk yer seçilir (kur_ortak'taki açgözlü yöntem).
YAN = {"H": ("KOVADA GÖLÜ", "Hülasa", "7", 40, "hul"), "M": ("EĞİRDİR", "Meclis", "8", 120, "yan"),
       "K": ("YEŞİLADA", "Kıssa", "9", 120, "yan"), "A": ("EĞİRDİR İSKELESİ", "Anahtar", "10", 120, "yan"),
       "V": ("EĞİRDİR KALESİ", "Büyük İmtihan", "11–12", 300, "kale")}
TERCIH = {"1": "sol üst-sol alt-sol", "2": "üst üst-sağ üst-sol", "3": "üst üst-sol sol", "4": "üst-sağ sağ üst", "5": "alt alt-sol alt-sağ",
          "H": "sağ alt-sağ alt", "M": "sağ üst-sağ alt-sağ", "K": "üst üst-sağ sağ", "A": "sol alt-sol üst-sol", "V": "alt alt-sağ alt-sol"}


def panorama_etiket():
    """Göller Yolu panoramasındaki etiketler. Konum: sahnenin izdüşümü (SU.panorama_goller); sayfa no kitapta kayar."""
    _, konum = SU.panorama_goller()
    rozet = {k: (x / 10, y / 10) for k, (x, y) in konum.items()}
    yasak = [(0, 0, 84, 18), (181, 81, 210, 110)]          # "Tur haritası" başlığı, pusula
    yerlesik, out = [], []

    def carpisir(p, q):
        return not (p[2] <= q[0] or q[2] <= p[0] or p[3] <= q[1] or q[3] <= p[1])

    for k in SU.SIRA:
        if k.isdigit():
            d = u.meta["duraklar"][int(k) - 1]
            ust, ad, sayfa, akce, cls = f"{k}. DURAK · {KO.tr_buyuk(d['yer'])}", d["baslik"], str(d["sayfa"]), d["akce"], ""
        else:
            ust, ad, sayfa, akce, cls = YAN[k]
        s_ = "–".join(str(u.sayfa_no(int(p))) for p in sayfa.split("–"))
        ust = f"{ust} · s.{s_}"
        x, y = rozet[k]
        w = max(len(ust) * 1.53, len(KO.duz_metin(ad)) * 1.62 + len(f"+{akce} akçe") * 1.4 + 1) + 4.2
        h = 8.4
        aday = {"sağ": (x + 4.4, y - h / 2), "sol": (x - 4.4 - w, y - h / 2), "üst": (x - w / 2, y - 4.4 - h), "alt": (x - w / 2, y + 4.4),
                "üst-sağ": (x + 3, y - 3.4 - h), "alt-sağ": (x + 3, y + 3.4), "üst-sol": (x - w - 3, y - 3.4 - h), "alt-sol": (x - w - 3, y + 3.4)}
        sira = TERCIH[k].split() + [a for a in aday if a not in TERCIH[k].split()]
        secim = aday[sira[0]]
        for ad_ in sira:
            lx, ly = aday[ad_]
            kutu = (lx, ly, lx + w, ly + h)
            if kutu[0] < 1.5 or kutu[1] < 1.5 or kutu[2] > 208.5 or kutu[3] > 108.5:
                continue
            if any(carpisir(kutu, q) for q in yasak + yerlesik):
                continue
            if any(kk != k and kutu[0] - 3.6 < rx < kutu[2] + 3.6 and kutu[1] - 3.6 < ry < kutu[3] + 3.6 for kk, (rx, ry) in rozet.items()):
                continue
            secim = (lx, ly)
            break
        yerlesik.append((secim[0], secim[1], secim[0] + w, secim[1] + h))
        sinif = f"durak-et {cls}".strip()
        out.append(f'<div class="{sinif}" style="left:{f(secim[0], 2)}mm;top:{f(secim[1], 2)}mm">'
                   f'<i>{ust}</i><b>{KO.zengin(ad)}<small>+{akce} akçe</small></b></div>')
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
