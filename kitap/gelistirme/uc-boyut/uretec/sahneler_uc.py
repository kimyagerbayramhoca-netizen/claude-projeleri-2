"""3B örneği · sahne bantları ve küçük bilgi grafikleri (yalnız bu örnek; ortak kütüphaneye dokunmaz).

Sahneler ({{sahne|ad}}): bant_tuzgolu (9/06 · Tuz Gölü ve Hasan Dağı), bant_mardin (9/09 · Mardin), bant_atolye (gözlük sayfası),
bant_goreme (10/04 Gazlar ünitesinin doğrulanmış sahnesi, salt okunur).
Bilgi grafikleri ({{info|ad}}): duz_metan, dipol_oklari, nasil_calisir, gozluk_sablonu, ub_ikon.
Kırmızı / camgöbeği taşıyan her çizim data-tema-sabit ile işaretlidir (palet eşlemesi bu renklere dokunmaz).
"""
import importlib.util
import math
import os
import sys

from cizim.temel import Svg, f, cizgi_d, koyu, rng as RNG
from cizim import sahne as S, yapilar as Y
from cizim.renkler import OBS, KEH

W, H = 2100, 460
KIR, CAM = "#F0322D", "#1CC6DC"            # gözlük camları ve baskı renkleri (şema)
KIR_A, CAM_A = "#FFD9D5", "#CFF4F9"
GRI, GRI_K, GRI_A = "#8C95A3", "#4A5260", "#E9ECF1"
YAZI = 'font-family="Nunito" font-weight="900"'


def _bitir(s, h=H):
    return s.cikti(f"0 0 {W} {h}", cls="sahne", par="xMidYMid slice")


def _alt_golge(s, h=H):
    g = s.lin([(0, "#0E2A3A", 0), (1, "#0E2A3A", .2)], 0, h - 70, 0, h, kull="userSpaceOnUse", ad="cg")
    return f'<rect x="0" y="{h - 70}" width="{W}" height="70" fill="{g}"/>'


def gozluk(x, y, w, ic=True):
    """Kâğıt 3B gözlük (ön parça), sol üst köşe (x, y), genişlik w. ic=True: takanın gözünden (kırmızı SOLDA)."""
    k = w / 150
    sol, sag = (KIR, CAM) if ic else (CAM, KIR)
    return (f'<g data-tema-sabit transform="translate({f(x)} {f(y)}) scale({f(k, 3)})">'
            f'<path d="M6 0 H144 Q150 0 150 6 V36 Q150 42 144 42 H86 Q84 28 75 28 Q66 28 64 42 H6 Q0 42 0 36 V6 Q0 0 6 0 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<rect x="12" y="8" width="46" height="26" rx="7" fill="{sol}" stroke="{OBS}" stroke-width="2"/>'
            f'<rect x="92" y="8" width="46" height="26" rx="7" fill="{sag}" stroke="{OBS}" stroke-width="2"/>'
            f'<path d="M18 13 L30 13 M98 13 L110 13" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" opacity=".7"/></g>')


def pamuk_gozluklu(x, y, w):
    """Pamuk'un başı (pamuk-bas-gulen, viewBox 8 2 84 82) + 3B gözlük. Pamuk bize bakıyor: SOL gözü bizim sağımızda → kırmızı cam sağda."""
    k = w / 84
    return (f'<use href="#pamuk-bas-gulen" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(w * 82 / 84)}"/>'
            f'<g data-tema-sabit transform="translate({f(x - 8 * k)} {f(y - 2 * k)}) scale({f(k, 3)})">'
            f'<path d="M22 37 H78 Q81 37 81 40 V54 Q81 57 78 57 H56 Q54 51 50 51 Q46 51 44 57 H22 Q19 57 19 54 V40 Q19 37 22 37 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<rect x="23" y="40" width="21" height="13.5" rx="3.4" fill="{CAM}" opacity=".9" stroke="{OBS}" stroke-width="1.2"/>'
            f'<rect x="56" y="40" width="21" height="13.5" rx="3.4" fill="{KIR}" opacity=".9" stroke="{OBS}" stroke-width="1.2"/>'
            f'<path d="M19 43 L12 40 M81 43 L88 40" stroke="{OBS}" stroke-width="1.5" stroke-linecap="round"/></g>')


