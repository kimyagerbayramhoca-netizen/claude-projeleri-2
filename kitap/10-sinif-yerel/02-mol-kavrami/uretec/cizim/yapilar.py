"""Simge yapılar ve yerel nesneler: kümbet (Gevaş/Ahlat), Ahlat Selçuklu mezar taşları, Van Kalesi
(uzun kaya + sur + burçlar), Adilcevaz kalesi, iskele, fener, şelale (Muradiye), asma köprü,
semaver, çay masası, yayla çadırı, koyun, obsidyen parçaları, el-Hâzinî terazisi.

Çizgi kuralı: manzara parçaları siyah kontur ALMAZ; dolgunun koyu tonu kullanılır (cizgi=None → otomatik).
"""
import math
from .temel import f, nok, cizgi_d, egri_d, karis, acik, koyu, orta_nokta, rng as RNG, selcuklu_yildizi
from .renkler import OBS, ALTIN, ALTIN_K, ALTIN_A, LAJVER, GOL, KEH


def _isik_tonu(renk, aci, isik=-1):
    """Yüzey normali açısına göre aydınlık/gölge tonu (aci: radyan, 0 = izleyiciye dönük)."""
    t = math.sin(aci) * (-isik)  # ışık soldaysa sola dönük yüzler (negatif açı) aydınlık
    return acik(renk, .28 * max(0, -t) + .04) if t < 0 else koyu(renk, .38 * t + .02)


# ------------------------------------------------------------------ kümbet

def kumbet(s, x, y, h, tohum=1, tas="#C99E74", cati=None, isik=-1, kenar=12, kapi=True, cizgi=None):
    """Selçuklu kümbeti: kare kaide + çokgen gövde (kenar sayısı) + bezemeli korniş + piramit çatı."""
    cati = cati or koyu(tas, .08)
    cz = cizgi or koyu(tas, .55)
    R = h * .26
    kh = h * .12          # kaide
    gh = h * .44          # gövde
    kor = h * .055        # korniş
    ch = h * .36          # çatı
    o = []
    # gölge
    o.append(f'<ellipse cx="{f(x + R * .4 * -isik)}" cy="{f(y)}" rx="{f(R * 1.9)}" ry="{f(h * .035)}" fill="#1B1D26" opacity=".22"/>')
    # kaide (kare, iki yüz görünür)
    kw = R * 1.3
    o.append(f'<rect x="{f(x - kw)}" y="{f(y - kh)}" width="{f(kw * 2)}" height="{f(kh)}" fill="{acik(tas, .05)}" stroke="{cz}" stroke-width="{f(h * .006)}"/>')
    o.append(f'<path d="M{f(x - kw)} {f(y - kh * .5)} H{f(x + kw)}" stroke="{koyu(tas, .2)}" stroke-width="{f(h * .004)}"/>')
    o.append(f'<rect x="{f(x + (0 if isik < 0 else -kw))}" y="{f(y - kh)}" width="{f(kw)}" height="{f(kh)}" fill="#000" opacity=".14"/>')
    # gövde yüzleri
    y0, y1 = y - kh, y - kh - gh
    yuz = []
    for i in range(kenar):
        a0 = -math.pi / 2 + (i - .5) * 2 * math.pi / kenar
        a1 = a0 + 2 * math.pi / kenar
        am = (a0 + a1) / 2
        if math.cos(am) <= 0.02:  # arka yüz (izleyici +z'de varsayılır; cos>0 ön)
            pass
        xa, xb = x + R * math.sin(a0 + math.pi / 2), x + R * math.sin(a1 + math.pi / 2)
        n = am + math.pi / 2  # normalin yatay açısı
        if math.cos(n) > 0.02:
            yuz.append((xa, xb, n))
    for xa, xb, n in yuz:
        ton = _isik_tonu(tas, n, isik)
        o.append(f'<path d="M{f(xa)} {f(y0)} L{f(xb)} {f(y0)} L{f(xb)} {f(y1)} L{f(xa)} {f(y1)} Z" fill="{ton}" stroke="{koyu(ton, .25)}" stroke-width="{f(h * .003)}"/>')
        # kör kemer (sivri)
        if abs(xb - xa) > R * .22:
            cx = (xa + xb) / 2
            ww = abs(xb - xa) * .32
            o.append(f'<path d="M{f(cx - ww)} {f(y0 - gh * .12)} V{f(y1 + gh * .42)} Q{f(cx - ww)} {f(y1 + gh * .22)} {f(cx)} {f(y1 + gh * .14)} Q{f(cx + ww)} {f(y1 + gh * .22)} {f(cx + ww)} {f(y1 + gh * .42)} V{f(y0 - gh * .12)}" '
                     f'fill="none" stroke="{koyu(ton, .3)}" stroke-width="{f(h * .005)}"/>')
    # kapı (ön yüz)
    if kapi:
        dw = R * .34
        o.append(f'<path d="M{f(x - dw)} {f(y0)} V{f(y0 - gh * .45)} Q{f(x - dw)} {f(y0 - gh * .7)} {f(x)} {f(y0 - gh * .8)} Q{f(x + dw)} {f(y0 - gh * .7)} {f(x + dw)} {f(y0 - gh * .45)} V{f(y0)} Z" fill="{koyu(tas, .55)}"/>')
        o.append(f'<path d="M{f(x - dw * 1.5)} {f(y0)} V{f(y0 - gh * .5)} Q{f(x - dw * 1.5)} {f(y0 - gh * .8)} {f(x)} {f(y0 - gh * .92)} Q{f(x + dw * 1.5)} {f(y0 - gh * .8)} {f(x + dw * 1.5)} {f(y0 - gh * .5)} V{f(y0)}" fill="none" stroke="{koyu(tas, .35)}" stroke-width="{f(h * .008)}"/>')
        # mukarnas izlenimi: kapı üstünde küçük basamaklar
        for k in range(3):
            yy = y0 - gh * (.55 + k * .08)
            o.append(f'<path d="M{f(x - dw * (.9 - k * .25))} {f(yy)} q{f(dw * (.9 - k * .25))} {f(-gh * .05)} {f(dw * 2 * (.9 - k * .25))} 0" fill="none" stroke="{acik(tas, .3)}" stroke-width="{f(h * .004)}"/>')
    # korniş + bezeme şeridi (zikzak)
    ky = y1 - kor
    o.append(f'<rect x="{f(x - R * 1.06)}" y="{f(ky)}" width="{f(R * 2.12)}" height="{f(kor)}" fill="{acik(tas, .12)}" stroke="{cz}" stroke-width="{f(h * .004)}"/>')
    zz = []
    n = 14
    for i in range(n + 1):
        zz.append((x - R * 1.02 + R * 2.04 * i / n, ky + (kor * .25 if i % 2 else kor * .78)))
    o.append(f'<path d="{cizgi_d(zz)}" fill="none" stroke="{koyu(tas, .35)}" stroke-width="{f(h * .004)}"/>')
    # çatı: piramit yüzleri
    ax, ay = x, ky - ch
    for xa, xb, n_ in yuz:
        ton = _isik_tonu(cati, n_, isik)
        xa2, xb2 = x + (xa - x) * 1.08, x + (xb - x) * 1.08
        o.append(f'<path d="M{f(xa2)} {f(ky)} L{f(xb2)} {f(ky)} L{f(ax)} {f(ay)} Z" fill="{ton}" stroke="{koyu(ton, .2)}" stroke-width="{f(h * .003)}"/>')
    o.append(f'<path d="M{f(ax)} {f(ay)} v{f(-h * .04)}" stroke="{koyu(cati, .4)}" stroke-width="{f(h * .01)}" stroke-linecap="round"/>')
    return "".join(o)


