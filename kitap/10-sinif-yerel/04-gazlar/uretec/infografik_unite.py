"""Gazlar · Kapadokya Yolu — üniteye özel bilgi grafikleri ({{info|ad|arg…}}; kur_ortak ortak infografik.py'den ÖNCE bakar).

Bütün sayılar uretec/dogrula.py içinde yeniden hesaplanır; burada yalnız çizim vardır. Yazılarda alt/üst simge tspan ile
(_yazi: "CO_2", "P_0", "10^{23}"); konturlu yazı yok; fontta olmayan sembol (→ ∝ ϑ) kullanılmaz, oklar path ile çizilir.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, GOL_AA, DERIN, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A,
                           ALTIN, ALTIN_K, ALTIN_A, LAJVER, ZUMRUT, GUM, GUM_K, GUM_A, ERGUVAN)
from cizim import sahne as S
import sahneler_unite as SU

T = 'font-family="Nunito" font-weight="800"'
TK = 'font-family="Nunito" font-weight="900"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'


def _tsp(metin, fs):
    """'CO_2', 'P_{gaz}', '10^{23}' → tspan'lı SVG metni (alt/üst simge, sonra taban çizgisine dönüş)."""
    out, i, geri = [], 0, 0.0
    while i < len(metin):
        c = metin[i]
        if c in "_^" and i + 1 < len(metin):
            if metin[i + 1] == "{":
                j = metin.index("}", i + 2)
                parca, i = metin[i + 2:j], j + 1
            else:
                parca, i = metin[i + 1], i + 2
            dy = fs * (.3 if c == "_" else -.42) - geri
            out.append(f'<tspan dy="{f(dy, 2)}" font-size="{f(fs * .66, 2)}">{parca}</tspan>')
            geri = fs * (.3 if c == "_" else -.42)
        else:
            j = i
            while j < len(metin) and metin[j] not in "_^":
                j += 1
            run = metin[i:j]
            out.append(f'<tspan dy="{f(-geri, 2)}">{run}</tspan>' if geri else run)
            geri = 0.0
            i = j
    return "".join(out)


def _yazi(x, y, metin, fs, renk=OBS, anchor="middle", font=T, ek=""):
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(fs)}" fill="{renk}"{ek}>{_tsp(metin, fs)}</text>'


def _ok(x1, y1, x2, y2, renk, k=3.0, uc=10):
    """Düz ok (gövde + dolu uç)."""
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - uc * math.cos(a), y2 - uc * math.sin(a)
    p1 = (bx + uc * .55 * math.sin(a), by - uc * .55 * math.cos(a))
    p2 = (bx - uc * .55 * math.sin(a), by + uc * .55 * math.cos(a))
    return (f'<path d="M{f(x1)} {f(y1)} L{f(bx)} {f(by)}" stroke="{renk}" stroke-width="{f(k)}" stroke-linecap="round"/>'
            f'<path d="M{f(x2)} {f(y2)} L{f(p1[0])} {f(p1[1])} L{f(p2[0])} {f(p2[1])} Z" fill="{renk}"/>')


def _eksen(s, x0, y0, x1, y1, xt, yt, xad, yad, fs=26, izgara=True):
    """Grafik ekseni. xt/yt: [(değer_konumu_px, etiket)]."""
    o = []
    if izgara:
        for px, _ in xt:
            o.append(f'<path d="M{f(px)} {f(y0)} V{f(y1)}" stroke="#DCE4E8" stroke-width="2"/>')
        for py, _ in yt:
            o.append(f'<path d="M{f(x0)} {f(py)} H{f(x1)}" stroke="#DCE4E8" stroke-width="2"/>')
    o.append(f'<path d="M{f(x0)} {f(y1 - 12)} V{f(y0)} H{f(x1 + 12)}" stroke="{OBS}" stroke-width="3.6" fill="none"/>')
    o.append(f'<path d="M{f(x0 - 8)} {f(y1 - 8)} L{f(x0)} {f(y1 - 22)} L{f(x0 + 8)} {f(y1 - 8)} Z M{f(x1 + 8)} {f(y0 - 8)} L{f(x1 + 22)} {f(y0)} L{f(x1 + 8)} {f(y0 + 8)} Z" fill="{OBS}"/>')
    for px, et in xt:
        o.append(_yazi(px, y0 + fs + 6, et, fs, GUM_K))
    for py, et in yt:
        o.append(_yazi(x0 - 10, py + fs * .35, et, fs, GUM_K, "end"))
    o.append(_yazi(x1 + 18, y0 + fs * 2.2, xad, fs, OBS, "end"))
    o.append(_yazi(x0 + 6, y1 - 30, yad, fs, OBS, "start"))
    return "".join(o)


# ------------------------------------------------------------------ 1. DURAK

def tanecik_kutulari(onek="gi-tan"):
    """Katı · sıvı · gaz: tanecik düzeni (gazda uzak, hızlı, rastgele)."""
    s = Svg(onek)
    W, H = 640, 250
    r = RNG(5)
    for k, (ad, alt) in enumerate((("KATI", "düzenli, titreşir"), ("SIVI", "yakın, kayar"), ("GAZ", "uzak, hızlı, rastgele"))):
        x0 = 14 + k * 212
        s += f'<rect x="{x0}" y="8" width="186" height="172" rx="16" fill="{["#EEF2F6", "#E6F4F7", "#FFF4E6"][k]}" stroke="{OBS}" stroke-width="3"/>'
        pts = []
        if k == 0:
            pts = [(x0 + 38 + i * 37, 46 + j * 37) for j in range(4) for i in range(4)]
        elif k == 1:
            for j in range(3):
                for i in range(5):
                    pts.append((x0 + 26 + i * 33 + r.uniform(-4, 4) + (j % 2) * 10, 160 - j * 31 + r.uniform(-4, 4)))
        else:
            pts = [(x0 + 40, 44), (x0 + 140, 38), (x0 + 92, 92), (x0 + 152, 140), (x0 + 44, 150), (x0 + 110, 158)]
        for (px, py) in pts:
            s += f'<circle cx="{f(px)}" cy="{f(py)}" r="14" fill="{GOL}" stroke="{OBS}" stroke-width="2.4"/><circle cx="{f(px - 4)}" cy="{f(py - 5)}" r="4" fill="#FFFFFF" opacity=".7"/>'
        if k == 2:
            for (px, py), (dx, dy) in zip(pts, ((34, 18), (-30, 10), (8, -36), (10, -38), (-8, -40), (36, -4))):
                s += _ok(px + dx * .45, py + dy * .45, px + dx * 1.25, py + dy * 1.25, MER, 3.4, 11)
        s += _yazi(x0 + 93, 214, ad, 30, OBS, font=B)
        s += _yazi(x0 + 93, 242, alt, 21, GUM_K)
    return s.cikti(f"0 0 {W} {H}", cls="info")


