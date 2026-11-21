"""Yazı genişliği ölçümü (fontTools): SVG yazılarının pencerelere sığdığını hesapla denetlemek için.

genislik("Magnezyum", "nunito", 800, 2.4) → mm (harf arası düzeltmesi ve bitişik harf yok; SVG'de de kapalı).
"""
import os
from functools import lru_cache

FONT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "fontlar"))
YOL = {"nunito": "nunito/static/Nunito-{w}.ttf", "baloo": "baloobhaijaan2/static/BalooBhaijaan2-{w}.ttf"}
PT = 0.3528


@lru_cache(None)
def _font(aile, agirlik):
    from fontTools.ttLib import TTFont
    t = TTFont(os.path.join(FONT, YOL[aile].format(w=agirlik)))
    return t.getBestCmap(), t["hmtx"].metrics, t["head"].unitsPerEm, t["OS/2"].sCapHeight


def genislik(metin, aile="nunito", agirlik=800, boy=3.0):
    cmap, hmtx, em, _ = _font(aile, agirlik)
    top = 0
    for c in metin:
        ad = cmap.get(ord(c))
        if ad is None:
            raise ValueError(f"{aile}-{agirlik} fontunda yok: {c!r} ({metin})")
        top += hmtx[ad][0]
    return top / em * boy


def buyuk_harf(aile="nunito", agirlik=800, boy=3.0):
    _, _, em, cap = _font(aile, agirlik)
    return cap / em * boy
