"""Çözünme ve Çözünürlük (yerel · Pamukkale–Afyon Yolu) — bütün sayıların ve cevap anahtarının doğrulaması.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Her görev, tuzak, hızlı görev, kıssa, meclis, merdiven, imtihan ve Üstad sorusu burada YENİDEN hesaplanır.
     Grafik değerleri infografik_unite.VERI'den okunur (grafikle soru aynı kaynaktan).
  2. Her çoktan seçmeli soruda TEK doğru şık (tek_sik); İmtihan ve Üstad'da A–E her harf en az bir kez.
  3. Sayfadan (unite.html) okunan data-dogru işaretleri, meclis hükümleri, Cevaplar ızgarası ve çözüm satırları hesapla aynı mı?
  4. Akçe muhasebesi (duraklar 100 + 5×120, toplam 1400) ve HUD akçe çubuğu.
Yardımcılar: yerel-ortak/dogrula_ortak.py
"""
import os
import re
import sys

BURA = os.path.dirname(os.path.abspath(__file__))


def _ortak():
    d = BURA
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


sys.path.insert(0, _ortak())
sys.path.insert(0, BURA)
from dogrula_ortak import (D, NA, mk, yakin, kontrol, tek_sik, yargi, dagilim, sayfa_oku, sayfa_isaretleri_ayni,  # noqa: E402
                           meclis_hukumleri, ogretmen_metinleri, anahtar_izgarasi)
from infografik_unite import VERI, oku  # noqa: E402

YARGI = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}
YARGI_IIII = {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}
YARGI_D13 = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}

# ------------------------------------------------------------------ küçük kimya modeli (benzer benzeri, iyon sayısı)
# tür: iyonik | polar | apolar ; hb: H, F/O/N'ye bağlı mı (hidrojen bağı verebilir mi)
TUR = {"H2O": ("polar", True), "NH3": ("polar", True), "C2H5OH": ("polar", True), "CH3OH": ("polar", True), "HF": ("polar", True),
       "HCl": ("polar", False), "H2S": ("polar", False), "CO": ("polar", False),
       "I2": ("apolar", False), "O2": ("apolar", False), "CCl4": ("apolar", False), "CH4": ("apolar", False), "C6H14": ("apolar", False),
       "C6H6": ("apolar", False), "CO2": ("apolar", False),
       "KBr": ("iyonik", False), "NaCl": ("iyonik", False), "KCl": ("iyonik", False), "KNO3": ("iyonik", False)}


def etkilesim(a, b):
    (ta, ha), (tb, hb) = TUR[a], TUR[b]
    t = {ta, tb}
    if t == {"iyonik", "polar"}:
        return "iyon–dipol"
    if t == {"iyonik", "apolar"}:
        return "iyon–indüklenmiş dipol"
    if t == {"polar"}:
        return "hidrojen bağı" if (ha and hb) else "dipol–dipol"
    if t == {"polar", "apolar"}:
        return "dipol–indüklenmiş dipol"
    if t == {"apolar"}:
        return "London"
    return "?"


def iyi_cozunur(a, b):
    return etkilesim(a, b) in ("iyon–dipol", "hidrojen bağı", "dipol–dipol", "London")


IYON = {"Na2SO4": 3, "NaCl": 2, "CaCl2": 3, "KNO3": 2, "AlCl3": 4, "KCl": 2, "KOH": 2, "C6H12O6": 0, "C2H5OH": 0, "CH3OH": 0}


def cozunur(S, su):
    """S (g/100 g su) ile su (g): çözünebilecek en çok madde (g)."""
    return S * su / 100


# ------------------------------------------------------------------ grafik verisi (sayfalarda yazan değerlerle aynı mı?)
kontrol("VERI KNO3: 20 °C 32, 60 °C 110, 80 °C 169", (oku("KNO3", 20), oku("KNO3", 60), oku("KNO3", 80)) == (32, 110, 169))
kontrol("VERI NaCl: 20 °C 36, 80 °C 38 (Kıssa 3 tablosu)", (oku("NaCl", 20), oku("NaCl", 80)) == (36, 38))
kontrol("VERI Li2SO4 sıcaklıkla azalır (ekzotermik örnek)", all(b[1] < a[1] for a, b in zip(VERI["Li2SO4"], VERI["Li2SO4"][1:])))
kontrol("VERI KNO3 sıcaklıkla artar (endotermik örnek)", all(b[1] > a[1] for a, b in zip(VERI["KNO3"], VERI["KNO3"][1:])))
kontrol("VERI CO2: 20 °C 1,7 · 40 °C 1,0 g/L; sıcaklıkla azalır", yakin(oku("CO2", 20), 1.7) and yakin(oku("CO2", 40), 1.0)
        and all(b[1] < a[1] for a, b in zip(VERI["CO2"], VERI["CO2"][1:])))
