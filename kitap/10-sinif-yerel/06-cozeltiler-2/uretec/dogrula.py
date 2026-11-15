#!/usr/bin/env python3
"""Derişim Birimleri · Göller Yolu — sayısal doğrulama ve cevap anahtarı denetimi.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Her görev, tuzak, hızlı görev, kıssa, meclis, merdiven, imtihan ve Üstad sorusu burada YENİDEN hesaplanır.
  2. Her çoktan seçmeli soruda TEK doğru şık (tek_sik); İmtihan ve Üstad'da A–E her harf en az bir kez.
  3. Sayfadan (unite.html) okunan data-dogru işaretleri, Cevaplar ızgarası, meclis hükümleri, çözüm satırları ve
     CEVABIN kutuları hesapla karşılaştırılır.
  4. Akçe muhasebesi: durak sayfalarındaki akçe çipleri sayfadan okunup toplanır (toplam 1400), HUD çubuğu.
Yardımcılar: yerel-ortak/dogrula_ortak.py.
"""
import importlib.util
import json
import os
import re
import sys


def _ortak():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


ORTAK = _ortak()
sys.path.insert(0, ORTAK)
from dogrula_ortak import *  # noqa: E402,F401,F403

URETEC = os.path.dirname(os.path.abspath(__file__))
KD, KK = 1.86, 0.52                       # 1 kg sudaki 1 mol taneciğin donma alçalması / kaynama yükselmesi (°C)
TANECIK = {"C6H12O6": 1, "sakaroz": 1, "NaCl": 2, "KCl": 2, "KNO3": 2, "CaCl2": 3, "MgCl2": 3, "Na2SO4": 3,
           "AlCl3": 4, "Al(NO3)3": 4, "Al2(SO4)3": 5, "Ca(NO3)2": 3}


def r2(x):
    return round(x + 1e-12, 2)


# ------------------------------------------------------------------ 1. DURAK · derişim ve yüzde (s.2)
kontrol("Görev 1: %15'lik 300 g salamura → 45 g tuz + 255 g su", yakin(300 * .15, 45) and yakin(300 - 45, 255) and yakin(45 / 300 * 100, 15))
kontrol("Görev 2: 80 derece, 250 mL kolonya → 200 mL etil alkol", yakin(250 * 80 / 100, 200))
kontrol("Hızlı 1: 40 g şeker + 160 g su → %20 (payda çözelti)", yakin(40 / (40 + 160) * 100, 20) and not yakin(40 / 160 * 100, 20))

# ------------------------------------------------------------------ 2. DURAK · ppm (s.3)
kontrol("Gül yağı: 3–4 ton gülden 1 kg (TÜRKPATENT) → 250–333 ppm; Pamuk 3500 kg → ≈ 286 ppm",
        round(1 / 3500 * 1e6) == 286 and yakin(1 / 4000 * 1e6, 250) and round(1 / 3000 * 1e6) == 333)
kontrol("Görev 3: 0,32 g = 320 mg Ca²⁺ / 4 L = 80 mg/L ≈ 80 ppm", yakin(.32 * 1000 / 4, 80))
kontrol("Görev 4: 0,8 kg / 3200 kg · 10⁶ = 250 ppm = %0,025 (oran 4000 kg/kg, 3–4 ton aralığında)",
        yakin(.8 / 3200 * 1e6, 250) and yakin(250 / 1e4, .025) and 3000 <= 3200 / .8 <= 4000)
kontrol("ppm ızgarası: %1 = 10 000 ppm → ÷100 = 100 ppm → ÷100 = 1 ppm", yakin(1e4 / 100, 100) and yakin(100 / 100, 1))
kontrol("Hızlı 2: 0,15 mg / 2,5 L = 0,06 ppm > 0,01 (6 katı) → aşıyor", yakin(.15 / 2.5, .06) and .06 > .01 and yakin(.06 / .01, 6))

# ------------------------------------------------------------------ 3. DURAK · molarite ve iyon derişimi (s.4)
kontrol("Görev 5: Na2SO4 = 142; 14,2/142 = 0,1 mol; 0,1/0,5 = 0,2 M", mk("Na2SO4") == 142 and yakin(14.2 / 142 / .5, .2))
kontrol("Görev 6: 0,2 M Na2SO4 → [Na⁺] 0,4 · [SO4²⁻] 0,2 · toplam 0,6 M", yakin(2 * .2, .4) and yakin(.2, .2) and yakin(3 * .2, .6))
kontrol("Görev 7: %40 NaOH, d 1,43 → 1430·0,40 = 572 g → 14,3 M = 10·d·%/M_A",
        mk("NaOH") == 40 and yakin(1430 * .4, 572) and yakin(572 / 40, 14.3) and yakin(10 * 1.43 * 40 / 40, 14.3))
