"""Atom ve Yapısı · üniteye özel bilgi grafikleri ({{info|ad}}; kur_ortak önek verir: fn(onek, *arg)).

Bütün sayılar (çizgi dalga boyları, tanecik sayıları, enerji düzeyleri) dogrula.py'de denetlenir; burada yalnız çizim
vardır. SVG yazılarında kontur yok; oklar yol (path) olarak çizilir. Baloo ve Nunito'da ⁺ ⁻ yok: üst/alt simgeler
_alt() ve _nk() ile tspan olarak yazılır. viewBox genişliği ≈ basılacak genişlik × 10 (1 birim ≈ 0,1 mm).
"""
import math
import re
from cizim.temel import Svg, f, nok, cizgi_d, karis, acik, koyu, selcuklu_yildizi, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, GOL_AA, DERIN, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A,
                           ERGUVAN, ALTIN, ALTIN_K, ALTIN_A, ZUMRUT, GUM, GUM_K, GUM_A, ATOM)

T = 'font-family="Nunito" font-weight="800"'
T7 = 'font-family="Nunito" font-weight="700"'
B = 'font-family="\'Baloo Bhaijaan 2\'" font-weight="800"'
PROTON, NOTRON, ELEKTRON = "#E2533D", "#9AA8B6", "#2B50B5"

# görünür ışık: dalga boyu (nm) → renk (temsilî, baskıya uygun doygun tonlar)
_NM = [(400, "#6A1FD0"), (420, "#5B2BE0"), (440, "#3D3BE8"), (470, "#1E7BE8"), (490, "#14B8E6"), (510, "#22C47A"), (540, "#6CCB2E"),
       (570, "#E8E02A"), (590, "#FFB21A"), (620, "#FF6A1A"), (660, "#E8282B"), (700, "#B01A1A")]
# dogrula.py ile aynı çizgiler (nm)
CIZGI = {"H": (410, 434, 486, 656), "Na": (589,), "Li": (610, 671)}
LAMBA = (410, 434, 486, 589, 656)


def nm_renk(nm):
    for (a, ca), (b, cb) in zip(_NM, _NM[1:]):
        if a <= nm <= b:
            return karis(ca, cb, (nm - a) / (b - a))
    return _NM[0][1] if nm < 400 else _NM[-1][1]


# ------------------------------------------------------------------ küçük yardımcılar

def _alt(metin, x, y, fs, renk=OBS, anchor="middle", font=B):
    """Yazı içinde _2 → alt simge, ^{…} → üst simge (tspan dy)."""
    parca = re.split(r"(_\d+|_\{[^}]*\}|\^\{[^}]*\})", metin)
    o = [f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(fs)}" fill="{renk}">']
    dy = 0
    for p in parca:
        if not p:
            continue
        if p.startswith("_"):
            ic = p[2:-1] if p.startswith("_{") else p[1:]
            o.append(f'<tspan dy="{f(fs * .24 - dy)}" font-size="{f(fs * .66)}">{ic}</tspan>')
            dy = fs * .24
        elif p.startswith("^"):
            o.append(f'<tspan dy="{f(-fs * .38 - dy)}" font-size="{f(fs * .62)}">{p[2:-1]}</tspan>')
            dy = -fs * .38
        else:
            o.append(f'<tspan dy="{f(-dy)}">{p}</tspan>' if dy else p)
            dy = 0
    o.append("</text>")
    return "".join(o)


def _nk(sembol, x, y, fs, A=None, Z=None, yuk="", renk=OBS, font=B):
    """Çekirdek gösterimi: sembolün solunda üstte A, altta Z (sağa yaslı); sağ üstte yük. x = sembolün sol kenarı."""
    o = []
    if A is not None:
        o.append(f'<text x="{f(x - fs * .06)}" y="{f(y - fs * .42)}" text-anchor="end" {font} font-size="{f(fs * .52)}" fill="{renk}">{A}</text>')
    if Z is not None:
        o.append(f'<text x="{f(x - fs * .06)}" y="{f(y + fs * .14)}" text-anchor="end" {font} font-size="{f(fs * .52)}" fill="{renk}">{Z}</text>')
    y_ = f'<tspan dy="{f(-fs * .4)}" font-size="{f(fs * .58)}">{yuk}</tspan>' if yuk else ""
    o.append(f'<text x="{f(x)}" y="{f(y)}" {font} font-size="{f(fs)}" fill="{renk}">{sembol}{y_}</text>')
    return "".join(o)


def _ok(x0, y0, x1, y1, renk=OBS, k=5, uc=16, kesik=False):
    a = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - uc * math.cos(a - .45), y1 - uc * math.sin(a - .45))
    p2 = (x1 - uc * math.cos(a + .45), y1 - uc * math.sin(a + .45))
    ks = ' stroke-dasharray="9 7"' if kesik else ""
    return (f'<path d="M{f(x0)} {f(y0)} L{f(x1 - uc * .6 * math.cos(a))} {f(y1 - uc * .6 * math.sin(a))}" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"{ks}/>'
            f'<path d="M{f(x1)} {f(y1)} L{nok(p1)} L{nok(p2)} Z" fill="{renk}"/>')


def _kutu(x, y, w, h, renk="#FFFFFF", cz=OBS, r=18, kesik=False, k=3):
    ks = ' stroke-dasharray="10 7"' if kesik else ""
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{renk}" stroke="{cz}" stroke-width="{k}"{ks}/>'


def _kure(s, x, y, r, renk, yazi="", yazi_renk="#FFFFFF", fs=None, cz=None):
    g = s.rad([(0, acik(renk, .55)), (.55, renk), (1, koyu(renk, .35))], .36, .32, .75, ad="kr")
    o = f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{g}" stroke="{cz or koyu(renk, .5)}" stroke-width="{f(max(1, r * .05))}"/>'
    o += f'<ellipse cx="{f(x - r * .35)}" cy="{f(y - r * .4)}" rx="{f(r * .26)}" ry="{f(r * .15)}" fill="#FFFFFF" opacity=".75" transform="rotate(-35 {f(x - r * .35)} {f(y - r * .4)})"/>'
    if yazi:
        fs = fs or r * (.95 if len(yazi) <= 1 else .7)
        o += f'<text x="{f(x)}" y="{f(y + fs * .36)}" text-anchor="middle" {B} font-size="{f(fs)}" fill="{yazi_renk}">{yazi}</text>'
    return o


