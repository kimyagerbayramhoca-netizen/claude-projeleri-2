"""Kimyasal Değişimler · Kars–Erzurum Yolu · üniteye özel çizim parçaları (karlı Doğu Anadolu kışı).

Ortak kütüphanede (yerel-ortak/cizim) olmayan parçalar burada; hepsi ortak `Svg`, `sahne`, `yapilar`
parçalarıyla aynı kurallara uyar: SVG metni döndürür, gradyanları verilen Svg'nin defs'ine yazar,
tohum sabit → her kurulumda aynı resim, ışık yönü `isik` (−1: güneş solda), konturlu yazı yok.

Parçalar: cam (karlı sarıçam), ciplak_agac, kar_zemin, kar_yagisi, buz_gol, at_kizak, buz_deligi,
ev_tas, mandira, peynir, guguk, inek, kaz, ani_sur, kirec_ocagi, harc_teknesi, soba, caydanlik,
co_dedektoru, menfez, tren, buhar, kaplica_havuz, tashan, tespih, pasli_kapi, telesiyej, tas_kopru,
istasyon, bazalt_kale.
"""
import math
from cizim.temel import f, nok, cizgi_d, egri_d, karis, acik, koyu, orta_nokta, rng as RNG
from cizim.renkler import OBS

KAR = "#FFFFFF"
KAR_G = "#C9D9EE"      # karın mavi gölgesi


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ------------------------------------------------------------------ ağaçlar

def cam(s, x, y, h, tohum, renk="#2F6B4C", golge=None, kar=True, isik=-1, kat=None, en=.46):
    """Karlı iğne yapraklı ağaç (Sarıkamış sarıçamı / ladin). (x, y) gövde tabanı."""
    r = RNG(tohum)
    golge = golge or koyu(renk, .38)
    n = kat or max(4, int(h / 26))
    w0 = h * en
    a, b = (acik(renk, .16), golge) if isik < 0 else (golge, acik(renk, .16))
    g = s.lin([(0, a), (.5, renk), (1, b)], 0, 0, 1, 0, ad="cm")
    o = [f'<rect x="{f(x - h * .03)}" y="{f(y - h * .14)}" width="{f(h * .06)}" height="{f(h * .14)}" fill="#5A3E2B"/>']
    top = y - h
    for i in range(n):
        t0 = i / n
        t1 = (i + 1.35) / n
        ty = top + (y - h * .1 - top) * t0 * .92
        by = top + (y - h * .1 - top) * min(1, t1)
        w = w0 * (.28 + .72 * min(1, t1)) * r.uniform(.9, 1.06)
        ap = (x + r.uniform(-1, 1) * h * .006, ty)
        bl, br = (x - w / 2, by), (x + w / 2, by)
        alt = [br]
        k = 5
        for j in range(1, k):
            px = x + w / 2 - w * j / k
            alt.append((px, by - (h * .035 if j % 2 else -h * .006) * r.uniform(.6, 1.2)))
        alt.append(bl)
        poly = [ap] + alt
        o.append(f'<path d="{cizgi_d(poly, True)}" fill="{g}"/>')
        if kar:
            sol_k = _lerp(ap, bl, r.uniform(.42, .62))
            sag_k = _lerp(ap, br, r.uniform(.22, .4))
            m1 = (x - w * .1, sol_k[1] + h * .02)
            m2 = (x + w * .08, sag_k[1] - h * .004)
            o.append(f'<path d="M{nok(ap)} L{nok(sol_k)} Q{nok(m1)} {f(x)} {f((sol_k[1] + sag_k[1]) / 2)} Q{nok(m2)} {nok(sag_k)} Z" fill="{KAR}" opacity=".96"/>')
            o.append(f'<path d="M{nok(sag_k)} Q{f(x + w * .06)} {f(sag_k[1] + h * .012)} {f(x)} {f((sol_k[1] + sag_k[1]) / 2 + h * .006)}" fill="none" stroke="{KAR_G}" stroke-width="{f(max(.8, h * .01))}" opacity=".9"/>')
            for px in (bl, br):
                o.append(f'<ellipse cx="{f(px[0] + (w * .05 if px is bl else -w * .05))}" cy="{f(px[1] - h * .008)}" rx="{f(w * .09)}" ry="{f(h * .014)}" fill="{KAR}"/>')
    return "".join(o)


def ciplak_agac(x, y, h, tohum, renk="#5B4636", kar=True, yayilim=.55):
    """Yapraksız kış ağacı (kavak/söğüt): gövde + çatallanan dallar, dalların üstünde ince kar."""
    r = RNG(tohum)
    o = []
    kar_o = []

    def dal(x0, y0, uz, aci, kal, d):
        x1 = x0 + uz * math.cos(aci)
        y1 = y0 - uz * math.sin(aci)
        mx = (x0 + x1) / 2 + r.uniform(-1, 1) * uz * .08
        my = (y0 + y1) / 2 + r.uniform(-1, 1) * uz * .06
        o.append(f'<path d="M{f(x0)} {f(y0)} Q{f(mx)} {f(my)} {f(x1)} {f(y1)}" stroke="{renk}" stroke-width="{f(kal)}" fill="none" stroke-linecap="round"/>')
        if kar and kal > 1.6 and math.sin(aci) < .93:
            kar_o.append(f'<path d="M{f(x0)} {f(y0 - kal * .45)} Q{f(mx)} {f(my - kal * .5)} {f(x1)} {f(y1 - kal * .4)}" stroke="#FFFFFF" stroke-width="{f(kal * .45)}" fill="none" stroke-linecap="round" opacity=".9"/>')
        if d > 0:
            for k in range(2 if d < 3 else 3):
                yeni = aci + r.uniform(-yayilim, yayilim)
                dal(x1, y1, uz * r.uniform(.55, .78), yeni, kal * .62, d - 1)

    dal(x, y, h * .38, math.pi / 2 + r.uniform(-.05, .05), max(2, h * .045), 4)
    return "".join(o) + "".join(kar_o)


# ------------------------------------------------------------------ kar

def kar_zemin(s, x0, x1, y, tohum, ust="#FFFFFF", alt="#D6E3F3", dalga=10, n=6, alt_y=None, golge="#B9CDE6"):
    """Karlı zemin bandı: yumuşak dalgalı üst kenar, mavi gölgeli tümsekler, parıltı."""
    r = RNG(tohum)
    alt_y = alt_y or y + 400
    pts = [(x0 + (x1 - x0) * i / n, y + r.uniform(-dalga, dalga)) for i in range(n + 1)]
    g = s.lin([(0, ust), (1, alt)], 0, y - dalga, 0, alt_y, kull="userSpaceOnUse", ad="kz")
    o = [f'<path d="{egri_d(pts)} L{f(x1)} {f(alt_y)} L{f(x0)} {f(alt_y)} Z" fill="{g}"/>']
    for _ in range(int((x1 - x0) / 160) + 2):
        cx = r.uniform(x0, x1)
        cy = y + r.uniform(12, 60)
        rx = r.uniform(50, 140)
        o.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(rx * .12)}" fill="{golge}" opacity=".35"/>')
    for _ in range(int((x1 - x0) / 60)):
        o.append(f'<circle cx="{f(r.uniform(x0, x1))}" cy="{f(y + r.uniform(8, 90))}" r="{f(r.uniform(.8, 1.8))}" fill="#FFFFFF" opacity=".95"/>')
    return "".join(o)


def kar_yagisi(x0, y0, w, h, n, tohum, op=.85, rmax=3.6):
    r = RNG(tohum)
    return "".join(f'<circle cx="{f(x0 + r.random() * w)}" cy="{f(y0 + r.random() * h)}" r="{f(r.uniform(1, rmax))}" fill="#FFFFFF" opacity="{f(op * r.uniform(.45, 1), 2)}"/>'
                   for _ in range(n))


