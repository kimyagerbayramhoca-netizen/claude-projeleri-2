"""Çözünme ve Çözünürlük · Pamukkale–Afyon Yolu · üniteye özel sahneler ve nişan ikonları.

kur_ortak {{sahne|ad}} için önce bu modüle bakar. Ortak kütüphane (yerel-ortak/cizim) DEĞİŞTİRİLMEZ; buradaki
parçalar ortak parçalardan (gökyüzü, dağ, kavak, bulut, ev …) kurulur.

Kompozisyon (TASARIM-SISTEMI.md §6): bant 2100×460 birim; sol üst ≈ %55 × %75 levhaya boş; odak sağ %40'ta;
ışık yönü sahne içinde tutarlı; tohum sabit; her Svg öneki "c5-" ile başlar (ünite içinde benzersiz).

Bölgeye özel parçalar (temsilî çizimler):
  teraslar()     Pamukkale travertenleri: beyaz kireç perdeler + turkuaz havuzlar (Karahayıt için kırmızı-turuncu)
  buhar()        sıcak su buharı (radyal gradyanlı yumuşak bulutçuklar; filtre yok)
  afyon_kayasi() Afyonkarahisar Kalesi'nin volkanik kayası: dik yamaçlar, tepede sur, bayrak, isteğe bağlı merdiven
  afyon_evi()    eski Afyon evi: taş zemin kat, beyaz sıvalı cumbalı üst kat, kiremit çatı
Sahneler: pamukkale, karahayit, acigol, omer_gecek, gazligol, afyon_carsi (duraklar) · frig_vadisi (Hülasa) ·
konak (Meclis) · mermer_ocagi (Kıssa) · kale_merdiven (Anahtar) · afyon_kalesi (İmtihan) · afyon_gece (Cevaplar) ·
afyon_final (Final) · panorama_rota (açılış haritası).
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, orta_nokta, halolu_yazi, rng as RNG
from cizim import sahne as S, yapilar as Y
from cizim.karakter import turk_bayragi
from cizim.sahneler import W, H, _bitir, _cerceve_golge

# ------------------------------------------------------------------ nişan ikonları (48×48 çizgi; öğrenci boyar)
NISAN_IKON = {
    "traverten": ('<path d="M5 13 Q13 19 21 13 Q29 19 37 13 Q41 16 44 13"/><path d="M8 24 Q16 30 24 24 Q32 30 40 24"/>'
                  '<path d="M4 35 Q12 41 20 35 Q28 41 36 35 Q40 38 44 35"/><path d="M12 17 v4 M30 17 v4 M17 28 v4 M35 28 v4"/>'),
    "sabun": ('<rect x="6" y="23" width="27" height="17" rx="5"/><path d="M11 23 q5 -6 12 -2"/><circle cx="36" cy="14" r="5.5"/>'
              '<circle cx="25" cy="9" r="3"/><circle cx="42" cy="27" r="3"/><path d="M12 31 h14"/>'),
    "ampul": ('<path d="M24 6 C15 6 10 13 10 19 C10 25 15 28 17 33 H31 C33 28 38 25 38 19 C38 13 33 6 24 6 Z"/>'
              '<path d="M18 37 h12 M19 41 h10 M21 33 v-7 l3 -4 l3 4 v7"/><path d="M4 18 h3 M41 18 h3 M8 6 l2 2 M40 6 l-2 2"/>'),
    "termometre": ('<path d="M19 8 a5 5 0 0 1 10 0 V27 a9 9 0 1 1 -10 0 Z"/><path d="M24 15 V33"/><circle cx="24" cy="35" r="3.4"/>'
                   '<path d="M33 11 h6 M33 17 h4 M33 23 h6"/>'),
    "kabarcik": ('<path d="M20 5 h8 v6 c0 3 6 5 6 12 V40 a3 3 0 0 1 -3 3 H17 a3 3 0 0 1 -3 -3 V23 c0 -7 6 -9 6 -12 Z"/>'
                 '<path d="M14 27 h20"/><circle cx="21" cy="35" r="2"/><circle cx="27" cy="31" r="2.4"/><circle cx="23" cy="20" r="1.6"/>'
                 '<circle cx="40" cy="9" r="2"/><circle cx="8" cy="14" r="1.6"/>'),
    "kristal": ('<path d="M9 19 L23 12 L37 19 L37 34 L23 41 L9 34 Z"/><path d="M9 19 L23 26 L37 19 M23 26 V41"/>'
                '<path d="M41 4 v7 M37.5 7.5 h7 M6 5 v5 M3.5 7.5 h5"/>'),
}

# ------------------------------------------------------------------ renkler (sahne paleti; renkler.py ile uyumlu tonlar)
TRV_TAS, TRV_TAS2, TRV_CIZ = "#FFFFFF", "#D5E7EE", "#9FC2D0"            # beyaz traverten
TRV_SU = ("#D3FAF6", "#45D0D6", "#0E9BB0")                              # turkuaz havuz
KRM_TAS, KRM_TAS2, KRM_CIZ = "#F6C59C", "#C9643A", "#8E3E22"            # Karahayıt kırmızı traverteni
KRM_SU = ("#FFE0B0", "#EC7A3A", "#B5402A")
KAYA, KAYA_G, KAYA_I = "#5B4B52", "#34282F", "#A07E70"                  # Afyon kalesinin volkanik kayası


# ================================================================== PARÇALAR

def teraslar(s, satirlar, tohum, tas=TRV_TAS, tas2=TRV_TAS2, cizgi=TRV_CIZ, su=TRV_SU, parilti="#FFFFFF",
             leke=None, gw=(70, 150)):
    """Traverten basamakları. satirlar: [(y, x_sol, x_sag, olcek), …] arkadan (yukarıdan) öne (aşağıya).
    Her satırda yan yana mercek biçimli havuz: su yüzü + beyaz dudak + aşağı sarkan kireç perdesi (damla izleri).
    leke: [(renk, olasılık)] → perdeye yosun/demir lekesi (Karahayıt)."""
    r = RNG(tohum)
    gs = s.lin([(0, su[0]), (.42, su[1]), (1, su[2])], 0, 0, 0, 1, ad="tsu")
    gt = s.lin([(0, tas), (.55, karis(tas, tas2, .45)), (1, tas2)], 0, 0, 0, 1, ad="tta")
    out = []
    for (y, xl, xr, o) in satirlar:
        x = xl - r.uniform(0, 40) * o
        while x < xr:
            w = r.uniform(*gw) * o
            d = w * r.uniform(.085, .13)
            c = r.uniform(30, 44) * o
            a, b = x, x + w
            m = (a + b) / 2
            yy = y + r.uniform(-3, 3) * o
            perde = (f"M{f(a)} {f(yy)} Q{f(m)} {f(yy + 2 * d)} {f(b)} {f(yy)} L{f(b - w * .03)} {f(yy + c)} "
                     f"Q{f(m)} {f(yy + c + 1.7 * d)} {f(a + w * .03)} {f(yy + c)} Z")
            out.append(f'<path d="{perde}" fill="{gt}"/>')
            if leke:
                for renk, ol in leke:
                    if r.random() < ol:
                        lx = a + w * r.uniform(.15, .7)
                        out.append(f'<path d="M{f(lx)} {f(yy + d)} q{f(w * .08)} {f(c * .5)} {f(w * .02)} {f(c * .9)} '
                                   f'h{f(w * .16)} q{f(-w * .05)} {f(-c * .45)} {f(w * .04)} {f(-c * .9)} Z" fill="{renk}" opacity=".55"/>')
            n = max(2, int(w / 13))
            for k in range(n):
                t = (k + .5) / n
                px = a + w * t + r.uniform(-2.5, 2.5)
                py = yy + 4 * d * t * (1 - t) + 2
                out.append(f'<path d="M{f(px)} {f(py)} v{f(c * r.uniform(.35, .9))}" stroke="{cizgi}" '
                           f'stroke-width="{f(1.1 * o + .5, 2)}" stroke-linecap="round" opacity="{f(r.uniform(.25, .6), 2)}"/>')
            out.append(f'<path d="M{f(a)} {f(yy)} Q{f(m)} {f(yy - d * .9)} {f(b)} {f(yy)} Q{f(m)} {f(yy + 2 * d)} {f(a)} {f(yy)} Z" fill="{gs}"/>')
            out.append(f'<path d="M{f(a + w * .2)} {f(yy - d * .18)} Q{f(m)} {f(yy - d * .52)} {f(b - w * .26)} {f(yy - d * .12)}" '
                       f'stroke="{parilti}" stroke-width="{f(1.5 * o + .6, 2)}" fill="none" opacity=".8" stroke-linecap="round"/>')
            out.append(f'<path d="M{f(a)} {f(yy)} Q{f(m)} {f(yy + 2 * d)} {f(b)} {f(yy)}" stroke="{tas}" '
                       f'stroke-width="{f(3 * o + 1.2, 2)}" fill="none" stroke-linecap="round"/>')
            x += w * r.uniform(.8, .94)
    return "".join(out)


def buhar(s, x, y, w, h, tohum, op=.7, renk="#FFFFFF", n=7, egim=.35):
    """Sıcak su buharı: yükseldikçe genişleyip incelen yumuşak bulutçuklar (radyal gradyan, filtre yok)."""
    r = RNG(tohum)
    g = s.rad([(0, renk, op), (.55, renk, op * .42), (1, renk, 0)], ad="bh")
    out = []
    for k in range(n):
        t = k / max(1, n - 1)
        cx = x + r.uniform(-.18, .18) * w + t * w * egim
        cy = y - t * h
        rx = w * (.22 + .55 * t) * r.uniform(.8, 1.2)
        out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(rx * r.uniform(.55, .75))}" fill="{g}"/>')
    return "".join(out)


def kabarciklar(x, y, w, h, tohum, n=18, renk="#FFFFFF", cizgi="#2A8FA0"):
    r = RNG(tohum)
    out = []
    for _ in range(n):
        px, py = x + r.random() * w, y + r.random() * h
        rr = r.uniform(1.6, 5.2)
        out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(rr)}" fill="{renk}" fill-opacity=".55" stroke="{cizgi}" stroke-width=".9" stroke-opacity=".6"/>')
    return "".join(out)


def bayrak_direk(x, y, boy, G, dalga=3.0, direk="#3A3A44"):
    """Gönder (x, y alt uç) + Türk bayrağı (G: bayrak eni)."""
    return (f'<path d="M{f(x)} {f(y)} V{f(y - boy)}" stroke="{direk}" stroke-width="{f(max(1.6, G * .06))}" stroke-linecap="round"/>'
            f'<circle cx="{f(x)}" cy="{f(y - boy - G * .05)}" r="{f(max(1.6, G * .07))}" fill="#E8C34A"/>'
            + turk_bayragi(x, y - boy, G, dalga))


def afyon_kayasi(s, x0, x1, taban, tepe_y, tohum, renk=KAYA, golge=KAYA_G, isik_renk=KAYA_I, sur="#B39A86",
                 sur_g="#6E5A50", bayrak=True, merdiven=False, isik=-1, gece=False):
    """Afyonkarahisar Kalesi'nin volkanik kayası (temsilî). Dik yamaçlı kütle, sol omuz, tepede surlar ve bayrak.
    Döndürür: (svg, tepe_noktasi)."""
    r = RNG(tohum)
    w, Hh = x1 - x0, taban - tepe_y
    A = (x0, taban)
    B = (x0 + w * .16, taban - Hh * .42)            # sol omuz başı
    C = (x0 + w * .30, taban - Hh * .62)
    D = (x0 + w * .38, tepe_y + Hh * .06)           # zirve sırtı sol
    E = (x0 + w * .55, tepe_y)                      # en yüksek
    F = (x0 + w * .70, tepe_y + Hh * .05)
    G_ = (x0 + w * .80, taban - Hh * .55)
    I = (x1, taban)
    p = []
    for a, b, k in ((A, B, .05), (B, C, .03), (C, D, .04), (D, E, .015), (E, F, .015), (F, G_, .035), (G_, I, .04)):
        seg = orta_nokta(a, b, 4, w * k, r)
        p += seg[:-1]
    p.append(I)
    g = s.lin([(0, isik_renk if isik < 0 else golge), (.45, renk), (1, golge if isik < 0 else isik_renk)], x0, 0, x1, 0,
              kull="userSpaceOnUse", ad="ky")
    out = [f'<path d="{cizgi_d(p, True)}" fill="{g}"/>']
    # gölge yüzü (ışığın karşısı)
    zi = min(range(len(p)), key=lambda i: p[i][1])
    if isik < 0:
        gp = p[zi:] + [(p[zi][0] + w * .1, taban)]
    else:
        gp = p[:zi + 1] + [(p[zi][0] - w * .1, taban)]
    out.append(f'<path d="{cizgi_d(gp, True)}" fill="{golge}" opacity=".55"/>')
    # dikey çatlaklar ve kaya basamakları
    for k in range(14):
        t = r.uniform(.08, .92)
        xa = x0 + w * t
        ust = min((q for q in p if abs(q[0] - xa) < w * .04), key=lambda q: q[1], default=(xa, tepe_y))[1]
        y0_ = ust + Hh * r.uniform(.05, .2)
        hat = orta_nokta((xa, y0_), (xa + r.uniform(-w * .03, w * .03), y0_ + Hh * r.uniform(.15, .45)), 3, w * .01, r)
        out.append(f'<path d="{cizgi_d(hat)}" stroke="{koyu(golge, .2)}" stroke-width="{f(w * .004 + 1)}" fill="none" opacity=".55" stroke-linecap="round"/>')
    for k in range(6):
        yy = tepe_y + Hh * r.uniform(.25, .9)
        xa = x0 + w * r.uniform(.15, .75)
        out.append(f'<path d="M{f(xa)} {f(yy)} q{f(w * .05)} {f(-Hh * .02)} {f(w * .1)} 0" stroke="{isik_renk}" stroke-width="{f(w * .004 + 1)}" fill="none" opacity=".5"/>')
    # surlar: zirve sırtını izleyen bant + mazgallar + iki kule
    sirt = [q for q in p if D[0] - w * .1 <= q[0] <= F[0] + w * .06]
    hs = Hh * .075
    sur_d = cizgi_d(sirt + [(q[0], q[1] - hs) for q in reversed(sirt)], True)
    gs = s.lin([(0, acik(sur, .15)), (1, sur_g)], 0, 0, 0, 1, ad="sr")
    out.append(f'<path d="{sur_d}" fill="{gs}" stroke="{koyu(sur_g, .25)}" stroke-width="{f(w * .003 + .8)}" stroke-linejoin="round"/>')
    mw = max(4.0, w * .016)
    xa = sirt[0][0]
    while xa < sirt[-1][0] - mw:
        yb = min((q for q in sirt if q[0] >= xa), key=lambda q: q[0])[1] - hs
        out.append(f'<rect x="{f(xa)}" y="{f(yb - mw * .9)}" width="{f(mw)}" height="{f(mw * .95)}" fill="{sur}" stroke="{koyu(sur_g, .25)}" stroke-width="{f(w * .002 + .5)}"/>')
        xa += mw * 2
    for qx in (sirt[0], sirt[-1]):
        tw, th = w * .05, Hh * .16
        out.append(f'<rect x="{f(qx[0] - tw / 2)}" y="{f(qx[1] - th)}" width="{f(tw)}" height="{f(th)}" fill="{sur}" stroke="{koyu(sur_g, .25)}" stroke-width="{f(w * .003 + .8)}"/>')
        for j in range(3):
            out.append(f'<rect x="{f(qx[0] - tw / 2 + j * tw * .4)}" y="{f(qx[1] - th - tw * .22)}" width="{f(tw * .2)}" height="{f(tw * .24)}" fill="{sur}" stroke="{koyu(sur_g, .25)}" stroke-width="{f(w * .002 + .5)}"/>')
        if gece:
            out.append(f'<rect x="{f(qx[0] - tw * .12)}" y="{f(qx[1] - th * .7)}" width="{f(tw * .24)}" height="{f(th * .25)}" fill="#FFD27A"/>')
    if gece:
        for q in sirt[::3]:
            out.append(f'<circle cx="{f(q[0])}" cy="{f(q[1] - hs * .5)}" r="{f(w * .006 + 1.2)}" fill="#FFE3A0"/>')
    if merdiven:
        st = [(x0 + w * .08, taban - Hh * .05), (x0 + w * .26, taban - Hh * .2), (x0 + w * .14, taban - Hh * .33),
              (x0 + w * .3, taban - Hh * .47), (x0 + w * .24, taban - Hh * .6), (x0 + w * .37, taban - Hh * .76),
              (D[0] + w * .02, D[1] + Hh * .04)]
        out.append(f'<path d="{cizgi_d(st)}" stroke="#E9DCC6" stroke-width="{f(w * .012 + 2)}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
        out.append(f'<path d="{cizgi_d(st)}" stroke="#8A7462" stroke-width="{f(w * .004 + .8)}" fill="none" stroke-dasharray="{f(w * .006 + 1)} {f(w * .006 + 1)}" stroke-linejoin="round"/>')
    tepe = (E[0], E[1] - hs)
    if bayrak:
        out.append(bayrak_direk(tepe[0], tepe[1] + 2, Hh * .22, Hh * .11, dalga=Hh * .012))
    return "".join(out), tepe


def afyon_evi(x, y, w, h, tohum, isik=-1, gece=False, cati="#B5523A", sivi="#F7F1E6", tas="#CDB79C"):
    """Eski Afyon evi: taş zemin kat, beyaz sıvalı ahşap çatkılı üst kat, çoğu zaman cumba, kiremit çatı."""
    r = RNG(tohum)
    o = []
    z = h * .42
    pen = "#FFD27A" if gece else "#4E6A7A"
    o.append(f'<rect x="{f(x)}" y="{f(y - z)}" width="{f(w)}" height="{f(z)}" fill="{tas}"/>')
    o.append(f'<rect x="{f(x + w * .4)}" y="{f(y - z * .8)}" width="{f(w * .2)}" height="{f(z * .8)}" fill="#6B4A2E"/>')
    ux, uw = x - w * .04, w * 1.08
    o.append(f'<rect x="{f(ux)}" y="{f(y - h)}" width="{f(uw)}" height="{f(h - z)}" fill="{sivi}"/>')
    o.append(f'<path d="M{f(ux)} {f(y - z)} H{f(ux + uw)} M{f(ux)} {f(y - h)} H{f(ux + uw)}" stroke="#7A4E2E" stroke-width="{f(max(1, w * .03))}"/>')
    n = r.randint(2, 3)
    for k in range(n):
        px = ux + uw * (k + .5) / n - w * .07
        o.append(f'<rect x="{f(px)}" y="{f(y - h + (h - z) * .22)}" width="{f(w * .14)}" height="{f((h - z) * .5)}" fill="{pen}" stroke="#7A4E2E" stroke-width="{f(max(.8, w * .02))}"/>')
    if r.random() < .6:
        cx, cw = x + w * r.uniform(.15, .45), w * .42
        o.append(f'<rect x="{f(cx)}" y="{f(y - h - h * .02)}" width="{f(cw)}" height="{f((h - z) * .8)}" fill="{acik(sivi, .3)}" stroke="#7A4E2E" stroke-width="{f(max(.8, w * .025))}"/>')
        o.append(f'<rect x="{f(cx + cw * .15)}" y="{f(y - h + (h - z) * .14)}" width="{f(cw * .7)}" height="{f((h - z) * .38)}" fill="{pen}"/>')
        o.append(f'<path d="M{f(cx)} {f(y - h + (h - z) * .78)} l{f(cw * .1)} {f(h * .06)} h{f(cw * .8)} l{f(cw * .1)} {f(-h * .06)}" fill="#8C5E36"/>')
    gx = ux + uw * .62 if isik < 0 else ux
    o.append(f'<rect x="{f(gx)}" y="{f(y - h)}" width="{f(uw * .38)}" height="{f(h)}" fill="#1B2A55" opacity="{".35" if gece else ".1"}"/>')
    o.append(f'<path d="M{f(ux - w * .1)} {f(y - h)} L{f(ux + uw * .5)} {f(y - h - h * .32)} L{f(ux + uw + w * .1)} {f(y - h)} Z" fill="{cati}"/>')
    o.append(f'<path d="M{f(ux + uw * .5)} {f(y - h - h * .32)} L{f(ux + uw + w * .1)} {f(y - h)} H{f(ux + uw * .5)} Z" fill="#000" opacity=".12"/>')
    return "".join(o)


def kolonlar(s, x, y, n, tohum, boy=70, ara=46, renk="#F4ECDD", golge="#C9B79C"):
    """Hierapolis'in yıkık sütunları (temsilî): kimi kırık, biri yerde yatan tambur."""
    r = RNG(tohum)
    o = []
    for k in range(n):
        h = boy * r.choice([1, 1, .55, .75, .35])
        cx = x + k * ara
        o.append(f'<rect x="{f(cx - 7)}" y="{f(y - h)}" width="14" height="{f(h)}" fill="{renk}"/>')
        o.append(f'<rect x="{f(cx + 1)}" y="{f(y - h)}" width="6" height="{f(h)}" fill="{golge}" opacity=".7"/>')
        if h == boy:
            o.append(f'<rect x="{f(cx - 11)}" y="{f(y - h - 6)}" width="22" height="7" fill="{renk}" stroke="{golge}" stroke-width="1.2"/>')
        else:
            o.append(f'<path d="M{f(cx - 7)} {f(y - h)} l5 -5 l4 4 l5 -6 V{f(y - h)} Z" fill="{renk}"/>')
        o.append(f'<rect x="{f(cx - 10)}" y="{f(y - 5)}" width="20" height="5" fill="{golge}"/>')
    o.append(f'<rect x="{f(x + n * ara - 10)}" y="{f(y - 12)}" width="34" height="12" rx="5" fill="{renk}" stroke="{golge}" stroke-width="1.4"/>')
    return "".join(o)


