# Kaynağa Sadakat Denetimi ve Yazım Birliği Raporu

Bu rapor, kitabın Geniş Özet metni üzerinde yapılan iki çalışmanın sonucunu verir:

1. **Kaynağa sadakat denetimi.** 25 bölümün madde, tablo ve kutu satırları, esas alınan iki Geniş Özet'in metniyle tek tek karşılaştırıldı.
2. **Yazım birliği.** Kişi ve eser adları kitap boyunca tek biçime getirildi. "İki Ömer" duasının Türkçesi Arapça lafızla uyumlu hâle getirildi.

## 1. Kaynağa sadakat denetimi

### Yöntem

- Bölümler dokuz grup hâlinde, metni yazmamış denetçilerce iki asıl kaynakla karşılaştırıldı: Sallâbî, *Siyer-i Nebî 1* ve Evlakî, *Rasûlullah'ın Hayatı*. Denetim kılavuzu: `kaynak/denetim/KILAVUZ.md`.
- Öncelik sırası:
  1. Sallâbî/Evlakî atıfları ve karşılaştırma tablolarının sütunları
  2. İsim, nesep, sayı, tarih, yer ve künyeler
  3. Hiçbir kaynakta karşılığı olmayan iddialar
  4. Anlam kayması
- Kaynak açıkça başka bir şey söylüyorsa metin en küçük değişiklikle düzeltildi.
- Kaynakta bulunamayan ama kaynakla çelişmeyen ifadeler silinmedi; aşağıda listelendi.
- Âyet ve hadis kutuları bu denetimin dışında tutuldu. Bunlar Arapça asıllarıyla birlikte daha önce ayrıca doğrulanmıştı.
- Editör olarak her düzeltmeyi kaynak satırıyla yeniden karşılaştırdım ve işaretlenen şüpheli noktaları kaynakta ayrıca aradım. Bütün düzeltmeleri düzyazı kaynağa da (`kaynak/bolumler/`) işledim.

### Sonuç

- **Kontrol edilenler:** 832 tablo satırı, 1.726 atıflı madde ve bunların içindeki isim, sayı ve künyeler.
- **39 düzeltme yapıldı:** 33'ünü denetçiler, 6'sını editör yaptı. 17 bölümde değişiklik oldu, 8 bölüm kaynakla tam uyumlu çıktı.
- **Ters atıf:** Sallâbî–Evlakî karşılaştırma tablolarında iki müellifin görüşlerinin yer değiştirdiği hiçbir yer çıkmadı. Yalnız ch16'daki bir hücrede Evlakî'nin görüşü eksik aktarılmıştı.
- **Yanlış kişiye bağlanan ya da eksik aktarılan görüşler:** Altı yer çıktı (ch14, ch16, ch18'de iki, ch21'de iki); hepsi düzeltildi ve aşağıda listelendi.

| Bölüm | Düzeltme | Kaynakta bulunamayan (dokunulmadı) |
|---|---|---|
| 1 | 0 | 1 |
| 2 | 1 | 3 |
| 3 | 2 | 0 |
| 4 | 0 | 3 |
| 5 | 3 | 4 |
| 6 | 1 | 3 |
| 7 | 6 | 0 |
| 8 | 0 | 4 |
| 9 | 2 | 2 |
| 10 | 1 | 0 |
| 11 | 0 | 0 |
| 12 | 2 | 1 |
| 13 | 0 | 0 |
| 14 | 1 | 3 |
| 15 | 1 | 0 |
| 16 | 2 | 2 |
| 17 | 0 | 1 |
| 18 | 2 | 1 |
| 19 | 0 | 0 |
| 20 | 0 | 1 |
| 21 | 2 | 0 |
| 22 | 4 | 2 |
| 23 | 2 | 0 |
| 24 | 3 | 1 |
| 25 | 4 | 2 |
| **Toplam** | **39** | **34** |

Her bölümün ayrıntılı raporu `kaynak/denetim/chNN.md` dosyasındadır. Raporlarda her düzeltmenin önceki ve sonraki hâli kaynak satırıyla birlikte verilir.

Raporlardaki adlandırma:
- `S2_1.txt` gibi dosyalar Sallâbî'nin, `E08.txt` gibi dosyalar Evlakî'nin Geniş Özetinden alınmış düz metin dilimleridir.
- Satır numaraları denetim anındaki `ozet/chNN.txt` dosyalarına aittir.

### Önemli düzeltmeler

**Anlamı tersine dönmüş ya da kaynakla çelişen yerler**

