# Kimya Rotası: özgün kimya kitabı

Verilen ders işleyiş modülleri kaynak alınarak yeniden yazılan, baskıya hazır renkli kimya kitabı.
Konu anlatımları ve sorular özgündür; kaynaklardan metin veya soru kopyalanmaz.

## Yapı
- `stil/kitap.css`: ortak sayfa tasarımı, renk sistemi ve kutu tipleri
- `araclar/derle.py`: `kaynak.html` → `unite.html` → PDF
- `10-sinif/02-mol-kavrami/`: örnek ünite (13 sayfa)

## Derleme
```
cd kitap
python3 araclar/derle.py 10-sinif/02-mol-kavrami
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
