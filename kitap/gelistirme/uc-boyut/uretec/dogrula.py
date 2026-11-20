#!/usr/bin/env python3
"""3B (anaglif) örneği · doğrulama. Sayfalardaki her sayı koordinatlardan ya da örgüden YENİDEN hesaplanır;
anaglifin kanal düzeni ve ayrıklığın işareti hem motorda hem de kaydedilmiş PNG'lerde denetlenir.

    python3 uretec/dogrula.py        (önce: python3 uretec/kur.py)   →   SONUÇ: hepsi doğru
"""
import sys
sys.dont_write_bytecode = True
import json
import math
import os
import re
import subprocess

import numpy as np
from PIL import Image

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
sys.path.insert(0, os.path.join(KITAP, "yerel-ortak"))
sys.path.insert(0, BURA)
import uc_boyut as UB  # noqa: E402
import gorseller as G  # noqa: E402
import sahneler_uc as SU  # noqa: E402

HATA, SAY = [], [0]
SABLON = open(os.path.join(BURA, "sablon.html"), encoding="utf-8").read()
BILGI = json.load(open(os.path.join(KLASOR, "gorsel", "uc-boyut.json"), encoding="utf-8"))
NA = 6.02214e23
KUTLE = {"H": 1.008, "C": 12.011, "O": 15.999, "Na": 22.990, "Cl": 35.45}
EN = {"H": 2.20, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98, "Cl": 3.16}      # Pauling elektronegatifliği


def denet(ad, kosul, ayrinti=""):
    SAY[0] += 1
    print(("  ✓ " if kosul else "  ✗ ") + ad + (f"  [{ayrinti}]" if ayrinti else ""))
    if not kosul:
        HATA.append(ad)


def tr(x, h=1):
    return f"{x:.{h}f}".replace(".", ",")


def sayfada(metin, ad=None):
    denet(f"sayfada yazıyor: “{ad or metin}”", metin in SABLON)


def bolum(ad):
    print(f"\n{ad}")


# ================================================================== 1. bağ açıları (koordinatlardan)
bolum("1 · Bağ açıları ve molekül şekilleri (koordinatlardan)")
denet("dörtyüzlü açısı arccos(−1/3) = 109,47°", abs(UB.TETRA - 109.4712) < 1e-3, f"{UB.TETRA:.4f}")
for ad, kur, merkez, uc, hedef, etiket, uzun in (
        ("CH4", UB.ch4, 0, [1, 2, 3, 4], 109.47, "Düzgün dörtyüzlü · 109,5°", 1.09), ("NH3", UB.nh3, 0, [1, 2, 3], 106.7, "Üçgen piramit · ≈ 107°", 1.012),
        ("H2O", UB.h2o, 0, [1, 2], 104.5, "Kırık doğru · 104,5°", .9572), ("CO2", UB.co2, 0, [1, 2], 180.0, "Doğrusal · 180°", 1.16),
        ("BF3", UB.bf3, 0, [1, 2, 3], 120.0, "Düzlem üçgen · 120°", 1.31)):
    for y, durum in ((kur(), "kurulduğu gibi"), (G.yapi(ad.lower()), "sayfadaki görünümde (döndürülmüş)")):
        acilar = [y.aci(a, merkez, b) for i, a in enumerate(uc) for b in uc[i + 1:]]
        denet(f"{ad} · {len(acilar)} bağ açısı = {tr(hedef, 2)}° · {durum}", all(abs(a - hedef) < .02 for a in acilar), " ".join(f"{a:.2f}" for a in acilar))
    denet(f"{ad} · bağ uzunluğu {uzun} Å", all(abs(y.uzaklik(merkez, a) - uzun) < 1e-9 for a in uc))
    sayfada(etiket)
y = UB.nh3()
denet("NH3 · açı sayfada “≈ 107°”: 106,7 yuvarlanınca 107", round(y.aci(1, 0, 2)) == 107)
denet("NH3 düzlemsel değil (piramit): N, üç H'nin düzleminin dışında", abs(y.kure[0]["p"][1] - y.kure[1]["p"][1]) > .3, f"N düzlemden {abs(y.kure[0]['p'][1] - y.kure[1]['p'][1]):.2f} Å yukarıda")
y = UB.bf3()
denet("BF3 düzlemsel: dört atom aynı düzlemde", all(abs(a["p"][2]) < 1e-12 for a in y.kure))
y = UB.h2o()
ciftler = [a for a in y.kure if a["el"] == "e"]
denet("H2O · 2 ortaklanmamış çift (4 nokta), NH3 · 1 çift (2 nokta), CH4/CO2/BF3 merkezinde yok",
      len(ciftler) == 4 and sum(a["el"] == "e" for a in UB.nh3().kure) == 2 and not any(a["el"] == "e" for k in (UB.ch4, UB.co2, UB.bf3) for a in k().kure))

