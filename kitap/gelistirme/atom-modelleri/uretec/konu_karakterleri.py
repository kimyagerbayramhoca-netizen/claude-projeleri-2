"""Konu karakterleri · atom modelleri ve tanecikler (ortak kütüphaneye taşınabilir: cizim/konu_karakterleri.py).

Pamuk / Elif / Yusuf ile aynı çizgi dili: koyu kontur (OBS), düz renk + yumuşak radyal gölge, büyük göz, pembe yanak.
Her karakter bir <symbol>'dür (kimlik öneki kk-); sayfaya {{defs}} ile bir kez gömülür, her yerde
<svg viewBox="…"><use href="#kk-…"/></svg> ya da SVG içinde <use href="#kk-…" x y width height/> ile çağrılır.
Kimlikler kk- ile başladığı için tema eşlemesi (tema.py) bu karakterlerin rengine DOKUNMAZ: tanecik renkleri
kitap boyunca aynı kalır (proton mercan, nötron gri, elektron kobalt, foton dalga boyunun rengi).

Gerçek bilim insanlarının yüzü çizilmez: model karakterleri "modelin kendisidir" (bilardo topu, üzümlü kek …);
ad ve yıl sayfada levhaya yazılır.

Kimlikler (viewBox):
  modeller   kk-atomos, kk-dalton, kk-thomson, kk-rutherford, kk-bohr, kk-bulut            0 0 120 120
  tanecikler kk-proton, kk-notron, kk-elektron[-heyecan|-sasiran|-sakin|-sersem]           0 0 60 60
             kk-alfa[-mutlu|-sasiran|-sersem]                                                0 0 72 66
             kk-foton-656 / -486 / -434 / -410 / -uv  (dalga boyuna göre renk)              0 0 92 50
  genel      kk-su (su molekülü), kk-iyon-arti (Na⁺), kk-iyon-eksi (Cl⁻), kk-atom             0 0 100 84 · 0 0 64 64 · 0 0 80 80
"""
import math
from cizim.temel import Svg, f, egri_d, acik, koyu, karis, rng as RNG
from cizim.renkler import OBS, KOB, GOL, KEH, MER, MER_K, ATOM

CZ = OBS
K = 2.4
GOZ = "#2A211F"
YANAK = "#F59C9C"
PROTON, NOTRON, ELEKTRON = "#E2533D", "#9AA8B6", "#2B50B5"     # 9/03 infografik_unite ile aynı

# görünür ışık: dalga boyu (nm) → renk (9/03 infografik_unite._NM ile aynı tablo; dogrula.py denetler)
NM_TABLO = [(400, "#6A1FD0"), (420, "#5B2BE0"), (440, "#3D3BE8"), (470, "#1E7BE8"), (490, "#14B8E6"), (510, "#22C47A"),
            (540, "#6CCB2E"), (570, "#E8E02A"), (590, "#FFB21A"), (620, "#FF6A1A"), (660, "#E8282B"), (700, "#B01A1A")]
UV_RENK = "#B49CEB"


def nm_renk(nm):
    for (a, ca), (b, cb) in zip(NM_TABLO, NM_TABLO[1:]):
        if a <= nm <= b:
            return karis(ca, cb, (nm - a) / (b - a))
    return NM_TABLO[0][1] if nm < 400 else NM_TABLO[-1][1]


# ------------------------------------------------------------------ yüz parçaları

