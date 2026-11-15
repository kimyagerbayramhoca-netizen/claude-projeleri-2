"""Periyodik tablo sayfası çizimi: yatay (landscape) tablo tek SVG olarak çizilir ve dikey A4 sayfaya −90° döndürülerek
yerleştirilir (okumak için kitap saat yönünde çevrilir). Birim: mm.

Hücre: üstte sınıf renginde şerit, atom numarası, sembol, Türkçe ad (sığacak boyuta küçülür), mol kütlesi;
rotalarda geçen Türkiye elementlerinde sağ üstte iğne + Yol numarası.
"""
import math
import os
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
ORTAK = os.path.normpath(os.path.join(BURA, "..", "..", "yerel-ortak"))
for _p in (ORTAK, BURA):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from PIL import ImageFont  # noqa: E402
from cizim.temel import Svg, f, cizgi_d, selcuklu_yildizi  # noqa: E402
import elementler as EL  # noqa: E402

FONT = os.path.normpath(os.path.join(BURA, "..", "..", "fontlar", "nunito", "static", "Nunito-700.ttf"))
_OLCU = ImageFont.truetype(FONT, 100)

OBS = "#1B1D26"
SINIF_RENK = {  # (dolgu, şerit/çizgi, ad)
    "metal": ("#FFE1D8", "#E2533D", "Metal"),
    "ametal": ("#D2F1EE", "#13A3A6", "Ametal"),
    "yari": ("#FFEBB8", "#F0A21A", "Yarı metal"),
    "soy": ("#EDDDF3", "#7B3F8C", "Soy gaz"),
    "belirsiz": ("#E8EDF0", "#8FA3AD", "Sınıfı kaynağa göre değişir"),
}
BW, BH = 266.0, 186.0
X0, CW, W_ = 8.5, 14.25, 13.65
Y0, RH, H_ = 23.6, 15.25, 14.65
YF = Y0 + 7 * RH + 4.0


def _gen(metin, boy_mm):
    return _OLCU.getlength(metin) / 100 * boy_mm


def _yazi(x, y, metin, boy, renk=OBS, aile="Nunito", kalin=800, anchor="middle", ek=""):
    return (f'<text x="{f(x, 2)}" y="{f(y, 2)}" text-anchor="{anchor}" font-family="{aile}" font-weight="{kalin}" '
            f'font-size="{f(boy, 2)}" fill="{renk}"{ek}>{metin}</text>')


def _igne(x, y, renk="#E2533D"):
    """Küçük harita iğnesi (sivri ucu x, y)."""
    return (f'<path d="M{f(x, 2)} {f(y, 2)} C{f(x - .6, 2)} {f(y - 1.1, 2)} {f(x - 1.25, 2)} {f(y - 1.7, 2)} {f(x - 1.25, 2)} {f(y - 2.45, 2)} '
            f'A1.25 1.25 0 1 1 {f(x + 1.25, 2)} {f(y - 2.45, 2)} C{f(x + 1.25, 2)} {f(y - 1.7, 2)} {f(x + .6, 2)} {f(y - 1.1, 2)} {f(x, 2)} {f(y, 2)} Z" '
            f'fill="{renk}" stroke="{OBS}" stroke-width=".22"/><circle cx="{f(x, 2)}" cy="{f(y - 2.45, 2)}" r=".45" fill="#FFFFFF"/>')


