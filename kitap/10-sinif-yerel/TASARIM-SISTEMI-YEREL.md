# Kimya Rotası · Yerel Tasarım Sistemi ("Van Gölü" + tezhip)

Bu belge, `10-sinif-yerel/02-mol-kavrami/` ünitesinde kurulan tasarımın **prototip** tanımıdır.
Başka kimya üniteleri ve başka ders kitapları bu sistemle, aynı klasör yapısı ve aynı çizim
kütüphanesiyle üretilir.

- Ana iskelet: **B · Van Gölü** (tur rotası, duraklar, akçe, Pamuk).
- Ödünç alınanlar: **C · Medrese Defteri**'nden tezhipli "Medeniyetimizden" köşesi, YANLIŞ/DOĞRU yıldız mühürleri, tezhip köşebendi inceliği.
- Kimlik kuralları: `kitap/YEREL-KIMLIK.md` (terimler, karakterler, örnek havuzu, Medeniyetimizden bilgileri). Bu belge onlarla çelişmez.
- Görsel kataloglar: `katalog/*.png` (`python3 02-mol-kavrami/uretec/katalog.py` ile yeniden üretilir).

---

## 1. İlkeler

1. **Görsel doygunluk illüstrasyonda, sükûnet metinde.** Her sayfada en az bir büyük, katmanlı sahne vardır
   (gökyüzü gradyanı, güneş halesi, dağ gölgesi, kar örtüsü, göl yansıması, parıltı). Soru ve metin alanları açık zeminde,
   yüksek kontrastla durur. Koyu/yoğun blok yalnızca illüstrasyon alanında (sahne bandı, panorama, Hülasa ebru zemini, koyu özet kartı).
2. **Her şey koddan.** İllüstrasyonlar Python ile SVG olarak üretilir; tohum (`tohum`) değerleri sabit olduğu için her kurulumda
   aynı resim çıkar. Elle çizilmiş dosya yoktur; tutarlılık ve yeniden kullanım bundan gelir.
3. **Okunurluk sınırları.** Gövde metni ≥ 9,5 pt (Nunito). Etiket/çip/harita yazıları 6–8 pt olabilir ama büyük harf + kalın.
   Kimyasal formüllerde `<sub>`/`<sup>`; SVG içinde `<tspan dy>`.
4. **Kimyasal doğruluk tasarımdan önce gelir.** Her sayı `uretec/dogrula.py` içinde yeniden hesaplanır; çoktan seçmelide tek doğru şık
   denetlenir; cevap anahtarı sayfadan (unite.html) okunup hesapla karşılaştırılır.
5. **Yerel ve saygılı.** Kurum/marka logosu, gerçek kişi görseli, kutsal metin hattı yok. Mezar taşlarında yazı yerine yalnızca
   geometrik oyma. Medeniyetimizden kutuları yalnızca `YEREL-KIMLIK.md`'deki doğrulanmış bilgilerle (el-Bîrûnî satranç tahtası bilgisi kullanılmaz).

---

## 2. Üretim hattı ve dosya düzeni

```
10-sinif-yerel/
  TASARIM-SISTEMI-YEREL.md    bu belge
  katalog/*.png               karakter, sahne, molekül, süs, infografik, ebru katalogları
  NN-unite-adi/
    stil.css                  tasarım sistemi (kanonik kopya; yeni üniteye aynen kopyala)
    unite.html                ÜRETİLİR
    NN-unite-adi.pdf          ÜRETİLİR
    onizleme/sNN.png          ÜRETİLİR (deviceScaleFactor 2)
    gorsel/ebru-*.jpg         ÜRETİLİR (kur.py, yoksa)
    uretec/
      sablon.html             sayfaların içeriği + {{yer-tutucular}}
      kur.py                  yer tutucu çözücü + sayfa künyesi (SAYFA, SIMDI) → unite.html
      render.js               PDF + PNG + taşma denetimi
      olc.sh                  taşma özeti
      dogrula.py              sayısal doğrulama
      katalog.py, fotograf.js katalog görselleri
      cizim/                  illüstrasyon kütüphanesi (bkz. §6)
```

```sh
python3 uretec/kur.py && python3 uretec/dogrula.py && uretec/olc.sh   # sonra onizleme/*.png'ye tek tek bak
```

