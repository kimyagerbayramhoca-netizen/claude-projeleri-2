"""Atom ve Yapısı · kat sayfası "Katla, doğrusu kalsın!" (ünitenin kendi türü; ortak cizim/katla.py parçalarıyla).

MEKANİK. Her satırda büyük bir cümle şeridi sayfayı boydan geçer. Açıkken cümle YANLIŞTIR: yanlış parça orta şerittedir
(70–140 mm). Orta şerit arkaya katlanınca o parça gizlenir; sol parça (A'ya yaslı) ile sağ parça (B'den başlar) yan yana
gelir ve DOĞRU cümleyi okur. Bölünme sözcük arasındadır (harf kesilmez); her parça kat çizgilerinden en az GUVEN (1,2 mm)
uzaktadır. Dikişte yalnız "DOĞRU" kurdelesi bölünür (bölünen harf O: GUVENLI_HARF). Başlık da aynı oyunu oynar:
"Katla," + "(ama önce yanlışı bul!)" + "doğrusu kalsın!" → katlıyken "Katla, doğrusu kalsın!".

KATLA_CUMLE tek doğruluk kaynağıdır: dogrula.py açık cümlenin yanlış, katlı cümlenin doğru olduğunu ve genişlikleri denetler.
Öğretmen cevabı <g class="ogr-svg" data-katla="C1" data-urun="katlı cümle" data-tur="gizlenen parça"> (katla_ayni okur).
"""
from cizim import katla as KC
from cizim import konu_karakterleri as KK
from cizim.renkler import OBS, OBS2, SOLUK, GOL_K, KEH_K, KOB_K, MER, MER_K, ZUMRUT

A_X, B_X, GUVEN = KC.A_X, KC.B_X, KC.GUVEN
SOL_X0, SAG_X1 = 8.0, 202.0              # şeridin dış sınırları
BOY_UST, FONT = 5.2, "baloo"             # şerit yazısının en büyük boyu (mm) ve yazı tipi

KATLA_CUMLE = [
    dict(kod="C1", durak="1. durak · Göbeklitepe", sol="Dalton modelinde atom", orta="elektronlu ve çekirdekli,",
         sag="içi dolu bir küredir.", ipucu="Elektron 1897’de, çekirdek 1911’de bulundu.",
         sol_cizim=("kk", "kk-dalton-sasiran", "Dalton · 1803–1808"), sag_cizim=("kk", "kk-dalton", "içi dolu, bölünemez"),
         neden="Elektron da çekirdek de Dalton’dan sonra bulundu."),
    dict(kod="C2", durak="2. durak · Harran", sol="Alfaların çoğu", orta="levhadan geri döndü, çok azı",
         sag="sapmadan geçti.", ipucu="Atomun büyük kısmı boşluktur.",
         sol_cizim=("kk", "kk-alfa-sasiran", "altın levha · 1909"), sag_cizim=("kk", "kk-alfa-mutlu", "çoğu düz geçti"),
         neden="Çoğu düz geçti; çok azı geri döndü."),
    dict(kod="C3", durak="4. durak · Urfa çarşısı", sol="İzotoplarda proton", orta="sayısı farklı, nötron",
         sag="sayısı aynıdır.", ipucu="Kimlik proton sayısıdır.",
         sol_cizim=("iz", (35, 17, "Cl"), "17 p · 18 n"), sag_cizim=("iz", (37, 17, "Cl"), "17 p · 20 n"),
         neden="p aynı (17), n farklı (18 ve 20)."),
    dict(kod="C4", durak="6. durak · Fırat kıyısı", sol="Ca^{2+} olurken elektronlar", orta="önce 3p’den, ardından",
         sag="4s’den verilir.", ipucu="Katyonda önce en dış katman boşalır.",
         sol_cizim=("orb", ("Ca", "ud"), "[Ar] 4s^{2}"), sag_cizim=("orb", ("Ca^{2+}", "0"), "[Ar] · 4s boş"),
         neden="İki e^{−} de 4s’den gider; 3p^{6} kalır."),
]


def katli(s):
    return f'{s["sol"]} {s["sag"]}'


def acik(s):
    return f'{s["sol"]} {s["orta"]} {s["sag"]}'


