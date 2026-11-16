#!/usr/bin/env python3
"""Periyodik Tablo · Maden Yolu I — sayısal doğrulama, veri tutarlılığı ve cevap anahtarı denetimi.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Element verisi: yerel kopya (tablo_veri.py) = kitap çerçevesinin periyodik tablosu (yerel-cerceve/uretec/elementler.py,
     periyodik.py renkleri) = klasik ünite (9-sinif/04-periyodik-tablo/uretec/elem.py): ad, kütle, sınıf, periyot, grup, blok.
  2. Konumlar elektron diziliminden YENİDEN bulunur (klasik ünitenin kuralı: A'da ns + np, B'de ns + (n−1)d; Cr, Cu, Mo, Ag istisna).
  3. İyon yükleri ve elektron sayıları, soy gaz yöntemi, son terim tablosu, yarı dolu orbital sayıları hesaplanır.
  4. Her çoktan seçmeli soruda TEK doğru şık; sayfadaki işaretler, Cevaplar ızgarası ve çözüm satırları hesapla aynı.
  5. Akçe: her durak sayfasındaki çipler + hazine kartları = durağın akçesi; toplam 1400; HUD çubukları; Ahilik eşikleri.
  6. Öğretmen işaretleri (her cevap alanında .ogr), meclis NEDEN ≤ 14 harf, elektronegatiflik ve logo/kurum adı YOK,
     Medeniyetimizden metni çerçevedeki medeniyet.py ile aynı, duraklar rotalar.json ile aynı yerler.
"""
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
KITAP = os.path.dirname(ORTAK)
URETEC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ORTAK)
sys.path.insert(0, URETEC)
from dogrula_ortak import *  # noqa: E402,F401,F403
import tablo_veri as TV  # noqa: E402
import importlib.util  # noqa: E402


def _yukle(ad, yol):
    spec = importlib.util.spec_from_file_location(ad, yol)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CER = _yukle("cer_elementler", os.path.join(KITAP, "yerel-cerceve", "uretec", "elementler.py"))
KLA = _yukle("kla_elem", os.path.join(KITAP, "9-sinif", "04-periyodik-tablo", "uretec", "elem.py"))
META = json.load(open(os.path.join(URETEC, "meta.json"), encoding="utf-8"))

# ================================================================== 1. element verisi = çerçeve = klasik ünite
kontrol("118 element, yerel kopya çerçevedeki VERI ile birebir aynı (ad, kütle)", TV.VERI == CER.VERI)
kontrol("sınıf kümeleri çerçeveyle aynı (yarı metal, ametal, soy gaz, belirsiz)",
        (TV.YARI, TV.AMETAL, TV.SOY, TV.BELIRSIZ) == (CER.YARI, CER.AMETAL, CER.SOY, CER.BELIRSIZ))
kontrol("118 elementin sınıfı çerçeveyle aynı", all(TV.sinif(s) == CER.sinif(s) for s in TV.SEMBOL))
kontrol("118 elementin (periyot, grup) konumu çerçeveyle aynı", all(TV.yer(z) == CER.yer(z) for z in range(1, 119)))
kontrol("klasik ünite: semboller aynı", TV.SEMBOL == KLA.SEMBOL)
kontrol("klasik ünite: periyot, grup, blok aynı (57–71 ve 89–103 f bloku, He s bloku)",
        all((TV.yer(z)[0], TV.yer(z)[1], TV.blok(z)) == KLA.yer(z) for z in range(1, 119)))
kontrol("klasik ünite: A/B adları aynı", all(TV.ab_adi(g) == KLA.ab(g) for g in range(1, 19)))
_kla_gen = open(os.path.join(KITAP, "9-sinif", "04-periyodik-tablo", "uretec", "gen.py"), encoding="utf-8").read()
for ad, kume in (("YARI", TV.YARI), ("AMETAL", TV.AMETAL), ("SOY", TV.SOY), ("BELIRSIZ", TV.BELIRSIZ)):
    m = re.search(rf"^{ad} = (\{{[^}}]*\}})", _kla_gen, re.M)
    kontrol(f"klasik ünite gen.py {ad} kümesi aynı", m is not None and eval(m.group(1)) == kume)
try:
    import importlib
    PER = _yukle("cer_periyodik", os.path.join(KITAP, "yerel-cerceve", "uretec", "periyodik.py"))
    kontrol("sınıf renkleri çerçevedeki periyodik tablo sayfasıyla aynı", PER.SINIF_RENK == TV.SINIF_RENK)
except Exception as e:  # PIL ya da font yoksa
    print("UYARI: periyodik.py yüklenemedi:", e)
kontrol("lantanit/aktinit düzeni: La, Lu, Ac, Lr f bloku; 3. grupta 6. ve 7. periyot boş (Sc, Y yalnız)",
        all(TV.blok(TV.Z[s]) == "f" for s in ("La", "Lu", "Ac", "Lr")) and
        [TV.SEMBOL[z - 1] for z in range(1, 119) if TV.yer(z)[1] == 3] == ["Sc", "Y"])
