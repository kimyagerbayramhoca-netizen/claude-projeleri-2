"""Çerçeve sayfalarının ortak yardımcıları: kimlik sayacı, metin biçimi, sayfa zemini, çini şeridi, gizli semboller.

Ortak kurucu (yerel-ortak/kur_ortak.py) varsa onun zemin/çini/zengin işlevleri kullanılır; böylece çerçeve
sayfaları ünitelerle birebir aynı görünür. Yoksa aynı çizimin yerel kopyası devreye girer.
"""
import html as _html
import os
import re
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
ORTAK = os.path.normpath(os.path.join(BURA, "..", "..", "yerel-ortak"))
for _p in (ORTAK, BURA):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cizim.temel import Svg, f, cizgi_d, selcuklu_yildizi  # noqa: E402
from cizim import karakter as K, sus as U  # noqa: E402
from cizim.renkler import GOL, GOL_K, KEH, ALTIN, OBS  # noqa: E402

try:                                    # ortak kurucunun metin ve çerçeve yardımcıları (varsa)
    import kur_ortak as KO              # noqa: E402
except Exception:                       # noqa: BLE001
    KO = None

SAYAC = {"n": 0}


def yeni(onek):
    SAYAC["n"] += 1
    return f"{onek}{SAYAC['n']}"


def zengin(metin):
    """meta.json kısa yazımı (N_A, 10^23, {H2O}) → HTML. Ortak kurucudaki işlevi kullanır."""
    if KO is not None:
        return KO.zengin(metin)
    m = str(metin or "")
    m = re.sub(r"_(?:\{([^}]*)\}|(.))", lambda x: f"<sub>{x.group(1) or x.group(2)}</sub>", m)
    return re.sub(r"\^(?:\{([^}]*)\}|([-−+]?\d+))", lambda x: f"<sup>{x.group(1) or x.group(2)}</sup>", m)


def e(s):
    return _html.escape(str(s), quote=False)


# ------------------------------------------------------------------ sayfa çerçevesi

def zemin():
    if KO is not None:
        return KO.zemin()
    d = []
    for i in range(-1, 16):
        for j in range(-1, 21):
            cx, cy = 7.5 + i * 15, 7.5 + j * 15
            d.append(cizgi_d(selcuklu_yildizi(cx, cy, 3.6), True, 2))
            d.append(f"M{f(cx + 5.3)} {f(cy + 5.3)} l4.4 4.4")
    return (f'<svg class="zemin" viewBox="0 0 210 297" preserveAspectRatio="none"><path d="{" ".join(d)}" fill="none" '
            f'stroke="#DDEEEE" stroke-width=".22" stroke-linejoin="round"/></svg>')


def cini():
    if KO is not None:
        return KO.cini_serit()
    karo = U.cini_serit_ince().split(">", 1)[1].rsplit("</svg>", 1)[0]
    parca = "".join(f'<g transform="translate({k * 24} 0)">{karo}</g>' for k in range(30))
    return f'<svg class="cini-serit" viewBox="0 0 700 8" preserveAspectRatio="none">{parca}</svg>'


def defs():
    """Gizli semboller: logo, sayfa no yıldızı, karakterler, ikonlar + çerçeveye özgü semboller."""
    s = Svg("ortak")
    ga = s.lin([(0, "#FFE7A8"), (1, KEH)], 0, 0, 1, 1, ad="lg")
    gn = s.rad([(0, "#5FD3D0"), (.7, GOL), (1, GOL_K)], .4, .35, .75, ad="ng")
    sy = [f'<symbol id="logo-yildiz" viewBox="0 0 24 24"><path d="{cizgi_d(selcuklu_yildizi(12, 12, 11.4), True, 2)}" fill="{ga}" stroke="#FFF" stroke-width=".8"/>'
          f'<circle cx="12" cy="12" r="3.6" fill="{OBS}"/></symbol>',
          f'<symbol id="no-yildiz" viewBox="0 0 100 100"><path d="{cizgi_d(selcuklu_yildizi(50, 50, 48), True)}" fill="{ALTIN}" stroke="{OBS}" stroke-width="3"/>'
          f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 40), True)}" fill="{gn}" stroke="{OBS}" stroke-width="2"/></symbol>']
    import cizimler as CZ
    return (f'<svg class="gizli-defs" aria-hidden="true"><defs>{s.govde()}{"".join(sy)}{K.semboller()}{U.ikon_sembolleri()}'
            f'{CZ.semboller()}</defs></svg>')
