# 9. sınıf · Periyodik Özellikler · "Maden Yolu II · Doğu Anadolu" (yerel tasarım · Yol 5)

Tema 1 · Bölüm 5. 16 sayfalık, A4, baskıya hazır ünite: 6 durak + Hülasa + 3 yan yol + Büyük İmtihan (2 sayfa) +
Üstad soruları + Cevaplar + Final. Yol 4’ün (Maden Yolu I · Batı Anadolu) devamıdır. Klasik kaynak (konu, veri, doğrulanmış
sorular): `kitap/9-sinif/05-periyodik-ozellikler/kaynak.html`; sorular yeni bağlamla ve yeni sözlerle yeniden kuruldu.
Tasarım sistemi: `kitap/yerel-ortak/TASARIM-SISTEMI.md`.

## Komutlar

```sh
cd kitap/9-sinif-yerel/05-periyodik-ozellikler
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh    # unite.html → PDF + onizleme/s01…s16.png + taşma özeti
node ../../yerel-ortak/render.js . --hepsi [--onizleme]                     # + öğretmen, fotokopi, baskı, hazine kartları PDF'leri
node ../../yerel-ortak/render.js . 3 4 --pdfsiz                             # yalnız 3. ve 4. sayfanın PNG'si
```

`dogrula.py` 253 denetim yapar → `SONUÇ: hepsi doğru`:
- **Veri:** `infografik_unite.VERI` klasik ünitenin `svgler.py`/`sablon.html` değerleriyle aynı (yarıçap, iyon yarıçapı, İE₁,
  ardışık İE tabloları, EN); element adları, atom numaraları, periyot/grup ve sınıflar kitabın tablosuyla
  (`yerel-cerceve/uretec/elementler.py`) aynı; sayfada geçen her “Sembol sayı” (EN, İE₁, yarıçap) VERI ile aynı.
- **Eğilimler:** yarıçap (tek istisna Al > Ga, sayfada yıldızla yazılı), İE₁ (yalnız 2A→3A ve 5A→6A düşer), EN (Pauling),
  metalik karakter; ardışık İE’den değerlik elektronu (en büyük oran ≥ 3) 11 element için.
- **Sorular:** bütün görev, tuzak, hızlı görev, kıssa, meclis, merdiven, imtihan ve Üstad soruları yeniden hesaplanır; tek doğru şık;
  İmtihan ve Üstad’da A–E her biri en az bir kez.
- **Sayfa:** `data-dogru` işaretleri, Cevaplar ızgarası ve durak etiketleri, çözüm satırları, meclis hükümleri, NEDEN ≤ 14 /
  DOĞRUSU ≤ 45 harf, merdiven ≤ 50 harf, 46 öğretmen metni, CEVABIN = ters cevap, hazine kartı kendi durak sayfasında.
- **Akçe:** her durak sayfasındaki akçe çipleri + hazine kartları = levhadaki akçe = meta.json; toplam 1400; HUD çubuğu.

## Dosyalar

| Dosya | Ne |
|---|---|
| `uretec/meta.json` | künye: 6 durak (yer, başlık, enlem–boylam, sayfa, akçe), Divriği Kalesi, 8 nişan (Üstad Mührü bonus), H1–H12, Divriği Darüşşifası, 12 kavram; `hud: "Maden Yolu II"` |
| `uretec/sablon.html` | 16 sayfanın içeriği; başta üniteye özel küçük CSS |
| `uretec/kur.py` | sayfa künyesi (HUD, altbilgi, akçe çubuğu), `{{harita-etiket}}`, `{{final}}` (Divriği Kalesi burcu), `{{nisan-sayim}}` (4 × 2), kesme yaprağında kısa rota adı |
| `uretec/sahneler_unite.py` | bölge sahneleri ve parçaları (basamaklı demir ocağı, galeri ağzı, vagonet, cevher treni, kale sırtı, baraj, enerji direği, Kemaliye evi) + 6 nişan ikonu + açılış haritası |
| `uretec/infografik_unite.py` | `VERI` (dogrula.py da okur) + mini tabloda yarıçaplar, r = d/2, atomdan iyona, izoelektronik seri, kromit kristali, İE₁ grafiği, karbonun ardışık İE’leri (kırık eksen), EN ısı haritası, su molekülünde halat çekme, metalik/ametalik harita, soru grafikleri, darüşşifa (temsilî) |
| `uretec/dogrula.py` | sayısal doğrulama ve cevap anahtarı denetimi |

## Sayfa planı