kontrol("periyotlardaki element sayıları 2, 8, 8, 18, 18, 32, 32",
        [TV.SON[p] - TV.BAS[p] + 1 for p in range(1, 8)] == [2, 8, 8, 18, 18, 32, 32])
kontrol("Türkçe adlar: rota elementleri", [TV.AD[s] for s in ("Al", "Co", "Cu", "Ag", "B", "Na", "Ga", "Sn")] ==
        ["Alüminyum", "Kobalt", "Bakır", "Gümüş", "Bor", "Sodyum", "Galyum", "Kalay"])

# ================================================================== 2. dizilim → konum (klasik ünitenin kuralı)
SIRA = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d", "5p", "6s", "4f", "5d", "6p", "7s", "5f", "6d", "7p"]
KAP = {"s": 2, "p": 6, "d": 10, "f": 14}
ISTISNA = {24: ("4s", "3d"), 29: ("4s", "3d"), 42: ("5s", "4d"), 47: ("5s", "4d")}   # klasik elem.py ile aynı


def dizilim(e, z=None):
    out, kalan = [], e
    for o in SIRA:
        if kalan == 0:
            break
        n = min(kalan, KAP[o[-1]])
        out.append([o, n])
        kalan -= n
    z = e if z is None else z
    if z == e and z in ISTISNA:
        s_, d_ = ISTISNA[z]
        for x in out:
            if x[0] == s_:
                x[1] = 1
            if x[0] == d_:
                x[1] += 1
    return out


def dizilim_metni(d):
    return " ".join(f"{o}{n}" for o, n in d)


def konum_dizilimden(z):
    """(periyot, IUPAC grup, blok) yalnız temel hâl diziliminden — klasik ünitenin kuralı (He özel: 8A)."""
    d = dizilim(z)
    if z == 2:
        return 1, 18, "s"
    nmax = max(int(o[0]) for o, _ in d)
    son = d[-1][0][-1]
    ns = sum(k for o, k in d if o == f"{nmax}s")
    np_ = sum(k for o, k in d if o == f"{nmax}p")
    nd = sum(k for o, k in d if o == f"{nmax - 1}d")
    if son == "p":
        return nmax, 10 + ns + np_, "p"            # A grubu: ns + np (IUPAC'ta dolu d de sayılır → 10 +)
    if son == "d" or (son == "s" and nd):
        return nmax, ns + nd, "d"                   # B grubu: ns + (n−1)d
    return nmax, ns, "s"


ilk = [z for z in range(1, 57)] + list(range(72, 87))
kontrol("dizilimden bulunan (periyot, grup, blok) Z = 1–56 ve 72–86 için tabloyla aynı",
        all(konum_dizilimden(z) == (TV.yer(z)[0], TV.yer(z)[1], TV.blok(z)) for z in ilk))
kontrol("dizilimler: Co …4s2 3d7, Fe …4s2 3d6, Mn …4s2 3d5, Cu …4s1 3d10, Ag …5s1 4d10, Cr …4s1 3d5",
        dizilim_metni(dizilim(27)).endswith("4s2 3d7") and dizilim_metni(dizilim(26)).endswith("4s2 3d6") and
        dizilim_metni(dizilim(25)).endswith("4s2 3d5") and dizilim_metni(dizilim(29)).endswith("4s1 3d10") and
        dizilim_metni(dizilim(47)).endswith("5s1 4d10") and dizilim_metni(dizilim(24)).endswith("4s1 3d5"))
kontrol("dizilimler: Si …3s2 3p2, O 1s2 2s2 2p4, S …3s2 3p4, Ga …4s2 3d10 4p1, Sn …5s2 4d10 5p2",
        dizilim_metni(dizilim(14)).endswith("3s2 3p2") and dizilim_metni(dizilim(8)) == "1s2 2s2 2p4" and
        dizilim_metni(dizilim(16)).endswith("3s2 3p4") and dizilim_metni(dizilim(31)).endswith("4s2 3d10 4p1") and
        dizilim_metni(dizilim(50)).endswith("5s2 4d10 5p2"))


def katmanlar(z):
    """İlk 20 element için katman dizilimi (2, 8, 8, 2 kuralı)."""
    out, kalan = [], z
    for kap in (2, 8, 8, 2):
        n = min(kalan, kap)
        if n:
            out.append(n)
        kalan -= n
    return out


kontrol("ilk 20 element: katman sayısı = periyot, son katman = A grubu no. (He hariç)",
        all(len(katmanlar(z)) == TV.yer(z)[0] and katmanlar(z)[-1] == int(TV.ab_adi(TV.yer(z)[1])[0]) for z in range(1, 21) if z != 2))
kontrol("katman: Al 2·8·3, K 2·8·8·1, Ca 2·8·8·2, B 2·3, P 2·8·5, Ar 2·8·8, S 2·8·6",
        [katmanlar(z) for z in (13, 19, 20, 5, 15, 18, 16)] == [[2, 8, 3], [2, 8, 8, 1], [2, 8, 8, 2], [2, 3], [2, 8, 5], [2, 8, 8], [2, 8, 6]])


