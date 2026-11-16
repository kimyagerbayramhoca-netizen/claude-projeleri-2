"""Periyodik Tablo · Maden Yolu I · üniteye özel bilgi grafikleri ({{info|ad}} → fn(onek, *arg)).

Birim kuralı: her grafikte 1 birim ≈ 0,1 mm (sayfadaki genişliğiyle çizilir); yazılar ≥ 22 birim (≈ 6,2 pt), çoğu 26–34.
Element verisi tablo_veri.py'den (kitap çerçevesinin periyodik tablosuyla aynı; dogrula.py denetler). Sınıf renkleri
çerçeveyle, blok renkleri klasik ünitenin büyük tablosuyla aynı ton ailesindedir. SVG yazısında kontur yok; alt/üst simge
`_alt()` ile tspan dy. Elektronegatiflik bilerek yazılmaz.
"""
import math
import re
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, selcuklu_yildizi, rng as RNG
from cizim.renkler import (OBS, SOLUK, GOL, GOL_K, GOL_A, GOL_AA, DERIN, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K,
                           KOB_A, ERGUVAN, ALTIN, ALTIN_K, ALTIN_A, LAJVER, ZUMRUT, GUM, GUM_K, GUM_A, KIREC)
import tablo_veri as TV

T = 'font-family="Nunito" font-weight="800"'
T9 = 'font-family="Nunito" font-weight="900"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'

# durak → rota elementleri (sınıf haritasındaki iğneler)
ROTA_EL = {"Al": 1, "Co": 2, "Cu": 2, "Ag": 3, "B": 4, "Na": 5}


# ------------------------------------------------------------------ yardımcılar

def _alt(metin, x, y, fs, renk=OBS, anchor="middle", font=B, ek=""):
    """Yazı içinde _2 → alt simge, ^{…} → üst simge (tspan dy)."""
    parca = re.split(r"(_\d+|\^\{[^}]*\})", metin)
    o = [f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(fs)}" fill="{renk}"{ek}>']
    dy = 0
    for p in parca:
        if not p:
            continue
        if p.startswith("_"):
            o.append(f'<tspan dy="{f(fs * .24 - dy)}" font-size="{f(fs * .66)}">{p[1:]}</tspan>')
            dy = fs * .24
        elif p.startswith("^"):
            o.append(f'<tspan dy="{f(-fs * .38 - dy)}" font-size="{f(fs * .62)}">{p[2:-1]}</tspan>')
            dy = -fs * .38
        else:
            o.append(f'<tspan dy="{f(-dy)}">{p}</tspan>' if dy else p)
            dy = 0
    o.append("</text>")
    return "".join(o)


def _ok(x0, y0, x1, y1, renk=OBS, k=4, uc=14):
    a = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - uc * math.cos(a - .45), y1 - uc * math.sin(a - .45))
    p2 = (x1 - uc * math.cos(a + .45), y1 - uc * math.sin(a + .45))
    return (f'<path d="M{f(x0)} {f(y0)} L{f(x1 - uc * .6 * math.cos(a))} {f(y1 - uc * .6 * math.sin(a))}" stroke="{renk}" stroke-width="{f(k)}" stroke-linecap="round"/>'
            f'<path d="M{f(x1)} {f(y1)} L{nok(p1)} L{nok(p2)} Z" fill="{renk}"/>')


def _kutu(x, y, w, h, renk="#FFFFFF", cz=OBS, r=14, k=3, kesik=False, ek=""):
    ks = ' stroke-dasharray="9 6"' if kesik else ""
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}" fill="{renk}" stroke="{cz}" stroke-width="{f(k)}"{ks}{ek}/>'


def _hap(x, y, metin, renk, yazi="#FFFFFF", fs=24, h=34, pad=14, font=T9):
    """Yuvarlak uçlu etiket hapı (x: sol kenar, y: üst kenar); genişliği yazı boyuna göre."""
    w = len(metin) * fs * .74 + 2 * pad
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{h}" rx="{h / 2}" fill="{renk}"/>'
            f'<text x="{f(x + w / 2)}" y="{f(y + h / 2 + fs * .36)}" text-anchor="middle" {font} font-size="{fs}" fill="{yazi}" letter-spacing="1">{metin}</text>'), w


def _yildiz_rozet(x, y, r, metin, dolgu=GOL, fs=None, yazi="#FFFFFF"):
    fs = fs or r * .95
    return (f'<path d="{cizgi_d(selcuklu_yildizi(x, y, r), True)}" fill="{ALTIN}" stroke="{OBS}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="{cizgi_d(selcuklu_yildizi(x, y, r * .8), True)}" fill="{dolgu}" stroke="{OBS}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<text x="{f(x)}" y="{f(y + fs * .36)}" text-anchor="middle" {B} font-size="{f(fs)}" fill="{yazi}">{metin}</text>')


def _igne(x, y, o=1.0, renk=MER, metin=""):
    """Harita iğnesi (sivri ucu x, y); başında küçük numara."""
    r = 13 * o
    d = (f"M{f(x)} {f(y)} C{f(x - r * .45)} {f(y - r * .9)} {f(x - r)} {f(y - r * 1.3)} {f(x - r)} {f(y - r * 1.9)} "
         f"A{f(r)} {f(r)} 0 1 1 {f(x + r)} {f(y - r * 1.9)} C{f(x + r)} {f(y - r * 1.3)} {f(x + r * .45)} {f(y - r * .9)} {f(x)} {f(y)} Z")
    o_ = f'<path d="{d}" fill="{renk}" stroke="{OBS}" stroke-width="{f(2 * o)}"/>'
    if metin:
        o_ += f'<circle cx="{f(x)}" cy="{f(y - r * 1.9)}" r="{f(r * .72)}" fill="#FFFFFF"/>'
        o_ += f'<text x="{f(x)}" y="{f(y - r * 1.9 + r * .36)}" text-anchor="middle" {B} font-size="{f(r * 1.05)}" fill="{OBS}">{metin}</text>'
    else:
        o_ += f'<circle cx="{f(x)}" cy="{f(y - r * 1.9)}" r="{f(r * .38)}" fill="#FFFFFF"/>'
    return o_


# ================================================================== 1. DURAK · tablonun hikâyesi (zaman şeridi)

TARIH = [
    ("1829", "Döbereiner", ["benzerleri üçlü", "gruplara ayırdı"], "atom kütlesi", "uclu"),
    ("1865", "Newlands", ["her sekizinci", "birinciye benzer"], "atom kütlesi", "oktav"),
    ("1869", "Mendeleyev", ["boşluk bıraktı,", "özellik tahmin etti"], "atom kütlesi", "kart"),
    ("1870", "L. Meyer", ["atom hacmi dalga", "dalga tekrar eder"], "atom kütlesi", "egri"),
    ("1913", "Moseley", ["X ışınlarıyla", "atom numarası"], "atom numarası", "xisin"),
]


