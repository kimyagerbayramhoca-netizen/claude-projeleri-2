"""Mol Kavramı (yerel · Van Gölü turu) — bütün sayısal cevapların ve cevap anahtarının doğrulaması.

Çalıştır:  python3 uretec/dogrula.py
  1. Her görev, tuzak, hızlı görev, kıssa, meclis, anahtar merdiveni ve imtihan sorusu yeniden hesaplanır.
  2. Her çoktan seçmeli soruda TEK doğru şık olduğu denetlenir.
  3. unite.html içindeki cevap anahtarı (s.13) ve şık metinleri sayfadan okunup hesapla karşılaştırılır.
  4. Akçe muhasebesi: durak toplamları ve ünite toplamı (1400).
  5. Üstad soruları (bonus) ve sayfadaki öğretmen işaretleri (data-dogru, meclis hükmü, .ogr) hesapla aynı mı?
Sonunda "SONUÇ: hepsi doğru" yazmalı. Yardımcılar: yerel-ortak/dogrula_ortak.py
"""
import os
import re
import sys
from fractions import Fraction as F

BURA = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(os.path.dirname(BURA), "unite.html")


def _ortak():
    d = BURA
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


sys.path.insert(0, _ortak())
from dogrula_ortak import (D, NA, M, mk, yakin, kontrol, tek_sik, yargi, sayfa_isaretleri_ayni,  # noqa: E402,F401
                           meclis_hukumleri, ogretmen_metinleri)
from dogrula_ortak import dagilim as harf_dagilimi  # noqa: E402
import math  # noqa: E402

yargi_kumesi = yargi
YARGI_SIK = {"A": "I", "B": "III", "C": "I,II", "D": "II,III", "E": "I,II,III"}  # kıssa 1
anahtar = {}

# ------------------------------------------------------------------ mol kütleleri (s.5 tablosu)
kontrol("CaCO3 = 100", mk(dict(Ca=1, C=1, O=3)) == 100)
kontrol("Na2CO3 = 106", mk(dict(Na=2, C=1, O=3)) == 106)
kontrol("NaCl = 58,5", yakin(mk(dict(Na=1, Cl=1)), 58.5))
kontrol("Mg(OH)2 = 58", mk(dict(Mg=1, O=2, H=2)) == 58)
kontrol("C6H12O6 = 180", mk(dict(C=6, H=12, O=6)) == 180)
kontrol("SO2 = 64, SO3 = 80, CH4 = 16, C2H6 = 30, C2H4 = 28, C3H8 = 44",
        [mk(dict(S=1, O=2)), mk(dict(S=1, O=3)), mk(dict(C=1, H=4)), mk(dict(C=2, H=6)), mk(dict(C=2, H=4)), mk(dict(C=3, H=8))] == [64, 80, 16, 30, 28, 44])

# ------------------------------------------------------------------ 1. durak · Edremit
yil = NA / (365.25 * 24 * 3600)
kontrol(f"Avogadro: ≈19 katrilyon yıl ({yil:.3g})", 1.85e16 < yil < 1.95e16)
kontrol(f"Avogadro: evren yaşının ≈1,4 milyon katı ({yil / 13.8e9:.3g})", 1.35e6 < yil / 13.8e9 < 1.45e6)
damla_ml = 0.05
gol_km3 = 600
gol_damla = gol_km3 * 1e9 * 1e6 / damla_ml          # km³ → m³ → mL → damla
damla_molekul = damla_ml * 1.0 / 18 * NA            # 0,05 mL su ≈ 0,05 g
kontrol(f"Van Gölü ≈1,2·10^19 damla ({gol_damla:.3g})", 1.15e19 < gol_damla < 1.25e19)
kontrol(f"1 damlada ≈1,7·10^21 molekül ({damla_molekul:.3g})", 1.65e21 < damla_molekul < 1.75e21)
kontrol(f"oran ≈140 kat ({damla_molekul / gol_damla:.0f})", 135 < damla_molekul / gol_damla < 145)
kontrol("1 mol su 18 g ≈ 18 mL; bir yudumda (10 mL) 10^23 mertebesi", 1e23 < 10 / 18 * NA < 1e24)
kontrol("Hızlı görev: 1 mol H2O → 2 mol H", 1 * 2 == 2)