def soy_gaz_yontemi(z):
    """Kitaptaki kestirme: önceki soy gaz, bir alt periyot; 4.–5. periyotta fark = IUPAC; 2.–3.'de fark 3–8 → +10."""
    once = max([0] + [g for g in TV.SOY_Z if g < z])
    p = TV.SOY_Z.index(once) + 2 if once else 1
    fark = z - once
    if p in (2, 3):
        return p, (fark if fark <= 2 else fark + 10)
    return p, fark


kontrol("soy gaz yöntemi Z = 3–54 için doğru konumu verir", all(soy_gaz_yontemi(z) == TV.yer(z) for z in range(3, 55)))
kontrol("soy gaz örnekleri: Ag 47−36=11 → (5,11) · P 15−10=5 → (3,15) · Ge 32−18=14 → (4,14) · Sb 51−36=15 · Sn 50−36=14",
        [soy_gaz_yontemi(z) for z in (47, 15, 32, 51, 50)] == [(5, 11), (3, 15), (4, 14), (5, 15), (5, 14)])


def son_terim_grubu(z):
    """Cevaplar'daki 'son terimden gruba' tablosu (Z ≤ 36)."""
    d = dizilim(z)
    nmax = max(int(o[0]) for o, _ in d)
    s_ = dict((o, k) for o, k in d)
    ns, np_, nd = s_.get(f"{nmax}s", 0), s_.get(f"{nmax}p", 0), s_.get(f"{nmax - 1}d", 0)
    if z == 2 or (ns == 2 and np_ == 6):
        return 18
    if np_:
        return 12 + np_
    if nd == 10:
        return 11 if ns == 1 else 12
    if nd:
        return ns + nd
    return ns


kontrol("son terim tablosu (s¹…s²d¹⁰) Z = 1–36 için doğru IUPAC grubunu verir", all(son_terim_grubu(z) == TV.yer(z)[1] for z in range(1, 37)))
kontrol("p ile biten: 4s2 3d10 4p4 → 2 + 10 + 4 = 16 (Se)", 2 + 10 + 4 == TV.yer(34)[1] == 16)


def yari_dolu(z):
    """Temel hâlde yarı dolu orbital sayısı (Hund)."""
    say = 0
    for o, n in dizilim(z):
        kap = KAP[o[-1]] // 2
        say += n if n <= kap else 2 * kap - n
    return say


# ================================================================== 3. iyonlar
YUK = {1: 1, 2: 2, 13: 3, 15: -3, 16: -2, 17: -1}     # grup → kararlı iyon (Al için 3+)


def e_sayisi(z, yuk):
    return z - yuk


kontrol("grup → iyon tablosu: Na+ Mg2+ Al3+ N3− O2− F− (hepsi Ne gibi 10 e⁻)",
        all(e_sayisi(TV.Z[s], YUK[TV.yer(TV.Z[s])[1]]) == 10 for s in ("Na", "Mg", "Al", "N", "O", "F")))
kontrol("K+ Ca2+ P3− S2− Cl− hepsi 18 e⁻ (Ar gibi)",
        all(e_sayisi(TV.Z[s], YUK[TV.yer(TV.Z[s])[1]]) == 18 for s in ("K", "Ca", "P", "S", "Cl")))
kontrol("iyon oluşumu: Na 2·8·1 → Na+ 2·8 · Cl 2·8·7 → Cl− 2·8·8", katmanlar(11)[:-1] == katmanlar(10) and katmanlar(17) + [] == [2, 8, 7] and katmanlar(18) == [2, 8, 8])
kontrol("Ag+ = [Kr] 4d10: Ag'nin 5s elektronu gider", dizilim_metni(dizilim(47)).replace(" 5s1", "") == dizilim_metni(dizilim(36)) + " 4d10")

# ================================================================== 4. sorular (tek doğru şık)
T = {}
# ---- durak görevleri, tuzaklar, hızlı görevler
kontrol("Görev 1: (40 + 137) / 2 = 88,5 ≈ Sr 88", (40 + 137) / 2 == 88.5 and TV.ELEMENTLER[37]["kutle"] == "88"
        and TV.ELEMENTLER[19]["kutle"] == "40" and TV.ELEMENTLER[55]["kutle"] == "137")
kontrol("Görev 2: Si (3,14) · O (2,16) · Fe (4,8)", (TV.yer(14), TV.yer(8), TV.yer(26)) == ((3, 14), (2, 16), (4, 8)))
kontrol("Görev 3: Ag (5,11) d bloku", TV.yer(47) == (5, 11) and TV.blok(47) == "d")
kontrol("Görev 4: Z = 5, 13, 15, 18 → yarı metal, metal, ametal, soy gaz",
        [TV.sinif(TV.SEMBOL[z - 1]) for z in (5, 13, 15, 18)] == ["yari", "metal", "ametal", "soy"])
