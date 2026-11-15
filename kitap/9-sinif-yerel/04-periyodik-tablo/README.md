# 9. sınıf · Periyodik Tablo · Yol 4 Maden Yolu I · Batı Anadolu (yerel tasarım)

**İskeletten üretildi** (`yerel-ortak/yeni_unite.py`). Bütün sayfa türleri hazır; içerik, sahneler ve sorular
örnek/yer tutucu metindir. Tasarım sistemi, bileşenler ve kurallar: `../../yerel-ortak/TASARIM-SISTEMI.md`
(özellikle §11 “Yeni ünite nasıl yapılır”). Rota ve ortak kurallar: `../../yerel-ortak/ROTALAR.md`. Dil ve karakterler:
`kitap/YEREL-KIMLIK.md`. Sayılar: `kitap/YAZIM-REHBERI.md`.

## Komutlar

```sh
cd kitap/9-sinif-yerel/04-periyodik-tablo
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh    # unite.html → PDF + onizleme/sNN.png + taşma
node ../../yerel-ortak/render.js . --hepsi                                                    # + öğretmen, fotokopi, baskı, hazine kartları PDF'leri
```

`olc.sh` çıktısı `alan dışı … yok` olmalı, `dogrula.py` sonu `SONUÇ: hepsi doğru`. Sonra `onizleme/*.png`'ye tam boy bak.

## Dosyalar

| Dosya | Ne |
|---|---|
| `uretec/meta.json` | künye ve tek doğruluk kaynağı: duraklar (yer, başlık, enlem–boylam), nişanlar, **hazine kartları** (sayfadaki kartlar, Hülasa sandığı ve kesme yaprağı buradan), medeniyet, kavramlar |
| `uretec/sablon.html` | sayfaların içeriği + `{{yer-tutucular}}` |
| `uretec/kur.py` | sayfa künyesi (HUD yeri, altbilgi, akçe çubuğu) |
| `uretec/sahneler_unite.py` | üniteye özel sahneler / nişan ikonları (`ornek_sahne` ile başla) |
| `uretec/dogrula.py` | sayısal doğrulama + sayfadaki cevap işaretleri ↔ anahtar |
| `unite.html`, `04-periyodik-tablo.pdf`, `onizleme/` | ÜRETİLİR |

## Sayfa planı (15 sayfa)

| s. | Sayfa | Sahne |
|---|---|---|
| 1 | Yola çıkış · tur haritası, nişanlar, yol arkadaşları, hedefler | `{{rota-haritasi}}` |
| 2 | 1. durak · sohbet, kavram, hazine, görev, hızlı görev, tuzak | `ornek_sahne (safak)` |
| 3 | 2. durak · sohbet, kavram, hazine, görev, hızlı görev, tuzak, Medeniyetimizden | `ornek_sahne (gun)` |
| 4 | 3. durak · sohbet, kavram, hazine, görev, hızlı görev, tuzak | `ornek_sahne (altin)` |
| 5 | 4. durak · sohbet, kavram, hazine, görev, hızlı görev, tuzak, Medeniyetimizden | `ornek_sahne (gun)` |
| 6 | 5. durak · sohbet, kavram, hazine, görev, hızlı görev, tuzak | `ornek_sahne (altin)` |
| 7 | Hülasa · 6 özet kart, hazine sandığı, muhasebe | `ornek_sahne (altin)` |
| 8 | Yan yol 1 · Meclis (4 hatalı çözüm) | `ornek_sahne` |
| 9 | Yan yol 2 · Kıssalar (4 bağlam sorusu) | `ornek_sahne` |
| 10 | Yan yol 3 · Anahtar merdiveni (3 × 3) | `ornek_sahne` |
| 11 | Büyük İmtihan 1–6 | `ornek_sahne (b62)` |
| 12 | Büyük İmtihan 7–12 + skor | `ornek_sahne (b30)` |
| 13 | Üstad soruları (6, bonus) | `ustad_bandi` |
| 14 | Cevaplar ve çözümler | `ornek_sahne (gece)` |
| 15 | Final · akçe rayı, unvanlar, nişan sayımı | `{{final}}` |

## Yapılacaklar

- [ ] `meta.json`: gerçek duraklar (yer, başlık, enlem–boylam), kale ve konumu, nişan adları, hazine kartları, medeniyet, kavramlar
- [ ] `sahneler_unite.py`: her durak için bölgeye özel sahne (ROTALAR.md); açılışta istersen bölge panoraması
- [ ] `sablon.html`: içerik; “Yer tutucu” alanlarını doldur; Medeniyetimizden kutuları yalnız doğrulanmış bilgiyle
- [ ] bütün sorular + `data-dogru` / `.ogr` işaretleri (öğretmen baskısı) + Cevaplar sayfası
- [ ] `dogrula.py`: her sayıyı yeniden hesapla; `SONUÇ: hepsi doğru`
- [ ] `node ../../yerel-ortak/render.js . --hepsi`: beş PDF; `pdffonts … | grep -c "Type 3"` → 0