def _goz(cx, cy, o, ifade, sklera, yon=0.0):
    k = max(1.3, 1.9 * o)
    if ifade in ("gulen", "gururlu"):            # mutlu kapalı göz ∩
        return f'<path d="M{f(cx - 4 * o)} {f(cy + 1.4 * o)} Q{f(cx)} {f(cy - 4.6 * o)} {f(cx + 4 * o)} {f(cy + 1.4 * o)}" fill="none" stroke="{CZ}" stroke-width="{f(k * 1.25)}" stroke-linecap="round"/>'
    if ifade == "sakin":                          # dingin, kapalı göz ∪
        return f'<path d="M{f(cx - 4 * o)} {f(cy - 1 * o)} Q{f(cx)} {f(cy + 3.6 * o)} {f(cx + 4 * o)} {f(cy - 1 * o)}" fill="none" stroke="{CZ}" stroke-width="{f(k * 1.2)}" stroke-linecap="round"/>'
    if ifade == "sersem":                         # fır dönen göz (sarmal)
        pts = [(cx + (.3 + t * .55) * o * math.cos(t * 1.15), cy + (.3 + t * .55) * o * math.sin(t * 1.15)) for t in range(0, 8)]
        return f'<path d="{egri_d(pts, h=2)}" fill="none" stroke="{CZ}" stroke-width="{f(k)}" stroke-linecap="round"/>'
    buyuk = ifade in ("sasiran", "heyecan")
    rx, ry = (4.3 * o, 5.4 * o) if buyuk else (3.8 * o, 4.6 * o)
    if ifade == "kararli":
        ry = 3.9 * o
    o_ = []
    if sklera:
        sx, sy = rx * 1.45, ry * 1.3
        o_.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(sx)}" ry="{f(sy)}" fill="#FFFFFF" stroke="{CZ}" stroke-width="{f(k * .8)}"/>')
        pr = .72 if not buyuk else .62
        o_.append(f'<ellipse cx="{f(cx + yon * o)}" cy="{f(cy + .4 * o)}" rx="{f(rx * pr)}" ry="{f(ry * pr)}" fill="{GOZ}"/>')
        o_.append(f'<circle cx="{f(cx - 1 * o + yon * o)}" cy="{f(cy - 1.2 * o)}" r="{f(1.25 * o)}" fill="#FFFFFF"/>')
    else:
        o_.append(f'<ellipse cx="{f(cx + yon * o)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{GOZ}"/>')
        o_.append(f'<circle cx="{f(cx - 1.3 * o + yon * o)}" cy="{f(cy - 1.7 * o)}" r="{f(1.55 * o)}" fill="#FFFFFF"/>')
        o_.append(f'<circle cx="{f(cx + 1.4 * o + yon * o)}" cy="{f(cy + 1.7 * o)}" r="{f(.7 * o)}" fill="#FFFFFF" opacity=".9"/>')
    if ifade == "heyecan":                        # pırıltı
        o_.append(f'<path d="M{f(cx + 2.2 * o)} {f(cy - 3.4 * o)} l{f(.6 * o)} {f(1.3 * o)} l{f(1.3 * o)} {f(.6 * o)} l{f(-1.3 * o)} {f(.6 * o)} l{f(-.6 * o)} {f(1.3 * o)} l{f(-.6 * o)} {f(-1.3 * o)} l{f(-1.3 * o)} {f(-.6 * o)} l{f(1.3 * o)} {f(-.6 * o)} Z" fill="#FFFFFF"/>')
    return "".join(o_)


def _kas(cx, cy, o, ifade, ex):
    k = max(1.3, 2.0 * o)
    y = cy - 8.6 * o
    d = ""
    if ifade == "sasiran":
        d = (f"M{f(cx - ex - 4 * o)} {f(y - .6 * o)} Q{f(cx - ex)} {f(y - 4.6 * o)} {f(cx - ex + 4 * o)} {f(y - .6 * o)} "
             f"M{f(cx + ex - 4 * o)} {f(y - .6 * o)} Q{f(cx + ex)} {f(y - 4.6 * o)} {f(cx + ex + 4 * o)} {f(y - .6 * o)}")
    elif ifade == "kararli":
        d = (f"M{f(cx - ex - 4.4 * o)} {f(y - .4 * o)} L{f(cx - ex + 4 * o)} {f(y + 2.6 * o)} "
             f"M{f(cx + ex + 4.4 * o)} {f(y - .4 * o)} L{f(cx + ex - 4 * o)} {f(y + 2.6 * o)}")
    elif ifade == "endiseli":
        d = (f"M{f(cx - ex - 4.2 * o)} {f(y + 2 * o)} L{f(cx - ex + 3.8 * o)} {f(y - 1.2 * o)} "
             f"M{f(cx + ex + 4.2 * o)} {f(y + 2 * o)} L{f(cx + ex - 3.8 * o)} {f(y - 1.2 * o)}")
    elif ifade == "gururlu":
        d = (f"M{f(cx - ex - 4 * o)} {f(y - .2 * o)} Q{f(cx - ex)} {f(y - 3.2 * o)} {f(cx - ex + 4 * o)} {f(y - 1 * o)} "
             f"M{f(cx + ex - 4 * o)} {f(y - 1 * o)} Q{f(cx + ex)} {f(y - 3.2 * o)} {f(cx + ex + 4 * o)} {f(y - .2 * o)}")
    elif ifade == "dusunen":
        d = f"M{f(cx + ex - 4 * o)} {f(y - .8 * o)} Q{f(cx + ex)} {f(y - 4 * o)} {f(cx + ex + 4 * o)} {f(y - 1.4 * o)}"
    return f'<path d="{d}" fill="none" stroke="{CZ}" stroke-width="{f(k)}" stroke-linecap="round"/>' if d else ""


