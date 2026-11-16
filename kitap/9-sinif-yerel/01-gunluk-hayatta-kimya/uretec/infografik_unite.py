"""Günlük Hayatta Kimya · İznik–Bursa Yolu — üniteye özel bilgi grafikleri ({{info|ad|arg…}}; kur_ortak ortak
infografik.py'den ÖNCE bakar).

Bütün sayılar uretec/dogrula.py içinde yeniden denetlenir (pH değerleri yaklaşık, deney verileri kurgusal); burada
yalnız çizim vardır. Yazılarda alt/üst simge tspan ile (_yazi: "CO_2", "H^+"); konturlu yazı yok; fontta olmayan
sembol (→ ✓ ★) SVG yazısında kullanılmaz, oklar path ile çizilir.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, DERIN, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A,
                           ALTIN, ALTIN_K, ALTIN_A, LAJVER, ZUMRUT, GUM, GUM_K, GUM_A, ERGUVAN)

T = 'font-family="Nunito" font-weight="800"'
TK = 'font-family="Nunito" font-weight="900"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'
PH_RENK = [(0, "#C8102E"), (2, "#E8412C"), (4, "#F39A1E"), (5.5, "#E9C93A"), (7, "#4DB560"), (8.5, "#1FA6A0"),
           (10, "#2B6CB5"), (12, "#5A3FA6"), (14, "#3A1F70")]


def _tsp(metin, fs):
    """'CO_2', 'H^+', 'OH^−' → tspan'lı SVG metni (alt/üst simge, sonra taban çizgisine dönüş)."""
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
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - uc * math.cos(a), y2 - uc * math.sin(a)
    p1 = (bx + uc * .55 * math.sin(a), by - uc * .55 * math.cos(a))
    p2 = (bx - uc * .55 * math.sin(a), by + uc * .55 * math.cos(a))
    return (f'<path d="M{f(x1)} {f(y1)} L{f(bx)} {f(by)}" stroke="{renk}" stroke-width="{f(k)}" stroke-linecap="round"/>'
            f'<path d="M{f(x2)} {f(y2)} L{f(p1[0])} {f(p1[1])} L{f(p2[0])} {f(p2[1])} Z" fill="{renk}"/>')


def _eksen(x0, y0, x1, y1, xt, yt, xad, yad, fs=24, izgara=True):
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
    if xad:
        o.append(_yazi(x1 + 18, y0 + fs * 2.2, xad, fs, OBS, "end"))
    if yad:
        o.append(_yazi(x0 + 8, y1 - 26, yad, fs, OBS, "start"))
    return "".join(o)


def _ph_renk(ph):
    for (a, ca), (b, cb) in zip(PH_RENK, PH_RENK[1:]):
        if a <= ph <= b:
            return karis(ca, cb, (ph - a) / (b - a))
    return PH_RENK[-1][1]


# ------------------------------------------------------------------ küçük nesne ikonları (pH cetveli, kıssalar)

