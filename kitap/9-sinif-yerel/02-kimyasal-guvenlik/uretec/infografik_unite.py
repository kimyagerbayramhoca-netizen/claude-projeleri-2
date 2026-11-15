"""Kimyasal Güvenlik · üniteye özel bilgi grafikleri ({{info|ad|arg…}} → ad(önek, *arg)).

Çizimler basitleştirilmiş ama tanınır: GHS piktogramı = beyaz zemin, kırmızı elmas çerçeve, siyah simge; güvenlik işaretleri
ISO 7010 renk/biçim dili (mavi daire zorunluluk, sarı üçgen uyarı, kırmızı çizgili daire yasak, yeşil kare acil durum,
kırmızı kare yangın ekipmanı). Adlar ve anlamlar guvenlik_veri.py'den okunur (dogrula.py aynı tabloyu kullanır).
Konturlu SVG yazısı yok; yazılar dolgulu (Nunito / Baloo); fontta olmayan sembol (✓ ✗ → ★) yerine path çizilir.
"""
import math
from cizim.temel import Svg, f, nok, cizgi_d, egri_d, karis, acik, koyu, yildiz_noktalari, halolu_yazi, rng as RNG
from cizim.renkler import OBS, GOL, GOL_K, GOL_A, KEH, KEH_K, KEH_A, MER, MER_K, MER_A, KOB, KOB_K, KOB_A, ZUMRUT, GUM, GUM_K, GUM_A
import guvenlik_veri as V

T = 'font-family="Nunito" font-weight="800"'
T9 = 'font-family="Nunito" font-weight="900"'
T7 = 'font-family="Nunito" font-weight="700"'
B = 'font-family="Baloo Bhaijaan 2" font-weight="800"'
KIRMIZI = "#E1251B"     # GHS / yasak kırmızısı
MAVI = "#1C5BA8"        # zorunluluk mavisi
SARI = "#F7C21A"        # uyarı sarısı
YESIL = "#1E8E4F"       # acil durum yeşili
SIYAH = "#15171C"


def _yazi(x, y, metin, boy, renk=OBS, hiza="middle", font=T):
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{hiza}" {font} font-size="{f(boy)}" fill="{renk}">{metin}</text>'


# ================================================================== GHS PİKTOGRAMLARI (0..100 koordinat)

def _alev(cx=50, taban=68, o=1.0, renk=SIYAH, ic="#FFFFFF"):
    """GHS alevi: dış alev + içte beyaz dil. taban: alevin oturduğu y."""
    def p(x, y):
        return f"{f(cx + (x - 50) * o, 2)} {f(taban + (y - 68) * o, 2)}"
    dis = (f"M{p(50, 22)} C{p(57, 31)} {p(66, 38)} {p(64, 51)} C{p(69, 47)} {p(70, 43)} {p(69, 39)} "
           f"C{p(77, 49)} {p(77, 62)} {p(70, 68)} L{p(30, 68)} C{p(23, 60)} {p(25, 48)} {p(33, 41)} "
           f"C{p(33, 47)} {p(36, 51)} {p(39, 52)} C{p(36, 41)} {p(42, 31)} {p(50, 22)} Z")
    icd = (f"M{p(51, 44)} C{p(55, 50)} {p(61, 54)} {p(59, 62)} C{p(57, 67)} {p(44, 67)} {p(42, 62)} "
           f"C{p(41, 57)} {p(45, 54)} {p(47, 52)} C{p(47, 56)} {p(49, 58)} {p(51, 57)} C{p(49, 53)} {p(49, 49)} {p(51, 44)} Z")
    return f'<path d="{dis}" fill="{renk}"/><path d="{icd}" fill="{ic}"/>'


def _ghs_simge(kod):
    k = SIYAH
    if kod == "GHS01":     # patlayan bomba
        pts = yildiz_noktalari(45, 58, 23, 14, 12, 0.2)
        o = f'<path d="{cizgi_d(pts, True)}" fill="{k}"/>'
        o += f'<circle cx="45" cy="58" r="12.5" fill="#FFFFFF"/><circle cx="45" cy="58" r="9.5" fill="{k}"/>'
        o += f'<path d="M45 49 Q50 40 58 37" stroke="{k}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        for (x, y, a) in ((66, 30, 20), (74, 44, -15), (58, 24, 55), (72, 60, 35)):
            o += f'<path d="M{x - 4} {y - 2} L{x + 4} {y - 4} L{x + 3} {y + 3} L{x - 3} {y + 3} Z" fill="{k}" transform="rotate({a} {x} {y})"/>'
        return o
    if kod == "GHS02":     # alev
        return _alev(50, 68) + f'<rect x="28" y="71" width="44" height="4.5" fill="{k}"/>'
    if kod == "GHS03":     # çember üstünde alev
        return (_alev(50, 54, .72) + f'<circle cx="50" cy="61" r="10" fill="none" stroke="{k}" stroke-width="5.4"/>'
                f'<rect x="31" y="74.5" width="38" height="4.5" fill="{k}"/>')
    if kod == "GHS04":     # gaz tüpü
        return (f'<g transform="rotate(-18 50 56)"><rect x="22" y="48" width="47" height="17" rx="8.5" fill="{k}"/>'
                f'<rect x="68" y="52.5" width="7" height="8" fill="{k}"/><rect x="74.5" y="49.5" width="5" height="14" rx="1.2" fill="{k}"/>'
                f'<path d="M28 52.5 h30" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity=".55"/></g>')
    if kod == "GHS05":     # aşınma: iki tüp, metal ve el
        o = ""
        for (cx, aci) in ((35, 42), (65, -42)):
            o += (f'<g transform="rotate({aci} {cx} 30)"><path d="M{cx - 4.5} 17 V36 A4.5 4.5 0 0 0 {cx + 4.5} 36 V17" fill="#FFFFFF" stroke="{k}" stroke-width="2.4"/>'
                  f'<path d="M{cx - 4.5} 29 V36 A4.5 4.5 0 0 0 {cx + 4.5} 36 V29 Z" fill="{k}"/></g>')
        o += f'<path d="M40 41 q1.6 3 0 4.6 q-1.6 -1.6 0 -4.6 Z M38 49 q1.6 3 0 4.6 q-1.6 -1.6 0 -4.6 Z" fill="{k}"/>'
        o += f'<path d="M60 41 q1.6 3 0 4.6 q-1.6 -1.6 0 -4.6 Z M62 49 q1.6 3 0 4.6 q-1.6 -1.6 0 -4.6 Z" fill="{k}"/>'
        o += f'<path d="M21 62 H44 V70 H21 Z" fill="{k}"/><circle cx="31" cy="62" r="2.8" fill="#FFFFFF"/><circle cx="38" cy="62" r="2" fill="#FFFFFF"/>'
        o += (f'<path d="M56 61 h13 q5 0 5 5 v3 q0 4 -5 4 h-13 q-3 0 -3 -3 v-6 q0 -3 3 -3 Z" fill="{k}"/>'
              f'<rect x="47" y="61.2" width="10" height="2.6" rx="1.3" fill="{k}"/><rect x="46" y="64.6" width="11" height="2.6" rx="1.3" fill="{k}"/>'
              f'<rect x="47" y="68" width="10" height="2.6" rx="1.3" fill="{k}"/><circle cx="63" cy="61" r="2.6" fill="#FFFFFF"/>')
        return o
    if kod == "GHS06":     # kurukafa ve çapraz kemik
        o = ""
        for (x1, y1, x2, y2) in ((31, 76, 69, 55), (31, 55, 69, 76)):
            o += f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{k}" stroke-width="5" stroke-linecap="round"/>'
            for (x, y) in ((x1, y1), (x2, y2)):
                o += f'<circle cx="{x - 1.6}" cy="{y - 1.6}" r="2.8" fill="{k}"/><circle cx="{x + 1.6}" cy="{y + 1.6}" r="2.8" fill="{k}"/>'
        o += f'<ellipse cx="50" cy="38" rx="14" ry="13" fill="{k}"/><rect x="42" y="45" width="16" height="11" rx="3" fill="{k}"/>'
        o += f'<circle cx="44.5" cy="38.5" r="4" fill="#FFFFFF"/><circle cx="55.5" cy="38.5" r="4" fill="#FFFFFF"/>'
        o += f'<path d="M50 44 L47.8 48 H52.2 Z" fill="#FFFFFF"/><path d="M45.5 52 v3.6 M50 52 v3.6 M54.5 52 v3.6" stroke="#FFFFFF" stroke-width="1.6"/>'
        return o
    if kod == "GHS07":     # ünlem
        return f'<path d="M45.5 23 H54.5 L52.4 59 H47.6 Z" fill="{k}"/><circle cx="50" cy="68" r="5" fill="{k}"/>'
    if kod == "GHS08":     # sağlık tehlikesi
        yil = yildiz_noktalari(50, 59, 11, 4.6, 8, -math.pi / 2)
        return (f'<circle cx="50" cy="27" r="7.4" fill="{k}"/>'
                f'<path d="M33 78 V53 C33 42 40 37.5 50 37.5 C60 37.5 67 42 67 53 V78 Z" fill="{k}"/>'
                f'<path d="{cizgi_d(yil, True)}" fill="#FFFFFF"/>')
    if kod == "GHS09":     # çevre: ölü ağaç ve balık
        o = f'<path d="M23 74 H77" stroke="{k}" stroke-width="3.2"/>'
        o += (f'<path d="M35 74 L37 40 M36.6 50 L28 41 M36.8 46 L45 35 M36.2 58 L43 51 M36.9 43 L33 33" stroke="{k}" stroke-width="3.4" '
              f'stroke-linecap="round" fill="none"/>')
        o += f'<path d="M50 63 Q60 54 70 63 Q60 70 50 63 Z" fill="{k}"/><path d="M69 63 L77 57 L77 69 Z" fill="{k}"/>'
        o += f'<circle cx="55" cy="62" r="1.8" fill="#FFFFFF"/><path d="M56 68 q2 2 4 0" stroke="{k}" stroke-width="1.5" fill="none"/>'
        return o
    raise KeyError(kod)


