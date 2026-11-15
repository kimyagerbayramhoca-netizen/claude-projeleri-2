# 10. sınıf · Mol Kavramı · "Van Gölü Turu" (yerel tasarım · referans ünite)

15 sayfalık, A4, baskıya hazır ünite; yerel tasarımın **referans uygulaması**. Ana iskelet **B · Van Gölü** konsepti;
"Medeniyetimizden" köşesi, YANLIŞ/DOĞRU yıldız mühürleri ve tezhip köşebentleri **C · Medrese Defteri** konseptinden.
Bütün illüstrasyonlar (manzaralar, karakterler, 3B moleküller, süsler, bilgi grafikleri, ebru dokusu) ortak kütüphane
`kitap/yerel-ortak/cizim/` ile **koddan** üretilir. Tasarım sistemi, kurucu, meta.json, cevap işaretleme ve varyantlar:
`kitap/yerel-ortak/TASARIM-SISTEMI.md`.

## Komutlar

```sh
cd kitap/10-sinif-yerel/02-mol-kavrami
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh   # unite.html → PDF + onizleme/s01…s15.png + taşma özeti
node ../../yerel-ortak/render.js . --hepsi                                 # + öğretmen, fotokopi, baskı, hazine kartları PDF'leri
```

| Komut | Ne yapar |
|---|---|
| `python3 uretec/kur.py` | `uretec/sablon.html` + `uretec/meta.json` + çizimler → `unite.html` (ebru dokuları yoksa onları da üretir) |
| `python3 uretec/kur.py --hepsi` | + `unite-fotokopi.html` ve `hazine-kartlari.html` (ara dosyalar) |
| `python3 uretec/dogrula.py` | 156 denetim: bütün sayılar, tek doğru şık, Üstad soruları, sayfadaki anahtar ve öğretmen işaretleri, akçe → `SONUÇ: hepsi doğru` |
| `bash uretec/olc.sh [sayfa…]` | render + taşma özeti; hedef `alan dışı … yok` |
| `node ../../yerel-ortak/render.js . --hepsi [--onizleme]` | beş PDF, fotokopi mürekkep raporu, Type 3 sayımı (+ `onizleme/varyant/` PNG'leri) |
| `node ../../yerel-ortak/render.js . --pdfsiz 3 4` | yalnız 3. ve 4. sayfanın PNG'si (hızlı deneme) |

Betikler göreli yollarla çalışır; hangi klasörden çağrıldıkları önemli değildir.
**Gerekenler:** Python 3 (numpy ve Pillow yalnız ebru için; pypdf baskı kutuları için), Node + `playwright` (Chromium), `pdffonts` (isteğe bağlı).

## Klasör

```
02-mol-kavrami/
  README.md                       bu dosya
  unite.html                      ÜRETİLİR (elle düzenleme; değişiklik kur.py'de kaybolur)
  02-mol-kavrami.pdf              ÜRETİLİR · öğrenci (≈ 8,4 MB)
  02-mol-kavrami-ogretmen.pdf     ÜRETİLİR · cevaplar kırmızı
  02-mol-kavrami-fotokopi.pdf     ÜRETİLİR · siyah-beyaz ana nüsha (ortalama mürekkep ≈ %10)
  02-mol-kavrami-baski.pdf        ÜRETİLİR · matbaa: 3,2 mm taşma, kesim izleri, TrimBox/BleedBox
  02-mol-kavrami-hazine-kartlari.pdf  ÜRETİLİR · H1–H10 kesme yaprağı
  onizleme/s01…s15.png            ÜRETİLİR (deviceScaleFactor 2) + hazine-kartlari.png + fotokopi-murekkep.json
  uretec/
    sablon.html                   15 sayfanın içeriği; çizimler {{yer-tutucu}} ile; öğretmen işaretleri (data-soru, data-dogru, .ogr)
    meta.json                     künye: duraklar, kale, nişanlar (Üstad Mührü dahil), H1–H10 hazine kartları, medeniyet, kavramlar
    kur.py                        ince kurucu: sayfa künyesi (SAYFA), HUD noktası (SIMDI), panorama etiketleri
    sahneler_unite.py             üniteye özel çizim: Üstad 5 grafiği (ustad_grafik)
    dogrula.py                    sayısal doğrulama (yerel-ortak/dogrula_ortak.py yardımcılarıyla)
    olc.sh                        taşma özeti
```

Van turu sahneleri (`edremit` … `gece`, `panorama`, `final`) ortak kütüphanededir: `yerel-ortak/cizim/sahneler.py`.

## Düzenleme akışı

1. Metin/soru → `uretec/sablon.html`. Hazine kartı, nişan, durak → `uretec/meta.json` (sayfa, Hülasa sandığı ve kesme yaprağı birlikte güncellenir).
2. Sayı değiştiyse → `uretec/dogrula.py` içindeki ilgili satırı da güncelle; doğru şık işaretini (`data-dogru`) ve kırmızı çözümü (`.ogr`) düzelt.
3. Sayfa künyesi (HUD yeri, altbilgi) → `uretec/kur.py`. Sayfa göndermesi → `s.{{sayfa|n}}`.
4. Ortak çizim ya da görünüm değişikliği gerekiyorsa → `yerel-ortak/` (ortak dosya; bütün üniteleri etkiler, yalnız eklemeyle).
5. `python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh` → sonra `onizleme/` PNG'lerine tek tek bak.

## Sayfa planı

| s. | Durak / yer | İçerik | Sahne |
|---|---|---|---|
| 1 | Yola çıkış | dev başlık, Pamuk karşılama, Van Gölü panoraması üstünde tur rotası, 7 nişan (Üstad Mührü dahil), yol arkadaşları, hedefler, Ahilik basamakları, işaretler | `panorama` |
| 2 | 1. durak · Edremit | Neden mol? · sohbet, desteler, kavram (H₂O), Avogadro log cetveli, Tuzak, H1, Kıyıdan, Hızlı görev | `edremit` |
| 3 | 2. durak · Gevaş | Atomun kütlesi · izotop çekirdekleri, akb/bağıl/ortalama kütle, Görev 1 + bor madalyonları, H2–H3, Tuzak, Hızlı görev, **Medeniyetimizden: el-Bîrûnî** | `gevas` |
| 4 | 3. durak · Tatvan | Mol ile tanecik · mol haritası, Na₂CO₃ formül birimi, Görev 2–4, H4–H6, Tuzak (NaCl kristali), Hızlı görev | `tatvan` |
| 5 | 4. durak · Ahlat | Mol ile kütle · mol kütlesi tablosu, H7–H8, mol haritası (açık), **Medeniyetimizden: el-Hâzinî**, Görev 5–6, 2 Tuzak, Hızlı görev | `ahlat` |
| 6 | 5. durak · Adilcevaz | Karışımlar · H9–H10, Görev 7–8, Hızlı görev, Tuzak, **Medeniyetimizden: Câbir bin Hayyân** | `adilcevaz` |
| 7 | Hülasa · Süphan eteği | 6 özet kart (ebru zemin), hazine sandığı (H1–H10, meta.json), Muhasebe, kendime not | `suphan` |
| 8 | Yan yol · Erciş | Meclis: 4 hatalı çözüm, **Medeniyetimizden: er-Râzî**, meclis notu | `ercis` |
| 9 | Yan yol · Muradiye | 4 Kıssa (Van Gölü sodası, bor, grafik, kahvaltı sofrası rafı) | `muradiye` |
| 10 | Yan yol · Van iskelesi | Anahtar merdiveni (3 × 3), akçe basamakları, yan yol toplamı | `iskele` |
| 11 | Van Kalesi 1/2 | Büyük İmtihan 1–6 | `kale_buyuk` |
| 12 | Van Kalesi 2/2 | Büyük İmtihan 7–12, imtihan skoru | `kale_kapi` |
| 13 | **Üstad soruları** (bonus) | 6 YKS/AYT tarzı soru (izotop, akb–gram, tablo, karışım, grafik, N_A kavramı); Üstad Mührü; akçeye dahil değil | `ustad_bandi` |
| 14 | Cevaplar | anahtar (durak etiketli) + yan yol/Üstad hızlı anahtarı, bütün çözümler (Üstad dahil), **Medeniyetimizden: Takiyüddin**, puan ve tekrar rotası | `gece` |
| 15 | Final | kale burcunda bayraklı Pamuk + 7 nişanlı çelenk, akçe rayı, unvanlar, akçe defteri, nişan sayımı, unvan kartım, sıradaki yol | `final` |

## Cevap anahtarı (dogrula.py ile ve sayfadaki işaretlerle denetlenir)

- **Büyük İmtihan:** 1 D · 2 C · 3 B · 4 E · 5 A · 6 C · 7 C · 8 D · 9 B · 10 E · 11 C · 12 D
- **Kıssalar:** 1 C · 2 B · 3 E · 4 D
- **Üstad (bonus):** 1 B · 2 E · 3 D · 4 C · 5 A · 6 D
- **Meclis:** 1 Yusuf (satır 2; 13 atom → 6,5 mol) · 2 Elif (satır 1; 44 g/mol → 0,25 mol) · 3 Yusuf (satır 2; 1 tanesi 180/N_A g) · 4 Pamuk (satır 2; CH₄ 1 mol, O₂ 0,5 mol)
- **Anahtar merdiveni:** 1 → 56 g/mol (Fe) · 2 → 2,4 mol H · 3 → 25/4
- **Akçe:** duraklar 100 + 4×150, Hülasa 40, Meclis 120, Kıssa 120, Anahtar 120, İmtihan 300 = **1400** (Üstad soruları akçesiz, bonus nişan)