def _nesne(tur, x, y, o=1.0):
    """Ev ve yol nesneleri: (x, y) ikon ortası; yaklaşık 60×60 birim (o ölçeği)."""
    g = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})" stroke="{OBS}" stroke-width="2.4" stroke-linejoin="round">']
    if tur == "mide":
        g.append('<path d="M-6 -26 C-6 -14 -2 -10 -10 -4 C-22 4 -24 22 -8 26 C8 30 24 20 24 4 C24 -10 12 -14 8 -6 C4 0 4 -18 6 -26 Z" fill="#F7B6B0"/>'
                 '<path d="M-12 10 q8 6 18 0" fill="none" stroke-width="2"/>')
    elif tur == "limon":
        g.append('<ellipse cx="0" cy="4" rx="24" ry="17" fill="#F6D637"/><path d="M-24 4 l-6 -2 M24 4 l6 -2" stroke-width="3"/>'
                 '<path d="M2 -12 q10 -14 22 -10 q-6 12 -22 10 Z" fill="#4E9A44"/>')
    elif tur in ("sise", "sirke"):
        c = "#F2E6C8" if tur == "sirke" else "#BFE6F2"
        g.append(f'<path d="M-8 -28 H8 V-18 L14 -8 V26 Q14 30 10 30 H-10 Q-14 30 -14 26 V-8 L-8 -18 Z" fill="{c}"/>'
                 '<rect x="-10" y="0" width="20" height="16" rx="2" fill="#FFFFFF"/><path d="M-8 -28 H8 V-22 H-8 Z" fill="#B85C3E"/>')
    elif tur == "kutu":
        g.append(f'<rect x="-14" y="-24" width="28" height="52" rx="6" fill="{MER}"/><path d="M-14 -16 H14 M-14 20 H14" stroke="#FFFFFF" stroke-width="3"/>'
                 '<ellipse cx="0" cy="-24" rx="14" ry="4" fill="#C9D2DC"/>')
    elif tur == "domates":
        g.append(f'<circle cx="0" cy="6" r="22" fill="{MER}"/><path d="M-12 -12 L0 -6 L12 -12 L6 -2 L0 -10 L-6 -2 Z" fill="#2F8A3E"/>'
                 '<path d="M-10 0 q-4 8 0 14" fill="none" stroke="#FFFFFF" stroke-width="3"/>')
    elif tur == "sut":
        g.append('<path d="M-14 -24 L-10 26 H10 L14 -24 Z" fill="#FFFFFF"/><path d="M-13 -12 H13" stroke-width="2"/>'
                 '<path d="M-13 -12 L-10 26 H10 L13 -12 Z" fill="#F6F2E6"/>')
    elif tur == "damla":
        g.append('<path d="M0 -28 C0 -28 -20 -2 -20 10 A20 20 0 0 0 20 10 C20 -2 0 -28 0 -28 Z" fill="#9ED8F2"/>'
                 '<path d="M-8 6 q-2 8 4 12" fill="none" stroke="#FFFFFF" stroke-width="3"/>')
    elif tur == "kaplica":
        g.append(f'<path d="M-26 4 Q0 30 26 4 Z" fill="#C9A47A"/><ellipse cx="0" cy="4" rx="26" ry="7" fill="{GOL}"/>'
                 '<path d="M-10 -4 q-6 -8 0 -16 q6 -8 0 -16 M6 -4 q-6 -8 0 -16 q6 -8 0 -14" fill="none" stroke="#7C8898" stroke-width="2.6"/>')
    elif tur == "dalga":
        g.append(f'<path d="M-26 0 q6.5 -10 13 0 t13 0 t13 0 t13 0 V20 H-26 Z" fill="{GOL}"/><path d="M-26 -12 q6.5 -10 13 0 t13 0 t13 0 t13 0" fill="none" stroke="{GOL}" stroke-width="3"/>')
    elif tur == "paket":
        g.append(f'<path d="M-18 -22 H18 V26 H-18 Z" fill="#FFFFFF"/><path d="M-18 -22 L-12 -30 H12 L18 -22" fill="#E8E2D4"/>'
                 f'<rect x="-12" y="-6" width="24" height="16" rx="2" fill="{KOB}"/>')
    elif tur == "sabun":
        g.append('<rect x="-24" y="-6" width="48" height="26" rx="9" fill="#F6C1D9"/><path d="M-14 4 h20" stroke="#FFFFFF" stroke-width="3"/>'
                 '<circle cx="-12" cy="-16" r="6" fill="#FFFFFF"/><circle cx="4" cy="-22" r="8" fill="#FFFFFF"/><circle cx="16" cy="-12" r="4" fill="#FFFFFF"/>')
    elif tur == "tablet":
        g.append('<circle cx="-8" cy="4" r="14" fill="#FFFFFF"/><path d="M-20 4 H4" stroke-width="2"/><circle cx="12" cy="-6" r="11" fill="#FFFFFF"/>')
    elif tur == "bidon":
        g.append(f'<path d="M-18 -18 H6 V-26 H14 V-18 H18 V28 H-18 Z" fill="#FFFFFF"/><path d="M-14 -12 C-26 -6 -26 10 -14 14" fill="none" stroke-width="3"/>'
                 f'<rect x="-10" y="-2" width="24" height="18" rx="2" fill="{KOB_A}"/>')
    elif tur == "acici":
        g.append(f'<path d="M-14 -22 H14 V28 H-14 Z" fill="#E8EEF2"/><rect x="-8" y="-30" width="16" height="9" fill="{MER}"/>'
                 f'<path d="M0 -10 L12 12 H-12 Z" fill="#FFFFFF"/><path d="M0 -4 V4 M0 7.5 V8.5" stroke="{MER}" stroke-width="3"/>')
    g.append("</g>")
    return "".join(g)


# ------------------------------------------------------------------ 1. DURAK · İZNİK

def temel_ihtiyaclar(onek="ui-tem"):
    """Temel ihtiyaçlar ve kimya: ortada çini yıldızında KİMYA, iki yanda altı ihtiyaç kartı."""
    s = Svg(onek)
    W, H = 640, 300
    cx, cy = 320, 150
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    kartlar = [("Beslenme", "gübre · ambalaj", MER, "bugday"), ("Barınma", "çimento · cam", KEH, "ev"), ("Giyinme", "lif · boya", ERGUVAN, "ipek"),
               ("Sağlık", "ilaç · aşı", ZUMRUT, "ilac"), ("Temizlik", "sabun · deterjan", GOL, "sabun"), ("Enerji", "yakıt · pil", KOB, "pil")]
    KW = 228
    for i, (ad, ornek, renk, ikon) in enumerate(kartlar):
        sol = i < 3
        x = 6 if sol else W - 6 - KW
        y = 16 + (i % 3) * 94
        ax, ay = (x + KW, y + 40) if sol else (x, y + 40)
        s += f'<path d="M{f(ax)} {f(ay)} L{cx} {cy}" stroke="{renk}" stroke-width="4" stroke-dasharray="8 6"/>'
        s += f'<rect x="{x}" y="{y}" width="{KW}" height="80" rx="14" fill="{acik(renk, .86)}" stroke="{renk}" stroke-width="3.4"/>'
        s += f'<circle cx="{x + 34}" cy="{y + 40}" r="24" fill="#FFFFFF" stroke="{renk}" stroke-width="3"/>'
        s += _ihtiyac_ikonu(ikon, x + 34, y + 40, renk)
        s += _yazi(x + 66, y + 36, ad, 26, OBS, "start", B)
        s += _yazi(x + 66, y + 63, ornek, 18.5, koyu(renk, .35), "start", TK)
    s += f'<path d="{cizgi_d(yildiz_noktalari(cx, cy, 76, 62, 16, -math.pi / 2), True)}" fill="{ALTIN}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(cx, cy, 60), True)}" fill="{KOB}" stroke="{OBS}" stroke-width="2.6"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="39" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.6"/>'
    s += _yazi(cx, cy + 8, "KİMYA", 22, KOB_K, "middle", B)
    return s.cikti(f"0 0 {W} {H}", cls="info")


