# 9. sınıf · Atom ve Yapısı · "Şanlıurfa–Harran Yolu" (yerel tasarım · Yol 3 · yeni düzen pilotu)

Tema 1 · Bölüm 3. **26 sayfalık**, A4, baskıya hazır ünite; yeni düzenin (katla, köşeyi katla, 3B, Hap Bilgi ailesi, konu
karakterleri, "Çini ve Toprak" paleti) ilk ünitesi. Plan ve gerekçeler: `PILOT-PLAN.md`. Rota Mezopotamya'nın altın ışığında
geçer: Göbeklitepe (şafak) → Harran kümbet evleri (öğle) → Harran Höyüğü (alacakaranlık) → Urfa çarşısı → Halfeti → Fırat
kıyısı; yan yollar Gümrük Hanı (Hülasa), sıra gecesi (Meclis), Harran Ovası (Kıssa), Urfa evleri (Anahtar merdiveni); Büyük
İmtihan Urfa Kalesi'nde. Bütün çizimler koddan üretilir: ortak kütüphane `kitap/yerel-ortak/` + bu ünitenin `uretec/` modülleri.
Klasik kaynak: `kitap/9-sinif/03-atom-ve-yapisi/kaynak.html` (içerik yeni bağlamda yeniden yazıldı; Cr/Cu istisnaları korunur).

## Komutlar

```sh
cd kitap/9-sinif-yerel/03-atom-ve-yapisi
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh   # unite.html → PDF + onizleme/s01…s26 + taşma özeti
node ../../yerel-ortak/render.js . --hepsi --onizleme                      # beş PDF (öğrenci, öğretmen, fotokopi, baskı, hazine)
python3 uretec/kur.py --3b                                                 # 3B resimlerini (gorsel/) baştan çizer
```

`dogrula.py` 324 denetim yapar ve `SONUÇ: hepsi doğru` ile biter. İçinde küçük bir **dizilim motoru** vardır (Aufbau sırası,
Cr/Cu istisnaları, katyonda önce en dış katman, Hund ile yarı dolu sayısı, küresel simetri, değerlik, enerji düzeyi sayısı).
Eski denetimlerin hepsi durur (p/n/e, izo ilişkileri, orbital şemaları, 6. durak tablosu, Rydberg çizgileri, enerji düzeyleri,
tek doğru şık, meclis, anahtar, öğretmen metinleri, Medeniyetimizden yılları, A–E dağılımı). Yeni düzen denetimleri:
26 sayfa ve katlama çiftleri (köşe ön yüzü tek sayfada, cevabı hemen sonraki çift sayfanın sol alt köşesinde; kat sayfası s.17,
karma s.18), 7 köşe cevabı (hesap = kartın öğretmen cevabı = arka yüz; cevap üçgene sığıyor), 7 Kendini dene (hesap ve sayfadaki
`.ogr`), durak başına 1 Bir bakışta + 1 Kendini dene + 1 köşe + en az 3 Hap Bilgi, sayfa başına en çok 4 Hap Bilgi (aynı türden ≤ 2),
kat cümleleri (açık hâli yanlış, katlı hâli doğru, genişlikler kat çizgilerinin 1,2 mm içinde), Şifreli Kapı (PROTON; okunabilir
25 dizinin hepsi PRO?O?), Çeldirici Röntgeni (her şık tanıdaki hatadan), Robot (tek hata, Rydberg ile), Heybe (9/01 ve 9/02
hazine kartlarıyla), 3B (8 resim, ayrıklık ≤ 3 mm, mm = piksel / 300 dpi), akçe 1600 ve HUD çubukları sayfa sayfa.

## Klasör

```
03-atom-ve-yapisi/
  README.md · PILOT-PLAN.md      bu dosya · yeni düzenin planı
  unite.html                    ÜRETİLİR (elle düzenleme) · unite-fotokopi.html, hazine-kartlari.html de
  03-atom-ve-yapisi.pdf         ÜRETİLİR · öğrenci (≈ 8,8 MB) · -ogretmen / -fotokopi / -baski / -hazine-kartlari .pdf
  onizleme/s01…s26.png          ÜRETİLİR (+ varyant/)
  gorsel/                       ÜRETİLİR (git'e girer) · 3B: ana-*.png, duz-*.png, duz-*-b.png, uc-boyut.json
  uretec/
    sablon.html                 26 sayfanın içeriği + üniteye özel CSS (<style> başta; Model Zinciri, enerji merdiveni, devam başlığı)
    meta.json                   6 durak (sayfa + sayfalar), kale, 8 nişan, H1–H12, medeniyet, kavramlar, hud, palet, akce_toplam, uc_boyut
    kur.py                      SAYFA (26), SIMDI, panorama etiketleri, final, mühür; {{orb}} {{iz}} {{rozet-tik}} {{rozet-yildiz}} {{katla-cumle}}
    sahneler_unite.py           15 sahne + NISAN_IKON + bölge parçaları
    infografik_unite.py         eski çizimler + akce_rayi (1600) + aşağıdaki modüllerin çizimleri ({{info|ad}} burada aranır)
    model_ciz.py                atom-modelleri örneğinden: zincir_yolu, pano_duzenek…pano_sonuc, enerji_merdiveni, mini_yorunge,
                                mini_bulut · yeni: tekne_iskelesi (Halfeti teknesi), dis_katman (dış katman konuşuyor)
    uc_unite.py                 3B kurucuları: orbital_s, orbital_p(x|y|z), orbital_p_uc, alfa_levha, alfa_tanecik, atom_bosluk
    katla_unite.py              kat sayfası "Katla, doğrusu kalsın!" (KATLA_CUMLE; ortak cizim/katla.py parçalarıyla)
    dogrula.py                  doğrulama (dizilim motoru dahil)
    olc.sh                      taşma özeti
```

