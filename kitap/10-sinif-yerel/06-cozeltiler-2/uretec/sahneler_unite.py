"""Derişim Birimleri · Göller Yolu (Isparta–Burdur) · üniteye özel sahneler, nişan ikonları ve sahne parçaları.

kur_ortak bu modüle {{sahne|ad|arg…}} ve {{info|ad|arg…}} için ORTAK kütüphaneden (yerel-ortak/cizim) ÖNCE bakar.
Bütün çizimler ortak parçalardan (sahne.py, yapilar.py, temel.py) kurulur; ortak dosyalar değiştirilmez.
  • bant 2100×460 birim (1 birim = 0,1 mm), preserveAspectRatio="xMidYMid slice"
  • sol üst ≈ %55 × %75 gökyüzü/su olarak BOŞ (levha oturur); odak sağda; ışık yönü sahne içinde aynı; tohum sabit
  • konturlu SVG yazısı yok (halolu_yazi); CSS filter yok; her Svg öneki benzersiz ("gy-…")
Eğirdir Kalesi bugün kısmen ayakta bir kalıntıdır; sahnelerde yıkık burç ve surlarla, onarılmış bütün bir kale gibi değil çizilir.
"""
import math
from cizim.temel import Svg, f, cizgi_d, egri_d, karis, acik, koyu, halolu_yazi, selcuklu_yildizi, yildiz_noktalari, rng as RNG
from cizim import sahne as S, yapilar as Y
from cizim.sahneler import W, H, _bitir, _cerceve_golge

OBS = "#1B1D26"

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    "beher": '<path d="M11 7 H37 M14 7 V37 C14 41 16 43 20 43 H28 C32 43 34 41 34 37 V7"/><path d="M14 25 H34"/><path d="M28 13 h6 M28 19 h6"/><circle cx="20" cy="32" r="2.2"/><circle cx="27" cy="36" r="1.7"/>',
    "gul": '<path d="M24 23 C20 23 18 20 20 17 C22 14 27 14 29 17 C31 21 28 25 24 25 C18 25 15 20 17 15 C19 10 27 9 31 13 C35 17 34 25 28 28 C22 31 14 28 13 21"/><path d="M24 28 V44"/><path d="M24 37 C19 33 14 34 12 37 C16 40 21 40 24 37 Z"/><path d="M38 30 C38 30 34 35 34 38 a4 4 0 0 0 8 0 C42 35 38 30 38 30 Z"/>',
    "balon": '<path d="M20 5 H28 M21 5 V20 C13 23 9 29 9 34 C9 40 15 44 24 44 C33 44 39 40 39 34 C39 29 35 23 27 20 V5"/><path d="M18 13 H30"/><path d="M11 33 H37"/><circle cx="19" cy="38" r="1.8"/><circle cx="27" cy="39" r="1.8"/>',
    "seyrelt": '<path d="M6 19 V37 C6 41 8 43 12 43 H18 C22 43 24 41 24 37 V19"/><path d="M6 30 H24"/><path d="M27 31 H41 M37 27 L41 31 L37 35"/><path d="M34 5 C34 5 30 10 30 13 a4 4 0 0 0 8 0 C38 10 34 5 34 5 Z"/>',
    "kar": '<path d="M24 5 V43 M7.5 14.5 L40.5 33.5 M7.5 33.5 L40.5 14.5"/><path d="M19.5 8 L24 12.5 L28.5 8 M19.5 40 L24 35.5 L28.5 40 M8 19.6 L14 18.6 L12 13 M40 28.4 L34 29.4 L36 35 M12 35 L14 29.4 L8 28.4 M36 13 L34 18.6 L40 19.6"/>',
}

# ------------------------------------------------------------------ küçük parçalar


def _cam(x, y, h, tohum, renk="#2E6B4A", kar=False, isik=-1):
    """Konik çam: üç katman, gölge yamacı; kar=True → katmanların üstünde kar."""
    r = RNG(tohum)
    out = [f'<rect x="{f(x - h * .035)}" y="{f(y - h * .15)}" width="{f(h * .07)}" height="{f(h * .15)}" fill="#5B3E26"/>']
    gol = koyu(renk, .32)
    sx = 1 if isik < 0 else -1
    for k in range(3):
        yb = y - h * .1 - k * h * .24
        yt = yb - h * (.46 - k * .06)
        yw = h * (.52 - k * .13) / 2 * r.uniform(.92, 1.08)
        out.append(f'<path d="M{f(x - yw)} {f(yb)} L{f(x)} {f(yt)} L{f(x + yw)} {f(yb)} Q{f(x)} {f(yb + h * .05)} {f(x - yw)} {f(yb)} Z" fill="{renk}"/>')
        out.append(f'<path d="M{f(x)} {f(yt)} L{f(x + sx * yw)} {f(yb)} Q{f(x + sx * yw * .5)} {f(yb + h * .035)} {f(x)} {f(yb + h * .03)} Z" fill="{gol}" opacity=".6"/>')
        if kar:
            ky = yt + (yb - yt) * .42
            out.append(f'<path d="M{f(x - yw * .5)} {f(ky)} L{f(x)} {f(yt)} L{f(x + yw * .5)} {f(ky)} Q{f(x + yw * .25)} {f(ky - h * .03)} {f(x)} {f(ky + h * .02)} Q{f(x - yw * .25)} {f(ky - h * .03)} {f(x - yw * .5)} {f(ky)} Z" fill="#FFFFFF"/>')
            out.append(f'<path d="M{f(x - yw)} {f(yb)} Q{f(x - yw * .5)} {f(yb - h * .045)} {f(x)} {f(yb - h * .01)} Q{f(x + yw * .5)} {f(yb - h * .045)} {f(x + yw)} {f(yb)} Q{f(x)} {f(yb + h * .03)} {f(x - yw)} {f(yb)} Z" fill="#F4F8FC"/>')
    return "".join(out)


def _gul_cali(x, y, r_, tohum, n=7, pembe=("#E8467C", "#FF7FA8", "#D63A6E", "#FF9BBE")):
    """Yağ gülü (Rosa damascena) çalısı: yeşil öbek + pembe çiçekler."""
    r = RNG(tohum)
    out = [f'<ellipse cx="{f(x)}" cy="{f(y - r_ * .55)}" rx="{f(r_)}" ry="{f(r_ * .62)}" fill="#356F35"/>',
           f'<ellipse cx="{f(x - r_ * .22)}" cy="{f(y - r_ * .74)}" rx="{f(r_ * .64)}" ry="{f(r_ * .4)}" fill="#4E8F42"/>']
    for _ in range(n):
        cx = x + r.uniform(-.85, .85) * r_
        cy = y - r_ * .6 + r.uniform(-.55, .35) * r_ * .62
        rr = r_ * r.uniform(.14, .21)
        c = r.choice(pembe)
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr)}" fill="{c}"/><circle cx="{f(cx + rr * .15)}" cy="{f(cy - rr * .1)}" r="{f(rr * .45)}" fill="{koyu(c, .22)}"/>')
    return "".join(out)


def _gul_tarlasi(x0, x1, y0, y1, tohum, sira=5):
    """Perspektifte gül sıraları (y0 uzak, y1 yakın)."""
    r = RNG(tohum)
    out = []
    for k in range(sira):
        t = k / max(1, sira - 1)
        y = y0 + (y1 - y0) * t ** 1.25
        rr = 9 + 26 * t
        adim = rr * 1.55
        x = x0 + r.uniform(0, adim)
        out.append(f'<path d="M{f(x0)} {f(y + rr * .1)} H{f(x1)}" stroke="#7A5A3A" stroke-width="{f(1 + 2 * t)}" opacity=".35"/>')
        i = 0
        while x < x1:
            out.append(_gul_cali(x, y, rr * r.uniform(.85, 1.1), tohum * 100 + k * 37 + i, n=int(4 + 4 * t)))
            x += adim * r.uniform(.85, 1.15)
            i += 1
    return "".join(out)


def _cuval(x, y, w, renk="#E9D7B0", gul=True):
    h = w * .9
    out = f'<path d="M{f(x - w / 2)} {f(y)} C{f(x - w * .6)} {f(y - h * .6)} {f(x - w * .38)} {f(y - h)} {f(x)} {f(y - h)} C{f(x + w * .38)} {f(y - h)} {f(x + w * .6)} {f(y - h * .6)} {f(x + w / 2)} {f(y)} Z" fill="{renk}" stroke="#8C6A3E" stroke-width="2"/>'
    if gul:
        for k in range(4):
            out += f'<circle cx="{f(x - w * .25 + k * w * .17)}" cy="{f(y - h * .98 + (k % 2) * 3)}" r="{f(w * .1)}" fill="{["#E8467C", "#FF7FA8", "#D63A6E", "#FF9BBE"][k]}"/>'
    return out


def _imbik_kazan(s, x, y, h):
    """Bakır gül imbiği: tuğla ocak + kazan + başlık + kuğu boynu boru + soğutma teknesi + toplama şişesi."""
    g = s.lin([(0, "#F6C08E"), (.42, "#D27E42"), (1, "#7E3E1C")], 0, 0, 1, 0, ad="bk")
    w = h * .62
    out = [f'<rect x="{f(x - w * .62)}" y="{f(y - h * .22)}" width="{f(w * 1.24)}" height="{f(h * .22)}" fill="#A6532E" stroke="#5A2A14" stroke-width="2.4"/>']
    for k in range(3):
        yy = y - h * .22 + (k + 1) * h * .055
        out.append(f'<path d="M{f(x - w * .62)} {f(yy)} H{f(x + w * .62)}" stroke="#7E3A1E" stroke-width="1.6"/>')
    out.append(f'<path d="M{f(x - w * .18)} {f(y)} v{f(-h * .1)} a{f(w * .18)} {f(h * .08)} 0 0 1 {f(w * .36)} 0 v{f(h * .1)} Z" fill="#3A1E10"/>')
    out.append(f'<path d="M{f(x - w * .12)} {f(y - h * .01)} q{f(w * .06)} {f(-h * .09)} {f(w * .12)} {f(-h * .03)} q{f(w * .05)} {f(-h * .05)} {f(w * .12)} {f(h * .03)} Z" fill="#FFB43A"/>')
    out.append(f'<path d="M{f(x - w / 2)} {f(y - h * .22)} C{f(x - w * .62)} {f(y - h * .58)} {f(x - w * .42)} {f(y - h * .8)} {f(x)} {f(y - h * .82)} C{f(x + w * .42)} {f(y - h * .8)} {f(x + w * .62)} {f(y - h * .58)} {f(x + w / 2)} {f(y - h * .22)} Z" fill="{g}" stroke="#5A2A14" stroke-width="2.6"/>')
    out.append(f'<path d="M{f(x - w * .36)} {f(y - h * .62)} C{f(x - w * .3)} {f(y - h * .72)} {f(x - w * .16)} {f(y - h * .76)} {f(x - w * .04)} {f(y - h * .77)}" stroke="#FFE2C2" stroke-width="{f(h * .025)}" fill="none" stroke-linecap="round" opacity=".8"/>')
    out.append(f'<path d="M{f(x - w * .2)} {f(y - h * .81)} C{f(x - w * .22)} {f(y - h * 1.0)} {f(x + w * .22)} {f(y - h * 1.0)} {f(x + w * .2)} {f(y - h * .81)} Z" fill="{g}" stroke="#5A2A14" stroke-width="2.4"/>')
    out.append(f'<path d="M{f(x + w * .1)} {f(y - h * .96)} C{f(x + w * .6)} {f(y - h * 1.08)} {f(x + w * 1.05)} {f(y - h * .92)} {f(x + w * 1.22)} {f(y - h * .62)}" stroke="#5A2A14" stroke-width="{f(h * .055)}" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M{f(x + w * .1)} {f(y - h * .96)} C{f(x + w * .6)} {f(y - h * 1.08)} {f(x + w * 1.05)} {f(y - h * .92)} {f(x + w * 1.22)} {f(y - h * .62)}" stroke="#D88A50" stroke-width="{f(h * .032)}" fill="none" stroke-linecap="round"/>')
    out.append(f'<rect x="{f(x + w * .98)}" y="{f(y - h * .62)}" width="{f(w * .5)}" height="{f(h * .42)}" rx="{f(h * .03)}" fill="#7DA3B8" stroke="#2F4A5A" stroke-width="2.2"/>')
    out.append(f'<path d="M{f(x + w * .98)} {f(y - h * .5)} H{f(x + w * 1.48)} M{f(x + w * .98)} {f(y - h * .36)} H{f(x + w * 1.48)}" stroke="#5E8496" stroke-width="2"/>')
    out.append(f'<path d="M{f(x + w * 1.36)} {f(y - h * .2)} v{f(h * .06)}" stroke="#5A2A14" stroke-width="3"/>')
    out.append(f'<path d="M{f(x + w * 1.26)} {f(y - h * .12)} h{f(w * .2)} l{f(w * .04)} {f(h * .12)} h{f(-w * .28)} Z" fill="#E6F4F4" stroke="#2F4A5A" stroke-width="2"/><path d="M{f(x + w * 1.25)} {f(y - h * .05)} h{f(w * .26)} l{f(w * .02)} {f(h * .05)} h{f(-w * .3)} Z" fill="#F2C04A"/>')
    return "".join(out)


