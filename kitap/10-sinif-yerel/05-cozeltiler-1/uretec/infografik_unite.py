"""Çözünme ve Çözünürlük · üniteye özel bilgi grafikleri ({{info|ad}} önce buraya bakar).

Grafiklerdeki bütün sayılar dogrula.py içindeki VERI sözlüğüyle AYNI kaynaktan gelir (VERI burada tanımlıdır;
dogrula.py onu içe aktarıp sorulardaki sayılarla karşılaştırır). Değerler yaklaşık deneysel verilerdir
(KNO₃, NaCl, Li₂SO₄, Na₂SO₄, CO₂, O₂) ya da stilize "X tuzu" eğrisidir.
"""
import math
from cizim.temel import Svg, f, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, rng as RNG
from cizim.renkler import OBS, GOL, GOL_K, GOL_A, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ALTIN, ALTIN_K, ERGUVAN, ZUMRUT, GUM, GUM_K, LAJVER

T = 'font-family="Nunito" font-weight="800"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'

# ------------------------------------------------------------------ veri (dogrula.py da bunu kullanır)
VERI = {
    "KNO3": [(0, 13), (10, 21), (20, 32), (30, 46), (40, 64), (50, 85), (60, 110), (70, 138), (80, 169)],
    "NaCl": [(0, 35.7), (20, 36), (40, 36.6), (60, 37.3), (80, 38)],
    "Li2SO4": [(0, 36), (20, 34), (40, 33), (60, 32), (80, 31)],
    "CO2": [(0, 3.3), (10, 2.3), (20, 1.7), (30, 1.3), (40, 1.0), (50, .8), (60, .6)],          # g/L, 1 atm CO₂
    "O2": [(0, 14.6), (10, 11.3), (20, 9.1), (30, 7.6), (40, 6.4)],                               # mg/L, havayla denge
    "X": [(0, 20), (10, 25), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 85), (80, 100)],
    "Na2SO4": [(0, 5), (10, 9), (20, 19), (30, 41), (32.4, 50), (40, 49), (60, 45), (80, 44), (100, 42.5)],
    "A": [(0, 20), (20, 30), (40, 45), (60, 65), (80, 90)],
    "B": [(0, 60), (20, 50), (40, 42), (60, 36), (80, 32)],
}


def oku(ad, t):
    """Doğrusal ara değer: VERI[ad] eğrisinden t sıcaklığındaki değer."""
    p = VERI[ad]
    for (a, x), (b, y) in zip(p, p[1:]):
        if a <= t <= b:
            return x + (y - x) * (t - a) / (b - a)
    raise ValueError(f"{ad}: {t} aralık dışı")