def ghs_g(kod, x=0, y=0, boy=100):
    """Sahnelerde kullanmak için: (x, y) sol üst, boy kenar uzunluğu."""
    k = boy / 100
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(k, 4)})"><path d="M50 3.5 L96.5 50 L50 96.5 L3.5 50 Z" fill="#FFFFFF" '
            f'stroke="{KIRMIZI}" stroke-width="7" stroke-linejoin="miter"/>{_ghs_simge(kod)}</g>')


def ghs(onek, kod, *_):
    """Tek GHS piktogramı. {{info|ghs|GHS05}}"""
    s = Svg(onek)
    s += ghs_g(kod)
    return s.cikti("0 0 100 100", cls="info ghs", oz=f'data-ghs="{kod}"')


# ================================================================== GÜVENLİK İŞARETLERİ (0..100)

def _isaret_simge(simge):
    b = "#FFFFFF"
    if simge == "baret":
        return (f'<path d="M27 61 C27 37 73 37 73 61 Z" fill="{b}"/><rect x="21" y="60" width="58" height="7" rx="3.5" fill="{b}"/>'
                f'<path d="M50 39 V60" stroke="{MAVI}" stroke-width="3"/><circle cx="50" cy="51" r="4.2" fill="{SARI}"/>')
    if simge == "gozluk":
        return (f'<rect x="24" y="43" width="23" height="16" rx="7" fill="{b}"/><rect x="53" y="43" width="23" height="16" rx="7" fill="{b}"/>'
                f'<path d="M46 50 Q50 46 54 50" stroke="{b}" stroke-width="4" fill="none"/><path d="M24 48 L15 45 M76 48 L85 45" stroke="{b}" stroke-width="4" stroke-linecap="round"/>'
                f'<path d="M29 47 q4 -2 8 0 M58 47 q4 -2 8 0" stroke="{MAVI}" stroke-width="2" fill="none" opacity=".7"/>')
    if simge == "eldiven":
        return (f'<path d="M37 76 V52 Q37 48 41 48 V31 Q41 27 44.5 27 Q48 27 48 31 V46 V27 Q48 23 51.5 23 Q55 23 55 27 V46 V30 Q55 26 58.5 26 '
                f'Q62 26 62 30 V48 V36 Q62 32 65.5 32 Q69 32 69 36 V60 Q69 70 61 76 Z" fill="{b}"/>'
                f'<path d="M37 56 L29 47 Q26 44 29 41 Q32 39 35 42 L41 50" fill="{b}"/><rect x="36" y="74" width="27" height="7" rx="2" fill="{b}"/>')
    if simge == "onluk":
        return (f'<path d="M35 25 L50 33 L65 25 L77 35 L72 47 L67 44 V80 H33 V44 L28 47 L23 35 Z" fill="{b}"/>'
                f'<path d="M50 33 V80 M42 28 L50 45 L58 28" stroke="{MAVI}" stroke-width="2.6" fill="none"/>'
                f'<circle cx="54" cy="53" r="1.8" fill="{MAVI}"/><circle cx="54" cy="63" r="1.8" fill="{MAVI}"/>')
    k = SIYAH
    if simge == "elektrik":
        return f'<path d="M54 30 L40 60 H50 L45 80 L62 50 H52 L58 30 Z" fill="{k}"/>'
    if simge == "sicak":
        o = f'<rect x="28" y="70" width="44" height="6" fill="{k}"/>'
        for x in (37, 50, 63):
            o += f'<path d="M{x} 66 q-5 -6 0 -11 q5 -5 0 -11 q-4 -4 0 -9" stroke="{k}" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
        return o
    if simge == "yanici":
        return _alev(50, 74, .55) + f'<rect x="37" y="76" width="26" height="3.4" fill="{k}"/>'
    if simge == "alev_yok":
        return _alev(50, 76, .78)
    if simge == "sigara_yok":
        return (f'<rect x="24" y="56" width="44" height="9" fill="{k}"/><rect x="68" y="56" width="8" height="9" fill="#C77A2E"/>'
                f'<path d="M30 52 q-4 -6 0 -11 q4 -5 0 -10 M38 50 q-4 -6 0 -11" stroke="{k}" stroke-width="2.6" fill="none"/>')
    if simge == "yeme_yok":
        return (f'<path d="M30 40 H58 V64 Q58 74 48 74 H40 Q30 74 30 64 Z" fill="{k}"/><path d="M58 46 Q68 46 68 54 Q68 61 58 61" stroke="{k}" stroke-width="4" fill="none"/>'
                f'<path d="M37 34 q-3 -4 0 -8 M45 34 q-3 -4 0 -8" stroke="{k}" stroke-width="2.4" fill="none"/>')
    if simge == "ilkyardim":
        return f'<path d="M42 24 H58 V42 H76 V58 H58 V76 H42 V58 H24 V42 H42 Z" fill="#FFFFFF"/>'
    if simge == "gozdusu":
        return (f'<path d="M20 60 Q50 38 80 60 Q50 82 20 60 Z" fill="#FFFFFF"/><circle cx="50" cy="60" r="9" fill="{YESIL}"/><circle cx="50" cy="60" r="4" fill="#FFFFFF"/>'
                + "".join(f'<path d="M{x} {y} q3.4 5.5 0 8 q-3.4 -2.5 0 -8 Z" fill="#FFFFFF"/>' for (x, y) in ((38, 24), (50, 20), (62, 24), (44, 35), (56, 35))))
    if simge == "sondurucu":
        return (f'<rect x="40" y="38" width="20" height="44" rx="7" fill="#FFFFFF"/><rect x="45" y="30" width="10" height="9" fill="#FFFFFF"/>'
                f'<path d="M50 30 L65 24 L67 30" stroke="#FFFFFF" stroke-width="3.4" fill="none"/>'
                f'<path d="M60 44 Q72 50 70 66" stroke="#FFFFFF" stroke-width="3" fill="none"/>')
    raise KeyError(simge)


def isaret_g(simge, x=0, y=0, boy=100):
    aile = V.ISARET[simge][0]
    k = boy / 100
    if aile == "zor":
        cer = f'<circle cx="50" cy="50" r="46" fill="{MAVI}"/><circle cx="50" cy="50" r="42.5" fill="none" stroke="#FFFFFF" stroke-width="2"/>'
        ust = ""
    elif aile == "uya":
        cer = f'<path d="M50 9 L93 86 H7 Z" fill="{SARI}" stroke="{SIYAH}" stroke-width="6" stroke-linejoin="round"/>'
        ust = ""
    elif aile == "yas":
        cer = f'<circle cx="50" cy="50" r="41" fill="#FFFFFF"/>'
        ust = f'<circle cx="50" cy="50" r="41" fill="none" stroke="{KIRMIZI}" stroke-width="9"/><path d="M21 21 L79 79" stroke="{KIRMIZI}" stroke-width="9"/>'
    elif aile == "acil":
        cer = f'<rect x="5" y="5" width="90" height="90" rx="8" fill="{YESIL}"/>'
        ust = ""
    else:
        cer = f'<rect x="5" y="5" width="90" height="90" rx="8" fill="{KIRMIZI}"/>'
        ust = ""
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(k, 4)})">{cer}{_isaret_simge(simge)}{ust}</g>'


def isaret(onek, simge, *_):
    """Tek güvenlik işareti. {{info|isaret|baret}}"""
    s = Svg(onek)
    s += isaret_g(simge)
    return s.cikti("0 0 100 100", cls="info isaret", oz=f'data-isaret="{simge}"')


# ================================================================== CAM MALZEMELER

def _cam(s):
    return s.lin([(0, "#FFFFFF", .95), (.45, "#E2F4F6", .75), (1, "#AFD4DC", .9)], 0, 0, 1, 0, ad="cam")