def _elektron(x, y, r=8, isaret=True):
    o = f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{ELEKTRON}" stroke="#13235E" stroke-width="1.4"/>'
    if isaret:
        o += f'<path d="M{f(x - r * .5)} {f(y)} H{f(x + r * .5)}" stroke="#FFFFFF" stroke-width="{f(max(1.2, r * .22))}" stroke-linecap="round"/>'
    return o


def _dalga(x0, y0, x1, y1, renk, genlik=9, dalga=24, k=4):
    """Işık (foton) dalgası: x0,y0 → x1,y1 boyunca sinüs + uçta ok."""
    L = math.hypot(x1 - x0, y1 - y0)
    a = math.atan2(y1 - y0, x1 - x0)
    n = max(2, int(L / 4))
    pts = []
    for i in range(n + 1):
        t = i / n * (L - 14)
        d = genlik * math.sin(2 * math.pi * t / dalga)
        pts.append((x0 + t * math.cos(a) - d * math.sin(a), y0 + t * math.sin(a) + d * math.cos(a)))
    o = f'<path d="{cizgi_d(pts)}" fill="none" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"/>'
    p1 = (x1 - 16 * math.cos(a - .5), y1 - 16 * math.sin(a - .5))
    p2 = (x1 - 16 * math.cos(a + .5), y1 - 16 * math.sin(a + .5))
    return o + f'<path d="M{f(x1)} {f(y1)} L{nok(p1)} L{nok(p2)} Z" fill="{renk}"/>'


def _t_isaret(x, y, h, renk="#D9C29A", cz="#8E7552"):
    """Küçük T dikilitaşı (zaman şeridi kilometre taşı)."""
    w, bw, bh = h * .26, h * .7, h * .22
    return (f'<path d="M{f(x - w / 2)} {f(y)} L{f(x - w * .44)} {f(y - h + bh)} H{f(x + w * .44)} L{f(x + w / 2)} {f(y)} Z" fill="{renk}" stroke="{cz}" stroke-width="2"/>'
            f'<rect x="{f(x - bw / 2)}" y="{f(y - h)}" width="{f(bw)}" height="{f(bh)}" rx="3" fill="{acik(renk, .2)}" stroke="{cz}" stroke-width="2"/>')


# ------------------------------------------------------------------ 1. DURAK · beş model, beş deney (zaman şeridi)

def model_yolculugu(onek="ay-my"):
    s = Svg(onek)
    W, H = 1820, 408
    r = RNG(3)
    # zemin: Göbeklitepe bozkırı + yol
    g = s.lin([(0, "#FFF8E8"), (1, "#F6E7BF")], 0, 0, 0, H, kull="userSpaceOnUse", ad="zm")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{g}"/>'
    yol = f"M0 296 C300 280 520 312 900 296 S1500 280 1820 298"
    s += f'<path d="{yol}" fill="none" stroke="#C9A25E" stroke-width="30" stroke-linecap="round"/>'
    s += f'<path d="{yol}" fill="none" stroke="#FFF1CF" stroke-width="3.5" stroke-dasharray="16 12"/>'
    x0 = 182
    adim = 364
    modeller = [
        ("Dalton", "1803–1808", "içi dolu küre", "kütlenin korunumu", "bu durak", "eksik: elektron, iyon, izotop"),
        ("Thomson", "1897 · 1904", "üzümlü kek", "katot ışınları", "bu durak", "eksik: çekirdek, boşluk"),
        ("Rutherford", "1911", "çekirdek + boşluk", "altın levha deneyi", "2. durak", "eksik: elektronların düzeni"),
        ("Bohr", "1913", "enerji katmanları", "H’nin çizgi spektrumu", "2.–3. durak", "eksik: çok elektronlu atomlar"),
        ("Modern", "1926 →", "elektron bulutu", "elektronun dalga davranışı", "2.–3. durak", "bugünkü model"),
    ]
    for i, (ad, yil, bicim, kanit, etiket, eksik) in enumerate(modeller):
        x = x0 + i * adim
        cy = 128
        # etiket çipi
        renk = KEH if etiket == "bu durak" else GOL
        s += f'<rect x="{f(x - 70)}" y="8" width="140" height="30" rx="15" fill="{acik(renk, .75)}" stroke="{koyu(renk, .3)}" stroke-width="2"/>'
        s += f'<text x="{f(x)}" y="30" text-anchor="middle" {T} font-size="19" fill="{koyu(renk, .45)}">{etiket.upper()}</text>'
        s += f'<circle cx="{f(x)}" cy="{cy}" r="86" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
        if i == 0:      # Dalton: içi dolu, bölünemez küre
            s += _kure(s, x, cy, 64, "#7E9AB0")
        elif i == 1:    # Thomson: (+) hamur içinde (−) elektronlar
            s += _kure(s, x, cy, 68, "#F2A28C", cz="#B5523E")
            for k, (dx, dy) in enumerate(((-30, -28), (14, -40), (38, -6), (-42, 10), (-8, 4), (22, 32), (-22, 42), (48, 30), (8, -12))):
                s += _elektron(x + dx, cy + dy, 9)
            for dx, dy in ((-14, -48), (32, -26), (-34, 30), (2, 30), (40, 12), (-50, -12)):
                s += f'<text x="{f(x + dx)}" y="{f(cy + dy + 6)}" text-anchor="middle" {B} font-size="20" fill="#9A3A28">+</text>'
        elif i == 2:    # Rutherford: küçük (+) çekirdek, büyük boşluk, dolaşan elektronlar
            s += f'<circle cx="{f(x)}" cy="{cy}" r="70" fill="#EEF6FA" stroke="#9FB2BC" stroke-width="2" stroke-dasharray="6 6"/>'
            for a in (25, -35):
                s += f'<ellipse cx="{f(x)}" cy="{cy}" rx="66" ry="24" fill="none" stroke="#9FB2BC" stroke-width="2" transform="rotate({a} {f(x)} {cy})"/>'
            s += _kure(s, x, cy, 11, PROTON)
            s += f'<text x="{f(x)}" y="{cy + 6}" text-anchor="middle" {B} font-size="15" fill="#FFFFFF">+</text>'
            for a, rr in ((.4, 66), (2.6, 60), (4.4, 64)):
                s += _elektron(x + rr * math.cos(a), cy + rr * .45 * math.sin(a), 8)
        elif i == 3:    # Bohr: belirli yarıçaplı katmanlar
            for k, rr in enumerate((28, 50, 72)):
                s += f'<circle cx="{f(x)}" cy="{cy}" r="{rr}" fill="none" stroke="{[KOB, GOL, KEH][k]}" stroke-width="3"/>'
            s += _kure(s, x, cy, 12, PROTON)
            for rr, n in ((28, 2), (50, 4), (72, 1)):
                for j in range(n):
                    a = -math.pi / 2 + j * 2 * math.pi / n + rr * .01
                    s += _elektron(x + rr * math.cos(a), cy + rr * math.sin(a), 7, isaret=False)
        else:           # modern: olasılık bulutu
            gb = s.rad([(0, "#5C8FE8", .85), (.45, "#7FB2F0", .45), (1, "#7FB2F0", 0)], x, cy, 78, kull="userSpaceOnUse", ad="bl")
            s += f'<circle cx="{f(x)}" cy="{cy}" r="78" fill="{gb}"/>'
            for k in range(140):
                a = r.uniform(0, 2 * math.pi)
                d = abs(r.gauss(0, 30))
                if d < 74:
                    s += f'<circle cx="{f(x + d * math.cos(a))}" cy="{f(cy + d * math.sin(a))}" r="1.8" fill="#1B3584" opacity=".55"/>'
            s += _kure(s, x, cy, 9, PROTON)
        s += f'<text x="{f(x)}" y="{cy + 106}" text-anchor="middle" {T} font-size="21" fill="{GUM_K}">{bicim}</text>'
        s += f'<rect x="{f(x - 78)}" y="250" width="156" height="38" rx="10" fill="#FFF8E6" stroke="#8E7552" stroke-width="2.4"/>'
        s += f'<text x="{f(x)}" y="278" text-anchor="middle" {B} font-size="25" fill="#5A4220">{yil}</text>'
        s += f'<text x="{f(x)}" y="336" text-anchor="middle" {B} font-size="33" fill="{OBS}">{ad}</text>'
        s += f'<text x="{f(x)}" y="366" text-anchor="middle" {T7} font-size="21" fill="{KOB_K}">kanıt: {kanit}</text>'
        s += f'<text x="{f(x)}" y="394" text-anchor="middle" {T7} font-size="21" fill="{MER_K if i < 4 else ZUMRUT}">{eksik}</text>'
        if i < 4:
            s += _t_isaret(x + adim / 2, 304, 44)
        if i < 4:
            s += _ok(x + 96, cy, x + adim - 96, cy, "#C9A25E", 5, 18)
    return s.cikti(f"0 0 {W} {H}", cls="info yolculuk")


