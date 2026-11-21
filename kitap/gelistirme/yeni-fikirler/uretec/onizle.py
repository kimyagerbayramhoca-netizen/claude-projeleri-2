"""Önizlemeler ve baskı benzetimleri (pdftoppm + PIL). Bütün benzetimler basılacak PDF'in kendisinden üretilir.

  usturlap-on.gif / usturlap-arka.gif   kesilip birleştirilmiş çark döner (ön: element seçimi, arka: mol hesabı)
  usturlap-on-Al.png / usturlap-arka-ornek.png   tek kare, büyük
  gizli-once-sonra.png, gizli-mercek.gif         gizli cevap: çıplak göz · kırmızı cam (R kanalı gri)
  animasyon-gaz.gif, animasyon-tuz.gif           asetat perde kaydırılınca (benzetim)
"""
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

BURA = os.path.dirname(os.path.abspath(__file__))
if BURA not in sys.path:
    sys.path.insert(0, BURA)
import usturlap as US  # noqa: E402

MASA = (233, 226, 212)      # masa rengi (kesilmiş disklerin altı)


def sayfa_raster(pdf, sayfa, dpi, bolge=None):
    """bolge: (x, y, w, h) mm → yalnız o bölge."""
    with tempfile.TemporaryDirectory() as t:
        komut = ["pdftoppm", "-f", str(sayfa), "-l", str(sayfa), "-r", str(dpi), "-png", "-aa", "yes", "-aaVector", "yes"]
        if bolge:
            k = dpi / 25.4
            komut += ["-x", str(int(bolge[0] * k)), "-y", str(int(bolge[1] * k)), "-W", str(int(bolge[2] * k)), "-H", str(int(bolge[3] * k))]
        subprocess.run(komut + [pdf, os.path.join(t, "s")], check=True)
        ad = [a for a in os.listdir(t) if a.endswith(".png")][0]
        return Image.open(os.path.join(t, ad)).convert("RGB")


# ------------------------------------------------------------------ Usturlap Çarkı
def _disk(img, dpi, yuz, yaricap):
    """yüzü kes: dış çizgi içi opak, delikler saydam; merkezde kare RGBA döndürür (kenar 2·yaricap mm)."""
    k = dpi / 25.4
    m = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(m)
    d.polygon([(x * k, y * k) for x, y in yuz["dis"]], fill=255)
    for h in yuz["delik"]:
        d.polygon([(x * k, y * k) for x, y in h], fill=0)
    rgba = img.convert("RGBA")
    rgba.putalpha(m)
    cx, cy = yuz["merkez"]
    s = yaricap * k
    return rgba.crop((int(cx * k - s), int(cy * k - s), int(cx * k + s), int(cy * k + s)))


def _golge(disk, kayma=4, alfa=70):
    a = np.asarray(disk.split()[-1]).astype(np.float32) / 255 * alfa
    g = Image.new("RGBA", disk.size, (40, 30, 20, 0))
    g.putalpha(Image.fromarray(a.astype(np.uint8)))
    out = Image.new("RGBA", (disk.width + kayma, disk.height + kayma), (0, 0, 0, 0))
    out.alpha_composite(g, (kayma, kayma))
    return out


class Cark:
    YAR = 86.0      # kırpma yarıçapı (mm): kürsü tepesi 82,2 mm

    def __init__(self, pdf, dpi=200):
        self.dpi = dpi
        geo = US.maske_geometrisi()
        s1, s2 = sayfa_raster(pdf, 1, dpi), sayfa_raster(pdf, 2, dpi)
        self.P_on = _disk(s1, dpi, geo["on"]["P"], self.YAR)
        self.Q_on = _disk(s1, dpi, geo["on"]["Q"], self.YAR).rotate(US.Q_DONUS, resample=Image.BICUBIC)   # kürsü tepeye
        self.P_arka = _disk(s2, dpi, geo["arka"]["P"], self.YAR)
        self.Q_arka = _disk(s2, dpi, geo["arka"]["Q"], self.YAR).rotate(-US.Q_DONUS, resample=Image.BICUBIC)

    def _birlestir(self, alt, ust, alt_donus, boyut=None):
        """alt disk alt_donus derece (ekranda saat yönü) döner; üst disk sabit."""
        a = alt.rotate(-alt_donus, resample=Image.BICUBIC)
        zem = Image.new("RGBA", alt.size, MASA + (255,))
        for disk in (a, ust):
            zem.alpha_composite(_golge(disk).crop((0, 0) + disk.size))
            zem.alpha_composite(disk)
        zem = zem.convert("RGB")
        return zem.resize((boyut, boyut), Image.LANCZOS) if boyut else zem

    def on(self, psi, boyut=None):
        """ön yüz: P, ψ kadar saat yönünün tersine döner (ψ_k = 18(k−1) → k. element tepede)."""
        return self._birlestir(self.P_on, self.Q_on, -psi, boyut)

    def arka(self, gama, boyut=None):
        """arka yüz: üstte P (yarıklı), altta Q; P arkadan bakana göre gama kadar saat yönünde döner."""
        a = self.P_arka.rotate(-gama, resample=Image.BICUBIC)
        zem = Image.new("RGBA", a.size, MASA + (255,))
        zem.alpha_composite(_golge(self.Q_arka).crop((0, 0) + a.size))
        zem.alpha_composite(self.Q_arka)
        zem.alpha_composite(_golge(a).crop((0, 0) + a.size))
        zem.alpha_composite(a)
        zem = zem.convert("RGB")
        return zem.resize((boyut, boyut), Image.LANCZOS) if boyut else zem


