#!/usr/bin/env python3
"""Günlük Hayatta Kimya · İznik–Bursa Yolu — doğrulama ve cevap anahtarı denetimi.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Her imtihan, kıssa ve Üstad sorusunun cevabı burada kurallardan YENİDEN çıkarılır (pH sınıflaması, seyreltme,
     organik/anorganik, polimer, nitel/nicel, adil deney çiftleri, disiplin eşleştirmesi) ve TEK doğru şık denetlenir.
  2. Grafik/tablo verileri (mide pH’ı, mor lahana, pH cetveli, deney tabloları) bilgi grafiği modülünden ve sayfadan okunur.
  3. Sayfadaki işaretler (data-soru / data-dogru), şık metinleri, Cevaplar ızgarası ve çözüm satırları hesapla aynı mı?
  4. Akçe muhasebesi (durak çipleri + hazine kartları = levha = meta; toplam 1400; HUD çubuğu).
Yardımcılar: yerel-ortak/dogrula_ortak.py.
"""
import json
import math
import os
import re
import sys
from itertools import combinations, permutations


def _ortak():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


BURA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ortak())
sys.path.insert(0, BURA)
from dogrula_ortak import *  # noqa: E402,F401,F403
from dogrula_ortak import _bloklar  # noqa: E402
import infografik_unite as IU  # noqa: E402