# ------------------------------------------------------------------ 2. DURAK · altın levha deneyi

def altin_levha(onek="ay-al"):
    s = Svg(onek)
    W, H = 1150, 440
    s += _kutu(0, 0, 640, H, "#F7FAFC", "#9FB2BC", 20, k=2)
    s += _kutu(660, 0, 490, H, "#FFFDF4", "#C9A25E", 20, k=2)
    s += f'<text x="320" y="38" text-anchor="middle" {B} font-size="30" fill="{GOL_K}">Düzenek (1909)</text>'
    s += f'<text x="905" y="38" text-anchor="middle" {B} font-size="30" fill="{ALTIN_K}">Yakından bakınca</text>'
    cx, cy = 360, 238
    # ekran (çinko sülfür kaplı, ışıldayan halka)
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="230" ry="160" fill="none" stroke="#7FD0A0" stroke-width="14" opacity=".9"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="230" ry="160" fill="none" stroke="#2F8F5E" stroke-width="2"/>'
    # kaynak: kurşun kutu
    s += f'<rect x="30" y="{cy - 46}" width="104" height="92" rx="8" fill="#5E6672" stroke="{OBS}" stroke-width="3"/>'
    s += f'<rect x="96" y="{cy - 9}" width="40" height="18" fill="#2A2E36"/>'
    s += f'<circle cx="76" cy="{cy}" r="16" fill="{MER}" stroke="{OBS}" stroke-width="2"/>'
    # demet
    s += f'<path d="M136 {cy} H{cx - 8}" stroke="{MER}" stroke-width="10" opacity=".35"/>'
    for k in range(6):
        s += f'<circle cx="{150 + k * 30}" cy="{cy}" r="5" fill="{MER}"/>'
    # levha
    gl = s.lin([(0, "#FFF0B0"), (.5, ALTIN), (1, ALTIN_K)], cx - 6, 0, cx + 6, 0, kull="userSpaceOnUse", ad="lv")
    s += f'<rect x="{cx - 5}" y="{cy - 92}" width="10" height="184" fill="{gl}" stroke="{ALTIN_K}" stroke-width="1.5"/>'
    # yollar: çoğu düz, birkaçı sapar, biri geri döner
    for dy in (-30, -12, 0, 12, 30):
        s += f'<path d="M{cx + 6} {cy + dy * .3} L{cx + 226} {cy + dy}" stroke="{MER}" stroke-width="2.6" opacity=".75"/>'
        s += f'<circle cx="{cx + 228}" cy="{cy + dy}" r="6" fill="#E6FFE0" stroke="#2F8F5E" stroke-width="2"/>'
    for (ex, ey) in ((cx + 170, cy - 120), (cx + 160, cy + 128)):
        s += f'<path d="M{cx + 6} {cy} L{ex} {ey}" stroke="{MER}" stroke-width="2.6" opacity=".75"/>'
        s += f'<circle cx="{ex}" cy="{ey}" r="6" fill="#E6FFE0" stroke="#2F8F5E" stroke-width="2"/>'
    s += f'<path d="M{cx - 6} {cy - 4} L{cx - 150} {cy - 118}" stroke="{MER}" stroke-width="2.6" stroke-dasharray="7 5"/>'
    s += f'<circle cx="{cx - 152}" cy="{cy - 120}" r="6" fill="#E6FFE0" stroke="#2F8F5E" stroke-width="2"/>'
    s += f'<text x="82" y="{cy + 84}" text-anchor="middle" {T} font-size="26" fill="{OBS}">α kaynağı</text>'
    s += f'<text x="{cx}" y="{cy + 126}" text-anchor="middle" {T} font-size="26" fill="{ALTIN_K}">ince altın levha</text>'
    s += f'<text x="{cx + 120}" y="{cy + 192}" text-anchor="middle" {T} font-size="26" fill="#2F8F5E">ışıldayan ekran</text>'
    # yakından: altın atomları (büyük boşluk, minik çekirdek)
    ax0 = 700
    cek = [(ax0 + 110, 140), (ax0 + 300, 170), (ax0 + 140, 320), (ax0 + 340, 340)]
    for (x, y) in cek:
        s += f'<circle cx="{x}" cy="{y}" r="74" fill="#FFF6D6" stroke="#D9B45A" stroke-width="2" stroke-dasharray="6 6"/>'
        s += _kure(s, x, y, 8, ALTIN)
    # α yolları
    s += _ok(ax0 - 20, 236, ax0 + 450, 236, MER, 3.4, 15)                       # boşluktan düz
    s += _ok(ax0 - 20, 92, ax0 + 450, 92, MER, 3.4, 15)
    yol = f"M{ax0 - 20} 168 L{ax0 + 250} 168 Q{ax0 + 290} 168 {ax0 + 330} 140 L{ax0 + 440} 64"
    s += f'<path d="{yol}" fill="none" stroke="{MER}" stroke-width="3.4"/>' + _ok(ax0 + 420, 78, ax0 + 446, 60, MER, 3.4, 15)
    s += f'<path d="M{ax0 - 20} 340 L{ax0 + 322} 340" stroke="{MER}" stroke-width="3.4"/>' + _ok(ax0 + 322, 352, ax0 + 20, 380, MER, 3.4, 15)
    s += f'<text x="{ax0 + 230}" y="226" text-anchor="middle" {T} font-size="26" fill="{OBS}">çoğu düz geçer</text>'
    s += f'<text x="{ax0 + 400}" y="128" text-anchor="middle" {T} font-size="26" fill="{OBS}">azı sapar</text>'
    s += f'<text x="{ax0 + 200}" y="420" text-anchor="middle" {T} font-size="26" fill="{MER_K}">çok azı geri döner</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info altinlevha")


