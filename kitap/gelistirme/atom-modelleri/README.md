# Geliştirme örneği · Atom modelleri (seçenek kataloğu)

Bu klasör, **bütün ünitelere uygulanmadan önce** seçim yapılsın diye hazırlanmış bir örnektir. Konu: 9. sınıf Yol 3
(Şanlıurfa–Harran Yolu) ünitesinin atom modelleri sayfaları (`9-sinif-yerel/03-atom-ve-yapisi`, s.2–4). Ünitenin
doğrulanmış içeriği, sahneleri ve Medeniyetimizden bilgileri **değiştirilmeden** yeniden kullanıldı; yeni olanlar bu
klasörün `uretec/` modüllerindedir. Ortak kütüphaneye (`yerel-ortak/`), ünite klasörlerine ve `yerel-cerceve/`'ye dokunulmadı.

**Öğretmenden beklenen seçimler**

1. Hap Bilgi ailesinden hangi türler kalsın? (6 seçenek, K1 sayfası)
2. Kitabın renk teması hangisi olsun? (5 seçenek, K2–K3 sayfaları, `onizleme/karsilastirma.png`)
3. Konu karakterleri bütün ünitelere yayılsın mı? (K4 sayfası)
4. Dört önerimizden hangileri kalsın? (aşağıda "Öneriler")

## Dosyalar

| Dosya | Ne |
|---|---|
| `atom-modelleri-van-golu.pdf` | 3 örnek sayfa · şu anki palet (Van Gölü) |
| `atom-modelleri-iznik-cini.pdf` · `-selcuklu-toprak.pdf` · `-rasathane-gecesi.pdf` · `-yumusak-pastel.pdf` | aynı 3 sayfa, diğer dört temada |
| `hap-bilgi-katalog.pdf` | 4 sayfa: K1 Hap Bilgi ailesi · K2 renk temaları · K3 renk denetimi · K4 konu karakterleri |
| `onizleme/<tema>/s01…s03.png` | her temanın sayfa önizlemeleri (2×) |
| `onizleme/karsilastirma.png` | aynı sayfa (s.2) beş temada yan yana |
| `onizleme/hap-bilgi.png` · `temalar.png` · `renk-denetimi.png` · `karakterler.png` | katalog sayfaları |
| `onizleme/renk-korlugu.png` · `renk-denetimi.json` | döteranopi benzetimi (PNG) ve sayısal sonuçlar |

Sayfa numaraları kitaptaki yerleriyle basılır (2, 3, 4). PDF'lerin hepsinde **Type 3 font 0**; toplam ≈ 10 MB.

```sh
cd kitap/gelistirme/atom-modelleri
python3 uretec/kur.py                    # 5 tema × 3 sayfa + katalog + karşılaştırma + renk denetimi (≈ 40 sn)
python3 uretec/kur.py --tema van-golu    # tek tema (hızlı deneme) · --katalog yalnız katalog · --pdfsiz yalnız PNG
python3 uretec/dogrula.py                # 83 denetim → SONUÇ: hepsi doğru
```

`kur.py` her HTML'i `render.js` ile basar ve taşma denetimini çalıştırır: altı HTML'in hepsinde **taşma yok**.
Ara dosyalar (`*.html`, `gorsel/`) `.gitignore`'dadır.

```
uretec/
  kur.py                  kurucu: SAYFA/SIMDI, yeni yer tutucular, 5 tema döngüsü, render.js
  sablon.html             3 örnek sayfa        katalog.html   4 katalog sayfası
  meta.json               9/03 meta.json'dan aynen (duraklar, nişanlar, hazine, medeniyet)
  gelistirme.css          yeni bileşenler: §A Hap Bilgi ailesi · §B sohbet şeridi · §C Model Zinciri · §D çizgi roman ·
                          §E enerji merdiveni · §F öneriler · §H katalog
  hap_bilgi.py            Hap Bilgi ikonları ({{hbi|ad}}), {{ok}}, {{siklik|3|3}}
  konu_karakterleri.py    konu karakteri kiti (kk-* sembolleri, {{kk|kimlik}}, KK.kullan)
  tema.py                 renk temaları: token tablosu + kurulumda palet eşlemesi (CSS, SVG, ebru JPEG)
  infografik_gelistirme.py  Model Zinciri yolu, 6 çizgi roman panosu, enerji merdiveni, öneri çizimleri
  sahneler_gelistirme.py  9/03 sahneleri (salt okunur yüklenir) + gece temasında yıldız
  katalog_kur.py          katalog yer tutucuları, karşılaştırma levhası, WCAG + döteranopi denetimi
  dogrula.py              bilgi ve sayı denetimi
```