def _olcu(x, y0, y1, n, uz=12, sag=True, k=2.2):
    o = ""
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n
        L = uz * (1.6 if i % 5 == 0 else 1)
        o += f'<path d="M{f(x)} {f(y)} h{f(L if sag else -L)}" stroke="{OBS}" stroke-width="{k}"/>'
    return o


def cam_parca(s, tur, x, y, o=1.0, sivi=GOL):
    """Cam malzeme: (x, y) taban ortası. o ölçek. Yükseklikler o=1'de ≈ 300 birim."""
    cam = _cam(s)
    st = f'stroke="{OBS}" stroke-width="{f(4 / max(o, .4) * o)}"'
    g = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">']
    if tur == "tup":
        g.append(f'<rect x="-46" y="-118" width="92" height="22" rx="6" fill="#C9955E" {st}/><path d="M-36 -96 V0 M36 -96 V0" stroke="{OBS}" stroke-width="5"/>')
        g.append(f'<path d="M-15 -270 V-30 A15 15 0 0 0 15 -30 V-270" fill="{cam}" {st}/>')
        g.append(f'<path d="M-13 -100 V-30 A13 13 0 0 0 13 -30 V-100 Z" fill="{sivi}" opacity=".85"/>')
        g.append(f'<path d="M-20 -272 h40" {st} stroke-linecap="round"/>')
    elif tur == "beher":
        g.append(f'<path d="M-62 -190 L-70 -200 L-56 -198 L58 -198 L58 -8 Q58 0 50 0 L-54 0 Q-62 0 -62 -8 Z" fill="{cam}" {st} stroke-linejoin="round"/>')
        g.append(f'<path d="M-58 -88 H54 V-8 Q54 -4 50 -4 H-54 Q-58 -4 -58 -8 Z" fill="{sivi}" opacity=".85"/>')
        g.append(_olcu(30, -160, -40, 3, 14, True, 3))
    elif tur == "erlen":
        g.append(f'<path d="M-18 -270 V-190 L-70 -14 Q-72 0 -58 0 H58 Q72 0 70 -14 L18 -190 V-270" fill="{cam}" {st} stroke-linejoin="round"/>')
        g.append(f'<path d="M-46 -82 H46 L66 -14 Q67 -4 58 -4 H-58 Q-67 -4 -66 -14 Z" fill="{sivi}" opacity=".85"/>')
        g.append(f'<path d="M-24 -272 h48" {st} stroke-linecap="round"/>')
    elif tur == "balon":
        g.append(f'<ellipse cx="0" cy="-8" rx="44" ry="12" fill="#C9955E" {st}/>')
        g.append(f'<path d="M-16 -280 V-150 A62 62 0 1 0 16 -150 V-280" fill="{cam}" {st}/>')
        g.append(f'<path d="M-60 -78 A62 62 0 0 0 60 -78 Z" fill="{sivi}" opacity=".85"/>')
        g.append(f'<path d="M-22 -282 h44" {st} stroke-linecap="round"/>')
    elif tur == "joje":
        g.append(f'<path d="M-10 -300 V-130 C-34 -122 -62 -96 -62 -54 Q-62 0 -44 0 H44 Q62 0 62 -54 C62 -96 34 -122 10 -130 V-300" fill="{cam}" {st}/>')
        g.append(f'<path d="M-58 -62 C-58 -88 -36 -112 -8 -120 H8 C36 -112 58 -88 58 -62 Q58 -4 44 -4 H-44 Q-58 -4 -58 -62 Z" fill="{sivi}" opacity=".85"/>')
        g.append(f'<path d="M-12 -238 h24" stroke="{MER}" stroke-width="5"/><rect x="-14" y="-326" width="28" height="28" rx="6" fill="{GUM}" {st}/>')
    elif tur == "mezur":
        g.append(f'<path d="M-50 0 L50 0 L36 -20 H-36 Z" fill="#8FA3AD" {st} stroke-linejoin="round"/>')
        g.append(f'<path d="M-24 -300 L-30 -306 H24 V-20 H-24 Z" fill="{cam}" {st} stroke-linejoin="round"/>')
        g.append(f'<path d="M-22 -150 Q0 -140 22 -150 V-22 H-22 Z" fill="{sivi}" opacity=".85"/>')
        g.append(_olcu(4, -290, -40, 10, 10, True, 2.6))
    elif tur == "pipet":
        g.append(f'<path d="M-5 -10 V-120 C-26 -126 -26 -170 -5 -176 V-262" fill="none" {st}/>')
        g.append(f'<path d="M5 -10 V-120 C26 -126 26 -170 5 -176 V-262" fill="none" {st}/>')
        g.append(f'<path d="M-5 -120 C-26 -126 -26 -170 -5 -176 H5 C26 -170 26 -126 5 -120 Z" fill="{cam}"/>')
        g.append(f'<path d="M-3 -12 V-118 C-20 -126 -20 -146 -12 -150 H12 C20 -146 20 -126 3 -118 V-12 Z" fill="{sivi}" opacity=".85"/>')
        g.append(f'<path d="M-9 -222 h18" stroke="{MER}" stroke-width="5"/><path d="M-5 0 L0 8 L5 0" fill="none" {st}/>')
        g.append(f'<path d="M-8 -262 C-34 -270 -40 -300 -26 -318 C-14 -334 14 -334 26 -318 C40 -300 34 -270 8 -262 Z" fill="{MER}" {st}/>')
        g.append(f'<circle cx="0" cy="-300" r="7" fill="{MER_K}"/><circle cx="-16" cy="-282" r="5" fill="{MER_K}"/><circle cx="16" cy="-282" r="5" fill="{MER_K}"/>')
    elif tur == "buret":
        g.append(f'<rect x="-46" y="-12" width="92" height="12" rx="3" fill="#8FA3AD" {st}/><path d="M-30 -12 V-330" stroke="#6E7F8A" stroke-width="8"/>')
        g.append(f'<rect x="-6" y="-336" width="22" height="270" fill="{cam}" {st}/>')
        g.append(f'<rect x="-4" y="-260" width="18" height="192" fill="{sivi}" opacity=".85"/>')
        g.append(_olcu(16, -326, -80, 8, 8, False, 2.2))
        g.append(f'<path d="M5 -66 V-36" {st}/><rect x="-10" y="-56" width="30" height="10" rx="3" fill="{KEH}" {st}/><path d="M5 -36 v12" {st}/>')
        g.append(f'<path d="M-30 -230 H-4" stroke="#6E7F8A" stroke-width="7"/>')
    g.append("</g>")
    return "".join(g)


def _alev_isareti(x, y, r, izin):
    """Küçük rozet: ısıtılır (kehribar daire içinde alev) / ısıtılmaz (beyaz daire, kırmızı çizgi)."""
    k = r / 50
    if izin:
        return (f'<g transform="translate({f(x - r)} {f(y - r)}) scale({f(k, 4)})"><circle cx="50" cy="50" r="48" fill="{KEH}" stroke="{OBS}" stroke-width="5"/>'
                f'{_alev(50, 76, .62, OBS, KEH)}</g>')
    return (f'<g transform="translate({f(x - r)} {f(y - r)}) scale({f(k, 4)})"><circle cx="50" cy="50" r="46" fill="#FFFFFF"/>{_alev(50, 76, .62, OBS)}'
            f'<circle cx="50" cy="50" r="44" fill="none" stroke="{KIRMIZI}" stroke-width="9"/><path d="M19 19 L81 81" stroke="{KIRMIZI}" stroke-width="9"/></g>')


def cam_takimi(onek):
    """Sekiz cam malzeme, iki panelde: ısıtılabilir kaplar | hacim ölçenler (ısıtılmaz) + duyarlılık şeridi."""
    s = Svg(onek)
    W, H = 2000, 600
    renkler = [GOL, KEH, "#7FD3CF", MER, KOB, GOL, "#F2A88A", KEH]
    s += f'<rect x="4" y="4" width="986" height="592" rx="26" fill="#FFF4DD" stroke="{OBS}" stroke-width="5"/>'
    s += f'<rect x="1010" y="4" width="986" height="592" rx="26" fill="#E6ECFB" stroke="{OBS}" stroke-width="5"/>'
    s += _alev_isareti(56, 54, 30, True) + _yazi(100, 66, "ISITILABİLİR KAPLAR · tutar, karıştırır, ısıtır", 32, KEH_K, "start", T9)
    s += _alev_isareti(1062, 54, 30, False) + _yazi(1106, 66, "HACİM ÖLÇENLER · ısıtılmaz", 32, KOB_K, "start", T9)
    taban = 440
    for i, (kod, ad, isit, duy, is_) in enumerate(V.CAM):
        x = 130 + i * 245 + (24 if i >= 4 else 0)
        s += f'<ellipse cx="{x}" cy="{taban + 4}" rx="80" ry="10" fill="{OBS}" opacity=".12"/>'
        s += cam_parca(s, kod, x, taban, .98 if kod not in ("buret", "joje", "pipet") else .9, renkler[i])
        s += _yazi(x, taban + 58, ad, 34, OBS, "middle", T9)
        s += _yazi(x, taban + 94, is_, 25, "#343947", "middle", T7)
        if duy:
            r = {"hassas": (KOB, "#FFFFFF", "HASSAS"), "orta": (GUM_A, OBS, "ORTA"), "yaklaşık": ("#FFFFFF", OBS, "YAKLAŞIK")}[duy]
            w = 34 + len(r[2]) * 17
            s += f'<rect x="{f(x - w / 2)}" y="{taban + 112}" width="{f(w)}" height="36" rx="18" fill="{r[0]}" stroke="{OBS}" stroke-width="3"/>'
            s += _yazi(x, taban + 138, r[2], 23, r[1], "middle", T9)
    return s.cikti(f"0 0 {W} {H}", cls="info cam-takimi")