kontrol("VERI O2: 10 °C 11,3 · 20 °C 9,1 mg/L", yakin(oku("O2", 10), 11.3) and yakin(oku("O2", 20), 9.1))
kontrol("VERI X: 20→30, 30→40, 40→50, 60→70, 80→100", [oku("X", t) for t in (20, 30, 40, 60, 80)] == [30, 40, 50, 70, 100])
kontrol("VERI X artan (endotermik); doygunluk noktaları A 35 < B 60 = S(50) < C 82", oku("X", 50) == 60 and 35 < 60 < 82)
kontrol("VERI A artan, B azalan (İmtihan 6)", all(b[1] > a[1] for a, b in zip(VERI["A"], VERI["A"][1:]))
        and all(b[1] < a[1] for a, b in zip(VERI["B"], VERI["B"][1:])))

# ------------------------------------------------------------------ 1. durak · Pamukkale
kontrol("Görev 1A: 786 < 790 → net 4 kJ ısı alır (endotermik, su soğur)", 790 - 786 == 4 and 786 < 790)
kontrol("Görev 1B: 650 > 600 → net 50 kJ ısı verir (ekzotermik, su ısınır)", 650 - 600 == 50 and 650 > 600)
kontrol("Hızlı görev: tunç 88 g Cu + 12 g Sn = 100 g; çözücü bakır (çok olan)", 88 + 12 == 100 and 88 > 12)

# ------------------------------------------------------------------ 2. durak · Karahayıt
g2 = {"I": iyi_cozunur("C2H5OH", "H2O"), "II": iyi_cozunur("I2", "CCl4"), "III": iyi_cozunur("KCl", "C6H14"), "IV": iyi_cozunur("C6H14", "H2O")}
kontrol(f"Görev 2: iyi çözünenler I ve II {g2}", yargi(g2) == {"I", "II"})
en_iyi = [m for m in ("NH3", "CCl4", "I2") if etkilesim(m, "H2O") == "hidrojen bağı"]
kontrol("Hızlı görev: suda en iyi NH3 (hidrojen bağı)", en_iyi == ["NH3"])
kontrol("Tablo: HCl–H2S → dipol–dipol", etkilesim("HCl", "H2S") == "dipol–dipol")
kontrol("Tuzak: CH4–H2O hidrojen bağı DEĞİL (dipol–indüklenmiş dipol)", etkilesim("CH4", "H2O") == "dipol–indüklenmiş dipol")
tablo = {("KBr", "H2O"): "iyon–dipol", ("HCl", "H2S"): "dipol–dipol", ("NH3", "H2O"): "hidrojen bağı",
         ("O2", "H2O"): "dipol–indüklenmiş dipol", ("NaCl", "CCl4"): "iyon–indüklenmiş dipol", ("I2", "CCl4"): "London"}
kontrol("Etkileşim tablosu (6 satır) modelle aynı", all(etkilesim(a, b) == v for (a, b), v in tablo.items()))

# ------------------------------------------------------------------ 3. durak · Acıgöl
kontrol("Görev 3: 0,2 mol Na2SO4 → 0,6 mol iyon; 0,4 mol Na+ = 2,408e23", yakin(.2 * IYON["Na2SO4"], .6) and yakin(.4 * NA, 2.408e23))
sira = sorted(("NaCl", "CaCl2", "C6H12O6"), key=lambda m: -IYON[m])
kontrol(f"Hızlı görev: iletkenlik CaCl2 > NaCl > glikoz {sira}", sira == ["CaCl2", "NaCl", "C6H12O6"])
kontrol("Elektrolit: KOH (iyonik) evet, CH3OH hayır", IYON["KOH"] > 0 and IYON["CH3OH"] == 0)

