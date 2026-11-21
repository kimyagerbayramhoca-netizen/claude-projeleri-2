# Yeni fikirler örneği · baskıya özgü dört özellik

Kimya Rotası için kâğıtta çalışan dört yeni özelliğin örneği: **Usturlap Çarkı** (iki diskli volvel: önde element bulucu,
arkada mol çarkı), **Gizli cevap** (3B gözlüğün kırmızı camıyla okunur), **Kâğıtta animasyon** (asetat perdeyle oynayan
geçmeli resim) ve **Ustanın Sırrı** (ebrunun kimyası). Paletler: 9. sınıf "Çini ve Toprak", 10. sınıf "Göl ve Rasathane".

```
python3 uretec/kur.py       # 2 HTML → render.js (PDF + PNG + taşma) → yeni-fikirler-ornek.pdf → önizlemeler (≈ 2 dk)
python3 uretec/dogrula.py   # 242 denetim → "SONUÇ: hepsi doğru"
```

Ortak dosyalara, ünitelere, `yerel-cerceve`'ye ve öbür `gelistirme` klasörlerine dokunulmadı. `karma-temalar/uretec`
(tema, konu karakterleri, karma.css), `atom-modelleri/uretec` (gelistirme.css, hap_bilgi) ve
`yerel-cerceve/uretec/elementler.py` salt okunur içe aktarılır.

## Çıktılar ve yapraklar

| Sayfa | Palet | İçerik | Yaprak |
|---|---|---|---|
| 1 | Çini ve Toprak | Usturlap Çarkı · kesme yaprağı **ön** (P ve Q diskleri, kesme çizgileri, kurulum adımları) | 1. yaprak ön (kesilir) |
| 2 | Göl ve Rasathane | Usturlap Çarkı · kesme yaprağı **arka** (mol çarkı ölçekleri, çözümlü örnek, baskı notu) | 1. yaprak arka |
| 3 | Çini ve Toprak | Gizli cevap: 6 soru + deneme şeridi + "kendi gizli cevabını yap" | 2. yaprak ön |
| 4 | Çini ve Toprak | Ustanın Sırrı · ebru (Kendini dene, Hap Bilgi, Bir bakışta) | 2. yaprak arka |
| 5 | Göl ve Rasathane | Kâğıtta animasyon: iki geçmeli resim, 6 karelik öykü şeridi | 3. yaprak ön (arkası boş ya da ünite sayfası) |
| 6 | (yalnız siyah) | Asetat perde | **ayrı şeffaf asetat** |

`onizleme/`: `s01–s06.png` · `usturlap-on.gif`, `usturlap-arka.gif` (kesilip birleştirilmiş çark döner) ·
`usturlap-on-Al.png`, `usturlap-arka-ornek.png` · `gizli-once-sonra.png`, `gizli-mercek.gif` · `animasyon-gaz.gif`,
`animasyon-tuz.gif`, `animasyon-temizlik.json`. Bütün benzetimler basılacak PDF'in kendisinden (pdftoppm) üretilir.

**Baskı notları:** Çift taraflı, **uzun kenardan çevirme**, ölçeklemeden (%100), renkli. 1. yaprak 160–200 g/m² kâğıda
basılırsa çark dayanıklı olur. Sayfa 6 şeffaf asetata (lazer için lazer asetatı, mürekkep püskürtmeli için inkjet asetatı).
Fotokopide gizli cevap çalışmaz (bütün mürekkepler griye döner); geçmeli resim siyah-beyazda da oynar, renkler kaybolur.
PDF 3,9 MB, Type 3 font yok.

## 1. Usturlap Çarkı (sayfa 1–2)

**Mekanik.** P (R 75,5 mm, "anakap") altta, Q (R 58 mm + tepede kürsü) üstte; merkezden çatal çivi (20 mm). Kürsüden
tutulur, P kenarından çevrilir; seçilen element önde, sonuç (n) arkada **hep tepededir**. Arka yüzde P üstte kalır:
Q'nun M ölçeği P'deki **halka yarıktan** (r 48–55 mm) görünür. Yarığı üç ince köprü (2 mm) tutar; köprüler dış ölçekte
1,3 · 2,6 · 6,6'nın hizasındadır (ölçeğin %1,9'u). İki yüz ayna yerleşimlidir (x → 210 − x); köprüler iki yüzde aynı yerde.

