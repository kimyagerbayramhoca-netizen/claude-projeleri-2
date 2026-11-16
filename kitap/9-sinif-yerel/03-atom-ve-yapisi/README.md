# 9. sınıf · Atom ve Yapısı · "Şanlıurfa–Harran Yolu" (yerel tasarım · Yol 3)

Tema 1 · Bölüm 3. 16 sayfalık, A4, baskıya hazır ünite. Rota Mezopotamya'nın altın ışığında geçer: Göbeklitepe (şafak) →
Harran kümbet evleri (öğle) → Harran Höyüğü (alacakaranlık) → Urfa çarşısı → Halfeti → Fırat kıyısı; yan yollar Gümrük Hanı
(Hülasa), sıra gecesi (Meclis), Harran Ovası (Kıssa), Urfa evleri (Anahtar merdiveni); Büyük İmtihan Urfa Kalesi'nde.
Bütün çizimler koddan üretilir: ortak kütüphane `kitap/yerel-ortak/cizim/` + bu ünitenin `uretec/` modülleri.
Klasik kaynak: `kitap/9-sinif/03-atom-ve-yapisi/kaynak.html` (içerik yeni bağlamda yeniden yazıldı; Cr/Cu istisnaları korunur).

## Komutlar

```sh
cd kitap/9-sinif-yerel/03-atom-ve-yapisi
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh   # unite.html → PDF + onizleme/s01…s16.png + taşma özeti
node ../../yerel-ortak/render.js . --hepsi --onizleme                      # beş PDF + varyant önizlemeleri
node ../../yerel-ortak/render.js . 3 4 --pdfsiz                            # yalnız 3. ve 4. sayfanın PNG'si
```

`dogrula.py` 195 denetim yapar ve `SONUÇ: hepsi doğru` ile biter. İçinde küçük bir **dizilim motoru** vardır (Aufbau sırası,
Cr/Cu istisnaları, katyonda önce en dış katman, Hund ile yarı dolu sayısı, küresel simetri, değerlik, enerji düzeyi sayısı).
Denetlenenler: her p/n/e sayısı, izotop/izoton/izobar/izoelektronik ilişkisi, sayfadaki orbital şemaları (`data-orb`, Hund),
6. durak tablosu (sayfadan okunur), hidrojen çizgileri (Rydberg → 410/434/486/656 nm) ve lamba spektrumu, enerji düzeyleri
(−13,6/n² eV), her soruda tek doğru şık, `data-dogru` işaretleri, meclis hükümleri, anahtar ızgarası ve durak etiketleri,
çözüm harfleri, hızlı anahtar, öğretmen (`.ogr`) metinleri ve NEDEN çizgisi ≤ 14 harf, akçe (100 + 5 × 120, yan yollar
3 × 120, imtihan 300, Hülasa 40 → 1400), HUD çubukları, Ahilik eşikleri, final defteri, `s.{{sayfa|n}}` göndermeleri,
Medeniyetimizden yılları (meta ↔ sayfa), İmtihanda A–E dağılımı.

## Klasör

```
03-atom-ve-yapisi/
  README.md                     bu dosya
  unite.html                    ÜRETİLİR (elle düzenleme)
  03-atom-ve-yapisi.pdf         ÜRETİLİR · öğrenci (≈ 6,6 MB) · -ogretmen / -fotokopi / -baski / -hazine-kartlari .pdf
  onizleme/s01…s16.png          ÜRETİLİR (+ varyant/ogretmen, fotokopi, baski)
  uretec/
    sablon.html                 16 sayfanın içeriği + üniteye özel küçük CSS (<style> başta)
    meta.json                   6 durak, kale, 8 nişan (Üstad Mührü bonus), H1–H12, medeniyet (sira/takma/kaynak), kavramlar, hud
    kur.py                      SAYFA, SIMDI, panorama etiketleri, final, mühür; {{orb}} {{iz}} {{rozet-tik}} {{rozet-yildiz}}
    sahneler_unite.py           15 sahne + NISAN_IKON (dikilitas kumbet yildiz sarraf orbital halka) + bölge parçaları
    infografik_unite.py         model_yolculugu, altin_levha, bohr_kumbet, spektrum, lamba_spektrumu, orbital_sekilleri,
                                iyon_olusumu, izo_kutulari, aufbau, kissa_grafik, ustad_enerji
    dogrula.py                  doğrulama (dizilim motoru dahil)
    olc.sh                      taşma özeti
```