def _agiz(cx, y, o, ifade):
    k = max(1.3, 2.0 * o)
    if ifade in ("gulen", "heyecan"):
        return (f'<path d="M{f(cx - 6 * o)} {f(y - 1.2 * o)} Q{f(cx)} {f(y + 8.4 * o)} {f(cx + 6 * o)} {f(y - 1.2 * o)} Q{f(cx)} {f(y + .8 * o)} {f(cx - 6 * o)} {f(y - 1.2 * o)} Z" '
                f'fill="#A8323E" stroke="{CZ}" stroke-width="{f(k * .8)}" stroke-linejoin="round"/>'
                f'<path d="M{f(cx - 2.8 * o)} {f(y + 3.4 * o)} Q{f(cx)} {f(y + 5.6 * o)} {f(cx + 2.8 * o)} {f(y + 3.4 * o)} Q{f(cx)} {f(y + 2.2 * o)} {f(cx - 2.8 * o)} {f(y + 3.4 * o)} Z" fill="#F08A96"/>')
    if ifade == "sasiran":
        return f'<ellipse cx="{f(cx)}" cy="{f(y + 1.8 * o)}" rx="{f(2.9 * o)}" ry="{f(3.6 * o)}" fill="#A8323E" stroke="{CZ}" stroke-width="{f(k * .8)}"/>'
    if ifade == "sersem":
        return f'<path d="M{f(cx - 5 * o)} {f(y + 1 * o)} q{f(1.7 * o)} {f(-2.4 * o)} {f(3.3 * o)} 0 t{f(3.3 * o)} 0 t{f(3.3 * o)} 0" fill="none" stroke="{CZ}" stroke-width="{f(k)}" stroke-linecap="round"/>'
    if ifade == "dusunen":
        return f'<path d="M{f(cx - 3.6 * o)} {f(y + 1.6 * o)} Q{f(cx)} {f(y + .4 * o)} {f(cx + 4.4 * o)} {f(y - .6 * o)}" fill="none" stroke="{CZ}" stroke-width="{f(k)}" stroke-linecap="round"/>'
    if ifade == "kararli":
        return f'<path d="M{f(cx - 4.6 * o)} {f(y + .4 * o)} Q{f(cx + .4 * o)} {f(y + 3.6 * o)} {f(cx + 5 * o)} {f(y - 1 * o)}" fill="none" stroke="{CZ}" stroke-width="{f(k)}" stroke-linecap="round"/>'
    if ifade == "endiseli":
        return f'<path d="M{f(cx - 4 * o)} {f(y + 2.4 * o)} Q{f(cx)} {f(y - .6 * o)} {f(cx + 4 * o)} {f(y + 2.4 * o)}" fill="none" stroke="{CZ}" stroke-width="{f(k)}" stroke-linecap="round"/>'
    # mutlu, sakin, gururlu
    g = 6.4 if ifade != "sakin" else 4.6
    return f'<path d="M{f(cx - 5.2 * o)} {f(y)} Q{f(cx)} {f(y + g * o)} {f(cx + 5.2 * o)} {f(y)}" fill="none" stroke="{CZ}" stroke-width="{f(k)}" stroke-linecap="round"/>'


def yuz(cx, cy, o=1.0, ifade="mutlu", sklera=False, yanak=True, yon=0.0, aralik=8.6):
    """Yüz: (cx, cy) gözlerin ortası. o ölçek. ifade: mutlu gulen sasiran kararli dusunen sakin sersem gururlu heyecan endiseli."""
    ex = aralik * o
    o_ = []
    if yanak:
        o_.append(f'<ellipse cx="{f(cx - ex - 4.6 * o)}" cy="{f(cy + 5.6 * o)}" rx="{f(3.6 * o)}" ry="{f(2.2 * o)}" fill="{YANAK}" opacity=".6"/>'
                  f'<ellipse cx="{f(cx + ex + 4.6 * o)}" cy="{f(cy + 5.6 * o)}" rx="{f(3.6 * o)}" ry="{f(2.2 * o)}" fill="{YANAK}" opacity=".6"/>')
    o_.append(_goz(cx - ex, cy, o, ifade, sklera, yon) + _goz(cx + ex, cy, o, ifade, sklera, yon))
    o_.append(_kas(cx, cy, o, ifade, ex))
    o_.append(_agiz(cx, cy + 8.2 * o, o, ifade))
    return "".join(o_)


def _kure(s, cx, cy, r, renk, cz=CZ, k=K, parlak=.7):
    g = s.rad([(0, acik(renk, .55)), (.5, renk), (1, koyu(renk, .3))], .36, .3, .78, ad="kr")
    return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}" stroke="{cz}" stroke-width="{f(k)}"/>'
            f'<ellipse cx="{f(cx - r * .38)}" cy="{f(cy - r * .44)}" rx="{f(r * .24)}" ry="{f(r * .13)}" fill="#FFFFFF" opacity="{parlak}" '
            f'transform="rotate(-35 {f(cx - r * .38)} {f(cy - r * .44)})"/>')


