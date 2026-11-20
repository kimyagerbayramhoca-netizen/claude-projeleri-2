#!/usr/bin/env python3
"""Katla örneği · doğrulayıcı. Önce python3 uretec/kur.py, sonra python3 uretec/dogrula.py → "SONUÇ: hepsi doğru".

Denetler: bağ satırlarındaki elektron sayıları, aktarım/ortak çift sayıları ve çizimdeki karşılıkları · tepkimelerin
denkliği, fiziksel hâlleri, şerit hilesi · dikişte bölünen yazının konumu ve ürünün açık sayfada tam okunmaması ·
Şifreli Kapı (PROTON, tek doğru seçenek, ünitedeki data-dogru ile birebir, yanlış harflerin kelime kuramaması) ·
çeldirici röntgeni, robot hatası, heybe cevapları · köşe sineması enerjileri · köşeyi katla dönüşümü ve gaz sorusu ·
PDF (6 sayfa, Type 3 yok), taşma raporu, katlı görünümde dikiş sürekliliği, ortak dosyalara dokunulmadığı.
"""
import itertools
import json
import math
import os
import re
import subprocess
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
ORTAK = os.path.join(KITAP, "yerel-ortak")
for _yol in (ORTAK, os.path.join(KITAP, "gelistirme", "atom-modelleri", "uretec"), os.path.join(KITAP, "gelistirme", "karma-temalar", "uretec"), BURA):
    sys.path.insert(0, _yol)
from dogrula_ortak import D  # noqa: E402
import katla_cizim as KC  # noqa: E402

Z = {"H": 1, "C": 6, "N": 7, "O": 8, "Na": 11, "Mg": 12, "Al": 13, "S": 16, "Cl": 17, "K": 19, "Fe": 26, "Cu": 29, "Ag": 47}
SOY_GAZ = {2: "He", 10: "Ne", 18: "Ar"}


def oku(yol):
    with open(yol, encoding="utf-8") as fp:
        return fp.read()


def duz_html(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s.replace("&nbsp;", " ")).strip()


def bohr(z):
    out, kalan = [], z
    for kap in (2, 8, 8, 2):
        if kalan <= 0:
            break
        out.append(min(kap, kalan))
        kalan -= out[-1]
    return out


def atomlar(formul):
    """'2NaNO3' → katsayı × atom sayıları. Parantez yok (bu sayfadaki formüller için yeterli)."""
    m = re.match(r"(\d*)(.*)", formul)
    k, f_ = int(m.group(1) or 1), m.group(2)
    say = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", f_):
        say[el] = say.get(el, 0) + k * int(n or 1)
    return say


def topla(terimler):
    say = {}
    for k, f_, _ in terimler:
        for el, n in atomlar(f"{k}{f_}").items():
            say[el] = say.get(el, 0) + n
    return say


