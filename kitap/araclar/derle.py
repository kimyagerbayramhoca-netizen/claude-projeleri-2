#!/usr/bin/env python3
"""Ünite kaynağını (kaynak.html) baskıya hazır HTML'e çevirir, sonra PDF üretir.

Kısa yazım kuralları (yalnızca kaynak.html içinde):
  {C2H6}        -> kimyasal formül, rakamlar alt simge olur:  C₂H₆
  {Mg(OH)2}     -> parantezli formüller de çalışır
  10^23, 10^-22 -> üs (sup)
  [[35|17|Cl]]  -> izotop gösterimi: kütle no üstte, atom no altta
  @ikon:ad      -> stil/ikonlar.py içindeki SVG ikon

Kullanım:  python3 araclar/derle.py 10-sinif/02-mol-kavrami
"""
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "araclar"))
from ikonlar import IKONLAR  # noqa: E402


def formul(m):
    ic = m.group(1)
    ic = re.sub(r"(?<=[A-Za-z\)])(\d+)", r"<sub>\1</sub>", ic)
    return f'<span class="f">{ic}</span>'


def izotop(m):
    kutle, atom, sembol = m.groups()
    return (f'<span class="izotop"><span class="yz"><span>{kutle}</span>'
            f'<span>{atom}</span></span>{sembol}</span>')


def donustur(html: str) -> str:
    # <style> ve <svg> bloklarına dokunma
    parcalar = re.split(r"(<style.*?</style>|<svg.*?</svg>)", html, flags=re.S)
    cikti = []
    for p in parcalar:
        if p.startswith("<style") or p.startswith("<svg"):
            cikti.append(p)
            continue
        p = re.sub(r"\[\[(\w+)\|(\w+)\|(\w+)\]\]", izotop, p)
        p = re.sub(r"\{([A-Za-z0-9()]+)\}", formul, p)
        p = re.sub(r"\^(-?\d+)", r"<sup>\1</sup>", p)
        p = re.sub(r"@ikon:(\w+)", lambda m: IKONLAR[m.group(1)], p)
        cikti.append(p)
    return "".join(cikti)


def main():
    unite = KOK / sys.argv[1]
    kaynak = (unite / "kaynak.html").read_text(encoding="utf-8")
    css = (KOK / "stil" / "kitap.css").read_text(encoding="utf-8")
    html = donustur(kaynak).replace("/*KITAP_CSS*/", css)
    hedef_html = unite / "unite.html"
    hedef_html.write_text(html, encoding="utf-8")
    hedef_pdf = unite / (unite.name + ".pdf")
    subprocess.run(["node", str(KOK / "araclar" / "pdf.js"), str(hedef_html), str(hedef_pdf)], check=True)
    print("Hazır:", hedef_pdf)


if __name__ == "__main__":
    main()
