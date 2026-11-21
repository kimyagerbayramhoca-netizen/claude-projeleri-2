#!/usr/bin/env python3
"""Yeni fikirler örneği · doğrulama. Önce: python3 uretec/kur.py (HTML, PDF, önizlemeler).

Denetler (kurulmuş HTML'den, PNG'lerden ve PDF'ten yeniden hesaplayarak):
  A. Usturlap ön yüzü: 20 elementin Z, simge, Türkçe ad (yerel-cerceve/uretec/elementler.py), katman dizilimi,
     periyot/grup, yaygın iyon (kural); dönme açıları; pencerelere sığma (fontTools ölçüsü); delik geometrisi.
  B. Mol çarkı: basılan her çentiğin açısı = 360°·log10(değer); iki ölçek aynı yönde; ok = 1; 2000 rastgele (m, M)
     çiftinde basılı çentiklerden okunan n = m/M; çözümlü örnek; sarı çizgilerin mol kütleleri; köprüler; ayna yerleşim;
     dışmerkezlik duyarlılığı (bilgi).
  C. Gizli cevap: cevaplar element verisinden; çeldiriciler yanlış; seçicilik ölçüleri PNG + maskelerden.
  D. Kâğıtta animasyon: şerit ve yarık geometrisi; çakışma yok; her dönüşün çarpışma nedeni; hidratlaşma yönleri;
     perde benzetiminde her karenin temizliği (PDF'ten).
  E. Ebru sayfası: doğrulanmış dört bilgi ve kurgu notu; F. yazı tipleri ve glifler; G. PDF (sayfa, Type 3, taşma).
"""
import html as H
import json
import math
import os
import random
import re
import subprocess
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
for _y in (os.path.join(KITAP, "yerel-cerceve", "uretec"), os.path.join(KITAP, "yerel-ortak", "cizim"), BURA):
    sys.path.insert(0, _y)
import elementler as EL  # noqa: E402
import usturlap as US  # noqa: E402
import gizli as GZ  # noqa: E402
import animasyon as AN  # noqa: E402
import olcu  # noqa: E402

PDF = os.path.join(KLASOR, "yeni-fikirler-ornek.pdf")
SONUC = []


def denet(ad, kosul, ayrinti=""):
    SONUC.append((ad, bool(kosul), ayrinti))
    if not kosul:
        print(f"  HATA · {ad} · {ayrinti}")


def oku(yol):
    with open(yol, encoding="utf-8") as fp:
        return fp.read()


