"""Atom ve Yapısı · 3B yapı kurucuları (meta.json "uc_boyut" → cizim/uc_boyut.unite_gorselleri; Yapi döndürür).

kur_ortak 3B kurucularını sahneler_unite ve infografik_unite'de arar; infografik_unite bunları kendi ad alanına alır.
Birimler ölçeksizdir (1s yarıçapı ≈ 1); meta.json'da "mm_birim": null verilir, motor resmi kutuya sığdırır.
Anaglifte renk yok (gri tonlar); düz resimde kitabın renkleri: proton mercan, nötron gri, elektron kobalt, altın sarısı.
  orbital_s       1s ve 2s: iki küre (2s daha büyük)
  orbital_p(e)    2p_x | 2p_y | 2p_z: eksen boyunca iki lob (küre zinciri, damla profili), çekirdekte düğüm
  orbital_p_uc    üç 2p orbitali birlikte, birbirine dik (üç gri ton)
  alfa_levha      altın levhanın içi (ölçeksiz): seyrek çekirdekler, 9 alfa izi (7 düz, 1 sapan, 1 geri dönen)
  alfa_tanecik    alfa taneciği: 2 proton + 2 nötron (dörtyüzlü)
  atom_bosluk     küçücük çekirdek + nokta bulutu (1s benzeri dağılım)
"""
import math
import random

import numpy as np
from cizim.uc_boyut import Yapi

PROTON, NOTRON, ELEKTRON, ALTIN = "#E2533D", "#9AA8B6", "#2B50B5", "#D9A93A"
LOB_UZ, LOB_R, LOB_N = 2.1, .74, 16          # lob boyu, en geniş yarıçap, küre sayısı
EKSEN_UZ = 2.75
EKSEN = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
P_RENK = {"x": ("#3D7BE8", .80), "y": ("#13A3A6", .60), "z": ("#8E5BD0", .40)}   # düz renk, anaglif gri tonu


def _eksenler(y, uz=EKSEN_UZ):
    """x sağa, y yukarı, z okuyucuya: ince çubuk + uçta harfli küçük küre."""
    for ad, u in EKSEN.items():
        u = np.asarray(u, float)
        y.cubuk_ekle(-uz * u, uz * u, r=.03, gri=.45, renk="#7C8696")
        y.atom("ek", uz * u, harf=ad, r=.2, gri=.93, renk="#FFFFFF")
    y.atom("ck", (0, 0, 0), harf="", r=.08, gri=.15, renk=PROTON)        # çekirdek (nokta)


def _lob(y, u, isaret, renk, gri):
    """Eksen u boyunca, çekirdekten dışa damla biçimli lob (küre zinciri)."""
    u = np.asarray(u, float) * isaret
    for k in range(LOB_N):
        t = LOB_UZ * (k + .5) / LOB_N
        r = .05 + LOB_R * math.sin(math.pi * t / (LOB_UZ + .25)) ** .8
        y.atom("lob", t * u, harf="", r=r, gri=gri, renk=renk)


def orbital_s():
    y = Yapi("orbital_s", birim="")
    y.atom("1s", (-1.85, 0, 0), harf="1s", r=.82, gri=.74, renk="#7FA9F0")
    y.atom("2s", (1.45, 0, 0), harf="2s", r=1.32, gri=.56, renk="#3D7BE8")
    return y


def orbital_p(eksen="x"):
    y = Yapi(f"orbital_p_{eksen}", birim="")
    _eksenler(y)
    renk, gri = P_RENK[eksen]
    for isaret in (1, -1):
        _lob(y, EKSEN[eksen], isaret, renk, .62)
    return y


def orbital_p_uc():
    y = Yapi("orbital_p_uc", birim="")
    _eksenler(y)
    for ad, (renk, gri) in P_RENK.items():
        for isaret in (1, -1):
            _lob(y, EKSEN[ad], isaret, renk, gri)
    return y