def gama_icin(m, M):
    """arka yüz: m (P) M'nin (Q) hizasına gelsin → P'nin dönüşü (saat yönü, derece)."""
    man = lambda v: v / 10 ** math.floor(math.log10(v))  # noqa: E731
    return (US.theta(man(M)) - US.theta(man(m))) % 360


def _yazi_bandi(img, metin):
    from PIL import ImageFont
    yol = os.path.join(BURA, "..", "..", "..", "fontlar", "nunito", "static", "Nunito-800.ttf")
    fnt = ImageFont.truetype(yol, max(14, img.width // 30))
    out = Image.new("RGB", (img.width, img.height + fnt.size + 14), (255, 255, 255))
    out.paste(img, (0, 0))
    ImageDraw.Draw(out).text((img.width // 2, img.height + 6), metin, fill=(27, 29, 38), font=fnt, anchor="ma")
    return out


def usturlap(pdf, hedef):
    c = Cark(pdf)
    # tek kareler (denetim için büyük)
    c.on(US.ADIM * 12).save(os.path.join(hedef, "usturlap-on-Al.png"))
    c.arka(gama_icin(53, 106)).save(os.path.join(hedef, "usturlap-arka-ornek.png"))
    # ön yüz GIF: H → C → Na → Cl → Ca (dönerek)
    kare, sure = [], []
    duraklar = [1, 6, 11, 17, 20]
    B = 440
    onceki = 0.0
    for z in duraklar:
        hedef_psi = US.ADIM * (z - 1)
        adim = max(1, int(abs(hedef_psi - onceki) / 15))
        for i in range(1, adim + 1):
            kare.append(_yazi_bandi(c.on(onceki + (hedef_psi - onceki) * i / adim, B), "Ön yüz · element bulucu"))
            sure.append(70)
        kare.append(_yazi_bandi(c.on(hedef_psi, B), f"Z = {z}: pencereleri oku"))
        sure.append(1500)
        onceki = hedef_psi
    kare = [k.quantize(96, dither=Image.Dither.NONE) for k in kare]
    kare[0].save(os.path.join(hedef, "usturlap-on.gif"), save_all=True, append_images=kare[1:], duration=sure, loop=0, optimize=True)
    # arka yüz GIF: 53 g soda (M 106) → 0,5 mol; 36 g su (M 18) → 2 mol
    kare, sure = [], []
    onceki = 0.0
    for m, M, metin in ((53, 106, "53 g / 106 g/mol → ok 5,0 → n = 0,5 mol"), (36, 18, "36 g / 18 g/mol → ok 2 → n = 2 mol")):
        g = gama_icin(m, M)
        fark = ((g - onceki + 180) % 360) - 180
        adim = max(1, int(abs(fark) / 14))
        for i in range(1, adim + 1):
            kare.append(_yazi_bandi(c.arka(onceki + fark * i / adim, B), "Arka yüz · Mol Çarkı"))
            sure.append(70)
        kare.append(_yazi_bandi(c.arka(g, B), metin))
        sure.append(2600)
        onceki = g
    kare = [k.quantize(96, dither=Image.Dither.NONE) for k in kare]
    kare[0].save(os.path.join(hedef, "usturlap-arka.gif"), save_all=True, append_images=kare[1:], duration=sure, loop=0, optimize=True)
    print("usturlap: on/arka GIF ve PNG yazıldı")


def hepsi(pdf, hedef):
    os.makedirs(hedef, exist_ok=True)
    usturlap(pdf, hedef)
    for ad in ("gizli", "animasyon"):
        if os.path.exists(os.path.join(BURA, ad + ".py")):
            __import__(ad).onizleme(pdf, hedef)


if __name__ == "__main__":
    kok = os.path.dirname(BURA)
    hepsi(os.path.join(kok, "yeni-fikirler-ornek.pdf"), os.path.join(kok, "onizleme"))
