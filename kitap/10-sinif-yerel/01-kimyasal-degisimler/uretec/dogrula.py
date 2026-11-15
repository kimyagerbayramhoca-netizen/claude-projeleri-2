"""Kimyasal Değişimler (yerel · Kars–Erzurum yolu) — bütün sayısal cevapların ve cevap anahtarının doğrulaması.

Çalıştır:  python3 uretec/dogrula.py
  1. Her denklemin atom ve yük denkliği yeniden sayılır; her görev, hızlı görev, tuzak, meclis, kıssa,
     anahtar merdiveni, imtihan ve üstad sorusu yeniden hesaplanır (YB'ler küçük bir çözücüyle bulunur).
  2. Her çoktan seçmeli soruda TEK doğru şık olduğu denetlenir; şık metinleri sayfadan okunup hesapla karşılaştırılır.
  3. unite.html'deki data-dogru işaretleri, meclis hükümleri, anahtar ızgarası, çözüm sayfasındaki harfler ve
     öğretmen (.ogr) metinleri hesapla aynı mı?
  4. Akçe muhasebesi: durak toplamları (100 + 5 × 120), yan yollar, imtihan, 1400; HUD çubukları; Ahilik eşikleri.
  5. Sayfa göndermeleri (s.{{sayfa|n}}) doğru sayfayı mı gösteriyor?
Sonunda "SONUÇ: hepsi doğru" yazmalı. Yardımcılar: yerel-ortak/dogrula_ortak.py
"""
import json
import os
import re
import sys
from fractions import Fraction as F
from math import gcd

BURA = os.path.dirname(os.path.abspath(__file__))


def _ortak():
    d = BURA
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


sys.path.insert(0, _ortak())
from dogrula_ortak import (D, M, mk, yakin, kontrol, tek_sik, yargi, dagilim, formul, sayfa_oku,  # noqa: E402
                           sayfa_isaretleri_ayni, meclis_hukumleri, ogretmen_metinleri, anahtar_izgarasi)

META = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
SABLON = open(os.path.join(BURA, "sablon.html"), encoding="utf-8").read()
HTML = sayfa_oku(__file__)


# ------------------------------------------------------------------ küçük kimya araçları

def taraf(t):
    """'2H2 + O2' → [(2, 'H2'), (1, 'O2')]"""
    out = []
    for p in t.split("+"):
        m = re.match(r"\s*(\d*)\s*([A-Za-z0-9()]+)\s*$", p)
        out.append((int(m.group(1) or 1), m.group(2)))
    return out


def sayim(yan):
    top = {}
    for k, f_ in yan:
        for el, n in formul(f_).items():
            top[el] = top.get(el, 0) + k * n
    return top


def denk(denklem, ad=None):
    """'2H2 + O2 -> 2H2O' atom denkliği; katsayılar en sade mi? (ortak böleni 1)"""
    sol, sag = denklem.split("->")
    L, R = taraf(sol), taraf(sag)
    ok = sayim(L) == sayim(R)
    g = 0
    for k, _ in L + R:
        g = gcd(g, k)
    kontrol(f"denk: {ad or denklem} (atomlar {sayim(L)} == {sayim(R)}, sade)", ok and g == 1)
    return L, R


# yükseltgenme basamağı: varsayılanlar + tek bilinmeyeni çöz; iki bilinmeyenli tuzlar için açık değerler
YB_VARS = {"H": 1, "O": -2, "Li": 1, "Na": 1, "K": 1, "Ag": 1, "Mg": 2, "Ca": 2, "Ba": 2, "Zn": 2, "Al": 3, "F": -1}
YB_ACIK = {"CuSO4": {"Cu": 2, "S": 6, "O": -2}, "FeSO4": {"Fe": 2, "S": 6, "O": -2},
           "Cu(NO3)2": {"Cu": 2, "N": 5, "O": -2}, "Fe(NO3)3": {"Fe": 3, "N": 5, "O": -2}}


def yb(tur):
    if tur in YB_ACIK:
        return dict(YB_ACIK[tur])
    d = formul(tur)
    if len(d) == 1:
        return {next(iter(d)): 0}                              # element hâli
    bilinmeyen = [e for e in d if e not in YB_VARS]
    if len(bilinmeyen) > 1:
        raise ValueError(f"YB çözülemez: {tur}")
    sonuc = {e: YB_VARS[e] for e in d if e in YB_VARS}
    if bilinmeyen:
        e = bilinmeyen[0]
        sonuc[e] = F(-sum(YB_VARS[x] * n for x, n in d.items() if x != e), d[e])
    else:
        kontrol(f"YB toplamı 0: {tur}", sum(sonuc[x] * n for x, n in d.items()) == 0)
    return sonuc


