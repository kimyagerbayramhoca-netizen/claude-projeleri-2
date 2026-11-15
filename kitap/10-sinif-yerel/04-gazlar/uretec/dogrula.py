"""Gazlar (yerel · Kapadokya Yolu) — bütün sayısal cevapların ve cevap anahtarının doğrulaması.

Çalıştır:  python3 uretec/dogrula.py
  1. Her görev, hızlı kontrol, tuzak, hızlı görev, meclis, kıssa, anahtar merdiveni, imtihan ve Üstad sorusu yeniden hesaplanır.
  2. Her çoktan seçmeli soruda TEK doğru şık olduğu denetlenir; şık metinleri unite.html'den okunup hesapla karşılaştırılır.
  3. Sayfadaki data-dogru işaretleri, meclis hükümleri ve Cevaplar sayfasındaki anahtar ızgarası hesapla aynı mı?
  4. Akçe muhasebesi: sayfa sayfa toplamlar (HTML'den okunur), ünite toplamı 1400, HUD akçe çubuğu yüzdeleri, ahilik eşikleri.
Sonunda "SONUÇ: hepsi doğru" yazmalı. Yardımcılar: yerel-ortak/dogrula_ortak.py
"""
import json
import math
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
from dogrula_ortak import (D, NA, mk, yakin, kontrol, tek_sik, yargi, sayfa_isaretleri_ayni,  # noqa: E402
                           meclis_hukumleri, anahtar_izgarasi, sayfa_oku, _bloklar)
from dogrula_ortak import dagilim as harf_dagilimi  # noqa: E402

R = 0.082          # L·atm/(mol·K) — kitapta kullanılan değer
V_NSA = 22.4       # L/mol
T = lambda t: t + 273   # noqa: E731  (°C → K)


def yak(a, b, t=1e-6):
    return yakin(a, b, t)


def yuvarla(x, n=2):
    return round(x + 1e-12, n)


# ------------------------------------------------------------------ 1. durak · Erciyes (s.2)
kontrol("Hızlı kontrol: −13 °C = 260 K, 300 K = 27 °C", T(-13) == 260 and 300 - 273 == 27)
kontrol("H1: −73 °C = 200 K", T(-73) == 200)
kontrol("1 atm = 76 cmHg = 760 mmHg", 76 * 10 == 760)


def p_std(h):   # standart atmosfer (troposfer), atm
    return (1 - 2.25577e-5 * h) ** 5.25588


kontrol(f"Kayseri ≈1050 m: ≈0,88 atm ≈67 cmHg ({p_std(1050):.3f} atm, {76 * p_std(1050):.1f} cm)",
        yuvarla(p_std(1050)) == 0.88 and round(76 * p_std(1050)) == 67)
kontrol(f"Erciyes zirvesi ≈3917 m: ≈0,62 atm ≈47 cmHg ({p_std(3917):.3f} atm, {76 * p_std(3917):.1f} cm)",
        yuvarla(p_std(3917)) == 0.61 or yuvarla(p_std(3917)) == 0.62)
kontrol("Erciyes ≈47 cmHg", round(76 * p_std(3917)) == 47)
kontrol("Pamuk: zirvede basınç deniz kıyısının ≈0,6 katı", round(p_std(3917), 1) == 0.6)
kontrol("Görev 1: P_gaz = 67 + 9 = 76 cmHg = 1 atm", 67 + 9 == 76)
kontrol("Görev 1: zirvede h = 76 − 47 = 29 cm (açık kol yüksek)", 76 - 47 == 29)
kontrol("Hızlı görev: 57 cmHg = 570 mmHg = 0,75 atm", 57 * 10 == 570 and yak(57 / 76, 0.75))

