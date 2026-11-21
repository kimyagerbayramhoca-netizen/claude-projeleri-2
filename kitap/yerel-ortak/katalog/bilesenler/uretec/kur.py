#!/usr/bin/env python3
"""Yeni ortak bileşenlerin DENEME ünitesi (katalog): her bileşen bir kez, palet, öğretmen ve fotokopi nüshalarıyla.

    python3 uretec/kur.py --hepsi && python3 uretec/dogrula.py && node ../../render.js . --hepsi
    python3 uretec/kur.py --tema gol-rasathane && node ../../render.js . --tema gol-rasathane

Sayfalar: 1 kısa bileşenler (Hap Bilgi ailesi, sohbet şeridi, konu karakterleri, Bir bakışta, Kendini dene, Yanlış ↔ Doğru,
Tahmin et) · 2 çizgi roman panosu + 3B kartları · 3 kat sayfası (sağ) · 4 karma sayfa (3'ün arkası) · 5 köşeyi katla (sağ) ·
6 köşenin arka yüzü · 7 gözlük sayfası · 8 köşe sineması (24 kare). Üretilen dosyalar (unite*.html, PDF, onizleme/, gorsel/)
git'e girmez; kaynak yalnız uretec/.
"""
import os
import sys

ORTAK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ORTAK)
import kur_ortak as KO  # noqa: E402

SAYFA = {
    1: ("Kısa bileşenler", "Hap Bilgi ailesi ve kısa bileşenler", 0),
    2: ("Pano ve 3B", "Çizgi roman panosu · 3B kartları", 7),
    3: ("<b>katla sayfası</b>", "katla sayfası", 18),
    4: ("Karma sayfa · <b>3’ün arka yüzü</b>", "Karma sayfa", 18),
    5: ("<b>Köşeyi katla</b>", "Köşeyi katla", 29),
    6: ("Köşenin sırrı · <b>5’in arka yüzü</b>", "Köşenin sırrı", 29),
    7: ("Ek · <b>3B gözlük</b>", "Ek · 3B gözlüğünü hazırla", 39),
    8: ("Köşe sineması", "Köşe sineması · 24 kare", 39),
}
SIMDI = {1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}

u = KO.Unite(__file__, SAYFA, SIMDI)
u.calistir()