# ------------------------------------------------------------------ 2. durak · Gevaş
kontrol("Görev 1: bor 10·0,20 + 11·0,80 = 10,8", yakin(10 * .2 + 11 * .8, 10.8))
kontrol("Hızlı görev: Cl 35·0,75 + 37·0,25 = 35,5", yakin(35 * .75 + 37 * .25, 35.5))
kontrol("Hızlı kontrol: 14C → 6 p, 8 n", (6, 14 - 6) == (6, 8))
kontrol("Çekirdek çizimleri: 12C/13C/14C = 6p + 6/7/8n", [12 - 6, 13 - 6, 14 - 6] == [6, 7, 8])

# ------------------------------------------------------------------ 3. durak · Tatvan
kontrol("Sohbet: 1 mol Na2CO3 → 2+1+3 = 6 mol atom", 2 + 1 + 3 == 6)
kontrol("Görev 2: 0,5 mol CaCO3 → 3,01e23 birim, 1,5 mol O", yakin(.5 * NA, 3.01e23) and yakin(.5 * 3, 1.5))
kontrol("Görev 3: 3,01e23 CO2 → 0,5 mol → 1 mol O", yakin(3.01e23 / NA, .5) and yakin(3.01e23 / NA * 2, 1))
kontrol("Görev 4: 4,8 mol atom glikoz (24 atom) → 0,2 mol", 6 + 12 + 6 == 24 and yakin(4.8 / 24, .2))
kontrol("Tuzak: 1 mol NaCl → 2 mol iyon = 1,204e24", yakin(2 * NA, 1.204e24))
kontrol("Hızlı görev: 1,204e24 H2O → 2 mol → 4 mol H", yakin(1.204e24 / NA, 2) and yakin(1.204e24 / NA * 2, 4))

# ------------------------------------------------------------------ 4. durak · Ahlat
kontrol("Görev 5A: 0,4 mol CaCO3 = 40 g", yakin(.4 * 100, 40))
kontrol("Görev 5B: 9 g H2O → 0,5 mol, 3,01e23 molekül, 1,5 mol atom", yakin(9 / 18, .5) and yakin(.5 * NA, 3.01e23) and yakin(.5 * 3, 1.5))
kontrol("Görev 6: 6,4 g SO2 → 0,1 mol → 0,2 mol O → 3,2 g (S 3,2 g)", yakin(6.4 / 64 * 2 * 16, 3.2) and yakin(6.4 / 64 * 32, 3.2))
kontrol("Tuzak: CO = N2 = 28 g/mol", mk(dict(C=1, O=1)) == mk(dict(N=2)) == 28)
kontrol("Tuzak: 1 tane H2O = 18/NA g ≈ 2,99e-23 g", abs(18 / NA - 2.99e-23) < .01e-23)
kontrol("Hızlı görev: 0,25 mol CH4 = 4 g, 1 mol H", yakin(.25 * 16, 4) and yakin(.25 * 4, 1))

# ------------------------------------------------------------------ 5. durak · Adilcevaz
x = F(6, 10) / 2  # 4x + 6(0,5 − x) = 2,4
kontrol("Görev 7: x = 0,3 → 10,8 g; H kontrolü 2,4",
        x == F(3, 10) and yakin(float(x * 16 + (F(1, 2) - x) * 30), 10.8) and yakin(float(x * 4 + (F(1, 2) - x) * 6), 2.4))
kontrol("Görev 8: 64 g → O2 2 mol, SO2 1 mol; atom 4/3", 64 / 32 == 2 and 64 / 64 == 1 and F(2 * 2, 1 * 3) == F(4, 3))
kontrol("Hızlı görev: eşit kütle CH4/O2 molekül oranı = 2", F(32, 16) / F(32, 32) == 2)

# ------------------------------------------------------------------ Hülasa kartları
kontrol("Hülasa 05: 16’şar g → CH4 1 mol, O2 0,5 mol", 16 / 16 == 1 and 16 / 32 == .5)

# ------------------------------------------------------------------ Meclis (her paylaşımda tek hata; doğru kişi)
kontrol("Meclis 1 (Ahmet): Na2B4O7 = 2+4+7 = 13 atom → 0,5·13 = 6,5 mol atom; hata satır 2 → Yusuf",
        2 + 4 + 7 == 13 and yakin(.5 * 13, 6.5) and yakin(.5 * 3, 1.5))
kontrol("Meclis 2 (Zehra): CO2 44 → 11/44 = 0,25; 11/28 ≈ 0,39 yuvarlaması doğru → Elif",
        mk(dict(C=1, O=2)) == 44 and yakin(11 / 44, .25) and round(11 / 28, 2) == .39)
