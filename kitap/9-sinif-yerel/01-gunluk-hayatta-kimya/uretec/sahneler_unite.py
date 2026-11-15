"""Günlük Hayatta Kimya · İznik–Bursa Yolu — üniteye özel sahneler, nişan ikonları ve açılış panoraması.

kur_ortak bu modüle {{sahne|ad}} için ORTAK kütüphaneden (yerel-ortak/cizim) ÖNCE bakar. Ortak dosyalar değiştirilmez;
buradaki her şey ortak parçalardan (sahne, yapilar, karakter sembolleri) ve aşağıdaki Bursa parçalarından kurulur:
  goknar · serv · buhar · cini_karo · cini_vazo · osmanli_ev · hamam · sur · saat_kulesi · han_cephe · esarp_ipi ·
  koza_cuvali · boya_kazani · cile_diregi · mangal · piknik_masasi · kabin · leylek · zeytin
Kompozisyon (TASARIM-SISTEMI §6): bant 2100×460 birim; sol üst ≈ %60 × %75 sakin gökyüzü/su (levha oturur); odak sağ
%40'ta (x > 1300); ışık solda (isik=-1); tohumlar sabit; her Svg öneki benzersiz; konturlu SVG yazısı yok (halolu_yazi).
Yerler temsilîdir. Cami, kilise, manastır çizilmez; Koza Han avlusundaki mescit de çizilmedi.
"""
import math
from cizim.temel import (Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari,
                         rng as RNG)
from cizim import sahne as S, yapilar as Y
from cizim.sahneler import W, H, _bitir, _cerceve_golge

# ------------------------------------------------------------------ İznik–Bursa paleti
KOBALT, KOBALT_K = "#2B50B5", "#1B3584"
TURKUAZ = "#13A3A6"
MERCAN = "#E2533D"
CINI_YESIL = "#1F8A5B"
TAS, TAS_K = "#D9C3A0", "#A88A62"        # Bursa taşı
TUGLA = "#B85C3E"
CATI = "#B8553A"
YESIL, YESIL_K = "#4E9A44", "#2F6B36"   # yeşil Bursa
GOKNAR, GOKNAR_K = "#2F6B4A", "#1C4A33"
IPEK = ["#E2533D", "#F0A21A", "#7B3F8C", "#13A3A6", "#2B50B5", "#FF5C8A", "#1F8A5B", "#F6E7BF"]
EV_RENK = ["#C29BD8", "#F0C05A", "#A9DCC0", "#F4ABA4", "#A8CCEE", "#F6EEDC"]   # Cumalıkızık sıvaları

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    "cini": '<rect x="7" y="7" width="34" height="34" rx="2"/><path d="M7 16 A9 9 0 0 0 16 7 M32 7 A9 9 0 0 0 41 16 M41 32 A9 9 0 0 0 32 41 M16 41 A9 9 0 0 0 7 32"/>'
            '<circle cx="24" cy="24" r="3.4"/><path d="M24 12 C20.5 15.5 21 19.5 24 20.6 C27 19.5 27.5 15.5 24 12 Z M24 36 C20.5 32.5 21 28.5 24 27.4 C27 28.5 27.5 32.5 24 36 Z'
            ' M12 24 C15.5 20.5 19.5 21 20.6 24 C19.5 27 15.5 27.5 12 24 Z M36 24 C32.5 20.5 28.5 21 27.4 24 C28.5 27 32.5 27.5 36 24 Z"/>',
    "ph": '<path d="M24 4 C24 4 10 20 10 29 A14 14 0 0 0 38 29 C38 20 24 4 24 4 Z"/><path d="M16 31 H32"/><path d="M16 28 V34 M21.3 29 V33 M26.7 29 V33 M32 28 V34"/>'
          '<path d="M17 21 C18 17 20 14 22 12"/>',
    "sise": '<path d="M20 4 H28 V11 L32 17 V41 A3 3 0 0 1 29 44 H19 A3 3 0 0 1 16 41 V17 L20 11 Z"/><path d="M20 8 H28"/><rect x="18.5" y="23" width="11" height="12" rx="1.5"/><path d="M21 27 H27 M21 31 H25"/>',
    "deney": '<path d="M8 9 H26 M10 9 V36 A5 5 0 0 0 15 41 H19 A5 5 0 0 0 24 36 V9"/><path d="M10 25 H24"/><path d="M14 31 h3 M18 34 h2"/>'
             '<path d="M35 6 V31"/><circle cx="35" cy="36" r="4.4"/><path d="M32.5 6 H37.5 M35 18 H39 M35 24 H39"/>',
    "koza": '<ellipse cx="19" cy="27" rx="10" ry="15" transform="rotate(-25 19 27)"/><path d="M12 19 C16 23 21 23 25 18 M11 27 C15 31 21 31 26 26 M13 35 C16 37 20 37 23 34"/>'
            '<path d="M27 13 C33 7 41 10 39 17 C37 24 43 28 45 23"/>',
}


# ================================================================== PARÇALAR

def _zemin(s, y, renk, h=H):
    """Ufkun altına düz zemin: katmanlar arasında gökyüzü boşluğu kalmasın."""
    return f'<rect x="0" y="{f(y)}" width="{W}" height="{f(h - y + 2)}" fill="{renk}"/>'


def goknar(x, y, h, tohum=0, renk=GOKNAR, golge=GOKNAR_K, isik=-1, op=1.0):
    """Uludağ göknarı: katlı üçgen taç. (x, y) gövde tabanı, h boy."""
    r = RNG(tohum)
    out = [f'<g opacity="{f(op, 2)}">' if op < 1 else "<g>",
           f'<rect x="{f(x - h * .028)}" y="{f(y - h * .16)}" width="{f(h * .056)}" height="{f(h * .17)}" fill="#5A3E2A"/>']
    n = 5
    for i in range(n):
        t = i / n
        yb = y - h * .12 - h * .7 * t
        yt = yb - h * .34
        w = h * .5 * (1 - t * .72) * r.uniform(.9, 1.08)
        out.append(f'<path d="M{f(x - w / 2)} {f(yb)} Q{f(x - w * .18)} {f(yb - h * .1)} {f(x)} {f(yt)} Q{f(x + w * .18)} {f(yb - h * .1)} {f(x + w / 2)} {f(yb)} '
                   f'Q{f(x)} {f(yb - h * .05)} {f(x - w / 2)} {f(yb)} Z" fill="{renk}"/>')
        gx = x + w / 2 if isik < 0 else x - w / 2
        out.append(f'<path d="M{f(x)} {f(yt)} Q{f(x - isik * w * .18)} {f(yb - h * .1)} {f(gx)} {f(yb)} Q{f(x - isik * w * .2)} {f(yb - h * .045)} {f(x)} {f(yb - h * .03)} Z" fill="{golge}" opacity=".85"/>')
    out.append("</g>")
    return "".join(out)


def serv(s, x, y, h, tohum=0, renk="#2E6B45"):
    """Selvi: ince, koyu yeşil."""
    return S.kavak(s, x, y, h, h * .17, tohum, renk=renk, golge="#1B4A2C", gov="#5A4030")


def buhar(s, x, y, h, tohum=0, w=40, op=.75):
    """Yükselen buhar: yukarı doğru büyüyüp silinen yumuşak bulutçuklar (filtre yok, radyal gradyan)."""
    r = RNG(tohum)
    g = s.rad([(0, "#FFFFFF", .95), (.6, "#FFFFFF", .5), (1, "#FFFFFF", 0)], ad="bh")
    out = []
    n = 7
    for i in range(n):
        t = i / (n - 1)
        px = x + math.sin(t * 5.2 + tohum) * w * .45 * t + r.uniform(-4, 4)
        py = y - h * t
        rr = w * (.35 + .75 * t)
        out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(rr)}" fill="{g}" opacity="{f(op * (1 - .8 * t), 2)}"/>')
    return "".join(out)


def cini_karo(x, y, a, desen=0, zemin="#FBFDFD"):
    """İznik çinisi karosu (a × a). desen 0: sekiz yapraklı gül + köşe yarımları · 1: lale + saz yaprağı."""
    c, k = a / 2, a * .03
    out = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(a)}" height="{f(a)}" fill="{zemin}"/>']
    for (qx, qy, a0) in ((x, y, 0), (x + a, y, 90), (x + a, y + a, 180), (x, y + a, 270)):
        out.append(f'<path d="M{f(qx)} {f(qy)} m0 0 h{f(a * .24)} A{f(a * .24)} {f(a * .24)} 0 0 1 {f(qx)} {f(qy + a * .24)} Z" fill="{TURKUAZ}" transform="rotate({a0} {f(qx)} {f(qy)})"/>')
        out.append(f'<circle cx="{f(qx)}" cy="{f(qy)}" r="{f(a * .07)}" fill="{MERCAN}"/>')
    if desen == 0:
        for j in range(8):
            out.append(f'<ellipse cx="{f(x + c)}" cy="{f(y + c - a * .19)}" rx="{f(a * .075)}" ry="{f(a * .15)}" fill="{KOBALT}" transform="rotate({j * 45} {f(x + c)} {f(y + c)})"/>')
        out.append(f'<circle cx="{f(x + c)}" cy="{f(y + c)}" r="{f(a * .1)}" fill="{MERCAN}"/><circle cx="{f(x + c)}" cy="{f(y + c)}" r="{f(a * .04)}" fill="#FFFFFF"/>')
    else:
        cx_, cy_ = x + c, y + c
        out.append(f'<path d="M{f(cx_)} {f(cy_ + a * .34)} C{f(cx_ - a * .02)} {f(cy_ + a * .1)} {f(cx_)} {f(cy_)} {f(cx_)} {f(cy_ - a * .05)}" stroke="{CINI_YESIL}" stroke-width="{f(a * .035)}" fill="none"/>')
        out.append(f'<path d="M{f(cx_)} {f(cy_ + a * .28)} C{f(cx_ - a * .3)} {f(cy_ + a * .2)} {f(cx_ - a * .34)} {f(cy_ - a * .08)} {f(cx_ - a * .3)} {f(cy_ - a * .2)} '
                   f'C{f(cx_ - a * .2)} {f(cy_ - a * .02)} {f(cx_ - a * .1)} {f(cy_ + a * .14)} {f(cx_)} {f(cy_ + a * .28)} Z" fill="{KOBALT}"/>')
        out.append(f'<path d="M{f(cx_)} {f(cy_ + a * .24)} C{f(cx_ + a * .28)} {f(cy_ + a * .18)} {f(cx_ + a * .32)} {f(cy_ - a * .04)} {f(cx_ + a * .28)} {f(cy_ - a * .16)} '
                   f'C{f(cx_ + a * .18)} {f(cy_)} {f(cx_ + a * .08)} {f(cy_ + a * .12)} {f(cx_)} {f(cy_ + a * .24)} Z" fill="{TURKUAZ}"/>')
        out.append(f'<path d="M{f(cx_ - a * .12)} {f(cy_ - a * .04)} Q{f(cx_ - a * .17)} {f(cy_ - a * .27)} {f(cx_ - a * .07)} {f(cy_ - a * .33)} L{f(cx_)} {f(cy_ - a * .2)} '
                   f'L{f(cx_ + a * .07)} {f(cy_ - a * .33)} Q{f(cx_ + a * .17)} {f(cy_ - a * .27)} {f(cx_ + a * .12)} {f(cy_ - a * .04)} Q{f(cx_)} {f(cy_ + a * .04)} {f(cx_ - a * .12)} {f(cy_ - a * .04)} Z" fill="{MERCAN}"/>')
    out.append(f'<rect x="{f(x + k / 2)}" y="{f(y + k / 2)}" width="{f(a - k)}" height="{f(a - k)}" fill="none" stroke="{KOBALT_K}" stroke-width="{f(k)}"/>')
    return "".join(out)


def cini_pano(x, y, nx, ny, a, kenar=True):
    out = [cini_karo(x + i * a, y + j * a, a, (i + j) % 2) for j in range(ny) for i in range(nx)]
    if kenar:
        out.append(f'<rect x="{f(x - a * .1)}" y="{f(y - a * .1)}" width="{f(nx * a + a * .2)}" height="{f(ny * a + a * .2)}" fill="none" stroke="{KOBALT_K}" stroke-width="{f(a * .14)}"/>')
    return "".join(out)


def cini_vazo(s, x, y, h, tohum=0):
    """İznik çinisi vazo (x: orta, y: taban). Desen: kobalt bantlar, mercan lale, turkuaz yaprak."""
    w = h * .62
    gov = (f"M{f(x - w * .2)} {f(y - h)} H{f(x + w * .2)} L{f(x + w * .16)} {f(y - h * .8)} C{f(x + w * .6)} {f(y - h * .68)} {f(x + w * .58)} {f(y - h * .2)} "
           f"{f(x + w * .22)} {f(y - h * .06)} L{f(x + w * .26)} {f(y)} H{f(x - w * .26)} L{f(x - w * .22)} {f(y - h * .06)} "
           f"C{f(x - w * .58)} {f(y - h * .2)} {f(x - w * .6)} {f(y - h * .68)} {f(x - w * .16)} {f(y - h * .8)} Z")
    g = s.lin([(0, "#FFFFFF"), (.55, "#F2F6FA"), (1, "#C9D6E4")], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="vz")
    kl = s.klip(f'<path d="{gov}"/>', ad="vk")
    out = [f'<ellipse cx="{f(x + 8)}" cy="{f(y)}" rx="{f(w * .45)}" ry="{f(h * .045)}" fill="#000" opacity=".18"/>',
           f'<path d="{gov}" fill="{g}"/>', f'<g clip-path="{kl}">']
    out.append(f'<rect x="{f(x - w)}" y="{f(y - h)}" width="{f(2 * w)}" height="{f(h * .2)}" fill="{KOBALT}"/>')
    out.append(f'<rect x="{f(x - w)}" y="{f(y - h * .13)}" width="{f(2 * w)}" height="{f(h * .13)}" fill="{KOBALT}"/>')
    out.append(f'<rect x="{f(x - w)}" y="{f(y - h * .79)}" width="{f(2 * w)}" height="{f(h * .035)}" fill="{TURKUAZ}"/>')
    for k in range(-2, 3):
        cx_ = x + k * w * .22
        out.append(f'<path d="M{f(cx_)} {f(y - h * .17)} C{f(cx_ - w * .02)} {f(y - h * .3)} {f(cx_)} {f(y - h * .42)} {f(cx_)} {f(y - h * .45)}" stroke="{CINI_YESIL}" stroke-width="{f(h * .012)}" fill="none"/>')
        out.append(f'<path d="M{f(cx_ - w * .06)} {f(y - h * .45)} Q{f(cx_ - w * .08)} {f(y - h * .58)} {f(cx_ - w * .03)} {f(y - h * .6)} L{f(cx_)} {f(y - h * .53)} '
                   f'L{f(cx_ + w * .03)} {f(y - h * .6)} Q{f(cx_ + w * .08)} {f(y - h * .58)} {f(cx_ + w * .06)} {f(y - h * .45)} Z" fill="{MERCAN if k % 2 == 0 else KOBALT}"/>')
        out.append(f'<path d="M{f(cx_)} {f(y - h * .25)} q{f(w * .09)} {f(-h * .02)} {f(w * .1)} {f(-h * .1)} q{f(-w * .07)} {f(h * .02)} {f(-w * .1)} {f(h * .1)} Z" fill="{TURKUAZ}"/>')
    out.append(f'<path d="M{f(x - w)} {f(y - h * .7)} q{f(w * .25)} {f(-h * .04)} {f(w * .5)} 0 t{f(w * .5)} 0 t{f(w * .5)} 0 t{f(w * .5)} 0" stroke="{KOBALT}" stroke-width="{f(h * .014)}" fill="none"/>')
    out.append(f'<rect x="{f(x + w * .05)}" y="{f(y - h)}" width="{f(w * .7)}" height="{f(h)}" fill="#13243F" opacity=".12"/></g>')
    out.append(f'<path d="{gov}" fill="none" stroke="#1B1D26" stroke-width="{f(h * .012)}" stroke-linejoin="round"/>')
    out.append(f'<ellipse cx="{f(x)}" cy="{f(y - h)}" rx="{f(w * .2)}" ry="{f(h * .02)}" fill="{KOBALT_K}" stroke="#1B1D26" stroke-width="{f(h * .01)}"/>')
    return "".join(out)