def ekipman_parca(s, tur, x, y, o=1.0):
    """Yardımcı malzemeler; (x, y) taban ortası; o=1'de ≈ 200 birim yükseklik."""
    cam = _cam(s)
    st = f'stroke="{OBS}" stroke-width="4"'
    g = [f'<g transform="translate({f(x)} {f(y)}) scale({f(o, 3)})">']
    if tur == "huni":
        g.append(f'<path d="M-70 -200 H70 L10 -110 V-10 H-10 V-110 Z" fill="{cam}" {st} stroke-linejoin="round"/>')
        g.append(f'<path d="M-56 -194 H56 L0 -120 Z" fill="#FFFFFF" stroke="{GUM_K}" stroke-width="3"/><path d="M-30 -194 L0 -120 L18 -194" fill="none" stroke="{GUM}" stroke-width="2"/>')
    elif tur == "ayirma":
        g.append(f'<path d="M-8 -210 V-196 C-50 -170 -58 -110 -30 -84 L-8 -66 V-30 H8 V-66 L30 -84 C58 -110 50 -170 8 -196 V-210" fill="{cam}" {st}/>')
        g.append(f'<path d="M-46 -126 C-48 -110 -42 -96 -30 -84 L-8 -66 H8 L30 -84 C42 -96 48 -110 46 -126 Z" fill="{KOB}" opacity=".8"/>')
        g.append(f'<path d="M-48 -126 H48 C48 -150 40 -166 26 -178 H-26 C-40 -166 -48 -150 -48 -126 Z" fill="{KEH}" opacity=".8"/>')
        g.append(f'<rect x="-18" y="-52" width="36" height="12" rx="4" fill="{KEH}" {st}/><path d="M0 -30 V-6" {st}/><rect x="-12" y="-222" width="24" height="14" rx="4" fill="{GUM}" {st}/>')
    elif tur == "sogutucu":
        g.append(f'<g transform="rotate(-28 0 -100)"><rect x="-26" y="-210" width="52" height="210" rx="20" fill="{GOL_A}" {st}/>'
                 f'<rect x="-8" y="-250" width="16" height="290" fill="{cam}" {st}/><path d="M26 -180 h26 M-26 -30 h-26" stroke="{OBS}" stroke-width="10"/>'
                 f'<path d="M26 -180 h24 M-26 -30 h-24" stroke="{GOL_A}" stroke-width="5"/></g>')
    elif tur == "piset":
        g.append(f'<path d="M-40 -10 V-130 Q-40 -150 -20 -152 H20 Q40 -150 40 -130 V-10 Q40 0 30 0 H-30 Q-40 0 -40 -10 Z" fill="#EAF6FF" {st}/>')
        g.append(f'<rect x="-14" y="-170" width="28" height="20" rx="4" fill="{KOB}" {st}/><path d="M0 -170 V-210 Q0 -222 14 -226 L50 -238" stroke="{OBS}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                 f'<path d="M0 -170 V-210 Q0 -222 14 -226 L50 -238" stroke="#EAF6FF" stroke-width="4" fill="none" stroke-linecap="round"/>')
        g.append(f'<path d="M-36 -70 H36 V-10 Q36 -4 30 -4 H-30 Q-36 -4 -36 -10 Z" fill="#9FD9E6" opacity=".85"/>')
    elif tur == "damlalik":
        g.append(f'<path d="M-9 -150 V-30 L0 -6 L9 -30 V-150" fill="{cam}" {st}/><path d="M-7 -70 V-30 L0 -12 L7 -30 V-70 Z" fill="{MER}" opacity=".8"/>')
        g.append(f'<path d="M-16 -150 C-22 -184 -16 -214 0 -216 C16 -214 22 -184 16 -150 Z" fill="{MER}" {st}/><path d="M0 4 q6 9 0 13 q-6 -4 0 -13 Z" fill="{MER}"/>')
    elif tur == "termometre":
        g.append(f'<rect x="-10" y="-230" width="20" height="200" rx="10" fill="{cam}" {st}/><circle cx="0" cy="-22" r="18" fill="{MER}" {st}/>')
        g.append(f'<rect x="-4" y="-140" width="8" height="110" fill="{MER}"/>' + _olcu(10, -210, -50, 8, 8, True, 2))
    elif tur == "spor":
        g.append(f'<rect x="-80" y="-18" width="160" height="18" rx="4" fill="#5A6B76" {st}/><rect x="-46" y="-240" width="12" height="222" fill="#8FA3AD" {st}/>')
        g.append(f'<rect x="-52" y="-176" width="24" height="24" rx="3" fill="#5A6B76" {st}/><path d="M-28 -164 H40" stroke="{OBS}" stroke-width="12"/><path d="M-28 -164 H40" stroke="#B8C3CC" stroke-width="6"/>')
        g.append(f'<path d="M40 -180 Q64 -180 64 -164 Q64 -148 40 -148" fill="none" stroke="{OBS}" stroke-width="8"/>')
    elif tur == "havan":
        g.append(f'<path d="M-66 -86 H66 Q62 -20 30 -10 H-30 Q-62 -20 -66 -86 Z" fill="#FBFBF7" {st}/><rect x="-36" y="-12" width="72" height="12" rx="4" fill="#E9E6DC" {st}/>')
        g.append(f'<path d="M-6 -96 L50 -186" stroke="{OBS}" stroke-width="22" stroke-linecap="round"/><path d="M-6 -96 L50 -186" stroke="#FBFBF7" stroke-width="14" stroke-linecap="round"/>')
        g.append(f'<ellipse cx="0" cy="-86" rx="66" ry="12" fill="#E1DED3" {st}/>')
    elif tur == "spatul":
        g.append(f'<path d="M-6 -20 L-10 -200 Q0 -216 10 -200 L6 -20 Q0 -4 -6 -20 Z" fill="#C9D3DB" {st}/><rect x="-8" y="-130" width="16" height="70" rx="4" fill="#5A6B76"/>')
    elif tur == "baget":
        g.append(f'<rect x="-8" y="-220" width="16" height="220" rx="8" fill="{cam}" {st} transform="rotate(14 0 -110)"/>')
    elif tur == "saatcami":
        g.append(f'<path d="M-76 -40 Q0 0 76 -40 Q0 -12 -76 -40 Z" fill="{cam}" {st}/><path d="M-30 -30 Q0 -20 30 -30" stroke="{KEH}" stroke-width="10" stroke-linecap="round"/>')
    elif tur == "kroze":
        g.append(f'<path d="M-46 -90 H46 L32 -6 Q30 0 22 0 H-22 Q-30 0 -32 -6 Z" fill="#FBFBF7" {st}/><ellipse cx="0" cy="-92" rx="50" ry="9" fill="#E9E6DC" {st}/>')
        g.append(f'<path d="M-52 -108 Q0 -128 52 -108 Z" fill="#FBFBF7" {st}/><circle cx="0" cy="-124" r="8" fill="#FBFBF7" {st}/>')
    elif tur == "bek":
        alev = s.lin([(0, "#BFE6FF"), (1, "#2B50B5")], 0, 0, 0, 1, ad="be")
        g.append(f'<path d="M0 -330 C14 -300 18 -268 0 -240 C-18 -268 -14 -300 0 -330 Z" fill="{alev}" opacity=".9"/><path d="M0 -300 C6 -284 6 -266 0 -252 C-6 -266 -6 -284 0 -300 Z" fill="#E6F6FF"/>')
        g.append(f'<rect x="-11" y="-240" width="22" height="200" fill="#8FA3AD" {st}/><rect x="-14" y="-110" width="28" height="22" rx="3" fill="{KEH}" {st}/>')
        g.append(f'<path d="M-60 -10 Q-60 -40 0 -40 Q60 -40 60 -10 V0 H-60 Z" fill="#5A6B76" {st}/><path d="M40 -26 H96" stroke="{OBS}" stroke-width="12"/><path d="M40 -26 H96" stroke="{MER}" stroke-width="6"/>')
    elif tur == "ispirto":
        g.append(f'<path d="M0 -224 C10 -206 12 -186 0 -170 C-12 -186 -10 -206 0 -224 Z" fill="{KEH}"/><path d="M0 -208 C4 -198 4 -188 0 -180 C-4 -188 -4 -198 0 -208 Z" fill="#FFF0CF"/>')
        g.append(f'<rect x="-4" y="-172" width="8" height="26" fill="#FFFFFF" {st}/><rect x="-16" y="-148" width="32" height="22" rx="4" fill="{GUM}" {st}/>')
        g.append(f'<path d="M-14 -126 C-70 -116 -76 -60 -66 -20 Q-62 0 -40 0 H40 Q62 0 66 -20 C76 -60 70 -116 14 -126 Z" fill="{cam}" {st}/>')
        g.append(f'<path d="M-68 -58 H68 C68 -40 66 -26 62 -18 Q58 -4 40 -4 H-40 Q-58 -4 -62 -18 C-66 -26 -68 -40 -68 -58 Z" fill="#B9A6E8" opacity=".75"/>')
    elif tur == "sacayak":
        g.append(f'<path d="M-70 0 L-50 -170 M70 0 L50 -170 M0 -10 L0 -170" stroke="#5A6B76" stroke-width="12" stroke-linecap="round"/>')
        g.append(f'<rect x="-84" y="-184" width="168" height="16" rx="4" fill="#8FA3AD" {st}/>')
        for k in range(9):
            g.append(f'<path d="M{-74 + k * 18} -184 v16" stroke="{OBS}" stroke-width="1.6"/>')
        g.append(f'<circle cx="0" cy="-176" r="26" fill="#E9E6DC" opacity=".9"/>')
        g.append(f'<g transform="translate(0 -186) scale(.62)">' + cam_parca(s, "beher", 0, 0, 1, GOL) + "</g>")
    elif tur == "masa":
        g.append(f'<g transform="rotate(-32 0 -120)"><path d="M-6 -20 L-6 -170 L-18 -230 M6 -20 L6 -170 L18 -230" stroke="#9A6B42" stroke-width="10" fill="none" stroke-linecap="round"/>'
                 f'<path d="M-6 -60 L6 -60" stroke="{OBS}" stroke-width="4"/>'
                 f'<path d="M-30 -240 H30" stroke="{OBS}" stroke-width="4"/>'
                 f'<path d="M-14 -300 V-232 A14 14 0 0 0 14 -232 V-300" fill="{cam}" {st}/><path d="M-12 -254 V-232 A12 12 0 0 0 12 -232 V-254 Z" fill="{KEH}" opacity=".9"/></g>')
    g.append("</g>")
    return "".join(g)


def ekipman(onek):
    """On iki yardımcı malzeme, iki sıra; altında ad ve kısa görev."""
    s = Svg(onek)
    W, H = 2000, 640
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="26" fill="#EEF9F8" stroke="{OBS}" stroke-width="5"/>'
    for i, (kod, ad, is_) in enumerate(V.EKIPMAN):
        sira, sut = divmod(i, 6)
        x = 170 + sut * 332
        y = 230 + sira * 304
        s += f'<ellipse cx="{x}" cy="{y + 4}" rx="76" ry="9" fill="{OBS}" opacity=".1"/>'
        s += ekipman_parca(s, kod, x, y, .78 if kod in ("spor", "termometre", "spatul", "baget", "ayirma") else .82)
        s += _yazi(x, y + 44, ad, 32, OBS, "middle", T9)
        s += _yazi(x, y + 76, is_, 25, "#343947", "middle", T7)
    return s.cikti(f"0 0 {W} {H}", cls="info ekipman")


def isitma(onek):
    """Isıtma takımı: bunzen beki, ispirto ocağı, sacayağı + tel kafes (üstünde beher), tüp maşası."""
    s = Svg(onek)
    W, H = 1240, 470
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="24" fill="#FFF4DD" stroke="{OBS}" stroke-width="5"/>'
    xs = [170, 470, 790, 1080]
    for i, (kod, ad, is_) in enumerate(V.ISITMA):
        x = xs[i]
        y = 362
        s += f'<ellipse cx="{x}" cy="{y + 4}" rx="80" ry="9" fill="{OBS}" opacity=".1"/>'
        s += ekipman_parca(s, kod, x, y, .9 if kod != "sacayak" else .95)
        s += _yazi(x, y + 44, ad, 32, OBS, "middle", T9)
        s += _yazi(x, y + 76, is_, 25, "#343947", "middle", T7)
    return s.cikti(f"0 0 {W} {H}", cls="info isitma")


# ================================================================== MEZÜR OKUMA · MENİSKÜS

def mezur(onek, deger=V.MEZUR_OKUMA, *_):
    """İmtihan sorusu: 30–40 mL arası büyütülmüş mezür; çukurun alt noktası `deger` mL."""
    s = Svg(onek)
    W, H = 300, 560
    x0, x1 = 90, 210
    ust, alt = 40, 520                 # 40 mL → y=40 · 30 mL → y=520 (her mL 48 birim)
    def yy(v):
        return alt - (v - 30) * 48
    cam = _cam(s)
    su = s.lin([(0, "#7FD3CF"), (1, "#13A3A6")], 0, 0, 0, 1, ad="su")
    s += f'<rect x="{x0}" y="10" width="{x1 - x0}" height="{H - 10}" fill="{cam}" stroke="{OBS}" stroke-width="5"/>'
    yd = yy(deger)
    kenar = yd - 34
    s += (f'<path d="M{x0 + 3} {f(kenar)} Q{x0 + 14} {f(yd - 2)} {(x0 + x1) / 2} {f(yd)} Q{x1 - 14} {f(yd - 2)} {x1 - 3} {f(kenar)} V{H} H{x0 + 3} Z" fill="{su}" opacity=".9"/>')
    for v in range(30, 41):
        y = yy(v)
        L = 46 if v % 5 == 0 else 26
        s += f'<path d="M{x0} {y} h{L}" stroke="{OBS}" stroke-width="{4 if v % 5 == 0 else 3}"/>'
        if v % 5 == 0:
            s += _yazi(x0 - 12, y + 12, str(v), 38, OBS, "end", B)
    s += _yazi(x1 + 14, 52, "mL", 30, OBS, "start", T9)
    # göz (hizada)
    s += f'<path d="M232 {f(yd - 4)} Q256 {f(yd - 24)} 282 {f(yd - 4)} Q256 {f(yd + 16)} 232 {f(yd - 4)} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/><circle cx="252" cy="{f(yd - 4)}" r="7" fill="{OBS}"/>'
    s += f'<path d="M230 {f(yd - 4)} H{(x0 + x1) / 2}" stroke="{OBS}" stroke-width="2.4" stroke-dasharray="7 6"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info mezur")


def meniskus(onek):
    """Su: çukur menisküs, alt nokta · cıva: tümsek, üst nokta · göz hizası (yukarıdan fazla, aşağıdan az)."""
    s = Svg(onek)
    W, H = 1000, 560
    cam = _cam(s)
    su = s.lin([(0, "#7FD3CF"), (1, "#13A3A6")], 0, 0, 0, 1, ad="su")
    civa = s.lin([(0, "#E6EBEF"), (.5, "#A3B3BE"), (1, "#586874")], 0, 0, 1, 0, ad="cv")
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="24" fill="#FFFFFF" stroke="{OBS}" stroke-width="4"/>'
    # su sütunu
    x0, x1, y = 300, 460, 250
    s += f'<rect x="{x0}" y="70" width="{x1 - x0}" height="440" fill="{cam}" stroke="{OBS}" stroke-width="5"/>'
    s += f'<path d="M{x0 + 3} {y - 40} Q{x0 + 20} {y} {(x0 + x1) / 2} {y} Q{x1 - 20} {y} {x1 - 3} {y - 40} V508 H{x0 + 3} Z" fill="{su}" opacity=".9"/>'
    for i in range(9):
        yy = 110 + i * 45
        s += f'<path d="M{x0} {yy} h{40 if i % 2 == 0 else 24}" stroke="{OBS}" stroke-width="3"/>'
    # gözler ve bakış çizgileri
    for (gy, renk, et, hiza) in ((110, MER_K, "yukarıdan: fazla okunur", -1), (y, ZUMRUT, "göz hizası: doğru", 0), (390, MER_K, "aşağıdan: az okunur", 1)):
        s += f'<path d="M150 {gy} Q178 {gy - 22} 206 {gy} Q178 {gy + 22} 150 {gy} Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="3.4"/><circle cx="182" cy="{gy}" r="9" fill="{OBS}"/>'
        s += f'<path d="M210 {gy} L{(x0 + x1) / 2} {y}" stroke="{renk}" stroke-width="3.4" stroke-dasharray="{"" if hiza == 0 else "10 8"}"/>'
        s += _yazi(24, gy + 52 if hiza >= 0 else gy - 34, et, 30, renk, "start", T9)
    s += f'<circle cx="{(x0 + x1) / 2}" cy="{y}" r="9" fill="{ZUMRUT}" stroke="{OBS}" stroke-width="3"/>'
    s += _yazi((x0 + x1) / 2, 50, "SU", 36, GOL_K, "middle", T9)
    s += _yazi((x0 + x1) / 2, 548, "çukurun dibi okunur", 28, OBS, "middle", T9)
    # cıva sütunu
    x0, x1, y = 690, 850, 250
    s += f'<rect x="{x0}" y="70" width="{x1 - x0}" height="440" fill="{cam}" stroke="{OBS}" stroke-width="5"/>'
    s += f'<path d="M{x0 + 3} {y + 34} Q{x0 + 20} {y} {(x0 + x1) / 2} {y} Q{x1 - 20} {y} {x1 - 3} {y + 34} V508 H{x0 + 3} Z" fill="{civa}"/>'
    s += f'<path d="M{x0 + 30} {y + 30} Q{x0 + 50} {y + 14} {x0 + 70} {y + 12}" stroke="#FFFFFF" stroke-width="6" fill="none" opacity=".7"/>'
    s += f'<path d="M{x0 - 40} {y} H{x1 + 40}" stroke="{ZUMRUT}" stroke-width="3.4"/><circle cx="{(x0 + x1) / 2}" cy="{y}" r="9" fill="{ZUMRUT}" stroke="{OBS}" stroke-width="3"/>'
    s += _yazi((x0 + x1) / 2, 50, "CIVA", 36, GUM_K, "middle", T9)
    s += _yazi((x0 + x1) / 2, 548, "tümseğin tepesi okunur", 28, OBS, "middle", T9)
    return s.cikti(f"0 0 {W} {H}", cls="info meniskus")


# ================================================================== ETİKET · DEPOLAMA · ATIK

def _rakam(x, y, n, r=22):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{KEH}" stroke="{OBS}" stroke-width="4"/>'
            + _yazi(x, y + r * .42, str(n), r * 1.25, OBS, "middle", B))


