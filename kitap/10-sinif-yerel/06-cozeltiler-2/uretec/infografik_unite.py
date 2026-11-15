"""Derişim Birimleri · üniteye özel bilgi grafikleri ({{info|ad}} → ad(önek)). Değerler uretec/dogrula.py'de denetlenir.

Yazılar dolgulu Nunito/Baloo (kontur yok); renkler renkler.py paletinden; zemin açık (fotokopiye uygun).
"""
import math
from cizim.temel import Svg, f, egri_d
from cizim.renkler import OBS, GOL, GOL_K, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ERGUVAN, SOLUK

T = 'font-family="Nunito" font-weight="800"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'


def _beher(x, y, w, h, su=.62, dolgu="#8ED8DA"):
    """y: taban. Cam beher + su (su: doluluk oranı)."""
    hs = h * su
    return (f'<path d="M{f(x)} {f(y - hs)} h{f(w)} v{f(hs - 6)} q0 6 -6 6 h{f(-(w - 12))} q-6 0 -6 -6 Z" fill="{dolgu}" opacity=".85"/>'
            f'<path d="M{f(x - 4)} {f(y - h)} h{f(w + 8)} M{f(x)} {f(y - h)} v{f(h - 6)} q0 6 6 6 h{f(w - 12)} q6 0 6 -6 v{f(-(h - 6))}" fill="none" stroke="{OBS}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M{f(x + w - 10)} {f(y - h * .78)} h7 M{f(x + w - 10)} {f(y - h * .56)} h7 M{f(x + w - 10)} {f(y - h * .34)} h7" stroke="{OBS}" stroke-width="1.6"/>')


def _tanecik(x, y, r_, renk, cizgi=OBS):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r_)}" fill="{renk}" stroke="{cizgi}" stroke-width="1.2"/>'