def osmanli_ev(s, x, y, w, h, duvar="#F6EEDC", cati=CATI, tohum=0, cumba=True, isik=-1, kat_tas=.4, cizgi="#5A4030"):
    """Bursa / Cumalıkızık evi: taş zemin kat, sıvalı ve çıkmalı üst kat (ahşap karkas), geniş saçaklı kiremit çatı."""
    r = RNG(tohum)
    zk = h * kat_tas
    ck = w * .07
    k = max(1.2, w * .012)
    out = [f'<rect x="{f(x)}" y="{f(y - zk)}" width="{f(w)}" height="{f(zk)}" fill="{TAS}" stroke="{cizgi}" stroke-width="{f(k)}"/>']
    for j in range(1, 3):
        out.append(f'<path d="M{f(x)} {f(y - zk * j / 3)} H{f(x + w)}" stroke="{TAS_K}" stroke-width="{f(k * .8)}" opacity=".7"/>')
    kx = x + w * r.choice([.18, .62])
    out.append(f'<path d="M{f(kx)} {f(y)} V{f(y - zk * .62)} Q{f(kx + w * .1)} {f(y - zk * .9)} {f(kx + w * .2)} {f(y - zk * .62)} V{f(y)} Z" fill="#7A4E2E" stroke="{cizgi}" stroke-width="{f(k)}"/>')
    ux0, ux1, uy0, uy1 = x - ck, x + w + ck, y - h, y - zk
    for bx in (x + w * .08, x + w * .5, x + w * .92):
        out.append(f'<path d="M{f(bx)} {f(uy1 + zk * .28)} L{f(bx + (ck if bx > x + w / 2 else -ck) * .9)} {f(uy1)}" stroke="#6B4A2E" stroke-width="{f(k * 1.6)}"/>')
    out.append(f'<rect x="{f(ux0)}" y="{f(uy0)}" width="{f(ux1 - ux0)}" height="{f(uy1 - uy0)}" fill="{duvar}" stroke="{cizgi}" stroke-width="{f(k)}"/>')
    out.append(f'<path d="M{f(ux0)} {f(uy1 - 2)} H{f(ux1)} M{f(ux0)} {f(uy0 + (uy1 - uy0) * .5)} H{f(ux1)}" stroke="#8A6040" stroke-width="{f(k * 1.3)}" opacity=".55"/>')
    n = max(2, int(w / 60))
    for i in range(n):
        px = ux0 + (ux1 - ux0) * (i + .5) / n
        pw, ph = (ux1 - ux0) / n * .42, (uy1 - uy0) * .52
        out.append(f'<rect x="{f(px - pw / 2)}" y="{f(uy0 + (uy1 - uy0) * .22)}" width="{f(pw)}" height="{f(ph)}" fill="#3E5A6E" stroke="#FFFFFF" stroke-width="{f(k * 1.6)}"/>')
        out.append(f'<path d="M{f(px)} {f(uy0 + (uy1 - uy0) * .22)} v{f(ph)} M{f(px - pw / 2)} {f(uy0 + (uy1 - uy0) * .22 + ph * .45)} h{f(pw)}" stroke="#FFFFFF" stroke-width="{f(k)}"/>')
    if cumba and w > 120:
        cx0, cw = x + w * .34, w * .32
        out.append(f'<rect x="{f(cx0)}" y="{f(uy0 + (uy1 - uy0) * .08)}" width="{f(cw)}" height="{f((uy1 - uy0) * .86)}" fill="{koyu(duvar, .06)}" stroke="{cizgi}" stroke-width="{f(k)}"/>')
        out.append(f'<rect x="{f(cx0 + cw * .14)}" y="{f(uy0 + (uy1 - uy0) * .2)}" width="{f(cw * .72)}" height="{f((uy1 - uy0) * .5)}" fill="#3E5A6E" stroke="#FFFFFF" stroke-width="{f(k * 1.6)}"/>')
        out.append(f'<path d="M{f(cx0 - cw * .06)} {f(uy0 + (uy1 - uy0) * .1)} L{f(cx0 + cw / 2)} {f(uy0 - (uy1 - uy0) * .02)} L{f(cx0 + cw * 1.06)} {f(uy0 + (uy1 - uy0) * .1)} Z" fill="{koyu(cati, .1)}"/>')
    sx = w * .14
    gc = s.lin([(0, acik(cati, .12)), (1, koyu(cati, .22))], 0, uy0 - h * .26, 0, uy0, kull="userSpaceOnUse", ad="ct")
    out.append(f'<path d="M{f(ux0 - sx)} {f(uy0 + h * .02)} L{f(x + w * .2)} {f(uy0 - h * .26)} H{f(x + w * .8)} L{f(ux1 + sx)} {f(uy0 + h * .02)} Z" fill="{gc}" stroke="{cizgi}" stroke-width="{f(k)}" stroke-linejoin="round"/>')
    for i in range(1, 8):
        tx = ux0 - sx + (ux1 - ux0 + 2 * sx) * i / 8
        out.append(f'<path d="M{f(tx)} {f(uy0 + h * .02)} L{f(x + w * .2 + (w * .6) * i / 8)} {f(uy0 - h * .26)}" stroke="{koyu(cati, .35)}" stroke-width="{f(k * .8)}" opacity=".45"/>')
    out.append(f'<rect x="{f(ux0 - sx)}" y="{f(uy0 + h * .015)}" width="{f(ux1 - ux0 + 2 * sx)}" height="{f(h * .025)}" fill="#6B4A2E"/>')
    if r.random() < .7:
        bx = x + w * r.uniform(.25, .7)
        out.append(f'<rect x="{f(bx)}" y="{f(uy0 - h * .36)}" width="{f(w * .07)}" height="{f(h * .16)}" fill="{TAS}" stroke="{cizgi}" stroke-width="{f(k)}"/>')
    gx = x + w * .6 if isik < 0 else x - ck
    out.append(f'<rect x="{f(gx)}" y="{f(uy0)}" width="{f(w * .4 + ck)}" height="{f(h - (uy0 - (y - h)))}" fill="#1B2A55" opacity=".1"/>')
    return "".join(out)


def mini_ev(x, y, w, h, duvar, cati=CATI, isik=-1):
    """Panorama / uzak plan için küçük ev."""
    return (f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{duvar}"/>'
            f'<rect x="{f(x + w * .62)}" y="{f(y - h)}" width="{f(w * .38)}" height="{f(h)}" fill="#1B2A55" opacity=".14"/>'
            f'<path d="M{f(x - w * .12)} {f(y - h)} L{f(x + w * .2)} {f(y - h * 1.5)} H{f(x + w * .8)} L{f(x + w * 1.12)} {f(y - h)} Z" fill="{cati}"/>'
            f'<rect x="{f(x + w * .2)}" y="{f(y - h * .7)}" width="{f(w * .18)}" height="{f(h * .3)}" fill="#3E5A6E"/>'
            f'<rect x="{f(x + w * .55)}" y="{f(y - h * .7)}" width="{f(w * .18)}" height="{f(h * .3)}" fill="#3E5A6E"/>')


def hamam(s, x, y, w, h, tohum=0, isik=-1):
    """Kaplıca binası: almaşık duvar, kurşun kaplı alçak kubbeler ve fil gözü pencereleri, kemerli kapı."""
    out = []
    g = s.lin([(0, "#EAD7B8"), (1, "#CDB28A")], x, 0, x + w, 0, kull="userSpaceOnUse", ad="hm")
    out.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{g}" stroke="#5A4030" stroke-width="3"/>')
    for j in range(1, 6):
        yy = y - h * j / 6
        out.append(f'<rect x="{f(x)}" y="{f(yy - 4)}" width="{f(w)}" height="7" fill="{TUGLA}" opacity=".75"/>')
    for i in range(1, 6):
        out.append(f'<path d="M{f(x + w * i / 6)} {f(y - h)} v{f(h)}" stroke="#B89C74" stroke-width="2" opacity=".5"/>')
    kubbeler = [(x + w * .22, w * .13), (x + w * .5, w * .2), (x + w * .79, w * .14)]
    for (kx, kr) in kubbeler:
        gk = s.rad([(0, "#DCE4EC"), (.6, "#A7B4C2"), (1, "#7C8898")], kx - kr * .35 * -isik * -1, y - h - kr * .55, kr * 1.3, kull="userSpaceOnUse", ad="kb")
        out.append(f'<rect x="{f(kx - kr * 1.05)}" y="{f(y - h - kr * .18)}" width="{f(kr * 2.1)}" height="{f(kr * .2)}" fill="#C9B08A" stroke="#5A4030" stroke-width="2.4"/>')
        out.append(f'<path d="M{f(kx - kr)} {f(y - h - kr * .16)} A{f(kr)} {f(kr * .72)} 0 0 1 {f(kx + kr)} {f(y - h - kr * .16)} Z" fill="{gk}" stroke="#4A5260" stroke-width="2.6"/>')
        for rr, n in ((.45, 6), (.75, 9)):
            for t in range(n):
                a = math.pi * (t + .5) / n
                px = kx - math.cos(a) * kr * rr
                py = y - h - kr * .16 - math.sin(a) * kr * .72 * rr
                out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(kr * .045)}" fill="#F4FBFF" stroke="#6D7A8A" stroke-width="1"/>')
        out.append(f'<path d="M{f(kx)} {f(y - h - kr * .88)} v{f(-kr * .22)}" stroke="#4A5260" stroke-width="3"/><circle cx="{f(kx)}" cy="{f(y - h - kr * 1.12)}" r="4" fill="#C9952B"/>')
    dx = x + w * .5
    out.append(f'<path d="M{f(dx - w * .07)} {f(y)} V{f(y - h * .52)} Q{f(dx)} {f(y - h * .8)} {f(dx + w * .07)} {f(y - h * .52)} V{f(y)} Z" fill="#5A3A26" stroke="#3A2618" stroke-width="3"/>')
    out.append(f'<path d="M{f(dx - w * .09)} {f(y - h * .5)} Q{f(dx)} {f(y - h * .86)} {f(dx + w * .09)} {f(y - h * .5)}" fill="none" stroke="{TUGLA}" stroke-width="7"/>')
    for px in (x + w * .16, x + w * .82):
        out.append(f'<rect x="{f(px - 14)}" y="{f(y - h * .66)}" width="28" height="{f(h * .3)}" rx="12" fill="#3E5A6E" stroke="#FFFFFF" stroke-width="3"/>')
    out.append(f'<rect x="{f(x + w * .6)}" y="{f(y - h)}" width="{f(w * .4)}" height="{f(h)}" fill="#1B2A55" opacity=".12"/>')
    return "".join(out)


