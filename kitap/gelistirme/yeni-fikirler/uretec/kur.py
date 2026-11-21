#!/usr/bin/env python3
"""Yeni fikirler örneği · kurucu.

    python3 uretec/kur.py              iki HTML → render.js (PDF + PNG + taşma) → yeni-fikirler-ornek.pdf → önizlemeler (onizle.py)
    python3 uretec/kur.py --pdfsiz     yalnız PNG (hızlı deneme; birleştirme ve önizleme yok)
    python3 uretec/kur.py --onizlemesiz

Sayfalar (kitap sırası):
  1 (9)  Usturlap Çarkı · kesme yaprağı ön yüz        ┐ 1. yaprak (kesilir)
  2 (10) Usturlap Çarkı · kesme yaprağı arka yüz      ┘
  3 (9)  Gizli cevap (kırmızı camdan bak)             ┐ 2. yaprak
  4 (9)  Ustanın Sırrı · ebru                         ┘
  5 (10) Kâğıtta animasyon (geçmeli resimler)         ┐ 3. yaprak (arkası boş ya da ünite sayfası)
  6 (10) Asetat perde (şeffaf asetata basılır)        ┘ ayrı asetat yaprak
Modüller: bu klasör + karma-temalar/uretec (tema, konu_karakterleri, karma.css) + atom-modelleri/uretec (gelistirme.css,
hap_bilgi): hepsi salt okunur. Ortak motor: yerel-ortak/kur_ortak.py, render.js. Element verisi: yerel-cerceve/uretec/elementler.py.
"""
import json
import os
import shutil
import subprocess
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
ORTAK = os.path.join(KITAP, "yerel-ortak")
ATOM = os.path.join(KITAP, "gelistirme", "atom-modelleri", "uretec")
KARMA = os.path.join(KITAP, "gelistirme", "karma-temalar", "uretec")
CERCEVE = os.path.join(KITAP, "yerel-cerceve", "uretec")
for _yol in (CERCEVE, ORTAK, ATOM, KARMA, BURA):          # arama sırası: bu klasör, karma, atom, ortak, çerçeve
    sys.path.insert(0, _yol)
import kur_ortak as KO  # noqa: E402
import tema as TM  # noqa: E402
import konu_karakterleri as KK  # noqa: E402
import hap_bilgi as HB  # noqa: E402
import usturlap as US  # noqa: E402

CSS = [(os.path.join(ORTAK, "stil.css"), r'<link rel="stylesheet" href="[^"]*yerel-ortak/stil\.css">'),
       (os.path.join(ATOM, "gelistirme.css"), r'<link rel="stylesheet" href="uretec/gelistirme\.css">'),
       (os.path.join(KARMA, "karma.css"), r'<link rel="stylesheet" href="uretec/karma\.css">'),
       (os.path.join(BURA, "yeni.css"), r'<link rel="stylesheet" href="uretec/yeni\.css">')]
RENDER = os.path.join(ORTAK, "render.js")
DEFS = KK.semboller()
PDF = os.path.join(KLASOR, "yeni-fikirler-ornek.pdf")
RAPOR = os.path.join(KLASOR, "kur-raporu.json")
KITAPLAR = [  # (sınıf, meta klasörü, şablon, palet, çıktı adı, kitaptaki sayfa numaraları)
    (9, "s9", "sablon9.html", "cini-toprak", "yeni-9", [1, 3, 4]),
    (10, "s10", "sablon10.html", "gol-rasathane", "yeni-10", [2, 5, 6]),
]


def hudk(sinif, metin):
    return (f'<header class="hud"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>Kimya Rotası {sinif}</span>'
            f'<span class="yer">{metin}</span></header>')


def altk(metin, no, tur=""):
    no_html = f'<span class="no"><svg viewBox="0 0 100 100"><use href="#no-yildiz"/></svg><b>{no}</b></span>'
    if tur == "duz":       # asetat sayfası: ebru şeridi yok
        return f'<footer class="alt"><span>{metin}</span>{no_html}</footer>'
    return f'<footer class="alt"><span>{metin}</span>{no_html}</footer><div class="ebru-alt"></div>'


def delta():
    """δ: Nunito'da yok; yazı içi küçük SVG (kontursuz dolgu yerine ince çizgi; PDF'te vektör)."""
    return ('<svg class="delta" viewBox="0 0 10 14" aria-label="delta"><path d="M7.6 2.3 C6.3 .9 2.6 .9 2.9 2.9 C3.2 4.6 8.4 5.1 8.6 8.9 '
            'C8.8 11.9 6.6 13.3 5 13.3 C2.5 13.3 1.2 11.5 1.4 9.4 C1.6 7.3 3.7 6 6 5.6" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round"/></svg>')


def _modul(ad):
    return __import__(ad)


