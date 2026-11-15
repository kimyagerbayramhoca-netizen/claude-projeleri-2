"""Atom ve Yapısı · Şanlıurfa–Harran Yolu · üniteye özel sahneler ve nişan ikonları.

kur_ortak bu modüle {{sahne|ad}} için ortak kütüphaneden (yerel-ortak/cizim) ÖNCE bakar. Bantlar 2100×H birim
(1 birim = 0,1 mm), sol üst ≈ %55 × %75 levhaya boş, odak sağda, tohumlar sabit. Işık: Mezopotamya'nın altın ışığı;
her sahnede ışık yönü tek (isik), bütün yapı çağrıları aynı yönle.
Çizimler TEMSİLÎDİR: yapıların bugünkü hâli (2023 depremleri sonrası) anlatılmaz; cami, kilise, manastır çizilmez.

Sayfa → sahne: 1 panorama_urfa · 2 gobeklitepe · 3 harran · 4 harran_hoyuk · 5 urfa_carsi · 6 halfeti · 7 firat ·
8 gumruk_hani (b40) · 9 sira_gecesi · 10 harran_ovasi · 11 urfa_evleri · 12 urfa_kalesi (b62) · 13 kale_kapi_urfa (b30) ·
14 ustad_bandi (ortak) · 15 harran_gece (b36) · 16 final_urfa (kur.py {{final}}).
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, selcuklu_yildizi, rng as RNG
from cizim import sahne as S
from cizim.sahneler import W, H, _bitir, _cerceve_golge
from cizim.renkler import ALTIN, OBS

# ------------------------------------------------------------------ bölge paleti
KERPIC, KERPIC_G, KERPIC_C = "#E6B077", "#BF8146", "#8E5730"        # Harran kerpici: ışık, gölge, sıra çizgisi
KALKER, KALKER_G, KALKER_K = "#EEDDB6", "#CDB283", "#9C8058"        # Urfa kalkeri (kesme taş)
BOZKIR, BOZKIR_K = "#E9C46F", "#B98A3E"                              # yaz bozkırı
BAKIR, BAKIR_K = "#E08A3C", "#9A4E1C"
FIRAT = dict(ufuk="#C9F1E6", orta="#22B2A6", derin="#08686E")

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    # Göbeklitepe T biçimli dikilitaş (kabartma kollar)
    "dikilitas": '<path d="M11 8 H37 V16 H29 V41 H19 V16 H11 Z"/><path d="M19 22 C22 26 26 26 29 22"/>'
                 '<path d="M21 31 h6"/><path d="M6 42 H42"/>',
    # Harran kümbet evi: kerpiç sıraları
    "kumbet": '<path d="M9 41 V31 C9 19 17 8 24 5 C31 8 39 19 39 31 V41 Z"/><path d="M10 31 H38 M12 24 H36 M16 17 H32 M20 11 H28"/>'
              '<path d="M20 41 V35 A4 4 0 0 1 28 35 V41"/>',
    # yıldız + çizgi spektrumu (Harran'ın gökbilimcileri)
    "yildiz": '<path d="M24 4 L27 13 L36 13 L29 19 L32 28 L24 22 L16 28 L19 19 L12 13 L21 13 Z"/>'
              '<rect x="6" y="34" width="36" height="9" rx="1.5"/><path d="M11 34 v9 M15 34 v9 M23 34 v9 M36 34 v9"/>',
    # sarraf: iki sikke, biri + biri −
    "sarraf": '<circle cx="17" cy="20" r="11"/><path d="M12 20 h10 M17 15 v10"/><circle cx="33" cy="31" r="10"/><path d="M28 31 h10"/>'
              '<path d="M27 9 Q36 9 38 17 M35 15 L38 18 L41 14"/>',
    # orbital kutuları: ↑↓ · ↑ · ↑
    "orbital": '<rect x="5" y="15" width="38" height="18"/><path d="M17.7 15 V33 M30.3 15 V33"/>'
               '<path d="M9 30 V19 M7 21.5 L9 18.5 L11 21.5 M14 18 V29 M12 26.5 L14 29.5 L16 26.5"/>'
               '<path d="M24 30 V19 M22 21.5 L24 18.5 L26 21.5"/><path d="M36.6 30 V19 M34.6 21.5 L36.6 18.5 L38.6 21.5"/>',
    # suya düşen damla ve halkalar (küresel simetri)
    "halka": '<path d="M24 4 C21 9 19 12 19 14.5 A5 5 0 0 0 29 14.5 C29 12 27 9 24 4 Z"/>'
             '<ellipse cx="24" cy="33" rx="19" ry="8"/><ellipse cx="24" cy="33" rx="12" ry="5"/><ellipse cx="24" cy="33" rx="5" ry="2.1"/>',
}


# ------------------------------------------------------------------ yardımcı parçalar

def _isinlar(s, gx, gy, n=12, uz=2400, op=.08, renk="#FFF0D0", a0=math.pi + .12, a1=2 * math.pi - .12):
    out = []
    for k in range(n):
        a = a0 + k * (a1 - a0) / n
        b = a + (a1 - a0) / n * .45
        out.append(f'<path d="M{f(gx)} {f(gy)} L{f(gx + uz * math.cos(a))} {f(gy + uz * math.sin(a))} L{f(gx + uz * math.cos(b))} {f(gy + uz * math.sin(b))} Z" fill="{renk}" opacity="{f(op, 2)}"/>')
    return "".join(out)


def _use(sembol, x, y, w, h, ayna=False):
    """Karakter sembolü (sayfanın {{defs}}'inden). ayna=True → sağa bakar."""
    if ayna:
        return f'<g transform="translate({f(x + w)} {f(y)}) scale(-1 1)"><use href="#{sembol}" x="0" y="0" width="{f(w)}" height="{f(h)}"/></g>'
    return f'<use href="#{sembol}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"/>'


def harran_evi(s, x, y, w, h, tohum, isik=1, renk=KERPIC, golge=KERPIC_G, kapi=True, badana=False, kapi_renk=None):
    """Harran'ın kovan biçimli kerpiç kubbeli evi: alçak kare gövde + konik kubbe, kerpiç sıraları, tepede baca deliği."""
    r = RNG(tohum)
    if badana:
        renk, golge = "#F4E8D2", "#C9B396"
    gh = h * .3
    yb, yt = y - gh, y - h
    kh = yb - yt
    out = []
    gg = s.lin([(0, acik(renk, .1)), (1, koyu(renk, .1))], 0, yb, 0, y, kull="userSpaceOnUse", ad="hg")
    out.append(f'<rect x="{f(x)}" y="{f(yb - 1)}" width="{f(w)}" height="{f(gh + 1)}" fill="{gg}"/>')
    sx = x if isik > 0 else x + w * .5
    out.append(f'<rect x="{f(sx)}" y="{f(yb - 1)}" width="{f(w * .5)}" height="{f(gh + 1)}" fill="#3A1E0A" opacity=".13"/>')
    egik = r.uniform(-.03, .03) * w
    d = (f"M{f(x + w * .03)} {f(yb)} C{f(x + w * .01)} {f(yb - kh * .58)} {f(x + w * .3 + egik)} {f(yt + kh * .05)} {f(x + w / 2 + egik)} {f(yt)} "
         f"C{f(x + w * .7 + egik)} {f(yt + kh * .05)} {f(x + w * .99)} {f(yb - kh * .58)} {f(x + w * .97)} {f(yb)} Z")
    if isik > 0:
        dur = [(0, golge), (.42, renk), (.8, acik(renk, .28)), (1, acik(renk, .12))]
    else:
        dur = [(0, acik(renk, .12)), (.2, acik(renk, .28)), (.58, renk), (1, golge)]
    gk = s.lin(dur, x, 0, x + w, 0, kull="userSpaceOnUse", ad="hk")
    out.append(f'<path d="{d}" fill="{gk}"/>')
    kl = s.klip(f'<path d="{d}"/>', ad="hkl")
    cz = []
    n = 10
    for i in range(1, n):
        yy = yb - kh * i / n
        cz.append(f'M{f(x - 4)} {f(yy + 2.5)} Q{f(x + w / 2)} {f(yy - kh * .035)} {f(x + w + 4)} {f(yy + 2.5)}')
    out.append(f'<path clip-path="{kl}" d="{" ".join(cz)}" fill="none" stroke="{KERPIC_C}" stroke-width="{f(max(.8, w * .011), 2)}" opacity=".42"/>')
    # gövdede kerpiç dizisi
    bz = []
    for j in range(1, 3):
        yy = yb + gh * j / 3
        bz.append(f"M{f(x)} {f(yy)} H{f(x + w)}")
    out.append(f'<path d="{" ".join(bz)}" stroke="{KERPIC_C}" stroke-width="{f(max(.7, w * .008), 2)}" opacity=".3"/>')
    out.append(f'<ellipse cx="{f(x + w / 2 + egik)}" cy="{f(yt + kh * .07)}" rx="{f(w * .055)}" ry="{f(w * .025)}" fill="#3A2214" opacity=".8"/>')
    if kapi:
        kw = w * .26
        kx = x + w * .37
        kh2 = gh * .86
        kr = kapi_renk or "#4A2A16"
        out.append(f'<path d="M{f(kx)} {f(y)} V{f(y - kh2 + kw / 2)} A{f(kw / 2)} {f(kw / 2)} 0 0 1 {f(kx + kw)} {f(y - kh2 + kw / 2)} V{f(y)} Z" fill="{kr}"/>')
    return "".join(out)


def harran_kumesi(s, x0, y, olcek, tohum, isik=1, n=6, badana_oran=.25, kapi=True, aralik=.92, renk=KERPIC, golge=KERPIC_G, kapi_renk=None):
    """Birbirine bitişik kovan evler: arka sıra daha küçük ve soluk, ön sıra büyük. renk/golge: akşam ve gece tonları için."""
    r = RNG(tohum)
    out = []
    w = 118 * olcek
    for sira, (dy, k, op) in enumerate(((-34 * olcek, .74, .86), (0, 1.0, 1))):
        xx = x0 + (w * .45 if sira == 0 else 0)
        for i in range(n - sira):
            ww = w * k * r.uniform(.9, 1.08)
            hh = ww * r.uniform(1.18, 1.36)
            ev = harran_evi(s, xx, y + dy, ww, hh, tohum * 31 + sira * 7 + i, isik=isik, kapi=kapi and sira == 1 and r.random() < .7,
                            badana=r.random() < badana_oran, renk=renk, golge=golge, kapi_renk=kapi_renk)
            out.append(f'<g opacity="{op}">{ev}</g>' if op < 1 else ev)
            xx += ww * aralik
    return "".join(out)


def t_dikilitas(s, x, y, h, tohum, isik=-1, tas="#E3D2AC", golge="#B49B72", oyma=1, yazi_renk="#8E7552"):
    """Göbeklitepe'nin T biçimli dikilitaşı (temsilî): gövde + üstte başlık. oyma: 0 yok · 1 hayvan · 2 kollu (merkez taşı)."""
    r = RNG(tohum)
    w = h * .25
    bw, bh = h * .58, h * .2
    yt = y - h
    out = []
    gv = [(x - w * .5, y), (x - w * .44, yt + bh), (x + w * .44, yt + bh), (x + w * .5, y)]
    gg = s.lin([(0, acik(tas, .18)), (.6, tas), (1, golge)] if isik < 0 else [(0, golge), (.4, tas), (1, acik(tas, .18))],
               x - w * .5, 0, x + w * .5, 0, kull="userSpaceOnUse", ad="tg")
    out.append(f'<path d="{cizgi_d(gv, True)}" fill="{gg}"/>')
    bas = [(x - bw * .5, yt + bh), (x - bw * .48, yt + bh * .08), (x - bw * .42, yt), (x + bw * .44, yt), (x + bw * .5, yt + bh * .12), (x + bw * .5, yt + bh)]
    gb = s.lin([(0, acik(tas, .25)), (1, tas)], 0, yt, 0, yt + bh, kull="userSpaceOnUse", ad="tb")
    out.append(f'<path d="{cizgi_d(bas, True)}" fill="{gb}"/>')
    out.append(f'<path d="M{f(x - bw * .5)} {f(yt + bh)} H{f(x + bw * .5)} V{f(yt + bh * 1.12)} H{f(x - bw * .5)} Z" fill="{golge}" opacity=".7"/>')
    gx = x + (w * .1 if isik < 0 else -w * .5)
    out.append(f'<path d="M{f(gx)} {f(yt + bh)} L{f(gx + w * .4)} {f(yt + bh)} L{f(gx + w * .44)} {f(y)} L{f(gx + w * .02)} {f(y)} Z" fill="#3A2A12" opacity=".12"/>')
    k = max(1.2, h * .012)
    if oyma == 2:          # kabartma kollar, eller ve kemer (merkez taşları)
        out.append(f'<path d="M{f(x - w * .42)} {f(yt + bh * 1.4)} C{f(x - w * .48)} {f(y - h * .35)} {f(x - w * .2)} {f(y - h * .32)} {f(x - w * .02)} {f(y - h * .33)}" '
                   f'fill="none" stroke="{yazi_renk}" stroke-width="{f(k * 2.2)}" stroke-linecap="round"/>')
        out.append(f'<path d="M{f(x + w * .42)} {f(yt + bh * 1.4)} C{f(x + w * .48)} {f(y - h * .35)} {f(x + w * .2)} {f(y - h * .32)} {f(x + w * .02)} {f(y - h * .33)}" '
                   f'fill="none" stroke="{yazi_renk}" stroke-width="{f(k * 2.2)}" stroke-linecap="round"/>')
        for i in range(4):
            out.append(f'<path d="M{f(x - w * .1 + i * w * .06)} {f(y - h * .335)} v{f(h * .03)}" stroke="{yazi_renk}" stroke-width="{f(k)}" stroke-linecap="round"/>')
        out.append(f'<path d="M{f(x - w * .44)} {f(y - h * .27)} H{f(x + w * .44)} M{f(x - w * .44)} {f(y - h * .24)} H{f(x + w * .44)}" stroke="{yazi_renk}" stroke-width="{f(k)}"/>')
        out.append(f'<path d="M{f(x - w * .12)} {f(y - h * .24)} L{f(x)} {f(y - h * .12)} L{f(x + w * .12)} {f(y - h * .24)}" fill="none" stroke="{yazi_renk}" stroke-width="{f(k)}"/>')
    elif oyma == 1:        # hayvan kabartmaları: tilki ya da yaban domuzu silüeti + yılan dalgaları
        cx, cy, o = x, y - h * .56, w * .32
        if r.random() < .5:   # tilki
            out.append(f'<path d="M{f(cx - o)} {f(cy)} q{f(o * .3)} {f(-o * .5)} {f(o)} {f(-o * .35)} l{f(o * .5)} {f(-o * .35)} l{f(o * .05)} {f(o * .4)} '
                       f'l{f(o * .3)} {f(o * .15)} l{f(-o * .4)} {f(o * .25)} q{f(-o * .6)} {f(o * .35)} {f(-o * 1.4)} {f(o * .1)} z" fill="{yazi_renk}" opacity=".55"/>')
        else:                 # yaban domuzu
            out.append(f'<path d="M{f(cx - o)} {f(cy + o * .2)} q0 {f(-o * .7)} {f(o * .8)} {f(-o * .65)} q{f(o * .6)} 0 {f(o * .9)} {f(o * .35)} l{f(o * .3)} {f(o * .1)} '
                       f'l{f(-o * .25)} {f(o * .25)} h{f(-o * 1.75)} z" fill="{yazi_renk}" opacity=".55"/>')
        yy = y - h * .3
        out.append(f'<path d="M{f(x - w * .3)} {f(yy)} q{f(w * .1)} {f(-w * .1)} {f(w * .2)} 0 t{f(w * .2)} 0 t{f(w * .2)} 0" fill="none" stroke="{yazi_renk}" stroke-width="{f(k)}" opacity=".6"/>')
    return "".join(out)


def kayalik(s, x0, x1, y_ust, y_alt, tohum, renk=KALKER, golge=KALKER_G, katman=7, isik=1, sirt=None):
    """Kalker yar (Fırat kıyısı): tabaka çizgili, sırt kırıklı. sirt: [(x, y)…] verilirse o sırt kullanılır."""
    r = RNG(tohum)
    if sirt is None:
        n = 10
        sirt = [(x0 + (x1 - x0) * i / n, y_ust + r.uniform(-1, 1) * (y_alt - y_ust) * .12) for i in range(n + 1)]
    d = f"M{f(x0)} {f(y_alt)} L" + " L".join(nok(p) for p in sirt) + f" L{f(x1)} {f(y_alt)} Z"
    g = s.lin([(0, acik(renk, .15)), (1, karis(renk, golge, .6))], 0, y_ust, 0, y_alt, kull="userSpaceOnUse", ad="kyg")
    out = [f'<path d="{d}" fill="{g}"/>']
    kl = s.klip(f'<path d="{d}"/>', ad="kyk")
    cz = []
    for i in range(1, katman):
        yy = y_ust + (y_alt - y_ust) * i / katman + r.uniform(-4, 4)
        cz.append(f"M{f(x0)} {f(yy)} " + " ".join(f"L{f(x0 + (x1 - x0) * j / 8)} {f(yy + r.uniform(-5, 5))}" for j in range(1, 9)))
    out.append(f'<path clip-path="{kl}" d="{" ".join(cz)}" fill="none" stroke="{koyu(golge, .25)}" stroke-width="2.2" opacity=".45"/>')
    # dikey kırıklar ve gölge cepleri
    for i in range(int((x1 - x0) / 60)):
        xx = r.uniform(x0, x1)
        yy = r.uniform(y_ust + 10, y_alt - 20)
        out.append(f'<path clip-path="{kl}" d="M{f(xx)} {f(yy)} l{f(r.uniform(-8, 8))} {f(r.uniform(18, 46))}" stroke="{koyu(golge, .35)}" stroke-width="2" opacity=".4"/>')
        if r.random() < .5:
            out.append(f'<ellipse clip-path="{kl}" cx="{f(xx)}" cy="{f(yy + 8)}" rx="{f(r.uniform(6, 14))}" ry="{f(r.uniform(3, 6))}" fill="{koyu(golge, .4)}" opacity=".35"/>')
    return "".join(out)


def tas_ev(s, x, y, w, h, tohum, tas=KALKER, isik=1, kemer=True, pencere="#4A3A2C", cumba=False, merdiven=False):
    """Urfa/Halfeti kesme taş evi: düz dam, kemerli kapı ve pencereler, isteğe bağlı cumba ve dış merdiven."""
    r = RNG(tohum)
    out = []
    g = s.lin([(0, acik(tas, .12)), (1, koyu(tas, .08))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="te")
    out.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{g}"/>')
    out.append(f'<rect x="{f(x if isik > 0 else x + w * .62)}" y="{f(y - h)}" width="{f(w * .38)}" height="{f(h)}" fill="#3A2A12" opacity=".1"/>')
    out.append(f'<rect x="{f(x - w * .03)}" y="{f(y - h - h * .07)}" width="{f(w * 1.06)}" height="{f(h * .08)}" fill="{koyu(tas, .12)}"/>')
    # taş sıraları
    sz = " ".join(f"M{f(x)} {f(y - h * k / 6)} H{f(x + w)}" for k in range(1, 6))
    out.append(f'<path d="{sz}" stroke="{koyu(tas, .3)}" stroke-width="{f(max(.6, w * .006), 2)}" opacity=".35"/>')
    n = max(1, int(w / 46))
    for i in range(n):
        px = x + w * (i + .5) / n - w * .07
        pw, ph = w * .14, h * .26
        py = y - h * .78
        if kemer:
            out.append(f'<path d="M{f(px)} {f(py + ph)} V{f(py + pw / 2)} A{f(pw / 2)} {f(pw / 2)} 0 0 1 {f(px + pw)} {f(py + pw / 2)} V{f(py + ph)} Z" fill="{pencere}"/>')
        else:
            out.append(f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" fill="{pencere}"/>')
    if r.random() < .8:
        kw = w * .18
        kx = x + w * (.18 + r.uniform(0, .5))
        out.append(f'<path d="M{f(kx)} {f(y)} V{f(y - h * .36)} A{f(kw / 2)} {f(kw / 2)} 0 0 1 {f(kx + kw)} {f(y - h * .36)} V{f(y)} Z" fill="#5A3A22"/>')
    if cumba:
        cx, cw = x + w * .55, w * .38
        cy = y - h * .62
        out.append(f'<rect x="{f(cx)}" y="{f(cy - h * .3)}" width="{f(cw)}" height="{f(h * .3)}" fill="{acik(tas, .08)}" stroke="{koyu(tas, .35)}" stroke-width="1.6"/>')
        out.append(f'<path d="M{f(cx)} {f(cy)} L{f(cx + cw * .12)} {f(cy + h * .1)} H{f(cx + cw * .88)} L{f(cx + cw)} {f(cy)} Z" fill="{koyu(tas, .2)}"/>')
        for j in range(3):
            out.append(f'<rect x="{f(cx + cw * (.1 + j * .3))}" y="{f(cy - h * .25)}" width="{f(cw * .2)}" height="{f(h * .17)}" fill="{pencere}"/>')
    if merdiven:   # sağ duvara yaslanıp dama çıkan dış taş merdiven (yandan, dolu taş gövde)
        n = 10
        L = w * .5
        pts = [(x + w, y), (x + w + L, y)]
        for j in range(n):
            y1 = y - (j + 1) * h / n
            pts += [(x + w + L - j * L / n, y1), (x + w + L - (j + 1) * L / n, y1)]
        pts.append((x + w, y - h))
        gm = s.lin([(0, acik(tas, .1)), (1, koyu(tas, .12))], x + w, 0, x + w + L, 0, kull="userSpaceOnUse", ad="mr")
        out.append(f'<path d="{cizgi_d(pts, True)}" fill="{gm}" stroke="{koyu(tas, .38)}" stroke-width="1.4" stroke-linejoin="round"/>')
        out.append(f'<path d="M{f(x + w + L)} {f(y - h / n - 14)} L{f(x + w)} {f(y - h - 14)}" stroke="#6B4A2E" stroke-width="4"/>')
        for j in range(0, n, 2):
            px = x + w + L - j * L / n
            out.append(f'<path d="M{f(px)} {f(y - (j + 1) * h / n)} V{f(y - (j + 1) * h / n - 14)}" stroke="#6B4A2E" stroke-width="3"/>')
    return "".join(out)


def kemer_dizisi(s, x0, y, n, ac, yuk, tohum, tas=KALKER, ic="#5A3E2A", ust=40, ayak=None, isik_ic=None):
    """Taş kemer dizisi (revak). ac: kemer açıklığı, yuk: ayak yüksekliği. isik_ic: kemer içine sıcak ışık rengi."""
    ayak = ayak or ac * .22
    toplam = n * (ac + ayak) + ayak
    out = []
    g = s.lin([(0, acik(tas, .1)), (1, koyu(tas, .1))], 0, y - yuk - ac / 2 - ust, 0, y, kull="userSpaceOnUse", ad="kd")
    out.append(f'<rect x="{f(x0)}" y="{f(y - yuk - ac / 2 - ust)}" width="{f(toplam)}" height="{f(yuk + ac / 2 + ust)}" fill="{g}"/>')
    for i in range(n):
        ax = x0 + ayak + i * (ac + ayak)
        d = f"M{f(ax)} {f(y)} V{f(y - yuk)} A{f(ac / 2)} {f(ac / 2)} 0 0 1 {f(ax + ac)} {f(y - yuk)} V{f(y)} Z"
        out.append(f'<path d="{d}" fill="{ic}"/>')
        if isik_ic:
            gi = s.rad([(0, isik_ic, .9), (1, isik_ic, 0)], ax + ac / 2, y - yuk * .5, ac * .9, kull="userSpaceOnUse", ad="ki")
            out.append(f'<path d="{d}" fill="{gi}"/>')
        # kemer taşı (voussoir) çizgileri
        for k in range(9):
            a = math.pi + k * math.pi / 8
            r1, r2 = ac / 2, ac / 2 + ac * .16
            cx, cy = ax + ac / 2, y - yuk
            out.append(f'<path d="M{f(cx + r1 * math.cos(a))} {f(cy + r1 * math.sin(a))} L{f(cx + r2 * math.cos(a))} {f(cy + r2 * math.sin(a))}" stroke="{koyu(tas, .32)}" stroke-width="1.6" opacity=".55"/>')
        out.append(f'<path d="M{f(ax - ac * .16)} {f(y - yuk)} A{f(ac * .66)} {f(ac * .66)} 0 0 1 {f(ax + ac * 1.16)} {f(y - yuk)}" fill="none" stroke="{koyu(tas, .3)}" stroke-width="1.8" opacity=".6"/>')
    out.append(f'<rect x="{f(x0 - 6)}" y="{f(y - yuk - ac / 2 - ust - 10)}" width="{f(toplam + 12)}" height="12" fill="{koyu(tas, .14)}"/>')
    return "".join(out)


def bakir_kap(s, x, y, w, tur="kazan", tohum=1):
    """Bakır kap (temsilî): kazan · tepsi · ibrik · cezve. Altın-turuncu parlak gradyan."""
    g = s.lin([(0, "#FFD7A0"), (.35, BAKIR), (.75, "#B5602A"), (1, BAKIR_K)], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="bk")
    out = []
    if tur == "kazan":
        h = w * .62
        out.append(f'<path d="M{f(x - w * .5)} {f(y - h)} H{f(x + w * .5)} C{f(x + w * .5)} {f(y - h * .2)} {f(x + w * .3)} {f(y)} {f(x)} {f(y)} C{f(x - w * .3)} {f(y)} {f(x - w * .5)} {f(y - h * .2)} {f(x - w * .5)} {f(y - h)} Z" fill="{g}" stroke="{BAKIR_K}" stroke-width="1.6"/>')
        out.append(f'<ellipse cx="{f(x)}" cy="{f(y - h)}" rx="{f(w * .5)}" ry="{f(w * .09)}" fill="#7A3A12" stroke="{BAKIR_K}" stroke-width="1.6"/>')
        out.append(f'<path d="M{f(x - w * .36)} {f(y - h * .55)} q{f(w * .1)} {f(h * .25)} {f(w * .24)} {f(h * .3)}" stroke="#FFE6C0" stroke-width="{f(w * .04)}" fill="none" opacity=".7" stroke-linecap="round"/>')
    elif tur == "tepsi":
        out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .5)}" ry="{f(w * .5)}" fill="{g}" stroke="{BAKIR_K}" stroke-width="1.6"/>')
        out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(w * .38)}" ry="{f(w * .38)}" fill="none" stroke="#FFE2B8" stroke-width="2" opacity=".7"/>')
        out.append(f'<path d="{cizgi_d(selcuklu_yildizi(x, y, w * .2), True)}" fill="none" stroke="{BAKIR_K}" stroke-width="1.4" opacity=".7"/>')
    elif tur == "ibrik":
        h = w * 1.3
        out.append(f'<path d="M{f(x - w * .12)} {f(y - h)} H{f(x + w * .12)} L{f(x + w * .16)} {f(y - h * .7)} C{f(x + w * .5)} {f(y - h * .55)} {f(x + w * .45)} {f(y)} {f(x)} {f(y)} '
                   f'C{f(x - w * .45)} {f(y)} {f(x - w * .5)} {f(y - h * .55)} {f(x - w * .16)} {f(y - h * .7)} Z" fill="{g}" stroke="{BAKIR_K}" stroke-width="1.6"/>')
        out.append(f'<path d="M{f(x + w * .4)} {f(y - h * .45)} q{f(w * .3)} {f(-h * .05)} {f(w * .42)} {f(-h * .45)}" stroke="{BAKIR}" stroke-width="{f(w * .07)}" fill="none" stroke-linecap="round"/>')
        out.append(f'<path d="M{f(x - w * .42)} {f(y - h * .6)} q{f(-w * .3)} {f(h * .15)} {f(-w * .1)} {f(h * .45)}" stroke="{BAKIR_K}" stroke-width="{f(w * .05)}" fill="none"/>')
    else:   # cezve
        h = w * .8
        out.append(f'<path d="M{f(x - w * .3)} {f(y - h)} H{f(x + w * .3)} L{f(x + w * .4)} {f(y)} H{f(x - w * .4)} Z" fill="{g}" stroke="{BAKIR_K}" stroke-width="1.6"/>')
        out.append(f'<path d="M{f(x + w * .3)} {f(y - h * .8)} H{f(x + w * .95)}" stroke="#6B4A2E" stroke-width="{f(w * .09)}" stroke-linecap="round"/>')
    return "".join(out)