def etiket_aseton(onek):
    """Temsilî etiket (aseton · oje çıkarıcıda da bulunur): 1 ürün adı · 2 uyarı kelimesi · 3 piktogram · 4 H · 5 P · 6 tedarikçi."""
    s = Svg(onek)
    W, H = 1060, 640
    s += f'<rect x="40" y="20" width="980" height="600" rx="22" fill="#FFFFFF" stroke="{OBS}" stroke-width="6"/>'
    s += f'<rect x="40" y="20" width="980" height="96" rx="22" fill="{GOL_A}" stroke="{OBS}" stroke-width="6"/><rect x="43" y="90" width="974" height="26" fill="{GOL_A}"/>'
    s += _yazi(90, 88, "ASETON", 62, OBS, "start", B) + _yazi(372, 86, "(propan-2-on) · 1 L", 34, "#343947", "start", T)
    s += _rakam(60, 40, 1)
    s += ghs_g("GHS02", 74, 140, 200) + ghs_g("GHS07", 270, 140, 200) + _rakam(60, 150, 3)
    s += f'<rect x="500" y="150" width="270" height="78" rx="12" fill="{MER_A}" stroke="{MER_K}" stroke-width="4"/>'
    s += _yazi(635, 206, "TEHLİKE", 54, MER_K, "middle", B) + _rakam(796, 190, 2)
    s += _yazi(500, 270, "Kolay alevlenir sıvı ve buhar.", 30, OBS, "start", T9)
    s += _yazi(500, 308, "Ciddi göz tahrişine yol açar.", 30, OBS, "start", T9)
    s += _yazi(500, 346, "Rehavete ya da baş dönmesine", 30, OBS, "start", T9)
    s += _yazi(500, 382, "yol açabilir.", 30, OBS, "start", T9) + _rakam(996, 300, 4)
    s += f'<path d="M80 410 H990" stroke="{GUM}" stroke-width="3" stroke-dasharray="10 8"/>'
    for i, t in enumerate(("Isıdan, kıvılcımdan, açık alevden uzak tutun. Sigara içilmez.", "Kabı sıkıca kapalı tutun.",
                           "Göz koruması kullanın.")):
        s += _yazi(80, 456 + i * 38, t, 29, "#343947", "start", T)
    s += _rakam(996, 474, 5)
    s += f'<path d="M80 560 H990" stroke="{GUM}" stroke-width="3"/>'
    s += _yazi(80, 600, "Tedarikçi: Örnek Kimya · Tel: 0 000 000 00 00", 27, "#56636E", "start", T) + _rakam(996, 590, 6)
    return s.cikti(f"0 0 {W} {H}", cls="info etiket")


