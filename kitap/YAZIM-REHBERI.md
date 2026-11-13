# Kimya Rotası: Ünite Yazım Rehberi

Her ünite, örnek ünite `10-sinif/02-mol-kavrami/kaynak.html` ile **aynı yapıda ve aynı tasarım dilinde** yazılır.
Yazmaya başlamadan önce o dosyayı baştan sona oku. Sınıf adları, kutu tipleri ve kısa yazım kuralları oradakiyle aynıdır.

## Özgünlük (çok önemli)
- Kaynak modüller yayınevi materyalidir, yalnızca **konu kapsamı ve kazanımlar** için kullanılır.
- Kaynaktan cümle, örnek, soru, sayı seti veya şekil **kopyalanmaz**. Anlatımı kendi cümlelerinle yaz. Her soruyu yeni bağlam, yeni madde ve yeni sayılarla baştan kur.
- Kitapta yayınevi adı, logosu veya filigranı geçmez.

## Doğruluk (çok önemli)
- Her hesaplamayı, cevap anahtarını ve şıkkı **yazdıktan sonra yeniden hesapla**. Gerekirse `python3` ile kontrol et.
- Her çoktan seçmeli soruda tam olarak bir doğru şık olmalı. Çeldiriciler tipik öğrenci hatalarından gelsin.
- Mol kütleleri: H 1, He 4, C 12, N 14, O 16, Na 23, Mg 24, Al 27, S 32, Cl 35,5, K 39, Ca 40, Fe 56, Cu 64, Zn 65, Ag 108. Kullanılan değerleri soruda belirt.
- N_A = 6,02·10^23. Gazlarda NŞA molar hacim 22,4 L, R = 0,082 L·atm/(mol·K), T(K) = t(°C) + 273.
- Bilimsel olarak tartışmalı ya da yanlış bilgi yazma. "Hayatın İçinden" verileri gerçek ve doğrulanabilir olmalı. Emin değilsen genel ifade kullan.
- Cevap şıkları dengeli dağılsın (A–E her biri en az bir kez).

## Sayfa planı (13–15 sayfa, A4)
1. **Bölüm kapağı** (`sayfa kapak`): sınıf, tema/bölüm, büyük başlık, slogan, ünitenin simge değeri/denklemi, içindekiler (sayfa numaralarıyla), "Kutuları tanı" lejantı, "Bu bölümün sonunda…" (3 madde)
2. **Konu anlatımı** (4–6 sayfa): `h2.konu` + numara. Her sayfada en az bir Kavram kutusu, uygun yerlerde Hayatın İçinden, Kavram Yanılgısı (yanlış/doğru), Çözümlü Örnek (adım adım `.cozum .adim` + `.sonuc`). Her konuda en az bir SVG şema/grafik/görsel.
3. **Tek sayfada özet**: 4 kutu, "Kendimi değerlendiriyorum" (6 madde), çizgili not alanı
4. **Hata Avcısı**: 4 hatalı öğrenci çözümü (`.defter`, kurgusal Türkçe öğrenci adları), her birinde tek bir net hata
5. **Bağlam temelli sorular**: 4 soru. Günlük hayat, sağlık, endüstri, çevre, laboratuvar. En az biri grafik, biri tablo içersin. Etiketler `etiket-soru`.
6. **İpucu Merdiveni**: 3 problem × 3 basamak
7. **Bölüm testi**: 12 soru, 2 sayfa (`sayfa test` ve `sayfa cift test devam`), 5 şık
8. **Cevap anahtarı ve çözümler**: anahtar ızgarası, test, bağlam, ipucu ve hata avcısının kısa çözümleri

## Kısa yazım kuralları (derle.py dönüştürür)
- `{C2H6}` kimyasal formül (rakamlar alt simge). Yalnızca harf, rakam ve parantez içerebilir. Yük yazımı gerekirse elle `<span class="f">SO<sub>4</sub><sup>2−</sup></span>` yaz.
- `10^23` üs. `[[35|17|Cl]]` izotop. `@ikon:ad` ikon (kavram, hayat, dikkat, ornek, ipucu, hata, hedef, test, lab).
- **SVG içinde bu kısaltmalar çalışmaz**: SVG'de alt simge için `<tspan font-size=".." dy="..">` kullan.
- Metinde başka amaçla `{ }` veya `^` kullanma.
- `{XaYb}` gibi harf alt simgeleri için elle `<sub>` yaz.

## Renk
Ünitenin kimlik rengini `<style>` içinde `:root{--unite:..;--unite-acik:..;--unite-koyu:..}` ile ver.
Kapak SVG degrade renklerini de bu renge göre ayarla.
Kutu renkleri (kavram, hayat, dikkat, ornek, ipucu, hata) değişmez.

## Derleme ve kontrol
```
cd kitap
python3 araclar/derle.py 10-sinif/<klasor>
node araclar/pdf.js 10-sinif/<klasor>/unite.html /dev/null <onizleme-klasoru>
```
"UYARI … taşma" çıkmamalı. Her sayfanın PNG önizlemesini aç ve şunları kontrol et: taşma, üst üste binme, boş kalan yarım sayfa, SVG yazılarının kutudan çıkması, bozuk alt simge.