Üniteye özel yer tutucular: `{{orb|ud,u,0}}` orbital kutuları (ok gövdesi ve ucu çizgi: fonttaki ↑↓'ya bağlı değil, fotokopide
koyu kalır) · `{{iz|35|17|Cl|−}}` çekirdek gösterimi (ortak `.izo` sınıfı) · `{{rozet-tik}}`, `{{rozet-yildiz|keh}}` yazısız rozet.

## Sayfa planı

| s. | Yer | İçerik | Sahne / grafik |
|---|---|---|---|
| 1 | Yola çıkış | başlık, Pamuk, stilize Şanlıurfa haritası (11 etiket), 8 nişan, yol arkadaşları, hedefler, Ahilik | `panorama_urfa` |
| 2 | 1. durak · Göbeklitepe | teori/model, Dalton, Thomson, beş model zaman şeridi, Görev 1, H1–H2, Tuzak, Hızlı, **İbn Heysem** | `gobeklitepe`; `model_yolculugu` |
| 3 | 2. durak · Harran | Rutherford, Bohr, modern bulut, altın levha, kümbet ↔ katmanlar, Görev 2, H3–H4, **Sâbit bin Kurra** | `harran`; `altin_levha`, `bohr_kumbet` |
| 4 | 3. durak · Harran Höyüğü | temel/uyarılmış hâl, çizgi spektrumu, s p d orbitalleri, Görev 3, lamba spektrumu, H5–H6, **el-Battânî** | `harran_hoyuk`; `spektrum`, `orbital_sekilleri`, `lamba_spektrumu` |
| 5 | 4. durak · Urfa çarşısı | p/n/e tablosu, iyon oluşumu, izo kardeşler, Görev 4 (⁶³Cu²⁺), H7–H8, Yoldan (bakırcılar, isot) | `urfa_carsi`; `iyon_olusumu`, `izo_kutulari` |
| 6 | 5. durak · Halfeti | Aufbau, Pauli, Hund, köşegen kural, Görev 5 (S, K), soy gaz kısaltması, H9–H10, Yoldan (Birecik Barajı) | `halfeti`; `aufbau` |
| 7 | 6. durak · Fırat kıyısı | değerlik, küresel simetri, beş atom tablosu, Cr/Cu, Görev 6 (Ca, Ca²⁺), H11–H12 | `firat` |
| 8 | Hülasa · Gümrük Hanı | 6 özet kart, hazine sandığı (12), Muhasebe (+40), tekrar sayfaları | `gumruk_hani` (b40) |
| 9 | Meclis · sıra gecesi | M1–M4, hata avcısının dört sorusu, meclis notu, Yoldan | `sira_gecesi` |
| 10 | Kıssa · Harran Ovası | K1 (nükleer tıp tablosu), K2 (alev testi), K3 (grafik), K4 (¹⁴C) | `harran_ovasi`; `kissa_grafik` |
| 11 | Anahtar · Urfa evleri | 3 problem × 3 basamak | `urfa_evleri`; `merdiven_akce` (ortak) |
| 12–13 | Urfa Kalesi | Büyük İmtihan 1–12 | `urfa_kalesi` (b62), `kale_kapi_urfa` (b30) |
| 14 | Üstad (bonus) | 6 AYT tarzı soru (tablo + enerji şeması), Üstad Mührü | `ustad_bandi` (ortak); `ustad_enerji` |
| 15 | Cevaplar | durak etiketli anahtar, bütün çözümler, hızlı anahtar, puan, tekrar rotası | `harran_gece` (Samanyolu) |
| 16 | Final | Urfa Kalesi burcunda bayraklı Pamuk + 8 nişanlı çelenk, akçe rayı (ATOM ÜSTADI), unvanlar, defter, nişan sayımı | `final_urfa` |

## Cevap anahtarı

