"""Periyodik Tablo · Maden Yolu I · Batı Anadolu — üniteye özel sahneler, nişan ikonları ve açılış panoraması.

kur_ortak bu modüle {{sahne|ad}} için ortak kütüphaneden ÖNCE bakar. Bantlar 2100×H birim (1 birim = 0,1 mm); sol üst
≈ %55 × %75 levhaya boş, odak sağda, ışık yönü sabit (isik = −1: güneş solda), tohumlar sabit, her Svg öneki benzersiz.
Maden ocakları, tesisler, gemi ve kale TEMSİLÎDİR; kurum logosu yoktur. Konturlu SVG yazısı yok (halolu_yazi).

Sayfa → sahne: 1 maden_panorama · 2 seydisehir · 3 kutahya_cini · 4 gumuskoy · 5 kirka · 6 bandirma · 7 kuscenneti (b40) ·
8 bigadic · 9 emet · 10 germiyan · 11 kale_kutahya (b62) · 12 kale_kapi_kutahya (b30) · 13 ustad_bandi (ortak) ·
14 kutahya_gece (b36) · 15 final_kutahya (kur.py {{final}}).
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim import sahne as S, yapilar as Y
from cizim.sahneler import W, H, _bitir, _cerceve_golge
from cizim.renkler import OBS, ALTIN, MER, KOB, GOL, KEH

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    # boşluk: 3×3 kart ızgarası, ortada kesik çizgili boş kart ve soru işareti (Mendeleyev'in boşluğu)
    "bosluk": "".join(f'<rect x="{6 + j * 13}" y="{6 + i * 13}" width="10" height="10" rx="1.5"/>'
                      for i in range(3) for j in range(3) if (i, j) != (1, 1))
              + '<rect x="19" y="19" width="10" height="10" rx="1.5" stroke-dasharray="2.4 2"/>'
              + '<path d="M22 22.6 Q24 20.4 26 22.4 Q26.6 24 24 25 V26.2"/><circle cx="24" cy="27.6" r=".5"/>'
              + '<path d="M8 44 H40"/>',
    # adres: çini karosu (sekiz köşeli yıldız) üstünde harita iğnesi
    "adres": '<rect x="5" y="15" width="28" height="28" rx="2"/>'
             '<path d="M19 19 L21.8 24.2 L27.6 23.4 L23.6 27.6 L27.6 31.8 L21.8 31 L19 36.2 L16.2 31 L10.4 31.8 L14.4 27.6 L10.4 23.4 L16.2 24.2 Z"/>'
             '<path d="M36 26 C31 19 29 15 29 11 A7 7 0 0 1 43 11 C43 15 41 19 36 26 Z"/><circle cx="36" cy="11" r="2.6"/>',
    # kestirme: dolambaçlı yol ve kısa ok (soy gaz yöntemi)
    "kestirme": '<path d="M6 40 C6 30 20 34 20 24 C20 14 6 18 6 8" stroke-dasharray="3 3"/>'
                '<path d="M6 40 L40 8"/><path d="M31 8 H40 V17"/>'
                '<rect x="27" y="33" width="15" height="7" rx="1.2"/><path d="M29 33 L31 29 H38 L40 33"/>',
    # sınır: tablo ızgarası üstünde merdiven çizgisi
    "sinir": '<path d="M6 8 H42 M6 18 H42 M6 28 H42 M6 38 H42 M6 8 V40 M18 8 V40 M30 8 V40 M42 8 V40"/>'
             '<path d="M18 8 V18 H24 V28 H30 V40" stroke-width="4"/>',
    # dümen: sekiz kollu gemi dümeni (Bandırma limanı) ve ortada + / −
    "dumen": '<circle cx="24" cy="24" r="12"/><circle cx="24" cy="24" r="4.4"/>'
             + "".join(f'<path d="M{f(24 + 4.4 * math.cos(a))} {f(24 + 4.4 * math.sin(a))} L{f(24 + 20 * math.cos(a))} {f(24 + 20 * math.sin(a))}"/>'
                       f'<circle cx="{f(24 + 21 * math.cos(a))}" cy="{f(24 + 21 * math.sin(a))}" r="1.8"/>' for a in [k * math.pi / 4 for k in range(8)]),
}

# ------------------------------------------------------------------ ortak yardımcılar


def _cerceve(s, h=H):
    return _cerceve_golge(s, h)


def _uzak(s, ufuk, tohum, dag, renk, golge, sis, kar=None, kar_oran=.4, kar_golge="#C9D6EA", isik=-1, kenar=None):
    """Uzak sıradağlar: dag = [(sol, sag, tepe_x, tepe_y, biçim), …]."""
    out = ""
    for i, (sol, sag, tx, ty, bicim) in enumerate(dag):
        d, _ = S.dag(s, sol, sag, ufuk, tx, ty, tohum + i, renk=renk, golge=golge, bicim=bicim,
                     kar_y=(ty + (ufuk - ty) * kar_oran) if kar else None, kar=kar or "#FFFFFF", kar_golge=kar_golge,
                     sis=sis, isik=isik, sirt=3, puruz=7, kenar_isik=kenar)
        out += d
    return out


def _zemin(s, x0, x1, y, h, ust, alt, dalga=6, tohum=1, genlik=14):
    tb, _ = S.tepe_bandi(s, x0, x1, y, genlik, tohum, ust, alt, dalga=dalga, olcek=h)
    return tb


def _bozkir_ot(x0, x1, y0, y1, n, tohum, renk="#B08A3E", op=.55):
    r = RNG(tohum)
    o = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        b = r.uniform(5, 12) * (.6 + (y - y0) / max(1, y1 - y0))
        o.append(f'<path d="M{f(x - 3)} {f(y)} l{f(1.5)} {f(-b)} M{f(x)} {f(y)} l0 {f(-b * 1.2)} M{f(x + 3)} {f(y)} l{f(-1.5)} {f(-b)}" stroke="{renk}" stroke-width="1.6" opacity="{f(op, 2)}"/>')
    return "".join(o)


def _tarla(s, x0, x1, y0, y1, tohum, renkler, n=7):
    """Uzak tarla parselleri (eğik bakış): yatay şeritler."""
    r = RNG(tohum)
    o = []
    y = y0
    while y < y1:
        hh = r.uniform(8, 20) * (1 + (y - y0) / max(1, y1 - y0))
        x = x0
        while x < x1:
            w = r.uniform(80, 240)
            o.append(f'<path d="M{f(x)} {f(y)} L{f(x + w)} {f(y + r.uniform(-2, 2))} L{f(x + w + 6)} {f(y + hh)} L{f(x + 4)} {f(y + hh)} Z" fill="{r.choice(renkler)}" opacity=".85"/>')
            x += w + r.uniform(4, 10)
        y += hh + r.uniform(2, 5)
    return "".join(o)


def _basamakli(s, cx, taban, w, h, n, ust, yan, golge, tohum, yol=True, kenar="#FFFFFF", isik=-1):
    """Açık ocak basamakları: kademeli yükselen, üstü açık renkli basamaklar (temsilî)."""
    r = RNG(tohum)
    o = []
    adim = h / n
    for k in range(n):
        y_alt = taban - k * adim
        y_ust = y_alt - adim
        w_alt = w * (1 - k / (n + .6))
        w_ust = w * (1 - (k + 1) / (n + .6))
        sx0, sx1 = cx - w_alt / 2, cx + w_alt / 2
        ux0, ux1 = cx - w_ust / 2 + r.uniform(-4, 4), cx + w_ust / 2 + r.uniform(-4, 4)
        # basamak yüzü (eğimli) + üst düzlük
        g = s.lin([(0, acik(yan, .12)), (1, koyu(yan, .05))], 0, y_ust, 0, y_alt, kull="userSpaceOnUse", ad="bs")
        o.append(f'<path d="M{f(sx0)} {f(y_alt)} L{f(ux0 + adim * .2)} {f(y_ust + adim * .32)} L{f(ux1 - adim * .2)} {f(y_ust + adim * .32)} L{f(sx1)} {f(y_alt)} Z" fill="{g}"/>')
        o.append(f'<path d="M{f(ux0 + adim * .2)} {f(y_ust + adim * .32)} L{f(ux0)} {f(y_ust)} L{f(ux1)} {f(y_ust)} L{f(ux1 - adim * .2)} {f(y_ust + adim * .32)} Z" fill="{ust}"/>')
        # gölge yanı
        gx = cx + (w_alt * .18 if isik < 0 else -w_alt * .5)
        o.append(f'<path d="M{f(gx)} {f(y_alt)} L{f(ux1 - adim * .2 if isik < 0 else ux0 + adim * .2)} {f(y_ust + adim * .32)} '
                 f'L{f(ux1 if isik < 0 else ux0)} {f(y_ust)} L{f(sx1 if isik < 0 else sx0)} {f(y_alt)} Z" fill="{golge}" opacity=".55"/>')
        o.append(f'<path d="M{f(ux0)} {f(y_ust)} H{f(ux1)}" stroke="{kenar}" stroke-width="2.4" opacity=".8"/>')
        # katman çizgileri
        for j in range(2):
            yy = y_ust + adim * (.5 + .22 * j)
            o.append(f'<path d="M{f(sx0 + (ux0 - sx0) * .5)} {f(yy)} H{f(sx1 - (sx1 - ux1) * .5)}" stroke="{koyu(yan, .2)}" stroke-width="1.2" opacity=".35" stroke-dasharray="{r.randint(20, 60)} {r.randint(6, 18)}"/>')
    if yol:
        pts = []
        for k in range(n):
            y = taban - k * adim - adim * .5
            x = cx + (w * (1 - k / (n + .6)) * (.32 if k % 2 == 0 else -.28))
            pts.append((x, y))
        o.append(f'<path d="{cizgi_d(pts)}" stroke="{acik(ust, .3)}" stroke-width="7" fill="none" opacity=".75" stroke-linejoin="round"/>')
    return "".join(o)


def _hol(s, x, y, w, h, duvar="#D9DEE3", cati="#7F8C99", tohum=1, testere=False, pencere="#9FC9DA", isik=-1, gece=False):
    """Fabrika salonu: uzun gövde, çatı (testere dişi ya da beşik), pencere şeridi, kapı."""
    r = RNG(tohum)
    o = []
    g = s.lin([(0, acik(duvar, .15)), (1, koyu(duvar, .08))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="hd")
    o.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{g}" stroke="{OBS}" stroke-width="2"/>')
    if testere:
        n = max(3, int(w / 60))
        dw = w / n
        d = f"M{f(x)} {f(y - h)}"
        for k in range(n):
            d += f" L{f(x + k * dw)} {f(y - h - dw * .45)} L{f(x + (k + 1) * dw)} {f(y - h)}"
        o.append(f'<path d="{d} Z" fill="{cati}" stroke="{OBS}" stroke-width="2" stroke-linejoin="round"/>')
        for k in range(n):
            o.append(f'<path d="M{f(x + k * dw + 3)} {f(y - h - dw * .4)} V{f(y - h - 3)}" stroke="{acik(pencere, .3)}" stroke-width="3"/>')
    else:
        o.append(f'<path d="M{f(x - 6)} {f(y - h)} L{f(x + w * .1)} {f(y - h - h * .22)} H{f(x + w * .9)} L{f(x + w + 6)} {f(y - h)} Z" fill="{cati}" stroke="{OBS}" stroke-width="2" stroke-linejoin="round"/>')
        # çatı havalandırma kapakları
        for k in range(int(w / 70)):
            vx = x + w * .12 + k * 70
            if vx + 30 < x + w * .88:
                o.append(f'<rect x="{f(vx)}" y="{f(y - h - h * .3)}" width="30" height="{f(h * .09)}" fill="{koyu(cati, .2)}" stroke="{OBS}" stroke-width="1.4"/>')
    pc = "#FFD27A" if gece else pencere
    for k in range(int((w - 20) / 26)):
        px = x + 12 + k * 26
        o.append(f'<rect x="{f(px)}" y="{f(y - h * .78)}" width="16" height="{f(h * .2)}" fill="{pc}" stroke="{OBS}" stroke-width="1.1" opacity="{.95 if gece and r.random() < .7 else .9}"/>')
    o.append(f'<rect x="{f(x + w * .62)}" y="{f(y - h * .45)}" width="{f(w * .12)}" height="{f(h * .45)}" fill="{koyu(duvar, .35)}" stroke="{OBS}" stroke-width="1.6"/>')
    gx = x + w * .7 if isik < 0 else x
    o.append(f'<rect x="{f(gx)}" y="{f(y - h)}" width="{f(w * .3)}" height="{f(h)}" fill="#0E2A3A" opacity=".1"/>')
    return "".join(o)


def _silo(s, x, y, w, h, renk="#E6EBEF", serit=None):
    g = s.lin([(0, koyu(renk, .1)), (.35, acik(renk, .4)), (.7, renk), (1, koyu(renk, .3))], x, 0, x + w, 0, kull="userSpaceOnUse", ad="sl")
    o = [f'<path d="M{f(x)} {f(y)} V{f(y - h)} Q{f(x + w / 2)} {f(y - h - w * .45)} {f(x + w)} {f(y - h)} V{f(y)} Z" fill="{g}" stroke="{OBS}" stroke-width="2"/>']
    for k in range(1, 4):
        o.append(f'<path d="M{f(x)} {f(y - h * k / 4)} H{f(x + w)}" stroke="{koyu(renk, .25)}" stroke-width="1.4" opacity=".7"/>')
    if serit:
        o.append(f'<rect x="{f(x)}" y="{f(y - h * .62)}" width="{f(w)}" height="{f(h * .08)}" fill="{serit}"/>')
    return "".join(o)


def _baca(s, x, y, w, h, tohum=1, duman=True, gece=False, serit=True):
    r = RNG(tohum)
    o = [f'<path d="M{f(x - w / 2)} {f(y)} L{f(x - w * .36)} {f(y - h)} H{f(x + w * .36)} L{f(x + w / 2)} {f(y)} Z" fill="#D9DEE3" stroke="{OBS}" stroke-width="2"/>']
    if serit:
        for k in (0, 2):
            yy = y - h + k * h * .07
            o.append(f'<path d="M{f(x - w * .37)} {f(yy)} H{f(x + w * .37)} L{f(x + w * .375)} {f(yy + h * .07)} H{f(x - w * .375)} Z" fill="#C8442F"/>')
    o.append(f'<path d="M{f(x + w * .05)} {f(y)} L{f(x + w * .1)} {f(y - h)} H{f(x + w * .36)} L{f(x + w / 2)} {f(y)} Z" fill="#0E2A3A" opacity=".14"/>')
    if gece:
        o.append(f'<circle cx="{f(x)}" cy="{f(y - h - 6)}" r="6" fill="#FF4A3A"/>')
    if duman:
        for k in range(6):
            rr = w * (.5 + k * .28)
            o.append(f'<circle cx="{f(x + k * w * .55 + r.uniform(-4, 4))}" cy="{f(y - h - 14 - k * w * .5)}" r="{f(rr)}" fill="#FFFFFF" opacity="{f(.6 - k * .08, 2)}"/>')
    return "".join(o)


def _konveyor(s, x0, y0, x1, y1, renk="#4A5560", k=14):
    a = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(a) * k, math.cos(a) * k
    o = [f'<path d="M{f(x0)} {f(y0)} L{f(x1)} {f(y1)} L{f(x1 + nx)} {f(y1 + ny)} L{f(x0 + nx)} {f(y0 + ny)} Z" fill="#E8ECEF" stroke="{renk}" stroke-width="2"/>']
    n = max(3, int(math.hypot(x1 - x0, y1 - y0) / 40))
    for i in range(n + 1):
        t = i / n
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        o.append(f'<path d="M{f(px)} {f(py)} L{f(px + nx)} {f(py + ny)}" stroke="{renk}" stroke-width="1.6"/>')
        if 0 < i < n and i % 2 == 0:
            o.append(f'<path d="M{f(px + nx / 2)} {f(py + ny)} V{f(max(y0, y1) + 30)}" stroke="{renk}" stroke-width="3"/>')
    return "".join(o)


def _kamyon(x, y, o=1.0, kasa="#F0A21A", yuk="#FFFFFF", yon=1):
    """Maden kamyonu (x, y: tekerlek tabanı ortası)."""
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o * yon, 3)} {f(o, 3)})">'
            f'<path d="M-60 -30 L40 -30 L52 -62 L-70 -62 Z" fill="{kasa}" stroke="{OBS}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="M-66 -62 Q-10 -84 48 -62 Z" fill="{yuk}" stroke="{OBS}" stroke-width="1.8"/>'
            f'<rect x="40" y="-52" width="34" height="24" rx="3" fill="{koyu(kasa, .1)}" stroke="{OBS}" stroke-width="2.2"/>'
            f'<rect x="48" y="-48" width="18" height="11" fill="#9FD9E6" stroke="{OBS}" stroke-width="1.4"/>'
            f'<rect x="-64" y="-32" width="140" height="10" fill="#3A3F4B"/>'
            + "".join(f'<circle cx="{cx}" cy="-12" r="15" fill="#2A2E3A" stroke="{OBS}" stroke-width="2"/><circle cx="{cx}" cy="-12" r="6" fill="#B9C3CC"/>' for cx in (-44, 50))
            + "</g>")


def _ekskavator(x, y, o=1.0, renk="#F0A21A", yon=1):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o * yon, 3)} {f(o, 3)})">'
            f'<rect x="-46" y="-16" width="92" height="16" rx="8" fill="#2A2E3A" stroke="{OBS}" stroke-width="2"/>'
            + "".join(f'<circle cx="{cx}" cy="-8" r="5" fill="#8A949E"/>' for cx in (-34, -17, 0, 17, 34))
            + f'<path d="M-36 -16 V-50 H22 L30 -16 Z" fill="{renk}" stroke="{OBS}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<rect x="-30" y="-46" width="22" height="20" fill="#9FD9E6" stroke="{OBS}" stroke-width="1.6"/>'
            f'<path d="M18 -40 L70 -82 L106 -40" stroke="{koyu(renk, .1)}" stroke-width="10" fill="none" stroke-linejoin="round"/>'
            f'<path d="M18 -40 L70 -82 L106 -40" stroke="{OBS}" stroke-width="2" fill="none" stroke-linejoin="round"/>'
            f'<path d="M98 -44 L120 -40 L116 -18 Q100 -14 92 -28 Z" fill="#5A6470" stroke="{OBS}" stroke-width="2"/>'
            f'</g>')


def _yigin(s, x, y, w, h, renk, golge, tohum, kenar=None):
    r = RNG(tohum)
    pts = [(x - w / 2, y)]
    for i in range(1, 10):
        t = i / 10
        pts.append((x - w / 2 + w * t, y - h * math.sin(math.pi * t) ** .8 * r.uniform(.9, 1.05)))
    pts.append((x + w / 2, y))
    o = [f'<path d="{egri_d(pts)} Z" fill="{renk}"/>',
         f'<path d="M{f(x + w * .02)} {f(y - h * .98)} Q{f(x + w * .2)} {f(y - h * .5)} {f(x + w * .16)} {f(y)} L{f(x + w / 2)} {f(y)} Q{f(x + w * .3)} {f(y - h * .6)} {f(x + w * .02)} {f(y - h * .98)} Z" fill="{golge}" opacity=".55"/>']
    if kenar:
        o.append(f'<path d="{egri_d(pts[:6])}" stroke="{kenar}" stroke-width="2" fill="none" opacity=".7"/>')
    return "".join(o)


def _gemi(s, x, y, uz, govde="#1D3A8A", alt="#B23A2E", ust="#F4F1EA", yuk=True, gece=False):
    """Yük gemisi (yandan): gövde, su hattı, kıçta köprü üstü, güvertede büyük torbalar."""
    o_ = uz / 600
    o = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o_, 3)})">',
         f'<path d="M-300 -46 L300 -46 L276 18 L-282 18 Q-300 -10 -300 -46 Z" fill="{govde}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>',
         f'<path d="M-292 0 L284 0 L276 18 L-282 18 Z" fill="{alt}"/>',
         f'<path d="M-296 -38 H296" stroke="#FFFFFF" stroke-width="3" opacity=".7"/>']
    if yuk:
        for k in range(9):
            bx = -230 + k * 40
            for j in range(2 if k % 3 else 1):
                o.append(f'<rect x="{bx}" y="{-46 - 30 * (j + 1)}" width="34" height="28" rx="6" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.8"/>'
                         f'<path d="M{bx + 6} {-46 - 30 * (j + 1)} q11 -10 22 0" stroke="{OBS}" stroke-width="1.6" fill="none"/>')
    o.append(f'<rect x="178" y="-130" width="96" height="84" fill="{ust}" stroke="{OBS}" stroke-width="2.6"/>'
             f'<rect x="196" y="-170" width="62" height="40" fill="{ust}" stroke="{OBS}" stroke-width="2.6"/>')
    pc = "#FFD27A" if gece else "#9FD9E6"
    for k in range(4):
        o.append(f'<rect x="{186 + k * 21}" y="-118" width="14" height="12" fill="{pc}" stroke="{OBS}" stroke-width="1.2"/>')
    o.append(f'<rect x="204" y="-160" width="46" height="12" fill="{pc}" stroke="{OBS}" stroke-width="1.2"/>')
    o.append(f'<rect x="232" y="-214" width="18" height="44" fill="{alt}" stroke="{OBS}" stroke-width="2.4"/>')
    o.append(f'<path d="M-250 -46 V-150 M-250 -140 L-150 -112" stroke="{OBS}" stroke-width="5" stroke-linecap="round"/>')
    o.append("</g>")
    return "".join(o)


def _vinc(s, x, y, h, renk="#F0A21A", yon=-1):
    """Liman vinci: dört ayaklı kule, makine dairesi ve uzun bom."""
    o = [f'<path d="M{f(x - h * .18)} {f(y)} L{f(x - h * .08)} {f(y - h * .62)} M{f(x + h * .18)} {f(y)} L{f(x + h * .08)} {f(y - h * .62)}" stroke="{renk}" stroke-width="{f(h * .045)}" stroke-linecap="round"/>',
         f'<path d="M{f(x - h * .18)} {f(y)} L{f(x - h * .08)} {f(y - h * .62)} M{f(x + h * .18)} {f(y)} L{f(x + h * .08)} {f(y - h * .62)}" stroke="{OBS}" stroke-width="1.6" fill="none"/>']
    for k in range(3):
        yy = y - h * (.15 + k * .17)
        o.append(f'<path d="M{f(x - h * (.16 - k * .03))} {f(yy)} L{f(x + h * (.16 - k * .03))} {f(yy - h * .15)}" stroke="{koyu(renk, .25)}" stroke-width="3"/>')
    o.append(f'<rect x="{f(x - h * .14)}" y="{f(y - h * .8)}" width="{f(h * .28)}" height="{f(h * .18)}" rx="4" fill="{renk}" stroke="{OBS}" stroke-width="2"/>')
    o.append(f'<path d="M{f(x - h * .1 * yon)} {f(y - h * .74)} L{f(x + h * .95 * yon)} {f(y - h * .98)}" stroke="{renk}" stroke-width="{f(h * .05)}" stroke-linecap="round"/>')
    o.append(f'<path d="M{f(x - h * .1 * yon)} {f(y - h * .74)} L{f(x + h * .95 * yon)} {f(y - h * .98)}" stroke="{OBS}" stroke-width="1.6"/>')
    o.append(f'<path d="M{f(x + h * .8 * yon)} {f(y - h * .95)} V{f(y - h * .5)}" stroke="{OBS}" stroke-width="2"/>')
    o.append(f'<rect x="{f(x + h * .8 * yon - 14)}" y="{f(y - h * .5)}" width="28" height="24" rx="5" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.8"/>')
    return "".join(o)


_DESEN = ["yildiz", "lale", "rumi", "yildiz", "karanfil"]


def _karo(x, y, a, desen, mavi="#1E47A8", turkuaz="#16A9A3", mercan="#D9452F"):
    """Tek çini karosu (a: kenar); kobalt mavisi ve bakır turkuazı."""
    cx, cy = x + a / 2, y + a / 2
    o = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(a)}" height="{f(a)}" fill="#F8FBFD" stroke="#9AB0C8" stroke-width="1.2"/>']
    if desen == "yildiz":
        o.append(f'<path d="{cizgi_d(selcuklu_yildizi(cx, cy, a * .42), True)}" fill="{mavi}"/>')
        o.append(f'<path d="{cizgi_d(selcuklu_yildizi(cx, cy, a * .24), True)}" fill="{turkuaz}"/>')
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(a * .07)}" fill="{mercan}"/>')
        for qx, qy in ((x, y), (x + a, y), (x, y + a), (x + a, y + a)):
            o.append(f'<path d="M{f(qx)} {f(qy - a * .16)} L{f(qx + a * .16)} {f(qy)} L{f(qx)} {f(qy + a * .16)} L{f(qx - a * .16)} {f(qy)} Z" fill="{turkuaz}"/>')
    elif desen == "lale":
        o.append(f'<path d="M{f(cx)} {f(y + a * .9)} V{f(y + a * .5)}" stroke="{turkuaz}" stroke-width="{f(a * .05)}"/>')
        o.append(f'<path d="M{f(cx)} {f(y + a * .72)} Q{f(x + a * .2)} {f(y + a * .6)} {f(x + a * .22)} {f(y + a * .82)} Q{f(cx)} {f(y + a * .82)} {f(cx)} {f(y + a * .72)} Z" fill="{turkuaz}"/>')
        o.append(f'<path d="M{f(cx - a * .16)} {f(y + a * .52)} Q{f(cx - a * .2)} {f(y + a * .2)} {f(cx - a * .06)} {f(y + a * .12)} L{f(cx)} {f(y + a * .3)} '
                 f'L{f(cx + a * .06)} {f(y + a * .12)} Q{f(cx + a * .2)} {f(y + a * .2)} {f(cx + a * .16)} {f(y + a * .52)} Z" fill="{mercan}"/>')
        o.append(f'<path d="M{f(x + a * .08)} {f(y + a * .08)} h{f(a * .84)} v{f(a * .84)} h{f(-a * .84)} Z" fill="none" stroke="{mavi}" stroke-width="{f(a * .04)}"/>')
    elif desen == "rumi":
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(a * .38)}" fill="none" stroke="{mavi}" stroke-width="{f(a * .07)}"/>')
        for k in range(4):
            aa = k * math.pi / 2 + math.pi / 4
            px, py = cx + a * .38 * math.cos(aa), cy + a * .38 * math.sin(aa)
            o.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(a * .09)}" fill="{turkuaz}"/>')
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(a * .14)}" fill="{mavi}"/>')
    else:
        for k in range(8):
            aa = k * math.pi / 4
            o.append(f'<ellipse cx="{f(cx + a * .22 * math.cos(aa))}" cy="{f(cy + a * .22 * math.sin(aa))}" rx="{f(a * .14)}" ry="{f(a * .07)}" '
                     f'fill="{mavi if k % 2 else turkuaz}" transform="rotate({f(math.degrees(aa))} {f(cx + a * .22 * math.cos(aa))} {f(cy + a * .22 * math.sin(aa))})"/>')
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(a * .1)}" fill="{mercan}"/>')
    return "".join(o)


def _cini_pano(s, x, y, kol, sira, a, tohum, cerceve="#1D3A8A"):
    r = RNG(tohum)
    o = [f'<rect x="{f(x - a * .18)}" y="{f(y - a * .18)}" width="{f(kol * a + a * .36)}" height="{f(sira * a + a * .36)}" rx="4" fill="{cerceve}" stroke="{OBS}" stroke-width="2.4"/>']
    for i in range(sira):
        for j in range(kol):
            o.append(_karo(x + j * a, y + i * a, a, r.choice(_DESEN)))
    return "".join(o)


def _vazo(s, x, y, h, tohum, govde="#F6F9FC", desen="#1E47A8", desen2="#16A9A3"):
    """Çini vazo (x: orta, y: taban)."""
    r = RNG(tohum)
    w = h * .55
    d = (f"M{f(x - w * .22)} {f(y)} Q{f(x - w * .62)} {f(y - h * .35)} {f(x - w * .48)} {f(y - h * .62)} "
         f"Q{f(x - w * .3)} {f(y - h * .82)} {f(x - w * .18)} {f(y - h * .86)} L{f(x - w * .22)} {f(y - h)} H{f(x + w * .22)} "
         f"L{f(x + w * .18)} {f(y - h * .86)} Q{f(x + w * .3)} {f(y - h * .82)} {f(x + w * .48)} {f(y - h * .62)} "
         f"Q{f(x + w * .62)} {f(y - h * .35)} {f(x + w * .22)} {f(y)} Z")
    g = s.lin([(0, koyu(govde, .12)), (.35, "#FFFFFF"), (1, koyu(govde, .2))], 0, 0, 1, 0, ad="vz")
    o = [f'<path d="{d}" fill="{g}" stroke="{OBS}" stroke-width="2"/>']
    kl = s.klip(f'<path d="{d}"/>', ad="vzk")
    ic = [f'<path d="M{f(x - w)} {f(y - h * .78)} H{f(x + w)}" stroke="{desen}" stroke-width="{f(h * .05)}"/>',
          f'<path d="M{f(x - w)} {f(y - h * .14)} H{f(x + w)}" stroke="{desen}" stroke-width="{f(h * .04)}"/>']
    for k in range(5):
        px = x - w * .4 + k * w * .2
        py = y - h * .45 + r.uniform(-h * .05, h * .05)
        ic.append(f'<path d="M{f(px)} {f(py + h * .14)} Q{f(px - w * .1)} {f(py)} {f(px)} {f(py - h * .14)} Q{f(px + w * .1)} {f(py)} {f(px)} {f(py + h * .14)} Z" fill="{desen if k % 2 else desen2}"/>')
    o.append(f'<g clip-path="{kl}">{"".join(ic)}</g>')
    return "".join(o)


def _firin(s, x, y, w, h, gece=False):
    """Çini fırını: tuğla kubbe, kemerli ağız, içte ateş ışığı (x: sol, y: taban)."""
    g = s.lin([(0, "#C66A45"), (1, "#8A3E26")], 0, y - h, 0, y, kull="userSpaceOnUse", ad="fr")
    o = [f'<path d="M{f(x)} {f(y)} V{f(y - h * .55)} Q{f(x)} {f(y - h)} {f(x + w / 2)} {f(y - h)} Q{f(x + w)} {f(y - h)} {f(x + w)} {f(y - h * .55)} V{f(y)} Z" fill="{g}" stroke="{OBS}" stroke-width="2.4"/>']
    for k in range(5):
        yy = y - h * (.12 + k * .16)
        o.append(f'<path d="M{f(x + 4)} {f(yy)} H{f(x + w - 4)}" stroke="#6E2E1A" stroke-width="1.4" opacity=".6"/>')
    ates = s.rad([(0, "#FFF4C8"), (.45, "#FFB43A"), (1, "#E2533D")], .5, .7, .7, ad="at")
    o.append(f'<path d="M{f(x + w * .3)} {f(y)} V{f(y - h * .35)} Q{f(x + w * .5)} {f(y - h * .55)} {f(x + w * .7)} {f(y - h * .35)} V{f(y)} Z" fill="{ates}" stroke="{OBS}" stroke-width="2"/>')
    hale = s.rad([(0, "#FFC56B", .55), (1, "#FFC56B", 0)], x + w / 2, y - h * .2, w * 1.1, kull="userSpaceOnUse", ad="fh")
    o.append(f'<circle cx="{f(x + w / 2)}" cy="{f(y - h * .2)}" r="{f(w * 1.1)}" fill="{hale}"/>')
    o.append(f'<rect x="{f(x + w * .42)}" y="{f(y - h * 1.18)}" width="{f(w * .16)}" height="{f(h * .24)}" fill="#8A3E26" stroke="{OBS}" stroke-width="2"/>')
    return "".join(o)


def _kutahya_evi(s, x, y, w, h, tohum, duvar="#FBF7EF", tas="#D8C2A0", cati="#B8553A", gece=False, isik=-1):
    """Kütahya evi: taş zemin kat, çıkmalı (cumbalı) ahşap çatkılı beyaz üst kat, kırma kiremit çatı (x: sol, y: taban)."""
    r = RNG(tohum)
    o = []
    zh = h * .38
    o.append(f'<rect x="{f(x)}" y="{f(y - zh)}" width="{f(w)}" height="{f(zh)}" fill="{tas}" stroke="{OBS}" stroke-width="1.6"/>')
    o.append(f'<rect x="{f(x + w * .4)}" y="{f(y - zh * .8)}" width="{f(w * .18)}" height="{f(zh * .8)}" rx="{f(w * .09)}" fill="#6E4422" stroke="{OBS}" stroke-width="1.4"/>')
    cik = w * .06
    ux0, ux1 = x - cik, x + w + cik
    uy0, uy1 = y - h, y - zh
    o.append(f'<path d="M{f(x)} {f(uy1)} L{f(ux0)} {f(uy1 - h * .05)} V{f(uy0)} H{f(ux1)} V{f(uy1 - h * .05)} L{f(x + w)} {f(uy1)} Z" fill="{duvar}" stroke="{OBS}" stroke-width="1.6"/>')
    # ahşap çatkı çizgileri
    for k in range(5):
        px = ux0 + (ux1 - ux0) * k / 4
        o.append(f'<path d="M{f(px)} {f(uy0)} V{f(uy1 - h * .05)}" stroke="#7A4E2E" stroke-width="1.6"/>')
    o.append(f'<path d="M{f(ux0)} {f((uy0 + uy1) / 2)} H{f(ux1)}" stroke="#7A4E2E" stroke-width="1.2" opacity=".7"/>')
    pc = "#FFD27A" if gece else "#9FC0D0"
    for k in range(4):
        px = ux0 + (ux1 - ux0) * (k + .5) / 4 - w * .055
        acik_ = (not gece) or r.random() < .75
        o.append(f'<rect x="{f(px)}" y="{f(uy0 + (uy1 - uy0) * .22)}" width="{f(w * .11)}" height="{f(h * .2)}" fill="{pc if acik_ else "#3A3355"}" stroke="#5A3A22" stroke-width="1.2"/>')
    o.append(f'<path d="M{f(ux0 - w * .08)} {f(uy0)} L{f(x + w * .2)} {f(uy0 - h * .26)} H{f(x + w * .8)} L{f(ux1 + w * .08)} {f(uy0)} Z" fill="{cati}" stroke="{OBS}" stroke-width="1.6" stroke-linejoin="round"/>')
    for k in range(4):
        yy = uy0 - h * .26 * (k + 1) / 5
        o.append(f'<path d="M{f(ux0 - w * .08 + (k + 1) * w * .05)} {f(yy)} H{f(ux1 + w * .08 - (k + 1) * w * .05)}" stroke="{koyu(cati, .25)}" stroke-width="1" opacity=".6"/>')
    gx = ux0 + (ux1 - ux0) * .7 if isik < 0 else ux0
    o.append(f'<rect x="{f(gx)}" y="{f(uy0)}" width="{f((ux1 - ux0) * .3)}" height="{f(h - h * .0)}" fill="#0E2A3A" opacity="{.18 if gece else .08}"/>')
    return "".join(o)


def _kale(s, x0, x1, taban, h, tohum, tas="#C9B48E", tepe="#A9B26A", gece=False, bayrak=True, yikik=True):
    """Kütahya Kalesi (temsilî): şehrin üstünde tepe, sırt boyunca mazgallı sur ve yuvarlak burçlar; bazı burçlar yıkık."""
    r = RNG(tohum)
    o = []
    w = x1 - x0
    # tepe
    pts = [(x0, taban)]
    for i in range(1, 12):
        t = i / 12
        pts.append((x0 + w * t, taban - h * .55 * math.sin(math.pi * t) ** .55 - r.uniform(0, h * .04)))
    pts.append((x1, taban))
    tg = s.lin([(0, acik(tepe, .1)), (1, koyu(tepe, .25))], 0, taban - h * .6, 0, taban, kull="userSpaceOnUse", ad="kt")
    o.append(f'<path d="{egri_d(pts)} Z" fill="{tg}"/>')
    o.append(f'<path d="M{f(x0 + w * .5)} {f(taban - h * .55)} Q{f(x0 + w * .75)} {f(taban - h * .3)} {f(x1)} {f(taban)} L{f(x0 + w * .6)} {f(taban)} Z" fill="#0E2A3A" opacity=".12"/>')
    # sur sırtı
    sy = [(x0 + w * (.12 + .76 * i / 10), taban - h * .55 * math.sin(math.pi * (.12 + .76 * i / 10)) ** .55) for i in range(11)]
    duvar_h = h * .16
    tg2 = s.lin([(0, acik(tas, .15)), (1, koyu(tas, .2))], 0, 0, 0, 1, ad="ks")
    ust = [(x, y - duvar_h) for x, y in sy]
    o.append(f'<path d="{cizgi_d(sy + list(reversed(ust)), True)}" fill="{tg2}" stroke="{OBS}" stroke-width="2"/>')
    for i in range(len(ust) - 1):
        (ax, ay), (bx, by) = ust[i], ust[i + 1]
        for k in range(3):
            t0 = k / 3 + .05
            mx, my = ax + (bx - ax) * t0, ay + (by - ay) * t0
            if not (yikik and i in (3, 7) and k > 0):
                o.append(f'<rect x="{f(mx)}" y="{f(my - duvar_h * .26)}" width="{f((bx - ax) / 7)}" height="{f(duvar_h * .28)}" fill="{tas}" stroke="{OBS}" stroke-width="1.2"/>')
    # yuvarlak burçlar
    for i in (0, 2, 5, 8, 10):
        bx, by = sy[i]
        bw = w * .055
        bh = duvar_h * (1.7 if i in (2, 8) else 1.45)
        kirik = yikik and i == 5
        g = s.lin([(0, acik(tas, .3)), (.45, tas), (1, koyu(tas, .35))], bx - bw / 2, 0, bx + bw / 2, 0, kull="userSpaceOnUse", ad="kb")
        if kirik:
            o.append(f'<path d="M{f(bx - bw / 2)} {f(by + 4)} V{f(by - bh * .7)} L{f(bx - bw * .2)} {f(by - bh * .8)} L{f(bx)} {f(by - bh * .62)} L{f(bx + bw * .25)} {f(by - bh * .74)} L{f(bx + bw / 2)} {f(by - bh * .55)} V{f(by + 4)} Z" fill="{g}" stroke="{OBS}" stroke-width="2"/>')
        else:
            o.append(f'<path d="M{f(bx - bw / 2)} {f(by + 4)} V{f(by - bh)} H{f(bx + bw / 2)} V{f(by + 4)} Z" fill="{g}" stroke="{OBS}" stroke-width="2"/>')
            for k in range(3):
                o.append(f'<rect x="{f(bx - bw / 2 + k * bw * .4)}" y="{f(by - bh - duvar_h * .22)}" width="{f(bw * .2)}" height="{f(duvar_h * .24)}" fill="{tas}" stroke="{OBS}" stroke-width="1.2"/>')
            pc = "#FFD27A" if gece else koyu(tas, .55)
            o.append(f'<rect x="{f(bx - bw * .08)}" y="{f(by - bh * .6)}" width="{f(bw * .16)}" height="{f(bh * .2)}" rx="{f(bw * .08)}" fill="{pc}"/>')
    if bayrak:
        bx, by = sy[8]
        bh = duvar_h * 1.7
        fy = by - bh - duvar_h * .25
        o.append(f'<path d="M{f(bx)} {f(fy)} V{f(fy - h * .3)}" stroke="#3A2E26" stroke-width="{f(max(2, h * .012))}"/>')
        G = h * .1
        o.append(f'<path d="M{f(bx)} {f(fy - h * .3)} q{f(G * .75)} {f(-G * .12)} {f(G * 1.5)} 0 v{f(G)} q{f(-G * .75)} {f(G * .12)} {f(-G * 1.5)} 0 Z" fill="#E30A17" stroke="{OBS}" stroke-width="1.2"/>')
        cx_, cy_ = bx + G * .55, fy - h * .3 + G * .5
        o.append(f'<circle cx="{f(cx_)}" cy="{f(cy_)}" r="{f(G * .25)}" fill="#FFFFFF"/><circle cx="{f(cx_ + G * .07)}" cy="{f(cy_)}" r="{f(G * .2)}" fill="#E30A17"/>')
        o.append(f'<path d="{cizgi_d(yildiz_noktalari(cx_ + G * .38, cy_, G * .11, G * .045, 5, math.pi), True)}" fill="#FFFFFF"/>')
    return "".join(o), sy


def _kulce(x, y, o=1.0):
    """Gümüş külçe yığını (x: orta, y: taban)."""
    out = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">']
    for (dx, dy) in ((-46, 0), (0, 0), (46, 0), (-23, -26), (23, -26), (0, -52)):
        out.append(f'<path d="M{dx - 22} {dy} L{dx - 16} {dy - 24} H{dx + 16} L{dx + 22} {dy} Z" fill="#C9D3DC" stroke="{OBS}" stroke-width="2"/>'
                   f'<path d="M{dx - 16} {dy - 24} H{dx + 16} L{dx + 10} {dy - 18} H{dx - 10} Z" fill="#F4F7F9"/>'
                   f'<path d="M{dx - 12} {dy - 8} H{dx + 4}" stroke="#FFFFFF" stroke-width="2.4" opacity=".9"/>')
    out.append("</g>")
    return "".join(out)


def _balikcil(x, y, o=1.0, renk="#F4F7F9", cizgi=OBS):
    """Ayakta duran balıkçıl (yandan; x, y: ayak ucu)."""
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">'
            f'<path d="M-2 0 L-4 -40 M4 0 L2 -40" stroke="#3A3F4B" stroke-width="2.4"/>'
            f'<path d="M-18 -44 Q-6 -66 14 -60 Q22 -52 12 -42 Q-4 -36 -18 -44 Z" fill="{renk}" stroke="{cizgi}" stroke-width="2"/>'
            f'<path d="M12 -58 Q22 -78 14 -92 Q10 -100 18 -104" stroke="{renk}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path d="M12 -58 Q22 -78 14 -92 Q10 -100 18 -104" stroke="{cizgi}" stroke-width="1.6" fill="none"/>'
            f'<path d="M18 -106 L40 -100 L18 -101 Z" fill="#F0A21A" stroke="{cizgi}" stroke-width="1"/>'
            f'<path d="M14 -106 Q4 -110 -6 -104" stroke="{cizgi}" stroke-width="1.6" fill="none"/>'
            f'<circle cx="19" cy="-104" r="1.6" fill="{cizgi}"/></g>')


def _pelikan(x, y, o=1.0, kanat=0):
    """Uçan pelikan silüeti (beyaz gövde, uçları koyu kanatlar)."""
    k = kanat
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">'
            f'<path d="M-60 {-4 + k} Q-30 {-26 + k} -4 -4 Q-30 {-12 + k * .5} -60 {-4 + k} Z" fill="#F4F7F9" stroke="{OBS}" stroke-width="1.6"/>'
            f'<path d="M60 {-4 + k} Q30 {-26 + k} 4 -4 Q30 {-12 + k * .5} 60 {-4 + k} Z" fill="#F4F7F9" stroke="{OBS}" stroke-width="1.6"/>'
            f'<path d="M-60 {-4 + k} Q-50 {-12 + k} -42 {-12 + k} L-48 {-4 + k} Z M60 {-4 + k} Q50 {-12 + k} 42 {-12 + k} L48 {-4 + k} Z" fill="#2A2E3A"/>'
            f'<ellipse cx="0" cy="0" rx="20" ry="8" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6"/>'
            f'<path d="M18 -2 Q30 -6 32 -2 L58 2 L32 4 Q24 6 18 2 Z" fill="#F2C230" stroke="{OBS}" stroke-width="1.2"/></g>')


def _zeytin(s, x, y, r0, tohum):
    return S.agac(s, x, y, r0, tohum, renk="#8FA86A", golge="#5E7448", gov="#6B5236")


def _ardic(s, x, y, h, tohum, renk="#3F6B45"):
    """Toros ardıcı / karaçam (koni)."""
    r = RNG(tohum)
    w = h * .42
    pts = [(x - w / 2, y - h * .1)]
    for i in range(1, 8):
        t = i / 8
        pts.append((x - w / 2 * (1 - t) + r.uniform(-w * .05, w * .05), y - h * .1 - h * .9 * t))
    pts.append((x, y - h))
    for i in range(1, 8):
        t = 1 - i / 8
        pts.append((x + w / 2 * (1 - t) + r.uniform(-w * .05, w * .05), y - h * .1 - h * .9 * t))
    pts.append((x + w / 2, y - h * .1))
    g = s.lin([(0, acik(renk, .25)), (1, koyu(renk, .3))], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="ar")
    return (f'<path d="M{f(x - 3)} {f(y)} V{f(y - h * .14)} H{f(x + 3)} V{f(y)} Z" fill="#5A3E26"/>'
            f'<path d="{cizgi_d(pts, True)}" fill="{g}"/>')


def _koy(s, x0, x1, y, n, tohum, duvar=("#EFE2C8", "#E6D2B0", "#F4EBDD"), cati=("#B8553A", "#C46A44", "#A84A32"), o=1.0):
    r = RNG(tohum)
    out = []
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(1, n - 1) + r.uniform(-8, 8)
        out.append(S.ev(x, y + r.uniform(-6, 6), 34 * o, 22 * o, tohum * 7 + i, duvar=r.choice(duvar), cati=r.choice(cati)))
    return "".join(out)


def _isik_huzmesi(s, gx, gy, n, renk="#FFF0D0", op=.08, uz=2400):
    o = []
    for k in range(n):
        a0 = math.pi + .1 + k * (math.pi - .2) / n
        a1 = a0 + .05
        o.append(f'<path d="M{gx} {gy} L{f(gx + uz * math.cos(a0))} {f(gy + uz * math.sin(a0))} L{f(gx + uz * math.cos(a1))} {f(gy + uz * math.sin(a1))} Z" fill="{renk}" opacity="{op}"/>')
    return "".join(o)


def _pamuk(x, y, w, poz="pamuk-otur"):
    """Pamuk sembolü (viewBox 140×160); (x, y) sol üst."""
    return f'<use href="#{poz}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(w * 160 / 140)}"/>'


# ================================================================== 1. DURAK · SEYDİŞEHİR (sabah) · alüminyum

def seydisehir():
    s = Svg("pt-sey")
    ufuk = 272
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    s += S.gunes(s, 520, 190, 40, cekirdek="#FFF9E8", hale="#FFD3A0", hale_r=480, guc=.9)
    s += S.bulut_serit(s, 860, 120, 520, 12, "#FFE3EA", "#F4B8C8", .6)
    s += S.bulut(s, 1500, 80, 230, 3, ust="#FFFFFF", alt="#F8CDD8", op=.9)
    s += S.bulut(s, 1880, 140, 170, 5, ust="#FFFFFF", alt="#F6D2C8", op=.85)
    # Toros sıradağları (kireçtaşı: mavimsi gri, tepeler hafif karlı)
    s += _uzak(s, ufuk, 11, [(820, 1700, 1260, 118, "sivri"), (1450, 2250, 1860, 96, "sivri"), (-80, 900, 300, 170, "tepe")],
               "#9AA7C8", "#7381A8", "#F2C9D6", kar="#FFFFFF", kar_oran=.22, kar_golge="#D6D6EE", kenar="#FFE7D8")
    s += _zemin(s, 0, W, ufuk + 26, 260, "#B8B27A", "#8C9858", dalga=5, tohum=12, genlik=18)
    s += _tarla(s, 0, 1200, ufuk + 30, ufuk + 92, 13, ["#C7B97A", "#B5B06E", "#D4C58C", "#A9A868"])
    for i in range(14):
        s += _ardic(s, 80 + i * 70 + (i % 3) * 14, ufuk + 40 + (i % 2) * 8, 46 + (i % 3) * 10, 14 + i)
    # tesis: elektroliz salonları (uzun), alümina siloları, baca, boksit yığını
    taban = 392
    s += _yigin(s, 1330, taban + 6, 300, 84, "#B5482E", "#7E2E1C", 15, kenar="#D9714E")
    s += _yigin(s, 1180, taban + 10, 170, 50, "#C25A38", "#8A3420", 16)
    s += _konveyor(s, 1360, taban - 70, 1560, taban - 200)
    for k in range(3):
        s += _silo(s, 1560 + k * 74, taban - 30, 64, 190, "#F2F4F6", serit="#C8442F" if k == 1 else None)
    s += _baca(s, 1790, taban - 30, 46, 290, 17)
    s += _hol(s, 1500, taban, 600, 118, "#E2E6EA", "#6E7C8A", 18)
    s += _hol(s, 1830, taban - 4, 320, 150, "#D5DBE0", "#5E6C7A", 19, testere=True)
    s += _kamyon(1190, taban + 46, .72, kasa="#E2E6EA", yuk="#B5482E", yon=-1)
    for i, x in enumerate((1440, 1470, 2060)):
        s += S.kavak(s, x, taban + 6, 120 + i * 14, 24, 20 + i, renk="#5E9A4A")
    # yol
    s += f'<path d="M0 446 C500 430 900 448 1300 432 S1900 440 2100 430 V{H} H0 Z" fill="#8C8070"/>'
    s += f'<path d="M0 452 C500 436 900 454 1300 438 S1900 446 2100 436" stroke="#F4E9D8" stroke-width="3" stroke-dasharray="26 18" fill="none"/>'
    s += _pamuk(1395, 346, 70, "pamuk-selam")
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== 2. DURAK · KÜTAHYA ÇİNİ ATÖLYESİ (öğle)

def kutahya_cini():
    s = Svg("pt-cin")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 300, 120, 36, hale="#FFF0B8", hale_r=420, guc=.75)
    for i, (x, y, w) in enumerate([(700, 110, 240), (1080, 70, 300), (1460, 120, 200)]):
        s += S.bulut(s, x, y, w, 30 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    s += _uzak(s, ufuk, 31, [(-60, 760, 260, 150, "tepe"), (600, 1500, 1000, 130, "tepe"), (1300, 2200, 1800, 120, "tepe")],
               "#8FB0C8", "#6C90B0", "#D6ECF5")
    s += _zemin(s, 0, W, ufuk + 22, 240, "#A9C46E", "#7EA453", dalga=6, tohum=32, genlik=16)
    # şehir: yamaçta Kütahya evleri, tepede (uzakta) kale silüeti
    kale, _ = _kale(s, 980, 1420, ufuk + 26, 150, 33, tas="#CDBB98", tepe="#9DB46A", bayrak=False)
    s += kale
    for i in range(9):
        s += _kutahya_evi(s, 120 + i * 96, ufuk + 70 + (i % 2) * 6, 70, 56, 34 + i)
    # atölye zemini (ön plan) + çini panoları + fırın + vazolar
    g = s.lin([(0, "#E9D9BE"), (1, "#C9B08A")], 0, 330, 0, H, kull="userSpaceOnUse", ad="az")
    s += f'<path d="M1080 {H} L1160 340 H2100 V{H} Z" fill="{g}"/>'
    s += f'<rect x="1180" y="120" width="920" height="232" fill="#F2E8D8" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M1160 122 H2100" stroke="#8A5A3A" stroke-width="10"/>'
    s += _cini_pano(s, 1236, 150, 6, 3, 52, 35)
    s += _cini_pano(s, 1640, 150, 4, 3, 52, 36, cerceve="#0A6C74")
    s += _firin(s, 1930, 352, 150, 190)
    for i, (x, h_, d1, d2) in enumerate(((1240, 120, "#1E47A8", "#16A9A3"), (1330, 90, "#16A9A3", "#1E47A8"), (1410, 132, "#1E47A8", "#D9452F"), (1500, 96, "#1E47A8", "#16A9A3"))):
        s += _vazo(s, x, 420 - (i % 2) * 4, h_, 37 + i, desen=d1, desen2=d2)
    # çalışma masası: boya kâseleri (kobalt mavisi, bakır turkuazı)
    s += f'<rect x="1590" y="372" width="300" height="20" rx="4" fill="#A8744A" stroke="{OBS}" stroke-width="2"/><path d="M1610 392 V440 M1870 392 V440" stroke="#7A4E2E" stroke-width="10"/>'
    for k, (c, ad) in enumerate((("#1E47A8", "Co"), ("#16A9A3", "Cu"), ("#D9452F", "Fe"))):
        x = 1640 + k * 90
        s += f'<path d="M{x - 30} 372 Q{x} 404 {x + 30} 372 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="2"/><ellipse cx="{x}" cy="372" rx="30" ry="7" fill="{c}" stroke="{OBS}" stroke-width="1.6"/>'
        s += halolu_yazi(f'x="{x}" y="364" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="26"', ad, OBS, "#FFFFFF", 2.2)
    s += _pamuk(1880, 262, 92, "pamuk-dusunen")
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== 3. DURAK · GÜMÜŞKÖY (ikindi) · gümüş

def gumuskoy():
    s = Svg("pt-gum")
    ufuk = 276
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "altin")
    s += S.gunes(s, 420, 210, 44, hale="#FFC97A", hale_r=520, guc=.9)
    s += S.bulut_serit(s, 700, 150, 520, 12, "#FFE9C8", "#F7B88E", .55)
    s += S.bulut(s, 1450, 90, 260, 41, ust="#FFFFFF", alt="#F6D2B8", op=.9)
    s += _uzak(s, ufuk, 42, [(-80, 900, 360, 150, "tepe"), (700, 1700, 1250, 120, "tepe"), (1500, 2250, 1900, 140, "tepe")],
               "#A99BBE", "#8579A6", "#F4CDBE")
    s += _zemin(s, 0, W, ufuk + 22, 250, "#C9B776", "#9C9A5C", dalga=6, tohum=43, genlik=16)
    s += _tarla(s, 0, 1150, ufuk + 26, ufuk + 80, 44, ["#D2C07E", "#BFB46C", "#E0CF96", "#B2AA66"])
    s += _koy(s, 120, 980, ufuk + 72, 10, 45)
    for i in range(7):
        s += S.kavak(s, 260 + i * 120, ufuk + 76, 90 + (i % 3) * 16, 20, 46 + i, renk="#6E9C48")
    # gümüş grisi ocak basamakları + tesis + eski cüruf yığınları (koyu)
    s += _basamakli(s, 1520, 392, 760, 220, 6, "#E3E8EC", "#A9B4BE", "#6F7C88", 47, kenar="#FFFFFF")
    s += _yigin(s, 1170, 404, 220, 46, "#4A4650", "#2E2B33", 48)
    s += _yigin(s, 1300, 410, 160, 30, "#55505C", "#35313A", 49)
    s += _hol(s, 1820, 404, 280, 120, "#D5DBE0", "#5E6C7A", 50, testere=True)
    s += _silo(s, 1760, 404, 56, 150, "#EEF1F4")
    s += _konveyor(s, 1620, 300, 1770, 250)
    s += _kamyon(1430, 392 - 220 * 2 / 6 + 4, .5, kasa="#F0A21A", yuk="#B9C3CC")
    s += _ekskavator(1300, 392 - 220 * 1 / 6 + 2, .55, yon=1)
    s += _kulce(2000, 436, .9)
    s += f'<path d="M0 448 C600 436 1200 452 2100 440 V{H} H0 Z" fill="#9B8A6E"/>'
    s += _pamuk(1880, 330, 64, "pamuk-akce")
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== 4. DURAK · KIRKA (sabah) · beyaz bor tepeleri

def kirka():
    s = Svg("pt-krk")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2F86D6"), (.55, "#86C8EE"), (1, "#E6F5FB")])
    s += S.gunes(s, 360, 110, 38, hale="#FFF4C8", hale_r=460, guc=.8)
    for i, (x, y, w) in enumerate([(820, 90, 260), (1240, 60, 320), (1700, 110, 220)]):
        s += S.bulut(s, x, y, w, 50 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    s += _uzak(s, ufuk, 51, [(-60, 800, 300, 170, "tepe"), (600, 1400, 1000, 160, "tepe"), (1200, 2200, 1700, 150, "tepe")],
               "#A8B9A0", "#869A80", "#E2F0F0")
    s += _zemin(s, 0, W, ufuk + 20, 260, "#D8C48A", "#B49E62", dalga=5, tohum=52, genlik=14)
    s += _bozkir_ot(0, 1100, ufuk + 40, H - 20, 160, 53)
    # beyaz tinkal basamakları (büyük) + ikinci tepe
    s += _basamakli(s, 1560, 410, 1000, 300, 7, "#FFFFFF", "#E4ECF2", "#A9BCCD", 54, kenar="#FFFFFF")
    s += _basamakli(s, 1080, 396, 380, 110, 4, "#FBFCFD", "#E1E9EF", "#B2C3D2", 55, yol=False)
    s += _kamyon(1480, 410 - 300 * 3 / 7 + 2, .62, kasa="#F0A21A", yuk="#FFFFFF")
    s += _kamyon(1740, 410 - 300 * 1 / 7 + 2, .7, kasa="#E2533D", yuk="#FFFFFF", yon=-1)
    s += _ekskavator(1660, 410 - 300 * 5 / 7 + 2, .5, yon=-1)
    # zenginleştirme tesisi ve silolar (sağ)
    s += _konveyor(s, 1860, 330, 1990, 250)
    s += _silo(s, 1960, 410, 60, 170, "#F2F4F6", serit="#2B50B5")
    s += _silo(s, 2030, 410, 60, 150, "#F2F4F6")
    s += f'<path d="M0 446 C700 436 1300 450 2100 440 V{H} H0 Z" fill="#B9A274"/>'
    s += _pamuk(1290, 330, 66, "pamuk-sasiran")
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== 5. DURAK · BANDIRMA (akşam) · liman ve bor tesisi

def bandirma():
    s = Svg("pt-ban")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gunbatimi")
    gx, gy = 700, ufuk - 26
    s += _isik_huzmesi(s, gx, gy, 12, "#FFE0A0", .1)
    s += S.gunes(s, gx, gy, 52, hale="#FFC56B", hale_r=620, guc=.95)
    for (x, y, w, k) in ((300, 130, 520, 18), (1160, 90, 600, 22), (1560, 200, 420, 14)):
        s += S.bulut_serit(s, x, y, w, k, "#FFC59A", "#FF6F8A", .7)
    uzak = _uzak(s, ufuk, 61, [(-80, 600, 200, 220, "tepe"), (1400, 2250, 1900, 200, "tepe")], "#7E5A8E", "#5E3E74", "#F28E8A")
    s += uzak
    s += S.gol(s, 0, ufuk, W, H - ufuk, 62, ufuk="#FFB59A", orta="#3F8FA0", derin="#123E5A", gunes_x=gx, parilti_renk="#FFE0A0", yogunluk=1.1)
    s += S.yansima(s, uzak, ufuk, 0, W, 120, op=.25)
    # sağ kıyı: tesis (silolar, tanklar, beyaz yığınlar), rıhtım, vinçler, gemi
    g = s.lin([(0, "#8E7A86"), (1, "#5A4A5E")], 0, 300, 0, H, kull="userSpaceOnUse", ad="ky")
    s += f'<path d="M1240 {H} L1270 352 H2100 V{H} Z" fill="{g}"/>'
    s += f'<rect x="1260" y="352" width="840" height="16" fill="#C9C2C8" stroke="{OBS}" stroke-width="2"/>'
    s += _yigin(s, 1980, 352, 220, 70, "#FFFFFF", "#C9C4D8", 63)
    for k in range(3):
        s += _silo(s, 1700 + k * 70, 352, 60, 176, "#ECEFF2", serit="#2B50B5" if k == 0 else None)
    s += _hol(s, 1880, 352, 220, 96, "#DDE2E6", "#6E7C8A", 64, gece=True)
    s += f'<rect x="1600" y="300" width="80" height="52" rx="26" fill="#E6EAEE" stroke="{OBS}" stroke-width="2"/>'
    s += _baca(s, 1660, 300, 30, 150, 65, duman=True, gece=True)
    s += _vinc(s, 1420, 352, 230, yon=-1)
    s += _vinc(s, 1560, 352, 200, renk="#13A3A6", yon=-1)
    gemi = _gemi(s, 1180, 382, 520, gece=True)
    s += S.yansima(s, gemi, 384, 900, 600, 70, op=.25)
    s += gemi
    for k, (x, y, o) in enumerate([(560, 170, 1.2), (630, 210, .9), (1000, 120, .8), (1080, 150, .6)]):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    s += _pamuk(1960, 228, 66, "pamuk-selam")
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== HÜLASA · KUŞCENNETİ (Manyas Gölü, şafak) · b40

def kuscenneti(h=400):
    s = Svg("pt-kus")
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    s += S.gunes(s, 1640, ufuk - 30, 46, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=520, guc=.95)
    s += S.bulut_serit(s, 700, 120, 560, 12, "#FFE3EA", "#F6B8C8", .6)
    s += S.bulut_serit(s, 1300, 70, 500, 10, "#FFE9D6", "#F6B0C4", .5)
    uzak = _uzak(s, ufuk, 71, [(-80, 700, 260, 170, "tepe"), (500, 1300, 900, 180, "tepe"), (1500, 2250, 1950, 170, "tepe")],
                 "#A99BCB", "#8E83B8", "#F2CFE0")
    s += uzak
    s += S.gol(s, 0, ufuk, W, h - ufuk, 72, ufuk="#FBD9CF", orta="#56C2C0", derin="#0E7480", gunes_x=1640, parilti_renk="#FFF1C4", yogunluk=1.2)
    s += S.yansima(s, uzak, ufuk, 0, W, 120, op=.28)
    # sazlık ve söğütler (ön plan, sağ)
    s += f'<path d="M1100 {h} Q1300 330 1600 320 T2100 300 V{h} Z" fill="#5E8A44"/>'
    s += S.sazlik(1120, 2100, h - 6, 73, renk="#4F7A36", bas="#7A4E2A", boy=70)
    for i, (x, r0) in enumerate(((1640, 46), (1760, 56), (1990, 50))):
        s += S.agac(s, x, 330, r0, 74 + i, renk="#7DAE5A")
    for i, (x, o) in enumerate(((1380, 1.1), (1500, .9), (1870, 1.0))):
        s += _balikcil(x, 352 + i * 4, o, renk="#F4F7F9" if i != 1 else "#AAB6C2")
    for k, (x, y, o, kn) in enumerate(((1250, 110, 1.0, 4), (1420, 150, .8, -4), (1560, 90, .7, 6), (1720, 140, .6, 0))):
        s += _pelikan(x, y, o, kn)
    s += S.sazlik(0, 600, h - 4, 75, renk="#5C7F3A", boy=46)
    s += _cerceve(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== YAN YOL 1 · BİGADİÇ (öğle) · maden kampında meclis

def bigadic():
    s = Svg("pt-big")
    ufuk = 268
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 260, 110, 36, hale="#FFF0B8", hale_r=420, guc=.75)
    for i, (x, y, w) in enumerate([(760, 100, 260), (1200, 70, 300), (1650, 120, 220)]):
        s += S.bulut(s, x, y, w, 80 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    s += _uzak(s, ufuk, 81, [(-60, 820, 340, 140, "tepe"), (700, 1500, 1100, 120, "tepe"), (1350, 2250, 1800, 150, "tepe")],
               "#86A8B8", "#668AA0", "#D6ECF5")
    s += _zemin(s, 0, W, ufuk + 22, 250, "#AFC277", "#7EA453", dalga=6, tohum=82, genlik=16)
    for i in range(12):
        s += _zeytin(s, 90 + i * 86, ufuk + 76 + (i % 2) * 10, 22 + (i % 3) * 4, 83 + i)
    # beyaz-gri kolemanit basamakları
    s += _basamakli(s, 1560, 400, 820, 230, 6, "#FBFAF6", "#DCD8CE", "#A8A296", 84)
    s += _kamyon(1450, 400 - 230 * 2 / 6 + 2, .55, kasa="#F0A21A", yuk="#FFFFFF")
    # maden kampı: çardak, masa, semaver, çay
    s += f'<path d="M1080 {H} L1120 380 H2100 V{H} Z" fill="#C9B48A"/>'
    s += f'<path d="M1720 250 L2080 230 L2100 250 L1740 272 Z" fill="#C8442F" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M1740 272 V420 M2080 252 V420" stroke="#6B4A2E" stroke-width="10"/>'
    s += f'<rect x="1780" y="372" width="260" height="18" rx="4" fill="#A8744A" stroke="{OBS}" stroke-width="2"/><path d="M1800 390 V430 M2020 390 V430" stroke="#7A4E2E" stroke-width="9"/>'
    s += Y.semaver(s, 1990, 372, 90)
    for k in range(4):
        s += Y.cay_bardak_kucuk(1820 + k * 36, 372, 30)
    s += '<use href="#yusuf-anlatan" x="1300" y="276" width="160" height="168"/>'
    s += _pamuk(1880, 300, 62, "pamuk-dusunen")
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== YAN YOL 2 · EMET (ikindi) · kolemanit ve kasaba

def emet():
    s = Svg("pt-emt")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "altin")
    s += S.gunes(s, 1820, 190, 40, hale="#FFC97A", hale_r=480, guc=.9)
    s += S.bulut_serit(s, 500, 140, 560, 12, "#FFE9C8", "#F7B88E", .55)
    s += S.bulut(s, 1250, 80, 240, 91, ust="#FFFFFF", alt="#F6D2B8", op=.9)
    s += _uzak(s, ufuk, 92, [(-80, 820, 330, 150, "tepe"), (650, 1550, 1100, 130, "sivri"), (1450, 2250, 1850, 150, "tepe")],
               "#A99BBE", "#8579A6", "#F4CDBE", isik=1)
    s += _zemin(s, 0, W, ufuk + 22, 250, "#C2BE7C", "#959A5C", dalga=6, tohum=93, genlik=16)
    s += _tarla(s, 0, 1000, ufuk + 28, ufuk + 84, 94, ["#D2C07E", "#BFB46C", "#E0CF96", "#9FB066"])
    for i in range(10):
        s += _kutahya_evi(s, 140 + i * 84, ufuk + 86 + (i % 2) * 8, 60, 46, 95 + i, isik=1)
    for i in range(6):
        s += S.kavak(s, 120 + i * 170, ufuk + 92, 100 + (i % 3) * 12, 20, 105 + i, renk="#6E9C48", isik=1)
    s += _basamakli(s, 1600, 404, 820, 250, 6, "#FBFAF6", "#D9D4C8", "#A49C8E", 96, isik=1)
    s += _kamyon(1700, 404 - 250 * 2 / 6 + 2, .55, kasa="#E2533D", yuk="#FFFFFF", yon=-1)
    s += _ekskavator(1480, 404 - 250 * 3 / 6 + 2, .45)
    s += f'<path d="M0 446 C700 434 1300 450 2100 438 V{H} H0 Z" fill="#A89A72"/>'
    s += '<use href="#elif-dusunen" x="1300" y="284" width="150" height="158"/>'
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== YAN YOL 3 · GERMİYAN SOKAĞI (akşam) · basamaklı sokak

def germiyan():
    s = Svg("pt-ger")
    s += S.gokyuzu(s, 0, 0, W, H, "alaca")
    s += S.yildizlar(s, 0, 0, W, 160, 60, 101)
    s += S.ay(s, 980, 70, 26, golge_renk="#3B2E6E")
    kale, _ = _kale(s, 1300, 2160, 250, 260, 102, tas="#8E7E9A", tepe="#4E4A72", gece=True, bayrak=True)
    s += kale
    # basamaklı sokak: arnavut kaldırımı ve taş merdiven sağa doğru yükselir
    g = s.lin([(0, "#7A6A88"), (1, "#4A3E5A")], 0, 300, 0, H, kull="userSpaceOnUse", ad="sk")
    s += f'<path d="M0 {H} L0 420 C600 410 1100 380 1500 330 L2100 290 V{H} Z" fill="{g}"/>'
    for k in range(9):
        x = 1300 + k * 70
        y = 360 - k * 8
        s += f'<path d="M{x} {y + 50} V{y} H{x + 70} V{y + 50}" fill="#9A8AA8" stroke="#2E2440" stroke-width="1.6"/>'
    for i in range(7):
        x = 1180 + i * 132
        y = 350 - i * 10
        s += _kutahya_evi(s, x, y, 104, 120 + (i % 2) * 14, 103 + i, duvar="#E9DFEF", tas="#A898B8", cati="#9A4A3A", gece=True)
    for i in range(6):
        x = 60 + i * 150
        s += _kutahya_evi(s, x, 432 - i * 4, 96, 104, 120 + i, duvar="#E4DAEA", tas="#9C8CAE", cati="#8E4434", gece=True)
    # sokak fenerleri
    for x, y in ((1150, 360), (1580, 310), (1980, 270)):
        s += f'<path d="M{x} {y + 70} V{y}" stroke="#2A2030" stroke-width="5"/><rect x="{x - 10}" y="{y - 24}" width="20" height="26" rx="4" fill="#FFD27A" stroke="#2A2030" stroke-width="2"/>'
        hale = s.rad([(0, "#FFD27A", .5), (1, "#FFD27A", 0)], x, y - 12, 90, kull="userSpaceOnUse", ad="fn")
        s += f'<circle cx="{x}" cy="{y - 12}" r="90" fill="{hale}"/>'
    s += _pamuk(1720, 238, 56, "pamuk-selam")
    s += _cerceve(s)
    return _bitir(s)


# ================================================================== BÜYÜK İMTİHAN 1 · KÜTAHYA KALESİ (gün batımı) · b62

def kale_kutahya(h=620):
    s = Svg("pt-kal")
    ufuk = 430
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2F5DA8"), (.38, "#86A9D6"), (.7, "#F6C99A"), (1, "#FFB46B")])
    s += S.gunes(s, 300, 340, 50, hale="#FFB45A", hale_r=520, guc=.95)
    for i, (x, y, w) in enumerate([(560, 150, 300), (980, 96, 340), (1500, 120, 280), (1880, 70, 220)]):
        s += S.bulut(s, x, y, w, 130 + i, ust="#FFF4E4", alt="#F0A98A", op=.95)
    s += S.bulut_serit(s, 300, 260, 600, 16, "#FFD8B0", "#F08A7A", .6)
    s += _uzak(s, ufuk, 131, [(-80, 900, 360, 290, "tepe"), (700, 1500, 1100, 300, "tepe")], "#B08AA8", "#7A5888", "#F4B8A0")
    kale, _ = _kale(s, 960, 2180, 520, 480, 132, tas="#CDB894", tepe="#8EA060", bayrak=True)
    s += kale
    s += _zemin(s, 0, W, 520, 200, "#8C9C5A", "#5E7040", dalga=7, tohum=133, genlik=10)
    for i in range(16):
        s += _kutahya_evi(s, 40 + i * 128, 600 - (i % 3) * 8, 92, 86, 134 + i)
    for i, x in enumerate((900, 980, 1040)):
        s += S.kavak(s, x, 560, 150 + i * 20, 26, 150 + i, renk="#4E8A3E")
    for k, (x, y, o) in enumerate([(820, 200, 1.0), (900, 230, .7), (1300, 110, .6)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += _cerceve(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== BÜYÜK İMTİHAN 2 · KALE KAPISI (b30)

def kale_kapi_kutahya(h=300):
    s = Svg("pt-kap")
    s += S.gokyuzu(s, 0, 0, W, h, duraklar=[(0, "#F7B07A"), (1, "#FFE1B0")])
    g = s.lin([(0, "#D2BE98"), (1, "#9C8664")], 0, 40, 0, h, kull="userSpaceOnUse", ad="sd")
    s += f'<rect x="0" y="60" width="{W}" height="{h - 60}" fill="{g}"/>'
    r = RNG(140)
    for row in range(8):
        y = 60 + row * 32
        off = 0 if row % 2 == 0 else 40
        for x in range(-40 + off, W, 80):
            s += f'<rect x="{x + 2}" y="{y + 2}" width="76" height="28" rx="4" fill="{karis("#D2BE98", "#A48E6A", r.uniform(0, .7))}" stroke="#6E5A40" stroke-width="1.6"/>'
    for x in range(0, W, 110):
        s += f'<rect x="{x}" y="20" width="70" height="44" fill="#C4AE88" stroke="#6E5A40" stroke-width="2.4"/>'
    cx = 1450
    for bx in (cx - 300, cx + 300):
        s += f'<rect x="{bx - 90}" y="0" width="180" height="{h}" fill="#C9B48E" stroke="#6E5A40" stroke-width="3"/>'
        for k in range(3):
            s += f'<rect x="{bx - 90 + k * 70}" y="-6" width="40" height="30" fill="#C9B48E" stroke="#6E5A40" stroke-width="2.4"/>'
        s += f'<rect x="{bx - 12}" y="110" width="24" height="44" rx="12" fill="#3A2A1E"/>'
    s += f'<path d="M{cx - 170} {h} V140 Q{cx - 170} 70 {cx} 52 Q{cx + 170} 70 {cx + 170} 140 V{h} Z" fill="#8E7A5A"/>'
    s += f'<path d="M{cx - 140} {h} V146 Q{cx - 140} 92 {cx} 78 Q{cx + 140} 92 {cx + 140} 146 V{h} Z" fill="#1E1A16"/>'
    isik = s.rad([(0, "#FFF4C8", .95), (.5, "#FFD27A", .5), (1, "#FFD27A", 0)], cx, 200, 260, kull="userSpaceOnUse", ad="ki")
    s += f'<path d="M{cx - 30} {h} V96 L{cx + 30} 96 V{h} Z" fill="#FFE9A8"/>'
    s += f'<circle cx="{cx}" cy="200" r="260" fill="{isik}"/>'
    for sx in (-1, 1):
        x0, x1 = cx + sx * 30, cx + sx * 132
        s += f'<path d="M{x0} {h} V100 Q{(x0 + x1) / 2} 84 {x1} 128 V{h} Z" fill="#6E4422" stroke="#2A1A10" stroke-width="4"/>'
        for k in range(4):
            yy = 140 + k * 40
            s += f'<path d="M{x0} {yy} H{x1}" stroke="#2A1A10" stroke-width="5"/>'
            for j in range(3):
                s += f'<circle cx="{x0 + sx * (24 + j * 34)}" cy="{yy}" r="4" fill="#C9A86A"/>'
    for x in (cx - 230, cx + 230):
        alev = s.rad([(0, "#FFF4C8"), (.5, "#FFB43A"), (1, "#E2533D", .0)], x, 112, 60, kull="userSpaceOnUse", ad="al")
        s += f'<rect x="{x - 6}" y="130" width="12" height="60" fill="#2A1A10"/><circle cx="{x}" cy="112" r="60" fill="{alev}"/>'
        s += f'<path d="M{x - 12} 130 Q{x - 14} 104 {x} 86 Q{x + 14} 104 {x + 12} 130 Z" fill="#FF8A3D"/><path d="M{x - 6} 130 Q{x - 6} 112 {x} 100 Q{x + 6} 112 {x + 6} 130 Z" fill="#FFE08A"/>'
    for k, (x, c) in enumerate(((760, "#1E47A8"), (2010, "#16A9A3"))):
        s += f'<path d="M{x - 60} 70 H{x + 60} V230 L{x} 270 L{x - 60} 230 Z" fill="{c}" stroke="#2A1A10" stroke-width="3"/>'
        s += f'<path d="M{x - 60} 82 H{x + 60}" stroke="{ALTIN}" stroke-width="6"/>'
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x, 160, 40), True)}" fill="{ALTIN}" stroke="#2A1A10" stroke-width="2"/>'
        s += f'<circle cx="{x}" cy="160" r="14" fill="{c}"/>'
    s += '<use href="#pamuk-akce" x="1680" y="128" width="150" height="171"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== CEVAPLAR · KÜTAHYA'DA GECE (b36)

def kutahya_gece(h=360):
    s = Svg("pt-gec")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 30, 150, 160)
    s += S.ay(s, 1180, 80, 32, golge_renk="#13204A")
    d, _ = S.dag(s, -60, 900, ufuk, 320, 120, 161, renk="#283565", golge="#1C2650", bicim="tepe", isik=1, sirt=2, puruz=5)
    s += d
    isik = s.rad([(0, "#FFD27A", .35), (1, "#FFD27A", 0)], 1700, ufuk - 40, 460, kull="userSpaceOnUse", ad="pj")
    s += f'<circle cx="1700" cy="{ufuk - 40}" r="460" fill="{isik}"/>'
    kale, _ = _kale(s, 1260, 2160, ufuk + 40, 230, 162, tas="#6E6A8E", tepe="#2C3460", gece=True, bayrak=True)
    s += kale
    s += _zemin(s, 0, W, ufuk + 36, 140, "#2C3A6A", "#141E44", dalga=6, tohum=163, genlik=10)
    r = RNG(164)
    for k in range(90):
        x = r.uniform(80, 2060)
        y = ufuk + 50 + r.uniform(0, 70)
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(4, 8))}" height="{f(r.uniform(4, 7))}" fill="#FFD27A" opacity="{f(r.uniform(.5, 1), 2)}"/>'
    s += _pamuk(1560, 248, 60, "pamuk-kitap")
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== FİNAL · KÜTAHYA KALESİ BURCU (gün batımı)

def final_kutahya(h=890, nisanlar=None):
    s = Svg("pt-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    gx, gy = 760, ufuk - 30
    s += _isik_huzmesi(s, gx, gy, 14, "#FFE0A0", .12, 1800)
    s += S.gunes(s, gx, gy, 70, hale="#FFC56B", hale_r=700, guc=.95)
    for (x, y, w, k) in ((200, 260, 520, 22), (1200, 180, 640, 26), (1500, 330, 480, 16), (100, 420, 380, 12)):
        s += S.bulut_serit(s, x, y, w, k, "#FFC59A", "#FF6F8A", .75)
    s += _uzak(s, ufuk, 171, [(980, 1900, 1400, 330, "tepe"), (-100, 760, 300, 420, "tepe"), (1750, 2300, 2050, 410, "tepe")],
               "#C47AA0", "#6E4C8A", "#FF8E84")
    s += _zemin(s, 0, W, ufuk + 6, 330, "#A86A8E", "#5E3E6E", dalga=7, tohum=172, genlik=10)
    for i in range(14):
        s += _kutahya_evi(s, 40 + i * 104, ufuk + 70 + (i % 2) * 8, 76, 64, 173 + i, duvar="#F4E6EC", tas="#C8A8B8", cati="#A84A4A", gece=True)
    # taş burç (ön plan) + mazgallar
    g = s.lin([(0, "#D2BE98"), (1, "#8E7A5A")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    s += f'<rect x="0" y="720" width="{W}" height="{h - 720}" fill="{g}"/>'
    r = RNG(190)
    for row in range(6):
        y = 724 + row * 30
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            s += f'<rect x="{x + 2}" y="{y}" width="86" height="27" rx="3" fill="{karis("#D2BE98", "#A48E6A", r.uniform(0, .7))}" stroke="#6E5A40" stroke-width="1.6"/>'
    for x in range(0, W, 150):
        s += f'<rect x="{x}" y="660" width="96" height="64" fill="#C4AE88" stroke="#6E5A40" stroke-width="2.6"/>'
    s.tanim(f'<linearGradient id="{s.onek}-tk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E2D0AA"/><stop offset=".6" stop-color="#C4AE88"/><stop offset="1" stop-color="#8E7A5A"/></linearGradient>')
    s += f'<path d="M1560 {h} V560 Q1770 520 1980 560 V{h} Z" fill="url(#{s.onek}-tk)" stroke="#6E5A40" stroke-width="3"/>'
    for x in range(1560, 1980, 84):
        s += f'<rect x="{x}" y="510" width="54" height="56" fill="#CDB894" stroke="#6E5A40" stroke-width="2.6"/>'
    s += f'<path d="M1740 {h} V760 Q1740 720 1770 712 Q1800 720 1800 760 V{h} Z" fill="#2A1A10"/>'
    s += '<use href="#pamuk-bayrak" x="1600" y="150" width="340" height="400"/>'
    s += f'<path d="M260 650 V330" stroke="#6B4A2E" stroke-width="10"/><circle cx="260" cy="324" r="10" fill="{ALTIN}"/>'
    s += f'<path d="M260 360 Q900 520 1640 330" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .6) / (len(nisanlar) + .2)
            x = (1 - t) ** 2 * 260 + 2 * (1 - t) * t * 900 + t * t * 1640
            y = (1 - t) ** 2 * 360 + 2 * (1 - t) * t * 520 + t * t * 330
            s += f'<path d="M{f(x)} {f(y)} v18" stroke="#5A3A22" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 52)} {f(y + 14)}) rotate({f((k % 2 * 2 - 1) * 5)} 52 60) scale(.84)">{ns}</g>'
    for k in range(60):
        x = r.uniform(300, 1900)
        y = r.uniform(80, 640)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== AÇILIŞ · BATI ANADOLU MADEN YOLU PANORAMASI

# Stilize tur haritası (temsilî, eğik bakış): kuzeybatıda Marmara ve Bandırma, ortada Kütahya, doğuda Kırka, güneydoğuda
# Seydişehir. Konumlar panorama birimidir (2100×1100); kuzey yukarıdadır. Etiket metinleri kur.py'de (HTML).
DURAKLAR = [  # (anahtar, x, y, üst satır, ad, "s.N · akçe", tür)
    ("1", 1840, 960, "1. DURAK · SEYDİŞEHİR", "Boşluktan tabloya", "s.2 · +100 akçe", "durak"),
    ("2", 1320, 680, "2. DURAK · KÜTAHYA", "Dizilimden adrese", "s.3 · +150 akçe", "durak"),
    ("3", 880, 600, "3. DURAK · GÜMÜŞKÖY", "Kestirme yollar", "s.4 · +150 akçe", "durak"),
    ("4", 1620, 560, "4. DURAK · KIRKA", "Metal mi, yarı metal mi?", "s.5 · +150 akçe", "durak"),
    ("5", 300, 476, "5. DURAK · BANDIRMA", "Aileler ve iyonlar", "s.6 · +150 akçe", "durak"),
    ("H", 430, 606, "KUŞCENNETİ", "Hülasa", "s.7 · +40 akçe", "hulasa"),
    ("M", 300, 840, "BİGADİÇ", "Meclis: Kim haklı?", "s.8 · +120 akçe", "yan"),
    ("K", 700, 860, "EMET", "Kıssa", "s.9 · +120 akçe", "yan"),
    ("A", 1220, 900, "GERMİYAN SOKAĞI", "Anahtar merdiveni", "s.10 · +120 akçe", "yan"),
    ("V", 1100, 740, "KÜTAHYA KALESİ", "Büyük İmtihan", "s.11–12 · +300 akçe", "kale"),
]
ROTA_ARA = {("1", "2"): [(1640, 900), (1460, 780)], ("2", "3"): [(1100, 610)], ("3", "4"): [(1050, 540), (1350, 520)],
            ("4", "5"): [(1360, 480), (980, 500), (620, 540), (420, 500)], ("5", "H"): [(330, 560)], ("H", "M"): [(360, 720)],
            ("M", "K"): [(500, 880)], ("K", "A"): [(960, 900)], ("A", "V"): [(1160, 820)]}


def maden_panorama(h=1100):
    s = Svg("pt-pan")
    ufuk = 330
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3E5BB0"), (.35, "#8C8FD2"), (.62, "#F2A8BC"), (.85, "#FFD2A8"), (1, "#FFEBD0")])
    gx, gy = 1880, ufuk - 50
    s += _isik_huzmesi(s, gx, gy, 12, "#FFF0D0", .08)
    s += S.gunes(s, gx, gy, 48, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=600, guc=.95)
    for (x, y, w_, k) in ((520, 150, 520, 18), (1120, 96, 600, 22), (1520, 200, 420, 14), (80, 230, 360, 12)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFE3EA", "#F6B0C4", .7)
    s += _uzak(s, ufuk + 8, 201, [(-120, 760, 300, 170, "tepe"), (520, 1500, 1000, 150, "tepe"), (1300, 2260, 1760, 120, "sivri")],
               "#A78CCE", "#6C5AA8", "#F2C2D8", kar="#FFFFFF", kar_oran=.18, kar_golge="#D6CCEE", kenar="#FFE6D2")
    # yayla zemini: ufukta sıcak, önde yeşil-altın
    gz = s.lin([(0, "#E9D2A6"), (.25, "#D9C98E"), (.6, "#B9C27A"), (1, "#97AE62")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="yz")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{gz}"/>'
    r = RNG(202)
    for i, (yy, genlik, c1, c2) in enumerate(((ufuk + 40, 22, "#DCC596", "#E6D3A8"), (ufuk + 120, 26, "#C9C484", "#D9D29A"), (ufuk + 260, 24, "#B5BE74", "#C6CC88"))):
        tb, _ = S.tepe_bandi(s, 0, W, yy, genlik, 203 + i, c1, c2, dalga=6, olcek=60)
        s += tb
    s += _tarla(s, 0, W, ufuk + 140, h, 206, ["#C9C27E", "#B6BE72", "#D8CC92", "#A8B86C", "#C2B272"], n=9)
    # Marmara Denizi (kuzeybatı) ve kıyı
    kiyi = [(0, 600), (90, 560), (190, 520), (262, 492), (300, 470), (340, 486), (420, 470), (560, 452), (700, 440), (820, 420), (920, 392), (1000, ufuk + 6)]
    deniz = s.lin([(0, "#7CC9D4"), (1, "#1E7E96")], 0, ufuk, 0, 600, kull="userSpaceOnUse", ad="dz")
    s += f'<path d="M0 {ufuk + 6} L1000 {ufuk + 6} L{egri_d(list(reversed(kiyi)))[1:]} Z" fill="{deniz}"/>'
    s += f'<path d="{egri_d(kiyi)}" stroke="#FFFFFF" stroke-width="5" fill="none" opacity=".85"/>'
    s += S.dalga_cizgileri(0, ufuk + 20, 900, 150, 207, n=30, op=.55)
    s += _gemi(s, 200, 452, 120)
    # Manyas Gölü (Kuşcenneti) ve Beyşehir Gölü
    for (cx, cy, rx, ry) in ((432, 640, 96, 30), (1648, 880, 70, 46)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#5FB8C4" stroke="#FFFFFF" stroke-width="4"/>'
        s += f'<ellipse cx="{cx - rx * .2}" cy="{cy - ry * .2}" rx="{rx * .6}" ry="{ry * .4}" fill="#9ED9DE" opacity=".7"/>'
    # Uludağ (karlı) ve Toros (güneydoğu)
    d, _ = S.dag(s, 560, 840, 500, 700, 404, 208, renk="#8FA0C2", golge="#6878A2", bicim="sivri", kar_y=446, kar="#FFFFFF",
                 kar_golge="#C9D3EA", isik=-1, sirt=3, puruz=6)
    s += d
    for i, (a, b, tx, ty) in enumerate(((1400, 1760, 1600, 960), (1680, 2160, 1960, 920), (1980, 2300, 2120, 970))):
        d, _ = S.dag(s, a, b, h + 40, tx, ty, 209 + i, renk="#9AA7C8", golge="#7381A8", bicim="sivri", kar_y=ty + 40, kar="#FFFFFF",
                     kar_golge="#D6D6EE", isik=-1, sirt=3, puruz=7)
        s += d
    # Porsuk Çayı: Kütahya → Eskişehir
    porsuk = [(1130, 760), (1220, 650), (1330, 560), (1440, 470), (1520, 420), (1640, 380), (1760, 352)]
    s += f'<path d="{egri_d(porsuk)}" fill="none" stroke="#2E8CA6" stroke-width="13" stroke-linecap="round" opacity=".8"/><path d="{egri_d(porsuk)}" fill="none" stroke="#8ED6E4" stroke-width="5" stroke-linecap="round"/>'
    # yerleşimler ve madenler (temsilî)
    s += _koy(s, 1440, 1560, 452, 5, 210, o=.9)
    s += halolu_yazi('x="1500" y="420" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="26" letter-spacing="2"', "ESKİŞEHİR", "#3A2E56", "#FFFFFF", 3)
    s += halolu_yazi('x="700" y="392" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="24" letter-spacing="2"', "ULUDAĞ", "#3A2E56", "#FFFFFF", 3)
    s += halolu_yazi('x="200" y="400" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="26" letter-spacing="3"', "MARMARA", "#0E4C5A", "#E6F6F8", 3)
    s += halolu_yazi('x="1940" y="1062" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="24" letter-spacing="2"', "TOROSLAR", "#3A2E56", "#FFFFFF", 3)
    s += _basamakli(s, 1720, 610, 190, 60, 4, "#FFFFFF", "#E4ECF2", "#A9BCCD", 211, yol=False)       # Kırka
    s += _basamakli(s, 960, 640, 120, 40, 3, "#E3E8EC", "#A9B4BE", "#6F7C88", 212, yol=False)       # Gümüşköy
    s += _basamakli(s, 400, 880, 130, 42, 3, "#FBFAF6", "#DCD8CE", "#A8A296", 213, yol=False)        # Bigadiç
    s += _basamakli(s, 800, 890, 130, 42, 3, "#FBFAF6", "#D9D4C8", "#A49C8E", 214, yol=False)        # Emet
    kale, _ = _kale(s, 1020, 1180, 752, 96, 215, bayrak=True)
    s += kale
    for i in range(7):
        s += _kutahya_evi(s, 1170 + (i % 4) * 46, 790 + (i // 4) * 40, 32, 30, 216 + i)
    for k in range(3):
        s += _silo(s, 1880 + k * 22, 990, 18, 50, "#F2F4F6")
    s += _hol(s, 1760, 1000, 110, 34, "#E2E6EA", "#6E7C8A", 219)
    s += _baca(s, 1950, 990, 14, 80, 220, duman=True)
    s += _yigin(s, 1790, 1012, 80, 22, "#B5482E", "#7E2E1C", 221)
    s += _vinc(s, 340, 470, 60, yon=-1)
    s += _yigin(s, 372, 476, 50, 16, "#FFFFFF", "#C9C4D8", 222)
    for k in range(40):
        x = r.uniform(40, 2060)
        y = r.uniform(ufuk + 120, h - 40)
        if any(math.hypot(x - a, y - b) < 110 for _, a, b, *_ in DURAKLAR) or (x < 1000 and y < 600):
            continue
        sc = .5 + (y - ufuk) / (h - ufuk) * .7
        s += S.kavak(s, x, y, 46 * sc, 12 * sc, 230 + k, renk=r.choice(["#5E9A4A", "#6EA850", "#4E8A3E"]))
    # rota
    sira = [d_[0] for d_ in DURAKLAR]
    konum = {d_[0]: (d_[1], d_[2]) for d_ in DURAKLAR}
    yol = []
    for i, k in enumerate(sira):
        yol.append(konum[k])
        if i + 1 < len(sira):
            yol += ROTA_ARA.get((k, sira[i + 1]), [])
    yd = egri_d(yol, False, .9)
    s += f'<path d="{yd}" fill="none" stroke="#1B1D26" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
    s += f'<path d="{yd}" fill="none" stroke="#FFF1CF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="3.2" stroke-dasharray="12 9" stroke-linecap="round"/>'
    for k, x, y, *_r, tur in DURAKLAR:
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
    px, py = 2000, 760
    s += f'<circle cx="{px}" cy="{py}" r="64" fill="#FFFFFF" opacity=".92" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 56, 12, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 29), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="9" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += halolu_yazi(f'x="{px}" y="{py - 72}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="28"', "K", "#1B1D26", "#FFFFFF", 2.4)
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), konum
