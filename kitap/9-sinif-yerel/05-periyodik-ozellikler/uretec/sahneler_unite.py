"""Periyodik Özellikler · Maden Yolu II · Doğu Anadolu — üniteye özel sahneler ve nişan ikonları.

kur_ortak {{sahne|ad}} için önce bu modüle bakar. Ortak kütüphane (yerel-ortak/cizim) DEĞİŞTİRİLMEZ; buradaki
parçalar ortak parçalardan (gökyüzü, dağ, göl, kavak, bulut, tekne, iskele, çadır …) kurulur.

Kompozisyon (TASARIM-SISTEMI.md §6): bant 2100×460 birim; sol üst ≈ %55 × %75 levhaya boş; odak sağ %40'ta;
ışık yönü sahne içinde tutarlı (isik=-1, güneş solda ya da tepede); tohum sabit; her Svg öneki "m2-" ile başlar.
Yerler temsilîdir: cami, kilise, manastır çizilmez; depremden etkilenen yapılar gösterilmez; logo yok.

Bölgeye özel parçalar:
  basamakli_ocak()  Divriği demir ocağı: pas kızılı tepeye oyulmuş basamaklar, yük yolu, kamyonlar
  galeri()          maden galerisi ağzı (ahşap çerçeve), raylar · vagonet() cevher arabası · cevher_yigini()
  tren()            cevher vagonları (demiryolu)
  kale_sirti()      Divriği Kalesi: kayalık sırtta sur ve burçlar (temsilî)
  baraj()           Keban Barajı gövdesi, dolusavak, santral (temsilî) · pilon() enerji direği
  kemaliye_evi()    Kemaliye (Eğin) evi: beyaz sıvalı, ahşap çatkılı, çok pencereli
Sahneler: divrigi, guleman, maden, hazar, firat_kavsagi, keban (duraklar) · firat_kamp (Hülasa) · kemaliye (Meclis) ·
karanlik_kanyon (Kıssa) · kale_yokusu (Anahtar) · divrigi_kalesi (İmtihan) · divrigi_gece (Cevaplar) · divrigi_final (Final) ·
panorama_rota (açılış haritası).
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim import sahne as S, yapilar as Y
from cizim.sahneler import W, H, _bitir, _cerceve_golge

PAS = "#B5543A"
PAS_K = "#7A3326"
OKR = "#C98A4E"

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    # atom: katmanlar + yarıçap çizgisi
    "yaricap": ('<circle cx="24" cy="24" r="18"/><circle cx="24" cy="24" r="11.5"/><circle cx="24" cy="24" r="5"/>'
                '<path d="M24 24 L41 15"/><path d="M36 13 l5 2 l-2 5"/><circle cx="24" cy="24" r="1.6"/>'),
    # iyon: büyük anyon ve küçük katyon
    "iyon": ('<circle cx="17" cy="27" r="13"/><path d="M11 27 h12"/><circle cx="36" cy="16" r="7"/>'
             '<path d="M32.5 16 h7 M36 12.5 v7"/><path d="M7 43 h34" stroke-dasharray="3 3"/>'),
    # bakır: kazan + kopan elektron
    "bakir": ('<path d="M9 22 h30 l-3 15 c-1 4 -4 6 -8 6 h-8 c-4 0 -7 -2 -8 -6 Z"/><path d="M6 22 h36"/>'
              '<path d="M15 22 c0 -6 18 -6 18 0"/><circle cx="40" cy="9" r="4"/><path d="M33 13 l-6 5" stroke-dasharray="2 2"/>'),
    # basamak: ardışık İE ve büyük sıçrama
    "sicrama": ('<path d="M6 41 V35 H13 V30 H20 V26 H27 V8 H34"/><path d="M6 41 H42"/><path d="M27 26 V8"/>'
                '<path d="M31 18 l3 -4 l3 4"/><circle cx="40" cy="8" r="2.4"/>'),
    # halat: bağ elektronları için çekişme
    "halat": ('<circle cx="10" cy="24" r="6"/><circle cx="38" cy="24" r="9"/><path d="M16 24 C22 21 26 27 29 24"/>'
              '<circle cx="27" cy="24" r="3"/><path d="M9 11 h3 M10.5 9.5 v3 M36 9 h5"/>'),
    # gümüş külçe + akçe
    "gumus": ('<path d="M6 34 L12 24 H32 L38 34 Z"/><path d="M12 24 L15 18 H29 L32 24"/><circle cx="36" cy="12" r="7"/>'
              '<path d="M33 12 h6"/><path d="M10 40 h28"/>'),
}


# ------------------------------------------------------------------ küçük yardımcılar

def _ova(s, y, tohum, ust="#C9B07A", alt="#7E8A4A", x0=0, x1=W, h=H):
    g = s.lin([(0, ust), (1, alt)], 0, y, 0, h, kull="userSpaceOnUse", ad="ova")
    r = RNG(tohum)
    pts = [(x0 + (x1 - x0) * i / 12, y + r.uniform(-6, 6)) for i in range(13)]
    return f'<path d="{egri_d(pts)} L{f(x1)} {f(h)} L{f(x0)} {f(h)} Z" fill="{g}"/>'


def _tarla(s, x0, x1, y0, y1, tohum, n=22, renkler=("#C9B26A", "#A7B45E", "#D9B878", "#8FA552", "#C49A5E")):
    r = RNG(tohum)
    o = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        t = (y - y0) / max(1, y1 - y0)
        w = r.uniform(60, 150) * (.5 + t)
        hh = w * .2
        o.append(f'<path d="M{f(x)} {f(y)} l{f(w)} {f(-hh * .15)} l{f(-w * .15)} {f(hh)} l{f(-w)} {f(hh * .15)} Z" fill="{r.choice(renkler)}" opacity=".55"/>')
    return "".join(o)


def _kesisim_x(pts, y):
    xs = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if (y1 - y) * (y2 - y) <= 0 and y1 != y2:
            xs.append(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
    return (min(xs), max(xs)) if len(xs) >= 2 else None


def kavak_sirasi(s, xs, y, h, w, tohum, renk="#5E9A44"):
    return "".join(S.kavak(s, x, y + (i % 3) * 5, h * (.85 + .1 * (i % 4)), w, tohum + i, renk=renk) for i, x in enumerate(xs))


def evler(s, x0, n, y, tohum, ara=58, w=44, h=30, duvar="#EFE2C8", cati="#B8553A", duz=True):
    r = RNG(tohum)
    return "".join(S.ev(x0 + i * ara + r.uniform(-6, 6), y + r.uniform(-5, 5) + (i % 2) * 6, w, h, tohum + i, duvar=duvar,
                        cati=cati, duz=duz and i % 3 != 1) for i in range(n))


def kamyon(x, y, o=1.0, yon=-1, renk="#F0A21A", yuk="#5A2A22"):
    """Damperli maden kamyonu (temsilî, yazısız)."""
    k = o
    sx = -1 if yon < 0 else 1
    g = (f'<g transform="translate({f(x)} {f(y)}) scale({f(sx * k)} {f(k)})">'
         f'<path d="M-40 -22 H14 L22 -6 H-40 Z" fill="{renk}" stroke="#1B1D26" stroke-width="2.4"/>'
         f'<path d="M-38 -22 Q-14 -40 12 -22 Z" fill="{yuk}"/>'
         f'<path d="M22 -6 H44 V-24 H30 Z" fill="{renk}" stroke="#1B1D26" stroke-width="2.4"/>'
         f'<rect x="32" y="-21" width="9" height="8" fill="#BFE3F2"/>'
         f'<circle cx="-26" cy="-2" r="8" fill="#2A2A30"/><circle cx="2" cy="-2" r="8" fill="#2A2A30"/><circle cx="34" cy="-2" r="8" fill="#2A2A30"/>'
         f'<circle cx="-26" cy="-2" r="3" fill="#9AA4AE"/><circle cx="2" cy="-2" r="3" fill="#9AA4AE"/><circle cx="34" cy="-2" r="3" fill="#9AA4AE"/></g>')
    return g


def basamakli_ocak(s, sirt, ust_y, taban, n, tohum, renkler=("#A8472F", "#C0683E", "#8E3B2C", "#B98256", "#7A3A3E", "#C77B4A")):
    """Tepe profili (sirt) üstüne oyulmuş açık ocak basamakları: her basamakta açık renkli düzlük + koyu şev."""
    r = RNG(tohum)
    o = []
    seviyeler = [ust_y + (taban - ust_y) * (i / n) ** 1.05 for i in range(n + 1)]
    for i in range(n):
        ya, yb = seviyeler[i], seviyeler[i + 1]
        a = _kesisim_x(sirt, ya)
        b = _kesisim_x(sirt, yb)
        if not a or not b:
            continue
        ic = 10 + i * 3
        xl_a, xr_a = a[0] + ic, a[1] - ic
        xl_b, xr_b = b[0] + ic * .6, b[1] - ic * .6
        c = renkler[i % len(renkler)]
        o.append(f'<path d="M{f(xl_a)} {f(ya)} L{f(xr_a)} {f(ya)} L{f(xr_b)} {f(yb)} L{f(xl_b)} {f(yb)} Z" fill="{c}"/>')
        o.append(f'<path d="M{f(xl_a)} {f(ya)} L{f(xr_a)} {f(ya)} L{f(xr_a - 6)} {f(ya + (yb - ya) * .28)} L{f(xl_a + 6)} {f(ya + (yb - ya) * .28)} Z" fill="{acik(c, .32)}"/>')
        for k in range(int((xr_b - xl_b) / 60)):
            x = xl_a + 20 + k * 60 + r.uniform(-12, 12)
            o.append(f'<path d="M{f(x)} {f(ya + (yb - ya) * .35)} l{f(r.uniform(-8, 8))} {f((yb - ya) * .5)}" stroke="{koyu(c, .25)}" stroke-width="2.4" opacity=".5"/>')
    # zikzak yük yolu
    yol = []
    for i in range(1, n, 2):
        a = _kesisim_x(sirt, seviyeler[i])
        if a:
            yol.append((a[1] - 40 - i * 4, seviyeler[i] + 6) if (i // 2) % 2 == 0 else (a[0] + 40 + i * 4, seviyeler[i] + 6))
    if len(yol) > 1:
        o.append(f'<path d="{cizgi_d(yol)}" stroke="#E7C38E" stroke-width="9" fill="none" stroke-linejoin="round" opacity=".9"/>')
        o.append(f'<path d="{cizgi_d(yol)}" stroke="#9C6A3E" stroke-width="2" fill="none" stroke-dasharray="10 9" opacity=".7"/>')
    return "".join(o), seviyeler


def galeri(s, x, y, w, h, tohum, kaya="#3A3F38"):
    """Maden galerisi ağzı: kemerli koyu açıklık, ahşap dikmeler ve başlık, içeri giden raylar."""
    o = []
    g = s.rad([(0, "#000000"), (1, "#24201C")], .5, .7, .7, ad="ga")
    o.append(f'<path d="M{f(x - w * .62)} {f(y)} L{f(x - w * .62)} {f(y - h * .7)} Q{f(x)} {f(y - h * 1.28)} {f(x + w * .62)} {f(y - h * .7)} L{f(x + w * .62)} {f(y)} Z" fill="{koyu(kaya, .1)}"/>')
    o.append(f'<path d="M{f(x - w / 2)} {f(y)} L{f(x - w / 2)} {f(y - h * .72)} Q{f(x)} {f(y - h * 1.1)} {f(x + w / 2)} {f(y - h * .72)} L{f(x + w / 2)} {f(y)} Z" fill="{g}"/>')
    ah = "#9A6B42"
    o.append(f'<rect x="{f(x - w / 2 - 8)}" y="{f(y - h * .8)}" width="14" height="{f(h * .8)}" fill="{ah}" stroke="#4A2E18" stroke-width="2"/>')
    o.append(f'<rect x="{f(x + w / 2 - 6)}" y="{f(y - h * .8)}" width="14" height="{f(h * .8)}" fill="{ah}" stroke="#4A2E18" stroke-width="2"/>')
    o.append(f'<rect x="{f(x - w / 2 - 18)}" y="{f(y - h * .86)}" width="{f(w + 36)}" height="16" fill="{acik(ah, .1)}" stroke="#4A2E18" stroke-width="2"/>')
    for k in range(5):
        t = k / 4
        yy = y - h * .05 - t * h * .45
        ww = w * (.62 - t * .4)
        o.append(f'<path d="M{f(x - ww / 2)} {f(yy)} H{f(x + ww / 2)}" stroke="#6E5A48" stroke-width="{f(3.4 - t * 2)}"/>')
    o.append(f'<path d="M{f(x - w * .18)} {f(y)} L{f(x - w * .06)} {f(y - h * .5)} M{f(x + w * .18)} {f(y)} L{f(x + w * .06)} {f(y - h * .5)}" stroke="#8A8F96" stroke-width="3"/>')
    return "".join(o)


def raylar(x0, y0, x1, y1, ara=16, renk="#5E646C"):
    a = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(a) * ara / 2, math.cos(a) * ara / 2
    o = []
    L = math.hypot(x1 - x0, y1 - y0)
    for k in range(int(L / 22) + 1):
        t = k * 22 / L
        cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        o.append(f'<path d="M{f(cx - nx * 1.6)} {f(cy - ny * 1.6)} L{f(cx + nx * 1.6)} {f(cy + ny * 1.6)}" stroke="#6E4A2E" stroke-width="5"/>')
    for sgn in (-1, 1):
        o.append(f'<path d="M{f(x0 + sgn * nx)} {f(y0 + sgn * ny)} L{f(x1 + sgn * nx)} {f(y1 + sgn * ny)}" stroke="{renk}" stroke-width="3.2"/>')
    return "".join(o)


def vagonet(s, x, y, o=1.0, cevher="#1E2224", parilti="#6FD08A"):
    """Cevher arabası (vagonet): kesik koni kasa, tekerlek, üstte cevher yığını."""
    k = o
    r = RNG(int(x * 7 + y))
    out = [f'<g transform="translate({f(x)} {f(y)}) scale({f(k)})">',
           f'<path d="M-38 -14 L-30 -46 H30 L38 -14 Z" fill="#8E949B" stroke="#1B1D26" stroke-width="3"/>',
           f'<path d="M-30 -46 H30" stroke="#C3C9CF" stroke-width="4"/>',
           f'<path d="M-30 -48 Q-12 -74 4 -60 Q16 -78 30 -48 Z" fill="{cevher}"/>']
    for _ in range(6):
        out.append(f'<circle cx="{f(r.uniform(-22, 22))}" cy="{f(r.uniform(-62, -50))}" r="{f(r.uniform(1.6, 3.2))}" fill="{parilti}"/>')
    out += [f'<circle cx="-20" cy="-8" r="9" fill="#2A2A30"/><circle cx="20" cy="-8" r="9" fill="#2A2A30"/>',
            f'<circle cx="-20" cy="-8" r="3.4" fill="#9AA4AE"/><circle cx="20" cy="-8" r="3.4" fill="#9AA4AE"/>', '</g>']
    return "".join(out)


def cevher_yigini(s, x, y, w, h, tohum, renk="#26292B", parilti="#6FD08A", n=14):
    r = RNG(tohum)
    o = [f'<path d="M{f(x - w / 2)} {f(y)} Q{f(x - w * .2)} {f(y - h * 1.1)} {f(x)} {f(y - h)} Q{f(x + w * .25)} {f(y - h * 1.05)} {f(x + w / 2)} {f(y)} Z" fill="{renk}"/>',
         f'<path d="M{f(x - w * .1)} {f(y - h * .98)} Q{f(x + w * .2)} {f(y - h * .9)} {f(x + w * .45)} {f(y - h * .05)} L{f(x + w / 2)} {f(y)} Q{f(x + w * .25)} {f(y - h * 1.05)} {f(x)} {f(y - h)} Z" fill="#000" opacity=".25"/>']
    for _ in range(n):
        px = x + r.uniform(-w * .35, w * .35)
        py = y - r.uniform(.1, .8) * h * (1 - abs(px - x) / (w * .6))
        o.append(f'<path d="M{f(px)} {f(py - 4)} l2 4 l-2 4 l-2 -4 Z" fill="{parilti}"/>')
    return "".join(o)


def tren(s, x, y, n, tohum, yon=-1):
    """Demiryolunda cevher treni: lokomotif + n açık vagon (yazısız)."""
    r = RNG(tohum)
    o = [f'<path d="M{f(x - 60)} {f(y + 12)} H{f(x + n * 120 + 260)}" stroke="#4A4A50" stroke-width="5"/>']
    for k in range(int((n * 120 + 320) / 26)):
        o.append(f'<path d="M{f(x - 60 + k * 26)} {f(y + 9)} v7" stroke="#6E4A2E" stroke-width="5"/>')
    lx = x
    o.append(f'<path d="M{f(lx)} {f(y)} V{f(y - 46)} H{f(lx + 60)} V{f(y - 70)} H{f(lx + 110)} V{f(y)} Z" fill="#B23A2E" stroke="#1B1D26" stroke-width="3"/>')
    o.append(f'<rect x="{f(lx + 66)}" y="{f(y - 64)}" width="34" height="22" fill="#BFE3F2" stroke="#1B1D26" stroke-width="2"/>')
    o.append(f'<path d="M{f(lx)} {f(y - 26)} H{f(lx + 110)}" stroke="#F0A21A" stroke-width="6"/>')
    for i in range(n):
        vx = lx + 130 + i * 120
        o.append(f'<path d="M{f(vx)} {f(y)} L{f(vx + 6)} {f(y - 44)} H{f(vx + 104)} L{f(vx + 110)} {f(y)} Z" fill="{karis("#5E3A2E", "#7A4A34", r.random())}" stroke="#1B1D26" stroke-width="3"/>')
        o.append(f'<path d="M{f(vx + 8)} {f(y - 44)} Q{f(vx + 34)} {f(y - 66)} {f(vx + 56)} {f(y - 52)} Q{f(vx + 80)} {f(y - 68)} {f(vx + 102)} {f(y - 44)} Z" fill="#2A1E1C"/>')
        o.append(f'<path d="M{f(vx + 104)} {f(y - 18)} h18" stroke="#1B1D26" stroke-width="4"/>')
    for i in range(n * 2 + 3):
        wx = lx + 22 + i * 60
        if wx < lx + 130 + n * 120:
            o.append(f'<circle cx="{f(wx)}" cy="{f(y + 2)}" r="10" fill="#2A2A30"/><circle cx="{f(wx)}" cy="{f(y + 2)}" r="3.6" fill="#9AA4AE"/>')
    if yon < 0:
        o.append(f'<path d="M{f(lx + 24)} {f(y - 46)} v-18" stroke="#3A3A40" stroke-width="10"/>')
        o.append(f'<circle cx="{f(lx + 18)}" cy="{f(y - 84)}" r="14" fill="#E9EEF2" opacity=".85"/><circle cx="{f(lx + 46)}" cy="{f(y - 102)}" r="18" fill="#E9EEF2" opacity=".7"/>')
    return "".join(o)


def kale_sirti(s, x0, x1, taban, tepe_y, tohum, kaya="#7A5A50", golge="#4E3A38", tas="#C9A88A", tas_g="#8C6E5A", gece=False, bayrak=False):
    """Divriği Kalesi (temsilî): kayalık sırt, sırtı izleyen sur, kare ve yuvarlak burçlar, mazgallar."""
    r = RNG(tohum)
    o = []
    n = 14
    sirt = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        yy = taban - (taban - tepe_y) * (math.sin(math.pi * min(1, t * 1.1)) ** .55) - r.uniform(0, 14)
        sirt.append((x, yy))
    kaya_g = s.lin([(0, acik(kaya, .12)), (1, golge)], 0, tepe_y, 0, taban, kull="userSpaceOnUse", ad="ky")
    o.append(f'<path d="M{f(x0)} {f(taban)} {cizgi_d(sirt)[1:]} L{f(x1)} {f(taban)} Z" fill="{kaya_g}"/>')
    for k in range(9):
        i = r.randint(2, n - 2)
        px, py = sirt[i]
        o.append(f'<path d="M{f(px)} {f(py + 8)} l{f(r.uniform(-30, 30))} {f(r.uniform(40, 110))}" stroke="{koyu(kaya, .35)}" stroke-width="{f(r.uniform(2, 5))}" opacity=".6"/>')
    # sur: sırt çizgisinin biraz üstünde
    duvar = [(x, y - 26) for x, y in sirt[2:-2]]
    alt = [(x, y + 8) for x, y in reversed(sirt[2:-2])]
    o.append(f'<path d="{cizgi_d(duvar + alt, True)}" fill="{tas}" stroke="{tas_g}" stroke-width="3"/>')
    for (xa, ya), (xb, yb) in zip(duvar, duvar[1:]):
        L = math.hypot(xb - xa, yb - ya)
        for k in range(int(L / 26)):
            t = (k + .3) / (L / 26)
            mx, my = xa + (xb - xa) * t, ya + (yb - ya) * t
            o.append(f'<rect x="{f(mx - 7)}" y="{f(my - 13)}" width="14" height="14" fill="{tas}" stroke="{tas_g}" stroke-width="2"/>')
    for k, i in enumerate(range(3, n - 2, 3)):
        bx, by = sirt[i]
        bw, bh = 54 + (k % 2) * 10, 96 + (k % 3) * 18
        bg = s.lin([(0, acik(tas, .15)), (.55, tas), (1, tas_g)], 0, 0, 1, 0, ad="bg")
        if k % 2:
            o.append(f'<path d="M{f(bx - bw / 2)} {f(by + 8)} V{f(by - bh)} Q{f(bx)} {f(by - bh - 18)} {f(bx + bw / 2)} {f(by - bh)} V{f(by + 8)} Z" fill="{bg}" stroke="{tas_g}" stroke-width="3"/>')
        else:
            o.append(f'<rect x="{f(bx - bw / 2)}" y="{f(by - bh)}" width="{bw}" height="{f(bh + 8)}" fill="{bg}" stroke="{tas_g}" stroke-width="3"/>')
        for j in range(3):
            o.append(f'<rect x="{f(bx - bw / 2 + j * bw * .38)}" y="{f(by - bh - 14)}" width="{f(bw * .24)}" height="16" fill="{tas}" stroke="{tas_g}" stroke-width="2"/>')
        pc = "#FFD27A" if gece else koyu(tas_g, .5)
        o.append(f'<rect x="{f(bx - 5)}" y="{f(by - bh * .62)}" width="10" height="{f(bh * .2)}" rx="5" fill="{pc}"/>')
        if bayrak and k == 1:
            o.append(f'<path d="M{f(bx)} {f(by - bh - 14)} V{f(by - bh - 90)}" stroke="#3A3A44" stroke-width="5"/>')
            o.append(f'<path d="M{f(bx)} {f(by - bh - 90)} q30 -8 60 4 q-8 14 0 30 q-30 -10 -60 -4 Z" fill="#E30A17"/>')
            o.append(f'<circle cx="{f(bx + 26)}" cy="{f(by - bh - 74)}" r="8" fill="#FFFFFF"/><circle cx="{f(bx + 29)}" cy="{f(by - bh - 74)}" r="6.4" fill="#E30A17"/>')
    return "".join(o), sirt


def baraj(s, x0, x1, ust, alt, tohum):
    """Keban Barajı (temsilî, mansaptan bakış): kayalık yamaçlar arasında beton gövde, kret yolu, dolusavak oluğu, santral."""
    r = RNG(tohum)
    o = []
    g = s.lin([(0, "#E3E6E8"), (.5, "#BFC5CA"), (1, "#8E979E")], 0, ust, 0, alt, kull="userSpaceOnUse", ad="bt")
    egim = 60
    o.append(f'<path d="M{f(x0)} {f(ust)} Q{f((x0 + x1) / 2)} {f(ust + 26)} {f(x1)} {f(ust)} L{f(x1 + egim)} {f(alt)} L{f(x0 - egim)} {f(alt)} Z" fill="{g}" stroke="#5E666E" stroke-width="3"/>')
    for k in range(1, 6):
        yy = ust + (alt - ust) * k / 6
        o.append(f'<path d="M{f(x0 - egim * k / 6)} {f(yy + 10)} Q{f((x0 + x1) / 2)} {f(yy + 30)} {f(x1 + egim * k / 6)} {f(yy + 10)}" stroke="#A3ABB2" stroke-width="2" fill="none"/>')
    o.append(f'<path d="M{f(x0 - 10)} {f(ust - 4)} Q{f((x0 + x1) / 2)} {f(ust + 20)} {f(x1 + 10)} {f(ust - 4)}" stroke="#F4F6F7" stroke-width="10" fill="none"/>')
    for k in range(int((x1 - x0) / 40)):
        xx = x0 + 10 + k * 40
        o.append(f'<path d="M{f(xx)} {f(ust - 8 + 22 * math.sin(math.pi * (xx - x0) / (x1 - x0)) * .45)} v-14" stroke="#7E868D" stroke-width="3"/>')
    # dolusavak (sağda): eğik oluk + köpüklü su + sıçrama
    sx = x1 - 120
    su = s.lin([(0, "#E9FBFF"), (1, "#8FD4E4")], 0, ust, 0, alt, kull="userSpaceOnUse", ad="ds")
    o.append(f'<path d="M{f(sx)} {f(ust + 6)} L{f(sx + 70)} {f(ust + 6)} L{f(sx + 150)} {f(alt - 10)} L{f(sx + 40)} {f(alt - 10)} Z" fill="#9AA2A8" stroke="#5E666E" stroke-width="3"/>')
    o.append(f'<path d="M{f(sx + 10)} {f(ust + 10)} L{f(sx + 60)} {f(ust + 10)} L{f(sx + 136)} {f(alt - 14)} L{f(sx + 52)} {f(alt - 14)} Z" fill="{su}"/>')
    for k in range(8):
        o.append(f'<path d="M{f(sx + 22 + k * 5)} {f(ust + 20 + k * 22)} l{f(30 + k * 4)} {f(60)}" stroke="#FFFFFF" stroke-width="3" opacity=".8"/>')
    for k in range(14):
        a = r.uniform(-2.6, -0.6)
        L = r.uniform(30, 90)
        o.append(f'<circle cx="{f(sx + 110 + math.cos(a) * L)}" cy="{f(alt - 20 + math.sin(a) * L * .6)}" r="{f(r.uniform(6, 16))}" fill="#FFFFFF" opacity="{f(r.uniform(.5, .9), 2)}"/>')
    # santral binası
    px = x0 + 60
    o.append(f'<rect x="{f(px)}" y="{f(alt - 70)}" width="190" height="70" fill="#D9C7A6" stroke="#5E666E" stroke-width="3"/>')
    o.append(f'<path d="M{f(px - 8)} {f(alt - 70)} H{f(px + 198)} L{f(px + 186)} {f(alt - 86)} H{f(px + 4)} Z" fill="#9C5A3A" stroke="#5E666E" stroke-width="2"/>')
    for k in range(5):
        o.append(f'<rect x="{f(px + 14 + k * 36)}" y="{f(alt - 56)}" width="20" height="26" fill="#5E7A8E"/>')
    return "".join(o)


def pilon(x, y, h, renk="#5E666E"):
    """Kafes enerji direği (temsilî)."""
    w = h * .22
    o = [f'<path d="M{f(x - w)} {f(y)} L{f(x - w * .2)} {f(y - h)} L{f(x + w * .2)} {f(y - h)} L{f(x + w)} {f(y)}" stroke="{renk}" stroke-width="4" fill="none"/>']
    for k in range(6):
        t0, t1 = k / 6, (k + 1) / 6
        xa, xb = w - (w * .8) * t0, w - (w * .8) * t1
        ya, yb = y - h * t0, y - h * t1
        o.append(f'<path d="M{f(x - xa)} {f(ya)} L{f(x + xb)} {f(yb)} M{f(x + xa)} {f(ya)} L{f(x - xb)} {f(yb)}" stroke="{renk}" stroke-width="2"/>')
    for t, kol in ((.78, 1.0), (.92, .75)):
        yy = y - h * t
        o.append(f'<path d="M{f(x - w * 1.5 * kol)} {f(yy)} H{f(x + w * 1.5 * kol)}" stroke="{renk}" stroke-width="4"/>')
        for sx in (-1, 1):
            o.append(f'<path d="M{f(x + sx * w * 1.45 * kol)} {f(yy)} v12" stroke="{renk}" stroke-width="2.4"/><circle cx="{f(x + sx * w * 1.45 * kol)}" cy="{f(yy + 14)}" r="3" fill="{renk}"/>')
    return "".join(o)


def kemaliye_evi(x, y, w, h, tohum, isik=-1, cati="#5E5A62", sivi="#FBF6EC", ahsap="#6E4A2E"):
    """Kemaliye (Eğin) evi (temsilî): taş zemin kat, beyaz sıvalı ahşap çatkılı üst katlar, sık pencereler, kırma çatı."""
    r = RNG(tohum)
    o = [f'<rect x="{f(x)}" y="{f(y - h * .3)}" width="{f(w)}" height="{f(h * .3)}" fill="#B8A48A" stroke="#5A4A3A" stroke-width="2"/>',
         f'<rect x="{f(x - w * .04)}" y="{f(y - h)}" width="{f(w * 1.08)}" height="{f(h * .7)}" fill="{sivi}" stroke="{ahsap}" stroke-width="3"/>']
    for k in range(1, 4):
        xx = x - w * .04 + w * 1.08 * k / 4
        o.append(f'<path d="M{f(xx)} {f(y - h)} V{f(y - h * .3)}" stroke="{ahsap}" stroke-width="3"/>')
    o.append(f'<path d="M{f(x - w * .04)} {f(y - h * .65)} H{f(x + w * 1.04)}" stroke="{ahsap}" stroke-width="3"/>')
    for kat in (0, 1):
        for k in range(4):
            px = x + w * (.05 + k * .26)
            py = y - h * (.92 - kat * .35)
            o.append(f'<rect x="{f(px)}" y="{f(py)}" width="{f(w * .14)}" height="{f(h * .2)}" fill="#3E5A6E" stroke="{ahsap}" stroke-width="2"/>')
            o.append(f'<path d="M{f(px + w * .07)} {f(py)} v{f(h * .2)}" stroke="#E9EEF2" stroke-width="1.6"/>')
    if isik < 0:
        o.append(f'<rect x="{f(x + w * .66)}" y="{f(y - h)}" width="{f(w * .38)}" height="{f(h)}" fill="#000" opacity=".1"/>')
    o.append(f'<path d="M{f(x - w * .12)} {f(y - h)} L{f(x + w * .2)} {f(y - h * 1.32)} L{f(x + w * .8)} {f(y - h * 1.32)} L{f(x + w * 1.12)} {f(y - h)} Z" fill="{cati}" stroke="#2E2A30" stroke-width="2"/>')
    return "".join(o)


def _ates(s, x, y, o=1.0):
    g = s.rad([(0, "#FFF4C8", .95), (.35, "#FFB43A", .6), (1, "#FF7A3D", 0)], x, y - 20 * o, 160 * o, kull="userSpaceOnUse", ad="at")
    return (f'<circle cx="{f(x)}" cy="{f(y - 20 * o)}" r="{f(160 * o)}" fill="{g}"/>'
            f'<path d="M{f(x - 26 * o)} {f(y)} l{f(52 * o)} {f(-10 * o)} M{f(x - 26 * o)} {f(y - 10 * o)} l{f(52 * o)} {f(10 * o)}" stroke="#5A3A22" stroke-width="{f(8 * o)}" stroke-linecap="round"/>'
            f'<path d="M{f(x - 18 * o)} {f(y - 6 * o)} Q{f(x - 22 * o)} {f(y - 40 * o)} {f(x)} {f(y - 66 * o)} Q{f(x + 22 * o)} {f(y - 40 * o)} {f(x + 18 * o)} {f(y - 6 * o)} Z" fill="#FF8A3D"/>'
            f'<path d="M{f(x - 9 * o)} {f(y - 6 * o)} Q{f(x - 10 * o)} {f(y - 28 * o)} {f(x)} {f(y - 44 * o)} Q{f(x + 10 * o)} {f(y - 28 * o)} {f(x + 9 * o)} {f(y - 6 * o)} Z" fill="#FFE08A"/>')


def _poz(ad, x, y, w):
    """Karakter sembolü (karakter.py); pamuk-* 140×160, pamuk-yuzer 120×80, pamuk-bayrak 170×200."""
    oran = {"pamuk-yuzer": 80 / 120, "pamuk-bayrak": 200 / 170}.get(ad, 160 / 140)
    return f'<use href="#{ad}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(w * oran)}"/>'


# ================================================================== 1. DURAK · DİVRİĞİ DEMİR OCAĞI (sabah)

def divrigi():
    s = Svg("m2-div")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    s += S.gunes(s, 1480, 132, 40, cekirdek="#FFF9E8", hale="#FFD3A0", hale_r=440, guc=.95)
    s += S.bulut(s, 1040, 110, 230, 511, ust="#FFFFFF", alt="#F6C8D0", op=.92)
    s += S.bulut(s, 1840, 66, 190, 512, ust="#FFFFFF", alt="#F9D3C4", op=.86)
    s += S.bulut_serit(s, 300, 200, 440, 10, "#FFE3EA", "#F6B8C8", .55)
    for i, (sol, sag, tx, ty, renk, golge) in enumerate(((-80, 900, 360, 196, "#A99BCB", "#8E83B8"), (700, 1500, 1120, 214, "#B6A6D4", "#9286BC"),
                                                         (1300, 2250, 1860, 176, "#A893C2", "#8A78AE"))):
        d, _ = S.dag(s, sol, sag, ufuk, tx, ty, 513 + i, renk=renk, golge=golge, bicim="tepe", sis="#F2CFE0", isik=-1, sirt=2, puruz=6)
        s += d
    d, _ = S.dag(s, -60, 820, ufuk + 20, 300, 236, 516, renk="#B9705A", golge="#8E4E42", bicim="tepe", sis="#F0C6B8", isik=-1, sirt=3, puruz=7)
    s += d
    s += _ova(s, ufuk + 6, 517, ust="#D6B07A", alt="#8E7A4A")
    s += _tarla(s, 0, 1200, ufuk + 20, 440, 518, renkler=("#D9B878", "#B9A45E", "#C98E5E", "#A7A45A"))
    # demir tepesi ve basamaklı ocak
    d, sirt = S.dag(s, 1030, 2260, ufuk + 90, 1690, 104, 519, renk="#B4553C", golge="#7E3326", bicim="tepe", sis="#E9A88E", isik=-1, sirt=4, puruz=10)
    s += d
    oc, sev = basamakli_ocak(s, sirt, 150, 372, 8, 520)
    s += oc
    for k, (yi, sx) in enumerate(((3, -1), (5, 1))):
        a = _kesisim_x(sirt, sev[yi])
        if a:
            s += kamyon(a[0] + 110 + k * 60 if sx > 0 else a[1] - 150, sev[yi] + 4, .8, yon=sx)
    s += cevher_yigini(s, 1960, 410, 230, 70, 521, renk="#3A2A28", parilti="#C9CDD2")
    s += cevher_yigini(s, 1240, 412, 160, 48, 522, renk="#4A2E28", parilti="#C9CDD2", n=8)
    # demiryolu ve cevher treni (ön)
    s += f'<path d="M0 436 C600 426 1300 440 2100 430" stroke="#8E7A5A" stroke-width="22" fill="none" opacity=".55"/>'
    s += tren(s, 420, 430, 5, 523)
    s += kavak_sirasi(s, (60, 92, 124, 1120, 1152), 400, 120, 22, 524, renk="#5E9644")
    s += evler(s, 230, 3, 404, 525, duvar="#EFDCC0", cati="#A9473A")
    s += S.cimen(1300, 2100, 452, 526, renk="#6E7A3A", renk2="#9DA85A", boy=12, cicek=["#FFFFFF", "#F0A21A"])
    s += _poz("pamuk-otur", 1880, 236, 110)
    s += S.marti(1180, 168, .8, 2, renk="#5A4A7A")
    s += S.marti(1236, 186, .6, -1, renk="#5A4A7A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 2. DURAK · GULEMAN KROM OCAKLARI (öğle)

def guleman():
    s = Svg("m2-gul")
    ufuk = 292
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 1960, 76, 34, hale="#FFF2C2", hale_r=330, guc=.8)
    for i, (x, y, w) in enumerate([(760, 112, 220), (1150, 82, 270), (1560, 130, 180), (380, 170, 150)]):
        s += S.bulut(s, x, y, w, 530 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    d, _ = S.dag(s, 600, 2260, ufuk, 1400, 120, 534, renk="#7E9CBE", golge="#5C7AA4", bicim="tepe", sis="#CFE6F2", isik=-1, sirt=3, puruz=8)
    s += d
    d, _ = S.dag(s, -80, 900, ufuk, 300, 168, 535, renk="#8DA9C6", golge="#6E8EB2", bicim="tepe", sis="#D6ECF5", isik=-1, sirt=2, puruz=6)
    s += d
    # ofiyolit tepeleri: koyu yeşil-gri serpantin, zeytuni lekeler
    d, sirt1 = S.dag(s, 980, 1700, ufuk + 60, 1330, 190, 536, renk="#5E6E58", golge="#3A4538", bicim="tepe", sis="#9DB0A0", isik=-1, sirt=4, puruz=12)
    s += d
    d, sirt2 = S.dag(s, 1400, 2300, ufuk + 80, 1880, 130, 537, renk="#4E5C4C", golge="#2E3830", bicim="tepe", sis="#8EA294", isik=-1, sirt=5, puruz=14)
    s += d
    r = RNG(538)
    for _ in range(26):
        x, y = r.uniform(1450, 2080), r.uniform(190, 360)
        a = _kesisim_x(sirt2, y)
        if a and a[0] + 30 < x < a[1] - 30:
            s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r.uniform(14, 40))}" ry="{f(r.uniform(5, 12))}" fill="{r.choice(["#7E8A5A", "#6A7A50", "#2A302C"])}" opacity=".55"/>'
    s += _ova(s, ufuk + 20, 539, ust="#B9C27A", alt="#6E8A48")
    # dere
    dere = [(2100, 372), (1700, 392), (1320, 380), (900, 410), (500, 420), (0, 446)]
    s += f'<path d="{egri_d(dere)}" stroke="#4FB6C8" stroke-width="22" fill="none" stroke-linecap="round"/>'
    s += f'<path d="{egri_d(dere)}" stroke="#BFEFF6" stroke-width="5" fill="none" stroke-dasharray="30 26"/>'
    s += kavak_sirasi(s, (140, 172, 204, 640, 672, 1060, 1092, 1124), 404, 128, 22, 540, renk="#5A9C47")
    s += evler(s, 1140, 5, 372, 541, ara=56, duvar="#F3EADA", cati="#C2563A", duz=False)
    # galeri, raylar, vagonetler, kromit yığını
    s += galeri(s, 1700, 352, 110, 120, 542, kaya="#2E3830")
    s += raylar(1700, 352, 2120, 400)
    s += vagonet(s, 1840, 372, .95)
    s += vagonet(s, 1975, 387, .95)
    s += cevher_yigini(s, 1520, 400, 210, 70, 543, renk="#1E2224", parilti="#6FD08A")
    s += _poz("pamuk-selam", 1932, 192, 104)
    s += S.cimen(0, 2100, 456, 544, renk="#4E7A36", renk2="#7DAE52", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 3. DURAK · MADEN · DİCLE VADİSİNDE BAKIR (ikindi)

def maden():
    s = Svg("m2-mad")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3E8ED4"), (.55, "#A9D7EE"), (.85, "#F7E3C0"), (1, "#FCD9A8")])
    s += S.gunes(s, 1820, 104, 38, cekirdek="#FFF7E0", hale="#FFD58A", hale_r=380, guc=.9)
    for i, (x, y, w) in enumerate([(820, 104, 230), (1240, 70, 260), (1600, 150, 170)]):
        s += S.bulut(s, x, y, w, 550 + i, ust="#FFFFFF", alt="#F6DCC2", op=.92)
    d, _ = S.dag(s, 700, 2260, ufuk, 1500, 120, 553, renk="#9C8AB0", golge="#7A6A96", bicim="tepe", sis="#F2D8C8", isik=-1, sirt=3, puruz=8)
    s += d
    # V biçimli vadi: sol yamaç ve sağ yamaç
    d, _ = S.dag(s, -120, 1300, 470, 120, 160, 554, renk="#B49A6A", golge="#8C7448", bicim="tepe", sis="#E9D2A8", isik=-1, sirt=4, puruz=10)
    s += d
    d, sirt = S.dag(s, 1150, 2300, 470, 1980, 150, 555, renk="#A6845A", golge="#7A5E3E", bicim="tepe", sis="#E2C69A", isik=-1, sirt=5, puruz=12)
    s += d
    r = RNG(556)
    for _ in range(30):
        x, y = r.uniform(1300, 2080), r.uniform(200, 440)
        a = _kesisim_x(sirt, y)
        if a and a[0] + 20 < x < a[1] - 10:
            s += f'<path d="M{f(x)} {f(y)} q{f(r.uniform(10, 30))} {f(r.uniform(-6, 6))} {f(r.uniform(30, 70))} {f(r.uniform(6, 20))}" stroke="{r.choice(["#3FA88A", "#5BC2A0", "#C8743A", "#2E8A74"])}" stroke-width="{f(r.uniform(4, 9))}" fill="none" stroke-linecap="round" opacity=".7"/>'
    # Dicle (Maden çayı)
    nehir = [(1280, 300), (1210, 340), (1240, 380), (1120, 420), (900, 446), (700, 470)]
    s += f'<path d="{egri_d(nehir)}" stroke="#3E9CB8" stroke-width="30" fill="none" stroke-linecap="round"/>'
    s += f'<path d="{egri_d(nehir)}" stroke="#CFF2F8" stroke-width="5" fill="none" stroke-dasharray="26 22"/>'
    # cüruf yığınları, eski baca, galeriler
    for k, (x, w, h) in enumerate(((1420, 200, 70), (1600, 150, 52))):
        s += cevher_yigini(s, x, 440, w, h, 557 + k, renk="#1E1A1C", parilti="#5E6A7A", n=8)
    s += f'<path d="M1540 384 L1552 214 H1584 L1596 384 Z" fill="#A65A3E" stroke="#4A2A1E" stroke-width="3"/>'
    for k in range(7):
        s += f'<path d="M{1545 + k * 1.4} {380 - k * 24} H{1591 - k * 1.4}" stroke="#7A3E2A" stroke-width="2"/>'
    s += f'<rect x="1546" y="206" width="44" height="12" fill="#7A3E2A"/>'
    s += galeri(s, 1820, 300, 84, 92, 558, kaya="#6E5638")
    s += galeri(s, 1980, 372, 90, 98, 559, kaya="#6E5638")
    s += raylar(1980, 372, 1760, 430)
    s += vagonet(s, 1860, 412, .85, cevher="#2E6E5A", parilti="#E9A060")
    s += kavak_sirasi(s, (980, 1012, 1044, 1290, 1322), 432, 116, 20, 560, renk="#5A9A46")
    # taş köprü (temsilî)
    s += f'<path d="M820 452 Q900 380 980 452" stroke="#C9B08A" stroke-width="26" fill="none"/>'
    s += f'<path d="M790 446 H1010" stroke="#B49A72" stroke-width="12"/>'
    s += _poz("pamuk-dusunen", 1700, 262, 96)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 4. DURAK · HAZAR GÖLÜ (altın saat)

def hazar():
    s = Svg("m2-haz")
    ufuk = 252
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "altin")
    s += S.gunes(s, 1500, 186, 44, cekirdek="#FFF8E0", hale="#FFC86A", hale_r=520, guc=.95)
    s += S.bulut_serit(s, 820, 90, 520, 14, "#FFF2D0", "#F6C898", .7)
    s += S.bulut_serit(s, 1500, 70, 420, 12, "#FFF2D0", "#F6C898", .6)
    sol, _ = S.dag(s, -140, 1080, ufuk, 380, 70, 561, renk="#8C86B8", golge="#6A66A0", bicim="sivri", kar_y=128, kar="#FFFFFF",
                   kar_golge="#D9D2EE", sis="#F7D9B8", isik=-1, sirt=4)
    orta, _ = S.dag(s, 900, 1700, ufuk, 1300, 168, 562, renk="#9A8EB8", golge="#7C70A0", bicim="tepe", sis="#F7D9B8", isik=-1, sirt=2, puruz=6)
    sag, _ = S.dag(s, 1500, 2280, ufuk, 1960, 110, 563, renk="#8478AE", golge="#62588E", bicim="sivri", kar_y=150, kar="#FFFFFF",
                   kar_golge="#D2CAE6", sis="#F2D2B8", isik=-1, sirt=4)
    s += orta + sol + sag
    s += S.gol(s, 0, ufuk, W, H - ufuk, 564, ufuk="#A9D8F2", orta="#2A78C2", derin="#0B3A78", gunes_x=1500,
               parilti_renk="#FFE3A0", cizgi_renk="#DDEEFF")
    s += S.yansima(s, sol + orta + sag, ufuk, 0, W, 120, op=.32)
    # sağ ön: iskele, sandal, dalgıç şamandırası, sazlık
    s += Y.iskele(s, 1660, 2120, 372, 26, 565, ahsap="#9A6B42")
    s += S.tekne(s, 1760, 418, 150, govde="#C8442F", ust="#F4E9D8")
    s += f'<path d="M1300 404 V330" stroke="#3A3A44" stroke-width="5"/><rect x="1300" y="330" width="58" height="40" fill="#E2263A"/>'
    s += f'<path d="M1300 330 L1358 370" stroke="#FFFFFF" stroke-width="8"/>'
    s += f'<ellipse cx="1300" cy="406" rx="22" ry="8" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += S.dalga_cizgileri(1180, 390, 300, 50, 566, op=.7, n=8, k=2.2)
    s += _poz("pamuk-yuzer", 1400, 382, 110)
    s += S.sazlik(0, 420, 462, 567, boy=60)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 5. DURAK · KEBAN BARAJ GÖLÜ · KARASU İLE MURAT'IN BULUŞTUĞU YER (sabah)

def firat_kavsagi():
    s = Svg("m2-fir")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    s += S.gunes(s, 1640, 150, 40, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=420, guc=.92)
    s += S.bulut(s, 1120, 118, 240, 571, ust="#FFFFFF", alt="#F6C8D0", op=.9)
    s += S.bulut(s, 1900, 84, 160, 572, ust="#FFFFFF", alt="#F9D3C4", op=.85)
    d, _ = S.dag(s, 800, 2260, ufuk, 1560, 96, 573, renk="#A9A0D0", golge="#8A80BA", bicim="sivri", kar_y=150, kar="#FFFFFF",
                 kar_golge="#DAD4EE", sis="#F4D3DE", isik=-1, sirt=4)
    s += d
    # iki kolun arasındaki burun ve iki yandaki yamaçlar (okr, katmanlı)
    d1, _ = S.dag(s, -80, 1180, ufuk + 40, 380, 176, 574, renk="#C9A66B", golge="#9C7A4A", bicim="tepe", sis="#F2D6B8", isik=-1, sirt=3, puruz=8)
    s += d1
    s += S.gol(s, 0, ufuk + 30, W, H - ufuk - 30, 575, ufuk="#BCEDE8", orta="#34B2AC", derin="#0E6A73", gunes_x=1640, parilti_renk="#FFF0C0")
    burun = [(1180, ufuk + 34), (1300, ufuk + 6), (1420, ufuk - 4), (1520, ufuk + 18), (1600, ufuk + 40), (1180, ufuk + 40)]
    g = s.lin([(0, "#C8A86E"), (1, "#8E7446")], 0, ufuk - 10, 0, ufuk + 40, kull="userSpaceOnUse", ad="br")
    s += f'<path d="{cizgi_d(burun, True)}" fill="{g}"/>'
    d2, _ = S.dag(s, 1700, 2300, ufuk + 60, 2050, 150, 576, renk="#B8925A", golge="#8A6A3E", bicim="tepe", sis="#EAD0A8", isik=-1, sirt=3, puruz=8)
    s += d2
    for k in range(5):
        y = 200 + k * 20
        s += f'<path d="M{1760 + k * 18} {y} q120 -10 260 6" stroke="#8A6A3E" stroke-width="3" fill="none" opacity=".45"/>'
    # iki kolun su çizgileri birbirine karışıyor
    for k in range(6):
        y = ufuk + 52 + k * 18
        s += f'<path d="M{900 + k * 40} {y} Q1300 {y - 10} 1560 {y + 6}" stroke="#E6FBF8" stroke-width="2.6" fill="none" opacity=".6"/>'
        s += f'<path d="M2100 {y + 4} Q1840 {y + 10} 1600 {y + 6}" stroke="#E6FBF8" stroke-width="2.6" fill="none" opacity=".6"/>'
    s += kavak_sirasi(s, (1340, 1372, 1404, 1436), ufuk + 26, 70, 13, 577, renk="#5E9A4A")
    s += S.agac(s, 1490, ufuk + 30, 16, 578, renk="#6EA84E", meyve="#F0A21A")
    s += S.tekne(s, 1690, 400, 170, govde="#2B50B5", ust="#F4E9D8")
    s += _poz("pamuk-otur", 1706, 290, 92)
    s += S.marti(1240, 170, .8, 2, renk="#5A4A7A")
    s += S.marti(1300, 196, .6, -1, renk="#5A4A7A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 6. DURAK · KEBAN · BARAJ VE GÜMÜŞLÜ KURŞUN OCAKLARI (öğle)

def keban():
    s = Svg("m2-keb")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 1180, 70, 32, hale="#FFF2C2", hale_r=300, guc=.8)
    for i, (x, y, w) in enumerate([(700, 120, 210), (1500, 76, 230), (1960, 140, 150)]):
        s += S.bulut(s, x, y, w, 580 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    d, _ = S.dag(s, -80, 1100, ufuk, 360, 170, 583, renk="#C2A87A", golge="#98805A", bicim="tepe", sis="#E9DCC0", isik=-1, sirt=3, puruz=7)
    s += d
    # sol ve sağ kayalık yamaçlar (baraj ayakları)
    d, _ = S.dag(s, 1080, 1560, 470, 1360, 120, 584, renk="#B39A78", golge="#86704E", bicim="tepe", sis="#E6D6B8", isik=-1, sirt=4, puruz=10)
    s += d
    d, _ = S.dag(s, 1900, 2320, 470, 2160, 96, 585, renk="#A88E6A", golge="#7A6448", bicim="tepe", sis="#E2D0B0", isik=-1, sirt=4, puruz=10)
    s += d
    s += f'<rect x="1380" y="150" width="620" height="40" fill="#5FB0C8"/>'
    s += baraj(s, 1420, 1960, 162, 410, 586)
    # mansapta Fırat
    nehir = [(1600, 410), (1400, 430), (1100, 440), (700, 452), (300, 466)]
    s += f'<path d="{egri_d(nehir)}" stroke="#4DB2C4" stroke-width="34" fill="none" stroke-linecap="round"/>'
    s += f'<path d="{egri_d(nehir)}" stroke="#D8F6FA" stroke-width="5" fill="none" stroke-dasharray="30 24"/>'
    # enerji hattı
    s += pilon(1240, 300, 190) + pilon(1080, 330, 150)
    s += f'<path d="M1240 152 Q1600 200 1950 168 M1080 213 Q1160 196 1240 152" stroke="#3A3E48" stroke-width="2" fill="none"/>'
    # eski gümüşlü kurşun galerileri ve atık yığınları (sol alt)
    s += _ova(s, 380, 587, ust="#C9B07A", alt="#8E8A52", x1=1200)
    for k, (x, y) in enumerate(((420, 420), (640, 410))):
        s += galeri(s, x, y, 64, 70, 588 + k, kaya="#7A6A50")
        s += f'<path d="M{x + 40} {y} q90 -30 170 0 Z" fill="#D9C79A" stroke="#9C8A5E" stroke-width="2"/>'
    s += evler(s, 820, 5, 420, 590, ara=60, duvar="#F1E4CC", cati="#B8553A")
    s += kavak_sirasi(s, (60, 92, 980, 1012, 1044), 430, 120, 20, 591, renk="#5A9A46")
    s += _poz("pamuk-akce", 1990, 290, 92)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== HÜLASA · FIRAT KIYISINDA KAMP (alacakaranlık, 40 mm)

def firat_kamp(h=400):
    s = Svg("m2-kmp")
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "alaca")
    s += S.yildizlar(s, 0, 0, W, 150, 70, 600)
    s += S.ay(s, 1340, 70, 24, golge_renk="#43346F")
    sol, _ = S.dag(s, -100, 1000, ufuk, 300, 120, 601, renk="#4E3E78", golge="#382C5E", bicim="tepe", sis="#C25E83", isik=-1, sirt=2, puruz=6)
    sag, _ = S.dag(s, 900, 2260, ufuk, 1800, 96, 602, renk="#5A4682", golge="#3E3066", bicim="tepe", sis="#D4708A", isik=-1, sirt=3, puruz=7)
    s += sol + sag
    s += S.gol(s, 0, ufuk, W, h - ufuk, 603, ufuk="#C88AA8", orta="#5A4E8E", derin="#22204E", gunes_x=1340, parilti_renk="#FFE0C0", cizgi_renk="#E0C8F0")
    s += S.yansima(s, sol + sag, ufuk, 0, W, 90, op=.3)
    kiyi = [(1300, h), (1360, 330), (1500, 300), (1800, 290), (2100, 296), (2100, h)]
    g = s.lin([(0, "#5E4A5A"), (1, "#2E2234")], 0, 290, 0, h, kull="userSpaceOnUse", ad="ky")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {h} Z" fill="{g}"/>'
    s += _ates(s, 1640, 352, .9)
    s += Y.cadir(s, 1880, 340, 200, 150, renk="#C8442F", serit="#F5E8D0")
    s += f'<circle cx="1960" cy="276" r="40" fill="#FFD27A" opacity=".18"/>'
    s += _poz("pamuk-otur", 1490, 260, 92)
    s += kavak_sirasi(s, (2040, 2070), 300, 110, 18, 604, renk="#3E3A5A")
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== MECLİS · KEMALİYE (EĞİN) EVLERİ (öğle)

def kemaliye():
    s = Svg("m2-kem")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 1080, 66, 30, hale="#FFF2C2", hale_r=300, guc=.8)
    for i, (x, y, w) in enumerate([(640, 110, 200), (1500, 90, 220)]):
        s += S.bulut(s, x, y, w, 610 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    d, _ = S.dag(s, -100, 1000, 470, 260, 150, 612, renk="#B79A78", golge="#8A7254", bicim="tepe", sis="#E8D8C0", isik=-1, sirt=4, puruz=12)
    s += d
    d, sirt = S.dag(s, 1100, 2300, 470, 1900, 60, 613, renk="#A98E6E", golge="#7C664C", bicim="tepe", sis="#E2D2B8", isik=-1, sirt=5, puruz=14)
    s += d
    # kanyon dibinde Fırat
    nehir = [(1250, 300), (1150, 360), (1080, 420), (980, 470)]
    s += f'<path d="{egri_d(nehir)}" stroke="#3FAEA8" stroke-width="40" fill="none" stroke-linecap="round"/>'
    s += f'<path d="{egri_d(nehir)}" stroke="#D2F4EE" stroke-width="5" fill="none" stroke-dasharray="26 22"/>'
    # yamaçta evler ve meyve ağaçları
    r = RNG(614)
    yer = [(1300, 300), (1430, 270), (1560, 236), (1700, 214), (1380, 380), (1520, 350), (1660, 318), (1820, 290), (1960, 262),
           (1600, 430), (1760, 400), (1920, 372)]
    for k, (x, y) in enumerate(yer):
        s += S.agac(s, x - 30 + r.uniform(-10, 10), y + 8, 20, 615 + k, renk="#5E9A46", meyve="#F0A21A" if k % 2 else "#7A2E3A")
    for k, (x, y) in enumerate(yer):
        w_ = 96 + (k % 3) * 14
        s += kemaliye_evi(x, y, w_, w_ * .9, 630 + k)
    s += kavak_sirasi(s, (1180, 1212), 440, 110, 18, 650, renk="#5E9A46")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== KISSA · KARANLIK KANYON (öğle)

def karanlik_kanyon():
    s = Svg("m2-kan")
    s += S.gokyuzu(s, 0, 0, W, 300, "gun")
    s += S.bulut(s, 760, 110, 220, 660, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    s += S.bulut(s, 1260, 70, 180, 661, ust="#FFFFFF", alt="#CFE3F1", op=.9)
    # uzak kanyon ağzı
    d, _ = S.dag(s, 700, 1700, 330, 1200, 170, 662, renk="#B9A2C8", golge="#9884B0", bicim="tepe", sis="#E2D8EC", isik=-1, sirt=2, puruz=6)
    s += d
    s += f'<path d="M1080 470 Q1170 380 1200 330 Q1240 380 1330 470 Z" fill="#3E9CA8"/>'
    # sol duvar (gölgede) ve sağ duvar (güneşte), katmanlı kalker
    sol = [(-40, 0), (380, 0), (560, 120), (700, 210), (930, 330), (1100, 470), (-40, 470)]
    g1 = s.lin([(0, "#6A5A6E"), (1, "#3E3446")], 0, 0, 1, 0, ad="sl")
    s += f'<path d="{cizgi_d(sol, True)}" fill="{g1}"/>'
    sag = [(2140, 0), (1780, 0), (1640, 120), (1500, 230), (1400, 330), (1330, 470), (2140, 470)]
    g2 = s.lin([(0, "#E8C48E"), (1, "#B8925E")], 0, 0, 1, 0, ad="sg")
    s += f'<path d="{cizgi_d(sag, True)}" fill="{g2}"/>'
    r = RNG(663)
    for k in range(12):
        y = 30 + k * 38
        s += f'<path d="M{f(1700 - k * 30)} {y} L2140 {f(y + r.uniform(-8, 8))}" stroke="#A67C4A" stroke-width="3" opacity=".5"/>'
    # kayaya oyulmuş yol ve tünel ağızları
    yol = [(1360, 440), (1460, 360), (1580, 280), (1720, 210), (1880, 150), (2140, 96)]
    s += f'<path d="{cizgi_d(yol)}" stroke="#D9BC8A" stroke-width="22" fill="none" stroke-linejoin="round"/>'
    s += f'<path d="{cizgi_d(yol)}" stroke="#8E6E44" stroke-width="3" fill="none" transform="translate(0 12)"/>'
    for (x, y) in ((1520, 318), (1800, 178), (2040, 118)):
        s += f'<path d="M{x - 30} {y + 12} V{y - 22} Q{x} {y - 52} {x + 30} {y - 22} V{y + 12} Z" fill="#2A2026"/>'
    for k in range(6):
        x = 1250 + k * 30
        s += f'<path d="M{x} 0 L{x + 160} 470" stroke="#FFF4C8" stroke-width="22" opacity=".07"/>'
    s += _poz("pamuk-sasiran", 1610, 160, 92)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== ANAHTAR · DİVRİĞİ KALESİ YOKUŞU (ikindi)

def kale_yokusu():
    s = Svg("m2-yok")
    ufuk = 330
    s += S.gokyuzu(s, 0, 0, W, ufuk, duraklar=[(0, "#4C8ED0"), (.6, "#BFDDEE"), (1, "#FCE2B8")])
    s += S.gunes(s, 1060, 120, 34, cekirdek="#FFF7E0", hale="#FFD58A", hale_r=340, guc=.85)
    s += S.bulut(s, 760, 90, 200, 670, ust="#FFFFFF", alt="#F2DCC8", op=.9)
    d, _ = S.dag(s, -80, 1100, ufuk, 400, 210, 671, renk="#C08A70", golge="#946452", bicim="tepe", sis="#F2CCB4", isik=-1, sirt=3, puruz=8)
    s += d
    s += _ova(s, ufuk, 672, ust="#D2AE7A", alt="#8E7A4A")
    kale, sirt = kale_sirti(s, 1180, 2240, 470, 120, 673, kaya="#8A6252", golge="#5A3E36", tas="#D6B08E", tas_g="#8E6A52")
    s += kale
    # kıvrılan taş merdiven
    yol = [(1180, 470), (1320, 430), (1460, 400), (1380, 352), (1520, 316), (1660, 290), (1580, 248), (1700, 214)]
    s += f'<path d="{cizgi_d(yol)}" stroke="#E9D2AE" stroke-width="30" fill="none" stroke-linejoin="round"/>'
    for (xa, ya), (xb, yb) in zip(yol, yol[1:]):
        L = math.hypot(xb - xa, yb - ya)
        for k in range(int(L / 22)):
            t = k / (L / 22)
            mx, my = xa + (xb - xa) * t, ya + (yb - ya) * t
            a = math.atan2(yb - ya, xb - xa) + math.pi / 2
            s += f'<path d="M{f(mx - 14 * math.cos(a))} {f(my - 14 * math.sin(a))} L{f(mx + 14 * math.cos(a))} {f(my + 14 * math.sin(a))}" stroke="#A88A62" stroke-width="2.4"/>'
    s += evler(s, 120, 8, 430, 674, ara=110, w=60, h=40, duvar="#EFDCC0", cati="#A9473A")
    s += kavak_sirasi(s, (60, 960, 992, 1024), 440, 120, 20, 675, renk="#5A9A46")
    s += _poz("pamuk-selam", 1556, 230, 86)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== İMTİHAN · DİVRİĞİ KALESİ (gün batımı, 51 mm)

def divrigi_kalesi(h=510):
    s = Svg("m2-kal")
    ufuk = 360
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2F4FA0"), (.36, "#8A8AC8"), (.66, "#F6A99A"), (1, "#FFC07A")])
    s += S.gunes(s, 360, 300, 54, hale="#FFB45A", hale_r=560, guc=.95)
    for i, (x, y, w) in enumerate([(640, 120, 300), (1060, 70, 320), (1560, 110, 260)]):
        s += S.bulut(s, x, y, w, 680 + i, ust="#FFF4E4", alt="#F0A98A", op=.92)
    s += S.bulut_serit(s, 160, 230, 560, 16, "#FFD8B0", "#F08A7A", .6)
    d, _ = S.dag(s, -80, 1000, ufuk, 360, 240, 683, renk="#A58DAE", golge="#87709A", bicim="tepe", sis="#F6C3AA", isik=-1, sirt=2, puruz=5)
    s += d
    d, _ = S.dag(s, 700, 1600, ufuk, 1200, 270, 684, renk="#B56A5A", golge="#8A4A44", bicim="tepe", sis="#F2B09A", isik=-1, sirt=3, puruz=6)
    s += d
    s += _ova(s, ufuk, 685, ust="#C9926A", alt="#7E6A48", h=h)
    s += _tarla(s, 0, 1000, ufuk + 10, h - 30, 686, renkler=("#E0A86A", "#C9985A", "#B8A060", "#D9906A"))
    kale, _ = kale_sirti(s, 1060, 2200, ufuk + 110, 110, 687, kaya="#7E5648", golge="#4E3432", tas="#D8AE8A", tas_g="#8A644E", bayrak=True)
    s += kale
    s += evler(s, 120, 12, ufuk + 112, 688, ara=78, w=52, h=36, duvar="#F0D8BC", cati="#A6463A")
    s += kavak_sirasi(s, (40, 70, 960, 990, 1020), ufuk + 128, 150, 24, 689, renk="#5E8A3E")
    s += S.cimen(0, 2100, h - 4, 690, renk="#6E7A3A", renk2="#9DA85A", boy=16, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    for k, (x, y, o) in enumerate([(700, 200, 1.1), (780, 232, .8), (1180, 140, .7)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== CEVAPLAR · DİVRİĞİ GECESİ (30 mm)

def divrigi_gece(h=300):
    s = Svg("m2-gec")
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, h, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 40, 150, 700)
    s += S.ay(s, 1180, 70, 28, golge_renk="#13204A")
    d, _ = S.dag(s, -80, 1100, ufuk + 10, 380, 150, 701, renk="#2E2C52", golge="#1E1C3E", bicim="tepe", isik=-1, sirt=2, puruz=6)
    s += d
    kale, _ = kale_sirti(s, 1380, 2140, ufuk + 40, 40, 702, kaya="#2E2A4A", golge="#1A1832", tas="#4A4878", tas_g="#2A2850", gece=True)
    s += kale
    g = s.lin([(0, "#1E2A55"), (1, "#0E1636")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="sz")
    s += f'<rect x="0" y="{ufuk + 20}" width="{W}" height="{h - ufuk}" fill="{g}"/>'
    s += evler(s, -20, 24, ufuk + 62, 703, ara=92, w=60, h=38, duvar="#3A3A5E", cati="#2A2244")
    r = RNG(704)
    for _ in range(60):
        x = r.uniform(0, W)
        s += f'<rect x="{f(x)}" y="{f(ufuk + r.uniform(36, 52))}" width="6" height="7" fill="#FFD27A" opacity="{f(r.uniform(.6, 1), 2)}"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== FİNAL · DİVRİĞİ KALESİ BURCUNDA PAMUK (89 mm)

def divrigi_final(nisanlar=None, h=900):
    s = Svg("m2-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    gx, gy = 760, ufuk - 30
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += (f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} '
              f'L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE0A0" opacity=".12"/>')
    s += S.gunes(s, gx, gy, 70, hale="#FFC56B", hale_r=700, guc=.95)
    for (x, y, w_, k) in ((200, 260, 520, 22), (1200, 180, 640, 26), (1500, 330, 480, 16), (100, 420, 380, 12)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC59A", "#FF6F8A", .75)
    d, _ = S.dag(s, 980, 1900, ufuk, 1400, 340, 711, renk="#B8606A", golge="#7E3E5A", bicim="tepe", sis="#FF9A8A", isik=-1, sirt=3, puruz=8)
    s += d
    d, _ = S.dag(s, -100, 760, ufuk, 300, 420, 712, renk="#8A4A5E", golge="#5E3448", bicim="tepe", sis="#E07A8A", isik=-1, sirt=2, puruz=6)
    s += d
    s += _ova(s, ufuk, 713, ust="#C9806A", alt="#6E4E5A", h=h)
    s += _tarla(s, 0, W, ufuk + 6, 700, 714, n=40, renkler=("#D9906A", "#B97A70", "#C9905A", "#A97A7E"))
    s += evler(s, -30, 26, 704, 715, ara=84, w=58, h=40, duvar="#F2D2C0", cati="#9C3A40")
    # burç (ön plan)
    g = s.lin([(0, "#8A6A6E"), (1, "#4E3A44")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    s += f'<rect x="0" y="720" width="{W}" height="{h - 720}" fill="{g}"/>'
    r = RNG(716)
    for row in range(6):
        y = 724 + row * 30
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            s += f'<rect x="{x + 2}" y="{y}" width="86" height="27" rx="3" fill="{karis("#A27C6E", "#5E4650", r.uniform(0, .6))}" stroke="#3E2C34" stroke-width="1.6"/>'
    for x in range(0, W, 150):
        s += f'<rect x="{x}" y="660" width="96" height="64" fill="#94706A" stroke="#3E2C34" stroke-width="2.6"/>'
        s += f'<rect x="{x}" y="660" width="96" height="10" fill="#B88A80"/>'
    s.tanim(f'<linearGradient id="{s.onek}-tk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B88A80"/>'
            f'<stop offset=".6" stop-color="#8E6A66"/><stop offset="1" stop-color="#5E4650"/></linearGradient>')
    s += f'<rect x="1560" y="560" width="420" height="{h - 560}" fill="url(#{s.onek}-tk)" stroke="#3E2C34" stroke-width="3"/>'
    for x in range(1560, 1980, 84):
        s += f'<rect x="{x}" y="510" width="54" height="56" fill="#A27C72" stroke="#3E2C34" stroke-width="2.6"/>'
    s += f'<path d="M1740 {h} V760 Q1740 720 1770 712 Q1800 720 1800 760 V{h} Z" fill="#2E1E24"/>'
    s += '<use href="#pamuk-bayrak" x="1600" y="150" width="340" height="400"/>'
    s += f'<path d="M260 650 V330" stroke="#6B4A2E" stroke-width="10"/><circle cx="260" cy="324" r="10" fill="#C9952B"/>'
    s += f'<path d="M260 360 Q900 520 1640 330" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .6) / (len(nisanlar) + .2)
            x = (1 - t) ** 2 * 260 + 2 * (1 - t) * t * 900 + t * t * 1640
            y = (1 - t) ** 2 * 360 + 2 * (1 - t) * t * 520 + t * t * 330
            s += f'<path d="M{f(x)} {f(y)} v18" stroke="#5A3A22" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 62)} {f(y + 14)}) rotate({f((k % 2 * 2 - 1) * 5)} 62 70)">{ns}</g>'
    for k in range(60):
        x = r.uniform(300, 1900)
        y = r.uniform(80, 640)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== AÇILIŞ · SİVAS–ELAZIĞ YOL HARİTASI (110 mm)

# stilize harita konumları (birim; mm = /10). Yönler korunur (batı solda, kuzey yukarıda); mesafeler okunurluk için
# sıkıştırılıp açılmıştır. Gerçek konumlar meta.json'da (enlem–boylam). Rota bir halkadır: Divriği'den çıkar, Murat
# vadisinden Guleman'a iner, Maden ve Hazar üzerinden Fırat'a döner, Keban'dan Divriği Kalesi'ne çıkar.
HARITA = {"1": (420, 560), "2": (1900, 850), "3": (1640, 980), "4": (1330, 930), "5": (960, 700), "6": (760, 820), "K": (215, 470)}
ROTA_ARA = {("1", "2"): [(700, 470), (1150, 500), (1600, 600), (1820, 700)], ("2", "3"): [(1810, 960)], ("3", "4"): [(1480, 1000)],
            ("4", "5"): [(1180, 870), (1060, 790)], ("5", "6"): [(860, 730)], ("6", "K"): [(560, 790), (330, 690), (240, 580)]}


def panorama_rota(h=1100):
    """Açılış haritası: Doğu Anadolu platosu; pas kızılı Divriği tepeleri ve kale, Fırat'ın iki kolu (Karasu, Murat) ve
    Keban Baraj Gölü, baraj, Hazar Gölü'nün mavisi, Dicle'nin başı, Maden'in bakır yeşili, Guleman'ın koyu krom tepeleri.
    Döndürür: (svg, konum)."""
    s = Svg("m2-har")
    ufuk = 330
    s += S.gokyuzu(s, 0, 0, W, ufuk + 8, "gunbatimi")
    s += S.gunes(s, 1300, ufuk - 40, 50, hale="#FFC56B", hale_r=620, guc=.9)
    for (x, y, w_, kk) in ((620, 140, 520, 18), (1260, 96, 620, 22), (1720, 210, 400, 14), (120, 220, 340, 12)):
        s += S.bulut_serit(s, x, y, w_, kk, "#FFC9A0", "#FF7A8A", .75)
    for i, (sol, sag, tx, ty, bic, renk, golge, kar) in enumerate((
            (-120, 900, 360, 180, "sivri", "#B08AB0", "#7A5C8E", 236), (600, 1500, 1060, 160, "tepe", "#C08FB0", "#8A6A9E", None),
            (1300, 2240, 1820, 170, "sivri", "#A9789E", "#7B5A8C", 226))):
        d_, _ = S.dag(s, sol, sag, ufuk + 8, tx, ty, 900 + i, renk=renk, golge=golge, bicim=bic, kar_y=kar,
                      kar="#FFE6EE", kar_golge="#C6A7D2", sis="#FFA18E", isik=-1, sirt=3, puruz=7)
        s += d_
    gk = s.lin([(0, "#C9A27E"), (.18, "#C8A870"), (.55, "#AFA25E"), (1, "#7E8E48")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kr")
    s += f'<rect x="0" y="{ufuk + 6}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    r = RNG(905)
    for _ in range(70):
        x, y = r.uniform(-60, 2100), r.uniform(ufuk + 30, h - 20)
        t = (y - ufuk) / (h - ufuk)
        w_ = r.uniform(70, 170) * (.45 + t)
        hh = w_ * .3 * (.4 + t)
        c = r.choice(["#C9B260", "#A8AE58", "#D3B06A", "#93A452", "#C99A50", "#B6B86A"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w_)} {f(-hh * .2)} l{f(-w_ * .2)} {f(hh)} l{f(-w_)} {f(hh * .2)} Z" fill="{c}" opacity=".45"/>'
    # Divriği: pas kızılı tepeler + basamaklı ocak + kale kayası
    for k, (x0, x1, ty) in enumerate(((140, 560, 430), (380, 760, 470))):
        d_, sirt = S.dag(s, x0, x1, 600 + k * 20, (x0 + x1) / 2, ty, 920 + k, renk="#B4553C", golge="#7E3326", bicim="tepe", sis="#E9A88E", isik=-1, sirt=3, puruz=8)
        s += d_
        if k == 1:
            oc, _ = basamakli_ocak(s, sirt, ty + 20, 600, 5, 925)
            s += oc
    kale, _ = kale_sirti(s, 120, 330, 540, 430, 926, kaya="#7E5648", golge="#4E3432", tas="#D8AE8A", tas_g="#8A644E")
    s += kale
    # Fırat: Karasu (kuzeyden) ve Murat (doğudan) kolları, Keban Baraj Gölü, baraj, mansap
    karasu = [(820, 340), (860, 470), (900, 590), (950, 690)]
    murat = [(2100, 560), (1700, 620), (1400, 650), (1150, 680), (980, 700)]
    for yol, k in ((karasu, 26), (murat, 30)):
        s += f'<path d="{egri_d(yol)}" stroke="#2E9CB4" stroke-width="{k}" fill="none" stroke-linecap="round"/>'
        s += f'<path d="{egri_d(yol)}" stroke="#BDEFF4" stroke-width="5" fill="none" stroke-dasharray="20 16"/>'
    s += f'<path d="M880 660 Q960 640 1060 670 Q1080 720 980 740 Q880 760 840 720 Q830 680 880 660 Z" fill="#3FB2B8" stroke="#1E7E8E" stroke-width="3"/>'
    s += f'<path d="M820 760 L760 800 L700 840" stroke="#2E9CB4" stroke-width="20" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M790 752 L836 792" stroke="#BFC5CA" stroke-width="16" stroke-linecap="round"/><path d="M790 752 L836 792" stroke="#5E666E" stroke-width="3"/>'
    s += f'<path d="M700 840 Q560 900 380 1000 Q300 1050 260 {h}" stroke="#2E9CB4" stroke-width="18" fill="none"/>'
    # Hazar Gölü (derin mavi) ve Dicle'nin başı
    s += f'<ellipse cx="1330" cy="930" rx="150" ry="44" fill="#1E64B0" stroke="#0E3E78" stroke-width="3"/>'
    s += f'<ellipse cx="1300" cy="922" rx="90" ry="16" fill="#5FA6E0" opacity=".7"/>'
    s += f'<path d="M1480 950 Q1560 990 1620 1030 Q1660 1060 1700 {h}" stroke="#2E9CB4" stroke-width="14" fill="none"/>'
    # Maden: bakır yeşili damarlar; Guleman: koyu krom tepeleri
    for k in range(7):
        s += f'<path d="M{1580 + k * 18} {950 + (k % 3) * 10} q20 -6 40 4" stroke="{["#3FA88A", "#C8743A"][k % 2]}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    d_, _ = S.dag(s, 1780, 2140, 880, 1990, 740, 930, renk="#4E5C4C", golge="#2E3830", bicim="tepe", sis="#8EA294", isik=-1, sirt=4, puruz=10)
    s += d_
    s += cevher_yigini(s, 2000, 900, 90, 30, 931, renk="#1E2224", parilti="#6FD08A", n=5)
    # Elazığ (şehir işareti) ve kavak kümeleri
    for i in range(7):
        s += S.ev(1140 + i * 26 + (i % 2) * 4, 770 + (i % 3) * 8, 20, 16, 940 + i, duvar="#F2E6D0", cati="#B8553A", duz=True)
    for _ in range(36):
        x, y = r.uniform(60, 2050), r.uniform(ufuk + 50, h - 30)
        if any(math.hypot(x - a, y - b) < 120 for a, b in HARITA.values()) or 1150 < x < 1500 and 860 < y < 990:
            continue
        sc = .45 + (y - ufuk) / (h - ufuk)
        for j in range(3):
            s += S.kavak(s, x + j * 18 * sc, y, 58 * sc, 11 * sc, 960 + _ * 3 + j, renk="#5E9A4A")
    # rota
    sira = list(HARITA)
    yol = []
    for i, k in enumerate(sira):
        yol.append(HARITA[k])
        if i + 1 < len(sira):
            yol += ROTA_ARA.get((k, sira[i + 1]), [])
    yd = egri_d(yol, False, .9)
    s += f'<path d="{yd}" fill="none" stroke="#1B1D26" stroke-width="17" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
    s += f'<path d="{yd}" fill="none" stroke="#FFF1CF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="3.2" stroke-dasharray="12 9" stroke-linecap="round"/>'
    for k, (x, y) in HARITA.items():
        if k == "K":
            s += f'<circle cx="{x}" cy="{y}" r="34" fill="#E2533D" stroke="#1B1D26" stroke-width="3"/>'
            s += f'<path d="M{x - 18} {y + 14} V{y - 6} h6 v-6 h6 v6 h4 v-6 h6 v6 h4 v-6 h6 v6 h4 V{y + 14} Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>'
        else:
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 36), True)}" fill="#F0C14A" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 29), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2" stroke-linejoin="round"/>'
            s += f'<text x="{x}" y="{y + 11}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="32" fill="#FFFFFF">{k}</text>'
    x, y = HARITA["1"]
    s += f'<path d="M{x + 36} {y + 40} v-64" stroke="#1B1D26" stroke-width="4"/><path d="M{x + 38} {y - 22} h44 l-10 13 l10 13 h-44 Z" fill="#E2533D" stroke="#1B1D26" stroke-width="2.4"/>'
    for (tx, ty, ad, hale) in ((1330, 1010, "Hazar Gölü", "#0A3A66"), (1235, 748, "Elazığ", "#5A3A1A"), (180, 640, "Divriği", "#5A2A1A"),
                               (1880, 640, "Murat", "#0A5A66"), (760, 380, "Karasu", "#0A5A66")):
        s += halolu_yazi(f'x="{tx}" y="{ty}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="34"', ad, "#FFFFFF", hale, 1.4)
    s += f'<text x="360" y="1080" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" letter-spacing="1.5" fill="#FFFFFF" opacity=".95">FIRAT</text>'
    for k, (x, y, o) in enumerate(((1000, 200, 1.1), (1066, 232, .8), (1500, 150, .7), (820, 290, .6))):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    px, py = 2000, 400
    s += f'<circle cx="{px}" cy="{py}" r="64" fill="#FFFFFF" opacity=".9" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 58, 12, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 30), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="9" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 70}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="28" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), dict(HARITA)
