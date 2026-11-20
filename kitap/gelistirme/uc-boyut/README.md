# Geliştirme örneği · 3B moleküller (kırmızı–camgöbeği kâğıt gözlükle, anaglif)

Öğretmenin "piyasadaki hiçbir kimya kitabında olmayan özellik" listesinden seçtiği fikir: molekülleri ve kristalleri
**kâğıttan dışarı çıkan** üç boyutlu resimler olarak basmak. Bu klasör fikrin çalıştığını gerçek kitap sayfalarında gösterir:
gerçek 3B koordinatlardan anaglif üreten küçük bir motor, kitap çerçevesinde 4 örnek sayfa, gözlüksüz bakış için
önizlemeler ve her sayıyı yeniden hesaplayan bir doğrulama betiği.

Ortak kütüphaneye, ünitelere, `yerel-cerceve/`'ye ve öteki `gelistirme/` klasörlerine dokunulmadı. Palet (`tema.py`) ve
Hap Bilgi ailesi (`hap_bilgi.py`, `gelistirme.css`) `karma-temalar/` ve `atom-modelleri/` klasörlerinden **salt okunur**
içe aktarılır.

## Dosyalar ve komutlar

| Dosya | Ne |
|---|---|
| `uc-boyut-ornek.pdf` | 4 sayfa, A4, 3,5 MB, Type 3 font 0 |
| `onizleme/s01.png` – `s04.png` | sayfa önizlemeleri (2×) |
| `onizleme/sallanan-ch4.gif`, `-nacl`, `-elmas`, `-hid-na` | "sallanan 3B": sol ve sağ göz bakışı art arda (7 kare/sn); gözlüksüz derinlik izlenimi (16–42 KB) |
| `onizleme/iki-goz.png` | sol gözün gördüğü · sağ gözün gördüğü · anaglif (CH₄) |
| `gorsel/ana-<ad>.png` | 13 anaglif, basılı boyutunda 300 dpi (38–207 KB) |
| `gorsel/duz-<ad>.png` | aynı koordinatlardan renkli düz resim (gözlüksüz bakış, fotokopi) |
| `gorsel/test-yazi.png`, `test-derinlik.png` | gözlük testi desenleri |
| `gorsel/uc-boyut.json` | her resmin stereo ölçüleri (sayfa, README ve doğrulama buradan okur) |

```sh
cd kitap/gelistirme/uc-boyut
python3 uretec/kur.py            # görseller yoksa üretir; iki HTML → render.js → PDF'ler birleşir (≈ 12 sn)
python3 uretec/kur.py --gorsel   # anaglifleri, düz resimleri, test desenlerini ve GIF'leri baştan üretir
python3 uretec/gorseller.py ch4  # tek yapı (deneme)
python3 uretec/dogrula.py        # 177 denetim → SONUÇ: hepsi doğru
```

```
uretec/
  uc_boyut.py      MOTOR: Yapi sınıfı, ışın–yüzey kesişimli çizim, stereo ölçüsü, anaglif; molekül ve örgü kurucuları
  gorseller.py     hangi yapı hangi görünümde, hangi boyutta; test desenleri; GIF ve iki-goz.png
  sahneler_uc.py   bantlar (Tuz Gölü–Hasan Dağı, Mardin, atölye masası), şemalar, kesme şablonu, nötr 3B ikonları
  sablon.html      4 sayfa        uc_boyut.css   anaglif kartları ve gözlük sayfası
  kur.py           kurucu (sayfa → künye → palet), render.js, PDF birleştirme
  dogrula.py       sayı, örgü, stereo, kanal ve dosya denetimi
  s9-06/ s9-09/ s10-04/meta.json   sayfaların künyeleri (9/06 ve 9/09 üniteleri henüz yazılmadığı için GEÇİCİ)
```