def _tarih_ikon(tur, x, y, s):
    """Zaman şeridi madalyon ikonları (merkez x, y; yarıçap ≈ 44)."""
    o = []
    if tur == "uclu":
        for k, (dx, c) in enumerate(((-26, "#9DB7C6"), (0, "#F0A21A"), (26, "#5FC08A"))):
            r = 13 + k * 2.5
            o.append(f'<circle cx="{f(x + dx)}" cy="{f(y + 6)}" r="{f(r)}" fill="{c}" stroke="{OBS}" stroke-width="2.4"/>')
        o.append(f'<path d="M{f(x - 30)} {f(y - 18)} Q{f(x)} {f(y - 34)} {f(x + 30)} {f(y - 18)}" stroke="{OBS}" stroke-width="2.6" fill="none" stroke-dasharray="5 4"/>')
    elif tur == "oktav":
        for k in range(8):
            c = MER if k in (0, 7) else "#FFFFFF"
            o.append(f'<rect x="{f(x - 36 + k * 9)}" y="{f(y - 18)}" width="8" height="36" rx="2" fill="{c}" stroke="{OBS}" stroke-width="1.8"/>')
        o.append(f'<path d="M{f(x - 32)} {f(y + 26)} Q{f(x)} {f(y + 40)} {f(x + 32)} {f(y + 26)}" stroke="{MER_K}" stroke-width="3" fill="none"/>')
    elif tur == "kart":
        for i in range(3):
            for j in range(3):
                xx, yy = x - 33 + j * 23, y - 33 + i * 23
                if (i, j) == (1, 1):
                    o.append(f'<rect x="{f(xx)}" y="{f(yy)}" width="20" height="20" rx="3" fill="#FFF7E2" stroke="{MER}" stroke-width="2.6" stroke-dasharray="4 3"/>')
                    o.append(f'<text x="{f(xx + 10)}" y="{f(yy + 16)}" text-anchor="middle" {B} font-size="19" fill="{MER_K}">?</text>')
                else:
                    o.append(f'<rect x="{f(xx)}" y="{f(yy)}" width="20" height="20" rx="3" fill="{KOB_A}" stroke="{OBS}" stroke-width="1.8"/>')
    elif tur == "egri":
        pts = [(x - 38 + i * 4, y + 6 - 26 * math.exp(-((i % 7) - 1.2) ** 2 / 1.6) + i * .3) for i in range(20)]
        o.append(f'<path d="M{f(x - 40)} {f(y + 26)} H{f(x + 40)} M{f(x - 40)} {f(y + 26)} V{f(y - 30)}" stroke="{OBS}" stroke-width="2.4" fill="none"/>')
        o.append(f'<path d="{egri_d(pts)}" stroke="{KOB}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    elif tur == "xisin":
        o.append(f'<path d="M{f(x - 40)} {f(y - 4)} L{f(x - 6)} {f(y - 4)}" stroke="{ERGUVAN}" stroke-width="7" stroke-linecap="round" opacity=".55"/>')
        o.append(f'<path d="M{f(x - 40)} {f(y - 4)} q5 -8 10 0 t10 0 t10 0" stroke="{ERGUVAN}" stroke-width="2.6" fill="none"/>')
        for k in range(4):
            o.append(f'<rect x="{f(x - 2 + k * 10)}" y="{f(y + 14 - k * 12)}" width="9" height="{f(12 + k * 12)}" fill="{GOL}" stroke="{OBS}" stroke-width="1.6"/>')
        o.append(f'<text x="{f(x + 18)}" y="{f(y - 34)}" text-anchor="middle" {B} font-size="20" fill="{GOL_K}">Z</text>')
    return "".join(o)


def tarih_seridi(onek="pt-tar"):
    """Döbereiner → Newlands → Mendeleyev → Meyer → Moseley: yatay şerit (madalyon + yazı). Genişlik 1860 (≈ 186 mm)."""
    s = Svg(onek)
    W, H = 1860, 182
    n = len(TARIH)
    sw = W / n
    for i, (yil, ad, fikir, olcut, ikon) in enumerate(TARIH):
        x0 = i * sw
        son = i == n - 1
        cx, cy = x0 + 62, 88
        dolgu = GOL if son else (KEH if i == 2 else "#FFFFFF")
        s += f'<circle cx="{f(cx)}" cy="{cy}" r="56" fill="{ALTIN}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<circle cx="{f(cx)}" cy="{cy}" r="48" fill="{acik(dolgu, .55) if dolgu != "#FFFFFF" else "#FFFFFF"}" stroke="{OBS}" stroke-width="2"/>'
        s += _tarih_ikon(ikon, cx, cy, s)
        tx = x0 + 130
        s += f'<text x="{f(tx)}" y="42" {B} font-size="40" fill="{GOL_K if son else OBS}">{yil}</text>'
        s += f'<text x="{f(tx)}" y="76" {T9} font-size="28" fill="{OBS}">{ad}</text>'
        for k, satir in enumerate(fikir):
            s += f'<text x="{f(tx)}" y="{106 + k * 27}" {T} font-size="24" fill="#343947">{satir}</text>'
        h_, w_ = _hap(0, 0, olcut.upper(), GOL if son else GUM_K, fs=18, h=26, pad=10)
        s += f'<g transform="translate({f(tx)} 150)">{h_}</g>'
        if not son:
            ax = x0 + sw - 14
            s += f'<path d="M{f(ax - 12)} {cy - 16} L{f(ax + 2)} {cy} L{f(ax - 12)} {cy + 16}" stroke="{ALTIN_K}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ================================================================== 1. DURAK · modern tablonun iskeleti (bloklar)

def blok_haritasi(onek="pt-blk"):
    """Periyot × grup iskeleti, bloklara göre renkli; sağda periyottaki element sayısı. Al ve Ga işaretli."""
    s = Svg(onek)
    X0, Y0, CW, RH, W_, H_ = 62, 66, 50, 40, 46, 36
    W, H = X0 + 18 * CW + 96, Y0 + 7 * RH + 18 + 2 * RH + 40
    for g in range(1, 19):
        x = X0 + (g - 1) * CW + W_ / 2
        s += f'<text x="{f(x)}" y="{Y0 - 38}" text-anchor="middle" {B} font-size="25" fill="{LAJVER}">{g}</text>'
        s += f'<text x="{f(x)}" y="{Y0 - 10}" text-anchor="middle" {T9} font-size="19" fill="{GUM_K}">{TV.ab_adi(g)}</text>'
    for p in range(1, 8):
        y = Y0 + (p - 1) * RH + H_ / 2 + 9
        s += f'<text x="{X0 - 22}" y="{f(y)}" text-anchor="middle" {B} font-size="27" fill="{LAJVER}">{p}</text>'
        say = TV.SON[p] - TV.BAS[p] + 1
        s += f'<text x="{X0 + 18 * CW + 44}" y="{f(y)}" text-anchor="middle" {B} font-size="27" fill="{MER_K}">{say}</text>'
    s += f'<text x="{X0 + 18 * CW + 44}" y="{Y0 - 26}" text-anchor="middle" {T9} font-size="18" fill="{MER_K}">ELEMENT</text>'
    s += f'<text x="{X0 - 22}" y="{Y0 - 26}" text-anchor="middle" {T9} font-size="18" fill="{LAJVER}">P.</text>'
    for el in TV.ELEMENTLER:
        z = el["z"]
        sut, sat = TV.hucre_konum(z)
        x = X0 + (sut - 1) * CW
        y = Y0 + (sat - 1) * RH + (18 if sat > 7 else 0)
        dol, cz = TV.BLOK_RENK[TV.blok(z)]
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{W_}" height="{H_}" rx="6" fill="{dol}" stroke="{cz}" stroke-width="2"/>'
        if el["sembol"] in ("Al", "Ga"):
            s += f'<rect x="{f(x - 3)}" y="{f(y - 3)}" width="{W_ + 6}" height="{H_ + 6}" rx="8" fill="none" stroke="{OBS}" stroke-width="4.4"/>'
            s += f'<text x="{f(x + W_ / 2)}" y="{f(y + 27)}" text-anchor="middle" {B} font-size="24" fill="{OBS}">{el["sembol"]}</text>'
    for p in (6, 7):
        x, y = X0 + 2 * CW, Y0 + (p - 1) * RH
        dol, cz = TV.BLOK_RENK["f"]
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{W_}" height="{H_}" rx="6" fill="#FFFFFF" stroke="{cz}" stroke-width="2.4" stroke-dasharray="5 4"/>'
        s += f'<text x="{f(x + W_ / 2)}" y="{f(y + 27)}" text-anchor="middle" {B} font-size="24" fill="{cz}">{"*" if p == 6 else "**"}</text>'
    # blok harfleri
    for b, (sut, sat, renk) in {"s": (1.5, 2.6, "#D63F72"), "d": (7.5, 4.6, "#C17F06"), "p": (15.5, 2.6, KOB), "f": (10, 8.55, ZUMRUT)}.items():
        x = X0 + (sut - 1) * CW + W_ / 2
        y = Y0 + (sat - 1) * RH + (18 if sat > 7 else 0) + 28
        s += f'<text x="{f(x)}" y="{f(y)}" text-anchor="middle" {B} font-size="54" fill="{renk}" opacity=".9">{b}</text>'
    s += f'<text x="{f(X0 + 3.6 * CW)}" y="{f(Y0 + 0.62 * RH + 2)}" {T} font-size="23" fill="{SOLUK}">1–3. periyotta geçiş elementi yok:</text>'
    s += f'<text x="{f(X0 + 3.6 * CW)}" y="{f(Y0 + 1.28 * RH + 2)}" {T} font-size="23" fill="{SOLUK}">2A’dan sonra doğrudan 3A gelir.</text>'
    yf = Y0 + 7 * RH + 18
    for r, ad in enumerate(("* Lantanitler (57–71)", "** Aktinitler (89–103)")):
        s += f'<text x="{f(X0 + 2 * CW - 10)}" y="{f(yf + r * RH + 25)}" text-anchor="end" {T9} font-size="20" fill="{ZUMRUT}">{ad.split(" (")[0]}</text>'
    # ok: Al → Ga (eka-alüminyum)
    xa = X0 + 12 * CW + W_ + 6
    ya1, ya2 = Y0 + 2 * RH + H_ / 2, Y0 + 3 * RH + H_ / 2
    s += f'<path d="M{f(xa)} {f(ya1)} C{f(xa + 40)} {f(ya1 + 4)} {f(xa + 40)} {f(ya2 - 4)} {f(xa + 6)} {f(ya2)}" stroke="{MER}" stroke-width="4" fill="none"/>'
    s += f'<path d="M{f(xa + 4)} {f(ya2)} l12 -9 l1 13 Z" fill="{MER}"/>'
    lx = X0
    ly = H - 14
    for b, ad in (("s", "s bloku"), ("p", "p bloku"), ("d", "d bloku"), ("f", "f bloku (iç geçiş)")):
        dol, cz = TV.BLOK_RENK[b]
        s += f'<rect x="{lx}" y="{ly - 22}" width="34" height="26" rx="5" fill="{dol}" stroke="{cz}" stroke-width="2"/>'
        s += f'<text x="{lx + 42}" y="{ly}" {T9} font-size="22" fill="{cz}">{ad}</text>'
        lx += 64 + len(ad) * 13
    s += f'<text x="{W - 4}" y="{ly}" text-anchor="end" {T9} font-size="20" fill="{MER_K}">Al’nin altı: eka-alüminyum = Ga</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ================================================================== 2. DURAK · dizilimden adrese (Co) ve dolma sırası

def adres_okuma(onek="pt-adr"):
    """₂₇Co: 1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁷ → periyot, blok, grup. Çini karoları gibi dizilmiş orbital terimleri."""
    s = Svg(onek)
    W, H = 1240, 400
    terim = [("1s", 2), ("2s", 2), ("2p", 6), ("3s", 2), ("3p", 6), ("4s", 2), ("3d", 7)]
    s += _alt("_27Co", 18, 70, 54, KOB_K, "start")
    s += f'<text x="20" y="104" {T9} font-size="20" fill="{GUM_K}" letter-spacing="1">KOBALT</text>'
    x0, y0, kw, kh, ara = 190, 26, 136, 92, 10
    for i, (o, n) in enumerate(terim):
        x = x0 + i * (kw + ara)
        vurgu = o in ("4s", "3d")
        dol = "#FFFFFF" if not vurgu else (KOB_A if o == "4s" else KEH_A)
        cz = OBS if not vurgu else (KOB if o == "4s" else KEH_K)
        s += f'<rect x="{f(x)}" y="{y0}" width="{kw}" height="{kh}" rx="10" fill="{dol}" stroke="{cz}" stroke-width="{4 if vurgu else 2.4}"/>'
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x + 18, y0 + 18, 11), True)}" fill="{GOL_A}" stroke="{GOL}" stroke-width="1.4"/>'
        s += _alt(f"{o}^{{{n}}}", x + kw / 2 + 6, y0 + 62, 46, OBS)
    # köşeli ayraçlar ve oklar
    x4s = x0 + 5 * (kw + ara) + kw / 2
    x3d = x0 + 6 * (kw + ara) + kw / 2
    yb = y0 + kh + 8
    kut = [(40, "PERİYOT", "4", "en büyük n = 4", KOB, KOB_A, x4s),
           (440, "BLOK", "d", "son orbital: d → B grubu", KEH_K, KEH_A, x3d),
           (840, "GRUP", "8B", "2 + 7 = 9 → IUPAC 9", MER, MER_A, (x4s + x3d) / 2)]
    s += f'<path d="M{f(x4s - kw / 2)} {yb + 14} V{yb + 26} H{f(x3d + kw / 2)} V{yb + 14}" stroke="{MER}" stroke-width="3.4" fill="none"/>'
    for (bx, ust, buyuk, alt, cz, dol, hx) in kut:
        by = 262
        s += _kutu(bx, by, 360, 124, dol, cz, 16, 3.4)
        s += f'<text x="{bx + 22}" y="{by + 36}" {T9} font-size="24" fill="{cz}" letter-spacing="1.6">{ust}</text>'
        s += f'<text x="{bx + 340}" y="{by + 96}" text-anchor="end" {B} font-size="78" fill="{OBS}">{buyuk}</text>'
        s += f'<text x="{bx + 22}" y="{by + 72}" {T} font-size="25" fill="#343947">{alt.split(" → ")[0]}</text>'
        if " → " in alt:
            s += f'<text x="{bx + 22}" y="{by + 102}" {T} font-size="25" fill="#343947">→ {alt.split(" → ")[1]}</text>'
        ty = yb + (30 if ust == "GRUP" else 4)
        s += _ok(hx, ty, bx + 180 + (hx - bx - 180) * .35, by - 6, cz, 3.6, 16)
    return s.cikti(f"0 0 {W} {H}", cls="info")