def _hucre_isaret(x, y, v, r=26):
    if v == "+":
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#DFF3E8" stroke="{ZUMRUT}" stroke-width="3"/>'
                f'<path d="M{x - 12} {y + 1} L{x - 3} {y + 11} L{x + 14} {y - 10}" stroke="{ZUMRUT}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if v == "x":
        return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{MER_A}" stroke="{MER_K}" stroke-width="3"/>'
                f'<path d="M{x - 10} {y - 10} L{x + 10} {y + 10} M{x + 10} {y - 10} L{x - 10} {y + 10}" stroke="{MER_K}" stroke-width="7" stroke-linecap="round"/>')
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{KEH_A}" stroke="{KEH_K}" stroke-width="3"/>'
            + _yazi(x, y + 15, "!", 44, KEH_K, "middle", B))


def depo_matrisi(onek):
    """Sadeleştirilmiş depolama matrisi (guvenlik_veri.MATRIS): ✓ birlikte · ✗ ayrı · ! yalnızca özel önlemle."""
    s = Svg(onek)
    W, H = 880, 700
    hx, hy, c, r = 250, 150, 124, 104
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="24" fill="#FFFFFF" stroke="{OBS}" stroke-width="4"/>'
    for i, a in enumerate(V.SINIF):
        x = hx + i * c + c / 2
        s += ghs_g(V.SINIF_GHS[a], x - 34, 22, 68)
        s += _yazi(x, 128, V.SINIF_AD[a] if a != "T" else "Tahriş", 25, OBS, "middle", T9)
        y = hy + i * r + r / 2
        s += ghs_g(V.SINIF_GHS[a], 26, y - 30, 60)
        s += _yazi(96, y + 9, V.SINIF_AD[a] if a != "T" else "Tahriş ed.", 27, OBS, "start", T9)
        for j, b in enumerate(V.SINIF):
            xx = hx + j * c + c / 2
            zemin = "#F7FAFB" if (i + j) % 2 else "#FFFFFF"
            s += f'<rect x="{hx + j * c}" y="{hy + i * r}" width="{c}" height="{r}" fill="{zemin}" stroke="{GUM}" stroke-width="2"/>'
            s += _hucre_isaret(xx, y, V.MATRIS[a][b])
    s += f'<rect x="{hx}" y="{hy}" width="{c * 5}" height="{r * 5}" fill="none" stroke="{OBS}" stroke-width="4"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info depo-matrisi")


def _kutu(s, x, y, w, h, govde, kapak, yazi=None):
    """Atık kutusu: (x, y) taban sol."""
    o = f'<path d="M{x + 8} {y} L{x} {y - h} H{x + w} L{x + w - 8} {y} Z" fill="{govde}" stroke="{OBS}" stroke-width="4" stroke-linejoin="round"/>'
    o += f'<rect x="{x - 10}" y="{y - h - 26}" width="{w + 20}" height="26" rx="8" fill="{kapak}" stroke="{OBS}" stroke-width="4"/>'
    o += f'<rect x="{x + w / 2 - 24}" y="{y - h - 36}" width="48" height="12" rx="5" fill="{kapak}" stroke="{OBS}" stroke-width="3"/>'
    for k in range(3):
        o += f'<path d="M{x + w * (.3 + .2 * k)} {y - h + 20} V{y - 18}" stroke="{OBS}" stroke-width="2.4" opacity=".25"/>'
    return o