# ------------------------------------------------------------------ 9/06 · Tuz Gölü ve Hasan Dağı
def _flamingo(x, y, o=1.0, yon=1):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(o * yon, 2)} {f(o, 2)})">'
            '<path d="M5 6 V44 M13 5 V44" stroke="#D96A86" stroke-width="2.6"/>'
            '<path d="M-2 0 C-12 -16 14 -24 24 -12 C32 -3 20 8 6 8 Z" fill="#F4A3B8"/>'
            '<path d="M21 -10 C36 -30 14 -44 25 -62 C29 -70 39 -66 38 -58" fill="none" stroke="#F4A3B8" stroke-width="5.4" stroke-linecap="round"/>'
            '<path d="M38 -58 l8 6" stroke="#3A2E2E" stroke-width="4.4" stroke-linecap="round"/></g>')


def bant_tuzgolu():
    s = Svg("uc-tuz")
    ufuk = 252
    s += S.gokyuzu(s, 0, 0, W, ufuk + 4, "gun")
    s += S.gunes(s, 1975, 92, 30, hale="#FFF2C2", hale_r=300, guc=.75)
    for i, (x, y, w) in enumerate([(1350, 92, 230), (720, 70, 200), (1700, 150, 160)]):
        s += S.bulut(s, x, y, w, 60 + i, ust="#FFFFFF", alt="#D5E6F3", op=.95)
    d2, _ = S.dag(s, 1500, 2060, ufuk, 1800, 140, 72, renk="#9DB3CF", golge="#7C96BA", bicim="sivri", kar_y=170, kar="#FFFFFF",
                  kar_golge="#D3DEEE", sis="#DCEBF5", isik=1, sirt=3)
    d1, _ = S.dag(s, 1160, 1900, ufuk, 1560, 84, 71, renk="#8FA9C9", golge="#6C88B0", bicim="sivri", kar_y=142, kar="#FFFFFF",
                  kar_golge="#D3DEEE", sis="#DCEBF5", isik=1, sirt=4)
    s += d2 + d1                                            # Hasan Dağı: çift tepeli sönmüş volkan
    tb, _ = S.tepe_bandi(s, 0, W, ufuk + 6, 22, 73, "#B4C5D9", "#D8E2EC")
    s += tb
    g = s.lin([(0, "#F3D4DF"), (.16, "#FAEDF1"), (.5, "#FFFFFF"), (1, "#E4ECF5")], 0, ufuk, 0, H, kull="userSpaceOnUse", ad="tz")
    s += f'<rect x="0" y="{ufuk}" width="{W}" height="{H - ufuk}" fill="{g}"/>'
    r = RNG(74)
    for _ in range(10):                                     # sığ su şeritleri: gökyüzü yansıması
        s += (f'<ellipse cx="{f(r.uniform(0, W))}" cy="{f(r.uniform(ufuk + 8, ufuk + 64))}" rx="{f(r.uniform(90, 260))}" '
              f'ry="{f(r.uniform(2.4, 5))}" fill="#9CCBE8" opacity=".5"/>')
    # tuz kabuğu: perspektifli altıgen çatlak ağı (tuz kristallerinin doğadaki izi)
    yol = []
    a = 1.0
    for m in range(-14, 15):
        for q in range(1, 9):
            cx, cz = m * a * 3 ** .5 + (q % 2) * a * 3 ** .5 / 2, 2.0 + q * a * 1.5
            pts = []
            for j in range(6):
                gx, gz = cx + a * math.cos(math.radians(30 + 60 * j)), cz + a * math.sin(math.radians(30 + 60 * j)) * 1.0
                pts.append((W / 2 + gx * 520 / gz, ufuk + 14 + 760 / gz))
            yol.append(cizgi_d(pts[:4], False))            # her altıgenin yarısı: kenarlar bir kez çizilir
    s += f'<path d="{" ".join(yol)}" fill="none" stroke="#B7C4D6" stroke-width="2" stroke-linejoin="round" opacity=".75"/>'
    for x, y, w, h in ((1235, 300, 96, 50), (1330, 304, 70, 36), (1140, 298, 60, 30)):       # tuzla: tuz yığınları
        s += (f'<path d="M{x - w / 2} {y} Q{x - w * .12} {y - h * 1.15} {x} {y - h} Q{x + w * .14} {y - h * 1.1} {x + w / 2} {y} Z" fill="#FFFFFF"/>'
              f'<path d="M{x} {y - h} Q{x + w * .14} {y - h * 1.1} {x + w / 2} {y} H{x + w * .08} Z" fill="#CBD6E4"/>')
    s += _flamingo(1420, 330, .62) + _flamingo(1470, 338, .7, -1) + _flamingo(1090, 322, .5)
    s += '<ellipse cx="1820" cy="436" rx="260" ry="12" fill="#8FA3BD" opacity=".35"/>'
    s += '<use href="#elif-aha" x="1560" y="196" width="232" height="244"/>'
    s += '<use href="#yusuf-anlatan" x="1800" y="196" width="232" height="244"/>'
    s += '<use href="#pamuk-selam" x="1706" y="306" width="118" height="135"/>'
    s += _alt_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ 9/09 · Mardin (taş evler, tepede kale, Mezopotamya ovası)