def dolma_sirasi(onek="pt-dol"):
    """Orbitallerin dolma sırası (köşegen kuralı): 1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s …"""
    s = Svg(onek)
    W, H = 560, 318
    satir = [["1s"], ["2s", "2p"], ["3s", "3p", "3d"], ["4s", "4p", "4d", "4f"], ["5s", "5p", "5d", "5f"]]
    x0, y0, dx, dy = 66, 52, 108, 52
    renk = {"s": TV.BLOK_RENK["s"], "p": TV.BLOK_RENK["p"], "d": TV.BLOK_RENK["d"], "f": TV.BLOK_RENK["f"]}
    for k in range(6):
        # köşegen oklar: (n, l) → n + l = sabit, sağ üstten sol alta
        ust = [(n, l) for n in range(1, len(satir) + 1) for l in range(4) if n + l == k + 1 and l < len(satir[n - 1])]
        if not ust:
            continue
        a = min(ust, key=lambda t: t[0])
        b = max(ust, key=lambda t: t[0])
        xa, ya = x0 + a[1] * dx + 30, y0 + (a[0] - 1) * dy - 22
        xb, yb = x0 + b[1] * dx - 30, y0 + (b[0] - 1) * dy + 18
        if a == b:
            xa, ya, xb, yb = xa - 4, ya + 2, xb + 18, yb - 8
        s += _ok(xa + 24, ya - 12, xb - 4, yb + 6, MER, 3.2, 13)
    for n, row in enumerate(satir):
        for l, o in enumerate(row):
            x, y = x0 + l * dx, y0 + n * dy
            dol, cz = renk[o[-1]]
            s += f'<rect x="{x - 34}" y="{y - 30}" width="68" height="40" rx="9" fill="{dol}" stroke="{cz}" stroke-width="2.2"/>'
            s += f'<text x="{x}" y="{y}" text-anchor="middle" {B} font-size="29" fill="{OBS}">{o}</text>'
    s += f'<text x="{W - 6}" y="{H - 6}" text-anchor="end" {T9} font-size="24" fill="{MER_K}">4s, 3d’den önce dolar</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ================================================================== 3. DURAK · soy gaz cetveli ve katman modeli