def buz_gol(s, x, y, w, h, tohum, ufuk="#F6E3EC", orta="#CFE6F2", derin="#8DBBD8", parilti_x=None):
    """Donmuş göl: buz gradyanı, rüzgârın süpürdüğü kar şeritleri, çatlaklar, parıltılar."""
    r = RNG(tohum)
    g = s.lin([(0, ufuk), (.3, orta), (1, derin)], 0, y, 0, y + h, kull="userSpaceOnUse", ad="bz")
    o = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{g}"/>']
    for _ in range(int(w / 70)):
        t = r.random() ** 1.3
        py = y + 6 + t * (h - 10)
        uz = (60 + 260 * t) * r.uniform(.5, 1.3)
        px = x + r.random() * w
        kal = 2 + 9 * t
        o.append(f'<path d="M{f(px)} {f(py)} q{f(uz * .3)} {f(-kal * .6)} {f(uz * .6)} 0 t{f(uz * .4)} {f(kal * .3)}" stroke="#FFFFFF" stroke-width="{f(kal)}" stroke-linecap="round" fill="none" opacity="{f(r.uniform(.45, .85), 2)}"/>')
    for _ in range(int(w / 260)):
        t = r.uniform(.25, 1)
        px, py = x + r.random() * w, y + t * (h - 4)
        pts = [(px, py)]
        for k in range(r.randint(3, 6)):
            px += r.uniform(14, 40) * (1 + t)
            py += r.uniform(-5, 5) * (1 + t)
            pts.append((px, py))
        o.append(f'<path d="{cizgi_d(pts)}" stroke="#5E8DB3" stroke-width="{f(.8 + 1.2 * t)}" fill="none" opacity=".55"/>')
        a = pts[len(pts) // 2]
        o.append(f'<path d="M{nok(a)} l{f(r.uniform(-10, 10) * (1 + t))} {f(r.uniform(6, 14) * (1 + t))}" stroke="#5E8DB3" stroke-width="{f(.7 + t)}" opacity=".45"/>')
    if parilti_x is not None:
        for i in range(int(h / 6)):
            t = i / (h / 6)
            py = y + 3 + i * 6
            gen = (10 + 80 * t) * r.uniform(.3, 1)
            px = parilti_x + r.uniform(-1, 1) * (6 + 30 * t) - gen / 2
            o.append(f'<path d="M{f(px)} {f(py)} h{f(gen)}" stroke="#FFF4D2" stroke-width="{f(1.4 + 2 * t)}" stroke-linecap="round" opacity="{f(r.uniform(.4, .85) * (1 - .5 * t), 2)}"/>')
    for _ in range(int(w / 40)):
        px, py = x + r.random() * w, y + r.random() * h
        rr = r.uniform(1.5, 3.4)
        o.append(f'<path d="M{f(px)} {f(py - rr * 2)} L{f(px + rr * .4)} {f(py)} L{f(px)} {f(py + rr * 2)} L{f(px - rr * .4)} {f(py)} Z M{f(px - rr * 2)} {f(py)} L{f(px)} {f(py + rr * .4)} L{f(px + rr * 2)} {f(py)} L{f(px)} {f(py - rr * .4)} Z" fill="#FFFFFF" opacity="{f(r.uniform(.5, .95), 2)}"/>')
    return "".join(o)


# ------------------------------------------------------------------ Çıldır: atlı kızak, buz deliği

def at_kizak(s, x, y, o=1.0, at="#7A4A2A", yele="#3A2416", kizak="#C8442F", yon=1, yolcu=True):
    """Buzda tırısa kalkmış at + arkasında kırmızı kızak. (x, y): atın ön toynakları zemini. yon=1 sağa gider."""
    gat = s.lin([(0, acik(at, .25)), (.6, at), (1, koyu(at, .3))], 0, 0, 0, 1, ad="at")
    cz = koyu(at, .55)
    p = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o * yon, 3)} {f(o, 3)})">']
    # gölge
    p.append('<ellipse cx="-80" cy="2" rx="150" ry="9" fill="#2A4A6A" opacity=".18"/>')
    # kızak (atın arkasında)
    kg = s.lin([(0, acik(kizak, .2)), (1, koyu(kizak, .25))], 0, 0, 0, 1, ad="kz")
    p.append(f'<path d="M-250 -6 H-118 Q-96 -6 -92 -22" fill="none" stroke="#3A2A20" stroke-width="5" stroke-linecap="round"/>'
             f'<path d="M-244 -14 V-6 M-200 -14 V-6 M-150 -14 V-6" stroke="#3A2A20" stroke-width="4"/>'
             f'<path d="M-252 -60 L-246 -14 H-130 L-118 -52 Q-150 -46 -176 -58 Q-210 -72 -252 -60 Z" fill="{kg}" stroke="#4A1A12" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M-246 -28 H-126" stroke="#F0C14A" stroke-width="4"/><path d="M-240 -40 q20 -6 40 0 t40 0 t40 0" stroke="#F0C14A" stroke-width="2.4" fill="none"/>'
             f'<path d="M-252 -60 Q-262 -78 -248 -88" fill="none" stroke="#4A1A12" stroke-width="4" stroke-linecap="round"/>')
    if yolcu:
        p.append('<use href="#pamuk-selam" x="-236" y="-150" width="92" height="105"/>')
    # koşum
    p.append(f'<path d="M-118 -48 L-34 -66 M-120 -36 L-30 -54" stroke="#3A2A20" stroke-width="3"/>')
    # at: bacaklar (arkadakiler koyu)
    for (x0, y0, x1, y1), ton in (((-30, -46, -46, -2), .25), ((30, -48, 50, -4), .25)):
        p.append(f'<path d="M{x0} {y0} Q{(x0 + x1) / 2 - 4} {(y0 + y1) / 2} {x1} {y1}" stroke="{koyu(at, ton)}" stroke-width="10" stroke-linecap="round" fill="none"/>'
                 f'<path d="M{x1 - 6} {y1 + 2} h12" stroke="#1E1410" stroke-width="6" stroke-linecap="round"/>')
    p.append(f'<path d="M-62 -70 C-82 -66 -88 -44 -78 -26" fill="none" stroke="{yele}" stroke-width="9" stroke-linecap="round"/>')
    p.append(f'<ellipse cx="-6" cy="-66" rx="62" ry="26" fill="{gat}" stroke="{cz}" stroke-width="2.4"/>')
    p.append(f'<path d="M36 -82 C46 -104 58 -122 70 -130 L84 -126 C96 -112 104 -104 110 -96 C112 -90 106 -86 100 -88 C92 -92 82 -98 76 -100 C70 -90 64 -74 58 -60 Z" fill="{gat}" stroke="{cz}" stroke-width="2.4" stroke-linejoin="round"/>')
    p.append(f'<path d="M72 -128 L74 -142 L82 -128 Z" fill="{at}" stroke="{cz}" stroke-width="2"/>')
    p.append(f'<path d="M40 -86 C50 -110 62 -126 72 -132 C66 -118 58 -102 50 -84 Z" fill="{yele}"/>')
    p.append(f'<circle cx="88" cy="-112" r="2.6" fill="#1E1410"/><path d="M104 -92 q3 2 0 4" stroke="#1E1410" stroke-width="2" fill="none"/>')
    p.append(f'<path d="M66 -122 L96 -96 M60 -100 L90 -92" stroke="#C8442F" stroke-width="3"/>')
    for (x0, y0, x1, y1) in ((-42, -50, -62, -4), (44, -50, 66, -16)):
        p.append(f'<path d="M{x0} {y0} Q{(x0 + x1) / 2 + 6} {(y0 + y1) / 2} {x1} {y1}" stroke="{at}" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 f'<path d="M{x1 - 6} {y1 + 2} h12" stroke="#1E1410" stroke-width="6" stroke-linecap="round"/>')
    p.append(f'<path d="M-20 -88 Q0 -94 30 -86" stroke="#FFFFFF" stroke-width="4" fill="none" opacity=".35"/>')
    # koşum çanı ve süs
    p.append(f'<circle cx="52" cy="-70" r="5" fill="#F0C14A" stroke="#7A5A10" stroke-width="1.6"/>')
    p.append("</g>")
    return "".join(p)


def buz_deligi(x, y, o=1.0, balik=True):
    """Buz altı balıkçılığı: buzda açılmış delik, ağ, kova; yanında tutulmuş balıklar."""
    k = o
    p = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(34 * k)}" ry="{f(10 * k)}" fill="#E8F2FA" stroke="#9FBCD6" stroke-width="{f(2 * k)}"/>',
         f'<ellipse cx="{f(x)}" cy="{f(y + 1 * k)}" rx="{f(26 * k)}" ry="{f(7 * k)}" fill="#1E4E72"/>',
         f'<path d="M{f(x - 18 * k)} {f(y - 2 * k)} q{f(18 * k)} {f(6 * k)} {f(36 * k)} 0" stroke="#7FB2D6" stroke-width="{f(1.6 * k)}" fill="none"/>',
         f'<path d="M{f(x + 8 * k)} {f(y)} L{f(x + 40 * k)} {f(y - 60 * k)}" stroke="#5A3E2B" stroke-width="{f(3 * k)}" stroke-linecap="round"/>',
         f'<path d="M{f(x + 40 * k)} {f(y - 60 * k)} L{f(x + 12 * k)} {f(y - 4 * k)}" stroke="#2A2A2A" stroke-width="{f(1 * k)}"/>',
         f'<path d="M{f(x + 46 * k)} {f(y + 2 * k)} h{f(26 * k)} l{f(-4 * k)} {f(-22 * k)} h{f(-18 * k)} Z" fill="#2B50B5" stroke="#1B3584" stroke-width="{f(1.6 * k)}"/>']
    if balik:
        for i, (dx, a) in enumerate(((-58, -8), (-44, 12))):
            bx, by = x + dx * k, y + 4 * k
            p.append(f'<g transform="translate({f(bx)} {f(by)}) rotate({a}) scale({f(k * .55, 3)})"><path d="M-20 0 C-12 -8 10 -8 20 0 C10 8 -12 8 -20 0 Z M-20 0 L-30 -7 L-30 7 Z" fill="#9FB4C2" stroke="#3A5464" stroke-width="2"/><circle cx="12" cy="-1" r="2" fill="#1B1D26"/></g>')
    return "".join(p)


# ------------------------------------------------------------------ Kars: taş ev, mandıra, peynir, güğüm, inek, kaz

