# 10. sınıf · Çözünme ve Çözünürlük · "Pamukkale–Afyon Yolu" (yerel tasarım · Yol 5)

Tema 2 · Bölüm 1 (Çözeltiler 1). 16 sayfalık, A4, baskıya hazır ünite: 6 durak + Hülasa + 3 yan yol + Büyük İmtihan (2 sayfa) +
Üstad soruları + Cevaplar + Final. Klasik kaynak (içerik ve cevaplar): `kitap/10-sinif/05-cozeltiler-1/kaynak.html`; buradaki
bütün sorular yeni bağlamla ve yeni sayılarla yeniden kuruldu. Tasarım sistemi: `kitap/yerel-ortak/TASARIM-SISTEMI.md`.

## Komutlar

```sh
cd kitap/10-sinif-yerel/05-cozeltiler-1
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh    # unite.html → PDF + onizleme/s01…s16.png + taşma özeti
node ../../yerel-ortak/render.js . --hepsi [--onizleme]                     # + öğretmen, fotokopi, baskı, hazine kartları PDF'leri
node ../../yerel-ortak/render.js . --pdfsiz 3 4                             # yalnız 3. ve 4. sayfanın PNG'si
```

`dogrula.py` 172 denetim yapar (bütün sayılar, tek doğru şık, grafik verisi ↔ soru, sayfadaki `data-dogru` işaretleri,
Cevaplar ızgarası ve çözüm satırları, meclis hükümleri, öğretmen metinleri, akçe ve HUD çubuğu) → `SONUÇ: hepsi doğru`.

## Dosyalar

| Dosya | Ne |
|---|---|
| `uretec/meta.json` | künye: 6 durak (yer, başlık, enlem–boylam, sayfa, akçe), kale, 8 nişan (Üstad Mührü bonus), H1–H12, 4 medeniyet, 11 kavram |
| `uretec/sablon.html` | 16 sayfanın içeriği; başta küçük üniteye özel CSS (`.dar` sıkı durak sayfaları, grafik yükseklikleri) |
| `uretec/kur.py` | sayfa künyesi (HUD, altbilgi, akçe çubuğu), `{{harita-etiket}}`, `{{final}}` (Afyon burcu), `{{nisan-sayim}}` (4 × 2) |
| `uretec/sahneler_unite.py` | bölge sahneleri ve parçaları (traverten basamakları, buhar, Afyon kalesi kayası, Afyon evi) + 6 nişan ikonu |
| `uretec/infografik_unite.py` | `VERI` (grafik verisi; dogrula.py da okur) + çözünme basamakları, sabun miseli, iletkenlik, çözünürlük/gaz/doygunluk/X/O₂/Na₂SO₄/A–B grafikleri, İbn Sînâ resmi |
| `uretec/dogrula.py` | sayısal doğrulama ve cevap anahtarı denetimi |

## Sayfa planı