def derisim_bardaklari(onek="inf-der"):
    """Aynı miktar su, artan çözünen: seyreltik → derişik (göreli)."""
    s = Svg(onek)
    Wd, Hd = 380, 116
    s += f'<rect width="{Wd}" height="{Hd}" rx="12" fill="#F4FAFB"/>'
    noktalar = {0: [(14, 30), (40, 18)], 1: [(10, 34), (26, 16), (44, 28), (30, 40), (52, 12)],
                2: [(8, 36), (20, 18), (34, 30), (48, 14), (56, 36), (14, 8), (40, 42), (28, 6), (54, 24), (20, 44)]}
    for k in range(3):
        x0 = 30 + k * 118
        s += _beher(x0, 92, 70, 70, .74)
        for (dx, dy) in noktalar[k]:
            s += _tanecik(x0 + 6 + dx, 92 - 50 + dy * .9, 4.2, "#FFFFFF", "#2F6A86")
    s += f'<path d="M40 104 H342" stroke="{KEH_K}" stroke-width="3"/><path d="M342 104 l-10 -6 v12 Z" fill="{KEH_K}"/>'
    s += f'<text x="34" y="16" {T} font-size="14" fill="{GOL_K}">seyreltik</text>'
    s += f'<text x="346" y="16" text-anchor="end" {T} font-size="14" fill="{MER_K}">derişik</text>'
    s += f'<text x="190" y="16" text-anchor="middle" {T} font-size="13" fill="{SOLUK}">aynı su · artan tuz</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def alyuvarlar(onek="inf-aly"):
    """Hipertonik / izotonik / hipotonik ortamda alyuvar (temsilî)."""
    s = Svg(onek)
    Wd, Hd = 120, 150
    s += f'<rect width="{Wd}" height="{Hd}" rx="10" fill="#FFFFFF"/>'
    satir = [("çok tuzlu", "büzüşür", "b"), ("serum", "aynı kalır", "n"), ("saf su", "şişer", "s")]
    for k, (ust, alt, tur) in enumerate(satir):
        cy = 26 + k * 48
        cx = 26
        if tur == "b":
            pts = []
            for i in range(24):
                a = 2 * math.pi * i / 24
                rr = 13 + (3 if i % 2 else -1)
                pts.append((cx + rr * math.cos(a), cy + rr * .8 * math.sin(a)))
            s += f'<path d="{egri_d(pts, True, .6)}" fill="#E2533D" stroke="{MER_K}" stroke-width="1.6"/>'
        elif tur == "n":
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="17" ry="12" fill="#E2533D" stroke="{MER_K}" stroke-width="1.6"/><ellipse cx="{cx}" cy="{cy}" rx="8" ry="5" fill="#F08A7A"/>'
        else:
            s += f'<circle cx="{cx}" cy="{cy}" r="19" fill="#F27A66" stroke="{MER_K}" stroke-width="1.6"/>'
        s += f'<text x="52" y="{cy - 2}" {T} font-size="13" fill="{OBS}">{ust}</text><text x="52" y="{cy + 13}" {T} font-size="12" fill="{SOLUK}">{alt}</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def ppm_zoom(onek="inf-ppm"):
    """%1 → 100 ppm → 1 ppm: iç içe 10×10 ızgaralar."""
    s = Svg(onek)
    Wd, Hd = 400, 132
    s += f'<rect width="{Wd}" height="{Hd}" rx="12" fill="#FBF4FA"/>'
    kutular = [(14, 10, 92), (154, 10, 92), (294, 10, 92)]
    renk = ["#F7D6E4", "#F2C2D6", "#EDB0C9"]
    for k, (x, y, a) in enumerate(kutular):
        s += f'<rect x="{x}" y="{y}" width="{a}" height="{a}" fill="{renk[k]}" stroke="{OBS}" stroke-width="2"/>'
        for i in range(1, 10):
            s += f'<path d="M{f(x + a * i / 10)} {y} v{a} M{x} {f(y + a * i / 10)} h{a}" stroke="#B9849C" stroke-width=".8"/>'
        hx, hy = x + a * .9, y
        s += f'<rect x="{f(hx)}" y="{f(hy)}" width="{f(a / 10)}" height="{f(a / 10)}" fill="{"#E8467C" if k == 2 else "#FFFFFF"}" stroke="{MER_K if k == 2 else OBS}" stroke-width="1.6"/>'
        if k < 2:
            nx, ny, na = kutular[k + 1]
            s += f'<path d="M{f(hx + a / 10)} {f(hy)} L{nx} {ny} M{f(hx + a / 10)} {f(hy + a / 10)} L{nx} {ny + na}" stroke="{ERGUVAN}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    for (x, y, a), et in zip(kutular, ("1 kare = %1", "1 kare = 100 ppm", "1 kare = 1 ppm")):
        s += f'<text x="{x + a / 2}" y="{y + a + 20}" text-anchor="middle" {T} font-size="14" fill="{OBS}">{et}</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def molarite_balonu(onek="inf-mol"):
    """Balon joje: 0,1 mol Na2SO4 · 500 mL çizgisi; Na+ (mor) ve SO4 2− (sarı) iyonları."""
    s = Svg(onek)
    Wd, Hd = 120, 156
    s += f'<rect width="{Wd}" height="{Hd}" rx="10" fill="#F4F7FD"/>'
    s += f'<path d="M60 146 C26 146 16 124 24 108 C30 96 44 92 52 88 V22 H68 V88 C76 92 90 96 96 108 C104 124 94 146 60 146 Z" fill="#E8F2FA" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M26 116 C34 132 86 132 94 116 C98 130 88 143 60 143 C32 143 22 130 26 116 Z M53 60 H67 V88 C75 92 88 96 94 106 C96 110 26 110 26 106 C32 96 45 92 53 88 Z" fill="#9FD3E6" opacity=".75"/>'
    s += f'<path d="M48 60 H72" stroke="{MER}" stroke-width="2.4"/>'
    for (x, y) in ((40, 120), (58, 132), (76, 118), (48, 104), (70, 106), (84, 128)):
        s += _tanecik(x, y, 4.2, "#8E5BD0")
    for (x, y) in ((52, 124), (66, 120), (78, 136)):
        s += f'<circle cx="{x}" cy="{y}" r="6" fill="#F2C230" stroke="{OBS}" stroke-width="1.2"/>'
    s += f'<text x="60" y="16" text-anchor="middle" {T} font-size="12" fill="{KOB_K}">500 mL</text>'
    s += f'<text x="76" y="64" {T} font-size="10" fill="{MER_K}">çizgi</text>'
    s += f'<circle cx="14" cy="148" r="4" fill="#8E5BD0" stroke="{OBS}" stroke-width="1"/><text x="21" y="152" {T} font-size="10" fill="{OBS}">Na</text><text x="35" y="148" {T} font-size="7" fill="{OBS}">+</text>'
    s += f'<circle cx="86" cy="148" r="5" fill="#F2C230" stroke="{OBS}" stroke-width="1"/><text x="93" y="152" {T} font-size="10" fill="{OBS}">SO</text><text x="108" y="155" {T} font-size="7" fill="{OBS}">4</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def seyreltme_karistirma(onek="inf-sey"):
    """Solda seyreltme (n aynı, V artar), sağda karıştırma (moller toplanır)."""
    s = Svg(onek)
    Wd, Hd = 400, 128
    s += f'<rect width="{Wd}" height="{Hd}" rx="12" fill="#F2FAF7"/>'
    s += _beher(16, 100, 50, 60, .7)
    s += _beher(108, 100, 74, 80, .82, "#BFE8EA")
    nok = [(6, 10), (22, 18), (36, 8), (12, 28), (30, 30), (40, 22)]
    for dx, dy in nok:
        s += _tanecik(20 + dx, 100 - 40 + dy, 3.8, "#2B50B5")
    for dx, dy in nok:
        s += _tanecik(116 + dx * 1.4, 100 - 58 + dy * 1.6, 3.8, "#2B50B5")
    s += f'<path d="M70 64 H100" stroke="{OBS}" stroke-width="2.4"/><path d="M100 64 l-8 -5 v10 Z" fill="{OBS}"/>'
    s += f'<path d="M85 40 C85 40 80 47 80 50 a5 5 0 0 0 10 0 C90 47 85 40 85 40 Z" fill="#7FCFE0" stroke="{OBS}" stroke-width="1.4"/>'
    s += f'<text x="98" y="122" text-anchor="middle" {T} font-size="13" fill="{GOL_K}">su ekle: n aynı, V artar</text>'
    s += f'<path d="M200 12 V118" stroke="#CFDCE0" stroke-width="2" stroke-dasharray="5 4"/>'
    s += _beher(214, 70, 38, 44, .7)
    s += _beher(214, 118, 38, 40, .7, "#F6D9A8")
    for dx, dy in ((6, 6), (20, 12), (12, 18)):
        s += _tanecik(218 + dx, 70 - 30 + dy, 3.4, "#2B50B5")
    for dx, dy in ((8, 8), (22, 16)):
        s += _tanecik(218 + dx, 118 - 26 + dy, 3.4, "#2B50B5")
    s += f'<path d="M258 50 C276 56 280 64 290 70 M258 100 C276 94 280 86 290 80" stroke="{OBS}" stroke-width="2.2" fill="none"/><path d="M296 75 l-10 -7 v14 Z" fill="{OBS}"/>'
    s += _beher(306, 104, 76, 82, .8, "#CDE9D9")
    for dx, dy in ((8, 12), (24, 22), (40, 10), (56, 26), (16, 34), (34, 40), (52, 44), (62, 14)):
        s += _tanecik(310 + dx, 104 - 62 + dy, 3.6, "#2B50B5")
    s += f'<text x="300" y="122" text-anchor="middle" {T} font-size="13" fill="{KEH_K}">karıştır: Σn / ΣV</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def kristal_kabi(onek="inf-kri"):
    """Câbir kutusu: buharlaşma kabında doyan çözelti ve ayrılan kristaller (temsilî)."""
    s = Svg(onek)
    Wd, Hd = 120, 100
    s += f'<rect width="{Wd}" height="{Hd}" rx="10" fill="#FFF7E6"/>'
    s += f'<rect x="20" y="80" width="80" height="12" rx="4" fill="#B8553A" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="M48 80 q6 -14 12 -4 q4 -10 12 4 Z" fill="{KEH}" stroke="{MER_K}" stroke-width="1.4"/>'
    s += f'<path d="M14 54 Q60 86 106 54 Z" fill="#E8F6F8" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M24 60 Q60 80 96 60 Z" fill="#8FD3D6"/>'
    for (x, y, a) in ((40, 62, 0), (56, 66, 20), (70, 64, -15), (82, 60, 10), (48, 70, 30)):
        s += f'<path d="M{x} {y - 5} l5 5 l-5 5 l-5 -5 Z" fill="#FFFFFF" stroke="#5E8496" stroke-width="1.2" transform="rotate({a} {x} {y})"/>'
    for k in range(3):
        s += f'<path d="M{44 + k * 16} 46 q-8 -10 2 -20 q8 -8 0 -18" stroke="#A9C4CC" stroke-width="3" fill="none" stroke-linecap="round"/>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def donma_termometreleri(onek="inf-ter"):
    """1 kg suda 1'er mol: saf su 0 · glikoz −1,86 · NaCl −3,72 · CaCl2 −5,58 °C (ideal; K_d = 1,86)."""
    s = Svg(onek)
    Wd, Hd = 400, 138
    s += f'<rect width="{Wd}" height="{Hd}" rx="12" fill="#F2F7FC"/>'
    s += f'<text x="200" y="15" text-anchor="middle" {T} font-size="12" fill="{SOLUK}">1 kg suda 1 mol madde · donmaya başlama sıcaklığı</text>'
    veri = [("saf su", "", 0), ("glikoz", "1 tanecik", -1.86), ("NaCl", "2 tanecik", -3.72), ("CaCl", "3 tanecik", -5.58)]
    y0, y1 = 30, 96
    Y = lambda t: y0 + (y1 - y0) * (-t) / 6
    for k, (ad, alt, t) in enumerate(veri):
        x = 30 + k * 98
        s += f'<rect x="{x - 7}" y="22" width="14" height="86" rx="7" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
        s += f'<circle cx="{x}" cy="110" r="10" fill="{MER}" stroke="{OBS}" stroke-width="2"/>'
        s += f'<rect x="{x - 3.5}" y="{f(Y(t))}" width="7" height="{f(110 - Y(t))}" fill="{MER}"/>'
        for j in range(0, 7, 2):
            s += f'<path d="M{x + 7} {f(Y(-j))} h5" stroke="{OBS}" stroke-width="1.2"/>'
        deger = "0 °C" if t == 0 else f"{t:.2f}".replace(".", ",").replace("-", "−") + " °C"
        s += f'<text x="{x + 15}" y="{f(Y(t) + 5)}" {T} font-size="14" fill="{KOB_K}">{deger}</text>'
        adt = ad + ('<tspan font-size="9" dy="3">2</tspan>' if ad == "CaCl" else "")
        s += f'<text x="{x + 15}" y="{f(min(Y(t) + 22, 118))}" {T} font-size="12" fill="{OBS}">{adt}</text>'
        if alt:
            s += f'<text x="{x}" y="132" text-anchor="middle" {T} font-size="11" fill="{SOLUK}">{alt}</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def kissa_donma(onek="inf-kd"):
    """Kıssa 3: 0,5 mol / 1 kg su · donmaya başlama sıcaklığı X −2,79 · Y −0,93 · Z −1,86 °C."""
    s = Svg(onek)
    Wd, Hd = 200, 150
    s += f'<rect width="{Wd}" height="{Hd}" rx="10" fill="#FFFFFF"/>'
    x0, y0, yalt = 46, 26, 132
    Y = lambda t: y0 + (yalt - y0) * (-t) / 3
    s += f'<path d="M{x0} {y0} H190" stroke="{OBS}" stroke-width="2"/><path d="M{x0} {y0 - 6} V{yalt + 4}" stroke="{OBS}" stroke-width="2"/>'
    for t in (-1, -2, -3):
        s += f'<path d="M{x0} {f(Y(t))} H190" stroke="#E2E8EE" stroke-width="1.2"/><text x="{x0 - 5}" y="{f(Y(t) + 5)}" text-anchor="end" {T} font-size="13" fill="{OBS}">{t}</text>'.replace(">-", ">−")
    s += f'<text x="{x0 - 5}" y="{y0 + 5}" text-anchor="end" {T} font-size="13" fill="{OBS}">0</text>'
    for k, (ad, t, c) in enumerate((("X", -2.79, MER), ("Y", -.93, GOL), ("Z", -1.86, KOB))):
        x = 66 + k * 42
        s += f'<rect x="{x}" y="{y0}" width="26" height="{f(Y(t) - y0)}" fill="{c}" stroke="{OBS}" stroke-width="1.6"/>'
        s += f'<text x="{x + 13}" y="{y0 - 7}" text-anchor="middle" {B} font-size="15" fill="{OBS}">{ad}</text>'
        s += f'<text x="{x + 13}" y="{f(Y(t) + 15)}" text-anchor="middle" {T} font-size="12" fill="{OBS}">{str(t).replace(".", ",").replace("-", "−")}</text>'
    s += f'<text x="8" y="14" {T} font-size="11" fill="{SOLUK}">°C</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info grafik")