YARGI_SIK = {"A": {"I"}, "B": {"II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}


def ph_sinif(ph):
    return "asidik" if ph < 7 else ("nötr" if ph == 7 else "bazik")


def seyrelt(ph0, adim=200):
    """Saf su eklendikçe pH’ın izlediği yol (25 °C): [H⁺] ya da [OH⁻] seyrelir, suyun kendi iyonları kalır."""
    yol = []
    for k in range(adim + 1):
        f_ = 10 ** (-k / 25)                       # seyrelme çarpanı (1 → 10^-8)
        if ph0 < 7:
            h = 10 ** -ph0 * f_
            h = (h + math.sqrt(h * h + 4e-14)) / 2  # su dengesi: [H⁺]([H⁺] − c) = Kw
            yol.append(-math.log10(h))
        elif ph0 > 7:
            oh = 10 ** -(14 - ph0) * f_
            oh = (oh + math.sqrt(oh * oh + 4e-14)) / 2
            yol.append(14 + math.log10(oh))
        else:
            yol.append(7.0)
    return yol


# organik/anorganik: karbon içerip anorganik sayılan istisnalar (CO, CO₂, H₂CO₃, karbonatlar, bikarbonatlar, HCN)
def organik_mi(f_):
    el = formul(f_)
    if "C" not in el:
        return False
    if f_ in ("CO", "CO2", "H2CO3", "HCN") or "CO3" in f_:
        return False
    return True


MADDE = {  # ad: (organik mi, polimer mi)
    "naylon": (True, True), "PET": (True, True), "nişasta": (True, True), "ipek": (True, True), "selüloz": (True, True),
    "yün": (True, True), "protein": (True, True), "glikoz": (organik_mi("C6H12O6"), False), "NaCl": (organik_mi("NaCl"), False),
    "CO2": (organik_mi("CO2"), False), "NH3": (organik_mi("NH3"), False), "CH4": (organik_mi("CH4"), False),
    "NaHCO3": (organik_mi("NaHCO3"), False)}
DOGAL_POLIMER = {"nişasta", "selüloz", "ipek", "yün", "protein", "pamuk", "DNA"}

# =================================================================== BÜYÜK İMTİHAN
A = {}
# I1: kimyanın konusu (yapı, özellik, etkileşim, dönüşüm) olmayan iş
konu = {"A": "dönüşüm", "B": "özellik", "C": None, "D": "yapı", "E": "yapı"}
A[1] = tek_sik("İmtihan 1", konu, lambda v: v is None, "C")
# I2: bazik çözelti (pH cetveli değerleri)
ph_I2 = {"A": 3.0, "B": 2.2, "C": 3.3, "D": 12.5, "E": 2.0}
A[2] = tek_sik("İmtihan 2", ph_I2, lambda v: ph_sinif(v) == "bazik", "D")
# I3: K 4, L 10, M 7, N 2 — I. N, K’den asidik  II. M nötr  III. L’ye su eklenince pH artar
K, L, Mx, N = 4, 10, 7, 2
d3 = yargi({"I": N < K, "II": ph_sinif(Mx) == "nötr", "III": seyrelt(L)[-1] > L})
A[3] = tek_sik("İmtihan 3", {"A": {"I", "II"}, "B": {"I"}, "C": {"II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}, lambda v: v == d3, "A")
# I4: pH 12’den başlayan seyreltme
y4 = seyrelt(12)
d4 = yargi({"I": ph_sinif(y4[0]) == "bazik", "II": min(y4) < 7, "III": all(b <= a for a, b in zip(y4, y4[1:]))})
A[4] = tek_sik("İmtihan 4", {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "III"}}, lambda v: v == d4, "E")
# I5: madde – kullanım; asetik asit (asit) gider tıkanıklığını (yağ, saç: kuvvetli baz işi) açmaz
ozellik = {"sitrik asit": "asit", "asetik asit": "asit", "NaClO": "baz", "NaHCO3": "baz", "Ca(ClO)2": "baz"}
is_ = {"kireç": "asit", "gider açma": "baz", "ağartma": "baz", "hamur": "baz", "havuz suyu": "baz"}
I5 = {"A": ("sitrik asit", "kireç"), "B": ("asetik asit", "gider açma"), "C": ("NaClO", "ağartma"), "D": ("NaHCO3", "hamur"), "E": ("Ca(ClO)2", "havuz suyu")}
A[5] = tek_sik("İmtihan 5", I5, lambda v: ozellik[v[0]] != is_[v[1]], "B")
# I6: çamaşır suyu + asit → klor gazı (tek güvenli/doğru uyarı)
I6 = {"A": "temizler", "B": "olmaz", "C": "sıcak", "D": "nötr", "E": "klor"}
A[6] = tek_sik("İmtihan 6", I6, lambda v: v == "klor", "E")
# I7: asidik yiyecek ve yüksek sıcaklık geçişi artırır; kısa temas artırmaz (Görev 4 verisiyle tutarlı)
d7 = yargi({"I": True, "II": True, "III": False})
A[7] = tek_sik("İmtihan 7", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == d7, "C")
# I8: araştırılan etken = bağımsız değişken = sıcaklık
A[8] = tek_sik("İmtihan 8", {"A": "sıcaklık", "B": "kütle", "C": "hacim", "D": "kap", "E": "marka"}, lambda v: v == "sıcaklık", "A")
# I9: karbon içerip organik olmayan
I9 = {"A": "CH4", "B": "C2H6O", "C": "C6H12O6", "D": "NaHCO3", "E": "C12H22O11"}
A[9] = tek_sik("İmtihan 9", I9, lambda v: "C" in formul(v) and not organik_mi(v), "D")
# I10: nitel = “var mı?” · nicel = “ne kadar?”
soru10 = {"I": "var mı", "II": "kaç", "III": "var mı"}
d10 = yargi({k: v == "var mı" for k, v in soru10.items()})
A[10] = tek_sik("İmtihan 10", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"II", "III"}}, lambda v: v == d10, "D")
# I11: doğal polimer olmayan
A[11] = tek_sik("İmtihan 11", {"A": "nişasta", "B": "selüloz", "C": "ipek", "D": "yün", "E": "naylon"}, lambda v: v not in DOGAL_POLIMER, "E")
# I12: sıcaklık–tepkime hızı–enerji → fizikokimya
A[12] = tek_sik("İmtihan 12", {"A": "analitik", "B": "fizikokimya", "C": "polimer", "D": "organik", "E": "biyokimya"}, lambda v: v == "fizikokimya", "B")
ANAHTAR = A
dagilim([A[i] for i in range(1, 13)])

# =================================================================== KISSALAR
KS = {}
mv = IU.MIDE_VERI
tepe = max(range(len(mv)), key=lambda i: mv[i][1])
dk1 = yargi({"I": mv[tepe][1] > mv[0][1], "II": max(p for _, p in mv) > 7, "III": all(b[1] <= a[1] for a, b in zip(mv[tepe:], mv[tepe + 1:]))})
KS["K1"] = tek_sik("Kıssa 1", YARGI_SIK, lambda v: v == dk1, "C")
kontrol(f"Kıssa 1: tepe pH {mv[tepe][1]} (karalamada ≈ 3,6)", mv[tepe][1] == 3.6)
dogru_dal = {"asitlik ölçümü": "analitik", "ambalaj filmi": "polimer", "tepkime hızı": "fizikokimya", "koku molekülü": "organik", "vücutta etki": "biyokimya"}
K2 = {"A": ("asitlik ölçümü", "analitik"), "B": ("ambalaj filmi", "polimer"), "C": ("tepkime hızı", "fizikokimya"), "D": ("koku molekülü", "anorganik"), "E": ("vücutta etki", "biyokimya")}
KS["K2"] = tek_sik("Kıssa 2", K2, lambda v: dogru_dal[v[0]] != v[1], "D")
P, R, Sx, Tx = 2, 12.5, 7, 9
yorum3 = {"A": ph_sinif(P) == "asidik", "B": R >= 12, "C": seyrelt(Tx)[-1] < Tx, "D": ph_sinif(Sx) == "nötr", "E": min(seyrelt(R)) < 7}
KS["K3"] = tek_sik("Kıssa 3 (yanlış yorum)", yorum3, lambda v: (v is False), "E")
DENEME_K4 = {1: (20, 50, "parça"), 2: (40, 50, "toz"), 3: (40, 50, "parça"), 4: (20, 100, "parça"), 5: (40, 100, "toz")}


def tek_fark(tablo, etken_i):
    return [(a, b) for a, b in combinations(sorted(tablo), 2)
            if [i for i in range(len(tablo[a])) if tablo[a][i] != tablo[b][i]] == [etken_i]]


KS["K4"] = tek_sik("Kıssa 4", {"A": (1, 2), "B": (1, 3), "C": (2, 3), "D": (1, 4), "E": (4, 5)}, lambda v: v in tek_fark(DENEME_K4, 0), "B")

# =================================================================== ÜSTAD
U = {}
Ku, Lu, Mu, Nu = 3, 5, 9, 12
erisir = lambda p0, hedef: any(abs(p - hedef) < .02 for p in seyrelt(p0, 400))  # noqa: E731
du1 = yargi({"I": Ku == min(Ku, Lu, Mu, Nu) and Nu == max(Ku, Lu, Mu, Nu), "II": erisir(Lu, Mu), "III": erisir(Nu, Mu)})
U["U1"] = tek_sik("Üstad 1", {"A": {"I"}, "B": {"I", "III"}, "C": {"II", "III"}, "D": {"I", "II"}, "E": {"I", "II", "III"}}, lambda v: v == du1, "B")
DENEME_U2 = {1: (4, 160, 30, 2.0), 2: (4, 200, 30, 3.1), 3: (6, 200, 30, 1.5), 4: (6, 160, 60, 1.4)}   # pH, °C, dk, Al
tab = {k: v[:3] for k, v in DENEME_U2.items()}


def etki(etken_i, isaret):
    """Yalnız bu etkenin farklı olduğu bir çift varsa: etken (işaretle) artınca Al artıyor mu?"""
    ciftler = tek_fark(tab, etken_i)
    if not ciftler:
        return False
    return all((DENEME_U2[b][3] - DENEME_U2[a][3]) * (DENEME_U2[b][etken_i] - DENEME_U2[a][etken_i]) * isaret > 0 for a, b in ciftler)


du2 = yargi({"I": etki(1, 1), "II": etki(0, -1), "III": etki(2, 1)})
U["U2"] = tek_sik("Üstad 2", {"A": {"I"}, "B": {"III"}, "C": {"I", "III"}, "D": {"I", "II"}, "E": {"I", "II", "III"}}, lambda v: v == du2, "D")
kontrol("Üstad 2: süresi tek başına değişen çift yok", tek_fark(tab, 2) == [])
dal3 = {"I": ("ipek proteini yapımı", "biyokimya", "biyokimya"), "II": ("şap kristali", "organik", "anorganik"), "III": ("tutunma hızı", "fizikokimya", "fizikokimya")}
du3 = yargi({k: v[1] == v[2] for k, v in dal3.items()})
U["U3"] = tek_sik("Üstad 3", {"A": {"I", "III"}, "B": {"I"}, "C": {"II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == du3, "A")
liste4 = ["CO2", "CH4", "NaHCO3", "nişasta", "naylon", "NH3"]
x = sum(1 for m in liste4 if MADDE[m][0] and not MADDE[m][1])
y = sum(1 for m in liste4 if MADDE[m][1])
z = sum(1 for m in liste4 if not MADDE[m][0])
U["U4"] = tek_sik("Üstad 4", {"A": (2, 2, 2), "B": (1, 3, 2), "C": (3, 2, 1), "D": (2, 1, 3), "E": (1, 2, 3)}, lambda v: v == (x, y, z), "E")
renk = {ad: (a, b) for a, b, _, ad in IU.LAHANA}
sirke, X_, Y_ = renk["kırmızı"], renk["yeşil"], renk["pembe"]
du5 = yargi({"I": X_[0] > 7, "II": Y_[0] > sirke[1], "III": any(renk["mavi"][0] <= p <= renk["mavi"][1] + .99 for p in seyrelt(X_[1], 400))})
U["U5"] = tek_sik("Üstad 5", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "II", "III"}, "D": {"II", "III"}, "E": {"III"}}, lambda v: v == du5, "C")
du6 = yargi({"I": True, "II": True, "III": ph_sinif(7.6) == "asidik"})
U["U6"] = tek_sik("Üstad 6", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == du6, "B")
dagilim([U[f"U{i}"] for i in range(1, 7)])

# =================================================================== DURAK GÖREVLERİ, MERDİVEN, MECLİS
# Görev 4 (s.5): adil karşılaştırma çiftleri; tablo sayfadan da okunur
DENEME_G4 = {d: (ph, t, dk) for d, ph, t, dk, _ in IU.AL_VERI}
kontrol(f"Görev 4: sıcaklık çifti {tek_fark(DENEME_G4, 1)} == [(1, 2)]", tek_fark(DENEME_G4, 1) == [(1, 2)])
kontrol(f"Görev 4: pH çifti {tek_fark(DENEME_G4, 0)} == [(2, 3)]", tek_fark(DENEME_G4, 0) == [(2, 3)])
kontrol("Görev 4: 2. denemede hem sıcaklık en yüksek hem pH en düşük (Tuzak)", DENEME_G4[2][1] == 220 and DENEME_G4[2][0] == 4)
# Görev 2 ve hızlı görev (s.3)
kontrol("Görev 2: K (pH 3) su ile artar, 7’yi geçmez", seyrelt(3)[-1] > 3 and max(seyrelt(3)) < 7)
kontrol("Görev 2: L (pH 11) su ile azalır, 7’nin altına inmez", seyrelt(11)[-1] < 11 and min(seyrelt(11)) > 7)
aday = [p for p in (3, 5, 9) if 4 < p < 7]
kontrol(f"Hızlı görev s.3: pH 4 + su → aday {aday} == [5]", aday == [5])
# Merdiven 1: X, Y, Z
cozum = []
for X, Y, Z in permutations([("limon tuzu", 2.2), ("lavabo açıcı", 13.5), ("saf su", 7.0)]):
    if X[1] > Y[1] and Z[1] < 7 and Y[1] == 7:
        cozum.append((X[0], Y[0], Z[0]))
kontrol(f"Merdiven 1: tek çözüm {cozum}", cozum == [("lavabo açıcı", "saf su", "limon tuzu")])
# Merdiven 3: kümeler
m3 = ["naylon", "NaCl", "glikoz", "CO2", "nişasta", "ipek", "NH3", "PET"]
iki = [m for m in m3 if MADDE[m][0] and MADDE[m][1]]
yalniz = [m for m in m3 if MADDE[m][0] and not MADDE[m][1]]
hic = [m for m in m3 if not MADDE[m][0] and not MADDE[m][1]]
kontrol(f"Merdiven 3: iki kümede {iki}, yalnız organik {yalniz}, hiçbiri {hic}",
        iki == ["naylon", "nişasta", "ipek", "PET"] and yalniz == ["glikoz"] and hic == ["NaCl", "CO2", "NH3"])
# Görev 5 (s.6) ve Kıssa 2’deki disiplin anahtar kelimeleri
dal5 = {"selüloz zinciri": "polimer", "boya miktarı": "analitik", "solma hızı": "fizikokimya", "metal tuzları": "anorganik", "koku molekülü": "organik"}
kontrol("Görev 5: beş iş beş ayrı disipline düşer", len(set(dal5.values())) == 5)
MECLIS = {"M1": ("Yusuf", 3), "M2": ("Elif", 2), "M3": ("Yusuf", 2), "M4": ("Pamuk", 1)}
kontrol("Meclis 1: pH 2 + su asla 9 olmaz (satır 3)", max(seyrelt(2)) < 7)
kontrol("Meclis 2: CO2 karbonlu ama anorganik (satır 2)", "C" in formul("CO2") and not organik_mi("CO2"))

# =================================================================== pH CETVELİ VE YEREL SAYILAR
ARALIK = {"mide asidi": (1, 3), "limon suyu": (2, 2.6), "sirke": (2.4, 3.4), "gazlı içecek": (2.5, 4), "domates": (4, 4.6),
          "süt": (6.4, 6.8), "saf su": (7, 7), "Çekirge suyu": (7.4, 7.8), "karbonat": (8, 8.5), "sabun": (9, 10.5),
          "antiasit": (10, 10.6), "çamaşır suyu": (11, 13), "lavabo açıcı": (13, 14)}
for ph, ad, *_ in IU.PH_NESNELER:
    a_, b_ = ARALIK[ad]
    kontrol(f"pH cetveli: {ad} ≈ {ph} tipik aralıkta ({a_}–{b_})", a_ <= ph <= b_)
kontrol("pH cetveli: değerler soldan sağa sıralı", [p for p, *_ in IU.PH_NESNELER] == sorted(p for p, *_ in IU.PH_NESNELER))
kontrol("mor lahana tablosu 1–14’ü boşluksuz kaplar", [a for a, *_ in IU.LAHANA][0] == 1 and all(IU.LAHANA[i][1] + 1 == IU.LAHANA[i + 1][0] for i in range(len(IU.LAHANA) - 1)) and IU.LAHANA[-1][1] == 14)


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


meta = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
iz = [d for d in meta["duraklar"] if d["yer"] == "İznik"][0]
uz = km((38.494, 43.38), (iz["enlem"], iz["boylam"]))
kontrol(f"Van → İznik kuş uçuşu {uz:.0f} km ≈ 1200 km (açılış kartı)", abs(uz - 1200) < 30)

# =================================================================== AKÇE
AKCE = {2: 100, 3: 150, 4: 150, 5: 150, 6: 150, 7: 40, 8: 120, 9: 120, 10: 120, 11: 150, 12: 150}
kontrol(f"ünite toplamı {sum(AKCE.values())} = meta {meta['akce_toplam']} = 1400", sum(AKCE.values()) == meta["akce_toplam"] == 1400)
kontrol("meta durak akçeleri 100/150/150/150/150", [d["akce"] for d in meta["duraklar"]] == [100, 150, 150, 150, 150])
kontrol(f"{len(meta['hazine'])} hazine kartı, her biri +10 akçe", all("+10 akçe" in h["not"] for h in meta["hazine"]))
CUBUK = [0, 0, 7, 18, 29, 39, 50, 53, 61, 70, 79, 89, 100, 100, 100]
birikim = [sum(v for k, v in AKCE.items() if k < s_) for s_ in range(1, 16)]
kontrol(f"HUD akçe çubuğu % {CUBUK}", [round(b * 100 / 1400) for b in birikim] == CUBUK)
kontrol("Ahilik eşikleri 400 / 800 / 1150 < 1400", 0 < 400 < 800 < 1150 < 1400)
kontrol("7 nişan; yalnız Üstad Mührü bonus", len(meta["nisanlar"]) == 7 and [n.get("bonus", False) for n in meta["nisanlar"]] == [False] * 6 + [True])

# =================================================================== SAYFADAN OKUMA
html = sayfa_oku(__file__)
if html:
    import kur  # noqa: E402  (SAYFA künyesi: HUD çubuğu)
    kontrol("kur.py HUD çubukları = hesap", [kur.SAYFA[i][2] for i in range(1, 16)] == CUBUK)
    sayfa_ = {i: s_ for i, s_ in enumerate(re.findall(r'<section class="sayfa[^"]*">(.*?)</section>', html, re.S), 1)}
    kontrol(f"{len(sayfa_)} sayfa = meta {meta['sayfa_sayisi']}", len(sayfa_) == meta["sayfa_sayisi"] == 15)
    beklenen = {**{f"I{i}": h for i, h in ANAHTAR.items()}, **KS, **U}
    sayfa_isaretleri_ayni(html, beklenen)
    kontrol(f"meclis hükümleri {meclis_hukumleri(html)}", meclis_hukumleri(html) == MECLIS)
    kontrol(f"Cevaplar anahtar ızgarası {anahtar_izgarasi(html)}", anahtar_izgarasi(html) == ANAHTAR)

    def sik_metni(kod):
        for k, blok in _bloklar(html):
            if k == kod:
                return {h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).replace("%__", "").strip()
                        for h, t in re.findall(r'<div(?: class="sik")?(?: data-dogru)?><b>([A-E])</b>(.*?)</div>', blok, re.S)}
        return {}

    Y5 = {"Yalnız I": {"I"}, "Yalnız II": {"II"}, "Yalnız III": {"III"}, "I ve II": {"I", "II"}, "I ve III": {"I", "III"},
          "II ve III": {"II", "III"}, "I, II ve III": {"I", "II", "III"}, "I, II, III": {"I", "II", "III"}}
    for kod, tablo in (("I3", {"A": {"I", "II"}, "B": {"I"}, "C": {"II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}),
                       ("I4", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "III"}}),
                       ("I7", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}),
                       ("I10", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"II", "III"}}),
                       ("K1", YARGI_SIK),
                       ("U1", {"A": {"I"}, "B": {"I", "III"}, "C": {"II", "III"}, "D": {"I", "II"}, "E": {"I", "II", "III"}}),
                       ("U2", {"A": {"I"}, "B": {"III"}, "C": {"I", "III"}, "D": {"I", "II"}, "E": {"I", "II", "III"}}),
                       ("U3", {"A": {"I", "III"}, "B": {"I"}, "C": {"II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}),
                       ("U5", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "II", "III"}, "D": {"II", "III"}, "E": {"III"}}),
                       ("U6", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}})):
        okunan = {h: Y5.get(t) for h, t in sik_metni(kod).items()}
        kontrol(f"{kod} yargı şıkları sayfadaki metinle aynı", okunan == tablo)
    kontrol("I2 şıkları: sirke, limon suyu, kola, çamaşır suyu, limon tuzu",
            [sik_metni("I2")[h] for h in "ABCDE"] == ["Sirke", "Limon suyu", "Kola", "Çamaşır suyu", "Limon tuzu"])
    kontrol("I9 şıkları: CH4, C2H5OH, C6H12O6, NaHCO3, C12H22O11",
            [sik_metni("I9")[h] for h in "ABCDE"] == ["CH4", "C2H5OH", "C6H12O6", "NaHCO3", "C12H22O11"])
    kontrol("I11 şıkları: nişasta, selüloz, ipek, yün, naylon", [sik_metni("I11")[h] for h in "ABCDE"] == ["Nişasta", "Selüloz", "İpek", "Yün", "Naylon"])
    kontrol("I12 şıkları sırası", [sik_metni("I12")[h] for h in "ABCDE"] == ["Analitik kimya", "Fizikokimya", "Polimer kimyası", "Organik kimya", "Biyokimya"])
    kontrol("U4 şıkları", [sik_metni("U4")[h] for h in "ABCDE"] == ["2 · 2 · 2", "1 · 3 · 2", "3 · 2 · 1", "2 · 1 · 3", "1 · 2 · 3"])
    kontrol("K4 şıkları", [sik_metni("K4")[h] for h in "ABCDE"] == ["1 ve 2", "1 ve 3", "2 ve 3", "1 ve 4", "4 ve 5"])
    kontrol("K2 doğru şık (D) ‘anorganik’ diye yanlış eşleştirir", sik_metni("K2")["D"].endswith("anorganik"))
    kontrol("K3 doğru şık (E) R’nin asidik olacağını iddia eder", "asidik olur" in sik_metni("K3")["E"])
    kontrol("I5 doğru şık (B) asetik asit – gider", sik_metni("I5")["B"].startswith("Asetik asit"))
    kontrol("I6 doğru şık (E) klor gazı", "klor" in sik_metni("I6")["E"])
    kontrol("I1 doğru şık (C) pano yüksekliği", "yüksekliği" in sik_metni("I1")["C"])

    # sayfadaki tablolar = hesaptaki veriler
    s5 = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "|", sayfa_[5]))
    for d, ph, t, dk, al in IU.AL_VERI:
        kontrol(f"s.5 Görev 4 tablosu deneme {d}: {ph}|{t}|{dk}|{al}", f"|{d}||{ph}||{t}||{dk}||{str(al).replace('.', ',')}|" in s5)
    s13 = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "|", sayfa_[13]))
    for i_ in range(4):
        sutun = [DENEME_U2[k][i_] for k in (1, 2, 3, 4)]
        bicim = "||".join(str(v).replace(".", ",") for v in sutun)
        kontrol(f"s.13 Üstad 2 tablo satırı {bicim}", bicim in s13)
    s9 = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "|", sayfa_[9]))
    kontrol("s.9 Kıssa 3 tablosu pH 2 · 12,5 · 7 · 9", "|pH||2||12,5||7||9|" in s9)
    kontrol("s.9 Kıssa 4 tablosu", "|Sıcaklık||20°C||40°C||40°C||20°C||40°C|" in s9 and "|Sirke||50mL||50mL||50mL||100mL||100mL|" in s9
            and "|Kireç||parça||toz||parça||parça||toz|" in s9)
    kontrol("s.11 İmtihan 3 değerleri K = 4, L = 10, M = 7, N = 2", "K = 4, L = 10, M = 7, N = 2" in sayfa_[11])
    kontrol("s.13 Üstad 1 değerleri K = 3, L = 5, M = 9, N = 12", "K = 3, L = 5, M = 9, N = 12" in sayfa_[13])

    # akçe: durak sayfalarındaki çipler + 10 × hazine kartı = levha = meta
    def cipler(s_):
        govde = s_.split('<main class="ic"', 1)[1]
        return [int(x_) for x_ in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', govde)]

    for no in (2, 3, 4, 5, 6):
        s_ = sayfa_[no]
        hz = s_.count('class="hazine"')
        top = sum(cipler(s_)) + 10 * hz
        kontrol(f"s.{no} akçe: çipler {cipler(s_)} + {hz} hazine = {top} (beklenen {AKCE[no]})", top == AKCE[no])
        lev = re.search(r'<div class="hedef">.*?<span class="cip akce">\+(\d+) akçe</span>', s_, re.S)
        kontrol(f"s.{no} levhadaki akçe {lev.group(1) if lev else None}", lev and int(lev.group(1)) == AKCE[no])
    kartlar = re.findall(r'<svg[^>]*class="hno"[^>]*>.*?>(H\d+)<', html, re.S)
    kontrol(f"her hazine kartı sayfada bir kez: {len(kartlar)}", sorted(set(kartlar), key=lambda k: int(k[1:])) == [h["kod"] for h in meta["hazine"]])
    kontrol("s.7 muhasebe +40", "6 satır = +40 akçe" in sayfa_[7])
    kontrol("s.8 meclis 4 × 30", cipler(sayfa_[8]).count(30) == 4 and sum(cipler(sayfa_[8])) == 120)
    kontrol("s.9 kıssa 4 × 30", "4 × 30 = +120 akçe" in sayfa_[9] and cipler(sayfa_[9]).count(30) == 4)
    kontrol("s.10 merdiven 3 × 40", "3 × 40 = +120 akçe" in sayfa_[10] and sayfa_[10].count('class="kart merdiven"') == 3)
    kontrol("s.11–12 imtihan 12 × 25", cipler(sayfa_[11]).count(25) + cipler(sayfa_[12]).count(25) == 12)
    kontrol("s.13 Üstad: akçe çipi yok", cipler(sayfa_[13]) == [])

    # Cevaplar sayfası
    cv = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sayfa_[14]))
    for i_, h in ANAHTAR.items():
        kontrol(f"Cevaplar: İmtihan {i_} · {h}", f" {i_} · {h} " in cv)
    kontrol("Cevaplar: Kıssa 1 C 2 D 3 E 4 B", "Kıssa 1 C 2 D 3 E 4 B" in cv)
    kontrol("Cevaplar: Meclis 1 Yusuf 2 Elif 3 Yusuf 4 Pamuk", "Meclis 1 Yusuf 2 Elif 3 Yusuf 4 Pamuk" in cv)
    for k, h in U.items():
        kontrol(f"Cevaplar: Üstad {k[1]} · {h}", f" {k[1]} · {h} " in cv.split("Üstad soruları", 1)[1])
    for k, (kisi, satir) in MECLIS.items():
        kontrol(f"Cevaplar: Meclis {k[1]} · {kisi} · satır {satir}", f"{k[1]} · {kisi} Satır {satir}" in cv)
    for parca in ("Z limon tuzu, Y saf su, X lavabo açıcı", "naylon, nişasta, ipek, PET", "5: asit + su"):
        kontrol(f"Cevaplar: '{parca}'", parca in cv)

    # öğretmen metni uzunlukları (TASARIM-SISTEMI §10)
    for kod, blok in _bloklar(html):
        if kod.startswith("M"):
            neden = re.search(r'NEDEN\?<span class="cizgili"><span class="ogr">(.*?)</span>', blok).group(1)
            dogrusu = re.search(r'DOĞRUSU<span class="cizgili"><span class="ogr">(.*?)</span>', blok).group(1)
            kontrol(f"{kod}: NEDEN ≤ 12 harf ({neden}) · DOĞRUSU ≤ 45 harf", len(neden) <= 12 and len(dogrusu) <= 45)
    for m in re.findall(r'<div class="cozum-alani">(.*?)</div></div>', sayfa_[10], re.S):
        for satir_ in re.findall(r'<span class="ogr">(.*?)</span></div>', m + "</div>"):
            duz = re.sub(r"<[^>]+>", "", satir_)
            kontrol(f"merdiven satırı ≤ 50 harf: {duz}", len(duz) <= 50)

    # kalın metinde fontta olmayan simge yok (Type 3 riski)
    kalin = " ".join(re.findall(r"<b>(.*?)</b>", html, re.S))
    kontrol("kalın metinde ✓ ✗ ★ ☆ → ← yok", not re.search("[✓✗★☆→←]", re.sub(r"<[^>]+>", "", kalin)))
    kontrol("Câbir için ‘adıyla anılan eserler’ ifadesi", "adıyla anılan eserler" in sayfa_[2])

D.sonuc()
