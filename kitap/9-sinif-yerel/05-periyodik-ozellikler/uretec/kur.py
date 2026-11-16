#!/usr/bin/env python3
"""Periyodik Özellikler · Maden Yolu II · Doğu Anadolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
açılış haritasının etiketleri, final sahnesi (Divriği Kalesi burcu) ve 4 × 2 nişan sayımı.
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
from cizim import sus as U  # noqa: E402
from cizim.temel import f  # noqa: E402

# no: (HUD'daki yer, altbilgideki konu, akçe çubuğu %) — çubuk: o sayfanın başına kadar alınabilecek en çok akçe / 1400
SAYFA = {
    1: ("Yola çıkış", "Maden Yolu II · yola çıkış", 0),
    2: ("1. durak · <b>Divriği</b>", "1. durak · Atom yarıçapı", 0),
    3: ("2. durak · <b>Guleman</b>", "2. durak · İyon yarıçapı", 7),
    4: ("3. durak · <b>Maden</b>", "3. durak · İyonlaşma enerjisi", 16),
    5: ("4. durak · <b>Hazar Gölü</b>", "4. durak · Ardışık iyonlaşma enerjileri", 24),
    6: ("5. durak · <b>Keban Baraj Gölü</b>", "5. durak · Elektronegatiflik", 33),
    7: ("6. durak · <b>Keban</b>", "6. durak · Metalik ve ametalik karakter", 41),
    8: ("Hülasa · <b>Fırat kıyısı</b>", "Hülasa · eğilimler özeti", 50),
    9: ("Yan yol · <b>Kemaliye</b>", "Yan yol 1 · Meclis: kim haklı?", 53),
    10: ("Yan yol · <b>Karanlık Kanyon</b>", "Yan yol 2 · Kıssalar", 61),
    11: ("Yan yol · <b>Kale yokuşu</b>", "Yan yol 3 · Anahtar merdiveni", 70),
    12: ("<b>Divriği Kalesi</b> · 1/2", "Büyük İmtihan · 1. bölüm", 79),
    13: ("<b>Divriği Kalesi</b> · 2/2", "Büyük İmtihan · 2. bölüm", 89),
    14: ("<b>Üstad</b> · bonus", "Üstad soruları · bonus", 100),
    15: ("<b>Cevaplar</b>", "Cevaplar ve çözümler", 100),
    16: ("<b>Final</b>", "Final · akçe rayı ve unvan", 100),
}
# HUD ilerleme noktaları: 6 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 11: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 10, 14: 11, 15: 11, 16: 11}

u = KO.Unite(__file__, SAYFA, SIMDI)

# ------------------------------------------------------------------ açılış haritasının etiketleri (HTML; sayfa no kaymalı)
# rozet merkezine göre (sol mm, üst mm) ofsetleri; konumlar sahneler_unite.HARITA'dan
ETIKET_YERI = {"1": (4.6, -12.6), "2": (-49, -16.4), "3": (-20, 5), "4": (-43, -14.6), "5": (4.4, -13.8), "6": (-50.5, 2.6), "K": (-17, -17.2)}


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
    """Final bandı: Divriği Kalesi burcunda bayraklı Pamuk + meta.json nişanlarından çelenk."""
    import sahneler_unite as SU
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
    return SU.divrigi_final(nisanlar=ns)


def nisan_sayim():
    """Final nişan sayımı: 8 nişan 4 × 2 ızgarada (8 sütunda adlar sıkışır)."""
    ic = "".join(f'<div>{u.yt["nisan"](x["ikon"])}<b>{KO.zengin(x["ad"])}</b><small><span class="kutucuk"></span></small></div>'
                 for x in u.meta["nisanlar"])
    return f'<div class="nisan-say" style="grid-template-columns:repeat(4,minmax(0,1fr));row-gap:1.2mm">{ic}</div>'


_hazine_yapragi = u.hazine_yapragi


def hazine_yapragi_kisa():
    """Kesme yaprağı (ortak hazine_yapragi.py) hücre başlığında rota adını kullanır; uzun ad ("… · Doğu Anadolu") iki satıra
    kırılıp kartları alttaki hücreye itiyor. Yaprak kurulurken yalnız kısa adı (meta.hud: "Maden Yolu II") kullan."""
    eski = u.meta["rota"]
    u.meta["rota"] = u.meta.get("hud") or eski
    try:
        return _hazine_yapragi()
    finally:
        u.meta["rota"] = eski


u.hazine_yapragi = hazine_yapragi_kisa
u.yer_tutucu("nisan-sayim", nisan_sayim)
u.yer_tutucu("harita-etiket", harita_etiket)
u.yer_tutucu("final", final)

if __name__ == "__main__":
    u.calistir()
