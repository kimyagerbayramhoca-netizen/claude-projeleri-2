"""Karma örnek · 10. sınıf Gazlar sayfalarının bilgi grafikleri ({{info|ad}} → fn(önek)). Karakterler: konu_karakterleri (kk-gaz-*).

  pistonlu_kap      Boyle (T sabit: V yarı → P 2 kat) ve Charles (P sabit: T 2 kat → V 2 kat) tanecik sahnesi
  gp_jtup … gp_sonuc   "Balonun kısa tarihi" çizgi romanı (1662 Boyle J-borusu · 1783 Charles'ın hidrojen balonu · 1787/1802)
  kinetik_kutular   200 K · 300 K · 600 K: uykulu–yavaş / canlı–hızlı tanecikler, duvar çarpışması kıvılcımları
  tunel_yarisi      Derinkuyu tünellerinde He · CH₄ · O₂ · SO₂ yarışı: aynı sürede yol ∝ 1/√M
Bütün sayılar dogrula.py'de yeniden hesaplanır. SVG yazısında kontur yok; alt simgeler tspan.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, acik, koyu, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ALTIN, ALTIN_K, GUM_K, ZUMRUT)
import konu_karakterleri as KK
from infografik_gelistirme import _ok, _egri_ok, _hiz, _alt, _carp

T = 'font-family="Nunito" font-weight="800"'
T9 = 'font-family="Nunito" font-weight="900"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'
W_P, H_P = 592, 520                     # pano: 59,2 × 52 mm

# Graham yarışı: aynı sürede alınan yol ∝ 1/√M (SO₂ = 10 m)
YARIS = [("he", "He", 4), ("ch4", "CH₄", 16), ("o2", "O₂", 32), ("so2", "SO₂", 64)]
# kinetik kutular: mutlak sıcaklıklar (K)
KUTU_T = (200, 300, 600)


def yol_m(M, ref_M=64, ref_yol=10):
    return ref_yol * math.sqrt(ref_M / M)


def _kivilcim(x, y, r=12, renk=KEH):
    """Duvar çarpışması kıvılcımı (basıncın tanecik karşılığı)."""
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        rr = r if i % 2 == 0 else r * .42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return f'<path d="{cizgi_d(pts, True)}" fill="{renk}" stroke="{OBS}" stroke-width="{f(max(1.2, r * .14))}" stroke-linejoin="round"/>'


def _iz(x, y, aci, uz, renk="#9FB2BC", k=4):
    """Hareket izi: taneciğin arkasında üç çizgi (aci: hareket yönü, derece)."""
    a = math.radians(aci)
    o = []
    for j, d in enumerate((-9, 0, 9)):
        px, py = x - d * math.sin(a), y + d * math.cos(a)
        L = uz * (1 - .18 * abs(j - 1))
        o.append(f'<path d="M{f(px - 22 * math.cos(a))} {f(py - 22 * math.sin(a))} l{f(-L * math.cos(a))} {f(-L * math.sin(a))}" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"/>')
    return "".join(o)


def _termometre(x, y, h, doluluk, renk=MER):
    return (f'<rect x="{f(x - 7)}" y="{f(y)}" width="14" height="{f(h)}" rx="7" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.4"/>'
            f'<rect x="{f(x - 3.4)}" y="{f(y + h * (1 - doluluk))}" width="6.8" height="{f(h * doluluk)}" rx="3.4" fill="{renk}"/>'
            f'<circle cx="{f(x)}" cy="{f(y + h + 9)}" r="12" fill="{renk}" stroke="{OBS}" stroke-width="2.4"/>')


# ------------------------------------------------------------------ (a) pistonlu kap: Boyle ve Charles

def _silindir(s, x, w, y_ust, y_alt, piston_y, agirlik=False, alev=False):
    g = s.lin([(0, "#EAF4FA"), (.5, "#FFFFFF"), (1, "#DCEBF3")], x, 0, x + w, 0, kull="userSpaceOnUse", ad="cam")
    o = [f'<path d="M{x} {y_ust} V{y_alt - 14} Q{x} {y_alt} {x + 14} {y_alt} H{x + w - 14} Q{x + w} {y_alt} {x + w} {y_alt - 14} V{y_ust}" fill="{g}" stroke="{OBS}" stroke-width="3.4"/>']
    o.append(f'<rect x="{x + 4}" y="{f(piston_y - 16)}" width="{w - 8}" height="16" rx="3" fill="#8E9CA8" stroke="{OBS}" stroke-width="2.4"/>')
    o.append(f'<rect x="{x + w / 2 - 6}" y="{f(piston_y - 70)}" width="12" height="54" fill="#B9C5CE" stroke="{OBS}" stroke-width="2.2"/>')
    if agirlik:
        o.append(f'<path d="M{x + w / 2 - 34} {f(piston_y - 70)} L{x + w / 2 - 24} {f(piston_y - 100)} H{x + w / 2 + 24} L{x + w / 2 + 34} {f(piston_y - 70)} Z" fill="#5E6672" stroke="{OBS}" stroke-width="2.4"/>')
    if alev:
        for k, (dx, h) in enumerate(((-30, 34), (0, 46), (30, 34))):
            cx = x + w / 2 + dx
            o.append(f'<path d="M{cx} {y_alt + 8} q-12 {-h * .45} 0 {-h} q12 {h * .55} 0 {h} Z" fill="{["#FFB21A", "#FF6A1A", "#FFB21A"][k]}" stroke="{OBS}" stroke-width="1.6" '
                     f'transform="translate(0 {h + 14})"/>')
    return "".join(o)


def _tanecikler(x, w, y_ust, y_alt, tur, n=6, tohum=1, olcek=46):
    """Silindirin içine n tanecik (N₂, O₂ karışık) — aynı tohum: aynı dizilim, yalnız ölçeklenir."""
    r = RNG(tohum)
    o = []
    for k in range(n):
        u, v = (k % 3 + .5) / 3 + r.uniform(-.08, .08), (k // 3 + .5) / 2 + r.uniform(-.1, .1)
        px, py = x + 18 + u * (w - 36), y_ust + 10 + v * (y_alt - y_ust - 20)
        kim = "kk-gaz-o2" if k in (1, 4) else "kk-gaz-n2"
        o.append(KK.kullan(kim + (f"-{tur}" if tur else ""), px - olcek / 2, py - olcek * .35, olcek))
    return "".join(o)


def pistonlu_kap(onek="gk-pk"):
    s = Svg(onek)
    W, H = 1820, 470
    y_ust, y_alt, w = 96, 396, 300
    tam, yari = 150, 273                     # gaz sütunu: V = 246 birim · V/2 = 123 birim
    kutular = [  # (x, piston_y, tur, başlık, alt yazı, ağırlık, alev, V etiketi)
        (30, tam, "", "Boyle · başta", "P = 1 atm", False, False, "V"),
        (400, yari, "sasiran", "Piston bastırıldı (T sabit)", "P = 2 atm", False, False, "V/2"),
        (1080, yari, "soguk", "Charles · 300 K", "P sabit", True, False, "V"),
        (1450, tam, "sicak", "Isıtıldı · 600 K", "", True, True, "2V"),
    ]
    for i, (x, py, tur, bas, alt, agirlik, alev, vetk) in enumerate(kutular):
        s += f'<text x="{x + w / 2}" y="34" text-anchor="middle" {B} font-size="28" fill="{OBS}">{bas}</text>'
        s += _silindir(s, x, w, y_ust, y_alt, py, agirlik, alev)
        r = RNG(3 + i)
        for k in range(6):
            u, v = (k % 3 + .5) / 3, (k // 3 + .5) / 2
            px = x + 24 + u * (w - 48) + r.uniform(-8, 8)
            py2 = py + 8 + v * (y_alt - py - 24) + r.uniform(-6, 6)
            kim = ("kk-gaz-o2" if k in (1, 4) else "kk-gaz-n2") + (f"-{tur}" if tur and tur != "sasiran" else "")
            s += KK.kullan(kim, px - 38, py2 - 26, 76)
        if tur in ("sasiran", "sicak"):
            for (kx, ky) in ((x, py + 46), (x + w, py + 84), (x + 96, y_alt), (x + 214, y_alt), (x + w, py + 20)):
                s += _kivilcim(kx, ky, 14)
        # hacim çubuğu (sağda) ve alt yazı
        s += f'<path d="M{x + w + 16} {py} V{y_alt} M{x + w + 9} {py} H{x + w + 23} M{x + w + 9} {y_alt} H{x + w + 23}" stroke="{GOL_K}" stroke-width="3.4"/>'
        s += f'<text x="{x + w + 30}" y="{f((py + y_alt) / 2 + 10)}" {B} font-size="30" fill="{GOL_K}">{vetk}</text>'
        if alt:
            s += f'<text x="{x + w / 2}" y="{y_alt + 40}" text-anchor="middle" {T9} font-size="24" fill="{KOB_K}">{alt}</text>'
    for y0, bas, alt in ((150, "P · V sabit", "n, T sabit · Boyle"), (290, "V / T sabit", "n, P sabit · Charles")):
        s += f'<rect x="790" y="{y0}" width="250" height="104" rx="18" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.6"/>'
        s += f'<text x="915" y="{y0 + 46}" text-anchor="middle" {B} font-size="31" fill="{OBS}">{bas}</text>'
        s += f'<text x="915" y="{y0 + 82}" text-anchor="middle" {T} font-size="21" fill="{GUM_K}">{alt}</text>'
    s += _ok(748, 202, 786, 202, OBS, 3.4, 14) + _ok(1044, 342, 1074, 342, OBS, 3.4, 14)
    return s.cikti(f"0 0 {W} {H}", cls="info piston")


# ------------------------------------------------------------------ (a) çizgi roman: balonun kısa tarihi

def _zemin(s, ust="#F3F8FB", alt="#DCE8EF"):
    g = s.lin([(0, ust), (1, alt)], 0, 0, 0, H_P, kull="userSpaceOnUse", ad="pz")
    return f'<rect width="{W_P}" height="{H_P}" fill="{g}"/>'


def _j_boru(s, x0, cam_ust_sol, cam_ust_sag, civa_sol, civa_sag, kapali_ust, alt=470):
    """J borusu: sol uzun kol açık, sağ kısa kol kapalı. civa_*: cıva yüzeyinin y'si; sağ kolda kapalı uçla cıva arası hava."""
    xl, xr, w = x0, x0 + 150, 46
    gc = s.lin([(0, "#E8EEF2"), (.5, "#C2CCD4"), (1, "#8E9CA8")], 0, 0, 1, 0, ad="cv")
    o = []
    # cıva: U kıvrımı + iki koldaki sütun
    o.append(f'<path d="M{xl} {civa_sol} V{alt} A75 75 0 0 0 {xr + w} {alt} V{civa_sag} H{xr} V{alt} A29 29 0 0 1 {xl + w} {alt} V{civa_sol} Z" fill="{gc}"/>')
    # hava sütunu (sağ kol, kapalı uç ile cıva arası)
    o.append(f'<rect x="{xr + 3}" y="{kapali_ust + 3}" width="{w - 6}" height="{civa_sag - kapali_ust - 3}" fill="#EAF7FF"/>')
    # cam
    o.append(f'<path d="M{xl} {cam_ust_sol} V{alt} A75 75 0 0 0 {xr + w} {alt} V{kapali_ust} A23 23 0 0 0 {xr} {kapali_ust} V{alt} A29 29 0 0 1 {xl + w} {alt} V{cam_ust_sol}" '
             f'fill="none" stroke="{OBS}" stroke-width="3.6" stroke-linejoin="round"/>')
    o.append(f'<path d="M{xl + 10} {cam_ust_sol + 10} V{alt - 20}" stroke="#FFFFFF" stroke-width="4" opacity=".8"/>')
    return "".join(o), (xr, w)