def _ova(s, y, tohum, ust="#B7CF7A", alt="#5E9442", x0=0, x1=W, h=H):
    g = s.lin([(0, ust), (1, alt)], 0, y, 0, h, kull="userSpaceOnUse", ad="ova")
    r = RNG(tohum)
    pts = [(x0 + (x1 - x0) * i / 12, y + r.uniform(-6, 6)) for i in range(13)]
    return f'<path d="{egri_d(pts)} L{f(x1)} {f(h)} L{f(x0)} {f(h)} Z" fill="{g}"/>'


def _tarlalar(s, x0, x1, y0, y1, tohum, n=26, renkler=("#C9C46A", "#9DBE58", "#D9BC72", "#86B04E", "#B8C878")):
    r = RNG(tohum)
    o = []
    for _ in range(n):
        x = r.uniform(x0, x1)
        y = r.uniform(y0, y1)
        t = (y - y0) / max(1, y1 - y0)
        w = r.uniform(60, 150) * (.5 + t)
        hh = w * .22
        o.append(f'<path d="M{f(x)} {f(y)} l{f(w)} {f(-hh * .15)} l{f(-w * .15)} {f(hh)} l{f(-w)} {f(hh * .15)} Z" fill="{r.choice(renkler)}" opacity=".6"/>')
    return "".join(o)


