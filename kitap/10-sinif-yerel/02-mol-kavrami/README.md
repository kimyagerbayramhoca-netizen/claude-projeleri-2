# 10. sınıf · Mol Kavramı · "Van Gölü Turu" (yerel tasarım)

14 sayfalık, A4, baskıya hazır ünite. Ana iskelet **B · Van Gölü** konsepti; "Medeniyetimizden" köşesi,
YANLIŞ/DOĞRU yıldız mühürleri ve tezhip köşebentleri **C · Medrese Defteri** konseptinden.
Bütün illüstrasyonlar (manzaralar, karakterler, 3B moleküller, süsler, bilgi grafikleri, ebru dokusu)
`uretec/cizim/` içindeki Python betikleriyle **koddan** üretilir. Tasarım sisteminin tamamı:
`../TASARIM-SISTEMI-YEREL.md`.

## Hızlı yeniden üretim

```sh
cd kitap/10-sinif-yerel/02-mol-kavrami
python3 uretec/kur.py        # uretec/sablon.html + çizimler → unite.html (gorsel/ebru-*.jpg yoksa onları da üretir)
python3 uretec/dogrula.py    # bütün sayılar, cevap anahtarı, tek doğru şık, akçe muhasebesi → "SONUÇ: hepsi doğru"
node uretec/render.js        # 02-mol-kavrami.pdf + onizleme/s01…s14.png (deviceScaleFactor 2) + taşma denetimi
```

Kısayollar:

| Komut | Ne yapar |
|---|---|
| `uretec/olc.sh` | `render.js`'i çalıştırıp taşma özetini verir; hedef çıktı `alan dışı … yok` |
| `node uretec/render.js 3 4` | yalnızca 3. ve 4. sayfanın PNG'si (PDF yine yazılır) |
| `node uretec/render.js --pdfsiz 3` | yalnızca PNG (hızlı deneme) |
| `python3 uretec/kur.py --ebru` | ebru dokularını da yeniden üretir |
| `python3 uretec/katalog.py` | `../katalog/*.png`: karakter, sahne, molekül, süs, infografik ve ebru katalogları |

Betikler göreli yollarla çalışır; hangi klasörden çağrıldıkları önemli değildir.

**Gerekenler:** Python 3 (numpy, Pillow; yalnız ebru için), Node + `playwright` (Chromium).
Yazı tipleri `kitap/fontlar/` klasöründen `@font-face` ile göreli yoldan yüklenir (Baloo Bhaijaan 2, Nunito, Amiri, Reem Kufi; yedek DejaVu).

## Klasör

```
02-mol-kavrami/
  README.md                bu dosya
  stil.css                 bileşen bazlı tasarım sistemi (tokenlar, sayfa çerçevesi, bütün bileşenler; yorumlu)
  unite.html               ÜRETİLİR: elle düzenleme, değişiklik kur.py'de kaybolur
  02-mol-kavrami.pdf       ÜRETİLİR (≈ 8,0 MB; bütün fontlar CID TrueType, Type 3 yok)
  onizleme/s01…s14.png     ÜRETİLİR
  gorsel/ebru-gol.jpg      ÜRETİLİR: göl paleti ebru (altbilgi şeridi, Medeniyetimizden üst şeridi)
  gorsel/ebru-gun.jpg      ÜRETİLİR: gün batımı paleti ebru (Hülasa zemini)
  uretec/
    sablon.html            14 sayfanın içeriği; illüstrasyonlar {{yer-tutucu}} ile çağrılır
    kur.py                 yer tutucuları çözer, HUD/altbilgi künyesini (SAYFA sözlüğü) yazar → unite.html
    render.js              PDF + PNG + taşma denetimi
    olc.sh                 taşma özeti
    dogrula.py             sayısal doğrulama (89 denetim)
    katalog.py, fotograf.js  tasarım sistemi kataloğu
    cizim/                 illüstrasyon kütüphanesi (temel, renkler, sahne, yapilar, karakter, molekul, sus, infografik, sahneler, ebru)
```

## Düzenleme akışı

1. Metin/soru değişikliği → `uretec/sablon.html`.
2. Sayı değiştiyse → `uretec/dogrula.py` içindeki ilgili satırı da güncelle; çalıştır.
3. Çizim değişikliği → ilgili `uretec/cizim/*.py` (ör. sahne `sahneler.py`, molekül `molekul.py`).
4. Görünüm → `stil.css` (bileşen başlıklarına bak).
5. `python3 uretec/kur.py && python3 uretec/dogrula.py && uretec/olc.sh` → taşma `yok` olmalı;
   sonra `onizleme/` PNG'lerine tek tek bak (taşma, üst üste binme, kesik yazı, bozuk alt simge).

