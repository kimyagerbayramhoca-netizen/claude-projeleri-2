# 10. sınıf · Kimyasal Değişimler · "Kars–Erzurum Yolu" (yerel tasarım · Yol 1)

Tema 1 · Bölüm 1. 16 sayfalık, A4, baskıya hazır ünite; 10. sınıf kitabının **açılış ünitesi**. Rota karlı Doğu Anadolu
kışında geçer: Çıldır Gölü → Kars → Ani → Sarıkamış → Pasinler → Erzurum; dönüşte Palandöken (Hülasa), Doğu Ekspresi,
Çobandede Köprüsü ve Kars Garı yan yolları, Kars Kalesi'nde Büyük İmtihan. Bütün çizimler koddan üretilir: ortak kütüphane
`kitap/yerel-ortak/cizim/` + bu ünitenin `uretec/` modülleri. Tasarım sistemi: `kitap/yerel-ortak/TASARIM-SISTEMI.md`.
Klasik kaynak: `kitap/10-sinif/01-kimyasal-degisimler/kaynak.html` (içerik yeniden yazıldı, her denklem yeniden denkleştirildi).

## Komutlar

```sh
cd kitap/10-sinif-yerel/01-kimyasal-degisimler
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh   # unite.html → PDF + onizleme/s01…s16.png + taşma özeti
node ../../yerel-ortak/render.js . --hepsi [--onizleme]                    # beş PDF (öğrenci, öğretmen, fotokopi, baskı, hazine kartları)
node ../../yerel-ortak/render.js . --pdfsiz 3 4                            # yalnız 3. ve 4. sayfanın PNG'si (hızlı deneme)
```

`dogrula.py` 218 denetim yapar ve `SONUÇ: hepsi doğru` ile biter: her denklemin atom denkliği ve sadeliği, bütün sayısal
cevaplar, küçük bir YB çözücüsüyle redoks/yükseltgenme basamakları, çözünürlük kuralıyla çökelek, her soruda tek doğru şık,
sayfadan okunan şık metinleri, `data-dogru` işaretleri, meclis hükümleri, anahtar ızgarası, çözüm sayfasındaki harfler,
öğretmen (`.ogr`) metinleri, akçe (durak 100 + 5 × 120, yan yollar 3 × 120, imtihan 300, Hülasa 40 → 1400), HUD çubukları,
Ahilik eşikleri ve `s.{{sayfa|n}}` göndermelerinin doğru sayfaya gittiği.

## Klasör

```
01-kimyasal-degisimler/
  README.md                        bu dosya
  unite.html                       ÜRETİLİR (elle düzenleme)
  01-kimyasal-degisimler.pdf       ÜRETİLİR · öğrenci (≈ 9,5 MB)
  …-ogretmen.pdf / …-fotokopi.pdf / …-baski.pdf / …-hazine-kartlari.pdf   ÜRETİLİR (render.js --hepsi)
  onizleme/s01…s16.png             ÜRETİLİR
  uretec/
    sablon.html                    16 sayfanın içeriği + üniteye özel küçük CSS (<style> başta)
    meta.json                      duraklar, kale, 8 nişan (Üstad Mührü bonus), H1–H12, medeniyet, kavramlar, "hud"
    kur.py                         SAYFA (HUD/altbilgi/akçe çubuğu), SIMDI, panorama etiketleri, final, mühür alt yazısı;
                                   ortak hazine rozeti ve kesme yaprağı için iki küçük yerel düzeltme (aşağıda)
    sahneler_unite.py              bütün sahneler (cildir … final_kars, panorama_kars) + NISAN_IKON (6 yerel nişan simgesi)
    infografik_unite.py            tepkime bilgi grafikleri (tanecik modelleri, çökelme, redoks, asit-baz, kireç döngüsü…)
    kars_parcalar.py               yerel çizim parçaları (karlı çam, buz göl, atlı kızak, Ani surları, kireç ocağı, soba,
                                   CO dedektörü, tren, kaplıca, Taşhan, taş köprü, bazalt kale…)
    dogrula.py                     sayısal doğrulama
    olc.sh                         taşma özeti
```

## Sayfa planı

