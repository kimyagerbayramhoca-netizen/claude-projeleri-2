#!/usr/bin/env python3
"""Baskı PDF'ine TrimBox (kesim) ve BleedBox (taşma) yazar: python3 pdf_kutular.py dosya.pdf [kenar_mm=12] [tasma_mm=3]

render.js --baski kâğıdı 234×321 mm basar: 210×297 mm kesim kutusu ortada (her yanda 12 mm), taşma payı 3 mm,
kesim izleri taşmanın dışında. Matbaa yazılımları kesim/taşmayı bu kutulardan okur.
"""
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

MM = 72 / 25.4


def kutula(yol, kenar=12.0, tasma=3.0, en=210.0, boy=297.0):
    """Kutular sayfanın SOL ÜST köşesinden ölçülür (HTML kâğıdı oradan başlar; Chromium sayfa kutusunu
    birkaç onda bir mm büyük yuvarlayabilir, sağ/alt kenara göre ölçmek kaydırırdı)."""
    w = PdfWriter(clone_from=PdfReader(yol))
    for p in w.pages:
        x0, y0 = float(p.mediabox.left), float(p.mediabox.top)      # PDF'te y yukarı doğru; üst kenar = top
        k, t, E, B = kenar * MM, tasma * MM, en * MM, boy * MM
        tr = [x0 + k, y0 - k - B, x0 + k + E, y0 - k]
        p.trimbox = RectangleObject([round(v, 3) for v in tr])
        p.bleedbox = RectangleObject([round(v, 3) for v in (tr[0] - t, tr[1] - t, tr[2] + t, tr[3] + t)])
    with open(yol, "wb") as fp:
        w.write(fp)
    p = w.pages[0]
    print(f"TrimBox {[round(float(v) / MM, 1) for v in p.trimbox]} mm · BleedBox {[round(float(v) / MM, 1) for v in p.bleedbox]} mm · "
          f"MediaBox {[round(float(v) / MM, 1) for v in p.mediabox]} mm · {len(w.pages)} sayfa")


if __name__ == "__main__":
    kutula(sys.argv[1], *(float(a) for a in sys.argv[2:4]))
