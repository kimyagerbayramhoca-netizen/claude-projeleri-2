# Kimya Rotası · Harman Tasarım Sistemi

Bu sistem üç konseptin harmanıdır:

- **İskelet: Konsept 1 (Görev Rotası).** Ünite bir "Dünya", konular KN1–KN5 kontrol noktalarıdır. Her sayfanın üstünde bir HUD vardır. Kitapta rota haritası, rozetler, XP, kilitli ipuçları, Tuzak!, Kayıt noktası ve Boss bulunur.
- **Anlatım: Konsept 2 (Sohbet & Akış).** Her konu Ece, Deniz ve Avo'nun mesajlaşmasıyla açılır. Doğruluk kontrolü, kaydet/yetenek kartı, yorumlarda kim haklı, hikâye kartı, anket ve durum güncellemesi bu konseptten gelir.
- **Dokunuş: Konsept 3 (Bento).** Sayfalar bento ızgarasıyla dizilir. Dev sayılar ve numaralı özet kart serisi (01/06…) bu konseptten gelir.
- **Daha cesur:** Çizgiler kalın mürekkeptir (0,55 mm), gölgeler serttir (1,6 mm kaydırılmış). Dev başlıklar Inter Display Black ile yazılır. Zemin açık kalır. Koyu blok için sınır: HUD + sayfa başına en fazla bir koyu blok.

Referans ünite: `10-sinif-yeni/02-mol-kavrami/` (`stil.css`, `unite.html`, `uretec/`).

---

## 1. Dosya düzeni (her ünite)

```
10-sinif-yeni/NN-unite-adi/
  stil.css          ← ortak tasarım sistemi (bu ünitedeki kopya kanonik; diğer ünitelere aynen kopyala)
  unite.html        ← <link rel="stylesheet" href="stil.css">; ünite özel küçük ayarlar <style> içinde
  NN-unite-adi.pdf  ← node uretec/render.js çıktısı
  onizleme/sNN.png  ← her sayfanın PNG'si (deviceScaleFactor 2)
  uretec/render.js  ← PDF + PNG + taşma denetimi (göreli yollar)
  uretec/olc.sh     ← taşma özeti: sayfa başına "alan dışı" en alt kenar (boşsa sığıyor)
  uretec/dogrula.py ← tüm sayısal cevapların ve "tek doğru şık" kuralının python doğrulaması
```

