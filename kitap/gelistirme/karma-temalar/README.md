# Geliştirme örneği · Karma temalar (9. sınıf "Çini ve Toprak" · 10. sınıf "Göl ve Rasathane")

Öğretmen atom modelleri örneğindeki bütün seçenekleri (Hap Bilgi ailesi, temalar, konu karakterleri, öneriler) onayladı ve
her sınıfa **farklı ama karma** bir palet istedi. Bu klasör iki sınıfın örneğini üretir:

* **9. sınıf:** atom modelleri örneğinin 3 sayfası (Yol 3 · Şanlıurfa–Harran, ünitede s.2–4), "Çini ve Toprak" paletiyle.
* **10. sınıf:** Gazlar ünitesinden (`10-sinif-yerel/04-gazlar`, Yol 4 · Kapadokya) 3 **yeni** sayfa (ünitede s.3, 5, 6),
  "Göl ve Rasathane" paletiyle.

Ortak kütüphaneye, ünitelere, `yerel-cerceve/`'ye ve `atom-modelleri/` çıktılarına dokunulmadı. Atom modelleri
modülleri (`hap_bilgi`, `infografik_gelistirme`, `sahneler_gelistirme`, `gelistirme.css`, `sablon.html`) **salt okunur**
içe aktarılır. `tema.py` ve `konu_karakterleri.py` buraya kopyalanıp genişletildi (karma paletler, gaz karakterleri).
Gazlar ünitesinin sahneleri ve NH₃–HCl borusu grafiği değiştirilmeden yüklenir.

## Dosyalar ve komutlar

| Dosya | Ne |
|---|---|
| `karma-9-cini-toprak.pdf` | 9. sınıf · 3 sayfa (Modellerin yolculuğu · Altın levha çizgi romanı · Enerji merdiveni) |
| `karma-10-gol-rasathane.pdf` | 10. sınıf · 3 sayfa (Boyle ve Charles · İdeal gaz · Tünelde yarış) |
| `karma-katalog.pdf` | 4 sayfa: K1 iki palet · K2 9↔10 karşılaştırma · K3 renk denetimi · K4 güncel karakter kiti |
| `onizleme/9-cini-toprak/s01–s03.png`, `onizleme/10-gol-rasathane/s01–s03.png` | sayfa önizlemeleri (2×) |
| `onizleme/karsilastirma-9-10.png` | 6 sayfa yan yana + iki palet şeridi |
| `onizleme/paletler.png` · `karsilastirma-sayfasi.png` · `renk-denetimi.png` · `karakterler.png` | katalog sayfaları |
| `onizleme/renk-korlugu-9-10.png` · `renk-denetimi.json` | döteranopi benzetimi ve sayısal sonuçlar |

```sh
cd kitap/gelistirme/karma-temalar
python3 uretec/kur.py              # iki sınıf + katalog + karşılaştırma + renk denetimi (≈ 25 sn)
python3 uretec/kur.py --sinif 10   # tek sınıf · --katalog yalnız katalog · --pdfsiz yalnız PNG
python3 uretec/dogrula.py          # 74 denetim → SONUÇ: hepsi doğru
```

Üç HTML'de de `render.js` taşma denetimi **taşma yok**; üç PDF'te **Type 3 font 0**; toplam ≈ 4,8 MB.

```
uretec/
  kur.py               iki kitap (u9: atom şablonu · u10: sablon10.html), tema uygulama, render.js
  sablon10.html        Gazlar 3 sayfa       katalog_karma.html   4 katalog sayfası
  tema.py              (kopya + ek) iki karma palet, "alaca" sahne ışığı, tema başına css vurgu katmanı
  konu_karakterleri.py (kopya + ek) 7 gaz taneciği × 3 sıcaklık ifadesi (kk-gaz-*)
  infografik_karma.py  pistonlu kap, 6 çizgi roman panosu, kinetik kutular, tünel yarışı
  sahneler_karma.py    Gazlar sahneleri (goreme, kizilcukur, derinkuyu, kapadokya_gece) + graham_boru (salt okunur)
  katalog_karma.py     katalog yer tutucuları, karşılaştırma ve döteranopi levhaları, renk denetimi
  karma.css            gaz sayfalarına küçük düzenler + ikili kart biçim ipucu
  dogrula.py           bilgi, sayı ve palet denetimi
  s9/meta.json · s10/meta.json   9/03 ve 10/04 meta.json'larından aynen
```

## 1. Paletler