def _flamingo(x, y, o=1.0, yon=1, c="#F48FB1", ck="#D9607F"):
    """Göl kıyısında flamingo: gövde, S boyun, kara uçlu gaga, ince bacaklar (y: ayak ucu)."""
    by = y - 40 * o
    return (f'<path d="M{f(x - 2 * o)} {f(by + 6 * o)} V{f(y)} M{f(x + 4 * o)} {f(by + 6 * o)} L{f(x + 4 * o)} {f(by + 20 * o)} L{f(x + yon * 12 * o)} {f(by + 26 * o)}" stroke="#C0506A" stroke-width="{f(1.6 * o)}" fill="none"/>'
            f'<ellipse cx="{f(x)}" cy="{f(by)}" rx="{f(17 * o)}" ry="{f(9 * o)}" fill="{c}"/>'
            f'<path d="M{f(x - yon * 15 * o)} {f(by - 2 * o)} q{f(-yon * 8 * o)} {f(2 * o)} {f(-yon * 10 * o)} {f(6 * o)} q{f(yon * 8 * o)} {f(-1 * o)} {f(yon * 12 * o)} {f(-2 * o)} Z" fill="{ck}"/>'
            f'<path d="M{f(x + yon * 12 * o)} {f(by - 4 * o)} C{f(x + yon * 22 * o)} {f(by - 16 * o)} {f(x + yon * 4 * o)} {f(by - 26 * o)} {f(x + yon * 10 * o)} {f(by - 38 * o)}" stroke="{c}" stroke-width="{f(4 * o)}" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{f(x + yon * 11 * o)}" cy="{f(by - 39 * o)}" r="{f(4.4 * o)}" fill="{c}"/>'
            f'<path d="M{f(x + yon * 14 * o)} {f(by - 40 * o)} q{f(yon * 7 * o)} {f(1 * o)} {f(yon * 7 * o)} {f(7 * o)}" stroke="{OBS}" stroke-width="{f(2.4 * o)}" fill="none" stroke-linecap="round"/>')


def _dikkuyruk(x, y, o=1.0, yon=1):
    """Dikkuyruk ördeği: kestane gövde, beyaz baş, kara tepe, mavi gaga, dik kuyruk."""
    return (f'<path d="M{f(x - yon * 13 * o)} {f(y - 3 * o)} L{f(x - yon * 19 * o)} {f(y - 17 * o)} L{f(x - yon * 15 * o)} {f(y - 18 * o)} L{f(x - yon * 9 * o)} {f(y - 4 * o)} Z" fill="#4E3424"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(15 * o)}" ry="{f(7 * o)}" fill="#8B5A3C"/>'
            f'<circle cx="{f(x + yon * 12 * o)}" cy="{f(y - 8 * o)}" r="{f(6 * o)}" fill="#FFFFFF"/>'
            f'<path d="M{f(x + yon * 6.5 * o)} {f(y - 10 * o)} a{f(6 * o)} {f(5 * o)} 0 0 1 {f(yon * 11 * o)} 0 Z" fill="{OBS}"/>'
            f'<path d="M{f(x + yon * 17 * o)} {f(y - 8 * o)} q{f(yon * 6 * o)} {f(1 * o)} {f(yon * 6 * o)} {f(4 * o)} q{f(-yon * 4 * o)} {f(1 * o)} {f(-yon * 7 * o)} {f(-1 * o)} Z" fill="#3A7BD5"/>'
            f'<path d="M{f(x - 16 * o)} {f(y + 6 * o)} q{f(16 * o)} {f(5 * o)} {f(32 * o)} 0" stroke="#FFFFFF" stroke-width="{f(1.4 * o)}" fill="none" opacity=".7"/>')


def _sur(s, x0, x1, y, h, tohum, tas="#CDB38C", tugla="#B5653E", isik=-1, kule_n=3, kirik=.6):
    """Taş-tuğla (almaşık) sur kalıntısı: yer yer yıkık üst kenar, çokgen burçlar, tuğla hatıllar. y: taban."""
    r = RNG(tohum)
    out = []
    gs = s.lin([(0, acik(tas, .12)), (1, koyu(tas, .18))], 0, y - h, 0, y, kull="userSpaceOnUse", ad="sr")
    n = 26
    ust = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        yy = y - h * (.62 + .1 * math.sin(i * 1.3 + tohum))
        if r.random() < kirik:
            yy += r.uniform(0, h * .22)
        ust.append((x, yy))
    d = cizgi_d([(x0, y)] + ust + [(x1, y)], True)
    out.append(f'<path d="{d}" fill="{gs}" stroke="#7A6248" stroke-width="2"/>')
    kl = s.klip(f'<path d="{d}"/>', ad="srk")
    bant = []
    for k in range(int(h / 26)):
        yy = y - 18 - k * 26
        bant.append(f'<path d="M{f(x0)} {f(yy)} H{f(x1)}" stroke="{tugla}" stroke-width="5" opacity=".8"/>')
        for j in range(int((x1 - x0) / 34)):
            xx = x0 + j * 34 + (k % 2) * 17 + r.uniform(-3, 3)
            bant.append(f'<path d="M{f(xx)} {f(yy - 21)} v14" stroke="#9C8466" stroke-width="1.2" opacity=".6"/>')
    out.append(f'<g clip-path="{kl}">{"".join(bant)}</g>')
    for k in range(kule_n):
        cx = x0 + (x1 - x0) * (k + .5) / kule_n + r.uniform(-20, 20)
        kw = h * r.uniform(.42, .55)
        kh = h * r.uniform(.95, 1.12)
        tepe = y - kh
        kir = [(cx - kw / 2, tepe + r.uniform(0, 14))]
        for j in range(1, 6):
            kir.append((cx - kw / 2 + kw * j / 6, tepe + r.uniform(0, kh * .16)))
        kir.append((cx + kw / 2, tepe + r.uniform(0, 18)))
        kd = cizgi_d([(cx - kw / 2, y)] + kir + [(cx + kw / 2, y)], True)
        gk = s.lin([(0, acik(tas, .2)), (.55, tas), (1, koyu(tas, .25))], 0, 0, 1, 0, ad="kl")
        out.append(f'<path d="{kd}" fill="{gk}" stroke="#7A6248" stroke-width="2.2"/>')
        kk = s.klip(f'<path d="{kd}"/>', ad="kk")
        bb = "".join(f'<path d="M{f(cx - kw / 2)} {f(y - 22 - j * 28)} H{f(cx + kw / 2)}" stroke="{tugla}" stroke-width="5" opacity=".85"/>' for j in range(int(kh / 28)))
        out.append(f'<g clip-path="{kk}">{bb}</g>')
        out.append(f'<path d="M{f(cx - 5)} {f(tepe + kh * .38)} v{f(kh * .16)} h10 v{f(-kh * .16)} Z" fill="#4A3A2A" opacity=".75"/>')
    for k in range(9):
        xx = x0 + r.uniform(0, x1 - x0)
        out.append(f'<path d="M{f(xx)} {f(y)} q{f(r.uniform(4, 10))} {f(-r.uniform(10, 26))} {f(r.uniform(10, 18))} 0 Z" fill="#6E8A44"/>')
    return "".join(out)


def _ev2(x, y, w, h, tohum, duvar="#F3E6CC", cati="#C2563A", isik=-1):
    """İki katlı göl evi: cumbalı üst kat, kiremit çatı (Yeşilada evleri gibi, temsilî)."""
    r = RNG(tohum)
    out = [f'<rect x="{f(x)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="{duvar}" stroke="#6E5236" stroke-width="1.8"/>',
           f'<rect x="{f(x + w * .2)}" y="{f(y - h * 1.02)}" width="{f(w * .6)}" height="{f(h * .42)}" fill="{koyu(duvar, .06)}" stroke="#6E5236" stroke-width="1.6"/>',
           f'<path d="M{f(x - w * .08)} {f(y - h)} L{f(x + w * .5)} {f(y - h * 1.38)} L{f(x + w * 1.08)} {f(y - h)} Z" fill="{cati}" stroke="#6E2E1E" stroke-width="1.8"/>']
    for k in range(3):
        px = x + w * (.24 + k * .2)
        out.append(f'<rect x="{f(px)}" y="{f(y - h * .92)}" width="{f(w * .1)}" height="{f(h * .2)}" fill="#3E5A6E"/>')
    for k in range(2):
        px = x + w * (.18 + k * .52)
        out.append(f'<rect x="{f(px)}" y="{f(y - h * .45)}" width="{f(w * .12)}" height="{f(h * .2)}" fill="#3E5A6E"/>')
    out.append(f'<rect x="{f(x + w * .44)}" y="{f(y - h * .34)}" width="{f(w * .12)}" height="{f(h * .34)}" fill="#7A4E2E"/>')
    if r.random() < .5:
        out.append(f'<rect x="{f(x + w * .1)}" y="{f(y - h * 1.3)}" width="{f(w * .07)}" height="{f(h * .2)}" fill="#8C5A35"/>')
    return "".join(out)


def _konfeti(r, n, x0, y0, w, h, renkler=("#F0A21A", "#13A3A6", "#E2533D", "#FFFFFF", "#2B50B5", "#FF5C8A")):
    out = []
    for _ in range(n):
        x, y = x0 + r.uniform(0, w), y0 + r.uniform(0, h)
        c = r.choice(renkler)
        out.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(r.uniform(6, 12))}" height="{f(r.uniform(3, 6))}" fill="{c}" transform="rotate({f(r.uniform(0, 180))} {f(x)} {f(y)})" opacity=".9"/>')
    return "".join(out)


def _gul_yapragi(r, n, x0, y0, w, h):
    out = []
    for _ in range(n):
        x, y = x0 + r.uniform(0, w), y0 + r.uniform(0, h)
        c = r.choice(["#FF7FA8", "#E8467C", "#FFB3CB", "#D63A6E"])
        a = r.uniform(0, 180)
        s_ = r.uniform(5, 9)
        out.append(f'<path d="M{f(x)} {f(y)} q{f(s_)} {f(-s_)} {f(2 * s_)} 0 q{f(-s_)} {f(s_ * .9)} {f(-2 * s_)} 0 Z" fill="{c}" transform="rotate({f(a)} {f(x)} {f(y)})" opacity=".92"/>')
    return "".join(out)


def _fisek(x, y, R, renk, tohum, n=18):
    """Havai fişek patlaması: ince ışınlar + uç noktaları (dolgulu şekiller; yazı yok)."""
    r = RNG(tohum)
    out = [f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R * 1.25)}" fill="{renk}" opacity=".08"/>']
    for k in range(n):
        a = 2 * math.pi * k / n + r.uniform(-.05, .05)
        rr = R * r.uniform(.78, 1.05)
        x1, y1 = x + math.cos(a) * rr * .25, y + math.sin(a) * rr * .25
        x2, y2 = x + math.cos(a) * rr, y + math.sin(a) * rr
        out.append(f'<path d="M{f(x1)} {f(y1)} L{f(x2)} {f(y2)}" stroke="{renk}" stroke-width="3" stroke-linecap="round" opacity=".9"/>')
        out.append(f'<circle cx="{f(x2)}" cy="{f(y2)}" r="4" fill="#FFF4D6"/>')
    out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="6" fill="#FFF4D6"/>')
    return "".join(out)


