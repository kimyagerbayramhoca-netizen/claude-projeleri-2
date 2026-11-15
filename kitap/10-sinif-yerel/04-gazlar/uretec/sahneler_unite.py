"""Gazlar · Kapadokya Yolu — üniteye özel sahneler, nişan ikonları ve açılış panoraması.

kur_ortak bu modüle {{sahne|ad}} için ORTAK kütüphaneden (yerel-ortak/cizim) ÖNCE bakar. Ortak dosyalar değiştirilmez;
buradaki her şey ortak parçalardan (sahne, yapilar, karakter sembolleri) ve aşağıdaki Kapadokya parçalarından kurulur:
  balon (sıcak hava balonu) · peri_bacasi · tuf_sirt (katmanlı tüf sırtları) · uchisar_kaya · testi · firin · guvercinlik_yuzu
Kompozisyon (TASARIM-SISTEMI §6): bant 2100×460 birim; sol üst ≈ %55 × %75 sakin gökyüzü (levha); odak sağ %40'ta;
ışık solda (isik=-1); tohumlar sabit; her Svg öneki benzersiz; konturlu SVG yazısı yok (gerekirse halolu_yazi).
"""
import math
from cizim.temel import (Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari,
                         deger_gurultusu, rng as RNG)
from cizim import sahne as S, yapilar as Y
from cizim.sahneler import W, H, _bitir, _cerceve_golge
from cizim.karakter import turk_bayragi

# ------------------------------------------------------------------ Kapadokya paleti
TUF = "#F2DFC4"      # krem tüf
TUF_P = "#EDC3B4"    # pembe tüf (Kızılçukur)
TUF_O = "#E4B07C"    # okr tüf
TUF_K = "#C99A78"    # tüf gölgesi
BAZALT = "#6B5650"   # peri bacası şapkası
KIL = "#B9532F"      # Avanos kili
KIL_K = "#7E3219"
NEHIR = "#B86A45"    # Kızılırmak

BALON_RENK = [("#E2533D", "#F0A21A"), ("#2B50B5", "#F6E7BF"), ("#13A3A6", "#FFFFFF"), ("#7B3F8C", "#FF8A3D"),
              ("#F0A21A", "#E2533D"), ("#1F8A5B", "#F2C94A"), ("#FF5C8A", "#FFF1DE"), ("#1D3A8A", "#13A3A6"),
              ("#C8442F", "#F6E7BF"), ("#13A3A6", "#F0A21A")]

# Üniteye özel nişan ikonları: 48×48 çizgi (dolgu yok; öğrenci boyar)
NISAN_IKON = {
    "barometre": '<circle cx="24" cy="24" r="17"/><path d="M12 30 A13 13 0 0 1 36 30"/><path d="M24 24 L32 15" stroke-width="3"/><circle cx="24" cy="24" r="2.6"/>'
                 '<path d="M14.5 21 l2.4 1.3 M19 15 l1.4 2.3 M24 13 v2.7 M29 15 l-1.4 2.3 M33.5 21 l-2.4 1.3"/><path d="M17 35 h14"/>',
    "balon": '<path d="M24 5 C35 5 41 13 41 21 C41 30 32 35 29 40 H19 C16 35 7 30 7 21 C7 13 13 5 24 5 Z"/><path d="M24 5 C19 13 18 30 21 40 M24 5 C29 13 30 30 27 40"/>'
             '<path d="M19 40 L20 44 M29 40 L28 44"/><rect x="19" y="44" width="10" height="3" rx="1"/>',
    "testi": '<path d="M19 6 H29 M20 6 V11 C13 14 10 21 11 28 C12 36 17 42 24 42 C31 42 36 36 37 28 C38 21 35 14 28 11 V6"/>'
             '<path d="M28 13 C36 13 38 19 35 25"/><path d="M14 26 H34 M15 31 H33"/><path d="M17 42 h14"/>',
    "tanecik": '<rect x="6" y="6" width="36" height="36" rx="4"/><circle cx="15" cy="16" r="3.4"/><circle cx="31" cy="20" r="3.4"/><circle cx="20" cy="33" r="3.4"/>'
               '<path d="M18 13 L24 9 M34 23 L39 27 M17 36 L11 39"/>',
    "baca": '<path d="M4 16 H18 M30 16 H44"/><path d="M18 4 V16 M30 4 V16"/><path d="M18 16 V30 M30 16 V30"/><path d="M8 44 V36 A6 6 0 0 1 20 36 V44 M28 44 V36 A6 6 0 0 1 40 36 V44"/>'
            '<path d="M24 7 V24 M20 20 L24 25 L28 20"/>',
}


# ================================================================== PARÇALAR

def _zemin(s, y, renk, h=H):
    """Ufkun altına düz zemin: katmanlar arasında gökyüzü boşluğu kalmasın."""
    return f'<rect x="0" y="{f(y)}" width="{W}" height="{f(h - y + 2)}" fill="{renk}"/>'


def _meridyen(x, y, r, u):
    """Balon zarfında u ∈ [−1, 1] meridyeninin noktaları (tepe → ağız)."""
    s_ = math.sin(u * math.pi / 2)
    return [(x, y - r), (x + r * .72 * s_, y - r * .7), (x + r * .97 * s_, y - r * .12), (x + r * .86 * s_, y + r * .45),
            (x + r * .56 * s_, y + r * .9), (x + r * .27 * u, y + r * 1.18)]


def balon(s, x, y, r, tohum=0, renk=None, alev=False, sepet=True, isik=-1, op=1.0, serit=None, cizgi=True):
    """Sıcak hava balonu. (x, y): zarfın en geniş yerinin ortası, r: yarıçap. Zarf tepesi y−r, ağzı y+1,18r, sepet y+1,52r."""
    rr = RNG(tohum)
    a, b = renk or BALON_RENK[tohum % len(BALON_RENK)]
    serit = (tohum % 3 == 0) if serit is None else serit
    lw = max(.6, r * .022)
    o = [f'<g opacity="{f(op, 2)}">' if op < 1 else "<g>"]
    if sepet:
        sy = y + r * 1.52
        sw = r * .34
        o.append(f'<path d="M{f(x - r * .26)} {f(y + r * 1.18)} L{f(x - sw / 2)} {f(sy)} M{f(x + r * .26)} {f(y + r * 1.18)} L{f(x + sw / 2)} {f(sy)} '
                 f'M{f(x - r * .09)} {f(y + r * 1.18)} L{f(x - sw * .2)} {f(sy)} M{f(x + r * .09)} {f(y + r * 1.18)} L{f(x + sw * .2)} {f(sy)}" '
                 f'stroke="#3A2E26" stroke-width="{f(lw * .9)}" fill="none"/>')
        if alev:
            ay = y + r * 1.18
            gl = s.rad([(0, "#FFF4C8", .95), (.4, "#FFB43A", .5), (1, "#FF7A3D", 0)], x, ay + r * .12, r * .5, kull="userSpaceOnUse", ad="ba")
            o.append(f'<circle cx="{f(x)}" cy="{f(ay + r * .12)}" r="{f(r * .5)}" fill="{gl}"/>')
            o.append(f'<path d="M{f(x - r * .09)} {f(sy - r * .02)} Q{f(x - r * .13)} {f(ay + r * .12)} {f(x)} {f(ay - r * .2)} Q{f(x + r * .13)} {f(ay + r * .12)} {f(x + r * .09)} {f(sy - r * .02)} Z" fill="#FF8A3D"/>'
                     f'<path d="M{f(x - r * .045)} {f(sy - r * .02)} Q{f(x - r * .06)} {f(ay + r * .2)} {f(x)} {f(ay - r * .02)} Q{f(x + r * .06)} {f(ay + r * .2)} {f(x + r * .045)} {f(sy - r * .02)} Z" fill="#FFE08A"/>')
        o.append(f'<rect x="{f(x - sw / 2)}" y="{f(sy)}" width="{f(sw)}" height="{f(r * .24)}" rx="{f(r * .03)}" fill="#A9773F" stroke="#5A3A22" stroke-width="{f(lw)}"/>')
        o.append(f'<path d="M{f(x - sw / 2)} {f(sy + r * .08)} h{f(sw)} M{f(x - sw / 2)} {f(sy + r * .16)} h{f(sw)}" stroke="#6E4A2C" stroke-width="{f(lw * .6)}" opacity=".75"/>')
        o.append(f'<rect x="{f(x - sw / 2 - r * .015)}" y="{f(sy - r * .015)}" width="{f(sw + r * .03)}" height="{f(r * .045)}" rx="{f(r * .02)}" fill="#7A4E2E"/>')
    # zarf: dilimler (meridyenler arası)
    n = 10
    us = [-1 + 2 * k / n for k in range(n + 1)]
    for k in range(n):
        m0, m1 = _meridyen(x, y, r, us[k]), _meridyen(x, y, r, us[k + 1])
        d = egri_d(m0) + " L" + nok(m1[-1]) + egri_d(list(reversed(m1)), bas_m=False) + " Z"
        o.append(f'<path d="{d}" fill="{a if k % 2 == 0 else b}"/>')
    dis = egri_d(_meridyen(x, y, r, 1)) + " L" + nok(_meridyen(x, y, r, -1)[-1]) + egri_d(list(reversed(_meridyen(x, y, r, -1))), bas_m=False) + " Z"
    kl = s.klip(f'<path d="{dis}"/>', ad="bz")
    if serit:
        c3 = rr.choice(["#1D3A8A", "#FFFFFF", "#F0A21A", "#1B1D26"])
        o.append(f'<g clip-path="{kl}"><rect x="{f(x - r * 1.1)}" y="{f(y - r * .2)}" width="{f(r * 2.2)}" height="{f(r * .2)}" fill="{c3}"/>'
                 f'<path d="' + " ".join(f"M{f(x - r * 1.1 + i * r * .22)} {f(y - r * .02)} l{f(r * .11)} {f(-r * .16)} l{f(r * .11)} {f(r * .16)}" for i in range(11)) +
                 f'" stroke="{a if c3 != a else b}" stroke-width="{f(lw * 1.4)}" fill="none"/></g>')
    # gölge ve parıltı
    gg = s.rad([(0, "#FFFFFF", .55), (.35, "#FFFFFF", .08), (.7, "#1B1D26", .05), (1, "#1B1D26", .32)],
               x + r * .38 * isik, y - r * .45, r * 1.55, kull="userSpaceOnUse", ad="bg")
    o.append(f'<path d="{dis}" fill="{gg}"/>')
    o.append(f'<path d="M{f(x - r * .27)} {f(y + r * 1.18)} h{f(r * .54)}" stroke="#3A2E26" stroke-width="{f(lw * 2.2)}" stroke-linecap="round"/>')
    if cizgi:
        o.append(f'<path d="{dis}" fill="none" stroke="{koyu(a, .45)}" stroke-width="{f(lw)}" opacity=".7"/>')
    o.append("</g>")
    return "".join(o)


