"""Kimyasal Güvenlik · Batı Karadeniz Maden Yolu — üniteye özel sahneler, nişan ikonları ve açılış panoraması.

kur_ortak bu modüle {{sahne|ad}} için ORTAK kütüphaneden (yerel-ortak/cizim) ÖNCE bakar. Ortak dosyalar değiştirilmez;
buradaki her şey ortak parçalardan (sahne, yapilar, karakter sembolleri) ve aşağıdaki Batı Karadeniz parçalarından kurulur:
  cam_agaci · orman_sirti (köknar-kayın ormanlı tepe) · kuyu_kulesi (maden kuyusu kulesi) · vagon · havalandirma_binasi
  yuksek_firin · pota (erimiş metal kepçesi) · sb_ev (Safranbolu evi: beyaz sıva + ahşap çatkı) · camasirhane · camasir_ipi
  surlar / burc (Amasra Kalesi) · kemer_kopru (Kemere) · lav_sutunlari (Güzelcehisar) · dukkan (Çekiciler Çarşısı)
Kompozisyon (TASARIM-SISTEMI §6): bant 2100×460; sol üst ≈ %55 × %75 sakin gökyüzü/deniz (levha); odak sağ %40'ta;
ışık solda (isik=-1); tohumlar sabit; her Svg öneki benzersiz; konturlu SVG yazısı yok (gerekirse halolu_yazi).
Hassasiyet: maden yalnız emniyet kültürüyle (kule, havalandırma, ölçer, lamba) çizilir; Amasra yalnız tarihî kale ve kıyı kasabasıdır.
Cami, kilise ve manastır çizilmez; logo yoktur. Çizimler temsilîdir.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim import sahne as S, yapilar as Y
from cizim.sahneler import W, H, _bitir, _cerceve_golge
from cizim.karakter import turk_bayragi  # noqa: F401
from cizim.renkler import MER, GOL, KEH, KOB  # noqa: F401
import infografik_unite as IU

# ------------------------------------------------------------------ Batı Karadeniz paleti
ORMAN = ["#2F6B3F", "#3B7D47", "#2A5E3A", "#467F3D", "#356F45"]   # köknar, kayın
ORMAN_A = "#5FA052"
DENIZ = ("#9FD3E6", "#2C83AE", "#11466B")                         # ufuk, orta, derin
SIVA = "#F7F2E6"         # Safranbolu beyaz sıvası
AHSAP = "#6B4527"        # çatkı (ahşap)
KIREMIT = "#B5523B"
TAS = "#CDBFA6"          # kale taşı (Amasra)
TAS_K = "#8E7F68"
CELIK = "#9A3B2A"        # kule boyası

# Üniteye özel nişan ikonları: 48×48 çizgi (dolgu yok; öğrenci boyar)
NISAN_IKON = {
    "baret": '<path d="M8 32 C8 16 40 16 40 32"/><path d="M5 32 H43 V36 H5 Z"/><path d="M24 15 V32"/><circle cx="24" cy="25" r="3.4"/>'
             '<path d="M24 8 V11 M15 10 l2 2.6 M33 10 l-2 2.6"/><path d="M14 42 h20"/>',
    "pota": '<path d="M9 14 H33 L30 34 Q29 38 25 38 H17 Q13 38 12 34 Z"/><path d="M33 14 L40 10"/><path d="M6 14 H36"/>'
            '<path d="M38 13 Q41 24 37 32 Q35 38 38 44"/><path d="M20 21 h6 M18 27 h9"/>',
    "elmas": '<path d="M24 4 L44 24 L24 44 L4 24 Z"/><path d="M24 9 L39 24 L24 39 L9 24 Z"/><path d="M22 15 H26 L25 28 H23 Z"/><circle cx="24" cy="32.5" r="1.8"/>',
    "etiket": '<path d="M17 4 H31 V10 Q38 13 38 20 V42 Q38 45 35 45 H13 Q10 45 10 42 V20 Q10 13 17 10 Z"/><rect x="13" y="22" width="22" height="16" rx="2"/>'
              '<path d="M16 27 h16 M16 32 h11"/><path d="M17 10 H31"/>',
    "erlen": '<path d="M19 4 H29 M20 4 V17 L8 40 Q7 44 11 44 H37 Q41 44 40 40 L28 17 V4"/><path d="M13 32 H35"/><path d="M27 23 h4 M27 28 h5"/>',
}


# ================================================================== PARÇALAR

def _zemin(s, y, renk, h=H):
    return f'<rect x="0" y="{f(y)}" width="{W}" height="{f(h - y + 2)}" fill="{renk}"/>'


def cam_agaci(s, x, y, h, w, tohum, renk=None, isik=-1, golge=None):
    """Köknar/ladin: üç-dört kat dişli koni. (x, y) gövde tabanı."""
    r = RNG(tohum)
    renk = renk or r.choice(ORMAN)
    golge = golge or koyu(renk, .3)
    kat = 4
    sol, sag = [], []
    for i in range(kat):
        t0 = i / kat
        yb = y - h * .1 - h * .82 * t0
        wb = w / 2 * (1 - t0 * .62) * r.uniform(.92, 1.06)
        yn = y - h * .1 - h * .82 * (i + 1) / kat + h * .06
        sol += [(x - wb, yb), (x - wb * .42, yn)]
        sag += [(x + wb, yb), (x + wb * .42, yn)]
    tepe = (x, y - h)
    pts = sol + [tepe] + list(reversed(sag))
    o = f'<rect x="{f(x - w * .05)}" y="{f(y - h * .12)}" width="{f(w * .1)}" height="{f(h * .12)}" fill="#4A3424"/>'
    o += f'<path d="{cizgi_d(pts, True)}" fill="{renk}"/>'
    yari = ([tepe] + list(reversed(sag)) + [(x, y - h * .1)]) if isik < 0 else (sol + [tepe, (x, y - h * .1)])
    o += f'<path d="{cizgi_d(yari, True)}" fill="{golge}" opacity=".55"/>'
    return o


def orman_sirti(s, x0, x1, y, genlik, tohum, renk, renk2, sik=1.0, olcek=1.0, agac=True, yuvarlak=.35, isik=-1, alt_ek=None):
    """Ormanlı tepe: yumuşak sırt + sırt boyunca sık ağaç silueti (köknar + yuvarlak taçlı kayın)."""
    tb, pts = S.tepe_bandi(s, x0, x1, y, genlik, tohum, renk, renk2)
    o = tb
    if agac:
        r = RNG(tohum + 7)
        n = int((x1 - x0) / (26 * olcek) * sik)
        for i in range(n):
            t = (i + r.uniform(0, .9)) / n
            x = x0 + (x1 - x0) * t
            j = min(len(pts) - 2, int(t * (len(pts) - 1)))
            py = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * (t * (len(pts) - 1) - j)
            py += r.uniform(2, 14) * olcek
            hh = r.uniform(34, 66) * olcek
            if r.random() < yuvarlak:
                o += S.agac(s, x, py + 6 * olcek, hh * .3, tohum * 31 + i, renk=karis(renk, "#7DB955", .35), isik=isik)
            else:
                o += cam_agaci(s, x, py, hh, hh * .5, tohum * 17 + i, renk=karis(renk, r.choice(ORMAN), .5), isik=isik)
    return o, pts


def deniz(s, x, y, w, h, tohum, gunes_x=None, renk=DENIZ, parilti="#FFE6A6"):
    return S.gol(s, x, y, w, h, tohum, ufuk=renk[0], orta=renk[1], derin=renk[2], gunes_x=gunes_x, parilti_renk=parilti)


def kuyu_kulesi(s, x, y, h, renk=CELIK, tohum=1):
    """Maden kuyusu kulesi (temsilî): kafes ayaklar, üstte iki makara çarkı, halatlar. (x, y) taban ortası."""
    o = []
    w = h * .42
    ust_y = y - h
    ayak = [(x - w / 2, y), (x - w * .16, ust_y + h * .1)], [(x + w / 2, y), (x + w * .16, ust_y + h * .1)]
    for (a, b) in ayak:
        o.append(f'<path d="M{nok(a)} L{nok(b)}" stroke="{renk}" stroke-width="{f(h * .028)}" stroke-linecap="round"/>')
    # kafes örgü
    n = 7
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        la = (ayak[0][0][0] + (ayak[0][1][0] - ayak[0][0][0]) * t0, y + (ust_y + h * .1 - y) * t0)
        lb = (ayak[0][0][0] + (ayak[0][1][0] - ayak[0][0][0]) * t1, y + (ust_y + h * .1 - y) * t1)
        ra = (ayak[1][0][0] + (ayak[1][1][0] - ayak[1][0][0]) * t0, y + (ust_y + h * .1 - y) * t0)
        rb = (ayak[1][0][0] + (ayak[1][1][0] - ayak[1][0][0]) * t1, y + (ust_y + h * .1 - y) * t1)
        o.append(f'<path d="M{nok(la)} L{nok(rb)} M{nok(ra)} L{nok(lb)} M{nok(la)} L{nok(ra)}" stroke="{koyu(renk, .2)}" stroke-width="{f(h * .01)}"/>')
    # arka payanda
    o.append(f'<path d="M{f(x + w * .16)} {f(ust_y + h * .14)} L{f(x + w * 1.25)} {f(y)}" stroke="{koyu(renk, .1)}" stroke-width="{f(h * .022)}"/>')
    # üst platform + çarklar
    o.append(f'<rect x="{f(x - w * .3)}" y="{f(ust_y + h * .06)}" width="{f(w * .6)}" height="{f(h * .05)}" fill="{koyu(renk, .25)}"/>')
    for k, cx in enumerate((x - w * .14, x + w * .14)):
        cy = ust_y + h * .02 + k * h * .03
        R = h * .1
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R)}" fill="none" stroke="{OBS_}" stroke-width="{f(h * .016)}"/>')
        for a in range(6):
            aa = a * math.pi / 3 + k * .3
            o.append(f'<path d="M{f(cx)} {f(cy)} L{f(cx + R * math.cos(aa))} {f(cy + R * math.sin(aa))}" stroke="{OBS_}" stroke-width="{f(h * .007)}"/>')
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(h * .02)}" fill="{OBS_}"/>')
        o.append(f'<path d="M{f(cx + R)} {f(cy)} L{f(x + w * 1.4)} {f(y - h * .16)}" stroke="#2A2E3A" stroke-width="{f(h * .006)}"/>')
    # kuyu ağzı binası
    o.append(f'<rect x="{f(x - w * .7)}" y="{f(y - h * .16)}" width="{f(w * 1.4)}" height="{f(h * .16)}" fill="#D8CDB8" stroke="{koyu("#D8CDB8", .45)}" stroke-width="{f(h * .006)}"/>')
    o.append(f'<path d="M{f(x - w * .78)} {f(y - h * .16)} L{f(x)} {f(y - h * .23)} L{f(x + w * .78)} {f(y - h * .16)} Z" fill="#7E8A93"/>')
    for k in range(3):
        o.append(f'<rect x="{f(x - w * .55 + k * w * .42)}" y="{f(y - h * .12)}" width="{f(w * .2)}" height="{f(h * .06)}" fill="#5B6F86"/>')
    return "".join(o)


OBS_ = "#1B1D26"


def vagon(s, x, y, w, tohum=1, govde="#5A6470"):
    """Kömür vagonu (maden arabası). (x, y) ray üstü sol."""
    r = RNG(tohum)
    o = f'<path d="M{f(x)} {f(y - w * .55)} H{f(x + w)} L{f(x + w * .9)} {f(y - w * .1)} H{f(x + w * .1)} Z" fill="{govde}" stroke="{OBS_}" stroke-width="3"/>'
    o += f'<path d="M{f(x + w * .05)} {f(y - w * .42)} H{f(x + w * .95)}" stroke="{acik(govde, .25)}" stroke-width="3"/>'
    for k in range(9):
        cx = x + w * (.12 + .76 * r.random())
        o += f'<circle cx="{f(cx)}" cy="{f(y - w * .58 - r.uniform(0, w * .12))}" r="{f(w * r.uniform(.06, .1))}" fill="#22252B"/>'
    for cx in (x + w * .25, x + w * .75):
        o += f'<circle cx="{f(cx)}" cy="{f(y - w * .07)}" r="{f(w * .09)}" fill="#3A3F4B" stroke="{OBS_}" stroke-width="2.4"/>'
    return o


def ray(x0, x1, y, k=1.0):
    o = ""
    for i in range(int((x1 - x0) / (28 * k))):
        xx = x0 + i * 28 * k
        o += f'<rect x="{f(xx)}" y="{f(y - 2)}" width="{f(16 * k)}" height="{f(7 * k)}" fill="#6B4A2E"/>'
    o += f'<path d="M{f(x0)} {f(y)} H{f(x1)}" stroke="#56636E" stroke-width="{f(4 * k)}"/>'
    return o


def havalandirma_binasi(s, x, y, w, h, tohum=1):
    """Havalandırma (vantilatör) binası: büyük ızgaralı pervane yuvası + hava kanalı."""
    o = f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="#E4DCCB" stroke="#9C9077" stroke-width="3"/>'
    o += f'<path d="M{f(x - w * .04)} {f(y - h)} H{f(x + w * 1.04)} L{f(x + w * .9)} {f(y - h * 1.18)} H{f(x + w * .1)} Z" fill="#7E8A93"/>'
    cx, cy, R = x + w * .5, y - h * .48, h * .34
    o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R)}" fill="#4F5B66" stroke="{OBS_}" stroke-width="3"/>'
    for a in range(5):
        aa = a * 2 * math.pi / 5
        p1 = (cx + R * .85 * math.cos(aa), cy + R * .85 * math.sin(aa))
        p2 = (cx + R * .85 * math.cos(aa + .7), cy + R * .85 * math.sin(aa + .7))
        o += f'<path d="M{f(cx)} {f(cy)} Q{nok(p1)} {nok(p2)} Z" fill="#B8C3CC"/>'
    for k in range(4):
        o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R * (.3 + .23 * k))}" fill="none" stroke="#2A2E3A" stroke-width="2"/>'
    o += f'<rect x="{f(x + w)}" y="{f(y - h * .7)}" width="{f(w * .5)}" height="{f(h * .26)}" fill="#A9B4BC" stroke="#6E7F8A" stroke-width="3"/>'
    # temiz hava okları
    for k in range(3):
        yy = y - h * (.88 - k * .1)
        o += f'<path d="M{f(x + w * 1.6)} {f(yy)} q30 -10 60 0 t60 0" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round" opacity=".85"/>'
    return o


def yuksek_firin(s, x, y, h, tohum=1):
    """Yüksek fırın (temsilî): gövde, tepe kubbesi, iniş boruları, yanında rüzgâr ısıtıcı kuleleri."""
    o = []
    w = h * .22
    gv = s.lin([(0, "#8C4A3A"), (.5, "#6E3A2E"), (1, "#3E2420")], 0, 0, 1, 0, ad="yf")
    kule = s.lin([(0, "#B8C3CC"), (.5, "#8FA3AD"), (1, "#5A6B76")], 0, 0, 1, 0, ad="kl")
    for k in range(3):     # ısıtıcı kuleler (sağda)
        kx = x + w * (1.1 + k * .55)
        kh = h * (.72 - k * .04)
        o.append(f'<rect x="{f(kx)}" y="{f(y - kh)}" width="{f(w * .45)}" height="{f(kh)}" fill="{kule}" stroke="{OBS_}" stroke-width="2.4"/>')
        o.append(f'<path d="M{f(kx)} {f(y - kh)} Q{f(kx + w * .225)} {f(y - kh - w * .3)} {f(kx + w * .45)} {f(y - kh)} Z" fill="{kule}" stroke="{OBS_}" stroke-width="2.4"/>')
    o.append(f'<path d="M{f(x - w / 2)} {f(y)} L{f(x - w * .42)} {f(y - h * .7)} Q{f(x)} {f(y - h * .82)} {f(x + w * .42)} {f(y - h * .7)} L{f(x + w / 2)} {f(y)} Z" fill="{gv}" stroke="{OBS_}" stroke-width="3"/>')
    for k in range(5):
        yy = y - h * (.1 + k * .13)
        o.append(f'<path d="M{f(x - w * .47)} {f(yy)} H{f(x + w * .47)}" stroke="#2A1A16" stroke-width="3" opacity=".6"/>')
    o.append(f'<rect x="{f(x - w * .12)}" y="{f(y - h)}" width="{f(w * .24)}" height="{f(h * .22)}" fill="#5A3A30" stroke="{OBS_}" stroke-width="2.4"/>')
    # iniş boruları
    o.append(f'<path d="M{f(x)} {f(y - h * .95)} Q{f(x + w * .9)} {f(y - h * 1.02)} {f(x + w * 1.2)} {f(y - h * .6)}" stroke="#3E2420" stroke-width="{f(w * .14)}" fill="none"/>')
    o.append(f'<path d="M{f(x)} {f(y - h * .95)} Q{f(x - w * .7)} {f(y - h * 1.0)} {f(x - w * .9)} {f(y - h * .55)}" stroke="#3E2420" stroke-width="{f(w * .12)}" fill="none"/>')
    # sıcak ağız ışığı
    sic = s.rad([(0, "#FFF2B0", .95), (.4, "#FF9A3D", .6), (1, "#FF7A3D", 0)], x, y - h * .12, w * .9, kull="userSpaceOnUse", ad="sic")
    o.append(f'<circle cx="{f(x)}" cy="{f(y - h * .12)}" r="{f(w * .9)}" fill="{sic}"/>')
    return "".join(o)


def buhar(s, x, y, n, tohum, boy=60, op=.85, renk="#FFFFFF"):
    """Yumuşak beyaz buhar (su buharı) kümeleri."""
    r = RNG(tohum)
    o = []
    for i in range(n):
        rr = boy * (.5 + i * .18) * r.uniform(.8, 1.15)
        o.append(f'<circle cx="{f(x + r.uniform(-.3, .9) * rr * i * .5)}" cy="{f(y - i * boy * .55)}" r="{f(rr)}" fill="{renk}" opacity="{f(op * (1 - i / (n + 1)), 2)}"/>')
    return "".join(o)


def pota(s, x, y, r, egim=38, tohum=1):
    """Erimiş metal kepçesi (pota): kepçe eğik, ağızdan akkor metal iner; (x, y) kepçe merkezi."""
    o = []
    ic = s.rad([(0, "#FFFBE0"), (.35, "#FFD45A"), (.8, "#FF8A2A"), (1, "#E2531D")], .5, .4, .7, ad="ak")
    o.append(f'<g transform="rotate({egim} {f(x)} {f(y)})">'
             f'<path d="M{f(x - r)} {f(y - r * .8)} H{f(x + r)} L{f(x + r * .82)} {f(y + r * .8)} Q{f(x)} {f(y + r * 1.05)} {f(x - r * .82)} {f(y + r * .8)} Z" fill="#3A3F4B" stroke="{OBS_}" stroke-width="4"/>'
             f'<ellipse cx="{f(x)}" cy="{f(y - r * .8)}" rx="{f(r)}" ry="{f(r * .22)}" fill="{ic}" stroke="{OBS_}" stroke-width="3"/>'
             f'<path d="M{f(x - r * 1.08)} {f(y - r * .2)} h{f(r * 2.16)}" stroke="#56636E" stroke-width="{f(r * .12)}"/>'
             f'</g>')
    # akış
    a = math.radians(egim)
    ux, uy = x + r * math.cos(a) + .8 * r * math.sin(a), y + r * math.sin(a) - .8 * r * math.cos(a)
    akis = s.lin([(0, "#FFF6C8"), (.5, "#FFC23A"), (1, "#FF6A1A")], 0, 0, 1, 0, ad="aks")
    o.append(f'<path d="M{f(ux - 6)} {f(uy)} C{f(ux + r * .5)} {f(uy + r * .2)} {f(ux + r * .55)} {f(uy + r * 1.1)} {f(ux + r * .5)} {f(y + r * 2.4)} '
             f'L{f(ux + r * .2)} {f(y + r * 2.4)} C{f(ux + r * .25)} {f(uy + r * 1.1)} {f(ux + r * .2)} {f(uy + r * .5)} {f(ux - 6)} {f(uy + r * .2)} Z" fill="{akis}"/>')
    hale = s.rad([(0, "#FFE08A", .75), (.5, "#FF9A3D", .25), (1, "#FF7A3D", 0)], ux + r * .4, y + r * 2.3, r * 2, kull="userSpaceOnUse", ad="hl")
    o.append(f'<circle cx="{f(ux + r * .4)}" cy="{f(y + r * 2.3)}" r="{f(r * 2)}" fill="{hale}"/>')
    rr = RNG(tohum)
    for k in range(34):
        aa = rr.uniform(-math.pi * .95, -math.pi * .05)
        d = rr.uniform(r * .3, r * 1.9)
        px, py = ux + r * .4 + d * math.cos(aa), y + r * 2.3 + d * math.sin(aa)
        o.append(f'<path d="M{f(px)} {f(py)} l{f(math.cos(aa) * 10)} {f(math.sin(aa) * 10)}" stroke="{rr.choice(["#FFE08A", "#FFB23A", "#FFFFFF"])}" stroke-width="3" stroke-linecap="round"/>')
    return "".join(o)


def sb_ev(s, x, y, w, h, tohum, isik=-1, cumba=True, kat=2, cati=KIREMIT, siva=SIVA, tas="#D9CCB4", baca=True, duman=False):
    """Safranbolu evi (temsilî): taş zemin kat, çıkmalı beyaz sıvalı üst kat(lar), ahşap çatkı, sık pencere, kiremit kırma çatı.
    (x, y) sol alt. w genişlik, h toplam duvar yüksekliği (çatısız)."""
    r = RNG(tohum)
    o = []
    zk = h * .32
    o.append(f'<rect x="{f(x)}" y="{f(y - zk)}" width="{f(w)}" height="{f(zk)}" fill="{tas}" stroke="{koyu(tas, .35)}" stroke-width="2"/>')
    for k in range(int(w / 18)):
        o.append(f'<path d="M{f(x + 6 + k * 18 + r.uniform(-3, 3))} {f(y - zk + r.uniform(6, zk - 6))} h{f(r.uniform(6, 12))}" stroke="{koyu(tas, .25)}" stroke-width="1.6" opacity=".6"/>')
    o.append(f'<path d="M{f(x + w * .14)} {f(y)} V{f(y - zk * .72)} Q{f(x + w * .22)} {f(y - zk * .9)} {f(x + w * .3)} {f(y - zk * .72)} V{f(y)} Z" fill="{AHSAP}"/>')
    cx0, cx1 = x - w * .06, x + w * 1.06
    ust_h = (h - zk) / kat
    for k_ in range(kat):
        yb = y - zk - k_ * ust_h
        o.append(f'<rect x="{f(cx0)}" y="{f(yb - ust_h)}" width="{f(cx1 - cx0)}" height="{f(ust_h)}" fill="{siva}" stroke="{AHSAP}" stroke-width="3"/>')
        o.append(f'<path d="M{f(cx0)} {f(yb)} H{f(cx1)}" stroke="{AHSAP}" stroke-width="5"/>')
        # çatkı: dikmeler + çaprazlar
        n = max(3, int((cx1 - cx0) / 34))
        for i in range(n + 1):
            xx = cx0 + (cx1 - cx0) * i / n
            o.append(f'<path d="M{f(xx)} {f(yb)} V{f(yb - ust_h)}" stroke="{AHSAP}" stroke-width="2.6"/>')
        # pencereler (sık, ahşap kepenkli)
        pw = (cx1 - cx0) / n
        for i in range(n):
            if r.random() < .2 and n > 4:
                xa = cx0 + pw * i
                o.append(f'<path d="M{f(xa)} {f(yb)} L{f(xa + pw)} {f(yb - ust_h)}" stroke="{AHSAP}" stroke-width="2"/>')
                continue
            px = cx0 + pw * i + pw * .22
            o.append(f'<rect x="{f(px)}" y="{f(yb - ust_h * .78)}" width="{f(pw * .56)}" height="{f(ust_h * .56)}" fill="#3E4A5C" stroke="{AHSAP}" stroke-width="2.4"/>')
            o.append(f'<path d="M{f(px + pw * .28)} {f(yb - ust_h * .78)} V{f(yb - ust_h * .22)}" stroke="{AHSAP}" stroke-width="1.8"/>')
            if r.random() < .45:
                o.append(f'<rect x="{f(px + 2)}" y="{f(yb - ust_h * .76)}" width="{f(pw * .52)}" height="{f(ust_h * .2)}" fill="#FFE7A8" opacity=".55"/>')
    # cumba (çıkma pencere kutusu)
    if cumba:
        yb = y - zk - (kat - 1) * ust_h
        cw = w * .34
        cxm = x + w * (.55 if r.random() < .5 else .3)
        o.append(f'<path d="M{f(cxm)} {f(yb - ust_h * .08)} H{f(cxm + cw)} V{f(yb - ust_h * .92)} H{f(cxm)} Z" fill="{acik(siva, .3)}" stroke="{AHSAP}" stroke-width="3.4"/>')
        o.append(f'<path d="M{f(cxm)} {f(yb - ust_h * .08)} L{f(cxm + cw * .1)} {f(yb + ust_h * .14)} H{f(cxm + cw * .9)} L{f(cxm + cw)} {f(yb - ust_h * .08)}" fill="{AHSAP}"/>')
        for i in range(3):
            o.append(f'<rect x="{f(cxm + cw * (.08 + i * .3))}" y="{f(yb - ust_h * .78)}" width="{f(cw * .24)}" height="{f(ust_h * .5)}" fill="#3E4A5C" stroke="{AHSAP}" stroke-width="2"/>')
    # gölge yüzü
    gx = x + w * .62 if isik < 0 else cx0
    o.append(f'<rect x="{f(gx)}" y="{f(y - h)}" width="{f(w * .44)}" height="{f(h)}" fill="#0B1E2E" opacity=".1"/>')
    # kırma çatı
    ty = y - h
    sacak = w * .14
    tep = ty - h * .34
    o.append(f'<path d="M{f(cx0 - sacak)} {f(ty + 4)} L{f(x + w * .28)} {f(tep)} H{f(x + w * .72)} L{f(cx1 + sacak)} {f(ty + 4)} Z" fill="{cati}" stroke="{koyu(cati, .35)}" stroke-width="2.4"/>')
    o.append(f'<path d="M{f(x + w * .72)} {f(tep)} L{f(cx1 + sacak)} {f(ty + 4)} H{f(x + w * .62)} Z" fill="{koyu(cati, .22)}" opacity=".7"/>')
    xl0, xr0, xl1, xr1 = x + w * .28, x + w * .72, cx0 - sacak, cx1 + sacak
    for k in range(4):
        t = (k + 1) / 5
        yy = tep + (ty + 4 - tep) * t
        o.append(f'<path d="M{f(xl0 + (xl1 - xl0) * t)} {f(yy)} H{f(xr0 + (xr1 - xr0) * t)}" stroke="{koyu(cati, .3)}" stroke-width="1.6" opacity=".55"/>')
    o.append(f'<path d="M{f(cx0 - sacak)} {f(ty + 4)} H{f(cx1 + sacak)}" stroke="{koyu(cati, .45)}" stroke-width="4"/>')
    if baca:
        bx = x + w * (.3 if r.random() < .5 else .66)
        o.append(f'<rect x="{f(bx)}" y="{f(tep - h * .12)}" width="{f(w * .07)}" height="{f(h * .2)}" fill="#E6DCCB" stroke="{koyu(tas, .4)}" stroke-width="2"/>')
        if duman:
            o.append(buhar(s, bx + w * .035, tep - h * .16, 4, tohum + 3, boy=h * .07, op=.6, renk="#EEF2F5"))
    return "".join(o)


def kasaba(s, x0, x1, y, n, tohum, olcek=1.0, egim=0.0, renkler=(SIVA, "#FBF6EC", "#F2EADB"), isik=-1):
    """Yamaçta Safranbolu evleri kümesi (arkadan öne)."""
    r = RNG(tohum)
    o = []
    for i in range(n):
        t = i / max(1, n - 1)
        x = x0 + (x1 - x0) * t + r.uniform(-12, 12) * olcek
        yy = y + egim * (x - x0) + r.uniform(-8, 8) * olcek
        w = r.uniform(70, 110) * olcek
        h = r.uniform(76, 110) * olcek
        o.append(sb_ev(s, x, yy, w, h, tohum * 13 + i, isik=isik, cumba=r.random() < .5, kat=r.choice([1, 2, 2]), siva=r.choice(renkler)))
    return "".join(o)


def camasirhane(s, x, y, w, h, tohum=1):
    """Tarihî köy çamaşırhanesi (temsilî): moloz taş duvar, kemerli ocak ağızları, büyük baca."""
    r = RNG(tohum)
    o = []
    tas = s.lin([(0, "#D9C9A8"), (1, "#B9A27E")], 0, y - h, 0, y, kull="userSpaceOnUse", ad="ct")
    o.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{tas}" stroke="#7E6A4E" stroke-width="3"/>')
    for k in range(int(w * h / 900)):
        px, py = x + r.uniform(6, w - 20), y - r.uniform(8, h - 8)
        o.append(f'<path d="M{f(px)} {f(py)} q{f(r.uniform(6, 10))} {f(-r.uniform(2, 5))} {f(r.uniform(12, 20))} 0" stroke="#8C7656" stroke-width="1.8" fill="none" opacity=".55"/>')
    # kemerli ocaklar
    for k in range(3):
        ax = x + w * (.12 + k * .28)
        aw = w * .2
        o.append(f'<path d="M{f(ax)} {f(y)} V{f(y - h * .45)} Q{f(ax + aw / 2)} {f(y - h * .75)} {f(ax + aw)} {f(y - h * .45)} V{f(y)} Z" fill="#3A2A20"/>')
        at = s.rad([(0, "#FFE08A"), (.6, "#FF8A3D", .7), (1, "#FF5C1A", 0)], ax + aw / 2, y - h * .12, aw * .8, kull="userSpaceOnUse", ad="at")
        o.append(f'<ellipse cx="{f(ax + aw / 2)}" cy="{f(y - h * .12)}" rx="{f(aw * .5)}" ry="{f(h * .2)}" fill="{at}"/>')
        o.append(f'<path d="M{f(ax)} {f(y - h * .45)} Q{f(ax + aw / 2)} {f(y - h * .75)} {f(ax + aw)} {f(y - h * .45)}" stroke="#E6D6B6" stroke-width="5" fill="none"/>')
    # çatı + baca
    o.append(f'<path d="M{f(x - w * .05)} {f(y - h)} L{f(x + w * .2)} {f(y - h * 1.32)} H{f(x + w * .8)} L{f(x + w * 1.05)} {f(y - h)} Z" fill="{KIREMIT}" stroke="{koyu(KIREMIT, .35)}" stroke-width="2.4"/>')
    bx = x + w * .62
    o.append(f'<rect x="{f(bx)}" y="{f(y - h * 1.6)}" width="{f(w * .1)}" height="{f(h * .4)}" fill="#C9B48E" stroke="#7E6A4E" stroke-width="2.4"/>')
    o.append(buhar(s, bx + w * .05, y - h * 1.66, 5, tohum + 9, boy=h * .1, op=.7, renk="#F4F1EA"))
    return "".join(o)


def camasir_ipi(s, x0, x1, y, tohum, sarkma=26):
    r = RNG(tohum)
    o = [f'<path d="M{f(x0)} {f(y)} Q{f((x0 + x1) / 2)} {f(y + sarkma * 2)} {f(x1)} {f(y)}" stroke="#4A3424" stroke-width="2.4" fill="none"/>']
    n = int((x1 - x0) / 46)
    renk = ["#E2533D", "#13A3A6", "#F0A21A", "#2B50B5", "#FFFFFF", "#7B3F8C", "#1F8A5B", "#FF5C8A"]
    for i in range(n):
        t = (i + .5) / n
        x = x0 + (x1 - x0) * t
        yy = y + sarkma * 2 * 2 * t * (1 - t)
        c = r.choice(renk)
        if r.random() < .5:   # gömlek
            o.append(f'<path d="M{f(x - 16)} {f(yy)} H{f(x + 16)} L{f(x + 22)} {f(yy + 12)} L{f(x + 14)} {f(yy + 15)} V{f(yy + 40)} H{f(x - 14)} V{f(yy + 15)} L{f(x - 22)} {f(yy + 12)} Z" fill="{c}" stroke="{OBS_}" stroke-width="1.8"/>')
        else:                 # örtü (kilim desenli)
            o.append(f'<rect x="{f(x - 16)}" y="{f(yy)}" width="32" height="44" fill="{c}" stroke="{OBS_}" stroke-width="1.8"/>'
                     f'<path d="M{f(x - 16)} {f(yy + 14)} h32 M{f(x - 16)} {f(yy + 30)} h32" stroke="{r.choice(renk)}" stroke-width="4"/>')
        o.append(f'<rect x="{f(x - 3)}" y="{f(yy - 5)}" width="6" height="9" fill="#9A6B42"/>')
    return "".join(o)


def kazan(s, x, y, r):
    """Bakır kazan (ocak üstünde)."""
    b = s.lin([(0, "#F2B27A"), (.5, "#C8742F"), (1, "#7E4219")], 0, 0, 1, 0, ad="kz")
    return (f'<path d="M{f(x - r)} {f(y - r * .9)} H{f(x + r)} Q{f(x + r * 1.02)} {f(y)} {f(x)} {f(y + r * .1)} Q{f(x - r * 1.02)} {f(y)} {f(x - r)} {f(y - r * .9)} Z" fill="{b}" stroke="{OBS_}" stroke-width="3"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y - r * .9)}" rx="{f(r)}" ry="{f(r * .18)}" fill="#7FD3CF" stroke="{OBS_}" stroke-width="3"/>'
            + buhar(s, x, y - r * 1.1, 4, int(x), boy=r * .28, op=.75, renk="#FFFFFF"))


def burc(s, x, y, w, h, tas=TAS, isik=-1, pencere=True, yuvarlak=False):
    """Kale burcu (kare ya da yarım yuvarlak). (x, y) taban ortası."""
    g = s.lin([(0, acik(tas, .18)), (.55, tas), (1, koyu(tas, .28))], 0, 0, 1, 0, ad="bc") if isik < 0 else \
        s.lin([(0, koyu(tas, .28)), (.45, tas), (1, acik(tas, .18))], 0, 0, 1, 0, ad="bc")
    o = f'<rect x="{f(x - w / 2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" rx="{f(w * .5 if yuvarlak else w * .04)}" fill="{g}" stroke="{koyu(tas, .5)}" stroke-width="2.4"/>' if yuvarlak else \
        f'<rect x="{f(x - w / 2)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{g}" stroke="{koyu(tas, .5)}" stroke-width="2.4"/>'
    n = max(3, int(w / 22))
    for k in range(n):
        if k % 2 == 0:
            o += f'<rect x="{f(x - w / 2 + k * w / n)}" y="{f(y - h - w * .16)}" width="{f(w / n)}" height="{f(w * .17)}" fill="{tas}" stroke="{koyu(tas, .5)}" stroke-width="2"/>'
    for k in range(int(h / 26)):
        o += f'<path d="M{f(x - w / 2)} {f(y - h + 18 + k * 26)} h{f(w)}" stroke="{koyu(tas, .3)}" stroke-width="1.4" opacity=".45"/>'
    if pencere:
        o += f'<rect x="{f(x - w * .07)}" y="{f(y - h * .7)}" width="{f(w * .14)}" height="{f(h * .16)}" rx="{f(w * .07)}" fill="#2A2420"/>'
    return o


def surlar(s, pts, h, tohum, tas=TAS, isik=-1, burc_her=3, burc_h=1.5):
    """Sırt boyunca sur: pts (x, y) zemin çizgisi; her `burc_her` noktada bir burç."""
    o = []
    ust = [(x, y - h) for x, y in pts]
    poly = pts + list(reversed(ust))
    g = s.lin([(0, acik(tas, .12)), (1, koyu(tas, .12))], 0, 0, 0, 1, ad="sr")
    o.append(f'<path d="{cizgi_d(poly, True)}" fill="{g}" stroke="{koyu(tas, .5)}" stroke-width="2.4"/>')
    for i in range(len(ust) - 1):
        (xa, ya), (xb, yb) = ust[i], ust[i + 1]
        n = max(1, int(abs(xb - xa) / 16))
        for k in range(n):
            if k % 2 == 0:
                t0, t1 = k / n, (k + 1) / n
                xx0, yy0 = xa + (xb - xa) * t0, ya + (yb - ya) * t0
                xx1 = xa + (xb - xa) * t1
                o.append(f'<rect x="{f(xx0)}" y="{f(yy0 - h * .16)}" width="{f(xx1 - xx0)}" height="{f(h * .17)}" fill="{tas}" stroke="{koyu(tas, .5)}" stroke-width="1.6"/>')
    r = RNG(tohum)
    for k in range(int(len(pts) * h / 30)):
        i = r.randrange(len(pts) - 1)
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        t = r.random()
        o.append(f'<path d="M{f(xa + (xb - xa) * t)} {f(ya + (yb - ya) * t - r.uniform(6, h - 8))} h{f(r.uniform(8, 16))}" stroke="{koyu(tas, .35)}" stroke-width="1.5" opacity=".5"/>')
    for i in range(0, len(pts), burc_her):
        x, y = pts[i]
        o.append(burc(s, x, y + 2, h * .9, h * burc_h, tas, isik, yuvarlak=(i // burc_her) % 2 == 1))
    return "".join(o)


def kemer_kopru(s, x0, x1, y, h, n=2, tas=TAS):
    """Taş kemer köprü: y tabliye üst kenarı, h kemer yüksekliği."""
    o = []
    g = s.lin([(0, acik(tas, .1)), (1, koyu(tas, .25))], 0, y, 0, y + h * 1.4, kull="userSpaceOnUse", ad="kp")
    d = f"M{f(x0)} {f(y)} H{f(x1)} V{f(y + h * 1.4)}"
    aw = (x1 - x0) / n
    for k in reversed(range(n)):
        a0 = x0 + k * aw + aw * .14
        a1 = x0 + (k + 1) * aw - aw * .14
        d += f" H{f(a1)} V{f(y + h * .7)} Q{f((a0 + a1) / 2)} {f(y + h * .02)} {f(a0)} {f(y + h * .7)} V{f(y + h * 1.4)}"
    d += f" H{f(x0)} Z"
    o.append(f'<path d="{d}" fill="{g}" stroke="{koyu(tas, .5)}" stroke-width="3"/>')
    o.append(f'<path d="M{f(x0 - 6)} {f(y)} H{f(x1 + 6)}" stroke="{koyu(tas, .45)}" stroke-width="7"/>')
    for k in range(int((x1 - x0) / 22)):
        o.append(f'<rect x="{f(x0 + k * 22)}" y="{f(y - 16)}" width="11" height="16" fill="{tas}" stroke="{koyu(tas, .45)}" stroke-width="1.6"/>')
    return "".join(o)


def lav_sutunlari(s, x0, x1, y, tohum, boy=(60, 210), en=48, renk="#5B6470", isik=-1):
    """Güzelcehisar bazalt (lav) sütunları: altıgen prizmalar, basamak basamak; (x0..x1) taban y."""
    r = RNG(tohum)
    o = []
    n = int((x1 - x0) / (en * .92))
    for i in range(n):
        x = x0 + i * en * .92 + r.uniform(-4, 4)
        hh = r.uniform(*boy) * (1 - .45 * abs(i / max(1, n - 1) - .55))
        yt = y - hh
        a = en / 2
        ust = [(x - a, yt), (x - a * .5, yt - a * .32), (x + a * .5, yt - a * .32), (x + a, yt), (x + a * .5, yt + a * .32), (x - a * .5, yt + a * .32)]
        on = [(x - a, yt), (x - a * .5, yt + a * .32), (x - a * .5, y), (x - a, y - 4)]
        on2 = [(x - a * .5, yt + a * .32), (x + a * .5, yt + a * .32), (x + a * .5, y), (x - a * .5, y)]
        on3 = [(x + a * .5, yt + a * .32), (x + a, yt), (x + a, y - 4), (x + a * .5, y)]
        tonlar = (acik(renk, .12), renk, koyu(renk, .3)) if isik < 0 else (koyu(renk, .3), renk, acik(renk, .12))
        for poly, c in ((on, tonlar[0]), (on2, tonlar[1]), (on3, tonlar[2])):
            o.append(f'<path d="{cizgi_d(poly, True)}" fill="{c}" stroke="#2A2E36" stroke-width="2"/>')
        o.append(f'<path d="{cizgi_d(ust, True)}" fill="{acik(renk, .35)}" stroke="#2A2E36" stroke-width="2"/>')
        for k in range(int(hh / 50)):
            yy = yt + 40 + k * 50 + r.uniform(-6, 6)
            o.append(f'<path d="M{f(x - a * .5)} {f(yy)} h{f(a)}" stroke="#2A2E36" stroke-width="1.6" opacity=".6"/>')
    return "".join(o)


def kasik(x, y, o=1.0, aci=0, renk="#C9955E"):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({aci}) scale({f(o, 3)})"><ellipse cx="0" cy="-34" rx="9" ry="13" fill="{renk}" stroke="{OBS_}" stroke-width="2"/>'
            f'<rect x="-2.6" y="-22" width="5.2" height="40" rx="2.6" fill="{renk}" stroke="{OBS_}" stroke-width="2"/></g>')


def dukkan(s, x, y, w, h, tohum, tente="#C8442F"):
    """Çekiciler Çarşısı esinli küçük ahşap dükkân: tente, raf, oyma kaşıklar, tepsiler."""
    r = RNG(tohum)
    o = []
    ah = s.lin([(0, "#C99566"), (1, "#8C5E36")], 0, y - h, 0, y, kull="userSpaceOnUse", ad="dk")
    o.append(f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{ah}" stroke="{OBS_}" stroke-width="3"/>')
    o.append(f'<rect x="{f(x + w * .08)}" y="{f(y - h * .78)}" width="{f(w * .84)}" height="{f(h * .62)}" fill="#3A2A20"/>')
    for k in range(2):
        yy = y - h * (.55 - k * .26)
        o.append(f'<path d="M{f(x + w * .08)} {f(yy)} h{f(w * .84)}" stroke="#C99566" stroke-width="5"/>')
        for j in range(int(w * .84 / 26)):
            if r.random() < .8:
                o.append(kasik(x + w * .14 + j * 26, yy - 4, .7, r.uniform(-8, 8), r.choice(["#E2B88A", "#C9955E", "#A8743F"])))
    # tepsi
    o.append(f'<ellipse cx="{f(x + w * .5)}" cy="{f(y - h * .1)}" rx="{f(w * .3)}" ry="{f(h * .05)}" fill="#D9A86A" stroke="{OBS_}" stroke-width="2"/>')
    # tente (şeritli)
    o.append(f'<path d="M{f(x - w * .06)} {f(y - h)} H{f(x + w * 1.06)} L{f(x + w * .96)} {f(y - h * 1.22)} H{f(x + w * .04)} Z" fill="{tente}" stroke="{OBS_}" stroke-width="3"/>')
    for k in range(5):
        xx = x + w * (.1 + k * .2)
        o.append(f'<path d="M{f(xx)} {f(y - h)} L{f(xx + w * .02)} {f(y - h * 1.22)}" stroke="#FFFFFF" stroke-width="{f(w * .07)}" opacity=".85"/>')
    o.append(f'<path d="M{f(x - w * .06)} {f(y - h)} q{f(w * .09)} {f(h * .1)} {f(w * .18)} 0 t{f(w * .18)} 0 t{f(w * .18)} 0 t{f(w * .18)} 0 t{f(w * .18)} 0 t{f(w * .18)} 0" fill="{tente}" stroke="{OBS_}" stroke-width="2.4"/>')
    return "".join(o)


def isaret_diregi(s, x, y, simgeler, boy=74):
    """Direğe asılı güvenlik işaretleri (alt alta)."""
    o = f'<rect x="{f(x - 5)}" y="{f(y - len(simgeler) * (boy + 10) - 20)}" width="10" height="{f(len(simgeler) * (boy + 10) + 20)}" fill="#8FA3AD" stroke="{OBS_}" stroke-width="2"/>'
    for i, sm in enumerate(simgeler):
        yy = y - (i + 1) * (boy + 10) - 10
        o += f'<rect x="{f(x - boy / 2 - 6)}" y="{f(yy - 6)}" width="{f(boy + 12)}" height="{f(boy + 12)}" rx="6" fill="#FFFFFF" stroke="{OBS_}" stroke-width="2.4"/>'
        o += IU.isaret_g(sm, x - boy / 2, yy, boy)
    return o


def _karakter(ad, x, y, w):
    vb = (140, 160) if ad.startswith("pamuk") else (200, 210)
    return f'<use href="#{ad}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(w * vb[1] / vb[0])}"/>'


# ================================================================== 1. DURAK · ZONGULDAK (sabah)

def zonguldak():
    s = Svg("kg-zon")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#4C70C0"), (.4, "#A39ED6"), (.7, "#F7B8C2"), (1, "#FFE2C2")])
    s += S.gunes(s, 1180, 200, 36, cekirdek="#FFF9EA", hale="#FFD9A6", hale_r=420, guc=.9)
    for i, (x, y, w_) in enumerate([(700, 110, 230), (1560, 80, 250), (1920, 150, 180)]):
        s += S.bulut(s, x, y, w_, 30 + i, ust="#FFFFFF", alt="#F3C9D4", op=.92)
    s += deniz(s, 0, ufuk, W, H - ufuk, 31, gunes_x=1180)
    # kıyı ormanlı tepeler (sağdan sola alçalır)
    s += orman_sirti(s, 900, 2140, ufuk + 6, 120, 32, "#4E8A55", "#2F6B3F", olcek=.8)[0]
    s += orman_sirti(s, 1250, 2140, ufuk + 60, 90, 33, "#3B7D47", "#2A5E3A", olcek=1.0)[0]
    # liman kıyısı + kaya
    s += f'<path d="M1080 {ufuk + 120} C1300 {ufuk + 90} 1600 {ufuk + 96} 2100 {ufuk + 80} V{H} H1040 Z" fill="#6E8C54"/>'
    s += S.kaya(s, 1130, ufuk + 140, 120, 40, 34, renk="#6E6A72")
    # maden alanı: kuyu kulesi + havalandırma binası + raylar + vagonlar
    zem = s.lin([(0, "#8F8A7A"), (1, "#5E5A50")], 0, 360, 0, H, kull="userSpaceOnUse", ad="zm")
    s += f'<path d="M1300 380 C1500 360 1800 362 2100 352 V{H} H1240 Z" fill="{zem}"/>'
    s += havalandirma_binasi(s, 1360, 392, 150, 120, 35)
    s += kuyu_kulesi(s, 1760, 384, 300, tohum=36)
    s += f'<rect x="1880" y="300" width="170" height="86" fill="#E4DCCB" stroke="#9C9077" stroke-width="3"/><path d="M1872 300 L1965 262 L2058 300 Z" fill="#7E8A93"/>'
    for k in range(3):
        s += f'<rect x="{1898 + k * 50}" y="322" width="30" height="34" fill="#FFE7A8" opacity=".85"/>'
    s += ray(1300, 2100, 420)
    s += vagon(s, 1560, 418, 92, 37) + vagon(s, 1665, 418, 92, 38)
    # emniyet köşesi: direkte işaretler (baret zorunlu, açık alev yasak, ilk yardım)
    s += isaret_diregi(s, 2030, 452, ["ilkyardim", "alev_yok", "baret"], 66)
    s += _karakter("pamuk-otur", 1240, 352, 82)
    s += S.cimen(1040, 1300, 456, 39, renk="#4E7F3A", renk2="#7DB955", boy=12)
    for k, (x, y, o) in enumerate([(820, 160, .8), (900, 186, .55), (1020, 140, .6)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3F5C")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 2. DURAK · KARABÜK (öğle)

def karabuk():
    s = Svg("kg-kar")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2F86D6"), (.55, "#8FD0F0"), (1, "#E6F6FB")])
    s += S.gunes(s, 1250, 70, 34, hale="#FFF2C2", hale_r=330, guc=.8)
    for i, (x, y, w_) in enumerate([(820, 120, 240), (1500, 92, 220)]):
        s += S.bulut(s, x, y, w_, 40 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    # vadiyi saran ormanlı dağlar
    d, _ = S.dag(s, 700, 1700, ufuk + 6, 1180, 120, 41, renk="#6F9F7A", golge="#4F7E5E", bicim="tepe", sis="#CFE8E4", isik=-1, sirt=3, puruz=10)
    s += d
    d, _ = S.dag(s, 1450, 2300, ufuk + 6, 1900, 96, 42, renk="#5E9271", golge="#3F6F52", bicim="tepe", sis="#CFE8E4", isik=-1, sirt=3, puruz=12)
    s += d
    s += orman_sirti(s, -40, 2140, ufuk + 20, 60, 43, "#4F8A57", "#3B7D47", olcek=.7)[0]
    s += _zemin(s, ufuk + 60, "#7E8A80")
    # fabrika: yüksek fırın, bacalar (beyaz buhar), bantlar
    s += buhar(s, 1500, 140, 4, 44, boy=40, op=.8) + buhar(s, 1590, 120, 4, 45, boy=36, op=.75)
    for (x, h_) in ((1480, 190), (1572, 220)):
        s += f'<rect x="{x}" y="{ufuk + 60 - h_}" width="34" height="{h_}" fill="#B8C3CC" stroke="{OBS_}" stroke-width="2.4"/>'
        s += f'<path d="M{x} {ufuk + 76 - h_} h34 M{x} {ufuk + 96 - h_} h34" stroke="{MER}" stroke-width="8"/>'
    s += yuksek_firin(s, 1700, ufuk + 70, 250, 46)
    s += f'<rect x="1290" y="{ufuk - 4}" width="200" height="64" fill="#C9C2B2" stroke="#7E7768" stroke-width="3"/><path d="M1280 {ufuk - 4} L1390 {ufuk - 40} L1500 {ufuk - 4} Z" fill="#8FA3AD"/>'
    s += f'<path d="M1180 {ufuk + 50} L1480 {ufuk - 60}" stroke="#5A6B76" stroke-width="14"/><path d="M1180 {ufuk + 50} L1480 {ufuk - 60}" stroke="#8FA3AD" stroke-width="6"/>'
    # ön plan: döküm alanı, pota ve akkor metal
    zm = s.lin([(0, "#6E6A64"), (1, "#3E3A36")], 0, 380, 0, H, kull="userSpaceOnUse", ad="dz")
    s += f'<path d="M1180 392 C1400 380 1700 386 2100 374 V{H} H1150 Z" fill="{zm}"/>'
    s += f'<rect x="1820" y="300" width="22" height="100" fill="#5A6B76"/><path d="M1831 300 V250 H1990" stroke="#5A6B76" stroke-width="14" fill="none"/>'
    s += f'<path d="M1950 250 V282" stroke="#2A2E3A" stroke-width="5"/>'
    s += pota(s, 1950, 318, 52, 34, 47)
    s += f'<rect x="1880" y="432" width="160" height="26" fill="#3A3F4B" stroke="{OBS_}" stroke-width="3"/>'
    s += isaret_diregi(s, 1350, 456, ["baret", "sicak"], 62)
    s += _karakter("yusuf-anlatan", 1400, 300, 110)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 3. DURAK · SAFRANBOLU (ikindi)

def safranbolu():
    s = Svg("kg-saf")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "altin")
    s += S.gunes(s, 1060, 150, 38, cekirdek="#FFF7DC", hale="#FFD27A", hale_r=380, guc=.85)
    for i, (x, y, w_) in enumerate([(760, 110, 220), (1640, 80, 240)]):
        s += S.bulut(s, x, y, w_, 50 + i, ust="#FFFFFF", alt="#F6DDB8", op=.9)
    s += orman_sirti(s, -40, 2140, ufuk, 110, 51, "#7FA864", "#5E8F4E", olcek=.7, yuvarlak=.6)[0]
    s += orman_sirti(s, 600, 2140, ufuk + 60, 80, 52, "#6E9C55", "#4F8344", olcek=.8, yuvarlak=.6)[0]
    s += _zemin(s, ufuk + 120, "#6E9C55")
    # saat kulesi tepesi (Hıdırlık yönü, temsilî)
    s += f'<rect x="1290" y="{ufuk - 10}" width="34" height="70" fill="#EDE4D3" stroke="{AHSAP}" stroke-width="2.4"/><path d="M1284 {ufuk - 10} L1307 {ufuk - 46} L1330 {ufuk - 10} Z" fill="{KIREMIT}"/>'
    s += f'<circle cx="1307" cy="{ufuk + 8}" r="9" fill="#FFFFFF" stroke="{AHSAP}" stroke-width="2"/><path d="M1307 {ufuk + 8} v-6 M1307 {ufuk + 8} h5" stroke="{OBS_}" stroke-width="1.6"/>'
    # yamaçta evler (arkadan öne)
    s += kasaba(s, 1180, 2060, ufuk + 98, 9, 53, olcek=.62, egim=.02)
    s += kasaba(s, 1260, 2080, ufuk + 160, 7, 54, olcek=.8, egim=.03)
    # ön: büyük konak (odak) + taş sokak
    yol = s.lin([(0, "#CDBFA6"), (1, "#9C8C70")], 0, 400, 0, H, kull="userSpaceOnUse", ad="ts")
    s += f'<path d="M1200 {H} C1400 420 1700 412 2100 404 V{H} Z" fill="{yol}"/>'
    r = RNG(55)
    for k in range(70):
        x, y = r.uniform(1260, 2090), r.uniform(414, 456)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r.uniform(6, 11))}" ry="{f(r.uniform(3, 5))}" fill="#8C7C62" opacity=".55"/>'
    s += sb_ev(s, 1620, 430, 300, 250, 56, cumba=True, kat=2, duman=True)
    s += S.agac(s, 1540, 430, 46, 57, renk="#6CB04F")
    s += S.agac(s, 2040, 430, 40, 58, renk="#7DB955", meyve="#E2533D")
    s += _karakter("elif-soru", 1350, 300, 118)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 4. DURAK · YÖRÜK KÖYÜ (akşamüstü)

def yorukkoy():
    s = Svg("kg-yor")
    ufuk = 260
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3F4FA0"), (.35, "#9E78B8"), (.65, "#F59AA2"), (.85, "#FFC28A"), (1, "#FFE0A8")])
    s += S.gunes(s, 1180, ufuk - 40, 44, cekirdek="#FFF6E0", hale="#FFB07A", hale_r=520, guc=.9)
    s += S.bulut_serit(s, 700, 150, 480, 10, "#FFD9E0", "#F29AB4", .6)
    s += S.bulut_serit(s, 1500, 100, 420, 11, "#FFE0D8", "#F2A6BC", .55)
    s += orman_sirti(s, -40, 2140, ufuk + 10, 100, 62, "#8A7DA8", "#6F6896", olcek=.7, yuvarlak=.5)[0]
    s += orman_sirti(s, -40, 2140, ufuk + 70, 70, 63, "#5E8355", "#486F45", olcek=.85, yuvarlak=.5)[0]
    s += _zemin(s, ufuk + 120, "#5E7F48")
    s += kasaba(s, 1150, 1500, ufuk + 112, 4, 64, olcek=.6, egim=.04)
    for i, x in enumerate((1520, 1556, 2050, 2086)):
        s += S.kavak(s, x, ufuk + 140, 150, 26, 65 + i, renk="#4F8A45")
    # çamaşırhane (odak) + kazan + ipte çamaşırlar
    zm = s.lin([(0, "#B9A27E"), (1, "#7E6A4E")], 0, 400, 0, H, kull="userSpaceOnUse", ad="cz")
    s += f'<path d="M1180 {H} C1400 418 1700 404 2100 400 V{H} Z" fill="{zm}"/>'
    s += camasirhane(s, 1600, 420, 300, 150, 66)
    s += kazan(s, 1520, 446, 38)
    s += f'<path d="M1494 452 l-8 8 M1546 452 l8 8" stroke="{OBS_}" stroke-width="4"/>'
    s += camasir_ipi(s, 1930, 2100, 300, 67, 20)
    s += f'<path d="M1930 300 V430" stroke="#6B4A2E" stroke-width="7"/>'
    s += _karakter("pamuk-sasiran", 1300, 340, 92)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 5. DURAK · BARTIN OKUL LABORATUVARI (iç mekân, öğle)

def bartin_lab():
    s = Svg("kg-lab")
    duvar = s.lin([(0, "#EAF3F4"), (1, "#D6E6E8")], 0, 0, 0, 380, kull="userSpaceOnUse", ad="dv")
    s += f'<rect x="0" y="0" width="{W}" height="{H}" fill="{duvar}"/>'
    s += f'<rect x="0" y="0" width="{W}" height="18" fill="#C9DCDF"/>'
    # büyük pencere: Bartın Irmağı, ahşap evler, yeşil tepeler
    px0, py0, px1, py1 = 1580, 40, 1890, 290
    s += f'<rect x="{px0 - 16}" y="{py0 - 16}" width="{px1 - px0 + 32}" height="{py1 - py0 + 32}" rx="6" fill="#FFFFFF" stroke="#9FB3B8" stroke-width="4"/>'
    ic = S.gokyuzu(s, px0, py0, px1 - px0, 140, "gun")
    ic += S.bulut(s, px0 + 120, py0 + 50, 120, 70, op=.95)
    ic += orman_sirti(s, px0 - 20, px1 + 20, py0 + 140, 50, 71, "#4F8A57", "#3B7D47", olcek=.5)[0]
    ic += deniz(s, px0, py0 + 190, px1 - px0, py1 - py0 - 190, 72, renk=("#9FD9D6", "#3E9DA8", "#1F6B78"))
    ic += kasaba(s, px0 + 40, px1 - 60, py0 + 196, 6, 73, olcek=.42)
    ic += S.tekne(s, px0 + 330, py1 - 18, 60, govde="#C8442F")
    kl = s.klip(f'<rect x="{px0}" y="{py0}" width="{px1 - px0}" height="{py1 - py0}"/>', ad="pk")
    s += f'<g clip-path="{kl}">{ic}</g>'
    s += f'<path d="M{(px0 + px1) / 2} {py0} V{py1} M{px0} {(py0 + py1) / 2 - 20} H{px1}" stroke="#FFFFFF" stroke-width="10"/>'
    # çeker ocak (sağda)
    s += f'<rect x="1930" y="40" width="200" height="320" fill="#C9D3DB" stroke="#6E7F8A" stroke-width="4"/>'
    s += f'<rect x="1950" y="130" width="160" height="150" fill="#EAF6FF" opacity=".8" stroke="#6E7F8A" stroke-width="3"/><rect x="1950" y="210" width="160" height="12" fill="#8FA3AD"/>'
    s += f'<path d="M2030 40 V0" stroke="#8FA3AD" stroke-width="30"/>'
    s += buhar(s, 2030, 190, 3, 74, boy=16, op=.5, renk="#FFFFFF")
    # duvarda işaretler + raf ve şişeler (GHS etiketli)
    s += IU.isaret_g("gozluk", 1318, 36, 62) + IU.isaret_g("gozdusu", 1400, 36, 62) + IU.isaret_g("onluk", 1482, 36, 62)
    s += f'<rect x="1300" y="200" width="250" height="12" fill="#9A6B42"/>'
    for i, (renk, kod) in enumerate((("#9FD9E6", "GHS02"), ("#FFE08A", "GHS05"), ("#F6D0C8", "GHS07"), ("#C9D3F0", "GHS09"))):
        bx = 1316 + i * 58
        s += f'<rect x="{bx}" y="132" width="44" height="68" rx="8" fill="{renk}" stroke="{OBS_}" stroke-width="3"/><rect x="{bx + 12}" y="116" width="20" height="18" fill="#56636E" stroke="{OBS_}" stroke-width="2"/>'
        s += IU.ghs_g(kod, bx + 6, 150, 32)
    # tezgâh
    s += f'<rect x="0" y="380" width="{W}" height="22" fill="#2F3A44"/><rect x="0" y="402" width="{W}" height="{H - 402}" fill="#B98D5E"/>'
    for k in range(9):
        s += f'<path d="M{80 + k * 250} 410 V{H}" stroke="#8C643E" stroke-width="4"/>'
    # tezgâhta cam malzeme (odak)
    s += f'<g transform="translate(1550 380) scale(.55)">' + IU.ekipman_parca(s, "sacayak", 0, 0, 1) + "</g>"
    s += IU.ekipman_parca(s, "bek", 1550, 380, .3)
    s += IU.cam_parca(s, "erlen", 1700, 380, .55, "#F0A21A")
    s += IU.cam_parca(s, "mezur", 1780, 380, .55, "#13A3A6")
    s += IU.cam_parca(s, "balon", 1880, 380, .48, "#E2533D")
    s += IU.cam_parca(s, "beher", 1440, 380, .5, "#2B50B5")
    s += _karakter("pamuk-akce", 1296, 292, 84)
    return _bitir(s)


# ================================================================== HÜLASA · BARTIN IRMAĞI (akşamüstü, b40)

def bartin_irmagi(h=400):
    s = Svg("kg-bir")
    ufuk = 210
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#33307A"), (.35, "#8A5AA8"), (.65, "#F08AA0"), (.85, "#FFB27A"), (1, "#FFD99A")])
    s += S.gunes(s, 1300, ufuk - 30, 36, cekirdek="#FFF3DA", hale="#FFB27A", hale_r=460, guc=.9)
    s += S.bulut_serit(s, 1500, 90, 420, 10, "#FFD0DA", "#E98FB0", .6)
    tepe = orman_sirti(s, -40, 2140, ufuk, 80, 81, "#6E6A9C", "#56588A", olcek=.6, yuvarlak=.5)[0]
    s += tepe
    s += _zemin(s, ufuk + 40, "#4F6F57", h)
    evler = kasaba(s, 1150, 2050, ufuk + 70, 8, 82, olcek=.62, egim=0)
    s += evler
    s += deniz(s, 0, ufuk + 80, W, h - ufuk - 80, 83, gunes_x=1300, renk=("#F2B4A8", "#6E6AA8", "#2C2E6A"), parilti="#FFD9A0")
    s += S.yansima(s, evler, ufuk + 80, 1100, 1000, 120, op=.3)
    for i, (x, y, uz, renk) in enumerate(((1500, ufuk + 150, 90, "#C8442F"), (1760, ufuk + 170, 110, "#13A3A6"), (1980, ufuk + 140, 80, "#F0A21A"))):
        s += S.tekne(s, x, y, uz, govde=renk)
    s += _karakter("pamuk-kitap", 1310, ufuk + 76, 74)
    s += _cerceve_golge(s, h)
    return _bitir(s, h)


# ================================================================== YAN YOL 1 · GÜZELCEHİSAR LAV SÜTUNLARI (meclis)

def lav_meclis():
    s = Svg("kg-lav")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 1150, 70, 30, hale="#FFF2C2", hale_r=300, guc=.75)
    for i, (x, y, w_) in enumerate([(820, 100, 220), (1560, 70, 200)]):
        s += S.bulut(s, x, y, w_, 90 + i, ust="#FFFFFF", alt="#D7E6F2", op=.95)
    s += deniz(s, 0, ufuk, W, H - ufuk, 91, renk=("#B6E3EE", "#2C8FB4", "#124F72"))
    s += S.dalga_cizgileri(0, ufuk + 20, 1400, 120, 92, n=26, op=.55)
    # yeşil yamaç ve kaya kıyısı (sağ)
    s += orman_sirti(s, 1300, 2140, ufuk - 10, 90, 93, "#4F8A57", "#3B7D47", olcek=.75)[0]
    s += f'<path d="M1220 {H} L1300 {ufuk + 70} C1500 {ufuk + 40} 1800 {ufuk + 50} 2100 {ufuk + 40} V{H} Z" fill="#5B5E66"/>'
    s += lav_sutunlari(s, 1300, 2120, H - 6, 94, boy=(80, 230), en=58)
    s += f'<path d="M1240 {H - 40} H2100" stroke="#9A6B42" stroke-width="12"/><path d="M1240 {H - 40} H2100" stroke="#C99566" stroke-width="6"/>'
    for k in range(18):
        s += f'<path d="M{1250 + k * 48} {H - 40} v40" stroke="#8C5E36" stroke-width="5"/>'
    s += _karakter("yusuf-defter", 1440, 236, 112) + _karakter("elif-dusunen", 1590, 226, 112) + _karakter("pamuk-dusunen", 1740, 292, 78)
    s += S.marti(1000, 150, .8, 3, renk="#2F3A55") + S.marti(1080, 120, .6, -2, renk="#2F3A55")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== YAN YOL 2 · AMASRA ÇEKİCİLER ÇARŞISI (kıssa)

def cekiciler():
    s = Svg("kg-cek")
    ufuk = 230
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3D8FD6"), (.6, "#9AD2EE"), (1, "#F2F6E8")])
    s += S.gunes(s, 1200, 80, 30, hale="#FFF2C2", hale_r=300, guc=.75)
    s += S.bulut(s, 900, 110, 220, 100, ust="#FFFFFF", alt="#D7E6F2", op=.95)
    s += deniz(s, 0, ufuk, 1300, H - ufuk, 101)
    # kale tepesi ve surlar (arka)
    s += f'<path d="M1150 {ufuk + 30} C1300 {ufuk - 40} 1600 {ufuk - 60} 2100 {ufuk - 30} V{H} H1150 Z" fill="#7FA864"/>'
    pts = [(1240, ufuk + 10), (1400, ufuk - 30), (1560, ufuk - 46), (1720, ufuk - 50), (1880, ufuk - 40), (2040, ufuk - 30), (2140, ufuk - 26)]
    s += surlar(s, pts, 54, 102, burc_her=2)
    # çarşı sokağı
    zm = s.lin([(0, "#D9CCB4"), (1, "#A89878")], 0, 330, 0, H, kull="userSpaceOnUse", ad="sk")
    s += f'<path d="M1150 {H} C1300 360 1600 340 2100 330 V{H} Z" fill="{zm}"/>'
    for i, (x, w_, h_, t) in enumerate(((1440, 150, 120, "#C8442F"), (1610, 160, 136, "#13A3A6"), (1790, 150, 130, "#F0A21A"), (1960, 170, 146, "#2B50B5"))):
        s += dukkan(s, x, 360 + i * 6, w_, h_, 103 + i, tente=t)
    for k in range(5):
        s += kasik(1500 + k * 34, 446, 1.0, -12 + k * 6, ["#E2B88A", "#C9955E", "#A8743F"][k % 3])
    s += _karakter("elif-aha", 1300, 300, 116)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== YAN YOL 3 · AMASRA KEMERE KÖPRÜSÜ (gün batımı, anahtar merdiveni)

def kemere():
    s = Svg("kg-kem")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gunbatimi")
    s += S.gunes(s, 1100, ufuk - 26, 46, cekirdek="#FFF3DA", hale="#FFB27A", hale_r=560, guc=.95)
    s += S.bulut_serit(s, 500, 160, 520, 10, "#FFD0DA", "#E98FB0", .6)
    s += S.bulut_serit(s, 1400, 110, 460, 11, "#FFE0D8", "#F2A6BC", .55)
    s += deniz(s, 0, ufuk, W, H - ufuk, 112, gunes_x=1100, renk=("#F7B49A", "#8A5A9C", "#2C2E6A"), parilti="#FFD9A0")
    # Boztepe (sağ, ada) + surlar
    s += f'<path d="M1640 {ufuk + 30} C1700 {ufuk - 90} 1900 {ufuk - 110} 2140 {ufuk - 80} V{ufuk + 60} H1640 Z" fill="#5E7A4E"/>'
    s += surlar(s, [(1700, ufuk - 30), (1820, ufuk - 76), (1960, ufuk - 90), (2100, ufuk - 80)], 44, 113, burc_her=2, tas="#C9B79A")
    for i, (x, w_, h_) in enumerate(((1660, 120, 60), (1780, 150, 70), (1960, 170, 64), (2090, 130, 56))):
        s += S.kaya(s, x, ufuk + 62, w_, h_, 114 + i, renk="#6A5C6E")
    for i in range(9):
        s += cam_agaci(s, 1760 + i * 42, ufuk - 84 + abs(i - 4) * 6, 52, 26, 120 + i, isik=-1)
    # köprü: kıyıdan (sol) adaya (sağ)
    s += f'<path d="M1120 {ufuk + 120} L1200 {ufuk + 40} H1300 V{ufuk + 140} Z" fill="#6E6A72"/>'
    s += kemer_kopru(s, 1290, 1660, ufuk + 26, 60, n=2, tas="#D9C7A2")
    for k in range(6):     # basamaklar
        s += f'<rect x="{1630 + k * 14}" y="{ufuk + 26 - k * 9}" width="40" height="9" fill="#D9C7A2" stroke="#8E7F68" stroke-width="1.6"/>'
    s += S.yansima(s, kemer_kopru(s, 1290, 1660, ufuk + 26, 60, n=2, tas="#D9C7A2"), ufuk + 110, 1280, 400, 120, op=.25)
    s += _karakter("pamuk-selam", 1430, ufuk - 74, 70)
    s += S.marti(900, 170, .9, 2, renk="#2A2442") + S.marti(980, 140, .6, -2, renk="#2A2442")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== AMASRA KALESİ · İMTİHAN 1 (b62) ve KAPI (b30)

def _amasra(s, ufuk, h, tohum, gunes_x=1000, gece=False):
    """Amasra: Zindan tepesinde ve kıyıda surlar, Kemere, Boztepe, iki liman; deniz önde."""
    tas = "#3E4677" if gece else TAS
    yesil = "#24304F" if gece else "#5E7F4E"
    o = ""
    o += f'<path d="M1050 {ufuk + 40} C1150 {ufuk - 120} 1400 {ufuk - 170} 1560 {ufuk - 150} C1700 {ufuk - 130} 1760 {ufuk - 40} 1800 {ufuk + 40} Z" fill="{yesil}"/>'
    o += f'<path d="M1780 {ufuk + 40} C1840 {ufuk - 70} 2000 {ufuk - 100} 2140 {ufuk - 80} V{ufuk + 40} Z" fill="{koyu(yesil, .1)}"/>'
    o += surlar(s, [(1080, ufuk + 10), (1180, ufuk - 70), (1300, ufuk - 130), (1420, ufuk - 152), (1560, ufuk - 140), (1680, ufuk - 90), (1760, ufuk - 10)],
                64, tohum, tas=tas, burc_her=2)
    o += surlar(s, [(1860, ufuk - 30), (1960, ufuk - 70), (2080, ufuk - 80)], 46, tohum + 1, tas=tas, burc_her=2)
    o += kemer_kopru(s, 1770, 1880, ufuk - 6, 34, n=1, tas=tas)
    # kıyı evleri (kasaba)
    renkler = ("#3A4272", "#434C80", "#353D6A") if gece else (SIVA, "#FBF6EC", "#F2EADB")
    o += kasaba(s, 1100, 1700, ufuk + 40, 8, tohum + 3, olcek=.55, renkler=renkler)
    return o


def amasra_kale(h=620):
    s = Svg("kg-amk")
    ufuk = 420
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gunbatimi")
    s += S.gunes(s, 860, ufuk - 40, 56, cekirdek="#FFF3DA", hale="#FFB27A", hale_r=640, guc=.95)
    for (x, y, w_, k) in ((300, 260, 520, 12), (1100, 170, 600, 14), (1600, 300, 420, 10)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFD0DA", "#E98FB0", .65)
    s += deniz(s, 0, ufuk, W, h - ufuk, 123, gunes_x=860, renk=("#F7B49A", "#8A5A9C", "#2C2E6A"), parilti="#FFD9A0")
    k = _amasra(s, ufuk, h, 124)
    s += k
    s += S.yansima(s, k, ufuk + 42, 1000, 1140, 160, op=.3)
    for i, (x, y, uz, renk) in enumerate(((1250, ufuk + 110, 110, "#C8442F"), (1500, ufuk + 140, 130, "#13A3A6"), (1880, ufuk + 120, 100, "#F0A21A"))):
        s += S.tekne(s, x, y, uz, govde=renk)
    s += S.marti(700, 300, 1.0, 3, renk="#2A2442") + S.marti(780, 260, .7, -2, renk="#2A2442")
    s += _cerceve_golge(s, h)
    return _bitir(s, h)


def amasra_kapi(h=300):
    s = Svg("kg-akp")
    s += S.gokyuzu(s, 0, 0, W, h, duraklar=[(0, "#4A3A8A"), (.5, "#C9467F"), (1, "#FF9A45")])
    s += S.gunes(s, 900, 250, 40, cekirdek="#FFF3DA", hale="#FFB27A", hale_r=420, guc=.9)
    # kalın sur duvarı ve kemerli kapı (sağ)
    g = s.lin([(0, "#E3D3B4"), (1, "#B9A27E")], 0, 60, 0, h, kull="userSpaceOnUse", ad="kd")
    s += f'<rect x="1150" y="70" width="1000" height="{h - 70}" fill="{g}" stroke="#8E7F68" stroke-width="3"/>'
    r = RNG(130)
    for k in range(80):
        x, y = r.uniform(1160, 2090), r.uniform(80, h - 10)
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(30, 60))}" height="{f(r.uniform(14, 22))}" fill="none" stroke="#9C8C70" stroke-width="1.6" opacity=".6"/>'
    for k in range(25):
        if k % 2 == 0:
            s += f'<rect x="{1150 + k * 40}" y="44" width="40" height="28" fill="#E3D3B4" stroke="#8E7F68" stroke-width="2"/>'
    s += burc(s, 1240, h, 130, 270, "#E3D3B4") + burc(s, 2040, h, 130, 270, "#E3D3B4")
    s += f'<path d="M1540 {h} V170 Q1640 70 1740 170 V{h} Z" fill="#2E2218" stroke="#8E7F68" stroke-width="5"/>'
    s += f'<path d="M1560 {h} V178 Q1640 96 1720 178 V{h} Z" fill="#6B4527"/>'
    for k in range(4):
        s += f'<path d="M{1580 + k * 40} {h} V160" stroke="#4A3424" stroke-width="4"/>'
    s += f'<circle cx="1700" cy="{h - 60}" r="7" fill="#F0A21A"/>'
    s += _karakter("pamuk-akce", 1820, h - 120, 96)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== CEVAPLAR · AMASRA GECE (b36)

def amasra_gece(h=360):
    s = Svg("kg-gec")
    ufuk = 250
    s += S.gokyuzu(s, 0, 0, W, h, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk, 160, 140)
    s += S.ay(s, 1250, 70, 30, golge_renk="#13204A")
    s += deniz(s, 0, ufuk, W, h - ufuk, 141, gunes_x=1250, renk=("#2C4A85", "#16285A", "#0A1230"), parilti="#FFF4D6")
    k = _amasra(s, ufuk, h, 142, gece=True)
    s += k
    r = RNG(143)
    for i in range(46):
        x, y = r.uniform(1100, 2080), r.uniform(ufuk - 120, ufuk + 30)
        s += f'<rect x="{f(x)}" y="{f(y)}" width="7" height="8" fill="#FFD27A" opacity="{f(r.uniform(.5, 1), 2)}"/>'
    for i in range(18):
        x = r.uniform(1100, 2080)
        s += f'<path d="M{f(x)} {f(ufuk + 50 + r.uniform(0, 50))} v{f(r.uniform(20, 60))}" stroke="#FFD27A" stroke-width="5" opacity=".45"/>'
    s += S.tekne(s, 1500, ufuk + 80, 110, govde="#3A4272", ust="#C9D3F0")
    s += Y.iskele(s, 1780, 2120, ufuk + 34, 14, 144, ahsap="#4A3A5C")
    s += _karakter("pamuk-otur", 1880, ufuk - 52, 78)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== FİNAL · AMASRA GÜN BATIMI (89 mm)

def final_amasra(h=900, nisanlar=None):
    s = Svg("kg-fin")
    ufuk = 600
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3A4CA0"), (.3, "#8A7CC8"), (.55, "#F29CB4"), (.78, "#FFC892"), (1, "#FFE6C0")])
    gx, gy = 760, ufuk - 30
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE8B0" opacity=".12"/>'
    s += S.gunes(s, gx, gy, 66, hale="#FFC98A", hale_r=680, guc=.95)
    for (x, y, w_, k) in ((200, 260, 520, 12), (1100, 170, 600, 14), (1500, 340, 460, 10)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFE0E6", "#F7A6BC", .7)
    s += deniz(s, 0, ufuk, W, h - ufuk, 153, gunes_x=gx, renk=("#FFC8A8", "#B07AA8", "#3A3C7A"), parilti="#FFE2A8")
    # kale tepesi (sağ) ve en yüksek burç
    s += f'<path d="M1150 {ufuk + 30} C1300 {ufuk - 200} 1600 {ufuk - 280} 1800 {ufuk - 260} C1960 {ufuk - 240} 2080 {ufuk - 160} 2140 {ufuk - 120} V{ufuk + 40} Z" fill="#5E7F4E"/>'
    pts = [(1200, ufuk - 20), (1330, ufuk - 140), (1470, ufuk - 220), (1620, ufuk - 256), (1780, ufuk - 262), (1940, ufuk - 230), (2100, ufuk - 160)]
    s += surlar(s, pts, 80, 154, burc_her=2)
    tx, ty = 1780, ufuk - 262
    s += burc(s, tx, ty + 4, 120, 150, TAS)
    s += kasaba(s, 1180, 1900, ufuk + 34, 9, 155, olcek=.6)
    s += f'<use href="#pamuk-bayrak" x="{tx - 92}" y="{ty - 150 - 190}" width="180" height="212"/>'
    # tekne (sol) ve nişan çelengi: direkten burca
    bx, by = 330, ufuk + 190
    s += S.tekne(s, bx, by, 300, govde="#C8442F", yelken="#F6E7BF")
    sx, sy = bx + 6, by - 230
    ex, ey = tx - 64, ty - 150
    kx, ky = (sx + ex) / 2, max(sy, ey) + 60
    s += f'<path d="M{f(sx)} {f(sy)} Q{f(kx)} {f(ky)} {f(ex)} {f(ey)}" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .8) / (len(nisanlar) + .6)
            x = (1 - t) ** 2 * sx + 2 * (1 - t) * t * kx + t * t * ex
            y = (1 - t) ** 2 * sy + 2 * (1 - t) * t * ky + t * t * ey
            s += f'<path d="M{f(x)} {f(y)} v16" stroke="#5A3A22" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 56)} {f(y + 12)}) rotate({f((k % 2 * 2 - 1) * 5)} 56 64)">{ns}</g>'
    r = RNG(156)
    for k in range(60):
        x, y = r.uniform(300, 1900), r.uniform(80, 560)
        c = r.choice(["#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A"])
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>'
    s += S.marti(1000, 300, 1.2, 4, ayrintili=True) + S.marti(1120, 240, .9, -3, ayrintili=True)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== AÇILIŞ · BATI KARADENİZ PANORAMASI + TUR ROTASI

# Stilize (temsilî) harita: GÜNEYDEN KUZEYE bakış (uzak = Karadeniz). Batı solda. Amasra çevresi okunsun diye açılarak çizildi.
# (anahtar, x, y, etiket üst, etiket ad, alt, tür)
DURAKLAR = [
    ("1", 300, 560, "1. DURAK · ZONGULDAK", "Önce tedbir", "s.2 · +100 akçe", "durak"),
    ("2", 1180, 960, "2. DURAK · KARABÜK", "Sıcağa saygı", "s.3 · +150 akçe", "durak"),
    ("3", 1470, 880, "3. DURAK · SAFRANBOLU", "Dokuz elmas", "s.4 · +150 akçe", "durak"),
    ("4", 1820, 950, "4. DURAK · YÖRÜK KÖYÜ", "Etiketi oku", "s.5 · +150 akçe", "durak"),
    ("5", 1020, 690, "5. DURAK · BARTIN", "Her işe bir kap", "s.6 · +150 akçe", "durak"),
    ("H", 860, 560, "BARTIN IRMAĞI", "Hülasa", "s.7 · +40 akçe", "hulasa"),
    ("M", 560, 455, "GÜZELCEHİSAR", "Meclis: Kim haklı?", "s.8 · +120 akçe", "yan"),
    ("K", 1170, 455, "ÇEKİCİLER ÇARŞISI", "Kıssa", "s.9 · +120 akçe", "yan"),
    ("A", 1430, 400, "KEMERE KÖPRÜSÜ", "Anahtar merdiveni", "s.10 · +120 akçe", "yan"),
    ("V", 1600, 315, "AMASRA KALESİ", "Büyük İmtihan", "s.11–12 · +300 akçe", "kale"),
]
ROTA_ARA = {("1", "2"): [(560, 760), (900, 930)], ("2", "3"): [(1320, 960)], ("3", "4"): [(1640, 950)],
            ("4", "5"): [(1700, 800), (1300, 730)], ("5", "H"): [(930, 640)], ("H", "M"): [(700, 540)],
            ("M", "K"): [(780, 420), (1000, 470)], ("K", "A"): [(1300, 450)], ("A", "V"): [(1520, 360)]}


def panorama_karadeniz(h=1100):
    s = Svg("kg-pan")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#3E5BB0"), (.45, "#8FA6E0"), (.8, "#F8C6C0"), (1, "#FFE6C8")])
    s += S.gunes(s, 1880, 150, 40, cekirdek="#FFF8E6", hale="#FFD9A0", hale_r=420, guc=.85)
    for (x, y, w_, k) in ((520, 120, 300, 200), (1180, 80, 340, 201), (1600, 170, 260, 202)):
        s += S.bulut(s, x, y, w_, k, ust="#FFFFFF", alt="#E3D3EC", op=.95)
    # Karadeniz (üst bant) — kıyı çizgisi aşağıda
    s += deniz(s, 0, ufuk, W, 330, 203, renk=("#A9DCEB", "#2C83AE", "#174E7A"))
    s += S.dalga_cizgileri(0, ufuk + 20, W, 220, 204, n=60, op=.5, k=2.2)
    # kara: kıyıdan içeri ormanlı tepeler
    kiyi = ("M-20 600 C120 560 240 540 330 572 C420 600 470 520 560 486 C640 456 720 500 820 520 "
            "C900 536 960 500 1060 470 C1120 452 1160 430 1240 440 C1300 448 1340 430 1400 412 "
            "C1440 400 1480 372 1530 350 C1570 336 1620 330 1650 352 C1680 374 1700 392 1760 404 "
            "C1860 420 1960 430 2120 420 L2120 1110 L-20 1110 Z")
    kara = s.lin([(0, "#E8D9A8"), (.04, "#7FB06A"), (.3, "#4E8F52"), (.7, "#3F7D48"), (1, "#5E9A55")], 0, 330, 0, h, kull="userSpaceOnUse", ad="kara")
    s += f'<path d="{kiyi}" fill="{kara}"/>'
    s += f'<path d="{kiyi.split(" L2120 1110")[0]}" fill="none" stroke="#F6E7BF" stroke-width="9" opacity=".9"/>'
    # Boztepe adası + Kemere
    s += f'<path d="M1660 300 C1700 268 1780 262 1820 282 C1850 300 1830 330 1780 336 C1730 340 1680 330 1660 300 Z" fill="#6FA562" stroke="#F6E7BF" stroke-width="7"/>'
    s += kemer_kopru(s, 1620, 1690, 334, 16, n=1, tas="#D9C7A2")
    # iç kesimde katman katman ormanlı sırtlar
    for i, (y, gen, renk, renk2) in enumerate(((640, 60, "#5E9A5A", "#4E8A50"), (760, 70, "#4F8D50", "#3F7D48"), (880, 60, "#5A9555", "#467F45"))):
        s += orman_sirti(s, -40, 2140, y, gen, 205 + i, renk, renk2, sik=.5, olcek=.75, yuvarlak=.45)[0]
    r = RNG(209)
    konum = {k: (x, y) for (k, x, y, *_r) in DURAKLAR}
    for k in range(220):       # orman dokusu (rozetlerden uzak)
        x, y = r.uniform(0, 2100), r.uniform(560, 1090)
        if any(math.hypot(x - a, y - b) < 95 for a, b in konum.values()):
            continue
        if not (y > 520 + 60 * math.sin(x / 300)):
            continue
        sc = .5 + (y - 500) / 700 * .6
        s += cam_agaci(s, x, y, 56 * sc, 28 * sc, 300 + k, isik=-1)
    # Bartın Irmağı: Bartın'dan denize
    s += f'<path d="M1040 740 C980 700 940 650 900 600 C870 560 860 530 840 512" stroke="#7FC8E0" stroke-width="16" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M1040 740 C980 700 940 650 900 600 C870 560 860 530 840 512" stroke="#B6E3EE" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>'
    # Zonguldak: liman, kuyu kulesi
    s += f'<g transform="translate(380 548) scale(.32)">{kuyu_kulesi(s, 0, 0, 300, tohum=210)}</g>'
    s += f'<path d="M150 560 h120 v14 h-120 Z" fill="#8FA3AD"/>' + S.tekne(s, 200, 548, 50, govde="#C8442F")
    # Karabük: yüksek fırın + bacalar
    s += f'<g transform="translate(1110 1000) scale(.32)">{yuksek_firin(s, 0, 0, 250, 211)}</g>'
    s += buhar(s, 1140, 900, 3, 212, boy=14, op=.75)
    # Safranbolu: beyaz-ahşap evler
    s += kasaba(s, 1490, 1600, 900, 4, 213, olcek=.36)
    # Yörük Köyü: köy evleri + çamaşırhane
    s += kasaba(s, 1850, 1940, 960, 3, 214, olcek=.32)
    s += camasirhane(s, 1950, 990, 70, 34, 215)
    # Bartın: evler ve okul
    s += kasaba(s, 1050, 1130, 700, 3, 216, olcek=.34)
    # Güzelcehisar: lav sütunları
    s += lav_sutunlari(s, 600, 690, 500, 217, boy=(18, 46), en=16)
    # Amasra: çarşı + kale surları (kıyıda)
    s += surlar(s, [(1500, 368), (1550, 346), (1600, 338)], 22, 218, burc_her=2)
    s += kasaba(s, 1200, 1280, 470, 3, 219, olcek=.3)
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
    s += f'<path d="M{f(x - 36)} {f(y + 40)} v-64" stroke="#1B1D26" stroke-width="4"/><path d="M{f(x - 38)} {f(y - 22)} h-44 l10 13 l-10 13 h44 Z" fill="#E2533D" stroke="#1B1D26" stroke-width="2.4"/>'
    for (ad_, x, y, fs, renk_h) in (("KARADENİZ", 560, 380, 46, "#123E63"), ("Bartın Irmağı", 760, 640, 28, "#1F4E3A"), ("Küre Dağları", 1840, 760, 28, "#1F4E3A")):
        s += halolu_yazi(f'x="{x}" y="{y}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="{fs}" letter-spacing="2"', ad_, "#FFFFFF", renk_h, 1.8)
    s += '<use href="#pamuk-selam" x="40" y="900" width="96" height="110"/>'
    s += S.marti(800, 330, 1.3, 6, ayrintili=True)
    px, py = 1960, h - 140
    s += f'<circle cx="{px}" cy="{py}" r="74" fill="#FFFFFF" opacity=".9" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 66, 14, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 34), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="10" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 82}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), konum