# ------------------------------------------------------------------ Ahlat mezar taşı

def mezar_tasi(s, x, y, w, h, tohum, renk="#B8673E", isik=-1, egim=0.0, likan=True, sade=False):
    """Ahlat Selçuklu mezar taşı (şahide): volkanik tüf; kenar şeridi, sivri kemerli niş, rozet.
    Yazı yerine yalnızca geometrik oyma (kutsal metin/hat kullanılmaz)."""
    r = RNG(tohum)
    d = w * .16  # kalınlık (yan yüz)
    cz = koyu(renk, .45)
    tep = h * .1
    on = [(x - w / 2, y), (x - w / 2, y - h + tep), (x - w / 2 + w * .12, y - h + tep * .2), (x, y - h), (x + w / 2 - w * .12, y - h + tep * .2), (x + w / 2, y - h + tep), (x + w / 2, y)]
    yan_x = (x + w / 2) if isik < 0 else (x - w / 2)
    sg = d if isik < 0 else -d
    yan = [(yan_x, y), (yan_x, y - h + tep), (yan_x + sg, y - h + tep + d * .4), (yan_x + sg, y - d * .2)]
    o = [f'<g transform="rotate({f(egim)} {f(x)} {f(y)})">',
         f'<ellipse cx="{f(x + d * .8 * -isik)}" cy="{f(y)}" rx="{f(w * .75)}" ry="{f(h * .025)}" fill="#1B1D26" opacity=".25"/>',
         f'<path d="{cizgi_d(yan, True)}" fill="{koyu(renk, .32)}"/>']
    g = s.lin([(0, acik(renk, .12)), (1, koyu(renk, .1))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="mt")
    o.append(f'<path d="{cizgi_d(on, True)}" fill="{g}" stroke="{cz}" stroke-width="{f(w * .02)}" stroke-linejoin="round"/>')
    if not sade:
        ic = w * .1
        o.append(f'<path d="M{f(x - w / 2 + ic)} {f(y - h * .04)} V{f(y - h + tep * 1.3)} L{f(x)} {f(y - h + tep * .55)} L{f(x + w / 2 - ic)} {f(y - h + tep * 1.3)} V{f(y - h * .04)}" fill="none" stroke="{cz}" stroke-width="{f(w * .025)}" opacity=".75"/>')
        # örgü şeridi (kenar)
        for k in range(int(h / (w * .16))):
            yy = y - h * .06 - k * w * .16
            if yy < y - h + tep * 1.5:
                break
            o.append(f'<path d="M{f(x - w / 2 + ic * .3)} {f(yy)} l{f(ic * .4)} {f(-w * .08)} M{f(x + w / 2 - ic * .3)} {f(yy)} l{f(-ic * .4)} {f(-w * .08)}" stroke="{cz}" stroke-width="{f(w * .018)}" opacity=".6"/>')
        # niş (sivri kemer)
        nw = w * .26
        ny0, ny1 = y - h * .22, y - h * .62
        o.append(f'<path d="M{f(x - nw)} {f(ny0)} V{f(ny1)} Q{f(x - nw)} {f(ny1 - h * .1)} {f(x)} {f(ny1 - h * .14)} Q{f(x + nw)} {f(ny1 - h * .1)} {f(x + nw)} {f(ny1)} V{f(ny0)} Z" fill="{koyu(renk, .22)}" stroke="{cz}" stroke-width="{f(w * .02)}"/>')
        o.append(f'<path d="M{f(x - nw * .5)} {f(ny0)} V{f(ny1 + h * .02)} M{f(x + nw * .5)} {f(ny0)} V{f(ny1 + h * .02)}" stroke="{acik(renk, .15)}" stroke-width="{f(w * .02)}" opacity=".7"/>')
        # rozet
        ry = y - h * .76
        y8 = selcuklu_yildizi(x, ry, w * .15)
        o.append(f'<circle cx="{f(x)}" cy="{f(ry)}" r="{f(w * .19)}" fill="{koyu(renk, .12)}" stroke="{cz}" stroke-width="{f(w * .018)}"/>'
                 f'<path d="{cizgi_d(y8, True)}" fill="none" stroke="{acik(renk, .25)}" stroke-width="{f(w * .02)}"/>')
        # yatay oyma bantlar (yazısız geometrik)
        for k in range(3):
            yy = y - h * (.13 + k * .03)
            o.append(f'<path d="M{f(x - w * .32)} {f(yy)} H{f(x + w * .32)}" stroke="{cz}" stroke-width="{f(w * .014)}" stroke-dasharray="{f(w * .05)} {f(w * .03)}" opacity=".7"/>')
    if likan:
        for _ in range(int(w * h / 900) + 4):
            px = x + r.uniform(-.45, .45) * w
            py = y - r.uniform(.05, .95) * h
            o.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r.uniform(.4, 1.2) * w * .035)}" fill="{r.choice(["#E8C447", "#D8A23A", "#C7D17A"])}" opacity=".75"/>')
    o.append("</g>")
    return "".join(o)