# ================================================================== 2. polarlık (bağ çekişlerinin vektör toplamı)
bolum("2 · Polarlık: bağ çekişlerinin vektör toplamı (birim vektörler, elektronegatif atoma doğru)")
for ad, kur, uc, beklenen in (("CH4", UB.ch4, [1, 2, 3, 4], "Apolar"), ("NH3", UB.nh3, [1, 2, 3], "Polar"), ("H2O", UB.h2o, [1, 2], "Polar"),
                              ("CO2", UB.co2, [1, 2], "Apolar"), ("BF3", UB.bf3, [1, 2, 3], "Apolar")):
    y = kur()
    top = np.zeros(3)
    for a in uc:
        u = y.kure[a]["p"] - y.kure[0]["p"]
        u = u / np.linalg.norm(u)
        top += u if EN[y.kure[a]["el"]] > EN[y.kure[0]["el"]] else -u       # çekiş, elektronegatifliği büyük olana doğru
    buyukluk = np.linalg.norm(top)
    sonuc = "Apolar" if buyukluk < 1e-9 else "Polar"
    denet(f"{ad} · çekişlerin toplamı {'sıfır' if sonuc == 'Apolar' else 'sıfır değil'} → {sonuc}", sonuc == beklenen, f"|Σ| = {buyukluk:.3f}")
    kart = SABLON[SABLON.index(f"{{{{ana|{ad.lower()}}}}}"):]
    denet(f"{ad} kartındaki etiket: {beklenen}", re.search(r'class="kutup (polar|apolar)">(\w+)<', kart).group(2) == beklenen)
denet("şema okları: C–O'da O'ya, O–H'de O'ya (elektronegatiflik O > C, O > H); N > H, F > B", EN["O"] > EN["C"] and EN["O"] > EN["H"] and EN["N"] > EN["H"] and EN["F"] > EN["B"])
dogrusal_su = np.array([1.0, 0, 0]) + np.array([-1.0, 0, 0])
denet("Kendini dene 2: H2O doğrusal olsaydı çekişler götürürdü → polar olmazdı", np.linalg.norm(dogrusal_su) == 0 and "2 olmazdı" in SABLON)
denet("Kendini dene 1: CCl4 dörtyüzlü (CH4 gibi) → dört eş çekişin toplamı sıfır → apolar", "1 apolar" in SABLON and EN["Cl"] > EN["C"])

# ================================================================== 3. örgüler: komşu sayıları, uzaklıklar, yoğunluklar
bolum("3 · Kristal örgüleri (geniş örgüden hesap)")
tuz = UB.nacl_orgu(5)
P, el = np.array([p for _, p in tuz]), [e for e, _ in tuz]
i0 = int(np.argmin(np.linalg.norm(P - P.mean(axis=0), axis=1)))
d = UB.en_yakin(P, i0)
kom = [j for j in range(len(P)) if abs(np.linalg.norm(P[j] - P[i0]) - d) < 1e-6]
denet("NaCl · en yakın komşu sayısı 6", len(kom) == 6 == UB.komsu_sayisi(P, i0, d))
denet("NaCl · komşuların hepsi zıt yüklü iyon (Na+ ↔ Cl−)", all(el[j] != el[i0] for j in kom))
denet("NaCl · Na+–Cl− aralığı a/2 = 2,82 Å", abs(d - 2.82) < 1e-9 and abs(UB.NACL_A / 2 - 2.82) < 1e-9, f"{d:.3f}")
ro = 4 * (KUTLE["Na"] + KUTLE["Cl"]) / (NA * (UB.NACL_A * 1e-8) ** 3)
denet("NaCl · örgüden yoğunluk ≈ 2,2 g/cm³ (hücrede 4 NaCl)", tr(ro) == "2,2", f"{ro:.3f}")
sayfada("Na<sup>+</sup>–Cl<sup>−</sup> 2,82 Å · 2,2 g/cm³", "Na+–Cl− 2,82 Å · 2,2 g/cm³")
sayfada("801&nbsp;°C’de erir", "801 °C (NaCl erime noktası 800,7 °C; kaynak değeri)")

E = np.array(UB.elmas_orgu(3)) * UB.ELMAS_A
i0 = int(np.argmin(np.linalg.norm(E - E.mean(axis=0), axis=1)))
d = UB.en_yakin(E, i0)
kom = [j for j in range(len(E)) if abs(np.linalg.norm(E[j] - E[i0]) - d) < 1e-6]
ac = [math.degrees(math.acos(np.clip((E[a] - E[i0]) @ (E[b] - E[i0]) / d / d, -1, 1))) for n, a in enumerate(kom) for b in kom[n + 1:]]
denet("elmas · her C'nin 4 komşusu", len(kom) == 4)
denet("elmas · C–C = a√3/4 = 1,54 Å", tr(d, 2) == "1,54" and abs(d - UB.ELMAS_A * 3 ** .5 / 4) < 1e-9, f"{d:.4f}")
denet("elmas · komşular arası 6 açının hepsi 109,5°", len(ac) == 6 and all(abs(a - UB.TETRA) < 1e-6 for a in ac))
ro_e = 8 * KUTLE["C"] / (NA * (UB.ELMAS_A * 1e-8) ** 3)
denet("elmas · örgüden yoğunluk ≈ 3,5 g/cm³ (hücrede 8 C)", tr(ro_e) == "3,5", f"{ro_e:.3f}")
sayfada("açı 109,5°")
sayfada("C–C 1,54 Å")

