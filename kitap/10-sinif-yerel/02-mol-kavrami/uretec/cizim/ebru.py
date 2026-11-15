"""Ebru (Türk kâğıt marmorlama sanatı) dokusu: matematiksel marmorlama ile vektör hesap, PIL ile raster.

Yöntem (Jaffer ve ark., "Mathematical Marbling"): tekneye (su yüzeyine) boya damlası bırakılınca
eski çizgiler damla merkezinden uzaklaşır:  P' = C + (P − C)·√(1 + r²/|P − C|²).
Sonra biz (ince çubuk) ya da tarak çekilir: çizgiye yakın noktalar çizgi yönünde kayar:
P' = P + α·λ/(d + λ)·M  (d: noktanın çizgiye uzaklığı).
Bu iki dönüşüm alanı korur ve hiçbir renk sınırını kesmez; bu yüzden sonuç gerçek ebruya çok benzer.

Kullanılan desenler:
  battal  : rastgele damlalar (temel ebru)
  gelgit  : battal + biz ile git-gel (paralel çizgiler, yön dönüşümlü)
  tarakli : gelgit + sık tarak (tek yönde)
Çıktı: JPEG (sayfada CSS arka planı olarak). Aynı dosya bütün sayfalarda kullanıldığı için PDF'e bir kez gömülür.
"""
import math
import numpy as np
from PIL import Image, ImageDraw


class Teknede:
    def __init__(self, w, h, zemin, tohum=1):
        self.w, self.h = w, h
        self.zemin = zemin
        self.damlalar = []          # [(noktalar Nx2, renk)]
        self.r = np.random.default_rng(tohum)

    # ---------------------------------------------------------- dönüşümler
    def damla(self, cx, cy, yaricap, renk, n=None):
        c = np.array([cx, cy], float)
        for i, (p, k) in enumerate(self.damlalar):
            v = p - c
            L2 = np.maximum((v * v).sum(1), 1e-9)
            self.damlalar[i] = (c + v * np.sqrt(1 + yaricap * yaricap / L2)[:, None], k)
        n = n or max(48, int(2 * math.pi * yaricap / 3))
        t = np.linspace(0, 2 * math.pi, n, endpoint=False)
        self.damlalar.append((np.stack([cx + yaricap * np.cos(t), cy + yaricap * np.sin(t)], 1), renk))

    def biz(self, B, M, alfa, lam):
        """B noktasından M yönünde çizgi; noktalar M yönünde α·λ/(d+λ) kadar kayar."""
        B = np.array(B, float)
        M = np.array(M, float) / np.linalg.norm(M)
        N = np.array([-M[1], M[0]])
        for i, (p, k) in enumerate(self.damlalar):
            d = np.abs((p - B) @ N)
            self.damlalar[i] = (p + (alfa * lam / (d + lam))[:, None] * M, k)

    def dalga(self, genlik, dalgaboyu, faz=0.0, eksen="x"):
        """Sinüs tarak: x ekseninde kaydırma, y'ye bağlı (eksen='x') ya da tersi."""
        for i, (p, k) in enumerate(self.damlalar):
            q = p.copy()
            if eksen == "x":
                q[:, 0] += genlik * np.sin(2 * math.pi * p[:, 1] / dalgaboyu + faz)
            else:
                q[:, 1] += genlik * np.sin(2 * math.pi * p[:, 0] / dalgaboyu + faz)
            self.damlalar[i] = (q, k)

    def incelt(self, en_uzun=3.0, en_fazla=12000):
        """Uzayan kenarlara ara nokta ekle (eğriler kırık görünmesin)."""
        for i, (p, k) in enumerate(self.damlalar):
            if len(p) >= en_fazla:
                continue
            q = np.roll(p, -1, axis=0)
            L = np.sqrt(((q - p) ** 2).sum(1))
            kac = np.minimum(np.ceil(L / en_uzun).astype(int), 40)
            if kac.max() <= 1:
                continue
            parca = []
            for j in range(len(p)):
                if kac[j] <= 1:
                    parca.append(p[j:j + 1])
                else:
                    t = np.linspace(0, 1, kac[j], endpoint=False)[:, None]
                    parca.append(p[j] + (q[j] - p[j]) * t)
            self.damlalar[i] = (np.concatenate(parca), k)

    def sadele(self, en_kisa=.6):
        for i, (p, k) in enumerate(self.damlalar):
            if len(p) < 200:
                continue
            q = np.roll(p, -1, axis=0)
            L = np.sqrt(((q - p) ** 2).sum(1))
            tut = np.ones(len(p), bool)
            birik = 0.0
            for j in range(len(p)):
                birik += L[j]
                if birik < en_kisa:
                    tut[j] = False
                else:
                    birik = 0.0
            self.damlalar[i] = (p[tut], k)

    # ---------------------------------------------------------- desenler
    def battal(self, renkler, adet, r_min, r_max, kenar=.08):
        for _ in range(adet):
            cx = self.r.uniform(-kenar, 1 + kenar) * self.w
            cy = self.r.uniform(-kenar, 1 + kenar) * self.h
            rr = self.r.uniform(r_min, r_max)
            self.damla(cx, cy, rr, renkler[self.r.integers(len(renkler))])
            if len(self.damlalar) % 6 == 0:
                self.incelt(5)

    def gelgit(self, aralik, alfa, lam, yon="dikey"):
        k = 0
        if yon == "dikey":
            x = aralik / 2
            while x < self.w:
                self.incelt(2.5)
                self.biz((x, 0), (0, 1 if k % 2 == 0 else -1), alfa, lam)
                x += aralik
                k += 1
        else:
            y = aralik / 2
            while y < self.h:
                self.incelt(2.5)
                self.biz((0, y), (1 if k % 2 == 0 else -1, 0), alfa, lam)
                y += aralik
                k += 1

    def tarak(self, aralik, alfa, lam, yon=(1, 0)):
        if yon[0] != 0:
            y = aralik / 2
            while y < self.h:
                self.incelt(2.5)
                self.biz((0, y), yon, alfa, lam)
                y += aralik
        else:
            x = aralik / 2
            while x < self.w:
                self.incelt(2.5)
                self.biz((x, 0), yon, alfa, lam)
                x += aralik

    # ---------------------------------------------------------- raster
    def resim(self, olcek=1.0, ss=3):
        W, H = int(self.w * olcek), int(self.h * olcek)
        im = Image.new("RGB", (W * ss, H * ss), self.zemin)
        dr = ImageDraw.Draw(im)
        k = olcek * ss
        for p, renk in self.damlalar:
            pts = [tuple(v) for v in (p * k)]
            if len(pts) > 2:
                dr.polygon(pts, fill=renk)
        return im.resize((W, H), Image.LANCZOS)