def _tuz_kamyonu(x, y, o=1.0, tohum=7):
    """Tuzlama aracı (sola gider): turuncu kasa, kabin, tepe lambası, arkada dönen tabla ve saçılan tuz."""
    r = RNG(tohum)
    out = [f'<rect x="{f(x)}" y="{f(y - 58 * o)}" width="{f(46 * o)}" height="{f(44 * o)}" rx="{f(6 * o)}" fill="#F28C28" stroke="{OBS}" stroke-width="{f(2.4 * o)}"/>',
           f'<path d="M{f(x + 6 * o)} {f(y - 52 * o)} h{f(26 * o)} v{f(16 * o)} h{f(-30 * o)} Z" fill="#BFE3F0" stroke="{OBS}" stroke-width="{f(1.6 * o)}"/>',
           f'<rect x="{f(x + 16 * o)}" y="{f(y - 66 * o)}" width="{f(12 * o)}" height="{f(8 * o)}" rx="{f(2 * o)}" fill="#FFC52E" stroke="{OBS}" stroke-width="{f(1.4 * o)}"/>',
           f'<path d="M{f(x + 46 * o)} {f(y - 54 * o)} h{f(98 * o)} l{f(8 * o)} {f(10 * o)} v{f(30 * o)} h{f(-106 * o)} Z" fill="#E87A1E" stroke="{OBS}" stroke-width="{f(2.4 * o)}"/>',
           f'<path d="M{f(x + 50 * o)} {f(y - 54 * o)} C{f(x + 70 * o)} {f(y - 72 * o)} {f(x + 120 * o)} {f(y - 74 * o)} {f(x + 142 * o)} {f(y - 54 * o)} Z" fill="#E9EEF2" stroke="#8D9BA6" stroke-width="{f(1.6 * o)}"/>',
           f'<path d="M{f(x + 52 * o)} {f(y - 40 * o)} h{f(94 * o)}" stroke="#FFFFFF" stroke-width="{f(5 * o)}" opacity=".85"/>',
           f'<rect x="{f(x - 6 * o)}" y="{f(y - 22 * o)}" width="{f(160 * o)}" height="{f(10 * o)}" rx="{f(3 * o)}" fill="#3A3F4B"/>']
    for wx in (x + 22 * o, x + 98 * o, x + 128 * o):
        out.append(f'<circle cx="{f(wx)}" cy="{f(y - 8 * o)}" r="{f(13 * o)}" fill="#22252E"/><circle cx="{f(wx)}" cy="{f(y - 8 * o)}" r="{f(5 * o)}" fill="#A3B3BE"/>')
    out.append(f'<path d="M{f(x + 150 * o)} {f(y - 18 * o)} h{f(16 * o)}" stroke="#3A3F4B" stroke-width="{f(4 * o)}"/><ellipse cx="{f(x + 170 * o)}" cy="{f(y - 14 * o)}" rx="{f(10 * o)}" ry="{f(3 * o)}" fill="#5E6672"/>')
    for _ in range(46):
        a = r.uniform(-.5, .9)
        d = r.uniform(12, 120) * o
        px, py = x + 172 * o + math.cos(a) * d, y - 14 * o + math.sin(a) * d * .35
        out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r.uniform(1.2, 2.8) * o)}" fill="#FFFFFF" opacity="{f(r.uniform(.6, 1), 2)}"/>')
    return "".join(out)


def _kar_yagisi(r, n, x0, y0, w, h, rmax=3.8):
    return "".join(f'<circle cx="{f(x0 + r.uniform(0, w))}" cy="{f(y0 + r.uniform(0, h))}" r="{f(r.uniform(1.2, rmax))}" fill="#FFFFFF" opacity="{f(r.uniform(.55, .95), 2)}"/>' for _ in range(n))


def _telesiyej(x0, y0, x1, y1, n=6):
    out = [f'<path d="M{f(x0)} {f(y0)} L{f(x1)} {f(y1)}" stroke="#3A3F4B" stroke-width="2.4"/>']
    for k in range(n):
        t = (k + .5) / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        out.append(f'<path d="M{f(x)} {f(y)} v16" stroke="#3A3F4B" stroke-width="2"/><path d="M{f(x - 8)} {f(y + 16)} h16 v8 h-16 Z" fill="{["#E2533D", "#2B50B5", "#F0A21A"][k % 3]}"/>')
    for t in (0, .5, 1):
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        out.append(f'<path d="M{f(x)} {f(y - 4)} V{f(y + 60)}" stroke="#5E6672" stroke-width="5"/><path d="M{f(x - 14)} {f(y)} h28" stroke="#5E6672" stroke-width="4"/>')
    return "".join(out)


def _sahne_bas(onek, tema=None, duraklar=None, ufuk=286):
    s = Svg(onek)
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, tema or "gun", duraklar=duraklar)
    return s


# ------------------------------------------------------------------ 1. DURAK · EĞİRDİR GÖLÜ (öğle)