def soygaz_cetveli(onek="pt-soy"):
    """0–118 sayı doğrusu: soy gazlar periyot sonu; Ag (47) = 36 + 11 ve P (15) = 10 + 5 örnekleri."""
    s = Svg(onek)
    W, H = 1860, 262
    x0, x1, y = 40, 1820, 128

    def X(z):
        return x0 + (x1 - x0) * z / 118

    renkler = ["#FFE1D8", "#FFEBB8", "#D2F1EE", "#DDE6FB", "#EDDDF3", "#FFDCE7", "#D7F1E2"]
    onceki = 0
    for i, z in enumerate(TV.SOY_Z):
        s += f'<rect x="{f(X(onceki))}" y="{y - 26}" width="{f(X(z) - X(onceki))}" height="52" fill="{renkler[i]}" stroke="{OBS}" stroke-width="2.2"/>'
        orta = (X(onceki) + X(z)) / 2
        etk = f"{i + 1}. periyot" if X(z) - X(onceki) > 160 else f"{i + 1}."
        s += f'<text x="{f(orta)}" y="{y + 9}" text-anchor="middle" {T9} font-size="{24 if X(z) - X(onceki) > 160 else 22}" fill="{OBS}">{etk}</text>'
        onceki = z
    for z in TV.SOY_Z:
        sem = TV.SEMBOL[z - 1]
        s += f'<path d="M{f(X(z))} {y - 40} V{y + 40}" stroke="{ERGUVAN}" stroke-width="5"/>'
        s += f'<circle cx="{f(X(z))}" cy="{y - 58}" r="24" fill="{ERGUVAN}" stroke="{OBS}" stroke-width="2"/>'
        s += f'<text x="{f(X(z))}" y="{y - 49}" text-anchor="middle" {B} font-size="{24 if len(sem) == 1 else 21}" fill="#FFFFFF">{sem}</text>'
        s += f'<text x="{f(X(z))}" y="{y + 70}" text-anchor="middle" {B} font-size="30" fill="{ERGUVAN}">{z}</text>'
    # örnek: Ag 47
    xa, xb = X(36), X(47)
    s += f'<path d="M{f(xa)} {y + 86} C{f(xa)} {y + 116} {f(xb)} {y + 116} {f(xb)} {y + 86}" stroke="{GOL_K}" stroke-width="4" fill="none"/>'
    s += f'<path d="M{f(xb)} {y + 82} l-9 15 h18 Z" fill="{GOL_K}"/>'
    s += f'<text x="{f(xb + 30)}" y="{y + 122}" {T9} font-size="26" fill="{GOL_K}">Ag: 47 − 36 = 11 → 5. periyot, 11. grup (1B)</text>'
    # örnek: P 15
    xa, xb = X(10), X(15)
    s += f'<path d="M{f(xa)} {y - 86} C{f(xa)} {y - 112} {f(xb)} {y - 112} {f(xb)} {y - 86}" stroke="{MER_K}" stroke-width="4" fill="none"/>'
    s += f'<path d="M{f(xb)} {y - 82} l-9 -15 h18 Z" fill="{MER_K}"/>'
    s += f'<text x="{f(xb + 26)}" y="{y - 98}" {T9} font-size="26" fill="{MER_K}">P: 15 − 10 = 5 → 3. periyot · 5 + 10 = 15. grup (5A)</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


def _katman(s, cx, cy, z, dizi, etiket, renk, r0=30, ara=26, e_r=7.5, yazilar=True):
    o = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{r0 - 6}" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>',
         f'<text x="{f(cx)}" y="{f(cy + 9)}" text-anchor="middle" {B} font-size="25" fill="#FFFFFF">{z}+</text>']
    for k, n in enumerate(dizi):
        r = r0 + 10 + k * ara
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{GUM_K}" stroke-width="2"/>')
        for j in range(n):
            a = -math.pi / 2 + 2 * math.pi * j / n + (.25 if k % 2 else 0)
            son = k == len(dizi) - 1
            o.append(f'<circle cx="{f(cx + r * math.cos(a))}" cy="{f(cy + r * math.sin(a))}" r="{e_r}" fill="{KEH if son else KOB}" stroke="{OBS}" stroke-width="1.6"/>')
    rmax = r0 + 10 + (len(dizi) - 1) * ara
    if not yazilar:
        return "".join(o)
    o.append(_alt(etiket, cx, cy + rmax + 42, 32, OBS))
    o.append(f'<text x="{f(cx)}" y="{f(cy + rmax + 76)}" text-anchor="middle" {T9} font-size="25" fill="{KOB_K}">{" · ".join(str(n) for n in dizi)}</text>')
    return "".join(o)


def katman_modeli(onek="pt-kat"):
    """İlk 20 element: katman sayısı = periyot, son katmandaki e⁻ = A grubu. Al (2·8·3) ve K (2·8·8·1), yan yana."""
    s = Svg(onek)
    W, H = 900, 300
    s += _katman(s, 150, 146, 13, [2, 8, 3], "", "#9DA9B5", r0=26, ara=24, e_r=7, yazilar=False)
    s += _katman(s, 590, 146, 19, [2, 8, 8, 1], "", "#A57BE0", r0=26, ara=22, e_r=7, yazilar=False)
    for x, ad, dz, sonuc in ((300, "_13Al", "2 · 8 · 3", "3 katman → 3. periyot · 3A"), (720, "_19K", "2 · 8 · 8 · 1", "4 katman → 4. periyot · 1A")):
        s += _alt(ad, x, 120, 40, OBS, "start")
        s += f'<text x="{x}" y="160" {T9} font-size="30" fill="{KOB_K}">{dz}</text>'
    s += f'<text x="20" y="292" {T9} font-size="27" fill="{MER_K}">Al: 3 katman → 3. periyot 3A · K: 4 katman → 4. periyot 1A</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ================================================================== 4. DURAK · sınıf haritası (rota elementleri işaretli)