GOL_PALET = {"zemin": "#F2ECDD", "boya": ["#13A3A6", "#0E4C5A", "#2B50B5", "#7FD3CF", "#FFFFFF", "#E5B44A", "#13A3A6", "#1D3A8A", "#BFE7E3"]}
GUN_PALET = {"zemin": "#FFF1E3", "boya": ["#E2533D", "#FF8A3D", "#FF5C8A", "#F0A21A", "#FFFFFF", "#7B3F8C", "#13A3A6", "#FFC27A", "#C9467F"]}


def ebru_gol(yol, w=900, h=300, olcek=2.4, tohum=3):
    t = Teknede(w, h, GOL_PALET["zemin"], tohum)
    t.battal(GOL_PALET["boya"], 150, 10, 34)
    t.gelgit(26, 30, 6, "dikey")
    t.dalga(5, 60, 0, "x")
    t.incelt(2.0)
    t.resim(olcek).save(yol, quality=86, optimize=True, progressive=True)


def ebru_gun(yol, w=700, h=760, olcek=2.2, tohum=8):
    t = Teknede(w, h, GUN_PALET["zemin"], tohum)
    t.battal(GUN_PALET["boya"], 230, 12, 40)
    t.gelgit(34, 26, 7, "yatay")
    t.tarak(52, 16, 4, (0, 1))
    t.incelt(2.0)
    t.resim(olcek).save(yol, quality=85, optimize=True, progressive=True)


if __name__ == "__main__":
    import sys
    ebru_gol(sys.argv[1] if len(sys.argv) > 1 else "ebru-gol.jpg")
