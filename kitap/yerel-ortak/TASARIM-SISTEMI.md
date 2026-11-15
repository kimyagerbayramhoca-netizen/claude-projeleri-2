# Kimya Rotası · Yerel Tasarım Sistemi ("Van Gölü" + tezhip) · ortak

Bu belge yeni tasarımın **ortak** tanımıdır: bütün yerel üniteler (`9-sinif-yerel/`, `10-sinif-yerel/`) ve kitap
çerçevesi (`yerel-cerceve/`) aynı çizim kütüphanesini, aynı `stil.css`'i, aynı kurucuyu (`kur_ortak.py`) ve aynı
basım betiğini (`render.js`) kullanır. Referans ünite: `10-sinif-yerel/02-mol-kavrami` (Yol 2 · Van Gölü Turu).

- Ana iskelet: **B · Van Gölü** (tur rotası, duraklar, akçe, Pamuk). Ödünç: **C · Medrese Defteri**'nden tezhipli
  "Medeniyetimizden" köşesi, YANLIŞ/DOĞRU yıldız mühürleri, tezhip köşebendi.
- Kimlik kuralları: `kitap/YEREL-KIMLIK.md` (terimler, karakterler, örnek havuzu, Medeniyetimizden bilgileri).
- Sayılar ve yazım: `kitap/YAZIM-REHBERI.md`. Rota tablosu ve ünite iskeleti: `yerel-ortak/ROTALAR.md`.
- Görsel kataloglar: `yerel-ortak/katalog/*.png` (`python3 kitap/yerel-ortak/katalog.py` ile yeniden üretilir).
- **Yeni ünite mi yapacaksın? Doğrudan §15'e git.**

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
   denetlenir; cevap anahtarı ve doğru şık işaretleri sayfadan (unite.html) okunup hesapla karşılaştırılır (§10).
5. **Tek doğruluk kaynağı.** Ünitenin künyesi `uretec/meta.json`'dadır (§9): hazine kartları sayfaya, Hülasa sandığına ve kesme
   yaprağına, nişanlar açılışa, finale ve nişan çelengine buradan basılır. Aynı bilgi iki yerde elle yazılmaz.
6. **Yerel ve saygılı.** Kurum/marka logosu, gerçek kişi görseli, kutsal metin hattı yok. Mezar taşlarında yazı yerine yalnızca
   geometrik oyma. Medeniyetimizden kutuları yalnızca `YEREL-KIMLIK.md`'deki doğrulanmış bilgilerle (el-Bîrûnî satranç tahtası bilgisi kullanılmaz).

---

## 2. Üretim hattı ve dosya düzeni

```
kitap/
  fontlar/                       OFL yazı tipleri (sabit kalınlıklı kopyalar static/ altında)
  yerel-ortak/                   ORTAK — ünite yazarı burayı DEĞİŞTİRMEZ (öneriyi raporuna yazar)
    TASARIM-SISTEMI.md           bu belge
    ROTALAR.md                   16 ünitenin rotası + ortak ünite iskeleti
    stil.css                     tasarım sistemi (tokenlar, çerçeve, bileşenler, öğretmen/fotokopi/baskı kuralları)
    cizim/                       illüstrasyon kütüphanesi (§6)
    kur_ortak.py                 ortak kurucu: yer tutucu motoru, HUD/altbilgi, genel yer tutucular, meta.json, ebru (§8)
    render.js                    unite.html → PDF + onizleme/sNN.png + taşma denetimi (+ varyantlar, §12)
    dogrula_ortak.py             doğrulama yardımcıları: mk, formul, tek_sik, sayfadan işaret okuma (§10)
    yeni_unite.py                yeni ünite iskeleti üretir (§15)
    katalog.py, katalog/*.png    görsel katalog
    fotograf.js                  HTML → PNG (katalog için)
    gorsel/ebru-*.jpg            ÜRETİLİR (kur_ortak, yoksa)
  9-sinif-yerel/  10-sinif-yerel/
    NN-unite-adi/
      README.md                  ünitenin kısa kılavuzu ve sayfa planı
      unite.html                 ÜRETİLİR (elle düzenleme; değişiklik kurulumda kaybolur)
      NN-unite-adi.pdf           ÜRETİLİR (+ -ogretmen, -fotokopi, -baski, -hazine-kartlari .pdf, §12)
      onizleme/sNN.png           ÜRETİLİR (deviceScaleFactor 2)
      uretec/
        sablon.html              sayfaların içeriği + {{yer-tutucular}}
        meta.json                künye ve tek doğruluk kaynağı (§9)
        kur.py                   İNCE kurucu: sayfa künyesi (SAYFA), HUD noktası (SIMDI), üniteye özel yer tutucular
        sahneler_unite.py        (isteğe bağlı) üniteye özel sahneler, nişan ikonları, bilgi grafikleri
        dogrula.py               sayısal doğrulama
        olc.sh                   taşma özeti
```

```sh
cd kitap/10-sinif-yerel/02-mol-kavrami
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh   # sonra onizleme/*.png'ye tek tek bak
```

`render.js` (`olc.sh` onu çağırır) iki tür sorunu listeler; ikisi de **boş** olmalıdır:
- **alan dışı:** içerik alanının (üstte 12 mm, altta 283 mm, yanlarda 10 mm) dışına çıkan öğe. Sahne bantları ve panorama `data-serbest` ile muaftır.
- **kutu taşması:** kart, balon, şık, levha, meşveret kartı, ızgara gibi kutulara sığmayan içerik. Bilerek yatay taşan dekorlu kapsayıcı `data-tasma-yatay` ile işaretlenir (yalnız Hülasa ebru zemini).

`render.js` kullanımı: `node kitap/yerel-ortak/render.js <ünite-klasörü> [sayfa…] [--pdfsiz]` → `<klasör>.pdf`, `onizleme/sNN.png`,
taşma raporu. Klasör verilmezse içinde bulunulan klasör kullanılır. Varyantlar için §12.

---

## 3. Renk tokenları (`stil.css :root` = `cizim/renkler.py`)