def _golge(cx, cy, rx, ry=5):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="#0E2A3A" opacity=".16"/>'


def _rozet(cx, cy, r, isaret, renk):
    """Küçük beyaz yük rozeti: + / − / 2+ (+ ve − çizgi; yazı tipine bağlı değil)."""
    o = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#FFFFFF" stroke="{CZ}" stroke-width="{f(max(1.2, r * .22))}"/>'
    k = max(1.3, r * .3)
    if isaret in ("+", "−"):
        o += f'<path d="M{f(cx - r * .5)} {f(cy)} H{f(cx + r * .5)}" stroke="{renk}" stroke-width="{f(k)}" stroke-linecap="round"/>'
        if isaret == "+":
            o += f'<path d="M{f(cx)} {f(cy - r * .5)} V{f(cy + r * .5)}" stroke="{renk}" stroke-width="{f(k)}" stroke-linecap="round"/>'
    else:   # 2+ : rakam yazı, artı çizgi
        o += (f'<text x="{f(cx - r * .22)}" y="{f(cy + r * .42)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" '
              f'font-size="{f(r * 1.25)}" fill="{renk}">2</text>'
              f'<path d="M{f(cx + r * .2)} {f(cy - r * .28)} H{f(cx + r * .74)} M{f(cx + r * .47)} {f(cy - r * .55)} V{f(cy - r * .01)}" '
              f'stroke="{renk}" stroke-width="{f(k * .8)}" stroke-linecap="round"/>')
    return o


# ------------------------------------------------------------------ atom modelleri (0 0 120 120)

def atomos(s, ifade="dusunen"):
    """Demokritos'un 'atomos'u: bölünemez, küçük, sert tanecik (çakıl taşı)."""
    r = RNG(5)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * 2 * math.pi / 10
        rr = 38 * (1 + r.uniform(-.09, .09))
        pts.append((60 + rr * math.cos(a) * 1.08, 66 + rr * math.sin(a) * .92))
    g = s.rad([(0, "#F3E6C8"), (.55, "#D9C29A"), (1, "#A88C60")], .36, .3, .8, ad="at")
    o = [_golge(60, 108, 34)]
    o.append(f'<path d="{egri_d(pts, True)}" fill="{g}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>')
    for _ in range(9):
        x, y = 60 + r.uniform(-30, 30), 66 + r.uniform(-26, 26)
        if abs(x - 60) < 22 and 52 < y < 86:
            continue
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(1, 2.2))}" fill="#9C8058" opacity=".55"/>')
    o.append(f'<path d="M36 46 Q44 36 56 34" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity=".7"/>')
    o.append(yuz(60, 66, 1.1, ifade))
    return "".join(o)


def dalton(s, ifade="gururlu"):
    """Dalton: içi dolu, bölünemez bilardo topu."""
    o = [_golge(60, 112, 36)]
    g = s.rad([(0, "#B9CFE4"), (.35, "#7C9CBC"), (.8, "#4E6F92"), (1, "#36506E")], .34, .28, .8, ad="dt")
    o.append(f'<circle cx="60" cy="62" r="46" fill="{g}" stroke="{CZ}" stroke-width="{K}"/>')
    o.append('<circle cx="79" cy="36" r="12.5" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
             '<circle cx="79" cy="36" r="8.4" fill="none" stroke="#36506E" stroke-width="1.2" stroke-dasharray="1.6 1.4"/>')
    o.append('<ellipse cx="38" cy="34" rx="11" ry="6" fill="#FFFFFF" opacity=".75" transform="rotate(-38 38 34)"/>'
             '<ellipse cx="30" cy="48" rx="3" ry="2" fill="#FFFFFF" opacity=".6"/>')
    o.append(yuz(56, 70, 1.18, ifade, sklera=True))
    return "".join(o)