# ------------------------------------------------------------------ alfa tanecikleri
BEAM = np.array([1.0, 0.0, .45]) / math.hypot(1.0, .45)      # alfa demetinin yönü (sağa ve okuyucuya doğru)
CEKIRDEKLER = [(x, yy, z) for x in (-.32, .32) for yy in (-1.8, -.6, .6, 1.8) for z in (-1.25, 0, 1.25)]
DUZ_IZ = [(-1.2, -.62), (-1.2, .62), (0, -.62), (0, .62), (1.2, -.62), (1.2, .62), (2.35, 0)]   # (y, z): çekirdeklerin arası
SAPAN = ((.32, .6, 0), .24, 35)            # çekirdek, çarpma uzaklığı (y), sapma açısı (°)
DONEN = (-.32, -.6, 1.25)                  # tam üstüne gelen alfanın çekirdeği


def _iz(y, a, b, koyu=False):
    y.cubuk_ekle(a, b, r=.055 if koyu else .042, gri=.18 if koyu else .44, renk="#C8321E" if koyu else "#E2533D")


def _alfa_top(y, p):
    y.atom("alfa", p, harf="", r=.16, gri=.28, renk=PROTON)


def alfa_levha():
    y = Yapi("alfa_levha", birim="")
    rng = random.Random(7)
    for (x, yy, z) in CEKIRDEKLER:
        y.atom("Au", (x + rng.uniform(-.06, .06), yy + rng.uniform(-.08, .08), z + rng.uniform(-.08, .08)), harf="", r=.13, gri=.22, renk=ALTIN)
    for yy, z in DUZ_IZ:                                   # çoğu: düz geçer
        o = np.array([0.0, yy, z])
        _iz(y, o - 4.0 * BEAM, o + 4.0 * BEAM)
        _alfa_top(y, o + 4.0 * BEAM)
    (cx, cy, cz), b, aci = SAPAN                           # biri: çekirdeğin yanından geçerken sapar
    c = np.array([cx, cy - b, cz])
    _iz(y, c - 4.0 * BEAM, c, True)
    a = math.radians(aci)
    d2 = np.array([BEAM[0] * math.cos(a), math.sin(a), BEAM[2]])
    d2 /= np.linalg.norm(d2)
    _iz(y, c, c + 3.4 * d2, True)
    _alfa_top(y, c + 3.4 * d2)
    n = np.array(DONEN)                                    # biri: tam üstüne gelir, geri döner
    c = n - .3 * BEAM
    _iz(y, c - 4.0 * BEAM + np.array([0, .05, 0]), c, True)
    d3 = np.array([-BEAM[0] * .95, .22, -BEAM[2] * .6])
    d3 /= np.linalg.norm(d3)
    _iz(y, c, c + 3.0 * d3, True)
    _alfa_top(y, c + 3.0 * d3)
    return y


def alfa_tanecik():
    y = Yapi("alfa_tanecik", birim="")
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    for k, p in enumerate(v):
        p = np.asarray(p, float) * .36
        if k % 2 == 0:
            y.atom("p", p, harf="p", r=.43, gri=.34, renk=PROTON)
        else:
            y.atom("n", p, harf="n", r=.43, gri=.82, renk=NOTRON)
    return y


def atom_bosluk(n=170):
    y = Yapi("atom_bosluk", birim="")
    rng = random.Random(11)
    y.atom("ck", (0, 0, 0), harf="", r=.1, gri=.18, renk=PROTON)
    k = 0
    while k < n:
        r = rng.gammavariate(3, .45)                        # 1s benzeri: r² e^(−2r) dağılımı
        if r > 2.6 or r < .35:
            continue
        u = np.array([rng.gauss(0, 1) for _ in range(3)])
        u /= np.linalg.norm(u)
        y.atom("e", r * u, harf="", r=.05, gri=.5, renk=ELEKTRON)
        k += 1
    return y
