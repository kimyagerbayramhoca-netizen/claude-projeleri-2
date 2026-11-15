# 10. sınıf · Gazlar · Yol 4 Kapadokya Yolu (yerel tasarım)

Tema 1 · Bölüm 4. Kaynak (doğrulanmış içerik): `../../10-sinif/04-gazlar/kaynak.html`. Referans ünite: `../02-mol-kavrami`.
Tasarım sistemi: `../../yerel-ortak/TASARIM-SISTEMI.md` · rotalar: `../../yerel-ortak/ROTALAR.md` · dil ve karakterler:
`kitap/YEREL-KIMLIK.md` · sayılar: `kitap/YAZIM-REHBERI.md`. Sabitler: R = 0,082 L·atm/(mol·K), NŞA'da 22,4 L/mol, T(K) = t(°C) + 273.

## Komutlar

```sh
cd kitap/10-sinif-yerel/04-gazlar
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh    # unite.html → PDF + onizleme/sNN.png + taşma özeti
node ../../yerel-ortak/render.js . 3 4 --pdfsiz                               # yalnız değişen sayfaların PNG'si
node ../../yerel-ortak/render.js . --hepsi                                    # öğrenci, öğretmen, fotokopi, baskı, hazine kartları PDF'leri
for f in *.pdf; do pdffonts "$f" | grep -c "Type 3"; done                     # hepsi 0 olmalı
```

`dogrula.py` sonu `SONUÇ: hepsi doğru` (188 denetim); `render.js` çıktısı `Taşma yok` ve `öğretmen: … taşma yok` olmalı.

## Dosyalar

| Dosya | Ne |
|---|---|
| `uretec/meta.json` | tek doğruluk kaynağı: 5 durak (yer, başlık, enlem–boylam, sayfa, akçe), kale, 7 nişan, 12 hazine kartı, medeniyet, kavramlar |
| `uretec/sablon.html` | 15 sayfanın içeriği + `{{yer-tutucular}}`; başta küçük üniteye özel CSS |
| `uretec/kur.py` | sayfa künyesi (HUD, altbilgi, akçe çubuğu), panorama etiketlerinin çakışmasız yerleşimi (geri izlemeli), mühür alt yazısı, final |
| `uretec/sahneler_unite.py` | Kapadokya sahneleri ve çizim parçaları: sıcak hava balonu, peri bacası kümesi, tüf sırtı, Uçhisar kaya kalesi, testi/küp/kase, fırın, güvercinlik yüzü, taş evler, bağ sıraları; 5 nişan ikonu |
| `uretec/infografik_unite.py` | gaz bilgi grafikleri: tanecik kutuları, barometreler (deniz kıyısı · Kayseri · Erciyes), manometre, Boyle/Charles/Gay-Lussac grafikleri, paket, testiler, balon kesiti, yoğunluk cetveli, NH₃–HCl borusu, kıssa P–T, imtihan V–t, Üstad V–T, tüf merdiven, darüşşifa portali, buhar çarkı |
| `uretec/dogrula.py` | bütün sayıları yeniden hesaplar; tek doğru şık; sayfadaki işaretler, şık metinleri, anahtar ızgarası, akçe toplamları, Cevaplar satırları |
| `unite.html`, `unite-fotokopi.html`, `hazine-kartlari.html`, `*.pdf`, `onizleme/` | ÜRETİLİR |

## Sayfa planı (15 sayfa · 1400 akçe)