def bant_mardin():
    s = Svg("uc-mar")
    s += S.gokyuzu(s, 0, 0, W, H, "altin")
    s += S.gunes(s, 1250, 300, 36, hale="#FFE2A0", hale_r=420, guc=.8)
    for i, (x, y, w) in enumerate([(1400, 70, 230), (900, 110, 180)]):
        s += S.bulut(s, x, y, w, 80 + i, ust="#FFF6E2", alt="#F2C99A", op=.85)
    ova = s.lin([(0, "#E8D49A"), (1, "#B9A55E")], 0, 330, 0, H, kull="userSpaceOnUse", ad="ov")
    s += f'<rect x="0" y="336" width="{W}" height="{H - 336}" fill="{ova}"/>'
    r = RNG(91)
    for _ in range(14):                                     # ova: tarla şeritleri
        x, y = r.uniform(0, 1400), r.uniform(346, 450)
        s += f'<path d="M{f(x)} {f(y)} l{f(r.uniform(160, 420))} {f(r.uniform(-6, 6))}" stroke="{r.choice(["#A9B45E", "#D9B878", "#8FA552", "#C49A5E"])}" stroke-width="{f(r.uniform(5, 11))}" opacity=".6" stroke-linecap="round"/>'
    tepe = s.lin([(0, "#D7B67C"), (1, "#A9824C")], 0, 80, 0, H, kull="userSpaceOnUse", ad="tp")
    s += f'<path d="M1040 {H} C1230 420 1370 200 1620 112 C1760 66 1920 84 {W} 150 L{W} {H} Z" fill="{tepe}"/>'
    s += Y.kucuk_kale(s, 1730, 112, 330, 64, tohum=3, tas="#D9BD8C")
    tonlar = ["#EBD3A2", "#E2C48E", "#F0DDB4", "#D9B880", "#E6CC98"]
    for i in range(6):                                      # yamaca basamaklanan düz damlı taş evler (uzaktan yakına)
        y = 176 + i * 50
        x = max(1090.0, 1650 - (y - 110) * 1.52) + r.uniform(0, 26)
        while x < W + 20:
            w, h = r.uniform(60, 96), r.uniform(40, 56)
            s += S.ev(x, y, w, h, r.randint(1, 999), duvar=r.choice(tonlar), duz=True, pencere="#6B4A2E", isik=-1)
            if r.random() < .5:                             # kemerli kapı / pencere
                kx = x + w * r.uniform(.25, .6)
                s += f'<path d="M{f(kx)} {f(y)} V{f(y - h * .42)} a{f(w * .09)} {f(w * .09)} 0 0 1 {f(w * .18)} 0 V{f(y)} Z" fill="#5A3E26"/>'
            x += w + r.uniform(-4, 10)
    s += '<ellipse cx="1560" cy="438" rx="230" ry="11" fill="#5A3E26" opacity=".3"/>'
    s += '<use href="#elif-soru" x="1330" y="204" width="226" height="237"/>'
    s += '<use href="#yusuf-anlatan" x="1560" y="204" width="226" height="237"/>'
    s += '<use href="#pamuk-dusunen" x="1486" y="318" width="110" height="126"/>'
    s += _alt_golge(s)
    return _bitir(s)