def ev_tas(s, x, y, w, h, tohum, duvar="#8E959E", cati="#8A98A6", kar=True, isik_pencere=False, isik=-1, baca=True):
    """Kars'ın kesme taş evi: kare gövde, beşik çatı (sac/kiremit), karlı çatı, pencereler."""
    r = RNG(tohum)
    o = []
    gd = s.lin([(0, acik(duvar, .12)), (1, koyu(duvar, .12))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="ed")
    o.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{gd}"/>')
    for k in range(1, int(h / 14)):
        yy = y - k * 14
        o.append(f'<path d="M{f(x)} {f(yy)} H{f(x + w)}" stroke="{koyu(duvar, .25)}" stroke-width="1" opacity=".35"/>')
    o.append(f'<rect x="{f(x + (w * .6 if isik < 0 else 0))}" y="{f(y - h)}" width="{f(w * .4)}" height="{f(h)}" fill="#0E1A2A" opacity=".14"/>')
    ch = h * .5
    o.append(f'<path d="M{f(x - w * .07)} {f(y - h)} L{f(x + w / 2)} {f(y - h - ch)} L{f(x + w * 1.07)} {f(y - h)} Z" fill="{cati}"/>')
    o.append(f'<path d="M{f(x + w / 2)} {f(y - h - ch)} L{f(x + w * 1.07)} {f(y - h)} L{f(x + w * .62)} {f(y - h)} Z" fill="#000" opacity=".16"/>')
    if baca:
        bx = x + w * .72
        o.append(f'<rect x="{f(bx)}" y="{f(y - h - ch * .85)}" width="{f(w * .09)}" height="{f(ch * .5)}" fill="{koyu(duvar, .2)}"/>')
    if kar:
        o.append(f'<path d="M{f(x - w * .09)} {f(y - h + 2)} L{f(x + w / 2)} {f(y - h - ch - 3)} L{f(x + w * 1.09)} {f(y - h + 2)} '
                 f'Q{f(x + w * .82)} {f(y - h - ch * .28)} {f(x + w * .62)} {f(y - h - ch * .2)} Q{f(x + w * .4)} {f(y - h - ch * .5)} {f(x + w * .2)} {f(y - h - ch * .14)} Q{f(x + w * .05)} {f(y - h - ch * .02)} {f(x - w * .09)} {f(y - h + 2)} Z" fill="#FFFFFF"/>')
    pc = "#FFD27A" if isik_pencere else "#3A4A5E"
    for i in range(2 if w > 40 else 1):
        px = x + w * (.18 + .44 * i)
        o.append(f'<rect x="{f(px)}" y="{f(y - h * .74)}" width="{f(w * .2)}" height="{f(h * .32)}" fill="{pc}" stroke="{koyu(duvar, .4)}" stroke-width="1.4"/>')
        o.append(f'<path d="M{f(px + w * .1)} {f(y - h * .74)} v{f(h * .32)}" stroke="{koyu(duvar, .4)}" stroke-width="1"/>')
    return "".join(o)


def mandira(s, x, y, w, h, tohum, tas="#9A8F86", isik=-1):
    """Taş mandıra (peynirhane): geniş gövde, ahşap kapı, olgunlaştırma odasının açık penceresinde kaşar rafları, bacadan duman."""
    r = RNG(tohum)
    o = []
    gd = s.lin([(0, acik(tas, .18)), (1, koyu(tas, .1))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="md")
    o.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{gd}"/>')
    for row in range(int(h / 18)):
        yy = y - row * 18
        off = (row % 2) * 16
        for xx in range(int(x - off), int(x + w), 32):
            x0, x1 = max(x, xx), min(x + w, xx + 30)
            if x1 - x0 > 4:
                o.append(f'<rect x="{f(x0)}" y="{f(yy - 17)}" width="{f(x1 - x0)}" height="16" rx="2" fill="{karis(tas, "#FFFFFF", r.uniform(0, .25))}" opacity=".55"/>')
    o.append(f'<rect x="{f(x + (w * .66 if isik < 0 else 0))}" y="{f(y - h)}" width="{f(w * .34)}" height="{f(h)}" fill="#0E1A2A" opacity=".13"/>')
    ch = h * .42
    o.append(f'<path d="M{f(x - w * .05)} {f(y - h)} L{f(x + w * .5)} {f(y - h - ch)} L{f(x + w * 1.05)} {f(y - h)} Z" fill="#6E3A2E"/>')
    o.append(f'<path d="M{f(x - w * .07)} {f(y - h + 2)} L{f(x + w * .5)} {f(y - h - ch - 3)} L{f(x + w * 1.07)} {f(y - h + 2)} Q{f(x + w * .75)} {f(y - h - ch * .3)} {f(x + w * .5)} {f(y - h - ch * .26)} Q{f(x + w * .25)} {f(y - h - ch * .32)} {f(x - w * .07)} {f(y - h + 2)} Z" fill="#FFFFFF"/>')
    # baca + duman
    bx = x + w * .78
    o.append(f'<rect x="{f(bx)}" y="{f(y - h - ch * .9)}" width="{f(w * .06)}" height="{f(ch * .5)}" fill="#5E5650"/><rect x="{f(bx - 3)}" y="{f(y - h - ch * .92)}" width="{f(w * .06 + 6)}" height="6" fill="#FFFFFF"/>')
    for k in range(4):
        o.append(f'<circle cx="{f(bx + w * .03 + k * 14 + r.uniform(-4, 4))}" cy="{f(y - h - ch * .98 - k * 22)}" r="{f(9 + k * 5)}" fill="#F2F4F7" opacity="{f(.75 - k * .14, 2)}"/>')
    # kapı (ahşap, çift kanat)
    dw, dh = w * .22, h * .62
    dx = x + w * .12
    o.append(f'<path d="M{f(dx)} {f(y)} V{f(y - dh + dw * .3)} Q{f(dx)} {f(y - dh)} {f(dx + dw / 2)} {f(y - dh)} Q{f(dx + dw)} {f(y - dh)} {f(dx + dw)} {f(y - dh + dw * .3)} V{f(y)} Z" fill="#7A4E2E" stroke="#4A2E18" stroke-width="2"/>')
    o.append(f'<path d="M{f(dx + dw / 2)} {f(y - dh)} V{f(y)}" stroke="#4A2E18" stroke-width="2"/>')
    for k in range(3):
        o.append(f'<path d="M{f(dx + 4)} {f(y - dh * (.2 + k * .25))} H{f(dx + dw - 4)}" stroke="#4A2E18" stroke-width="1.6" opacity=".7"/>')
    # olgunlaştırma odası penceresi: kaşar rafları
    wx, wy, ww, wh = x + w * .44, y - h * .82, w * .46, h * .5
    o.append(f'<rect x="{f(wx)}" y="{f(wy)}" width="{f(ww)}" height="{f(wh)}" fill="#3A2C22" stroke="#4A2E18" stroke-width="3"/>')
    isik_g = s.rad([(0, "#FFE7A8", .9), (1, "#FFE7A8", 0)], wx + ww / 2, wy + wh / 2, ww * .7, kull="userSpaceOnUse", ad="mi")
    o.append(f'<rect x="{f(wx)}" y="{f(wy)}" width="{f(ww)}" height="{f(wh)}" fill="{isik_g}"/>')
    for row in range(3):
        ry = wy + wh * (.34 + row * .3)
        o.append(f'<path d="M{f(wx + 3)} {f(ry)} H{f(wx + ww - 3)}" stroke="#8C5A2E" stroke-width="3"/>')
        for k in range(int(ww / 26)):
            o.append(peynir(s, wx + 14 + k * 26, ry - 1, 10.5, cizgi=False))
    o.append(f'<path d="M{f(wx + ww / 2)} {f(wy)} V{f(wy + wh)}" stroke="#4A2E18" stroke-width="2.4" opacity=".8"/>')
    return "".join(o)


def peynir(s, x, y, r, renk="#F2D37A", kabuk="#D9A23A", cizgi=True, dilim=False):
    """Kaşar tekeri (silindir): (x, y) alt orta."""
    hh = r * .62
    cz = f' stroke="#8C5A1A" stroke-width="{f(max(.6, r * .06))}"' if cizgi else ""
    o = [f'<path d="M{f(x - r)} {f(y - hh)} V{f(y)} A{f(r)} {f(r * .32)} 0 0 0 {f(x + r)} {f(y)} V{f(y - hh)} Z" fill="{kabuk}"{cz}/>',
         f'<ellipse cx="{f(x)}" cy="{f(y - hh)}" rx="{f(r)}" ry="{f(r * .32)}" fill="{renk}"{cz}/>']
    if dilim:
        o.append(f'<path d="M{f(x)} {f(y - hh)} L{f(x + r)} {f(y - hh)} V{f(y)} L{f(x)} {f(y)} Z" fill="#FFF0B8"{cz}/>')
    return "".join(o)


def guguk(s, x, y, h, maden="#B8C4CE"):
    """Süt güğümü (metal kap)."""
    g = s.lin([(0, acik(maden, .55)), (.4, maden), (1, koyu(maden, .35))], 0, 0, 1, 0, ad="gg")
    w = h * .5
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .62)}" ry="{f(h * .05)}" fill="#1B1D26" opacity=".2"/>'
            f'<path d="M{f(x - w / 2)} {f(y)} V{f(y - h * .55)} Q{f(x - w / 2)} {f(y - h * .7)} {f(x - w * .25)} {f(y - h * .78)} V{f(y - h * .9)} H{f(x + w * .25)} V{f(y - h * .78)} Q{f(x + w / 2)} {f(y - h * .7)} {f(x + w / 2)} {f(y - h * .55)} V{f(y)} Z" fill="{g}" stroke="#4A5866" stroke-width="{f(h * .02)}"/>'
            f'<rect x="{f(x - w * .3)}" y="{f(y - h)}" width="{f(w * .6)}" height="{f(h * .1)}" rx="{f(h * .03)}" fill="{g}" stroke="#4A5866" stroke-width="{f(h * .02)}"/>'
            f'<path d="M{f(x - w / 2)} {f(y - h * .42)} H{f(x + w / 2)} M{f(x - w / 2)} {f(y - h * .12)} H{f(x + w / 2)}" stroke="#4A5866" stroke-width="{f(h * .015)}" opacity=".7"/>'
            f'<path d="M{f(x - w * .28)} {f(y - h * .7)} q{f(-w * .3)} {f(h * .05)} {f(-w * .2)} {f(h * .18)}" stroke="#4A5866" stroke-width="{f(h * .025)}" fill="none"/>')


def inek(x, y, o=1.0, yon=1, renk="#9C3B22", ak="#F4EEE6"):
    """Doğu Anadolu Kırmızısı esinli inek (temsilî)."""
    k = o
    p = [f'<g transform="translate({f(x)} {f(y)}) scale({f(k * yon, 3)} {f(k, 3)})">',
         '<ellipse cx="0" cy="2" rx="46" ry="5" fill="#2A4A6A" opacity=".18"/>']
    for lx in (-30, -18, 20, 32):
        p.append(f'<path d="M{lx} -24 V-2" stroke="{koyu(renk, .25)}" stroke-width="7" stroke-linecap="round"/><path d="M{lx - 3} 0 h6" stroke="#2A1A12" stroke-width="5" stroke-linecap="round"/>')
    p.append(f'<path d="M-40 -46 Q-42 -60 -26 -62 H24 Q40 -62 42 -48 L40 -24 Q0 -18 -38 -24 Z" fill="{renk}" stroke="{koyu(renk, .5)}" stroke-width="2"/>')
    p.append(f'<path d="M-8 -60 q6 10 -2 20 q10 4 18 -2 q-4 -10 2 -18 Z" fill="{ak}" opacity=".9"/>')
    p.append(f'<path d="M-40 -48 q-10 4 -12 18" stroke="{koyu(renk, .5)}" stroke-width="3" fill="none"/>')
    p.append(f'<path d="M40 -56 L58 -60 Q66 -56 66 -44 L62 -34 Q54 -30 48 -36 L40 -40 Z" fill="{renk}" stroke="{koyu(renk, .5)}" stroke-width="2"/>')
    p.append(f'<path d="M54 -58 q8 2 10 12 q-6 6 -10 -2 Z" fill="{ak}"/><circle cx="56" cy="-50" r="2" fill="#1B1D26"/>')
    p.append(f'<path d="M50 -60 q-2 -8 4 -10 M60 -60 q4 -6 10 -4" stroke="#E8DCC4" stroke-width="3" fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M-30 -62 q20 -6 50 -2" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>')
    p.append("</g>")
    return "".join(p)


def kaz(x, y, o=1.0, yon=1):
    """Kaz (beyaz-gri)."""
    k = o
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(k * yon, 3)} {f(k, 3)})">'
            f'<ellipse cx="0" cy="1" rx="16" ry="2.4" fill="#2A4A6A" opacity=".18"/>'
            f'<path d="M-4 -2 v-6 M4 -2 v-6" stroke="#F0A21A" stroke-width="2.4"/>'
            f'<path d="M-18 -12 Q-16 -24 0 -24 Q14 -24 14 -14 Q6 -6 -10 -7 Z" fill="#F4F6F8" stroke="#6A7684" stroke-width="1.6"/>'
            f'<path d="M-14 -16 q10 -6 22 -2" stroke="#B9C4CE" stroke-width="3" fill="none"/>'
            f'<path d="M10 -20 Q12 -34 18 -40 Q24 -42 24 -36 Q20 -32 18 -22 Z" fill="#F4F6F8" stroke="#6A7684" stroke-width="1.6"/>'
            f'<path d="M23 -38 l7 2 l-7 2 Z" fill="#F0A21A" stroke="#8C5500" stroke-width=".8"/><circle cx="20.5" cy="-38" r="1.2" fill="#1B1D26"/></g>')