Her palet üç katmanlıdır (`tema.py` `TEMALAR["cini-toprak"]`, `TEMALAR["gol-rasathane"]`):

1. **Taban:** tokenların büyük kısmı taban temadan (İznik Çini / Van Gölü). Kurulumda aynı palet eşlemesi çalışır (OKLab, CSS filter yok).
2. **Vurgu katmanı:** temanın `css` alanı bileşen bazında birkaç kural ekler. Bunlar HUD, bant çizgisi, levha etiketi,
   başlık vurgusu, levha gölgesi, altbilgi, koyu kartlar ve sonuç panosudur. Sahne bantları temanın ışığıyla boyanır:
   9. sınıfta ikindi sıcaklığı (`sicak`), 10. sınıfta alacakaranlık (`alaca`, yeni).
3. **Kutu zeminleri:** `-a` / `-aa` tintleri Yumuşak Pastel'den, yumuşak ve göz yormayan.

**Sabit anlam renkleri (iki kitapta aynı aile):** akçe kehribarı `keh`, Tuzak kırmızısı `mer`, doğru yeşili `zumrut`
**#1A7F53** (iyileştirilmiş, beyazda 5,0), balon ve kart tintleri `mer-a #FCE2E4` ve `keh-a #FFEAB8` (iki kitapta birebir).
Karakter, tanecik ve spektrum renkleri hiçbir temada değişmez.

| Palet | Taban | Vurgu | Kimlik |
|---|---|---|---|
| **Çini ve Toprak** (9) | İznik Çini | Selçuklu Toprak | beyaz zemin, kobalt ana renk, çini turkuazı kavram, mercan Tuzak; kerpiç-kahve HUD, terakota levha vurgusu, altın; sıcak sahne |
| **Göl ve Rasathane** (10) | Van Gölü | Rasathane Gecesi | turkuaz ana renk, kehribar, çivit-erguvan kavram; gece laciverti HUD ve koyu kartlar, altın HUD vurgusu; alacakaranlık sahne |

İlk bakıştaki fark HUD rengi (kahve ↔ lacivert), ana renk (kobalt ↔ turkuaz), kavram rengi ve sahne ışığından gelir.
Seri kimliğini ortak çerçeve, bileşenler, anlam renkleri ve karakterler taşır (K1 ve K2 sayfaları).

### Token tablosu (taban değerinden farklı olanlarda parantez içinde taban)

| Token | Çini ve Toprak (taban İznik Çini) | Göl ve Rasathane (taban Van Gölü) |
|---|---|---|
| `--kar` | `#FFFFFF` | `#F9FBFD` (taban `#FBFDFD`) |
| `--kirec` | `#FFFAF2` (taban `#FFFEFA`) | `#FFFDF6` (taban `#FFFDF7`) |
| `--obs` | `#131A33` | `#14193C` (taban `#1B1D26`) |
| `--obs-2` | `#2B3556` | `#2C3360` (taban `#343947`) |
| `--soluk` | `#4E5A73` | `#525A7E` (taban `#56636E`) |
| `--cizgi` | `#D8DEEA` (taban `#D2DBEE`) | `#D3D9EA` (taban `#CFDCE0`) |
| `--gol` | `#1F4FA8` | `#13A3A6` |
| `--gol-k` | `#14377C` | `#0A6C74` |
| `--gol-a` | `#E5EAF6` (taban `#DDE6F7`) | `#DEF1EF` (taban `#DCF3F1`) |
| `--gol-aa` | `#F3F6FC` (taban `#EFF3FC`) | `#F0F8F7` (taban `#EEF9F8`) |
| `--derin` | `#0E2457` | `#161B47` (taban `#0E4C5A`) |
| `--keh` | `#D9A11F` (taban `#F2A516`) | `#F0A21A` |
| `--keh-k` | `#7A5608` (taban `#8A5300`) | `#8C5500` |
| `--keh-a` | `#FFEAB8` (taban `#FFF1CF`) | `#FFEAB8` (taban `#FFF0CF`) |
| `--mer` | `#E04A35` | `#E2533D` |
| `--mer-k` | `#A11E12` | `#A12817` |
| `--mer-a` | `#FCE2E4` (taban `#FDE4DF`) | `#FCE2E4` (taban `#FDE7E1`) |
| `--kob` | `#13798F` (taban `#20855A`) | `#5B4FB8` (taban `#2B50B5`) |
| `--kob-k` | `#0C5466` (taban `#135C3C`) | `#3D2F8C` (taban `#1B3584`) |
| `--kob-a` | `#E2F1F5` (taban `#DFF2E7`) | `#EEEBFA` (taban `#E6ECFB`) |
| `--gun` | `#E5763D` (taban `#F26B3A`) | `#F2884C` (taban `#FF7A3D`) |
| `--pembe` | `#E0587A` (taban `#E94E7C`) | `#E35C9A` (taban `#FF5C8A`) |
| `--erguvan` | `#6A3E8E` (taban `#5E3D93`) | `#8E3B86` (taban `#7B3F8C`) |
| `--altin` | `#C9952B` | `#D4A02C` (taban `#C9952B`) |
| `--altin-k` | `#85600F` (taban `#8A6212`) | `#866011` (taban `#8A6212`) |
| `--altin-a` | `#F6E6BC` (taban `#F6E7BF`) | `#F7E9C2` (taban `#F6E7BF`) |
| `--lajver` | `#173A8F` | `#1A2368` (taban `#1D3A8A`) |
| `--zumrut` | `#1A7F53` (taban `#127A4F`) | `#1A7F53` (taban `#1F8A5B`) |
| `--gum` | `#B2BAC6` (taban `#A9B5C8`) | `#A9B0C8` (taban `#A3B3BE`) |
| `--gum-k` | `#56627A` (taban `#55617A`) | `#565D80` (taban `#586874`) |
| `--gum-a` | `#F1F3F7` (taban `#EEF1F7`) | `#EEF0F7` (taban `#EDF2F5`) |

