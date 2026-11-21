# Kimya Rotası · Proje durumu ve devam notu

Bu dosya, yeni bir oturumun konuşma geçmişini okumadan kaldığı yerden devam edebilmesi için yazıldı.
Yeni oturumda ilk iş bu dosyayı oku, sonra kullanıcıya kısa bir durum özeti ver ve kararını sor.

## 1. Proje ve kullanıcı
- Van'da kimya öğretmeni. Özgün, yeni nesil bir lise kimya ders kitabı: 9. sınıf 10 ünite, 10. sınıf 6 ünite.
  Kaynak yayınevi modülleri yalnız konu kapsamı için kullanılır; hiçbir şey kopyalanmaz.
- Çıktı: baskıya hazır PDF (HTML/CSS → Playwright Chromium).
- **Kullanıcı tercihleri**
  - Türkçe yaz.
  - PDF'leri ve PNG önizlemeleri sohbete doğrudan gönder (SendUserFile, render).
  - Görseller doygun ve zengin olsun; "sınırları zorla".
  - Şimdilik yalnız ders kitabı. Etkileşimli web sayfası, test üretici ve öğretmen kılavuzu sonraya bırakıldı.
  - Büyük bir işe kullanıcının onayı olmadan başlama. Kullanıcının sözü: "Taslağı bitirmeden hiçbir şey yapma".
  - Kullanıcı bağlam (context) kullanımından şikâyet etti, idareli çalış. Ayrıntı için bkz. §8.
- **Git**
  - Yalnız `claude/max-file-upload-limit-62wc8f` dalına commit ve push yapılır. PR açılmaz.
  - Commit mesajının sonuna oturumun verdiği Co-Authored-By ve Claude-Session satırları eklenir.
  - Model adı başka hiçbir yere yazılmaz.
  - Kullanıcının e-postası gizlidir.
- **Kullanım sınırları:** 5 saatlik ve haftalık sınırlar sık doluyor. Aynı anda en çok 2–3 ajan çalıştır. Sınır dolarsa ajanı SendMessage ile sürdür.

## 2. Klasör haritası (`kitap/`)
| Yol | Ne |
|---|---|
| `9-sinif/`, `10-sinif/` | **Klasik tasarım**, 16 ünitenin hepsi tamam (kaynak.html, derle.py). Birleşik kitaplar: `kimya-rotasi-9-sinif.pdf`, `kimya-rotasi-10-sinif.pdf` |
| `yerel-ortak/` | **Yeni (yerel) tasarımın ortak kütüphanesi**: `kur_ortak.py`, `stil.css`, `render.js`, `cizim/` (sahne, karakter, molekül, süs, infografik), `dogrula_ortak.py`, `yeni_unite.py`, `fotokopi.py`, `TASARIM-SISTEMI.md` (ana belge), `ROTALAR.md` (16 rota) |
| `9-sinif-yerel/`, `10-sinif-yerel/` | Yeni tasarımdaki üniteler (her birinde `uretec/`: sablon.html, meta.json, kur.py, sahneler_unite.py, dogrula.py) |
| `yerel-cerceve/` | Kitap çerçevesi: kapaklar, rehber, Türkiye rota haritası ve içindekiler, Medeniyetimizden zaman şeridi, periyodik tablo, sözlük, nişan albümü. `kitap_yerel.js` birleşik kitabı kurar. `rotalar.json` |
| `gelistirme/` | Onay bekleyen yeni özellik örnekleri (§4) |
| `YEREL-KIMLIK.md`, `YAZIM-REHBERI.md` | Dil, karakterler, örnek havuzu; doğruluk kuralları ve mol kütleleri |
| `fontlar/` | OFL yazı tipleri. Değişken fontların `static/` kopyaları var (Type 3 olmaması için) |

## 3. Yeni tasarımdaki ünitelerin durumu
Her ünite 15–16 sayfadır: açılış haritası, 4–6 durak, Hülasa, Meclis, Kıssa, Anahtar merdiveni, Büyük İmtihan (2 sayfa), Üstad, Cevaplar, Final.