def _ihtiyac_ikonu(ad, x, y, renk):
    k = f'stroke="{OBS}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"'
    if ad == "bugday":
        return (f'<path d="M{x} {y + 16} V{y - 14}" {k}/>' + "".join(
            f'<ellipse cx="{f(x + sx * 5)}" cy="{f(y - 10 + j * 8)}" rx="4" ry="7" fill="{KEH}" {k} transform="rotate({sx * 30} {f(x + sx * 5)} {f(y - 10 + j * 8)})"/>'
            for j in range(3) for sx in (-1, 1)))
    if ad == "ev":
        return f'<path d="M{x - 15} {y + 14} V{y - 2} L{x} {y - 15} L{x + 15} {y - 2} V{y + 14} Z" fill="{acik(renk, .5)}" {k}/><rect x="{x - 4}" y="{y + 3}" width="8" height="11" fill="#FFFFFF" {k}/>'
    if ad == "ipek":
        return f'<ellipse cx="{x - 3}" cy="{y + 2}" rx="10" ry="15" fill="#FFF6DA" {k} transform="rotate(-25 {x - 3} {y + 2})"/><path d="M{x + 4} {y - 8} C{x + 14} {y - 18} {x + 18} {y - 2} {x + 12} {y + 8}" fill="none" stroke="{renk}" stroke-width="3"/>'
    if ad == "ilac":
        return f'<rect x="{x - 16}" y="{y - 7}" width="32" height="14" rx="7" fill="#FFFFFF" {k}/><path d="M{x} {y - 7} V{y + 7}" {k}/><rect x="{x}" y="{y - 7}" width="16" height="14" rx="7" fill="{acik(renk, .4)}" {k}/>'
    if ad == "sabun":
        return f'<rect x="{x - 15}" y="{y - 4}" width="30" height="16" rx="6" fill="{acik(renk, .5)}" {k}/><circle cx="{x - 6}" cy="{y - 10}" r="4" fill="#FFFFFF" {k}/><circle cx="{x + 6}" cy="{y - 14}" r="5" fill="#FFFFFF" {k}/>'
    if ad == "pil":
        return f'<rect x="{x - 9}" y="{y - 13}" width="18" height="28" rx="3" fill="{acik(renk, .5)}" {k}/><rect x="{x - 4}" y="{y - 17}" width="8" height="4" fill="{OBS}"/><path d="M{x + 2} {y - 8} L{x - 4} {y + 2} H{x + 3} L{x - 2} {y + 11}" fill="none" stroke="{KEH}" stroke-width="2.6"/>'
    return ""


def cini_renkleri(onek="ui-cin"):
    """Çininin renkleri: ham metal oksit tozu → fırında sırla pişince renk (dönüşüm)."""
    s = Svg(onek)
    W, H = 560, 196
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    sutun = [("kobalt oksit", "#2E2E3A", KOB, "lacivert"), ("bakır oksit", "#3A3A36", "#1FB3B0", "turkuaz"),
             ("hematit", "#8C3A26", MER, "kırmızı"), ("kuvars", "#F2EEE4", "#FBFDFD", "beyaz")]
    for i, (ham, ham_r, pis_r, ad) in enumerate(sutun):
        x = 62 + i * 120
        s += f'<path d="M{x - 34} 52 Q{x} 84 {x + 34} 52 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.4"/>'
        s += f'<path d="M{x - 26} 52 Q{x - 10} 30 {x} 34 Q{x + 14} 30 {x + 26} 52 Z" fill="{ham_r}" stroke="{OBS}" stroke-width="2"/>'
        s += _yazi(x, 22, ham, 18, OBS, font=TK)
        s += _ok(x, 82, x, 108, ALTIN_K, 3.6, 11)
        s += f'<rect x="{x - 30}" y="112" width="60" height="44" rx="5" fill="{pis_r}" stroke="{OBS}" stroke-width="2.4"/>'
        if pis_r != "#FBFDFD":
            s += f'<path d="M{x - 12} 134 q12 -16 24 0 q-12 16 -24 0 Z" fill="#FFFFFF" opacity=".75"/>'
        else:
            s += f'<path d="M{x - 12} 134 q12 -16 24 0 q-12 16 -24 0 Z" fill="{KOB}" opacity=".25"/>'
        s += _yazi(x, 182, ad, 21, koyu(pis_r, .45) if pis_r != "#FBFDFD" else GUM_K, font=TK)
    s += _yazi(503, 70, "fırında", 20, ALTIN_K, "middle", TK) + _yazi(503, 94, "≈ 900 °C", 19, GUM_K, "middle", TK)
    s += (f'<path d="M503 172 C478 160 482 138 494 126 C494 140 500 142 503 134 C506 122 500 112 506 104 C522 120 530 140 520 158 C516 166 510 170 503 172 Z" fill="#F08A2A" stroke="{OBS}" stroke-width="2.2"/>'
          f'<path d="M503 168 C494 162 494 150 502 142 C504 152 510 150 512 146 C516 156 512 164 503 168 Z" fill="#FFD25A"/>')
    return s.cikti(f"0 0 {W} {H}", cls="info")


