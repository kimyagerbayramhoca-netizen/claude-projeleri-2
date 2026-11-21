#!/usr/bin/env python3
"""Kimya Rotası · 3B → ANAGLİF MOTORU (kırmızı–camgöbeği kâğıt gözlük) · ORTAK (kaynak: gelistirme/uc-boyut).

Ünitede: meta.json "uc_boyut": ["ch4", "nacl", {"ad": "ch4-yan", "yapi": "ch4", "donus": [[60, 10, 0]]}, …] → kur_ortak
kurulumdan önce unite_gorselleri() ile ünitenin gorsel/ klasörüne ana-<ad>.png (anaglif), duz-<ad>.png (gözlüksüz küçük)
ve duz-<ad>-b.png (fotokopi nüshasında anaglifin yerine geçen büyük düz resim) üretir; ölçüler ve imzalar
gorsel/uc-boyut.json'dadır. İmza (tanım + koordinatlar + bu dosyanın kodu) değişmedikçe resim YENİDEN ÇİZİLMEZ.
Sayfada: {{ana|ad}} (anaglif + fotokopi yedeği) · {{duz|ad}} (düz resim) · {{test|yazi}} {{test|derinlik}} (gözlük testi).
Hazır yapılar: KATALOG (ch4 nh3 h2o co2 bf3 nacl elmas grafit buz gaz kup hid-na hid-cl); yeni yapı için ünitenin
sahneler_unite.py (ya da infografik_unite.py) modülüne Yapi döndüren bir kurucu yazılır ve "yapi" alanında adı verilir.

Bir yapı (molekül, kristal, tanecik kutusu) GERÇEK 3B koordinatlarla tanımlanır; motor aynı koordinatlardan
  • sol göz ve sağ göz için gri tonlu, derinlik tamponlu (z-buffer) çubuk-top resmi,
  • ikisinden anaglif (R = sol göz · G, B = sağ göz · beyaz zemin),
  • gözlüksüz bakış ve fotokopi için renkli DÜZ resim
üretir. Çıktı PNG'dir (basılı boyutunda 300 dpi), sayfaya <img> ile konur.

STEREO (ayrıntı ve gerekçe: README §2)
  Model ekseni: x sağa, y yukarı, z OKUYUCUYA doğru. Sıfır paralaks düzlemi (kâğıt) yapının derinlik ortasıdır (z = 0).
  Göz başına yatay kaydırma (shear):   sol göz  x' = x + k·z      sağ göz  x' = x − k·z
  → okuyucuya yakın (z > 0) parçalar ÇAPRAZ ayrıklık alır: sol göz resmi sağda kalır, parça kâğıttan dışarı çıkar.
  k = min(K_ORTO, AYRIKLIK_UST_MM / (2 · z_en_yakın_mm));  K_ORTO = göz aralığı / (2 · okuma uzaklığı) = 62 / 750.
  Kaydırma "ışın yönü" olarak uygulanır (d = (−s·k, 0, 1)): küre ve silindir yüzeyindeki her nokta kendi derinliğine
  göre kayar; gölgelendirme de iki gözde yüzeye yapışık kalır (küreler gerçekten yuvarlak görünür).

ANAGLİF (gözlük: SOL göz KIRMIZI cam, SAĞ göz CAMGÖBEĞİ cam)
  R kanalı = sol göz resmi   →  kâğıtta camgöbeği mürekkep (kırmızı camdan koyu, camgöbeği camdan görünmez)
  G, B     = sağ göz resmi   →  kâğıtta kırmızı mürekkep   (camgöbeği camdan koyu, kırmızı camdan görünmez)
  Atomlar GRİ tonludur (renkli atom anaglifte iki gözde farklı parlaklık verir: retina rekabeti). Elementler boy,
  ton ve üzerlerindeki harfle ayrılır.

Kullanım:
    import uc_boyut as UB
    y = UB.ch4(); y.dondur(8, 22, 0)
    s = UB.uret(y, en_mm=56, yuk_mm=48, mm_birim=13)       # s.anaglif, s.sol, s.sag, s.bilgi
    UB.kaydet(s.anaglif, "ana-ch4.png");  UB.kaydet(UB.duz_resim(y, 24, 21), "duz-ch4.png")
"""
import hashlib
import json
import math
import os
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
KITAP = os.path.abspath(os.path.join(BURA, "..", ".."))
ORTAK_GORSEL = os.path.join(KITAP, "yerel-ortak", "gorsel")
YAZI = os.path.join(KITAP, "fontlar", "baloobhaijaan2", "static", "BalooBhaijaan2-800.ttf")

# ------------------------------------------------------------------ stereo sabitleri
GOZ_ARALIGI_MM = 62.0            # ergen/yetişkin ortalaması (58–65 mm)
OKUMA_MM = 375.0                 # kitap okuma uzaklığı 35–40 cm'nin ortası
K_ORTO = GOZ_ARALIGI_MM / (2 * OKUMA_MM)      # 0,0827: derinliğin 1:1 (gerçek oranında) göründüğü kaydırma
AYRIKLIK_UST_MM = 3.0            # en yakın noktada toplam ayrıklığın üst sınırı (kâğıtta, mm)
DPI = 300
SS = 3                           # kenar yumuşatma: 3×3 üst örnekleme

# ------------------------------------------------------------------ elementler
# yarıçap: çubuk-top modeli için küçültülmüş (model birimi Å) · gri: anaglifteki ton (0 siyah – 1 beyaz)
# renk: düz resimdeki renk (yerel-ortak/cizim/renkler.py ATOM ile aynı; F ve vurgu ek)
ELEMENT = {
    "H": (.30, .93, "#F3F5F8"), "C": (.42, .42, "#3A3F4B"), "N": (.42, .55, "#2B50B5"), "O": (.41, .68, "#E2533D"),
    "B": (.44, .76, "#F2A88A"), "F": (.38, .86, "#8FD06A"), "Na": (.50, .50, "#8E5BD0"), "Cl": (.78, .88, "#39A85A"),
}
BAG = {  # tür: (yarıçap, gri, düz renk, kesik (dolu, boş) ya da None)
    "tek": (.105, .64, "#AEB6C2", None), "cift": (.07, .64, "#AEB6C2", None),
    "kafes": (.05, .74, "#C3CAD4", None), "hidrojen": (.05, .50, "#6F7A8A", (.20, .15)),
    "zayif": (.04, .62, "#8A94A3", (.16, .16)),
}
VURGU_BAG = (.30, "#1B1D26")     # sayım için kalın koyu çubuk: (gri, düz renk)
ISIK = np.array([-.42, .62, .66])
ISIK = ISIK / np.linalg.norm(ISIK)
TETRA = math.degrees(math.acos(-1 / 3))       # 109,47°


def _rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255


def _rot(rx, ry, rz):
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def yon(kutup, azimut):
    """Birim vektör: kutup açısı +y ekseninden, azimut y çevresinde (+x'ten +z'ye), derece."""
    t, a = math.radians(kutup), math.radians(azimut)
    return np.array([math.sin(t) * math.cos(a), math.cos(t), math.sin(t) * math.sin(a)])


def _dik(u):
    """u'ya dik bir birim vektör (kararlı seçim)."""
    u = np.asarray(u, float)
    e = np.array([1.0, 0, 0]) if abs(u[0]) < .85 else np.array([0, 1.0, 0])
    v = np.cross(u, e)
    return v / np.linalg.norm(v)


