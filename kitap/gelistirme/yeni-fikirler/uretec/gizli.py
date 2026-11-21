"""Gizli cevap · kırmızı camdan bak.

Cevap açık camgöbeği (yalnız C mürekkebi, %35) basılır. Aynı yere, aynı yazı tipi ve boyda üç ÇELDİRİCİ cevap
(yalnız M ve Y mürekkebi: kırmızı, macenta, turuncu) ve hafif bir harf konfetisi basılır. 3B gözlüğün KIRMIZI camı yalnız
kırmızı ışığı geçirir: M ve Y kırmızıyı yansıtır (kâğıt gibi açık görünür), C kırmızıyı soğurur (koyu görünür). Cam = R kanalı.
Gerçek cevabın altındaki M/Y miktarı, çıplak gözle parlaklığı (L*) çevresiyle aynı olacak kadar azaltılır; bu, R kanalını
neredeyse değiştirmez. Böylece çıplak göz üst üste binmiş dört cevap görür, gerçeğini seçemez; kırmızı cam yalnız gerçeğini gösterir.

Baskı modeli (çıkarmalı, ideal üst üste basım): her mürekkep, kaplama oranı t ile doğrusal RGB'yi 1 − t·(1 − dolu) ile çarpar.
Dolu mürekkep katsayıları ofset C, M, Y'ye yakın seçildi (aşağıda).

Ölçü · "seçicilik": her aday yazı j (gerçek + 3 çeldirici) için yalnız ona ait piksellerde (öbür maskeler < 0,1)
  karşıtlık_j = |ort(V, yazı_j) − ort(V, zemin)| / sd(V, zemin)          (zemin: bütün maskeler < 0,02)
  kırmızı cam V = R (doğrusal):  gerçek ≥ 3 ve gerçek / en güçlü çeldirici ≥ 3 · Weber (zemin − yazı)/zemin ≥ 0,25
  çıplak göz V = L*, a*, b*:     her kanalda gerçek / en güçlü çeldirici ≤ 1 (gerçek cevap çeldiricilerden belirgin değil)
dogrula.py ölçüleri PNG'lerden ve kaydedilen maskelerden yeniden hesaplar.
"""
import json
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
GORSEL = os.path.join(KLASOR, "gorsel")
FONT = os.path.abspath(os.path.join(BURA, "..", "..", "..", "fontlar"))
BALOO = os.path.join(FONT, "baloobhaijaan2", "static", "BalooBhaijaan2-800.ttf")
NUNITO = os.path.join(FONT, "nunito", "static", "Nunito-900.ttf")
DPI = 400
MM = DPI / 25.4

# dolu mürekkebin doğrusal RGB katsayısı (kâğıt = 1): ofset C, M, Y'ye yakın
CYAN = np.array([0.06, 0.36, 0.78])
MAG = np.array([0.84, 0.05, 0.27])
SARI = np.array([0.98, 0.85, 0.06])
C_YAZI = 0.35          # cevap: açık camgöbeği (%35 C)
TABAN = (0.12, 0.16)   # bütün kutuya hafif pembe-şeftali zemin (M, Y)
RENKLER = [  # konfeti (M, Y, ağırlık): açık pembe, sarı, şeftali; hiçbirinde C yok
    (0.30, 0.05, 4), (0.00, 0.55, 3), (0.20, 0.45, 3), (0.55, 0.00, 2), (0.00, 0.90, 2), (0.70, 0.30, 1)]
CELDIRICI_RENK = [(1.0, 1.0), (0.55, 1.0), (1.0, 0.0)]   # kırmızı, turuncu, macenta (üçü her kutuda)
HARFLER = "ABCÇDEFGHIİKLMNOPRSŞTUÜVYZ0123456789+·"
ESIK = {"cam": 3.0, "cam_oran": 3.0, "cam_weber": 0.25, "goz_oran": 1.0}

