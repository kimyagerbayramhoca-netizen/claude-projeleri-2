#!/usr/bin/env python3
"""Geliştirme örneği · atom modelleri — bilgi ve sayı denetimi. Sonunda "SONUÇ: hepsi doğru" yazmalı.

    python3 uretec/dogrula.py        (önce python3 uretec/kur.py: atom-modelleri-van-golu.html okunur)

Denetlenenler: model yılları (sayfa ↔ doğrulanmış tablo), Rydberg ile H'nin görünür çizgileri, −13,6/n² eV düzeyleri,
foton enerjileri (12,09 = 1,89 + 10,20), α/elektron kütle oranı (≈ 7300), çekirdek/atom ölçeği (nohut–stadyum),
Bohr'un tek elektronlu tanecikleri, Na 2·8·1, dalga boyu renk tablosu (9/03 ile aynı), Medeniyetimizden metni (9/03
meta.json ile aynı), Kendini dene cevapları, Hap Bilgi ailesinin altı türünün sayfalarda kullanımı, tema kontrastları.
"""
import importlib.util
import os
import re
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
sys.path.insert(0, os.path.join(KITAP, "yerel-ortak"))
sys.path.insert(0, BURA)
from dogrula_ortak import D, kontrol  # noqa: E402
import infografik_gelistirme as IG  # noqa: E402
import konu_karakterleri as KK  # noqa: E402
import tema as TM  # noqa: E402

html_yol = os.path.join(KLASOR, "atom-modelleri-van-golu.html")
if not os.path.exists(html_yol):
    sys.exit("önce: python3 uretec/kur.py --tema van-golu")
HTML = open(html_yol, encoding="utf-8").read()
METIN = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>|<svg.*?</svg>", " ", HTML, flags=re.S)))
SVGMETIN = " ".join(re.findall(r">([^<>]+)</t(?:ext|span)>", HTML))

# ------------------------------------------------------------------ 1. model yılları (doğrulanmış tablo → sayfa)
YIL = {"Demokritos": "MÖ y. 400", "Dalton": "1803–1808", "Thomson": "1897 · 1904", "Rutherford": "1911", "Bohr": "1913", "Modern model": "1920’ler"}
for ad, yil in YIL.items():
    kontrol(f"Model zinciri plakası: {ad} · {yil}", re.search(rf"<b>{ad}</b><span>{re.escape(yil)}</span>", HTML) is not None)
kontrol("Thomson: elektron 1897 (katot ışınları), model 1904", "katot ışınlarında elektron (1897)" in METIN)
kontrol("Altın levha deneyi 1909–1911, çekirdekli model 1911", "altın levha deneyi (1909–1911)" in METIN and "Rutherford’un yorumu (1911)" in METIN)
kontrol("Kuantum modeli 1920'ler: de Broglie 1924, Schrödinger 1926", "de Broglie 1924 · Schrödinger 1926" in METIN)
kontrol("Geiger–Marsden düzeneği 1909", "1909 · Düzenek." in METIN and "Geiger ve Marsden’in deneyi (1909)" in METIN)
kontrol("Demokritos ≈ 2400 yıl önce (MÖ y. 400 → 2026)", abs((2026 + 400) - 2400) <= 50)

# ------------------------------------------------------------------ 2. hidrojen: Rydberg ve Bohr enerjileri
R = 1.09678e7                                               # m⁻¹ (9/03 dogrula.py ile aynı)
balmer = {n: round(1e9 / (R * (1 / 4 - 1 / n ** 2))) for n in (3, 4, 5, 6)}
kontrol(f"Rydberg: n → 2 çizgileri {balmer} == çizim {IG.BALMER}", balmer == IG.BALMER)
kontrol("Görünür dört çizgi sayfada: 410 · 434 · 486 · 656 nm", "410 · 434 · 486 · 656 nm" in METIN)
for nm in (410, 434, 486, 656):
    kontrol(f"Spektrum etiketi {nm} çizimde", f">{nm}<" in HTML)