# ------------------------------------------------------------------ Van Kalesi

def van_kalesi(s, x0, x1, y, h, tohum=4, tas="#CDB894", golge="#8C7A60", sur="#D9C7A2", isik=-1, ayrinti=1.0, bayrak=False):
    """Uzun kalker kaya (Van Kayası) + kaya üstünde sur, mazgallar, burçlar, kayaya oyulmuş merdiven."""
    r = RNG(tohum)
    w = x1 - x0
    # kaya üst profili: doğuya (sağa) hafif yükselen, kırıklı sırt
    n = 40
    ust = []
    for i in range(n + 1):
        t = i / n
        yy = y - h * (.55 + .25 * math.sin(math.pi * min(1, t * 1.15)) + .06 * math.sin(t * 17 + 1))
        if t < .06:
            yy = y - h * (.15 + t / .06 * .45)
        if t > .95:
            yy = y - h * (.6 * (1 - (t - .95) / .05) + .12)
        ust.append((x0 + w * t, yy + r.uniform(-h * .012, h * .012)))
    kaya = [(x0 - w * .02, y)] + ust + [(x1 + w * .02, y)]
    g = s.lin([(0, acik(tas, .1)), (.6, tas), (1, koyu(tas, .15))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="vk")
    o = [f'<path d="{cizgi_d(kaya, True)}" fill="{g}"/>']
    # dikey kaya katmanları ve gölge yarıkları
    for i in range(int(w / (h * .12))):
        px = x0 + r.uniform(.03, .97) * w
        j = min(n, max(0, int((px - x0) / w * n)))
        top = ust[j][1]
        boy = (y - top) * r.uniform(.35, .95)
        gen = h * r.uniform(.01, .035)
        o.append(f'<path d="M{f(px)} {f(top + h * .03)} l{f(gen)} {f(boy * .5)} l{f(-gen * .6)} {f(boy * .5)} l{f(-gen)} 0 Z" fill="{golge}" opacity="{f(r.uniform(.35, .7), 2)}"/>')
    # alt kısım gölge
    o.append(f'<path d="M{f(x0)} {f(y - h * .12)} Q{f(x0 + w * .5)} {f(y - h * .2)} {f(x1)} {f(y - h * .1)} L{f(x1)} {f(y)} L{f(x0)} {f(y)} Z" fill="{golge}" opacity=".35"/>')
    # oyma nişler (kaya mezarları izlenimi)
    for k in range(int(3 * ayrinti)):
        px = x0 + w * (.35 + .12 * k)
        j = int((px - x0) / w * n)
        py = ust[j][1] + h * .28
        o.append(f'<path d="M{f(px)} {f(py)} h{f(h * .07)} v{f(h * .1)} h{f(-h * .07)} Z" fill="{koyu(tas, .45)}"/>')
    # merdiven (zikzak)
    mx = x0 + w * .16
    yol = [(mx, y - h * .05), (mx + w * .06, y - h * .2), (mx + w * .015, y - h * .32), (mx + w * .07, y - h * .47)]
    o.append(f'<path d="{cizgi_d(yol)}" fill="none" stroke="{acik(tas, .35)}" stroke-width="{f(h * .035)}" stroke-linejoin="round"/>')
    o.append(f'<path d="{cizgi_d(yol)}" fill="none" stroke="{koyu(tas, .3)}" stroke-width="{f(h * .012)}" stroke-dasharray="{f(h * .012)} {f(h * .012)}"/>')
    # sur: üst profilin üstünde duvar bandı + mazgallar
    sh = h * .14
    duvar_ust = [(p[0], p[1] - sh) for p in ust[2:-2]]
    duvar = ust[2:-2] + list(reversed(duvar_ust))
    gs = s.lin([(0, acik(sur, .15)), (1, koyu(sur, .1))], 0, y - h * 1.2, 0, y - h * .4, kull="userSpaceOnUse", ad="vs")
    o.append(f'<path d="{cizgi_d(duvar, True)}" fill="{gs}" stroke="{koyu(sur, .45)}" stroke-width="{f(h * .006)}"/>')
    # taş sıraları
    for k in range(1, 3):
        hat = [(p[0], p[1] - sh * k / 3) for p in ust[2:-2]]
        o.append(f'<path d="{cizgi_d(hat)}" fill="none" stroke="{koyu(sur, .25)}" stroke-width="{f(h * .004)}" opacity=".6"/>')
    # mazgallar (diş)
    mz = h * .045
    xx = ust[2][0]
    while xx < ust[-3][0]:
        j = (xx - x0) / w * n
        j0 = int(j)
        t = j - j0
        yy = ust[j0][1] * (1 - t) + ust[min(n, j0 + 1)][1] * t - sh
        o.append(f'<rect x="{f(xx)}" y="{f(yy - mz)}" width="{f(mz * .9)}" height="{f(mz + 1)}" fill="{sur}" stroke="{koyu(sur, .45)}" stroke-width="{f(h * .005)}"/>')
        xx += mz * 1.7
    # burçlar
    for t in (.12, .3, .52, .74, .9):
        j = int(t * n)
        bx, by = x0 + w * t, ust[j][1]
        bw, bh = h * .13, sh + h * .12
        o.append(f'<rect x="{f(bx - bw / 2)}" y="{f(by - bh)}" width="{f(bw)}" height="{f(bh)}" fill="{sur}" stroke="{koyu(sur, .45)}" stroke-width="{f(h * .006)}"/>')
        o.append(f'<rect x="{f(bx + (0 if isik < 0 else -bw / 2))}" y="{f(by - bh)}" width="{f(bw / 2)}" height="{f(bh)}" fill="#000" opacity=".13"/>')
        for k in range(3):
            o.append(f'<rect x="{f(bx - bw / 2 + k * bw * .4)}" y="{f(by - bh - mz)}" width="{f(bw * .2)}" height="{f(mz + 1)}" fill="{sur}" stroke="{koyu(sur, .45)}" stroke-width="{f(h * .005)}"/>')
        o.append(f'<path d="M{f(bx - bw * .12)} {f(by - bh * .45)} v{f(-bh * .22)} q{f(bw * .12)} {f(-bh * .1)} {f(bw * .24)} 0 v{f(bh * .22)} Z" fill="{koyu(sur, .55)}"/>')
    if bayrak:
        j = int(.52 * n)
        bx, by = x0 + w * .52, ust[j][1] - sh - h * .12 - mz
        from .karakter import turk_bayragi
        o.append(f'<path d="M{f(bx)} {f(by)} v{f(-h * .32)}" stroke="#5A4A3A" stroke-width="{f(h * .012)}"/>')
        o.append(turk_bayragi(bx, by - h * .32, h * .14, h * .02))
    return "".join(o), ust


def kucuk_kale(s, x, y, w, h, tohum=2, tas="#C2A27C", isik=-1):
    """Kıyı kayalığında küçük kale (Adilcevaz kalesi esinli): yuvarlak burçlar + sur."""
    r = RNG(tohum)
    o = []
    kaya = [(x - w * .6, y)] + [(x - w * .6 + w * 1.2 * i / 10, y - h * .35 * math.sin(math.pi * i / 10) ** .7 - r.uniform(0, h * .05)) for i in range(11)] + [(x + w * .6, y)]
    o.append(f'<path d="{cizgi_d(kaya, True)}" fill="{koyu(tas, .25)}"/>')
    o.append(f'<path d="{cizgi_d(kaya[:7] + [(x, y)], True)}" fill="{koyu(tas, .1)}" opacity=".7"/>')
    yt = y - h * .33
    o.append(f'<rect x="{f(x - w * .42)}" y="{f(yt - h * .3)}" width="{f(w * .84)}" height="{f(h * .3)}" fill="{tas}" stroke="{koyu(tas, .45)}" stroke-width="{f(h * .01)}"/>')
    for k in range(9):
        o.append(f'<rect x="{f(x - w * .42 + k * w * .1)}" y="{f(yt - h * .36)}" width="{f(w * .05)}" height="{f(h * .07)}" fill="{tas}" stroke="{koyu(tas, .45)}" stroke-width="{f(h * .008)}"/>')
    for bx in (x - w * .42, x + w * .42, x - w * .05):
        bw = w * .16
        bh = h * (.58 if bx != x - w * .05 else .75)
        g = s.lin([(0, acik(tas, .2)), (.5, tas), (1, koyu(tas, .3))], 0, 0, 1, 0, ad="kk")
        o.append(f'<rect x="{f(bx - bw / 2)}" y="{f(yt - bh)}" width="{f(bw)}" height="{f(bh)}" rx="{f(bw * .1)}" fill="{g}" stroke="{koyu(tas, .45)}" stroke-width="{f(h * .01)}"/>')
        for k in range(3):
            o.append(f'<rect x="{f(bx - bw / 2 + k * bw * .4)}" y="{f(yt - bh - h * .06)}" width="{f(bw * .2)}" height="{f(h * .07)}" fill="{tas}" stroke="{koyu(tas, .45)}" stroke-width="{f(h * .008)}"/>')
        o.append(f'<rect x="{f(bx - bw * .1)}" y="{f(yt - bh * .6)}" width="{f(bw * .2)}" height="{f(bh * .16)}" rx="{f(bw * .1)}" fill="{koyu(tas, .6)}"/>')
    return "".join(o)


# ------------------------------------------------------------------ iskele, fener

def iskele(s, x0, x1, y, kal, tohum=1, ahsap="#9A6B42", cizgi=None, merdiven=True, direk_n=None):
    r = RNG(tohum)
    cz = cizgi or koyu(ahsap, .5)
    o = []
    n = direk_n or max(3, int((x1 - x0) / (kal * 5)))
    for i in range(n + 1):
        px = x0 + (x1 - x0) * i / n
        o.append(f'<rect x="{f(px - kal * .18)}" y="{f(y)}" width="{f(kal * .36)}" height="{f(kal * 2.6)}" fill="{koyu(ahsap, .3)}"/>')
    o.append(f'<rect x="{f(x0)}" y="{f(y - kal * .35)}" width="{f(x1 - x0)}" height="{f(kal * .7)}" fill="{ahsap}" stroke="{cz}" stroke-width="{f(kal * .06)}"/>')
    for i in range(int((x1 - x0) / (kal * .9))):
        px = x0 + i * kal * .9
        o.append(f'<path d="M{f(px)} {f(y - kal * .35)} v{f(kal * .7)}" stroke="{cz}" stroke-width="{f(kal * .04)}" opacity=".6"/>')
    # korkuluk
    o.append(f'<path d="M{f(x0)} {f(y - kal * 1.5)} H{f(x1)}" stroke="{acik(ahsap, .15)}" stroke-width="{f(kal * .14)}"/>')
    for i in range(n + 1):
        px = x0 + (x1 - x0) * i / n
        o.append(f'<path d="M{f(px)} {f(y - kal * .35)} V{f(y - kal * 1.6)}" stroke="{koyu(ahsap, .2)}" stroke-width="{f(kal * .16)}"/>')
    if merdiven:
        for k in range(5):
            o.append(f'<rect x="{f(x1 + k * kal * .32)}" y="{f(y - kal * .35 + k * kal * .42)}" width="{f(kal * .7)}" height="{f(kal * .22)}" fill="{ahsap}" stroke="{cz}" stroke-width="{f(kal * .04)}"/>')
    return "".join(o)


def fener(s, x, y, h, govde="#FFFFFF", serit="#C8442F", isik_renk="#FFE08A", isik=True):
    w = h * .22
    o = []
    if isik:
        gl = s.rad([(0, isik_renk, .8), (.4, isik_renk, .25), (1, isik_renk, 0)], x, y - h * .9, h * .7, kull="userSpaceOnUse", ad="fn")
        o.append(f'<circle cx="{f(x)}" cy="{f(y - h * .9)}" r="{f(h * .7)}" fill="{gl}"/>')
    o.append(f'<path d="M{f(x - w)} {f(y)} L{f(x - w * .6)} {f(y - h * .78)} L{f(x + w * .6)} {f(y - h * .78)} L{f(x + w)} {f(y)} Z" fill="{govde}" stroke="{OBS}" stroke-width="{f(h * .02)}"/>')
    for k in range(3):
        yy = y - h * (.12 + k * .24)
        t = (y - yy) / (h * .78)
        ww = w * (1 - .4 * t)
        o.append(f'<path d="M{f(x - ww)} {f(yy)} L{f(x - ww * .94)} {f(yy - h * .1)} L{f(x + ww * .94)} {f(yy - h * .1)} L{f(x + ww)} {f(yy)} Z" fill="{serit}"/>')
    o.append(f'<rect x="{f(x - w * .5)}" y="{f(y - h * .95)}" width="{f(w)}" height="{f(h * .17)}" fill="{isik_renk}" stroke="{OBS}" stroke-width="{f(h * .02)}"/>'
             f'<path d="M{f(x - w * .7)} {f(y - h * .95)} L{f(x)} {f(y - h * 1.08)} L{f(x + w * .7)} {f(y - h * .95)} Z" fill="{serit}" stroke="{OBS}" stroke-width="{f(h * .02)}"/>'
             f'<rect x="{f(x - w * .75)}" y="{f(y - h * .8)}" width="{f(w * 1.5)}" height="{f(h * .04)}" fill="{OBS}"/>')
    return "".join(o)


# ------------------------------------------------------------------ şelale, köprü

def selale(s, x, y_ust, y_alt, w, tohum=3, kaya="#2F3340", su="#DDF4F6"):
    """Geniş perde şelale (Muradiye/Bendimahi esinli): koyu bazalt dudak, beyaz-mavi su perdesi,
    dikey akış çizgileri, iki yanda iri kayalar, dipte köpük ve sis."""
    r = RNG(tohum)
    o = []
    kh = y_alt - y_ust
    # su perdesi (hafif kavisli, aşağıda genişler)
    g = s.lin([(0, "#FFFFFF"), (.35, su), (.8, "#A9DDE4"), (1, "#E9F8FA")], 0, y_ust, 0, y_alt, kull="userSpaceOnUse", ad="sl")
    sol0, sag0 = x - w * .42, x + w * .42
    sol1, sag1 = x - w * .5, x + w * .5
    o.append(f'<path d="M{f(sol0)} {f(y_ust)} Q{f(x)} {f(y_ust + 8)} {f(sag0)} {f(y_ust)} L{f(sag1)} {f(y_alt)} L{f(sol1)} {f(y_alt)} Z" fill="{g}"/>')
    # akış çizgileri
    for k in range(int(w / 6)):
        t = r.random()
        xu = sol0 + (sag0 - sol0) * t
        xa = sol1 + (sag1 - sol1) * t
        yb = y_ust + r.uniform(.02, .5) * kh
        ys = yb + r.uniform(.2, .5) * kh
        xb = xu + (xa - xu) * (yb - y_ust) / kh
        xs = xu + (xa - xu) * (ys - y_ust) / kh
        o.append(f'<path d="M{f(xb)} {f(yb)} L{f(xs)} {f(ys)}" stroke="{r.choice(["#7FC8D2", "#B9E6EC", "#5FB3C2"])}" stroke-width="{f(r.uniform(1, 2.6))}" stroke-linecap="round" opacity="{f(r.uniform(.45, .9), 2)}"/>')
    # dudak (üst kenar) ve yan kayalar
    o.append(f'<path d="M{f(sol0 - w * .12)} {f(y_ust + 4)} Q{f(x)} {f(y_ust - 10)} {f(sag0 + w * .12)} {f(y_ust + 4)} L{f(sag0 + w * .1)} {f(y_ust + 14)} Q{f(x)} {f(y_ust + 2)} {f(sol0 - w * .1)} {f(y_ust + 14)} Z" fill="{koyu(kaya, .2)}"/>')
    o.append(f'<path d="M{f(sol0 - w * .02)} {f(y_ust + 6)} Q{f(x)} {f(y_ust + 14)} {f(sag0 + w * .02)} {f(y_ust + 6)}" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".9"/>')
    for sx in (-1, 1):
        for k in range(3):
            bx = x + sx * (w * .5 + k * w * .09) + r.uniform(-8, 8)
            by = y_alt - k * kh * .22 - r.uniform(0, 12)
            bw, bh = w * r.uniform(.16, .24), kh * r.uniform(.28, .42)
            gk = s.lin([(0, karis(kaya, "#6A7080", .5)), (1, koyu(kaya, .25))], 0, 0, 1, 1, ad="sk")
            o.append(f'<path d="M{f(bx - bw / 2)} {f(by)} C{f(bx - bw / 2)} {f(by - bh * .8)} {f(bx - bw * .1)} {f(by - bh)} {f(bx + bw * .2)} {f(by - bh * .9)} '
                     f'C{f(bx + bw * .5)} {f(by - bh * .7)} {f(bx + bw * .55)} {f(by - bh * .2)} {f(bx + bw / 2)} {f(by)} Z" fill="{gk}" stroke="{koyu(kaya, .4)}" stroke-width="1.4"/>')
            o.append(f'<path d="M{f(bx - bw * .3)} {f(by - bh * .6)} q{f(bw * .2)} {f(-bh * .25)} {f(bw * .45)} {f(-bh * .22)}" stroke="#8C93A3" stroke-width="2" fill="none" opacity=".7"/>')
    # köpük ve sis
    for _ in range(22):
        cx = x + r.uniform(-.6, .6) * w
        o.append(f'<circle cx="{f(cx)}" cy="{f(y_alt + r.uniform(-8, 8))}" r="{f(r.uniform(7, 18))}" fill="#FFFFFF" opacity="{f(r.uniform(.65, .95), 2)}"/>')
    sis = s.rad([(0, "#FFFFFF", .8), (1, "#FFFFFF", 0)], x, y_alt - 10, w * .95, kull="userSpaceOnUse", ad="ss")
    o.append(f'<ellipse cx="{f(x)}" cy="{f(y_alt - 10)}" rx="{f(w * .95)}" ry="{f(kh * .45)}" fill="{sis}"/>')
    return "".join(o)


def gokkusagi(s, cx, cy, R, kal, op=.55):
    renk = ["#E2533D", "#FF8A3D", "#F2C230", "#5FC08A", "#13A3A6", "#2B50B5", "#7B3F8C"]
    o = []
    for i, c in enumerate(renk):
        rr = R - i * kal
        o.append(f'<path d="M{f(cx - rr)} {f(cy)} A{f(rr)} {f(rr)} 0 0 1 {f(cx + rr)} {f(cy)}" fill="none" stroke="{c}" stroke-width="{f(kal + .6)}"/>')
    m = s.lin([(0, "#FFF", 0), (.35, "#FFF", 1), (.65, "#FFF", 1), (1, "#FFF", 0)], cx - R, 0, cx + R, 0, kull="userSpaceOnUse", ad="gkm")
    mk = s.maske(f'<rect x="{f(cx - R - 5)}" y="{f(cy - R - 5)}" width="{f(2 * R + 10)}" height="{f(R + 10)}" fill="{m}"/>', ad="gk")
    return f'<g mask="{mk}" opacity="{f(op, 2)}">{"".join(o)}</g>'


def asma_kopru(s, x0, x1, y, sarkma, direk_h, renk="#7A4E2E", halat="#3A2E26"):
    o = []
    for px in (x0, x1):
        o.append(f'<rect x="{f(px - 4)}" y="{f(y - direk_h)}" width="8" height="{f(direk_h + 6)}" fill="{renk}" stroke="{koyu(renk, .4)}" stroke-width="1.2"/>')
    mx = (x0 + x1) / 2
    o.append(f'<path d="M{f(x0)} {f(y - direk_h)} Q{f(mx)} {f(y - direk_h + sarkma * 2.2)} {f(x1)} {f(y - direk_h)}" fill="none" stroke="{halat}" stroke-width="2.4"/>')
    o.append(f'<path d="M{f(x0)} {f(y)} Q{f(mx)} {f(y + sarkma)} {f(x1)} {f(y)}" fill="none" stroke="{koyu(renk, .2)}" stroke-width="6"/>')
    n = int((x1 - x0) / 9)
    for i in range(1, n):
        t = i / n
        px = x0 + (x1 - x0) * t
        yd = y + sarkma * 4 * t * (1 - t)
        yu = y - direk_h + sarkma * 2.2 * 4 * t * (1 - t) / 2 + 0
        yu = (1 - t) ** 2 * (y - direk_h) + 2 * (1 - t) * t * (y - direk_h + sarkma * 2.2) + t * t * (y - direk_h)
        o.append(f'<path d="M{f(px)} {f(yu)} V{f(yd)}" stroke="{halat}" stroke-width="1.1" opacity=".8"/>')
    return "".join(o)


# ------------------------------------------------------------------ çay, semaver, çadır, koyun, obsidyen

def semaver(s, x, y, h, maden="#C9A86A", isik=-1):
    """Pirinç semaver: gövde, musluk, üstte demlik (kırmızı-beyaz)."""
    w = h * .42
    g = s.lin([(0, acik(maden, .5)), (.35, maden), (.7, koyu(maden, .25)), (1, acik(maden, .1))], 0, 0, 1, 0, ad="sm")
    cz = koyu(maden, .55)
    o = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .9)}" ry="{f(h * .03)}" fill="#1B1D26" opacity=".25"/>',
         f'<path d="M{f(x - w * .35)} {f(y)} L{f(x - w * .25)} {f(y - h * .1)} L{f(x + w * .25)} {f(y - h * .1)} L{f(x + w * .35)} {f(y)} Z" fill="{g}" stroke="{cz}" stroke-width="{f(h * .012)}"/>',
         f'<path d="M{f(x - w * .3)} {f(y - h * .1)} C{f(x - w * .62)} {f(y - h * .18)} {f(x - w * .6)} {f(y - h * .5)} {f(x - w * .4)} {f(y - h * .58)} L{f(x + w * .4)} {f(y - h * .58)} C{f(x + w * .6)} {f(y - h * .5)} {f(x + w * .62)} {f(y - h * .18)} {f(x + w * .3)} {f(y - h * .1)} Z" fill="{g}" stroke="{cz}" stroke-width="{f(h * .014)}"/>',
         f'<path d="M{f(x - w * .5)} {f(y - h * .4)} h{f(w)} M{f(x - w * .5)} {f(y - h * .25)} h{f(w)}" stroke="{cz}" stroke-width="{f(h * .01)}" opacity=".6"/>',
         f'<path d="M{f(x + w * .48)} {f(y - h * .24)} h{f(w * .25)} v{f(h * .05)}" fill="none" stroke="{cz}" stroke-width="{f(h * .028)}" stroke-linecap="round"/>',
         f'<path d="M{f(x - w * .55)} {f(y - h * .42)} q{f(-w * .2)} {f(h * .06)} 0 {f(h * .14)} M{f(x + w * .55)} {f(y - h * .42)} q{f(w * .2)} {f(h * .06)} 0 {f(h * .14)}" fill="none" stroke="{cz}" stroke-width="{f(h * .02)}"/>',
         f'<rect x="{f(x - w * .2)}" y="{f(y - h * .66)}" width="{f(w * .4)}" height="{f(h * .08)}" fill="{g}" stroke="{cz}" stroke-width="{f(h * .012)}"/>']
    # demlik
    o.append(f'<path d="M{f(x - w * .3)} {f(y - h * .66)} C{f(x - w * .42)} {f(y - h * .74)} {f(x - w * .36)} {f(y - h * .88)} {f(x - w * .2)} {f(y - h * .9)} L{f(x + w * .2)} {f(y - h * .9)} C{f(x + w * .36)} {f(y - h * .88)} {f(x + w * .42)} {f(y - h * .74)} {f(x + w * .3)} {f(y - h * .66)} Z" fill="#C8442F" stroke="{OBS}" stroke-width="{f(h * .012)}"/>'
             f'<path d="M{f(x - w * .22)} {f(y - h * .78)} q{f(w * .22)} {f(-h * .05)} {f(w * .44)} 0" fill="none" stroke="#FFFFFF" stroke-width="{f(h * .02)}" opacity=".8"/>'
             f'<ellipse cx="{f(x)}" cy="{f(y - h * .93)}" rx="{f(w * .1)}" ry="{f(h * .03)}" fill="#C8442F" stroke="{OBS}" stroke-width="{f(h * .01)}"/>'
             f'<path d="M{f(x + w * .3)} {f(y - h * .78)} l{f(w * .2)} {f(-h * .05)}" stroke="#C8442F" stroke-width="{f(h * .03)}" stroke-linecap="round"/>')
    # buhar
    o.append(f'<path d="M{f(x - w * .1)} {f(y - h * 1.0)} q{f(-w * .15)} {f(-h * .08)} 0 {f(-h * .16)} q{f(w * .15)} {f(-h * .08)} 0 {f(-h * .16)}" fill="none" stroke="#FFFFFF" stroke-width="{f(h * .025)}" stroke-linecap="round" opacity=".8"/>')
    return "".join(o)


