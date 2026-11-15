# 10. sınıf · Derişim Birimleri · Yol 6 Göller Yolu (yerel tasarım)

Tema 2 · Bölüm 2 (Çözeltiler 2). Klasik kaynak: `../../10-sinif/06-cozeltiler-2/kaynak.html`. 10. sınıf kitabının **son yolu**:
final sayfası “yolculuk tamamlandı” der ve kitabın sonundaki **Nişan albümü**ne gönderir (sıradaki yol yok).
Tasarım sistemi: `../../yerel-ortak/TASARIM-SISTEMI.md` · rota: `../../yerel-ortak/ROTALAR.md` · dil: `../../YEREL-KIMLIK.md`.

## Komutlar

```sh
cd kitap/10-sinif-yerel/06-cozeltiler-2
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh      # unite.html → PDF + onizleme/sNN.png + taşma
node ../../yerel-ortak/render.js . --hepsi --onizleme                          # + öğretmen, fotokopi, baskı, hazine kartları
```

Beklenen: `dogrula.py` → `SONUÇ: hepsi doğru` (157 denetim) · `olc.sh` → `alan dışı … yok`, kutu taşması yok ·
her PDF'te `pdffonts … | grep -c "Type 3"` → 0.

## Rota ve sayfa planı (15 sayfa, 5 durak)

Eğirdir'den başlayıp kuzey yolundan batıya (Isparta → Burdur → Salda), kışın güney yolundan dönüp (Davraz → Kovada)
Eğirdir Kalesi'nde biten bir halka.

| s. | Sayfa | Konu | Sahne (`uretec/sahneler_unite.py`) |
|---|---|---|---|
| 1 | Yola çıkış | tur haritası, 7 nişan, hedefler | `panorama_goller` (göller, gül bahçeleri, Davraz, rota) + `{{panorama-etiket}}` |
| 2 | 1. durak · Eğirdir Gölü · öğle | derişim, derişik/seyreltik, izotonik; kütlece ve hacimce % | `egirdir_golu` (elma bahçesi, üç bardak) |
| 3 | 2. durak · Isparta gül bahçeleri · şafak | ppm, mg/L, içme suyu sınırları · el-Kindî | `isparta_gul` (gül tarlası, bakır imbikler) |
| 4 | 3. durak · Burdur Gölü · ikindi | molarite, iyon derişimi, yoğunluk köprüsü | `burdur_golu` (flamingo, dikkuyruk ördeği, seyyar laboratuvar) |
| 5 | 4. durak · Salda Gölü · öğle | seyreltme, deriştirme, karıştırma · Câbir | `salda_golu` (beyaz hidromanyezit kıyı, çamlar) |
| 6 | 5. durak · Davraz yolu · kış | koligatif özellikler, tanecik sayısı | `davraz_kis` (kar, telesiyej, tuzlama aracı) |
| 7 | Hülasa · Kovada Gölü | 6 özet, sandık, muhasebe | `kovada` (çadırlar, ateş) |
| 8 | Meclis · Eğirdir köy odası | 4 hatalı çözüm · el-Bîrûnî | `koy_odasi` (pencerede göl ve Yeşilada, Isparta halısı) |
| 9 | Kıssalar · Yeşilada | serum, su sertliği (tablo), donma grafiği, gübre tankı | `yesilada` |
| 10 | Anahtar merdiveni · Eğirdir iskelesi | %98 H₂SO₄, Cl⁻ karışımı, eşit donma | `egirdir_iskele` |
| 11–12 | Büyük İmtihan · Eğirdir Kalesi | 12 meşveret sorusu | `egirdir_kalesi` (yer yer yıkık surlar), `sur_dibi` |
| 13 | Üstad soruları | 6 AYT sorusu (biri grafikli) | ortak `ustad_bandi` |
| 14 | Cevaplar | anahtar, bütün çözümler, sabit sıcaklık tablosu | `egirdir_gece` |
| 15 | Final · yolculuk tamamlandı | akçe rayı, unvanlar, nişan sayımı, altı yol | `final_goller` (havai fişek, nişan çelengi, Pamuk bayrakla) |

Akçe: duraklar 100/150/150/150/150 · Hülasa 40 · Meclis/Kıssa/Anahtar 120'şer · İmtihan 300 = **1400**; Üstad bonus (akçesiz).

## Dosyalar

| Dosya | Ne |
|---|---|
| `uretec/meta.json` | künye: duraklar, 7 nişan (`beher gul balon seyrelt kar` + ortak `kale ustad`), H1–H10, medeniyet, kavramlar |
| `uretec/sablon.html` | 15 sayfanın içeriği; başta küçük üniteye özel `<style>` |
| `uretec/kur.py` | sayfa künyesi; panorama etiketlerinin çakışmasız yerleşimi; final sahnesi; mühür alt yazısı “GÖLLER YOLU” |
| `uretec/sahneler_unite.py` | 14 sahne + parçalar (çam, gül çalısı, bakır imbik, flamingo, dikkuyruk, almaşık sur kalıntısı, tuzlama aracı …) |
| `uretec/infografik_unite.py` | derişim bardakları, alyuvarlar, ppm ızgarası, balon joje, seyreltme/karıştırma, termometreler, kıssa ve Üstad grafikleri |
| `uretec/dogrula.py` | bütün sayılar, tek doğru şık, sayfadan okunan işaretler/anahtar/çözümler, akçe (sayfadaki çiplerden) |

## Doğrulanmış yerel bilgiler (2026-11, WebSearch)

- Isparta gül yağı: yaklaşık 3–4 ton taze gülden 1 kg yağ (TÜRKPATENT başarı hikâyesi, akademik kaynaklar); hasat gün ağarırken başlar, gül aynı gün damıtılır.
- Burdur Gölü: tektonik, kapalı havzalı, tuzlu-sodalı göl; suyunda sodyum sülfat bol; su seviyesi düşüyor; dikkuyruk ördeği için kritik kışlak; Ramsar alanı.
- Salda Gölü: beyaz kıyılar hidromanyezit; su magnezyumca zengin ve bazik; NASA, Jezero kraterine benzetti (2019 arazi çalışması).
- Eğirdir Gölü: Türkiye'nin büyük tatlı su göllerinden (sıralama kaynaklarda farklı olduğu için sayı verilmedi); Yeşilada karaya yolla bağlı.
- Eğirdir Kalesi: yarımadada, kısmen ayakta taş-tuğla sur kalıntısı; sahnelerde yıkık burçlarla çizildi.
- Su sertliği, nitrat ve kuyu örnekleri **örnek veridir** (gerçek ölçüm iddiası yok); DSÖ kılavuz değerleri nitrat 50 mg/L, arsenik 0,01 mg/L.
- Medeniyetimizden metinleri `yerel-cerceve/uretec/medeniyet.py` zaman şeridiyle birebir aynıdır (dogrula.py denetler).