# ------------------------------------------------------------------ 2. durak · Göreme (s.3)
kontrol("Hızlı kontrol: T sabit, V yarıya → P 2 katı", yak(1 * 1 / 0.5, 2))
kontrol("Pamuk: 390/300 = 1,3", yak(T(117) / T(27), 1.3))
kontrol("Görev 2: 0,9·2,0 = 0,75·V → 2,4 L", yak(0.9 * 2.0 / 0.75, 2.4))
v3 = 3000 * T(117) / T(27)
kontrol(f"Görev 3: 3900 m³, 900 m³ dışarı ({v3:.1f})", yak(v3, 3900) and yak(v3 - 3000, 900))
kontrol(f"Tuzak: 313/293 ≈ 1,07 ({T(40) / T(20):.4f})", round(T(40) / T(20), 2) == 1.07)
kontrol("Hızlı görev: 2,6·300/260 = 3 L", yak(2.6 * T(27) / T(-13), 3))
kontrol("Charles grafiği: 0 °C'de 22,4 L → 273 °C'de 44,8 L", yak(22.4 * T(273) / T(0), 44.8))
kontrol("Boyle grafiği: P·V = 4 → (1;4) (2;2) (4;1)", all(yak(p * v, 4) for p, v in ((1, 4), (2, 2), (4, 1))))

# ------------------------------------------------------------------ 3. durak · Avanos (s.4)
kontrol("Pamuk: 300 K → 600 K, basınç 2 katı", yak(600 / 300, 2))
kontrol("Görev 4: 1·450/300 = 1,5 atm", yak(1 * T(177) / T(27), 1.5))
v5 = 0.9 * 6 / T(27) * T(-3) / 0.6
kontrol(f"Görev 5 (birleşik): 8,1 L ({v5:.4f})", yak(v5, 8.1))
n_n2 = 11.2 / V_NSA
kontrol("Hızlı görev: 11,2 L N2 = 0,5 mol = 14 g", yak(n_n2, 0.5) and yak(n_n2 * mk("N2"), 14))
kontrol(f"Hızlı görev: 0,5 mol = 3,01·10²³ molekül ({n_n2 * NA:.3e})", yak(n_n2 * NA, 3.01e23))
kontrol("Testiler: 5,6 L = 0,25 mol → He 1 g, N2 7 g, CO2 11 g",
        yak(5.6 / V_NSA, 0.25) and [0.25 * mk(x) for x in ("He", "N2", "CO2")] == [1, 7, 11])
kontrol("Gay-Lussac grafiği: P/T = 1/300 → 450 K'de 1,5 atm", yak(450 / 300, 1.5))

# ------------------------------------------------------------------ 4. durak · Kızılçukur (s.5)
kontrol(f"R = 22,4/273 ≈ 0,082 ({22.4 / 273:.5f})", round(22.4 / 273, 3) == 0.082)
PV = 0.9 * 2.46e6
n1, n2 = PV / (R * T(27)), PV / (R * T(87))
kontrol(f"Görev 6: n1 = 90 000, n2 = 75 000 mol ({n1:.1f}, {n2:.1f})", yak(n1, 90000) and yak(n2, 75000))
kontrol(f"Görev 6: 15 000 mol · 29 = 435 kg ({(n1 - n2) * 29 / 1000:.1f})", yak((n1 - n2) * 29 / 1000, 435))
n7 = 1.23 * 4 / (R * T(27))
kontrol(f"Görev 7: propan 0,2 mol · 44 = 8,8 g ({n7:.4f})", yak(n7, 0.2) and mk("C3H8") == 44 and yak(n7 * 44, 8.8))
kontrol("Hızlı görev: V = 0,4·0,082·300/2,46 = 4 L", yak(0.4 * R * T(27) / 2.46, 4))
kontrol("Hızlı kontrol: düşük P'deki He (0,5 atm) ideale daha yakın", 0.5 < 2 and mk("He") < mk("SO2"))
kontrol("Zarf kesiti: içeride 87 °C, dışarıda 27 °C", T(87) > T(27))

