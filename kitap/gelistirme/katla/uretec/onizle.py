"""Katla örneği · telefonda bakılacak benzetimler (PIL + numpy; PDF'in kendisinden, pdftoppm ile).

  acik-katli-s1.png / -s2.png   kat sayfası: açık · katlı (sol + sağ parça birleştirilir) · katlı fotokopi (gri)
  katlama-s1.gif / -s2.gif      orta şerit kapanırken (A ve B dağ, orta vadi katı; iki yarım cos θ ile daralır)
  kose-katli.png                köşeyi katla: ön yüz köşesi · arka yüz köşesi · katlanınca (benzetim)
  kose-cizgi-filmi.gif / -serit.png   24 karelik köşe sineması (sayfa 4'teki karelerden kesilir)

Katlı görünüm: sayfa 1590 px genişlikte basılır (70 mm = 530 px tam); sol [0, 530) ile sağ [1060, 1590) yan yana konur.
Köşe benzetimi (mm, ön yüz W × H, kat sabiti a): katlanınca görünen nokta (X, Y) ← arka yüz pikseli (Y − (H − a), W + H − a − X);
X + Y > W + H − a olan bölge (köşenin eski yeri) boşalır, masa rengiyle doldurulur.
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

BURA = os.path.dirname(os.path.abspath(__file__))
if BURA not in sys.path:
    sys.path.insert(0, BURA)
import katla_cizim as KC  # noqa: E402

FONT = os.path.join(KC.FONTLAR, "nunito", "static", "Nunito-900.ttf")
MASA = (176, 186, 194)


def png(pdf, sayfa, gen, yuk):
    """PDF'in bir sayfasını tam gen × yuk piksel PNG olarak döndürür (RGB)."""
    with tempfile.TemporaryDirectory() as d:
        onek = os.path.join(d, "s")
        subprocess.run(["pdftoppm", "-f", str(sayfa), "-l", str(sayfa), "-png", "-singlefile", "-scale-to-x", str(gen), "-scale-to-y", str(yuk), pdf, onek], check=True)
        return Image.open(onek + ".png").convert("RGB")


def katli(img):
    W, H = img.size
    x70, x140 = W // 3, 2 * W // 3
    out = Image.new("RGB", (x70 + W - x140, H), "white")
    out.paste(img.crop((0, 0, x70, H)), (0, 0))
    out.paste(img.crop((x140, 0, W, H)), (x70, 0))
    return out


def dikis_olcusu(img, kayma=0):
    """Katlı görünümde dikişin iki yanındaki sütun farkı / parça içindeki komşu sütun farkı (≈ 1 ise dikiş görünmez).
    kayma: sağ parçayı piksel kaydırarak kötü katlamayı dener."""
    a = np.asarray(img, dtype=float)
    W = a.shape[1]
    x70, x140 = W // 3, 2 * W // 3
    dikis = np.abs(a[:, x70 - 1] - a[:, x140 + kayma]).mean()
    ref = (np.abs(a[:, x70 - 3] - a[:, x70 - 2]).mean() + np.abs(a[:, x140 + 1] - a[:, x140 + 2]).mean()) / 2
    return dikis, ref


def _etiket(img, metin, alt=""):
    f1, f2 = ImageFont.truetype(FONT, 30), ImageFont.truetype(FONT, 21)
    out = Image.new("RGB", (img.width, img.height + 78), "white")
    out.paste(img, (0, 78))
    d = ImageDraw.Draw(out)
    d.text((8, 6), metin, font=f1, fill=(27, 29, 38))
    if alt:
        d.text((8, 44), alt, font=f2, fill=(86, 99, 110))
    return out


def _yan_yana(paneller, ara=24):
    H = max(p.height for p in paneller)
    out = Image.new("RGB", (sum(p.width for p in paneller) + ara * (len(paneller) - 1), H), (235, 239, 242))
    x = 0
    for p in paneller:
        out.paste(p, (x, 0))
        x += p.width + ara
    return out


def acik_katli(img, cikti, baslik):
    s = .5
    acik = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    k = katli(img)
    kat = k.resize((round(k.width * s), round(k.height * s)), Image.LANCZOS)
    gri = ImageOps.autocontrast(ImageOps.grayscale(kat), cutoff=1).convert("RGB")
    _yan_yana([_etiket(acik, "AÇIK", baslik), _etiket(kat, "KATLI", "A ile B buluştu"), _etiket(gri, "KATLI · FOTOKOPİ", "renksiz de okunuyor mu?")]).save(cikti, optimize=True)


def katlama_gif(img, cikti, gen=600):
    W, H = img.size
    x70, x140 = W // 3, 2 * W // 3
    yari = (x140 - x70) // 2
    L, M1, M2, R = (img.crop((0, 0, x70, H)), img.crop((x70, 0, x70 + yari, H)), img.crop((x70 + yari, 0, x140, H)), img.crop((x140, 0, W, H)))
    kareler, sureler = [], []
    acilar = list(range(0, 91, 9))
    for i, aci in enumerate(acilar + acilar[-2:0:-1]):
        c, sn = np.cos(np.radians(aci)), np.sin(np.radians(aci))
        w = max(1, round(yari * c))
        tuval = Image.new("RGB", (W, H), MASA)
        tuval.paste(L, (0, 0))
        if aci < 90:
            tuval.paste(ImageEnhance.Brightness(M1.resize((w, H))).enhance(1 - .45 * sn), (x70, 0))
            tuval.paste(ImageEnhance.Brightness(M2.resize((w, H))).enhance(1 - .22 * sn), (x70 + w, 0))
        tuval.paste(R, (x70 + (2 * w if aci < 90 else 0), 0))
        kareler.append(tuval.resize((gen, round(H * gen / W)), Image.LANCZOS))
        sureler.append(1200 if aci == 0 else (2200 if aci == 90 else 70))
    pal = kareler[0].quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    pk = [k.quantize(palette=pal, dither=Image.Dither.NONE) for k in kareler]
    pk[0].save(cikti, save_all=True, append_images=pk[1:], duration=sureler, loop=0, optimize=True, disposal=1)