| s. | Yer | İçerik | Sahne |
|---|---|---|---|
| 1 | Yola çıkış | dev başlık, Pamuk, Sivas–Elazığ halka haritası (6 durak + kale; Karasu, Murat, Keban Baraj Gölü, Hazar, Fırat), 8 nişan, hedefler, Ahilik (Eğilim Üstadı) | `panorama_rota` (gün batımı) |
| 2 | 1 · Divriği demir ocağı | atom yarıçapı, r = d/2, mini tablo, Görev 1, H1–H2, Tuzak (Mg > Na), çapraz durum, **Divriği Darüşşifası** | `divrigi` (sabah; basamaklı pas kızılı ocak, kamyonlar, cevher treni) |
| 3 | 2 · Guleman krom ocakları | iyon yarıçapı, p/e, Na→Na⁺ / Cl→Cl⁻, izoelektronik seri, Görev 2 (Fe iyonları, 18 e⁻), kromit kristali, H3–H4 | `guleman` (öğle; koyu ofiyolit tepeler, galeri, vagonetler) |
| 4 | 3 · Maden (Dicle vadisi) | iyonlaşma enerjisi, İE₁ grafiği (Z 1–20), iki istisna, Görev 3 (Si P S Cl), H5–H6 | `maden` (ikindi; V vadi, bakır yeşili damarlar, cüruf, galeriler) |
| 5 | 4 · Hazar Gölü | ardışık İE, karbon (kırık eksen), grup bulma, denklemi doğru oku, Görev 4 (dört kart), H7–H8 | `hazar` (altın saat; derin mavi göl, iskele, dalgıç şamandırası) |
| 6 | 5 · Keban Baraj Gölü | elektronegatiflik (Pauling), EN ısı haritası, O–H halat çekme, Görev 5 (N O P K; O–H, N–H, C–H), H9–H10 | `firat_kavsagi` (sabah; Karasu ile Murat’ın buluştuğu göl) |
| 7 | 6 · Keban | metalik/ametalik karakter, aktiflik, özellik haritası (kitabın sınıf renkleri), eğilim tablosu, Görev 6, galen, H11–H12 | `keban` (öğle; baraj, dolusavak, enerji hattı, eski galeriler) |
| 8 | Hülasa · Fırat kıyısı | 6 özet kart, hazine sandığı (12), muhasebe | `firat_kamp` (alacakaranlık, çadır, ateş) |
| 9 | Meclis · Kemaliye | 4 hatalı çözüm, hata avcısının dört sorusu, Eğin evleri | `kemaliye` |
| 10 | Kıssalar · Karanlık Kanyon | maden suyu iyonları (tablo), Na-iyon pil, alkali İE₁ (grafik), florit ve HF (tablo) | `karanlik_kanyon` |
| 11 | Anahtar merdiveni · kale yokuşu | 3 problem × 3 basamak | `kale_yokusu` |
| 12–13 | Divriği Kalesi | Büyük İmtihan 1–12 + skor | `divrigi_kalesi`, ortak `kale_kapi` |
| 14 | Üstad (bonus) | ardışık İE tablosu, 8 element grafiği, Al → Al³⁺ hesabı, Ca, izoelektronik dörtlü, kısmi yük çıkarımı | ortak `ustad_bandi` |
| 15 | Cevaplar | anahtar (durak etiketli), yan yol + Üstad anahtarı, bütün çözümler, “Bu yoldaki sayılar” (ölçek notu) | `divrigi_gece` |
| 16 | Final | akçe rayı (Eğilim Üstadı), unvanlar, akçe defteri, nişan sayımı, sıradaki yol (Yol 6) | `divrigi_final` (burçta bayraklı Pamuk) |

## Cevap anahtarı

- **Büyük İmtihan:** 1 C · 2 A · 3 D · 4 B · 5 C · 6 E · 7 A · 8 D · 9 B · 10 D · 11 E · 12 B
- **Kıssalar:** 1 C · 2 B · 3 D · 4 A
- **Üstad (bonus):** 1 E · 2 C · 3 B · 4 A · 5 D · 6 A
- **Meclis:** 1 Elif (satır 2; K 227 > Ca 197) · 2 Pamuk (satır 3; S²⁻ > S) · 3 Yusuf (satır 3; Be 899 > B 801) · 4 Yusuf (satır 2; en büyük oran 6,8 → 3A)
- **Anahtar merdiveni:** 1 → 6A, Z = 8, 8 İE · 2 → Cl⁻ > K⁺ > F⁻ > Na⁺ · 3 → Q soy gaz, Y 5A, R en büyük
- **Akçe:** duraklar 100 + 5 × 120, Hülasa 40, Meclis 120, Kıssa 120, Anahtar 120, İmtihan 300 = **1400**

## Veri ve ölçek

Yarıçaplar pm (yaklaşık), İE kJ/mol (yuvarlatılmış ölçüm değerleri), **elektronegatiflik Pauling ölçeği (F = 4,0; Cl 3,2; O 3,4)** —
klasik ünitenin değerleri. Klasik ünitede olmayan ardışık İE’ler (Na 496 · 4562 · 6910 · 9543; Mg İE₃ 7733, İE₄ 10 543;
Ca 590 · 1145 · 4912 · 6491) aynı ölçüm tablosundan, aynı yuvarlamayla eklendi.

## Bilinen notlar

- Kesme yaprağında render.js “hazine yaprağı taşma” uyarısı verir (iki satırlık formüller hücreyi doldurur); görünüşte kesilme yoktur.
  Uzun rota adı yüzünden hücre başlığı iki satıra kırılıyordu; `kur.py` yaprakta kısa adı (`hud`) kullanır.
- Fotokopide özellik haritasındaki sınıf renkleri (metal/yarı metal/ametal) griye döner ve ayrışmaz; harita metni ve oklar okunur.