# ------------------------------------------------------------------ 5. durak · Derinkuyu (s.6)
v_oran = math.sqrt(36.5 / 17)
x = 100 * v_oran / (1 + v_oran)
kontrol(f"Görev 8: hız oranı ≈1,47, halka NH3 ucundan ≈59 cm ({v_oran:.4f}, {x:.2f})",
        round(v_oran, 2) == 1.47 and round(x) == 59 and round(100 - x) == 41)
kontrol(f"Görev 9: CO2 NŞA'da ≈1,96 g/L; havanın ≈1,5 katı ({44 / 22.4:.4f}, {44 / 29:.3f})",
        round(44 / 22.4, 2) == 1.96 and round(44 / 29, 1) == 1.5)
kontrol("Görev 10: √(64/16) = 2 → 30/2 = 15 s", yak(math.sqrt(mk("SO2") / mk("CH4")), 2) and 30 / 2 == 15)
kontrol("Tuzak: √(32/2) = 4 kat (16 değil)", yak(math.sqrt(32 / 2), 4))
kontrol("Hızlı görev: 2·32 = 64 g/mol → SO2", 2 * mk("O2") == mk("SO2") == 64)
kontrol("Yoğunluk cetveli: He 4 · CH4 16 · NH3 17 · O2 32 · CO2 44 · SO2 64; hava ≈ 29",
        [mk(f_) for f_ in ("He", "CH4", "NH3", "O2", "CO2", "SO2")] == [4, 16, 17, 32, 44, 64] and
        all(mk(f_) < 29 for f_ in ("He", "CH4", "NH3")) and all(mk(f_) > 29 for f_ in ("O2", "CO2", "SO2")))
kontrol("H12 notu: süre oranı = hız oranının tersi", yak(math.sqrt(64 / 16), 30 / 15))

# ------------------------------------------------------------------ Meclis (s.8): hatalı satır ve doğrusu
kontrol(f"M1: 3·307/290 ≈ 3,18 L ({3 * T(34) / T(17):.4f})", round(3 * T(34) / T(17), 2) == 3.18)
kontrol("M2: 1,2·5 = P·2 → 3 atm", yak(1.2 * 5 / 2, 3))
kontrol(f"M3: 570 mmHg = 0,75 atm; V = 0,15·0,082·300/0,75 = 4,92 L ({0.15 * R * 300 / 0.75:.4f})",
        yak(570 / 760, 0.75) and yak(0.15 * R * 300 / 0.75, 4.92))
kontrol("M4: √(16/4) = 2 kat (4 değil)", yak(math.sqrt(16 / 4), 2))
MECLIS = {"M1": ("Yusuf", 1), "M2": ("Elif", 1), "M3": ("Yusuf", 2), "M4": ("Pamuk", 2)}

# ------------------------------------------------------------------ Kıssalar (s.9)
YS = {"K1": {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}},
      "K2": {"A": {"I"}, "B": {"III"}, "C": {"I", "III"}, "D": {"I", "II"}, "E": {"I", "II", "III"}},
      "K3": {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}}
k1 = yargi({"I": yak(4 * 0.9 / 0.6, 6), "II": yak(4 * 0.9 / 0.8 - 4, 0.5), "III": yak(4 * 0.9 / 0.8, 2 * 4)})
k2 = yargi({"I": mk("C3H8") > 29 > mk("CH4"), "II": round(math.sqrt(44 / 16), 2) == 1.66, "III": mk("C3H8") < mk("CH4")})
egim_x, egim_y = 1.2 / 400, 0.4 / 400        # grafikte 400 K'de X 1,2 atm, Y 0,4 atm (orijinden)
k3 = yargi({"I": True, "II": yak(egim_x / egim_y, 3), "III": yak(egim_y * 300, 0.3)})
P_K4 = {"I": (8 / 4) * R * T(27) / 41, "II": (64 / 32) * R * T(27) / 24.6, "III": (44 / 44) * R * T(127) / 8.2}
kontrol(f"K4: P = 1,2 · 2 · 4 atm {[round(v, 3) for v in P_K4.values()]}",
        [round(v, 3) for v in P_K4.values()] == [1.2, 2.0, 4.0])