| Ünite | Rota | Durum |
|---|---|---|
| 10/01 Kimyasal Değişimler | Kars–Erzurum | ✅ tamam, incelendi |
| 10/02 Mol Kavramı | Van Gölü Turu | ✅ tamam (prototip) |
| 10/03 Stokiyometri | Dicle Yolu | ✅ tamam |
| 10/04 Gazlar | Kapadokya | ✅ tamam |
| 10/05 Çözeltiler 1 | Pamukkale–Afyon | ✅ tamam |
| 10/06 Çözeltiler 2 | Göller Yolu | ✅ tamam |
| 9/01 Günlük Hayatta Kimya | İznik–Bursa | ⚠️ bitmek üzere. PDF ve dogrula.py geçiyor, ama **son sayfa incelemesi yapılmadı** |
| 9/02 Kimyasal Güvenlik | Batı Karadeniz | ⚠️ aynı durum (dogrula 230 denetim geçiyor). Madencilik saygıyla işlenmeli, kaza anılmamalı |
| 9/03 Atom ve Yapısı | Şanlıurfa–Harran | ✅ tamam (6 durak) |
| 9/04 Periyodik Tablo | Maden Yolu I | ✅ tamam. Durak sırası: Seydişehir → Kütahya → Gümüşköy → Kırka → Bandırma |
| 9/05 Periyodik Özellikler | Maden Yolu II | ✅ tamam (6 durak, Keban Baraj Gölü eklendi) |
| 9/06 Kimyasal Etkileşimler | Tuz Gölü–Aksaray | ❌ başlanmadı. Ihlara ve Güzelyurt'u Gazlar kullandı, kullanma |
| 9/07 Adlandırma | İstanbul | ❌ başlanmadı. Cami sahne olmaz; adlandırma kuralları klasik üniteyle birebir |
| 9/08 Moleküller Arası | Doğu Karadeniz | ❌ başlanmadı. Rize, çay ve Anzer 9/10'a ait |
| 9/09 Katılar | Mardin–Midyat | ❌ başlanmadı |
| 9/10 Sıvılar | Rize–Kaçkar | ❌ başlanmadı |

- **10. sınıf birleşik kitap:** bir kez denendi (114 sayfa, ~52 MB). Ara sürüm git'e girmez: `kitap/kimya-rotasi-*-yerel*.pdf` commit edilmez. GitHub'da dosya sınırı 100 MB.
- **9. sınıf birleşik kitap:** üniteler bitince kurulur. Sınırı aşarsa iki cilde bölünür.

## 4. Kullanıcının beğendiği, yaygınlaştırma onayı bekleyen özellikler (`gelistirme/`)
| Klasör | İçerik |
|---|---|
| `atom-modelleri/` | Kişileştirilmiş atom modelleri, Rutherford çizgi romanı, Bohr enerji merdiveni. **Hap Bilgi ailesi** (`hap_bilgi.py`: Hap Bilgi, Altın Kural, Unutma!, Sınav Radarı, Dikkat!, Kilit Bilgi). **Konu karakterleri** (`konu_karakterleri.py`). 5 renk teması (`tema.py`). Öneriler: Bir bakışta, Kendini dene, Yanlış bilinen ↔ Doğrusu, Tahmin et sonra gözle |
| `karma-temalar/` | **Sınıfa göre karma paletler**: 9. sınıf "Çini ve Toprak", 10. sınıf "Göl ve Rasathane". Gazlar'dan 3 yeni sayfa ve gaz molekülü karakterleri |
| `uc-boyut/` | **3B kırmızı-camgöbeği gözlük** (`uc_boyut.py` anaglif motoru): molekül şekilleri, kristaller, 22,4 L küpü, gözlük şablonu. Kırmızı cam sol göze. En çok 3 mm ayrıklık |
| `katla/` | **Katla, tepkime olsun** (iki tam sayfa), köşeyi katla, karma sayfa (Şifreli Kapı, Çeldirici Röntgeni, Robot yanıldı mı?, Heybe, Nineme Anlat), sayfa köşesi çizgi filmi |