# ================================================================== 1. DURAK · PAMUKKALE (sabah)

def pamukkale():
    s = Svg("c5-pam")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    s += S.gunes(s, 1920, 118, 40, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=440, guc=.95)
    s += S.bulut(s, 1180, 120, 250, 501, ust="#FFFFFF", alt="#F6C8D0", op=.92)
    s += S.bulut(s, 1560, 70, 170, 502, ust="#FFFFFF", alt="#F9D3C4", op=.85)
    s += S.bulut_serit(s, 260, 205, 460, 10, "#FFE3EA", "#F6B8C8", .55)
    d, _ = S.dag(s, 280, 1500, ufuk, 860, 112, 503, renk="#B6A6D4", golge="#9286BC", bicim="sivri", kar_y=168,
                 kar="#FFFFFF", kar_golge="#D9D2EE", sis="#F4D3DE", isik=-1, sirt=4)
    s += d
    d, _ = S.dag(s, -80, 560, ufuk, 180, 214, 504, renk="#A99BCB", golge="#8E83B8", bicim="tepe", sis="#F2CFE0", isik=-1, sirt=2, puruz=5)
    s += d
    d, _ = S.dag(s, 1650, 2260, ufuk - 10, 2000, 196, 505, renk="#AE9FCC", golge="#9387BC", bicim="tepe", sis="#F6D6DC", isik=-1, sirt=2, puruz=6)
    s += d
    # ova: tarlalar, kavaklar, köy
    s += _ova(s, ufuk, 506, ust="#C6D88A", alt="#6FA24C")
    s += _tarlalar(s, 0, 1150, ufuk + 8, 440, 507)
    for i, x in enumerate((70, 98, 126, 520, 548, 576, 604, 930, 958)):
        s += S.kavak(s, x, ufuk + 60 + (i % 3) * 8, 96 + (i % 4) * 12, 18, 510 + i, renk="#5E9E48")
    for i, x in enumerate((640, 690, 742, 800)):
        s += S.ev(x, ufuk + 72 + (i % 2) * 6, 40, 28, 520 + i, duvar="#F3E2C6", cati="#C2563A")
    # traverten yamacı: yayvan beyaz kütle, sağ yarıda
    yamac = [(1000, H), (1080, 420), (1190, 330), (1300, 250), (1400, 200), (1600, 182), (1850, 176), (2150, 170), (2150, H)]
    gy = s.lin([(0, "#FFFFFF"), (1, "#DDEBF0")], 0, 170, 0, H, kull="userSpaceOnUse", ad="ym")
    s += f'<path d="{egri_d(yamac[:-1])} L2150 {H} Z" fill="{gy}"/>'
    # plato: ağaçlar ve Hierapolis kalıntıları
    for i, x in enumerate((1470, 1500, 1980, 2010, 2040)):
        s += S.kavak(s, x, 186, 70 + (i % 2) * 18, 15, 530 + i, renk="#3F7A44")
    s += kolonlar(s, 1660, 182, 6, 540, boy=62, ara=40)
    s += S.agac(s, 1580, 184, 18, 541, renk="#4F8A4A")
    s += S.agac(s, 1930, 180, 20, 542, renk="#4F8A4A")
    # teraslar (arkadan öne)
    satir = []
    for i in range(10):
        t = i / 9
        y = 200 + 262 * t ** 1.08
        xl = 1390 - 380 * t ** 1.15
        satir.append((y, xl, 2150, .5 + .75 * t))
    s += teraslar(s, satir, 545)
    # öndeki büyük havuz ve yüzen Pamuk
    ax, bx, yy = 1600, 1880, 404
    g = s.lin([(0, "#E4FFFB"), (.4, "#52D6DA"), (1, "#0F9CB2")], 0, yy - 20, 0, yy + 40, kull="userSpaceOnUse", ad="bhv")
    s += f'<path d="M{ax} {yy} Q{(ax + bx) / 2} {yy - 34} {bx} {yy} Q{(ax + bx) / 2} {yy + 62} {ax} {yy} Z" fill="{g}"/>'
    s += f'<path d="M{ax} {yy} Q{(ax + bx) / 2} {yy + 62} {bx} {yy}" stroke="#FFFFFF" stroke-width="6" fill="none" stroke-linecap="round"/>'
    s += f'<use href="#pamuk-yuzer" x="1676" y="352" width="120" height="80"/>'
    s += f'<path d="M1650 398 q20 -8 40 0 M1780 396 q18 -7 36 0" stroke="#FFFFFF" stroke-width="3" fill="none" opacity=".85"/>'
    s += S.marti(1180, 196, .8, 2, renk="#5A4A7A")
    s += S.marti(1236, 214, .6, -1, renk="#5A4A7A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 2. DURAK · KARAHAYIT (öğle, Kırmızı Su)

def karahayit():
    s = Svg("c5-krh")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 1960, 72, 34, hale="#FFF2C2", hale_r=330, guc=.8)
    for i, (x, y, w) in enumerate([(760, 116, 220), (1120, 88, 260), (1520, 132, 190), (380, 176, 150)]):
        s += S.bulut(s, x, y, w, 560 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    d, _ = S.dag(s, 700, 2260, ufuk, 1500, 118, 565, renk="#7E9CBE", golge="#5C7AA4", bicim="tepe", sis="#CFE6F2", isik=-1, sirt=3, puruz=8)
    s += d
    d, _ = S.dag(s, -80, 900, ufuk, 360, 190, 566, renk="#94B2CF", golge="#7699BF", bicim="tepe", sis="#D6ECF5", isik=-1, sirt=2, puruz=5)
    s += d
    s += _ova(s, ufuk, 567, ust="#BFD27E", alt="#6E9E48")
    s += _tarlalar(s, 0, 1100, ufuk + 10, 440, 568, renkler=("#C9C46A", "#9DBE58", "#86B04E", "#B8C878"))
    for i, x in enumerate((90, 118, 146, 640, 668, 1000, 1028)):
        s += S.kavak(s, x, ufuk + 70 + (i % 3) * 6, 100 + (i % 3) * 14, 18, 570 + i, renk="#5A9A46")
    # kırmızı traverten tepeciği (sağ)
    cx, tepe = 1640, 196
    taban_ = [(1180, H), (1300, 380), (1460, 262), (1580, 214), (1700, 214), (1840, 262), (2000, 360), (2120, H)]
    g = s.lin([(0, "#F7D2B0"), (1, "#C86A44")], 0, 196, 0, H, kull="userSpaceOnUse", ad="kt")
    s += f'<path d="{egri_d(taban_)} Z" fill="{g}"/>'
    satir = []
    for i in range(9):
        t = i / 8
        y = 222 + 240 * t
        hw = 70 + 520 * t ** .95
        satir.append((y, cx - hw, cx + hw, .5 + .65 * t))
    s += teraslar(s, satir, 575, tas=KRM_TAS, tas2=KRM_TAS2, cizgi=KRM_CIZ, su=KRM_SU, parilti="#FFF1D8",
                  leke=[("#5E9E5A", .35), ("#F2F0E8", .3), ("#9C3A1E", .3)])
    # tepedeki kaynak borusu: buharlı kırmızı su
    s += f'<rect x="{cx - 9}" y="168" width="18" height="40" rx="3" fill="#7A6A64" stroke="#3A2E2A" stroke-width="2"/>'
    s += f'<path d="M{cx - 4} 170 q-30 -10 -48 30 q-6 16 -2 30" stroke="#E2633A" stroke-width="9" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M{cx + 4} 170 q32 -8 46 32 q4 14 0 28" stroke="#E2633A" stroke-width="9" fill="none" stroke-linecap="round"/>'
    s += buhar(s, cx, 160, 120, 150, 576, op=.75)
    s += buhar(s, cx - 260, 300, 90, 110, 577, op=.5)
    s += buhar(s, cx + 300, 330, 90, 120, 578, op=.5)
    # kaplıca yapısı (sağ uç): düz damlı, kemer pencereli; kubbesiz
    bx, by = 1950, 300
    s += f'<rect x="{bx}" y="{by}" width="170" height="80" fill="#F4ECE0" stroke="#7A5A40" stroke-width="3"/>'
    s += f'<rect x="{bx - 8}" y="{by - 10}" width="186" height="12" fill="#C9A27A" stroke="#7A5A40" stroke-width="2.4"/>'
    for k in range(4):
        x = bx + 16 + k * 40
        s += f'<path d="M{x} {by + 66} V{by + 30} a12 12 0 0 1 24 0 V{by + 66} Z" fill="#6FB8C8" stroke="#7A5A40" stroke-width="2"/>'
    for i, x in enumerate((1190, 1222, 2080)):
        s += S.kavak(s, x, 404 + (i % 2) * 8, 130 + i * 10, 22, 580 + i, renk="#4F8F45")
    s += S.cimen(1100, 2100, 452, 581, renk="#5C9A40", renk2="#86C25A", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += S.marti(1080, 150, .8, 2)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 3. DURAK · ACIGÖL (ikindi, tuzla)

def acigol():
    s = Svg("c5-aci")
    ufuk = 262
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "altin")
    s += S.gunes(s, 1700, 132, 36, hale="#FFE0A0", hale_r=380, guc=.88)
    for i, (x, y, w) in enumerate([(820, 110, 240), (1180, 84, 200), (1900, 150, 160)]):
        s += S.bulut(s, x, y, w, 590 + i, ust="#FFFFFF", alt="#F5D9B5", op=.95)
    uzak = ""
    for i, (a, b, tx, ty, bic) in enumerate(((-80, 760, 300, 170, "tepe"), (560, 1460, 1000, 136, "sivri"), (1300, 2240, 1840, 158, "tepe"))):
        d, _ = S.dag(s, a, b, ufuk, tx, ty, 595 + i, renk=["#B08FA0", "#A68AA8", "#B596A2"][i], golge=["#8A6A86", "#7E6696", "#8C6E88"][i],
                     bicim=bic, sis="#F3C9A8", isik=-1, sirt=3, puruz=6)
        uzak += d
    s += uzak
    # göl: sütlü turkuaz, kıyıda beyaz tuz kabuğu
    s += S.gol(s, 0, ufuk, W, 110, 600, ufuk="#FBE9D0", orta="#9ADBD2", derin="#55B4B0", gunes_x=1700, parilti_renk="#FFF6D8", yogunluk=.8)
    s += S.yansima(s, uzak, ufuk, 0, W, 90, op=.22)
    s += f'<path d="M0 {ufuk + 104} C400 {ufuk + 92} 900 {ufuk + 112} 1400 {ufuk + 98} C1700 {ufuk + 92} 1900 {ufuk + 100} 2100 {ufuk + 94} V{ufuk + 124} H0 Z" fill="#F6F3EA"/>'
    s += f'<path d="M0 {ufuk + 118} C500 {ufuk + 110} 1200 {ufuk + 124} 2100 {ufuk + 112} V{H} H0 Z" fill="#D9C8A8"/>'
    # buharlaştırma havuzları (perspektif)
    r = RNG(601)
    renkler = ["#F4B6C2", "#8FD9D3", "#F2F0EA", "#F7C9A8", "#B5E3DC", "#F2F0EA"]
    satirlar = [(ufuk + 124, 22), (ufuk + 148, 30), (ufuk + 180, 40)]
    for j, (y, hh) in enumerate(satirlar):
        x = -40 + j * 30
        k = 0
        while x < W:
            w = r.uniform(170, 260) * (1 + j * .35)
            c = renkler[(k + j * 2) % len(renkler)]
            s += f'<path d="M{f(x)} {f(y)} H{f(x + w)} l{f(8 + j * 6)} {hh} H{f(x - 8 - j * 6)} Z" fill="{c}" stroke="#B08A5E" stroke-width="{4 + j * 2}" stroke-linejoin="round"/>'
            s += f'<path d="M{f(x + 14)} {f(y + hh * .45)} h{f(w * .4)}" stroke="#FFFFFF" stroke-width="2.4" opacity=".7"/>'
            x += w + 10
            k += 1
    # tuz yığınları + bant + tesis (sağ)
    for i, (x, h_) in enumerate(((1460, 70), (1560, 96), (1680, 82), (1790, 60))):
        g = s.lin([(0, "#FFFFFF"), (1, "#D8DCE4")], x - h_, 0, x + h_, 0, kull="userSpaceOnUse", ad="ty")
        s += f'<path d="M{x - h_ * 1.2} {ufuk + 120} L{x} {ufuk + 120 - h_} L{x + h_ * 1.2} {ufuk + 120} Z" fill="{g}"/>'
        s += f'<path d="M{x} {ufuk + 120 - h_} L{x + h_ * 1.2} {ufuk + 120} H{x + h_ * .1} Z" fill="#B9C2D0" opacity=".55"/>'
    s += f'<path d="M1600 {ufuk + 30} L1820 {ufuk + 112}" stroke="#4A4F5C" stroke-width="10"/><path d="M1600 {ufuk + 30} L1820 {ufuk + 112}" stroke="#9AA3B0" stroke-width="4"/>'
    for k in range(5):
        s += f'<path d="M{1630 + k * 42} {ufuk + 42 + k * 16} v{40 - k * 4}" stroke="#4A4F5C" stroke-width="4"/>'
    s += f'<rect x="1880" y="{ufuk + 30}" width="220" height="90" fill="#C9D0D8" stroke="#4A4F5C" stroke-width="3"/>'
    s += f'<path d="M1870 {ufuk + 34} L1990 {ufuk - 6} L2110 {ufuk + 34} Z" fill="#8F9AA8" stroke="#4A4F5C" stroke-width="3"/>'
    for k in range(4):
        s += f'<rect x="{1898 + k * 50}" y="{ufuk + 58}" width="30" height="22" fill="#5E7A90"/>'
    # yükleyici (sarı)
    lx, ly = 1340, ufuk + 152
    s += f'<rect x="{lx}" y="{ly - 40}" width="90" height="34" rx="6" fill="#F0A21A" stroke="#3A2E14" stroke-width="3"/>'
    s += f'<rect x="{lx + 50}" y="{ly - 66}" width="38" height="28" fill="#F0A21A" stroke="#3A2E14" stroke-width="3"/><rect x="{lx + 56}" y="{ly - 60}" width="24" height="14" fill="#9FD9E6"/>'
    s += f'<path d="M{lx} {ly - 30} l-46 10 l-6 20 h40 Z" fill="#8F9AA8" stroke="#3A2E14" stroke-width="3"/>'
    for cx_ in (lx + 18, lx + 72):
        s += f'<circle cx="{cx_}" cy="{ly - 4}" r="14" fill="#2A2A30"/><circle cx="{cx_}" cy="{ly - 4}" r="5" fill="#9AA3B0"/>'
    for k, (x, y, o) in enumerate([(980, 170, .9), (1040, 196, .7), (1240, 150, .6)]):
        s += S.marti(x, y, o, 2 - k, renk="#4A3A5A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 4. DURAK · ÖMER–GECEK (sabah, jeotermal)

def omer_gecek():
    s = Svg("c5-omr")
    ufuk = 290
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "safak")
    s += S.gunes(s, 1180, 210, 34, cekirdek="#FFF9E8", hale="#FFD9A0", hale_r=360, guc=.9)
    s += S.bulut_serit(s, 1300, 130, 520, 12, "#FFE3EA", "#F6B8C8", .6)
    s += S.bulut_serit(s, 300, 190, 420, 10, "#FFE8E0", "#F4C0C8", .5)
    d, _ = S.dag(s, 600, 2250, ufuk, 1560, 150, 610, renk="#B2A0C8", golge="#8C7EB0", bicim="tepe", sis="#F6D4DA", isik=-1, sirt=3, puruz=7)
    s += d
    d, _ = S.dag(s, -80, 800, ufuk, 300, 196, 611, renk="#A897C2", golge="#8A7CB0", bicim="tepe", sis="#F6D4DA", isik=-1, sirt=2, puruz=5)
    s += d
    s += _ova(s, ufuk, 612, ust="#D9CF8A", alt="#8EA85A")
    s += _tarlalar(s, 0, 1200, ufuk + 8, 440, 613, renkler=("#E0C77A", "#C9C46A", "#B5B860", "#D9B86A"))
    for i, x in enumerate((140, 168, 700, 728, 756)):
        s += S.kavak(s, x, ufuk + 64 + (i % 2) * 8, 104, 18, 615 + i, renk="#5E9A4A")
    # sera ve şehir ısıtma hattı: gümüş borular
    for k, y in enumerate((ufuk + 70, ufuk + 92)):
        s += f'<path d="M1080 {y} H2150" stroke="#5E6672" stroke-width="{16 - k * 3}"/><path d="M1080 {y - 3} H2150" stroke="#D5DBE2" stroke-width="{7 - k}"/>'
        for x in range(1100, 2150, 90):
            s += f'<rect x="{x}" y="{y - 10 + k}" width="8" height="{20 - 2 * k}" fill="#4A4F5C"/>'
    # kuyu başları + vanalar + büyük buhar
    for i, (x, hh) in enumerate(((1380, 120), (1640, 150), (1900, 110))):
        s += f'<rect x="{x - 14}" y="{ufuk + 70 - hh}" width="28" height="{hh}" fill="#8F9AA8" stroke="#3A3E48" stroke-width="3"/>'
        s += f'<rect x="{x - 26}" y="{ufuk + 70 - hh - 16}" width="52" height="18" rx="4" fill="#B8C1CC" stroke="#3A3E48" stroke-width="3"/>'
        s += f'<circle cx="{x + 34}" cy="{ufuk + 70 - hh * .55}" r="15" fill="none" stroke="#E2533D" stroke-width="5"/><path d="M{x + 14} {ufuk + 70 - hh * .55} h20" stroke="#3A3E48" stroke-width="4"/>'
        s += buhar(s, x, ufuk + 50 - hh, 120 + i * 20, 230, 620 + i, op=.85, n=8, egim=.5)
    # termal havuz (ön sağ)
    py = 404
    g = s.lin([(0, "#D8FFFB"), (.5, "#5ED8DA"), (1, "#1592A8")], 0, py - 30, 0, H, kull="userSpaceOnUse", ad="th")
    s += f'<path d="M1240 {py} C1400 {py - 26} 1900 {py - 30} 2150 {py - 18} V{H} H1180 Z" fill="#E9E1D2"/>'
    s += f'<path d="M1300 {py + 8} C1460 {py - 14} 1880 {py - 18} 2150 {py - 6} V{H} H1250 Z" fill="{g}"/>'
    s += buhar(s, 1500, py, 140, 90, 625, op=.55, n=5)
    s += buhar(s, 1860, py - 4, 150, 80, 626, op=.55, n=5)
    s += S.cimen(1100, 1300, 452, 627, renk="#6E8A3A", renk2="#9DB85A", boy=12)
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 5. DURAK · GAZLIGÖL (öğle, maden suyu çeşmesi)

def gazligol():
    s = Svg("c5-gaz")
    ufuk = 286
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 1990, 70, 32, hale="#FFF2C2", hale_r=320, guc=.8)
    for i, (x, y, w) in enumerate([(700, 120, 230), (1080, 90, 270), (1500, 140, 180)]):
        s += S.bulut(s, x, y, w, 630 + i, ust="#FFFFFF", alt="#CFE3F1", op=.95)
    # uzakta tüf tepeleri (Frig Vadisi yönü)
    r = RNG(634)
    for k in range(9):
        x = 560 + k * 170 + r.uniform(-30, 30)
        hh = r.uniform(60, 120)
        s += f'<path d="M{f(x - 50)} {ufuk + 4} C{f(x - 40)} {f(ufuk - hh)} {f(x + 40)} {f(ufuk - hh)} {f(x + 50)} {ufuk + 4} Z" fill="{["#E8C9A8", "#DDB892", "#F0D6B4"][k % 3]}"/>'
        s += f'<path d="M{f(x + 8)} {f(ufuk - hh * .9)} C{f(x + 40)} {f(ufuk - hh)} {f(x + 44)} {f(ufuk - hh * .4)} {f(x + 50)} {ufuk + 4} H{f(x + 18)} Z" fill="#B9906E" opacity=".45"/>'
    s += _ova(s, ufuk, 635, ust="#C9D58A", alt="#76A24E")
    for i, x in enumerate((80, 108, 380, 408, 436)):
        s += S.kavak(s, x, ufuk + 70, 110, 18, 640 + i, renk="#5A9A46")
    # çınar ağacı (arkada)
    for i, (x, r0) in enumerate(((1430, 70), (2040, 84))):
        s += S.agac(s, x, 404, r0, 645 + i, renk="#5E9E48")
    # taş çeşme: kemerli niş, iki lüle, yalak; köpüren maden suyu
    cx, ty, by = 1700, 196, 410
    g = s.lin([(0, "#F1E3CA"), (1, "#C9B08A")], 0, ty, 0, by, kull="userSpaceOnUse", ad="cs")
    s += f'<rect x="{cx - 170}" y="{ty}" width="340" height="{by - ty}" fill="{g}" stroke="#7A5E40" stroke-width="4"/>'
    s += f'<rect x="{cx - 186}" y="{ty - 22}" width="372" height="26" fill="#D9C29C" stroke="#7A5E40" stroke-width="4"/>'
    s += f'<path d="M{cx - 120} {by - 60} V{ty + 110} Q{cx - 120} {ty + 30} {cx} {ty + 26} Q{cx + 120} {ty + 30} {cx + 120} {ty + 110} V{by - 60} Z" fill="#9C7E5A" stroke="#7A5E40" stroke-width="4"/>'
    s += f'<path d="M{cx - 96} {by - 60} V{ty + 112} Q{cx - 96} {ty + 52} {cx} {ty + 48} Q{cx + 96} {ty + 52} {cx + 96} {ty + 112} V{by - 60} Z" fill="#C9E8EC"/>'
    from cizim.temel import selcuklu_yildizi
    s += f'<path d="{cizgi_d(selcuklu_yildizi(cx, ty + 96, 26), True)}" fill="#2B50B5" stroke="#F6E7BF" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{ty + 96}" r="9" fill="#13A3A6"/>'
    for lx in (cx - 46, cx + 46):
        s += f'<rect x="{lx - 7}" y="{ty + 160}" width="14" height="22" fill="#C9A86A" stroke="#5A4020" stroke-width="2.4"/>'
        s += f'<path d="M{lx} {ty + 182} q-2 40 0 82" stroke="#BFF3F6" stroke-width="8" fill="none" stroke-linecap="round"/>'
        s += kabarciklar(lx - 14, ty + 186, 28, 70, 650 + int(lx), n=9)
    s += f'<rect x="{cx - 200}" y="{by - 60}" width="400" height="52" rx="8" fill="#E2CFA8" stroke="#7A5E40" stroke-width="4"/>'
    s += f'<rect x="{cx - 184}" y="{by - 52}" width="368" height="22" rx="6" fill="#7FD9DC"/>'
    s += kabarciklar(cx - 180, by - 54, 360, 22, 652, n=30)
    # yalağın kenarında maden suyu şişeleri (etiketsiz) ve kabarcıklar
    for k, x in enumerate((cx + 214, cx + 252, cx + 290)):
        g2 = s.lin([(0, "#E6FBFF", .95), (1, "#8FD3DE", .9)], 0, 0, 1, 0, ad="sh")
        s += f'<path d="M{x - 12} {by - 4} V{by - 62} q0 -14 8 -20 V{by - 100} h8 V{by - 82} q8 6 8 20 V{by - 4} Z" fill="{g2}" stroke="#2A6A78" stroke-width="2.4"/>'
        s += kabarciklar(x - 9, by - 70, 18, 60, 660 + k, n=8)
    s += f'<rect x="{cx + 190}" y="{by - 4}" width="130" height="10" rx="3" fill="#B8956A" stroke="#7A5E40" stroke-width="2"/>'
    s += f'<use href="#elif-sasiran" x="1860" y="234" width="210" height="221"/>'
    s += S.cimen(1150, 2100, 452, 655, renk="#5C9A40", renk2="#86C25A", boy=12, cicek=["#FFFFFF", "#F0A21A"])
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== 6. DURAK · AFYON ÇARŞISI (altın saat, lokumcu; arkada kale)