# ------------------------------------------------------------------ gözlük sayfası · atölye masası (bant 30 mm)
def bant_atolye():
    s = Svg("uc-ato")
    h = 300
    g = s.lin([(0, "#F7EBD2"), (1, "#E6CB98")], 0, 0, 0, h, kull="userSpaceOnUse", ad="ms")
    s += f'<rect width="{W}" height="{h}" fill="{g}"/>'
    r = RNG(5)
    for _ in range(26):                                     # ahşap damarı
        x, y = r.uniform(-100, W), r.uniform(8, h - 8)
        s += f'<path d="M{f(x)} {f(y)} q{f(r.uniform(120, 300))} {f(r.uniform(-7, 7))} {f(r.uniform(320, 640))} 0" fill="none" stroke="#C9A566" stroke-width="{f(r.uniform(1.2, 3))}" opacity=".45"/>'
    # karton, renkli asetatlar, kâğıt gözlük ve gözlüklü Pamuk (levhanın sağında)
    s += '<g transform="rotate(-7 1400 150)"><rect x="1320" y="70" width="170" height="150" rx="6" fill="#C9A26B" stroke="#8A6A3C" stroke-width="3"/><path d="M1340 100 H1470 M1340 130 H1470 M1340 160 H1470 M1340 190 H1470" stroke="#B08A54" stroke-width="2" opacity=".6"/></g>'
    s += (f'<g data-tema-sabit><rect x="1500" y="64" width="86" height="86" rx="5" transform="rotate(8 1543 107)" fill="{KIR}" opacity=".86" stroke="{OBS}" stroke-width="2.4"/>'
          f'<rect x="1548" y="126" width="86" height="86" rx="5" transform="rotate(-10 1591 169)" fill="{CAM}" opacity=".86" stroke="{OBS}" stroke-width="2.4"/></g>')
    s += (f'<path d="M1700 72 L1652 244 M1980 72 L2028 244" stroke="{OBS}" stroke-width="5" stroke-linecap="round" fill="none"/>'
          f'<path d="M1700 72 L1652 244 M1980 72 L2028 244" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" fill="none"/>')
    s += gozluk(1700, 50, 280, ic=True)
    s += pamuk_gozluklu(1760, 136, 160)
    return _bitir(s, h)


# ------------------------------------------------------------------ 10/04 · Göreme (Gazlar ünitesinin sahnesi, değiştirilmeden)
def bant_goreme():
    kitap = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    yol = os.path.join(kitap, "10-sinif-yerel", "04-gazlar", "uretec", "sahneler_unite.py")
    spec = importlib.util.spec_from_file_location("uc_gaz_sahne", yol)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.goreme()


# ================================================================== BİLGİ GRAFİKLERİ (gri dil: anaglifin yanında renk yok)
def _atom(x, y, r, harf, ton="#FFFFFF", yazi=OBS):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{ton}" stroke="{OBS}" stroke-width="2.4"/>'
            f'<text x="{f(x)}" y="{f(y + r * .36)}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="{f(r * 1.05)}" fill="{yazi}">{harf}</text>')


