#!/usr/bin/env python3
"""Yeni ünite iskeleti üretir (yerel tasarım · ROTALAR.md §2 iskeleti).

    python3 kitap/yerel-ortak/yeni_unite.py 9-sinif-yerel 01-gunluk-hayatta-kimya --yol 1 --rota "İznik–Bursa Yolu" --unite "Günlük Hayatta Kimya"
    seçenekler: --durak 4|5|6 (varsayılan 5) · --tema "Tema 1 · Bölüm 1" · --bolge "Bursa" · --kale "Bursa Hisarı"
                --palet cini-toprak|gol-rasathane|yok (varsayılan sınıfa göre) · --kok <kitap klasörü>

Akçe düzeni 1600 (9/03 pilotu, kullanıcı onayı 2026-11-22): duraklar 700 · Hülasa 40 · Katla 40 (4 tahmin × 10) ·
karma sayfa 160 (Şifreli Kapı 60 · Çeldirici Röntgeni 30 · Robot 30 · Heybe 40) · Meclis, Kıssa, Anahtar 3 × 120 ·
Büyük İmtihan 300; Üstad (ve 3B) akçesiz. Ahilik: Kalfa 450 · Usta 900 · Üstad 1300.
Kat yaprağı: kat sayfası (Katla) kitapta TEK numaralı sağ sayfadır, karma sayfa onun arka yüzüdür (TASARIM-SISTEMI.md §16.4).
Sıra her ünitede pilottaki gibi: … son durak → Hülasa → Katla → Karma → Meclis … Ünite tek numaralı sayfada başlar; durak
sayısı tekse (5) Hülasa'dan önce akçesiz bir bonus sayfa ("Bir bakışta") girer, böylece Katla yine tek numaralı sayfaya düşer.

Oluşan klasör (kitap/<sınıf>/<klasör>/), 4/5/6 durakta 16/18/18 sayfa:
    README.md                ünitenin kısa kılavuzu (komutlar, sayfa planı, yapılacaklar)
    .gitignore               ara dosyalar (unite-fotokopi.html, hazine-kartlari.html, önizleme varyantları)
    uretec/sablon.html       bütün sayfa türleri: açılış, N durak, (tek N'de bonus "Bir bakışta"), Hülasa, Katla (kat sayfası) + karma sayfa (arka yüzü),
                             Meclis, Kıssa, Anahtar merdiveni, Büyük İmtihan (2), Üstad, Cevaplar, Final — örnek bileşenler ve yorumlarla
    uretec/meta.json         künye (duraklar, nişanlar, hazine kartları, palet, akce_toplam…) — örnek değerlerle, DOLDUR
    uretec/kur.py            ince kurucu: sayfa künyesi + HUD
    uretec/sahneler_unite.py ortak parçalardan kurulu örnek sahne (ornek_sahne) + üniteye özel nişan ikonları yeri
    uretec/dogrula.py        doğrulama şablonu (tek doğru şık, sayfadaki işaretler ↔ cevap anahtarı)
    uretec/olc.sh            taşma özeti
Üretilen ünite hemen kurulur ve basılır:  cd kitap/<sınıf>/<klasör> && python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh
"""
import argparse
import json
import os
import sys

ORTAK = os.path.dirname(os.path.abspath(__file__))
KITAP = os.path.dirname(ORTAK)

DURAK_AKCE = {4: [100, 200, 200, 200], 5: [100, 150, 150, 150, 150], 6: [100, 120, 120, 120, 120, 120]}
AKCE_TOPLAM = 1600
AHILIK = (450, 900, 1300)                     # Kalfa, Usta, Üstad (Çırak 0+)
# sayfa başına akçe (durak dışı): kat sayfası 4 tahmin × 10; karma: Şifreli Kapı 60 + Röntgen 30 + Robot 30 + Heybe 4 × 10
SAYFA_AKCE = dict(bonus=0, hulasa=40, katla=40, karma=160, meclis=120, kissa=120, merdiven=120, imtihan1=150, imtihan2=150, ustad=0, cevaplar=0, final=0)
PALET = {9: "cini-toprak", 10: "gol-rasathane"}  # sınıf paletleri: Çini ve Toprak · Göl ve Rasathane (tema.py, TASARIM-SISTEMI.md §16.3)
GOK =["safak", "gun", "altin", "gun", "altin", "safak"]
SAAT = {"safak": "sabah", "gun": "öğle", "altin": "ikindi", "gunbatimi": "akşamüstü", "alaca": "alacakaranlık", "gece": "gece"}
IKON = ["deste", "izotop", "kefal", "mizan", "karisim", "deste"]
NISAN_RENK = ["gol", "kob", "gol", "mer", "erg", "kob"]
# kıssa, imtihan ve üstad örnek cevapları (A–E dağılımı tutar; kendi sorularınla değiştir)
ORNEK_IMTIHAN = "DCBEACCDBECD"
ORNEK_KISSA = "CBED"
ORNEK_USTAD = "BEADCB"
# karma sayfa · Şifreli Kapı örneği: her sorunun (doğru harf, seçenek harfleri); doğrular sırayla ORNEK_SIFRE'yi yazar
ORNEK_SIFRE = "KERVAN"
ORNEK_SK = [("K", "MZKTÇ"), ("E", "ĞJŞEV"), ("R", "BRCDH"), ("V", "GPSYV"), ("A", "ÇFAĞJ"), ("N", "ZLŞTN")]


def doldur(s, **kw):
    for k, v in kw.items():
        s = s.replace(f"«{k}»", str(v))
    return s