def duz(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def grup(html, nitelik):
    """<g ... nitelik ...> ... </g> bloğunu iç içe g'leri sayarak çıkarır."""
    i = html.index(nitelik)
    bas = html.rindex("<g", 0, i)
    derinlik, j = 0, bas
    for m in re.finditer(r"<(/?)g\b[^>]*?(/?)>", html[bas:]):
        if m.group(2):
            continue
        derinlik += -1 if m.group(1) else 1
        if derinlik == 0:
            j = bas + m.end()
            break
    return html[bas:j]


# ------------------------------------------------------------------ A. element çarkı
def kural_iyon(e):
    s, g, sinif = e["sembol"], e["grup"], EL.sinif(e["sembol"])
    if s == "H":
        return "H+ · H−"
    if sinif == "soy":
        return "yok"
    if s in ("B", "C", "Si"):
        return f"{g - 10} bağ"
    if g in (1, 2):
        return f"{s}{'' if g == 1 else g}+"
    if g == 13:
        return f"{s}3+"
    if g in (15, 16, 17):
        y = 18 - g
        return f"{s}{'' if y == 1 else y}−"
    return "?"


def denet_cark(h9):
    P = grup(h9, 'data-yuz="P-on"')
    gruplar = re.findall(r'<g transform="rotate\(([-\d.]+)\)" data-z="(\d+)" data-psi="([-\d.]+)">(.*?)</g>', P, flags=re.S)
    denet("A1 P ön yüzünde 20 element grubu", len(gruplar) == 20, f"{len(gruplar)} grup")
    for don, z, psi, ic in gruplar:
        z = int(z)
        e = EL.ELEMENTLER[z - 1]
        p, g = EL.yer(z)
        alan = {a: duz(t) for a, t in re.findall(r'data-alan="(\w+)">(.*?)</text>', ic, flags=re.S)}
        diz = US.katmanlar(z)
        denet(f"A2 Z={z} simge/ad/Z", alan.get("sembol") == e["sembol"] and alan.get("ad") == e["ad"] and alan.get("z") == str(z),
              f"{alan.get('z')} {alan.get('sembol')} {alan.get('ad')}")
        denet(f"A3 Z={z} dizilim", alan.get("dizilim") == "·".join(map(str, diz)) and sum(diz) == z and len(diz) == p
              and all(k <= c for k, c in zip(diz, (2, 8, 8, 2))), alan.get("dizilim"))
        degerlik = diz[-1]
        beklenen_grup = 18 if (z == 2) else (degerlik if degerlik <= 2 else degerlik + 10)
        denet(f"A4 Z={z} periyot/grup", alan.get("periyot") == str(p) and alan.get("grup") == str(g) and g == beklenen_grup,
              f"{alan.get('periyot')}/{alan.get('grup')} (beklenen {p}/{g})")
        iyon = re.sub(r"\s*·\s*", " · ", alan.get("iyon", "")).replace(" ", " ").strip()
        denet(f"A5 Z={z} yaygın iyon", iyon == kural_iyon({"sembol": e["sembol"], "grup": g}), f"{iyon!r} ≠ {kural_iyon({'sembol': e['sembol'], 'grup': g})!r}")
        denet(f"A6 Z={z} dönme açısı", abs(float(psi) - US.ADIM * (z - 1)) < 1e-6 and abs(float(don) - float(psi)) < 1e-6, psi)
        # pencerelere sığma (fontTools)
        r1, r2, ya = US.KURSU_P
        gen_ad = 2 * 62.35 * math.sin(math.radians(ya)) - 1.0
        w_ad = olcu.genislik(e["ad"], "nunito", 800, 6.8 * olcu.PT)
        w_sem = olcu.genislik(e["sembol"], "baloo", 800, 15.5 * olcu.PT)
        denet(f"A7 Z={z} kürsüye sığar", w_ad <= gen_ad and w_sem <= 2 * 65.5 * math.sin(math.radians(ya)) - 1.0, f"ad {w_ad:.1f} > {gen_ad:.1f}")
        bant = US.BANT_A[1] - US.BANT_A[0] - 1.2
        w_diz = olcu.genislik(alan.get("dizilim", ""), "nunito", 900, 9.4 * olcu.PT)
        w_iyon = olcu.genislik(iyon.replace("+", "+").replace(" · ", "  ·  "), "nunito", 900, 8.6 * olcu.PT)
        denet(f"A8 Z={z} doğu penceresine sığar", w_diz <= bant and w_iyon <= bant, f"dizilim {w_diz:.1f}, iyon {w_iyon:.1f} > {bant:.1f}")
    # pencere ve bant geometrisi
    denet("A9 pencere yarım açısı < kart yarım açısı < 9°", US.BANT_A[2] < US.KART_YARI < US.ADIM / 2 and US.KURSU_P[2] < US.KART_YARI)
    denet("A10 bantlar yarıkla kesişmez", US.BANT_A[1] + .8 < US.YARIK[0] and US.BANT_B[1] < US.BANT_A[0] - 1, f"{US.BANT_A} {US.YARIK}")
    denet("A11 yarık Q'nun altında (önden görünmez)", US.YARIK[1] + 2.5 <= US.R_Q, f"yarık dış {US.YARIK[1]} · R_Q {US.R_Q}")
    denet("A12 kürsü penceresinin alt rayı ≥ 3 mm", US.KURSU_P[0] - US.R_Q >= 3.0, f"{US.KURSU_P[0] - US.R_Q:.1f} mm")
    dis = US.q_dis_noktalar(720)

    def icinde(px, py, poly):
        ic = False
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[i - 1]
            if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
                ic = not ic
        return ic

    def kenar_uzaklik(px, py, poly):
        en = 1e9
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[i - 1]
            dx, dy = x2 - x1, y2 - y1
            t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy or 1)))
            en = min(en, math.hypot(px - x1 - t * dx, py - y1 - t * dy))
        return en
    for ad, v in US.pencereler().items():
        kose = US.pencere_kose(*v)
        pay = min(kenar_uzaklik(x, y, dis) for x, y in kose)
        denet(f"A13 {ad} penceresi Q'nun içinde, kenara ≥ 2,5 mm", all(icinde(x, y, dis) for x, y in kose) and pay >= 2.5, f"pay {pay:.2f} mm")
    denet("A14 sayfa yerleşimi: diskler arası ≥ 6 mm, sayfa içinde", math.dist(US.P_ON, US.Q_ON) - US.R_P - US.R_Q >= 6
          and US.P_ON[0] - US.R_P >= 10 and US.Q_ON[0] + US.R_Q <= 200 and US.Q_ON[1] + US.R_Q <= 281, f"{math.dist(US.P_ON, US.Q_ON) - US.R_P - US.R_Q:.1f} mm")
    denet("A15 arka yüz ayna yerleşimi (uzun kenardan çevirme)", US.P_ARKA == (210 - US.P_ON[0], US.P_ON[1]) and US.Q_ARKA == (210 - US.Q_ON[0], US.Q_ON[1]))
    on, arka = sorted(US.kopru_acilari_on()), sorted((-a) % 360 for a in US.kopru_acilari_arka())
    denet("A16 köprüler iki yüzde aynı yerde (ayna)", all(abs(a - b) < 1e-9 for a, b in zip(on, arka)))
    denet("A17 kesme ve merkez işaretleri ön yüzde", h9.count('stroke-width=".26"') >= 2 and h9.count("M-3.2 0 H3.2") >= 2)


