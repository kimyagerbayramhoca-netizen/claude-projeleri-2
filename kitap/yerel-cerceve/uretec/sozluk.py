"""Kavram sözlüğü: klasik ünitelerin (9-sinif/*, 10-sinif/*) Kavram kutularındaki anahtar terimler, ÖZGÜN kısa tanımlarla.

Hazır ünitenin meta.json "kavramlar" listesi varsa o ünite için o kullanılır (ünitenin kendi tanımı önceliklidir) ve
buradaki listeyle birleştirilir. Sıralama Türkçe alfabeyle (veri.turkce_anahtar). Her terimin yanında Yol numarası durur.
"""
import math
import os
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
if BURA not in sys.path:
    sys.path.insert(0, BURA)

import veri as V  # noqa: E402

KAVRAMLAR = {
    (9, 1): [("madde", "Kütlesi ve hacmi olan, taneciklerden oluşan her şey."),
             ("kimya", "Maddenin yapısını, özelliklerini, etkileşimlerini ve dönüşümlerini inceleyen bilim."),
             ("asit", "Suda çözünce H⁺ (H₃O⁺) iyonu derişimini artıran madde."),
             ("baz", "Suda çözünce OH⁻ iyonu derişimini artıran madde."),
             ("pH", "Çözeltinin ne kadar asidik ya da bazik olduğunu gösteren sayı; 25 °C’de 7 nötrdür."),
             ("bağımsız değişken", "Deneyde araştırmacının bilerek değiştirdiği tek etken."),
             ("bağımlı değişken", "Bağımsız değişkene bağlı olarak ölçülen sonuç."),
             ("kontrol değişkeni", "Bütün denemelerde aynı tutulan etken."),
             ("nitel analiz", "Örnekte hangi maddelerin bulunduğunu belirleyen analiz."),
             ("nicel analiz", "Örnekteki bir maddenin ne kadar olduğunu ölçen analiz."),
             ("polimer", "Küçük birimlerin çok kez tekrarlanmasıyla oluşan dev molekül; doğal ya da sentetik olabilir.")],
    (9, 2): [("laboratuvar", "Deney ve ölçümlerin kontrollü koşullarda yapıldığı, araç gereçle donatılmış çalışma yeri."),
             ("kişisel koruyucu donanım (KKD)", "Çalışanı sıçrama, ısı ve zararlı buhardan koruyan önlük, gözlük, eldiven, maske."),
             ("güvenlik işareti", "Yapılması ya da kaçınılması gerekeni yazısız anlatan resimli işaret."),
             ("tehlike piktogramı", "Ambalajda maddenin nasıl zarar verebileceğini gösteren kırmızı çerçeveli simge."),
             ("GHS", "Kimyasalları sınıflandırıp etiketlemek için kullanılan uluslararası sistem; dokuz piktogramı vardır."),
             ("çeker ocak", "Zararlı gaz ve buharı ortamdan uzaklaştıran havalandırmalı laboratuvar dolabı."),
             ("hassas ölçüm", "Pipet, büret, balon joje gibi kesin hacim veren araçlarla yapılan ölçüm.")],
    (9, 3): [("teori (kuram)", "Bir olayı açıklayıp sonuçlarını öngören, deneylere dayalı kapsamlı açıklama."),
             ("model", "Bir yapıyı ya da teoriyi temsil eden çizim, benzetme veya matematiksel ifade."),
             ("atom numarası", "Çekirdekteki proton sayısı; elementin kimliğini belirler."),
             ("izotop", "Proton sayısı aynı, nötron sayısı farklı atomlar."),
             ("temel hâl", "Elektronların en düşük enerjili düzeylerde bulunduğu durum."),
             ("uyarılmış hâl", "Enerji soğuran elektronun üst düzeye çıktığı kararsız durum; dönerken ışık yayılır."),
             ("orbital", "Elektronun bulunma olasılığının yüksek olduğu bölge (s, p, d, f)."),
             ("değerlik elektronu", "Atomun en dış enerji düzeyindeki, tepkimelere katılan elektronlar."),
             ("küresel simetri", "Dizilimi tam ya da yarı dolu orbitalle biten taneciğin dengeli yük dağılımı.")],
    (9, 4): [("periyodik yasa", "Atom numarasına göre dizilen elementlerin özelliklerinin düzenli aralıklarla tekrarlanması."),
             ("periyot", "Periyodik tablonun yatay satırı; satırdaki atomların katman sayısı aynıdır."),
             ("grup", "Periyodik tablonun dikey sütunu; aynı gruptakilerin kimyasal özellikleri benzerdir."),
             ("blok", "Dizilimde en son yazılan orbitalin türü: s, p, d ya da f."),
             ("geçiş elementi", "Tablonun d blokunda (B gruplarında) yer alan metal."),
             ("iç geçiş elementi", "f blokundaki lantanit ve aktinitler."),
             ("iyon", "Elektron vermiş ya da almış, yüklü atom veya atom grubu."),
             ("katyon", "Pozitif yüklü iyon."),
             ("anyon", "Negatif yüklü iyon."),
             ("yarı metal", "Özellikleri metal ile ametal arasında olan element: B, Si, Ge, As, Sb, Te."),
             ("soy gaz", "18. grup (8A) elementleri; dış katmanları dolu olduğundan tepkimeye pek girmezler.")],
    (9, 5): [("atom yarıçapı", "Atomun büyüklüğü; grupta aşağı artar, periyotta sağa doğru genellikle azalır."),
             ("izoelektronik", "Elektron sayısı aynı olan tanecikler; proton sayısı çok olan daha küçüktür."),
             ("iyonlaşma enerjisi", "Gaz hâlindeki atom ya da iyondan bir elektron koparmak için gereken en az enerji."),
             ("ardışık iyonlaşma enerjisi", "Elektronlar sırayla koparılırken her adımda gereken enerji; iç katmanda büyük sıçrar."),
             ("endotermik", "Gerçekleşmek için dışarıdan enerji alan olay; iyonlaşma böyledir."),
             ("elektronegatiflik", "Atomun bağdaki ortak elektronları kendine çekme yeteneği; birimsiz bir ölçek."),
             ("metalik karakter", "Atomun elektron verip katyon oluşturma eğilimi."),
             ("ametalik karakter", "Atomun elektron alma ya da bağ elektronlarını kendine çekme eğilimi.")],
    (9, 6): [("kimyasal bağ", "Atomları ya da iyonları bir arada tutan güçlü etkileşim."),
             ("iyonik bağ", "Zıt yüklü iyonlar arasındaki elektrostatik çekim."),
             ("kovalent bağ", "Atomların elektronlarını ortaklaşa kullanmasıyla oluşan bağ."),
             ("metalik bağ", "Metal katyonları ile aralarında serbestçe dolaşan elektron denizi arasındaki çekim."),
             ("Lewis yapısı", "Sembolün çevresine değerlik elektronlarının nokta olarak yazıldığı gösterim."),
             ("dipol", "Bir ucu kısmen pozitif, öbür ucu kısmen negatif olan bağ ya da molekül."),
             ("polar molekül", "Yük dağılımı simetrik olmayan, kalıcı dipolü olan molekül."),
             ("apolar molekül", "Yük dağılımı dengeli, dipol momenti sıfır olan molekül.")],
    (9, 7): [("iyonik bileşik", "Metal ya da amonyum iyonu içeren; formülü iyonların en basit sayı oranını veren bileşik."),
             ("moleküler bileşik", "Yalnız ametallerden oluşan; formülü moleküldeki gerçek atom sayılarını veren bileşik."),
             ("çok atomlu iyon (kök)", "Birlikte yük taşıyan atom grubu; bileşikte tek parça gibi davranır (NO₃⁻, NH₄⁺)."),
             ("amonyum", "En önemli çok atomlu katyon: NH₄⁺."),
             ("-at / -it eki", "Aynı ametalin oksijence zengin anyonu -at, bir oksijen eksiği -it alır: nitrat, nitrit."),
             ("Romen rakamı (adlandırmada)", "Birden çok yük alabilen metalin iyon yükü: demir(III) klorür."),
             ("sayı ön eki", "Moleküler bileşik adında atom sayısını gösteren mono-, di-, tri-…: karbon dioksit."),
             ("-ik asit", "Oksijenli asidin adı anyondan türer: sülfat → sülfürik asit."),
             ("yaygın ad", "Bileşiğin gündelik adı: tuz ruhu (HCl), kezzap (HNO₃), zaç yağı (H₂SO₄).")],
    (9, 8): [("yoğun faz", "Taneciklerin birbirine çok yakın olduğu katı ve sıvı hâl."),
             ("iyon–dipol etkileşimi", "Bir iyon ile polar molekül arasındaki çekim."),
             ("dipol–dipol etkileşimi", "Polar moleküllerin zıt yüklü uçları arasındaki çekim."),
             ("hidrojen bağı", "F, O ya da N’ye bağlı H ile komşu molekülün F, O, N atomu arasındaki güçlü çekim."),
             ("indüklenmiş dipol", "Yakındaki iyon ya da dipolün apolar tanecikte oluşturduğu geçici kutuplanma."),
             ("London kuvvetleri", "Anlık dipoller arasındaki zayıf çekim; bütün taneciklerde vardır."),
             ("benzer benzeri çözer", "Polar maddeler polar, apolar maddeler apolar çözücülerde iyi çözünür.")],
    (9, 9): [("kristal katı", "Taneciklerin düzenli, tekrar eden bir örgü kurduğu katı; belirli erime noktası vardır."),
             ("amorf katı", "Taneciklerin gelişigüzel dizildiği katı; bir sıcaklık aralığında yumuşar (cam)."),
             ("birim hücre", "Tekrarlanarak kristal örgüyü oluşturan en küçük yapı birimi."),
             ("iyonik katı", "Örgü noktalarındaki zıt yüklü iyonların elektrostatik çekimle tutunduğu katı."),
             ("moleküler katı", "Örgü noktalarında moleküllerin bulunduğu, zayıf etkileşimlerle tutunan katı."),
             ("kovalent ağ katı", "Atomların kovalent bağlarla kesintisiz ağ oluşturduğu katı: elmas, kuvars."),
             ("metalik katı", "Metal katyonlarının elektron denizi içinde tutunduğu katı."),
             ("allotrop", "Aynı elementin atomlarının farklı dizilmesiyle oluşan hâlleri: elmas–grafit, O₂–O₃."),
             ("camsı geçiş sıcaklığı", "Amorf katının sert hâlden yumuşak hâle geçtiği sıcaklık aralığı.")],
    (9, 10): [("buharlaşma", "Sıvı yüzeyindeki taneciklerin her sıcaklıkta gaza dönüşmesi; endotermiktir."),
              ("dinamik denge", "Buharlaşma ve yoğuşma hızlarının eşitlendiği, olayların durmadan sürdüğü denge."),
              ("denge buhar basıncı", "Dengedeki buharın yaptığı basınç; bir sıvı için yalnız sıcaklıkla değişir."),
              ("kaynama", "Buhar basıncı dış basınca ulaşınca sıvının her yerinden buharlaşması."),
              ("kaynama noktası", "Buhar basıncının dış basınca eşitlendiği sıcaklık; dış basınç azalınca düşer."),
              ("viskozite (akmazlık)", "Sıvının akmaya karşı gösterdiği direnç."),
              ("yüzey gerilimi", "Yüzeydeki taneciklerin içe çekilmesiyle sıvı yüzeyinin gerilmiş zar gibi davranması."),
              ("kohezyon", "Aynı tür tanecikler arasındaki çekim (su–su)."),
              ("adezyon", "Farklı tür tanecikler arasındaki çekim (su–cam)."),
              ("kılcallık", "İnce boruda sıvının kohezyon–adezyon yarışıyla yükselmesi ya da alçalması."),
              ("menisküs", "Sıvının ince borudaki eğri yüzeyi.")],
    (10, 1): [("fiziksel değişim", "Maddenin kimliği değişmeden biçiminin, boyutunun ya da hâlinin değişmesi."),
              ("kimyasal değişim", "Bağların kopup yenilerinin oluştuğu, yeni madde ortaya çıkan değişim."),
              ("çökelme tepkimesi", "İki çözelti karışınca suda az çözünen bir katının (çökelek) oluştuğu tepkime."),
              ("yükseltgenme", "Taneciğin elektron vermesi; yükseltgenme basamağı artar."),
              ("indirgenme", "Taneciğin elektron alması; yükseltgenme basamağı azalır."),
              ("redoks tepkimesi", "Yükseltgenme ve indirgenmenin birlikte olduğu, elektron alışverişli tepkime."),
              ("yanma", "Maddenin oksijenle tepkimesi; her yanma bir redoks tepkimesidir."),
              ("sentez tepkimesi", "İki ya da daha çok maddeden tek bir ürünün oluştuğu tepkime."),
              ("analiz tepkimesi", "Bir maddenin ısı, ışık ya da elektrikle daha basit maddelere ayrışması."),
              ("Arrhenius asidi", "Suda çözünce ortama H⁺ (H₃O⁺) iyonu veren madde."),
              ("Arrhenius bazı", "Suda çözünce ortama OH⁻ iyonu veren ya da suyla tepkimesinden OH⁻ oluşturan madde.")],
    (10, 3): [("kütlenin korunumu kanunu", "Tepkimeye girenlerin kütleleri toplamı, oluşanlarınkine eşittir."),
              ("tepkime denklemi", "Tepkimeyi formüller, katsayılar ve fiziksel hâllerle gösteren ifade."),
              ("denkleştirme", "Her atomun sayısını iki tarafta eşitlemek için katsayıları ayarlamak; alt simge değişmez."),
              ("katsayı", "Denklemde formülün önündeki, mol (tanecik) oranını gösteren sayı."),
              ("sınırlayıcı bileşen", "Tepkimede önce tükenen ve oluşan ürün miktarını belirleyen madde."),
              ("artan madde", "Tepkime bitince harcanmadan kalan tepken."),
              ("teorik verim", "Denkleme göre hesaplanan, oluşabilecek en çok ürün miktarı."),
              ("yüzde verim", "Gerçekte elde edilen ürünün teorik verime oranının yüzdesi."),
              ("saflık yüzdesi", "Örnekteki asıl maddenin kütlesinin örnek kütlesine oranının yüzdesi.")],
    (10, 4): [("basınç", "Birim yüzeye dik etki eden kuvvet; atm, mmHg, Pa ile ölçülür."),
              ("mutlak sıcaklık", "Kelvin cinsinden sıcaklık: T(K) = t(°C) + 273."),
              ("NŞA", "Normal şartlar: 0 °C ve 1 atm; 1 mol ideal gaz 22,4 L hacim kaplar."),
              ("Boyle yasası", "Sabit sıcaklık ve miktarda gazın basıncı ile hacmi ters orantılıdır."),
              ("Charles yasası", "Sabit basınç ve miktarda gazın hacmi mutlak sıcaklıkla doğru orantılıdır."),
              ("Gay-Lussac yasası", "Sabit hacim ve miktarda gazın basıncı mutlak sıcaklıkla doğru orantılıdır."),
              ("Avogadro yasası", "Aynı sıcaklık ve basınçta eşit hacimli gazlarda eşit sayıda tanecik vardır."),
              ("ideal gaz denklemi", "P·V = n·R·T; R = 0,082 L·atm/(mol·K)."),
              ("kinetik teori", "Gaz taneciklerinin sürekli, gelişigüzel hareket ettiğini açıklayan model; ortalama kinetik enerji mutlak sıcaklıkla orantılıdır."),
              ("difüzyon", "Gaz taneciklerinin başka bir gaz içinde kendiliğinden yayılması."),
              ("efüzyon", "Gazın küçük bir delikten boşluğa kaçması."),
              ("manometre", "Kapalı kaptaki gazın basıncını ölçen araç.")],
    (10, 5): [("çözelti", "Tanecik düzeyinde homojen karışım."),
              ("çözücü", "Çözeltide diğerini dağıtan bileşen; sulu çözeltide sudur."),
              ("çözünen", "Çözücü içinde dağılan bileşen."),
              ("iyonik çözünme", "Çözünenin çözeltide iyonlar hâlinde dağılması (NaCl)."),
              ("moleküler çözünme", "Çözünenin molekül hâlinde dağılması; iyon oluşmaz (şeker)."),
              ("hidratasyon", "Çözünen taneciklerin su molekülleriyle sarılması."),
              ("solvatasyon", "Çözünen taneciklerin sudan başka bir çözücünün molekülleriyle sarılması."),
              ("elektrolit", "Suda iyonlarına ayrışarak çözeltisini elektrik iletken yapan madde."),
              ("çözünürlük", "Belirli sıcaklık ve basınçta 100 g çözücüde çözünebilen en çok madde kütlesi."),
              ("doymuş çözelti", "O koşulda çözebileceği en çok maddeyi çözmüş çözelti."),
              ("aşırı doymuş çözelti", "Çözünürlüğün üstünde madde içeren kararsız çözelti.")],
    (10, 6): [("derişim", "Belirli miktar çözeltide çözünmüş madde miktarı."),
              ("kütlece yüzde", "100 g çözeltideki çözünenin gram cinsinden kütlesi."),
              ("hacimce yüzde", "100 mL çözeltideki çözünenin mL cinsinden hacmi; kolonya derecesi buna örnektir."),
              ("ppm", "Milyonda bir kısım: 1 kg çözeltide 1 mg çözünen 1 ppm’dir."),
              ("molarite", "1 L çözeltideki çözünenin mol sayısı (mol/L, M)."),
              ("seyreltme", "Çözücü ekleyerek derişimi azaltma; çözünenin mol sayısı değişmez."),
              ("koligatif özellik", "Çözünenin cinsine değil, tanecik derişimine bağlı çözelti özelliği."),
              ("buhar basıncı düşmesi", "Uçucu olmayan madde çözülen sıvının buhar basıncının azalması."),
              ("kaynama noktası yükselmesi", "Uçucu olmayan madde çözülen sıvının daha yüksek sıcaklıkta kaynaması."),
              ("donma noktası alçalması", "Çözünen taneciklerin donmayı zorlaştırması; kışın yola tuz serpilmesi buna dayanır.")],
}


