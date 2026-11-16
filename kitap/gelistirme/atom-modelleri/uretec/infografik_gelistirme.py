"""Geliştirme örneği · bilgi grafikleri ({{info|ad}} → fn(önek)). Karakterler konu_karakterleri.py'den (<use href="#kk-…">).

  zincir_yolu        Model Zinciri'nin arkasındaki yol (HTML ızgaranın altında)
  pano_duzenek … pano_sonuc   altın levha çizgi romanının 6 panosu (yazılar HTML; burada yalnız resim)
  enerji_merdiveni   Bohr: basamaklar (n = 1…6, ∞) + soğurma/yayma + görünür dört çizgi
  tahmin_beklenen / tahmin_gozlenen   Thomson'a göre beklenen ↔ gözlenen (öneri)
  mini_yorunge / mini_bulut           yanlış bilinen ↔ doğrusu (öneri)
Bütün sayılar dogrula.py'de yeniden hesaplanır (Rydberg, −13,6/n² eV, foton enerjileri). Dalga boyu renkleri ve spektrum
data-tema-sabit içindedir (temalar fiziksel rengi değiştirmez). SVG yazısında kontur yok; ⁺ ⁻ tspan ile.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, acik, koyu, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A, ALTIN, ALTIN_K,
                           GUM, GUM_K, GUM_A, ZUMRUT)
import konu_karakterleri as KK

T = 'font-family="Nunito" font-weight="800"'
T9 = 'font-family="Nunito" font-weight="900"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'
W_P, H_P = 592, 610          # pano: 59,2 × 61 mm
ELEKTRON = KK.ELEKTRON

# Bohr · hidrojen: E_n = −13,6 / n² eV (dogrula.py aynı değerleri hesaplar)
ENERJI = {n: -13.6 / n ** 2 for n in range(1, 7)}
BALMER = {6: 410, 5: 434, 4: 486, 3: 656}            # n → 2 inişlerinin dalga boyu (nm), Rydberg ile denetlenir


def _ok(x0, y0, x1, y1, renk=OBS, k=5, uc=16, kesik=False):
    a = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - uc * math.cos(a - .45), y1 - uc * math.sin(a - .45))
    p2 = (x1 - uc * math.cos(a + .45), y1 - uc * math.sin(a + .45))
    ks = ' stroke-dasharray="10 8"' if kesik else ""
    return (f'<path d="M{f(x0)} {f(y0)} L{f(x1 - uc * .6 * math.cos(a))} {f(y1 - uc * .6 * math.sin(a))}" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"{ks}/>'
            f'<path d="M{f(x1)} {f(y1)} L{nok(p1)} L{nok(p2)} Z" fill="{renk}"/>')


def _egri_ok(p0, c, p1, renk=OBS, k=4.4, uc=17, kesik=True):
    """İkinci derece Bezier yol + uçta ok başı (teğet yönünde)."""
    ks = ' stroke-dasharray="11 8"' if kesik else ""
    a = math.atan2(p1[1] - c[1], p1[0] - c[0])
    q1 = (p1[0] - uc * math.cos(a - .45), p1[1] - uc * math.sin(a - .45))
    q2 = (p1[0] - uc * math.cos(a + .45), p1[1] - uc * math.sin(a + .45))
    son = (p1[0] - uc * .55 * math.cos(a), p1[1] - uc * .55 * math.sin(a))
    return (f'<path d="M{nok(p0)} Q{nok(c)} {nok(son)}" fill="none" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"{ks}/>'
            f'<path d="M{nok(p1)} L{nok(q1)} L{nok(q2)} Z" fill="{renk}"/>')


def _hiz(x, y, n=3, uz=46, ara=13, renk="#9FB2BC"):
    """Hız çizgileri (sola doğru)."""
    return "".join(f'<path d="M{f(x - k * 6)} {f(y + (k - (n - 1) / 2) * ara)} h{f(-uz + k * 8)}" stroke="{renk}" stroke-width="4" stroke-linecap="round"/>' for k in range(n))


def _no(x, y, n, renk=GOL_K, r=17):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="#FFFFFF" stroke="{renk}" stroke-width="3.4"/>'
            f'<text x="{f(x)}" y="{f(y + r * .42)}" text-anchor="middle" {T9} font-size="{f(r * 1.2)}" fill="{renk}">{n}</text>')


def _alt(metin, x, y, fs, renk=OBS, anchor="middle", font=T):
    """_2 alt simge, ^{…} üst simge (tspan)."""
    import re
    parca = re.split(r"(_\d+|\^\{[^}]*\})", metin)
    o = [f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" {font} font-size="{f(fs)}" fill="{renk}">']
    dy = 0
    for p in parca:
        if not p:
            continue
        if p.startswith("_"):
            o.append(f'<tspan dy="{f(fs * .24 - dy)}" font-size="{f(fs * .66)}">{p[1:]}</tspan>')
            dy = fs * .24
        elif p.startswith("^"):
            o.append(f'<tspan dy="{f(-fs * .38 - dy)}" font-size="{f(fs * .62)}">{p[2:-1]}</tspan>')
            dy = -fs * .38
        else:
            o.append(f'<tspan dy="{f(-dy)}">{p}</tspan>' if dy else p)
            dy = 0
    o.append("</text>")
    return "".join(o)


# ------------------------------------------------------------------ MODEL ZİNCİRİ · yol

def zincir_yolu(onek="ag-zy"):
    s = Svg(onek)
    W, H = 1880, 220
    yol = "M-20 126 C300 100 620 150 940 122 S1560 96 1900 128"
    s += f'<path d="{yol}" fill="none" stroke="#B48A48" stroke-width="58" stroke-linecap="round"/>'
    s += f'<path d="{yol}" fill="none" stroke="#E2C48A" stroke-width="50" stroke-linecap="round"/>'
    s += f'<path d="{yol}" fill="none" stroke="#FFF4D8" stroke-width="4" stroke-dasharray="20 16"/>'
    r = RNG(12)
    for _ in range(46):                        # yol kenarında kuru ot
        x = r.uniform(0, W)
        y = 126 + 34 * math.sin(x / 300) * .2 + r.choice((-38, 40)) + r.uniform(-4, 4)
        s += f'<path d="M{f(x)} {f(y)} l-4 -12 M{f(x)} {f(y)} l1 -15 M{f(x)} {f(y)} l6 -11" stroke="#B98A3E" stroke-width="2.2" stroke-linecap="round" opacity=".7"/>'
    for k in range(1, 6):                      # karakterler arası yön okları
        x = W * k / 6
        y = 126 - 12 * math.sin(k)
        s += (f'<path d="M{f(x - 16)} {f(y - 14)} L{f(x + 6)} {f(y)} L{f(x - 16)} {f(y + 14)}" fill="none" stroke="#7A5A2A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<path d="M{f(x - 2)} {f(y - 14)} L{f(x + 20)} {f(y)} L{f(x - 2)} {f(y + 14)}" fill="none" stroke="#7A5A2A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>')
    return s.cikti(f"0 0 {W} {H}", cls="yol", par="none")


# ------------------------------------------------------------------ ÇİZGİ ROMAN · altın levha

def _pano_zemin(s, ust="#F3F8FB", alt="#DCE8EF"):
    g = s.lin([(0, ust), (1, alt)], 0, 0, 0, H_P, kull="userSpaceOnUse", ad="pz")
    return f'<rect width="{W_P}" height="{H_P}" fill="{g}"/>'


def _yakin_zemin(s):
    """Altın levhanın içi (büyüteçle): sıcak açık zemin + büyüteç halkası izi."""
    g = s.rad([(0, "#FFFDF4"), (1, "#FBEFCF")], .5, .55, .75, ad="yz")
    return f'<rect width="{W_P}" height="{H_P}" fill="{g}"/>'


def _altin_atom(cx, cy, r=92, yuz="kk-cekirdek", w=38):
    return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{r}" fill="#FFF5D6" stroke="#D9B45A" stroke-width="2.4" stroke-dasharray="8 7"/>'
            + KK.kullan(yuz, cx - w / 2, cy - w * .55, w))


def _halka_aralikli(cx, cy, rx, ry, bosluk_deg=18):
    """Sol tarafında demetin girdiği boşluk olan elips halka (yol)."""
    t1, t2 = math.radians(180 + bosluk_deg), math.radians(180 - bosluk_deg)
    p1 = (cx + rx * math.cos(t1), cy + ry * math.sin(t1))
    p2 = (cx + rx * math.cos(t2), cy + ry * math.sin(t2))
    return f"M{nok(p1)} A{rx} {ry} 0 1 1 {nok(p2)}"


def _carp(x, y, R=34, r=15, renk=KEH):
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        rr = R if i % 2 == 0 else r
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return f'<path d="{cizgi_d(pts, True)}" fill="{renk}" stroke="{OBS}" stroke-width="2.6" stroke-linejoin="round"/>'


def pano_duzenek(onek="ag-p1"):
    s = Svg(onek)
    s += _pano_zemin(s)
    s += f'<rect x="0" y="548" width="{W_P}" height="62" fill="#C9D6DE"/><path d="M0 548 H{W_P}" stroke="#9FB2BC" stroke-width="3"/>'
    cx, cy, rx, ry = 380, 392, 190, 150
    d = _halka_aralikli(cx, cy, rx, ry, 16)
    s += f'<path d="{d}" fill="none" stroke="#9FE0B4" stroke-width="20" stroke-linecap="round" opacity=".95"/>'
    s += f'<path d="{_halka_aralikli(cx, cy, rx + 10, ry + 10, 15)}" fill="none" stroke="#2F8F5E" stroke-width="2.6"/>'
    s += f'<path d="{_halka_aralikli(cx, cy, rx - 10, ry - 10, 17)}" fill="none" stroke="#2F8F5E" stroke-width="2.6"/>'
    # kurşun blok ve radyoaktif kaynak
    s += f'<rect x="14" y="336" width="112" height="112" rx="12" fill="#5E6672" stroke="{OBS}" stroke-width="3.4"/>'
    s += f'<rect x="30" y="352" width="80" height="80" rx="8" fill="#4A515C"/><rect x="112" y="380" width="22" height="24" fill="#2A2E36"/>'
    gk = s.rad([(0, "#FFE3D8"), (.4, MER), (1, MER, 0)], 70, 392, 44, kull="userSpaceOnUse", ad="kn")
    s += f'<circle cx="70" cy="392" r="44" fill="{gk}"/><circle cx="70" cy="392" r="14" fill="{MER}" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<path d="M134 392 H{cx - 8}" stroke="{MER}" stroke-width="14" opacity=".2" stroke-linecap="round"/>'
    # levhadan sonra: çoğu düz, birkaçı sapar, biri geri döner (ekranda ışıltı)
    for dy in (-24, -8, 8, 24):
        s += f'<path d="M{cx + 6} {cy + dy * .2} L{cx + rx - 2} {cy + dy}" stroke="{MER}" stroke-width="3.2" opacity=".75"/>'
        s += f'<circle cx="{cx + rx}" cy="{cy + dy}" r="8.5" fill="#F4FFE8" stroke="#2F8F5E" stroke-width="2.6"/>'
    for t in (-52, 58):
        a = math.radians(t)
        ex, ey = cx + rx * math.cos(a), cy + ry * math.sin(a)
        s += f'<path d="M{cx + 6} {cy} L{f(ex)} {f(ey)}" stroke="{MER}" stroke-width="3.2" opacity=".75"/>'
        s += f'<circle cx="{f(ex)}" cy="{f(ey)}" r="8.5" fill="#F4FFE8" stroke="#2F8F5E" stroke-width="2.6"/>'
    a = math.radians(222)
    ex, ey = cx + rx * math.cos(a), cy + ry * math.sin(a)
    s += f'<path d="M{cx - 6} {cy - 4} L{f(ex)} {f(ey)}" stroke="{MER}" stroke-width="3.2" stroke-dasharray="9 7"/>'
    s += f'<circle cx="{f(ex)}" cy="{f(ey)}" r="8.5" fill="#F4FFE8" stroke="#2F8F5E" stroke-width="2.6"/>'
    # ince altın levha
    gl = s.lin([(0, "#FFF0B0"), (.5, ALTIN), (1, ALTIN_K)], cx - 7, 0, cx + 7, 0, kull="userSpaceOnUse", ad="lv")
    s += f'<rect x="{cx - 6}" y="{cy - 104}" width="12" height="208" rx="2" fill="{gl}" stroke="{ALTIN_K}" stroke-width="2"/>'
    s += f'<path d="M{cx + 18} {cy - 118} l6 -16 l6 16 l16 6 l-16 6 l-6 16 l-6 -16 l-16 -6 Z" fill="#FFF6C8" stroke="{ALTIN_K}" stroke-width="1.8"/>'
    # uçan α
    s += _hiz(148, 400, 3, 44, 15)
    s += KK.kullan("kk-alfa", 150, 350, 112)
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def pano_gecer(onek="ag-p2"):
    s = Svg(onek)
    s += _yakin_zemin(s)
    s += _altin_atom(150, 300, 150, w=76)
    s += _altin_atom(470, 470, 150, w=76)
    s += _altin_atom(560, 250, 110, w=60)
    s += _hiz(40, 444, 3, 50, 16, "#D9B45A")
    s += KK.kullan("kk-alfa-mutlu", 42, 392, 126)
    s += _hiz(300, 264, 3, 50, 16, "#D9B45A")
    s += KK.kullan("kk-alfa-mutlu", 302, 212, 120)
    s += f'<path d="M14 470 H40 M14 290 H300" stroke="#D9B45A" stroke-width="3" stroke-dasharray="9 8"/>'
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def pano_sapar(onek="ag-p3"):
    s = Svg(onek)
    s += _yakin_zemin(s)
    s += _altin_atom(240, 420, 170, w=112)
    s += f'<path d="M14 506 C130 506 220 500 278 470 C330 440 372 360 440 290" fill="none" stroke="{MER}" stroke-width="5" stroke-dasharray="12 9" stroke-linecap="round"/>'
    s += _ok(426, 306, 444, 286, MER, 5, 20)
    for k in range(3):
        s += f'<path d="M{f(300 + k * 13)} {f(430 - k * 15)} q 12 -7 21 2" fill="none" stroke="{MER_K}" stroke-width="3.4" stroke-linecap="round" opacity="{f(.9 - k * .22, 2)}"/>'
    s += KK.kullan("kk-alfa-sasiran", 424, 156, 132, donus=-16)
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def pano_doner(onek="ag-p4"):
    s = Svg(onek)
    s += _yakin_zemin(s)
    s += _altin_atom(436, 440, 160, w=128)
    s += f'<path d="M14 478 H326" stroke="{MER}" stroke-width="5" stroke-dasharray="12 9" stroke-linecap="round"/>'
    s += f'<path d="M330 462 C270 440 230 400 186 352" fill="none" stroke="{MER}" stroke-width="5.4" stroke-linecap="round"/>'
    s += _ok(196, 364, 180, 346, MER, 5.4, 22)
    s += _carp(350, 470, 36, 16)
    s += KK.kullan("kk-alfa-sersem", 26, 214, 140, donus=-8)
    for x, y in ((52, 210), (88, 192), (124, 206)):
        s += f'<path d="M{x} {y - 10} l3.4 7 l7.6 1 l-5.6 5.4 l1.4 7.6 l-6.8 -3.6 l-6.8 3.6 l1.4 -7.6 l-5.6 -5.4 l7.6 -1 Z" fill="{KEH}" stroke="{OBS}" stroke-width="1.6"/>'
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def pano_neden(onek="ag-p5"):
    s = Svg(onek)
    s += _pano_zemin(s, "#F2F8F2", "#E0EEDC")
    cx, cy = 318, 404
    s += f'<ellipse cx="{cx}" cy="{cy + 10}" rx="262" ry="160" fill="#0E2A3A" opacity=".12"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="258" ry="156" fill="#C9D2DA" stroke="{OBS}" stroke-width="3"/>'
    for k in range(5):        # tribün sıraları
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{246 - k * 10}" ry="{146 - k * 8}" fill="none" stroke="#A7B4BE" stroke-width="2"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="190" ry="102" fill="#D9765E" stroke="{OBS}" stroke-width="2.4"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="160" ry="80" fill="#7CC36A" stroke="#FFFFFF" stroke-width="3"/>'
    for k in range(-3, 4):
        s += f'<path d="M{cx + k * 44} {cy - 76} V{cy + 76}" stroke="#6AB35A" stroke-width="20" opacity=".5"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="160" ry="80" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
    s += f'<path d="M{cx} {cy - 80} V{cy + 80}" stroke="#FFFFFF" stroke-width="2.6"/><circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="#FFFFFF" stroke-width="2.6"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="5.2" fill="#E9C77E" stroke="{OBS}" stroke-width="1.6"/>'
    s += f'<path d="M{cx + 6} {cy - 5} L{cx + 70} {cy - 54}" stroke="{OBS}" stroke-width="2.2"/><circle cx="{cx + 70}" cy="{cy - 54}" r="3.4" fill="{OBS}"/>'
    s += f'<use href="#pamuk-dusunen" x="0" y="424" width="136" height="155"/>'
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


def pano_sonuc(onek="ag-p6"):
    s = Svg(onek)
    s += KK.kullan("kk-rutherford", 196, 104, 196)
    s += f'<path d="M410 172 L370 186" stroke="{OBS}" stroke-width="2.2"/>'
    s += _alt("çoğu boşluk", 416, 180, 25, GOL_K, "start", T9)
    s += f'<path d="M186 246 L284 212" stroke="{OBS}" stroke-width="2.2"/>'
    s += _alt("küçük, yoğun", 182, 246, 25, MER_K, "end", T9)
    s += _alt("(+) çekirdek", 182, 276, 25, MER_K, "end", T9)
    return s.cikti(f"0 0 {W_P} {H_P}", cls="resim", par="xMidYMid slice")


# ------------------------------------------------------------------ ENERJİ MERDİVENİ (Bohr · H atomu)

def _y_basamak(n):
    """Basamak üst yüzeyi: y = 150 + 470/n (ölçekli değil; yukarıda sıklaşma korunur)."""
    return 150 + 470 / n


def _ev(n):
    e = ENERJI[n]
    return ("−13,6" if n == 1 else f"{e:.2f}".replace(".", ",").replace("-", "−"))


def enerji_merdiveni(onek="ag-em"):
    s = Svg(onek)
    zemin = 742
    # ---- sol: basamaklar
    s += f'<path d="M40 {zemin} V120" stroke="{GUM_K}" stroke-width="3.4"/>' + _ok(40, 160, 40, 112, GUM_K, 3.4, 15)
    s += f'<text x="54" y="124" {T} font-size="21" fill="{GUM_K}">enerji</text>'
    s += f'<path d="M70 140 H1000" stroke="{GUM_K}" stroke-width="2.6" stroke-dasharray="10 8"/>'
    s += f'<text x="1000" y="128" text-anchor="end" {T} font-size="19" fill="{GUM_K}">n = ∞ · E = 0: elektron atomdan kopar</text>'
    araliklar = {1: (70, 330), 2: (330, 560), 3: (560, 720), 4: (720, 830), 5: (830, 910), 6: (910, 970)}
    harf = {1: "K", 2: "L", 3: "M"}
    tas = s.lin([(0, "#F7EDD5"), (1, "#D9C29A")], 0, 220, 0, zemin, kull="userSpaceOnUse", ad="ts")
    for n, (x0, x1) in araliklar.items():
        y = _y_basamak(n)
        w = x1 - x0
        s += f'<rect x="{x0}" y="{f(y)}" width="{w}" height="{f(zemin - y)}" fill="{tas}" stroke="{OBS}" stroke-width="2.6"/>'
        s += f'<path d="M{x0 + 3} {f(y + 4)} H{x1 - 3}" stroke="#FFFFFF" stroke-width="3" opacity=".8"/>'
        if n <= 3:
            y0 = y + 42
            s += f'<text x="{f(x0 + w / 2)}" y="{f(y0)}" text-anchor="middle" {B} font-size="33" fill="{OBS}">n = {n}</text>'
            s += f'<text x="{f(x0 + w / 2)}" y="{f(y0 + 30)}" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">{harf[n]} katmanı</text>'
            s += f'<text x="{f(x0 + w / 2)}" y="{f(y0 + 58)}" text-anchor="middle" {T9} font-size="22" fill="{KOB_K}">{_ev(n)} eV</text>'
        else:
            s += f'<text x="{f(x0 + w / 2)}" y="{f(y + 30)}" text-anchor="middle" {B} font-size="{26 if n == 4 else 22}" fill="{OBS}">{n}</text>'
            s += f'<text x="{f(x0 + w / 2)}" y="{f(y + 54)}" text-anchor="middle" {T9} font-size="{17 if n == 4 else 15}" fill="{KOB_K}">{_ev(n)}</text>'
    s += f'<text x="970" y="{zemin + 16}" text-anchor="end" {T} font-size="17" fill="{GUM_K}">basamaklar yukarıda sıklaşır · ölçekli değil</text>'
    y1, y2, y3 = _y_basamak(1), _y_basamak(2), _y_basamak(3)
    # 1 · soğurma: temel hâldeki elektron UV fotonu yutar, n = 3'e çıkar
    s += KK.kullan("kk-foton-uv", 30, 404, 150, donus=27)
    s += f'<text x="98" y="392" text-anchor="middle" {T9} font-size="19" fill="{GUM_K}">UV foton</text>'
    s += KK.kullan("kk-elektron", 150, y1 - 84, 90)
    s += _egri_ok((214, y1 - 92), (300, 150), (640, y3 - 96), KOB, 5, 20)
    s += _no(330, 238, 1, KOB)
    s += KK.kullan("kk-elektron-heyecan", 592, y3 - 88, 94)
    s += f'<text x="586" y="{f(y3 - 46)}" text-anchor="end" {T9} font-size="20" fill="{KOB_K}">uyarılmış hâl</text>'
    s += f'<text x="146" y="{f(y1 - 26)}" text-anchor="end" {T9} font-size="20" fill="{GOL_K}">temel hâl</text>'
    # 2 · yayma: n = 3 → 2, kırmızı foton (656 nm)
    s += _egri_ok((600, y3 - 34), (548, y3 - 30), (512, y2 - 64), MER, 5, 20)
    s += _no(536, y3 + 36, 2, MER)
    s += f'<g data-tema-sabit="">{KK.kullan("kk-foton-656", 726, 160, 140, donus=-6)}</g>'
    s += f'<text x="926" y="206" text-anchor="middle" {T9} font-size="19" fill="{MER_K}">656 nm</text>'
    s += KK.kullan("kk-elektron-sakin", 420, y2 - 80, 86)
    # 3 · yine yayma: n = 2 → 1 (UV, çizimde yalnız ok)
    s += _egri_ok((414, y2 - 20), (330, y2 - 10), (290, y1 - 10), GUM_K, 4, 17)
    s += _no(338, y2 + 26, 3, GUM_K)
    # ---- sağ: görünür dört çizgi (hep n = 2'ye iniş)
    xa, xb = 1100, 1780

    def nmx(nm):
        return xa + (nm - 400) / 300 * (xb - xa)
    yl = {2: 480, 3: 382, 4: 320, 5: 280, 6: 252}
    s += f'<rect x="1032" y="62" width="776" height="690" rx="22" fill="#F4F6FF" stroke="#C3CAEB" stroke-width="2.4"/>'
    s += f'<text x="1420" y="108" text-anchor="middle" {B} font-size="31" fill="{KOB_K}">Görünür ışık: hep n = 2’ye iniş</text>'
    s += f'<text x="1420" y="144" text-anchor="middle" {T} font-size="20" fill="{GUM_K}">fark büyüdükçe dalga boyu kısalır (mora kayar)</text>'
    s += f'<path d="M1100 192 H1792" stroke="{GUM_K}" stroke-width="2" stroke-dasharray="9 7"/><text x="1088" y="199" text-anchor="end" {T} font-size="19" fill="{GUM_K}">∞</text>'
    for n, y in yl.items():
        s += f'<path d="M1100 {y} H1792" stroke="{OBS}" stroke-width="{3.4 if n == 2 else 2.4}"/>'
        s += f'<text x="1088" y="{y + 7}" text-anchor="end" {T9} font-size="{21 if n == 2 else 18}" fill="{OBS}">n = {n}</text>'
    sabit = []
    for n, nm in BALMER.items():
        x = nmx(nm)
        renk = KK.nm_renk(nm)
        sabit.append(_ok(x, yl[n] + 2, x, yl[2] - 3, renk, 6.4, 19))
        sabit.append(f'<path d="M{f(x)} {yl[2] + 6} V630" stroke="{renk}" stroke-width="3.2" stroke-dasharray="3 8" stroke-linecap="round"/>')
    for nm, y in {410: 494, 434: 560, 486: 516, 656: 516}.items():
        w = 92
        sabit.append(KK.kullan(f"kk-foton-{nm}", nmx(nm) - w * .74, y, w))
    sabit.append(f'<rect x="{xa}" y="632" width="{xb - xa}" height="52" rx="6" fill="#14142E" stroke="{OBS}" stroke-width="2.4"/>')
    for nm in BALMER.values():
        sabit.append(f'<rect x="{f(nmx(nm) - 4.5)}" y="635" width="9" height="46" fill="{KK.nm_renk(nm)}"/>')
    s += f'<g data-tema-sabit="">{"".join(sabit)}</g>'
    for nm in (400, 500, 600, 700):
        x = nmx(nm)
        etk, anc, dx = ("700 nm", "end", 16) if nm == 700 else (str(nm), "middle", 0)
        s += f'<path d="M{f(x)} 686 v9" stroke="{OBS}" stroke-width="2"/><text x="{f(x + dx)}" y="716" text-anchor="{anc}" {T} font-size="17" fill="{GUM_K}">{etk}</text>'
    for nm in BALMER.values():
        dx = {410: -12, 434: 12}.get(nm, 0)
        s += f'<text x="{f(nmx(nm) + dx)}" y="742" text-anchor="middle" {T9} font-size="19" fill="{OBS}">{nm}</text>'
    return s.cikti("0 56 1820 704", cls="info merdiven")


# ------------------------------------------------------------------ ÖNERİLER · küçük resimler

def _cerceve_mini(s, W, H):
    return f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#FFFFFF" stroke="#C9D3DA" stroke-width="2"/>'


def tahmin_beklenen(onek="ag-tb"):
    """Thomson'a göre: (+) yük her yere dağınık → α'lar hafifçe sapar, hepsi geçer."""
    s = Svg(onek)
    W, H = 420, 200
    s += _cerceve_mini(s, W, H)
    g = s.rad([(0, "#FFD9C8"), (.6, "#F4A68E"), (1, "#D9846C")], .4, .35, .8, ad="tk")
    s += f'<circle cx="210" cy="100" r="74" fill="{g}" stroke="{OBS}" stroke-width="2.6"/>'
    for x, y in ((180, 64), (238, 70), (170, 120), (250, 128), (212, 100), (206, 148), (230, 50)):
        s += f'<circle cx="{x}" cy="{y}" r="7" fill="{ELEKTRON}" stroke="#13235E" stroke-width="1.4"/><path d="M{x - 3.4} {y} H{x + 3.4}" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>'
    for k, y in enumerate((44, 76, 100, 124, 156)):
        s += f'<path d="M14 {y} C150 {y} 270 {y + (k - 2) * 4} 384 {y + (k - 2) * 9}" fill="none" stroke="{MER}" stroke-width="3.2" stroke-linecap="round" opacity=".85"/>'
        s += _ok(370, y + (k - 2) * 8.5, 398, y + (k - 2) * 9.6, MER, 3.2, 13)
    return s.cikti(f"0 0 {W} {H}", cls="mini-t", oz='data-tema-sabit=""')


def tahmin_gozlenen(onek="ag-tg"):
    """Gözlenen: çoğu düz geçer, azı sapar, çok azı geri döner → küçük, yoğun (+) çekirdek."""
    s = Svg(onek)
    W, H = 420, 200
    s += _cerceve_mini(s, W, H)
    s += f'<circle cx="210" cy="100" r="74" fill="#EEF6FA" stroke="#8FA6B2" stroke-width="2.4" stroke-dasharray="7 6"/>'
    s += f'<circle cx="210" cy="100" r="9" fill="{MER}" stroke="{OBS}" stroke-width="2"/>'
    for y in (40, 70, 132, 162):
        s += f'<path d="M14 {y} H384" stroke="{MER}" stroke-width="3.2" opacity=".85"/>' + _ok(370, y, 398, y, MER, 3.2, 13)
    s += f'<path d="M14 110 C140 110 196 112 214 96 C232 80 300 50 380 30" fill="none" stroke="{MER}" stroke-width="3.2" opacity=".85"/>' + _ok(366, 34, 392, 27, MER, 3.2, 13)
    s += f'<path d="M14 92 H190" stroke="{MER_K}" stroke-width="4.6" stroke-linecap="round"/>'
    s += f'<path d="M192 92 C176 78 120 70 40 64" fill="none" stroke="{MER_K}" stroke-width="4.6" stroke-linecap="round"/>' + _ok(56, 65, 30, 63, MER_K, 4.6, 16)
    return s.cikti(f"0 0 {W} {H}", cls="mini-t", oz='data-tema-sabit=""')


def mini_yorunge(onek="ag-my"):
    s = Svg(onek)
    W, H = 300, 150
    s += f'<ellipse cx="150" cy="75" rx="126" ry="56" fill="none" stroke="{OBS}" stroke-width="5"/>'
    s += f'<circle cx="150" cy="75" r="20" fill="{MER}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<circle cx="268" cy="54" r="15" fill="{ELEKTRON}" stroke="#13235E" stroke-width="3"/><path d="M261 54 H275" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>'
    s += _ok(236, 122, 190, 131, OBS, 4.6, 17)
    return s.cikti(f"0 0 {W} {H}", cls="mini", oz='data-tema-sabit=""')


def mini_bulut(onek="ag-mb"):
    s = Svg(onek)
    W, H = 300, 150
    r = RNG(21)
    g = s.rad([(0, "#2F5FCF", 1), (.4, "#5C8FE8", .7), (.75, "#8DB6F2", .3), (1, "#A9CBF7", 0)], 150, 75, 80, kull="userSpaceOnUse", ad="mb")
    s += f'<ellipse cx="150" cy="75" rx="140" ry="74" fill="{g}"/>'
    for _ in range(170):
        a = r.uniform(0, 2 * math.pi)
        d = abs(r.gauss(0, 24))
        if d < 66:
            s += f'<circle cx="{f(150 + d * 1.8 * math.cos(a))}" cy="{f(75 + d * math.sin(a))}" r="2.6" fill="#14296B" opacity=".6"/>'
    s += f'<circle cx="150" cy="75" r="11" fill="{MER}" stroke="{OBS}" stroke-width="2.6"/>'
    return s.cikti(f"0 0 {W} {H}", cls="mini", oz='data-tema-sabit=""')
