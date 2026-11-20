# Katla örneği · baskıya özgü sayfalar

Kimya Rotası için kâğıtta çalışan özellikler: iki **katlamalı sayfa** ("Katla, bağ oluşsun" ve "Katla, tepkime olsun"),
bir **karma sayfa** (Şifreli Kapı, Çeldirici Röntgeni, Robot yanıldı mı?, Heybe, Nineme Anlat), **köşe sineması**
(24 karelik çizgi film) ve **köşeyi katla** (cevap arka yüzün köşesinde).

```
python3 uretec/kur.py       # HTML → PDF + PNG + taşma denetimi → katla-ornek.pdf → önizlemeler
python3 uretec/dogrula.py   # 177 denetim → "SONUÇ: hepsi doğru"
```

## Çıktılar

| Dosya | İçerik |
|---|---|
| `katla-ornek.pdf` | 6 sayfa, çift taraflı basılacak sırada (aşağıdaki tablo) |
| `onizleme/s01–s06.png` | sayfaların PNG'leri |
| `onizleme/acik-katli-s1.png`, `-s2.png` | kat sayfası açık · katlı · katlı fotokopi (gri) yan yana |
| `onizleme/katlama-s1.gif`, `-s2.gif` | orta şeridin kapanışı (telefonda bakmak için) |
| `onizleme/kose-katli.png` | köşeyi katla: ön yüz köşesi · arka yüz köşesi · katlanınca (benzetim) |
| `onizleme/kose-cizgi-filmi.gif`, `-serit.png` | köşe sinemasının 24 karesi |

| Sayfa | Palet | İçerik | Yaprak |
|---|---|---|---|
| 1 | Çini ve Toprak | Katla, bağ oluşsun (9. sınıf, Yol 6) | 1. yaprak ön |
| 2 | Çini ve Toprak | Karma sayfa | 1. yaprak arka |
| 3 | Göl ve Rasathane | Katla, tepkime olsun (10. sınıf, Yol 1) | 2. yaprak ön |
| 4 | Göl ve Rasathane | Köşe sineması (24 kare) | 2. yaprak arka |
| 5 | Göl ve Rasathane | Köşeyi katla: hızlı görev (ön) | 3. yaprak ön |
| 6 | Göl ve Rasathane | Köşenin sırrı (arka; cevap sol alt köşede) | 3. yaprak arka |

## 1. Katlamalı sayfa (Mad dergisi "fold-in" fikri)

**Mekanik.** İki dikey kat çizgisi var: A (soldan 70 mm) ve B (140 mm). A ve B'den arkaya kat izi yapılır, orta şerit
(70–140 mm) arkaya itilir, A çizgisi B çizgisine değer. Sol parça (0–70) ile sağ parça (140–210) yan yana gelir.
Dört satır aynı iki çizgiyi kullanır: tek katlama dördünü birden tamamlar. Kâğıt üç kat çizgisiyle düzleşir:
A ve B "dağ", orta (105 mm) "vadi". Ciltli kitapta da olur: orta şerit sayfanın arkasına, iki yaprağın arasına girer.
Alternatif (Mad yöntemi): sayfayı ortadan (105 mm) öne katla, sonra B çizgisinden geri katla; görüntü aynıdır.

**Kurallar** (`uretec/katla_cizim.py`, `dogrula.py` denetler):

* Dikişi geçen her şey (ok, ortak çift halesi, ürün kabı, bölünmüş yazı) "katlı uzayda" tek parça çizilir ve sayfaya
  iki kez basılır: solda x ≤ 70, sağda x ≥ 140 kırpılarak. Yarımlar bu yüzden kesin hizalıdır.
* Şekiller orta şeride 1 mm taşar (±1 mm kat hatasında dikişte beyaz boşluk kalmaz). Yazı tam dikişte kesilir:
  taşma payı, bölünen harfin öbür yarısını göstermesin.
* Açık sayfada ürün okunmaz: ürün formülünün bir harfi tam dikişe ortalanır ve ikiye bölünür (Na|a|Cl → "N◖" ile "◗Cl").
  Bölünen harfin ortasında dikey gövde yoktur (a, o, e, g, C, O, H…). Bağ/tepkime türü kelimesi de bölünür.
