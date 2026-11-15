#!/usr/bin/env python3
"""Kimyasal Değişimler · Kars–Erzurum Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
açılış panoramasının durak etiketleri, mühürdeki rota adı ve final sahnesi (Kars Kalesi burcu).
Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır; sahneler uretec/sahneler_unite.py'dedir.
"""
import os
import re
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
from cizim import sus as U  # noqa: E402
from cizim.temel import f  # noqa: E402

# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / 1400
SAYFA = {
    1: ('Yola çıkış', 'Kars–Erzurum yolu · yola çıkış', 0),
    2: ('1. durak · <b>Çıldır Gölü</b>', '1. durak · Fiziksel mi, kimyasal mı?', 0),
    3: ('2. durak · <b>Kars</b>', '2. durak · Tepkime denklemi', 7),
    4: ('3. durak · <b>Ani</b>', '3. durak · Asit-baz tepkimeleri', 16),
    5: ('4. durak · <b>Sarıkamış</b>', '4. durak · Yanma, sentez, analiz', 24),
    6: ('5. durak · <b>Pasinler</b>', '5. durak · Çökelme tepkimeleri', 33),
    7: ('6. durak · <b>Erzurum</b>', '6. durak · İndirgenme-yükseltgenme', 41),
    8: ('Hülasa · <b>Palandöken</b>', 'Hülasa · tepkimelerin özeti', 50),
    9: ('Yan yol · <b>Doğu Ekspresi</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    10: ('Yan yol · <b>Çobandede</b>', 'Yan yol 2 · Kıssalar', 61),
    11: ('Yan yol · <b>Kars Garı</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    12: ('<b>Kars Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    13: ('<b>Kars Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
    14: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    15: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    16: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD ilerleme noktaları: 6 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 11: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 10, 14: 11, 15: 11, 16: 11}

u = KO.Unite(__file__, SAYFA, SIMDI)
import sahneler_unite as SU  # noqa: E402  (Unite uretec'i sys.path'e ekledikten sonra)

# ------------------------------------------------------------------ açılış panoramasının durak etiketleri
# anahtar: (üst satır, ad, alt [sayfa · akçe], tür, (sol mm, üst mm) rozet merkezine göre)
ETIKET = {
    "1": ("1. DURAK · ÇILDIR GÖLÜ", "Ne değişti?", "2|+100 akçe", "durak", (-45.5, -4.4)),
    "2": ("2. DURAK · KARS", "Tepkime denklemi", "3|+120 akçe", "durak", (-41, -4.4)),
    "3": ("3. DURAK · ANİ", "Asit ve baz", "4|+120 akçe", "durak", (-31, -13.6)),
    "4": ("4. DURAK · SARIKAMIŞ", "Yanma, sentez, analiz", "5|+120 akçe", "durak", (-18, 4.6)),
    "5": ("5. DURAK · PASİNLER", "Çökelme", "6|+120 akçe", "durak", (-17, -13.6)),
    "6": ("6. DURAK · ERZURUM", "Elektron alışverişi", "7|+120 akçe", "durak", (-24, -13.6)),
    "H": ("PALANDÖKEN", "Hülasa", "8|+40 akçe", "hul", (4.4, -4.2)),
    "M": ("DOĞU EKSPRESİ", "Meclis: Kim haklı?", "9|+120 akçe", "yan", (-16, 4.4)),
    "K": ("ÇOBANDEDE KÖPRÜSÜ", "Kıssa", "10|+120 akçe", "yan", (-14, 4.4)),
    "A": ("KARS GARI", "Anahtar merdiveni", "11|+120 akçe", "yan", (-20, 4.4)),
    "V": ("KARS KALESİ", "Büyük İmtihan", "12–13|+300 akçe", "kale", (-41, -2.2)),
}


def panorama():
    return SU.panorama_kars()[0]


def panorama_etiket():
    """HTML durak etiketleri: konumlar sahnenin DURAKLAR listesinden; sayfa no kaymalı (YEREL_SAYFA_BASLANGIC)."""
    out = []
    for k, x, y, _t in SU.DURAKLAR:
        ust, ad, alt_, cls, (dx, dy) = ETIKET[k]
        sayfa, akce = alt_.split("|")
        sayfa = re.sub(r"\d+", lambda m: str(u.sayfa_no(int(m.group()))), sayfa)
        cls = {"durak": "", "hul": "hul", "yan": "yan", "kale": "kale"}[cls]
        out.append(f'<div class="durak-et {cls}" style="left:{f(x / 10 + dx, 2)}mm;top:{f(y / 10 + dy, 2)}mm"><i>{ust} · s.{sayfa}</i><b>{ad}<small>{akce}</small></b></div>'
                   .replace('class="durak-et "', 'class="durak-et"'))
    return "".join(out)


def final():
    """Final sahnesi: Kars Kalesi burcunda bayraklı Pamuk + meta.json nişanlarından çelenk."""
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
    return SU.final_kars(nisanlar=ns)


def muhur(tur, boy=""):
    """YANLIŞ / DOĞRU mührü; alt yayda bu yolun adı."""
    return U.muhur(u.yeni("mh"), tur, alt="KARS–ERZURUM YOLU")


def _rozet_duzelt(html):
    """Ortak hazine rozetinde yazı boyu sabit (30): üç haneli kodlar (H10–H12) dairenin dışına taşar. Burada küçültülür."""
    return re.sub(r'<text x="50" y="60" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">(H\d\d)</text>',
                  r'<text x="50" y="58" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="23" fill="#1B1D26">\1</text>', html)


_html_kur = u.html_kur
u.html_kur = lambda: _rozet_duzelt(_html_kur())
import hazine_yapragi as _HY  # noqa: E402  (hazine-kartlari.html de aynı rozeti kullanır)
_yaprak = _HY.yaprak_html
# kesme yaprağının üst satırına uzun rota adı sığmıyor: "Yol 1 · Kars–Erzurum"
# ve iki satıra kayan formüllü kartlar (H1, H2, H6, H7, H8, H11, H12) 1,3 kat büyütmeyle hücreden taşıyor: büyütme 1,06
_HY.yaprak_html = lambda birim: (_rozet_duzelt(_yaprak(birim))
                                 .replace("<span>Yol 1 · Kars–Erzurum Yolu</span>", "<span>Yol 1 · Kars–Erzurum</span>")
                                 .replace("</head>", "<style>.hy-kart { zoom: 1.06; }</style></head>", 1))

u.yer_tutucu("panorama", panorama)
u.yer_tutucu("panorama-etiket", panorama_etiket)
u.yer_tutucu("final", final)
u.yer_tutucu("muhur", muhur)

if __name__ == "__main__":
    u.calistir()