# ------------------------------------------------------------------ Ani: sur, kireç ocağı, harç teknesi

def ani_sur(s, x0, x1, y, h, tohum, isik=-1, kirik=True, kum="#C69A6E", suslu=True, kapi=True, gedik_yer=(.56, .87)):
    """Ani'nin tüf taşı surları: iki renk taş örgü, yarım yuvarlak burçlar, geometrik taş kakma şeritleri, karlı üst kenar."""
    r = RNG(tohum)
    w = x1 - x0
    o = []
    kizil = "#A65A3E"
    kara = "#4E3A38"
    ust = []
    n = 72
    gedik = gedik_yer if kirik else ()          # yıkık gedikler: sur yer yer yarı boyuna kadar çökmüş (Ani bugün harabedir)
    for i in range(n + 1):
        t = i / n
        yy = y - h * (.78 + .08 * math.sin(t * 9 + 1))
        if kirik and r.random() < .3:
            yy += r.uniform(0, h * .12)
        for gc in gedik:
            d = abs(t - gc)
            if d < .055:
                hedef = y - h * (.34 + .08 * r.random())
                yy += (hedef - yy) * min(1, (1 - d / .055) * 1.7)
                yy += r.uniform(-h * .05, h * .05)
        ust.append((x0 + w * t, yy))
    duvar = [(x0, y)] + ust + [(x1, y)]
    g = s.lin([(0, acik(kum, .1)), (.7, kum), (1, koyu(kum, .2))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="as")
    o.append(f'<path d="{cizgi_d(duvar, True)}" fill="{g}"/>')
    kirp = s.kid("asc")                       # taş sıraları gediklerde gökyüzüne taşmasın
    s.tanim(f'<clipPath id="{kirp}"><path d="{cizgi_d(duvar, True)}"/></clipPath>')
    o.append(f'<g clip-path="url(#{kirp})">')
    # taş sıraları
    for k in range(1, int(h / 16)):
        yy = y - k * 16
        o.append(f'<path d="M{f(x0)} {f(yy)} H{f(x1)}" stroke="{koyu(kum, .35)}" stroke-width="1.1" opacity=".4"/>')
        off = (k % 2) * 13
        for xx in range(int(x0 + off), int(x1), 26):
            if r.random() < .25:
                o.append(f'<rect x="{xx}" y="{f(yy)}" width="25" height="15" fill="{r.choice([kizil, kara, acik(kum, .25)])}" opacity=".55"/>')
    o.append('</g>')
    # burçlar
    adet = max(3, int(w / 230))
    for i in range(adet):
        bx = x0 + w * (i + .5) / adet
        bw = h * .52
        bh = h * r.uniform(1.0, 1.15)
        gb = s.lin([(0, koyu(kum, .2)), (.35, acik(kum, .15)), (.7, kum), (1, koyu(kum, .3))], bx - bw / 2, 0, bx + bw / 2, 0, kull="userSpaceOnUse", ad="ab")
        top = y - bh
        yikik = kirik and i % 2 == 1
        if yikik:                                  # tepesi yıkılmış burç: kırık, basamaklı üst kenar
            top += h * .2
            kir = [(bx - bw / 2, top + 26), (bx - bw * .3, top + 4), (bx - bw * .12, top + 22), (bx + bw * .05, top - 6),
                   (bx + bw * .22, top + 16), (bx + bw / 2, top + 34)]
            o.append(f'<path d="M{f(bx - bw / 2)} {f(y)} L{" L".join(f"{f(a_)} {f(b_)}" for a_, b_ in kir)} V{f(y)} Z" fill="{gb}"/>')
        else:
            o.append(f'<path d="M{f(bx - bw / 2)} {f(y)} V{f(top + 8)} Q{f(bx)} {f(top - 4)} {f(bx + bw / 2)} {f(top + 8)} V{f(y)} Z" fill="{gb}"/>')
        # kakma şerit: dama (iki renk kare) — yalnız Ani'de (suslu)
        sy = top + bh * .3
        for j in (range(8) if suslu else ()):
            cx = bx - bw / 2 + bw * (j + .5) / 8
            for row in range(2):
                if (j + row) % 2 == 0:
                    o.append(f'<rect x="{f(cx - bw / 16)}" y="{f(sy + row * bw / 8)}" width="{f(bw / 8)}" height="{f(bw / 8)}" fill="{kara}" opacity=".85"/>')
                else:
                    o.append(f'<rect x="{f(cx - bw / 16)}" y="{f(sy + row * bw / 8)}" width="{f(bw / 8)}" height="{f(bw / 8)}" fill="{kizil}" opacity=".85"/>')
        if suslu:
            o.append(f'<path d="M{f(bx - bw / 2)} {f(sy - 3)} H{f(bx + bw / 2)} M{f(bx - bw / 2)} {f(sy + bw / 4 + 3)} H{f(bx + bw / 2)}" stroke="{kara}" stroke-width="2.4"/>')
        # dar mazgal pencere
        o.append(f'<rect x="{f(bx - bw * .05)}" y="{f(top + bh * .58)}" width="{f(bw * .1)}" height="{f(bh * .16)}" rx="{f(bw * .05)}" fill="{kara}"/>')
        # kar kapağı (yıkık burçta kırık kenarda ince kar)
        if yikik:
            o.append(f'<path d="M{" L".join(f"{f(a_)} {f(b_ - 5)}" for a_, b_ in kir)} L{" L".join(f"{f(a_)} {f(b_ + 3)}" for a_, b_ in reversed(kir))} Z" fill="#FFFFFF"/>')
            continue
        o.append(f'<path d="M{f(bx - bw / 2 - 3)} {f(top + 10)} Q{f(bx)} {f(top - 8)} {f(bx + bw / 2 + 3)} {f(top + 10)} Q{f(bx + bw * .2)} {f(top + 6)} {f(bx)} {f(top + 12)} Q{f(bx - bw * .25)} {f(top + 6)} {f(bx - bw / 2 - 3)} {f(top + 10)} Z" fill="#FFFFFF"/>')
    # surun üstündeki kar
    kar_ust = [(p[0], p[1] - 4) for p in ust]
    o.append(f'<path d="{cizgi_d(kar_ust + [(p[0], p[1] + 5) for p in reversed(ust)], True)}" fill="#FFFFFF"/>')
    # gediklerin dibinde moloz
    for gc in gedik:
        gx = x0 + w * gc
        for _ in range(11):
            mx, mr = gx + r.uniform(-w * .06, w * .06), r.uniform(7, 15)
            my = y - r.uniform(0, 14)
            ton = r.choice([kum, koyu(kum, .2), kizil, acik(kum, .15)])
            o.append(f'<path d="M{f(mx - mr)} {f(my)} L{f(mx - mr * .4)} {f(my - mr * .8)} L{f(mx + mr * .6)} {f(my - mr * .7)} L{f(mx + mr)} {f(my)} Z" fill="{ton}" stroke="{koyu(kum, .4)}" stroke-width="1"/>')
        o.append(f'<ellipse cx="{f(gx)}" cy="{f(y + 2)}" rx="{f(w * .07)}" ry="5" fill="#FFFFFF" opacity=".85"/>')
    if not kapi:
        return "".join(o)
    # kapı açıklığı
    kx = x0 + w * .3
    o.append(f'<path d="M{f(kx - h * .16)} {f(y)} V{f(y - h * .36)} Q{f(kx - h * .16)} {f(y - h * .52)} {f(kx)} {f(y - h * .56)} Q{f(kx + h * .16)} {f(y - h * .52)} {f(kx + h * .16)} {f(y - h * .36)} V{f(y)} Z" fill="#2E2222"/>')
    o.append(f'<path d="M{f(kx - h * .2)} {f(y)} V{f(y - h * .38)} Q{f(kx - h * .2)} {f(y - h * .58)} {f(kx)} {f(y - h * .62)} Q{f(kx + h * .2)} {f(y - h * .58)} {f(kx + h * .2)} {f(y - h * .38)} V{f(y)}" fill="none" stroke="{kara}" stroke-width="4"/>')
    return "".join(o)


def kirec_ocagi(s, x, y, h, tohum=1):
    """Taş kireç ocağı: kubbemsi gövde, ağzında ateş, üstten çıkan duman (kalker kavrulur: CaCO₃ → CaO + CO₂)."""
    r = RNG(tohum)
    w = h * 1.1
    g = s.lin([(0, "#D9C2A2"), (1, "#8E7458")], 0, 0, 1, 0, ad="ko")
    o = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .7)}" ry="{f(h * .06)}" fill="#2A3A5A" opacity=".2"/>',
         f'<path d="M{f(x - w / 2)} {f(y)} Q{f(x - w * .52)} {f(y - h * .8)} {f(x - w * .16)} {f(y - h)} H{f(x + w * .16)} Q{f(x + w * .52)} {f(y - h * .8)} {f(x + w / 2)} {f(y)} Z" fill="{g}" stroke="#6A5440" stroke-width="2.4"/>']
    for k in range(1, 5):
        yy = y - h * k * .2
        o.append(f'<path d="M{f(x - w * (.5 - k * .06))} {f(yy)} Q{f(x)} {f(yy + 6)} {f(x + w * (.5 - k * .06))} {f(yy)}" stroke="#6A5440" stroke-width="1.4" fill="none" opacity=".6"/>')
    ates = s.rad([(0, "#FFF4C8"), (.5, "#FFB43A"), (1, "#E2533D")], .5, .7, .7, ad="ka")
    o.append(f'<path d="M{f(x - w * .14)} {f(y)} V{f(y - h * .26)} Q{f(x)} {f(y - h * .4)} {f(x + w * .14)} {f(y - h * .26)} V{f(y)} Z" fill="#3A2016"/>')
    o.append(f'<path d="M{f(x - w * .1)} {f(y)} Q{f(x - w * .08)} {f(y - h * .16)} {f(x)} {f(y - h * .3)} Q{f(x + w * .08)} {f(y - h * .16)} {f(x + w * .1)} {f(y)} Z" fill="{ates}"/>')
    o.append(f'<path d="M{f(x - w * .2)} {f(y - h)} h{f(w * .4)}" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>')
    for k in range(5):
        o.append(f'<circle cx="{f(x + k * 10 + r.uniform(-6, 6))}" cy="{f(y - h * 1.08 - k * h * .22)}" r="{f(h * (.08 + k * .04))}" fill="#E9ECF2" opacity="{f(.8 - k * .13, 2)}"/>')
    return "".join(o)