kontrol("Meclis 3 (Mehmet Emin): glikoz 180 (satır 1 doğru); 1 tanesi 180/NA ≈ 2,99e-22 g → Yusuf",
        mk(dict(C=6, H=12, O=6)) == 180 and abs(180 / NA - 2.99e-22) < .01e-22)
kontrol("Meclis 4 (Rabia): 16 g CH4 1 mol, O2 0,5 mol → Pamuk", 16 / 16 == 1 and 16 / 32 == .5)

# ------------------------------------------------------------------ Kıssalar
n1 = 10.6 / 106
d1 = yargi_kumesi({"I": yakin(n1, .1), "II": yakin(n1 * NA, 6.02e22), "III": yakin(n1 * 3, .2)})
anahtar["K1"] = tek_sik("Kıssa 1 (soda)", {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == d1, "C")
nb = 2.16 / 10.8 * NA
anahtar["K2"] = tek_sik("Kıssa 2 (bor)", {"A": 6.02e22, "B": 1.204e23, "C": 1.806e23, "D": 2.408e23, "E": 1.204e24}, lambda v: yakin(v, nb), "B")
MX, MY = 12 / .5, 16 / .5
d3 = yargi_kumesi({"I": MX == 24, "II": F(int(MY), int(MX)) == F(4, 3), "III": MY - MX == 8})
anahtar["K3"] = tek_sik("Kıssa 3 (grafik)", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == d3, "E")
I_ = 5 / 100 * 5            # CaCO3: 5 atom/birim
II_ = 1.204e23 / NA * 3     # H2O: 3 atom
III_ = .02 * 24             # glikoz: 24 atom
kontrol(f"Kıssa 4 atom molleri: I {I_:.2f}, II {II_:.2f}, III {III_:.2f}", yakin(I_, .25) and yakin(II_, .6) and yakin(III_, .48))
sira = " > ".join(k for k, _ in sorted({"I": I_, "II": II_, "III": III_}.items(), key=lambda t: -t[1]))
anahtar["K4"] = tek_sik("Kıssa 4 (raf)", {"A": "I > II > III", "B": "III > II > I", "C": "II > I > III", "D": "II > III > I", "E": "I = II > III"},
                        lambda v: v == sira, "D")
kontrol("Kıssa 4: E (I = II > III) yanlış", not yakin(I_, II_))

# ------------------------------------------------------------------ Anahtar merdiveni
kontrol("Merdiven 1: X2O3 0,2 mol 32 g → 160 → X = 56 (Fe)", (32 / .2 - 48) / 2 == 56)
xm = (44 * .4 - 14.4) / (44 - 28)
kontrol("Merdiven 2: x = 0,2 → 0,8 + 1,6 = 2,4 mol H", yakin(xm, .2) and yakin(xm * 4 + (.4 - xm) * 8, 2.4))
kontrol("Merdiven 3: 20 mol atom → 5 mol SO3 (400 g) / 4 mol CH4 (64 g) = 25/4", F(5 * 80, 4 * 16) == F(25, 4))

# ------------------------------------------------------------------ Büyük İmtihan (12 soru)
T = {}
T[1] = tek_sik("İmtihan 1", dict(A=.3, B=1.1, C=2.4, D=3.3, E=3.6), lambda v: yakin(v, .3 * 11), "D")
T[2] = tek_sik("İmtihan 2", dict(A=.5, B=1, C=2, D=4, E=12), lambda v: yakin(v, 1.204e24 / NA), "C")
T[3] = tek_sik("İmtihan 3", dict(A=20.5, B=29, C=41, D=58, E=116), lambda v: yakin(v, .5 * 58), "B")
d4 = yargi_kumesi({"I": yakin(6.4 / 32, .2), "II": yakin(.2 * NA, 1.204e23), "III": yakin(.2 * 2, .4)})
T[4] = tek_sik("İmtihan 4", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == d4, "E")
ciftler = {"A": (dict(C=1, O=1), dict(N=2)), "B": (dict(C=1, O=2), dict(S=1, O=2)), "C": (dict(H=2, O=1), dict(N=1, H=3)),
           "D": (dict(C=1, H=4), dict(O=2)), "E": (dict(N=1, O=1), dict(O=2))}
T[5] = tek_sik("İmtihan 5", ciftler, lambda v: mk(v[0]) == mk(v[1]), "A")
T[6] = tek_sik("İmtihan 6", {"A": 12, "B": 12 * NA, "C": 12 / NA, "D": NA / 12, "E": 1 / 12}, lambda v: yakin(v, 12 / NA), "C")
atom = dict(A=1, B=.5 * 3, C=8 / 16 * 5, D=3.01e23 / NA * 3, E=4.4 / 44 * 3)
T[7] = tek_sik("İmtihan 7", atom, lambda v: v == max(atom.values()), "C")
T[8] = tek_sik("İmtihan 8", dict(A=10, B=20, C=25, D=40, E=80), lambda v: v == 10 / .25, "D")
T[9] = tek_sik("İmtihan 9", dict(A=63.0, B=63.6, C=64.0, D=64.4, E=65.0), lambda v: yakin(v, 63 * .7 + 65 * .3), "B")
# 10: nötr izotoplar — fiziksel özellikler (kütle, yoğunluk) farklıdır; yalnız E yanlış
dogru_ifade = {"A": True, "B": True, "C": True, "D": True, "E": False}
T[10] = tek_sik("İmtihan 10 (yanlış olan)", dogru_ifade, lambda v: not v, "E")
x11 = 1.0 - .7   # x + 2(0,5 − x) = 0,7 → x = 0,3
T[11] = tek_sik("İmtihan 11", dict(A=8.0, B=9.6, C=10.4, D=11.2, E=12.8), lambda v: yakin(v, x11 * 16 + (.5 - x11) * 28), "C")
nch4, nso2 = 64 / 16, 64 / 64
d12 = yargi_kumesi({"I": nch4 / nso2 == 4, "II": nch4 * 5 == nso2 * 3, "III": nch4 * 4 == 8 * nso2 * 2})
T[12] = tek_sik("İmtihan 12", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}, lambda v: v == d12, "D")
dagilim = {k: list(T.values()).count(k) for k in "ABCDE"}
kontrol(f"İmtihan şık dağılımı her harf en az bir kez {dagilim}", all(v >= 1 for v in dagilim.values()))

