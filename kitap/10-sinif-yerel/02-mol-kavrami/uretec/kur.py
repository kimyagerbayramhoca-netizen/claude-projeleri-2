#!/usr/bin/env python3
"""Mol Kavramı · Van Gölü Turu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
    python3 uretec/kur.py --ebru     # ebru dokularını da yeniden üretir
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Bu dosyada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi), HUD ilerleme noktası,
açılış panoramasının durak etiketleri. Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır.
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
from cizim import sahneler as SH  # noqa: E402
from cizim.temel import f  # noqa: E402

# ------------------------------------------------------------------ sayfa künyesi (HUD + altbilgi)
# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / 1400
SAYFA = {
    1: ("Yola çıkış", "Van Gölü turu · yola çıkış", 0),
    2: ("1. durak · <b>Edremit</b>", "1. durak · Neden mol?", 0),
    3: ("2. durak · <b>Gevaş</b>", "2. durak · Atomun kütlesi", 7),
    4: ("3. durak · <b>Tatvan</b>", "3. durak · Mol ile tanecik sayısı", 18),
    5: ("4. durak · <b>Ahlat</b>", "4. durak · Mol ile kütle", 29),
    6: ("5. durak · <b>Adilcevaz</b>", "5. durak · Karışımlar", 39),
    7: ("Hülasa · <b>Süphan eteği</b>", "Hülasa · Mol özeti", 50),
    8: ("Yan yol · <b>Erciş</b>", "Yan yol 1 · Meclis: kim haklı?", 53),
    9: ("Yan yol · <b>Muradiye</b>", "Yan yol 2 · Kıssalar", 61),
    10: ("Yan yol · <b>Van iskelesi</b>", "Yan yol 3 · Anahtar merdiveni", 70),
    11: ("<b>Van Kalesi</b> · 1/2", "Büyük İmtihan · 1. bölüm", 79),
    12: ("<b>Van Kalesi</b> · 2/2", "Büyük İmtihan · 2. bölüm", 89),
    13: ("<b>Cevaplar</b>", "Cevaplar ve çözümler", 100),
    14: ("<b>Final</b>", "Final · akçe rayı ve unvan", 100),
}
# ilerleme noktaları: 5 durak + hülasa + 3 yan yol + kale ; her sayfada hangisi "şimdi" (−1: yok, 10: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 9, 13: 10, 14: 10}

u = KO.Unite(__file__, SAYFA, SIMDI)


# ------------------------------------------------------------------ üniteye özel: Van Gölü panoramasının durak etiketleri
def panorama_etiket():
    """Açılış panoramasındaki durak etiketleri (HTML; konumlar sahnenin projeksiyonundan, sayfa no kaymalı)."""
    _, konum = SH.panorama()
    # etiket yerleşimi: (sol mm, üst mm) ofsetleri, rozet merkezine göre
    yer = {"1": (2.4, 4.4), "2": (-44, -3.4), "3": (-10, 4.4), "4": (-33.5, -11), "5": (-12, 3.2),
           "H": (-23, -12.6), "M": (-19, -12.4), "K": (3.8, -9.6), "A": (4.2, -14.4), "V": (6.2, 2.2)}
    out = []
    for (k, a, b, ust, ad, alt_, tur, _y) in SH.DURAKLAR:
        x, y = konum[k]
        dx, dy = yer[k]
        cls = {"durak": "", "hulasa": "hul", "yan": "yan", "kale": "kale"}[tur]
        sayfa, akce = alt_.split(" · ")
        sayfa = re.sub(r"\d+", lambda m: str(u.sayfa_no(int(m.group()))), sayfa)
        out.append(f'<div class="durak-et {cls}" style="left:{f(x / 10 + dx, 2)}mm;top:{f(y / 10 + dy, 2)}mm"><i>{ust} · {sayfa}</i><b>{ad}<small>{akce}</small></b></div>')
    return "".join(out)


u.yer_tutucu("panorama-etiket", panorama_etiket)

if __name__ == "__main__":
    u.calistir()
