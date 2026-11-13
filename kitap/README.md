# Âlemlere Rahmet — Cahiliyeden Uhud'a Siyer-i Nebî (Geniş Özet)

Ali Muhammed Sallâbî'nin *Siyer-i Nebî* (1. cilt) ve Enver el-Evlakî'nin *Rasûlullah'ın Hayatı* eserlerinin Geniş Özetleri esas alınarak hazırlanmış birleşik siyer kitabı. Hazırlık dört adımda yapıldı:

1. İki kaynak kronolojik bir anlatıda birleştirildi.
2. Metin, kayıtlı **Geniş Özet** formatına göre maddeleştirildi ve tablolaştırıldı.
3. Bütün bölümler iki kaynakla satır satır karşılaştırılarak denetlendi.
4. İsim yazımları kitap boyunca tekleştirildi.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `Alemlere_Rahmet_Siyer-i_Nebi.docx` | Word sürümü (A4, 448 sayfa). İlk açılışta içindekiler tablosunu güncellemek için "Evet" deyin. |
| `Alemlere_Rahmet_Siyer-i_Nebi.pdf` | PDF sürümü. |
| `DENETIM_RAPORU.md` | Kaynağa sadakat denetiminin ve yazım birliğinin sonuçları; karar bekleyen 14 madde. |
| `kaynak/denetim/` | Bölüm bölüm denetim raporları (`ch01.md` … `ch25.md`) ve denetim kılavuzu. |
| `kaynak/ozet/` | Kitabın Geniş Özet satırları: `onsoz.txt`, `ch01.txt` … `ch25.txt`, `sonsoz.txt`. |
| `kaynak/bolumler/`, `kaynak/on-arka/` | Maddeleştirmenin dayandığı düzyazı metin (25 bölüm, Önsöz, Sonsöz, Kronoloji). |
| `kaynak/arapca/` | Âyet ve hadis kutularının Arapça metinleri, kutu etiketleri ve KAYNAKLAR listesi. |
| `kaynak/OZET_KILAVUZ.md` | Geniş Özet içerik kuralları ve satır biçimi. |
| `kaynak/PLAN.md` | Bölüm planı ve her bölümün hangi kaynaktan beslendiği. |
| `kaynak/dizgi/` | Derleme hattı (kayıtlı `build.js` ve kitap modu) ve yazım birliği betiği `yazim_birligi.py`. |

## İçerik formatı (kayıtlı Geniş Özet)

- Her bölüm büyük harfli, numaralı bir başlıkla ve bir âyet ya da hadis kutusuyla açılır. Alt başlıklar `5.1`, `5.2` … diye numaralıdır.
- Her alt başlık tek cümlelik italik bir girişle başlar. Ardından kısa, kendi başına tam cümleli ana maddeler (●) ve alt maddeler (◦) gelir. "Etiket: içerik" kalıbı kullanılmaz.
- Görüşler, taksimler ve karşılaştırmalar tablolarla verilir. İki müellifin ayrıştığı yerlerde `Konu | Sallâbî | Evlakî` tablosu kullanılır. Kitapta 278 tablo vardır.
- Kutular:
  - **Âyet** (sarı) ve **hadis** (yeşil): Arapça aslı ve meali ile.
  - **Kavram** (mavi): tanımlar.
  - **Söz** (mor): âlim sözleri ve önemli nakiller.
  - **✎ düzeltme notu.**
- Dipnot yoktur. Rivayet kaynakları maddelerin sonunda parantez içinde verilir. Kitabın sonunda 128 eserlik KAYNAKLAR listesi vardır.

## Arapça metinlerin kaynakları

- **Âyetler (103):** KFGQPC Hafs rivayeti, Osmanî hatlı mushaf metni (quran.ws dijital metni, CC BY 4.0). Âyet fontu "KFGQPC HAFS Uthmanic Script" Word dosyasına gömülüdür.
- **Hadisler (91):**
  - 75'i Sallâbî Geniş Özeti'ndeki Arapça lafızdan.
  - 12'si sunnah.com yapısındaki bir hadis veritabanından (npm `hadith` paketi, MIT).
  - 4'ü Mektebetü'ş-Şâmile'den.
  - Arapça lafzın kaynağı tercümeninkinden farklıysa kutunun kaynak satırında "Arapça lafız: …" yazar.

## Doğruluk denetimi

- 25 bölümün bütün madde, tablo ve kutu satırları iki kaynağın metniyle tek tek karşılaştırıldı: 832 tablo satırı ve 1.726 atıflı madde.
- Toplam 39 düzeltme yapıldı ve hepsi düzyazı kaynağa da işlendi. Bunlar arasında anlamı tersine dönmüş cümleler, yanlış kişiye bağlanmış görüşler ve yanlış maddeye bağlanmış künyeler var.
- Kaynakta karşılığı bulunamayan 14 küçük somut ayrıntı karar için listelendi.
- Ayrıntılar `DENETIM_RAPORU.md` ve `kaynak/denetim/` içindedir.

## Yeniden üretmek

```bash
cd kitap/kaynak
python3 -I dizgi/yazim_birligi.py .     # isim yazımlarını tekleştirir (metinler zaten uygulanmış hâlde)
python3 -I dizgi/ozet_check.py          # Geniş Özet satırlarının denetimi
bash dizgi/derle.sh . ..                # kitap/ içine .docx ve .pdf yazar (ara dosyalar kitap/icerik/)
BICIM=duzyazi bash dizgi/derle.sh . ..  # aynı tasarımla düzyazı sürümü
```

`dizgi/kitap_mode.js` değişirse önce şunu çalıştırın: `cd dizgi && python3 assemble.py build.js kitap_mode.js kitap_build.js`.

Gerekenler:

- Node.js ve `docx` paketi (`npm install -g docx`)
- Python 3 ve `lxml`
- LibreOffice (PDF ve içindekiler sayfa numaraları için)
- KFGQPC v3 âyet fontu `UthmanicHafs-v-3.0.ttf`. Bu dosya `@quran.ws/text` npm paketinin `data/` klasöründe ya da fonts.qurancomplex.gov.sa adresinde bulunur. Yolunu `FONT` değişkeniyle verin; varsayılan `~/.fonts/UthmanicHafs-v-3.0.ttf`.
- PDF'in görünümü için Carlito (Calibri muadili) ve Amiri fontları.