kontrol("Hızlı 3: 0,25 M · 0,4 L = 0,1 mol MgSO4 · 120 = 12 g", mk("MgSO4") == 120 and yakin(.25 * .4 * 120, 12))
kontrol("Pamuk: 1 Na2SO4 → 3 iyon", TANECIK["Na2SO4"] == 3)

# ------------------------------------------------------------------ 4. DURAK · seyreltme, deriştirme, karıştırma (s.5)
kontrol("Görev 8: 0,8·150 = M₂·600 → 0,2 M; eklenen su 450 mL", yakin(.8 * 150 / 600, .2) and 600 - 150 == 450)
kontrol("Görev 9: 0,3·500 = 0,75·V₂ → 200 mL; buharlaşan 300 mL", yakin(.3 * 500 / .75, 200) and 500 - 200 == 300)
kontrol("Görev 10: (0,5·0,2 + 0,2·0,3)/0,5 = 0,32 M", yakin((.5 * .2 + .2 * .3) / .5, .32))
kontrol("Tuzak 4: 0,6 M ve 0,2 M yalnız eşit hacimde 0,4 M (300 mL + 100 mL → 0,5 M)",
        yakin((.6 * .1 + .2 * .1) / .2, .4) and not yakin((.6 * .3 + .2 * .1) / .4, .4))
kontrol("Hızlı 4: 0,4·250 = M₂·1000 → 0,1 M", yakin(.4 * 250 / 1000, .1))
kontrol("Pamuk: eşit hacim su → derişim yarıya", yakin(1 / 2, .5))

# ------------------------------------------------------------------ 5. DURAK · koligatif (s.6)
kontrol("Termometreler: 1 mol/kg glikoz −1,86 · NaCl −3,72 · CaCl2 −5,58 °C",
        [r2(KD * TANECIK[m]) for m in ("C6H12O6", "NaCl", "CaCl2")] == [1.86, 3.72, 5.58])
n11 = 117 / mk("NaCl")
kontrol(f"Görev 11: 117/58,5 = {n11} mol → 4 mol tanecik; −7,44 °C · 102,08 °C",
        yakin(n11, 2) and yakin(KD * 4, 7.44) and yakin(100 + KK * 4, 102.08))
g12 = {"I": .4 * 1, "II": .15 * 3, "III": .25 * 2}
kontrol(f"Görev 12: tanecik {g12} → donma sıcaklığı I > II > III", -KD * g12["I"] > -KD * g12["II"] > -KD * g12["III"])
kontrol("Hızlı 5: 0,1 mol Al2(SO4)3 → 0,5 mol tanecik → −0,93 °C", yakin(.1 * 5, .5) and yakin(KD * .5, .93))
kontrol("Tanecik sayacı: formüllerden iyon sayısı", all(TANECIK[k] == v for k, v in
        {"NaCl": 2, "KNO3": 2, "CaCl2": 3, "MgCl2": 3, "Na2SO4": 3, "AlCl3": 4, "Al(NO3)3": 4, "Al2(SO4)3": 5}.items()))

# ------------------------------------------------------------------ MECLİS (s.8)
kontrol("Meclis 1: 24/(24+136) = %15 (hatalı 24/136 ≈ %17,6)", yakin(24 / 160 * 100, 15) and r2(24 / 136 * 100) == 17.65)
kontrol("Meclis 2: 11,7/58,5 = 0,2 mol; 0,2/0,25 = 0,8 M (hatalı 0,2/250 = 8·10⁻⁴)",
        yakin(11.7 / mk("NaCl"), .2) and yakin(.2 / .25, .8) and yakin(.2 / 250, 8e-4))
kontrol("Meclis 3: 1,2·250/600 = 0,5 M (hatalı 1,2·250/350 ≈ 0,86)", yakin(1.2 * 250 / 600, .5) and r2(1.2 * 250 / 350) == .86)
kontrol("Meclis 4: KCl 0,4 > sakaroz 0,2 mol tanecik → KCl daha düşük sıcaklıkta donar", .2 * TANECIK["KCl"] > .2 * TANECIK["sakaroz"])
MECLIS = {"M1": ("Yusuf", 1), "M2": ("Pamuk", 2), "M3": ("Elif", 2), "M4": ("Yusuf", 3)}

