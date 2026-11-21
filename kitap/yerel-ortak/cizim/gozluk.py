"""3B gözlük sayfası ve 3B ikonları · SVG çizimleri (ORTAK; kaynak: gelistirme/uc-boyut/uretec/sahneler_uc.py).

Kırmızı / camgöbeği taşıyan her çizim data-tema-sabit ile işaretlidir (palet eşlemesi gözlük renklerine dokunmaz).
Anaglifin yanında renk yok kuralı: 3B kartlarındaki ikonlar (ub_ikon) nötr gridir; renk yalnız gözlük sayfasındadır.

Yer tutucularla (kur_ortak):
  {{gozluk-sayfasi|n}}          bütün gözlük sayfası (bant, nasıl çalışır, kesme şablonu, yapılış, kullanım, test kartı)
  {{sahne|bant_atolye}}         gözlük sayfasının sahne bandı (30 mm: .bant.b30)
  {{info|nasil_calisir}}        üstten bakış şeması · {{info|gozluk_sablonu}} gerçek ölçüde kesme şablonu (188 mm)
  {{ub-ikon|ad}} ya da {{info|ub_ikon|ad}}   nötr 3B ikonları: gozluk cetvel duz saat damla goz
"""
from cizim.temel import Svg, f, koyu, rng as RNG
from cizim.renkler import OBS

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
        o.append(f'<text x="{x0 + 220}" y="176" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="74" fill="{OBS}">{ad}</text>')
        o.append(f'<text x="{x0 + 220}" y="242" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="56" fill="{koyu(renk, .38)}">{alt}</text>')
        o.append(f'<text x="{x0 + 220}" y="296" text-anchor="middle" {YAZI} font-size="29" fill="{GRI_K}">{"(mavi-yeşil) · kes, çıkar" if s > 0 else "pencereyi kes, çıkar"}</text>')
        fx = cx + s * 680                                   # katlama çizgisi + yapıştırma kulağı
        o.append(f'<path d="M{fx} 10 V370" stroke="{OBS}" stroke-width="2.6" stroke-dasharray="5 9"/>')
        o.append(f'<text transform="translate({fx + s * 56} 190) rotate({-90 * s})" text-anchor="middle" {YAZI} font-size="27" fill="{GRI_K}">KATLA · SAP BURAYA</text>')
    o.append(f'<text x="{cx}" y="50" text-anchor="middle" {YAZI} font-size="28" letter-spacing="2" fill="{GRI_K}">İÇ YÜZ · BU YÜZ SANA BAKSIN</text>')
    o.append(f'<text x="{cx}" y="226" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="34" fill="{OBS}">Kimya</text>'
             f'<text x="{cx}" y="260" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="34" fill="{OBS}">Rotası</text>')
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
        o.append(f'<text x="620" y="{y + 92}" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="50" fill="{GRI}" letter-spacing="6">{ad}</text>')
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
