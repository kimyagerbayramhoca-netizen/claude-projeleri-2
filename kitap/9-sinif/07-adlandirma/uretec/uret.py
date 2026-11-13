#!/usr/bin/env python3
"""sablon.html -> ../kaynak.html
Şablonda iyonlar «SO4|2−» biçiminde yazılır; bu betik onları
<span class="f">SO<sub>4</sub><sup>2−</sup></span> biçimine çevirir.
Kullanım (ünite klasöründen): python3 uretec/uret.py"""
import re
from pathlib import Path

BURA = Path(__file__).resolve().parent


def iyon(m):
    f, q = m.group(1), m.group(2)
    f = re.sub(r"(?<=[A-Za-z\)])(\d+)", r"<sub>\1</sub>", f)
    return f'<span class="f">{f}<sup>{q}</sup></span>'


metin = (BURA / "sablon.html").read_text(encoding="utf-8")
metin = re.sub(r"«([A-Za-z0-9()]+)\|([0-9]*[+−])»", iyon, metin)
assert "«" not in metin and "»" not in metin, "çözülmemiş iyon yazımı kaldı"
(BURA.parent / "kaynak.html").write_text(metin, encoding="utf-8")
print("kaynak.html yazıldı")