def gp_jtup(onek="gk-p1"):
    s = Svg(onek)
    s += _zemin(s)
    s += f'<rect x="0" y="470" width="{W_P}" height="50" fill="#C9D6DE"/>'
    j, (xr, w) = _j_boru(s, 210, 140, 0, 420, 420, 270, 430)
    s += j
    s += KK.kullan("kk-gaz-n2", xr - 2, 300, 50) + KK.kullan("kk-gaz-o2", xr - 2, 352, 50)
    # cıva dökülen şişe
    s += f'<path d="M108 128 L176 150 L168 176 L100 156 Z" fill="#DCE8EF" stroke="{OBS}" stroke-width="2.6"/><path d="M176 150 L196 136 L204 156 L168 176" fill="#C2CCD4" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M204 150 Q214 170 216 200 V410" stroke="#9FAAB4" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def gp_olcum(onek="gk-p2"):
    s = Svg(onek)
    s += _zemin(s)
    s += f'<rect x="0" y="470" width="{W_P}" height="50" fill="#C9D6DE"/>'
    # önce · sonra
    j1, (xr1, w) = _j_boru(s, 40, 170, 0, 420, 420, 280, 430)
    s += j1 + KK.kullan("kk-gaz-n2", xr1 - 2, 312, 48) + KK.kullan("kk-gaz-o2", xr1 - 2, 362, 48)
    j2, (xr2, w) = _j_boru(s, 330, 150, 0, 210, 350, 280, 430)
    s += j2 + KK.kullan("kk-gaz-n2-sasiran" if False else "kk-gaz-n2", xr2 - 2, 286, 46) + KK.kullan("kk-gaz-o2", xr2 + 2, 316, 40)
    # ölçüler
    s += f'<path d="M{xr1 + w + 12} 280 V420 M{xr1 + w + 6} 280 H{xr1 + w + 18} M{xr1 + w + 6} 420 H{xr1 + w + 18}" stroke="{GOL_K}" stroke-width="3"/>'
    s += f'<text x="{xr1 + w + 24}" y="358" {B} font-size="30" fill="{GOL_K}">V</text>'
    s += f'<path d="M{xr2 + w + 12} 280 V350 M{xr2 + w + 6} 280 H{xr2 + w + 18} M{xr2 + w + 6} 350 H{xr2 + w + 18}" stroke="{GOL_K}" stroke-width="3"/>'
    s += f'<text x="{xr2 + w + 22}" y="326" {B} font-size="28" fill="{GOL_K}">V/2</text>'
    s += f'<path d="M{330 - 14} 210 V350 M{330 - 20} 210 H{330 - 8} M{330 - 20} 350 H{330 - 8}" stroke="{MER_K}" stroke-width="3"/>'
    s += _ok(250, 300, 300, 300, OBS, 4, 15)
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def _charliere(s, cx, cy, r, tohum=0, kesit=True):
    """Hidrojen balonu (temsilî): ipek küre, üst yarıda ağ, ipler, kayık biçimli sepet; kesit penceresinde H₂."""
    g = s.rad([(0, "#FFE7A8"), (.55, "#F0A21A"), (1, "#B9751A")], .38, .32, .8, ad="ch")
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{g}" stroke="{OBS}" stroke-width="3"/>']
    for k in range(-3, 4):          # dilimler
        rx = abs(k) * r / 3.6
        o.append(f'<path d="M{cx} {cy - r} Q{f(cx + k * r / 2.6)} {cy} {cx} {cy + r}" fill="none" stroke="#B5523E" stroke-width="2.2" opacity=".75"/>')
    for k in range(1, 4):           # ağ
        yy = cy - r + k * r * .32
        half = math.sqrt(max(0, r * r - (yy - cy) ** 2))
        o.append(f'<path d="M{f(cx - half)} {f(yy)} Q{cx} {f(yy + 12)} {f(cx + half)} {f(yy)}" fill="none" stroke="{OBS}" stroke-width="1.6" opacity=".6"/>')
    sy = cy + r + 62
    for dx in (-r * .7, -r * .25, r * .25, r * .7):
        o.append(f'<path d="M{f(cx + dx)} {f(cy + math.sqrt(max(0, r * r - dx * dx)) - 4)} L{f(cx + dx * .45)} {sy}" stroke="{OBS}" stroke-width="1.8"/>')
    o.append(f'<path d="M{cx - 54} {sy} H{cx + 54} Q{cx + 46} {sy + 26} {cx + 30} {sy + 28} H{cx - 30} Q{cx - 46} {sy + 26} {cx - 54} {sy} Z" fill="#2B50B5" stroke="{OBS}" stroke-width="2.6"/>')
    o.append(f'<path d="M{cx - 46} {sy + 8} H{cx + 46}" stroke="{ALTIN}" stroke-width="3"/>')
    for dx in (-18, 16):            # iki genel figür (yüzsüz siluet)
        o.append(f'<circle cx="{cx + dx}" cy="{sy - 10}" r="9" fill="#3A3F4B" stroke="{OBS}" stroke-width="1.6"/>')
    if kesit:
        o.append(f'<circle cx="{cx}" cy="{cy + 6}" r="{f(r * .5)}" fill="#FFF8E6" stroke="{OBS}" stroke-width="2" stroke-dasharray="6 5"/>')
        o.append(KK.kullan("kk-gaz-h2", cx - r * .42, cy - r * .2, r * .48) + KK.kullan("kk-gaz-h2", cx - r * .05, cy + r * .1, r * .44))
    return "".join(o)


