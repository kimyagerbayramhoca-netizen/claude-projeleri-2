"""Bilgi grafikleri (infografik): Avogadro sayı merdiveni, bor izotop madalyonları, izotop çekirdekleri,
"göl üstünde köprüler" mol haritası, karışım kapları, eşit kütle terazisi, kıssa resimleri,
akçe rayı, unvan rozetleri, imbik (damıtma), özgül ağırlık resmi.

Bütün sayılar dogrula.py ile denetlenir; burada yalnızca çizim vardır.
"""
import math
from .temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, selcuklu_yildizi, yildiz_noktalari, halolu_yazi, rng as RNG
from .renkler import (OBS, GOL, GOL_K, GOL_A, GOL_AA, DERIN, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A,
                      ALTIN, ALTIN_K, ALTIN_A, LAJVER, ZUMRUT, GUM, GUM_K, GUM_A, PEMBE, ERGUVAN, ATOM)
from . import molekul as M
from . import sahne as S
from . import yapilar as Y

T = 'font-family="Nunito" font-weight="800"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'


def _sup(taban, us, x, y, fs, renk=OBS, anchor="middle", font=B):
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(fs)}" fill="{renk}">{taban}'
            f'<tspan dy="{f(-fs * .38)}" font-size="{f(fs * .62)}">{us}</tspan></text>')


# ------------------------------------------------------------------ 1. DURAK · Avogadro sayı merdiveni (log ölçek)

def avogadro_merdiveni(onek="inf-avo"):
    """10⁰ … 10²⁴ logaritmik cetvel; üstte ve altta resimli işaretler. ~125 mm genişlikte basılır."""
    s = Svg(onek)
    W, H = 1300, 640
    g = s.lin([(0, "#EAF7F6"), (1, "#FFF5E2")], 0, 0, 1, 0, ad="zm")
    s += f'<rect x="0" y="0" width="{W}" height="{H}" rx="30" fill="{g}"/>'
    x0, x1, y = 54, 1246, 322
    def X(us):
        return x0 + (x1 - x0) * us / 24
    gs = s.lin([(0, "#7FD3CF"), (.5, GOL), (1, DERIN)], 0, 0, 1, 0, ad="cv")
    s += f'<rect x="{x0 - 18}" y="{y - 16}" width="{x1 - x0 + 36}" height="32" rx="16" fill="{gs}" stroke="{OBS}" stroke-width="4"/>'
    for us in range(0, 25):
        b = us % 3 == 0
        s += f'<path d="M{f(X(us))} {y + 16} v{14 if b else 8}" stroke="{OBS}" stroke-width="{3 if b else 2}"/>'
        if b and us not in (18, 21, 24):
            s += _sup("10", us, X(us), y + 70, 32, GUM_K)
    isaret = [
        (math.log10(12), "12", "1 düzine yumurta", "yumurta", "ust", "start"),
        (math.log10(500), "500", "1 top kâğıt", "kagit", "alt", "middle"),
        (math.log10(8e9), "≈ 8·10⁹", "dünyadaki insan", "insan", "ust", "middle"),
        (math.log10(1.2e19), "≈ 1,2·10¹⁹", "Van Gölü’ndeki damla", "gol", "alt", "end"),
        (math.log10(1.67e21), "≈ 1,7·10²¹", "1 damladaki su molekülü", "damla", "ust", "end"),
        (math.log10(6.02e23), "6,02·10²³", "1 mol", "mol", "alt", "end"),
    ]
    for us, e1, e2, tur, yon, anc in isaret:
        x = X(us)
        renk = MER if tur == "mol" else (KOB if tur in ("gol", "damla") else KEH_K)
        tx = x + (20 if anc == "end" else 0)
        if tur == "mol":
            tx = W - 24
        if anc == "start":
            tx = 22
        if yon == "ust":
            s += f'<path d="M{f(x)} {y - 16} V{y - 60}" stroke="{renk}" stroke-width="3" stroke-dasharray="6 5"/>'
            s += f'<text x="{f(tx)}" y="{y - 72}" text-anchor="{anc}" {B} font-size="44" fill="{renk}">{e1}</text>'
            s += f'<text x="{f(tx)}" y="{y - 120}" text-anchor="{anc}" {T} font-size="31" fill="{OBS}">{e2}</text>'
            s += _kucuk_resim(s, tur, x - (60 if anc == "end" else 0) + (40 if anc == "start" else 0), y - 226)
        else:
            s += f'<path d="M{f(x)} {y + 16} V{y + 104}" stroke="{renk}" stroke-width="3" stroke-dasharray="6 5"/>'
            s += f'<text x="{f(tx)}" y="{y + 140}" text-anchor="{anc}" {B} font-size="44" fill="{renk}">{e1}</text>'
            s += f'<text x="{f(tx)}" y="{y + 178}" text-anchor="{anc}" {T} font-size="31" fill="{OBS}">{e2}</text>'
            s += _kucuk_resim(s, tur, x - (70 if anc == "end" and tur != "mol" else (40 if tur == "mol" else 0)), y + 262)
        s += f'<circle cx="{f(x)}" cy="{y}" r="12" fill="#FFFFFF" stroke="{renk}" stroke-width="5"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info avo")


