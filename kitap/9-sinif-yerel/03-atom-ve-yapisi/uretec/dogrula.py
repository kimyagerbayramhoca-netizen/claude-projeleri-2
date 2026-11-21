"""Atom ve Yapısı (yerel · Şanlıurfa–Harran yolu) — bütün cevapların ve cevap anahtarının doğrulaması.

Çalıştır:  python3 uretec/dogrula.py
  1. Küçük bir dizilim motoru (Aufbau sırası, Cr/Cu istisnaları, katyonda önce en dış katman) ile her dizilim, yarı dolu
     orbital, değerlik elektronu, küresel simetri ve enerji düzeyi sayısı yeniden hesaplanır.
  2. p, n, e sayıları; izotop/izoton/izobar/izoelektronik ilişkileri; Hund kuralı (sayfadaki orbital şemalarından okunur);
     hidrojenin çizgileri (Rydberg) ve enerji düzeyleri yeniden hesaplanır.
  3. Her çoktan seçmeli soruda TEK doğru şık; sayfadaki data-dogru işaretleri, meclis hükümleri, anahtar ızgarası,
     çözüm harfleri, hızlı anahtar ve öğretmen (.ogr) metinleri hesapla aynı mı?
  4. Akçe: durak toplamları (100 + 5 × 120), yan yollar, imtihan, 1400; HUD çubukları; Ahilik eşikleri; final defteri.
  5. Sayfa göndermeleri (s.{{sayfa|n}}) doğru sayfayı mı gösteriyor? İmtihanda A–E her harf en az bir kez mi?
Sonunda "SONUÇ: hepsi doğru" yazmalı. Yardımcılar: yerel-ortak/dogrula_ortak.py
"""
import json
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
from dogrula_ortak import (D, kontrol, tek_sik, yargi, dagilim, sayfa_oku, sayfa_isaretleri_ayni,  # noqa: E402
                           meclis_hukumleri, ogretmen_metinleri, anahtar_izgarasi, kendini_dene_ayni, sifreli_kapi_ayni,
                           celdirici_ayni, robot_ayni, katla_ayni, uc_boyut_resimleri)
import infografik_unite as IU  # noqa: E402  (çizimdeki veriler: spektrum çizgileri, kıssa grafiği, enerji düzeyleri)

META = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
SABLON = open(os.path.join(BURA, "sablon.html"), encoding="utf-8").read()
HTML = sayfa_oku(__file__)

# ================================================================== DİZİLİM MOTORU
SIRA = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d", "5p", "6s", "4f", "5d", "6p", "7s"]
KAP = {"s": 2, "p": 6, "d": 10, "f": 14}
ORB = {"s": 1, "p": 3, "d": 5, "f": 7}
SEMBOL = {1: "H", 2: "He", 4: "Be", 6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
          16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co",
          28: "Ni", 29: "Cu", 30: "Zn"}
Z_ = {v: k for k, v in SEMBOL.items()}


def dizilim(Z, aufbau_saf=False):
    """{alt kabuk: elektron} Aufbau sırasıyla (sözlük sırası = yazım sırası). Cr ve Cu deneysel istisnaları uygulanır."""
    d, kalan = {}, Z
    for ak in SIRA:
        if kalan == 0:
            break
        k = min(kalan, KAP[ak[1]])
        d[ak] = k
        kalan -= k
    if not aufbau_saf and Z in (24, 29):          # 4s² 3d⁴ → 4s¹ 3d⁵ · 4s² 3d⁹ → 4s¹ 3d¹⁰
        d["4s"] -= 1
        d["3d"] += 1
    return d


def iyon_dizilim(Z, yuk):
    """Katyon: elektronlar en yüksek n'den (aynı n'de önce p, sonra s) verilir; anyon: Aufbau ile eklenir."""
    if yuk <= 0:
        return dizilim(Z - yuk)
    d = dict(dizilim(Z))
    for _ in range(yuk):
        ak = max((a for a, k in d.items() if k), key=lambda a: (int(a[0]), "spdf".index(a[1])))
        d[ak] -= 1
    return {a: k for a, k in d.items() if k}


def yazim(d, kisalt=True):
    """'[Ar] 4s2 3d6' biçiminde (karşılaştırma için düz metin; üst simgeler rakam)."""
    soy = {"[Ne]": dizilim(10), "[Ar]": dizilim(18)}
    if kisalt:
        for ad in ("[Ar]", "[Ne]"):
            c = soy[ad]
            if all(d.get(a, 0) == k for a, k in c.items()):
                kalan = [f"{a}{k}" for a, k in d.items() if a not in c and k]
                return " ".join([ad] + kalan)
    return " ".join(f"{a}{k}" for a, k in d.items() if k)


def yari_dolu(d):
    return sum(k if k <= ORB[a[1]] else 2 * ORB[a[1]] - k for a, k in d.items())


def kuresel(d):
    return all(k in (0, ORB[a[1]], 2 * ORB[a[1]]) for a, k in d.items())


def duzey_sayisi(d):
    return max(int(a[0]) for a, k in d.items() if k)


def degerlik(d):
    n = duzey_sayisi(d)
    v = sum(k for a, k in d.items() if int(a[0]) == n)
    dd = f"{n - 1}d"
    if dd in d and not any(a == f"{n}p" for a in d):   # d dolmaya başlamış (geçiş metali): son s + d
        v += d[dd]
    return v


def hund_uygun(kod):
    """Orbital şeması kodları (ud, u, d, 0): Pauli (≤ 2, zıt) ve Hund (boş varken eşleşme yok, tekler aynı yönlü)."""
    if len(kod) == 1:
        return kod[0] in ("ud", "u", "d", "0")
    tek = [k for k in kod if k in ("u", "d")]
    if "ud" in kod and "0" in kod:
        return False
    return len(set(tek)) <= 1


def pne(A, Z, yuk=0):
    return Z, A - Z, Z - yuk


print("— Dizilim motoru (öz denetim)")
kontrol("O: 1s2 2s2 2p4", yazim(dizilim(8), False) == "1s2 2s2 2p4")
kontrol("K: [Ar] 4s1", yazim(dizilim(19)) == "[Ar] 4s1")
kontrol("Cr: [Ar] 4s1 3d5 (Aufbau'ya göre 4s2 3d4)", yazim(dizilim(24)) == "[Ar] 4s1 3d5" and yazim(dizilim(24, True)) == "[Ar] 4s2 3d4")
kontrol("Cu: [Ar] 4s1 3d10 (Aufbau'ya göre 4s2 3d9)", yazim(dizilim(29)) == "[Ar] 4s1 3d10" and yazim(dizilim(29, True)) == "[Ar] 4s2 3d9")
kontrol("Fe3+: [Ar] 3d5 · Ca2+ ve S2− Ar dizilimi",
        yazim(iyon_dizilim(26, 3)) == "[Ar] 3d5" and iyon_dizilim(20, 2) == dizilim(18) and iyon_dizilim(16, -2) == dizilim(18))
