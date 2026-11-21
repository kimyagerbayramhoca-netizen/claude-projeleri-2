"""Atom ve Yapısı · yeni düzen çizimleri ({{info|ad}}; infografik_unite bunları kendi ad alanına alır).

Kaynak: gelistirme/atom-modelleri/uretec/infografik_gelistirme.py (oradaki dosya değişmedi; buraya kopyalandı ve 9/03'e bağlandı).
  zincir_yolu                 Model Zinciri'nin arkasındaki yol (s.2)
  pano_duzenek … pano_sonuc   altın levha çizgi romanının 6 panosu (s.4; yazılar HTML'de)
  enerji_merdiveni            Bohr: n = 1…6 basamakları, soğurma/yayma, görünür dört çizgi (s.6)
  mini_yorunge / mini_bulut   Tuzak! ikili kartının küçük resimleri (s.5)
  tekne_iskelesi              Halfeti teknesi: orbital tekneleri, ₇N'nin elektronları (s.12)
  dis_katman                  Dış katman konuşuyor: ₁₂Mg'nin değerlik elektronları (s.15)
Sayılar dogrula.py'de yeniden hesaplanır. Dalga boyu renkleri data-tema-sabit içindedir (palet fiziksel rengi değiştirmez).
SVG yazısında kontur yok; ⁺ ⁻ tspan ile; font adları tırnaklı.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, acik, koyu, rng as RNG
from cizim.renkler import (OBS, GOL, GOL_K, GOL_A, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A, ALTIN, ALTIN_K,
                           GUM, GUM_K, GUM_A, ZUMRUT)
from cizim import konu_karakterleri as KK

T = 'font-family="Nunito" font-weight="800"'
T9 = 'font-family="Nunito" font-weight="900"'
B = 'font-family="\'Baloo Bhaijaan 2\'" font-weight="800"'
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


# ------------------------------------------------------------------ 5. DURAK · HALFETİ TEKNESİ (konu karakterleri)
# Orbital = tekne, elektron = yolcu. ₇N: 1s² 2s² 2p³ (dogrula.py dizilim motoruyla denetler). Yalnız su ve tekne çizilir.
TEKNE = [("1s", ("u", "d")), ("2s", ("u", "d")), ("2p", ("u",)), ("2p", ("u",)), ("2p", ("u",))]
TEKNE_YANLIS = [("u", "d"), ("u",), ()]          # Hund'a aykırı 2p³


def _spin(cx, y, yukari, k=6, renk=OBS):
    """Spin oku (çizgi; fonttaki ↑↓'ya bağlı değil). y: okun orta noktası."""
    y0, y1 = (y + 18, y - 18) if yukari else (y - 18, y + 18)
    u = -1 if yukari else 1
    return (f'<path d="M{f(cx)} {f(y0)} V{f(y1 - u * 6)}" stroke="{renk}" stroke-width="{k}" stroke-linecap="round"/>'
            f'<path d="M{f(cx - 10)} {f(y1 - u * 11)} L{f(cx)} {f(y1)} L{f(cx + 10)} {f(y1 - u * 11)}" fill="none" stroke="{renk}" '
            f'stroke-width="{k}" stroke-linecap="round" stroke-linejoin="round"/>')


def _govde(x0, x1, y, etiket, h=64):
    """Tekne gövdesi (yamuk) + ad."""
    return (f'<path d="M{f(x0)} {f(y)} H{f(x1)} L{f(x1 - 28)} {f(y + h)} H{f(x0 + 28)} Z" fill="#9A6B42" stroke="{OBS}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{f(x0 + 10)} {f(y + 16)} H{f(x1 - 10)}" stroke="#C98E55" stroke-width="8" stroke-linecap="round"/>'
            f'<text x="{f((x0 + x1) / 2)}" y="{f(y + 52)}" text-anchor="middle" {B} font-size="34" fill="#FFFFFF">{etiket}</text>')


def tekne_iskelesi(onek="ay-ti"):
    """Halfeti teknesi: enerji sırasıyla tekneler (orbitaller), ₇N'nin 7 elektronu yolcu; sağda Hund'a aykırı küçük örnek."""
    s = Svg(onek)
    W, H = 1880, 560
    su = s.lin([(0, "#D7F2F1"), (1, "#8FD3D6")], 0, 0, 0, 1, ad="su")
    s += f'<rect x="380" y="402" width="1120" height="128" rx="26" fill="{su}"/>'
    for k in range(5):
        s += f'<path d="M{410 + k * 220} {478 + (k % 2) * 18} q40 -12 80 0 t80 0" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
    # sol: kimlik
    s += _alt("_7N", 40, 150, 96, OBS, "start", B)
    s += _alt("1s^{2} 2s^{2} 2p^{3}", 40, 232, 44, KOB_K, "start", B)
    s += f'<text x="40" y="284" {T} font-size="29" fill="{OBS}">7 elektron · 5 tekne</text>'
    s += f'<text x="40" y="324" {T} font-size="26" fill="#5A6470">tekne = orbital</text>'
    s += f'<text x="40" y="358" {T} font-size="26" fill="#5A6470">yolcu = elektron</text>'
    # tekneler
    xs = [400, 622, 866, 1072, 1278]
    for (ad, yolcu), x0 in zip(TEKNE, xs):
        x1 = x0 + 196
        s += _govde(x0, x1, 392, ad)
        for j, sp in enumerate(yolcu):
            cx = x0 + 58 + j * 80
            s += KK.kullan("kk-elektron-sakin", cx - 36, 318, 72)
            s += _spin(cx, 276, sp == "u")
    s += f'<path d="M866 382 C960 366 1380 366 1474 382" fill="none" stroke="{KEH_K}" stroke-width="5" stroke-dasharray="12 9"/>'
    s += f'<text x="1170" y="236" text-anchor="middle" {T} font-size="27" fill="{KEH_K}">eş enerjili üç tekne</text>'
    # kurallar
    s += f'<text x="400" y="200" {T9} font-size="27" fill="{GOL_K}">Pauli: teknede en çok iki yolcu,</text>'
    s += f'<text x="400" y="234" {T9} font-size="27" fill="{GOL_K}">yönleri zıt</text>'
    s += f'<text x="1170" y="200" text-anchor="middle" {T9} font-size="27" fill="{GOL_K}">Hund: önce her tekneye bir yolcu</text>'
    s += _ok(400, 548, 1490, 548, OBS, 5, 18)
    s += f'<text x="945" y="538" text-anchor="middle" {T} font-size="26" fill="{OBS}">Aufbau: önce düşük enerjili tekne · enerji sağa doğru artar</text>'
    # sağ: yanlış örnek
    s += f'<rect x="1530" y="120" width="340" height="396" rx="22" fill="#FFFFFF" stroke="{MER}" stroke-width="4" stroke-dasharray="14 10"/>'
    s += f'<text x="1700" y="176" text-anchor="middle" {B} font-size="38" fill="{MER_K}">Yanlış</text>'
    for k, yolcu in enumerate(TEKNE_YANLIS):
        x0 = 1550 + k * 104
        s += (f'<path d="M{x0} 290 H{x0 + 96} L{x0 + 82} 328 H{x0 + 14} Z" fill="#9A6B42" stroke="{OBS}" stroke-width="3.4" stroke-linejoin="round"/>'
              f'<text x="{x0 + 48}" y="318" text-anchor="middle" {B} font-size="22" fill="#FFFFFF">2p</text>')
        for j, sp in enumerate(yolcu):
            s += _spin(x0 + 30 + j * 36, 254, sp == "u", 5)
    s += f'<path d="M1772 222 L1846 296 M1846 222 L1772 296" stroke="{MER}" stroke-width="9" stroke-linecap="round"/>'
    s += f'<text x="1700" y="400" text-anchor="middle" {T} font-size="27" fill="{OBS}">Boş tekne varken</text>'
    s += f'<text x="1700" y="436" text-anchor="middle" {T} font-size="27" fill="{OBS}">eşleşme olmaz.</text>'
    s += f'<text x="1700" y="486" text-anchor="middle" {T9} font-size="25" fill="{MER_K}">Hund kuralına aykırı</text>'
    return s.cikti(f"0 0 {W} {H}", cls="info tekne")


# ------------------------------------------------------------------ 6. DURAK · DIŞ KATMAN KONUŞUYOR (konu karakterleri)
DIS_KATMAN = ("Mg", 12, 12, (2, 8, 2))          # sembol, p, n, katman elektronları (dogrula: dizilim(12) → 2 · 8 · 2)


def dis_katman(onek="ay-dk"):
    """₁₂Mg'nin Bohr çizimi: iç katmanlar küçük nokta, dış katmanın iki elektronu konu karakteri."""
    s = Svg(onek)
    W, H = 760, 520
    sembol, p, n, katman = DIS_KATMAN
    cx, cy = 400, 262
    R = (92, 152, 214)
    for r in R:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#8FA6B2" stroke-width="4"/>'
    g = s.rad([(0, "#FF9A86"), (1, MER)], .38, .32, .75, ad="ck")
    s += f'<circle cx="{cx}" cy="{cy}" r="50" fill="{g}" stroke="{OBS}" stroke-width="3.4"/>'
    s += f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" {B} font-size="34" fill="#FFFFFF">{p} p</text>'
    s += f'<text x="{cx}" y="{cy + 28}" text-anchor="middle" {T9} font-size="24" fill="#FFFFFF">{n} n</text>'
    for r, sayi in zip(R[:2], katman[:2]):
        for k in range(sayi):
            a = math.radians(90 + 360 * k / sayi + (22.5 if sayi == 8 else 0))
            x, y = cx + r * math.cos(a), cy - r * math.sin(a)
            s += (f'<circle cx="{f(x)}" cy="{f(y)}" r="12" fill="{ELEKTRON}" stroke="#13235E" stroke-width="2.4"/>'
                  f'<path d="M{f(x - 5.5)} {f(y)} H{f(x + 5.5)}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>')
    for a in (30, 210):
        r = math.radians(a)
        x, y = cx + R[2] * math.cos(r), cy - R[2] * math.sin(r)
        s += KK.kullan("kk-elektron-heyecan", x - 42, y - 42, 84)
    for j, (r, ad, sayi) in enumerate(zip(R, "KLM", katman)):
        s += f'<text x="22" y="{60 + j * 46}" {T9} font-size="30" fill="{OBS}">{ad} {sayi}</text>'
    s += _alt("_12Mg: [Ne] 3s^{2}", 22, 500, 30, OBS, "start", B)
    return s.cikti(f"0 0 {W} {H}", cls="info diskatman")