# ------------------------------------------------------------------ B. mol çarkı
def tikler(h10, yuz, olcek):
    G = grup(h10, f'data-yuz="{yuz}"')
    out = []
    for deg, x1, y1 in re.findall(rf'<line data-olcek="{olcek}" data-deger="([\d.]+)"[^>]*?x1="([-\d.]+)" y1="([-\d.]+)"', G):
        aci = math.degrees(math.atan2(float(x1), -float(y1))) % 360
        out.append((float(deg), aci))
    return sorted(out)


def oku_olcek(t, aci):
    """basılı çentiklerden ters okuma (komşu iki çentik arasında açıyla doğrusal: gözle kestirme)."""
    aci %= 360
    for (v1, a1), (v2, a2) in zip(t, t[1:] + [(10.0, 360.0)]):
        if a1 <= aci <= a2:
            return v1 + (v2 - v1) * (aci - a1) / (a2 - a1)
    return t[0][0]


def aci_olcek(t, v):
    for (v1, a1), (v2, a2) in zip(t, t[1:] + [(10.0, 360.0)]):
        if v1 <= v <= v2:
            return a1 + (a2 - a1) * (v - v1) / (v2 - v1)
    raise ValueError(v)


def mantis(v):
    return v / 10 ** math.floor(math.log10(v))