def serit_boyu(satirlar=KATLA_CUMLE):
    """Bütün satırlarda sığan en büyük ortak boy: sol ≤ A − GUVEN − 8 · orta ≤ (B − A) − 2·GUVEN · sağ ≤ 202 − B − GUVEN."""
    sinir = {"sol": A_X - GUVEN - SOL_X0, "orta": (B_X - A_X) - 2 * GUVEN, "sag": SAG_X1 - B_X - GUVEN}
    boy = BOY_UST
    for s in satirlar:
        for ad, en in sinir.items():
            w = KC.genislik(s[ad], 1.0, FONT)
            boy = min(boy, en / w)
    return round(boy * .985, 2)


def _yasli_orta(metin, y, boy):
    """Orta parça: iki kat çizgisi arasında sözcük aralığı açılarak yayılır (iki uçta GUVEN payı)."""
    soz = metin.split(" ")
    x0, x1 = A_X + GUVEN, B_X - GUVEN
    ws = [KC.genislik(w, boy, FONT) for w in soz]
    bosluk = (x1 - x0 - sum(ws)) / max(1, len(soz) - 1)
    bosluk = min(bosluk, boy * .9)                       # çok açılmasın: fazlası iki uca eşit dağılır
    toplam = sum(ws) + bosluk * (len(soz) - 1)
    x = x0 + (x1 - x0 - toplam) / 2
    o = []
    for w, g in zip(soz, ws):
        o.append(KC.yazi(w, x, y, boy, OBS, FONT)[0])
        x += g + bosluk
    return "".join(o), x0 + (x1 - x0 - toplam) / 2, x - bosluk


def _orb_kutu(x, y, kod, w=6.4, h=6.8):
    """Orbital kutusu (mm): kod 'ud' ↑↓, 'u' ↑, '0' boş · oklar çizgi (fonttaki ↑↓'ya bağlı değil)."""
    o = [f'<rect x="{KC.f(x)}" y="{KC.f(y)}" width="{w}" height="{h}" fill="#FFFFFF" stroke="{OBS}" stroke-width=".35"/>']

    def ok(cx, yukari):
        y0, y1 = (y + h - 1, y + 1) if yukari else (y + 1, y + h - 1)
        u = 1 if yukari else -1
        return (f'<path d="M{KC.f(cx)} {KC.f(y0)} V{KC.f(y1 + u * .4)}" stroke="{OBS}" stroke-width=".42" stroke-linecap="round"/>'
                f'<path d="M{KC.f(cx - 1.1)} {KC.f(y1 + u * 1.5)} L{KC.f(cx)} {KC.f(y1)} L{KC.f(cx + 1.1)} {KC.f(y1 + u * 1.5)}" fill="none" '
                f'stroke="{OBS}" stroke-width=".42" stroke-linecap="round" stroke-linejoin="round"/>')
    if kod == "ud":
        o.append(ok(x + w * .33, True) + ok(x + w * .67, False))
    elif kod == "u":
        o.append(ok(x + w / 2, True))
    return "".join(o)


def _cizim(tur, veri, alt, cx, y0, hiza):
    """Satırın yan çizimi (açıkta görünür, dikişi geçmez). cx: çizimin ortası."""
    o = []
    if tur == "kk":
        o.append(KK.kullan(veri, cx - 7.5, y0 + 9.4, 15))
    elif tur == "iz":
        A, Z, sem = veri
        o.append(KC.yazi(str(A), cx - 3.2, y0 + 14.0, 3.0, KOB_K, "nunito9", "sag")[0])
        o.append(KC.yazi(str(Z), cx - 3.2, y0 + 20.2, 3.0, KOB_K, "nunito9", "sag")[0])
        o.append(KC.yazi(sem, cx - 2.6, y0 + 20.2, 8.6, OBS, "baloo")[0])
    elif tur == "orb":
        sem, kod = veri
        o.append(KC.yazi(sem, cx, y0 + 14.6, 6.0, OBS, "baloo", "orta")[0])
        o.append(KC.yazi("4s", cx - 4.4, y0 + 21.6, 3.2, OBS2, "nunito9", "sag")[0])
        o.append(_orb_kutu(cx - 3.2, y0 + 16.6, kod))
    o.append(KC.yazi(alt, cx, y0 + 27.4, 2.75, OBS2, "nunito", "orta", en=40)[0])
    return "".join(o)