Bir HTML tek paletle kurulabildiği için iki HTML üretilir (9. sınıf "Çini ve Toprak": s.1, 2, 4 · 10. sınıf "Göl ve
Rasathane": s.3); PDF'ler `pypdf` ile sayfa sırasına göre birleştirilir. `render.js` taşma denetimi iki HTML'de de
**taşma yok**.

## 1. Nasıl çalışır

1. **Geometri.** Her yapı gerçek 3B koordinatlarla kurulur (`uc_boyut.py`, birim Å): moleküller bağ uzunluğu ve bağ
   açısından (CH₄: dörtyüzlünün köşeleri; NH₃: 106,7°'den hesaplanan piramit; H₂O: 104,5°), kristaller örgü
   sabitlerinden (NaCl a = 5,64 Å; elmas a = 3,567 Å; grafit 1,42 / 3,35 Å; altıgen buz O···O 2,76 Å). Buzda hidrojenler
   "buz kuralları"na göre yerleştirilir (her O'da 2 H, her O–O çizgisinde tam 1 H).
2. **Çizim.** Her göz için ayrı, gri tonlu çubuk-top resmi çizilir. Çizim piksel başına ışın–küre ve ışın–silindir
   kesişimiyle, derinlik tamponuyla yapılır (3×3 üst örnekleme); kesişen çubuklar ve örtüşen küreler kendiliğinden
   doğru çıkar. Küreler yumuşak gölgelidir, kenara doğru koyulaşır; harf, kürenin ön yüzüne ve yalnız o kürenin
   görünen piksellerine basılır.
3. **Neden gri?** Renkli atom anaglifte iki göze farklı parlaklıkta görünür (retina rekabeti: resim titreşir). Elementler
   boy, ton ve harfle ayrılır (H küçük ve açık, C koyu, Cl büyük ve açık, Na küçük ve koyu).
4. **Sayım dili.** Kristallerde bir tanecik **koyu**, ona bağlı çubuklar **kalın** çizilir: kalın çubuk sayısı komşu
   sayısıdır (6, 4, 3, 4). Aynı dil düz resimde de geçerlidir.
5. **Anaglif.** `R = sol göz resmi`, `G = B = sağ göz resmi`, zemin beyaz. Gözlük: **sol göz kırmızı, sağ göz
   camgöbeği**. Kâğıtta sol gözün resmi camgöbeği mürekkeple, sağ gözünki kırmızı mürekkeple basılmış olur: kırmızı cam
   kırmızı baskıyı kâğıttan ayırt edilmez yapar, camgöbeği baskıyı koyu gösterir; camgöbeği cam tersini yapar.
6. **Düz resim.** Aynı koordinatlardan, aynı görünümde, kitabın atom renkleriyle (`renkler.ATOM`) tek bakışlı resim.
   Gözlüğü olmayan ve fotokopiyle çalışan öğrenci için.
7. **Sayfa.** PNG'ler `<img>` ile, milimetre ölçüsüyle konur (`{{ana|ch4}}`, `{{duz|ch4}}`). Anaglifin çevresi beyaz,
   etiketler mürekkep rengi, kutup çipleri siyah-beyaz; kırmızı ve camgöbeği yalnız gözlük sayfasındadır.

## 2. Stereo parametreleri

**Eksenler:** x sağa, y yukarı, z okuyucuya. **Sıfır paralaks düzlemi** (kâğıt) yapının derinlik ortasıdır: yapının ön
yarısı kâğıdın önünde, arka yarısı kâğıdın arkasında görünür; kartın çerçevesi kâğıt düzleminde durduğu için göze
dayanak olur.

**Kaydırma:** sol göz `x' = x + k·z`, sağ göz `x' = x − k·z`. Yakın parça (z > 0) çapraz ayrıklık alır: sol gözün resmi
sağda kalır, parça kâğıttan dışarı çıkar. Kaydırma, ışın yönü `d = (∓k, 0, 1)` olarak uygulanır; böylece küre yüzeyindeki
her nokta kendi derinliğine göre kayar ve gölgelendirme iki gözde yüzeye yapışık kalır.

**k nasıl seçildi?**

| Sabit | Değer | Gerekçe |
|---|---|---|
| göz aralığı *e* | 62 mm | ergen ve yetişkin ortalaması (58–65 mm) |
| okuma uzaklığı *D* | 375 mm | kitap için 35–40 cm'nin ortası |
| `K_ORTO = e / (2D)` | **0,0827** | bu değerde derinlik gerçek oranında görünür (1 mm derinlik = 1 mm çıkma) |
| ayrıklık üst sınırı | **3,0 mm** | en yakın noktada iki resim arası toplam kayma; 375 mm'den 27,5 açı dakikası |

`k = min(K_ORTO, 3,0 mm / (2 · en yakın noktanın kâğıda uzaklığı))`. Yani derinlik hiç abartılmaz; yapı derinse
derinlik **sıkıştırılır**. Üst sınır 3 mm çünkü: (a) kâğıt gözlükte ayrıklık büyüdükçe hayalet görüntü (öbür gözün
resminin sızması) belirginleşir; (b) göz kâğıda odaklanırken kâğıdın önüne yakınsamak zorundadır; 27,5′, stereo görüntülerde yaygın kullanılan
1° rahatlık sınırının yarısından azdır; (c) 3 mm, harf ve küçük atom boyundan küçüktür, gözlüksüz bakışta resim okunur kalır.
Algılanan çıkma `D·p / (e + p)` (p: toplam ayrıklık): moleküllerde 11–17 mm; sayfadaki "öndeki atomlar kâğıttan
1–2 cm dışarı çıkar" cümlesi buradan.

| Resim | Basılı boyut | Ölçek | k | En yakın nokta | Toplam ayrıklık | Derinlik oranı |
|---|---|---|---|---|---|---|
| CH₄ | 55 × 40 mm | 1 Å = 15 mm | 0,0827 | 16,9 mm | 2,79 mm | 1,00 |
| NH₃ | 55 × 40 mm | 1 Å = 15 mm | 0,0827 | 15,3 mm | 2,53 mm | 1,00 |
| H₂O | 55 × 40 mm | 1 Å = 15 mm | 0,0827 | 11,0 mm | 1,82 mm | 1,00 |
| CO₂ | 55 × 40 mm | 1 Å = 15 mm | 0,0827 | 17,3 mm | 2,87 mm | 1,00 |
| BF₃ | 55 × 40 mm | 1 Å = 15 mm | 0,0787 | 19,1 mm | 3,00 mm | 0,95 |
| NaCl | 58 × 55 mm | 1 Å = 5,5 mm | 0,0541 | 27,7 mm | 3,00 mm | 0,65 |
| elmas | 58 × 55 mm | 1 Å = 8,8 mm | 0,0545 | 27,5 mm | 3,00 mm | 0,66 |
| grafit | 58 × 55 mm | 1 Å = 5,9 mm | 0,0583 | 25,7 mm | 3,00 mm | 0,70 |
| buz | 58 × 55 mm | 1 Å = 4,6 mm | 0,0808 | 18,6 mm | 3,00 mm | 0,98 |
| gaz kutusu | 92 × 51 mm | (ölçeksiz) | 0,0471 | 31,8 mm | 3,00 mm | 0,57 |
| 22,4 L küpü + top | 78 × 49 mm | 1 cm = 1,2 mm | 0,0548 | 27,4 mm | 3,00 mm | 0,66 |
| Na⁺ hidratasyonu | 46 × 46 mm | 1 Å = 6,3 mm | 0,0804 | 18,6 mm | 3,00 mm | 0,97 |
| Cl⁻ hidratasyonu | 46 × 46 mm | 1 Å = 6,2 mm | 0,0788 | 19,0 mm | 3,00 mm | 0,95 |

"Derinlik oranı" = k / K_ORTO: 1,00 gerçek oran, 0,65 "derinlik %65'e sıkıştırıldı" demektir. Beş molekül **ortak
ölçekte** basılır (1 Å = 15 mm, 150 milyon kat büyütme) ve derinlikleri gerçek orandadır; bağ açısı (109,5° gibi) doğru
algılansın diye bu önemlidir. Kristallerde ve gaz kutusunda resim büyük tutulduğu için derinlik 0,57–0,70'e iner; resim
küçültülürse oran 1'e yaklaşır (boyut ↔ derinlik sadakati arasında seçim).

**Uyarı:** ayrıklık milimetre olarak sabitlendiği için sayfa **ölçeklenmeden** basılmalıdır. Büyütülürse (afiş,
projeksiyon) ayrıklık da büyür; o kullanım için `AYRIKLIK_UST_MM` küçültülüp resimler yeniden üretilir.

## 3. Sayfalar

| s. | Sayfa | Palet · künye | İçerik | Dikkat görselleri |
|---|---|---|---|---|
| 1 | **Moleküllerin gerçek şekli** | 9 · Yol 6 Tuz Gölü–Aksaray · 5. durak | CH₄ düzgün dörtyüzlü 109,5° · NH₃ üçgen piramit ≈ 107° · H₂O kırık doğru 104,5° · CO₂ doğrusal 180° · BF₃ düzlem üçgen 120°. Her kartta büyük anaglif, küçük düz resim, şekil adı, açı, polar/apolar ve tek cümle gerekçe. "Şekil polarlığı nasıl belirler?" kartı: düz CH₄ çizimi (90° izlenimi) ve bağ çekişi okları | Kilit Bilgi · Dikkat! · Kendini dene |
| 2 | **Kristalin içine gir** | 9 · Yol 9 Mardin–Midyat · 4. durak | NaCl (6 komşu) · elmas (4) · grafit (3, tabakalar arası kesik çizgi) · buz (4 hidrojen bağı, boşluklu altıgen örgü). Her kartta komşu sayısı büyük rakamla; koyu tanecik + kalın çubuk sayım dili | Altın Kural · Unutma! · Sınav Radarı |
| 3 | **Tanecikler üç boyutta** | 10 · Yol 4 Kapadokya · yan yol | gaz kutusu (8 N₂ + 2 O₂, üç boyutta rastgele yönler, hareket izleri) · 22,4 L'lik küp (kenar 28,2 cm) ve 5 numara futbol topu (≈ 4 top) · Na⁺ ve Cl⁻ çevresinde hidratasyon kabuğu | Kilit Bilgi · Sınav Radarı · Dikkat! |
| 4 | **3B gözlüğünü hazırla** | 9 · ek | nasıl çalışır (üstten bakış şeması) · gerçek ölçüde kesme şablonu (SOL = kırmızı, SAĞ = camgöbeği; 5 cm ölçü çizgisi) · yapılışı · kullanım ipuçları · iki testli "Doğru taktın mı?" kartı · fotokopi notu | Dikkat! · Unutma! · Hap Bilgi |

Gözlük testi: **Test 1** tek gözle (SOL yazısı yalnız sol göz resminde, SAĞ yazısı yalnız sağ göz resminde);
**Test 2** iki gözle (A dairesi +2,4 mm çapraz ayrıklıkta önde, B dairesi −2,4 mm'de arkada). Gözlük ters takılırsa
ikisi de ters sonuç verir.

## 4. Doğrulama (`uretec/dogrula.py`, 177 denetim)

* **Bağ açıları** koordinatlardan, hem kurulduğu hâliyle hem sayfadaki döndürülmüş görünümde (CH₄'te 6 açının hepsi).
* **Polarlık:** bağ çekişlerinin vektör toplamı (CH₄, CO₂, BF₃ sıfır; NH₃, H₂O sıfır değil); kartlardaki etiketler.
* **Komşu sayıları** geniş örgüden: NaCl 6 (hepsi zıt yüklü), elmas 4 (açılar 109,5°), grafit 3 (120°, tabaka arası
  3,35 Å), buz 4 (dörtyüzlü). **Yoğunluklar örgüden:** NaCl 2,16 · elmas 3,52 · grafit 2,27 · buz 0,92 g/cm³.
* **Çizilen parçalar:** 27 iyon (13 Na⁺ + 14 Cl⁻), 18 atom / 16 bağ, 3 × 16 atom, 20 H₂O ve 27 hidrojen bağı; buz
  kuralları; kalın çubuk sayıları; kartlardaki büyük rakamlar.
* **10. sınıf:** ∛22 400 = 28,19 cm; 28,2³ ≈ 22 400; çapı 22 cm olan küre 5,58 L; 22,4 / 5,6 = 4 (kesin oran 4,02);
  22,4 L ve 24,5 L (RT/P); tanecikler arası uzaklık / tanecik boyu ≈ 9; hidratasyonda O ve H uçlarının yönü.
* **Stereo:** her resim için k, ayrıklık ≤ 3,0 mm, sıfır paralaks düzlemi ortada, 300 dpi, en yakın kürenin kayma
  işareti ve büyüklüğü (kimlik tamponundan).
* **Kanallar:** kaydedilmiş PNG'nin R kanalı sol göz resmiyle, G ve B kanalı sağ göz resmiyle birebir; sentetik
  yakın/uzak küre sahnesinde saçakların rengi ve yönü; PDF'e gömülü 15 resim PNG'lerle birebir (kayıpsız).
* **Gözlük sayfası:** test desenlerinin kanalları ve ayrıklık işaretleri; şablon ölçüleri (154 mm, pencereler 44 × 27 mm,
  merkezler 62 mm, saplar 125 mm, 5 cm çizgisi); şema ve Pamuk'un gözlüğünde sağ–sol.
* **Baskı kuralları:** Type 3 font 0, CSS filter yok, konturlu SVG yazısı yok, fontlarda olmayan simge yok.

Ayrıca iki göz resmi ayrı ayrı (R ve G kanalı) gözle incelendi: her biri temiz, eksiksiz bir gri resim.

## 5. Kullanılan bilgiler ve güven

| Bilgi | Kaynak / denetim | Güven |
|---|---|---|
| CH₄ 109,5° · H₂O 104,5° · CO₂ 180° · BF₃ 120° | geometri + standart değerler; koordinatlardan yeniden hesap | yüksek |
| NH₃ ≈ 107° (ölçüm 106,7°) | standart değer; sayfada "≈" ile | yüksek |
| polar: NH₃, H₂O · apolar: CH₄, CO₂, BF₃ | simetri; vektör toplamı | yüksek |
| NaCl 6:6 koordinasyon, Na⁺–Cl⁻ 2,82 Å, 801 °C | kaya tuzu yapısı (a = 5,64 Å); erime noktası kaynak değeri (800,7 °C) | yüksek |
| elmas: 4 komşu, 109,5°, C–C 1,54 Å, elektriği iletmez | a = 3,567 Å'dan hesap | yüksek |
| grafit: 3 komşu, C–C 1,42 Å, tabaka arası 3,35 Å, iletir | standart değerler | yüksek |
| buz: 4 hidrojen bağı, altıgen boşluklu örgü, 0,92 < 1,00 g/cm³ | ideal altıgen örgüden 0,924 (ölçüm 0,917) | yüksek |
| yoğunluklar 2,2 · 3,5 · 2,3 g/cm³ | örgüden hesap (ölçüm 2,17 · 3,51 · 2,26) | yüksek |
| 22,4 L (NŞA) · 24,5 L (25 °C, 1 atm) | RT/P | yüksek |
| 5 numara top: çap ≈ 22 cm (çevre 68–70 cm) → ≈ 5,6 L → küp ≈ 4 top | kural değeri + küre hacmi | yüksek |
| gazda tanecikler arası uzaklık ≈ tanecik boyunun 10 katı | NŞA'da 3,3 nm / 0,36 nm ≈ 9 | orta-yüksek ("yaklaşık") |
| hidratasyon: O ucu Na⁺'ya, H ucu Cl⁻'ye döner | iyon–dipol; Na–O 2,40 Å, Cl–O 3,20 Å | yüksek (yön); **6 su çizimi temsilî** (gerçekte Na⁺ 5–6, Cl⁻ 6–7, sürekli değişir) |
| göller üstten donar çünkü buz yüzer | yaygın anlatım; suyun 4 °C'de en yoğun olması da rol oynar | orta-yüksek (basitleştirme) |
| göz aralığı ≈ 6 cm; okuma uzaklığı 35–40 cm | ortalama değerler | yüksek |

Temsilî olanlar (sayfada sayı olarak verilmez): ortaklanmamış çiftlerin iki nokta olarak yeri; buzdaki proton dizilimi
(kurallara uyan dizilimlerden biri); gaz kutusunun ölçeği (sayfada "ölçekli değil" diye yazıyor); çubuk-top modelinde
küre yarıçapları küçültülmüştür, yalnız bağ uzunlukları ve açılar ölçeklidir.

## 6. Baskı önerileri

* **Renk ayrımı (en önemli nokta).** Resimler RGB PNG olarak, kayıpsız gömülüdür. Matbaada CMYK'ya çevrilirken hedef:
  sol göz resmi **yalnız C** kalıbında, sağ göz resmi **M + Y** kalıplarında, **K boş**. Otomatik çevirme griyi K'ya
  taşırsa ya da camgöbeğine M katarsa her iki göz öbür resmi de görür (hayalet). Öneri: anaglif resimler için ayrı
  çevirme (C = 100 − R%, M = Y = 100 − G%, K = 0) ve bir **deneme şeridi**.
* **Mürekkep gerçeği.** Camgöbeği mürekkep yeşili bir miktar emer; bu yüzden sağ göz, sol gözün resmini soluk olarak
  görebilir. Ayrıklığın 3 mm ile sınırlı ve tonların gri olması bunu azaltır ama sıfırlamaz. Ofsette sonuç genellikle
  ev yazıcısından iyidir.
* **Kâğıt.** Beyaz, mat kuşe ya da iyi 1. hamur. Parlak kâğıt lamba yansıması yapar; sarımsı kâğıt mavi-yeşil kanalı
  zayıflatır.
* **Çakışma.** C ile M/Y kalıpları arasında 0,1–0,2 mm yatay kayma zararsızdır (ayrıklık zaten 3 mm). **Düşey** kayma
  göz yorar; 0,2 mm'nin altında tutulmalı.
* **Okul yazıcısı.** "En iyi kalite / fotoğraf" kipi, "gerçek boyut" (ölçekleme yok). Mürekkebi azalmış kartuşla
  basmayın: renklerden biri soluksa o gözün resmi kaybolur.
* **Gözlük.** Standart kırmızı–camgöbeği kâğıt gözlük (kırmızı solda). Hazır kâğıt gözlük çok ucuzdur ve filtreleri
  asetattan iyidir; öneri, kitabın arka kapağına bir gözlük iliştirmek, kesme şablonunu yedek olarak tutmak.
* **Ekran.** Anaglifler telefonda ve tahtada da çalışır (ekran renkleri mürekkepten saftır); sayfa ölçeklenirse §2'deki
  uyarı geçerlidir.
* **Fotokopi.** Siyah-beyazda iki resim aynı griye döner; 3B olmaz, resim çift görünür. Fotokopi varyantında anaglif
  gizlenip düz resim büyütülmelidir (aşağıda).

## 7. Onaylanırsa ortak kütüphanede ne değişir

* `yerel-ortak/cizim/uc_boyut.py`: motor aynen taşınır. `cizim/molekul.py`'deki `_geometri` ile birleştirilirse kitabın
  SVG molekülleri ve anaglifleri **aynı koordinatlardan** çıkar (tek doğruluk kaynağı). `renkler.ATOM`'a F eklenir.
* `kur_ortak.py`: `{{ana|ad}}` ve `{{duz|ad}}` yer tutucuları; ünitenin `kur.py`'si kurulumdan önce `gorsel/` altına
  PNG'leri üretir (yapı listesi `meta.json`'da `"uc_boyut": [...]`; değişmeyen resim yeniden çizilmez).
* `stil.css`: `.kart.ub` ailesi (anaglif kartı, `.ub-serit`, `.kutup`, `.duz-et`), `.kf` (büyük harfli etikette formül
  korunur). Kural: anaglif kartında renkli etiket yok.
* `html.fotokopi` kuralları: `img.ana { display: none }`, `img.duz` büyür; öğretmen ve baskı varyantları etkilenmez.
* `dogrula_ortak.py`: `aci`, `komsu_sayisi`, anaglif kanal denetimi, "PNG mm ölçüsü = piksel / 300 dpi" denetimi.
* `yerel-cerceve/`: gözlük sayfası her kitabın ekine girer; içindekilerde 3B sayfaları küçük gözlük ikonuyla işaretlenir.
* PDF boyutu: anaglif başına 0,04–0,2 MB; ünite başına 4–8 anaglif ≈ 1 MB.

## 8. En çok hangi ünitelerde işe yarar

**9. sınıf**

| Ünite | 3B'de gösterilecek yapılar |
|---|---|
| 03 Atom ve yapısı | s ve p orbitallerinin biçimi (1s, 2s küre; 2pₓ, 2p_y, 2p_z üç eksende); altın levha deneyinde sapan α tanecikleri |
| 04–05 Periyodik tablo ve özellikler | tablonun üstünde yükselen 3B sütunlar: atom yarıçapı, iyonlaşma enerjisi, elektronegatiflik |
| 06 Kimyasal etkileşimler | bu örnekteki 5 molekül; NaCl'de iyonik örgünün oluşumu; metalik bağ (katyon örgüsü + serbest elektronlar); HCl, CCl₄, CH₃Cl ile polarlık karşılaştırması |
| 07 Adlandırma | çok atomlu iyonların biçimi: NH₄⁺ ve SO₄²⁻ dörtyüzlü, NO₃⁻ ve CO₃²⁻ düzlem üçgen, PO₄³⁻ |
| 08 Moleküller arası etkileşimler | su ikilisinde hidrojen bağı; HF zinciri; HCl'de dipol–dipol dizilimi; iki apolar molekülde anlık dipol (London); buz |
| 09 Katılar | bu örnekteki 4 örgü; CsCl (8 komşu); metal örgüleri (yüzey ve hacim merkezli küp, sıkı istif); kuru buz (moleküler katı); düzenli kuvars ↔ düzensiz cam |
| 10 Sıvılar | yüzeydeki molekül ↔ içteki molekül (yüzey gerilimi); sıvı su ↔ buz |

**10. sınıf**

| Ünite | 3B'de gösterilecek yapılar |
|---|---|
| 01 Kimyasal değişimler | tepkime öncesi ve sonrası moleküller (CH₄ + 2O₂ → CO₂ + 2H₂O); kalsit örgüsü |
| 02 Mol kavramı | "1 mol ne kadar yer tutar?": yan yana küpler: su 18 mL (kenar 2,6 cm), tuz 27 cm³ (3,0 cm), demir 7,1 cm³ (1,9 cm), gaz 22,4 L (28,2 cm) |
| 03 Stokiyometri | 2H₂ + O₂ → 2H₂O'da tanecik sayımı; sınırlayıcı bileşen kutusu |
| 04 Gazlar | gaz kutusu; Boyle (aynı tanecik, yarı hacim); difüzyon (iki gazın karışması); 22,4 L küpü |
| 05–06 Çözeltiler | hidratasyon kabukları; NaCl kristalinin köşesinden kopan iyon; şekerin moleküler çözünmesi; derişik ↔ seyreltik kutular |

En büyük kazanç **06, 08 ve 09**'da: şekil, komşuluk ve boşluk kavramları düz çizimde kaybolan bilgilerdir.

## Bilinen sorunlar ve sınırlar

* **Deneme baskısı yapılmadı.** Hayalet görüntünün düzeyi, 3 mm ayrıklığın rahatlığı ve asetat filtrelerin yeterliliği
  ancak kâğıt üzerinde görülebilir (aşağıdaki liste).
* **Derinlik sıkışması:** kristallerde ve gaz kutusunda 0,57–0,70 (§2). NaCl küpü olduğundan biraz yassı algılanabilir.
* **Kalabalık örgüler:** NaCl (27 iyon) ve buz (60 atom) gözlüksüz bakışta karışıktır; derdi zaten 3B'de çözülmek.
  Küçük düz resimler (24 × 23 mm) bu ikisinde fotokopi için sınırda kalır; fotokopi varyantında büyütülmeli.
* **Harfler:** elmas ve grafitte atomlara harf konmadı (hepsi C; öndeki bağ harfi yarı örtüyordu). Buzda yalnız seçili
  O harflidir; H'ler küçük açık kürelerdir. Bazı arka atomların harfi öndeki atomun arkasında kalır (doğal örtüşme).
* **Künyeler geçici:** 9/06 ve 9/09 üniteleri henüz yazılmadı; durak adları (Hasan Dağı, Mardin çarşısı), nişanlar,
  akçe ve sayfa numaraları örnektir. s.3 Gazlar ünitesine "yan yol" olarak iliştirildi; hidratasyon kutusu aslında
  Çözeltiler'e aittir ("Sıradaki yol" çipiyle belirtildi).
* **İki HTML, bir PDF:** paletler HTML başına uygulandığı için PDF birleştirme yapılır; fontlar iki kez gömülür.
* **Varyantlar yok:** fotokopi, öğretmen ve baskı (taşma paylı) varyantları üretilmedi.
* **Herkes göremez:** iki gözle derinlik algısı zayıf olan öğrenciler etkiyi göremeyebilir (sayfada not var). Renk
  görme farklılıklarında anaglifin nasıl algılandığı denenmedi.
* **Pamuk'un gözlüğü aynalı görünür:** Pamuk bize baktığı için kırmızı cam resimde sağdadır (doğrusu bu). Karışıklık
  olursa banttaki Pamuk gözlüksüz çizilebilir.
* Sahne bantları (Tuz Gölü–Hasan Dağı, Mardin) bu örnek için çizildi, temsilîdir; üniteler yazılırken yenilenir.

## Fiziksel deneme baskısı gerektirenler

1. Renkli lazer, mürekkep püskürtmeli ve ofset provada **hayalet** düzeyi (özellikle sağ gözde camgöbeği sızıntısı).
2. **3 mm** üst sınırın 9. sınıf öğrencisinde rahatlığı; gerekirse 2,5 mm (tek sabit: `AYRIKLIK_UST_MM`).
3. Gri tonların baskıda ayrışması: Na⁺ / Cl⁻, C / H, seçili koyu tanecik; kalın ↔ ince çubuk farkı.
4. Kırtasiye **asetatıyla** yapılan gözlüğün yeterliliği (tek kat mı, çift kat mı) ve hazır kâğıt gözlükle karşılaştırma.
5. **Test 1 ve Test 2**'nin sınıfta işe yaraması (ters takan öğrenci gerçekten fark ediyor mu).
6. Şablonun **gerçek ölçüsü** (5 cm çizgisi) ve kartona yapıştırılınca burna oturması.
7. CMYK ayrımı: C / M+Y / K boş ayrımının matbaa iş akışında uygulanabilirliği.
8. Siyah-beyaz fotokopide düz resimlerin okunurluğu.