Derleme: `node uretec/render.js` (ya da `uretec/olc.sh 3 4` ile yalnızca 3. ve 4. sayfanın PNG'si). Betik iki tür sorunu raporlar:
- **Alan dışı:** HUD altı (9,4 mm) ile altbilgi üstü (284 mm) arasındaki içerik alanından taşan öğe.
- **Kutu taşması:** kart, balon, şık gibi kutulara sığmayan metin.

Hedef: `alan dışı: yok`.

Kurallar:
- Fontlar yalnızca şunlardır: Inter, Inter Display, JetBrains Mono, Caladea (değişkenler; SVG içinde de `font-family="Caladea"`) ve yedek olarak DejaVu. Harici kaynak kullanılmaz.
- Kimyasal formüllerde `<sub>` kullanılır.
- `.etiket` (mono büyük harf) içinde `<sub>` kullanılabilir. Etiket `inline-block` olduğu için alt simge ayrılmaz.

---

## 2. Renk tokenları (`:root`)

| Token | Değer | Kullanım |
|---|---|---|
| `--kagit` | `#FFFCF2` | sayfa zemini (5 mm nokta deseni ile) |
| `--murekkep` | `#13132B` | çizgi, metin, sert gölge, HUD, tek koyu blok |
| `--soluk` | `#565A7C` | ikincil metin, mono etiketler |
| `--cizgi` | `#D8D3E6` | kesik ayraçlar |
| `--mor` / `-a` / `-k` | `#5A2DFF` / `#ECE6FF` / `#3414C4` | marka, KN, Avo, yetenek, ipucu merdiveni |
| `--lime` / `-a` / `-k` | `#8CD11E` / `#EDF9D4` / `#3D6A00` | XP, ilerleme, "Doğrusu", kayıt noktası |
| `--mercan` / `-a` / `-k` | `#FF4A36` / `#FFE5E0` / `#B31F0E` | Tuzak!, Boss, Ece |
| `--turkuaz` / `-a` / `-k` | `#00A3B4` / `#D8F4F6` / `#006C78` | görev çözüm akışı, Deniz |
| `--sari` / `-a` / `-k` | `#FFC21A` / `#FFF2CC` / `#8F5E00` | ana görev, hızlı görev, yer imi, vurgu |

Ölçüler:
- `--cz` .55 mm (kart çizgisi), `--cz-ince` .35 mm
- `--golge` 1.6 mm, `--golge-k` 1 mm, `--golge-b` 2.4 mm
- `--r` 3.2 mm (köşe)

Tipografi:
- Gövde metni Inter 9.8pt; balon ve kart metni ≥ 9.5pt.
- Dev başlıklar Inter Display 900: KN başlığı 29pt, açılış 52pt, dev sayı 58pt.
- Etiket ve çiplerde JetBrains Mono 7–8pt kullanılır, yalnızca etiket ve çip için.

---

## 3. Bileşenler (sınıf → ne için)

### Sayfa çerçevesi
| Sınıf | Ne için |
|---|---|
| `.sayfa` | 210×297 mm, `overflow:hidden`, içerik alanı 14.5 mm–283 mm |
| `.hud` | Üstteki koyu şerit. İçinde `.logo`, `.yer` (Dünya · **KN n/5**), `.noktalar` ve `.xp` bulunur. `.noktalar` 10 noktadır: KN1–5, Kayıt, Yan1–3, Boss; boss noktası `i.boss` ile elmas biçimindedir. Nokta durumları: `.tam` geçildi, `.simdi` buradasın. `.xp` içinde yazılacak kutu `.yaz` ve sayfa başındaki en çok XP oranını gösteren `.xpbar i` vardır. |
| `.alt` | Altbilgi: ünite adı · sayfa adı · altıgen `.no` (Boss sayfalarında `.no.boss`) |

### Temel parçalar
| Sınıf | Ne için |
|---|---|
| `.kart` | Beyaz kart, kalın çizgi, sert gölge. Çeşitleri: `.duz` (gölgesiz), `.b` (büyük gölge), `.mor-z` / `.lime-z` / `.sari-z` / `.mercan-z` / `.turkuaz-z` (zemin rengi) |
| `.kart-bas` | Kart üst satırı: solda etiket, sağda `.sag` (yıldız + XP çipi) |
| `.etiket` | Mono büyük harf başlık, isteğe bağlı `svg.ikon` |
| `.cip` | Hap. Çeşitleri: `.xp` (lime), `.koyu`, `.mor`, `.mercan`, `.sari`, `.eksi`, `.buyuk` |
| `.yildiz` | Zorluk: `★★<s>★</s>` |
| `.bento` | Grid; sütunlar satır içi `grid-template-columns` ile verilir. Çeşitleri: `.yakin` (sık aralık), `.dikey` (flex sütun) |
| `.ara-bas` | Sayfa içi ara başlık |
| `.vurgu`, `.vurgu-l` | Sarı vurgu, lime alt çizgi |
| `.kesir`, `.izo`, `.var` | Kesir, izotop (kütle/atom no önde), italik değişken |

### Dünya açılışı (sayfa 1)
| Sınıf | Ne için |
|---|---|
| `.acilis-ust`, `.dev-baslik` (`span.mor`, `em` = lime vurgulu) | Dev ünite başlığı |
| `.avo-sahne` + `.balon-avo` + `svg.avo` | Avo'nun karşılama balonu |
| `.rota` | Yılan biçimli rota haritası SVG kartı (yol = kalın mürekkep + mor-a dolgu + kesik mor çizgi) |
| `.rozetler` / `.rozet` | Boyanacak altıgen rozetler (`#rozet-cerceve` sembolü) |
| `.karakterler` / `.karakter` | Sohbettekiler tanıtımı |
| `.hedefler` | Numaralı ana görev listesi |
| `.unvan-bar` + `.unvan-ad` | Unvan merdiveni |
| `.isaretler` | İşaret lejantı (6'lı şerit ya da 2 sütun) |

### Konu sayfası (KN)
| Sınıf | Ne için |
|---|---|
| `.kn-bas` | `svg.kn-hex` (altıgen KN rozeti) + üst etiket + `h1` (içinde `em` = lime vurgu) + `p.alt-bas` + sağda `.kart.ana-gorev` (XP + rozet çipi). Yan görev sayfalarında aynı yapı kullanılır, altıgen yerine elmas ikon gelir. |
| `.sohbet` | Mesajlaşma kartı. Başlık `.sohbet-bas` (`#kanal` + avatar yığını); mesajlar `.mesaj.ece.sag`, `.mesaj.deniz`, `.mesaj.avo`; her mesajda `svg.av` + `.balon` > `.kim` bulunur. Ek parçalar: `.saat` (isteğe bağlı zaman damgası), `.tepki` (küçük tepki çipi). |
| `.dev-sayi-blok` + `.dev-sayi` + `.cetvel` | Kahraman sayı (koyu blok; sayfada tek koyu blok bu olur) |
| `.sayi-kart` | Bento istatistik kutusu: etiket + `.n` (dev sayı, `small` = birim) + kısa açıklama |
| `.yetenek` | **Yetenek kartı** (kesik çizgili, sarı yer imi): `.yno` (Y1… ünite boyunca sürekli numara; renkler `.sari`, `.turkuaz`, `.mercan`, `.lime`) + `.yad` (ad) + `.yf` (formül) + `.yac` (not/XP) |
| `.kes-not` | "✂ kes · defterine yapıştır" satırı |
| `.gorev` (`.kart` ile) | **Görev** = çözümlü örnek. İçinde `.soru`, `ol.akis` (numaralı çözüm akışı; `li > i` numara) ve `.sonuc` (koyu hap, sarı "SONUÇ") bulunur. Tablo gerekiyorsa `table.gorev-tablo` kullanılır. |
| `.tuzak` | **Tuzak! · Doğruluk kontrolü.** `.tuzak-ust` mercan çizgili şerittir ve XP çipini taşır. Altında `.tuzak-iddia` (`small` kaynak + üstü çizili `p` + `.damga` YANLIŞ) ve `.tuzak-dogru` (`.bas` "✓ Doğrusu" + `p`) gelir. |
| `.hizli` (`.kart` ile) | **Hızlı görev** (konu sonu). İçinde `.soru`, `.kilit` (kilitli ipucu, −10 XP, ters yazı) ve `.cevap-satir` (`.cevap-kutu` + ters yazılmış `.ters-cevap`) bulunur. |
| `.kavram`, `.hayat` | Tanım kutusu ve günlük hayat kutusu (etiket rengi) |
| `.zincir` | Eşitlik zinciri kutucukları |

### Kayıt noktası, yan görevler, Boss, final
| Sınıf | Ne için |
|---|---|
| `.ozet-kart` | **Mol Özeti kart serisi**. `.sira` "01/06" etiketini taşır. Renkler: `.koyu` (sayfada tek), `.mor`, `.lime`, `.sari`, `.mercan`. Listeler `ul.ozet-liste` (noktalı) ve `ul.ozet-liste.no` (01, 02… mercan numara). |
| `.durum-satir` + `.piller` + `.pil-baslik` | **Durum güncellemesi**: her ifade için şarj pili seçimi (`#pil-tam/#pil-yari/#pil-bos`) |
| `.paylasim` | **Yorumlarda kim haklı?** paylaşımı. Sırasıyla: `.paylasim-bas` (`.harf` avatar + ad + XP), `.psoru`, `.cozum-satir` (numaralı öğrenci satırları), `.yorumlar` > `.yorum` (karakter avatarı + iddia + `.kutucuk` haklı), `.senin` (kim haklı · satır · Neden? · Doğrusu) |
| `.hikaye` | **Hikâye kartı**. Sırasıyla: `.hikaye-bas` (renkli bağlam şeridi + XP), `.hikaye-ic`, `.yol` (KARAT→GRAM→MOL→TANE çipleri), `ul.yargi` (I/II/III), `.karalama`, `.siklar` > `.sik` |
| `.merdiven` | **İpucu merdiveni**. Solda soru, çözüm satırları ve `.xp-hesap` (40 − (□×10) = □), sağda `.basamaklar` > `.basamak` (kilit, BASAMAK n, −10 XP; basamaklar kademeli içeri kayar) bulunur. |
| `.boss-bas` | Boss başlığı (boss SVG + dev başlık + ekipman kartı) |
| `.anket` | **Anket kartı** (test sorusu). Sırasıyla: `.anket-bas` (`.sno` mercan numara + etiket + XP), `.soru`, `ul.yargi`, `.karalama` (kalan boşluğu işlem alanına çevirir), `.oy` (`.yatay` = 2 sütun). Her şık `b` harf + `span` metin + `em` "%__" (isteğe bağlı tahmin) içerir. |
| `.karalama` | Noktalı işlem alanı. `flex:1` olduğu için kartın boş kısmını doldurur. |
| `.anahtar` | 12'li cevap anahtarı karoları (`i` no, `b` harf, `small` hangi KN) |
| `.cozumler` > `.grup` > `h4` + `p.c` | İki sütunlu çözüm metni |
| `.xp-tablo(.genis)` | XP defteri (durak · en çok · senin XP kutusu, TOPLAM satırı) |
| `.ray` > `.hat` + `.esik` | XP rayı; eşik konumları yüzdeyle verilir (400/1400 = %28,57 …) |

### SVG sembolleri (`unite.html` başındaki gizli `<svg><defs>`)
- **Karakterler:** `#avo` (büyük Avo, 60×66), `#av-avo`, `#av-ece`, `#av-deniz` (40×40 daire avatarlar)
- **Boss:** `#boss`
- **İkonlar:** `#i-hedef`, `#i-kilit`, `#i-tuzak`, `#i-tuzak-b`, `#i-xp`, `#i-bayrak`, `#i-hata`, `#i-ipucu`, `#i-hikaye`, `#i-sohbet`, `#i-makas`, `#i-yetenek`, `#i-dogru`
- **Piller:** `#pil-tam`, `#pil-yari`, `#pil-bos`
- **Rozet çerçevesi:** `#rozet-cerceve`
- **Ok uçları:** `#ok`, `#ok-m`, `#ok-t`, `#ok-g`

Yeni ünite bu `<defs>` bloğunu aynen kopyalar.

---

## 4. Karakterler: ses ve kişilik

| Karakter | Görünüş | Ses | Örnek |
|---|---|---|---|
| **Ece** (10. sınıf) | Mercan daire, sarı “?” rozeti; mesajları sağda, mercan balonda | Meraklı, gündelik dil, kısa sorular. Tipik hataları yüksek sesle düşünür ve bazen yanılır (Tuzak ve Kim haklı? kartlarına bağlanır). | “Peki mol bir kütle mi, bir sayı mı?” |
| **Deniz** (kimya kulübü) | Turkuaz daire, gözlüklü; solda, turkuaz balonda | Sakin ve güvenilir. Günlük benzetmelerle (düzine, bisiklet-tekerlek) adım adım anlatır, terimi `vurgu` ile işaretler. | “Molekülü bisiklet, atomları tekerlek gibi düşün.” |
| **Avo** (`@NA`) | Altıgen mor gövdeli, yörünge antenli küçük robot, göğsünde “n” yazar. Avogadro sayısının kişileşmiş hâlidir. Balonu kesik çizgili mor-a. | Çok kısa ve net, hep sayıyla konuşur, hafif esprili. Kural ve eşitlik söyler; rehberdir. Ara sıra yanılabilir (Kim haklı? sayfasında). | “1 mol CO₂ = N_A molekül = 3 mol atom.” |

Kurallar:
- Her KN sayfası 4–5 mesajlık bir sohbetle açılır. Sıra çoğunlukla Ece soru → Deniz açıklama → Avo sayı/kural → Ece kavrayış ya da yeni soru şeklindedir.
- Son mesaj sayfadaki Tuzak ya da Göreve köprü kurabilir (“Görev 8’e bak”).
- Avo, açılış ve final sayfalarında büyük boyda rehber balonuyla görünür. Diğer sayfalarda avatar, ipucu ya da not satırı olarak çıkar.
- Gerçek bir oyun, uygulama ya da markanın adı veya görsel kimliği kullanılmaz. Sohbet kanalı `#mol-sohbeti` gibi nötr adlarla yazılır.

---

## 5. Oyun terimleri sözlüğü

| Terim | Kitaptaki karşılığı |
|---|---|
| **Dünya n** | Ünite (10. sınıf 2. ünite = Dünya 2) |
| **KN n / Kontrol noktası** | Konu sayfası (bir konu = bir sayfa) |
| **HUD** | Her sayfanın üstündeki koyu gösterge şeridi |
| **Rota haritası** | Açılıştaki yılan biçimli yol; her durakta sayfa no ve XP yazar |
| **Ana görev** | Konunun öğrenme hedefi (sağ üst sarı kart) |
| **Görev** | Çözümlü örnek. Çözüm kapatılıp önce öğrenci dener; tutarsa XP alır. |
| **Yetenek kartı (Yn)** | Formül kartı; kesilip deftere yapıştırılır. Numarası ünite boyunca sürer. |
| **Tuzak! · Doğruluk kontrolü** | Kavram yanılgısı kartı |
| **Hızlı görev** | Konu sonu kısa soru; kilitli ipucu ve ters yazılmış cevap içerir |
| **İpucu kilidi** | Açılırsa XP’den düşen ipucu (−10) |
| **Kayıt noktası** | Tek sayfalık özet (Mol Özeti 01/06…) + durum güncellemesi |
| **Yan görev** | Kim haklı? (hata avcısı), Hikâye kartları (bağlam), İpucu merdiveni |
| **Boss** | Bölüm testi (Dev Sayı); faz 1 ve faz 2 |
| **XP rayı / XP defteri** | Final sayfasında XP toplama ve unvan |
| **Rozet** | KN ve Boss başarıları; öğrenci kendisi boyar |
| **Unvan** | Çaylak → Kaşif → Usta → (Ünite) Efsanesi |
| **Durum güncellemesi / şarj** | Öz değerlendirme (tam / yarım / tekrar) |

---

## 6. XP kuralları

**Ünite başı toplam: 1400 XP.** Dağılım:

| Durak | XP | Nasıl kazanılır |
|---|---|---|
| KN1 | 100 | Konu sayfasındaki çiplerin toplamı |
| KN2–KN5 | 150’şer | Görevler + yetenek kartları (+10’ar) + tuzaklar (+10/+20) + hızlı görev (+20…+40) |
| Kayıt noktası | 40 | Durum güncellemesinin altı satırı doldurulursa |
| Yan görev · Kim haklı? | 120 | 4 paylaşım × 30 (doğru kişi +10, neden +10, doğrusu +10) |
| Yan görev · Hikâye kartları | 120 | 4 kart × 30 |
| Yan görev · İpucu merdiveni | 120 | 3 problem × 40; açılan her basamak −10 |
| Boss | 300 | 12 soru × 25 |

Kurallar:
- KN sayfasındaki tüm XP çiplerinin toplamı rota haritasındaki KN XP’sine **eşit olmalıdır**. Bu kontrol `uretec/dogrula.py` sonunda yapılır.
- İpucu kilidi açılırsa −10 XP düşer (hızlı görevde ve merdivende).
- Görev XP’si yalnızca öğrenci çözümü kapatıp kendisi doğru bulursa alınır.
- **Unvan eşikleri:** Çaylak 0+, Kaşif 400+, Usta 800+, Efsane 1150+. Unvanın adı üniteye göre verilir: “Mol Efsanesi”, “Gaz Efsanesi” …
- Ray yüzdeleri: 400/1400 = %28,57; 800/1400 = %57,14; 1150/1400 = %82,14.
- **Boss Avcısı rozeti:** 10+ doğru.
- HUD `.xpbar` genişliği, o sayfanın başına kadar alınabilecek en çok XP’nin 1400’e oranıdır. Mol ünitesindeki değerler: 0, 0, 7, 18, 29, 39, 50, 53, 61, 70, 79, 89, 100, 100.

Başka bir ünitenin toplamı farklı olacaksa önce bu tablo, rota haritası, XP defteri ve eşikler birlikte yeniden hesaplanır.

---

## 7. Sayfa planı (şablon)

1. **Dünya açılışı:** chip satırı, dev başlık, Avo balonu, rota haritası, rozetler, Sohbettekiler + ana görevler + unvan merdiveni, işaret şeridi
2. **KN1…KN5 (sayfa 2–6), her biri:** `kn-bas` → (sohbet | kavram/harita) → yetenek kartları → görevler → (tuzak | hızlı görev)
3. **Kayıt noktası (s.7):** dev başlık “… Özeti.” → 6 özet kart (3×2) → durum güncellemesi + kendime not
4. **Yan görev 1 (s.8):** Kim haklı? (2×2 paylaşım + Avo notu)
5. **Yan görev 2 (s.9):** Hikâye kartları (2×2; grafik ve tablo olanlar dahil)
6. **Yan görev 3 (s.10):** İpucu merdiveni (3 satır) + yan görev XP toplamı
7. **Boss (s.11–12):** 6 + 6 anket kartı; faz 2’nin sonunda Boss skoru
8. **Cevaplar (s.13):** anahtar (KN etiketiyle) + çözümler + puan + tekrar rotası
9. **Final (s.14):** XP rayı, unvan kartları, XP defteri, rozet sayımı, unvan kartım, sıradaki dünya

Yoğunluk deneyimi:
- KN sayfası tek A4’e ancak her satırın yüksekliği dengelenirse sığar.
- Uzun yetenek formülleri dar sütunda 12–13pt’ye inmelidir.
- Üç sütunlu tuzak kartları uzar; iddia metnini kısa tut.
- Boş kalan dikey alanı `.karalama` ya da çözüm satırlarıyla doldur.
- Her render sonrası `uretec/olc.sh` → `yok` olmalı ve tüm PNG’lere bakılmalıdır.