def _kurdele(y, boy=3.0):
    """Dikişe ortalı yeşil DOĞRU kurdelesi (katlı uzay): şekil TASMA payıyla, yazı tam dikişte kesilir."""
    sekil = (f'<path d="M{KC.f(A_X - 9.6)} {KC.f(y - 3.4)} H{KC.f(A_X + 9.6)} l-1.4 2.3 l1.4 2.3 H{KC.f(A_X - 9.6)} l1.4 -2.3 Z" '
             f'fill="{ZUMRUT}"/>')
    yazi_svg, _, _ = KC.bolunmus("D", "O", "ĞRU", y - .05, boy, "#FFFFFF", "baloo")   # şeridin ortası y − 1,1
    return sekil, yazi_svg


def cumle_sayfasi(onek, rozet_svg, muhur_svg, rota="Yol 3 · Şanlıurfa–Harran", satirlar=KATLA_CUMLE):
    """muhur_svg: () → YANLIŞ mührü <svg> (ünitenin muhur yer tutucusu). Dönen: (Sayfa, satır bilgileri)."""
    s = KC.Sayfa(onek)
    KC._kat_isaretleri(s)
    KC._baslik(s, "Katla,", "doğrusu kalsın!", "(ama önce yanlışı bul!)", [rota, "Dört cümle, tek katlama."],
               ["Dört cümlede de yanlış var.", "4 tahmin · +40 akçe"], rozet_svg, ["Önce yanlışı bul,", "sonra katla!"])
    KC._nasil_katlanir(s, "Önce yanlışı çiz, sonra katla; aç ve açıkla.")
    s.ekle(KC.yazi("Büyük cümleyi oku: yanlış sözcükleri çiz.", 8, 45.5, 2.95, GOL_K, "nunito", en=59)[0]
           + KC.yazi("Katlayınca orta parça gizlenir,", 8, 49.6, 2.95, OBS2, "nunito", en=59)[0]
           + KC.yazi("kalan sözcükler doğrusunu yazar.", 8, 53.7, 2.95, OBS2, "nunito", en=59)[0])
    boy = serit_boyu(satirlar)
    bilgi = []
    for k, c in enumerate(satirlar):
        y0 = KC.satir_y(k)
        ys = y0 + 34.2
        s.ekle(KC._bant(k) + KC._no(9.4, y0 + 6.2, k + 1))
        s.ekle(KC.yazi(c["durak"], 15, y0 + 7.4, 3.5, OBS, "baloo", en=52)[0])
        s.ekle(KC.yazi("kanıt", SAG_X1, y0 + 7.4, 3.0, KEH_K, "nunito9", "sag")[0])
        s.ekle(_cizim(*c["sol_cizim"], 38.0, y0, "sol") + _cizim(*c["sag_cizim"], 172.0, y0, "sag"))
        sol_svg, sx0, sx1 = KC.yazi(c["sol"], A_X - GUVEN, ys, boy, OBS, FONT, "sag")
        sag_svg, gx0, gx1 = KC.yazi(c["sag"], B_X + GUVEN, ys, boy, OBS, FONT, "sol")
        orta_svg, ox0, ox1 = _yasli_orta(c["orta"], ys, boy)
        s.ekle(sol_svg + sag_svg + orta_svg)
        sekil, yazi_svg = _kurdele(y0 + 41.8)
        s.dikis(sekil)
        s.dikis(yazi_svg, yazi_mi=True)
        mh = muhur_svg().replace("<svg ", f'<svg x="123.4" y="{KC.f(y0 + 1.0)}" width="11.4" height="11.4" ', 1)
        s.ekle(KC._orta_kart(y0 + 2.5, y0 + 26.0, "ÖNCE TAHMİN ET", ["Yanlış sözcükler:"], [c["ipucu"]]) + mh)
        s.ekle(KC._orta_kart(y0 + 36.6, y0 + 47.2, "AÇ VE AÇIKLA", soru="Neden yanlıştı?"))
        s.ekle(KC._ogr_grubu(c["kod"], katli(c), c["orta"],
                             KC._orta_cevap(y0 + 2.5, y0 + 26.0, ["Yanlış sözcükler:"], [c["orta"].rstrip(",")])
                             + KC._orta_cevap(y0 + 36.6, y0 + 47.2, soru="Neden yanlıştı?", soru_cevap=c["neden"])))
        bilgi.append(dict(kod=c["kod"], boy=boy, sol=(sx0, sx1), orta=(ox0, ox1), sag=(gx0, gx1)))
    KC._alt_bolum(s, "", "Kat izini tırnağınla keskinleştir.", "Katlayınca YANLIŞ mühürleri saklanır.", 1)
    return s, bilgi
