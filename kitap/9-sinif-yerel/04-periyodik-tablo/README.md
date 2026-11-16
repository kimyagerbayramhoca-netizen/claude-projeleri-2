# 9. sınıf · Periyodik Tablo · Yol 4 "Maden Yolu I · Batı Anadolu" (yerel tasarım)

Tema 1 · Bölüm 4. 15 sayfalık, A4, baskıya hazır ünite. Rota Batı Anadolu'nun madenlerinden geçer: Seydişehir (alüminyum) →
Kütahya çini atölyesi (kobalt, bakır) → Gümüşköy (gümüş) → Kırka (bor) → Bandırma (bor işleme, liman); dönüşte Kuşcenneti
(Hülasa), Bigadiç, Emet ve Germiyan Sokağı yan yolları, Kütahya Kalesi'nde Büyük İmtihan. Klasik kaynak:
`kitap/9-sinif/04-periyodik-tablo/kaynak.html` (konu sırası korundu, metin ve sorular yeni bağlamla yeniden yazıldı).
Tasarım sistemi: `kitap/yerel-ortak/TASARIM-SISTEMI.md`.

## Komutlar

```sh
cd kitap/9-sinif-yerel/04-periyodik-tablo
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh   # unite.html → PDF + onizleme/s01…s15.png + taşma özeti
node ../../yerel-ortak/render.js . 3 4 --pdfsiz                             # yalnız değişen sayfaların PNG'si
node ../../yerel-ortak/render.js . --hepsi --onizleme                       # öğrenci, öğretmen, fotokopi, baskı, hazine kartları
```

`dogrula.py` 185 denetim yapar ve `SONUÇ: hepsi doğru` ile biter:
- **Element verisi:** yerel kopya (`uretec/tablo_veri.py`) kitap çerçevesindeki `yerel-cerceve/uretec/elementler.py` ile birebir
  (118 ad, yuvarlatılmış kütle, sınıf, konum) ve `periyodik.py` sınıf renkleriyle aynı; klasik ünitenin `elem.py` ve `gen.py`'si ile
  periyot, grup, blok ve sınıf kümeleri aynı (57–71 ve 89–103 f satırında, 3. grupta 6.–7. periyot yer tutucu, He s bloku/8A).
- **Konumlar dizilimden:** Aufbau + klasik ünitenin istisnaları (Cr, Cu, Mo, Ag); A'da ns + np, B'de ns + (n−1)d; Z = 1–56 ve 72–86
  tablo ile aynı. Ayrıca katman kuralı (Z ≤ 20), soy gaz kestirmesi (Z = 3–54), son terim tablosu (Z ≤ 36), yarı dolu orbital sayısı.
- **İyonlar:** grup → kararlı iyon, e = p − yük, izoelektronik çiftler, Ag⁺ = [Kr] 4d¹⁰.
- **Sorular:** 12 imtihan, 4 kıssa, 6 Üstad sorusunda tek doğru şık (`tek_sik`); görev, tuzak, hızlı görev, merdiven, meclis sonuçları.
- **Sayfadan okuma:** `data-dogru` işaretleri, A–E beş şık, Cevaplar ızgarası ve çözüm satırlarındaki harfler, meclis hükümleri,
  yan yol hızlı anahtarı, her soruda öğretmen çözümü (`.ogr`), meclis NEDEN ≤ 14 harf, DOĞRUSU ≤ 45 harf.
- **Akçe:** her durak sayfasının çipleri + hazine kartları = durağın akçesi; toplam 1400; HUD çubukları; Ahilik eşikleri.
- **Yasaklar ve tutarlılık:** elektronegatiflik yazılmadı, kurum adı/logo yok, bor rezervi "yaklaşık"; duraklar ve kale
  `rotalar.json` ile aynı yer ve koordinat; Medeniyetimizden metni `yerel-cerceve/uretec/medeniyet.py` ile aynı.

## Klasör

