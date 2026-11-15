#!/usr/bin/env python3
"""Atom ve Yapısı · Şanlıurfa–Harran Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
açılış panoramasının durak etiketleri, final sahnesi, mühürdeki rota adı ve üç küçük yer tutucu:
  {{orb|ud,u,0}}        orbital şeması (kutu + ok; ok çizgidir, fonta bağlı değil): ud ↑↓ · u ↑ · d ↓ · 0 boş
  {{iz|35|17|Cl|−}}     çekirdek gösterimi (kütle no üstte, atom no altta, isteğe bağlı yük)
  {{rozet-tik}} {{rozet-yildiz|renk}}   yazısız (çizgi) rozetler: fontta olmayan ✓ ★ yerine
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
from cizim.temel import f, cizgi_d, selcuklu_yildizi  # noqa: E402

# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / 1400
SAYFA = {
    1: ('Yola çıkış', 'Şanlıurfa–Harran yolu · yola çıkış', 0),
    2: ('1. durak · <b>Göbeklitepe</b>', '1. durak · Atom modellerinin yolculuğu', 0),
    3: ('2. durak · <b>Harran</b>', '2. durak · Çekirdek, katmanlar, elektron bulutu', 7),
    4: ('3. durak · <b>Harran Höyüğü</b>', '3. durak · Işık, enerji düzeyleri, orbitaller', 16),
    5: ('4. durak · <b>Urfa çarşısı</b>', '4. durak · p, n, e ve iyonlar', 24),
    6: ('5. durak · <b>Halfeti</b>', '5. durak · Elektron dizilimi kuralları', 33),
    7: ('6. durak · <b>Fırat kıyısı</b>', '6. durak · Değerlik elektronu, küresel simetri', 41),
    8: ('Hülasa · <b>Gümrük Hanı</b>', 'Hülasa · atomun özeti', 50),
    9: ('Yan yol · <b>Sıra gecesi</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    10: ('Yan yol · <b>Harran Ovası</b>', 'Yan yol 2 · Kıssalar', 61),
    11: ('Yan yol · <b>Urfa evleri</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    12: ('<b>Urfa Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    13: ('<b>Urfa Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
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
    "1": ("1. DURAK · GÖBEKLİTEPE", "Fikirlerin yolculuğu", "2|+100 akçe", "durak", (-19, -13.8)),
    "2": ("2. DURAK · HARRAN", "Çekirdek ve katmanlar", "3|+120 akçe", "durak", (-46.5, -4.4)),
    "3": ("3. DURAK · HARRAN HÖYÜĞÜ", "Işık ve orbitaller", "4|+120 akçe", "durak", (-21, 4.4)),
    "4": ("4. DURAK · URFA ÇARŞISI", "p, n, e ve iyonlar", "5|+120 akçe", "durak", (4.6, -4.4)),
    "5": ("5. DURAK · HALFETİ", "Dizilim kuralları", "6|+120 akçe", "durak", (4.4, -4.4)),
    "6": ("6. DURAK · FIRAT KIYISI", "Değerlik ve simetri", "7|+120 akçe", "durak", (4.4, -4.4)),
    "H": ("GÜMRÜK HANI", "Hülasa", "8|+40 akçe", "hul", (-31, -4.2)),
    "M": ("SIRA GECESİ", "Meclis: Kim haklı?", "9|+120 akçe", "yan", (-44, -4.2)),
    "K": ("HARRAN OVASI", "Kıssa", "10|+120 akçe", "yan", (-26, 4.2)),
    "A": ("URFA EVLERİ", "Anahtar merdiveni", "11|+120 akçe", "yan", (-17, 4.4)),
    "V": ("URFA KALESİ", "Büyük İmtihan", "12–13|+300 akçe", "kale", (-36, -13.4)),
}


def panorama():
    return SU.panorama_urfa()


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
    """Final sahnesi: Urfa Kalesi burcunda bayraklı Pamuk + meta.json nişanlarından çelenk."""
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
    return SU.final_urfa(nisanlar=ns)


def muhur(tur, boy=""):
    """YANLIŞ / DOĞRU mührü; alt yayda bu yolun adı."""
    return U.muhur(u.yeni("mh"), tur, alt="ŞANLIURFA–HARRAN")


# ------------------------------------------------------------------ orbital şeması ve çekirdek gösterimi

OBS = "#1B1D26"


def _ok(x, y0, y1, yukari=True):
    """Dikey ok (çizgi + üçgen uç); fonttaki ↑↓ işaretine bağlı değil."""
    if yukari:
        return (f'<path d="M{f(x)} {f(y1)} V{f(y0 + 4.5)}" stroke="{OBS}" stroke-width="2" stroke-linecap="round"/>'
                f'<path d="M{f(x - 3.6)} {f(y0 + 5.2)} L{f(x)} {f(y0)} L{f(x + 3.6)} {f(y0 + 5.2)} Z" fill="{OBS}"/>')
    return (f'<path d="M{f(x)} {f(y0)} V{f(y1 - 4.5)}" stroke="{OBS}" stroke-width="2" stroke-linecap="round"/>'
            f'<path d="M{f(x - 3.6)} {f(y1 - 5.2)} L{f(x)} {f(y1)} L{f(x + 3.6)} {f(y1 - 5.2)} Z" fill="{OBS}"/>')


def orb_svg(kodlar, cls="orb", renk="#FFFFFF"):
    """'ud,u,0' → kutular: ud ↑↓ · u ↑ · d ↓ · 0 boş. Kutu 20×22 birim, bitişik."""
    kod = [k.strip() for k in str(kodlar).split(",") if k.strip()]
    w = 20 * len(kod) + 2
    o = [f'<rect x="1" y="1" width="{w - 2}" height="22" fill="{renk}" stroke="{OBS}" stroke-width="1.6"/>']
    for i, k in enumerate(kod):
        x0 = 1 + 20 * i
        if i:
            o.append(f'<path d="M{x0} 1 V23" stroke="{OBS}" stroke-width="1.6"/>')
        if k == "ud":
            o.append(_ok(x0 + 6.5, 4, 20, True) + _ok(x0 + 13.5, 4, 20, False))
        elif k == "u":
            o.append(_ok(x0 + 10, 4, 20, True))
        elif k == "d":
            o.append(_ok(x0 + 10, 4, 20, False))
        elif k != "0":
            raise ValueError(f"orbital kodu: {k}")
    return f'<svg class="{cls}" viewBox="0 0 {w} 24" data-orb="{",".join(kod)}">{"".join(o)}</svg>'


def iz(A, Z, sembol, yuk=""):
    """Çekirdek gösterimi: üstte kütle numarası, altta atom numarası (HTML; SVG değil)."""
    y = f"<sup>{yuk}</sup>" if yuk else ""
    return f'<span class="iz"><span class="iz-s"><i>{A}</i><i>{Z}</i></span>{sembol}{y}</span>'


def rozet_tik():
    """Cevaplar levhası için yazısız rozet: göbekte çizgi tik (✓ fontta yok)."""
    tik = '<path d="M37 51 L46 60 L64 41" fill="none" stroke="#1B1D26" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    return U.durak_rozeti(u.yeni("dr"), tik, "", *KO.RENK["gol"])


def rozet_yildiz(renk="keh"):
    """Final levhası için yazısız rozet: göbekte sekiz köşeli yıldız (★ fontta yok)."""
    y = f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 15), True)}" fill="#F0A21A" stroke="#1B1D26" stroke-width="2.2" stroke-linejoin="round"/>'
    return U.durak_rozeti(u.yeni("dr"), y, "", *KO.RENK[renk])


def _rozet_duzelt(html):
    """Ortak hazine rozetinde yazı boyu sabit (30): üç haneli kodlar (H10–H12) dairenin dışına taşar. Burada küçültülür."""
    return re.sub(r'<text x="50" y="60" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="#1B1D26">(H\d\d)</text>',
                  r'<text x="50" y="58" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="23" fill="#1B1D26">\1</text>', html)


_html_kur = u.html_kur
u.html_kur = lambda: _rozet_duzelt(_html_kur())
import hazine_yapragi as _HY  # noqa: E402  (hazine-kartlari.html de aynı rozeti kullanır)
_yaprak = _HY.yaprak_html
# kesme yaprağının üst satırına uzun rota adı sığmıyor: "Yol 3 · Şanlıurfa–Harran"
_HY.yaprak_html = lambda birim: (_rozet_duzelt(_yaprak(birim))
                                 .replace("<span>Yol 3 · Şanlıurfa–Harran Yolu</span>", "<span>Yol 3 · Şanlıurfa–Harran</span>")
                                 .replace("</head>", "<style>.hy-kart { zoom: 1.06; }</style></head>", 1))

u.yer_tutucu("panorama", panorama)
u.yer_tutucu("panorama-etiket", panorama_etiket)
u.yer_tutucu("final", final)
u.yer_tutucu("muhur", muhur)
u.yer_tutucu("orb", lambda kodlar, cls="orb": orb_svg(kodlar, cls))
u.yer_tutucu("iz", iz)
u.yer_tutucu("rozet-tik", rozet_tik)
u.yer_tutucu("rozet-yildiz", rozet_yildiz)

if __name__ == "__main__":
    u.calistir()