# Sorular (9. sınıf · Usturlap Çarkı'nın ön yüzüyle bulunabilir). cevap: (metin, üst simge)
SORULAR = [
    {"no": 1, "soru": "<sub>13</sub>Al atomunun katman dizilimi nedir?", "cevap": ("2·8·3", ""), "tur": "dizilim", "z": 13,
     "celdirici": [("2·8·2", ""), ("2·8·4", ""), ("2·8·1", "")]},
    {"no": 2, "soru": "<sub>17</sub>Cl<sup>−</sup> iyonunda kaç elektron vardır?", "cevap": ("18 elektron", ""), "tur": "elektron", "z": 17, "yuk": -1,
     "celdirici": [("17 elektron", ""), ("16 elektron", ""), ("20 elektron", "")]},
    {"no": 3, "soru": "<sub>12</sub>Mg atomu kaçıncı periyottadır?", "cevap": ("3. periyot", ""), "tur": "periyot", "z": 12,
     "celdirici": [("2. periyot", ""), ("4. periyot", ""), ("3. grup", "")]},
    {"no": 4, "soru": "2. periyot, 15. grup elementi hangisidir?", "cevap": ("N · azot", ""), "tur": "yer", "z": 7,
     "celdirici": [("P · fosfor", ""), ("O · oksijen", ""), ("C · karbon", "")]},
    {"no": 5, "soru": "<sub>20</sub>Ca atomu hangi iyonu oluşturur?", "cevap": ("Ca", "2+"), "tur": "iyon", "z": 20,
     "celdirici": [("Ca", "+"), ("Ca", "2−"), ("Cl", "−")]},
    {"no": 6, "soru": "<sub>10</sub>Ne ile <sub>11</sub>Na’dan hangisi iyon oluşturmaz?", "cevap": ("Ne · soy gaz", ""), "tur": "soy", "z": 10,
     "celdirici": [("Na · metal", ""), ("Na · iyon", ""), ("Ne · iyon", "")]},
]
DENEME = {"cevap": ("TAMAM", ""), "celdirici": [("HATA", ""), ("BAKMA", ""), ("DUR", "")]}
KUTU = (72.0, 15.0)          # mm
KUTU_DENEME = (40.0, 9.0)


# ------------------------------------------------------------------ renk dönüşümleri
def lin2srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def srgb2lin(x):
    return np.where(x <= 0.04045, x / 12.92, np.power((x + 0.055) / 1.055, 2.4))


def lab(rgb_lin):
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = rgb_lin @ M.T / np.array([0.95047, 1.0, 1.08883])
    fx = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    L = 116 * fx[..., 1] - 16
    a = 500 * (fx[..., 0] - fx[..., 1])
    b = 200 * (fx[..., 1] - fx[..., 2])
    return np.stack([L, a, b], -1)


def baski(m, y, c):
    """kaplama haritaları → doğrusal RGB (H×W×3)."""
    out = np.ones(m.shape + (3,))
    for t, dolu in ((m, MAG), (y, SARI), (c, CYAN)):
        out *= 1 - t[..., None] * (1 - dolu)
    return out


def ust_uste(a, b):
    return 1 - (1 - a) * (1 - b)


# ------------------------------------------------------------------ çizim
def _yazi_maskesi(boyut, metin, ust, yukseklik_mm, font=BALOO):
    W, H = boyut
    for em in np.arange(yukseklik_mm, 2.0, -0.1):
        fnt = ImageFont.truetype(font, int(em * MM))
        fk = ImageFont.truetype(font, int(em * MM * .62))
        w = fnt.getlength(metin) + (fk.getlength(ust) + .05 * em * MM if ust else 0)
        if w <= W * 0.86:
            break
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    x0 = (W - w) / 2
    taban = H / 2 + .602 * em * MM / 2           # büyük harf yüksekliğini ortala
    d.text((x0, taban), metin, fill=255, font=fnt, anchor="ls")
    if ust:
        d.text((x0 + fnt.getlength(metin) + .05 * em * MM, taban - .42 * em * MM), ust, fill=255, font=fk, anchor="ls")
    return np.asarray(im).astype(np.float64) / 255


