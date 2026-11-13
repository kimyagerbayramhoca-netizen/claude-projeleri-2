# GENİŞ ÖZET FORMATINA ÇEVİRME KILAVUZU

Kitabın düzyazı bölümleri, kullanıcının kayıtlı **"Geniş Özet"** formatına çevrilecek: madde madde, tablolu, kutulu. Görünümü derleyici (build.js) uygular; senin işin yalnızca **içerik satırlarını** yazmak.

Girdi: `ozet_in/chNN.md` (düzyazı bölüm; alıntı kutularının yeri `[[QUOTE id · tür · kaynak · Türkçe başı]]` ile işaretli; dipnotlar `[^n-m]` ve dosya sonunda tanımları).
Çıktı: `ozet/chNN.txt` — satır başına bir öğe, alanlar `|` ile ayrılır, boş satır yok.

## Satır türleri

| Satır | Ne zaman |
|---|---|
| `H2|Konu başlığı` | Bölümdeki her `##` alt başlık (ve gerekirse `###` başlıkları da ayrı H2 olabilir). Numarayı derleyici koyar; sen yazma. |
| `INTRO|Tek cümle.` | **Her H2'nin hemen ardından**, o konuyu özetleyen tek cümlelik italik giriş. |
| `B1|Madde.` | Ana madde. |
| `B2|Alt madde.` | Bir B1'i açan, ayrıntı veren alt madde. |
| `QUOTE|<id>` | Girdideki her `[[QUOTE id …]]` işaretinin yerine, **aynı sırayla, her biri bir kez**. Arapçalı kutuyu derleyici basar; kutu metnini maddelerde tekrar etme. |
| `KAVRAM|💡 KAVRAM · TERİM|Tanım cümlesi.` | Metinde tanımı yapılan önemli terimler (ör. şerh-i sadr, hanîf, tedâfü kanunu, Suffe). |
| `SOZ|💬 KİMİN SÖZÜ|"Söz."|kaynak` | Metinde tırnakla aktarılan âlim/sahâbî sözleri ve önemli nakiller (Peygamber sözü değil; onlar zaten QUOTE). Kaynak bilinmiyorsa son alan boş kalır: `SOZ|💬 SEYYİD KUTUB|"…"|`. |
| `TABLE|Başlık|Başlık[|Başlık]` + `ROW|…|…` satırları + `ENDTABLE` | Görüş listeleri, taksimler, karşılaştırmalar, sıralı aşamalar, isim–rol listeleri. **Sallâbî ile Evlakî'nin farklı anlattığı yerler** için `TABLE|Konu|Sallâbî|Evlakî` kullan. ROW'daki hücre sayısı başlık sayısına eşit olmalı. |
| `NOTE|açıklama` | Yalnızca "Hazırlayanın notu" türünden editör düzeltmeleri için (ör. 1. bölümdeki Süheyl/Urve notu). |

Vurgu: madde içinde `**kalın**` (az kullan), eser adı `*italik*`.

## Değişmez kurallar (kayıtlı skill'den)