def sinif_haritasi(onek="pt-sin"):
    """118 elementin metal / ametal / yarı metal / soy gaz haritası (çerçevenin renkleri), merdiven çizgisi, rota iğneleri."""
    s = Svg(onek)
    X0, Y0, CW, RH, W_, H_ = 46, 28, 100, 41, 95, 37
    YF = Y0 + 7 * RH + 14
    W, H = X0 + 18 * CW + 6, YF + 2 * RH + 8
    for p in range(1, 8):
        s += f'<text x="{X0 - 22}" y="{f(Y0 + (p - 1) * RH + H_ / 2 + 10)}" text-anchor="middle" {B} font-size="28" fill="{LAJVER}">{p}</text>'
    for g in (1, 2, 13, 14, 15, 16, 17, 18):
        x = X0 + (g - 1) * CW + W_ / 2
        yy = Y0 - 6 if g in (1, 18) else (Y0 + RH - 6 if g in (2, 13, 14, 15, 16, 17) else Y0 - 6)
        s += f'<text x="{f(x)}" y="{f(yy)}" text-anchor="middle" {T9} font-size="20" fill="{GUM_K}">{TV.ab_adi(g)}</text>'
    for el in TV.ELEMENTLER:
        z, sem = el["z"], el["sembol"]
        sut, sat = TV.hucre_konum(z)
        x = X0 + (sut - 1) * CW
        y = Y0 + (sat - 1) * RH if sat <= 7 else YF + (sat - 8) * RH
        dol, cz, _ = TV.SINIF_RENK[TV.sinif(sem)]
        rota = sem in ROTA_EL
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{W_}" height="{H_}" rx="7" fill="{dol}" stroke="{OBS if rota else cz}" stroke-width="{4.2 if rota else 1.8}"/>'
        s += f'<rect x="{f(x + 1)}" y="{f(y + 1)}" width="{W_ - 2}" height="7" rx="4" fill="{cz}"/>'
        s += f'<text x="{f(x + 7)}" y="{f(y + 22)}" {T9} font-size="16" fill="{GUM_K}">{z}</text>'
        s += f'<text x="{f(x + W_ / 2 + 10)}" y="{f(y + 33)}" text-anchor="middle" {B} font-size="{33 if len(sem) == 1 else 30}" fill="{OBS}">{sem}</text>'
        if rota:
            s += _yildiz_rozet(x + W_ - 6, y + 4, 17, str(ROTA_EL[sem]), MER, fs=20)
    for p, metin in ((6, "57–71"), (7, "89–103")):
        x, y = X0 + 2 * CW, Y0 + (p - 1) * RH
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{W_}" height="{H_}" rx="7" fill="#FFF4F0" stroke="{MER}" stroke-width="1.8" stroke-dasharray="6 4"/>'
        s += f'<text x="{f(x + W_ / 2)}" y="{f(y + 26)}" text-anchor="middle" {T9} font-size="20" fill="{MER_K}">{metin}</text>'
    for r, ad in enumerate(("lantanitler", "aktinitler")):
        s += f'<text x="{f(X0 + 2 * CW - 10)}" y="{f(YF + r * RH + 26)}" text-anchor="end" {T9} font-size="21" fill="{MER_K}">{ad}</text>'
    # merdiven (çerçevedeki periyodik tablo sayfasıyla aynı basamaklar)
    basamak = [(2, 13), (3, 14), (4, 14), (5, 15), (6, 16), (7, 16)]
    d = []
    for i, (p, g) in enumerate(basamak):
        x = X0 + (g - 1) * CW - (CW - W_) / 2
        y = Y0 + (p - 1) * RH - (RH - H_) / 2
        d.append(f"M{f(x)} {f(y)}" if i == 0 else f"H{f(x)}")
        d.append(f"V{f(y + RH)}")
    s += f'<path d="{" ".join(d)}" fill="none" stroke="{OBS}" stroke-width="7.5" stroke-linejoin="round"/>'
    # boşluğa açıklama: sınıflar
    lx, ly = X0 + 2 * CW + 14, Y0 + 14
    s += f'<text x="{lx}" y="{ly + 6}" {T9} font-size="22" fill="{LAJVER}" letter-spacing="1.5">SINIFLAR · ÇERÇEVEDEKİ TABLOYLA AYNI RENKLER</text>'
    x = lx
    for k in ("metal", "ametal", "yari", "soy", "belirsiz"):
        dol, cz, ad = TV.SINIF_RENK[k]
        ad = {"belirsiz": "Po, At, 113–117: belirsiz"}.get(k, ad)
        s += f'<rect x="{x}" y="{ly + 22}" width="44" height="30" rx="5" fill="{dol}" stroke="{cz}" stroke-width="2"/><rect x="{x}" y="{ly + 22}" width="44" height="7" rx="3" fill="{cz}"/>'
        s += f'<text x="{x + 52}" y="{ly + 46}" {T9} font-size="23" fill="{OBS}">{ad}</text>'
        x += 72 + len(ad) * 12.6
    s += _yildiz_rozet(lx + 14, ly + 80, 16, "1", MER, fs=19)
    s += f'<text x="{lx + 40}" y="{ly + 88}" {T9} font-size="23" fill="{MER_K}">Rotamızın elementleri: 1 Al · 2 Co, Cu · 3 Ag · 4 B · 5 Na (durak no)</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ================================================================== 4. DURAK · özellik çizelgesi

OZELLIK = [
    ("görünüş", ["parlak", "parlak (gri)", "çoğu mat", "renksiz"]),
    ("iletkenlik", ["çok iyi", "yarı iletken", "iletmez*", "iletmez"]),
    ("çekiçle", ["tel, levha olur", "kırılır", "katısı ufalanır", "—"]),
    ("oda koşulu", ["katı (Hg sıvı)", "katı", "katı, sıvı, gaz", "tek atomlu gaz"]),
    ("tepkimede", ["yalnız + değer", "ikisine benzer", "+ ya da − değer", "çok isteksiz"]),
]


def _ozellik_ikon(sat, sut, x, y):
    """Satır ikonları: parıltı, şimşek, çekiç, hâl, ± (sütuna göre dolu / yarım / boş)."""
    o = []
    if sat == 0:
        if sut in (0, 1):
            for a in range(4):
                aa = a * math.pi / 4
                o.append(f'<path d="M{f(x - 12 * math.cos(aa))} {f(y - 12 * math.sin(aa))} L{f(x + 12 * math.cos(aa))} {f(y + 12 * math.sin(aa))}" stroke="{KEH_K}" stroke-width="{3 if a % 2 == 0 else 2}" stroke-linecap="round"/>')
        else:
            o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="10" fill="{GUM_A}" stroke="{GUM_K}" stroke-width="2"/>')
    elif sat == 1:
        d = f"M{f(x + 3)} {f(y - 15)} L{f(x - 8)} {f(y + 2)} H{f(x)} L{f(x - 3)} {f(y + 15)} L{f(x + 9)} {f(y - 3)} H{f(x + 1)} Z"
        dol = {0: KEH, 1: KEH_A, 2: "#FFFFFF", 3: "#FFFFFF"}[sut]
        o.append(f'<path d="{d}" fill="{dol}" stroke="{OBS}" stroke-width="1.8" stroke-linejoin="round"/>')
        if sut >= 2:
            o.append(f'<path d="M{f(x - 13)} {f(y + 13)} L{f(x + 13)} {f(y - 13)}" stroke="{MER}" stroke-width="3" stroke-linecap="round"/>')
    elif sat == 2:
        if sut == 0:
            o.append(f'<path d="M{f(x - 14)} {f(y + 8)} h28 v5 h-28 Z" fill="#C9D3DC" stroke="{OBS}" stroke-width="1.6"/>')
            o.append(f'<path d="M{f(x - 4)} {f(y + 6)} L{f(x + 6)} {f(y - 12)}" stroke="#8A5A2E" stroke-width="4" stroke-linecap="round"/><rect x="{f(x + 1)}" y="{f(y - 19)}" width="14" height="8" rx="2" fill="#586874" transform="rotate(28 {f(x + 8)} {f(y - 15)})"/>')
        elif sut in (1, 2):
            for k, (dx, dy) in enumerate(((-8, 4), (4, 8), (8, -5), (-3, -8))):
                o.append(f'<path d="M{f(x + dx)} {f(y + dy)} l6 -3 l2 6 l-6 2 Z" fill="{"#B9C3CC" if sut == 1 else "#F2C230"}" stroke="{OBS}" stroke-width="1.2"/>')
    elif sat == 3:
        if sut == 3:
            for k in range(3):
                o.append(f'<circle cx="{f(x - 10 + k * 10)}" cy="{f(y + (k % 2) * 6 - 3)}" r="4" fill="{ERGUVAN}"/>')
        else:
            o.append(f'<rect x="{f(x - 11)}" y="{f(y - 9)}" width="22" height="18" rx="3" fill="{["#C9D3DC", "#B9C3CC", "#F2C230"][sut]}" stroke="{OBS}" stroke-width="1.6"/>')
    elif sat == 4:
        isaret = {0: "+", 1: "±", 2: "±", 3: "0"}[sut]
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="13" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.8"/>')
        o.append(f'<text x="{f(x)}" y="{f(y + 9)}" text-anchor="middle" {B} font-size="24" fill="{OBS}">{isaret}</text>')
    return "".join(o)


