# 10. sınıf · Stokiyometri · "Dicle Yolu" (Yol 3 · yerel tasarım)

16 sayfalık, A4, baskıya hazır ünite (Tema 1 · Bölüm 3). Rota: Ergani'den (Çayönü) Dicle'ye inip Diyarbakır, Malabadi,
Batman ve Hasankeyf'e uzanır, Diyarbakır Surları'nda biter. Bütün çizimler (manzaralar, karakterler, 3B moleküller,
bilgi grafikleri) ortak kütüphane `kitap/yerel-ortak/cizim/` ve üniteye özel `uretec/sahneler_unite.py` ile **koddan**
üretilir. Tasarım sistemi, kurucu, meta.json, cevap işaretleme ve varyantlar: `kitap/yerel-ortak/TASARIM-SISTEMI.md`.

## Komutlar

```sh
cd kitap/10-sinif-yerel/03-stokiyometri
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh   # unite.html → PDF + onizleme/s01…s16.png + taşma özeti
node ../../yerel-ortak/render.js . --hepsi --onizleme                      # beş PDF + onizleme/varyant/ PNG'leri
```

| Komut | Ne yapar |
|---|---|
| `python3 uretec/kur.py` | `uretec/sablon.html` + `uretec/meta.json` + çizimler → `unite.html` |
| `python3 uretec/kur.py --hepsi` | + `unite-fotokopi.html` ve `hazine-kartlari.html` (ara dosyalar) |
| `python3 uretec/dogrula.py` | 354 denetim (aşağıda) → `SONUÇ: hepsi doğru` |
| `bash uretec/olc.sh [sayfa…]` | render + taşma özeti; hedef `alan dışı … yok` |
| `node ../../yerel-ortak/render.js . --hepsi [--onizleme]` | öğrenci, öğretmen, fotokopi, baskı, hazine kartları PDF'leri; mürekkep raporu; Type 3 sayımı |
| `node ../../yerel-ortak/render.js . --pdfsiz 3 4` | yalnız 3. ve 4. sayfanın PNG'si (hızlı deneme) |

## Klasör

```
03-stokiyometri/
  README.md                          bu dosya
  unite.html                         ÜRETİLİR (elle düzenleme)
  03-stokiyometri.pdf                ÜRETİLİR · öğrenci (≈ 6,5 MB)
  03-stokiyometri-ogretmen.pdf       ÜRETİLİR · 30 doğru işareti, 45 kırmızı cevap
  03-stokiyometri-fotokopi.pdf       ÜRETİLİR · siyah-beyaz (ortalama mürekkep ≈ %10)
  03-stokiyometri-baski.pdf          ÜRETİLİR · 3,2 mm taşma, TrimBox/BleedBox
  03-stokiyometri-hazine-kartlari.pdf  ÜRETİLİR · H1–H12 kesme yaprağı
  onizleme/                          ÜRETİLİR · s01…s16.png, hazine-kartlari.png, varyant/
  uretec/
    sablon.html                      16 sayfanın içeriği + üniteye özel küçük CSS; öğretmen işaretleri (data-soru, data-dogru, .ogr)
    meta.json                        künye (TEK DOĞRULUK KAYNAĞI): 6 durak, kale, 8 nişan, H1–H12, medeniyet, kavramlar, 1400 akçe
    kur.py                           SAYFA (HUD + altbilgi + akçe çubuğu), SIMDI, yerel yer tutucular: {{dicle-etiket}} {{muhur}} {{mol}} {{final}}
    sahneler_unite.py                bantlar, panorama, final, bilgi grafikleri, nişan ikonları; grafik verileri MOL_ZAMAN, USTAD_GRAFIK
    dogrula.py                       yeniden hesap + sayfa denetimi (yerel-ortak/dogrula_ortak.py ile)
    olc.sh                           taşma özeti
```

## Düzenleme akışı

1. Metin/soru → `uretec/sablon.html`; hazine kartı, nişan, durak, medeniyet → `uretec/meta.json`.
2. Sayı değiştiyse `uretec/dogrula.py`'deki hesabı güncelle; `data-dogru` ve `.ogr` metnini düzelt. Grafik verisi
   `sahneler_unite.py`'deki `MOL_ZAMAN` / `USTAD_GRAFIK` sözlüklerindedir; çizim ve doğrulama aynı sayıyı okur.
3. Sayfa künyesi → `uretec/kur.py`; sayfa göndermesi → `s.{{sayfa|n}}`.
4. `python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh`, sonra `onizleme/` PNG'lerine tek tek bak.

## Sayfa planı