# ------------------------------------------------------------------ KISSALAR (s.9)
anahtar = {}
d = yargi({"I": yakin(5 / 100 * 1000, 50), "II": r2(50 / mk("C6H12O6")) == .28, "III": yakin(.5 * 50 / mk("C6H12O6"), .5)})
anahtar["K1"] = tek_sik("Kıssa 1 (glikoz serumu)", YARGI_5, lambda v: v == d, "C")
k2 = {"P": 180 / 2, "R": 650 / 5, "S": 40 / .5, "T": 440 / 4}
sert = {k for k, v in k2.items() if v > 100}
kontrol(f"Kıssa 2: mg/L {k2} → sert {sorted(sert)}", k2 == {"P": 90, "R": 130, "S": 80, "T": 110})
anahtar["K2"] = tek_sik("Kıssa 2 (sertlik)", {"A": {"P", "R"}, "B": {"R", "S"}, "C": {"R"}, "D": {"R", "T"}, "E": {"S", "T"}}, lambda v: v == sert, "D")
olcum = {"X": -2.79, "Y": -.93, "Z": -1.86}


def k3(uclu):
    return all(yakin(-KD * .5 * TANECIK[m], olcum[h]) for m, h in zip(uclu, "XYZ"))


anahtar["K3"] = tek_sik("Kıssa 3 (donma grafiği)", {"A": ("NaCl", "C6H12O6", "CaCl2"), "B": ("CaCl2", "NaCl", "C6H12O6"), "C": ("C6H12O6", "NaCl", "CaCl2"),
                                                   "D": ("AlCl3", "C6H12O6", "NaCl"), "E": ("CaCl2", "C6H12O6", "NaCl")}, k3, "E")
m4 = (.05 * 200 + .01 * 800) / 1000
no3 = 2 * m4
kontrol(f"Kıssa 4: Ca(NO3)2 {m4} M → NO3⁻ {no3} M, hedef 0,030–0,040", yakin(m4, .018) and yakin(no3, .036) and .030 <= no3 <= .040)
anahtar["K4"] = tek_sik("Kıssa 4 (gübre tankı)", {"A": (.018, "alt"), "B": (.036, "icinde"), "C": (.060, "ust"), "D": (.030, "sinir"), "E": (.072, "ust")},
                        lambda v: yakin(v[0], no3) and v[1] == "icinde", "B")

# ------------------------------------------------------------------ ANAHTAR MERDİVENİ (s.10)
kontrol("Merdiven 1: %98 H2SO4, d 1,84 → 1840·0,98 = 1803,2 g = 18,4 mol → 18,4 M",
        mk("H2SO4") == 98 and yakin(1840 * .98, 1803.2) and yakin(1803.2 / 98, 18.4) and yakin(10 * 1.84 * 98 / 98, 18.4))
kontrol("Merdiven 2: Cl⁻ 0,2·0,3·2 + 0,3·0,2 = 0,18 mol / 0,5 L = 0,36 M", yakin(.2 * .3 * 2 + .3 * .2, .18) and yakin(.18 / .5, .36))
kontrol("Merdiven 3: 0,1·3 = 0,3 mol/250 g → 1,2 mol/kg; 1,2·180 = 216 g glikoz", yakin(.1 * 3 / .25, 1.2) and yakin(1.2 * mk("C6H12O6"), 216))