def cay_bardak_kucuk(x, y, h, seviye=.8):
    w = h * .5
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .75)}" ry="{f(h * .08)}" fill="#F4F6F8" stroke="{OBS}" stroke-width="{f(h * .04)}"/>'
            f'<path d="M{f(x - w * .42)} {f(y - h)} C{f(x - w * .3)} {f(y - h * .7)} {f(x - w * .12)} {f(y - h * .6)} {f(x - w * .2)} {f(y - h * .35)} C{f(x - w * .3)} {f(y - h * .15)} {f(x - w * .25)} {f(y - h * .05)} {f(x - w * .2)} {f(y - h * .04)} '
            f'L{f(x + w * .2)} {f(y - h * .04)} C{f(x + w * .25)} {f(y - h * .05)} {f(x + w * .3)} {f(y - h * .15)} {f(x + w * .2)} {f(y - h * .35)} C{f(x + w * .12)} {f(y - h * .6)} {f(x + w * .3)} {f(y - h * .7)} {f(x + w * .42)} {f(y - h)} Z" fill="#C2401C" stroke="{OBS}" stroke-width="{f(h * .04)}"/>'
            f'<path d="M{f(x - w * .3)} {f(y - h * .92)} q{f(w * .05)} {f(h * .2)} {f(-w * .02)} {f(h * .35)}" stroke="#FFFFFF" stroke-width="{f(h * .05)}" fill="none" opacity=".7"/>')


