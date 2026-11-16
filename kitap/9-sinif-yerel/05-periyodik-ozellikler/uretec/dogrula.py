"""Periyodik Özellikler (yerel · Maden Yolu II) — eğilimlerin, sayıların ve cevap anahtarının doğrulaması.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Veri: infografik_unite.VERI klasik ünitenin (9-sinif/05) değerleriyle aynı mı? Element adları ve sınıfları kitabın
     periyodik tablosuyla (yerel-cerceve/uretec/elementler.py) aynı mı? Sayfada geçen her "Sembol sayı" verisi VERI ile aynı mı?
  2. Eğilimler: yarıçap, İE₁ (2A–3A, 5A–6A istisnaları), EN (Pauling), metalik karakter VERI'den yeniden kurulur.
  3. Her görev, tuzak, hızlı görev, kıssa, meclis, merdiven, imtihan ve Üstad sorusu YENİDEN hesaplanır; ardışık İE'den
     değerlik elektronu (en büyük sıçrama) bulunur; her çoktan seçmelide TEK doğru şık; İmtihan ve Üstad'da A–E en az bir kez.
  4. Sayfadan (unite.html) okunan data-dogru işaretleri, Cevaplar ızgarası, çözüm satırları, meclis hükümleri, öğretmen
     metinleri ve CEVABIN kutuları hesapla aynı mı?
  5. Akçe: her durak sayfasındaki akçe çipleri + hazine kartları = levhadaki durak akçesi = meta.json; toplam 1400; HUD çubuğu.
"""
import ast
import html as _html
import itertools
import json
import os
import re
import runpy
import sys

BURA = os.path.dirname(os.path.abspath(__file__))


def _ortak():
    d = BURA
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


ORTAK = _ortak()
KITAP = os.path.dirname(ORTAK)
sys.path.insert(0, ORTAK)
sys.path.insert(0, BURA)
from dogrula_ortak import (D, kontrol, tek_sik, yargi, dagilim, sayfa_oku, sayfa_isaretleri_ayni,  # noqa: E402
                           meclis_hukumleri, ogretmen_metinleri, anahtar_izgarasi)
from infografik_unite import VERI, Z, YER, SINIF, AD, TABLO, TEST5, KESIT, USTAD8, IE_SIRA  # noqa: E402