kontrol("katman sığası 2n²: K 2, L 8, M 18, N 32", [sum(KAP[t] for t in "spdf"[:n]) for n in (1, 2, 3, 4)] == [2, 8, 18, 32])
kontrol("n. düzeyde n² orbital: 1, 4, 9, 16", [sum(ORB[t] for t in "spdf"[:n]) for n in (1, 2, 3, 4)] == [1, 4, 9, 16])

# ================================================================== DURAKLAR (görev, hızlı görev, kavram görevi)
print("— Duraklar")
# 1. durak: Thomson modelinde olanlar
THOMSON = {"elektron": True, "çekirdek": False, "(+) yük": True, "katman": False}
kontrol("1. durak hızlı: Thomson'da 2 öğe (elektron, (+) yük)", sum(THOMSON.values()) == 2)
# 2. durak: Na katmanları, L katmanı
na = dizilim(11)
katman = {n: sum(k for a, k in na.items() if int(a[0]) == n) for n in (1, 2, 3)}
kontrol(f"2. durak görev: Na K/L/M = {katman}", katman == {1: 2, 2: 8, 3: 1})
kontrol("2. durak hızlı: L katmanı en çok 2·2² = 8", 2 * 2 ** 2 == 8)
# 3. durak: n = 3 ve 3d
kontrol("3. durak görev: n = 3 → 3s 3p 3d, 9 orbital, 18 e", (1 + 3 + 5, 2 * 9) == (9, 18) and 3 ** 2 == 9 and 2 * 3 ** 2 == 18)
kontrol("3. durak kavram görevi: 3d en çok 5 × 2 = 10", ORB["d"] * 2 == 10)
# Rydberg ile hidrojenin görünür çizgileri (nm) → çizimdeki çizgiler
R = 1.09678e7
balmer = [round(1e9 / (R * (1 / 4 - 1 / n ** 2))) for n in (6, 5, 4, 3)]
kontrol(f"H görünür çizgileri (Rydberg) {balmer} == çizim {IU.CIZGI['H']}", tuple(balmer) == IU.CIZGI["H"])
kontrol("Na sarı çizgisi 589 nm, Li 610 ve 671 nm", IU.CIZGI["Na"] == (589,) and IU.CIZGI["Li"] == (610, 671))
var = [el for el, cz in IU.CIZGI.items() if set(cz) <= set(IU.LAMBA)]
artan = set(IU.LAMBA) - set().union(*[set(IU.CIZGI[e]) for e in var])
kontrol(f"3. durak hızlı (lamba): {var}, açıklanmayan çizgi yok", var == ["H", "Na"] and not artan)
# 4. durak: Cu2+, X3+, izo eşleştir
kontrol("4. durak görev: 63Cu2+ → p 29, n 34, e 27", pne(63, 29, 2) == (29, 34, 27))
kontrol("4. durak hızlı: X3+ 10 e → Z = 13", 10 + 3 == 13)


def izo(a, b):
    """a, b: (A, Z, yük) → ilişkiler kümesi."""
    (A1, Z1, q1), (A2, Z2, q2) = a, b
    p1, n1, e1 = pne(A1, Z1, q1)
    p2, n2, e2 = pne(A2, Z2, q2)
    r = set()
    if Z1 == Z2 and A1 != A2:
        r.add("izotop")
    if n1 == n2 and Z1 != Z2:
        r.add("izoton")
    if A1 == A2 and Z1 != Z2:
        r.add("izobar")
    if Z1 != Z2 and e1 == e2 and iyon_dizilim(Z1, q1) == iyon_dizilim(Z2, q2):   # farklı tanecikler
        r.add("izoelektronik")
    return r


esles = {"a": izo((23, 11, 1), (20, 10, 0)), "b": izo((14, 6, 0), (14, 7, 0)), "c": izo((39, 19, 0), (40, 20, 0)), "d": izo((16, 8, 0), (18, 8, 0))}
kontrol(f"4. durak eşleştir {esles}", esles == {"a": {"izoelektronik"}, "b": {"izobar"}, "c": {"izoton"}, "d": {"izotop"}})
kontrol("izo kutuları: 12C–14C izotop, 14C–16O izoton (n 8), 40Ar–40Ca izobar, O2−/Na+/Ne izoelektronik",
        izo((12, 6, 0), (14, 6, 0)) == {"izotop"} and izo((14, 6, 0), (16, 8, 0)) == {"izoton"} and izo((40, 18, 0), (40, 20, 0)) == {"izobar"}
        and "izoelektronik" in izo((16, 8, -2), (23, 11, 1)) and "izoelektronik" in izo((23, 11, 1), (20, 10, 0)))
kontrol("iyon çizimi: Na 11p 11e → Na+ 10e; Cl 17p 17e → Cl− 18e", pne(23, 11, 1)[2] == 10 and pne(35, 17, -1)[2] == 18)
# 5. durak: S, K, P, Al, Ti
s_ = dizilim(16)
kontrol("5. durak görev: S 1s2 2s2 2p6 3s2 3p4, 3p'de 2 yarı dolu", yazim(s_, False) == "1s2 2s2 2p6 3s2 3p4" and yari_dolu({"3p": 4}) == 2)
kontrol("5. durak görev: K …3p6 4s1; üst simge toplamları 16 ve 19", yazim(dizilim(19), False).endswith("3p6 4s1") and sum(s_.values()) == 16 and sum(dizilim(19).values()) == 19)
kontrol("5. durak soy gaz: Al [Ne] 3s2 3p1 · Ti [Ar] 4s2 3d2", yazim(dizilim(13)) == "[Ne] 3s2 3p1" and yazim(dizilim(22)) == "[Ar] 4s2 3d2")
kontrol("5. durak hızlı: P'de 3 yarı dolu orbital", yari_dolu(dizilim(15)) == 3)
# 6. durak: tablo, Ca2+, Cl/Cl−, Si, kavram örnekleri
kontrol("6. durak kavram: S değerlik 6 · Ti değerlik 4", degerlik(dizilim(16)) == 6 and degerlik(dizilim(22)) == 4)
kontrol("6. durak görev: Ca [Ar] 4s2 · Ca2+ 1s2 2s2 2p6 3s2 3p6 (Ar ile izoelektronik)",
        yazim(dizilim(20)) == "[Ar] 4s2" and yazim(iyon_dizilim(20, 2), False) == "1s2 2s2 2p6 3s2 3p6" and iyon_dizilim(20, 2) == dizilim(18))