def gul_suyu(onek="ui-gul"):
    """el-Kindî: gül ve damıtma (imbik) ikonu, Medeniyetimizden kutusu için."""
    s = Svg(onek)
    s += '<rect width="120" height="120" rx="14" fill="#FFF6E8"/>'
    s += (f'<path d="M30 92 V60 Q30 40 50 40 Q70 40 70 60 V92 Z" fill="#CFE8F0" stroke="{OBS}" stroke-width="2.4"/>'
          f'<path d="M50 40 V26 Q50 18 60 18 H96 L100 30" fill="none" stroke="{OBS}" stroke-width="3"/>'
          f'<path d="M92 34 q-6 12 0 20 q6 -8 0 -20 Z" fill="{GOL}"/>'
          f'<path d="M84 74 H108 L104 98 H88 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.2"/><path d="M87 88 H105" stroke="{GOL}" stroke-width="5"/>'
          f'<rect x="22" y="92" width="56" height="10" rx="3" fill="#B85C3E" stroke="{OBS}" stroke-width="2"/>')
    for k in range(5):
        a = k * 2 * math.pi / 5
        s += f'<ellipse cx="{f(50 + 9 * math.cos(a))}" cy="{f(64 + 9 * math.sin(a))}" rx="8" ry="6" fill="#E85A8A" stroke="{OBS}" stroke-width="1.4" transform="rotate({f(math.degrees(a))} {f(50 + 9 * math.cos(a))} {f(64 + 9 * math.sin(a))})"/>'
    s += f'<circle cx="50" cy="64" r="5" fill="#B8205A"/>'
    return s.cikti("0 0 120 120", cls="info")


# ------------------------------------------------------------------ 2. DURAK · ÇEKİRGE

# (pH, ad, ikon, kat, etiket x’i) — kat 1: çubuğun üstü, 2: altı. Değerler yaklaşıktır (dogrula.py aralıkları denetler).
PH_NESNELER = [(1.5, "mide asidi", "mide", 1, 210), (2.2, "limon suyu", "limon", 2, 300), (3.0, "sirke", "sirke", 1, 430),
               (3.3, "gazlı içecek", "kutu", 2, 520), (4.4, "domates", "domates", 1, 625), (6.6, "süt", "sut", 2, 860),
               (7.0, "saf su", "damla", 1, 950), (7.6, "Çekirge suyu", "kaplica", 2, 1070), (8.3, "karbonat", "paket", 1, 1120),
               (10.0, "sabun", "sabun", 2, 1330), (10.5, "antiasit", "tablet", 1, 1400), (12.5, "çamaşır suyu", "bidon", 2, 1620),
               (13.5, "lavabo açıcı", "acici", 1, 1760)]


def ph_cetveli(onek="ui-phc"):
    """pH cetveli: 0–14 renk çubuğu, üstte ve altta ev ve yol nesneleri (yaklaşık değerler)."""
    s = Svg(onek)
    W, H = 1900, 446
    x0, x1 = 70, 1830
    X = lambda p: x0 + (x1 - x0) * p / 14   # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#FFFFFF"/>'
    g = s.lin([(p / 14, c) for p, c in PH_RENK], x0, 0, x1, 0, kull="userSpaceOnUse", ad="phg")
    yb0, yb1 = 186, 228
    s += f'<rect x="{x0}" y="{yb0}" width="{x1 - x0}" height="{yb1 - yb0}" rx="21" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    for p in range(15):
        s += f'<path d="M{f(X(p))} {yb0 + 6} V{yb1 - 6}" stroke="#FFFFFF" stroke-width="{4 if p == 7 else 2}" opacity=".85"/>'
        s += _yazi(X(p), 256, str(p), 27, OBS if p != 7 else ZUMRUT, font=B)
    for (ph, ad, ikon, kat, lx) in PH_NESNELER:
        px = X(ph)
        renk = koyu(_ph_renk(ph), .25)
        deger = f"≈ {str(ph).replace('.', ',')}".replace(",0", "") if ph not in (7.0,) else "7"
        if kat == 1:
            s += f'<path d="M{f(px)} {yb0} V168 L{f(lx)} 146" stroke="{renk}" stroke-width="3" fill="none"/>'
            s += f'<circle cx="{f(px)}" cy="{yb0 - 4}" r="6" fill="{renk}" stroke="#FFFFFF" stroke-width="2"/>'
            s += _nesne(ikon, lx, 44, .9)
            s += _yazi(lx, 108, ad, 28, OBS, font=TK) + _yazi(lx, 136, deger, 24, renk, font=TK)
        else:
            s += f'<path d="M{f(px)} {yb1} V262 M{f(px)} 262 L{f(lx)} 268" stroke="{renk}" stroke-width="3" fill="none"/>'
            s += f'<circle cx="{f(px)}" cy="{yb1 + 4}" r="6" fill="{renk}" stroke="#FFFFFF" stroke-width="2"/>'
            s += _nesne(ikon, lx, 298, .9)
            s += _yazi(lx, 358, ad, 28, OBS, font=TK) + _yazi(lx, 384, deger, 24, renk, font=TK)
    s += _ok(860, 430, 120, 430, MER_K, 4, 16) + _yazi(160, 422, "ASİDİK · asitlik artar", 24, MER_K, "start", TK)
    s += _ok(1040, 430, 1780, 430, ERGUVAN, 4, 16) + _yazi(1740, 422, "bazlık artar · BAZİK", 24, ERGUVAN, "end", TK)
    s += f'<rect x="896" y="414" width="108" height="30" rx="15" fill="{acik(ZUMRUT, .85)}" stroke="{ZUMRUT}" stroke-width="2.4"/>' + _yazi(950, 437, "NÖTR", 23, ZUMRUT, font=TK)
    return s.cikti(f"0 0 {W} {H}", cls="info")