r, ri, ie1, ie, en = VERI["r"], VERI["ri"], VERI["ie1"], VERI["ie"], VERI["en"]
YARGI_A = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}     # Kıssa 1
YARGI_I3 = {"A": {"I"}, "B": {"III"}, "C": {"I", "III"}, "D": {"I", "II"}, "E": {"II", "III"}}        # İmtihan 3
YARGI_I9 = {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}  # İmtihan 9, Üstad 1
YARGI_U2 = {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}
YARGI_U4 = {"A": {"I", "II"}, "B": {"I"}, "C": {"II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}
YARGI_U5 = {"A": {"I"}, "B": {"II"}, "C": {"I", "III"}, "D": {"I", "II"}, "E": {"I", "II", "III"}}


def vir(x, h=1):
    return f"{x:.{h}f}".replace(".", ",")


# ================================================================== 1. VERİ · klasik ünite ve kitabın periyodik tablosu
klasik_yol = os.path.join(KITAP, "9-sinif", "05-periyodik-ozellikler", "uretec")
kp = open(os.path.join(klasik_yol, "svgler.py"), encoding="utf-8").read()
ks = open(os.path.join(klasik_yol, "sablon.html"), encoding="utf-8").read()


def _lit(ad):
    """svgler.py'deki 'ad=[...]' ya da 'ad={...}' sabitini (çok satırlı olabilir) parantez eşleyerek okur."""
    i = re.search(rf"^{ad}=", kp, re.M).end()
    acan = kp[i]
    kapa = {"[": "]", "{": "}", "(": ")"}[acan]
    derin = 0
    for j in range(i, len(kp)):
        derin += (kp[j] == acan) - (kp[j] == kapa)
        if derin == 0:
            return ast.literal_eval(kp[i:j + 1])


k_ie = dict(zip("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca".split(), _lit("ie")))
kontrol("İE₁ (Z = 1–20) klasik üniteyle aynı", all(ie1[s] == v for s, v in k_ie.items()))
k_r = {s: v for (s, v) in _lit("rad").values()}
kontrol(f"atom yarıçapları ({len(k_r)} element) klasik üniteyle aynı", k_r == r)
k_en = {s: v for (s, v) in _lit("en").values()}
kontrol(f"elektronegatiflikler ({len(k_en)} element, Pauling) klasik üniteyle aynı", all(en[s] == v for s, v in k_en.items()))
kontrol("I = 2,7 klasik ünitenin bağlam sorusundaki değerle aynı", en["I"] == 2.7 and "2,7" in ks)
k_iyon = {f"{s}{q.replace('−', '-')}": v for s, q, _, v in _lit("ions")}
kontrol("izoelektronik seri yarıçapları klasik üniteyle aynı", all(ri[k] == v for k, v in k_iyon.items()))
kontrol("karbonun ardışık İE'leri klasik üniteyle aynı", ie["C"] == _lit("vals"))
kontrol("1A İE₁ (Li–Cs) klasik üniteyle aynı", all(ie1[s] == v for s, v in _lit("al")))
kontrol("ardışık beş element grafiği (P S Cl Ar K) klasik üniteyle aynı", [ie1[s] for _, s in TEST5] == _lit("v5"))
for ad, desen in (("Rb", r"403\D+2633\D+3860\D+5080"), ("Sr", r"549\D+1064\D+4138\D+5500"), ("Al", r"578\D+1817\D+2745\D+11577"),
                  ("Si", r"786\D+1577\D+3232\D+4356"), ("P", r"1012\D+1907\D+2914\D+4964\D+6274\D+21267"),
                  ("B", r"801, 2427, 3660, 25026"), ("O", r"1314, 3388, 5301, 7469, 10990, 13327 ve 71330")):
    kontrol(f"ardışık İE ({ad}) klasik ünitedeki tabloyla aynı", bool(re.search(desen, ks)))
kontrol("Mg İE₂ = 1451 klasik üniteyle aynı", re.search(r"İE\D{0,14}2\D{0,14}= 1451", ks) is not None and ie["Mg"][:2] == [738, 1451])
for metin, deger in (("Li+ (≈ 76 pm)", ri["Li+"]), ("Na+ (≈ 102 pm)", ri["Na+"]), ("99 → 181 pm", ri["Cl-"])):
    kontrol(f"iyon yarıçapı '{metin}' klasik ünitede", metin.replace("+", "<sup>+</sup>") in ks or metin in re.sub(r"<[^>]+>", "", ks))
kontrol("K⁺ 138 ve Ca²⁺ 100 pm klasik ünitenin bağlam tablosunda", re.search(r"102\D+72\D+138\D+100", re.sub(r"<[^>]+>", " ", ks)) is not None
        and (ri["K+"], ri["Ca2+"]) == (138, 100))
# klasik ünitede olmayan ama aynı ölçüm tablosundan alınan ardışık İE'ler (rapor: yeni veri) — tutarlılık
kontrol("ek veriler: Na, Mg, Ca İE₁'leri ana tabloyla aynı", ie["Na"][0] == ie1["Na"] and ie["Mg"][0] == ie1["Mg"] and ie["Ca"][0] == ie1["Ca"])

cerceve = os.path.join(KITAP, "yerel-cerceve", "uretec", "elementler.py")
if os.path.exists(cerceve):
    E = runpy.run_path(cerceve)
    adlar = {e["sembol"]: e["ad"] for e in E["ELEMENTLER"]}
    zler = {e["sembol"]: e["z"] for e in E["ELEMENTLER"]}
    kontrol(f"element adları kitabın tablosuyla aynı ({len(AD)} ad)", all(adlar[s] == a for s, a in AD.items()))
    kontrol(f"atom numaraları kitabın tablosuyla aynı ({len(Z)} element)", all(zler[s] == z for s, z in Z.items()))
    kontrol("sınıflar (metal · yarı metal · ametal · soy gaz · değişen) kitabın tablosuyla aynı",
            all(E["sinif"](s) == SINIF[s] for s in Z))
    for s, (p, g) in YER.items():
        per, iupac = E["yer"](zler[s])
        if not (per == p and E["ab_adi"](iupac) == f"{g}A"):
            kontrol(f"{s} yeri (periyot {p}, {g}A) kitabın tablosuyla aynı", False)
    kontrol("haritadaki 42 baş grup elementinin periyot ve grubu kitabın tablosuyla aynı", True)
else:
    print("UYARI: elementler.py yok; ad/sınıf denetimi atlandı")

# ================================================================== 2. EĞİLİMLER (VERI'den)


def per(s):
    return YER[s][0]


def grp(s):
    return YER[s][1]


aykiri = []
for s1, s2 in itertools.permutations(r, 2):
    if grp(s1) == grp(s2) and per(s1) < per(s2) and not r[s1] < r[s2]:
        aykiri.append((s1, s2))
    if per(s1) == per(s2) and grp(s1) < grp(s2) and not r[s1] > r[s2]:
        aykiri.append((s1, s2))
kontrol(f"atom yarıçapı: grupta aşağı artar, periyotta sağa azalır; tek istisna Al > Ga (sayfada yazılı) {aykiri}", aykiri == [("Al", "Ga")])
istisna = {(2, 3), (5, 6)}
for p, ad in ((2, "2."), (3, "3.")):
    sira = [s for s in IE_SIRA if per(s) == p]
    adimlar = [(grp(a), grp(b), ie1[b] > ie1[a]) for a, b in zip(sira, sira[1:])]
    kontrol(f"İE₁ {ad} periyot: yalnız 2A→3A ve 5A→6A'da düşer {[(a, b) for a, b, art in adimlar if not art]}",
            all(art != ((a, b) in istisna) for a, b, art in adimlar))
kontrol("İE₁ grupta azalır: Li > Na > K > Rb > Cs, Be > Mg > Ca > Sr, H > Li",
        ie1["Li"] > ie1["Na"] > ie1["K"] > ie1["Rb"] > ie1["Cs"] and ie1["Be"] > ie1["Mg"] > ie1["Ca"] > ie1["Sr"] and ie1["H"] > ie1["Li"])
kontrol("her periyotta en büyük İE₁ soy gaz, en küçüğü alkali metal",
        all(max((s for s in IE_SIRA if per(s) == p), key=ie1.get) == {1: "He", 2: "Ne", 3: "Ar"}[p] for p in (1, 2, 3))
        and all(min((s for s in IE_SIRA if per(s) == p), key=ie1.get) == {2: "Li", 3: "Na"}[p] for p in (2, 3)))
ok = True
for s1, s2 in itertools.permutations(en, 2):
    if s1 == "H" or s2 == "H":
        continue
    if grp(s1) == grp(s2) and per(s1) < per(s2) and not en[s1] > en[s2]:
        ok = False
    if per(s1) == per(s2) and grp(s1) < grp(s2) and not en[s1] < en[s2]:
        ok = False
kontrol("EN: periyotta sağa artar, grupta aşağı azalır; istisna yok (Pauling)", ok)
kontrol("EN en büyük F (4,0); soy gazlara değer yok", max(en, key=en.get) == "F" and en["F"] == 4.0 and not any(SINIF[s] == "soy" for s in en))


def daha_metalik(a, b):
    """a, b'den kesin daha metalik mi? (konum: aşağıda ve solda; ikisi birden ya da biri eşit)"""
    return per(a) >= per(b) and grp(a) <= grp(b) and (per(a), grp(a)) != (per(b), grp(b))


def oranlar(dizi):
    return [b / a for a, b in zip(dizi, dizi[1:])]


def grup_bul(dizi, esik=3):
    """En büyük oran ≥ eşikse, ondan önce kopan elektron sayısı (= baş grup numarası); yoksa None."""
    o = oranlar(dizi)
    m = max(o)
    return o.index(m) + 1 if m >= esik else None


beklenen_grup = {"C": 4, "Rb": 1, "Sr": 2, "Al": 3, "Si": None, "P": 5, "B": 3, "O": 6, "Mg": 2, "Na": 1, "Ca": 2}
for s, g in beklenen_grup.items():
    kontrol(f"ardışık İE {s}: oranlar {[vir(x) for x in oranlar(ie[s])]} → grup {g}", grup_bul(ie[s]) == g)
    if g and s in YER:
        kontrol(f"  {s} kitapta {g}A grubunda", grp(s) == g)
kontrol("ardışık İE'ler hep artar (İE₁ < İE₂ < …)", all(all(b > a for a, b in zip(v, v[1:])) for v in ie.values()))

# tanecik boyu modeli: önce elektron bulunan katman sayısı, sonra p/e (küçük p/e → büyük)


def katmanlar(e):
    if e <= 20:
        k, kal = [], e
        for c in (2, 8, 8, 2):
            if kal <= 0:
                break
            k.append(min(c, kal))
            kal -= c
        return k
    return {36: [2, 8, 18, 8]}[e]


def tanecik(ad):
    m = re.fullmatch(r"([A-Z][a-z]?)(\d?)([+-]?)", ad)
    s, n, isaret = m.groups()
    q = (int(n) if n else 1) * (1 if isaret == "+" else -1) if isaret else 0
    p = Z[s]
    return p, p - q


def boy(ad):
    p, e = tanecik(ad)
    return (len(katmanlar(e)), -p / e)


def _model_gecerli(a, b):
    """model: aynı element, izoelektronik ya da aynı yüklü iyonlar (+ sayfadaki K⁺–F⁻ örneği)."""
    pa, ea = tanecik(a)
    pb, eb = tanecik(b)
    return pa == pb or ea == eb or (pa - ea) == (pb - eb) or {a, b} == {"K+", "F-"}


ciftler = [(a, b) for a, b in itertools.combinations(ri, 2) if _model_gecerli(a, b)]
ok = all((boy(a) > boy(b)) == (ri[a] > ri[b]) for a, b in ciftler)
kontrol(f"iyon yarıçapı modeli (katman, p/e) VERI ile uyumlu: {len(ciftler)} çift (aynı element, izoelektronik, aynı yük)", ok)
kontrol("atom ve iyonu: Na > Na⁺, Cl⁻ > Cl (VERI)", r["Na"] > ri["Na+"] and ri["Cl-"] > r["Cl"])

# ================================================================== 3. DURAK GÖREVLERİ
# 1. durak
kontrol("Kavram görevi: Cl₂'de d = 198 pm → r = 99 pm (VERI)", 198 / 2 == r["Cl"])
g1 = sorted(["O", "Mg", "Si", "Ca"], key=r.get, reverse=True)
kontrol(f"Görev 1: {' > '.join(g1)} = Ca > Mg > Si > O", g1 == ["Ca", "Mg", "Si", "O"])
kontrol("Görev 1 adım 2: Ca–Mg aynı grup, Mg–Si aynı periyot, Si bir alt periyotta (O'dan)",
        grp("Ca") == grp("Mg") == 2 and per("Mg") == per("Si") == 3 and per("Si") == per("O") + 1)
kontrol("Hızlı 1: Na, Al, K → en büyük K, en küçük Al", max(["Na", "Al", "K"], key=r.get) == "K" and min(["Na", "Al", "K"], key=r.get) == "Al")
kontrol("Tuzak 1: Mg 160 < Na 186 (aynı periyot)", r["Mg"] < r["Na"] and per("Mg") == per("Na"))
kontrol("Çapraz durum: Li 152 > Cl 99 (Li üstte ama büyük)", r["Li"] > r["Cl"] and per("Li") < per("Cl"))
kontrol("Yoldan: K (4 katman) 227 > Na (3 katman) 186", r["K"] > r["Na"] and len(katmanlar(19)) == 4 and len(katmanlar(11)) == 3)
# 2. durak
pe = {"Fe": 26 / 26, "Fe2+": 26 / 24, "Fe3+": 26 / 23}
kontrol(f"Görev 2A: p/e 1 · {vir(pe['Fe2+'], 2)} · {vir(pe['Fe3+'], 2)} → Fe > Fe²⁺ > Fe³⁺",
        vir(pe["Fe2+"], 2) == "1,08" and vir(pe["Fe3+"], 2) == "1,13" and pe["Fe"] < pe["Fe2+"] < pe["Fe3+"])
g2b = sorted(["S2-", "Cl-", "K+", "Ca2+"], key=boy, reverse=True)
kontrol(f"Görev 2B: hepsi 18 e⁻, {g2b} = S²⁻ > Cl⁻ > K⁺ > Ca²⁺",
        g2b == ["S2-", "Cl-", "K+", "Ca2+"] and {tanecik(x)[1] for x in g2b} == {18})
kontrol("Hızlı 2: Cl⁻ > K⁺ (18 e⁻; 17 < 19 proton)", boy("Cl-") > boy("K+") and ri["Cl-"] > ri["K+"])
kontrol("Tuzak 2: K⁺ (3 katman, 138) > F⁻ (2 katman, 133)", ri["K+"] > ri["F-"] and len(katmanlar(18)) == 3 and len(katmanlar(10)) == 2)
kontrol("Kromit FeCr₂O₄ yük dengesi: 2 + 2·3 − 4·2 = 0", 2 + 2 * 3 - 4 * 2 == 0)
kontrol("Manyetit Fe₃O₄: Fe²⁺ + 2 Fe³⁺ = 8 = 4·2", 2 + 2 * 3 == 4 * 2)
# 3. durak
g3 = sorted(["Si", "P", "S", "Cl"], key=ie1.get, reverse=True)
kontrol(f"Görev 3: {' > '.join(g3)} = Cl > P > S > Si (5A > 6A istisnası)", g3 == ["Cl", "P", "S", "Si"] and ie1["P"] > ie1["S"])
p3 = [s for s in IE_SIRA if per(s) == 3]
kontrol("Hızlı 3: 3. periyotta en kolay Na, en zor Ar", min(p3, key=ie1.get) == "Na" and max(p3, key=ie1.get) == "Ar")
kontrol("İki istisna: Be 899 > B 801, Mg 738 > Al 578, N 1402 > O 1314, P 1012 > S 1000",
        (ie1["Be"], ie1["B"], ie1["Mg"], ie1["Al"], ie1["N"], ie1["O"], ie1["P"], ie1["S"]) == (899, 801, 738, 578, 1402, 1314, 1012, 1000))
kontrol("Tuzak 3: iyonlaşma hep enerji ister (bütün İE > 0)", all(v > 0 for v in ie1.values()))
# 4. durak
kontrol(f"karbon oranları {[vir(x) for x in oranlar(ie['C'])]} = ×2,2 ×2,0 ×1,3 ×6,1",
        [vir(x) for x in oranlar(ie["C"])] == ["2,2", "2,0", "1,3", "6,1"])
g4 = {h: grup_bul(ie[s]) for h, s in (("X", "Rb"), ("Y", "Sr"), ("Z", "Al"), ("T", "Si"))}
kontrol(f"Görev 4: {g4} = X 1A · Y 2A · Z 3A · T kesinleşmez", g4 == {"X": 1, "Y": 2, "Z": 3, "T": None})
kontrol("Görev 4 adımları: X ≈ 6,5 · Y 1,9 3,9 1,3 · Z 3,1 1,5 4,2 (ilk oran da > 3) · T 2,0 2,0 1,3",
        vir(oranlar(ie["Rb"])[0]) == "6,5" and [vir(x) for x in oranlar(ie["Sr"])] == ["1,9", "3,9", "1,3"]
        and [vir(x) for x in oranlar(ie["Al"])] == ["3,1", "1,5", "4,2"] and oranlar(ie["Al"])[0] > 3
        and [vir(x) for x in oranlar(ie["Si"])] == ["2,0", "2,0", "1,3"])
kontrol("Hızlı 4: 738 · 1451 · 7733 → 2A (ilk üç değer)", grup_bul(ie["Mg"][:3]) == 2)
kontrol("Tuzak 4: Mg İE₂ 1451 > İE₁ 738", ie["Mg"][1] > ie["Mg"][0])
# 5. durak
g5a = sorted(["N", "O", "P", "K"], key=en.get, reverse=True)
kontrol(f"Görev 5A: {' > '.join(g5a)} = O > N > P > K", g5a == ["O", "N", "P", "K"])
fark = {b: round(en[b[0]] - en["H"], 1) for b in ("O", "N", "C")}
kontrol(f"Görev 5B: farklar O–H {vir(fark['O'])} · N–H {vir(fark['N'])} · C–H {vir(fark['C'])} → O–H > N–H > C–H",
        (vir(fark["O"]), vir(fark["N"]), vir(fark["C"])) == ("1,2", "0,8", "0,4"))
kontrol("Hızlı 5: H–F (1,8) daha polar H–Cl (1,0)", round(en["F"] - en["H"], 1) == 1.8 and round(en["Cl"] - en["H"], 1) == 1.0)
kontrol("Halat: O (3,4) δ⁻, H (2,2) δ⁺; fark 1,2", en["O"] > en["H"] and round(en["O"] - en["H"], 1) == 1.2)
# 6. durak
g6 = sorted(["Na", "Mg", "Al", "K"], key=en.get)
kontrol(f"Görev 6: metalik karakter (EN küçükten) {' > '.join(g6)} = K > Na > Mg > Al",
        g6 == ["K", "Na", "Mg", "Al"] and daha_metalik("K", "Na") and daha_metalik("Na", "Mg") and daha_metalik("Mg", "Al"))
kontrol("Görev 6 notu: Al İE₁ < Mg İE₁ ama Al için 3 elektron: 5140 > 2189 kJ/mol",
        ie1["Al"] < ie1["Mg"] and sum(ie["Al"][:3]) == 5140 and sum(ie["Mg"][:2]) == 2189)
kontrol("Hızlı 6: K, Ca'dan aktif (aynı periyot, alkali)", daha_metalik("K", "Ca") and ie1["K"] < ie1["Ca"])
kontrol("Tuzak 6: H ametal; İE₁ 1312 alkalilerden çok büyük", SINIF["H"] == "ametal" and all(ie1["H"] > ie1[s] for s in ("Li", "Na", "K", "Rb", "Cs")))
kontrol("Galen PbS: Pb metal, S ametal (kitabın tablosu)", SINIF["Pb"] == "metal" and SINIF["S"] == "ametal")
kontrol("Harita: en metalik Cs (sol alt), en ametalik F (sağ üst)", TABLO[5][0] == "Cs" and TABLO[1][6] == "F")

# ================================================================== 4. MECLİS · KISSA · MERDİVEN
mec = {}
mec["M1"] = r["K"] > r["Ca"]                                           # öğrenci "Ca > K" demiş: yanlış
mec["M2"] = tanecik("S2-")[0] / tanecik("S2-")[1] < 1 and vir(16 / 18, 2) == "0,89"   # p/e küçük → büyük
mec["M3"] = ie1["Be"] > ie1["B"]                                       # "İE₁(B) > İE₁(Be)" yanlış
mec["M4"] = grup_bul(ie["B"]) == 3 and oranlar(ie["B"])[0] > 3 and [vir(x) for x in oranlar(ie["B"])] == ["3,0", "1,5", "6,8"]
for k, v in mec.items():
    kontrol(f"Meclis {k}: öğrenci çözümündeki hata gerçekten hata", v)
MECLIS = {"M1": ("Elif", 2), "M2": ("Pamuk", 3), "M3": ("Yusuf", 3), "M4": ("Yusuf", 2)}

K = {}
d = yargi({"I": ri["K+"] > ri["Na+"] and len(katmanlar(18)) > len(katmanlar(10)),
           "II": tanecik("Na+")[1] == tanecik("Mg2+")[1] and ri["Mg2+"] < ri["Na+"],
           "III": len(katmanlar(tanecik("Ca2+")[1])) < len(katmanlar(tanecik("K+")[1]))})
K[1] = tek_sik("Kıssa 1 (maden suyu iyonları)", YARGI_A, lambda v: v == d, "C")
k2 = {"A": False, "B": len(katmanlar(10)) > len(katmanlar(2)), "C": False, "D": Z["Na"] < Z["Li"],
      "E": 11 / 10 > 3 / 2}
K[2] = tek_sik("Kıssa 2 (Na⁺ > Li⁺ nedeni)", k2, bool, "B")
alk = ["Li", "Na", "K", "Rb", "Cs"]
k3 = {"A": all(ie1[a] > ie1[b] for a, b in zip(alk, alk[1:])), "B": min(alk, key=ie1.get) == "Cs",
      "C": ie1["Rb"] < ie1["K"], "D": daha_metalik("Li", "Cs"), "E": True}
K[3] = tek_sik("Kıssa 3 (yanlış olan)", k3, lambda v: not v, "D")
hx = ["F", "Cl", "Br", "I"]
fk = [round(en[x] - en["H"], 1) for x in hx]
k4 = {"A": fk == sorted(fk, reverse=True) and len(set(fk)) == 4, "B": max(hx, key=lambda x: en[x] - en["H"]) == "I",
      "C": any(en["H"] > en[x] for x in hx), "D": en["H"] > en["Br"], "E": en["F"] < en["Cl"]}
K[4] = tek_sik("Kıssa 4 (HF ve halojenler)", k4, bool, "A")
kontrol(f"Kıssa 4 farkları {[vir(x) for x in fk]} = 1,8 · 1,0 · 0,8 · 0,5", [vir(x) for x in fk] == ["1,8", "1,0", "0,8", "0,5"])

# merdiven
o_or = [vir(x) for x in oranlar(ie["O"])]
kontrol(f"Merdiven 1: oranlar {o_or} → 6A, 2-6 → Z = 8, 8 İE",
        o_or == ["2,6", "1,6", "1,4", "1,5", "1,2", "5,4"] and grup_bul(ie["O"]) == 6 and sum([2, 6]) == Z["O"] == 8 and len(ie["O"]) == 7)
m2 = sorted(["F-", "Na+", "Cl-", "K+"], key=boy, reverse=True)
kontrol(f"Merdiven 2: {m2} = Cl⁻ > K⁺ > F⁻ > Na⁺ (181 · 138 · 133 · 102)",
        m2 == ["Cl-", "K+", "F-", "Na+"] and [ri[x] for x in m2] == [181, 138, 133, 102])
m3_deg = [1086, 1402, 1314, 1681, 2081, 496]
harf = list("XYZTQR")
dus = min(range(5), key=lambda i: m3_deg[i + 1] - m3_deg[i])
soy = harf[dus]
bes_a = harf[dus - 3]
kontrol(f"Merdiven 3: soy gaz {soy}, 5A {bes_a}, en büyük atom R; elementler C N O F Ne Na",
        soy == "Q" and bes_a == "Y" and [ie1[s] for s in ("C", "N", "O", "F", "Ne", "Na")] == m3_deg and per("Na") == per("Ne") + 1)

# ================================================================== 5. BÜYÜK İMTİHAN
T = {}
sira1 = sorted(["Be", "Mg", "Al", "K"], key=r.get, reverse=True)
i1 = {"A": ["Be", "Mg", "Al", "K"], "B": ["K", "Al", "Mg", "Be"], "C": ["K", "Mg", "Al", "Be"], "D": ["Mg", "K", "Al", "Be"], "E": ["Al", "Mg", "Be", "K"]}
T[1] = tek_sik("İmtihan 1 (atom yarıçapı)", i1, lambda v: v == sira1, "C")
sira2 = sorted(["Se2-", "Br-", "Rb+", "Sr2+"], key=boy, reverse=True)
kontrol("İmtihan 2: dördü de 36 elektronlu", {tanecik(x)[1] for x in sira2} == {36})
i2 = {"A": ["Se2-", "Br-", "Rb+", "Sr2+"], "B": ["Sr2+", "Rb+", "Br-", "Se2-"], "C": ["Br-", "Se2-", "Rb+", "Sr2+"], "D": ["Rb+", "Sr2+", "Se2-", "Br-"], "E": ["Se2-", "Br-", "Sr2+", "Rb+"]}
T[2] = tek_sik("İmtihan 2 (izoelektronik 36 e⁻)", i2, lambda v: v == sira2, "A")
d3 = yargi({"I": True, "II": len(katmanlar(10)) < len(katmanlar(12)), "III": False})
T[3] = tek_sik("İmtihan 3 (Mg → Mg²⁺)", YARGI_I3, lambda v: v == d3, "D")
sira4 = sorted(["Be", "B", "N", "O"], key=ie1.get, reverse=True)
i4 = {"A": ["O", "N", "B", "Be"], "B": ["N", "O", "Be", "B"], "C": ["O", "N", "Be", "B"], "D": ["N", "O", "B", "Be"], "E": ["Be", "B", "N", "O"]}
T[4] = tek_sik("İmtihan 4 (İE₁, iki istisna)", i4, lambda v: v == sira4, "B")
# değişim: (başlangıç hâli, başlangıç yükü, son yük) → İE₁'e eşit mi?
i5 = {"A": ("k", 0, 1), "B": ("g", 1, 2), "C": ("g", 0, 1), "D": ("g", 0, 2), "E": ("k", 0, 0)}
T[5] = tek_sik("İmtihan 5 (İE₁ tanımı)", i5, lambda v: v == ("g", 0, 1), "C")
i6 = {"A": 2, "B": 3, "C": 4, "D": 6, "E": 5}
T[6] = tek_sik("İmtihan 6 (fosforun ardışık İE'leri)", i6, lambda v: v == grup_bul(ie["P"]), "E")
kontrol("İmtihan 6 oranları ≈ 1,9 · 1,5 · 1,7 · 1,3 · 3,4", [vir(x) for x in oranlar(ie["P"])] == ["1,9", "1,5", "1,7", "1,3", "3,4"])
pe7 = {"Cl+": 17 / 16, "Cl": 1, "Cl-": 17 / 18}
sira7 = sorted(pe7, key=pe7.get, reverse=True)
i7 = {"A": ["Cl+", "Cl", "Cl-"], "B": ["Cl-", "Cl", "Cl+"], "C": ["Cl", "Cl+", "Cl-"], "D": None, "E": ["Cl-", "Cl+", "Cl"]}
T[7] = tek_sik("İmtihan 7 (katyon > atom > anyon)", i7, lambda v: v == sira7, "A")
IE1_, IE2_, SUB = 1.0, 2.0, .5          # sembolik: hâl değişimi > 0, İE₂ > İE₁
Q1, Q2, Q3 = SUB + IE1_, IE2_, IE1_ + IE2_
i8 = {"A": Q1 == IE1_, "B": Q3 == IE2_, "C": Q1 < IE1_, "D": Q2 == IE2_, "E": Q3 < Q2}
T[8] = tek_sik("İmtihan 8 (Q₁ Q₂ Q₃)", i8, bool, "D")
d9 = yargi({"I": en["N"] > en["C"] > en["Si"], "II": r["Si"] > r["C"] > r["N"], "III": ie1["C"] > ie1["N"] > ie1["Si"]})
T[9] = tek_sik("İmtihan 9 (C, N, Si)", YARGI_I9, lambda v: v == d9, "B")
i10 = {"A": ("Mg", "Na"), "B": ("Al", "Mg"), "C": ("Li", "K"), "D": ("Ca", "Al"), "E": ("S", "P")}
T[10] = tek_sik("İmtihan 10 (ilk yazılan daha metalik)", i10, lambda c: daha_metalik(*c) and en[c[0]] < en[c[1]], "D")
el5 = dict(TEST5)
kontrol("İmtihan 11: tepe T, hemen ardından dip Q → T soy gaz, Q alkali",
        max(el5, key=lambda h: ie1[el5[h]]) == "T" and min(el5, key=lambda h: ie1[el5[h]]) == "Q" and SINIF[el5["T"]] == "soy")
i11 = {"A": SINIF[el5["T"]] == "soy", "B": max(["X", "Y", "Z", "Q"], key=lambda h: r[el5[h]]) == "Q",
       "C": grp(el5["X"]) == 5, "D": max(["X", "Y", "Z", "Q"], key=lambda h: en[el5[h]]) == "Z", "E": r[el5["Y"]] < r[el5["Z"]]}
T[11] = tek_sik("İmtihan 11 (yanlış olan)", i11, lambda v: not v, "E")
kes = {h: TABLO[p - 1][g - 1] for h, (p, g) in KESIT.items()}
kontrol(f"İmtihan 12 kesiti: {kes} = Li N F Na S", kes == {"X": "Li", "Y": "N", "Z": "F", "T": "Na", "Q": "S"})
i12 = {"A": max(kes, key=lambda h: r[kes[h]]) == "T", "B": ie1[kes["Q"]] > ie1[kes["Y"]], "C": max(kes, key=lambda h: en[kes[h]]) == "Z",
       "D": min(kes, key=lambda h: en[kes[h]]) == "T", "E": grp(kes["X"]) == grp(kes["T"])}
T[12] = tek_sik("İmtihan 12 (yanlış olan)", i12, lambda v: not v, "B")
dagilim(T.values())
DURAK_ET = {1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4, 7: 4, 8: 4, 9: 5, 10: 6, 11: 3, 12: 6}
kontrol("İmtihan her durağa en az bir soru sorar", set(DURAK_ET.values()) == set(range(1, 7)))

# ================================================================== 6. ÜSTAD (bonus)
U = {}
xyz = {"X": ie["Na"], "Y": ie["Mg"], "Z": ie["Al"]}
gr = {h: grup_bul(v) for h, v in xyz.items()}
d = yargi({"I": gr["Y"] == 2, "II": max(gr, key=gr.get) == "Z", "III": xyz["X"][1] > xyz["Y"][1]})
U[1] = tek_sik("Üstad 1 (tablo · ardışık İE)", YARGI_I9, lambda v: v == d, "E")
kontrol("Üstad 1 grupları X 1A, Y 2A, Z 3A", gr == {"X": 1, "Y": 2, "Z": 3})
u2 = [ie1[s] for s in USTAD8]
tepe = max(range(7), key=lambda i: u2[i] - u2[i + 1])
d = yargi({"I": tepe + 1 == 4 and SINIF[USTAD8[3]] == "soy", "II": grp(USTAD8[0]) == 5, "III": r[USTAD8[7]] > r[USTAD8[4]]})
U[2] = tek_sik("Üstad 2 (sekiz ardışık element)", YARGI_U2, lambda v: v == d, "C")
u3 = round(.2 * sum(ie["Al"][:3]), 1)
U[3] = tek_sik("Üstad 3 (0,2 mol Al → Al³⁺)", {"A": 115.6, "B": 1028, "C": 549, "D": 1542, "E": 5140}, lambda v: abs(v - u3) < 1e-6, "B")
kontrol("Üstad 3 çeldiricileri: 0,2·İE₁ · 0,2·İE₃ · 0,3·toplam · 1 mol", (round(.2 * 578, 1), round(.2 * 2745), round(.3 * 5140), 5140) == (115.6, 549, 1542, 5140))
ca = ie["Ca"]
kontrol("Üstad 4: X 2A (sıçrama 2'den sonra), 4. periyot → Ca (Z = 20)", grup_bul(ca) == 2 and TABLO[3][1] == "Ca" and Z["Ca"] == 20)
d = yargi({"I": ca[0] + ca[1] == 1735, "II": Z["Ca"] - 2 == Z["Ar"], "III": ca[0] < ie1["K"]})
U[4] = tek_sik("Üstad 4 (ardışık İE · izoelektronik)", YARGI_U4, lambda v: v == d, "A")
dort = {"X": "O2-", "Y": "F-", "Z": "Na+", "T": "Mg2+"}
kontrol("Üstad 5: dördü de 10 elektronlu → O, F, Na, Mg", {tanecik(v)[1] for v in dort.values()} == {10})
d = yargi({"I": sorted(dort, key=lambda h: boy(dort[h]), reverse=True) == ["X", "Y", "Z", "T"],
           "II": max(dort, key=lambda h: en[re.match(r"[A-Z][a-z]?", dort[h]).group()]) == "Y",
           "III": max(dort, key=lambda h: ie1[re.match(r"[A-Z][a-z]?", dort[h]).group()]) == "Z"})
U[5] = tek_sik("Üstad 5 (izoelektronik dörtlü)", YARGI_U5, lambda v: v == d, "D")
uygun = [p for p in itertools.permutations("XYZ") if p.index("X") < p.index("Y") < p.index("Z")]
u6 = {"A": tuple("XYZ"), "B": tuple("YXZ"), "C": tuple("ZYX"), "D": tuple("XZY"), "E": tuple("YZX")}
kontrol(f"Üstad 6: koşullara uyan tek sıra {uygun}", uygun == [tuple("XYZ")])
U[6] = tek_sik("Üstad 6 (kısmi yük · çıkarım)", u6, lambda v: v in uygun, "A")
dagilim(U.values())

# ================================================================== 7. SAYFADAN OKUNANLAR
html = sayfa_oku(__file__)
if html:
    duz = _html.unescape(re.sub(r"<[^>]+>", "", html))
    beklenen = {f"I{k}": v for k, v in T.items()}
    beklenen.update({f"K{k}": v for k, v in K.items()})
    beklenen.update({f"U{k}": v for k, v in U.items()})
    sayfa_isaretleri_ayni(html, beklenen)
    izgara = anahtar_izgarasi(html)
    kontrol(f"Cevaplar: anahtar ızgarası hesapla aynı {izgara}", izgara == T)
    et = dict((int(n), int(dno)) for n, dno in re.findall(r"<i>(\d+)</i><b>[A-E]</b><small>(\d)\. durak</small>", html))
    kontrol("Cevaplar: ızgaradaki durak etiketleri", et == DURAK_ET)
    for no, h in T.items():
        kontrol(f"Cevaplar: çözüm satırı '{no} · {h}' var", f"<b>{no} · {h}</b>" in html)
    for k, h in K.items():
        kontrol(f"Cevaplar: kıssa çözümü '{k} · {h}' var", f"<b>{k} · {h}</b>" in html)
    for k, h in U.items():
        kontrol(f"Cevaplar: Üstad çözümü 'Ü{k} · {h}' var", f"<b>Ü{k} · {h}</b>" in html)
    for ad, sozluk in (("Kıssa", K), ("Üstad", U)):
        m = re.search(rf"<p><b>{ad}</b>(.*?)</p>", html)
        kontrol(f"Cevaplar: hızlı anahtar '{ad}' satırı hesapla aynı",
                bool(m) and re.findall(r'<span class="ck">(\d) ([A-E])</span>', m.group(1)) == [(str(k), v) for k, v in sozluk.items()])
    mh = meclis_hukumleri(html)
    kontrol(f"Meclis hükümleri (haklı kişi, satır) {mh}", mh == MECLIS)
    m = re.search(r"<p><b>Meclis</b>(.*?)</p>", html)
    kontrol("Cevaplar: hızlı anahtar 'Meclis' satırı hükümlerle aynı",
            bool(m) and re.findall(r'<span class="ck">\d (\w+)</span>', m.group(1)) == [MECLIS[f"M{i}"][0] for i in range(1, 5)])
    for i in range(1, 5):
        kontrol(f"Cevaplar: meclis çözümü '{i} · {MECLIS[f'M{i}'][0]}' ve 'Satır {MECLIS[f'M{i}'][1]}'",
                f"<b>{i} · {MECLIS[f'M{i}'][0]}</b> Satır {MECLIS[f'M{i}'][1]}:" in html)
    nedenler = [_html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r'NEDEN\?<span class="cizgili"><span class="ogr">(.*?)</span></span>', html)]
    dogrular = [_html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r'DOĞRUSU<span class="cizgili"><span class="ogr">(.*?)</span></span>', html)]
    kontrol(f"Meclis NEDEN ≤ 14 harf {[len(x) for x in nedenler]}", len(nedenler) == 4 and all(len(x) <= 14 for x in nedenler))
    kontrol(f"Meclis DOĞRUSU ≤ 45 harf {[len(x) for x in dogrular]}", len(dogrular) == 4 and all(len(x) <= 45 for x in dogrular))
    mrd = [_html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r'<div><span class="ogr">(.*?)</span></div>', html)]
    kontrol(f"Merdiven çözüm satırları ≤ 50 harf ({len(mrd)} satır)", len(mrd) == 9 and all(len(x) <= 50 for x in mrd))
    kar = [_html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r'<div class="karalama"><span class="ogr">(.*?)</span></div>', html)]
    kontrol(f"Karalama çözümleri ≤ 72 harf ({len(kar)} kart)", len(kar) == 22 and all(len(x) <= 72 for x in kar))
    ogr = ogretmen_metinleri(html)
    kontrol(f"öğretmen metinleri: {len(ogr)} (1 kavram + 6 CEVABIN + 8 meclis + 4 kıssa + 9 merdiven + 12 imtihan + 6 Üstad = 46)", len(ogr) == 46)
    ciftler = re.findall(r'CEVABIN:<span class="ogr">(.*?)</span></div><span class="ters-cevap"><span class="ters">(.*?)</span></span>', html)
    kontrol(f"CEVABIN kırmızı cevabı ters yazılı cevapla aynı ({len(ciftler)} kutu)", len(ciftler) == 6 and all(a == b for a, b in ciftler))
    kontrol("Üstad sayfası: 6 kart, grafik (ustad-graf) ve tablo, Üstad Mührü",
            html.count('class="ustad-soru"') == 6 and "ustad-graf" in html and 'class="ustad-tablo"' in html and "Üstad Mührü" in html)
    kontrol("12 meşveret + 4 kıssa + 4 meclis kartı", html.count('class="kart mesveret"') == 12 and html.count('class="kart kissa"') == 4
            and html.count('class="kart meclis"') == 4)
    # hazine kartları: her biri tam bir kez, kendi durağının sayfasında
    meta = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
    bolumler = re.split(r'(?=<section class="sayfa s\d+)', html)
    for h in meta["hazine"]:
        sayfa = meta["duraklar"][h["durak"] - 1]["sayfa"]
        bl = next(b for b in bolumler if b.startswith(f'<section class="sayfa s{sayfa} ') or b.startswith(f'<section class="sayfa s{sayfa}"'))
        kartlar = re.findall(r'<div class="hazine[^"]*">(.*?)<svg class="sikke"', bl, re.S)
        kontrol(f"hazine kartı {h['kod']} {sayfa}. sayfada (durak {h['durak']})", sum(f">{h['kod']}</text>" in k for k in kartlar) == 1)
    # Pauling ölçeği yazılı; sayfadaki "Sembol d,d" EN değerleri VERI ile aynı
    kontrol("ölçek yazılı: 'Pauling ölçeği' ve 'F = 4,0'", "Pauling ölçeği" in duz and "F = 4,0" in duz)
    yanlis_en = [(s, v) for s, v in re.findall(r"\b(H|Li|Be|B|C|N|O|F|Na|Mg|Al|Si|P|S|Cl|K|Ca|Br|I) (\d,\d)\b", duz) if vir(en[s]) != v]
    kontrol(f"sayfadaki 'Sembol d,d' EN değerleri VERI ile aynı (aykırı: {yanlis_en})", not yanlis_en)
    yanlis_ie = [(s, v) for s, v in re.findall(r"\b(H|He|Li|Be|B|C|N|O|F|Ne|Na|Mg|Al|Si|P|S|Cl|Ar|K|Ca|Rb|Cs) \(?(\d{3,4})\)?(?! pm)", duz)
                 if int(v) >= 370 and ie1[s] != int(v)]
    kontrol(f"sayfadaki 'Sembol sayı' İE₁ değerleri VERI ile aynı (aykırı: {yanlis_ie})", not yanlis_ie)
    yanlis_r = [(s, v) for s, v in re.findall(r"\b(Li|Be|B|C|N|O|F|Na|Mg|Al|Si|P|S|Cl|K|Ca)\s\(?(\d{2,3})\)?\s?(?:pm|&gt;|>|<|\)|·)", duz)
                if int(v) < 370 and r[s] != int(v)]
    kontrol(f"sayfadaki atom yarıçapı sayıları VERI ile aynı (aykırı: {yanlis_r})", not yanlis_r)
    for metin in ("1314 · 3388 · 5301 · 7469 · 10 990 · 13 327 · 71 330", "1012 · 1907 · 2914 · 4964 · 6274 · 21 267",
                  "801, 2427, 3660 ve 25 026", "1086 · 1402 · 1314 · 1681 · 2081 · 496", "738 · 1451 · 7733",
                  "590, 1145, 4912 ve 6491", "578, 1817 ve 2745", "Turan Melek Sultan", "1228", "UNESCO Dünya Mirası"):
        kontrol(f"sayfada '{metin}' var", metin in duz)
    kontrol("Medeniyetimizden: Divriği Darüşşifası hastane (şifahane) olarak anlatılır; caminin adı yalnız UNESCO bilgisinde",
            "Divriği Darüşşifası" in duz and "hastane" in duz and duz.count("Ulu Cami") == 1)