def _grafik(onek, egriler, xmax, ymax, xadim, yadim, xet="sıcaklık (°C)", yet="g / 100 g su", W=620, H=420,
            isaret=(), noktalar=(), yaz=None, ondalik=False, cls="info grafik", zemin="#FFFFFF"):
    """Ortak çizgi grafiği. egriler: [(ad, renk, etiket, (ex, ey) etiket kayması)], isaret: [(x, y)] kesik kılavuz,
    noktalar: [(x, y, harf, renk)]."""
    s = Svg(onek)
    x0, y0, x1, y1 = 92, H - 66, W - 22, 26
    X = lambda v: x0 + (x1 - x0) * v / xmax
    Y = lambda v: y0 - (y0 - y1) * v / ymax
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{zemin}"/>'
    v = 0
    while v <= xmax + 1e-9:
        s += f'<path d="M{f(X(v))} {y0} V{y1}" stroke="#E2E8EC" stroke-width="2"/>'
        s += f'<text x="{f(X(v))}" y="{y0 + 32}" text-anchor="middle" {T} font-size="25" fill="{OBS}">{f(v)}</text>'
        v += xadim
    v = 0
    while v <= ymax + 1e-9:
        s += f'<path d="M{x0} {f(Y(v))} H{x1}" stroke="#E2E8EC" stroke-width="2"/>'
        et = f"{v:.1f}".replace(".", ",").replace(",0", "") if ondalik else f(v)
        s += f'<text x="{x0 - 12}" y="{f(Y(v) + 9)}" text-anchor="end" {T} font-size="25" fill="{OBS}">{et}</text>'
        v += yadim
    s += f'<path d="M{x0} {y1 - 8} V{y0} H{x1 + 8}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    s += f'<text x="{x1}" y="{H - 10}" text-anchor="end" {T} font-size="23" fill="{GUM_K}">{xet}</text>'
    s += f'<text x="{x0 + 10}" y="{y1 + 6}" {T} font-size="23" fill="{GUM_K}">{yet}</text>'
    for (gx, gy) in isaret:
        s += f'<path d="M{f(X(gx))} {y0} V{f(Y(gy))} H{x0}" stroke="{ALTIN}" stroke-width="2.6" stroke-dasharray="7 6" fill="none"/>'
    for ad, renk, etiket, (ex, ey) in egriler:
        pts = [(X(a), Y(b)) for a, b in VERI[ad] if a <= xmax]
        s += f'<path d="{egri_d(pts, gerginlik=.8)}" stroke="{renk}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        if etiket:
            lx, ly = pts[-1]
            s += f'<text x="{f(lx + ex)}" y="{f(ly + ey)}" text-anchor="end" {B} font-size="28" fill="{renk}">{etiket}</text>'
    for (px, py, harf, renk) in noktalar:
        s += f'<circle cx="{f(X(px))}" cy="{f(Y(py))}" r="11" fill="#FFFFFF" stroke="{renk}" stroke-width="5"/>'
        s += f'<text x="{f(X(px) + 16)}" y="{f(Y(py) - 12)}" {B} font-size="30" fill="{renk}">{harf}</text>'
    if yaz:
        s += yaz(X, Y)
    return s.cikti(f"0 0 {W} {H}", cls=cls)


def _alt(etiket, sayi):
    """SVG içinde alt simgeli formül: ('KNO', '3') → KNO<tspan>3</tspan>."""
    return f'{etiket}<tspan dy="6" font-size="20">{sayi}</tspan>'


# ------------------------------------------------------------------ 4. durak: katıların çözünürlük eğrileri
def cozunurluk_egrileri(onek="inf-coz"):
    def yaz(X, Y):
        o = f'<text x="{f(X(62))}" y="{f(Y(150))}" {B} font-size="28" fill="{MER}">{_alt("KNO", "3")}</text>'
        o += f'<text x="{f(X(48))}" y="{f(Y(42) - 4)}" {B} font-size="26" fill="{GOL_K}">NaCl</text>'
        o += f'<text x="{f(X(57))}" y="{f(Y(25) + 6)}" {B} font-size="26" fill="{KOB}">Li<tspan dy="6" font-size="19">2</tspan><tspan dy="-6">SO</tspan><tspan dy="6" font-size="19">4</tspan></text>'
        return o
    return _grafik(onek, [("KNO3", MER, "", (0, 0)), ("NaCl", GOL, "", (0, 0)), ("Li2SO4", KOB, "", (0, 0))], 80, 180, 20, 30,
                   isaret=[(60, 110), (20, 32)], yaz=yaz)


# ------------------------------------------------------------------ 4. durak: CO₂'nin çözünürlüğü (1 atm CO₂)
def gaz_egrisi(onek="inf-gaz"):
    def yaz(X, Y):
        return (f'<text x="{f(X(31))}" y="{f(Y(2.25))}" {B} font-size="28" fill="{GOL_K}">CO<tspan dy="6" font-size="20">2</tspan></text>'
                f'<text x="{f(X(60))}" y="{f(Y(3.1))}" text-anchor="end" {T} font-size="21" fill="{GUM_K}">1 atm CO₂ altında</text>')
    return _grafik(onek, [("CO2", GOL, "", (0, 0))], 60, 3.5, 10, .5, yet="g CO₂ / 1 L su", isaret=[(20, 1.7), (40, 1.0)],
                   yaz=yaz, ondalik=True, W=520, H=380)