# ------------------------------------------------------------------ BÜYÜK İMTİHAN (s.11–12)
T = {}
T[1] = tek_sik("İmtihan 1", dict(A=42, B=300, C=308, D=312, E=338), lambda v: yakin(v, 350 - 350 * .12), "C")
T[2] = tek_sik("İmtihan 2", dict(A=35, B=40, C=45, D=50, E=56), lambda v: yakin(v, 400 * .7 / (400 + 160) * 100), "D")
T[3] = tek_sik("İmtihan 3", dict(A=.03, B=.3, C=1.5, D=3, E=7.5), lambda v: yakin(v, 1.5 / 5), "B")
T[4] = tek_sik("İmtihan 4", dict(A=9, B=14.4, C=36, D=90, E=900), lambda v: yakin(v, 36 * 2.5), "D")
T[5] = tek_sik("İmtihan 5", dict(A=.2, B=.4, C=.8, D=11.2, E=44.8), lambda v: yakin(v, 22.4 / mk("KOH") / 2), "A")
d6 = yargi({"I": yakin(.3 * 2, .6), "II": yakin(.3 * 3, .9), "III": yakin(.3 * 5, 1.2)})
T[6] = tek_sik("İmtihan 6", YARGI_5, lambda v: v == d6, "C")
T[7] = tek_sik("İmtihan 7", dict(A=1.8, B=4.8, C=6, D=7.2, E=72), lambda v: yakin(v, .15 * .4 * mk("MgSO4")), "D")
T[8] = tek_sik("İmtihan 8", dict(A=200, B=400, C=600, D=800, E=1000), lambda v: yakin(v, .9 * 200 / .3 - 200), "B")
T[9] = tek_sik("İmtihan 9", dict(A=.175, B=.25, C=.35, D=.5, E=.7), lambda v: yakin(v, (.6 * .15 + .1 * .35) / .5), "B")
# İmtihan 10: dibinde katı varken (doymuş, sabit T) su buharlaşır, katı çöker: derişim = çözünürlük (sabit), çözünen azalır, çökelek artar
d10 = yargi({"I": True, "II": True, "III": True})
T[10] = tek_sik("İmtihan 10", YARGI_5, lambda v: v == d10, "E")
t11 = {"I": -KD * .2 * TANECIK["NaCl"], "II": -KD * .1 * TANECIK["Al(NO3)3"], "III": -KD * .5}
iliski = {"A": lambda t: yakin(t["I"], t["II"]) and t["II"] > t["III"], "B": lambda t: t["I"] > t["II"] > t["III"],
          "C": lambda t: t["III"] > t["I"] and yakin(t["I"], t["II"]), "D": lambda t: t["II"] > t["I"] > t["III"],
          "E": lambda t: yakin(t["I"], t["II"]) and yakin(t["II"], t["III"])}
T[11] = tek_sik("İmtihan 11", iliski, lambda fn: fn(t11), "A")
T[12] = tek_sik("İmtihan 12", dict(A=99.69, B=100.10, C=100.21, D=100.26, E=100.31), lambda v: yakin(v, r2(100 + KK * .2 * TANECIK["CaCl2"])), "E")
dagilim([T[i] for i in range(1, 13)])
DURAK_ETIKET = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 4, 11: 5, 12: 5}

# ------------------------------------------------------------------ ÜSTAD SORULARI (bonus; 1400 akçeye dahil değil)
U = {}
m1 = 10 * 1.2 * 36.5 / mk("HCl")
U[1] = tek_sik("Üstad 1", dict(A=.04, B=.4, C=.6, D=1.2, E=4), lambda v: yakin(v, m1 * 50 / 1500), "B")
iyon = .2 * .1 * TANECIK["Al2(SO4)3"] + .3 * .2 * TANECIK["Na2SO4"]
U[2] = tek_sik("Üstad 2", dict(A=.24, B=.40, C=.48, D=.56, E=.93), lambda v: yakin(v, iyon / (.1 + .2 + .2)), "D")
n3 = .4 * .5
v_doy = n3 / 2.0                                   # 2,0 M'de doyar → 0,1 L kalır → 400 mL buharlaşmış (grafik)
kontrol(f"Üstad 3 grafiği: 0,4 M·0,5 L = {n3} mol; 2,0 M'de V = {v_doy} L → 400 mL'de doyar",
        yakin(v_doy, .1) and yakin((.5 - v_doy) * 1000, 400) and yakin(.2 / (.5 - .2), .2 / .3))
U[3] = tek_sik("Üstad 3", dict(A=10, B=15, C=20, D=30, E=40), lambda v: yakin(v, (n3 - 2.0 * .05) * 100), "A")
tan4 = 1.674 / KD
U[4] = tek_sik("Üstad 4", dict(A=5.85, B=11.7, C=17.55, D=23.4, E=35.1), lambda v: yakin(v, (tan4 - .1 * 3) / 2 * mk("NaCl")), "C")
U[5] = tek_sik("Üstad 5", dict(A=1e-5, B=1e-4, C=1.9e-4, D=1e-3, E=1.9e-3), lambda v: yakin(v, 1.9e-3 / mk("F")), "B")
m6 = (.2 * 400 - .1 * 400) / (.3 - .2)            # 40 + 0,3m = 0,2(400 + m)
kontrol(f"Üstad 6: m = {m6} g; 800 g'da 160 g şeker; %16 için 1000 g", yakin(m6, 400) and yakin(.1 * 400 + .3 * m6, 160))
U[6] = tek_sik("Üstad 6", dict(A=50, B=100, C=150, D=160, E=200), lambda v: yakin(v, 160 / .16 - 800), "E")
dagilim(list(U.values()))