def barometreler(onek="gi-bar"):
    """Yükseldikçe cıva sütunu kısalır: deniz kıyısı 76 cm · Kayseri ≈ 67 cm · Erciyes zirvesi ≈ 47 cm (standart atmosfer, yaklaşık)."""
    s = Svg(onek)
    W, H = 760, 360
    g = s.lin([(0, "#BFE3F7"), (1, "#F2FAFD")], 0, 0, 0, 1, ad="gk")
    s += f'<rect width="{W}" height="{H}" rx="20" fill="{g}"/>'
    # arazi: deniz (sol), ova (orta), Erciyes (sağ)
    s += f'<path d="M0 300 H190 V{H} H0 Z" fill="#3DB7C4"/><path d="M14 312 h60 M100 326 h50" stroke="#FFFFFF" stroke-width="4" opacity=".7"/>'
    s += f'<path d="M190 300 C260 292 400 290 470 284 C520 250 560 160 640 70 C660 52 676 52 690 70 C720 110 740 180 760 230 V{H} H190 Z" fill="#9DBB6A"/>'
    s += f'<path d="M608 108 C630 82 650 60 664 58 C680 60 700 86 716 116 C700 108 690 118 676 104 C664 116 650 104 636 118 C626 108 618 116 608 108 Z" fill="#FFFFFF"/>'
    s += f'<path d="M470 284 C520 250 560 160 640 70 C660 52 676 52 690 70 C720 110 740 180 760 230 V300 H470 Z" fill="#7B8DB4" opacity=".55"/>'
    cm = 76
    olc = 2.55   # birim / cm
    for k, (x, ad, yuk, deger, atm) in enumerate(((105, "Deniz kıyısı", "0 m", 76, "1 atm"), (330, "Kayseri", "≈ 1 050 m", 67, "≈ 0,88 atm"),
                                                    (560, "Erciyes zirvesi", "≈ 3 917 m", 47, "≈ 0,62 atm"))):
        taban = 330
        ust = taban - cm * olc - 40
        s += f'<rect x="{x - 44}" y="{taban - 24}" width="88" height="26" rx="6" fill="#C9D2DA" stroke="{OBS}" stroke-width="3"/>'
        s += f'<rect x="{x - 38}" y="{taban - 18}" width="76" height="14" fill="#8C99A6"/>'
        s += f'<rect x="{x - 13}" y="{ust}" width="26" height="{taban - 10 - ust}" rx="13" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
        hg = deger * olc
        gm = s.lin([(0, "#E9EEF2"), (.5, "#A7B3BE"), (1, "#6E7C88")], 0, 0, 1, 0, ad="hg")
        s += f'<rect x="{x - 9}" y="{f(taban - 12 - hg)}" width="18" height="{f(hg + 2)}" fill="{gm}"/>'
        s += f'<path d="M{x + 18} {f(taban - 12 - hg)} H{x + 34} M{x + 26} {f(taban - 12 - hg)} V{taban - 12} M{x + 18} {taban - 12} H{x + 34}" stroke="{MER}" stroke-width="3"/>'
        s += _yazi(x + 40, taban - 12 - hg / 2 + 10, f"{'≈ ' if k else ''}{deger} cm", 26, MER_K, "start", font=B)
        s += _yazi(x, 34, ad, 24, OBS, font=B)
        s += _yazi(x, 58, yuk + " · " + atm, 19, GUM_K)
    return s.cikti(f"0 0 {W} {H}", cls="info")


def manometre(onek="gi-man", h=9, yon="acik", etiket=""):
    """Açık uçlu manometre. yon='acik': cıva açık kolda h kadar yüksek (P_gaz = P_0 + h); 'gaz': gaz kolunda yüksek (P_0 − h)."""
    s = Svg(onek)
    W, H = 380, 330
    k = 6.0
    s += f'<rect x="18" y="70" width="120" height="110" rx="30" fill="{GOL_A}" stroke="{OBS}" stroke-width="3.4"/>'
    s += _yazi(78, 120, "gaz", 30, GOL_K, font=B)
    if etiket:
        s += _yazi(78, 150, etiket, 20, GUM_K)
    xl, xr, alt = 200, 300, 300
    boru = f"M138 125 H{xl} V{alt} H{xr} V40"
    s += f'<path d="{boru}" fill="none" stroke="{OBS}" stroke-width="26" stroke-linejoin="round"/><path d="{boru}" fill="none" stroke="#FFFFFF" stroke-width="18" stroke-linejoin="round"/>'
    orta = 220
    yl = orta + (h * k / 2 if yon == "acik" else -h * k / 2)
    yr = orta - (h * k / 2 if yon == "acik" else -h * k / 2)
    gm = "#9AA6B2"
    s += f'<path d="M{xl} {f(yl)} V{alt} H{xr} V{f(yr)}" fill="none" stroke="{gm}" stroke-width="18"/>'
    s += f'<path d="M{xl - 30} {f(yl)} H{xr + 30}" stroke="{KEH_K}" stroke-width="2" stroke-dasharray="6 5"/>' if yon == "acik" else \
         f'<path d="M{xl - 30} {f(yr)} H{xr + 30}" stroke="{KEH_K}" stroke-width="2" stroke-dasharray="6 5"/>'
    ust_y, alt_y = min(yl, yr), max(yl, yr)
    xh = xr + 34 if yon == "acik" else xl - 34
    s += f'<path d="M{xh} {f(ust_y)} V{f(alt_y)} M{xh - 8} {f(ust_y)} H{xh + 8} M{xh - 8} {f(alt_y)} H{xh + 8}" stroke="{MER}" stroke-width="3.4"/>'
    s += _yazi(xh + (12 if yon == "acik" else -12), (ust_y + alt_y) / 2 + 10, f"h = {h} cm", 26, MER_K, "start" if yon == "acik" else "end", font=B)
    s += _ok(xr, 0, xr, 30, KOB, 4, 13)
    s += _yazi(xr - 22, 22, "P_0", 28, KOB_K, "end", font=B)
    s += _yazi(250, 326, "açık uçlu manometre", 20, GUM_K)
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ------------------------------------------------------------------ 2. DURAK