# ------------------------------------------------------------------ YAPI
class Yapi:
    """Küreler (atom, iyon, top) + bağlar (atomlar arası) + serbest çubuklar (kutu kenarı, iz)."""

    def __init__(self, ad, birim="Å"):
        self.ad, self.birim = ad, birim
        self.kure, self.bag, self.cubuk = [], [], []
        self.R = np.eye(3)

    def atom(self, el, p, harf=None, ust="", r=None, gri=None, renk=None, vurgu=False, desen=None):
        r0, g0, c0 = ELEMENT.get(el, (.4, .6, "#888888"))
        self.kure.append(dict(el=el, p=np.asarray(p, float), r=r or r0, gri=g0 if gri is None else gri, renk=renk or c0,
                              harf=el if harf is None else harf, ust=ust, vurgu=vurgu, desen=desen))
        return len(self.kure) - 1

    def bagla(self, i, j, tur="tek", vurgu=False):
        self.bag.append(dict(i=i, j=j, tur=tur, vurgu=vurgu))

    def cubuk_ekle(self, a, b, r=.05, gri=.5, renk="#7C8696", kesik=None):
        self.cubuk.append(dict(a=np.asarray(a, float), b=np.asarray(b, float), r=r, gri=gri, renk=renk, kesik=kesik))

    def cift(self, i, yonu, uz=None, dik=None):
        """Ortaklanmamış elektron çifti: i. atomun yüzeyinin hemen dışında iki küçük koyu nokta."""
        a = self.kure[i]
        yonu = np.asarray(yonu, float) / np.linalg.norm(yonu)
        d = _dik(yonu) if dik is None else np.asarray(dik, float)
        m = a["p"] + yonu * (uz or a["r"] + .17)
        for s in (-1, 1):
            self.atom("e", m + s * .115 * d, harf="", r=.075, gri=.16, renk="#1B1D26")

    # --- ölçüler (doğrulama da bunları kullanır)
    def aci(self, i, j, k):
        """j tepe olmak üzere i–j–k açısı (derece)."""
        u, v = self.kure[i]["p"] - self.kure[j]["p"], self.kure[k]["p"] - self.kure[j]["p"]
        return math.degrees(math.acos(np.clip(u @ v / np.linalg.norm(u) / np.linalg.norm(v), -1, 1)))

    def uzaklik(self, i, j):
        return float(np.linalg.norm(self.kure[i]["p"] - self.kure[j]["p"]))

    def komsular(self, i, tur=None):
        return [b["j"] if b["i"] == i else b["i"] for b in self.bag if i in (b["i"], b["j"]) and (tur is None or b["tur"] in tur)]

    # --- dönüşümler
    def dondur(self, rx=0, ry=0, rz=0):
        R = _rot(rx, ry, rz)
        for a in self.kure:
            a["p"] = R @ a["p"]
        for c in self.cubuk:
            c["a"], c["b"] = R @ c["a"], R @ c["b"]
        self.R = R @ self.R
        return self

    def sinir(self):
        lo = np.min([a["p"] - a["r"] for a in self.kure] + [np.minimum(c["a"], c["b"]) - c["r"] for c in self.cubuk], axis=0)
        hi = np.max([a["p"] + a["r"] for a in self.kure] + [np.maximum(c["a"], c["b"]) + c["r"] for c in self.cubuk], axis=0)
        return lo, hi

    def ortala(self):
        """Sınır kutusunun ortasını başlangıca taşır: sıfır paralaks düzlemi = yapının derinlik ortası."""
        lo, hi = self.sinir()
        m = (lo + hi) / 2
        for a in self.kure:
            a["p"] = a["p"] - m
        for c in self.cubuk:
            c["a"], c["b"] = c["a"] - m, c["b"] - m
        return self


# ------------------------------------------------------------------ çizim (ışın–yüzey kesişimi, derinlik tamponu)
AMB, DIF, PAR, PAR_N, KENAR, KENAR_E = .50, .56, .26, 34, .52, .40


def _golge(n, dhat, taban):
    """n: (h, w, 3) birim normaller · taban: gri (h, w) / sayı ya da renk (3,) / (h, w, 3) → gölgelenmiş değer."""
    nl = np.clip(n @ ISIK, 0, 1)
    e = np.clip(n @ dhat, 0, 1)
    hv = ISIK + dhat
    hv = hv / np.linalg.norm(hv)
    par = PAR * np.clip(n @ hv, 0, 1) ** PAR_N
    t = np.clip(e / KENAR_E, 0, 1)
    kenar = 1 - KENAR * (1 - t * t * (3 - 2 * t))           # siluete doğru koyulaşan yumuşak kenar
    isik = (AMB + DIF * nl) * kenar
    taban = np.asarray(taban, np.float32)
    if taban.ndim in (1, 3):                               # renk
        return np.clip(taban * isik[..., None] + (par * kenar)[..., None], 0, 1)
    return np.clip(taban * isik + par * kenar, 0, 1)


# futbol topu deseni: kesik ikosahedron (12 beşgen koyu, 20 altıgen açık); yüzeye yapışık → iki gözde tutarlı
def _top_normalleri():
    fi = (1 + 5 ** .5) / 2
    V = []
    for a in (-1, 1):
        for b in (-fi, fi):
            V += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(V, float)
    V /= np.linalg.norm(V, axis=1)[:, None]
    F = []
    for i in range(12):
        for j in range(i + 1, 12):
            for k in range(j + 1, 12):
                if V[i] @ V[j] > .4 and V[j] @ V[k] > .4 and V[i] @ V[k] > .4:
                    f = V[i] + V[j] + V[k]
                    F.append(f / np.linalg.norm(f))
    h_v = 2 / 3 + 1 / (3 * 5 ** .5)                        # beşgen düzleminin merkeze uzaklığı (çevrel yarıçap 1)
    h_f = fi ** 2 / 3 ** .5 / (1 + fi ** 2) ** .5          # altıgen düzlemi = ikosahedronun iç yarıçapı
    return np.vstack([V / h_v, np.array(F) / h_f]).astype(np.float32)


_TOP = _top_normalleri()


def _top_deseni(n_yerel, renkli):
    v = n_yerel @ _TOP.T                                    # (h, w, 32): en büyük değer = ışının ilk çarptığı yüz
    sira = np.sort(v, axis=-1)
    besgen = np.argmax(v, axis=-1) < 12
    dikis = (sira[..., -1] - sira[..., -2]) < .016
    if renkli:
        out = np.where(besgen[..., None], _rgb("#2A2E3A"), _rgb("#F7F8FA"))
        return np.where(dikis[..., None], _rgb("#4A505E"), out).astype(np.float32)
    return np.where(dikis, .40, np.where(besgen, .27, .96)).astype(np.float32)


def _kure_ciz(tmp, c, r, taban, pid, s, k, olcek, desen=None, Rt=None, renkli=False):
    z, img, kim = tmp
    Hs, Ws = z.shape
    xc, rr = c[0] + s * k * c[2], r * 1.02
    x0, x1 = max(0, int((xc - rr) * olcek + Ws / 2) - 1), min(Ws, int((xc + rr) * olcek + Ws / 2) + 2)
    y0, y1 = max(0, int(Hs / 2 - (c[1] + rr) * olcek) - 1), min(Hs, int(Hs / 2 - (c[1] - rr) * olcek) + 2)
    if x0 >= x1 or y0 >= y1:
        return
    qx = (((np.arange(x0, x1) + .5) - Ws / 2) / olcek - c[0])[None, :].astype(np.float32)
    qy = ((Hs / 2 - (np.arange(y0, y1) + .5)) / olcek - c[1])[:, None].astype(np.float32)
    A = 1 + (s * k) ** 2
    B = -s * k * qx - c[2]
    disc = B * B - A * (qx * qx + qy * qy + c[2] * c[2] - r * r)
    m = disc >= 0
    t = (-B + np.sqrt(np.where(m, disc, 0))) / A
    zz = z[y0:y1, x0:x1]
    m &= t > zz
    if not m.any():
        return
    n = np.stack([(qx - s * k * t) / r, np.broadcast_to(qy / r, t.shape), (t - c[2]) / r], -1)
    dhat = np.array([-s * k, 0, 1.0]) / math.sqrt(A)
    if desen == "top":
        taban = _top_deseni((n @ Rt.T.astype(np.float32)), renkli)      # n_yerel = Rᵀ·n
    val = _golge(n, dhat, taban)
    zz[m] = t[m]
    img[y0:y1, x0:x1][m] = val[m]
    kim[y0:y1, x0:x1][m] = pid