# ------------------------------------------------------------------ 4. durak · Ömer–Gecek
kontrol("Kavram: 20 °C KNO3 32 → 132 g doymuş çözelti", 100 + oku("KNO3", 20) == 132)
kontrol("Görev 4: 60 °C, 40 g su → 44 g KNO3 → 84 g", yakin(cozunur(oku("KNO3", 60), 40), 44) and yakin(40 + 44, 84))
kontrol("Görev 5: 3 atm → 3·1,7 = 5,1 g; 1 atm'e inince 3,4 g ayrılır", yakin(3 * oku("CO2", 20), 5.1) and yakin(5.1 - 1.7, 3.4))
kontrol("Hızlı görev: 20 °C 50 g su → 18 g NaCl", yakin(cozunur(oku("NaCl", 20), 50), 18))

# ------------------------------------------------------------------ 5. durak · Gazlıgöl (şeker, 20 °C ≈ 200)
S_SEKER_20, S_SEKER_80 = 200, 360          # yaklaşık (gerçek ≈ 204 ve 362 g/100 g su)
kontrol("Şeker çözünürlüğü yaklaşık değerleri gerçeğe yakın (±%3)", abs(S_SEKER_20 - 204) / 204 < .03 and abs(S_SEKER_80 - 362) / 362 < .03)


def sinif(m, su, S, kati=False):
    oran = m / su * 100
    return "doymamış" if oran < S - 1e-9 else ("doymuş" if abs(oran - S) < 1e-9 or kati else "aşırı doymuş")


g6 = [sinif(m, 50, S_SEKER_20) for m in (80, 100, 130)]
kontrol(f"Görev 6: {g6} = doymamış, doymuş, aşırı doymuş", g6 == ["doymamış", "doymuş", "aşırı doymuş"])

# ------------------------------------------------------------------ 6. durak · Afyon çarşısı (X tuzu + şerbet)
su7 = 60 / oku("X", 40) * 100
kontrol("Görev 7: 40 °C, 60 g X → 120 g su → 180 g çözelti", yakin(su7, 120) and yakin(su7 + 60, 180))
k8 = 400 / (100 + oku("X", 80))
su8, x8 = 100 * k8, oku("X", 80) * k8
kontrol("Görev 8: 400 g → 200 g su + 200 g X; 20 °C 60 g → 140 g çöker", yakin(su8, 200) and yakin(x8, 200) and yakin(x8 - cozunur(oku("X", 20), su8), 140))
kontrol("Görev 9A: 80 °C 50 g su 180 g şeker alır; 150 → doymamış, 30 g daha", yakin(cozunur(S_SEKER_80, 50), 180) and 180 - 150 == 30)
kontrol("Görev 9B: 20 °C 50 g su 100 g alır; 150 > 100, katı yok → aşırı doymuş; 50 g çöker",
        sinif(150, 50, S_SEKER_20) == "aşırı doymuş" and 150 - cozunur(S_SEKER_20, 50) == 50)
oran = 100 / 250 * 100
T_kr = [t for t, v in VERI["X"] if yakin(v, oran)]
kontrol(f"Hızlı görev: 100 g X / 250 g su = {oran} → kristallenme {T_kr} °C", T_kr == [30])
kontrol("Tuzak: S = 25, 375 g doymuş → 75 g tuz + 300 g su (375·25/100 = 93,75 yanlış)",
        yakin(375 * 25 / 125, 75) and yakin(375 - 75, 300) and yakin(375 * 25 / 100, 93.75))

# ------------------------------------------------------------------ Meclis
kontrol("Meclis 1 (Ömer): CCl4 apolar → I2–CCl4 London; hata satır 2 → Yusuf", etkilesim("I2", "CCl4") == "London")
kontrol("Meclis 2 (Hatice): toz şeker yalnız hızlı; çözünürlük aynı (satır 3) → Pamuk", True)
kontrol("Meclis 3 (Furkan): 375 g çözeltide 75 g X (93,75 yanlış) → Elif, satır 2", yakin(375 * 25 / 125, 75) and not yakin(375 * 25 / 100, 75))
kontrol("Meclis 4 (Esma): S = 40, 60 g X → 150 g su → 150 g buharlaşır (24 → 276 yanlış) → Yusuf, satır 1",
        yakin(60 * 100 / 40, 150) and 300 - 150 == 150 and yakin(60 * 40 / 100, 24) and yakin(300 - 24, 276))

