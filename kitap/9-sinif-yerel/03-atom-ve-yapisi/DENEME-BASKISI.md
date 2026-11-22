# Deneme baskısı · 9/03 Atom ve Yapısı

**Durum (21.11.2026):** PDF hazır (10 sayfa, A4, Type 3 yok). Kâğıt denemesi bekleniyor.

## Amaç
Yeni dört parça önce kâğıtta denenir: köşeyi katla, kat sayfası, 3B (anaglif) sayfaları ve gözlük şablonu. Kâğıtta sorun çıkarsa ortak kodda (`kitap/yerel-ortak`) bir kez düzeltilir, sonra bütün ünitelere geçilir.

## Dosya
- `03-atom-ve-yapisi-deneme.pdf` (bu klasörde).
- 10 sayfa, A4. Çift taraflı basılınca 5 yaprak olur.
- Her yaprak kitaptaki gerçek bir ön-arka çiftidir. Sayfalardaki numaralar kitabın asıl numaralarıdır; deneme sırası aşağıdaki tabloda.

## Sayfa haritası
| Yaprak | Deneme s. | Kitap s. | İçerik | Denenen |
|---|---|---|---|---|
| 1 | 1 | 3 | 1. durak devamı, köşeyi katla kartı | Köşe 1 |
| 1 | 2 | 4 | 2. durak, sol altta köşe 1 cevabı | Köşe 1 |
| 2 | 3 | 7 | 3. durak devamı, köşeyi katla kartı (lamba) | Köşe 2 |
| 2 | 4 | 8 | 3B-1 Orbitaller (5 anaglif), sol altta köşe 2 cevabı | 3B, köşe 2 |
| 3 | 5 | 9 | 3B-2 Alfa tanecikleri (3 anaglif), bonus köşe | 3B, köşe 3 |
| 3 | 6 | 10 | 4. durak, sol altta köşe 3 cevabı | Köşe 3 |
| 4 | 7 | 17 | Kat sayfası "Katla, doğrusu kalsın!" (4 cümle) | Kat izleri |
| 4 | 8 | 18 | Karma sayfa, 3 sütun: Şifreli Kapı, Çeldirici Röntgeni, Robot, Heybe | Sütun aralıkları |
| 5 | 9 | (katalog s. 7) | Gözlük şablonu, gerçek boyut, 188 mm | Ölçü, kesim |
| 5 | 10 | — | Boş (gözlüğün arkası) | — |

Köşe nasıl çalışır: Kart ön yüzdedir (deneme s. 1, 3, 5). O sayfanın sağ alt köşesi öne katlanır. Arka yüzün sol altındaki 64×64 mm kutuda cevap vardır; katlanınca düz okunur.

## Baskı ayarları
- Renkli yazıcı, A4 kâğıt.
- Ölçek "Gerçek boyut" ya da %100 olmalı. "Sayfaya sığdır" kapalı kalmalı; açık kalırsa gözlük ve köşe kutuları küçülür.
- Çift taraflı, uzun kenardan çevir.
- 5. yaprak (gözlük) istenirse kalın kâğıda ya da kartona basılır.
- Gözlük için kırmızı ve camgöbeği şeffaf film gerekir.

## Denetim listesi
1. Ölçü: Gözlük şablonu cetvelle 188 mm mi? Değilse yazıcı ölçeklemiştir; ayarı düzeltip yeniden basın.
2. Köşe (yaprak 1, 2, 3): Sağ alt köşe katlanınca cevap düz okunuyor mu? 64×64 mm kutunun içinde mi (±1 mm)?
3. Ön-arka hizası: Yaprak ışığa tutulunca köşe ile arkadaki cevap kutusu üst üste geliyor mu?
4. Kat sayfası (yaprak 4): Kat izlerinden katlanınca arkadaki karma sayfada yazı kesiliyor mu? Kat çizgisi sütun aralığına düşüyor mu?
5. 3B (deneme s. 4 ve 5): Kırmızı cam sol gözde, kitap 35–40 cm uzakta ve düz. Derinlik görünüyor mu? Çift görüntü (gölge) var mı?
6. Renkler ve küçük yazılar rahat okunuyor mu?
7. Sayfaların üstündeki akçe sayacı "/1600" yazıyor mu?
8. Gözlük kolay kesiliyor mu, yüze oturuyor mu? Takınca kırmızı cam sol gözde mi?

## Geri bildirim
| # | Denetim | Sonuç (iyi / sorun) | Not |
|---|---|---|---|
| 1 | Gözlük 188 mm | | |
| 2 | Köşe cevapları | | |
| 3 | Ön-arka hizası | | |
| 4 | Kat sayfası | | |
| 5 | 3B derinlik | | |
| 6 | Renk ve yazı | | |
| 7 | Akçe /1600 | | |
| 8 | Gözlük kesim ve takma | | |

Kısa not yeterli. İsterseniz sorunlu yerin fotoğrafını da gönderin.

## Sonraki adım
- Sorun çıkarsa: ortak kodda düzeltilir, pilot yeniden üretilir, yeni deneme PDF'i hazırlanır.
- Hepsi iyiyse: 3. adım (bütün üniteler) onayla başlar: 9/01, 9/02, 9/04–9/10, 10/01–10/06. Ardından 4. adım: çerçeve ve birleşik kitaplar.
- 3. adımdan önce: `yeni_unite.py` ve infografik akçe rayı hâlâ 1400 kullanıyor, 1600'e çekilecek. 9/06 için yeni şifre kelimesi seçilecek (PROTON, katla örneğiyle çakışıyor).

## Yeniden üretme (teknik)
Depo kökünden:

```bash
U=kitap/9-sinif-yerel/03-atom-ve-yapisi
K=kitap/yerel-ortak/katalog/bilesenler
(cd $U && python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh)
(cd $K && python3 uretec/kur.py && python3 uretec/dogrula.py)
node kitap/yerel-ortak/render.js "$PWD/$U"
node kitap/yerel-ortak/render.js "$PWD/$K"
python3 - <<'EOF'
from pypdf import PdfReader, PdfWriter
U = "kitap/9-sinif-yerel/03-atom-ve-yapisi"
r = PdfReader(f"{U}/03-atom-ve-yapisi.pdf")
g = PdfReader("kitap/yerel-ortak/katalog/bilesenler/bilesenler.pdf")
w = PdfWriter()
for p in [3, 4, 7, 8, 9, 10, 17, 18]:
    w.add_page(r.pages[p - 1])
w.add_page(g.pages[6])  # gözlük şablonu
mb = r.pages[0].mediabox
w.add_blank_page(width=float(mb.width), height=float(mb.height))
w.add_metadata({"/Title": "Kimya Rotası 9/03 · deneme baskısı"})
w.write(f"{U}/03-atom-ve-yapisi-deneme.pdf")
EOF
pdfinfo $U/03-atom-ve-yapisi-deneme.pdf | grep -E "Pages|Page size"   # 10 sayfa, A4
pdffonts $U/03-atom-ve-yapisi-deneme.pdf | grep -c "Type 3"           # 0 olmalı
```