def thomson(s, ifade="gulen"):
    """Thomson: (+) hamurlu üzümlü kek; üzümler (−) elektronlar."""
    o = ['<ellipse cx="60" cy="106" rx="50" ry="9" fill="#F3F5F8" stroke="#1B1D26" stroke-width="2.2"/>',
         '<ellipse cx="60" cy="104" rx="38" ry="5" fill="#DCE5EE"/>']
    g = s.rad([(0, "#FFD9C8"), (.5, "#F4A68E"), (1, "#D06F55")], .4, .3, .85, ad="tk")
    o.append(f'<path d="M14 101 C12 66 30 28 60 26 C90 28 108 66 106 101 Q60 110 14 101 Z" fill="{g}" stroke="{CZ}" stroke-width="{K}" stroke-linejoin="round"/>')
    o.append('<path d="M26 54 C34 36 48 30 60 30" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" opacity=".6"/>')
    for x, y in ((40, 56), (78, 52), (86, 74), (30, 76), (52, 98), (74, 99), (62, 40)):
        o.append(f'<path d="M{x - 3} {y} H{x + 3} M{x} {y - 3} V{y + 3}" stroke="#A9402B" stroke-width="2" stroke-linecap="round"/>')
    for x, y in ((48, 42), (74, 40), (28, 62), (94, 60), (22, 88), (98, 88), (38, 96), (86, 98)):
        o.append(f'<circle cx="{x}" cy="{y}" r="5.4" fill="{ELEKTRON}" stroke="#13235E" stroke-width="1.4"/>'
                 f'<path d="M{f(x - 2.6)} {y} H{f(x + 2.6)}" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round"/>')
    o.append(yuz(60, 70, 1.1, ifade))
    return "".join(o)


def rutherford(s, ifade="kararli"):
    """Rutherford: atomun çoğu boşluk; ortada minicik, yoğun, (+) çekirdek (ölçek abartılı)."""
    o = [_golge(60, 114, 30, 4)]
    o.append('<circle cx="60" cy="60" r="52" fill="#EEF6FA" stroke="#8FA6B2" stroke-width="2" stroke-dasharray="5 5"/>')
    for a in (28, -28):
        o.append(f'<ellipse cx="60" cy="60" rx="47" ry="17" fill="none" stroke="#B4C5CE" stroke-width="1.5" transform="rotate({a} 60 60)"/>')
    for a, aci in ((.5, 28), (3.6, 28), (2.2, -28)):
        x, y = 47 * math.cos(a), 17 * math.sin(a)
        t = math.radians(aci)
        px, py = 60 + x * math.cos(t) - y * math.sin(t), 60 + x * math.sin(t) + y * math.cos(t)
        o.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="4.4" fill="{ELEKTRON}" stroke="#13235E" stroke-width="1.2"/>'
                 f'<path d="M{f(px - 2.1)} {f(py)} H{f(px + 2.1)}" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round"/>')
    for a in range(8):          # yoğunluk çizgileri
        t = a * math.pi / 4 + .3
        o.append(f'<path d="M{f(60 + 20 * math.cos(t))} {f(60 + 20 * math.sin(t))} L{f(60 + 25 * math.cos(t))} {f(60 + 25 * math.sin(t))}" stroke="{MER}" stroke-width="2" stroke-linecap="round"/>')
    o.append(_kure(s, 60, 60, 16, PROTON))
    o.append(yuz(60, 60.5, .62, ifade, sklera=True, yanak=False, aralik=8))
    o.append(_rozet(73.5, 46.5, 5.4, "+", MER_K))
    return "".join(o)


def bohr(s, ifade="gururlu"):
    """Bohr: elektronlar belirli enerjili halkalarda (Na: 2 · 8 · 1)."""
    o = [_golge(60, 115, 30, 4)]
    for rr, c in ((24, KOB), (37, GOL), (50, KEH)):
        o.append(f'<circle cx="60" cy="60" r="{rr}" fill="none" stroke="{CZ}" stroke-width="5.2"/>'
                 f'<circle cx="60" cy="60" r="{rr}" fill="none" stroke="{c}" stroke-width="3"/>')
    o.append(_kure(s, 60, 60, 15, PROTON))
    o.append(yuz(60, 60, .6, ifade, sklera=True, yanak=False, aralik=8))
    for rr, n, a0 in ((24, 2, -.4), (37, 8, .2), (50, 1, -2.3)):
        for j in range(n):
            a = a0 + j * 2 * math.pi / n
            x, y = 60 + rr * math.cos(a), 60 + rr * math.sin(a)
            o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="4.3" fill="{ELEKTRON}" stroke="#13235E" stroke-width="1.2"/>')
    return "".join(o)