def afyon_carsi():
    s = Svg("c5-car")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#4C8FD0"), (.5, "#A8CBE6"), (.82, "#FBDDB0"), (1, "#FFC98A")])
    s += S.gunes(s, 420, 210, 40, hale="#FFC56B", hale_r=420, guc=.85)
    s += S.bulut_serit(s, 900, 120, 520, 14, "#FFE6C4", "#F6B08A", .6)
    kale, _ = afyon_kayasi(s, 1180, 1860, 330, 36, 670, isik=-1)
    s += kale
    # kalenin eteğinde eski Afyon evleri (iki sıra)
    for i in range(12):
        x = 1030 + i * 88
        s += afyon_evi(x, 352 + (i % 2) * 6, 66, 62, 671 + i, cati=["#B5523A", "#A9473A", "#C2643E"][i % 3])
    for i in range(7):
        x = 560 + i * 70
        s += afyon_evi(x, 360, 54, 48, 690 + i)
    # sokak: arnavut kaldırımı
    g = s.lin([(0, "#C9B79C"), (1, "#8F7C64")], 0, 360, 0, H, kull="userSpaceOnUse", ad="yl")
    s += f'<path d="M0 372 C600 362 1400 376 2100 366 V{H} H0 Z" fill="{g}"/>'
    r = RNG(699)
    for k in range(70):
        x, y = r.uniform(0, 2100), r.uniform(380, 458)
        s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(10 + (y - 380) * .12)}" ry="{f(4 + (y - 380) * .05)}" fill="#7E6A54" opacity=".35"/>'
    # lokumcu dükkânı (sağ ön): çizgili tente, vitrinde lokum tepsileri, bakır kazan
    dx = 1700
    s += f'<rect x="{dx}" y="226" width="420" height="160" fill="#F4E6CC" stroke="#6E4422" stroke-width="4"/>'
    s += f'<rect x="{dx - 8}" y="200" width="436" height="32" fill="#7A4E2E" stroke="#4A2E1A" stroke-width="3"/>'
    s += halolu_yazi(f'x="{dx + 210}" y="225" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="27" letter-spacing="3"',
                     "LOKUM · ŞERBET", "#FFF1CF", "#4A2E1A", 1.2)
    for k in range(9):
        x = dx - 10 + k * 49
        c = "#E2533D" if k % 2 == 0 else "#FFFFFF"
        s += f'<path d="M{x} 232 h49 l-6 46 q-18 10 -37 0 Z" fill="{c}" stroke="#8E2A22" stroke-width="2"/>'
    s += f'<rect x="{dx + 24}" y="292" width="230" height="86" fill="#DCEFF2" stroke="#6E4422" stroke-width="4"/>'
    for j, (y, renkler) in enumerate(((318, ("#F7B6C8", "#FFFFFF", "#F7B6C8", "#C8E6A0", "#FFFFFF")), (352, ("#FFFFFF", "#F7B6C8", "#F6D28A", "#FFFFFF", "#F7B6C8")))):
        s += f'<rect x="{dx + 36}" y="{y + 14}" width="206" height="8" rx="3" fill="#C9A86A"/>'
        for k, c in enumerate(renkler):
            x = dx + 44 + k * 40
            s += f'<path d="M{x} {y} l12 -6 l12 6 v14 l-12 6 l-12 -6 Z" fill="{c}" stroke="#B88A9A" stroke-width="1.6"/>'
            s += f'<path d="M{x} {y} l12 6 l12 -6 M{x + 12} {y + 6} v14" stroke="#B88A9A" stroke-width="1.2" fill="none"/>'
    # bakır kazan (ocakta) + buhar
    kx = dx + 330
    s += f'<rect x="{kx - 56}" y="352" width="112" height="34" rx="4" fill="#5A3A22" stroke="#2A1A10" stroke-width="3"/>'
    s += f'<path d="M{kx - 50} 352 q-6 -48 50 -54 q56 6 50 54 Z" fill="#C8743A" stroke="#6E3A18" stroke-width="3"/>'
    s += f'<path d="M{kx - 44} 312 q44 -14 88 0" stroke="#F2B07A" stroke-width="5" fill="none"/>'
    s += f'<ellipse cx="{kx}" cy="302" rx="52" ry="10" fill="#F6E2B8" stroke="#6E3A18" stroke-width="3"/>'
    s += buhar(s, kx, 290, 80, 120, 700, op=.8, n=6, egim=.2)
    s += f'<use href="#pamuk-akce" x="1560" y="304" width="120" height="137"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== HÜLASA · FRİG VADİSİ (alacakaranlık, kamp)