def atik_semasi(onek):
    """Atık nereye? Lavabo DEĞİL · altı kutu ve örnekleri (guvenlik_veri.ATIK)."""
    s = Svg(onek)
    W, H = 2000, 560
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="26" fill="#FFFFFF" stroke="{OBS}" stroke-width="5"/>'
    # lavabo (yasak)
    s += f'<path d="M60 250 H240 Q236 330 150 336 Q64 330 60 250 Z" fill="#E6EBEF" stroke="{OBS}" stroke-width="5"/><path d="M150 250 V196 Q150 176 176 176 H200" stroke="{OBS}" stroke-width="12" fill="none"/>'
    s += f'<path d="M150 250 V196 Q150 176 176 176 H200" stroke="#B8C3CC" stroke-width="6" fill="none"/><path d="M196 186 v14" stroke="#B8C3CC" stroke-width="8"/>'
    s += f'<circle cx="150" cy="262" r="96" fill="none" stroke="{KIRMIZI}" stroke-width="14"/><path d="M82 194 L218 330" stroke="{KIRMIZI}" stroke-width="14"/>'
    s += _yazi(150, 418, "Lavaboya değil!", 32, MER_K, "middle", T9)
    s += _yazi(150, 456, "seyreltmek de", 25, "#343947", "middle", T7) + _yazi(150, 484, "zararsız yapmaz", 25, "#343947", "middle", T7)
    renk = {"kimyasal": ("#FFE08A", KEH), "cam": ("#D9EEF2", GOL), "tibbi": ("#FFC9C2", KIRMIZI), "pil": ("#C9D3DB", "#56636E"),
            "yag": ("#FFE3B8", "#C8742F"), "ambalaj": ("#DCE6FA", KOB)}
    for i, (kod, ad, ornek) in enumerate(V.ATIK):
        x = 330 + i * 278
        govde, kapak = renk[kod]
        s += _kutu(s, x, 380, 190, 150, govde, kapak)
        cx = x + 95
        # kutunun üstünde küçük nesne + ok
        if kod == "kimyasal":
            s += f'<g transform="translate({cx} 300) scale(.55)">' + cam_parca(s, "erlen", 0, 0, .8, "#3A8CF2") + "</g>"
        elif kod == "cam":
            s += f'<path d="M{cx - 40} 296 L{cx - 6} 236 L{cx + 2} 290 Z M{cx + 6} 298 L{cx + 30} 250 L{cx + 44} 296 Z" fill="{GOL_A}" stroke="{OBS}" stroke-width="3.4"/>'
        elif kod == "tibbi":
            s += (f'<g transform="rotate(-30 {cx} 270)"><rect x="{cx - 50}" y="258" width="76" height="22" rx="4" fill="#FFFFFF" stroke="{OBS}" stroke-width="3.4"/>'
                  f'<path d="M{cx + 26} 269 h34" stroke="{OBS}" stroke-width="3"/><path d="M{cx - 50} 269 h-20" stroke="{OBS}" stroke-width="7"/>'
                  f'<rect x="{cx - 40}" y="262" width="40" height="14" fill="{MER}" opacity=".6"/></g>')
        elif kod == "pil":
            s += (f'<rect x="{cx - 20}" y="232" width="40" height="70" rx="6" fill="{KEH}" stroke="{OBS}" stroke-width="3.4"/>'
                  f'<rect x="{cx - 8}" y="224" width="16" height="9" fill="#C9D3DB" stroke="{OBS}" stroke-width="3"/><rect x="{cx - 18}" y="268" width="36" height="32" fill="{OBS}" opacity=".85"/>')
        elif kod == "yag":
            s += (f'<path d="M{cx - 26} 302 V248 Q{cx - 26} 236 {cx - 12} 232 V218 H{cx + 12} V232 Q{cx + 26} 236 {cx + 26} 248 V302 Z" fill="#F2C94A" stroke="{OBS}" stroke-width="3.4"/>'
                  f'<rect x="{cx - 14}" y="210" width="28" height="10" fill="#C8742F" stroke="{OBS}" stroke-width="3"/>')
        else:
            s += (f'<path d="M{cx - 28} 302 V244 Q{cx - 28} 232 {cx - 14} 228 L{cx - 10} 212 H{cx + 10} L{cx + 14} 228 Q{cx + 28} 232 {cx + 28} 244 V302 Z" fill="#DCE6FA" stroke="{OBS}" stroke-width="3.4"/>'
                  f'<path d="M{cx - 16} 258 H{cx + 16}" stroke="{KOB}" stroke-width="6"/>')
        satirlar = ad.split(" (")
        s += _yazi(cx, 432, satirlar[0], 29, OBS, "middle", T9)
        if len(satirlar) > 1:
            s += _yazi(cx, 464, "(" + satirlar[1], 25, MER_K if kod == "tibbi" else "#343947", "middle", T)
            dy = 30
        else:
            dy = 0
        for j, o_ in enumerate(ornek[:1]):
            parca = o_.split(", ")
            for k_, p in enumerate(parca[:2]):
                s += _yazi(cx, 466 + dy + k_ * 30, p + ("," if k_ == 0 and len(parca) > 1 else ""), 24, "#343947", "middle", T7)
    return s.cikti(f"0 0 {W} {H}", cls="info atik")


# ================================================================== KÜÇÜK ŞEKİLLER (görev, kıssa, üstad)

def asit_su(onek):
    """Doğru: asit, bagetle suya azar azar · Yanlış: az su derişik asidin üstüne → sıçrama."""
    s = Svg(onek)
    W, H = 760, 430
    cam = _cam(s)
    for (x, dogru) in ((190, True), (570, False)):
        zemin = "#E8F6EE" if dogru else MER_A
        s += f'<rect x="{x - 176}" y="8" width="352" height="414" rx="22" fill="{zemin}" stroke="{OBS}" stroke-width="4"/>'
        s += f'<path d="M{x - 80} 168 L{x - 88} 158 L{x - 74} 160 L{x + 78} 160 L{x + 78} 352 Q{x + 78} 360 {x + 70} 360 L{x - 72} 360 Q{x - 80} 360 {x - 80} 352 Z" fill="{cam}" stroke="{OBS}" stroke-width="5"/>'
        if dogru:
            s += f'<path d="M{x - 76} 220 H{x + 74} V352 Q{x + 74} 356 {x + 70} 356 H{x - 72} Q{x - 76} 356 {x - 76} 352 Z" fill="#9FD9E6" opacity=".9"/>'
            s += f'<path d="M{x + 40} 60 L{x + 6} 300" stroke="{OBS}" stroke-width="9" stroke-linecap="round"/><path d="M{x + 40} 60 L{x + 6} 300" stroke="#E2F4F6" stroke-width="4" stroke-linecap="round"/>'
            s += f'<g transform="rotate(-50 {x + 70} 80)"><rect x="{x + 40}" y="20" width="56" height="96" rx="10" fill="{cam}" stroke="{OBS}" stroke-width="4"/><rect x="{x + 43}" y="70" width="50" height="43" rx="6" fill="{KEH}"/></g>'
            s += f'<path d="M{x + 30} 128 Q{x + 34} 140 {x + 28} 150" stroke="{KEH}" stroke-width="5" fill="none"/>'
            s += (f'<circle cx="{x + 130}" cy="200" r="30" fill="{ZUMRUT}" stroke="{OBS}" stroke-width="4"/>'
                  f'<path d="M{x + 116} 201 L{x + 127} 213 L{x + 145} 189" stroke="#FFFFFF" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
            s += _yazi(x, 400, "asit suya, yavaşça", 30, ZUMRUT, "middle", T9)
        else:
            s += f'<path d="M{x - 76} 250 H{x + 74} V352 Q{x + 74} 356 {x + 70} 356 H{x - 72} Q{x - 76} 356 {x - 76} 352 Z" fill="{KEH}" opacity=".9"/>'
            s += f'<g transform="rotate(50 {x - 70} 80)"><rect x="{x - 96}" y="20" width="56" height="96" rx="10" fill="{cam}" stroke="{OBS}" stroke-width="4"/><rect x="{x - 93}" y="70" width="50" height="43" rx="6" fill="#9FD9E6"/></g>'
            for (dx, dy, rr) in ((-40, 210, 12), (-10, 180, 9), (24, 196, 11), (52, 170, 8), (-60, 170, 7), (6, 150, 6)):
                s += f'<circle cx="{x + dx}" cy="{dy}" r="{rr}" fill="{KEH}" stroke="{OBS}" stroke-width="2.4"/>'
            s += f'<path d="M{x - 30} 140 q-10 -20 0 -40 M{x + 10} 130 q-10 -20 0 -40 M{x + 50} 140 q-10 -20 0 -40" stroke="{GUM}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            s += (f'<circle cx="{x + 130}" cy="200" r="30" fill="{MER}" stroke="{OBS}" stroke-width="4"/>'
                  f'<path d="M{x + 118} 188 L{x + 142} 212 M{x + 142} 188 L{x + 118} 212" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>')
            s += _yazi(x, 400, "su asidin üstüne: sıçrar", 30, MER_K, "middle", T9)
    return s.cikti(f"0 0 {W} {H}", cls="info asit-su")


def _eksenler(s, x0, y0, x1, y1, xs, ys, xet, yet):
    o = f'<path d="M{x0} {y1} V{y0} H{x1}" stroke="{OBS}" stroke-width="4" fill="none"/>'
    for (v, px) in xs:
        o += f'<path d="M{px} {y0} v10" stroke="{OBS}" stroke-width="3"/>' + _yazi(px, y0 + 40, v, 26, OBS, "middle", T)
    for (v, py) in ys:
        o += f'<path d="M{x0} {py} h-10" stroke="{OBS}" stroke-width="3"/><path d="M{x0} {py} H{x1}" stroke="{GUM}" stroke-width="1.6" stroke-dasharray="6 6"/>'
        o += _yazi(x0 - 16, py + 9, v, 26, OBS, "end", T)
    o += _yazi(x1, y0 + 74, xet, 26, "#343947", "end", T9) + _yazi(x0 - 4, y1 - 18, yet, 26, "#343947", "start", T9)
    return o


