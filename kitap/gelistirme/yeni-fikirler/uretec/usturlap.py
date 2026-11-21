"""Usturlap Çarkı · iki kâğıt disk, çatal çiviyle birleşir (usturlap süslemeli volvel).

Diskler
  P (büyük, R 75,5 mm, "anakap")  ön yüz: 20 elementin verisi + kenar halkası (Z · simge · ad)
                                   arka yüz: dış logaritmik ölçek (m ve n) + kullanım ve çözümlü örnek
                                   halka yarık r 48–55 mm (3 ince köprü): arkadan Q'nun M ölçeği görünür
  Q (küçük, R 58 mm + kürsü)       ön yüz: kürsü penceresi (Z, simge, ad) + pencere A (dizilim, iyon) + pencere B (periyot, grup)
                                   arka yüz: iç logaritmik ölçek (M) + kırmızı ok (n)
Kullanım: kürsüden tut (Q sabit), büyük diski (P) çevir. Ön yüzde seçili element, arka yüzde sonuç (n) hep tepededir.

Açılar: "tepeden saat yönünde" derece, o yüze bakan kişiye göre. Arka yüz ön yüzün aynasıdır: x → −x (uzun kenardan çevirme).
Ölçek: θ(x) = 360° · log10(x), x ∈ [1, 10). İki ölçek de arkadan bakana göre saat yönünde artar.
"""
import math
import os
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KITAP = os.path.abspath(os.path.join(BURA, "..", "..", ".."))
for _y in (os.path.join(KITAP, "yerel-ortak", "cizim"), os.path.join(KITAP, "yerel-cerceve", "uretec"), BURA):
    if _y not in sys.path:
        sys.path.insert(0, _y)
from temel import f, selcuklu_yildizi, cizgi_d  # noqa: E402
import elementler as EL  # noqa: E402
import olcu  # noqa: E402

PT = 0.3528
# ------------------------------------------------------------------ ölçüler (mm)
R_P, R_Q = 75.5, 58.0
LIMB = (61.6, 74.0)            # P kenar halkası içerik bandı (kürsü penceresi bunun içinde)
KURSU_P = (61.6, 74.2, 8.6)    # kürsü penceresi: r1, r2, ± yarım açı (kiriş kenarlı)
BANT_A = (32.0, 46.0, 8.0)     # pencere A (doğu): dizilim + iyon
BANT_B = (15.0, 29.5, 8.0)     # pencere B (batı): periyot + grup
KART_YARI = 8.8                # P'deki kartların yarım açısı (komşu kart 18° ötede)
YARIK = (48.0, 55.0)           # P'deki halka yarık
KOPRU_MANTIS = (1.3, 2.6, 6.6) # köprülerin arka yüz ölçeğindeki yeri (m)
KOPRU_EN = 2.0                 # mm
ADIM = 18.0                    # element başına açı
# sayfa yerleşimi (s1 ön; s2 arka = ayna, uzun kenardan çevirme)
P_ON, Q_ON, Q_DONUS = (85.5, 89.5), (142.0, 223.0), 35.0
P_ARKA, Q_ARKA = (210 - P_ON[0], P_ON[1]), (210 - Q_ON[0], Q_ON[1])

# ------------------------------------------------------------------ renkler (Van tokenları; tema eşlemesi karma palete çevirir)
OBS, OBS2, SOLUK, KAR, KIREC, CIZGI = "#1B1D26", "#343947", "#56636E", "#FBFDFD", "#FFFDF7", "#CFDCE0"
GOL, GOLK, GOLA, GOLAA, DERIN = "#13A3A6", "#0A6C74", "#DCF3F1", "#EEF9F8", "#0E4C5A"
KEH, KEHK, KEHA = "#F0A21A", "#8C5500", "#FFF0CF"
MER, MERK, MERA = "#E2533D", "#A12817", "#FDE7E1"
KOB, KOBK, KOBA = "#2B50B5", "#1B3584", "#E6ECFB"
ALTIN, ALTINK, ALTINA, LAJ = "#C9952B", "#8A6212", "#F6E7BF", "#1D3A8A"
ERG, ZUM, GUM, GUMK, GUMA = "#7B3F8C", "#1F8A5B", "#A3B3BE", "#586874", "#EDF2F5"
BALOO, NUN = "'Baloo Bhaijaan 2'", "Nunito"
SINIF_RENK = {"metal": (KEHA, KEHK), "ametal": (GOLA, GOLK), "yari": (KOBA, KOBK), "soy": (MERA, MERK)}
SINIF_AD = {"metal": "metal", "ametal": "ametal", "yari": "yarı metal", "soy": "soy gaz"}

# ------------------------------------------------------------------ veri (yerel-cerceve/uretec/elementler.py ile aynı kaynak)
# Yaygın iyon kuralı (klasik 9/06–9/07 üniteleriyle aynı): 1, 2 ve 13. grup metalleri e⁻ verir (+);
# 15–17. grup ametalleri e⁻ alır (−); H hem H⁺ hem H⁻ (hidrür); soy gazlar iyon oluşturmaz.
# Seçilen kural (C, Si ve B): iyon yazılmaz, ortak bağ sayısı yazılır (C ve Si 4, B 3). C⁴⁻ (karbür) yalnız birkaç bileşikte görülür.
IYON = {"H": [("H", "+"), ("H", "−")], "He": "yok", "Li": [("Li", "+")], "Be": [("Be", "2+")], "B": "bag3", "C": "bag4",
        "N": [("N", "3−")], "O": [("O", "2−")], "F": [("F", "−")], "Ne": "yok", "Na": [("Na", "+")], "Mg": [("Mg", "2+")],
        "Al": [("Al", "3+")], "Si": "bag4", "P": [("P", "3−")], "S": [("S", "2−")], "Cl": [("Cl", "−")], "Ar": "yok",
        "K": [("K", "+")], "Ca": [("Ca", "2+")]}