sira = ">".join(sorted(P_K4, key=lambda k: -P_K4[k]))
K4_SIK = {"A": "I,II,III", "B": "III,II,I", "C": "II,III,I", "D": "III,I,II", "E": "eşit"}
kissa = {k: tek_sik(k, YS[k], lambda v, s=s: v == s, b) for k, s, b in (("K1", k1, "C"), ("K2", k2, "D"), ("K3", k3, "E"))}
kissa["K4"] = tek_sik("K4", K4_SIK, lambda v: v == ",".join(sorted(P_K4, key=lambda k: -P_K4[k])), "B")
kontrol(f"K4 sıralama III > II > I ({sira})", sira == "III>II>I")

# ------------------------------------------------------------------ Anahtar merdiveni (s.10)
kontrol("Merdiven 1: (1,5·4)/300 = V/400 → 8 L", yak(1.5 * 4 / T(27) * T(127) / 1, 8))
m2 = 1.05 * R * T(127) / 0.82
kontrol(f"Merdiven 2: M = 42 → 14n = 42 → C3H6 ({m2:.4f})", yak(m2, 42) and 42 / 14 == 3 and mk("C3H6") == 42)
kontrol("Merdiven 3: √(M/2) = 24/6 = 4 → M = 32 (O2)", yak(2 * (24 / 6) ** 2, 32) and mk("O2") == 32)

# ------------------------------------------------------------------ Büyük İmtihan (s.11–12)
Y5 = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}
Y5b = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}
I = {}
I["I1"] = tek_sik("I1", {"A": True, "B": False, "C": True, "D": True, "E": True}, lambda v: v is False, "B")   # yanlış olan
I["I2"] = tek_sik("I2", Y5, lambda v: v == yargi({"I": yak(0.75 * 76, 57), "II": yak(0.75 * 760, 570), "III": yak(0.75 * 760, 570)}), "E")
v_i3 = 0.9 * 4 / 1.2
I["I3"] = tek_sik("I3", {"A": 2.4, "B": 2.7, "C": 3, "D": 3.6, "E": 5.3}, lambda v: yak(v, v_i3), "C")
kontrol("I3 çeldirici: doğru orantı sanılırsa 4·1,2/0,9 ≈ 5,3", round(4 * 1.2 / 0.9, 1) == 5.3)
v_i4 = 5 * T(77) / T(-23)
I["I4"] = tek_sik("I4", {"A": 3.6, "B": 5, "C": 6, "D": 7, "E": 10}, lambda v: yak(v, v_i4), "D")
I["I5"] = tek_sik("I5", Y5b, lambda v: v == yargi({"I": True, "II": False, "III": True}), "D")
m_i6 = 8.96 / V_NSA * mk("CH4")
I["I6"] = tek_sik("I6", {"A": 6.4, "B": 4.8, "C": 3.2, "D": 8.96, "E": 16}, lambda v: yak(v, m_i6), "A")
p_i7 = 0.25 * R * T(27) / 2.05
I["I7"] = tek_sik("I7", {"A": 0.75, "B": 1.5, "C": 3, "D": 6, "E": 12}, lambda v: yak(v, p_i7), "C")
I["I8"] = tek_sik("I8", {"A": True, "B": True, "C": True, "D": True, "E": False}, lambda v: v is False, "E")   # yanlış olan


def ideallik(gaz, t, p):   # yüksek T, düşük P, küçük ve apolar tanecik → daha ideal (sıralama ölçütü)
    apolar = gaz in ("He", "CO2")
    return (t, -p, apolar, -mk(gaz))