def frig_vadisi(h=400):
    s = Svg("c5-frg")
    ufuk = 300
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "alaca")
    s += S.yildizlar(s, 0, 0, W, 170, 70, 710)
    s += S.ay(s, 1560, 74, 22, golge_renk="#2A2A5E")
    s += S.bulut_serit(s, 300, 230, 520, 12, "#FFB59A", "#C25E83", .55)
    r = RNG(711)
    # arka sıra: alçak tüf tepeleri
    for k in range(10):
        x = 520 + k * 175 + r.uniform(-20, 20)
        hh = r.uniform(70, 130)
        s += f'<path d="M{f(x - 90)} {ufuk + 6} C{f(x - 70)} {f(ufuk - hh)} {f(x + 70)} {f(ufuk - hh * 1.05)} {f(x + 90)} {ufuk + 6} Z" fill="{["#8E5E78", "#9A6A80", "#84587A"][k % 3]}"/>'
    s += _ova(s, ufuk, 712, ust="#7A5A6E", alt="#4A3A54", h=h)
    # ön sıra: peri bacaları (şapkalı konik tüfler), oyma pencereler
    for k, (x, hh, w) in enumerate(((1280, 210, 70), (1400, 260, 84), (1530, 200, 66), (1990, 240, 80), (2090, 190, 60))):
        g = s.lin([(0, "#F2B48A"), (.6, "#D98C6E"), (1, "#9C5E5A")], x - w, 0, x + w, 0, kull="userSpaceOnUse", ad="pb")
        s += f'<path d="M{x - w} {ufuk + 70} C{x - w * .8} {ufuk + 70 - hh * .6} {x - w * .4} {ufuk + 70 - hh} {x} {ufuk + 70 - hh} C{x + w * .4} {ufuk + 70 - hh} {x + w * .8} {ufuk + 70 - hh * .6} {x + w} {ufuk + 70} Z" fill="{g}"/>'
        s += f'<ellipse cx="{x}" cy="{ufuk + 70 - hh}" rx="{w * .45}" ry="{w * .2}" fill="#6E4A52"/>'
        for j in range(2):
            yy = ufuk + 70 - hh * (.35 + .25 * j)
            s += f'<path d="M{x - 10 + j * 14} {yy} v-20 a8 8 0 0 1 16 0 v20 Z" fill="#3A2438"/>'
    # kamp: çadır, ateş, kitap okuyan Pamuk
    s += Y.cadir(s, 1760, 372, 170, 130, renk="#B23A2E", serit="#F5E8D0")
    fx, fy = 1640, 372
    hl = s.rad([(0, "#FFE3A0", .9), (.4, "#FFB45A", .35), (1, "#FF7A3D", 0)], fx, fy - 20, 220, kull="userSpaceOnUse", ad="at")
    s += f'<circle cx="{fx}" cy="{fy - 20}" r="220" fill="{hl}"/>'
    s += f'<path d="M{fx - 34} {fy} l30 -12 l30 12 M{fx - 30} {fy - 12} l60 12" stroke="#5A3A22" stroke-width="7" stroke-linecap="round"/>'
    s += f'<path d="M{fx - 18} {fy - 8} Q{fx - 22} {fy - 44} {fx} {fy - 70} Q{fx + 22} {fy - 44} {fx + 18} {fy - 8} Z" fill="#FF8A3D"/>'
    s += f'<path d="M{fx - 9} {fy - 8} Q{fx - 9} {fy - 30} {fx} {fy - 44} Q{fx + 9} {fy - 30} {fx + 9} {fy - 8} Z" fill="#FFE08A"/>'
    s += f'<use href="#pamuk-kitap" x="1440" y="232" width="140" height="160"/>'
    s += S.cimen(1150, 2100, h - 6, 713, renk="#3E3550", renk2="#5A4A66", boy=12)
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== MECLİS · ESKİ BİR AFYON EVİ (içeri, akşam)