## Sayfa planı

| s. | Durak / yer | İçerik | Sahne |
|---|---|---|---|
| 1 | Yola çıkış | dev başlık, Pamuk karşılama, Van Gölü panoraması üstünde tur rotası, nişanlar, yol arkadaşları, hedefler, Ahilik basamakları, işaretler | `panorama` |
| 2 | 1. durak · Edremit | Neden mol? · sohbet, desteler, kavram (H₂O), Avogadro log cetveli, Tuzak, H1, Kıyıdan, Hızlı görev | `edremit` (sabah, çay iskelesi, semaver) |
| 3 | 2. durak · Gevaş | Atomun kütlesi · izotop çekirdekleri, akb/bağıl/ortalama kütle, Görev 1 + bor madalyonları, H2–H3, Tuzak, Hızlı görev, **Medeniyetimizden: el-Bîrûnî** | `gevas` (Halime Hatun Kümbeti) |
| 4 | 3. durak · Tatvan | Mol ile tanecik · mol haritası (kütle köprüsü kilitli), Na₂CO₃ formül birimi, Görev 2–4 (kireç, soda, bal/glikoz), H4–H6, Tuzak (NaCl kristali), Hızlı görev | `tatvan` (Nemrut, feribot, obsidyen) |
| 5 | 4. durak · Ahlat | Mol ile kütle · mol kütlesi tablosu, H7–H8, mol haritası (açık), **Medeniyetimizden: el-Hâzinî terazisi**, Görev 5–6, 2 Tuzak, Hızlı görev | `ahlat` (Selçuklu mezar taşları) |
| 6 | 5. durak · Adilcevaz | Karışımlar · H9–H10, Görev 7 (karışım kapları), Görev 8 (eşit kütle terazisi), Hızlı görev, Tuzak, **Medeniyetimizden: Câbir bin Hayyân** | `adilcevaz` (Süphan, kıyı kalesi) |
| 7 | Hülasa · Süphan eteği | 6 özet kart (ebru zemin), hazine sandığı (H1–H10), Muhasebe (çay bardakları), kendime not | `suphan` (yayla, çadır, koyunlar) |
| 8 | Yan yol · Erciş | Meclis: 4 hatalı çözüm (Ahmet, Zehra, Mehmet Emin, Rabia), **Medeniyetimizden: er-Râzî**, meclis notu | `ercis` (köy odası) |
| 9 | Yan yol · Muradiye | 4 Kıssa (Van Gölü sodası, bor, grafik, kahvaltı sofrası rafı) | `muradiye` (şelale, asma köprü) |
| 10 | Yan yol · Van iskelesi | Anahtar merdiveni (3 problem × 3 basamak), akçe basamakları, yan yol toplamı | `iskele` |
| 11 | Van Kalesi 1/2 | Büyük İmtihan 1–6 (meşveret kartları) | `kale_buyuk` |
| 12 | Van Kalesi 2/2 | Büyük İmtihan 7–12, imtihan skoru | `kale_kapi` |
| 13 | Cevaplar | anahtar (durak etiketli), bütün çözümler, yan yol hızlı anahtarı, **Medeniyetimizden: Takiyüddin**, puan, tekrar rotası | `gece` |
| 14 | Final | kale burcunda bayraklı Pamuk + nişan çelengi, akçe rayı, unvanlar, akçe defteri, nişan sayımı, unvan kartım, sıradaki yol | `final` |

## Cevap anahtarı (dogrula.py ile denetlenir)

- **Büyük İmtihan:** 1 D · 2 C · 3 B · 4 E · 5 A · 6 C · 7 C · 8 D · 9 B · 10 E · 11 C · 12 D
- **Kıssalar:** 1 C · 2 B · 3 E · 4 D
- **Meclis:** 1 Yusuf (satır 2; 13 atom → 6,5 mol) · 2 Elif (satır 1; 44 g/mol → 0,25 mol) · 3 Yusuf (satır 2; 1 tanesi 180/N_A g) · 4 Pamuk (satır 2; CH₄ 1 mol, O₂ 0,5 mol)
- **Anahtar merdiveni:** 1 → 56 g/mol (Fe) · 2 → 2,4 mol H · 3 → 25/4
- **Akçe:** duraklar 100 + 4×150, Hülasa 40, Meclis 120, Kıssa 120, Anahtar 120, İmtihan 300 = **1400**