I9 = {"A": ("He", 273, 0.5), "B": ("He", 0, 2), "C": ("NH3", 273, 0.5), "D": ("CO2", 273, 0.5), "E": ("SO2", 0, 2)}
en_iyi = max(I9, key=lambda k: ideallik(*I9[k]))
I["I9"] = tek_sik("I9", I9, lambda v: v == I9[en_iyi], "A")
m_i10 = 1.96 * V_NSA
I["I10"] = tek_sik("I10", {"A": "CH4", "B": "N2", "C": "O2", "D": "CO2", "E": "SO2"}, lambda v: abs(mk(v) - m_i10) < 0.5, "D")
m_i11 = 16 * 2 ** 2
I["I11"] = tek_sik("I11", {"A": 8, "B": 64, "C": 32, "D": 4, "E": 256}, lambda v: v == m_i11, "B")
vx0, vy0 = 16.8, 5.6                                    # grafikte 0 °C'deki hacimler
I["I12"] = tek_sik("I12", Y5, lambda v: v == yargi({"I": yak(vx0 / vy0, 3), "II": True, "III": yak(vx0 * T(273) / T(0), 25.2)}), "C")
kontrol(f"I12: 273 °C'de V_X = 33,6 L ({vx0 * T(273) / T(0)})", yak(vx0 * T(273) / T(0), 33.6))
ANAHTAR = {int(k[1:]): v for k, v in I.items()}
kontrol(f"İmtihan anahtarı {''.join(ANAHTAR[i] for i in range(1, 13))}", "".join(ANAHTAR[i] for i in range(1, 13)) == "BECDDACEADBC")
harf_dagilimi(ANAHTAR.values())

# ------------------------------------------------------------------ Üstad soruları (s.13)
cikan = 1 - T(7) / T(77)
U = {}
U["U1"] = tek_sik("U1", {"A": 10, "B": 20, "C": 25, "D": 80, "E": 91}, lambda v: yak(v, cikan * 100), "B")
p_u2 = (3 * 2 + 1 * 3) / 5 * T(127) / T(27)
U["U2"] = tek_sik("U2", {"A": 1.8, "B": 2, "C": 2.25, "D": 2.4, "E": 3.6}, lambda v: yak(v, p_u2), "D")
p_gaz = 67 - 7            # gaz kolu 7 cm yüksek → P_gaz < P0
fark = p_gaz - 47         # Erciyes'te açık kol bu kadar alçak (gaz kolu yüksek) ya da yüksek
U3 = {"A": ("gaz", 13), "B": ("acik", 13), "C": ("acik", 7), "D": ("gaz", 7), "E": ("esit", 0)}
U["U3"] = tek_sik("U3", U3, lambda v: v == (("acik" if fark > 0 else "gaz"), abs(fark)), "B")
K, L, Mn = (200, 2), (400, 4), (400, 2)                 # grafikteki (T, V) noktaları: P ∝ T/V
P = {ad: t / v for ad, (t, v) in (("K", K), ("L", L), ("M", Mn))}
u4 = yargi({"I": yak(P["K"], P["L"]), "II": yak(P["M"], 2 * P["K"]), "III": yak(P["M"] / P["L"], 2)})
U["U4"] = tek_sik("U4", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == u4, "E")
mx = 16 * 4
hiz = math.sqrt(4 / mx)
t_he = 40 * hiz
U["U5"] = tek_sik("U5", {"A": (0.25, 10), "B": (1 / 16, 2.5), "C": (4, 160), "D": (0.25, 160), "E": (0.5, 20)},
                  lambda v: yak(v[0], hiz) and yak(v[1], t_he), "A")
u6 = yargi({"I": yak((1 / 16) / (1 / 64), 4), "II": True, "III": yak(1 / 16, 1 / 64)})
U["U6"] = tek_sik("U6", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"II", "III"}}, lambda v: v == u6, "C")

