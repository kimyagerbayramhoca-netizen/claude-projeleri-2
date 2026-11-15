"""Medeniyetimizden zaman şeridinin verisi (doğrulanmış, tartışmasız bilgiler).

Her satır: ad, tarih (görünen), sira (sıralama yılı), katki (tek satırlık katkı), ikon, takma adlar (rotalar.json /
meta.json'daki yazılışlarla eşleştirmek için). Yol rozetleri ELLE yazılmaz: rotalar.json'daki "medeniyet" önerilerinden
ve hazır ünitelerin meta.json "medeniyet" listesinden hesaplanır.

Kaynak notları (WebSearch ile denetlendi, 2026-11): TDV İslâm Ansiklopedisi maddeleri (Takıyyüddin er-Râsıd, Câbir b. Hayyân,
Uluğ Bey, Zîc-i İlhânî, Keşfü'z-zunûn, İbrâhim Hakkı Erzurûmî), nobelprize.org (Aziz Sancar), Britannica (Hârizmî),
Encyclopaedia Iranica (Bîrûnî), Wellcome/ARCE kataloğu (İbn Sînâ, De congelatione). Tartışmalı ya da efsanevi bilgi yok.
"""
import re
import unicodedata

KISILER = [
    {"ad": "Câbir bin Hayyân", "tarih": "8. yüzyıl", "sira": 780, "ikon": "imbik",
     "katki": "Adıyla anılan eserler damıtma, kristallendirme ve süzme gibi işlemleri sistemli biçimde anlatır.",
     "takma": ["Câbir", "Cabir"]},
    {"ad": "el-Hârizmî", "tarih": "y. 780 – 850", "sira": 800, "ikon": "cebir",
     "katki": "Cebir kitabıyla denklem çözmeyi sistemleştirdi; “algoritma” sözcüğü onun adından gelir.",
     "takma": ["Hârizmî", "Harizmi"]},
    {"ad": "el-Kindî", "tarih": "9. yüzyıl", "sira": 830, "ikon": "gul",
     "katki": "Koku ve damıtma üzerine kitabında gül suyu gibi kokulu suların damıtılmasını tarif etti.",
     "takma": ["Kindî", "Kindi"]},
    {"ad": "Ebû Bekir er-Râzî", "tarih": "865 – 925", "sira": 865, "ikon": "razi",
     "katki": "Maddeleri sınıflandırdı; laboratuvar araçlarını ve işlemlerini tek tek tarif etti.",
     "takma": ["er-Râzî", "Râzî", "Razi"]},
    {"ad": "İbn Heysem", "tarih": "y. 965 – 1040", "sira": 965, "ikon": "goz",
     "katki": "Kitâbü’l-Menâzır’da görmenin, cisimden göze gelen ışıkla olduğunu deney ve gözlemle savundu.",
     "takma": ["İbnü'l-Heysem", "İbnü’l-Heysem", "Ibn Heysem"]},
    {"ad": "el-Bîrûnî", "tarih": "973 – 1048", "sira": 973, "ikon": "ozgul",
     "katki": "Birçok metal ve değerli taşın özgül ağırlığını hassas biçimde ölçtü.",
     "takma": ["Bîrûnî", "Biruni"]},
    {"ad": "İbn Sînâ", "tarih": "980 – 1037", "sira": 980, "ikon": "sina",
     "katki": "Kitâbü’ş-Şifâ’da taşların ve madenlerin oluşumunu inceledi; metallerin altına dönüştürülebileceğini kabul etmedi.",
     "takma": ["İbni Sina", "Ibn Sina"]},
    {"ad": "el-Hâzinî", "tarih": "12. yüzyıl", "sira": 1121, "ikon": "terazi",
     "katki": "Mîzânü’l-Hikme’de (1121) hidrostatik terazisini ve maddelerin özgül ağırlık tablolarını anlattı.",
     "takma": ["Hâzinî", "Hazini"]},
    {"ad": "el-Cezerî", "tarih": "kitabı 1206", "sira": 1206, "ikon": "cark",
     "katki": "Diyarbakır’da Artuklu sarayının mühendisiydi; kitabında su saatlerini ve otomatik makineleri çizimleriyle anlattı.",
     "takma": ["Cezerî", "Cezeri"]},
    {"ad": "Nasîrüddîn-i Tûsî", "tarih": "1201 – 1274", "sira": 1259, "ikon": "rasat",
     "katki": "Merâga Rasathanesi’ni kurdu (1259); buradaki gözlemlerle Zîc-i İlhânî hazırlandı.",
     "takma": ["Tûsî", "Tusi", "Nasîrüddin Tûsî"]},
    {"ad": "Uluğ Bey", "tarih": "1394 – 1449", "sira": 1420, "ikon": "yildiz",
     "katki": "Semerkant’ta kurdurduğu rasathanede hazırlanan zîcinde 1018 yıldızın konumu yer alır.",
     "takma": ["Ulugh Beg"]},
    {"ad": "Takiyüddin", "tarih": "1526 – 1585", "sira": 1577, "ikon": "saat",
     "katki": "1577’den itibaren İstanbul’da Tophane sırtlarındaki rasathanede gözlem yaptı; mekanik saati gözlem aracı olarak kullandı.",
     "takma": ["Takıyyüddin", "Takiyyüddin", "Takiyuddin"]},
    {"ad": "Kâtip Çelebi", "tarih": "1609 – 1657", "sira": 1640, "ikon": "kure",
     "katki": "Keşfü’z-Zunûn’da yaklaşık 15.000 kitabı tanıttı; Cihannümâ’da dünyanın coğrafyasını anlattı.",
     "takma": ["Kâtib Çelebi", "Katip Celebi"]},
    {"ad": "İbrahim Hakkı Erzurumî", "tarih": "1703 – 1780", "sira": 1757, "ikon": "marifet",
     "katki": "Mârifetnâme’de (1757) gökbilimden insan bedenine pek çok bilgiyi Türkçe bir araya getirdi.",
     "takma": ["İbrâhim Hakkı", "Erzurumlu İbrahim Hakkı"]},
    {"ad": "Aziz Sancar", "tarih": "1946 · Savur, Mardin", "sira": 2015, "ikon": "dna",
     "katki": "DNA onarımının mekanizmaları üzerine çalışmalarıyla 2015 Nobel Kimya Ödülü’nü T. Lindahl ve P. Modrich ile paylaştı.",
     "takma": []},
]