def bulut(s, ifade="sakin"):
    """Modern model: elektron bulutu (olasılık); burun yerinde minicik çekirdek."""
    r = RNG(9)
    g = s.rad([(0, "#3E6BD6", .95), (.3, "#5C8FE8", .7), (.65, "#8DB6F2", .32), (1, "#A9CBF7", 0)], 60, 60, 56, kull="userSpaceOnUse", ad="bl")
    o = [_golge(60, 114, 28, 4), f'<circle cx="60" cy="60" r="56" fill="{g}"/>']
    o.append('<circle cx="60" cy="60" r="44" fill="none" stroke="#5C86D6" stroke-width="1.4" stroke-dasharray="3 4" opacity=".8"/>')
    for _ in range(190):
        a = r.uniform(0, 2 * math.pi)
        d = abs(r.gauss(0, 21))
        x, y = 60 + d * math.cos(a), 60 + d * math.sin(a)
        if d < 52 and not ((x - 60) ** 2 / 26 ** 2 + (y - 61) ** 2 / 19 ** 2 < 1):
            o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.5" fill="#14296B" opacity=".5"/>')
    o.append('<ellipse cx="60" cy="61" rx="25" ry="18.5" fill="#FFFFFF" opacity=".72"/>')
    o.append(yuz(60, 56, 1.12, ifade))
    o.append(_kure(s, 60, 63.5, 3.4, PROTON, k=1.1, parlak=.5))
    return "".join(o)


def cekirdek_altin(s, ifade="kararli"):
    """Altın çekirdeği (79+): çizgi romanın sert, yoğun, (+) kahramanı. 60×60."""
    o = [_golge(30, 56.5, 14, 2.4), _kure(s, 30, 33, 18, "#E5B43A")]
    o.append(yuz(29.5, 34.5, .72, ifade, sklera=True, yanak=False, aralik=8.2))
    o.append(_rozet(44.5, 16.5, 6.4, "+", "#8A6212"))
    return "".join(o)


# ------------------------------------------------------------------ tanecikler

def tanecik(s, renk, ifade, isaret=None, isaret_renk=MER_K, sklera=True):
    """60×60: gövde (30,33) r 20; sağ üstte yük rozeti."""
    o = [_golge(30, 56.5, 15, 2.6), _kure(s, 30, 33, 20, renk)]
    o.append(yuz(29, 34.5, .78, ifade, sklera=sklera, yanak=not sklera or renk != ELEKTRON, aralik=8.4))
    if isaret:
        o.append(_rozet(45.5, 16, 6.6, isaret, isaret_renk))
    return "".join(o)


def alfa(s, ifade="kararli"):
    """α taneciği: 2 proton + 2 nötron (He çekirdeği, 2+); pilot gözlüklü."""
    o = [_golge(35, 62, 22, 3)]
    for (x, y, c) in ((24, 24, PROTON), (46, 22, NOTRON), (24, 44, NOTRON), (46, 42, PROTON)):
        o.append(_kure(s, x, y, 14, c, parlak=.55))
    # gözlük kayışı + camlar
    o.append(f'<path d="M9 31 Q35 25 62 30" fill="none" stroke="{CZ}" stroke-width="5.6" stroke-linecap="round"/>'
             f'<path d="M9 31 Q35 25 62 30" fill="none" stroke="#7A5232" stroke-width="3.2" stroke-linecap="round"/>')
    for x in (28, 43):
        o.append(f'<circle cx="{x}" cy="31" r="7.2" fill="#E3F4FB" stroke="{CZ}" stroke-width="2"/>')
    o.append(f'<path d="M35.2 30.4 Q35.6 28.6 36 30.4" stroke="{CZ}" stroke-width="2"/>')
    yz = yuz(35.5, 31.5, .6, ifade, sklera=False, yanak=False, aralik=12.6)
    o.append(yz)
    o.append(_rozet(62, 12, 8.4, "2+", MER_K))
    return "".join(o)


def foton(s, renk, ifade="mutlu", uv=False):
    """Foton: dalga kuyruklu ışık paketi (sağa uçar). renk: dalga boyunun rengi."""
    pts = []
    for i in range(0, 53):
        x = 3 + i
        pts.append((x, 25 + 6.5 * math.sin(2 * math.pi * (x - 3) / 16) * min(1, i / 10)))
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    o = [f'<path d="{d}" fill="none" stroke="{CZ}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>',
         f'<path d="{d}" fill="none" stroke="{renk}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>']
    hale = s.rad([(0, renk, .55), (.6, renk, .18), (1, renk, 0)], 68, 25, 24, kull="userSpaceOnUse", ad="fh")
    o.append(f'<circle cx="68" cy="25" r="24" fill="{hale}"/>')
    g = s.rad([(0, "#FFFFFF"), (.32, acik(renk, .35)), (.75, renk), (1, koyu(renk, .25))], .4, .35, .75, ad="fg")
    o.append(f'<circle cx="68" cy="25" r="14" fill="{g}" stroke="{CZ}" stroke-width="2.2"/>')
    if uv:
        o.append(f'<path d="M57 22.5 H79" stroke="{CZ}" stroke-width="1.6"/>'
                 f'<rect x="58.6" y="20.4" width="8.6" height="6.4" rx="2.6" fill="{CZ}"/><rect x="69.4" y="20.4" width="8.6" height="6.4" rx="2.6" fill="{CZ}"/>'
                 f'<path d="M60.4 22.4 l2.4 -.9 M71.2 22.4 l2.4 -.9" stroke="#FFFFFF" stroke-width="1" stroke-linecap="round"/>'
                 + _agiz(68.4, 31, .62, "gulen"))
    else:
        o.append(yuz(68.4, 24.6, .6, ifade, sklera=True, yanak=False, aralik=7.6))
    return "".join(o)