Üniteye özel yer tutucular: `{{orb|ud,u,0}}` orbital kutuları (ok çizgi, fonta bağlı değil) · `{{iz|35|17|Cl|−}}` çekirdek gösterimi ·
`{{rozet-tik}}`, `{{rozet-yildiz|keh}}` yazısız rozet · `{{katla-cumle}}` kat sayfası. Ortak yeni bileşenler: `TASARIM-SISTEMI.md` §16.

## Sayfa planı (L sol · R sağ; ünite kitapta tek sayfada başlar)

| s. | | Yer | İçerik | Köşe / katlama |
|---|---|---|---|---|
| 1 | R | Yola çıkış | başlık, Pamuk, panorama (11 etiket), 8 nişan, yol arkadaşları, hedefler, Ahilik 450/900/1300, 8 işaret | – |
| 2 | L | 1. durak · Göbeklitepe | bant, sohbet + Kavram, **Model Zinciri** (6 model karakteri), Görev 1, Sınav radarı | – |
| 3 | R | 1. durak · devam | Tuzak! ikili + H1–H2, Hap Bilgi ×3, İbn Heysem, Kendini dene, Bir bakışta | köşe: Thomson'da kaç öğe? |
| 4 | L | 2. durak · Harran | bant, sohbet şeridi, **çizgi roman** (6 pano, Pamuk anlatıyor), Görev 2 | köşe cevabı 1 |
| 5 | R | 2. durak · devam | Kavram + Kümbet ve Bohr, Altın Kural · Dikkat! · Hap bilgi, Tuzak! ikili + H3–H4, Sâbit bin Kurra, KD, BB | köşe: L katmanı |
| 6 | L | 3. durak · Harran Höyüğü | bant, sohbet + Kavram, **enerji merdiveni** (foton karakterleri), Görev 3 | köşe cevabı 2 |
| 7 | R | 3. durak · devam | orbital biçimleri + H5–H6, Kilit · Dikkat! · Radar · Hap, el-Battânî, KD, BB | köşe: lamba spektrumu |
| 8 | L | 3B · Orbitaller | 5 anaglif kartı (1s/2s, 2pₓ, 2p_y, 2p_z, 2p üçü), Hap bilgi, KD (bonus), Dikkat!, Unutma! | köşe cevabı 3 |
| 9 | R | 3B · Alfa tanecikleri | altın levhanın içi, alfa taneciği, atomun boşluğu; Kilit · Dikkat! · Unutma! | köşe (bonus): 10⁵ kat |
| 10 | L | 4. durak · Urfa çarşısı | bant, sohbet + Kavram (tablo, izo görevi), iyon ve izo çizimleri, Radar + Hap, Görev 4 | köşe cevabı 3B |
| 11 | R | 4. durak · devam | **Çarşıda tanışma** (5 tanecik karakteri) + H7–H8, Altın Kural · Dikkat! · Unutma!, Tuzak! ikili + Yoldan, KD, BB | köşe: X³⁺ |
| 12 | L | 5. durak · Halfeti | bant, sohbet + Kavram, **Halfeti teknesi**, dolma sırası + Görev 5, Soy gaz kısaltması | köşe cevabı 4 |
| 13 | R | 5. durak · devam | H9–H10 + Yoldan, Kilit · Dikkat! · Unutma! · Hap, KD, BB | köşe: P yarı dolu |
| 14 | L | 6. durak · Fırat kıyısı | bant, sohbet + Kavram, beş atom tablosu + istisnalar, Radar (AYT) + Yoldan, Görev 6 | köşe cevabı 5 |
| 15 | R | 6. durak · devam | **Dış katman konuşuyor** + H11–H12, Kilit · Unutma! · Dikkat!, Tuzak! ikili, KD, BB | köşe: Si |
| 16 | L | Hülasa · Gümrük Hanı | 6 özet kart, hazine sandığı, kendime not, muhasebe (+40) | köşe cevabı 6 |
| 17 | R | **Kat sayfası** | Katla, doğrusu kalsın! · 4 yanlış cümle, orta şerit katlanınca doğrusu kalır (+40) | A ve B kat çizgileri |
| 18 | L | **Karma sayfa** | Şifreli Kapı (PROTON), Çeldirici Röntgeni (¹⁹F⁻), Robot yanıldı mı? (H spektrumu), Heybe (+160) | 17'nin arka yüzü |
| 19 | R | Meclis · sıra gecesi | M1–M4, hata avcısının dört sorusu, meclis notu | – |
| 20 | L | Kıssa · Harran Ovası | K1–K4 | – |
| 21 | R | Anahtar · Urfa evleri | 3 problem × 3 basamak | – |
| 22–23 | L R | Urfa Kalesi | Büyük İmtihan 1–12 | – |
| 24 | L | Üstad (bonus) | 6 AYT tarzı soru, Üstad Mührü | – |
| 25 | R | Cevaplar | durak etiketli anahtar, çözümler, hızlı anahtar, tekrar rotası | – |
| 26 | L | Final | bayraklı Pamuk + 8 nişan, akçe rayı (0–1600), unvanlar, defter, nişan sayımı | – |