# zaman şeridindeki eser işaretleri (rotalarda "Medeniyetimizden" önerisi olarak geçen kurumlar)
ESERLER = [
    {"ad": "Gevher Nesibe Darüşşifası", "tarih": "1206", "sira": 1206.5, "yer": "Kayseri",
     "katki": "Selçuklu şifahanesi ve tıp medresesi", "takma": ["Gevher Nesibe"]},
    {"ad": "Divriği Darüşşifası", "tarih": "1228", "sira": 1228, "yer": "Sivas",
     "katki": "Turan Melek Sultan’ın yaptırdığı şifahane", "takma": ["Divriği"]},
    {"ad": "Süleymaniye Darüşşifası ve Tıp Medresesi", "tarih": "1550 – 1557", "sira": 1555, "yer": "İstanbul",
     "katki": "Süleymaniye Külliyesi’nde şifahane ve tıp medresesi", "takma": ["Süleymaniye"]},
]


def _anahtar(s):
    """Karşılaştırma anahtarı: şapka/nokta işaretleri ve 'el-/er-/ebû bekir' önekleri atılır."""
    s = s.replace("İ", "i").replace("I", "ı").lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = s.replace("ı", "i").replace("’", "'")
    s = re.sub(r"\b(el|er|es|en|et)-", "", s)
    s = re.sub(r"\bebu bekir\b", "", s)
    s = re.sub(r"[^a-z' ]", " ", s)
    return " ".join(s.split())


def eslesir(kayit, ad):
    a = _anahtar(ad)
    adaylar = [_anahtar(kayit["ad"])] + [_anahtar(t) for t in kayit.get("takma", [])]
    return any(a == x or (len(x) > 4 and (x in a or a in x)) for x in adaylar)


def yol_rozetleri(kayit, sinif_yollari):
    """kayit için [(sinif, yol, renk, hazir)] — o kişinin/eserin anlatıldığı yollar."""
    out = []
    for sinif, yollar in sinif_yollari.items():
        for y in yollar:
            if any(eslesir(kayit, m) for m in y.get("medeniyet", [])):
                out.append((sinif, y["yol"], y["renk"], y["hazir"]))
    return out