# ------------------------------------------------------------------ 2. DURAK · kümbetin halkaları ↔ Bohr katmanları

def bohr_kumbet(onek="ay-bk"):
    s = Svg(onek)
    W, H = 800, 440
    # sol: kümbet kesiti, kerpiç halkaları
    x0, yb, w, h = 40, 390, 280, 330
    d = f"M{x0} {yb} C{x0} {yb - h * .6} {x0 + w * .3} {yb - h} {x0 + w / 2} {yb - h} C{x0 + w * .7} {yb - h} {x0 + w} {yb - h * .6} {x0 + w} {yb} Z"
    g = s.lin([(0, "#F3C995"), (1, "#C98A4E")], x0, 0, x0 + w, 0, kull="userSpaceOnUse", ad="kb")
    s += f'<path d="{d}" fill="{g}" stroke="#8E5730" stroke-width="3"/>'
    for k, c in enumerate((KOB, GOL, KEH)):
        yy = yb - 60 - k * 92
        s += f'<path d="M{x0 + 10 + k * 28} {yy} Q{x0 + w / 2} {yy - 26} {x0 + w - 10 - k * 28} {yy}" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
    for k in range(9):
        yy = yb - 20 - k * 34
        s += f'<path d="M{x0 + 6} {yy} H{x0 + w - 6}" stroke="#8E5730" stroke-width="1.6" opacity=".35"/>'
    s += f'<text x="{x0 + w / 2}" y="{yb + 34}" text-anchor="middle" {T} font-size="28" fill="#8E5730">kümbet: halka halka kerpiç</text>'
    s += _ok(330, 220, 380, 220, GUM_K, 4, 15)
    # sağ: Bohr modeli · Na (2 · 8 · 1)
    cx, cy = 600, 214
    for k, (rr, c) in enumerate(((60, KOB), (112, GOL), (164, KEH))):
        s += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{c}" stroke-width="5"/>'
    s += _kure(s, cx, cy, 30, PROTON, "11+", fs=22)
    for rr, n, a0 in ((60, 2, 0), (112, 8, .2), (164, 1, -.9)):
        for j in range(n):
            a = a0 + j * 2 * math.pi / n
            s += _elektron(cx + rr * math.cos(a), cy + rr * math.sin(a), 10)
    s += _nk("Na", 446, 424, 36, Z=11, renk=OBS)
    s += f'<text x="508" y="424" {T} font-size="26" fill="{OBS}">K 2 · L 8 · M 1</text>'
    for rr, ad, c in ((60, "K", KOB), (112, "L", GOL_K), (164, "M", KEH_K)):
        s += f'<text x="{cx + rr * .7 + 6}" y="{cy - rr * .7 - 6}" {B} font-size="28" fill="{c}">{ad}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info bohr")


# ------------------------------------------------------------------ 3. DURAK · enerji düzeyleri ve çizgi spektrumu

def _nm_x(nm, x0, x1):
    return x0 + (nm - 400) / 300 * (x1 - x0)