def isot_cuvali(s, x, y, w, tohum, renk="#C8321E"):
    """Ağzı açık çuval, içinde tepeleme isot (kırmızı pul biber)."""
    r = RNG(tohum)
    h = w * .7
    g = s.lin([(0, "#E9D6A8"), (1, "#B99E6A")], x - w / 2, 0, x + w / 2, 0, kull="userSpaceOnUse", ad="cv")
    out = [f'<path d="M{f(x - w * .46)} {f(y)} C{f(x - w * .56)} {f(y - h * .5)} {f(x - w * .5)} {f(y - h)} {f(x - w * .42)} {f(y - h)} '
           f'H{f(x + w * .42)} C{f(x + w * .5)} {f(y - h)} {f(x + w * .56)} {f(y - h * .5)} {f(x + w * .46)} {f(y)} Z" fill="{g}" stroke="#7A6440" stroke-width="1.6"/>']
    gi = s.rad([(0, "#F0643C"), (.6, renk), (1, "#7E1A10")], x - w * .1, y - h - w * .12, w * .55, kull="userSpaceOnUse", ad="is")
    out.append(f'<path d="M{f(x - w * .44)} {f(y - h + 2)} Q{f(x - w * .2)} {f(y - h - w * .3)} {f(x)} {f(y - h - w * .32)} Q{f(x + w * .22)} {f(y - h - w * .3)} {f(x + w * .44)} {f(y - h + 2)} Z" fill="{gi}"/>')
    for _ in range(int(w / 3)):
        px = x + r.uniform(-w * .32, w * .32)
        py = y - h - r.uniform(0, w * .22)
        out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r.uniform(.8, 1.8))}" fill="{r.choice(["#FF7A4A", "#8E1C10", "#FFB08A"])}" opacity=".8"/>')
    out.append(f'<path d="M{f(x - w * .44)} {f(y - h + 3)} q{f(w * .44)} {f(w * .06)} {f(w * .88)} 0" stroke="#7A6440" stroke-width="2.2" fill="none"/>')
    return "".join(out)