def harc_teknesi(s, x, y, w):
    """Ahşap harç teknesi: içinde beyaz kireç harcı, üstünde mala (usta malası)."""
    h = w * .28
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .62)}" ry="{f(h * .2)}" fill="#2A3A5A" opacity=".2"/>'
            f'<path d="M{f(x - w / 2)} {f(y - h)} H{f(x + w / 2)} L{f(x + w * .42)} {f(y)} H{f(x - w * .42)} Z" fill="#9A6B42" stroke="#5A3A22" stroke-width="2.4"/>'
            f'<path d="M{f(x - w * .46)} {f(y - h)} Q{f(x - w * .2)} {f(y - h * 1.5)} {f(x)} {f(y - h * 1.2)} Q{f(x + w * .25)} {f(y - h * 1.45)} {f(x + w * .46)} {f(y - h)} Z" fill="#F4F2EC" stroke="#B9B4AA" stroke-width="1.6"/>'
            f'<path d="M{f(x - w * .3)} {f(y - h * .45)} H{f(x + w * .3)}" stroke="#5A3A22" stroke-width="1.6" opacity=".6"/>'
            f'<g transform="translate({f(x + w * .1)} {f(y - h * 1.35)}) rotate(-24)"><path d="M0 0 L{f(w * .34)} {f(-h * .18)} L{f(w * .36)} {f(h * .22)} Z" fill="#C9D3DC" stroke="#4A5866" stroke-width="2"/>'
            f'<path d="M{f(w * .02)} 0 L{f(-w * .12)} {f(-h * .2)}" stroke="#4A5866" stroke-width="3"/><rect x="{f(-w * .24)}" y="{f(-h * .34)}" width="{f(w * .14)}" height="{f(h * .2)}" rx="{f(h * .08)}" fill="#8C5A2E" transform="rotate(30 {f(-w * .17)} {f(-h * .24)})"/></g>')


# ------------------------------------------------------------------ Sarıkamış: soba, çaydanlık, CO dedektörü, menfez, tren

def soba(s, x, y, h, govde="#2E2F36", isik_g=True):
    """Döküm odun sobası: dört ayak, ateş camı, kapak kolu, üstte çaydanlık yeri, yukarı çıkıp duvara giren boru.
    (x, y): ayakların zemini ortası. Boru sobanın üstünden yükselip y - 2,1h hizasında sola döner."""
    w = h * .62
    o = []
    if isik_g:
        sicak = s.rad([(0, "#FFC56B", .55), (.4, "#FF9A45", .2), (1, "#FF9A45", 0)], x, y - h * .4, h * 1.6, kull="userSpaceOnUse", ad="sc")
        o.append(f'<circle cx="{f(x)}" cy="{f(y - h * .4)}" r="{f(h * 1.6)}" fill="{sicak}"/>')
    g = s.lin([(0, "#5A5C66"), (.35, govde), (1, "#121318")], 0, 0, 1, 0, ad="sb")
    o.append(f'<ellipse cx="{f(x)}" cy="{f(y + 2)}" rx="{f(w * .75)}" ry="{f(h * .05)}" fill="#1B1D26" opacity=".35"/>')
    for lx in (-.36, .36):
        o.append(f'<path d="M{f(x + lx * w)} {f(y - h * .14)} L{f(x + lx * w * 1.18)} {f(y)}" stroke="#1B1D26" stroke-width="{f(h * .05)}" stroke-linecap="round"/>')
    o.append(f'<rect x="{f(x - w / 2)}" y="{f(y - h * .9)}" width="{f(w)}" height="{f(h * .78)}" rx="{f(w * .08)}" fill="{g}" stroke="#0E0F14" stroke-width="{f(h * .012)}"/>')
    o.append(f'<rect x="{f(x - w * .56)}" y="{f(y - h * .96)}" width="{f(w * 1.12)}" height="{f(h * .08)}" rx="{f(h * .02)}" fill="#3A3C46" stroke="#0E0F14" stroke-width="{f(h * .01)}"/>')
    o.append(f'<rect x="{f(x - w * .56)}" y="{f(y - h * .18)}" width="{f(w * 1.12)}" height="{f(h * .06)}" rx="{f(h * .02)}" fill="#3A3C46" stroke="#0E0F14" stroke-width="{f(h * .01)}"/>')
    ates = s.rad([(0, "#FFF6CC"), (.45, "#FFB43A"), (1, "#C8442F")], .5, .75, .75, ad="sa")
    fx, fy, fw, fh = x - w * .3, y - h * .66, w * .6, h * .34
    o.append(f'<rect x="{f(fx - 4)}" y="{f(fy - 4)}" width="{f(fw + 8)}" height="{f(fh + 8)}" rx="6" fill="#121318"/>')
    o.append(f'<rect x="{f(fx)}" y="{f(fy)}" width="{f(fw)}" height="{f(fh)}" rx="4" fill="{ates}"/>')
    for k in range(3):
        bx = fx + fw * (.2 + k * .3)
        o.append(f'<path d="M{f(bx - fw * .1)} {f(fy + fh)} Q{f(bx - fw * .12)} {f(fy + fh * .45)} {f(bx)} {f(fy + fh * .15)} Q{f(bx + fw * .12)} {f(fy + fh * .45)} {f(bx + fw * .1)} {f(fy + fh)} Z" fill="#FFE08A" opacity=".85"/>')
    o.append(f'<path d="M{f(fx + fw * .1)} {f(fy + fh * .88)} h{f(fw * .8)}" stroke="#6E2A12" stroke-width="{f(h * .025)}" stroke-linecap="round"/>')
    o.append(f'<path d="M{f(fx)} {f(fy + fh * .34)} H{f(fx + fw)} M{f(fx)} {f(fy + fh * .67)} H{f(fx + fw)}" stroke="#121318" stroke-width="2" opacity=".5"/>')
    o.append(f'<rect x="{f(x + w * .34)}" y="{f(y - h * .54)}" width="{f(w * .08)}" height="{f(h * .1)}" rx="2" fill="#C9A86A" stroke="#0E0F14" stroke-width="1.4"/>')
    # boru
    bw = w * .22
    by = y - h * 2.1
    o.append(f'<path d="M{f(x - bw / 2)} {f(y - h * .96)} V{f(by + bw)} Q{f(x - bw / 2)} {f(by)} {f(x - bw * 1.5)} {f(by)} H{f(x - w * 1.6)} V{f(by + bw)} H{f(x - bw * 1.5)} Q{f(x + bw / 2)} {f(by + bw)} {f(x + bw / 2)} {f(by + bw * 1.6)} V{f(y - h * .96)} Z" fill="#3A3C46" stroke="#0E0F14" stroke-width="2"/>')
    for k in range(3):
        yy = y - h * (1.2 + k * .26)
        o.append(f'<path d="M{f(x - bw / 2)} {f(yy)} H{f(x + bw / 2)}" stroke="#0E0F14" stroke-width="2" opacity=".6"/>')
    o.append(f'<path d="M{f(x - w * 1.6)} {f(by - 4)} v{f(bw + 8)}" stroke="#7A6A5A" stroke-width="8"/>')
    return "".join(o)


def caydanlik(s, x, y, h, renk="#C8442F", ust="#2B50B5"):
    """Çift katlı çaydanlık: altta su kazanı, üstte demlik. (x, y): taban ortası."""
    w = h * .62
    g = s.lin([(0, acik(renk, .35)), (.5, renk), (1, koyu(renk, .3))], 0, 0, 1, 0, ad="cd")
    g2 = s.lin([(0, acik(ust, .35)), (.5, ust), (1, koyu(ust, .3))], 0, 0, 1, 0, ad="cd2")
    return (f'<path d="M{f(x - w / 2)} {f(y)} Q{f(x - w * .56)} {f(y - h * .36)} {f(x - w * .3)} {f(y - h * .5)} H{f(x + w * .3)} Q{f(x + w * .56)} {f(y - h * .36)} {f(x + w / 2)} {f(y)} Z" fill="{g}" stroke="#1B1D26" stroke-width="{f(h * .025)}"/>'
            f'<path d="M{f(x + w * .45)} {f(y - h * .24)} q{f(w * .28)} {f(-h * .06)} {f(w * .34)} {f(-h * .26)}" stroke="{koyu(renk, .2)}" stroke-width="{f(h * .06)}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{f(x - w * .28)} {f(y - h * .5)} Q{f(x - w * .36)} {f(y - h * .74)} {f(x - w * .18)} {f(y - h * .82)} H{f(x + w * .18)} Q{f(x + w * .36)} {f(y - h * .74)} {f(x + w * .28)} {f(y - h * .5)} Z" fill="{g2}" stroke="#1B1D26" stroke-width="{f(h * .025)}"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y - h * .86)}" rx="{f(w * .1)}" ry="{f(h * .04)}" fill="{ust}" stroke="#1B1D26" stroke-width="{f(h * .02)}"/>'
            f'<path d="M{f(x - w * .2)} {f(y - h * .66)} q{f(w * .2)} {f(-h * .05)} {f(w * .4)} 0" stroke="#FFFFFF" stroke-width="{f(h * .03)}" fill="none" opacity=".8"/>'
            f'<path d="M{f(x - w * .3)} {f(y - h * .24)} q{f(w * .3)} {f(-h * .06)} {f(w * .6)} 0" stroke="#FFFFFF" stroke-width="{f(h * .03)}" fill="none" opacity=".7"/>'
            f'<path d="M{f(x - w * .05)} {f(y - h * .95)} q{f(-w * .12)} {f(-h * .1)} 0 {f(-h * .2)} q{f(w * .12)} {f(-h * .1)} 0 {f(-h * .2)} M{f(x + w * .12)} {f(y - h * .92)} q{f(-w * .1)} {f(-h * .08)} 0 {f(-h * .16)}" stroke="#FFFFFF" stroke-width="{f(h * .035)}" fill="none" stroke-linecap="round" opacity=".85"/>')