# ------------------------------------------------------------------ Kıssalar
anahtar = {}
k1 = yargi({"I": all(b[1] < a[1] for a, b in zip(VERI["O2"], VERI["O2"][1:])), "II": yakin(oku("O2", 10) - oku("O2", 20), 2.2), "III": False})
anahtar["K1"] = tek_sik("Kıssa 1 (dere, O2)", YARGI, lambda v: v == k1, "C")
ampul = {"P": "sönük", "R": "parlak", "S": "yanmıyor", "T": "parlak"}
tur_ampul = {"KNO3": "parlak", "glikoz": "yanmıyor", "sirke asidi": "sönük", "HCl": "parlak"}
p_s = tuple(next(m for m, a in tur_ampul.items() if a == ampul[k]) for k in ("P", "S"))
anahtar["K2"] = tek_sik("Kıssa 2 (ampul)", {"A": ("glikoz", "sirke asidi"), "B": ("sirke asidi", "glikoz"), "C": ("KNO3", "glikoz"),
                                            "D": ("HCl", "sirke asidi"), "E": ("sirke asidi", "KNO3")}, lambda v: v == p_s, "B")
kno3_80, nacl_80 = 140 <= oku("KNO3", 80), 30 <= oku("NaCl", 80)
kno3 = 140 - oku("KNO3", 20)
nacl = max(0, 30 - oku("NaCl", 20))
kontrol("Kıssa 3: 80 °C'ta ikisi de çözünmüş; 20 °C'ta 108 g KNO3, NaCl yok", kno3_80 and nacl_80 and kno3 == 108 and nacl == 0)
anahtar["K3"] = tek_sik("Kıssa 3 (gübre)", {"A": (0, 0), "B": (0, 6), "C": (108, 6), "D": (137, 0), "E": (108, 0)}, lambda v: v == (kno3, nacl), "E")
k4 = yargi({"I": True, "II": False, "III": False})      # aşırı doymuş kararsız; kristallenme ısı verir; sonunda sıvı doymuş
anahtar["K4"] = tek_sik("Kıssa 4 (cep ısıtıcısı)", YARGI_D13, lambda v: v == k4, "A")

# ------------------------------------------------------------------ Anahtar merdiveni
k1m = 400 / (100 + 60)
kontrol("Merdiven 1: 400/160 = 2,5 → 250 g su + 150 g Q; 10 °C 50 g → 100 g çöker",
        yakin(k1m, 2.5) and yakin(60 * k1m - cozunur(20, 100 * k1m), 100))
su_ilk = 200 - 40 * 100 / 50
kontrol("Merdiven 2: önce 120 g, +20 → 140 g su; kalan 60 g su 30 g çözer → 10 g çöker",
        yakin(su_ilk, 120) and yakin(su_ilk + 20, 140) and yakin(40 - cozunur(50, 200 - 140), 10))
Ytab = {0: 12, 20: 24, 40: 40, 60: 64}
kontrol("Merdiven 3: 60 °C'ta doymamış (120 < 192); 40 g/100 g → 40 °C; 0 °C'ta 36 g → 84 g çöker",
        120 < cozunur(Ytab[60], 300) and [t for t, v in Ytab.items() if v == 120 / 300 * 100] == [40] and 120 - cozunur(Ytab[0], 300) == 84)

# ------------------------------------------------------------------ Büyük İmtihan (12 soru)
T = {}
i1 = {"A": True, "B": False, "C": True, "D": True, "E": True}   # B: hacim her zaman toplanmaz (etanol + su)
T[1] = tek_sik("İmtihan 1 (yanlış olan)", i1, lambda v: not v, "B")
i2 = {"A": (("KBr", "H2O"), "iyon–dipol"), "B": (("I2", "C6H6"), "London"), "C": (("NH3", "H2O"), "hidrojen bağı"),
      "D": (("HCl", "H2S"), "hidrojen bağı"), "E": (("O2", "H2O"), "dipol–indüklenmiş dipol")}
T[2] = tek_sik("İmtihan 2 (yanlış eşleşme)", i2, lambda v: etkilesim(*v[0]) != v[1], "D")
T[3] = tek_sik("İmtihan 3 (hekzanda çözünen)", {"A": "NaCl", "B": "H2O", "C": "CCl4", "D": "KNO3", "E": "NH3"},
               lambda v: iyi_cozunur(v, "C6H14"), "C")