def spektrum(onek="ay-sp"):
    s = Svg(onek)
    W, H = 1150, 440
    s += _kutu(0, 0, 470, H, "#F7F8FF", "#AFB9E0", 20, k=2)
    # enerji düzeyleri
    duz = {1: 392, 2: 236, 3: 164, 4: 124}
    for n, y in duz.items():
        s += f'<path d="M96 {y} H452" stroke="{OBS}" stroke-width="3"/>'
        s += f'<text x="86" y="{y + 8}" text-anchor="end" {T} font-size="23" fill="{OBS}">n = {n}</text>'
    s += f'<text x="235" y="40" text-anchor="middle" {B} font-size="28" fill="{KOB_K}">Enerji düzeyleri</text>'
    s += _ok(30, 392, 30, 96, GUM_K, 3, 13)
    s += f'<text x="40" y="92" {T7} font-size="19" fill="{GUM_K}">enerji</text>'
    # soğurma (yukarı), yayma (aşağı)
    s += _ok(150, duz[1] - 4, 150, duz[3] + 8, GUM_K, 4.5, 16, kesik=True)
    s += _elektron(150, duz[1], 10)
    s += f'<text x="162" y="{duz[1] - 40}" {T} font-size="19" fill="{GUM_K}">enerji soğurur</text>'
    s += _ok(270, duz[3] + 2, 270, duz[2] - 6, MER, 5, 16)
    s += _dalga(280, duz[2] - 34, 360, duz[2] - 76, nm_renk(656), 7, 18, 3.5)
    s += _ok(330, duz[4] + 2, 330, duz[2] - 6, GOL_K, 5, 16)
    s += _dalga(340, duz[2] - 10, 440, duz[2] - 40, nm_renk(486), 7, 14, 3.5)
    s += f'<text x="300" y="{duz[2] + 40}" text-anchor="middle" {T} font-size="20" fill="{MER_K}">inerken ışık yayar</text>'
    # sağ: sürekli ve çizgi spektrumu
    xa, xb = 540, 1120
    s += f'<text x="{(xa + xb) / 2}" y="40" text-anchor="middle" {B} font-size="28" fill="{OBS}">Işığı prizmadan geçir</text>'
    gr = s.lin([(min(1, max(0, (nm - 400) / 300)), c) for nm, c in _NM], xa, 0, xb, 0, kull="userSpaceOnUse", ad="gk")
    s += f'<text x="{xa}" y="84" {T} font-size="21" fill="{OBS}">Güneş ışığı · sürekli spektrum</text>'
    s += f'<rect x="{xa}" y="94" width="{xb - xa}" height="58" rx="6" fill="{gr}" stroke="{OBS}" stroke-width="2"/>'
    s += f'<text x="{xa}" y="214" {T} font-size="21" fill="{OBS}">Hidrojen · çizgi spektrumu</text>'
    s += f'<rect x="{xa}" y="224" width="{xb - xa}" height="58" rx="6" fill="#14142E" stroke="{OBS}" stroke-width="2"/>'
    for nm in CIZGI["H"]:
        x = _nm_x(nm, xa, xb)
        s += f'<rect x="{f(x - 4)}" y="226" width="8" height="54" fill="{nm_renk(nm)}"/>'
        s += f'<text x="{f(x)}" y="306" text-anchor="middle" {T} font-size="20" fill="{OBS}">{nm}</text>'
    for nm in (400, 500, 600, 700):
        x = _nm_x(nm, xa, xb)
        s += f'<path d="M{f(x)} 156 v10" stroke="{OBS}" stroke-width="2"/><text x="{f(x)}" y="186" text-anchor="middle" {T7} font-size="17" fill="{GUM_K}">{nm}</text>'
    s += f'<text x="{xb + 6}" y="186" {T7} font-size="17" fill="{GUM_K}">nm</text>'
    s += f'<text x="{(xa + xb) / 2}" y="352" text-anchor="middle" {T} font-size="21" fill="{KOB_K}">Her çizgi, iki düzey arasındaki bir sıçrama.</text>'
    s += f'<text x="{(xa + xb) / 2}" y="384" text-anchor="middle" {T} font-size="21" fill="{KOB_K}">Çizgiler her elementte farklı: atomun parmak izi.</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info spektrum", oz='data-tema-sabit=""')


def lamba_spektrumu(onek="ay-ls"):
    s = Svg(onek)
    W, H = 720, 330
    xa, xb = 130, 700
    satir = [("H", CIZGI["H"]), ("Na", CIZGI["Na"]), ("Li", CIZGI["Li"]), ("Lamba", LAMBA)]
    for i, (ad, cz) in enumerate(satir):
        y = 12 + i * 70
        vurgu = ad == "Lamba"
        s += f'<text x="{xa - 12}" y="{y + 38}" text-anchor="end" {B} font-size="{26 if not vurgu else 25}" fill="{MER_K if vurgu else OBS}">{ad}</text>'
        s += f'<rect x="{xa}" y="{y}" width="{xb - xa}" height="52" rx="6" fill="#14142E" stroke="{MER if vurgu else OBS}" stroke-width="{4 if vurgu else 2}"/>'
        for nm in cz:
            x = _nm_x(nm, xa, xb)
            s += f'<rect x="{f(x - 4)}" y="{y + 3}" width="8" height="46" fill="{nm_renk(nm)}"/>'
    for nm in (400, 450, 500, 550, 600, 650, 700):
        x = _nm_x(nm, xa, xb)
        s += f'<path d="M{f(x)} 292 v10" stroke="{OBS}" stroke-width="2"/><text x="{f(x)}" y="326" text-anchor="middle" {T7} font-size="19" fill="{GUM_K}">{nm}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info lamba", oz='data-tema-sabit=""')


# ------------------------------------------------------------------ 3. DURAK · orbital biçimleri

def _lob(s, x, y, rx, ry, aci, renk):
    g = s.rad([(0, acik(renk, .55)), (.6, renk), (1, koyu(renk, .3))], .4, .35, .7, ad="lb")
    return f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{g}" stroke="{koyu(renk, .45)}" stroke-width="2" transform="rotate({f(aci)} {f(x)} {f(y)})" opacity=".92"/>'