def fener(s, x, y, boy, isik_renk="#FFD27A", zincir=60):
    """Asma fener (kandil biçimli); sıcak ışık halesi."""
    hl = s.rad([(0, isik_renk, .55), (.5, isik_renk, .15), (1, isik_renk, 0)], x, y, boy * 2.6, kull="userSpaceOnUse", ad="fh")
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(boy * 2.6)}" fill="{hl}"/>'
            f'<path d="M{f(x)} {f(y - boy * .6 - zincir)} V{f(y - boy * .6)}" stroke="#3A2A1A" stroke-width="2"/>'
            f'<path d="M{f(x - boy * .3)} {f(y - boy * .5)} H{f(x + boy * .3)} L{f(x + boy * .42)} {f(y + boy * .3)} L{f(x)} {f(y + boy * .62)} L{f(x - boy * .42)} {f(y + boy * .3)} Z" '
            f'fill="{isik_renk}" stroke="#5A3E1E" stroke-width="2"/>'
            f'<path d="M{f(x - boy * .22)} {f(y - boy * .62)} H{f(x + boy * .22)} L{f(x + boy * .3)} {f(y - boy * .5)} H{f(x - boy * .3)} Z" fill="#8A6212"/>'
            f'<path d="M{f(x)} {f(y - boy * .5)} V{f(y + boy * .55)} M{f(x - boy * .36)} {f(y + boy * .05)} H{f(x + boy * .36)}" stroke="#8A6212" stroke-width="1.4" opacity=".7"/>')


def pamuk_bitkisi(x, y, h, tohum, yaprak="#4E8A3A"):
    """Pamuk bitkisi: yeşil çalı, üstünde açılmış beyaz kozalar."""
    r = RNG(tohum)
    out = [f'<path d="M{f(x)} {f(y)} V{f(y - h * .7)}" stroke="#6B5A3A" stroke-width="{f(max(1, h * .04))}"/>']
    for _ in range(5):
        a = r.uniform(-2.6, -.5)
        L = h * r.uniform(.35, .55)
        ex, ey = x + L * math.cos(a), y - h * .25 + L * math.sin(a)
        out.append(f'<ellipse cx="{f(ex)}" cy="{f(ey)}" rx="{f(h * .2)}" ry="{f(h * .12)}" fill="{r.choice([yaprak, koyu(yaprak, .15), acik(yaprak, .15)])}" transform="rotate({f(math.degrees(a) + 90)} {f(ex)} {f(ey)})"/>')
    for _ in range(r.randint(3, 5)):
        px = x + r.uniform(-h * .38, h * .38)
        py = y - h * r.uniform(.45, .95)
        rr = h * r.uniform(.08, .12)
        out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(rr)}" fill="#FFFFFF"/><circle cx="{f(px + rr * .5)}" cy="{f(py - rr * .3)}" r="{f(rr * .7)}" fill="#F6F2EA"/>'
                   f'<path d="M{f(px - rr)} {f(py + rr * .6)} l{f(rr * .5)} {f(-rr * .4)} l{f(rr * .5)} {f(rr * .4)} l{f(rr * .5)} {f(-rr * .4)}" stroke="#7A5A34" stroke-width="1" fill="none"/>')
    return "".join(out)


def samanyolu(s, x0, y0, x1, y1, en, tohum, n=420):
    """Samanyolu: çapraz yumuşak ışık kuşağı + yoğun küçük yıldızlar."""
    r = RNG(tohum)
    a = math.atan2(y1 - y0, x1 - x0)
    L = math.hypot(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    g = s.rad([(0, "#C9C2F0", .42), (.45, "#8C86D6", .18), (1, "#6C6AC0", 0)], .5, .5, .5, ad="sy")
    out = [f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(L / 2)}" ry="{f(en)}" fill="{g}" transform="rotate({f(math.degrees(a))} {f(cx)} {f(cy)})"/>']
    g2 = s.rad([(0, "#FFF4E0", .35), (1, "#FFF4E0", 0)], .5, .5, .5, ad="sy2")
    out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(L * .32)}" ry="{f(en * .42)}" fill="{g2}" transform="rotate({f(math.degrees(a))} {f(cx)} {f(cy)})"/>')
    for _ in range(n):
        t = r.uniform(0, 1)
        d = r.gauss(0, en * .45)
        px = x0 + (x1 - x0) * t - d * math.sin(a)
        py = y0 + (y1 - y0) * t + d * math.cos(a)
        out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r.choice([.7, .9, 1.1, 1.4]))}" fill="#FFFFFF" opacity="{f(r.uniform(.35, .95), 2)}"/>')
    return "".join(out)


def usturlap(s, x, y, R, renk="#D9A93A", koyu_r="#6A4A10"):
    """Usturlap (temsilî): halkalı pirinç disk, örümcek (rete) ve askı."""
    g = s.rad([(0, "#FFE8A8"), (.55, renk), (1, "#8A6212")], x - R * .3, y - R * .3, R * 1.3, kull="userSpaceOnUse", ad="us")
    out = [f'<path d="M{f(x - R * .16)} {f(y - R * 1.02)} A{f(R * .2)} {f(R * .2)} 0 1 1 {f(x + R * .16)} {f(y - R * 1.02)}" fill="none" stroke="{koyu_r}" stroke-width="{f(R * .06)}"/>',
           f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R)}" fill="{g}" stroke="{koyu_r}" stroke-width="{f(R * .05)}"/>',
           f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R * .82)}" fill="none" stroke="{koyu_r}" stroke-width="{f(R * .025)}"/>']
    for k in range(24):
        a = k * math.pi / 12
        out.append(f'<path d="M{f(x + R * .82 * math.cos(a))} {f(y + R * .82 * math.sin(a))} L{f(x + R * .94 * math.cos(a))} {f(y + R * .94 * math.sin(a))}" stroke="{koyu_r}" stroke-width="{f(R * .02)}"/>')
    out.append(f'<circle cx="{f(x)}" cy="{f(y + R * .12)}" r="{f(R * .5)}" fill="none" stroke="{koyu_r}" stroke-width="{f(R * .035)}"/>')
    out.append(f'<path d="M{f(x - R * .8)} {f(y)} H{f(x + R * .8)} M{f(x)} {f(y - R * .8)} V{f(y + R * .8)}" stroke="{koyu_r}" stroke-width="{f(R * .025)}" opacity=".7"/>')
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5 + .3
        out.append(f'<path d="M{f(x)} {f(y)} Q{f(x + R * .5 * math.cos(a + .4))} {f(y + R * .5 * math.sin(a + .4))} {f(x + R * .72 * math.cos(a))} {f(y + R * .72 * math.sin(a))}" stroke="{koyu_r}" stroke-width="{f(R * .03)}" fill="none"/>'
                   f'<circle cx="{f(x + R * .72 * math.cos(a))}" cy="{f(y + R * .72 * math.sin(a))}" r="{f(R * .04)}" fill="{koyu_r}"/>')
    out.append(f'<path d="M{f(x - R * .75)} {f(y - R * .25)} L{f(x + R * .75)} {f(y + R * .25)}" stroke="{koyu_r}" stroke-width="{f(R * .07)}" stroke-linecap="round"/>')
    out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R * .07)}" fill="{koyu_r}"/>')
    return "".join(out)


def prizma(s, x, y, a, isik_x0, isik_y0):
    """Cam prizma + gelen beyaz ışık + çıkan gökkuşağı yelpazesi (sağa)."""
    p = [(x, y - a * .87), (x - a / 2, y), (x + a / 2, y)]
    g = s.lin([(0, "#FFFFFF", .85), (1, "#BFE6F0", .55)], x - a / 2, y - a, x + a / 2, y, kull="userSpaceOnUse", ad="pr")
    out = [f'<path d="M{f(isik_x0)} {f(isik_y0)} L{f(x - a * .2)} {f(y - a * .4)}" stroke="#FFF6DC" stroke-width="7" opacity=".9" stroke-linecap="round"/>']
    renkler = ["#E8282B", "#FF7A1A", "#FFD21A", "#2DBE4E", "#14B8E6", "#3D3BE8", "#7B2BD9"]
    for i, c in enumerate(renkler):
        a0 = -.18 + i * .05
        out.append(f'<path d="M{f(x + a * .18)} {f(y - a * .36)} L{f(x + a * 3.2)} {f(y - a * .36 + a * 3 * math.tan(a0))} L{f(x + a * 3.2)} {f(y - a * .36 + a * 3 * math.tan(a0 + .05))} Z" fill="{c}" opacity=".78"/>')
    out.append(f'<path d="{cizgi_d(p, True)}" fill="{g}" stroke="#5A7A86" stroke-width="2.4" stroke-linejoin="round"/>')
    return "".join(out)