def ozellik_tablosu(onek="pt-ozl"):
    """Metal · yarı metal · ametal · soy gaz: beş özellik, ikonlu çizelge (çerçeve renkleri)."""
    s = Svg(onek)
    W, H = 1080, 380
    X0, Y0, CW, RH = 190, 64, 222, 57
    basliklar = [("metal", "Metal", "Al, Ag, Cu"), ("yari", "Yarı metal", "B, Si"), ("ametal", "Ametal", "S, O, Cl"), ("soy", "Soy gaz", "Ne, Ar")]
    for j, (k, ad, ornek) in enumerate(basliklar):
        dol, cz, _ = TV.SINIF_RENK[k]
        x = X0 + j * CW
        s += f'<rect x="{x + 4}" y="4" width="{CW - 8}" height="56" rx="12" fill="{cz}"/>'
        s += f'<text x="{x + CW / 2}" y="32" text-anchor="middle" {B} font-size="28" fill="#FFFFFF">{ad}</text>'
        s += f'<text x="{x + CW / 2}" y="53" text-anchor="middle" {T9} font-size="19" fill="#FFFFFF">{ornek}</text>'
        s += f'<rect x="{x + 4}" y="{Y0}" width="{CW - 8}" height="{len(OZELLIK) * RH - 6}" rx="12" fill="{dol}" stroke="{cz}" stroke-width="2"/>'
    for i, (ozel, degerler) in enumerate(OZELLIK):
        y = Y0 + i * RH
        s += f'<text x="{X0 - 14}" y="{y + RH / 2 + 6}" text-anchor="end" {T9} font-size="23" fill="{LAJVER}">{ozel.upper()}</text>'
        if i:
            s += f'<path d="M{X0 - 170} {y - 3} H{X0 + 4 * CW - 6}" stroke="{OBS}" stroke-width="1.2" stroke-dasharray="4 5" opacity=".45"/>'
        for j, deg in enumerate(degerler):
            x = X0 + j * CW
            s += _ozellik_ikon(i, j, x + 30, y + RH / 2 - 3)
            s += f'<text x="{x + 52}" y="{y + RH / 2 + 5}" {T9} font-size="{23 if len(deg) <= 13 else 21}" fill="{OBS}">{deg}</text>'
    s += f'<text x="{W - 6}" y="{H - 8}" text-anchor="end" {T} font-size="21" fill="{SOLUK}">* grafit (C) iletir · F yalnız 1− olur</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ================================================================== 5. DURAK · aileler ve iyon oluşumu

AILE = [
    ("1A", "Alkali metaller", ["Li", "Na", "K", "Rb", "Cs", "Fr"], ["1 değerlik e^{−}", "→ 1+ iyon"], "#FFE1D8", MER, "Na"),
    ("2A", "Toprak alkali", ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"], ["2 değerlik e^{−}", "→ 2+ iyon"], "#FFF0CF", KEH_K, "Mg"),
    ("3A", "Toprak metalleri", ["B", "Al", "Ga", "In", "Tl"], ["3 değerlik e^{−}", "B yarı metal"], "#E6ECFB", KOB, "Al"),
    ("3B–2B", "Geçiş metalleri", ["Co", "Cu", "Ag", "Fe", "Mn"], ["d bloku", "hepsi metal"], "#FFEFC4", "#C17F06", "Co"),
    ("7A", "Halojenler", ["F", "Cl", "Br", "I", "At", "Ts"], ["7 değerlik e^{−}", "→ 1− iyon"], "#D2F1EE", GOL_K, "Cl"),
    ("8A", "Soy gazlar", ["He", "Ne", "Ar", "Kr", "Xe", "Rn"], ["8 değerlik e^{−}", "(He: 2)"], "#EDDDF3", ERGUVAN, "Ar"),
]


def aileler(onek="pt-ail"):
    """Grupların özel adları: altı aile sütunu; Bandırma'da gördüklerimiz (Na, Mg, Cl) işaretli."""
    s = Svg(onek)
    W, H = 1860, 404
    HK = 362
    cw = W / len(AILE)
    for i, (grp, ad, uyeler, notlar, dol, cz, vurgu) in enumerate(AILE):
        x = i * cw
        s += f'<rect x="{f(x + 6)}" y="6" width="{f(cw - 12)}" height="{HK - 12}" rx="18" fill="{dol}" stroke="{cz}" stroke-width="3"/>'
        s += f'<rect x="{f(x + 6)}" y="6" width="{f(cw - 12)}" height="64" rx="18" fill="{cz}"/><rect x="{f(x + 6)}" y="50" width="{f(cw - 12)}" height="20" fill="{cz}"/>'
        s += f'<text x="{f(x + cw / 2)}" y="32" text-anchor="middle" {T9} font-size="21" fill="#FFFFFF" letter-spacing="1.4">{grp}</text>'
        s += f'<text x="{f(x + cw / 2)}" y="62" text-anchor="middle" {B} font-size="{30 if len(ad) < 15 else 27}" fill="#FFFFFF">{ad}</text>'
        sx = x + 22
        for k, u in enumerate(uyeler):
            yy = 78 + k * 46
            v = u == vurgu
            s += f'<rect x="{f(sx)}" y="{yy}" width="78" height="40" rx="7" fill="#FFFFFF" stroke="{OBS if v else cz}" stroke-width="{4 if v else 1.8}"/>'
            s += f'<text x="{f(sx + 39)}" y="{yy + 30}" text-anchor="middle" {B} font-size="27" fill="{OBS}">{u}</text>'
        ix = x + 204
        if grp in ("1A", "2A", "7A"):
            yuk = {"1A": "1+", "2A": "2+", "7A": "1−"}[grp]
            s += f'<circle cx="{f(ix)}" cy="146" r="48" fill="#FFFFFF" stroke="{cz}" stroke-width="4"/>'
            s += f'<text x="{f(ix)}" y="163" text-anchor="middle" {B} font-size="46" fill="{cz}">{yuk}</text>'
            s += f'<text x="{f(ix)}" y="222" text-anchor="middle" {T9} font-size="20" fill="{cz}" letter-spacing="1">İYON YÜKÜ</text>'
        elif grp == "3A":
            s += f'<circle cx="{f(ix)}" cy="146" r="48" fill="#FFFFFF" stroke="{cz}" stroke-width="4"/>'
            s += _alt("Al^{3+}", ix, 160, 38, cz)
            s += f'<text x="{f(ix)}" y="222" text-anchor="middle" {T9} font-size="20" fill="{cz}" letter-spacing="1">SEYDİŞEHİR</text>'
        elif grp == "8A":
            for k in range(3):
                s += f'<circle cx="{f(ix - 30 + k * 30)}" cy="{146 + (k % 2) * 22 - 11}" r="17" fill="#FFFFFF" stroke="{cz}" stroke-width="3"/>'
            s += f'<text x="{f(ix)}" y="222" text-anchor="middle" {T9} font-size="20" fill="{cz}" letter-spacing="1">TEK ATOM</text>'
        else:
            for k, c in enumerate(("#2B50B5", "#1FA7A0", "#B9C3CC")):
                s += f'<rect x="{f(ix - 50 + k * 34)}" y="{112 + k * 8}" width="30" height="62" rx="6" fill="{c}" stroke="{OBS}" stroke-width="2"/>'
            s += f'<text x="{f(ix)}" y="222" text-anchor="middle" {T9} font-size="20" fill="{cz}" letter-spacing="1">RENKLİ</text>'
        for k, n_ in enumerate(notlar):
            s += _alt(n_, ix, 270 + k * 34, 24, OBS, font=T9)
    s += f'<text x="{W / 2}" y="{H - 10}" text-anchor="middle" {T} font-size="23" fill="{SOLUK}">Kalın çerçeve: rotada karşımıza çıkanlar · boraksta Na, deniz suyunda Mg ve Cl · Kütahya’nın kobaltı · Seydişehir’in alüminyumu</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


def _atom_kabuk(cx, cy, p, dizi, renk, r0=24, ara=22, e_r=6.5, eklenen=0, giden=0):
    o = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{r0 - 4}" fill="{renk}" stroke="{OBS}" stroke-width="2.2"/>',
         f'<text x="{f(cx)}" y="{f(cy + 8)}" text-anchor="middle" {B} font-size="22" fill="#FFFFFF">{p}+</text>']
    for k, n in enumerate(dizi):
        r = r0 + 8 + k * ara
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{GUM_K}" stroke-width="1.8"/>')
        for j in range(n):
            a = -math.pi / 2 + 2 * math.pi * j / max(n, 1) + (.2 if k % 2 else 0)
            yeni = k == len(dizi) - 1 and j >= n - eklenen
            o.append(f'<circle cx="{f(cx + r * math.cos(a))}" cy="{f(cy + r * math.sin(a))}" r="{e_r}" fill="{MER if yeni else KOB}" stroke="{OBS}" stroke-width="1.4"/>')
    return "".join(o)


