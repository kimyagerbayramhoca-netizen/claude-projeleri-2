#!/usr/bin/env python3
"""Kimyasal Güvenlik (yerel · Batı Karadeniz Maden Yolu) — cevapların ve sayfadaki işaretlerin doğrulaması.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Kimya: tepkime denkliği (NaOCl + 2HCl), klorun havaya göre yoğunluğu, buharın hacim katı, metan aralığı.
  2. Piktogram ↔ anlam tutarlılığı: guvenlik_veri.GHS tek kaynak; sayfadaki GHS kartları, piktogram dizileri, işaret aileleri.
  3. Her çoktan seçmeli soru (İmtihan 12, Kıssa 4, Üstad 6) veri tablolarından YENİDEN çözülür; tek doğru şık (tek_sik).
  4. Sayfadan okunanlar: data-dogru işaretleri, şık metinleri, meclis hükümleri, Cevaplar ızgarası ve satırları.
  5. Akçe muhasebesi (sayfa sayfa çip + hazine, toplam 1400, HUD çubuğu), meta.json tutarlılığı, öğretmen metni uzunlukları,
     kalın yazıda fontta olmayan sembol, hassasiyet (felaket/kayıp dili yok; Amasra maden bağlamında geçmez).
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
from dogrula_ortak import (D, mk, formul, kontrol, tek_sik, yargi, dagilim, sayfa_isaretleri_ayni,  # noqa: E402
                           meclis_hukumleri, anahtar_izgarasi, sayfa_oku, _bloklar)
import guvenlik_veri as V  # noqa: E402

Y5 = {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}      # I6
Y5b = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}     # I12, U5'te farklı sıra aşağıda
Y_K = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}    # K1, K4

# ================================================================== 1. KİMYA
def denk(sol, sag):
    def say(taraf):
        t = {}
        for kat, f_ in taraf:
            for el, n in formul(f_).items():
                t[el] = t.get(el, 0) + kat * n
        return t
    return say(sol) == say(sag)


kontrol("NaOCl + 2HCl → NaCl + Cl2 + H2O denk", denk([(1, "NaOCl"), (2, "HCl")], [(1, "NaCl"), (1, "Cl2"), (1, "H2O")]))
kontrol("NaOCl + HCl (katsayısız) denk DEĞİL (2 doğru katsayı)", not denk([(1, "NaOCl"), (1, "HCl")], [(1, "NaCl"), (1, "Cl2"), (1, "H2O")]))
kontrol(f"Cl2 = {mk('Cl2')} g/mol > hava ≈ 29 → havadan yoğun, yerde birikir (×{mk('Cl2') / 29:.2f})", mk("Cl2") == 71 and mk("Cl2") > 29)
v_buhar = (1 / mk("H2O")) * 0.082 * 373 * 1000          # 1 g su, 100 °C, 1 atm → mL
kontrol(f"1 g su buharı ≈ {v_buhar:.0f} mL ≈ {V.SU_BUHAR_KAT} × 1 mL (yaklaşık)", abs(v_buhar - V.SU_BUHAR_KAT) / V.SU_BUHAR_KAT < .02)
kontrol("metan tutuşma aralığı ≈ %5–15", V.METAN_ARALIK == (5, 15))

# ================================================================== 2. PİKTOGRAM ↔ ANLAM (tek kaynak)
kodlar = [k for k, *_ in V.GHS]
kontrol("GHS: dokuz piktogram, GHS01…GHS09, adlar benzersiz", kodlar == [f"GHS0{i}" for i in range(1, 10)] and len(set(V.GHS_AD.values())) == 9)
BEKLENEN_AD = {"GHS01": "Patlayıcı", "GHS02": "Yanıcı", "GHS03": "Yakıcı (oksitleyici)", "GHS04": "Basınçlı gaz",
               "GHS05": "Aşındırıcı (korozif)", "GHS06": "Zehirli (toksik)", "GHS07": "Tahriş edici, zararlı",
               "GHS08": "Ciddi sağlık tehlikesi", "GHS09": "Çevreye zararlı"}
kontrol("GHS adları resmî anlamlarla aynı (patlayıcı, yanıcı, oksitleyici, basınçlı gaz, aşındırıcı, akut toksik, tahriş, sağlık, çevre)",
        V.GHS_AD == BEKLENEN_AD)
SIMGE_BEK = {"GHS01": "bomba", "GHS02": "alev", "GHS03": "çember", "GHS04": "tüp", "GHS05": "aşınma", "GHS06": "kurukafa",
             "GHS07": "ünlem", "GHS08": "sağlık", "GHS09": "balık"}
kontrol("GHS simge adları çizimle aynı", all(SIMGE_BEK[k] in V.GHS_SIMGE[k] for k in kodlar))
# gerçek etiket örnekleri (AB CLP uyumlu) ve sayfadaki iddialar
kontrol("metanol: alev + kurukafa + sağlık tehlikesi", V.MADDE_PIKTO["metanol"] == {"GHS02", "GHS06", "GHS08"})
kontrol("oksijen tüpü: gaz tüpü + çember üstünde alev", V.MADDE_PIKTO["oksijen tüpü"] == {"GHS03", "GHS04"})
kontrol("aseton ve etil alkol: alev + ünlem", V.MADDE_PIKTO["aseton"] == V.MADDE_PIKTO["etil alkol"] == {"GHS02", "GHS07"})
kontrol("sud kostik (lavabo açıcı): aşınma", V.MADDE_PIKTO["sud kostik"] == {"GHS05"})
kontrol("bakır(II) sülfat: ünlem + çevre", V.MADDE_PIKTO["bakır(II) sülfat"] == {"GHS07", "GHS09"})
kontrol("işaret aileleri: zorunluluk mavi daire, uyarı sarı üçgen, yasak kırmızı çizgili daire, acil yeşil kare",
        [V.ISARET_AILE[a][1] for a in ("zor", "uya", "yas", "acil")] == ["mavi daire", "sarı üçgen", "kırmızı çizgili daire", "yeşil kare"])
kontrol("ızgaradaki her işaretin kısa adı var", all(k in V.ISARET_KISA and k in V.ISARET for k in V.ISARET_IZGARA))

# ================================================================== 3. SORULAR (veriden yeniden çözülür)
T = {}
# --- İmtihan
T["I1"] = tek_sik("İmtihan 1 (GHS03)", {"A": "Yanıcı", "B": "Yakıcı (oksitleyici)", "C": "Patlayıcı", "D": "Basınçlı gaz", "E": "Tahriş edici"},
                  lambda v: v == V.GHS_AD["GHS03"], "B")
KURAL = {"A": False, "B": False, "C": False, "D": True, "E": False}    # stoğa dökme / kırık cam çöpe / uçucu açık / tüpü yöneltmeme / koklama
T["I2"] = tek_sik("İmtihan 2 (kural)", KURAL, lambda v: v, "D")
T["I3"] = tek_sik("İmtihan 3 (menisküs)", {"A": 34, "B": 35, "C": 36, "D": 37, "E": 38}, lambda v: v == V.MEZUR_OKUMA, "C")
is_ = {ad: is__ for _k, ad, is__ in V.EKIPMAN}
esle = {"I": is_["Kroze"], "II": is_["Soğutucu"], "III": is_["Piset"]}
harf = {"a": "buharı yoğuşturur", "b": "katıyı çok ısıtır", "c": "saf suyla yıkar"}
dogru_esle = {r: [h for h, t in harf.items() if t == esle[r]][0] for r in esle}
I4S = {"A": "I-b II-a III-c", "B": "I-a II-b III-c", "C": "I-c II-a III-b", "D": "I-b II-c III-a", "E": "I-a II-c III-b"}
T["I4"] = tek_sik("İmtihan 4 (eşleştirme)", I4S, lambda v: v == " ".join(f"{r}-{dogru_esle[r]}" for r in ("I", "II", "III")), "A")
isit = {ad for _k, ad, _i in V.ISITMA}
T["I5"] = tek_sik("İmtihan 5 (beher alevin üstünde)", {"A": "Saat camı", "B": "Sacayağı + tel kafes", "C": "Kroze", "D": "Havan", "E": "Piset"},
                  lambda v: v in isit and "tel kafes" in v, "B")
a6 = yargi({"I": "GHS05" == "GHS05", "II": True, "III": "GHS05" == "GHS02"})
T["I6"] = tek_sik("İmtihan 6 (aşınma piktogramı)", Y5, lambda v: v == a6, "C")
SIN = {"A": {"O"}, "B": {"A"}, "C": {"Z"}, "D": {"A"}, "E": {"Y"}}     # yakıcı tuz, asit, zehirli tuz, baz, başka yanıcı sıvı
T["I7"] = tek_sik("İmtihan 7 (aseton rafı, özel önlemsiz)", SIN, lambda v: V.birlikte({"Y"}, v), "E")
KUTU = {"A": "kimyasal", "B": "pil", "C": "cam", "D": "ambalaj", "E": "tibbi"}
kontrol("enjektör tıbbi atık kutusunda", V.ATIK_KISA["tibbi"][2] == "enjektör" and V.ATIK_KUTU["enjektör, kanlı pamuk"].startswith("Tıbbi"))
T["I8"] = tek_sik("İmtihan 8 (tıbbi atık)", KUTU, lambda v: v == "tibbi", "E")
kontrol("kaza tablosu: göz için 15–20 dakika bol akan su", "15–20 dakika" in V.KAZA[0][1] and "ovma" in V.KAZA[0][1])
T["I9"] = tek_sik("İmtihan 9 (göze sıçrama)", {"A": "15–20 dk su", "B": "ovmak", "C": "baz", "D": "beklemek", "E": "araştırmak"},
                  lambda v: v == "15–20 dk su", "A")
I10_ISARET = ["elektrik", "gozluk", "sicak", "ilkyardim"]
a10 = {["I", "II", "III", "IV"][i] for i, k in enumerate(I10_ISARET) if V.ISARET[k][0] == "uya"}
T["I10"] = tek_sik("İmtihan 10 (uyarı işaretleri)", {"A": {"I", "II"}, "B": {"I", "III"}, "C": {"II", "IV"}, "D": {"III", "IV"}, "E": {"I", "II", "III"}},
                   lambda v: v == a10, "B")
I11 = {"A": ("GHS06", "GHS06"), "B": ("GHS02", "GHS02"), "C": ("GHS04", "GHS04"), "D": ("GHS07", "GHS01"), "E": ("GHS09", "GHS09")}
T["I11"] = tek_sik("İmtihan 11 (yanlış eşleştirme)", I11, lambda v: v[0] != v[1], "D")
a12 = yargi({"I": denk([(1, "NaOCl"), (2, "HCl")], [(1, "NaCl"), (1, "Cl2"), (1, "H2O")]), "II": mk("Cl2") < 29, "III": True})
T["I12"] = tek_sik("İmtihan 12 (klor)", Y5b, lambda v: v == a12, "D")
ANAHTAR = {i: T[f"I{i}"] for i in range(1, 13)}
dagilim([ANAHTAR[i] for i in range(1, 13)])
DURAK_ET = {1: 3, 2: 1, 3: 5, 4: 5, 5: 2, 6: 3, 7: 4, 8: 4, 9: 2, 10: 1, 11: 3, 12: 4}
kontrol(f"her durak İmtihan'da en az 2 soruyla temsil ediliyor {sorted(DURAK_ET.values())}",
        all(list(DURAK_ET.values()).count(d) >= 2 for d in range(1, 6)))

# --- Kıssalar
T["K1"] = tek_sik("Kıssa 1 (çözücü atölyesi)", Y_K, lambda v: v == yargi({"I": True, "II": True, "III": True}), "E")
k2 = ("Pipet", "Erlenmayer", "Büret")
kontrol("K2: pipet hassas aktarır; balon joje tek hacim hazırlar; erlen çalkalamada sıçratmaz; büret musluklu",
        "Pipet + puar" in V.HASSAS and "Büret" in V.HASSAS and dict((ad, is__) for _k, ad, _i, _d, is__ in V.CAM)["Erlenmayer"].startswith("çalkala"))
T["K2"] = tek_sik("Kıssa 2 (su laboratuvarı)", {"A": ("Mezür", "Beherglas", "Pipet"), "B": ("Balon joje", "Erlenmayer", "Büret"),
                                                "C": ("Büret", "Balon joje", "Pipet"), "D": k2, "E": ("Pipet", "Beherglas", "Mezür")},
                  lambda v: v == k2, "D")
G = V.KAZA_GRAFIK
azalma = {ad: (a - b) / a for ad, (a, b) in G.items()}
top1, top2 = sum(a for a, _ in G.values()), sum(b for _, b in G.values())
k3 = {"A": max(azalma, key=azalma.get) == "Göze sıçrama", "B": all(abs(v - .5) < 1e-9 for v in azalma.values()),
      "C": azalma["Isı yanığı"] == 0, "D": max(G, key=lambda k: G[k][1]) == "Deriye temas", "E": top2 > top1 / 2}
kontrol(f"K3 verisi: göz %{azalma['Göze sıçrama'] * 100:.1f}, kesik %{azalma['Kesik'] * 100:.0f}, toplam {top1}→{top2}",
        abs(azalma["Göze sıçrama"] - .875) < 1e-9 and top1 == 30 and top2 == 11)
T["K3"] = tek_sik("Kıssa 3 (kaza grafiği)", k3, lambda v: v, "A")
k4 = yargi({"I": not V.birlikte({"Y"}, {"O"}), "II": V.birlikte({"A"}, {"T"}), "III": not V.birlikte({"Y"}, {"T"})})
T["K4"] = tek_sik("Kıssa 4 (depo)", Y_K, lambda v: v == k4, "C")

# --- Üstad
U1 = {"A": {"GHS02", "GHS07", "GHS09"}, "B": {"GHS02", "GHS06", "GHS08"}, "C": {"GHS03", "GHS06", "GHS05"},
      "D": {"GHS02", "GHS04", "GHS06"}, "E": {"GHS01", "GHS06", "GHS08"}}
h_ifade = {"H225": "GHS02", "H301+H311+H331": "GHS06", "H370": "GHS08"}
T["U1"] = tek_sik("Üstad 1 (H ifadeleri → piktogram)", U1, lambda v: v == set(h_ifade.values()) == V.MADDE_PIKTO["metanol"], "B")
u2_maddeler = {"etil alkol": {"Y", "T"}, "aseton": {"Y", "T"}, "potasyum nitrat": {"O"}, "sud kostik": {"A"}, "metanol": {"Y", "Z"},
               "bakır(II) sülfat": {"T"}}
for ad, sn in u2_maddeler.items():
    kontrol(f"U2 parantezi {ad}: {sorted(sn)} etiketle uyumlu",
            {V.GHS_SINIF[g] for g in V.MADDE_PIKTO[ad] if g in V.GHS_SINIF} == sn)
n2, yer2 = V.en_az_bolme(u2_maddeler)
T["U2"] = tek_sik(f"Üstad 2 (en az bölme {n2}: {yer2})", {"A": 2, "B": 3, "C": 4, "D": 5, "E": 6}, lambda v: v == n2, "C")
co = dict(V.CO_GRAFIK)


def co_t(t):
    ts = sorted(co)
    for a, b in zip(ts, ts[1:]):
        if a <= t <= b:
            return co[a] + (co[b] - co[a]) * (t - a) / (b - a)


ilk = min(t for t in range(0, 71) if co_t(t) >= V.CO_ESIK)
u3 = yargi({"I": ilk == 20, "II": co_t(50) < V.CO_ESIK, "III": co_t(40) > co_t(30)})
kontrol(f"U3: eşik ilk {ilk}. dk; 50. dk {co_t(50):.0f} ppm; eşik altına iniş ≈ 53,3. dk", abs(co_t(50 + 10 / 3) - V.CO_ESIK) < 1e-9)
T["U3"] = tek_sik("Üstad 3 (CO grafiği)", {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}},
                  lambda v: v == u3, "D")
# göz yukarıdayken bakış çizgisi ön yüzü menisküsün üstünde keser: daha yüksek işaret okunur.
# mezür: sayılar yukarı artar → fazla; büret: sayılar aşağı artar → az.
okuma = {"mezür": +1, "büret": -1}
u4 = yargi({"I": True, "II": okuma["mezür"] > 0, "III": okuma["büret"] > 0})
T["U4"] = tek_sik("Üstad 4 (paralaks)", {"A": {"I", "II"}, "B": {"I"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}},
                  lambda v: v == u4, "A")
UYARI = {"TEHLİKE": 2, "DİKKAT": 1}
u5 = yargi({"I": UYARI["TEHLİKE"] > UYARI["DİKKAT"], "II": True, "III": False})   # H314 → aşınma; H319 de göz koruması ister
T["U5"] = tek_sik("Üstad 5 (uyarı kelimesi)", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}},
                  lambda v: v == u5, "B")
duzelt = {"I": False, "II": True, "III": True}          # termometre doğru; su üstten giriyor (yanlış); tıpalı kap (kapalı sistem)
T["U6"] = tek_sik("Üstad 6 (damıtma)", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"II", "III"}},
                  lambda v: v == yargi(duzelt), "E")
dagilim([T[f"U{i}"] for i in range(1, 7)])
MER2 = V.en_az_bolme({s: {s} for s in V.SINIF})
kontrol(f"Merdiven 2: beş sınıf en az {MER2[0]} bölme {MER2[1]}", MER2[0] == 4)
MECLIS = {"M1": ("Yusuf", 3), "M2": ("Pamuk", 1), "M3": ("Yusuf", 2), "M4": ("Elif", 2)}

# ================================================================== 4. AKÇE, META
meta = json.load(open(os.path.join(BURA, "meta.json"), encoding="utf-8"))
AKCE = {2: 100, 3: 150, 4: 150, 5: 150, 6: 150, 7: 40, 8: 120, 9: 120, 10: 120, 11: 150, 12: 150}
kontrol(f"ünite toplamı {sum(AKCE.values())} = meta {meta['akce_toplam']} = 1400", sum(AKCE.values()) == meta["akce_toplam"] == 1400)
kontrol("meta durak akçeleri 100/150/150/150/150", [d["akce"] for d in meta["duraklar"]] == [100, 150, 150, 150, 150])
kontrol("10 hazine kartı, kodlar H1…H10, her biri +10 akçe", [h["kod"] for h in meta["hazine"]] == [f"H{i}" for i in range(1, 11)]
        and all("+10 akçe" in h.get("not", "") for h in meta["hazine"]))
kontrol("her durakta iki hazine kartı", all(sum(1 for h in meta["hazine"] if h["durak"] == d) == 2 for d in range(1, 6)))
nis = meta["nisanlar"]
kontrol("7 nişan: 5 durak + Kale Kapısı + Üstad Mührü (bonus, ustad, laj)",
        len(nis) == 7 and nis[5]["ikon"] == "kale" and nis[6]["ikon"] == "ustad" and nis[6]["renk"] == "laj" and nis[6].get("bonus"))
import sahneler_unite as SU  # noqa: E402
kontrol("nişan ikonları ünitede tanımlı", all(n["ikon"] in SU.NISAN_IKON for n in nis[:5]))
kontrol("medeniyet: er-Râzî (865–925) s.6 · Câbir bin Hayyân s.8", [(m["ad"], m["yil"], m["sayfa"]) for m in meta["medeniyet"]] ==
        [("Ebû Bekir er-Râzî", "865–925", 6), ("Câbir bin Hayyân", "8. yy", 8)])
CUBUK = [0, 0, 7, 18, 29, 39, 50, 53, 61, 70, 79, 89, 100, 100, 100]
birikim = [sum(v for k, v in AKCE.items() if k < s) for s in range(1, 16)]
kontrol(f"HUD akçe çubuğu % {CUBUK}", [round(b * 100 / 1400) for b in birikim] == CUBUK)
kontrol("Ahilik eşikleri 400 / 800 / 1150 (%28,57 / %57,14 / %82,14)", [round(x / 1400 * 100, 2) for x in (400, 800, 1150)] == [28.57, 57.14, 82.14])

# ================================================================== 5. SAYFADAN OKUMA
html = sayfa_oku(__file__)
if html:
    sayfa_ = {i: s for i, s in enumerate(re.findall(r'<section class="sayfa[^"]*">(.*?)</section>', html, re.S), 1)}
    kontrol("15 sayfa", len(sayfa_) == 15)
    sayfa_isaretleri_ayni(html, {k: v for k, v in T.items()})
    kontrol(f"meclis hükümleri {meclis_hukumleri(html)}", meclis_hukumleri(html) == MECLIS)
    kontrol(f"Cevaplar anahtar ızgarası {anahtar_izgarasi(html)}", anahtar_izgarasi(html) == ANAHTAR)
    izg = re.search(r'<div class="anahtar-izgara">(.*?)</div>\s*</div>', html, re.S).group(1)
    et = dict((int(n), int(d)) for n, d in re.findall(r"<i>(\d+)</i><b>[A-E]</b><small>(\d)\. durak</small>", izg))
    kontrol(f"anahtar ızgarasındaki durak etiketleri {et}", et == DURAK_ET)

    def sik_metni(kod):
        for k, blok in _bloklar(html):
            if k == kod:
                return {h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).replace("%__", "").strip()
                        for h, t in re.findall(r'<div(?: class="sik")?(?: data-dogru)?><b>([A-E])</b>(.*?)</div>', blok, re.S)}
        return {}

    YMET = {"Yalnız I": {"I"}, "Yalnız II": {"II"}, "Yalnız III": {"III"}, "I ve II": {"I", "II"}, "I ve III": {"I", "III"},
            "II ve III": {"II", "III"}, "I, II ve III": {"I", "II", "III"}}
    for kod, tablo in (("I6", Y5), ("I12", Y5b), ("K1", Y_K), ("K4", Y_K), ("U3", {"A": {"I"}, "B": {"III"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"I", "II", "III"}}),
                       ("U4", {"A": {"I", "II"}, "B": {"I"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}),
                       ("U5", {"A": {"I"}, "B": {"I", "II"}, "C": {"I", "III"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}),
                       ("U6", {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"I", "III"}, "E": {"II", "III"}})):
        okunan = {h: YMET.get(t) for h, t in sik_metni(kod).items()}
        kontrol(f"{kod} yargı şıkları sayfadaki metinle aynı", okunan == tablo)
    kontrol("I10 şıkları sayfada", {h: set(t.split(" ve ")) if "," not in t else {"I", "II", "III"} for h, t in sik_metni("I10").items()} ==
            {"A": {"I", "II"}, "B": {"I", "III"}, "C": {"II", "IV"}, "D": {"III", "IV"}, "E": {"I", "II", "III"}})
    kontrol("I1 şıkları GHS adlarıyla", list(sik_metni("I1").values()) == ["Yanıcı", "Yakıcı (oksitleyici)", "Patlayıcı", "Basınçlı gaz", "Tahriş edici"])
    kontrol("I3 şıkları 34–38", list(sik_metni("I3").values()) == ["34", "35", "36", "37", "38"])
    kontrol("I4 şıkları", sik_metni("I4") == I4S)
    kontrol("U2 şıkları 2–6", list(sik_metni("U2").values()) == ["2", "3", "4", "5", "6"])
    kontrol("K2 şıkları", [t.replace(" ", "") for t in sik_metni("K2").values()] ==
            ["Mezür–Beherglas–Pipet", "Balonjoje–Erlenmayer–Büret", "Büret–Balonjoje–Pipet",
             "Pipet–Erlenmayer–Büret", "Pipet–Beherglas–Mezür"])
    kontrol("I7 doğru şık başka bir yanıcı sıvı (alev)", "yanıcı" in sik_metni("I7")["E"])
    kontrol("I8 doğru şık enjektör", "enjektör" in sik_metni("I8")["E"])
    kontrol("I11 D şıkkı ünlem–patlama eşleşmesi", "Ünlem" in sik_metni("I11")["D"] and "patlar" in sik_metni("I11")["D"])
    kontrol("U1 B şıkkı alev, kurukafa, sağlık", sik_metni("U1")["B"] == "Alev, kurukafa, sağlık")

    # piktogram ↔ ad ↔ anlam (sayfa 4 ızgarası) ve bütün data-ghs kodları
    kartlar = re.findall(r'<div class="ghs-kart"><svg[^>]*data-ghs="(GHS0\d)".*?</svg><div><b>([^<]+)<small>([^<]+)</small></b><p>([^<]+) <i>Örn\. ([^<]+)\.</i>',
                         sayfa_[4], re.S)
    kontrol(f"s.4 GHS ızgarası 9 kart, sıra GHS01…09 ({len(kartlar)})", [k[0] for k in kartlar] == kodlar)
    for kod, ad, simge, anlam, ornek in kartlar:
        kontrol(f"s.4 {kod}: {ad} · {simge}", (kod, ad, simge, anlam, ornek) in [(a, b, c, d, e) for a, b, c, d, e in V.GHS])
    tum = re.findall(r'data-ghs="([^"]+)"', html)
    kontrol(f"sayfadaki bütün piktogram kodları geçerli ({len(tum)} adet)", all(k in kodlar for k in tum))
    blok = dict(_bloklar(html))
    kontrol("I1 kartında GHS03, I6 kartında GHS05 çizili", 'data-ghs="GHS03"' in blok["I1"] and 'data-ghs="GHS05"' in blok["I6"])
    kontrol("I10 kartındaki işaret sırası", re.findall(r'data-isaret="([^"]+)"', blok["I10"]) == I10_ISARET)
    gorev4 = sayfa_[4].split("Görev 1", 1)[1].split("SONUÇ", 1)[0]
    kontrol("s.4 metanol görevinde çizilen piktogramlar = metanol etiketi", set(re.findall(r'data-ghs="([^"]+)"', gorev4)) == V.MADDE_PIKTO["metanol"])
    k4b = re.findall(r'data-ghs="([^"]+)".*?<span>([XYZT])</span>', blok["K4"], re.S)
    kontrol(f"K4: X alev, Y çember, Z aşınma, T ünlem {k4b}", k4b == [("GHS02", "X"), ("GHS03", "Y"), ("GHS05", "Z"), ("GHS07", "T")])
    k1b = re.findall(r'data-ghs="([^"]+)"', blok["K1"])
    kontrol("K1: alev + ünlem çizili", k1b == ["GHS02", "GHS07"])
    hul = re.findall(r'data-ghs="([^"]+)"', sayfa_[7])
    kontrol("Hülasa: dokuz piktogramın hepsi", hul == kodlar)
    # işaret ızgarası: her işaret kendi ailesinin sütununda
    for aile, ic in re.findall(r'<div class="isaret-aile (\w+)">(.*?)</div></div></div>', sayfa_[2], re.S):
        isr = re.findall(r'data-isaret="([^"]+)"', ic)
        kontrol(f"s.2 işaret ailesi {aile}: {isr}", isr and all(V.ISARET[k][0] == aile for k in isr))
    g2 = re.findall(r'data-isaret="([^"]+)"', sayfa_[2].split("Görev 1", 1)[1].split("SONUÇ", 1)[0])
    kontrol(f"s.2 görev: I zorunluluk, II uyarı, III yasak, IV acil {g2}", [V.ISARET[k][0] for k in g2] == ["zor", "uya", "yas", "acil"])

    # akçe: durak sayfaları (levha dışındaki çipler + hazine), yan yollar, imtihan
    def cipler(s):
        govde = s.split('<main class="ic"', 1)[1]
        return [int(x) for x in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', govde)]

    for no in (2, 3, 4, 5, 6):
        s = sayfa_[no]
        hz = len(re.findall(r'<div class="hazine[ "]', s))
        top = sum(cipler(s)) + 10 * hz
        kontrol(f"s.{no} akçe: çipler {cipler(s)} + {hz} hazine = {top} (beklenen {AKCE[no]})", top == AKCE[no] and hz == 2)
        lev = re.search(r'<div class="hedef">.*?<span class="cip akce">\+(\d+) akçe</span>', s, re.S)
        kontrol(f"s.{no} levhadaki akçe {lev.group(1) if lev else None}", lev and int(lev.group(1)) == AKCE[no])
    kontrol("s.7 muhasebe 6 satır +40", "6 satır = +40 akçe" in sayfa_[7] and sayfa_[7].count('<div class="satir">') == 6)
    kontrol("s.8 meclis 4 × 30", cipler(sayfa_[8]).count(30) == 4 and sum(cipler(sayfa_[8])) == 120)
    kontrol("s.9 kıssa 4 × 30", "4 × 30 = +120 akçe" in sayfa_[9] and cipler(sayfa_[9]).count(30) == 4)
    kontrol("s.10 merdiven 3 × 40", "3 × 40 = +120 akçe" in sayfa_[10] and sayfa_[10].count('class="kart merdiven"') == 3)
    kontrol("s.11–12 imtihan 12 × 25", cipler(sayfa_[11]).count(25) + cipler(sayfa_[12]).count(25) == 12)
    kontrol("s.13 Üstad akçesiz", not cipler(sayfa_[13]))
    bar = [int(x) for x in re.findall(r'<span class="bar"><i style="width:(\d+)%">', html)]
    kontrol(f"HUD çubukları sayfada {bar}", bar == CUBUK)
    defter = [int(x) for x in re.findall(r'<td class="n">(\d+)</td>', sayfa_[15])]
    kontrol(f"final akçe defteri {defter}", defter[:-1] == [100, 150, 150, 150, 150, 40, 120, 120, 120, 300] and defter[-1] == 1400 == sum(defter[:-1]))

    # Cevaplar sayfası satırları
    cv = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sayfa_[14]))
    for i, h in ANAHTAR.items():
        kontrol(f"Cevaplar: İmtihan {i} · {h}", f" {i} · {h} " in cv)
    kontrol("Cevaplar: Kıssa 1 E 2 D 3 A 4 C", "Kıssa 1 E 2 D 3 A 4 C" in cv)
    kontrol("Cevaplar: Meclis 1 Yusuf 2 Pamuk 3 Yusuf 4 Elif", "Meclis 1 Yusuf 2 Pamuk 3 Yusuf 4 Elif" in cv)
    ust = cv.split("Üstad soruları", 1)[1]
    for k in range(1, 7):
        kontrol(f"Cevaplar: Üstad {k} · {T[f'U{k}']}", f"{k} · {T[f'U{k}']}" in ust)
    for k, (kisi, satir) in MECLIS.items():
        kontrol(f"Cevaplar: Meclis {k[1]} · {kisi}, satır {satir}", f"Meclis {k[1]} · {kisi}, satır {satir}" in cv)
    for parca in ("36 mL", "%87,5", "≈ 53", "15–20"):
        kontrol(f"Cevaplar: '{parca}'", parca in cv)

    # öğretmen metinleri: meclis NEDEN ≤ 14, DOĞRUSU ≤ 45, merdiven ≤ 50, karalama ≤ 75, her soru kartında bir karalama çözümü
    for kod, blok_ in _bloklar(html):
        if kod.startswith("M"):
            neden = re.search(r'NEDEN\?<span class="cizgili"><span class="ogr">(.*?)</span>', blok_).group(1)
            dogru = re.search(r'DOĞRUSU<span class="cizgili"><span class="ogr">(.*?)</span>', blok_).group(1)
            kontrol(f"{kod} öğretmen: NEDEN '{neden}' ≤ 14 · DOĞRUSU ≤ 45 ({len(dogru)})", len(neden) <= 14 and len(dogru) <= 45)
        elif kod[0] in "IKU":
            kar = re.findall(r'<div class="karalama"><span class="ogr">(.*?)</span>', blok_)
            if kod in ("I6", "I12"):      # yargılı kısa kartlar: karalamasız, çözüm Cevaplar'da
                kontrol(f"{kod} karalamasız kısa kart", not kar)
            else:
                kontrol(f"{kod} karalamada öğretmen çözümü (≤ 75 harf)", len(kar) == 1 and len(re.sub(r"<[^>]+>", "", kar[0])) <= 75)
    for satir in re.findall(r'<div class="cozum-alani">(.*?)</div></div></div>', sayfa_[10], re.S):
        for t in re.findall(r'<span class="ogr">(.*?)</span></div>', satir):
            kontrol(f"merdiven satırı ≤ 50: '{re.sub('<[^>]+>', '', t)}'", len(re.sub(r"<[^>]+>", "", t)) <= 50)
    cevap_kutu = re.findall(r'<div class="cevap-kutu">CEVABIN:<span class="ogr">(.*?)</span>', html)
    kontrol(f"5 hızlı görevin hepsinde öğretmen cevabı {cevap_kutu}", len(cevap_kutu) == 5 and all(cevap_kutu))
    hk = re.findall(r'<b>Hızlı kontrol:</b>.*?<span class="ogr">(.*?)</span>', html, re.S)
    kontrol(f"5 hızlı kontrolün hepsinde öğretmen cevabı {hk}", len(hk) == 5 and all(hk))

    # kalın yazıda fontta olmayan sembol yok; ilk yardım ve hassasiyet dili
    kalin = " ".join(re.findall(r"<b>(.*?)</b>", html, re.S))
    kontrol("kalın metinde ✓ ✗ ★ ☆ → ← ⚠ yok", not re.search("[✓✗★☆→←⚠]", re.sub(r"<[^>]+>", "", kalin)))
    duz = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", " ", html, flags=re.S)))
    kontrol("ilk yardım: kimyasal sıçramada 15–20 dakika bol akan su", duz.count("15–20 dakika") >= 2)
    kontrol("ilk yardım: yanığa buz yok, nötrleştirme yok, kusturma yok",
            "buz, diş macunu, yağ sürme" in duz and "nötrleştirme yok" in duz and "Kusturma" in duz)
    yasak = [r"facia", r"felaket", r"hayatını kaybet", r"\böldü", r"can kaybı", r"\bölüm\b", r"patlamada", r"\b2022\b"]
    bulunan = [y for y in yasak if re.search(y, duz.lower())]
    kontrol(f"hassasiyet: felaket/kayıp dili yok {bulunan}", not bulunan)
    cumleler = re.split(r"[.!?]", duz)
    kontrol("hassasiyet: Amasra hiçbir cümlede maden/ocak/grizu ile birlikte geçmez",
            not any("Amasra" in c and re.search(r"maden|ocak|grizu|kömür", c, re.I) for c in cumleler))
    kontrol("sayfa göndermeleri s.N biçiminde (ham {{ yok)", "{{" not in re.sub(r"<!--.*?-->", "", html, flags=re.S))

D.sonuc()
