#!/usr/bin/env python3
"""Kimyasal Güvenlik · Batı Karadeniz Maden Yolu — ünite kurucusu (ince). Ortak motor: yerel-ortak/kur_ortak.py

    python3 uretec/kur.py            # uretec/sablon.html + meta.json + çizimler → unite.html
    python3 uretec/kur.py --hepsi    # + unite-fotokopi.html + hazine-kartlari.html
Sonra: node ../../yerel-ortak/render.js . [--hepsi]   (ya da: bash uretec/olc.sh)

Burada yalnız üniteye özel olanlar durur: sayfa künyesi (HUD + altbilgi + akçe çubuğu), HUD ilerleme noktası,
açılış panoramasının durak etiketleri, mühür alt yazısı ("MADEN YOLU") ve Amasra final sahnesi.
Hazine kartları, nişanlar ve duraklar uretec/meta.json'dadır; sahneler uretec/sahneler_unite.py,
bilgi grafikleri uretec/infografik_unite.py, ortak veri (GHS, işaretler, matris, malzemeler) uretec/guvenlik_veri.py.
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
    1: ('Yola çıkış', 'Batı Karadeniz maden yolu · yola çıkış', 0),
    2: ('1. durak · <b>Zonguldak</b>', '1. durak · Güvenli çalışma ve işaretler', 0),
    3: ('2. durak · <b>Karabük</b>', '2. durak · Isı, kimyasal, cam ve kaza anı', 7),
    4: ('3. durak · <b>Safranbolu</b>', '3. durak · Tehlike piktogramları', 18),
    5: ('4. durak · <b>Yörük Köyü</b>', '4. durak · Etiket, depolama ve atık', 29),
    6: ('5. durak · <b>Bartın</b>', '5. durak · Laboratuvar malzemeleri', 39),
    7: ('Hülasa · <b>Bartın Irmağı</b>', 'Hülasa · Güvenlik özeti', 50),
    8: ('Yan yol · <b>Güzelcehisar</b>', 'Yan yol 1 · Meclis: kim haklı?', 53),
    9: ('Yan yol · <b>Çekiciler Çarşısı</b>', 'Yan yol 2 · Kıssalar', 61),
    10: ('Yan yol · <b>Kemere Köprüsü</b>', 'Yan yol 3 · Anahtar merdiveni', 70),
    11: ('<b>Amasra Kalesi</b> · 1/2', 'Büyük İmtihan · 1. bölüm', 79),
    12: ('<b>Amasra Kalesi</b> · 2/2', 'Büyük İmtihan · 2. bölüm', 89),
    13: ('<b>Üstad</b> · bonus', 'Üstad soruları · bonus', 100),
    14: ('<b>Cevaplar</b>', 'Cevaplar ve çözümler', 100),
    15: ('<b>Final</b>', 'Final · akçe rayı ve unvan', 100),
}
# HUD ilerleme noktaları: 5 durak + Hülasa + 3 yan yol + kale; her sayfada "şimdi" olan (−1: yok, 10: hepsi tamam)
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 9, 13: 10, 14: 10, 15: 10}

u = KO.Unite(__file__, SAYFA, SIMDI)
import sahneler_unite as SU  # noqa: E402  (kur_ortak uretec/ klasörünü sys.path'e ekledi)

# ------------------------------------------------------------------ açılış: Batı Karadeniz panoramasının durak etiketleri
# Gazlar'daki geri izlemeli yerleşimin bu haritaya uyarlanmışı: her etiket için 12 aday yer denenir; harita dışına, başlığın,
# pusulanın, Pamuk'un ya da yer adlarının üstüne, başka bir etikete ya da rozete binmeyen yerleşim aranır.
YASAK = [(0, 0, 100, 17),        # "Tur haritası" başlığı
         (182, 81, 210, 110),    # pusula
         (2, 88, 16, 101),       # Pamuk
         (40, 33, 72, 39.5), (66, 60.5, 86, 65.5), (173, 72.5, 195, 77.5)]   # KARADENİZ, Bartın Irmağı, Küre Dağları


def panorama_etiket():
    _, konum = SU.panorama_karadeniz()
    rozet = {k: (x / 10, y / 10) for k, (x, y) in konum.items()}

    def carpisir(a, b, pay=0.0):
        return not (a[2] + pay <= b[0] or b[2] + pay <= a[0] or a[3] + pay <= b[1] or b[3] + pay <= a[1])

    ogeler = []
    for (k, _x, _y, ust, ad, alt_, tur) in SU.DURAKLAR:
        x, y = rozet[k]
        cls = {"durak": "", "hulasa": "hul", "yan": "yan", "kale": "kale"}[tur]
        sayfa, akce = alt_.split(" · ")
        sayfa = re.sub(r"\d+", lambda m: str(u.sayfa_no(int(m.group()))), sayfa)
        ust_tam = f"{ust} · {sayfa}"
        w = max(len(ust_tam) * 1.53, len(ad) * 1.62 + len(akce) * 1.4 + 1) + 4.2
        h = 8.4
        adaylar = [(x + 4.6, y - h / 2), (x - 4.6 - w, y - h / 2), (x - w / 2, y + 4.6), (x - w / 2, y - 4.6 - h),
                   (x + 3, y + 3.4), (x + 3, y - 3.4 - h), (x - w - 3, y + 3.4), (x - w - 3, y - 3.4 - h),
                   (x - w + 6, y + 4.6), (x - 6, y + 4.6), (x - w + 6, y - 4.6 - h), (x - 6, y - 4.6 - h)]
        uygun = []
        for lx, ly in adaylar:
            kutu = (lx, ly, lx + w, ly + h)
            if kutu[0] < 2 or kutu[1] < 2 or kutu[2] > 208 or kutu[3] > 108:
                continue
            if any(carpisir(kutu, y_) for y_ in YASAK):
                continue
            if any(kk != k and kutu[0] - 4 < rx < kutu[2] + 4 and kutu[1] - 4 < ry < kutu[3] + 4 for kk, (rx, ry) in rozet.items()):
                continue
            uygun.append(kutu)
        ogeler.append((k, cls, ust_tam, ad, akce, uygun))

    def ara(i, secilen):
        if i == len(ogeler):
            return secilen
        for kutu in ogeler[i][5]:
            if not any(carpisir(kutu, s_, 1.0) for s_ in secilen):
                r = ara(i + 1, secilen + [kutu])
                if r:
                    return r
        return None

    secim = ara(0, [])
    if not secim:
        raise SystemExit("panorama: etiketler için çakışmasız yerleşim bulunamadı")
    out = []
    for (k, cls, ust_tam, ad, akce, _), kutu in zip(ogeler, secim):
        out.append(f'<div class="durak-et {cls}" style="left:{f(kutu[0], 2)}mm;top:{f(kutu[1], 2)}mm"><i>{ust_tam}</i>'
                   f'<b>{ad}<small>{akce}</small></b></div>'.replace('class="durak-et "', 'class="durak-et"'))
    return "".join(out)


def panorama():
    return SU.panorama_karadeniz()[0]


# ------------------------------------------------------------------ mühür: alt yazı bu yolun adı
def muhur(tur, boy=""):
    return U.muhur(u.yeni("mh"), tur, alt="MADEN YOLU")


# ------------------------------------------------------------------ final: Amasra sahnesi + nişan çelengi (meta.json)
def final():
    ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *KO.RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
          .replace("<svg ", '<svg width="112" height="134" ', 1) for n in u.meta["nisanlar"]]
    return SU.final_amasra(nisanlar=ns)


# ------------------------------------------------------------------ GHS ve güvenlik işaretleri: TEK KAYNAK guvenlik_veri.py
import guvenlik_veri as V  # noqa: E402
import infografik_unite as IU  # noqa: E402
ROMA = ["I", "II", "III", "IV", "V", "VI"]


def ghs_izgara():
    """Dokuz GHS kartı: piktogram (data-ghs) + tehlike adı + simge adı + anlam + örnek."""
    kartlar = []
    for kod, ad, simge, anlam, ornek in V.GHS:
        kartlar.append(f'<div class="ghs-kart">{IU.ghs(u.yeni("gh"), kod)}<div><b>{ad}<small>{simge}</small></b>'
                       f'<p>{anlam} <i>Örn. {ornek}.</i></p></div></div>')
    return '<div class="ghs-izgara">' + "".join(kartlar) + "</div>"


def isaret_izgara():
    """Beş işaret ailesi (renk + biçim) ve örnek işaretler."""
    out = []
    for aile in ("zor", "uya", "yas", "acil", "yan"):
        ad, bicim, anlam = V.ISARET_AILE[aile]
        isr = "".join(f'<div>{IU.isaret(u.yeni("is"), k)}<span>{v[1]}</span></div>' for k, v in V.ISARET.items() if v[0] == aile)
        out.append(f'<div class="isaret-aile {aile}"><div class="ab">{ad}<small>{bicim} · {anlam}</small></div><div class="isr">{isr}</div></div>')
    return '<div class="isaret-izgara">' + "".join(out) + "</div>"


def isaret_dizi(*simgeler):
    """Soru içi işaret sırası: I, II, III … altında."""
    return '<div class="isaret-dizi">' + "".join(f'<div>{IU.isaret(u.yeni("is"), s)}<span>{ROMA[i]}</span></div>'
                                                for i, s in enumerate(simgeler)) + "</div>"


def ghs_dizi(*kodlar):
    """Piktogram sırası. 'GHS02:X' → altına X yazılır; son argüman 'mini' ise küçük boy."""
    mini = bool(kodlar) and kodlar[-1] == "mini"
    kodlar = [k for k in kodlar if k != "mini"]
    parca = []
    for k in kodlar:
        kod, _, et = k.partition(":")
        parca.append(f'<div>{IU.ghs(u.yeni("gh"), kod)}{f"<span>{et}</span>" if et else ""}</div>')
    return f'<div class="ghs-dizi{" mini" if mini else ""}">' + "".join(parca) + "</div>"


u.yer_tutucu("ghs-izgara", ghs_izgara)
u.yer_tutucu("isaret-izgara", isaret_izgara)
u.yer_tutucu("isaret-dizi", isaret_dizi)
u.yer_tutucu("ghs-dizi", ghs_dizi)
u.yer_tutucu("panorama-etiket", panorama_etiket)
u.yer_tutucu("panorama-karadeniz", panorama)
u.yer_tutucu("muhur", muhur)
u.yer_tutucu("final", final)

if __name__ == "__main__":
    u.calistir()