def cadir(s, x, y, w, h, renk="#B23A2E", serit="#F5E8D0", isik=-1):
    o = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .65)}" ry="{f(h * .06)}" fill="#1B1D26" opacity=".2"/>',
         f'<path d="M{f(x - w / 2)} {f(y)} L{f(x)} {f(y - h)} L{f(x + w / 2)} {f(y)} Z" fill="{renk}"/>',
         f'<path d="M{f(x)} {f(y - h)} L{f(x + w / 2)} {f(y)} L{f(x + w * .1)} {f(y)} Z" fill="#000" opacity=".2"/>',
         f'<path d="M{f(x - w * .08)} {f(y)} L{f(x)} {f(y - h * .55)} L{f(x + w * .08)} {f(y)} Z" fill="#2A1A14"/>']
    for k in range(3):
        t = .3 + k * .22
        o.append(f'<path d="M{f(x - w / 2 * t)} {f(y - h * (1 - t))} L{f(x + w / 2 * t)} {f(y - h * (1 - t))}" stroke="{serit}" stroke-width="{f(h * .05)}"/>')
    return "".join(o)


def koyun(x, y, o=1.0, yon=1, yun="#F4F1EA", bas="#3A3330"):
    k = o
    yy = []
    for (dx, dy, r) in ((-8, -10, 7), (0, -12, 8), (8, -10, 7), (-4, -6, 7), (5, -6, 7)):
        yy.append(f'<circle cx="{f(x + dx * k * yon)}" cy="{f(y + dy * k)}" r="{f(r * k)}" fill="{yun}"/>')
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(12 * k)}" ry="{f(2 * k)}" fill="#1B1D26" opacity=".18"/>'
            f'<path d="M{f(x - 6 * k)} {f(y - 3 * k)} v{f(3 * k)} M{f(x + 6 * k)} {f(y - 3 * k)} v{f(3 * k)}" stroke="{bas}" stroke-width="{f(2 * k)}"/>'
            + "".join(yy) +
            f'<ellipse cx="{f(x + 13 * k * yon)}" cy="{f(y - 11 * k)}" rx="{f(4.2 * k)}" ry="{f(5.2 * k)}" fill="{bas}"/>'
            f'<ellipse cx="{f(x + 10 * k * yon)}" cy="{f(y - 13 * k)}" rx="{f(3 * k)}" ry="{f(1.4 * k)}" fill="{bas}"/>')


