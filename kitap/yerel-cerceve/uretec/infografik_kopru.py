"""Ortak infografik modülündeki parçalara ince köprü (imza değişirse tek yerden düzeltilir)."""
import os
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
ORTAK = os.path.normpath(os.path.join(BURA, "..", "..", "yerel-ortak"))
if ORTAK not in sys.path:
    sys.path.insert(0, ORTAK)

from cizim import infografik as I  # noqa: E402


def unvan(onek, kat, renk):
    """Ahilik unvan rozeti (1 Çırak … 4 Üstad)."""
    return I.unvan_rozeti(onek, kat, renk)
