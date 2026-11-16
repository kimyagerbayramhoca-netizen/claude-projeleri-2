"""Karma örnek · sahneler: 10/04 Gazlar ünitesinin doğrulanmış sahneleri ve iki bilgi grafiği (değiştirilmeden, salt okunur).

Gazlar ünitesinin uretec/sahneler_unite.py ve infografik_unite.py dosyaları başka adlarla yüklenir (ad çakışması olmaz).
9. sınıf sayfaları atom-modelleri/uretec/sahneler_gelistirme.py'yi kullanır.
"""
import importlib.util
import os

_KITAP = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_GAZ = os.path.join(_KITAP, "10-sinif-yerel", "04-gazlar", "uretec")


def _yukle(ad, dosya):
    spec = importlib.util.spec_from_file_location(ad, os.path.join(_GAZ, dosya))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


import sys  # noqa: E402

GAZ_SAHNE = _yukle("gaz_sahne_unite", "sahneler_unite.py")
_eski = sys.modules.get("sahneler_unite")
sys.modules["sahneler_unite"] = GAZ_SAHNE          # Gazlar infografik_unite.py "import sahneler_unite" der
GAZ_INFO = _yukle("gaz_info_unite", "infografik_unite.py")
if _eski is None:
    del sys.modules["sahneler_unite"]
else:
    sys.modules["sahneler_unite"] = _eski


def bant_goreme():
    return GAZ_SAHNE.goreme()


def bant_kizilcukur():
    return GAZ_SAHNE.kizilcukur()


def bant_derinkuyu():
    return GAZ_SAHNE.derinkuyu()


def graham_boru(onek="gi-gra"):
    """NH₃–HCl borusu (Gazlar ünitesi, doğrulanmış: halka NH₃ ucundan ≈ 59 cm)."""
    return GAZ_INFO.graham_boru(onek)


def bant_kapadokya_gece():
    return GAZ_SAHNE.kapadokya_gece()