else:
    print("UYARI: unite.html yok; önce python3 uretec/kur.py çalıştır.")

# ================================================================== 8. AKÇE
meta = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
toplamlar = [d["akce"] for d in meta["duraklar"]]
kontrol(f"Durak akçeleri {toplamlar} = 100 + 5 × 120", toplamlar == [100, 120, 120, 120, 120, 120])
if html:
    for d in meta["duraklar"]:
        bl = next(b for b in re.split(r'(?=<section class="sayfa s\d+)', html) if b.startswith(f'<section class="sayfa s{d["sayfa"]} '))
        levha = int(re.search(r'<div class="hedef">.*?<span class="cip akce">\+(\d+) akçe</span>', bl, re.S).group(1))
        cipler = re.findall(r'<span class="cip akce">\+(\d+)(?: \+(\d+))?(?: akçe)?</span>', bl)
        toplam = sum(int(a) + int(b or 0) for a, b in cipler) - levha
        kart = len(re.findall(r'<div class="hazine[ "]', bl))
        kontrol(f"{d['no']}. durak (s.{d['sayfa']}): çipler {toplam} + {kart} hazine × 10 = levha {levha} = meta {d['akce']}",
                toplam + 10 * kart == levha == d["akce"])
yan = dict(hulasa=40, meclis=4 * 30, kissa=4 * 30, anahtar=3 * 40, imtihan=12 * 25)
toplam = sum(toplamlar) + sum(yan.values())
kontrol(f"Ünite toplam akçe {toplam} = 1400", toplam == 1400 == meta.get("akce_toplam", 1400))
kontrol("Ahilik eşikleri 400/800/1150 (%28,57 · %57,14 · %82,14)", [round(a / 1400 * 100, 2) for a in (400, 800, 1150)] == [28.57, 57.14, 82.14])
birikim = [0, 0] + [sum(toplamlar[:i]) for i in range(1, 7)] + [700 + 40, 860, 980, 1100, 1250, 1400, 1400, 1400]
from kur import SAYFA  # noqa: E402
bar = [SAYFA[n][2] for n in range(1, 17)]
kontrol(f"HUD akçe çubuğu {bar}", [round(b / 1400 * 100) for b in birikim] == bar)
kontrol("meta.json: 8 nişan (6 durak + Kale + bonus Üstad), 12 hazine kartı, Divriği Darüşşifası (1228)",
        len(meta["nisanlar"]) == 8 and meta["nisanlar"][-1].get("bonus") and [h["kod"] for h in meta["hazine"]] == [f"H{i}" for i in range(1, 13)]
        and meta["medeniyet"][0]["ad"] == "Divriği Darüşşifası" and meta["medeniyet"][0]["yil"] == "1228")
kontrol("meta.json kısa sandık biçimleri ≤ 16 harf", all(len(h["kisa"]) <= 16 for h in meta["hazine"]))

print("\nCEVAP ANAHTARI · İmtihan:", " ".join(f"{k}{v}" for k, v in T.items()), "· Kıssa:", " ".join(f"K{k}{v}" for k, v in K.items()),
      "· Üstad:", " ".join(f"Ü{k}{v}" for k, v in U.items()), "· Meclis:", " ".join(f"{k} {v[0]} s{v[1]}" for k, v in MECLIS.items()))
D.sonuc()