# ------------------------------------------------------------------ sayfadan okunan anahtar ve şıklar
if os.path.exists(HTML):
    html = open(HTML, encoding="utf-8").read()
    izgara = re.search(r'<div class="anahtar-izgara">(.*?)</div>\s*</div>', html, re.S)
    sayfa_anahtar = dict((int(n), h) for n, h in re.findall(r"<i>(\d+)</i><b>([A-E])</b>", izgara.group(1))) if izgara else {}
    kontrol(f"s.14 anahtar ızgarası hesapla aynı {sayfa_anahtar}", sayfa_anahtar == T)
    for no, harf in T.items():
        kontrol(f"s.14 çözüm satırı '{no} · {harf}' var", f"<b>{no} · {harf}</b>" in html)
    for k, harf in zip(("1", "2", "3", "4"), (anahtar["K1"], anahtar["K2"], anahtar["K3"], anahtar["K4"])):
        kontrol(f"s.14 kıssa çözümü '{k} · {harf}' var", f"<b>{k} · {harf}</b>" in html)
    # her meşveret kartında A–E beş şık
    kartlar = re.findall(r'<div class="oy[^"]*">(.*?)</div></div>\s*</div>', html, re.S)
    harfler = [re.findall(r"<b>([A-E])</b>", k) for k in kartlar]
    kontrol(f"12 meşveret kartı, her birinde A–E ({len(harfler)} kart)", len(harfler) == 12 and all(sorted(h) == list("ABCDE") for h in harfler))
    # kıssa şıkları
    siklar = re.findall(r'<div class="siklar[^"]*">(.*?)</div></div>', html, re.S)
    kontrol(f"4 kıssa + 6 Üstad kartında A–E ({len(siklar)} kart)", len(siklar) == 10 and all(sorted(re.findall(r"<b>([A-E])</b>", k)) == list("ABCDE") for k in siklar))
    # sayfada yazan kritik sayılar
    for metin in ("10,6 g saf Na<sub>2</sub>CO<sub>3</sub>", "2,16 gramdır", "5 g CaCO<sub>3</sub>", "0,02 mol C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>",
                  "0,5 mol boraks", "≈ 19 katrilyon yıl", "≈ 140 kat"):
        kontrol(f"sayfada '{metin}' var", metin in html)