def ustad_buharlasma(onek="inf-ub"):
    """Üstad 3: 500 mL, 0,4 M X çözeltisi; derişim = 0,2/(0,5 − x) mol/L; 400 mL'de 2,0 M'de doyar, sonra sabit."""
    s = Svg(onek)
    Wd, Hd = 220, 176
    s += f'<rect width="{Wd}" height="{Hd}" rx="10" fill="#FFFDF7"/>'
    x0, y0, x1, y1 = 40, 146, 206, 14
    X = lambda v: x0 + (x1 - x0) * v / 450
    Y = lambda m: y0 - (y0 - y1) * m / 2.4
    for v in (100, 200, 300, 400):
        s += f'<path d="M{f(X(v))} {y0} V{y1}" stroke="#E8E1CC" stroke-width="1.2"/>'
    for m in (.4, 1.2, 2.0):
        s += f'<path d="M{x0} {f(Y(m))} H{x1}" stroke="#E8E1CC" stroke-width="1.2"/>'
    pts = [(X(v), Y(.2 / (.5 - v / 1000))) for v in range(0, 401, 20)] + [(X(450), Y(2.0))]
    s += f'<path d="M{x0} {y1 - 4} V{y0} H{x1 + 4}" fill="none" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="{"M" + " L".join(f"{f(a)} {f(b)}" for a, b in pts)}" fill="none" stroke="#1D3A8A" stroke-width="3.4" stroke-linejoin="round"/>'
    s += f'<path d="M{f(X(400))} {y0} V{f(Y(2.0))}" stroke="#C9952B" stroke-width="1.6" stroke-dasharray="4 3"/>'
    for v, m in ((0, .4), (400, 2.0), (450, 2.0)):
        s += f'<circle cx="{f(X(v))}" cy="{f(Y(m))}" r="4" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
    for m, et in ((.4, "0,4"), (2.0, "2,0")):
        s += f'<text x="{x0 - 5}" y="{f(Y(m) + 5)}" text-anchor="end" {T} font-size="13" fill="{OBS}">{et}</text>'
    for v in (0, 400):
        s += f'<text x="{f(X(v))}" y="{y0 + 16}" text-anchor="middle" {T} font-size="13" fill="{OBS}">{v}</text>'
    s += f'<text x="{x1}" y="{y0 + 28}" text-anchor="end" {T} font-size="11" fill="{SOLUK}">buharlaşan su (mL)</text>'
    s += f'<text x="{x0 + 4}" y="{y1 + 2}" {T} font-size="11" fill="{SOLUK}">M</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info")


def ozet_joje(onek="inf-oj"):
    """Hülasa koyu kartı: açık panelde %, ppm, M üç kap."""
    s = Svg(onek)
    Wd, Hd = 300, 74
    s += f'<rect width="{Wd}" height="{Hd}" rx="12" fill="#F4FAFB"/>'
    for k, (et, c) in enumerate((("%", "#8ED8DA"), ("ppm", "#F7C0D4"), ("M", "#B9C8F2"))):
        x = 26 + k * 96
        s += _beher(x, 64, 50, 52, .66, c)
        s += f'<text x="{x + 25}" y="44" text-anchor="middle" {B} font-size="{18 if k == 1 else 22}" fill="{OBS}">{et}</text>'
    return s.cikti(f"0 0 {Wd} {Hd}", cls="info ozet-mol")
