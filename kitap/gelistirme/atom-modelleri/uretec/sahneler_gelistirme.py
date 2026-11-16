"""Geliştirme örneği · sahne bantları: 9/03 ünitesinin doğrulanmış sahneleri (değiştirilmeden) + tema dokunuşu.

9/03'ün uretec/sahneler_unite.py dosyası burada başka bir adla (ay_sahneler) salt okunur yüklenir; ad çakışması olmaz.
Rasathane Gecesi temasında sahneler tema.py'de gece eşlemesiyle boyanır; burada yalnız gökyüzünün üstüne (ön planın
ARKASINA) sabit renkli yıldızlar eklenir.
"""
import importlib.util
import os
import re

import tema
from cizim import sahne as S
from cizim.temel import Svg

_KITAP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_AY = os.path.join(_KITAP, "9-sinif-yerel", "03-atom-ve-yapisi", "uretec")


def _yukle(ad, dosya):
    spec = importlib.util.spec_from_file_location(ad, os.path.join(_AY, dosya))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AY_SAHNE = _yukle("ay_sahneler", "sahneler_unite.py")
AY_INFO = _yukle("ay_infografik", "infografik_unite.py")


def _gece(svg, tohum, ufuk=250):
    """Gece temasında: gök dikdörtgeninin hemen ardına yıldızlar (sabit renk) ekle."""
    if tema.TEMALAR[tema.AKTIF]["sahne"] != "gece":
        return svg
    s = Svg(f"gy{tohum}")
    yildiz = S.yildizlar(s, 0, 0, 2100, ufuk, 150, tohum)
    m = re.search(r"</defs>\s*<rect[^>]*/>", svg)
    if not m:
        return svg
    return svg[:m.end()] + f'<g data-tema-sabit="">{yildiz}</g>' + svg[m.end():]


def bant_gobeklitepe():
    return _gece(AY_SAHNE.gobeklitepe(), 61, 230)


def bant_harran():
    return _gece(AY_SAHNE.harran(), 62, 260)


def bant_hoyuk():
    return _gece(AY_SAHNE.harran_hoyuk(), 63, 200)


def bant_gece():
    return AY_SAHNE.harran_gece()