def seyreltme(onek="ui-sey", tur="iki"):
    """Su eklenince pH: asit 3’ten, baz 11’den 7’ye yaklaşır (7’yi geçmez)."""
    s = Svg(onek)
    W, H = 470, 300
    x0, y0, x1, y1 = 64, 250, 440, 30
    Y = lambda p: y0 - (y0 - y1) * p / 14   # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += _eksen(x0, y0, x1, y1, [], [(Y(p), str(p)) for p in (0, 7, 14)], "eklenen su", "pH", fs=22)
    s += f'<path d="M{x0} {f(Y(7))} H{x1}" stroke="{ZUMRUT}" stroke-width="3" stroke-dasharray="10 7"/>'
    s += _yazi(x1 - 4, Y(7) - 10, "7: nötr", 21, ZUMRUT, "end", TK)
    def egri(p0):
        pts = []
        for i in range(41):
            t = i / 40
            x = x0 + 8 + (x1 - x0 - 16) * t
            pts.append((x, Y(7 + (p0 - 7) * math.exp(-3.2 * t))))
        return egri_d(pts)
    s += f'<path d="{egri(3)}" stroke="{MER}" stroke-width="6" fill="none"/>'
    s += f'<path d="{egri(11)}" stroke="{ERGUVAN}" stroke-width="6" fill="none"/>'
    s += _yazi(x0 + 16, Y(3) + 30, "asit + su: pH artar", 21, MER_K, "start", TK)
    s += _yazi(x0 + 16, Y(11) - 14, "baz + su: pH azalır", 21, ERGUVAN, "start", TK)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def imtihan_seyreltme(onek="ui-isy"):
    """İmtihan: bir çözeltiye su eklendikçe pH (12’den 7’ye yaklaşır)."""
    s = Svg(onek)
    W, H = 430, 270
    x0, y0, x1, y1 = 58, 224, 404, 28
    Y = lambda p: y0 - (y0 - y1) * p / 14   # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += _eksen(x0, y0, x1, y1, [], [(Y(p), str(p)) for p in (0, 7, 12, 14)], "eklenen su", "pH", fs=21)
    s += f'<path d="M{x0} {f(Y(7))} H{x1}" stroke="{GUM}" stroke-width="2.6" stroke-dasharray="9 7"/>'
    pts = [(x0 + 6 + (x1 - x0 - 12) * i / 40, Y(7 + 5 * math.exp(-3.4 * i / 40))) for i in range(41)]
    s += f'<path d="{egri_d(pts)}" stroke="{KOB}" stroke-width="6" fill="none"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


def mide_ph(onek="ui-mid"):
    """Kıssa 1: antiasit tabletten sonra mide ortamının pH’ı (temsilî değerler)."""
    s = Svg(onek)
    W, H = 470, 300
    x0, y0, x1, y1 = 60, 248, 440, 48
    X = lambda t: x0 + (x1 - x0) * t / 60   # noqa: E731
    Y = lambda p: y0 - (y0 - y1) * p / 8    # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += _eksen(x0, y0, x1, y1, [(X(t), str(t)) for t in (0, 15, 30, 45, 60)], [(Y(p), str(p)) for p in (0, 2, 4, 6, 8)], "zaman (dk)", "pH", fs=21)
    s += f'<path d="M{x0} {f(Y(7))} H{x1}" stroke="{ZUMRUT}" stroke-width="3" stroke-dasharray="10 7"/>' + _yazi(x1 - 4, Y(7) - 10, "7: nötr", 20, ZUMRUT, "end", TK)
    veri = MIDE_VERI
    s += f'<path d="{egri_d([(X(t), Y(p)) for t, p in veri], gerginlik=.8)}" stroke="{MER}" stroke-width="6" fill="none"/>'
    for t, p in veri[::2]:
        s += f'<circle cx="{f(X(t))}" cy="{f(Y(p))}" r="6" fill="#FFFFFF" stroke="{MER_K}" stroke-width="3"/>'
    s += _ok(X(0) + 34, Y(5.8), X(0) + 6, Y(2.2), KOB, 3, 11) + _yazi(X(0) + 30, Y(6) - 4, "tablet", 20, KOB_K, "start", TK)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


MIDE_VERI = [(0, 1.8), (5, 2.6), (15, 3.6), (30, 3.2), (45, 2.7), (60, 2.4)]   # (dk, pH) temsilî