def iyon_olusumu(onek="pt-iyn"):
    """Na → Na⁺ + e⁻ (Ne düzeni) ve Cl + e⁻ → Cl⁻ (Ar düzeni): katman modelleri."""
    s = Svg(onek)
    W, H = 1060, 500
    # üst satır: sodyum
    y1, y2 = 120, 360
    s += _atom_kabuk(110, y1, 11, [2, 8, 1], "#8E5BD0")
    s += _alt("Na", 110, y1 + 112, 30, OBS)
    s += f'<text x="110" y="{y1 + 140}" text-anchor="middle" {T9} font-size="24" fill="{KOB_K}">2 · 8 · 1</text>'
    s += _ok(220, y1, 330, y1, OBS, 4, 16)
    s += _alt("1 e^{−} verir", 275, y1 - 16, 24, MER_K, font=T9)
    s += _atom_kabuk(430, y1, 11, [2, 8], "#8E5BD0")
    s += _alt("Na^{+}", 430, y1 + 112, 30, OBS)
    s += f'<text x="430" y="{y1 + 140}" text-anchor="middle" {T9} font-size="24" fill="{KOB_K}">2 · 8 (Ne gibi)</text>'
    s += f'<text x="540" y="{y1 + 10}" {B} font-size="34" fill="{OBS}">+</text>'
    s += f'<circle cx="600" cy="{y1}" r="13" fill="{MER}" stroke="{OBS}" stroke-width="1.6"/>'
    s += _alt("e^{−}", 640, y1 + 10, 30, OBS, "start")
    # alt satır: klor
    s += _atom_kabuk(110, y2, 17, [2, 8, 7], "#39A85A")
    s += _alt("Cl", 110, y2 + 112, 30, OBS)
    s += f'<text x="110" y="{y2 + 140}" text-anchor="middle" {T9} font-size="24" fill="{KOB_K}">2 · 8 · 7</text>'
    s += f'<text x="215" y="{y2 + 10}" {B} font-size="34" fill="{OBS}">+</text>'
    s += f'<circle cx="262" cy="{y2}" r="13" fill="{MER}" stroke="{OBS}" stroke-width="1.6"/>'
    s += _alt("e^{−}", 282, y2 + 10, 28, OBS, "start")
    s += _ok(320, y2, 380, y2, OBS, 4, 16)
    s += f'<text x="350" y="{y2 - 16}" text-anchor="middle" {T9} font-size="24" fill="{MER_K}">alır</text>'
    s += _atom_kabuk(490, y2, 17, [2, 8, 8], "#39A85A", eklenen=1)
    s += _alt("Cl^{−}", 490, y2 + 112, 30, OBS)
    s += f'<text x="490" y="{y2 + 140}" text-anchor="middle" {T9} font-size="24" fill="{KOB_K}">2 · 8 · 8 (Ar gibi)</text>'
    # sağ kutu: değişmeyenler / değişenler
    bx, by = 720, 210
    s += _kutu(bx, by, 330, 280, "#FFFFFF", OBS, 16, 2.6)
    s += f'<text x="{bx + 18}" y="{by + 38}" {T9} font-size="21" fill="{ZUMRUT}" letter-spacing="1">DEĞİŞMEZ</text>'
    for k, t in enumerate(("proton sayısı", "nötron sayısı", "çekirdek")):
        s += f'<text x="{bx + 18}" y="{by + 74 + k * 32}" {T} font-size="26" fill="{OBS}">• {t}</text>'
    s += f'<text x="{bx + 18}" y="{by + 178}" {T9} font-size="21" fill="{MER_K}" letter-spacing="1">DEĞİŞİR</text>'
    for k, t in enumerate(("elektron sayısı, dizilim", "kimyasal özellik")):
        s += f'<text x="{bx + 18}" y="{by + 214 + k * 32}" {T} font-size="26" fill="{OBS}">• {t}</text>'
    s += _alt("Na^{+}: 10 e^{−} · Cl^{−}: 18 e^{−}", bx + 165, 70, 27, KOB_K, font=T9)
    s += f'<text x="{bx + 165}" y="110" text-anchor="middle" {T} font-size="22" fill="{SOLUK}">yük = p − e</text>'
    s += f'<text x="{bx + 165}" y="140" text-anchor="middle" {T} font-size="22" fill="{SOLUK}">11 − 10 = 1+ · 17 − 18 = 1−</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ================================================================== soru şekilleri (kıssa, imtihan, üstad)