def kaza_grafigi(onek):
    """Kıssa: iki dönemde kaza sayıları (guvenlik_veri.KAZA_GRAFIK)."""
    s = Svg(onek)
    W, H = 820, 560
    x0, y0, x1, y1 = 110, 440, 800, 70
    ust = 12
    sy = (y0 - y1 - 20) / ust
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="20" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    s += _eksenler(s, x0, y0, x1, y1, [], [(str(v), y0 - v * sy) for v in range(0, ust + 1, 2)], "", "kaza sayısı")
    for i, (ad, (a, b)) in enumerate(V.KAZA_GRAFIK.items()):
        cx = x0 + 90 + i * 172
        for k, (v, renk) in enumerate(((a, "#A3B3BE"), (b, GOL))):
            x = cx - 46 + k * 50
            s += f'<rect x="{x}" y="{f(y0 - v * sy)}" width="44" height="{f(v * sy)}" fill="{renk}" stroke="{OBS}" stroke-width="3"/>'
            s += _yazi(x + 22, y0 - v * sy - 10, str(v), 26, OBS, "middle", B)
        s += _yazi(cx, y0 + 38, ad, 25, OBS, "middle", T9)
    s += f'<rect x="460" y="22" width="28" height="22" fill="#A3B3BE" stroke="{OBS}" stroke-width="3"/>' + _yazi(496, 41, "1. dönem", 25, OBS, "start", T9)
    s += f'<rect x="630" y="22" width="28" height="22" fill="{GOL}" stroke="{OBS}" stroke-width="3"/>' + _yazi(666, 41, "2. dönem", 25, OBS, "start", T9)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik kaza-grafik")


def co_grafigi(onek):
    """Üstad: sobalı odada CO derişimi (ppm) — zaman (dk); kesikli çizgi dedektör eşiği, ok pencerenin açıldığı an."""
    s = Svg(onek)
    W, H = 760, 520
    x0, y0, x1, y1 = 110, 420, 730, 60
    tmax, pmax = 70, 120
    def p(t, v):
        return (x0 + (x1 - x0 - 20) * t / tmax, y0 - (y0 - y1 - 20) * v / pmax)
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="20" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    s += _eksenler(s, x0, y0, x1, y1, [(str(t), p(t, 0)[0]) for t in range(0, 71, 10)], [(str(v), p(0, v)[1]) for v in range(0, 121, 20)],
                   "zaman (dk)", "CO (ppm)")
    ye = p(0, V.CO_ESIK)[1]
    s += f'<path d="M{x0} {f(ye)} H{x1 - 20}" stroke="{MER}" stroke-width="4" stroke-dasharray="14 9"/>' + _yazi(x1 - 22, ye - 12, "dedektör eşiği", 25, MER_K, "end", T9)
    pts = [p(t, v) for t, v in V.CO_GRAFIK]
    s += f'<path d="{cizgi_d(pts)}" stroke="{KOB}" stroke-width="6" fill="none" stroke-linejoin="round"/>'
    for (x, y) in pts:
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="7" fill="#FFFFFF" stroke="{KOB}" stroke-width="4"/>'
    xp = p(V.CO_PENCERE, 0)[0]
    s += f'<path d="M{f(xp)} {y0} V{y1 + 30}" stroke="{ZUMRUT}" stroke-width="3" stroke-dasharray="6 6"/>'
    s += _yazi(xp + 8, y1 + 22, "pencere açıldı", 25, ZUMRUT, "start", T9)
    return s.cikti(f"0 0 {W} {H}", cls="info grafik co-grafik")


def damitma(onek, hatali=1, *_):
    """Basit damıtma düzeneği. hatali=1: Üstad sorusu (II: su üstten giriyor, III: toplama kabı tıpalı) · 0: doğru düzenek."""
    s = Svg(onek)
    W, H = 980, 560
    cam = _cam(s)
    s += f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="22" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/>'
    # ısıtıcı + sacayağı
    s += ekipman_parca(s, "bek", 170, 520, .55)
    # cam balon + termometre
    s += f'<path d="M156 160 V250 A62 62 0 1 0 184 250 V160" fill="{cam}" stroke="{OBS}" stroke-width="5"/>'
    s += f'<path d="M112 322 A62 62 0 0 0 228 322 Z" fill="{KEH}" opacity=".75"/>'
    s += f'<path d="M184 196 L330 250" stroke="{OBS}" stroke-width="18" stroke-linecap="round"/><path d="M184 196 L330 250" stroke="#E2F4F6" stroke-width="9" stroke-linecap="round"/>'
    s += f'<rect x="164" y="60" width="12" height="148" rx="6" fill="#FFFFFF" stroke="{OBS}" stroke-width="3"/><circle cx="170" cy="204" r="9" fill="{MER}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<rect x="150" y="146" width="40" height="18" rx="4" fill="{GUM_K}"/>'
    # soğutucu (eğik)
    ax, ay, bx, by = 330, 250, 720, 392
    s += f'<path d="M{ax} {ay} L{bx} {by}" stroke="{OBS}" stroke-width="64" stroke-linecap="round"/><path d="M{ax} {ay} L{bx} {by}" stroke="{GOL_A}" stroke-width="54" stroke-linecap="round"/>'
    s += f'<path d="M{ax - 20} {ay - 7} L{bx + 40} {by + 15}" stroke="{OBS}" stroke-width="16"/><path d="M{ax - 20} {ay - 7} L{bx + 40} {by + 15}" stroke="#F4FBFC" stroke-width="8"/>'
    ust_n, alt_n = (400, 260), (660, 356)   # su bağlantıları
    giris, cikis = (ust_n, alt_n) if hatali else (alt_n, ust_n)
    s += f'<path d="M{ust_n[0]} {ust_n[1] - 20} v-60" stroke="{OBS}" stroke-width="12"/><path d="M{alt_n[0]} {alt_n[1] + 26} v60" stroke="{OBS}" stroke-width="12"/>'
    s += _yazi(giris[0] + 18, giris[1] - (70 if giris == ust_n else -96), "su girer", 26, KOB_K, "start", T9)
    s += _yazi(cikis[0] + 18, cikis[1] - (70 if cikis == ust_n else -96), "su çıkar", 26, KOB_K, "start", T9)
    # toplama erleni
    ex, ey = 800, 520
    s += cam_parca(s, "erlen", ex, ey, .62, "#9FD9E6")
    if hatali:
        s += f'<rect x="{ex - 20}" y="{ey - 182}" width="40" height="22" rx="4" fill="{GUM_K}" stroke="{OBS}" stroke-width="3"/>'
    # etiketler I II III
    for (x, y, et) in ((214, 150, "I"), (ust_n[0] - 54, ust_n[1] - 64, "II"), (ex + 52, ey - 196, "III")):
        s += f'<circle cx="{x}" cy="{y}" r="24" fill="{KEH}" stroke="{OBS}" stroke-width="3.4"/>' + _yazi(x, y + 10, et, 26, OBS, "middle", B)
    return s.cikti(f"0 0 {W} {H}", cls="info damitma")


def metan_seridi(onek):
    """Metanın havadaki hacim yüzdesi: ≈ %5–15 tutuşabilir aralık; ölçer ve havalandırma derişimi bu aralığın çok altında tutar."""
    s = Svg(onek)
    W, H = 1000, 250
    x0, x1, y = 40, 960, 100
    def px(v):
        return x0 + (x1 - x0) * v / 20
    a, b = V.METAN_ARALIK
    g = s.lin([(0, "#BFEBD3"), (1, "#E3F6EC")], 0, 0, 1, 0, ad="gv")
    s += f'<rect x="{x0}" y="{y}" width="{f(px(a) - x0)}" height="56" fill="{g}" stroke="{OBS}" stroke-width="3"/>'
    s += f'<rect x="{f(px(a))}" y="{y}" width="{f(px(b) - px(a))}" height="56" fill="#FFC9C2" stroke="{OBS}" stroke-width="3"/>'
    s += f'<rect x="{f(px(b))}" y="{y}" width="{f(x1 - px(b))}" height="56" fill="#E6EBEF" stroke="{OBS}" stroke-width="3"/>'
    for v in range(0, 21, 5):
        s += f'<path d="M{f(px(v))} {y + 56} v12" stroke="{OBS}" stroke-width="3"/>' + _yazi(px(v), y + 98, f"%{v}", 28, OBS, "middle", T9)
    s += _yazi((px(a) + px(b)) / 2, y + 38, "tutuşabilir aralık", 30, MER_K, "middle", T9)
    s += _yazi((x0 + px(a)) / 2, y + 38, "seyreltilmiş", 26, ZUMRUT, "middle", T9)
    s += _yazi((px(b) + x1) / 2, y + 38, "O₂ azalır", 26, GUM_K, "middle", T9)
    s += _yazi(x0, 62, "havalandırma + ölçer: derişim hep en solda tutulur", 28, OBS, "start", T9)
    s += f'<path d="M{f(px(a) - 20)} 80 H{x0 + 40}" stroke="{ZUMRUT}" stroke-width="6" marker-end=""/><path d="M{x0 + 54} 70 L{x0 + 36} 80 L{x0 + 54} 90 Z" fill="{ZUMRUT}"/>'
    return s.cikti(f"0 0 {W} {H}", cls="info metan")