def konak():
    from cizim.sus import kilim_serit
    s = Svg("c5-kon")
    g = s.lin([(0, "#FBF3E4"), (1, "#EEDDC0")], 0, 0, 0, H, kull="userSpaceOnUse", ad="dv")
    s += f'<rect width="{W}" height="{H}" fill="{g}"/>'
    # ahşap tavan ve kirişler
    s += f'<rect width="{W}" height="40" fill="#7A4E2E"/>'
    for x in range(0, W, 70):
        s += f'<rect x="{x}" y="0" width="34" height="40" fill="#8C5A35"/><path d="M{x} 40 h34" stroke="#5E3A20" stroke-width="4"/>'
    s += f'<rect y="40" width="{W}" height="10" fill="#5E3A20"/>'
    # pencere: kale kayası gün batımında
    wx, wy, ww, wh = 1340, 70, 460, 170
    pen = Svg("c5-kon-p")
    pen += S.gokyuzu(pen, wx, wy, ww, wh, "gunbatimi")
    pen += S.gunes(pen, wx + 80, wy + 120, 18, hale="#FFC56B", hale_r=140, guc=.9)
    kk, _ = afyon_kayasi(pen, wx + 150, wx + 430, wy + wh, wy + 24, 721, renk="#4A3A48", golge="#2A1E2C", isik_renk="#B07A70", sur="#C7A080", sur_g="#6E5050")
    pen += kk
    for i in range(6):
        pen += afyon_evi(wx + 10 + i * 76, wy + wh, 52, 40, 722 + i, cati="#9C3A30")
    s.defs += pen.defs
    kl = s.klip(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}"/>', ad="pk")
    s += f'<g clip-path="{kl}">{"".join(pen.parca)}</g>'
    s += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="#6E4422" stroke-width="14"/>'
    s += f'<path d="M{wx + ww / 3} {wy} V{wy + wh} M{wx + 2 * ww / 3} {wy} V{wy + wh} M{wx} {wy + wh * .42} H{wx + ww}" stroke="#6E4422" stroke-width="7"/>'
    s += f'<rect x="{wx - 22}" y="{wy + wh + 2}" width="{ww + 44}" height="12" fill="#8C5A35"/>'
    # duvar dolabı ve nişte gaz lambası
    for x0 in (940, 1960):
        s += f'<rect x="{x0}" y="70" width="110" height="170" fill="#9A6B42" stroke="#5E3A20" stroke-width="4"/>'
        s += f'<path d="M{x0 + 10} 80 h90 v150 h-90 Z M{x0 + 55} 80 V230" stroke="#6E4422" stroke-width="3" fill="none"/>'
    s += f'<path d="M1230 120 v-26 a26 26 0 0 1 52 0 v26 Z" fill="#E8D9BC" stroke="#7A5A40" stroke-width="3"/>'
    lm = s.rad([(0, "#FFF1C4", .9), (1, "#FFD27A", 0)], 1256, 110, 90, kull="userSpaceOnUse", ad="lm")
    s += f'<circle cx="1256" cy="110" r="90" fill="{lm}"/><path d="M1248 120 q8 -26 16 0 Z" fill="#FFB43A"/>'
    # sedir, kilim, minder
    s += f'<rect x="0" y="322" width="{W}" height="62" fill="#8E2A22"/>'
    kil = kilim_serit("c5-kon-k", 2100, 60).replace("<svg ", '<svg width="2100" height="60" ')
    s += f'<g transform="translate(0 324)">{kil}</g>'
    s += f'<rect x="-20" y="248" width="{W + 40}" height="82" rx="26" fill="#1F6E70" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="M-20 262 H{W + 20} M-20 314 H{W + 20}" stroke="#D99A2B" stroke-width="4"/>'
    for x in range(30, W, 72):
        s += f'<path d="M{x} 266 L{x + 22} 288 L{x} 310 L{x - 22} 288 Z" fill="#E2533D" stroke="#F5E8D0" stroke-width="2.4"/>'
    s += f'<path d="M0 384 H{W} V{H} H0 Z" fill="#6E3A22"/>'
    s += f'<path d="M80 394 H{W - 80} L{W} {H} H0 Z" fill="#A9473A"/>'
    # meclistekiler + sini: çay ve lokum
    s += '<use href="#elif-soru" x="1290" y="178" width="260" height="273"/>'
    s += '<use href="#yusuf-anlatan" x="1790" y="178" width="260" height="273"/>'
    s += f'<ellipse cx="1676" cy="440" rx="130" ry="20" fill="#C9A86A" stroke="#7A5A2A" stroke-width="4"/>'
    for x in (1600, 1640, 1712, 1752):
        s += Y.cay_bardak_kucuk(x, 440, 26)
    s += f'<ellipse cx="1676" cy="434" rx="26" ry="8" fill="#FFFFFF" stroke="#7A5A2A" stroke-width="2"/>'
    for k, c in enumerate(("#F7B6C8", "#FFFFFF", "#F7B6C8")):
        s += f'<path d="M{1660 + k * 12} 428 l6 -4 l6 4 v7 l-6 3 l-6 -3 Z" fill="{c}" stroke="#B88A9A" stroke-width="1"/>'
    s += '<use href="#pamuk-dusunen" x="1580" y="236" width="180" height="206"/>'
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== KISSA · İSCEHİSAR MERMER OCAĞI (gün)