def denet_mol(h10):
    tm, tM = tikler(h10, "P-arka", "m"), tikler(h10, "Q-arka", "M")
    denet("B1 dış ölçek çentik sayısı", len(tm) == len(US.olcek_tikleri()), f"{len(tm)}")
    hata_m = max(abs(a - (360 * math.log10(v)) % 360) for v, a in tm)
    hata_M = max(abs(a - (360 * math.log10(v)) % 360) for v, a in tM if v > 1)
    denet("B2 her çentik 360°·log10(x) açısında (< 0,01°)", hata_m < .01 and hata_M < .01, f"dış {hata_m:.4f}°, iç {hata_M:.4f}°")
    denet("B3 iki ölçek de arkadan bakana göre saat yönünde artar", all(b[1] > a[1] for a, b in zip(tm, tm[1:])) and all(b[1] > a[1] for a, b in zip(tM[1:], tM[2:])))
    ok = re.search(r'<line data-olcek="M" data-deger="1" data-ok="1" x1="0" y1="([-\d.]+)"', grup(h10, 'data-yuz="Q-arka"'))
    denet("B4 kırmızı ok iç ölçekte 1'de (tepede)", ok is not None)
    rng = random.Random(2026)
    en_buyuk, ornek = 0.0, None
    for _ in range(2000):
        m = 10 ** rng.uniform(-1, 3)
        M = 10 ** rng.uniform(0, 2.6)
        am, aM = aci_olcek(tm, mantis(m)), aci_olcek(tM, mantis(M))
        gama = aM - am                      # P'nin dönüşü: m, M'nin hizasına gelir
        n_okunan = oku_olcek(tm, -gama)     # ok (Q'da 0°) P'nin hangi değerini gösterir
        hata = abs(n_okunan / mantis(m / M) - 1)
        if hata > en_buyuk:
            en_buyuk, ornek = hata, (round(m, 3), round(M, 3))
    denet("B5 2000 rastgele (m, M): okunan n = m/M (hata < %0,5)", en_buyuk < .005, f"en büyük %{100 * en_buyuk:.3f} {ornek}")
    # çözümlü örnek: 53 g Na2CO3, M = 2·23 + 12 + 3·16
    M_soda = 2 * 23 + 12 + 3 * 16
    gama = aci_olcek(tM, mantis(M_soda)) - aci_olcek(tm, mantis(53))
    n = oku_olcek(tm, -gama)
    denet("B6 örnek: M(Na2CO3) = 106; 5,3 ↔ 1,06 → ok 5,0 → n = 0,5 mol", M_soda == 106 and abs(n - 5.0) < .01 and abs(53 / 106 - .5) < 1e-12, f"okunan {n:.3f}")
    gama2 = aci_olcek(tM, 1.8) - aci_olcek(tm, 3.6)
    denet("B7 önizleme örneği: 36 g su (M 18) → 2 mol", abs(oku_olcek(tm, -gama2) - 2.0) < .01 and 2 * 1 + 16 == 18)
    kutle = {"H": 1, "C": 12, "O": 16, "Na": 23, "Cl": 35.5}
    formul = {"CH₄": {"C": 1, "H": 4}, "H₂O": {"H": 2, "O": 1}, "O₂": {"O": 2}, "CO₂": {"C": 1, "O": 2}, "NaCl": {"Na": 1, "Cl": 1}, "soda": {"Na": 2, "C": 1, "O": 3}}
    gosterge = re.findall(r'<line data-gosterge="([^"]+)" data-deger="([\d.]+)" x1="([-\d.]+)" y1="([-\d.]+)"', grup(h10, 'data-yuz="Q-arka"'))
    dogru = all(abs(float(d) - mantis(sum(kutle[e] * n for e, n in formul[ad].items()))) < 1e-9
                and abs(math.degrees(math.atan2(float(x), -float(y))) % 360 - 360 * math.log10(float(d))) < .01 for ad, d, x, y in gosterge)
    denet("B8 sarı çizgiler: mol kütleleri ve açıları", len(gosterge) == 6 and dogru, f"{len(gosterge)} çizgi")
    kop = US.kopru_acilari_arka()
    kapali = len(kop) * math.degrees(US.KOPRU_EN / ((US.YARIK[0] + US.YARIK[1]) / 2)) / 360
    denet("B9 köprüler dış ölçekte 1,3 · 2,6 · 6,6'da; kapalı pay < %3", [round(mantis(10 ** (a / 360)), 2) for a in kop] == [1.3, 2.6, 6.6] and kapali < .03,
          f"%{100 * kapali:.1f}")
    # dışmerkezlik (bilgi): iç ölçek 1 mm kayık basılırsa en büyük okuma hatası
    r = US.YARIK[1] - 1.5
    en = 0
    for t in range(360):
        for yon in range(0, 360, 30):
            ex, ey = math.cos(math.radians(yon)), math.sin(math.radians(yon))
            x, y = r * math.sin(math.radians(t)) + ex, -r * math.cos(math.radians(t)) + ey
            fark = (math.degrees(math.atan2(x, -y)) - t + 180) % 360 - 180
            en = max(en, abs(10 ** (fark / 360) - 1))
    denet("B10 dışmerkezlik bilgisi (1 mm kaymada okuma hatası < %1,5)", en < .015, f"%{100 * en:.2f}")
    return en_buyuk, en