def unite(alt):
    u = KO.Unite(os.path.join(BURA, alt, "kur.py"), {})
    u.ek_defs = DEFS
    yt = {"hudk": hudk, "altk": altk, "hbi": HB.ikon, "delta": delta, "usturlap-on": US.sayfa_on, "usturlap-arka": US.sayfa_arka}
    if os.path.exists(os.path.join(BURA, "gizli.py")):
        GZ = _modul("gizli")
        yt.update({"gizli": GZ.yer_tutucu, "gizli-sema": GZ.sema})
    if os.path.exists(os.path.join(BURA, "animasyon.py")):
        AN = _modul("animasyon")
        yt.update({"anim": AN.sayfa_svg, "perde": AN.perde_svg, "anim-kare": AN.kare_seridi})
    if os.path.exists(os.path.join(BURA, "usta.py")):
        UT = _modul("usta")
        yt.update({"usta": UT.usta, "sir": UT.sir_cizim, "unesco": UT.unesco_rozet})
    for ad, fn in yt.items():
        u.yer_tutucu(ad, fn)
    return u


def yaz(yol, metin):
    with open(yol, "w", encoding="utf-8") as fp:
        fp.write(metin)
    print(f"{os.path.relpath(yol, KITAP)} yazıldı ({len(metin) / 1024:.0f} KB)")


def html_kur(alt, sablon, palet, ad):
    u = unite(alt)
    TM.AKTIF = palet
    u.sayac = 0
    with open(os.path.join(BURA, sablon), encoding="utf-8") as fp:
        html = u._cozumle(fp.read())
    hedef = os.path.join(KLASOR, ad + ".html")
    yaz(hedef, TM.tema_html(html, palet, CSS, hedef, ORTAK))
    return hedef


def bas(html, sayfalar, pdfsiz=False):
    """render.js: PDF + PNG + taşma denetimi. PNG'ler onizleme/sNN.png (kitap sırasıyla) olur."""
    cikti = subprocess.run(["node", RENDER, html] + (["--pdfsiz"] if pdfsiz else []), capture_output=True, text=True, cwd=KLASOR)
    metin = cikti.stdout + cikti.stderr
    ad = os.path.splitext(os.path.basename(html))[0]
    gecici = os.path.join(KLASOR, "onizleme-" + ad)
    hedef = os.path.join(KLASOR, "onizleme")
    os.makedirs(hedef, exist_ok=True)
    if os.path.isdir(gecici):
        for f_ in sorted(os.listdir(gecici)):
            if f_.startswith("s") and f_.endswith(".png"):
                n = sayfalar[int(f_[1:-4]) - 1]
                shutil.move(os.path.join(gecici, f_), os.path.join(hedef, f"s{n:02d}.png"))
        shutil.rmtree(gecici)
    sorun = [l for l in metin.splitlines() if "alan dışı" in l or ("taşma" in l.lower() and "Taşma yok" not in l) or "HATA" in l or "Error" in l]
    t3 = [l for l in metin.splitlines() if "Type 3" in l]
    print(f"  bas: {os.path.basename(html)} → {'; '.join(sorun) if sorun else 'taşma yok'} {' '.join(t3)}")
    if cikti.returncode:
        print(metin[-2500:])
    return sorun, cikti.returncode


def birlestir(parcalar):
    """parcalar: [(pdf, [kitap sayfa no])] → kitap sırasıyla tek PDF."""
    gecici = os.path.join(KLASOR, "yenifikir-gecici")
    os.makedirs(gecici, exist_ok=True)
    tek = {}
    for pdf, nolar in parcalar:
        ad = os.path.splitext(os.path.basename(pdf))[0]
        subprocess.run(["pdfseparate", pdf, os.path.join(gecici, ad + "-%d.pdf")], check=True)
        for i, n in enumerate(nolar, 1):
            yol = os.path.join(gecici, f"{ad}-{i}.pdf")
            if os.path.exists(yol):
                tek[n] = yol
    sira = [tek[n] for n in sorted(tek)]
    subprocess.run(["pdfunite"] + sira + [PDF], check=True)
    shutil.rmtree(gecici)
    for pdf, _ in parcalar:
        os.remove(pdf)
    print(f"{os.path.relpath(PDF, KITAP)} yazıldı ({len(sira)} sayfa)")


def main(argv):
    pdfsiz = "--pdfsiz" in argv
    yalniz = [int(a.split("=")[1]) for a in argv if a.startswith("--sinif=")]
    if os.path.exists(os.path.join(BURA, "gizli.py")):
        _modul("gizli").hazirla()          # gizli cevap PNG'leri (gorsel/)
    rapor = {"tasma": {}, "kod": {}}
    parcalar = []
    for sinif, alt, sablon, palet, ad, sayfalar in KITAPLAR:
        if yalniz and sinif not in yalniz:
            continue
        html = html_kur(alt, sablon, palet, ad)
        sorun, kod = bas(html, sayfalar, pdfsiz)
        rapor["tasma"][ad], rapor["kod"][ad] = sorun, kod
        parcalar.append((os.path.join(KLASOR, ad + ".pdf"), sayfalar))
    if pdfsiz or yalniz:
        return
    birlestir(parcalar)
    t3 = subprocess.run(["pdffonts", PDF], capture_output=True, text=True).stdout.count("Type 3")
    rapor["type3"] = t3
    print(f"Type 3 font: {t3}")
    with open(RAPOR, "w", encoding="utf-8") as fp:
        json.dump(rapor, fp, ensure_ascii=False, indent=1)
    if "--onizlemesiz" not in argv:
        import onizle
        onizle.hepsi(PDF, os.path.join(KLASOR, "onizleme"))


if __name__ == "__main__":
    main(sys.argv[1:])
