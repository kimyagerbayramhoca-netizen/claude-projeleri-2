#!/usr/bin/env python3
"""Deneme ünitesi doğrulaması: yeni bileşenlerin sayfadan okunan işaretleri hesapla aynı mı? (dogrula_ortak yardımcıları)

    python3 uretec/dogrula.py      → SONUÇ: hepsi doğru
"""
import os
import re
import sys

ORTAK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ORTAK)
from dogrula_ortak import (D, kontrol, sayfa_oku, kendini_dene_ayni, sifreli_kapi_ayni, celdirici_ayni, robot_ayni,  # noqa: E402
                           katla_ayni, uc_boyut_resimleri, mk)
from cizim import katla as KC  # noqa: E402

html = sayfa_oku(__file__)
yol = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "unite.html")

# Kendini dene: CCl4 dörtyüzlü ve simetrik → apolar; doğrusal H2O'da iki O–H çekişi götürür → polar olmazdı
kendini_dene_ayni(html, {"KD1": ["apolar", "olmazdı"]})

# Şifreli Kapı: doğru seçenekler PROTON
sifreli_kapi_ayni(html, "PROTON")

# Çeldirici röntgeni: 27/13 Al3+ → p = 13, n = 27 − 13 = 14, e = 13 − 3 = 10
p, n, e = 13, 27 - 13, 13 - 3
celdirici_ayni(html, {"CR1": ("B", f"{p}, {n}, {e}")})

# Robot: Na+ 10 elektron → neon (Ne, Z = 10) düzeni, argon değil (Ar 18): 3. cümle hatalı
robot_ayni(html, {"RB1": 3})

# Kat sayfası: ürünler ve bağ türleri katla.BAG tablosundan; ürünlerin formülü atom sayımıyla
beklenen = {}
for b in KC.BAG:
    urun = b["denklem"][0].split("→")[-1].strip() + b["denklem"][1] + b["denklem"][2]
    beklenen[b["kod"]] = (urun.replace("_", ""), b["tur"])
katla_ayni(html, beklenen)
kontrol("katla: NaCl ve MgO iyonik (metal + ametal), H2 ve O2 kovalent", [beklenen[k][1] for k in ("B1", "B2", "B3", "B4")] == ["iyonik", "iyonik", "kovalent", "kovalent"])
kontrol("katla: ürün kütleleri NaCl 58,5 · MgO 40", mk("NaCl") == 58.5 and mk("MgO") == 40)

# 3B resimleri: dosya var, ölçü = piksel / 300 dpi
sorun = uc_boyut_resimleri(html, yol)
kontrol(f"3B resimleri ölçüde ve yerinde {sorun or ''}", not sorun)

# palet ve konu karakterleri: yalnız kullanılan semboller gömülü
kontrol("palet: <html data-tema=cini-toprak>", 'data-tema="cini-toprak"' in re.search(r"<html[^>]*>", html).group(0))
semboller = set(re.findall(r'<symbol id="(kk-[^"]+)"', html))
kullanilan = set(re.findall(r'href="#(kk-[\w-]+)"', html))
kontrol(f"konu karakterleri: {len(semboller)} sembol, hepsi kullanılıyor ya da kullanılanın içinde", kullanilan <= semboller and len(semboller) < 30)

# köşe sineması: 1. sayfa (sağ) → 1. kare; kat sayfası 3 → 2. kare
kontrol("köşe sineması: s.1'de 1. kare", re.search(r'class="kare film-kose"[^>]*data-kare="1"', html) is not None)
kontrol("köşe sineması: kat sayfasında 2/24", "köşe sineması · 2/24" in html)

D.sonuc()