def _silindir_ciz(tmp, a, b, rho, taban, s, k, olcek):
    z, img, kim = tmp
    Hs, Ws = z.shape
    L = float(np.linalg.norm(b - a))
    if L < 1e-9:
        return
    u = (b - a) / L
    d = np.array([-s * k, 0, 1.0])
    du = float(d @ u)
    A = float(d @ d) - du * du
    if A < 1e-7:                                            # ışına paralel çubuk: uçtan görünür, atlanır
        return
    xa, xb, rr = a[0] + s * k * a[2], b[0] + s * k * b[2], rho * 1.05
    x0, x1 = max(0, int((min(xa, xb) - rr) * olcek + Ws / 2) - 1), min(Ws, int((max(xa, xb) + rr) * olcek + Ws / 2) + 2)
    y0, y1 = max(0, int(Hs / 2 - (max(a[1], b[1]) + rr) * olcek) - 1), min(Hs, int(Hs / 2 - (min(a[1], b[1]) - rr) * olcek) + 2)
    if x0 >= x1 or y0 >= y1:
        return
    qx = (((np.arange(x0, x1) + .5) - Ws / 2) / olcek - a[0])[None, :].astype(np.float32)
    qy = ((Hs / 2 - (np.arange(y0, y1) + .5)) / olcek - a[1])[:, None].astype(np.float32)
    qz = -a[2]
    qu = qx * u[0] + qy * u[1] + qz * u[2]
    B = (-s * k * qx + qz) - qu * du
    disc = B * B - A * (qx * qx + qy * qy + qz * qz - qu * qu - rho * rho)
    m = disc >= 0
    t = (-B + np.sqrt(np.where(m, disc, 0))) / A
    sx = qu + t * du
    zz = z[y0:y1, x0:x1]
    m &= (sx >= 0) & (sx <= L) & (t > zz)
    if not m.any():
        return
    n = np.stack([(qx - s * k * t - sx * u[0]) / rho, (qy - sx * u[1]) / rho, (qz + t - sx * u[2]) / rho], -1)
    val = _golge(n, d / math.sqrt(float(d @ d)), taban)
    zz[m] = t[m]
    img[y0:y1, x0:x1][m] = val[m]
    kim[y0:y1, x0:x1][m] = 0


_yazi_bellek = {}


def _yazi(boy):
    boy = max(6, int(round(boy)))
    if boy not in _yazi_bellek:
        _yazi_bellek[boy] = ImageFont.truetype(YAZI, boy)
    return _yazi_bellek[boy]


def _harf_ciz(img, kim, pid, metin, ust, cx, cy, rp, ton):
    """Atomun ön yüzüne harf (ve yük işareti): yalnız o atomun GÖRÜNEN piksellerine basılır (örtüşme korunur)."""
    Hs, Ws = kim.shape
    boy = rp * (1.22 if len(metin) == 1 else .98)
    font = _yazi(boy)
    l, t, r, b = font.getbbox(metin)
    w, h = r - l, b - t
    isaret = rp * .30 if ust else 0
    kap = Image.new("L", (int(w + isaret * 1.5) + 6, int(h + rp * .5) + 6), 0)
    ciz = ImageDraw.Draw(kap)
    oy = int(rp * .25) + 3
    ciz.text((3 - l, oy - t), metin, font=font, fill=255)
    if ust:                                                 # fontta ⁺ ⁻ yok: işaret çubukla çizilir
        kal = max(2, rp * .085)
        ix, iy = 3 + w + isaret * .78, oy + isaret * .1
        ciz.rectangle([ix - isaret / 2, iy - kal / 2, ix + isaret / 2, iy + kal / 2], fill=255)
        if ust == "+":
            ciz.rectangle([ix - kal / 2, iy - isaret / 2, ix + kal / 2, iy + isaret / 2], fill=255)
    alfa = np.asarray(kap, np.float32) / 255
    x0 = int(round(cx - (w + isaret * 1.5) / 2)) - 3
    y0 = int(round(cy - h / 2)) - oy
    ax0, ay0 = max(0, -x0), max(0, -y0)
    x1, y1 = min(Ws, x0 + alfa.shape[1]), min(Hs, y0 + alfa.shape[0])
    x0, y0 = max(0, x0), max(0, y0)
    if x0 >= x1 or y0 >= y1:
        return
    al = alfa[ay0:ay0 + (y1 - y0), ax0:ax0 + (x1 - x0)] * (kim[y0:y1, x0:x1] == pid)
    if img.ndim == 3:
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - al[..., None]) + np.asarray(ton, np.float32) * al[..., None]
    else:
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - al) + ton * al


def _parcala(a, b, kesik):
    """Kesikli çubuk: (dolu, boş) uzunluklarıyla parçalar; iki uçta yarım boşluk."""
    L = np.linalg.norm(b - a)
    dolu, bos = kesik
    n = max(1, int(round((L + bos) / (dolu + bos))))
    adim = L / n
    do = adim * dolu / (dolu + bos)
    u = (b - a) / L
    return [(a + u * (i * adim + (adim - do) / 2), a + u * (i * adim + (adim + do) / 2)) for i in range(n)]