def tr_buyuk(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


# ------------------------------------------------------------------ sayfa şablonları

BAS = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Kimya Rotası «sinif» · «unite» · «rota»</title>
<link rel="stylesheet" href="«stil»">
</head>
<body>
<!-- Bu dosyadan uretec/kur.py ile unite.html üretilir. İçerik burada; çizimler {{yer-tutucu}} ile gelir.
     Yer tutucular ve bileşenler: yerel-ortak/TASARIM-SISTEMI.md (§5 bileşenler, §8 yer tutucular, §9 cevap işaretleme).
     HTML yorumları olduğu gibi kalır; yorum içindeki {{…}} çözülmez (örnek bileşenler bu yüzden yorumda durur). -->
{{defs}}
"""

SON = """
</body>
</html>
"""

ACILIS = """
<!-- ================================================================ SAYFA 1 · YOLA ÇIKIŞ -->
<section class="sayfa s1">
  {{zemin}}
  {{hud|1}}
  {{cini}}
  <div class="acilis">
    <div>
      <div class="cipler"><span class="cip koyu buyuk">Yol «yol» · «rota»</span><span class="cip buyuk">«sinif». sınıf · {{meta|tema}}</span></div>
      «dev_baslik»
      <p class="slogan">Ünitenin sloganı: bir atasözü ya da <b>yerel bir cümle.</b></p>
      <div class="cipler" style="margin-top:2.6mm"><span class="cip">«n» durak</span><span class="cip">3 yan yol</span><span class="cip mer">1 kale</span><span class="cip akce">{{sikke|}} {{meta|akce_toplam}} akçe</span></div>
      <!-- uygun ünitede 3B açılımı eklenirse: <span class="cip kob">2 sayfa 3B</span> (bonus, akçesiz) -->
      <div class="cipler" style="margin-top:1.4mm"><span class="cip gol">1 katla sayfası</span><span class="cip keh">1 karma sayfa</span></div>
    </div>
    <div class="pamuk-sahne">
      <div class="balon-buyuk"><span class="et keh">Pamuk · tur rehberin</span><br>Miyav, hoş geldin! Bu yolda <b>neyi</b> öğreneceğimizi bir cümleyle söyle.</div>
      {{poz|pamuk-selam|pamuk-buyuk}}
    </div>
  </div>
  <!-- Tur haritası: meta.json duraklarının enlem–boylamından genel harita. Bölgeye özel panorama çizince
       {{rota-haritasi}} yerine {{sahne|panorama_adi}}, {{rota-etiket}} yerine kendi etiket yer tutucunu koy (Mol: panorama). -->
  <div class="panorama-kutu" data-serbest>
    {{rota-haritasi}}
    <div class="panorama-bas"><h2>Tur haritası</h2><p>«ilk_yer»’den başla, «kale»’ne çık.</p></div>
    {{rota-etiket}}
  </div>
  <main class="ic" style="top:173mm">
    <div class="ara-bas">Kazanılacak nişanlar <small>Durağı bitirince nişanını kendin boya. Kalem senden, nişan bizden.</small></div>
    {{nisan-izgara}}
    <div class="bento" style="grid-template-columns:1fr 1fr">
      <div class="kart karakterler">
        <span class="et mer">{{ikon|meclis}}Yol arkadaşların</span>
        <div class="kisiler"><div class="kisi">{{av|elif}}<div><b>Elif<small>«sinif». sınıf · Edremit</small></b><p>Meraklı; “Neden?” demeden geçmez.</p></div></div>
        <div class="kisi">{{av|yusuf}}<div><b>Yusuf<small>kimya kulübü · Erciş</small></b><p>Sakin; adım adım, örnekle anlatır.</p></div></div>
        <div class="kisi">{{av|pamuk}}<div><b>Pamuk<small>Van kedisi</small></b><p>Bir gözü mavi, bir gözü kehribar; hep sayıyla konuşur.</p></div></div>
        <div class="kisi">{{av|zeynep}}<div><b>Zeynep Hoca<small>kimya öğretmeni</small></b><p>“Medeniyetimizden” köşelerini o anlatır.</p></div></div></div>
      </div>
      <div class="kart">
        <span class="et">{{ikon|hedef}}Yolun sonunda · hedefler</span>
        <ol class="hedefler">
          <li>Birinci kazanım (öğrencinin yapacağı iş).</li>
          <li>İkinci kazanım.</li>
          <li>Üçüncü kazanım.</li>
        </ol>
        <div class="et keh" style="margin-top:3mm">Ahilik basamakları · toplam akçene göre</div>
        <div class="basamak-unvan" style="margin-top:3.4mm">
          <div><b>Çırak</b><small>0+</small></div><div><b>Kalfa</b><small>«kalfa»+</small></div><div><b>Usta</b><small>«usta»+</small></div><div><b>Üstad</b><small>«ustad»+</small></div>
        </div>
      </div>
    </div>
    <div class="kart gol-z isaretler">
      <span class="et">İşaretler</span>
      <div class="is">{{ikon|hedef}}<div><b>Görev</b>Çözümü kapat, dene.</div></div>
      <div class="is">{{ikon|anahtar}}<div><b>Anahtar</b>Açarsan −10 akçe.</div></div>
      <div class="is">{{ikon|tuzak}}<div><b>Tuzak!</b>Yanlış bilinen.</div></div>
      <div class="is">{{ikon|hazine}}<div><b>Hazine</b>Kes, deftere yapıştır.</div></div>
      <div class="is">{{ikon|medeniyet}}<div><b>Medeniyet</b>Bilim mirasımız.</div></div>
      <div class="is">{{ikon|kale}}<div><b>Kale</b>Büyük İmtihan.</div></div>
    </div>
  </main>
  {{alt|1}}
</section>
"""

DURAK = """
<!-- ================================================================ SAYFA «p» · «i». DURAK · «YER» -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <!-- Sahne bandı: uretec/sahneler_unite.py içine bu durağa özel bir sahne yaz (odak sağda, sol üst levhaya boş) ve adını buraya koy. -->
  <div class="bant" data-serbest>{{sahne|ornek_sahne|«gok»|«i»}}
    <div class="levha">{{rozet|«i»}}<div><div class="ust">«i». durak · «yer» · «saat»</div><h1>«i». durak <em>başlığı</em></h1><p class="alt-bas">Durağın tek cümlelik özeti: <b>anahtar fikir</b>.</p><div class="hedef"><b>Hedef</b>Bu durakta öğrencinin yapacağı iş.<span class="cip akce">+«akce» akçe</span><span class="cip">Nişan: «nisan»</span></div></div></div>
  </div>
  <main class="ic" style="top:60mm">
    <!-- Akçe (1600 düzeni): Kavram + Görev + Hızlı görev + Kendini dene (+10) + 2 hazine kartı (+10'ar) = durak akçesi (+«akce»);
         Tuzak ve Hap Bilgi kutuları akçe taşımaz. dogrula.py çipleri sayar. -->
    <div class="bento" style="grid-template-columns:1.05fr .95fr">
      <div class="kart sohbet">
        <div class="sohbet-bas"><b>#yol-sohbeti</b><span class="yigin">{{av|elif}}{{av|yusuf}}{{av|pamuk}}</span></div>
        <div class="mesaj elif sag">{{av|elif}}<div class="balon"><span class="kim">Elif</span>Yerden bir gözlemle açılan soru: “Neden …?”</div></div>
        <div class="mesaj yusuf">{{av|yusuf}}<div class="balon"><span class="kim">Yusuf</span>Adım adım, yerel bir benzetmeyle cevap; <span class="vurgu">kavramın adı</span> burada geçer.</div></div>
        <div class="mesaj pamuk">{{av|pamuk}}<div class="balon"><span class="kim">Pamuk</span>Kısa, sayılı bir espri. Miyav!</div></div>
      </div>
      <div class="bento dikey">
        <div class="kart kavram" style="flex:1">
          <div class="kart-bas"><span class="et kob">{{ikon|kitap}}Kavram</span><span class="cip akce">+«a_kav» akçe</span></div>
          <p><b>Terim:</b> tek cümlelik tanım. Formülde alt/üst simge: H<sub>2</sub>O, 10<sup>23</sup>.</p>
          <!-- sağa 3B molekül:  <div class="resim-sag" style="width:20mm">{{mol|H2O|0,0,0|20mm|e}}</div> -->
        </div>
        {{hazine|H«h1»}}
        <div class="kes-not">{{ikon|makas}}Kes · defterine yapıştır</div>
      </div>
    </div>
    <div class="bento" style="grid-template-columns:1.15fr .85fr">
      <div class="kart gorev">
        <div class="kart-bas"><span class="et">{{ikon|hedef}}Görev «i» · çözümlü</span><span class="sag"><span class="yildiz">★★<s>★</s></span><span class="cip akce">+«a_gor» akçe</span></span></div>
        <!-- köşeye molekül:  <div class="kose-mol">{{mol|CO2|15,30,0|15mm}}</div> -->
        <div class="baglam">Yerel bağlam: tek kısa cümle.</div>
        <p class="soru">Soru kökü. Kullanılan değerleri parantezde ver (C: 12, O: 16 g/mol).</p>
        <ol class="akis"><li><i>1</i><span>Birinci adım (hangi hazine kartı?)</span></li><li><i>2</i><span>İkinci adım</span></li></ol>
        <div class="sonuc"><span>SONUÇ</span>Cevap ve birimi</div>
      </div>
      <div class="kart hizli">
        <div class="kart-bas"><span class="et keh">{{ikon|hedef}}Hızlı görev</span><span class="cip akce">+«a_hiz» akçe</span></div>
        <p class="soru">Kısa bir soru.</p>
        <div class="anahtar-ipucu">{{ikon|anahtar}}<span>Anahtar <b>(−10)</b>: <span class="ters">İpucu ters yazılır.</span></span></div>
        <div class="cevap-satir"><div class="cevap-kutu">CEVABIN:<span class="ogr">öğretmen cevabı</span></div><span class="ters-cevap"><span class="ters">Cevap: …</span></span></div>
      </div>
    </div>
    <div class="bento" style="grid-template-columns:.9fr 1.1fr">
      <div class="tuzak">
        <div class="tuzak-ust"><b>{{ikon|tuzak}}Tuzak!</b></div>
        <div class="tuzak-iddia"><small>Yanlış bilinen</small><p>“Yaygın yanlış inanış.”</p>{{muhur|yanlis}}</div>
        <div class="tuzak-dogru"><span class="bas">{{ikon|dogru}}Doğrusu</span><p>Doğru bilgi, kısa ve net.</p></div>
      </div>
«yan_kutu»
    </div>
    <div class="bento esnek" style="grid-template-columns:1fr .62fr">
      <div class="kart iskelet-alan"><span class="et gum">Yer tutucu</span><p>Bilgi grafiği (info yer tutucusu), ikinci görev ya da tablo alanı. Boşluk bırakma: kalan yeri doldur.</p></div>
      <div class="bento dikey">
        {{hazine|H«h2»}}
        <div class="kes-not">{{ikon|makas}}Kes · defterine yapıştır</div>
        <!-- Kendini dene: iki kısa soru; cevaplar .ogr (öğretmen) ve ters satırda; dogrula.py kendini_dene_ayni ile okur. -->
        <div class="kart kendini-dene" data-soru="KD«i»" style="flex:1">
          <div class="kart-bas"><span class="et kob">{{ikon|hedef}}Kendini dene</span><span class="cip akce">+10 akçe</span></div>
          <div class="soru-k"><i>1</i><div><b>Kısa soru 1?</b><span class="yaz"><span class="ogr">cevap 1</span></span></div></div>
          <div class="soru-k"><i>2</i><div><b>Kısa soru 2?</b><span class="yaz"><span class="ogr">cevap 2</span></span></div></div>
          <div class="ters-alan"><span class="ters">Cevaplar: 1 cevap 1 · 2 cevap 2</span></div>
        </div>
      </div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

MEDENIYET = """      <div class="medeniyet">{{kose}}
        <span class="med-bas">{{ikon|medeniyet}}Medeniyetimizden</span>
        <div class="zh">{{av|zeynep}}Zeynep Hoca anlatıyor</div>
        <p class="metin"><b>Âlimin adı</b> (yıl): YEREL-KIMLIK.md’deki doğrulanmış bilgi, iki cümle.</p>
        <p class="not">Konuya bağlayan tek cümle.</p>
      </div>"""

KIYIDAN = """      <div class="kart kiyidan">
        <span class="et">{{ikon|dalga}}Yoldan</span>
        <p>Bölgeden, doğrulanmış bir günlük hayat bilgisi. Emin değilsen “yaklaşık” de.</p>
      </div>"""

HULASA = """
<!-- ================================================================ SAYFA «p» · HÜLASA -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant b40" data-serbest>{{sahne|ornek_sahne|altin|21}}
    <div class="levha kob">{{rozet|H|-|erg}}<div><div class="ust" style="color:var(--erguvan)">Hülasa · konaklama yeri</div><h1>«kisa» <em style="color:var(--erguvan)">Hülasası</em></h1><p class="alt-bas">Yolun altı kartı. Sınavdan önceki gece bu sayfa yeter.</p></div></div>
  </div>
  <main class="ic" style="top:52.2mm">
    <div class="ozetler" data-tasma-yatay>
      <div class="ozet-kart koyu"><span class="sira">01/06</span><span class="et">Ünitenin sayısı</span><div class="dev-sayi acik">x = y</div><p>Koyu kart: ünitenin simge sayısı ya da denklemi.</p></div>
      <div class="ozet-kart gol"><span class="sira">02/06</span><span class="et">Tek kural</span><h3>Kural cümlesi.</h3><div class="ozet-f">a = b / c</div><p>Kısa açıklama.</p></div>
      <div class="ozet-kart"><span class="sira">03/06</span><span class="et">Okuma</span><h3>Başlık</h3><ul class="ozet-liste"><li>Madde</li><li>Madde</li><li>Madde</li></ul></div>
      <div class="ozet-kart keh"><span class="sira">04/06</span><span class="et keh">Konu</span><h3>Başlık</h3><ul class="ozet-liste"><li>Madde</li><li>Madde</li></ul></div>
      <div class="ozet-kart mer"><span class="sira">05/06</span><span class="et mer">Karşılaştırma</span><h3>Başlık</h3><p>İki şeyin farkı, tek cümle.</p></div>
      <div class="ozet-kart"><span class="sira">06/06</span><span class="et mer">{{ikon|tuzak}}En sık 4 hata</span>
        <ul class="ozet-liste no"><li>Hata</li><li>Hata</li><li>Hata</li><li>Hata</li></ul>
        <div class="muhur-kose">{{muhur|yanlis}}</div></div>
    </div>
    <div class="kart keh-z sandik">
      <div class="kart-bas"><span class="et keh">{{ikon|hazine}}Hazine sandığın · {{meta|hazine_sayisi}} kart</span><span class="kes-not">{{ikon|makas}}Hepsini kesip defterine yapıştırdın mı?</span></div>
      <div class="sandik-izgara">{{sandik}}</div>
    </div>
    <div class="bento esnek" style="grid-template-columns:1.5fr .5fr">
      <div class="kart muhasebe">
        <div class="kart-bas"><span class="et keh">{{ikon|cay}}Muhasebe · kendimi muhasebe ediyorum</span><span class="cip akce">6 satır = +40 akçe</span></div>
        <div class="satir bas"><span>Bardağını ne kadar doldurabilirsin?</span><span>{{cay|1}}Tamam</span><span>{{cay|.5}}Yarım</span><span>{{cay|0}}Tekrar</span></div>
«muhasebe»
      </div>
      <div class="kart not-kart">
        <span class="et">{{ikon|kitap}}Kendime not</span>
        <p class="kucuk">Bu yolda en çok neye dikkat etmeliyim?</p>
        <div class="cizgiler"><div></div><div></div><div></div><div></div></div>
        {{poz|pamuk-kitap|pamuk-oku}}
      </div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

BONUS = """
<!-- ================================================================ SAYFA «p» · BONUS · BİR BAKIŞTA (akçesiz) -->
<!-- Durak sayısı tek olduğu için bu sayfa girer: sıra yine Hülasa → Katla → Karma kalır ve kat sayfası (s.«p_kat») TEK numaralı
     sağ sayfaya düşer. Akçe çipi YOK; HUD çubuğu bu sayfada artmaz. Bileşen: "Bir bakışta" (.bakista, Hap Bilgi ailesi,
     TASARIM-SISTEMI.md §16.2). Uygun ünitede bunun yerine 3B sayfası konabilir (bonus, akçesiz; meta.json "uc_boyut", §16.5). -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant b40" data-serbest>{{sahne|ornek_sahne|alaca|81}}
    <div class="levha kob">{{rozet|B|-|kob}}<div><div class="ust">Bonus · akçesiz</div><h1>Yol <em>bir bakışta</em></h1><p class="alt-bas">Her durak üç cümlede. Hülasa’dan önce bir <b>soluklan</b>.</p></div></div>
  </div>
  <main class="ic" style="top:52.2mm">
    <div class="bento" style="grid-template-columns:repeat(3,1fr);align-items:stretch">
«bakista»
    </div>
    <div class="kart iskelet-alan esnek"><span class="et gum">Yer tutucu</span><p>Konu karakteri, kavram haritası, Hap Bilgi kutuları ya da tablo. Boşluk bırakma: kalan yeri doldur.</p></div>
  </main>
  {{alt|«p»}}
</section>
"""

BAKISTA = """      <div class="bakista">
        <span class="et">{{ikon|hulasa}}«i». durak · bir bakışta</span>
        <ol><li><i>1</i><span>Durağın ilk ana fikri, <b>kısa</b>.</span></li><li><i>2</i><span>İkinci ana fikir.</span></li><li><i>3</i><span>Üçüncü ana fikir.</span></li></ol>
      </div>"""

ALTIN_KURAL = ('      <div class="hb hb-kural">{{kose}}<span class="serit">{{hbi|yildiz}}ALTIN KURAL</span>'
               '<p class="kural">Ünitenin <em>tek cümlelik</em> altın kuralı.</p><p class="alt-not">Kısa bir açıklama.</p></div>')

KATLA = """
<!-- ================================================================ SAYFA «p» · KAT SAYFASI (TEK numaralı sağ sayfa) · KATLA -->
<!-- Kat yaprağı (TASARIM-SISTEMI.md §16.4): bu sayfa kitapta SAĞ (tek) sayfadır; arka yüzü hemen sonraki karma sayfadır
     (s.«p_arka»). Sıra kuralını kur_ortak denetler (bozulursa UYARI yazar). 4 satır × 10 akçe = 40 (başlıkta "4 tahmin · +40 akçe").
     Ortak tür:  {{katla|bag}} "Katla, bağ oluşsun!"  ya da  {{katla|tepkime}} "Katla, tepkime olsun!".
     Ünitenin kendi 4 satırı: uretec/sahneler_unite.py içinde KATLA_BAG (ya da KATLA_TEPKIME), cizim/katla.py BAG / TEPKIME
     biçiminde; yoksa ortak örnek satırlar basılır. Cümle türü ("Katla, doğrusu kalsın!") ünite modülüyle yapılır:
     örnek 9-sinif-yerel/03-atom-ve-yapisi/uretec/katla_unite.py + kur.py'deki {{katla-cumle}} yer tutucusu. -->
<section class="sayfa s«p» kat">
  {{zemin14}}
  {{hud|«p»|kat}}
  {{cini14}}
  {{katla|bag}}
  {{alt|«p»|kat}}
</section>
"""

KARMA_SK = """    <div class="kart sk" data-sk="«k»" data-soru="SK«k»">
      <div class="sk-bas"><span class="sk-no">«k»</span><span class="kaynak">Yol «yol» · «d». durak</span></div>
      <p class="soru">Şifre sorusu «k»: «d». duraktan kısa bir soru?</p>
      <ol class="sk-sec«sinif»">«secenek»</ol>
    </div>"""

KARMA = """
<!-- ================================================================ SAYFA «p» · KARMA SAYFA (s.«p_on» kat sayfasının arka yüzü) -->
<!-- Kat izleri 70 ve 140 mm'de: üç sütun (k1 11–67 · k2 73–137 · k3 143–199 mm); kat yerinden çizgi, tablo, resim geçmez.
     Akçe: Şifreli Kapı 60 · Çeldirici Röntgeni 30 · Robot yanıldı mı? 30 · Heybe 4 × 10 = 160 (TASARIM-SISTEMI.md §16.4).
     Şifreli Kapı: doğru seçeneklerin kod harfleri sırayla şifreyi yazar (örnek «sifre»); yanlış harfler kelime KURMAMALI (elle bak).
     Robot: tek hatalı cümle data-dogru; kurgu notu zorunlu. Heybe: önceki yollardan ve bu yoldan aralıklı tekrar. -->
<section class="sayfa s«p» karma">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="k-bas">{{rozet|«yol»|YOL}}<div><h1>Karma sayfa: <em>kapıyı aç</em></h1><p>Altı soru, bir şifre · bir çeldirici röntgeni · bir yapay zekâ hatası · heybeden dört soru</p></div><span class="kat-not">{{kikon|katla}}Kat izleri sütun aralığına düşer</span></div>
  <div class="kol k1">
    <div class="kart kapi-kart keh-z">
      <div class="kart-bas"><span class="et keh">{{kikon|kapi}}Şifreli kapı</span><span class="cip akce">+60 akçe</span></div>
      <div class="kapi-ic">{{kapi}}<p>Altı sorunun doğru seçeneğindeki harfi sırayla kutulara yaz. Anlamlı bir kelime çıkarsa kapı açılır.</p></div>
      <div class="sifre">«sifre_kutu»</div>
      <p class="kucuk">Kelime çıkmadıysa bir soruda yanıldın: yanlış harfler kelime kurmaz.</p>
    </div>
«sk_1_3»
  </div>
  <div class="kol k2">
«sk_4_6»
    <!-- ÖRNEK (kendi sorunla değiştir): şıklarda sayı + tanı; doğru şık class="d" data-dogru, çeldiriciler class="y". -->
    <div class="kart rn esnek" data-soru="CR1">
      <div class="kart-bas"><span class="et mer">{{kikon|rontgen}}Çeldirici röntgeni</span><span class="cip akce">+30 akçe</span></div>
      <p class="soru"><span class="iz"><span class="izo"><span>23</span><span>11</span></span>Na<sup>+</sup></span> iyonunun proton, nötron ve elektron sayıları sırasıyla hangisidir?</p>
      <div class="rn-sec">
        <div class="y"><b>A</b><span class="say">11, 12, 11</span><span class="tani">Yükü unuttu: e = p saydı.</span></div>
        <div class="y"><b>B</b><span class="say">11, 23, 10</span><span class="tani">Kütle numarasını nötron saydı.</span></div>
        <div class="d" data-dogru><b>C</b><span class="say">11, 12, 10</span><span class="tani">Doğru: katyon 1 e<sup>−</sup> vermiş, e = 11 − 1.</span></div>
        <div class="y"><b>D</b><span class="say">12, 11, 10</span><span class="tani">Protonla nötronu karıştırdı.</span></div>
        <div class="y"><b>E</b><span class="say">11, 12, 12</span><span class="tani">Yükü ekledi: e = 11 + 1.</span></div>
      </div>
      <div class="isaret-acik"><span class="id">doğru</span><span class="iy">çeldirici</span></div>
      <p class="kucuk">p = Z = 11 · n = A − Z = 23 − 11 = 12 · (1+): 1 e<sup>−</sup> vermiş, e = 10</p>
      <div class="yaz-satir">E’yi seçen arkadaşına:<span class="ogr">katyon e<sup>−</sup> verir</span></div>
    </div>
  </div>
  <div class="kol k3">
    <div class="kart robot-kart" data-soru="RB1">
      <div class="kart-bas"><span class="et kob">{{kikon|robot}}Robot yanıldı mı?</span><span class="cip akce">+30 akçe</span></div>
      <div class="robot-bas">{{robot}}<p>KimyaBot’a soruldu: “Bu yolun bir sorusu?” Yanıtında <u>tek</u> bir hata var.</p></div>
      <div class="bot-cevap"><ol>
        <li>Doğru bir cümle.</li>
        <li>Doğru bir cümle.</li>
        <li data-dogru>Tek hatalı cümle (yaygın bir yanlış).</li>
        <li>Doğru bir cümle.</li>
      </ol></div>
      <div class="yaz-satir">Hatalı cümle no ve doğrusu:<span class="ogr">3 · doğrusu</span></div>
      <p class="ters-satir"><span class="ters">Cevap: 3. cümle</span></p>
      <p class="kurgu">KimyaBot kurgusal bir yapay zekâdır; gerçek bir uygulama değildir.</p>
    </div>
    <div class="kart heybe-kart esnek">
      <div class="kart-bas"><span class="et">{{kikon|heybe}}Heybe</span><span class="cip akce">+40 akçe</span></div>
«heybe»
      <p class="ters-satir"><span class="ters">Cevaplar: cevap 1 · cevap 2 · cevap 3 · cevap 4</span></p>
    </div>
  </div>
  {{alt|«p»}}
</section>
"""

HEYBE_SOR = ('      <div class="heybe-sor"><span class="heybe-cip«sinif»">«cip»</span><p>Heybe sorusu «k»: kısa bir tekrar sorusu?</p>'
             '<div class="yaz-satir">Cevap:<span class="ogr">cevap «k»</span></div></div>')

MECLIS_KART = """      <div class="kart meclis" data-soru="M«k»">
        <div class="meclis-bas«renk»"><span class="harf" style="background:var(--«renk2»)">«harf»</span><div><b>«ad»</b> <small>çözümünü meclise getirdi · Hata «k»</small></div><span class="cip akce">+30</span></div>
        <div class="ic2">
          <p class="psoru">Soru kökü (değerler parantezde).</p>
          <div class="cozum-defter"><div><i>1</i>Doğru bir adım.</div><div><i>2</i>Hatalı adım (tek, net bir hata).</div><div><i>3</i>Hatanın taşıdığı sonuç.</div></div>
          <div class="yorum" data-dogru>{{av|yusuf}}<span><b>Yusuf:</b> Bence sorun 2. satırda.</span><span class="k"><span class="kutucuk"></span>haklı</span></div>
          <div class="yorum">{{av|elif}}<span><b>Elif:</b> Hata 3. satırda.</span><span class="k"><span class="kutucuk"></span>haklı</span></div>
          <div class="hukum"><div class="s">HÜKMÜN · SATIR <span class="kutucuk"></span>1 <span class="kutucuk" data-dogru></span>2 <span class="kutucuk"></span>3 · NEDEN?<span class="cizgili"><span class="ogr">kısa neden</span></span></div><div class="s">DOĞRUSU<span class="cizgili"><span class="ogr">doğru sonuç</span></span></div></div>
        </div>
      </div>"""

MECLIS = """
<!-- ================================================================ SAYFA «p» · YAN YOL 1 · MECLİS -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant" data-serbest>{{sahne|ornek_sahne|gun|31}}
    <div class="levha keh">{{rozet|M|-|keh}}<div><div class="ust">Yan yol 1 · yer adı</div><h1>Meclis: <em>kim haklı?</em></h1><p class="alt-bas">Dört çözüm meclise geldi; her birinde <b>tek hata</b> var.</p><div class="hedef"><b>Usul</b>Doğru kişi +10, neden +10, doğrusu +10.<span class="cip akce">4 × 30 = +120 akçe</span></div></div></div>
  </div>
  <main class="ic" style="top:60mm">
    <!-- Cevap işaretleme: haklı yorumda <div class="yorum" data-dogru>, hatalı satırın kutucuğunda <span class="kutucuk" data-dogru>,
         neden ve doğrusu <span class="ogr">…</span> içinde (öğrenci baskısında görünmez). -->
    <div class="bento" style="grid-template-columns:1fr 1fr">
«kartlar»
    </div>
    <div class="kart keh-z meclis-not esnek">
      {{poz|pamuk-dusunen|pn}}
      <p><b>Meclis notu (Pamuk):</b> Bir çözümü kontrol etmenin en hızlı yolu birimlere bakmaktır. Hükmünü verince cevapları <b>s.{{sayfa|«cevap_s»}}</b>’{{ek|«cevap_s»|de}} kontrol et.</p>
      <div class="muhur-yer">{{muhur|dogru}}</div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

KISSA_KART = """      <div class="kart kissa" data-soru="K«k»">
        <div class="kissa-bas«renk»"><span class="et«renk»">{{ikon|kissa}}Kıssa «k» · başlık</span><span class="cip akce">+30</span></div>
        <div class="kissa-ic">
          <p class="metin">Bağlam metni: günlük hayat, sağlık, endüstri, çevre ya da laboratuvar (doğrulanabilir bilgi). <b>Gerekli veri</b> kalın.</p>
          <!-- resimli üst satır:  <div class="ust-satir"><p class="metin">…</p>{{info|ad}}</div> · yargılı soru: <ul class="yargi"><li><b>I.</b>…</li></ul> -->
          <p class="soru">Soru kökü?</p>
          <div class="karalama"><span class="ogr">Kısa çözüm (öğretmen baskısında kırmızı).</span></div>
          <div class="siklar">«siklar»</div>
          <div class="hisse"><b>Kıssadan hisse:</b> Tek cümlelik ders.</div>
        </div>
      </div>"""

KISSA = """
<!-- ================================================================ SAYFA «p» · YAN YOL 2 · KISSALAR -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant" data-serbest>{{sahne|ornek_sahne|safak|41}}
    <div class="levha keh">{{rozet|K|-|keh}}<div><div class="ust">Yan yol 2 · yer adı</div><h1><em>Kıssalar</em></h1><p class="alt-bas">Önce oku, sonra gereken bilgiyi seç. <b>Kıssadan hisse!</b></p><div class="hedef"><b>Usul</b>Çözümünü kartın boş yerine yaz; şıkkı sonra işaretle.<span class="cip akce">4 × 30 = +120 akçe</span></div></div></div>
  </div>
  <main class="ic" style="top:60mm">
    <!-- En az bir kıssada grafik, birinde tablo. Doğru şık: <div class="sik" data-dogru>. Karalamadaki <span class="ogr"> öğretmen çözümüdür. -->
    <div class="bento kissa-izgara esnek" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr">
«kartlar»
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

MERDIVEN_KART = """    <div class="kart merdiven">
      <div>
        <div class="bas-satir"><span class="no">«k»</span><p class="soru">Problem «k»: iki-üç adımlı bir soru. Değerler parantezde (H: 1, C: 12 g/mol).</p></div>
        <div class="cozum-alani"><div><span class="ogr">1. adım (öğretmen)</span></div><div><span class="ogr">2. adım</span></div><div><span class="ogr"><b>Sonuç</b></span></div></div>
        <div class="indigim">İndiğim:<span class="kutucuk"></span>0<span class="kutucuk"></span>1<span class="kutucuk"></span>2<span class="kutucuk"></span>3 &nbsp;·&nbsp; 40 − (<span class="kk"></span> × 10) = <span class="kk"></span> akçe</div>
      </div>
      <div class="basamaklar">
        <div class="et">{{ikon|anahtar}}Takılırsan bir basamak in</div>
        <div class="basamak">{{ikon|kilit}}<span><small>Basamak 1</small>Hangi kavram? Hangi hazine kartı?</span><span class="eksi">−10</span></div>
        <div class="basamak">{{ikon|kilit}}<span><small>Basamak 2</small>Denklemi kur.</span><span class="eksi">−10</span></div>
        <div class="basamak">{{ikon|kilit}}<span><small>Basamak 3</small>Son adım, neredeyse çözüm.</span><span class="eksi">−10</span></div>
      </div>
    </div>"""

MERDIVEN = """
<!-- ================================================================ SAYFA «p» · YAN YOL 3 · ANAHTAR MERDİVENİ -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant" data-serbest>{{sahne|ornek_sahne|gunbatimi|51}}
    <div class="levha keh">{{rozet|A|-|keh}}<div><div class="ust">Yan yol 3 · yer adı</div><h1>Anahtar <em>merdiveni</em></h1><p class="alt-bas">Önce anahtarsız dene. Takılırsan <b>bir basamak in</b>, yeniden dene.</p><div class="hedef"><b>Usul</b>Her problem +40 akçe; açtığın her anahtar −10.<span class="cip akce">3 × 40 = +120 akçe</span></div></div></div>
  </div>
  <main class="ic" style="top:60mm">
«kartlar»
    <div class="bento esnek" style="grid-template-columns:1fr .62fr .7fr">
      <div class="kart keh-z mrd-kart">{{info|merdiven_akce}}</div>
      <div class="kart keh-z yan-toplam">
        <span class="et keh">{{ikon|akce}}Yan yollar</span>
        <div class="tablo"><span>Meclis</span><span class="kk"></span><span>Kıssa</span><span class="kk"></span><span>Anahtar</span><span class="kk"></span><span class="top">Toplam / 360</span><span class="kk top"></span></div>
      </div>
      <div class="kart mer-z siradaki">{{poz|pamuk-sasiran|ps}}<div><span class="et mer">{{ikon|kale}}Sırada</span><b>«kale» · Büyük İmtihan</b><p>12 soru · 25 dakika</p></div></div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

MESVERET = """      <div class="kart mesveret" data-soru="I«k»">
        <div class="mesveret-bas">{{sno|«k»}}<span class="et mer">Meşveret · önce tahmin et</span><span class="cip akce">+25</span></div>
        <p class="soru">Örnek soru «k». Soru kökü; gerekli değerler parantezde.</p>
        <div class="karalama"><span class="ogr">Kısa çözüm.</span></div>
        <div class="oy uc">«oy»</div>
      </div>"""

IMTIHAN1 = """
<!-- ================================================================ SAYFA «p» · BÜYÜK İMTİHAN 1/2 · «KALE» -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant b62" data-serbest>{{sahne|ornek_sahne|gunbatimi|61}}
    <div class="levha mer">{{rozet|K|-|mer}}<div><div class="ust">«kale» · Büyük İmtihan · 1. bölüm</div><h1>Kale <em>kapısı</em></h1><p class="alt-bas">12 soru · 25 dakika. Her doğru <b>+25 akçe</b>; 10+ doğru: <b>Kale Kapısı</b> nişanı.</p>
      <div class="hedef"><b>Azık</b>Soruda kullanılan sabitler ve mol kütleleri.</div>
      <div class="hedef"><b>Meşveret</b>Sınıfça oylayın, şıklara tahmin yüzdesi (%__) yazın, sonra çözün.</div></div></div>
  </div>
  <main class="ic" style="top:76.5mm">
    <!-- 12 soru, 5 şık, A–E her biri en az bir kez. Doğru şık: <div data-dogru><b>D</b>…  Uzun şıklar: class="oy yatay" ya da "oy". -->
    <div class="mesveret-izgara esnek">
«kartlar»
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

IMTIHAN2 = """
<!-- ================================================================ SAYFA «p» · BÜYÜK İMTİHAN 2/2 -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant b30" data-serbest>{{sahne|ornek_sahne|gunbatimi|62}}
    <div class="levha mer kucuk">{{rozet|K|-|mer}}<div><div class="ust">Büyük İmtihan · 2. bölüm</div><h1>Kapı <em>aralandı</em></h1><p class="alt-bas">Sorular 7–12 · sabrın sonu selamettir.</p></div></div>
  </div>
  <main class="ic" style="top:44.5mm">
    <div class="mesveret-izgara esnek">
«kartlar»
    </div>
    <div class="kart mer-z skor">
      {{poz|pamuk-akce|ps}}
      <div><span class="et mer">{{ikon|kale}}İmtihan skoru</span><p><b>10+ doğru:</b> Kale Kapısı nişanını boya · <b>7–9:</b> yan yolları tekrar et · <b>6 ve altı:</b> duraklara dön. Sonra: <b>Üstad soruları</b>.</p></div>
      <div class="skor-kutu">Doğru <span class="kk"></span> × 25 = <span class="kk b"></span> akçe</div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

USTAD_KART = """      <div class="ustad-soru" data-soru="U«k»">
        <div class="ustad-bas">{{sno|«k»|laj}}<span class="et">Konu · konu</span><span class="ustad-zor">AYT</span></div>
        <p class="soru">Üstad sorusu «k»: çok adımlı, YKS/AYT düzeyinde bir soru kökü. Gerekli değerler parantezde.</p>
        <div class="karalama"><span class="ogr">Çözümün iki satırlık özeti.</span></div>
        <div class="siklar">«siklar»</div>
      </div>"""

USTAD = """
<!-- ================================================================ SAYFA «p» · ÜSTAD SORULARI (bonus) -->
<section class="sayfa s«p» ustad-sayfa">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant b40" data-serbest>{{sahne|ustad_bandi}}
    <div class="levha ustad">{{rozet|Ü|-|laj}}<div><div class="ust">Üstad soruları · bonus · YKS/AYT tarzı</div><h1>Üstad <em>soruları</em></h1><p class="alt-bas">Altı zor soru. Akçe yok; <b>6/6</b> doğru: <b>Üstad Mührü</b>.</p></div></div>
  </div>
  <main class="ic" style="top:54mm">
    <!-- 6 soru · 5 şık · tek doğru (data-dogru) · cevaplar dağınık · en az birinde grafik ya da tablo (<div class="ustad-sekil">…</div>
         ya da <table class="ustad-tablo">). Çözümler Cevaplar sayfasına da yazılır. Akçeye dahil DEĞİL (toplam 1600 kalır). -->
    <div class="ustad-izgara esnek">
«kartlar»
    </div>
    <div class="ustad-muhur">
      {{nisan|ustad}}
      <div><span class="et">{{ikon|medeniyet}}Üstad Mührü · bonus nişan</span><p><b>6/6 doğru:</b> mührü boya ve final sayfasında işaretle. <b>4–5:</b> çözümleri oku, yarın yeniden dene. Akçeye eklenmez.</p></div>
      <div class="skor-kutu">Doğru <span class="kk"></span> / 6</div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

CEVAPLAR = """
<!-- ================================================================ SAYFA «p» · CEVAPLAR VE ÇÖZÜMLER -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant b36" data-serbest>{{sahne|ornek_sahne|gece|71}}
    <div class="levha kucuk">{{rozet|✓|-|gol}}<div><div class="ust">Turun sonu · gece nöbeti</div><h1>Cevaplar &amp; <em>çözümler</em></h1></div></div>
  </div>
  <main class="ic" style="top:50.5mm">
    <!-- dogrula.py bu ızgarayı okur ve soru sayfalarındaki data-dogru işaretleriyle karşılaştırır. -->
    <div class="kart anahtar-kart">
      <div class="kart-bas"><span class="et">{{ikon|anahtar}}Büyük İmtihan anahtarı · durak etiketiyle</span><span class="kes-not">Yanlışın hangi duraktan? Etikete bak.</span></div>
      <div class="anahtar-izgara">
«anahtar»
      </div>
    </div>
    <div class="kart cozum-kart esnek">
      <div class="cozumler">
        <div class="grup"><h4>Büyük İmtihan</h4>
«imtihan_cozum»
        </div>
        <div class="grup"><h4>Kıssalar</h4>
«kissa_cozum»
        </div>
        <div class="grup yan-anahtar"><h4>Yan yollar · hızlı anahtar</h4>
          <p><b>Kıssa</b>«kissa_ck»</p>
          <p><b>Meclis</b><span class="ck">1 Yusuf</span><span class="ck">2 Yusuf</span><span class="ck">3 Yusuf</span><span class="ck">4 Yusuf</span></p>
          <p><b>Merdiven</b><span class="ck">1 · …</span><span class="ck">2 · …</span><span class="ck">3 · …</span></p>
          <p><b>Karma</b><span class="ck">Kapı «sifre»</span><span class="ck">Röntgen C</span><span class="ck">Robot 3</span></p>
        </div>
        <div class="grup"><h4>Üstad soruları</h4>
«ustad_cozum»
        </div>
        <div class="grup"><h4>Meclis · merdiven · hızlı görevler</h4>
          <p class="c"><b>Meclis 1 · Yusuf</b> Hatalı satır ve doğrusu.</p>
          <p class="c"><b>Merdiven 1</b> Kısa çözüm.</p>
          <p class="c"><b>1. durak</b> Hızlı görev cevabı.</p>
        </div>
      </div>
    </div>
    <div class="bento" style="grid-template-columns:.8fr 1.2fr">
      <div class="kart keh-z puan">
        <span class="et keh">{{ikon|akce}}Puanını hesapla</span>
        <p>İmtihan: doğru sayın × 8,33 ≈ puanın. Her doğru <b>+25 akçe</b>.</p>
        <div class="skor-kutu">Doğru <span class="kk"></span> × 8,33 ≈ <span class="kk"></span> puan</div>
      </div>
      <div class="kart tekrar">
        <span class="et">{{ikon|harita}}Tekrar rotası · yanlışın nereden?</span>
        <ul class="ozet-liste">«tekrar»</ul>
      </div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

FINAL = """
<!-- ================================================================ SAYFA «p» · FİNAL -->
<section class="sayfa s«p»">
  {{zemin}}
  {{hud|«p»}}
  {{cini}}
  <div class="bant final-bant" data-serbest>{{final}}
    <div class="levha final-levha">{{rozet|★|-|keh}}<div><div class="ust">«hud» tamam · Yol «yol» final</div><h1>Yol <em>tamamlandı!</em></h1><p class="alt-bas">Akçeni topla, unvanını al, nişanlarını say.</p></div></div>
    <div class="balon-buyuk final-balon"><span class="et keh">Pamuk</span><br>Ünitenin özünü tek cümleyle söyleyen kapanış. Miyav!</div>
  </div>
  <main class="ic" style="top:103mm">
    <div class="kart ray-kart">
      <div class="kart-bas"><span class="et keh">{{ikon|akce}}Akçe rayı</span><span class="kes-not">Toplamını raya işaretle · unvanını yuvarlak içine al</span></div>
      {{info|akce_rayi|ÜSTAD|«toplam_akce»}}
    </div>
    <div class="unvanlar">
      <div class="unvan">{{info|unvan_rozeti|1|#A3B3BE}}<b>Çırak</b><small>0–«kalfa_1» akçe</small><p>Yola çıktın. Durak görevlerini tekrar dene.</p></div>
      <div class="unvan">{{info|unvan_rozeti|2|#13A3A6}}<b>Kalfa</b><small>«kalfa»–«usta_1» akçe</small><p>Haritayı biliyorsun. Yan yollarla güçlen.</p></div>
      <div class="unvan">{{info|unvan_rozeti|3|#0E4C5A}}<b>Usta</b><small>«usta»–«ustad_1» akçe</small><p>Her yönde geçiş yapıyorsun. Tuzaklara dikkat.</p></div>
      <div class="unvan ust">{{info|unvan_rozeti|4|#F0A21A}}<b>Üstad</b><small>«ustad»–«toplam_akce» akçe</small><p>Kale kapısını açtın. Sıradaki yol seni bekliyor.</p></div>
    </div>
    <div class="bento esnek" style="grid-template-columns:1.06fr .94fr">
      <div class="kart defter-kart">
        <span class="et keh">{{ikon|hulasa}}Akçe defteri</span>
        <table class="«defter_sinif»">
          <tr><th>Durak</th><th>En çok</th><th>Senin</th></tr>
«defter»
          <tr class="top"><td>TOPLAM</td><td class="n">«toplam_akce»</td><td class="k"><span></span></td></tr>
        </table>
      </div>
      <div class="bento dikey">
        <div class="kart nisan-kart">
          <span class="et">{{ikon|kale}}Nişan sayımı · boyadıklarını işaretle</span>
          {{nisan-sayim}}
        </div>
        <div class="kart unvan-kartim">
          <span class="et mer">{{ikon|bayrak}}Unvan kartım</span>
          <div class="satirlar"><div>Adım:</div><div>Unvanım:</div><div>Toplam akçe:</div></div>
        </div>
        <div class="kart gol-z siradaki-yol">
          <span class="et">{{ikon|harita}}Sıradaki yol →</span>
          <b>Yol «yol_sonra» · sıradaki ünite</b>
          <p>Bir sonraki yolun merak uyandıran tek cümlesi.</p>
        </div>
      </div>
    </div>
  </main>
  {{alt|«p»}}
</section>
"""

# ------------------------------------------------------------------ diğer dosyalar

KUR_PY = '''#!/usr/bin/env python3
"""«unite» · «rota» — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node «render» . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası
ve (gerekirse) üniteye özel yer tutucular. Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır;
sahneler uretec/sahneler_unite.py'dedir.
"""
import os
import sys


def _ortak():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "kur_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak/kur_ortak.py bulunamadı")


sys.path.insert(0, _ortak())
import kur_ortak as KO  # noqa: E402

# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / «toplam_akce»
# Kat yaprağı: s.«p_kat» kat sayfası (TEK numaralı sağ sayfa) + s.«p_kar» karma sayfa (arka yüzü).
SAYFA = {
«sayfa»
}
# HUD ilerleme noktaları: «n» durak + Hülasa + 3 yan yol + kale; kat ve karma sayfası Hülasa'nın noktasında.
# Her sayfada "şimdi" olan (−1: yok, «tam»: hepsi tamam)
SIMDI = {«simdi»}

u = KO.Unite(__file__, SAYFA, SIMDI)

# Üniteye özel yer tutucu örneği (şablonda {{selam|Elif}} → <b>Merhaba Elif</b>):
# u.yer_tutucu("selam", lambda ad: f"<b>Merhaba {ad}</b>")

if __name__ == "__main__":
    u.calistir()
'''

SAHNELER_PY = '''"""«unite» · üniteye özel sahneler, nişan ikonları ve bilgi grafikleri.

kur_ortak bu modüle {{sahne|ad|arg…}} ve {{info|ad|arg…}} için ORTAK kütüphaneden (yerel-ortak/cizim) ÖNCE bakar.
Ortak dosyaları değiştirme; yeni çizimleri burada ortak parçalardan kur (TASARIM-SISTEMI.md §6):
  • bant 2100×460 birim (1 birim = 0,1 mm), preserveAspectRatio="xMidYMid slice"
  • sol üst ≈ %55 × %75 gökyüzü/su olarak BOŞ (levha oturur); odak yapı sağ %40'ta; ufuk y ≈ 260–300
  • ışık yönü (isik) bütün çağrılarda aynı; tohum sabit → her kurulumda aynı resim
  • her Svg öneki benzersiz (aynı önek iki farklı çizimde kullanılırsa renkler bozulur)
  • konturlu (stroke) SVG yazısı yok: hale gerekiyorsa temel.halolu_yazi
"""
from cizim.temel import Svg, f, egri_d  # noqa: F401
from cizim import sahne as S, yapilar as Y  # noqa: F401
from cizim.sahneler import W, H, _bitir, _cerceve_golge

# Üniteye özel nişan ikonları: 48×48 çizgi SVG (dolgu yok; öğrenci boyar). meta.json nisanlar[].ikon bu adları kullanabilir.
NISAN_IKON = {
    # "cini": '<circle cx="24" cy="24" r="16"/><path d="M24 8 V40 M8 24 H40"/>',
}


def ornek_sahne(tema="gun", tohum="1"):
    """ÖRNEK durak bandı (ortak parçalardan): gökyüzü + güneş/ay + bulut + uzak dağlar + ova + kavaklar + sağda kümbet.
    Şablonda: {{sahne|ornek_sahne|safak|1}}. tema: safak gun altin gunbatimi alaca gece (sahne.GOK).
    Bunu kopyalayıp durağın gerçek yerini çiz (ör. kumbet yerine Y.van_kalesi, Y.kucuk_kale, Y.iskele, Y.selale …)."""
    t = int(tohum)
    s = Svg(f"un-{tema}-{t}")
    ufuk = 286
    gece = tema in ("gece", "alaca")
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, tema)
    if gece:
        s += S.yildizlar(s, 0, 0, W, ufuk, 90, t)
        s += S.ay(s, 1500, 90, 26)
    else:
        s += S.gunes(s, 1820, 96, 34, hale="#FFF2C2", hale_r=330, guc=.8)
        for i, (x, y, w) in enumerate([(820, 120, 230), (1180, 92, 280), (1560, 150, 200)]):
            s += S.bulut(s, x, y, w, t * 10 + i, ust="#FFFFFF", alt="#CFE3F1", op=.92)
    uzak = ""
    d, _ = S.dag(s, 980, 2240, ufuk, 1640, 84, t * 7 + 1, renk="#6F9AC2", golge="#4F79A8", bicim="sivri", kar_y=128,
                 kar="#FFFFFF", kar_golge="#C9DAEE", sis="#BFE0F0", isik=-1, sirt=4)
    uzak += d
    d, _ = S.dag(s, -80, 820, ufuk, 320, 196, t * 7 + 2, renk="#8FB4D2", golge="#7099C0", bicim="tepe", sis="#D6ECF5", isik=-1, sirt=2, puruz=5)
    uzak += d
    s += uzak
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 34, 26, t * 7 + 3, "#B7CF7A", "#7FAE52")
    s += tb
    ova = s.lin([(0, "#A9C76B"), (1, "#5F9442")], 0, ufuk + 40, 0, H, kull="userSpaceOnUse", ad="ova")
    s += f'<path d="M0 {ufuk + 52} C500 {ufuk + 40} 1200 {ufuk + 64} 2100 {ufuk + 48} V{H} H0 Z" fill="{ova}"/>'
    for i, (x, h_) in enumerate([(1290, 140), (1322, 165), (1354, 130), (2010, 180), (2046, 150), (2080, 170)]):
        s += S.kavak(s, x, 372, h_, 26, t * 50 + i, renk="#5A9C47")
    s += Y.kumbet(s, 1660, 380, 250, t, tas="#D7A47B", cati="#B9825E")
    for i, x in enumerate((1460, 1840, 1900)):
        s += S.agac(s, x, 372, 30, t * 60 + i, renk="#7DB955", meyve="#E2533D" if i == 1 else None)
    s += S.cimen(1100, 2100, 430, t, renk="#5C9A40", renk2="#86C25A", boy=12, cicek=["#FFFFFF", "#F0A21A", "#E2533D"])
    s += _cerceve_golge(s)
    return _bitir(s)
'''

DOGRULA_PY = '''"""«unite» · sayısal doğrulama ve cevap anahtarı denetimi.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Her görev, kendini dene, hızlı görev, kıssa, meclis, merdiven, imtihan, karma sayfa ve üstad sorusu burada YENİDEN hesaplanır.
  2. Her çoktan seçmeli soruda TEK doğru şık (tek_sik).
  3. Sayfadan okunan işaretler (data-soru / data-dogru) ve Cevaplar sayfasındaki anahtar hesapla aynı mı?
  4. Akçe muhasebesi (toplam 1600) ve kat yaprağı (kat sayfası tek numaralı sağ sayfada, karma sayfa arka yüzünde).
Yardımcılar: yerel-ortak/dogrula_ortak.py (mk, formul, atom_sayisi, yakin, tek_sik, yargi, YARGI_5, NA, M,
kendini_dene_ayni, sifreli_kapi_ayni, celdirici_ayni, robot_ayni, katla_ayni …; TASARIM-SISTEMI.md §16.6).
"""
import json
import os
import re
import sys


def _ortak():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


sys.path.insert(0, _ortak())
from dogrula_ortak import *  # noqa: E402,F401,F403
from cizim import katla as KC  # noqa: E402

BURA = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BURA, "meta.json"), encoding="utf-8") as fp:
    META = json.load(fp)
with open(os.path.join(BURA, "sablon.html"), encoding="utf-8") as fp:
    SABLON = fp.read()


def bolum(n_):
    """sablon.html'de n. sayfanın <section> bloğu (sınıf sırası: "sayfa sNN ek-sınıf")."""
    return re.search(rf'<section class="sayfa s{n_}\\b.*?</section>', SABLON, re.S).group(0)


# ------------------------------------------------------------------ örnek: mol kütlesi ve tek doğru şık
kontrol("örnek: CO2 = 44 g/mol", mk("CO2") == 44)
kontrol("örnek: Mg(OH)2 = 58 g/mol, 5 atom", mk("Mg(OH)2") == 58 and atom_sayisi("Mg(OH)2") == 5)
# İmtihan sorusu örneği (şablondaki ÖRNEK sorular yerine kendi sorunu yaz ve burada hesapla):
# T["I1"] = tek_sik("İmtihan 1", dict(A=.3, B=1.1, C=2.4, D=3.3, E=3.6), lambda v: yakin(v, .3 * atom_sayisi("C3H8")), "D")
# Yargılı soru örneği:
# d = yargi({"I": yakin(6.4 / 32, .2), "II": yakin(.2 * NA, 1.204e23), "III": yakin(.2 * 2, .4)})
# T["I4"] = tek_sik("İmtihan 4", YARGI_5, lambda v: v == d, "E")

# ------------------------------------------------------------------ hesaplanan anahtar (şimdilik şablondaki örnek harfler)
T = {f"I{i + 1}": h for i, h in enumerate("«imtihan»")}
T.update({f"K{i + 1}": h for i, h in enumerate("«kissa»")})
T.update({f"U{i + 1}": h for i, h in enumerate("«ustad»")})
dagilim([T[f"I{i}"] for i in range(1, 13)])
dagilim([T[f"U{i}"] for i in range(1, 7)], harfler="ABCDE")

# ------------------------------------------------------------------ sayfadan okunan işaretler ve anahtar
html = sayfa_oku(__file__)
if html:
    sayfa_isaretleri_ayni(html, T)
    izgara = anahtar_izgarasi(html)
    kontrol(f"Cevaplar sayfasındaki anahtar ızgarası data-dogru işaretleriyle aynı {izgara}",
            izgara == {i: T[f"I{i}"] for i in range(1, 13)})
    for kod, (kisi, satir) in meclis_hukumleri(html).items():
        kontrol(f"{kod}: meclis hükmü işaretli (haklı: {kisi}, satır: {satir})", bool(kisi) and bool(satir))

# ------------------------------------------------------------------ yeni bileşenler (şablondaki ÖRNEK değerler; kendi sorunla değiştir)
# Kat sayfası ({{katla|bag}}): satırlar sahneler_unite.KATLA_BAG, yoksa ortak örnek (cizim/katla.py BAG).
# {{katla|tepkime}} seçilirse KATLA_TEPKIME / KC.TEPKIME; cümle türünde ünite modülünün satırları (9/03 katla_unite.py).
import sahneler_unite as SU  # noqa: E402
KATLA = getattr(SU, "KATLA_BAG", None) or KC.BAG
for b in KATLA:
    urun = KC.duz(b["denklem"][0].split("→")[-1].strip() + b["denklem"][1] + b["denklem"][2])
    kontrol(f"katla {b['kod']}: katlıyken denklemde ürün {urun} = {b['urun']}", urun == b["urun"])
if html:
    katla_ayni(html, {b["kod"]: (b["urun"], b["tur"]) for b in KATLA})
    # Kendini dene: her durakta bir kart; öğretmen cevapları (.ogr) sırayla
    kendini_dene_ayni(html, {f"KD{d['no']}": ["cevap 1", "cevap 2"] for d in META["duraklar"]})
    # Şifreli Kapı: doğru seçenekler sırayla şifreyi yazar; öğretmen kutuları aynı
    sifreli_kapi_ayni(html, "«sifre»")
    # Çeldirici röntgeni (örnek): 23/11 Na+ → p = Z = 11, n = A − Z = 23 − 11, e = 11 − 1 (katyon 1 e− vermiş)
    p, n, e = 11, 23 - 11, 11 - 1
    celdirici_ayni(html, {"CR1": ("C", f"{p}, {n}, {e}")})
    # Robot yanıldı mı?: tek hatalı cümle
    robot_ayni(html, {"RB1": 3})

# ------------------------------------------------------------------ akçe muhasebesi (1600 · Kalfa «kalfa» · Usta «usta» · Üstad «ustad_esik»)
CIP = r'<span class="cip akce">\\+(\\d+)(?: akçe)?</span>'


def cipler(t):
    return [int(v) for v in re.findall(CIP, t)]


for d in META["duraklar"]:
    t = bolum(d["sayfa"])
    ana = t[t.index("<main"):]                       # levhadaki "+N akçe" (durak toplamı) sayılmaz
    hz = 10 * len(re.findall(r"\\{\\{hazine\\|H\\d+\\}\\}", ana))
    kontrol(f"{d['no']}. durak (s.{d['sayfa']}): çipler {cipler(ana)} + hazine {hz} = {d['akce']}; levhada +{d['akce']}",
            sum(cipler(ana)) + hz == d["akce"] and f"+{d['akce']} akçe" in t[:t.index("<main")])
    tuzak = re.search(r'<div class="tuzak">.*?<div class="tuzak-dogru">', ana, re.S)
    kontrol(f"{d['no']}. durak: Tuzak akçe taşımaz, Kendini dene +10", tuzak is not None and "cip akce" not in tuzak.group(0)
            and 'Kendini dene</span><span class="cip akce">+10 akçe</span>' in ana)
kat_s = int(re.search(r'<section class="sayfa s(\\d+) kat">', SABLON).group(1))
hul_s = int(re.search(r"SAYFA (\\d+) · HÜLASA -->", SABLON).group(1))
kontrol(f"kat yaprağı: Hülasa s.{hul_s} → kat sayfası s.{kat_s} tek numaralı (sağ) → karma sayfa s.{kat_s + 1} arka yüzü",
        kat_s % 2 == 1 and hul_s == kat_s - 1 and f'<section class="sayfa s{kat_s + 1} karma">' in SABLON)
bonus = re.search(r"SAYFA (\\d+) · BONUS", SABLON)
kontrol(f"bonus sayfa {'s.' + bonus.group(1) if bonus else 'yok'}: yalnız durak sayısı tekse, Hülasa'dan hemen önce, akçe çipi yok",
        (bonus is not None) == (len(META["duraklar"]) % 2 == 1)
        and (bonus is None or (int(bonus.group(1)) == hul_s - 1 and "cip akce" not in bolum(hul_s - 1))))
kontrol(f"sayfa sayısı {META['sayfa_sayisi']} çift ve şablonla aynı",
        META["sayfa_sayisi"] % 2 == 0 and SABLON.count('<section class="sayfa s') == META["sayfa_sayisi"])
durak = [d["akce"] for d in META["duraklar"]]
yan = dict(hulasa=40, katla=10 * len(KATLA), karma=sum(cipler(bolum(kat_s + 1))), meclis=4 * 30, kissa=4 * 30, anahtar=3 * 40,
           imtihan=12 * 25)
kontrol(f"duraklar {sum(durak)} = 700 · katla {yan['katla']} = 40 · karma {yan['karma']} = 60 + 30 + 30 + 40",
        (sum(durak), yan["katla"], yan["karma"]) == (700, 40, 160))
toplam = sum(durak) + sum(yan.values())
kontrol(f"Ünite toplam akçe {toplam} = 1600 = meta.akce_toplam", toplam == 1600 == META["akce_toplam"])
defter = [int(v) for v in re.findall(r'<td class="n">(\\d+)</td>', bolum(META["sayfa_sayisi"]))]
kontrol(f"final defteri {defter}: kalemler toplamı = TOPLAM = 1600", sum(defter[:-1]) == defter[-1] == 1600)

D.sonuc()
'''

OLC_SH = '''#!/bin/sh
# Taşma özeti: sayfa başına "alan dışı" en alt kenar ve kutu taşmaları (boşsa her şey sığıyor).
# Kullanım: bash uretec/olc.sh          → bütün sayfalar (PDF de yazılır)
#           bash uretec/olc.sh 3 4      → yalnızca 3. ve 4. sayfanın PNG'si
# -X utf8: render.js UTF-8 yazar; Windows'ta python3 boruyu cp1254 okursa "alan dışı" satırları gözden kaçar
cd "$(dirname "$0")/.." && node «render» . "$@" 2>&1 | python3 -X utf8 -c "
import sys,re
mx={}
for l in sys.stdin:
  m=re.match(r'(s\\d+): alan dışı .*?alt=([\\d.]+)',l)
  if m: mx[m.group(1)]=max(mx.get(m.group(1),0),float(m.group(2)))
  elif 'kutu' in l or 'kenar' in l or 'sayfa' in l or 'MB' in l or 'HATA' in l: print(l.strip()[:160])
print('alan dışı (en alt kenar, mm):',mx or 'yok')"
'''

README = """# «sinif». sınıf · «unite» · Yol «yol» «rota» (yerel tasarım)

**İskeletten üretildi** (`yerel-ortak/yeni_unite.py`). Bütün sayfa türleri hazır; içerik, sahneler ve sorular
örnek/yer tutucu metindir. Tasarım sistemi, bileşenler ve kurallar: `«ortak»/TASARIM-SISTEMI.md`
(özellikle §11 “Yeni ünite nasıl yapılır”). Rota ve ortak kurallar: `«ortak»/ROTALAR.md`. Dil ve karakterler:
`kitap/YEREL-KIMLIK.md`. Sayılar: `kitap/YAZIM-REHBERI.md`.

## Komutlar

```sh
cd kitap/«sinif_klasor»/«klasor»
python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh    # unite.html → PDF + onizleme/sNN.png + taşma
node «render» . --hepsi                                                    # + öğretmen, fotokopi, baskı, hazine kartları PDF'leri
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
| `unite.html`, `«klasor».pdf`, `onizleme/` | ÜRETİLİR |

## Sayfa planı («sayfa_sayisi» sayfa · «toplam_akce» akçe)

Akçe: duraklar 700 · Hülasa 40 · Katla 40 · karma sayfa 160 · Meclis, Kıssa, Anahtar 3 × 120 · Büyük İmtihan 300;
Üstad akçesiz. Ahilik: Kalfa «kalfa» · Usta «usta» · Üstad «ustad». Durakta: Kavram + Görev + Hızlı görev + Kendini dene (+10)
+ 2 hazine kartı = durak akçesi; Tuzak ve Hap Bilgi akçe taşımaz. Kat yaprağı: s.«p_kat» (kat sayfası, sağ) + s.«p_kar» (karma, arka yüzü); sıra Hülasa → Katla → Karma.«bonus_not»

| s. | Sayfa | Sahne | Akçe |
|---|---|---|---|
«plan»

## Yapılacaklar

- [ ] `meta.json`: gerçek duraklar (yer, başlık, enlem–boylam), kale ve konumu, nişan adları, hazine kartları, medeniyet, kavramlar; `palet` sınıfa göre hazır («palet»)
- [ ] `sahneler_unite.py`: her durak için bölgeye özel sahne (ROTALAR.md); açılışta istersen bölge panoraması
- [ ] `sablon.html`: içerik; “Yer tutucu” alanlarını doldur; Medeniyetimizden kutuları yalnız doğrulanmış bilgiyle
- [ ] bütün sorular + `data-dogru` / `.ogr` işaretleri (öğretmen baskısı) + Cevaplar sayfası
- [ ] her durakta Kendini dene (2 kısa soru, +10); istersen Hap Bilgi ailesi, Bir bakışta, konu karakterleri (TASARIM-SISTEMI.md §16)
- [ ] kat sayfası: ünitenin 4 satırı (`sahneler_unite.KATLA_BAG` / `KATLA_TEPKIME`, ya da cümle türü için ünite modülü: 9/03 `katla_unite.py`)
- [ ] karma sayfa: Şifreli Kapı için ünitenin kelimesi (yanlış harfler kelime kurmamalı), Çeldirici Röntgeni, Robot yanıldı mı?, Heybe (önceki yollardan)
- [ ] uygun ünitede 3B sayfası (bonus, akçesiz; `meta.json` `uc_boyut`, TASARIM-SISTEMI.md §16.5 · kat yaprağının tek/çift sırası korunmalı)
- [ ] `dogrula.py`: her sayıyı yeniden hesapla; `SONUÇ: hepsi doğru` (akçe toplamı 1600)
- [ ] `node «render» . --hepsi`: beş PDF; `pdffonts … | grep -c "Type 3"` → 0
"""

GITIGNORE = """# ara dosyalar (render.js --hepsi yeniden üretir)
unite-fotokopi.html
hazine-kartlari.html
onizleme/varyant/
__pycache__/
"""


# ------------------------------------------------------------------ üretim

KIVRIM = ('<svg viewBox="0 0 300 20" preserveAspectRatio="none"><path d="M4 12 C40 2 70 2 100 11 S160 20 200 10 S270 2 296 10" '
          'fill="none" stroke="#F0A21A" stroke-width="9" stroke-linecap="round"/></svg>')


def dev_baslik(unite):
    """Açılış dev başlığı (.acilis sol sütunu ≈ 100 mm genişlik, başlığa ≈ 17 mm yükseklik kalır).
    Baloo 800'de harf başına ≈ 0,49 em → tek satırda punto ≈ 578 / harf sayısı.
    ≤ 11 harf: 54 pt (Mol gibi) · ≤ 22 harf: tek satır, küçülerek (en az 26 pt) · daha uzun: iki satır, en çok 26 pt."""
    kel = unite.split(" ")
    if len(kel) == 1:
        stil = "" if len(unite) <= 11 else f' style="font-size:{max(26, 578 // len(unite))}pt"'
        return f'<h1 class="dev-baslik"{stil}><span class="kav">{KIVRIM}{unite}</span></h1>'
    uz = len(unite)
    if uz <= 22:
        stil = "" if uz <= 11 else f' style="font-size:{max(26, 578 // uz)}pt"'
        return f'<h1 class="dev-baslik"{stil}><span class="mol">{kel[0]}</span> <span class="kav">{KIVRIM}{" ".join(kel[1:])}</span></h1>'
    k = min(range(1, len(kel)), key=lambda i: max(len(" ".join(kel[:i])), len(" ".join(kel[i:]))))
    s1, s2 = " ".join(kel[:k]), " ".join(kel[k:])
    pt = min(26, 578 // max(len(s1), len(s2)))
    return (f'<h1 class="dev-baslik" style="font-size:{pt}pt;line-height:.94"><span class="mol">{s1}</span><br>'
            f'<span class="kav">{KIVRIM}{s2}</span></h1>')


def siklar(dogru, cls="sik"):
    return "".join(f'<div class="{cls}"{" data-dogru" if h == dogru else ""}><b>{h}</b>Seçenek {h}</div>' for h in "ABCDE")


def oy(dogru):
    return "".join(f'<div{" data-dogru" if h == dogru else ""}><b>{h}</b><span>sayı</span><em>%__</em></div>' for h in "ABCDE")


def uret(a):
    sinif = 9 if a.sinif_klasor.startswith("9") else 10
    n = a.durak
    if n not in DURAK_AKCE:
        raise SystemExit("--durak 4, 5 ya da 6 olmalı")
    hedef = os.path.join(a.kok, a.sinif_klasor, a.klasor)
    if os.path.exists(hedef):
        raise SystemExit(f"klasör zaten var, dokunmuyorum: {hedef}")
    uretec = os.path.join(hedef, "uretec")
    ortak_rel = os.path.relpath(ORTAK, hedef).replace(os.sep, "/")
    render = f"{ortak_rel}/render.js"
    rota_k = a.rota.split(" ")
    hud = " ".join(rota_k[:-1] + [rota_k[-1].replace("I", "ı").replace("İ", "i").lower()]) if len(rota_k) > 1 else a.rota
    kale = a.kale or "Kale"
    kisa = a.unite.split(" ")[0]

    # sayfa sırası · kat yaprağı kuralı: kat sayfası (Katla) kitapta TEK numaralı sağ sayfa, karma sayfa onun arka yüzü
    # (hemen sonraki çift sayfa; TASARIM-SISTEMI.md §16.4). Sıra her ünitede 9/03 pilotu gibi Hülasa → Katla → Karma.
    # Ünite tek numaralı sayfada başlar: durak sayısı tekse Hülasa'dan önce akçesiz bonus sayfa ("Bir bakışta") girer.
    P_DURAK = list(range(2, 2 + n))
    blok = (["bonus"] if n % 2 else []) + ["hulasa", "katla", "karma"]
    sira = ["acilis"] + ["durak"] * n + blok + ["meclis", "kissa", "merdiven", "imtihan1", "imtihan2", "ustad", "cevaplar", "final"]
    P = {tur: no for no, tur in enumerate(sira, 1) if tur != "durak"}
    p_bon, p_hul, p_kat, p_kar = P.get("bonus"), P["hulasa"], P["katla"], P["karma"]
    p_mec, p_kis, p_mrd = P["meclis"], P["kissa"], P["merdiven"]
    p_im1, p_im2, p_ust, p_cev, p_fin = P["imtihan1"], P["imtihan2"], P["ustad"], P["cevaplar"], P["final"]
    toplam = len(sira)
    assert p_kat % 2 == 1 and p_kar == p_kat + 1 == p_hul + 2, "Hülasa → Katla (tek numaralı) → Karma (arka yüzü) olmalı"
    assert toplam % 2 == 0, "sayfa sayısı çift (sonraki ünite yine tek sayfada başlar)"

    # akçe: sayfa başına en çok akçe → HUD çubuğu (o sayfanın başına kadar alınabilecek en çok akçe / toplam)
    akce = DURAK_AKCE[n]
    kalfa, usta, ustad = AHILIK
    sayfa_akce = {no: (akce[no - 2] if tur == "durak" else SAYFA_AKCE.get(tur, 0)) for no, tur in enumerate(sira, 1)}
    assert sum(sayfa_akce.values()) == AKCE_TOPLAM, sum(sayfa_akce.values())
    bar, birikim = {}, 0
    for no in range(1, toplam + 1):
        bar[no] = round(100 * birikim / AKCE_TOPLAM)
        birikim += sayfa_akce[no]

    def durak_cip(a_):
        """Durak çipleri: Kavram + Görev + Hızlı görev = durak akçesi − Kendini dene (10) − 2 hazine kartı (20)."""
        kalan = a_ - 30
        taban = kalan // 3 // 10 * 10
        return taban, kalan - 2 * taban, taban          # kavram, görev, hızlı görev (100 → 20/30/20 · 120 → 30/30/30)

    sayfa = {1: ("Yola çıkış", f"{hud} · yola çıkış")}
    for i, p in enumerate(P_DURAK):
        sayfa[p] = (f"{i + 1}. durak · <b>Yer {i + 1}</b>", f"{i + 1}. durak · Konu")
    sayfa.update({p_hul: ("Hülasa · <b>Yer</b>", "Hülasa · özet"), p_kat: ("Hülasa · <b>Katla</b>", "Katla sayfası · bağ oluşsun"),
                  p_kar: ("Hülasa · <b>Karma</b>", "Karma sayfa · kapıyı aç"), p_mec: ("Yan yol · <b>Yer</b>", "Yan yol 1 · Meclis: kim haklı?"),
                  p_kis: ("Yan yol · <b>Yer</b>", "Yan yol 2 · Kıssalar"), p_mrd: ("Yan yol · <b>Yer</b>", "Yan yol 3 · Anahtar merdiveni"),
                  p_im1: (f"<b>{kale}</b> · 1/2", "Büyük İmtihan · 1. bölüm"), p_im2: (f"<b>{kale}</b> · 2/2", "Büyük İmtihan · 2. bölüm"),
                  p_ust: ("<b>Üstad</b> · bonus", "Üstad soruları · bonus"), p_cev: ("<b>Cevaplar</b>", "Cevaplar ve çözümler"),
                  p_fin: ("<b>Final</b>", "Final · akçe rayı ve unvan")})
    simdi = {1: -1}
    for i, p in enumerate(P_DURAK):
        simdi[p] = i
    simdi.update({p_hul: n, p_kat: n, p_kar: n, p_mec: n + 1, p_kis: n + 2, p_mrd: n + 3, p_im1: n + 4, p_im2: n + 4,
                  p_ust: n + 5, p_cev: n + 5, p_fin: n + 5})
    if p_bon:                                           # bonus sayfa: son durağın noktasında, çubuk artmaz
        sayfa[p_bon] = ("Bonus · <b>Bir bakışta</b>", "Bonus · yol bir bakışta")
        simdi[p_bon] = n - 1

    # meta.json (örnek değerler: DOLDUR)
    me, mb = a.merkez
    ofs = [(-.30, -.72), (-.42, -.16), (-.10, .22), (.20, -.30), (.34, .38), (.06, .80)]
    duraklar = [{"no": i + 1, "yer": f"Yer {i + 1}", "baslik": f"{i + 1}. durak başlığı", "enlem": round(me + ofs[i][0], 3),
                 "boylam": round(mb + ofs[i][1], 3), "sayfa": P_DURAK[i], "akce": akce[i]} for i in range(n)]
    nisanlar = [{"ad": f"{i + 1}. Durak Nişanı", "ikon": IKON[i], "renk": NISAN_RENK[i], "aciklama": f"{i + 1}. durak · konu"} for i in range(n)]
    nisanlar += [{"ad": "Kale Kapısı", "ikon": "kale", "renk": "keh", "aciklama": "İmtihan · 10+ doğru"},
                 {"ad": "Üstad Mührü", "ikon": "ustad", "renk": "laj", "aciklama": "Üstad · 6/6 doğru", "bonus": True}]
    hazine = []
    for i in range(n):
        hazine.append({"kod": f"H{2 * i + 1}", "baslik": "Kart başlığı · +10 akçe", "formul": "a = b · c", "not": "Kısa not", "durak": i + 1})
        hazine.append({"kod": f"H{2 * i + 2}", "renk": "gol", "baslik": "Kart başlığı · +10 akçe", "formul": "x = y / z", "durak": i + 1})
    palet = PALET[sinif] if a.palet is None else (None if a.palet == "yok" else a.palet)
    meta = {
        "sinif": sinif, "yol": a.yol, "rota": a.rota, "unite": a.unite, "klasor": a.klasor, "tema": a.tema, "bolge": a.bolge,
        "merkez": {"enlem": me, "boylam": mb}, "duraklar": duraklar, "kale": kale,
        "kale_konum": {"enlem": round(me - .22, 3), "boylam": round(mb + .95, 3)},
        "nisanlar": nisanlar, "hazine": hazine, "medeniyet": [], "kavramlar": [{"terim": "terim", "tanim": "tanım"}],
        "sayfa_sayisi": toplam,
    }
    if palet:
        meta["palet"] = palet
    meta["akce_toplam"] = AKCE_TOPLAM

    # sablon.html (sayfa sırasıyla)
    esik = dict(kalfa=kalfa, usta=usta, ustad=ustad, kalfa_1=kalfa - 1, usta_1=usta - 1, ustad_1=ustad - 1, toplam_akce=AKCE_TOPLAM)
    s = {1: doldur(ACILIS, yol=a.yol, rota=a.rota, sinif=sinif, dev_baslik=dev_baslik(a.unite), n=n, ilk_yer="Yer 1", kale=kale, **esik)}
    for i, p in enumerate(P_DURAK):
        gok = GOK[i]
        kav, gor, hiz = durak_cip(akce[i])
        s[p] = doldur(DURAK, p=p, i=i + 1, YER=f"YER {i + 1}", yer=f"Yer {i + 1}", gok=gok, saat=SAAT[gok], akce=akce[i],
                      nisan=nisanlar[i]["ad"], h1=2 * i + 1, h2=2 * i + 2, a_kav=kav, a_gor=gor, a_hiz=hiz,
                      yan_kutu=MEDENIYET if i in (1, 3) else KIYIDAN)
    muh = "\n".join(f'        <div class="satir"><span>Kazanım cümlesi {k} (… yapabilirim).</span>{{{{cay|0|b}}}}{{{{cay|0|b}}}}{{{{cay|0|b}}}}</div>' for k in range(1, 7))
    if p_bon:
        kutular = [doldur(BAKISTA, i=i + 1) for i in range(n)] + ([ALTIN_KURAL] if n % 3 else [])
        s[p_bon] = doldur(BONUS, p=p_bon, p_kat=p_kat, bakista="\n".join(kutular))
    s[p_hul] = doldur(HULASA, p=p_hul, kisa=kisa, muhasebe=muh)
    s[p_kat] = doldur(KATLA, p=p_kat, p_arka=p_kar)

    def sk(k):
        dogru, harfler = ORNEK_SK[k - 1]
        d = (k - 1) % n + 1
        sec = "".join(f'<li{" data-dogru" if h == dogru else ""}><b>{h}</b>{(j if k == 3 else 10 * j) if k in (3, 4) else "seçenek"}</li>'
                      for j, h in enumerate(harfler, 1))
        return doldur(KARMA_SK, k=k, yol=a.yol, d=d, sinif=" bes" if k in (3, 4) else "", secenek=sec)
    kutu = "".join(f'<span><i>{k}</i><span class="ogr">{h}</span></span>' for k, h in enumerate(ORNEK_SIFRE, 1))
    heybe_cip = [(f"1 yol önce · Yol {a.yol - 1}" if a.yol > 1 else "Bu yoldan · 1. durak", ""),
                 (f"2 yol önce · Yol {a.yol - 2}" if a.yol > 2 else "Bu yoldan · 2. durak", " y3"),
                 (f"Bu yoldan · {max(1, n - 2)}. durak", " y5"), (f"Bu yoldan · {n}. durak", " y5")]
    heybe = "\n".join(doldur(HEYBE_SOR, k=k, cip=c, sinif=cls) for k, (c, cls) in enumerate(heybe_cip, 1))
    s[p_kar] = doldur(KARMA, p=p_kar, p_on=p_kat, yol=a.yol, sifre=ORNEK_SIFRE, sifre_kutu=kutu,
                      sk_1_3="\n".join(sk(k) for k in (1, 2, 3)), sk_4_6="\n".join(sk(k) for k in (4, 5, 6)), heybe=heybe)
    renkler = [("", "gol", "A", "Ahmet"), (" mer", "mer", "Z", "Zehra"), (" kob", "kob", "M", "Mehmet Emin"), (" keh", "keh", "R", "Rabia")]
    s[p_mec] = doldur(MECLIS, p=p_mec, cevap_s=p_cev, kartlar="\n".join(doldur(MECLIS_KART, k=k + 1, renk=r[0], renk2=r[1], harf=r[2], ad=r[3])
                                                                       for k, r in enumerate(renkler)))
    kr = ["", " keh", " kob", " mer"]
    s[p_kis] = doldur(KISSA, p=p_kis, kartlar="\n".join(doldur(KISSA_KART, k=k + 1, renk=kr[k], siklar=siklar(ORNEK_KISSA[k])) for k in range(4)))
    s[p_mrd] = doldur(MERDIVEN, p=p_mrd, kale=kale, kartlar="\n".join(doldur(MERDIVEN_KART, k=k) for k in (1, 2, 3)))
    s[p_im1] = doldur(IMTIHAN1, p=p_im1, KALE=tr_buyuk(kale), kale=kale,
                      kartlar="\n".join(doldur(MESVERET, k=k, oy=oy(ORNEK_IMTIHAN[k - 1])) for k in range(1, 7)))
    s[p_im2] = doldur(IMTIHAN2, p=p_im2, kartlar="\n".join(doldur(MESVERET, k=k, oy=oy(ORNEK_IMTIHAN[k - 1])) for k in range(7, 13)))
    s[p_ust] = doldur(USTAD, p=p_ust, kartlar="\n".join(doldur(USTAD_KART, k=k, siklar=siklar(ORNEK_USTAD[k - 1])) for k in range(1, 7)))
    anahtar = "\n".join(f'        <div><i>{k}</i><b>{ORNEK_IMTIHAN[k - 1]}</b><small>{(k - 1) % n + 1}. durak</small></div>' for k in range(1, 13))
    im_c = "\n".join(f'          <p class="c"><b>{k} · {ORNEK_IMTIHAN[k - 1]}</b> Kısa çözüm.</p>' for k in range(1, 13))
    ki_c = "\n".join(f'          <p class="c"><b>{k} · {ORNEK_KISSA[k - 1]}</b> Kısa çözüm.</p>' for k in range(1, 5))
    us_c = "\n".join(f'          <p class="c"><b>{k} · {ORNEK_USTAD[k - 1]}</b> Kısa çözüm.</p>' for k in range(1, 7))
    ki_ck = "".join(f'<span class="ck">{k} {ORNEK_KISSA[k - 1]}</span>' for k in range(1, 5))
    tekrar = "".join(f'<li><b>{i + 1}. durak (s.{{{{sayfa|{p}}}}})</b> · konu → soru …</li>' for i, p in enumerate(P_DURAK))
    s[p_cev] = doldur(CEVAPLAR, p=p_cev, anahtar=anahtar, imtihan_cozum=im_c, kissa_cozum=ki_c, ustad_cozum=us_c, kissa_ck=ki_ck,
                      tekrar=tekrar, sifre=ORNEK_SIFRE)
    kalem = {"hulasa": "Hülasa · muhasebe", "katla": "Katla sayfası", "karma": "Karma sayfa · kapıyı aç", "meclis": "Yan yol · Meclis",
             "kissa": "Yan yol · Kıssalar", "merdiven": "Yan yol · Anahtar merdiveni"}
    satirlar = [(f"{i + 1}. durak · Yer {i + 1}", akce[i]) for i in range(n)]
    satirlar += [(kalem[t], SAYFA_AKCE[t]) for t in sira if t in kalem]
    satirlar.append((f"{kale} · Büyük İmtihan", SAYFA_AKCE["imtihan1"] + SAYFA_AKCE["imtihan2"]))
    assert sum(v for _, v in satirlar) == AKCE_TOPLAM
    defter = "\n".join(f'          <tr><td>{ad}</td><td class="n">{v}</td><td class="k"><span></span></td></tr>' for ad, v in satirlar)
    s[p_fin] = doldur(FINAL, p=p_fin, hud=hud, yol=a.yol, yol_sonra=a.yol + 1, kale=kale, defter=defter,
                      defter_sinif="defter sik" if len(satirlar) + 2 >= 13 else "defter", **esik)
    sablon = doldur(BAS, sinif=sinif, unite=a.unite, rota=a.rota, stil=f"{ortak_rel}/stil.css") + "".join(s[k] for k in sorted(s)) + SON
    assert sorted(s) == list(range(1, toplam + 1))

    # kur.py
    sayfa_satir = "\n".join(f'    {k}: ({v[0]!r}, {v[1]!r}, {bar[k]}),' for k, v in sorted(sayfa.items()))
    simdi_satir = ", ".join(f"{k}: {v}" for k, v in sorted(simdi.items()))
    kur = doldur(KUR_PY, unite=a.unite, rota=a.rota, render=render, sayfa=sayfa_satir, simdi=simdi_satir, n=n, tam=n + 5,
                 toplam_akce=AKCE_TOPLAM, p_kat=p_kat, p_kar=p_kar)

    plan = [("1", "Yola çıkış · tur haritası, nişanlar, yol arkadaşları, hedefler, Ahilik eşikleri", "{{rota-haritasi}}")]
    for i, p in enumerate(P_DURAK):
        plan.append((str(p), f"{i + 1}. durak · sohbet, kavram, hazine, görev, hızlı görev, tuzak, kendini dene"
                     + (", Medeniyetimizden" if i in (1, 3) else ""), f"ornek_sahne ({GOK[i]})"))
    plan += [(str(p_hul), "Hülasa · 6 özet kart, hazine sandığı, muhasebe", "ornek_sahne (altin)"),
             (str(p_kat), "Kat sayfası (sağ) · Katla, bağ oluşsun! (4 satır, ortak tür)", r"{{katla\|bag}}"),
             (str(p_kar), "Karma sayfa (kat sayfasının arka yüzü) · Şifreli Kapı, Çeldirici Röntgeni, Robot, Heybe", "— (3 sütun)"),
             (str(p_mec), "Yan yol 1 · Meclis (4 hatalı çözüm)", "ornek_sahne"), (str(p_kis), "Yan yol 2 · Kıssalar (4 bağlam sorusu)", "ornek_sahne"),
             (str(p_mrd), "Yan yol 3 · Anahtar merdiveni (3 × 3)", "ornek_sahne"), (str(p_im1), "Büyük İmtihan 1–6", "ornek_sahne (b62)"),
             (str(p_im2), "Büyük İmtihan 7–12 + skor", "ornek_sahne (b30)"), (str(p_ust), "Üstad soruları (6, bonus)", "ustad_bandi"),
             (str(p_cev), "Cevaplar ve çözümler", "ornek_sahne (gece)"), (str(p_fin), "Final · akçe rayı, unvanlar, nişan sayımı", "{{final}}")]
    if p_bon:
        plan.append((str(p_bon), "Bonus · Bir bakışta (her durak 3 madde; akçesiz; uygun ünitede yerine 3B sayfası)", "ornek_sahne (alaca)"))
    plan.sort(key=lambda r: int(r[0]))
    bonus_not = (f" Durak sayısı tek: s.{p_bon} akçesiz bonus sayfa (Bir bakışta; uygun ünitede yerine 3B sayfası), Katla tek sayfada kalsın diye."
                 if p_bon else "")
    readme = doldur(README, sinif=sinif, unite=a.unite, yol=a.yol, rota=a.rota, ortak=ortak_rel, sinif_klasor=a.sinif_klasor, klasor=a.klasor,
                    render=render, sayfa_sayisi=toplam, p_kat=p_kat, p_kar=p_kar, palet=palet or "yok: Van Gölü renkleri", **esik,
                    bonus_not=bonus_not,
                    plan="\n".join(f"| {s_} | {i} | `{c}` | {sayfa_akce[int(s_)] or '–'} |" for s_, i, c in plan))
    dogrula = doldur(DOGRULA_PY, unite=a.unite, imtihan=ORNEK_IMTIHAN, kissa=ORNEK_KISSA, ustad=ORNEK_USTAD, sifre=ORNEK_SIFRE,
                     kalfa=kalfa, usta=usta, ustad_esik=ustad)

    os.makedirs(uretec)
    yaz = {
        os.path.join(hedef, "README.md"): readme,
        os.path.join(hedef, ".gitignore"): GITIGNORE,
        os.path.join(uretec, "sablon.html"): sablon,
        os.path.join(uretec, "meta.json"): json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        os.path.join(uretec, "kur.py"): kur,
        os.path.join(uretec, "sahneler_unite.py"): doldur(SAHNELER_PY, unite=a.unite),
        os.path.join(uretec, "dogrula.py"): dogrula,
        os.path.join(uretec, "olc.sh"): doldur(OLC_SH, render=render),
    }
    for yol, metin in yaz.items():
        with open(yol, "w", encoding="utf-8") as fp:
            fp.write(metin)
    for ad in ("kur.py", "olc.sh", "dogrula.py"):
        os.chmod(os.path.join(uretec, ad), 0o755)
    print(f"İskelet hazır: {hedef}  ({toplam} sayfa, {n} durak, {AKCE_TOPLAM} akçe, kat yaprağı s.{p_kat}–{p_kar}, palet: {palet or 'yok'})")
    print("Sıradaki adım:")
    print(f"  cd {os.path.relpath(hedef)} && python3 uretec/kur.py && python3 uretec/dogrula.py && bash uretec/olc.sh")
    print("  sonra uretec/meta.json → duraklar, nişanlar, hazine kartları; uretec/sahneler_unite.py → sahneler; uretec/sablon.html → içerik")
    return hedef


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):          # Windows konsolu (cp1254) "→" yazamaz: iskelet yazılmışken çökmesin
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description="Yeni ünite iskeleti (yerel tasarım)")
    p.add_argument("sinif_klasor", help="9-sinif-yerel ya da 10-sinif-yerel")
    p.add_argument("klasor", help="NN-unite-adi (ör. 01-gunluk-hayatta-kimya)")
    p.add_argument("--yol", type=int, required=True)
    p.add_argument("--rota", required=True, help='ör. "İznik–Bursa Yolu"')
    p.add_argument("--unite", required=True, help='ör. "Günlük Hayatta Kimya"')
    p.add_argument("--durak", type=int, default=5, help="durak sayısı: 4, 5 ya da 6")
    p.add_argument("--tema", default="Tema · Bölüm", help='künyedeki tema/bölüm, ör. "Tema 1 · Bölüm 1"')
    p.add_argument("--bolge", default="", help="bölge adı (meta.json)")
    p.add_argument("--kale", default="", help="Büyük İmtihan kalesi, ör. \"Bursa Hisarı\"")
    p.add_argument("--merkez", default="39.0,35.0", help="örnek durakların yerleşeceği merkez: enlem,boylam")
    p.add_argument("--palet", default=None, choices=["cini-toprak", "gol-rasathane", "yok"],
                   help='meta.json "palet" (varsayılan sınıfa göre: 9 → cini-toprak "Çini ve Toprak", 10 → gol-rasathane '
                        '"Göl ve Rasathane"; yok → alan yazılmaz, Van Gölü renkleri)')
    p.add_argument("--kok", default=KITAP, help="kitap klasörü (deneme için başka yer verilebilir)")
    a = p.parse_args(argv)
    if a.sinif_klasor not in ("9-sinif-yerel", "10-sinif-yerel"):
        print("UYARI: sınıf klasörü 9-sinif-yerel ya da 10-sinif-yerel olmalı", file=sys.stderr)
    a.merkez = tuple(float(v) for v in a.merkez.split(","))
    return uret(a)


if __name__ == "__main__":
    main()