gr = UB.grafit_orgu(4, 3)
Pg, kat = np.array([p for _, p in gr]), np.array([L for L, _ in gr])
orta = np.where(kat == 1)[0]
i0 = int(orta[np.argmin(np.linalg.norm(Pg[orta][:, [0, 2]], axis=1))])
d = UB.en_yakin(Pg, i0)
kom = [j for j in range(len(Pg)) if abs(np.linalg.norm(Pg[j] - Pg[i0]) - d) < 1e-6]
ac = [math.degrees(math.acos(np.clip((Pg[a] - Pg[i0]) @ (Pg[b] - Pg[i0]) / d / d, -1, 1))) for n, a in enumerate(kom) for b in kom[n + 1:]]
denet("grafit · her C'nin 3 komşusu (aynı tabakada)", len(kom) == 3 and all(kat[j] == 1 for j in kom))
denet("grafit · C–C 1,42 Å, açılar 120°", abs(d - 1.42) < 1e-9 and all(abs(a - 120) < 1e-6 for a in ac))
diger = Pg[kat != 1]
denet("grafit · tabakalar arası 3,35 Å (bağ uzunluğunun 2,4 katı)", abs(np.abs(diger[:, 1] - Pg[i0][1]).min() - 3.35) < 1e-9 and abs(3.35 / 1.42 - 2.36) < .01)
ro_g = 4 * KUTLE["C"] / (NA * (3 ** .5 / 2) * (3 ** .5 * UB.GRAFIT_D) ** 2 * (2 * UB.GRAFIT_C) * 1e-24)
denet("grafit · örgüden yoğunluk ≈ 2,3 g/cm³ (altıgen hücrede 4 C)", tr(ro_g) == "2,3", f"{ro_g:.3f}")
sayfada("C–C 1,42&nbsp;Å · tabaka arası 3,35&nbsp;Å", "C–C 1,42 Å · tabaka arası 3,35 Å")
sayfada("Elmasta 4 komşu (3,5&nbsp;g/cm³), grafitte 3 komşu (2,3&nbsp;g/cm³)", "elmasta 4 komşu (3,5 g/cm³), grafitte 3 komşu (2,3 g/cm³)")
denet("elmas grafitten yoğun (aynı element, farklı diziliş)", ro_e > ro_g)

B = np.array(UB.buz_orgu(2))
i0 = int(np.argmin(np.linalg.norm(B - B.mean(axis=0), axis=1)))
d = UB.en_yakin(B, i0)
kom = [j for j in range(len(B)) if abs(np.linalg.norm(B[j] - B[i0]) - d) < 1e-3]
ac = [math.degrees(math.acos(np.clip((B[a] - B[i0]) @ (B[b] - B[i0]) / d / d, -1, 1))) for n, a in enumerate(kom) for b in kom[n + 1:]]
denet("buz · her H2O'nun 4 komşusu (O···O)", len(kom) == 4)
denet("buz · O···O 2,76 Å, komşu yönleri dörtyüzlü (109,5°)", abs(d - 2.76) < 1e-3 and all(abs(a - UB.TETRA) < .01 for a in ac), f"{d:.3f}")
ro_b = 4 * (2 * KUTLE["H"] + KUTLE["O"]) / (NA * (3 ** .5 / 2) * UB.BUZ_A ** 2 * UB.BUZ_C * 1e-24)
denet("buz · örgüden yoğunluk ≈ 0,92 g/cm³ < su 1,00 g/cm³ → buz yüzer", tr(ro_b, 2) == "0,92" and ro_b < 1.00, f"{ro_b:.3f}")
sayfada("buz (0,92&nbsp;g/cm³) sudan (1,00&nbsp;g/cm³) hafiftir", "buz (0,92 g/cm³) sudan (1,00 g/cm³) hafiftir")
sayfada("O···O 2,76 Å")

bolum("3b · Sayfadaki örgü parçaları (çizilen yapı)")
y = UB.nacl()
denet("NaCl resmi · 27 iyon = 13 Na+ + 14 Cl−, 54 kafes çubuğu", [sum(a["el"] == e for a in y.kure) for e in ("Na", "Cl")] == [13, 14] and len(y.bag) == 54)
denet("NaCl resmi · koyu iyon Na+, kalın çubuk 6, uçlarında 6 Cl−", y.kure[y.odak]["el"] == "Na" and sum(b["vurgu"] for b in y.bag) == 6
      and all(y.kure[j]["el"] == "Cl" for j in y.komsular(y.odak)) and len(y.komsular(y.odak)) == 6)
y = UB.elmas()
denet("elmas resmi · 18 atom, 16 bağ; koyu atomun 4 kalın bağı", len(y.kure) == 18 and len(y.bag) == 16 and sum(b["vurgu"] for b in y.bag) == 4 == len(y.komsular(y.odak)))
y = UB.grafit()
denet("grafit resmi · 3 tabaka × 16 atom; koyu atomun 3 kalın bağı; tabakalar arası kesik çizgi var",
      len(y.kure) == 48 and sum(b["vurgu"] for b in y.bag) == 3 == len(y.komsular(y.odak, ("tek",))) and sum(b["tur"] == "zayif" for b in y.bag) >= 6)
denet("grafit resmi · kesik çizgiler tam 3,35 Å (üst üste gelen atomlar)", all(abs(y.uzaklik(b["i"], b["j"]) - 3.35) < 1e-9 for b in y.bag if b["tur"] == "zayif"))
y = UB.buz()
O = [i for i, a in enumerate(y.kure) if a["el"] == "O"]
denet("buz resmi · 20 H2O (20 O + 40 H); her O'da tam 2 H (kovalent)", len(O) == 20 and sum(a["el"] == "H" for a in y.kure) == 40 and all(len(y.komsular(o, ("tek",))) == 2 for o in O))
denet("buz resmi · 27 hidrojen bağı; her O–O çizgisinde tam 1 H, O–H···O doğrusal", len(y.hbag) == 27 and len({tuple(sorted((v, a))) for v, _, a in y.hbag}) == 27
      and all(abs(y.aci(v, h, a) - 180) < .01 and abs(y.uzaklik(v, a) - 2.76) < 1e-3 for v, h, a in y.hbag))
