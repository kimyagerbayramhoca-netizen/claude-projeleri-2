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
  {{katla-cumle}}       kat sayfası "Katla, doğrusu kalsın!" (uretec/katla_unite.py · satırlar KATLA_CUMLE)
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

# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / 1600
# Yeni düzen (26 sayfa): her durak iki sayfa (sol: bant + büyük çizim · sağ: tekrar + köşeyi katla); 3B açılımı s.8–9;
# kat yaprağı s.17 (kat sayfası) + s.18 (karma sayfa, arka yüz). Köşesi katlanan sağ sayfalar: 3 5 7 9 11 13 15.
SAYFA = {
    1: ('Yola çıkış', 'Şanlıurfa–Harran yolu · yola çıkış', 0),
    2: ('1. durak · <b>Göbeklitepe</b>', '1. durak · Atom modellerinin yolculuğu', 0),
    3: ('1. durak · <b>Göbeklitepe</b>', '1. durak · Model zinciri: tekrar ve köşe', 3),
    4: ('2. durak · <b>Harran</b>', '2. durak · Altın levha çizgi romanı', 6),
    5: ('2. durak · <b>Harran</b>', '2. durak · Çekirdek, katmanlar, elektron bulutu', 8),
    6: ('3. durak · <b>Höyük</b>', '3. durak · Enerji merdiveni ve ışık', 14),
    7: ('3. durak · <b>Höyük</b>', '3. durak · Orbitaller, lamba spektrumu', 18),
    8: ('3. durak · <b>3B</b>', '3B · Orbitaller üç boyutta', 21),
    9: ('3. durak · <b>3B</b>', '3B · Alfa tanecikleri üç boyutta', 21),
    10: ('4. durak · <b>Urfa çarşısı</b>', '4. durak · p, n, e ve iyonlar', 21),
    11: ('4. durak · <b>Urfa çarşısı</b>', '4. durak · Tanecikler ve izo kardeşler', 25),
    12: ('5. durak · <b>Halfeti</b>', '5. durak · Elektron dizilimi kuralları', 29),
    13: ('5. durak · <b>Halfeti</b>', '5. durak · Aufbau, Pauli, Hund: tekrar', 32),
    14: ('6. durak · <b>Fırat kıyısı</b>', '6. durak · Değerlik elektronu, küresel simetri', 36),
    15: ('6. durak · <b>Fırat kıyısı</b>', '6. durak · Dış katman konuşuyor', 40),
    16: ('Hülasa · <b>Gümrük Hanı</b>', 'Hülasa · atomun özeti', 44),
    17: ('Hülasa · <b>Katla</b>', 'Katla sayfası · doğrusu kalsın', 46),
    18: ('Hülasa · <b>Karma</b>', 'Karma sayfa · kapıyı aç', 49),
    19: ('Yan yol · <b>Sıra gecesi</b>', 'Yan yol 1 · Meclis: kim haklı?', 59),
    20: ('Yan yol · <b>Harran Ovası</b>', 'Yan yol 2 · Kıssalar', 66),
    21: ('Yan yol · <b>Urfa evleri</b>', 'Yan yol 3 · Anahtar merdiveni', 74),
    22: ('<b>Urfa Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 81),
    23: ('<b>Urfa Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 91),
    24: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    25: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    26: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD ilerleme noktaları: 6 durak + Hülasa + 3 yan yol + kale; 3B yanındaki durağın, kat ve karma Hülasa'nın noktasında
SIMDI = {1: -1, 2: 0, 3: 0, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 4, 13: 4, 14: 5, 15: 5,
         16: 6, 17: 6, 18: 6, 19: 7, 20: 8, 21: 9, 22: 10, 23: 10, 24: 11, 25: 11, 26: 11}

u = KO.Unite(__file__, SAYFA, SIMDI)
import sahneler_unite as SU  # noqa: E402  (Unite uretec'i sys.path'e ekledikten sonra)

# ------------------------------------------------------------------ açılış panoramasının durak etiketleri
# anahtar: (üst satır, ad, alt [sayfa · akçe], tür, (sol mm, üst mm) rozet merkezine göre)
ETIKET = {
    "1": ("1. DURAK · GÖBEKLİTEPE", "Fikirlerin yolculuğu", "2–3|+100 akçe", "durak", (-50, 4.4)),
    "2": ("2. DURAK · HARRAN", "Çekirdek ve katmanlar", "4–5|+120 akçe", "durak", (-52, -4.4)),
    "3": ("3. DURAK · HARRAN HÖYÜĞÜ", "Işık ve orbitaller · 3B", "6–9|+120 akçe", "durak", (-52, -4.4)),
    "4": ("4. DURAK · URFA ÇARŞISI", "p, n, e ve iyonlar", "10–11|+120 akçe", "durak", (4.4, -4.4)),
    "5": ("5. DURAK · HALFETİ", "Dizilim kuralları", "12–13|+120 akçe", "durak", (4.4, -4.4)),
    "6": ("6. DURAK · FIRAT KIYISI", "Değerlik ve simetri", "14–15|+120 akçe", "durak", (4.4, -2.6)),
    "H": ("GÜMRÜK HANI", "Hülasa · katla · karma", "16–18|+240 akçe", "hul", (-40, -4.2)),
    "M": ("SIRA GECESİ", "Meclis: Kim haklı?", "19|+120 akçe", "yan", (-48, -4.2)),
    "K": ("HARRAN OVASI", "Kıssa", "20|+120 akçe", "yan", (-36, -3)),
    "A": ("URFA EVLERİ", "Anahtar merdiveni", "21|+120 akçe", "yan", (-44, -4.2)),
    "V": ("URFA KALESİ", "Büyük İmtihan", "22–23|+300 akçe", "kale", (-49, -14)),
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
    """Dikey ok: gövde ve uç ÇİZGİ (fotokopide dolgular açılır, çizgiler koyu kalır); fonttaki ↑↓ işaretine bağlı değil."""
    u = (f'M{f(x - 3.4)} {f(y0 + 4.8)} L{f(x)} {f(y0 + .8)} L{f(x + 3.4)} {f(y0 + 4.8)}' if yukari else
         f'M{f(x - 3.4)} {f(y1 - 4.8)} L{f(x)} {f(y1 - .8)} L{f(x + 3.4)} {f(y1 - 4.8)}')
    return (f'<path d="M{f(x)} {f(y0 + 1)} V{f(y1 - 1)}" stroke="{OBS}" stroke-width="2" stroke-linecap="round"/>'
            f'<path d="{u}" fill="none" stroke="{OBS}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')


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
    return f'<span class="iz"><span class="izo"><span>{A}</span><span>{Z}</span></span>{sembol}{y}</span>'


def rozet_tik():
    """Cevaplar levhası için yazısız rozet: göbekte çizgi tik (✓ fontta yok)."""
    tik = '<path d="M37 51 L46 60 L64 41" fill="none" stroke="#1B1D26" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    return U.durak_rozeti(u.yeni("dr"), tik, "", *KO.RENK["gol"])


def rozet_yildiz(renk="keh"):
    """Final levhası için yazısız rozet: göbekte sekiz köşeli yıldız (★ fontta yok)."""
    y = f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 15), True)}" fill="#F0A21A" stroke="#1B1D26" stroke-width="2.2" stroke-linejoin="round"/>'
    return U.durak_rozeti(u.yeni("dr"), y, "", *KO.RENK[renk])


import hazine_yapragi as _HY  # noqa: E402  (kesme yaprağı)
_yaprak = _HY.yaprak_html
# kesme yaprağının üst satırına uzun rota adı sığmıyor: "Yol 3 · Şanlıurfa–Harran"
_HY.yaprak_html = lambda birim: (_yaprak(birim)
                                 .replace("<span>Yol 3 · Şanlıurfa–Harran Yolu</span>", "<span>Yol 3 · Şanlıurfa–Harran</span>")
                                 .replace("</head>", "<style>.hy-kart { zoom: 1.06; }</style></head>", 1))


def katla_cumle():
    """{{katla-cumle}}: "Katla, doğrusu kalsın!" (katla_unite.py; ortak katla parçaları). Kat sayfası TEK numaralı sayfadır."""
    import katla_unite as KU
    u._sag_sayfa_denetle("kat sayfası")
    rozet = u.yt["rozet"](str(u.meta["yol"]), "YOL")
    s, _ = KU.cumle_sayfasi(u.yeni("kc"), rozet, lambda: muhur("yanlis"), rota="Yol 3 · Şanlıurfa–Harran")
    return s.cikti()


u.yer_tutucu("panorama", panorama)
u.yer_tutucu("panorama-etiket", panorama_etiket)
u.yer_tutucu("final", final)
u.yer_tutucu("muhur", muhur)
u.yer_tutucu("orb", lambda kodlar, cls="orb": orb_svg(kodlar, cls))
u.yer_tutucu("iz", iz)
u.yer_tutucu("rozet-tik", rozet_tik)
u.yer_tutucu("rozet-yildiz", rozet_yildiz)
u.yer_tutucu("katla-cumle", katla_cumle)

if __name__ == "__main__":
    u.calistir()