def co_dedektoru(x, y, w):
    """Duvara takılı karbonmonoksit dedektörü: beyaz gövde, ızgara delikleri, yeşil ışık (sesli alarmlı)."""
    h = w * .7
    o = [f'<rect x="{f(x - w / 2)}" y="{f(y - h / 2)}" width="{f(w)}" height="{f(h)}" rx="{f(w * .16)}" fill="#F7F8FA" stroke="#1B1D26" stroke-width="{f(w * .04)}"/>']
    for k in range(3):
        o.append(f'<path d="M{f(x - w * .3)} {f(y - h * .24 + k * h * .2)} h{f(w * .4)}" stroke="#8A96A2" stroke-width="{f(w * .045)}" stroke-linecap="round"/>')
    o.append(f'<circle cx="{f(x + w * .3)}" cy="{f(y + h * .22)}" r="{f(w * .07)}" fill="#2BCB6A" stroke="#14753A" stroke-width="{f(w * .02)}"/>')
    o.append(f'<circle cx="{f(x + w * .3)}" cy="{f(y + h * .22)}" r="{f(w * .16)}" fill="#2BCB6A" opacity=".25"/>')
    o.append(f'<text x="{f(x - w * .1)}" y="{f(y + h * .36)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="{f(w * .24)}" fill="#1B1D26">CO</text>')
    return "".join(o)


def menfez(x, y, w, h):
    """Havalandırma menfezi (ızgara)."""
    o = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="3" fill="#E9EEF2" stroke="#4A5866" stroke-width="2"/>']
    for k in range(1, 5):
        yy = y + h * k / 5
        o.append(f'<path d="M{f(x + 4)} {f(yy)} H{f(x + w - 4)}" stroke="#4A5866" stroke-width="2.2"/>')
    return "".join(o)


def tren(s, x, y, uz, n=4, govde="#C8442F", serit="#F4F1EA", cati="#5E6672", pencere="#BFE3F0", isik_pencere=False, kar=True):
    """Yolcu treni (logosuz, temsilî): sola bakan lokomotif + n vagon. (x, y): rayın sol ucu; uz: toplam boy."""
    vw = uz / (n + 1.15)
    vh = vw * .3
    o = [f'<path d="M{f(x - 20)} {f(y + 4)} H{f(x + uz + 20)}" stroke="#5A4A3E" stroke-width="5"/>']
    for k in range(int((uz + 40) / 14)):
        o.append(f'<path d="M{f(x - 16 + k * 14)} {f(y + 1)} v8" stroke="#6E5A46" stroke-width="3"/>')
    g = s.lin([(0, acik(govde, .2)), (.6, govde), (1, koyu(govde, .25))], 0, y - vh, 0, y, kull="userSpaceOnUse", ad="tr")
    pc = "#FFD27A" if isik_pencere else pencere
    for i in range(n + 1):
        vx = x + i * vw * 1.02 + (0 if i == 0 else vw * .13)
        ww = vw * (1.15 if i == 0 else 1)
        if i == 0:
            o.append(f'<path d="M{f(vx)} {f(y - 4)} V{f(y - vh * .55)} L{f(vx + ww * .16)} {f(y - vh)} H{f(vx + ww)} V{f(y - 4)} Z" fill="{g}" stroke="#1B1D26" stroke-width="2.2"/>')
            o.append(f'<path d="M{f(vx + ww * .03)} {f(y - vh * .55)} L{f(vx + ww * .16)} {f(y - vh * .9)} H{f(vx + ww * .3)} V{f(y - vh * .55)} Z" fill="{pc}" stroke="#1B1D26" stroke-width="1.6"/>')
            o.append(f'<circle cx="{f(vx + ww * .05)}" cy="{f(y - vh * .3)}" r="{f(vh * .07)}" fill="#FFF4C8" stroke="#1B1D26" stroke-width="1.2"/>')
            luk = s.rad([(0, "#FFF4C8", .7), (1, "#FFF4C8", 0)], vx - ww * .1, y - vh * .3, ww * .5, kull="userSpaceOnUse", ad="tl")
            o.append(f'<ellipse cx="{f(vx - ww * .1)}" cy="{f(y - vh * .3)}" rx="{f(ww * .45)}" ry="{f(vh * .3)}" fill="{luk}"/>')
            for k in range(3):
                o.append(f'<rect x="{f(vx + ww * (.42 + k * .17))}" y="{f(y - vh * .82)}" width="{f(ww * .1)}" height="{f(vh * .3)}" fill="{koyu(govde, .2)}"/>')
        else:
            o.append(f'<rect x="{f(vx)}" y="{f(y - vh)}" width="{f(ww)}" height="{f(vh - 4)}" rx="{f(vh * .1)}" fill="{g}" stroke="#1B1D26" stroke-width="2.2"/>')
            for k in range(5):
                o.append(f'<rect x="{f(vx + ww * (.06 + k * .185))}" y="{f(y - vh * .82)}" width="{f(ww * .13)}" height="{f(vh * .32)}" rx="2" fill="{pc}" stroke="#1B1D26" stroke-width="1.4"/>')
        o.append(f'<path d="M{f(vx)} {f(y - vh * .38)} H{f(vx + ww)}" stroke="{serit}" stroke-width="{f(vh * .07)}"/>')
        o.append(f'<path d="M{f(vx + (ww * .16 if i == 0 else 0))} {f(y - vh)} H{f(vx + ww)}" stroke="{cati}" stroke-width="{f(vh * .1)}"/>')
        if kar:
            o.append(f'<path d="M{f(vx + (ww * .16 if i == 0 else 2))} {f(y - vh - 2)} q{f(ww * .2)} {f(-vh * .1)} {f(ww * .4)} 0 t{f(ww * .4)} 0 L{f(vx + ww - 2)} {f(y - vh + 2)} H{f(vx + (ww * .16 if i == 0 else 2))} Z" fill="#FFFFFF"/>')
        for wx in (vx + ww * .18, vx + ww * .82):
            o.append(f'<circle cx="{f(wx)}" cy="{f(y - 1)}" r="{f(vh * .12)}" fill="#2A2C34" stroke="#0E0F14" stroke-width="1.4"/>')
    return "".join(o)


def buhar(s, x, y, h, tohum, op=.7, en=1.0):
    """Sıcak su buharı: yükselip açılan yumuşak bulutçuklar."""
    r = RNG(tohum)
    o = []
    for k in range(7):
        t = k / 6
        cx = x + r.uniform(-12, 12) * en + math.sin(t * 4 + tohum) * 16 * en
        cy = y - h * t
        rr = (10 + 28 * t) * en * r.uniform(.8, 1.2)
        g = s.rad([(0, "#FFFFFF", op * (1 - .6 * t)), (1, "#FFFFFF", 0)], cx, cy, rr, kull="userSpaceOnUse", ad="bh")
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr)}" fill="{g}"/>')
    return "".join(o)


def kaplica_havuz(s, x, y, w, h, tohum, su="#5FD0D0"):
    """Açık hava kaplıca havuzu: beyaz mineral kabuklu kenar (kademeli), turkuaz sıcak su, buhar."""
    r = RNG(tohum)
    o = []
    for k in range(3):
        kw, kh = w * (1 - k * .12), h * (1 - k * .18)
        ky = y - k * h * .16
        o.append(f'<ellipse cx="{f(x)}" cy="{f(ky)}" rx="{f(kw / 2 + 10)}" ry="{f(kh / 2 + 6)}" fill="{["#E9E3D6", "#F4EFE4", "#FFFFFF"][k]}" stroke="#C9BFA8" stroke-width="2"/>')
        for j in range(int(kw / 30)):
            a = math.pi * (j + .5) / int(kw / 30)
            px = x - kw / 2 * math.cos(a)
            py = ky + kh / 2 * .9 * math.sin(a) + 6
            o.append(f'<path d="M{f(px)} {f(py - 4)} q3 8 0 12" stroke="#D9CFB8" stroke-width="2" fill="none"/>')
    g = s.rad([(0, acik(su, .4)), (.7, su), (1, koyu(su, .25))], .5, .4, .7, ad="kh")
    sw, sh = w * .66, h * .48
    o.append(f'<ellipse cx="{f(x)}" cy="{f(y - h * .32)}" rx="{f(sw / 2)}" ry="{f(sh / 2)}" fill="{g}"/>')
    for k in range(5):
        o.append(f'<path d="M{f(x - sw * .32 + r.uniform(0, sw * .4))} {f(y - h * .32 + r.uniform(-sh * .2, sh * .2))} q8 -3 16 0" stroke="#FFFFFF" stroke-width="2" fill="none" opacity=".7"/>')
    for k in range(4):
        o.append(buhar(s, x - sw * .3 + k * sw * .2, y - h * .38, h * 1.6, tohum * 10 + k, op=.6, en=.9))
    return "".join(o)


# ------------------------------------------------------------------ Erzurum: Taşhan, tespih, paslı kapı; Palandöken: telesiyej

def tespih(x, y, n=11, r=4.2, renk="#1B1D26", puskul="#1B1D26"):
    """Asılı Oltu taşı tespihi: siyah boncuklar, imame, püskül."""
    o = []
    for k in range(n):
        a = math.pi * (k + .5) / n
        px = x + r * 3.2 * math.cos(a)
        py = y + r * 4.6 * math.sin(a)
        o.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r)}" fill="{renk}"/><circle cx="{f(px - r * .3)}" cy="{f(py - r * .3)}" r="{f(r * .3)}" fill="#FFFFFF" opacity=".7"/>')
    by = y + r * 4.6 + r * 1.6
    o.append(f'<rect x="{f(x - r * .7)}" y="{f(by - r)}" width="{f(r * 1.4)}" height="{f(r * 3)}" rx="{f(r * .6)}" fill="{renk}"/>')
    o.append(f'<path d="M{f(x - r * .9)} {f(by + r * 2)} L{f(x - r * 1.4)} {f(by + r * 6)} H{f(x + r * 1.4)} L{f(x + r * .9)} {f(by + r * 2)} Z" fill="{puskul}" opacity=".9"/>')
    return "".join(o)