def gp_kalkis(onek="gk-p3"):
    s = Svg(onek)
    s += _zemin(s, "#CFE8F7", "#F3E9D6")
    s += f'<rect x="0" y="440" width="{W_P}" height="80" fill="#9CC17A"/>'
    for x in (40, 130, 470, 560):     # bahçe ağaçları
        s += f'<circle cx="{x}" cy="420" r="38" fill="#5E9A4E" stroke="{OBS}" stroke-width="2"/><rect x="{x - 5}" y="440" width="10" height="26" fill="#7A5232"/>'
    r = RNG(8)
    for k in range(26):               # kalabalık
        x, y = 20 + k * 22 + r.uniform(-4, 4), 478 + r.uniform(-6, 8)
        s += f'<circle cx="{f(x)}" cy="{f(y - 16)}" r="8" fill="#4E5A73"/><path d="M{f(x - 10)} {f(y + 12)} Q{f(x)} {f(y - 10)} {f(x + 10)} {f(y + 12)} Z" fill="#6B7894"/>'
    s += _charliere(s, 300, 268, 78)
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def gp_ucus(onek="gk-p4"):
    s = Svg(onek)
    s += _zemin(s, "#BFE0F5", "#EEF6FA")
    for k, (y, renk) in enumerate(((420, "#B9D28C"), (452, "#D8C27A"), (484, "#A8C67E"))):
        s += f'<path d="M0 {y} Q150 {y - 18} 300 {y} T600 {y} V520 H0 Z" fill="{renk}"/>'
    s += f'<path d="M60 470 C200 380 330 300 420 220" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="14 10"/>'
    s += _charliere(s, 410, 236, 58, kesit=False)
    # düşen kum torbası
    s += f'<path d="M318 392 q-14 -4 -10 -18 q4 -10 16 -8 q12 2 12 14 q-2 14 -18 12 Z" fill="#B98A3E" stroke="{OBS}" stroke-width="2"/>'
    s += f'<path d="M318 408 v14 M310 412 v10 M326 412 v10" stroke="{GUM_K}" stroke-width="2" stroke-linecap="round"/>'
    s += f'<path d="M560 420 V200 M552 200 H568 M552 420 H568" stroke="{OBS}" stroke-width="3"/>'
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def _kab(s, x, y, su_renk, buz=False, buhar=False, balon_r=30, tur=""):
    """Ağzına balon geçirilmiş şişe, su banyosunda."""
    o = [f'<rect x="{x - 120}" y="{y - 40}" width="240" height="150" rx="16" fill="{su_renk}" stroke="{OBS}" stroke-width="2.6" opacity=".9"/>']
    o.append(f'<path d="M{x - 18} {y - 150} V{y - 100} L{x - 60} {y - 20} Q{x - 66} {y + 30} {x - 30} {y + 40} H{x + 30} Q{x + 66} {y + 30} {x + 60} {y - 20} L{x + 18} {y - 100} V{y - 150} Z" '
             f'fill="#F4FAFD" stroke="{OBS}" stroke-width="3"/>')
    o.append(KK.kullan("kk-gaz-n2" + (f"-{tur}" if tur else ""), x - 34, y - 34, 44) + KK.kullan("kk-gaz-o2" + (f"-{tur}" if tur else ""), x - 4, y - 6, 40))
    gb = s.rad([(0, "#FFC2B4"), (.6, MER), (1, MER_K)], .38, .32, .8, ad="bl")
    o.append(f'<ellipse cx="{x}" cy="{f(y - 150 - balon_r * .9)}" rx="{f(balon_r)}" ry="{f(balon_r * 1.1)}" fill="{gb}" stroke="{OBS}" stroke-width="2.6"/>')
    o.append(f'<rect x="{x - 20}" y="{y - 158}" width="40" height="12" rx="4" fill="{MER_K}" stroke="{OBS}" stroke-width="2"/>')
    if buz:
        for dx, dy in ((-90, 0), (80, 20), (-70, 50)):
            o.append(f'<rect x="{x + dx}" y="{y + dy}" width="26" height="22" rx="5" fill="#FFFFFF" stroke="#5B8FD6" stroke-width="2" transform="rotate(12 {x + dx} {y + dy})"/>')
    if buhar:
        for dx in (-80, 70, 96):
            o.append(f'<path d="M{x + dx} {y - 50} q-12 -18 0 -36 t0 -36" fill="none" stroke="#9FB2BC" stroke-width="4" stroke-linecap="round"/>')
    return "".join(o)