def _ok(x1, y1, x2, y2, renk=OBS, kal=4.6, bas=13):
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - bas * math.cos(a), y2 - bas * math.sin(a)
    return (f'<path d="M{f(x1)} {f(y1)} L{f(bx)} {f(by)}" stroke="{renk}" stroke-width="{kal}" stroke-linecap="round"/>'
            f'<path d="M{f(x2)} {f(y2)} L{f(bx - bas * .62 * math.sin(a))} {f(by + bas * .62 * math.cos(a))} L{f(bx + bas * .62 * math.sin(a))} {f(by - bas * .62 * math.cos(a))} Z" fill="{renk}" stroke="{renk}" stroke-width="2" stroke-linejoin="round"/>')


def duz_metan(onek):
    """Defterdeki düz CH₄ çizimi (artı biçimi, 90° izlenimi) ve gerçek açı."""
    o = [f'<path d="M150 150 V52 M150 150 V248 M150 150 H52 M150 150 H248" stroke="{OBS}" stroke-width="5" stroke-linecap="round"/>',
         f'<path d="M150 104 A46 46 0 0 1 196 150" fill="none" stroke="{GRI_K}" stroke-width="3.4" stroke-dasharray="6 5"/>',
         _atom(150, 150, 34, "C", "#5A6270", "#FFFFFF")]
    for x, y in ((150, 36), (150, 264), (36, 150), (264, 150)):
        o.append(_atom(x, y, 30, "H"))
    o.append(f'<text x="226" y="100" text-anchor="middle" {YAZI} font-size="42" fill="{GRI_K}">90°?</text>')
    return f'<svg class="info" viewBox="0 0 300 300">{"".join(o)}</svg>'


def dipol_oklari(onek):
    """Bağ çekişleri (elektronu daha çok çeken atoma doğru oklar): CO₂'de götürür, H₂O'da toplanır."""
    o = []
    # CO2 (doğrusal)
    o.append(f'<path d="M70 96 H290" stroke="{OBS}" stroke-width="12"/><path d="M70 96 H290" stroke="#FFFFFF" stroke-width="4"/>')
    o.append(_atom(180, 96, 32, "C", "#5A6270", "#FFFFFF") + _atom(62, 96, 32, "O", "#C9CED6") + _atom(298, 96, 32, "O", "#C9CED6"))
    o.append(_ok(156, 40, 76, 40) + _ok(204, 40, 284, 40))
    # H2O (kırık doğru): O üstte, H'ler altta 104,5°
    ox, oy, d = 560, 66, 104
    hs = [(ox + s * d * math.sin(math.radians(52.25)), oy + d * math.cos(math.radians(52.25))) for s in (-1, 1)]
    for hx, hy in hs:
        o.append(f'<path d="M{f(hx)} {f(hy)} L{ox} {oy}" stroke="{OBS}" stroke-width="12"/><path d="M{f(hx)} {f(hy)} L{ox} {oy}" stroke="{GRI_A}" stroke-width="6"/>')
    o.append(_atom(ox, oy, 32, "O", "#C9CED6") + "".join(_atom(hx, hy, 25, "H") for hx, hy in hs))
    for s, (hx, hy) in zip((-1, 1), hs):                    # bağ çekişleri: H'den O'ya
        kx, ky = s * 30, -6
        o.append(_ok(hx + kx + (ox - hx) * .16, hy + ky + (oy - hy) * .16, hx + kx + (ox - hx) * .8, hy + ky + (oy - hy) * .8))
    o.append(_ok(ox, 196, ox, 122, KEH, 8, 17))            # toplam çekiş: yukarı (O'ya doğru)
    return f'<svg class="info" viewBox="0 0 700 210">{"".join(o)}</svg>'


# "Nasıl çalışır?" şeması (üstten bakış). Yakın nokta için: sol gözün resmi (camgöbeği baskı) SAĞDA, sağ gözünki (kırmızı) SOLDA.
SEMA = dict(kagit=330, sol_goz=(250, 52), sag_goz=(550, 52), camgobegi_baski=(458, 330), kirmizi_baski=(342, 330))