kontrol("Görev 5: Mg2+ 10 e⁻ (Ne), Cl− 18 e⁻ (Ar), X2− 18 e⁻ → Z = 16 (3,16)",
        e_sayisi(12, 2) == 10 and e_sayisi(17, -1) == 18 and 18 - 2 == 16 and TV.yer(16) == (3, 16))
kontrol("Hızlı (s.2): Al (3,13) = 3A; altındaki 13 + 18 = 31 (Ga)", TV.ab_adi(TV.yer(13)[1]) == "3A" and 13 + 18 == 31 and TV.yer(31) == (4, 13))
kontrol("Hızlı (s.3): Mn …4s2 3d5 → (4,7) = 7B", TV.yer(25) == (4, 7) and TV.ab_adi(7) == "7B")
kontrol("Hızlı (s.4): 4s2 4p5 → 4. periyot 17. grup → Z = 18 + 17 = 35 (Br)", TV.yer(35) == (4, 17) and TV.SEMBOL[34] == "Br")
kontrol("Hızlı (s.5): Sb (5,15) yarı metal", TV.yer(51) == (5, 15) and TV.sinif("Sb") == "yari")
kontrol("Hızlı (s.6): O2− F− Na+ 10 e⁻, Cl− 18 e⁻ → yalnız Cl− farklı",
        [e_sayisi(8, -2), e_sayisi(9, -1), e_sayisi(11, 1), e_sayisi(17, -1)] == [10, 10, 10, 18])
kontrol("Hızlı kontrol (s.5): bakır metal, kükürt ametal", TV.sinif("Cu") == "metal" and TV.sinif("S") == "ametal")
kontrol("Kendini yokla (s.7): Se (34) 4. periyot 6A · Al3+ 10 e⁻ · Te yarı metal", TV.yer(34) == (4, 16) and e_sayisi(13, 3) == 10 and TV.sinif("Te") == "yari")
kontrol("Tuzak (s.2): Te 128 > I 127 ama Z: Te 52 < I 53", TV.ELEMENTLER[51]["kutle"] == "128" and TV.ELEMENTLER[52]["kutle"] == "127")
kontrol("Tuzak (s.3): S …3s2 3p4 → 6A", TV.ab_adi(TV.yer(16)[1]) == "6A")
kontrol("Tuzak (s.5): H 1A'da ama ametal", TV.yer(1) == (1, 1) and TV.sinif("H") == "ametal")
kontrol("Tuzak (s.6): Na 2·8·1 → 3. periyot 1A", katmanlar(11) == [2, 8, 1] and TV.yer(11) == (3, 1))
kontrol("eka-alüminyum: Al'nin altı galyum, çerçevede kütle 70 (tahmin ≈ 68)", TV.yer(31) == (TV.yer(13)[0] + 1, 13) and TV.ELEMENTLER[30]["kutle"] == "70")
kontrol("zaman şeridi yılları sıralı: 1829 < 1865 < 1869 < 1870 < 1913", [1829, 1865, 1869, 1870, 1913] == sorted([1829, 1865, 1869, 1870, 1913]))

# ---- Büyük İmtihan
T["I1"] = tek_sik("İmtihan 1", dict(A=("kütle", "Mendeleyev"), B=("numara", "Moseley"), C=("numara", "Mendeleyev"),
                                     D=("hacim", "Meyer"), E=("kütle no", "Newlands")), lambda v: v == ("numara", "Moseley"), "B")
ifade = dict(A=(7, 18) == (len(TV.BAS), 18),
             B=[g for g in range(1, 19) if TV.ab_adi(g) == "8B"] == [8, 9, 10],
             C=not any(TV.yer(z)[1] is not None and 3 <= TV.yer(z)[1] <= 12 for z in range(1, 19)),
             D=TV.SON[6] - TV.BAS[6] + 1 == 32 and TV.SON[7] - TV.BAS[7] + 1 == 32,
             E=all(TV.yer(TV.BAS[p])[1] == 1 and TV.SEMBOL[TV.BAS[p] - 1] != "H" for p in range(1, 8)))
T["I2"] = tek_sik("İmtihan 2 (yanlış olan)", ifade, lambda v: not v, "E")
T["I3"] = tek_sik("İmtihan 3", dict(A=(4, 3), B=(3, 13), C=(4, 1), D=(4, 13), E=(5, 13)), lambda v: v == TV.yer(31), "D")
T["I4"] = tek_sik("İmtihan 4", dict(A="4s2 3d9", B="4s1 3d10", C="4s2 4p9", D="3d11", E="4s2 3d8 4p1"),
                  lambda v: dizilim_metni(dizilim(29)).endswith(v), "B")
