#!/usr/bin/env python3
"""Kimya Rotası · KİTAP ÇERÇEVESİ kurucusu: kapaklar, rehber, harita/içindekiler, zaman şeridi, periyodik tablo,
kavram sözlüğü, nişan albümü ve "Notlar" sayfaları → sayfalar/kitap-<sınıf>.html (+ plan-<sınıf>.json)

    python3 uretec/kur.py 10                 # 10. sınıf çerçevesi (sayfa planı ünitelerden hesaplanır)
    python3 uretec/kur.py 9 --plan plan.json # sayfa planını dosyaya da yaz (kitap_yerel.js kullanır)
Sonra önizleme:  node uretec/bas.js sayfalar/kitap-10.html     (onizleme/*.png + taşma denetimi)
Bütün kitap:     node kitap_yerel.js 10                         (kitap/kimya-rotasi-10-yerel.pdf)

Veri: ../rotalar.json + hazır ünitelerin uretec/meta.json dosyaları (bkz. veri.py).
Ortak kütüphane (yerel-ortak/) yalnız içe aktarılır, değiştirilmez.
"""
import html as _html
import json
import os
import re
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
CERCEVE = os.path.dirname(BURA)
ORTAK = os.path.normpath(os.path.join(CERCEVE, "..", "yerel-ortak"))
for _p in (ORTAK, BURA):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import veri as V  # noqa: E402
import harita as HR  # noqa: E402
from cizim.temel import Svg, f, cizgi_d, selcuklu_yildizi  # noqa: E402
from cizim import karakter as K, sus as U  # noqa: E402
from cizim.renkler import GOL, GOL_K, KEH, MER, KOB, ALTIN, OBS, LAJVER, ERGUVAN  # noqa: E402

from yardim import yeni, e, zengin, zemin, cini, defs  # noqa: E402


class Kitap:
    """Bir sınıfın çerçeve sayfaları."""

    def __init__(self, sinif):
        self.sinif = int(sinif)
        self.yollar = V.yollar(self.sinif)
        self.ad = f"Kimya Rotası {self.sinif}"
        self.alt_baslik = V.alt_baslik(self.sinif)
        self.baslangic = V.baslangic()
        import sozluk as SZ
        import album as AL
        self.sozluk_sayfalari = SZ.sayfalara_bol(self)
        self.album_sayfalari = AL.sayfalara_bol(self)
        self.kavram_sayisi = sum(len(sf) for sf in self.sozluk_sayfalari) if self.sozluk_sayfalari and isinstance(self.sozluk_sayfalari[0], list) else 0
        self.plan, self.baslar = V.sayfa_plani(self.sinif, self.yollar, len(self.sozluk_sayfalari), len(self.album_sayfalari))

    # ---------------------------------------------------------------- çerçeve parçaları
    def no(self, tur, **k):
        return V.ilk_no(self.plan, tur, **k)

    def hud(self, yer, vurgu=""):
        yol = "".join(f'<i style="--r:{y["renk"]}" class="{"" if y["hazir"] else "yok"}">{y["yol"]}</i>' for y in self.yollar)
        return (f'<header class="hud"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>{self.ad}</span>'
                f'<span class="yer">{yer}{" · <b>" + vurgu + "</b>" if vurgu else ""}</span>'
                f'<span class="yollar"><span class="yazi">Yollar</span>{yol}</span></header>')

    def alt(self, konu, no):
        return (f'<footer class="alt"><span>{self.ad} · {e(self.alt_baslik)}</span><span>{konu}</span>'
                f'<span class="no"><svg viewBox="0 0 100 100"><use href="#no-yildiz"/></svg><b>{no}</b></span></footer><div class="ebru-alt"></div>')

    def sayfa(self, sinif_adi, ad, no, ic, cerceve=True, hud=None, konu=""):
        """<section> sarmalayıcı. ad: önizleme dosya adı parçası."""
        p = []
        if cerceve:
            p += [zemin(), self.hud(*hud) if hud else "", cini()]
        p.append(ic)
        if cerceve and konu:
            p.append(self.alt(konu, no))
        return (f'<section class="sayfa {sinif_adi}" data-ad="{self.sinif:02d}-{no:02d}-{ad}" data-no="{no}">' + "".join(p) + "</section>")

    # ---------------------------------------------------------------- sayfalar
    def kur(self):
        import sayfalar as S
        bolum = []
        for p in self.plan:
            t = p["tur"]
            if t == "unite" or t == "hazine":
                continue
            fn = getattr(S, t)
            bolum.append(fn(self, p))
        govde = "\n".join(bolum)
        return (f'<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<title>{self.ad} · kitap çerçevesi</title>\n'
                f'<link rel="stylesheet" href="../../yerel-ortak/stil.css">\n<link rel="stylesheet" href="../cerceve.css">\n</head>\n<body>\n'
                f'<!-- ÜRETİLİR: uretec/kur.py {self.sinif}. Düzeltmeyi uretec/ altındaki modüllerde yap. -->\n{defs()}\n{govde}\n</body>\n</html>\n')


def main(argv):
    if not argv or argv[0] not in ("9", "10"):
        raise SystemExit("kullanım: python3 uretec/kur.py <9|10> [--plan plan.json]")
    k = Kitap(argv[0])
    html = k.kur()
    os.makedirs(os.path.join(CERCEVE, "sayfalar"), exist_ok=True)
    hedef = os.path.join(CERCEVE, "sayfalar", f"kitap-{k.sinif}.html")
    with open(hedef, "w", encoding="utf-8") as fp:
        fp.write(html)
    plan = {"sinif": k.sinif, "html": hedef, "sayfalar": k.plan, "baslar": k.baslar,
            "uniteler": [{"yol": y["yol"], "rota": y["rota"], "unite": y["unite"], "klasor": y["klasor"], "dizin": y["dizin"],
                          "sayfa_sayisi": y["sayfa_sayisi"], "varyantlar": y["varyantlar"]} for y in k.yollar if y["hazir"]]}
    if "--plan" in argv:
        pyol = argv[argv.index("--plan") + 1]
        with open(pyol, "w", encoding="utf-8") as fp:
            json.dump(plan, fp, ensure_ascii=False, indent=1)
    with open(os.path.join(CERCEVE, "sayfalar", f"plan-{k.sinif}.json"), "w", encoding="utf-8") as fp:
        json.dump(plan, fp, ensure_ascii=False, indent=1)
    cerceve_n = sum(1 for p in k.plan if p["tur"] not in ("unite", "hazine"))
    print(f"{os.path.relpath(hedef)} yazıldı ({len(html) / 1024:.0f} KB) · kitap {len(k.plan)} sayfa, çerçeve {cerceve_n} sayfa")


if __name__ == "__main__":
    main(sys.argv[1:])