def obsidyen(s, x, y, w, h, tohum=5):
    """Nemrut obsidyeni: siyah volkanik cam parçaları, keskin kenar, mavi-mor yansıma."""
    r = RNG(tohum)
    o = []
    for k in range(4):
        cx = x + r.uniform(-.4, .4) * w
        bw = w * r.uniform(.25, .45)
        bh = h * r.uniform(.5, 1)
        pts = [(cx - bw / 2, y), (cx - bw * .4, y - bh * .6), (cx - bw * .05, y - bh), (cx + bw * .45, y - bh * .5), (cx + bw / 2, y)]
        g = s.lin([(0, "#3B3F5C"), (.45, "#12131C"), (1, "#05060A")], 0, 0, 1, 1, ad="ob")
        o.append(f'<path d="{cizgi_d(pts, True)}" fill="{g}" stroke="#000" stroke-width=".8"/>')
        o.append(f'<path d="M{nok(pts[1])} L{nok(pts[2])} L{f(cx + bw * .05)} {f(y - bh * .45)} Z" fill="#7C86C8" opacity=".45"/>')
        o.append(f'<path d="M{f(cx - bw * .3)} {f(y - bh * .5)} L{f(cx - bw * .1)} {f(y - bh * .85)}" stroke="#FFFFFF" stroke-width="1.2" opacity=".8"/>')
    return "".join(o)