def triad_grafik(onek="pt-tri"):
    """Kıssa 2: Cl–Br–I üçlüsünün atom kütleleri; Br silinmiş."""
    s = Svg(onek)
    W, H = 620, 420
    x0, y0, y1 = 96, 30, 340
    s += f'<path d="M{x0} {y0} V{y1} H{W - 20}" stroke="{OBS}" stroke-width="3.2" fill="none"/>'
    for v in (0, 40, 80, 120):
        y = y1 - (y1 - y0 - 20) * v / 130
        s += f'<path d="M{x0 - 8} {f(y)} H{W - 20}" stroke="{GUM}" stroke-width="1.4" stroke-dasharray="5 5"/>'
        s += f'<text x="{x0 - 14}" y="{f(y + 8)}" text-anchor="end" {T9} font-size="22" fill="{GUM_K}">{v}</text>'
    for i, (sem, v, renk) in enumerate((("Cl", 35.5, "#39A85A"), ("Br", None, "#C4572E"), ("I", 127, "#7B3F8C"))):
        x = x0 + 50 + i * 160
        if v is None:
            hgt = (y1 - y0 - 20) * 80 / 130
            s += f'<rect x="{x}" y="{f(y1 - hgt)}" width="96" height="{f(hgt)}" fill="#FFFFFF" stroke="{renk}" stroke-width="3" stroke-dasharray="9 6"/>'
            s += f'<text x="{x + 48}" y="{f(y1 - hgt / 2 + 16)}" text-anchor="middle" {B} font-size="46" fill="{renk}">?</text>'
        else:
            hgt = (y1 - y0 - 20) * v / 130
            s += f'<rect x="{x}" y="{f(y1 - hgt)}" width="96" height="{f(hgt)}" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>'
            s += f'<text x="{x + 48}" y="{f(y1 - hgt - 10)}" text-anchor="middle" {B} font-size="28" fill="{OBS}">{str(v).replace(".", ",")}</text>'
        s += f'<text x="{x + 48}" y="{y1 + 36}" text-anchor="middle" {B} font-size="32" fill="{OBS}">{sem}</text>'
    s += f'<text x="22" y="{(y0 + y1) / 2}" text-anchor="middle" {T9} font-size="21" fill="{GUM_K}" transform="rotate(-90 22 {(y0 + y1) / 2})">atom kütlesi</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def iskelet(onek="pt-isk"):
    """İmtihan 10: ilk dört periyodun iskeleti; X, Y, Z, T, Q harfleri."""
    s = Svg(onek)
    X0, Y0, CW, RH, W_ = 44, 40, 50, 48, 45
    harf = {(2, 1): "X", (4, 9): "Y", (3, 13): "Z", (4, 2): "T", (2, 18): "Q"}
    W, H = X0 + 18 * CW + 8, Y0 + 4 * RH + 6
    for z in range(1, 37):
        p, g = TV.yer(z)
        x, y = X0 + (g - 1) * CW, Y0 + (p - 1) * RH
        h = harf.get((p, g))
        s += f'<rect x="{x}" y="{y}" width="{W_}" height="{RH - 5}" rx="5" fill="{"#FDE7E1" if h else "#FFFFFF"}" stroke="{GUM_K}" stroke-width="1.8"/>'
        if h:
            s += f'<text x="{x + W_ / 2}" y="{y + 32}" text-anchor="middle" {B} font-size="31" fill="{MER_K}">{h}</text>'
    for g in (1, 2, 13, 14, 15, 16, 17, 18):
        s += f'<text x="{X0 + (g - 1) * CW + W_ / 2}" y="{Y0 - 12}" text-anchor="middle" {T9} font-size="19" fill="{GUM_K}">{TV.ab_adi(g)}</text>'
    for p in range(1, 5):
        s += f'<text x="{X0 - 22}" y="{Y0 + (p - 1) * RH + 30}" text-anchor="middle" {B} font-size="24" fill="{LAJVER}">{p}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info")


def ustad_grafik(onek="pt-ugr"):
    """Üstad 3: katman sayısı (x) ve değerlik elektron sayısı (y); X, Y, Z, T nötr atomları."""
    s = Svg(onek)
    W, H = 500, 440
    x0, y0, x1, y1 = 70, 24, 486, 360
    nx, ny = 4, 8

    def P(k, d):
        return x0 + (x1 - x0) * k / (nx + .4), y1 - (y1 - y0) * d / (ny + .6)
    s += f'<path d="M{x0} {y0} V{y1} H{x1}" stroke="{OBS}" stroke-width="3.4" fill="none"/>'
    for d in range(1, ny + 1):
        _, y = P(0, d)
        s += f'<path d="M{x0 - 7} {f(y)} H{x1}" stroke="{GUM}" stroke-width="1.4" stroke-dasharray="4 5"/>'
        if d % 2 == 0 or d in (3,):
            s += f'<text x="{x0 - 12}" y="{f(y + 10)}" text-anchor="end" {T9} font-size="28" fill="{GUM_K}">{d}</text>'
    for k in range(1, nx + 1):
        x, _ = P(k, 0)
        s += f'<path d="M{f(x)} {y1} V{y1 + 8}" stroke="{OBS}" stroke-width="2.6"/>'
        s += f'<text x="{f(x)}" y="{y1 + 38}" text-anchor="middle" {T9} font-size="30" fill="{OBS}">{k}</text>'
    for (ad, k, d) in (("X", 2, 3), ("Y", 3, 3), ("Z", 3, 6), ("T", 4, 2)):
        x, y = P(k, d)
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="17" fill="{LAJVER}" stroke="{OBS}" stroke-width="2"/>'
        s += f'<text x="{f(x + 22)}" y="{f(y - 10)}" {B} font-size="38" fill="{LAJVER}">{ad}</text>'
    s += f'<text x="{(x0 + x1) / 2}" y="{H - 6}" text-anchor="middle" {T9} font-size="27" fill="{GUM_K}">katman sayısı</text>'
    s += f'<text x="22" y="{(y0 + y1) / 2}" text-anchor="middle" {T9} font-size="27" fill="{GUM_K}" transform="rotate(-90 22 {(y0 + y1) / 2})">değerlik e<tspan dy="-9" font-size="18">−</tspan></text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


MECLIS_DENETIM = [
    ("Nötr atom mu?", ["Yer iyondan değil,", "atomdan: O^{2−} değil O"]),
    ("Sıra doğru mu?", ["4s, 3d’den önce:", "K 2 · 8 · 8 · 1"]),
    ("Son orbital d mi?", ["d ile biten B grubu:", "Ni → 8B"]),
    ("Helyum mu?", ["1s^{2} ama soy gaz:", "He → 8A"]),
    ("Kutu var mı?", ["3. periyotta 3B yok,", "8A’da metal yok"]),
]


def meclis_denetim(onek="pt-mcd"):
    """Meclis: bir yer bulma çözümünü denetlemenin beş sorusu (hata avı kontrol listesi)."""
    s = Svg(onek)
    W, H = 1860, 196
    n = len(MECLIS_DENETIM)
    tw = W / n
    renk = [MER, KOB, KEH_K, ERGUVAN, GOL_K]
    for i, (bas, satir) in enumerate(MECLIS_DENETIM):
        x = i * tw
        s += f'<rect x="{f(x + 8)}" y="10" width="{f(tw - 16)}" height="{H - 20}" rx="18" fill="#FFFFFF" stroke="{renk[i]}" stroke-width="3"/>'
        s += _yildiz_rozet(x + 50, 52, 28, str(i + 1), renk[i], fs=28)
        s += f'<text x="{f(x + 90)}" y="64" {B} font-size="32" fill="{OBS}">{bas}</text>'
        for k, t in enumerate(satir):
            s += _alt(t, x + 28, 118 + k * 36, 27, "#343947", "start", font=T)
        if i < n - 1:
            ax = x + tw - 4
            s += f'<path d="M{f(ax - 10)} 84 L{f(ax + 6)} 99 L{f(ax - 10)} 114" stroke="{ALTIN_K}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info")
