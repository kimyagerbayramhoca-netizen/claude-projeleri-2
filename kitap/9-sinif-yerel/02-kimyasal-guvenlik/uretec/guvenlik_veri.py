"""Kimyasal Güvenlik · tek doğruluk kaynağı olan VERİ (çizim yok).

Bilgi grafikleri (infografik_unite.py) ve doğrulama (dogrula.py) aynı tabloları buradan okur; böylece sayfada çizilen
piktogram ile adı/anlamı, depolama matrisinin hücreleri ve sorulardaki cevaplar birbirine kilitlenir.

Kaynak notları (2026-11 denetimi): GHS piktogramları ve Türkçe adları SEA Yönetmeliği (AB CLP uyumlu) ile; güvenlik işaretleri
"Sağlık ve Güvenlik İşaretleri Yönetmeliği" (ISO 7010 esinli renk/biçim) ile; ilk yardım süreleri güncel ilk yardım
önerileriyle (kimyasal sıçrama: 15–20 dk bol akan su; ısı yanığı: ≈ 20 dk serin akan su, buz yok) uyumludur.
Depolama matrisi kitabın SADELEŞTİRİLMİŞ örneğidir (sayfada da öyle yazar); gerçek depoda güvenlik bilgi formu esas alınır.
"""

# ------------------------------------------------------------------ GHS piktogramları (kod, tehlike adı, simge adı, anlam, örnek)
GHS = [
    ("GHS01", "Patlayıcı", "patlayan bomba", "Isı, darbe, sürtünme ya da kıvılcımla patlayabilir.", "TNT, nitrogliserin"),
    ("GHS02", "Yanıcı", "alev", "Kolay tutuşur; alevden, kıvılcımdan uzak tutulur.", "etil alkol, aseton, metan"),
    ("GHS03", "Yakıcı (oksitleyici)", "çember üstünde alev", "Yanmayı başlatır ya da şiddetlendirir.", "oksijen, potasyum permanganat"),
    ("GHS04", "Basınçlı gaz", "gaz tüpü", "Tüp ısınırsa patlayabilir; soğuk gaz soğuk yanığı yapar.", "oksijen, azot, CO₂ tüpü"),
    ("GHS05", "Aşındırıcı (korozif)", "aşınma", "Deriyi, gözü ve metali aşındırır; kimyasal yanık yapar.", "tuz ruhu, sud kostik"),
    ("GHS06", "Zehirli (toksik)", "kurukafa", "Az miktarı bile yutulunca, solununca ağır zehirler.", "metanol, karbon monoksit"),
    ("GHS07", "Tahriş edici, zararlı", "ünlem", "Deriyi, gözü, solunum yolunu tahriş eder.", "aseton, bazı temizleyiciler"),
    ("GHS08", "Ciddi sağlık tehlikesi", "sağlık tehlikesi", "Uzun sürede kanser ya da organ hasarı yapabilir.", "benzen, formaldehit"),
    ("GHS09", "Çevreye zararlı", "ağaç ve balık", "Su canlıları için zehirlidir; lavaboya dökülmez.", "bakır(II) sülfat, cıva bileşikleri"),
]
GHS_AD = {k: ad for k, ad, *_ in GHS}
GHS_SIMGE = {k: sim for k, _a, sim, *_ in GHS}

# Gerçek etiketlerdeki piktogramlar (soru ve örneklerde kullanılan maddeler; AB CLP uyumlu sınıflandırma)
MADDE_PIKTO = {
    "etil alkol": {"GHS02", "GHS07"},
    "aseton": {"GHS02", "GHS07"},
    "metanol": {"GHS02", "GHS06", "GHS08"},
    "potasyum nitrat": {"GHS03"},
    "sud kostik": {"GHS05"},
    "tuz ruhu": {"GHS05", "GHS07"},
    "bakır(II) sülfat": {"GHS07", "GHS09"},
    "oksijen tüpü": {"GHS03", "GHS04"},
    "karbon monoksit": {"GHS02", "GHS04", "GHS06", "GHS08"},
    "amonyum nitrat": {"GHS03", "GHS07"},
}