def _kucuk_resim(s, tur, x, y):
    o = []
    if tur == "yumurta":
        for k in range(6):
            cx = x - 50 + (k % 3) * 50
            cy = y - 12 + (k // 3) * 36
            o.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="17" ry="21" fill="#FFF3DD" stroke="{OBS}" stroke-width="3"/>')
        o.append(f'<path d="M{f(x - 78)} {f(y + 20)} h156 l-10 30 h-136 Z" fill="#D9B48C" stroke="{OBS}" stroke-width="3"/>')
    elif tur == "kagit":
        for k in range(5):
            o.append(f'<rect x="{f(x - 56 + k * 3)}" y="{f(y - 30 + k * 10)}" width="112" height="22" rx="3" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>')
        o.append(f'<rect x="{f(x - 56)}" y="{f(y - 2)}" width="118" height="14" fill="{MER}" stroke="{OBS}" stroke-width="3"/>')
    elif tur == "insan":
        for k, c in enumerate([MER, GOL, KEH, KOB, ZUMRUT]):
            cx = x - 64 + k * 32
            o.append(f'<circle cx="{f(cx)}" cy="{f(y - 18)}" r="12" fill="#F6D2B5" stroke="{OBS}" stroke-width="2.6"/>'
                     f'<path d="M{f(cx - 16)} {f(y + 30)} q0 -34 16 -34 q16 0 16 34 Z" fill="{c}" stroke="{OBS}" stroke-width="2.6"/>')
    elif tur == "gol":
        o.append(f'<path d="M{f(x - 90)} {f(y + 10)} C{f(x - 60)} {f(y - 40)} {f(x + 40)} {f(y - 46)} {f(x + 90)} {f(y)} C{f(x + 70)} {f(y + 40)} {f(x - 40)} {f(y + 44)} {f(x - 90)} {f(y + 10)} Z" fill="{GOL}" stroke="{OBS}" stroke-width="3"/>'
                 f'<path d="M{f(x - 50)} {f(y)} q20 -10 40 0 t40 0" stroke="#FFFFFF" stroke-width="4" fill="none"/>'
                 f'<path d="M{f(x + 20)} {f(y - 34)} l26 -40 l26 40 Z" fill="#8199BB" stroke="{OBS}" stroke-width="3"/><path d="M{f(x + 36)} {f(y - 58)} l10 -16 l10 16 l-6 -3 l-4 5 l-4 -5 Z" fill="#FFFFFF"/>')
    elif tur == "damla":
        o.append(f'<path d="M{f(x)} {f(y - 56)} C{f(x + 14)} {f(y - 30)} {f(x + 42)} {f(y - 4)} {f(x + 42)} {f(y + 18)} A42 42 0 0 1 {f(x - 42)} {f(y + 18)} C{f(x - 42)} {f(y - 4)} {f(x - 14)} {f(y - 30)} {f(x)} {f(y - 56)} Z" fill="#9FDDE8" stroke="{OBS}" stroke-width="3"/>')
        for k, (dx, dy) in enumerate(((-16, 10), (12, 2), (2, 30), (-6, -14), (20, 26))):
            o.append(f'<circle cx="{f(x + dx)}" cy="{f(y + dy)}" r="6.5" fill="{MER}" stroke="{OBS}" stroke-width="1.6"/>'
                     f'<circle cx="{f(x + dx - 6)}" cy="{f(y + dy + 4)}" r="3.6" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.2"/>'
                     f'<circle cx="{f(x + dx + 6)}" cy="{f(y + dy + 4)}" r="3.6" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.2"/>')
    elif tur == "mol":
        y8 = selcuklu_yildizi(x, y, 64)
        g = s.rad([(0, "#FFE6A8"), (1, KEH)], .4, .35, .8, ad="ms")
        o.append(f'<path d="{cizgi_d(y8, True)}" fill="{g}" stroke="{OBS}" stroke-width="4" stroke-linejoin="round"/>'
                 f'<text x="{f(x)}" y="{f(y + 14)}" text-anchor="middle" {B} font-size="42" fill="{OBS}">mol</text>')
    return "".join(o)


# ------------------------------------------------------------------ 2. DURAK · izotop çekirdekleri + bor madalyonları

def cekirdekler(onek="inf-cek"):
    s = Svg(onek)
    W, H = 900, 300
    for k, (n, ad) in enumerate(((6, "¹²C"), (7, "¹³C"), (8, "¹⁴C"))):
        cx = 150 + k * 300
        s += f'<circle cx="{cx}" cy="120" r="104" fill="none" stroke="{GUM}" stroke-width="3" stroke-dasharray="8 7"/>'
        s += M.cekirdek_ciz(s, cx, 120, 86, 6, n, tohum=k + 3)
        s += f'<text x="{cx}" y="268" text-anchor="middle" {B} font-size="46" fill="{OBS}">{ad}</text>'
        s += f'<text x="{cx}" y="308" text-anchor="middle" {T} font-size="34" fill="{GUM_K}">6p · {n}n</text>'
    return s.cikti(f"0 -10 {W} {H + 30}", cls="info cek")


def bor_madalyon(onek="inf-bor"):
    """Bor izotop bolluğu: iki çini madalyon (pasta dilimli) + ağırlıklı ortalama terazisi."""
    s = Svg(onek)
    W, H = 1000, 420
    def madalyon(cx, cy, R, oran, renk, ust, alt):
        o = []
        y16 = yildiz_noktalari(cx, cy, R + 18, R + 6, 16, -math.pi / 2)
        ga = s.lin([(0, "#F6DE95"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="ma")
        o.append(f'<path d="{cizgi_d(y16, True)}" fill="{ga}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>')
        a1 = -math.pi / 2 + 2 * math.pi * oran
        buyuk = 1 if oran > .5 else 0
        o.append(f'<path d="M{cx} {cy} L{cx} {cy - R + 8} A{R - 8} {R - 8} 0 {buyuk} 1 {f(cx + (R - 8) * math.cos(a1))} {f(cy + (R - 8) * math.sin(a1))} Z" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{R * .42}" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.4"/>')
        o.append(f'<text x="{cx}" y="{cy + 13}" text-anchor="middle" {B} font-size="38" fill="{OBS}">%{int(oran * 100)}</text>')
        o.append(f'<text x="{cx}" y="{cy + R + 62}" text-anchor="middle" {B} font-size="40" fill="{renk}">{ust}</text>')
        o.append(f'<text x="{cx}" y="{cy + R + 100}" text-anchor="middle" {T} font-size="34" fill="{GUM_K}">{alt}</text>')
        return "".join(o)
    s += madalyon(150, 150, 104, .2, MER, "¹⁰B", "kütle 10")
    s += madalyon(470, 150, 104, .8, KOB, "¹¹B", "kütle 11")
    # ortalama çizelgesi
    x0, x1, y = 650, 970, 190
    s += f'<rect x="{x0}" y="{y - 14}" width="{x1 - x0}" height="28" rx="14" fill="{GUM_A}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<rect x="{x0}" y="{y - 14}" width="{(x1 - x0) * .2}" height="28" rx="14" fill="{MER}"/><rect x="{x0 + (x1 - x0) * .2}" y="{y - 14}" width="{(x1 - x0) * .8}" height="28" fill="{KOB}"/>'
    s += f'<rect x="{x0}" y="{y - 14}" width="{x1 - x0}" height="28" rx="14" fill="none" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M{x0} {y + 56} H{x1}" stroke="{OBS}" stroke-width="3"/><path d="M{x0} {y + 46} v20 M{x1} {y + 46} v20" stroke="{OBS}" stroke-width="3"/>'
    s += f'<text x="{x0}" y="{y + 98}" text-anchor="middle" {T} font-size="34">10</text><text x="{x1}" y="{y + 98}" text-anchor="middle" {T} font-size="34">11</text>'
    xo = x0 + (x1 - x0) * .8
    s += f'<path d="M{f(xo)} {y + 22} v34" stroke="{KEH_K}" stroke-width="4"/><path d="M{f(xo - 14)} {y + 30} h28 l-14 18 Z" fill="{KEH}" stroke="{OBS}" stroke-width="2"/>'
    s += f'<text x="{f(xo)}" y="{y - 40}" text-anchor="middle" {B} font-size="54" fill="{KEH_K}">10,8</text>'
    s += f'<text x="{(x0 + x1) / 2}" y="{y + 146}" text-anchor="middle" {T} font-size="32" fill="{GUM_K}">ağır izotopa yakın</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info bor")


# ------------------------------------------------------------------ 3–4. DURAK · göl üstünde köprüler: mol haritası

def mol_haritasi(onek="inf-har", kutle_acik=True):
    """Adalar: TANECİK (kefaller), MOL (fener), KÜTLE (terazi), ATOM MOLÜ (çakıllar). Köprü üstünde işlem."""
    s = Svg(onek)
    W, H = 1100, 500
    g = s.lin([(0, "#BFE7E3"), (1, "#5FC2C0")], 0, 0, 0, 1, ad="su")
    s += f'<rect x="0" y="0" width="{W}" height="{H}" rx="30" fill="{g}"/>'
    s += S.dalga_cizgileri(20, 20, W - 40, H - 40, 7, n=46, op=.55, k=2.4)
    def ada(cx, cy, rx, ry, renk, ad, alt, kilit=False):
        o = [f'<ellipse cx="{cx}" cy="{cy + 14}" rx="{rx + 8}" ry="{ry + 6}" fill="#0E4C5A" opacity=".25"/>',
             f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 8}" ry="{ry + 6}" fill="#F3E0B8" stroke="{OBS}" stroke-width="3"/>',
             f'<ellipse cx="{cx}" cy="{cy - 4}" rx="{rx}" ry="{ry}" fill="{renk if not kilit else "#D5DDE2"}" stroke="{OBS}" stroke-width="3"/>']
        o.append(f'<text x="{cx}" y="{cy + ry * .1}" text-anchor="middle" {B} font-size="{44 if ad == "MOL" else 34}" fill="{OBS if not kilit else GUM_K}">{ad}</text>')
        o.append(f'<text x="{cx}" y="{cy + ry * .1 + 36}" text-anchor="middle" {T} font-size="29" fill="{OBS if not kilit else GUM_K}">{alt}</text>')
        return "".join(o)
    def kopru(x0, y0, x1, y1, metin, renk=KEH, kilit=False, etiket=-1, alt_s=""):
        L = math.hypot(x1 - x0, y1 - y0)
        a = math.degrees(math.atan2(y1 - y0, x1 - x0))
        o = [f'<g transform="translate({x0} {y0}) rotate({f(a, 2)})">',
             f'<rect x="0" y="-15" width="{f(L)}" height="30" rx="6" fill="{"#C9A27A" if not kilit else "#D5DDE2"}" stroke="{OBS}" stroke-width="3"{" stroke-dasharray=\"10 8\"" if kilit else ""}/>']
        for k in range(1, int(L / 24)):
            o.append(f'<path d="M{k * 24} -15 v30" stroke="{OBS}" stroke-width="1.6" opacity=".45"/>')
        o.append(f'<path d="M{f(L - 30)} -8 l18 8 l-18 8 Z" fill="{OBS}"/>')
        o.append("</g>")
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if abs(y1 - y0) > abs(x1 - x0):
            lx, ly = mx + 92, my + 8
        else:
            lx, ly = mx, my + etiket * 46
        w = len(metin) * 17 + 58
        yaz = renk != KEH and not kilit
        o.append(f'<rect x="{f(lx - w / 2)}" y="{f(ly - 22)}" width="{f(w)}" height="44" rx="22" fill="{renk if not kilit else "#FFFFFF"}" stroke="{OBS}" stroke-width="3"/>'
                 f'<text x="{f(lx)}" y="{f(ly + 11)}" text-anchor="middle" {B} font-size="32" fill="{"#FFFFFF" if yaz else OBS}">{metin}'
                 + (f'<tspan dy="7" font-size="18">{alt_s}</tspan>' if alt_s else "") + '</text>')
        return "".join(o)
    # köprüler (önce), sonra adalar
    s += kopru(296, 230, 456, 230, "÷ N", KEH, etiket=-1, alt_s="A")
    s += kopru(456, 296, 296, 296, "× N", KEH, etiket=1, alt_s="A")
    s += kopru(804, 230, 644, 230, "÷ M", MER, kilit=not kutle_acik, etiket=-1, alt_s="A")
    s += kopru(644, 296, 804, 296, "× M", MER, kilit=not kutle_acik, etiket=1, alt_s="A")
    s += kopru(550, 336, 550, 400, "× (a + b)", KOB)
    s += ada(190, 262, 108, 78, "#FFF1C4", "TANECİK", "sayı · N")
    s += ada(550, 262, 98, 82, GOL, "MOL", "n")
    s += ada(910, 262, 108, 78, "#FDE2DC", "KÜTLE", "m (g)", kilit=not kutle_acik)
    s += ada(550, 438, 150, 46, "#E2E9FB", "ATOM MOLÜ", "XaYb için")
    # simgeler: kefaller (tanecik), fener (mol), terazi (kütle)
    s += S.kefal(s, 140, 196, 46, -8) + S.kefal(s, 236, 188, 40, 6)
    s += Y.fener(s, 612, 210, 70, isik=False)
    if kutle_acik:
        s += Y.basit_terazi(s, 990, 214, 62)
    else:
        s += f'<g transform="translate(960 168)" stroke="{GUM_K}" stroke-width="5" fill="none"><rect x="0" y="22" width="44" height="34" rx="6"/><path d="M8 22 V12 a14 14 0 0 1 28 0 V22"/></g>'
        s += f'<text x="910" y="372" text-anchor="middle" {T} font-size="24" fill="{GUM_K}">Ahlat’ta açılır</text>'
    s += f'<text x="34" y="50" {T} font-size="29" fill="{DERIN}">N<tspan dy="7" font-size="20">A</tspan><tspan dy="-7"> = 6,02·10²³ · Ne verilirse önce mole git.</tspan></text>'
    return s.cikti(f"0 0 {W} {H}", cls="mol-haritasi")


# ------------------------------------------------------------------ 5. DURAK · karışım kapları ve eşit kütle terazisi

def karisim_kaplari(onek="inf-kar"):
    """İki gaz kabı (CH₄ ve C₂H₆) + birleşmiş karışım kabı; x ve 0,5 − x etiketleri."""
    s = Svg(onek)
    W, H = 1000, 420
    def kap(cx, cy, w, h, renk, icerik):
        g = s.lin([(0, acik(renk, .7)), (1, acik(renk, .35))], 0, 0, 0, 1, ad="kp")
        return (f'<path d="M{cx - w / 2} {cy - h / 2 + 30} Q{cx - w / 2} {cy - h / 2} {cx} {cy - h / 2} Q{cx + w / 2} {cy - h / 2} {cx + w / 2} {cy - h / 2 + 30} '
                f'V{cy + h / 2 - 20} Q{cx + w / 2} {cy + h / 2} {cx + w / 2 - 20} {cy + h / 2} H{cx - w / 2 + 20} Q{cx - w / 2} {cy + h / 2} {cx - w / 2} {cy + h / 2 - 20} Z" '
                f'fill="{g}" stroke="{OBS}" stroke-width="4"/>{icerik}'
                f'<path d="M{cx - w / 2 + 16} {cy - h / 2 + 34} V{cy + h / 2 - 30}" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity=".7"/>')
    ch4 = M.molekul_ciz(s, *M._geometri("CH4"), (10, 20, 5), 34, yer_golgesi=False)[0]
    c2h6 = M.molekul_ciz(s, *M._geometri("C2H6"), (10, 25, 0), 30, yer_golgesi=False)[0]
    ic1 = "".join(f'<g transform="translate({x} {y})">{ch4}</g>' for x, y in ((150, 150), (110, 250), (195, 260)))
    ic2 = "".join(f'<g transform="translate({x} {y})">{c2h6}</g>' for x, y in ((420, 160), (420, 270)))
    s += kap(150, 210, 210, 300, GOL, ic1)
    s += kap(420, 210, 210, 300, KEH, ic2)
    s += f'<text x="150" y="400" text-anchor="middle" {B} font-size="36">CH<tspan dy="8" font-size="24">4</tspan><tspan dy="-8"> · x mol</tspan></text>'
    s += f'<text x="420" y="400" text-anchor="middle" {B} font-size="36">C<tspan dy="8" font-size="24">2</tspan><tspan dy="-8">H</tspan><tspan dy="8" font-size="24">6</tspan><tspan dy="-8"> · 0,5 − x</tspan></text>'
    s += f'<path d="M545 210 h90" stroke="{OBS}" stroke-width="5" marker-end="url(#{onek}-ok)"/>'
    s.tanim(f'<marker id="{onek}-ok" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{OBS}"/></marker>')
    ic3 = "".join(f'<g transform="translate({x} {y})">{ch4}</g>' for x, y in ((760, 140), (880, 280), (790, 300))) + \
          "".join(f'<g transform="translate({x} {y})">{c2h6}</g>' for x, y in ((880, 150), (800, 220)))
    s += kap(825, 210, 260, 320, KOB, ic3)
    s += f'<text x="825" y="408" text-anchor="middle" {B} font-size="34">0,5 mol · 2,4 mol H</text>'
    return s.cikti(f"0 0 {W} {H + 10}", cls="info karisim")


def esit_kutle_terazi(onek="inf-esit"):
    """64 g O₂ (2 mol, 2 molekül simgesi) ile 64 g SO₂ (1 mol, 1 simge): terazi dengede."""
    s = Svg(onek)
    W, H = 1000, 470
    o2 = M.molekul_ciz(s, *M._geometri("O2"), (10, 20, 0), 34, yer_golgesi=False)[0]
    so2 = M.molekul_ciz(s, *M._geometri("SO2"), (0, 20, 0), 34, yer_golgesi=False)[0]
    sol = f'<g transform="translate(-40 -36)">{o2}</g><g transform="translate(44 -36)">{o2}</g>'
    sag = f'<g transform="translate(0 -44)">{so2}</g>'
    s += Y.basit_terazi(s, 500, 440, 400, sol_ic=sol, sag_ic=sag, egim=0)
    s += f'<text x="158" y="455" text-anchor="middle" {B} font-size="36" fill="{MER_K}">64 g O<tspan dy="8" font-size="24">2</tspan></text>'
    s += f'<text x="158" y="40" text-anchor="middle" {B} font-size="34" fill="{OBS}">2 mol</text>'
    s += f'<text x="842" y="455" text-anchor="middle" {B} font-size="36" fill="{KEH_K}">64 g SO<tspan dy="8" font-size="24">2</tspan></text>'
    s += f'<text x="842" y="40" text-anchor="middle" {B} font-size="34" fill="{OBS}">1 mol</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info esit")


# ------------------------------------------------------------------ Medeniyetimizden resimleri

def hazini_kart(onek="inf-haz"):
    s = Svg(onek)
    W, H = 640, 420
    g = s.rad([(0, "#FFF7E0"), (1, "#F2DFB0")], .5, .45, .7, ad="hz")
    s += f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="{g}"/>'
    for k in range(9):
        a = math.pi * k / 8
        s += f'<path d="M320 400 L{f(320 + 600 * math.cos(math.pi + a))} {f(400 + 600 * math.sin(math.pi + a))}" stroke="#E8CB8A" stroke-width="2" opacity=".6"/>'
    hh = 270
    s += Y.hazini_terazisi(s, 320, 396, hh)
    kx = hh * 1.05 * .92
    ky = 396 - hh * .9 + hh * .45
    s += f'<rect x="{f(320 - kx - 10)}" y="{f(ky - 22)}" width="20" height="22" fill="#8C6A3A" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="M{f(320 + kx - 22)} {f(ky - 2)} q8 -26 30 -18 q14 8 4 18 Z" fill="#7C86C8" stroke="{OBS}" stroke-width="2"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info hazini")


def imbik(onek="inf-imb"):
    """Câbir bin Hayyân: damıtma düzeneği (imbik) temsilî çizim."""
    s = Svg(onek)
    W, H = 520, 360
    g = s.lin([(0, "#E8F6F7", .9), (1, "#BFE3E8", .9)], 0, 0, 1, 1, ad="cm")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFF7E6"/>'
    # ocak + ateş
    s += f'<rect x="60" y="270" width="160" height="60" rx="8" fill="#B8553A" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M110 270 q10 -30 30 -36 q-4 20 12 28 q8 -18 20 -22 q-2 18 -12 30 Z" fill="{KEH}" stroke="{MER_K}" stroke-width="2"/>'
    # kabak (cucurbit) + başlık + oluk
    s += f'<path d="M80 270 C60 220 80 170 120 160 L160 160 C200 170 220 220 200 270 Z" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M86 250 C90 230 190 230 194 250 C196 262 84 262 86 250 Z" fill="{GOL}" opacity=".6"/>'
    s += f'<path d="M116 160 C100 110 150 80 180 100 C200 112 196 138 170 156 Z" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M188 110 L360 190 L360 202 L180 128 Z" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    # toplama kabı + damlalar
    s += f'<path d="M340 300 C320 260 340 220 380 214 L410 214 C450 220 470 260 450 300 Z" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M346 290 C350 276 440 276 444 290 C446 300 344 300 346 290 Z" fill="#7FD3CF"/>'
    for k in range(3):
        s += f'<path d="M{368 + k * 4} {222 + k * 20} q6 10 0 14 q-6 -4 0 -14 Z" fill="#5FB3C2"/>'
    s += f'<rect x="320" y="300" width="150" height="20" rx="6" fill="#B8553A" stroke="{OBS}" stroke-width="3"/>'
    # buhar
    s += f'<path d="M150 150 q-10 -20 6 -34 M164 146 q-8 -18 6 -30" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info imbik")


def ozgul_agirlik(onek="inf-ozg"):
    """el-Bîrûnî: aynı hacimde farklı maddeler farklı ağırlıkta (su ile kıyas) — temsilî."""
    s = Svg(onek)
    W, H = 560, 360
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFF7E6"/>'
    renk = [("#9FDDE8", "su", "1"), ("#9AA4AE", "demir", "≈ 7,9"), ("#D9B44A", "altın", "≈ 19,3")]
    for k, (c, ad, oz) in enumerate(renk):
        x = 60 + k * 170
        g = s.lin([(0, acik(c, .4)), (1, koyu(c, .15))], 0, 0, 1, 1, ad="ok")
        s += f'<path d="M{x} 200 l40 -24 h80 l-40 24 Z" fill="{acik(c, .5)}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<path d="M{x + 80} 200 l40 -24 v80 l-40 24 Z" fill="{koyu(c, .15)}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<rect x="{x}" y="200" width="80" height="80" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<text x="{x + 52}" y="322" text-anchor="middle" {B} font-size="30">{ad}</text>'
        s += f'<text x="{x + 52}" y="150" text-anchor="middle" {B} font-size="30" fill="{ALTIN_K}">{oz}</text>'
    s += f'<text x="{W / 2}" y="52" text-anchor="middle" {T} font-size="25" fill="{OBS}">aynı hacim, farklı ağırlık</text>'
    s += f'<text x="{W / 2}" y="86" text-anchor="middle" {T} font-size="22" fill="{GUM_K}">(suya göre kaç kat ağır?)</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ozgul")


# ------------------------------------------------------------------ kıssa resimleri

def soda_resmi(onek="inf-soda"):
    s = Svg(onek)
    W, H = 420, 300
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#E6F6F6"/>'
    s += f'<path d="M0 190 C120 170 300 176 420 186 V300 H0 Z" fill="{GOL}"/>'
    s += f'<path d="M30 220 h80 M160 214 h120 M300 232 h80" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
    # buharlaşan kap + kristaller
    s += f'<path d="M110 150 h200 l-20 70 h-160 Z" fill="#D7DEE3" stroke="{OBS}" stroke-width="4"/>'
    r = RNG(5)
    for k in range(9):
        x = 140 + k * 17
        h = r.uniform(18, 34)
        s += f'<path d="M{x} 150 l8 {-h} l8 {h} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/>'
    for k in range(3):
        s += f'<path d="M{170 + k * 40} 110 q-12 -20 0 -40 q12 -20 0 -40" stroke="#9AAAB4" stroke-width="4" fill="none" stroke-linecap="round"/>'
    s += f'<circle cx="360" cy="60" r="34" fill="#FFE08A" stroke="{KEH}" stroke-width="4"/>'
    s += f'<text x="210" y="280" text-anchor="middle" {B} font-size="34" fill="#FFFFFF">pH ≈ 9,5–10</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info kissa-resim")


def bor_resmi(onek="inf-borr"):
    s = Svg(onek)
    W, H = 400, 300
    s += f'<rect width="{W}" height="{H}" rx="20" fill="#FFF3E2"/>'
    # kristal (çok yüzlü)
    pts = [(200, 40), (300, 100), (290, 210), (200, 260), (110, 210), (100, 100)]
    renk = ["#C9C2D9", "#A79FC2", "#8A82A8", "#B5ADCC", "#D9D3E6", "#E6E1F0"]
    for k in range(6):
        a, b = pts[k], pts[(k + 1) % 6]
        s += f'<path d="M200 150 L{nok(a)} L{nok(b)} Z" fill="{renk[k]}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<path d="M150 90 L190 70" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>'
    s += f'<rect x="258" y="196" width="104" height="80" rx="10" fill="#FFFFFF" stroke="{OBS}" stroke-width="4"/>'
    s += f'<text x="312" y="256" text-anchor="middle" {B} font-size="54">B</text><text x="276" y="224" {B} font-size="22" fill="{GUM_K}">5</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info kissa-resim")


def grafik_xy(onek="inf-graf"):
    """Kütle (g) – mol grafiği: X için (12 g; 0,5 mol), Y için (16 g; 0,5 mol) noktalı doğrular."""
    s = Svg(onek)
    W, H = 520, 400
    x0, y0, x1, y1 = 100, 330, 490, 50
    s += f'<rect width="{W}" height="{H + 40}" rx="18" fill="#FFFFFF"/>'
    for k in range(0, 5):
        yy = y0 - (y0 - y1) * k / 4
        s += f'<path d="M{x0} {f(yy)} H{x1}" stroke="#DCE4E8" stroke-width="2"/>'
        s += f'<text x="{x0 - 12}" y="{f(yy + 10)}" text-anchor="end" {T} font-size="30">{["0", "0,25", "0,5", "0,75", "1"][k]}</text>'
    for k in range(0, 5):
        xx = x0 + (x1 - x0) * k / 4
        s += f'<path d="M{f(xx)} {y0} V{y1}" stroke="#DCE4E8" stroke-width="2"/>'
        s += f'<text x="{f(xx)}" y="{y0 + 36}" text-anchor="middle" {T} font-size="30">{k * 8}</text>'
    s += f'<path d="M{x0} {y1 - 10} V{y0} H{x1 + 10}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    s += f'<text x="{x1}" y="{y0 + 72}" text-anchor="end" {T} font-size="28" fill="{GUM_K}">kütle (g)</text>'
    s += f'<text x="{x0 - 4}" y="{y1 - 16}" {T} font-size="28" fill="{GUM_K}">mol</text>'
    def X(g):
        return x0 + (x1 - x0) * g / 32
    def Yy(n):
        return y0 - (y0 - y1) * n / 1.0
    s += f'<path d="M{x0} {y0} L{f(X(24))} {f(Yy(1))}" stroke="{MER}" stroke-width="6"/>'
    s += f'<path d="M{x0} {y0} L{f(X(32))} {f(Yy(1))}" stroke="{KOB}" stroke-width="6"/>'
    for g, c, ad in ((12, MER, "X"), (16, KOB, "Y")):
        s += f'<path d="M{f(X(g))} {y0} V{f(Yy(.5))} H{x0}" stroke="{c}" stroke-width="2.6" stroke-dasharray="7 6" fill="none"/>'
        s += f'<circle cx="{f(X(g))}" cy="{f(Yy(.5))}" r="10" fill="#FFFFFF" stroke="{c}" stroke-width="5"/>'
    s += f'<text x="{f(X(24) - 20)}" y="{f(Yy(1) - 12)}" {B} font-size="34" fill="{MER}">X</text>'
    s += f'<text x="{f(X(32) - 30)}" y="{f(Yy(1) - 12)}" {B} font-size="34" fill="{KOB}">Y</text>'
    return s.cikti(f"0 0 {W} {H + 40}", cls="info grafik")


def raf_kaplari(onek="inf-raf"):
    """Laboratuvar rafında üç etiketli kap (kıssa 4 tablosu ile birlikte)."""
    s = Svg(onek)
    W, H = 760, 300
    s += f'<rect x="20" y="236" width="720" height="22" rx="6" fill="#9A6B42" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M60 258 v34 M700 258 v34" stroke="{OBS}" stroke-width="6"/>'
    kaplar = [("I", "#FFFFFF", KEH), ("II", "#BFE7EF", GOL), ("III", "#FFF3D6", KOB)]
    for k, (ad, sivi, et) in enumerate(kaplar):
        x = 140 + k * 240
        g = s.lin([(0, "#FFFFFF", .9), (1, "#D6E8EC", .8)], 0, 0, 1, 0, ad="rk")
        s += f'<path d="M{x - 60} 236 V110 Q{x - 60} 90 {x - 40} 86 V60 H{x + 40} V86 Q{x + 60} 90 {x + 60} 110 V236 Z" fill="{g}" stroke="{OBS}" stroke-width="4"/>'
        s += f'<path d="M{x - 56} 236 V160 H{x + 56} V236 Z" fill="{sivi}" opacity=".9"/>'
        s += f'<rect x="{x - 48}" y="40" width="96" height="24" rx="6" fill="{koyu(et, .1)}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<rect x="{x - 46}" y="128" width="92" height="50" rx="8" fill="#FFFFFF" stroke="{et}" stroke-width="4"/>'
        s += f'<text x="{x}" y="168" text-anchor="middle" {B} font-size="44" fill="{OBS}">{ad}</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info raf")


# ------------------------------------------------------------------ final: akçe rayı + unvan rozetleri

def akce_rayi(onek="inf-ray", ust_unvan="MOL ÜSTADI"):
    """Final sayfası akçe rayı (0–1400; Kalfa 400, Usta 800, Üstad 1150). ust_unvan: en üst basamağın adı
    (ör. {{info|akce_rayi|ÜSTAD}}; Mol ünitesinde varsayılan "MOL ÜSTADI")."""
    s = Svg(onek)
    W, H = 1880, 260
    x0, x1, y = 60, 1820, 150
    def X(a):
        return x0 + (x1 - x0) * a / 1400
    g = s.lin([(0, GUM), (.2857, GOL_A), (.5714, GOL), (.8214, KEH), (1, KEH)], x0, 0, x1, 0, kull="userSpaceOnUse", ad="ry")
    s += f'<path d="M{x0} {y + 30} H{x1}" stroke="#9A6B42" stroke-width="12"/>'
    for k in range(0, 1401, 50):
        s += f'<rect x="{f(X(k) - 6)}" y="{y + 18}" width="12" height="30" rx="3" fill="#7A4E2E"/>'
    s += f'<rect x="{x0}" y="{y - 20}" width="{x1 - x0}" height="40" rx="20" fill="{g}" stroke="{OBS}" stroke-width="4"/>'
    for a in range(0, 1401, 100):
        s += f'<path d="M{f(X(a))} {y - 20} v{12 if a % 200 else 18}" stroke="{OBS}" stroke-width="3"/>'
    esik = [(0, "ÇIRAK", GUM_K), (400, "KALFA", GOL_K), (800, "USTA", DERIN), (1150, ust_unvan, KEH_K), (1400, "", OBS)]
    for a, ad, c in esik:
        x = X(a)
        s += f'<path d="M{f(x)} {y - 26} V{y - 74}" stroke="{c}" stroke-width="4"/>'
        y8 = selcuklu_yildizi(x, y - 92, 20)
        s += f'<path d="{cizgi_d(y8, True)}" fill="{KEH if a == 1150 else "#FFFFFF"}" stroke="{OBS}" stroke-width="3"/>'
        anc = "start" if a == 0 else ("end" if a == 1400 else "middle")
        s += f'<text x="{f(x)}" y="{y + 92}" text-anchor="{anc}" {B} font-size="34" fill="{c}">{a}</text>'
        if ad:
            s += f'<text x="{f(x + (6 if a == 0 else 0))}" y="{y - 124}" text-anchor="{"start" if a == 0 else "middle"}" {T} font-size="26" fill="{c}">{ad}</text>'
    # kervan/kefal: ilerleme işareti yeri
    s += f'<text x="{x1}" y="{y - 124}" text-anchor="end" {T} font-size="26" fill="{OBS}">TOPLAM</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info ray-svg")


def unvan_rozeti(onek, kat, renk):
    s = Svg(onek)
    ga = s.lin([(0, "#F6DE95"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="ua")
    s += f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 47), True)}" fill="{ga}" stroke="{OBS}" stroke-width="2.6" stroke-linejoin="round"/>'
    s += f'<circle cx="50" cy="50" r="31" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>'
    yer = {1: [(50, 50, 13)], 2: [(39, 50, 10), (61, 50, 10)], 3: [(50, 39, 9), (37, 58, 9), (63, 58, 9)],
           4: [(50, 34, 8.5), (35, 50, 8.5), (65, 50, 8.5), (50, 66, 8.5)]}[kat]
    for cx, cy, r in yer:
        y5 = yildiz_noktalari(cx, cy, r, r * .42, 5, -math.pi / 2)
        s += f'<path d="{cizgi_d(y5, True)}" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6" stroke-linejoin="round"/>'
    return s.cikti("0 0 100 100")


def razi_araclari(onek="inf-raz"):
    """Ebû Bekir er-Râzî: laboratuvar araçları (temsilî): havan-havan eli, balon, beher, imbik başlığı, kepçe, raf."""
    s = Svg(onek)
    W, H = 560, 360
    s += f'<rect width="{W}" height="{H}" rx="18" fill="#FFF7E6"/>'
    cam = s.lin([(0, "#FFFFFF", .95), (.5, "#E3F2F4", .7), (1, "#BCD9DF", .85)], 0, 0, 1, 0, ad="cm")
    tunc = s.lin([(0, "#E9C98A"), (.5, "#C9A06A"), (1, "#8C6A3A")], 0, 0, 1, 0, ad="tn")
    # raf
    s += f'<rect x="30" y="280" width="500" height="18" rx="5" fill="#9A6B42" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M60 298 v40 M500 298 v40" stroke="{OBS}" stroke-width="6"/>'
    # havan + havan eli
    s += f'<path d="M60 230 h110 l-12 50 h-86 Z" fill="{tunc}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<ellipse cx="115" cy="230" rx="55" ry="10" fill="#6E4A2C" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M100 226 L150 150" stroke="{OBS}" stroke-width="18" stroke-linecap="round"/><path d="M100 226 L150 150" stroke="#C9A06A" stroke-width="12" stroke-linecap="round"/>'
    # balon (uzun boyunlu)
    s += f'<path d="M232 120 h24 v58 C300 192 306 268 244 278 C182 268 188 192 232 178 Z" fill="{cam}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M206 236 C214 266 274 266 282 236 C268 244 220 244 206 236 Z" fill="{GOL}" opacity=".75"/>'
    s += f'<path d="M222 200 Q212 224 220 250" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round"/>'
    # beher
    s += f'<path d="M318 180 h80 l-4 98 h-72 Z" fill="{cam}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M322 230 h72 l-2 46 h-68 Z" fill="{KEH}" opacity=".7"/>'
    for k in range(3):
        s += f'<path d="M376 {200 + k * 20} h14" stroke="{OBS}" stroke-width="2"/>'
    # imbik başlığı (ambix) asılı
    s += f'<path d="M430 160 C430 130 470 116 492 130 C506 140 506 160 494 172 L430 172 Z" fill="{cam}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M494 150 L540 182" stroke="{OBS}" stroke-width="7" stroke-linecap="round"/><path d="M494 150 L540 182" stroke="#E3F2F4" stroke-width="3" stroke-linecap="round"/>'
    s += f'<path d="M424 172 h76 l-8 108 h-60 Z" fill="{cam}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M430 246 h64 l-3 32 h-58 Z" fill="#7FD3CF"/>'
    # yazı
    s += f'<text x="{W / 2}" y="60" text-anchor="middle" {T} font-size="27" fill="{OBS}">önce sınıflandır, sonra ölç</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info razi")


# ------------------------------------------------------------------ anahtar merdiveni: akçe basamakları

def merdiven_akce(onek="inf-mrd"):
    """İskele merdiveni suya iner: 0 basamak 40 akçe … 3 basamak 10 akçe. 'Ne kadar az inersen o kadar ustasın.'"""
    from .karakter import akce_sikke
    s = Svg(onek)
    W, H = 900, 330
    g = s.lin([(0, "#FFE6C8"), (1, "#FBD3DA")], 0, 0, 0, 1, ad="gk")
    s += f'<rect width="{W}" height="{H}" rx="22" fill="{g}"/>'
    su = s.lin([(0, "#7FD3CF"), (1, "#1D6F86")], 0, 230, 0, H, kull="userSpaceOnUse", ad="su")
    s += f'<path d="M0 250 C200 240 500 256 900 244 V{H - 22} Q900 {H} 878 {H} H22 Q0 {H} 0 {H - 22} Z" fill="{su}"/>'
    s += S.dalga_cizgileri(20, 262, 860, 50, 5, n=18, op=.7, k=2.4)
    ahsap = s.lin([(0, "#C99566"), (1, "#8C5E36")], 0, 0, 0, 1, ad="ah")
    for k in range(4):
        x = 60 + k * 205
        y = 70 + k * 52
        s += f'<rect x="{x}" y="{y}" width="215" height="{290 - y}" fill="{ahsap}" stroke="{OBS}" stroke-width="3"/>'
        s += f'<rect x="{x}" y="{y}" width="215" height="14" fill="#E2B88A" stroke="{OBS}" stroke-width="3"/>'
        for j in range(4 - k):
            s += akce_sikke(s, x + 40 + j * 46, y - 26, 20)
        s += halolu_yazi(f'x="{x + 107}" y="{y + 64}" text-anchor="middle" {B} font-size="48"', f"+{40 - 10 * k}", "#FFFFFF", OBS, 1.4)
        if y + 100 < 290:
            s += f'<text x="{x + 107}" y="{y + 100}" text-anchor="middle" {T} font-size="31" fill="#FFF6E6">{k} basamak</text>'
        else:
            s += f'<text x="{x + 107}" y="{y - 52}" text-anchor="middle" {T} font-size="31" fill="{OBS}">{k} basamak</text>'
    s += f'<text x="{W - 26}" y="46" text-anchor="end" {T} font-size="34" fill="{OBS}">Az in, çok kazan!</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info merdiven-akce")


def elmas(onek="inf-elm"):
    """Pırlanta kesim elmas (yalnız C atomlarından): faset yüzler, parıltılar."""
    s = Svg(onek)
    W, H = 200, 190
    tac = [(30, 70), (60, 40), (100, 32), (140, 40), (170, 70)]
    renk = ["#E9F6FF", "#C6E6FA", "#9FD3F2", "#DDF1FF", "#B5DDF5", "#F4FBFF", "#8CC6EA", "#CDEBFA"]
    s += f'<ellipse cx="100" cy="182" rx="60" ry="6" fill="#0E2A3A" opacity=".2"/>'
    for i in range(4):
        a, b = tac[i], tac[i + 1]
        s += f'<path d="M{nok(a)} L{nok(b)} L100 70 Z" fill="{renk[i]}" stroke="#2B5D7A" stroke-width="2" stroke-linejoin="round"/>'
    s += f'<path d="M30 70 L170 70" stroke="#2B5D7A" stroke-width="2"/>'
    alt = [(30, 70), (65, 70), (100, 70), (135, 70), (170, 70)]
    for i in range(4):
        a, b = alt[i], alt[i + 1]
        s += f'<path d="M{nok(a)} L{nok(b)} L100 172 Z" fill="{renk[i + 4]}" stroke="#2B5D7A" stroke-width="2" stroke-linejoin="round"/>'
    s += f'<path d="M30 70 L60 40 L100 32 L140 40 L170 70 L100 172 Z" fill="none" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
    for (x, y, r) in ((58, 28, 9), (150, 22, 7), (178, 100, 6)):
        s += f'<path d="M{x} {y - r} L{x + r * .3} {y - r * .3} L{x + r} {y} L{x + r * .3} {y + r * .3} L{x} {y + r} L{x - r * .3} {y + r * .3} L{x - r} {y} L{x - r * .3} {y - r * .3} Z" fill="{KEH}"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info elmas")


def balon(onek="inf-bal"):
    """Helyum balonu."""
    s = Svg(onek)
    g = s.rad([(0, "#FFB3A6"), (.5, MER), (1, MER_K)], .38, .32, .75, ad="bl")
    s += f'<path d="M60 150 C55 170 70 180 62 200" stroke="{OBS}" stroke-width="2.4" fill="none"/>'
    s += f'<ellipse cx="60" cy="72" rx="50" ry="64" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="M54 135 L66 135 L62 146 L58 146 Z" fill="{MER_K}" stroke="{OBS}" stroke-width="2"/>'
    s += f'<ellipse cx="40" cy="44" rx="12" ry="18" fill="#FFFFFF" opacity=".55" transform="rotate(-25 40 44)"/>'
    s += f'<text x="60" y="88" text-anchor="middle" {B} font-size="40" fill="#FFFFFF">He</text>'
    return s.cikti("0 0 120 205", cls="info balon")


def halka_aleti(onek="inf-hlk"):
    """Gözlem halkaları (armiller küre) · temsilî çizim. Teleskop DEĞİL (16. yy rasathanelerinde teleskop yoktu)."""
    s = Svg(onek)
    W, H = 300, 300
    g = s.rad([(0, "#2C4A85"), (1, "#0B1636")], .5, .4, .8, ad="gc")
    s += f'<rect width="{W}" height="{H}" rx="18" fill="{g}"/>'
    s += S.yildizlar(s, 10, 10, W - 20, 120, 26, 7)
    pir = s.lin([(0, "#F7E3A1"), (.5, ALTIN), (1, ALTIN_K)], 0, 0, 1, 1, ad="pr")
    cx, cy, R = 150, 140, 92
    s += f'<path d="M150 232 L120 282 H180 Z" fill="{pir}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<rect x="100" y="280" width="100" height="12" rx="4" fill="{pir}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R}" fill="none" stroke="{OBS}" stroke-width="12"/><ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R}" fill="none" stroke="{pir}" stroke-width="7"/>'
    for (rx, ry, a) in ((R, R * .32, -18), (R * .34, R, 22), (R, R * .5, 30)):
        s += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{OBS}" stroke-width="9" transform="rotate({a} {cx} {cy})"/>'
              f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{pir}" stroke-width="5" transform="rotate({a} {cx} {cy})"/>')
    s += f'<path d="M{cx - 20} {cy - R - 26} L{cx + 20} {cy + R + 26}" stroke="{OBS}" stroke-width="7" stroke-linecap="round"/><path d="M{cx - 20} {cy - R - 26} L{cx + 20} {cy + R + 26}" stroke="{ALTIN_A}" stroke-width="3" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="16" fill="#5FB3E0" stroke="{OBS}" stroke-width="3"/><path d="M{cx - 8} {cy - 6} q8 -6 16 0" stroke="#FFFFFF" stroke-width="3" fill="none"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info halka")