def peri_bacasi(s, x, y, h, w, tohum, govde=TUF, sapka=BAZALT, isik=-1, pencere=0, sapkali=True, golge=None, kapi=False, isikli=False):
    """Peri bacası: tüf gövde (alt geniş, boyun dar), üstte bazalt şapka. (x, y) taban ortası; h boy, w taban genişliği.
    pencere: oyma pencere sayısı (kaya oyma evler); isikli=True → pencereler gece ışıklı."""
    r = RNG(tohum)
    golge = golge or koyu(govde, .2)
    j = lambda v: v * r.uniform(.9, 1.1)  # noqa: E731
    sol = [(x - w / 2, y), (x - j(w * .42), y - h * .2), (x - j(w * .3), y - h * .48), (x - j(w * .2), y - h * .72), (x - w * .14, y - h * .88)]
    sag = [(x + w * .14, y - h * .88), (x + j(w * .2), y - h * .7), (x + j(w * .31), y - h * .46), (x + j(w * .43), y - h * .18), (x + w / 2, y)]
    d = egri_d(sol) + " L" + nok(sag[0]) + egri_d(sag, bas_m=False) + " Z"
    a_, b_ = (acik(govde, .22), golge) if isik < 0 else (golge, acik(govde, .22))
    g = s.lin([(0, a_), (.5, govde), (1, b_)], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="pb")
    o = [f'<path d="{d}" fill="{g}"/>']
    # oluklar (erozyon)
    for k in range(3):
        t = r.uniform(.15, .45) * (-isik)
        x0 = x + w * t * .5
        o.append(f'<path d="M{f(x0)} {f(y - h * .84)} Q{f(x0 + w * t * .3)} {f(y - h * .45)} {f(x0 + w * t * .7)} {f(y - h * .05)}" stroke="{koyu(govde, .28)}" stroke-width="{f(max(.8, w * .025))}" fill="none" opacity=".45"/>')
    # oyma pencereler
    for k in range(pencere):
        py = y - h * r.uniform(.18, .62)
        gen = w * r.uniform(.07, .1)
        px = x + r.uniform(-.18, .18) * w * (1 - (y - py) / h)
        renk = "#FFD27A" if isikli else koyu(govde, .62)
        if k % 3 == 0:
            o.append(f'<path d="M{f(px - gen)} {f(py + gen * 1.6)} V{f(py)} A{f(gen)} {f(gen)} 0 0 1 {f(px + gen)} {f(py)} V{f(py + gen * 1.6)} Z" fill="{renk}"/>')
        else:
            o.append(f'<rect x="{f(px - gen * .8)}" y="{f(py)}" width="{f(gen * 1.6)}" height="{f(gen * 1.5)}" fill="{renk}"/>')
    if kapi:
        dw = w * .1
        o.append(f'<path d="M{f(x - dw)} {f(y)} V{f(y - h * .12)} A{f(dw)} {f(dw)} 0 0 1 {f(x + dw)} {f(y - h * .12)} V{f(y)} Z" fill="{"#FFC65A" if isikli else koyu(govde, .65)}"/>')
    if sapkali:
        cy = y - h * .9
        cw = w * r.uniform(.3, .38)
        ch = h * .11
        gs = s.lin([(0, acik(sapka, .25)), (1, koyu(sapka, .25))], x - cw, 0, x + cw, 0, kull="userSpaceOnUse", ad="ps")
        o.append(f'<path d="M{f(x - cw)} {f(cy + ch * .25)} Q{f(x - cw * .9)} {f(cy - ch * .55)} {f(x - cw * .1)} {f(cy - ch)} Q{f(x + cw * .7)} {f(cy - ch * .7)} {f(x + cw)} {f(cy + ch * .2)} '
                 f'Q{f(x)} {f(cy + ch * .55)} {f(x - cw)} {f(cy + ch * .25)} Z" fill="{gs}"/>')
        o.append(f'<path d="M{f(x - cw * .7)} {f(cy - ch * .2)} Q{f(x - cw * .4)} {f(cy - ch * .7)} {f(x)} {f(cy - ch * .85)}" stroke="#FFFFFF" stroke-width="{f(max(.6, w * .02))}" fill="none" opacity=".35"/>')
    else:
        o.append(f'<ellipse cx="{f(x)}" cy="{f(y - h * .88)}" rx="{f(w * .14)}" ry="{f(h * .03)}" fill="{acik(govde, .2)}"/>')
    return "".join(o)


def peri_kumesi(s, x0, x1, y, n, tohum, boy=(120, 220), en=(.42, .6), renkler=(TUF, "#F4E4CC", "#EBD2B4"), isik=-1, pencere=True, isikli=False):
    """Bir grup peri bacası (arkadan öne, küçükten büyüğe)."""
    r = RNG(tohum)
    out = []
    ogeler = []
    for k in range(n):
        xx = x0 + (x1 - x0) * (k + r.uniform(.1, .9)) / n
        h = r.uniform(*boy)
        ogeler.append((h, xx))
    for h, xx in sorted(ogeler):
        out.append(peri_bacasi(s, xx, y + r.uniform(-4, 6), h, h * r.uniform(*en), tohum * 37 + int(xx), govde=r.choice(renkler), isik=isik,
                               pencere=r.choice([0, 0, 1, 2, 3]) if pencere else 0, sapkali=r.random() < .8, isikli=isikli))
    return "".join(out)


def tuf_sirt(s, x0, x1, y, h, tohum, renkler=(TUF_P, TUF, TUF_O, "#FFF2E2"), dalga=7, katman=6, oluk=True, isik=-1):
    """Katmanlı tüf sırtı: yuvarlak tepeler, yatay renk katmanları, dikey erozyon olukları. (Altı y'ye kadar kapalı.)"""
    r = RNG(tohum)
    n = 80
    gur = deger_gurultusu(n + 1, n / dalga, r)
    pts = [(x0 + (x1 - x0) * i / n, y - h * (.55 + .45 * (abs(gur[i]) ** .6)) ) for i in range(n + 1)]
    d = egri_d(pts) + f" L{f(x1)} {f(y)} L{f(x0)} {f(y)} Z"
    kl = s.klip(f'<path d="{d}"/>', ad="ts")
    o = [f'<path d="{d}" fill="{renkler[0]}"/>', f'<g clip-path="{kl}">']
    for k in range(katman):
        yy = y - h + h * (k + 1) / (katman + 1) + r.uniform(-h * .04, h * .04)
        kal = h / (katman + 1) * r.uniform(.35, .7)
        c = renkler[(k + 1) % len(renkler)]
        dal = " ".join(f"{f(x0 + (x1 - x0) * i / 24)} {f(yy + math.sin(i * .9 + k) * h * .02)}" for i in range(25))
        o.append(f'<path d="M{dal} L{f(x1)} {f(yy + kal)} L{f(x0)} {f(yy + kal)} Z" fill="{c}" opacity=".8"/>')
    if oluk:
        for k in range(int((x1 - x0) / 34)):
            px = x0 + r.uniform(0, 1) * (x1 - x0)
            i = min(n, max(0, int((px - x0) / (x1 - x0) * n)))
            top = pts[i][1]
            o.append(f'<path d="M{f(px)} {f(top + 4)} q{f(r.uniform(-6, 6))} {f((y - top) * .5)} {f(r.uniform(-4, 4))} {f(y - top)}" stroke="{koyu(renkler[0], .25)}" stroke-width="{f(r.uniform(1.2, 3))}" fill="none" opacity=".35"/>')
    # gölge yanı: sağa bakan yamaçlar
    gl = s.lin([(0, "#3A2A4A", 0), (1, "#3A2A4A", .18)], 0, y - h, 0, y, kull="userSpaceOnUse", ad="tg")
    o.append(f'<rect x="{f(x0)}" y="{f(y - h)}" width="{f(x1 - x0)}" height="{f(h)}" fill="{gl}"/>')
    o.append("</g>")
    o.append(f'<path d="{egri_d(pts)}" stroke="#FFFFFF" stroke-width="2" fill="none" opacity=".45"/>')
    return "".join(o), pts


def uchisar_kaya(s, x, y, w, h, tohum=7, tas="#EDD6B2", isik=-1, bayrak=True, isikli=False, pencere=1.0):
    """Uçhisar Kalesi: içi oyulmuş dev tüf kayası (temsilî). (x, y) taban ortası. Döndürür (svg, tepe noktası)."""
    r = RNG(tohum)
    prof = [(-.5, 0), (-.47, -.18), (-.42, -.34), (-.36, -.44), (-.3, -.5), (-.24, -.62), (-.18, -.72), (-.1, -.84), (-.04, -.94), (.03, -1.0),
            (.1, -.96), (.15, -.86), (.2, -.8), (.27, -.74), (.33, -.62), (.38, -.5), (.43, -.36), (.47, -.2), (.5, 0)]
    pts = [(x + w * px + r.uniform(-w * .008, w * .008), y + h * py + (r.uniform(-h * .015, h * .015) if -1 < py < 0 else 0)) for px, py in prof]
    d = egri_d(pts, gerginlik=.8) + " Z"
    g = s.lin([(0, acik(tas, .25)), (.45, tas), (1, koyu(tas, .22))], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="uk")
    o = [f'<path d="{d}" fill="{g}"/>']
    kl = s.klip(f'<path d="{d}"/>', ad="ukk")
    ic = []
    # dikey kaya damarları + yatay katman izleri
    for k in range(14):
        px = x + w * r.uniform(-.42, .42)
        ic.append(f'<path d="M{f(px)} {f(y - h * r.uniform(.5, 1))} q{f(r.uniform(-10, 10))} {f(h * .3)} {f(r.uniform(-6, 6))} {f(h * .9)}" stroke="{koyu(tas, .2)}" stroke-width="{f(w * .006)}" fill="none" opacity=".4"/>')
    for k in range(5):
        yy = y - h * (.12 + k * .17)
        ic.append(f'<path d="M{f(x - w / 2)} {f(yy)} Q{f(x)} {f(yy + r.uniform(-8, 8))} {f(x + w / 2)} {f(yy)}" stroke="{acik(tas, .3)}" stroke-width="{f(h * .012)}" fill="none" opacity=".35"/>')
    # gölge tarafı
    gl = s.lin([(0, "#2A1E3A", 0), (.55, "#2A1E3A", 0), (1, "#2A1E3A", .28)], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="ug")
    ic.append(f'<rect x="{f(x - w / 2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{gl}"/>')
    # oyma odalar: pencere/kapı açıklıkları
    sayi = int(42 * pencere)
    for k in range(sayi):
        py = y - h * r.uniform(.12, .86)
        t = (y - py) / h
        yarı = .44 - .36 * t ** 1.4
        px = x + w * r.uniform(-yarı, yarı) + w * .02
        gw = w * r.uniform(.012, .022)
        gh = gw * r.uniform(1.2, 1.9)
        renk = (r.choice(["#FFD27A", "#FFE6A0", "#F7B955"]) if (isikli and r.random() < .7) else koyu(tas, .6))
        if r.random() < .45:
            ic.append(f'<path d="M{f(px - gw)} {f(py + gh)} V{f(py)} A{f(gw)} {f(gw)} 0 0 1 {f(px + gw)} {f(py)} V{f(py + gh)} Z" fill="{renk}"/>')
        else:
            ic.append(f'<rect x="{f(px - gw)}" y="{f(py)}" width="{f(gw * 2)}" height="{f(gh)}" fill="{renk}"/>')
    o.append(f'<g clip-path="{kl}">{"".join(ic)}</g>')
    tepe = (x + w * .03, y - h)
    if bayrak:
        bx, by = tepe[0], tepe[1] + h * .02
        o.append(f'<path d="M{f(bx)} {f(by)} v{f(-h * .22)}" stroke="#4A3A2E" stroke-width="{f(max(2, h * .008))}"/>')
        o.append(turk_bayragi(bx, by - h * .22, h * .085, h * .01))
    return "".join(o), tepe


def testi(s, x, y, h, renk=KIL, tohum=0, kulp=True, desen=True, bicim="testi"):
    """Avanos çömleği (temsilî). (x, y) taban ortası. bicim: testi (kulplu, dar boyunlu) | kup (geniş) | kase."""
    r = RNG(tohum)
    w = h * (.62 if bicim == "testi" else .8)
    g = s.lin([(0, acik(renk, .28)), (.45, renk), (1, koyu(renk, .35))], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="ts")
    cz = koyu(renk, .55)
    lw = max(.8, h * .018)
    o = [f'<ellipse cx="{f(x + w * .1)}" cy="{f(y)}" rx="{f(w * .55)}" ry="{f(h * .05)}" fill="#1B1D26" opacity=".2"/>']
    if bicim == "kase":
        o.append(f'<path d="M{f(x - w / 2)} {f(y - h)} Q{f(x - w * .45)} {f(y)} {f(x)} {f(y)} Q{f(x + w * .45)} {f(y)} {f(x + w / 2)} {f(y - h)} Z" fill="{g}" stroke="{cz}" stroke-width="{f(lw)}"/>')
        o.append(f'<ellipse cx="{f(x)}" cy="{f(y - h)}" rx="{f(w / 2)}" ry="{f(h * .14)}" fill="{koyu(renk, .3)}" stroke="{cz}" stroke-width="{f(lw)}"/>')
        return "".join(o)
    boyun = w * (.2 if bicim == "testi" else .3)
    d = (f"M{f(x - boyun)} {f(y - h)} L{f(x - boyun)} {f(y - h * .82)} C{f(x - w * .58)} {f(y - h * .72)} {f(x - w * .58)} {f(y - h * .18)} {f(x - w * .2)} {f(y)} "
         f"L{f(x + w * .2)} {f(y)} C{f(x + w * .58)} {f(y - h * .18)} {f(x + w * .58)} {f(y - h * .72)} {f(x + boyun)} {f(y - h * .82)} L{f(x + boyun)} {f(y - h)} Z")
    if kulp and bicim == "testi":
        o.append(f'<path d="M{f(x + boyun)} {f(y - h * .9)} C{f(x + w * .62)} {f(y - h * .92)} {f(x + w * .6)} {f(y - h * .6)} {f(x + w * .4)} {f(y - h * .5)}" stroke="{cz}" stroke-width="{f(h * .07)}" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{f(x + boyun)} {f(y - h * .9)} C{f(x + w * .62)} {f(y - h * .92)} {f(x + w * .6)} {f(y - h * .6)} {f(x + w * .4)} {f(y - h * .5)}" stroke="{renk}" stroke-width="{f(h * .04)}" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="{d}" fill="{g}" stroke="{cz}" stroke-width="{f(lw)}" stroke-linejoin="round"/>')
    o.append(f'<ellipse cx="{f(x)}" cy="{f(y - h)}" rx="{f(boyun * 1.25)}" ry="{f(h * .04)}" fill="{koyu(renk, .25)}" stroke="{cz}" stroke-width="{f(lw)}"/>')
    if desen:
        yy = y - h * r.uniform(.45, .55)
        zz = " ".join(f"{'M' if i == 0 else 'L'}{f(x - w * .4 + i * w * .08)} {f(yy + (h * .04 if i % 2 else -h * .04))}" for i in range(11))
        o.append(f'<path d="{zz}" stroke="#F6E7BF" stroke-width="{f(lw * 1.2)}" fill="none" opacity=".9"/>')
        o.append(f'<path d="M{f(x - w * .42)} {f(yy - h * .1)} H{f(x + w * .42)} M{f(x - w * .4)} {f(yy + h * .1)} H{f(x + w * .4)}" stroke="#F6E7BF" stroke-width="{f(lw * .8)}" opacity=".8"/>')
    o.append(f'<path d="M{f(x - w * .3)} {f(y - h * .7)} Q{f(x - w * .36)} {f(y - h * .4)} {f(x - w * .22)} {f(y - h * .15)}" stroke="#FFFFFF" stroke-width="{f(lw * 1.6)}" fill="none" opacity=".4" stroke-linecap="round"/>')
    return "".join(o)