E = {n: -13.6 / n ** 2 for n in range(1, 7)}
kontrol("Düzey enerjileri −13,6/n² (çizimle aynı)", all(abs(IG.ENERJI[n] - E[n]) < 1e-9 for n in E))
for n, etk in {1: "−13,6", 2: "−3,40", 3: "−1,51", 4: "−0,85", 5: "−0,54", 6: "−0,38"}.items():
    kontrol(f"n = {n} etiketi {etk}", f"{E[n]:.2f}".replace(".", ",").replace("-", "−").startswith(etk if n > 1 else "−13,60") and etk in SVGMETIN)
e13, e32, e21 = E[3] - E[1], E[3] - E[2], E[2] - E[1]
kontrol(f"Soğurma 1 → 3: {e13:.3f} eV ≈ 12,09", round(e13, 2) == 12.09 and "12,09 eV’luk UV" in METIN)
kontrol(f"Yayma 3 → 2: {e32:.3f} eV ≈ 1,89 ve 1239,84/E ≈ 656 nm", round(e32, 2) == 1.89 and round(1239.84 / e32) in (656, 657) and "1,89 eV’luk" in METIN)
kontrol(f"Yayma 2 → 1: {e21:.2f} eV = 10,20 (UV: {1239.84 / e21:.1f} nm < 400)", round(e21, 2) == 10.2 and 1239.84 / e21 < 400 and "10,20 eV’luk UV" in METIN)
kontrol("Enerji korunur: 1,89 + 10,20 = 12,09", round(1.89 + 10.20, 2) == 12.09 and abs(e32 + e21 - e13) < 1e-9)
kontrol("1 → 3 soğurma fotonu UV (102,6 nm)", 1239.84 / e13 < 400)
kontrol("Kendini dene (s.4): 4 → 2 iniş ışık YAYAR (486 nm)", E[4] > E[2] and balmer[4] == 486 and "1 yayar (486 nm)" in METIN)
kontrol("Kendini dene (s.4): 6 → 2 dalga boyu 3 → 2'den kısa (410 < 656)", balmer[6] < balmer[3] and "2 6’dan 2’ye (410 nm)" in METIN)
kontrol("Kilit bilgi: fark büyüdükçe dalga boyu kısalır", (E[6] - E[2]) > (E[3] - E[2]) and balmer[6] < balmer[3])

# ------------------------------------------------------------------ 3. Bohr'un sınırı, Na katmanları
tek = {"H": (1, 0), "He+": (2, 1), "Li2+": (3, 2)}
kontrol("H, He⁺, Li²⁺ tek elektronlu (Z − yük = 1)", all(z - q == 1 for z, q in tek.values()))
kontrol("Sayfada Bohr sınırı: H, He⁺, Li²⁺", HTML.count("(H, He<sup>+</sup>, Li<sup>2+</sup>)") >= 2)
kontrol("Kendini dene (s.2): Bohr H'ye uyar, Na'ya (11 e⁻) uymaz", 11 - 0 > 1 and "2 H atomu" in METIN)
kontrol("Bohr karakteri Na 2 · 8 · 1 (= 11, K ≤ 2, L ≤ 8)", 2 + 8 + 1 == 11 and 2 <= 2 * 1 ** 2 and 8 <= 2 * 2 ** 2)