kontrol("6. durak kavram görevi: Cl simetrik değil, Cl− simetrik", not kuresel(dizilim(17)) and kuresel(iyon_dizilim(17, -1)))
kontrol("6. durak hızlı: Si değerlik 4, yarı dolu 2", (degerlik(dizilim(14)), yari_dolu(dizilim(14))) == (4, 2))
kontrol("Cr: 6 yarı dolu, simetrik · Cu: 1 yarı dolu, simetrik", (yari_dolu(dizilim(24)), kuresel(dizilim(24)), yari_dolu(dizilim(29)), kuresel(dizilim(29))) == (6, True, 1, True))
# 6. durak tablosu sayfadan okunur ve hesapla karşılaştırılır
if HTML:
    for el in ("P", "Cl", "Ca", "Mn", "Fe"):
        m = re.search(rf'<tr data-atom="{el}">(.*?)</tr>', HTML, re.S)
        hucre = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<td>(.*?)</td>", m.group(1), re.S)]
        d = dizilim(Z_[el])
        son = list(d.items())[-1]
        orb = re.search(r'data-orb="([^"]+)"', m.group(1)).group(1).split(",")
        beklenen_orb = (["ud"] * max(0, son[1] - ORB[son[0][1]]) + ["u"] * (ORB[son[0][1]] - max(0, son[1] - ORB[son[0][1]])))[:ORB[son[0][1]]] if son[1] >= ORB[son[0][1]] else ["u"] * son[1] + ["0"] * (ORB[son[0][1]] - son[1])
        kontrol(f"tablo {el}: dizilim '{hucre[1]}' · şema {orb} · değerlik {hucre[3]} · yarı dolu {hucre[4]} · simetri {hucre[5]}",
                hucre[1].replace(" ", "") == yazim(d).replace(" ", "") and orb == beklenen_orb and hund_uygun(orb)
                and int(hucre[3].split()[0]) == degerlik(d) and int(hucre[4]) == yari_dolu(d) and (hucre[5] == "var") == kuresel(d))

# ================================================================== MECLİS
print("— Meclis")
MECLIS = {"M1": ("Yusuf", 3), "M2": ("Elif", 2), "M3": ("Pamuk", 2), "M4": ("Elif", 3)}
kontrol("M1: Co2+ nötron = 59 − 27 = 32 (yazılan 34 hatalı satır 3)", pne(59, 27, 2)[1] == 32 and 59 - (27 - 2) == 34)
kontrol("M2: P3− e = 18 (yazılan 15 − 3 = 12 hatalı satır 2)", pne(31, 15, -3)[2] == 18)
kontrol("M3: Ca [Ar] 4s2 (3d2 hatalı satır 2)", yazim(dizilim(20)) == "[Ar] 4s2")
kontrol("M4: Cr 6 yarı dolu (5 hatalı satır 3; satır 2 doğru)", yari_dolu(dizilim(24)) == 6 and yazim(dizilim(24)) == "[Ar] 4s1 3d5")

# ================================================================== KISSALAR
print("— Kıssalar")
Y3 = {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}
Y5 = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}
k1 = yargi({"I": pne(60, 27)[1] == 33, "II": pne(131, 53)[1] > 2 * 53, "III": pne(99, 43)[1] == 56})
K = {"K1": tek_sik("Kıssa 1 (nükleer tıp)", Y3, lambda v: v == k1, "D")}
# Kıssa 2: alev testi — Rutherford modelinde enerji düzeyi yok (MODEL tablosu, aşağıda da kullanılır)
MODEL = {"Dalton": {"kütle korunur", "sabit oran", "atomlar korunur", "elementler farklı"},
         "Thomson": {"elektron", "(+) yük düzgün", "nötr", "bölünebilir"},
         "Rutherford": {"elektron", "çekirdek", "boşluk", "bölünebilir"},
         "Bohr": {"elektron", "çekirdek", "katman", "tek elektronlu spektrum"},
         "Modern": {"elektron", "çekirdek", "orbital", "belirsizlik"}}
k2 = yargi({"I": True, "II": True, "III": "katman" in MODEL["Rutherford"]})
K["K2"] = tek_sik("Kıssa 2 (alev testi)", Y5, lambda v: v == k2, "C")
T = {ad: dict(zip("pne", v)) for ad, v in IU.KISSA_TANECIK.items()}
k3 = {"A": T["K"]["e"] > T["K"]["p"], "B": T["L"]["p"] + T["L"]["n"] == 23,
      "C": len({v["e"] for v in T.values()}) == 1 and len({tuple(sorted(iyon_dizilim(v["p"], v["p"] - v["e"]).items())) for v in T.values()}) == 1,
      "D": T["M"]["p"] == T["M"]["e"], "E": T["L"]["n"] == T["M"]["n"] and T["L"]["p"] != T["M"]["p"]}
K["K3"] = tek_sik("Kıssa 3 (grafik, yanlış olan)", k3, lambda v: v is False, "E")
c14, n14 = pne(14, 6), pne(14, 7)
k4 = {"A": False, "B": (c14[1], n14[1]) == (8, 7), "C": False, "D": "izotop" in izo((14, 6, 0), (14, 7, 0)), "E": n14[0] < c14[0]}
K["K4"] = tek_sik("Kıssa 4 (C-14 bozunması, doğru olan)", k4, lambda v: v is True, "B")
kontrol("C-14 yarılanma süresi metinde yaklaşık 5730 yıl", "5730 yılda yarıya" in SABLON)

# ================================================================== ANAHTAR MERDİVENİ
print("— Anahtar merdiveni")
e_atom = 18 - 2
kontrol("1: X2− 18 e → p 16, n 18, A 34", (e_atom, e_atom + 2, e_atom + e_atom + 2) == (16, 18, 34))
aday = [Z for Z in range(19, 31) if duzey_sayisi(dizilim(Z)) == 4 and list(dizilim(Z).items())[-1] == ("3d", 5) and yari_dolu(dizilim(Z)) == 6]
kontrol(f"2: 4 düzey, d5 ile biter, 6 yarı dolu → {aday} (Cr), değerlik {degerlik(dizilim(24))}", aday == [24] and degerlik(dizilim(24)) == 6)
p3 = [p for p in range(1, 40) if p + (p - 3) + (p - 3 + 7) == 79]
kontrol(f"3: Y3+ toplam 79 → p {p3}, A 56, Fe [Ar] 4s2 3d6", p3 == [26] and 26 + (26 - 3 + 7) == 56 and yazim(dizilim(26)) == "[Ar] 4s2 3d6")

# ================================================================== BÜYÜK İMTİHAN
print("— Büyük İmtihan")
I = {}
I["I1"] = tek_sik("İ1 Dalton açıklayamaz", {"A": "kütle korunur", "B": "sabit oran", "C": "izotop", "D": "atomlar korunur", "E": "elementler farklı"},
                  lambda v: v not in MODEL["Dalton"], "C")
I["I2"] = tek_sik("İ2 geri dönüş = çekirdek", {"A": "çekirdek", "B": "boşluk", "C": "katman", "D": "bölünemez", "E": "belirsizlik"},
                  lambda v: v == "çekirdek", "A")
Y3b = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}
I["I3"] = tek_sik("İ3 Bohr yargıları (II: çıkarken soğurur)", Y3b, lambda v: v == yargi({"I": "katman" in MODEL["Bohr"], "II": False, "III": "tek elektronlu spektrum" in MODEL["Bohr"]}), "D")
I["I4"] = tek_sik("İ4 27Al3+ p n e", {"A": (13, 14, 13), "B": (13, 14, 10), "C": (13, 27, 10), "D": (14, 13, 10), "E": (13, 14, 16)},
                  lambda v: v == pne(27, 13, 3), "B")