def egirdir_golu():
    s = _sahne_bas("gy-egr", "gun", ufuk=270)
    ufuk = 270
    s += S.gunes(s, 1180, 70, 32, hale="#FFF2C2", hale_r=300, guc=.8)
    for i, (x, y, w_) in enumerate([(760, 110, 240), (1430, 86, 280), (1880, 140, 180), (420, 170, 160)]):
        s += S.bulut(s, x, y, w_, 600 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    uzak = ""
    d, _ = S.dag(s, 980, 2240, ufuk, 1560, 96, 601, renk="#7FA0C4", golge="#5B7EA8", bicim="sivri", kar_y=150,
                 kar="#FFFFFF", kar_golge="#C9DAEE", sis="#C4E2F0", isik=-1, sirt=4)
    uzak += d
    d, _ = S.dag(s, -80, 900, ufuk, 360, 176, 602, renk="#93B6D2", golge="#7298BE", bicim="tepe", sis="#D8EDF6", isik=-1, sirt=2, puruz=6)
    uzak += d
    d, _ = S.dag(s, 1700, 2200, ufuk, 1960, 150, 603, renk="#6E92B8", golge="#4F739E", bicim="sivri", sis="#C4E2F0", isik=-1, sirt=3, puruz=10)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, H - ufuk, 604, ufuk="#BFF0EC", orta="#1FB5B5", derin="#0A6A7A", gunes_x=1180, parilti_renk="#FFF3C8", yogunluk=1.25)
    s += S.yansima(s, uzak, ufuk, 0, W, 130, op=.25)
    # uzakta Yeşilada (evli küçük ada) + yelkenli
    s += f'<path d="M1040 {ufuk + 12} C1070 {ufuk - 6} 1150 {ufuk - 10} 1190 {ufuk + 12} Z" fill="#6E8F5C"/>'
    for k in range(5):
        s += f'<rect x="{1068 + k * 20}" y="{ufuk - 6 - (k % 2) * 4}" width="14" height="10" fill="#F3E6CC"/><path d="M{1066 + k * 20} {ufuk - 6 - (k % 2) * 4} l9 -6 l9 6 Z" fill="#C2563A"/>'
    s += S.tekne(s, 820, ufuk + 54, 70, govde="#F4E9D8", yelken="#FFFFFF")
    s += S.tekne(s, 1290, ufuk + 34, 46, govde="#C8442F")
    # sağ kıyı: elma bahçesi + iskele + deney masası (derişim: üç bardak)
    kiyi = [(1380, H), (1420, 352), (1560, 330), (1760, 322), (1960, 318), (2100, 312), (2100, H)]
    g = s.lin([(0, "#9CC65E"), (1, "#4E8A3E")], 0, 310, 0, H, kull="userSpaceOnUse", ad="ky")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {H} Z" fill="{g}"/>'
    for i, x in enumerate((1600, 1680, 1760, 1850, 1930, 2010, 2085)):
        s += S.agac(s, x, 330 - (x - 1600) * .02, 34 + (i % 3) * 4, 610 + i, renk=["#5FA048", "#6CB04F", "#4E8F42"][i % 3], meyve="#E2533D", isik=-1)
    for i, x in enumerate((1450, 1484, 2060)):
        s += S.kavak(s, x, 352, 150 + (i % 2) * 20, 26, 620 + i, renk="#4F8F45")
    s += Y.iskele(s, 1240, 1500, 404, 16, 625, ahsap="#A8743F", merdiven=False)
    # masa ve üç bardak (seyreltik → derişik)
    s += f'<rect x="1560" y="372" width="230" height="10" rx="3" fill="#8C5A2E"/><path d="M1578 382 v46 M1772 382 v46" stroke="#6E4422" stroke-width="7"/>'
    for k, n in enumerate((2, 5, 10)):
        bx = 1592 + k * 66
        s += f'<path d="M{bx} 314 h44 v52 q0 6 -6 6 h-32 q-6 0 -6 -6 Z" fill="#E6F6F8" stroke="{OBS}" stroke-width="2.2" opacity=".95"/>'
        s += f'<path d="M{bx + 2} 332 h40 v34 q0 4 -4 4 h-32 q-4 0 -4 -4 Z" fill="#7FD3D6" opacity=".8"/>'
        rr = RNG(630 + k)
        for _ in range(n):
            s += f'<circle cx="{f(bx + 8 + rr.uniform(0, 28))}" cy="{f(340 + rr.uniform(0, 24))}" r="3" fill="#FFFFFF" stroke="#5E8496" stroke-width="1"/>'
    s += S.sazlik(0, 240, 460, 631, boy=70)
    s += S.cimen(1380, 2100, 440, 632, renk="#4E8A3E", renk2="#7DBE55", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += S.marti(1000, 150, .9, 2)
    s += S.marti(1060, 176, .6, -1)
    s += S.marti(1120, 418, 1.1, 5, ayrintili=True)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 2. DURAK · ISPARTA GÜL BAHÇELERİ (şafak, hasat, imbikhane)

def isparta_gul():
    ufuk = 262
    s = _sahne_bas("gy-gul", duraklar=[(0, "#5465B8"), (.36, "#A58ED3"), (.62, "#FFA7C0"), (.84, "#FFD0AE"), (1, "#FFEFDA")], ufuk=ufuk)
    s += S.gunes(s, 1560, 214, 40, cekirdek="#FFF9E8", hale="#FFC9B0", hale_r=420, guc=.95)
    s += S.bulut_serit(s, 900, 120, 520, 12, "#FFE3EA", "#F6B8C8", .7)
    s += S.bulut_serit(s, 1500, 70, 460, 10, "#FFE8EE", "#F4B2C6", .6)
    uzak = ""
    d, _ = S.dag(s, 1100, 2240, ufuk, 1820, 92, 641, renk="#B6A2D4", golge="#8F82BC", bicim="sivri", kar_y=128,
                 kar="#FFFFFF", kar_golge="#DAD2EE", sis="#F6D2DE", isik=-1, sirt=4, puruz=8)
    uzak += d
    d, _ = S.dag(s, -60, 980, ufuk, 420, 168, 642, renk="#C2AEDA", golge="#9C8CC4", bicim="tepe", sis="#F8D9E2", isik=-1, sirt=2, puruz=6)
    uzak += d
    s += uzak
    # şehir silüeti (Isparta, temsilî: apartmanlar ve evler)
    r = RNG(643)
    for k in range(34):
        x = 760 + k * 32 + r.uniform(-6, 6)
        hh = r.uniform(26, 62)
        c = r.choice(["#D9C3D8", "#E6D0DE", "#CDB6CF", "#E9DCE6"])
        s += f'<rect x="{f(x)}" y="{f(ufuk - hh + 6)}" width="{f(r.uniform(22, 34))}" height="{f(hh)}" fill="{c}"/>'
        for j in range(int(hh / 14)):
            s += f'<rect x="{f(x + 5)}" y="{f(ufuk - hh + 12 + j * 13)}" width="5" height="5" fill="#B49AB8" opacity=".8"/><rect x="{f(x + 14)}" y="{f(ufuk - hh + 12 + j * 13)}" width="5" height="5" fill="#B49AB8" opacity=".8"/>'
    gk = s.lin([(0, "#C9B98A"), (.25, "#9DB46A"), (1, "#5E8E40")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="tr")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{H - ufuk}" fill="{gk}"/>'
    s += _gul_tarlasi(-20, 2120, ufuk + 22, 452, 644, sira=6)
    # çuvallar ve sepetler, imbikhane (sağ)
    s += f'<path d="M1500 {H} V346 H2100 V{H} Z" fill="#B7A27A" opacity=".55"/>'
    s += f'<rect x="1640" y="214" width="430" height="150" fill="#E7D2B0" stroke="#7A5A3A" stroke-width="3"/>'
    s += f'<path d="M1624 218 L1855 150 L2086 218 Z" fill="#B8553A" stroke="#6E2E1E" stroke-width="3"/>'
    s += f'<rect x="1700" y="132" width="34" height="86" fill="#A6532E" stroke="#5A2A14" stroke-width="2.4"/>'
    for k in range(3):
        s += f'<circle cx="{1717 + k * 18}" cy="{112 - k * 30}" r="{20 + k * 9}" fill="#FFFFFF" opacity="{f(.75 - k * .2, 2)}"/>'
    for k in range(4):
        s += f'<rect x="{1680 + k * 100}" y="240" width="40" height="44" fill="#6E8FA6" stroke="#5A3E26" stroke-width="2"/>'
    s += _imbik_kazan(s, 1720, 452, 150)
    s += _imbik_kazan(s, 1930, 452, 130)
    for k, x in enumerate((1540, 1590, 1566)):
        s += _cuval(x, 452 - (k == 2) * 30, 56)
    s += f'<path d="M1600 452 q20 -34 50 0 Z" fill="#B07C4A" stroke="#5A3A22" stroke-width="2"/>' + "".join(
        f'<circle cx="{1610 + k * 9}" cy="{438 - (k % 2) * 6}" r="6" fill="{["#E8467C", "#FF7FA8", "#D63A6E"][k % 3]}"/>' for k in range(4))
    s += _gul_yapragi(RNG(645), 26, 1100, 90, 900, 260)
    s += S.marti(1180, 120, .7, 2, renk="#5A3A6E")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 3. DURAK · BURDUR GÖLÜ (ikindi: tuzlu göl, flamingo, dikkuyruk, seyyar laboratuvar)

def burdur_golu():
    ufuk = 282
    s = _sahne_bas("gy-brd", "altin", ufuk=ufuk)
    s += S.gunes(s, 620, 120, 36, hale="#FFE0A0", hale_r=380, guc=.85)
    for i, (x, y, w_) in enumerate([(1150, 100, 260), (1600, 70, 220), (1960, 130, 160)]):
        s += S.bulut(s, x, y, w_, 650 + i, ust="#FFFFFF", alt="#F4D9B0", op=.9)
    uzak = ""
    d, _ = S.dag(s, -60, 1200, ufuk, 520, 150, 651, renk="#C9A98A", golge="#A6866E", bicim="tepe", sis="#F2DCC0", isik=-1, sirt=3, puruz=7)
    uzak += d
    d, _ = S.dag(s, 1050, 2240, ufuk, 1700, 132, 652, renk="#B99A86", golge="#94766A", bicim="tepe", sis="#F0D8BE", isik=-1, sirt=3, puruz=8)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, H - ufuk, 653, ufuk="#DDF2E0", orta="#5CC2B0", derin="#1F7C80", gunes_x=620, parilti_renk="#FFF1C4", yogunluk=1.1)
    s += S.yansima(s, uzak, ufuk, 0, W, 120, op=.22)
    # çekilen kıyının açık şeridi
    s += f'<path d="M0 {ufuk + 30} C300 {ufuk + 24} 520 {ufuk + 36} 800 {ufuk + 30} L800 {ufuk + 38} C520 {ufuk + 44} 300 {ufuk + 32} 0 {ufuk + 38} Z" fill="#F4EAD2" opacity=".75"/>'
    # Burdur evleri (uzak sağ yamaç)
    r = RNG(654)
    for k in range(18):
        s += S.ev(1240 + k * 34 + r.uniform(-6, 6), ufuk - 4 + r.uniform(-8, 6), 26, 18, 655 + k, duvar="#F3E2C6", cati="#C2563A", isik=-1)
    # flamingolar (sığlık) ve dikkuyruk ördekleri — odak sağda
    for k, (x, y, o, yon) in enumerate([(1290, 352, .95, 1), (1370, 366, 1.1, -1), (1450, 350, .9, 1), (1520, 382, 1.25, 1), (1600, 360, 1.0, -1)]):
        s += _flamingo(x, y, o, yon)
        s += f'<path d="M{f(x - 20 * o)} {f(y + 2)} q{f(20 * o)} {f(6 * o)} {f(40 * o)} 0" stroke="#FFFFFF" stroke-width="1.6" fill="none" opacity=".7"/>'
    for k, (x, y, o, yon) in enumerate([(1240, 316, .8, 1), (1300, 410, 1.1, -1), (1420, 428, 1.2, 1), (1180, 300, .7, -1)]):
        s += _dikkuyruk(x, y, o, yon)
    # sağ ön kıyı: kumsal + seyyar laboratuvar
    kiyi = [(1660, H), (1700, 390), (1800, 372), (1920, 366), (2020, 360), (2100, 356), (2100, H)]
    gk = s.lin([(0, "#E6D3A8"), (1, "#B89A6A")], 0, 350, 0, H, kull="userSpaceOnUse", ad="kk")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {H} Z" fill="{gk}"/>'
    s += S.sazlik(1630, 1760, 440, 656, boy=56)
    s += f'<rect x="1790" y="336" width="250" height="10" rx="3" fill="#8C5A2E"/><path d="M1808 346 v62 M2022 346 v62" stroke="#6E4422" stroke-width="7"/>'
    s += f'<g transform="translate(130 0)">'
    s += f'<path d="M1772 336 C1744 334 1736 312 1748 298 C1754 290 1764 288 1768 286 V244 H1786 V286 C1790 288 1800 290 1806 298 C1818 312 1810 334 1782 336 Z" fill="#E8F6F8" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M1752 312 C1756 326 1798 326 1802 312 C1806 324 1798 334 1777 334 C1756 334 1748 324 1752 312 Z" fill="#7FCFD0"/><path d="M1764 258 h26" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="M1830 336 v-40 h40 v40 Z" fill="#E8F6F8" stroke="{OBS}" stroke-width="2.2"/><path d="M1832 318 h36 v16 h-36 Z" fill="#9FD9D4"/>'
    s += f'<path d="M1700 336 v-26 h40 v26" fill="none" stroke="{OBS}" stroke-width="2"/><rect x="1702" y="316" width="36" height="20" fill="#F4E9D8"/></g>'
    s += S.cimen(1660, 2100, 452, 657, renk="#7A8F4A", renk2="#A9B86A", boy=10)
    s += S.marti(1300, 150, .8, 2, renk="#5A4A3A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 4. DURAK · SALDA GÖLÜ (öğle: turkuaz su, bembeyaz kıyı, çamlar)

def salda_golu():
    ufuk = 272
    s = _sahne_bas("gy-sal", duraklar=[(0, "#2F8FE0"), (.55, "#86CDF2"), (1, "#E6F7FC")], ufuk=ufuk)
    s += S.gunes(s, 1420, 64, 30, hale="#FFF6D0", hale_r=280, guc=.8)
    for i, (x, y, w_) in enumerate([(820, 110, 220), (1180, 80, 260), (1800, 120, 200)]):
        s += S.bulut(s, x, y, w_, 660 + i, ust="#FFFFFF", alt="#D2E6F4", op=.95)
    uzak = ""
    d, _ = S.dag(s, -80, 1100, ufuk, 420, 160, 661, renk="#6E9A86", golge="#4F7E6C", bicim="tepe", sis="#CBE8E2", isik=-1, sirt=3, puruz=7)
    uzak += d
    d, _ = S.dag(s, 1000, 2240, ufuk, 1640, 126, 662, renk="#7FA68E", golge="#5C8670", bicim="tepe", sis="#D2ECE6", isik=-1, sirt=3, puruz=7)
    uzak += d
    s += uzak
    for k in range(40):   # karşı kıyı çamları
        x = 30 + k * 52
        s += _cam(x, ufuk + 4, 38 + (k % 4) * 6, 663 + k, renk="#2F6B4C")
    s += S.gol(s, 0, ufuk, W, H - ufuk, 664, ufuk="#B8F2EA", orta="#1EC2C4", derin="#0B5E8A", gunes_x=1420, parilti_renk="#FFFBE0", yogunluk=1.2)
    s += S.yansima(s, uzak, ufuk, 0, W, 110, op=.2)
    # sığ, açık turkuaz kıyı şeridi + bembeyaz hidromanyezit kumsalı (sağ önde)
    sig = s.lin([(0, "#9FF0E6"), (1, "#56D8D2")], 0, 330, 0, 420, kull="userSpaceOnUse", ad="sg")
    s += f'<path d="M1060 {H} C1180 400 1300 360 1480 342 C1700 326 1900 324 2100 318 V{H} Z" fill="{sig}"/>'
    s += f'<path d="M1180 {H} C1290 420 1400 388 1560 372 C1760 356 1930 352 2100 348 V{H} Z" fill="#FBFBF6"/>'
    s += f'<path d="M1180 {H} C1290 420 1400 388 1560 372 C1760 356 1930 352 2100 348" fill="none" stroke="#E2EEEC" stroke-width="10"/>'
    r = RNG(665)
    for k in range(60):
        x = r.uniform(1300, 2090)
        y = r.uniform(380, 455)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r.uniform(6, 16))}" ry="{f(r.uniform(1.5, 3))}" fill="#E7EFEE" opacity=".9"/>'
    for k, (x, y) in enumerate([(1520, 380), (1590, 372), (1990, 352), (2060, 350)]):
        s += _cam(x, y, 120 + (k % 2) * 30, 666 + k, renk="#2E6B4A")
    s += '<use href="#pamuk-dusunen" x="1700" y="290" width="120" height="137"/>'
    s += f'<path d="M1840 402 h36 v-44 h-36 Z" fill="#E8F6F8" stroke="{OBS}" stroke-width="2.2"/><path d="M1842 380 h32 v20 h-32 Z" fill="#7FD3D6"/><path d="M1886 360 l26 -14" stroke="#5E8496" stroke-width="3"/>'
    s += S.marti(900, 160, .8, 2, renk="#2E4A5A")
    s += S.marti(960, 186, .55, -1, renk="#2E4A5A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 5. DURAK · DAVRAZ YOLU (kış: kar, çamlar, telesiyej, tuzlama aracı)

def davraz_kis():
    ufuk = 300
    s = _sahne_bas("gy-dvz", duraklar=[(0, "#4F86C9"), (.55, "#A9CDEB"), (1, "#EAF4FB")], ufuk=ufuk)
    s += S.gunes(s, 260, 90, 30, cekirdek="#FFFFFF", hale="#FFF6DA", hale_r=260, guc=.7)
    d, _ = S.dag(s, 900, 2260, ufuk, 1560, 60, 671, renk="#9DB2CC", golge="#6F86A8", bicim="sivri", kar_y=96,
                 kar="#FFFFFF", kar_golge="#C9D8EE", sis="#E2EEF8", isik=-1, sirt=5, puruz=10)
    s += d
    d, _ = S.dag(s, -80, 980, ufuk, 360, 150, 672, renk="#B2C4DA", golge="#8EA2C0", bicim="tepe", kar_y=170,
                 kar="#FFFFFF", kar_golge="#D6E2F2", sis="#E8F1FA", isik=-1, sirt=3, puruz=6)
    s += d
    s += _telesiyej(1300, 250, 1700, 120, n=7)
    kz = s.lin([(0, "#F6FAFE"), (1, "#D8E5F2")], 0, ufuk - 10, 0, H, kull="userSpaceOnUse", ad="kz")
    s += f'<path d="M0 {ufuk + 10} C400 {ufuk - 6} 900 {ufuk + 16} 1400 {ufuk + 4} C1700 {ufuk - 4} 1900 {ufuk + 8} 2100 {ufuk} V{H} H0 Z" fill="{kz}"/>'
    for k in range(34):
        x = 820 + k * 40
        s += _cam(x, ufuk + 14 + (k % 3) * 4, 60 + (k % 4) * 10, 673 + k, renk="#2C5E48", kar=True)
    # yol (perspektif) + kar setleri
    s += f'<path d="M1180 {H} C1300 410 1420 360 1560 330 L1640 330 C1580 370 1560 420 1600 {H} Z" fill="#7C8794"/>'
    s += f'<path d="M1390 {H} C1440 420 1520 370 1600 330" stroke="#F4F1EA" stroke-width="4" stroke-dasharray="18 16" fill="none"/>'
    s += f'<path d="M1150 {H} C1270 412 1400 360 1556 330 L1540 330 C1380 362 1250 410 1110 {H} Z" fill="#FFFFFF"/>'
    s += f'<path d="M1610 {H} C1570 420 1590 370 1646 330 L1680 332 C1620 372 1610 420 1660 {H} Z" fill="#FFFFFF"/>'
    s += _tuz_kamyonu(1440, 438, 1.05, 674)
    for k, (x, y, h_) in enumerate([(1760, 420, 170), (1860, 440, 200), (1990, 430, 180), (2070, 450, 210), (1120, 430, 150)]):
        s += _cam(x, y, h_, 680 + k, renk="#2A5A44", kar=True)
    s += f'<g transform="translate(1696 330)"><rect x="-3" y="0" width="6" height="74" fill="#5E6672"/><circle cx="0" cy="-8" r="20" fill="#FFFFFF" stroke="#E2533D" stroke-width="6"/>'
    s += f'<path d="M0 -20 V4 M-10 -14 L10 -2 M-10 -2 L10 -14" stroke="#2B50B5" stroke-width="3"/></g>'
    s += _kar_yagisi(RNG(685), 140, 0, 0, W, H)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ HÜLASA · KOVADA GÖLÜ (altın saat: çadırlar, ateş, çamlar)

def kovada(h=400):
    ufuk = 250
    s = Svg("gy-kov")
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "altin")
    s += S.gunes(s, 1680, 180, 36, hale="#FFD27A", hale_r=380, guc=.9)
    s += S.bulut_serit(s, 1200, 110, 520, 12, "#FFE6C0", "#F4B28A", .6)
    uzak = ""
    d, _ = S.dag(s, -80, 1000, ufuk, 380, 120, 691, renk="#7E9A86", golge="#5E7E6C", bicim="tepe", sis="#F2DEC0", isik=-1, sirt=3, puruz=7)
    uzak += d
    d, _ = S.dag(s, 1100, 2240, ufuk, 1880, 96, 692, renk="#8EA28A", golge="#6C846E", bicim="sivri", sis="#F4E0C4", isik=-1, sirt=3, puruz=9)
    uzak += d
    s += uzak
    for k in range(44):
        s += _cam(20 + k * 48, ufuk + 6, 44 + (k % 4) * 8, 693 + k, renk="#2F5E46")
    s += S.gol(s, 0, ufuk, W, h - ufuk, 694, ufuk="#FFE2B0", orta="#3FA6A0", derin="#0E5A66", gunes_x=1680, parilti_renk="#FFE9B0")
    s += S.yansima(s, uzak, ufuk, 0, W, 100, op=.25)
    kiyi = [(1260, h), (1320, 318), (1520, 300), (1760, 296), (1980, 300), (2100, 296), (2100, h)]
    g = s.lin([(0, "#9DBE62"), (1, "#5A8A40")], 0, 290, 0, h, kull="userSpaceOnUse", ad="kv")
    s += f'<path d="{egri_d(kiyi[:-1])} L2100 {h} Z" fill="{g}"/>'
    s += Y.cadir(s, 1600, 306, 120, 86, renk="#B23A2E")
    s += Y.cadir(s, 1760, 300, 104, 76, renk="#2B50B5", serit="#F5E8D0")
    s += f'<path d="M1690 346 l-26 12 M1690 346 l26 12 M1690 346 l0 14" stroke="#5A3A22" stroke-width="6"/>'
    s += f'<path d="M1672 344 q18 -48 36 0 q-10 -20 -18 -8 q-6 -14 -18 8 Z" fill="#FF8A3D"/><path d="M1682 344 q8 -24 16 0 Z" fill="#FFE08A"/>'
    s += f'<circle cx="1690" cy="320" r="70" fill="#FFB43A" opacity=".12"/>'
    for k, (x, y, hh) in enumerate([(1360, 330, 160), (1440, 340, 190), (1960, 330, 180), (2050, 342, 200)]):
        s += _cam(x, y, hh, 700 + k, renk="#2E5E44")
    s += '<use href="#pamuk-kitap" x="1840" y="268" width="110" height="126"/>'
    s += S.cimen(1260, 2100, h - 6, 705, renk="#4E7E3A", renk2="#86B85A", boy=12, cicek=["#FFFFFF", "#F0A21A"])
    s += S.marti(1100, 120, .8, 2, renk="#5A4A3A")
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ MECLİS · EĞİRDİR'DE GÖL MANZARALI KÖY ODASI