# ------------------------------------------------------------------ 4. altın levha: ölçek ve kütle
m_alfa, m_e = 6.6446573e-27, 9.1093837e-31
kontrol(f"α / elektron kütle oranı {m_alfa / m_e:.0f} ≈ 7300", abs(m_alfa / m_e - 7300) < 50 and "yaklaşık 7300 kat" in METIN)
oran_atom = 1e-10 / 1e-14, 1e-10 / 1e-15                     # atom ≈ 10⁻¹⁰ m, çekirdek ≈ 10⁻¹⁴–10⁻¹⁵ m
kontrol(f"Çekirdek atomdan on binlerce kat küçük ({oran_atom[0]:.0e}–{oran_atom[1]:.0e})", 1e4 <= oran_atom[0] and oran_atom[1] <= 1e5)
kontrol(f"Nohut–stadyum benzetmesi aynı ölçekte (200 m / 0,8 cm = {200 / .008:.0f})", 1e4 <= 200 / .008 <= 1e5)
kontrol("α = He çekirdeği: 2 p + 2 n, yük +2", 2 + 2 == 4 and "2 proton + 2 nötron · yükü +2" in METIN)
kontrol("Kendini dene (s.3) cevapları: boşluk · (+) çekirdek", "1 atomun çoğu boşluk · 2 (+) çekirdek" in METIN)
kontrol("Kendini dene (s.2): altın levhayı Thomson açıklayamaz", "1 Thomson" in METIN)

# ------------------------------------------------------------------ 5. 9/03 ile aynı kaynaklar
spec = importlib.util.spec_from_file_location("ay_info", os.path.join(KITAP, "9-sinif-yerel", "03-atom-ve-yapisi", "uretec", "infografik_unite.py"))
AY = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AY)
kontrol("Dalga boyu → renk tablosu 9/03 ile aynı", KK.NM_TABLO == AY._NM)
kontrol("H çizgileri 9/03 ile aynı", tuple(sorted(IG.BALMER.values())) == AY.CIZGI["H"])
kontrol("Tanecik renkleri 9/03 ile aynı", (KK.PROTON, KK.NOTRON, KK.ELEKTRON) == (AY.PROTON, AY.NOTRON, AY.ELEKTRON))
import json  # noqa: E402
meta_ay = json.load(open(os.path.join(KITAP, "9-sinif-yerel", "03-atom-ve-yapisi", "uretec", "meta.json"), encoding="utf-8"))
bat = [m for m in meta_ay["medeniyet"] if m["ad"] == "el-Battânî"][0]
kontrol("Medeniyetimizden: el-Battânî yılı 9/03 meta ile aynı", f"({bat['yil']})" in METIN)
kontrol("Medeniyetimizden: 365 gün 5 saat 46 dakika 24 saniye (9/03 meta)", "365 gün 5 saat 46 dakika 24 saniye" in bat["katki"] and "365 gün 5 saat 46 dakika 24 saniye" in METIN)
kontrol("Medeniyetimizden: Harran’da doğdu, Rakka’da gözlem", "Harran’da doğdu" in METIN and "Rakka’da" in METIN)

# ------------------------------------------------------------------ 6. Hap Bilgi ailesi ve öneriler sayfalarda
sablon = open(os.path.join(BURA, "sablon.html"), encoding="utf-8").read()
for tur in ("hb-hap", "hb-kural", "hb-unutma", "hb-radar", "hb-dikkat", "hb-kilit"):
    sayfalar = [i + 1 for i, s in enumerate(sablon.split('<section class="sayfa')[1:]) if tur in s]
    kontrol(f"{tur} sayfalarda kullanılıyor: {sayfalar}", bool(sayfalar))
for oneri in ("bakista", "kendini-dene", "ikili", "tahmin"):
    kontrol(f"öneri bileşeni '{oneri}' sayfada", f'class="{oneri}' in sablon or f' {oneri}"' in sablon or f'kart {oneri}' in sablon)

# ------------------------------------------------------------------ 7. tema kontrastları
for ad in TM.SIRA:
    es = TM.Esleme(ad)
    kontrol(f"{TM.TEMALAR[ad]['ad']}: gövde metni obs/kar ≥ 7", TM.kontrast(es.token("obs"), es.token("kar")) >= 7)
    for y, z in (("gol-k", "gol-aa"), ("keh-k", "keh-a"), ("mer-k", "mer-a"), ("kob-k", "kob-a")):
        kontrol(f"{TM.TEMALAR[ad]['ad']}: {y}/{z} ≥ 4,5", TM.kontrast(es.token(y), es.token(z)) >= 4.5)

D.sonuc()