| Aile | Token | Değer | Kullanım |
|---|---|---|---|
| Zemin | `--kar` | `#FBFDFD` | Süphan karı: sayfa zemini |
| | `--kirec` | `#FFFDF7` | kireç beyazı: Medeniyetimizden, Üstad kartları |
| Mürekkep | `--obs` / `--obs-2` | `#1B1D26` / `#343947` | Nemrut obsidyeni: çizgi, metin, HUD |
| | `--soluk` / `--cizgi` | `#56636E` / `#CFDCE0` | ikincil metin / kesik ayraç |
| Van Gölü | `--gol` / `-k` / `-a` / `-aa` | `#13A3A6` / `#0A6C74` / `#DCF3F1` / `#EEF9F8` | ana renk, Yusuf, durak rozeti, kavram vurgusu |
| | `--derin` | `#0E4C5A` | sert gölge (`--golge: 1.1mm 1.3mm 0`) |
| Kehribar | `--keh` / `-k` / `-a` | `#F0A21A` / `#8C5500` / `#FFF0CF` | akçe, hazine, hızlı görev, Pamuk'un bir gözü |
| İznik mercanı | `--mer` / `-k` / `-a` | `#E2533D` / `#A12817` / `#FDE7E1` | Tuzak!, Elif, imtihan |
| İznik kobaltı | `--kob` / `-k` / `-a` | `#2B50B5` / `#1B3584` / `#E6ECFB` | kavram kutusu, Zeynep Hoca |
| Gün batımı | `--gun` / `--pembe` / `--erguvan` | `#FF7A3D` / `#FF5C8A` / `#7B3F8C` | sahne gökyüzü, Hülasa rozeti |
| Tezhip | `--altin` / `-k` / `-a` / `--lajver` | `#C9952B` / `#8A6212` / `#F6E7BF` / `#1D3A8A` | Medeniyetimizden, Üstad sayfası, rozet çerçeveleri, nişanlar |
| Çini yeşili | `--zumrut` | `#1F8A5B` | "Doğrusu", DOĞRU mührü tonu |
| Kefal gümüşü | `--gum` / `-k` / `-a` | `#A3B3BE` / `#586874` / `#EDF2F5` | ikincil etiket, akçe sikkesi |
| Öğretmen | `--ogr` / `--ogr-a` | `#D3121B` / `#FFE9E7` | yalnız öğretmen baskısı (§10) |
| Göz | `MAVI` (renkler.py) | `#3A8CF2` | Pamuk'un mavi gözü |

Yer tutucularda kısa renk adları (`kur_ortak.RENK`): `gol keh mer kob erg laj alt zum gum`.

Atom renkleri (CPK esinli, palete uyarlanmış; `renkler.ATOM`): H `#F3F5F8` · C `#3A3F4B` · O `#E2533D` · N `#2B50B5` · S `#F2C230` ·
Na `#8E5BD0` · Cl `#39A85A` · Ca `#9DB7C6` · He `#5ED3F3` · Mg `#5FC08A` · B `#F2A88A`.

Gökyüzü temaları (`sahne.GOK`): `safak`, `gun`, `altin`, `gunbatimi`, `alaca`, `gece`. Her sayfa farklı saatte geçer
(Mol: Edremit sabah → Gevaş öğle → Tatvan ikindi → Ahlat altın saat → … → Kale gün batımı → Cevaplar gece → Final gün batımı).

---

## 4. Tipografi ölçeği