def _eksen(x, y, L=78):
    return (f'<path d="M{x - L} {y} H{x + L} M{x} {y + L} V{y - L} M{x - L * .62} {y + L * .62} L{x + L * .62} {y - L * .62}" stroke="#A9B4BC" stroke-width="2" stroke-dasharray="5 5"/>'
            f'<text x="{x + L + 4}" y="{y + 7}" {T7} font-size="17" fill="{GUM_K}">x</text>'
            f'<text x="{x + 5}" y="{y - L - 4}" {T7} font-size="17" fill="{GUM_K}">y</text>'
            f'<text x="{f(x + L * .62 + 4)}" y="{f(y - L * .62 - 2)}" {T7} font-size="17" fill="{GUM_K}">z</text>')


def orbital_sekilleri(onek="ay-ob"):
    s = Svg(onek)
    W, H = 1000, 300
    cy = 120
    xs = [100, 300, 480, 660, 870]
    s += _eksen(xs[0], cy)
    gs = s.rad([(0, acik(GOL, .6)), (.6, GOL), (1, GOL_K)], .4, .35, .7, ad="sg")
    s += f'<circle cx="{xs[0]}" cy="{cy}" r="58" fill="{gs}" stroke="{GOL_K}" stroke-width="2" opacity=".92"/>'
    for i, aci in enumerate((0, 90, -45)):
        x = xs[1 + i]
        s += _eksen(x, cy)
        dx, dy = 40 * math.cos(math.radians(aci)), 40 * math.sin(math.radians(aci))
        s += _lob(s, x + dx, cy + dy, 40, 22, aci, MER) + _lob(s, x - dx, cy - dy, 40, 22, aci, MER)
        s += f'<circle cx="{x}" cy="{cy}" r="3.5" fill="{OBS}"/>'
    x = xs[4]
    s += _eksen(x, cy)
    for a in (45, 135, 225, 315):
        dx, dy = 40 * math.cos(math.radians(a)), 40 * math.sin(math.radians(a))
        s += _lob(s, x + dx, cy + dy, 36, 18, a, ERGUVAN)
    s += f'<circle cx="{x}" cy="{cy}" r="3.5" fill="{OBS}"/>'
    s += f'<text x="{xs[0]}" y="236" text-anchor="middle" {B} font-size="30" fill="{GOL_K}">s</text>'
    s += f'<text x="{xs[0]}" y="268" text-anchor="middle" {T} font-size="19" fill="{OBS}">küre · 1 orbital</text>'
    for i, alt in enumerate(("x", "y", "z")):
        s += _alt(f"p_{{{alt}}}", xs[1 + i], 236, 30, MER_K)
    s += f'<text x="{xs[2]}" y="268" text-anchor="middle" {T} font-size="19" fill="{OBS}">iki loplu · eş enerjili 3 orbital</text>'
    s += f'<text x="{xs[4]}" y="236" text-anchor="middle" {B} font-size="30" fill="{ERGUVAN}">d</text>'
    s += f'<text x="{xs[4]}" y="268" text-anchor="middle" {T} font-size="19" fill="{OBS}">5 orbitalden biri</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info orbital")


# ------------------------------------------------------------------ 4. DURAK · iyon oluşumu (Na → Na⁺, Cl → Cl⁻)

def iyon_olusumu(onek="ay-io"):
    s = Svg(onek)
    W, H = 1000, 400
    satir = [  # (atom, iyon, r_atom, r_iyon, renk, p, e_atom, e_iyon, eylem, not)
        ("Na", "+", 70, 38, ATOM["Na"], 11, 11, 10, "1 e⁻ verir", "katyon: küçülür"),
        ("Cl", "−", 37, 68, ATOM["Cl"], 17, 17, 18, "1 e⁻ alır", "anyon: büyür"),
    ]
    for i, (el, yk, ra, ri, renk, p, ea, ei, eylem, notu) in enumerate(satir):
        y = 96 + i * 190
        s += _kure(s, 150, y, ra, renk, el, fs=min(34, ra * .8))
        s += _alt(f"{p} p · {ea} e^{{−}}", 150, y + 92, 23, OBS, font=T)
        s += _ok(250, y, 430, y, GUM_K, 5, 18)
        s += _alt(eylem.replace("e⁻", "e^{−}"), 340, y - 18, 22, MER_K if i == 0 else GOL_K, font=T)
        if i == 0:
            s += _elektron(340, y + 26, 10)
            s += _ok(352, y + 26, 400, y + 46, ELEKTRON, 3, 12)
        else:
            s += _elektron(300, y + 30, 10)
            s += _ok(312, y + 34, 360, y + 14, ELEKTRON, 3, 12)
        s += _kure(s, 560, y, ri, renk, el, fs=min(34, ri * .8))
        s += f'<circle cx="{560 + ri * .75}" cy="{y - ri * .75}" r="17" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
        s += f'<text x="{560 + ri * .75}" y="{y - ri * .75 + 9}" text-anchor="middle" {B} font-size="26" fill="{OBS}">{yk}</text>'
        s += _alt(f"{p} p · {ei} e^{{−}}", 560, y + 92, 23, OBS, font=T)
        s += _kutu(690, y - 46, 300, 92, MER_A if i == 0 else GOL_AA, MER_K if i == 0 else GOL_K, 16, k=2.4)
        s += f'<text x="840" y="{y - 6}" text-anchor="middle" {B} font-size="27" fill="{MER_K if i == 0 else GOL_K}">{notu}</text>'
        s += f'<text x="840" y="{y + 28}" text-anchor="middle" {T} font-size="20" fill="{OBS}">proton sayısı aynı: {p}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info iyon")


# ------------------------------------------------------------------ 4. DURAK · izotop, izoton, izobar, izoelektronik

