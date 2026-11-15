#!/usr/bin/env python3
"""Kur: uretec/sablon.html + koddan üretilen illüstrasyonlar → unite.html (+ gorsel/ebru-*.jpg).

Çalıştır (ünite klasöründen ya da herhangi bir yerden):
    python3 uretec/kur.py            # unite.html'i kurar (ebru dokuları yoksa üretir)
    python3 uretec/kur.py --ebru     # ebru dokularını da yeniden üretir
Sonra: node uretec/render.js         # PDF + onizleme/sNN.png + taşma denetimi

Şablondaki yer tutucular  {{ad|arg1|arg2…}}  biçimindedir; aşağıdaki YT sözlüğü hangisinin ne ürettiğini gösterir.
"""
import os
import re
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
UNITE = os.path.dirname(BURA)
ORTAK = os.path.normpath(os.path.join(BURA, "..", "..", "..", "yerel-ortak"))
sys.path.insert(0, ORTAK)
sys.path.insert(0, BURA)

from cizim.temel import Svg, f, cizgi_d, selcuklu_yildizi            # noqa: E402
from cizim import sahneler as SH, karakter as K, sus as U, molekul as M, infografik as I, ebru as E  # noqa: E402
from cizim.renkler import GOL, GOL_K, KEH, MER, KOB, ALTIN, OBS, ERGUVAN  # noqa: E402

# ------------------------------------------------------------------ sayfa künyesi (HUD + altbilgi)
# bar: o sayfanın başına kadar alınabilecek en çok akçenin 1400'e oranı (%)
SAYFA = {
    1: ("Yola çıkış", "Van Gölü turu · yola çıkış", 0),
    2: ("1. durak · <b>Edremit</b>", "1. durak · Neden mol?", 0),
    3: ("2. durak · <b>Gevaş</b>", "2. durak · Atomun kütlesi", 7),
    4: ("3. durak · <b>Tatvan</b>", "3. durak · Mol ile tanecik sayısı", 18),
    5: ("4. durak · <b>Ahlat</b>", "4. durak · Mol ile kütle", 29),
    6: ("5. durak · <b>Adilcevaz</b>", "5. durak · Karışımlar", 39),
    7: ("Hülasa · <b>Süphan eteği</b>", "Hülasa · Mol özeti", 50),
    8: ("Yan yol · <b>Erciş</b>", "Yan yol 1 · Meclis: kim haklı?", 53),
    9: ("Yan yol · <b>Muradiye</b>", "Yan yol 2 · Kıssalar", 61),
    10: ("Yan yol · <b>Van iskelesi</b>", "Yan yol 3 · Anahtar merdiveni", 70),
    11: ("<b>Van Kalesi</b> · 1/2", "Büyük İmtihan · 1. bölüm", 79),
    12: ("<b>Van Kalesi</b> · 2/2", "Büyük İmtihan · 2. bölüm", 89),
    13: ("<b>Cevaplar</b>", "Cevaplar ve çözümler", 100),
    14: ("<b>Final</b>", "Final · akçe rayı ve unvan", 100),
}
# ilerleme noktaları: 5 durak + hülasa + 3 yan yol + kale ; her sayfada hangisi "şimdi"
SIMDI = {1: -1, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 9, 13: 10, 14: 10}