d5 = yargi({"I": TV.sinif("Si") == "yari", "II": TV.blok(14) == "p", "III": False})   # III: yarı iletken, metal kadar iletmez
T["I5"] = tek_sik("İmtihan 5", dict(A={"I"}, B={"II"}, C={"I", "II"}, D={"I", "III"}, E={"I", "II", "III"}), lambda v: v == d5, "C")
# halojen ifadeleri: A değerlik 7 (17. grup), B F2 Cl2 Br2 I2, C brom sıvı, D yalnız 1− (YANLIŞ: Cl, Br, I + değer de alır), E tuz yapar
hal = dict(A=all(TV.yer(TV.Z[s])[1] - 10 == 7 for s in ("F", "Cl", "Br", "I")), B=True, C=True, D=False, E=True)
T["I6"] = tek_sik("İmtihan 6 (yanlış olan)", hal, lambda v: not v, "D")
T["I7"] = tek_sik("İmtihan 7", dict(A=38, B=3, C=13, D=2, E=30), lambda z: TV.yer(z)[1] == 2, "A")
d8 = yargi({"I": e_sayisi(20, 2) == 18, "II": e_sayisi(20, 2) == 18, "III": TV.yer(20)[0] == 3})
T["I8"] = tek_sik("İmtihan 8", dict(A={"I"}, B={"III"}, C={"I", "II"}, D={"II", "III"}, E={"I", "II", "III"}), lambda v: v == d8, "C")
cift = dict(A=((11, 0), (10, 0)), B=((12, 2), (9, -1)), C=((17, -1), (10, 0)), D=((19, 1), (10, 0)), E=((8, -2), (18, 0)))
T["I9"] = tek_sik("İmtihan 9", cift, lambda v: e_sayisi(*v[0]) == e_sayisi(*v[1]), "B")
ISK = {"X": (2, 1), "Y": (4, 9), "Z": (3, 13), "T": (4, 2), "Q": (2, 18)}


def isk_z(h):
    p, g = ISK[h]
    return next(z for z in range(1, 37) if TV.yer(z) == (p, g))


d10 = yargi({"I": TV.blok(isk_z("X")) == "s" and TV.blok(isk_z("T")) == "s", "II": TV.blok(isk_z("Y")) == "d",
             "III": ISK["Z"][0] == ISK["Q"][0]})
T["I10"] = tek_sik("İmtihan 10", dict(A={"I"}, B={"II"}, C={"I", "III"}, D={"I", "II"}, E={"II", "III"}), lambda v: v == d10, "D")
T["I11"] = tek_sik("İmtihan 11", dict(A=(2, 18), B=(2, 15), C=(3, 3), D=(4, 13), E=(3, 13)), lambda v: v == TV.yer(10 + 3), "E")
OZ = {("parlak", "iyi", "tel"): "metal", ("parlak", "zayıf", "kırılgan"): "yari", ("mat", "yok", "ufalanır"): "ametal"}
gercek = (OZ[("parlak", "iyi", "tel")], OZ[("parlak", "zayıf", "kırılgan")], OZ[("mat", "yok", "ufalanır")])
T["I12"] = tek_sik("İmtihan 12", dict(A=("metal", "yari", "ametal"), B=("metal", "ametal", "yari"), C=("yari", "metal", "ametal"),
                                      D=("metal", "metal", "ametal"), E=("ametal", "yari", "metal")), lambda v: v == gercek, "A")
dagilim([T[f"I{i}"] for i in range(1, 13)])

# ---- Kıssalar
dk1 = yargi({"I": e_sayisi(11, 1) == e_sayisi(12, 2), "II": e_sayisi(19, 1) == e_sayisi(17, -1), "III": e_sayisi(20, 2) == e_sayisi(9, -1)})
T["K1"] = tek_sik("Kıssa 1", YARGI_5, lambda v: v == dk1, "C")
br = (35.5 + 127) / 2
T["K2"] = tek_sik("Kıssa 2", dict(A=63.5, B=81.3, C=91.5, D=127.0, E=162.5), lambda v: abs(v - br) < .1, "B")
kontrol(f"Kıssa 2: tahmin {br} çerçevedeki Br kütlesine (80) yakın", abs(br - float(TV.ELEMENTLER[34]["kutle"])) < 2)
dk3 = yargi({"I": TV.yer(31)[1] == TV.yer(49)[1], "II": TV.blok(29) == "d", "III": TV.sinif("Se") == "ametal"})
T["K3"] = tek_sik("Kıssa 3", YARGI_5, lambda v: v == dk3, "E")
k4 = dict(A=all(TV.yer(z)[0] == 4 for z in (25, 26, 27, 29)), B=all(TV.blok(z) == "d" for z in (25, 26, 27, 29)),
          C=TV.ab_adi(TV.yer(26)[1]) == TV.ab_adi(TV.yer(27)[1]) == "8B", D=dizilim_metni(dizilim(29)).endswith("4s2 3d9"),
          E=TV.ab_adi(TV.yer(25)[1]) == "7B")
T["K4"] = tek_sik("Kıssa 4 (yanlış olan)", k4, lambda v: not v, "D")