def kose_benzet(on, arka, a_mm=KC.KOSE_A):
    """Ön ve arka yüz aynı ölçekte (px/mm = W/210). Köşe öne katlanınca ön yüzün görünüşü."""
    W, H = on.size
    o = W / 210
    a = a_mm * o
    F, B = np.asarray(on).copy(), np.asarray(arka)
    Y, X = np.mgrid[0:H, 0:W]
    Xc, Yc = X + .5, Y + .5
    toplam = (Xc - (W - a)) + (Yc - (H - a))
    kare = (Xc >= W - a) & (Yc >= H - a)
    inen = kare & (toplam <= a)                       # katlanan köşenin indiği üçgen
    bos = kare & (toplam > a)                         # köşenin eski yeri: boşalır
    xb = np.clip(np.floor(Yc - (H - a)).astype(int), 0, W - 1)
    yb = np.clip(np.floor(W + H - a - Xc).astype(int), 0, H - 1)
    F[inen] = B[yb[inen], xb[inen]]
    golge = np.clip(1 - (a - toplam) / (6 * o), 0, 1) * .28      # kat çizgisine yakın hafif gölge
    F[inen] = (F[inen] * (1 - golge[inen, None])).astype(np.uint8)
    F[bos] = MASA
    return Image.fromarray(F)


def kose_paneli(on, arka, katli_on, cikti):
    W, H = on.size
    o = W / 210
    kes = lambda im, x0: im.crop((round(x0 * o), round((297 - 112) * o), round((x0 + 105) * o), H))  # noqa: E731
    _yan_yana([_etiket(kes(on, 105), "ÖN YÜZ · sayfa 5", "sağ alt köşe, kesik çizgi"),
               _etiket(kes(arka, 0), "ARKA YÜZ · sayfa 6", "sol alt köşe, cevap yan yatık"),
               _etiket(kes(katli_on, 105), "KÖŞE KATLANINCA", "benzetim: çevir + kat çizgisine yansıt")]).save(cikti, optimize=True)


def film(pdf, gif, serit, sayfa=4):
    o = 12
    img = png(pdf, sayfa, 210 * o, 297 * o)
    kareler = [img.crop((round(x * o), round(y * o), round((x + KC.FILM_KARE) * o), round((y + KC.FILM_KARE) * o))) for x, y in KC.film_yerleri()]
    kucuk = [k.resize((240, 240), Image.LANCZOS) for k in kareler]
    pal = kucuk[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    pk = [k.quantize(palette=pal, dither=Image.Dither.NONE) for k in kucuk]
    pk[0].save(gif, save_all=True, append_images=pk[1:], duration=110, loop=0, optimize=True)
    f2 = ImageFont.truetype(FONT, 22)
    hucre = 168
    out = Image.new("RGB", (12 * hucre + 8, 2 * (hucre + 30) + 8), "white")
    d = ImageDraw.Draw(out)
    for i, k in enumerate(kareler):
        x, y = 8 + (i % 12) * hucre, 8 + (i // 12) * (hucre + 30)
        out.paste(k.resize((hucre - 8, hucre - 8), Image.LANCZOS), (x, y))
        d.text((x + (hucre - 8) // 2, y + hucre - 4), str(i + 1), font=f2, fill=(10, 108, 116), anchor="mt")
    out.save(serit, optimize=True)
    return kareler


def hepsi(pdf, klasor):
    os.makedirs(klasor, exist_ok=True)
    olcu = {}
    for no, sayfa, baslik in ((1, 1, "9. sınıf · Katla, bağ oluşsun"), (2, 3, "10. sınıf · Katla, tepkime olsun")):
        img = png(pdf, sayfa, 1590, 2249)
        acik_katli(img, os.path.join(klasor, f"acik-katli-s{no}.png"), baslik)
        katlama_gif(img, os.path.join(klasor, f"katlama-s{no}.gif"))
        olcu[no] = dikis_olcusu(img), dikis_olcusu(img, 8)
        print(f"  s{no}: dikiş farkı {olcu[no][0][0]:.2f} · komşu sütun {olcu[no][0][1]:.2f} · 1,5 mm kaymış katta {olcu[no][1][0]:.2f}")
    on, arka = png(pdf, 5, 1260, 1782), png(pdf, 6, 1260, 1782)
    kose_paneli(on, arka, kose_benzet(on, arka), os.path.join(klasor, "kose-katli.png"))
    film(pdf, os.path.join(klasor, "kose-cizgi-filmi.gif"), os.path.join(klasor, "kose-cizgi-filmi-serit.png"))
    print("  önizlemeler yazıldı:", ", ".join(sorted(f for f in os.listdir(klasor) if not f.startswith("s0"))))
    return olcu


if __name__ == "__main__":
    hepsi(sys.argv[1], sys.argv[2])