def goruntu(yapi, goz=0, k=0.0, olcek=40.0, W=400, H=400, renkli=False, ss=SS, harf=True, golge=False, kimlik=False):
    """Tek bakış. goz: +1 sol göz (x + k·z), −1 sağ göz (x − k·z), 0 düz. olcek: son resimde piksel / model birimi.
    → (H, W) gri ya da (H, W, 3) renkli float dizi [0, 1]; kimlik=True ise ayrıca üst örneklenmiş kimlik tamponu."""
    s = float(goz)
    Ws, Hs, ol = W * ss, H * ss, olcek * ss
    z = np.full((Hs, Ws), -1e9, np.float32)
    img = np.ones((Hs, Ws, 3) if renkli else (Hs, Ws), np.float32)
    kim = np.zeros((Hs, Ws), np.int16)
    if golge:                                               # düz resimde yumuşak yer gölgesi (yalnız süs)
        lo, hi = yapi.sinir()
        gy, gx = np.mgrid[0:Hs, 0:Ws].astype(np.float32)
        ex = ((gx - Ws / 2) / ol) / ((hi[0] - lo[0]) * .46)
        ey = ((Hs / 2 - gy) / ol - (lo[1] - (hi[1] - lo[1]) * .07)) / ((hi[1] - lo[1]) * .075)
        g = np.clip(1 - (ex * ex + ey * ey), 0, 1) ** 1.5 * .30
        img *= (1 - g)[..., None] if renkli else (1 - g)
    tmp = (z, img, kim)
    for bg in yapi.bag:                                     # bağlar: iki yarım (düz resimde her yarı kendi atomunun renginde)
        A, B = yapi.kure[bg["i"]], yapi.kure[bg["j"]]
        rho, gri, renk, kesik = BAG[bg["tur"]]
        if bg["vurgu"]:
            rho, gri, renk = rho * (1.9 if bg["tur"] in ("kafes", "hidrojen", "zayif") else 1.25), VURGU_BAG[0], VURGU_BAG[1]
        a, b = A["p"], B["p"]
        kay = [np.zeros(3)]
        if bg["tur"] == "cift":
            o = np.cross(b - a, [0, 0, 1.0])
            o = o / np.linalg.norm(o) if np.linalg.norm(o) > 1e-6 else np.array([0, 1.0, 0])
            kay = [o * .135, -o * .135]
        for o in kay:
            if kesik:
                u = (b - a) / np.linalg.norm(b - a)
                for p, q in _parcala(a + u * A["r"], b - u * B["r"], kesik):
                    _silindir_ciz(tmp, p + o, q + o, rho, _rgb(renk) if renkli else gri, s, k, ol)
            elif renkli and bg["tur"] in ("tek", "cift") and not bg["vurgu"]:
                ua = (b - a) / np.linalg.norm(b - a)
                orta = ((a + ua * A["r"]) + (b - ua * B["r"])) / 2
                for p, q, at in ((a, orta, A), (orta, b, B)):
                    c = _rgb(at["renk"])
                    _silindir_ciz(tmp, p + o, q + o, rho, c * .82 + .10, s, k, ol)
            else:
                _silindir_ciz(tmp, a + o, b + o, rho, _rgb(renk) if renkli else gri, s, k, ol)
    for c in yapi.cubuk:
        ton = _rgb(c["renk"]) if renkli else c["gri"]
        for p, q in (_parcala(c["a"], c["b"], c["kesik"]) if c["kesik"] else [(c["a"], c["b"])]):
            _silindir_ciz(tmp, p, q, c["r"], ton, s, k, ol)
    for i, a in enumerate(yapi.kure):
        _kure_ciz(tmp, a["p"], a["r"], _rgb(a["renk"]) if renkli else a["gri"], i + 1, s, k, ol, a["desen"], yapi.R, renkli)
    if harf:
        for i, a in enumerate(yapi.kure):
            if not a["harf"]:
                continue
            rp = a["r"] * ol
            if renkli:
                c = _rgb(a["renk"])
                ton = (1, 1, 1) if (c @ np.array([.3, .59, .11])) < .62 else _rgb("#1B1D26")
            else:
                ton = 1.0 if a["gri"] < .62 else .13
            cx = (a["p"][0] + s * k * (a["p"][2] + a["r"] * .97)) * ol + Ws / 2      # harf kürenin ÖN yüzünde
            _harf_ciz(img, kim, i + 1, a["harf"], a["ust"], cx, Hs / 2 - a["p"][1] * ol, rp, ton)
    out = img.reshape((H, ss, W, ss, 3) if renkli else (H, ss, W, ss)).mean(axis=(1, 3))
    return (out, kim) if kimlik else out


# ------------------------------------------------------------------ yerleşim, stereo ölçüsü, anaglif
def px(mm):
    return int(round(mm / 25.4 * DPI))


def yerlestir(yapi, en_mm, yuk_mm, mm_birim=None, pay_mm=1.6, k=None):
    """Yapıyı ortalar; basılı ölçeği (mm / model birimi) ve k'yi seçer. → bilgi sözlüğü."""
    yapi.ortala()
    lo, hi = yapi.sinir()
    hx, hy, hz = (hi - lo) / 2
    if mm_birim is None:
        mm_birim = min((en_mm / 2 - pay_mm - AYRIKLIK_UST_MM / 2) / hx, (yuk_mm / 2 - pay_mm) / hy)
    z_mm = hz * mm_birim                                    # en yakın (ve en uzak) noktanın kâğıda uzaklığı
    if k is None:
        k = min(K_ORTO, AYRIKLIK_UST_MM / (2 * z_mm))
    return dict(ad=yapi.ad, en_mm=en_mm, yuk_mm=yuk_mm, mm_birim=round(mm_birim, 4), k=round(k, 5), z_mm=round(z_mm, 2),
                ayriklik_mm=round(2 * k * z_mm, 3), derinlik_orani=round(k / K_ORTO, 3), W=px(en_mm), H=px(yuk_mm),
                tasma_mm=round(max(0.0, (hx * mm_birim + k * z_mm) - en_mm / 2, hy * mm_birim - yuk_mm / 2), 2))


def anaglif_birlestir(sol, sag):
    """R = SOL göz resmi; G = B = SAĞ göz resmi (uint8 gri diziler). Beyaz zemin iki gözde de 255 kalır."""
    return np.dstack([sol, sag, sag])


def _u8(a):
    return np.clip(np.rint(a * 255), 0, 255).astype(np.uint8)


def uret(yapi, en_mm, yuk_mm, mm_birim=None, k=None, ss=SS, pay_mm=1.6):
    """Anaglif üretir → SimpleNamespace(sol, sag, anaglif, bilgi). Yapı yerinde ortalanır."""
    b = yerlestir(yapi, en_mm, yuk_mm, mm_birim, pay_mm, k)
    ol = b["mm_birim"] / 25.4 * DPI
    sol = _u8(goruntu(yapi, +1, b["k"], ol, b["W"], b["H"], ss=ss))
    sag = _u8(goruntu(yapi, -1, b["k"], ol, b["W"], b["H"], ss=ss))
    return SimpleNamespace(sol=sol, sag=sag, anaglif=anaglif_birlestir(sol, sag), bilgi=b)


def duz_resim(yapi, en_mm, yuk_mm, mm_birim=None, ss=SS, golge=False, pay_mm=1.0, goz=0, k=0.0):
    """AYNI koordinatlardan renkli düz resim (gözlüksüz bakış, fotokopi). goz/k verilirse o gözün renkli bakışı (GIF)."""
    yapi.ortala()
    lo, hi = yapi.sinir()
    hx, hy, _ = (hi - lo) / 2
    if mm_birim is None:
        mm_birim = min((en_mm / 2 - pay_mm) / hx, (yuk_mm / 2 - pay_mm) / (hy * (1.12 if golge else 1)))
    return _u8(goruntu(yapi, goz, k, mm_birim / 25.4 * DPI, px(en_mm), px(yuk_mm), renkli=True, ss=ss, golge=golge))


def kaydet(dizi, yol, dpi=DPI):
    Image.fromarray(dizi).save(yol, dpi=(dpi, dpi), optimize=True)


# ================================================================== YAPILAR (gerçek koordinatlar)
# ------------------------------------------------------------------ moleküller (bağ uzunlukları Å, açılar derece)
def ch4(d=1.09):
    """Metan: düzgün dörtyüzlü; H–C–H = arccos(−1/3) = 109,47°."""
    y = Yapi("CH4")
    c = y.atom("C", (0, 0, 0))
    for kut, az in ((0, 0), (TETRA, 90), (TETRA, 210), (TETRA, 330)):
        y.bagla(c, y.atom("H", d * yon(kut, az)))
    return y