def redoks_mu(denklem):
    sol, sag = denklem.split("->")
    def kume(yan):
        k = {}
        for _, t in taraf(yan):
            for e, v in yb(t).items():
                k.setdefault(e, set()).add(v)
        return k
    a, b = kume(sol), kume(sag)
    return any(a.get(e) != b.get(e) for e in set(a) | set(b))


AZ_COZUNUR = {"AgCl", "AgBr", "AgI", "BaSO4", "PbSO4", "CaCO3", "BaCO3", "MgCO3", "Fe(OH)3", "Mg(OH)2", "Cu(OH)2", "PbCl2", "PbI2"}


def cokelek(a, b):
    """İki iyonik bileşiğin çözeltisi: çift yer değiştirme ürünlerinden suda az çözünen var mı? (katyon, anyon ayrımı basit tablo)"""
    IYON = {"NaNO3": ("Na", "NO3"), "KCl": ("K", "Cl"), "K2SO4": ("K", "SO4"), "NH4NO3": ("NH4", "NO3"), "LiCl": ("Li", "Cl"),
            "KOH": ("K", "OH"), "AgNO3": ("Ag", "NO3"), "NaBr": ("Na", "Br")}
    YUK = {"Na": 1, "K": 1, "NH4": 1, "Li": 1, "Ag": 1, "NO3": -1, "Cl": -1, "SO4": -2, "OH": -1, "Br": -1}
    (k1, a1), (k2, a2) = IYON[a], IYON[b]
    def tuz(k, an):
        q, r = YUK[k], -YUK[an]
        g = gcd(q, r)
        kk, aa = r // g, q // g
        ks = k if kk == 1 else (f"({k}){kk}" if len(formul(k)) > 1 or k == "NH4" else f"{k}{kk}")
        as_ = an if aa == 1 else (f"({an}){aa}" if len(formul(an)) > 1 else f"{an}{aa}")
        return ks + as_
    return any(t in AZ_COZUNUR for t in (tuz(k1, a2), tuz(k2, a1)))


def sayi(m):
    return float(m.replace(",", "."))


def bloklar(html):
    yer = [(m.start(), m.group(1)) for m in re.finditer(r'data-soru="([^"]+)"', html)]
    out = {}
    for i, (b, k) in enumerate(yer):
        s = yer[i + 1][0] if i + 1 < len(yer) else len(html)
        out[k] = html[b:min(s, html.find("</section>", b))]
    return out


def sik_metni(blok):
    """{'A': 'metin', …} (etiketler ve %__ temizlenmiş)"""
    out = {}
    for h, ic in re.findall(r'<div(?: class="sik")?(?: data-dogru)?><b>([A-E])</b>(.*?)</div>', blok, re.S):
        ic = re.sub(r"<em>.*?</em>", "", ic)
        out[h] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", ic)).strip()
    return out


B = bloklar(HTML) if HTML else {}


def siklar_ayni(kod, beklenen):
    """Sayfadaki şık metinleri beklenenle aynı mı? beklenen: {'A': '0,6', …} (sayfadaki metin)"""
    gercek = sik_metni(B.get(kod, ""))
    kontrol(f"sayfada {kod}: şık metinleri {gercek} == {beklenen}", gercek == beklenen)


# ================================================================== 1. DURAK · ÇILDIR · FİZİKSEL Mİ KİMYASAL MI?
print("— 1. durak")
kimyasal = {"gölün donması": False, "kaşarın olgunlaşması": True, "odunun yanması": True, "Oltu taşının parlatılması": False}
kontrol("Görev 1: kimyasal olanlar (b) ve (c)", [k for k, v in kimyasal.items() if v] == ["kaşarın olgunlaşması", "odunun yanması"])
hizli1 = {"süt ekşir": True, "kar erir": False, "demir paslanır": True, "şeker çözünür": False}
kontrol("D1 hızlı: 2 kimyasal", sum(hizli1.values()) == 2)
kontrol("buz yüzer: özgül ağırlık ≈ 0,92 < 1", 0.92 < 1)