`render.js` iki tür sorunu listeler; ikisi de **boş** olmalıdır:
- **alan dışı:** içerik alanının (üstte 12 mm, altta 283 mm, yanlarda 10 mm) dışına çıkan öğe. Sahne bantları ve panorama `data-serbest` ile muaftır.
- **kutu taşması:** kart, balon, şık, levha, meşveret kartı, ızgara gibi kutulara sığmayan içerik. Bilerek yatay taşan dekorlu kapsayıcı `data-tasma-yatay` ile işaretlenir (yalnız Hülasa ebru zemini).

---

## 3. Renk tokenları (`stil.css :root` = `uretec/cizim/renkler.py`)

| Aile | Token | Değer | Kullanım |
|---|---|---|---|
| Zemin | `--kar` | `#FBFDFD` | Süphan karı: sayfa zemini |
| | `--kirec` | `#FFFDF7` | kireç beyazı: Medeniyetimizden zemini |
| Mürekkep | `--obs` / `--obs-2` | `#1B1D26` / `#343947` | Nemrut obsidyeni: çizgi, metin, HUD |
| | `--soluk` / `--cizgi` | `#56636E` / `#CFDCE0` | ikincil metin / kesik ayraç |
| Van Gölü | `--gol` / `-k` / `-a` / `-aa` | `#13A3A6` / `#0A6C74` / `#DCF3F1` / `#EEF9F8` | ana renk, Yusuf, durak rozeti, kavram vurgusu |
| | `--derin` | `#0E4C5A` | sert gölge (`--golge: 1.1mm 1.3mm 0`) |
| Kehribar | `--keh` / `-k` / `-a` | `#F0A21A` / `#8C5500` / `#FFF0CF` | akçe, hazine, hızlı görev, Pamuk'un bir gözü |
| İznik mercanı | `--mer` / `-k` / `-a` | `#E2533D` / `#A12817` / `#FDE7E1` | Tuzak!, Elif, imtihan |
| İznik kobaltı | `--kob` / `-k` / `-a` | `#2B50B5` / `#1B3584` / `#E6ECFB` | kavram kutusu, Zeynep Hoca |
| Gün batımı | `--gun` / `--pembe` / `--erguvan` | `#FF7A3D` / `#FF5C8A` / `#7B3F8C` | sahne gökyüzü, Hülasa rozeti |
| Tezhip | `--altin` / `-k` / `-a` / `--lajver` | `#C9952B` / `#8A6212` / `#F6E7BF` / `#1D3A8A` | Medeniyetimizden, rozet çerçeveleri, nişanlar |
| Çini yeşili | `--zumrut` | `#1F8A5B` | "Doğrusu", DOĞRU mührü tonu |
| Kefal gümüşü | `--gum` / `-k` / `-a` | `#A3B3BE` / `#586874` / `#EDF2F5` | ikincil etiket, akçe sikkesi |
| Göz | `MAVI` (renkler.py) | `#3A8CF2` | Pamuk'un mavi gözü |

Atom renkleri (CPK esinli, palete uyarlanmış; `renkler.ATOM`): H `#F3F5F8` · C `#3A3F4B` · O `#E2533D` · N `#2B50B5` · S `#F2C230` ·
Na `#8E5BD0` · Cl `#39A85A` · Ca `#9DB7C6` · He `#5ED3F3` · Mg `#5FC08A` · B `#F2A88A`.

Gökyüzü temaları (`sahne.GOK`): `safak`, `gun`, `altin`, `gunbatimi`, `alaca`, `gece`. Her sayfa farklı saatte geçer:
Edremit sabah → Gevaş öğle → Tatvan ikindi → Ahlat altın saat → … → İskele akşamüstü → Kale gün batımı → Cevaplar gece → Final gün batımı.

---

## 4. Tipografi ölçeği