Baskı: çift taraflı, **uzun kenardan çevirme**. Köşesi katlanan sayfalar 3 5 7 9 11 13 15, kat sayfası 17; kitapta da tek numaralı
olmalı (ünite tek sayfada başlar, 26 çift sayfa: sonraki ünite yine tek sayfada başlar).

## Cevap anahtarı

* **Büyük İmtihan:** 1 C · 2 A · 3 D · 4 B · 5 C · 6 D · 7 E · 8 A · 9 B · 10 E · 11 D · 12 B (A2 B3 C2 D3 E2)
* **Kıssalar:** 1 D · 2 C · 3 E · 4 B — **Üstad:** 1 C · 2 E · 3 C · 4 B · 5 A · 6 D
* **Meclis:** M1 Yusuf (satır 3) · M2 Elif (2) · M3 Pamuk (2) · M4 Elif (3)
* **Anahtar merdiveni:** A = 34 (³⁴S) · Z = 24 (Cr), değerlik 6 · A = 56, Fe [Ar] 4s² 3d⁶
* **Köşeler (eski hızlı görevler):** 2 · 8 · H ve Na · 13 · 3 · 4 değerlik, 2 yarı dolu · 3B köşesi: ≈ 100 000 kat (10⁵)
* **Kendini dene:** KD1 her yere dağılmış · modern model — KD2 atomun büyük kısmı boşluk · (+) çekirdek — KD3 yayar (486 nm) ·
  6’dan 2’ye (410 nm) — KD4 10 · izotop — KD5 [Ne] 3s² 3p⁵ · hayır (Pauli) — KD6 1 · evet — KD7 (3B) 2p_z · 2
* **Kat sayfası** (katlıyken): Dalton modelinde atom içi dolu bir küredir · Alfaların çoğu sapmadan geçti · İzotoplarda proton
  sayısı aynıdır · Ca²⁺ olurken elektronlar 4s’den verilir
* **Karma:** Kapı P R O T O N · Röntgen C (9, 10, 10) · Robot 3. cümle · Heybe: asit suya · bazik · 2 · 18
* **Kavram ve görevler:** deney · K 2, L 8, M 1 · 10 · a izoelektronik, b izobar, c izoton, d izotop · Al [Ne] 3s² 3p¹,
  Ti [Ar] 4s² 3d² · Cl yok, Cl⁻ var · G1 Dalton'da yük ve izotop yok · G2 boşluk + küçük yoğun (+) çekirdek · G3 9 orbital,
  18 e⁻ · G4 p 29, n 34, e 27 · G5 S [Ne] 3s² 3p⁴, K [Ar] 4s¹ · G6 Ca²⁺ 1s² 2s² 2p⁶ 3s² 3p⁶

## Akçe (yeni düzen: 1600)

Duraklar 100 + 120 × 5 = 700 · Hülasa 40 · **Katla 4 × 10 = 40** · **Karma 160** (Kapı 60, Röntgen 30, Robot 30, Heybe 40) · Meclis
4 × 30 · Kıssa 4 × 30 · Anahtar 3 × 40 · İmtihan 12 × 25 = 300 → **1600**. 120'lik duraklarda: kavram görevi +30, görev +30, köşe
(eski hızlı görev) +30, Kendini dene +10 (eski Tuzak'ın +10'u), iki hazine kartı +20. Tuzak ve Hap Bilgi kutuları akçe taşımaz.
3B sayfaları ve Üstad bonus (akçesiz). Ahilik: Çırak 0+, Kalfa 450+, Usta 900+, Atom Üstadı 1300+ (eski oranlara yakın).
Final rayı ünitenin `infografik_unite.akce_rayi`'sidir (ortaktaki 0–1400 sabit). **Kitap çerçevesi** (rehber: "Her yolda en çok
1400 akçe", nişan albümü) karar kesinleşince güncellenmeli.