# ================================================================== 2. DURAK · KARS · DENKLEM
print("— 2. durak")
denk("C12H22O11 + H2O -> 4C3H6O3", "laktoz → laktik asit (Görev 2, x = 4)")
kontrol("Görev 2: x = 12/3 = 4", F(12, 3) == 4)
denk("2Mg + O2 -> 2MgO", "magnezyum yanması")
kontrol("Görev 3: 10 − 6 = 4 g O2; mol ile: 6/24 = 0,25 mol Mg → 0,25·40 = 10 g MgO, 0,125·32 = 4 g O2",
        10 - 6 == 4 and yakin(6 / M["Mg"] * mk("MgO"), 10) and yakin(6 / M["Mg"] / 2 * mk("O2"), 4))
L, R = denk("C3H8 + 5O2 -> 3CO2 + 4H2O", "propan yanması")
kontrol("D2 hızlı: katsayılar toplamı 13", sum(k for k, _ in L + R) == 13)
L, R = denk("N2 + 3H2 -> 2NH3", "tuzak: molekül sayısı 4 → 2")
kontrol("tuzak: molekül sayısı korunmaz (4 → 2)", sum(k for k, _ in L) == 4 and sum(k for k, _ in R) == 2)
denk("CH4 + 2O2 -> CO2 + 2H2O", "korunum modeli (infografik)")

# ================================================================== 3. DURAK · ANİ · ASİT-BAZ
print("— 3. durak")
denk("Ca(OH)2 + 2HCl -> CaCl2 + 2H2O", "Görev 4a / Görev 5")
denk("KOH + HNO3 -> KNO3 + H2O", "Görev 4b")
denk("Ca(OH)2 + CO2 -> CaCO3 + H2O", "harcın sertleşmesi")
denk("HCl + NaOH -> NaCl + H2O", "nötralleşme modeli")
kontrol("Görev 5: M(Ca(OH)2) = 74, 7,4/74 = 0,1 mol → 0,2 mol HCl", mk("Ca(OH)2") == 74 and yakin(7.4 / 74 * 2, 0.2))
ametal = {"C", "S", "N", "P"}
asidik = [o for o in ("CO2", "SO2", "CaO", "Na2O") if set(formul(o)) - {"O"} <= ametal]
kontrol("D3 hızlı: asidik oksitler CO2 ve SO2", asidik == ["CO2", "SO2"])

# ================================================================== 4. DURAK · SARIKAMIŞ · YANMA, SENTEZ, ANALİZ
print("— 4. durak")
denk("C + O2 -> CO2", "tam yanma (karbon)")
denk("2C + O2 -> 2CO", "eksik yanma")
L, R = denk("2C4H10 + 13O2 -> 8CO2 + 10H2O", "Görev 6: bütan")
kontrol("Görev 6: H7 kuralı (x CO2, y/2 H2O; O2 = (2x + y/2)/2)", (F(4), F(10, 2), F(2 * 4 + 5, 2)) == (4, 5, F(13, 2)))
for d in ("CaCO3 -> CaO + CO2", "CaO + H2O -> Ca(OH)2", "2NaHCO3 -> Na2CO3 + H2O + CO2", "2H2O2 -> 2H2O + O2", "CaO + CO2 -> CaCO3"):
    denk(d)
def tur_(d):
    sol, sag = d.split("->")
    return "sentez" if len(taraf(sol)) > 1 and len(taraf(sag)) == 1 else ("analiz" if len(taraf(sol)) == 1 and len(taraf(sag)) > 1 else "?")
kontrol("Görev 7: (a) sentez (b) analiz (c) sentez",
        [tur_(d) for d in ("2Mg + O2 -> 2MgO", "2H2O2 -> 2H2O + O2", "CaO + CO2 -> CaCO3")] == ["sentez", "analiz", "sentez"])
kontrol("D4 hızlı: 2,4/12 = 0,2 mol C → 0,2 mol CO", yakin(2.4 / M["C"], 0.2))
denk("N2 + O2 -> 2NO", "tuzak: ısı alan yanma")
kontrol("her yanma redokstur (C + O2, 2C4H10 + 13O2)", redoks_mu("C + O2 -> CO2") and redoks_mu("2Mg + O2 -> 2MgO"))

