# Kimya Rotası · Bu deponun talimatları

Bu depo tek bir iş içindir: Van'daki bir kimya öğretmeni için özgün 9. ve 10. sınıf kimya ders kitabı.
- Durum ve sıradaki adım: `kitap/PROJE-DURUMU.md`. Kısadır; ilk iş onu oku.
- Ayrıntı gerekirse `kitap/PROJE-AYRINTI.md` dosyasında yalnızca ilgili başlığı oku.

## İletişim
- Türkçe, kısa ve sade yaz. Dosya adı ya da komut gibi teknik ayrıntıyı yalnızca gerekirse ver.
- Üretilen PDF'leri ve önizlemeleri sohbete doğrudan gönder.
- Kullanıcı onaylamadan büyük bir işe başlama: ünite dalgası, yaygınlaştırma, birleşik kitap. Örnek istenirse yalnızca örneği yap.
- Yalnızca ders kitabı kapsamında kal. Web sayfası, test üretici ve öğretmen kılavuzu sonraya kaldı.

## Bağlamı ve kullanım sınırını koru
- Sayfa görsellerini kendin açma. Görsel kontrolü bir ajana yaptır ve en fazla 15 satırlık metin raporu iste.
- Büyük dosyaları baştan sona okuma; `grep` ve `sed -n` ile gereken parçayı oku.
- Aynı anda en fazla 2 ajan çalıştır. Ajan görevini kısa yaz ve ilgili dosyaları göster.
- Kullanım sınırı dolarsa ajanı SendMessage ile kaldığı yerden sürdür, yenisini başlatma.

## İçerik doğruluğu
- Kaynak yayınevi metinlerinden cümle, soru ya da sayı seti kopyalanmaz.
- Her sayı ve cevap `uretec/dogrula.py` ile yeniden hesaplanır. Her soruda yalnızca bir doğru şık olur.
- Yer ve tarih bilgisi doğrulanmadan yazılmaz. Emin olunmayan bilgi "yaklaşık" diye verilir ya da hiç yazılmaz.
- Cami, kilise ve manastır oyun sahnesi yapılmaz. Depremde hasar görmüş yapılar sağlam gösterilmez. Logo kullanılmaz.

## Baskı kuralları (tamamı: `kitap/yerel-ortak/TASARIM-SISTEMI.md`)
- PDF'te Type 3 font olmamalı: `pdffonts x.pdf | grep -c "Type 3"` komutu 0 vermeli.
- SVG'de konturlu yazı kullanma, onun yerine `halolu_yazi` kullan. CSS `filter` kullanma. Yazılar açık zemin üzerinde olmalı.
- SVG'de yazı tipi adı tırnak içinde yazılır: `font-family="'Baloo Bhaijaan 2'"`.
- Fontlarda bulunmayan sembolleri (→ ↓ ↑ δ α Δ Σ ↔ ✓ ★) kalın yazıda kullanma; şekille ya da tspan ile çiz.

## Git
- Yalnızca `claude/max-file-upload-limit-62wc8f` dalına commit ve push yap. PR açma.
- Birleşik kitap PDF'lerini (`kitap/kimya-rotasi-*-yerel*.pdf`) commit etme; GitHub'ın 100 MB sınırını aşıyorlar.
- Kullanıcının e-postası gizlidir. Model adını commit mesajlarına ya da dosyalara yazma.