def grafik_boyle(onek="gi-boy"):
    s = Svg(onek)
    W, H = 470, 360
    x0, y0, x1, y1 = 80, 290, 440, 40
    X = lambda v: x0 + (x1 - x0) * v / 8   # noqa: E731
    Y = lambda p: y0 - (y0 - y1) * p / 4   # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += _eksen(s, x0, y0, x1, y1, [(X(v), str(v)) for v in (2, 4, 6, 8)], [(Y(p), str(p)) for p in (1, 2, 3, 4)], "V (L)", "P (atm)")
    s += _yazi(x0 - 10, y0 + 9, "0", 26, GUM_K, "end")
    pts = [(X(v), Y(4 / v)) for v in [1 + i * .125 for i in range(57)]]
    s += f'<path d="{cizgi_d(pts)}" fill="none" stroke="{GOL}" stroke-width="6" stroke-linecap="round"/>'
    for v, p in ((1, 4), (2, 2), (4, 1)):
        s += f'<path d="M{f(X(v))} {f(y0)} V{f(Y(p))} H{f(x0)}" stroke="{GOL_K}" stroke-width="2" stroke-dasharray="6 5" fill="none"/>'
        s += f'<circle cx="{f(X(v))}" cy="{f(Y(p))}" r="9" fill="#FFFFFF" stroke="{GOL_K}" stroke-width="5"/>'
    s += f'<rect x="{f(X(4.1))}" y="{f(Y(3.6))}" width="196" height="44" rx="10" fill="{KEH_A}" stroke="{KEH_K}" stroke-width="2.4"/>'
    s += _yazi(X(4.1) + 98, Y(3.6) + 31, "P·V = 4 (sabit)", 26, KEH_K, font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def grafik_charles(onek="gi-cha"):
    s = Svg(onek)
    W, H = 480, 360
    x0, y0, x1, y1 = 30, 290, 450, 40
    X = lambda t: x0 + (x1 - x0) * (t + 300) / 600   # noqa: E731
    Y = lambda v: y0 - (y0 - y1) * v / 50            # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    xs = X(0)
    for v in (22.4, 44.8):
        s += f'<path d="M{f(x0)} {f(Y(v))} H{f(x1)}" stroke="#DCE4E8" stroke-width="2"/>'
    s += f'<path d="M{f(xs)} {f(y1 - 12)} V{f(y0 + 6)} M{f(x0)} {f(y0)} H{f(x1 + 12)}" stroke="{OBS}" stroke-width="3.6"/>'
    s += f'<path d="M{f(x1 + 8)} {f(y0 - 8)} L{f(x1 + 22)} {f(y0)} L{f(x1 + 8)} {f(y0 + 8)} Z M{f(xs - 8)} {f(y1 - 8)} L{f(xs)} {f(y1 - 22)} L{f(xs + 8)} {f(y1 - 8)} Z" fill="{OBS}"/>'
    s += f'<path d="M{f(X(-273))} {f(Y(0))} L{f(X(0))} {f(Y(22.4))}" stroke="{MER}" stroke-width="5" stroke-dasharray="12 9"/>'
    s += f'<path d="M{f(X(0))} {f(Y(22.4))} L{f(X(273))} {f(Y(44.8))}" stroke="{MER}" stroke-width="6" stroke-linecap="round"/>'
    for t, v in ((0, 22.4), (273, 44.8)):
        s += f'<circle cx="{f(X(t))}" cy="{f(Y(v))}" r="9" fill="#FFFFFF" stroke="{MER_K}" stroke-width="5"/>'
    s += f'<circle cx="{f(X(-273))}" cy="{f(Y(0))}" r="11" fill="{MER}" stroke="{OBS}" stroke-width="3"/>'
    s += _yazi(X(-273), y0 + 34, "−273", 26, MER_K, font=B)
    s += _yazi(X(0), y0 + 34, "0", 26, GUM_K)
    s += _yazi(X(273), y0 + 34, "273", 26, GUM_K)
    s += _yazi(xs + 10, Y(22.4) + 34, "22,4", 24, GUM_K, "start")
    s += _yazi(xs - 10, Y(44.8) + 9, "44,8", 24, GUM_K, "end")
    s += _yazi(x1 + 18, y0 + 66, "t (°C)", 26, OBS, "end")
    s += _yazi(xs + 10, y1 - 26, "V (L)", 26, OBS, "start")
    s += _yazi(X(-273) + 6, Y(9), "mutlak sıfır", 24, MER_K, "start", font=B)
    s += _yazi(X(-273) + 6, Y(9) + 28, "0 K", 24, MER_K, "start", font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def paket_boyle(onek="gi-pak"):
    """Ağzı kapalı esnek paket: yerde 0,9 atm · 2,0 L → yükseklerde 0,75 atm · 2,4 L."""
    s = Svg(onek)
    W, H = 520, 260
    for k, (x, ad, p, v, sk) in enumerate(((120, "Göreme · yerde", "0,9 atm", "2,0 L", 1.0), (390, "balon yükselince", "0,75 atm", "2,4 L", 1.2))):
        w, h = 120 * sk ** .5, 150 * sk ** .5
        cy = 120
        pts = [(x - w / 2, cy - h / 2), (x + w / 2, cy - h / 2), (x + w / 2 + 8 * (sk - 1) * 10, cy), (x + w / 2, cy + h / 2), (x - w / 2, cy + h / 2), (x - w / 2 - 8 * (sk - 1) * 10, cy)]
        d = egri_d(pts, True, .7)
        g = s.lin([(0, "#FFE08A"), (1, "#F0A21A")], 0, 0, 1, 1, ad="pk")
        s += f'<path d="{d}" fill="{g}" stroke="{OBS}" stroke-width="3.4"/>'
        for yy in (cy - h / 2 + 6, cy + h / 2 - 6):
            s += f'<path d="M{f(x - w / 2 + 4)} {f(yy)} ' + " ".join(f"l6 {(-5 if i % 2 else 5)}" for i in range(int(w / 6) - 1)) + f'" stroke="{KEH_K}" stroke-width="2.4" fill="none"/>'
        s += f'<circle cx="{f(x)}" cy="{cy}" r="{f(30 * sk ** .5)}" fill="#FFFFFF" stroke="{MER}" stroke-width="3"/>'
        s += _yazi(x, cy + 10, v, 26, MER_K, font=B)
        s += _yazi(x, 238, ad, 22, OBS, font=B)
        s += _yazi(x, 22, p, 22, KOB_K, font=B)
    s += _ok(220, 120, 290, 120, GOL_K, 5, 18)
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ------------------------------------------------------------------ 3. DURAK

def grafik_gay(onek="gi-gay"):
    s = Svg(onek)
    W, H = 470, 340
    x0, y0, x1, y1 = 80, 280, 440, 40
    X = lambda t: x0 + (x1 - x0) * t / 500   # noqa: E731
    Y = lambda p: y0 - (y0 - y1) * p / 2     # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += _eksen(s, x0, y0, x1, y1, [(X(t), str(t)) for t in (150, 300, 450)], [(Y(p), str(p).replace(".", ",")) for p in (0.5, 1, 1.5, 2)], "T (K)", "P (atm)")
    s += f'<path d="M{f(X(0))} {f(Y(0))} L{f(X(500))} {f(Y(500 / 300))}" stroke="{ERGUVAN}" stroke-width="6" stroke-linecap="round"/>'
    for t, p in ((300, 1), (450, 1.5)):
        s += f'<path d="M{f(X(t))} {f(y0)} V{f(Y(p))} H{f(x0)}" stroke="{ERGUVAN}" stroke-width="2" stroke-dasharray="6 5" fill="none"/>'
        s += f'<circle cx="{f(X(t))}" cy="{f(Y(p))}" r="9" fill="#FFFFFF" stroke="{ERGUVAN}" stroke-width="5"/>'
    s += f'<rect x="{f(X(30))}" y="{f(Y(1.95))}" width="180" height="44" rx="10" fill="#F1E6F5" stroke="{ERGUVAN}" stroke-width="2.4"/>'
    s += _yazi(X(30) + 90, Y(1.95) + 31, "P / T = sabit", 26, ERGUVAN, font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def testiler(onek="gi-tes"):
    """Avogadro: aynı P ve T'de eşit hacimli üç testi: tanecik sayıları eşit, kütleler farklı."""
    s = Svg(onek)
    W, H = 640, 330
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#FFF6EC"/>'
    s += f'<rect x="150" y="10" width="340" height="40" rx="20" fill="{KEH_A}" stroke="{KEH_K}" stroke-width="2.4"/>'
    s += _yazi(320, 39, "NŞA · 5,6’şar L · 0,25’er mol", 24, KEH_K, font=B)
    yer = [(-34, -40), (30, -52), (-8, 0), (36, 18), (-30, 40)]
    for k, (ad, kutle, renk) in enumerate((("He", "1 g", "#5ED3F3"), ("N_2", "7 g", KOB), ("CO_2", "11 g", "#3A3F4B"))):
        x = 110 + k * 210
        s += SU.testi(s, x, 268, 200, renk=["#C8743A", SU.KIL, "#A84A2A"][k], tohum=900 + k, desen=False)
        s += f'<ellipse cx="{x}" cy="{180}" rx="58" ry="66" fill="#FFF8EE" opacity=".93"/>'
        for dx, dy in yer:
            cx, cy = x + dx, 180 + dy
            if k == 0:
                s += f'<circle cx="{cx}" cy="{cy}" r="9" fill="{renk}" stroke="{OBS}" stroke-width="2"/>'
            elif k == 1:
                s += f'<circle cx="{cx - 7}" cy="{cy}" r="9" fill="{renk}" stroke="{OBS}" stroke-width="2"/><circle cx="{cx + 7}" cy="{cy}" r="9" fill="{renk}" stroke="{OBS}" stroke-width="2"/>'
            else:
                s += (f'<circle cx="{cx - 13}" cy="{cy}" r="8" fill="{MER}" stroke="{OBS}" stroke-width="2"/><circle cx="{cx + 13}" cy="{cy}" r="8" fill="{MER}" stroke="{OBS}" stroke-width="2"/>'
                      f'<circle cx="{cx}" cy="{cy}" r="9" fill="{renk}" stroke="{OBS}" stroke-width="2"/>')
        s += _yazi(x, 300, ad, 30, OBS, font=B)
        s += _yazi(x, 324, kutle, 22, MER_K, font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info")


def kucuk_gl(onek="gi-kgl"):
    """Ağzı kapalı testi fırında: 300 K'de 1 atm → 450 K'de 1,5 atm (sabit hacim)."""
    s = Svg(onek)
    W, H = 420, 250
    for k, (x, T_, P_, alev) in enumerate(((100, "300 K", "1 atm", False), (310, "450 K", "1,5 atm", True))):
        if alev:
            gl = s.rad([(0, "#FFE08A", .9), (1, "#FF7A3D", 0)], x, 210, 90, kull="userSpaceOnUse", ad="al")
            s += f'<circle cx="{x}" cy="210" r="90" fill="{gl}"/>'
            s += f'<path d="M{x - 40} 236 Q{x - 30} 200 {x - 10} 196 Q{x} 214 {x + 6} 192 Q{x + 24} 210 {x + 40} 236 Z" fill="#FF8A3D"/>'
        s += SU.testi(s, x, 222, 150, renk=SU.KIL, tohum=930 + k, desen=False, kulp=False)
        s += f'<ellipse cx="{x}" cy="72" rx="20" ry="7" fill="#5A3A22"/>'
        n = 6
        r = RNG(940 + k)
        for i in range(n):
            px, py = x + r.uniform(-34, 34), 150 + r.uniform(-32, 40)
            s += f'<circle cx="{f(px)}" cy="{f(py)}" r="7" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
            if alev:
                a = r.uniform(0, 6.28)
                s += _ok(px + 9 * math.cos(a), py + 9 * math.sin(a), px + 30 * math.cos(a), py + 30 * math.sin(a), "#FFE08A", 3, 9)
        s += _yazi(x, 30, T_ + " · " + P_, 24, MER_K if alev else KOB_K, font=B)
    s += _ok(170, 150, 240, 150, GOL_K, 5, 16)
    return s.cikti(f"0 0 {W} {H}", cls="info")


def buhar_carki(onek="gi-buh"):
    """Takiyüddin'in buharla dönen şişi (temsilî): ağzı kapalı bakır ibrik ateşte, borudan çıkan buhar kanatlı çarkı çevirir."""
    s = Svg(onek)
    W, H = 340, 270
    g = s.lin([(0, "#FFF4DE"), (1, "#F6E2C0")], 0, 0, 0, 1, ad="zm")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{g}"/>'
    gl = s.rad([(0, "#FFE08A", .9), (1, "#FF7A3D", 0)], 90, 230, 80, kull="userSpaceOnUse", ad="at")
    s += f'<circle cx="90" cy="230" r="80" fill="{gl}"/>'
    s += f'<path d="M50 250 Q60 214 80 210 Q88 226 94 204 Q110 220 130 250 Z" fill="#FF8A3D"/><path d="M68 250 Q76 228 92 222 Q104 236 112 250 Z" fill="#FFE08A"/>'
    s += f'<path d="M40 254 H140" stroke="#5A3A22" stroke-width="8" stroke-linecap="round"/>'
    bk = s.lin([(0, "#F3B27A"), (.5, "#C8743A"), (1, "#7E3A1E")], 0, 0, 1, 0, ad="bk")
    s += f'<path d="M66 196 C34 190 34 120 70 108 V92 H110 V108 C146 120 146 190 114 196 Z" fill="{bk}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M110 120 C150 110 168 100 186 92" stroke="{OBS}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M110 120 C150 110 168 100 186 92" stroke="#C8743A" stroke-width="7" fill="none" stroke-linecap="round"/>'
    for k in range(4):
        s += f'<path d="M{196 + k * 10} {88 - k * 3} q8 -6 16 0" stroke="#FFFFFF" stroke-width="5" fill="none" opacity="{f(.9 - k * .15, 2)}" stroke-linecap="round"/>'
    cx, cy, R = 262, 82, 40
    for k in range(8):
        a = k * math.pi / 4
        s += f'<path d="M{f(cx)} {f(cy)} L{f(cx + R * math.cos(a))} {f(cy + R * math.sin(a))} L{f(cx + R * math.cos(a + .3))} {f(cy + R * math.sin(a + .3))} Z" fill="#9AA6B2" stroke="{OBS}" stroke-width="2"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="9" fill="{KEH}" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M{cx} {cy} V240" stroke="{OBS}" stroke-width="6"/><path d="M{cx - 70} 240 H{cx + 60}" stroke="{OBS}" stroke-width="6"/>'
    for k in range(4):
        s += f'<rect x="{cx - 60 + k * 26}" y="226" width="20" height="28" rx="6" fill="#B9532F" stroke="{OBS}" stroke-width="2"/>'
    s += _ok(150, 52, 214, 52, KOB, 3, 10)
    s += _yazi(150, 36, "buhar", 22, KOB_K, "start", font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ------------------------------------------------------------------ 4. DURAK

def balon_kesit(onek="gi-bal"):
    """Balon zarfının kesiti: içeride sıcak (87 °C), seyrek ve hızlı tanecikler; dışarıda serin (27 °C), sık ve yavaş."""
    s = Svg(onek)
    W, H = 560, 430
    g = s.lin([(0, "#D7EEFB"), (1, "#F4FBFE")], 0, 0, 0, 1, ad="gk")
    s += f'<rect width="{W}" height="{H}" rx="20" fill="{g}"/>'
    x, y, r = 280, 170, 132
    m = [SU._meridyen(x, y, r, 1), SU._meridyen(x, y, r, -1)]
    dis = egri_d(m[0]) + " L" + nok(m[1][-1]) + egri_d(list(reversed(m[1])), bas_m=False) + " Z"
    ic = s.rad([(0, "#FFE7C2"), (1, "#FFB98A")], .5, .4, .7, ad="ic")
    s += f'<path d="{dis}" fill="{ic}" stroke="{MER_K}" stroke-width="6"/>'
    rr = RNG(17)
    # dışarı: sık, yavaş (mavi)
    sayi = 0
    while sayi < 34:
        px, py = rr.uniform(16, W - 16), rr.uniform(16, H - 70)
        if (px - x) ** 2 / (r + 22) ** 2 + (py - y - 20) ** 2 / (r * 1.3 + 22) ** 2 < 1:
            continue
        s += f'<circle cx="{f(px)}" cy="{f(py)}" r="8" fill="{KOB}" stroke="{OBS}" stroke-width="2"/>'
        a = rr.uniform(0, 6.28)
        s += _ok(px + 10 * math.cos(a), py + 10 * math.sin(a), px + 24 * math.cos(a), py + 24 * math.sin(a), KOB_K, 2.4, 7)
        sayi += 1
    # içeri: seyrek, hızlı (mercan)
    for (px, py) in ((236, 92), (322, 112), (262, 168), (330, 196), (220, 214), (290, 248), (250, 120)):
        s += f'<circle cx="{px}" cy="{py}" r="8" fill="{MER}" stroke="{OBS}" stroke-width="2"/>'
        a = rr.uniform(0, 6.28)
        s += _ok(px + 10 * math.cos(a), py + 10 * math.sin(a), px + 46 * math.cos(a), py + 46 * math.sin(a), MER_K, 2.8, 9)
    # ağız: hava çıkışı + brülör
    my = y + r * 1.18
    s += _ok(x - 26, my - 8, x - 70, my + 34, MER_K, 3.4, 11)
    s += _ok(x + 26, my - 8, x + 70, my + 34, MER_K, 3.4, 11)
    s += f'<path d="M{x - 14} {my + 40} Q{x - 18} {my + 12} {x} {my - 18} Q{x + 18} {my + 12} {x + 14} {my + 40} Z" fill="#FF8A3D"/>'
    s += f'<rect x="{x - 40}" y="{my + 42}" width="80" height="40" rx="6" fill="#A9773F" stroke="#5A3A22" stroke-width="3"/>'
    s += f'<rect x="{x - 120}" y="{y - 26}" width="240" height="56" rx="12" fill="#FFFFFF" opacity=".88"/>'
    s += _yazi(x, y + 2, "içeride 87 °C", 26, MER_K, font=B)
    s += _yazi(x, y + 24, "seyrek · hızlı", 21, MER_K)
    s += f'<rect x="8" y="{H - 58}" width="222" height="46" rx="12" fill="#FFFFFF" opacity=".9"/>'
    s += _yazi(119, H - 37, "dışarıda 27 °C", 24, KOB_K, font=B)
    s += _yazi(119, H - 17, "sık · yavaş", 20, KOB_K)
    s += _yazi(W - 16, H - 22, "ağızdan hava çıkar", 21, MER_K, "end", font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ------------------------------------------------------------------ 5. DURAK

def yogunluk_cetveli(onek="gi-yog"):
    """Mol kütlesi cetveli: havadan (≈ 29) hafif gazlar yükselir, ağır gazlar aşağıda birikir (aynı P ve T)."""
    s = Svg(onek)
    W, H = 760, 260
    x0, x1, y = 40, 730, 150
    X = lambda m: x0 + (x1 - x0) * m / 70   # noqa: E731
    g = s.lin([(0, GOL_A), (.414, "#FFFFFF"), (1, MER_A)], x0, 0, x1, 0, kull="userSpaceOnUse", ad="cg")
    s += f'<rect x="{x0}" y="{y - 14}" width="{x1 - x0}" height="28" rx="14" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    for m in range(0, 71, 10):
        s += f'<path d="M{f(X(m))} {y + 14} v12" stroke="{OBS}" stroke-width="3"/>' + _yazi(X(m), y + 50, str(m), 22, GUM_K)
    s += f'<path d="M{f(X(29))} {y - 52} V{y + 20}" stroke="{OBS}" stroke-width="4" stroke-dasharray="8 6"/>'
    s += f'<rect x="{f(X(29) - 62)}" y="{y - 88}" width="124" height="36" rx="18" fill="{OBS}"/>'
    s += _yazi(X(29), y - 62, "hava ≈ 29", 23, "#FFFFFF", font=B)
    for m, ad, ust in ((4, "He", True), (16, "CH_4", False), (17, "NH_3", True), (32, "O_2", True), (44, "CO_2", False), (64, "SO_2", True)):
        c = GOL_K if m < 29 else MER_K
        yy = y - 34 if ust else y + 92
        s += f'<circle cx="{f(X(m))}" cy="{y}" r="9" fill="{GOL if m < 29 else MER}" stroke="{OBS}" stroke-width="2.4"/>'
        s += _yazi(X(m), yy, ad, 26, c, font=B)
    s += _ok(60, 56, 60, 14, GOL_K, 4, 13) + _yazi(80, 46, "havadan hafif: yükselir", 23, GOL_K, "start", font=B)
    s += _ok(452, 14, 452, 56, MER_K, 4, 13) + _yazi(472, 46, "ağır: aşağıda birikir", 23, MER_K, "start", font=B)
    s += _yazi(x1, y + 92, "M (g/mol)", 22, GUM_K, "end")
    return s.cikti(f"0 0 {W} {H}", cls="info")


def graham_boru(onek="gi-gra"):
    """NH₃–HCl borusu (100 cm): beyaz NH₄Cl halkası NH₃ ucundan ≈ 59 cm uzakta oluşur."""
    s = Svg(onek)
    W, H = 700, 200
    x0, x1, y = 60, 640, 90
    s += f'<rect x="{x0}" y="{y - 22}" width="{x1 - x0}" height="44" rx="14" fill="#F4F9FB" stroke="{OBS}" stroke-width="3.4"/>'
    s += f'<rect x="{x0 - 44}" y="{y - 30}" width="48" height="60" rx="10" fill="{GOL_A}" stroke="{GOL_K}" stroke-width="3"/>'
    s += f'<rect x="{x1 - 4}" y="{y - 30}" width="48" height="60" rx="10" fill="{MER_A}" stroke="{MER_K}" stroke-width="3"/>'
    s += _yazi(x0 - 20, y - 42, "NH_3", 26, GOL_K, font=B) + _yazi(x1 + 20, y - 42, "HCl", 26, MER_K, font=B)
    xr = x0 + (x1 - x0) * .594
    s += f'<rect x="{f(xr - 9)}" y="{y - 20}" width="18" height="40" fill="#FFFFFF" stroke="{GUM_K}" stroke-width="2.4"/>'
    s += f'<rect x="{f(xr - 9)}" y="{y - 20}" width="18" height="40" fill="#DDE4EA" opacity=".6"/>'
    r = RNG(3)
    for k in range(7):
        px = x0 + 20 + k * (xr - x0 - 40) / 6
        s += f'<circle cx="{f(px)}" cy="{f(y + r.uniform(-10, 10))}" r="6" fill="{GOL}" stroke="{OBS}" stroke-width="1.6"/>'
    for k in range(5):
        px = xr + 24 + k * (x1 - xr - 44) / 4
        s += f'<circle cx="{f(px)}" cy="{f(y + r.uniform(-10, 10))}" r="7" fill="{MER}" stroke="{OBS}" stroke-width="1.6"/>'
    s += f'<path d="M{x0} {y + 42} V{y + 62} M{f(xr)} {y + 42} V{y + 62} M{x1} {y + 42} V{y + 62}" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M{x0} {y + 52} H{f(xr)}" stroke="{GOL_K}" stroke-width="3"/><path d="M{f(xr)} {y + 52} H{x1}" stroke="{MER_K}" stroke-width="3"/>'
    s += _yazi((x0 + xr) / 2, y + 86, "≈ 59 cm", 26, GOL_K, font=B) + _yazi((xr + x1) / 2, y + 86, "≈ 41 cm", 26, MER_K, font=B)
    s += _yazi(xr, y - 34, "beyaz NH_4Cl halkası", 22, OBS, font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ------------------------------------------------------------------ KISSA, İMTİHAN, ÜSTAD grafikleri

def kissa_pt(onek="gi-kpt"):
    """Kıssa 3: eşit hacimli iki çelik tüp, P–T doğruları (X: 400 K'de 1,2 atm; Y: 400 K'de 0,4 atm)."""
    s = Svg(onek)
    W, H = 470, 350
    x0, y0, x1, y1 = 90, 286, 440, 40
    X = lambda t: x0 + (x1 - x0) * t / 400   # noqa: E731
    Y = lambda p: y0 - (y0 - y1) * p / 1.2   # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += _eksen(s, x0, y0, x1, y1, [(X(t), str(t)) for t in (100, 200, 300, 400)], [(Y(p), f"{p:.1f}".replace(".", ",")) for p in (0.3, 0.6, 0.9, 1.2)], "T (K)", "P (atm)", fs=24)
    s += f'<path d="M{f(X(0))} {f(Y(0))} L{f(X(400))} {f(Y(1.2))}" stroke="{KOB}" stroke-width="6"/>'
    s += f'<path d="M{f(X(0))} {f(Y(0))} L{f(X(400))} {f(Y(0.4))}" stroke="{KEH}" stroke-width="6"/>'
    s += _yazi(X(372), Y(1.2) + 8, "X", 32, KOB_K, "end", font=B) + _yazi(X(400) - 6, Y(0.4) - 16, "Y", 32, KEH_K, "end", font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def imtihan_vt(onek="gi-ivt"):
    """İmtihan 12: aynı basınçta X ve Y için V–t doğruları (0 °C'de X 16,8 L, Y 5,6 L)."""
    s = Svg(onek)
    W, H = 470, 330
    x0, y0, x1, y1 = 20, 270, 440, 30
    X = lambda t: x0 + (x1 - x0) * (t + 300) / 600   # noqa: E731
    Y = lambda v: y0 - (y0 - y1) * v / 40            # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    xs = X(0)
    for v in (5.6, 16.8):
        s += f'<path d="M{f(x0)} {f(Y(v))} H{f(x1)}" stroke="#DCE4E8" stroke-width="2"/>'
    s += f'<path d="M{f(xs)} {f(y1 - 10)} V{f(y0 + 6)} M{f(x0)} {f(y0)} H{f(x1 + 12)}" stroke="{OBS}" stroke-width="3.6"/>'
    s += f'<path d="M{f(x1 + 8)} {f(y0 - 8)} L{f(x1 + 22)} {f(y0)} L{f(x1 + 8)} {f(y0 + 8)} Z M{f(xs - 8)} {f(y1 - 6)} L{f(xs)} {f(y1 - 20)} L{f(xs + 8)} {f(y1 - 6)} Z" fill="{OBS}"/>'
    for v0, c, ad in ((16.8, KOB, "X"), (5.6, KEH_K, "Y")):
        s += f'<path d="M{f(X(-273))} {f(Y(0))} L{f(X(0))} {f(Y(v0))}" stroke="{c}" stroke-width="4" stroke-dasharray="10 8"/>'
        s += f'<path d="M{f(X(0))} {f(Y(v0))} L{f(X(273))} {f(Y(2 * v0))}" stroke="{c}" stroke-width="6"/>'
        s += _yazi(X(273) + 4, Y(2 * v0) - 10, ad, 30, c, "end", font=B)
    s += _yazi(X(-273), y0 + 32, "−273", 24, GUM_K) + _yazi(X(273), y0 + 32, "273", 24, GUM_K)
    s += _yazi(xs - 8, Y(16.8) + 8, "16,8", 22, GUM_K, "end") + _yazi(xs - 8, Y(5.6) + 8, "5,6", 22, GUM_K, "end")
    s += _yazi(x1 + 18, y0 + 58, "t (°C)", 24, OBS, "end") + _yazi(xs + 10, y1 + 2, "V (L)", 24, OBS, "start")
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def ustad_vt(onek="gi-uvt"):
    """Üstad 4: V–T grafiği; K (200 K; 2 L), L (400 K; 4 L), M (400 K; 2 L); gaz miktarı sabit."""
    s = Svg(onek)
    W, H = 440, 330
    x0, y0, x1, y1 = 80, 270, 410, 40
    X = lambda t: x0 + (x1 - x0) * t / 500   # noqa: E731
    Y = lambda v: y0 - (y0 - y1) * v / 5     # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += _eksen(s, x0, y0, x1, y1, [(X(t), str(t)) for t in (200, 400)], [(Y(v), str(v)) for v in (2, 4)], "T (K)", "V (L)", fs=24)
    s += f'<path d="M{f(X(0))} {f(Y(0))} L{f(X(450))} {f(Y(4.5))}" stroke="{GUM}" stroke-width="2.4" stroke-dasharray="8 7"/>'
    s += _ok(X(200), Y(2), X(392), Y(3.92), LAJVER, 5, 15)
    s += _ok(X(400), Y(4), X(400), Y(2.12), MER, 5, 15)
    for t, v, ad, dx, dy in ((200, 2, "K", -26, -12), (400, 4, "L", -10, -20), (400, 2, "M", 30, 10)):
        s += f'<circle cx="{f(X(t))}" cy="{f(Y(v))}" r="10" fill="#FFFFFF" stroke="{OBS}" stroke-width="4"/>'
        s += _yazi(X(t) + dx, Y(v) + dy, ad, 30, OBS, font=B)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


# ------------------------------------------------------------------ ANAHTAR · tüf basamaklarında akçe

def merdiven_tuf(onek="gi-mrd"):
    from cizim.karakter import akce_sikke
    from cizim.temel import halolu_yazi
    s = Svg(onek)
    W, H = 900, 330
    g = s.lin([(0, "#FFE0C8"), (1, "#F7B9C6")], 0, 0, 0, 1, ad="gk")
    s += f'<rect width="{W}" height="{H}" rx="22" fill="{g}"/>'
    s += SU.guvercinler(560, 40, 260, 70, 5, 31, renk="#FFFFFF")
    tuf = s.lin([(0, "#E9A36A"), (1, "#B4643A")], 0, 0, 0, 1, ad="tf")
    for k in range(4):
        x = 50 + k * 205
        y = 70 + k * 52
        s += f'<path d="M{x} {H - 20} V{y + 10} Q{x} {y} {x + 12} {y} H{x + 203} Q{x + 215} {y} {x + 215} {y + 10} V{H - 20} Z" fill="{tuf}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<path d="M{x + 6} {y + 16} H{x + 209}" stroke="#FFD9B0" stroke-width="5" opacity=".8"/>'
        s += f'<path d="M{x + 30} {y + 40} q-6 60 6 {H - 80 - y}" stroke="#8E4A26" stroke-width="3" fill="none" opacity=".45"/>'
        if y + 120 < H - 40:
            s += f'<path d="M{x + 170} {y + 120} v-12 a9 9 0 0 1 18 0 v12 Z" fill="#5A2E18" opacity=".8"/>'
        for j in range(4 - k):
            s += akce_sikke(s, x + 40 + j * 46, y - 26, 20)
        s += halolu_yazi(f'x="{x + 107}" y="{y + 64}" text-anchor="middle" {B} font-size="48"', f"+{40 - 10 * k}", "#FFFFFF", OBS, 1.4)
        if y + 100 < H - 30:
            s += f'<text x="{x + 107}" y="{y + 100}" text-anchor="middle" {T} font-size="31" fill="{OBS}">{k} basamak</text>'
        else:
            s += f'<text x="{x + 107}" y="{y - 52}" text-anchor="middle" {T} font-size="31" fill="{OBS}">{k} basamak</text>'
    s += f'<text x="{W - 26}" y="46" text-anchor="end" {T} font-size="34" fill="{OBS}">Az in, çok kazan!</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info merdiven-akce")


# ------------------------------------------------------------------ MEDENİYETİMİZDEN · Gevher Nesibe (temsilî taç kapı)

def sifahane(onek="gi-sif"):
    """Selçuklu taç kapısı (temsilî; yazısız, yalnız geometrik süs): Gevher Nesibe Darüşşifası köşesi için."""
    s = Svg(onek)
    W, H = 300, 320
    g = s.lin([(0, "#FFF4DE"), (1, "#F2DDB8")], 0, 0, 0, 1, ad="zm")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{g}"/>'
    tas = s.lin([(0, "#E9D2A8"), (1, "#C9A47A")], 0, 0, 1, 0, ad="ts")
    s += f'<rect x="40" y="26" width="220" height="280" fill="{tas}" stroke="#7A5A3A" stroke-width="4"/>'
    s += f'<rect x="54" y="40" width="192" height="266" fill="none" stroke="#8C6A44" stroke-width="3"/>'
    zz = " ".join(f"{'M' if i == 0 else 'L'}{f(60 + i * 12)} {48 if i % 2 else 58}" for i in range(16))
    s += f'<path d="{zz}" stroke="#8C6A44" stroke-width="3" fill="none"/>'
    s += f'<path d="M80 306 V150 Q80 84 150 70 Q220 84 220 150 V306 Z" fill="#D9B98E" stroke="#7A5A3A" stroke-width="4"/>'
    for k in range(4):
        y = 104 + k * 22
        w = 58 - k * 9
        for j in range(-3 + k // 2, 4 - k // 2):
            s += f'<path d="M{150 + j * 22 - 10} {y + 12} Q{150 + j * 22} {y - 6} {150 + j * 22 + 10} {y + 12} Z" fill="#E9D2A8" stroke="#8C6A44" stroke-width="2"/>'
    s += f'<path d="M116 306 V222 Q116 196 150 190 Q184 196 184 222 V306 Z" fill="#5A3A26" stroke="#3A2614" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(150, 176, 14), True)}" fill="{ALTIN}" stroke="#7A5A3A" stroke-width="2"/>'
    for (x, y) in ((64, 260), (236, 260), (64, 200), (236, 200)):
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 9), True)}" fill="none" stroke="#8C6A44" stroke-width="2"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info")