def katmanlar(z):
    """Z ≤ 20 için katman dizilimi (2, 8, 8, 2 kuralı)."""
    k, kalan = [], z
    for kap in (2, 8, 8, 2):
        k.append(min(kap, kalan))
        kalan -= k[-1]
        if not kalan:
            break
    assert kalan == 0
    return k


def veri():
    out = []
    for e in EL.ELEMENTLER[:20]:
        z = e["z"]
        p, g = EL.yer(z)
        out.append({"z": z, "sembol": e["sembol"], "ad": e["ad"], "periyot": p, "grup": g, "dizilim": katmanlar(z),
                    "sinif": EL.sinif(e["sembol"]), "iyon": IYON[e["sembol"]]})
    return out


def iyon_metin(iyon):
    """Düz metin (denetim ve önizleme için)."""
    if iyon == "yok":
        return "yok"
    if isinstance(iyon, str):
        return iyon[-1] + " bağ"
    return " · ".join(b + y for b, y in iyon)


# ------------------------------------------------------------------ geometri yardımcıları
def kut(r, a):
    """tepeden saat yönünde a derece, r yarıçap → (x, y) (SVG, y aşağı)."""
    t = math.radians(a)
    return (r * math.sin(t), -r * math.cos(t))


def p2(p):
    return f"{f(p[0], 2)} {f(p[1], 2)}"


def dilim_d(r1, r2, a1, a2, kiris=False):
    """Halka dilimi (a1 → a2 saat yönünde). kiris=True: iç/dış kenar düz (maketle kesmek kolay)."""
    if kiris:
        return f"M{p2(kut(r2, a1))} L{p2(kut(r2, a2))} L{p2(kut(r1, a2))} L{p2(kut(r1, a1))} Z"
    buyuk = 1 if (a2 - a1) % 360 > 180 else 0
    return (f"M{p2(kut(r2, a1))} A{f(r2, 2)} {f(r2, 2)} 0 {buyuk} 1 {p2(kut(r2, a2))} L{p2(kut(r1, a2))} "
            f"A{f(r1, 2)} {f(r1, 2)} 0 {buyuk} 0 {p2(kut(r1, a1))} Z")


def daire(r, renk="none", cizgi=None, en=0.3, ek=""):
    c = f' stroke="{cizgi}" stroke-width="{f(en, 2)}"' if cizgi else ""
    return f'<circle r="{f(r, 2)}" fill="{renk}"{c}{ek}/>'


def yazi(x, y, metin, pt, w=800, aile=NUN, renk=OBS, hiza="middle", ek=""):
    return (f'<text x="{f(x, 2)}" y="{f(y, 2)}" font-family="{aile}" font-weight="{w}" font-size="{f(pt * PT, 3)}" '
            f'fill="{renk}" text-anchor="{hiza}"{ek}>{metin}</text>')


def ust_tspan(ust, pt, yuk=None):
    """üst simge: küçük punto, yukarı kaydırılmış; ardından taban çizgisine dönülür."""
    dy = yuk if yuk is not None else pt * PT * .42
    return f'<tspan dy="{f(-dy, 2)}" font-size="{f(pt * PT * .62, 3)}">{ust}</tspan><tspan dy="{f(dy, 2)}"> </tspan>'


def iyon_svg(iyon, pt):
    if iyon == "yok":
        return "yok"
    if isinstance(iyon, str):
        return f"{iyon[-1]} bağ"
    parca = []
    for i, (b, y) in enumerate(iyon):
        parca.append(("  ·  " if i else "") + b + ust_tspan(y, pt))
    return "".join(parca).rstrip()


def yay_yolu(kimlik, r, a_orta, alt=False, aci=150):
    """Yazı yolu: üst yayda soldan sağa (saat yönü), alt yayda soldan sağa (saat yönünün tersi)."""
    if not alt:
        a1, a2 = a_orta - aci / 2, a_orta + aci / 2
        return f'<path id="{kimlik}" d="M{p2(kut(r, a1))} A{f(r)} {f(r)} 0 0 1 {p2(kut(r, a2))}" fill="none"/>'
    a1, a2 = a_orta + aci / 2, a_orta - aci / 2
    return f'<path id="{kimlik}" d="M{p2(kut(r, a1))} A{f(r)} {f(r)} 0 0 0 {p2(kut(r, a2))}" fill="none"/>'


def yay_yazi(kimlik, metin, pt, w=800, aile=NUN, renk=OBS, harf=0):
    ls = f' letter-spacing="{f(harf, 2)}"' if harf else ""
    return (f'<text font-family="{aile}" font-weight="{w}" font-size="{f(pt * PT, 3)}" fill="{renk}"{ls}>'
            f'<textPath href="#{kimlik}" startOffset="50%" text-anchor="middle">{metin}</textPath></text>')


def theta(x):
    """logaritmik ölçek açısı (derece), x mantis [1, 10)."""
    return 360.0 * math.log10(x)


def kopru_acilari_arka():
    return [theta(m) for m in KOPRU_MANTIS]


def kopru_acilari_on():
    return [(-a) % 360 for a in kopru_acilari_arka()]


