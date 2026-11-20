#!/usr/bin/env python3
"""3B örneği · bütün görselleri üretir (motor: uc_boyut.py).

    python3 uretec/gorseller.py            hepsi: anaglifler + düz resimler + gözlük testi + önizleme (GIF, iki-goz.png)
    python3 uretec/gorseller.py ch4 buz    yalnız adı verilen yapılar (deneme)

gorsel/ana-<ad>.png      anaglif (basılı boyutunda 300 dpi)        gorsel/duz-<ad>.png   aynı koordinatlardan renkli düz resim
gorsel/test-yazi.png, test-derinlik.png   gözlük testi            gorsel/uc-boyut.json  stereo ölçüleri (README, dogrula.py, sayfa)
onizleme/sallanan-<ad>.gif  "sallanan 3B"   onizleme/iki-goz.png   sol göz · sağ göz · anaglif
"""
import sys
sys.dont_write_bytecode = True
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
sys.path.insert(0, BURA)
import uc_boyut as UB  # noqa: E402

GORSEL = os.path.join(KLASOR, "gorsel")
ONIZ = os.path.join(KLASOR, "onizleme")
NUNITO = os.path.join(UB.KITAP, "fontlar", "nunito", "static", "Nunito-800.ttf")

# ad: (kurucu, dönüşler [(rx, ry, rz) sırayla], anaglif en × yük (mm), mm / model birimi (None: sığdır), düz resim en × yük (mm))
# Moleküller ortak ölçekte: 1 Å = 15 mm (150 milyon kat büyütme); k = K_ORTO ya da ona çok yakın (derinlik gerçek oranında).
MOL_OLCEK = 15.0
YAPILAR = {
    "ch4": (UB.ch4, [(20, 18, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "nh3": (UB.nh3, [(24, 14, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "h2o": (UB.h2o, [(10, 35, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "co2": (UB.co2, [(12, 40, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "bf3": (UB.bf3, [(-50, 18, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "nacl": (UB.nacl, [(14, -22, 0)], (58, 55), None, (24, 23)),
    "elmas": (UB.elmas, [(16, -27, 0)], (58, 55), None, (24, 23)),
    "grafit": (UB.grafit, [(24, -20, 0)], (58, 55), None, (24, 23)),
    "buz": (UB.buz, [(0, 4, 0), (66, 0, 0)], (58, 55), None, (24, 23)),
    "gaz": (UB.gaz_kutusu, [(12, -18, 0)], (92, 51), None, (44, 25)),
    "kup": (UB.mol_kupu, [(14, -24, 0)], (78, 49), None, (38, 24)),
    "hid-na": (lambda: UB.hidrasyon("Na"), [(20, -28, 0)], (46, 46), None, (21, 21)),
    "hid-cl": (lambda: UB.hidrasyon("Cl"), [(20, -28, 0)], (46, 46), None, (21, 21)),
}
SALLANAN = ("ch4", "nacl", "elmas", "hid-na")


def yapi(ad):
    """Sayfadaki görünümüyle (döndürülmüş, ortalanmış) yapı."""
    kur, don = YAPILAR[ad][0], YAPILAR[ad][1]
    y = kur()
    for d in don:
        y.dondur(*d)
    return y.ortala()


def _yazi(boy, yol=NUNITO):
    return ImageFont.truetype(yol, boy)


# ------------------------------------------------------------------ gözlük testi (aynı anaglif_birlestir yolundan)
def test_yazi(en_mm=54, yuk_mm=13):
    """SOL yazısı yalnız SOL göz resminde (kâğıtta camgöbeği), SAĞ yazısı yalnız SAĞ göz resminde (kâğıtta kırmızı).
    Gözlük doğru takılıysa sol göz (kırmızı cam) yalnız SOL'u, sağ göz (camgöbeği cam) yalnız SAĞ'ı koyu görür."""
    W, H = UB.px(en_mm), UB.px(yuk_mm)
    sol, sag = Image.new("L", (W, H), 255), Image.new("L", (W, H), 255)
    f = _yazi(int(H * .78), UB.YAZI)
    for im, metin, x in ((sol, "SOL", W * .25), (sag, "SAĞ", W * .75)):
        ImageDraw.Draw(im).text((x, H * .5), metin, font=f, fill=40, anchor="mm")
    return UB.anaglif_birlestir(np.asarray(sol), np.asarray(sag))


TEST_AYRIKLIK_MM = 2.4


def test_derinlik(en_mm=54, yuk_mm=20):
    """A dairesi çapraz ayrıklıkla (+2,4 mm: kâğıdın önünde), B dairesi ters ayrıklıkla (−2,4 mm: kâğıdın arkasında).
    Çerçeve sıfır ayrıklıkta (kâğıt düzlemi). Gözlük ters takılırsa A arkada, B önde görünür."""
    W, H = UB.px(en_mm), UB.px(yuk_mm)
    sol, sag = Image.new("L", (W, H), 255), Image.new("L", (W, H), 255)
    d = UB.px(TEST_AYRIKLIK_MM) / 2
    f = _yazi(int(H * .42), UB.YAZI)
    r = H * .33
    for im, s in ((sol, +1), (sag, -1)):
        c = ImageDraw.Draw(im)
        c.rounded_rectangle([3, 3, W - 4, H - 4], radius=18, outline=120, width=5)
        for harf, x, isaret in (("A", W * .27, +1), ("B", W * .73, -1)):
            cx = x + s * isaret * d                         # sol göz resmi: yakın cisim SAĞA kayar (x + k·z, z > 0)
            c.ellipse([cx - r, H / 2 - r, cx + r, H / 2 + r], fill=205, outline=70, width=6)
            for a in range(0, 360, 45):                     # eşleşmeyi kolaylaştıran noktalı doku
                dx, dy = r * .74 * np.cos(np.radians(a)), r * .74 * np.sin(np.radians(a))
                c.ellipse([cx + dx - 5, H / 2 + dy - 5, cx + dx + 5, H / 2 + dy + 5], fill=95)
            c.text((cx, H / 2 - H * .01), harf, font=f, fill=45, anchor="mm")
    return UB.anaglif_birlestir(np.asarray(sol), np.asarray(sag))


# ------------------------------------------------------------------ önizleme: sallanan 3B (GIF) ve iki göz levhası
def sallanan(ad, en_px=300):
    """Sol ve sağ göz bakışları art arda (7 kare/sn): gözlüksüz derinlik izlenimi. Renkli; k = baskıdaki k."""
    y = yapi(ad)
    (en, yuk), mb = YAPILAR[ad][2], YAPILAR[ad][3]
    b = UB.yerlestir(y, en, yuk, mb)
    kare = []
    for goz in (+1, -1):
        a = UB.duz_resim(y, en, yuk, mm_birim=b["mm_birim"], ss=2, goz=goz, k=b["k"])
        kare.append(Image.fromarray(a).resize((en_px, int(round(en_px * a.shape[0] / a.shape[1]))), Image.LANCZOS))
    pal = kare[0].quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    kare = [k.quantize(palette=pal, dither=Image.Dither.NONE) for k in kare]
    yol = os.path.join(ONIZ, f"sallanan-{ad}.gif")
    kare[0].save(yol, save_all=True, append_images=kare[1:], duration=140, loop=0, optimize=True)
    return yol


def iki_goz(ad="ch4"):
    """Sol göz · sağ göz · anaglif yan yana, Türkçe etiketlerle."""
    y = yapi(ad)
    (en, yuk), mb = YAPILAR[ad][2], YAPILAR[ad][3]
    s = UB.uret(y, en, yuk, mb)
    H, W = s.sol.shape
    pay, ust, alt = 26, 96, 132
    T = Image.new("RGB", (3 * W + 4 * pay, H + ust + alt), "white")
    c = ImageDraw.Draw(T)
    f1, f2, f3 = _yazi(40, UB.YAZI), _yazi(25), _yazi(23)
    kareler = [(np.dstack([s.sol] * 3), "SOL GÖZÜN GÖRDÜĞÜ", "kırmızı camın ardından", "kâğıtta camgöbeği mürekkeple basılır", (0, 150, 160)),
               (np.dstack([s.sag] * 3), "SAĞ GÖZÜN GÖRDÜĞÜ", "camgöbeği camın ardından", "kâğıtta kırmızı mürekkeple basılır", (200, 30, 30)),
               (s.anaglif, "ANAGLİF", "iki resim üst üste", f"en yakın noktada kayma {s.bilgi['ayriklik_mm']:.1f} mm".replace(".", ","), (27, 29, 38))]
    for i, (dizi, bas, a1, a2, renk) in enumerate(kareler):
        x = pay + i * (W + pay)
        T.paste(Image.fromarray(dizi), (x, ust))
        c.rectangle([x, ust, x + W - 1, ust + H - 1], outline=(190, 196, 206), width=2)
        c.rectangle([x, 18, x + W - 1, 26], fill=renk)
        c.text((x + W / 2, 60), bas, font=f1, fill=(27, 29, 38), anchor="mm")
        c.text((x + W / 2, ust + H + 34), a1, font=f2, fill=(27, 29, 38), anchor="mm")
        c.text((x + W / 2, ust + H + 74), a2, font=f3, fill=renk, anchor="mm")
    c.text((T.width / 2, T.height - 22), "Kimya Rotası · 3B örneği · CH₄: aynı molekül iki gözden; yakındaki H atomu iki resimde farklı yerde",
           font=_yazi(22), fill=(86, 99, 110), anchor="mm")
    yol = os.path.join(ONIZ, "iki-goz.png")
    T.save(yol, optimize=True)
    return yol


# ------------------------------------------------------------------
def main(argv):
    os.makedirs(GORSEL, exist_ok=True)
    os.makedirs(ONIZ, exist_ok=True)
    json_yol = os.path.join(GORSEL, "uc-boyut.json")
    bilgi = json.load(open(json_yol, encoding="utf-8")) if (argv and os.path.exists(json_yol)) else {}
    for ad in (argv or YAPILAR):
        (en, yuk), mb, (den, dyuk) = YAPILAR[ad][2], YAPILAR[ad][3], YAPILAR[ad][4]
        y = yapi(ad)
        s = UB.uret(y, en, yuk, mb)
        UB.kaydet(s.anaglif, os.path.join(GORSEL, f"ana-{ad}.png"))
        UB.kaydet(UB.duz_resim(y, den, dyuk, golge=ad in ("ch4", "nh3", "h2o", "co2", "bf3")), os.path.join(GORSEL, f"duz-{ad}.png"))
        b = {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in s.bilgi.items()}
        b.update(birim=y.birim, kure=len(y.kure), donus=YAPILAR[ad][1], kb=round(os.path.getsize(os.path.join(GORSEL, f"ana-{ad}.png")) / 1024))
        bilgi[ad] = b
        print(f"{ad:7s} {en}×{yuk} mm · 1 {y.birim} = {b['mm_birim']:.2f} mm · k = {b['k']:.4f} · en yakın nokta {b['z_mm']:.1f} mm · "
              f"toplam ayrıklık {b['ayriklik_mm']:.2f} mm · derinlik oranı {b['derinlik_orani']:.2f} · {b['kb']} KB" + (f" · TAŞMA {b['tasma_mm']} mm" if b["tasma_mm"] else ""))
    with open(json_yol, "w", encoding="utf-8") as fp:
        json.dump(dict(sabit=dict(goz_araligi_mm=UB.GOZ_ARALIGI_MM, okuma_mm=UB.OKUMA_MM, k_orto=round(UB.K_ORTO, 5), ayriklik_ust_mm=UB.AYRIKLIK_UST_MM,
                                  dpi=UB.DPI, mol_olcek_mm=MOL_OLCEK, test_ayriklik_mm=TEST_AYRIKLIK_MM), **{k: v for k, v in bilgi.items() if k != "sabit"}),
                  fp, ensure_ascii=False, indent=1)
    if argv:
        return
    UB.kaydet(test_yazi(), os.path.join(GORSEL, "test-yazi.png"))
    UB.kaydet(test_derinlik(), os.path.join(GORSEL, "test-derinlik.png"))
    for ad in SALLANAN:
        yol = sallanan(ad)
        print(f"{os.path.relpath(yol, KLASOR)} · {os.path.getsize(yol) / 1024:.0f} KB")
    print(os.path.relpath(iki_goz(), KLASOR))


if __name__ == "__main__":
    main(sys.argv[1:])