## Bölge ve bilim tarihi bilgileri

| Bilgi | Yer | Güven |
|---|---|---|
| Göbeklitepe ≈ 12 bin yıllık, T biçimli dikilitaşlar daire biçiminde | s.2 | yüksek |
| Harran'ın kerpiç, kovan (konik kubbeli) evleri | s.4, s.25 | yüksek |
| Sâbit bin Kurra (836–901) Harran doğumlu; Bağdat'ta Öklid ve Batlamyus çevirilerini düzeltti | s.5 | yüksek (TDV: doğum 221/836 Harran; Britannica: ölüm 901 Bağdat) |
| el-Battânî (y. 858–929) Harran doğumlu, gözlemleri çoğunlukla Rakka'da; güneş yılı 365 g 5 sa 46 dk 24 sn | s.7 | yüksek |
| İbn Heysem (y. 965–1040), Kitâbü'l-Menâzır; görme ışıkla, deneyle sınama | s.3 | yüksek (zaman şeridiyle aynı) |
| Birecik Barajı'nın suları 2000'de eski Halfeti'nin bir bölümünü kapladı; yeni yerleşim ≈ 15 km ötede | s.13 | orta-yüksek (oran verilmedi) |
| Urfa bakırcılar çarşısı, isot, sıra geceleri | s.10–11, s.19 | yüksek (genel bilgi) |
| Atom tarihi: Demokritos MÖ y. 400, Dalton 1803–08, Thomson 1897/1904, Geiger–Marsden 1909, Rutherford 1911, Bohr 1913, proton 1919, nötron 1932, modern model 1920'ler (de Broglie 1924, Schrödinger 1926) | s.2–5 | yüksek |
| H çizgileri 410/434/486/656 nm (Rydberg ile denetlendi), Na 589, Li 610/671 nm; Eₙ = −13,6/n² eV (12,09 = 1,89 + 10,20 eV) | s.6–7, s.18, s.24 | yüksek |
| Elektron, alfa taneciğinden ≈ 7300 kat hafif (hesap 7294) | s.5 | yüksek |
| Atom çapı ≈ 10⁻¹⁰ m, çekirdek ≈ 10⁻¹⁵ m (≈ 10⁵ kat); kütlenin %99,9'dan fazlası çekirdekte | s.9, s.11 | yüksek (büyüklük sırası) |
| Birçok diş macununda florür iyonu bulunur | s.18 | yüksek (genel bilgi) |
| ¹⁴C yarılanma ≈ 5730 yıl; Co-60, Tc-99m, I-131 kullanımları; alev renkleri Na sarı, Sr kırmızı, Cu yeşilimsi mavi | s.20 | yüksek |
| "Çekirdek nohut, atom stadyum"; Rutherford'un "top mermisi" sözü (yaygın alıntının Türkçe kısaltması) | s.4–5 | benzetme / alıntı |

Yerler temsilîdir: yapıların bugünkü hâli (2023 depremleri sonrası) anlatılmaz; Balıklıgöl ve cami/kilise çizilmez, durak
yapılmaz. Halfeti teknesinde yalnız su ve tekne var (Rumkale ve su içindeki minare çizilmedi). 3B resimleri ölçekli değildir
(sayfada yazılı).

## Yerel düzeltmeler ve notlar

* Ünitenin kendi SVG yazılarında `font-family` artık tırnaklı (`'Baloo Bhaijaan 2'`); eski `_rozet_duzelt` kaldırıldı
  (ortak `hno` üç haneli kodu kendisi küçültüyor).
* Büyük harfli etiketlerde formül `.kf` ile korunur (₁₂Mg, 2pₓ, 1s).
* Köşe cevaplarında ölçülü yazım tek karakterli: `8 e^−`, `3s^2` (yer tutucu `{…}` içeremez).
* Fiziksel renkler `data-tema-sabit`: lamba spektrumu, spektrum, enerji merdiveni fotonları, mini çizimler.
* Cevaplar ve final levhasında ✓ ve ★ yerine çizgi rozet (Baloo'da bu glifler yok). `.mini-gorev` büyük harfe çevrilmez.
* HUD başlığı `meta.hud = "Urfa–Harran"`; 3. durakta HUD yeri "Höyük".
* Fiziksel deneme baskısı gerekir: köşe ve kat hizası (±1 mm), 3B derinliği ve hayalet görüntü.