# ------------------------------------------------------------------ 5. durak: doygunluk (A, B, C noktaları)
def doygunluk_grafigi(onek="inf-doy"):
    def yaz(X, Y):
        return (f'<text x="{f(X(4))}" y="{f(Y(84))}" {B} font-size="24" fill="{MER}">aşırı doymuş</text>'
                f'<text x="{f(X(58))}" y="{f(Y(22))}" {B} font-size="24" fill="{GOL_K}">doymamış</text>'
                f'<text x="{f(X(77))}" y="{f(Y(91))}" text-anchor="end" {B} font-size="24" fill="{KOB}">eğri: doymuş</text>')
    return _grafik(onek, [("X", KOB, "", (0, 0))], 80, 100, 20, 20, noktalar=[(50, 35, "A", GOL), (50, 60, "B", KOB), (50, 82, "C", MER)],
                   yaz=yaz, W=560, H=400)


# ------------------------------------------------------------------ 6. durak: X tuzunun çözünürlük eğrisi (hesaplar)
def x_egrisi(onek="inf-x"):
    def yaz(X, Y):
        o = ""
        for t, v in VERI["X"]:
            if t in (20, 30, 40, 60, 80):
                o += f'<circle cx="{f(X(t))}" cy="{f(Y(v))}" r="7" fill="#FFFFFF" stroke="{ERGUVAN}" stroke-width="4"/>'
                o += f'<text x="{f(X(t) - 10)}" y="{f(Y(v) - 14)}" text-anchor="end" {B} font-size="24" fill="{ERGUVAN}">{f(v)}</text>'
        o += f'<text x="{f(X(10))}" y="{f(Y(88))}" {B} font-size="30" fill="{ERGUVAN}">X tuzu</text>'
        return o
    return _grafik(onek, [("X", ERGUVAN, "", (0, 0))], 80, 100, 10, 10, yaz=yaz, W=560, H=430)


# ------------------------------------------------------------------ Kıssa 1: çözünmüş O₂ (havayla dengede)
def o2_grafik(onek="inf-o2"):
    def yaz(X, Y):
        return f'<text x="{f(X(24))}" y="{f(Y(12))}" {B} font-size="28" fill="{GOL_K}">O<tspan dy="6" font-size="20">2</tspan></text>'
    return _grafik(onek, [("O2", GOL, "", (0, 0))], 40, 16, 10, 4, yet="mg O₂ / 1 L su", isaret=[(10, 11.3), (20, 9.1)], yaz=yaz,
                   ondalik=False, W=480, H=360)


# ------------------------------------------------------------------ Üstad 1: Na₂SO₄ (Acıgöl tuzu) — tepe yapan eğri
def na2so4_grafik(onek="inf-nas"):
    def yaz(X, Y):
        return (f'<text x="{f(X(48))}" y="{f(Y(56))}" {B} font-size="26" fill="{LAJVER}">Na<tspan dy="6" font-size="19">2</tspan><tspan dy="-6">SO</tspan><tspan dy="6" font-size="19">4</tspan></text>'
                f'<circle cx="{f(X(32.4))}" cy="{f(Y(50))}" r="8" fill="#FFFFFF" stroke="{MER}" stroke-width="4"/>'
                f'<text x="{f(X(37))}" y="{f(Y(39))}" {T} font-size="22" fill="{MER}">≈ 32 °C’ta tepe</text>')
    return _grafik(onek, [("Na2SO4", LAJVER, "", (0, 0))], 100, 60, 20, 10, isaret=[(40, 49)], yaz=yaz, W=500, H=360, cls="info ustad-graf",
                   zemin="#FFFDF7")