def kale_tepesi(s, x0, x1, y_taban, y_tepe, tohum, isik=-1, tas=KALKER, sutun=True, sur=True, gece=False, olcek=1.0):
    """Urfa Kalesi (temsilî): dik yamaçlı kalker kaya kütlesi, sırtında burçlu sur ve iki yüksek sütun.
    Yapıların bugünkü hâli anlatılmaz; çizim temsilîdir."""
    r = RNG(tohum)
    out = []
    w = x1 - x0
    hh = y_taban - y_tepe
    # kaya kütlesi: dik yanlar, hafif dalgalı düz sırt
    pts = [(x0, y_taban), (x0 + w * .05, y_taban - hh * .18), (x0 + w * .1, y_taban - hh * .42), (x0 + w * .13, y_taban - hh * .7),
           (x0 + w * .17, y_tepe + hh * .12), (x0 + w * .2, y_tepe + hh * .04)]
    for i in range(1, 8):
        pts.append((x0 + w * (.2 + .64 * i / 8), y_tepe + r.uniform(-.02, .05) * hh))
    pts += [(x0 + w * .86, y_tepe + hh * .06), (x0 + w * .9, y_tepe + hh * .3), (x0 + w * .93, y_taban - hh * .38), (x0 + w * .97, y_taban - hh * .12), (x1, y_taban)]
    d = cizgi_d(pts, True)
    g = s.lin([(0, acik(tas, .08)), (.55, karis(tas, "#B08A5C", .45)), (1, karis(tas, "#7A5A3A", .6))], 0, y_tepe, 0, y_taban, kull="userSpaceOnUse", ad="kt")
    out.append(f'<path d="{d}" fill="{g}"/>')
    kl = s.klip(f'<path d="{d}"/>', ad="ktk")
    # kaya yüzleri: açık ve koyu çokgenler (doğal kırıklar)
    yuz = []
    for k in range(int(26 * max(.5, olcek))):
        cx = r.uniform(x0, x1)
        cy = r.uniform(y_tepe + hh * .1, y_taban)
        rr = r.uniform(18, 46) * max(.5, olcek)
        n = r.randint(4, 6)
        p = [(cx + rr * math.cos(a) * r.uniform(.6, 1.1), cy + rr * .6 * math.sin(a) * r.uniform(.6, 1.1)) for a in [j * 2 * math.pi / n + r.uniform(-.3, .3) for j in range(n)]]
        renk = r.choice([acik(tas, .18), koyu(tas, .12), koyu(tas, .22), karis(tas, "#C9A070", .4)])
        yuz.append(f'<path d="{cizgi_d(p, True)}" fill="{renk}" opacity=".55"/>')
    out.append(f'<g clip-path="{kl}">{"".join(yuz)}</g>')
    dur = [(0, "#3A2410", 0), (.45, "#3A2410", 0), (1, "#3A2410", .26)] if isik < 0 else [(0, "#3A2410", .26), (.55, "#3A2410", 0), (1, "#3A2410", 0)]
    gg0 = s.lin(dur, x0, 0, x1, 0, kull="userSpaceOnUse", ad="ktg")
    out.append(f'<path d="{d}" fill="{gg0}"/>')
    cz = []
    for i in range(7):
        yy = y_tepe + hh * (.18 + .12 * i)
        cz.append(f"M{f(x0)} {f(yy)} " + " ".join(f"L{f(x0 + w * j / 10)} {f(yy + r.uniform(-5, 5))}" for j in range(1, 11)))
    out.append(f'<path clip-path="{kl}" d="{" ".join(cz)}" fill="none" stroke="#6E5032" stroke-width="2" opacity=".3"/>')
    sy = y_tepe + hh * .03
    gs = s.lin([(0, acik(tas, .14)), (1, koyu(tas, .1))], 0, sy - 70 * olcek, 0, sy + 10, kull="userSpaceOnUse", ad="ks")
    if sutun:   # iki yüksek sütun (başlıklı), surun arkasında
        for sx in (x0 + w * .5, x0 + w * .58):
            sh = 210 * olcek
            sw = 13 * olcek
            gg = s.lin([(0, acik(tas, .3)), (.45, tas), (1, koyu(tas, .28))], sx - sw, 0, sx + sw, 0, kull="userSpaceOnUse", ad="su")
            out.append(f'<rect x="{f(sx - sw)}" y="{f(sy - sh)}" width="{f(sw * 2)}" height="{f(sh)}" fill="{gg}"/>')
            for j in range(1, 9):
                out.append(f'<path d="M{f(sx - sw)} {f(sy - sh * j / 9)} H{f(sx + sw)}" stroke="{koyu(tas, .32)}" stroke-width="1.1" opacity=".5"/>')
            out.append(f'<path d="M{f(sx - sw * 1.7)} {f(sy - sh)} L{f(sx - sw * 1.15)} {f(sy - sh - 20 * olcek)} H{f(sx + sw * 1.15)} L{f(sx + sw * 1.7)} {f(sy - sh)} Z" '
                       f'fill="{koyu(tas, .06)}" stroke="{koyu(tas, .35)}" stroke-width="1.3"/>')
            out.append(f'<rect x="{f(sx - sw * 1.9)}" y="{f(sy - sh - 28 * olcek)}" width="{f(sw * 3.8)}" height="{f(9 * olcek)}" fill="{koyu(tas, .12)}"/>')
    if sur:
        sx0, sx1 = x0 + w * .17, x0 + w * .88
        sh = 58 * olcek
        out.append(f'<rect x="{f(sx0)}" y="{f(sy - sh)}" width="{f(sx1 - sx0)}" height="{f(sh + 12)}" fill="{gs}"/>')
        mz = []
        x = sx0
        while x < sx1 - 12 * olcek:
            mz.append(f'<rect x="{f(x)}" y="{f(sy - sh - 13 * olcek)}" width="{f(13 * olcek)}" height="{f(14 * olcek)}" fill="{gs}"/>')
            x += 24 * olcek
        out.append("".join(mz))
        for bx in (sx0 - 8 * olcek, sx0 + (sx1 - sx0) * .3, sx0 + (sx1 - sx0) * .7, sx1 - 40 * olcek):
            bw, bh = 48 * olcek, 92 * olcek
            out.append(f'<rect x="{f(bx)}" y="{f(sy - bh)}" width="{f(bw)}" height="{f(bh + 12)}" fill="{gs}" stroke="{koyu(tas, .3)}" stroke-width="1.4"/>')
            for k in range(3):
                out.append(f'<rect x="{f(bx + k * bw / 3 + 2)}" y="{f(sy - bh - 12 * olcek)}" width="{f(bw / 3 - 5)}" height="{f(13 * olcek)}" fill="{gs}"/>')
            pen = "#FFD27A" if gece else "#4A3220"
            out.append(f'<rect x="{f(bx + bw * .42)}" y="{f(sy - bh * .66)}" width="{f(bw * .16)}" height="{f(bh * .22)}" fill="{pen}"/>')
        out.append(f'<path d="M{f(sx0)} {f(sy - sh * .45)} H{f(sx1)}" stroke="{koyu(tas, .3)}" stroke-width="1.3" opacity=".45"/>')
    return "".join(out)


def _bozkir(s, y, h, tohum, ust=BOZKIR, alt=BOZKIR_K, dalga=24):
    g = s.lin([(0, ust), (1, alt)], 0, y, 0, y + h, kull="userSpaceOnUse", ad="bz")
    r = RNG(tohum)
    pts = [(x, y + r.uniform(-dalga, dalga) * .4) for x in range(0, 2101, 150)]
    return f'<path d="{egri_d(pts)} L2100 {f(y + h + 400)} L0 {f(y + h + 400)} Z" fill="{g}"/>'


def _kuru_ot(x0, x1, y, tohum, n=None, renk=("#C99A48", "#E2BC6A", "#A97C34"), boy=16):
    r = RNG(tohum)
    out = []
    for _ in range(n or int((x1 - x0) / 5)):
        px = r.uniform(x0, x1)
        b = boy * r.uniform(.5, 1.3)
        e = r.uniform(-.5, .5) * b
        out.append(f'<path d="M{f(px)} {f(y)} q{f(e * .3)} {f(-b * .6)} {f(e)} {f(-b)}" stroke="{r.choice(renk)}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def _gelincik(x0, x1, y0, y1, n, tohum):
    r = RNG(tohum)
    return "".join(f'<circle cx="{f(r.uniform(x0, x1))}" cy="{f(r.uniform(y0, y1))}" r="{f(r.uniform(2, 3.6))}" fill="{r.choice(["#E2533D", "#F2C230", "#FFFFFF"])}"/>' for _ in range(n))


def _tahta_yol(x0, x1, y, en=16, renk="#9A6B42"):
    """Ahşap gezi yolu ve korkuluk (ören yeri)."""
    out = [f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1 - x0)}" height="{en}" fill="{renk}"/>',
           f'<path d="M{f(x0)} {f(y + 4)} H{f(x1)}" stroke="#C8955E" stroke-width="2"/>',
           f'<path d="M{f(x0)} {f(y - 34)} H{f(x1)}" stroke="#6B4A2E" stroke-width="4"/>']
    x = x0
    while x <= x1:
        out.append(f'<path d="M{f(x)} {f(y + en)} V{f(y - 36)}" stroke="#6B4A2E" stroke-width="4"/>')
        x += 46
    return "".join(out)


# ------------------------------------------------------------------ 1. DURAK · GÖBEKLİTEPE (şafak)

def gobeklitepe():
    s = Svg("ah-gob")
    ufuk = 268
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    s += _isinlar(s, 1840, ufuk - 30, 14, op=.07, renk="#FFE9C4")
    s += S.gunes(s, 1840, ufuk - 30, 44, cekirdek="#FFF9E8", hale="#FFC27A", hale_r=520, guc=.95)
    s += S.bulut_serit(s, 220, 170, 480, 10, "#FFE3EA", "#F6B8C8", .5)
    s += S.bulut_serit(s, 1080, 118, 420, 9, "#FFE8EE", "#F5BACB", .55)
    s += S.bulut(s, 1460, 96, 170, 9, ust="#FFFFFF", alt="#F9D3C4", op=.85)
    # uzak tepeler (Germuş sırtları) ve bozkır
    for i, (sol, sag, tx, ty, renk, golge) in enumerate(((-100, 900, 340, 186, "#B9A2CF", "#9884BC"), (700, 1600, 1150, 206, "#C3A6C6", "#A086B2"),
                                                         (1350, 2250, 1980, 176, "#B49CC9", "#937DB6"))):
        d, _ = S.dag(s, sol, sag, ufuk, tx, ty, 40 + i, renk=renk, golge=golge, bicim="tepe", sis="#F7D3D6", isik=1, sirt=2, puruz=6)
        s += d
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 22, 24, 44, "#E7C08A", "#D7A867", dalga=6)
    s += tb
    s += _bozkir(s, ufuk + 40, 120, 45, ust="#EBC371", alt="#C9953F")
    # kazı alanı: oval çukur ve taş duvar halkaları
    cx, cy, rx, ry = 1600, 372, 360, 74
    gc = s.lin([(0, "#B98F55"), (1, "#8E6A3C")], 0, cy - ry, 0, cy + ry, kull="userSpaceOnUse", ad="cuk")
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{gc}"/>'
    r = RNG(46)
    tas = []
    for halka in (1.0, .78):
        for k in range(70):
            a = k * 2 * math.pi / 70 + r.uniform(-.02, .02)
            px, py = cx + rx * halka * math.cos(a), cy + ry * halka * math.sin(a)
            tas.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(r.uniform(9, 15) * halka)}" ry="{f(r.uniform(5, 8) * halka)}" fill="{r.choice(["#D9C29A", "#C7AE84", "#E6D4B0"])}" stroke="#8E7552" stroke-width="1"/>')
    s += "".join(tas)
    # arka sıradaki dikilitaşlar (küçük, soluk)
    for k in range(9):
        a = math.pi + .25 + k * (math.pi - .5) / 8
        px, py = cx + rx * .86 * math.cos(a), cy + ry * .86 * math.sin(a)
        s += f'<g opacity=".88">{t_dikilitas(s, px, py + 6, 104, 50 + k, isik=1, oyma=1 if k % 2 else 0)}</g>'
    # iki büyük merkez taşı (kollu kabartma)
    s += t_dikilitas(s, cx - 66, cy + 30, 238, 61, isik=1, oyma=2)
    s += t_dikilitas(s, cx + 70, cy + 34, 250, 62, isik=1, oyma=2)
    # ön sıradaki dikilitaşlar
    for k, a in enumerate((.35, .7, 2.45, 2.8)):
        px, py = cx + rx * .9 * math.cos(a), cy + ry * .9 * math.sin(a)
        s += t_dikilitas(s, px, py + 16, 148, 70 + k, isik=1, oyma=1)
    # ahşap gezi yolu (önde) ve Pamuk
    s += _tahta_yol(1180, 2100, 432)
    s += _use("pamuk-selam", 1190, 330, 88, 100)
    s += _kuru_ot(0, 1180, 452, 47, boy=18)
    s += _gelincik(980, 1200, 420, 450, 18, 48)
    s += S.kaya(s, 1060, 446, 70, 30, 49, renk="#C9AE84", isik=1)
    s += S.marti(1220, 150, .7, 2, renk="#6A4A70")
    s += S.marti(1290, 176, .5, 1, renk="#6A4A70")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 2. DURAK · HARRAN KÜMBET EVLERİ (öğle)