## A. Örnek sayfalar

| s. | Yer (9/03 sahnesi) | İçerik | Dikkat görselleri |
|---|---|---|---|
| 2 | Göbeklitepe · sabah | sohbet şeridi; **Model Zinciri**: altı model altı karakter (atomos, Dalton bilardo topu, Thomson üzümlü kek, Rutherford minik çekirdek, Bohr halkaları, elektron bulutu), her biri kendi balonunda *fikrini* ve *“ama…”* eksiğini söyler; ad ve yıl levhada | Hap Bilgi ×2 · Sınav Radarı · Unutma! |
| 3 | Harran · öğle | **Çizgi roman** (6 pano): düzenek (1909) → çoğu geçer → bazıları sapar → çok azı geri döner (Rutherford'un “top mermisi” benzetmesi) → neden? (nohut–stadyum) → **deneyden sonuca**; Pamuk anlatır, α'lar pilot gözlüklü | Altın Kural · Dikkat! · Hap Bilgi (+ H3 hazine kartı) |
| 4 | Harran Höyüğü · akşam | **Enerji merdiveni**: n = 1…6 basamakları (−13,6/n² eV), elektron UV fotonu yutup n = 3'e çıkar, 3 → 2 inerken kırmızı foton (656 nm) yayar, 2 → 1 UV; sağda dört görünür çizgi (410 · 434 · 486 · 656 nm), fotonlar dalga boyunun renginde; Bohr'un sınırı (H, He⁺, Li²⁺); Medeniyetimizden: el-Battânî (9/03 metni) | Kilit Bilgi · Dikkat! · Sınav Radarı · Hap Bilgi |

Tarihler: Demokritos MÖ y. 400 · Dalton 1803–1808 · Thomson elektron 1897, model 1904 · altın levha 1909–1911,
çekirdekli model 1911 · Bohr 1913 · kuantum modeli 1920'ler (de Broglie 1924, Schrödinger 1926). Gerçek bilim
insanlarının yüzü çizilmedi; karakterler modelin kendisidir. Çizgi romandaki deneyci figürü yerine anlatıcı Pamuk'tur.

## B. Hap Bilgi ailesi · 6 dikkat görseli

Her türün **kendine özgü biçimi** var; renk görmeyen ya da fotokopi okuyucusu türü şekilden tanır. Hepsi vektör,
metin açık zeminde ve ≥ 9,5 pt, CSS `filter` yok, ✓ ★ ↔ gibi işaretler SVG.

| # | Tür (CSS) | Biçim | Ne zaman? | Örnek sayfada |
|---|---|---|---|---|
| 1 | **Hap Bilgi** (`.hb-hap`, `.gol .kob .mer`) | iki renkli kapsül, yuvarlak uçlar, hap ikonu | Tek cümlelik, ezberlenecek kısa bilgi (tanım, sayı, sıra); sayfa başına 1–2 | s.2, 3, 4 |
| 2 | **Altın Kural** (`.hb-kural` + `{{kose}}`) | lacivert–altın çift çerçeve, tezhip köşebent, kertikli kurdele | Ünitenin üstüne kurulduğu temel kural; ünitede en çok 2–3 kez | s.3 |
| 3 | **Unutma!** (`.hb-unutma`) | yapışkan not: bant, çizgili kâğıt, mercan kenar, kıvrık köşe, hafif eğik | Kolay gözden kaçan küçük ayrıntı ya da istisna | s.2 |
| 4 | **Sınav Radarı** (`.hb-radar`) | radar ikonu, yer imi kurdelesi (TYT/AYT), sıklık noktaları | TYT/AYT'de sık sorulan bilgi ya da soru kalıbı | s.2, 4 |
| 5 | **Dikkat!** (`.hb-dikkat`) | kalın kırmızı sol çizgi, kehribar uyarı üçgeni, altı çizili anahtar söz | İşlem/okuma hatası (birim, işaret, “soğurur/yayar”); **Tuzak!** yanlış inancı mühürler, Dikkat! dikkatsizliği önler | s.3, 4 |
| 6 | **Kilit Bilgi** (`.hb-kilit`) | anahtar madalyonu, yuvarlak sol uç, anahtar deliği filigranı | Konunun tamamını açan tek fikir; durak başına en çok 1 | s.4 |

Kural önerisi: sayfa başına en çok 3–4 dikkat görseli, aynı türden en çok 2. Karar şeması K1 sayfasında.

## C. Renk temaları

Tema **kurulumda** uygulanır (fotokopi.py ile aynı yöntem): kitap Van Gölü renkleriyle kurulur, sonra `tema.py`
stil.css'teki bütün renkleri (tokenlar, elle yazılmış onaltılık renkler, rgba), satır içi SVG renklerini ve ebru JPEG'ini
OKLab uzayında eşler. Kodda türetilen tonlar (açık/koyu karışımlar, gradyan durakları) kendi tokenıyla birlikte kayar
(token çevresine konan çapalarla yumuşak komşu ağırlıklandırması); token ailelerinden uzak renkler (deri, gök, toprak)
değişmez. **Dokunulmayanlar:** karakterler (Pamuk, Elif, Yusuf, Zeynep, kk-*), `data-tema-sabit` taşıyan her şey
(spektrum, dalga boyuna göre renkli fotonlar, tanecik çizimleri), maskeler. Sahne bantları ayrı bir “sahne eşlemesi” alır.

**Anlam renkleri sabit kalır:** `keh` hep ödül/akçe (altın-kehribar), `mer` hep Tuzak/Dikkat (kırmızı), `zumrut` hep
doğru (yeşil). Tema *kimlik* renklerini değiştirir: `gol` ana renk, `kob` kavram, `obs` mürekkep ve HUD, `derin` sert
gölge, zemin, gri, tezhip ve gün batımı tonları.

| Tema | Kimlik | Sahne |
|---|---|---|
| **Van Gölü** (şu anki) | göl turkuazı, kehribar, İznik mercanı ve kobaltı, tezhip altını | aynen |
| **İznik Çini** | bembeyaz zemin, kobalt ana renk, mercan kırmızısı, çini yeşili (kavram) | aynen |
| **Selçuklu Toprak** | parşömen zemin, kerpiç-terakota ana renk, lacivert taş (kavram), altın, turkuaz-yeşil (doğru), koyu kırmızı Tuzak | hafif ikindi sıcaklığı |
| **Rasathane Gecesi** | gece laciverti HUD ve mürekkep, çivit ana renk, açık erguvan kavram, yıldız altını; metin alanları açık | gece (ay ışığı eşlemesi + sabit renkli yıldızlar); levhada gün saati “gece” olur |
| **Yumuşak Pastel** | krem zemin, adaçayı yeşili ana renk, şeftali, lavanta; az doygun, gölgeler yumuşak, mürekkep yine koyu | yumuşatılmış, az doygun |

Token tablosu (`stil.css :root` = `cizim/renkler.py`; HUD ve vurgu gibi elle yazılmış birkaç renk için ek çapalar
`tema.py VAN_EK`'te):

| Token | Van Gölü | İznik Çini | Selçuklu Toprak | Rasathane Gecesi | Yumuşak Pastel |
|---|---|---|---|---|---|
| `--kar` | `#FBFDFD` | `#FFFFFF` | `#FCF9F3` | `#F8F8FD` | `#FDFCF8` |
| `--kirec` | `#FFFDF7` | `#FFFEFA` | `#FFFBF1` | `#FFFDF5` | `#FFFDF8` |
| `--obs` | `#1B1D26` | `#131A33` | `#2A1D16` | `#12173A` | `#2A2E39` |
| `--obs-2` | `#343947` | `#2B3556` | `#4A372B` | `#2B3160` | `#434957` |
| `--soluk` | `#56636E` | `#4E5A73` | `#6A584B` | `#535A80` | `#5E6672` |
| `--cizgi` | `#CFDCE0` | `#D2DBEE` | `#E5D6C6` | `#D5D7EC` | `#DDE3E5` |
| `--gol` | `#13A3A6` | `#1F4FA8` | `#B4532C` | `#3443A8` | `#5E9A78` |
| `--gol-k` | `#0A6C74` | `#14377C` | `#7C3416` | `#1F2A78` | `#36664B` |
| `--gol-a` | `#DCF3F1` | `#DDE6F7` | `#F6E0D2` | `#E0E3F7` | `#E2EFE5` |
| `--gol-aa` | `#EEF9F8` | `#EFF3FC` | `#FBF1EA` | `#F0F1FC` | `#F2F8F3` |
| `--derin` | `#0E4C5A` | `#0E2457` | `#5A2B15` | `#161B47` | `#7D9688` |
| `--keh` | `#F0A21A` | `#F2A516` | `#D69E1E` | `#E2A81C` | `#EBAA5E` |
| `--keh-k` | `#8C5500` | `#8A5300` | `#7A5608` | `#7F5A06` | `#80530F` |
| `--keh-a` | `#FFF0CF` | `#FFF1CF` | `#FBEFC8` | `#FCF0CB` | `#FFF1DE` |
| `--mer` | `#E2533D` | `#E04A35` | `#8F1B2C` | `#D9414F` | `#DD7464` |
| `--mer-k` | `#A12817` | `#A11E12` | `#6A0F1E` | `#991A2A` | `#9C3B2C` |
| `--mer-a` | `#FDE7E1` | `#FDE4DF` | `#F8E0E3` | `#FCE3E6` | `#FCEAE5` |
| `--kob` | `#2B50B5` | `#20855A` | `#25479B` | `#8A5BC4` | `#7A86C4` |
| `--kob-k` | `#1B3584` | `#135C3C` | `#16306F` | `#55308E` | `#434F8C` |
| `--kob-a` | `#E6ECFB` | `#DFF2E7` | `#E2E8F6` | `#F1E9FA` | `#EDEFFA` |
| `--gun` | `#FF7A3D` | `#F26B3A` | `#E0783A` | `#F2884C` | `#F29B6E` |
| `--pembe` | `#FF5C8A` | `#E94E7C` | `#D65A6E` | `#E35C9A` | `#EE8AA5` |
| `--erguvan` | `#7B3F8C` | `#5E3D93` | `#77406C` | `#7A2860` | `#8C5A86` |
| `--altin` | `#C9952B` | `#C9952B` | `#C9952B` | `#D4A02C` | `#C9A257` |
| `--altin-k` | `#8A6212` | `#8A6212` | `#85600F` | `#866011` | `#81622A` |
| `--altin-a` | `#F6E7BF` | `#F6E7BF` | `#F6E6BC` | `#F7E9C2` | `#F6ECD4` |
| `--lajver` | `#1D3A8A` | `#173A8F` | `#1E3A87` | `#1A2368` | `#3D5390` |
| `--zumrut` | `#1F8A5B` | `#127A4F` | `#0E766C` | `#127559` | `#2C7560` |
| `--gum` | `#A3B3BE` | `#A9B5C8` | `#B8A99B` | `#A7ABC7` | `#B6C0C6` |
| `--gum-k` | `#586874` | `#55617A` | `#6B5D51` | `#575D82` | `#626E76` |
| `--gum-a` | `#EDF2F5` | `#EEF1F7` | `#F3EEE7` | `#EEEFF8` | `#F1F4F5` |

### Renk denetimi (kontrast ve renk körlüğü)

**Kontrast** (WCAG oranı, `tema.kontrast`): gövde metni bütün temalarda ≥ 13. Eşik altında kalan tek değer
**şu anki** Van Gölü paletindedir: “Doğrusu” etiketi (`--zumrut` #1F8A5B, 7,8 pt kalın) beyaz üstünde 4,3.
**Öneri:** `--zumrut` → `#1A7F53` (4,9); görünüm neredeyse aynı kalır.

| Yazı / zemin (eşik) | Van Gölü | İznik Çini | Selçuklu Toprak | Rasathane Gecesi | Yumuşak Pastel |
|---|---|---|---|---|---|
| gövde · obs / kar (≥ 7,0) | 16,4 | 17,2 | 15,5 | 16,4 | 13,2 |
| etiket · gol-k / beyaz (≥ 4,5) | 6,2 | 11,2 | 8,9 | 12,7 | 6,7 |
| etiket · gol-k / gol-aa (≥ 4,5) | 5,7 | 10,1 | 8,0 | 11,3 | 6,2 |
| akçe · keh-k / keh-a (≥ 4,5) | 5,5 | 5,7 | 5,8 | 5,5 | 6,0 |
| Tuzak · mer-k / mer-a (≥ 4,5) | 6,2 | 6,4 | 9,9 | 6,8 | 5,9 |
| kavram · kob-k / kob-a (≥ 4,5) | 9,4 | 6,9 | 10,1 | 8,1 | 6,7 |
| Doğrusu · zumrut / beyaz (≥ 4,5) | **4,3** ⚠ | 5,3 | 5,5 | 5,7 | 5,5 |
| HUD · beyaz / obs (≥ 7,0) | 16,8 | 17,2 | 16,3 | 17,4 | 13,6 |
| HUD · keh / obs (≥ 4,5) | 7,9 | 8,3 | 6,8 | 8,2 | 6,8 |
| çip · beyaz / gol (≥ 3,0) | 3,1 | 7,7 | 5,0 | 8,3 | 3,3 |
| Tuzak başlığı · beyaz / mer (≥ 3,0) | 3,8 | 4,0 | 8,9 | 4,4 | 3,1 |
| kurdele · beyaz / kob (≥ 3,0) | 7,2 | 4,6 | 8,6 | 4,8 | 3,5 |
| tezhip · altin-a / lajver (≥ 4,5) | 8,4 | 8,4 | 8,4 | 11,7 | 6,3 |

**Döteranopi** (kırmızı-yeşil renk körlüğünün en yaygın türü): (1) her temanın s01.png'si Machado (2009) matrisiyle
doğrusal RGB'de boyandı → `onizleme/renk-korlugu.png` (üst sıra normal, alt sıra döteranop); (2) anlamca birbirinden
ayrılması gereken token çiftlerinin OKLab uzaklığı (ΔE·100) normal ve döteranop görüşte ölçüldü (ΔE < 6 sorun ⚠,
6–12 dikkat):

| Çift (biçim ipucu) | Van Gölü | İznik Çini | Selçuklu Toprak | Rasathane Gecesi | Yumuşak Pastel |
|---|---|---|---|---|---|
| Yanlış ↔ Doğru (çarpı/tik, mühür) | 28,0 → 10,9 | 29,3 → 14,3 | 24,9 → 10,1 | 29,1 → 13,2 | 26,1 → 19,0 |
| Tuzak ↔ ana renk (başlık şeridi) | 28,9 → 14,8 | 35,2 → 32,9 | 14,2 → 13,4 | 32,9 → 30,3 | 19,9 → 7,3 |
| Akçe ↔ Tuzak (çip / başlık) | 18,7 → 14,4 | 20,9 → 16,5 | 34,2 → 31,5 | 24,5 → 17,9 | 13,9 → 11,5 |
| Ana renk ↔ kavram (etiket renkleri) | 24,4 → 23,0 | 23,0 → 21,8 | 29,3 → 28,8 | 16,0 → 13,3 | 15,0 → 12,1 |
| Ana renk ↔ akçe (kapsül kapakları) | 26,5 → 23,8 | 45,4 → 47,0 | 20,1 → 18,1 | 45,6 → 46,7 | 20,8 → 18,3 |
| Elif ↔ Pamuk balonu (balon zemini) | 3,9 → **3,4** ⚠ | 4,6 → **4,0** ⚠ | 6,1 → **5,5** ⚠ | 5,7 → **5,0** ⚠ | 2,3 → **2,1** ⚠ |
| Yanlış ↔ doğru zemini (ikili kart) | 4,7 → **3,3** ⚠ | 4,5 → **3,7** ⚠ | 4,2 → **3,8** ⚠ | 3,9 → **3,0** ⚠ | 3,5 → **2,3** ⚠ |
| Kavram ↔ erguvan (gün batımı / rozet) | 13,8 → 8,9 | 25,7 → 19,2 | 14,7 → 12,2 | 18,2 → 17,2 | 13,1 → 10,8 |

Notlar:
* İlk denemede üç sorun çıktı ve düzeltildi: Selçuklu'da Tuzak kırmızısı terakota ana renkle karışıyordu (2,4) → koyu
  kırmızı `#8F1B2C`; Rasathane'de ana renk–kavram (4,9) ve kavram–erguvan (1,9) birbirine çok yakındı → kavram açık
  erguvan `#8A5BC4`, erguvan koyu mürdüm `#7A2860`; Pastel'de kavram–erguvan (4,2) → erguvan `#8C5A86`.
* **Yanlış ↔ Doğru** (kırmızı/yeşil) döteranopta bütün temalarda yakınlaşır (ΔE 10–19); kitapta bu anlam hiçbir yerde
  yalnız renkle verilmez (çarpı/tik ikonu, YANLIŞ/DOĞRU mührü, üstü çizili yazı).
* Kalan tek ⚠ çiftler iki açık zemin tonudur: Elif–Pamuk balonları ve “yanlış/doğru” ikili kartı. İkisinde de biçim ipucu
  var (Pamuk balonu kesik çizgili, adlar yazılı; ikili kartta ikon + üstü çizili yazı). Yeni bileşenlerde de kural:
  **renk + biçim**.

## D. Konu karakterleri

`uretec/konu_karakterleri.py` · Pamuk/Elif/Yusuf ile aynı çizgi dili (koyu kontur `OBS`, düz renk + yumuşak radyal
gölge, iri göz, pembe yanak). Her karakter bir `<symbol>`'dür, `{{defs}}` ile sayfaya bir kez gömülür; şablonda
`{{kk|kk-dalton}}`, çizimde `KK.kullan("kk-alfa-sasiran", x, y, w)`. Kimlikler `kk-` ile başladığı için temalar
renklerini değiştirmez (tanecik renkleri kitap boyunca aynı: proton mercan, nötron gri, elektron kobalt). El çizilmedi
(kalkan el kuralı sorunu doğmaz); duygu yüz ve kaşla verilir. Yük rozetleri (+, −, 2+) çizgiyle çizilir.

| Kimlik | viewBox | Ad | Not |
|---|---|---|---|
| `#kk-atomos` | `0 0 120 120` | Atomos | Demokritos’un bölünemez taneciği · MÖ y. 400 |
| `#kk-dalton` | `0 0 120 120` | Dalton topu | içi dolu bilardo topu · 1803–1808 |
| `#kk-thomson` | `0 0 120 120` | Üzümlü kek | (+) hamur, (−) üzümler · 1897 · 1904 |
| `#kk-rutherford` | `0 0 120 120` | Minik çekirdek | çoğu boşluk, yoğun (+) çekirdek · 1911 |
| `#kk-bohr` | `0 0 120 120` | Halkalı Bohr | belirli enerjili katmanlar · 1913 |
| `#kk-bulut` | `0 0 120 120` | Elektron bulutu | olasılık bölgesi · 1920’ler |
| `#kk-cekirdek` | `0 0 60 60` | Altın çekirdeği | yoğun, (+) · çizgi roman |
| `#kk-proton` | `0 0 60 60` | Proton | + yük · çekirdekte |
| `#kk-notron` | `0 0 60 60` | Nötron | yüksüz · çekirdekte |
| `#kk-elektron` | `0 0 60 60` | Elektron | − yük · 4 ifade |
| `#kk-alfa` | `0 0 72 66` | α taneciği | 2p + 2n, 2+ · pilot gözlüklü |
| `#kk-foton-656` | `0 0 92 50` | Foton 656 nm | kırmızı (n = 3 → 2) |
| `#kk-foton-486` | `0 0 92 50` | Foton 486 nm | camgöbeği (n = 4 → 2) |
| `#kk-foton-434` | `0 0 92 50` | Foton 434 nm | mavi (n = 5 → 2) |
| `#kk-foton-410` | `0 0 92 50` | Foton 410 nm | mor (n = 6 → 2) |
| `#kk-foton-uv` | `0 0 92 50` | UV foton | görünmez · güneş gözlüklü |
| `#kk-su` | `0 0 100 84` | Su molekülü | H₂O · sonraki üniteler |
| `#kk-iyon-arti` | `0 0 64 64` | Katyon | Na⁺ · iyon rozeti |
| `#kk-iyon-eksi` | `0 0 64 64` | Anyon | Cl⁻ · iyon rozeti |
| `#kk-atom` | `0 0 80 80` | Atom | genel maskot |

İfade ekli kimlikler: `kk-elektron-heyecan / -sasiran / -sakin / -sersem`, `kk-alfa-mutlu / -sasiran / -sersem`,
`kk-dalton-sasiran`, `kk-thomson-endiseli`, `kk-cekirdek-sasiran`. Yüz fonksiyonu `yuz(cx, cy, ölçek, ifade, sklera)`
10 ifade verir (mutlu, gülen, şaşkın, kararlı, düşünceli, sakin, sersem, gururlu, heyecanlı, endişeli); su molekülü,
katyon, anyon ve genel atom sonraki üniteler için hazır.

## E. Öneriler (bizim eklediklerimiz)

| # | Öneri | Nerede | Neden |
|---|---|---|---|
| öneri 1 | **Bir bakışta** · 3 maddelik koyu özet kartı | s.2 sağ alt, s.4 sağ alt | sayfanın sonunda üç cümlelik toparlama; Hülasa'ya hazırlık |
| öneri 2 | **Kendini dene** · 2 kısa soru, cevaplar ters yazılı (+20 akçe) | s.2, s.3, s.4 | anında geri bildirim; akçe sistemine bağlı |
| öneri 3 | **Yanlış bilinen ↔ Doğrusu** · yan yana görsel çift (çarpı/tik, mini çizim) | s.2 sol alt | Tuzak!'ın hafif, görsel kardeşi; yanlış model ile doğrusu aynı anda görülür |
| öneri 4 | **Tahmin et, sonra gözle** · “Thomson'a göre beklenen” ↔ “gözlenen” | s.3 | tahmin–gözlem–açıklama: modelin neden değiştiğini öğrenci kendisi görür |

Ayrıca örnek sayfalarda kullanılan ve ortak kütüphaneye aday yapı taşları: **sohbet şeridi** (3 mesajlık tek satır sohbet,
yer kazandırır), **çizgi roman panosu** (anlatıcı kutusu + konuşma balonu + pano numarası), **Model Zinciri**
(12 sütunlu ızgarada karakter + balon + levha).

## Doğruluk

`uretec/dogrula.py` 83 denetim yapar ve `SONUÇ: hepsi doğru` ile biter: model yılları (sayfadaki levhalar ↔ tablo);
Rydberg (R = 1,09678·10⁷ m⁻¹) ile n → 2 çizgileri 410/434/486/656 nm; düzey enerjileri −13,6/n² eV ve etiketleri;
foton enerjileri 12,09 = 1,89 + 10,20 eV, 656 nm ve UV sınıflaması; α/elektron kütle oranı ≈ 7294 (“yaklaşık 7300 kat”);
çekirdek/atom ölçeği ve nohut–stadyum benzetmesi (≈ 25 000); H, He⁺, Li²⁺'nin tek elektronlu olduğu; Na 2·8·1;
dalga boyu renk tablosu, H çizgileri ve tanecik renklerinin 9/03 ile aynı olduğu; el-Battânî metninin 9/03 meta.json ile
aynı olduğu; Kendini dene cevapları; altı Hap Bilgi türünün ve dört önerinin sayfada kullanıldığı; temaların gövde ve
etiket kontrastları.

## Ortak kütüphaneye taşınırsa ne değişir?

Onay gelirse şunlar **ortak dosyalara** eklenir (yalnız ekleme; mevcut API değişmez):

1. **`yerel-ortak/cizim/konu_karakterleri.py`** (yeni) ← `uretec/konu_karakterleri.py`.
   `kur_ortak.ortak_defs()` içine `KK.semboller()` eklenir; `Unite._genel_yer_tutucular`'a `{{kk|kimlik|sınıf}}`.
   Bütün ünitelerin HTML'i ≈ 60 KB büyür (semboller bir kez gömülür).
2. **`yerel-ortak/cizim/hap_bilgi.py`** (yeni) ← `uretec/hap_bilgi.py`; yer tutucular `{{hbi|ad}}`, `{{ok}}`, `{{siklik|n|m}}`.
3. **`yerel-ortak/stil.css`**: yeni bölümler · §36 Hap Bilgi ailesi (`gelistirme.css` §A; yalnız seçilen türler),
   §37 sohbet şeridi, §38 çizgi roman panosu, §39 öneri bileşenleri (§F; seçilenler). Her biri için `html.fotokopi`
   kuralları da yazılır (şu an yok, bkz. bilinen sorunlar). Model Zinciri ve enerji merdiveni konuya özeldir; 9/03'ün
   `infografik_unite.py`'sine ve şablonuna girer.
4. **`yerel-ortak/tema.py`** (yeni) ← `uretec/tema.py`. İki yol:
   * **Bir tema kitabın yeni varsayılanı olursa:** eşleme her seferinde çalışmaz; `stil.css :root`, `cizim/renkler.py`,
     `kur_ortak.RENK`, `ortak_defs` gradyanları ve elle yazılmış birkaç onaltılık renk (HUD, vurgu, sahne dışı süsler)
     **bir kez** yeni değerlerle güncellenir; ebru dokuları `tema.ebru_boya` ile yeniden boyanır. Bütün üniteler yeniden
     kurulur ve görsel olarak kontrol edilir.
   * **Temalar seçenek olarak kalırsa:** `kur_ortak.Unite.kur()`'a `--tema <ad>` eklenir (`unite-<tema>.html`,
     fotokopi varyantı gibi); `render.js`'e `--tema` bayrağı. Ünite yazarları renklerini yine tokenlardan alır;
     fiziksel renkler (spektrum, alev rengi) `data-tema-sabit` ile işaretlenir.
5. **`TASARIM-SISTEMI.md`**: §5 bileşen tablosu (Hap Bilgi ailesi, öneriler), §6 modül tablosu (`konu_karakterleri`,
   `hap_bilgi`, `tema`), §7 karakter sayfası (konu karakterleri), §12 varyantlar (tema), §14 (renk + biçim kuralı).
   `katalog.py` konu karakterleri kataloğu üretir.

## Bütün ünitelere uygulama planı

1. **Seçim** (öğretmen): Hap Bilgi türleri, tema, öneriler, karakterler.
2. **Ortak kütüphane** (bir kez, yukarıdaki 1–5): modüller, stil.css bölümleri + fotokopi kuralları, tema kararı;
   `katalog.py` ve `TASARIM-SISTEMI.md` güncellenir.
3. **Ünite başına** (16 ünite, her biri ≈ yarım gün): mevcut Tuzak/Kavram/Hızlı görev kutularından uygun cümleleri
   seçilen dikkat görsellerine dönüştür (sayfa başına 3–4); her durağa bir Bir bakışta + bir Kendini dene; konuya göre
   1–2 konu karakteri ekle (ör. Mol: “mol paketi”, Gazlar: gaz tanecikleri, Asit–baz: H⁺/OH⁻ iyonları) ve bir panoyu
   çizgi romanla anlat; `dogrula.py`'ye yeni sayıları ekle.
4. **Denetim**: `olc.sh` (taşma yok), `dogrula.py` (hepsi doğru), `render.js --hepsi` (öğretmen/fotokopi/baskı), Type 3 = 0,
   renk denetimi (`katalog_kur.renk_denetimi`), her PNG'ye tam boy bakış.
5. **Kitap birleştirme**: `yerel-cerceve/` yeniden basılır.

## Bilinen sorunlar ve sınırlar

* **Fotokopi varyantı** yeni bileşenler için henüz tanımlı değil (kapsül kapağı, Bir bakışta koyu kartı, Sınav Radarı
  kurdelesi koyu zeminli). `fotokopi.py` SVG'leri doğru griler; CSS tarafı için `html.fotokopi` kuralları yazılmalı.
* **Öğretmen baskısı:** Kendini dene cevapları yalnız ters yazılı; `.ogr` işaretleri eklenmedi.
* α harfi Nunito ve Baloo'da yok; DejaVu Sans'tan gelir (9/03'te de böyle). PDF'te Type 3 yok, ama harf biçimi biraz farklı.
* Tema eşlemesi token ailelerine yakın renklerde çalışır; elle seçilmiş uzak renkler (Model Zinciri'nin kum yolu, çizgi
  roman zeminleri) bilerek sabit kalır. Gece eşlemesi sahnedeki dekoratif prizma gökkuşağını da koyulaştırır (bilgi
  grafiğindeki spektrum sabittir).
* Van Gölü “Doğrusu” yeşili 4,3 kontrastta (öneri yukarıda); açık zemin tonları döteranopta yakın (biçim ipucu var).
* Örnek sayfalar ünitenin 2–4. sayfalarından daha yoğundur; üniteye taşınırsa 9/03'ün Görev 1–3 ve hazine kartları
  H1, H2, H4–H6 yeniden yerleştirilmelidir (örnekte yalnız H3 var).
* Rutherford'un “top mermisi” sözü, 1936'daki konuşmasından yaygın bilinen alıntının Türkçe kısaltmasıdır.