| s. | Yer (HUD) | İçerik | Sahne (`sahneler_unite.py`) |
|---|---|---|---|
| 1 | Yola çıkış | kapak, yol haritası (6 durak + Hülasa + 3 yan yol + kale), nişanlar, karakterler, hedefler, Ahilik basamakları | `panorama_dicle` + `{{dicle-etiket}}` |
| 2 | 1. durak · Çayönü | tepkime denklemi, kütlenin korunumu; H1–H2; Görev 1; Medeniyet: İbn Sînâ | `cayonu` (kazı alanı, sabah) |
| 3 | 2. durak · Hevsel | denkleştirme (tam sayılı, kesirli, formülü bilinmeyen); H3–H4; Görev 2–3 | `hevsel` (bazalt sur + bahçeler, öğle) |
| 4 | 3. durak · Malabadi | denklemden hesaba; H5–H6; Görev 4–5; Medeniyet: el-Cezerî | `malabadi` (sivri kemer, ikindi) |
| 5 | 4. durak · Batman | grafik okuma, sınırlayıcı bileşen, B–D–S; H7–H8; Görev 6–7 | `batman` (Raman eteği, rafineri) |
| 6 | 5. durak · Hasankeyf | yüzde verim, saflık; H9–H10; Görev 8–9; Medeniyet: el-Hâzinî | `hasankeyf` (kalker yamaç, baraj gölü) |
| 7 | 6. durak · Bakırcılar | karışım ve ardışık tepkimeler; H11–H12; Görev 10–11 | `bakircilar` (alaca kemer, bakır kaplar) |
| 8 | Hülasa · Hasan Paşa Hanı | 6 özet kartı, hazine sandığı, muhasebe (+40) | `han_hulasa` |
| 9 | Yan yol 1 · Dicle kıyısı | Meclis (4 çözüm, tek hata); Medeniyet: Câbir bin Hayyân | `karpuz_meclis` (bostan çardağı) |
| 10 | Yan yol 2 · On Gözlü Köprü | 4 Kıssa (sağlık, tarım, laboratuvar, mutfak) | `on_gozlu` |
| 11 | Yan yol 3 · Surların eteği | Anahtar merdiveni (3 problem, 3 basamak) | `sur_etegi` (gün batımı) |
| 12–13 | Diyarbakır Surları | Büyük İmtihan 12 soru, meşveret | `kale_sur`, `sur_kapisi` |
| 14 | Üstad · bonus | 6 AYT tarzı soru, Üstad Mührü | ortak `ustad_bandi` |
| 15 | Cevaplar | anahtar ızgarası (durak etiketli), bütün çözümler, kısa anahtar, yanlış defteri, tekrar rotası | `gece_dicle` |
| 16 | Final | akçe rayı, unvanlar, akçe defteri, nişan sayımı, unvan kartı | `final_dicle` |

Bilgi grafikleri: `korunum_semasi`, `iki_yaka`, `oran_koprusu`, `mol_zaman` (durak/kıssa), `sinirlayici_tanecik`, `verim_saati`,
`saflik_tasi`, `lpg_tupu`, `bakir_zinciri`, `mg_denemeleri`, `ustad_grafik`, `cezeri_duzenek` (temsilî), `hazini_kart`, `imbik`.

## Cevap anahtarı (dogrula.py ile ve sayfadaki işaretlerle denetlenir)

| Bölüm | Anahtar |
|---|---|
| Büyük İmtihan 1–12 | A B E A C D B E C D B D (A 2 · B 3 · C 2 · D 3 · E 2) |
| Kıssalar 1–4 | E D C B |
| Üstad 1–6 | E B D C A D |
| Meclis | M1 Yusuf, satır 2 · M2 Pamuk, satır 1 · M3 Yusuf, satır 2 · M4 Elif, satır 3 |
| Anahtar merdiveni | 1 → 23 · 2 → 1,6 g S artar, 16 g Cu₂S · 3 → 16 g CaCO₃ |
| Hızlı görevler | 1 → 36 g, hayır · 2 → 9 · 3 → 22 g · 4 → O₂, 0,9 mol · 5 → 50 g · 6 → %32,5 |

Akçe: duraklar 100 + 5 × 120, Hülasa 40, Meclis 120, Kıssa 120, Merdiven 120, İmtihan 12 × 25 = **1400**
(Çırak 0–399 · Kalfa 400–799 · Usta 800–1149 · Oran Üstadı 1150–1400). Üstad soruları akçeye eklenmez.

`dogrula.py` neyi denetler: açık listedeki 31 denklem ve **sayfadan toplanan bütün denklemler** (denk mi, en küçük tam sayı mı;
kasıtlı denk olmayan 4 soru/meclis satırı ayrı); bütün görev, tuzak, hızlı görev, meclis, kıssa, merdiven, imtihan ve üstad
sonuçlarının yeniden hesabı ve sayfadaki metinle eşleşmesi; şıkları **sayfadan okuyarak** tek doğru şık; `data-dogru`
işaretleri, anahtar ızgarası, Cevaplar satırları, meclis hükümleri, öğretmen metinleri; çip + hazine kartlarından durak
akçeleri, akçe defteri, HUD çubuğu yüzdeleri, unvan sınırları; meta.json tutarlılığı (nişanlar, kartlar, medeniyet sayfaları).

## Yerel bilgiler (kaynak: web taraması; yaklaşık olanlar sayfada "yaklaşık"/temsilî)

- Çayönü (Ergani): malakit ve bakır boncuklar; bakırın işlendiği en eski yerlerden biri.
- Hevsel Bahçeleri: surlarla Dicle arasında; 2015'te Diyarbakır Kalesi ile birlikte UNESCO Dünya Mirası Listesi.
- Malabadi Köprüsü: Artuklu, 1147. el-Cezerî Âmid'de Artuklu sarayında 25 yılı aşkın çalıştı; kitabını 1206'da bitirdi.
- Batman: Raman Dağı'nda petrol 1940; Batman Rafinerisi 1955.
- Hasankeyf: kireç taşı ve dolomit yamaçlar, oyma mağaralar; Ilısu Barajı suları 2020'de eski yerleşimin büyük bölümünü kapladı;
  Zeynel Bey Türbesi ve başka bazı yapılar Kültür Parkı'na taşındı. (Kale/köprü kalıntıları "sağlam" çizilmedi.)
- Diyarbakır Bakırcılar Çarşısı, Hasan Paşa Hanı, On Gözlü Köprü, Diyarbakır Surları.
- Medeniyetimizden: İbn Sînâ (Kitâbü'ş-Şifâ, madenlerin dönüşmezliği), el-Cezerî, el-Hâzinî (Mîzânü'l-Hikme, alaşım terazisi),
  Câbir bin Hayyân (damıtma, kristallendirme, süzme).