else:
    print("UYARI: unite.html yok; önce python3 uretec/kur.py çalıştır.")

# ------------------------------------------------------------------ akçe muhasebesi
durak = {
    "1. durak": dict(kavram=30, tuzak=20, H1=10, hizli=40),
    "2. durak": dict(hizli_kontrol=20, gorev1=50, H2=10, H3=10, tuzak=20, hizli=40),
    "3. durak": dict(gorev2=25, gorev3=25, gorev4=30, H4=10, H5=10, H6=10, tuzak=10, hizli=30),
    "4. durak": dict(H7=10, H8=10, gorev5=50, gorev6=40, tuzak1=10, tuzak2=10, hizli=20),
    "5. durak": dict(H9=10, H10=10, gorev7=50, gorev8=40, tuzak=10, hizli=30),
}
toplamlar = {k: sum(v.values()) for k, v in durak.items()}
kontrol(f"Durak akçeleri {toplamlar} = 100/150/150/150/150", list(toplamlar.values()) == [100, 150, 150, 150, 150])
yan = dict(hulasa=40, meclis=4 * 30, kissa=4 * 30, anahtar=3 * 40, imtihan=12 * 25)
toplam = sum(toplamlar.values()) + sum(yan.values())
kontrol(f"Ünite toplam akçe {toplam} = 1400", toplam == 1400)
kontrol("Ray eşikleri: 400/1400 %28,57 · 800/1400 %57,14 · 1150/1400 %82,14",
        [round(400 / 1400 * 100, 2), round(800 / 1400 * 100, 2), round(1150 / 1400 * 100, 2)] == [28.57, 57.14, 82.14])
bar = [0, 0, 7, 18, 29, 39, 50, 53, 61, 70, 79, 89, 100, 100, 100]          # 15 sayfa (13: Üstad, akçesiz)
birikim = [0, 0, 100, 250, 400, 550, 700, 740, 860, 980, 1100, 1250, 1400, 1400, 1400]
kontrol("HUD akçe çubuğu yüzdeleri", [round(b / 1400 * 100) for b in birikim] == bar)

# ------------------------------------------------------------------ Üstad soruları (bonus; 1400 akçeye dahil değil)
U = {}
q = (24.3 - 24) / (25 + 26 - 2 * 24)                     # 24(1 − 2q) + 25q + 26q = 24,3
kontrol(f"Üstad 1: q = {q:.3f} → bolluk 0,8 / 0,1 / 0,1, ortalama 24,3", yakin(q, .1) and yakin(24 * (1 - 2 * q) + 25 * q + 26 * q, 24.3))
U[1] = tek_sik("Üstad 1", {"A": 3.01e22, "B": 6.02e22, "C": 1.204e23, "D": 2.408e23, "E": 3.01e23}, lambda v: yakin(v, 2 * q * .5 * NA), "B")
for ad, MX in (("Mg", 24), ("S", 32)):                 # a = 1 X atomu (g), b = 1 ¹²C atomu (g) = 12/N_A
    a_, b_ = MX / NA, 12 / NA
    U[2] = tek_sik(f"Üstad 2 (X = {ad})", {"A": a_ + 32 * b_, "B": a_ + 4 * b_ / 3, "C": 12 * a_ / b_ + 32, "D": (a_ + 32) / NA, "E": a_ + 8 * b_ / 3},
                   lambda v: math.isclose(v, (MX + 32) / NA, rel_tol=1e-9), "E")   # göreli: değerler ~10⁻²² g
nI, nII, nIII = .2, 6.8 / mk("NH3"), 1.806e23 / NA
H3 = [nI * 6, nII * 3, nIII * 2]
K3 = [nI * mk("C2H6"), 6.8, nIII * mk("H2O")]
A3 = [nI * 8, nII * 4, nIII * 3]
kontrol(f"Üstad 3: H {[round(v, 2) for v in H3]} · kütle {[round(v, 2) for v in K3]} · atom {[round(v, 2) for v in A3]}",
        yakin(H3[0], 1.2) and yakin(H3[1], 1.2) and yakin(K3[0], 6) and yakin(K3[2], 5.4) and yakin(A3[2], .9))
