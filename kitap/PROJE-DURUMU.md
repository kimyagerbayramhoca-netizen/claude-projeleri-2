# Kimya Rotası · Kısa devam notu

Yeni oturumda yalnızca bunu oku. Ayrıntı gerekirse `kitap/PROJE-AYRINTI.md` içinde ilgili başlığı bul ve yalnız o bölümü oku.

## Kurallar
- Türkçe ve kısa yaz. PDF ve PNG'leri sohbete gönder. Kullanıcının onayı olmadan büyük bir işe başlama.
- Dal: `claude/max-file-upload-limit-62wc8f`. PR açma. Commit sonuna oturumun verdiği satırları ekle. Kullanıcının e-postası gizli.
- **Bağlamı koru:**
  - Görselleri sen açma. Görsel kontrolü bir ajana yaptır ve en çok 10 satırlık rapor iste.
  - Büyük dosyaları `grep` ve `sed` ile parça parça oku.
  - Aynı anda en çok 2 ajan çalıştır.

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

## Kullanıcıdan beklenenler
1. **"başla":** Yaygınlaştırma planı (AYRINTI §4). Sırası: ortak kütüphaneye taşı → 9/03 ile pilot → bütün üniteler → birleşik kitaplar.
2. **Hangi yeni fikirler örneklenecek** (AYRINTI §5). Önerim: Usturlap Çarkı, Gizli cevap, Kâğıtta animasyon, Ustanın Sırrı.
3. **Deneme baskısı geri bildirimi:** 3B derinliği ve katlama.
4. **Eski kararlar:**
   - Kitap adı ve yazar
   - Elektronegatiflik değerleri (şu an Pauling ölçeği kullanılıyor)
   - Roma rakamından önce boşluk olacak mı

## Komutlar
- Ünite: `cd <ünite> && python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh`
- Sürümler: `node kitap/yerel-ortak/render.js <ünite> --hepsi`
- Kontrol: `pdffonts x.pdf | grep -c "Type 3"` → 0 olmalı
- Kayıt: `git add -A kitap ':!kitap/kimya-rotasi-*-yerel*.pdf'`, ardından commit ve push
- Bilinen hata (yaygınlaştırırken düzelt): `yerel-ortak/cizim` içinde SVG'de `font-family="Baloo Bhaijaan 2"` tırnaksız yazılmış, `"'Baloo Bhaijaan 2'"` olmalı.