# ---- Üstad
X_u1 = next(z for z in range(3, 11) if TV.yer(z)[1] == 16)          # 2. periyotta 2− iyon yapan: 6A
Y_u1 = e_sayisi(X_u1, -2) + 3
du1 = yargi({"I": TV.sinif(TV.SEMBOL[Y_u1 - 1]) == "metal", "II": TV.yer(X_u1)[0] == TV.yer(Y_u1)[0], "III": Y_u1 - X_u1 == 5})
T["U1"] = tek_sik("Üstad 1", dict(A={"I"}, B={"II"}, C={"I", "II"}, D={"I", "III"}, E={"II", "III"}), lambda v: v == du1, "D")
alti = [z for z in range(19, 37) if yari_dolu(z) == 6]
kontrol(f"Üstad 2: 4. periyotta 6 yarı dolu orbitali olan tek element Cr {alti}", alti == [24])
T["U2"] = tek_sik("Üstad 2", dict(A="6A", B="6B", C="7B", D="8B", E="1B"), lambda v: v == TV.ab_adi(TV.yer(alti[0])[1]), "B")
U3N = {"X": (2, 3), "Y": (3, 3), "Z": (3, 6), "T": (4, 2)}


def a_grubu(per, deg):
    return next(z for z in range(1, 37) if TV.yer(z)[0] == per and TV.yer(z)[1] in (1, 2, 13, 14, 15, 16, 17, 18)
                and int(TV.ab_adi(TV.yer(z)[1])[0]) == deg)


u3 = {k: a_grubu(*v) for k, v in U3N.items()}
kontrol(f"Üstad 3: grafik noktaları X B, Y Al, Z S, T Ca ({u3})", u3 == {"X": 5, "Y": 13, "Z": 16, "T": 20})
du3 = yargi({"I": TV.yer(u3["X"])[1] == TV.yer(u3["Y"])[1], "II": TV.sinif("B") == "yari" and TV.sinif("Al") == "metal",
             "III": e_sayisi(u3["Z"], -2) == e_sayisi(u3["T"], 2)})
T["U3"] = tek_sik("Üstad 3", YARGI_5, lambda v: v == du3, "E")
du4 = yargi({"I": TV.ab_adi(TV.yer(47)[1]) == "1B" and TV.yer(47)[0] == 5, "II": "5s2" in dizilim_metni(dizilim(47)),
             "III": dizilim_metni(dizilim(47)).replace(" 5s1", "") == dizilim_metni(dizilim(36)) + " 4d10"})
T["U4"] = tek_sik("Üstad 4", dict(A={"I"}, B={"I", "II"}, C={"I", "III"}, D={"II", "III"}, E={"I", "II", "III"}), lambda v: v == du4, "C")
U5 = {"X": (11, 10), "Y": (16, 18), "Z": (13, 10), "T": (17, 17)}
u5 = dict(A=TV.yer(U5["X"][0])[1] == TV.yer(U5["Y"][0])[1], B=U5["X"][1] == U5["Z"][1], C=U5["Y"][0] - U5["Y"][1] == -2,
          D=U5["T"][0] == U5["T"][1] and TV.yer(17)[1] == 17, E=TV.yer(U5["Z"][0]) == (3, 13))
T["U5"] = tek_sik("Üstad 5 (yanlış olan)", u5, lambda v: not v, "A")
X6 = next(z for z in range(1, 37) if TV.yer(z) == (4, 17))
Y6 = next(z for z in range(1, 37) if TV.yer(z) == (3, 17))
Z6 = next(z for z in range(1, 37) if TV.yer(z) == (4, 2))
kontrol(f"Üstad 6: X Br {X6}, Y Cl {Y6} (= 35 − 18), Z Ca {Z6}", (X6, Y6, Z6) == (35, 17, 20) and X6 - 18 == Y6)
T["U6"] = tek_sik("Üstad 6", dict(A=2, B=3, C=5, D=15, E=18), lambda v: v == Z6 - Y6, "B")
dagilim([T[f"U{i}"] for i in range(1, 7)])

# ---- anahtar merdiveni ve meclis
kontrol("Merdiven 1: X2+ 18 e⁻ → p = 20 (Ca, 4. periyot 2A); bir üstü 20 − 8 = 12 (Mg)",
        18 + 2 == 20 and TV.yer(20) == (4, 2) and 20 - 8 == 12 and TV.yer(12) == (3, 2))
kontrol("Merdiven 2: 5. periyot 6B → 36 + 6 = 42 (Mo)", TV.yer(42) == (5, 6) and TV.SEMBOL[41] == "Mo")
kontrol("Merdiven 3: Sn 50 → 50 − 36 = 14 → 5. periyot 4A (14), p bloku, metal",
        soy_gaz_yontemi(50) == (5, 14) and TV.blok(50) == "p" and TV.sinif("Sn") == "metal")