* Dikişi geçen çizgiler kalındır (≥ 0,6 mm) ve dikişi yataya yakın keser: haleler dikişe ortalı yatay elips, aktarım
  okları dikişi tepe noktasında geçer. Dikişe komşu her öge (elektron, atom halkası) dikişten ≥ 1,2 mm uzaktadır.
  Kat çizgisi sayfanın içinden çizilmez; yalnız üstte ve altta A/B işaretleri, satır aralarında küçük üçgenler
  (hepsi orta şeritte, katlayınca görünmez).
* Satır zeminleri, çini şeridi (7 mm karo) ve sayfa zemini (14 mm desen) 70 mm'de kesintisiz sürer; alt şerit
  ebru yerine düz renk.
* Yazı genişlikleri fontTools ile fontun kendi ölçülerinden hesaplanır; SVG yazısında harf arası düzeltme ve bitişik
  harfler kapalı, `text-rendering: geometricPrecision` açık (tarayıcı ölçüsü = hesap; 26,75 mm'ye 26,76 mm).
* Renksiz de çalışır: sol atomun elektronu ●, sağ atomunki ×, boş yer kesik çember, ortak çift hale; kap renkleri
  yazıyla da söylenir ("bromtimol mavisiyle sarı"). Üçüncü önizleme paneli gri fotokopi benzetimidir.
* Orta şerit öğrencinin çalışma alanıdır: "Önce tahmin et" (ürün, tür, ipucu) ve "Aç ve açıkla" satırları.

**Sayfa 1 · Katla, bağ oluşsun** (atom düzeyinde bağ oluşumu; Bohr halkaları, nokta–çarpı):

| Satır | Girenler | Katlayınca | Neden |
|---|---|---|---|
| 1 | ₁₁Na 2·8·1 + ₁₇Cl 2·8·7 | Na + Cl → NaCl | 1 e⁻ aktarımı: Na⁺ (10 e⁻, Ne) ve Cl⁻ (18 e⁻, Ar), iyonik |
| 2 | ₁₂Mg 2·8·2 + ₈O 2·6 | Mg + O → MgO | 2 e⁻ aktarımı: Mg²⁺ ve O²⁻ (10 e⁻, Ne), iyonik |
| 3 | ₁H + ₁H | H + H → H₂ | 1 ortak çift, her H 2 e⁻, kovalent |
| 4 | ₈O + ₈O | O + O → O₂ | 2 ortak çift (çift bağ), her O 8 e⁻, kovalent |

4. satır için su (H₂O) denendi ve bırakıldı: 104,5°'lik açıyla çizilen Bohr halkaları dikişe dik açıyla kesişiyor,
O'nun K halkası dikişin üstüne düşüyordu (kat hatasında kırık çizgiler). O₂ hem doğrusal hem de "1 ortak çift /
2 ortak çift" karşılaştırmasını tamamlıyor (iyonik satırlardaki "1 e⁻ / 2 e⁻" ile paralel).

**Sayfa 3 · Katla, tepkime olsun** (10/01 Kimyasal Değişimler duraklarından):

| Satır | Durak | Denklem | Görünüm |
|---|---|---|---|
| 1 | Pasinler | AgNO₃(suda) + NaCl(suda) → AgCl(k) + NaNO₃(suda) | beyaz çökelek |
| 2 | Ani | HCl(suda) + NaOH(suda) → NaCl(suda) + H₂O(s) | bromtimol mavisi: asitte sarı, bazda mavi, nötrde yeşil |
| 3 | Erzurum | Fe(k) + CuSO₄(suda) → FeSO₄(suda) + Cu(k) | çivi bakırla kaplanır, mavi renk solar |
| 4 | Sarıkamış | 2Mg(k) + O₂(g) → 2MgO(k) | göz alıcı beyaz alev, beyaz kül |

Büyük harf şeridi gerçek bir katlama hilesidir: açıkken girenler okunur ("Ag NO₃ + Na Cl", "H Cl + Na OH",
"Fe + Cu SO₄", "Mg + O=O"), katlayınca orta şerit gizlenir ve ürün kalır ("AgCl", "HOH", "FeSO₄", "MgO").
Gizlenen parça seyirci iyonlardır; "Aç ve açıkla" kartı bunu sorar. Pb(NO₃)₂ + KI tepkimesi kullanılmadı (kurşun zehirli).

## 2. Karma sayfa (sayfa 1'in arkası)

Sütunlar 11–67, 73–137, 143–199 mm: kat izleri (70 ve 140 mm) sütun aralığına düşer.

* **Şifreli Kapı.** Altı soru bitmiş ünitelerden aynen alındı (9/03 I1, I2, I6 · 9/04 I1, I7 · 9/01 I11; α yerine
  "alfa"). Seçenek etiketleri kod harfleridir; doğru harfler sırayla **PROTON** yazar. Yanlış harfler kelime kurmaz:
  5⁶ = 15 625 dizilimden yalnız "PRO?O?" kalıbındaki 25 dizi okunabilir (PROTOK, PROMON, PROVOR…), PROTON dışında
  hiçbiri Türkçe kelime değil; 4. konumda L, 6. konumda G yok (PROLOG kurulamaz). dogrula.py soruları, seçenekleri ve
  doğru şıkkı ünitedeki `data-dogru` ile karşılaştırır.
* **Çeldirici Röntgeni** (9/03 I4, ²⁷₁₃Al³⁺ → 13, 14, 10): A yükü unuttu (e = p), C kütle numarasını nötron saydı,
  D proton ile nötronu karıştırdı, E yükü ekledi (13 + 3). Doğru seçenek düz yeşil, çeldiriciler kesik kırmızı çerçeve
  (renksiz de ayrılır). "Sıra sende": ²³₁₁Na⁺ için çeldirici uydur.
* **Robot yanıldı mı?** Kurgusal KimyaBot'un NaCl açıklamasında tek hata: "Na⁺ … argon gibi" (doğrusu neon; 10 e⁻).
  Öbür üç cümle doğru (Na 1 e⁻ verir, Cl⁻ 18 e⁻, zıt yükler çekişir).
* **Heybe:** 1 yol önce (Yol 5) yarıçapı en büyük K · 3 yol önce (Yol 3) n = 4'te en çok 32 e⁻ · 5 yol önce (Yol 1)
  çamaşır suyu + asidik kireç sökücü → zehirli klor gazı. Cevaplar ters yazılı.
* **Nineme anlat:** öbür yüzde katlanan NaCl'yi kimya sözcüğü kullanmadan üç cümleyle anlatmak.

## 3. Köşe sineması

Elektron merdiveni (H atomu, E = −13,6/n² eV; basamaklar enerjiyle orantılı): mor ötesi foton soğurulur (1 → 3,
12,09 eV, 103 nm), elektron n = 3'ten n = 2'ye inerken kırmızı foton (1,89 eV, 656 nm), sonra n = 1'e inerken mor ötesi
foton (10,2 eV, 122 nm) yayar. Karakterler `karma-temalar` konu karakterleri (kk-elektron, kk-foton-656, kk-foton-uv).
Kitapta kare n, n. **sağ** sayfanın dış alt köşesine (14 × 14 mm, altbilginin üstü) basılır; başparmakla sayfalar
bırakılınca oynar. 24 kare = 24 sağ sayfa (48 sayfa). Örnekte 1. kare sayfa 1'de, 2. kare sayfa 3'te; sayfa 4
bütün kareleri gösterir (kat izleri kare sütunlarının arasında). Sol sayfalara ve köşesi katlanan sayfaya kare konmaz.

## 4. Köşeyi katla

Kat çizgisi ön yüzün sağ alt köşesinden a = 64 mm uzakta, 45° eğik: (W − a, H) ile (W, H − a) noktalarından geçer.
Köşe öne katlanınca arka yüzün sol alt köşesi görünür. Arka yüzdeki (x, y) noktası ön yüzde
**(W + H − a − y, H − a + x)** noktasında görünür: sayfayı çevirmek bir yansıma, kat çizgisi ikinci yansıma; ikisi
birlikte 90° dönme (ayna değil). Bu yüzden cevap arka yüzde 90° sola döndürülerek basılır (SVG: `translate(0 a)
rotate(-90)`); katlanınca düz okunur ve kat çizgisinin üstündeki üçgene oturur. Ön yüzün köşe üçgenine görev konmaz
(arkaya gider); arka yüzün sol alt köşesine sayfa numarası, altbilgi ve ebru şeridi konmaz. Hızlı görev 10/04
Gazlar'dan: −13 °C'de 2,6 L hava 27 °C'de 2,6 · 300/260 = 3 L.

## Baskı ve cilt notları

* Çift taraflı, **uzun kenardan çevirme**. 1–2, 3–4, 5–6 aynı yaprağın iki yüzüdür; katlamalı sayfa ile köşe sayfası
  hep tek sayfadan (sağ) başlamalı.
* Katlamalı sayfanın arkası da 70 ve 140 mm'den kırışır: arka yüze üç sütunlu, sütun aralıkları kat yerinde olan bir
  sayfa konur (karma sayfa, köşe sineması). Kat yerinden geçen ince çizgi, tablo ya da resim konmaz; katlıyken
  okunması gereken bir şey konmaz.
* 80 g/m² kâğıtta kat izi tırnakla keskinleştirilmeli. Ciltli kitapta kat sayfası sayfanın tamamını kullanır;
  orta şerit katlanınca sağ parça cilde 70 mm yaklaşır, cilt payı sol parçadadır.
* Yazıcı ön–arka hizası ±1–2 mm kayabilir: köşe cevabı bu yüzden kat çizgisine dayalı geniş bir üçgende.

## Fiziksel test gerekenler

1. **Kat sayfaları (1 ve 3):** A–B katı elle ne kadar doğru yapılıyor; bölünen harfler ve oklar ±1 mm'de okunuyor mu;
   kat izi kalınca sayfa yeniden düz açılıyor mu.
2. **Köşeyi katla (5–6):** çift taraflı baskıda cevap üçgeni kat çizgisine oturuyor mu (benzetim doğru, kâğıtta denenmedi).
3. **Köşe sineması:** 14 mm'lik kareler başparmakla çevrilince akıyor mu; 24 kare için 48 sayfalık bir bölüm gerekir.
4. Fotokopi: gri benzetim okunuyor; gerçek fotokopi makinesinde açık sarı/mavi kap renkleri denenmeli.

## Bilinen sınırlar

* Açık kat sayfasında ürün formülü ve tür kelimesi yarım harfle bölünür, ama "neden" satırının geri kalanı okunabilir;
  kararlı bir öğrenci yarımlardan tahmin edebilir. Tahmin, orta şeritte satırlar kapatılarak yapılır.
* Büyük harf şeridinde katlayınca "Ag Cl" gibi küçük bir boşluk kalır (harfler dikişten 0,6 mm uzakta: kat hatasında
  harf kesilmesin diye).
* Cep Hülasası (tek A4'ten 8 sayfalık cep kitapçığı) bütçe yüzünden yapılmadı.
* Ortak kütüphanede bulunan bir sorun (değiştirilmedi): SVG'lerde `font-family="Baloo Bhaijaan 2"` tırnaksız yazılınca
  "2" geçersiz CSS sayılıyor ve yazı Nunito'ya düşüyor (ör. `cizim/sus.py` durak rozeti). Bu klasörde ad tırnakla
  yazıldı: `font-family="'Baloo Bhaijaan 2'"`.

## Dosyalar

`uretec/katla_cizim.py` (kat sayfaları, çizgi film kareleri, köşe, ikonlar; ortak kütüphaneye `cizim/katla.py` olarak
taşınabilir) · `katla.css` · `sablon9.html`, `sablon10.html` · `kur.py` · `onizle.py` (pdftoppm + PIL benzetimleri) ·
`dogrula.py` · `s9/`, `s10/meta.json` (künye). Paletler ve konu karakterleri `karma-temalar/uretec`, ek bileşen
CSS'i `atom-modelleri/uretec`'ten salt okunur kullanılır; ortak dosyalara, ünitelere ve `yerel-cerceve`'ye dokunulmadı.
