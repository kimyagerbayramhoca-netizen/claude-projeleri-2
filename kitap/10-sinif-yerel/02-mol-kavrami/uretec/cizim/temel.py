"""Temel SVG yardımcıları: kimlik ad alanı, gradyanlar, yol (path) kurucuları, renk ve gürültü.

Bütün illüstrasyonlar bu modülün `Svg` sınıfıyla kurulur. Her çizim kendi `onek`ini (ön ekini)
alır; böylece aynı HTML belgesine gömülen yüzlerce satır içi SVG'nin gradyan/klip kimlikleri
çakışmaz (çakışırsa Chrome ilk tanımı kullanır ve renkler bozulur).

Birim kuralı: sahnelerde 1 birim = 0,1 mm (210 mm genişlik = 2100 birim). Küçük ikonlar
kendi viewBox'larını kullanır.
"""
import math
import random

# ------------------------------------------------------------------ sayı biçimi

def f(v, h=1):
    """Sayıyı kısa yaz: 12.0 → '12', 3.14159 → '3.1' (h ondalık)."""
    s = f"{v:.{h}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def nok(p, h=1):
    return f"{f(p[0], h)} {f(p[1], h)}"


# ------------------------------------------------------------------ renk

def _hex(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _rgb(t):
    return "#" + "".join(f"{max(0, min(255, round(v))):02X}" for v in t)


def karis(a, b, t):
    """İki rengi karıştır (t=0 → a, t=1 → b)."""
    x, y = _hex(a), _hex(b)
    return _rgb(tuple(x[i] + (y[i] - x[i]) * t for i in range(3)))


def acik(c, t):
    return karis(c, "#FFFFFF", t)


def koyu(c, t):
    return karis(c, "#000000", t)


def golge_rengi(c, t=.35, ton="#1B2A55"):
    """Gölgeyi siyaha değil, mavi-mor bir tona doğru koyulaştır (daha canlı gölge)."""
    return karis(c, ton, t)


# ------------------------------------------------------------------ yol kurucuları

def cizgi_d(noktalar, kapali=False, h=1):
    if not noktalar:
        return ""
    s = "M" + nok(noktalar[0], h) + "".join(" L" + nok(p, h) for p in noktalar[1:])
    return s + (" Z" if kapali else "")


def egri_d(noktalar, kapali=False, gerginlik=1.0, h=1, bas_m=True):
    """Catmull-Rom → kübik Bezier. Noktalardan geçen yumuşak eğri."""
    p = list(noktalar)
    n = len(p)
    if n < 3:
        return cizgi_d(p, kapali, h)
    s = ("M" + nok(p[0], h)) if bas_m else ""
    rng = range(n) if kapali else range(n - 1)
    for i in rng:
        p0 = p[(i - 1) % n] if (kapali or i > 0) else p[i]
        p1 = p[i]
        p2 = p[(i + 1) % n]
        p3 = p[(i + 2) % n] if (kapali or i + 2 < n) else p2
        k = gerginlik / 6
        c1 = (p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k)
        c2 = (p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k)
        s += f" C{nok(c1, h)} {nok(c2, h)} {nok(p2, h)}"
    return s + (" Z" if kapali else "")


def daire_noktalari(cx, cy, r, n=24, bas=0.0, ry=None):
    ry = r if ry is None else ry
    return [(cx + r * math.cos(bas + 2 * math.pi * i / n), cy + ry * math.sin(bas + 2 * math.pi * i / n)) for i in range(n)]


def yildiz_noktalari(cx, cy, R, r, kose=8, bas=-math.pi / 2):
    pts = []
    for i in range(2 * kose):
        a = bas + math.pi * i / kose
        rr = R if i % 2 == 0 else r
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def selcuklu_yildizi(cx, cy, R):
    """8 köşeli Selçuklu yıldızı: iki karenin üst üste binmesi (iç yarıçap R·cos(45°)/cos(22,5°))."""
    r = R * math.cos(math.pi / 4) / math.cos(math.pi / 8)
    return yildiz_noktalari(cx, cy, R, r, 8, -math.pi / 2)


def dondur(p, a, mx=0, my=0):
    c, s = math.cos(a), math.sin(a)
    x, y = p[0] - mx, p[1] - my
    return (mx + x * c - y * s, my + x * s + y * c)


# ------------------------------------------------------------------ gürültü

def orta_nokta(a, b, derinlik, puruz, rng, azalma=0.55):
    """İki nokta arasında orta nokta yer değiştirmesiyle doğal sırt çizgisi (dağ, kaya)."""
    pts = [a, b]
    amp = puruz
    for _ in range(derinlik):
        yeni = [pts[0]]
        for i in range(len(pts) - 1):
            p, q = pts[i], pts[i + 1]
            m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + rng.uniform(-amp, amp))
            yeni += [m, q]
        pts = yeni
        amp *= azalma
    return pts