d3 = yargi({"I": yakin(H3[0], H3[1]), "II": max(K3) == K3[0], "III": min(A3) == A3[2] and sorted(A3)[1] > A3[2]})
U[3] = tek_sik("Üstad 3", {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}, lambda v: v == d3, "D")
y4 = (mk("NaCl") * .5 - 28.35) / (2 * mk("NaCl") - mk("CaCl2"))      # x = 0,5 − 2y
x4 = .5 - 2 * y4
kontrol(f"Üstad 4: NaCl {x4:.2f} mol, CaCl2 {y4:.2f} mol → kütle 28,35 g, Cl 0,5 mol",
        yakin(x4 * mk("NaCl") + y4 * mk("CaCl2"), 28.35) and yakin(x4 + 2 * y4, .5) and yakin(y4, .15))
U[4] = tek_sik("Üstad 4", {"A": 5.85, "B": 8.775, "C": 11.7, "D": 16.65, "E": 17.55}, lambda v: yakin(v, x4 * mk("NaCl")), "C")
nY = (20.8 - 8) / mk("SO2")
kontrol("Üstad 5: grafik (8; 2,5) → X eğimi 5/16 = CH4 (SO2 olsa 3/64); (20,8; 3,1) → Y = SO2",
        yakin(2.5 / 8, 5 / mk("CH4")) and not yakin(2.5 / 8, 3 / mk("SO2")) and yakin(2.5 + nY * 3, 3.1))
U[5] = tek_sik("Üstad 5", {"A": .2, "B": .25, "C": .4, "D": .6, "E": .8}, lambda v: yakin(v, nY), "A")
m1 = 18 / NA                                            # 1 H2O molekülü (g); akb ve atom kütleleri tanımdan bağımsız


def u6(N):                                              # N: 1 moldeki tanecik sayısı
    return {"A": N * m1, "B": 18 / (N * m1), "C": 3 * N, "D": m1, "E": N * m1}


U[6] = tek_sik("Üstad 6 (değişmeyen nicelik)", {k: (u6(6.02e23)[k], u6(3.01e23)[k]) for k in "ABCDE"}, lambda v: yakin(v[0], v[1]), "D")
harf_dagilimi(U.values())

# ------------------------------------------------------------------ sayfadaki öğretmen işaretleri (öğretmen baskısı = bu işaretler)
if os.path.exists(HTML):
    beklenen = {f"I{k}": v for k, v in T.items()}
    beklenen.update({f"K{i}": anahtar[f"K{i}"] for i in range(1, 5)})
    beklenen.update({f"U{k}": v for k, v in U.items()})
    sayfa_isaretleri_ayni(html, beklenen)
    kontrol(f"meclis hükümleri (haklı kişi, satır) {meclis_hukumleri(html)}",
            meclis_hukumleri(html) == {"M1": ("Yusuf", 2), "M2": ("Elif", 1), "M3": ("Yusuf", 2), "M4": ("Pamuk", 2)})
    for k, h in U.items():
        kontrol(f"s.14 Üstad çözümü 'Ü{k} · {h}' var", f"<b>Ü{k} · {h}</b>" in html)
    us = re.search(r"<p><b>Üstad</b>(.*?)</p>", html)
    kontrol("s.14 hızlı anahtarda Üstad satırı hesapla aynı", bool(us) and re.findall(r'<span class="ck">(\d) ([A-E])</span>', us.group(1)) == [(str(k), h) for k, h in U.items()])
    ogr = ogretmen_metinleri(html)
    kontrol(f"öğretmen metinleri: {len(ogr)} (5 CEVABIN + 3 boşluk + 8 meclis + 4 kıssa + 9 merdiven + 12 imtihan + 6 Üstad = 47)", len(ogr) == 47)
    ciftler = re.findall(r'CEVABIN:<span class="ogr">(.*?)</span></div><span class="ters-cevap"><span class="ters">(?:Cevap: )?(.*?)</span></span>', html)
    kontrol(f"CEVABIN kutusundaki kırmızı cevap ters yazılı cevapla aynı ({len(ciftler)} kutu)",
            len(ciftler) == 5 and all(a == b or a.endswith("= " + b) for a, b in ciftler))
    kontrol("Üstad sayfası: 6 kart, Üstad Mührü nişanı, akçe yok", html.count('class="ustad-soru"') == 6 and "Üstad Mührü" in html)

print("\nCEVAP ANAHTARI · İmtihan:", " ".join(f"{k}{v}" for k, v in T.items()), "· Kıssa:", " ".join(f"{k}{v}" for k, v in anahtar.items()),
      "· Üstad:", " ".join(f"Ü{k}{v}" for k, v in U.items()))
D.sonuc()