**Ön yüz (9. sınıf), Z = 1–20.** Kürsü penceresi: Z, simge, Türkçe ad. Doğu penceresi: katman dizilimi (2·8·…) ve yaygın
iyon. Batı penceresi: periyot ve grup (IUPAC). Kenar halkası 20 elementi her an gösterir (seçmek için); sektörler metal,
ametal, yarı metal, soy gaz renginde. Her pencere bir halka bandını kullanır (bant başına bir pencere: 18°'lik adımda
komşu içerik pencereye girmez). Veri `elementler.py`'den; iyon kuralı klasik 9/06–9/07 ile aynı: 1, 2 ve 13. grup
metalleri +, 15–17. grup ametalleri −, H⁺ ve H⁻ (hidrür), soy gaz iyon yok.
**Seçilen kural (C, Si, B):** iyon yazılmaz, ortak bağ sayısı yazılır (C ve Si "4 bağ", B "3 bağ"); C⁴⁻ (karbür) yalnız
birkaç bileşikte görülür. Kural sayfa 1'de ve Q'nun üstünde yazılı.

**Arka yüz (10. sınıf), mol çarkı.** İki ölçek θ(x) = 360°·log10(x), bir onluk; arkadan bakana göre saat yönünde.
Dış ölçek (P): m ve n; iç ölçek (Q, yarıkta): M; kırmızı ok M = 1'de. Kullanım: M'yi m'nin hizasına çevir, ok n'yi
gösterir; virgül kaba hesapla konur. Çözümlü örnek (P'nin ortasında): 53 g göl sodası Na₂CO₃ (2·23 + 12 + 3·16 = 106):
dışta 5,3 ↔ içte 1,06 → ok 5,0 → 53/106 ≈ 0,5 → **n = 0,5 mol**. İç ölçekte sarı çizgiler: CH₄ 16, H₂O 18, O₂ 32,
CO₂ 44, NaCl 58,5, soda 106. Deneme: "1'i 1'e, 5'i 5'e getir, ok iki kez de 1'i göstermeli" (dışmerkezliği yakalar).

**Kurulum (sayfa 1):** 1 diskleri makasla kes · 2 üç pencereyi ve halka yarığı maket bıçağıyla çıkar, köprüleri kesme ·
3 merkezleri del · 4 Q'yu üste koy, çatal çiviyi P'nin arkasından tak, bacaklarını öne aç.

## 2. Gizli cevap (sayfa 3)

Cevap **%35 camgöbeği** (yalnız C). Aynı yere aynı yazı tipi ve boyda **üç çeldirici cevap** (kırmızı, turuncu, macenta:
yalnız M ve Y) ve açık bir harf konfetisi basılır. Kırmızı cam (3B gözlüğün sol camı) M ve Y'yi kâğıt gibi açık, C'yi
koyu gösterir: yalnız doğru cevap kalır. Gerçek cevabın altındaki M (gerekirse) azaltılarak çıplak gözdeki parlaklığı
çevresine eşitlenir; bu R kanalını neredeyse değiştirmez. Kutu 72 × 15 mm, 400 dpi PNG. Sorular çarkın ön yüzüyle
çözülür ("Çarkta: doğu penceresi…"); yanlış cevaplar "Çeldirici avı" kartında hata türüne bağlanır.

**Ölçü (seçicilik).** Her aday yazı için yalnız ona ait pikseller ile zemin arasındaki karşıtlık (zemin standart sapmasıyla).
Kırmızı cam = R kanalı (gri); çıplak göz = CIELAB L*, a*, b*. Sonuç (7 kutu, `gorsel/gizli-olcum.json`):

| | eşik | ölçülen |
|---|---|---|
| Camla gerçek cevabın karşıtlığı | ≥ 3 | 7,2–8,2 |
| Camla gerçek / en güçlü çeldirici | ≥ 3 | 3,0–7,0 (deneme şeridi 3,0) |
| Camla Weber karşıtlığı | ≥ 0,25 | 0,30–0,32 |
| Çıplak gözle gerçek / en güçlü çeldirici (L*, a*, b*'nin en büyüğü) | ≤ 1 | 0,29–0,78 |

Yani çıplak gözle doğru cevap üç çeldiricinin hiçbirinden belirgin değildir (göz çoğu kutuda bir çeldiriciyi okur:
"2·8·4", "19 elektron", "O · karbon"); camla doğru cevap tek başına kalır. `gizli-once-sonra.png` sayfanın kendisini iki
görünümde gösterir.

## 3. Kâğıtta animasyon (sayfa 5–6)

N = 6 kare, şerit (yarık) **0,6 mm**, çubuk 3,0 mm, dönem 3,6 mm; resim 180 mm = 50 dönem. Kareler SVG clipPath ile
vektör olarak iç içe basılır; perde sağa 0,6 mm kaydıkça sıradaki kare görünür. Dört hizalama artısı sayfa ve asetatta aynı.

* **Gaz tanecikleri (Yol 4 · Gazlar):** aynı kapta 8'er tanecik. Soğukta 4'lü sıralar (kare başına 4,5 mm), sıcakta 2'li sıra
  ve sütunlar (7–11 mm). Her dönüş bir duvara ya da komşu taneciğe değerken olur (esnek çarpışma); sıcakta duvar
  vuruşu dönem başına 8, soğukta 4 (basınç büyük). Hiçbir karede tanecikler üst üste binmez (en küçük boşluk 0,7 mm).
* **Tuz suda çözünüyor (Yol 5 · Çözeltiler):** köşedeki Na⁺ ve kenardaki Cl⁻ kristalden ayrılır; 4'er su molekülü sarar:
  Na⁺'ya O ucuyla, Cl⁻'ye H ucuyla. Kristalde her iyonun komşusu zıt yüklü; Cl⁻ > Na⁺ (ölçekli değil). Çakışma yok.

**Perde benzetimi (PDF'ten, 423 dpi; bir şerit = 10 piksel):** hizalıyken her 6 karede görünen mürekkep doğru kareyle
örtüşür (IoU gaz 0,87–0,96, tuz 0,92; başka karelerden sızıntı en çok %2,2). 0,12 mm kaymada doğru kare yine baskın,
sızıntı %4–10. GIF'lerde üstte asetat altından görünüm, altta yalnız yarıklardaki şeritler.

## 4. Ustanın Sırrı · ebru (sayfa 4, 9. sınıf, Yol 10 Sıvılar)

Kurgusal **Revnak Usta** (gerçek bir kişiye benzetilmedi) çırak Elif'e üç sırrı anlatır; Ahilik bağı: çırak ustasının
yanında çalışarak öğrenir. Kitreli su (viskozite), öd (yüzey gerilimi), toprak boya (çözünmezlik) birer şemayla;
Kendini dene (3 soru, ters cevap), Hap Bilgi ("yüzey aktif madde yüzey gerilimini düşürür"), Bir bakışta, UNESCO kartı.

**Doğrulanan bilgiler (WebSearch, standart, 3 arama):**

| Bilgi | Güven | Kaynak |
|---|---|---|
| "Ebru, Turkish art of marbling" 2014'te (9.COM) UNESCO Temsilî Listesi'ne alındı; Türkçe adıyla Geleneksel Türk Ebru Sanatı | yüksek (Türkçe ad: orta-yüksek) | ich.unesco.org/en/RL/ebru-turkish-art-of-marbling-00644 · karar 9.COM 10.44 · yakegm.ktb.gov.tr |
| Tekne suyu kitreyle (kitre zamkı) koyulaştırılır; koyuluk boyayı yüzeyde tutar | yüksek | en.wikipedia.org/wiki/Paper_marbling · ktb.gov.tr/EN-98711/marbling.html · MEB Ebru I ders kitabı |
| Boyaya öd (sığır ödü) katılır; yüzey aktif madde olarak yüzey gerilimini düşürür; ödsüz boya yayılmaz, batar | yüksek | Paper marbling (Wikipedia) · dergipark makaleleri |
| Geleneksel boyalar suda çözünmeyen doğal pigmentlerdir (toprak, taş, bitki kökenli) | yüksek | MEB Ebru I ders kitabı · muslimheritage.com |
| Ebru ustadan çırağa aktarılır | orta-yüksek | UNESCO dosyası (arama özeti) |

ich.unesco.org bu oturumun ağında açılamadı (WebFetch); doğrulama arama sonuçlarıyla yapıldı. **Bırakılanlar** (tek
kaynak ya da doğrulanamadı): kitre/su oranı, kitrenin iki gün önceden hazırlanması, ezme taşının adı, fırçanın gül dalı
ve at kılından olması, "renkler birbirine karışmaz", karabiber–deterjan deneyi, UNESCO'daki "yağlı su" ifadesi.

## Denetim (`uretec/dogrula.py`, 242/242)

A element verisi, dizilim, periyot/grup, iyon kuralı, dönme açıları, pencerelere sığma (fontTools), delik geometrisi ·
B basılı her çentik 360°·log10(x) açısında (< 0,01°); 2000 rastgele (m, M) çiftinde basılı çentiklerden okunan n = m/M
(en büyük hata **%0,05**); örnek ve sarı çizgiler; köprüler; ayna yerleşim; 1 mm dışmerkezlikte en büyük hata %0,69 ·
C cevaplar veriden, çeldiriciler yanlış, ölçüler PNG + maskelerden · D şerit ve yarık geometrisi, çakışma, çarpışma
nedenleri, hidratlaşma yönleri, perde benzetimi · E ebru bilgileri · F tırnaklı Baloo adı, fontta olmayan glif yok
(δ satır içi SVG çizildi) · G 6 sayfa A4, Type 3 = 0, render.js taşma yok.

## Fiziksel deneme gerekenler

1. **Çark:** çift taraflı baskıda iki yüzün çakışması (±1 mm'de dışmerkezlik, ön yüz pencere payları 0,5–1,7 mm);
   öğrencinin yarığı ve pencereleri maket bıçağıyla kesebilmesi; köprülerin ve kürsünün dayanıklılığı (kâğıt gramajı);
   çatal çivinin sıkılığı (P dönerken Q kaymamalı); gerçek çarkla mol hesabının doğruluğu (deneme: 1↔1, 5↔5).
2. **Gizli cevap:** yazıcı sürücüsü macenta/kırmızıya C ya da K katarsa çeldiriciler camdan da görünür; okul yazıcısında,
   lazerde ve ofset provada denenmeli. Kâğıt gözlüğün kırmızı camıyla gerçek okunurluk (Weber ≈ 0,32 hesaplandı);
   öğrencilerin çıplak gözle doğru cevabı seçip seçemediği. Ofsette cevap yalnız C, çeldirici yalnız M+Y kalıbına ayrılmalı.
3. **Animasyon:** asetatta çubukların tam opak çıkması; 0,6 mm yarığın elle hizalanması ve akıcılığı; küçük eğiklikte
   hare (moiré) bantları; lazer ve inkjet asetat karşılaştırması.
4. **Ebru:** içerik öğretmen gözüyle; isterse sınıfta kitreli su + ödlü boya gösterisi.

## Bilinen sınırlar

* Sayfa sayısı 6 (5 kâğıt + 1 asetat). Kesme yaprağındaki kurulum adımları kesimden sonra artık kâğıtta kalır.
* P'nin arka yüzündeki talimat ve örnek P ile birlikte döner; ok tepeye geldiğinde okunur durumdadır.
* Bir köprü oku kapatırsa (n'nin mantisi 1,3, 2,6 ya da 6,6 civarı) sonuç kürsünün arkasındaki kırmızı uzantıyla okunur.
* Gizli cevap PNG'leri RGB'dir; benzetim ideal mürekkep modeliyle yapıldı (C, M, Y dolu katsayıları ofsete yakın).
* GIF'lerdeki "çubuksuz" görünüm bir yaklaşımdır (her dönemde yarığın ortası uzatılır).
* Ortak koddan gelen rozet SVG'sinde Baloo adı hâlâ tırnaksız (bilinen ortak hata; bu klasörde düzeltilmedi).
  Ortak stillerdeki `.ic`, `.etiket`, `.kim` sınıflarıyla çakışmamak için bu klasör `gz-ic`, `gz-etiket`, `sir-kim` kullanır.

## Dosyalar

`uretec/usturlap.py` (disk geometrisi, dört yüz, kesme çizgileri, benzetim maskeleri) · `gizli.py` (cevap kutuları, ölçü,
önizleme) · `animasyon.py` (kareler, geçme, perde, kare temizliği, GIF) · `usta.py` (Revnak Usta, sır şemaları) ·
`olcu.py` (fontTools ile yazı genişliği) · `onizle.py` (çark benzetimi) · `kur.py` · `dogrula.py` · `yeni.css` ·
`sablon9.html`, `sablon10.html` · `s9/`, `s10/meta.json` (künye) · `gorsel/` (gizli cevap PNG'leri, maskeler, ölçüler,
temalı ebru dokuları).
