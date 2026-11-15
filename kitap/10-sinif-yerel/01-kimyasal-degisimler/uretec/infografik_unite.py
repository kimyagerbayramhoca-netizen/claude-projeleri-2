"""Kimyasal Değişimler · üniteye özel bilgi grafikleri ({{info|ad}}; kur_ortak önek verir: fn(onek, *arg)).

Tanecik modelleri ortak `molekul.molekul_ciz` ile çizilir (aynı 3B top-çubuk görünüm). Bütün sayılar dogrula.py'de
denetlenir; burada yalnız çizim vardır. SVG yazılarında kontur yok; oklar yol (path) olarak çizilir.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, selcuklu_yildizi, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, GOL_AA, DERIN, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A,
                           ALTIN, ALTIN_K, ALTIN_A, LAJVER, ZUMRUT, GUM, GUM_K, GUM_A, ATOM)
from cizim import molekul as M
import kars_parcalar as P

T = 'font-family="Nunito" font-weight="800"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'
OZEL = {"H2": ([("H", (-.37, 0, 0)), ("H", (.37, 0, 0))], [(0, 1, 1)]), "C": ([("C", (0, 0, 0))], [])}
RENK = {"Ag": "#C3CBD3", "Ba": "#6FBF8E", "K": "#A57BE0", "Zn": "#8E9AAB", "Fe2": "#D96B2B", "Cu2": "#3D8FD6"}


def _mol(s, ad, x, y, olcek=26, donus=(0, 0, 0), yg=False):
    A, Bg = OZEL[ad] if ad in OZEL else M._geometri(ad)
    svg, _ = M.molekul_ciz(s, A, Bg, donus, olcek, yer_golgesi=yg)
    return f'<g transform="translate({f(x)} {f(y)})">{svg}</g>'


def _kure(s, x, y, r, renk, yazi="", yazi_renk="#FFFFFF"):
    g = M._kure_gradyan(s, renk, "ik")
    o = f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{g}" stroke="{koyu(renk, .55)}" stroke-width="{f(max(.8, r * .06))}"/>'
    o += f'<ellipse cx="{f(x - r * .35)}" cy="{f(y - r * .4)}" rx="{f(r * .26)}" ry="{f(r * .16)}" fill="#FFFFFF" opacity=".8" transform="rotate(-35 {f(x - r * .35)} {f(y - r * .4)})"/>'
    if yazi:
        fs = r * (.9 if len(yazi) <= 1 else .72)
        o += f'<text x="{f(x)}" y="{f(y + fs * .36)}" text-anchor="middle" {B} font-size="{f(fs)}" fill="{yazi_renk}">{yazi}</text>'
    return o


def _yuk(x, y, yazi, r=11):
    """İyon yükü rozeti: beyaz daire içinde +, 2+, −, 2−."""
    fs = r * (1.5 if len(yazi) == 1 else 1.05)
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6"/>'
            f'<text x="{f(x)}" y="{f(y + fs * .36)}" text-anchor="middle" {B} font-size="{f(fs)}" fill="{OBS}">{yazi}</text>')


def _iyon(s, x, y, tur, k=1.55):
    """Çözeltideki iyonlar (tanecik modeli); k: büyütme."""
    if tur == "H+":
        return _kure(s, x, y, 11 * k, ATOM["H"], "H", OBS) + _yuk(x + 11 * k, y - 11 * k, "+", 8 * k)
    if tur == "OH-":
        return _kure(s, x - 6 * k, y, 15 * k, ATOM["O"], "O") + _kure(s, x + 12 * k, y - 9 * k, 9 * k, ATOM["H"]) + _yuk(x + 14 * k, y + 12 * k, "−", 8 * k)
    if tur == "Na+":
        return _kure(s, x, y, 15 * k, ATOM["Na"], "Na") + _yuk(x + 14 * k, y - 13 * k, "+", 8 * k)
    if tur == "Cl-":
        return _kure(s, x, y, 19 * k, ATOM["Cl"], "Cl") + _yuk(x + 17 * k, y - 16 * k, "−", 8 * k)
    if tur == "Ca2+":
        return _kure(s, x, y, 17 * k, ATOM["Ca"], "Ca", OBS) + _yuk(x + 16 * k, y - 15 * k, "2+", 9 * k)
    if tur == "CO3":
        o = _kure(s, x, y, 10 * k, ATOM["C"])
        for j in range(3):
            a = -math.pi / 2 + j * 2 * math.pi / 3
            o += _kure(s, x + 16 * k * math.cos(a), y + 16 * k * math.sin(a), 10 * k, ATOM["O"])
        return o + _yuk(x + 22 * k, y + 16 * k, "2−", 9 * k)
    raise ValueError(tur)


def _kap(s, x, y, w, h, su="#BFE7EF", ad="", alt=""):
    """Beher: (x, y) sol üst. Su seviyesi %78."""
    g = s.lin([(0, "#FFFFFF", .95), (1, "#E3F2F4", .85)], 0, 0, 1, 0, ad="cm")
    o = [f'<path d="M{f(x)} {f(y)} V{f(y + h - 14)} Q{f(x)} {f(y + h)} {f(x + 14)} {f(y + h)} H{f(x + w - 14)} Q{f(x + w)} {f(y + h)} {f(x + w)} {f(y + h - 14)} V{f(y)}" fill="{g}" stroke="{OBS}" stroke-width="3.4"/>',
         f'<path d="M{f(x + 3)} {f(y + h * .22)} H{f(x + w - 3)} V{f(y + h - 14)} Q{f(x + w - 3)} {f(y + h - 3)} {f(x + w - 14)} {f(y + h - 3)} H{f(x + 14)} Q{f(x + 3)} {f(y + h - 3)} {f(x + 3)} {f(y + h - 14)} Z" fill="{su}" opacity=".85"/>',
         f'<path d="M{f(x - 8)} {f(y)} H{f(x + 10)}" stroke="{OBS}" stroke-width="3.4" stroke-linecap="round"/>',
         f'<path d="M{f(x + 12)} {f(y + h * .3)} V{f(y + h - 20)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity=".6"/>']
    if ad:
        o.append(_alt(ad, x + w / 2, y + h + 40, 30, OBS))
    if alt:
        o.append(_alt(alt, x + w / 2, y + h + 72, 22, GUM_K, font=T))
    return "".join(o)


def _ok(x0, y0, x1, y1, renk=OBS, k=5, uc=16):
    a = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - uc * math.cos(a - .45), y1 - uc * math.sin(a - .45))
    p2 = (x1 - uc * math.cos(a + .45), y1 - uc * math.sin(a + .45))
    return (f'<path d="M{f(x0)} {f(y0)} L{f(x1 - uc * .6 * math.cos(a))} {f(y1 - uc * .6 * math.sin(a))}" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"/>'
            f'<path d="M{f(x1)} {f(y1)} L{nok(p1)} L{nok(p2)} Z" fill="{renk}"/>')


def _alt(metin, x, y, fs, renk=OBS, anchor="middle", font=B):
    """Yazı içinde _2 → alt simge, ^{…} → üst simge (tspan dy)."""
    import re
    parca = re.split(r"(_\d+|\^\{[^}]*\})", metin)
    o = [f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(fs)}" fill="{renk}">']
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


def _kutu(x, y, w, h, renk="#FFFFFF", cz=OBS, r=18, kesik=False):
    k = ' stroke-dasharray="10 7"' if kesik else ""
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{renk}" stroke="{cz}" stroke-width="3"{k}/>'


# ------------------------------------------------------------------ 1. DURAK · tanecik gözüyle: donma (fiziksel) / yanma (kimyasal)

def tanecik_iki_olay(onek="kz-tan"):
    s = Svg(onek)
    W, H = 1300, 470
    r = RNG(5)
    for p, (x0, baslik, renk) in enumerate(((0, "Donma · fiziksel", GOL_K), (665, "Yanma · kimyasal", MER_K))):
        s += _kutu(x0, 0, 635, H, "#FFFFFF" if p else "#F6FBFC", koyu(renk, .1), 24)
        s += f'<text x="{x0 + 318}" y="46" text-anchor="middle" {B} font-size="34" fill="{renk}">{baslik}</text>'
        s += _kutu(x0 + 22, 70, 250, 280, "#EAF6F8" if p == 0 else "#FFF4EA", "#9FB2BC", 16)
        s += _kutu(x0 + 362, 70, 250, 280, "#EAF0FA" if p == 0 else "#FFF4EA", "#9FB2BC", 16)
        s += _ok(x0 + 284, 210, x0 + 350, 210, renk, 6)
    # donma: sıvıda dağınık, buzda düzenli H2O
    for (x, y) in ((70, 120), (180, 110), (110, 200), (220, 210), (70, 300), (170, 300)):
        s += _mol(s, "H2O", x, y, 40, (r.uniform(-40, 40), r.uniform(-60, 60), r.uniform(0, 360)))
    for i in range(3):
        for j in range(3):
            x = 410 + i * 76 + (38 if j % 2 else 0) - 12
            y = 120 + j * 82
            s += _mol(s, "H2O", x, y, 30, (0, 0, 180 if (i + j) % 2 else 0))
    for i in range(3):
        for j in range(3):
            x = 410 + i * 76 + (38 if j % 2 else 0) - 12
            y = 120 + j * 82
            if i < 2:
                s += f'<path d="M{f(x + 20)} {f(y)} H{f(x + 56)}" stroke="#7FA6C8" stroke-width="2.4" stroke-dasharray="4 4"/>'
    s += f'<text x="317" y="198" text-anchor="middle" {T} font-size="20" fill="{GOL_K}">ısı</text><text x="317" y="246" text-anchor="middle" {T} font-size="20" fill="{GOL_K}">verir</text>'
    s += f'<text x="147" y="384" text-anchor="middle" {T} font-size="25" fill="{OBS}">su (sıvı)</text><text x="487" y="384" text-anchor="middle" {T} font-size="25" fill="{OBS}">buz (katı)</text>'
    s += _alt("Aynı H_2O, yeni düzen", 318, 438, 30, GOL_K)
    # yanma: C + O2 → CO2
    for k, (x, y) in enumerate(((725, 120), (850, 160), (735, 250), (865, 300))):
        s += _mol(s, "C", x, y, 52)
    for k, (x, y) in enumerate(((810, 225), (745, 320), (875, 95))):
        s += _mol(s, "O2", x, y, 38, (10, 25, r.uniform(-40, 40)))
    for k, (x, y) in enumerate(((1095, 115), (1185, 185), (1090, 255), (1180, 315))):
        s += _mol(s, "CO2", x, y, 34, (15, 30, r.uniform(-20, 20)))
    s += f'<text x="982" y="190" text-anchor="middle" {T} font-size="20" fill="{MER_K}">ısı ve</text><text x="982" y="246" text-anchor="middle" {T} font-size="20" fill="{MER_K}">ışık</text>'
    s += _alt("C ve O_2", 812, 384, 25, OBS, font=T)
    s += _alt("CO_2", 1152, 384, 25, OBS, font=T)
    s += _alt("Yeni tanecik: CO_2", 983, 438, 30, MER_K)
    return s.cikti(f"0 0 {W} {H}", cls="info tanecik")


# ------------------------------------------------------------------ 1. DURAK · kimyasal değişimin göstergeleri

def gostergeler(onek="kz-gos"):
    s = Svg(onek)
    W, H = 640, 420
    ad = ["gaz çıkışı", "renk", "çökelek", "ısı · ışık", "koku", "sıcaklık", "pH", "iletkenlik"]
    for i, a in enumerate(ad):
        cx, cy = 80 + (i % 4) * 160, 92 + (i // 4) * 200
        s += f'<rect x="{cx - 66}" y="{cy - 66}" width="132" height="132" rx="26" fill="{[GOL_AA, KEH_A, KOB_A, MER_A][i % 4]}" stroke="{OBS}" stroke-width="3"/>'
        g = ""
        if i == 0:
            g = (f'<path d="M{cx - 30} {cy - 30} V{cy + 30} Q{cx - 30} {cy + 40} {cx - 20} {cy + 40} H{cx + 20} Q{cx + 30} {cy + 40} {cx + 30} {cy + 30} V{cy - 30}" fill="#DDF2F4" stroke="{OBS}" stroke-width="3"/>'
                 + "".join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{rr}" fill="#FFFFFF" stroke="{GOL_K}" stroke-width="2.4"/>' for dx, dy, rr in ((-12, 22, 6), (8, 8, 7), (-4, -10, 5), (12, -26, 6), (-14, -40, 4))))
        elif i == 1:
            g = (f'<circle cx="{cx - 24}" cy="{cy}" r="20" fill="{KOB}" stroke="{OBS}" stroke-width="3"/>' + _ok(cx - 2, cy, cx + 6, cy, OBS, 4, 12)
                 + f'<circle cx="{cx + 28}" cy="{cy}" r="20" fill="{ZUMRUT}" stroke="{OBS}" stroke-width="3"/>')
        elif i == 2:
            g = (f'<path d="M{cx - 30} {cy - 30} V{cy + 30} Q{cx - 30} {cy + 40} {cx - 20} {cy + 40} H{cx + 20} Q{cx + 30} {cy + 40} {cx + 30} {cy + 30} V{cy - 30}" fill="#E8F4F6" stroke="{OBS}" stroke-width="3"/>'
                 f'<path d="M{cx - 27} {cy + 22} Q{cx} {cy + 12} {cx + 27} {cy + 22} V{cy + 30} Q{cx + 27} {cy + 37} {cx + 20} {cy + 37} H{cx - 20} Q{cx - 27} {cy + 37} {cx - 27} {cy + 30} Z" fill="#FFFFFF" stroke="{GUM_K}" stroke-width="2"/>'
                 + "".join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="3" fill="{GUM_K}"/>' for dx, dy in ((-10, 4), (6, -6), (12, 10), (-4, -14))))
        elif i == 3:
            g = (f'<path d="M{cx} {cy + 34} C{cx - 26} {cy + 34} {cx - 30} {cy + 10} {cx - 18} {cy - 6} C{cx - 12} {cy - 14} {cx - 6} {cy - 22} {cx - 6} {cy - 34} C{cx + 10} {cy - 22} {cx + 16} {cy - 12} {cx + 14} {cy} C{cx + 20} {cy - 6} {cx + 22} {cy - 14} {cx + 22} {cy - 18} C{cx + 34} {cy} {cx + 28} {cy + 34} {cx} {cy + 34} Z" fill="{KEH}" stroke="{MER_K}" stroke-width="3"/>'
                 f'<path d="M{cx} {cy + 34} C{cx - 12} {cy + 34} {cx - 12} {cy + 18} {cx - 4} {cy + 8} C{cx + 2} {cy + 16} {cx + 12} {cy + 22} {cx} {cy + 34} Z" fill="#FFF0B8"/>')
        elif i == 4:
            g = (f'<path d="M{cx - 26} {cy + 6} H{cx + 22} V{cy + 26} Q{cx + 22} {cy + 38} {cx + 10} {cy + 38} H{cx - 14} Q{cx - 26} {cy + 38} {cx - 26} {cy + 26} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
                 + "".join(f'<path d="M{cx + dx} {cy} q-8 -10 0 -20 q8 -10 0 -20" stroke="{MER}" stroke-width="3.4" fill="none" stroke-linecap="round"/>' for dx in (-12, 2, 16)))
        elif i == 5:
            g = (f'<rect x="{cx - 9}" y="{cy - 40}" width="18" height="60" rx="9" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
                 f'<circle cx="{cx}" cy="{cy + 28}" r="15" fill="{MER}" stroke="{OBS}" stroke-width="3"/><rect x="{cx - 4}" y="{cy - 14}" width="8" height="36" fill="{MER}"/>'
                 + "".join(f'<path d="M{cx + 12} {cy - 30 + k * 12} h8" stroke="{OBS}" stroke-width="2"/>' for k in range(4)))
        elif i == 6:
            cs = ["#E2533D", "#F08A3A", "#F2C230", "#7BC67A", "#3A9CC8", "#2B50B5", "#6A3FA0"]
            g = "".join(f'<rect x="{cx - 42 + k * 12}" y="{cy - 12}" width="12" height="34" fill="{c}"/>' for k, c in enumerate(cs))
            g += f'<rect x="{cx - 42}" y="{cy - 12}" width="84" height="34" fill="none" stroke="{OBS}" stroke-width="3"/><path d="M{cx - 6} {cy - 36} v18 M{cx - 12} {cy - 24} l6 6 l6 -6" stroke="{OBS}" stroke-width="3" fill="none"/>'
        else:
            g = (f'<path d="M{cx} {cy - 38} C{cx - 22} {cy - 38} {cx - 28} {cy - 14} {cx - 16} {cy} C{cx - 10} {cy + 8} {cx - 10} {cy + 14} {cx - 10} {cy + 18} H{cx + 10} C{cx + 10} {cy + 14} {cx + 10} {cy + 8} {cx + 16} {cy} C{cx + 28} {cy - 14} {cx + 22} {cy - 38} {cx} {cy - 38} Z" fill="#FFF3B8" stroke="{OBS}" stroke-width="3"/>'
                 f'<path d="M{cx - 10} {cy + 24} h20 M{cx - 8} {cy + 31} h16" stroke="{OBS}" stroke-width="3"/>'
                 + "".join(f'<path d="M{cx + 30 * math.cos(a)} {cy - 14 + 30 * math.sin(a)} l{8 * math.cos(a)} {8 * math.sin(a)}" stroke="{KEH_K}" stroke-width="3" stroke-linecap="round"/>' for a in (-2.6, -1.57, -.55)))
        s += g
        s += f'<text x="{cx}" y="{cy + 98}" text-anchor="middle" {T} font-size="24" fill="{OBS}">{a}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info gostergeler")


# ------------------------------------------------------------------ 2. DURAK · atomlar korunur, moleküller değişir

def korunum_model(onek="kz-kor"):
    s = Svg(onek)
    W, H = 1300, 450
    s += _kutu(0, 60, 470, 240, "#F2F7FC", "#9FB2BC", 22)
    s += _kutu(620, 60, 470, 240, "#FFF6EA", "#9FB2BC", 22)
    s += f'<text x="235" y="42" text-anchor="middle" {T} font-size="24" fill="{GUM_K}">TEPKENLER</text><text x="855" y="42" text-anchor="middle" {T} font-size="24" fill="{GUM_K}">ÜRÜNLER</text>'
    s += _mol(s, "CH4", 125, 180, 62, (10, 20, 5))
    s += _mol(s, "O2", 330, 120, 48, (10, 25, 0)) + _mol(s, "O2", 340, 230, 48, (10, 25, 10))
    s += _mol(s, "CO2", 745, 180, 46, (15, 30, 0))
    s += _mol(s, "H2O", 950, 130, 52) + _mol(s, "H2O", 970, 240, 52, (0, 0, 20))
    s += _ok(486, 180, 604, 180, OBS, 7, 22)
    s += _alt("CH_4 + 2O_2", 235, 350, 36)
    s += _alt("CO_2 + 2H_2O", 855, 350, 36)
    # atom sayım çizelgesi
    x0 = 1120
    s += _kutu(x0, 60, 180, 290, "#FFFFFF", OBS, 16)
    s += f'<text x="{x0 + 90}" y="96" text-anchor="middle" {T} font-size="21" fill="{GUM_K}">ATOM SAYIMI</text>'
    for k, (el, a, b) in enumerate((("C", 1, 1), ("H", 4, 4), ("O", 4, 4))):
        yy = 146 + k * 52
        s += f'<circle cx="{x0 + 34}" cy="{yy - 10}" r="16" fill="{ATOM[el]}" stroke="{OBS}" stroke-width="2"/>'
        s += f'<text x="{x0 + 34}" y="{yy - 2}" text-anchor="middle" {B} font-size="22" fill="{OBS if el == "H" else "#FFFFFF"}">{el}</text>'
        s += f'<text x="{x0 + 112}" y="{yy}" text-anchor="middle" {B} font-size="30" fill="{OBS}">{a} = {b}</text>'
    s += f'<path d="M{x0 + 14} 302 H{x0 + 166}" stroke="{OBS}" stroke-width="2"/>'
    s += f'<text x="{x0 + 90}" y="336" text-anchor="middle" {T} font-size="21" fill="{GOL_K}">molekül: 3 ve 3</text>'
    s += f'<text x="650" y="426" text-anchor="middle" {T} font-size="24" fill="{OBS}">Atomlar yer değiştirdi; hiçbiri kaybolmadı, hiçbiri yoktan var olmadı.</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info korunum")


# ------------------------------------------------------------------ 3. DURAK · nötralleşme tanecik modeli

def asit_baz_model(onek="kz-ab"):
    s = Svg(onek)
    W, H = 1300, 470
    s += _kap(s, 20, 40, 300, 300, "#FFE8DE", "HCl(suda)", "asit: H^{+} verir")
    s += _kap(s, 400, 40, 300, 300, "#E6ECFB", "NaOH(suda)", "baz: OH^{−} verir")
    s += _kap(s, 900, 40, 380, 300, "#E9F7F4", "NaCl(suda) + H_2O", "tuz + su")
    for (x, y) in ((85, 145), (240, 215), (120, 290)):
        s += _iyon(s, x, y, "H+")
    for (x, y) in ((205, 125), (85, 225), (250, 300)):
        s += _iyon(s, x, y, "Cl-")
    for (x, y) in ((465, 135), (640, 215), (500, 295)):
        s += _iyon(s, x, y, "Na+")
    for (x, y) in ((615, 120), (470, 215), (650, 300)):
        s += _iyon(s, x, y, "OH-")
    s += f'<text x="360" y="200" text-anchor="middle" {B} font-size="48" fill="{OBS}">+</text>'
    s += _ok(728, 190, 880, 190, OBS, 7, 22)
    for (x, y) in ((975, 145), (1140, 280), (1210, 150)):
        s += _mol(s, "H2O", x, y, 44, (0, 0, 15))
    for (x, y) in ((1070, 115), (995, 285)):
        s += _iyon(s, x, y, "Na+") + f'<circle cx="{x}" cy="{y}" r="40" fill="none" stroke="{GUM_K}" stroke-width="2.4" stroke-dasharray="6 6"/>'
    for (x, y) in ((1230, 240), (1090, 200)):
        s += _iyon(s, x, y, "Cl-") + f'<circle cx="{x}" cy="{y}" r="44" fill="none" stroke="{GUM_K}" stroke-width="2.4" stroke-dasharray="6 6"/>'
    s += _alt("H^{+} + OH^{−} → H_2O", 805, 26, 30, MER_K)
    s += f'<text x="1090" y="460" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">kesikli halka: seyirci iyon</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info asit-baz")


# ------------------------------------------------------------------ 4. DURAK · kireç döngüsü (Ani harcı)

def kirec_dongusu(onek="kz-kd"):
    """Kireç döngüsü: CaCO₃ —ısı (analiz)→ CaO —+H₂O (sentez)→ Ca(OH)₂ —+CO₂→ CaCO₃. ~42 mm genişlikte okunsun diye iri yazı."""
    s = Svg(onek)
    W, H = 900, 660
    g = s.rad([(0, "#FFF7E6"), (1, "#F4E4C6")], .5, .5, .7, ad="zm")
    s += f'<rect width="{W}" height="{H}" rx="26" fill="{g}"/>'
    dugum = [(450, 120, "CaCO_3"), (720, 470, "CaO"), (180, 470, "Ca(OH)_2")]
    for (x0, y0, x1, y1, et, renk, tx, ty) in ((560, 170, 715, 360, "ısı: analiz", MER_K, 715, 250),
                                              (610, 545, 290, 545, "+ H₂O: sentez", GOL_K, 450, 625),
                                              (185, 360, 340, 170, "+ CO₂", KOB_K, 175, 250)):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        bx, by = mx + (mx - 450) * .3, my + (my - 380) * .3
        s += f'<path d="M{x0} {y0} Q{f(bx)} {f(by)} {x1} {y1}" fill="none" stroke="{renk}" stroke-width="10" stroke-linecap="round"/>'
        a_ = math.atan2(y1 - by, x1 - bx)
        s += f'<path d="M{x1} {y1} L{f(x1 - 32 * math.cos(a_ - .45))} {f(y1 - 32 * math.sin(a_ - .45))} L{f(x1 - 32 * math.cos(a_ + .45))} {f(y1 - 32 * math.sin(a_ + .45))} Z" fill="{renk}"/>'
        gw = 30 + 22 * len(et)
        s += f'<rect x="{f(tx - gw / 2)}" y="{f(ty - 34)}" width="{f(gw)}" height="56" rx="28" fill="#FFFFFF" stroke="{renk}" stroke-width="3"/>'
        s += f'<text x="{f(tx)}" y="{f(ty + 7)}" text-anchor="middle" {B} font-size="38" fill="{renk}">{et}</text>'
    for (x, y, fm), dy in zip(dugum, (78, 86, 86)):
        s += _alt(fm, x, y + dy, 56, OBS)
    # küçük resimler: taş, beyaz toz, kova
    s += f'<path d="M405 92 L430 58 L472 52 L506 76 L512 116 L472 138 L420 132 Z" fill="#D9CDB8" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M680 444 q18 -26 44 -18 q26 -18 44 8 q8 26 -18 36 h-62 q-18 -8 -8 -26 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M136 430 h88 l-9 52 h-70 Z" fill="#9A6B42" stroke="{OBS}" stroke-width="3"/><path d="M140 432 q32 -22 80 0 Z" fill="#F4F2EC" stroke="{OBS}" stroke-width="2"/>'
    s += f'<text x="450" y="360" text-anchor="middle" {B} font-size="40" fill="{ALTIN_K}">kireç</text><text x="450" y="402" text-anchor="middle" {B} font-size="40" fill="{ALTIN_K}">döngüsü</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info kirec")


# ------------------------------------------------------------------ 4. DURAK · tam / eksik yanma + CO güvenliği

def yanma_co(onek="kz-yc"):
    s = Svg(onek)
    W, H = 1300, 420
    for p, (x0, bas, renk, alev) in enumerate(((0, "Tam yanma", GOL_K, "#4FA8E8"), (430, "Eksik yanma", MER_K, "#F08A3A"))):
        s += _kutu(x0, 0, 410, H, "#FFFFFF", koyu(renk, .1), 22)
        s += f'<text x="{x0 + 205}" y="44" text-anchor="middle" {B} font-size="32" fill="{renk}">{bas}</text>'
        fx, fy = x0 + 70, 250
        s += (f'<path d="M{fx} {fy + 40} C{fx - 34} {fy + 40} {fx - 40} {fy + 4} {fx - 22} {fy - 18} C{fx - 14} {fy - 30} {fx - 6} {fy - 42} {fx - 6} {fy - 60} '
              f'C{fx + 16} {fy - 42} {fx + 24} {fy - 26} {fx + 20} {fy - 8} C{fx + 30} {fy - 16} {fx + 30} {fy - 28} {fx + 30} {fy - 32} C{fx + 46} {fy} {fx + 38} {fy + 40} {fx} {fy + 40} Z" fill="{alev}" stroke="{koyu(alev, .4)}" stroke-width="3"/>')
        if p == 1:
            for k in range(4):
                s += f'<circle cx="{fx + 6 + k * 10}" cy="{fy - 80 - k * 26}" r="{10 + k * 4}" fill="#5E6270" opacity="{.55 - k * .1}"/>'
    s += _mol(s, "C", 160, 140, 48) + f'<text x="208" y="152" {B} font-size="38">+</text>' + _mol(s, "O2", 300, 140, 40, (10, 25, 0))
    s += _ok(200, 200, 200, 250, GOL_K, 5, 14)
    s += _mol(s, "CO2", 215, 305, 40, (15, 30, 0))
    s += _alt("C + O_2 → CO_2", 205, 392, 30, GOL_K)
    s += _mol(s, "C", 545, 125, 44) + _mol(s, "C", 600, 125, 44) + f'<text x="636" y="137" {B} font-size="38">+</text>' + _mol(s, "O2", 725, 125, 38, (10, 25, 0))
    s += _ok(640, 180, 640, 230, MER_K, 5, 14)
    s += _mol(s, "CO", 575, 295, 42, (0, 25, 0)) + _mol(s, "CO", 715, 295, 42, (0, 25, 0))
    s += f'<path d="M790 230 l20 36 h-40 Z" fill="{KEH}" stroke="{OBS}" stroke-width="2.4"/><path d="M790 242 v12" stroke="{OBS}" stroke-width="3"/><circle cx="790" cy="260" r="2" fill="{OBS}"/>'
    s += _alt("2C + O_2 → 2CO", 640, 392, 30, MER_K)
    # güvenlik ikonları
    x0 = 862
    s += _kutu(x0, 0, 438, H, "#FFF8E8", KEH_K, 22)
    s += f'<text x="{x0 + 219}" y="44" text-anchor="middle" {B} font-size="30" fill="{KEH_K}">Isınırken güvende kal</text>'
    ik = [("baca: her yıl", "temizlet"), ("CO dedektörü", "tak"), ("menfez açık,", "oda havalansın"), ("sobayı", "söndürüp uyu")]
    for i, (a, b) in enumerate(ik):
        cx, cy = x0 + 110 + (i % 2) * 218, 120 + (i // 2) * 150
        s += f'<circle cx="{cx}" cy="{cy}" r="42" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
        if i == 0:
            s += f'<rect x="{cx - 12}" y="{cy - 30}" width="24" height="48" fill="#5E6270" stroke="{OBS}" stroke-width="2"/><path d="M{cx - 28} {cy + 22} h56" stroke="{OBS}" stroke-width="4"/><path d="M{cx + 16} {cy - 30} l14 -10 M{cx + 18} {cy - 18} l14 -4" stroke="{GOL}" stroke-width="4" stroke-linecap="round"/>'
        elif i == 1:
            s += P.co_dedektoru(cx, cy, 52)
        elif i == 2:
            s += P.menfez(cx - 26, cy - 20, 52, 40) + f'<path d="M{cx + 30} {cy - 8} q10 -6 20 0 M{cx + 30} {cy + 6} q10 -6 20 0" stroke="{GOL}" stroke-width="3" fill="none"/>'
        else:
            s += f'<rect x="{cx - 20}" y="{cy - 22}" width="40" height="44" rx="6" fill="#2E2F36"/><rect x="{cx - 12}" y="{cy - 12}" width="24" height="16" rx="3" fill="#8A93A0"/>'
            s += f'<path d="M{cx + 14} {cy - 36} a10 10 0 1 0 12 12 a8 8 0 1 1 -12 -12 Z" fill="#F0C14A" stroke="{OBS}" stroke-width="2"/>'
        s += f'<text x="{cx}" y="{cy + 64}" text-anchor="middle" {T} font-size="21" fill="{OBS}">{a}</text><text x="{cx}" y="{cy + 88}" text-anchor="middle" {T} font-size="21" fill="{OBS}">{b}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info yanma")


# ------------------------------------------------------------------ 5. DURAK · çökelme tanecik modeli

def cokelme_model(onek="kz-ck"):
    s = Svg(onek)
    W, H = 1300, 470
    s += _kap(s, 20, 40, 300, 300, "#EEF2FA", "CaCl_2(suda)", "berrak")
    s += _kap(s, 400, 40, 300, 300, "#EEF2FA", "Na_2CO_3(suda)", "berrak")
    s += _kap(s, 900, 40, 380, 300, "#EEF2FA", "CaCO_3(k) + NaCl(suda)", "bulanık, dipte çökelek")
    for (x, y) in ((100, 140), (210, 265)):
        s += _iyon(s, x, y, "Ca2+")
    for (x, y) in ((230, 130), (80, 235), (120, 305), (265, 190)):
        s += _iyon(s, x, y, "Cl-")
    for (x, y) in ((460, 125), (640, 150), (470, 300), (650, 300)):
        s += _iyon(s, x, y, "Na+")
    for (x, y) in ((545, 195), (560, 285)):
        s += _iyon(s, x, y, "CO3", 1.3)
    s += f'<text x="360" y="200" text-anchor="middle" {B} font-size="48" fill="{OBS}">+</text>'
    s += _ok(728, 190, 880, 190, OBS, 7, 22)
    # dipte çökelek
    s += f'<path d="M906 300 Q990 282 1090 292 T1274 296 V326 Q1274 337 1263 337 H917 Q906 337 906 326 Z" fill="#FFFFFF" stroke="{GUM_K}" stroke-width="2.4"/>'
    for k in range(9):
        x = 940 + k * 36
        s += _kure(s, x, 314 + (k % 2) * 6, 9, ATOM["Ca"]) + _kure(s, x + 14, 310 + (k % 2) * 6, 7, ATOM["O"])
    for (x, y) in ((975, 120), (1165, 245), (1090, 235), (1250, 255)):
        s += _iyon(s, x, y, "Na+") + f'<circle cx="{x}" cy="{y}" r="40" fill="none" stroke="{GUM_K}" stroke-width="2.4" stroke-dasharray="6 6"/>'
    for (x, y) in ((1100, 140), (980, 225), (1230, 160)):
        s += _iyon(s, x, y, "Cl-") + f'<circle cx="{x}" cy="{y}" r="44" fill="none" stroke="{GUM_K}" stroke-width="2.4" stroke-dasharray="6 6"/>'
    s += _alt("Ca^{2+} + CO_3^{2−} → CaCO_3(k)", 805, 26, 28, MER_K)
    s += f'<text x="1090" y="460" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">kesikli halka: seyirci iyon</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info cokelme")


# ------------------------------------------------------------------ 5. DURAK · Medeniyetimizden: süzme (temsilî)

def suzme(onek="kz-sz"):
    s = Svg(onek)
    W, H = 520, 360
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFF7E6"/>'
    s += f'<path d="M150 330 V60 M150 90 H240" stroke="#8C5A2E" stroke-width="10" stroke-linecap="round"/><rect x="100" y="326" width="320" height="16" rx="6" fill="#8C5A2E"/>'
    s += f'<circle cx="300" cy="96" r="14" fill="none" stroke="#5A4A3E" stroke-width="6"/>'
    cam = s.lin([(0, "#FFFFFF", .95), (1, "#D6EAEE", .8)], 0, 0, 1, 0, ad="cm")
    s += f'<path d="M230 96 H370 L312 180 V236 H288 V180 Z" fill="{cam}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M244 102 H356 L300 176 Z" fill="#FFFFFF" stroke="{GUM_K}" stroke-width="2"/><path d="M262 120 Q300 138 338 120 L300 170 Z" fill="#F2F0EA" stroke="#C9C4B8" stroke-width="1.6"/>'
    for k in range(7):
        s += f'<circle cx="{285 + (k % 4) * 9}" cy="{140 + (k // 4) * 10}" r="4" fill="#D9D4C8"/>'
    s += f'<path d="M300 240 v24" stroke="#7FC8D2" stroke-width="3" stroke-dasharray="4 6"/>'
    s += f'<path d="M248 262 V318 Q248 326 256 326 H344 Q352 326 352 318 V262" fill="{cam}" stroke="{OBS}" stroke-width="3"/><path d="M252 290 H348 V318 Q348 322 344 322 H256 Q252 322 252 318 Z" fill="#BFE7EF"/>'
    s += f'<g transform="rotate(-38 140 120)"><path d="M70 100 H140 V170 Q140 178 132 178 H78 Q70 178 70 170 Z" fill="{cam}" stroke="{OBS}" stroke-width="3"/><path d="M73 130 H137 V170 Q137 175 132 175 H78 Q73 175 73 170 Z" fill="#E6E2D6"/></g>'
    s += f'<path d="M196 92 q14 -6 32 6" stroke="#C9C4B8" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info suzme")


# ------------------------------------------------------------------ 6. DURAK · redoks: demir çivi bakır sülfatta

def redoks_model(onek="kz-rd"):
    s = Svg(onek)
    W, H = 1300, 470
    s += _kap(s, 30, 70, 260, 280, "#5FA4E0", "önce", "CuSO_4 mavi")
    s += _kap(s, 380, 70, 260, 280, "#A9D8C8", "sonra", "renk açıldı, çivi bakırlandı")
    for x0, bakir in ((160, False), (510, True)):
        s += f'<rect x="{x0 - 9}" y="40" width="18" height="250" rx="6" fill="#8E96A2" stroke="{OBS}" stroke-width="3"/><rect x="{x0 - 22}" y="32" width="44" height="14" rx="5" fill="#8E96A2" stroke="{OBS}" stroke-width="3"/><path d="M{x0 - 9} 290 L{x0} 318 L{x0 + 9} 290 Z" fill="#8E96A2" stroke="{OBS}" stroke-width="3"/>'
        if bakir:
            s += f'<rect x="{x0 - 10}" y="140" width="20" height="150" rx="6" fill="#C8743A" opacity=".9"/><path d="M{x0 - 10} 290 L{x0} 318 L{x0 + 10} 290 Z" fill="#C8743A"/>'
            r = RNG(9)
            for k in range(10):
                s += f'<circle cx="{x0 + r.uniform(-16, 16)}" cy="{r.uniform(150, 300)}" r="{r.uniform(3, 6)}" fill="#B05A28"/>'
    s += _ok(312, 200, 360, 200, OBS, 6, 18)
    # büyüteç: elektron aktarımı
    cx, cy, R = 980, 215, 205
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#FFFFFF" stroke="{OBS}" stroke-width="5"/><path d="M{cx - R * .72} {cy + R * .72} L560 330" stroke="{OBS}" stroke-width="3" stroke-dasharray="8 7"/>'
    s += _kure(s, cx - 110, cy - 50, 40, ATOM["Fe"], "Fe")
    s += _kure(s, cx + 110, cy - 50, 34, RENK["Cu2"], "Cu") + _yuk(cx + 142, cy - 82, "2+", 15)
    for k, (ex, ey) in enumerate(((cx - 34, cy - 118), (cx + 6, cy - 128))):
        s += f'<circle cx="{ex}" cy="{ey}" r="15" fill="#F2C230" stroke="{OBS}" stroke-width="2.4"/><path d="M{ex - 7} {ey} h14" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M{cx - 80} {cy - 90} Q{cx} {cy - 170} {cx + 80} {cy - 90}" fill="none" stroke="{KEH_K}" stroke-width="5" stroke-dasharray="10 8"/>'
    s += f'<path d="M{cx + 80} {cy - 90} l-24 -4 l12 -18 Z" fill="{KEH_K}"/>'
    s += _alt("Fe → Fe^{2+} + 2e^{−}", cx - 98, cy + 32, 23, MER_K)
    s += _alt("Cu^{2+} + 2e^{−} → Cu", cx + 98, cy + 32, 23, KOB_K)
    s += f'<text x="{cx - 105}" y="{cy + 70}" text-anchor="middle" {T} font-size="21" fill="{MER_K}">yükseltgenme</text><text x="{cx - 105}" y="{cy + 96}" text-anchor="middle" {B} font-size="20" fill="{GUM_K}">YB 0 → +2</text>'
    s += f'<text x="{cx + 108}" y="{cy + 70}" text-anchor="middle" {T} font-size="21" fill="{KOB_K}">indirgenme</text><text x="{cx + 108}" y="{cy + 96}" text-anchor="middle" {B} font-size="20" fill="{GUM_K}">YB +2 → 0</text>'
    s += _alt("verilen e^{−} = alınan e^{−}", cx, cy + 150, 26, OBS)
    return s.cikti(f"0 0 {W} {H}", cls="info redoks")


# ------------------------------------------------------------------ 6. DURAK · Medeniyetimizden: Marifetnâme (temsilî, yazısız)

def marifetname(onek="kz-mf"):
    s = Svg(onek)
    W, H = 520, 360
    g = s.rad([(0, "#FFF7E0"), (1, "#F0DDB0")], .5, .45, .7, ad="zm")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{g}"/>'
    s += f'<path d="M40 300 Q150 270 260 300 Q370 270 480 300 V320 Q370 292 260 320 Q150 292 40 320 Z" fill="{LAJVER}" stroke="{OBS}" stroke-width="3"/>'
    sayfa = s.lin([(0, "#FFFDF4"), (1, "#F1E6C8")], 0, 0, 0, 1, ad="sy")
    s += f'<path d="M50 60 Q150 34 258 60 V298 Q150 272 50 298 Z" fill="{sayfa}" stroke="{OBS}" stroke-width="2.6"/>'
    s += f'<path d="M470 60 Q370 34 262 60 V298 Q370 272 470 298 Z" fill="{sayfa}" stroke="{OBS}" stroke-width="2.6"/>'
    s += f'<path d="M64 72 Q150 50 246 72 V284 Q150 262 64 284 Z M456 72 Q370 50 274 72 V284 Q370 262 456 284 Z" fill="none" stroke="{ALTIN}" stroke-width="3"/>'
    cx, cy = 156, 172
    for k, (rr, c) in enumerate(((84, "#1D3A8A"), (66, "#2B50B5"), (50, "#13A3A6"), (34, "#F6E7BF"), (18, "#7FB24E"))):
        s += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{c}" stroke="{ALTIN_K}" stroke-width="2"/>'
    for k in range(12):
        a = k * math.pi / 6
        s += f'<circle cx="{f(cx + 75 * math.cos(a))}" cy="{f(cy + 75 * math.sin(a))}" r="3.2" fill="{ALTIN_A}"/>'
    s += f'<circle cx="{cx + 58}" cy="{cy - 6}" r="6" fill="#F0C14A" stroke="{OBS}" stroke-width="1.4"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(366, 120, 34), True)}" fill="{ALTIN_A}" stroke="{ALTIN_K}" stroke-width="2.4"/><circle cx="366" cy="120" r="12" fill="#13A3A6" stroke="{ALTIN_K}" stroke-width="2"/>'
    for k in range(6):
        s += f'<path d="M296 {176 + k * 18} Q366 {170 + k * 18} 438 {176 + k * 18}" stroke="#A8957A" stroke-width="2" fill="none" opacity=".7"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info marifet")


# ------------------------------------------------------------------ kıssa resimleri

def kul_resmi(onek="kz-kul"):
    s = Svg(onek)
    W, H = 420, 300
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#FFF3E2"/>'
    s += f'<path d="M40 150 h130 l-12 120 h-106 Z" fill="#6E7280" stroke="{OBS}" stroke-width="3"/><path d="M44 152 Q105 120 166 152 Z" fill="#B9BCC4" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="M60 140 Q105 110 150 140" stroke="{OBS}" stroke-width="4" fill="none"/>'
    cam = s.lin([(0, "#FFFFFF", .95), (1, "#D6EAEE", .8)], 0, 0, 1, 0, ad="cm")
    s += f'<path d="M230 120 L246 270 H330 L346 120" fill="{cam}" stroke="{OBS}" stroke-width="3"/><path d="M236 170 L248 266 H328 L340 170 Z" fill="#E9E2C8"/>'
    for k, (dx, dy, rr) in enumerate(((268, 230, 7), (300, 210, 9), (286, 186, 6), (312, 176, 5), (276, 160, 5))):
        s += f'<circle cx="{dx}" cy="{dy}" r="{rr}" fill="#FFFFFF" stroke="{KEH_K}" stroke-width="2"/>'
    s += f'<g transform="rotate(30 330 70)"><rect x="310" y="20" width="40" height="80" rx="8" fill="#F4E6C6" stroke="{OBS}" stroke-width="3"/><rect x="318" y="6" width="24" height="18" rx="4" fill="{MER}" stroke="{OBS}" stroke-width="2.4"/></g>'
    s += f'<path d="M292 104 q-4 10 0 20" stroke="#C9B48A" stroke-width="4" stroke-dasharray="3 5" fill="none"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info kissa-resim")


def termit_resmi(onek="kz-ter"):
    s = Svg(onek)
    W, H = 420, 300
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#1E2340"/>'
    for x0, x1 in ((20, 180), (240, 400)):
        s += f'<path d="M{x0} 230 H{x1} V244 H{x0} Z M{x0 + 20} 210 H{x1 - 20} V230 H{x0 + 20} Z M{x0} 196 H{x1} V210 H{x0} Z" fill="#8E96A2" stroke="#0E0F14" stroke-width="2"/>'
    sicak = s.rad([(0, "#FFF4C8", 1), (.4, "#FFB43A", .8), (1, "#FF6A2A", 0)], 210, 220, 110, kull="userSpaceOnUse", ad="sc")
    s += f'<circle cx="210" cy="220" r="110" fill="{sicak}"/>'
    s += f'<path d="M150 70 h120 l-20 70 h-80 Z" fill="#7A6A5A" stroke="#0E0F14" stroke-width="3"/><path d="M200 140 Q206 180 210 210 Q214 180 220 140 Z" fill="#FFD27A"/>'
    s += f'<rect x="196" y="200" width="28" height="50" fill="#FFB43A"/>'
    r = RNG(3)
    for k in range(24):
        a = r.uniform(-math.pi, 0)
        d = r.uniform(40, 120)
        s += f'<path d="M{f(210 + 30 * math.cos(a))} {f(150 + 20 * math.sin(a))} l{f(d * .3 * math.cos(a))} {f(d * .3 * math.sin(a))}" stroke="#FFE08A" stroke-width="3" stroke-linecap="round"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info kissa-resim")


def iletkenlik_grafigi(onek="kz-il"):
    """Ba(OH)₂ çözeltisine H₂SO₄ eklendikçe iletkenlik: K noktasında sıfıra yakın, sonra artar (temsilî)."""
    s = Svg(onek)
    W, H = 520, 420
    x0, y0, x1, y1 = 70, 330, 490, 40
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for k in range(1, 5):
        yy = y0 - (y0 - y1) * k / 4
        s += f'<path d="M{x0} {f(yy)} H{x1}" stroke="#DCE4E8" stroke-width="2"/>'
        xx = x0 + (x1 - x0) * k / 4
        s += f'<path d="M{f(xx)} {y0} V{y1}" stroke="#DCE4E8" stroke-width="2"/>'
    s += f'<path d="M{x0} {y1 - 10} V{y0} H{x1 + 10}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    kx = x0 + (x1 - x0) * .5
    d = f"M{x0} {y1 + 30} C{x0 + 80} {y1 + 90} {kx - 70} {y0 - 40} {kx} {y0 - 8} C{kx + 60} {y0 - 30} {x1 - 60} {y1 + 120} {x1} {y1 + 70}"
    s += f'<path d="{d}" stroke="{KOB}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    s += f'<circle cx="{f(kx)}" cy="{y0 - 8}" r="11" fill="#FFFFFF" stroke="{MER}" stroke-width="5"/><text x="{f(kx)}" y="{y0 - 28}" text-anchor="middle" {B} font-size="34" fill="{MER}">K</text>'
    s += _alt("eklenen H_2SO_4 →", x1, y0 + 40, 25, GUM_K, anchor="end")
    s += f'<text x="{x0 - 6}" y="{y1 - 16}" {T} font-size="25" fill="{GUM_K}">iletkenlik</text>'
    s += f'<text x="{x0 - 14}" y="{y0 + 8}" text-anchor="end" {B} font-size="24" fill="{OBS}">0</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def model_soru(onek="kz-ms"):
    """İmtihan sorusu: kapalı kapta tepkime öncesi ve sonrası tanecikler (4 H₂ + 3 O₂ → 4 H₂O + 1 O₂ artar).
    40 mm genişlikte okunur olsun diye sıkı: iki kutu üst üste değil yan yana, yazılar 34 birim."""
    s = Svg(onek)
    W, H = 520, 330
    for p, x0 in enumerate((0, 300)):
        s += _kutu(x0, 44, 220, 220, "#F6FAFC", "#7F94A2", 18)
        s += f'<text x="{x0 + 110}" y="34" text-anchor="middle" {T} font-size="34" fill="{GUM_K}">{["ÖNCE", "SONRA"][p]}</text>'
    for (x, y) in ((52, 88), (60, 150), (52, 212), (112, 248)):
        s += _mol(s, "H2", x, y, 44, (0, 0, 20))
    for (x, y) in ((168, 86), (160, 160), (176, 226)):
        s += _mol(s, "O2", x, y, 38, (10, 25, 15))
    for (x, y) in ((356, 100), (456, 104), (358, 192), (458, 188)):
        s += _mol(s, "H2O", x, y, 40, (0, 0, 10))
    s += _mol(s, "O2", 412, 246, 34, (10, 25, -15))
    s += _ok(228, 154, 292, 154, OBS, 6, 18)
    s += f'<g transform="translate(260 306)"><circle cx="-96" cy="-2" r="13" fill="{ATOM["H"]}" stroke="{OBS}" stroke-width="2.5"/><text x="-76" y="9" {T} font-size="32">H</text><circle cx="40" cy="-2" r="13" fill="{ATOM["O"]}" stroke="{OBS}" stroke-width="2.5"/><text x="60" y="9" {T} font-size="32">O</text></g>'
    return s.cikti(f"0 0 {W} {H}", cls="info model-soru")


def kutle_grafigi(onek="kz-kg"):
    """Üstad 4: kireç taşı örneği ısıtılırken katı kütlesi (50 g → 36,8 g)."""
    s = Svg(onek)
    W, H = 540, 380
    x0, y0, x1, y1 = 96, 300, 510, 40
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'

    def Y(m):
        return y0 - (y0 - y1) * (m - 30) / 25
    for m in (30, 35, 40, 45, 50, 55):
        s += f'<path d="M{x0} {f(Y(m))} H{x1}" stroke="#E2E8EC" stroke-width="2"/>'
        s += f'<text x="{x0 - 12}" y="{f(Y(m) + 8)}" text-anchor="end" {T} font-size="22" fill="{OBS}">{m}</text>'
    s += f'<path d="M{x0} {y1 - 6} V{y0} H{x1 + 6}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    xa, xb = x0 + 60, x0 + 260
    s += f'<path d="M{x0} {f(Y(50))} H{xa} C{xa + 80} {f(Y(49))} {xb - 70} {f(Y(37.5))} {xb} {f(Y(36.8))} H{x1}" stroke="{MER}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M{xb} {f(Y(36.8))} H{x0}" stroke="{MER}" stroke-width="2.4" stroke-dasharray="7 6"/>'
    s += f'<rect x="{x0 + 6}" y="{f(Y(36.8) - 30)}" width="70" height="26" rx="6" fill="#FFFFFF"/><text x="{x0 + 12}" y="{f(Y(36.8) - 10)}" {B} font-size="24" fill="{MER_K}">36,8</text>'
    s += f'<text x="{x1}" y="{y0 + 40}" text-anchor="end" {T} font-size="24" fill="{GUM_K}">zaman</text>'
    s += f'<text x="{x0 - 4}" y="{y1 - 16}" {T} font-size="24" fill="{GUM_K}">katı kütlesi (g)</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")