# ------------------------------------------------------------------ güvenlik işaretleri (aile: biçim, renk, anlam)
ISARET_AILE = {
    "zor": ("Zorunluluk", "mavi daire", "yapmalısın"),
    "uya": ("Uyarı", "sarı üçgen", "dikkat et"),
    "yas": ("Yasak", "kırmızı çizgili daire", "yapma"),
    "acil": ("Acil durum", "yeşil kare", "yardım burada"),
    "yan": ("Yangın ekipmanı", "kırmızı kare", "söndürücü burada"),
}
# simge → (aile, ad)
ISARET = {
    "baret": ("zor", "Baret tak"), "gozluk": ("zor", "Gözlük tak"), "eldiven": ("zor", "Eldiven tak"), "onluk": ("zor", "Önlük giy"),
    "elektrik": ("uya", "Elektrik"), "sicak": ("uya", "Sıcak yüzey"), "yanici": ("uya", "Yanıcı madde"),
    "alev_yok": ("yas", "Açık alev yok"), "sigara_yok": ("yas", "Sigara içilmez"), "yeme_yok": ("yas", "Yeme-içme yok"),
    "ilkyardim": ("acil", "İlk yardım"), "gozdusu": ("acil", "Göz duşu"),
    "sondurucu": ("yan", "Yangın söndürücü"),
}

# ------------------------------------------------------------------ depolama matrisi (sadeleştirilmiş örnek)
# Sınıflar: Y yanıcı (alev) · O yakıcı/oksitleyici · Z zehirli (kurukafa) · A aşındırıcı · T tahriş edici (ünlem)
# Değer: "+" birlikte · "x" ayrı · "!" yalnızca özel önlemle (bu kitapta "!" eşleşmesinden de kaçınılır)
SINIF = ["Y", "O", "Z", "A", "T"]
SINIF_AD = {"Y": "Yanıcı", "O": "Yakıcı", "Z": "Zehirli", "A": "Aşındırıcı", "T": "Tahriş edici"}
SINIF_GHS = {"Y": "GHS02", "O": "GHS03", "Z": "GHS06", "A": "GHS05", "T": "GHS07"}
GHS_SINIF = {v: k for k, v in SINIF_GHS.items()}
MATRIS = {
    "Y": {"Y": "+", "O": "x", "Z": "!", "A": "x", "T": "+"},
    "O": {"Y": "x", "O": "+", "Z": "x", "A": "x", "T": "x"},
    "Z": {"Y": "!", "O": "x", "Z": "+", "A": "x", "T": "+"},
    "A": {"Y": "x", "O": "x", "Z": "x", "A": "+", "T": "+"},
    "T": {"Y": "+", "O": "x", "Z": "+", "A": "+", "T": "+"},
}


def birlikte(s1, s2, ozel_onlemle=False):
    """Matristeki sınıf kümeleri s1, s2 olan iki madde aynı bölmeye konabilir mi? (her sınıf çifti '+' olmalı)"""
    for a in s1:
        for b in s2:
            v = MATRIS[a][b]
            if v == "x" or (v == "!" and not ozel_onlemle):
                return False
    return True


def en_az_bolme(maddeler):
    """{ad: sınıf kümesi} → en az bölme sayısı ve bir yerleşim (kaba kuvvet; madde sayısı küçük)."""
    adlar = list(maddeler)
    en_iyi = [None]

    def ara(i, gruplar):
        if en_iyi[0] and len(gruplar) >= len(en_iyi[0]):
            return
        if i == len(adlar):
            en_iyi[0] = [list(g) for g in gruplar]
            return
        m = adlar[i]
        for g in gruplar:
            if all(birlikte(maddeler[m], maddeler[o]) for o in g):
                g.append(m)
                ara(i + 1, gruplar)
                g.pop()
        gruplar.append([m])
        ara(i + 1, gruplar)
        gruplar.pop()

    ara(0, [])
    return len(en_iyi[0]), en_iyi[0]


# ------------------------------------------------------------------ cam malzemeler (ad, ısıtılır mı, hacim duyarlılığı)
# duyarlılık: "hassas" (pipet, büret, balon joje) · "orta" (mezür) · "yaklaşık" (beher, erlen çizgileri) · None (ölçmez)
CAM = [
    ("tup", "Deney tüpü", True, None, "az madde ısıtır, karıştırır"),
    ("beher", "Beherglas", True, "yaklaşık", "karıştırır, ısıtır, aktarır"),
    ("erlen", "Erlenmayer", True, "yaklaşık", "çalkalarken sıçratmaz"),
    ("balon", "Cam balon", True, None, "ısıtır, kaynatır, damıtır"),
    ("joje", "Balon joje", False, "hassas", "tek ve kesin hacim hazırlar"),
    ("mezur", "Mezür", False, "orta", "hacim ölçer, aktarır"),
    ("pipet", "Pipet + puar", False, "hassas", "az sıvıyı hassas aktarır"),
    ("buret", "Büret", False, "hassas", "titrasyonda hacim ölçer"),
]
HASSAS = {ad for _k, ad, _i, d, _ in CAM if d == "hassas"}
ISITILIR = {ad for _k, ad, i, *_ in CAM if i}