denet("buz resmi · koyu molekülün 4 hidrojen bağı (2 veren + 2 alan), 4'ü de kalın",
      sum(v == y.odak for v, _, _ in y.hbag) == 2 and sum(a == y.odak for _, _, a in y.hbag) == 2 and sum(b["vurgu"] for b in y.bag) == 4)
for n, metin in ((6, "Sofra tuzu"), (4, "Elmas"), (3, "Grafit"), (4, "Buz")):
    kart = SABLON[SABLON.index(f'<span class="et">{metin}'):]
    denet(f"{metin} kartındaki büyük sayı: {n} komşu", re.search(r'<b class="sayi">(\d)</b>', kart).group(1) == str(n))

# ================================================================== 4. 10. sınıf sayfası
bolum("4 · Gaz kutusu, 22,4 L küpü, hidrasyon")
kenar = (22.4 * 1000) ** (1 / 3)
denet("22,4 L = 22 400 cm³ → küp kenarı ∛22 400 = 28,2 cm", tr(kenar) == "28,2", f"{kenar:.3f}")
denet("28,2 · 28,2 · 28,2 ≈ 22 400 (fark < %0,2)", abs(28.2 ** 3 - 22400) / 22400 < .002, f"{28.2 ** 3:.0f}")
top = math.pi / 6 * UB.TOP_CAP_CM ** 3 / 1000
denet("5 numara top: çevre 68–70 cm → çap 21,6–22,3 cm → ≈ 22 cm", 68 / math.pi <= UB.TOP_CAP_CM <= 70 / math.pi + .05, f"{68 / math.pi:.1f}–{70 / math.pi:.1f}")
denet("çapı 22 cm olan kürenin hacmi ≈ 5,6 L", tr(top) == "5,6", f"{top:.3f}")
denet("22,4 / 5,6 = 4; kesin oran 4,02 → “yaklaşık 4 top”", abs(22.4 / 5.6 - 4) < 1e-9 and abs(22.4 / top - 4) < .05, f"{22.4 / top:.2f}")
y = UB.mol_kupu()
tp = [a for a in y.kure if a["desen"] == "top"][0]
denet("resimdeki küp kenarı 28,19 cm, top yarıçapı 11 cm; ikisi aynı zeminde", abs(y.kenar - kenar) < 1e-9 and tp["r"] == 11 and abs(tp["p"][1] - 11) < 1e-9)
for m in ("28,2&nbsp;cm", "5,6&nbsp;L", "22,4 / 5,6 = <b>4</b>", "1 mol gaz ≈ 4 top", "6,02·10<sup>23</sup>"):
    sayfada(m)
R_gaz = 0.082057
denet("NŞA (0 °C, 1 atm): RT/P = 22,4 L", tr(R_gaz * 273.15) == "22,4", f"{R_gaz * 273.15:.3f}")
denet("oda koşulları (25 °C, 1 atm): RT/P = 24,5 L", tr(R_gaz * 298.15) == "24,5", f"{R_gaz * 298.15:.3f}")
sayfada("<b>22,4&nbsp;L</b>. Oda koşulları (25&nbsp;°C, 1&nbsp;atm): <b>24,5&nbsp;L</b>", "NŞA 22,4 L · oda koşulları 24,5 L")
aralik = (22.4e-3 / NA) ** (1 / 3) * 1e9
denet("NŞA'da tanecikler arası ortalama uzaklık ≈ 3,3 nm; N2 çapı ≈ 0,36 nm → yaklaşık 10 katı", 8 < aralik / .364 < 12, f"{aralik:.2f} nm · oran {aralik / .364:.1f}")
y = UB.gaz_kutusu()
n2, o2 = sum(t["el"] == "N" for t in y.tanecik), sum(t["el"] == "O" for t in y.tanecik)
denet("gaz kutusu · 8 N2 + 2 O2 = 4'e 1; havada N2/O2 = 78/21 ≈ 3,7 (yaklaşık 4'e 1)", (n2, o2) == (8, 2) and abs(78 / 21 - 4) < .5)
vz = np.array([t["v"][2] for t in y.tanecik])
denet("gaz kutusu · hız yönleri üç boyutta: öne ve arkaya gidenler de var", (vz > .25).sum() >= 2 and (vz < -.25).sum() >= 2, " ".join(f"{v:+.2f}" for v in vz))
lo, hi = y.sinir()
denet("gaz kutusu · bütün tanecikler ve izler kutunun içinde", all((np.abs(a["p"]) + a["r"] <= hi + 1e-9).all() for a in y.kure) and all((np.abs(c["a"]) <= hi).all() and (np.abs(c["b"]) <= hi).all() for c in y.cubuk))
sayfada("8 N<sub>2</sub> + 2 O<sub>2</sub>")
for iyon, ad in (("Na", "Na+"), ("Cl", "Cl−")):
    y = UB.hidrasyon(iyon)
    m = y.iyon
    denet(f"hidrasyon {ad} · 6 su molekülü, sekizyüzlü (iyon–O uzaklıkları eşit)", len(y.su) == 6 and len({round(y.uzaklik(m, o), 6) for o, _, _ in y.su}) == 1)
    denet(f"hidrasyon {ad} · her suda H–O–H = 104,5°", all(abs(y.aci(h1, o, h2) - 104.5) < 1e-6 for o, h1, h2 in y.su))
    if iyon == "Na":
        denet("Na+ çevresi · her suda O iyona H'lerden yakın (O ucu içe dönük); Na–O 2,40 Å",
              all(y.uzaklik(m, o) < min(y.uzaklik(m, h1), y.uzaklik(m, h2)) and abs(y.uzaklik(m, o) - 2.40) < 1e-9 for o, h1, h2 in y.su))
    else:
        denet("Cl− çevresi · her suda bir H iyona O'dan yakın (H ucu içe dönük), Cl···H–O doğrusal; Cl–O 3,20 Å",
              all(y.uzaklik(m, h1) < y.uzaklik(m, o) and abs(y.aci(m, h1, o) - 180) < 1e-6 and abs(y.uzaklik(m, o) - 3.20) < 1e-9 for o, h1, h2 in y.su))
