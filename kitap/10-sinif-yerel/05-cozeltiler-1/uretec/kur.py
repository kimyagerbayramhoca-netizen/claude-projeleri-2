#!/usr/bin/env python3
"""Çözünme ve Çözünürlük · Pamukkale–Afyon Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
açılış haritasının etiketleri ({{harita-etiket}}) ve Afyon kalesi burcundaki final sahnesi ({{final}} geçersiz kılınır).
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
    1: ("Yola çıkış", "Pamukkale–Afyon yolu · yola çıkış", 0),
    2: ("1. durak · <b>Pamukkale</b>", "1. durak · Çözünme nasıl olur?", 0),
    3: ("2. durak · <b>Karahayıt</b>", "2. durak · Benzer benzeri çözer", 7),
    4: ("3. durak · <b>Acıgöl</b>", "3. durak · İyonlar ve iletkenlik", 16),
    5: ("4. durak · <b>Ömer–Gecek</b>", "4. durak · Çözünürlük ve etkenleri", 24),
    6: ("5. durak · <b>Gazlıgöl</b>", "5. durak · Doygunluk ve hız", 33),
    7: ("6. durak · <b>Afyon çarşısı</b>", "6. durak · Çözünürlük hesapları", 41),
    8: ("Hülasa · <b>Frig Vadisi</b>", "Hülasa · çözelti özeti", 50),
    9: ("Yan yol · <b>Afyon evi</b>", "Yan yol 1 · Meclis: kim haklı?", 53),
    10: ("Yan yol · <b>İscehisar</b>", "Yan yol 2 · Kıssalar", 61),
    11: ("Yan yol · <b>Kale merdivenleri</b>", "Yan yol 3 · Anahtar merdiveni", 70),
    12: ("<b>Afyonkarahisar Kalesi</b> · 1/2", "Büyük İmtihan · 1. bölüm", 79),
    13: ("<b>Afyonkarahisar Kalesi</b> · 2/2", "Büyük İmtihan · 2. bölüm", 89),
    14: ("<b>Üstad</b> · bonus", "Üstad soruları · bonus", 100),
    15: ("<b>Cevaplar</b>", "Cevaplar ve çözümler", 100),
    16: ("<b>Final</b>", "Final · akçe rayı ve unvan", 100),
}
# HUD ilerleme noktaları: 6 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 11: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 10, 14: 11, 15: 11, 16: 11}

u = KO.Unite(__file__, SAYFA, SIMDI)

# ------------------------------------------------------------------ açılış haritasının etiketleri (HTML; sayfa no kaymalı)
# rozet merkezine göre (sol mm, üst mm) ofsetleri; konumlar sahneler_unite.HARITA'dan
ETIKET_YERI = {"1": (-29, -13.5), "2": (4.2, -10), "3": (-18, -13), "4": (-41, -10), "5": (-41, -10), "6": (-34.5, 6), "K": (-37, -18)}


def harita_etiket():
    import sahneler_unite as SU
    out = []
    for i, d in enumerate(u.meta["duraklar"]):
        k = str(i + 1)
        x, y = SU.HARITA[k]
        dx, dy = ETIKET_YERI[k]
        ust = f'{k}. DURAK · {KO.tr_buyuk(d["yer"])} · s.{u.sayfa_no(d["sayfa"])}'
        out.append(f'<div class="durak-et" style="left:{f(x / 10 + dx, 2)}mm;top:{f(y / 10 + dy, 2)}mm"><i>{ust}</i>'
                   f'<b>{KO.zengin(d["baslik"])}<small>+{d["akce"]} akçe</small></b></div>')
    x, y = SU.HARITA["K"]
    dx, dy = ETIKET_YERI["K"]
    out.append(f'<div class="durak-et kale" style="left:{f(x / 10 + dx, 2)}mm;top:{f(y / 10 + dy, 2)}mm"><i>KALE · s.{u.sayfa_no(12)}–{u.sayfa_no(13)}</i>'
               f'<b>{u.meta["kale"]}<small>+300 akçe</small></b></div>')
    return "".join(out)


def final():
    """Final bandı: Afyon kalesi burcunda bayraklı Pamuk + meta.json nişanlarından çelenk."""
    import sahneler_unite as SU
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
    return SU.afyon_final(nisanlar=ns)


def nisan_sayim():
    """Final nişan sayımı: 8 nişan 8 sütunda adları sıkıştırır; 4 × 2 ızgarada okunur."""
    ic = "".join(f'<div>{u.yt["nisan"](x["ikon"])}<b>{KO.zengin(x["ad"])}</b><small><span class="kutucuk"></span></small></div>'
                 for x in u.meta["nisanlar"])
    return f'<div class="nisan-say" style="grid-template-columns:repeat(4,minmax(0,1fr));row-gap:1.2mm">{ic}</div>'


u.yer_tutucu("nisan-sayim", nisan_sayim)
u.yer_tutucu("harita-etiket", harita_etiket)
u.yer_tutucu("final", final)

if __name__ == "__main__":
    u.calistir()