# ------------------------------------------------------------------ akçe muhasebesi
meta = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
AKCE = {2: 100, 3: 150, 4: 150, 5: 150, 6: 150, 7: 40, 8: 120, 9: 120, 10: 120, 11: 150, 12: 150}
kontrol(f"ünite toplamı {sum(AKCE.values())} = meta {meta['akce_toplam']} = 1400", sum(AKCE.values()) == meta["akce_toplam"] == 1400)
kontrol("meta durak akçeleri 100/150/150/150/150", [d["akce"] for d in meta["duraklar"]] == [100, 150, 150, 150, 150])
kontrol("12 hazine kartı, her biri +10 akçe", len(meta["hazine"]) == 12 and all("+10 akçe" in h["not"] for h in meta["hazine"]))
CUBUK = [0, 0, 7, 18, 29, 39, 50, 53, 61, 70, 79, 89, 100, 100, 100]
birikim = [sum(v for k, v in AKCE.items() if k < s) for s in range(1, 16)]
kontrol(f"HUD akçe çubuğu % {CUBUK}", [round(b * 100 / 1400) for b in birikim] == CUBUK)
kontrol("ahilik eşikleri 400 / 800 / 1150 < 1400", 0 < 400 < 800 < 1150 < 1400)

# ------------------------------------------------------------------ sayfadan okuma: işaretler, şık metinleri, akçe, anahtar
html = sayfa_oku(__file__)
if html:
    sayfa_ = {}
    for i, s in enumerate(re.findall(r'<section class="sayfa[^"]*">(.*?)</section>', html, re.S), 1):
        sayfa_[i] = s

    beklenen = {**{f"I{i}": h for i, h in ANAHTAR.items()}, **kissa, **U}
    sayfa_isaretleri_ayni(html, beklenen)
    kontrol(f"meclis hükümleri {meclis_hukumleri(html)}", meclis_hukumleri(html) == MECLIS)
    kontrol(f"Cevaplar anahtar ızgarası {anahtar_izgarasi(html)}", anahtar_izgarasi(html) == ANAHTAR)

    def sik_metni(kod):
        for k, blok in _bloklar(html):
            if k == kod:
                return {h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).replace("%__", "").strip()
                        for h, t in re.findall(r'<div(?: class="sik")?(?: data-dogru)?><b>([A-E])</b>(.*?)</div>', blok, re.S)}
        return {}

    SAYI = {"I3": "2,4 2,7 3 3,6 5,3", "I4": "3,6 5 6 7 10", "I6": "6,4 4,8 3,2 8,96 16", "I7": "0,75 1,5 3 6 12",
            "I11": "8 64 32 4 256", "U1": "%10 %20 %25 %80 %91", "U2": "1,8 2 2,25 2,4 3,6"}
    for kod, bek in SAYI.items():
        okunan = " ".join(sik_metni(kod)[h] for h in "ABCDE")
        kontrol(f"{kod} şıkları sayfada: {okunan}", okunan == bek)
    kontrol("I10 şıkları CH4 N2 O2 CO2 SO2", " ".join(sik_metni("I10")[h] for h in "ABCDE") == "CH4 N2 O2 CO2 SO2")
    kontrol("I9 şıkları He·273·0,5 … SO2·0·2", [sik_metni("I9")[h].replace(" ", "") for h in "ABCDE"] ==
            ["He·273·0,5", "He·0·2", "NH3·273·0,5", "CO2·273·0,5", "SO2·0·2"])
    kontrol("U5 şıkları", [sik_metni("U5")[h] for h in "ABCDE"] ==
            ["1/4 kat · 10 s", "1/16 kat · 2,5 s", "4 kat · 160 s", "1/4 kat · 160 s", "1/2 kat · 20 s"])
    kontrol("K4 şıkları", [sik_metni("K4")[h].replace(" ", "") for h in "ABCDE"] ==
            ["I&gt;II&gt;III", "III&gt;II&gt;I", "II&gt;III&gt;I", "III&gt;I&gt;II", "I=II=III"])
    Y5_METIN = {"Yalnız I": {"I"}, "Yalnız II": {"II"}, "Yalnız III": {"III"}, "I ve II": {"I", "II"}, "I ve III": {"I", "III"},
                "II ve III": {"II", "III"}, "I, II ve III": {"I", "II", "III"}}
    for kod, tablo in (("I2", Y5), ("I5", Y5b), ("I12", Y5), ("K1", YS["K1"]), ("K2", YS["K2"]), ("K3", YS["K3"]),
                       ("U4", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}),
                       ("U6", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"II", "III"}})):
        okunan = {h: Y5_METIN.get(t) for h, t in sik_metni(kod).items()}
        kontrol(f"{kod} yargı şıkları sayfadaki metinle aynı", okunan == tablo)

    # akçe: durak sayfalarında levha dışındaki çipler + 10 × hazine kartı
    def cipler(s):
        govde = s.split('<main class="ic"', 1)[1]
        return [int(x) for x in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', govde)]

    for no in (2, 3, 4, 5, 6):
        s = sayfa_[no]
        hz = s.count('class="hazine"')
        top = sum(cipler(s)) + 10 * hz
        kontrol(f"s.{no} akçe: çipler {cipler(s)} + {hz} hazine = {top} (beklenen {AKCE[no]})", top == AKCE[no])
        lev = re.search(r'<div class="hedef">.*?<span class="cip akce">\+(\d+) akçe</span>', s, re.S)
        kontrol(f"s.{no} levhadaki akçe {lev.group(1) if lev else None}", lev and int(lev.group(1)) == AKCE[no])
    kontrol("s.7 muhasebe +40", "6 satır = +40 akçe" in sayfa_[7])
    kontrol("s.8 meclis 4 × 30", cipler(sayfa_[8]).count(30) == 4 and sum(cipler(sayfa_[8])) == 120)
    kontrol("s.9 kıssa 4 × 30", "4 × 30 = +120 akçe" in sayfa_[9] and cipler(sayfa_[9]).count(30) == 4)
    kontrol("s.10 merdiven 3 × 40", "3 × 40 = +120 akçe" in sayfa_[10])
    kontrol("s.11–12 imtihan 12 × 25", cipler(sayfa_[11]).count(25) + cipler(sayfa_[12]).count(25) == 12)

    # Cevaplar sayfası: çözüm satırları ve hızlı anahtar
    cv = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sayfa_[14]))
    for i, h in ANAHTAR.items():
        kontrol(f"Cevaplar: İmtihan {i} · {h}", f" {i} · {h} " in cv)
    kontrol("Cevaplar: Kıssa 1 C 2 D 3 E 4 B", "Kıssa 1 C 2 D 3 E 4 B" in cv)
    kontrol("Cevaplar: Meclis 1 Yusuf 2 Elif 3 Yusuf 4 Pamuk", "Meclis 1 Yusuf 2 Elif 3 Yusuf 4 Pamuk" in cv)
    for k, h in U.items():
        kontrol(f"Cevaplar: Üstad {k[1]} · {h}", f"{k[1]} · {h}" in cv.split("Üstad soruları", 1)[1])
    for parca in ("57 / 76 = 0,75 atm", "2,6 · 300/260 = 3 L", "14 g · 3,01·10²³", "= 4 L", "64 g/mol", "8 L", "C 3 H 6", "M = 32"):
        kontrol(f"Cevaplar: '{parca}'", parca in cv)

    # Bu yazı tipinde olmayan ya da kalın yazıda Type 3'e düşebilecek simgeler kalın metinde olmasın
    kalin = " ".join(re.findall(r"<b>(.*?)</b>", html, re.S))
    kontrol("kalın metinde ✓ ✗ ★ ☆ → ← yok", not re.search("[✓✗★☆←]", re.sub(r"<[^>]+>", "", kalin)))

D.sonuc()