def yarik_dilimleri(on=True):
    """yarığın köprüler arası parçaları: [(a1, a2)] saat yönünde (o yüzün açılarıyla)."""
    kop = sorted(kopru_acilari_on() if on else kopru_acilari_arka())
    yari = math.degrees(KOPRU_EN / 2 / ((YARIK[0] + YARIK[1]) / 2))
    out = []
    for i, a in enumerate(kop):
        b = kop[(i + 1) % len(kop)] + (360 if i == len(kop) - 1 else 0)
        out.append((a + yari, b - yari))
    return out


# ------------------------------------------------------------------ Q'nun dış çizgisi (daire + kürsü)
def kursu_noktalari():
    """sağ yarı (tepe çerçevesinde), tabandan tepeye; sol yarı ayna."""
    return [(16.0, -55.75), (14.6, -62.0), (16.9, -66.2), (16.4, -70.6), (13.6, -75.4), (9.0, -78.2), (4.6, -78.6),
            (3.0, -80.6), (0.0, -82.2)]


def q_dis_d():
    sag = kursu_noktalari()
    a1 = math.degrees(math.atan2(16.0, 55.75))
    yol = f"M{p2(kut(R_Q, a1))} A{f(R_Q)} {f(R_Q)} 0 1 1 {p2(kut(R_Q, 360 - a1))} "
    sol_yukari = [(-x, y) for x, y in sag[:-1]]           # sol taban → tepe
    sag_asagi = list(reversed(sag[:-1]))                   # tepe → sağ taban
    nok = sol_yukari[1:] + [sag[-1]] + sag_asagi
    return yol + "L" + " L".join(p2(p) for p in nok) + " Z"


def q_dis_noktalar(n=240):
    """simülasyon maskesi için çokgen (yerel, tepe çerçevesi)."""
    sag = kursu_noktalari()
    a1 = math.degrees(math.atan2(16.0, 55.75))
    pts = [kut(R_Q, a1 + (360 - 2 * a1) * i / n) for i in range(n + 1)]
    pts += [(-x, y) for x, y in sag[1:]] + list(reversed(sag[1:-1]))
    return pts


def pencereler():
    """Q ön yüzündeki delikler (yerel, kiriş kenarlı dörtgenler): ad → (r1, r2, a_orta, yarım açı)."""
    return {"kursu": (KURSU_P[0], KURSU_P[1], 0.0, KURSU_P[2]), "A": (BANT_A[0], BANT_A[1], 90.0, BANT_A[2]),
            "B": (BANT_B[0], BANT_B[1], 270.0, BANT_B[2])}


def pencere_kose(r1, r2, a, y):
    return [kut(r2, a - y), kut(r2, a + y), kut(r1, a + y), kut(r1, a - y)]


# ------------------------------------------------------------------ süs parçaları
def hancer(r1, r2, a, en=3.4, renk=ALTIN):
    """usturlap ankebutundaki yıldız göstergesi (alev biçimli hançer) + uçta küçük daire."""
    p = []
    for t in range(0, 11):
        s = t / 10
        r = r1 + (r2 - r1) * s
        w = en * math.sin(math.pi * min(1, s * 1.25)) * (1 - s) ** .35
        p.append((r, w))
    sag = [kut(r, a) for r, _ in p]
    d = []
    for (r, w), (x, y) in zip(p, sag):
        nx, ny = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.append((x + nx * w / 2 * (1 + .35 * math.sin(r)), y + ny * w / 2))
    sol = []
    for (r, w), (x, y) in zip(p, sag):
        nx, ny = math.cos(math.radians(a)), math.sin(math.radians(a))
        sol.append((x - nx * w / 2, y - ny * w / 2))
    yol = "M" + " L".join(p2(q) for q in d + sol[::-1]) + " Z"
    uc = kut(r2 + 1.3, a)
    return (f'<path d="{yol}" fill="{renk}" stroke="{OBS}" stroke-width=".32" stroke-linejoin="round"/>'
            f'<circle cx="{f(uc[0], 2)}" cy="{f(uc[1], 2)}" r="1.05" fill="{KAR}" stroke="{OBS}" stroke-width=".3"/>'
            f'<circle cx="{f(uc[0], 2)}" cy="{f(uc[1], 2)}" r=".38" fill="{MER}"/>')


def merkez_isareti(r=1.6):
    return (f'<circle r="{r}" fill="#fff" stroke="{OBS}" stroke-width=".25"/>'
            f'<path d="M-3.2 0 H3.2 M0 -3.2 V3.2" stroke="{OBS}" stroke-width=".22"/>')


def makas(x, y, aci=0, k=1.0):
    return (f'<g transform="translate({f(x, 2)} {f(y, 2)}) rotate({f(aci, 1)}) scale({f(k, 2)})">'
            f'<circle cx="-2.4" cy="-1.2" r="1" fill="none" stroke="{OBS}" stroke-width=".35"/>'
            f'<circle cx="-2.4" cy="1.2" r="1" fill="none" stroke="{OBS}" stroke-width=".35"/>'
            f'<path d="M-1.5 -.8 L3.2 1.1 M-1.5 .8 L3.2 -1.1" stroke="{OBS}" stroke-width=".42" stroke-linecap="round"/></g>')


def tarama_d(r1, r2, a1, a2, adim=1.6):
    """kesilecek alanı belli eden ince çapraz çizgiler (yarık için)."""
    d = []
    n = int((a2 - a1) * math.pi / 180 * r2 / adim)
    for i in range(n + 1):
        a = a1 + (a2 - a1) * i / max(n, 1)
        d.append(f"M{p2(kut(r1 + .4, a))} L{p2(kut(r2 - .4, a + 1.4))}")
    return " ".join(d)