def hud(no):
    yer, _, bar = SAYFA[no]
    s = SIMDI[no]
    noktalar = []
    turler = ["d"] * 5 + ["hul"] + ["yan"] * 3 + ["kale"]
    for i, t in enumerate(turler):
        durum = "tam" if i < s else ("simdi" if i == s else "")
        if t == "kale":
            renk = "#E2533D" if durum else "#8FA3AD"
            noktalar.append(f'<i class="kale {durum}"><svg viewBox="0 0 24 22"><path d="M2 21 V8 H6 V4 H9 V8 H11 V4 H13 V8 H15 V4 H18 V8 H22 V21 Z" fill="{renk if durum == "tam" else "none"}" stroke="{renk}" stroke-width="2.2" stroke-linejoin="round"/></svg></i>')
        else:
            cls = {"d": "", "hul": "hul", "yan": "yan"}[t]
            noktalar.append(f'<i class="{cls} {durum}"></i>')
    return (f'<header class="hud"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>Kimya Rotası 10</span>'
            f'<span class="yer">Van Gölü turu · {yer}</span><span class="noktalar">{"".join(noktalar)}</span>'
            f'<span class="akce"><svg viewBox="0 0 40 40"><use href="#akce"/></svg>Akçe <span class="yaz"></span> /1400 '
            f'<span class="bar"><i style="width:{bar}%"></i></span></span></header>')


def alt(no):
    _, konu, _ = SAYFA[no]
    return (f'<footer class="alt"><span>Kimya Rotası 10 · Mol Kavramı</span><span>{konu}</span>'
            f'<span class="no"><svg viewBox="0 0 100 100"><use href="#no-yildiz"/></svg><b>{no}</b></span></footer><div class="ebru-alt"></div>')


# ------------------------------------------------------------------ sayfa çerçevesinin vektör dokuları

def cini_serit():
    """HUD altı İznik şeridi: 30 karo, tek SVG (desen değil; PDF'te vektör kalır)."""
    karo = U.cini_serit_ince().split(">", 1)[1].rsplit("</svg>", 1)[0]
    parca = "".join(f'<g transform="translate({k * 24} 0)">{karo}</g>' for k in range(30))
    return f'<svg class="cini-serit" viewBox="0 0 700 8" preserveAspectRatio="none">{parca}</svg>'


def zemin():
    """Sayfa zemini: çok açık Selçuklu yıldız geçmesi, tek path (210×297 mm)."""
    d = []
    adim = 15
    for i in range(-1, 16):
        for j in range(-1, 21):
            cx, cy = 7.5 + i * adim, 7.5 + j * adim
            d.append(cizgi_d(selcuklu_yildizi(cx, cy, 3.6), True, 2))
            d.append(f"M{f(cx + 5.3)} {f(cy + 5.3)} l4.4 4.4")
    return (f'<svg class="zemin" viewBox="0 0 210 297" preserveAspectRatio="none"><path d="{" ".join(d)}" fill="none" '
            f'stroke="#DDEEEE" stroke-width=".22" stroke-linejoin="round"/></svg>')


# ------------------------------------------------------------------ paylaşılan semboller (her sayfada <use> ile)

def ortak_defs():
    s = Svg("ortak")
    ga = s.lin([(0, "#FFE7A8"), (1, KEH)], 0, 0, 1, 1, ad="lg")
    gn = s.rad([(0, "#5FD3D0"), (.7, GOL), (1, GOL_K)], .4, .35, .75, ad="ng")
    sy = [f'<symbol id="logo-yildiz" viewBox="0 0 24 24"><path d="{cizgi_d(selcuklu_yildizi(12, 12, 11.4), True, 2)}" fill="{ga}" stroke="#FFF" stroke-width=".8"/>'
          f'<circle cx="12" cy="12" r="3.6" fill="{OBS}"/></symbol>',
          f'<symbol id="no-yildiz" viewBox="0 0 100 100"><path d="{cizgi_d(selcuklu_yildizi(50, 50, 48), True)}" fill="{ALTIN}" stroke="{OBS}" stroke-width="3"/>'
          f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 40), True)}" fill="{gn}" stroke="{OBS}" stroke-width="2"/></symbol>']
    return (f'<svg class="gizli-defs" aria-hidden="true"><defs>{s.govde()}{"".join(sy)}{K.semboller()}{U.ikon_sembolleri()}</defs></svg>')


# ------------------------------------------------------------------ yer tutucular

SAYAC = {"n": 0}


def _yeni(onek):
    SAYAC["n"] += 1
    return f"{onek}{SAYAC['n']}"