# ------------------------------------------------------------------ el-Hâzinî'nin terazisi (Mîzânü'l-Hikme)

def hazini_terazisi(s, x, y, h, maden="#C9A86A", cizgi="#5A3E1B"):
    """Uzun kollu, kefeleri asılı hassas terazi (temsilî çizim). (x, y): ayak tabanı ortası."""
    g = s.lin([(0, acik(maden, .55)), (.4, maden), (1, koyu(maden, .3))], 0, 0, 1, 0, ad="ht")
    gk = s.rad([(0, acik(maden, .6)), (.6, maden), (1, koyu(maden, .35))], .45, .35, .7, ad="hk")
    L = h * 1.05
    ty = y - h * .9
    o = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(h * .3)}" ry="{f(h * .035)}" fill="#1B1D26" opacity=".25"/>',
         f'<path d="M{f(x - h * .2)} {f(y)} L{f(x - h * .05)} {f(y - h * .08)} L{f(x + h * .05)} {f(y - h * .08)} L{f(x + h * .2)} {f(y)} Z" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .012)}"/>',
         f'<rect x="{f(x - h * .022)}" y="{f(ty)}" width="{f(h * .044)}" height="{f(h * .82)}" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .01)}"/>',
         f'<path d="M{f(x - h * .07)} {f(ty - h * .02)} L{f(x)} {f(ty - h * .12)} L{f(x + h * .07)} {f(ty - h * .02)} Z" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .01)}"/>']
    # kol (ince uzun, üzerinde ölçek çentikleri)
    o.append(f'<rect x="{f(x - L)}" y="{f(ty - h * .015)}" width="{f(2 * L)}" height="{f(h * .03)}" rx="{f(h * .015)}" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .01)}"/>')
    for k in range(-10, 11):
        if k == 0:
            continue
        px = x + L * k / 10.5
        o.append(f'<path d="M{f(px)} {f(ty - h * .015)} v{f(h * (.022 if k % 5 else .04))}" stroke="{cizgi}" stroke-width="{f(h * .006)}"/>')
    # dil (ibre) ve sürgü ağırlık
    o.append(f'<path d="M{f(x)} {f(ty - h * .02)} L{f(x - h * .012)} {f(ty - h * .2)} L{f(x + h * .012)} {f(ty - h * .2)} Z" fill="{koyu(maden, .35)}"/>'
             f'<rect x="{f(x + L * .48)}" y="{f(ty + h * .015)}" width="{f(h * .05)}" height="{f(h * .07)}" rx="{f(h * .01)}" fill="{koyu(maden, .25)}" stroke="{cizgi}" stroke-width="{f(h * .008)}"/>'
             f'<path d="M{f(x + L * .48 + h * .025)} {f(ty)} v{f(h * .015)}" stroke="{cizgi}" stroke-width="{f(h * .008)}"/>')
    # kefeler
    for sx in (-1, 1):
        kx = x + sx * L * .92
        ky = ty + h * .45
        o.append(f'<path d="M{f(kx)} {f(ty)} L{f(kx - h * .12)} {f(ky)} M{f(kx)} {f(ty)} L{f(kx + h * .12)} {f(ky)} M{f(kx)} {f(ty)} L{f(kx)} {f(ky)}" stroke="{cizgi}" stroke-width="{f(h * .007)}" opacity=".9"/>'
                 f'<path d="M{f(kx - h * .16)} {f(ky)} Q{f(kx)} {f(ky + h * .14)} {f(kx + h * .16)} {f(ky)} Z" fill="{gk}" stroke="{cizgi}" stroke-width="{f(h * .01)}"/>'
                 f'<ellipse cx="{f(kx)}" cy="{f(ky)}" rx="{f(h * .16)}" ry="{f(h * .025)}" fill="{acik(maden, .3)}" stroke="{cizgi}" stroke-width="{f(h * .008)}"/>')
    # süs: altın sekiz köşeli yıldız ayak üstünde
    y8 = selcuklu_yildizi(x, y - h * .32, h * .06)
    o.append(f'<path d="{cizgi_d(y8, True)}" fill="{ALTIN_A}" stroke="{cizgi}" stroke-width="{f(h * .008)}"/>')
    return "".join(o)