- **ch10, Tesnîm âyeti:** Metin "Allah'a yakın olanların kadehine Tesnîm'den katılır" diyordu. Kaynağa göre Tesnîm iyilerin içkisine katılır, Allah'a yakın olanlar ise ondan katıksız içer (S2_3).
- **ch07, Herakleios:** Metin "peygamberin kendi aralarından çıkacağını sandı" diyordu. Kaynakta "Araplardan çıkacağını tahmin etmedi" yazar (S1_6).
- **ch03, Yahudilerin amacı:** Metinde liderliği "ellerinde tutmak" yazıyordu; kaynakta "ellerine geçirmek"tir (S1_3).
- **ch06, Hacerülesved hakemliği:** Kanlı kaplara batırılan kılıçlar değil, ellerdir (E05).
- **ch24, "Allah bize yeter" sözü:** Söz, Mekke'den gelen ilk haberle değil, Hubâb'ın keşif raporunun ardından söylendi (S9_1). Kaçışı önleme amacı ise kaynakta yalnız kadınlar için söylenir, köleler için değil.

**Yanlış kişiye bağlanan ya da eksik aktarılan görüşler**

- **ch18:** Âişe, Esmâ ve Ümmü Seleme'yi sayan "kadın kahramanlar" dersi Evlakî'ye verilmişti. Bu ders Sallâbî'nindir (S6_1).
- **ch18:** Evlakî'nin "caiz yalan" hükmü "caiz bir söz" diye yumuşatılmıştı (E15).
- **ch16:** Evlakî, altı Hazrecli konusunda Sallâbî'ye karşıt gösterilmişti. Oysa o da "altısı da Hazrecliydi" der, öteki rivayeti ek olarak anar (E13).
- **ch21:** Evlakî'nin "dua ile çaba bir arada olmalı" dersi Saîd Havvâ'nın sözüymüş gibi okunuyordu (E17).
- **ch21:** Nevevî'nin savaşta tevriye hükmü, Rasûlullah'ın yön vermeden yola çıktığı Müslim 1901 rivayetine aittir; Ka'b b. Mâlik'in sözüne bağlanmıştı (S8_1).
- **ch14:** Dârü'l-Erkam'da tekbiri Ömer getirmedi; Ömer tekbirlerle karşılandı (E11).

**Yanlış maddeye bağlanmış künyeler**

- **ch22:** Taberî, *Tefsîr* 10/21, Ümmü Safvân'ın sözünden alınıp gençlerin "Bunları dinleri aldatmış" sözüne taşındı (S8_4).
- **ch24:** Buhârî, Meğâzî 19, Übey b. Halef'in ölümünden alınıp "Onu bırakın" sahnesine taşındı (E19).
- **ch25:** İbn Kesîr 4/48, Ümmü Sa'd rivayetinden alınıp Benî Dînarlı kadının sözüne taşındı (S9_3).
- **ch12:** Müslim 2797, İbn Abbas'ın sözünden kaldırıldı. Bu künye bir önceki "melekler onu parçalayacaklardı" hadisine aittir (S3_3).

**Somut bilgi ve anlam kaymaları**

- **ch07:**
  - 40 ukiyye altın "bir buçuk kilo" değil, Evlakî'nin hesabıyla 1,6 kilodur (E06).
  - Yahudilerin tehdidi Evlakî'nin lafzına döndü: "Bir gün aramızdan bir peygamber çıkacak".
  - "Neredeyse imkânsız" yerine kaynaktaki "imkânsız", "en güçlü delil" yerine "en güçlü öngörülerden biri" yazıldı.
- **ch05:** Evlakî'nin çobanlık derslerinde koruma 3., ileri görüşlülük 4. derstir. 2. ders olan sabır, Sallâbî'nin sabır hasletiyle birlikte anlatıldığı için bu belirtildi (E04).
- **ch25:**
  - Sallâbî'nin "eseri olabilir" dediği şey kesin bir tespit gibi yazılmıştı.
  - "Uhud'dan geriye kalanı korumak" ifadesi kaynaktaki "zaferi kalıcı kılmak" ifadesine döndü.
  - Evlakî "şehadet âyeti" ve "hadislerin birçoğu" der; metin bunu "âyet ve hadislerin çoğu" diye abartmıştı.
- **ch22:**
  - Ümeyye'nin öldürüleceği haberi "yıllar önce" değil, "önceden" verildi.
  - Hz. Ömer'in "mütevekkiller" kıssasındaki "mescitte oturma" ayrıntısı kaynakta yok; Evlakî "miskin miskin gezen" der.
  - el-Mısrî'nin "acı verici" dediği kınama "incelikli" diye aktarılmıştı.