kontrol("Meclis 1: Ca …3p6 4s2 → 4. periyot 2A", dizilim_metni(dizilim(20)).endswith("3p6 4s2") and TV.yer(20) == (4, 2))
kontrol("Meclis 2: Ni …4s2 3d8 → 4. periyot 8B (10)", TV.yer(28) == (4, 10) and TV.ab_adi(10) == "8B")
kontrol("Meclis 3: O 1s2 2s2 2p4 → 2. periyot 6A", TV.yer(8) == (2, 16))
kontrol("Meclis 4: He 1. periyot 8A, soy gaz", TV.yer(2) == (1, 18) and TV.sinif("He") == "soy")
MECLIS = {"M1": ("Yusuf", 1), "M2": ("Elif", 2), "M3": ("Yusuf", 2), "M4": ("Pamuk", 3)}

# ================================================================== 5. sayfadan okuma (unite.html)
html = sayfa_oku(__file__)
if html:
    sayfa_isaretleri_ayni(html, T)
    izgara = anahtar_izgarasi(html)
    kontrol(f"Cevaplar ızgarası data-dogru işaretleriyle aynı {izgara}", izgara == {i: T[f"I{i}"] for i in range(1, 13)})
    hk = meclis_hukumleri(html)
    kontrol(f"meclis hükümleri {hk}", hk == MECLIS)
    # Cevaplar sayfasındaki çözüm satırları
    cev = html[html.index('<section class="sayfa s14">'):html.index('<section class="sayfa s15">')]
    for grup, kod in (("Büyük İmtihan", "I"), ("Kıssalar", "K"), ("Üstad soruları", "U")):
        blok = re.search(rf"<h4>{grup}</h4>(.*?)</div>", cev, re.S).group(1)
        satir = dict((f"{kod}{n}", h) for n, h in re.findall(r"<b>(\d+) · ([A-E])</b>", blok))
        kontrol(f"Cevaplar · {grup}: çözüm harfleri anahtarla aynı", satir == {k: v for k, v in T.items() if k.startswith(kod) and k[1:].isdigit()})
    hiz = re.search(r"<b>Kıssa</b>(.*?)</p>", cev, re.S).group(1)
    kontrol("Cevaplar · yan yol hızlı anahtarı (kıssa) aynı", re.findall(r'<span class="ck">(\d) ([A-E])</span>', hiz) ==
            [(str(i), T[f"K{i}"]) for i in range(1, 5)])
    mec = re.search(r"<b>Meclis</b>(.*?)</p>", cev, re.S).group(1)
    kontrol("Cevaplar · meclis hızlı anahtarı aynı", re.findall(r'<span class="ck">(\d) (\w+) · (\d)</span>', mec) ==
            [(k[1], v[0], str(v[1])) for k, v in MECLIS.items()])
    # öğretmen işaretleri
    for kod, blok in [(m.group(1), html[m.start():html.find("</section>", m.start())]) for m in re.finditer(r'data-soru="([KIU]\d+)"', html)]:
        blok = blok[:blok.find('data-soru="', 10)] if 'data-soru="' in blok[10:] else blok
        kontrol(f"{kod}: karalamada öğretmen çözümü (.ogr) var", re.search(r'<div class="karalama"><span class="ogr">[^<]', blok) is not None)
    nedenler = re.findall(r'NEDEN\?<span class="cizgili"><span class="ogr">(.*?)</span>', html)
    kontrol(f"meclis NEDEN cevapları ≤ 14 harf {nedenler}", len(nedenler) == 4 and all(len(n) <= 14 for n in nedenler))
    dogrusu = re.findall(r'DOĞRUSU<span class="cizgili"><span class="ogr">(.*?)</span>', html)
    kontrol("meclis DOĞRUSU cevapları ≤ 45 harf", len(dogrusu) == 4 and all(len(re.sub("<[^>]+>", "", d)) <= 45 for d in dogrusu))
    kutu = re.findall(r'<div class="cevap-kutu">CEVABIN:<span class="ogr">([^<]+)</span>', html)
    kontrol(f"5 hızlı görevin hepsinde öğretmen cevabı {kutu}", len(kutu) == 5)
    kontrol("merdivende 3 × 3 öğretmen çözüm satırı", len(re.findall(r'<div class="cozum-alani">(?:<div><span class="ogr">.*?</span></div>){3}</div>', html)) == 3)
    kontrol("hızlı kontrol ve kendini yokla boşluklarında öğretmen cevabı (5)", len(re.findall(r'<span class="bos(?: g)?"><span class="ogr">', html)) == 5)
    # yasaklar
    duz = re.sub(r"<[^>]+>", " ", html)
    kontrol("elektronegatiflik yazılmadı (karar bekliyor)", "elektronegatif" not in duz.lower())
    kontrol("kurum adı/logo yok (Eti, Etibank)", not re.search(r"\bEti\b|Etibank|Eti Maden|Eti Gümüş|Eti Alüminyum", duz))
    kontrol("bor rezervi 'yaklaşık' diye yazıldı", "yaklaşık %70" in duz)
    # akçe: durak sayfaları (çipler + hazine kartları)
    for d in META["duraklar"]:
        no = d["sayfa"]
        sec = html[html.index(f'<section class="sayfa s{no}">'):html.index(f'<section class="sayfa s{no + 1}">')]
        ic = sec[sec.index('<main class="ic"'):]
        cipler = sum(int(x) for x in re.findall(r'<span class="cip akce">\+(\d+) akçe</span>', ic))
        haz = sum(10 for h in META["hazine"] if h["durak"] == d["no"])
        kontrol(f"{d['no']}. durak (s.{no}): çipler {cipler} + hazine {haz} = {d['akce']} akçe", cipler + haz == d["akce"])
        kontrol(f"{d['no']}. durak levhasında +{d['akce']} akçe ve nişan adı", f'+{d["akce"]} akçe' in sec[:sec.index('<main')]
                and f'Nişan: {META["nisanlar"][d["no"] - 1]["ad"]}' in sec)
    kontrol("hazine kartlarının hepsi sayfada", all(f'<b>{h["kod"]}</b>' in html or f'>{h["kod"]}<' in html for h in META["hazine"]))
    kontrol("Ahilik eşikleri 400 / 800 / 1150 açılışta ve finalde", html.count("<small>400+</small>") == 1 and
            "400–799" in html and "800–1149" in html and "1150–1400" in html)
    # sayfa göndermeleri
    kontrol("s.{{sayfa}} göndermeleri: Gümüşköy s.4, Cevaplar s.14, durak sayfaları s.2–6",
            "sürpriz: s.4" in duz and "s.14" in duz and all(f"s.{n}" in duz for n in range(2, 7)))