def nh3(aci=106.7, d=1.012):
    """Amonyak: üçgen piramit; H–N–H = 106,7° (≈ 107°). Bağın C₃ ekseniyle açısı: cos²α = (2cos θ + 1) / 3."""
    alfa = math.degrees(math.acos(math.sqrt((2 * math.cos(math.radians(aci)) + 1) / 3)))
    y = Yapi("NH3")
    n = y.atom("N", (0, 0, 0))
    for az in (90, 210, 330):
        y.bagla(n, y.atom("H", d * yon(180 - alfa, az)))
    y.cift(n, (0, 1, 0), dik=(1, 0, 0))
    return y


def h2o(aci=104.5, d=.9572):
    """Su: kırık doğru (açısal); H–O–H = 104,5°. İki ortaklanmamış çift yaklaşık dörtyüzlü yönlerde."""
    y = Yapi("H2O")
    o = y.atom("O", (0, 0, 0))
    yari = math.radians(aci / 2)
    for s in (-1, 1):
        y.bagla(o, y.atom("H", d * np.array([s * math.sin(yari), -math.cos(yari), 0])))
    f = math.radians(TETRA / 2)
    for s in (-1, 1):
        y.cift(o, (0, math.cos(f), s * math.sin(f)), dik=(1, 0, 0))
    return y


def co2(d=1.16):
    """Karbondioksit: doğrusal; O=C=O = 180°."""
    y = Yapi("CO2")
    c = y.atom("C", (0, 0, 0))
    for s in (-1, 1):
        y.bagla(c, y.atom("O", (s * d, 0, 0)), "cift")
    return y


def bf3(d=1.31):
    """Bor triflorür: düzlem üçgen; F–B–F = 120°."""
    y = Yapi("BF3")
    b = y.atom("B", (0, 0, 0))
    for a in (90, 210, 330):
        y.bagla(b, y.atom("F", (d * math.cos(math.radians(a)), d * math.sin(math.radians(a)), 0)))
    return y


# ------------------------------------------------------------------ örgüler (doğrulama için geniş örgü + sayfa için parça)
NACL_A, ELMAS_A = 5.64, 3.567                 # küp kenarı (Å)
GRAFIT_D, GRAFIT_C = 1.42, 3.35               # tabaka içi C–C, tabakalar arası (Å)
BUZ_D = 2.76                                  # O···O (Å); ideal altıgen örgü: c = 8d/3, a = c / √(8/3)
BUZ_C = 8 * BUZ_D / 3
BUZ_A = BUZ_C / math.sqrt(8 / 3)


def nacl_orgu(n=5):
    """n×n×n iyon; komşu aralığı a/2. → [(el, p)]"""
    d = NACL_A / 2
    return [("Cl" if (i + j + k) % 2 == 0 else "Na", d * np.array([i, j, k], float)) for i in range(n) for j in range(n) for k in range(n)]


def elmas_orgu(n=3):
    """n³ küp hücre (8 atom/hücre): yüzey merkezli örgü + (¼,¼,¼) kaydırılmış ikinci örgü. → kesirli koordinat listesi"""
    ymk = [(0, 0, 0), (.5, .5, 0), (.5, 0, .5), (0, .5, .5)]
    return [np.array([i + f[0] + s, j + f[1] + s, k + f[2] + s]) for i in range(n) for j in range(n) for k in range(n) for f in ymk for s in (0, .25)]


def grafit_orgu(n=4, katman=3):
    """AB dizilimli grafit: katman başına n×n hücre, 2 atom/hücre. → [(katman no, p)] (p: x, y = yığılma, z)"""
    d = GRAFIT_D
    a1, a2 = np.array([3 ** .5 * d, 0]), np.array([3 ** .5 * d / 2, 1.5 * d])
    out = []
    for L in range(katman):
        kay = np.array([0, d]) * (L % 2)
        for m in range(-n, n + 1):
            for q in range(-n, n + 1):
                for t in ((0, 0), (0, d)):
                    p = m * a1 + q * a2 + t + kay
                    out.append((L, np.array([p[0], L * GRAFIT_C, p[1]])))
    return out


def _buz_p(u, v, w):
    """Altıgen hücrede kesirli (u, v, w) → Å; altıgen eksen (c) = y."""
    return np.array([BUZ_A * (u + v / 2), BUZ_C * w, BUZ_A * v * 3 ** .5 / 2])


BUZ_BAZ = {"A": (1 / 3, 1 / 3, 0.0), "B": (2 / 3, 2 / 3, .5), "C": (1 / 3, 1 / 3, 3 / 8), "D": (2 / 3, 2 / 3, 7 / 8)}


def buz_orgu(n=3):
    """Altıgen buzun (Ih) oksijen örgüsü, (2n+1)³ hücre. → nokta listesi"""
    return [_buz_p(u + m, v + q, w + t) for m in range(-n, n + 1) for q in range(-n, n + 1) for t in range(-n, n + 1)
            for u, v, w in BUZ_BAZ.values()]


def komsu_sayisi(noktalar, i, d, tol=.04):
    """i. noktanın d (±tol·d) uzaklığındaki komşu sayısı."""
    P = np.asarray(noktalar, float)
    u = np.linalg.norm(P - P[i], axis=1)
    return int(((u > d * (1 - tol)) & (u < d * (1 + tol))).sum())


def en_yakin(noktalar, i):
    P = np.asarray(noktalar, float)
    u = np.linalg.norm(P - P[i], axis=1)
    return float(u[u > 1e-6].min())


def nacl():
    """Sofra tuzu: 3×3×3 = 27 iyon (13 Na⁺ + 14 Cl⁻). Merkezdeki Na⁺ ve 6 komşusuna giden çubuklar vurgulu."""
    y = Yapi("NaCl")
    d = NACL_A / 2
    idx = {}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                el = "Cl" if (i + j + k) % 2 == 0 else "Na"
                merkez = (i, j, k) == (1, 1, 1)
                idx[(i, j, k)] = y.atom(el, d * np.array([i - 1, j - 1, k - 1], float), vurgu=merkez, gri=.26 if merkez else None,
                                         renk="#5A2FA0" if merkez else None)
    for (i, j, k), a in idx.items():
        for di, dj, dk in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            b = idx.get((i + di, j + dj, k + dk))
            if b is not None:
                y.bagla(a, b, "kafes", vurgu=(1, 1, 1) in ((i, j, k), (i + di, j + dj, k + dk)))
    y.odak = idx[(1, 1, 1)]
    return y


def elmas(odak=(.25, .75, .75)):
    """Elmas: bir küp hücre (18 atom görünür: 8 köşe + 6 yüz + 4 iç), 16 bağ; bir iç atomun 4 bağı vurgulu."""
    y = Yapi("elmas")
    P = [p for p in elmas_orgu(2) if (p <= 1 + 1e-9).all()]
    P = [p for i, p in enumerate(P) if not any(np.allclose(p, q) for q in P[:i])]
    d = 3 ** .5 / 4
    oi = [i for i, p in enumerate(P) if np.allclose(p, odak)][0]
    for i, p in enumerate(P):
        y.atom("C", ELMAS_A * (p - .5), harf="", r=.34, vurgu=i == oi, gri=.24 if i == oi else .52,
               renk="#15171D" if i == oi else "#4A505E")
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if abs(np.linalg.norm(P[i] - P[j]) - d) < 1e-6:
                y.bagla(i, j, "tek", vurgu=oi in (i, j))
    h = ELMAS_A / 2
    for a in (-h, h):                                       # hücre çerçevesi (ince)
        for b in (-h, h):
            for e in range(3):
                p, q = [a, b], [a, b]
                p.insert(e, -h), q.insert(e, h)
                y.cubuk_ekle(p, q, r=.022, gri=.80, renk="#C9D0DA")
    y.odak = oi
    return y


