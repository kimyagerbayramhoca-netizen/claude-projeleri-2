# Âlemlere Rahmet — Cahiliyeden Uhud'a Siyer-i Nebî

Ali Muhammed Sallâbî'nin *Siyer-i Nebî* (1. cilt) ve Enver el-Evlakî'nin *Rasulullah'ın Hayatı* eserlerinin Geniş Özetleri esas alınarak, iki kaynağın kronolojik olarak birleştirilmesi ve akıcı düzyazıyla yeniden yazılmasıyla hazırlanmış kitap. Kayıtlı **Geniş Özet** tasarımıyla dizilmiştir.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `Alemlere_Rahmet_Siyer-i_Nebi.docx` | Word sürümü (A4, düzenlenebilir). İlk açılışta Word içindekiler tablosunu güncellemek isteyip istemediğini sorar; "Evet" deyin. |
| `Alemlere_Rahmet_Siyer-i_Nebi.pdf` | PDF sürümü (335 sayfa). |
| `kaynak/bolumler/` | 25 bölümün Markdown metinleri (`ch01.md` … `ch25.md`). |
| `kaynak/on-arka/` | Önsöz, Sonsöz ve Kronoloji. |
| `kaynak/arapca/` | Âyet ve hadis kutularının Arapça metinleri, kutu etiketleri ve KAYNAKLAR listesi. |
| `kaynak/PLAN.md` | Bölüm planı, hangi bölümün hangi kaynaktan beslendiği ve yazım kılavuzu. |
| `kaynak/dizgi/` | Kitabı Markdown'dan Word ve PDF'e çeviren hat. |

## Tasarım

Görünüm, kayıtlı "Geniş Özet ve Açıklamalı Tam Metin" skill'inin `build.js` dosyasıyla aynıdır (`kaynak/dizgi/build.js`, değiştirilmeden): A4, Calibri 11, renk rehberli kapak, kırmızı numaralı başlıklar ve renkli kutular.

- **Âyetler:** altın kutu, Arapça aslı ve meali
- **Hadisler:** yeşil kutu, Arapça lafzı ve tercümesi
- **Sözler:** mor kutu
- **Tablolar:** mavi başlıklı
- **Kitabın sonu:** KAYNAKLAR listesi ve kapanış cümlesi

Kitap için `kitap_mode.js` ile şunlar eklendi:

- Kısım sayfaları
- İçindekiler
- Her bölümün yeni sayfadan başlaması
- Dipnotlu düzyazı paragraflar

Tek font farkı âyetlerde: "KFGQPC HAFS Uthmanic Script" (v3) kullanıldı. Bu font Word dosyasının içine gömülüdür, bu yüzden yüklü olmayan bilgisayarlarda da doğru görünür.

## Arapça metinlerin kaynakları

- **Âyetler (103):** Kral Fahd Mushaf Basım Kompleksi'nin (KFGQPC) Hafs rivayetiyle Osmanî hatlı mushaf metni. Dijital metin quran.ws'den alındı (CC BY 4.0). Vakf işaretleri ve âyet numaraları dahildir.
- **Hadisler (91):**
  - 75'i Sallâbî Geniş Özeti'ndeki Arapça lafızdan (gerektiğinde alıntılanan kısma göre birebir kırpılarak).
  - 12'si sunnah.com yapısındaki bir hadis veritabanından (npm `hadith` paketi, MIT).
  - 4'ü Mektebetü'ş-Şâmile'den (Vâkıdî'nin el-Megāzî'si; Ahmed b. Hanbel'den nakleden eserler).
- Arapça lafzın alındığı kaynak tercümeninkinden farklıysa, kutunun kaynak satırında "Arapça lafız: …" diye belirtilmiştir.

## Yeniden üretmek

Bir bölümü düzenledikten sonra:

```bash
cd kitap/kaynak/dizgi
python3 check.py              # bölüm denetimi
bash derle.sh .. ../..        # kitap/ içine .docx ve .pdf yazar (ara dosyalar kitap/icerik/)
```

`kitap_mode.js` değişirse önce `python3 assemble.py build.js kitap_mode.js kitap_build.js` çalıştırın.

Gerekenler:

- Node.js ve `docx` paketi (`npm install -g docx`)
- Python 3 ve `lxml`
- LibreOffice (PDF ve içindekiler sayfa numaraları için)
- KFGQPC v3 âyet fontu (`UthmanicHafs-v-3.0.ttf`). Bu dosya `@quran.ws/text` npm paketinin `data/` klasöründe ya da fonts.qurancomplex.gov.sa adresinde bulunur. Yolunu `FONT` değişkeniyle verin; varsayılan `~/.fonts/UthmanicHafs-v-3.0.ttf`.
- PDF'in bu ortamdaki görünümü için: Carlito (Calibri muadili) ve Amiri fontları.