def nasil_calisir(onek):
    """Üstten bakış: iki göz, iki cam, kâğıtta iki ayrı baskı; bakış doğruları kâğıdın ÖNÜNDE kesişir."""
    kagit, sol, sag, cb, kb = SEMA["kagit"], SEMA["sol_goz"], SEMA["sag_goz"], SEMA["camgobegi_baski"], SEMA["kirmizi_baski"]
    t = (sag[0] - sol[0]) / ((sag[0] - sol[0]) + (cb[0] - kb[0]))      # kesişme: gözler arası / (gözler arası + ayrıklık)
    kx, ky = sol[0] + (cb[0] - sol[0]) * t, sol[1] + (kagit - sol[1]) * t
    o = [f'<g data-tema-sabit>',
         f'<rect x="60" y="{kagit}" width="680" height="16" rx="3" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.4"/>',
         f'<path d="M{sol[0]} {sol[1]} L{cb[0]} {cb[1]}" stroke="{CAM}" stroke-width="4.4" stroke-dasharray="11 7"/>',
         f'<path d="M{sag[0]} {sag[1]} L{kb[0]} {kb[1]}" stroke="{KIR}" stroke-width="4.4" stroke-dasharray="11 7"/>',
         f'<rect x="{cb[0] - 20}" y="{kagit - 7}" width="40" height="14" rx="4" fill="{CAM}" stroke="{OBS}" stroke-width="2"/>',
         f'<rect x="{kb[0] - 20}" y="{kagit - 7}" width="40" height="14" rx="4" fill="{KIR}" stroke="{OBS}" stroke-width="2"/>',
         f'<rect x="{sol[0] - 54}" y="92" width="108" height="15" rx="5" fill="{KIR}" stroke="{OBS}" stroke-width="2.4"/>',
         f'<rect x="{sag[0] - 54}" y="92" width="108" height="15" rx="5" fill="{CAM}" stroke="{OBS}" stroke-width="2.4"/>',
         f'<path d="M{sol[0] + 54} 99.5 H{sag[0] - 54}" stroke="{OBS}" stroke-width="4"/>', '</g>']
    for x, y in (sol, sag):                                 # gözler (aşağı, kâğıda bakıyor)
        o.append(f'<circle cx="{x}" cy="{y}" r="30" fill="#FFFFFF" stroke="{OBS}" stroke-width="2.6"/><circle cx="{x + (400 - x) * .05}" cy="{y + 15}" r="12" fill="{OBS}"/>')
    o.append(f'<circle cx="{f(kx)}" cy="{f(ky)}" r="24" fill="#C9CED6" stroke="{OBS}" stroke-width="2.6"/><circle cx="{f(kx - 7)}" cy="{f(ky - 8)}" r="6" fill="#FFFFFF" opacity=".9"/>')
    yz = lambda x, y, m, a="middle", b=27, renk=OBS: f'<text x="{x}" y="{y}" text-anchor="{a}" {YAZI} font-size="{b}" fill="{renk}">{m}</text>'
    o += [yz(sol[0] - 44, 44, "SOL GÖZ", "end"), yz(sag[0] + 44, 44, "SAĞ GÖZ", "start"), yz(sol[0] - 64, 108, "kırmızı cam", "end", 25), yz(sag[0] + 64, 108, "camgöbeği cam", "start", 25),
          yz(f(kx + 36), f(ky - 4), "atom burada", "start", 25), yz(f(kx + 36), f(ky + 23), "görünür", "start", 25),
          yz(kb[0] - 30, kagit - 16, "kırmızı baskı", "end", 25), yz(cb[0] + 30, kagit - 16, "camgöbeği baskı", "start", 25),
          yz(400, kagit + 44, "KÂĞIT", "middle", 25, GRI_K)]
    return f'<svg class="info" viewBox="0 0 800 384">{"".join(o)}</svg>'