# ------------------------------------------------------------------ İmtihan 6: A ve B katıları
def ab_grafik(onek="inf-ab"):
    def yaz(X, Y):
        return (f'<text x="{f(X(52))}" y="{f(Y(72))}" {B} font-size="44" fill="{MER}">A</text>'
                f'<text x="{f(X(64))}" y="{f(Y(48))}" {B} font-size="44" fill="{KOB}">B</text>')
    return _grafik(onek, [("A", MER, "", (0, 0)), ("B", KOB, "", (0, 0))], 80, 100, 20, 20, W=400, H=320)


# ------------------------------------------------------------------ 1. durak: çözünmenin üç basamağı (tanecik)
def _su(x, y, a, o=1.0):
    """Su molekülü: O (mercan) + iki H (beyaz); a: H'lerin baktığı yön (derece)."""
    r = math.radians(a)
    hx1, hy1 = x + 15 * o * math.cos(r + .9), y + 15 * o * math.sin(r + .9)
    hx2, hy2 = x + 15 * o * math.cos(r - .9), y + 15 * o * math.sin(r - .9)
    return (f'<circle cx="{f(hx1)}" cy="{f(hy1)}" r="{f(7 * o)}" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
            f'<circle cx="{f(hx2)}" cy="{f(hy2)}" r="{f(7 * o)}" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(12 * o)}" fill="{MER}" stroke="{OBS}" stroke-width="2"/>')


def _iyon(x, y, art, o=1.0):
    renk, isaret, r = ("#8E5BD0", "+", 15) if art else ("#39A85A", "−", 20)
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * o)}" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>'
            f'<text x="{f(x)}" y="{f(y + 8 * o)}" text-anchor="middle" {B} font-size="{f(24 * o)}" fill="#FFFFFF">{isaret}</text>')


def cozunme_basamaklari(onek="inf-bas"):
    s = Svg(onek)
    W, H = 1500, 430
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#F6FBFC"/>'
    kut = [(20, "1 · Çözünen ayrılır", "enerji ALIR", MER), (520, "2 · Çözücüde yer açılır", "enerji ALIR", MER),
           (1020, "3 · Sarılma (hidratasyon)", "enerji VERİR", ZUMRUT)]
    for x, bas, en, renk in kut:
        s += f'<rect x="{x}" y="18" width="460" height="394" rx="18" fill="#FFFFFF" stroke="{GOL_K}" stroke-width="3"/>'
        s += f'<text x="{x + 230}" y="62" text-anchor="middle" {B} font-size="32" fill="{OBS}">{bas}</text>'
        s += f'<rect x="{x + 130}" y="360" width="200" height="38" rx="19" fill="{acik(renk, .82)}" stroke="{renk}" stroke-width="3"/>'
        s += f'<text x="{x + 230}" y="387" text-anchor="middle" {T} font-size="24" fill="{koyu(renk, .25)}">{en}</text>'
    # 1: kristal kafes → ayrılan iyonlar
    for i in range(3):
        for j in range(3):
            s += _iyon(80 + i * 44, 140 + j * 44, (i + j) % 2 == 0, .9)
    s += f'<path d="M230 186 h60" stroke="{OBS}" stroke-width="5"/><path d="M290 176 l18 10 l-18 10 Z" fill="{OBS}"/>'
    for k, (x, y) in enumerate(((350, 120), (420, 160), (360, 230), (430, 280), (380, 320))):
        s += _iyon(x, y, k % 2 == 0, .9)
    # 2: su molekülleri itilip boşluk açılıyor
    r = RNG(5)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        rr = 120 + r.uniform(-10, 14)
        s += _su(770 + rr * math.cos(a), 210 + rr * .75 * math.sin(a), r.uniform(0, 360), .85)
    s += f'<circle cx="770" cy="210" r="56" fill="none" stroke="{GOL}" stroke-width="3" stroke-dasharray="9 7"/>'
    s += f'<text x="770" y="219" text-anchor="middle" {T} font-size="22" fill="{GOL_K}">boşluk</text>'
    # 3: Na⁺ çevresinde O'lar, Cl⁻ çevresinde H'ler
    for cx, cy, art in ((1150, 200, True), (1340, 250, False)):
        s += _iyon(cx, cy, art, 1.1)
        for k in range(6):
            a = k / 6 * 2 * math.pi
            R = 54 if art else 62
            x, y = cx + R * math.cos(a), cy + R * math.sin(a)
            yon = math.degrees(a) if art else math.degrees(a) + 180
            s += _su(x, y, yon, .78)
    s += f'<text x="1150" y="312" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">O ucu (−) Na<tspan dy="-8" font-size="15">+</tspan><tspan dy="8">’ya</tspan></text>'
    s += f'<text x="1340" y="345" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">H ucu (+) Cl<tspan dy="-8" font-size="15">−</tspan><tspan dy="8">’ye</tspan></text>'
    return s.cikti(f"0 0 {W} {H}", cls="info basamak-info")


