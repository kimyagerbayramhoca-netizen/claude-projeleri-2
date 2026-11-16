#!/usr/bin/env python3
"""Karma temalar · bilgi, sayı ve palet denetimi. Sonunda "SONUÇ: hepsi doğru" yazmalı.

    python3 uretec/dogrula.py        (önce python3 uretec/kur.py)

10. sınıf (Gazlar) sayfalarındaki her sayı yeniden hesaplanır: R = 22,4/273, T = t + 273, Boyle/Charles oranları
(pistonlu kap ve J borusu çizimindeki hacim sütunları dahil), kinetik kutular (E_k ∝ T, hız ∝ √T), PV = nRT görevleri,
Graham (tünel yarışı yolları, NH₃–HCl borusu, sızma süresi), mol kütleleri; çizgi roman tarihleri ve iddiaları
(doğrulanmış tablo). 9. sınıf sayfaları atom-modelleri şablonundan aynen kurulur (orada dogrula.py: 83 denetim);
burada yalnız tarihleri ve paleti denetlenir. Paletler: anlam renkleri, Doğrusu yeşili, WCAG eşikleri, döteranopi çiftleri.
"""
import math
import os
import re
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
ATOM = os.path.join(KITAP, "gelistirme", "atom-modelleri", "uretec")
sys.path.insert(0, os.path.join(KITAP, "yerel-ortak"))
sys.path.insert(0, ATOM)
sys.path.insert(0, BURA)
from dogrula_ortak import D, kontrol  # noqa: E402
import infografik_karma as IK  # noqa: E402
import konu_karakterleri as KK  # noqa: E402
import tema as TM  # noqa: E402
import katalog_karma as KAT  # noqa: E402


def oku(ad):
    yol = os.path.join(KLASOR, ad)
    if not os.path.exists(yol):
        sys.exit(f"önce: python3 uretec/kur.py ({ad} yok)")
    html = open(yol, encoding="utf-8").read()
    metin = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>|<svg.*?</svg>", " ", html, flags=re.S)))
    return html, metin.replace(" ,", ",")


H10, M10 = oku("karma-10-gol-rasathane.html")
H9, M9 = oku("karma-9-cini-toprak.html")
SVG10 = " ".join(re.findall(r">([^<>]+)</t(?:ext|span)>", H10))
TAM = re.sub(r"<[^>]+>", "", H10)          # etiketleri atılmış ham metin (alt simgeler bitişik)

# ------------------------------------------------------------------ 1. sabitler
R = 22.4 / 273
kontrol(f"R = 22,4 / 273 = {R:.5f} ≈ 0,082", round(R, 3) == 0.082 and "R = 22,4 / 273 ≈ 0,082" in M10)
K_ = lambda t: t + 273  # noqa: E731
kontrol("T = t + 273 sayfada", "T = t + 273" in M10)
AK = dict(H=1, He=4, C=12, N=14, O=16, S=32, Cl=35.5)
MOL = {"he": AK["He"], "h2": 2 * AK["H"], "o2": 2 * AK["O"], "n2": 2 * AK["N"], "co2": AK["C"] + 2 * AK["O"], "so2": AK["S"] + 2 * AK["O"], "ch4": AK["C"] + 4 * AK["H"]}
for k, vb, ad, M, _ in KK.GAZLAR:
    kontrol(f"gaz karakteri {ad}: M = {M} (atom kütlelerinden {MOL[k]})", M == MOL[k])
kontrol("hava ≈ 29 g/mol (0,78·28 + 0,21·32 + 0,01·40 = 28,96)", round(0.78 * 28 + 0.21 * 32 + 0.01 * 40) == 29)

# ------------------------------------------------------------------ 2. (a) Boyle ve Charles
kontrol("Boyle: 1 atm · V = 2 atm · V/2", 1 * 1 == 2 * 0.5)
y_alt, tam, yari = 396, 150, 273      # pistonlu_kap: silindir tabanı ve piston yüksekliği (çizimle aynı)
src = open(os.path.join(BURA, "infografik_karma.py"), encoding="utf-8").read()
kontrol("pistonlu kap çiziminde y_alt=396, tam=150, yarı=273", "y_ust, y_alt, w = 96, 396, 300" in src and "tam, yari = 150, 273" in src)
kontrol(f"pistonlu kap: gaz sütunu {y_alt - tam} ve {y_alt - yari} → oran 2 (V ↔ V/2, V ↔ 2V)", (y_alt - tam) == 2 * (y_alt - yari))
kontrol("Charles: 300 K → 600 K, P sabit → V iki katı", 600 / 300 == 2)
kontrol("J borusu: cıva farkı 76 cmHg = 1 atm; toplam 2 atm → hava hacmi yarıya", (76 + 76) / 76 == 2)
kontrol("J borusu çizimi: hava sütunu 140 → 70 birim (önce/sonra)", (420 - 280) == 2 * (350 - 280) and "j2, (xr2, w) = _j_boru(s, 330, 150, 0, 210, 350, 280, 430)" in src)
v2 = 2.6 * K_(27) / K_(-13)
kontrol(f"Kendini dene (s.3): −13 °C’de 2,6 L → 27 °C’de {v2:.2f} L = 3 L", abs(v2 - 3) < 1e-9 and "2 3 L" in M10)
kontrol("Kendini dene (s.3): T sabit, V yarıya → P 2 katı", "1 2 katına" in M10)