| s. | Yer | İçerik | Sahne |
|---|---|---|---|
| 1 | Yola çıkış | dev başlık, Pamuk, Denizli–Afyon yol haritası (6 durak + kale), 8 nişan, yol arkadaşları, hedefler, Ahilik | `panorama_rota` |
| 2 | 1 · Pamukkale travertenleri | çözelti, çözücü/çözünen, üç basamak + enerji, Görev 1 (A/B), H1–H2, Tuzak (erime ≠ çözünme), tunç, **İbn Sînâ** | `pamukkale` (sabah; teraslar, turkuaz havuzda Pamuk) |
| 3 | 2 · Karahayıt (Kırmızı Su) | polar/apolar, etkileşim tablosu, sabun miseli, Görev 2, H3–H4, Tuzak (CH₄) | `karahayit` (öğle; kırmızı traverten, buhar) |
| 4 | 3 · Acıgöl | iyonik/moleküler, ampul testi, fiziksel/kimyasal, Görev 3 (iyon sayma), H5–H6, Tuzak (şekerli su) | `acigol` (ikindi; tuz havuzları) |
| 5 | 4 · Ömer–Gecek | çözünürlük, KNO₃–NaCl–Li₂SO₄ ve CO₂ grafikleri, Görev 4–5, Pamukkale’nin sırrı, H7–H8 | `omer_gecek` (sabah; kuyu başları, buhar) |
| 6 | 5 · Gazlıgöl | doymamış/doymuş/aşırı doymuş (A–B–C), hız ≠ çözünürlük, Görev 6 (şeker), H9–H10, bal, **Câbir** | `gazligol` (öğle; çeşme, şaşıran Elif) |
| 7 | 6 · Afyon çarşısı | 3 adım stratejisi, X eğrisi, Görev 7–9 (şerbet), H11–H12, Tuzak, kristallenme sıcaklığı | `afyon_carsi` (altın saat; kale, lokumcu) |
| 8 | Hülasa · Frig Vadisi | 6 özet kart, hazine sandığı (12), muhasebe | `frig_vadisi` (alacakaranlık, kamp) |
| 9 | Meclis · eski Afyon evi | 4 hatalı çözüm, **er-Râzî**, meclis notu | `konak` (pencerede kale) |
| 10 | Kıssalar · İscehisar | O₂ grafiği, ampul tablosu, gübre tesisi (KNO₃ + NaCl), cep ısıtıcısı | `mermer_ocagi` |
| 11 | Anahtar merdiveni · kale merdivenleri | 3 problem × 3 basamak | `kale_merdiven` |
| 12–13 | Afyonkarahisar Kalesi | Büyük İmtihan 1–12 + skor | `afyon_kalesi`, ortak `kale_kapi` |
| 14 | Üstad (bonus) | Na₂SO₄ grafiği, gaz T–P, iyon tablosu, buharlaştır + soğut, enerji, traverten dengesi | ortak `ustad_bandi` |
| 15 | Cevaplar | anahtar (durak etiketli), yan yol + Üstad anahtarı, bütün çözümler, **el-Bîrûnî** | `afyon_gece` |
| 16 | Final | akçe rayı (Çözelti Üstadı), unvanlar, akçe defteri, nişan sayımı, sıradaki yol | `afyon_final` (burçta bayraklı Pamuk) |

## Cevap anahtarı

- **Büyük İmtihan:** 1 B · 2 D · 3 C · 4 A · 5 E · 6 C · 7 A · 8 E · 9 D · 10 B · 11 C · 12 D
- **Kıssalar:** 1 C · 2 B · 3 E · 4 A
- **Üstad (bonus):** 1 E · 2 B · 3 C · 4 A · 5 D · 6 D
- **Meclis:** 1 Yusuf (satır 2; CCl₄ apolar → London) · 2 Pamuk (satır 3; hız ≠ çözünürlük) · 3 Elif (satır 2; 375 g çözelti → 75 g X) · 4 Yusuf (satır 1; 150 g su buharlaşır)
- **Anahtar merdiveni:** 1 → 100 g · 2 → 140 g su, 10 g tuz · 3 → 40 °C, 84 g
- **Akçe:** duraklar 100 + 5 × 120, Hülasa 40, Meclis 120, Kıssa 120, Anahtar 120, İmtihan 300 = **1400**

## Bölge bilgileri (yaklaşık; ayrıntı ve güven düzeyi ajan raporunda)

Pamukkale travertenleri CO₂ kaçınca çöken CaCO₃’tır (su ılık, yaklaşık 35 °C); Karahayıt Kırmızı Su yaklaşık 58 °C, demirli;
Acıgöl Türkiye’nin başlıca doğal sodyum sülfat kaynağı (buharlaştırma ve soğutmayla kristallendirme); Ömer–Gecek suyu yer yer
90 °C’u aşar, jeotermal ısıtmada kullanılır; Gazlıgöl suları Na⁺ ve HCO₃⁻ bakımından zengin; Afyonkarahisar Kalesi yaklaşık
226 m yükseklikte volkanik bir kaya üstündedir, kaleye yaklaşık 700 basamakla çıkılır.

## Bilinen notlar

- Hazine kesme yaprağında uzun rota adı nedeniyle render.js "hazine yaprağı taşma" uyarısı verir; görünüşte kesilme yoktur
  (ortak `hazine_yapragi.py` üst satırı kısaltabilir).