# ------------------------------------------------------------------ meta.json ve kitap zaman şeridi
meta = json.load(open(os.path.join(URETEC, "meta.json"), encoding="utf-8"))
kontrol("meta: 10 benzersiz hazine kartı H1–H10", [h["kod"] for h in meta["hazine"]] == [f"H{i}" for i in range(1, 11)])
kontrol("meta: 5 durak, akçe 100/150/150/150/150, sayfa 2–6", [d_["akce"] for d_ in meta["duraklar"]] == [100, 150, 150, 150, 150]
        and [d_["sayfa"] for d_ in meta["duraklar"]] == [2, 3, 4, 5, 6])
kontrol("meta: 7 nişan (5 durak + kale + bonus Üstad Mührü)", len(meta["nisanlar"]) == 7 and meta["nisanlar"][-1].get("bonus"))
spec = importlib.util.spec_from_file_location("medeniyet", os.path.join(os.path.dirname(ORTAK), "yerel-cerceve", "uretec", "medeniyet.py"))
if spec and os.path.exists(spec.origin):
    med = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(med)
    for m in meta["medeniyet"]:
        kisi = next((k for k in med.KISILER if med.eslesir(k, m["ad"])), None)
        kontrol(f"medeniyet: {m['ad']} kitap zaman şeridindeki katkıyla aynı", bool(kisi) and kisi["katki"] == m["katki"])