def _hucre(x, y, el, isaret=None, w=W_, h=H_, olcek=1.0):
    dol, cz, _ = SINIF_RENK[EL.sinif(el["sembol"])]
    o = [f'<rect x="{f(x, 2)}" y="{f(y, 2)}" width="{f(w, 2)}" height="{f(h, 2)}" rx="{f(.9 * olcek, 2)}" fill="{dol}" stroke="{cz}" stroke-width="{f(.28 * olcek, 2)}"/>',
         f'<path d="M{f(x + .14, 2)} {f(y + 1.35 * olcek, 2)} V{f(y + .9 * olcek, 2)} A{f(.8 * olcek, 2)} {f(.8 * olcek, 2)} 0 0 1 {f(x + .9 * olcek, 2)} {f(y + .14, 2)} '
         f'H{f(x + w - .9 * olcek, 2)} A{f(.8 * olcek, 2)} {f(.8 * olcek, 2)} 0 0 1 {f(x + w - .14, 2)} {f(y + .9 * olcek, 2)} V{f(y + 1.35 * olcek, 2)} Z" fill="{cz}"/>']
    o.append(_yazi(x + .9 * olcek, y + 4.1 * olcek, str(el["z"]), 2.25 * olcek, OBS, kalin=800, anchor="start"))
    o.append(_yazi(x + w / 2, y + 9.4 * olcek, el["sembol"], 5.5 * olcek, OBS, "Baloo Bhaijaan 2", 800))
    boy = 1.95 * olcek
    sigacak = (w - 1.0 * olcek)
    g = _gen(el["ad"], boy)
    if g > sigacak:
        boy = boy * sigacak / g
    o.append(_yazi(x + w / 2, y + 11.95 * olcek, el["ad"], boy, "#343947", kalin=700))
    if el["kutle"]:
        o.append(_yazi(x + w / 2, y + 14.0 * olcek, el["kutle"], 2.0 * olcek, cz if cz != "#8FA3AD" else "#586874", kalin=900))
    if isaret:
        etiket, renk = isaret
        o.append(_igne(x + w - 1.75 * olcek, y + 4.9 * olcek, renk))
        o.append(_yazi(x + w - .55 * olcek, y + 7.0 * olcek, etiket, 1.75 * olcek, renk, kalin=900, anchor="end"))
    return "".join(o)