def firin(s, x, y, w, h, tohum=0, ates=True):
    """Çömlek fırını (temsilî): tuğla kubbe, kemerli ağızda ateş ve sıcak ışık. (x, y) taban ortası."""
    r = RNG(tohum)
    o = []
    if ates:
        gl = s.rad([(0, "#FFE9A8", .85), (.35, "#FFB43A", .4), (1, "#FF7A3D", 0)], x, y - h * .25, w * .95, kull="userSpaceOnUse", ad="fg")
        o.append(f'<circle cx="{f(x)}" cy="{f(y - h * .25)}" r="{f(w * .95)}" fill="{gl}"/>')
    d = f"M{f(x - w / 2)} {f(y)} V{f(y - h * .45)} Q{f(x - w / 2)} {f(y - h)} {f(x)} {f(y - h)} Q{f(x + w / 2)} {f(y - h)} {f(x + w / 2)} {f(y - h * .45)} V{f(y)} Z"
    g = s.lin([(0, "#D98A5A"), (.5, "#B5603A"), (1, "#7E3A22")], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="fk")
    o.append(f'<path d="{d}" fill="{g}" stroke="#4A2414" stroke-width="{f(w * .012)}"/>')
    kl = s.klip(f'<path d="{d}"/>', ad="fkk")
    t = []
    for row in range(9):
        yy = y - row * h * .11
        off = (row % 2) * w * .06
        for col in range(-6, 7):
            t.append(f'<rect x="{f(x + col * w * .12 + off - w * .055)}" y="{f(yy - h * .1)}" width="{f(w * .11)}" height="{f(h * .095)}" rx="{f(w * .01)}" fill="none" stroke="#6E3018" stroke-width="{f(w * .006)}" opacity=".55"/>')
    o.append(f'<g clip-path="{kl}">{"".join(t)}</g>')
    aw = w * .2
    o.append(f'<path d="M{f(x - aw)} {f(y)} V{f(y - h * .25)} A{f(aw)} {f(aw)} 0 0 1 {f(x + aw)} {f(y - h * .25)} V{f(y)} Z" fill="#2A140C"/>')
    if ates:
        o.append(f'<path d="M{f(x - aw * .8)} {f(y)} Q{f(x - aw * .6)} {f(y - h * .3)} {f(x - aw * .2)} {f(y - h * .38)} Q{f(x - aw * .1)} {f(y - h * .22)} {f(x)} {f(y - h * .42)} '
                 f'Q{f(x + aw * .25)} {f(y - h * .22)} {f(x + aw * .4)} {f(y - h * .33)} Q{f(x + aw * .7)} {f(y - h * .2)} {f(x + aw * .8)} {f(y)} Z" fill="#FF8A3D"/>'
                 f'<path d="M{f(x - aw * .45)} {f(y)} Q{f(x - aw * .3)} {f(y - h * .18)} {f(x)} {f(y - h * .26)} Q{f(x + aw * .3)} {f(y - h * .16)} {f(x + aw * .45)} {f(y)} Z" fill="#FFE08A"/>')
    o.append(f'<path d="M{f(x - w * .06)} {f(y - h)} v{f(-h * .12)} h{f(w * .12)} v{f(h * .12)}" fill="#7E3A22" stroke="#4A2414" stroke-width="{f(w * .01)}"/>')
    for k in range(3):
        o.append(f'<path d="M{f(x - w * .02 + k * 6)} {f(y - h * 1.14)} q{f(-w * .05)} {f(-h * .1)} 0 {f(-h * .2)} q{f(w * .05)} {f(-h * .1)} 0 {f(-h * .2)}" stroke="#C9BFB8" stroke-width="{f(w * .02)}" fill="none" opacity=".55" stroke-linecap="round"/>')
    return "".join(o)


def guvercinlik_yuzu(s, x0, x1, y_ust, y_alt, tohum, tas=TUF, isik=-1, sira=4):
    """Güvercinlik Vadisi kaya yüzü: oyma güvercinlik delikleri (beyaz ve kırmızı boyalı çerçeveli)."""
    r = RNG(tohum)
    o = []
    w = x1 - x0
    prof = [(x0, y_alt)] + [(x0 + w * i / 10, y_ust + (y_alt - y_ust) * .12 * math.sin(i * 1.3) + r.uniform(-8, 8)) for i in range(11)] + [(x1, y_alt)]
    g = s.lin([(0, acik(tas, .18)), (1, koyu(tas, .2))], 0, y_ust, 0, y_alt, kull="userSpaceOnUse", ad="gv")
    d = egri_d(prof[1:-1]) + f" L{f(x1)} {f(y_alt)} L{f(x0)} {f(y_alt)} Z"
    o.append(f'<path d="{d}" fill="{g}"/>')
    for k in range(sira):
        yy = y_ust + (y_alt - y_ust) * (.25 + .17 * k)
        n = int(w / 46)
        for j in range(n):
            if r.random() < .25:
                continue
            px = x0 + w * (j + .5) / n + r.uniform(-6, 6)
            gw = r.uniform(5, 8)
            o.append(f'<rect x="{f(px - gw * 1.9)}" y="{f(yy - gw * 1.9)}" width="{f(gw * 3.8)}" height="{f(gw * 3.6)}" rx="{f(gw)}" fill="{r.choice(["#FFFFFF", "#FFF4E2", "#C9563A"])}" opacity=".9"/>')
            o.append(f'<path d="M{f(px - gw)} {f(yy + gw)} V{f(yy - gw * .2)} A{f(gw)} {f(gw)} 0 0 1 {f(px + gw)} {f(yy - gw * .2)} V{f(yy + gw)} Z" fill="#3A2A26"/>')
    return "".join(o)


def guvercinler(x, y, w, h, n, tohum, renk="#FFFFFF", golge="#6E6A80"):
    r = RNG(tohum)
    out = []
    for _ in range(n):
        px, py = x + r.random() * w, y + r.random() * h
        o_ = r.uniform(.5, 1.1)
        k = r.uniform(-4, 4)
        out.append(f'<path d="M{f(px - 14 * o_)} {f(py - 2 * o_ + k)} Q{f(px - 7 * o_)} {f(py - 9 * o_ + k)} {f(px)} {f(py)} Q{f(px + 7 * o_)} {f(py - 9 * o_ + k)} {f(px + 14 * o_)} {f(py - 2 * o_ + k)} '
                   f'Q{f(px + 6 * o_)} {f(py - 3 * o_)} {f(px)} {f(py + 3 * o_)} Q{f(px - 6 * o_)} {f(py - 3 * o_)} {f(px - 14 * o_)} {f(py - 2 * o_ + k)} Z" fill="{renk}" stroke="{golge}" stroke-width=".8"/>')
    return "".join(out)


def _tasevler(s, x0, x1, y, n, tohum, olcek=1.0, renkler=("#F1DEC0", "#E8CDA6", "#F6E8D2", "#E2C39A"), egim=0.0):
    """Kapadokya taş evleri: düz damlı, kemerli kapılı küçük kübik evler (yamaçta merdivenlenir)."""
    r = RNG(tohum)
    out = []
    for k in range(n):
        x = x0 + (x1 - x0) * k / max(1, n - 1) + r.uniform(-6, 6)
        yy = y + egim * (x - x0) + r.uniform(-3, 3)
        w = r.uniform(34, 52) * olcek
        h = r.uniform(24, 38) * olcek
        c = r.choice(renkler)
        out.append(f'<rect x="{f(x)}" y="{f(yy - h)}" width="{f(w)}" height="{f(h)}" fill="{c}" stroke="{koyu(c, .35)}" stroke-width="{f(1.2 * olcek)}"/>')
        out.append(f'<rect x="{f(x + w * .62)}" y="{f(yy - h)}" width="{f(w * .38)}" height="{f(h)}" fill="#000" opacity=".1"/>')
        out.append(f'<rect x="{f(x - w * .04)}" y="{f(yy - h - h * .1)}" width="{f(w * 1.08)}" height="{f(h * .12)}" fill="{koyu(c, .22)}"/>')
        dw = w * .14
        out.append(f'<path d="M{f(x + w * .3 - dw)} {f(yy)} V{f(yy - h * .4)} A{f(dw)} {f(dw)} 0 0 1 {f(x + w * .3 + dw)} {f(yy - h * .4)} V{f(yy)} Z" fill="{koyu(c, .55)}"/>')
        out.append(f'<rect x="{f(x + w * .62)}" y="{f(yy - h * .7)}" width="{f(w * .16)}" height="{f(h * .22)}" fill="{koyu(c, .5)}"/>')
    return "".join(out)


def _bag_satirlari(s, x0, x1, y, h, tohum, renk="#7FA24E"):
    """Bağ / bahçe sıraları (perspektif yeşil şeritler)."""
    r = RNG(tohum)
    out = []
    for k in range(7):
        yy = y + h * k / 7
        out.append(f'<path d="M{f(x0 + r.uniform(0, 30))} {f(yy)} Q{f((x0 + x1) / 2)} {f(yy - 6)} {f(x1 - r.uniform(0, 30))} {f(yy + 2)}" stroke="{karis(renk, "#3F6E2E", k / 8)}" stroke-width="{f(3 + k * .9)}" stroke-dasharray="{f(6 + k)} {f(5 + k * .6)}" fill="none" opacity=".85"/>')
    return "".join(out)


# ================================================================== 1. DURAK · ERCİYES ETEĞİ (öğle)