# ------------------------------------------------------------------ P ÖN YÜZ
def _limb_icerik(e):
    """tepe çerçevesinde (kürsü penceresi) Z · simge · ad."""
    zem, koyu = SINIF_RENK[e["sinif"]]
    o = [f'<path d="{dilim_d(LIMB[0], LIMB[1], -KART_YARI - .2, KART_YARI + .2)}" fill="{zem}"/>',
         yazi(0, -71.0, str(e["z"]), 7.5, 900, renk=koyu, ek=' data-alan="z"'),
         yazi(0, -65.5, e["sembol"], 15.5, 800, BALOO, OBS, ek=' data-alan="sembol"'),
         yazi(0, -62.35, e["ad"], 6.8, 800, renk=OBS2, ek=' data-alan="ad"')]
    return "".join(o)


def _kart_A(e):
    """doğu penceresi: dizilim (üst satır) + iyon (alt satır)."""
    zem, koyu = SINIF_RENK[e["sinif"]]
    r1, r2, _ = BANT_A
    xm = (r1 + r2) / 2
    diz = "·".join(str(k) for k in e["dizilim"])
    o = [f'<path d="{dilim_d(r1 - .8, r2 + .8, 90 - KART_YARI, 90 + KART_YARI)}" fill="{zem}"/>',
         f'<path d="M{f(r1 + 1.2)} .75 H{f(r2 - 1.2)}" stroke="{koyu}" stroke-width=".18" stroke-dasharray=".6 .5" opacity=".7"/>',
         yazi(xm, -0.95, diz, 9.4, 900, renk=OBS, ek=' data-alan="dizilim"'),
         yazi(xm, 3.75, iyon_svg(e["iyon"], 8.6), 8.6, 900, renk=koyu, ek=' data-alan="iyon"')]
    return "".join(o)


def _kart_B(e):
    """batı penceresi: periyot (dışta, solda) · grup (içte, sağda)."""
    zem, koyu = SINIF_RENK[e["sinif"]]
    r1, r2, _ = BANT_B
    o = [f'<path d="{dilim_d(r1 - .8, r2 + .8, 270 - KART_YARI, 270 + KART_YARI)}" fill="{zem}"/>',
         f'<path d="M{f(-22.2)} -2.3 V2.3" stroke="{koyu}" stroke-width=".2" opacity=".7"/>',
         yazi(-25.6, 1.15, str(e["periyot"]), 9.4, 900, renk=OBS, ek=' data-alan="periyot"'),
         yazi(-18.5, 1.15, str(e["grup"]), 9.4, 900, renk=koyu, ek=' data-alan="grup"')]
    return "".join(o)


def on_P():
    o = [daire(R_P, KIREC)]
    # kenar halkası zemini ve dış derece bölmeleri (usturlap kenarı)
    o.append(f'<path d="{dilim_d(58.2, 75.5, 0, 359.99)}" fill="{GUMA}"/>')
    d = []
    for i in range(200):
        a = i * 1.8
        uz = 1.3 if i % 10 == 0 else (.9 if i % 5 == 0 else .55)
        d.append(f"M{p2(kut(74.25, a))} L{p2(kut(74.25 + uz, a))}")
    o.append(f'<path d="{" ".join(d)}" stroke="{OBS2}" stroke-width=".16"/>')
    o.append(daire(74.2, cizgi=OBS2, en=.22) + daire(61.45, cizgi=OBS2, en=.22) + daire(58.3, cizgi=ALTIN, en=.5))
    # iç süs halkası (Q'nun hemen dışında görünür): eşkenar dörtgenler
    sus = []
    for i in range(20):
        a = i * ADIM + ADIM / 2
        x, y = kut(59.85, a)
        sus.append(f'<path d="M{f(x, 2)} {f(y - .9, 2)} l.9 .9 l-.9 .9 l-.9 -.9 Z" transform="rotate({f(a, 1)} {f(x, 2)} {f(y, 2)})" fill="{ALTIN}"/>')
    o.append("".join(sus))
    # bant zeminleri
    o.append(f'<path d="{dilim_d(BANT_A[0] - 1.3, BANT_A[1] + 1.3, 0, 359.99)}" fill="{GUMA}"/>')
    o.append(f'<path d="{dilim_d(BANT_B[0] - 1.3, BANT_B[1] + 1.3, 0, 359.99)}" fill="{GUMA}"/>')
    o.append(daire(BANT_A[0] - 1.35, cizgi=ALTIN, en=.35) + daire(BANT_A[1] + 1.35, cizgi=ALTIN, en=.35)
             + daire(BANT_B[0] - 1.35, cizgi=ALTIN, en=.35) + daire(BANT_B[1] + 1.35, cizgi=ALTIN, en=.35))
    # merkezde Selçuklu yıldızı (Q'nun altında kalır)
    o.append(f'<path d="{cizgi_d(selcuklu_yildizi(0, 0, 11.5), True, 2)}" fill="{ALTINA}" stroke="{ALTIN}" stroke-width=".3"/>')
    # elementler: her şey "tepe" çerçevesinde çizilir, ψ_k kadar döndürülür
    for e in veri():
        psi = ADIM * (e["z"] - 1)
        o.append(f'<g transform="rotate({f(psi, 2)})" data-z="{e["z"]}" data-psi="{f(psi, 2)}">'
                 f'{_limb_icerik(e)}{_kart_A(e)}{_kart_B(e)}</g>')
    # sektör sınırları (kenar halkası)
    d = []
    for i in range(20):
        a = i * ADIM + ADIM / 2
        d.append(f"M{p2(kut(LIMB[0] - .15, a))} L{p2(kut(LIMB[1] + .2, a))}")
    o.append(f'<path d="{" ".join(d)}" stroke="{OBS2}" stroke-width=".25"/>')
    # yarık (kesilecek) ve köprüler
    for a1, a2 in yarik_dilimleri(True):
        o.append(f'<path d="{dilim_d(YARIK[0], YARIK[1], a1, a2)}" fill="{GUMA}" stroke="{OBS}" stroke-width=".3"/>'
                 f'<path d="{tarama_d(YARIK[0], YARIK[1], a1, a2)}" stroke="{GUM}" stroke-width=".18"/>')
    for a in kopru_acilari_on():
        x, y = kut((YARIK[0] + YARIK[1]) / 2, a)
        o.append(f'<g transform="translate({f(x, 2)} {f(y, 2)}) rotate({f(a + 90, 1)})">{yazi(0, .6, "köprü", 3.4, 900, renk=MERK)}</g>')
    o.append(f'<path id="usp-yt" d="M{p2(kut(51.5, 300))} A51.5 51.5 0 0 1 {p2(kut(51.5, 60))}" fill="none"/>')
    o.append(yay_yazi("usp-yt", "HALKA YARIĞI MAKETLE KES · KÖPRÜLERİ KESME", 4.6, 900, renk=MERK))
    o.append(merkez_isareti())
    return "".join(o)