| Rol | Aile | Ağırlık | Boyut |
|---|---|---|---|
| Açılış dev başlığı | Baloo Bhaijaan 2 | 800 | 54 pt (uzun ünite adında küçülür; `yeni_unite.dev_baslik`) |
| Durak levhası başlığı (`.levha h1`) | Baloo Bhaijaan 2 | 800 | 25 pt (küçük levha 21 pt) |
| Dev sayı (`.dev-sayi`) | Baloo Bhaijaan 2 | 800 | 34 pt (Hülasa'da 27 pt) |
| Ara başlık / özet kart başlığı | Baloo Bhaijaan 2 | 800 | 14 / 13 pt |
| Hazine formülü (`.hf`) | Baloo Bhaijaan 2 | 800 | 14,4 pt |
| Soru metni | Nunito | 800 | 10 pt (Üstad 9,8 pt) |
| Gövde, balon, çözüm, şık | Nunito | 400–700 | 9,5–10 pt |
| Etiket (`.et`), çip | Nunito | 900, BÜYÜK HARF, `letter-spacing .085em` | 7,8 pt |
| Medeniyetimizden metni | Amiri | 400/700 | 10,6 pt |
| Medeniyetimizden başlığı, mühür yazısı, Üstad etiketi | Reem Kufi | 700 | 9,4 pt / SVG |
| Yedek | DejaVu Sans / DejaVu Serif | | ⇄ gibi oklar için |

Yazı tipleri `kitap/fontlar/` (OFL) içinden `stil.css`'e göre göreli yolla yüklenir (`../fontlar/...`). SVG içinde
`font-family="Baloo Bhaijaan 2"` / `"Nunito"` / `"Reem Kufi"` doğrudan kullanılır (sayfa `@font-face`'leri geçerlidir).

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
| `{{zemin}}` → `svg.zemin` | çok açık Selçuklu yıldız geçmesi; **tek vektör path** (CSS desen değil, bkz. §14); kenarlardan 7,5 mm taşar |
| `{{hud|n}}` → `.hud` | koyu üst şerit: logo "Kimya Rotası 9/10", "<rota> · <yer>", ilerleme noktaları (duraklar ●, Hülasa ■, 3 yan yol ◆, kale), akçe kutusu + çubuk |
| `{{cini}}` → `svg.cini-serit` | HUD altında İznik çini şeridi (kobalt zemin, beyaz yıldız, turkuaz göbek, mercan nokta) |
| `.bant` (`.b30 .b36 .b40 .b62`, `.final-bant`) | kenardan kenara sahne bandı (varsayılan 46 mm) — `data-serbest` |
| `.levha` (`.keh .mer .kob .kucuk .ustad`) | bandın sol üstündeki beyaz başlık levhası: rozet + üst etiket + h1 + alt başlık + `.hedef` satırları |
| `.ic` | içerik alanı (flex sütun); `style="top:60mm"` gibi bandın altından başlar; `.esnek` kalan yüksekliği doldurur |
| `{{alt|n}}` → `.alt` + `.ebru-alt` | altbilgi ("Kimya Rotası N · Ünite" · sayfa adı · yıldız içinde sayfa no) + ebru kenar suyu |

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
| `{{hazine|H4}}` → `.hazine` | Hazine kartı (formül; kes, deftere yapıştır) — içerik **meta.json**'dan (§9). Numara ünite boyunca sürer |
| `.gorev` + `.baglam` + `.soru` + `ol.akis` + `.sonuc` | çözümlü görev; `.kose-mol` ile köşeye 3B molekül yüzdürülür |
| `.tuzak` → `.tuzak-ust` + `.tuzak-iddia` (`{{muhur|yanlis}}`) + `.tuzak-dogru` | Tuzak! (yanlış bilinen, üstü çizili, yıldız mühürlü) |
| `.hizli` + `.anahtar-ipucu` (ters yazı) + `.cevap-satir` | Hızlı görev: anahtar −10 akçe, cevap ters yazılı; `.cevap-kutu` içine `<span class="ogr">` (§10) |
| `.medeniyet` + `{{kose}}` + `.med-bas` + `.zh` + `.metin` + `.not` | **Medeniyetimizden** (tezhipli): lacivert-altın çift çerçeve, ebru üst şeridi, dört köşebent, Amiri metin, Zeynep Hoca avatarı |
| `.harita-kart` + `{{info|mol_haritasi|kilitli/acik}}` | "göl üstünde köprüler" mol haritası (Mol'e özel) |
| `.iskelet-alan` | iskeletin yer tutucu alanı (çizgili gri); içerik gelince silinir |

### Hülasa, yan yollar, imtihan, Üstad, cevaplar, final
| Bileşen | Ne için |
|---|---|
| `.ozetler` + `.ozet-kart` (`.koyu .gol .keh .mer .kob`) | 6 özet kart; ebru zemin üstünde |
| `.sandik` + `.sandik-izgara` + `{{sandik}}` | hazine sandığı: bütün H kartları tek bakışta (meta.json `kisa` alanı) |
| `.muhasebe` + `{{cay|seviye|b}}` | Muhasebe: her ifade için Tamam/Yarım/Tekrar çay bardağı (öğrenci boyar) |
| `.meclis` + `.cozum-defter` + `.yorum` + `.hukum` | Meclis: hatalı çözüm, iki yorum, hüküm satırı |
| `.kissa` + `.kissa-bas` + `.kissa-ic` + `ul.yargi` + `.siklar` + `.hisse` | Kıssa: bağlam sorusu + "Kıssadan hisse" |
| `.merdiven` + `.basamaklar` + `.basamak` | Anahtar merdiveni (3 basamak, kademeli içeri kayar) |
| `.mesveret-izgara` + `.mesveret` + `{{sno|n}}` + `.oy` (`.yatay .uc`) | Meşveret (test) kartı: tahmin yüzdesi `%__`, karalama alanı |
| `.ustad-izgara` + `.ustad-soru` + `.ustad-muhur` | Üstad soruları (§11) |
| `.anahtar-izgara`, `.cozumler`, `.yan-anahtar` | cevaplar (durak etiketli anahtar, iki sütun çözüm, yan yol hızlı anahtarı) |
| `.ray-kart` + `{{info|akce_rayi|ÜSTAD}}`, `.unvanlar`, `table.defter` (`.sik`), `{{nisan-sayim}}` | final: akçe rayı, Ahilik unvanları, akçe defteri, nişan sayımı (7–8 nişanda `.nisan-say.cok`) |

---

## 6. İllüstrasyon kütüphanesi (`yerel-ortak/cizim/`)

Bütün fonksiyonlar **SVG metni döndürür**; gradyan/klip/maske tanımları verilen `Svg` nesnesinin `<defs>`'ine yazılır.
Koordinatlarda sahneler için 1 birim = 0,1 mm (bant 2100×460). `tohum` aynı kaldıkça çizim aynı kalır.
**API yalnız eklemeyle büyür** (geriye uyumlu); ünite yazarı ortak modülü değiştirmez, kendi `uretec/sahneler_unite.py`'sine yazar.

| Modül | Ne çizer | Başlıca fonksiyonlar |
|---|---|---|
| `temel.py` | altyapı | `Svg(onek)` (`lin`, `rad`, `klip`, `maske`, `desen`, `cikti`), `egri_d` (Catmull-Rom→Bezier), `selcuklu_yildizi`, `yildiz_noktalari`, `karis/acik/koyu`, `orta_nokta` (fraktal sırt), `deger_gurultusu`, `halolu_yazi` |
| `renkler.py` | palet | tokenlar, `ATOM`, `ATOM_R` |
| `sahne.py` | doğa parçaları | `gokyuzu(tema)`, `gunes` (hale), `ay`, `yildizlar`, `bulut` (kümülüs), `bulut_serit` (gün batımı stratus), `dag` (biçim: `sivri`/`volkan`/`kaldera`/`tepe`; gölgeli yamaç, sırt oyukları, kar örtüsü, kenar ışığı), `tepe_bandi`, `gol` (derinlik gradyanı + parıltı + güneş yolu), `yansima`, `dalga_cizgileri`, `kavak`, `agac` (meyveli), `cimen` (çiçekli), `sazlik`, `kaya`, `marti` (silüet/ayrıntılı), `kefal` (inci kefali), `damla_sicrama`, `tekne` (yelkenli/motorlu), `feribot` (vagonlu tren feribotu), `ev` |
| `yapilar.py` | simge yapı ve nesneler | `kumbet`, `mezar_tasi`, `van_kalesi`, `kucuk_kale`, `iskele`, `fener`, `selale`, `gokkusagi`, `asma_kopru`, `semaver`, `cay_bardak_kucuk`, `cadir`, `koyun`, `obsidyen`, `hazini_terazisi`, `basit_terazi` |
| `karakter.py` | karakterler | bkz. §7 |
| `molekul.py` | 3B moleküller | `molekul_svg(onek, AD, donus=(x°,y°,z°), etiket, iyon_etiket)`: H2O, CO2, O2, N2, CO, SO2, SO3, NH3, CH4, C2H6, C2H4, C3H8, He, C6H12O6, Na2CO3, NaCl, CaCO3 · `cekirdek_ciz(p, n)` · `kristal_nacl()` |
| `sus.py` | süs ve işaret | `cini_serit_ince/genis`, `zemin_gecme`, `tezhip_kose`, `kilim_serit`, `muhur("yanlis"|"dogru")`, `durak_rozeti`, `nisan(ikon, kurdele)` + `NISAN_IKON` (`deste izotop kefal mizan karisim kale ustad`), `cay_bardagi`, `IKON` + `ikon_sembolleri()` |
| `infografik.py` | sayısal grafikler | `avogadro_merdiveni`, `cekirdekler`, `bor_madalyon`, `mol_haritasi(kutle_acik)`, `karisim_kaplari`, `esit_kutle_terazi`, `hazini_kart`, `imbik`, `razi_araclari`, `halka_aleti`, `ozgul_agirlik`, `soda_resmi`, `bor_resmi`, `grafik_xy`, `raf_kaplari`, `merdiven_akce`, `elmas`, `balon`, `akce_rayi(onek, ust_unvan="MOL ÜSTADI")`, `unvan_rozeti` |
| `sahneler.py` | sayfa sahneleri | Van turu: `edremit`, `gevas`, `tatvan`, `ahlat`, `adilcevaz`, `suphan`, `ercis`, `muradiye`, `iskele`, `kale_buyuk`, `kale_kapi`, `gece`, `final(nisanlar)`, `panorama()` (+ `DURAKLAR`, `_proje`). **Genel:** `ustad_bandi()` (Üstad sayfası, her ünitede aynı), `rota_haritasi(duraklar, kale)` (meta.json'dan genel tur haritası) |
| `ebru.py` | ebru dokusu | `Teknede`: `damla`, `biz`, `dalga`, `battal`, `gelgit`, `tarak`, `resim` → JPEG; `ebru_gol`, `ebru_gun` |

### Sahne kompozisyon kuralı (başlık bantları)
- Bant 2100×460 birim, `preserveAspectRatio="xMidYMid slice"`.
- **Sol üst ≈ %55 × %75 gökyüzü/su olarak sakin bırakılır**; oraya `.levha` oturur. Odak yapı (kümbet, kale, iskele, şelale, karakterler) **sağ %40'ta** durur.
- Ufuk çizgisi y ≈ 260–300; alt kenarda `_cerceve_golge` hafif koyulaşma yapar.
- Işık yönü (`isik=-1` güneş solda) sahnedeki bütün dağ, ağaç, yapı çağrılarında aynı verilir.
- Sahne içeriği x = 0…2100 dışına taşabilir: baskı sürümünde (§12) bandın kenarı 3 mm taşma payına uzar.

### Panorama (açılış haritası)
İki yol var:
1. **Genel:** `{{rota-haritasi}}` + `{{rota-etiket}}` (kur_ortak) — meta.json'daki durakların ve `kale_konum`'un enlem–boylamı eğik bakışlı
   stilize araziye izdüşürülür; rota kıvrılır, durak rozetleri ve kale rozeti konur; HTML etiketler çakışmayacak yere kendiliğinden yerleşir.
   İskelet bununla açılır.
2. **Bölgeye özel** (Mol: `panorama()`): `GOL_KIYI` gölün yaklaşık kıyı çizgisi, `DURAKLAR` durakların konumu ve etiketleri; `_proje(enlem, boylam)`
   eğik bakışlı izdüşüm. Etiketler HTML'dir; Mol'de `uretec/kur.py:panorama_etiket` mm ofsetleriyle yerleştirir.
   Başka bir yer için aynı yapıyla `uretec/sahneler_unite.py`'ye yaz (bölgenin kıyı/sınır çizgisi + kendi durakların).

### Ebru
Matematiksel marmorlama: damla bırakılınca eski çizgiler `P' = C + (P − C)·√(1 + r²/|P − C|²)` ile itilir; biz/tarak çekilince noktalar
çizgiye uzaklıkla azalan miktarda kayar. Alan korunur, sınırlar kesişmez; sonuç gerçek ebruya benzer (battal → gelgit → taraklı).
Çıktı JPEG'dir (`yerel-ortak/gorsel/`) ve PDF'e **bir kez** gömülür (bütün sayfalarda aynı dosya).

---

## 7. Karakter sayfası (`karakter.py`, katalog: `katalog/karakterler.png`)

Bütün pozlar **aynı baş ve gövde parçalarından** kurulur; poz yalnızca kol/pati, aksesuar ve ifadeyi değiştirir.
Bu yüzden yüz, renk ve kıyafet her yerde aynıdır. Semboller `{{defs}}` ile sayfa başına bir kez gömülür; sayfada
`<svg viewBox="…"><use href="#…"/></svg>` (ya da `{{poz|sembol|sınıf}}`, `{{av|kim}}`) ile çağrılır.

| Karakter | Sabit görünüş | Ses |
|---|---|---|
| **Pamuk** (Van kedisi, maskot) | bembeyaz kabarık kürk, **izleyicinin solunda mavi, sağında kehribar göz**, pembe iç kulak, turkuaz tasma + gümüş akçe madalyonu, kabarık kuyruk | kısa, esprili, hep sayıyla konuşur; "Miyav!" |
| **Elif** (10. sınıf, Edremit) | koyu kumral uzun saç, kehribar saç bandı, mercan kazak, kehribar rozet | meraklı; "Neden?" diye sorar, bazen yanılır (Tuzak/Meclis'e bağlanır) |
| **Yusuf** (kimya kulübü, Erciş) | kısa siyah saç, yuvarlak gözlük, turkuaz kazak + beyaz yaka, kehribar altıgen rozet | sakin, adım adım, yerel benzetmelerle |
| **Zeynep Hoca** | topuz saç, kobalt gözlük, beyaz önlük + kobalt fular | yalnız "Medeniyetimizden" köşelerinde |

| Sembol | viewBox | Poz / ifade |
|---|---|---|
| `pamuk-selam`, `pamuk-dusunen`, `pamuk-sasiran`, `pamuk-akce`, `pamuk-kitap`, `pamuk-otur` | 0 0 140 160 | el sallıyor · patisi çenede · iki pati havada · akçe tutuyor · tezhipli kitap · sade oturuş |
| `pamuk-bayrak` | 0 -40 170 200 | kale burcunda Türk bayrağıyla (final) |
| `pamuk-yuzer` | 0 0 120 80 | gölde yüzüyor |
| `pamuk-bas`, `pamuk-bas-gulen`, `pamuk-bas-sasiran` | 8 2 84 82 | yalnız baş |
| `elif-soru`, `elif-dusunen`, `elif-aha`, `elif-sasiran` · `yusuf-anlatan`, `yusuf-defter`, `yusuf-gulen` · `zeynep-anlatan`, `zeynep-kitap` | 0 0 200 210 | yarım boy |
| `av-pamuk` (0 0 40 40), `av-elif`, `av-yusuf`, `av-zeynep` (0 0 200 210) | | avatar |
| `akce` | 0 0 40 40 | gümüş akçe (yazısız, sekiz köşeli yıldız) |

Yeni poz eklemek (ortak kütüphaneye öneri olarak): `pamuk_poz()` içine bir `elif poz == "…"` dalı ve `semboller()` listesine ad.
**El jesti kuralı:** kalkan / anlatan el her zaman **açık avuçtur** (`_el(..., isaret=True)`). Yumruktan tek parmak çıkan el çizilmez.
Meclis/kıssa öğrenci adları (`YEREL-KIMLIK.md`): Ahmet, Zehra, Mehmet Emin, Rabia, Ömer, Hatice, Furkan, Esma.

---

## 8. Ortak kurucu ve yer tutucular (`kur_ortak.py`)

Ünitenin `uretec/kur.py`'si incedir; bütün iş `kur_ortak.Unite` sınıfındadır:

```python
import kur_ortak as KO
SAYFA = {1: ("Yola çıkış", "Van Gölü turu · yola çıkış", 0),          # no: (HUD yeri, altbilgi konusu, akçe çubuğu %)
         2: ("1. durak · <b>Edremit</b>", "1. durak · Neden mol?", 0), …}
SIMDI = {1: -1, 2: 0, 3: 1, …}       # HUD'da "şimdi" olan nokta: 0..durak-1 duraklar, durak = Hülasa, +1..+3 yan yollar, +4 kale, +5 hepsi tamam
u = KO.Unite(__file__, SAYFA, SIMDI)
u.yer_tutucu("panorama-etiket", panorama_etiket)    # üniteye özel yer tutucu (ya da ortak olanı geçersiz kılma)
u.calistir()
```

- **Motor:** şablondaki `{{ad|arg1|arg2…}}` → `fn(arg1, arg2…)`. Bilinmeyen ad ya da hata, hangi yer tutucuda olduğuyla birlikte durur.
  **HTML yorumları olduğu gibi kalır**, içlerindeki `{{…}}` çözülmez (iskeletteki örnek bileşenler yorumda durur).
- `{{sahne|ad|…}}` ve `{{info|ad|…}}` önce ünitenin `uretec/sahneler_unite.py` (ve `infografik_unite.py`) modülüne, sonra ortak
  `cizim/sahneler.py` / `cizim/infografik.py`'ye bakar. Üniteye özel nişan ikonları: `sahneler_unite.NISAN_IKON = {"ad": "<svg içi>"}`.
- Her SVG kimlik öneki sayaçla benzersizdir (`u.yeni("mol")` → `mol12`).
- Ebru dokuları `yerel-ortak/gorsel/` altında yoksa üretilir (`--ebru` ile yeniden).

| Yer tutucu | Üretir |
|---|---|
| `{{defs}}` | gizli `<defs>`: logo ve sayfa no yıldızı, bütün karakter sembolleri, ikonlar (+ `u.ek_defs`) |
| `{{zemin}}` `{{cini}}` `{{hud|n}}` `{{alt|n}}` | sayfa çerçevesi (HUD ve altbilgi metinleri `SAYFA`'da, "şimdi" noktası `SIMDI`'de; logo/ünite adı meta.json'dan) |
| `{{sahne|ad|arg…}}` | sahne (ünite modülü → `cizim/sahneler.py`); `{{sahne|ustad_bandi}}` Üstad bandı |
| `{{rota-haritasi}}` `{{rota-etiket}}` | meta.json duraklarından genel tur haritası ve çakışmasız durak etiketleri |
| `{{final}}` | final sahnesi; nişan çelengi meta.json `nisanlar`'dan |
| `{{rozet|metin|ust|renk}}` | durak rozeti; `ust="-"` → büyük harf rozeti; renk `gol keh mer kob erg laj` |
| `{{hno|H4|renk}}` `{{sno|7|renk}}` | hazine / soru numarası rozeti (Üstad: `{{sno|n|laj}}`) |
| `{{hazine|H4}}` | **hazine kartı, meta.json'dan** (başlık, formül ya da adımlar, not, renk) |
| `{{sandik}}` | Hülasa sandığının hücreleri (meta.json `kisa` ya da `formul`) |
| `{{nisan-izgara}}` `{{nisan-sayim}}` | açılıştaki nişan ızgarası, finaldeki nişan sayımı (meta.json `nisanlar`; sütun sayısı kendiliğinden) |
| `{{nisan|ikon|kurdele|renk}}` | tek nişan (`deste izotop kefal mizan karisim kale ustad` + ünitenin ikonları; renk meta.json'dan) |
| `{{meta|alan}}` | meta.json alanı (`unite`, `rota`, `tema`, `duraklar.0.yer` …) ya da hesap: `hazine_sayisi durak_sayisi nisan_sayisi akce_toplam sinif_adi` |
| `{{sayfa|13}}` · `{{sayfa|13|de}}` · `{{ek|13|de}}` | sayfa göndermesi (kitap kaymalı): `13` · `13’te` · `te`. Ekler: `de` (bulunma), `den`, `e`, `i`; Türkçe ses uyumuna göre (`6’da`, `40’ta`, `3’ü`) |
| `{{mol|AD|rx,ry,rz|genişlik|e|ion}}` | 3B molekül (`e` element harfleri, `ion` Na₂CO₃ iyon yükleri) |
| `{{kristal|genişlik}}` | NaCl kristali |
| `{{muhur|yanlis}}` `{{muhur|dogru}}` | yıldız mühür |
| `{{cay|seviye|b}}` | çay bardağı (`b` = boyanacak boş bardak) |
| `{{kose}}` | dört tezhip köşebendi (`.medeniyet` içinde) |
| `{{kilim}}` | kilim şeridi |
| `{{av|kim}}` `{{poz|sembol|sınıf}}` `{{ikon|ad|sınıf}}` `{{sikke|sınıf}}` | karakter, ikon, akçe |
| `{{info|fonksiyon|arg…}}` | bilgi grafiği (`fonksiyon(önek, *arg)`; sayı gibi görünen arg sayıya çevrilir) |

**Ortam değişkenleri** (kitap birleştirme betiği için):

| Değişken | Etki |
|---|---|
| `YEREL_SAYFA_BASLANGIC=37` | ünitenin 1. sayfası kitapta 37 olur: altbilgi numarası, `{{sayfa|n}}`, `{{ek|n}}`, panorama ve rota etiketlerindeki "s.N" kayar (ekler yeni sayıya göre seçilir) |
| `YEREL_CIKTI=/yol/x.html` | `unite.html` yerine oraya yazar; `stil.css` bağlantısı yeni yere göre düzeltilir (fotokopi: `x-fotokopi.html`) |

```sh
YEREL_SAYFA_BASLANGIC=37 YEREL_CIKTI=/tmp/kitap/mol.html python3 kitap/10-sinif-yerel/02-mol-kavrami/uretec/kur.py
node kitap/yerel-ortak/render.js /tmp/kitap/mol.html --pdfsiz
```

---

## 9. `meta.json` · ünitenin künyesi (tek doğruluk kaynağı)

```json
{"sinif": 10, "yol": 2, "rota": "Van Gölü Turu", "unite": "Mol Kavramı", "klasor": "02-mol-kavrami", "tema": "Tema 1 · Bölüm 2",
 "bolge": "Van", "merkez": {"enlem": 38.6, "boylam": 42.9},
 "duraklar": [{"no": 1, "yer": "Edremit", "baslik": "Neden mol?", "enlem": 38.425, "boylam": 43.30, "sayfa": 2, "akce": 100}],
 "kale": "Van Kalesi", "kale_konum": {"enlem": 38.50, "boylam": 43.40},
 "nisanlar": [{"ad": "Deste Ustası", "ikon": "deste", "renk": "gol", "aciklama": "1. durak · deste"},
              {"ad": "Üstad Mührü", "ikon": "ustad", "renk": "laj", "aciklama": "Üstad · 6/6 doğru", "bonus": true}],
 "hazine": [{"kod": "H1", "baslik": "Desteyi aç", "formul": "1 mol = N_A tane", "not": "N_A = 6,02·10^23 · +10 akçe", "durak": 1},
            {"kod": "H9", "renk": "kob", "sinif": "strateji", "baslik": "3 adımlık strateji", "adimlar": ["…", "…", "…"], "kisa": "x · toplam − x"}],
 "medeniyet": [{"ad": "el-Bîrûnî", "yil": "973–1048", "katki": "…", "sayfa": 3}],
 "kavramlar": [{"terim": "mol", "tanim": "…"}],
 "sayfa_sayisi": 15}
```

| Alan | Zorunlu | Ne / kim kullanır |
|---|---|---|
| `sinif`, `yol`, `rota`, `unite`, `klasor` | ✓ | logo ("Kimya Rotası 10"), HUD ("Van Gölü turu · …", rota adının son kelimesi küçük harfle; `hud` alanı ile değiştirilebilir), altbilgi, kesme yaprağı, kitap çerçevesi |
| `tema`, `bolge`, `merkez` | | künye, `{{meta|tema}}` |
| `duraklar[]` | ✓ | `no`, `yer`, `baslik`, `enlem`, `boylam` (+ isteğe bağlı `sayfa`, `akce`): HUD nokta sayısı, genel tur haritası ve etiketleri, içindekiler |
| `kale`, `kale_konum` | | Büyük İmtihan kalesi; konum verilirse tur haritasına kale rozeti |
| `nisanlar[]` | ✓ | `ad`, `ikon`, `renk` (`gol keh mer kob erg laj`), `aciklama`, `bonus`: açılış ızgarası, nişan sayımı, final çelengi |
| `hazine[]` | ✓ | `kod` (benzersiz), `baslik`, `formul` **ya da** `adimlar[]`, `not`, `renk` (hno rozeti; yoksa kehribar), `sinif` (ek CSS sınıfı, ör. `strateji`), `kisa` (sandık için kısa biçim), `durak` |
| `medeniyet[]` | | `ad`, `yil`, `katki`, `sayfa`: kitap dizini (sayfadaki kutu şablonda yazılır) |
| `kavramlar[]` | | `terim`, `tanim`: kitap sözlüğü |
| `sayfa_sayisi`, `akce_toplam` (1400), `hud` | | künye / HUD |

**Metin alanları HTML olabilir**; ayrıca etiket dışındaki metinde kısa yazım çalışır (`kur_ortak.zengin`):
`{H2O}` → H₂O (formül), `N_A`, `n_{atom}` → alt simge, `10^23`, `10^-23`, `^{2−}` → üst simge, `10²³`, `CO₂` (Unicode) → `<sup>`/`<sub>`.
Düz metin isteyen araçlar `kur_ortak.duz_metin(...)` kullanır.

---

## 10. Cevap işaretleme · öğretmen baskısı

Öğrenci baskısında **hiçbir şey değişmez**; öğretmen baskısı aynı `unite.html`'in `<html class="ogretmen">` ile basılmasıdır
(`render.js --ogretmen`, §12). İşaretler:

| İşaret | Nereye | Öğretmen baskısında |
|---|---|---|
| `data-soru="KOD"` | her soru kartı: `.kissa` (K1–K4), `.mesveret` (I1–I12), `.ustad-soru` (U1–U6), `.meclis` (M1–M4) | görünmez; `dogrula.py` sayfadaki doğru şıkkı bu kodla okur |
| `data-dogru` | doğru şık: `<div class="sik" data-dogru><b>C</b>…` · meşverette `<div data-dogru><b>D</b>…` (**açılış etiketinin son niteliği**, hemen ardından `<b>HARF</b>`) | şık kırmızı çerçeve, harf kırmızı daire |
| `data-dogru` | meclis: haklı yorum `<div class="yorum" data-dogru>`, hatalı satırın kutucuğu `<span class="kutucuk" data-dogru></span>2` | kutucuk kırmızı, içinde beyaz tik |
| `<span class="ogr">…</span>` | öğretmene özel cevap/çözüm: `.cevap-kutu` (CEVABIN), `.karalama`, `.hukum .cizgili` (neden, doğrusu), `.cozum-alani > div` (merdiven), `.bos-satir` | kırmızı (`--ogr`); öğrenci baskısında `display:none` → **yerleşimi hiç etkilemez** |

Kırmızı metin yerleşimi bozmaz: karalama, hüküm çizgisi ve merdiven satırında mutlak konumla üste basılır; sığmayacak kadar uzun yazma
(karalamada 2–3 kısa satır). Öğretmen baskısının her sayfasında sağ üstte "ÖĞRETMEN NÜSHASI" sekmesi vardır.

`dogrula_ortak` yardımcıları: `isaretli_dogrular(html)` → `{kod: ['C']}`, `sik_harfleri(html)`, `sayfa_isaretleri_ayni(html, {"I1": "D", …})`
(her kartta tek işaret + A–E beş şık), `meclis_hukumleri(html)` → `{kod: (kişi, satır)}`, `anahtar_izgarasi(html)` (Cevaplar ızgarası),
`ogretmen_metinleri(html)`. Böylece soru sayfasındaki işaret, Cevaplar sayfasındaki anahtar ve hesap üçlüsü birbirine kilitlenir.

---

## 11. Üstad soruları sayfası (bonus; her ünitede aynı kimlik)

ROTALAR.md §2.6: Büyük İmtihan'dan sonra, Cevaplar'dan önce **1 sayfa**; YKS/AYT tarzı **6 zor soru**, 5 şık, tek doğru, cevaplar dağınık;
en az birinde grafik ya da tablo. **1400 akçeye dahil değildir.** 6/6 yapan "Üstad Mührü" nişanını (`ikon: ustad`, `renk: laj`,
`bonus: true`) boyar; nişan açılışta, nişan sayımında ve final çelenginde görünür. Çözümler Cevaplar sayfasına da yazılır.

```html
<section class="sayfa sNN ustad-sayfa">  {{zemin}} {{hud|NN}} {{cini}}
  <div class="bant b40" data-serbest>{{sahne|ustad_bandi}}
    <div class="levha ustad">{{rozet|Ü|-|laj}}<div><div class="ust">Üstad soruları · bonus · YKS/AYT tarzı</div><h1>Üstad <em>soruları</em></h1>…</div></div></div>
  <main class="ic" style="top:54mm">
    <div class="ustad-izgara esnek">                                   <!-- 2 sütun × 3 satır, sütun sütun akar -->
      <div class="ustad-soru" data-soru="U1">
        <div class="ustad-bas">{{sno|1|laj}}<span class="et">İzotop · tanecik</span><span class="ustad-zor">AYT</span></div>
        <p class="soru">…</p>   <!-- şekil: <div class="ustad-sekil">{{info|…}}</div> · tablo: <table class="ustad-tablo"> -->
        <div class="karalama"><span class="ogr">kısa çözüm</span></div>
        <div class="siklar">…<div class="sik" data-dogru><b>C</b>…</div>…</div>   <!-- uzun şıklarda class="siklar iki" -->
      </div> …
    </div>
    <div class="ustad-muhur">{{nisan|ustad}}<div>…</div><div class="skor-kutu">Doğru <span class="kk"></span> / 6</div></div>
  </main> {{alt|NN}} </section>
```

Görünüş: lacivert medrese gecesi bandı (`ustad_bandi`: altın Selçuklu geçmesi, ışıklı revak, altın mühür madalyonu), kireç zeminli
lacivert-altın çift çerçeveli kartlar, Reem Kufi "AYT" etiketi. HUD noktası "hepsi tamam", akçe çubuğu %100.

---

## 12. Varyantlar (öğretmen, fotokopi, baskı, hazine kartları)

Bu bölüm adım 2'de tamamlanır (`render.js --hepsi`).

---

## 13. Oyun dili ve akçe

Terimler `YEREL-KIMLIK.md`'dedir: Akçe · Durak/Yol · Nişan · Ahilik basamakları (Çırak → Kalfa → Usta → Üstad) · Kale / Büyük İmtihan ·
Hülasa · Hazine kartı · Anahtar · Tuzak! (mühür) · Kıssa (Kıssadan hisse) · Meclis · Meşveret · Muhasebe · Görev · Üstad soruları.

| Bölüm | Akçe | Kaynak |
|---|---|---|
| Duraklar | 700 | 1. durak 100; kalanlar eşit (5 durak: 4×150 · 4 durak: 3×200 · 6 durak: 5×120) |
| Hülasa | 40 | muhasebe 6 satır |
| Meclis / Kıssa / Anahtar | 120'şer | 4×30 / 4×30 / 3×40 (anahtar −10) |
| Büyük İmtihan | 300 | 12×25 |
| Üstad soruları | — | bonus: akçe yok, Üstad Mührü |
| **Toplam** | **1400** | eşikler: Kalfa 400 (%28,57) · Usta 800 (%57,14) · Üstad 1150 (%82,14) |

HUD çubuğu = o sayfanın başına kadar alınabilecek en çok akçe / 1400 (Mol: `0 0 7 18 29 39 50 53 61 70 79 89 100 100 100`).
Toplam değişirse `kur.py:SAYFA`, `dogrula.py` akçe bölümü, açılış rozetleri, final rayı ve defteri birlikte değişir.

---

## 14. PDF ve baskı kuralları (deneyle bulundu)

- **CSS `background-image` ile tekrar eden SVG desen KULLANMA.** Chromium bunu PDF'te sayfa başına ≈ 400 KB raster desen yapar.
  Zemin geçmesi ve çini şeridi bu yüzden satır içi vektördür (tek path / 30 karo).
- Doku gerekiyorsa **tek bir JPEG**: aynı dosya bütün sayfalarda kullanıldığında PDF'e bir kez gömülür (ebru).
- Satır içi SVG gradyanları, maskeler, klipler vektör kalır. Yansıma maskesi ve mühür mürekkep maskesi sorunsuzdur.
- `filter` (blur, feTurbulence) kullanılmadı: hem PDF boyutunu hem render süresini şişirir; CSS `filter` PDF'te rasterleşir.
  Yumuşaklık radyal gradyanla verilir; siyah-beyaz sürüm de filtreyle değil, kurulumda palet eşlemesiyle yapılır (§12).
- **PDF'te Type 3 font olmamalı** (matbaa güvenliği). Üç kaynağı var, üçü de kapatıldı:
  1. Değişken font → sabit kalınlıklı kopyalar (§4).
  2. Konturlu (`stroke`) SVG yazısı → Chromium bunu Type 3 yapar. Yazıya kontur verme; hale gerekiyorsa
     `temel.halolu_yazi(nitelik, metin, dolgu, hale, kalinlik)` kullan (8 yöne kaydırılmış koyu kopya + asıl yazı, aynı görünüm).
  3. Fontta olmayan sembol (✶ ★ ✓ ✗ → ⇄ gibi) kalın bağlamda yedek fonta düşüp sahte kalınlık alırsa Type 3 olur.
     Mühürde ✶ yerine • kullanılır; yeni sembolü ya fontta olan bir karakterle ya da SVG path / CSS kenarlığıyla çiz (öğretmen tiki CSS'tir).
  Denetim: `pdffonts <klasor>.pdf | grep -c "Type 3"` → `0` olmalı.
- Mol: 14 sayfa ≈ 8,0 MB (hedef ≤ 25 MB), bütün yazı tipleri CID TrueType olarak gömülü. `unite.html` ≈ 3,8 MB (satır içi SVG'ler).
- Her SVG'nin kimlik öneki benzersizdir (`Svg(onek)`, `u.yeni()` sayacı); çakışırsa Chrome ilk tanımı kullanır ve renkler bozulur.

---

## 15. Yeni ünite nasıl yapılır (tarif)

1. **İskeleti üret** (klasör var ise dokunmaz):
   ```sh
   python3 kitap/yerel-ortak/yeni_unite.py 9-sinif-yerel 01-gunluk-hayatta-kimya --yol 1 --rota "İznik–Bursa Yolu" \
           --unite "Günlük Hayatta Kimya" --kale "Bursa Hisarı" --durak 5 --tema "Tema 1 · Bölüm 1" --merkez 40.2,29.3
   cd kitap/9-sinif-yerel/01-gunluk-hayatta-kimya && python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh
   ```
   Hemen kurulur ve basılır: ROTALAR.md §2'deki bütün sayfa türleri (açılış, N durak, Hülasa, Meclis, Kıssa, Anahtar merdiveni,
   Büyük İmtihan 1–2, Üstad, Cevaplar, Final; 4/5/6 durakta 14/15/16 sayfa), örnek bileşenler ve yorumlu kullanım notlarıyla.
2. **`uretec/meta.json`'u doldur:** gerçek duraklar (yer, başlık, enlem–boylam, sayfa, akçe), kale ve konumu, nişanlar (ikon adları:
   ortak `deste izotop kefal mizan karisim kale ustad` ya da `sahneler_unite.NISAN_IKON`), hazine kartları, medeniyet, kavramlar.
   Açılıştaki tur haritası ve etiketleri buradan kendiliğinden güncellenir.
3. **`uretec/kur.py`:** `SAYFA`'daki HUD yer adları ve altbilgi konuları (akçe çubuğu ve `SIMDI` iskelette hesaplı gelir).
4. **Sahneler (`uretec/sahneler_unite.py`):** `ornek_sahne`'yi kopyalayıp her durağın gerçek yerini çiz (ROTALAR.md'deki yer–kimya bağı);
   §6 kompozisyon kuralı: odak sağda, sol üst levhaya boş, ışık yönü tutarlı, tohum sabit, önek benzersiz. Farklı gün saati için `gokyuzu` teması.
   Şablonda `{{sahne|ornek_sahne|…}}` yerine `{{sahne|senin_sahnen}}`. İstersen açılışa bölge panoraması (§6).
5. **İçerik (`uretec/sablon.html`):** bileşenleri §5'ten seç. Her durak: bant + levha (hedef, akçe, nişan) → sohbet → kavram →
   hazine kartları (`{{hazine|Hn}}`) → görevler → Tuzak → hızlı görev → (Medeniyetimizden). "Yer tutucu" alanlarını doldur; yarım boş alan bırakma.
   Medeniyetimizden yalnız `YEREL-KIMLIK.md`'deki doğrulanmış bilgiyle. Sayfa göndermesi `s.{{sayfa|n}}` ile (kitapta kayar).
6. **Sorular ve cevap işaretleri (§10):** her soru kartına `data-soru`, doğru şıkka `data-dogru`, CEVABIN/karalama/hüküm/merdivene
   `<span class="ogr">`; Cevaplar sayfasında anahtar ızgarası + bütün çözümler (Üstad dahil). İmtihanda A–E her harf en az bir kez.
7. **Doğrulama (`uretec/dogrula.py`):** her sayıyı `dogrula_ortak` yardımcılarıyla yeniden hesapla (`mk("C6H12O6")`, `tek_sik`, `yargi`),
   sayfadaki işaretleri ve anahtarı karşılaştır, akçe toplamını denetle → `SONUÇ: hepsi doğru`.
8. **Bas ve bak:** `bash uretec/olc.sh` → `alan dışı … yok`, kutu taşması yok; `onizleme/*.png`'lere **tam boy** bak (kontrol listesi aşağıda).
9. **Varyantlar:** `node <yerel-ortak>/render.js . --hepsi` (öğretmen, fotokopi, baskı, hazine kartları; §12).
10. Ortak kütüphaneye eklenmesini istediğin bir şey (yeni poz, yapı, bileşen) olursa ortak dosyayı değiştirme; raporunda öner.

### Kontrol listesi (her render sonrası)
- [ ] `olc.sh` → `alan dışı … yok`, kutu taşması yok
- [ ] `dogrula.py` → `SONUÇ: hepsi doğru`
- [ ] Her PNG: kesik/üst üste binen yazı yok; alt simge/üst simge kopmamış (`N_A`, `CO₂`, `10²³`); SVG yazısı kutusundan taşmıyor
- [ ] Sahnede levhanın altında kalan odak öğe yok (odak sağda)
- [ ] Yarım boş alan yok (boşlukları `.karalama`, çözüm satırı ya da küçük illüstrasyonla doldur)
- [ ] Gövde ≥ 9,5 pt; metin alanları açık zeminde
- [ ] PDF ≤ 25 MB; `pdffonts … | grep -c "Type 3"` → 0
- [ ] Karakter elleri açık avuç (tek parmaklı yumruk yok)
- [ ] Öğretmen baskısında her soruda tek kırmızı şık; kırmızı metin kutusundan taşmıyor