iletken = yargi({"I": IYON["C6H12O6"] > 0, "II": IYON["KCl"] > 0, "III": True, "IV": IYON["C2H5OH"] > 0})   # HCl suda iyonlaşır
T[4] = tek_sik("İmtihan 4 (iletenler)", {"A": {"II", "III"}, "B": {"I", "II"}, "C": {"III", "IV"}, "D": {"I", "II", "III"}, "E": {"II", "III", "IV"}},
               lambda v: v == iletken, "A")
kimyasal = {"şeker": False, "NaNO3": False, "etanol": False, "KBr": False, "HCl": True}
T[5] = tek_sik("İmtihan 5 (kimyasal çözünme)", dict(zip("ABCDE", kimyasal.values())), lambda v: v, "E")
i6 = yargi({"I": all(b[1] > a[1] for a, b in zip(VERI["A"], VERI["A"][1:])),
            "II": all(b[1] < a[1] for a, b in zip(VERI["B"], VERI["B"][1:])), "III": False})
T[6] = tek_sik("İmtihan 6 (A–B grafiği)", YARGI, lambda v: v == i6, "C")
T[7] = tek_sik("İmtihan 7 (CO2 artırma)", {"A": {"I", "II"}, "B": {"I"}, "C": {"II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}},
               lambda v: v == {"I", "II"}, "A")
i8 = {"A": ("hız", None), "B": ("hız", None), "C": (None, None), "D": (None, None), "E": ("hız", "çözünürlük")}
T[8] = tek_sik("İmtihan 8 (ikisini de artıran)", i8, lambda v: v == ("hız", "çözünürlük"), "E")
T[9] = tek_sik("İmtihan 9 (dipte kalan)", dict(A=0, B=5, C=8, D=13, E=32), lambda v: yakin(v, 45 - cozunur(40, 80)), "D")
k10 = 350 / (100 + 75)
T[10] = tek_sik("İmtihan 10 (çöken)", dict(A=50, B=100, C=125, D=150, E=175), lambda v: yakin(v, 75 * k10 - cozunur(25, 100 * k10)), "B")
T[11] = tek_sik("İmtihan 11 (buharlaşan)", dict(A=80, B=120, C=160, D=240, E=280), lambda v: yakin(v, 400 - 120 * 100 / 50), "C")
i12 = tuple(sinif(m, su, 25) for su, m in ((60, 15), (120, 20), (40, 14)))
T[12] = tek_sik("İmtihan 12 (sınıflandırma)", {"A": ("doymamış", "doymuş", "aşırı doymuş"), "B": ("doymuş", "aşırı doymuş", "doymamış"),
                                               "C": ("aşırı doymuş", "doymamış", "doymuş"), "D": ("doymuş", "doymamış", "aşırı doymuş"),
                                               "E": ("doymuş", "doymuş", "aşırı doymuş")}, lambda v: v == i12, "D")
dagilim(T.values())

# ------------------------------------------------------------------ Üstad soruları (bonus; 1400 akçeye dahil değil)
U = {}
na = VERI["Na2SO4"]
tepe = max(na, key=lambda p: p[1])
artan = all(b[1] > a[1] for a, b in zip(na, na[1:]) if b[0] <= tepe[0])
azalan = all(b[1] < a[1] for a, b in zip(na, na[1:]) if a[0] >= tepe[0])
u1 = yargi({"I": artan and tepe[0] > 30, "II": azalan and oku("Na2SO4", 60) < oku("Na2SO4", 40), "III": artan and azalan and 31 < tepe[0] < 33})
U[1] = tek_sik("Üstad 1 (Na2SO4 grafiği)", YARGI, lambda v: v == u1, "E")
u2 = oku("CO2", 20) * 3 * 2 - oku("CO2", 40) * 3 * 2
U[2] = tek_sik("Üstad 2 (CO2, 2 L, 3 atm, 40 → 20 °C)", dict(A=2.1, B=4.2, C=6.0, D=7.0, E=10.2), lambda v: yakin(v, u2), "B")
iy = [.2 * IYON["Na2SO4"], .3 * IYON["KNO3"], .15 * IYON["AlCl3"]]
u3 = yargi({"I": yakin(iy[0], iy[1]) and yakin(iy[1], iy[2]), "II": .15 * 3 > .2 * 2, "III": IYON["C2H5OH"] > 0})
kontrol(f"Üstad 3: iyon molleri {iy} = 0,6; Cl- 0,45 > Na+ 0,4", all(yakin(v, .6) for v in iy))
U[3] = tek_sik("Üstad 3 (tablo)", YARGI_IIII, lambda v: v == u3, "C")
k4u = 300 / (100 + oku("X", 80))
su4, x4 = 100 * k4u - 50, oku("X", 80) * k4u
u4 = x4 - cozunur(oku("X", 20), su4)
kontrol(f"Üstad 4: 150 g su + 150 g X; 50 g su gider → {su4} g su; 20 °C'ta 30 g kalır → {u4} g", yakin(su4, 100) and yakin(u4, 120))
U[4] = tek_sik("Üstad 4 (buharlaştır + soğut)", dict(A=120, B=50, C=75, D=105, E=135), lambda v: yakin(v, u4), "A")
endo = 790 > 786                                         # harcanan > açığa çıkan (Görev 1A ile aynı model)
u5 = yargi({"I": endo, "II": not endo, "III": endo})
U[5] = tek_sik("Üstad 5 (enerji)", YARGI_D13, lambda v: v == u5, "D")
# Ca2+ + 2HCO3- ⇌ CaCO3(k) + CO2(g) + H2O : CO2 ortamdan giderse sağa (daha çok CaCO3); CO2 eklenirse, soğutulursa
# (CO2 suda daha çok kalır), seyreltilirse sola.
u6 = {"A": -1, "B": -1, "C": -1, "D": +1, "E": -1}
U[6] = tek_sik("Üstad 6 (traverten dengesi)", u6, lambda v: v > 0, "D")
dagilim(U.values())

# ------------------------------------------------------------------ sayfadan okunanlar (unite.html)
html = sayfa_oku(__file__)
if html:
    beklenen = {f"I{k}": v for k, v in T.items()}
    beklenen.update({k: v for k, v in anahtar.items()})
    beklenen.update({f"U{k}": v for k, v in U.items()})
    sayfa_isaretleri_ayni(html, beklenen)
    izgara = anahtar_izgarasi(html)
    kontrol(f"s.15 anahtar ızgarası hesapla aynı {izgara}", izgara == T)
    for no, h in T.items():
        kontrol(f"s.15 çözüm satırı '{no} · {h}' var", f"<b>{no} · {h}</b>" in html)
    for i in range(1, 5):
        kontrol(f"s.15 kıssa çözümü '{i} · {anahtar[f'K{i}']}' var", f"<b>{i} · {anahtar[f'K{i}']}</b>" in html)
    for k, h in U.items():
        kontrol(f"s.15 Üstad çözümü 'Ü{k} · {h}' var", f"<b>Ü{k} · {h}</b>" in html)
    ks = re.search(r"<p><b>Kıssa</b>(.*?)</p>", html)
    kontrol("s.15 hızlı anahtar: Kıssa satırı hesapla aynı", bool(ks) and re.findall(r'<span class="ck">(\d) ([A-E])</span>', ks.group(1)) == [(str(i), anahtar[f"K{i}"]) for i in range(1, 5)])
    us = re.search(r"<p><b>Üstad</b>(.*?)</p>", html)
    kontrol("s.15 hızlı anahtar: Üstad satırı hesapla aynı", bool(us) and re.findall(r'<span class="ck">(\d) ([A-E])</span>', us.group(1)) == [(str(k), h) for k, h in U.items()])
    mh = meclis_hukumleri(html)
    kontrol(f"meclis hükümleri (haklı kişi, satır) {mh}", mh == {"M1": ("Yusuf", 2), "M2": ("Pamuk", 3), "M3": ("Elif", 2), "M4": ("Yusuf", 1)})
    mc = re.search(r"<p><b>Meclis</b>(.*?)</p>", html)
    kontrol("s.15 hızlı anahtar: Meclis satırı sayfadaki hükümlerle aynı", bool(mc) and re.findall(r'<span class="ck">\d (\w+)</span>', mc.group(1)) == [mh[f"M{i}"][0] for i in range(1, 5)])
    for i, kisi in enumerate(("Yusuf", "Pamuk", "Elif", "Yusuf"), 1):
        kontrol(f"s.15 meclis çözümü '{i} · {kisi}' var", f"<b>{i} · {kisi}</b>" in html)
    ogr = ogretmen_metinleri(html)
    kontrol(f"öğretmen metinleri: {len(ogr)} (1 boşluk + 6 CEVABIN + 8 meclis + 4 kıssa + 9 merdiven + 12 imtihan + 6 Üstad = 46)", len(ogr) == 46)
    ciftler = re.findall(r'CEVABIN:<span class="ogr">(.*?)</span></div><span class="ters-cevap"><span class="ters">(?:Cevap: )?(.*?)</span></span>', html)
    kontrol(f"CEVABIN kutusundaki kırmızı cevap ters yazılı cevapla aynı ({len(ciftler)} kutu)", len(ciftler) == 6 and all(a == b for a, b in ciftler))
    kontrol("Üstad sayfası: 6 kart, Üstad Mührü, akçe yok", html.count('class="ustad-soru"') == 6 and "Üstad Mührü" in html)
    kontrol("Üstad: en az bir grafik (Na2SO4) ve bir tablo", "ustad-graf" in html and 'class="ustad-tablo"' in html)
    kontrol("12 meşveret + 4 kıssa kartı", html.count('class="kart mesveret"') == 12 and html.count('class="kart kissa"') == 4)
    for metin in ("140 g KNO<sub>3</sub> ve 30 g NaCl", "375 · 25 / 100", "yaklaşık 700 basamak", "80 °C’ta 360, 20 °C’ta 200",
                  "0,2 mol Na<sub>2</sub>SO<sub>4</sub>", "≈ 1,7 g CO<sub>2</sub>", "10 °C’tan 20 °C’a", "60 g X ile"):
        kontrol(f"sayfada '{metin}' var", metin in html)
    for h in ("H" + str(i) for i in range(1, 13)):
        kontrol(f"hazine kartı {h} sayfada bir kez", html.count(f'<b>{h}</b>') >= 1)
else:
    print("UYARI: unite.html yok; önce python3 uretec/kur.py çalıştır.")

# ------------------------------------------------------------------ akçe muhasebesi
durak = {
    "1. durak": dict(kavram=20, gorev1=30, H1=10, H2=10, tuzak=10, hizli=20),
    "2. durak": dict(gorev2=40, H3=10, H4=10, tuzak=20, hizli=40),
    "3. durak": dict(gorev3=40, H5=10, H6=10, tuzak=20, hizli=40),
    "4. durak": dict(gorev4=30, gorev5=30, H7=10, H8=10, tuzak=10, hizli=30),
    "5. durak": dict(gorev6=40, H9=10, H10=10, tuzak=20, hizli=40),
    "6. durak": dict(gorev7=20, gorev8=25, gorev9=25, H11=10, H12=10, tuzak=10, hizli=20),
}
toplamlar = [sum(v.values()) for v in durak.values()]
kontrol(f"Durak akçeleri {toplamlar} = 100/120/120/120/120/120", toplamlar == [100, 120, 120, 120, 120, 120])
import json  # noqa: E402
meta = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
kontrol("meta.json durak akçeleri sayfadakiyle aynı", [d["akce"] for d in meta["duraklar"]] == toplamlar)
yan = dict(hulasa=40, meclis=4 * 30, kissa=4 * 30, anahtar=3 * 40, imtihan=12 * 25)
toplam = sum(toplamlar) + sum(yan.values())
kontrol(f"Ünite toplam akçe {toplam} = 1400", toplam == 1400)
kontrol("Ahilik eşikleri 400/800/1150 (%28,57 · %57,14 · %82,14)",
        [round(a / 1400 * 100, 2) for a in (400, 800, 1150)] == [28.57, 57.14, 82.14])
birikim = [0, 0] + [sum(toplamlar[:i]) for i in range(1, 7)] + [700 + 40, 860, 980, 1100, 1250, 1400, 1400, 1400]
from kur import SAYFA  # noqa: E402
bar = [SAYFA[n][2] for n in range(1, 17)]
kontrol(f"HUD akçe çubuğu {bar}", [round(b / 1400 * 100) for b in birikim] == bar)
kontrol("meta.json: 8 nişan (6 durak + Kale + bonus Üstad), 12 hazine kartı",
        len(meta["nisanlar"]) == 8 and meta["nisanlar"][-1].get("bonus") and [h["kod"] for h in meta["hazine"]] == [f"H{i}" for i in range(1, 13)])

print("\nCEVAP ANAHTARI · İmtihan:", " ".join(f"{k}{v}" for k, v in T.items()), "· Kıssa:", " ".join(f"{k}{v}" for k, v in anahtar.items()),
      "· Üstad:", " ".join(f"Ü{k}{v}" for k, v in U.items()))
D.sonuc()