- **Kullanıcının kararı:** "Hepsi çok iyi". Katla ve 3B en sevdikleri; "bunların oranı fazla olsun".
- **Önerilen yaygınlaştırma planı** (kullanıcının "başla" demesi bekleniyor):
  1. Ortak kütüphaneye taşı: hap_bilgi, konu_karakterleri, tema (karma paletler, `--tema` seçeneği), katla_cizim, uc_boyut. Yeni bileşenlerin fotokopi kurallarını ve öğretmen nüshası (`.ogr`) cevaplarını ekle.
  2. Pilot olarak 9/03 Atom ve Yapısı'nı tamamen yeni düzenle yap ve kullanıcıya göster.
  3. Yay: 9/01 ve 9/02'yi bitir; 9/06–9/10'u yeni düzenle yap; biten 11 üniteyi elden geçir. Her ünitede:
     - 1 katla sayfası, her durakta 1 köşeyi katla
     - uygun ünitelerde 1 adet 3B sayfası
     - Hap Bilgi kutuları, Bir bakışta, Kendini dene
     - Şifreli Kapı, Çeldirici Röntgeni, Robot yanıldı mı?, Heybe
     - konu karakterleri ve 1 çizgi roman şeridi
  4. Çerçeve düzeltmeleri, ardından iki birleşik kitap ve sürümleri (öğretmen, fotokopi, baskı).
- **Fiziksel deneme baskısı gerekiyor:** 3B derinliğinin rahatlığı ve gölgelenme; katlamada yaklaşık 1 mm tolerans; köşe cevabının denk gelmesi; çizgi filminin akıcılığı. Kullanıcıdan geri bildirim istendi.

## 5. Kullanıcıya önerilen, seçim bekleyen yeni fikirler
- **En son önerdiklerim:**
  - Usturlap Çarkı (element çarkı ve mol hesap çarkı)
  - Gizli cevap (kırmızı camdan bakınca beliren)
  - Kâğıtta animasyon (asetatla kayan perde)
  - Kâğıttan molekül modelleri
  - Yük yapbozu
  - Ustanın Sırrı (zanaatın kimyası: çini, ebru, kök boya, kalaycılık)
  - Kimya İcazetnamesi
  - Element Ligi kartları
  - Defter kenarı notları
  - Yanlış Sayfa
  - Gerçek boyut sayfası
  - Renkli kenar şeritleri
  - Kolay okunur baskı
  - Heybe zarfı
  - Matbaa imkânı varsa: termokromik, fosforlu ve kokulu mürekkep
- **Önerim:** Usturlap Çarkı, Gizli cevap, Kâğıtta animasyon ve Ustanın Sırrı için birer sayfalık örnek.
- **Daha önce önerilip henüz seçilmeyenler:** Işığa tut, Cep Hülasası, Kitap boyu sır, Kervan Oyunu, Kelimenin Yolculuğu, Etiket Dedektifi.

## 6. Bekleyen eski kararlar
- Kitap adı ("Kimya Rotası" geçici) ve yazar adı.
- Elektronegatiflik: yeni tasarımda Pauling ölçeği kullanılıyor (F 4,0; Cl 3,2; O 3,4). Kullanıcı onaylamadı.
- d-blok değerlik sayımı, lantanit yerleşimi (IUPAC kullanıldı), Roma rakamı boşluğu ("demir(III)" mü "demir (III)" mü).

## 7. Bilinen sorunlar ve yapılacak düzeltmeler
- **Ortak kod hatası:** `yerel-ortak/cizim` içinde 15 yerde SVG'de `font-family="Baloo Bhaijaan 2"` tırnaksız yazılmış. Bu geçersiz CSS; Chrome Nunito'ya düşüyor.
  - Düzeltme: `font-family="'Baloo Bhaijaan 2'"`.
  - Düzeltince SVG başlıklarının ölçüsü değişir. Bütün üniteleri yeniden kur ve kontrol et.