# ------------------------------------------------------------------ 3. çizgi roman: tarihler ve iddialar (doğrulanmış tablo)
TARIH = [("1662 · Boyle.", "Boyle J borusu deneyi, 1662"), ("1 Aralık 1783 · Paris.", "Charles–Robert hidrojen balonu, 1 Aralık 1783"),
         ("Charles ile Robert, hidrojen balonuyla havalanıyor", "Charles ve Nicolas-Louis Robert, hidrojen"), ("Tuileries Bahçesi", "kalkış Tuileries Bahçesi"),
         ("Yaklaşık 550 m’ye çıktılar", "yükseklik ≈ 550 m (≈ 1800 ft)"), ("2 saat 5 dakikada 36 km uçtular", "2 sa 5 dk, 36 km"),
         ("Nesles-la-Vallée’ye iniş", "iniş Nesles-la-Vallée"), ("kum torbası atarak yükseldiler", "kum safrasıyla yükseklik ayarı"),
         ("1787 dolayı.", "Charles yasası y. 1787, yayımlanmadı"), ("1802’de Gay-Lussac yayımladı, Charles’a bağladı", "Gay-Lussac 1802, Charles’ı kaynak gösterdi")]
for parca, ad in TARIH:
    kontrol(f"çizgi roman: {ad}", parca in M10)
kontrol("çizgi roman: gerçek kişi yüzü yok (balon sepetinde yüzsüz siluet)", "yüzsüz siluet" in src)

# ------------------------------------------------------------------ 4. (b) kinetik teori ve ideal gaz
kontrol(f"kinetik kutular: {IK.KUTU_T} K = −73, 27, 327 °C", [t - 273 for t in IK.KUTU_T] == [-73, 27, 327] and all(f"({c} °C)" in SVG10 for c in ("−73", "27", "327")))
ek = [t / IK.KUTU_T[0] for t in IK.KUTU_T]
hiz = [math.sqrt(x) for x in ek]
kontrol(f"ortalama E_k oranı {ek} → ×1 · ×1,5 · ×3", ek == [1, 1.5, 3] and all(f"×{e}" in SVG10 for e in ("1", "1,5", "3")))
kontrol(f"hız oranı √(T/200) = {[round(h, 2) for h in hiz]} → 1 · 1,22 · 1,73", [round(h, 2) for h in hiz] == [1, 1.22, 1.73] and "hız ×1,22" in SVG10 and "hız ×1,73" in SVG10)
kontrol("Dikkat!: 27 °C = 300 K", K_(27) == 300 and "27 °C = 300 K" in M10)
kontrol(f"Dikkat!: 20 → 40 °C hacim oranı {K_(40) / K_(20):.4f} ≈ 1,07 (2 değil)", round(K_(40) / K_(20), 2) == 1.07 and "313/293 ≈ 1,07" in M10)
PV = 0.9 * 2.46e6
n1, n2 = PV / (0.082 * K_(27)), PV / (0.082 * K_(87))
kontrol(f"Görev 6: PV = {PV:.4g} = 2,214·10⁶", abs(PV - 2.214e6) < 1)
kontrol(f"Görev 6: n₁ = {n1:.1f} = 90 000 mol, n₂ = {n2:.1f} = 75 000 mol", round(n1) == 90000 and round(n2) == 75000 and "90 000 mol" in M10 and "75 000 mol" in M10)
kontrol(f"Görev 6: çıkan {(n1 - n2) * 29:.0f} g ≈ 435 kg", round((n1 - n2) * 29) == 435000 and "435 000 g" in M10 and "435 kg" in M10)
V = 0.4 * 0.082 * K_(27) / 2.46
kontrol(f"Kendini dene (s.5): V = nRT/P = {V:.3f} L = 4 L", abs(V - 4) < 1e-9 and "1 4 L" in M10)
kontrol("Kendini dene (s.5): aynı T’de ortalama E_k eşit", "2 eşit" in M10)

# ------------------------------------------------------------------ 5. (c) difüzyon ve Graham
for k, ad, M in IK.YARIS:
    d = IK.yol_m(M)
    kontrol(f"tünel yarışı: {ad} (M = {M}) aynı sürede {d:.2f} m = 10·√(64/{M})", abs(d - 10 * math.sqrt(64 / M)) < 1e-9 and MOL[k] == M)