def erciyes():
    s = Svg("gz-erc")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2F86D6"), (.5, "#86C8EE"), (1, "#E4F5FB")])
    s += _zemin(s, ufuk, "#B9BE6A")
    s += S.gunes(s, 330, 80, 32, hale="#FFF2C2", hale_r=320, guc=.8)
    for i, (x, y, w) in enumerate([(700, 140, 230), (1060, 96, 260), (1880, 130, 190), (420, 200, 150)]):
        s += S.bulut(s, x, y, w, 11 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    uzak = ""
    d, _ = S.dag(s, -80, 900, ufuk + 4, 320, 196, 12, renk="#9DB5CF", golge="#7E9BBB", bicim="tepe", sis="#D6ECF5", isik=-1, sirt=2, puruz=5)
    uzak += d
    # Küçük Erciyes (sol omuz) + Büyük Erciyes (sivri, karlı)
    d, _ = S.dag(s, 900, 1700, ufuk + 6, 1240, 150, 13, renk="#8193B8", golge="#5E709A", bicim="volkan", kar_y=196, kar="#FFFFFF",
                 kar_golge="#C9D6EE", sis="#C4E0EE", isik=-1, sirt=3, puruz=8)
    uzak += d
    d, _ = S.dag(s, 1050, 2260, ufuk + 6, 1640, 28, 14, renk="#7488B0", golge="#4F648F", bicim="sivri", kar_y=150, kar="#FFFFFF",
                 kar_golge="#C3D2EC", sis="#BFDDEE", isik=-1, sirt=8, puruz=14, kenar_isik="#F2F8FF")
    uzak += d
    s += uzak
    # teleferik hattı (yamaçta, temsilî)
    s += '<path d="M1380 292 L1560 196 L1700 128" stroke="#3A3F4B" stroke-width="2" fill="none" opacity=".7"/>'
    for t in (.15, .35, .55, .75, .9):
        x = 1380 + 320 * t
        y = 292 - 164 * t
        s += f'<path d="M{f(x)} {f(y)} v9" stroke="#3A3F4B" stroke-width="1.6"/><rect x="{f(x - 5)}" y="{f(y + 9)}" width="10" height="7" rx="2" fill="#E2533D"/>'
    # Kayseri ovası
    s += S.tepe_bandi(s, 0, W, ufuk + 30, 24, 15, "#C9C27A", "#A9B65E")[0]
    ova = s.lin([(0, "#B9BE6A"), (1, "#6E9A44")], 0, ufuk + 30, 0, H, kull="userSpaceOnUse", ad="ova")
    s += f'<path d="M0 {ufuk + 40} C600 {ufuk + 30} 1300 {ufuk + 56} 2100 {ufuk + 36} V{H} H0 Z" fill="{ova}"/>'
    # tarlalar
    r = RNG(16)
    for k in range(16):
        x = r.uniform(900, 2050)
        y = r.uniform(ufuk + 50, ufuk + 110)
        w = r.uniform(80, 170)
        c = r.choice(["#D8C26A", "#9DBB55", "#C9A24E", "#86AE4A", "#E2CF86"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w)} -6 l{f(-w * .15)} {f(w * .18)} l{f(-w)} 6 Z" fill="{c}" opacity=".75"/>'
    # yol
    s += f'<path d="M1180 {H} C1240 {ufuk + 120} 1420 {ufuk + 70} 1520 {ufuk + 40}" stroke="#E6D3AE" stroke-width="16" fill="none" opacity=".9"/>'
    s += f'<path d="M1180 {H} C1240 {ufuk + 120} 1420 {ufuk + 70} 1520 {ufuk + 40}" stroke="#FFFFFF" stroke-width="2.4" stroke-dasharray="12 12" fill="none" opacity=".8"/>'
    # Selçuklu kümbeti (Kayseri kümbetleri esinli) + kavaklar
    for i, (x, h) in enumerate([(1250, 150), (1282, 172), (1314, 140), (1990, 170), (2026, 150), (2062, 182)]):
        s += S.kavak(s, x, 404, h, 26, 20 + i, renk="#5A9C47")
    s += Y.kumbet(s, 1760, 418, 230, 21, tas="#D9B48C", cati="#B98A62", kenar=12)
    for i, x in enumerate((1560, 1640, 1900)):
        s += S.agac(s, x, 410, 30, 30 + i, renk="#7DB955", meyve="#E2533D" if i == 1 else None)
    s += S.cimen(1100, 2100, 452, 31, renk="#5C9A40", renk2="#86C25A", boy=13, cicek=["#FFFFFF", "#F0A21A", "#E2533D", "#B07CD8"])
    for k, (x, y, o) in enumerate([(980, 150, .8), (1040, 170, .55), (560, 120, .6)]):
        s += S.marti(x, y, o, 2 - k, renk="#2F3A55")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 2. DURAK · GÖREME (şafak, balonlar)

def goreme():
    s = Svg("gz-gor")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3C4C9E"), (.34, "#8C7CC6"), (.6, "#F2A2B6"), (.82, "#FFCDA0"), (1, "#FFE8C6")])
    s += _zemin(s, ufuk, "#EBC6A8")
    s += S.gunes(s, 520, 286, 40, cekirdek="#FFF8E6", hale="#FFC98A", hale_r=520, guc=.95)
    s += S.bulut_serit(s, 640, 170, 520, 12, "#FFE3EA", "#F6B0C4", .6)
    s += S.bulut_serit(s, 1300, 110, 480, 10, "#FFE6E0", "#F2A6BC", .55)
    # uzak balonlar (küçük) + orta balonlar
    r = RNG(40)
    for k in range(14):
        x = r.uniform(700, 2060)
        y = r.uniform(40, 200)
        rr = r.uniform(9, 20)
        s += balon(s, x, y, rr, 41 + k, op=.92, cizgi=False)
    s += tuf_sirt(s, -40, 2140, ufuk + 10, 70, 42, renkler=("#E7B8B4", "#F3D2C2", "#D9A2A6", "#FBE6D8"), dalga=9)[0]
    s += tuf_sirt(s, -40, 2140, ufuk + 60, 60, 43, renkler=("#F1D3BC", "#FBE9D6", "#E9C0A2", "#FFF3E4"), dalga=6)[0]
    for k, (x, y, rr) in enumerate([(1180, 150, 34), (1380, 210, 28), (990, 230, 22), (1560, 120, 40)]):
        s += balon(s, x, y, rr, 50 + k)
    # vadi tabanı
    g = s.lin([(0, "#E8C9A4"), (1, "#B98F68")], 0, ufuk + 60, 0, H, kull="userSpaceOnUse", ad="vt")
    s += f'<path d="M0 {ufuk + 70} C500 {ufuk + 60} 1200 {ufuk + 84} 2100 {ufuk + 64} V{H} H0 Z" fill="{g}"/>'
    s += _bag_satirlari(s, 700, 1500, ufuk + 100, 60, 44)
    # peri bacaları (sağ ön) — odak
    s += peri_kumesi(s, 1380, 2100, ufuk + 120, 8, 45, boy=(130, 230), renkler=(TUF, "#F6E6CF", "#ECD1B2"))
    # kalkan balon (alevli) — odak
    s += balon(s, 1790, 196, 92, 2, renk=("#E2533D", "#F0A21A"), alev=True, serit=True)
    s += balon(s, 1460, 300, 52, 6, renk=("#13A3A6", "#FFFFFF"), alev=True)
    s += peri_kumesi(s, 1500, 2100, H - 10, 5, 46, boy=(150, 260), en=(.5, .7), renkler=("#F4E2C8", "#EAD0AE"))
    s += S.cimen(1200, 2100, H - 2, 47, renk="#8C8A4A", renk2="#B5A862", boy=12)
    s += '<use href="#pamuk-sasiran" x="1945" y="330" width="112" height="128"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 3. DURAK · AVANOS (ikindi, Kızılırmak, çömlek)

def avanos():
    s = Svg("gz-ava")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#4A93D4"), (.45, "#A6D2EC"), (.78, "#FBE3B4"), (1, "#FFD69A")])
    s += _zemin(s, ufuk, "#CFAE84")
    s += S.gunes(s, 300, 120, 36, hale="#FFE0A0", hale_r=380, guc=.85)
    for i, (x, y, w) in enumerate([(760, 110, 220), (1150, 80, 260), (1700, 120, 200)]):
        s += S.bulut(s, x, y, w, 60 + i, ust="#FFFFFF", alt="#F3D9B8", op=.95)
    # arka tepe ve Avanos evleri (yamaçta)
    d, _ = S.dag(s, 700, 2240, ufuk + 6, 1500, 120, 61, renk="#D7B48E", golge="#B48E6E", bicim="tepe", sis="#F4DCC0", isik=-1, sirt=3, puruz=8)
    s += d
    s += _tasevler(s, 1160, 1980, ufuk - 14, 13, 62, olcek=1.0, egim=-.05)
    s += _tasevler(s, 1250, 2060, ufuk + 22, 12, 63, olcek=1.15, egim=-.03)
    s += tuf_sirt(s, -40, 900, ufuk + 6, 80, 64, renkler=("#E9C4A6", "#F6DEC6", "#DDB08E", "#FFF0DE"), dalga=5)[0]
    # Kızılırmak
    g = s.lin([(0, "#D9926A"), (.45, NEHIR), (1, "#7E3E26")], 0, ufuk + 40, 0, H, kull="userSpaceOnUse", ad="nh")
    s += f'<path d="M0 {ufuk + 46} C400 {ufuk + 36} 900 {ufuk + 60} 1300 {ufuk + 70} C1600 {ufuk + 78} 1900 {ufuk + 72} 2100 {ufuk + 80} V{H} H0 Z" fill="{g}"/>'
    s += S.dalga_cizgileri(0, ufuk + 60, 1500, 130, 65, renk="#FFE6D2", n=40, op=.55)
    # asma köprü (yaya köprüsü)
    s += Y.asma_kopru(s, 380, 1020, ufuk + 54, 22, 70, renk="#6E4A2E", halat="#3A2A1E")
    # kıyı (sağ ön): atölye zemini
    gk = s.lin([(0, "#D9B98E"), (1, "#A9835C")], 0, ufuk + 90, 0, H, kull="userSpaceOnUse", ad="kz")
    s += f'<path d="M1180 {H} C1240 {ufuk + 120} 1400 {ufuk + 98} 1600 {ufuk + 96} C1800 {ufuk + 94} 1980 {ufuk + 90} 2100 {ufuk + 88} V{H} Z" fill="{gk}"/>'
    for i, (x, h) in enumerate([(1130, 170), (1165, 196), (1200, 160), (2060, 200)]):
        s += S.kavak(s, x, ufuk + 100, h, 28, 66 + i, renk="#5E9A48")
    # fırın ve çömlekler (odak)
    s += firin(s, 1700, ufuk + 150, 250, 190, 67)
    s += f'<rect x="1360" y="{ufuk + 108}" width="230" height="10" rx="3" fill="#7A4E2E"/><path d="M1376 {ufuk + 118} v40 M1574 {ufuk + 118} v40" stroke="#5A3A22" stroke-width="7"/>'
    for k, (x, h, b) in enumerate([(1395, 64, "testi"), (1455, 52, "kup"), (1512, 70, "testi"), (1560, 34, "kase")]):
        s += testi(s, x, ufuk + 108, h, renk=[KIL, "#C8743A", "#A84A2A", "#D08A55"][k], tohum=70 + k, bicim=b)
    for k, (x, h, b) in enumerate([(1895, 120, "testi"), (1990, 92, "kup"), (2070, 110, "testi"), (1460, 104, "testi")]):
        s += testi(s, x, H - 6, h, renk=[KIL, "#C8743A", "#A84A2A", "#B9602F"][k], tohum=80 + k, bicim=b)
    s += '<use href="#pamuk-otur" x="1525" y="342" width="96" height="110"/>'
    s += S.sazlik(0, 300, H, 68, renk="#6E7A3E", bas="#7A4E2A", boy=60)
    s += S.marti(900, 160, .8, 2, renk="#3A3355")
    s += S.marti(960, 182, .55, -1, renk="#3A3355")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 4. DURAK · KIZILÇUKUR ÜSTÜ (balon sepetinde, sabah)

def kizilcukur():
    s = Svg("gz-kiz")
    s += S.gokyuzu(s, 0, 0, W, H, duraklar=[(0, "#3E8BD6"), (.45, "#9CCFF0"), (.75, "#FCE3C4"), (1, "#FFD2A6")])
    s += S.gunes(s, 260, 200, 36, cekirdek="#FFF8E2", hale="#FFD9A0", hale_r=420, guc=.9)
    s += S.bulut_serit(s, 560, 120, 460, 10, "#FFFFFF", "#F7D6DA", .55)
    # Kızılçukur sırtları: pembe-krem katmanlar
    s += tuf_sirt(s, -40, 2140, 330, 120, 90, renkler=("#E7A9A6", "#F4C9BC", "#D98E90", "#FBE2D6", "#EEB7A8"), dalga=9, katman=8)[0]
    s += tuf_sirt(s, -40, 2140, 400, 110, 91, renkler=("#F2C2AE", "#FBE3D2", "#E7A894", "#FFF0E4"), dalga=7, katman=6)[0]
    s += tuf_sirt(s, -40, 2140, 470, 90, 92, renkler=("#EAB59C", "#F8D9C4", "#DB9A82", "#FFEBDC"), dalga=11, katman=5)[0]
    s += _bag_satirlari(s, 300, 1100, 430, 30, 93, renk="#86A84E")
    # diğer balonlar
    for k, (x, y, rr, o) in enumerate([(1040, 210, 50, 1), (760, 300, 30, .95), (1240, 330, 26, .95), (560, 120, 22, .9), (900, 90, 18, .9),
                                       (1150, 70, 24, .9), (420, 300, 16, .85), (1330, 150, 36, 1)]):
        s += balon(s, x, y, rr, 100 + k, op=o)
    # bizim sepet (sağ ön): brülör çerçevesi, alev, ipler
    bx0, bx1, by = 1470, 1980, 300
    gl = s.rad([(0, "#FFF2C0", .9), (.4, "#FFB43A", .4), (1, "#FF7A3D", 0)], 1725, 70, 220, kull="userSpaceOnUse", ad="al")
    s += f'<circle cx="1725" cy="70" r="220" fill="{gl}"/>'
    s += (f'<path d="M1690 120 Q1676 60 1712 -10 Q1722 40 1740 -10 Q1770 64 1756 120 Z" fill="#FF8A3D"/>'
          f'<path d="M1704 122 Q1700 70 1722 20 Q1744 74 1740 122 Z" fill="#FFE08A"/>'
          f'<path d="M1708 124 Q1712 92 1722 70 Q1734 94 1736 124 Z" fill="#7FB8FF" opacity=".75"/>')
    s += f'<rect x="1660" y="120" width="130" height="34" rx="8" fill="#9AA6B2" stroke="#3A3F4B" stroke-width="4"/><path d="M1676 137 h98" stroke="#5E6874" stroke-width="5"/>'
    s += f'<path d="M1500 {by} L1676 152 M1950 {by} L1774 152 M1600 {by} L1690 152 M1850 {by} L1760 152" stroke="#3A3F4B" stroke-width="4" fill="none"/>'
    s += f'<path d="M1560 0 L1676 124 M1890 0 L1774 124" stroke="#4A4F5A" stroke-width="5"/>'
    # yolcular (sepetin içinde, belden yukarısı görünür)
    s += '<use href="#elif-aha" x="1468" y="132" width="210" height="221"/>'
    s += '<use href="#yusuf-gulen" x="1760" y="128" width="210" height="221"/>'
    s += '<use href="#pamuk-selam" x="1640" y="196" width="128" height="146"/>'
    # sepet (hasır örgü)
    gs = s.lin([(0, "#C8925A"), (1, "#8C5A30")], 0, by, 0, H, kull="userSpaceOnUse", ad="sp")
    s += f'<rect x="{bx0}" y="{by}" width="{bx1 - bx0}" height="{H - by + 20}" rx="14" fill="{gs}" stroke="#4A2E18" stroke-width="5"/>'
    s += f'<rect x="{bx0 - 12}" y="{by - 14}" width="{bx1 - bx0 + 24}" height="28" rx="12" fill="#7A4E2E" stroke="#4A2E18" stroke-width="4"/>'
    for k in range(1, 8):
        s += f'<path d="M{bx0} {by + 18 + k * 22} H{bx1}" stroke="#6E4422" stroke-width="3" opacity=".6"/>'
    for k in range(1, 12):
        x = bx0 + k * (bx1 - bx0) / 12
        s += f'<path d="M{f(x)} {by + 14} V{H}" stroke="#E0B07A" stroke-width="2.4" opacity=".55"/>'
    s += f'<rect x="{bx0 + 30}" y="{by + 40}" width="70" height="44" rx="8" fill="#F6E7BF" stroke="#4A2E18" stroke-width="3"/><path d="M{bx0 + 40} {by + 62} h50" stroke="#C9952B" stroke-width="4"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 5. DURAK · DERİNKUYU (yeraltı şehri kesiti)

def derinkuyu():
    s = Svg("gz-der")
    yuzey = 96
    s += S.gokyuzu(s, 0, 0, W, yuzey + 4, duraklar=[(0, "#3E8BD6"), (1, "#BFE6F7")])
    s += S.bulut(s, 1500, 60, 160, 120, op=.9)
    s += S.bulut(s, 1960, 48, 120, 121, op=.85)
    s += _tasevler(s, 1350, 2060, yuzey + 2, 11, 122, olcek=.85)
    for i, x in enumerate((1290, 1325, 2075)):
        s += S.kavak(s, x, yuzey + 2, 90, 18, 123 + i, renk="#5E9A48")
    # yer altı: tüf katmanları
    g = s.lin([(0, "#E8C9A0"), (.35, "#D7AE80"), (.7, "#C08D62"), (1, "#9C6C48")], 0, yuzey, 0, H, kull="userSpaceOnUse", ad="yt")
    s += f'<rect x="0" y="{yuzey}" width="{W}" height="{H - yuzey}" fill="{g}"/>'
    s += f'<path d="M0 {yuzey} H{W}" stroke="#7FA24E" stroke-width="8"/>'
    r = RNG(124)
    for k in range(7):
        yy = yuzey + 40 + k * 50 + r.uniform(-8, 8)
        s += f'<path d="M0 {f(yy)} C600 {f(yy + r.uniform(-12, 12))} 1400 {f(yy + r.uniform(-12, 12))} 2100 {f(yy)}" stroke="#B9875E" stroke-width="2" fill="none" opacity=".45"/>'
    for k in range(60):
        x, y = r.uniform(0, W), r.uniform(yuzey + 10, H)
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(1.5, 4))}" fill="#8C5E3E" opacity=".25"/>'
    oda = "#4A2E1E"

    def oda_ciz(x, y, w, h, lamba=True):
        o = f'<path d="M{f(x)} {f(y + h)} V{f(y + h * .35)} Q{f(x)} {f(y)} {f(x + w * .2)} {f(y)} H{f(x + w * .8)} Q{f(x + w)} {f(y)} {f(x + w)} {f(y + h * .35)} V{f(y + h)} Z" fill="{oda}"/>'
        if lamba:
            lx, ly = x + w * .5, y + h * .3
            gl = s.rad([(0, "#FFE6A0", .85), (.4, "#FFB43A", .35), (1, "#FFB43A", 0)], lx, ly, w * .45, kull="userSpaceOnUse", ad="lm")
            o += f'<circle cx="{f(lx)}" cy="{f(ly)}" r="{f(w * .45)}" fill="{gl}"/><circle cx="{f(lx)}" cy="{f(ly)}" r="4" fill="#FFF4C8"/>'
        return o
    # katlar (sol yarı sönük; levha önünde)
    for (x, y, w, h) in ((120, 150, 220, 70), (420, 160, 180, 60), (700, 250, 260, 70), (260, 300, 200, 64), (900, 360, 240, 70), (520, 380, 180, 60)):
        s += oda_ciz(x, y, w, h, lamba=False).replace(f'fill="{oda}"', f'fill="{oda}" opacity=".55"')
    # tüneller
    s += f'<path d="M340 200 H420 M600 200 H700 L700 280 M960 300 H1080 M1140 400 H1260 L1260 330" stroke="{oda}" stroke-width="26" fill="none" opacity=".55"/>'
    # sağ: odak katlar
    s += oda_ciz(1200, 140, 300, 90)       # 1. kat
    s += oda_ciz(1560, 150, 240, 80)
    s += oda_ciz(1300, 270, 340, 96)       # 2. kat (karakterler)
    s += oda_ciz(1780, 280, 260, 86)
    s += oda_ciz(1180, 380, 260, 80)       # 3. kat
    s += oda_ciz(1560, 390, 300, 70)
    s += f'<path d="M1500 200 H1560 M1640 330 H1780 M1440 420 H1560" stroke="{oda}" stroke-width="30" fill="none"/>'
    # merdivenler
    for k in range(6):
        s += f'<rect x="{1240 + k * 12}" y="{230 + k * 8}" width="14" height="6" fill="#C9A27A"/>'
    # havalandırma bacası (yüzeyden dibe)
    bx = 1700
    s += f'<rect x="{bx - 22}" y="{yuzey - 14}" width="44" height="{H - yuzey + 20}" fill="#2E1C12"/>'
    s += f'<rect x="{bx - 34}" y="{yuzey - 22}" width="68" height="14" rx="4" fill="#C9A27A" stroke="#7A5A3A" stroke-width="3"/>'
    for k in range(5):
        y = yuzey + 30 + k * 70
        s += f'<path d="M{bx} {y} v34 m-10 -12 l10 14 l10 -14" stroke="#7FD3F0" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    # taze hava yayılması (difüzyon noktaları)
    for k in range(40):
        x = bx + r.uniform(-260, 330)
        y = r.uniform(160, 440)
        if abs(x - bx) < 30:
            continue
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(2.5, 4.5))}" fill="#9FE3F5" opacity="{f(max(.15, .85 - abs(x - bx) / 400), 2)}"/>'
    # sürgü taşı (değirmen taşı biçimli kapı)
    tx, ty, tr = 1540, 330, 48
    gt = s.rad([(0, "#D9D2C8"), (.7, "#A89F94"), (1, "#7A7068")], .4, .35, .8, ad="st")
    s += f'<circle cx="{tx}" cy="{ty}" r="{tr}" fill="{gt}" stroke="#4A4038" stroke-width="5"/><circle cx="{tx}" cy="{ty}" r="10" fill="#4A4038"/>'
    s += f'<path d="M{tx - 30} {ty - 20} A36 36 0 0 1 {tx + 6} {ty - 36}" stroke="#FFFFFF" stroke-width="4" fill="none" opacity=".45"/>'
    # karakterler (2. katta)
    s += '<use href="#elif-soru" x="1330" y="262" width="100" height="105"/>'
    s += '<use href="#yusuf-anlatan" x="1420" y="262" width="100" height="105"/>'
    s += '<use href="#pamuk-dusunen" x="1590" y="296" width="62" height="71"/>'
    # tandır kokusu (3. kat mutfak): kıvrımlı koku çizgileri
    for k in range(3):
        s += f'<path d="M{1620 + k * 40} 450 q-14 -16 0 -32 q14 -16 0 -32" stroke="#FFD9A0" stroke-width="4" fill="none" opacity=".75" stroke-linecap="round"/>'
    s += f'<ellipse cx="1660" cy="452" rx="44" ry="10" fill="#7A3A22"/><ellipse cx="1660" cy="448" rx="30" ry="6" fill="#FF9A4A"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== HÜLASA · HASAN DAĞI ETEĞİ (altın saat, b40)