def koy_odasi():
    from cizim.sus import kilim_serit
    s = Svg("gy-oda")
    g = s.lin([(0, "#F7E7CB"), (1, "#EBD3AC")], 0, 0, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect width="{W}" height="{H}" fill="{g}"/>'
    s += f'<rect y="0" width="{W}" height="34" fill="#7A4E2E"/><rect y="34" width="{W}" height="8" fill="#5E3A20"/>'
    for x in range(0, W, 120):
        s += f'<rect x="{x}" y="0" width="60" height="34" fill="#8C5A35"/>'
    # pencere: Eğirdir Gölü, Yeşilada ve dağ
    wx, wy, ww, wh = 1360, 52, 440, 180
    pen = Svg("gy-oda-p")
    pen += S.gokyuzu(pen, wx, wy, ww, wh * .6, "gun")
    pd, _ = S.dag(pen, wx - 40, wx + ww + 40, wy + wh * .6, wx + ww * .62, wy + 18, 711, renk="#7C93B5", golge="#55709A",
                  bicim="sivri", kar_y=wy + 50, kar="#FFFFFF", kar_golge="#C9D8EE", sis="#C4E2EE", isik=-1, sirt=4, puruz=6)
    pen += pd
    pen += S.gol(pen, wx, wy + wh * .6, ww, wh * .4, 712, ufuk="#C8EEF0", orta="#22AEB0", derin="#0B6B78")
    pen += f'<path d="M{wx + 60} {wy + wh * .66} C{wx + 90} {wy + wh * .58} {wx + 170} {wy + wh * .57} {wx + 200} {wy + wh * .66} Z" fill="#6E8F5C"/>'
    for k in range(4):
        pen += f'<rect x="{wx + 84 + k * 26}" y="{wy + wh * .6 - (k % 2) * 4}" width="18" height="12" fill="#F3E6CC"/><path d="M{wx + 82 + k * 26} {wy + wh * .6 - (k % 2) * 4} l11 -7 l11 7 Z" fill="#C2563A"/>'
    pen += S.tekne(pen, wx + 300, wy + wh * .82, 40, govde="#C8442F", yelken="#FFF6E6")
    s.defs += pen.defs
    kl = s.klip(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}"/>', ad="pk")
    s += f'<g clip-path="{kl}">{"".join(pen.parca)}</g>'
    s += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#6E4422" stroke-width="14"/>'
    s += f'<path d="M{wx + ww / 2} {wy} V{wy + wh} M{wx} {wy + wh * .45} H{wx + ww}" stroke="#6E4422" stroke-width="8"/>'
    s += f'<rect x="{wx - 22}" y="{wy + wh + 2}" width="{ww + 44}" height="12" fill="#8C5A35"/>'
    for sx, x0 in ((-1, wx - 58), (1, wx + ww + 6)):
        s += (f'<path d="M{x0} 46 h52 C{x0 + 52} 120 {x0 + 26 + sx * 9} 190 {x0 + 42} 240 L{x0 + 8} 240 C{x0 - 8} 186 {x0 + 8} 116 {x0} 46 Z" fill="#2B6E8E"/>'
              f'<path d="M{x0 + 15} 54 C{x0 + 17} 124 {x0 + 11} 192 {x0 + 20} 236" stroke="#1E5470" stroke-width="5" fill="none"/>'
              f'<path d="M{x0} 46 h52" stroke="#F0A21A" stroke-width="7"/>')
    # duvarda Isparta halısı (madalyonlu, temsilî)
    s += f'<g transform="translate(1904 50)"><rect width="176" height="176" fill="#F5E8D0" stroke="#6E4422" stroke-width="4"/><rect x="8" y="8" width="160" height="160" fill="#7E1F2A"/>'
    s += f'<rect x="18" y="18" width="140" height="140" fill="none" stroke="#D99A2B" stroke-width="5"/>'
    s += f'<path d="M88 40 L136 88 L88 136 L40 88 Z" fill="#1E3F7A" stroke="#D99A2B" stroke-width="4"/><path d="M88 62 L114 88 L88 114 L62 88 Z" fill="#E8C27A"/><circle cx="88" cy="88" r="9" fill="#7E1F2A"/>'
    for cx, cy in ((34, 34), (142, 34), (34, 142), (142, 142)):
        s += f'<path d="M{cx} {cy - 10} l10 10 l-10 10 l-10 -10 Z" fill="#E8C27A"/>'
    s += "".join(f'<path d="M{8 + k * 18} 176 v14" stroke="#F5E8D0" stroke-width="4"/>' for k in range(10)) + '</g>'
    # raf: kitaplar, gül kolonyası şişesi, semaver
    s += f'<rect x="760" y="150" width="270" height="12" fill="#7A4E2E"/>'
    for k, (c, hh) in enumerate([("#2B50B5", 60), ("#E2533D", 70), ("#13A3A6", 54), ("#F0A21A", 66), ("#1D3A8A", 60)]):
        s += f'<rect x="{770 + k * 26}" y="{150 - hh}" width="22" height="{hh}" fill="{c}" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="M912 150 v-46 q0 -8 8 -10 v-10 h12 v10 q8 2 8 10 v46 Z" fill="#FFD3E2" stroke="{OBS}" stroke-width="2"/><rect x="916" y="118" width="20" height="18" fill="#FFFFFF" stroke="#D63A6E" stroke-width="1.6"/>'
    s += Y.semaver(s, 990, 150, 80)
    # sedir, minder, kilim
    s += f'<rect x="0" y="322" width="{W}" height="62" fill="#8E2A22"/>'
    kil = kilim_serit("gy-oda-k", 2100, 60).replace("<svg ", '<svg width="2100" height="60" ')
    s += f'<g transform="translate(0 324)">{kil}</g>'
    s += f'<rect x="-20" y="246" width="{W + 40}" height="84" rx="26" fill="#253C78" stroke="{OBS}" stroke-width="3"/>'
    s += f'<rect x="-20" y="258" width="{W + 40}" height="60" fill="#2E4A8E"/>'
    s += f'<path d="M-20 262 H{W + 20} M-20 314 H{W + 20}" stroke="#D99A2B" stroke-width="4"/>'
    for x in range(30, W, 72):
        s += f'<path d="M{x} 266 L{x + 22} 288 L{x} 310 L{x - 22} 288 Z" fill="#B23A2E" stroke="#F5E8D0" stroke-width="2.4"/><rect x="{x - 4}" y="284" width="8" height="8" fill="#F5E8D0"/>'
    s += f'<path d="M0 384 H{W} V{H} H0 Z" fill="#7A2A22"/>'
    s += f'<path d="M80 394 H{W - 80} L{W} {H} H0 Z" fill="#B23A2E"/>'
    for x in range(120, W - 100, 90):
        s += f'<path d="M{x} 406 l20 14 l-20 14 l-20 -14 Z" fill="#D99A2B"/>'
    s += '<use href="#elif-soru" x="1290" y="178" width="260" height="273"/>'
    s += '<use href="#yusuf-anlatan" x="1790" y="178" width="260" height="273"/>'
    s += f'<ellipse cx="1676" cy="440" rx="130" ry="20" fill="#C9A86A" stroke="#7A5A2A" stroke-width="4"/>'
    for x in (1606, 1648, 1690, 1732):
        s += Y.cay_bardak_kucuk(x, 440, 26)
    s += '<use href="#pamuk-dusunen" x="1580" y="236" width="180" height="206"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ KISSA · YEŞİLADA (sabah: yolla bağlanan adacık, evler, kayıklar)

def yesilada():
    ufuk = 268
    s = _sahne_bas("gy-yes", duraklar=[(0, "#5A8FD8"), (.5, "#B5D6F2"), (.85, "#FFE6CC"), (1, "#FFF2DE")], ufuk=ufuk)
    s += S.gunes(s, 1240, 200, 32, hale="#FFE8B8", hale_r=340, guc=.85)
    for i, (x, y, w_) in enumerate([(760, 100, 230), (1500, 80, 260), (1950, 130, 160)]):
        s += S.bulut(s, x, y, w_, 720 + i, ust="#FFFFFF", alt="#E8D6E2", op=.92)
    uzak = ""
    d, _ = S.dag(s, 1300, 2240, ufuk, 1820, 70, 721, renk="#8E9EC4", golge="#6B7CA6", bicim="sivri", kar_y=110,
                 kar="#FFFFFF", kar_golge="#D2DAEE", sis="#E8D8E8", isik=-1, sirt=4, puruz=10)
    uzak += d
    d, _ = S.dag(s, -80, 1000, ufuk, 420, 160, 722, renk="#A5B2D2", golge="#8494BC", bicim="tepe", sis="#EEDDE8", isik=-1, sirt=2, puruz=6)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, H - ufuk, 723, ufuk="#E8F0F4", orta="#3FB0B8", derin="#0E5E7A", gunes_x=1240, parilti_renk="#FFF0C4", yogunluk=1.15)
    s += S.yansima(s, uzak, ufuk, 0, W, 120, op=.22)
    # bağlantı yolu (soldan adaya) + fenerler
    s += f'<path d="M940 {ufuk + 70} L1430 {ufuk + 40} L1432 {ufuk + 52} L944 {ufuk + 84} Z" fill="#B9A487" stroke="#7A6248" stroke-width="2"/>'
    for k in range(8):
        x = 980 + k * 56
        y = ufuk + 70 - k * 3.8
        s += f'<path d="M{x} {f(y)} v-22" stroke="#3A3F4B" stroke-width="2.4"/><circle cx="{x}" cy="{f(y - 24)}" r="4" fill="#FFE08A"/>'
    # ada: tepecik + evler + çınarlar
    ada = [(1380, ufuk + 56), (1420, ufuk + 6), (1560, ufuk - 26), (1760, ufuk - 34), (1940, ufuk - 14), (2060, ufuk + 20), (2100, ufuk + 56)]
    ga = s.lin([(0, "#8DB06A"), (1, "#5E8A48")], 0, ufuk - 40, 0, ufuk + 60, kull="userSpaceOnUse", ad="ad")
    s += f'<path d="{egri_d(ada)} Z" fill="{ga}"/>'
    for k, (x, hh) in enumerate([(1470, 52), (1560, 60), (1650, 56), (1740, 64), (1830, 58), (1920, 54), (2000, 50)]):
        s += _ev2(x, ufuk + 30 - (k % 2) * 6 - (k in (2, 3, 4)) * 10, 70, hh, 724 + k, duvar=["#F3E6CC", "#F6DDB8", "#EFE9DD", "#F3D9C2"][k % 4])
    for k, x in enumerate((1440, 1610, 1790, 2070)):
        s += S.agac(s, x, ufuk + 34, 34, 732 + k, renk="#4E8F42", isik=-1)
    s += f'<path d="M1380 {ufuk + 56} H2100 V{ufuk + 66} H1380 Z" fill="#C9B796"/>'
    # kayıklar
    s += S.tekne(s, 1300, ufuk + 112, 90, govde="#2B50B5", ust="#F4E9D8")
    s += S.tekne(s, 1560, ufuk + 140, 110, govde="#C8442F", ust="#F4E9D8")
    s += S.tekne(s, 820, ufuk + 96, 60, govde="#F4E9D8", yelken="#FFFFFF")
    s += S.sazlik(0, 220, 460, 736, boy=64)
    s += S.marti(1100, 130, .9, 2)
    s += S.marti(1160, 156, .6, -2)
    s += S.marti(1840, 410, 1.1, 5, ayrintili=True)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ ANAHTAR · EĞİRDİR İSKELESİ (gün batımı)