kontrol("tünel etiketleri: 40 m · 20 m · ≈ 14,1 m · 10 m", all(x in SVG10 for x in ("40 m", "20 m", "≈ 14,1 m", "10 m")))
kontrol("tünel etiketleri: 4 · 2 · ≈ 1,41 kat hızlı", all(x in SVG10 for x in ("4 kat hızlı", "2 kat hızlı", "≈ 1,41 kat hızlı")))
kontrol("He / SO₂: √(64/4) = √16 = 4", math.sqrt(64 / 4) == 4 and "√(64 / 4) = √16 = 4" in M10)
x = 100 * math.sqrt(36.5 / 17) / (1 + math.sqrt(36.5 / 17))
kontrol(f"Görev 8: √(36,5/17) = {math.sqrt(36.5 / 17):.3f} ≈ 1,47; halka NH₃ ucundan {x:.1f} ≈ 59 cm", round(math.sqrt(36.5 / 17), 2) == 1.47 and round(x) == 59 and "≈ 59 cm" in M10)
kontrol("Kendini dene (s.6): H₂/O₂ = √(32/2) = 4 kat", math.sqrt(32 / 2) == 4 and "1 4 kat" in M10)
t_ch4 = 30 * math.sqrt(16 / 64)
kontrol(f"Kendini dene (s.6): SO₂ 30 s → CH₄ {t_ch4:.0f} s", t_ch4 == 15 and "2 15 s" in M10)
kontrol("Altın Kural: v₁/v₂ = √(M₂/M₁) = t₂/t₁", "√(M2 / M1) = t2 / t1" in M10.replace("₁", "1").replace("₂", "2") or "√(M<sub>2</sub> / M<sub>1</sub>) = t<sub>2</sub> / t<sub>1</sub>" in H10)
kontrol("CO₂ (44) havadan (≈ 29) ağır", MOL["co2"] == 44 > 29 and "(44) havadan (≈ 29) ağır" in M10)
kontrol("Derinkuyu ≈ 85 m (Gazlar ünitesi metni)", "yaklaşık 85 m derine iner" in M10)
kontrol("gaz molekül biçimleri: CO₂ doğrusal, SO₂ ≈ 119° kırık", "a = math.radians(59.5)" in open(os.path.join(BURA, "konu_karakterleri.py"), encoding="utf-8").read())

# ------------------------------------------------------------------ 6. 9. sınıf (atom modelleri, aynı şablon)
for ad, yil in {"Demokritos": "MÖ y. 400", "Dalton": "1803–1808", "Thomson": "1897 · 1904", "Rutherford": "1911", "Bohr": "1913", "Modern model": "1920’ler"}.items():
    kontrol(f"9. sınıf plaka: {ad} · {yil}", re.search(rf"<b>{ad}</b><span>{re.escape(yil)}</span>", H9) is not None)
kontrol("9. sınıf: H çizgileri 410 · 434 · 486 · 656 nm", "410 · 434 · 486 · 656 nm" in M9)

# ------------------------------------------------------------------ 7. paletler
cini, gol = TM.Esleme("cini-toprak"), TM.Esleme("gol-rasathane")
for es, ad in ((cini, "Çini ve Toprak"), (gol, "Göl ve Rasathane")):
    kontrol(f"{ad}: Doğrusu yeşili #1A7F53", es.token("zumrut") == "#1A7F53")
    L, a, b = TM.oklab(es.token("mer"))
    kontrol(f"{ad}: Tuzak rengi kırmızı ailede ({es.token('mer')})", a > .12 and L < .7)
    L, a, b = TM.oklab(es.token("keh"))
    kontrol(f"{ad}: akçe rengi altın-kehribar ailede ({es.token('keh')})", b > .12 and a > 0)
kontrol("iki kitapta balon/kart tintleri ortak (mer-a, keh-a)", cini.token("mer-a") == gol.token("mer-a") and cini.token("keh-a") == gol.token("keh-a"))
kontrol("iki kitap ilk bakışta farklı: ana renk (gol) OKLab uzaklığı > 0,15", math.dist(TM.oklab(cini.token("gol")), TM.oklab(gol.token("gol"))) > .15)
rd = KAT.renk_denetimi()
for ad in TM.SIRA:
    zayif = [k["ad"] for k in rd[ad]["kontrast"] if k["oran"] < k["esik"]]
    kontrol(f"{TM.TEMALAR[ad]['ad']}: bütün yazı/zemin çiftleri eşiğin üstünde {zayif or ''}", not zayif)
    kalan = [c["ad"] for c in rd[ad]["ciftler"] if c["doteranopi"] < 6]
    kontrol(f"{TM.TEMALAR[ad]['ad']}: döteranopide ΔE < 6 kalan tek çift ikili kart zeminleri {kalan}", kalan in ([], ["Yanlış ↔ doğru zemini"]))
css = open(os.path.join(BURA, "karma.css"), encoding="utf-8").read()
kontrol("ikili kart biçim ipucu: kesik mercan ↔ düz yeşil çerçeve (karma.css)", ".ikili .yan.y { border: .4mm dashed var(--mer); }" in css and ".ikili .yan.d { border: .4mm solid var(--zumrut); }" in css)
kontrol("CSS filter kullanılmadı", "filter:" not in css and "filter:" not in TM.TEMALAR["cini-toprak"]["css"] + TM.TEMALAR["gol-rasathane"]["css"])

D.sonuc()