def lahana_skala(onek="ui-lah"):
    """Üstad: mor lahana suyunun renk–pH tablosu (temsilî)."""
    s = Svg(onek)
    W, H = 700, 128
    s += f'<rect width="{W}" height="{H}" rx="14" fill="#FFFFFF"/>'
    x0, x1 = 20, 680
    X = lambda p: x0 + (x1 - x0) * (p - .5) / 14   # noqa: E731
    for (a, b, c, ad) in LAHANA:
        s += f'<rect x="{f(X(a))}" y="22" width="{f(X(b + 1) - X(a))}" height="40" fill="{c}" stroke="{OBS}" stroke-width="2"/>'
        s += _yazi((X(a) + X(b + 1)) / 2, 88, ad, 21, OBS, font=TK)
        s += _yazi((X(a) + X(b + 1)) / 2, 114, f"{a}–{b}" if a != b else f"{a}", 20, GUM_K, font=TK)
    s += _yazi(x0, 16, "pH", 18, GUM_K, "start", TK)
    return s.cikti(f"0 0 {W} {H}", cls="info")


LAHANA = [(1, 3, "#E0204A", "kırmızı"), (4, 6, "#E77BB4", "pembe"), (7, 7, "#7B3F8C", "mor"), (8, 10, "#2B6CB5", "mavi"),
          (11, 12, "#2E9E58", "yeşil"), (13, 14, "#F2CF2A", "sarı")]


# ------------------------------------------------------------------ 4. DURAK · ULUDAĞ

def mangal_deney(onek="ui-mng"):
    """Mutfak deneyi düzeneği: iki mangal, iki sıcaklık; değiştir · ölç · sabit tut."""
    s = Svg(onek)
    W, H = 540, 300
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for i, (sic, renk) in enumerate(((180, KEH), (220, MER))):
        x = 120 + i * 230
        s += f'<path d="M{x - 70} 150 H{x + 70} L{x + 60} 180 H{x - 60} Z" fill="#3A3F4B" stroke="{OBS}" stroke-width="2.4"/>'
        s += f'<path d="M{x - 52} 180 L{x - 60} 214 M{x + 52} 180 L{x + 60} 214" stroke="{OBS}" stroke-width="5"/>'
        g = s.rad([(0, "#FFE08A"), (.6, renk), (1, "#B8202E")], .5, .3, .7, ad="kr")
        s += f'<rect x="{x - 62}" y="146" width="124" height="10" rx="4" fill="{g}"/>'
        s += f'<path d="M{x - 46} 146 Q{x - 48} 112 {x} 108 Q{x + 48} 112 {x + 46} 146 Z" fill="#DDE3EA" stroke="#5A6470" stroke-width="2.4"/>'
        s += f'<path d="M{x - 24} 132 l10 -10 l8 8 M{x + 6} 120 l10 8" stroke="#FFFFFF" stroke-width="3" fill="none"/>'
        s += _yazi(x, 136, str(i + 1), 22, OBS, font=B)
        s += f'<rect x="{x + 54}" y="60" width="12" height="70" rx="6" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.4"/><circle cx="{x + 60}" cy="134" r="10" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>'
        s += f'<rect x="{x + 57}" y="{78 if i else 96}" width="6" height="{52 if i else 34}" fill="{renk}"/>'
        s += _yazi(x + 60, 50, f"{sic} °C", 22, koyu(renk, .3), font=TK)
    s += _ok(232, 120, 300, 120, KOB, 3.4, 12)
    etiket = [("DEĞİŞTİR", "sıcaklık", KOB), ("ÖLÇ", "geçen Al", KEH_K), ("SABİT TUT", "yiyecek, kütle, pH, süre", GOL_K)]
    x = 10
    for (bas, ic, renk) in etiket:
        w = 124 if bas != "SABİT TUT" else 258
        s += f'<rect x="{x}" y="236" width="{w}" height="50" rx="12" fill="{acik(renk, .86)}" stroke="{renk}" stroke-width="2.6"/>'
        s += _yazi(x + w / 2, 256, bas, 17, renk, font=TK, ek=' letter-spacing="1"') + _yazi(x + w / 2, 278, ic, 18, OBS, font=T)
        x += w + 10
    return s.cikti(f"0 0 {W} {H}", cls="info")


AL_VERI = [(1, 4, 180, 20, 2.2), (2, 4, 220, 20, 3.6), (3, 6, 220, 20, 1.4), (4, 6, 180, 40, 1.1)]   # (deneme, pH, °C, dk, mg/kg) kurgusal


def al_grafik(onek="ui-alg"):
    """Görev 4: denemelerde yiyeceğe geçen alüminyum (kurgusal veriler)."""
    s = Svg(onek)
    W, H = 420, 290
    x0, y0, x1, y1 = 58, 236, 400, 30
    Y = lambda v: y0 - (y0 - y1) * v / 4   # noqa: E731
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    xt = [(x0 + 50 + i * 82, str(d)) for i, (d, *_r) in enumerate(AL_VERI)]
    s += _eksen(x0, y0, x1, y1, xt, [(Y(v), str(v)) for v in (0, 1, 2, 3, 4)], "deneme", "Al (mg/kg)", fs=20)
    for (px, _), (d, ph, t, dk, al) in zip(xt, AL_VERI):
        renk = MER if ph == 4 else GOL
        s += f'<rect x="{px - 26}" y="{f(Y(al))}" width="52" height="{f(y0 - Y(al))}" rx="5" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>'
        s += _yazi(px, Y(al) - 8, str(al).replace(".", ","), 20, OBS, font=TK)
    s += f'<rect x="250" y="30" width="20" height="16" rx="3" fill="{MER}"/>' + _yazi(276, 44, "pH 4", 18, OBS, "start", TK)
    s += f'<rect x="330" y="30" width="20" height="16" rx="3" fill="{GOL}"/>' + _yazi(356, 44, "pH 6", 18, OBS, "start", TK)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik")