* **Büyük İmtihan:** 1 C · 2 A · 3 D · 4 B · 5 C · 6 D · 7 E · 8 A · 9 B · 10 E · 11 D · 12 B (A2 B3 C2 D3 E2)
* **Kıssalar:** 1 D · 2 C · 3 E · 4 B — **Üstad:** 1 C · 2 E · 3 C · 4 B · 5 A · 6 D
* **Meclis:** M1 Yusuf (satır 3) · M2 Elif (2) · M3 Pamuk (2) · M4 Elif (3)
* **Anahtar merdiveni:** A = 34 (³⁴S) · Z = 24 (Cr), değerlik 6 · A = 56, Fe [Ar] 4s² 3d⁶
* **Hızlı görevler:** 2 · 8 · H ve Na · 13 · 3 · 4 değerlik, 2 yarı dolu
* **Kavram ve görevler:** deney · K 2, L 8, M 1 · 10 · a izoelektronik, b izobar, c izoton, d izotop · Al [Ne] 3s² 3p¹,
  Ti [Ar] 4s² 3d² · Cl yok, Cl⁻ var · G1 Dalton'da yük ve izotop yok · G2 boşluk + küçük yoğun (+) çekirdek · G3 9 orbital,
  18 e⁻ · G4 p 29, n 34, e 27 · G5 S [Ne] 3s² 3p⁴, K [Ar] 4s¹ · G6 Ca²⁺ 1s² 2s² 2p⁶ 3s² 3p⁶

## Akçe

Duraklar 100 + 120 × 5 = 700 · Hülasa 40 · Meclis 4 × 30 · Kıssa 4 × 30 · Anahtar 3 × 40 · İmtihan 12 × 25 = 300 → **1400**.
120'lik duraklarda: kavram görevi +30, görev +30, hızlı +30, tuzak +10, iki hazine kartı +20. Ahilik: Çırak 0+, Kalfa 400+,
Usta 800+, Atom Üstadı 1150+. Üstad soruları akçeye eklenmez (Üstad Mührü).

## Bölge ve bilim tarihi bilgileri

| Bilgi | Yer | Güven |
|---|---|---|
| Göbeklitepe ≈ 12 bin yıllık, T biçimli dikilitaşlar daire biçiminde | s.2 | yüksek |
| Harran'ın kerpiç, kovan (konik kubbeli) evleri | s.3, s.15 | yüksek |
| Sâbit bin Kurra (836–901) Harran doğumlu; Bağdat'ta Öklid ve Batlamyus çevirilerini düzeltti | s.3 | yüksek (TDV: doğum 221/836 Harran; Britannica: ölüm 901 Bağdat) |
| el-Battânî (y. 858–929) Harran doğumlu, gözlemleri çoğunlukla Rakka'da; güneş yılı 365 g 5 sa 46 dk 24 sn | s.4 | yüksek |
| İbn Heysem (y. 965–1040), Kitâbü'l-Menâzır; görme ışıkla, deneyle sınama | s.2 | yüksek (zaman şeridiyle aynı) |
| Birecik Barajı'nın suları 2000'de eski Halfeti'nin bir bölümünü kapladı; yeni yerleşim ≈ 15 km ötede | s.6 | orta-yüksek (oran kaynaklara göre değişiyor; oran verilmedi) |
| Urfa bakırcılar çarşısı, isot, sıra geceleri | s.5, s.9 | yüksek (genel bilgi) |
| Atom tarihi: Dalton 1803–08, Thomson 1897/1904, Geiger–Marsden 1909, Rutherford 1911, Bohr 1913, proton 1919, nötron 1932, modern model 1926 sonrası | s.2–5 | yüksek |
| H çizgileri 410/434/486/656 nm (Rydberg ile denetlendi), Na 589, Li 610/671 nm; Eₙ = −13,6/n² eV | s.4, s.14 | yüksek |
| ¹⁴C yarılanma ≈ 5730 yıl; Co-60, Tc-99m, I-131 kullanımları; alev renkleri Na sarı, Sr kırmızı, Cu yeşilimsi mavi | s.10 | yüksek |
| "Çekirdek nohut, atom stadyum" | s.3 | benzetme (oran ≈ 10⁴–10⁵) |

Yerler temsilîdir: yapıların bugünkü hâli (2023 depremleri sonrası) anlatılmaz; Balıklıgöl ve cami/kilise çizilmez, durak yapılmaz.

## Yerel düzeltmeler (ortak kütüphaneye öneri)

* `kur.py · _rozet_duzelt`: hazine rozetinde üç haneli kodlar (H10–H12) daireden taşıyordu → yazı 23.
* Cevaplar ve final levhasında ✓ ve ★ yerine çizgi rozet (Baloo'da bu glifler yok).
* `.mini-gorev`: kavram içi görev satırı büyük harfe çevrilmez (Cl, Na, 3d bozulmasın).
* HUD başlığı `meta.hud = "Urfa–Harran"`; 3. durakta HUD yeri "Höyük" (uzun adlar akçe çubuğunu kesiyordu).
* Panorama stilizedir: şehirdeki duraklar ve Harran/Höyük okunurluk için aralıklı çizildi.