1. **Sıra metnin sırasıdır.** Bölümün ilk satırı epigraf kutusudur (`QUOTE|…`). Ardından bölümün ilk `##` başlığından önceki giriş paragrafları için `H2|Bölüme Bakış` açılır (INTRO + B1 maddeleri). Sonra metindeki `##` başlıkları aynı sırayla gelir. (`onsoz` ve `sonsoz` dosyalarında da aynı düzen: `onsoz`'da epigraf yoktur, doğrudan H2 ile başla.)
2. **Maddeleştirme istisnasızdır:** kısa giriş cümlesi (INTRO) + kısa, **kendi başına tam cümleli** maddeler. Bir madde 1–2 cümleyi geçmesin.
3. **"Etiket: içerik" kalıbı kullanılmaz.** Yanlış: `B1|Doğum tarihi: 12 Rebîülevvel.` Doğru: `B1|Rasûlullah (s.a.v.) Rebîülevvel ayının on ikisinde, pazartesi günü doğdu.`
4. **Geniş Özet kaynağın içinde kalır:** girdideki bölümde olmayan hiçbir bilgi, yorum, tarih, âyet, hadis ekleme. Ezberden bir şey yazma.
5. **Hiçbir içerik atlanmaz:** bölümdeki her olay, isim, rakam, rivayet farkı, müellif görüşü ve ders bir maddeye, tabloya ya da kutuya girmeli. Sadece bağlaç cümleleri, tekrarlar ve süs ifadeleri düşer. Hedef uzunluk, düzyazının kelime sayısının yaklaşık %65–85'i.
6. **Müellif atıfları korunur:** "Sallâbî'ye göre…", "Evlakî'nin dikkat çektiği gibi…", "İbn Kesîr…" gibi kim neyi söylüyorsa maddede belirt.
7. **Dipnotlar:** Formatta dipnot yoktur. Dipnottaki kaynak bilgisini ilgili maddenin sonuna kısa parantezle ekle: `… (Buhârî, 3; Müslim, 160).` Dipnotta açıklama ya da değerlendirme varsa onu `B2` alt maddesi yap. Hiçbir `[^…]` işareti kalmamalı.
8. **Arapça harf yazma.** Arapça yalnızca QUOTE kutularından gelir.
9. **Kutular madde grupları arasına yerleşir:** QUOTE, KAVRAM, SOZ ve TABLE satırlarını ilgili maddelerin hemen ardına koy.
10. Bölüm sonundaki "Bu Bölümün İbretleri" → `H2|Bu Bölümün İbretleri` + INTRO + B1/B2 maddeleri (her ders ayrı madde).
11. İmla: kitabın yazımını koru (Rasûlullah (s.a.v.), Kur'ân, Ensâr, Muhâcir, Hz. Hatice, Ebû Bekir…). "(s.a.v.)" ve "(r.a.)" her maddede değil, alt başlıkta ilk anışta.

## Örnek

```
QUOTE|ch08-45
H2|Bölüme Bakış
INTRO|Bu bölüm, Hira'daki ilk vahyi iki müellifin farklı vurgularıyla anlatır.
B1|Sallâbî, vahyin başlangıcı hadisinden rüya, halvet, ilim ve fetret üzerine bir dizi ders çıkarır.
B1|Evlakî aynı sahneye "ikra" kelimesinin anlamları ve vahyin şekilleri üzerinden yaklaşır.
H2|Sabah Aydınlığı Gibi Rüyalar
INTRO|Vahiy, Rasûlullah'a (s.a.v.) önce sâdık rüyalar hâlinde geldi.
B1|Gördüğü her rüya, sabahın aydınlığı gibi aynen çıkıyordu (Buhârî, 3; Müslim, 160).
B2|Âlimler bu dönemin altı ay sürdüğünü söyler; Beyhakî de böyle zikreder.
KAVRAM|💡 KAVRAM · SÂLİH RÜYA|Kalbin kendisine açıldığı ve ruhun hoşnut olduğu güzel rüyadır; ona sâdık rüya da denir.
QUOTE|ch08-46
TABLE|Konu|Sallâbî|Evlakî
ROW|Rüyanın rolü|Melekle karşılaşmaya hazırlayan ilâhî terbiyedir.|Altı ayın yirmi üç yıla oranı hadisteki kırk altıda bire denk düşer.
ENDTABLE
SOZ|💬 SEYYİD KUTUB|"Mübalağasız, yeryüzü tarihinde geçen saniyelerin en muazzamı."|Fî Zılâli'l-Kur'ân, 6/3936
```

## Denetim

Her dosyayı yazdıktan sonra çalıştır ve "OK" görene kadar düzelt:
`cd /tmp/claude-0/-home-user-claude-projeleri-2/195be770-d2ea-5fd0-bbb7-354eb75986b4/scratchpad && python3 -I gs/ozet_check.py ch08`