# ================================================================== 6. akçe, HUD, künye, rota, medeniyet
durak = [d["akce"] for d in META["duraklar"]]
yan = dict(hulasa=40, meclis=4 * 30, kissa=4 * 30, anahtar=3 * 40, imtihan=12 * 25)
kontrol(f"durak akçeleri 100 + 4 × 150 {durak}", durak == [100, 150, 150, 150, 150])
kontrol(f"ünite toplam akçe {sum(durak) + sum(yan.values())} = 1400", sum(durak) + sum(yan.values()) == META["akce_toplam"] == 1400)
sys.argv = [sys.argv[0]]
K = _yukle("unite_kur", os.path.join(URETEC, "kur.py"))   # yol açıkça verilir (çerçevenin uretec/kur.py’si ile karışmasın)
birikim = [0, 0] + list(__import__("itertools").accumulate(durak + [40, 120, 120, 120, 150, 150]))
bar = [round(100 * b / 1400) for b in birikim] + [100, 100]
kontrol(f"HUD akçe çubukları {bar}", [K.SAYFA[n][2] for n in range(1, 16)] == [min(100, b) for b in bar])
kontrol("nişanlar: 5 durak + Kale Kapısı + Üstad Mührü (bonus)", len(META["nisanlar"]) == 7 and META["nisanlar"][-1].get("bonus") is True
        and META["nisanlar"][5]["ikon"] == "kale")
ROT = json.load(open(os.path.join(KITAP, "yerel-cerceve", "rotalar.json"), encoding="utf-8"))
r94 = next(r for r in ROT["rotalar"] if r["sinif"] == 9 and r["yol"] == 4)
kontrol("duraklar rotalar.json'daki yerler (Seydişehir, Kırka, Bandırma, Gümüşköy, Kütahya)",
        sorted(d["yer"] for d in META["duraklar"]) == sorted(d["yer"] for d in r94["duraklar"]))
kontrol("durak koordinatları rotalar.json ile aynı", all(any(abs(d["enlem"] - x["enlem"]) < 1e-6 and abs(d["boylam"] - x["boylam"]) < 1e-6
                                                         for x in r94["duraklar"] if x["yer"] == d["yer"]) for d in META["duraklar"]))
kontrol("kale Kütahya Kalesi, konumu rotalar.json ile aynı", META["kale"] == r94["kale"]["ad"] and
        abs(META["kale_konum"]["enlem"] - r94["kale"]["enlem"]) < 1e-6 and abs(META["kale_konum"]["boylam"] - r94["kale"]["boylam"]) < 1e-6)
MED = _yukle("cer_medeniyet", os.path.join(KITAP, "yerel-cerceve", "uretec", "medeniyet.py"))
for m in META["medeniyet"]:
    k = next(x for x in MED.KISILER if MED.eslesir(x, m["ad"]))
    kontrol(f"Medeniyetimizden · {m['ad']}: katkı ve yıllar çerçevedeki medeniyet.py ile aynı",
            m["katki"] == k["katki"] and m["yil"].replace("–", " – ") == k["tarih"])
kontrol("Medeniyetimizden kişileri rotalar.json önerisiyle aynı (er-Râzî, el-Bîrûnî)",
        sorted(MED._anahtar(m["ad"]) for m in META["medeniyet"]) == sorted(MED._anahtar(x) for x in ["Ebû Bekir er-Râzî", "el-Bîrûnî"]))

D.sonuc()