- **ch03:** Esed ile Zübyân-Abs'ın yurtları ayrıldı: Teymâ'nın doğusundan Kûfe'nin batısına kadarki bölge ve Teymâ'dan Havran'a uzanan bölge (S1_2).
- **ch02:** Kisrâ'nın iddiası "ilâhlık" değil, "ilâhlar soyundan gelme"dir (S1_1).
- **ch09:**
  - "Ucb" kutusu, hastalığın belirtisini tanım yerine koymuştu.
  - "Onlara katılanlar" diye ayrı bir grup kaynakta yok; bu isimler Sallâbî'de üçüncü halkadadır.
- **ch12:** Kur'ân'da adı en çok geçen peygamberin Hz. Mûsâ olmasına kaynakta olmayan bir sebep ("bu yüzden") bağlanmıştı.
- **ch15:** Kureyş'in suskunluğu Nevfeloğulları'nın silahlarına bağlanmıyor; yalnız Huzâa silahlarından ve Hazrec oklarından korkmaya bağlanıyor (S4_3).
- **ch16:** Evlakî'deki ad "Bahîra b. Faras"tır.
- **ch23:**
  - "Esâs b. Kays" yerine "Şâs b. Kays" yazıldı (bkz. 2. bölüm).
  - Haham "Finhâs" adıyla tekleştirildi.

### Karar bekleyenler: kaynakta karşılığı olmayan somut ayrıntılar (14)

Bu ifadeler kaynakla çelişmiyor ve çoğu tarihî olarak da bilinen bilgiler. Ancak iki kaynakta da geçmiyorlar. Önsöz "kaynaklarda bulunmayan bilgi eklenmedi" dediği için tutarlılık açısından en küçük değişiklikle düzeltilmeleri önerilir.

| # | Yer | Metindeki ifade | Kaynakta olan | Önerilen değişiklik |
|---|---|---|---|---|
| 1 | ch02 | "Hâkim din Mecûsîlikti" | Ülkede çok sayıda din vardı; en köklü inanç Zerdüştîlikti (S1_1) | "Ülkede pek çok din bir arada bulunuyordu" |
| 2 | ch05 | soyuna dair "sahih hadislerin en meşhuru" | "çok sayıda sahih hadis" (S1_5) | "sahih hadislerden biri" |
| 3 | ch05 | "Sabah Hâris…" dedi | zaman kaydı yok | "Sabah" kelimesini çıkarmak |
| 4 | ch05 | Ficâr: "mukaddes ayların ve Harem'in hürmeti" | yalnız Harem'in hürmeti (S1_5) | "ayların ve" kısmını çıkarmak |
| 5 | ch06 | Kâsım "ilk oğuldur", Abdullah "ikinci oğuldur" | doğum sırası verilmez | sıra bilgisini çıkarmak |
| 6 | ch09 | Gizli davet: "tarihçilerin verdiği ad" | adı kimin koyduğu söylenmez | "döneme verilen ad" |
| 7 | ch16 | "Belki en belirleyici etken Yahudi komşuluğuydu" | Sallâbî bu etkeni üçüncü sırada sayar | "Etkenlerden biri de Yahudi komşuluğuydu" |
| 8 | ch17 | Beyhare görüşmesi Akabe'den "bir yıl önce" | süre verilmez | "daha önce" |
| 9 | ch18 | Ümmü Ma'bed'in ailesi "yıllar sonra" Medine'ye geldi | süre verilmez | "sonra" |
| 10 | ch20 | "Askerî okul (en önemlisi)" | dört sebep derece verilmeden sayılır (E16) | "(en önemlisi)" kısmını çıkarmak |
| 11 | ch22 | istişare "ertesi gün" yapıldı | "ertesi gün" yalnız ağlama sahnesi için geçer | "ertesi gün" kısmını çıkarmak |
| 12 | ch22 | Hz. Sevde "taziyeden" dönüyordu | "yanındaydım" (S8_5) | "yanından dönünce" |
| 13 | ch24 | "kervan ortaklarından" yardım istediler | muhatap "Ey Kureyşliler!" (S9_1) | "Kureyşlilerden" |
| 14 | ch25 | Amr b. Cemûh için "topal bir ihtiyar" | yalnız topal olduğu ve dört oğlu yazılı | "topal bir sahâbî" |

### Kaynakta birebir karşılığı olmayan yorum ve anlatı cümleleri (20, dokunulmadı)

Bunlar çoğunlukla "İbretler" kısımlarındaki değerlendirmeler ya da sahneyi canlandıran anlatı cümleleridir. Önsöz bu kısımları zaten kitabın kendi değerlendirmesi olarak tanıtır. Hiçbiri kaynakla çelişmiyor.