# ------------------------------------------------------------------ 1. Katla, bağ oluşsun
print("— 1. sayfa · Katla, bağ oluşsun —")
s1, b1 = KC.bag_sayfasi("f1", '<svg class="durak-rozet" viewBox="0 0 100 100"></svg>', KC.kare(0), 1)
for b, kayit in zip(KC.BAG, b1):
    (ss, sk, *_), (gs, gk, *_) = b["sol"], b["sag"]
    D.kontrol(f"{b['kod']}: {ss} dizilimi {sk} = Bohr({Z[ss]})", sk == bohr(Z[ss]))
    D.kontrol(f"{b['kod']}: {gs} dizilimi {gk} = Bohr({Z[gs]})", gk == bohr(Z[gs]))
    v1, v2 = sk[-1], gk[-1]
    if b["tur"] == "iyonik":
        n = b["aktarim"]
        D.kontrol(f"{b['kod']}: metal {v1} e⁻ verir = ametalin oktet eksiği {8 - v2} = {n}", v1 == n == 8 - v2)
        kat, an = Z[ss] - n, Z[gs] + n
        D.kontrol(f"{b['kod']}: {ss}{n}+ {kat} e⁻ ({SOY_GAZ.get(kat)}), {gs}{n}− {an} e⁻ ({SOY_GAZ.get(an)}) soy gaz düzeninde", kat in SOY_GAZ and an in SOY_GAZ)
        D.kontrol(f"{b['kod']}: çizimde {n} aktarım oku, {n} boş yer, ortak çift yok", kayit["oklar"] == n == len(kayit["sag_bos"]) and kayit["haleler"] == 0)
        D.kontrol(f"{b['kod']}: yükler dengede → formül 1:1 ({b['urun']})", atomlar(b["urun"]) == {ss: 1, gs: 1})
    else:
        n = b["ortak"]
        hedef = 2 if ss == "H" else 8
        D.kontrol(f"{b['kod']}: {n} ortak çift → her {ss} {v1 - n + 2 * n} e⁻ (hedef {hedef})", v1 - n + 2 * n == hedef and v2 - n + 2 * n == hedef)
        D.kontrol(f"{b['kod']}: çizimde {n} ortak çift halesi, ok yok", kayit["haleler"] == n and kayit["oklar"] == 0)
        D.kontrol(f"{b['kod']}: ürün {b['urun']} = {ss}{gs} atomları", atomlar(b["urun"]) == {ss: 2})
    D.kontrol(f"{b['kod']}: dış katmanda çizilen elektron sayısı {len(kayit['sol_e'])} ve {len(kayit['sag_e'])} = {v1} ve {v2}", len(kayit["sol_e"]) == v1 and len(kayit["sag_e"]) == v2)
    yakin = [70 - x - KC.E_R for x, _ in kayit["sol_e"]] + [x - 140 - KC.E_R for x, _ in kayit["sag_e"] + kayit["sag_bos"]]
    D.kontrol(f"{b['kod']}: elektron ve boş yerler dikişten ≥ {KC.GUVEN} mm uzakta (en yakın {min(yakin):.2f})", min(yakin) >= KC.GUVEN - 1e-6)
    cx1, cx2 = kayit["cx"]
    r1, r2 = kayit["r"]
    D.kontrol(f"{b['kod']}: atom halkaları dikişi geçmiyor ({70 - (cx1 + r1 + .21):.2f} ve {cx2 - r2 - .21 - 140:.2f} mm)", cx1 + r1 + .21 <= 70 - KC.GUVEN + 1e-6 and cx2 - r2 - .21 >= 140 + KC.GUVEN - 1e-6)
    # denklem ve neden
    sol, kes, sag = b["denklem"]
    D.kontrol(f"{b['kod']}: denklem “{KC.duz(sol + kes + sag)}” denk", topla([(1, x.strip(), "") for x in KC.duz(sol + kes + sag).split("→")[0].split("+")]) == atomlar(b["urun"]))
    for ad, (a, k, c), boy, font in (("denklem", b["denklem"], 4.3, "baloo"), ("neden", b["neden"], 3.35, "nunito")):
        u_k = 70 - KC.genislik(k, boy, font) / 2 - KC.genislik(a, boy, font)
        _, u0, u1 = KC.bolunmus(a, k, c, 0, boy, font=font)
        D.kontrol(f"{b['kod']} {ad}: bölünen harf “{k}” dikişe ortalı ve güvenli harf", abs(u_k - u0) < 1e-9 and k in KC.GUVENLI_HARF)
        D.kontrol(f"{b['kod']} {ad}: satır sayfaya sığıyor (x {u0:.1f}–{u1 + 70:.1f} mm)", u0 >= 6 and u1 + 70 <= 204)
    D.kontrol(f"{b['kod']}: açık sayfada ürün “{b['urun']}” hiçbir parçada tam yazılı değil", b["urun"] not in KC.duz(sol) and b["urun"] not in KC.duz(sag))
    a, k, c = b["neden"]
    D.kontrol(f"{b['kod']}: bağ türü “{b['tur_kelime']}” dikişte bölünüyor", b["tur_kelime"] not in KC.duz(a) and b["tur_kelime"] not in KC.duz(c) and b["tur_kelime"] in KC.duz(a + k + c))