# ------------------------------------------------------------------ genel (sonraki üniteler için)

def su(s, ifade="mutlu"):
    """Su molekülü: O (kırmızı) + 2 H; H–O–H açısı ≈ 104,5°."""
    o = [_golge(50, 80, 26, 3.4)]
    for sgn in (-1, 1):
        a = math.radians(52.25)
        o.append(_kure(s, 50 + sgn * 31 * math.sin(a), 46 - 31 * math.cos(a), 14, ATOM["H"], parlak=.4))
    o.append(_kure(s, 50, 48, 26, ATOM["O"]))
    o.append(yuz(50, 49, .95, ifade, sklera=True, yanak=False))
    return "".join(o)


def iyon(s, eksi=False, ifade="mutlu"):
    """İyon: Na⁺ (küçük, mor) · Cl⁻ (büyük, yeşil). İyon yarıçapı: Cl⁻ > Na⁺."""
    if eksi:
        o = [_golge(32, 61, 20, 2.6), _kure(s, 32, 34, 25, ATOM["Cl"]), yuz(31, 36, .9, ifade, sklera=True, yanak=False),
             _rozet(52, 12, 7.6, "−", "#1F6B3A")]
    else:
        o = [_golge(32, 58, 14, 2.4), _kure(s, 32, 38, 17, ATOM["Na"]), yuz(31.5, 39.5, .66, ifade, sklera=True, yanak=False, aralik=8.6),
             _rozet(47, 20, 6.8, "+", "#5A2F98")]
    return "".join(o)


def atom_genel(s, ifade="mutlu"):
    o = [_golge(40, 75, 22, 3)]
    o.append(f'<ellipse cx="40" cy="42" rx="36" ry="12" fill="none" stroke="{CZ}" stroke-width="4" transform="rotate(-18 40 42)"/>'
             f'<ellipse cx="40" cy="42" rx="36" ry="12" fill="none" stroke="#7FB2F0" stroke-width="2.2" transform="rotate(-18 40 42)"/>')
    o.append(_kure(s, 40, 42, 22, "#5FB4B0"))
    o.append(yuz(39.5, 43, .82, ifade, sklera=True, yanak=False))
    x, y = 40 + 36 * math.cos(.35), 42 + 12 * math.sin(.35)
    t = math.radians(-18)
    px, py = 40 + (x - 40) * math.cos(t) - (y - 42) * math.sin(t), 42 + (x - 40) * math.sin(t) + (y - 42) * math.cos(t)
    o.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="5" fill="{ELEKTRON}" stroke="#13235E" stroke-width="1.3"/>')
    return "".join(o)


# ------------------------------------------------------------------ sembol kütüphanesi

FOTONLAR = (656, 486, 434, 410)


def katalog():
    """(kimlik, viewBox, ad, açıklama) — katalog sayfası ve README için."""
    return [
        ("kk-atomos", "0 0 120 120", "Atomos", "Demokritos’un bölünemez taneciği · MÖ y. 400"),
        ("kk-dalton", "0 0 120 120", "Dalton topu", "içi dolu bilardo topu · 1803–1808"),
        ("kk-thomson", "0 0 120 120", "Üzümlü kek", "(+) hamur, (−) üzümler · 1897 · 1904"),
        ("kk-rutherford", "0 0 120 120", "Minik çekirdek", "çoğu boşluk, yoğun (+) çekirdek · 1911"),
        ("kk-bohr", "0 0 120 120", "Halkalı Bohr", "belirli enerjili katmanlar · 1913"),
        ("kk-bulut", "0 0 120 120", "Elektron bulutu", "olasılık bölgesi · 1920’ler"),
        ("kk-cekirdek", "0 0 60 60", "Altın çekirdeği", "yoğun, (+) · çizgi roman"),
        ("kk-proton", "0 0 60 60", "Proton", "+ yük · çekirdekte"),
        ("kk-notron", "0 0 60 60", "Nötron", "yüksüz · çekirdekte"),
        ("kk-elektron", "0 0 60 60", "Elektron", "− yük · 4 ifade"),
        ("kk-alfa", "0 0 72 66", "α taneciği", "2p + 2n, 2+ · pilot gözlüklü"),
        ("kk-foton-656", "0 0 92 50", "Foton 656 nm", "kırmızı (n = 3 → 2)"),
        ("kk-foton-486", "0 0 92 50", "Foton 486 nm", "camgöbeği (n = 4 → 2)"),
        ("kk-foton-434", "0 0 92 50", "Foton 434 nm", "mavi (n = 5 → 2)"),
        ("kk-foton-410", "0 0 92 50", "Foton 410 nm", "mor (n = 6 → 2)"),
        ("kk-foton-uv", "0 0 92 50", "UV foton", "görünmez · güneş gözlüklü"),
        ("kk-su", "0 0 100 84", "Su molekülü", "H₂O · sonraki üniteler"),
        ("kk-iyon-arti", "0 0 64 64", "Katyon", "Na⁺ · iyon rozeti"),
        ("kk-iyon-eksi", "0 0 64 64", "Anyon", "Cl⁻ · iyon rozeti"),
        ("kk-atom", "0 0 80 80", "Atom", "genel maskot"),
    ]