def gp_charles(onek="gk-p5"):
    s = Svg(onek)
    s += _zemin(s, "#F7F2EA", "#EEE2CF")
    s += _kab(s, 160, 412, "#BFE2F5", buz=True, balon_r=30, tur="soguk")
    s += _kab(s, 440, 412, "#F6C9B8", buhar=True, balon_r=54, tur="sicak")
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def gp_sonuc(onek="gk-p6"):
    import importlib
    S = importlib.import_module("sahneler_karma")
    s = Svg(onek)
    s += S.GAZ_SAHNE.balon(s, 296, 150, 70, tohum=3, alev=True)
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


# ------------------------------------------------------------------ (b) kinetik kutular

def kinetik_kutular(onek="gk-kk"):
    s = Svg(onek)
    W, H = 1820, 470
    turler = ("soguk", "", "sicak")
    iz_uz = {200: 30, 300: round(30 * math.sqrt(1.5)), 600: round(30 * math.sqrt(3))}      # iz uzunluğu ∝ √T
    kivilcim = {200: (2, 11), 300: (4, 15), 600: (8, 20)}
    r0 = RNG(14)
    yerler = [(.18, .3, 25), (.5, .22, 160), (.82, .34, 200), (.28, .72, -30), (.62, .68, 110), (.86, .78, 250)]
    for i, (T_, tur) in enumerate(zip(KUTU_T, turler)):
        x0 = 30 + i * 600
        w, y0, h = 560, 70, 300
        tc = T_ - 273
        s += _termometre(x0 + 22, 12, 46, (.25, .5, .92)[i], (KOB, KEH, MER)[i])
        s += f'<text x="{x0 + 44}" y="50" {B} font-size="32" fill="{OBS}">{T_} K <tspan font-size="22" fill="{GUM_K}" dx="6">({str(tc).replace("-", "−")} °C)</tspan></text>'
        g = s.lin([(0, ("#EAF3FB", "#F6FBFF", "#FFF4EC")[i]), (1, "#FFFFFF")], 0, y0, 0, y0 + h, kull="userSpaceOnUse", ad="kt")
        s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="22" fill="{g}" stroke="{OBS}" stroke-width="3.4"/>'
        n, rr = kivilcim[T_]
        duvar = [(x0, y0 + 60), (x0 + w, y0 + 200), (x0 + 180, y0 + h), (x0 + w, y0 + 80), (x0 + 380, y0), (x0, y0 + 230), (x0 + 470, y0 + h), (x0 + 90, y0)]
        for (kx, ky) in duvar[:n]:
            s += _kivilcim(kx, ky, rr)
        for k, (u, v, aci) in enumerate(yerler):
            px, py = x0 + 58 + u * (w - 116), y0 + 40 + v * (h - 80)
            kim = ("kk-gaz-o2" if k in (1, 4) else "kk-gaz-n2") + (f"-{tur}" if tur else "")
            s += _iz(px, py, aci, iz_uz[T_] * 1.5, ("#9EC4E8", "#B8C6D2", "#F2A28C")[i], 5)
            s += KK.kullan(kim, px - 46, py - 32, 92)
        ek = ("1", "1,5", "3")[i]
        hz = ("1", "1,22", "1,73")[i]
        s += f'<text x="{x0 + w / 2}" y="{y0 + h + 44}" text-anchor="middle" {T9} font-size="25" fill="{KOB_K}">ortalama E<tspan dy="6" font-size="17">k</tspan><tspan dy="-6"> ×{ek} · hız ×{hz}</tspan></text>'
    s += f'<text x="{W / 2}" y="{H - 8}" text-anchor="middle" {T} font-size="21" fill="{GUM_K}">ortalama kinetik enerji mutlak sıcaklıkla orantılı (200 K’e göre) · hız √T ile artar · kıvılcım = duvar çarpışması</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info kinetik")


