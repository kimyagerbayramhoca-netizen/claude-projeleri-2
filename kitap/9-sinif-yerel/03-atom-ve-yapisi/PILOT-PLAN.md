# 9/03 Atom ve Yapısı · Pilot planı (yeni düzen)

Durum: **uygulandı** (koordinatörün "uygula" mesajıyla). Ortak kütüphanenin gerçek yer tutucuları kullanıldı
(`yerel-ortak/TASARIM-SISTEMI.md` §16). Kur, dogrula (324 denetim, hepsi doğru), taşma (yok) ve beş nüsha (Type 3 = 0) geçti.
Plandan sapmalar ve uygulamadaki karşılıkları §0.1'de; ünitenin güncel sayfa planı ve cevap anahtarı `README.md`'de.
L = sol (çift) sayfa, R = sağ (tek) sayfa. Ünite kitapta tek numaralı sayfada başlar; ünite içi tek numara = sağ sayfa.

### 0.1 Uygulamada değişenler

- **Kat sayfası türü ünitede:** ortakta yalnız `{{katla|bag}}` ve `{{katla|tepkime}}` var. "Katla, doğrusu kalsın!" ünitenin
  `uretec/katla_unite.py` modülüne yazıldı (ortak `cizim/katla.py` parçalarıyla) ve `kur.py`'de `{{katla-cumle}}` yer tutucusu
  oldu. Satırlar `katla_unite.KATLA_CUMLE`. Öğretmen cevabı ortak `_ogr_grubu` ile; `katla_ayni` aynen okur.
- **Yeni modüller:** `model_ciz.py` (atom-modelleri çizimleri + Halfeti teknesi + dış katman), `uc_unite.py` (3B kurucuları;
  lob küre zinciriyle, motorda elipsoit gerekmedi), `katla_unite.py`. `infografik_unite.py` hepsini kendi ad alanına alır.
- **s.4–5:** çizgi roman ile sohbet+kavram s.4'e sığmadı. s.4'te sohbet şeridi + çizgi roman + Görev 2; Kavram (+30) s.5'e geçti.
  Akçe sayfa dağılımı: s.4 30, s.5 90 (durak toplamı yine 120); HUD çubuğu s.5 = 8.
- **Hap Bilgi yerleri** sığdırma için birkaç kez kaydı (durak başına en az 3, sayfa başına en çok 4 korunuyor; dogrula denetler).
- **Akçe rayı:** ortaktaki ray 0–1400 sabit; ünite `infografik_unite.akce_rayi`'yi 1600 ölçeğiyle tanımladı (önce ünite modülünde aranır).
- **Köşe cevapları:** yer tutucu içinde `{…}` olamadığı için ölçülü yazım tek karakterli (`8 e^−`, `3s^2`).
- **Font:** ünitenin kendi SVG yazıları da tırnaklı `'Baloo Bhaijaan 2'`; `kur.py`'deki `_rozet_duzelt` kaldırıldı.
- Büyük harfli etiketlerde formüller `.kf` ile korundu; öğretmen nüshasında taşan üç kırmızı cevap kısaltıldı.

## 0. Özet

- **16 → 26 sayfa (+10).** Her durak iki sayfalık bir açılım olur (L + R). Araya 3B açılımı (2 sayfa), Hülasa'nın arkasına
  kat yaprağı (kat sayfası + arka yüzü karma sayfa) girer. 26 çift; sonraki ünite yine tek sayfada başlar, "Notlar" gerekmez.