# ------------------------------------------------------------------ Q ÖN YÜZ
def _pencere_cerceve(r1, r2, a, y, kalin=1.0):
    k = pencere_kose(r1, r2, a, y)
    d = "M" + " L".join(p2(p) for p in k) + " Z"
    return (f'<path d="{d}" fill="none" stroke="{OBS}" stroke-width="{f(kalin * 2 + .7, 2)}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{ALTIN}" stroke-width="{f(kalin * 2, 2)}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{GUMA}" stroke="{OBS}" stroke-width=".35" stroke-linejoin="round"/>'
            f'<path d="M{p2(k[0])} L{p2(k[2])} M{p2(k[1])} L{p2(k[3])}" stroke="{GUM}" stroke-width=".25"/>')


def on_Q():
    o = [f'<defs><radialGradient id="usq-g" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{KAR}"/><stop offset=".82" stop-color="{KIREC}"/>'
         f'<stop offset="1" stop-color="{ALTINA}"/></radialGradient></defs>',
         f'<path d="{q_dis_d()}" fill="url(#usq-g)"/>']
    # pirinç kenar: koyu halka + noktalar
    o.append(f'<path d="{dilim_d(54.0, 58.0, 0, 359.99)}" fill="{ALTINA}"/>')
    o.append(daire(57.6, cizgi=OBS, en=.35) + daire(54.0, cizgi=ALTIN, en=.5))
    o.append("".join(f'<circle cx="{f(kut(55.8, i * 6)[0], 2)}" cy="{f(kut(55.8, i * 6)[1], 2)}" r=".55" fill="{ALTIN}" stroke="{ALTINK}" stroke-width=".15"/>'
                     for i in range(60) if 18 < i * 6 < 342))
    # kürsü süsü: iç kontur + küçük halka
    sag = kursu_noktalari()
    ic = [(x * .86, y * .985) for x, y in sag[1:]]
    ic_d = "M" + " L".join(p2(p) for p in [(-x, y) for x, y in reversed(ic)] + ic)
    o.append(f'<path d="{ic_d}" fill="none" stroke="{ALTIN}" stroke-width=".45"/>')
    o.append(f'<circle cx="0" cy="-79.6" r="1.25" fill="{MER}" stroke="{OBS}" stroke-width=".3"/>')
    # ankebut kemerleri (pencerelerin, notun ve lejantın dışından geçer)
    for a1, a2 in ((102, 150), (210, 258), (282, 438)):
        for r, en in ((33.6, .55), (34.9, .25)):
            o.append(f'<path d="M{p2(kut(r, a1))} A{r} {r} 0 {1 if a2 - a1 > 180 else 0} 1 {p2(kut(r, a2))}" fill="none" stroke="{ALTIN}" stroke-width="{en}"/>')
    # yıldız göstergeleri (hançer): 4 büyük + 4 küçük
    for a in (45, 135, 225, 315):
        o.append(hancer(36.0, 52.0, a))
    for a in (67, 113, 247, 293):
        o.append(hancer(40.5, 51.2, a, en=2.4, renk=KEH))
    # merkez rozeti (çatal çivinin bacakları dikeyde üstünden geçer)
    o.append(f'<path d="{cizgi_d(selcuklu_yildizi(0, 0, 9.0), True, 2)}" fill="{ALTINA}" stroke="{ALTIN}" stroke-width=".35"/>')
    o.append(f'<circle cx="0" cy="7.5" r="11.8" fill="none" stroke="{ALTIN}" stroke-width=".4" stroke-dasharray="1.2 .7"/>')
    # pencereler
    for ad, (r1, r2, a, y) in pencereler().items():
        o.append(_pencere_cerceve(r1, r2, a, y, .55 if ad == "kursu" else .5))
    # kürsü penceresinin altında okuma okları
    for s in (-1, 1):
        x = s * 10.6
        o.append(f'<path d="M{f(x - .9)} -59.2 L{f(x + .9)} -59.2 L{f(x)} -60.9 Z" fill="{MER}"/>')
    # etiketler
    o.append(yazi(30.3, -0.95, "dizilim", 6.4, 900, renk=GUMK, hiza="end"))
    o.append(yazi(30.3, 3.75, "yaygın iyon", 6.4, 900, renk=GUMK, hiza="end"))
    o.append(yazi(-25.6, -5.0, "periyot", 5.6, 900, renk=GUMK))
    o.append(yazi(-18.5, -4.25, "grup", 5.6, 900, renk=GUMK))
    o.append(yazi(0, -53.0, "Z · simge · ad", 5.4, 900, renk=GUMK))
    # başlık (alt yay)
    o.append(yay_yolu("usq-b1", 49.8, 180, alt=True, aci=110))
    o.append(yay_yazi("usq-b1", "USTURLAP ÇARKI", 10.5, 800, BALOO, LAJ, harf=.35))
    o.append(yay_yolu("usq-b2", 45.6, 180, alt=True, aci=110))
    o.append(yay_yazi("usq-b2", "9. sınıf · elementi tepeye getir, pencereden oku", 5.6, 800, renk=OBS2))
    # sınıf renkleri (lejant)
    for i, (sk, (zem, koyu)) in enumerate(SINIF_RENK.items()):
        x = -21.5 if i % 2 == 0 else 6.5
        y = 27.6 + (i // 2) * 5.0
        o.append(f'<rect x="{f(x)}" y="{f(y - 2.9)}" width="3.6" height="3.6" rx=".7" fill="{zem}" stroke="{koyu}" stroke-width=".35"/>'
                 + yazi(x + 4.6, y, SINIF_AD[sk], 5.8, 900, renk=koyu, hiza="start"))
    # kural notu (üstte; çatal çivinin bacakları dikeyde merkezden ±22 mm, burası daha yukarıda)
    ust = [("İyon: metal e" + ust_tspan("−", 5.4) + "verir (+), ametal e" + ust_tspan("−", 5.4) + "alır (−).", -45.0),
           ("Soy gaz iyon oluşturmaz.", -40.6),
           ("B, C, Si iyon yerine ortak bağ kurar.", -36.2)]
    for metin, y in ust:
        o.append(yazi(0, y, metin, 5.4, 800, renk=OBS2))
    o.append(f'<path d="M-3.4 -24 V-31 M3.4 -24 V-31" stroke="{CIZGI}" stroke-width=".25" stroke-dasharray=".8 .6"/>')
    o.append(merkez_isareti())
    return "".join(o)


# ------------------------------------------------------------------ ARKA YÜZLER (mol çarkı)
def olcek_tikleri():
    """(değer, tür) listesi: tür ∈ tam, yarim, onda, yirmide."""
    out = []
    for i in range(100, 1000):
        x = i / 100
        if i % 100 == 0:
            out.append((x, "tam"))
        elif i % 50 == 0:
            out.append((x, "yarim"))
        elif i % 10 == 0 and (x < 5 or True):
            out.append((x, "onda"))
        elif i % 5 == 0 and x < 2:
            out.append((x, "yirmide"))
    return out


def _sayi_tr(x):
    s = f"{x:g}".replace(".", ",")
    return s


ARKA_P_TIK = {"tam": 4.6, "yarim": 3.4, "onda": 2.3, "yirmide": 1.5}
ARKA_Q_TIK = {"tam": 3.2, "yarim": 2.4, "onda": 1.8, "yirmide": 1.3}
GOSTERGE = [("CH₄", 16), ("H₂O", 18), ("O₂", 32), ("CO₂", 44), ("NaCl", 58.5), ("soda", 106)]


def arka_P():
    o = [daire(R_P, KIREC)]
    # dış süs halkası
    o.append(f'<path d="{dilim_d(70.6, 75.5, 0, 359.99)}" fill="{GOLAA}"/>')
    o.append(daire(70.6, cizgi=ALTIN, en=.45) + daire(73.6, cizgi=OBS2, en=.2))
    o.append("".join(f'<circle cx="{f(kut(72.1, i * 6 + 3)[0], 2)}" cy="{f(kut(72.1, i * 6 + 3)[1], 2)}" r=".42" fill="{ALTIN}"/>' for i in range(60)))
    # m · n ölçeği (dış), yarığın dış kenarından (55) 1 mm sonra başlar
    r0 = YARIK[1] + 1.0
    d = {k: [] for k in ARKA_P_TIK}
    for x, tur in olcek_tikleri():
        a = theta(x)
        d[tur].append(f'<line data-olcek="m" data-deger="{x:g}" x1="{f(kut(r0, a)[0], 3)}" y1="{f(kut(r0, a)[1], 3)}" '
                      f'x2="{f(kut(r0 + ARKA_P_TIK[tur], a)[0], 3)}" y2="{f(kut(r0 + ARKA_P_TIK[tur], a)[1], 3)}"/>')
    for tur, en in (("tam", .42), ("yarim", .3), ("onda", .22), ("yirmide", .16)):
        o.append(f'<g stroke="{OBS}" stroke-width="{en}" stroke-linecap="butt">{"".join(d[tur])}</g>')
    o.append(daire(r0, cizgi=OBS, en=.2))
    for k in range(1, 10):
        a = theta(k)
        o.append(f'<g transform="rotate({f(a, 3)})">{yazi(0, -(r0 + 6.05), str(k), 10.5, 800, BALOO, OBS, ek=f" data-etiket=\"m{k}\"")}</g>')
    for x in (1.5, 2.5, 3.5, 4.5):
        a = theta(x)
        o.append(f'<g transform="rotate({f(a, 3)})">{yazi(0, -(r0 + 4.1), _sayi_tr(x), 6.0, 900, renk=OBS2)}</g>')
    for x in (1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 1.8, 1.9):
        a = theta(x)
        o.append(f'<g transform="rotate({f(a, 3)})">{yazi(0, -(r0 + 3.0), _sayi_tr(x), 5.0, 900, renk=GUMK)}</g>')
    o.append(yay_yolu("uap-d", 68.4, 180, alt=True, aci=60))
    o.append(yay_yazi("uap-d", "dış ölçek: m (g) ve sonuç n (mol)", 5.2, 900, renk=GOLK))
    # orta: başlık, formül, adımlar, örnek
    o.append(yay_yolu("uap-b", 42.6, 0, aci=120))
    o.append(yay_yazi("uap-b", "MOL ÇARKI · 10. sınıf", 10.0, 800, BALOO, LAJ, harf=.3))
    o.append(yazi(0, -28.6, "n = m / M", 15.0, 800, BALOO, MERK))
    adim = ["1. Dış ölçekte kütleyi (m) bul.", "2. Yarıktaki M’yi m’nin hizasına çevir.",
            "3. Kırmızı ok n’yi gösterir (hep tepede).", "4. Virgülü kaba hesapla koy."]
    for i, s in enumerate(adim):
        o.append(yazi(-31.5, -20.4 + i * 4.15, s, 6.4, 800, renk=OBS, hiza="start"))
    o.append(f'<rect x="-34" y="8.6" width="68" height="26.8" rx="2.4" fill="{MERA}" stroke="{MER}" stroke-width=".35"/>')
    orn = [("ÖRNEK · göl sodası", 6.6, 900, MERK), ("53 g Na₂CO₃ kaç mol? (M = 106 g/mol)", 6.3, 800, OBS),
           ("Dışta 5,3’ü bul; içte 1,06’yı hizasına getir.", 6.0, 700, OBS), ("Ok 5,0’ı gösterir. Kaba hesap: 53/106 ≈ 0,5", 6.0, 700, OBS)]
    for i, (s, pt, w, r) in enumerate(orn):
        o.append(yazi(0, 13.3 + i * 4.2, s, pt, w, renk=r))
    o.append(yazi(0, 32.6, "n = 0,5 mol", 9.0, 800, BALOO, MERK))
    o.append(yazi(0, 39.6, "Deneme: 1’i 1’e, sonra 5’i 5’e getir;", 5.4, 800, renk=GUMK))
    o.append(yazi(0, 42.9, "ok iki kez de 1’i göstermeli.", 5.4, 800, renk=GUMK))
    # çatal çivi başı
    o.append(daire(5.2, ALTINA, ALTIN, .35) + merkez_isareti(1.4))
    return "".join(o)


def arka_Q():
    o = [f'<path d="{q_dis_d()}" transform="scale(-1 1)" fill="{GUMA}" stroke="{CIZGI}" stroke-width=".3"/>',
         daire(R_Q - .3, KAR)]
    # yarıktan görünen halka zemini
    o.append(f'<path d="{dilim_d(YARIK[0] - .8, YARIK[1] + .9, 0, 359.99)}" fill="{ALTINA}"/>')
    r0 = YARIK[1] + .8          # tik tepesi (P'nin yarık kenarının 0,8 mm altında)
    d = {k: [] for k in ARKA_Q_TIK}
    for x, tur in olcek_tikleri():
        a = theta(x)
        if x == 1.0:
            continue
        d[tur].append(f'<line data-olcek="M" data-deger="{x:g}" x1="{f(kut(r0, a)[0], 3)}" y1="{f(kut(r0, a)[1], 3)}" '
                      f'x2="{f(kut(r0 - ARKA_Q_TIK[tur] - .8, a)[0], 3)}" y2="{f(kut(r0 - ARKA_Q_TIK[tur] - .8, a)[1], 3)}"/>')
    for tur, en in (("tam", .4), ("yarim", .3), ("onda", .22), ("yirmide", .16)):
        o.append(f'<g stroke="{OBS}" stroke-width="{en}">{"".join(d[tur])}</g>')
    for k in range(2, 10):
        a = theta(k)
        o.append(f'<g transform="rotate({f(a, 3)})">{yazi(0, -(r0 - 6.15), str(k), 7.6, 800, BALOO, OBS)}</g>')
    for x in (1.5, 2.5):
        a = theta(x)
        o.append(f'<g transform="rotate({f(a, 3)})">{yazi(0, -(r0 - 5.2), _sayi_tr(x), 5.2, 900, renk=OBS2)}</g>')
    # madde göstergeleri
    for ad, M in GOSTERGE:
        x = M / 10 ** math.floor(math.log10(M))
        a = theta(x)
        o.append(f'<line data-gosterge="{ad}" data-deger="{x:g}" x1="{f(kut(r0, a)[0], 3)}" y1="{f(kut(r0, a)[1], 3)}" '
                 f'x2="{f(kut(r0 - 4.4, a)[0], 3)}" y2="{f(kut(r0 - 4.4, a)[1], 3)}" stroke="{KEH}" stroke-width=".5"/>')
        o.append(f'<g transform="rotate({f(a, 3)})">{yazi(0, -(YARIK[0] + .75), ad, 4.4, 900, renk=KEHK)}</g>')
    # kırmızı ok (M = 1, n'yi gösterir)
    o.append(f'<line data-olcek="M" data-deger="1" data-ok="1" x1="0" y1="{f(-r0, 2)}" x2="0" y2="{f(-(YARIK[0] + .3), 2)}" stroke="{MER}" stroke-width=".7"/>'
             f'<path d="M-1.15 {f(-(r0 - 1.9), 2)} L1.15 {f(-(r0 - 1.9), 2)} L0 {f(-r0 - .1, 2)} Z" fill="{MER}"/>')
    o.append(yazi(1.7, -(r0 - 6.15), "1", 7.6, 800, BALOO, OBS, hiza="start"))
    o.append(yazi(-1.5, -(r0 - 5.0), "n", 6.4, 900, renk=MERK, hiza="end"))
    # kürsünün arka yüzü: P'nin dışında kalan tepe, okun uzantısı
    o.append(f'<path d="M0 {f(-R_P - .4, 2)} V-81 M-1.2 {f(-R_P - .6, 2)} L1.2 {f(-R_P - .6, 2)} L0 {f(-R_P + 1.2, 2)} Z" stroke="{MER}" stroke-width=".55" fill="{MER}"/>')
    # görünmeyen iç bölge: kısa not
    for i, s in enumerate(["Bu yüz büyük diskin arkasında kalır.", "M ölçeği halka yarıktan görünür."]):
        o.append(yazi(0, 36 + i * 3.6, s, 5.2, 800, renk=GUMK))
    o.append(merkez_isareti(1.4))
    return "".join(o)


# ------------------------------------------------------------------ SAYFALAR
def _q_on_kesme():
    """Q ön yüz kesme çizgileri (yerel): dış çizgi + 3 pencere."""
    o = [f'<path d="{q_dis_d()}" fill="none" stroke="{OBS2}" stroke-width=".26"/>']
    return "".join(o)


def _p_on_kesme():
    return f'<circle r="{R_P}" fill="none" stroke="{OBS2}" stroke-width=".26"/>'


def sayfa_on():
    """s1: P ve Q ön yüzleri, kesme çizgileri (kesikli), makas işaretleri. Tam sayfa SVG (mm)."""
    px, py = P_ON
    qx, qy = Q_ON
    return (f'<svg class="usturlap-svg" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">'
            f'<g transform="translate({px} {py})" data-yuz="P-on">{on_P()}{_p_on_kesme()}</g>'
            f'<g transform="translate({qx} {qy}) rotate({Q_DONUS})" data-yuz="Q-on">{on_Q()}{_q_on_kesme()}</g>'
            f'{makas(px - 52, py + 55.5, 225)}{makas(qx - 41, qy + 41, 225)}'
            f'{yazi(px - 58.5, py + 63.5, "P · büyük disk", 6.5, 900, renk=OBS2, hiza="start")}'
            f'{yazi(qx + 28, qy + 60.4, "Q · küçük disk", 6.5, 900, renk=OBS2, hiza="start")}'
            f'</svg>')


def sayfa_arka():
    px, py = P_ARKA
    qx, qy = Q_ARKA
    return (f'<svg class="usturlap-svg" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">'
            f'<g transform="translate({px} {py})" data-yuz="P-arka">{arka_P()}</g>'
            f'<g transform="translate({qx} {qy}) rotate({-Q_DONUS})" data-yuz="Q-arka">{arka_Q()}</g>'
            f'</svg>')


# ------------------------------------------------------------------ simülasyon için sayfa geometrisi
def _yerlestir(pts, merkez, donus=0.0, ayna=False):
    c, s = math.cos(math.radians(donus)), math.sin(math.radians(donus))
    out = []
    for x, y in pts:
        if ayna:
            x = -x
        out.append((merkez[0] + x * c - y * s, merkez[1] + x * s + y * c))
    return out


def _dilim_nokta(r1, r2, a1, a2, n=60):
    dis = [kut(r2, a1 + (a2 - a1) * i / n) for i in range(n + 1)]
    ic = [kut(r1, a2 - (a2 - a1) * i / n) for i in range(n + 1)]
    return dis + ic


def maske_geometrisi():
    """sayfa mm koordinatlarında: her yüz için dış çizgi ve delik çokgenleri (s1 ön, s2 arka)."""
    on = {"P": {"merkez": P_ON, "dis": _yerlestir([kut(R_P, i * 1.5) for i in range(240)], P_ON),
                "delik": [_yerlestir(_dilim_nokta(YARIK[0], YARIK[1], a1, a2), P_ON) for a1, a2 in yarik_dilimleri(True)]},
          "Q": {"merkez": Q_ON, "donus": Q_DONUS, "dis": _yerlestir(q_dis_noktalar(), Q_ON, Q_DONUS),
                "delik": [_yerlestir(pencere_kose(*v), Q_ON, Q_DONUS) for v in pencereler().values()]}}
    arka = {"P": {"merkez": P_ARKA, "dis": _yerlestir([kut(R_P, i * 1.5) for i in range(240)], P_ARKA),
                  "delik": [_yerlestir(_dilim_nokta(YARIK[0], YARIK[1], a1, a2), P_ARKA) for a1, a2 in yarik_dilimleri(False)]},
            "Q": {"merkez": Q_ARKA, "donus": -Q_DONUS, "dis": _yerlestir(q_dis_noktalar(), Q_ARKA, -Q_DONUS, ayna=True),
                  "delik": [_yerlestir(pencere_kose(*v), Q_ARKA, -Q_DONUS, ayna=True) for v in pencereler().values()]}}
    return {"on": on, "arka": arka}