| Bölüm | Cümleler |
|---|---|
| ch01 | "Siyer"in tekilinin *sîret* olduğu (dil bilgisi) |
| ch02 | Düalizmi "iki gücün savaş alanı" diye niteleyen cümle; Evlakî'nin tevhid gruplarını Müslim 2865'e bağlayan sentez |
| ch04 | İbretlerdeki üç yorum cümlesi |
| ch05 | Çobanlık dersini "öğretmene" genişleten İbret cümlesi |
| ch06 | Üç hâdiseyi "güven"e bağlayan giriş; İbretlerdeki bugüne uygulama |
| ch08 | Hira yıllarına, ilk davete ve selâm müjdesine dair dört anlatı ve yorum cümlesi (İbn Kayyim'i bu konuda "başta" sayan cümle dâhil) |
| ch09 | "Mekke'nin çarşılarında kimse bilmiyordu" anlatısı |
| ch12 | Azîmet ve ruhsat için "ikisi de meşrudur" (kaynaktaki âyet ve hadisten çıkan sonuç) |
| ch14 | Ebû Tâlib'in "evlatlarını siper etmesi" (kaynakta oğullarını yeğeninin yatağına yatırır); müşriklerin "kulaklarını tıkaması"; İbretlerdeki "vicdan" genellemesi |
| ch16 | "İnsanî tebessüm" yorumu |
| ch25 | Şehitlerin "vadide, kayaların dibinde" yattığı tasvir |

## 2. Yazım birliği

`kaynak/dizgi/yazim_birligi.py` 52 kuraldan oluşur. Kurallar Geniş Özet'e, düzyazıya, Önsöz–Sonsöz–Kronoloji'ye ve Arapçalı kutuların Türkçe meal, kaynak ve etiket satırlarına uygulandı. KAYNAKLAR listesi de bu kapsamdadır. Arapça harfli metne dokunmaz.

| Önce | Sonra |
|---|---|
| ā, ī, ū (İA usulü) | â, î, û |
| Rasulullah | Rasûlullah |
| Ebu Bekir / Ebu'l- | Ebû Bekir / Ebü'l- |
| Beni Hâşim | Benî Hâşim |
| el-Aliy | el-Alî |
| Nâ'ile, Kâ'b | Nâile, Ka'b |
| Mut'im b. Adî | Mut'im b. Adiy |
| Abbâs, Ümeyr, Kayyım | Abbas, Umeyr, Kayyim |
| Muhacir, Mabed, Rum, Said | Muhâcir, Ma'bed, Rûm, Saîd |
| Eşas b. Kays (Evlakî) | Şâs b. Kays (Sallâbî) |
| Fenhas (Evlakî) | Finhâs (Sallâbî) |

Uygulamadan sonra hiçbir eski yazım kalmadığı ayrıca tarandı.

**Hata ve onarımı.** İlk sürümdeki `Eşas → Esâs` kuralı yanlıştı. Kural, Saîd Havvâ'nın *el-Esâs* adlı eseri için düşünülmüştü. Ama Evlakî'nin "Eşas b. Kays" diye yazdığı Yahudiyi "Esâs b. Kays" yaptı; bu kişi Sallâbî'de Şâs b. Kays'tır. Denetim bunu ch23'te yakaladı. Kural `Eşas b. Kays → Şâs b. Kays` olarak düzeltildi ve metin onarıldı.

**"İki Ömer" duası (ch14).** Türkçe meal, kutudaki Arapça lafızla birebir örtüşecek şekilde yeniden yazıldı: "Allah'ım! İslâm'ı, şu iki adamdan sana daha sevimli olanıyla, Ebû Cehil ile ya da Ömer b. Hattâb ile aziz kıl." Kaynak: Tirmizî, Menâkıb (İbn Ömer rivayeti).

**Dizgi.** Hadis kutusunun kaynak satırında aynı künye zaten varsa "Arapça lafız: …" notu artık tekrarlanmıyor. Kapakta eserin adı "Rasûlullah'ın Hayatı" diye düzeltildi.

## 3. Çıktı

- Word ve PDF yeniden dizildi: 448 sayfa.
- Word dosyası OOXML doğrulamasından geçti.
- 103 âyet ve 91 hadis kutusunun hepsinde Arapça asıl var.
- Düzyazı sürümü (`BICIM=duzyazi`) de aynı düzeltmelerle derlenebiliyor: 420 dipnot var, tanımsız dipnot yok.