# ================================================================== 5. DURAK · PASİNLER · ÇÖKELME
print("— 5. durak")
denk("CaCl2 + Na2CO3 -> CaCO3 + 2NaCl", "çökelme modeli")
denk("AgNO3 + NaCl -> AgCl + NaNO3", "Görev 8")
kontrol("Görev 9: 0,05·100 = 5 g CaCO3", mk("CaCO3") == 100 and yakin(0.05 * mk("CaCO3"), 5))
denk("Ba(NO3)2 + Na2SO4 -> BaSO4 + 2NaNO3", "D5 hızlı")
kontrol("D5 hızlı: çöken BaSO4", "BaSO4" in AZ_COZUNUR and "NaNO3" not in AZ_COZUNUR)

# ================================================================== 6. DURAK · ERZURUM · REDOKS
print("— 6. durak")
kontrol("Görev 10: Fe2O3’te Fe +3, K2Cr2O7’de Cr +6", yb("Fe2O3")["Fe"] == 3 and yb("K2Cr2O7")["Cr"] == 6)
denk("Fe + CuSO4 -> FeSO4 + Cu", "Görev 11 / redoks modeli")
kontrol("Görev 11: 5,6/56 = 0,1 mol Fe → 0,2 mol e⁻ → 0,1 mol Cu = 6,4 g",
        yakin(5.6 / M["Fe"], 0.1) and yakin(5.6 / M["Fe"] * (yb("FeSO4")["Fe"] - 0), 0.2) and yakin(0.1 * M["Cu"], 6.4))
L, R = denk("4Fe + 3O2 -> 2Fe2O3", "D6 hızlı: pas")
kontrol("D6 hızlı: 0,4 mol Fe × 3 = 1,2 mol e⁻", yakin(0.4 * yb("Fe2O3")["Fe"], 1.2))
for d in ("Mg + 2HCl -> MgCl2 + H2", "2Na + 2H2O -> 2NaOH + H2", "Fe + CuSO4 -> FeSO4 + Cu"):
    denk(d)
    kontrol(f"metal tepkimesi redokstur: {d}", redoks_mu(d))
AKT = "K Na Ca Mg Al Zn Fe Pb H Cu Ag Au".split()
kontrol("aktiflik: Fe ve Zn Cu’dan aktif, Ag H’den az aktif", AKT.index("Fe") < AKT.index("Cu") and AKT.index("Zn") < AKT.index("Cu") and AKT.index("Ag") > AKT.index("H"))

# ================================================================== MECLİS (s.9)
print("— Meclis")
denk("Ca(NO3)2 + Na2CO3 -> CaCO3 + 2NaNO3", "M1")
kontrol("M1: seyirci Na⁺ ve NO3⁻ (Ca²⁺, CO3²⁻ çöker)", "CaCO3" in AZ_COZUNUR)
kontrol("M2: Fe 0 → +2 yükseltgenir, Cu +2 → 0 indirgenir", yb("FeSO4")["Fe"] > yb("Fe")["Fe"] and yb("Cu")["Cu"] < yb("CuSO4")["Cu"])
kontrol("M4: 0,1 mol C3H8 → 0,3 CO2 + 0,4 H2O = 0,7 mol (0,6 değil)", yakin(0.1 * 3 + 0.1 * 4, 0.7))
MECLIS = {"M1": ("Yusuf", 3), "M2": ("Elif", 3), "M3": ("Yusuf", 2), "M4": ("Pamuk", 2)}

# ================================================================== KISSALAR (s.10)
print("— Kıssalar")
SET_A = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}
denk("K2CO3 + 2CH3COOH -> 2CH3COOK + H2O + CO2", "K1")
K = {}
K["K1"] = tek_sik("K1", SET_A, lambda v: v == yargi({"I": True, "II": True, "III": False}), "C")
denk("2Al + Fe2O3 -> Al2O3 + 2Fe", "K2 termit")
nAl = 8.1 / M["Al"]
e_k2, fe_k2 = nAl * 3, nAl * M["Fe"]
K["K2"] = tek_sik("K2", {"A": (0.3, 8.4), "B": (0.6, 16.8), "C": (0.9, 8.4), "D": (0.9, 16.8), "E": (1.8, 33.6)},
                  lambda v: yakin(v[0], e_k2) and yakin(v[1], fe_k2), "D")