# ------------------------------------------------------------------ (c) tünel yarışı

def tunel_yarisi(onek="gk-ty"):
    s = Svg(onek)
    W, H = 1820, 520
    g = s.lin([(0, "#E8C9A2"), (1, "#D4A57A")], 0, 0, 0, H, kull="userSpaceOnUse", ad="tf")
    s += f'<rect width="{W}" height="{H}" rx="20" fill="{g}"/>'
    r = RNG(31)
    for _ in range(90):
        s += f'<circle cx="{f(r.uniform(10, W - 10))}" cy="{f(r.uniform(10, H - 10))}" r="{f(r.uniform(2, 5))}" fill="#B98A62" opacity=".35"/>'
    x_bas, olcek, x_son = 250, 25, 1440      # 1 m = 25 birim
    for i, (k, ad, M) in enumerate(YARIS):
        y = 30 + i * 120
        s += f'<rect x="200" y="{y}" width="{x_son - 200}" height="104" rx="52" fill="#FFF3E0" stroke="#8E5730" stroke-width="3"/>'
        s += f'<path d="M226 {y + 92} H{x_son - 26}" stroke="#E7CFAE" stroke-width="5" stroke-linecap="round"/>'
        s += f'<text x="186" y="{y + 48}" text-anchor="end" {B} font-size="34" fill="{OBS}">{ad}</text>'
        s += f'<text x="186" y="{y + 80}" text-anchor="end" {T9} font-size="21" fill="{GUM_K}">M = {M}</text>'
        d = yol_m(M)
        x = x_bas + d * olcek
        _, _, vw, vh = (float(v) for v in KK.vb(f"kk-gaz-{k}").split())
        w = {"he": 92, "ch4": 96}.get(k, 116)
        h = w * vh / vw
        s += _hiz(x - w * .5 + 4, y + 56, 3, 26 + d * 7, 13, "#C99A78")
        s += KK.kullan(f"kk-gaz-{k}" + ("-sicak" if k == "he" else ""), x - w / 2, y + 52 - h / 2, w, h)
        yol = f"{d:.1f}".replace(".", ",").replace(",0", "")
        kat = f"{math.sqrt(64 / M):.2f}".rstrip("0").rstrip(".").replace(".", ",")
        tx = x + w / 2 + 10
        s += f'<text x="{f(tx)}" y="{y + 48}" {B} font-size="30" fill="{GOL_K}">{"≈ " if "," in yol else ""}{yol} m</text>'
        alt = ("≈ " if "," in kat else "") + f"{kat} kat hızlı" if M != 64 else "en yavaş (ölçü)"
        s += f'<text x="{f(tx)}" y="{y + 80}" {T9} font-size="21" fill="{KOB_K}">{alt}</text>'
    s += f'<path d="M{x_bas} 18 V506" stroke="{OBS}" stroke-width="3" stroke-dasharray="12 9"/>'
    s += f'<text x="{x_bas + 10}" y="{H - 4}" {T9} font-size="20" fill="{OBS}">aynı anda çıkış · aynı sürede</text>'
    s += f'<rect x="1470" y="30" width="326" height="460" rx="22" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.8"/>'
    s += f'<text x="1633" y="80" text-anchor="middle" {B} font-size="30" fill="{KOB_K}">Graham</text>'
    s += f'<text x="1633" y="126" text-anchor="middle" {T9} font-size="22" fill="{GUM_K}">aynı T ve P’de</text>'
    s += f'<text x="1633" y="186" text-anchor="middle" {B} font-size="34" fill="{OBS}">v₁ / v₂ = √(M₂ / M₁)</text>'
    s += f'<path d="M1500 214 H1766" stroke="{GUM_K}" stroke-width="2" stroke-dasharray="8 6"/>'
    s += f'<text x="1633" y="262" text-anchor="middle" {T9} font-size="22" fill="{GUM_K}">He ile SO₂:</text>'
    s += f'<text x="1633" y="318" text-anchor="middle" {B} font-size="34" fill="{OBS}">√(64 / 4) = √16</text>'
    s += f'<text x="1633" y="390" text-anchor="middle" {B} font-size="54" fill="{GOL_K}">= 4</text>'
    s += f'<text x="1633" y="440" text-anchor="middle" {T9} font-size="22" fill="{KOB_K}">He 4 kat hızlı;</text>'
    s += f'<text x="1633" y="470" text-anchor="middle" {T9} font-size="22" fill="{KOB_K}">aynı yolu ¼ sürede alır</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info tunel")
