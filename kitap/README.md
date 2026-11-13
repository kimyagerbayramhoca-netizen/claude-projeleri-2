# Kimya Rotası: özgün kimya kitabı

Verilen ders işleyiş modülleri kaynak alınarak yeniden yazılan, baskıya hazır renkli kimya kitabı.
Konu anlatımları ve sorular özgündür; kaynaklardan metin veya soru kopyalanmaz.

## Birleşik kitaplar
- `kimya-rotasi-9-sinif.pdf`: 10 ünite, 150 sayfa
- `kimya-rotasi-10-sinif.pdf`: 6 ünite, 89 sayfa

Her kitapta genel kapak, "Bu kitabı nasıl kullanırım?" sayfası ve iki sayfalık içindekiler var.
Sayfa numaraları baştan sona süreklidir. Baskıda her ünite sağ sayfada başlasın diye gerektiğinde araya boş sayfa eklenir.
Ünite klasörlerindeki tek ünite PDF'leri kendi içinde 1'den numaralanır.

## Üniteler
| Sınıf | Tema · Bölüm | Klasör |
|---|---|---|
| 9 | Tema 1 · 1 | `9-sinif/01-gunluk-hayatta-kimya` |
| 9 | Tema 1 · 2 | `9-sinif/02-kimyasal-guvenlik` |
| 9 | Tema 1 · 3 | `9-sinif/03-atom-ve-yapisi` |
| 9 | Tema 1 · 4 | `9-sinif/04-periyodik-tablo` |
| 9 | Tema 1 · 5 | `9-sinif/05-periyodik-ozellikler` |
| 9 | Tema 2 · 1 | `9-sinif/06-kimyasal-etkilesimler` |
| 9 | Tema 2 · 2 | `9-sinif/07-adlandirma` |
| 9 | Tema 2 · 3 | `9-sinif/08-molekuller-arasi` |
| 9 | Tema 2 · 4 | `9-sinif/09-katilar` |
| 9 | Tema 2 · 5 | `9-sinif/10-sivilar` |
| 10 | Tema 1 · 1 | `10-sinif/01-kimyasal-degisimler` |
| 10 | Tema 1 · 2 | `10-sinif/02-mol-kavrami` |
| 10 | Tema 1 · 3 | `10-sinif/03-stokiyometri` |
| 10 | Tema 1 · 4 | `10-sinif/04-gazlar` |
| 10 | Tema 2 · 1 | `10-sinif/05-cozeltiler-1` |
| 10 | Tema 2 · 2 | `10-sinif/06-cozeltiler-2` |

## Yapı
- `stil/kitap.css`: ortak sayfa tasarımı, renk sistemi ve kutu tipleri
- `araclar/derle.py`: `kaynak.html` → `unite.html` → PDF
- `YAZIM-REHBERI.md`: yeni ünite yazarken uyulacak kurallar
- Bazı ünitelerde `uretec/` klasörü var: şekiller bir betikle üretilir ve `kaynak.html` şablondan kurulur. Bu ünitelerde düzeltmeyi `uretec/sablon.html` veya `uretec/svgler.py` üzerinde yap, sonra `uretec/kur.sh` (08'de `kur.py`) çalıştır.

## Derleme
```
cd kitap
python3 araclar/derle.py 10-sinif/02-mol-kavrami
node araclar/kitap.js 9-sinif     # birleşik kitap: kapak + içindekiler + üniteler
node araclar/kitap.js 10-sinif
```

## Renk ve kutu sistemi
| Kutu | Renk | Amaç |
|---|---|---|
| Kavram | indigo | Tanımlar |
| Hayatın İçinden | amber | Günlük hayat bağlamı |
| Kavram Yanılgısı | kırmızı | Yanlış ve doğru karşılaştırması |
| Çözümlü Örnek | yeşil-turkuaz | Adım adım çözüm |
| Hata Avcısı | turuncu | Hatalı öğrenci çözümünü bulma |
| İpucu Merdiveni | mor | Kademeli ipuçlu problem |