def gozluk_sablonu(onek):
    """Kesilecek karton şablon, GERÇEK ÖLÇÜDE (1 birim = 0,1 mm; 188 mm genişlikte basılır). İç yüz: kırmızı pencere SOLDA."""
    cx = 770                                                # ön parçanın ortası
    o = ['<g data-tema-sabit>']
    # ön parça: 136 mm çerçeve + iki yanda 9 mm yapıştırma kulağı; burun oyuğu; pencereler 44 × 27 mm, merkezleri 62 mm aralı
    o.append(f'<path d="M{cx - 770} 10 H{cx + 770} V370 H{cx + 680} V430 H{cx + 75} Q{cx + 66} 315 {cx} 315 Q{cx - 66} 315 {cx - 75} 430 H{cx - 680} V370 H{cx - 770} Z" '
             f'fill="#FFFFFF" stroke="{OBS}" stroke-width="4" stroke-linejoin="round"/>')
    for s, renk, ac, ad, alt in ((-1, KIR, KIR_A, "SOL GÖZ", "KIRMIZI"), (1, CAM, CAM_A, "SAĞ GÖZ", "CAMGÖBEĞİ")):
        x0 = cx + s * 310 - 220
        o.append(f'<rect x="{x0}" y="70" width="440" height="270" rx="60" fill="{ac}" stroke="{renk}" stroke-width="7"/>')
        o.append(f'<rect x="{x0}" y="70" width="440" height="270" rx="60" fill="none" stroke="{OBS}" stroke-width="3" stroke-dasharray="14 9"/>')
        o.append(f'<text x="{x0 + 220}" y="176" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="74" fill="{OBS}">{ad}</text>')
        o.append(f'<text x="{x0 + 220}" y="242" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="56" fill="{koyu(renk, .38)}">{alt}</text>')
        o.append(f'<text x="{x0 + 220}" y="296" text-anchor="middle" {YAZI} font-size="29" fill="{GRI_K}">{"(mavi-yeşil) · kes, çıkar" if s > 0 else "pencereyi kes, çıkar"}</text>')
        fx = cx + s * 680                                   # katlama çizgisi + yapıştırma kulağı
        o.append(f'<path d="M{fx} 10 V370" stroke="{OBS}" stroke-width="2.6" stroke-dasharray="5 9"/>')
        o.append(f'<text transform="translate({fx + s * 56} 190) rotate({-90 * s})" text-anchor="middle" {YAZI} font-size="27" fill="{GRI_K}">KATLA · SAP BURAYA</text>')
    o.append(f'<text x="{cx}" y="50" text-anchor="middle" {YAZI} font-size="28" letter-spacing="2" fill="{GRI_K}">İÇ YÜZ · BU YÜZ SANA BAKSIN</text>')
    o.append(f'<text x="{cx}" y="226" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="34" fill="{OBS}">Kimya</text>'
             f'<text x="{cx}" y="260" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="34" fill="{OBS}">Rotası</text>')
    # açıklama (sağ boşluk): çizgi türleri
    for i, (cizgi, metin) in enumerate(((f'stroke="{OBS}" stroke-width="4"', "düz çizgi: kes"), (f'stroke="{OBS}" stroke-width="2.6" stroke-dasharray="5 9"', "noktalı: katla"),
                                         (f'stroke="{OBS}" stroke-width="3" stroke-dasharray="14 9"', "kesik: oy, çıkar"))):
        y = 70 + i * 64
        o.append(f'<path d="M1580 {y} H1650" {cizgi} fill="none"/><text x="1666" y="{y + 9}" {YAZI} font-size="26" fill="{GRI_K}">{metin}</text>')
    o.append(f'<text x="1580" y="282" {YAZI} font-size="26" fill="{GRI_K}">gerçek ölçü:</text><text x="1580" y="316" {YAZI} font-size="26" fill="{GRI_K}">ön parça 15,4 cm</text>'
             f'<text x="1580" y="350" {YAZI} font-size="26" fill="{GRI_K}">saplar 12,5 cm</text>')
    # saplar: 2 × (125 mm × 15 mm), arka ucu kulağa göre kıvrık
    for i, ad in enumerate(("SOL SAP", "SAĞ SAP")):
        y = 462 + i * 172
        o.append(f'<path d="M30 {y} H1100 Q1250 {y} 1280 {y + 96} Q1290 {y + 150} 1240 {y + 150} Q1200 {y + 150} 1180 {y + 150} Q1150 {y + 150} 1100 {y + 150} H30 Z" '
                 f'fill="#FFFFFF" stroke="{OBS}" stroke-width="4" stroke-linejoin="round"/>')
        o.append(f'<path d="M120 {y} V{y + 150}" stroke="{OBS}" stroke-width="2.6" stroke-dasharray="5 9"/>')
        o.append(f'<text transform="translate(84 {y + 75}) rotate(-90)" text-anchor="middle" {YAZI} font-size="24" fill="{GRI_K}">YAPIŞTIR</text>')
        o.append(f'<text x="620" y="{y + 92}" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="50" fill="{GRI}" letter-spacing="6">{ad}</text>')
    # ölçek denetimi: 50 mm
    o.append(f'<path d="M1350 600 H1850 M1350 584 V616 M1850 584 V616 M1600 592 V608" stroke="{OBS}" stroke-width="3.4" stroke-linecap="round" fill="none"/>')
    o.append(f'<text x="1600" y="566" text-anchor="middle" {YAZI} font-size="27" fill="{GRI_K}">ölçü denetimi: bu çizgi tam 5 cm</text>')
    o.append(f'<text x="1600" y="660" text-anchor="middle" {YAZI} font-size="27" fill="{GRI_K}">(değilse yazıcıda “gerçek boyut” seç)</text>')
    o.append('</g>')
    return f'<svg class="info sablon" viewBox="0 0 1880 800">{"".join(o)}</svg>'