v = {"1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 6, "4s": 2, "3d": 3}
kontrol("İ5 dizilim 23 elektron = V", sum(v.values()) == 23 and v == dizilim(23))
I["I5"] = tek_sik("İ5 V yargıları", Y5, lambda s_: s_ == yargi({"I": sum(v.values()) == 23, "II": yari_dolu(v) == 3, "III": kuresel(v)}), "C")
I["I6"] = tek_sik("İ6 simetri göstermeyen", {"A": 15, "B": 24, "C": 12, "D": 8, "E": 30}, lambda z: not kuresel(dizilim(z)), "D")
I["I7"] = tek_sik("İ7 Thomson için yanlış", {"A": "elektron", "B": "nötr", "C": "(+) yük düzgün", "D": "bölünebilir", "E": "çekirdek"},
                  lambda s_: s_ not in MODEL["Thomson"], "E")
I["I8"] = tek_sik("İ8 modern model", {"A": "orbital", "B": "içi dolu küre", "C": "dairesel yörünge", "D": "kesin konum-hız", "E": "(+) yük düzgün"},
                  lambda s_: s_ in MODEL["Modern"], "A")
n4 = {"A": False, "B": (sum(ORB.values()), 2 * sum(ORB.values())) == (16, 32), "C": 2 * 4 ** 2 == 18, "D": False, "E": SIRA.index("4s") > SIRA.index("3d")}
I["I9"] = tek_sik("İ9 n = 4", n4, lambda s_: s_ is True, "B")
I["I10"] = tek_sik("İ10 izotop çifti", {"A": ((40, 18, 0), (40, 20, 0)), "B": ((14, 6, 0), (16, 8, 0)), "C": ((24, 12, 2), (20, 10, 0)),
                                         "D": ((39, 19, 0), (40, 20, 0)), "E": ((1, 1, 0), (2, 1, 0))}, lambda c: "izotop" in izo(*c), "E")
cu = dizilim(29)
cu_s = {"A": yazim(cu) == "[Ar] 4s2 3d9", "B": yazim(cu) == "[Ar] 4s1 3d10" and kuresel(cu), "C": not kuresel(cu), "D": yari_dolu(cu) == 2, "E": duzey_sayisi(cu) == 3}
I["I12"] = tek_sik("İ12 Cu", cu_s, lambda s_: s_ is True, "B")
# İ11: şemalar sayfadan okunur
if HTML:
    blok = HTML[HTML.index('data-soru="I11"'):HTML.index('data-soru="I12"')]
    sema = dict((h, o.split(",")) for h, o in re.findall(r'<b>([A-E])</b><span>\d[spdf] <svg class="orb" viewBox="[^"]+" data-orb="([^"]+)"', blok))
    kontrol(f"İ11 şemalar sayfadan okundu {sorted(sema)}", sorted(sema) == list("ABCDE"))
    I["I11"] = tek_sik("İ11 Hund'a aykırı şema", sema, lambda k: not hund_uygun(k), "D")
else:
    I["I11"] = "D"
dagilim([I[f"I{i}"] for i in range(1, 13)])

# ================================================================== ÜSTAD
print("— Üstad soruları")
TAB = {"X": (17, 18, 18), "Y": (17, 20, 17), "Z": (18, 22, 18), "T": (20, 20, 18)}
iz_ = {k: (p + n, p, p - e) for k, (p, n, e) in TAB.items()}
u1 = yargi({"I": "izotop" in izo(iz_["X"], iz_["Y"]),
            "II": "izoelektronik" in izo(iz_["X"], iz_["Z"]) and "izoelektronik" in izo(iz_["Z"], iz_["T"]),
            "III": "izoton" in izo(iz_["Y"], iz_["Z"]), "IV": "izobar" in izo(iz_["Z"], iz_["T"])})
U = {"U1": tek_sik("Ü1 tablo", {"A": {"I", "II"}, "B": {"II", "III"}, "C": {"I", "II", "IV"}, "D": {"I", "III", "IV"}, "E": {"I", "II", "III", "IV"}},
                   lambda s_: s_ == u1, "C")}
Zx = [Z for Z in range(19, 31) if yazim(iyon_dizilim(Z, 3)) == "[Ar] 3d5"]
u2 = yargi({"I": Zx == [26], "II": yari_dolu(dizilim(26)) == 4, "III": kuresel(iyon_dizilim(26, 3))})
U["U2"] = tek_sik("Ü2 X3+ [Ar] 3d5", Y3b, lambda s_: s_ == u2, "E")
E = IU.ENERJI_EV
kontrol("Ü3 düzey enerjileri −13,6/n² (yuvarlanmış)", all(abs(E[n] - (-13.6 / n ** 2)) < .006 for n in E))
fark = {k: E[a] - E[b] for k, (a, b) in IU.GECIS.items()}           # > 0: ışık yayılır (inen), < 0: soğurulur
u3 = yargi({"I": all(fark[k] > 0 for k in "abc"), "II": fark["d"] < 0, "III": fark["b"] > fark["a"]})
U["U3"] = tek_sik("Ü3 enerji düzeyleri", Y3b, lambda s_: s_ == u3, "C")
kontrol(f"Ü3 karalama: a 2,55 eV · b 1,89 eV", (round(fark["a"], 2), round(fark["b"], 2)) == (2.55, 1.89))
px = [p for p in range(1, 30) if p + 16 + (p + 2) == 50]
zy = px[0] + 2 + 3 if px else None
u4 = {"A": "[Ar] 3d3", "B": "[Ar] 4s2 3d1", "C": "[Ar] 4s1 3d2", "D": "[Ar] 4s2 4p1", "E": "[Ne] 3s2 3p6 3d3"}
U["U4"] = tek_sik(f"Ü4 X p={px}, Y Z={zy}", u4, lambda s_: s_ == yazim(dizilim(zy)), "B")


def sema_temel(Z, semalar):
    """Sayfadaki orbital şemaları temel hâl mi? (dizilim ve Hund)"""
    d = dizilim(Z)
    for ak, kod in semalar.items():
        e = sum(2 if k == "ud" else (1 if k in ("u", "d") else 0) for k in kod)
        if e != d.get(ak, 0) or not hund_uygun(kod):
            return False
    return sum(sum(2 if k == "ud" else (1 if k in ("u", "d") else 0) for k in kod) for kod in semalar.values()) == Z


if HTML:
    blok = HTML[HTML.index('data-soru="U5"'):HTML.index('data-soru="U6"')]
    satirlar = re.findall(r"<li><b>(I+)\.</b><sub>(\d+)</sub>[A-Z][a-z]?:(.*?)</li>", blok, re.S)
    u5 = {}
    for rom, z, ic in satirlar:
        sem = {ak: o.split(",") for ak, o in re.findall(r'(\d[spdf]) <svg class="orb" viewBox="[^"]+" data-orb="([^"]+)"', ic)}
        u5[rom] = sema_temel(int(z), sem)
    kontrol(f"Ü5 şemalar sayfadan: {u5}", len(u5) == 3)
    U["U5"] = tek_sik("Ü5 temel hâl olanlar", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"II", "III"}},
                      lambda s_: s_ == yargi(u5), "A")
else:
    U["U5"] = "A"
cu1, zn2, ni = iyon_dizilim(29, 1), iyon_dizilim(30, 2), dizilim(28)
u6 = yargi({"I": cu1 == zn2, "II": ni == cu1, "III": kuresel(cu1) and kuresel(zn2)})
U["U6"] = tek_sik("Ü6 Cu+, Zn2+, Ni", Y3b, lambda s_: s_ == u6, "D")