# ------------------------------------------------------------------ 3. Katla, tepkime olsun
print("— 3. sayfa · Katla, tepkime olsun —")
COZUNUR = {"AgNO3": True, "NaCl": True, "AgCl": False, "NaNO3": True, "HCl": True, "NaOH": True, "CuSO4": True, "FeSO4": True}
AKTIFLIK = ["K", "Na", "Ca", "Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "H", "Cu", "Ag", "Au"]
s3, b3 = KC.tepkime_sayfasi("f2", '<svg class="durak-rozet" viewBox="0 0 100 100"></svg>', KC.kare(1), 2)


def denklem_coz(satirlar):
    metin = " ".join(KC.duz(a + k + c) for a, k, c in satirlar)
    sol, sag = metin.split("→")

    def terimler(t):
        out = []
        for p in re.findall(r"(\d*)([A-Za-z0-9]+)\((suda|k|s|g)\)", t):
            out.append((int(p[0] or 1), p[1], p[2]))
        return out
    return terimler(sol), terimler(sag)


for t, kayit in zip(KC.TEPKIME, b3):
    g, u = denklem_coz(t["satirlar"])
    D.kontrol(f"{t['kod']}: yazılı denklem tablo ile aynı ({len(g)} giren, {len(u)} ürün)", g == t["girenler"] and u == t["urunler"])
    D.kontrol(f"{t['kod']}: atomlar denk {topla(g)}", topla(g) == topla(u))
    for k, f_, hal in g + u:
        if f_ in COZUNUR:
            D.kontrol(f"{t['kod']}: {f_}({hal}) hâli çözünürlükle uyumlu", (hal == "suda") == COZUNUR[f_])
    for j, (a, k, c) in enumerate(t["satirlar"]):
        _, u0, u1 = KC.bolunmus(a, k, c, 0, 3.7)
        urun = u[j]
        etiket = f"{urun[1]}({urun[2]})"
        D.kontrol(f"{t['kod']} satır {j + 1}: ürün {etiket} dikişte bölünüyor, harf “{k}” güvenli", etiket not in KC.duz(a) and etiket not in KC.duz(c) and etiket in KC.duz(a + k + c).replace(" ", "") and k in KC.GUVENLI_HARF)
        D.kontrol(f"{t['kod']} satır {j + 1}: sayfaya sığıyor (x {u0:.1f}–{u1 + 70:.1f} mm)", u0 >= 6 and u1 + 70 <= 204)
    a, k, c = t["neden"]
    _, u0, u1 = KC.bolunmus(a, k, c, 0, 3.35, font="nunito")
    D.kontrol(f"{t['kod']}: neden satırı sığıyor ve “{t['tur_kelime']}” bölünüyor", u0 >= 6 and u1 + 70 <= 204 and t["tur_kelime"] not in KC.duz(a) and t["tur_kelime"] not in KC.duz(c) and k in KC.GUVENLI_HARF)
    sol, orta, sag = t["serit"]
    katli = KC.duz(sol + sag)
    D.kontrol(f"{t['kod']}: şerit katlanınca “{katli}” = ana ürün {t['ana_urun']} atomları", katli == t["serit_katli"] and atomlar(katli.replace("=", "")) == atomlar(t["ana_urun"]))
    acik = KC.duz(sol + "".join(orta) + sag).replace("=", "")
    D.kontrol(f"{t['kod']}: şerit açıkken girenleri yazar (“{KC.duz(sol + ' '.join(orta) + ' ' + sag)}”)", topla([(1, x, "") for x in acik.split("+")]) == topla([(1, f_, "") for _, f_, _ in g]))
    (sx0, sx1), (gx0, gx1) = kayit["serit_x"]
    ox = kayit["orta_x"]
    D.kontrol(f"{t['kod']}: şerit harfleri dikişten ≥ {KC.SERIT_PAY} mm (sol {70 - sx1:.2f}, sağ {gx0 - 140:.2f}, orta {min(min(a_ - 70, 140 - b_) for a_, b_ in ox):.2f})",
              70 - sx1 >= KC.SERIT_PAY - 1e-6 and gx0 - 140 >= KC.SERIT_PAY - 1e-6 and all(a_ >= 70 + KC.SERIT_PAY - 1e-6 and b_ <= 140 - KC.SERIT_PAY + 1e-6 for a_, b_ in ox))
t1, t2, t3, t4 = KC.TEPKIME
D.kontrol("T1: AgCl çöker (beyaz), Na⁺ ve NO₃⁻ seyirci", not COZUNUR["AgCl"] and "beyaz" in t1["neden"][2])
D.kontrol("T2: bromtimol mavisi asitte sarı, bazda mavi, nötrde yeşil", "sarı" in t2["kap"][0][1] and "mavi" in t2["kap"][1][1] and "yeşil" in t2["neden"][2])
D.kontrol("T3: Fe, Cu’dan aktif (aktiflik sırası) → Fe Cu²⁺’yi indirger", AKTIFLIK.index("Fe") < AKTIFLIK.index("Cu"))
D.kontrol("T3: Fe → Fe²⁺ + 2e⁻ ve Cu²⁺ + 2e⁻ → Cu: 2 e⁻ aktarılır", "2 e^{−}" in t3["neden"][0])
D.kontrol("T4: 2Mg + O₂ → 2MgO; Mg²⁺ ve O²⁻ yükleri dengede", topla(t4["girenler"]) == {"Mg": 2, "O": 2} == topla(t4["urunler"]))

# ------------------------------------------------------------------ dikiş kuralları (iki kat sayfası)
ince = []
for s in (s1, s3):
    for frag, yazi_mi in s.dikis_parcalari:
        if yazi_mi:
            continue
        for oge in re.findall(r"<(?:path|ellipse|circle|rect)\b[^>]*>", frag):
            k = re.search(r'stroke-width="([\d.]+)"', oge)
            if not k or float(k.group(1)) >= .6:
                continue
            c = re.search(r'<circle cx="([\d.]+)"[^>]* r="([\d.]+)"', oge)
            if not (c and abs(float(c.group(1)) - 70) >= float(c.group(2)) + KC.GUVEN):
                ince.append(oge[:60])
D.kontrol(f"dikişi geçen çizgiler ≥ 0,6 mm; ince çizgili ögeler (çökelek taneleri) dikişten uzak ({len(ince)} sorun)", not ince)
D.kontrol("kat sayfalarında kat çizgisi boyunca çizgi yok (yalnız uçlarda A/B işaretleri)",
          not re.search(r'M(70|140)(\.0)? [\d.]+ V', s1.cikti()) and not re.search(r'M(70|140)(\.0)? [\d.]+ V', s3.cikti()))

# ------------------------------------------------------------------ 2. Karma sayfa · Şifreli Kapı
print("— 2. sayfa · karma sayfa —")
UNITE = {"9/01": "9-sinif-yerel/01-gunluk-hayatta-kimya", "9/03": "9-sinif-yerel/03-atom-ve-yapisi", "9/04": "9-sinif-yerel/04-periyodik-tablo", "9/05": "9-sinif-yerel/05-periyodik-ozellikler"}
s9 = oku(os.path.join(BURA, "sablon9.html"))


def unite_sorusu(kaynak):
    birim, kod = kaynak.split()
    html = oku(os.path.join(KITAP, UNITE[birim], "uretec", "sablon.html"))
    blok = html.split(f'data-soru="{kod}"', 1)[1].split('data-soru="', 1)[0]
    soru = duz_html(re.search(r'<p class="soru">(.*?)</p>', blok, re.S).group(1))
    sik = re.findall(r'<div( data-dogru)?><b>(\w)</b><span>(.*?)</span>', blok, re.S)
    return soru, [duz_html(x[2]) for x in sik], [i for i, x in enumerate(sik) if x[0]]


def norm(s):
    return s.replace("α", "alfa").replace("’", "'").strip().rstrip(".")


kod_harf = []
for kart in re.findall(r'<div class="kart sk" data-sk="(\d)" data-kaynak="([^"]+)">(.*?)</ol>', s9, re.S):
    n, kaynak, ic = kart
    soru = duz_html(re.search(r'<p class="soru">(.*?)</p>', ic, re.S).group(1))
    sik = re.findall(r'<li( data-dogru)?><b>(.)</b>(.*?)</li>', ic, re.S)
    dogru = [i for i, x in enumerate(sik) if x[0]]
    harfler = [x[1] for x in sik]
    u_soru, u_sik, u_dogru = unite_sorusu(kaynak)
    D.kontrol(f"Kapı {n} ({kaynak}): soru ünitedekiyle aynı", norm(soru) == norm(u_soru))
    D.kontrol(f"Kapı {n}: 5 seçenek ünitedekilerle aynı sırada", [norm(duz_html(x[2])) for x in sik] == [norm(x) for x in u_sik])
    D.kontrol(f"Kapı {n}: tek doğru seçenek ve ünitedeki data-dogru ile aynı ({'ABCDE'[u_dogru[0]]})", len(dogru) == 1 and dogru == u_dogru)
    D.kontrol(f"Kapı {n}: 5 farklı kod harfi {''.join(harfler)}", len(set(harfler)) == 5)
    kod_harf.append((harfler, harfler[dogru[0]]))
sifre = "".join(h for _, h in kod_harf)
D.kontrol(f"Şifreli Kapı: doğru harfler “{sifre}” = PROTON", sifre == "PROTON" and len(kod_harf) == 6)
SESLI = set("AEIİOÖUÜ")
IZINLI_BAS = {"PR", "TR", "KR", "BR", "GR", "DR", "FR", "PL", "KL", "BL", "GL", "FL", "SL", "ST", "SP", "SK"}
okunur = []
for dizi in itertools.product(*[h for h, _ in kod_harf]):
    w = "".join(dizi)
    if w[:2] not in IZINLI_BAS and w[1] not in SESLI and w[0] not in SESLI:
        continue
    if re.search(r"[^AEIİOÖUÜ]{3}", w) or not set(w) & SESLI:
        continue
    okunur.append(w)
D.kontrol(f"Şifreli Kapı: 5⁶ = {5 ** 6} dizilimden okunabilen yalnız PRO?O? kalıbı ({len(okunur)} dizi)", all(w.startswith("PRO") and w[4] == "O" for w in okunur) and len(okunur) == 25)
print("    okunabilen diziler (hiçbiri PROTON dışında Türkçe kelime değil):", " ".join(okunur))
D.kontrol("Şifreli Kapı: L 4. konumda, G 6. konumda yok (PROLOG kurulamaz)", "L" not in kod_harf[3][0] and "G" not in kod_harf[5][0])

# çeldirici röntgeni
A_, Z_, q = 27, 13, 3
dogru3 = (Z_, A_ - Z_, Z_ - q)
tanilar = {"A": (Z_, A_ - Z_, Z_), "B": dogru3, "C": (Z_, A_, Z_ - q), "D": (A_ - Z_, Z_, Z_ - q), "E": (Z_, A_ - Z_, Z_ + q)}
rn = re.findall(r'<div class="([yd])"( data-dogru)?><b>(\w)</b><span class="say">([\d, ]+)</span>', s9)
D.kontrol(f"Röntgen: ²⁷₁₃Al³⁺ → p, n, e = {dogru3}", dogru3 == (13, 14, 10))
for cls, dd, harf, say in rn:
    deger = tuple(int(x) for x in say.split(","))
    D.kontrol(f"Röntgen {harf}: {say} tanıdaki hatayla üretiliyor", tanilar[harf] == deger and (cls == "d") == bool(dd) == (deger == dogru3))
_, u_sik, u_dogru = unite_sorusu("9/03 I4")
D.kontrol("Röntgen: seçenekler ve doğru (B) ünitedeki I4 ile aynı", [x[3] for x in rn] == u_sik and u_dogru == [1])
D.kontrol("Röntgen: “Sıra sende” ²³₁₁Na⁺ → 11, 12, 10 (açık uçlu; öğretmen notu)", (11, 23 - 11, 11 - 1) == (11, 12, 10))

# robot
cumle = [duz_html(x) for x in re.findall(r"<li>(.*?)</li>", s9.split('class="bot-cevap"', 1)[1].split("</ol>", 1)[0], re.S)]
iddia = [Z["Na"] == 11 and bohr(11)[-1] == 1 and "1 elektronu" in cumle[0],
         Z["Cl"] + 1 == 18 and "18 elektronu" in cumle[1],
         (Z["Na"] - 1 == 10) and ("argon" not in cumle[2] or SOY_GAZ[Z["Na"] - 1] == "Ar"),
         "iyonik bağ" in cumle[3]]
D.kontrol(f"Robot: 4 cümle, tek hata 3. cümlede (Na⁺ 10 e⁻ → {SOY_GAZ[10]}, argon değil; argon {SOY_GAZ[18]} = Cl⁻)", len(cumle) == 4 and iddia == [True, True, False, True])

# heybe
YARICAP = {"Be": 96, "Mg": 141, "Al": 121, "K": 203}      # kovalent yarıçap (pm)
D.kontrol("Heybe 1 (Yol 5): en büyük yarıçap K", max(YARICAP, key=YARICAP.get) == "K")
_, u_sik, u_dogru = unite_sorusu("9/05 I1")
D.kontrol("Heybe 1: ünitedeki doğru sıralama K ile başlıyor", u_sik[u_dogru[0]].startswith("K"))
D.kontrol("Heybe 2 (Yol 3): n = 4 → 2n² = 32", 2 * 4 ** 2 == 32)
_, u_sik, u_dogru = unite_sorusu("9/01 I6")
D.kontrol("Heybe 3 (Yol 1): ünitede doğru = zehirli klor gazı", "klor gazı" in u_sik[u_dogru[0]])
D.kontrol("Heybe: ters cevaplar K · 32 · zehirli klor gazı", "Cevaplar: K · 32 · zehirli klor gazı" in s9)
D.kontrol("Heybe etiketleri 1/3/5 yol önce = Yol 5/3/1 (karma sayfa Yol 6’nın arkası)", all(f"{n} yol önce · Yol {6 - n}" in s9 for n in (1, 3, 5)))

# ------------------------------------------------------------------ 4. Köşe sineması
print("— 4. sayfa · köşe sineması —")
s10 = oku(os.path.join(BURA, "sablon10.html"))
E = KC.ENERJI
lam = lambda a, b: 1239.84 / abs(E[a] - E[b])  # noqa: E731
D.kontrol(f"E1, E2, E3 = {E[1]:.1f}, {E[2]:.1f}, {E[3]:.2f} eV (sayfada −13,6 · −3,4 · −1,51)", "−13,6" in s10 and "−3,4" in s10 and "−1,51" in s10 and round(E[3], 2) == -1.51)
for a, b, de, nm in ((1, 3, "12,09", 103), (3, 2, "1,89", 656), (2, 1, "10,2", 122)):
    D.kontrol(f"{a}→{b}: ΔE = {abs(E[a] - E[b]):.2f} eV, λ = {lam(a, b):.1f} nm (sayfada {de} eV · {nm} nm)", f"{abs(E[a] - E[b]):.2f}".rstrip("0").replace(".", ",") == de and round(lam(a, b)) == nm and f"{nm} nm" in s10)
oran = (KC._P[2][1] - KC._P[1][1]) / (KC._P[3][1] - KC._P[1][1])
D.kontrol(f"basamaklar enerjiyle orantılı ({oran:.3f} ≈ {(E[2] - E[1]) / (E[3] - E[1]):.3f})", abs(oran - (E[2] - E[1]) / (E[3] - E[1])) < .005)
kareler = [KC.kare(i) for i in range(KC.KARE_SAYISI)]
D.kontrol("24 kare; kırmızı foton yalnız inişte (kare 18–22), mor ötesi geliş 2–4 ve gidiş 23–24",
          len(kareler) == 24 and [i + 1 for i, k in enumerate(kareler) if "kk-foton-656" in k] == [18, 19, 20, 21, 22]
          and [i + 1 for i, k in enumerate(kareler) if "kk-foton-uv" in k] == [1, 2, 3, 4, 23, 24])
D.kontrol("ters cevap: n = 3 → 1 foton 12,09 eV (103 nm)", "Cevap: 12,09 eV (103 nm)" in s10 and round(abs(E[3] - E[1]), 2) == 12.09)

# ------------------------------------------------------------------ 5–6. Köşeyi katla
print("— 5–6. sayfa · köşeyi katla —")
gaz = "Sabit basınçta gece −13 °C’de 2,6 L olan hava, öğlen 27 °C’de kaç L olur?"
D.kontrol("hızlı görev metni 10/04 Gazlar’daki doğrulanmış soruyla aynı", gaz in oku(os.path.join(KITAP, "10-sinif-yerel", "04-gazlar", "uretec", "sablon.html")) and gaz in s10)
T1, T2 = -13 + 273, 27 + 273
V2 = 2.6 * T2 / T1
D.kontrol(f"V₂ = 2,6 · {T2}/{T1} = {V2:.3f} L → köşedeki cevap “{KC.duz(KC.KOSE_CEVAP[1])}”, “{KC.KOSE_CEVAP[2]}”", abs(V2 - 3) < 1e-9 and KC.duz(KC.KOSE_CEVAP[1]) == "V2 = 3 L" and KC.KOSE_CEVAP[2] == f"{T1} K → {T2} K")
W, H, a = 210.0, 297.0, KC.KOSE_A


def katlaninca(xb, yb):
    """Arka yüz noktası (arka yüzün kendi önünden bakışla) → ön yüzde köşe katlanınca görüldüğü yer."""
    xf = W - xb                          # 1. yansıma: sayfayı çevirmek
    X, Y = W + H - a - yb, H - a + (W - xf)  # 2. yansıma: kat çizgisi x + y = W + H − a
    return X, Y


D.kontrol("köşe: dört özel nokta doğru yere gidiyor", katlaninca(0, H) == (W - a, H - a) and katlaninca(a, H) == (W - a, H) and katlaninca(0, H - a) == (W, H - a))
hata = 0.0
for p, q in ((5, 5), (20, 10), (30, 25), (8, 40), (50, 6)):
    lx, ly = q, a - p                    # SVG: translate(0 a) rotate(-90) → (p, q) ↦ (q, a − p)
    X, Y = katlaninca(lx, H - a + ly)
    hata = max(hata, abs(X - (W - a + p)), abs(Y - (H - a + q)))
D.kontrol(f"köşe: arka yüzde 90° sola döndürülen cevap katlanınca düz ve yerinde (en büyük sapma {hata:.1e} mm)", hata < 1e-9)
D.kontrol("köşe: iki yansımanın bileşkesi 90° dönme (determinant +1)", (lambda m: m[0][0] * m[1][1] - m[0][1] * m[1][0])([[0, -1], [1, 0]]) == 1)

# ------------------------------------------------------------------ çıktılar
print("— çıktılar —")
pdf = os.path.join(KLASOR, "katla-ornek.pdf")
bilgi = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
D.kontrol("katla-ornek.pdf 6 sayfa", re.search(r"Pages:\s+6\b", bilgi) is not None)
fontlar = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
D.kontrol(f"PDF’te Type 3 yazı tipi yok, hepsi gömülü ({len(fontlar)} yazı tipi)", fontlar and not any("Type 3" in l for l in fontlar) and all(" yes " in l for l in fontlar))
rapor = json.load(open(os.path.join(KLASOR, "kur-raporu.json"), encoding="utf-8"))
D.kontrol("render.js taşma denetimi temiz (alan dışı / kutu taşması yok)", all(not v for v in rapor["tasma"].values()) and all(v == 0 for v in rapor["kod"].values()))
oniz = os.path.join(KLASOR, "onizleme")
beklenen = [f"s0{n}.png" for n in range(1, 7)] + ["acik-katli-s1.png", "acik-katli-s2.png", "katlama-s1.gif", "katlama-s2.gif", "kose-katli.png", "kose-cizgi-filmi.gif", "kose-cizgi-filmi-serit.png"]
D.kontrol("önizlemeler eksiksiz", all(os.path.exists(os.path.join(oniz, f_)) for f_ in beklenen))
import onizle  # noqa: E402
for no, sayfa in ((1, 1), (2, 3)):
    img = onizle.png(pdf, sayfa, 1590, 2249)
    (dk, ref), (kayik, _) = onizle.dikis_olcusu(img), onizle.dikis_olcusu(img, 8)
    D.kontrol(f"katlı görünüm s{no}: dikiş farkı {dk:.2f} ≤ 1,5 × komşu sütun farkı {ref:.2f}; 1,5 mm kaymış katta {kayik:.2f}", dk <= 1.5 * ref and kayik > 3 * dk)
# yalnız bu klasör değişti mi?
degisen = subprocess.run(["git", "status", "--porcelain", "--", ".."], capture_output=True, text=True, cwd=KITAP).stdout.splitlines()
disari = [l for l in degisen if not l.startswith("??") and "gelistirme/katla/" not in l and "gelistirme/uc-boyut/" not in l]
D.kontrol(f"izlenen hiçbir dosya değişmedi: ortak, üniteler, yerel-cerceve, atom-modelleri, karma-temalar ({len(disari)} dış değişiklik)", not disari)
D.sonuc()