# ------------------------------------------------------------------ sayfadan okunanlar (unite.html)
html = sayfa_oku(__file__)
if html:
    beklenen = {f"I{k}": v for k, v in T.items()}
    beklenen.update(anahtar)
    beklenen.update({f"U{k}": v for k, v in U.items()})
    sayfa_isaretleri_ayni(html, beklenen)
    izgara = anahtar_izgarasi(html)
    kontrol(f"Cevaplar ızgarası hesapla aynı {izgara}", izgara == T)
    etiket = dict((int(n), int(e)) for n, e in re.findall(r"<i>(\d+)</i><b>[A-E]</b><small>(\d)\. durak</small>", html))
    kontrol("Cevaplar ızgarasındaki durak etiketleri", etiket == DURAK_ETIKET)
    for no, h in T.items():
        kontrol(f"Cevaplar: '{no} · {h}' çözümü var", f"<b>{no} · {h}</b>" in html)
    for i in range(1, 5):
        kontrol(f"Cevaplar: kıssa '{i} · {anahtar[f'K{i}']}' çözümü var", f"<b>{i} · {anahtar[f'K{i}']}</b>" in html)
    for k, h in U.items():
        kontrol(f"Cevaplar: Üstad 'Ü{k} · {h}' çözümü var", f"<b>Ü{k} · {h}</b>" in html)
    satir = lambda ad: re.search(rf"<p><b>{ad}</b>(.*?)</p>", html)
    kontrol("hızlı anahtar: Kıssa satırı", re.findall(r'<span class="ck">(\d) ([A-E])</span>', satir("Kıssa").group(1)) == [(str(i), anahtar[f"K{i}"]) for i in range(1, 5)])
    kontrol("hızlı anahtar: Üstad satırı", re.findall(r'<span class="ck">(\d) ([A-E])</span>', satir("Üstad").group(1)) == [(str(k), h) for k, h in U.items()])
    kontrol("hızlı anahtar: Meclis satırı", re.findall(r'<span class="ck">\d (\w+)</span>', satir("Meclis").group(1)) == [v[0] for v in MECLIS.values()])
    kontrol(f"meclis hükümleri {meclis_hukumleri(html)}", meclis_hukumleri(html) == MECLIS)
    for kod, (kisi, s_) in MECLIS.items():
        kontrol(f"Cevaplar: meclis {kod[1]} · {kisi} · satır {s_}", f"<b>{kod[1]} · {kisi}</b> Satır {s_}:" in html)
    ogr = ogretmen_metinleri(html)
    kontrol(f"öğretmen metinleri {len(ogr)} = 5 CEVABIN + 8 meclis + 4 kıssa + 9 merdiven + 12 imtihan + 6 Üstad = 44", len(ogr) == 44)
    ciftler = re.findall(r'CEVABIN:<span class="ogr">(.*?)</span></div><span class="ters-cevap"><span class="ters">(?:Cevap: )?(.*?)</span></span>', html)
    kontrol(f"CEVABIN (kırmızı) = ters yazılı cevap ({len(ciftler)} kutu)", len(ciftler) == 5 and all(a == b for a, b in ciftler))
    kontrol("hızlı cevaplar: %20 · Aşıyor: 0,06 ppm · 12 g · 0,1 M · 0,5 mol · −0,93 °C",
            [a for a, _ in ciftler] == ["%20", "Aşıyor: 0,06 ppm", "12 g", "0,1 M", "0,5 mol · −0,93 °C"])
    kontrol("Üstad sayfası: 6 kart, Üstad Mührü nişanı", html.count('class="ustad-soru"') == 6 and "Üstad Mührü" in html)
    for metin in ("Kütlece %15’lik 300 g salamura", "3200 kg taze gülden 0,8 kg gül yağı", "14,2 g Na<sub>2</sub>SO<sub>4</sub> ile 500 mL",
                  "1 kg suda 117 g NaCl", "%98 H<sub>2</sub>SO<sub>4</sub>, yoğunluk 1,84 g/mL", "−1,674 °C", "1,9 ppm", "3–4 ton"):
        kontrol(f"sayfada '{metin}' var", metin in html)

    # akçe: durak sayfalarındaki çipler sayfadan okunur (levha hariç) + hazine kartı başına 10
    bolum = {int(n): b for n, b in re.findall(r'<section class="sayfa s(\d+)[^"]*">(.*?)</section>', html, re.S)}
    durak_akce = []
    for no in range(2, 7):
        ana = bolum[no].split('<main class="ic"', 1)[1]
        cipler = [int(x) for x in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', ana)]
        kart = ana.count('<div class="hazine')
        durak_akce.append(sum(cipler) + 10 * kart)
    kontrol(f"durak sayfaları akçe (çipler + kart×10) {durak_akce} = meta", durak_akce == [d_["akce"] for d_ in meta["duraklar"]])
    say = lambda no, kalip: len(re.findall(kalip, bolum[no].split('<main class="ic"', 1)[1]))
    yan = dict(hulasa=40 if "6 satır = +40 akçe" in bolum[7] else 0, meclis=30 * say(8, r'<span class="cip akce">\+30</span>'),
               kissa=30 * say(9, r'<span class="cip akce">\+30</span>'), anahtar=40 * say(10, r'<span class="no">\d</span>'),
               imtihan=25 * (say(11, r'<span class="cip akce">\+25</span>') + say(12, r'<span class="cip akce">\+25</span>')))
    toplam = sum(durak_akce) + sum(yan.values())
    kontrol(f"yan yollar ve imtihan {yan}; ünite toplamı {toplam} = 1400", yan == dict(hulasa=40, meclis=120, kissa=120, anahtar=120, imtihan=300) and toplam == 1400)
    kur = open(os.path.join(URETEC, "kur.py"), encoding="utf-8").read()
    bar = [int(b) for b in re.findall(r"^\s+\d+: \('.*?', '.*?', (\d+)\),", kur, re.M)]
    birikim = [0, 0, 100, 250, 400, 550, 700, 740, 860, 980, 1100, 1250, 1400, 1400, 1400]
    kontrol(f"HUD akçe çubuğu {bar}", bar == [round(b / 1400 * 100) for b in birikim])
    kontrol("Ahilik eşikleri 400 / 800 / 1150 (%28,57 · %57,14 · %82,14)",
            [round(x / 1400 * 100, 2) for x in (400, 800, 1150)] == [28.57, 57.14, 82.14] and "1150–1400 akçe" in html and "400–799 akçe" in html)

print("\nCEVAP ANAHTARI · İmtihan:", " ".join(f"{k}{v}" for k, v in T.items()), "· Kıssa:", " ".join(f"{k}{v}" for k, v in anahtar.items()),
      "· Üstad:", " ".join(f"Ü{k}{v}" for k, v in U.items()))
D.sonuc()
