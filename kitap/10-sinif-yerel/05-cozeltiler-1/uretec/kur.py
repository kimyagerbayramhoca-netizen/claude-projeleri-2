#!/usr/bin/env python3
"""Çözünme ve Çözünürlük · Pamukkale–Afyon Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası
ve (gerekirse) üniteye özel yer tutucular. Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır;
sahneler uretec/sahneler_unite.py'dedir.
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

# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / 1400
SAYFA = {
    1: ('Yola çıkış', 'Pamukkale–Afyon yolu · yola çıkış', 0),
    2: ('1. durak · <b>Yer 1</b>', '1. durak · Konu', 0),
    3: ('2. durak · <b>Yer 2</b>', '2. durak · Konu', 7),
    4: ('3. durak · <b>Yer 3</b>', '3. durak · Konu', 16),
    5: ('4. durak · <b>Yer 4</b>', '4. durak · Konu', 24),
    6: ('5. durak · <b>Yer 5</b>', '5. durak · Konu', 33),
    7: ('6. durak · <b>Yer 6</b>', '6. durak · Konu', 41),
    8: ('Hülasa · <b>Yer</b>', 'Hülasa · özet', 50),
    9: ('Yan yol · <b>Yer</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    10: ('Yan yol · <b>Yer</b>', 'Yan yol 2 · Kıssalar', 61),
    11: ('Yan yol · <b>Yer</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    12: ('<b>Afyonkarahisar Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    13: ('<b>Afyonkarahisar Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
    14: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    15: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    16: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD ilerleme noktaları: 6 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 11: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 10, 14: 11, 15: 11, 16: 11}

u = KO.Unite(__file__, SAYFA, SIMDI)

# Üniteye özel yer tutucu örneği (şablonda {{selam|Elif}} → <b>Merhaba Elif</b>):
# u.yer_tutucu("selam", lambda ad: f"<b>Merhaba {ad}</b>")

if __name__ == "__main__":
    u.calistir()
