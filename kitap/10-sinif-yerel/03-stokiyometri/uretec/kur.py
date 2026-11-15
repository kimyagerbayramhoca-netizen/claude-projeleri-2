#!/usr/bin/env python3
"""Stokiyometri · Dicle Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası
ve üniteye özel yer tutucular:
  {{dicle-etiket}}   açılış panoramasının (sahneler_unite.panorama_dicle) durak etiketleri
  {{muhur|…}}        mühür alt yazısı "DİCLE YOLU" (ortak mühür "VAN GÖLÜ TURU" yazıyor)
  {{mol|…}}          ortak moleküllere ek olarak H2 ve C4H10 (sahneler_unite.YEREL_MOLEKUL)
  {{final}}          Dicle finali (sahneler_unite.final_dicle): bazalt burç, nişan çelengi
Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır; sahneler uretec/sahneler_unite.py'dedir.
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
    1: ('Yola çıkış', 'Dicle yolu · yola çıkış', 0),
    2: ('1. durak · <b>Çayönü</b>', '1. durak · Tepkime denklemi ve korunum', 0),
    3: ('2. durak · <b>Hevsel</b>', '2. durak · Denklemleri denkleştirme', 7),
    4: ('3. durak · <b>Malabadi</b>', '3. durak · Denklemden hesaba', 16),
    5: ('4. durak · <b>Batman</b>', '4. durak · Sınırlayıcı bileşen', 24),
    6: ('5. durak · <b>Hasankeyf</b>', '5. durak · Verim ve saflık', 33),
    7: ('6. durak · <b>Bakırcılar</b>', '6. durak · Karışımlar ve ardışık tepkimeler', 41),
    8: ('Hülasa · <b>Dicle kıyısı</b>', 'Hülasa · stokiyometri özeti', 50),
    9: ('Yan yol · <b>Hasan Paşa Hanı</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    10: ('Yan yol · <b>On Gözlü Köprü</b>', 'Yan yol 2 · Kıssalar', 61),
    11: ('Yan yol · <b>Surların eteği</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    12: ('<b>Diyarbakır Surları</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    13: ('<b>Diyarbakır Surları</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
    14: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    15: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    16: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD ilerleme noktaları: 6 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 11: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 10, 14: 11, 15: 11, 16: 11}

u = KO.Unite(__file__, SAYFA, SIMDI)
import sahneler_unite as SU  # noqa: E402  (KO.Unite uretec/'i sys.path'e ekledi)


def muhur(tur, boy=""):
    """Ortak mühür + bu ünitenin rota adı (alt yazı)."""
    return U.muhur(u.yeni("mh"), tur, alt="DİCLE YOLU")


_ortak_mol = u.yt["mol"]


def mol(ad, donus="0,0,0", en="", etiket="", ion=""):
    """Ortak {{mol}} + yerel geometriler (H2, C4H10)."""
    if ad in SU.YEREL_MOLEKUL:
        rx, ry, rz = (float(v) for v in donus.split(","))
        svg = SU.yerel_molekul_svg(u.yeni("mol"), ad, (rx, ry, rz), etiket=bool(etiket))
        return svg.replace("<svg ", f'<svg style="width:{en}" ', 1) if en else svg
    return _ortak_mol(ad, donus, en, etiket, ion)


def final():
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
    return SU.final_dicle(nisanlar=ns)


def dicle_etiket():
    """Açılış panoramasındaki durak / yan yol / kale etiketleri (HTML; konum sahnenin koordinatlarından, sayfa no kaymalı)."""
    _, konum = SU.panorama_dicle()
    out = []
    for k, ust, ad, sayfa, akce, tur, dx, dy in SU.PANORAMA_ETIKET:
        x, y = konum[k]
        s_ = "–".join(str(u.sayfa_no(int(p))) for p in str(sayfa).split("-"))
        cls = {"durak": "", "hulasa": " hul", "yan": " yan", "kale": " kale"}[tur]
        out.append(f'<div class="durak-et{cls}" style="left:{f(x / 10 + dx, 2)}mm;top:{f(y / 10 + dy, 2)}mm">'
                   f'<i>{ust} · s.{s_}</i><b>{ad}<small>{akce}</small></b></div>')
    return "".join(out)


u.yer_tutucu("muhur", muhur)
u.yer_tutucu("mol", mol)
u.yer_tutucu("final", final)
u.yer_tutucu("dicle-etiket", dicle_etiket)

if __name__ == "__main__":
    u.calistir()