def _gurultu(boyut, rng, em_mm):
    """M ve Y kaplama haritaları: taban + sahte harfler + kıvrımlar."""
    W, H = boyut
    m = np.full((H, W), TABAN[0])
    y = np.full((H, W), TABAN[1])
    renk_listesi = [r for r in RENKLER for _ in range(r[2])]
    alan = W * H / MM ** 2
    n_harf = int(alan * 0.62)
    for _ in range(n_harf):
        dm, dy, _w = rng.choice(renk_listesi)
        boy = em_mm * rng.uniform(.55, 1.15)
        fnt = ImageFont.truetype(BALOO if rng.random() < .75 else NUNITO, max(8, int(boy * MM)))
        harf = rng.choice(HARFLER)
        g = Image.new("L", (int(boy * MM * 1.6), int(boy * MM * 1.8)), 0)
        ImageDraw.Draw(g).text((g.width / 2, g.height / 2), harf, fill=255, font=fnt, anchor="mm")
        g = g.rotate(rng.uniform(-35, 35), resample=Image.BICUBIC, expand=True)
        x = int(rng.uniform(-g.width / 2, W - g.width / 2))
        yy = int(rng.uniform(-g.height / 2, H - g.height / 2))
        a = np.zeros((H, W))
        tuval = Image.new("L", (W, H), 0)
        tuval.paste(g, (x, yy))
        a = np.asarray(tuval).astype(np.float64) / 255
        m = ust_uste(m, dm * a)
        y = ust_uste(y, dy * a)
    # kıvrımlar (harf kalınlığında)
    for _ in range(int(alan * 0.05) + 3):
        dm, dy, _w = rng.choice(renk_listesi)
        tuval = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(tuval)
        x, yy = rng.uniform(0, W), rng.uniform(0, H)
        aci = rng.uniform(0, 2 * math.pi)
        noktalar = []
        for _k in range(14):
            aci += rng.uniform(-.8, .8)
            x += math.cos(aci) * em_mm * .45 * MM
            yy += math.sin(aci) * em_mm * .45 * MM
            noktalar.append((x, yy))
        d.line(noktalar, fill=255, width=max(2, int(em_mm * .16 * MM)), joint="curve")
        a = np.asarray(tuval).astype(np.float64) / 255
        m = ust_uste(m, dm * a)
        y = ust_uste(y, dy * a)
    return m, y


def _kaydir(T, dx, dy, aci):
    im = Image.fromarray((T * 255).astype(np.uint8)).rotate(aci, resample=Image.BICUBIC, translate=(dx, dy))
    return np.asarray(im).astype(np.float64) / 255


WL = np.array([0.2126, 0.7152, 0.0722])


def _parlaklik(m, y, c):
    return (baski(m, y, c) * WL).sum(-1)


def _katmanlar(cevap, celdirici, boyut_mm, tohum):
    """gürültü (M, Y), gerçek yazı maskesi T ve çeldirici maskeleri D."""
    W, H = int(round(boyut_mm[0] * MM)), int(round(boyut_mm[1] * MM))
    rng = random.Random(tohum)
    em = boyut_mm[1] * .62
    T = _yazi_maskesi((W, H), *cevap, em)
    m, y = _gurultu((W, H), rng, em * .8)
    renk = list(CELDIRICI_RENK)
    rng.shuffle(renk)
    D = []
    for i, (metin, ust) in enumerate(celdirici):
        a = _kaydir(_yazi_maskesi((W, H), metin, ust, em), rng.uniform(-.13, .13) * em * MM, rng.uniform(-.09, .09) * em * MM, rng.uniform(-3, 3))
        dm, dy = renk[i % len(renk)]
        m, y = ust_uste(m, dm * a), ust_uste(y, dy * a)
        D.append(a)
    return m, y, T, D