def hasan(h=400):
    s = Svg("gz-has")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#4C86C8"), (.42, "#A9C6E2"), (.78, "#F9D9AC"), (1, "#FFC98A")])
    s += _zemin(s, ufuk, "#A9BE62", h)
    s += S.gunes(s, 300, 150, 36, hale="#FFC77A", hale_r=380, guc=.9)
    for i, (x, y, w) in enumerate([(700, 90, 220), (1240, 60, 200)]):
        s += S.bulut(s, x, y, w, 140 + i, ust="#FFF6E8", alt="#F2C9A0", op=.95)
    uzak = ""
    d, _ = S.dag(s, 1150, 1900, ufuk + 6, 1480, 96, 141, renk="#B58FA6", golge="#806A94", bicim="volkan", kar_y=150, kar="#FFF1E8",
                 kar_golge="#D2BED8", sis="#F4CFB4", isik=-1, sirt=4, puruz=9, kenar_isik="#FFE3C8")
    uzak += d
    d, _ = S.dag(s, 1350, 2260, ufuk + 6, 1780, 30, 142, renk="#A986A2", golge="#73608C", bicim="sivri", kar_y=118, kar="#FFF1E8",
                 kar_golge="#CDB8D6", sis="#F4CFB4", isik=-1, sirt=6, puruz=12, kenar_isik="#FFE3C8")
    uzak += d
    d, _ = S.dag(s, -80, 900, ufuk + 6, 340, 176, 143, renk="#C7A7B4", golge="#A08AA6", bicim="tepe", sis="#F7D8BC", isik=-1, sirt=2, puruz=5)
    uzak += d
    s += uzak
    # uzakta peri bacası silüetleri
    s += peri_kumesi(s, 700, 1150, ufuk + 8, 6, 144, boy=(40, 70), renkler=("#E8C9B0", "#F0D6BE"), pencere=False)
    s += S.tepe_bandi(s, 0, W, ufuk + 40, 40, 145, "#B7C46A", "#93AE52")[0]
    s += S.tepe_bandi(s, 0, W, ufuk + 88, 36, 146, "#9CBF5A", "#6E9E44")[0]
    s += Y.cadir(s, 1500, ufuk + 112, 140, 104, renk="#9E2F28")
    s += Y.cadir(s, 1660, ufuk + 100, 104, 78, renk="#253C78", serit="#F0A21A")
    r = RNG(147)
    for k in range(16):
        x = 780 + r.uniform(0, 640)
        y = ufuk + 70 + r.uniform(0, 70)
        s += Y.koyun(x, y, 1.0 + (y - ufuk - 70) / 70 * .8, r.choice([1, -1]))
    s += S.cimen(0, W, h - 4, 148, renk="#4E8F3A", renk2="#7DBE55", boy=15, yogun=1.2, cicek=["#FFFFFF", "#F0A21A", "#E2533D", "#B07CD8", "#FFD24A"])
    s += '<use href="#pamuk-kitap" x="1880" y="236" width="140" height="160"/>'
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== MECLİS · GÜZELYURT TAŞ EVİ (iç mekân)