# ------------------------------------------------------------------ 2. durak: sabun misel
def sabun_miseli(onek="inf-sab"):
    s = Svg(onek)
    W, H = 520, 380
    g = s.lin([(0, "#DFF4F7"), (1, "#A9DDE6")], 0, 0, 0, 1, ad="sz")
    s += f'<rect width="{W}" height="{H}" rx="20" fill="{g}"/>'
    cx, cy = 260, 196
    yag = s.rad([(0, "#FFE7A0"), (1, "#E9B44A")], ad="yg")
    s += f'<circle cx="{cx}" cy="{cy}" r="74" fill="{yag}" stroke="#B8862A" stroke-width="3"/>'
    s += f'<text x="{cx}" y="{cy + 10}" text-anchor="middle" {B} font-size="34" fill="{KEH_K}">yağ</text>'
    for k in range(16):
        a = k / 16 * 2 * math.pi
        x1, y1 = cx + 58 * math.cos(a), cy + 58 * math.sin(a)
        x2, y2 = cx + 118 * math.cos(a), cy + 118 * math.sin(a)
        mx, my = (x1 + x2) / 2 + 8 * math.cos(a + 1.5), (y1 + y2) / 2 + 8 * math.sin(a + 1.5)
        s += f'<path d="M{f(x1)} {f(y1)} Q{f(mx)} {f(my)} {f(x2)} {f(y2)}" stroke="{OBS}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        s += f'<circle cx="{f(cx + 128 * math.cos(a))}" cy="{f(cy + 128 * math.sin(a))}" r="12" fill="{KOB}" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<circle cx="30" cy="32" r="10" fill="{KOB}" stroke="{OBS}" stroke-width="2"/><text x="48" y="40" {T} font-size="23" fill="{KOB_K}">baş: iyonik, suyu sever</text>'
    s += f'<path d="M18 358 q8 -10 16 0 t16 0" stroke="{OBS}" stroke-width="4" fill="none"/><text x="58" y="366" {T} font-size="23" fill="{OBS}">kuyruk: apolar, yağı sever</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info sabun")