def basit_terazi(s, x, y, h, sol_ic="", sag_ic="", egim=0.0, maden="#B8C3CC", cizgi=OBS):
    """Okul terazisi (eşit kollu); kefelerin içine SVG içerik yerleştirilebilir. egim derece (sağ kefe aşağı +)."""
    L = h * .9
    ty = y - h * .85
    g = s.lin([(0, acik(maden, .5)), (.5, maden), (1, koyu(maden, .3))], 0, 0, 1, 0, ad="bt")
    o = [f'<path d="M{f(x - h * .28)} {f(y)} h{f(h * .56)} l{f(-h * .1)} {f(-h * .07)} h{f(-h * .36)} Z" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .012)}"/>',
         f'<rect x="{f(x - h * .025)}" y="{f(ty)}" width="{f(h * .05)}" height="{f(h * .8)}" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .012)}"/>',
         f'<g transform="rotate({f(egim)} {f(x)} {f(ty)})">',
         f'<rect x="{f(x - L)}" y="{f(ty - h * .02)}" width="{f(2 * L)}" height="{f(h * .04)}" rx="{f(h * .02)}" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .012)}"/>']
    o.append("</g>")
    a = math.radians(egim)
    for sx, ic in ((-1, sol_ic), (1, sag_ic)):
        kx = x + sx * L * .95 * math.cos(a)
        kyy = ty + sx * L * .95 * math.sin(a)
        ky = kyy + h * .42
        o.append(f'<path d="M{f(kx)} {f(kyy)} L{f(kx - h * .2)} {f(ky)} M{f(kx)} {f(kyy)} L{f(kx + h * .2)} {f(ky)}" stroke="{cizgi}" stroke-width="{f(h * .01)}"/>'
                 f'<g transform="translate({f(kx)} {f(ky)})">{ic}</g>'
                 f'<path d="M{f(kx - h * .27)} {f(ky)} Q{f(kx)} {f(ky + h * .16)} {f(kx + h * .27)} {f(ky)} Z" fill="{g}" stroke="{cizgi}" stroke-width="{f(h * .012)}"/>')
    o.append(f'<circle cx="{f(x)}" cy="{f(ty)}" r="{f(h * .035)}" fill="{KEH}" stroke="{cizgi}" stroke-width="{f(h * .012)}"/>')
    return "".join(o)