```
04-periyodik-tablo/
  README.md                  bu dosya
  unite.html                 ÜRETİLİR
  04-periyodik-tablo*.pdf    ÜRETİLİR (öğrenci ≈ 5,9 MB · öğretmen ≈ 5,9 · fotokopi ≈ 5,4 · baskı ≈ 6,4 · hazine kartları ≈ 0,25 MB)
  onizleme/                  ÜRETİLİR (s01…s15.png, varyant/, hazine-kartlari.png, fotokopi-murekkep.json)
  uretec/
    sablon.html              15 sayfanın içeriği + küçük üniteye özel CSS
    meta.json                5 durak, kale, 7 nişan (Üstad Mührü bonus), H1–H10, medeniyet, 18 kavram, "hud": "Maden Yolu I"
    kur.py                   SAYFA/SIMDI, panorama etiketlerinin çakışmasız yerleşimi, mühür ("MADEN YOLU I"), final, iki yerel düzeltme
    sahneler_unite.py        13 sahne + açılış panoraması + 5 nişan ikonu; yerel parçalar (ocak basamakları, tesis salonu, silo,
                             baca, konveyör, kamyon, ekskavatör, yük gemisi, liman vinci, çini karosu/panosu, vazo, fırın,
                             Kütahya evi, Kütahya Kalesi, gümüş külçe, balıkçıl, pelikan, ardıç)
    infografik_unite.py      zaman şeridi, blok haritası, adres okuma, dolma sırası, soy gaz cetveli, katman modeli, sınıf
                             haritası (rota iğneli), özellik çizelgesi, aileler, iyon oluşumu, hata avı listesi, soru şekilleri
    tablo_veri.py            118 elementin verisi (çerçeveyle aynı; dogrula.py kilitler)
    dogrula.py, olc.sh
```

## Sayfa planı

| s. | Sayfa | Sahne / bilgi grafiği | Akçe |
|---|---|---|---|
| 1 | Yola çıkış: başlık, Pamuk, tur haritası (10 etiket), 7 nişan, yol arkadaşları, hedefler, Ahilik | `maden_panorama` (Marmara, Uludağ, Porsuk, Eskişehir, Toroslar, Beyşehir ve Manyas gölleri) | – |
| 2 | 1. durak · **Seydişehir** · tablonun hikâyesi ve yapısı (periyodik yasa, Döbereiner→Moseley, eka-alüminyum→galyum, periyot/grup/blok, A/B↔IUPAC) | `seydisehir` (elektroliz salonları, alümina siloları, boksit yığını, Toroslar); `tarih_seridi`, `blok_haritasi` | 100 |
| 3 | 2. durak · **Kütahya** · elektron diziliminden yer bulma | `kutahya_cini` (çini panoları, fırın, vazolar, Co/Cu/Fe boya kâseleri); `adres_okuma` (Co), `dolma_sirasi` | 150 |
| 4 | 3. durak · **Gümüşköy** · katman ve soy gaz kestirmesi, He/Cr/Cu/Ag · **el-Bîrûnî** | `gumuskoy` (gümüş grisi basamaklar, tesis, külçeler); `katman_modeli`, `soygaz_cetveli` | 150 |
| 5 | 4. durak · **Kırka** · metal, ametal, yarı metal, soy gaz · **er-Râzî** | `kirka` (beyaz tinkal basamakları, kamyonlar, silolar); `sinif_haritasi`, `ozellik_tablosu`, `razi_araclari` | 150 |
| 6 | 5. durak · **Bandırma** · grup adları, iyon, izoelektronik | `bandirma` (gün batımı, yük gemisi, vinçler, tesis); `aileler`, `iyon_olusumu` | 150 |
| 7 | Hülasa · Kuşcenneti (Manyas Gölü) · 6 özet, sandık (10 kart), muhasebe, kendini yokla | `kuscenneti` (b40) | 40 |
| 8 | Yan yol 1 · Bigadiç · Meclis M1–M4 + hata avı listesi | `bigadic` (maden kampı, çardak, semaver); `meclis_denetim` | 120 |
| 9 | Yan yol 2 · Emet · Kıssa 1–4 (tablo, grafik) | `emet`; `triad_grafik` | 120 |
| 10 | Yan yol 3 · Germiyan Sokağı · Anahtar merdiveni 3 × 3 | `germiyan` (akşam, basamaklı sokak, kale) | 120 |
| 11–12 | Kütahya Kalesi · Büyük İmtihan 1–12 | `kale_kutahya` (b62), `kale_kapi_kutahya` (b30); `iskelet` | 300 |
| 13 | Üstad soruları (6, AYT tarzı, bonus) | `ustad_bandi` (ortak); `ustad_grafik` | bonus |
| 14 | Cevaplar ve çözümler | `kutahya_gece` (b36) | – |
| 15 | Final: akçe rayı, unvanlar (Tablo Üstadı 1150+), defter, nişan sayımı, sıradaki yol | `final_kutahya` | – |

Akçe: durak 100 + 4 × 150 = 700 · Hülasa 40 · Meclis 4 × 30 · Kıssa 4 × 30 · Anahtar 3 × 40 · İmtihan 12 × 25 = 300 → **1400**.
HUD çubuğu %: 0 · 0 · 7 · 18 · 29 · 39 · 50 · 53 · 61 · 70 · 79 · 89 · 100 · 100 · 100.

## Cevap anahtarları