# ------------------------------------------------------------------ 3. durak: iletkenlik düzeneği (3 kap)
def iletkenlik(onek="inf-ilt"):
    s = Svg(onek)
    W, H = 1260, 400
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#F6FBFC"/>'
    kaplar = [(220, "Acıgöl suyu", "parlak", 1.0, "#BFE7E2", True), (630, "sirke", "sönük", .45, "#F4E7C8", True),
              (1040, "şekerli su", "yanmıyor", 0, "#FFFFFF", False)]
    for x, ad, durum, guc, sivi, iyon in kaplar:
        # pil ve kablolar
        s += f'<rect x="{x - 150}" y="64" width="64" height="34" rx="5" fill="{GUM}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<rect x="{x - 86}" y="74" width="8" height="14" fill="{OBS}"/>'
        s += f'<path d="M{x - 150} 81 H{x - 170} V200 H{x - 40} M{x - 78} 81 H{x + 40} V120 M{x + 40} 154 V200" stroke="{OBS}" stroke-width="4" fill="none"/>'
        # ampul
        if guc:
            hl = s.rad([(0, "#FFF4C8", .95 * guc), (.5, "#FFD27A", .5 * guc), (1, "#FFD27A", 0)], x + 40, 132, 70, kull="userSpaceOnUse", ad="am")
            s += f'<circle cx="{x + 40}" cy="132" r="70" fill="{hl}"/>'
        s += f'<circle cx="{x + 40}" cy="128" r="22" fill="{"#FFE58A" if guc > .8 else ("#FFF1C4" if guc else "#FFFFFF")}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<rect x="{x + 30}" y="146" width="20" height="12" fill="{GUM_K}"/>'
        # kap + elektrotlar
        s += f'<path d="M{x - 90} 180 V330 Q{x - 90} 350 {x - 70} 350 H{x + 70} Q{x + 90} 350 {x + 90} 330 V180" fill="none" stroke="{OBS}" stroke-width="4"/>'
        s += f'<path d="M{x - 86} 230 H{x + 86} V330 Q{x + 86} 346 {x + 70} 346 H{x - 70} Q{x - 86} 346 {x - 86} 330 Z" fill="{sivi}"/>'
        s += f'<rect x="{x - 46}" y="196" width="12" height="120" fill="#5E6672"/><rect x="{x + 34}" y="196" width="12" height="120" fill="#5E6672"/>'
        s += f'<path d="M{x - 40} 200 V196 M{x + 40} 200 V196" stroke="{OBS}" stroke-width="4"/>'
        r = RNG(int(x))
        for k in range(8 if iyon else 5):
            px, py = x + r.uniform(-66, 66), r.uniform(250, 330)
            if iyon and (guc > .8 or k < 3):
                art = k % 2 == 0
                s += f'<circle cx="{f(px)}" cy="{f(py)}" r="10" fill="{"#8E5BD0" if art else "#39A85A"}" stroke="{OBS}" stroke-width="1.6"/>'
                s += f'<text x="{f(px)}" y="{f(py + 6)}" text-anchor="middle" {B} font-size="16" fill="#FFFFFF">{"+" if art else "−"}</text>'
            else:
                s += f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="14" ry="9" fill="#FFFFFF" stroke="{GUM_K}" stroke-width="2"/>'
        s += f'<text x="{x}" y="384" text-anchor="middle" {B} font-size="30" fill="{OBS}">{ad}</text>'
        s += f'<text x="{x + 74}" y="128" {T} font-size="23" fill="{KEH_K if guc else GUM_K}">{durum}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info iletkenlik")


# ------------------------------------------------------------------ Medeniyetimizden: İbn Sînâ (kitap + damla + taş)
def ibni_sina(onek="inf-ibs"):
    s = Svg(onek)
    W, H = 420, 330
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFF7E6"/>'
    s += f'<path d="M60 250 Q130 226 206 250 V110 Q130 86 60 110 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M206 250 Q282 226 352 250 V110 Q282 86 206 110 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    for k in range(5):
        s += f'<path d="M80 {130 + k * 22} Q130 {120 + k * 22} 188 {130 + k * 22}" stroke="{GUM}" stroke-width="3" fill="none"/>'
    # sağ sayfada: damla → teras
    s += f'<path d="M262 116 q12 22 0 36 q-12 -14 0 -36 Z" fill="{GOL}" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="M262 160 v18" stroke="{OBS}" stroke-width="3"/><path d="M254 176 l8 10 l8 -10 Z" fill="{OBS}"/>'
    for k in range(3):
        y = 198 + k * 14
        s += f'<path d="M{226 + k * 6} {y} Q{262} {y + 10} {300 - k * 6} {y}" stroke="#FFFFFF" stroke-width="7" fill="none"/>'
        s += f'<path d="M{226 + k * 6} {y} Q{262} {y + 10} {300 - k * 6} {y}" stroke="{GUM_K}" stroke-width="2" fill="none"/>'
    s += f'<text x="210" y="300" text-anchor="middle" {T} font-size="22" fill="{ALTIN_K}">“Su da taşa dönüşür.”</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info imbik")