def semboller():
    s = Svg("kk")
    sy = []

    def ekle(kimlik, vb, icerik):
        sy.append(f'<symbol id="{kimlik}" viewBox="{vb}">{icerik}</symbol>')

    ekle("kk-atomos", "0 0 120 120", atomos(s))
    ekle("kk-dalton", "0 0 120 120", dalton(s))
    ekle("kk-dalton-sasiran", "0 0 120 120", dalton(s, "sasiran"))
    ekle("kk-thomson", "0 0 120 120", thomson(s))
    ekle("kk-thomson-endiseli", "0 0 120 120", thomson(s, "endiseli"))
    ekle("kk-rutherford", "0 0 120 120", rutherford(s))
    ekle("kk-bohr", "0 0 120 120", bohr(s))
    ekle("kk-bulut", "0 0 120 120", bulut(s))
    ekle("kk-cekirdek", "0 0 60 60", cekirdek_altin(s))
    ekle("kk-cekirdek-sasiran", "0 0 60 60", cekirdek_altin(s, "sasiran"))
    ekle("kk-proton", "0 0 60 60", tanecik(s, PROTON, "kararli", "+", MER_K))
    ekle("kk-notron", "0 0 60 60", tanecik(s, NOTRON, "sakin"))
    for ifade in ("mutlu", "heyecan", "sasiran", "sakin", "sersem"):
        ekle("kk-elektron" + ("" if ifade == "mutlu" else "-" + ifade), "0 0 60 60", tanecik(s, ELEKTRON, ifade, "−", "#1B3584"))
    for ifade in ("kararli", "mutlu", "sasiran", "sersem"):
        ekle("kk-alfa" + ("" if ifade == "kararli" else "-" + ifade), "0 0 72 66", alfa(s, "gulen" if ifade == "mutlu" else ifade))
    for nm in FOTONLAR:
        ekle(f"kk-foton-{nm}", "0 0 92 50", foton(s, nm_renk(nm), "gulen" if nm == 656 else "mutlu"))
    ekle("kk-foton-uv", "0 0 92 50", foton(s, UV_RENK, uv=True))
    ekle("kk-su", "0 0 100 84", su(s))
    ekle("kk-iyon-arti", "0 0 64 64", iyon(s, False))
    ekle("kk-iyon-eksi", "0 0 64 64", iyon(s, True))
    ekle("kk-atom", "0 0 80 80", atom_genel(s))
    return s.govde() + "".join(sy)


VIEWBOX = {k: vb for k, vb, *_ in katalog()}


def vb(kimlik):
    """Sembolün viewBox'ı (ifade ekli kimlikler kök kimliğin kutusunu kullanır)."""
    for k in sorted(VIEWBOX, key=len, reverse=True):
        if kimlik == k or kimlik.startswith(k + "-"):
            return VIEWBOX[k]
    return VIEWBOX.get(kimlik, "0 0 120 120")


def kullan(kimlik, x, y, w, h=None, donus=0, ayna=False):
    """SVG içinde karakter: <use> (x, y sol üst; w genişlik; h verilmezse viewBox oranı)."""
    _, _, vw, vh = (float(v) for v in vb(kimlik).split())
    h = h if h is not None else w * vh / vw
    t = []
    if donus:
        t.append(f"rotate({f(donus)} {f(x + w / 2)} {f(y + h / 2)})")
    if ayna:
        t.append(f"translate({f(2 * x + w)} 0) scale(-1 1)")
    tr = f' transform="{" ".join(t)}"' if t else ""
    return f'<use href="#{kimlik}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"{tr}/>'