def tablo_svg(onek, sinif, yol_renk):
    """yol_renk: {(sinif, yol): renk}. Döndürür: dikey sayfaya yerleşecek SVG (viewBox 0 0 186 266)."""
    s = Svg(onek)
    o = []
    # --- başlık
    o.append(_yazi(X0, 9.6, "Periyodik Tablo", 7.4, OBS, "Baloo Bhaijaan 2", 800, "start"))
    o.append(_yazi(X0 + 61, 9.0, "118 element · Türkçe adlar · mol kütleleri (g/mol)", 2.7, "#56636E", kalin=800, anchor="start"))
    o.append(_yazi(BW - 1, 6.6, "Üstte IUPAC grup numarası (1–18), altta A/B adı", 2.3, "#56636E", kalin=800, anchor="end"))
    o.append(_yazi(BW - 1, 10.2, "Periyot numarası solda", 2.3, "#56636E", kalin=800, anchor="end"))
    # --- grup başlıkları ve periyotlar
    for g in range(1, 19):
        x = X0 + (g - 1) * CW + W_ / 2
        o.append(_yazi(x, Y0 - 3.6, str(g), 3.1, "#1D3A8A", "Baloo Bhaijaan 2", 800))
        o.append(_yazi(x, Y0 - .9, EL.ab_adi(g), 2.1, "#586874", kalin=900))
    for p in range(1, 8):
        o.append(_yazi(X0 - 3.6, Y0 + (p - 1) * RH + H_ / 2 + 1.3, str(p), 3.4, "#1D3A8A", "Baloo Bhaijaan 2", 800))
    # --- Türkiye işaretleri
    isaret = {}
    for sem, yer_, refs in EL.TURKIYE:
        bu = [y for (sn, y) in refs if sn == sinif]
        if bu:
            isaret[sem] = ("Y" + "·".join(str(y) for y in sorted(bu)), yol_renk.get((sinif, bu[0]), "#E2533D"))
        else:
            sn, y = refs[0]
            isaret[sem] = (f"{sn}·{y}", "#586874")
    # --- hücreler
    for el in EL.ELEMENTLER:
        p, g = EL.yer(el["z"])
        if g is None:
            k = el["z"] - 57 if el["z"] < 89 else el["z"] - 89
            r = 0 if el["z"] < 89 else 1
            x, y = X0 + (2 + k) * CW, YF + r * RH
        else:
            x, y = X0 + (g - 1) * CW, Y0 + (p - 1) * RH
        o.append(_hucre(x, y, el, isaret.get(el["sembol"])))
    # 3. grupta yer tutucular
    for p, metin, alt in ((6, "57–71", "lantanitler"), (7, "89–103", "aktinitler")):
        x, y = X0 + 2 * CW, Y0 + (p - 1) * RH
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{W_}" height="{H_}" rx=".9" fill="#FFF4F0" stroke="#E2533D" stroke-width=".28" stroke-dasharray="1 .7"/>')
        o.append(_yazi(x + W_ / 2, y + 6.6, metin, 2.6, "#A12817", kalin=900))
        o.append(_yazi(x + W_ / 2, y + 9.6, alt, 1.9, "#A12817", kalin=800))
        o.append(_yazi(x + W_ / 2, y + 12.6, "*" if p == 6 else "**", 2.6, "#A12817", kalin=900))
    for r, (ad, per, yild) in enumerate((("Lantanitler", "6. periyot", "*"), ("Aktinitler", "7. periyot", "**"))):
        y = YF + r * RH
        o.append(_yazi(X0 + 2 * CW - 1.4, y + 6.2, f"{yild} {ad}", 3.0, "#A12817", "Baloo Bhaijaan 2", 800, "end"))
        o.append(_yazi(X0 + 2 * CW - 1.4, y + 9.6, f"{per} · iç geçiş metalleri", 2.1, "#56636E", kalin=800, anchor="end"))
    # metal / ametal sınırı (merdiven): B-Si-As-Te-At sol kenarı
    basamak = [(2, 13), (3, 14), (4, 14), (5, 15), (6, 16), (7, 16)]
    d = []
    for i, (p, g) in enumerate(basamak):
        x = X0 + (g - 1) * CW - (CW - W_) / 2
        y = Y0 + (p - 1) * RH - (RH - H_) / 2
        d.append(f"{'M' if i == 0 else 'H'}{f(x, 2)}" + (f" {f(y, 2)}" if i == 0 else ""))
        d.append(f"V{f(y + RH, 2)}")
    o.append(f'<path d="{" ".join(d)}" fill="none" stroke="{OBS}" stroke-width=".75" stroke-linejoin="round"/>')
    # --- boşluktaki anahtar (3–6. gruplar), sınıflar (1. periyot, 7–17. gruplar) ve Türkiye paneli (2–3. periyot, 7–12. gruplar)
    ax, ay = X0 + 2 * CW + .6, Y0
    o.append(_yazi(ax, ay + 2.6, "NASIL OKUNUR?", 2.4, "#1D3A8A", kalin=900, anchor="start", ek=' letter-spacing=".35"'))
    ornek = {"z": 29, "sembol": "Cu", "ad": "Bakır", "kutle": "64"}
    ox, oy, ol = ax + .4, ay + 5.2, 1.72
    o.append(_hucre(ox, oy, ornek, None, W_ * ol, H_ * ol, ol))
    for (ty, metin) in ((4.1, "atom numarası"), (9.4, "sembol"), (11.95, "Türkçe ad"), (14.0, "mol kütlesi (g/mol)")):
        yy = oy + ty * ol - 1.0
        o.append(f'<path d="M{f(ox + W_ * ol + .6, 2)} {f(yy, 2)} h2.6" stroke="{OBS}" stroke-width=".25"/>')
        o.append(_yazi(ox + W_ * ol + 3.7, yy + .7, metin, 2.15, OBS, kalin=800, anchor="start"))
    lx, ly = X0 + 6 * CW + .6, Y0 + 2.6
    o.append(_yazi(lx, ly, "SINIFLAR", 2.4, "#1D3A8A", kalin=900, anchor="start", ek=' letter-spacing=".35"'))
    x = lx
    for k in ("metal", "ametal", "yari", "soy", "belirsiz"):
        dol, cz, ad = SINIF_RENK[k]
        ad = ad if k != "belirsiz" else "Po, At, 113–117: sınıfı kaynağa göre değişir"
        if k == "soy":
            ad = "Soy gaz"
        o.append(f'<rect x="{f(x)}" y="{f(ly + 3)}" width="6.5" height="4.4" rx=".7" fill="{dol}" stroke="{cz}" stroke-width=".28"/>'
                 f'<rect x="{f(x)}" y="{f(ly + 3)}" width="6.5" height="1.1" rx=".4" fill="{cz}"/>')
        o.append(_yazi(x + 8, ly + 6.4, ad, 2.35, OBS, kalin=800, anchor="start"))
        x += 8 + _gen(ad, 2.35) + 4.2

    # Türkiye paneli
    tx, ty0 = X0 + 6 * CW, Y0 + RH
    tw, th = 6 * CW - (CW - W_), 2 * RH - (RH - H_)
    o.append(f'<rect x="{f(tx)}" y="{f(ty0)}" width="{f(tw)}" height="{f(th)}" rx="1.6" fill="#FFFDF7" stroke="#1D3A8A" stroke-width=".4"/>'
             f'<rect x="{f(tx + .7)}" y="{f(ty0 + .7)}" width="{f(tw - 1.4)}" height="{f(th - 1.4)}" rx="1.2" fill="none" stroke="#C9952B" stroke-width=".25"/>')
    o.append(_igne(tx + 3.0, ty0 + 4.9) + _yazi(tx + 5.2, ty0 + 4.3, "TÜRKİYE’DEN · ROTALARDA GEÇEN ELEMENTLER", 2.3, "#1D3A8A", kalin=900, anchor="start", ek=' letter-spacing=".2"'))
    satirlar = []
    goruldu = set()
    for sem, yer_, refs in EL.TURKIYE:
        anahtar = (EL.KISA_YER.get(sem, yer_), tuple(refs))
        if anahtar in goruldu:
            continue
        goruldu.add(anahtar)
        ayni = [s2 for s2, y2, r2 in EL.TURKIYE if EL.KISA_YER.get(s2, y2) == anahtar[0] and r2 == refs]
        satirlar.append((" · ".join(ayni), anahtar[0], refs))
    sw = (tw - 3.0) / 2
    for i, (sem, yer_, refs) in enumerate(satirlar):
        c, r = i // 4, i % 4
        x0, y0 = tx + 1.8 + c * sw, ty0 + 6.6 + r * 5.95
        o.append(_yazi(x0, y0 + 2.8, sem, 2.7, "#A12817", "Baloo Bhaijaan 2", 800, "start"))
        bx = x0 + (9.6 if "·" in sem else 5.4)
        boy = min(2.05, 2.05 * (sw - (bx - x0) - 1) / max(1e-6, _gen(yer_, 2.05)))
        o.append(_yazi(bx, y0 + 1.9, yer_, boy, OBS, kalin=800, anchor="start"))
        etk = " · ".join(f"{sn}. sınıf Yol {yl}" for sn, yl in refs)
        o.append(_yazi(bx, y0 + 4.4, etk, 1.85, "#1D3A8A" if any(sn == sinif for sn, _ in refs) else "#586874", kalin=900, anchor="start"))
    # --- dipnotlar
    ny = YF + 2 * RH + 3.9
    notlar = ["* ve ** : 57–71 lantanitler ve 89–103 aktinitler IUPAC düzeninde ayrı iki satırdır; hepsi metaldir.",
              "[ ] : Kararlı izotopu olmayan elementte en uzun ömürlü izotopun kütle numarası. 104–118: çok az atom elde edildiğinden kütle yazılmadı.",
              "Kalın merdiven çizgisi metalleri ametal ve yarı metallerden ayırır. Mol kütleleri yuvarlanmıştır (Cl 35,5); kitaptaki sorularda bu değerler kullanılır.",
              "İğne: Türkiye’de çıkarılan ya da üretilen, rotalarda geçen element; yanındaki sayı Yol numarasıdır (gri: öbür sınıfın kitabındaki yol)."]
    for i, n in enumerate(notlar):
        o.append(_yazi(X0, ny + i * 3.35, n, 2.2, "#343947", kalin=700, anchor="start"))
    s += f'<g transform="rotate(-90) translate(-{f(BW)} 0)">{"".join(o)}</g>'
    return s.cikti(f"0 0 {f(BH)} {f(BW)}", cls="pt-svg")