def sur(s, x0, x1, y, h, tohum=0, tas="#D6C29E", isik=-1, burc_ara=230, harab=0.0):
    """Bursa ve İznik surları: taş-tuğla almaşık beden duvarı, yarım yuvarlak burçlar, mazgal dişleri."""
    r = RNG(tohum)
    out = []
    g = s.lin([(0, acik(tas, .1)), (1, koyu(tas, .14))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="sr")
    ust = []
    for i in range(int((x1 - x0) / 14) + 1):
        px = x0 + i * 14
        dus = harab * r.uniform(0, h * .35) if r.random() < .5 else 0
        ust.append((px, y - h + dus))
    yol = f"M{f(x0)} {f(y)} " + " ".join(f"L{f(px)} {f(py)}" for px, py in ust) + f" L{f(x1)} {f(y)} Z"
    out.append(f'<path d="{yol}" fill="{g}" stroke="#5A4A36" stroke-width="2.4" stroke-linejoin="round"/>')
    kl = s.klip(f'<path d="{yol}"/>', ad="sk")
    out.append(f'<g clip-path="{kl}">')
    for j in range(1, int(h / 22) + 1):
        out.append(f'<rect x="{f(x0)}" y="{f(y - j * 22)}" width="{f(x1 - x0)}" height="5" fill="{TUGLA}" opacity=".55"/>')
    out.append("</g>")
    if harab < .5:
        for i in range(int((x1 - x0) / 26)):
            px = x0 + i * 26 + 4
            out.append(f'<rect x="{f(px)}" y="{f(y - h - 14)}" width="16" height="16" fill="{koyu(tas, .05)}" stroke="#5A4A36" stroke-width="2"/>')
    bx = x0 + burc_ara * .5
    while bx < x1 - 30:
        bw, bh = h * .62, h * 1.22
        out.append(f'<path d="M{f(bx - bw / 2)} {f(y)} V{f(y - bh)} H{f(bx + bw / 2)} V{f(y)} Z" fill="{g}" stroke="#5A4A36" stroke-width="2.4"/>')
        for j in range(1, int(bh / 22) + 1):
            out.append(f'<rect x="{f(bx - bw / 2)}" y="{f(y - j * 22)}" width="{f(bw)}" height="5" fill="{TUGLA}" opacity=".55"/>')
        for t in range(3):
            out.append(f'<rect x="{f(bx - bw / 2 + t * bw / 3 + 2)}" y="{f(y - bh - 14)}" width="{f(bw / 3 - 7)}" height="15" fill="{koyu(tas, .05)}" stroke="#5A4A36" stroke-width="2"/>')
        out.append(f'<rect x="{f(bx + (bw * .1 if isik < 0 else -bw / 2))}" y="{f(y - bh)}" width="{f(bw * .4)}" height="{f(bh)}" fill="#1B2A55" opacity=".16"/>')
        out.append(f'<rect x="{f(bx - 4)}" y="{f(y - bh * .62)}" width="8" height="18" rx="3" fill="#2E2A30"/>')
        bx += burc_ara * r.uniform(.85, 1.15)
    return "".join(out)


def saat_kulesi(s, x, y, h, tohum=0, isik=-1, bayrak=True, isikli=False):
    """Tophane Saat Kulesi (temsilî): kare taş gövde, kat silmeleri, saat kadranı, küçük çatı ve bayrak direği."""
    w = h * .2
    out = []
    g = s.lin([(0, "#F0E2C6"), (1, "#C8AE86")], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="sq")
    out.append(f'<rect x="{f(x - w * .62)}" y="{f(y - h * .06)}" width="{f(w * 1.24)}" height="{f(h * .06)}" fill="#BFA47E" stroke="#4A3A2A" stroke-width="2.4"/>')
    out.append(f'<rect x="{f(x - w / 2)}" y="{f(y - h * .82)}" width="{f(w)}" height="{f(h * .76)}" fill="{g}" stroke="#4A3A2A" stroke-width="2.4"/>')
    for j in range(1, 5):
        yy = y - h * .06 - h * .76 * j / 5
        out.append(f'<rect x="{f(x - w * .56)}" y="{f(yy - 3)}" width="{f(w * 1.12)}" height="7" fill="#E8D6B4" stroke="#4A3A2A" stroke-width="1.6"/>')
        pen = "#FFD27A" if isikli else "#3E5A6E"
        out.append(f'<rect x="{f(x - w * .12)}" y="{f(yy + h * .03)}" width="{f(w * .24)}" height="{f(h * .08)}" rx="{f(w * .1)}" fill="{pen}" stroke="#4A3A2A" stroke-width="1.6"/>')
    cy = y - h * .74
    out.append(f'<circle cx="{f(x)}" cy="{f(cy)}" r="{f(w * .3)}" fill="#FFFDF7" stroke="#1B1D26" stroke-width="2.6"/>')
    out.append(f'<path d="M{f(x)} {f(cy)} v{f(-w * .2)} M{f(x)} {f(cy)} l{f(w * .14)} {f(w * .06)}" stroke="#1B1D26" stroke-width="2.6" stroke-linecap="round"/>')
    out.append(f'<rect x="{f(x - w * .58)}" y="{f(y - h * .86)}" width="{f(w * 1.16)}" height="{f(h * .04)}" fill="#E8D6B4" stroke="#4A3A2A" stroke-width="2"/>')
    out.append(f'<rect x="{f(x - w * .4)}" y="{f(y - h * .95)}" width="{f(w * .8)}" height="{f(h * .09)}" fill="#F0E2C6" stroke="#4A3A2A" stroke-width="2"/>')
    out.append(f'<path d="M{f(x - w * .2)} {f(y - h * .87)} v{f(-h * .05)} a{f(w * .07)} {f(w * .07)} 0 0 1 {f(w * .14)} 0 v{f(h * .05)} Z M{f(x + w * .06)} {f(y - h * .87)} v{f(-h * .05)} a{f(w * .07)} {f(w * .07)} 0 0 1 {f(w * .14)} 0 v{f(h * .05)} Z" fill="{"#FFD27A" if isikli else "#3E5A6E"}"/>')
    out.append(f'<path d="M{f(x - w * .5)} {f(y - h * .95)} L{f(x)} {f(y - h * 1.08)} L{f(x + w * .5)} {f(y - h * .95)} Z" fill="#6E7A86" stroke="#2A2E36" stroke-width="2"/>')
    out.append(f'<rect x="{f(x + (w * .05 if isik < 0 else -w / 2))}" y="{f(y - h * .82)}" width="{f(w * .45)}" height="{f(h * .76)}" fill="#1B2A55" opacity=".12"/>')
    tepe = (x, y - h * 1.08)
    if bayrak:
        out.append(f'<path d="M{f(x)} {f(y - h * 1.08)} v{f(-h * .22)}" stroke="#2A2E36" stroke-width="3"/>')
        bx, by = x + 2, y - h * 1.3
        out.append(f'<path d="M{f(bx)} {f(by)} h{f(h * .17)} v{f(h * .11)} h{f(-h * .17)} Z" fill="#E30A17"/>'
                   f'<circle cx="{f(bx + h * .062)}" cy="{f(by + h * .055)}" r="{f(h * .029)}" fill="#FFFFFF"/>'
                   f'<circle cx="{f(bx + h * .07)}" cy="{f(by + h * .055)}" r="{f(h * .023)}" fill="#E30A17"/>'
                   f'<path d="{cizgi_d(yildiz_noktalari(bx + h * .107, by + h * .055, h * .016, h * .0065, 5, math.pi), True)}" fill="#FFFFFF"/>')
    return "".join(out), tepe


def han_cephe(s, x0, x1, y_ust, y_alt, tohum=0, aralik=170):
    """Koza Han avlu cephesi: iki katlı revak (sivri kemerler), taş-tuğla almaşık duvar, kiremit saçak ve sıra bacalar."""
    r = RNG(tohum)
    out = []
    hgt = y_alt - y_ust
    out.append(f'<rect x="{f(x0)}" y="{f(y_ust)}" width="{f(x1 - x0)}" height="{f(hgt)}" fill="{TUGLA}"/>')
    for j in range(int(hgt / 30) + 1):
        out.append(f'<rect x="{f(x0)}" y="{f(y_ust + j * 30)}" width="{f(x1 - x0)}" height="13" fill="#EAD7B8"/>')
        out.append(f'<path d="M{f(x0)} {f(y_ust + j * 30 + 13)} H{f(x1)}" stroke="#7E3A26" stroke-width="1.6" opacity=".6"/>')
    orta = y_ust + hgt * .47
    out.append(f'<rect x="{f(x0)}" y="{f(orta - 8)}" width="{f(x1 - x0)}" height="16" fill="#D9C3A0" stroke="#5A3A26" stroke-width="2"/>')
    for (ky0, ky1, oran) in ((y_ust + hgt * .1, orta - 8, .62), (orta + 8, y_alt, .74)):
        n = int((x1 - x0) / aralik)
        for i in range(n + 1):
            cx_ = x0 + aralik * (i + .5)
            kw = aralik * oran
            ust = ky0 + (ky1 - ky0) * .12
            yol = (f"M{f(cx_ - kw / 2)} {f(ky1)} V{f(ust + kw * .45)} Q{f(cx_ - kw / 2)} {f(ust)} {f(cx_)} {f(ust - kw * .12)} "
                   f"Q{f(cx_ + kw / 2)} {f(ust)} {f(cx_ + kw / 2)} {f(ust + kw * .45)} V{f(ky1)} Z")
            gi = s.lin([(0, "#3A2218"), (1, "#7A4A30")], 0, ust, 0, ky1, kull="userSpaceOnUse", ad="kmr")
            out.append(f'<path d="{yol}" fill="{gi}" stroke="#EAD7B8" stroke-width="{f(aralik * .06)}"/>')
            out.append(f'<path d="{yol}" fill="none" stroke="#5A3A26" stroke-width="2"/>')
    out.append(f'<path d="M{f(x0)} {f(y_ust)} H{f(x1)} L{f(x1 + 30)} {f(y_ust - 26)} H{f(x0 - 30)} Z" fill="{CATI}" stroke="#5A3A26" stroke-width="2.4"/>')
    for i in range(int((x1 - x0) / 120) + 1):
        bx = x0 + 60 + i * 120 + r.uniform(-8, 8)
        out.append(f'<path d="M{f(bx - 9)} {f(y_ust - 24)} L{f(bx - 6)} {f(y_ust - 66)} H{f(bx + 6)} L{f(bx + 9)} {f(y_ust - 24)} Z" fill="#E6D2B0" stroke="#5A3A26" stroke-width="2"/>')
        out.append(f'<path d="M{f(bx - 10)} {f(y_ust - 66)} L{f(bx)} {f(y_ust - 80)} L{f(bx + 10)} {f(y_ust - 66)} Z" fill="#8C96A2" stroke="#5A3A26" stroke-width="1.6"/>')
    return "".join(out)


def esarp_ipi(x0, y0, x1, y1, n, tohum=0, sark=40, boy=(70, 110), renkler=IPEK):
    """İpe asılı ipek eşarplar (sarkan ip + saçaklı dikdörtgenler)."""
    r = RNG(tohum)
    mx, my = (x0 + x1) / 2, max(y0, y1) + sark
    out = [f'<path d="M{f(x0)} {f(y0)} Q{f(mx)} {f(my + sark * .6)} {f(x1)} {f(y1)}" stroke="#5A3A26" stroke-width="3" fill="none"/>']
    for i in range(n):
        t = (i + .5) / n
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (my + sark * .6) + t * t * y1
        w = (x1 - x0) / n * .78
        hh = r.uniform(*boy)
        c = renkler[(i + tohum) % len(renkler)]
        egim = r.uniform(-6, 6)
        out.append(f'<g transform="rotate({f(egim)} {f(px)} {f(py)})">'
                   f'<path d="M{f(px - w / 2)} {f(py)} H{f(px + w / 2)} L{f(px + w / 2 + 4)} {f(py + hh)} H{f(px - w / 2 - 4)} Z" fill="{c}" stroke="#2A2030" stroke-width="1.6"/>'
                   f'<path d="M{f(px - w / 2)} {f(py + hh * .18)} H{f(px + w / 2)} M{f(px - w / 2 - 2)} {f(py + hh * .8)} H{f(px + w / 2 + 2)}" stroke="{acik(c, .55)}" stroke-width="{f(w * .07)}"/>'
                   f'<path d="M{f(px - w * .2)} {f(py + hh * .45)} l{f(w * .2)} {f(-hh * .1)} l{f(w * .2)} {f(hh * .1)} l{f(-w * .2)} {f(hh * .1)} Z" fill="{acik(c, .4)}"/>'
                   + "".join(f'<path d="M{f(px - w / 2 - 3 + k * (w + 6) / 6)} {f(py + hh)} v9" stroke="{c}" stroke-width="2"/>' for k in range(7))
                   + "</g>")
    return "".join(out)


def koza_cuvali(x, y, w, tohum=0):
    """Ağzı açık çuval, içinde beyaz–krem ipek kozaları."""
    r = RNG(tohum)
    h = w * .9
    out = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .55)}" ry="{f(w * .08)}" fill="#000" opacity=".18"/>',
           f'<path d="M{f(x - w * .42)} {f(y - h * .78)} C{f(x - w * .6)} {f(y - h * .4)} {f(x - w * .56)} {f(y)} {f(x)} {f(y)} C{f(x + w * .56)} {f(y)} {f(x + w * .6)} {f(y - h * .4)} {f(x + w * .42)} {f(y - h * .78)} Z" fill="#C9A46E" stroke="#5A4030" stroke-width="2.4"/>',
           f'<path d="M{f(x - w * .3)} {f(y - h * .6)} q{f(w * .1)} {f(h * .3)} 0 {f(h * .55)} M{f(x + w * .2)} {f(y - h * .65)} q{f(w * .1)} {f(h * .3)} {f(w * .02)} {f(h * .6)}" stroke="#A9864E" stroke-width="2" fill="none"/>',
           f'<ellipse cx="{f(x)}" cy="{f(y - h * .78)}" rx="{f(w * .44)}" ry="{f(w * .12)}" fill="#8C6A3E" stroke="#5A4030" stroke-width="2.4"/>']
    for k in range(int(w / 6)):
        px = x + r.uniform(-w * .36, w * .36)
        py = y - h * .78 - r.uniform(-w * .05, w * .2) * (1 - abs(px - x) / (w * .4))
        a = r.uniform(0, 180)
        out.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(w * .07)}" ry="{f(w * .045)}" fill="{r.choice(["#FFFDF2", "#FFF6DA", "#F6EED8"])}" stroke="#B8A780" stroke-width="1.2" transform="rotate({f(a)} {f(px)} {f(py)})"/>')
    return "".join(out)


def boya_kazani(s, x, y, w, renk="#B8202E", tohum=0):
    """Bakır boya kazanı (kök boya banyosu) + karıştırma çubuğu + buhar."""
    g = s.lin([(0, "#E9A36A"), (.5, "#C46A35"), (1, "#7A3A1C")], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="bk")
    h = w * .6
    out = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .55)}" ry="{f(w * .07)}" fill="#000" opacity=".2"/>',
           f'<path d="M{f(x - w / 2)} {f(y - h)} C{f(x - w / 2)} {f(y - h * .1)} {f(x - w * .3)} {f(y)} {f(x)} {f(y)} C{f(x + w * .3)} {f(y)} {f(x + w / 2)} {f(y - h * .1)} {f(x + w / 2)} {f(y - h)} Z" fill="{g}" stroke="#4A2412" stroke-width="2.6"/>',
           f'<ellipse cx="{f(x)}" cy="{f(y - h)}" rx="{f(w / 2)}" ry="{f(w * .1)}" fill="{renk}" stroke="#4A2412" stroke-width="2.6"/>',
           f'<ellipse cx="{f(x - w * .12)}" cy="{f(y - h - w * .02)}" rx="{f(w * .14)}" ry="{f(w * .025)}" fill="{acik(renk, .35)}"/>',
           f'<path d="M{f(x + w * .08)} {f(y - h)} L{f(x + w * .34)} {f(y - h - w * .5)}" stroke="#8A6A44" stroke-width="{f(w * .05)}" stroke-linecap="round"/>']
    for px in (x - w * .52, x + w * .52):
        out.append(f'<path d="M{f(px)} {f(y - h * .8)} a{f(w * .06)} {f(w * .06)} 0 0 {1 if px > x else 0} 0 {f(w * .14)}" stroke="#4A2412" stroke-width="3" fill="none"/>')
    out.append(buhar(s, x - w * .1, y - h - w * .05, w * .9, tohum, w * .22, .6))
    return "".join(out)


def cile_diregi(x, y, h, renkler=("#B8202E", "#F0B43A", "#1D3A8A", "#1F8A5B", "#7B3F8C")):
    """Boyanmış iplik çileleri asılı sırık (kök boya, cehri, çivit…)."""
    w = len(renkler) * 46
    out = [f'<path d="M{f(x)} {f(y)} V{f(y - h)} M{f(x + w)} {f(y)} V{f(y - h)}" stroke="#6B4A2E" stroke-width="7"/>',
           f'<path d="M{f(x - 8)} {f(y - h + 6)} H{f(x + w + 8)}" stroke="#8A6040" stroke-width="9" stroke-linecap="round"/>']
    for i, c in enumerate(renkler):
        cx_ = x + 23 + i * 46
        top = y - h + 10
        out.append(f'<path d="M{f(cx_ - 15)} {f(top)} C{f(cx_ - 20)} {f(top + h * .3)} {f(cx_ - 12)} {f(top + h * .55)} {f(cx_)} {f(top + h * .58)} '
                   f'C{f(cx_ + 12)} {f(top + h * .55)} {f(cx_ + 20)} {f(top + h * .3)} {f(cx_ + 15)} {f(top)} Z" fill="{c}" stroke="#2A2030" stroke-width="1.6"/>')
        for k in (-8, 0, 8):
            out.append(f'<path d="M{f(cx_ + k)} {f(top + 4)} C{f(cx_ + k * 1.3)} {f(top + h * .25)} {f(cx_ + k * .8)} {f(top + h * .45)} {f(cx_ + k * .2)} {f(top + h * .54)}" stroke="{acik(c, .35)}" stroke-width="2" fill="none"/>')
    return "".join(out)


def mangal(s, x, y, w, tohum=0, paket=3):
    """Mangal: ayaklı kutu, kor, ızgara teli, folyo paketleri ve duman."""
    h = w * .32
    out = [f'<path d="M{f(x - w * .4)} {f(y)} L{f(x - w * .34)} {f(y - h)} M{f(x + w * .4)} {f(y)} L{f(x + w * .34)} {f(y - h)}" stroke="#2A2E36" stroke-width="5"/>',
           f'<path d="M{f(x - w / 2)} {f(y - h)} H{f(x + w / 2)} L{f(x + w * .44)} {f(y - h * 1.8)} H{f(x - w * .44)} Z" fill="#3A3F4B" stroke="#1B1D26" stroke-width="2.6"/>']
    g = s.rad([(0, "#FFE08A"), (.5, "#FF7A3D"), (1, "#B8202E")], x, y - h * 1.8, w * .5, kull="userSpaceOnUse", ad="kor")
    out.append(f'<rect x="{f(x - w * .43)}" y="{f(y - h * 1.95)}" width="{f(w * .86)}" height="{f(h * .2)}" rx="4" fill="{g}"/>')
    for i in range(12):
        out.append(f'<path d="M{f(x - w * .44 + i * w * .08)} {f(y - h * 2.0)} v{f(-4)}" stroke="#8C96A2" stroke-width="2"/>')
    out.append(f'<path d="M{f(x - w * .46)} {f(y - h * 2.02)} H{f(x + w * .46)}" stroke="#8C96A2" stroke-width="3"/>')
    gf = s.lin([(0, "#FFFFFF"), (.5, "#C9D2DC"), (1, "#8E9AA8")], 0, y - h * 2.6, 0, y - h * 2, kull="userSpaceOnUse", ad="fl")
    for i in range(paket):
        px = x - w * .3 + i * w * .3
        out.append(f'<path d="M{f(px - w * .12)} {f(y - h * 2.03)} Q{f(px - w * .13)} {f(y - h * 2.45)} {f(px)} {f(y - h * 2.5)} Q{f(px + w * .13)} {f(y - h * 2.45)} {f(px + w * .12)} {f(y - h * 2.03)} Z" fill="{gf}" stroke="#5A6470" stroke-width="2"/>')
        out.append(f'<path d="M{f(px - w * .05)} {f(y - h * 2.48)} q{f(w * .05)} {f(-h * .25)} {f(w * .1)} 0" stroke="#5A6470" stroke-width="2" fill="#E9EEF2"/>')
        out.append(f'<path d="M{f(px - w * .07)} {f(y - h * 2.2)} l{f(w * .04)} {f(-h * .1)} l{f(w * .03)} {f(h * .08)}" stroke="#FFFFFF" stroke-width="2" fill="none"/>')
    out.append(buhar(s, x + w * .05, y - h * 2.5, w * 1.3, tohum, w * .2, .55))
    return "".join(out)


