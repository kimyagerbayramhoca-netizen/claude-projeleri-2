"""Kimya Rotası · yerel illüstrasyon kütüphanesi (kodla üretilen SVG).

Modüller (bağımlılık sırasıyla):
  temel       Svg sınıfı (kimlik ad alanı, gradyan/klip/maske/desen), yol kurucuları, renk karıştırma, gürültü
  renkler     palet tokenları (stil.css :root ile aynı) + atom renkleri/yarıçapları
  sahne       manzara parçaları: gökyüzü, güneş, ay, yıldız, bulut, dağ, tepe, göl, yansıma, ağaç, kavak, çimen,
              sazlık, kaya, martı, inci kefali, sıçrama, tekne, feribot, ev
  yapilar     simge yapılar ve nesneler: kümbet, Ahlat mezar taşı, Van Kalesi, kıyı kalesi, iskele, fener, şelale,
              gökkuşağı, asma köprü, semaver, çay bardağı, çadır, koyun, obsidyen, el-Hâzinî terazisi, okul terazisi
  karakter    Pamuk / Elif / Yusuf / Zeynep Hoca pozları ve avatarları (<symbol> kütüphanesi), akçe, Türk bayrağı
  molekul     3B top-çubuk moleküller, izotop çekirdekleri, NaCl kristali
  sus         çini şeritleri, zemin geçmesi, tezhip köşebendi, kilim, mühürler, rozetler, nişanlar, çay bardağı, ikonlar
  infografik  sayısal bilgi grafikleri (Avogadro cetveli, bor madalyonları, mol haritası, karışım kapları …)
  sahneler    sayfa sahneleri (başlık bantları, açılış panoraması, kale, final) = yukarıdaki parçaların birleşimi
  ebru        matematiksel ebru (marmorlama) → JPEG doku
  konu_karakterleri  atom modelleri, tanecikler, fotonlar, gaz tanecikleri (kk-* <symbol>; yalnız kullanılınca gömülür)
  hap_bilgi   Hap Bilgi ailesi ikonları, metin içi ok, sıklık noktaları
  katla       kat sayfaları (fontTools ile ölçülü yazı), köşe sineması kareleri, köşeyi katla, karma sayfa ikonları
  uc_boyut    3B anaglif motoru (numpy + PIL; PNG üretir) ve ünite resim önbelleği · gozluk: gözlük sayfası çizimleri

Bütün fonksiyonlar SVG METNİ döndürür; gradyan/klip tanımları verilen Svg nesnesinin <defs>'ine yazılır.
Her çizim kendi önekini (onek) taşır: aynı HTML'de yüzlerce satır içi SVG'nin kimlikleri çakışmaz.
"""