sayfada("çevresi: O uçları içe dönük")
sayfada("çevresi: H uçları içe dönük")

# ================================================================== 5. stereo ölçüleri
bolum("5 · Stereo ölçüleri (her anaglif için)")
denet("K_ORTO = göz aralığı / (2 · okuma uzaklığı) = 62 / 750 = 0,0827", abs(UB.K_ORTO - 62 / 750) < 1e-12 and 350 <= UB.OKUMA_MM <= 400, f"{UB.K_ORTO:.4f}")
denet("ayrıklık üst sınırı 3,0 mm = 375 mm'den 27,5 açı dakikası (≤ 1°)", math.degrees(math.atan(UB.AYRIKLIK_UST_MM / UB.OKUMA_MM)) * 60 < 60,
      f"{math.degrees(math.atan(UB.AYRIKLIK_UST_MM / UB.OKUMA_MM)) * 60:.1f}′")
cikma = {}
for ad, (kur, don, (en, yuk), mb, _) in G.YAPILAR.items():
    y = G.yapi(ad)
    b = UB.yerlestir(y, en, yuk, mb)
    lo, hi = y.sinir()
    j = BILGI[ad]
    im = Image.open(os.path.join(KLASOR, "gorsel", f"ana-{ad}.png"))
    a = np.asarray(im)
    ol = b["mm_birim"] / 25.4 * UB.DPI
    yakin = max(range(len(y.kure)), key=lambda i: y.kure[i]["p"][2] + y.kure[i]["r"])
    uzak = min(range(len(y.kure)), key=lambda i: y.kure[i]["p"][2] - y.kure[i]["r"])
    zy, zu = y.kure[yakin]["p"][2], y.kure[uzak]["p"][2]
    kim = [UB.goruntu(y, g, b["k"], ol, b["W"], b["H"], ss=1, harf=False, kimlik=True)[1] for g in (+1, -1)]
    mx = [np.where(k == yakin + 1)[1].mean() for k in kim]
    kosullar = {
        "ölçü JSON ile aynı": abs(b["k"] - j["k"]) < 1e-9 and abs(b["ayriklik_mm"] - j["ayriklik_mm"]) < 1e-9 and abs(b["mm_birim"] - j["mm_birim"]) < 1e-9,
        "k ≤ K_ORTO": b["k"] <= UB.K_ORTO + 5e-6,               # k, JSON için 5 basamağa yuvarlanır
        "toplam ayrıklık ≤ 3,0 mm": b["ayriklik_mm"] <= UB.AYRIKLIK_UST_MM + 1e-6 and abs(b["ayriklik_mm"] - 2 * b["k"] * hi[2] * b["mm_birim"]) < 2e-3,
        "sıfır paralaks düzlemi yapının ortasında": abs(hi[2] + lo[2]) < 1e-9,
        "resim çerçeveye sığıyor": b["tasma_mm"] == 0,
        "300 dpi": a.shape[:2] == (UB.px(yuk), UB.px(en)) and round(im.info["dpi"][0]) == 300,
        "G = B (sağ göz), R ≠ G (sol göz ayrı)": (a[..., 1] == a[..., 2]).all() and (a[..., 0] != a[..., 1]).any(),
        "zemin beyaz": all((a[r, c] == 255).all() for r in (0, -1) for c in (0, -1)),
        "en yakın küre: sol göz resmi sağda (çapraz ayrıklık)": zy > 0 and mx[0] - mx[1] > 0 and abs((mx[0] - mx[1]) - 2 * b["k"] * zy * ol) < .8,
        "en uzak küre: ters işaret": zu < 0,
    }
    cikma[ad] = UB.OKUMA_MM * b["ayriklik_mm"] / (UB.GOZ_ARALIGI_MM + b["ayriklik_mm"])
    denet(f"{ad:7s} k = {b['k']:.4f} · ayrıklık {b['ayriklik_mm']:.2f} mm · derinlik oranı {b['derinlik_orani']:.2f} · en yakın küre kayması {mx[0] - mx[1]:+.1f} px",
          all(kosullar.values()), "; ".join(k for k, v in kosullar.items() if not v))
mol = [cikma[a] for a in ("ch4", "nh3", "h2o", "co2", "bf3")]
denet("moleküller ortak ölçekte: 1 Å = 15 mm → 15 mm / 10⁻⁷ mm = 150 milyon kat", all(BILGI[a]["mm_birim"] == 15 for a in ("ch4", "nh3", "h2o", "co2", "bf3")) and 15 / 1e-7 == 1.5e8)
denet("moleküllerde derinlik gerçek oranında (k/K_ORTO ≥ 0,95)", all(BILGI[a]["derinlik_orani"] >= .95 for a in ("ch4", "nh3", "h2o", "co2", "bf3")))
denet("“öndeki atomlar kâğıttan 1–2 cm dışarı çıkar”: algılanan çıkma = D·p/(e + p)", all(10 <= c <= 20 for c in mol), " ".join(f"{c:.1f}" for c in mol) + " mm")
sayfada("Öndeki atomlar kâğıttan 1–2 cm dışarı çıkar")