IKON = {
    # 3B rozeti: gözlük (nötr gri: anaglifin yanında renk yok)
    "gozluk": ("0 0 48 24", f'<path d="M3 4 H45 Q47 4 47 6 V18 Q47 20 45 20 H29 Q27.5 14 24 14 Q20.5 14 19 20 H3 Q1 20 1 18 V6 Q1 4 3 4 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.8" stroke-linejoin="round"/>'
                            f'<rect x="5" y="7" width="13" height="9" rx="2.6" fill="{GRI_K}"/><rect x="30" y="7" width="13" height="9" rx="2.6" fill="#C5CBD5"/>'),
    "cetvel": ("0 0 24 24", f'<rect x="1.5" y="8" width="21" height="8" rx="1.4" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6"/><path d="M5 8 v3.2 M8.5 8 v2 M12 8 v3.2 M15.5 8 v2 M19 8 v3.2" stroke="{OBS}" stroke-width="1.3"/>'),
    "duz": ("0 0 24 24", f'<path d="M3 17 L9 7 H21 L15 17 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.6" stroke-linejoin="round"/><path d="M8 13 h8 M9.4 10.6 h8" stroke="{GRI}" stroke-width="1.3"/>'),
    "saat": ("0 0 24 24", f'<circle cx="12" cy="12" r="9.2" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.7"/><path d="M12 6.6 V12 L15.8 14.4" fill="none" stroke="{OBS}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'),
    "damla": ("0 0 24 24", f'<g data-tema-sabit stroke="{OBS}" stroke-width="1.4" stroke-linejoin="round"><path d="M7 3.5 C4.4 7.6 3 9.6 3 11.6 A4 4 0 0 0 11 11.6 C11 9.6 9.6 7.6 7 3.5 Z" fill="{CAM}"/>'
                           f'<path d="M17 3.5 C14.4 7.6 13 9.6 13 11.6 A4 4 0 0 0 21 11.6 C21 9.6 19.6 7.6 17 3.5 Z" fill="{KIR}"/><path d="M12 11.5 C9.4 15.6 8 17.2 8 19 A4 4 0 0 0 16 19 C16 17.2 14.6 15.6 12 11.5 Z" fill="#F2C230"/></g>'),
    "goz": ("0 0 24 24", f'<path d="M1.6 12 Q12 2.4 22.4 12 Q12 21.6 1.6 12 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="12" r="4.2" fill="{OBS}"/><circle cx="10.6" cy="10.6" r="1.3" fill="#FFFFFF"/>'),
}


def ub_ikon(onek, ad, cls="ubi"):
    vb, govde = IKON[ad]
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true">{govde}</svg>'
