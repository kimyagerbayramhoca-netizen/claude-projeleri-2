# Kimya Rotası · Yerel Tasarım Sistemi ("Van Gölü" + tezhip) · ortak

Bu belge yeni tasarımın **ortak** tanımıdır: bütün yerel üniteler (`9-sinif-yerel/`, `10-sinif-yerel/`) ve kitap
çerçevesi (`yerel-cerceve/`) aynı çizim kütüphanesini, aynı `stil.css`'i, aynı kurucuyu (`kur_ortak.py`) ve aynı
basım betiğini (`render.js`) kullanır. Referans ünite: `10-sinif-yerel/02-mol-kavrami` (Yol 2 · Van Gölü Turu).

- Ana iskelet: **B · Van Gölü** (tur rotası, duraklar, akçe, Pamuk). Ödünç: **C · Medrese Defteri**'nden tezhipli
  "Medeniyetimizden" köşesi, YANLIŞ/DOĞRU yıldız mühürleri, tezhip köşebendi.
- Kimlik kuralları: `kitap/YEREL-KIMLIK.md` (terimler, karakterler, örnek havuzu, Medeniyetimizden bilgileri).
- Sayılar ve yazım: `kitap/YAZIM-REHBERI.md`. Rota tablosu ve ünite iskeleti: `yerel-ortak/ROTALAR.md`.
- Görsel kataloglar: `yerel-ortak/katalog/*.png` (`python3 kitap/yerel-ortak/katalog.py` ile yeniden üretilir).
- **Yeni ünite mi yapacaksın? Doğrudan §15'e git.** Yaygınlaştırılan yeni bileşenler (Hap Bilgi ailesi, konu karakterleri,
  sınıf paletleri, katla, 3B): **§16**; canlı örnek `yerel-ortak/katalog/bilesenler/uretec/sablon.html`.

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
    fotokopi.py                  fotokopi varyantı: SVG renklerini kurulumda griye eşler (§12)
    hazine_yapragi.py            meta.json H kartlarından A4 kesme yaprağı (§12)
    pdf_kutular.py               baskı PDF'ine TrimBox/BleedBox yazar (pypdf; §12)
    tema.py                      sınıf paletleri (Çini ve Toprak, Göl ve Rasathane): kurulumda palet eşlemesi (§16.3)
    katalog.py, katalog/*.png    görsel katalog
    katalog/bilesenler/uretec/   yeni bileşenlerin deneme ünitesi (8 sayfa; §16 · çıktıları git'e girmez)
    fotograf.js                  HTML → PNG (katalog için)
    gorsel/ebru-*.jpg            ÜRETİLİR (kur_ortak, yoksa) · ebru-gol-<palet>.jpg (tema.py) · test-yazi/derinlik.png (3B gözlük testi)
  9-sinif-yerel/  10-sinif-yerel/
    NN-unite-adi/
      README.md                  ünitenin kısa kılavuzu ve sayfa planı
      unite.html                 ÜRETİLİR (elle düzenleme; değişiklik kurulumda kaybolur)
      NN-unite-adi.pdf           ÜRETİLİR (+ -ogretmen, -fotokopi, -baski, -hazine-kartlari .pdf, §12)
      onizleme/sNN.png           ÜRETİLİR (deviceScaleFactor 2)
      gorsel/                    ÜRETİLİR yalnız meta.json "uc_boyut" varsa: ana-/duz-*.png + uc-boyut.json (§16.5)
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

> **Yeni bileşenler** (stil.css §37–§44, belge §16): Hap Bilgi ailesi (`.hb.hb-hap|kural|unutma|radar|dikkat|kilit`),
> `.sohbet-serit`, çizgi roman (`.roman-kart .roman .pano`), `.bakista`, `.kendini-dene`, `.ikili-kart .ikili`,
> `.tahmin-kart .tahmin`, konu karakteri `svg.konu-k`; katla (kat sayfası, karma sayfa, köşe sineması, köşeyi katla); 3B (`.kart.ub`).

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
SVG'de yazı tipi adı **tırnakla** yazılır: `font-family="'Baloo Bhaijaan 2'"` (tırnaksız "…2" geçersiz CSS'tir, yazı Nunito'ya düşer; §14).

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
| `konu_karakterleri.py` | konu karakterleri (§16.1) | 51 sembol `kk-*` (atom modelleri, tanecikler, fotonlar, iyonlar, 7 gaz × 3 ifade); `semboller(gerekli)`, `kimlikler()`, `vb(kimlik)`, `kullan(kimlik, x, y, w)` (SVG içinde `<use>`), `nm_renk(nm)` |
| `hap_bilgi.py` | Hap Bilgi ikonları (§16.2) | `IKON` (`hap yildiz radar dikkat anahtar delik carpi tik ciftok`), `ikon(ad, cls)`, `ok()`, `siklik(dolu, toplam)`, `yildiz_satir(n)` |
| `katla.py` | katla sayfaları (§16.4) | `bag_sayfasi`, `tepkime_sayfasi` (+ `BAG`, `TEPKIME` satırları), `kare(i)` + `film_izgara()` (köşe sineması), `kose_on`, `kose_arka(cevap)`, `kose_adimlar`, `kose_harita`, `ikon`, `robot`, `kapi`, `zemin14` · yazı genişliği fontTools ile |
| `uc_boyut.py` | 3B anaglif motoru (§16.5) | `Yapi`, kurucular (`ch4 nh3 h2o co2 bf3 nacl elmas grafit buz gaz_kutusu mol_kupu hidrasyon`), `uret`, `duz_resim`, `KATALOG`, `unite_gorselleri(klasor, liste)` (imzalı önbellek), `gozluk_testleri()` · numpy + PIL |
| `gozluk.py` | 3B gözlük sayfası çizimleri | `bant_atolye` (sahne), `nasil_calisir`, `gozluk_sablonu` (gerçek ölçü), `ub_ikon(onek, ad)` (`gozluk cetvel duz saat damla goz`) |

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
| `{{hud|n|kat}}` `{{alt|n|kat}}` `{{alt|n|kose-on}}` `{{alt|n|kose-arka}}` | katla sayfalarının çerçevesi (§16.4); ikinci argümansız biçim aynen eskisi gibi |
| `{{kk|…}}` `{{hbi|…}}` `{{ok}}` `{{siklik|…}}` · katla · 3B | yeni bileşenlerin yer tutucuları: tam liste **§16.7** |

`{{rozet|✓|-}}` ve `{{rozet|★|-}}`: Baloo'da ✓ ★ yok; rozet bunları yazı yerine şekille çizer (Type 3 olmasın, §14).
`{{hno|H10}}`: üç haneli kod kendiliğinden küçük yazılır (23 birim; daireye sığar).

**Ortam değişkenleri** (kitap birleştirme betiği için):

| Değişken | Etki |
|---|---|
| `YEREL_SAYFA_BASLANGIC=37` | ünitenin 1. sayfası kitapta 37 olur: altbilgi numarası, `{{sayfa|n}}`, `{{ek|n}}`, panorama ve rota etiketlerindeki "s.N" kayar (ekler yeni sayıya göre seçilir) |
| `YEREL_CIKTI=/yol/x.html` | `unite.html` yerine oraya yazar; `stil.css` bağlantısı yeni yere göre düzeltilir (fotokopi: `x-fotokopi.html`) |

```sh
YEREL_SAYFA_BASLANGIC=37 YEREL_CIKTI=/tmp/kitap/mol.html python3 kitap/10-sinif-yerel/02-mol-kavrami/uretec/kur.py
node kitap/yerel-ortak/render.js /tmp/kitap/mol.html --pngsiz     # yalnız /tmp/kitap/mol.pdf
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
| `palet` | | sınıf paleti: 9. sınıf `"cini-toprak"` (Çini ve Toprak), 10. sınıf `"gol-rasathane"` (Göl ve Rasathane). Varsa unite.html (öğrenci, öğretmen, baskı) ve hazine yaprağı bu paletle kurulur; fotokopi paletsiz. **Yoksa çıktı hiç değişmez** (§16.3) |
| `uc_boyut` | | 3B yapı listesi: `["ch4", "nacl", {"ad": "ch4-yan", "yapi": "ch4", "donus": [[60, 10, 0]], "en": 55, "yuk": 40, "duz": [22, 19]}]` → ünitenin `gorsel/` klasörüne PNG'ler; `{{ana|ad}}`, `{{duz|ad}}` (§16.5) |

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

Kırmızı metin yerleşimi bozmaz: karalama, hüküm çizgisi ve merdiven satırında mutlak konumla üste basılır; sığmayacak kadar uzun yazma:
karalamada 1–2 kısa satır (dar karalamada tek satır ≈ 40 harf), meclis NEDEN çizgisinde ≤ 12 harf (≈ 17 mm; ör. “çeşit sayılmış”),
DOĞRUSU çizgisinde ≤ 45 harf, merdiven satırında ≤ 50 harf. `render.js --ogretmen` taşan kırmızı metni sayfa ve metinle bildirir. Öğretmen baskısının her sayfasında sağ üstte "ÖĞRETMEN NÜSHASI" sekmesi vardır.

Yeni bileşenlerin işaretleri (§16.6): Kendini dene `.yaz > .ogr` · Şifreli Kapı `ol.sk-sec > li[data-dogru]` + `.sifre > span > .ogr` ·
Çeldirici Röntgeni `.rn-sec > div[data-dogru]` · Robot yanıldı mı? `.bot-cevap li[data-dogru]` (hatalı cümle) · Heybe ve öbür
yazı satırları `.yaz-satir > .ogr` · kat sayfası SVG içinde `<g class="ogr-svg" data-katla data-urun data-tur>` (kendiliğinden) ·
köşeyi katla `.bosluk > .ogr`, `.karalama > .ogr`.

`dogrula_ortak` yardımcıları: `isaretli_dogrular(html)` → `{kod: ['C']}`, `sik_harfleri(html)`, `sayfa_isaretleri_ayni(html, {"I1": "D", …})`
(her kartta tek işaret + A–E beş şık), `meclis_hukumleri(html)` → `{kod: (kişi, satır)}`, `anahtar_izgarasi(html)` (Cevaplar ızgarası),
`ogretmen_metinleri(html)`. Böylece soru sayfasındaki işaret, Cevaplar sayfasındaki anahtar ve hesap üçlüsü birbirine kilitlenir.
Yeni bileşenler için: `kendini_dene` / `kendini_dene_ayni`, `sifreli_kapi` / `sifreli_kapi_ayni(html, "PROTON")`,
`celdirici_rontgeni` / `celdirici_ayni`, `robot_hatalari` / `robot_ayni`, `katla_cevaplari` / `katla_ayni`,
`uc_boyut_resimleri(html, html_yolu)` (PNG var mı, mm ölçüsü = piksel / 300 dpi mi) — §16.6.

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

Tek komut bütün çıktıları üretir (ünite klasöründen ya da herhangi bir yerden):

```sh
node kitap/yerel-ortak/render.js <ünite-klasörü> --hepsi            # önce python3 uretec/kur.py --hepsi, sonra beş PDF
node kitap/yerel-ortak/render.js <ünite-klasörü> --hepsi --onizleme  # + varyant PNG'leri: onizleme/varyant/<ad>/sNN.png
node kitap/yerel-ortak/render.js <ünite-klasörü> --ogretmen          # tek tek: --ogretmen --fotokopi --baski --hazine
```

| PDF | Ne | Nasıl üretilir |
|---|---|---|
| `<klasör>.pdf` | öğrenci baskısı (A4) + `onizleme/sNN.png` + taşma raporu | `unite.html` |
| `<klasör>-ogretmen.pdf` | öğretmen nüshası: doğru şıklar kırmızı çerçeve + kırmızı harf, CEVABIN kutuları dolu, meclis hükmü (haklı kişi, satır, neden, doğrusu), merdiven çözüm satırları, karalamalarda kısa çözümler; her sayfada "ÖĞRETMEN NÜSHASI" sekmesi | aynı `unite.html`, `<html class="ogretmen">` (stil.css §31); işaretler §10. render.js kırmızı metnin kutusundan taşmasını ayrıca denetler |
| `<klasör>-fotokopi.pdf` | siyah-beyaz fotokopi ana nüshası: metin saf siyah; kutular beyaz/çok açık gri, siyah çerçeve; koyu hap ve şeritler (HUD, SONUÇ, Tuzak başlığı, Medeniyetimizden başlığı, koyu özet kartı) beyaz + siyah çerçeve; ebru yok; sahneler çok açık ton + koyu çizgi; molekül ve karakterler açık dolgu + koyu kontur | `unite-fotokopi.html` (kur.py --fotokopi): **kurulumda palet eşlemesi** (`yerel-ortak/fotokopi.py`: SVG dolgusu → mürekkebin %22'si, çizgi → koyu, SVG yazısı → siyah) + stil.css §34 tokenları. CSS `filter` kullanılmaz (PDF'te rasterleşir). render.js sayfa başına **ortalama mürekkep** yazar (`onizleme/fotokopi-murekkep.json`; hedef < %15) |
| `<klasör>-baski.pdf` | matbaa: kâğıt 9,21×12,64 inç, kesim 210×297 mm, **3,2 mm taşma**, kesim izleri taşmanın dışında, kenarda künye satırı; **TrimBox ve BleedBox** pypdf ile yazılır (`yerel-ortak/pdf_kutular.py`) | aynı `unite.html`, `<html class="baski">` (stil.css §35) + render.js DOM hazırlığı: kenara değen her şey taşma payına uzar — sayfa zemini, HUD, çini şeridi (sola bir karo), sahne bantları ve panorama (viewBox kenarında **ayna kopya**), altbilgi ebru şeridi, Hülasa ebru zemini. Kesim kutusunun içi öğrenci baskısıyla aynı (piksel karşılaştırmasıyla denetlendi) |
| `<klasör>-hazine-kartlari.pdf` | tek A4 kesme yaprağı: meta.json'daki bütün H kartları, sayfadaki `.hazine` bileşeniyle aynı (1,3×), her hücrede yol adı ve durak, kesik çizgiler ve makaslar (≤ 10 kart 2×5, ≤ 14 kart 2×7, daha çoksa 3 sütun) | `hazine-kartlari.html` (kur.py --hazine; `yerel-ortak/hazine_yapragi.py`); önizleme `onizleme/hazine-kartlari.png` |

| `<klasör>-<palet>.pdf` | palet denemesi (meta.json'a dokunmadan): `node render.js <ünite> --tema gol-rasathane` | `unite-<palet>.html` (`kur.py --tema <palet>`; render.js önce kendisi kurar); `--onizleme` ile `onizleme/varyant/<palet>/` |

**Palet ve nüshalar:** meta.json'da `palet` varsa öğrenci, öğretmen, baskı ve hazine yaprağı paletlidir; fotokopi her zaman
Van Gölü renklerinden griye eşlenir (paletsiz). `--tema` ayrıca bir deneme nüshası üretir.

Her PDF'te Type 3 font sayısı tablo hâlinde yazılır (`pdffonts`); hepsi **0** olmalı. Ara dosyalar (`unite-fotokopi.html`,
`hazine-kartlari.html`, `onizleme/varyant/`) her çalıştırmada yeniden üretilir; ünitenin `.gitignore`'unda durur.

**Fotokopiye uygun tasarım için:** koyu zemin üstüne açık yazıyı yalnız stil.css'teki bileşenlerle yap (hepsinin fotokopi kuralı var);
satır içi `style="background:#…"` ile yeni koyu kutu açma. Sahne çizerken renkleri `renkler.py`'den al; fotokopi eşlemesi rolüne
göre (dolgu/çizgi/yazı) otomatik çalışır.

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
  4. Tırnaksız `font-family="Baloo Bhaijaan 2"` geçersizdir ("2" bir CSS adı olamaz): yazı Nunito'ya düşer. Doğrusu
     `font-family="'Baloo Bhaijaan 2'"`. Bu yazıda Baloo'da olmayan karakter (✓ ★ Δ Σ α δ ↔) yedek sistem fontuna düşer ve
     **Type 3** olur: rozetteki ✓ ★ bu yüzden şekille çizilir. Baloo'da → ↓ ↑ ² ³ ° × √ − · var; Nunito'da → yok.
  Denetim: `pdffonts <klasor>.pdf | grep -c "Type 3"` → `0` olmalı.
- **Palet (tema.py) ve fiziksel renk:** spektrum çizgileri, alev renkleri, fotonlar, gözlük camları gibi gerçek rengi anlam taşıyan
  SVG grupları `<g data-tema-sabit="">` içine alınır (palet eşlemesi dokunmaz). Konu karakterleri (`kk-*`) ve insan karakterleri
  zaten sabittir; `<img>` (3B PNG) hiç eşlenmez. stil.css'te eşlenmemesi gereken bölge `/* tema-sabit */ … /* /tema-sabit */`
  arasına yazılır (öğretmen kırmızısı, fotokopi kuralları).
- Mol: 15 sayfa ≈ 8,4 MB (hedef ≤ 25 MB), bütün yazı tipleri CID TrueType olarak gömülü. `unite.html` ≈ 4 MB (satır içi SVG'ler).
  Varyantlar: öğretmen ≈ 8,4 MB, fotokopi ≈ 7,7 MB, baskı ≈ 9 MB, hazine kartları ≈ 0,25 MB.
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

---

## 16. Yeni bileşenler (yaygınlaştırma) · konu karakterleri, Hap Bilgi ailesi, paletler, katla, 3B

`gelistirme/` örneklerinden (atom-modelleri, karma-temalar, katla, uc-boyut) ortak kütüphaneye taşındı. **Kullanmayan ünitenin
çıktısı değişmez**: yeni sınıflar yeni adlarla başlar, semboller yalnız kullanılınca gömülür, `palet` ve `uc_boyut` alanları
yoksa hiçbir şey yapılmaz. Canlı örnek (her bileşen bir kez, 8 sayfa): `yerel-ortak/katalog/bilesenler/` →
`python3 uretec/kur.py --hepsi && python3 uretec/dogrula.py && node ../../render.js . --hepsi` (çıktılar git'e girmez).

### 16.1 Konu karakterleri (`cizim/konu_karakterleri.py`)
`{{kk|kimlik|sınıf}}` → `<svg class="konu-k sınıf" viewBox="…"><use href="#kimlik"/></svg>` (blok; boyu sayfanın kuralıyla).
SVG içinde: `KK.kullan("kk-foton-656", x, y, w)`. Kur sırasında sayfada geçen `href="#kk-…"` sembolleri (ve gradyanları)
gizli `<defs>`'e eklenir; hiç kullanılmıyorsa HTML değişmez. Renkler sabittir (palet dokunmaz). El ve gerçek kişi yüzü çizilmez.

| Grup | Kimlikler (viewBox) |
|---|---|
| modeller | `kk-atomos` `kk-dalton[-sasiran]` `kk-thomson[-endiseli]` `kk-rutherford` `kk-bohr` `kk-bulut` (120×120) · `kk-cekirdek[-sasiran]` (60×60) |
| tanecikler | `kk-proton` `kk-notron` `kk-elektron[-heyecan|-sasiran|-sakin|-sersem]` (60×60) · `kk-alfa[-mutlu|-sasiran|-sersem]` (72×66) · `kk-foton-656|-486|-434|-410|-uv` (92×50) |
| genel | `kk-su` (100×84) · `kk-iyon-arti` `kk-iyon-eksi` (64×64) · `kk-atom` (80×80) |
| gazlar | `kk-gaz-he|-h2|-o2|-n2|-co2|-so2|-ch4` + `-soguk` / `-sicak` ifadesi (renkler `renkler.ATOM`) |

### 16.2 Hap Bilgi ailesi ve kısa bileşenler (stil.css §37–§40, ikonlar `cizim/hap_bilgi.py`)
Her dikkat görselinin kendine özgü **biçimi** vardır (renksiz ve fotokopide de tanınır). Sayfa başına 3–4 tane yeter;
Tuzak! yanlış inancı, Dikkat! işlem/okuma hatasını yakalar.

| Bileşen | HTML |
|---|---|
| Hap Bilgi (kapsül) | `<div class="hb hb-hap"><span class="kap">{{hbi|hap}}Hap<br>bilgi</span><p>Tek bilgi<small>açıklama</small></p></div>` · kapak rengi `.gol .kob .mer` |
| Altın Kural (tezhipli) | `<div class="hb hb-kural">{{kose}}<span class="serit">{{hbi|yildiz}}ALTIN KURAL</span><p class="kural">… <em>…</em></p><p class="alt-not">…</p></div>` |
| Unutma! (yapışkan not) | `<div class="hb hb-unutma"><b class="bas">Unutma!</b><p>…</p></div>` |
| Sınav Radarı | `<div class="hb hb-radar"><span class="kurdele"><span>TYT</span></span>{{hbi|radar}}<div><b class="bas">Sınav radarı</b><p>…</p><span class="siklik">sık sorulur {{siklik|3|3}}</span></div></div>` |
| Dikkat! | `<div class="hb hb-dikkat">{{hbi|dikkat}}<div><b class="bas">Dikkat!</b><p>… <span class="cizgi-alti">…</span></p></div></div>` |
| Kilit Bilgi | `<div class="hb hb-kilit"><span class="madalyon">{{hbi|anahtar}}</span><div><b class="bas">Kilit bilgi</b><p>…</p></div>{{hbi|delik|anahtar-delik}}</div>` |
| Sohbet şeridi | `<div class="kart sohbet-serit"><b>#yol-<br>sohbeti</b>` + 3 × `.mesaj` (§5) `</div>` |
| Çizgi roman panosu | `<div class="kart roman-kart">` .kart-bas (+ `<span class="sag"><span class="anlatan">{{av|pamuk}}Pamuk anlatıyor</span>…</span>`) `<div class="roman">` 6 × `<div class="pano">{{info|pano_…}}<span class="pno">1</span><div class="anlatici"><b>…</b> …</div><div class="konus asagi|yukari|sola" style="left:…;top:…;--k:…%">…</div><span class="etiket" style="…">…</span></div>`; son pano `.pano.sonuc-pano` (`.anlatici` + `<ol><li><i>1</i><span>…</span></li></ol>`). Pano resimleri ünitenin `infografik_unite.py`'sinde `<svg class="resim">` döndürür |
| Bir bakışta (koyu özet) | `<div class="bakista"><span class="et">{{ikon|hulasa}}Bir bakışta</span><ol><li><i>1</i><span>…</span></li>…</ol></div>` |
| Kendini dene | `<div class="kart kendini-dene" data-soru="KD1">` .kart-bas + `<div class="soru-k"><i>1</i><div><b>Soru?</b><span class="yaz"><span class="ogr">cevap</span></span></div></div>` … + `<div class="ters-alan"><span class="ters">Cevaplar: …</span></div>` |
| Yanlış bilinen ↔ Doğrusu | `<div class="kart ikili-kart">` .kart-bas + `<div class="ikili"><div class="yan y"><span class="bas">{{hbi|carpi}}Yanlış bilinen</span><p>…</p>(svg.mini)</div><div class="ara">{{hbi|ciftok}}</div><div class="yan d"><span class="bas">{{hbi|tik}}Doğrusu</span><p>…</p></div></div>` |
| Tahmin et, sonra gözle | `<div class="kart tahmin-kart">` .kart-bas (+ `<span class="ust-not">…</span>`) + `<div class="tahmin"><div class="yan b"><span class="bas">Beklenen</span>(svg)<p>…</p></div><div class="yan g"><span class="bas">Gözlenen</span>…</div></div>` |