# ================================================================== SAYFA İŞARETLERİ
print("— Sayfa işaretleri")
if HTML:
    sayfa_isaretleri_ayni(HTML, {**I, **K, **U})
    kontrol(f"meclis hükümleri {meclis_hukumleri(HTML)} == {MECLIS}", meclis_hukumleri(HTML) == MECLIS)
    izg = anahtar_izgarasi(HTML)
    kontrol(f"anahtar ızgarası {izg}", izg == {i: I[f"I{i}"] for i in range(1, 13)})
    etiket = re.findall(r"<i>(\d+)</i><b>[A-E]</b><small>(\d)\. durak</small>", HTML)
    kontrol("anahtar ızgarası durak etiketleri 1–6, 1–6", [int(d) for _, d in etiket] == [1, 2, 3, 4, 5, 6] * 2)
    cev = HTML[HTML.index('class="cozumler'):]
    gruplar = re.findall(r'<div class="grup"><h4>(.*?)</h4>(.*?)</div>', cev, re.S)
    g = {ad: dict((int(n_), h) for n_, h in re.findall(r"<b>(\d+) · ([A-E])</b>", ic)) for ad, ic in gruplar}
    kontrol("çözümler · İmtihan harfleri", g.get("Büyük İmtihan") == {i: I[f"I{i}"] for i in range(1, 13)})
    kontrol("çözümler · Kıssa harfleri", g.get("Kıssalar") == {i: K[f"K{i}"] for i in range(1, 5)})
    kontrol("çözümler · Üstad harfleri", g.get("Üstad soruları") == {i: U[f"U{i}"] for i in range(1, 7)})
    hz = re.search(r'yan-anahtar.*?</div>', cev, re.S).group(0)
    ck = re.findall(r'<span class="ck">(\d) ([A-E])</span>', hz)
    kontrol("hızlı anahtar · Kıssa", ck[:4] == [(str(i), K[f"K{i}"]) for i in range(1, 5)])
    kontrol("hızlı anahtar · Üstad", ck[4:] == [(str(i), U[f"U{i}"]) for i in range(1, 7)])
    kontrol("hızlı anahtar · Meclis", re.findall(r'<span class="ck">\d (Yusuf|Elif|Pamuk)</span>', hz) == [v_[0] for v_ in MECLIS.values()])
    kontrol("çözümler · Meclis kişileri ve satırları",
            re.findall(r"<b>Meclis (\d) · (\w+) \((\d)\)</b>", cev) == [(k_[1], v_[0], str(v_[1])) for k_, v_ in MECLIS.items()])
    ogr = ogretmen_metinleri(HTML)
    for beklenen in ("2", "8", "10", "13", "3", "4 · 2", "H ve Na", "K 2 · L 8 · M 1", "deney (yeni gözlem)",
                     "a izoelektronik · b izobar · c izoton · d izotop", "Al: [Ne] 3s2 3p1 · Ti: [Ar] 4s2 3d2", "Cl: p5, yok · Cl−: p6, var",
                     "n = A − Z", "n = 59 − 27 = 32", "anyon e− alır", "e = 15 + 3 = 18", "4s önce dolar", "Ca: [Ar] 4s2", "4s1 eksik",
                     "6 yarı dolu orbital", "A = 16 + 18 = 34", "Z = 24 · değerlik 1 + 5 = 6", "A = 56 · Fe: [Ar] 4s2 3d6"):
        kontrol(f"öğretmen metni var: {beklenen}", any(beklenen in o.replace(" (kükürdün 34S izotopu)", "") for o in ogr))
    kontrol("her cevap kutusunda öğretmen metni (6 durak köşesi + 3B köşesi)", HTML.count('<div class="cevap-kutu">CEVABIN:<span class="ogr">') == 7)
    kontrol("meclis NEDEN çizgileri ≤ 14 harf", all(len(re.sub(r"<[^>]+>", "", n_)) <= 14 for n_ in
                                                   re.findall(r'NEDEN\?<span class="cizgili"><span class="ogr">(.*?)</span></span>', HTML)))

# ================================================================== AKÇE
print("— Akçe")


def bolum(n_):
    return re.search(rf'<section class="sayfa s{n_}\b.*?</section>', SABLON, re.S).group(0)


def bolumler(ss):
    return "".join(bolum(n_) for n_ in ss)


def ana_kisim(n_):
    """Sayfanın <main>'den sonrası (levha çipi sayılmaz; alt banttaki .kose-ic kutuları sayılır)."""
    t_ = bolum(n_)
    return t_[t_.index("<main"):]


CIP = r'<span class="cip akce">\+(\d+)(?: akçe)?</span>'
for d in META["duraklar"]:
    t = bolum(d["sayfa"])
    ana = "".join(ana_kisim(n_) for n_ in d["sayfalar"])
    cipler = [int(v_) for v_ in re.findall(CIP, ana)]
    hazine = len(re.findall(r"\{\{hazine\|H\d+\}\}", ana)) * 10
    kontrol(f"{d['no']}. durak (s.{d['sayfalar']}): {cipler} + hazine {hazine} = {d['akce']}", sum(cipler) + hazine == d["akce"])
    kontrol(f"{d['no']}. durak levhasında +{d['akce']} akçe ve yer adı", f'+{d["akce"]} akçe' in t[:t.index("<main")] and d["yer"] in t[:t.index("<main")])
    kontrol(f"{d['no']}. durağın hazine kartları meta ile aynı",
            sorted(re.findall(r"\{\{hazine\|(H\d+)\}\}", ana)) == sorted(h["kod"] for h in META["hazine"] if h["durak"] == d["no"]))
duraklar = sum(d["akce"] for d in META["duraklar"])
kontrol("duraklar 100 + 5 × 120 = 700", duraklar == 700 and [d["akce"] for d in META["duraklar"]] == [100] + [120] * 5)
kontrol("Hülasa (s.16): muhasebe 6 satır = +40", "6 satır = +40 akçe" in bolum(16) and bolum(16).count("{{cay|0|b}}{{cay|0|b}}{{cay|0|b}}") == 6)
import katla_unite as KU  # noqa: E402
kat = 10 * len(KU.KATLA_CUMLE)
karma = sum(int(v_) for v_ in re.findall(CIP, bolum(18)))
kontrol(f"katla (s.17) {len(KU.KATLA_CUMLE)} tahmin × 10 = {kat} · karma (s.18) {karma} = 60 + 30 + 30 + 40", (kat, karma) == (40, 160))
mec = sum(int(v_) for v_ in re.findall(r'<span class="cip akce">\+(\d+)</span>', bolum(19)))
kis = sum(int(v_) for v_ in re.findall(r'<span class="cip akce">\+(\d+)</span>', bolum(20)))
anh = 40 * bolum(21).count('<div class="kart merdiven">')
imt = sum(int(v_) for n_ in (22, 23) for v_ in re.findall(r'<span class="cip akce">\+(\d+)</span>', bolum(n_)))
kontrol(f"yan yollar: meclis {mec}, kıssa {kis}, anahtar {anh} = 120 + 120 + 120", (mec, kis, anh) == (120, 120, 120))
kontrol(f"imtihan 12 × 25 = {imt}", imt == 300)
toplam = duraklar + 40 + kat + karma + mec + kis + anh + imt
kontrol(f"toplam akçe {toplam} == 1600 == meta.akce_toplam; s.1 çipinde de 1600",
        toplam == 1600 == META["akce_toplam"] and re.search(r"</svg> ?1600 akçe", HTML or "") is not None)
