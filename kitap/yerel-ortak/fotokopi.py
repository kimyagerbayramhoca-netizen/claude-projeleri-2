"""Siyah-beyaz FOTOKOPİ ana nüshası: kurulum anında palet eşlemesi (kur_ortak.Unite.kur("fotokopi") çağırır).

CSS `filter: grayscale()` KULLANILMAZ: Chromium filtreli öğeyi PDF'te rasterleştirir (bulanık yazı, büyük dosya).
Bunun yerine üretilen HTML'deki satır içi SVG renkleri griye çevrilir, HTML kısmı da stil.css §34 (html.fotokopi)
kurallarıyla siyah-beyaza döner. Sonuç vektör kalır, yazılar keskin, mürekkep az.

Eşleme (renk rolüne göre; L = algısal açıklık 0…1):
  dolgu   fill, stop-color          → çok açık gri: mürekkep = %22 × özgün mürekkep  (en koyu gece göğü bile ≈ %20 gri)
  çizgi   stroke                    → L < 0,62 ise koyu çizgi (L' = 0,55·L, siyaha yakın); açık çizgi dolgu gibi açılır
  yazı    text / tspan / textPath   → saf siyah (#000) — fill'i olmayan yazıya da eklenir
  karakter ayrıntısı                → <symbol> içindeki çok koyu dolgular (göz bebeği, kaş, saç; L < 0,16) orta gri (%45 açıklık):
                                      gözler okunur, büyük koyu alan oluşmaz
  maske / clipPath içi              → dokunulmaz (maskeler parlaklıkla çalışır)
"""
import re

FOTOKOPI_DOLGU = .22       # dolgunun özgün mürekkebinin kaçta kaçı kalsın
FOTOKOPI_CIZGI_ESIK = .62  # bundan koyu çizgiler koyu kalır


def _rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def aciklik(h):
    r, g, b = _rgb(h)
    return (.299 * r + .587 * g + .114 * b) / 255


def _gri(L):
    v = max(0, min(255, round(L * 255)))
    return f"#{v:02X}{v:02X}{v:02X}"


def dolgu_gri(h, sembolde=False):
    L = aciklik(h)
    if sembolde and L < .16:
        return _gri(.45)
    return _gri(1 - FOTOKOPI_DOLGU * (1 - L))


def cizgi_gri(h):
    L = aciklik(h)
    if L < FOTOKOPI_CIZGI_ESIK:
        return _gri(.55 * L)
    return dolgu_gri(h)


_HEX = re.compile(r"^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")
_NITELIK = re.compile(r'(\s)(fill|stroke|stop-color|flood-color|lighting-color|color)=("|\')(.*?)\3')
_ETIKET = re.compile(r"<(/?)([a-zA-Z][\w:.-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*?)(/?)>")
_YAZI = ("text", "tspan", "textpath")


def _nitelik_esle(ad, nitelik, yigin):
    sembolde = "symbol" in yigin

    def esle(m):
        bosluk, ozellik, tirnak, deger = m.groups()
        if not _HEX.match(deger.strip()):
            return m.group(0)
        if ozellik == "fill":
            yeni = "#000000" if ad in _YAZI else dolgu_gri(deger, sembolde)
        elif ozellik == "stroke":
            yeni = cizgi_gri(deger)
        elif ozellik in ("stop-color", "flood-color", "lighting-color"):
            yeni = dolgu_gri(deger)
        else:  # color
            yeni = "#000000"
        return f"{bosluk}{ozellik}={tirnak}{yeni}{tirnak}"

    nitelik = _NITELIK.sub(esle, nitelik)
    if ad == "text" and not re.search(r'\sfill=', nitelik):
        nitelik += ' fill="#000000"'
    return nitelik


def fotokopi_svg(html):
    """HTML içindeki bütün satır içi SVG'lerin renklerini griye eşler (yorumlar ve SVG dışı HTML olduğu gibi kalır)."""
    parcalar = re.split(r"(<!--.*?-->)", html, flags=re.S)
    out = []
    svg_derinlik = 0
    yigin = []
    for parca in parcalar:
        if parca.startswith("<!--"):
            out.append(parca)
            continue
        i = 0
        for m in _ETIKET.finditer(parca):
            out.append(parca[i:m.start()])
            i = m.end()
            kapanis, ad, nitelik, kendinden = m.groups()
            adk = ad.lower()
            if kapanis:
                if svg_derinlik:
                    while yigin and yigin[-1] != adk:
                        yigin.pop()
                    if yigin:
                        yigin.pop()
                    if adk == "svg":
                        svg_derinlik -= 1
                out.append(m.group(0))
                continue
            if adk == "svg":
                svg_derinlik += 1
            if svg_derinlik:
                if not any(e in ("mask", "clippath") for e in yigin):
                    nitelik = _nitelik_esle(adk, nitelik, yigin)
                if kendinden:
                    if adk == "svg":
                        svg_derinlik -= 1
                else:
                    yigin.append(adk)
                out.append(f"<{ad}{nitelik}{kendinden}>")
            else:
                out.append(m.group(0))
        out.append(parca[i:])
    return "".join(out)


def fotokopi_html(html):
    """Öğrenci HTML'inden fotokopi HTML'i: SVG renkleri griye, <html> etiketine class="fotokopi" (stil.css §34)."""
    html = fotokopi_svg(html)
    return re.sub(r"<html([^>]*)>", lambda m: f'<html{m.group(1)} class="fotokopi">' if "class=" not in m.group(1)
                  else m.group(0).replace('class="', 'class="fotokopi '), html, count=1)
