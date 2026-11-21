# Kimya Rotası · Kısa devam notu

Yeni oturumda yalnızca bunu oku. Ayrıntı gerekirse `kitap/PROJE-AYRINTI.md` içinde ilgili başlığı bul ve yalnız o bölümü oku.

## Kurallar
Depo kökündeki `CLAUDE.md` dosyasında; oturum başında kendiliğinden yüklenir.

## Şu an
- Kullanıcı "başla" dedi (21 Kasım 2026): yaygınlaştırma planı (AYRINTI §4) başladı. Şimdilik yalnız tasarım yapılıyor.
- Adım 1: özellikleri ortak kütüphaneye taşıma sürüyor.
- Adım 2: 9/03 pilotu. Planı `9-sinif-yerel/03-atom-ve-yapisi/PILOT-PLAN.md`.
- Pilot bitince kullanıcıya gösterilecek. Onayı gelmeden öteki ünitelere geçilmeyecek.

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
1. **Pilot 9/03'e görüş.** Onay gelirse plan sürer: bütün üniteler → birleşik kitaplar (AYRINTI §4).
2. **Yeni fikir örneklerine görüş** ve kitaba hangi oranda gireceği. Seçilmemiş öteki fikirler: AYRINTI §5.
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