defter = [int(v_) for v_ in re.findall(r'<td class="n">(\d+)</td>', bolum(26))]
kontrol(f"final defteri {defter}: kalemler toplamı = TOPLAM = 1600", sum(defter[:-1]) == defter[-1] == 1600 and defter[6:9] == [40, 40, 160])
kontrol("defter durak satırları meta ile aynı (akçe ve yer)", defter[:6] == [d["akce"] for d in META["duraklar"]]
        and all(f"{d['no']}. durak · {d['yer']}" in bolum(26) for d in META["duraklar"]))
kur = open(os.path.join(BURA, "kur.py"), encoding="utf-8").read()
cubuk = [int(v_) for v_ in re.findall(r"^\s+\d+: \('.*?', '.*?', (\d+)\),", kur, re.M)]
once_ = [0, 0, 50, 100, 130, 220, 280, 340, 340, 340, 400, 460, 520, 580, 640, 700, 740, 780, 940, 1060, 1180, 1300, 1450, 1600, 1600, 1600]
sayfa_cip = {n_: sum(int(v_) for v_ in re.findall(CIP, ana_kisim(n_) if "<main" in bolum(n_) else bolum(n_))) + 10 * len(re.findall(r"\{\{hazine\|H\d+\}\}", bolum(n_)))
             for n_ in range(1, 27)}
sayfa_cip[16] = 40                     # muhasebe çipi “6 satır = +40 akçe”
sayfa_cip[17] = kat
sayfa_cip[21] = anh
kontrol(f"sayfa başına akçe birikimi = HUD hesabı ({[sayfa_cip[n_] for n_ in range(1, 27)]})",
        [sum(sayfa_cip[k_] for k_ in range(1, n_)) for n_ in range(1, 27)] == once_)
kontrol(f"HUD çubukları {cubuk}", cubuk == [round(100 * a / 1600) for a in once_])
for esik in ("450+", "900+", "1300+"):
    kontrol(f"Ahilik eşiği {esik} (s.1)", esik in bolum(1))
kontrol("final unvan aralıkları", all(t in bolum(26) for t in ("0–449", "450–899", "900–1299", "1300–1600")))
kontrol("akçe rayı (ünite sürümü) 1600 ölçeğinde, eşikler 450 · 900 · 1300", IU.AKCE_TOPLAM == META["akce_toplam"] == 1600 and IU.AHILIK == (450, 900, 1300)
        and all(f">{a_}</text>" in IU.akce_rayi() for a_ in (450, 900, 1300, 1600)) and "{{info|akce_rayi|ATOM ÜSTADI}}" in bolum(26))
kontrol("Üstad soruları akçe çipi taşımaz", 'cip akce' not in bolum(24))
kontrol("3B sayfaları (s.8–9) bonus: akçe çipi yok", all('cip akce' not in bolum(n_) for n_ in (8, 9)))
kontrol("8 nişan: 6 durak + Kale Kapısı + Üstad Mührü (bonus)", len(META["nisanlar"]) == 8 and META["nisanlar"][-1].get("bonus") is True)

# ================================================================== YENİ DÜZEN (pilot): sayfa yapısı, köşeler, kat, karma, 3B
print("— Yeni düzen: sayfa yapısı ve katlama çiftleri")
from cizim import katla as KC  # noqa: E402
KOSE_ON = [3, 5, 7, 9, 11, 13, 15]
kontrol("26 sayfa (çift), meta ile aynı", SABLON.count('<section class="sayfa s') == 26 == META["sayfa_sayisi"])
for n_ in range(1, 27):
    t_ = bolum(n_)
    kontrol(f"s.{n_}: köşe ön yüzü yalnız tek sayfada, arka yüzü hemen sonraki çift sayfada",
            ("{{kose-on}}" in t_) == (n_ in KOSE_ON) == (f"{{{{alt|{n_}|kose-on}}}}" in t_)
            and ("{{kose-arka|" in t_) == (n_ - 1 in KOSE_ON) == (f"{{{{alt|{n_}|kose-arka}}}}" in t_))
kontrol("kat sayfası s.17 (tek, sağ), karma s.18 arka yüzü (3 sütun)", "{{katla-cumle}}" in bolum(17) and "{{hud|17|kat}}" in bolum(17)
        and all(f'class="kol k{k_}"' in bolum(18) for k_ in (1, 2, 3)))
kontrol("3B açılımı s.8–9: 8 anaglif, meta.uc_boyut ile aynı", sorted(re.findall(r"\{\{ana\|([\w-]+)\}\}", bolum(8) + bolum(9)))
        == sorted(g["ad"] for g in META["uc_boyut"]) and len(META["uc_boyut"]) == 8)
for d in META["duraklar"]:
    t_ = bolumler(d["sayfalar"])
    hb = len(re.findall(r'class="hb hb-(hap|kural|unutma|radar|dikkat|kilit)\b', t_))
    kontrol(f"{d['no']}. durak (s.{d['sayfalar']}): sol + sağ sayfa, 1 Bir bakışta, 1 Kendini dene, 1 köşe, {hb} Hap Bilgi (≥ 3)",
            d["sayfalar"][0] % 2 == 0 and d["sayfalar"][1] == d["sayfalar"][0] + 1 and t_.count('class="bakista"') == 1
            and t_.count('class="kart kendini-dene"') == 1 and t_.count("{{kose-on}}") == 1 and hb >= 3)
for n_ in range(1, 27):
    say = {k_: len(re.findall(rf'class="hb hb-{k_}\b', bolum(n_))) for k_ in ("hap", "kural", "unutma", "radar", "dikkat", "kilit")}
    if sum(say.values()):
        kontrol(f"s.{n_}: Hap Bilgi {sum(say.values())} ≤ 4, aynı türden ≤ 2", sum(say.values()) <= 4 and max(say.values()) <= 2)

print("— Köşeyi katla (cevap = hesap = kart = arka yüz)")
KOSE = {3: ("2", sum(THOMSON.values()) == 2, "2"), 5: ("8", 2 * 2 ** 2 == 8, "8 e^−"), 7: ("H ve Na", var == ["H", "Na"], "H ve Na"),
        9: ("100 000", round(1e-10 / 1e-15) == 100000, "10^5 kat"), 11: ("13", 10 + 3 == 13, "Z = 13"),
        13: ("3", yari_dolu(dizilim(15)) == 3, "3"), 15: ("4 · 2", (degerlik(dizilim(14)), yari_dolu(dizilim(14))) == (4, 2), "4 · 2")}