def _altigen_pul(merkezler):
    d = GRAFIT_D
    a1, a2 = np.array([3 ** .5 * d, 0]), np.array([3 ** .5 * d / 2, 1.5 * d])
    pts = []
    for m, q in merkezler:
        c = np.array([0, -d]) + m * a1 + q * a2
        for j in range(6):
            p = c + d * np.array([math.cos(math.radians(90 + 60 * j)), math.sin(math.radians(90 + 60 * j))])
            if not any(np.linalg.norm(p - t) < 1e-6 for t in pts):
                pts.append(p)
    return pts


def grafit():
    """Grafit: üç tabaka (A–B–A), tabaka başına 4 altıgen (16 atom). Orta tabakada bir atomun 3 bağı vurgulu;
    üst üste gelen atomlar arasındaki kesik çizgiler tabakalar arası zayıf etkileşimi gösterir."""
    y = Yapi("grafit")
    d = GRAFIT_D
    pul = _altigen_pul([(0, 0), (1, 0), (0, 1), (1, 1)])
    mer = np.mean(pul, axis=0)
    kat = []
    for L in range(3):
        kay = np.array([0, d]) * (L % 2)
        kat.append([y.atom("C", (p[0] + kay[0] - mer[0], (L - 1) * GRAFIT_C, p[1] + kay[1] - mer[1]), harf="", r=.33, gri=.50, renk="#4A505E")
                    for p in pul])
    for ids in kat:
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                if abs(y.uzaklik(ids[a], ids[b]) - d) < 1e-6:
                    y.bagla(ids[a], ids[b], "tek")
    orta = kat[1]
    oi = min((i for i in orta if len(y.komsular(i)) == 3), key=lambda i: np.linalg.norm(y.kure[i]["p"][[0, 2]]))
    y.kure[oi].update(vurgu=True, gri=.24, renk="#15171D")
    for b in y.bag:
        if oi in (b["i"], b["j"]):
            b["vurgu"] = True
    for L in (0, 1):                                        # üst üste gelen atom çiftleri: zayıf etkileşim
        for a in kat[L]:
            for b in kat[L + 1]:
                if np.linalg.norm((y.kure[a]["p"] - y.kure[b]["p"])[[0, 2]]) < 1e-6:
                    y.bagla(a, b, "zayif")
    y.odak = oi
    return y


def buz(merkezler=((0, 0), (1, 0)), ek1=(), tohum=4):
    """Altıgen buz: iki bitişik altıgen kanal × iki büzgülü tabaka = 20 H₂O. Her O–O çizgisinde tam bir H, her O'da
    tam iki H (buz kuralları). Dört komşusu da resimde olan bir molekülün 4 hidrojen bağı vurgulu."""
    y = Yapi("buz")
    s1, s2 = set(), set()
    for m, q in merkezler:
        s1 |= {(m, q), (m - 1, q), (m, q - 1)}
        s2 |= {(m - 1, q - 1), (m, q - 1), (m - 1, q)}
    s1 |= set(ek1)
    O = {}
    for m, q in sorted(s1):
        O[("C", m, q)] = _buz_p(1 / 3 + m, 1 / 3 + q, 3 / 8)
        O[("A", m, q)] = _buz_p(1 / 3 + m, 1 / 3 + q, 1.0)
    for m, q in sorted(s2):
        O[("B", m, q)] = _buz_p(2 / 3 + m, 2 / 3 + q, .5)
        O[("D", m, q)] = _buz_p(2 / 3 + m, 2 / 3 + q, 7 / 8)
    ad = list(O)
    P = np.array([O[a] for a in ad])
    hepsi = np.array(buz_orgu(2))
    kenar = [(i, j) for i in range(len(ad)) for j in range(i + 1, len(ad)) if abs(np.linalg.norm(P[i] - P[j]) - BUZ_D) < .02]
    der = [sum(i in e for e in kenar) for i in range(len(ad))]
    rng = np.random.default_rng(tohum)
    sira = [kenar[i] for i in rng.permutation(len(kenar))]
    veren = {}

    def dene(n):                                            # her kenara bir verici seç: derece − 2 ≤ verilen ≤ 2
        if n == len(sira):
            return all(der[i] - 2 <= sum(v == i for v in veren.values()) <= 2 for i in range(len(ad)))
        for v in (sira[n] if rng.random() < .5 else sira[n][::-1]):
            if sum(x == v for x in veren.values()) < 2:
                veren[sira[n]] = v
                if dene(n + 1):
                    return True
                del veren[sira[n]]
        return False

    assert dene(0), "buz kuralları sağlanamadı"
    ok = [y.atom("O", p - P.mean(axis=0), harf="", r=.40) for p in P]
    odak = next(i for i, a in enumerate(ad) if a[0] == "B" and der[i] == 4)
    y.kure[ok[odak]].update(harf="O", vurgu=True, gri=.30, renk="#A12817")
    for i in range(len(ad)):
        yonler = [(hp - P[i]) / BUZ_D for hp in hepsi if abs(np.linalg.norm(hp - P[i]) - BUZ_D) < .02]      # 4 dörtyüzlü yön
        ic = {tuple(np.round((P[j if a == i else a] - P[i]) / BUZ_D, 3)): (a, j) for a, j in kenar if i in (a, j)}
        h_yon = [(P[(j if a == i else a)] - P[i]) / BUZ_D for (a, j) in kenar if i in (a, j) and veren[(a, j)] == i]
        bos = [u for u in yonler if tuple(np.round(u, 3)) not in ic]
        h_yon += bos[:2 - len(h_yon)]
        assert len(h_yon) == 2
        for u in h_yon:
            y.bagla(ok[i], y.atom("H", y.kure[ok[i]]["p"] + .96 * u, harf="", r=.25))
    y.hbag = []
    for (a, j) in kenar:                                    # hidrojen bağı: H ··· O (kesik); vericinin H'sinden alıcının O'suna
        v = veren[(a, j)]
        al = j if v == a else a
        hi = min(y.komsular(ok[v]), key=lambda h: np.linalg.norm(y.kure[h]["p"] - y.kure[ok[al]]["p"]))
        y.bagla(hi, ok[al], "hidrojen", vurgu=odak in (a, j))
        y.hbag.append((ok[v], hi, ok[al]))
    y.odak, y.oksijen = ok[odak], ok
    return y