def _esle(m, y, T, c_yazi, pay_m, guc):
    """parlaklık eşleme: gerçek yazının altında M ve Y azaltılır (pay_m: düzeltmenin M payı, guc: oranı); R kanalı neredeyse değişmez."""
    c = c_yazi * T
    hedef = _parlaklik(m, y, np.zeros_like(m))
    yazi = T > .01
    for _ in range(4):
        for kanal, pay in (("m", pay_m), ("y", 1 - pay_m)):
            if pay <= 0:
                continue
            l0 = _parlaklik(m, y, c)
            fark = guc * pay * (hedef - l0)
            if kanal == "m":
                d1 = (_parlaklik(np.clip(m - 1e-3, 0, 1), y, c) - l0) / 1e-3
                m = np.clip(m - fark / np.maximum(d1, 1e-6) * yazi, 0, 1)
            else:
                d1 = (_parlaklik(m, np.clip(y - 1e-3, 0, 1), c) - l0) / 1e-3
                y = np.clip(y - fark / np.maximum(d1, 1e-6) * yazi, 0, 1)
    return (lin2srgb(baski(m, y, c)) * 255 + .5).astype(np.uint8)


ESLEME_IZGARA = [(pm, g) for pm in (1.0, .5, 0.0) for g in (1.0, .7, .4, 0.0)]


def kutu(cevap, celdirici, boyut_mm=KUTU, tohum=1, c_yazi=C_YAZI):
    """→ (sRGB uint8 resim, T, D, seçilen eşleme). Eşleme, çıplak gözdeki en büyük oranı en küçük yapan (M payı, güç) çiftidir."""
    m, y, T, D = _katmanlar(cevap, celdirici, boyut_mm, tohum)
    en_iyi = None
    for pm, g in ESLEME_IZGARA:
        img = _esle(m, y, T, c_yazi, pm, g)
        o = olc(srgb2lin(img.astype(np.float64) / 255), T, D)
        puan = o["goz_oran_enbuyuk"] if o["cam_weber"] >= ESIK["cam_weber"] else 99
        if en_iyi is None or puan < en_iyi[0]:
            en_iyi = (puan, img, (pm, g))
    return en_iyi[1], T, D, en_iyi[2]


# ------------------------------------------------------------------ ölçüm
def _karsitlik(V, maske, zemin):
    return abs(V[maske].mean() - V[zemin].mean()) / (V[zemin].std() + 1e-9)


def olc(rgb_lin, T, D):
    """rgb_lin: basılan resmin doğrusal RGB'si; T: gerçek yazı maskesi; D: çeldirici maskeleri."""
    hepsi = [T] + list(D)
    zemin = np.all([h < .02 for h in hepsi], 0)
    tek = []
    for i, h in enumerate(hepsi):
        obur = [g for j, g in enumerate(hepsi) if j != i]
        tek.append((h > .6) & np.all([g < .1 for g in obur], 0))
    kanallar = {"R": rgb_lin[..., 0]}
    L = lab(rgb_lin)
    kanallar.update({"L": L[..., 0], "a": L[..., 1], "b": L[..., 2]})
    k = {ad: [round(float(_karsitlik(V, t, zemin)), 2) for t in tek] for ad, V in kanallar.items()}
    R = kanallar["R"]
    o = {"cam": k["R"][0], "cam_oran": round(k["R"][0] / max(k["R"][1:]), 1),
         "cam_weber": round(float((R[zemin].mean() - R[tek[0]].mean()) / R[zemin].mean()), 3),
         "goz_oran": {ad: round(k[ad][0] / max(k[ad][1:]), 2) for ad in ("L", "a", "b")}, "karsitlik": k,
         "piksel": [int(t.sum()) for t in tek] + [int(zemin.sum())]}
    o["goz_oran_enbuyuk"] = max(o["goz_oran"].values())
    return o


def gecti(o):
    return (o["cam"] >= ESIK["cam"] and o["cam_oran"] >= ESIK["cam_oran"] and o["cam_weber"] >= ESIK["cam_weber"]
            and o["goz_oran_enbuyuk"] <= ESIK["goz_oran"])


# ------------------------------------------------------------------ kurulum
def _kaydet(ad, img, T, D):
    Image.fromarray(img).save(os.path.join(GORSEL, f"gizli-{ad}.png"), dpi=(DPI, DPI), optimize=True)
    np.savez_compressed(os.path.join(GORSEL, f"gizli-{ad}-maske.npz"), T=(T * 255).astype(np.uint8),
                        D=np.stack([(d * 255).astype(np.uint8) for d in D]))
    return olc(srgb2lin(img.astype(np.float64) / 255), T, D)


