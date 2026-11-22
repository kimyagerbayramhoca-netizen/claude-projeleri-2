# Kimya Rotası · Kısa devam notu

Yeni oturumda yalnızca bunu oku. Ayrıntı gerekirse `kitap/PROJE-AYRINTI.md` içinde ilgili başlığı bul ve yalnız o bölümü oku.

## Kurallar
Depo kökündeki `CLAUDE.md` dosyasında; oturum başında kendiliğinden yüklenir.

## Şu an
- Kullanıcı "başla" dedi (21 Kasım 2026): yaygınlaştırma planı (AYRINTI §4) başladı. Şimdilik yalnız tasarım yapılıyor.
- Adım 1 bitti: özellikler ortak kütüphanede. API: `yerel-ortak/TASARIM-SISTEMI.md` §16; örnek: `yerel-ortak/katalog/bilesenler/`.
  - Tırnaksız font hatası düzeltildi. SVG yazıları artık Baloo; biten üniteler yeniden kurulunca görsel kontrol gerekir.
  - `yeni_unite.py` iskelete `palet` alanını koymuyor (eklenecek).
- Adım 2: 9/03 pilotu kuruldu (16 → 26 sayfa; dogrula 324 denetim doğru, taşma yok, Type 3 = 0). Planı ve sapmalar: `9-sinif-yerel/03-atom-ve-yapisi/PILOT-PLAN.md` §0.1.
  - Kullanıcı onayladı ("olur yap bakalım"): ünitenin 10 sayfa uzaması, iki sayfa 3B, ünite başına 1600 akçe (Kalfa 450, Usta 900, Üstad 1300).
  - Deneme baskısı hazır ve gönderildi: `9-sinif-yerel/03-atom-ve-yapisi/DENEME-BASKISI.md` ve `03-atom-ve-yapisi-deneme.pdf` (10 sayfa, A4). Kâğıt geri bildirimi bekleniyor. Bütün ünitelere ancak bu geri bildirim ve onaydan sonra geçilir.
  - Çerçeve kaynağı (`yerel-cerceve/uretec/sayfalar.py`) 1600'e güncellendi. Çerçeve, üniteler 1600'e dönünce yeniden kurulacak (adım 4).
  - 3. adımdan önce: `yeni_unite.py` ve infografik akçe rayı (`yerel-ortak/cizim/infografik.py`) hâlâ 1400 kullanıyor, 1600'e çekilecek.
  - 9/06'da Şifreli Kapı için PROTON dışında bir kelime seçilmeli.

## Durum
- **Klasik tasarım:** 16 ünitenin hepsi tamam (`kitap/9-sinif`, `kitap/10-sinif`).
- **Yeni tasarım** (`kitap/*-sinif-yerel`; ortak kod `kitap/yerel-ortak`, belgesi `yerel-ortak/TASARIM-SISTEMI.md`):
  - Tamam: 10/01–10/06, 9/03, 9/04, 9/05.
  - Son kontrol bekliyor: 9/01 ve 9/02 (doğrulamaları geçiyor).
  - Başlanmadı: 9/06–9/10. Rotaları: `yerel-ortak/ROTALAR.md`.
- **Kitap çerçevesi:** `kitap/yerel-cerceve`; birleşik kitabı `kitap_yerel.js` kurar.
- **Özellik örnekleri** (`kitap/gelistirme`):
  - Hap Bilgi ailesi, konu karakterleri, karma paletler (9. sınıf "Çini ve Toprak", 10. sınıf "Göl ve Rasathane")
  - 3B gözlük (`uc-boyut`), katlama (`katla`)
  - Kullanıcı hepsini beğendi; katla ve 3B'nin ağırlığı fazla olsun istiyor.
- **Yeni fikir örnekleri** (`kitap/gelistirme/yeni-fikirler`): Usturlap Çarkı, Gizli cevap, Kâğıtta animasyon, Ustanın Sırrı (ebru). Kullanıcıya gönderildi, görüşü bekleniyor.

## Kullanıcıdan beklenenler
1. **Deneme baskısının kâğıt sonucu** (3B derinliği, katlama, gözlük; tablo `DENEME-BASKISI.md` içinde). İyiyse onayla plan sürer: bütün üniteler → birleşik kitaplar (AYRINTI §4).
2. **Yeni fikir örneklerine görüş** ve kitaba hangi oranda gireceği. Seçilmemiş öteki fikirler: AYRINTI §5.
3. **Eski kararlar:**
   - Kitap adı ve yazar
   - Elektronegatiflik değerleri (şu an Pauling ölçeği kullanılıyor)
   - Roma rakamından önce boşluk olacak mı

## Komutlar
- Ünite: `cd <ünite> && python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh`
- Sürümler: `node kitap/yerel-ortak/render.js <ünite> --hepsi`
- Kontrol: `pdffonts x.pdf | grep -c "Type 3"` → 0 olmalı
- Kayıt: `git add -A kitap ':!kitap/kimya-rotasi-*-yerel*.pdf'`, ardından commit ve push