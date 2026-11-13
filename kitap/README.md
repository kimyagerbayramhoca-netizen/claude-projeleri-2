# Âlemlere Rahmet — Cahiliyeden Uhud'a Siyer-i Nebî

Ali Muhammed Sallâbî'nin *Siyer-i Nebî* (1. cilt) ve Enver el-Evlakî'nin *Rasulullah'ın Hayatı* eserlerinin Geniş Özetleri esas alınarak, iki kaynağın kronolojik olarak birleştirilmesi ve akıcı düzyazıyla yeniden yazılmasıyla hazırlanmış kitap.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `Alemlere_Rahmet_Siyer-i_Nebi.docx` | Word sürümü (düzenlenebilir). İlk açılışta Word içindekiler tablosunu güncellemek isteyip istemediğini sorar; "Evet" deyin. |
| `Alemlere_Rahmet_Siyer-i_Nebi.pdf` | Baskıya hazır PDF (16 × 24 cm, kapaklı). |
| `kaynak/bolumler/` | 25 bölümün Markdown metinleri (`ch01.md` … `ch25.md`). |
| `kaynak/on-arka/` | Künye, Önsöz, Sonsöz ve Kronoloji. |
| `kaynak/PLAN.md` | Bölüm planı, hangi bölümün hangi kaynaktan beslendiği ve yazım kılavuzu. |
| `kaynak/dizgi/` | Kitabı Markdown'dan Word ve PDF'e çeviren betikler, Word şablonu ve kapak. |

## Kitabın yapısı

- **I. Kısım — Nübüvvetin Arifesinde** (1–7. bölümler): Bi'setten önceki dünya, Cahiliye toplumu, Fil Yılı, doğumdan Hira'ya.
- **II. Kısım — Mekke'de Davet** (8–15. bölümler): İlk vahiy, gizli ve açık davet, işkence, Habeşistan, boykot, Hüzün Yılı, Tâif, İsrâ ve Mi'râc.
- **III. Kısım — Hicret** (16–18. bölümler): Kabilelere arz, Akabe biatleri, hicret yolculuğu.
- **IV. Kısım — Medine'de Devlet** (19–25. bölümler): Mescid, kardeşlik, Vesîka, seriyyeler, Bedir, Bedir–Uhud arası, Uhud.

Her bölüm bir âyet ya da hadisle açılır ve "Bu Bölümün İbretleri" başlıklı bir kısımla biter. İki kaynağın birbirinden ayrıldığı yerlerde her iki görüş de sahibinin adıyla verilmiştir. Rivayet kaynakları dipnotlardadır (dipnotlar her sayfada 1'den başlar).

## Yeniden üretmek

Bir bölümü düzenledikten sonra kitabı yeniden oluşturmak için:

```bash
cd kitap/kaynak/dizgi
python3 check.py                                   # bölüm denetimi
python3 build.py ../../Alemlere_Rahmet_Siyer-i_Nebi.docx
python3 to_pdf.py ../../Alemlere_Rahmet_Siyer-i_Nebi.docx ../../Alemlere_Rahmet_Siyer-i_Nebi.pdf
```

Gerekenler: `pandoc`, `python-docx`, LibreOffice (PDF ve içindekiler sayfa numaraları için) ve PDF'te Palatino yerine kullanılan TeX Gyre Pagella yazı tipi (`apt-get install fonts-texgyre`). Word sürümü Palatino Linotype yazı tipini kullanır. Bu yazı tipi Windows'ta hazır bulunur; yüklü olmayan sistemlerde Word benzer bir yazı tipiyle gösterir.