# ------------------------------------------------------------------ C. gizli cevap
def denet_gizli(h9):
    import numpy as np
    from PIL import Image
    el = {e["z"]: e for e in EL.ELEMENTLER[:20]}
    beklenen = {1: "·".join(map(str, US.katmanlar(13))), 2: f"{17 + 1} elektron", 3: f"{EL.yer(12)[0]}. periyot",
                4: [f"{el[z]['sembol']} · {el[z]['ad'].lower()}" for z in range(1, 21) if EL.yer(z) == (2, 15)][0],
                5: ("Ca", f"{EL.yer(20)[1]}+"), 6: "Ne · soy gaz" if EL.sinif("Ne") == "soy" and EL.sinif("Na") == "metal" else "?"}
    for s in GZ.SORULAR:
        n = s["no"]
        cevap = s["cevap"] if s["cevap"][1] else s["cevap"][0]
        denet(f"C1 soru {n} cevabı veriden", cevap == beklenen[n], f"{cevap} ≠ {beklenen[n]}")
        denet(f"C2 soru {n} çeldiricileri yanlış ve farklı", all(c != s["cevap"] for c in s["celdirici"]) and len(set(s["celdirici"])) == 3)
        denet(f"C3 soru {n} sayfada", f'data-gizli="{n}"' in h9 and f"gorsel/gizli-{n}.png" in h9)
    for ad in [str(s["no"]) for s in GZ.SORULAR] + ["deneme"]:
        img = np.asarray(Image.open(os.path.join(KLASOR, "gorsel", f"gizli-{ad}.png")).convert("RGB")).astype(np.float64) / 255
        mz = np.load(os.path.join(KLASOR, "gorsel", f"gizli-{ad}-maske.npz"))
        o = GZ.olc(GZ.srgb2lin(img), mz["T"] / 255, [d / 255 for d in mz["D"]])
        denet(f"C4 kutu {ad}: kırmızı camla okunur", o["cam"] >= GZ.ESIK["cam"] and o["cam_oran"] >= GZ.ESIK["cam_oran"] and o["cam_weber"] >= GZ.ESIK["cam_weber"],
              f"karşıtlık {o['cam']}, çeldiriciye oran {o['cam_oran']}, Weber {o['cam_weber']}")
        denet(f"C5 kutu {ad}: çıplak gözle gizli (her kanalda oran ≤ 1)", o["goz_oran_enbuyuk"] <= GZ.ESIK["goz_oran"], str(o["goz_oran"]))
        boy = Image.open(os.path.join(KLASOR, "gorsel", f"gizli-{ad}.png")).size
        mm = GZ.KUTU if ad != "deneme" else GZ.KUTU_DENEME
        denet(f"C6 kutu {ad}: {GZ.DPI} dpi, {mm[0]:g}×{mm[1]:g} mm", boy == (int(round(mm[0] * GZ.MM)), int(round(mm[1] * GZ.MM))), str(boy))
    # mürekkep ayrımı: gürültü renklerinde C yok, cevapta yalnız C
    denet("C7 gürültü ve çeldiricilerde camgöbeği yok; cevap yalnız C", all(len(r) == 3 for r in GZ.RENKLER) and 0 < GZ.C_YAZI <= .5
          and all(len(c) == 2 for c in GZ.CELDIRICI_RENK))