# ------------------------------------------------------------------ 10. sınıf sahneleri
def gaz_kutusu(tohum=11, n_n2=8, n_o2=2, boyut=(11.0, 6.0, 5.0)):
    """Gaz taneciği kutusu (birim keyfî; tanecikler görünsün diye büyütülmüş ve sıkıştırılmış): 5 × 2 bölmeye birer
    molekül (sağa-sola düzgün yayılım), derinlik ve yön tamamen rastgele; incelen çizgi = hareket izi (hızın tersi)."""
    y = Yapi("gaz kutusu", birim="birim")
    rng = np.random.default_rng(tohum)
    h = np.array(boyut) / 2
    for a in (-1, 1):
        for b in (-1, 1):
            for e in range(3):
                p, q = [a * 1.0, b * 1.0], [a * 1.0, b * 1.0]
                p.insert(e, -1.0), q.insert(e, 1.0)
                y.cubuk_ekle(np.array(p) * h, np.array(q) * h, r=.055, gri=.45, renk="#6F7A8A")
            for c in (-1, 1):
                y.atom("k", np.array([a, b, c]) * h, harf="", r=.055, gri=.45, renk="#6F7A8A")
    y.tanecik = []
    turler = ["N"] * n_n2 + ["O"] * n_o2
    rng.shuffle(turler)
    pay = 1.05
    for n, el in enumerate(turler):
        ix, iy = n % 5, n // 5
        for _ in range(2000):
            p = np.array([-h[0] + (ix + .22 + .56 * rng.random()) * boyut[0] / 5, -h[1] + (iy + .24 + .52 * rng.random()) * boyut[1] / 2,
                          (rng.random() * 2 - 1) * (h[2] - pay)])
            u = rng.normal(size=3); u /= np.linalg.norm(u)      # molekül ekseni
            v = rng.normal(size=3); v /= np.linalg.norm(v)      # hız yönü (üç boyutta rastgele)
            yari = .47 if el == "N" else .50
            uclar = [p - yari * u, p + yari * u]
            if (all((np.abs(t) < h - .62).all() for t in uclar) and (np.abs(p - v * 2.55) < h - .15).all()
                    and all(np.linalg.norm(p - t["p"]) > 2.1 for t in y.tanecik)):
                break
        else:
            raise RuntimeError("gaz kutusu yerleşmedi")
        i, j = (y.atom(el, t, r=.50) for t in uclar)
        y.bagla(i, j, "tek")
        for a, b, r in ((.95, 1.5, .07), (1.68, 2.08, .052), (2.26, 2.52, .036)):      # incelen hareket izi
            y.cubuk_ekle(p - v * a, p - v * b, r=r, gri=.66, renk="#9AA4B2")
        y.tanecik.append(dict(el=el, p=p, v=v))
    return y


MOL_HACMI_L, TOP_CAP_CM = 22.4, 22.0


def mol_kupu(tohum=3):
    """1 mol gazın NŞA'daki hacmi: kenarı ∛22 400 cm³ = 28,19 cm olan küp, yanında 22 cm çaplı futbol topu (birim cm)."""
    y = Yapi("22,4 L küp", birim="cm")
    a = (MOL_HACMI_L * 1000) ** (1 / 3)
    for u in (0, a):
        for v in (0, a):
            for e in range(3):
                p, q = [u, v], [u, v]
                p.insert(e, 0), q.insert(e, a)
                y.cubuk_ekle(p, q, r=.30, gri=.36, renk="#3D2F8C")
            for w in (0, a):
                y.atom("k", (u, v, w), harf="", r=.30, gri=.36, renk="#3D2F8C")
    rng = np.random.default_rng(tohum)
    for _ in range(16):                                     # küpün içinde seyrek gaz tanecikleri (temsilî)
        y.atom("g", 1.6 + rng.random(3) * (a - 3.2), harf="", r=.62, gri=.62, renk="#13A3A6")
    r = TOP_CAP_CM / 2
    y.atom("top", (a + 6.5 + r, r, a / 2 + 1.0), harf="", r=r, gri=.96, renk="#F7F8FA", desen="top")
    y.kenar = a
    return y