def piknik_masasi(x, y, w, tohum=0):
    """Kareli örtülü ahşap piknik masası; üstünde ekmek, domates, limon, ayran."""
    h = w * .3
    out = [f'<path d="M{f(x + w * .12)} {f(y)} L{f(x + w * .2)} {f(y - h)} M{f(x + w * .88)} {f(y)} L{f(x + w * .8)} {f(y - h)}" stroke="#6B4A2E" stroke-width="8"/>',
           f'<rect x="{f(x - w * .06)}" y="{f(y - h * .45)}" width="{f(w * 1.12)}" height="9" rx="3" fill="#8A6040"/>',
           f'<path d="M{f(x)} {f(y - h)} H{f(x + w)} L{f(x + w * .96)} {f(y - h * .78)} H{f(x + w * .04)} Z" fill="#FFFFFF" stroke="#5A3A26" stroke-width="2"/>']
    n = 10
    for i in range(n):
        if i % 2 == 0:
            out.append(f'<path d="M{f(x + w * i / n)} {f(y - h)} h{f(w / n)} l{f(-w * .004)} {f(h * .22)} h{f(-w / n)} Z" fill="#D7263D" opacity=".85"/>')
    out.append(f'<path d="M{f(x)} {f(y - h)} H{f(x + w)}" stroke="#D7263D" stroke-width="3"/>')
    tx = x + w * .15
    out.append(f'<ellipse cx="{f(tx)}" cy="{f(y - h - 8)}" rx="{f(w * .09)}" ry="{f(w * .04)}" fill="#E8B46A" stroke="#7A4A20" stroke-width="2"/>')
    out.append(f'<circle cx="{f(x + w * .36)}" cy="{f(y - h - 12)}" r="{f(w * .045)}" fill="{MERCAN}" stroke="#7A1C10" stroke-width="2"/><path d="M{f(x + w * .36)} {f(y - h - 12 - w * .045)} l-5 -6 m5 6 l5 -6" stroke="#2F7A36" stroke-width="3"/>')
    out.append(f'<ellipse cx="{f(x + w * .5)}" cy="{f(y - h - 9)}" rx="{f(w * .04)}" ry="{f(w * .028)}" fill="#F2D23A" stroke="#8A7010" stroke-width="2"/>')
    for k, cx_ in enumerate((x + w * .66, x + w * .78)):
        out.append(f'<path d="M{f(cx_ - 11)} {f(y - h - 40)} L{f(cx_ - 8)} {f(y - h - 2)} H{f(cx_ + 8)} L{f(cx_ + 11)} {f(y - h - 40)} Z" fill="#FFFFFF" stroke="#5A6470" stroke-width="2"/>')
    out.append(f'<rect x="{f(x + w * .86)}" y="{f(y - h - 30)}" width="{f(w * .08)}" height="28" rx="4" fill="#C9D2DC" stroke="#5A6470" stroke-width="2"/>')
    return "".join(out)


def kabin(x, y, o=1.0, renk="#E2533D", pamuk=False):
    """Teleferik kabini (askı kolu kabloya değer: (x, y) kablo noktası)."""
    g = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">',
         '<circle cx="0" cy="0" r="6" fill="#2A2E36"/><path d="M0 0 V34" stroke="#2A2E36" stroke-width="5"/>',
         f'<path d="M-34 34 H34 Q42 34 42 44 V86 Q42 98 30 98 H-30 Q-42 98 -42 86 V44 Q-42 34 -34 34 Z" fill="{renk}" stroke="#1B1D26" stroke-width="3"/>',
         '<rect x="-34" y="44" width="68" height="28" rx="6" fill="#BFE6F2" stroke="#1B1D26" stroke-width="2.4"/>',
         '<path d="M-12 44 V72 M12 44 V72" stroke="#1B1D26" stroke-width="2"/>',
         f'<path d="M-42 84 H42" stroke="{acik(renk, .4)}" stroke-width="5"/>']
    if pamuk:
        g.append('<use href="#pamuk-bas-gulen" x="-25" y="44" width="30" height="29"/>')
    g.append("</g>")
    return "".join(g)


def leylek(x, y, o=1.0, ucan=True, yon=1):
    """Leylek: beyaz gövde, siyah kanat uçları, kırmızı gaga ve bacaklar."""
    if ucan:
        return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o * yon, 3)} {f(o, 3)})">'
                '<path d="M-60 -6 C-40 -26 -16 -16 0 -4 C16 -16 40 -26 60 -6 C40 -10 18 -2 0 6 C-18 -2 -40 -10 -60 -6 Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
                '<path d="M-60 -6 C-50 -14 -40 -16 -32 -14 L-36 -6 Z M60 -6 C50 -14 40 -16 32 -14 L36 -6 Z" fill="#1B1D26"/>'
                '<ellipse cx="0" cy="2" rx="16" ry="6" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
                '<path d="M14 0 L34 -2" stroke="#FFFFFF" stroke-width="4"/><path d="M34 -2 L48 0" stroke="#E2533D" stroke-width="3"/>'
                '<path d="M-14 4 L-40 8" stroke="#E2533D" stroke-width="2.4"/></g>')
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o * yon, 3)} {f(o, 3)})">'
            '<path d="M-4 0 L-6 30 M6 0 L4 30" stroke="#E2533D" stroke-width="3"/>'
            '<ellipse cx="0" cy="-10" rx="14" ry="20" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
            '<path d="M6 -24 C14 -12 14 0 4 8 L-2 -8 Z" fill="#1B1D26"/>'
            '<path d="M-2 -28 C-4 -40 4 -46 8 -50" stroke="#FFFFFF" stroke-width="7" fill="none"/>'
            '<path d="M8 -50 L28 -44" stroke="#E2533D" stroke-width="3.4"/></g>')


def zeytin(s, x, y, r0, tohum=0):
    """Zeytin ağacı: kıvrık gri gövde, gümüşi yeşil yaprak kümeleri."""
    r = RNG(tohum)
    out = [f'<path d="M{f(x - r0 * .18)} {f(y)} C{f(x - r0 * .3)} {f(y - r0 * .5)} {f(x + r0 * .2)} {f(y - r0 * .7)} {f(x - r0 * .05)} {f(y - r0 * 1.2)} '
           f'L{f(x + r0 * .1)} {f(y - r0 * 1.2)} C{f(x + r0 * .35)} {f(y - r0 * .7)} {f(x + r0 * .05)} {f(y - r0 * .45)} {f(x + r0 * .2)} {f(y)} Z" fill="#7A6A58" stroke="#4A3E30" stroke-width="2"/>']
    for i in range(9):
        a = r.uniform(math.pi * 1.05, math.pi * 1.95)
        d = r0 * r.uniform(.25, .7)
        cx_, cy_ = x + math.cos(a) * d * 1.3, y - r0 * 1.35 + math.sin(a) * d * .55
        rr = r0 * r.uniform(.32, .45)
        out.append(f'<ellipse cx="{f(cx_)}" cy="{f(cy_)}" rx="{f(rr * 1.2)}" ry="{f(rr * .8)}" fill="{r.choice(["#7C8F4E", "#6E8445", "#8FA060"])}"/>')
        out.append(f'<ellipse cx="{f(cx_ - rr * .3)}" cy="{f(cy_ - rr * .3)}" rx="{f(rr * .6)}" ry="{f(rr * .35)}" fill="#B9C79A" opacity=".55"/>')
    return "".join(out)


def kahvalti_masasi(s, x, y, w, tohum=0):
    """Köy kahvaltısı: beyaz örtü, semaver, çay bardakları, peynir, zeytin, domates, pekmez–tahin."""
    h = w * .26
    out = [f'<path d="M{f(x + w * .1)} {f(y)} V{f(y - h)} M{f(x + w * .9)} {f(y)} V{f(y - h)}" stroke="#6B4A2E" stroke-width="7"/>',
           f'<path d="M{f(x - w * .03)} {f(y - h)} H{f(x + w * 1.03)} L{f(x + w)} {f(y - h * .62)} H{f(x)} Z" fill="#FFFDF7" stroke="#5A3A26" stroke-width="2"/>',
           f'<path d="M{f(x)} {f(y - h * .66)} H{f(x + w)}" stroke="{KOBALT}" stroke-width="5"/>']
    out.append(Y.semaver(s, x + w * .12, y - h, w * .3))
    yt = y - h - 2
    out.append(Y.cay_bardak_kucuk(x + w * .3, yt, w * .07))
    out.append(Y.cay_bardak_kucuk(x + w * .37, yt, w * .07))
    for (px, rx, renk, ic) in ((x + w * .5, w * .07, "#FFFFFF", "#FFF6DA"), (x + w * .66, w * .065, "#FFFFFF", "#3A4A2A"),
                               (x + w * .82, w * .07, "#FFFFFF", MERCAN)):
        out.append(f'<ellipse cx="{f(px)}" cy="{f(yt)}" rx="{f(rx)}" ry="{f(rx * .32)}" fill="{renk}" stroke="#5A6470" stroke-width="2"/>')
        if ic == "#FFF6DA":
            out.append(f'<rect x="{f(px - rx * .5)}" y="{f(yt - rx * .42)}" width="{f(rx)}" height="{f(rx * .38)}" rx="3" fill="{ic}" stroke="#B8A780" stroke-width="1.4"/>')
        elif ic == MERCAN:
            for k in (-1, 0, 1):
                out.append(f'<circle cx="{f(px + k * rx * .4)}" cy="{f(yt - rx * .18)}" r="{f(rx * .24)}" fill="{MERCAN}" stroke="#7A1C10" stroke-width="1.2"/>')
        else:
            for k in range(5):
                out.append(f'<ellipse cx="{f(px - rx * .45 + k * rx * .22)}" cy="{f(yt - rx * .14 - (k % 2) * 3)}" rx="{f(rx * .12)}" ry="{f(rx * .09)}" fill="{ic}"/>')
    px = x + w * .94
    out.append(f'<path d="M{f(px - w * .045)} {f(yt - w * .05)} Q{f(px)} {f(yt + 4)} {f(px + w * .045)} {f(yt - w * .05)} Z" fill="#FFFFFF" stroke="#5A6470" stroke-width="2"/>'
               f'<ellipse cx="{f(px)}" cy="{f(yt - w * .05)}" rx="{f(w * .045)}" ry="{f(w * .012)}" fill="#4A1E12"/>'
               f'<path d="M{f(px - w * .02)} {f(yt - w * .052)} q{f(w * .02)} {f(-w * .006)} {f(w * .035)} 0" stroke="#E8C68A" stroke-width="3" fill="none"/>')
    return "".join(out)


def _ova(s, ufuk, renk1="#B9CF6A", renk2="#5F9442", h=H, ad="ova"):
    g = s.lin([(0, renk1), (1, renk2)], 0, ufuk, 0, h, kull="userSpaceOnUse", ad=ad)
    return f'<path d="M0 {f(ufuk + 8)} C500 {f(ufuk)} 1200 {f(ufuk + 20)} 2100 {f(ufuk + 6)} V{f(h)} H0 Z" fill="{g}"/>'


def _orman(s, x0, x1, y, n, tohum, boy=(40, 70), renk=GOKNAR, golge=GOKNAR_K, op=1.0, egim=0.0):
    r = RNG(tohum)
    out = []
    xs = sorted(r.uniform(x0, x1) for _ in range(n))
    for i, x in enumerate(xs):
        yy = y + egim * (x - x0) + r.uniform(-6, 6)
        out.append(goknar(x, yy, r.uniform(*boy), tohum * 100 + i, renk=renk, golge=golge, op=op))
    return "".join(out)


# ================================================================== 1. DURAK · İZNİK ÇİNİ ATÖLYESİ (sabah)