def harran():
    s = Svg("ah-har")
    ufuk = 300
    gok = [(0, "#1F7FD6"), (.5, "#62B7EE"), (.85, "#CDEBF7"), (1, "#FCEBC8")]
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=gok)
    s += S.gunes(s, 1930, 70, 36, cekirdek="#FFFDF0", hale="#FFE6A0", hale_r=460, guc=.9)
    s += S.bulut(s, 1250, 110, 230, 21, ust="#FFFFFF", alt="#D6E8F5", op=.95)
    s += S.bulut(s, 760, 80, 180, 22, ust="#FFFFFF", alt="#D6E8F5", op=.8)
    s += S.bulut(s, 1660, 170, 150, 23, ust="#FFFFFF", alt="#E3EEF6", op=.9)
    # uzak düz ufuk: Harran Ovası, ılık pus
    s += f'<rect x="0" y="{ufuk - 8}" width="{W}" height="16" fill="#F3E2BE" opacity=".8"/>'
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 6, 10, 24, "#D9C08E", "#CBAE78", dalga=4)
    s += tb
    # tarlalar: altın buğday anızı ve yeşil pamuk şeritleri
    g = s.lin([(0, "#E9C46F"), (1, "#C98F3A")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="tar")
    s += f'<rect x="0" y="{ufuk + 8}" width="{W}" height="{H - ufuk}" fill="{g}"/>'
    for i in range(6):
        yy = ufuk + 14 + i * i * 4.2
        s += f'<path d="M0 {f(yy)} H{W}" stroke="{["#8FB45A", "#D9B060"][i % 2]}" stroke-width="{f(2 + i * 1.2)}" opacity=".7"/>'
    # uzakta küçük kovan ev kümeleri
    s += f'<g opacity=".75">{harran_kumesi(s, 900, ufuk + 12, .28, 25, n=5, kapi=False)}</g>'
    s += f'<g opacity=".85">{harran_kumesi(s, 1180, ufuk + 22, .4, 26, n=4, kapi=False)}</g>'
    # ön plan: büyük kovan ev kümesi (sağ)
    s += f'<rect x="1300" y="402" width="800" height="70" fill="#C9944E"/>'
    s += harran_kumesi(s, 1330, 412, 1.12, 27, n=6, badana_oran=.3)
    # avlu duvarı ve Pamuk
    s += f'<path d="M1240 452 V418 H1330 V452 Z" fill="{KERPIC}"/><path d="M1240 418 H1330" stroke="{KERPIC_C}" stroke-width="3"/>'
    s += _use("pamuk-otur", 1250, 336, 72, 82)
    # tandır dumanı, saman yığını, kuyu
    s += f'<ellipse cx="1150" cy="440" rx="60" ry="22" fill="#E6C27A"/><path d="M1095 440 Q1150 380 1205 440 Z" fill="#E9CB86"/>'
    for k in range(4):
        s += f'<circle cx="{1085 - k * 14}" cy="{408 - k * 22}" r="{14 + k * 5}" fill="#FFFFFF" opacity="{f(.5 - k * .1, 2)}"/>'
    s += _kuru_ot(0, 1240, 455, 28, boy=14, renk=("#B07E2C", "#E0B25A", "#8A6A2E"))
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 3. DURAK · HARRAN HÖYÜĞÜ (alacakaranlık, ilk yıldızlar)

def harran_hoyuk():
    s = Svg("ah-hoy")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "alaca")
    s += S.yildizlar(s, 0, 0, W, ufuk - 90, 130, 31)
    s += S.ay(s, 1520, 96, 22, golge_renk="#3A2E66")
    s += f'<circle cx="1700" cy="150" r="5" fill="#FFF6D8"/><circle cx="1700" cy="150" r="16" fill="#FFF6D8" opacity=".2"/>'
    gl = s.rad([(0, "#FFB070", .75), (.5, "#FF8A6A", .25), (1, "#FF8A6A", 0)], 1900, ufuk, 600, kull="userSpaceOnUse", ad="sf")
    s += f'<ellipse cx="1900" cy="{ufuk}" rx="900" ry="150" fill="{gl}"/>'
    # höyük silüeti ve ova
    hoy = [(900, ufuk + 8), (1120, ufuk - 26), (1400, ufuk - 46), (1700, ufuk - 40), (1950, ufuk - 14), (2100, ufuk + 4)]
    s += f'<path d="{egri_d(hoy)} L2100 {H} L900 {H} Z" fill="#4A3352"/>'
    g = s.lin([(0, "#5A3C5E"), (1, "#2C2140")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="ova")
    s += f'<path d="M0 {ufuk + 6} C600 {ufuk + 2} 1200 {ufuk + 18} 2100 {ufuk + 30} V{H} H0 Z" fill="{g}"/>'
    # höyüğün üstünde akşam tonunda kovan evler, kapılarında ışık
    s += harran_kumesi(s, 1240, ufuk - 14, .5, 32, n=6, kapi=True, badana_oran=0, renk="#9A6E72", golge="#5A3E58", kapi_renk="#FFC86A")
    # ön plan: taş seki, prizma (ışığın renklere ayrılması), ekranda renk şeridi, usturlap
    s += f'<path d="M1180 {H} L1200 400 Q1500 380 1800 392 L2100 386 V{H} Z" fill="#3C2A40"/>'
    s += f'<rect x="1430" y="368" width="150" height="36" rx="4" fill="#8E7A6A"/><rect x="1430" y="368" width="150" height="8" fill="#A99484"/>'
    s += prizma(s, 1500, 368, 64, 1180, 300)
    s += f'<rect x="1720" y="300" width="300" height="120" rx="6" fill="#F6F1E6" opacity=".92"/>'
    renkler = ["#7B2BD9", "#3D3BE8", "#14B8E6", "#2DBE4E", "#FFD21A", "#FF7A1A", "#E8282B"]
    for i, c in enumerate(renkler):
        s += f'<rect x="{1740 + i * 38}" y="318" width="36" height="84" fill="{c}" opacity=".85"/>'
    s += usturlap(s, 1980, 210, 52)
    s += f'<path d="M1980 262 L1960 400 M1980 262 L2004 400" stroke="#6A4A10" stroke-width="5"/>'
    s += _use("pamuk-sasiran", 1300, 330, 82, 94)
    s += S.marti(1180, 120, .6, 2, renk="#2A1E40")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 4. DURAK · URFA ÇARŞISI (sabah; bakırcılar, isot)

def urfa_carsi():
    s = Svg("ah-car")
    ufuk = 300
    gok = [(0, "#3A93DC"), (.55, "#9BD3F0"), (1, "#FDEBC6")]
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=gok)
    s += S.gunes(s, 260, 70, 30, cekirdek="#FFFDF0", hale="#FFE6A0", hale_r=380, guc=.8)
    s += S.bulut(s, 900, 120, 200, 41, ust="#FFFFFF", alt="#DCEAF4", op=.9)
    # uzakta kale tepesi (iki sütun) ve taş evler
    s += f'<g opacity=".55">{kale_tepesi(s, 640, 1120, ufuk + 10, ufuk - 120, 42, isik=-1, olcek=.5)}</g>'
    for i in range(9):
        s += f'<g opacity=".7">{tas_ev(s, 420 + i * 92, ufuk + 30, 84, 40 + (i % 3) * 10, 43 + i, isik=-1, kemer=True)}</g>'
    s += f'<rect x="0" y="{ufuk + 28}" width="{W}" height="{H - ufuk}" fill="#D9C7A0"/>'
    # taş döşeme
    for i in range(7):
        yy = ufuk + 40 + i * i * 3.6
        s += f'<path d="M0 {f(yy)} H{W}" stroke="#B9A47C" stroke-width="{f(1.5 + i * .4)}" opacity=".6"/>'
    # revak: üç büyük kemer (sağ), içinde dükkânlar
    s += kemer_dizisi(s, 1180, 452, 3, 250, 160, 44, ic="#6A4A30", ust=46, isik_ic="#FFC97A")
    # dükkân 1: bakırcı (kazanlar, tepsiler)
    for k, (x, y, w, t) in enumerate(((1300, 420, 70, "tepsi"), (1388, 400, 62, "tepsi"), (1260, 448, 90, "kazan"), (1360, 450, 70, "kazan"),
                                      (1440, 448, 40, "ibrik"))):
        s += bakir_kap(s, x, y, w, t, 50 + k)
    # dükkân 2: isot çuvalları
    for k, x in enumerate((1590, 1660, 1730)):
        s += isot_cuvali(s, x, 452, 62, 60 + k, renk=["#C8321E", "#A9281A", "#D9452A"][k])
    # dükkân 3: asılı fenerler ve kumaşlar
    for k, (x, c) in enumerate(((1860, "#2B50B5"), (1900, "#E2533D"), (1940, "#13A3A6"), (1980, "#F0A21A"))):
        s += f'<path d="M{x} 300 V400 L{x + 30} 410 V300 Z" fill="{c}" opacity=".95"/><path d="M{x} 330 H{x + 30} M{x} 360 H{x + 30}" stroke="#FFFFFF" stroke-width="2" opacity=".6"/>'
    s += fener(s, 1295, 290, 26)
    s += fener(s, 1560, 292, 26)
    s += fener(s, 1825, 290, 26)
    s += _use("pamuk-akce", 1505, 366, 74, 86)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 5. DURAK · HALFETİ (öğle; teraslı taş evler, turkuaz su)

def halfeti():
    s = Svg("ah-hal")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gun")
    s += S.gunes(s, 1880, 64, 30, cekirdek="#FFFDF0", hale="#FFE6A0", hale_r=360, guc=.8)
    s += S.bulut(s, 1240, 96, 210, 51, ust="#FFFFFF", alt="#D6E8F5", op=.9)
    s += S.bulut(s, 700, 70, 160, 52, ust="#FFFFFF", alt="#D6E8F5", op=.75)
    # karşı kıyı: alçak kalker yarlar (soluk)
    karsi = kayalik(s, -20, 1300, ufuk - 50, ufuk + 6, 53, renk="#E3D2AE", golge="#C2A982", katman=4)
    s += f'<g opacity=".85">{karsi}</g>'
    # Fırat (baraj gölü)
    s += S.gol(s, 0, ufuk + 4, W, H - ufuk, 54, ufuk=FIRAT["ufuk"], orta=FIRAT["orta"], derin=FIRAT["derin"], gunes_x=1880, parilti_renk="#FFF6D0", yogunluk=1.1)
    s += S.yansima(s, karsi, ufuk + 4, 0, 1300, 80, op=.25)
    # sağ yamaç: teraslı taş evler
    yamac = [(1180, H), (1240, 360), (1330, 300), (1450, 250), (1600, 190), (1780, 150), (1950, 120), (2100, 110), (2100, H)]
    g = s.lin([(0, "#E8D5AC"), (1, "#B79868")], 0, 110, 0, H, kull="userSpaceOnUse", ad="ym")
    s += f'<path d="{egri_d(yamac[:-1])} L2100 {H} Z" fill="{g}"/>'
    r = RNG(55)
    evler = []
    for sira, (yy, x0, x1, hh) in enumerate(((190, 1640, 2100, 54), (250, 1480, 2100, 60), (310, 1340, 2100, 64), (372, 1260, 2060, 70))):
        x = x0
        while x < x1:
            ww = r.uniform(70, 104)
            evler.append(tas_ev(s, x, yy, ww, hh * r.uniform(.85, 1.1), 56 + sira * 20 + int(x), tas=r.choice(["#F1E2BF", "#E9D7AE", "#F4E9D0"]), isik=1,
                                cumba=r.random() < .2))
            x += ww + r.uniform(6, 22)
    s += "".join(evler)
    # su altında kalmış eski evlerin izleri (temsilî): su çizgisinde soluk duvar uçları
    for k, x in enumerate((1220, 1300, 1390)):
        s += f'<rect x="{x}" y="{ufuk + 120 + k * 6}" width="58" height="22" fill="#CDBB94" opacity=".55"/><rect x="{x}" y="{ufuk + 136 + k * 6}" width="58" height="10" fill="{FIRAT["orta"]}" opacity=".7"/>'
    # iskele, tekneler, karagül saksıları
    s += f'<rect x="1150" y="408" width="420" height="16" fill="#9A6B42"/><path d="M1150 414 H1570" stroke="#C8955E" stroke-width="2"/>'
    for x in range(1160, 1571, 52):
        s += f'<rect x="{x}" y="420" width="8" height="40" fill="#6B4A2E"/>'
    s += S.tekne(s, 1000, 440, 120, govde="#2B50B5", ust="#F4E9D8")
    s += f'<path d="M940 410 H1060 V398 H940 Z" fill="#E2533D"/><path d="M944 410 V420 M1056 410 V420" stroke="#3A2A1A" stroke-width="2"/>'
    s += S.tekne(s, 760, 456, 90, govde="#C8442F", ust="#F4E9D8")
    for k, x in enumerate((1600, 1660)):
        s += f'<path d="M{x - 14} 408 L{x - 10} 384 H{x + 10} L{x + 14} 408 Z" fill="#B5602A"/>'
        for j in range(3):
            s += f'<circle cx="{x - 8 + j * 8}" cy="{378 - (j % 2) * 6}" r="7" fill="#3A0A14"/><circle cx="{x - 8 + j * 8}" cy="{378 - (j % 2) * 6}" r="3" fill="#7A1426"/>'
    s += _use("pamuk-selam", 1420, 318, 80, 92)
    s += S.dalga_cizgileri(0, ufuk + 40, 1150, 160, 57, op=.5)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 6. DURAK · FIRAT KIYISI (ikindi; tekne ve halkalar)