denk("Ba(OH)2 + H2SO4 -> BaSO4 + 2H2O", "K3")
K["K3"] = tek_sik("K3", {"A": {"I"}, "B": {"II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}},
                  lambda v: v == yargi({"I": True, "II": True, "III": True}), "E")
k4 = yargi({"I": AKT.index("Fe") < AKT.index("Cu") and AKT.index("Zn") < AKT.index("Cu"),
            "II": AKT.index("Ag") < AKT.index("H"), "III": redoks_mu("Fe + CuSO4 -> FeSO4 + Cu")})
K["K4"] = tek_sik("K4", {"A": {"I"}, "B": {"I", "III"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == k4, "B")
siklar_ayni("K2", {"A": "0,3 mol e− · 8,4 g", "B": "0,6 mol e− · 16,8 g", "C": "0,9 mol e− · 8,4 g", "D": "0,9 mol e− · 16,8 g", "E": "1,8 mol e− · 33,6 g"})

# ================================================================== ANAHTAR MERDİVENİ (s.11)
print("— Anahtar merdiveni")
n = 40 / mk("CaCO3")
kontrol("A1: 0,4 mol → 22,4 g CaO kalır, 0,4 mol = 17,6 g CO2 (toplam 40)",
        yakin(n, 0.4) and yakin(n * mk("CaO"), 22.4) and yakin(n * mk("CO2"), 17.6) and yakin(n * (mk("CaO") + mk("CO2")), 40))
denk("Cu + 2AgNO3 -> Cu(NO3)2 + 2Ag", "A2")
kontrol("A2: 3,2/64 = 0,05 mol Cu → 0,1 mol e⁻ → 10,8 g Ag", yakin(3.2 / M["Cu"] * 2, 0.1) and yakin(3.2 / M["Cu"] * 2 * M["Ag"], 10.8))
ag, no3, ca, cl = 0.3, 0.3, 0.1, 0.1 * 2
cok = min(ag, cl)
kontrol("A3: Cl⁻ biter → 0,2·143,5 = 28,7 g AgCl; kalan 0,1 Ag⁺, 0,3 NO3⁻, 0,1 Ca²⁺",
        yakin(cok * mk("AgCl"), 28.7) and yakin(ag - cok, 0.1) and no3 == 0.3 and ca == 0.1 and mk("AgCl") == 143.5)

# ================================================================== BÜYÜK İMTİHAN (s.12–13)
print("— Büyük İmtihan")
I = {}
I["I1"] = tek_sik("I1", {"A": False, "B": False, "C": True, "D": False, "E": False}, lambda v: v, "C")
kor = yargi({"I": True, "II": False, "III": True, "IV": True})
I["I2"] = tek_sik("I2", {"A": {"I", "II"}, "B": {"I", "III"}, "C": {"II", "IV"}, "D": {"I", "III", "IV"}, "E": {"I", "II", "III", "IV"}}, lambda v: v == kor, "D")
once, sonra = {"H2": 4, "O2": 3}, {"H2O": 4, "O2": 1}
kontrol("I3 modeli: atomlar korunur (H 8 = 8, O 6 = 6)", sayim([(v, k) for k, v in once.items()]) == sayim([(v, k) for k, v in sonra.items()]))
harc = [once["H2"] - sonra.get("H2", 0), once["O2"] - sonra["O2"], sonra["H2O"]]
g = gcd(gcd(harc[0], harc[1]), harc[2])
denk("2H2 + O2 -> 2H2O", "I3")
I["I3"] = tek_sik("I3", {"A": 5, "B": 7, "C": 10, "D": 11, "E": 12}, lambda v: v == sum(x // g for x in harc), "A")
i4 = yargi({"I": tur_("CaCO3 -> CaO + CO2") == "analiz", "II": True, "III": redoks_mu("CaCO3 -> CaO + CO2")})
I["I4"] = tek_sik("I4", {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == i4, "C")
I["I5"] = tek_sik("I5", {"A": ("NaNO3", "KCl"), "B": ("K2SO4", "NH4NO3"), "C": ("LiCl", "NaNO3"), "D": ("KOH", "NaNO3"), "E": ("AgNO3", "NaBr")},
                  lambda v: cokelek(*v), "E")
denk("Fe(NO3)3 + 3KOH -> Fe(OH)3 + 3KNO3", "I6")
i6 = yargi({"I": True, "II": True, "III": False})
I["I6"] = tek_sik("I6", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == i6, "B")
S = {h: yb(t)["S"] for h, t in zip("ABCDE", ("H2S", "S8", "SO2", "H2SO4", "Na2SO3"))}
kontrol(f"I7: YB(S) {S}", S == {"A": -2, "B": 0, "C": 4, "D": 6, "E": 4})
I["I7"] = tek_sik("I7", S, lambda v: v == max(S.values()), "D")
I8 = {"A": "2Na + 2H2O -> 2NaOH + H2", "B": "HCl + KOH -> KCl + H2O", "C": "CaO + H2O -> Ca(OH)2",
      "D": "AgNO3 + NaCl -> AgCl + NaNO3", "E": "MgCO3 -> MgO + CO2"}
for d in I8.values():
    denk(d)
I["I8"] = tek_sik("I8", I8, redoks_mu, "A")
denk("Mg + CuSO4 -> MgSO4 + Cu", "I9")
i9 = yargi({"I": yb("MgSO4")["Mg"] - yb("Mg")["Mg"] == 2, "II": yb("CuSO4")["Cu"] - yb("Cu")["Cu"] == 2, "III": True})
I["I9"] = tek_sik("I9", {"A": {"I"}, "B": {"II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == i9, "E")
I["I10"] = tek_sik("I10", {"A": 0.6, "B": 0.8, "C": 1.0, "D": 1.2, "E": 2.0}, lambda v: yakin(v, 0.2 * 5), "C")
bazik = {"KOH": True, "NH3": True, "Na2O": True, "CH3OH": False, "CaO": True}
I["I11"] = tek_sik("I11", dict(zip("ABCDE", bazik)), lambda v: not bazik[v], "D")
denk("HNO3 + KOH -> KNO3 + H2O", "I12")
i12 = yargi({"I": True, "II": True, "III": False})
I["I12"] = tek_sik("I12", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == i12, "B")
dagilim([I[f"I{i}"] for i in range(1, 13)])
siklar_ayni("I3", {"A": "5", "B": "7", "C": "10", "D": "11", "E": "12"})
siklar_ayni("I10", {"A": "0,6", "B": "0,8", "C": "1,0", "D": "1,2", "E": "2,0"})
siklar_ayni("I7", {"A": "H2S", "B": "S8", "C": "SO2", "D": "H2SO4", "E": "Na2SO3"})
siklar_ayni("I11", {"A": "KOH", "B": "NH3", "C": "Na2O", "D": "CH3OH", "E": "CaO"})

# ================================================================== ÜSTAD (s.14)
print("— Üstad")
U = {}
x, y = F(6, 10) / F(2, 10), 2 * F(8, 10) / F(2, 10)
o2 = (F(6, 10) * 2 + F(8, 10)) / 2
urun = 0.6 * mk("CO2") + 0.8 * mk("H2O")
u1 = yargi({"I": (x, y) == (3, 8), "II": o2 == 1, "III": yakin(urun, 26.4)})
kontrol(f"U1: C3H8, 1 mol O2, ürün {urun:.1f} g (26,4 değil)", (x, y) == (3, 8) and o2 == 1 and yakin(urun, 40.8))
U["U1"] = tek_sik("U1", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}, lambda v: v == u1, "B")
ncl = 28.7 / mk("AgCl")
xn = (mk("KCl") * ncl - 13.3) / (mk("KCl") - mk("NaCl"))
kontrol(f"U2: NaCl {xn:.3f} mol → {xn * mk('NaCl'):.2f} g", yakin(xn, 0.1) and yakin(xn * mk("NaCl") + (ncl - xn) * mk("KCl"), 13.3))
U["U2"] = tek_sik("U2", {"A": 5.85, "B": 6.65, "C": 7.45, "D": 9.75, "E": 11.7}, lambda v: yakin(v, xn * mk("NaCl")), "A")
denk("Cl2 + 2NaOH -> NaCl + NaClO + H2O", "U3")
u3 = yargi({"I": yb("NaCl")["Cl"] < 0 < yb("NaClO")["Cl"], "II": yb("NaClO")["Cl"] == 1, "III": yakin(0.1 * 1, 0.2)})
U["U3"] = tek_sik("U3", SET_A | {"B": {"III"}}, lambda v: v == u3, "C")
co2 = 50 - 36.8
kum = 50 - co2 / mk("CO2") * mk("CaCO3")
kontrol("U4: 13,2 g CO2 = 0,3 mol → 30 g CaCO3; kalan 20 g kum + 16,8 g CaO = 36,8 g",
        yakin(co2 / mk("CO2"), 0.3) and yakin(kum + 0.3 * mk("CaO"), 36.8))
U["U4"] = tek_sik("U4", {"A": 26.4, "B": 30, "C": 44, "D": 60, "E": 73.6}, lambda v: yakin(v, 100 * (50 - kum) / 50), "D")
xm = F(6, 10) / 3
km = float(xm) * (mk("NaOH") + mk("Ca(OH)2"))
U["U5"] = tek_sik("U5", {"A": 17.1, "B": 22.8, "C": 25.6, "D": 28.5, "E": 34.2}, lambda v: yakin(v, km), "B")
for d in ("2KClO3 -> 2KCl + 3O2", "CaO + SO2 -> CaSO3", "Zn + 2HCl -> ZnCl2 + H2"):
    denk(d)
u6 = {"A": tur_("2KClO3 -> 2KCl + 3O2") == "analiz" and redoks_mu("2KClO3 -> 2KCl + 3O2"),
      "B": not redoks_mu("CaO + SO2 -> CaSO3"),
      "C": True,                                                   # Zn, H’nin yerini alır (tekli yer değiştirme)
      "D": yb("O2")["O"] > yb("KClO3")["O"],
      "E": yb("ZnCl2")["Zn"] < yb("Zn")["Zn"]}                    # "Zn indirgenir" — yanlış (yükseltgenir)
U["U6"] = tek_sik("U6 (yanlış olan)", u6, lambda v: not v, "E")
siklar_ayni("U2", {"A": "5,85", "B": "6,65", "C": "7,45", "D": "9,75", "E": "11,7"})
siklar_ayni("U4", {"A": "%26,4", "B": "%30", "C": "%44", "D": "%60", "E": "%73,6"})
siklar_ayni("U5", {"A": "17,1", "B": "22,8", "C": "25,6", "D": "28,5", "E": "34,2"})

# ================================================================== SAYFA İŞARETLERİ
print("— Sayfa işaretleri")
if HTML:
    sayfa_isaretleri_ayni(HTML, {**I, **K, **U})
    kontrol(f"meclis hükümleri {meclis_hukumleri(HTML)} == {MECLIS}", meclis_hukumleri(HTML) == MECLIS)
    izg = anahtar_izgarasi(HTML)
    kontrol(f"anahtar ızgarası {izg}", izg == {i: I[f"I{i}"] for i in range(1, 13)})
    cev = HTML[HTML.index('class="cozumler'):]
    gruplar = re.findall(r'<div class="grup"><h4>(.*?)</h4>(.*?)</div>', cev, re.S)
    g = {ad: dict((int(n_), h) for n_, h in re.findall(r"<b>(\d+) · ([A-E])</b>", ic)) for ad, ic in gruplar}
    kontrol("çözümler · İmtihan harfleri", g.get("Büyük İmtihan") == {i: I[f"I{i}"] for i in range(1, 13)})
    kontrol("çözümler · Kıssa harfleri", g.get("Kıssalar") == {i: K[f"K{i}"] for i in range(1, 5)})
    kontrol("çözümler · Üstad harfleri", g.get("Üstad soruları") == {i: U[f"U{i}"] for i in range(1, 7)})
    hz = re.search(r'yan-anahtar.*?</div>', cev, re.S).group(0)
    kontrol("hızlı anahtar · Kıssa", re.findall(r'<span class="ck">(\d) ([A-E])</span>', hz)[:4] == [(str(i), K[f"K{i}"]) for i in range(1, 5)])
    kontrol("hızlı anahtar · Üstad", re.findall(r'<span class="ck">(\d) ([A-E])</span>', hz)[4:] == [(str(i), U[f"U{i}"]) for i in range(1, 7)])
    kontrol("hızlı anahtar · Meclis", re.findall(r'<span class="ck">\d (Yusuf|Elif|Pamuk|Zehra|Ahmet)</span>', hz) == [v[0] for v in MECLIS.values()])
    ogr = ogretmen_metinleri(HTML)
    for beklenen in ("2", "1 + 5 + 3 + 4 = 13", "CO2 ve SO2", "0,2 mol CO", "BaSO4", "1,2 mol e−"):
        kontrol(f"öğretmen metni var: {beklenen}", beklenen in ogr)
    kontrol("her cevap kutusunda öğretmen metni", HTML.count('<div class="cevap-kutu">CEVABIN:<span class="ogr">') == 6)

# ================================================================== AKÇE
print("— Akçe")
def bolum(n_):
    m_ = re.search(rf'<section class="sayfa s{n_}\b.*?</section>', SABLON, re.S)
    return m_.group(0)
for d in META["duraks"] if "duraks" in META else META["duraklar"]:
    t = bolum(d["sayfa"])
    ana = t[t.index("<main"):]
    cipler = [int(v) for v in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', ana)]
    hazine = len(re.findall(r"\{\{hazine\|H\d+\}\}", ana)) * 10
    kontrol(f"{d['no']}. durak (s.{d['sayfa']}): {cipler} + hazine {hazine} = {d['akce']}", sum(cipler) + hazine == d["akce"])
    kontrol(f"{d['no']}. durak levhasında +{d['akce']} akçe", f'+{d["akce"]} akçe' in t[:t.index("<main")])
    kontrol(f"{d['no']}. durağın hazine kartları meta ile aynı",
            sorted(re.findall(r"\{\{hazine\|(H\d+)\}\}", ana)) == sorted(h["kod"] for h in META["hazine"] if h["durak"] == d["no"]))
duraklar = sum(d["akce"] for d in META["duraklar"])
kontrol("duraklar 100 + 5 × 120 = 700", duraklar == 700)
hul = 40
kontrol("Hülasa: muhasebe 6 satır = +40", "6 satır = +40 akçe" in bolum(8) and bolum(8).count("{{cay|0|b}}{{cay|0|b}}{{cay|0|b}}") == 6)
mec = sum(int(v) for v in re.findall(r'<span class="cip akce">\+(\d+)</span>', bolum(9)))
kis = sum(int(v) for v in re.findall(r'<span class="cip akce">\+(\d+)</span>', bolum(10)))
anh = 40 * bolum(11).count('<div class="kart merdiven">')
imt = sum(int(v) for n_ in (12, 13) for v in re.findall(r'<span class="cip akce">\+(\d+)</span>', bolum(n_)))
kontrol(f"yan yollar: meclis {mec}, kıssa {kis}, anahtar {anh} = 120 + 120 + 120", (mec, kis, anh) == (120, 120, 120))
kontrol(f"imtihan 12 × 25 = {imt}", imt == 300)
toplam = duraklar + hul + mec + kis + anh + imt
kontrol(f"toplam akçe {toplam} == 1400; s.1 çipinde de 1400", toplam == 1400 and re.search(r"</svg> ?1400 akçe", HTML or "") is not None)
defter = [int(v) for v in re.findall(r'<td class="n">(\d+)</td>', bolum(16))]
kontrol(f"final defteri {defter}: kalemler toplamı = TOPLAM = 1400", sum(defter[:-1]) == defter[-1] == 1400)
kontrol("defter durak satırları meta ile aynı", defter[:6] == [d["akce"] for d in META["duraklar"]])
# HUD çubukları: o sayfaya kadar alınabilecek en çok akçe / 1400
sys.path.insert(0, BURA)
kur = open(os.path.join(BURA, "kur.py"), encoding="utf-8").read()
cubuk = [int(v) for v in re.findall(r"^\s+\d+: \('.*?', '.*?', (\d+)\),", kur, re.M)]
once_ = [0, 0, 100, 220, 340, 460, 580, 700, 740, 860, 980, 1100, 1250, 1400, 1400, 1400]
kontrol(f"HUD çubukları {cubuk}", cubuk == [round(100 * a / 1400) for a in once_])
for esik in ("400+", "800+", "1150+"):
    kontrol(f"Ahilik eşiği {esik} (s.1)", esik in bolum(1))
kontrol("final unvan aralıkları", all(t in bolum(16) for t in ("0–399", "400–799", "800–1149", "1150–1400")))

# ================================================================== SAYFA GÖNDERMELERİ
print("— Sayfa göndermeleri")
konu = {2: "Fiziksel", 3: "denklem", 4: "Arrhenius", 5: "yanma", 6: "çözünür", 7: "redoks", 8: "Hülasa", 9: "Meclis",
        10: "Kıssa", 11: "Anahtar", 12: "İmtihan", 13: "İmtihan", 15: "Cevaplar"}
for n_ in sorted(set(int(v) for v in re.findall(r"\{\{sayfa\|(\d+)\}\}", SABLON))):
    kontrol(f"s.{{{{sayfa|{n_}}}}} → {konu.get(n_)}", n_ in konu and konu[n_] in bolum(n_))
kontrol("YB kuralları 6. durakta (azık s.12 → s.6 çözünürlük, s.7 YB)", "YB:" in bolum(7) and "Az çözünür" in bolum(6))

D.sonuc()