def iznik():
    s = Svg("iz-izn")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3E5FB8"), (.38, "#8FA6E0"), (.7, "#FFCFA8"), (1, "#FFEBD0")])
    s += _zemin(s, ufuk, "#E8D2B0")
    s += S.gunes(s, 360, 214, 40, cekirdek="#FFF6E0", hale="#FFC27A", hale_r=560, guc=.95)
    for (x, y, w_, k) in ((640, 110, 520, 10), (1220, 70, 600, 12), (1720, 150, 380, 8)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFE9E6", "#F2B8C0", .55)
    d, _ = S.dag(s, -80, 1280, ufuk + 4, 560, 150, 11, renk="#8F93C8", golge="#6C70A8", bicim="tepe", sis="#F6CDC4", isik=-1, sirt=2, puruz=6)
    s += d
    d, _ = S.dag(s, 900, 2240, ufuk + 4, 1620, 168, 12, renk="#8088C0", golge="#5F6699", bicim="tepe", sis="#F6CDC4", isik=-1, sirt=3, puruz=7)
    s += d
    s += S.gol(s, 0, ufuk, W, 92, 13, ufuk="#FFDDBE", orta="#5DB7C6", derin="#1E7E96", gunes_x=360)
    s += f'<path d="M0 {ufuk + 1} H{W}" stroke="#5A5C92" stroke-width="4" opacity=".55"/>'
    for k, (x, y, o) in enumerate(((620, 190, 1.1), (690, 214, .8), (980, 160, .7))):
        s += S.marti(x, y, o, 2 - k, renk="#3A3560")
    # sağ kıyı: İznik surları ve kapısı (temsilî)
    gz = s.lin([(0, "#D9C49A"), (1, "#B79B6A")], 0, 300, 0, H, kull="userSpaceOnUse", ad="kiyi")
    s += f'<path d="M1060 {H} C1100 360 1180 336 1300 330 C1600 318 1900 300 2140 296 V{H} Z" fill="{gz}"/>'
    s += serv(s, 1215, 336, 120, 14) + serv(s, 1246, 334, 140, 15)
    s += sur(s, 1290, 1720, 334, 56, 16, tas="#DCC7A0", harab=.6, burc_ara=170)
    kx = 1500
    s += (f'<path d="M{kx - 46} 334 V284 H{kx + 46} V334 Z" fill="#CDB68C" stroke="#5A4A36" stroke-width="2.4"/>'
          f'<path d="M{kx - 26} 334 V306 Q{kx} 280 {kx + 26} 306 V334 Z" fill="#3A2C22"/>'
          f'<path d="M{kx - 30} 306 Q{kx} 274 {kx + 30} 306" stroke="{TUGLA}" stroke-width="6" fill="none"/>')
    s += S.agac(s, 1760, 334, 46, 17, renk="#5E9E48", meyve=None)
    # çini atölyesi: sundurma, çini pano, fırın
    s += f'<path d="M1540 252 L2140 228 L2140 252 L1540 276 Z" fill="{CATI}" stroke="#5A3A26" stroke-width="3"/>'
    for i in range(1, 12):
        tx = 1540 + i * 55
        s += f'<path d="M{tx} {276 - i * 2.2} L{tx + 6} {252 - i * 2.2}" stroke="#7E2E1C" stroke-width="2" opacity=".6"/>'
    gd = s.lin([(0, "#F6EAD6"), (1, "#E6D2B2")], 0, 270, 0, 430, kull="userSpaceOnUse", ad="atd")
    s += f'<rect x="1560" y="268" width="560" height="166" fill="{gd}"/>'
    s += cini_pano(1604, 290, 4, 2, 52)
    s += f'<rect x="1600" y="400" width="216" height="10" fill="#8A6040"/>'
    for px in (1556, 1836, 2096):
        s += f'<rect x="{px - 8}" y="262" width="16" height="190" fill="#7A5236" stroke="#4A2E1C" stroke-width="2"/>'
    gf = s.rad([(0, "#FFE9A0"), (.45, "#FF9A3D"), (1, "#B8402A")], .5, .8, .7, ad="frn")
    s += (f'<path d="M1880 440 V350 Q1880 296 1960 292 Q2040 296 2040 350 V440 Z" fill="#C9A47A" stroke="#5A3A26" stroke-width="3"/>'
          f'<path d="M1924 440 V392 Q1960 360 1996 392 V440 Z" fill="{gf}" stroke="#5A3A26" stroke-width="3"/>'
          f'<path d="M1900 330 h120 M1890 360 h140 M1886 400 h36 M1998 400 h40" stroke="#A9864E" stroke-width="3"/>'
          f'<rect x="1950" y="250" width="22" height="46" fill="#B89470" stroke="#5A3A26" stroke-width="2"/>')
    s += buhar(s, 1961, 246, 120, 18, 28, .45)
    s += f'<path d="M1060 {H} C1300 438 1700 436 2140 432 V{H} Z" fill="#CFAF82"/>'
    # tezgâh: pigment kâseleri ve fırçalar
    s += f'<rect x="1340" y="392" width="230" height="16" rx="4" fill="#9A6B42" stroke="#5A3A26" stroke-width="2.4"/>'
    s += f'<path d="M1356 408 V452 M1554 408 V452" stroke="#6B4A2E" stroke-width="9"/>'
    for i, c in enumerate((KOBALT, TURKUAZ, MERCAN, CINI_YESIL)):
        px = 1372 + i * 50
        s += (f'<path d="M{px - 20} 392 Q{px} 418 {px + 20} 392 Z" fill="#FFFFFF" stroke="#5A6470" stroke-width="2"/>'
              f'<ellipse cx="{px}" cy="392" rx="20" ry="5" fill="{c}" stroke="#5A6470" stroke-width="1.6"/>')
    s += f'<path d="M1556 388 L1590 354 M1562 390 L1600 362" stroke="#8A6040" stroke-width="4"/><path d="M1590 354 l6 -7 M1600 362 l7 -6" stroke="#1B1D26" stroke-width="5" stroke-linecap="round"/>'
    s += cini_vazo(s, 1705, 452, 150, 19)
    s += '<use href="#pamuk-dusunen" x="1772" y="356" width="84" height="96"/>'
    s += S.cimen(1060, 2100, 456, 20, renk="#7E9A48", renk2="#A9C068", boy=10, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 2. DURAK · ÇEKİRGE KAPLICALARI (öğle)

def cekirge():
    s = Svg("iz-cek")
    ufuk = 296
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2F8FD8"), (.5, "#86C8EE"), (1, "#E4F5FB")])
    s += _zemin(s, ufuk, "#7DB45A")
    s += S.gunes(s, 300, 74, 30, hale="#FFF2C2", hale_r=300, guc=.75)
    for i, (x, y, w_) in enumerate(((620, 120, 220), (980, 70, 280), (1980, 120, 200))):
        s += S.bulut(s, x, y, w_, 30 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    d, _ = S.dag(s, 760, 2340, ufuk + 6, 1640, 34, 31, renk="#8396C2", golge="#5C6FA0", bicim="sivri", kar_y=130, kar="#FFFFFF",
                 kar_golge="#C6D4EE", sis="#C8E4F2", isik=-1, sirt=7, puruz=12, kenar_isik="#F4F9FF")
    s += d
    d, _ = S.dag(s, -120, 1100, ufuk + 6, 420, 170, 32, renk="#9DB8D2", golge="#7C9CBE", bicim="tepe", sis="#D8EEF6", isik=-1, sirt=2, puruz=6)
    s += d
    tb, _ = S.tepe_bandi(s, 600, 2140, ufuk - 10, 50, 33, "#5E9E4E", "#3F7F3E", dalga=4)
    s += tb
    s += _orman(s, 980, 2100, ufuk - 30, 34, 34, boy=(26, 42), op=.9)
    s += _ova(s, ufuk, "#A9CF6A", "#5F9442")
    # Çekirge yamacı: evler ve selviler
    r = RNG(35)
    for k in range(9):
        x = 1240 + k * 92 + r.uniform(-10, 10)
        yy = 330 - (k % 3) * 14
        s += mini_ev(x, yy, 58, 34, r.choice(["#F6EEDC", "#F0D9A8", "#EBC9C0", "#FFFFFF"]))
    for x in (1236, 1520, 1700, 1990):
        s += serv(s, x, 336, 104, x)
    # kaplıca binası (odak) + açık havuz
    s += S.agac(s, 1390, 430, 64, 36, renk="#4E9A44")
    s += hamam(s, 1460, 432, 400, 104, 37)
    for (bx, by) in ((1527, 296), (1660, 270), (1777, 296)):
        s += buhar(s, bx, by, 120, int(bx), 22, .7)
    s += f'<path d="M1270 {H} C1500 440 1800 438 2140 436 V{H} Z" fill="#CDB892"/>'
    g = s.lin([(0, "#BFF2EE"), (1, "#1FA6A8")], 0, 410, 0, 452, kull="userSpaceOnUse", ad="hv")
    s += (f'<ellipse cx="1990" cy="436" rx="120" ry="26" fill="#B89C74" stroke="#5A4A36" stroke-width="3"/>'
          f'<ellipse cx="1990" cy="434" rx="104" ry="19" fill="{g}"/>'
          f'<path d="M1916 432 h40 M2000 438 h50" stroke="#FFFFFF" stroke-width="3" opacity=".7"/>')
    s += buhar(s, 1960, 420, 150, 38, 30, .75) + buhar(s, 2030, 424, 130, 39, 24, .65)
    s += '<use href="#pamuk-sasiran" x="1880" y="318" width="96" height="110"/>'
    s += S.cimen(1270, 2100, 458, 40, renk="#4E8F3A", renk2="#7DBE55", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D", "#B07CD8"])
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 3. DURAK · CUMALIKIZIK (ikindi, köy kahvaltısı)

def cumalikizik():
    s = Svg("iz-cum")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#4C94D2"), (.45, "#A9D2EC"), (.78, "#FCE6B6"), (1, "#FFDCA0")])
    s += _zemin(s, ufuk, "#6FA052")
    s += S.gunes(s, 250, 120, 34, hale="#FFE2A0", hale_r=420, guc=.85)
    for i, (x, y, w_) in enumerate(((700, 100, 240), (1100, 60, 280), (1880, 90, 200))):
        s += S.bulut(s, x, y, w_, 50 + i, ust="#FFFFFF", alt="#F3D9C0", op=.95)
    d, _ = S.dag(s, 400, 2300, ufuk + 6, 1500, 90, 51, renk="#5E8F5A", golge="#3F6E45", bicim="tepe", sis="#CFE6C8", isik=-1, sirt=4, puruz=10)
    s += d
    s += _orman(s, 900, 2100, 220, 46, 52, boy=(30, 52), renk="#3E7B4C", golge="#24543A", egim=-.02)
    for k in range(14):
        r = RNG(53 + k)
        s += S.agac(s, 700 + k * 100 + r.uniform(-30, 30), 268 + r.uniform(-14, 10), 22, 53 + k, renk=r.choice(["#5E9E48", "#4E9A44", "#6DAE52"]))
    s += _ova(s, ufuk, "#8CC05A", "#4E8A3C")
    # arka sıra evler (yamaç)
    r = RNG(54)
    for k in range(10):
        x = 1180 + k * 92 + r.uniform(-8, 8)
        s += mini_ev(x, 318 - (k % 2) * 10, 62, 38, EV_RENK[k % len(EV_RENK)])
    s += S.agac(s, 1300, 446, 70, 55, renk="#4E9A40")
    # ön sıra: renkli Cumalıkızık evleri (odak)
    x = 1470
    for k, (w_, h_, c) in enumerate(((150, 170, EV_RENK[0]), (160, 186, EV_RENK[1]), (140, 160, EV_RENK[2]), (170, 194, EV_RENK[3]))):
        s += osmanli_ev(s, x, 432, w_, h_, duvar=c, tohum=56 + k)
        x += w_ + 26
    # Arnavut kaldırımı sokak ve ortasındaki ark
    g = s.lin([(0, "#B8A88E"), (1, "#8C7A62")], 0, 420, 0, H, kull="userSpaceOnUse", ad="sk")
    s += f'<path d="M1300 {H} C1500 446 1800 440 2140 438 V{H} Z" fill="{g}"/>'
    r = RNG(57)
    for k in range(60):
        px, py = r.uniform(1320, 2100), r.uniform(444, 458)
        s += f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(r.uniform(6, 11))}" ry="3.4" fill="#D2C4AA" opacity=".8"/>'
    s += kahvalti_masasi(s, 1310, 452, 230, 58)
    s += '<use href="#pamuk-selam" x="1238" y="362" width="76" height="87"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 4. DURAK · ULUDAĞ YAYLA PİKNİĞİ (öğle)

def uludag():
    s = Svg("iz-ulu")
    ufuk = 268
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#1E6FC6"), (.5, "#62B2EA"), (1, "#D8F0FA")])
    s += _zemin(s, ufuk, "#6DAA4E")
    s += S.gunes(s, 380, 70, 30, hale="#FFF6D0", hale_r=280, guc=.7)
    for i, (x, y, w_) in enumerate(((760, 90, 200), (1120, 50, 240))):
        s += S.bulut(s, x, y, w_, 70 + i, ust="#FFFFFF", alt="#D2E6F4", op=.95)
    d, _ = S.dag(s, 620, 1900, ufuk + 8, 1260, 40, 71, renk="#8D97BC", golge="#646F9A", bicim="sivri", kar_y=150, kar="#FFFFFF",
                 kar_golge="#C8D4EE", sis="#CDE6F4", isik=-1, sirt=8, puruz=16, kenar_isik="#F6FAFF")
    s += d
    d, _ = S.dag(s, 1300, 2360, ufuk + 8, 1880, 70, 72, renk="#8690B6", golge="#5D6894", bicim="sivri", kar_y=170, kar="#FFFFFF",
                 kar_golge="#C3D0EC", sis="#CDE6F4", isik=-1, sirt=6, puruz=14)
    s += d
    # teleferik halatı ve kabin (uzakta)
    s += f'<path d="M520 300 L2140 40" stroke="#2A2E36" stroke-width="2.4"/><path d="M520 310 L2140 52" stroke="#2A2E36" stroke-width="1.6" opacity=".7"/>'
    s += kabin(1560, 300 - (1560 - 520) * 260 / 1620 + 2, .5, renk=MERCAN)
    # göknar ormanı katmanları
    s += _orman(s, 0, 2100, ufuk + 6, 70, 73, boy=(36, 56), renk="#4E7E62", golge="#36604A", op=.85)
    s += _orman(s, 0, 2100, ufuk + 36, 46, 74, boy=(56, 88))
    g = s.lin([(0, "#9CCB5E"), (1, "#5E9A3E")], 0, ufuk + 40, 0, H, kull="userSpaceOnUse", ad="yy")
    s += f'<path d="M0 {ufuk + 60} C600 {ufuk + 40} 1300 {ufuk + 70} 2100 {ufuk + 50} V{H} H0 Z" fill="{g}"/>'
    s += goknar(1290, 440, 150, 75) + goknar(2060, 430, 170, 76) + goknar(2010, 446, 120, 77)
    # piknik (odak): masa, mangal, Yusuf defterle
    s += piknik_masasi(1360, 440, 230, 78)
    s += mangal(s, 1700, 448, 150, 79)
    s += '<use href="#yusuf-defter" x="1790" y="236" width="200" height="210"/>'
    s += '<use href="#pamuk-otur" x="1600" y="352" width="78" height="90"/>'
    s += S.cimen(1200, 2100, 458, 80, renk="#4E8F3A", renk2="#86C25A", boy=13, cicek=["#FFFFFF", "#F0A21A", "#B07CD8", "#FF5C8A"])
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 5. DURAK · KOZA HAN AVLUSU (altın saat)

def kozahan():
    s = Svg("iz-koz")
    s += S.gokyuzu(s, 0, 0, W, 90, duraklar=[(0, "#5A9AD8"), (1, "#FFE0A6")])
    s += han_cephe(s, -40, 2140, 90, 420, 90, aralik=176)
    # altın saat ışığı
    gl = s.lin([(0, "#FFD27A", .38), (1, "#FFD27A", 0)], 0, 0, 1, 0, ad="isk")
    s += f'<rect x="0" y="80" width="{W}" height="340" fill="{gl}"/>'
    s += esarp_ipi(1250, 214, 1700, 210, 6, 91, sark=24, boy=(70, 100))
    s += esarp_ipi(1700, 210, 2140, 216, 6, 92, sark=24, boy=(70, 100))
    g = s.lin([(0, "#E9DCC4"), (1, "#C9B694")], 0, 410, 0, H, kull="userSpaceOnUse", ad="avl")
    s += f'<rect x="0" y="410" width="{W}" height="{H - 410}" fill="{g}"/>'
    for k in range(12):
        s += f'<path d="M{k * 190} {H} L{k * 190 + 140} 410" stroke="#B8A27E" stroke-width="2" opacity=".6"/>'
    s += '<path d="M0 432 H2100" stroke="#B8A27E" stroke-width="2" opacity=".6"/>'
    # avlu: ağaç gölgesi (solda), koza çuvalları, boya kazanı, çile direği
    s += S.agac(s, 980, 430, 120, 93, renk="#4E9A44")
    s += koza_cuvali(1400, 452, 120, 94) + koza_cuvali(1522, 456, 96, 95)
    s += boya_kazani(s, 1690, 452, 130, renk="#B8202E", tohum=96)
    s += cile_diregi(1820, 452, 190)
    s += '<use href="#pamuk-akce" x="1340" y="300" width="96" height="110"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== HÜLASA · GÖLYAZI (gün batımı, 40 mm)

def golyazi(h=400):
    s = Svg("iz-gol")
    h = int(h)
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gunbatimi")
    s += S.gunes(s, 1180, ufuk - 22, 44, cekirdek="#FFF3D6", hale="#FFB36B", hale_r=620, guc=.95)
    for (x, y, w_, k) in ((420, 120, 520, 20), (1460, 90, 560, 22), (900, 170, 380, 14)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC9B8", "#E2709A", .7)
    d, _ = S.dag(s, -60, 1100, ufuk + 4, 420, 176, 101, renk="#7A4E8C", golge="#5A3A72", bicim="tepe", sis="#F08A8A", isik=-1, sirt=2, puruz=5)
    s += d
    d, _ = S.dag(s, 1500, 2200, ufuk + 4, 1900, 190, 102, renk="#6E4A84", golge="#4E346A", bicim="tepe", sis="#F08A8A", isik=-1, sirt=2, puruz=5)
    s += d
    s += S.gol(s, 0, ufuk, W, h - ufuk, 103, ufuk="#FFC08A", orta="#C2649A", derin="#3A2A6A", gunes_x=1180, parilti_renk="#FFE0A0")
    # Gölyazı yarımadası: evler, çınarlar, leylek yuvası
    gy = s.lin([(0, "#5A3A62"), (1, "#3E2A50")], 0, 250, 0, 330, kull="userSpaceOnUse", ad="ya")
    s += f'<path d="M1380 312 C1460 280 1560 262 1700 258 C1860 254 2000 262 2140 270 V330 C1900 326 1600 328 1380 312 Z" fill="{gy}"/>'
    r = RNG(104)
    for k in range(13):
        x = 1460 + k * 50 + r.uniform(-8, 8)
        yy = 300 - r.uniform(0, 22)
        hh = r.uniform(26, 40)
        s += f'<rect x="{f(x)}" y="{f(yy - hh)}" width="40" height="{f(hh)}" fill="#4A2E58"/><path d="M{f(x - 5)} {f(yy - hh)} L{f(x + 20)} {f(yy - hh - 16)} L{f(x + 45)} {f(yy - hh)} Z" fill="#3A2248"/>'
        if r.random() < .7:
            s += f'<rect x="{f(x + 12)}" y="{f(yy - hh * .6)}" width="8" height="10" fill="#FFC86A"/>'
    for x in (1440, 1780, 2060):
        s += S.agac(s, x, 300, 38, int(x), renk="#3E2A50", golge="#2A1C38")
    s += f'<path d="M1966 300 V196" stroke="#3A2248" stroke-width="7"/><path d="M1936 196 Q1966 182 1996 196 Q1966 206 1936 196 Z" fill="#5A3A26"/>'
    s += leylek(1966, 188, .9, ucan=False)
    for (x, y, o, yon) in ((1560, 110, .9, 1), (1700, 70, .7, -1), (1830, 136, .8, 1)):
        s += leylek(x, y, o, ucan=True, yon=yon)
    for (x, y, uz, c) in ((760, 300, 90, "#4A2E58"), (1240, 330, 110, "#3A2248")):
        s += S.tekne(s, x, y, uz, govde=c, ust="#7A5A86", cizgi="#2A1838", ayrinti=True)
    s += Y.iskele(s, 1660, 2140, 352, 14, 105, ahsap="#4A2E3A", cizgi="#2A1828", merdiven=False, direk_n=6)
    s += '<use href="#pamuk-kitap" x="1860" y="236" width="106" height="121"/>'
    s += S.sazlik(1240, 1640, h + 4, 106, renk="#3A2A3A", bas="#5A3A26", boy=70)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== YAN YOL 1 · TİRİLYE (sabah, meclis)

def tirilye():
    s = Svg("iz-tir")
    ufuk = 226
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#5C86D2"), (.5, "#A9C8EE"), (.85, "#FFE2C2"), (1, "#FFF2DE")])
    s += S.gunes(s, 280, 150, 34, hale="#FFE2B0", hale_r=420, guc=.85)
    for i, (x, y, w_) in enumerate(((720, 90, 220), (1100, 50, 260))):
        s += S.bulut(s, x, y, w_, 110 + i, ust="#FFFFFF", alt="#F2D6CC", op=.9)
    s += f'<path d="M-20 {ufuk + 2} C300 {ufuk - 14} 700 {ufuk - 10} 980 {ufuk + 2} Z" fill="#9AA6CF" opacity=".8"/>'
    s += S.gol(s, 0, ufuk, W, H - ufuk, 111, ufuk="#CFE8F4", orta="#3FA0C8", derin="#145C8E", gunes_x=280, parilti_renk="#FFF0C0")
    # Tirilye: zeytinlikli yamaçta taş evler (sağ)
    gy = s.lin([(0, "#9CB06A"), (1, "#6E8A44")], 0, 140, 0, 400, kull="userSpaceOnUse", ad="yam")
    s += f'<path d="M1080 {H} C1160 300 1300 200 1500 150 C1700 110 1950 104 2140 110 V{H} Z" fill="{gy}"/>'
    r = RNG(112)
    for k in range(16):
        x = 1360 + (k % 8) * 96 + r.uniform(-10, 10)
        yy = 250 - (k // 8) * 70 - (k % 8) * 8 + r.uniform(-6, 6)
        s += mini_ev(x, yy, 64, 42, r.choice(["#E8D4B0", "#DCC29A", "#F2E6D0", "#E6C8A8"]), cati="#B04A30")
    for k in range(8):
        s += zeytin(s, 1180 + k * 120 + r.uniform(-20, 20), 330 + r.uniform(-10, 14), 40, 113 + k)
    # kahve bahçesi: asma çardağı, ahşap döşeme
    s += f'<path d="M1240 40 H2140" stroke="#6B4A2E" stroke-width="12"/><path d="M1300 40 V420 M2080 40 V420" stroke="#6B4A2E" stroke-width="12"/>'
    for k in range(24):
        x = 1250 + k * 37 + r.uniform(-8, 8)
        y = 40 + r.uniform(-14, 26)
        s += f'<path d="M{f(x)} {f(y)} q14 -10 26 0 q-2 14 -13 18 q-11 -4 -13 -18 Z" fill="{r.choice(["#4E9A44", "#6DB35A", "#3E7E3E"])}"/>'
        if k % 5 == 2:
            s += "".join(f'<circle cx="{f(x + 10 + (j % 2) * 7)}" cy="{f(y + 22 + j * 6)}" r="5" fill="#6A3A7A"/>' for j in range(4))
    s += f'<rect x="1200" y="396" width="940" height="70" fill="#9A6B42"/>'
    for k in range(10):
        s += f'<path d="M{1200 + k * 96} 396 V{H}" stroke="#6B4A2E" stroke-width="3"/>'
    s += f'<ellipse cx="1676" cy="420" rx="150" ry="22" fill="#F6EAD2" stroke="#7A5A2A" stroke-width="4"/>'
    s += '<use href="#elif-soru" x="1300" y="176" width="250" height="263"/>'
    s += '<use href="#yusuf-anlatan" x="1800" y="176" width="250" height="263"/>'
    s += '<use href="#pamuk-dusunen" x="1590" y="250" width="170" height="194"/>'
    for x in (1600, 1640, 1712, 1752):
        s += Y.cay_bardak_kucuk(x, 424, 26)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== YAN YOL 2 · MUDANYA (öğle, iskele)

def mudanya():
    s = Svg("iz-mud")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2E8AD6"), (.55, "#8ECCF0"), (1, "#E6F6FC")])
    s += S.gunes(s, 360, 80, 30, hale="#FFF2C2", hale_r=300, guc=.75)
    for i, (x, y, w_) in enumerate(((680, 110, 230), (1080, 60, 300), (1900, 90, 220))):
        s += S.bulut(s, x, y, w_, 120 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    s += f'<path d="M-20 {ufuk + 2} C200 {ufuk - 30} 520 {ufuk - 26} 820 {ufuk + 2} Z" fill="#8FA8C8" opacity=".85"/>'
    s += S.gol(s, 0, ufuk, W, H - ufuk, 121, ufuk="#BFE6F2", orta="#2E9AC8", derin="#0E4F86", gunes_x=360, parilti_renk="#FFFFFF")
    # deniz otobüsü (katamaran, uzakta) ve tekneler
    s += (f'<g transform="translate(860 272) scale(.9)"><path d="M-110 0 H110 L96 18 H-100 Z" fill="#F4F6F8" stroke="#1B1D26" stroke-width="2.4"/>'
          f'<path d="M-80 0 V-22 H70 L90 0 Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="2.4"/><path d="M-70 -14 H64" stroke="#2B50B5" stroke-width="7"/>'
          f'<path d="M-108 10 H100" stroke="{MERCAN}" stroke-width="4"/></g>')
    s += S.tekne(s, 1120, 330, 120, govde="#2B50B5", yelken="#FFF1DE")
    s += S.tekne(s, 1520, 360, 110, govde=MERCAN, ust="#F4E9D8")
    # sahil: tarihî evler ve çınarlar (sağ)
    g = s.lin([(0, "#D6C6A6"), (1, "#B8A27E")], 0, 300, 0, 360, kull="userSpaceOnUse", ad="rht")
    s += f'<path d="M1600 312 H2140 V372 H1600 Z" fill="{g}"/>'
    r = RNG(122)
    for k, x in enumerate((1640, 1770, 1900, 2020)):
        s += osmanli_ev(s, x, 312, 110, 140 + (k % 2) * 16, duvar=["#FFFFFF", "#F6D8A8", "#CFE2F2", "#F2C6C0"][k], tohum=123 + k, kat_tas=.32)
    for x in (1610, 2110):
        s += S.agac(s, x, 314, 46, int(x), renk="#4E9A44")
    s += Y.iskele(s, 1180, 1760, 392, 18, 124, ahsap="#9A6B42", merdiven=True, direk_n=7)
    s += '<use href="#pamuk-otur" x="1300" y="300" width="84" height="96"/>'
    for k, (x, y, o) in enumerate(((1440, 150, 1.4), (1580, 200, 1.1), (1260, 120, .9))):
        s += S.marti(x, y, o, 4 - k, ayrintili=(k == 0))
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== YAN YOL 3 · TELEFERİK (ikindi)

def teleferik():
    s = Svg("iz-tel")
    ufuk = 330
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3A4FA6"), (.35, "#8C78C6"), (.62, "#F59CA8"), (.85, "#FFC88E"), (1, "#FFE2B8")])
    s += S.gunes(s, 520, 250, 40, cekirdek="#FFF3DA", hale="#FFB870", hale_r=520, guc=.9)
    for (x, y, w_, k) in ((900, 120, 520, 130), (1500, 80, 480, 131)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFD7CF", "#F094AE", .65)
    # uzakta Bursa ovası ve şehir
    s += _ova(s, ufuk, "#C9B98A", "#8C9A62", ad="tov")
    r = RNG(132)
    for k in range(70):
        x, y = r.uniform(0, 1300), r.uniform(ufuk + 12, ufuk + 90)
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(8, 16))}" height="{f(r.uniform(6, 10))}" fill="{r.choice(["#E8D4B0", "#F2E6D0", "#D9B48C", "#C2563A"])}" opacity=".85"/>'
    # Uludağ yamacı: sağa doğru yükselen orman
    gy = s.lin([(0, "#4E8A50"), (1, "#2E5E3A")], 0, 0, 0, H, kull="userSpaceOnUse", ad="tym")
    s += f'<path d="M700 {H} C1000 360 1400 220 1800 120 C1950 84 2050 70 2140 66 V{H} Z" fill="{gy}"/>'
    for k in range(70):
        t = r.random()
        x = 760 + t * 1380
        ytop = H - (H - 70) * (t ** 1.1) * .95
        y = r.uniform(ytop + 20, H)
        s += goknar(x, y, r.uniform(36, 70) * (1 + (y - ytop) / 400), 133 + k)
    # halat, direkler, kabinler (basamak basamak)
    p0, p1 = (420, 420), (2140, 20)
    def hp(x):
        return p0[1] + (p1[1] - p0[1]) * (x - p0[0]) / (p1[0] - p0[0])
    for (dx, dh) in ((1280, 150), (1840, 140)):
        y0 = hp(dx) + 10
        s += f'<path d="M{dx - 26} {f(y0 + dh)} L{dx} {f(y0)} L{dx + 26} {f(y0 + dh)} M{dx - 18} {f(y0 + dh * .66)} H{dx + 18} M{dx - 10} {f(y0 + dh * .33)} H{dx + 10}" stroke="#3A3F4B" stroke-width="6" fill="none"/>'
        s += f'<path d="M{dx - 40} {f(y0)} H{dx + 40}" stroke="#3A3F4B" stroke-width="8"/>'
    s += f'<path d="M{p0[0]} {p0[1]} L{p1[0]} {p1[1]}" stroke="#1B1D26" stroke-width="3.2"/>'
    s += f'<path d="M{p0[0]} {p0[1] + 14} L{p1[0]} {p1[1] + 14}" stroke="#1B1D26" stroke-width="2" opacity=".7"/>'
    for (x, renk, o, pm) in ((1420, MERCAN, .95, False), (1640, TURKUAZ, 1.1, True), (1990, "#F0A21A", 1.2, False)):
        s += kabin(x, hp(x), o, renk, pamuk=pm)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== BÜYÜK İMTİHAN · BURSA HİSARI (gün batımı, 62 mm)

def hisar_buyuk(h=620):
    s = Svg("iz-his")
    h = int(h)
    ufuk = 360
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gunbatimi")
    s += S.gunes(s, 520, ufuk - 30, 54, cekirdek="#FFF3D6", hale="#FFB36B", hale_r=640, guc=.95)
    for (x, y, w_, k) in ((300, 150, 520, 140), (1000, 90, 560, 141), (1500, 200, 420, 142)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC9B8", "#E2709A", .7)
    d, _ = S.dag(s, 300, 2300, ufuk + 6, 1200, 80, 143, renk="#9A6E9E", golge="#6A4A7E", bicim="sivri", kar_y=170, kar="#FFE6EE",
                 kar_golge="#D6A9C6", sis="#FF9E8A", isik=-1, sirt=7, puruz=14, kenar_isik="#FFD7C2")
    s += d
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 20, 40, 144, "#4E7A58", "#2E5A3E", dalga=5)
    s += tb
    s += _orman(s, 500, 2100, ufuk + 10, 40, 145, boy=(30, 50), renk="#3A6A4E", golge="#244A36", op=.9)
    g = s.lin([(0, "#7A8A5A"), (1, "#4E5E3A")], 0, ufuk + 40, 0, h, kull="userSpaceOnUse", ad="sh")
    s += f'<rect x="0" y="{ufuk + 40}" width="{W}" height="{h - ufuk - 40}" fill="{g}"/>'
    r = RNG(146)
    for k in range(80):
        x, y = r.uniform(0, 1300), r.uniform(ufuk + 60, h - 30)
        w_ = r.uniform(30, 52)
        s += mini_ev(x, y, w_, w_ * .62, r.choice(["#F6EEDC", "#F0D9A8", "#EBC9C0", "#FFFFFF", "#E8D4B0"]), cati=r.choice(["#B8553A", "#A8442C", "#C2563A"]))
    for k in range(18):
        s += serv(s, r.uniform(0, 1300), r.uniform(ufuk + 80, h - 20), r.uniform(60, 100), 147 + k)
    # Hisar: kayalık sırt, surlar, burçlar, saat kulesi (sağ)
    gk = s.lin([(0, "#B89A7A"), (1, "#7A5E46")], 0, 360, 0, h, kull="userSpaceOnUse", ad="hk")
    s += f'<path d="M1120 {h} C1220 520 1300 470 1440 452 C1640 430 1900 420 2140 424 V{h} Z" fill="{gk}"/>'
    s += sur(s, 1260, 2140, 470, 92, 148, tas="#E2CCA4", burc_ara=210)
    kule, tepe = saat_kulesi(s, 1760, 400, 290, 149)
    s += kule
    s += S.agac(s, 1490, 470, 40, 150, renk="#4E8A44") + S.agac(s, 2060, 470, 44, 151, renk="#4E8A44")
    s += '<use href="#pamuk-akce" x="1460" y="470" width="120" height="137"/>'
    s += _cerceve_golge(s, h) if h == H else ""
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== BÜYÜK İMTİHAN 2 · HİSAR KAPISI (alaca, 30 mm)

def hisar_kapi(h=300):
    from cizim.sus import kilim_serit
    s = Svg("iz-hka")
    h = int(h)
    s += S.gokyuzu(s, 0, 0, W, 120, "alaca")
    s += S.yildizlar(s, 0, 0, W, 90, 40, 160)
    g = s.lin([(0, "#E2CCA4"), (1, "#B89A72")], 0, 40, 0, h, kull="userSpaceOnUse", ad="hkd")
    s += f'<rect x="0" y="64" width="{W}" height="{h - 64}" fill="{g}"/>'
    for j in range(1, 10):
        s += f'<rect x="0" y="{64 + j * 24}" width="{W}" height="6" fill="{TUGLA}" opacity=".6"/>'
    for i in range(0, W, 30):
        s += f'<rect x="{i + 4}" y="44" width="20" height="22" fill="#D8C29A" stroke="#5A4A36" stroke-width="2"/>'
    for bx in (1440, 1960):
        s += f'<rect x="{bx - 80}" y="20" width="160" height="{h}" fill="#D8C29A" stroke="#5A4A36" stroke-width="3"/>'
        for t in range(4):
            s += f'<rect x="{bx - 80 + t * 40 + 4}" y="0" width="30" height="22" fill="#D8C29A" stroke="#5A4A36" stroke-width="2"/>'
        for j in range(1, 11):
            s += f'<rect x="{bx - 80}" y="{20 + j * 24}" width="160" height="6" fill="{TUGLA}" opacity=".6"/>'
        s += f'<rect x="{bx - 8}" y="70" width="16" height="40" rx="6" fill="#2E2A30"/>'
    kx = 1700
    s += f'<path d="M{kx - 130} {h} V150 Q{kx - 130} 60 {kx} 54 Q{kx + 130} 60 {kx + 130} 150 V{h} Z" fill="#3A2618" stroke="#2A1A10" stroke-width="5"/>'
    gl = s.rad([(0, "#FFD27A", .9), (.5, "#FFB43A", .35), (1, "#FFB43A", 0)], kx, 200, 200, kull="userSpaceOnUse", ad="gl")
    s += f'<rect x="{kx - 130}" y="54" width="260" height="{h - 54}" fill="{gl}"/>'
    s += f'<path d="M{kx - 150} 150 Q{kx - 150} 40 {kx} 34 Q{kx + 150} 40 {kx + 150} 150" fill="none" stroke="#E2CCA4" stroke-width="22"/>'
    s += f'<path d="M{kx - 150} 150 Q{kx - 150} 40 {kx} 34 Q{kx + 150} 40 {kx + 150} 150" fill="none" stroke="{TUGLA}" stroke-width="6" stroke-dasharray="26 14"/>'
    for (px, ac) in ((kx - 126, -1), (kx + 126, 1)):
        s += f'<path d="M{px} {h} V150 L{px - ac * 70} 170 V{h} Z" fill="#7A4E2E" stroke="#3A2618" stroke-width="3"/>'
    for tx in (1330, 2070):
        s += f'<path d="M{tx} 120 v40" stroke="#5A3A26" stroke-width="6"/><path d="M{tx - 8} 120 q8 -26 16 0 Z" fill="#FFB43A"/>'
        s += f'<circle cx="{tx}" cy="112" r="40" fill="{gl}"/>'
    kil = kilim_serit("iz-hka-k", 2100, 60).replace("<svg ", '<svg width="2100" height="60" ')
    s += f'<g transform="translate(0 {h - 60})">{kil}</g>'
    s += '<use href="#pamuk-selam" x="1640" y="150" width="96" height="110"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== CEVAPLAR · BURSA GECESİ (36 mm)

def bursa_gece(h=360):
    s = Svg("iz-gec")
    h = int(h)
    ufuk = 240
    s += S.gokyuzu(s, 0, 0, W, h, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk, 160, 170)
    s += S.ay(s, 1200, 80, 32, golge_renk="#13204A")
    d, _ = S.dag(s, 300, 2300, ufuk + 6, 1100, 60, 171, renk="#2E3A70", golge="#232C5A", bicim="sivri", kar_y=150, kar="#B8C4E8",
                 kar_golge="#7E8CC0", isik=-1, sirt=6, puruz=12)
    s += d
    g = s.lin([(0, "#1C2350"), (1, "#0E1230")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="sg")
    s += f'<rect x="0" y="{ufuk}" width="{W}" height="{h - ufuk}" fill="{g}"/>'
    r = RNG(172)
    for k in range(260):
        x, y = r.uniform(0, W), r.uniform(ufuk + 10, h - 10)
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(4, 8))}" height="{f(r.uniform(4, 7))}" fill="{r.choice(["#FFD27A", "#FFE6A8", "#FFB86A"])}" opacity="{f(r.uniform(.5, 1), 2)}"/>'
    gk = s.lin([(0, "#3A3A6A"), (1, "#232450")], 0, 200, 0, h, kull="userSpaceOnUse", ad="gk")
    s += f'<path d="M1300 {h} C1380 290 1460 270 1600 262 C1800 252 2000 252 2140 256 V{h} Z" fill="{gk}"/>'
    s += sur(s, 1420, 2140, 300, 60, 173, tas="#4A4C80", burc_ara=200)
    kule, _ = saat_kulesi(s, 1800, 262, 210, 174, isikli=True)
    s += kule
    s += '<use href="#pamuk-otur" x="240" y="250" width="90" height="103"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== FİNAL · BURSA'DA GÜN BATIMI (90 mm)

def final_bursa(h=900, nisanlar=None):
    s = Svg("iz-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#33449C"), (.3, "#8A7CC8"), (.55, "#F29CB4"), (.78, "#FFC892"), (1, "#FFE6C0")])
    gx, gy = 620, ufuk - 40
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE8B0" opacity=".12"/>'
    s += S.gunes(s, gx, gy, 64, hale="#FFC98A", hale_r=680, guc=.95)
    for (x, y, w_, k) in ((200, 240, 520, 20), (1100, 160, 600, 24), (1500, 330, 460, 14)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFE0E6", "#F7A6BC", .7)
    d, _ = S.dag(s, 500, 2400, ufuk + 6, 1460, 120, 180, renk="#A07AA8", golge="#6E5288", bicim="sivri", kar_y=230, kar="#FFEAF0",
                 kar_golge="#D8B0CC", sis="#FFA18E", isik=-1, sirt=8, puruz=16, kenar_isik="#FFD7C2")
    s += d
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 40, 50, 181, "#5E8A58", "#3E6A44", dalga=5)
    s += tb
    s += _orman(s, 0, 2100, ufuk + 30, 50, 182, boy=(34, 56), renk="#3E6E50", golge="#26503A", op=.9)
    g = s.lin([(0, "#8CB860"), (1, "#4E8A3E")], 0, ufuk + 60, 0, h, kull="userSpaceOnUse", ad="fz")
    s += f'<path d="M0 {ufuk + 80} C600 {ufuk + 60} 1300 {ufuk + 90} 2100 {ufuk + 70} V{h} H0 Z" fill="{g}"/>'
    # Hisar ve saat kulesi (sağ) + Pamuk bayrakla
    gk = s.lin([(0, "#C2A27E"), (1, "#8A6A4A")], 0, 620, 0, h, kull="userSpaceOnUse", ad="fk")
    s += f'<path d="M1200 {h} C1300 760 1420 700 1600 684 C1800 668 2000 664 2140 666 V{h} Z" fill="{gk}"/>'
    s += sur(s, 1320, 2140, 712, 110, 183, tas="#EAD4AC", burc_ara=220)
    kule, tepe = saat_kulesi(s, 1800, 640, 380, 184, bayrak=False)
    s += kule
    s += f'<use href="#pamuk-bayrak" x="{f(tepe[0] - 150)}" y="{f(tepe[1] - 330)}" width="300" height="353"/>'
    # dut ağacı (sol): ipek böceğinin yaprağı; ipek iplikten nişan çelengi
    s += S.agac(s, 240, h - 10, 150, 185, renk="#3E8A3E", golge="#245A2A", meyve="#4A1E3A")
    sx, sy = 360, h - 330
    ex, ey = tepe[0] - 120, tepe[1] - 60
    kx, ky = (sx + ex) / 2, max(sy, ey) + 60
    s += f'<path d="M{f(sx)} {f(sy)} Q{f(kx)} {f(ky)} {f(ex)} {f(ey)}" stroke="#F6E7BF" stroke-width="6" fill="none"/>'
    s += f'<path d="M{f(sx)} {f(sy)} Q{f(kx)} {f(ky)} {f(ex)} {f(ey)}" stroke="#C9952B" stroke-width="2" fill="none" stroke-dasharray="10 8"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .7) / (len(nisanlar) + .4)
            x = (1 - t) ** 2 * sx + 2 * (1 - t) * t * kx + t * t * ex
            y = (1 - t) ** 2 * sy + 2 * (1 - t) * t * ky + t * t * ey
            s += f'<path d="M{f(x)} {f(y)} v16" stroke="#C9952B" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 56)} {f(y + 12)}) rotate({f((k % 2 * 2 - 1) * 5)} 56 64)">{ns}</g>'
    for k, (x, y) in enumerate(((300, h - 360), (210, h - 300), (330, h - 270))):
        s += f'<ellipse cx="{x}" cy="{y}" rx="16" ry="10" fill="#FFF8E6" stroke="#B8A780" stroke-width="2" transform="rotate({k * 30 - 20} {x} {y})"/>'
    s += cini_pano(560, h - 120, 9, 1, 104, kenar=False)
    r = RNG(186)
    for k in range(60):
        x, y = r.uniform(300, 1900), r.uniform(80, 640)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ Van → İznik kartı: sadeleştirilmiş Türkiye ana hatları
# Kaynak: yerel-cerceve/uretec/turkiye_veri.py (Natural Earth, kamu malı; Lambert konik, 1 birim = 1 km) — Douglas–Peucker
# ile ≈ 7 km toleransla sadeleştirilip BURAYA KOPYALANDI (ünite başka klasörden içe aktarma yapmaz).
TR_ANADOLU = [(1568, 175), (1595, 211), (1585, 244), (1598, 284), (1654, 286), (1700, 326), (1678, 314), (1667, 354),
    (1635, 362), (1664, 418), (1670, 468), (1685, 473), (1668, 524), (1704, 540), (1705, 570), (1727, 585),
    (1726, 602), (1712, 599), (1686, 626), (1675, 613), (1678, 596), (1664, 589), (1641, 604), (1548, 593),
    (1530, 621), (1514, 626), (1499, 603), (1483, 621), (1437, 635), (1368, 637), (1305, 674), (1240, 693),
    (1194, 691), (1149, 669), (1080, 702), (1045, 704), (1037, 690), (1008, 682), (999, 721), (1012, 748), (984, 750),
    (984, 775), (970, 780), (967, 794), (944, 784), (950, 773), (933, 741), (970, 703), (953, 672), (916, 693),
    (926, 695), (918, 708), (893, 715), (835, 685), (798, 710), (769, 751), (761, 740), (744, 759), (697, 758),
    (665, 770), (626, 752), (596, 710), (536, 679), (478, 667), (452, 740), (428, 731), (384, 748), (334, 715),
    (337, 697), (328, 697), (336, 684), (322, 674), (311, 690), (280, 656), (274, 666), (263, 659), (265, 673),
    (241, 689), (234, 684), (246, 680), (236, 674), (250, 663), (214, 665), (209, 676), (182, 671), (208, 659),
    (242, 665), (244, 647), (255, 651), (271, 638), (176, 639), (176, 621), (204, 623), (210, 607), (196, 608),
    (193, 590), (173, 595), (177, 568), (160, 559), (182, 552), (183, 525), (152, 517), (144, 496), (128, 508),
    (98, 485), (124, 470), (114, 467), (118, 442), (136, 462), (137, 486), (141, 472), (148, 481), (181, 473),
    (161, 474), (144, 448), (176, 424), (155, 415), (162, 400), (141, 378), (172, 347), (98, 352), (113, 294),
    (164, 254), (194, 251), (211, 251), (229, 270), (260, 264), (244, 251), (251, 247), (274, 255), (265, 267),
    (359, 273), (364, 263), (336, 254), (354, 243), (436, 237), (379, 225), (360, 200), (375, 178), (546, 203),
    (562, 178), (664, 124), (724, 105), (841, 114), (858, 97), (880, 106), (870, 118), (903, 148), (949, 141),
    (957, 168), (979, 190), (1009, 177), (1074, 212), (1087, 200), (1105, 218), (1142, 224), (1233, 198), (1292, 216),
    (1367, 177), (1405, 143), (1430, 151), (1440, 141), (1484, 146), (1499, 127)]
TR_TRAKYA = [(285, 89), (280, 106), (299, 141), (370, 177), (358, 202), (327, 204), (322, 191), (321, 202), (290, 188),
    (270, 200), (235, 195), (213, 225), (160, 248), (111, 288), (119, 258), (173, 233), (109, 220), (138, 189),
    (138, 158), (164, 148), (164, 119), (144, 98), (206, 70), (225, 71), (246, 94)]
TR_VAN_GOLU = [(1570, 486), (1553, 485), (1546, 467), (1538, 475), (1520, 469), (1497, 473), (1505, 458), (1512, 457),
    (1506, 446), (1531, 435), (1562, 432), (1571, 422), (1565, 421), (1562, 426), (1559, 418), (1587, 408),
    (1608, 411), (1588, 428), (1580, 427), (1563, 454), (1572, 452), (1584, 460), (1584, 471), (1572, 479)]
TR_VAN, TR_IZNIK = (1590, 464), (416, 270)   # Van ve İznik aynı izdüşümde


def van_iznik_karti(s, x, y, w):
    """Açılış haritasının köşesinde: Van'dan İznik'e (kuş uçuşu ≈ 1200 km) küçük Türkiye kartı."""
    xs = [p[0] for p in TR_ANADOLU + TR_TRAKYA]
    ys = [p[1] for p in TR_ANADOLU + TR_TRAKYA]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    o = (w - 40) / (x1 - x0)
    hh = (y1 - y0) * o
    ox, oy = x + 20 - x0 * o, y + 54 - y0 * o
    P = lambda p: (ox + p[0] * o, oy + p[1] * o)  # noqa: E731
    out = [f'<rect x="{f(x + 6)}" y="{f(y + 7)}" width="{f(w)}" height="{f(hh + 104)}" rx="18" fill="#0E4C5A" opacity=".85"/>',
           f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(hh + 104)}" rx="18" fill="#FFFDF7" stroke="#1B1D26" stroke-width="3"/>']
    for kume, c in ((TR_ANADOLU, "#F2E2B8"), (TR_TRAKYA, "#F2E2B8")):
        out.append(f'<path d="{cizgi_d([P(p) for p in kume], True)}" fill="{c}" stroke="#8A6212" stroke-width="2.2" stroke-linejoin="round"/>')
    out.append(f'<path d="{cizgi_d([P(p) for p in TR_VAN_GOLU], True)}" fill="{TURKUAZ}" stroke="#0A6C74" stroke-width="1.6"/>')
    (vx, vy), (ix, iy) = P(TR_VAN), P(TR_IZNIK)
    kx, ky = (vx + ix) / 2, min(vy, iy) - hh * .55
    out.append(f'<path d="M{f(vx)} {f(vy)} Q{f(kx)} {f(ky)} {f(ix)} {f(iy)}" fill="none" stroke="{MERCAN}" stroke-width="4" stroke-dasharray="11 8" stroke-linecap="round"/>')
    a = math.atan2(iy - ky, ix - kx)
    out.append(f'<path d="M{f(ix)} {f(iy)} L{f(ix - 16 * math.cos(a) + 8 * math.sin(a))} {f(iy - 16 * math.sin(a) - 8 * math.cos(a))} '
               f'L{f(ix - 16 * math.cos(a) - 8 * math.sin(a))} {f(iy - 16 * math.sin(a) + 8 * math.cos(a))} Z" fill="{MERCAN}"/>')
    out.append(f'<circle cx="{f(vx)}" cy="{f(vy)}" r="9" fill="#FFFFFF" stroke="#1B1D26" stroke-width="3"/>')
    out.append(f'<path d="{cizgi_d(selcuklu_yildizi(ix, iy, 14), True)}" fill="#F0C14A" stroke="#1B1D26" stroke-width="2"/>')
    out.append(f'<use href="#pamuk-bas-gulen" x="{f(vx - 30)}" y="{f(vy - 70)}" width="60" height="58"/>')
    out.append(f'<text x="{f(x + 22)}" y="{f(y + 38)}" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">Van’dan İznik’e</text>')
    out.append(f'<text x="{f(vx + 2)}" y="{f(vy + 34)}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="20" letter-spacing="1" fill="#0A6C74">VAN</text>')
    out.append(f'<text x="{f(ix)}" y="{f(iy + 36)}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="20" letter-spacing="1" fill="#A12817">İZNİK</text>')
    out.append(f'<text x="{f(x + w - 20)}" y="{f(y + hh + 90)}" text-anchor="end" font-family="Nunito" font-weight="900" font-size="21" fill="#56636E">kuş uçuşu ≈ 1200 km</text>')
    return "".join(out), (x, y, x + w + 6, y + hh + 111)


# ================================================================== AÇILIŞ · BURSA PANORAMASI + TUR ROTASI

# Stilize (temsilî) harita: KUZEYDEN GÜNEYE bakış (uzak = güney, doğu solda). Uludağ arkada; İznik Gölü sol önde; Bursa
# eteklerde; Gemlik Körfezi kıyısında Mudanya ve Tirilye sağ önde; Uluabat Gölü (Gölyazı) sağda. Şehir içindeki yakın
# duraklar (Koza Han, Hisar, teleferik) okunur olsun diye açılarak çizildi.
# (anahtar, x, y, etiket üst, etiket ad, alt, tür)
DURAKLAR = [
    ("1", 170, 700, "1. DURAK · İZNİK", "Kimya her yerde", "s.2 · +100 akçe", "durak"),
    ("2", 1570, 520, "2. DURAK · ÇEKİRGE", "Asidik, bazik, nötr", "s.3 · +150 akçe", "durak"),
    ("3", 620, 470, "3. DURAK · CUMALIKIZIK", "Evdeki kimyasallar", "s.4 · +150 akçe", "durak"),
    ("4", 960, 330, "4. DURAK · ULUDAĞ", "Mutfak ve adil deney", "s.5 · +150 akçe", "durak"),
    ("5", 1080, 650, "5. DURAK · KOZA HAN", "Disiplinler, meslekler", "s.6 · +150 akçe", "durak"),
    ("H", 1910, 650, "GÖLYAZI", "Hülasa", "s.7 · +40 akçe", "hulasa"),
    ("M", 1830, 930, "TİRİLYE", "Meclis: Kim haklı?", "s.8 · +120 akçe", "yan"),
    ("K", 1450, 960, "MUDANYA", "Kıssa", "s.9 · +120 akçe", "yan"),
    ("A", 1130, 520, "TELEFERİK", "Anahtar merdiveni", "s.10 · +120 akçe", "yan"),
    ("V", 1340, 650, "BURSA HİSARI", "Büyük İmtihan", "s.11–12 · +300 akçe", "kale"),
]
ROTA_ARA = {("1", "2"): [(420, 820), (900, 850), (1400, 800), (1680, 660)], ("2", "3"): [(1380, 470), (960, 470)],
            ("3", "4"): [(740, 380)], ("4", "5"): [(940, 470), (1000, 590)], ("5", "H"): [(1300, 740), (1700, 760)],
            ("H", "M"): [(1990, 800)], ("M", "K"): [(1640, 960)], ("K", "A"): [(1290, 880), (1200, 700)],
            ("A", "V"): [(1250, 560)]}
# etiket yerleşiminde yasak alanlar (x0, y0, x1, y1; birim = 0,1 mm): başlık, Van kartı, pusula, Pamuk, yer adları
PANORAMA_YASAK = [(0, 0, 1010, 175), (1460, 14, 2096, 330), (1880, 900, 2100, 1100), (20, 850, 150, 990),
                  (780, 205, 1030, 262), (290, 710, 560, 752), (1840, 700, 2060, 736), (850, 1030, 1220, 1072)]


def bursa_panorama(h=1100):
    s = Svg("iz-pan")
    ufuk = 380
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3F72C8"), (.42, "#8EC0EC"), (.78, "#FFE2BE"), (1, "#FFF2DC")])
    s += S.gunes(s, 150, 300, 46, cekirdek="#FFF8E6", hale="#FFD08A", hale_r=520, guc=.95)
    for (x, y, w_, k) in ((700, 150, 480, 201), (1180, 90, 420, 202)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFFFFF", "#F6CFC4", .6)
    # Uludağ (arkada, karlı) ve ön sırtlar
    d, _ = S.dag(s, 160, 1820, ufuk + 6, 900, 96, 203, renk="#8A98C4", golge="#5F6EA0", bicim="sivri", kar_y=210, kar="#FFFFFF",
                 kar_golge="#C6D2EE", sis="#D6E8F4", isik=-1, sirt=9, puruz=18, kenar_isik="#F6FAFF")
    s += d
    d, _ = S.dag(s, 1100, 2200, ufuk + 6, 1520, 200, 204, renk="#8FA4CA", golge="#6A7EAA", bicim="tepe", kar_y=230, kar="#FFFFFF",
                 kar_golge="#C6D2EE", sis="#D6E8F4", isik=-1, sirt=4, puruz=10)
    s += d
    d, _ = S.dag(s, -120, 700, ufuk + 6, 260, 250, 205, renk="#9AB0D2", golge="#7A92BA", bicim="tepe", sis="#E2F0F8", isik=-1, sirt=2, puruz=6)
    s += d
    gk = s.lin([(0, "#6FAE5A"), (.35, "#9CC86A"), (.7, "#C8D27E"), (1, "#B9CF7A")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kara")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    tb, _ = S.tepe_bandi(s, 160, 1900, ufuk + 60, 70, 206, "#4E8E4C", "#3E7A40", dalga=6)
    s += tb
    s += _orman(s, 220, 1820, ufuk + 40, 90, 207, boy=(30, 50), renk="#2F6B4A", golge="#1C4A33", op=.95)
    r = RNG(208)
    # tarlalar (ova)
    for k in range(90):
        x = r.uniform(0, W)
        y = r.uniform(ufuk + 150, 1000)
        sc = .5 + (y - ufuk) / (h - ufuk)
        w_ = r.uniform(60, 150) * sc
        c = r.choice(["#C9D27A", "#A9C86A", "#D8C878", "#8FBA56", "#E2D48C", "#7FB04E"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w_)} {f(-w_ * .06)} l{f(-w_ * .2)} {f(w_ * .3)} l{f(-w_)} {f(w_ * .06)} Z" fill="{c}" opacity=".6"/>'
    # İznik Gölü (sol önde) + İznik
    gg = s.lin([(0, "#BFE9EC"), (.4, "#3FB2BC"), (1, "#1A7E92")], 0, 640, 0, 800, kull="userSpaceOnUse", ad="izg")
    goly = "M40 690 C120 640 300 632 480 646 C600 656 700 676 720 712 C730 748 640 776 480 788 C320 798 140 790 60 760 C10 742 0 716 40 690 Z"
    s += f'<path d="{goly}" fill="{gg}" stroke="#2A8A9A" stroke-width="3"/>'
    s += f'<path d="M140 720 h80 M300 700 h110 M420 760 h90 M560 720 h70" stroke="#FFFFFF" stroke-width="3" opacity=".7"/>'
    s += sur(s, 70, 260, 690, 26, 209, tas="#E2CCA4", burc_ara=60, harab=.5)
    for k in range(6):
        s += mini_ev(110 + k * 26, 676 - (k % 2) * 8, 20, 14, r.choice(["#F6EEDC", "#F0D9A8", "#FFFFFF"]))
    s += cini_karo(186, 610, 34, 0)
    # Gemlik Körfezi / Marmara (sağ önde) ve kıyı kasabaları
    gd = s.lin([(0, "#7FD0EA"), (1, "#1E6FA8")], 0, 960, 0, h, kull="userSpaceOnUse", ad="dz")
    deniz = f"M740 {h} C780 1040 840 1010 1000 1004 C1200 998 1350 994 1460 992 C1640 988 1820 968 2000 950 L{W + 20} 942 V{h} Z"
    s += f'<path d="{deniz}" fill="{gd}"/>'
    s += f'<path d="M900 1050 h90 M1150 1040 h120 M1500 1030 h100 M1800 1010 h110" stroke="#FFFFFF" stroke-width="3" opacity=".7"/>'
    for (x0, n, cl) in ((1400, 6, ["#FFFFFF", "#F6D8A8", "#CFE2F2"]), (1780, 6, ["#E8D4B0", "#DCC29A"])):
        for k in range(n):
            s += mini_ev(x0 + k * 22, 990 - (k % 2) * 6 - (k * 3 if x0 > 1700 else 0), 18, 13, r.choice(cl), cati="#B04A30")
    s += S.tekne(s, 1240, 1060, 44, govde="#2B50B5", yelken="#FFF1DE") + S.tekne(s, 1640, 1050, 40, govde=MERCAN)
    s += Y.iskele(s, 1440, 1520, 1000, 8, 210, merdiven=False, direk_n=3)
    # Uluabat Gölü ve Gölyazı (sağ)
    gu = s.lin([(0, "#BFE9EC"), (1, "#2A8EA8")], 0, 620, 0, 740, kull="userSpaceOnUse", ad="ulg")
    s += f'<path d="M1760 690 C1800 640 1940 620 2060 630 C2120 636 2140 660 2140 690 C2140 724 2060 740 1960 738 C1860 736 1740 724 1760 690 Z" fill="{gu}" stroke="#2A8A9A" stroke-width="3"/>'
    s += f'<path d="M1880 668 C1900 650 1940 646 1960 656 C1950 672 1920 680 1890 676 Z" fill="#9CB86A"/>'
    for k in range(4):
        s += mini_ev(1892 + k * 16, 668 - (k % 2) * 4, 13, 10, "#F0D9A8", cati="#A8442C")
    s += leylek(2010, 600, .4, ucan=True)
    # Bursa: şehir dokusu, Çekirge buharı, Cumalıkızık renkli evleri, Koza Han, Hisar ve Saat Kulesi
    for k in range(70):
        x = r.uniform(940, 1700)
        y = r.uniform(540, 740)
        if any(math.hypot(x - a_, y - b_) < 60 for (_k, a_, b_, *_r) in DURAKLAR):
            continue
        w_ = r.uniform(18, 28)
        s += mini_ev(x, y, w_, w_ * .66, r.choice(["#F6EEDC", "#F0D9A8", "#EBC9C0", "#FFFFFF", "#E8D4B0"]), cati=r.choice([CATI, "#A8442C", "#C2563A"]))
    for k in range(10):
        s += serv(s, r.uniform(960, 1700), r.uniform(560, 740), r.uniform(34, 52), 211 + k)
    for (bx, by) in ((1610, 500), (1650, 512), (1530, 506)):
        s += buhar(s, bx, by, 70, int(bx), 12, .7)
    for k in range(9):
        s += mini_ev(560 + k * 20, 456 + (k % 3) * 9, 17, 13, EV_RENK[k % len(EV_RENK)], cati="#A8442C")
    s += (f'<g transform="translate(1000 612)"><rect x="0" y="0" width="64" height="30" fill="#EAD7B8" stroke="#5A3A26" stroke-width="2"/>'
          f'<path d="M-4 0 H68 L64 -8 H0 Z" fill="{CATI}"/>' + "".join(f'<path d="M{6 + i * 12} 30 v-12 q4 -6 8 0 v12" fill="#5A3424"/>' for i in range(5))
          + "".join(f'<rect x="{4 + i * 14}" y="-16" width="4" height="9" fill="#E6D2B0" stroke="#5A3A26" stroke-width="1"/>' for i in range(5)) + '</g>')
    s += sur(s, 1240, 1450, 640, 30, 212, tas="#E2CCA4", burc_ara=70)
    kule, _ = saat_kulesi(s, 1300, 612, 82, 213)
    s += kule
    # teleferik: Teferrüç → Sarıalan
    a0, a1 = (1190, 600), (968, 352)
    s += f'<path d="M{a0[0]} {a0[1]} L{a1[0]} {a1[1]}" stroke="#1B1D26" stroke-width="3"/>'
    for t in (.33, .66):
        px, py = a0[0] + (a1[0] - a0[0]) * t, a0[1] + (a1[1] - a0[1]) * t
        s += f'<path d="M{f(px)} {f(py + 4)} v36 M{f(px - 10)} {f(py + 40)} h20" stroke="#3A3F4B" stroke-width="4"/>'
    s += kabin(1060, 600 - (1190 - 1060) * 248 / 222, .32, MERCAN) + kabin(1015, 600 - (1190 - 1015) * 248 / 222, .32, TURKUAZ)
    # ağaç kümeleri (rozetlerden uzak)
    konum = {k: (x, y) for (k, x, y, *_r) in DURAKLAR}
    for k in range(70):
        x = r.uniform(20, 2080)
        y = r.uniform(ufuk + 150, 980)
        if any(math.hypot(x - a_, y - b_) < 100 for a_, b_ in konum.values()):
            continue
        if 30 < x < 740 and 630 < y < 800:
            continue
        sc = .35 + (y - ufuk) / 700 * .9
        if r.random() < .55:
            for j in range(3):
                s += S.kavak(s, x + j * 16 * sc, y, 64 * sc, 12 * sc, 400 + k * 3 + j, renk="#5E9A4A")
        else:
            for j in range(2):
                s += S.agac(s, x + j * 30 * sc, y, 14 * sc, 500 + k * 2 + j, renk=r.choice(["#3E8A3E", "#4E9A44"]))
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
    for (ad_, x, y, fs) in (("Uludağ", 905, 250, 44), ("İznik Gölü", 425, 744, 34), ("Uluabat Gölü", 1950, 730, 28), ("Gemlik Körfezi", 1035, 1064, 32)):
        s += halolu_yazi(f'x="{x}" y="{y}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="{fs}" letter-spacing="1"', ad_, "#FFFFFF", "#1E4E6A", 1.6)
    kart, _ = van_iznik_karti(s, 1478, 22, 590)
    s += kart
    s += '<use href="#pamuk-selam" x="40" y="866" width="96" height="110"/>'
    s += S.marti(1560, 1040, 1.1, 6, ayrintili=True)
    px, py = 1990, h - 120
    s += f'<circle cx="{px}" cy="{py}" r="70" fill="#FFFFFF" opacity=".92" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 62, 13, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 32), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="10" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py + 100}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="28" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), konum