def firat():
    s = Svg("ah-fir")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "altin")
    s += _isinlar(s, 1720, 170, 12, op=.06, renk="#FFF2D0")
    s += S.gunes(s, 1720, 170, 38, cekirdek="#FFF9E8", hale="#FFD27A", hale_r=480, guc=.9)
    s += S.bulut_serit(s, 300, 150, 420, 10, "#FFF1D6", "#F7CF9E", .55)
    s += S.bulut_serit(s, 1100, 92, 380, 9, "#FFF1D6", "#F7CF9E", .5)
    # iki yakada kalker yarlar
    sol = kayalik(s, -40, 900, ufuk - 70, ufuk + 6, 61, renk="#E6CFA0", golge="#BF9D6C", katman=5)
    s += sol
    sirt = [(1500, ufuk + 6), (1560, ufuk - 80), (1650, ufuk - 120), (1760, ufuk - 140), (1880, ufuk - 170), (2000, ufuk - 186), (2120, ufuk - 190)]
    sag = kayalik(s, 1500, 2120, ufuk - 190, ufuk + 6, 62, renk="#E9D3A4", golge="#B8936A", katman=7, sirt=sirt)
    s += sag
    s += S.gol(s, 0, ufuk + 4, W, H - ufuk, 63, ufuk="#FBE7C2", orta="#2AAEA4", derin="#07646B", gunes_x=1720, parilti_renk="#FFE9B0", yogunluk=1.2)
    s += S.yansima(s, sol + sag, ufuk + 4, 0, W, 120, op=.22)
    # su halkaları: düşen taşın açtığı eş merkezli halkalar (küresel simetri benzetmesi)
    hx, hy = 1250, 400
    for k in range(6):
        s += f'<ellipse cx="{hx}" cy="{hy}" rx="{18 + k * 34}" ry="{5 + k * 9}" fill="none" stroke="#FFFFFF" stroke-width="{f(3.2 - k * .35, 2)}" opacity="{f(.85 - k * .12, 2)}"/>'
    s += f'<circle cx="{hx}" cy="{hy - 28}" r="5" fill="#FFFFFF"/><path d="M{hx - 8} {hy - 8} L{hx} {hy - 26} L{hx + 8} {hy - 8}" stroke="#FFFFFF" stroke-width="2" fill="none" opacity=".7"/>'
    # tur teknesi: Elif, Yusuf, Pamuk (gövde teknenin arkasında)
    tx, ty = 1620, 420
    s += f'<path d="M{tx - 210} {ty - 128} H{tx + 170} V{ty - 116} H{tx - 210} Z" fill="#E2533D"/>'
    s += f'<path d="M{tx - 200} {ty - 116} V{ty - 40} M{tx + 160} {ty - 116} V{ty - 40}" stroke="#3A2A1A" stroke-width="5"/>'
    s += _use("yusuf-anlatan", tx - 170, ty - 150, 120, 126)
    s += _use("elif-soru", tx - 40, ty - 150, 120, 126, ayna=True)
    s += f'<path d="M{tx - 260} {ty - 46} L{tx + 230} {ty - 46} L{tx + 196} {ty + 4} Q{tx} {ty + 22} {tx - 220} {ty + 4} Z" fill="#2B50B5" stroke="#1B1D26" stroke-width="4" stroke-linejoin="round"/>'
    s += f'<path d="M{tx - 252} {ty - 32} H{tx + 222}" stroke="#F4E9D8" stroke-width="6"/>'
    s += _use("pamuk-selam", tx + 110, ty - 140, 82, 94)
    s += S.dalga_cizgileri(900, ufuk + 60, 1100, 150, 64, op=.55)
    for k, (x, y, o) in enumerate(((1060, 160, .9), (1130, 190, .7), (980, 210, .6))):
        s += S.marti(x, y, o, 2 - k, renk="#5A4630")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ HÜLASA · GÜMRÜK HANI (akşamüstü; iki katlı revaklı avlu)

def gumruk_hani(h=400):
    s = Svg("ah-gum")
    ufuk = 210
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "alaca")
    s += S.yildizlar(s, 0, 0, 1300, 150, 50, 71)
    gl = s.rad([(0, "#FFB070", .6), (1, "#FFB070", 0)], 600, ufuk, 700, kull="userSpaceOnUse", ad="ak")
    s += f'<ellipse cx="600" cy="{ufuk}" rx="900" ry="140" fill="{gl}"/>'
    # karşı kanat (uzak): iki katlı revak, kemerlerde ışık
    s += kemer_dizisi(s, 40, ufuk + 6, 8, 96, 44, 72, tas="#D8BF92", ic="#5A3E2A", ust=14, isik_ic="#FFC97A")
    s += kemer_dizisi(s, 40, ufuk + 96, 6, 130, 50, 76, tas="#CDB386", ic="#4A3220", ust=8, isik_ic="#FFB65A")
    g = s.lin([(0, "#C4A87C"), (1, "#8E7550")], 0, ufuk + 96, 0, h, kull="userSpaceOnUse", ad="av")
    s += f'<rect x="0" y="{ufuk + 96}" width="{W}" height="{h}" fill="{g}"/>'
    for i in range(6):
        s += f'<path d="M0 {ufuk + 104 + i * i * 4} H{W}" stroke="#7A6440" stroke-width="1.5" opacity=".4"/>'
    for i in range(-6, 20):
        s += f'<path d="M{1050 + i * 14} {ufuk + 96} L{1050 + i * 80} {h}" stroke="#7A6440" stroke-width="1.2" opacity=".25"/>'
    # sağ kanat (yakın): üst kat küçük kemerler + balkon parmaklığı, alt kat büyük kemerler
    s += kemer_dizisi(s, 1150, 236, 5, 118, 50, 73, ic="#5A3E2A", ust=18, isik_ic="#FFC97A")
    s += f'<rect x="1150" y="236" width="960" height="14" fill="#B79A6E"/>'
    for x in range(1156, 2110, 18):
        s += f'<path d="M{x} 236 V214" stroke="#6B4A2E" stroke-width="3"/>'
    s += f'<path d="M1150 214 H2110" stroke="#6B4A2E" stroke-width="5"/>'
    for k, x in enumerate((1330, 1600, 1870)):   # balkona asılı kilimler
        s += f'<rect x="{x}" y="214" width="90" height="56" fill="{["#B5302A", "#2B50B5", "#1F8A5B"][k]}"/>'
        s += f'<path d="M{x + 8} 242 l14 -12 l14 12 l14 -12 l14 12 l14 -12" stroke="#F0C14A" stroke-width="3" fill="none"/>'
    s += kemer_dizisi(s, 1150, 400, 3, 210, 60, 74, ic="#4A3220", ust=6, isik_ic="#FFB65A")
    # çay masaları, tabureler, bardaklar
    for k, x in enumerate((760, 930, 1090)):
        s += f'<ellipse cx="{x}" cy="352" rx="54" ry="12" fill="#6B4A2E"/><rect x="{x - 5}" y="352" width="10" height="34" fill="#4A3220"/>'
        for j in range(3):
            bx = x - 30 + j * 26
            s += f'<path d="M{bx - 6} 340 L{bx - 4} 350 H{bx + 4} L{bx + 6} 340 Z" fill="#B5302A" opacity=".9"/><path d="M{bx - 6} 340 H{bx + 6}" stroke="#FFFFFF" stroke-width="1.4"/>'
        s += f'<rect x="{x - 72}" y="370" width="24" height="18" fill="#8E5A34"/><rect x="{x + 48}" y="370" width="24" height="18" fill="#8E5A34"/>'
    for x in (1270, 1520, 1770, 2020):
        s += fener(s, x, 300, 20, zincir=40)
    s += S.agac(s, 620, 384, 92, 75, renk="#4E7A3A", gov="#5A3E24")
    s += _use("pamuk-kitap", 990, 290, 70, 80)
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ YAN YOL 1 · SIRA GECESİ (gece; Urfa evinin avlusu)

def sira_gecesi():
    s = Svg("ah-sir")
    ufuk = 210
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 20, 110, 81)
    s += S.ay(s, 880, 80, 24)
    # avlu: solda alçak taş duvar ve saksılar, zeminde kilim; sağda eyvan
    g = s.lin([(0, "#6A5A4E"), (1, "#3A2E28")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect x="0" y="{ufuk}" width="{W}" height="{H - ufuk}" fill="{g}"/>'
    for i in range(8):
        s += f'<path d="M0 {ufuk + 12 + i * 26} H1150" stroke="#2A201A" stroke-width="1.4" opacity=".45"/>'
    for i in range(14):
        s += f'<path d="M{i * 84 + (i % 2) * 40} {ufuk} V{ufuk + 26}" stroke="#2A201A" stroke-width="1.2" opacity=".35"/>'
    g2 = s.lin([(0, "#8E7462"), (1, "#5A4A40")], 0, 380, 0, H, kull="userSpaceOnUse", ad="zm")
    s += f'<rect x="0" y="380" width="{W}" height="{H - 380}" fill="{g2}"/>'
    s += f'<rect x="560" y="404" width="560" height="56" fill="#9A2A22"/><rect x="572" y="412" width="536" height="40" fill="none" stroke="#F0C14A" stroke-width="3"/>'
    for k in range(8):
        cx = 600 + k * 66
        s += f'<path d="M{cx} 432 l14 -12 l14 12 l-14 12 Z" fill="#F0C14A" opacity=".85"/>'
    for k, x in enumerate((180, 300, 420)):
        s += f'<path d="M{x - 22} 380 L{x - 16} 340 H{x + 16} L{x + 22} 380 Z" fill="#9A4E1C"/>'
        s += f'<circle cx="{x}" cy="330" r="{26 - k * 3}" fill="#3E6E2C"/><circle cx="{x - 10}" cy="322" r="6" fill="#E2533D"/>'
    s += f'<rect x="1150" y="60" width="950" height="{H}" fill="#C9B289"/>'
    for i in range(12):
        s += f'<path d="M1150 {60 + i * 34} H2100" stroke="#9C8058" stroke-width="1.4" opacity=".45"/>'
    ex, ew = 1300, 640
    d = f"M{ex} {H} V200 A{ew / 2} {ew / 2 * .7} 0 0 1 {ex + ew} 200 V{H} Z"
    gi = s.rad([(0, "#FFD48A"), (.7, "#E8A050"), (1, "#7A4A20")], ex + ew / 2, 330, 420, kull="userSpaceOnUse", ad="ey")
    s += f'<path d="{d}" fill="{gi}"/>'
    s += f'<path d="M{ex - 24} {H} V200 A{ew / 2 + 24} {(ew / 2 + 24) * .7} 0 0 1 {ex + ew + 24} 200 V{H}" fill="none" stroke="#8E7050" stroke-width="10"/>'
    # kemer çevresinde taş oyma bordür (geometrik)
    for k in range(17):
        a = math.pi + k * math.pi / 16
        rx, ry = ew / 2 + 42, (ew / 2 + 42) * .7
        px, py = ex + ew / 2 + rx * math.cos(a), 200 + ry * math.sin(a)
        s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 9), True)}" fill="#E8D4AA" stroke="#8E7050" stroke-width="1.2"/>'
    # minderler (kilim desenli) ve yastıklar
    for k in range(5):
        mx = ex + 30 + k * 118
        s += f'<rect x="{mx}" y="400" width="110" height="40" rx="6" fill="{["#B5302A", "#2B50B5", "#B5302A", "#1F8A5B", "#B5302A"][k]}"/>'
        s += f'<path d="M{mx + 10} 420 l12 -10 l12 10 l12 -10 l12 10 l12 -10 l12 10 l12 -10" stroke="#F0C14A" stroke-width="2.4" fill="none"/>'
        s += f'<rect x="{mx + 8}" y="352" width="94" height="50" rx="14" fill="{["#E2533D", "#F0A21A", "#13A3A6", "#E2533D", "#7B3F8C"][k]}" stroke="#3A1E10" stroke-width="2"/>'
    s += f'<ellipse cx="1620" cy="452" rx="120" ry="16" fill="#C9952B" stroke="#6A4A10" stroke-width="2"/>'
    for j in range(5):
        bx = 1540 + j * 40
        s += f'<path d="M{bx - 7} 432 L{bx - 5} 446 H{bx + 5} L{bx + 7} 432 Z" fill="#A9281A" opacity=".9"/><path d="M{bx - 7} 432 H{bx + 7}" stroke="#FFFFFF" stroke-width="1.4"/>'
    s += f'<path d="M1500 446 C1490 420 1510 404 1520 404 C1530 404 1550 420 1540 446 Z" fill="#E2533D" stroke="#3A1E10" stroke-width="2"/>'
    s += f'<ellipse cx="2010" cy="400" rx="34" ry="46" fill="#8E5A34" stroke="#3A1E10" stroke-width="2.4"/><path d="M2010 356 L2050 190" stroke="#5A3A22" stroke-width="9" stroke-linecap="round"/>'
    s += fener(s, 1450, 150, 22, zincir=80)
    s += fener(s, 1790, 150, 22, zincir=80)
    s += _use("pamuk-dusunen", 1950, 330, 80, 92)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ YAN YOL 2 · HARRAN OVASI (sabah; pamuk tarlaları, sulama kanalı)