def _uret(ad, cevap, celdirici, boyut, tohum0):
    """tohum taraması: eşiği geçen ilk tohum (en çok 4 deneme); hiçbiri geçmezse en iyisi."""
    en_iyi = None
    for k in range(4):
        tohum = tohum0 + 1000 * k
        img, T, D, es = kutu(cevap, celdirici, boyut, tohum)
        o = olc(srgb2lin(img.astype(np.float64) / 255), T, D)
        if en_iyi is None or o["goz_oran_enbuyuk"] < en_iyi[0]["goz_oran_enbuyuk"]:
            en_iyi = (o, img, T, D, es, tohum)
        if gecti(o):
            break
    o, img, T, D, es, tohum = en_iyi
    return dict(_kaydet(ad, img, T, D), esleme={"M_payi": es[0], "guc": es[1]}, tohum=tohum)


def hazirla(zorla=False):
    os.makedirs(GORSEL, exist_ok=True)
    json_yol = os.path.join(GORSEL, "gizli-olcum.json")
    adlar = [str(s["no"]) for s in SORULAR] + ["deneme"]
    if not zorla and os.path.exists(json_yol) and all(os.path.exists(os.path.join(GORSEL, f"gizli-{a}.png")) for a in adlar) \
            and os.path.getmtime(json_yol) > os.path.getmtime(__file__):
        with open(json_yol, encoding="utf-8") as fp:
            return json.load(fp)
    olcum = {}
    for s in SORULAR:
        olcum[str(s["no"])] = _uret(str(s["no"]), s["cevap"], s["celdirici"], KUTU, 100 + s["no"])
    olcum["deneme"] = _uret("deneme", DENEME["cevap"], DENEME["celdirici"], KUTU_DENEME, 7)
    with open(json_yol, "w", encoding="utf-8") as fp:
        json.dump(olcum, fp, ensure_ascii=False, indent=1)
    kotu = [k for k, v in olcum.items() if not gecti(v)]
    print(f"gizli: {len(olcum)} kutu · camla karşıtlık en az {min(v['cam'] for v in olcum.values())}, "
          f"çeldiriciye oranı en az {min(v['cam_oran'] for v in olcum.values())} · çıplak gözle oran en çok "
          f"{max(v['goz_oran_enbuyuk'] for v in olcum.values())} · eşik dışı: {kotu or 'yok'}")
    return olcum


def yer_tutucu(no):
    if no == "deneme":
        return f'<img src="gorsel/gizli-deneme.png" alt="deneme şeridi (kırmızı camla okunur)">'
    return f'<img src="gorsel/gizli-{no}.png" alt="gizli cevap {no} (kırmızı camla okunur)">'


def sema():
    """Nasıl çalışır? Kırmızı ışık üç mürekkebe çarpar; kırmızı camdan bakan göz ne görür?"""
    KIR, CAM, MAC, SAR, OBS = "#E0332E", "#3FC1E3", "#E0338C", "#F7D21E", "#1B1D26"
    o = ['<svg viewBox="0 0 480 200" xmlns="http://www.w3.org/2000/svg" data-tema-sabit>']
    for i, (renk, ad, sonuc) in enumerate(((MAC, "macenta", "açık"), (SAR, "sarı", "açık"), (CAM, "camgöbeği", "koyu"))):
        x = 10 + i * 160
        o.append(f'<rect x="{x}" y="132" width="140" height="30" rx="6" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>')
        o.append(f'<text x="{x + 70}" y="153.5" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="21" fill="{OBS}">{ad}</text>')
        o.append(f'<path d="M{x + 18} 30 L{x + 50} 128" stroke="{KIR}" stroke-width="6" stroke-linecap="round"/>')
        if i < 2:
            o.append(f'<path d="M{x + 88} 128 L{x + 112} 62" stroke="{KIR}" stroke-width="6" stroke-linecap="round"/>'
                     f'<path d="M{x + 103} 66 L{x + 115} 48 L{x + 123} 70 Z" fill="{KIR}"/>')
        else:
            o.append(f'<path d="M{x + 80} 96 l20 20 M{x + 100} 96 l-20 20" stroke="{OBS}" stroke-width="5" stroke-linecap="round"/>')
        o.append(f'<rect x="{x + 92}" y="14" width="44" height="26" rx="7" fill="{KIR}" opacity=".88" stroke="{OBS}" stroke-width="2.4"/>')
        zem = "#FFFFFF" if i < 2 else "#3A2A2A"
        o.append(f'<rect x="{x + 24}" y="172" width="92" height="24" rx="12" fill="{zem}" stroke="{OBS}" stroke-width="2"/>'
                 f'<text x="{x + 70}" y="190" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="18" '
                 f'fill="{"#1B1D26" if i < 2 else "#FFFFFF"}">{sonuc}</text>')
    o.append('<text x="10" y="22" font-family="Nunito" font-weight="900" font-size="17" fill="#A12817">kırmızı ışık</text>')
    o.append('</svg>')
    return "".join(o)