| Rol | Aile | Ağırlık | Boyut |
|---|---|---|---|
| Açılış dev başlığı | Baloo Bhaijaan 2 | 800 | 54 pt |
| Durak levhası başlığı (`.levha h1`) | Baloo Bhaijaan 2 | 800 | 25 pt (küçük levha 21 pt) |
| Dev sayı (`.dev-sayi`) | Baloo Bhaijaan 2 | 800 | 34 pt (Hülasa'da 27 pt) |
| Ara başlık / özet kart başlığı | Baloo Bhaijaan 2 | 800 | 14 / 13 pt |
| Hazine formülü (`.hf`) | Baloo Bhaijaan 2 | 800 | 14,4 pt |
| Soru metni | Nunito | 800 | 10 pt |
| Gövde, balon, çözüm, şık | Nunito | 400–700 | 9,5–10 pt |
| Etiket (`.et`), çip | Nunito | 900, BÜYÜK HARF, `letter-spacing .085em` | 7,8 pt |
| Medeniyetimizden metni | Amiri | 400/700 | 10,6 pt |
| Medeniyetimizden başlığı, mühür yazısı | Reem Kufi | 700 | 9,4 pt / SVG |
| Yedek | DejaVu Sans / DejaVu Serif | | ⇄ gibi oklar için |

Yazı tipleri `kitap/fontlar/` (OFL) içinden göreli yolla yüklenir (`../../fontlar/...`). SVG içinde `font-family="Baloo Bhaijaan 2"` /
`"Nunito"` / `"Reem Kufi"` doğrudan kullanılır (sayfa `@font-face`'leri geçerlidir).

**Sabit kalınlıklı kopyalar:** Baloo, Nunito ve Reem Kufi değişken (variable) fonttur; Chromium bunları PDF'e **Type 3** olarak gömer
(bazı matbaa RIP'leri sorun çıkarır). Bu yüzden `stil.css` her kalınlık için ayrı `@font-face` ile `fontlar/<aile>/static/*.ttf`
dosyalarını yükler. Kopyaları üretmek / yeni kalınlık eklemek: `python3 kitap/araclar/statik_fontlar.py` (listeyi betikte güncelle).
Mevcut kalınlıklar: Baloo 400–800, Nunito 400–900 (italik 400, 600–900), Reem Kufi 400–700; istenen kalınlık yoksa en yakını seçilir.

---

## 5. Sayfa çerçevesi ve bileşenler (`stil.css` bölüm numaralarıyla)

### Çerçeve
| Sınıf / yer tutucu | Ne için |
|---|---|
| `.sayfa` | 210×297 mm, `overflow:hidden`, `@page A4 margin 0` |
| `{{zemin}}` → `svg.zemin` | çok açık Selçuklu yıldız geçmesi; **tek vektör path** (CSS desen değil, bkz. §10) |
| `{{hud|n}}` → `.hud` | koyu üst şerit: logo, "Van Gölü turu · …", 10 ilerleme noktası (5 durak ●, Hülasa ■, 3 yan yol ◆, kale), akçe kutusu + çubuk |
| `{{cini}}` → `svg.cini-serit` | HUD altında İznik çini şeridi (kobalt zemin, beyaz yıldız, turkuaz göbek, mercan nokta) |
| `.bant` (`.b30 .b36 .b40 .b62`, `.final-bant`) | kenardan kenara sahne bandı (varsayılan 46 mm) — `data-serbest` |
| `.levha` (`.keh .mer .kob .kucuk`) | bandın sol üstündeki beyaz başlık levhası: rozet + üst etiket + h1 + alt başlık + `.hedef` satırları |
| `.ic` | içerik alanı (flex sütun); `style="top:60mm"` gibi bandın altından başlar; `.esnek` kalan yüksekliği doldurur |
| `{{alt|n}}` → `.alt` + `.ebru-alt` | altbilgi (ünite · sayfa adı · yıldız içinde sayfa no) + ebru kenar suyu |

### Temel parçalar
`.kart` (`.gol-z .keh-z .mer-z .kob-z .gum-z .kirec-z`, `.duz`), `.kart-bas`, `.et` (renk sınıfları), `.cip` (`.akce .koyu .gol .mer .kob .eksi .buyuk`),
`.yildiz`, `.vurgu`, `.kesir`, `.bento` (+ satır içi `grid-template-columns`), `.bento.dikey`, `.ara-bas`.

> `.et` **inline-block**'tur. `inline-flex` yapılırsa içindeki `<sub>`/`<sup>` ayrı flex öğesine dönüşür ve "N  A" gibi kopar.
> Aynı nedenle `.sonuc`, `.sik`, `.hisse`, `.cozum-defter` satırları blok/inline akışla kurulur.

### Konu (durak) sayfası
| Bileşen | Ne için |
|---|---|
| `.sohbet` + `.mesaj.(elif|yusuf|pamuk|zeynep)` (`.sag` = sağdan) | "#kıyı-sohbeti": 3–4 mesajla konu açılışı |
| `.kavram` | tanım kutusu (kobalt) |
| `.kiyidan` | günlük hayat / yerel bağlam kutusu |
| `.hazine` + `{{hno|H4|renk}}` + `{{sikke|sikke}}` | Hazine kartı (formül; kes, deftere yapıştır). Numara ünite boyunca sürer (H1…H10) |
| `.gorev` + `.baglam` + `.soru` + `ol.akis` + `.sonuc` | çözümlü görev; `.kose-mol` ile köşeye 3B molekül yüzdürülür |
| `.tuzak` → `.tuzak-ust` + `.tuzak-iddia` (`{{muhur|yanlis}}`) + `.tuzak-dogru` | Tuzak! (yanlış bilinen, üstü çizili, yıldız mühürlü) |
| `.hizli` + `.anahtar-ipucu` (ters yazı) + `.cevap-satir` | Hızlı görev: anahtar −10 akçe, cevap ters yazılı |
| `.medeniyet` + `{{kose}}` + `.med-bas` + `.zh` + `.metin` + `.not` | **Medeniyetimizden** (tezhipli): lacivert-altın çift çerçeve, ebru üst şeridi, dört köşebent, Amiri metin, Zeynep Hoca avatarı |
| `.harita-kart` + `{{info|mol_haritasi|kilitli/acik}}` | "göl üstünde köprüler" mol haritası |

### Hülasa, yan yollar, imtihan, final
| Bileşen | Ne için |
|---|---|
| `.ozetler` + `.ozet-kart` (`.koyu .gol .keh .mer .kob`) | 6 özet kart; ebru zemin üstünde |
| `.sandik` + `.sandik-izgara` | hazine sandığı: H1–H10 tek bakışta |
| `.muhasebe` + `{{cay|seviye|b}}` | Muhasebe: her ifade için Tamam/Yarım/Tekrar çay bardağı (öğrenci boyar) |
| `.meclis` + `.cozum-defter` + `.yorum` + `.hukum` | Meclis: hatalı çözüm, iki yorum, hüküm satırı |
| `.kissa` + `.kissa-bas` + `.kissa-ic` + `ul.yargi` + `.siklar` + `.hisse` | Kıssa: bağlam sorusu + "Kıssadan hisse" |
| `.merdiven` + `.basamaklar` + `.basamak` | Anahtar merdiveni (3 basamak, kademeli içeri kayar) |
| `.mesveret-izgara` + `.mesveret` + `{{sno|n}}` + `.oy` (`.yatay .uc`) | Meşveret (test) kartı: tahmin yüzdesi `%__`, karalama alanı |
| `.anahtar-izgara`, `.cozumler`, `.yan-anahtar` | cevaplar (durak etiketli anahtar, iki sütun çözüm, yan yol hızlı anahtarı) |
| `.ray-kart` + `{{info|akce_rayi}}`, `.unvanlar`, `table.defter`, `.nisan-say` | final: akçe rayı, Ahilik unvanları, akçe defteri, nişan sayımı |

---

## 6. İllüstrasyon kütüphanesi (`uretec/cizim/`)

Bütün fonksiyonlar **SVG metni döndürür**; gradyan/klip/maske tanımları verilen `Svg` nesnesinin `<defs>`'ine yazılır.
Koordinatlarda sahneler için 1 birim = 0,1 mm (bant 2100×460). `tohum` aynı kaldıkça çizim aynı kalır.

| Modül | Ne çizer | Başlıca fonksiyonlar |
|---|---|---|
| `temel.py` | altyapı | `Svg(onek)` (`lin`, `rad`, `klip`, `maske`, `desen`, `cikti`), `egri_d` (Catmull-Rom→Bezier), `selcuklu_yildizi`, `yildiz_noktalari`, `karis/acik/koyu`, `orta_nokta` (fraktal sırt), `deger_gurultusu` |
| `renkler.py` | palet | tokenlar, `ATOM`, `ATOM_R` |
| `sahne.py` | doğa parçaları | `gokyuzu(tema)`, `gunes` (hale), `ay`, `yildizlar`, `bulut` (kümülüs), `bulut_serit` (gün batımı stratus), `dag` (biçim: `sivri`/`volkan`/`kaldera`/`tepe`; gölgeli yamaç, sırt oyukları, kar örtüsü, kenar ışığı), `tepe_bandi`, `gol` (derinlik gradyanı + parıltı + güneş yolu), `yansima`, `dalga_cizgileri`, `kavak`, `agac` (meyveli), `cimen` (çiçekli), `sazlik`, `kaya`, `marti` (silüet/ayrıntılı), `kefal` (inci kefali), `damla_sicrama`, `tekne` (yelkenli/motorlu), `feribot` (vagonlu tren feribotu), `ev` |
| `yapilar.py` | simge yapı ve nesneler | `kumbet` (çokgen gövde, kör kemer, mukarnaslı kapı, piramit çatı), `mezar_tasi` (Ahlat şahidesi, yazısız oyma, likenler), `van_kalesi` (kalker kaya + sur + mazgal + burç + merdiven + bayrak), `kucuk_kale`, `iskele`, `fener`, `selale`, `gokkusagi`, `asma_kopru`, `semaver`, `cay_bardak_kucuk`, `cadir`, `koyun`, `obsidyen`, `hazini_terazisi`, `basit_terazi` (kefelere içerik konur) |
| `karakter.py` | karakterler | bkz. §7 |
| `molekul.py` | 3B moleküller | `molekul_svg(onek, AD, donus=(x°,y°,z°), etiket, iyon_etiket)`: H2O, CO2, O2, N2, CO, SO2, SO3, NH3, CH4, C2H6, C2H4, C3H8, He, C6H12O6 (β-glukopiranoz, sandalye), Na2CO3 (formül birimi + iyon yükleri), NaCl, CaCO3 · `cekirdek_ciz(p, n)` izotop çekirdeği · `kristal_nacl()` |
| `sus.py` | süs ve işaret | `cini_serit_ince/genis`, `zemin_gecme`, `tezhip_kose`, `kilim_serit` (basamaklı göz + elibelinde), `muhur("yanlis"|"dogru")`, `durak_rozeti`, `nisan(ikon, kurdele)` + `NISAN_IKON`, `cay_bardagi`, `IKON` + `ikon_sembolleri()` |
| `infografik.py` | sayısal grafikler | `avogadro_merdiveni` (log cetvel: düzine → kâğıt → insan → göl damlası → damladaki molekül → mol), `cekirdekler`, `bor_madalyon`, `mol_haritasi(kutle_acik)`, `karisim_kaplari`, `esit_kutle_terazi`, `hazini_kart`, `imbik`, `razi_araclari`, `halka_aleti`, `ozgul_agirlik`, `soda_resmi`, `bor_resmi`, `grafik_xy`, `raf_kaplari`, `merdiven_akce`, `elmas`, `balon`, `akce_rayi`, `unvan_rozeti` |
| `sahneler.py` | sayfa sahneleri | `edremit`, `gevas`, `tatvan`, `ahlat`, `adilcevaz`, `suphan`, `ercis`, `muradiye`, `iskele`, `kale_buyuk`, `kale_kapi`, `gece`, `final(nisanlar)`, `panorama()` (+ `DURAKLAR`, `_proje`) |
| `ebru.py` | ebru dokusu | `Teknede`: `damla`, `biz`, `dalga`, `battal`, `gelgit`, `tarak`, `resim` → JPEG; `ebru_gol`, `ebru_gun` |

### Sahne kompozisyon kuralı (başlık bantları)
- Bant 2100×460 birim, `preserveAspectRatio="xMidYMid slice"`.
- **Sol üst ≈ %55 × %75 gökyüzü/su olarak sakin bırakılır**; oraya `.levha` oturur. Odak yapı (kümbet, kale, iskele, şelale, karakterler) **sağ %40'ta** durur.
- Ufuk çizgisi y ≈ 260–300; alt kenarda `_cerceve_golge` hafif koyulaşma yapar.
- Işık yönü (`isik=-1` güneş solda) sahnedeki bütün dağ, ağaç, yapı çağrılarında aynı verilir.

### Panorama (açılış haritası)
`GOL_KIYI` gölün yaklaşık enlem–boylam kıyı çizgisi, `DURAKLAR` durakların konumu ve etiketleridir. `_proje(enlem, boylam)` eğik bakışlı
perspektif projeksiyon verir (uzak kıyı küçük, yakın büyük). Rota, duraklar arasından `ROTA_ARA` ara noktalarıyla kıyı boyunca kıvrılır.
Durak etiketleri HTML'dir (`{{panorama-etiket}}`); yerleri `kur.py` içindeki `yer` sözlüğünde mm cinsinden ofsettir.
**Başka bir yer için:** `GOL_KIYI` yerine o bölgenin kıyı/sınır çizgisi, `DURAKLAR` yerine yeni duraklar yazılır (ör. Pamukkale–Salda, Kapadokya vadileri).

### Ebru
Matematiksel marmorlama: damla bırakılınca eski çizgiler `P' = C + (P − C)·√(1 + r²/|P − C|²)` ile itilir; biz/tarak çekilince noktalar
çizgiye uzaklıkla azalan miktarda kayar. Alan korunur, sınırlar kesişmez; sonuç gerçek ebruya benzer (battal → gelgit → taraklı).
Çıktı JPEG'dir ve PDF'e **bir kez** gömülür (bütün sayfalarda aynı dosya).

---

## 7. Karakter sayfası (`karakter.py`, katalog: `katalog/karakterler.png`)

Bütün pozlar **aynı baş ve gövde parçalarından** kurulur; poz yalnızca kol/pati, aksesuar ve ifadeyi değiştirir.
Bu yüzden yüz, renk ve kıyafet her yerde aynıdır. Semboller `{{defs}}` ile sayfa başına bir kez gömülür; sayfada
`<svg viewBox="…"><use href="#…"/></svg>` (ya da `{{poz|sembol|sınıf}}`, `{{av|kim}}`) ile çağrılır.

| Karakter | Sabit görünüş | Ses |
|---|---|---|
| **Pamuk** (Van kedisi, maskot) | bembeyaz kabarık kürk, **izleyicinin solunda mavi, sağında kehribar göz**, pembe iç kulak, turkuaz tasma + gümüş akçe madalyonu, kabarık kuyruk | kısa, esprili, hep sayıyla konuşur; "Miyav!" |
| **Elif** (10. sınıf, Edremit) | koyu kumral uzun saç, kehribar saç bandı, mercan kazak, kehribar rozet | meraklı; "Neden?" diye sorar, bazen yanılır (Tuzak/Meclis'e bağlanır) |
| **Yusuf** (kimya kulübü, Erciş) | kısa siyah saç, yuvarlak gözlük, turkuaz kazak + beyaz yaka, kehribar altıgen rozet | sakin, adım adım, yerel benzetmelerle (kahvaltı tabağı, lokmalar) |
| **Zeynep Hoca** | topuz saç, kobalt gözlük, beyaz önlük + kobalt fular | yalnız "Medeniyetimizden" köşelerinde |

| Sembol | viewBox | Poz / ifade | Bu ünitede |
|---|---|---|---|
| `pamuk-selam` | 0 0 140 160 | el sallıyor, gülen gözler | s.1 karşılama |
| `pamuk-dusunen` | 0 0 140 160 | patisi çenede, soru balonu | s.8 meclis notu, Erciş sahnesi |
| `pamuk-sasiran` | 0 0 140 160 | iki pati havada, "!" | s.10 "Sırada" |
| `pamuk-akce` | 0 0 140 160 | göz kırpıyor, akçe tutuyor | s.6, s.12, kale kapısı sahnesi |
| `pamuk-kitap` | 0 0 140 160 | tezhipli kitap okuyor | s.7 kendime not |
| `pamuk-otur` | 0 0 140 160 | sade oturuş | yedek |
| `pamuk-bayrak` | 0 -40 170 200 | kale burcunda Türk bayrağıyla | s.14 final |
| `pamuk-yuzer` | 0 0 120 80 | gölde yüzüyor | s.1 harita |
| `pamuk-bas`, `pamuk-bas-gulen`, `pamuk-bas-sasiran` | 8 2 84 82 | yalnız baş | rozet/ikon için |
| `elif-soru`, `elif-dusunen`, `elif-aha`, `elif-sasiran` | 0 0 200 210 | yarım boy | Erciş sahnesi (`elif-soru`) |
| `yusuf-anlatan`, `yusuf-defter`, `yusuf-gulen` | 0 0 200 210 | yarım boy | Erciş sahnesi (`yusuf-anlatan`) |
| `zeynep-anlatan`, `zeynep-kitap` | 0 0 200 210 | yarım boy | yedek |
| `av-pamuk` | 0 0 40 40 | avatar | sohbet |
| `av-elif`, `av-yusuf`, `av-zeynep` | 0 0 200 210 | avatar | sohbet, Medeniyetimizden |
| `akce` | 0 0 40 40 | gümüş akçe (yazısız, sekiz köşeli yıldız) | HUD, hazine kartı |

Yeni poz eklemek: `pamuk_poz()` içine bir `elif poz == "…"` dalı (kol: `_kol`, pati: `_pati`, aksesuar) ve `semboller()` listesine ad ekle.
İnsanlar için `insan_poz()` (kol: `_insan_kol`, el: `_el`, ifade: `normal/gulen/sasiran/dusunen/soru/aha`).
**El jesti kuralı:** kalkan / anlatan el her zaman **açık avuçtur** (`_el(..., isaret=True)`: dört parmak + başparmak). Yumruktan tek
parmak çıkan el çizilmez; küçük boyutta yanlış bir el işareti gibi okunabilir. Yeni pozda eli 4× büyütüp ayrıca kontrol et.
Meclis/kıssa öğrenci adları (`YEREL-KIMLIK.md`): Ahmet, Zehra, Mehmet Emin, Rabia, Ömer, Hatice, Furkan, Esma.

---

## 8. Yer tutucular (`uretec/kur.py` → `YT`)

| Yer tutucu | Üretir |
|---|---|
| `{{defs}}` | gizli `<defs>`: logo ve sayfa no yıldızı, bütün karakter sembolleri, ikonlar |
| `{{zemin}}` `{{cini}}` `{{hud|n}}` `{{alt|n}}` | sayfa çerçevesi (HUD ve altbilgi metinleri `SAYFA` sözlüğünde, "şimdi" noktası `SIMDI`'de) |
| `{{sahne|ad}}` | `sahneler.ad()` |
| `{{panorama-etiket}}` | panorama üstündeki HTML durak etiketleri |
| `{{final}}` | final sahnesi (nişan çelengiyle) |
| `{{rozet|metin|ust|renk}}` | durak rozeti; `ust="-"` → büyük harf rozeti; renk `gol keh mer kob erg` |
| `{{hno|H4|renk}}` `{{sno|7|renk}}` | hazine / soru numarası rozeti |
| `{{mol|AD|rx,ry,rz|genişlik|e|ion}}` | 3B molekül (`e` element harfleri, `ion` Na₂CO₃ iyon yükleri) |
| `{{kristal|genişlik}}` | NaCl kristali |
| `{{muhur|yanlis}}` `{{muhur|dogru}}` | yıldız mühür |
| `{{nisan|ad|kurdele}}` | boyanacak nişan (`deste izotop kefal mizan karisim kale`) |
| `{{cay|seviye|b}}` | çay bardağı (`b` = boyanacak boş bardak) |
| `{{kose}}` | dört tezhip köşebendi (`.medeniyet` içinde) |
| `{{kilim}}` | kilim şeridi |
| `{{av|kim}}` `{{poz|sembol|sınıf}}` `{{ikon|ad|sınıf}}` `{{sikke|sınıf}}` | karakter, ikon, akçe |
| `{{info|fonksiyon|arg…}}` | `infografik.fonksiyon()` |

---

## 9. Oyun dili ve akçe (bu ünitenin sayıları)

Terimler `YEREL-KIMLIK.md`'dedir: Akçe · Durak/Yol · Nişan · Ahilik basamakları (Çırak → Kalfa → Usta → Mol Üstadı) · Van Kalesi / Büyük İmtihan ·
Hülasa · Hazine kartı · Anahtar · Tuzak! (mühür) · Kıssa (Kıssadan hisse) · Meclis · Meşveret · Muhasebe · Görev.

| Durak | Akçe | Kaynak |
|---|---|---|
| 1. durak | 100 | kavram 30 + tuzak 20 + H1 10 + hızlı 40 |
| 2.–5. durak | 150'şer | görevler + hazine kartları (10'ar) + tuzaklar + hızlı görev |
| Hülasa | 40 | muhasebe 6 satır |
| Meclis / Kıssa / Anahtar | 120'şer | 4×30 / 4×30 / 3×40 (anahtar −10) |
| Büyük İmtihan | 300 | 12×25 |
| **Toplam** | **1400** | eşikler: Kalfa 400 (%28,57) · Usta 800 (%57,14) · Mol Üstadı 1150 (%82,14) |

HUD çubuğu = o sayfanın başına kadar alınabilecek en çok akçe / 1400: `0 0 7 18 29 39 50 53 61 70 79 89 100 100`.
Başka üniteyi farklı toplamla kurarken `kur.py:SAYFA`, `dogrula.py` akçe bölümü, s.1 rozetleri, s.14 rayı ve defteri birlikte değiştirilir.

---

## 10. PDF ve baskı kuralları (deneyle bulundu)

- **CSS `background-image` ile tekrar eden SVG desen KULLANMA.** Chromium bunu PDF'te sayfa başına ≈ 400 KB raster desen yapar.
  Zemin geçmesi ve çini şeridi bu yüzden satır içi vektördür (tek path / 30 karo).
- Doku gerekiyorsa **tek bir JPEG**: aynı dosya bütün sayfalarda kullanıldığında PDF'e bir kez gömülür (ebru).
- Satır içi SVG gradyanları, maskeler, klipler vektör kalır. Yansıma maskesi ve mühür mürekkep maskesi sorunsuzdur.
- `filter` (blur, feTurbulence) kullanılmadı: hem PDF boyutunu hem render süresini şişirir. Yumuşaklık radyal gradyanla verilir.
- **PDF'te Type 3 font olmamalı** (matbaa güvenliği). Üç kaynağı var, üçü de kapatıldı:
  1. Değişken font → sabit kalınlıklı kopyalar (§4).
  2. Konturlu (`stroke`) SVG yazısı → Chromium bunu Type 3 yapar. Yazıya kontur verme; hale gerekiyorsa
     `temel.halolu_yazi(nitelik, metin, dolgu, hale, kalinlik)` kullan (8 yöne kaydırılmış koyu kopya + asıl yazı, aynı görünüm).
  3. Fontta olmayan sembol (✶ ★ ✓ ✗ → ⇄ gibi) kalın bağlamda yedek fonta düşüp sahte kalınlık alırsa Type 3 olur.
     Mühürde ✶ yerine • kullanılır; yeni sembolü ya fontta olan bir karakterle ya da SVG path ile çiz.
  Denetim: `pdffonts 02-mol-kavrami.pdf | grep -c "Type 3"` → `0` olmalı.
- Sonuç: 14 sayfa ≈ 8,0 MB (hedef ≤ 25 MB), bütün yazı tipleri CID TrueType olarak gömülü. `unite.html` ≈ 3,8 MB (satır içi SVG'ler).
- Her SVG'nin kimlik öneki benzersizdir (`Svg(onek)`, kur.py'de `_yeni()` sayacı); çakışırsa Chrome ilk tanımı kullanır ve renkler bozulur.

---

## 11. Başka üniteye / derse uyarlama (tarif)

1. Klasörü kopyala: `02-mol-kavrami/` → `NN-yeni-unite/` (`unite.html`, PDF, `onizleme/`, `gorsel/` üretilir; kopyalamaya gerek yok).
2. `uretec/kur.py` → `SAYFA` (HUD yeri, altbilgi adı, akçe çubuğu) ve `SIMDI` (ilerleme noktası) sözlüklerini yeni sayfa planına göre yaz.
3. Sahneleri seç ya da üret: `sahneler.py`'deki bir fonksiyonu kopyalayıp yer değiştir (ör. "Pamukkale" = `dag(bicim="tepe")` + beyaz traverten basamakları
   için `tepe_bandi` + turkuaz `gol`; "Kapadokya" = `kaya` ile peri bacaları; "Erzurum" = `kumbet` + karlı `dag`). Odak sağda, sol üst boş kuralına uy.
   Farklı gün saati için `gokyuzu` temasını değiştir.
4. Rotayı değiştir: `panorama()` içinde `GOL_KIYI` (bölge sınırı) ve `DURAKLAR`; etiket ofsetleri `kur.py:yt_panorama_etiket`.
5. Kimya dışı derslerde `molekul.py` yerine `infografik.py`'ye o dersin grafiklerini ekle (aynı `Svg` + palet + `B`/`T` yazı stilleri);
   fizik için `basit_terazi`, `feribot`, `selale` gibi nesneler zaten hazır.
6. Karakterler aynı kalır (Pamuk, Elif, Yusuf, Zeynep Hoca); yeni poz gerekiyorsa §7'deki gibi ekle.
7. `uretec/sablon.html` içeriğini yaz; bileşenleri §5'ten seç. Her durak sayfası: bant + levha (hedef, akçe, nişan) → sohbet → kavram/harita →
   hazine kartları → görevler → tuzak → hızlı görev → (Medeniyetimizden).
8. `uretec/dogrula.py`'yi yeni sorulara göre yaz (tek doğru şık + anahtarın sayfadan okunması dahil).
9. `python3 uretec/kur.py && python3 uretec/dogrula.py && uretec/olc.sh` → taşma `yok`; `onizleme/*.png`'lere tam boy bak.
10. Kataloğu güncelle: `python3 uretec/katalog.py`.

### Kontrol listesi (her render sonrası)
- [ ] `olc.sh` → `alan dışı … yok`, kutu taşması yok
- [ ] `dogrula.py` → `SONUÇ: hepsi doğru`
- [ ] Her PNG: kesik/üst üste binen yazı yok; alt simge/üst simge kopmamış (`N_A`, `CO₂`, `10²³`); SVG yazısı kutusundan taşmıyor
- [ ] Sahnede levhanın altında kalan odak öğe yok (odak sağda)
- [ ] Yarım boş alan yok (boşlukları `.karalama`, çözüm satırı ya da küçük illüstrasyonla doldur)
- [ ] Gövde ≥ 9,5 pt; metin alanları açık zeminde
- [ ] PDF ≤ 25 MB; `pdffonts … | grep -c "Type 3"` → 0
- [ ] Karakter elleri açık avuç (tek parmaklı yumruk yok)