def harran_ovasi():
    s = Svg("ah-ova")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "safak")
    s += S.gunes(s, 1880, ufuk - 40, 40, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=440, guc=.95)
    s += S.bulut_serit(s, 420, 160, 420, 10, "#FFE3EA", "#F6B8C8", .5)
    s += f'<g opacity=".6">{harran_kumesi(s, 1450, ufuk + 6, .26, 85, n=6, kapi=False)}</g>'
    g = s.lin([(0, "#A9C26A"), (1, "#4E8A3A")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="tr")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{H - ufuk}" fill="{g}"/>'
    # sıralar: perspektifte ufka koşan pamuk sıraları
    for k in range(-12, 26):
        x0 = 1050 + k * 90
        s += f'<path d="M{1050 + k * 16} {ufuk + 6} L{x0} {H}" stroke="#3E6E2C" stroke-width="{f(2 + abs(k) * .05, 2)}" opacity=".35"/>'
    # sulama kanalı (beton kenarlı, düz)
    s += f'<path d="M{1180} {ufuk + 6} L{1240} {ufuk + 6} L{1500} {H} L{1330} {H} Z" fill="#D9D2C2"/>'
    gk = s.lin([(0, "#9FE0E6"), (1, "#2C9EA6")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="kn")
    s += f'<path d="M{1190} {ufuk + 6} L{1230} {ufuk + 6} L{1470} {H} L{1360} {H} Z" fill="{gk}"/>'
    s += S.dalga_cizgileri(1300, 360, 140, 90, 86, op=.6, n=8)
    r = RNG(87)
    for k in range(70):
        y = ufuk + 20 + (k / 70) ** 1.6 * (H - ufuk - 10)
        x = r.uniform(1520, 2100) if k % 2 else r.uniform(0, 1150)
        sc = .3 + (y - ufuk) / (H - ufuk) * 1.1
        s += pamuk_bitkisi(x, y, 46 * sc, 900 + k)
    s += pamuk_bitkisi(1660, 452, 86, 88)
    s += pamuk_bitkisi(1780, 456, 92, 89)
    s += pamuk_bitkisi(1960, 458, 96, 90)
    s += _use("pamuk-otur", 1830, 368, 78, 90)
    s += S.marti(1000, 150, .7, 2, renk="#6A4A70")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ YAN YOL 3 · URFA EVLERİ (ikindi; taş evler, dama çıkan merdiven)

def urfa_evleri():
    s = Svg("ah-eve")
    ufuk = 290
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "altin")
    s += S.gunes(s, 1640, 150, 34, cekirdek="#FFF9E8", hale="#FFD27A", hale_r=420, guc=.85)
    s += S.bulut_serit(s, 340, 130, 420, 10, "#FFF1D6", "#F7CF9E", .55)
    for i in range(12):
        s += f'<g opacity=".55">{tas_ev(s, 300 + i * 74, ufuk + 20, 70, 44 + (i % 4) * 9, 91 + i, isik=1)}</g>'
    g = s.lin([(0, "#E3CFA4"), (1, "#B99E70")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="sk")
    s += f'<rect x="0" y="{ufuk + 20}" width="{W}" height="{H - ufuk}" fill="{g}"/>'
    for i in range(7):
        s += f'<path d="M0 {ufuk + 28 + i * i * 3.4} H{W}" stroke="#A88D62" stroke-width="1.4" opacity=".5"/>'
    # büyük taş ev: cumba + dama çıkan dış merdiven
    s += tas_ev(s, 1500, 452, 420, 250, 95, isik=1, cumba=True)
    s += tas_ev(s, 1240, 452, 220, 190, 96, isik=1, merdiven=True)
    s += tas_ev(s, 1930, 452, 200, 210, 97, isik=1)
    # damda yazlık yatak (temsilî): kafes ve yorgan
    s += f'<rect x="1540" y="186" width="160" height="14" fill="#E2533D"/><path d="M1540 186 V150 H1700 V186" fill="none" stroke="#6B4A2E" stroke-width="4"/>'
    s += f'<path d="M1560 150 V186 M1580 150 V186 M1600 150 V186 M1620 150 V186 M1640 150 V186 M1660 150 V186 M1680 150 V186" stroke="#6B4A2E" stroke-width="1.6" opacity=".6"/>'
    # avlu: nar ağacı, saksılar
    s += S.agac(s, 1180, 440, 70, 98, renk="#4E8A3A", gov="#5A3E24", meyve="#C8321E")
    for k, x in enumerate((1460, 1480)):
        s += f'<path d="M{x - 10} 452 L{x - 7} 434 H{x + 7} L{x + 10} 452 Z" fill="#B5602A"/><circle cx="{x}" cy="428" r="9" fill="#5FA548"/>'
    s += _use("pamuk-dusunen", 1330, 360, 70, 80)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ KALE · URFA KALESİ (gün batımı; b62)

def urfa_kalesi(h=620):
    s = Svg("ah-kal")
    ufuk = 430
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    s += _isinlar(s, 900, ufuk - 40, 14, op=.08, renk="#FFE0A0")
    s += S.gunes(s, 900, ufuk - 40, 56, hale="#FFC56B", hale_r=640, guc=.95)
    for (x, y, w_, k) in ((200, 200, 520, 22), (1000, 140, 600, 26), (1300, 300, 420, 16)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC59A", "#FF6F8A", .7)
    # uzak tepeler ve şehrin zemini
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 10, 18, 100, "#B9708A", "#A0607E", dalga=5)
    s += tb
    g = s.lin([(0, "#C77E7A"), (1, "#7A4A5E")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="zm")
    s += f'<rect x="0" y="{ufuk + 14}" width="{W}" height="{h - ufuk}" fill="{g}"/>'
    # kale tepesi (sağ)
    s += kale_tepesi(s, 1160, 2160, h - 50, 250, 101, isik=-1, olcek=1.0)
    # aşağıda şehir: taş evler
    r = RNG(102)
    for i in range(18):
        x = i * 70 - 30
        s += tas_ev(s, x, h - 36 + (i % 2) * 8, 66, 54 + r.uniform(0, 40), 103 + i, tas=r.choice(["#E8C2A2", "#DDB394", "#F0D0B0"]), isik=-1)
    for i in range(6):
        s += S.agac(s, 160 + i * 190, h - 44, 34, 110 + i, renk="#5C7A3A", gov="#4A3220", meyve="#C8321E" if i % 2 else None)
    g2 = s.lin([(0, "#8E5A5A"), (1, "#4A2A3A")], 0, h - 50, 0, h, kull="userSpaceOnUse", ad="sh")
    s += f'<rect x="0" y="{h - 36}" width="{W}" height="36" fill="{g2}"/>'
    for k, (x, y, o) in enumerate(((1080, 180, 1.0), (1150, 210, .7), (720, 140, .8))):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


def kale_kapi_urfa(h=300):
    s = Svg("ah-kkp")
    s += S.gokyuzu(s, 0, 0, W, h, "gunbatimi")
    s += S.gunes(s, 520, 220, 40, hale="#FFC56B", hale_r=420, guc=.9)
    # kayaya oyulmuş hendek ve sur (yakın plan)
    g = s.lin([(0, "#E8C9A0"), (1, "#9C7450")], 0, 60, 0, h, kull="userSpaceOnUse", ad="sr")
    s += f'<rect x="1180" y="70" width="940" height="{h}" fill="{g}"/>'
    r = RNG(111)
    for row in range(8):
        y = 74 + row * 30
        off = 0 if row % 2 == 0 else 40
        for x in range(1180 - 40 + off, 2120, 80):
            s += f'<rect x="{x + 2}" y="{y}" width="76" height="27" rx="3" fill="{karis("#E3C59A", "#B58E66", r.uniform(0, .7))}" stroke="#7A5A3A" stroke-width="1.4"/>'
    for x in range(1180, 2120, 64):
        s += f'<rect x="{x}" y="34" width="40" height="40" fill="#D9B98E" stroke="#7A5A3A" stroke-width="2"/>'
    s += f'<path d="M1560 {h} V170 Q1560 110 1630 104 Q1700 110 1700 170 V{h} Z" fill="#3A2214"/>'
    s += f'<path d="M1572 {h} V172 Q1572 122 1630 116 Q1688 122 1688 172 V{h}" fill="none" stroke="#C9A06A" stroke-width="5"/>'
    s += f'<rect x="1500" y="250" width="260" height="20" fill="#7A4E2E"/><path d="M1500 252 L1440 {h} M1760 252 L1820 {h}" stroke="#5A3A22" stroke-width="7"/>'
    s += f'<rect x="1100" y="{h - 40}" width="1020" height="40" fill="#5A3A2A"/>'
    s += _use("pamuk-selam", 1830, 160, 76, 88)
    for k in range(30):
        x = r.uniform(300, 1100)
        y = r.uniform(30, 200)
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(1, 2.4))}" fill="#FFF0D0" opacity="{f(r.uniform(.3, .8), 2)}"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ CEVAPLAR · HARRAN GECESİ (Samanyolu ve kovan evler)

def harran_gece(h=360):
    s = Svg("ah-gec")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gece")
    s += samanyolu(s, 300, 330, 1900, -60, 120, 121)
    s += S.yildizlar(s, 0, 0, W, ufuk - 20, 190, 122)
    s += S.ay(s, 1260, 70, 20, golge_renk="#13204A")
    g = s.lin([(0, "#2A2A52"), (1, "#14142E")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="ov")
    s += f'<path d="M0 {ufuk + 4} C700 {ufuk - 4} 1400 {ufuk + 8} 2100 {ufuk + 2} V{h} H0 Z" fill="{g}"/>'
    s += harran_kumesi(s, 1240, ufuk + 70, .82, 123, n=7, kapi=True, badana_oran=0, renk="#4A4670", golge="#26244A", kapi_renk="#FFD27A")
    r = RNG(124)
    for k in range(7):
        x = 1300 + k * 96 + r.uniform(-8, 8)
        gl = s.rad([(0, "#FFD27A", .4), (1, "#FFD27A", 0)], x, ufuk + 60, 70, kull="userSpaceOnUse", ad="kg")
        s += f'<circle cx="{f(x)}" cy="{ufuk + 60}" r="70" fill="{gl}"/>'
    s += usturlap(s, 1150, ufuk + 20, 34, renk="#B38A2C", koyu_r="#3A2A0A")
    s += _use("pamuk-dusunen", 1060, ufuk + 6, 64, 74)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ FİNAL · URFA KALESİ BURCU (gün batımı)

def final_urfa(h=900, nisanlar=None):
    s = Svg("ah-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    gx, gy = 760, ufuk - 30
    s += _isinlar(s, gx, gy, 14, op=.12, renk="#FFE0A0", uz=1800)
    s += S.gunes(s, gx, gy, 70, hale="#FFC56B", hale_r=700, guc=.95)
    for (x, y, w_, k) in ((200, 260, 520, 22), (1200, 180, 640, 26), (1500, 330, 480, 16), (100, 420, 380, 12)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC59A", "#FF6F8A", .75)
    # uzakta Harran ovası ve kovan evler, yakın şehir
    s += f'<rect x="0" y="{ufuk}" width="{W}" height="{h - ufuk}" fill="#B76A6E"/>'
    s += f'<g opacity=".55">{harran_kumesi(s, 120, ufuk + 34, .4, 131, n=8, kapi=False, badana_oran=0)}</g>'
    r = RNG(132)
    for i in range(14):
        s += f'<g opacity=".85">{tas_ev(s, 60 + i * 96, ufuk + 110 + (i % 2) * 8, 88, 54 + r.uniform(0, 30), 133 + i, tas="#C99A86", isik=-1)}</g>'
    # iki sütun (arka planda, kale tepesinde)
    s += f'<g opacity=".9">{kale_tepesi(s, 1100, 1560, ufuk + 120, ufuk - 40, 134, isik=-1, sur=False, olcek=1.1)}</g>'
    for k, (x, y, o) in enumerate([(560, 200, 1.4), (640, 240, 1.0), (1100, 120, .8), (1180, 150, .6), (300, 160, .7)]):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    # ön plan: kalker burç ve mazgallar
    g = s.lin([(0, "#E8C9A0"), (1, "#9C7450")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    s += f'<rect x="0" y="720" width="{W}" height="{h - 720}" fill="{g}"/>'
    for row in range(6):
        y = 724 + row * 30
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            s += f'<rect x="{x + 2}" y="{y}" width="86" height="27" rx="3" fill="{karis("#E3C59A", "#B58E66", r.uniform(0, .7))}" stroke="#7A5A3A" stroke-width="1.6"/>'
    for x in range(0, W, 150):
        s += f'<rect x="{x}" y="660" width="96" height="64" fill="#D9B98E" stroke="#7A5A3A" stroke-width="2.6"/><rect x="{x - 3}" y="652" width="102" height="14" rx="6" fill="#F4E4C4"/>'
    gt = s.lin([(0, "#E8CDA6"), (.6, "#C9A47A"), (1, "#9C7450")], 1560, 0, 1980, 0, kull="userSpaceOnUse", ad="tk")
    s += f'<rect x="1560" y="560" width="420" height="{h - 560}" fill="{gt}" stroke="#7A5A3A" stroke-width="3"/>'
    for x in range(1560, 1980, 84):
        s += f'<rect x="{x}" y="510" width="54" height="56" fill="#D2B084" stroke="#7A5A3A" stroke-width="2.6"/><rect x="{x - 3}" y="504" width="60" height="12" rx="6" fill="#F4E4C4"/>'
    s += f'<path d="M1740 {h} V760 Q1740 720 1770 712 Q1800 720 1800 760 V{h} Z" fill="#3A2214"/>'
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


# ------------------------------------------------------------------ AÇILIŞ · ŞANLIURFA PANORAMASI + TUR ROTASI

# Stilize tur haritası (temsilî): batıda Fırat (Birecik Barajı gölü) ve Halfeti, ortada Urfa platosu ve şehir,
# kuzeydoğuda Göbeklitepe, güneydoğuda Harran Ovası ve Harran. Konumlar panorama birimidir (2100×1100);
# şehir kalabalık olduğu için şehirdeki duraklar aralıklı çizildi (ölçek dışı).
DURAKLAR = [  # (anahtar, x, y, tür)
    ("1", 1700, 470, "durak"), ("2", 1790, 975, "durak"), ("3", 1950, 905, "durak"), ("4", 1430, 650, "durak"),
    ("5", 400, 565, "durak"), ("6", 480, 715, "durak"), ("H", 1130, 700, "hulasa"), ("M", 1270, 800, "yan"),
    ("K", 1580, 880, "yan"), ("A", 1520, 760, "yan"), ("V", 1310, 590, "kale"),
]
ROTA_ARA = {("1", "2"): [(1760, 640), (1720, 820)], ("2", "3"): [(1880, 970)], ("3", "4"): [(1900, 760), (1640, 690)],
            ("4", "5"): [(1180, 560), (820, 520), (560, 520)], ("5", "6"): [(380, 650)], ("6", "H"): [(700, 760), (950, 740)],
            ("H", "M"): [(1170, 790)], ("M", "K"): [(1420, 860)], ("K", "A"): [(1620, 810)], ("A", "V"): [(1400, 720), (1320, 650)]}


def _durak_rozet(k, x, y, tur):
    if tur == "durak":
        return (f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 36), True)}" fill="#F0C14A" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 29), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2" stroke-linejoin="round"/>'
                f'<text x="{f(x)}" y="{f(y + 11)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="32" fill="#FFFFFF">{k}</text>')
    if tur == "kale":
        return (f'<circle cx="{f(x)}" cy="{f(y)}" r="34" fill="#E2533D" stroke="#1B1D26" stroke-width="3"/>'
                f'<path d="M{f(x - 18)} {f(y + 14)} V{f(y - 6)} h6 v-6 h6 v6 h4 v-6 h6 v6 h4 v-6 h6 v6 h4 V{f(y + 14)} Z" fill="#FFFFFF" stroke="#1B1D26" stroke-width="1.6"/>')
    renk = "#F0A21A" if tur == "yan" else "#7B3F8C"
    return (f'<path d="M{f(x)} {f(y - 32)} L{f(x + 32)} {f(y)} L{f(x)} {f(y + 32)} L{f(x - 32)} {f(y)} Z" fill="{renk}" stroke="#1B1D26" stroke-width="3" stroke-linejoin="round"/>'
            f'<text x="{f(x)}" y="{f(y + 10)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="27" fill="#FFFFFF">{k}</text>')


def panorama_urfa(h=1100):
    s = Svg("ah-pan")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "altin")
    gx, gy = 1860, ufuk - 70
    s += _isinlar(s, gx, gy, 12, op=.07, renk="#FFF0D0")
    s += S.gunes(s, gx, gy, 46, cekirdek="#FFF9E8", hale="#FFD27A", hale_r=600, guc=.95)
    for (x, y, w_, k) in ((560, 150, 520, 18), (1140, 100, 560, 22), (1500, 210, 380, 14), (60, 220, 340, 12)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFF1D6", "#F7CF9E", .6)
    # kuzeyde uzak dağlar (Toroslar, soluk) ve Karacadağ (doğuda, geniş volkan)
    for i, (sol, sag, tx, ty, bicim) in enumerate(((-150, 760, 300, 196, "tepe"), (520, 1400, 980, 170, "sivri"), (1200, 1900, 1560, 210, "tepe"),
                                                   (1700, 2300, 2020, 226, "volkan"))):
        d, _ = S.dag(s, sol, sag, ufuk + 6, tx, ty, 140 + i, renk="#BFA6C8", golge="#9A82B4", bicim=bicim, sis="#F6D9C8", isik=1, sirt=2, puruz=6)
        s += d
    # plato: altın bozkır, yeşil vadi ve bahçeler
    g = s.lin([(0, "#E9CB86"), (.35, "#DDB26A"), (.7, "#C9A05A"), (1, "#B08A4A")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="pl")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{g}"/>'
    for i, (yy, genlik, c1, c2) in enumerate(((ufuk + 30, 22, "#E3BF7C", "#EBCB8C"), (ufuk + 90, 26, "#D9B06A", "#E3C07E"), (ufuk + 170, 22, "#CFA25C", "#DCB474"))):
        tb, _ = S.tepe_bandi(s, 0, W, yy, genlik, 143 + i, c1, c2, dalga=6, olcek=40)
        s += tb
    r = RNG(146)
    # Atatürk Barajı gölü (kuzey, uzak; stilize)
    gol = [(240, 360), (520, 334), (820, 350), (1040, 336), (1180, 352), (1100, 380), (820, 392), (560, 388), (330, 398)]
    s += f'<path d="{egri_d(gol, True)}" fill="#52C3C8" stroke="#FFFFFF" stroke-width="4" opacity=".9"/>'
    # Fırat ve Birecik Barajı gölü (batı)
    firat_d = [(560, 360), (520, 430), (450, 500), (410, 580), (440, 660), (500, 740), (460, 840), (420, 960), (380, 1110)]
    s += f'<path d="{egri_d(firat_d)}" fill="none" stroke="#1E9AA0" stroke-width="64" stroke-linecap="round" opacity=".9"/>'
    s += f'<path d="{egri_d(firat_d)}" fill="none" stroke="#5FD3CC" stroke-width="40" stroke-linecap="round"/>'
    s += f'<path d="{egri_d(firat_d)}" fill="none" stroke="#B9F0E8" stroke-width="8" stroke-dasharray="20 26" stroke-linecap="round" opacity=".8"/>'
    # Fırat kıyısı kalker yarları (temsilî)
    for k in range(10):
        yy = 470 + k * 60
        s += f'<path d="M{350 - k * 3} {yy} l-40 18 l10 30" fill="none" stroke="#B8936A" stroke-width="6" opacity=".55"/>'
    # Halfeti (teraslı evler) ve tekne
    for k in range(7):
        s += tas_ev(s, 420 + (k % 4) * 30, 560 - (k // 4) * 26 + (k % 2) * 4, 26, 18, 150 + k, tas="#F1E2BF", isik=1, kemer=False)
    s += S.tekne(s, 520, 712, 34, govde="#2B50B5", ust="#F4E9D8")
    for k in range(5):
        s += f'<ellipse cx="520" cy="728" rx="{14 + k * 14}" ry="{4 + k * 4}" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="{f(.8 - k * .14, 2)}"/>'
    # Antep fıstığı / zeytin bahçeleri (plato; sıralı koyu yeşil)
    for bi, (bx0, by0, nx, ny) in enumerate(((650, 600, 10, 4), (800, 820, 12, 4), (1000, 470, 8, 3))):
        for i in range(nx):
            for j in range(ny):
                x = bx0 + i * 30 + j * 12
                y = by0 + j * 22
                if any(math.hypot(x - a, y - b) < 70 for _, a, b, _t in DURAKLAR):
                    continue
                sc = .6 + (y - ufuk) / (h - ufuk) * .6
                s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(9 * sc)}" fill="{r.choice(["#7A8E3A", "#6B7F32", "#889B44"])}"/><circle cx="{f(x - 3 * sc)}" cy="{f(y - 3 * sc)}" r="{f(4 * sc)}" fill="#A8BC5E" opacity=".7"/>'
    # Göbeklitepe (kuzeydoğu tepe): oval çukur ve küçük T taşları
    tb = [(1560, 520), (1630, 440), (1720, 418), (1820, 444), (1880, 520)]
    s += f'<path d="{egri_d(tb)} Z" fill="#D9AE62"/>'
    s += f'<ellipse cx="1720" cy="452" rx="58" ry="14" fill="#9C7A48"/>'
    for k in range(6):
        a = math.pi + k * math.pi / 5
        s += t_dikilitas(s, 1720 + 50 * math.cos(a), 456 + 12 * math.sin(a), 30, 160 + k, isik=1, oyma=0)
    # Urfa şehri: kale tepesi ve taş evler (stilize, büyütülmüş)
    s += kale_tepesi(s, 1200, 1430, 640, 540, 170, isik=-1, olcek=.42)
    for k in range(40):
        x = r.uniform(1060, 1620)
        y = r.uniform(600, 820)
        if any(math.hypot(x - a, y - b) < 52 for _, a, b, _t in DURAKLAR) or (1200 < x < 1430 and y < 650):
            continue
        sc = .5 + (y - ufuk) / (h - ufuk) * .5
        s += tas_ev(s, x, y, 34 * sc, 22 * sc, 200 + k, tas=r.choice(["#F1E2BF", "#E9D7AE", "#F4E9D0"]), isik=1, kemer=False)
    # Harran Ovası (güneydoğu): yeşil-altın tarlalar, sulama kanalları, pamuk
    ova = [(1150, 1100), (1240, 900), (1420, 840), (1700, 820), (2100, 800), (2100, 1100)]
    go = s.lin([(0, "#B9C56E"), (1, "#7FA650")], 0, 820, 0, 1100, kull="userSpaceOnUse", ad="ova")
    s += f'<path d="{egri_d(ova[:-1])} L2100 1100 Z" fill="{go}"/>'
    for k in range(9):
        s += f'<path d="M{1300 + k * 100} 1100 L{1500 + k * 66} 830" stroke="{["#E6D07A", "#6E9A44"][k % 2]}" stroke-width="{f(18 - k)}" opacity=".45"/>'
    s += f'<path d="M1240 860 L2100 920" stroke="#3DB5BE" stroke-width="7" opacity=".9"/><path d="M1500 840 L1420 1100" stroke="#3DB5BE" stroke-width="6" opacity=".9"/>'
    for k in range(80):
        x = r.uniform(1260, 2080)
        y = r.uniform(860, 1080)
        if any(math.hypot(x - a, y - b) < 50 for _, a, b, _t in DURAKLAR):
            continue
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(2.4, 4.2))}" fill="#FFFFFF" opacity=".9"/>'
    # Harran ve höyük: kovan ev kümeleri
    s += harran_kumesi(s, 1760, 1010, .3, 171, n=5, kapi=False)
    hoy = [(1880, 945), (1930, 905), (2000, 900), (2050, 940)]
    s += f'<path d="{egri_d(hoy)} Z" fill="#C9A066"/>'
    s += harran_kumesi(s, 1900, 930, .2, 172, n=4, kapi=False)
    # yollar (ince, açık)
    for yol in ([(1310, 600), (1500, 560), (1700, 480)], [(1430, 660), (1600, 780), (1790, 970)], [(1300, 610), (900, 560), (420, 560)]):
        s += f'<path d="{egri_d(yol)}" fill="none" stroke="#F6E7C4" stroke-width="6" opacity=".7"/>'
    # rota (ana yol + yan yollar)
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
    for k, x, y, tur in DURAKLAR:
        s += _durak_rozet(k, x, y, tur)
    # pusula (sağ alt)
    px, py = 2010, 1030
    s += f'<circle cx="{px}" cy="{py}" r="42" fill="#FFFFFF" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="M{px} {py - 34} L{px + 8} {py} L{px} {py + 34} L{px - 8} {py} Z" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="M{px - 34} {py} L{px} {py - 8} L{px + 34} {py} L{px} {py + 8} Z" fill="#F0C14A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 50}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="24" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")