# ------------------------------------------------------------------ diğer malzemeler (kısa görev)
EKIPMAN = [
    ("huni", "Huni + süzgeç kâğıdı", "katıyı sıvıdan süzer"),
    ("ayirma", "Ayırma hunisi", "karışmayan sıvıları ayırır"),
    ("sogutucu", "Soğutucu", "buharı yoğuşturur"),
    ("piset", "Piset", "saf suyla yıkar"),
    ("damlalik", "Damlalık", "damla damla aktarır"),
    ("termometre", "Termometre", "sıcaklık ölçer"),
    ("spor", "Spor + kıskaç", "düzeneği dik tutar"),
    ("havan", "Havan", "katıyı toz eder"),
    ("spatul", "Spatül", "katı alır"),
    ("baget", "Baget", "karıştırır"),
    ("saatcami", "Saat camı", "az katı tartar, örter"),
    ("kroze", "Kroze", "katıyı çok ısıtır"),
]
ISITMA = [
    ("bek", "Bunzen beki", "gazla ısıtır"),
    ("ispirto", "İspirto ocağı", "hafif ısıtır"),
    ("sacayak", "Sacayağı + tel kafes", "kabı taşır, ısıyı yayar"),
    ("masa", "Tüp maşası", "sıcak tüpü tutar"),
]

# ------------------------------------------------------------------ atık sınıfları (kutu, örnekler)
ATIK = [
    ("kimyasal", "Kimyasal atık kabı", ["bakır(II) sülfat çözeltisi", "artan asit, baz (ayrı kaplar)"]),
    ("cam", "Kırık cam kutusu", ["kırılan beher, deney tüpü"]),
    ("tibbi", "Tıbbi atık (kırmızı torba)", ["kullanılmış enjektör, kanlı pamuk"]),
    ("pil", "Atık pil kutusu", ["bitmiş kalem pil"]),
    ("yag", "Bitkisel atık yağ", ["kızartma yağı"]),
    ("ambalaj", "Ambalaj (geri dönüşüm)", ["boş, durulanmış deterjan şişesi"]),
]
ATIK_KUTU = {o: ad for _k, ad, ornek in ATIK for o in ornek}

# ------------------------------------------------------------------ kaza anı (durum → ilk adım) · güncel ilk yardım önerileri
KAZA = [
    ("Göze kimyasal sıçradı", "Göz duşunda, kapaklar açık, 15–20 dakika bol akan suyla yıka; ovma."),
    ("Deriye kimyasal döküldü", "Bulaşan giysiyi çıkar; 15–20 dakika bol akan su. Asit de baz da olsa önce su."),
    ("Isı yanığı", "Yaklaşık 20 dakika serin (buzlu değil) akan su; buz, diş macunu, yağ sürme."),
    ("Cam kesiği", "Öğretmene haber ver; temiz bezle bastır; batan camı kendin çıkarma."),
    ("Giysi alev aldı", "Koşma: dur, yere yat, yuvarlan; yangın battaniyesiyle sar."),
    ("Kimyasal yutuldu ya da solundu", "Kusturma; temiz havaya çık. 112’yi ara, 114 Zehir Danışma; etiketi götür."),
]

# ------------------------------------------------------------------ sayısal küçük bilgiler (dogrula.py yeniden hesaplar)
SU_BUHAR_KAT = 1700          # 100 °C ve 1 atm'de 1 g su buharı ≈ 1,70 L; 1 g sıvı su ≈ 1 mL
METAN_ARALIK = (5, 15)       # metanın havada tutuşabildiği yaklaşık hacim yüzdesi aralığı
KAZA_GRAFIK = {"Kesik": (10, 4), "Isı yanığı": (6, 3), "Göze sıçrama": (8, 1), "Deriye temas": (6, 3)}   # Kıssa 3
CO_GRAFIK = [(0, 0), (10, 25), (20, 50), (30, 80), (40, 100), (50, 60), (60, 30), (70, 15)]               # Üstad 3 (dk, ppm)
CO_ESIK = 50                 # soruda verilen dedektör eşiği (ppm)
CO_PENCERE = 40              # pencerenin açıldığı an (dk)
MEZUR_OKUMA = 36             # İmtihan 3: çukur menisküsün alt noktası (mL)