# ------------------------------------------------------------------ 5. DURAK · KOZA HAN

def disiplin_ikon(onek="ui-dis", ad="analitik"):
    """Altı alt disiplinin ikonları (renkli, 100×100)."""
    s = Svg(onek)
    renk = {"analitik": KOB, "organik": ZUMRUT, "anorganik": KEH, "biyokimya": MER, "fizikokimya": ERGUVAN, "polimer": GOL}[ad]
    k = f'stroke="{OBS}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
    s += f'<circle cx="50" cy="50" r="46" fill="{acik(renk, .82)}" stroke="{renk}" stroke-width="4"/>'
    if ad == "analitik":
        s += f'<path d="M30 26 V66 Q30 76 40 76 Q50 76 50 66 V26" fill="#FFFFFF" {k}/><path d="M30 50 V66 Q30 76 40 76 Q50 76 50 66 V50 Z" fill="{acik(renk, .3)}" {k}/>'
        s += f'<circle cx="62" cy="40" r="15" fill="#FFFFFF" {k}/><path d="M73 51 L84 62" stroke="{OBS}" stroke-width="6" stroke-linecap="round"/>'
        s += f'<path d="M55 44 V36 M62 44 V32 M69 44 V38" stroke="{renk}" stroke-width="4"/>'
    elif ad == "organik":
        pts = [(50 + 26 * math.cos(math.radians(30 + 60 * i)), 50 + 26 * math.sin(math.radians(30 + 60 * i))) for i in range(6)]
        s += f'<path d="{cizgi_d(pts, True)}" fill="#FFFFFF" {k}/>'
        s += f'<path d="{cizgi_d([(50 + 18 * math.cos(math.radians(30 + 60 * i)), 50 + 18 * math.sin(math.radians(30 + 60 * i))) for i in (0, 1)])}" {k} fill="none"/>'
        s += _yazi(50, 61, "C", 30, koyu(renk, .3), font=B)
    elif ad == "anorganik":
        s += f'<path d="M50 18 L76 36 L68 76 H32 L24 36 Z" fill="{acik(renk, .35)}" {k}/><path d="M24 36 H76 M50 18 L42 36 L50 76 L58 36 Z" fill="none" {k}/>'
    elif ad == "biyokimya":
        for i in range(7):
            y = 22 + i * 9.5
            dx = 16 * math.sin(i * .9)
            s += f'<path d="M{f(50 - dx)} {f(y)} H{f(50 + dx)}" stroke="{renk}" stroke-width="4"/>'
        s += f'<path d="{egri_d([(50 + 16 * math.sin(i * .9), 22 + i * 9.5) for i in range(7)])}" fill="none" {k}/>'
        s += f'<path d="{egri_d([(50 - 16 * math.sin(i * .9), 22 + i * 9.5) for i in range(7)])}" fill="none" {k}/>'
    elif ad == "fizikokimya":
        s += f'<rect x="30" y="20" width="14" height="48" rx="7" fill="#FFFFFF" {k}/><circle cx="37" cy="72" r="10" fill="{MER}" {k}/><rect x="34" y="40" width="6" height="30" fill="{MER}"/>'
        s += f'<circle cx="66" cy="54" r="18" fill="#FFFFFF" {k}/><path d="M66 54 V42 M66 54 L75 59" {k}/><path d="M62 32 H70 M66 32 V36" {k}/>'
    else:
        for i in range(5):
            x = 22 + i * 14
            y = 50 + (8 if i % 2 else -8)
            if i:
                s += f'<path d="M{x - 14} {50 - (8 if i % 2 else -8)} L{x} {y}" {k}/>'
        for i in range(5):
            x = 22 + i * 14
            y = 50 + (8 if i % 2 else -8)
            s += f'<circle cx="{x}" cy="{y}" r="7.5" fill="{[renk, KEH, MER, KOB, renk][i]}" {k}/>'
    return s.cikti("0 0 100 100", cls="info ikon-dis")