- **rotalar.json:** ünitelerin meta.json'larından güncellenmeli (9/03 ve 9/05 altı durak oldu, 9/04'ün sırası değişti). Ardından albüm, harita ve sözlük yeniden kurulmalı.
- **Çerçeve:**
  - Fotokopi kitabında rota renkleri griye dönmüyor.
  - Hazine kartları ekinde sayfa numarası yok.
  - Bazı sayfaların altında boşluk var.
  - Zaman şeridine Sâbit bin Kurra ve el-Battânî eklenmeli (9/03 meta.json'da hazır).
  - Sözlük tanımları gözden geçirilmeli.
- **Ünite ajanlarının ortak kütüphane önerileri:**
  - Mühür alt yazısı `meta.rota`'dan gelsin.
  - Final sahnesi için kanca eklensin.
  - Hazine rozeti 3 karakterli kodlar (H10–H12) için küçülsün.
  - Hazine yaprağında kısa rota adı kullanılsın.
  - `hud_rota` özel adların harf durumunu bozmasın.
  - `sik_harfleri` regex'i `.tam` sınıfını kabul etsin.
  - `ustad-sekil` genişliği düzeltilsin.
  - `nisan-sayim` 8 nişanda 4×2 dizilsin.
  - `_alt()` tspan yardımcısı ortaklaşsın (Nunito'da → ↓ ↑ δ α yok; Baloo'da δ Δ Σ ↔ ✓ ★ yok).
  - Glif denetimi ve fotokopide tarama desenleri eklensin.
  - Rota etiketleri için çakışma çözücü eklensin.
  - Yeni moleküller: H₂, C₄H₁₀ ve iyonlar.

## 8. Çalışma yöntemi ve bağlam tasarrufu
- **Komutlar**
  - Yeni ünite: `python3 kitap/yerel-ortak/yeni_unite.py <9-sinif-yerel|10-sinif-yerel> <NN-klasor> --yol N --rota "…" --unite "…" --tema "…" --durak 4|5|6 --kale "…" --merkez enlem,boylam`
  - Kur ve denetle: `cd <ünite> && python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh` → "SONUÇ: hepsi doğru", taşma yok.
  - Sürümler: `node kitap/yerel-ortak/render.js <ünite> --hepsi [--onizleme]` → öğrenci, öğretmen, fotokopi, baskı ve hazine kartları.
  - Birleşik kitap: `python3 kitap/yerel-cerceve/uretec/kur.py <9|10> && node kitap/yerel-cerceve/kitap_yerel.js <9|10> [--varyantlar]`
  - Her PDF'te `pdffonts x.pdf | grep -c "Type 3"` → 0 olmalı.
- **Ünite ajanı görevi**
  - Önce şunları okusun: `TASARIM-SISTEMI.md` (§8–12, §15), `ROTALAR.md`, `YEREL-KIMLIK.md`, `YAZIM-REHBERI.md`, klasik ünite ve biten bir örnek ünite.
  - Bölgedeki bilgileri doğrulasın; uydurma bilgi yazmasın.
  - Cami, kilise ve manastır oyun sahnesi olmaz. Depremde hasar gören yapılar sağlam gösterilmez. Logo kullanılmaz.
  - Konturlu SVG yazısı yerine `halolu_yazi` kullanılır. Kalkan el açık avuçtur. CSS `filter` yasaktır.
  - Ortak dosyalara dokunmasın ve commit yapmasın; bunları ana oturum yapar.
- **Bağlam tasarrufu (ana oturum için)**
  - Görselleri küçük oku: ünite başına bir kontakt sayfası (≤1600 px) ve en çok bir tam sayfa.
  - Büyük dosyaları baştan sona okuma; `grep` ve `sed -n` ile ilgili parçayı oku.
  - Ajan raporlarını kısa iste.
  - Kullanıcıya yazdığın mesajları kısa tut.
  - Ara kayıtları tek komutla al: `git add -A kitap ':!kitap/kimya-rotasi-*-yerel*.pdf'`, ardından commit ve push.