def egirdir_iskele():
    ufuk = 282
    s = _sahne_bas("gy-isk", duraklar=[(0, "#34408E"), (.38, "#8E6FB8"), (.7, "#FF9A9A"), (1, "#FFD39A")], ufuk=ufuk)
    s += S.gunes(s, 1240, 232, 40, hale="#FFC27A", hale_r=400, guc=.9)
    s += S.bulut_serit(s, 1050, 150, 560, 14, "#FFD0C4", "#F28FA0", .7)
    s += S.bulut_serit(s, 1550, 92, 480, 12, "#FFC9B8", "#E9849C", .6)
    uzak = ""
    d, _ = S.dag(s, -60, 860, ufuk, 300, 186, 741, renk="#8E7BA8", golge="#6E5C8E", bicim="tepe", sis="#F6B8A8", isik=1, sirt=2, puruz=5)
    uzak += d
    d, _ = S.dag(s, 1500, 2240, ufuk, 1860, 120, 742, renk="#7A6896", golge="#5C4C7A", bicim="sivri", sis="#F2A8A0", isik=1, sirt=4, puruz=9)
    uzak += d
    s += uzak
    s += _sur(s, 1560, 2060, ufuk + 4, 54, 743, tas="#A88C98", tugla="#8E5A60", kule_n=3, kirik=.7)
    s += S.gol(s, 0, ufuk, W, H - ufuk, 744, ufuk="#FBC9A8", orta="#5E8FB0", derin="#1D3F6A", gunes_x=1240, parilti_renk="#FFE2A8")
    s += S.yansima(s, uzak, ufuk, 0, W, 120, op=.28)
    x0u, x1u = 1430, 1600
    s += f'<path d="M{x0u} {ufuk + 48} L{x1u} {ufuk + 48} L{x1u + 120} {H} L{x0u - 220} {H} Z" fill="#9A6B42"/>'
    for k in range(14):
        t = k / 14
        y = ufuk + 48 + (H - ufuk - 48) * t ** 1.3
        s += f'<path d="M{f(x0u - 220 * t ** 1.3)} {f(y)} H{f(x1u + 120 * t ** 1.3)}" stroke="#6E4A2C" stroke-width="{f(1 + 2 * t)}"/>'
    for (x, y, hh) in [(x0u + 8, ufuk + 48, 28), (x1u - 8, ufuk + 48, 28), (x0u - 60, ufuk + 108, 44), (x1u + 30, ufuk + 108, 44), (x0u - 150, ufuk + 158, 60)]:
        s += f'<rect x="{f(x - hh * .12)}" y="{f(y - hh)}" width="{f(hh * .24)}" height="{hh}" fill="#5A3A22"/>'
        s += f'<circle cx="{x}" cy="{y - hh}" r="{f(hh * .14)}" fill="#FFD27A"/>'
    s += S.tekne(s, 1800, ufuk + 96, 120, govde="#2B50B5", ust="#F4E9D8")
    s += S.tekne(s, 1960, ufuk + 132, 130, govde="#C8442F", ust="#F4E9D8")
    s += f'<path d="M1740 {ufuk + 118} q40 20 80 0" stroke="#E8D3A8" stroke-width="4" fill="none" stroke-dasharray="6 5"/>'
    s += '<use href="#pamuk-akce" x="1640" y="300" width="120" height="137"/>'
    s += S.marti(1150, 140, 1.0, 2, renk="#2F2A4A")
    s += S.marti(1210, 168, .7, -2, renk="#2F2A4A")
    s += S.marti(1100, 410, 1.1, 4, ayrintili=True)
    s += _cerceve_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ BÜYÜK İMTİHAN 1 · EĞİRDİR KALESİ (62 mm: yarımadada yer yer yıkık surlar)