Yazıda ok: `{{ok}}` (Nunito'da → yok). Model Zinciri ve enerji merdiveni konuya özeldir: 9/03'ün kendi modülüne ve `<style>`'ına girer.

### 16.3 Sınıf paletleri (`yerel-ortak/tema.py`)
- **meta.json `"palet"`**: 9. sınıf `"cini-toprak"` (Çini ve Toprak: taban İznik Çini, vurgu Selçuklu Toprak, kutular pastel,
  sahneler "sıcak ikindi") · 10. sınıf `"gol-rasathane"` (Göl ve Rasathane: taban Van Gölü, vurgu Rasathane Gecesi, sahneler
  "alacakaranlık"). Alan yoksa çıktı hiç değişmez.
- Nasıl: ünite Van Gölü renkleriyle kurulur, `tema_html` sonra uygular: stil.css satır içi `<style data-tema>` olarak gömülüp
  eşlenir, SVG renkleri ve ünitenin `<style>` blokları eşlenir, ebru `yerel-ortak/gorsel/ebru-gol-<palet>.jpg` olarak bir kez
  boyanır, paletin "vurgu katmanı" (HUD, levha, bant çizgisi, `.bakista`, `.sonuc`, son pano) eklenir, `<html data-tema="…">`.
- Nüshalar: öğrenci, öğretmen, baskı, hazine yaprağı paletli; **fotokopi paletsiz** (griye Van Gölü renklerinden eşlenir).
- Deneme: `python3 uretec/kur.py --tema gol-rasathane` → `unite-gol-rasathane.html`; `node render.js <ünite> --tema gol-rasathane`
  → `<klasör>-gol-rasathane.pdf` (önce kendisi kurar; `--onizleme` ile `onizleme/varyant/<palet>/`). Kaynak temalar da denenebilir:
  `van-golu iznik-cini selcuklu-toprak rasathane-gecesi yumusak-pastel`.
  (Karıştırma: meta.json `tema` alanı ve `yeni_unite.py --tema` müfredat temasıdır, "Tema 1 · Bölüm 2"; renk paleti `palet` alanıdır.)
- **Sabit kalanlar:** fiziksel renk taşıyan SVG grupları `<g data-tema-sabit="">` (spektrum, alev, foton, gözlük camı, kap
  çözeltileri — ünite yazarı işaretler), karakterler (`pamuk- elif- yusuf- zeynep- av- kk- kr-`), `<img>` (3B PNG), mask/clipPath,
  stil.css'te `/* tema-sabit */ … /* /tema-sabit */` (öğretmen kırmızısı, fotokopi kuralları). Anlam renkleri ailede kalır:
  keh = akçe, mer = Tuzak/Dikkat, zumrut = doğru.
- Ünite yazarı renkleri tokenlardan alır (`renkler.py`, `var(--…)`); tokena yakın olmayan elle seçilmiş renk değişmez.

### 16.4 Katla (`cizim/katla.py`, stil.css §41)
**Sayfa sırası kuralı:** kat sayfası ve köşesi katlanan sayfa kitapta **TEK numaralı (sağ) sayfadır**; arka yüzleri hemen sonraki
ÇİFT sayfadır (kat sayfasının arkası: karma sayfa ya da köşe sineması; köşe sayfasının arkası: köşenin sırrı). Çift taraflı,
uzun kenardan çevirme. kur_ortak kitap numarasıyla (`YEREL_SAYFA_BASLANGIC`) denetler, kural bozulursa `UYARI:` yazar.
Arka yüze kat yerinden (70 ve 140 mm) geçen ince çizgi, tablo ya da resim konmaz; sütun aralıkları oraya denk gelir.

| Sayfa | Şablon |
|---|---|
| Kat sayfası (sağ) | `<section class="sayfa kat">{{zemin14}}{{hud|n|kat}}{{cini14}}{{katla|bag|film}}{{alt|n|kat}}</section>` · `{{katla|tepkime}}`. Satırlar `cizim/katla.py` `BAG` / `TEPKIME`; ünite kendi 4 satırını `sahneler_unite.KATLA_BAG` / `KATLA_TEPKIME` ile verir (aynı biçim; yeni tepkimede ürün kabı `urun_renk` ya da `urun_resmi`). Başlık satırı meta.json'dan ("Yol 6 · Tuz Gölü–Aksaray"). `film`: köşede sinema karesi. HUD yazısı sağ parçaya (142–199 mm) sığmalı |
| Karma sayfa (arka) | `{{hud|n}}` + `<div class="k-bas">{{rozet|…}}<div><h1>… <em>…</em></h1><p>…</p></div><span class="kat-not">{{kikon|katla}}…</span></div>` + `<div class="kol k1|k2|k3">` (11–67 · 73–137 · 143–199 mm) içinde kartlar |
| Köşe sineması (arka) | `{{film}}` (24 kare) + `<div class="film-alt">` 3 kart (`.enerji-tablo`) |
| Köşeyi katla ön (sağ) | `{{kose-on}}` + `{{alt|n|kose-on}}`; içerik `<div class="kose-ic" style="left:…;top:…;…">` kutularında, sağ alt 64 × 64 mm boş · `{{kose-adimlar|3 L}}` |
| Köşenin sırrı (arka) | `{{kose-arka|CEVAP|V_2 = 3 L|260 K → 300 K}}` (çip, büyük cevap, alt satır; ölçülü yazım `_2` `^{−}`) + `{{alt|n|kose-arka}}`; sol alt 64 × 64 mm boş · `{{kose-harita|3 L}}` |

Karma sayfa bileşenleri:
- **Şifreli Kapı:** `<div class="kart kapi-kart keh-z">` .kart-bas (`{{kikon|kapi}}`) + `<div class="kapi-ic">{{kapi}}<p>…</p></div>` +
  `<div class="sifre"><span><i>1</i><span class="ogr">P</span></span>…</div>`; soru kartları `<div class="kart sk" data-sk="1" data-soru="SK1">
  <div class="sk-bas"><span class="sk-no">1</span><span class="kaynak">Yol 3 · …</span></div><p class="soru">…</p><ol class="sk-sec [uc|bes]">
  <li data-dogru><b>P</b>…</li>…</ol></div>`. Seçenek etiketleri kod harfleridir; doğru harfler sırayla şifreyi yazar, yanlışlar kelime kurmamalı.
- **Çeldirici Röntgeni:** `<div class="kart rn" data-soru="CR1">` + `<div class="rn-sec"><div class="y"><b>A</b><span class="say">…</span><span class="tani">…</span></div>
  <div class="d" data-dogru>…</div>…</div>` + `<div class="isaret-acik"><span class="id">doğru</span><span class="iy">çeldirici</span></div>` (doğru düz yeşil, çeldirici kesik kırmızı).
- **Robot yanıldı mı?:** `<div class="kart robot-kart" data-soru="RB1">` + `<div class="robot-bas">{{robot}}<p>…</p></div><div class="bot-cevap"><ol><li>…</li>
  <li data-dogru>hatalı cümle</li>…</ol></div>` + `<p class="kurgu">KimyaBot kurgusal…</p>` (tek hata; kurgu notu zorunlu).
- **Heybe:** `<div class="kart heybe-kart">` + `<div class="heybe-sor"><span class="heybe-cip [y3|y5]">1 yol önce · Yol 5</span><p>…</p><div class="yaz-satir">Cevap:<span class="ogr">…</span></div></div>` + `<p class="ters-satir"><span class="ters">Cevaplar: …</span></p>`.
- **Nineme Anlat:** `<div class="kart nine-kart esnek">` + `<div class="yaz-satir">1.</div>…`. Yazı satırı her yerde `.yaz-satir`.

**Köşe sineması (her sağ sayfa):** `{{film-kose}}` doğrudan `<section>` içine; sayfa kitapta tek numaralıysa dış alt köşeye
(185–199 × 266,8–280,8 mm) kare `((s + 1) / 2 − 1) mod 24 + 1` basılır, sol sayfada boş döner. O köşe boş bırakılır (render.js
çakışmayı "köşe sineması karesi kutunun üstünde" diye bildirir). Belirli kare: `{{film-kare|k}}`. Köşesi katlanan sayfaya kare konmaz.

### 16.5 3B anaglif (`cizim/uc_boyut.py`, `cizim/gozluk.py`, stil.css §42)
- **meta.json `"uc_boyut"`**: hazır yapı adları (`ch4 nh3 h2o co2 bf3 nacl elmas grafit buz gaz kup hid-na hid-cl`) ya da
  `{"ad", "yapi", "donus", "en", "yuk", "mm_birim", "duz", "golge"}`; yeni yapı için ünitenin modülüne `Yapi` döndüren kurucu
  yazılır, adı `"yapi"`'ye. Kurulumdan önce ünitenin `gorsel/` klasörüne `ana-<ad>.png` (anaglif, 300 dpi), `duz-<ad>.png`
  (gözlüksüz küçük), `duz-<ad>-b.png` (fotokopi yedeği, gri, anaglif boyunda) ve `uc-boyut.json` yazılır. İmza (tanım +
  koordinatlar + motor kodu) değişmedikçe **yeniden çizilmez**; `--3b` zorlar. Resimler ünitenin malıdır (git'e girer).
- Sayfada: `{{ana|ad}}` (anaglif + gizli yedek), `{{duz|ad}}`, `{{ub-ikon|gozluk}}` (nötr gri ikonlar: `gozluk cetvel duz saat damla goz`),
  `{{test|yazi}}` `{{test|derinlik}}` (`yerel-ortak/gorsel/test-*.png`), **gözlük sayfası** `{{gozluk-sayfasi|n}}` (bütün sayfa;
  SAYFA'da n olmalı; kitap ekine sonra `yerel-cerceve` alacak). Yollar `YEREL_CIKTI`'ya göre kendiliğinden düzelir.
- Kart: `<div class="ub-serit">{{ub-ikon|gozluk}}<span><b>3B gözlükle bak:</b> …</span></div>` · `<div class="ub-izgara"><div class="kart ub">
  <div class="kart-bas"><span class="et">CH<sub>4</sub> · metan</span><span class="sekil-ad">…</span></div><div class="ub-govde">{{ana|ch4}}
  <div class="ub-yan">{{duz|ch4}}<span class="duz-et">gözlüksüz</span><span class="kutup apolar|polar">…</span><p>…</p></div></div></div></div>` ·
  kristal `.kart.ub.kr` (`.tur`, `.sayi`, `.sayi-et`, `.ub-not` + `.veri`) · geniş `.kart.ub.genis` · `.duz-satir` · `.cift-ana > figure + figcaption` · `.kf`
  (büyük harfli etikette formül: NaCl ≠ NACL).
- Kurallar: anaglifin çevresi beyaz, yanında kırmızı/camgöbeği süs yok; renk yalnız gözlük sayfasında (`data-tema-sabit`).
  Baskı ve gözlük önerileri: `gelistirme/uc-boyut/README.md` §6; fiziksel deneme baskısı yapılmadı.

### 16.6 Varyant kuralları (öğretmen · fotokopi · palet)
| Bileşen | Öğretmen nüshası | Fotokopi |
|---|---|---|
| Kendini dene | `.yaz > .ogr` cevap satıra kırmızı | numara kutusu beyaz + siyah çizgi |
| Şifreli Kapı | `li[data-dogru]` kırmızı harf; `.sifre > span > .ogr` kutuda harf | `.sk-no` beyaz halka |
| Çeldirici Röntgeni | `div[data-dogru]` kırmızı halka; `.yaz-satir > .ogr` | doğru düz, çeldirici kesik çerçeve (renksiz ayrılır) |
| Robot yanıldı mı? | hatalı cümle `li[data-dogru]` kırmızı dalgalı alt çizgi; `.yaz-satir > .ogr` | konuşma balonu beyaz |
| Heybe · Nineme | `.yaz-satir > .ogr` | `.heybe-cip` beyaz + siyah çizgi |
| Kat sayfası | `g.ogr-svg` (ürün, tür, neden; kendiliğinden) | SVG gri (fotokopi.py); kat şeridi üst çizgili |
| Köşeyi katla | `.bosluk > .ogr`, `.karalama > .ogr` | köşe SVG gri |
| Hap Bilgi ailesi | — | kapsül kapağı, Altın Kural kurdelesi, radar kurdelesi açık gri; madalyon açık gri; yapışkan not beyaz + gri çizgi |
| Bir bakışta · son pano | — | beyaz + siyah çerçeve, yazı siyah |
| Yanlış ↔ Doğrusu | — | yanlış kesik, doğru düz çerçeve (outline: yerleşim değişmez) |
| 3B | — | `img.ana` gizli, yerine aynı kutuda gri `img.duz.yedek`; küçük düz resim ve "gözlüksüz" gizli; `.kutup.polar` gri |

Öğretmen metni yerleşimi bozmaz (mutlak ya da satır içi); `render.js --ogretmen` taşanı bildirir. Dogrulama yardımcıları
(`dogrula_ortak`): `kendini_dene_ayni(html, {"KD1": ["apolar", "olmazdı"]})`, `sifreli_kapi_ayni(html, "PROTON")`,
`celdirici_ayni(html, {"CR1": ("B", "13, 14, 10")})`, `robot_ayni(html, {"RB1": 3})`, `katla_ayni(html, {"B1": ("NaCl", "iyonik")})`,
`uc_boyut_resimleri(html, html_yolu)` → `[]`; okuyucuları `kendini_dene`, `sifreli_kapi`, `celdirici_rontgeni`, `robot_hatalari`, `katla_cevaplari`.

### 16.7 Yeni yer tutucular (tam liste)
| Yer tutucu | Üretir |
|---|---|
| `{{kk|kimlik|sınıf}}` | konu karakteri `svg.konu-k` (16.1) |
| `{{hbi|ad|sınıf}}` | Hap Bilgi ikonu (`hap yildiz radar dikkat anahtar delik carpi tik ciftok`; sınıf yoksa `hbi`, `{{hbi|ad|}}` sınıfsız) |
| `{{ok}}` · `{{siklik|dolu|toplam}}` | metin içi SVG ok · radar sıklık noktaları |
| `{{hud|n|kat}}` · `{{alt|n|kat}}` | kat sayfası şeridi (logo solda, yer sağ parçada) · düz alt şerit (dikişte kopmaz) |
| `{{alt|n|kose-on}}` · `{{alt|n|kose-arka}}` | köşe boş kalan altbilgi (ön: sağ alt · arka: sol alt) |
| `{{zemin14}}` · `{{cini14}}` | kat sayfasının 14 mm adımlı zemini · 7 mm karolu çini şeridi |
| `{{katla|bag}}` · `{{katla|tepkime}}` · `…|film}}` | tam sayfa kat SVG'si (+ köşe sineması karesi) |
| `{{kikon|ad}}` · `{{robot}}` · `{{kapi}}` | karma sayfa ikonları (`kapi rontgen robot heybe nine film kose katla`) · KimyaBot · kemerli kapı |
| `{{film}}` · `{{film-kose}}` · `{{film-kose|n}}` · `{{film-kare|k}}` | 24 karelik ızgara · sağ sayfa köşe karesi (kendiliğinden) · belirli kare |
| `{{kose-on}}` · `{{kose-arka|baş|cevap|alt}}` · `{{kose-adimlar|c}}` · `{{kose-harita|c}}` | köşeyi katla |
| `{{ana|ad}}` · `{{duz|ad}}` · `{{test|yazi|derinlik}}` · `{{ub-ikon|ad}}` · `{{gozluk-sayfasi|n}}` | 3B (16.5) |
| `{{sahne|bant_atolye}}` · `{{info|nasil_calisir}}` · `{{info|gozluk_sablonu}}` · `{{info|ub_ikon|ad}}` | gözlük sayfasının parçaları (tek tek kullanım) |

### 16.8 Yeni CSS sınıfları (stil.css §37–§44)
§37 `.hb` `.hb-hap` (`.kap`, `.gol .kob .mer`) `.hb-kural` (`.serit .kural .alt-not`) `.hb-unutma` (`b.bas`) `.hb-radar` (`.kurdele .bas .siklik`)
`.hb-dikkat` (`.bas .cizgi-alti`) `.hb-kilit` (`.madalyon .bas .anahtar-delik`) · §38 `.sohbet-serit` · §39 `.roman-kart` (`.anlatan`) `.roman`
`.pano` (`.pno .anlatici .konus.asagi|yukari|sola|bagir .etiket svg.resim`) `.pano.sonuc-pano` · §40 `svg.konu-k` `.bakista` `.kendini-dene`
(`.soru-k .yaz .ters-alan`) `.ikili-kart` `.ikili` (`.yan.y .yan.d .bas .ara svg.mini`) `.tahmin-kart` `.tahmin` (`.yan.b .yan.g`) `.ust-not` ·
§41 `svg.katla-svg` `.kat-hud` `.hud.kat-serit` `.alt.kat-alt` `.k-bas` `.kat-not` `.kol.k1|k2|k3` `.kapi-kart` `.kapi-ic` `.sifre` `.sk` `.sk-bas`
`.sk-no` `.kaynak` `.sk-sec.uc|bes` `.rn` `.rn-sec` (`.y .d .say .tani`) `.isaret-acik` (`.id .iy`) `.robot-kart` `.robot-bas` `.bot-cevap` `.kurgu`
`.yaz-satir` `.heybe-kart` `.heybe-sor` `.heybe-cip.y3|y5` `.ters-satir` `.nine-kart` `svg.film-svg` `.film-alt` `.enerji-tablo` `svg.film-kose`
`svg.kose-svg.on|arka` `.ebru-alt.kose-on|kose-arka` `.alt.kose-on-alt|kose-arka-alt` `.kose-ic` `svg.kose-adimlar` `svg.kose-harita` ·
§42 `.ub-serit` `.ub-izgara` `.kart.ub` (`.kr .genis`) `.sekil-ad` `.ub-govde` `img.ana` `img.duz(.yedek)` `.ub-yan` `.duz-et` `.kutup.polar|apolar`
`.ub-not` `.veri` `.duz-satir` `.cift-ana` `.kf` `section.gozluk-sayfa` (`.nasil .sablon-bas .sablon-alan ul.ipucu .test-kart .kucuk-p`) ·
§43 öğretmen (`.ogr-svg` + yukarıdaki işaretler) · §44 fotokopi. Taşma denetimi (render.js) `.hb .bakista .ikili .yan .tahmin .yan .rn-sec > div
.bot-cevap .kol .kose-ic .film-alt > .kart .ub-serit` kutularını da ölçer.