def yt_sahne(ad, *arg):
    if ad == "panorama":
        svg, konum = SH.panorama()
        return svg
    return getattr(SH, ad)()


def yt_mol(ad, donus="0,0,0", en="", etiket="", ion=""):
    rx, ry, rz = (float(v) for v in donus.split(","))
    svg = M.molekul_svg(_yeni("mol"), ad, (rx, ry, rz), etiket=bool(etiket), iyon_etiket=bool(ion))
    if en:
        svg = svg.replace("<svg ", f'<svg style="width:{en}" ', 1)
    return svg


def yt_kristal(en=""):
    svg = M.kristal_nacl(_yeni("kr"))
    return svg.replace("<svg ", f'<svg style="width:{en}" ', 1) if en else svg


def yt_muhur(tur, boy=""):
    return U.muhur(_yeni("mh"), tur)


def yt_rozet(metin, ust="DURAK", renk="gol"):
    r = {"gol": (GOL, GOL_K), "keh": (KEH, "#8C5500"), "mer": (MER, "#A12817"), "kob": (KOB, "#1B3584"), "erg": (ERGUVAN, "#4E2760")}[renk]
    if ust == "-":
        harf = f'<text x="50" y="64" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="40" fill="{OBS}">{metin}</text>'
        return U.durak_rozeti(_yeni("dr"), harf, "", r[0], r[1])
    return U.durak_rozeti(_yeni("dr"), metin, ust, r[0], r[1])


def yt_hno(metin, renk="keh"):
    r = {"gol": (GOL, GOL_K), "keh": (KEH, "#8C5500"), "mer": (MER, "#A12817"), "kob": (KOB, "#1B3584")}[renk]
    svg = U.durak_rozeti(_yeni("hn"), f'<text x="50" y="60" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="{OBS}">{metin}</text>', "", r[0], r[1], cls="hno")
    return svg


def yt_sno(metin, renk="mer"):
    r = {"gol": (GOL, GOL_K), "keh": (KEH, "#8C5500"), "mer": (MER, "#A12817"), "kob": (KOB, "#1B3584")}[renk]
    return U.durak_rozeti(_yeni("sn"), f'<text x="50" y="62" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="36" fill="{OBS}">{metin}</text>', "", r[0], r[1], cls="sno")


def yt_nisan(ad, kurdele="#E2533D"):
    renk = {"deste": (GOL, GOL_K), "izotop": (KOB, "#1B3584"), "kefal": (GOL, GOL_K), "mizan": (MER, "#A12817"),
            "karisim": (ERGUVAN, "#4E2760"), "kale": (KEH, "#8C5500")}[ad]
    return U.nisan(_yeni("ns"), U.NISAN_IKON[ad], renk[0], renk[1], kurdele=kurdele if kurdele != "-" else None)


def yt_cay(seviye, bos=""):
    return U.cay_bardagi(_yeni("cy"), float(seviye), bool(bos))


def yt_kose():
    return "".join(U.tezhip_kose(_yeni("tk")).replace('class="tezhip-kose"', f'class="kose k{k}"') for k in range(1, 5))


def yt_kilim():
    return U.kilim_serit(_yeni("kl"), 1880, 60)


def yt_av(kim):
    vb = "0 0 40 40" if kim == "pamuk" else "0 0 200 210"
    return f'<svg class="av" viewBox="{vb}"><use href="#av-{kim}"/></svg>'


def yt_poz(ad, cls=""):
    vb = "0 -40 170 200" if ad == "pamuk-bayrak" else ("0 0 140 160" if ad.startswith("pamuk") else "0 0 200 210")
    return f'<svg class="{cls}" viewBox="{vb}"><use href="#{ad}"/></svg>'