def mermer_ocagi():
    s = Svg("c5-mer")
    ufuk = 270
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "gun")
    s += S.gunes(s, 260, 70, 30, hale="#FFF4CC", hale_r=280, guc=.8)
    for i, (x, y, w) in enumerate([(760, 110, 220), (1150, 80, 260), (1600, 120, 200)]):
        s += S.bulut(s, x, y, w, 730 + i, op=.95)
    d, _ = S.dag(s, -60, 1100, ufuk, 500, 170, 734, renk="#9DB2C8", golge="#7C94B2", bicim="tepe", sis="#D6EAF4", isik=-1, sirt=2, puruz=6)
    s += d
    s += _ova(s, ufuk, 735, ust="#CFC98A", alt="#8EA458")
    # ocak tepesi: basamaklı kesilmiş beyaz mermer yüzler (sağ)
    tepe = [(1050, H), (1150, 300), (1300, 196), (1500, 150), (1760, 136), (2000, 150), (2150, 170), (2150, H)]
    gt = s.lin([(0, "#C8B88A"), (1, "#9C8A60")], 0, 130, 0, H, kull="userSpaceOnUse", ad="tp")
    s += f'<path d="{egri_d(tepe[:-1])} L2150 {H} Z" fill="{gt}"/>'
    r = RNG(736)
    for k in range(6):
        y0 = 176 + k * 46
        x0 = 1330 - k * 46
        gm = s.lin([(0, "#FFFFFF"), (1, ["#E8E4DA", "#F1E6EE", "#E4E8EE"][k % 3])], 0, y0, 0, y0 + 46, kull="userSpaceOnUse", ad="mm")
        s += f'<rect x="{x0}" y="{y0}" width="{2150 - x0}" height="46" fill="{gm}" stroke="#A8A08E" stroke-width="2"/>'
        s += f'<rect x="{x0}" y="{y0}" width="{2150 - x0}" height="8" fill="#FFFFFF"/>'
        x = x0 + r.uniform(20, 60)
        while x < 2150:
            s += f'<path d="M{f(x)} {y0 + 8} V{y0 + 46}" stroke="#B8B0A0" stroke-width="2"/>'
            x += r.uniform(60, 120)
        for _ in range(3):
            vx = r.uniform(x0 + 20, 2100)
            s += f'<path d="M{f(vx)} {y0 + 12} q{f(r.uniform(-20, 20))} 14 {f(r.uniform(-10, 30))} 30" stroke="#B7A9C2" stroke-width="1.6" fill="none" opacity=".6"/>'
    # bloklar ve vinç
    for i, (x, y, w, h) in enumerate(((1180, 430, 90, 50), (1290, 440, 120, 60), (1440, 436, 80, 44))):
        s += f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="#F7F5EE" stroke="#8F8878" stroke-width="3"/>'
        s += f'<path d="M{x} {y - h} l14 -10 h{w} l-14 10 Z" fill="#FFFFFF" stroke="#8F8878" stroke-width="2"/>'
        s += f'<path d="M{x + w} {y - h} l14 -10 v{h} l-14 10 Z" fill="#D9D3C4" stroke="#8F8878" stroke-width="2"/>'
    vx = 1880
    s += f'<path d="M{vx} 360 V120 M{vx} 130 L{vx - 220} 150 M{vx} 130 L{vx + 60} 136" stroke="#E0A21A" stroke-width="10" stroke-linecap="round"/>'
    s += f'<path d="M{vx - 200} 150 V250" stroke="#3A3A44" stroke-width="3"/><rect x="{vx - 240}" y="250" width="80" height="44" fill="#F7F5EE" stroke="#8F8878" stroke-width="3"/>'
    s += f'<rect x="{vx - 30}" y="330" width="60" height="40" fill="#E0A21A" stroke="#5A3E10" stroke-width="3"/>'
    s += S.cimen(1000, 1200, 452, 737, renk="#7A8A3A", renk2="#A9B85A", boy=10)
    s += S.marti(1200, 120, .7, 2, renk="#3A3E4A")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== ANAHTAR MERDİVENİ · KALE MERDİVENLERİ (ikindi)