def hidrasyon(iyon="Na"):
    """Hidrasyon kabuğu: iyonun çevresinde sekizyüzlü dizilmiş 6 su molekülü.
    Na⁺: suyun O ucu iyona döner (Na–O 2,40 Å). Cl⁻: suyun bir H'si iyona döner (Cl···H 2,24 Å; Cl–O 3,20 Å)."""
    y = Yapi("hidrasyon " + iyon)
    if iyon == "Na":
        m = y.atom("Na", (0, 0, 0), ust="+", r=.74, gri=.42)
    else:
        m = y.atom("Cl", (0, 0, 0), ust="−", r=1.12, gri=.88)
    y.su = []
    eksen = [np.array(v, float) for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
    for n, e in enumerate(eksen):
        d1 = _dik(e)
        d2 = np.cross(e, d1)
        f = math.radians(25 + 47 * n)
        dk = math.cos(f) * d1 + math.sin(f) * d2          # su düzleminin iyon ekseni çevresindeki dönüşü
        if iyon == "Na":
            o = y.atom("O", 2.40 * e)
            yari = math.radians(104.5 / 2)
            hs = [y.atom("H", y.kure[o]["p"] + .9572 * (math.cos(yari) * e + s * math.sin(yari) * dk), r=.27) for s in (-1, 1)]
            y.bagla(m, o, "zayif")
        else:
            o = y.atom("O", 3.20 * e)
            t = math.radians(104.5)
            hs = [y.atom("H", y.kure[o]["p"] - .9572 * e, r=.27),
                  y.atom("H", y.kure[o]["p"] + .9572 * (-math.cos(t) * e + math.sin(t) * dk), r=.27)]
            y.bagla(m, hs[0], "zayif")
        for h in hs:
            y.bagla(o, h)
        y.su.append((o, hs[0], hs[1]))
    y.iyon = m
    return y


# ================================================================== ÜNİTE GÖRSELLERİ (meta.json "uc_boyut")
# ad: (kurucu, dönüşler [(rx, ry, rz) sırayla], anaglif en × yük (mm), mm / model birimi (None: sığdır), düz resim en × yük (mm))
# Moleküller ortak ölçekte: 1 Å = 15 mm (150 milyon kat büyütme); k = K_ORTO ya da ona çok yakın (derinlik gerçek oranında).
MOL_OLCEK = 15.0
KATALOG = {
    "ch4": ("ch4", [(20, 18, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "nh3": ("nh3", [(24, 14, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "h2o": ("h2o", [(10, 35, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "co2": ("co2", [(12, 40, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "bf3": ("bf3", [(-50, 18, 0)], (55, 40), MOL_OLCEK, (22, 19)),
    "nacl": ("nacl", [(14, -22, 0)], (58, 55), None, (24, 23)),
    "elmas": ("elmas", [(16, -27, 0)], (58, 55), None, (24, 23)),
    "grafit": ("grafit", [(24, -20, 0)], (58, 55), None, (24, 23)),
    "buz": ("buz", [(0, 4, 0), (66, 0, 0)], (58, 55), None, (24, 23)),
    "gaz": ("gaz_kutusu", [(12, -18, 0)], (92, 51), None, (44, 25)),
    "kup": ("mol_kupu", [(14, -24, 0)], (78, 49), None, (38, 24)),
    "hid-na": ("hidrasyon:Na", [(20, -28, 0)], (46, 46), None, (21, 21)),
    "hid-cl": ("hidrasyon:Cl", [(20, -28, 0)], (46, 46), None, (21, 21)),
}
GOLGELI = {"ch4", "nh3", "h2o", "co2", "bf3"}          # düz resimde zemin gölgesi (tek moleküller)
TEST = {"yazi": (54, 13), "derinlik": (54, 20)}       # gözlük testi desenleri (mm)
TEST_AYRIKLIK_MM = 2.4


def tanim(giris):
    """meta.json "uc_boyut" öğesi → tam tanım. 'ch4' (KATALOG) ya da sözlük:
    {"ad": "ch4-yan", "yapi": "ch4", "donus": [[60, 10, 0]], "en": 55, "yuk": 40, "mm_birim": 15, "duz": [22, 19],
     "golge": true}. Eksik alanlar KATALOG'daki aynı yapıdan (yoksa molekül ölçüsünden) gelir."""
    if isinstance(giris, str):
        giris = {"ad": giris}
    ad = giris["ad"]
    kaynak = KATALOG.get(giris.get("katalog") or ad) or KATALOG.get(giris.get("yapi", ""), None)
    kurucu, donus, (en, yuk), mb, (den, dyuk) = kaynak or (giris.get("yapi", ad), [(0, 0, 0)], (55, 40), MOL_OLCEK, (22, 19))
    return dict(ad=ad, yapi=giris.get("yapi", kurucu), donus=[tuple(d) for d in giris.get("donus", donus)],
                en=float(giris.get("en", en)), yuk=float(giris.get("yuk", yuk)), mm_birim=giris.get("mm_birim", mb),
                duz=tuple(float(v) for v in giris.get("duz", (den, dyuk))), golge=bool(giris.get("golge", ad in GOLGELI)))


def yapi_kur(t, moduller=()):
    """Tanımdaki kurucuyu (önce ünitenin modülleri, sonra bu motor) çağırır; dönüşleri uygular, ortalar.
    'hidrasyon:Na' biçimi kurucuya bir argüman verir."""
    ad, _, arg = t["yapi"].partition(":")
    fn = next((getattr(m, ad) for m in moduller if hasattr(m, ad)), None) or globals().get(ad)
    if not callable(fn):
        raise KeyError(f"3B yapı kurucusu yok: {ad} (KATALOG: {', '.join(KATALOG)} · ya da ünitenin modülünde bir fonksiyon)")
    y = fn(arg) if arg else fn()
    for d in t["donus"]:
        y.dondur(*d)
    return y.ortala()


_KOD = None


def _kod_imzasi():
    global _KOD
    if _KOD is None:
        with open(__file__, "rb") as fp:
            _KOD = hashlib.sha1(fp.read()).hexdigest()[:12]
    return _KOD


def _sade(v):
    if isinstance(v, np.ndarray):
        return np.round(v, 4).tolist()
    if isinstance(v, (float, np.floating)):
        return round(float(v), 6)
    return v


def imza(t, y):
    """Tanım + küreler + bağlar + çubuklar + motorun kaynak kodu → kısa sha1 (değişmedikçe resim yeniden çizilmez)."""
    veri = [t, [sorted((k, _sade(v)) for k, v in d.items()) for d in y.kure + y.bag + y.cubuk], _kod_imzasi()]
    return hashlib.sha1(json.dumps(veri, sort_keys=True, default=str).encode()).hexdigest()[:16]


def unite_gorselleri(klasor, girisler, moduller=(), zorla=False, sessiz=False):
    """Ünitenin gorsel/ klasörüne 3B resimlerini üretir (gerekirse) → {ad: bilgi} (gorsel/uc-boyut.json'a da yazılır).
    Her yapı için: ana-<ad>.png (anaglif, basılı boyutunda 300 dpi), duz-<ad>.png (düz, küçük), duz-<ad>-b.png
    (düz, anaglif boyutunda: fotokopi nüshasında anaglifin yerine geçer)."""
    gorsel = os.path.join(klasor, "gorsel")
    os.makedirs(gorsel, exist_ok=True)
    json_yol = os.path.join(gorsel, "uc-boyut.json")
    try:
        with open(json_yol, encoding="utf-8") as fp:
            eski = json.load(fp)
    except (OSError, ValueError):
        eski = {}
    bilgi, cizilen = {}, []
    for giris in girisler:
        t = tanim(giris)
        y = yapi_kur(t, moduller)
        im = imza(t, y)
        dosya = {k: os.path.join(gorsel, f) for k, f in (("ana", f"ana-{t['ad']}.png"), ("duz", f"duz-{t['ad']}.png"), ("buyuk", f"duz-{t['ad']}-b.png"))}
        if not zorla and eski.get(t["ad"], {}).get("imza") == im and all(os.path.exists(p) for p in dosya.values()):
            bilgi[t["ad"]] = eski[t["ad"]]
            continue
        s = uret(y, t["en"], t["yuk"], t["mm_birim"])
        kaydet(s.anaglif, dosya["ana"])
        kaydet(duz_resim(y, *t["duz"], golge=t["golge"]), dosya["duz"])
        kaydet(duz_resim(y, t["en"], t["yuk"], golge=t["golge"]), dosya["buyuk"])
        b = {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in s.bilgi.items()}
        b.update(imza=im, yapi=t["yapi"], birim=y.birim, kure=len(y.kure), donus=[list(d) for d in t["donus"]],
                 duz_en=t["duz"][0], duz_yuk=t["duz"][1], kb=round(os.path.getsize(dosya["ana"]) / 1024))
        bilgi[t["ad"]] = b
        cizilen.append(t["ad"])
    kayit = dict(sabit=dict(goz_araligi_mm=GOZ_ARALIGI_MM, okuma_mm=OKUMA_MM, k_orto=round(K_ORTO, 5), ayriklik_ust_mm=AYRIKLIK_UST_MM,
                            dpi=DPI, mol_olcek_mm=MOL_OLCEK), **bilgi)
    if kayit != eski:
        with open(json_yol, "w", encoding="utf-8") as fp:
            json.dump(kayit, fp, ensure_ascii=False, indent=1)
    if cizilen and not sessiz:
        print(f"3B resimler çizildi ({len(cizilen)}): {', '.join(cizilen)} → {os.path.relpath(gorsel)}")
    return bilgi


# ------------------------------------------------------------------ gözlük testi (aynı anaglif_birlestir yolundan)
def _test_yazi_tipi(boy, yol=None):
    return ImageFont.truetype(yol or YAZI, boy)


def test_yazi(en_mm=54, yuk_mm=13):
    """SOL yazısı yalnız SOL göz resminde (kâğıtta camgöbeği), SAĞ yazısı yalnız SAĞ göz resminde (kâğıtta kırmızı).
    Gözlük doğru takılıysa sol göz (kırmızı cam) yalnız SOL'u, sağ göz (camgöbeği cam) yalnız SAĞ'ı koyu görür."""
    W, H = px(en_mm), px(yuk_mm)
    sol, sag = Image.new("L", (W, H), 255), Image.new("L", (W, H), 255)
    f_ = _test_yazi_tipi(int(H * .78))
    for im, metin, x in ((sol, "SOL", W * .25), (sag, "SAĞ", W * .75)):
        ImageDraw.Draw(im).text((x, H * .5), metin, font=f_, fill=40, anchor="mm")
    return anaglif_birlestir(np.asarray(sol), np.asarray(sag))


def test_derinlik(en_mm=54, yuk_mm=20):
    """A dairesi çapraz ayrıklıkla (+2,4 mm: kâğıdın önünde), B dairesi ters ayrıklıkla (−2,4 mm: kâğıdın arkasında).
    Çerçeve sıfır ayrıklıkta (kâğıt düzlemi). Gözlük ters takılırsa A arkada, B önde görünür."""
    W, H = px(en_mm), px(yuk_mm)
    sol, sag = Image.new("L", (W, H), 255), Image.new("L", (W, H), 255)
    d = px(TEST_AYRIKLIK_MM) / 2
    f_ = _test_yazi_tipi(int(H * .42))
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
            c.text((cx, H / 2 - H * .01), harf, font=f_, fill=45, anchor="mm")
    return anaglif_birlestir(np.asarray(sol), np.asarray(sag))


def gozluk_testleri(hedef=ORTAK_GORSEL, zorla=False):
    """Gözlük testi desenleri (bütün kitapta aynı): yerel-ortak/gorsel/test-yazi.png, test-derinlik.png → {ad: yol}."""
    os.makedirs(hedef, exist_ok=True)
    out = {}
    for ad, fn in (("yazi", test_yazi), ("derinlik", test_derinlik)):
        yol = os.path.join(hedef, f"test-{ad}.png")
        if zorla or not os.path.exists(yol) or os.path.getmtime(yol) < os.path.getmtime(__file__):
            kaydet(fn(*TEST[ad]), yol)
        out[ad] = yol
    return out