def yt_ikon(ad, cls="ikon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24"><use href="#i-{ad}"/></svg>'


def yt_sikke(cls="sikke"):
    return f'<svg class="{cls}" viewBox="0 0 40 40"><use href="#akce"/></svg>'


def yt_info(ad, *arg):
    fn = getattr(I, ad)
    if ad == "mol_haritasi":
        return fn(_yeni("mh"), kutle_acik=(arg and arg[0] == "acik"))
    if ad == "unvan_rozeti":
        return fn(_yeni("ur"), int(arg[0]), arg[1])
    return fn(_yeni(ad[:4]))


def yt_final():
    ns = [U.nisan(_yeni("nf"), U.NISAN_IKON[k], *{"deste": (GOL, GOL_K), "izotop": (KOB, "#1B3584"), "kefal": (GOL, GOL_K),
                                                   "mizan": (MER, "#A12817"), "karisim": (ERGUVAN, "#4E2760"), "kale": (KEH, "#8C5500")}[k],
                  kurdele="#E2533D").replace("<svg ", '<svg width="124" height="148" ', 1)
          for k in ("deste", "izotop", "kefal", "mizan", "karisim", "kale")]
    return SH.final(nisanlar=ns)


def yt_panorama_etiket():
    """Açılış panoramasındaki durak etiketleri (HTML; konumlar sahnenin projeksiyonundan)."""
    _, konum = SH.panorama()
    # etiket yerleşimi: (sol mm, üst mm) ofsetleri, rozet merkezine göre
    yer = {"1": (2.4, 4.4), "2": (-44, -3.4), "3": (-10, 4.4), "4": (-33.5, -11), "5": (-12, 3.2),
           "H": (-23, -12.6), "M": (-19, -12.4), "K": (3.8, -9.6), "A": (4.2, -14.4), "V": (6.2, 2.2)}
    out = []
    for (k, a, b, ust, ad, alt_, tur, _y) in SH.DURAKLAR:
        x, y = konum[k]
        dx, dy = yer[k]
        cls = {"durak": "", "hulasa": "hul", "yan": "yan", "kale": "kale"}[tur]
        sayfa, akce = alt_.split(" · ")
        out.append(f'<div class="durak-et {cls}" style="left:{f(x / 10 + dx, 2)}mm;top:{f(y / 10 + dy, 2)}mm"><i>{ust} · {sayfa}</i><b>{ad}<small>{akce}</small></b></div>')
    return "".join(out)


YT = {
    "hud": lambda no: hud(int(no)), "alt": lambda no: alt(int(no)), "cini": cini_serit, "zemin": zemin, "defs": ortak_defs,
    "sahne": yt_sahne, "sno": yt_sno, "mol": yt_mol, "kristal": yt_kristal, "muhur": yt_muhur, "rozet": yt_rozet, "hno": yt_hno,
    "nisan": yt_nisan, "cay": yt_cay, "kose": yt_kose, "kilim": yt_kilim, "av": yt_av, "poz": yt_poz, "ikon": yt_ikon,
    "sikke": yt_sikke, "info": yt_info, "final": yt_final, "panorama-etiket": yt_panorama_etiket,
}


def kur():
    gorsel = os.path.join(ORTAK, "gorsel")
    os.makedirs(gorsel, exist_ok=True)
    if "--ebru" in sys.argv or not os.path.exists(os.path.join(gorsel, "ebru-gol.jpg")):
        print("ebru dokuları üretiliyor…")
        E.ebru_gol(os.path.join(gorsel, "ebru-gol.jpg"))
        E.ebru_gun(os.path.join(gorsel, "ebru-gun.jpg"))
    sablon = open(os.path.join(BURA, "sablon.html"), encoding="utf-8").read()

    def degistir(m):
        parca = m.group(1).split("|")
        ad, arg = parca[0].strip(), [a.strip() for a in parca[1:]]
        if ad not in YT:
            raise KeyError(f"bilinmeyen yer tutucu: {ad}")
        return YT[ad](*arg)

    html = re.sub(r"\{\{([^{}]+)\}\}", degistir, sablon)
    hedef = os.path.join(UNITE, "unite.html")
    open(hedef, "w", encoding="utf-8").write(html)
    print(f"unite.html yazıldı ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    kur()