# ------------------------------------------------------------------ D. kâğıtta animasyon
def denet_animasyon(h10):
    denet("D1 yarık genişliği 0,5–0,8 mm, 4–6 kare", .5 <= AN.W <= .8 and 4 <= AN.N <= 6, f"w {AN.W} mm, N {AN.N}")
    for ad in ("gaz", "tuz"):
        G = grup(h10, f'data-panel="{ad}"')
        tamam = True
        for k in range(AN.N):
            cp = re.search(rf'<clipPath id="an-{ad}-{k}">(.*?)</clipPath>', G, flags=re.S).group(1)
            xs = [float(x) for x in re.findall(r'<rect x="([-\d.]+)"', cp)]
            ws = [float(w) for w in re.findall(r'width="([\d.]+)"', cp)]
            tamam &= len(xs) == 50 and all(abs(x - (j * AN.P + k * AN.W)) < 1e-6 for j, x in enumerate(xs)) and all(abs(w - AN.W) < 1e-9 for w in ws)
        denet(f"D2 {ad}: kare k, j. dönemde [j·p + k·w] şeridinde (50 dönem)", tamam)
    S = re.search(r'<svg class="perde-svg".*?</svg>', h10, flags=re.S).group(0)
    tamam = True
    for y1, _ in AN.PERDE_Y:
        cub = sorted((float(x), float(w)) for x, y, w in re.findall(rf'<rect data-cubuk="-?\d+" x="([\d.]+)" y="({y1:g})" width="([\d.]+)"', S))
        yariklar = [b[0] - (a[0] + a[1]) for a, b in zip(cub, cub[1:])]
        ilk = [x + w for x, w in cub if x + w > AN.X0 - 1e-6][0]
        kalan = (ilk - AN.X0) % AN.P
        tamam &= all(abs(g - AN.W) < 1e-6 for g in yariklar) and min(kalan, AN.P - kalan) < 1e-6
    denet("D3 perde: çubuk 3,0 mm, yarık 0,6 mm, yarıklar 0. karenin şeritlerinde", tamam)
    denet("D4 perde ve geçme aynı artılarla hizalanır", h10.count('r="1.4" fill="none"') >= 8)
    # gaz fiziği
    tan, carp, hiz = AN.gaz_verisi()
    zn = []
    for zi, z in enumerate(AN.GAZ_ZINCIR):
        zn += [zi] * z[3]
    bosluk = min(math.dist(tan[i]["konum"][k], tan[j]["konum"][k]) - 2 * AN.R_G for k in range(AN.N)
                 for i in range(len(tan)) for j in range(i + 1, len(tan)) if zn[i] != zn[j] and tan[i]["kutu"] == tan[j]["kutu"])
    komsu = min(math.dist(tan[i]["konum"][k], tan[i + 1]["konum"][k]) - 2 * AN.R_G for k in range(AN.N) for i in range(len(tan) - 1) if zn[i] == zn[i + 1])
    denet("D5 gaz: hiçbir karede tanecikler üst üste binmez", bosluk > 0 and komsu > -1e-6, f"en küçük boşluk {bosluk:.2f} mm")
    nedensiz = 0
    for i, t in enumerate(tan):
        for k in range(AN.N):
            a, b, c = t["konum"][k - 1], t["konum"][k], t["konum"][(k + 1) % AN.N]
            v1, v2 = (b[0] - a[0], b[1] - a[1]), (c[0] - b[0], c[1] - b[1])
            if v1[0] * v2[0] + v1[1] * v2[1] < -1e-9 or (abs(v1[0]) + abs(v1[1]) > 1e-9 and abs(v2[0]) + abs(v2[1]) < 1e-9):
                x1, y1, x2, y2 = AN.KUTU[t["kutu"]]
                duvar = min(abs(b[0] - x1), abs(b[0] - x2), abs(b[1] - y1), abs(b[1] - y2)) - AN.R_G
                diger = min(math.dist(b, u["konum"][k]) - 2 * AN.R_G for j, u in enumerate(tan) if j != i and u["kutu"] == t["kutu"])
                if not (abs(duvar) < 1e-6 or abs(diger) < 1e-6):
                    nedensiz += 1
    denet("D6 gaz: her yön değişimi duvara ya da taneciğe değerken (esnek çarpışma)", nedensiz == 0, f"{nedensiz} nedensiz dönüş")
    soguk = [t for t in tan if t["kutu"] == "soguk"]
    duvar_say = {k: sum(1 for c in carp if c["tur"] == "duvar" and c["kutu"] == k) for k in ("soguk", "sicak")}
    denet("D7 gaz: aynı sayıda tanecik; sıcakta daha hızlı ve duvara daha sık", len(soguk) == len(tan) - len(soguk) == 8
          and min(hiz["sicak"]) > max(hiz["soguk"]) and duvar_say["sicak"] > duvar_say["soguk"], f"hız {hiz} · duvar {duvar_say}")
    # tuz: çakışma yok, yönler doğru
    def nesneler(sek):
        obj, bekle = [], []
        for s in sek:
            if s[0] != "d":
                continue
            if abs(s[3] - AN.R_H) < 1e-9:
                bekle.append(s)
            elif abs(s[3] - AN.R_O) < 1e-9:
                obj.append(("su", bekle + [s]))
                bekle = []
            else:
                obj.append(("iyon", [s]))
        return obj
    cak = 0
    for k in range(AN.N):
        ob = nesneler(AN.tuz_sabit()) + nesneler(AN.tuz_kare(k))
        cak += sum(1 for i in range(len(ob)) for j in range(i + 1, len(ob)) if not (ob[i][0] == ob[j][0] == "iyon")
                   and min(math.dist(a[1:3], b[1:3]) - a[3] - b[3] for a in ob[i][1] for b in ob[j][1]) < -.05)
    denet("D8 tuz: hiçbir karede molekül/iyon çakışması yok", cak == 0, f"{cak}")
    son = nesneler(AN.tuz_kare(AN.N - 1))
    yon_dogru = 0
    for ad in ("Na", "Cl"):
        ix, iy = AN._iyon_konum(ad, AN.N - 1)
        kabuk = sorted((o for o in son if o[0] == "su"), key=lambda o: math.dist(o[1][-1][1:3], (ix, iy)))[:4]
        for o in kabuk:
            dO = math.dist(o[1][-1][1:3], (ix, iy))
            dH = min(math.dist(h[1:3], (ix, iy)) for h in o[1][:2])
            yon_dogru += (dO < dH) if ad == "Na" else (dH < dO)
    denet("D9 tuz: Na⁺'yı saran 4 su O ucuyla, Cl⁻'yi saran 4 su H ucuyla döner", yon_dogru == 8, f"{yon_dogru}/8")
    komsu_ok = all(a[2] != b[2] for a in AN.KRISTAL for b in AN.KRISTAL if abs(math.dist(a[:2], b[:2]) - AN.D) < 1e-6)
    denet("D10 tuz: kristalde her iyonun komşusu zıt yüklü; Cl⁻ > Na⁺", komsu_ok and AN.R_CL > AN.R_NA)
    # perde benzetimi (PDF)
    t = AN.temizlik(PDF)
    for ad, kareler in t.items():
        tam = [x for x in kareler if x["perde"] == "tam"]
        kotu = [x["kare"] for x in tam if x["en_iyi"] != x["kare"] or x["iou"][x["kare"] - 1] < .85 or x["hayalet"] > .03]
        en_kotu = min(x["iou"][x["kare"] - 1] for x in tam)
        kay = [x for x in kareler if x["perde"] != "tam"]
        denet(f"D11 {ad}: perde benzetiminde 6 karenin her biri temiz okunur", not kotu,
              f"en düşük IoU {en_kotu:.2f}, en çok hayalet %{100 * max(x['hayalet'] for x in tam):.1f}; kötü: {kotu}")
        denet(f"D12 {ad}: 0,12 mm kaymada da doğru kare baskın", all(x["en_iyi"] == x["kare"] for x in kay),
              f"hayalet en çok %{100 * max(x['hayalet'] for x in kay):.0f}")
    return t