def terimler(k):
    """[(terim_html, tanim_html, yol)] Türkçe alfabe sırasıyla. meta.json kavramları o ünite için önceliklidir."""
    from yardim import zengin
    out = {}
    for y in k.yollar:
        liste = [(t, d) for t, d in KAVRAMLAR.get((k.sinif, y["yol"]), [])]
        meta = [(m.get("terim", ""), m.get("tanim", "")) for m in (y.get("kavramlar") or []) if m.get("terim")]
        if meta:
            adlar = {V.turkce_anahtar(t) for t, _ in meta}
            liste = meta + [(t, d) for t, d in liste if V.turkce_anahtar(t) not in adlar]
        for t, d in liste:
            out.setdefault(V.turkce_anahtar(t), (zengin(t), zengin(d), y["yol"], t))
    return [out[a] for a in sorted(out)]


def _yukseklik(terim, tanim):
    """Bir maddenin tahmini yüksekliği (mm), 58 mm'lik sütunda 9 pt yazıyla."""
    import re
    metin = re.sub(r"<[^>]+>", "", terim + " " + tanim)
    satir = math.ceil((len(metin) + 5) / 41)
    return satir * 3.92 + 2.1


def sayfalara_bol(k):
    """Sayfalar → sütunlar → öğeler [('harf', 'A') | ('madde', terim, tanim, yol)]. 1. sayfa bantlı (daha kısa)."""
    liste = terimler(k)
    k.kavram_sayisi = len(liste)
    ogeler = []
    son_harf = None
    for terim, tanim, yol, duz in liste:
        h = V.ilk_harf(duz.lstrip("-"))
        if h != son_harf:
            ogeler.append(("harf", h, 7.2))
            son_harf = h
        ogeler.append(("madde", terim, tanim, yol, _yukseklik(terim, tanim)))
    sayfalar = []
    i = 0
    while i < len(ogeler):
        boy = 218.0 if not sayfalar else 246.0
        sutunlar = []
        for _ in range(3):
            sutun, h = [], 0.0
            while i < len(ogeler):
                o = ogeler[i]
                yuk = o[-1]
                if o[0] == "harf" and i + 1 < len(ogeler):
                    yuk += ogeler[i + 1][-1]          # başlık sütun sonunda yalnız kalmasın
                if h + yuk > boy and sutun:
                    break
                sutun.append(o[:-1])
                h += o[-1]
                i += 1
            sutunlar.append(sutun)
        sayfalar.append(sutunlar)
    return sayfalar