def tashan(s, x, y, w, h, tohum, tas="#B79C78", isik=-1):
    """Erzurum Taşhan'ı esinli iki katlı kesme taş han cephesi: alt katta kemerli dükkânlar (Oltu taşı tespihleri),
    üst katta revak; saçakta kar. Temsilî."""
    r = RNG(tohum)
    o = []
    g = s.lin([(0, acik(tas, .12)), (1, koyu(tas, .12))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="th")
    o.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{g}"/>')
    for k in range(1, int(h / 15)):
        o.append(f'<path d="M{f(x)} {f(y - k * 15)} H{f(x + w)}" stroke="{koyu(tas, .3)}" stroke-width="1" opacity=".35"/>')
    o.append(f'<rect x="{f(x)}" y="{f(y - h * .52)}" width="{f(w)}" height="{f(h * .05)}" fill="{koyu(tas, .2)}"/>')
    o.append(f'<rect x="{f(x - 6)}" y="{f(y - h - 6)}" width="{f(w + 12)}" height="12" fill="{koyu(tas, .25)}"/>')
    o.append(f'<path d="M{f(x - 8)} {f(y - h - 6)} q{f(w * .25)} -10 {f(w * .5)} -2 t{f(w * .5 + 16)} 0 v4 H{f(x - 8)} Z" fill="#FFFFFF"/>')
    n = max(4, int(w / 70))
    aw = w / n
    for i in range(n):
        ax = x + aw * (i + .5)
        # alt kat dükkân kemeri
        kw, kh = aw * .74, h * .4
        o.append(f'<path d="M{f(ax - kw / 2)} {f(y)} V{f(y - kh * .62)} Q{f(ax - kw / 2)} {f(y - kh)} {f(ax)} {f(y - kh * 1.04)} Q{f(ax + kw / 2)} {f(y - kh)} {f(ax + kw / 2)} {f(y - kh * .62)} V{f(y)} Z" fill="#3E2A1E"/>')
        ic = s.rad([(0, "#FFD99A", .75), (1, "#FFD99A", 0)], ax, y - kh * .45, kw * .7, kull="userSpaceOnUse", ad="ti")
        o.append(f'<path d="M{f(ax - kw / 2 + 4)} {f(y)} V{f(y - kh * .6)} Q{f(ax - kw / 2 + 4)} {f(y - kh * .95)} {f(ax)} {f(y - kh)} Q{f(ax + kw / 2 - 4)} {f(y - kh * .95)} {f(ax + kw / 2 - 4)} {f(y - kh * .6)} V{f(y)} Z" fill="{ic}"/>')
        for t in range(3):
            o.append(tespih(ax - kw * .26 + t * kw * .26, y - kh * .78, n=9, r=2.6 + (t % 2) * .4))
        o.append(f'<path d="M{f(ax - kw / 2 - 3)} {f(y)} V{f(y - kh * .62)} Q{f(ax - kw / 2 - 3)} {f(y - kh - 3)} {f(ax)} {f(y - kh * 1.08)} Q{f(ax + kw / 2 + 3)} {f(y - kh - 3)} {f(ax + kw / 2 + 3)} {f(y - kh * .62)} V{f(y)}" fill="none" stroke="{koyu(tas, .35)}" stroke-width="3"/>')
        # üst kat revak
        uw, uh = aw * .56, h * .3
        uy = y - h * .56
        o.append(f'<path d="M{f(ax - uw / 2)} {f(uy)} V{f(uy - uh * .6)} Q{f(ax - uw / 2)} {f(uy - uh)} {f(ax)} {f(uy - uh * 1.04)} Q{f(ax + uw / 2)} {f(uy - uh)} {f(ax + uw / 2)} {f(uy - uh * .6)} V{f(uy)} Z" fill="#2E2A30"/>')
        o.append(f'<path d="M{f(ax - uw * .42)} {f(uy)} V{f(uy - uh * .55)} Q{f(ax - uw * .42)} {f(uy - uh * .88)} {f(ax)} {f(uy - uh * .92)} Q{f(ax + uw * .42)} {f(uy - uh * .88)} {f(ax + uw * .42)} {f(uy - uh * .55)} V{f(uy)} Z" fill="#FFD27A" opacity=".55"/>')
    o.append(f'<rect x="{f(x + (w * .7 if isik < 0 else 0))}" y="{f(y - h)}" width="{f(w * .3)}" height="{f(h)}" fill="#0E1A2A" opacity=".1"/>')
    return "".join(o)


def pasli_kapi(s, x, y, w, h, tohum):
    """Paslanmış demir bahçe kapısı: dikey çubuklar, kıvrımlı üst, turuncu-kahve pas lekeleri ve akıntıları."""
    r = RNG(tohum)
    o = []
    demir = "#3E4652"
    pas = ["#B5521E", "#C8692A", "#8E3A16", "#D98A3A"]
    n = 7
    for i in range(n + 1):
        px = x + w * i / n
        o.append(f'<path d="M{f(px)} {f(y)} V{f(y - h)}" stroke="{demir}" stroke-width="5" stroke-linecap="round"/>')
        o.append(f'<path d="M{f(px)} {f(y - h)} l-5 -12 l5 -6 l5 6 Z" fill="{demir}"/>')
    for yy in (y - h * .12, y - h * .55, y - h * .92):
        o.append(f'<path d="M{f(x - 4)} {f(yy)} H{f(x + w + 4)}" stroke="{demir}" stroke-width="6" stroke-linecap="round"/>')
    for i in range(n):
        cx = x + w * (i + .5) / n
        o.append(f'<path d="M{f(cx - w / n * .4)} {f(y - h * .55)} q{f(w / n * .4)} {f(-h * .18)} {f(w / n * .8)} 0" stroke="{demir}" stroke-width="3" fill="none"/>')
    for _ in range(26):
        px, py = x + r.uniform(0, w), y - r.uniform(.05, .95) * h
        rr = r.uniform(3, 9)
        c = r.choice(pas)
        o.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(rr)}" ry="{f(rr * .7)}" fill="{c}" opacity="{f(r.uniform(.6, .95), 2)}"/>')
        if r.random() < .5:
            o.append(f'<path d="M{f(px)} {f(py)} q{f(r.uniform(-2, 2))} {f(rr * 2)} 0 {f(rr * 3.4)}" stroke="{c}" stroke-width="{f(rr * .45)}" stroke-linecap="round" opacity=".7"/>')
    return "".join(o)


def telesiyej(x0, y0, x1, y1, n, tohum, direk=4):
    """Telesiyej: halat, direkler, asılı sandalyeler."""
    r = RNG(tohum)
    o = [f'<path d="M{f(x0)} {f(y0)} L{f(x1)} {f(y1)}" stroke="#2A2C34" stroke-width="2.4"/>',
         f'<path d="M{f(x0)} {f(y0 + 8)} L{f(x1)} {f(y1 + 8)}" stroke="#2A2C34" stroke-width="1.6" opacity=".7"/>']
    for k in range(direk + 1):
        t = k / direk
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        hh = 70 + 30 * (1 - t)
        o.append(f'<path d="M{f(px)} {f(py - 6)} V{f(py + hh)}" stroke="#4A5260" stroke-width="5"/><path d="M{f(px - 12)} {f(py - 4)} h24" stroke="#4A5260" stroke-width="4"/>')
    for k in range(n):
        t = (k + .5) / n
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        o.append(f'<path d="M{f(px)} {f(py)} v20" stroke="#2A2C34" stroke-width="1.8"/><path d="M{f(px - 9)} {f(py + 20)} h18 v8 h-18 Z" fill="{r.choice(["#E2533D", "#2B50B5", "#F0A21A"])}" stroke="#1B1D26" stroke-width="1.4"/>')
    return "".join(o)


# ------------------------------------------------------------------ köprü, istasyon, bazalt kale