| s. | Sayfa | Sahne (`sahneler_unite`) | Akçe |
|---|---|---|---|
| 1 | Yola çıkış · Kapadokya tur haritası, nişanlar, yol arkadaşları, hedefler | `kapadokya_panorama` (kuzeyden güneye stilize harita; Erciyes, Hasan Dağı, Kızılırmak, balonlar) | – |
| 2 | 1. durak · **Erciyes** · gaz hâli, basınç, barometre, manometre · Medeniyetimizden: Gevher Nesibe Darüşşifası | `erciyes` (karlı Erciyes, kümbet, bağlar) | 100 |
| 3 | 2. durak · **Göreme** · Boyle ve Charles · Yoldan: neden şafakta? | `goreme` (şafakta balonlar, peri bacaları) | 150 |
| 4 | 3. durak · **Avanos** · Gay-Lussac, Avogadro, birleşik denklem · Medeniyetimizden: Takiyüddin | `avanos` (çömlekçi fırını, testiler, Kızılırmak kıyısı) | 150 |
| 5 | 4. durak · **Kızılçukur** · kinetik teori, PV = nRT | `kizilcukur` (balon sepeti, brülör alevi, pembe sırtlar) | 150 |
| 6 | 5. durak · **Derinkuyu** · gaz yoğunluğu, difüzyon/efüzyon, Graham · Yoldan: Derinkuyu | `derinkuyu` (yeraltı katları, havalandırma bacası, taş kapı) | 150 |
| 7 | Hülasa · 6 özet kart, hazine sandığı (12 kart), muhasebe | `hasan` (Hasan Dağı eteğinde konaklama) | 40 |
| 8 | Yan yol 1 · **Güzelyurt** · Meclis: kim haklı? (4 hatalı çözüm) · Medeniyetimizden: İbn Sînâ | `guzelyurt` (taş evler) | 120 |
| 9 | Yan yol 2 · **Ihlara** · Kıssalar (4) | `ihlara` (kanyon, Melendiz) | 120 |
| 10 | Yan yol 3 · **Güvercinlik Vadisi** · Anahtar merdiveni (3 × 3 basamak) | `guvercinlik` (güvercinlikli kaya yüzü) | 120 |
| 11 | **Uçhisar Kalesi** · Büyük İmtihan 1–6 | `uchisar_buyuk` (kaya kalesi) | 150 |
| 12 | Büyük İmtihan 7–12 + skor | `uchisar_kapi` (kale kapısı, kilim şeridi) | 150 |
| 13 | Üstad soruları (6, YKS/AYT, bonus) | `ustad_bandi` (ortak) | bonus |
| 14 | Cevaplar ve çözümler | `kapadokya_gece` | – |
| 15 | Final · akçe rayı, unvanlar (Çırak 0+, Kalfa 400+, Usta 800+, Gaz Üstadı 1150+), nişan çelengi | `final_kapadokya` (balon, Uçhisar, Pamuk bayrakla) | – |

Akçe çubuğu (HUD) %: 0 · 0 · 7 · 18 · 29 · 39 · 50 · 53 · 61 · 70 · 79 · 89 · 100 · 100 · 100 (`dogrula.py` denetler).

## Cevap anahtarları

- **Büyük İmtihan:** 1 B · 2 E · 3 C · 4 D · 5 D · 6 A · 7 C · 8 E · 9 A · 10 D · 11 B · 12 C (A 2, B 2, C 3, D 3, E 2)
- **Kıssalar:** 1 C · 2 D · 3 E · 4 B
- **Üstad:** 1 B · 2 D · 3 B · 4 E · 5 A · 6 C
- **Meclis (haklı · hatalı satır):** 1 Yusuf · 1 — 2 Elif · 1 — 3 Yusuf · 2 — 4 Pamuk · 2
- **Anahtar merdiveni:** 1) 8 L · 2) C₃H₆ · 3) 32 g/mol (O₂)
- **Hızlı görevler:** s.2 0,75 atm · s.3 3 L · s.4 14 g, 3,01·10²³ · s.5 4 L · s.6 64 g/mol (SO₂)

## Bölge ve tarih bilgileri (güven)

| Bilgi | Kullanım | Güven |
|---|---|---|
| Erciyes ≈ 3917 m; zirvede P ≈ 0,62 atm (≈ 47 cmHg), Kayseri ≈ 1050 m'de ≈ 0,88 atm (≈ 67 cmHg) | s.2 barometreler, görevler | yükseklik yüksek; basınçlar standart atmosfer hesabı ("≈") |
| Gevher Nesibe Darüşşifası, Kayseri, 1205–1206; I. Gıyaseddin Keyhüsrev kız kardeşi Gevher Nesibe Sultan adına; darüşşifa + tıp medresesi | s.2 Medeniyetimizden | yüksek |
| Göreme'de balon uçuşları çoğunlukla gün doğumunda; rüzgâr sınırı aşınca izin verilmez | s.3 Yoldan | yüksek (genel ifade) |
| Avanos çömlekçiliği, Kızılırmak kili | s.4 sahne | yüksek |
| Takiyüddin, et-Turuku's-Seniyye (1551): buharla dönen kebap şişi | s.4 Medeniyetimizden | yüksek |
| Derinkuyu Yeraltı Şehri: tüfe oyulmuş, ≈ 85 m derinlik, havalandırma bacaları, yuvarlak taş kapılar | s.6 Yoldan, sahne | yüksek ("yaklaşık") |
| İbn Sînâ (980–1037), el-Kânûn fi't-Tıb: sağlığı koruyan altı etkenin ilki hava | s.8 Medeniyetimizden | yüksek |
| Uçhisar Kalesi (kaya kalesi), Ihlara Vadisi ve Melendiz Çayı, Güzelyurt taş evleri, Güvercinlik Vadisi | sahneler | yüksek; çizimler temsilîdir |

Cami, kilise ve manastırlar oyun durağı yapılmadı; logo yok; çizimler temsilî.