# ------------------------------------------------------------------ önizleme (basılacak PDF'ten)
def onizleme(pdf, hedef):
    import onizle as O
    img = O.sayfa_raster(pdf, 3, 150)
    a = np.asarray(img).astype(np.float64) / 255
    R = a[..., 0]
    cam = (np.stack([R, R, R], -1) * 255).astype(np.uint8)
    kirmizi = np.stack([R, R * .12, R * .1], -1)
    once, sonra = img, Image.fromarray(cam)
    h = 1400
    w = int(img.width * h / img.height)
    birlesik = Image.new("RGB", (2 * w + 24, h + 70), (255, 255, 255))
    birlesik.paste(once.resize((w, h), Image.LANCZOS), (0, 70))
    birlesik.paste(sonra.resize((w, h), Image.LANCZOS), (w + 24, 70))
    d = ImageDraw.Draw(birlesik)
    fnt = ImageFont.truetype(os.path.join(FONT, "nunito", "static", "Nunito-900.ttf"), 34)
    d.text((w // 2, 16), "Çıplak gözle", fill=(27, 29, 38), font=fnt, anchor="ma")
    d.text((w + 24 + w // 2, 16), "Kırmızı camla (R kanalı, gri)", fill=(161, 40, 23), font=fnt, anchor="ma")
    birlesik.save(os.path.join(hedef, "gizli-once-sonra.png"), optimize=True)
    # yakın plan: ilk iki kutu, iki görünüm
    # mercek GIF'i: kırmızı cam sayfanın üstünde gezinir
    kucuk = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
    k = np.asarray(kucuk).astype(np.float64) / 255
    kr = (np.stack([k[..., 0], k[..., 0] * .12, k[..., 0] * .1], -1) * 255).astype(np.uint8)
    H_, W_ = k.shape[:2]
    kareler = []
    yol = [(W_ * .3, H_ * .38), (W_ * .7, H_ * .38), (W_ * .7, H_ * .52), (W_ * .3, H_ * .52), (W_ * .3, H_ * .66), (W_ * .7, H_ * .66)]
    for i in range(len(yol) - 1):
        for t in np.linspace(0, 1, 5, endpoint=False):
            cx = yol[i][0] + (yol[i + 1][0] - yol[i][0]) * t
            cy = yol[i][1] + (yol[i + 1][1] - yol[i][1]) * t
            m = Image.new("L", (W_, H_), 0)
            ImageDraw.Draw(m).rounded_rectangle((cx - 150, cy - 70, cx + 150, cy + 70), 30, fill=255)
            kare = Image.composite(Image.fromarray(kr), kucuk, m)
            ImageDraw.Draw(kare).rounded_rectangle((cx - 150, cy - 70, cx + 150, cy + 70), 30, outline=(27, 29, 38), width=5)
            kareler.append(kare.crop((0, int(H_ * .25), W_, int(H_ * .8))).resize((520, int(520 * H_ * .55 / W_)), Image.LANCZOS).quantize(128))
    kareler[0].save(os.path.join(hedef, "gizli-mercek.gif"), save_all=True, append_images=kareler[1:], duration=220, loop=0, optimize=True)
    print("gizli: önce/sonra PNG ve mercek GIF'i yazıldı")