def monomer_polimer(onek="ui-mon"):
    """Monomerden polimere: tek tek birimler → zincir."""
    s = Svg(onek)
    W, H = 560, 120
    s += f'<rect width="{W}" height="{H}" rx="14" fill="#FFFFFF"/>'
    r = RNG(7)
    renkler = [GOL, KEH, MER, KOB, ERGUVAN]
    for i in range(4):
        x, y = 34 + (i % 2) * 44, 34 + (i // 2) * 40
        s += f'<circle cx="{x}" cy="{y}" r="14" fill="{renkler[i % 5]}" stroke="{OBS}" stroke-width="2.4"/>'
    s += _yazi(56, 112, "monomer", 19, OBS, font=TK)
    s += _ok(118, 52, 178, 52, ALTIN_K, 4, 14)
    pts = [(200 + i * 38, 52 + (14 if i % 2 else -14)) for i in range(9)]
    s += f'<path d="{cizgi_d(pts)}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    for i, (x, y) in enumerate(pts):
        s += f'<circle cx="{x}" cy="{y}" r="14" fill="{renkler[i % 5]}" stroke="{OBS}" stroke-width="2.4"/>'
    s += _yazi(352, 112, "polimer (ipek, naylon…)", 19, OBS, font=TK)
    return s.cikti(f"0 0 {W} {H}", cls="info")


KARIYER = [("Sağlık", "eczacı", "biyokimyacı", MER), ("Endüstri", "kimya mühendisi", "kimyager", KOB),
           ("Gıda", "gıda mühendisi", "kalite kontrol", KEH), ("Malzeme", "malzeme mühendisi", "nanoteknoloji", ERGUVAN),
           ("Tarım", "ziraat mühendisi", "toprak analizi", ZUMRUT), ("Çevre ve enerji", "çevre mühendisi", "pil araştırması", GOL)]


def kariyer_haritasi(onek="ui-kar"):
    """Kimya alanında meslekler: KİMYA yıldızından çıkan yol üzerinde altı sektör durağı (yatay, sayfa genişliği)."""
    s = Svg(onek)
    W, H = 1700, 176
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    s += f'<path d="M120 88 H1690" stroke="{OBS}" stroke-width="16" stroke-linecap="round" opacity=".85"/>'
    s += f'<path d="M120 88 H1690" stroke="#FFF1CF" stroke-width="10" stroke-linecap="round"/>'
    s += f'<path d="M120 88 H1690" stroke="#E08A1A" stroke-width="3" stroke-dasharray="12 9"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(70, 88, 66, 53, 16, -math.pi / 2), True)}" fill="{ALTIN}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<circle cx="70" cy="88" r="46" fill="{KOB}" stroke="{OBS}" stroke-width="3"/>' + _yazi(70, 97, "KİMYA", 23, "#FFFFFF", font=B)
    for i, (ad, is1, is2, renk) in enumerate(KARIYER):
        x = 152 + i * 258
        s += f'<rect x="{x}" y="14" width="246" height="148" rx="16" fill="{acik(renk, .87)}" stroke="{renk}" stroke-width="3.4"/>'
        s += _yazi(x + 123, 54, ad, 31, OBS, font=B)
        s += _yazi(x + 123, 102, is1, 23, koyu(renk, .35), font=TK) + _yazi(x + 123, 140, is2, 23, koyu(renk, .35), font=TK)
    return s.cikti(f"0 0 {W} {H}", cls="info")


# ------------------------------------------------------------------ YAN YOLLAR

def lab_duzenek(onek="ui-lab"):
    """Anahtar merdiveni 2: sıcak ve soğuk sirkede kireç; terazi ve kronometre."""
    s = Svg(onek)
    W, H = 420, 270
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFFFFF"/>'
    for i, (sic, renk) in enumerate(((20, KOB), (50, MER))):
        x = 80 + i * 130
        s += f'<path d="M{x - 44} 70 V196 Q{x - 44} 210 {x - 30} 210 H{x + 30} Q{x + 44} 210 {x + 44} 196 V70" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
        s += f'<path d="M{x - 44} 120 V196 Q{x - 44} 210 {x - 30} 210 H{x + 30} Q{x + 44} 210 {x + 44} 196 V120 Z" fill="#F4E8C8" stroke="{OBS}" stroke-width="2.4"/>'
        for k in range(3):
            s += f'<ellipse cx="{x - 18 + k * 18}" cy="{198 - (k % 2) * 6}" rx="9" ry="6" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
        for k in range(4):
            s += f'<circle cx="{x - 20 + k * 13}" cy="{160 - k * 9}" r="3.4" fill="none" stroke="{GUM_K}" stroke-width="1.6"/>'
        s += f'<rect x="{x + 14}" y="40" width="10" height="120" rx="5" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.2"/><circle cx="{x + 19}" cy="164" r="8" fill="{renk}" stroke="{OBS}" stroke-width="2"/>'
        s += f'<rect x="{x + 16}" y="{120 if i == 0 else 92}" width="6" height="{44 if i == 0 else 72}" fill="{renk}"/>'
        s += _yazi(x - 4, 240, f"{sic} °C", 22, koyu(renk, .2), font=TK)
    s += f'<rect x="300" y="168" width="104" height="42" rx="8" fill="#E8EEF2" stroke="{OBS}" stroke-width="2.6"/><rect x="314" y="182" width="56" height="18" rx="3" fill="#2E3A44"/>'
    s += _yazi(342, 197, "2,0 g", 15, "#7CF2D2", font=TK) + f'<rect x="318" y="158" width="68" height="10" rx="3" fill="#C9D2DC" stroke="{OBS}" stroke-width="2"/>'
    s += f'<circle cx="352" cy="96" r="34" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/><path d="M352 96 V72 M352 96 L368 104" stroke="{OBS}" stroke-width="3" stroke-linecap="round"/><path d="M346 56 H358 M352 56 V62" stroke="{OBS}" stroke-width="3"/>'
    s += _yazi(352, 152, "kronometre", 18, GUM_K, font=TK) + _yazi(352, 238, "terazi", 18, GUM_K, font=TK)
    return s.cikti(f"0 0 {W} {H}", cls="info")