def deger_gurultusu(n, olcek, rng):
    """1B yumuşak gürültü: n örnek, yaklaşık `olcek` örnekte bir rastgele düğüm."""
    dugum = [rng.uniform(-1, 1) for _ in range(int(n / olcek) + 3)]
    out = []
    for i in range(n):
        u = i / olcek
        k = int(u)
        t = u - k
        t = t * t * (3 - 2 * t)
        out.append(dugum[k] * (1 - t) + dugum[k + 1] * t)
    return out


# ------------------------------------------------------------------ SVG kurucu

class Svg:
    """Kimlik ad alanlı SVG parçası.

    s = Svg('edremit')
    gok = s.lin([(0, '#FFB'), (1, '#F80')])          # → 'url(#edremit-l1)'
    s += f'<rect width="10" height="10" fill="{gok}"/>'
    html = s.cikti('0 0 10 10', w='100%')
    """

    def __init__(self, onek):
        self.onek = onek
        self.n = 0
        self.defs = []
        self.parca = []

    # kimlik
    def kid(self, ad="k"):
        self.n += 1
        return f"{self.onek}-{ad}{self.n}"

    def __iadd__(self, s):
        self.parca.append(s)
        return self

    def ekle(self, s):
        self.parca.append(s)

    def tanim(self, s):
        self.defs.append(s)

    # gradyanlar
    @staticmethod
    def _duraklar(duraklar):
        out = []
        for d in duraklar:
            o, c = d[0], d[1]
            op = d[2] if len(d) > 2 else None
            out.append(f'<stop offset="{f(o, 3)}" stop-color="{c}"' + (f' stop-opacity="{f(op, 3)}"' if op is not None else "") + "/>")
        return "".join(out)

    def lin(self, duraklar, x1=0, y1=0, x2=0, y2=1, kull=None, donus=None, ad="l"):
        i = self.kid(ad)
        u = f' gradientUnits="{kull}"' if kull else ""
        t = f' gradientTransform="{donus}"' if donus else ""
        self.defs.append(f'<linearGradient id="{i}" x1="{f(x1, 3)}" y1="{f(y1, 3)}" x2="{f(x2, 3)}" y2="{f(y2, 3)}"{u}{t}>{self._duraklar(duraklar)}</linearGradient>')
        return f"url(#{i})"

    def rad(self, duraklar, cx=.5, cy=.5, r=.5, fx=None, fy=None, kull=None, donus=None, ad="r"):
        i = self.kid(ad)
        u = f' gradientUnits="{kull}"' if kull else ""
        t = f' gradientTransform="{donus}"' if donus else ""
        fo = (f' fx="{f(fx, 3)}"' if fx is not None else "") + (f' fy="{f(fy, 3)}"' if fy is not None else "")
        self.defs.append(f'<radialGradient id="{i}" cx="{f(cx, 3)}" cy="{f(cy, 3)}" r="{f(r, 3)}"{fo}{u}{t}>{self._duraklar(duraklar)}</radialGradient>')
        return f"url(#{i})"

    def klip(self, icerik, ad="c"):
        i = self.kid(ad)
        self.defs.append(f'<clipPath id="{i}">{icerik}</clipPath>')
        return f"url(#{i})"

    def maske(self, icerik, ad="m"):
        i = self.kid(ad)
        self.defs.append(f'<mask id="{i}" maskUnits="userSpaceOnUse">{icerik}</mask>')
        return f"url(#{i})"

    def desen(self, w, h, icerik, kull="userSpaceOnUse", donus=None, ad="p"):
        i = self.kid(ad)
        t = f' patternTransform="{donus}"' if donus else ""
        self.defs.append(f'<pattern id="{i}" width="{f(w, 2)}" height="{f(h, 2)}" patternUnits="{kull}"{t}>{icerik}</pattern>')
        return f"url(#{i})"

    def govde(self):
        d = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return d + "".join(self.parca)

    def cikti(self, vb, w=None, h=None, cls=None, stil=None, oz="", par=None):
        a = f' viewBox="{vb}"'
        if w is not None:
            a += f' width="{w}"'
        if h is not None:
            a += f' height="{h}"'
        if cls:
            a += f' class="{cls}"'
        if stil:
            a += f' style="{stil}"'
        if par:
            a += f' preserveAspectRatio="{par}"'
        return f'<svg xmlns="http://www.w3.org/2000/svg"{a}{(" " + oz) if oz else ""}>{self.govde()}</svg>'


def rng(tohum):
    return random.Random(tohum)