def tas_kopru(s, x0, x1, y, h, kemerler, tas="#B8A386", isik=-1, kar=True):
    """Kesme taş köprü. kemerler: [(merkez_x, açıklık, yükseklik), …]. (y): su yüzeyi; h: güverte yüksekliği."""
    o = []
    g = s.lin([(0, acik(tas, .15)), (1, koyu(tas, .2))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="kp")
    d = f"M{f(x0)} {f(y + 6)} V{f(y - h)} H{f(x1)} V{f(y + 6)}"
    for cx, ac, yk in sorted(kemerler, key=lambda k: -k[0]):
        d += f" H{f(cx + ac / 2)} V{f(y - yk * .25)} Q{f(cx + ac / 2)} {f(y - yk)} {f(cx)} {f(y - yk * 1.06)} Q{f(cx - ac / 2)} {f(y - yk)} {f(cx - ac / 2)} {f(y - yk * .25)} V{f(y + 6)}"
    d += " Z"
    o.append(f'<path d="{d}" fill="{g}" stroke="{koyu(tas, .45)}" stroke-width="2.4" fill-rule="evenodd"/>')
    for cx, ac, yk in kemerler:
        o.append(f'<path d="M{f(cx - ac / 2 - 10)} {f(y - yk * .25)} Q{f(cx - ac / 2 - 10)} {f(y - yk - 12)} {f(cx)} {f(y - yk * 1.06 - 14)} Q{f(cx + ac / 2 + 10)} {f(y - yk - 12)} {f(cx + ac / 2 + 10)} {f(y - yk * .25)}" fill="none" stroke="{koyu(tas, .3)}" stroke-width="5" opacity=".7"/>')
        for k in range(9):
            a = math.pi * (k + .5) / 9
            o.append(f'<path d="M{f(cx - (ac / 2) * math.cos(a))} {f(y - yk * .25 - (yk * .78) * math.sin(a))} l{f(-6 * math.cos(a))} {f(-10 * math.sin(a))}" stroke="{koyu(tas, .35)}" stroke-width="1.6"/>')
    for k in range(1, int(h / 18)):
        o.append(f'<path d="M{f(x0)} {f(y - h + k * 18)} H{f(x1)}" stroke="{koyu(tas, .3)}" stroke-width="1" opacity=".25"/>')
    o.append(f'<rect x="{f(x0 - 6)}" y="{f(y - h - 12)}" width="{f(x1 - x0 + 12)}" height="14" fill="{acik(tas, .1)}" stroke="{koyu(tas, .45)}" stroke-width="2"/>')
    if kar:
        o.append(f'<path d="M{f(x0 - 8)} {f(y - h - 12)} q{f((x1 - x0) * .25)} -9 {f((x1 - x0) * .5)} -2 t{f((x1 - x0) * .5 + 16)} 0 v5 H{f(x0 - 8)} Z" fill="#FFFFFF"/>')
    return "".join(o)


def istasyon(s, x, y, w, h, tohum, tas="#A8A096", cati="#5E6672"):
    """İki katlı kesme taş istasyon binası: kemerli pencereler, cephe saati, karlı beşik çatı, peron saçağı. Temsilî."""
    o = []
    g = s.lin([(0, acik(tas, .15)), (1, koyu(tas, .15))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="is")
    o.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{g}"/>')
    for k in range(1, int(h / 16)):
        o.append(f'<path d="M{f(x)} {f(y - k * 16)} H{f(x + w)}" stroke="{koyu(tas, .3)}" stroke-width="1" opacity=".3"/>')
    ch = h * .32
    o.append(f'<path d="M{f(x - w * .04)} {f(y - h)} L{f(x + w * .1)} {f(y - h - ch)} H{f(x + w * .9)} L{f(x + w * 1.04)} {f(y - h)} Z" fill="{cati}"/>')
    o.append(f'<path d="M{f(x - w * .05)} {f(y - h + 2)} L{f(x + w * .1)} {f(y - h - ch - 3)} H{f(x + w * .9)} L{f(x + w * 1.05)} {f(y - h + 2)} Q{f(x + w * .7)} {f(y - h - ch * .3)} {f(x + w * .5)} {f(y - h - ch * .22)} Q{f(x + w * .25)} {f(y - h - ch * .32)} {f(x - w * .05)} {f(y - h + 2)} Z" fill="#FFFFFF"/>')
    # orta alınlık + saat
    o.append(f'<path d="M{f(x + w * .38)} {f(y - h)} L{f(x + w * .5)} {f(y - h - ch * 1.25)} L{f(x + w * .62)} {f(y - h)} Z" fill="{koyu(tas, .1)}"/>')
    cx, cy, rr = x + w * .5, y - h - ch * .45, ch * .32
    o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr)}" fill="#FFFDF7" stroke="#2A2C34" stroke-width="3"/><path d="M{f(cx)} {f(cy)} v{f(-rr * .7)} M{f(cx)} {f(cy)} l{f(rr * .5)} {f(rr * .2)}" stroke="#2A2C34" stroke-width="3" stroke-linecap="round"/>')
    for kat in (0, 1):
        yy = y - h * (.12 + kat * .46)
        for i in range(7):
            px = x + w * (.08 + i * .13)
            ww, hh = w * .07, h * .3
            o.append(f'<path d="M{f(px)} {f(yy)} V{f(yy - hh * .7)} Q{f(px)} {f(yy - hh)} {f(px + ww / 2)} {f(yy - hh)} Q{f(px + ww)} {f(yy - hh)} {f(px + ww)} {f(yy - hh * .7)} V{f(yy)} Z" fill="#FFD27A" stroke="{koyu(tas, .45)}" stroke-width="2.4"/>')
            o.append(f'<path d="M{f(px + ww / 2)} {f(yy)} V{f(yy - hh * .9)} M{f(px)} {f(yy - hh * .5)} H{f(px + ww)}" stroke="{koyu(tas, .45)}" stroke-width="1.4"/>')
    # peron saçağı
    o.append(f'<path d="M{f(x - w * .06)} {f(y - h * .2)} H{f(x + w * 1.06)} L{f(x + w * 1.1)} {f(y - h * .12)} H{f(x - w * .1)} Z" fill="#7A5A3A" stroke="#4A3422" stroke-width="2"/>')
    o.append(f'<path d="M{f(x - w * .08)} {f(y - h * .21)} H{f(x + w * 1.08)}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')
    for i in range(6):
        px = x - w * .02 + i * w * .208
        o.append(f'<path d="M{f(px)} {f(y - h * .12)} V{f(y)}" stroke="#4A3422" stroke-width="4"/>')
    return "".join(o)


def bazalt_kale(s, x0, x1, y, h, tohum, isik=-1, bayrak=True, kar=True, gece=False):
    """Kars Kalesi esinli bazalt kale: koyu bazalt tepe, yamaca basamaklanan surlar, köşe burçları, tepede iç kale + bayrak.
    Temsilî. Döndürür: (svg, tepe_noktasi)."""
    from cizim.karakter import turk_bayragi
    r = RNG(tohum)
    w = x1 - x0
    o = []
    bz = "#3A3C46" if not gece else "#232741"
    bz2 = "#565A66" if not gece else "#2E3352"
    # tepe (bazalt kaya)
    n = 24
    ust = []
    for i in range(n + 1):
        t = i / n
        yy = y - h * (.15 + .55 * math.sin(math.pi * min(1, t * 1.05)) ** 1.4) + r.uniform(-h * .02, h * .02)
        ust.append((x0 + w * t, yy))
    tepe = [(x0 - 20, y)] + ust + [(x1 + 20, y)]
    g = s.lin([(0, acik(bz2, .1)), (1, koyu(bz, .25))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="bk")
    o.append(f'<path d="{cizgi_d(tepe, True)}" fill="{g}"/>')
    for _ in range(int(w / 26)):
        px = x0 + r.uniform(.04, .96) * w
        j = int((px - x0) / w * n)
        top = ust[j][1] + 6
        boy = (y - top) * r.uniform(.3, .9)
        o.append(f'<path d="M{f(px)} {f(top)} l{f(r.uniform(4, 10))} {f(boy)}" stroke="{koyu(bz, .35)}" stroke-width="{f(r.uniform(1.5, 4))}" opacity=".6"/>')
    if kar:
        for _ in range(int(w / 40)):
            px = x0 + r.uniform(.05, .95) * w
            j = int((px - x0) / w * n)
            py = ust[j][1] + r.uniform(4, (y - ust[j][1]) * .7)
            rw = r.uniform(14, 40)
            o.append(f'<path d="M{f(px - rw)} {f(py)} q{f(rw)} {f(-rw * .3)} {f(rw * 2)} 0 q{f(-rw)} {f(rw * .16)} {f(-rw * 2)} 0 Z" fill="#FFFFFF" opacity=".9"/>')
    # surlar: yamaca basamaklanan duvar parçaları
    tas = "#4A4C58" if not gece else "#2A2F4C"
    tas_a = "#6A6E7C" if not gece else "#3A4066"
    sh = h * .16
    parca = []
    adim = 7
    for i in range(adim):
        t0, t1 = .1 + i * .8 / adim, .1 + (i + 1) * .8 / adim
        a, b = int(t0 * n), int(t1 * n)
        yy = min(ust[a][1], ust[b][1]) - 4
        parca.append((x0 + w * t0, x0 + w * t1, yy))
    for xa, xb, yy in parca:
        gs = s.lin([(0, tas_a), (1, tas)], 0, yy - sh, 0, yy + 10, kull="userSpaceOnUse", ad="ks")
        o.append(f'<rect x="{f(xa)}" y="{f(yy - sh)}" width="{f(xb - xa + 1)}" height="{f(sh + 20)}" fill="{gs}"/>')
        for k in range(1, 4):
            o.append(f'<path d="M{f(xa)} {f(yy - sh + k * sh / 4)} H{f(xb)}" stroke="{koyu(tas, .4)}" stroke-width="1" opacity=".5"/>')
        mz = h * .035
        xx = xa
        while xx < xb - mz:
            o.append(f'<rect x="{f(xx)}" y="{f(yy - sh - mz)}" width="{f(mz)}" height="{f(mz + 1)}" fill="{tas_a}"/>')
            if kar:
                o.append(f'<rect x="{f(xx - 1)}" y="{f(yy - sh - mz - 3)}" width="{f(mz + 2)}" height="4" rx="2" fill="#FFFFFF"/>')
            xx += mz * 1.8
    # burçlar
    for t in (.12, .34, .62, .86):
        j = int(t * n)
        bx, by = x0 + w * t, ust[j][1] - 6
        bw, bh = h * .14, sh + h * .14
        gb = s.lin([(0, acik(tas_a, .1)), (.5, tas_a), (1, koyu(tas, .2))], bx - bw / 2, 0, bx + bw / 2, 0, kull="userSpaceOnUse", ad="kb")
        o.append(f'<rect x="{f(bx - bw / 2)}" y="{f(by - bh)}" width="{f(bw)}" height="{f(bh + 14)}" fill="{gb}"/>')
        for k in range(3):
            o.append(f'<rect x="{f(bx - bw / 2 + k * bw * .4)}" y="{f(by - bh - h * .04)}" width="{f(bw * .2)}" height="{f(h * .04 + 1)}" fill="{tas_a}"/>')
        if kar:
            o.append(f'<rect x="{f(bx - bw / 2 - 2)}" y="{f(by - bh - 3)}" width="{f(bw + 4)}" height="5" rx="2" fill="#FFFFFF"/>')
        o.append(f'<rect x="{f(bx - bw * .08)}" y="{f(by - bh * .6)}" width="{f(bw * .16)}" height="{f(bh * .22)}" rx="{f(bw * .08)}" fill="{koyu(tas, .5) if not gece else "#FFD27A"}"/>')
    # iç kale (tepede)
    j = int(.5 * n)
    kx, ky = x0 + w * .5, min(p[1] for p in ust) - 2
    kw, kh = h * .34, h * .3
    gi = s.lin([(0, acik(tas_a, .12)), (.5, tas_a), (1, koyu(tas, .25))], kx - kw / 2, 0, kx + kw / 2, 0, kull="userSpaceOnUse", ad="ki")
    o.append(f'<rect x="{f(kx - kw / 2)}" y="{f(ky - kh)}" width="{f(kw)}" height="{f(kh + 16)}" fill="{gi}"/>')
    for k in range(5):
        o.append(f'<rect x="{f(kx - kw / 2 + k * kw * .21)}" y="{f(ky - kh - h * .045)}" width="{f(kw * .12)}" height="{f(h * .045 + 1)}" fill="{tas_a}"/>')
    if kar:
        o.append(f'<rect x="{f(kx - kw / 2 - 3)}" y="{f(ky - kh - 3)}" width="{f(kw + 6)}" height="6" rx="3" fill="#FFFFFF"/>')
    for k in range(2):
        o.append(f'<rect x="{f(kx - kw * .3 + k * kw * .44)}" y="{f(ky - kh * .65)}" width="{f(kw * .12)}" height="{f(kh * .22)}" rx="{f(kw * .06)}" fill="{"#FFD27A" if gece else koyu(tas, .5)}"/>')
    tepe_nokta = (kx, ky - kh - h * .045)
    if bayrak:
        o.append(f'<path d="M{f(kx)} {f(ky - kh - h * .04)} v{f(-h * .34)}" stroke="#5A4A3A" stroke-width="{f(max(2, h * .012))}"/>')
        o.append(turk_bayragi(kx, ky - kh - h * .38, h * .13, h * .018))
    return "".join(o), tepe_nokta