# ------------------------------------------------------------------ E–G
def denet_ebru(h9):
    s4 = duz(re.search(r'<section class="sayfa usta s4">.*?</section>', h9, flags=re.S).group(0))
    for ad, kalip in (("kitre → viskozite", r"kitre.*koyulaştırılır.*viskozite"), ("öd → yüzey gerilimi", r"öd.*yüzey gerilimini.*düşürür"),
                      ("suda çözünmeyen doğal pigment", r"suda çözünmeyen doğal pigment"), ("UNESCO 2014", r"Geleneksel Türk Ebru Sanatı, 2014’te UNESCO"),
                      ("kurgusal usta notu", r"Revnak Usta kurgusal bir karakterdir"), ("Kendini dene", r"Kendini dene"), ("Hap Bilgi", r"Hap\s*bilgi")):
        denet(f"E1 ebru sayfası: {ad}", re.search(kalip, s4, flags=re.S | re.I) is not None)


def denet_yazi(h9, h10):
    tirnaksiz = 0
    for ad in ("usturlap.py", "gizli.py", "animasyon.py", "usta.py", "kur.py"):
        tirnaksiz += len(re.findall(r'font-family="Baloo', oku(os.path.join(BURA, ad))))
    denet("F1 bu klasörün SVG'lerinde Baloo adı tırnaklı", tirnaksiz == 0, f"{tirnaksiz} tırnaksız")
    eksik = []
    for h in (h9, h10):
        for svg in re.findall(r'<svg class="(?:usturlap-svg|anim-svg|perde-svg)".*?</svg>', h, flags=re.S):
            for nit, metin in re.findall(r'<text([^>]*)>(.*?)</text>', svg, flags=re.S):
                aile = "baloo" if "Baloo" in nit else "nunito"
                w = int(re.search(r'font-weight="(\d+)"', nit).group(1)) if "font-weight" in nit else 400
                for c in set(duz(metin)):
                    try:
                        olcu.genislik(c, aile, w, 1)
                    except ValueError:
                        eksik.append((aile, c))
    import usta as UT
    for svg in [UT.usta(), UT.unesco_rozet(), GZ.sema(), AN.kare_seridi("gaz")] + [UT.sir_cizim(n) for n in (1, 2, 3)]:
        for nit, metin in re.findall(r'<text([^>]*)>(.*?)</text>', svg, flags=re.S):
            aile = "baloo" if "Baloo" in nit else "nunito"
            w = int(re.search(r'font-weight="(\d+)"', nit).group(1)) if "font-weight" in nit else 400
            for c in set(duz(metin)):
                try:
                    olcu.genislik(c, aile, w, 1)
                except ValueError:
                    eksik.append((aile, c))
    denet("F2 SVG yazılarında fontta olmayan glif yok", not eksik, str(sorted(set(eksik))[:8]))
    yasak = [c for c in "→↓↑δαΔΣ↔✓★" for s in (oku(os.path.join(BURA, "sablon9.html")), oku(os.path.join(BURA, "sablon10.html"))) if c in s]
    denet("F3 şablon metinlerinde Nunito/Baloo'da olmayan simge yok (→ ↓ ↑ δ α Δ Σ ↔ ✓ ★)", not yasak, str(yasak))