| s. | Yer | İçerik | Sahne / grafik |
|---|---|---|---|
| 1 | Yola çıkış | başlık, Pamuk karşılama, tur haritası (11 etiket), 8 nişan, yol arkadaşları, hedefler, Ahilik basamakları, işaretler | `panorama_kars` |
| 2 | 1. durak · Çıldır Gölü | Ne değişti? fiziksel/kimyasal · kavram (+20), göstergeler + tanecik modeli, Görev 1, H1–H2, Tuzak (gaz çıkışı), Hızlı, **İbn Sînâ** | `cildir`; `gostergeler`, `tanecik_iki_olay` |
| 3 | 2. durak · Kars (mandıra) | Tepkime denklemi · laktoz → laktik asit, korunanlar + CH₄ modeli, Görev 2–3, H3–H4, Tuzak (molekül sayısı), Hızlı (propan), Yoldan (Kars kaşarı, gravyer) | `kars_mandira`; `korunum_model` |
| 4 | 3. durak · Ani | Asit ve baz · Arrhenius, nötralleşme, oksitler, Görev 4–5, H5–H6, Tuzak (OH'li alkol), Hızlı, **er-Râzî** | `ani` (yıkık surlar, kireç ocağı); `asit_baz_model` |
| 5 | 4. durak · Sarıkamış | Yanma, sentez, analiz · tam/eksik yanma ve CO güvenliği, Görev 6–7, sentez/analiz + kireç döngüsü, H7–H8, Tuzak, Hızlı | `sarikamis` (sobalı oda); `yanma_co`, `kirec_dongusu` |
| 6 | 5. durak · Pasinler | Çökelme · çözünürlük kuralları, net iyon/seyirci, Görev 8–9, H9–H10, Tuzak, Hızlı (BaSO₄), **Câbir bin Hayyân** | `pasinler` (Hasankale, kaplıca); `cokelme_model` |
| 7 | 6. durak · Erzurum | Redoks · YB kuralları, Fe/CuSO₄ modeli, metal tepkimeleri + aktiflik, Görev 10–11, H11–H12, Tuzak, Hızlı, **Erzurumlu İbrahim Hakkı** | `erzurum` (Taşhan); `redoks_model` |
| 8 | Hülasa · Palandöken | 6 özet kart, hazine sandığı (12), Muhasebe (+40), kendime not | `palandoken` |
| 9 | Yan yol · Doğu Ekspresi | Meclis M1–M4, meclis notu, Yoldan (tren, çay) | `tren_ici` |
| 10 | Yan yol · Çobandede | Kıssa 1–4 (kül suyu, termit, iletkenlik grafiği, bakır geri kazanımı) | `cobandede`; `kul_resmi`, `termit_resmi`, `iletkenlik_grafigi` |
| 11 | Yan yol · Kars Garı | Anahtar merdiveni (3 × 3 basamak), akçe basamakları, yan yol toplamı | `kars_gari` |
| 12 | Kars Kalesi 1/2 | Büyük İmtihan 1–6 (meşveret) | `kars_kalesi`; `model_soru` |
| 13 | Kars Kalesi 2/2 | Büyük İmtihan 7–12, skor | `kale_kapi_bazalt` |
| 14 | Üstad (bonus) | 6 AYT tarzı soru, Üstad Mührü | `ustad_bandi` (ortak); `kutle_grafigi` |
| 15 | Cevaplar | durak etiketli anahtar, bütün çözümler, hızlı anahtar, puan, tekrar rotası | `kars_gece` |
| 16 | Final | Kars Kalesi burcunda bayraklı Pamuk + 8 nişanlı çelenk, akçe rayı, unvanlar, defter, nişan sayımı, sıradaki yol | `final_kars` |

## Cevap anahtarı

* **Büyük İmtihan:** 1 C · 2 D · 3 A · 4 C · 5 E · 6 B · 7 D · 8 A · 9 E · 10 C · 11 D · 12 B (A2 B2 C3 D3 E2)
* **Kıssalar:** 1 C · 2 D · 3 E · 4 B — **Üstad:** 1 B · 2 A · 3 C · 4 D · 5 B · 6 E
* **Meclis:** M1 Yusuf (satır 3) · M2 Elif (3) · M3 Yusuf (2) · M4 Pamuk (2)
* **Anahtar merdiveni:** 22,4 g CaO kalır, 0,4 mol CO₂ · 0,1 mol e⁻, 10,8 g Ag · 28,7 g AgCl; kalan 0,1 Ag⁺, 0,3 NO₃⁻, 0,1 Ca²⁺
* **Hızlı görevler:** 2 · 13 · CO₂ ve SO₂ · 0,2 mol CO · BaSO₄ · 1,2 mol e⁻
* **Görevler:** G1 (b), (c) · G2 x = 4 · G3 4 g O₂ · G4 Ca(OH)₂ + 2HCl, KOH + HNO₃ · G5 0,2 mol HCl · G6 2C₄H₁₀ + 13O₂ → 8CO₂ + 10H₂O · G7 (b) · G8 seyirci Na⁺, NO₃⁻ · G9 5 g · G10 Fe +3, Cr +6 · G11 0,2 mol e⁻, 6,4 g Cu

## Akçe

Duraklar 100 + 120 × 5 = 700 · Hülasa 40 · Meclis 4 × 30 · Kıssa 4 × 30 · Anahtar 3 × 40 · İmtihan 12 × 25 = 300 → **1400**.
Ahilik: Çırak 0+, Kalfa 400+, Usta 800+, Tepkime Üstadı 1150+. Üstad soruları akçeye eklenmez (Üstad Mührü).

## Bölge bilgileri (kaynakla doğrulandı; yaklaşık değerler "yaklaşık" diye yazıldı)

| Bilgi | Kullanıldığı yer | Güven |
|---|---|---|
| Çıldır Gölü ≈ 1959 m, kışın buz tutar; atlı kızak, buzu delip balık avı | s.2 | yüksek |
| Kars kaşarı coğrafi işaretli; telemesi haşlanıp yoğrulur, aylarca olgunlaşır; gravyer delikleri propiyonik asit bakterilerinin CO₂'si | s.3 | yüksek |
| Ani: 1064 Alparslan fethi; tüf taşı surlar; bölgenin tüf, kireç ve volkanik külü yapı malzemesi; surlar bugün yer yer yıkık çizildi | s.4 | yüksek |
| Sarıkamış sarıçam ormanları; Doğu Ekspresi Ankara–Kars, Erzurum ve Sarıkamış'tan geçer, bir günden uzun | s.5, s.9 | yüksek |
| CO renksiz, kokusuz; hemoglobine O₂'den yaklaşık 200–250 kat sıkı bağlanır; baca, dedektör, havalandırma, 112 | s.5 | yüksek (sakin, eğitici dil) |
| Pasinler'in eski adı Hasankale; kaplıca suyu yaklaşık 40 °C (kaynaklarda 39–45 °C); Hasankale kalesi yıkık sur olarak çizildi | s.6 | orta-yüksek |
| Taşhan (16. yy) bugün Oltu taşı çarşısı; Oltu taşı çelik bıçakla kesilip parlatılır | s.7 | yüksek |
| Erzurumlu İbrahim Hakkı 1703–1780, Hasankale doğumlu; Marifetnâme 1757, madde dört unsurla açıklanır | s.7 | yüksek (ölüm yılı için kaynaklarda 1780 yaygın) |
| İbn Sînâ 980–1037, Kitâbü'ş-Şifâ: metalin türü değiştirilemez, ancak boyanıp benzetilebilir | s.2 | yüksek |
| er-Râzî 865–925, maddeleri sınıflandırdı (tuzlar bir sınıf), araçları tarif etti; Câbir 8. yy, damıtma/kristallendirme/süzme | s.4, s.6 | yüksek |
| Kars Kalesi bazalt; Çobandede Köprüsü Aras üzerinde, taş kemerli (13. yy sonu) | s.10, s.12, s.16 | yüksek |

## Yerel düzeltmeler (ortak kütüphaneye öneri)

* `kur.py` · `_rozet_duzelt`: ortak hazine rozeti yazı boyunu sabit 30 tutuyor; üç haneli kodlar (H10–H12) daireden taşıyordu → 23.
* `kur.py` · kesme yaprağı: rota adı üst satıra sığmıyor ("Kars–Erzurum Yolu" → "Kars–Erzurum") ve iki satırlı formüllü kartlar
  1,3 büyütmeyle hücreden taşıyordu → bu ünitede `.hy-kart { zoom: 1.06 }`.
* `sablon.html` başındaki `<style>`: `ul.yargi.iki` (iki sütunlu yargı), `.s14 .ustad-izgara` (satırlar içeriğe göre),
  `.s12/.s13 .mesveret .karalama` (min 8 mm), küçük bilgi kartı düzenleri.