- **Katla:** 1 kat sayfası ("Katla, doğrusu kalsın!", 4 cümle) + **7 köşeyi katla** (6 durak + 3B'nin 2. sayfası).
- **3B:** 2 sayfa, 8 anaglif (s ve p orbitalleri; altın levhada alfa tanecikleri, alfa taneciği, atomun boşluğu).
- **Hap Bilgi ailesi:** 28 kutu; durak açılımı başına 4, 3B sayfası başına 3; sayfa başına en çok 4, aynı türden en çok 2.
  Metinleri mevcut Kavram, Tuzak, Hızlı görev, H kartı, Hülasa ve Yoldan cümlelerinden dönüştürüldü (kaynak her kutuda yazılı).
- **Her durakta:** 1 Bir bakışta, 1 Kendini dene (+10 akçe), 1 köşeyi katla (eski Hızlı görev).
- **Konu karakterleri:** Model Zinciri (1. durak), Rutherford çizgi romanı (2. durak, tek çizgi roman şeridi), enerji merdiveni
  (3. durak), Tanecik tanıtımı (4.), Halfeti teknesi (5.), Dış katman konuşuyor (6.), kat sayfası satırları.
- **Karma sayfa:** Şifreli Kapı (PROTON), Çeldirici Röntgeni (¹⁹₉F⁻), Robot yanıldı mı? (hidrojen spektrumu), Heybe (4 soru).
- **Palet:** meta.json `"palet": "cini-toprak"`.
- **Korunanlar:** 6 durak, Görev 1–6, H1–H12, 8 nişan, Medeniyetimizden (3), Hülasa, Meclis, Kıssa, Anahtar, Büyük İmtihan,
  Üstad, Cevaplar, Final; bütün soru, şık ve cevaplar aynen. Değişen yalnız yerleşim, sayfa numaraları ve akçe toplamı.
- **Yerini yenisine bırakan üç çizim** (içerik aynı, daha zengin biçim): `model_yolculugu` → Model Zinciri,
  `altin_levha` → çizgi roman, `spektrum` → enerji merdiveni. Veri tabloları (`CIZGI`, `LAMBA`, `ENERJI_EV`, `GECIS`,
  `KISSA_TANECIK`) `infografik_unite.py`'de kalır; dogrula onları kullanıyor.
- **Akçe (öneri):** toplam **1600**: kat sayfası 40 + karma 160 yeni standart; 3B sayfaları bonus (akçesiz). Ayrıntı §1.4, karar §10.

## 1. Bu ünitedeki ortak kurallar

### 1.1 Parite ve katlama çiftleri

| Ön yüz (R) | Ne | Arka yüz (L) | Arka yüzde ne olur |
|---|---|---|---|
| s.3 | 1. durak köşesi | s.4 | sol alt 64 × 64 mm: köşe cevabı (90° dönük) |
| s.5 | 2. durak köşesi | s.6 | aynı |
| s.7 | 3. durak köşesi | s.8 | aynı (3B-1 sayfası) |
| s.9 | 3B köşesi (bonus) | s.10 | aynı |
| s.11 | 4. durak köşesi | s.12 | aynı |
| s.13 | 5. durak köşesi | s.14 | aynı |
| s.15 | 6. durak köşesi | s.16 | aynı (Hülasa) |
| s.17 | kat sayfası | s.18 | karma sayfa: 3 sütun 11–67 · 73–137 · 143–199 mm, kat izleri sütun aralığında |

s.1, 19, 21, 23, 25'te köşe yok; s.2, 18, 20, 22, 24, 26'nın sol alt köşesi serbest.

### 1.2 Sayfa iskeletleri

**Durağın sol sayfası** (s.2, 4, 6, 10, 12, 14): bant + levha (mevcut, değişmez) → sohbet + Kavram (mevcut) → büyük çizim →
alt bant. Köşe cevabı taşıyan sol sayfalarda (s.2 hariç hepsi) akış 228 mm'de biter, alt bant sağda mutlak kutudur:

```html
<section class="sayfa s4">
  {{zemin}} {{hud|4}} {{cini}}
  <div class="bant b40" data-serbest>{{sahne|harran}} <div class="levha">…mevcut levha…</div></div>
  <main class="ic" style="top:54.5mm; bottom:69mm"> …satırlar… </main>
  <div class="kose-ic" style="left:70mm; right:11mm; top:230mm; bottom:15.6mm"> …Görev kartı… </div>
  {{kose-arka|CEVAP|2|elektron, (+) yük}}
  {{alt|4|kose-arka}}
</section>
```

**Durağın sağ sayfası** (s.3, 5, 7, 11, 13, 15): bant yok; devam başlığı → A satırı (konu parçası + H kartları) → B satırı
(Hap Bilgi şeridi) → C satırı (Tuzak / Medeniyet / Yoldan) → D satırı (Kendini dene + Bir bakışta) → alt bantta köşe kartı:

```html
<section class="sayfa s3 kose-s">
  {{zemin}} {{hud|3}} {{cini}}
  <main class="ic" style="top:22mm; bottom:69mm">
    <div class="devam-bas">{{rozet|1}}<div><span class="ust">1. durak · Göbeklitepe · devam</span><h2>Fikirlerin <em>yolculuğu</em></h2></div></div>
    …A, B, C, D satırları…
  </main>
  <div class="kose-ic" style="left:11mm; width:129mm; top:230mm; bottom:15.6mm"> …köşe kartı… </div>
  {{kose-on}}
  {{alt|3|kose-on}}
</section>
```

Köşe kartı (eski Hızlı görev; anahtar ve öğretmen cevabı kalır, ters cevabın yerine köşe):

```html
<div class="kart hizli kose-kart">
  <div class="kart-bas"><span class="et keh">{{kikon|kose}}Hızlı görev · köşeyi katla</span><span class="cip akce">+20 akçe</span></div>
  <p class="soru">…</p>
  <div class="anahtar-ipucu">{{ikon|anahtar}}<span>Anahtar <b>(−10)</b>: <span class="ters">…</span></span></div>
  <div class="cevap-satir"><div class="cevap-kutu">CEVABIN:<span class="ogr">2</span></div><em>Kontrol: sağ alt köşeyi katla {{ok}}</em></div>
</div>
```

Sınıf sırası her zaman `sayfa sNN ek-sınıf` (dogrula'daki `bolum()` buna göre arar): `sayfa s17 kat`, `sayfa s3 kose-s`.

### 1.3 Hap Bilgi kuralı
Sayfa başına en çok 4 dikkat görseli, aynı türden en çok 2. Tuzak! yanlış inancı mühürler, Dikkat! işlem ya da okuma hatasını
önler. 6 Tuzak kutusundan 4'ü "Tuzak!" başlıklı **Yanlış bilinen ↔ Doğrusu** kartına (`.ikili-kart`, YANLIŞ mühürlü), 2'si
(3. ve 5. durak) **Dikkat!**'e dönüşür. Yazıda ok için `{{ok}}`; kalın yazıda ve SVG'de α yerine "alfa".

### 1.4 Akçe (öneri: 1600)
Durak çipleri: Kavram görevi, Görev, Kendini dene **+10** (Tuzak'ın +10'u buraya geçer), köşe (eski Hızlı görevin değeri),
2 hazine kartı +20. Tuzak ve Hap Bilgi kutuları akçe taşımaz. Durak toplamları değişmez: 100 + 5 × 120.

| Bölüm | Akçe | Sayfa |
|---|---|---|
| Duraklar | 700 | 2–7, 10–15 |
| Hülasa · muhasebe | 40 | 16 |
| **Katla · doğrusu kalsın** (4 tahmin × 10) | **40** | 17 |
| **Karma sayfa** (Kapı 60 · Röntgen 30 · Robot 30 · Heybe 40) | **160** | 18 |
| Meclis · Kıssa · Anahtar | 3 × 120 | 19–21 |
| Büyük İmtihan | 300 | 22–23 |
| 3B (2 sayfa) ve Üstad | bonus, akçesiz | 8–9, 24 |
| **Toplam** | **1600** | Ahilik eşikleri: Kalfa 450 · Usta 900 · Atom Üstadı 1300 |

Sayfa başına çip: s.2 50 · s.3 50 · s.4–7 60'ar · s.10–15 60'ar · s.16 40 · s.17 40 · s.18 160 · s.19–21 120'şer · s.22–23 150'şer.
Eşikler eski oranlara yakın (%28,1 · %56,3 · %81,3; eskisi %28,6 · %57,1 · %82,1).

## 2. Sayfa sayfa plan

| s. | Yön | Sayfa | Bileşenler | Akçe |
|---|---|---|---|---|
| 1 | R | Yola çıkış | mevcut + yeni çipler, 8 işaret, eşikler (§6) | – |
| 2 | L | 1. durak · Göbeklitepe | bant, sohbet + Kavram, **Model Zinciri**, Görev 1 | 50 |
| 3 | R | 1. durak · devam | Tuzak! ikili + H1–H2 · Hap Bilgi ×4 · İbn Heysem · Kendini dene + Bir bakışta · **köşe** | 50 |
| 4 | L | 2. durak · Harran | bant, sohbet + Kavram, **çizgi roman** (6 pano), Görev 2 · köşe cevabı 1 | 60 |
| 5 | R | 2. durak · devam | Kümbet ve Bohr + H3–H4 · Hap Bilgi ×4 · Tuzak! ikili + Sâbit bin Kurra · KD + BB · **köşe** | 60 |
| 6 | L | 3. durak · Harran Höyüğü | bant, sohbet + Kavram, **enerji merdiveni**, Hap bilgi, Görev 3 · köşe cevabı 2 | 60 |
| 7 | R | 3. durak · devam | orbital biçimleri + H5–H6 · Hap Bilgi ×3 · el-Battânî · KD + BB · **köşe** (lamba) | 60 |
| 8 | L | 3B · Orbitaller | 5 anaglif kartı, Hap Bilgi ×3, Kendini dene (bonus) · köşe cevabı 3 | – |
| 9 | R | 3B · Alfa tanecikleri | 3 anaglif kartı, Hap Bilgi ×3 · **köşe** (bonus) | – |
| 10 | L | 4. durak · Urfa çarşısı | bant, sohbet + Kavram, iyon + izo çizimleri, Sınav Radarı, Görev 4 · köşe cevabı 3B | 60 |
| 11 | R | 4. durak · devam | **Tanecik tanıtımı** + H7–H8 · Hap Bilgi ×3 · Tuzak! ikili + Yoldan · KD + BB · **köşe** | 60 |
| 12 | L | 5. durak · Halfeti | bant, sohbet + Kavram, **Halfeti teknesi**, aufbau, Görev 5, Soy gaz · köşe cevabı 4 | 60 |
| 13 | R | 5. durak · devam | H9–H10 + Yoldan · Hap Bilgi ×4 · KD + BB · **köşe** | 60 |
| 14 | L | 6. durak · Fırat kıyısı | bant, sohbet + Kavram, tablo + istisnalar, Sınav Radarı, Yoldan, Görev 6 · köşe cevabı 5 | 60 |
| 15 | R | 6. durak · devam | **Dış katman konuşuyor** + H11–H12 · Hap Bilgi ×3 · Tuzak! ikili · KD + BB · **köşe** | 60 |
| 16 | L | Hülasa · Gümrük Hanı | mevcut; alt satır yeniden dizilir · köşe cevabı 6 | 40 |
| 17 | R | **Kat sayfası** | Katla, doğrusu kalsın! (4 cümle) | 40 |
| 18 | L | **Karma sayfa** | Şifreli Kapı, Çeldirici Röntgeni, Robot yanıldı mı?, Heybe | 160 |
| 19 | R | Meclis · Sıra gecesi | mevcut (gönderme s.25) | 120 |
| 20 | L | Kıssa · Harran Ovası | mevcut | 120 |
| 21 | R | Anahtar · Urfa evleri | mevcut | 120 |
| 22 | L | Büyük İmtihan 1/2 | mevcut | 150 |
| 23 | R | Büyük İmtihan 2/2 | mevcut | 150 |
| 24 | L | Üstad | mevcut | – |
| 25 | R | Cevaplar | mevcut + 1 satır yeni sayfalar, tekrar rotası sayfaları | – |
| 26 | L | Final | mevcut; defter 2 satır, toplam 1600, unvanlar, ray | – |

KD = Kendini dene, BB = Bir bakışta. Durak sayfalarında sığmayan olursa çıkarma sırası: Sınav Radarı → Bir bakışta 3. madde
→ devam başlığının çipi. Mevcut içerik kısaltılmaz.

## 3. Duraklar

### 3.1 · 1. durak · Göbeklitepe (s.2 L · s.3 R)

**s.2 (L)**, bant `gobeklitepe`, levha aynen.
1. Sohbet + Kavram (+20), aynen (mevcut s.2).
2. **Model Zinciri** (`model_yolculugu` kartının yerine): `gelistirme/atom-modelleri/uretec/sablon.html` satır 40–59 **aynen**,
   yalnız `+40 akçe` çipi çıkar. Altı model karakteri (`kk-atomos kk-dalton kk-thomson kk-rutherford kk-bohr kk-bulut`), plakalar:
   Demokritos MÖ y. 400 · Dalton 1803–1808 · Thomson 1897 · 1904 · Rutherford 1911 · Bohr 1913 · Modern model 1920'ler.
   Çizim `zincir_yolu`, CSS gelistirme.css §C (satır 93–118) ünitenin `<style>`'ına.
3. Görev 1 (+30), aynen. s.2'nin sol alt köşesi serbest (s.1'de köşe yok), sayfa olağan akışla 281 mm'ye kadar.

**s.3 (R)**, devam başlığı: "1. durak · Göbeklitepe · devam" · *Fikirlerin yolculuğu*.
- **A:** Tuzak! ikili + H1, H2 (+20, mevcut kartlar):
  - Yanlış bilinen: "Eski model tamamen yanlıştı." `{{muhur|yanlis}}` · mini `{{kk|kk-dalton-sasiran|mini}}`
  - Doğrusu: "Dalton’un “atomlar korunur” fikri bugün de doğru." · mini `{{kk|kk-dalton|mini}}` (mevcut Tuzak metni aynen)
- **B · Hap Bilgi ×4:**
  - Hap bilgi (`.gol`): "Teori deneye dayanır; model teoriyi anlatır." (kaynak: s.2 Kavram)
  - Hap bilgi (`.kob`): "Yeni deney {{ok}} yeni model" (kaynak: s.2 Kavram görevi)
  - Unutma!: "Dalton ve Thomson modellerinde çekirdek yok. Çekirdek, altın levha deneyiyle geldi (Rutherford, 1911)." (kaynak: s.2 Hızlı görev)
  - Sınav Radarı (TYT): "Modellerin sırası ve her modelin açıklayamadığı gözlem sık sorulur." `{{siklik|3|3}}` (kaynak: Görev 1)
- **C:** Medeniyetimizden · İbn Heysem, mevcut metin aynen.
- **D:** Kendini dene (`data-soru="KD1"`, +10) + Bir bakışta.
  - KD1-1: "Thomson modelinde atomun (+) yükü nerededir?" → *Her yere dağılmış (kekin hamuru).*
  - KD1-2: "Model zincirinde Bohr’dan sonra hangi model gelir?" → *Modern model (orbital).*
  - Ters: "Cevaplar: 1 her yere dağılmış · 2 modern model"
  - Bir bakışta: (1) Model deneyle sınanır; açıklayamadığı bir deney çıkınca **değişir**. (2) **Çekirdek** Rutherford’la (1911),
    **katmanlar** Bohr’la (1913) geldi. (3) Bugün elektronun yolu değil, **bulunma olasılığı** (orbital) konuşulur.
- **Köşe (+20):** "Elektron, çekirdek, (+) yük, katman: kaçı Thomson modelinde var?" · Anahtar: *Üzümlü kek: hamur ve üzüm.* ·
  `.ogr` 2 · arka (s.4): `{{kose-arka|CEVAP|2|elektron, (+) yük}}`

### 3.2 · 2. durak · Harran (s.4 L · s.5 R)

**s.4 (L)**, bant `harran` (b40), levha aynen.
1. Sohbet + Kavram (+30), aynen.
2. **Çizgi roman** (`altin_levha` + `bohr_kumbet` kartının yerine; `bohr_kumbet` s.5'e geçer): atom-modelleri sablon satır 105–143
   **aynen**; değişen iki şey: başlık "Çizgi roman · altın levha deneyi 1909–1911: Geiger ve Marsden’in deneyi, Rutherford’un yorumu"
   (dogrula'daki "1909–1911" denetimi için), `+40 akçe` çipi çıkar. Pamuk anlatıyor; altı pano: düzenek → çoğu geçer → bazıları
   sapar → çok azı geri döner ("Kâğıda top mermisi atmışsınız da geri dönmüş gibiydi.") → nohut–stadyum → deneyden sonuca.
   Pano çizimleri (`pano_duzenek … pano_sonuc`) ünitenin `infografik_unite.py`'sine.
3. Alt bant (70–199 mm): Görev 2 (+30), aynen. Sol alt: 1. durağın köşe cevabı.

**s.5 (R)**, devam: "2. durak · Harran · devam" · *Çekirdek ve katmanlar*.
- **A:** Kümbet ve Bohr katmanları (`bohr_kumbet`, mevcut) + H3, H4 (+20).
- **B · Hap Bilgi ×4:**
  - Altın Kural: "Çoğu geçer {{ok}} atom çoğunlukla *boşluk*. Çok azı döner {{ok}} küçük, yoğun, (+) *çekirdek*." · alt not:
    "Deneyin bütün yorumu bu iki cümlede." (kaynak: Görev 2 sonucu)
  - Dikkat!: "α’yı geri çeviren *elektronlar değil, (+) çekirdektir*. Elektron, α’dan yaklaşık 7300 kat hafiftir; onu durduramaz."
    (kaynak: Görev 2 + tanecik tablosu; kütle oranı 7294)
  - Hap bilgi (`.kob`): "α = He çekirdeği" · küçük: "2 proton + 2 nötron · yükü +2"
  - Sınav Radarı (TYT): "Altın levhanın üç gözlemi ve her birinin sonucu sık sorulur."
- **C:** Tuzak! ikili (atom-modelleri satır 71–79 biçimi) + Medeniyetimizden · Sâbit bin Kurra (aynen):
  - Yanlış bilinen: "Elektron dairesel yolda döner." · `{{info|mini_yorunge}}`
  - Doğrusu: "Bu Bohr’un fikriydi; bugün yol çizilmez, orbital denir." · `{{info|mini_bulut}}`
- **D:** Kendini dene (KD2, +10) + Bir bakışta.
  - KD2-1: "Taneciklerin çoğunun sapmadan geçmesi atom hakkında ne söyler?" → *Atomun büyük kısmı boşluk.*
  - KD2-2: "Geri dönen alfalar hangi yükteki bir merkezden itilmiştir?" → *(+) yüklü çekirdek.*
  - Bir bakışta: (1) Altın levha: çoğu geçti (**boşluk**), çok azı döndü (küçük, yoğun, (+) **çekirdek**). (2) Bohr: elektronlar
    belirli enerjili **katmanlarda**; bir katmanda en çok 2n² e⁻. (3) Modern model: yol çizilmez; bulunma olasılığı yüksek bölge **orbitaldir**.
- **Köşe (+30):** "L katmanı (n = 2) en çok kaç e⁻ alır?" · Anahtar: *2n² kuralında n = 2 al.* · `.ogr` 8 ·
  arka (s.6): `{{kose-arka|CEVAP|8 e^{−}|2 · 2^{2} = 8}}`

### 3.3 · 3. durak · Harran Höyüğü (s.6 L · s.7 R)

**s.6 (L)**, bant `harran_hoyuk` (b40), levha aynen.
1. Sohbet + Kavram (+30), aynen.
2. **Enerji merdiveni** (`spektrum` kartının yerine): atom-modelleri satır 192–200 **aynen** (adım şeridi: 12,09 eV soğurur · 1,89 eV
   kırmızı 656 nm · 10,20 eV UV · 1,89 + 10,20 = 12,09), `+40 akçe` çipi çıkar. Fotonlar `kk-foton-*`, elektron `kk-elektron-*`.
   Çizim `enerji_merdiveni`; foton ve çizgi grupları `data-tema-sabit`. CSS gelistirme.css §E (satır 149–158) `<style>`'a.
3. Hap bilgi (`.gol`): "H çizgileri" · küçük: "410 · 434 · 486 · 656 nm" (kaynak: s.4 sohbet + çizim; Rydberg ile denetli).
4. Alt bant: Görev 3 (+30), aynen. Sol alt: 2. durağın köşe cevabı.

**s.7 (R)**, devam: "3. durak · Harran Höyüğü · devam" · *Işık ve orbitaller*.
- **A:** Orbitallerin biçimi (`orbital_sekilleri`, mevcut) + H5, H6 (+20).
- **B · Hap Bilgi ×3:**
  - Kilit bilgi: "Fotonun enerjisi = iki düzeyin **enerji farkı**. Çıkarken soğurur, inerken yayar; fark büyüdükçe dalga boyu kısalır." (kaynak: s.4 Kavram)
  - Dikkat! (eski Tuzak): "Elektron üst düzeye *çıkarken ışık yaymaz, soğurur*; ışık inerken yayılır." (kaynak: s.4 Tuzak)
  - Sınav Radarı (TYT): "“Işık yayar” görürsen elektron iniyor; “soğurur” görürsen çıkıyor." (kaynak: H5)
- **C:** Medeniyetimizden · el-Battânî (aynen) + küçük not: "Sayfayı çevir: orbitaller 3B'de!"
- **D:** Kendini dene (KD3, +10) + Bir bakışta.
  - KD3-1: "Elektron n = 4’ten n = 2’ye inerse ışık soğurur mu, yayar mı?" → *Yayar (486 nm).*
  - KD3-2: "Hangi inişin dalga boyu daha kısa: 6’dan 2’ye mi, 3’ten 2’ye mi?" → *6’dan 2’ye (410 nm).*
  - Bir bakışta: (1) Elektron belirli düzeylerde bulunur; çıkarken **soğurur**, inerken **yayar**. (2) H’nin görünür dört çizgisi
    **n = 2’ye inişlerden** gelir. (3) Orbital türleri: s 1 · p 3 · d 5 · f 7 orbital; her orbitalde en çok **2 e⁻**.
- **Köşe (+30):** "Lambanın çizgilerini eşleştir: hangi elementler var?" + `{{info|lamba_spektrumu}}` (mevcut) · `.ogr` H ve Na ·
  arka (s.8): `{{kose-arka|CEVAP|H ve Na|Na çizgisi 589 nm}}`

### 3.4 · 4. durak · Urfa çarşısı (s.10 L · s.11 R)

**s.10 (L)**, bant `urfa_carsi`, levha aynen.
1. Sohbet + Kavram (+30; tablo ve izo eşleştir görevi), aynen.
2. İyon olur, kimlik kalır + "İzo" kardeşler (mevcut iki çizim).
3. Sınav Radarı (TYT): "İzotop, izoton, izobar ve izoelektronik ayrımı sık sorulur." (kaynak: Kavram görevi)
4. Alt bant: Görev 4 (+30), aynen. Sol alt: 3B köşesinin cevabı.

**s.11 (R)**, devam: "4. durak · Urfa çarşısı · devam" · *Tanecik sayımı*.
- **A:** **Tanecik tanıtımı** (yeni, konu karakterleri) + H7, H8 (+20). Kart başlığı "Çarşıda tanışma · üç tanecik, iki iyon";
  beş karakter yan yana, her birinin altında iki satırlık balon:
  - `kk-proton`: "Ben protonum: +1, çekirdekteyim. Sayım kimliktir: Z = p."
  - `kk-notron`: "Ben nötronum: yüksüzüm, çekirdekteyim. A = p + n."
  - `kk-elektron-sakin`: "Ben elektronum: −1 ve çok hafifim. Alınıp verilen benim."
  - `kk-iyon-arti`: "Elektron verdim, katyon oldum: e = p − yük."
  - `kk-iyon-eksi`: "Elektron aldım, anyon oldum."
- **B · Hap Bilgi ×3:**
  - Altın Kural: "Kimyasal olaylarda çekirdek değişmez: p ve n aynı kalır, yalnız *elektronlar* alınıp verilir." · alt not:
    "Kimlik proton sayısıdır." (kaynak: Hülasa 01 + s.5 Yoldan)
  - Dikkat!: "Nötron sayısı *n = A − Z*’dir, A − e değil. İyonda e değişir, n değişmez." (kaynak: Hülasa "En sık 4 hata")
  - Unutma!: "Katyon: e = p − yük. Anyon: e = p + yükün büyüklüğü. Cl⁻: 17 + 1 = 18 e⁻." (kaynak: H8)
- **C:** Tuzak! ikili + Yoldan (bakırcılar, aynen):
  - Yanlış bilinen: "Na⁺ olurken Na bir proton kaybeder." · mini `{{kk|kk-iyon-arti|mini}}`
  - Doğrusu: "Çekirdek değişmez; Na⁺ bir elektron vermiştir, p yine 11." · çip "p 11 · e 10" (mevcut Tuzak metni aynen)
- **D:** Kendini dene (KD4, +10) + Bir bakışta.
  - KD4-1: "²⁴₁₂Mg²⁺ iyonunda kaç elektron var?" → *10.*
  - KD4-2: "¹²C ile ¹³C arasındaki ilişki nedir?" → *İzotop (ikisinde de 6 p).*
  - Bir bakışta: (1) **Z = p** (kimlik) · A = p + n · n = A − Z. (2) İyonda yalnız **elektron** değişir: e = p − yük.
    (3) İzotop aynı p · izoton aynı n · izobar aynı A · izoelektronik aynı e ve dizilim.
- **Köşe (+30):** "X³⁺ iyonunda 10 elektron var. X’in atom numarası kaçtır?" · Anahtar: *Katyon: p = e + yük.* · `.ogr` 13 ·
  arka (s.12): `{{kose-arka|CEVAP|Z = 13|p = 10 + 3}}`

### 3.5 · 5. durak · Halfeti (s.12 L · s.13 R)

**s.12 (L)**, bant `halfeti` (b40), levha aynen.
1. Sohbet + Kavram (üç kural; çipsiz), aynen.
2. **Halfeti teknesi** (yeni çizim `tekne_iskelesi`, ≈ 188 × 58 mm): iskelede enerji sırasıyla dizilmiş tekneler = orbitaller
   (1s · 2s · 2p'nin üç teknesi), `kk-elektron` karakterleri ₇N'nin 7 elektronu olarak biner; spin, karakterin üstünde çizgi okla
   (yazı değil). Etiketler: "önce alçak iskele (Aufbau)" · "teknede en çok iki kişi, sırtları zıt (Pauli)" · "boş tekne varken
   eşleşme yok (Hund)". Küçük ek: "Yanlış: iki elektron aynı teknede, öteki tekne boş" (2p {{orb|ud,u,0}} gibi). Yalnız su ve
   tekne; Rumkale ile Savaşan köyünün su içindeki minaresi çizilmez.
3. Dolma sırası (`aufbau`, mevcut) solda, Görev 5 (+30, mevcut) sağda.
4. Alt bant: Soy gaz kısaltması kartı (+30, mevcut; başlığı "Soy gaz kısaltması · sen yaz" olur, "Kendini dene" ile karışmasın).
   Sol alt: 4. durağın köşe cevabı.

**s.13 (R)**, devam: "5. durak · Halfeti · devam" · *Dizilim kuralları*.
- **A:** H9, H10 (+20) + Yoldan (Birecik Barajı, aynen).
- **B · Hap Bilgi ×4:**
  - Kilit bilgi: "Elektronlar en düşük enerjili boş orbitale girer: sırayı numara değil **enerji** belirler." (kaynak: Kavram + s.6 Tuzak doğrusu)
  - Dikkat! (eski Tuzak): "3d, 4s’ten *sonra* dolar: 4s’nin enerjisi daha düşük. …3p⁶ 4s² 3d… diye yaz." (kaynak: s.6 Tuzak, H9)
  - Unutma!: "Kontrol: üst simgelerin toplamı elektron sayısına eşit olmalı." (kaynak: Kavram)
  - Hap bilgi (`.gol`): "[Ne] = 10 e⁻ · [Ar] = 18 e⁻" (kaynak: Soy gaz kartı)
- **D:** Kendini dene (KD5, +10) + Bir bakışta.
  - KD5-1: "₁₇Cl’nin dizilimini soy gaz kısaltmasıyla yaz." → *[Ne] 3s² 3p⁵.*
  - KD5-2: "Bir orbitalde aynı spinli iki elektron bulunabilir mi?" → *Hayır (Pauli: spinler zıt).*
  - Bir bakışta: (1) **Aufbau:** en düşük enerjiden başla; 4s, 3d’den önce dolar. (2) **Pauli:** bir orbitalde en çok 2 e⁻,
    spinleri zıt. (3) **Hund:** eş enerjili orbitallere önce teker teker, aynı yönlü.
- **Köşe (+30):** "₁₅P atomunda kaç yarı dolu orbital var?" · Anahtar: *3p³ için Hund.* · `.ogr` 3 ·
  arka (s.14): `{{kose-arka|CEVAP|3|3p^{3}: birer e^{−}}}`

### 3.6 · 6. durak · Fırat kıyısı (s.14 L · s.15 R)

**s.14 (L)**, bant `firat`, levha aynen.
1. Sohbet + Kavram (+30), aynen.
2. Dizilimi oku · beş atom tablosu + İki ünlü istisna (mevcut).
3. Sınav Radarı (AYT): "Cr ve Cu istisnaları ile küresel simetri sık sorulur." + Yoldan (Fırat halkaları, aynen).
4. Alt bant: Görev 6 (+30), aynen. Sol alt: 5. durağın köşe cevabı.

**s.15 (R)**, devam: "6. durak · Fırat kıyısı · devam" · *Değerlik ve simetri*.
- **A:** **Dış katman konuşuyor** (yeni çizim `dis_katman`, ≈ 120 × 50 mm) + H11, H12 (+20): ₁₂Mg'nin Bohr çizimi (2 · 8 · 2);
  iç katmanlarda küçük sakin noktalar, dış katmanda iki `kk-elektron-heyecan`. Balon: "Biz değerlik elektronlarıyız: tepkimede
  alınıp verilen biziz!" Alt yazı: "Mg: [Ne] 3s² · değerlik 2".
- **B · Hap Bilgi ×3:**
  - Kilit bilgi: "Değerlik elektronları en yüksek enerji düzeyindekilerdir; d dolmaya başladıysa son s ve d birlikte sayılır." (kaynak: Kavram, H11)
  - Unutma!: "İki istisna: Cr [Ar] 4s¹ 3d⁵ · Cu [Ar] 4s¹ 3d¹⁰" (kaynak: H12)
  - Dikkat!: "Simetri için son alt kabuk *yarı ya da tam dolu* olmalı: p⁴ ya da d⁶ ile biten dizilim simetrik değildir." (kaynak: Kavram)
- **C:** Tuzak! ikili:
  - Yanlış bilinen: "Uyarılmış atom farklı bir elementtir." · mini: "temel: 2s {{orb|ud}} 2p {{orb|0,0,0}}"
  - Doğrusu: "Be’nin 1s² 2s¹ 2p¹ hâli de Be’dir; proton sayısı aynı." · mini: "uyarılmış: 2s {{orb|u}} 2p {{orb|u,0,0}}" (mevcut metin aynen)
- **D:** Kendini dene (KD6, +10) + Bir bakışta.
  - KD6-1: "₁₉K’nın değerlik elektron sayısı kaçtır?" → *1 ([Ar] 4s¹).*
  - KD6-2: "₁₈Ar küresel simetrik midir?" → *Evet (3p⁶ tam dolu).*
  - Bir bakışta: (1) **Değerlik:** en yüksek düzeydeki e⁻; geçiş metalinde son s + d. (2) **Küresel simetri:** s¹, s², p³, p⁶, d⁵,
    d¹⁰ ile biten dizilimde var. (3) **İstisna:** Cr 4s¹ 3d⁵, Cu 4s¹ 3d¹⁰; katyonda önce 4s boşalır.
- **Köşe (+30):** "₁₄Si: değerlik elektronu ve yarı dolu orbital sayısı kaçtır?" · Anahtar: *[Ne] 3s² 3p²* · `.ogr` 4 · 2 ·
  arka (s.16): `{{kose-arka|CEVAP|4 · 2|[Ne] 3s^{2} 3p^{2}}}`

Köşe cevaplarının sığma sınırı (`kose_cevap_ici`): büyük satır 7 mm'den başlar, 6,2 mm boyda ≤ 36 mm; alt satır 3,2 mm boyda ≤ 30 mm.

## 4. 3B açılımı (s.8 L · s.9 R) · bonus, akçesiz

Her iki sayfa: `{{zemin}} {{hud|n}} {{cini}}`, `k-bas` başlığı (rozet "3B"), `ub-serit`, `ub-izgara` kartları (§16.5 biçimi).
Anaglifte renk yok; düz resimlerde kitabın tanecik renkleri (proton mercan, nötron gri, elektron kobalt). Ölçeksiz olanlar yazılır.

**s.8 · Orbitaller üç boyutta** (sol alt: 3. durağın köşe cevabı)
- Başlık: "Orbitaller *üç boyutta*" · "Kâğıt düz, orbital değil. Gözlüğünü tak: kırmızı cam sol gözüne."
- Şerit: "**3B gözlükle bak:** kırmızı cam sol gözde, kitap 35–40 cm uzakta ve düz. Gözlüğün yoksa küçük düz resme bak."
- Kartlar (her birinde `{{ana|…}}` + `{{duz|…}}` + "gözlüksüz" + kısa metin; eksenler ince çubuk, uçta x, y, z harfli küçük küre):
  1. `orb-s` (geniş kart) "s orbitalleri · 1s ve 2s": "İkisi de küre. 2s daha büyük: elektron çekirdekten daha uzakta da bulunabilir. Her biri en çok 2 e⁻."
  2. `orb-px` "2pₓ · x ekseninde": "İki lob çekirdeğin iki yanında; ortada, çekirdekte elektron bulunmaz."
  3. `orb-py` "2p_y · y ekseninde": "Aynı biçim, yukarı–aşağı."
  4. `orb-pz` "2p_z · z ekseninde": "Bu orbital kâğıttan sana doğru uzanır: öndeki lob sayfanın önünde görünür."
  5. `orb-p3` "2p · üçü birlikte": "Üç orbital birbirine dik; üçü en çok 6 e⁻ alır."
- Hap Bilgi ×3: Dikkat! "p orbitalinin iki lobu *tek bir orbitaldir*; iki lob birlikte en çok 2 e⁻ alır." (kaynak: s.4 Kavram) ·
  Unutma! "Orbital, elektronun yolu değildir; bulunma olasılığı yüksek bölgedir." (kaynak: s.3 Kavram) ·
  Hap bilgi (`.kob`) "s: küre · p: iki loblu, üç eksende" (kaynak: orbital biçimleri çizimi).
- Kendini dene (`data-soru="KD7"`, **bonus**, çipsiz): (1) "Hangi 2p orbitali kâğıttan sana doğru uzanıyordu?" → *2p_z.*
  (2) "2pₓ orbitalinin iki lobunda toplam en çok kaç elektron bulunur?" → *2.* · Ters: "Cevaplar: 1 2p_z · 2 iki elektron"

**s.9 · Alfa tanecikleri üç boyutta** (sağ alt: bonus köşe)
- Başlık: "Alfa tanecikleri *üç boyutta*" · "Altın levhanın içine gir: tanecikler sana doğru geliyor."
- Kartlar:
  1. `alfa-levha` (geniş, ≈ 120 × 72 mm) "Altın levhanın içinde · ölçekli değil": seyrek dizilmiş altın çekirdekleri (küçük koyu küre),
     soldan arkadan gelip öne çıkan 9 alfa izi (ince silindir zinciri): 7'si düz, 1'i bir çekirdeğin yanından sapar, 1'i tam üstüne
     gelip geri döner. Etiketler (kartın HTML'inde): "altın çekirdekleri (büyütüldü)" · "düz geçen alfalar: çoğu" · "sapan alfa" ·
     "geri dönen alfa". Metin: "Çoğu alfa, çekirdeklerin arasındaki boşluktan düz geçer. Bir çekirdeğin yakınından geçen sapar;
     tam üstüne gelen geri döner."
  2. `alfa-tanecik` "Alfa taneciği yakından": dörtyüzlü dizilmiş 2 koyu (p harfli) + 2 açık (n harfli) küre. "Alfa taneciği bir
     helyum çekirdeğidir: 2 proton + 2 nötron, yükü +2."
  3. `atom-bosluk` "Atomun boşluğu": küçücük çekirdek + çevresinde ≈ 150 küçük noktalı elektron bulutu (1s benzeri dağılım).
     "Ortada küçücük çekirdek, çevresinde elektron bulutu. Gerçek ölçekte çekirdek bu resimde görünmezdi."
- Hap Bilgi ×3: Kilit bilgi "Atomun kütlesinin %99,9’dan fazlası çekirdektedir; hacminin neredeyse tamamı boşluktur." (kaynak: s.5 Yoldan) ·
  Dikkat! "Resimdeki çekirdekler *büyütüldü*; gerçek ölçekte görünmezlerdi." (kaynak: s.3 sohbet) ·
  Unutma! "Gözlük: kırmızı cam sol gözde. Sayfayı ölçeklemeden bas, 35–40 cm’den bak." (kaynak: uc-boyut kuralları)
- **Köşe (bonus, çipsiz, anahtarsız):** "Atomun çapı yaklaşık 10⁻¹⁰ m, çekirdeğinki yaklaşık 10⁻¹⁵ m. Atom, çekirdekten yaklaşık
  kaç kat büyüktür?" · `.ogr` 100 000 · arka (s.10): `{{kose-arka|CEVAP|10^{5} kat|yaklaşık 100 000}}`

meta.json `"uc_boyut"` (boyutlar ilk öneri; `donus` hafif eğik bakış):

```json
[{"ad": "orb-s", "yapi": "orbital_s", "en": 96, "yuk": 44, "duz": [30, 22], "donus": [[12, -18, 0]]},
 {"ad": "orb-px", "yapi": "orbital_p:x", "en": 56, "yuk": 42, "duz": [24, 20], "donus": [[12, -18, 0]]},
 {"ad": "orb-py", "yapi": "orbital_p:y", "en": 56, "yuk": 42, "duz": [24, 20], "donus": [[12, -18, 0]]},
 {"ad": "orb-pz", "yapi": "orbital_p:z", "en": 56, "yuk": 42, "duz": [24, 20], "donus": [[12, -18, 0]]},
 {"ad": "orb-p3", "yapi": "orbital_p_uc", "en": 56, "yuk": 42, "duz": [24, 20], "donus": [[12, -18, 0]]},
 {"ad": "alfa-levha", "yapi": "alfa_levha", "en": 120, "yuk": 72, "duz": [48, 29]},
 {"ad": "alfa-tanecik", "yapi": "alfa_tanecik", "en": 46, "yuk": 46, "duz": [22, 22]},
 {"ad": "atom-bosluk", "yapi": "atom_bosluk", "en": 56, "yuk": 50, "duz": [24, 22]}]
```

Kurucular (`Yapi` döndürür) `infografik_unite.py`'ye (kur_ortak 3B kurucularını `sahneler_unite` ve `infografik_unite`'de arar):
`orbital_s()`, `orbital_p(eksen)`, `orbital_p_uc()`, `alfa_levha()`, `alfa_tanecik()`, `atom_bosluk()`. Lob için motorda elipsoid
olmadığından ya ortak `Yapi.elipsoid(...)` eklenir ya da lob, eksen boyunca 9–11 kürenin birleşimiyle çizilir (damla profili; §9).
Tonlar gri: 1s açık, 2s orta; pₓ açık, p_y orta, p_z koyu (üçü birlikte kartında ayrılsın).

## 5. Kat yaprağı

### 5.1 · s.17 (R) · "Katla, doğrusu kalsın!"

```html
<section class="sayfa s17 kat">{{zemin14}}{{hud|17|kat}}{{cini14}}{{katla-cumle}}{{alt|17|kat}}</section>
```

**Mekanik:** her satırda büyük bir cümle şeridi sayfayı boydan geçer. Açıkken cümle yanlıştır; orta şerit (70–140 mm) arkaya
katlanınca yanlış parça gizlenir, kalan sol + sağ parça doğru cümleyi okur. Bölünme sözcük arasından (harf kesilmez); sol parça
A'dan, orta parça iki çizgiden, sağ parça B'den en az 1,2 mm uzak. Katlıyken araya ≈ 2,4 mm'lik boşluk düşer (bir sözcük arası).
Başlık da aynı oyunu oynar: "Katla," + "(ama önce yanlışı bul!)" + "doğrusu kalsın!" → katlıyken "Katla, doğrusu kalsın!".

Başlık satırı: sol "Yol 3 · Şanlıurfa–Harran" / "Dört cümle, tek katlama." · sağ "Dört cümlede de yanlış var." / "4 tahmin · +40 akçe" ·
balon "Önce yanlışı bul, / sonra katla!". Alt: "Kat izini tırnağınla keskinleştir." · "A ile B buluşunca oku" · "Katlayınca YANLIŞ mühürleri saklanır."

Her satır: sol parçada durak etiketi ve karakter, ortada "ÖNCE TAHMİN ET" kartı (satır: "Yanlış sözcükler:" + İPUCU), cümle
şeridindeki yanlış parça ve küçük `{{muhur|yanlis}}` (orta şeritte, açıkken görünür), "AÇ VE AÇIKLA" kartı (soru: "Neden yanlıştı?"),
sağ parçada kanıt. Dikişte, cümlenin altında yeşil "DOĞRU" kurdelesi (bölünen harf **O**; katlıyken birleşir).

| Kod | Durak | Sol parça | Orta (gizlenen, yanlış) | Sağ parça | Katlıyken (doğru) |
|---|---|---|---|---|---|
| C1 | 1 · Göbeklitepe | Dalton modelinde atom | elektronlu ve çekirdekli, | içi dolu bir küredir. | Dalton modelinde atom içi dolu bir küredir. |
| C2 | 2 · Harran | Alfaların çoğu | levhadan geri döndü, çok azı | sapmadan geçti. | Alfaların çoğu sapmadan geçti. |
| C3 | 4 · Urfa çarşısı | İzotoplarda proton | sayısı farklı, nötron | sayısı aynıdır. | İzotoplarda proton sayısı aynıdır. |
| C4 | 6 · Fırat kıyısı | Ca²⁺ olurken elektronlar | önce 3p’den, ardından | 4s’den verilir. | Ca²⁺ olurken elektronlar 4s’den verilir. |

| Kod | Sol parça çizimi | Sağ parça kanıtı | İPUCU | Öğretmen (`g.ogr-svg`) |
|---|---|---|---|---|
| C1 | `kk-dalton-sasiran` · "Dalton · 1803–1808" | `kk-dalton` · "içi dolu, bölünemez" | Elektron 1897’de, çekirdek 1911’de bulundu. | yanlış: elektronlu ve çekirdekli · neden: ikisi de Dalton’dan sonra bulundu |
| C2 | `kk-alfa-sasiran` · "altın levha · 1909" | `kk-alfa-mutlu` · "çoğu düz geçti" | Atomun büyük kısmı boşluktur. | yanlış: levhadan geri döndü, çok azı · neden: çoğu geçti, çok azı döndü |
| C3 | ³⁵₁₇Cl kartı "17 p · 18 n" | ³⁷₁₇Cl kartı "17 p · 20 n" | Kimlik proton sayısıdır. | yanlış: sayısı farklı, nötron · neden: p aynı (17), n farklı (18, 20) |
| C4 | "Ca: [Ar] 4s {{orb|ud}}" | "Ca²⁺: [Ar] 4s {{orb|0}}" | Katyonda önce en dış katman boşalır. | yanlış: önce 3p’den, ardından · neden: iki e⁻ de 4s’den gider, 3p⁶ kalır |

Genişlik tahmini (Nunito 800, 4,8 mm; sınırlar: sol ≤ 60,8 mm, orta ≤ 67,6 mm, sağ ≤ 60,8 mm): C1 54 · 63 · 51 mm ·
C2 36 · 64 · 37 · C3 47 · 52 · 37 · C4 56 · 53 · 36. Kısa orta parçalar sözcük aralığıyla iki yana yayılır. Uygularken fontTools
ölçüsüyle tek bir boy seçilir (4,4–5,0 mm). Sığmazsa yedekler: C1 orta "elektronlu, çekirdekli," · C4 sol "Ca²⁺ olurken e⁻’lar".
Satır verisi `sahneler_unite.KATLA_CUMLE` (biçim §7.4).

### 5.2 · s.18 (L) · Karma sayfa: kapıyı aç

`{{hud|18}}`, `{{zemin}}`, `{{cini}}`, başlık `k-bas`: `{{rozet|3|YOL}}` · "Karma sayfa: *kapıyı aç*" · "Altı soru, bir şifre · bir
çeldirici röntgeni · bir yapay zekâ hatası · heybeden dört soru" · `<span class="kat-not">{{kikon|katla}}Kat izleri sütun aralığına düşer</span>`.
Sütunlar: k1 Kapı kartı + Soru 1–3 · k2 Soru 4–6 + Çeldirici Röntgeni · k3 Robot + Heybe. Kat yerinden çizgi, tablo, resim geçmez.

**Şifreli Kapı** (`.kapi-kart`, +60): "Altı sorunun doğru seçeneğindeki harfi sırayla kutulara yaz. Anlamlı bir kelime çıkarsa kapı
açılır." · altında: "Kelime çıkmadıysa bir soruda yanıldın: yanlış harfler kelime kurmaz." · `.sifre` kutularında `.ogr` P R O T O N.

| Soru | Kaynak etiketi | Soru metni | Seçenekler (kod harfi · metin) | Doğru |
|---|---|---|---|---|
| SK1 | Yol 3 · 1. durak | Atomun içinde (−) yüklü tanecikler bulunduğunu söyleyen ilk model hangisidir? | N Demokritos’un atomos fikri · M Dalton modeli · **P Thomson modeli** · Ç Bohr modeli · Z Modern model | P |
| SK2 | Yol 3 · 2. durak | Rutherford modeli hangisini açıklayamaz? | C Alfaların çoğunun sapmadan geçmesini · Ş Bazı alfaların geri dönmesini · V (+) yükün küçük bir bölgede toplanmasını · Y Kütlenin neredeyse tamamının çekirdekte olmasını · **R Elektronun çekirdeğe düşmemesini** | R |
| SK3 | Yol 3 · 3. durak | n = 2 enerji düzeyinde kaç orbital vardır? | B 2 · **O 4** · D 6 · G 8 · H 9 | O |
| SK4 | Yol 3 · 4. durak | Elektron sayısı 18, nötron sayısı 20 olan X²⁺ iyonunun kütle numarası kaçtır? | Ğ 20 · J 36 · V 38 · **T 40** · Ş 58 | T |
| SK5 | Yol 3 · 5. durak | “Bir orbitalde en çok iki elektron bulunur; spinleri zıttır.” Bu hangi kuraldır? | **O Pauli ilkesi** · B Aufbau ilkesi · D Hund kuralı · G Bohr modeli · H Küresel simetri | O |
| SK6 | Yol 3 · 6. durak | Hangisinin temel hâl dizilimi küresel simetriktir? | Ç ₁₄Si · **N ₁₅P** · J ₁₃Al · Ğ ₁₆S · V ₁₇Cl | N |

Çeldiricilerin kaynağı: SK4'te 20 = A'yı p sandı, 36 = p'yi e − 2 aldı, 38 = p'yi e aldı, 58 = e'yi de ekledi. Harf kümeleri:
1 {N M P Ç Z} · 2 {C Ş V Y R} · 3 {B O D G H} · 4 {Ğ J V T Ş} · 5 {O B D G H} · 6 {Ç N J Ğ V}. 5⁶ = 15 625 dizilimden okunabilen
(katla dogrula'sındaki ölçüt) yalnız PRO?O? kalıbındaki 25 dizi: PROĞOÇ PROĞOJ PROĞON PROĞOĞ PROĞOV PROJOÇ PROJOJ PROJON PROJOĞ
PROJOV PROVOÇ PROVOJ PROVON PROVOĞ PROVOV PROTOÇ PROTOJ **PROTON** PROTOĞ PROTOV PROŞOÇ PROŞOJ PROŞON PROŞOĞ PROŞOV.
PROTON dışında hiçbiri Türkçe kelime değil (betikle sayıldı, gözle bakıldı).

**Çeldirici Röntgeni** (`.kart.rn`, `data-soru="CR1"`, +30): "Birçok diş macununda florür iyonu bulunur. ¹⁹₉F⁻ iyonunun proton,
nötron ve elektron sayıları sırasıyla hangisidir?"

| Şık | Sayılar | Tanı |
|---|---|---|
| A | 9, 10, 9 | Yükü unuttu: e = p saydı. |
| B | 9, 9, 10 | Nötronu A − e ile buldu: 19 − 10. |
| **C** | **9, 10, 10** | Doğru: anyon 1 e⁻ almış, e = 9 + 1. |
| D | 9, 19, 10 | Kütle numarasını nötron saydı. |
| E | 9, 10, 8 | Anyonda elektronu çıkardı: 9 − 1. |

Altında: "p = Z = 9 · n = A − Z = 19 − 9 = 10 · (1−): 1 e⁻ almış, e = 10" · "B’yi seçen arkadaşına bir cümle:" (yaz satırı;
B, Hülasa'daki "n = A − e yazmak" hatası) · "**Sıra sende:** ³⁹₁₉K⁺ için bir çeldirici uydur; hangi hatayı taşıdığını yaz."
(`.ogr`: "Doğrusu 19, 20, 18; ör. 19, 20, 20 = yükü ekledi").

**Robot yanıldı mı?** (`.robot-kart`, `data-soru="RB1"`, +30): "KimyaBot’a soruldu: “Hidrojen neden çizgili ışık verir?” Yanıtında *tek* bir hata var."
1. Hidrojendeki elektron yalnız belirli enerji düzeylerinde bulunabilir.
2. Elektron üst düzeyden alta inerken iki düzeyin enerji farkı kadar enerjili ışık yayar.
3. Fark büyüdükçe ışığın dalga boyu da büyür: 6’dan 2’ye iniş kırmızı ışık verir. ← `data-dogru` (hatalı)
4. Düzeyler her elementte farklı olduğu için her elementin çizgileri kendine özgüdür.

"Hatalı cümle no: ___ · Doğrusu:" · `.ogr`: "3 · Fark büyüdükçe dalga boyu kısalır: 6’dan 2’ye iniş mor (410 nm), 3’ten 2’ye iniş
kırmızı (656 nm)." · Ters satır: "Cevap: 3. cümle" · "KimyaBot kurgusal bir yapay zekâdır; gerçek bir uygulama değildir."

**Heybe** (`.heybe-kart`, 4 × 10 = +40; her cevap `.yaz-satir > .ogr`):
1. `1 yol önce · Yol 2`: "Derişik asit seyreltilirken hangisi yapılır: asit suya mı eklenir, su asite mi?" → *Asit suya; yavaşça, karıştırarak.* (9/02 H3)
2. `2 yol önce · Yol 1`: "pH’ı 9 olan sabunlu su asidik mi, bazik mi?" → *Bazik (pH > 7).* (9/01 H3)
3. `Bu yoldan · 5. durak`: "₈O atomunun 2p orbitallerinde kaç yarı dolu orbital vardır?" → *2 (2p⁴).*
4. `Bu yoldan · 2. durak`: "M katmanı (n = 3) en çok kaç elektron alır?" → *18 (2n²).*
- Ters: "Cevaplar: asit suya · bazik · 2 · 18"

Nineme Anlat bu sayfaya girmiyor (koordinatör listesinde yok); k3'te yer artarsa eklenebilir.

## 6. Değişen mevcut sayfalar

- **s.1 Yola çıkış:** çip satırı aynı (`{{meta|akce_toplam}}` 1600 yazar); ikinci çip satırı: "1 katla sayfası · 7 köşe · 2 sayfa 3B".
  Ahilik: Çırak 0+ · Kalfa 450+ · Usta 900+ · Atom Üstadı 1300+. İşaretler 6 → 8: + "Köşe · Önce çöz, sonra köşeyi katla."
  (`{{kikon|kose}}`), + "3B · Kırmızı cam sol göze." (`{{ub-ikon|gozluk}}`). Panorama etiketleri §7.2.
- **s.16 Hülasa:** sol alt 64 × 64 mm köşe cevabı (`{{kose-arka|CEVAP|4 · 2|[Ne] 3s^{2} 3p^{2}}}`, `{{alt|16|kose-arka}}`).
  Alt satır: Muhasebe sağa (70–199 mm), "Kendime not" sandık satırının sağına ya da muhasebenin altına iki satır. "Tekrar için:
  modeller s.{{sayfa|2}}–{{sayfa|5}} · ışık ve orbital s.{{sayfa|6}}–{{sayfa|9}} · p, n, e s.{{sayfa|10}}–{{sayfa|11}} · kurallar
  s.{{sayfa|12}}–{{sayfa|13}} · simetri s.{{sayfa|14}}–{{sayfa|15}}".
- **s.19 Meclis:** "s.{{sayfa|15}}" → "s.{{sayfa|25}}".
- **s.25 Cevaplar:** tekrar rotası: 1. durak s.{{sayfa|2}} · 2. durak s.{{sayfa|4}} · 3. durak s.{{sayfa|6}} · 4. durak s.{{sayfa|10}} ·
  5. durak s.{{sayfa|12}} · 6. durak s.{{sayfa|14}}. Hızlı anahtarın altına tek satır: "Yeni sayfalar: Kendini dene cevapları ters
  yazılı · köşe cevapları arka yüzde · Katla: katlayınca doğrusu kalır · Karma: Kapı PROTON · Röntgen C · Robot 3. cümle ·
  Heybe: asit suya · bazik · 2 · 18".
- **s.26 Final:** defterde Hülasa'dan sonra iki satır: "Katla · doğrusu kalsın | 40" ve "Karma sayfa · kapıyı aç | 160"; TOPLAM 1600.
  Unvanlar: 0–449 · 450–899 · 900–1299 · 1300–1600. Akçe rayı 1600 ölçeğinde (§9).

## 7. meta.json ve kur.py

### 7.1 meta.json
- `"sayfa_sayisi": 26`, `"akce_toplam": 1600`, `"palet": "cini-toprak"`, `"uc_boyut": […]` (§4).
- `duraklar[i]`: `"sayfa"` ilk sayfa olur, yeni `"sayfalar"`: 1 → [2, 3] · 2 → [4, 5] · 3 → [6, 7] · 4 → [10, 11] · 5 → [12, 13] · 6 → [14, 15].
- `medeniyet[i].sayfa`: İbn Heysem 3 · Sâbit bin Kurra 5 · el-Battânî 7.
- Ahilik eşikleri ortak destek gelirse: `"ahilik": [450, 900, 1300]`.

### 7.2 kur.py
```python
SAYFA = {
    1: ('Yola çıkış', 'Şanlıurfa–Harran yolu · yola çıkış', 0),
    2: ('1. durak · <b>Göbeklitepe</b>', '1. durak · Atom modellerinin yolculuğu', 0),
    3: ('1. durak · <b>Göbeklitepe</b>', '1. durak · Model zinciri: tekrar ve köşe', 3),
    4: ('2. durak · <b>Harran</b>', '2. durak · Altın levha çizgi romanı', 6),
    5: ('2. durak · <b>Harran</b>', '2. durak · Çekirdek, katmanlar, elektron bulutu', 8),
    6: ('3. durak · <b>Höyük</b>', '3. durak · Enerji merdiveni ve ışık', 14),
    7: ('3. durak · <b>Höyük</b>', '3. durak · Orbitaller, lamba spektrumu', 18),
    8: ('3. durak · <b>3B</b>', '3B · Orbitaller üç boyutta', 21),
    9: ('3. durak · <b>3B</b>', '3B · Alfa tanecikleri üç boyutta', 21),
    10: ('4. durak · <b>Urfa çarşısı</b>', '4. durak · p, n, e ve iyonlar', 21),
    11: ('4. durak · <b>Urfa çarşısı</b>', '4. durak · Tanecikler ve izo kardeşler', 25),
    12: ('5. durak · <b>Halfeti</b>', '5. durak · Elektron dizilimi kuralları', 29),
    13: ('5. durak · <b>Halfeti</b>', '5. durak · Aufbau, Pauli, Hund: tekrar', 32),
    14: ('6. durak · <b>Fırat kıyısı</b>', '6. durak · Değerlik elektronu, küresel simetri', 36),
    15: ('6. durak · <b>Fırat kıyısı</b>', '6. durak · Dış katman konuşuyor', 40),
    16: ('Hülasa · <b>Gümrük Hanı</b>', 'Hülasa · atomun özeti', 44),
    17: ('Hülasa · <b>Katla</b>', 'Katla sayfası · doğrusu kalsın', 46),
    18: ('Hülasa · <b>Karma</b>', 'Karma sayfa · kapıyı aç', 49),
    19: ('Yan yol · <b>Sıra gecesi</b>', 'Yan yol 1 · Meclis: kim haklı?', 59),
    20: ('Yan yol · <b>Harran Ovası</b>', 'Yan yol 2 · Kıssalar', 66),
    21: ('Yan yol · <b>Urfa evleri</b>', 'Yan yol 3 · Anahtar merdiveni', 74),
    22: ('<b>Urfa Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 81),
    23: ('<b>Urfa Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 91),
    24: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    25: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    26: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD noktaları aynı (6 durak + Hülasa + 3 yan yol + kale); 3B, kat ve karma yanındaki durağın/Hülasa'nın noktasında
SIMDI = {1: -1, 2: 0, 3: 0, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 4, 13: 4, 14: 5, 15: 5,
         16: 6, 17: 6, 18: 6, 19: 7, 20: 8, 21: 9, 22: 10, 23: 10, 24: 11, 25: 11, 26: 11}
```
Panorama `ETIKET` sayfa alanları: 1 "2–3" · 2 "4–5" · 3 "6–9" (ad "Işık ve orbitaller · 3B") · 4 "10–11" · 5 "12–13" · 6 "14–15" ·
H "16–18|+240 akçe" (ad "Hülasa · katla · karma") · M "19" · K "20" · A "21" · V "22–23".
`_rozet_duzelt` silinir: ortak `hno` üç haneli kodu artık kendisi küçültüyor ve fontu tırnaklı yazıyor; eski regex hiç eşleşmez.

### 7.3 infografik_unite.py
- `gelistirme/atom-modelleri/uretec/infografik_gelistirme.py`'den kopya (oradaki dosyaya dokunulmaz): `zincir_yolu`,
  `pano_duzenek … pano_sonuc` (yardımcılarıyla), `enerji_merdiveni`, `mini_yorunge`, `mini_bulut`. Konu karakterleri ortak `KK`'den.
- Yeni: `tekne_iskelesi` (s.12), `dis_katman` (s.15), 3B kurucuları (§4).
- Kullanılmayan `model_yolculugu`, `altin_levha`, `spektrum` silinebilir; veri sabitleri kalır.

### 7.4 sahneler_unite.py · `KATLA_CUMLE`
```python
KATLA_CUMLE = [   # tek doğruluk kaynağı: dogrula.py cümleleri ve genişlikleri yeniden denetler
    dict(kod="C1", durak="1. durak · Göbeklitepe", sol="Dalton modelinde atom", orta="elektronlu ve çekirdekli,", sag="içi dolu bir küredir.",
         ipucu=["Elektron 1897’de, çekirdek 1911’de bulundu."], sol_kk=("kk-dalton-sasiran", "Dalton · 1803–1808"),
         sag_kk=("kk-dalton", "içi dolu, bölünemez"), neden="İkisi de Dalton’dan sonra bulundu."),
    dict(kod="C2", durak="2. durak · Harran", sol="Alfaların çoğu", orta="levhadan geri döndü, çok azı", sag="sapmadan geçti.",
         ipucu=["Atomun büyük kısmı boşluktur."], sol_kk=("kk-alfa-sasiran", "altın levha · 1909"),
         sag_kk=("kk-alfa-mutlu", "çoğu düz geçti"), neden="Çoğu geçti, çok azı döndü."),
    dict(kod="C3", durak="4. durak · Urfa çarşısı", sol="İzotoplarda proton", orta="sayısı farklı, nötron", sag="sayısı aynıdır.",
         ipucu=["Kimlik proton sayısıdır."], sol_iz=(35, 17, "Cl", "17 p · 18 n"), sag_iz=(37, 17, "Cl", "17 p · 20 n"),
         neden="p aynı (17), n farklı (18 ve 20)."),
    dict(kod="C4", durak="6. durak · Fırat kıyısı", sol="Ca^{2+} olurken elektronlar", orta="önce 3p’den, ardından", sag="4s’den verilir.",
         ipucu=["Katyonda önce en dış katman boşalır."], sol_orb=("Ca", "[Ar] 4s", "ud"), sag_orb=("Ca^{2+}", "[Ar] 4s", "0"),
         neden="İki e^{−} de 4s’den gider; 3p^{6} kalır."),
]
```
Öğretmen grubu `_ogr_grubu(kod, urun=katlı cümle, tur=orta parça, …)`; böylece ortak `katla_ayni` aynen kullanılır.

## 8. dogrula.py · eklenecek ve değişecek denetimler (taslak)

Mevcut motor (`dizilim`, `iyon_dizilim`, `yari_dolu`, `kuresel`, `degerlik`, `pne`, `izo`, `MODEL`, `THOMSON`, `R`, `IU.*`) kullanılır.

```python
from dogrula_ortak import kendini_dene_ayni, sifreli_kapi_ayni, celdirici_ayni, robot_ayni, katla_ayni, uc_boyut_resimleri
import sahneler_unite as SU

def bolum(n_):                      # "sayfa sNN ek-sınıf" sırası şart
    return re.search(rf'<section class="sayfa s{n_}\b.*?</section>', SABLON, re.S).group(0)
def bolumler(ss):
    return "".join(bolum(n_) for n_ in ss)

# ---- yapı ve parite
kontrol("26 sayfa (çift), meta ile aynı", SABLON.count('<section class="sayfa s') == 26 == META["sayfa_sayisi"])
KOSE_ON = [3, 5, 7, 9, 11, 13, 15]
for n_ in range(1, 27):
    t = bolum(n_)
    kontrol(f"s.{n_}: köşe ön yüzü yalnız tek sayfada, arka yüzü hemen sonraki çift sayfada",
            ("{{kose-on}}" in t) == (n_ in KOSE_ON) and ("{{kose-arka|" in t) == (n_ - 1 in KOSE_ON)
            and ("|kose-on}}" in t) == (n_ in KOSE_ON) and ("|kose-arka}}" in t) == (n_ - 1 in KOSE_ON))
kontrol("kat sayfası s.17 (tek), karma s.18", "{{katla|cumle}}" in bolum(17) and 'class="kol k1"' in bolum(18))
kontrol("3B açılımı s.8–9: 8 anaglif, akçe çipi yok", sum(bolum(n_).count("{{ana|") for n_ in (8, 9)) == 8
        and all("cip akce" not in bolum(n_) for n_ in (8, 9)))
kontrol("7 köşe kartında öğretmen cevabı", HTML.count('<div class="cevap-kutu">CEVABIN:<span class="ogr">') == 7)

# ---- köşe cevapları: hesap = .ogr = arka yüz
KOSE = {3: ("2", sum(THOMSON.values()) == 2), 5: ("8", 2 * 2 ** 2 == 8), 7: ("H ve Na", var == ["H", "Na"]),
        9: ("100 000", round(1e-10 / 1e-15) == 100000), 11: ("13", 10 + 3 == 13),
        13: ("3", yari_dolu(dizilim(15)) == 3), 15: ("4 · 2", (degerlik(dizilim(14)), yari_dolu(dizilim(14))) == (4, 2))}
ARKA = {4: "2", 6: "8 e^{−}", 8: "H ve Na", 10: "10^{5} kat", 12: "Z = 13", 14: "3", 16: "4 · 2"}
for n_, (c, ok) in KOSE.items():
    kontrol(f"köşe s.{n_}: {c} hesapla doğru, kartta ve s.{n_ + 1} köşesinde", ok and f'<span class="ogr">{c}</span>' in bolum(n_)
            and f"{{{{kose-arka|CEVAP|{ARKA[n_ + 1]}|" in bolum(n_ + 1))

# ---- Kendini dene (sayfadaki .ogr, sırayla)
kontrol("KD1: Thomson'da (+) yük dağınık; Bohr'dan sonra modern", "(+) yük düzgün" in MODEL["Thomson"])
kontrol("KD2: boşluk ve (+) çekirdek Rutherford'da", {"boşluk", "çekirdek"} <= MODEL["Rutherford"])
kontrol("KD3: 4→2 486 nm yayılır; 6→2 (410) < 3→2 (656)", (balmer[2], balmer[0], balmer[3]) == (486, 410, 656))
kontrol("KD4: Mg2+ 10 e; 12C–13C izotop", pne(24, 12, 2)[2] == 10 and izo((12, 6, 0), (13, 6, 0)) == {"izotop"})
kontrol("KD5: Cl [Ne] 3s2 3p5", yazim(dizilim(17)) == "[Ne] 3s2 3p5")
kontrol("KD6: K değerlik 1; Ar simetrik", degerlik(dizilim(19)) == 1 and kuresel(dizilim(18)))
kontrol("KD7 (3B): bir orbitalde en çok 2 e (p lobu çifti tek orbital)", KAP["p"] // ORB["p"] == 2)
kendini_dene_ayni(HTML, {"KD1": ["her yere dağılmış", "modern model"], "KD2": ["atomun büyük kısmı boşluk", "(+) çekirdek"],
                         "KD3": ["yayar (486 nm)", "6’dan 2’ye (410 nm)"], "KD4": ["10", "izotop"],
                         "KD5": ["[Ne] 3s² 3p⁵", "hayır (Pauli)"], "KD6": ["1", "evet (3p⁶)"], "KD7": ["2p_z", "2"]})

# ---- kat sayfası: açık cümle yanlış, katlı cümle doğru, ölçüler
OLGU = {"C1": (not ({"elektron", "çekirdek"} & MODEL["Dalton"])),                         # Dalton'da ikisi de yok
        "C2": True,                                                                        # gözlem: çoğu geçti (çizgi roman 2. pano)
        "C3": izo((35, 17, 0), (37, 17, 0)) == {"izotop"} and pne(35, 17)[1] != pne(37, 17)[1],
        "C4": iyon_dizilim(20, 2) == dizilim(18) and dizilim(20)["4s"] == 2}
KC = __import__("cizim.katla", fromlist=["katla"])
for s in SU.KATLA_CUMLE:
    katli, acik = f'{s["sol"]} {s["sag"]}', f'{s["sol"]} {s["orta"]} {s["sag"]}'
    gs, go, gg = (KC.genislik(KC.duz(x), BOY) for x in (s["sol"], s["orta"], s["sag"]))   # BOY: seçilen şerit boyu
    kontrol(f'{s["kod"]}: “{acik}” yanlış, “{katli}” doğru; sol {gs:.1f} · orta {go:.1f} · sağ {gg:.1f} mm sığıyor',
            OLGU[s["kod"]] and gs <= 60.8 and go <= 67.6 and gg <= 60.8 and katli.endswith(".") and s["orta"] not in katli)
katla_ayni(HTML, {s["kod"]: (KC.duz(f'{s["sol"]} {s["sag"]}'), KC.duz(s["orta"])) for s in SU.KATLA_CUMLE})
kontrol("DOĞRU kurdelesinde bölünen harf güvenli (O)", "O" in KC.GUVENLI_HARF)

# ---- karma sayfa
ilk = next(m for m in ("Demokritos", "Dalton", "Thomson", "Bohr", "Modern") if "elektron" in MODEL.get(m, set()))
RUTH_ACIKLAR = {"çoğu geçer", "geri döner", "(+) yük küçük bölgede", "kütle çekirdekte"}
SK = {"SK1": tek_sik("SK1 ilk elektronlu model", {"N": "Demokritos", "M": "Dalton", "P": "Thomson", "Ç": "Bohr", "Z": "Modern"}, lambda m: m == ilk, "P"),
      "SK2": tek_sik("SK2 Rutherford açıklayamaz", {"C": "çoğu geçer", "Ş": "geri döner", "V": "(+) yük küçük bölgede", "Y": "kütle çekirdekte",
                                                     "R": "elektron neden düşmez"}, lambda g: g not in RUTH_ACIKLAR, "R"),
      "SK3": tek_sik("SK3 n=2 orbital", {"B": 2, "O": 4, "D": 6, "G": 8, "H": 9}, lambda v: v == 2 ** 2, "O"),
      "SK4": tek_sik("SK4 X2+ e18 n20 → A", {"Ğ": 20, "J": 36, "V": 38, "T": 40, "Ş": 58}, lambda v: v == (18 + 2) + 20, "T"),
      "SK5": tek_sik("SK5 Pauli", {"O": "Pauli", "B": "Aufbau", "D": "Hund", "G": "Bohr", "H": "simetri"}, lambda v: v == "Pauli", "O"),
      "SK6": tek_sik("SK6 küresel simetrik", {"Ç": 14, "N": 15, "J": 13, "Ğ": 16, "V": 17}, lambda z: kuresel(dizilim(z)), "N")}
kontrol("şifre PROTON", "".join(SK.values()) == "PROTON")
sifreli_kapi_ayni(HTML, "PROTON")
# okunabilir dizi analizi: katla dogrula'sındaki ölçütle 25 dizi, hepsi PRO?O? (liste ekrana basılır, gözle bakılır)
A_, Z_, q_ = 19, 9, -1
e_ = Z_ - q_
tani = {"A": (Z_, A_ - Z_, Z_), "B": (Z_, A_ - e_, e_), "C": (Z_, A_ - Z_, e_), "D": (Z_, A_, e_), "E": (Z_, A_ - Z_, Z_ + q_)}
kontrol("Röntgen 19F−: 9, 10, 10 (C); beş seçenek farklı", tani["C"] == pne(19, 9, -1) and len(set(tani.values())) == 5)
celdirici_ayni(HTML, {"CR1": ("C", "9, 10, 10")})
lam = {n: round(1e9 / (R * (1 / 4 - 1 / n ** 2))) for n in (3, 6)}
fark = {n: 13.6 * (1 / 4 - 1 / n ** 2) for n in (3, 6)}
iddia = {1: True, 2: True, 3: (fark[6] > fark[3]) == (lam[6] > lam[3]), 4: True}
kontrol(f"Robot: tek hata 3. cümle (6→2 {lam[6]} nm < 3→2 {lam[3]} nm)", [k for k, v in iddia.items() if not v] == [3])
robot_ayni(HTML, {"RB1": 3})
M02 = json.load(open(os.path.join(BURA, "..", "..", "02-kimyasal-guvenlik", "uretec", "meta.json"), encoding="utf-8"))
M01 = json.load(open(os.path.join(BURA, "..", "..", "01-gunluk-hayatta-kimya", "uretec", "meta.json"), encoding="utf-8"))
kontrol("Heybe 1: asit suya (9/02 H3)", any(h["kod"] == "H3" and "asit → su" in h["formul"] for h in M02["hazine"]))
kontrol("Heybe 2: pH 9 bazik (9/01 H3: asidik < 7 < bazik)", any(h["kod"] == "H3" and "bazik" in h["formul"] for h in M01["hazine"]) and 9 > 7)
kontrol("Heybe 3–4: O 2p4 → 2 yarı dolu; M katmanı 18", yari_dolu({"2p": dizilim(8)["2p"]}) == 2 and 2 * 3 ** 2 == 18)

# ---- 3B
kontrol("3B: n = 2'de 2s + üç 2p = 4 orbital; alfa 2 p + 2 n, yük +2", 1 + ORB["p"] == 4 and pne(4, 2, 2) == (2, 2, 0))
kontrol("3B resimleri: dosya var, mm = piksel / 300 dpi", not uc_boyut_resimleri(HTML, os.path.join(BURA, "..", "unite.html")))

# ---- Hap Bilgi ve durak bileşenleri
HB = ("hb-hap", "hb-kural", "hb-unutma", "hb-radar", "hb-dikkat", "hb-kilit")
for n_ in range(2, 16):
    say = {k: len(re.findall(rf'class="hb {k}\b', bolum(n_))) for k in HB}
    kontrol(f"s.{n_}: Hap Bilgi {sum(say.values())} ≤ 4, aynı türden ≤ 2", sum(say.values()) <= 4 and max(say.values()) <= 2)
for d in META["duraklar"]:
    t = bolumler(d["sayfalar"])
    kontrol(f"{d['no']}. durak: 1 Bir bakışta, 1 Kendini dene, 1 köşe, 4 Hap Bilgi",
            t.count('class="bakista"') == 1 and t.count('class="kart kendini-dene"') == 1 and t.count("{{kose-on}}") == 1
            and sum(len(re.findall(rf'class="hb {k}\b', t)) for k in HB) == 4)

# ---- akçe (eski bölüm, yeni sayfalarla)
for d in META["duraklar"]:
    t = bolumler(d["sayfalar"])
    ana = "".join(p[p.index("<main"):] for p in (bolum(n_) for n_ in d["sayfalar"]))   # levha çipi sayılmaz
    # NOT: alt banttaki .kose-ic kutuları <main> dışında; çipler bölümün <main>'den sonrasının tamamından sayılır
    cipler = [int(v_) for v_ in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', ana)]
    hazine = len(re.findall(r"\{\{hazine\|H\d+\}\}", t)) * 10
    kontrol(f"{d['no']}. durak (s.{d['sayfalar']}): {cipler} + hazine {hazine} = {d['akce']}", sum(cipler) + hazine == d["akce"])
kat = 10 * len(SU.KATLA_CUMLE)
karma = sum(int(v_) for v_ in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', bolum(18)))
kontrol(f"katla {kat} = 40, karma {karma} = 160 (60 + 30 + 30 + 40)", (kat, karma) == (40, 160))
# mec, kis, anh, imt: bolum(19), (20), (21), (22, 23) · Hülasa bolum(16) · Final bolum(26) · s.1 bolum(1) · Üstad bolum(24)
toplam = 700 + 40 + kat + karma + 3 * 120 + 300
kontrol(f"toplam {toplam} = 1600 = meta.akce_toplam", toplam == 1600 == META["akce_toplam"])
once_ = [0, 0, 50, 100, 160, 220, 280, 340, 340, 340, 400, 460, 520, 580, 640, 700, 740, 780, 940, 1060, 1180, 1300, 1450, 1600, 1600, 1600]
kontrol(f"HUD çubukları {cubuk}", cubuk == [round(100 * a / 1600) for a in once_])   # [0,0,3,6,10,14,18,21,21,21,25,29,32,36,40,44,46,49,59,66,74,81,91,100,100,100]
for esik in ("450+", "900+", "1300+"):
    kontrol(f"Ahilik eşiği {esik} (s.1)", esik in bolum(1))
kontrol("final unvanları", all(t in bolum(26) for t in ("0–449", "450–899", "900–1299", "1300–1600")))
kontrol("defter: 6 durak + Hülasa 40 + Katla 40 + Karma 160 + 3 × 120 + 300 = 1600", sum(defter[:-1]) == defter[-1] == 1600)

# ---- sayfa göndermeleri
konu = {2: "Dalton", 4: "Rutherford", 5: "Bohr", 6: "spektrum", 9: "3B", 10: "proton", 11: "iyon", 12: "Aufbau",
        13: "Hund", 14: "simetri", 15: "değerlik", 25: "Cevaplar"}
```

Değişmeyenler: dizilim motoru öz denetimleri, 6. durak tablosu (sayfadan okunur), Meclis, Kıssalar, Anahtar merdiveni, Büyük
İmtihan (İ11 şemaları), Üstad, sayfa işaretleri, öğretmen metinleri listesi (Hızlı görev cevapları köşe kartlarında aynı `.ogr`),
Medeniyetimizden (meta `sayfa` alanından), model ve keşif yılları, cami/kilise/manastır sahne adı denetimi.

## 9. Ortak kütüphaneden beklenenler

Taşımada **var görünenler** (TASARIM-SISTEMI §16, okundu): `{{kk}}`, `{{hbi}}`, `{{ok}}`, `{{siklik}}`, Hap Bilgi ailesi ve Bir bakışta,
Kendini dene, Yanlış ↔ Doğrusu, çizgi roman panosu CSS'i (§37–§40); `{{hud|n|kat}}`, `{{alt|n|kat|kose-on|kose-arka}}`, `{{zemin14}}`,
`{{cini14}}`, `{{kose-on}}`, `{{kose-arka|baş|cevap|alt}}`, `{{kikon}}`, `{{robot}}`, `{{kapi}}`, karma sayfa sınıfları (§41); `{{ana}}`,
`{{duz}}`, `{{ub-ikon}}`, `.kart.ub` ailesi, meta `"uc_boyut"` (§42); meta `"palet"`; öğretmen ve fotokopi kuralları (§43–§44);
`kendini_dene_ayni`, `sifreli_kapi_ayni`, `celdirici_ayni`, `robot_ayni`, `katla_ayni`, `uc_boyut_resimleri`; `hno` üç haneli kod.

**Bu pilot için ek beklenenler:**
1. **Üçüncü kat sayfası türü** (uygulamada ünitede `{{katla-cumle}}`, `katla_unite.py`; ortağa taşınması önerilir): Şerit cümle (sol sağa yaslı A'ya,
   orta iki çizgi arasında, sağ B'den), durak etiketi, iki yan çizim (`kk` ya da çekirdek kartı ya da orbital şeması), orta şeritte
   "ÖNCE TAHMİN ET" ve "AÇ VE AÇIKLA" kartları, orta şeritte küçük YANLIŞ mührü, dikişte bölünen "DOĞRU" kurdelesi, `_ogr_grubu`
   ile öğretmen cevabı. Her ünitede yanlış bilinen var: bağı ve tepkimesi olmayan ünitelerin kat sayfası da bu olur. Gelmezse
   ünite `katla_unite.py`'de `u._katla()` parçalarıyla kendi yer tutucusunu yazar.
2. **Köşe kartı sınıfı** `.kart.hizli.kose-kart` (ters cevabın yerine "Kontrol: sağ alt köşeyi katla") ve fotokopi kuralı.
3. **Devam başlığı** `.devam-bas` (iki sayfalık durağın sağ sayfası: rozet + üst etiket + h2). Gelmezse ünitenin `<style>`'ına.
4. **3B motorunda lob:** uygulamada gerekmedi (küre zinciri yeterli göründü); kâğıt denemesinde dikiş izi görülürse `Yapi.elipsoid`.
5. **Akçe toplamı parametreli** (uygulamada ünitenin kendi `akce_rayi`'si): ortak `akce_rayi` (0–1400 sabit) toplamı ve eşikleri `meta.akce_toplam` ve
   `meta.ahilik`'ten alsın; çerçevede "Her yolda en çok 1400 akçe" ve "Kalfa 400, Usta 800, Üstad 1150" metinleri (yerel-cerceve
   `sayfalar.py`) karar sonrası güncellenir.
6. `kose-arka` cevap satırında ölçülü yazım (`^{}` `_{}`) ve sığma uyarısı (büyük satır ≤ 36 mm, alt satır ≤ 30 mm).
7. render.js taşma denetimi `.kose-kart` ve `.devam-bas` kutularını da ölçsün.
8. Çerçeve (sonra): gözlük şablonu kitap ekine; içindekilerde 3B ve katla sayfalarına küçük ikon; rotalar.json 26 sayfa.

## 10. Açık kararlar ve riskler

1. **Akçe toplamı.** Öneri 1600 (kat + karma her ünitede standart olacak; 3B bonus). Seçenek B: toplam 1400 kalır, kat ve karma
   da bonus olur (s.17–18'den çipler kalkar; final, s.1, HUD değişmez). Karar ana oturumun.
2. **3B iki sayfa oldu.** Koordinatör "1 adet 3B sayfası" dedi. 25 içerik sayfası tek sayı; çift olması için bir sayfa
   gerekiyordu, kullanıcının "3B'nin oranı fazla olsun" isteğine en uygun aday bu. Tek sayfa istenirse s.8 orbitaller + alfa
   birlikte, s.9 yerine sade bir "Yol defteri" sayfası (zayıf seçenek).
3. Model Zinciri, çizgi roman ve enerji merdiveni eski üç çizimin yerini alıyor. Bilgi aynı; dogrula'daki yıl denetimi için
   çizgi roman başlığında "1909–1911" korunuyor.
4. 4 Tuzak kutusu "Tuzak!" ikili kartına, 2'si Dikkat!'e dönüşüyor; Tuzak'ın +10 akçesi Kendini dene'ye geçiyor.
5. **PROTON** şifresi katla örneğindeki (Yol 6 karma sayfası) şifreyle aynı. 9/06 kurulurken orada başka kelime seçilmeli.
6. Kat cümlelerinin genişlikleri tahmin; gerçek ölçü fontTools ile. Sayfa yerleşimleri `olc.sh` ile denenecek. Sığmazsa çıkarma sırası §2'de.
7. Köşe hizası, kat hizası ve 3B derinliği **kâğıtta denenmedi**; deneme baskısı gerekir. Köşe sineması (`{{film-kose}}`) bu üniteye
   konmadı (7 sağ sayfa köşeli; kitap düzeyinde karar).
8. "Sık sorulur" ve TYT/AYT etiketleri genel öğretmen bilgisi; istenirse etiketsiz yazılır.

## 11. "uygula" gelince sıra

1. Ortak kütüphanenin son hâlini oku (§16.4–§16.8, `cizim/katla.py`, `kur_ortak.py` yer tutucuları); ad farkı varsa bu planı düzelt.
2. meta.json (§7.1) → kur.py (§7.2) → `infografik_unite.py` ve `sahneler_unite.py` (§7.3–7.4) → `sablon.html` 26 bölüm (§2–§6;
   ünite `<style>`'ına Model Zinciri ve enerji merdiveni CSS'i).
3. `python3 uretec/kur.py` (3B resimleri ilk kurulumda çizilir) → `python3 uretec/dogrula.py` → `bash uretec/olc.sh`
   → `node ../../yerel-ortak/render.js . --hepsi --onizleme` → her PDF'te `pdffonts … | grep -c "Type 3"` = 0.
4. Görsel kontrolü bir ajana yaptır (en çok 15 satır rapor): taşma, köşe boşlukları, kat şeridi hizası, 3B kartlarının beyaz zemini.
5. README.md (sayfa planı, cevap anahtarı, akçe) güncellenir. Commit ana oturumun.