def izo_kutulari(onek="ay-iz"):
    s = Svg(onek)
    W, H = 1000, 470
    kutu = [
        ("İzotop", "aynı proton sayısı (Z)", KOB, [("C", 12, 6), ("C", 14, 6)], "n: 6 ve 8"),
        ("İzoton", "aynı nötron sayısı", GOL_K, [("C", 14, 6), ("O", 16, 8)], "n: 8 ve 8"),
        ("İzobar", "aynı kütle numarası (A)", KEH_K, [("Ar", 40, 18), ("Ca", 40, 20)], "Z: 18 ve 20"),
        ("İzoelektronik", "aynı e⁻ sayısı ve dizilim", MER_K, [("O", None, 8, "2−"), ("Na", None, 11, "+"), ("Ne", None, 10, "")], "hepsi 10 e⁻"),
    ]
    for i, (ad, ayni, renk, ornek, alt) in enumerate(kutu):
        x = (i % 2) * 505
        y = (i // 2) * 240
        s += _kutu(x + 2, y + 2, 491, 226, "#FFFFFF", renk, 18, k=3)
        s += f'<path d="M{x + 2} {y + 54} H{x + 493}" stroke="{renk}" stroke-width="2"/>'
        s += f'<text x="{x + 22}" y="{y + 40}" {B} font-size="31" fill="{renk}">{ad}</text>'
        s += _alt(ayni.replace("e⁻", "e^{−}"), x + 476, y + 38, 20, OBS, anchor="end", font=T)
        n = len(ornek)
        for j, o in enumerate(ornek):
            el, A, Z = o[0], o[1], o[2]
            yk = o[3] if len(o) > 3 else ""
            cx = x + (120 + j * 220 if n == 2 else 82 + j * 150)
            s += _nk(el, cx, y + 150, 58 if n == 2 else 52, A=A, Z=Z, yuk=yk, renk=OBS)
        s += _alt(alt.replace("e⁻", "e^{−}"), x + 246, y + 208, 22, renk, font=T)
    return s.cikti(f"0 0 {W} {H}", cls="info izokutu")


# ------------------------------------------------------------------ 5. DURAK · Aufbau köşegen kuralı

AUFBAU_SIRA = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d", "5p", "6s", "4f", "5d", "6p", "7s"]


def aufbau(onek="ay-au"):
    s = Svg(onek)
    W, H = 640, 560
    tur = "spdf"
    renk = {"s": GOL, "p": MER, "d": ERGUVAN, "f": KEH}
    var = {1: "s", 2: "sp", 3: "spd", 4: "spdf", 5: "spdf", 6: "spd", 7: "sp"}
    bx, by, gx, gy, bw, bh = 40, 18, 140, 62, 108, 46

    def merkez(n, l):
        return bx + l * gx + bw / 2, by + (n - 1) * gy + bh / 2

    for n in range(1, 8):
        for l, t in enumerate(tur):
            if t not in var[n]:
                continue
            x, y = bx + l * gx, by + (n - 1) * gy
            s += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="{acik(renk[t], .8)}" stroke="{koyu(renk[t], .35)}" stroke-width="2.4"/>'
    yazilar = []
    for n in range(1, 8):
        for l, t in enumerate(tur):
            if t in var[n]:
                x, y = bx + l * gx, by + (n - 1) * gy
                yazilar.append(f'<rect x="{x + bw / 2 - 27}" y="{y + 8}" width="54" height="31" rx="9" fill="#FFFFFF" opacity=".92"/>'
                               f'<text x="{x + bw / 2}" y="{y + 33}" text-anchor="middle" {B} font-size="29" fill="{koyu(renk[t], .5)}">{n}{t}</text>')
    # köşegen oklar (kutuların üstünde, ince; uçları kutuların dışında)
    gruplar = [["1s"], ["2s"], ["2p", "3s"], ["3p", "4s"], ["3d", "4p", "5s"], ["4d", "5p", "6s"], ["4f", "5d", "6p", "7s"], ["5f", "6d", "7p"]]
    for gr in gruplar:
        n0, l0 = int(gr[0][0]), tur.index(gr[0][1])
        n1, l1 = int(gr[-1][0]), tur.index(gr[-1][1])
        x0, y0 = merkez(n0, l0)
        x1, y1 = merkez(n1, l1)
        a = math.atan2(y1 - y0, x1 - x0) if len(gr) > 1 else math.atan2(gy, -gx)
        x0, y0 = x0 - 66 * math.cos(a), y0 - 66 * math.sin(a)
        x1, y1 = x1 + 70 * math.cos(a), y1 + 70 * math.sin(a)
        s += _ok(x0, y0, x1, y1, "#46525C", 3.2, 15)
    s += "".join(yazilar)
    s += f'<text x="{W - 10}" y="{H - 82}" text-anchor="end" {T} font-size="20" fill="{GUM_K}">okları yukarıdan aşağı izle</text>'
    return s.cikti(f"0 0 {W} {H - 60}", cls="info aufbau")


# ------------------------------------------------------------------ KISSA 3 · tanecik grafiği (p, n, e)

KISSA_TANECIK = {"K": (9, 10, 10), "L": (11, 12, 10), "M": (10, 10, 10), "R": (12, 12, 10)}


def kissa_grafik(onek="ay-kg"):
    s = Svg(onek)
    W, H = 420, 330
    x0, y0, x1, y1 = 56, 30, 410, 280      # eksen kutusu
    ymax = 14

    def Y(v):
        return y1 - v / ymax * (y1 - y0)
    s += f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    for v in range(0, ymax + 1, 2):
        s += f'<path d="M{x0} {f(Y(v))} H{x1}" stroke="#DCE4E8" stroke-width="1.6"/>'
        if v % 4 == 0:
            s += f'<text x="{x0 - 8}" y="{f(Y(v) + 8)}" text-anchor="end" {T} font-size="24" fill="{GUM_K}">{v}</text>'
    s += f'<path d="M{x0} {y0 - 6} V{y1} H{x1}" fill="none" stroke="{OBS}" stroke-width="2.4"/>'
    renk = (PROTON, NOTRON, ELEKTRON)
    gw = (x1 - x0) / 4
    for i, (ad, deg) in enumerate(KISSA_TANECIK.items()):
        gx = x0 + i * gw + 12
        for j, v in enumerate(deg):
            bx = gx + j * 22
            s += f'<rect x="{f(bx)}" y="{f(Y(v))}" width="20" height="{f(y1 - Y(v))}" fill="{renk[j]}" stroke="{OBS}" stroke-width="1.2"/>'
        s += f'<text x="{f(gx + 32)}" y="{y1 + 30}" text-anchor="middle" {B} font-size="26" fill="{OBS}">{ad}</text>'
    for j, (ad, c) in enumerate((("p", PROTON), ("n", NOTRON), ("e", ELEKTRON))):
        s += f'<rect x="{x0 + 14 + j * 76}" y="6" width="18" height="18" fill="{c}" stroke="{OBS}" stroke-width="1.2"/>'
        s += f'<text x="{x0 + 38 + j * 76}" y="23" {T} font-size="25" fill="{OBS}">{ad}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


# ------------------------------------------------------------------ ÜSTAD 3 · hidrojenin enerji düzeyleri ve geçişler

ENERJI_EV = {1: -13.6, 2: -3.4, 3: -1.51, 4: -0.85}       # E_n = −13,6/n² eV (yuvarlanmış)
GECIS = {"a": (4, 2), "b": (3, 2), "c": (2, 1), "d": (1, 3)}


def ustad_enerji(onek="ay-ue"):
    s = Svg(onek)
    W, H = 400, 340
    duz = {1: 312, 2: 150, 3: 92, 4: 56}
    s += f'<text x="398" y="30" text-anchor="end" {T7} font-size="22" fill="{GUM_K}">eV</text>'
    for n, y in duz.items():
        s += f'<path d="M58 {y} H278" stroke="{OBS}" stroke-width="2.6"/>'
        s += f'<text x="52" y="{y + 9}" text-anchor="end" {T} font-size="25" fill="{OBS}">n={n}</text>'
        s += f'<text x="284" y="{y + 9}" {T7} font-size="24" fill="{GUM_K}">{str(ENERJI_EV[n]).replace(".", ",").replace("-", "−")}</text>'
    xs = {"a": 90, "b": 140, "c": 190, "d": 240}
    for k, (a, b) in GECIS.items():
        x = xs[k]
        y0, y1 = duz[a], duz[b]
        renk = GOL_K if b > a else MER
        s += _ok(x, y0, x, y1 + (6 if b < a else -6), renk, 3.4, 13)
        s += f'<text x="{x + 9}" y="{(y0 + y1) / 2 + 9}" {B} font-size="30" fill="{renk}">{k}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info enerji")

# yeni düzen: atom-modelleri çizimleri, konu karakterli yeni çizimler ve 3B kurucuları ({{info|ad}} ve "uc_boyut" bu ad alanında arar)
from model_ciz import (zincir_yolu, pano_duzenek, pano_gecer, pano_sapar, pano_doner, pano_neden, pano_sonuc,  # noqa: E402,F401
                       enerji_merdiveni, mini_yorunge, mini_bulut, tekne_iskelesi, dis_katman, TEKNE, DIS_KATMAN)
from uc_unite import orbital_s, orbital_p, orbital_p_uc, alfa_levha, alfa_tanecik, atom_bosluk  # noqa: E402,F401


# ------------------------------------------------------------------ final · akçe rayı (yeni düzen: 1600 akçe)
AKCE_TOPLAM = 1600                                     # meta.json "akce_toplam" ile aynı (dogrula denetler)
AHILIK = (450, 900, 1300)                              # Kalfa, Usta, Atom Üstadı (s.1 ve final unvanlarıyla aynı)


def akce_rayi(onek="ay-ray", ust_unvan="ATOM ÜSTADI"):
    """Ortak cizim/infografik.akce_rayi'nin 1600 ölçekli eşi (ortaktaki 0–1400 sabit; kat 40 + karma 160 eklendi).
    {{info|akce_rayi|ATOM ÜSTADI}} önce bu modülde aranır."""
    s = Svg(onek)
    W, H = 1880, 260
    x0, x1, y = 60, 1820, 150
    T_ = AKCE_TOPLAM

    def X(a):
        return x0 + (x1 - x0) * a / T_
    kalfa, usta, ustad = AHILIK
    g = s.lin([(0, GUM), (kalfa / T_, GOL_A), (usta / T_, GOL), (ustad / T_, KEH), (1, KEH)], x0, 0, x1, 0, kull="userSpaceOnUse", ad="ry")
    s += f'<path d="M{x0} {y + 30} H{x1}" stroke="#9A6B42" stroke-width="12"/>'
    for k in range(0, T_ + 1, 50):
        s += f'<rect x="{f(X(k) - 6)}" y="{y + 18}" width="12" height="30" rx="3" fill="#7A4E2E"/>'
    s += f'<rect x="{x0}" y="{y - 20}" width="{x1 - x0}" height="40" rx="20" fill="{g}" stroke="{OBS}" stroke-width="4"/>'
    for a in range(0, T_ + 1, 100):
        s += f'<path d="M{f(X(a))} {y - 20} v{12 if a % 200 else 18}" stroke="{OBS}" stroke-width="3"/>'
    esik = [(0, "ÇIRAK", GUM_K), (kalfa, "KALFA", GOL_K), (usta, "USTA", DERIN), (ustad, ust_unvan, KEH_K), (T_, "", OBS)]
    for a, ad, c in esik:
        x = X(a)
        s += f'<path d="M{f(x)} {y - 26} V{y - 74}" stroke="{c}" stroke-width="4"/>'
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y - 92, 20), True)}" fill="{KEH if a == ustad else "#FFFFFF"}" stroke="{OBS}" stroke-width="3"/>'
        anc = "start" if a == 0 else ("end" if a == T_ else "middle")
        s += f'<text x="{f(x)}" y="{y + 92}" text-anchor="{anc}" {B} font-size="34" fill="{c}">{a}</text>'
        if ad:
            s += f'<text x="{f(x + (6 if a == 0 else 0))}" y="{y - 124}" text-anchor="{"start" if a == 0 else "middle"}" {T} font-size="26" fill="{c}">{ad}</text>'
    s += f'<text x="{x1}" y="{y - 124}" text-anchor="end" {T} font-size="26" fill="{OBS}">TOPLAM</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ray-svg")