# ================================================================== 6. anaglif kanalları ve kâğıttaki renkler
bolum("6 · Anaglif: kanal düzeni, ayrıklığın işareti, kâğıttaki mürekkep")
y = G.yapi("ch4")
s = UB.uret(y, *G.YAPILAR["ch4"][2], G.YAPILAR["ch4"][3])
a = np.asarray(Image.open(os.path.join(KLASOR, "gorsel", "ana-ch4.png")))
denet("ana-ch4.png · R kanalı = SOL göz resmi (yeniden çizimle birebir)", (a[..., 0] == s.sol).all())
denet("ana-ch4.png · G ve B kanalı = SAĞ göz resmi (yeniden çizimle birebir)", (a[..., 1] == s.sag).all() and (a[..., 2] == s.sag).all())
denet("anaglif_birlestir(sol, sag) → [sol, sag, sag]", (UB.anaglif_birlestir(s.sol, s.sag) == np.dstack([s.sol, s.sag, s.sag])).all())
# sentetik sahne: solda YAKIN küre (z = +1), sağda UZAK küre (z = −1)
t = UB.Yapi("deneme")
t.atom("C", (-1.2, 0, 1.0), harf="", r=.5)
t.atom("C", (1.2, 0, -1.0), harf="", r=.5)
k, ol = .06, 80.0
sol, sag = (UB._u8(UB.goruntu(t, g, k, ol, 400, 200)) for g in (+1, -1))
ana = UB.anaglif_birlestir(sol, sag).astype(int)
mur = lambda kanal, x0, x1: (np.arange(x0, x1) * (255 - ana[:, x0:x1, kanal]).sum(axis=0)).sum() / (255 - ana[:, x0:x1, kanal]).sum()
fy, fu = mur(0, 0, 200) - mur(1, 0, 200), mur(0, 200, 400) - mur(1, 200, 400)
denet("yakın küre: sol göz resmi (R) sağ göz resminin (G) SAĞINDA, fark = 2·k·z·ölçek", abs(fy - 2 * k * 1.0 * ol) < .3, f"{fy:+.2f} px (beklenen {2 * k * ol:+.2f})")
denet("uzak küre: sol göz resmi sağ göz resminin SOLUNDA", abs(fu + 2 * k * 1.0 * ol) < .3, f"{fu:+.2f} px")
yal_sol = (ana[..., 0] < 150) & (ana[..., 1] == 255)          # yalnız sol göz resminde mürekkep
yal_sag = (ana[..., 1] < 150) & (ana[..., 0] == 255)
denet("kâğıtta: yalnız SOL göz resminin olduğu yer CAMGÖBEĞİ (R düşük, G = B = 255)", yal_sol[:, :200].sum() > 50 and (ana[yal_sol][:, 2] == 255).all())
denet("kâğıtta: yalnız SAĞ göz resminin olduğu yer KIRMIZI (R = 255, G = B düşük)", yal_sag[:, :200].sum() > 50 and (ana[yal_sag][:, 2] < 150).all())
denet("yakın kürede camgöbeği saçak sağda, kırmızı saçak solda (kâğıttan dışarı çıkar)", np.where(yal_sol[:, :200])[1].mean() > np.where(yal_sag[:, :200])[1].mean())
denet("uzak kürede tersi (kâğıdın arkasına gider)", np.where(yal_sol[:, 200:])[1].mean() < np.where(yal_sag[:, 200:])[1].mean())
# kırmızı cam (sol göz) R kanalını, camgöbeği cam (sağ göz) G/B kanalını geçirir: her göz yalnız kendi resmini koyu görür
denet("kırmızı camdan (R kanalı) bakınca sağ göz resmi görünmez: R kanalı = yalnız sol resim", (ana[..., 0] == sol).all() and (ana[..., 1] == sag).all())
# gerçek resimde (CH4) en öndeki H: camgöbeği saçağın ağırlık merkezi kırmızınınkinin sağında
ych = G.yapi("ch4")
b = BILGI["ch4"]
ol = b["mm_birim"] / 25.4 * UB.DPI
n = max(range(len(ych.kure)), key=lambda i: ych.kure[i]["p"][2])
cx, cy, rp = b["W"] / 2 + ych.kure[n]["p"][0] * ol, b["H"] / 2 - ych.kure[n]["p"][1] * ol, ych.kure[n]["r"] * ol
pen = a[int(cy - rp):int(cy + rp), int(cx - rp * 1.7):int(cx + rp * 1.7)].astype(int)
cyan, kirm = (pen[..., 1] - pen[..., 0] > 60), (pen[..., 0] - pen[..., 1] > 60)
denet("ana-ch4.png · en öndeki H atomunda camgöbeği saçak sağda, kırmızı saçak solda", np.where(cyan)[1].mean() > np.where(kirm)[1].mean() + 5,
      f"camgöbeği x̄ = {np.where(cyan)[1].mean():.0f}, kırmızı x̄ = {np.where(kirm)[1].mean():.0f}")