def egirdir_kalesi(h=620):
    s = Svg("gy-kal")
    ufuk = 400
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#2F5DA8"), (.4, "#8EB0DA"), (.72, "#F6D0A4"), (1, "#FFC07A")])
    s += S.gunes(s, 300, 300, 50, hale="#FFC46A", hale_r=520, guc=.95)
    for i, (x, y, w_) in enumerate([(620, 140, 300), (1080, 92, 360), (1560, 150, 280), (1900, 80, 220)]):
        s += S.bulut(s, x, y, w_, 750 + i, ust="#FFF4E4", alt="#F0B08A", op=.95)
    uzak = ""
    d, _ = S.dag(s, 1180, 2260, ufuk, 1700, 110, 751, renk="#9C86A8", golge="#76628C", bicim="sivri", kar_y=150,
                 kar="#FFF1EC", kar_golge="#D6BED2", sis="#F6C8A8", isik=-1, sirt=5, puruz=12, kenar_isik="#FFD9C0")
    uzak += d
    d, _ = S.dag(s, -80, 860, ufuk, 320, 300, 752, renk="#A893AE", golge="#86709A", bicim="tepe", sis="#F6C6AA", isik=-1, sirt=2, puruz=5)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, h - ufuk, 753, ufuk="#FFD8B0", orta="#3FA9B0", derin="#0F5A6E", gunes_x=300, parilti_renk="#FFE6A8")
    s += S.yansima(s, uzak, ufuk, 0, W, 140, op=.25)
    # yarımada: kayalık zemin + kasaba evleri (sol) + kale kalıntısı (sağ)
    yar = [(620, h), (680, ufuk + 80), (900, ufuk + 56), (1200, ufuk + 44), (1600, ufuk + 40), (2000, ufuk + 46), (2140, ufuk + 60), (2140, h)]
    gz = s.lin([(0, "#C9B27E"), (1, "#7E8A4A")], 0, ufuk + 40, 0, h, kull="userSpaceOnUse", ad="yz")
    s += f'<path d="{egri_d(yar[:-1])} L2140 {h} Z" fill="{gz}"/>'
    r = RNG(754)
    for k in range(10):
        s += S.ev(720 + k * 46 + r.uniform(-6, 6), ufuk + 74 + r.uniform(-6, 8), 36, 26, 755 + k, duvar=r.choice(["#F3E2C6", "#F6DDB8", "#EFE9DD"]), cati="#C2563A", isik=-1)
    for k in range(6):
        s += S.kavak(s, 700 + k * 80, ufuk + 96, 120 + (k % 3) * 20, 24, 766 + k, renk="#5E8A40")
    s += _sur(s, 1200, 2120, ufuk + 156, 210, 772, tas="#D2BA92", tugla="#B5653E", isik=-1, kule_n=4, kirik=.55)
    s += _sur(s, 1080, 1420, ufuk + 190, 120, 773, tas="#C8AE86", tugla="#A85A36", isik=-1, kule_n=1, kirik=.8)
    for k in range(8):
        x = 1150 + k * 120 + r.uniform(-30, 30)
        s += f'<path d="M{f(x)} {h} q{f(r.uniform(10, 30))} {f(-r.uniform(20, 50))} {f(r.uniform(30, 60))} 0 Z" fill="#6E8A44"/>'
    s += S.cimen(1050, 2140, h - 4, 774, renk="#5E8A3E", renk2="#8DB85A", boy=16, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += S.tekne(s, 320, ufuk + 110, 90, govde="#2B50B5", yelken="#FFF1DE")
    s += S.tekne(s, 520, ufuk + 160, 70, govde="#C8442F")
    s += S.sazlik(0, 380, h, 775, boy=90)
    for k, (x, y, o) in enumerate([(880, 210, 1.1), (950, 240, .8), (1340, 120, .7), (1400, 150, .5)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ BÜYÜK İMTİHAN 2 · SUR DİBİ (30 mm: almaşık duvar, kemerli geçit, sancaklar)

def sur_dibi(h=300):
    s = Svg("gy-sur")
    s += S.gokyuzu(s, 0, 0, W, h, duraklar=[(0, "#F7B07A"), (1, "#FFE1B0")])
    g = s.lin([(0, "#E1C79E"), (1, "#B8946A")], 0, 40, 0, h, kull="userSpaceOnUse", ad="sd")
    ust = [(0, 70)]
    r = RNG(781)
    for x in range(60, W + 60, 60):
        ust.append((x, 54 + r.uniform(0, 40) + (30 if 400 < x < 700 else 0)))
    d = cizgi_d(ust + [(W, h), (0, h)], True)
    s += f'<path d="{d}" fill="{g}" stroke="#8C6E4A" stroke-width="3"/>'
    kl = s.klip(f'<path d="{d}"/>', ad="sk")
    ic = []
    for row in range(9):
        y = 60 + row * 30
        if row % 3 == 2:
            ic.append(f'<rect x="0" y="{y}" width="{W}" height="12" fill="#B5653E"/><rect x="0" y="{y + 14}" width="{W}" height="12" fill="#A85A36"/>')
            continue
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            ic.append(f'<rect x="{x + 2}" y="{y + 2}" width="86" height="26" rx="3" fill="{karis("#E3C79A", "#B8946A", r.uniform(0, .6))}" stroke="#8C6E4A" stroke-width="1.6"/>')
    s += f'<g clip-path="{kl}">{"".join(ic)}</g>'
    cx = 1450
    s += f'<path d="M{cx - 160} {h} V150 Q{cx - 160} 84 {cx} 66 Q{cx + 160} 84 {cx + 160} 150 V{h} Z" fill="#8C6E4A"/>'
    s += f'<path d="M{cx - 128} {h} V156 Q{cx - 128} 104 {cx} 90 Q{cx + 128} 104 {cx + 128} 156 V{h} Z" fill="#FFE9A8"/>'
    isik = s.rad([(0, "#FFF4C8", .95), (.5, "#FFD27A", .45), (1, "#FFD27A", 0)], cx, 210, 280, kull="userSpaceOnUse", ad="ki")
    s += f'<circle cx="{cx}" cy="210" r="280" fill="{isik}"/>'
    s += f'<path d="M{cx - 128} {h} L{cx - 420} {h} L{cx - 128} 170 Z M{cx + 128} {h} L{cx + 420} {h} L{cx + 128} 170 Z" fill="#FFE9A8" opacity=".3"/>'
    for k in range(3):
        s += f'<path d="M{cx - 40 + k * 40} {h} l-8 -40 l16 0 Z" fill="#E8D2A0" opacity=".6"/>'
    for k, (x, c) in enumerate(((760, "#B23A2E"), (2000, "#13A3A6"))):
        s += f'<path d="M{x - 60} 70 H{x + 60} V230 L{x} 270 L{x - 60} 230 Z" fill="{c}" stroke="#3A2614" stroke-width="3"/>'
        s += f'<path d="M{x - 60} 82 H{x + 60}" stroke="#C9952B" stroke-width="6"/>'
        s += f'<path d="{cizgi_d(selcuklu_yildizi(x, 160, 40), True)}" fill="#C9952B" stroke="#3A2614" stroke-width="2"/><circle cx="{x}" cy="160" r="14" fill="{c}"/>'
    for k in range(10):
        x = r.uniform(0, W)
        s += f'<path d="M{f(x)} {h} q{f(r.uniform(6, 14))} {f(-r.uniform(16, 34))} {f(r.uniform(18, 30))} 0 Z" fill="#6E8A44"/>'
    s += '<use href="#pamuk-akce" x="1680" y="128" width="150" height="171"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ CEVAPLAR · EĞİRDİR'DE GECE (30 mm)

def egirdir_gece(h=360):
    s = Svg("gy-gec")
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 30, 150, 791)
    s += S.ay(s, 1300, 80, 32, golge_renk="#13204A")
    d, _ = S.dag(s, 1380, 2240, ufuk, 1820, 60, 792, renk="#26315E", golge="#1A2248", bicim="sivri", kar_y=96, kar="#C8D2F0", kar_golge="#8F9CC8", isik=1, sirt=3, puruz=8)
    s += d
    d2, _ = S.dag(s, -60, 900, ufuk, 320, 120, 793, renk="#283565", golge="#1C2650", bicim="tepe", isik=1, sirt=2, puruz=5)
    s += d2
    sur = _sur(s, 1440, 2000, ufuk + 4, 60, 794, tas="#3A3F66", tugla="#2E3358", kule_n=3, kirik=.7)
    s += sur
    s += S.gol(s, 0, ufuk, W, h - ufuk, 795, ufuk="#3A5A9A", orta="#1D3366", derin="#0B1636", gunes_x=1300, parilti_renk="#FFF0C0", cizgi_renk="#9FB4E8")
    s += S.yansima(s, d + d2 + sur, ufuk, 0, W, 80, op=.3)
    r = RNG(796)
    for k in range(46):
        x = 900 + r.uniform(0, 1150)
        s += f'<circle cx="{f(x)}" cy="{f(ufuk + r.uniform(-4, 6))}" r="{f(r.uniform(1.4, 3))}" fill="#FFD27A" opacity="{f(r.uniform(.6, 1), 2)}"/>'
    s += S.tekne(s, 600, ufuk + 50, 70, govde="#1D3A8A", ust="#C9D6EA")
    s += f'<circle cx="610" cy="{ufuk + 22}" r="16" fill="#FFD27A" opacity=".35"/><circle cx="610" cy="{ufuk + 22}" r="5" fill="#FFE9A8"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ FİNAL · YOLCULUK TAMAMLANDI (90 mm: alacakaranlıkta havai fişek, sur burcunda Pamuk, nişan çelengi)

def final_goller(h=900, nisanlar=None):
    s = Svg("gy-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, duraklar=[(0, "#1B1F5E"), (.3, "#4B3C8E"), (.55, "#C9467F"), (.75, "#FF7A5C"), (.9, "#FFB45A"), (1, "#FFD98A")])
    s += S.yildizlar(s, 0, 0, W, 220, 60, 801)
    gx, gy = 760, ufuk - 24
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE0A0" opacity=".1"/>'
    s += S.gunes(s, gx, gy, 66, hale="#FFC56B", hale_r=640, guc=.95)
    for (x, y, w_, k) in ((200, 300, 520, 22), (1200, 250, 600, 26), (100, 440, 380, 12)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFC59A", "#FF6F8A", .7)
    for (x, y, R, c, t) in ((1180, 150, 110, "#FFD27A", 802), (1500, 90, 80, "#FF7FA8", 803), (1880, 190, 95, "#7FE0E0", 804), (980, 300, 70, "#FF9A5C", 805), (2020, 60, 60, "#FFE9A8", 806)):
        s += _fisek(x, y, R, c, t)
    uzak = ""
    d, _ = S.dag(s, 1000, 1900, ufuk, 1420, 330, 807, renk="#C98AA6", golge="#7E5A92", bicim="sivri", kar_y=390,
                 kar="#FFE3EC", kar_golge="#C7A6CF", sis="#FF9A8A", isik=-1, sirt=4, kenar_isik="#FFD3B8")
    uzak += d
    d, _ = S.dag(s, -100, 820, ufuk, 300, 430, 808, renk="#6B4C86", golge="#4E3A6E", bicim="tepe", sis="#E07A8A", isik=-1, sirt=2, puruz=6)
    uzak += d
    s += uzak
    s += S.gol(s, 0, ufuk, W, h - ufuk, 809, ufuk="#FFB59A", orta="#C86A9A", derin="#2D3A7A", gunes_x=gx, parilti_renk="#FFE3A0")
    s += S.yansima(s, uzak, ufuk, 0, W, 200, op=.3)
    s += S.tekne(s, 420, ufuk + 80, 80, govde="#2B50B5", yelken="#FFF1DE")
    for k, (x, y, o) in enumerate([(560, 210, 1.3), (640, 248, .9), (300, 170, .7)]):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    # ön plan: almaşık sur kalıntısı (üst kenarı yer yer yıkık) + sağda yıkık burç
    gb = s.lin([(0, "#E8C998"), (1, "#A9845A")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    r = RNG(810)
    ust = [(0, 700)]
    for x in range(80, 1580, 80):
        ust.append((x, 686 + r.uniform(0, 34)))
    d = cizgi_d(ust + [(1580, 700), (1580, h), (0, h)], True)
    s += f'<path d="{d}" fill="{gb}" stroke="#8C6E4A" stroke-width="3"/>'
    kl = s.klip(f'<path d="{d}"/>', ad="bk")
    bb = []
    for row in range(7):
        y = 712 + row * 28
        if row % 3 == 1:
            bb.append(f'<rect x="0" y="{y}" width="1580" height="11" fill="#B5653E"/><rect x="0" y="{y + 13}" width="1580" height="11" fill="#A85A36"/>')
            continue
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, 1580, 90):
            bb.append(f'<rect x="{x + 2}" y="{y}" width="86" height="25" rx="3" fill="{karis("#E8C998", "#B08B60", r.uniform(0, .6))}" stroke="#8C6E4A" stroke-width="1.6"/>')
    s += f'<g clip-path="{kl}">{"".join(bb)}</g>'
    kd = cizgi_d([(1560, h), (1560, 580), (1620, 566), (1700, 590), (1780, 560), (1860, 576), (1940, 556), (2000, 572), (2000, h)], True)
    s += f'<path d="{kd}" fill="url(#{s.onek}-tk)" stroke="#8C6E4A" stroke-width="3"/>'
    s.tanim(f'<linearGradient id="{s.onek}-tk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F2D7A8"/><stop offset=".6" stop-color="#D9B482"/><stop offset="1" stop-color="#A9845A"/></linearGradient>')
    kk = s.klip(f'<path d="{kd}"/>', ad="kk")
    s += f'<g clip-path="{kk}">' + "".join(f'<rect x="1560" y="{620 + j * 70}" width="440" height="12" fill="#B5653E"/>' for j in range(4)) + '</g>'
    s += f'<path d="M1760 {h} V770 Q1760 728 1790 720 Q1820 728 1820 770 V{h} Z" fill="#5A3A22"/>'
    s += '<use href="#pamuk-bayrak" x="1600" y="170" width="340" height="400"/>'
    # nişan çelengi
    s += f'<path d="M260 650 V330" stroke="#6B4A2E" stroke-width="10"/><circle cx="260" cy="324" r="10" fill="#C9952B"/>'
    s += f'<path d="M260 360 Q900 520 1640 350" stroke="#5A3A22" stroke-width="4" fill="none"/>'
    if nisanlar:
        for k, ns in enumerate(nisanlar):
            t = (k + .6) / (len(nisanlar) + .2)
            x = (1 - t) ** 2 * 260 + 2 * (1 - t) * t * 900 + t * t * 1640
            y = (1 - t) ** 2 * 360 + 2 * (1 - t) * t * 520 + t * t * 350
            s += f'<path d="M{f(x)} {f(y)} v18" stroke="#5A3A22" stroke-width="3"/>'
            s += f'<g transform="translate({f(x - 62)} {f(y + 14)}) rotate({f((k % 2 * 2 - 1) * 5)} 62 70)">{ns}</g>'
    s += _gul_yapragi(r, 70, 280, 60, 1700, 600)
    s += _konfeti(r, 40, 300, 80, 1600, 560)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ------------------------------------------------------------------ AÇILIŞ · GÖLLER YOLU PANORAMASI + TUR ROTASI

# yaklaşık kıyı çizgileri (enlem, boylam) — stilize harita için; çizim temsilîdir
EGIRDIR = [(37.86, 30.86), (37.875, 30.82), (37.92, 30.80), (37.98, 30.775), (38.04, 30.765), (38.10, 30.79), (38.15, 30.84),
           (38.20, 30.88), (38.25, 30.93), (38.285, 30.985), (38.265, 31.03), (38.215, 31.0), (38.16, 30.98), (38.11, 31.0),
           (38.06, 30.975), (38.0, 30.93), (37.94, 30.91), (37.89, 30.895)]
BURDUR = [(37.655, 30.0), (37.69, 30.05), (37.73, 30.11), (37.77, 30.18), (37.80, 30.25), (37.815, 30.31), (37.79, 30.325),
          (37.755, 30.27), (37.72, 30.21), (37.685, 30.14), (37.65, 30.07), (37.635, 30.02)]
# işaret yerleri (temsilî; Eğirdir çevresindeki yan yollar okunur olsun diye biraz açıldı)
PAN_YER = {"1": (38.17, 30.85, "durak"), "2": (37.80, 30.49, "durak"), "3": (37.77, 30.235, "durak"), "4": (37.555, 29.705, "durak"),
           "5": (37.69, 30.66, "durak"), "H": (37.62, 30.875, "hulasa"), "M": (37.74, 31.03, "yan"), "K": (37.893, 30.838, "yan"),
           "A": (38.0, 30.775, "yan"), "V": (37.848, 30.872, "kale")}
SIRA = ["1", "2", "3", "4", "5", "H", "M", "K", "A", "V"]
ROTA_ARA = {("1", "2"): [(38.10, 30.76), (37.95, 30.65), (37.86, 30.57)], ("2", "3"): [(37.79, 30.37)], ("3", "4"): [(37.70, 30.02), (37.62, 29.84)],
            ("4", "5"): [(37.56, 29.93), (37.60, 30.20), (37.64, 30.45)], ("5", "H"): [(37.64, 30.78)],
            ("H", "M"): [(37.67, 30.98)], ("M", "K"): [(37.81, 30.96), (37.87, 30.90)], ("K", "A"): [(37.95, 30.82)], ("A", "V"): [(37.92, 30.79), (37.87, 30.83)]}


def _p(enl, boy, ufuk=330, ust=372, alt=1080):
    """Hafif eğik, kuşbakışına yakın izdüşüm (kuzey yukarıda). Döner: x, y, ölçek."""
    u = (boy - 29.50) / (31.10 - 29.50)
    v = (enl - 37.48) / (38.32 - 37.48)
    k = .6
    z = 1 + v * k
    X = W / 2 + (u - .5) * 2000 / z
    t = (1 / z - 1 / (1 + k)) / (1 - 1 / (1 + k))
    return X, ust + (alt - ust) * t, 1 / z


def _kiyi(noktalar, tohum, kap=True):
    r = RNG(tohum)
    out = []
    n = len(noktalar)
    for i, (a, b) in enumerate(noktalar):
        a2, b2 = noktalar[(i + 1) % n]
        for t in (0, .5):
            aa, bb = a + (a2 - a) * t, b + (b2 - b) * t
            if t:
                aa += r.uniform(-.006, .006)
                bb += r.uniform(-.008, .008)
            out.append(_p(aa, bb)[:2])
    return out


def _elips(enl, boy, re, rb, n=20):
    return [(enl + re * math.sin(2 * math.pi * i / n), boy + rb * math.cos(2 * math.pi * i / n)) for i in range(n)]


def panorama_goller(h=1100):
    s = Svg("gy-pan")
    ufuk = 340
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2E3A8E"), (.3, "#7A68BE"), (.6, "#FF9DB8"), (.82, "#FFC79E"), (1, "#FFE6C4")])
    gx, gy = 1840, ufuk - 34
    for k in range(12):
        a0 = math.pi + .1 + k * (math.pi - .2) / 12
        a1 = a0 + .05
        s += f'<path d="M{gx} {gy} L{f(gx + 2400 * math.cos(a0))} {f(gy + 2400 * math.sin(a0))} L{f(gx + 2400 * math.cos(a1))} {f(gy + 2400 * math.sin(a1))} Z" fill="#FFE8C8" opacity=".09"/>'
    s += S.gunes(s, gx, gy, 46, hale="#FFC9A8", hale_r=560, guc=.95)
    for (x, y, w_, k) in ((900, 120, 560, 18), (1420, 80, 600, 22), (1100, 230, 420, 10)):
        s += S.bulut_serit(s, x, y, w_, k, "#FFD3E0", "#FF8FB0", .75)
    uzak = ""
    d, _ = S.dag(s, -200, 820, ufuk + 8, 300, 196, 811, renk="#B48CB8", golge="#7E5C96", bicim="tepe", sis="#FFB4C0", isik=1, sirt=3, puruz=8)
    uzak += d
    d, _ = S.dag(s, 620, 1420, ufuk + 8, 1020, 220, 812, renk="#A786B6", golge="#76608F", bicim="tepe", sis="#FFB8C2", isik=1, sirt=3, puruz=8)
    uzak += d
    d, _ = S.dag(s, 1260, 2300, ufuk + 8, 1820, 178, 813, renk="#9E7EAE", golge="#715A8C", bicim="sivri", kar_y=214,
                 kar="#FFE8EE", kar_golge="#D2B6D6", sis="#FFB4BC", isik=1, sirt=4, puruz=9, kenar_isik="#FFD7C2")
    uzak += d
    s += uzak
    gk = s.lin([(0, "#C9A0A8"), (.1, "#C9B08A"), (.4, "#A9B262"), (1, "#5E8E40")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kara")
    s += f'<rect x="0" y="{ufuk + 4}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    r = RNG(814)
    for _ in range(110):     # tarla yamaları; Isparta çevresinde pembe gül bahçeleri
        enl, boy = r.uniform(37.45, 38.3), r.uniform(29.45, 31.15)
        x, y, sc = _p(enl, boy)
        pembe = abs(enl - 37.80) < .07 and abs(boy - 30.47) < .16
        w_ = r.uniform(60, 140) * sc * (1.3 if pembe else 1)
        hh = w_ * .42
        c = r.choice(["#F48FB1", "#FF9EBF", "#E8779E"]) if pembe else r.choice(["#B9B65E", "#8FB24E", "#D3B86A", "#7AA84A", "#C9A04E"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w_)} {f(-hh * .2)} l{f(-w_ * .2)} {f(hh)} l{f(-w_)} {f(hh * .2)} Z" fill="{c}" opacity="{".9" if pembe else ".45"}"/>'
        if pembe:
            for j in range(3):
                s += f'<path d="M{f(x - w_ * .05 * j)} {f(y + hh * (.25 + .25 * j))} h{f(w_ * .85)}" stroke="#D63A6E" stroke-width="2.2" stroke-dasharray="3 5" opacity=".8"/>'
    # dağlar: Barla (Eğirdir batısı), Dedegöl yönü (doğu), Davraz (karlı)
    for (enl, boy, yuk, gen, renk, golge, tohum, kar) in ((38.06, 30.66, 120, 230, "#9A8CB0", "#76688F", 815, False),
                                                          (38.02, 31.08, 130, 240, "#8E80A8", "#6A5C88", 816, True),
                                                          (37.72, 30.70, 120, 300, "#8E7AA6", "#6A5888", 817, True)):
        x, y, sc = _p(enl, boy)
        d, _ = S.dag(s, x - gen / 2, x + gen / 2, y + 26, x, y - yuk, tohum, renk=renk, golge=golge, bicim="sivri",
                     kar_y=(y - yuk * .55) if kar else None, kar="#FFFFFF", kar_golge="#D8CDEA", sis="#C9B08A", isik=-1, sirt=4, puruz=8,
                     kenar_isik="#FFD7C2")
        s += d
    # göller
    def gol_ciz(pts, ad, renkler, kenar="#FFF3D6", kenar_w=5, ic_parilti=30):
        gg = s.lin(renkler, 0, min(p[1] for p in pts), 0, max(p[1] for p in pts) + 40, kull="userSpaceOnUse", ad=ad)
        gd = egri_d(pts, True, .9)
        out = f'<path d="{gd}" fill="#F3E0B8" transform="translate(0 5)"/><path d="{gd}" fill="{gg}"/>'
        kl = s.klip(f'<path d="{gd}"/>', ad=ad + "k")
        ic = []
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        for _ in range(ic_parilti):
            y = r.uniform(min(ys), max(ys))
            x = r.uniform(min(xs), max(xs))
            ic.append(f'<path d="M{f(x)} {f(y)} h{f(r.uniform(8, 26))}" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" opacity="{f(r.uniform(.3, .65), 2)}"/>')
        out += f'<g clip-path="{kl}">{"".join(ic)}</g>'
        out += f'<path d="{gd}" fill="none" stroke="{kenar}" stroke-width="{kenar_w}" opacity=".9"/>'
        return out
    s += gol_ciz(_kiyi(EGIRDIR, 818), "eg", [(0, "#7FD8DA"), (.4, "#2AB2BA"), (1, "#0E7A88")], ic_parilti=50)
    s += gol_ciz(_kiyi(BURDUR, 819), "bu", [(0, "#CDEEDC"), (.4, "#7CCDBA"), (1, "#3A9C92")], ic_parilti=40)
    s += gol_ciz([_p(*q)[:2] for q in _elips(37.555, 29.668, .03, .04)], "sa", [(0, "#8FF0E6"), (1, "#14A9B4")], kenar="#FFFFFF", kenar_w=12)
    s += gol_ciz([_p(*q)[:2] for q in _elips(37.625, 30.875, .03, .012)], "kv", [(0, "#9FD6C8"), (1, "#2E8E86")], ic_parilti=6)
    s += gol_ciz([_p(*q)[:2] for q in _elips(37.733, 30.488, .01, .013)], "gc", [(0, "#5FB8B0"), (1, "#1E6E70")], ic_parilti=3)
    # Yeşilada (evli adacık) ve Eğirdir yarımadası
    yx, yy, ysc = _p(37.893, 30.838)
    s += f'<ellipse cx="{f(yx)}" cy="{f(yy)}" rx="{f(22 * ysc * 2)}" ry="{f(8 * ysc * 2)}" fill="#7E9A5E" stroke="#F3E0B8" stroke-width="2"/>'
    for k in range(3):
        s += f'<rect x="{f(yx - 16 + k * 11)}" y="{f(yy - 8)}" width="8" height="6" fill="#F3E6CC"/><path d="M{f(yx - 17 + k * 11)} {f(yy - 8)} l5 -4 l5 4 Z" fill="#C2563A"/>'
    for (enl, boy, n, sk) in ((37.765, 30.555, 26, 1.1), (37.718, 30.29, 16, 1.0), (37.872, 30.87, 8, .9)):
        x, y, sc = _p(enl, boy)
        for k in range(n):
            s += S.ev(x - 70 * sc + r.uniform(0, 140 * sc), y - 18 * sc + r.uniform(0, 36 * sc), 22 * sc * 1.5 * sk, 16 * sc * 1.5 * sk, 820 + k, duvar="#F3E2C6", cati="#C2563A", isik=-1)
    x, y, sc = _p(37.80, 30.49)
    s += _imbik_kazan(s, x - 96, y + 36, 50)
    x, y, sc = _p(37.625, 30.87)
    s += Y.cadir(s, x + 40, y + 14, 34, 26, renk="#9E2F28")
    for k in range(8):
        x, y, sc = _p(37.555 + r.uniform(-.06, .06), 29.668 + r.choice((-1, 1)) * r.uniform(.05, .08))
        s += _cam(x, y + 10, 40 * sc * 1.4, 840 + k, renk="#2F6B4C")
    for k in range(70):    # kavaklar, elma bahçeleri
        enl, boy = r.uniform(37.5, 38.25), r.uniform(29.5, 31.1)
        x, y, sc = _p(enl, boy)
        if y < ufuk + 60:
            continue
        if r.random() < .55:
            s += S.kavak(s, x, y, 56 * sc * 1.5, 11 * sc * 1.5, 850 + k, renk="#5E9A4A", isik=-1)
        else:
            s += S.agac(s, x, y, 12 * sc * 1.5, 950 + k, renk="#6FAA4E", meyve="#E2533D" if boy > 30.7 else None)
    # rota
    konum = {k: _p(a, b)[:2] for k, (a, b, _t) in PAN_YER.items()}
    yol = []
    for i, k in enumerate(SIRA):
        yol.append(konum[k])
        if i + 1 < len(SIRA):
            yol += [_p(a, b)[:2] for a, b in ROTA_ARA.get((k, SIRA[i + 1]), [])]
    yd = egri_d(yol, False, .9)
    s += f'<path d="{yd}" fill="none" stroke="{OBS}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
    s += f'<path d="{yd}" fill="none" stroke="#FFF1CF" stroke-width="9.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{yd}" fill="none" stroke="#E08A1A" stroke-width="3" stroke-dasharray="12 9" stroke-linecap="round"/>'
    for k in SIRA:
        x, y = konum[k]
        tur = PAN_YER[k][2]
        if tur == "durak":
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 34), True)}" fill="#F0C14A" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<path d="{cizgi_d(selcuklu_yildizi(x, y, 27), True)}" fill="#13A3A6" stroke="{OBS}" stroke-width="2" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 10)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#FFFFFF">{k}</text>'
        elif tur == "kale":
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="32" fill="#E2533D" stroke="{OBS}" stroke-width="3"/>'
            s += f'<path d="M{f(x - 18)} {f(y + 14)} V{f(y - 6)} h6 v-6 h6 v6 h4 v-6 h6 v6 h4 v-6 h6 v6 h4 V{f(y + 14)} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6"/>'
        else:
            renk = "#F0A21A" if tur == "yan" else "#7B3F8C"
            s += f'<path d="M{f(x)} {f(y - 30)} L{f(x + 30)} {f(y)} L{f(x)} {f(y + 30)} L{f(x - 30)} {f(y)} Z" fill="{renk}" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>'
            s += f'<text x="{f(x)}" y="{f(y + 9)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="25" fill="#FFFFFF">{k}</text>'
    x, y = konum["1"]
    s += f'<path d="M{f(x + 34)} {f(y + 36)} v-62" stroke="{OBS}" stroke-width="4"/><path d="M{f(x + 36)} {f(y - 24)} h42 l-10 12 l10 12 h-42 Z" fill="#E2533D" stroke="{OBS}" stroke-width="2.4"/>'
    # göl adları (halolu yazı)
    for enl, boy, ad, fs, dx in ((38.285, 30.98, "Eğirdir Gölü", 40, -150), (37.70, 30.10, "Burdur Gölü", 42, -40), (37.505, 29.67, "Salda", 38, 0)):
        x, y, _ = _p(enl, boy)
        s += halolu_yazi(f'x="{f(x + dx)}" y="{f(y)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="{fs}"', ad, "#FFFFFF", "#0A5A66", 1.6)
    x, y, _ = _p(37.72, 30.45)
    s += halolu_yazi(f'x="{f(x)}" y="{f(y)}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" letter-spacing="1.4"', "ISPARTA · GÜL BAHÇELERİ", "#FFFFFF", "#8E2A4E", 1.4)
    for k, (x, y, o) in enumerate(((1000, 190, 1.1), (1070, 222, .8), (1480, 140, .8), (1540, 166, .6))):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    px, py = 160, 330
    s += f'<circle cx="{px}" cy="{py}" r="74" fill="#FFFFFF" opacity=".9" stroke="{OBS}" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 66, 14, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 34), True)}" fill="#13A3A6" stroke="{OBS}" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="10" fill="#F0A21A" stroke="{OBS}" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 76}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="{OBS}">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), konum