- **Büyük İmtihan:** 1 B · 2 E · 3 D · 4 B · 5 C · 6 D · 7 A · 8 C · 9 B · 10 D · 11 E · 12 A (A 2, B 3, C 2, D 3, E 2)
- **Kıssalar:** 1 C · 2 B · 3 E · 4 D — **Üstad:** 1 D · 2 B · 3 E · 4 C · 5 A · 6 B
- **Meclis (haklı · hatalı satır):** M1 Yusuf · 1 — M2 Elif · 2 — M3 Yusuf · 2 — M4 Pamuk · 3
- **Merdiven:** 1) Ca, 4. periyot 2A; bir üstü 12 (Mg) · 2) 42 (Mo) · 3) Sn: 5. periyot 4A (14), p bloku, metal
- **Hızlı görevler:** s.2 3A, 31 (Ga) · s.3 4. periyot 7B · s.4 35 (Br) · s.5 Sb: 5. periyot 5A, yarı metal · s.6 Cl⁻
- **Görevler:** 1) ≈ 88,5 · 2) Si 4A, O 6A, Fe 8B · 3) Ag 5. periyot 1B · 4) yarı metal, metal, ametal, soy gaz · 5) 10 (Ne), 18 (Ar), X 3. periyot 6A

## Bölge ve tarih bilgileri (güven)

| Bilgi | Kullanım | Güven |
|---|---|---|
| Seydişehir'de Türkiye'nin birincil alüminyum tesisi; boksit → alümina (Al₂O₃) → elektroliz | s.2 | yüksek (WebSearch: MTA, tesis haberleri) |
| Kırka'da tinkal (boraks) açık ocakta çıkarılır; konsantrenin bir kısmı Bandırma'daki tesislere gider | s.5, s.6 | yüksek |
| Bandırma'daki tesislerde bor cevherinden borik asit gibi ürünler; Bandırma bir Marmara liman kenti | s.6 | yüksek (ürün listesi genel tutuldu) |
| Türkiye dünya bor rezervlerinin **yaklaşık** %70'ine sahip | s.5 | yüksek ("yaklaşık") |
| Gümüşköy (Kütahya'nın batısı) gümüş yatağı ve işletmesi | s.4 | yüksek (kurum adı yazılmadı) |
| Kütahya çinisinde kobalt maviyi, bakır turkuaz-yeşili verir; seramikte demir kırmızı-kahverengi, mangan mor-kahverengi | s.3, Kıssa 4 | yüksek (genel seramik kimyası) |
| Bigadiç ve Emet'te kolemanit gibi bor mineralleri | s.8, s.9 | yüksek |
| Mendeleyev 1869; eka-alüminyum tahmini (1871) ≈ 68, ≈ 5,9 g/cm³, Ea₂O₃; galyum 1875 (≈ 70, ≈ 5,9 g/cm³), ≈ 30 °C'de erir | s.2 | yüksek |
| Döbereiner 1829 (Ca–Sr–Ba), Newlands 1865, L. Meyer 1870, Moseley 1913 | s.2 | yüksek |
| Gümüşün kararlı izotopları ¹⁰⁷Ag ve ¹⁰⁹Ag; akçe gümüş sikke | s.4 | yüksek |
| İnce film güneş pillerinde Cu, In, Ga, Se | Kıssa 3 | yüksek |
| el-Bîrûnî 973–1048, metal ve değerli taşların özgül ağırlığı, *el-Cemâhir*; er-Râzî 865–925, maddeleri sınıflandırdı | s.4, s.5 | yüksek (`medeniyet.py` ifadesi) |

Cami, kilise ve manastır oyun durağı yapılmadı; logo yok; maden, tesis ve kale çizimleri temsilîdir (kale yer yer yıkık çizildi).

## Yerel düzeltmeler ve ortak kütüphaneye öneriler

- `kur.py · _rozet_duzelt`: ortak hazine rozeti yazı boyu sabit 30, H10 daireden taşar → 23 (Kimyasal Değişimler'deki gibi).
- `kur.py`: kesme yaprağının üst satırı "Yol 4 · Maden Yolu I" olarak kısaltıldı; `meta.json "hud"` ile HUD'da "Batı anadolu"
  küçük harf sorunu önlendi (ortak `hud_rota` son kelimeyi küçültüyor; özel adlar için istisna önerilir).
- Konturlu yazı yerine `halolu_yazi`; SVG'de kalın bağlamda `⁻` (U+207B) Nunito'da yok ve Type 3'e düşüyordu → tspan üst simge.
  Öneri: `dogrula_ortak`'a SVG/HTML'de fontta olmayan glifleri tarayan bir denetim.