for n_, (c_, ok_, arka) in KOSE.items():
    m_ = re.search(r"\{\{kose-arka\|CEVAP\|([^|}]+)\|([^}]*)\}\}", bolum(n_ + 1))
    kontrol(f"köşe s.{n_}: {c_} hesapla doğru, kartın öğretmen cevabı aynı, s.{n_ + 1} köşesinde “{arka}”",
            ok_ and f'<span class="ogr">{c_}</span>' in bolum(n_) and m_ is not None and m_.group(1) == arka)
    ana_w = KC.genislik(m_.group(1), 6.2, "baloo")
    alt_w = KC.genislik(m_.group(2), 3.2, "baloo")
    kontrol(f"köşe cevabı s.{n_ + 1} üçgene sığıyor (ana {ana_w:.1f} ≤ 36 · alt {alt_w:.1f} ≤ 30 mm)", ana_w <= 36 and alt_w <= 30)

print("— Kendini dene")
kontrol("KD1: Thomson'da (+) yük dağınık", "(+) yük düzgün" in MODEL["Thomson"])
kontrol("KD2: boşluk ve (+) çekirdek Rutherford modelinde", {"boşluk", "çekirdek"} <= MODEL["Rutherford"])
kontrol(f"KD3: 4→2 {balmer[2]} nm yayılır; 6→2 ({balmer[0]}) < 3→2 ({balmer[3]})", balmer[2] == 486 and balmer[0] < balmer[3])
kontrol("KD4: Mg2+ 10 e · 12C–13C izotop", pne(24, 12, 2)[2] == 10 and izo((12, 6, 0), (13, 6, 0)) == {"izotop"})
kontrol("KD5: Cl [Ne] 3s2 3p5", yazim(dizilim(17)) == "[Ne] 3s2 3p5")
kontrol("KD6: K değerlik 1 · Ar simetrik", degerlik(dizilim(19)) == 1 and kuresel(dizilim(18)))
kontrol("KD7 (3B): bir p orbitali (iki lob) en çok 2 e", KAP["p"] // ORB["p"] == 2)
if HTML:
    kendini_dene_ayni(HTML, {"KD1": ["her yere dağılmış", "modern model"], "KD2": ["atomun büyük kısmı boşluk", "(+) çekirdek"],
                             "KD3": ["yayar (486 nm)", "6’dan 2’ye (410 nm)"], "KD4": ["10", "izotop"],
                             "KD5": ["[Ne] 3s2 3p5", "hayır (Pauli)"], "KD6": ["1", "evet"], "KD7": ["2pz", "2"]})

print("— Kat sayfası: Katla, doğrusu kalsın!")
OLGU = {"C1": not ({"elektron", "çekirdek"} & MODEL["Dalton"]),
        "C2": True,                                       # gözlem: çoğu sapmadan geçti (çizgi roman 2. pano, Görev 2)
        "C3": izo((35, 17, 0), (37, 17, 0)) == {"izotop"} and pne(35, 17)[1] != pne(37, 17)[1],
        "C4": iyon_dizilim(20, 2) == dizilim(18) and dizilim(20)["4s"] == 2}
boy_ = KU.serit_boyu()
for c_ in KU.KATLA_CUMLE:
    gs, go, gg = (KC.genislik(c_[k_], boy_, KU.FONT) for k_ in ("sol", "orta", "sag"))
    kontrol(f'{c_["kod"]}: açık “{KC.duz(KU.acik(c_))}” yanlış, katlı “{KC.duz(KU.katli(c_))}” doğru · sol {gs:.1f} orta {go:.1f} sağ {gg:.1f} mm',
            OLGU[c_["kod"]] and gs <= KC.A_X - KC.GUVEN - 8 and go <= KC.B_X - KC.A_X - 2 * KC.GUVEN and gg <= 202 - KC.B_X - KC.GUVEN
            and KU.katli(c_).endswith(".") and c_["orta"] not in KU.katli(c_))
kontrol("DOĞRU kurdelesinde bölünen harf güvenli (O)", "O" in KC.GUVENLI_HARF)
if HTML:
    katla_ayni(HTML, {c_["kod"]: (KC.duz(KU.katli(c_)), KC.duz(c_["orta"])) for c_ in KU.KATLA_CUMLE})

print("— Karma sayfa")
ilk = next(m_ for m_ in ("Dalton", "Thomson", "Rutherford", "Bohr", "Modern") if "elektron" in MODEL[m_])
RUTH_ACIKLAR = {"çoğu geçer", "geri döner", "(+) yük küçük bölgede", "kütle çekirdekte"}
SK = {"SK1": tek_sik("SK1 ilk elektronlu model", {"N": "Demokritos", "M": "Dalton", "P": "Thomson", "Ç": "Bohr", "Z": "Modern"}, lambda m_: m_ == ilk, "P"),
      "SK2": tek_sik("SK2 Rutherford açıklayamaz", {"C": "çoğu geçer", "Ş": "geri döner", "V": "(+) yük küçük bölgede", "Y": "kütle çekirdekte",
                                                     "R": "elektron neden düşmez"}, lambda g_: g_ not in RUTH_ACIKLAR, "R"),
      "SK3": tek_sik("SK3 n = 2'de orbital", {"B": 2, "O": 4, "D": 6, "G": 8, "H": 9}, lambda v_: v_ == 2 ** 2, "O"),
      "SK4": tek_sik("SK4 X2+ e 18, n 20 → A", {"Ğ": 20, "J": 36, "V": 38, "T": 40, "Ş": 58}, lambda v_: v_ == (18 + 2) + 20, "T"),
      "SK5": tek_sik("SK5 Pauli", {"O": "Pauli", "B": "Aufbau", "D": "Hund", "G": "Bohr", "H": "simetri"}, lambda v_: v_ == "Pauli", "O"),
      "SK6": tek_sik("SK6 küresel simetrik", {"Ç": 14, "N": 15, "J": 13, "Ğ": 16, "V": 17}, lambda z_: kuresel(dizilim(z_)), "N")}
kontrol("Şifreli Kapı: hesaplanan doğru harfler PROTON", "".join(SK.values()) == "PROTON")
import itertools  # noqa: E402
if HTML:
    sifreli_kapi_ayni(HTML, "PROTON")
    kodlar = [re.findall(r"<li(?: data-dogru)?><b>(.)</b>", re.search(rf'data-soru="SK{i_}".*?</ol>', HTML, re.S).group(0)) for i_ in range(1, 7)]
    SESLI = set("AEIİOÖUÜ")
    IZINLI = {"PR", "TR", "KR", "BR", "GR", "DR", "FR", "PL", "KL", "BL", "GL", "FL", "SL", "ST", "SP", "SK"}
    okunur = []
    for dizi in itertools.product(*kodlar):
        w_ = "".join(dizi)
        if w_[:2] not in IZINLI and w_[1] not in SESLI and w_[0] not in SESLI:
            continue
        if re.search(r"[^AEIİOÖUÜ]{3}", w_) or not set(w_) & SESLI:
            continue
        okunur.append(w_)
    kontrol(f"Şifreli Kapı: 5⁶ dizilimden okunabilen yalnız PRO?O? kalıbı ({len(okunur)} dizi; PROTON dışında hiçbiri kelime değil)",
            len(okunur) == 25 and all(w_.startswith("PRO") and w_[4] == "O" for w_ in okunur) and "PROTON" in okunur)
A_, Z_, q_ = 19, 9, -1
e_ = Z_ - q_
tani = {"A": (Z_, A_ - Z_, Z_), "B": (Z_, A_ - e_, e_), "C": (Z_, A_ - Z_, e_), "D": (Z_, A_, e_), "E": (Z_, A_ - Z_, Z_ + q_)}
kontrol(f"Röntgen 19F−: doğru {tani['C']} (C); beş seçenek farklı ve her biri tanıdaki hatadan", tani["C"] == pne(19, 9, -1) == (9, 10, 10)
        and len(set(tani.values())) == 5)
lam_ = {n_: round(1e9 / (R * (1 / 4 - 1 / n_ ** 2))) for n_ in (3, 6)}
fark_ = {n_: 13.6 * (1 / 4 - 1 / n_ ** 2) for n_ in (3, 6)}
iddia = {1: True, 2: True, 3: (fark_[6] > fark_[3]) == (lam_[6] > lam_[3]), 4: True}
kontrol(f"Robot: tek hata 3. cümlede (6→2 {lam_[6]} nm < 3→2 {lam_[3]} nm; fark büyüdükçe dalga boyu kısalır)",
        [k_ for k_, v_ in iddia.items() if not v_] == [3])
if HTML:
    celdirici_ayni(HTML, {"CR1": ("C", ", ".join(map(str, tani["C"])))})
    for h_, (p_, n__, e__) in tani.items():
        kontrol(f"Röntgen {h_}: sayfadaki sayılar tanıdaki hatayla aynı", re.search(rf'<b>{h_}</b><span class="say">{p_}, {n__}, {e__}</span>', HTML) is not None)
    robot_ayni(HTML, {"RB1": 3})
M02 = json.load(open(os.path.join(BURA, "..", "..", "02-kimyasal-guvenlik", "uretec", "meta.json"), encoding="utf-8"))
M01 = json.load(open(os.path.join(BURA, "..", "..", "01-gunluk-hayatta-kimya", "uretec", "meta.json"), encoding="utf-8"))
kontrol("Heybe 1 (Yol 2): asit suya — 9/02 H3 ile aynı", any(h_["kod"] == "H3" and "asit → su" in h_["formul"] for h_ in M02["hazine"]))
kontrol("Heybe 2 (Yol 1): pH 9 bazik — 9/01 H3: asidik < 7 < bazik", any(h_["kod"] == "H3" and "bazik" in h_["formul"] for h_ in M01["hazine"]) and 9 > 7)
kontrol("Heybe 3–4: O 2p4 → 2 yarı dolu · M katmanı 2·3² = 18", yari_dolu({"2p": dizilim(8)["2p"]}) == 2 and 2 * 3 ** 2 == 18)
kontrol("Heybe: ters cevaplar", "Cevaplar: asit suya · bazik · 2 · 18" in bolum(18))

print("— 3B")
kontrol("3B: n = 2'de 2s + üç 2p = 4 orbital · alfa 2 p + 2 n, yük +2", 1 + ORB["p"] == 4 and pne(4, 2, 2) == (2, 2, 0))
import uc_unite as UU  # noqa: E402
kontrol("3B alfa levhası: 7 düz + 1 sapan + 1 geri dönen iz; 24 seyrek çekirdek", len(UU.DUZ_IZ) == 7 and len(UU.CEKIRDEKLER) == 24)
if HTML:
    sorun = uc_boyut_resimleri(HTML, os.path.join(BURA, "..", "unite.html"))
    kontrol(f"3B resimleri: dosya var, mm ölçüsü = piksel / 300 dpi {sorun or ''}", not sorun)
    bilgi = json.load(open(os.path.join(BURA, "..", "gorsel", "uc-boyut.json"), encoding="utf-8"))
    bilgi = {k_: v_ for k_, v_ in bilgi.items() if k_ != "sabit"}
    kontrol(f"3B ayrıklık ≤ 3,0 mm, taşma yok ({len(bilgi)} resim)", len(bilgi) == 8 and all(b_["ayriklik_mm"] <= 3.0001 and b_["tasma_mm"] == 0 for b_ in bilgi.values()))
kontrol("palet: meta.json cini-toprak", META.get("palet") == "cini-toprak")
kontrol("Halfeti teknesi: N 1s2 2s2 2p3, tekneler Hund'a uygun, yanlış örnek Hund'a aykırı",
        dizilim(7) == {"1s": 2, "2s": 2, "2p": 3} and sum(len(y_) for _, y_ in IU.TEKNE) == 7
        and all(hund_uygun(list(y_) if len(y_) != 2 else ["ud"]) for _, y_ in IU.TEKNE)
        and not hund_uygun(["ud", "u", "0"]))
kontrol("Dış katman: Mg 2 · 8 · 2, değerlik 2", [sum(k_ for a_, k_ in dizilim(12).items() if int(a_[0]) == n_) for n_ in (1, 2, 3)] == list(IU.DIS_KATMAN[3])
        and degerlik(dizilim(12)) == 2)

# ================================================================== SAYFA GÖNDERMELERİ ve BİLGİLER
print("— Sayfa göndermeleri ve bilgiler")
konu = {2: "Dalton", 4: "Rutherford", 5: "Bohr", 6: "enerji", 9: "3B", 10: "proton", 11: "iyon", 12: "Aufbau",
        13: "Hund", 14: "simetri", 15: "Değerlik", 25: "Cevaplar"}
for n_ in sorted(set(int(v_) for v_ in re.findall(r"\{\{sayfa\|(\d+)\}\}", SABLON))):
    kontrol(f"s.{{{{sayfa|{n_}}}}} → {konu.get(n_)}", n_ in konu and konu[n_] in bolum(n_))
for m_ in META["medeniyet"]:
    kutu = bolum(m_["sayfa"])
    kontrol(f"Medeniyetimizden {m_['ad']} ({m_['yil']}) s.{m_['sayfa']}'de", m_["ad"] in kutu and m_["yil"] in kutu)
kontrol("el-Battânî güneş yılı 365 gün 5 saat 46 dakika 24 saniye", "365 gün 5 saat 46 dakika 24 saniye" in bolum(next(m_["sayfa"] for m_ in META["medeniyet"] if m_["ad"] == "el-Battânî"))
        and "365 gün 5 saat 46 dakika 24 saniye" in json.dumps(META, ensure_ascii=False))
kontrol("model yılları: Dalton 1803–1808, Thomson 1897 · 1904, Rutherford 1911 (deney 1909–1911), Bohr 1913",
        all(t in SABLON for t in ("1803–1808", "1897 · 1904", "1909–1911", "Bohr (1913)", "Rutherford (1911)")))
kontrol("keşif yılları: elektron 1897, proton 1919, nötron 1932", re.search(r"proton \(p\)</td><td>\+1</td><td>≈ 1</td><td>çekirdek</td><td>1919", SABLON)
        and re.search(r"nötron \(n\)</td><td>0</td><td>≈ 1</td><td>çekirdek</td><td>1932", SABLON) and "<td>bulut</td><td>1897" in SABLON)
kontrol("cami/kilise/manastır sahne adı yok", not re.search(r"\{\{sahne\|[^}]*(cami|kilise|manastir|balikli)", SABLON, re.I))

D.sonuc()