### Vurgu katmanının renkleri (token tablosunda görünmez)

| Palet | Renkler |
|---|---|
| Çini ve Toprak | HUD `#2E1F17` · HUD yeri `#E8D4BE` · levha etiketi `#8A3C1A` · levha vurgusu `#B4532C` · levha gölgesi `#7C3416` · hedef çizgisi `#C9952B` |
| Göl ve Rasathane | HUD `#10153A` · HUD vurgusu `#F0C24A` · levha etiketi `#3D2F8C` · levha vurgusu `#0E8F93` · levha gölgesi `#3D2F8C` · hedef çizgisi `#D4A02C` |

## 2. Renk denetimi

Atom modelleri örneğiyle aynı yöntem kullanıldı: WCAG kontrast oranı ve Machado (2009) döteranopi matrisi. Döteranopi
denetimi hem token çiftleri (OKLab ΔE·100) hem sayfa PNG'leri üzerinde yapıldı. Vurgu katmanının renkleri de denetlendi.

**Kontrast:** bütün çiftler eşiğin üstünde (gövde 16–17; en düşük: 10. sınıf çip beyaz/turkuaz 3,1 ≥ 3; başlık vurgusu
#0E8F93, 25 pt, 3,9 ≥ 3).

| Yazı / zemin (eşik) | Çini ve Toprak | Göl ve Rasathane |
|---|---|---|
| gövde · obs / kar (≥ 7,0) | 17,2 | 16,4 |
| etiket · gol-k / beyaz (≥ 4,5) | 11,2 | 6,2 |
| etiket · gol-k / gol-aa (≥ 4,5) | 10,4 | 5,7 |
| akçe · keh-k / keh-a (≥ 4,5) | 5,6 | 5,2 |
| Tuzak · mer-k / mer-a (≥ 4,5) | 6,3 | 6,0 |
| kavram · kob-k / kob-a (≥ 4,5) | 7,3 | 9,0 |
| Doğrusu · zumrut / beyaz (≥ 4,5) | 5,0 | 5,0 |
| HUD · beyaz / obs (≥ 7,0) | 17,2 | 17,0 |
| HUD · keh / obs (≥ 4,5) | 7,4 | 8,0 |
| çip · beyaz / gol (≥ 3,0) | 7,7 | 3,1 |
| Tuzak başlığı · beyaz / mer (≥ 3,0) | 4,0 | 3,8 |
| kurdele · beyaz / kob (≥ 3,0) | 5,0 | 6,5 |
| tezhip · altin-a / lajver (≥ 4,5) | 8,3 | 11,7 |
| **vurgu katmanı (tema css)** | | |
| Çini ve Toprak · HUD yeri · #E8D4BE / #2E1F17 (≥ 4,5) | 11,0 | – |
| Çini ve Toprak · levha etiketi · #8A3C1A / levha (≥ 4,5) | 7,3 | – |
| Çini ve Toprak · levha başlık (25 pt) · #B4532C (≥ 3,0) | 4,8 | – |
| Çini ve Toprak · altbilgi · #7C3416 / kar (≥ 4,5) | 8,9 | – |
| Çini ve Toprak · koyu kart · beyaz / #2E1F17 (≥ 7,0) | 15,9 | – |
| Göl ve Rasathane · HUD vurgusu · #F0C24A / #10153A (≥ 4,5) | – | 10,5 |
| Göl ve Rasathane · levha etiketi · #3D2F8C / levha (≥ 4,5) | – | 10,6 |
| Göl ve Rasathane · levha başlık (25 pt) · #0E8F93 (≥ 3,0) | – | 3,9 |
| Göl ve Rasathane · altbilgi · #3D2F8C / kar (≥ 4,5) | – | 10,2 |
| Göl ve Rasathane · koyu kart · beyaz / #14193C (≥ 7,0) | – | 17,0 |

**Döteranopi (ΔE < 6 sorun ⚠):**

| Çift (ipucu) | Çini ve Toprak | Göl ve Rasathane |
|---|---|---|
| Yanlış ↔ Doğru (çarpı/tik, mühür) | 28,8 → 12,9 | 28,5 → 13,8 |
| Tuzak ↔ ana renk (başlık şeridi) | 35,2 → 32,9 | 28,9 → 14,8 |
| Akçe ↔ Tuzak (çip / başlık) | 19,6 → 12,5 | 18,7 → 14,4 |
| Ana renk ↔ kavram (etiket renkleri) | 13,7 → 13,3 | 24,3 → 20,5 |
| Ana renk ↔ akçe (kapsül kapakları) | 41,9 → 43,5 | 26,5 → 23,8 |
| Elif ↔ Pamuk balonu (balon zemini · tint düzeltildi) | 6,7 → 6,2 | 6,7 → 6,2 |
| Yanlış ↔ doğru zemini (ikili kart · biçim: kesik ↔ düz çerçeve) | **5,0 → 3,9** ⚠ | **5,3 → 3,7** ⚠ |
| Kavram ↔ erguvan (gün batımı / rozet) | 17,8 → 9,0 | 12,4 → 10,3 |
| Kavram ↔ Doğru (kavram kutusu · doğru etiketi) | 10,1 → 9,5 | 24,5 → 20,0 |
| Ana renk ↔ Doğru (etiket · doğru) | 22,4 → 21,2 | 14,1 → 13,6 |

**Düzeltilen sorunlu çiftler:**
* **Kavram ↔ Doğru (9. sınıf):** kavram rengi ilk tarifte #1C7A68'di ve doğru yeşiline (#1A7F53) çok yakındı
  (ΔE 4,0; döteranopta 3,5). Kavram rengi çini turkuazı **#13798F** yapıldı (9,5). Metin kontrastı 7,3.
* **Elif ↔ Pamuk balon zeminleri:** iki palette de 2,4–2,8 çıktı. Ortak tintler **mer-a #FCE2E4**, **keh-a #FFEAB8** oldu (6,2).
* **Yanlış ↔ doğru zemini (ikili kart):** pastel tintlerde pembe ile nane, döteranop gözde griye yakınsar (en iyi aday 5,8).
  Renkle çözülemediği için **biçim ipucu** eklendi: yanlış tarafı kesik mercan, doğru tarafı düz yeşil çerçeve
  (`karma.css`). Kartta ayrıca çarpı/tik ikonu, başlık ve üstü çizili yazı var.
* Kırmızı/yeşil Yanlış ↔ Doğru çifti döteranopta 12,9 / 13,8'e iner. Anlam hiçbir yerde yalnız renkle verilmez.

## 3. 10. sınıf · Gazlar sayfaları

Ünitenin doğrulanmış içeriği, sabitleri (R = 0,082 L·atm/(mol·K), T(K) = t(°C) + 273, NŞA'da 22,4 L), görevleri,
Tuzak'ları ve Derinkuyu bilgisi aynen kullanıldı. Sahneler ünitenin `goreme`, `kizilcukur`, `derinkuyu` sahneleridir.

| s. | Sayfa | İçerik | Dikkat görselleri ve öneriler |
|---|---|---|---|
| 3 | **Göreme · Boyle ve Charles** | **Pistonlu kap tanecik sahnesi:** aynı 6 tanecik; Boyle (1 atm · V → 2 atm · V/2, şaşkın tanecikler, duvar kıvılcımları) ve Charles (300 K uykulu → 600 K canlı, V → 2V). **Çizgi roman, balonun kısa tarihi (6 pano):** 1662 Boyle J borusu → ölçüm (76 cmHg fazla = 1 atm, hacim yarıya) → 1 Aralık 1783 Charles ile Robert, Tuileries'den hidrojen balonu → ≈ 550 m, 2 sa 5 dk, 36 km, Nesles-la-Vallée → y. 1787 Charles'ın bulgusu, 1802 Gay-Lussac yayımladı → bugün Göreme | Hap Bilgi ×2 (Boyle, Charles) · Kendini dene · Bir bakışta |
| 5 | **Kızılçukur · ideal gaz** | **Aynı kap, üç sıcaklık:** 200 K (−73 °C) uykulu ve yavaş, 300 K (27 °C), 600 K (327 °C) canlı ve hızlı. Ortalama E<sub>k</sub> ×1 · ×1,5 · ×3, hız ×1 · ×1,22 · ×1,73 (√T), iz uzunluğu ∝ √T, kıvılcım sayısı = duvar çarpışması. Kinetik teori, PV = nRT, Görev 6 (zarf: 90 000 → 75 000 mol, ≈ 435 kg hava çıkar), Tuzak | **Dikkat!** (°C → K: 27 °C = 300 K; 20 → 40 °C hacim 313/293 ≈ 1,07 katı) · **Sınav Radarı** (birimler, R) · **Kilit Bilgi** (basınç = duvar çarpması) · Kendini dene · Bir bakışta |
| 6 | **Derinkuyu · tünelde yarış** | **Tünel yarışı:** aynı sürede He 40 m, CH₄ 20 m, O₂ ≈ 14,1 m, SO₂ 10 m (yol ∝ 1/√M), Graham kutusu √(64/4) = √16 = 4. Difüzyon/efüzyon tablosu, Görev 8 (NH₃–HCl halkası ≈ 59 cm), Derinkuyu ≈ 85 m | **Altın Kural** (v₁/v₂ = √(M₂/M₁) = t₂/t₁) · Hap Bilgi ×2 · Kendini dene (H₂/O₂ 4 kat; SO₂ 30 s → CH₄ 15 s) · Bir bakışta |

**Tarih ve iddialar (güven):**

| İddia | Kaynak / denetim | Güven |
|---|---|---|
| Boyle'un J borusu deneyi, 1662 | Boyle yasası 1662'de yayımlandı (*New Experiments…*, 2. baskı ekleri); standart bilim tarihi bilgisi | yüksek |
| "76 cm cıva farkı → hacim yarıya" | fizik ilkesi (bugünkü 1 atm = 76 cmHg). Boyle kendi ölçümlerini inç ile yaptı (≈ 29 inç) | yüksek (ilke) |
| Charles ile Nicolas-Louis Robert, 1 Aralık 1783, Tuileries Bahçesi, hidrojen balonu | Wikipedia (Jacques Charles, Charlière, Robert kardeşler); Smithsonian NASM yazısı | yüksek |
| ≈ 550 m yükseklik, 2 sa 5 dk, 36 km, iniş Nesles-la-Vallée, kum safrasıyla yükseklik ayarı | aynı kaynaklar (≈ 1800 ft) | yüksek |
| Charles yasası y. 1787, yayımlanmadı; Gay-Lussac 1802'de yayımladı ve Charles'a bağladı | Wikipedia, Encyclopedia.com (tarih "1787 dolayı" diye verildi) | yüksek (yıl yaklaşık) |
| Gerçek kişi yüzü yok | balon sepetinde iki yüzsüz siluet; J borusu panosunda yalnız cam ve cıva | – |

Sayısal denetim (`dogrula.py`, 74 denetim): R = 22,4/273 = 0,08205; mol kütleleri atom kütlelerinden; pistonlu kap ve
J borusu çizimindeki hacim sütunları (246 ↔ 123 birim; 140 ↔ 70 birim); Kendini dene sonuçları (3 L, 2 katı, 4 L, eşit,
4 kat, 15 s); kinetik oranlar (1,5 · 3; √1,5 = 1,22, √3 = 1,73); °C ↔ K etiketleri; Görev 6 (2,214·10⁶ L·atm;
90 000 / 75 000 mol; 435 000 g); tünel yolları 10·√(64/M); Görev 8 (√(36,5/17) = 1,465; x = 59,4 cm); 9. sınıf
plakalarındaki yıllar; palet kuralları (Doğrusu #1A7F53, kırmızı/altın aileleri, ortak tintler, kontrast eşikleri, kalan
döteranopi çiftleri, ikili kart biçim ipucu, CSS filter yok).

## 4. Güncel konu karakterleri kiti

Atom modelleri kitine (20 karakter) **7 gaz taneciği** eklendi, her biri üç ifadeli: oda sıcaklığı, `-soguk` (kapalı
gözler, "z z", kar kristali) ve `-sicak` (iri parlak gözler, ter damlası, sıcaklık kıvrımları). Renkler `renkler.ATOM`'dan
gelir (H beyaz, He camgöbeği, C koyu gri, N kobalt, O mercan, S sarı). Biçimler doğrudur: CO₂ doğrusal, SO₂ ≈ 119° kırık.
CH₄ düzlemde dört H'li (dörtyüzlünün 2B izdüşümü). El çizilmez. K4 sayfasında ayrıca `yuz()` fonksiyonunun 10 ifadesi
"ifade sözlüğü" olarak gösterilir.

| Kimlik | viewBox | Ad | M (g/mol) | Not |
|---|---|---|---|---|
| `#kk-gaz-he` (+ `-soguk`, `-sicak`) | `0 0 60 60` | He | 4 | tek atomlu, en hafif soy gaz |
| `#kk-gaz-h2` (+ `-soguk`, `-sicak`) | `0 0 84 60` | H₂ | 2 | en hafif gaz |
| `#kk-gaz-o2` (+ `-soguk`, `-sicak`) | `0 0 92 64` | O₂ | 32 | havanın %21’i |
| `#kk-gaz-n2` (+ `-soguk`, `-sicak`) | `0 0 92 64` | N₂ | 28 | havanın %78’i |
| `#kk-gaz-co2` (+ `-soguk`, `-sicak`) | `0 0 124 64` | CO₂ | 44 | doğrusal; havadan ağır |
| `#kk-gaz-so2` (+ `-soguk`, `-sicak`) | `0 0 104 82` | SO₂ | 64 | kırık (V) biçimli |
| `#kk-gaz-ch4` (+ `-soguk`, `-sicak`) | `0 0 96 96` | CH₄ | 16 | düzgün dörtyüzlü |

## 5. Ortak kütüphaneye taşınırsa

Atom modelleri README'sindeki plan geçerli. Ek olarak:
* `tema.py`'ye **katmanlı tema** (taban + `css` vurgu katmanı + kutu tintleri) ve `alaca` sahne ışığı;
  `meta.json`'a `"palet": "cini-toprak"` alanı. `kur_ortak` bu alanı okuyup sınıfın paletini uygular:
  9-sinif-yerel → Çini ve Toprak, 10-sinif-yerel → Göl ve Rasathane.
* Palet kesinleşirse eşleme yerine değerler bir kez yazılabilir: ortak stil.css'e sınıf başına
  `html[data-palet="…"]` token blokları ve vurgu kuralları, renkler.py'ye sınıf paletleri.
* `konu_karakterleri.py` (gaz karakterleri dahil) ortak `cizim/` altına girer.
* Fotokopi varyantı için `html.fotokopi` kuralları vurgu katmanını da kapsamalı (koyu HUD ve kartlar beyaza döner).

## Bilinen sorunlar ve sınırlar

* **Fotokopi ve öğretmen varyantları** üretilmedi: yeni bileşenlerin `html.fotokopi` kuralları ve Kendini dene için
  `.ogr` işaretleri yok (atom modelleri örneğiyle aynı durum).
* **Yanlış ↔ doğru zemini** döteranopta renkle ayrışmıyor (ΔE 3,7–3,9). Biçim ipucuyla çözüldü, tintler değişmedi.
* 10. sınıf s.3'te ünitenin Görev 2–3 ve H4–H5 kartları yok; yerine tanecik sahnesi ve çizgi roman geldi. Üniteye
  taşınırsa görevler sonraki sayfaya kaydırılmalı. s.5 ve s.6'da Görev 7, 9, 10 ve H9–H12 kartları da yok.
* Gece/alacakaranlık eşlemesi sahnedeki dekoratif renkleri (prizma, balon zarfları) koyulaştırır. Bilgi grafiklerindeki
  spektrum ve tanecik renkleri sabittir.
* α harfi Nunito/Baloo'da yok, DejaVu'dan gelir (Type 3 değil). `¼` ve `√` fontlarda var.
* Katalog sayfaları nötr Van Gölü çerçevesiyle basılır; iki palet K1–K3'te yan yana gösterilir.