def kale_merdiven():
    s = Svg("c5-mrd")
    ufuk = 330
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, "altin")
    s += S.gunes(s, 560, 150, 36, hale="#FFE0A0", hale_r=360, guc=.85)
    s += S.bulut(s, 900, 110, 220, 740, ust="#FFFFFF", alt="#F5D9B5", op=.9)
    kale, _ = afyon_kayasi(s, 1080, 2140, 470, 20, 741, merdiven=True, isik=-1)
    s += kale
    for i in range(6):
        s += afyon_evi(980 + i * 80, 452, 60, 56, 742 + i)
    s += f'<use href="#pamuk-selam" x="1310" y="250" width="86" height="98"/>'
    for k, (x, y, o) in enumerate([(1500, 90, .9), (1560, 112, .7)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += _cerceve_golge(s)
    return _bitir(s)


# ================================================================== BÜYÜK İMTİHAN · AFYONKARAHİSAR KALESİ (gün batımı, 62 mm)

def afyon_kalesi(h=620):
    s = Svg("c5-kal")
    ufuk = 440
    s += S.gokyuzu(s, 0, 0, W, ufuk + 6, duraklar=[(0, "#2F4FA0"), (.36, "#8A8AC8"), (.66, "#F6A99A"), (1, "#FFC07A")])
    s += S.gunes(s, 300, 360, 56, hale="#FFB45A", hale_r=560, guc=.95)
    for i, (x, y, w) in enumerate([(560, 140, 300), (1000, 90, 340), (1560, 130, 260)]):
        s += S.bulut(s, x, y, w, 750 + i, ust="#FFF4E4", alt="#F0A98A", op=.92)
    s += S.bulut_serit(s, 200, 260, 560, 16, "#FFD8B0", "#F08A7A", .6)
    d, _ = S.dag(s, -80, 900, ufuk, 360, 330, 754, renk="#A58DAE", golge="#87709A", bicim="tepe", sis="#F6C3AA", isik=-1, sirt=2, puruz=5)
    s += d
    d, _ = S.dag(s, 1700, 2260, ufuk, 2080, 340, 755, renk="#A38AAE", golge="#7E6896", bicim="tepe", sis="#F6C3AA", isik=-1, sirt=2, puruz=5)
    s += d
    s += _ova(s, ufuk, 756, ust="#D8B87A", alt="#7E8E48", h=h)
    s += _tarlalar(s, 0, 900, ufuk + 10, h - 30, 757, renkler=("#E0B86A", "#C9A85A", "#B8B060", "#D9A070"))
    kale, _ = afyon_kayasi(s, 940, 1960, ufuk + 60, 150, 758, isik=-1)
    s += kale
    for i in range(14):
        s += afyon_evi(820 + i * 92, ufuk + 110 + (i % 2) * 8, 70, 66, 760 + i, cati=["#B5523A", "#A9473A", "#C2643E"][i % 3])
    for i in range(9):
        s += afyon_evi(160 + i * 76, ufuk + 120, 54, 50, 780 + i)
    for i, x in enumerate((60, 90, 600, 630, 1980, 2010, 2040)):
        s += S.kavak(s, x, ufuk + 140, 150 + (i % 3) * 20, 26, 790 + i, renk="#5E8A3E")
    s += S.cimen(0, 2100, h - 4, 797, renk="#5E7A3A", renk2="#8DA85A", boy=16, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    for k, (x, y, o) in enumerate([(700, 220, 1.1), (780, 252, .8), (1180, 150, .7)]):
        s += S.marti(x, y, o, 2 - k, renk="#3A3355")
    s += _cerceve_golge(s, h)
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== CEVAPLAR · AFYON GECESİ (30 mm)

def afyon_gece(h=300):
    s = Svg("c5-gec")
    ufuk = 236
    s += S.gokyuzu(s, 0, 0, W, h, "gece")
    s += S.yildizlar(s, 0, 0, W, ufuk - 40, 150, 800)
    s += S.ay(s, 1180, 70, 28, golge_renk="#13204A")
    kale, _ = afyon_kayasi(s, 1420, 2080, ufuk + 30, 28, 801, renk="#2E2E50", golge="#1A1A36", isik_renk="#4A4A78", sur="#4E4E7E",
                           sur_g="#2A2A4E", gece=True)
    s += kale
    g = s.lin([(0, "#1E2A55"), (1, "#0E1636")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="sz")
    s += f'<rect x="0" y="{ufuk}" width="{W}" height="{h - ufuk}" fill="{g}"/>'
    for i in range(22):
        s += afyon_evi(-20 + i * 98, ufuk + 40 + (i % 3) * 8, 70, 60, 802 + i, gece=True, cati="#3A2E4E", sivi="#4A4A6E", tas="#3A3A5A")
    r = RNG(830)
    for _ in range(60):
        x = r.uniform(0, W)
        s += f'<circle cx="{f(x)}" cy="{f(ufuk + r.uniform(60, 64))}" r="{f(r.uniform(1.6, 3))}" fill="#FFD27A" opacity="{f(r.uniform(.6, 1), 2)}"/>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


# ================================================================== FİNAL · KALE BURCUNDA PAMUK (90 mm)

def afyon_final(nisanlar=None, h=900):
    s = Svg("c5-fin")
    ufuk = 560
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gunbatimi")
    gx, gy = 760, ufuk - 30
    for k in range(14):
        a0 = math.pi + k * math.pi / 14
        a1 = a0 + math.pi / 34
        s += (f'<path d="M{gx} {gy} L{f(gx + 1800 * math.cos(a0))} {f(gy + 1800 * math.sin(a0))} '
              f'L{f(gx + 1800 * math.cos(a1))} {f(gy + 1800 * math.sin(a1))} Z" fill="#FFE0A0" opacity=".12"/>')
    s += S.gunes(s, gx, gy, 70, hale="#FFC56B", hale_r=700, guc=.95)
    for (x, y, w, k) in ((200, 260, 520, 22), (1200, 180, 640, 26), (1500, 330, 480, 16), (100, 420, 380, 12)):
        s += S.bulut_serit(s, x, y, w, k, "#FFC59A", "#FF6F8A", .75)
    d, _ = S.dag(s, 980, 1900, ufuk, 1400, 340, 841, renk="#C88AA6", golge="#7E5A92", bicim="tepe", sis="#FF9A8A", isik=-1, sirt=3, puruz=8)
    s += d
    d, _ = S.dag(s, -100, 760, ufuk, 300, 420, 842, renk="#6B4C86", golge="#4E3A6E", bicim="tepe", sis="#E07A8A", isik=-1, sirt=2, puruz=6)
    s += d
    # Afyon ovası ve şehir (kale burcundan bakış)
    s += _ova(s, ufuk, 843, ust="#C98A7A", alt="#6E5A6E", h=h)
    s += _tarlalar(s, 0, W, ufuk + 6, 700, 844, n=40, renkler=("#D99A7A", "#B98A80", "#C9A07A", "#A98A8E"))
    for i in range(26):
        s += afyon_evi(-30 + i * 84, 700 + (i % 3) * 6, 58, 52, 845 + i, cati="#9C3A40", sivi="#F2D8CC", tas="#B9958E")
    # kale burcu (ön plan)
    g = s.lin([(0, "#8A6A6E"), (1, "#4E3A44")], 0, 640, 0, h, kull="userSpaceOnUse", ad="bs")
    s += f'<rect x="0" y="720" width="{W}" height="{h - 720}" fill="{g}"/>'
    r = RNG(875)
    for row in range(6):
        y = 724 + row * 30
        off = 0 if row % 2 == 0 else 45
        for x in range(-45 + off, W, 90):
            s += f'<rect x="{x + 2}" y="{y}" width="86" height="27" rx="3" fill="{karis("#9C7C78", "#5E4650", r.uniform(0, .6))}" stroke="#3E2C34" stroke-width="1.6"/>'
    for x in range(0, W, 150):
        s += f'<rect x="{x}" y="660" width="96" height="64" fill="#8E6E70" stroke="#3E2C34" stroke-width="2.6"/>'
        s += f'<rect x="{x}" y="660" width="96" height="10" fill="#B08A86"/>'
    s += f'<rect x="1560" y="560" width="420" height="{h - 560}" fill="url(#{s.onek}-tk)" stroke="#3E2C34" stroke-width="3"/>'
    s.tanim(f'<linearGradient id="{s.onek}-tk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B08A86"/>'
            f'<stop offset=".6" stop-color="#8A6A6E"/><stop offset="1" stop-color="#5E4650"/></linearGradient>')
    for x in range(1560, 1980, 84):
        s += f'<rect x="{x}" y="510" width="54" height="56" fill="#9C7C78" stroke="#3E2C34" stroke-width="2.6"/>'
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


# ================================================================== AÇILIŞ · PAMUKKALE–AFYON TUR HARİTASI (110 mm)

# stilize harita konumları (birim; mm = /10). Gerçek yönler korunur (batı solda, kuzey yukarıda), mesafeler
# okunurluk için sıkıştırılıp açılmıştır: Pamukkale ile Karahayıt arası yaklaşık 5 km, Afyon kümesi ise ≈ 25 km'lik bir alandadır.
HARITA = {"1": (330, 905), "2": (520, 735), "3": (960, 850), "4": (1330, 650), "5": (1530, 480), "6": (1625, 820), "K": (1835, 700)}
ROTA_ARA = {("1", "2"): [(420, 830)], ("2", "3"): [(700, 760), (840, 830)], ("3", "4"): [(1110, 820), (1240, 730)],
            ("4", "5"): [(1420, 560)], ("5", "6"): [(1640, 560), (1690, 700)], ("6", "K"): [(1730, 800)]}


def panorama_rota(h=1100):
    """Açılış sayfası haritası: Denizli–Afyon arası stilize arazi; Pamukkale travertenleri, Karahayıt, Acıgöl,
    Ömer–Gecek buharı, Gazlıgöl çeşmesi, Frig tüfleri, Afyon kalesi; kıvrılan rota ve rozetler.
    Döndürür: (svg, konum) — konum: {"1": (x, y), …, "K": (x, y)} (birim)."""
    from cizim.temel import selcuklu_yildizi, yildiz_noktalari
    s = Svg("c5-har")
    ufuk = 330
    s += S.gokyuzu(s, 0, 0, W, ufuk + 8, "gunbatimi")
    s += S.gunes(s, 300, ufuk - 40, 50, hale="#FFC56B", hale_r=620, guc=.9)
    for (x, y, w_, kk) in ((620, 140, 520, 18), (1260, 96, 620, 22), (1720, 210, 400, 14), (120, 220, 340, 12)):
        s += S.bulut_serit(s, x, y, w_, kk, "#FFC9A0", "#FF7A8A", .75)
    for i, (sol, sag, tx, ty, bic, renk, golge) in enumerate((
            (-120, 820, 330, 190, "sivri", "#B08AB0", "#7A5C8E"), (560, 1500, 1040, 150, "tepe", "#C08FB0", "#8A6A9E"),
            (1300, 2240, 1800, 186, "tepe", "#A9789E", "#7B5A8C"))):
        d_, _ = S.dag(s, sol, sag, ufuk + 8, tx, ty, 900 + i, renk=renk, golge=golge, bicim=bic, kar_y=240 if i == 0 else None,
                      kar="#FFE6EE", kar_golge="#C6A7D2", sis="#FFA18E", isik=-1, sirt=3, puruz=7)
        s += d_
    gk = s.lin([(0, "#C9A27E"), (.14, "#C8B074"), (.5, "#A7B864"), (1, "#6E9E48")], 0, ufuk, 0, h, kull="userSpaceOnUse", ad="kr")
    s += f'<rect x="0" y="{ufuk + 6}" width="{W}" height="{h - ufuk}" fill="{gk}"/>'
    r = RNG(905)
    for _ in range(80):
        x, y = r.uniform(-60, 2100), r.uniform(ufuk + 30, h - 20)
        t = (y - ufuk) / (h - ufuk)
        w_ = r.uniform(70, 170) * (.45 + t)
        hh = w_ * .3 * (.4 + t)
        c = r.choice(["#B9B65E", "#8FB24E", "#D3B86A", "#7AA84A", "#C9A04E", "#A8C46A"])
        s += f'<path d="M{f(x)} {f(y)} l{f(w_)} {f(-hh * .2)} l{f(-w_ * .2)} {f(hh)} l{f(-w_)} {f(hh * .2)} Z" fill="{c}" opacity=".5"/>'
    # Pamukkale: beyaz traverten yamacı + turkuaz havuzlar (1. durak çevresi)
    s += f'<path d="M120 {h} C150 980 210 930 300 880 C380 850 480 860 560 900 C600 930 620 990 640 {h} Z" fill="#F4FBFD"/>'
    s += teraslar(s, [(905 + 40 * i, 200 - 25 * i, 600 + 10 * i, .55 + .12 * i) for i in range(5)], 906, gw=(60, 110))
    # Karahayıt: kırmızı tepecik + buhar
    s += f'<path d="M430 790 Q520 690 610 790 Z" fill="#E08A5A"/>'
    s += teraslar(s, [(745, 485, 560, .35), (770, 460, 585, .42)], 907, tas=KRM_TAS, tas2=KRM_TAS2, cizgi=KRM_CIZ, su=KRM_SU, gw=(40, 70))
    s += buhar(s, 520, 690, 50, 90, 908, op=.7, n=5)
    # Acıgöl: beyaz tuz kabuklu göl
    s += f'<ellipse cx="960" cy="860" rx="230" ry="62" fill="#F6F3EA"/>'
    s += f'<ellipse cx="960" cy="858" rx="206" ry="50" fill="#A8E0D8"/>'
    s += f'<ellipse cx="930" cy="852" rx="120" ry="22" fill="#D2F2EC" opacity=".8"/>'
    for k in range(5):
        s += f'<rect x="{1120 + k * 30}" y="{886 + (k % 2) * 8}" width="26" height="14" fill="{["#F4B6C2", "#F2F0EA", "#8FD9D3"][k % 3]}" stroke="#B08A5E" stroke-width="2"/>'
    # Ömer–Gecek: buhar sütunları + borular
    s += f'<path d="M1250 690 H1420" stroke="#5E6672" stroke-width="8"/><path d="M1250 688 H1420" stroke="#D5DBE2" stroke-width="3"/>'
    for x in (1290, 1380):
        s += f'<rect x="{x - 6}" y="660" width="12" height="30" fill="#8F9AA8" stroke="#3A3E48" stroke-width="2"/>'
        s += buhar(s, x, 650, 50, 110, 910 + x, op=.8, n=6, egim=.4)
    # Gazlıgöl: çeşme + kabarcıklar; Frig tüfleri (kuzeydoğu)
    s += f'<rect x="1480" y="430" width="60" height="44" fill="#E9D8B8" stroke="#7A5E40" stroke-width="3"/>'
    s += f'<path d="M1494 474 V450 a16 16 0 0 1 32 0 V474 Z" fill="#7FD9DC"/>'
    s += kabarciklar(1470, 476, 80, 20, 912, n=10)
    for k, (x, hh) in enumerate(((1700, 70), (1745, 96), (1795, 66), (1850, 84))):
        s += f'<path d="M{x - 24} 470 C{x - 20} {470 - hh} {x + 20} {470 - hh} {x + 24} 470 Z" fill="#E8B48E"/><ellipse cx="{x}" cy="{470 - hh * .86}" rx="12" ry="5" fill="#9C6A5A"/>'
    # İscehisar: beyaz mermer basamakları (doğu)
    for k in range(3):
        s += f'<rect x="{1960 + k * 14}" y="{590 + k * 16}" width="{110 - k * 14}" height="16" fill="#F7F5EE" stroke="#A8A08E" stroke-width="2"/>'
    # Afyon: kale kayası + şehir
    kale, _ = afyon_kayasi(s, 1770, 1910, 720, 600, 913, isik=-1)
    s += kale
    for i in range(10):
        s += afyon_evi(1560 + i * 44 + (i % 2) * 6, 790 + (i % 3) * 18, 32, 28, 914 + i)
    for _ in range(40):
        x, y = r.uniform(80, 2050), r.uniform(ufuk + 40, h - 30)
        if any(math.hypot(x - a, y - b) < 130 for a, b in HARITA.values()) or 100 < x < 660 and y > 860 or 700 < x < 1220 and 780 < y < 940:
            continue
        sc = .45 + (y - ufuk) / (h - ufuk)
        for j in range(3):
            s += S.kavak(s, x + j * 18 * sc, y, 58 * sc, 11 * sc, 920 + _ * 3 + j, renk="#5E9A4A")
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
    s += (halolu_yazi(f'x="960" y="972" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="40"', "Acıgöl", "#FFFFFF", "#0A5A66", 1.4)
          + halolu_yazi(f'x="300" y="1062" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="40"', "Pamukkale", "#FFFFFF", "#0A5A66", 1.4)
          + halolu_yazi(f'x="1960" y="790" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="40"', "Afyon", "#FFFFFF", "#5A2A1A", 1.4))
    s += f'<text x="1040" y="1010" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" letter-spacing="1.5" fill="#FFFFFF" opacity=".95">TUZLU GÖL · SODYUM SÜLFAT</text>'
    for k, (x, y, o) in enumerate(((1000, 200, 1.1), (1066, 232, .8), (1500, 150, .7), (820, 290, .6))):
        s += S.marti(x, y, o, 3 - k, renk="#3A2550")
    px, py = 1980, 980
    s += f'<circle cx="{px}" cy="{py}" r="74" fill="#FFFFFF" opacity=".9" stroke="#1B1D26" stroke-width="3"/>'
    s += f'<path d="{cizgi_d(yildiz_noktalari(px, py, 66, 14, 4, -math.pi / 2), True)}" fill="#1D3A8A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<path d="{cizgi_d(selcuklu_yildizi(px, py, 34), True)}" fill="#13A3A6" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<circle cx="{px}" cy="{py}" r="10" fill="#F0A21A" stroke="#1B1D26" stroke-width="2"/>'
    s += f'<text x="{px}" y="{py - 76}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">K</text>'
    return s.cikti(f"0 0 {W} {h}", cls="sahne panorama", par="xMidYMid slice"), dict(HARITA)
