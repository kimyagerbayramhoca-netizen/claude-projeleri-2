"""Mol Kavramı · üniteye özel çizimler (kur_ortak {{info|…}} ve {{sahne|…}} için önce buraya bakar).

Van turu sahneleri ortak kütüphanededir (cizim/sahneler.py: edremit, gevas, …, panorama); burada yalnız
bu üniteye özgü küçük bilgi grafikleri durur.
"""
from cizim.temel import Svg
from cizim.renkler import OBS, LAJVER, ALTIN, MER

T = 'font-family="Nunito" font-weight="800"'


def ustad_grafik(onek="ust-graf"):
    """Üstad 5: kaba önce X (CH4), sonra Y (SO2) eklenir. Toplam kütle (g) – toplam atom (mol) grafiği.
    Noktalar (0; 0) → (8; 2,5) → (20,8; 3,1); dogrula.py aynı değerleri hesaplar."""
    s = Svg(onek)
    W, H = 400, 300
    x0, y0, x1, y1 = 58, 252, 380, 24          # eksen kutusu
    X = lambda g: x0 + (x1 - x0) * g / 24
    Y = lambda n: y0 - (y0 - y1) * n / 3.6
    s += f'<rect width="{W}" height="{H}" rx="14" fill="#FFFDF7"/>'
    for g in (4, 8, 12, 16, 20, 24):
        s += f'<path d="M{X(g):.1f} {y0} V{y1}" stroke="#E2DCC8" stroke-width="1.4"/>'
    for n in (1, 2, 3):
        s += f'<path d="M{x0} {Y(n):.1f} H{x1}" stroke="#E2DCC8" stroke-width="1.4"/>'
    s += f'<path d="M{x0} {y1 - 6} V{y0} H{x1 + 6}" fill="none" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M{x0} {y1 - 14} l-6 10 h12 Z M{x1 + 14} {y0} l-10 -6 v12 Z" fill="{OBS}"/>'
    s += (f'<path d="M{X(8):.1f} {y0} V{Y(2.5):.1f} H{x0} M{X(20.8):.1f} {y0} V{Y(3.1):.1f} H{x0}" fill="none" stroke="{ALTIN}" '
          f'stroke-width="1.8" stroke-dasharray="6 5"/>')
    s += f'<path d="M{X(0):.1f} {Y(0):.1f} L{X(8):.1f} {Y(2.5):.1f}" stroke="{LAJVER}" stroke-width="5" stroke-linecap="round"/>'
    s += f'<path d="M{X(8):.1f} {Y(2.5):.1f} L{X(20.8):.1f} {Y(3.1):.1f}" stroke="{MER}" stroke-width="5" stroke-linecap="round"/>'
    for g, n in ((8, 2.5), (20.8, 3.1)):
        s += f'<circle cx="{X(g):.1f}" cy="{Y(n):.1f}" r="6.5" fill="#fff" stroke="{OBS}" stroke-width="2.6"/>'
    s += f'<text x="{X(3.2):.1f}" y="{Y(1.75):.1f}" {T} font-size="25" fill="{LAJVER}">X</text>'
    s += f'<text x="{X(14):.1f}" y="{Y(3.08):.1f}" {T} font-size="25" fill="{MER}">Y</text>'
    for g, et in ((8, "8"), (20.8, "20,8")):
        s += f'<text x="{X(g):.1f}" y="{y0 + 26}" text-anchor="middle" {T} font-size="21" fill="{OBS}">{et}</text>'
    for n, et in ((2.5, "2,5"), (3.1, "3,1")):
        s += f'<text x="{x0 - 8}" y="{Y(n) + 7:.1f}" text-anchor="end" {T} font-size="21" fill="{OBS}">{et}</text>'
    s += f'<text x="{x0 - 8}" y="{y0 + 7}" text-anchor="end" {T} font-size="21" fill="{OBS}">0</text>'
    s += f'<text x="{x1}" y="{y0 - 12}" text-anchor="end" {T} font-size="19" fill="#56636E">kütle (g)</text>'
    s += f'<text x="{x0 + 10}" y="{y1 + 6}" {T} font-size="19" fill="#56636E">atom (mol)</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ustad-graf")