def denet_pdf():
    from pypdf import PdfReader
    r = PdfReader(PDF)
    denet("G1 PDF 6 sayfa, A4", len(r.pages) == 6 and all(abs(float(p.mediabox.width) - 595.3) < 1.5 and abs(float(p.mediabox.height) - 841.9) < 1.5 for p in r.pages),
          f"{len(r.pages)} sayfa")
    t3 = subprocess.run(["pdffonts", PDF], capture_output=True, text=True).stdout.count("Type 3")
    denet("G2 pdffonts: Type 3 font yok", t3 == 0, f"{t3}")
    rapor = json.load(open(os.path.join(KLASOR, "kur-raporu.json"), encoding="utf-8"))
    denet("G3 render.js taşma denetimi temiz", all(not v for v in rapor["tasma"].values()) and all(v == 0 for v in rapor["kod"].values()), str(rapor["tasma"]))
    for n in range(1, 7):
        denet(f"G4 önizleme s{n:02d}.png var", os.path.exists(os.path.join(KLASOR, "onizleme", f"s{n:02d}.png")))
    for ad in ("usturlap-on.gif", "usturlap-arka.gif", "gizli-once-sonra.png", "gizli-mercek.gif", "animasyon-gaz.gif", "animasyon-tuz.gif"):
        denet(f"G5 önizleme {ad} var", os.path.exists(os.path.join(KLASOR, "onizleme", ad)))


def main():
    h9, h10 = oku(os.path.join(KLASOR, "yeni-9.html")), oku(os.path.join(KLASOR, "yeni-10.html"))
    print("A · element çarkı");      denet_cark(h9)
    print("B · mol çarkı");          hata, dis = denet_mol(h10)
    print("C · gizli cevap");        denet_gizli(h9)
    print("D · kâğıtta animasyon");  denet_animasyon(h10)
    print("E · ebru");               denet_ebru(h9)
    print("F · yazı");               denet_yazi(h9, h10)
    print("G · PDF");                denet_pdf()
    gecen = sum(1 for _, k, _ in SONUC if k)
    print(f"{gecen}/{len(SONUC)} denetim geçti · mol çarkı en büyük okuma hatası %{100 * hata:.3f} · 1 mm dışmerkezlikte %{100 * dis:.2f}")
    print("SONUÇ: hepsi doğru" if gecen == len(SONUC) else "SONUÇ: HATA VAR")
    return 0 if gecen == len(SONUC) else 1


if __name__ == "__main__":
    sys.exit(main())