def guzelyurt():
    from cizim.sus import kilim_serit
    s = Svg("gz-guz")
    # taş örgü duvar
    g = s.lin([(0, "#F3E2C6"), (1, "#E2C9A2")], 0, 0, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect width="{W}" height="{H}" fill="{g}"/>'
    r = RNG(160)
    for row in range(9):
        y = row * 36
        off = 0 if row % 2 == 0 else 60
        for x in range(-60 + off, W, 120):
            s += f'<rect x="{x + 3}" y="{y + 3}" width="114" height="30" rx="5" fill="{karis("#F1DEBE", "#DCC09A", r.uniform(0, .7))}" stroke="#C4A57C" stroke-width="2"/>'
    # tonoz kemer izi
    s += f'<path d="M0 60 Q1050 -40 2100 60" stroke="#B89468" stroke-width="10" fill="none" opacity=".5"/>'
    # kemerli pencere: Hasan Dağı ve Güzelyurt evleri
    wx, wy, ww, wh = 1360, 46, 400, 196
    pen = Svg("gz-guz-p")
    pen += S.gokyuzu(pen, wx, wy, ww, wh * .62, "gun")
    pd, _ = S.dag(pen, wx - 30, wx + ww + 30, wy + wh * .62, wx + ww * .55, wy + 24, 161, renk="#8E93B8", golge="#636E9A",
                  bicim="sivri", kar_y=wy + 70, kar="#FFFFFF", kar_golge="#C9D6EE", sis="#C4E0EE", isik=-1, sirt=4, puruz=8)
    pen += pd
    pen += f'<rect x="{wx}" y="{f(wy + wh * .6)}" width="{ww}" height="{f(wh * .4)}" fill="#C8B07A"/>'
    pen += _tasevler(pen, wx + 10, wx + ww - 40, wy + wh - 6, 7, 162, olcek=.8)
    s.defs += pen.defs
    kemer = f"M{wx} {wy + wh} V{wy + 90} A{ww / 2} {ww / 2 * .55} 0 0 1 {wx + ww} {wy + 90} V{wy + wh} Z"
    kl = s.klip(f'<path d="{kemer}"/>', ad="pk")
    s += f'<g clip-path="{kl}">{"".join(pen.parca)}</g>'
    s += f'<path d="{kemer}" fill="none" stroke="#9C7A4E" stroke-width="16"/>'
    s += f'<path d="M{wx + ww / 2} {wy + 22} V{wy + wh} M{wx} {wy + 130} H{wx + ww}" stroke="#9C7A4E" stroke-width="8"/>'
    s += f'<rect x="{wx - 24}" y="{wy + wh}" width="{ww + 48}" height="14" fill="#B89468"/>'
    # nişler (taka) ve çömlekler, kandil
    for k, nx in enumerate((900, 1080)):
        s += f'<path d="M{nx} 220 V120 Q{nx} 92 {nx + 40} 88 Q{nx + 80} 92 {nx + 80} 120 V220 Z" fill="#C9A47A" stroke="#9C7A4E" stroke-width="5"/>'
        s += testi(s, nx + 40, 214, 60 if k == 0 else 48, renk=KIL if k == 0 else "#C8743A", tohum=163 + k, bicim="testi" if k == 0 else "kup")
    for nx in (1880, 1990):
        s += f'<path d="M{nx} 200 V110 Q{nx} 84 {nx + 36} 80 Q{nx + 72} 84 {nx + 72} 110 V200 Z" fill="#C9A47A" stroke="#9C7A4E" stroke-width="5"/>'
    lx, ly = 1952, 150
    gl = s.rad([(0, "#FFE9A8", .85), (.5, "#FFB43A", .25), (1, "#FFB43A", 0)], lx, ly, 120, kull="userSpaceOnUse", ad="kl")
    s += f'<circle cx="{lx}" cy="{ly}" r="120" fill="{gl}"/><ellipse cx="{lx}" cy="{ly + 14}" rx="22" ry="8" fill="#B9532F"/><path d="M{lx} {ly + 6} q-6 -12 0 -24 q6 12 0 24" fill="#FFB43A"/>'
    # sedir, kilim, minder
    s += f'<rect x="0" y="330" width="{W}" height="56" fill="#8E2A22"/>'
    kil = kilim_serit("gz-guz-k", 2100, 60).replace("<svg ", '<svg width="2100" height="60" ')
    s += f'<g transform="translate(0 330)">{kil}</g>'
    s += f'<rect x="-20" y="254" width="{W + 40}" height="80" rx="26" fill="#1D3A8A" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="M-20 270 H{W + 20} M-20 318 H{W + 20}" stroke="#F0A21A" stroke-width="4"/>'
    for x in range(30, W, 80):
        s += f'<path d="M{x} 276 L{x + 18} 294 L{x} 312 L{x - 18} 294 Z" fill="#E2533D" stroke="#F6E7BF" stroke-width="2.4"/>'
    s += f'<path d="M0 386 H{W} V{H} H0 Z" fill="#7A2A22"/><path d="M80 394 H{W - 80} L{W} {H} H0 Z" fill="#B23A2E"/>'
    for x in range(120, W - 100, 90):
        s += f'<path d="M{x} 406 l20 14 l-20 14 l-20 -14 Z" fill="#F0A21A"/>'
    # meclis: Elif, Pamuk, Yusuf + sini
    s += '<use href="#elif-soru" x="1290" y="180" width="260" height="273"/>'
    s += '<use href="#yusuf-anlatan" x="1790" y="180" width="260" height="273"/>'
    s += f'<ellipse cx="1676" cy="440" rx="130" ry="20" fill="#C9A86A" stroke="#7A5A2A" stroke-width="4"/>'
    for x in (1606, 1648, 1690, 1732):
        s += Y.cay_bardak_kucuk(x, 440, 26)
    s += '<use href="#pamuk-dusunen" x="1580" y="238" width="180" height="206"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== KISSA · IHLARA VADİSİ (sabah)

def ihlara():
    s = Svg("gz-ihl")
    s += S.gokyuzu(s, 0, 0, W, 300, duraklar=[(0, "#3F8ED8"), (.6, "#A6D6F0"), (1, "#E8F6FA")])
    s += _zemin(s, 280, "#7DA24E")
    s += S.gunes(s, 1180, 70, 28, hale="#FFF4CC", hale_r=260, guc=.8)
    s += S.bulut(s, 760, 90, 180, 170, op=.95)
    s += S.bulut(s, 1500, 70, 150, 171, op=.9)
    # sol duvar (uzak, alçak) ve sağ duvar (yakın, yüksek): katmanlı kanyon
    gL = s.lin([(0, "#E9B98A"), (1, "#B97E56")], 0, 160, 0, H, kull="userSpaceOnUse", ad="kl")
    s += f'<path d="M-20 {H} V230 C200 214 420 222 700 236 C820 244 900 262 960 300 L1000 {H} Z" fill="{gL}"/>'
    gR = s.lin([(0, "#E4A877"), (.5, "#C98652"), (1, "#8E5634")], 1100, 0, 2100, 0, kull="userSpaceOnUse", ad="kr")
    sag = [(1180, H), (1200, 330), (1260, 250), (1340, 170), (1440, 110), (1600, 70), (1800, 52), (2000, 40), (2140, 36), (2140, H)]
    s += f'<path d="{cizgi_d(sag, True)}" fill="{gR}"/>'
    r = RNG(172)
    kl = s.klip(f'<path d="{cizgi_d(sag, True)}"/>', ad="kk")
    ic = []
    for k in range(9):
        yy = 60 + k * 44
        ic.append(f'<path d="M1150 {yy} C1500 {yy + r.uniform(-14, 14)} 1800 {yy - 12 + r.uniform(-10, 10)} 2140 {yy - 20}" stroke="#F2C49A" stroke-width="{f(r.uniform(3, 8))}" fill="none" opacity=".5"/>')
    for k in range(18):
        px, py = r.uniform(1350, 2080), r.uniform(120, 360)
        ww = r.uniform(10, 18)
        ic.append(f'<path d="M{f(px - ww)} {f(py + ww * 1.4)} V{f(py)} A{f(ww)} {f(ww)} 0 0 1 {f(px + ww)} {f(py)} V{f(py + ww * 1.4)} Z" fill="#5A3420" opacity=".8"/>')
    s += f'<g clip-path="{kl}">{"".join(ic)}</g>'
    # Melendiz Çayı (uzaktan yakına genişler)
    gs = s.lin([(0, "#BDEDEE"), (1, "#2C9BA6")], 0, 280, 0, H, kull="userSpaceOnUse", ad="cy")
    s += f'<path d="M900 290 C960 300 1010 320 980 350 C940 390 1000 420 1180 440 L1500 {H} L760 {H} C800 430 760 400 820 360 C860 330 860 304 900 290 Z" fill="{gs}"/>'
    s += S.dalga_cizgileri(820, 360, 600, 100, 173, n=24, op=.75)
    # yeşillik: kavaklar, söğütler
    for k, (x, y, h) in enumerate([(700, 330, 130), (740, 336, 150), (1090, 330, 140), (1130, 336, 120), (600, 360, 160), (1240, 380, 170)]):
        s += S.kavak(s, x, y, h, 28, 174 + k, renk="#4F9445")
    for k, (x, y, r0) in enumerate([(820, 400, 40), (1080, 410, 44), (560, 430, 52), (1300, 440, 50)]):
        s += S.agac(s, x, y, r0, 180 + k, renk="#5FA048")
    # tahta köprü
    s += f'<path d="M820 410 Q960 396 1110 414" stroke="#7A4E2E" stroke-width="12" fill="none"/><path d="M820 392 Q960 378 1110 396" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    for k in range(7):
        x = 830 + k * 45
        s += f'<path d="M{x} {404 - abs(k - 3) * 2} v-18" stroke="#5A3A22" stroke-width="4"/>'
    s += S.cimen(0, 2100, H - 2, 185, renk="#3F7A36", renk2="#6EA84E", boy=14, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += S.kaya(s, 1700, 452, 220, 64, 186, renk="#9C7056")
    s += '<use href="#pamuk-kitap" x="1640" y="292" width="122" height="139"/>'
    s += S.marti(1500, 130, .7, 2, renk="#3A3E4A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== ANAHTAR · GÜVERCİNLİK VADİSİ (gün batımı)

def guvercinlik():
    s = Svg("gz-guv")
    ufuk = 280
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3A4C9C"), (.4, "#8E7BC0"), (.72, "#F7A6A0"), (1, "#FFD39A")])
    s += _zemin(s, ufuk, "#C99A7A")
    s += S.gunes(s, 1260, 250, 38, hale="#FFC27A", hale_r=400, guc=.9)
    s += S.bulut_serit(s, 1080, 150, 520, 14, "#FFD0C4", "#F28FA0", .7)
    s += S.bulut_serit(s, 1480, 96, 460, 12, "#FFC9B8", "#E9849C", .6)
    s += tuf_sirt(s, -40, 2140, ufuk + 4, 60, 190, renkler=("#C9A2B0", "#E2BFC0", "#B88EA2", "#F0D6D2"), dalga=8)[0]
    # Uçhisar silüeti (arkada, sağ)
    uk, _ = uchisar_kaya(s, 1840, ufuk + 20, 380, 230, 191, tas="#D8B6A6", bayrak=True, pencere=.6)
    s += uk
    s += _tasevler(s, 1600, 2080, ufuk + 26, 10, 192, olcek=.75, renkler=("#E8C9B6", "#DDB7A4", "#F0D8C8"))
    # vadi: güvercinlikli kaya yüzleri
    s += guvercinlik_yuzu(s, 1080, 1620, 270, H, 193, tas="#F0D2B8")
    s += guvercinlik_yuzu(s, 1700, 2140, 330, H, 194, tas="#EAC7AC", sira=3)
    gv = s.lin([(0, "#C99A7A"), (1, "#8C5E44")], 0, 340, 0, H, kull="userSpaceOnUse", ad="vd")
    s += f'<path d="M0 {H} V350 C300 334 700 352 1080 360 L1080 {H} Z" fill="{gv}"/>'
    s += _bag_satirlari(s, 200, 1000, 380, 60, 195, renk="#7A9A48")
    # taş basamaklar (vadiye inen)
    for k in range(7):
        x = 1620 + k * 14
        y = 330 + k * 20
        s += f'<rect x="{x}" y="{y}" width="90" height="16" rx="3" fill="#E8C9A4" stroke="#9C7A56" stroke-width="2.4"/>'
    s += guvercinler(1150, 140, 700, 160, 14, 196)
    s += S.cimen(1060, 2100, H - 2, 197, renk="#7E8A44", renk2="#A9B05A", boy=12)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== BÜYÜK İMTİHAN · UÇHİSAR KALESİ (62 mm)

def uchisar_buyuk(h=620):
    s = Svg("gz-uch")
    ufuk = 430
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#2F5DA8"), (.38, "#86A9D6"), (.7, "#F6C99A"), (1, "#FFB46B")])
    s += _zemin(s, ufuk, "#D9B98E", h)
    s += S.gunes(s, 240, 340, 50, hale="#FFB45A", hale_r=520, guc=.95)
    for i, (x, y, w) in enumerate([(520, 150, 300), (980, 96, 340), (1700, 70, 240)]):
        s += S.bulut(s, x, y, w, 200 + i, ust="#FFF4E4", alt="#F0A98A", op=.95)
    s += S.bulut_serit(s, 300, 260, 600, 16, "#FFD8B0", "#F08A7A", .6)
    # uzakta Erciyes (karlı) ve tüf sırtları
    d, _ = S.dag(s, 300, 1100, ufuk + 6, 700, 300, 201, renk="#B78FA8", golge="#8C6A92", bicim="sivri", kar_y=336, kar="#FFE8E4",
                 kar_golge="#D2B6CC", sis="#F7C2A8", isik=-1, sirt=4, puruz=10)
    s += d
    s += tuf_sirt(s, -40, 2140, ufuk + 20, 70, 202, renkler=("#E9B8A8", "#F6D6C6", "#D9A196", "#FFEBDE"), dalga=10)[0]
    # Uçhisar Kalesi (odak, sağ)
    uk, tepe = uchisar_kaya(s, 1560, ufuk + 110, 820, 520, 203, tas="#EED7B4", bayrak=True)
    s += uk
    s += _tasevler(s, 1080, 2080, ufuk + 112, 20, 204, olcek=1.1)
    s += _tasevler(s, 1150, 2060, ufuk + 160, 16, 205, olcek=1.35)
    g = s.lin([(0, "#D9B98E"), (1, "#A9835C")], 0, ufuk + 140, 0, h, kull="userSpaceOnUse", ad="zm")
    s += f'<path d="M0 {ufuk + 150} C500 {ufuk + 130} 1000 {ufuk + 160} 2100 {ufuk + 150} V{h} H0 Z" fill="{g}"/>'
    s += peri_kumesi(s, 0, 900, ufuk + 170, 7, 206, boy=(80, 150))
    for k in range(10):
        x = 900 + k * 120
        s += S.kavak(s, x, h - 6, 150 + (k % 3) * 20, 26, 207 + k, renk="#5E8E3E")
    s += S.cimen(0, W, h - 4, 218, renk="#6E8A3E", renk2="#9DB85A", boy=16, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += guvercinler(900, 160, 500, 160, 9, 219)
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== BÜYÜK İMTİHAN 2 · KALE KAPISI (30 mm)

def uchisar_kapi(h=300):
    s = Svg("gz-kap")
    s += S.gokyuzu(s, 0, 0, W, h, duraklar=[(0, "#F7B07A"), (1, "#FFE1B0")])
    g = s.lin([(0, "#F1DCBC"), (1, "#D7B48C")], 0, 0, 0, h, kull="userSpaceOnUse", ad="dv")
    prof = [(0, 40), (300, 26), (700, 34), (1100, 20), (1500, 30), (1900, 18), (2100, 24)]
    s += f'<path d="{egri_d(prof)} V{h} H0 Z" fill="{g}"/>'
    r = RNG(230)
    for k in range(26):
        x = r.uniform(0, W)
        s += f'<path d="M{f(x)} 40 q{f(r.uniform(-12, 12))} 110 {f(r.uniform(-8, 8))} 260" stroke="#C9A27A" stroke-width="{f(r.uniform(2, 5))}" fill="none" opacity=".4"/>'
    for k in range(4):
        yy = 80 + k * 60
        s += f'<path d="M0 {yy} C700 {yy + r.uniform(-8, 8)} 1400 {yy + r.uniform(-8, 8)} 2100 {yy}" stroke="#FFF2DE" stroke-width="5" fill="none" opacity=".5"/>'
    # oyma pencereler
    for k in range(16):
        px, py = r.uniform(700, 2060), r.uniform(70, 200)
        if 1250 < px < 1650:
            continue
        ww = r.uniform(14, 22)
        s += f'<path d="M{f(px - ww)} {f(py + ww * 1.5)} V{f(py)} A{f(ww)} {f(ww)} 0 0 1 {f(px + ww)} {f(py)} V{f(py + ww * 1.5)} Z" fill="#5A3A26"/>'
    # kapı: kemerli, aralık, sıcak ışık
    cx = 1450
    s += f'<path d="M{cx - 150} {h} V150 Q{cx - 150} 70 {cx} 56 Q{cx + 150} 70 {cx + 150} 150 V{h} Z" fill="#B88E62"/>'
    s += f'<path d="M{cx - 122} {h} V156 Q{cx - 122} 92 {cx} 80 Q{cx + 122} 92 {cx + 122} 156 V{h} Z" fill="#3A2614"/>'
    isik = s.rad([(0, "#FFF4C8", .95), (.5, "#FFD27A", .5), (1, "#FFD27A", 0)], cx, 200, 260, kull="userSpaceOnUse", ad="ki")
    s += f'<path d="M{cx - 26} {h} V100 L{cx + 26} 100 V{h} Z" fill="#FFE9A8"/><circle cx="{cx}" cy="200" r="260" fill="{isik}"/>'
    for sx in (-1, 1):
        x0, x1 = cx + sx * 26, cx + sx * 116
        s += f'<path d="M{x0} {h} V104 Q{(x0 + x1) / 2} 90 {x1} 130 V{h} Z" fill="#6E4422" stroke="#3A2614" stroke-width="4"/>'
        for k in range(4):
            yy = 140 + k * 38
            s += f'<path d="M{x0} {yy} H{x1}" stroke="#3A2614" stroke-width="5"/>'
            for j in range(3):
                s += f'<circle cx="{x0 + sx * (20 + j * 30)}" cy="{yy}" r="4" fill="#C9A86A"/>'
    # fenerler
    for x in (cx - 230, cx + 230):
        s += f'<path d="M{x} 96 v22" stroke="#3A2614" stroke-width="4"/><rect x="{x - 16}" y="118" width="32" height="44" rx="6" fill="#FFE08A" stroke="#5A3A22" stroke-width="4"/>'
        al = s.rad([(0, "#FFF4C8", .9), (1, "#FFB43A", 0)], x, 140, 70, kull="userSpaceOnUse", ad="fn")
        s += f'<circle cx="{x}" cy="140" r="70" fill="{al}"/>'
    # basamaklar ve kilim
    for k in range(3):
        s += f'<rect x="{cx - 200 - k * 30}" y="{h - 14 - (2 - k) * 14}" width="{400 + k * 60}" height="16" fill="#D9BC92" stroke="#9C7A56" stroke-width="2"/>'
    from cizim.sus import kilim_serit
    kil = kilim_serit("gz-kap-k", 220, 60).replace("<svg ", '<svg width="220" height="60" ')
    s += f'<g transform="translate(2040 30) rotate(90) translate(0 -60)">{kil}</g>'
    s += '<use href="#pamuk-akce" x="1670" y="128" width="150" height="171"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== CEVAPLAR · KAPADOKYA GECESİ (36 mm)

def kapadokya_gece(h=360):
    s = Svg("gz-gec")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, h, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk, 160, 240)
    s += S.ay(s, 1180, 80, 32, golge_renk="#13204A")
    s += tuf_sirt(s, -40, 2140, ufuk + 10, 60, 241, renkler=("#2C3768", "#34407A", "#262F5C", "#3B4888"), dalga=8, oluk=False)[0]
    uk, _ = uchisar_kaya(s, 1700, ufuk + 60, 520, 260, 242, tas="#3E4677", bayrak=True, isikli=True, pencere=.8)
    s += uk
    s += peri_kumesi(s, 400, 1400, h - 10, 9, 243, boy=(90, 170), renkler=("#3A4272", "#434C80", "#353D6A"), isikli=True)
    g = s.lin([(0, "#1C2350"), (1, "#0E1230")], 0, ufuk + 60, 0, h, kull="userSpaceOnUse", ad="zm")
    s += f'<path d="M0 {h - 20} C600 {h - 34} 1400 {h - 16} 2100 {h - 28} V{h} H0 Z" fill="{g}"/>'
    r = RNG(244)
    for k in range(30):
        x = r.uniform(1350, 2080)
        y = r.uniform(ufuk + 40, ufuk + 90)
        s += f'<rect x="{f(x)}" y="{f(y)}" width="7" height="8" fill="#FFD27A" opacity="{f(r.uniform(.6, 1), 2)}"/>'
    s += '<use href="#pamuk-otur" x="260" y="250" width="90" height="103"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== FİNAL · BALONLAR VE UÇHİSAR (90 mm)

def final_kapadokya(h=900, nisanlar=None):
    s = Svg("gz-fin")
    ufuk = 600
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3A4CA0"), (.3, "#8A7CC8"), (.55, "#F29CB4"), (.78, "#FFC892"), (1, "#FFE6C0")])
    gx, gy = 640, ufuk - 30
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE8B0" opacity=".12"/>'
    s += _zemin(s, ufuk, "#EBC6A8", h)
    s += S.gunes(s, gx, gy, 66, hale="#FFC98A", hale_r=680, guc=.95)
    for (x, y, w_, k) in ((200, 260, 520, 20), (1100, 170, 600, 24), (1500, 340, 460, 14)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFE0E6", "#F7A6BC", .7)
    r = RNG(250)
    for k in range(16):
        x, y = r.uniform(100, 2050), r.uniform(60, 480)
        s += balon(s, x, y, r.uniform(10, 26), 251 + k, op=.9, cizgi=False)
    s += tuf_sirt(s, -40, 2140, ufuk + 20, 110, 270, renkler=("#E7B8B4", "#F3D2C2", "#D9A2A6", "#FBE6D8"), dalga=9)[0]
    s += tuf_sirt(s, -40, 2140, ufuk + 110, 90, 271, renkler=("#F1D3BC", "#FBE9D6", "#E9C0A2", "#FFF3E4"), dalga=7)[0]
    # Uçhisar (sağ) + Pamuk bayrakla zirvede
    uk, tepe = uchisar_kaya(s, 1760, h + 10, 620, 470, 272, tas="#F0D9B6", bayrak=False)
    s += uk
    s += f'<use href="#pamuk-bayrak" x="{f(tepe[0] - 150)}" y="{f(tepe[1] - 330)}" width="300" height="353"/>'
    g = s.lin([(0, "#E3C29A"), (1, "#B48C62")], 0, ufuk + 160, 0, h, kull="userSpaceOnUse", ad="zm")
    s += f'<path d="M0 {ufuk + 170} C500 {ufuk + 150} 1000 {ufuk + 190} 1500 {ufuk + 180} L1500 {h} H0 Z" fill="{g}"/>'
    s += peri_kumesi(s, 0, 1400, h - 6, 10, 273, boy=(150, 280), en=(.42, .58))
    # büyük balon (sol) ve nişan çelengi: balon sepetinden Uçhisar'ın bayrak direğine
    bx, by, br = 330, 300, 130
    s += balon(s, bx, by, br, 2, renk=("#E2533D", "#F0A21A"), alev=True, serit=True)
    sx, sy = bx + br * .17, by + br * 1.6
    ex, ey = tepe[0] - 40, tepe[1] - 70
    kx, ky = (sx + ex) / 2, max(sy, ey) + 180
    s += f'<path d="M{f(sx)} {f(sy)} Q{f(kx)} {f(ky)} {f(ex)} {f(ey)}" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .7) / (len(nisanlar) + .4)
            x = (1 - t) ** 2 * sx + 2 * (1 - t) * t * kx + t * t * ex
            y = (1 - t) ** 2 * sy + 2 * (1 - t) * t * ky + t * t * ey
            s += f'<path d="M{f(x)} {f(y)} v16" stroke="#5A3A22" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 56)} {f(y + 12)}) rotate({f((k % 2 * 2 - 1) * 5)} 56 64)">{ns}</g>'
    for k in range(60):
        x, y = r.uniform(300, 1900), r.uniform(80, 640)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== AÇILIŞ · KAPADOKYA PANORAMASI + TUR ROTASI

# Stilize (temsilî) yerleşim: güneyden kuzeye değil, KUZEYDEN GÜNEYE bakış (uzak = güney). Doğu solda: Erciyes sol arkada,
# Hasan Dağı sağ arkada, Kızılırmak önde (kuzey). Kümelenen Göreme–Uçhisar–Avanos çevresi okunur olsun diye açılarak çizildi.
# (anahtar, x, y, etiket üst, etiket ad, alt, tür)
DURAKLAR = [
    ("1", 300, 560, "1. DURAK · ERCİYES", "Gaz ve basınç", "s.2 · +100 akçe", "durak"),
    ("2", 905, 742, "2. DURAK · GÖREME", "Boyle ve Charles", "s.3 · +150 akçe", "durak"),
    ("3", 1030, 968, "3. DURAK · AVANOS", "Üç yasa bir arada", "s.4 · +150 akçe", "durak"),
    ("4", 690, 676, "4. DURAK · KIZILÇUKUR", "İdeal gaz", "s.5 · +150 akçe", "durak"),
    ("5", 1150, 512, "5. DURAK · DERİNKUYU", "Yoğunluk, yayılma", "s.6 · +150 akçe", "durak"),
    ("H", 1700, 452, "HASAN DAĞI ETEĞİ", "Hülasa", "s.7 · +40 akçe", "hulasa"),
    ("M", 1560, 548, "GÜZELYURT", "Meclis: Kim haklı?", "s.8 · +120 akçe", "yan"),
    ("K", 1830, 606, "IHLARA VADİSİ", "Kıssa", "s.9 · +120 akçe", "yan"),
    ("A", 1250, 806, "GÜVERCİNLİK VADİSİ", "Anahtar merdiveni", "s.10 · +120 akçe", "yan"),
    ("V", 1380, 700, "UÇHİSAR KALESİ", "Büyük İmtihan", "s.11–12 · +300 akçe", "kale"),
]
ROTA_ARA = {("1", "2"): [(520, 640), (720, 720)], ("2", "3"): [(960, 860)], ("3", "4"): [(860, 900), (720, 800)],
            ("4", "5"): [(840, 600), (1000, 540)], ("5", "H"): [(1400, 470)], ("H", "M"): [(1650, 500)], ("M", "K"): [(1700, 600)],
            ("K", "A"): [(1700, 760), (1450, 860)], ("A", "V"): [(1330, 770)]}


def kapadokya_panorama(h=1100):
    s = Svg("gz-pan")
    ufuk = 360
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#34449A"), (.3, "#7E70C0"), (.55, "#EE98B2"), (.8, "#FFC892"), (1, "#FFE4BE")])
    gx, gy = 140, ufuk - 40
    for k in range(12):
        a0 = math.pi + .1 + k * (math.pi - .2) / 12
        a1 = a0 + .05
        s += f'<path d="M{gx} {gy} L{f(gx + 2400 * math.cos(a0))} {f(gy + 2400 * math.sin(a0))} L{f(gx + 2400 * math.cos(a1))} {f(gy + 2400 * math.sin(a1))} Z" fill="#FFE4B0" opacity=".09"/>'
    s += S.gunes(s, gx, gy, 50, hale="#FFC56B", hale_r=600, guc=.95)
    for (x, y, w_, k) in ((620, 150, 520, 18), (1240, 96, 600, 22), (1700, 220, 400, 14)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFD2C0", "#F790A8", .75)
    # gökyüzünde balonlar
    r = RNG(300)
    for k in range(22):
        x, y = r.uniform(560, 2050), r.uniform(50, 330)
        s += balon(s, x, y, r.uniform(10, 24), 301 + k, op=.95, cizgi=False)
    for k, (x, y, rr) in enumerate([(820, 250, 34), (1010, 190, 28), (640, 330, 24), (1240, 290, 30)]):
        s += balon(s, x, y, rr, 330 + k)
    # uzak dağlar: Erciyes (sol), Hasan Dağı (sağ)
    uzak = ""
    d, _ = S.dag(s, -120, 820, ufuk + 8, 330, 70, 340, renk="#C78CAE", golge="#7F5C96", bicim="sivri", kar_y=150, kar="#FFE6EE",
                 kar_golge="#C6A7D2", sis="#FFA18E", isik=-1, sirt=7, puruz=12, kenar_isik="#FFD7C2")
    uzak += d
    d, _ = S.dag(s, 1380, 2240, ufuk + 8, 1760, 170, 341, renk="#B486AA", golge="#74578C", bicim="volkan", kar_y=226, kar="#FFE0E6",
                 kar_golge="#C3A3CC", sis="#FFA18E", isik=-1, sirt=4, puruz=8)
    uzak += d
    d, _ = S.dag(s, 1560, 2000, ufuk + 8, 1620, 224, 342, renk="#A97CA0", golge="#6E5288", bicim="volkan", kar_y=262, kar="#FFE0E6",
                 kar_golge="#C3A3CC", sis="#FFA18E", isik=-1, sirt=2, puruz=6)
    uzak += d
    s += uzak
    # kara: tüf ovası (uzakta pembe sis, önde sıcak okr)
    gk = s.lin([(0, "#D9A2A0"), (.15, "#E7BE9E"), (.5, "#E2C392"), (1, "#B9A162")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kara")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    # tüf sırtları ve vadiler (orta plan)
    s += tuf_sirt(s, -40, 2140, ufuk + 70, 50, 343, renkler=("#E7B4A8", "#F2CDBE", "#DDA59A", "#FBE2D6"), dalga=12)[0]
    s += tuf_sirt(s, 380, 1300, 760, 70, 344, renkler=("#EDB9A8", "#F7D9C8", "#E0A694", "#FFEBDE"), dalga=8)[0]
    # tarla yamaları ve bağlar
    for k in range(60):
        x = r.uniform(0, W)
        y = r.uniform(ufuk + 90, h - 40)
        sc = .45 + (y - ufuk) / (h - ufuk)
        w_ = r.uniform(60, 150) * sc
        c = r.choice(["#C9C27A", "#A9C46A", "#D3B86A", "#8FB24E", "#E2CF86"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w_)} {f(-w_ * .06)} l{f(-w_ * .2)} {f(w_ * .3)} l{f(-w_)} {f(w_ * .06)} Z" fill="{c}" opacity=".5"/>'
    # Kızılırmak (önde, kuzey)
    g = s.lin([(0, "#D9926A"), (1, "#8C4A2E")], 0, 940, 0, h, kull="userSpaceOnUse", ad="nh")
    nehir = "M-20 1010 C300 990 600 1040 900 1010 C1200 980 1500 1030 1800 1000 C1950 985 2050 995 2120 990 L2120 1060 C1900 1068 1600 1086 1300 1060 C1000 1034 700 1084 400 1066 C200 1054 60 1070 -20 1072 Z"
    s += f'<path d="{nehir}" fill="{g}"/>'
    s += f'<path d="M100 1030 h120 M520 1046 h90 M1100 1024 h140 M1600 1040 h100" stroke="#FFE6D2" stroke-width="3" opacity=".6"/>'
    # simge yapılar
    s += peri_kumesi(s, 760, 1060, 730, 7, 345, boy=(40, 80), en=(.45, .6))       # Göreme
    s += peri_kumesi(s, 1080, 1330, 820, 6, 346, boy=(36, 66))                      # Güvercinlik
    uk, _ = uchisar_kaya(s, 1410, 690, 150, 120, 347, tas="#F0D6B0", bayrak=True, pencere=.5)
    s += uk
    s += _tasevler(s, 1320, 1500, 700, 6, 348, olcek=.5)
    # Avanos: evler + çömlek
    s += _tasevler(s, 980, 1160, 960, 6, 349, olcek=.55)
    s += testi(s, 1170, 968, 30, tohum=350)
    s += testi(s, 1196, 970, 22, tohum=351, bicim="kup")
    # Erciyes eteği: kümbet + kavak
    s += Y.kumbet(s, 380, 560, 70, 352, tas="#E2B48C", cati="#C08A62")
    # Derinkuyu: yeraltı girişi + baca
    s += f'<path d="M1110 520 h80 v-14 a40 22 0 0 0 -80 0 Z" fill="#7A5A3A"/><path d="M1124 520 v-10 a26 14 0 0 1 52 0 v10 Z" fill="#2E1C12"/>'
    s += _tasevler(s, 1200, 1300, 506, 3, 353, olcek=.45)
    # Güzelyurt + Ihlara kanyonu
    s += _tasevler(s, 1520, 1620, 540, 4, 354, olcek=.45)
    s += f'<path d="M1760 590 C1800 600 1840 640 1900 650 L1916 640 C1860 626 1820 590 1780 580 Z" fill="#9C6A48"/>'
    s += f'<path d="M1770 588 C1810 602 1846 632 1902 646" stroke="#5FC0C8" stroke-width="5" fill="none"/>'
    # Hasan Dağı eteği: çadır + koyunlar
    s += Y.cadir(s, 1660, 452, 40, 30, renk="#9E2F28")
    for k in range(4):
        s += Y.koyun(1700 + k * 14, 456 + (k % 2) * 3, .55)
    # kavaklar ve köyler (rozet çevresi boş)
    konum = {k: (x, y) for (k, x, y, *_r) in DURAKLAR}
    for k in range(70):
        x = r.uniform(20, 2080)
        y = r.uniform(ufuk + 100, 1000)
        if any(math.hypot(x - a, y - b) < 90 for a, b in konum.values()):
            continue
        sc = .35 + (y - ufuk) / 700 * .9
        if r.random() < .6:
            for j in range(3):
                s += S.kavak(s, x + j * 16 * sc, y, 64 * sc, 12 * sc, 400 + k * 3 + j, renk="#5E9A4A")
        else:
            for j in range(2):
                s += S.agac(s, x + j * 30 * sc, y, 14 * sc, 500 + k * 2 + j, renk=r.choice(["#6FAA4E", "#7DB955"]))
    # rota
    sira = [d_[0] for d_ in DURAKLAR]
    yol = []
    for i, k in enumerate(sira):
        yol.append(konum[k])
        if i + 1 < len(sira):
            yol += ROTA_ARA.get((k, sira[i + 1]), [])
    yd = egri_d(yol, False, .9)
    s += f'<path d="{yd}" fill="none" stroke="#1B1D26" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
    s += f'<path d="{yd}" fill="none" stroke="#FFF1CF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="3.2" stroke-dasharray="12 9" stroke-linecap="round"/>'
    for (k, x, y, *_r) in DURAKLAR:
        tur = _r[3]
        if tur == "durak":
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 36), True)}" fill="#F0C14A" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 29), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 11)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="32" fill="#FFFFFF">{k}</text>'
        elif tur == "kale":
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="34" fill="#E2533D" stroke="#1B1D26" stroke-width="3"/>'
            s += f'<path d="M{f(x - 18)} {f(y + 14)} V{f(y - 6)} h6 v-6 h6 v6 h4 v-6 h6 v6 h4 v-6 h6 v6 h4 V{f(y + 14)} Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
        else:
            renk = "#F0A21A" if tur == "yan" else "#7B3F8C"
            s += f'<path d="M{f(x)} {f(y - 32)} L{f(x + 32)} {f(y)} L{f(x)} {f(y + 32)} L{f(x - 32)} {f(y)} Z" fill="{renk}" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 10)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="27" fill="#FFFFFF">{k}</text>'
    x, y = konum["1"]
    s += f'<path d="M{f(x + 36)} {f(y + 40)} v-64" stroke="#1B1D26" stroke-width="4"/><path d="M{f(x + 38)} {f(y - 22)} h44 l-10 13 l10 13 h-44 Z" fill="#E2533D" stroke="#1B1D26" stroke-width="2.4"/>'
    # yer adları (haritada, halolu)
    for (ad_, x, y, fs) in (("Erciyes", 330, 120, 44), ("Hasan Dağı", 1760, 214, 40), ("Kızılırmak", 330, 1050, 34)):
        s += halolu_yazi(f'x="{x}" y="{y}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="{fs}" letter-spacing="1"', ad_, "#FFFFFF", "#5A2E4A", 1.6)
    s += '<use href="#pamuk-selam" x="520" y="900" width="104" height="119"/>'
    s += S.marti(1500, 1010, 1.4, 6, ayrintili=True)
    # pusula
    px, py = 1960, h - 140
    s += f'<circle cx="{px}" cy="{py}" r="74" fill="#FFFFFF" opacity=".9" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 66, 14, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 34), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="10" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py + 104}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), konum