# ================================================================== 7. gözlük sayfası
bolum("7 · Gözlük sayfası: test desenleri, şema, şablon ölçüleri")
ty = np.asarray(Image.open(os.path.join(KLASOR, "gorsel", "test-yazi.png"))).astype(int)
w = ty.shape[1] // 2
denet("test 1 · SOL yazısı yalnız R kanalında (kâğıtta camgöbeği): kırmızı camdan koyu, camgöbeği camdan görünmez",
      ty[:, :w, 0].min() < 80 and (ty[:, :w, 1] == 255).all() and (ty[:, :w, 2] == 255).all())
denet("test 1 · SAĞ yazısı yalnız G/B kanalında (kâğıtta kırmızı): camgöbeği camdan koyu, kırmızı camdan görünmez",
      ty[:, w:, 1].min() < 80 and (ty[:, w:, 0] == 255).all() and (ty[:, w:, 1] == ty[:, w:, 2]).all())
td = np.asarray(Image.open(os.path.join(KLASOR, "gorsel", "test-derinlik.png"))).astype(int)
w = td.shape[1] // 2
ic = slice(30, td.shape[0] - 30)                                  # çerçeve çizgisi dışarıda kalsın
mk = lambda kanal, x0, x1: (np.arange(x0, x1) * (255 - td[ic, x0:x1, kanal]).sum(axis=0)).sum() / (255 - td[ic, x0:x1, kanal]).sum()
fa, fb = mk(0, 20, w) - mk(1, 20, w), mk(0, w, td.shape[1] - 20) - mk(1, w, td.shape[1] - 20)
beklenen = UB.px(G.TEST_AYRIKLIK_MM)
denet(f"test 2 · A dairesi çapraz ayrıklıkta (+{tr(G.TEST_AYRIKLIK_MM)} mm): kâğıdın ÖNÜNDE", abs(fa - beklenen) < 1.5, f"{fa:+.1f} px (beklenen {beklenen:+d})")
denet(f"test 2 · B dairesi ters ayrıklıkta (−{tr(G.TEST_AYRIKLIK_MM)} mm): kâğıdın ARKASINDA", abs(fb + beklenen) < 1.5, f"{fb:+.1f} px")
denet("test 2 · çerçeve sıfır ayrıklıkta (kâğıt düzlemi)", (td[2:8, :, 0] == td[2:8, :, 1]).all() and td[4, w, 0] < 200)
sayfada("yalnız <b>SOL</b> yazısı koyu görünmeli")
sayfada("<b>A</b> önde, <b>B</b> arkada durmalı")
S = SU.SEMA
denet("şema · sol gözün resmi (camgöbeği baskı) sağda, sağ gözünki (kırmızı) solda → bakış doğruları kâğıdın önünde kesişir",
      S["camgobegi_baski"][0] > S["kirmizi_baski"][0] and S["sol_goz"][0] < S["sag_goz"][0])
sab = SU.gozluk_sablonu("x")
css = open(os.path.join(BURA, "uc_boyut.css"), encoding="utf-8").read()
denet("şablon gerçek ölçüde: viewBox 1880 × 800 birim, 188 mm × 80 mm basılır (1 birim = 0,1 mm)", 'viewBox="0 0 1880 800"' in sab and "width: 188mm; height: 80mm" in css)
denet("şablon · ön parça 154 mm (136 mm çerçeve + 2 × 9 mm kulak)", "M0 10 H1540" in sab and "M90 10 V370" in sab and "M1450 10 V370" in sab)
pen = [int(v) for v in re.findall(r'<rect x="(\d+)" y="70" width="440" height="270" rx="60" fill="#', sab)]
denet("şablon · pencereler 44 × 27 mm, merkezleri 62 mm aralı (= göz aralığı), arada 18 mm köprü",
      len(pen) == 2 and (pen[1] + 220) - (pen[0] + 220) == 620 == UB.GOZ_ARALIGI_MM * 10 and pen[1] - (pen[0] + 440) == 180, str(pen))
denet("şablon · iç yüzde SOL pencere kırmızı, SAĞ pencere camgöbeği", sab.index("SOL GÖZ") < sab.index("SAĞ GÖZ") and sab.index(">KIRMIZI<") < sab.index(">CAMGÖBEĞİ<")
      and sab.index(SU.KIR_A) < sab.index(SU.CAM_A))
denet("şablon · saplar 125 mm, ölçü çizgisi tam 50 mm", sab.count("H1100 Q1250") == 2 and "M30 462 H1100" in sab and "M1350 600 H1850" in sab)
for m in ("ön parça 15,4 cm", "saplar 12,5 cm", "bu çizgi tam 5 cm"):
    denet(f"şablonda yazıyor: “{m}”", m in sab)
denet("Pamuk bize bakıyor: kırmızı cam Pamuk'un SOL gözünde, yani resimde sağda", SU.pamuk_gozluklu(0, 0, 84).index(SU.CAM) < SU.pamuk_gozluklu(0, 0, 84).index(SU.KIR))
denet("banttaki gözlük takanın gözünden: kırmızı solda", SU.gozluk(0, 0, 150).index(SU.KIR) < SU.gozluk(0, 0, 150).index(SU.CAM))
sayfada("Gözlerinin arası yaklaşık 6 cm", "gözler arası yaklaşık 6 cm (motorda 62 mm)")
sayfada("Kitap <b>30–40 cm</b> uzakta", "kitap 30–40 cm uzakta (motorda 375 mm)")
sayfada("Sol gözün resmi camgöbeği, sağ gözün resmi kırmızı mürekkeple basılır")
sayfada("Kırmızı cam <b>sol</b> göze, camgöbeği (mavi-yeşil) cam <b>sağ</b> göze")

# ================================================================== 8. dosyalar ve baskı kuralları
bolum("8 · Dosyalar ve baskı kuralları")
yasak = "→↓↑δαΔΣ↔✓★⁺⁻∛∠"
svgler = SU.bant_tuzgolu() + SU.bant_mardin() + SU.bant_atolye() + SU.duz_metan("x") + SU.dipol_oklari("x") + SU.nasil_calisir("x") + sab + "".join(SU.ub_ikon("x", a) for a in SU.IKON)
kaynaklar = re.sub(r"<!--.*?-->", "", SABLON, flags=re.S) + svgler               # basılan metin: şablon (yorumlar hariç) + yeni çizimler
denet("şablonda ve çizimlerde fontlarda olmayan simge yok (→ ↓ ↑ δ α Δ Σ ↔ ✓ ★ ⁺ ⁻ ∛)", not any(c in kaynaklar for c in yasak), "".join(c for c in yasak if c in kaynaklar))
denet("uc_boyut.css · CSS filter yok", not re.search(r"(?<![\w-])filter\s*:", css))
denet("yeni çizimlerde konturlu (stroke) SVG yazısı yok", not re.search(r"<text[^>]*\sstroke=", svgler))
denet("büyük harfe çevrilen etikette NaCl korunuyor (.kf)", '<span class="kf">NaCl</span>' in SABLON and ".kf { text-transform: none" in css)
for sinif, adlar in ((9, ["ch4", "nh3", "h2o", "co2", "bf3", "nacl", "elmas", "grafit", "buz"]), (10, ["gaz", "kup", "hid-na", "hid-cl"])):
    yol = os.path.join(KLASOR, f"uc-boyut-{sinif}.html")
    if not os.path.exists(yol):
        denet(f"uc-boyut-{sinif}.html var (önce python3 uretec/kur.py)", False)
        continue
    html = open(yol, encoding="utf-8").read()
    tam = all(f'src="gorsel/ana-{a}.png"' in html and f'style="width:{BILGI[a]["en_mm"]}mm;height:{BILGI[a]["yuk_mm"]}mm"' in html and f'src="gorsel/duz-{a}.png"' in html for a in adlar)
    denet(f"uc-boyut-{sinif}.html · {len(adlar)} anaglif basılı boyutunda (mm) ve yanında düz resmi", tam)
    denet(f"uc-boyut-{sinif}.html · palet {'cini-toprak' if sinif == 9 else 'gol-rasathane'}", f'data-tema="{"cini-toprak" if sinif == 9 else "gol-rasathane"}"' in html)
    denet(f"uc-boyut-{sinif}.html · gözlük camı renkleri palet eşlemesinden etkilenmemiş", sinif == 10 or (SU.KIR in html and SU.CAM in html))
pdf = os.path.join(KLASOR, "uc-boyut-ornek.pdf")
if os.path.exists(pdf):
    from pypdf import PdfReader
    r = PdfReader(pdf)
    kutu = [(float(p.mediabox.width), float(p.mediabox.height)) for p in r.pages]
    denet("uc-boyut-ornek.pdf · 4 sayfa, A4", len(r.pages) == 4 and all(abs(w - 595.3) < 1.5 and abs(h - 841.9) < 1.5 for w, h in kutu), str(kutu[0]))
    fontlar = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
    denet("uc-boyut-ornek.pdf · Type 3 font: 0", fontlar.count("Type 3") == 0 and "TrueType" in fontlar)
    metin = [p.extract_text() for p in r.pages]
    denet("PDF sayfa sırası: molekül · kristal · 10. sınıf · gözlük", "gerçek şekli" in metin[0] and "içine gir" in metin[1] and "üç boyutta" in metin[2] and "hazırla" in metin[3])
    denet("PDF ≤ 25 MB", os.path.getsize(pdf) < 25e6, f"{os.path.getsize(pdf) / 1048576:.2f} MB")
    gomulu = [np.asarray(im.image.convert("RGB")) for p in r.pages for im in p.images]
    adlar = [f"ana-{a}" for a in G.YAPILAR] + ["test-yazi", "test-derinlik"]
    eksik = []
    for a in adlar:
        k = np.asarray(Image.open(os.path.join(KLASOR, "gorsel", a + ".png")))
        if not any(g.shape == k.shape and (g == k).all() for g in gomulu):
            eksik.append(a)
    denet(f"PDF'e gömülü {len(adlar)} anaglif PNG ile birebir aynı (kayıpsız; kanallar bozulmamış)", not eksik, " ".join(eksik))
else:
    denet("uc-boyut-ornek.pdf var (önce python3 uretec/kur.py)", False)
for ad in G.SALLANAN:
    g = Image.open(os.path.join(KLASOR, "onizleme", f"sallanan-{ad}.gif"))
    denet(f"sallanan-{ad}.gif · 2 kare (sol, sağ göz), kare başına 140 ms ≈ 7 kare/sn", g.n_frames == 2 and g.info.get("duration") == 140, f"{os.path.getsize(g.filename) / 1024:.0f} KB")
for ad in ("iki-goz.png", "s01.png", "s02.png", "s03.png", "s04.png"):
    denet(f"onizleme/{ad} var", os.path.exists(os.path.join(KLASOR, "onizleme", ad)))

print(f"\n{SAY[0]} denetim · {len(HATA)} hata")
if HATA:
    print("HATALAR:\n  " + "\n  ".join(HATA))
    sys.exit(1)
print("SONUÇ: hepsi doğru")
