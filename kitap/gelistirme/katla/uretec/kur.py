#!/usr/bin/env python3
"""Katla örneği · kurucu.

    python3 uretec/kur.py              iki HTML → render.js (PDF + PNG + taşma) → katla-ornek.pdf → önizlemeler (onizle.py)
    python3 uretec/kur.py --pdfsiz     yalnız PNG (hızlı deneme; birleştirme ve önizleme yok)

Sayfalar: 1 kat sayfası 9 (Çini ve Toprak) · 2 karma sayfa (1'in arkası) · 3 kat sayfası 10 (Göl ve Rasathane) ·
4 köşe sineması (3'ün arkası) · 5 köşeyi katla ön · 6 köşeyi katla arka.
Modüller: bu klasör (katla_cizim, katla.css, şablonlar) + karma-temalar/uretec (tema, konu_karakterleri, karma.css) +
atom-modelleri/uretec (gelistirme.css): hepsi salt okunur kullanılır. Ortak motor: yerel-ortak/kur_ortak.py, render.js.
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
for _yol in (ORTAK, ATOM, KARMA, BURA):          # arama sırası: bu klasör, karma, atom, ortak
    sys.path.insert(0, _yol)
import kur_ortak as KO  # noqa: E402
import tema as TM  # noqa: E402
import konu_karakterleri as KK  # noqa: E402
import katla_cizim as KC  # noqa: E402

CSS = [(os.path.join(ORTAK, "stil.css"), r'<link rel="stylesheet" href="[^"]*yerel-ortak/stil\.css">'),
       (os.path.join(ATOM, "gelistirme.css"), r'<link rel="stylesheet" href="uretec/gelistirme\.css">'),
       (os.path.join(KARMA, "karma.css"), r'<link rel="stylesheet" href="uretec/karma\.css">'),
       (os.path.join(BURA, "katla.css"), r'<link rel="stylesheet" href="uretec/katla\.css">')]
RENDER = os.path.join(ORTAK, "render.js")
DEFS = KK.semboller()
PDF = os.path.join(KLASOR, "katla-ornek.pdf")
RAPOR = os.path.join(KLASOR, "kur-raporu.json")
KITAPLAR = [  # (sınıf, meta klasörü, şablon, palet, çıktı adı, ilk sayfa no)
    (9, "s9", "sablon9.html", "cini-toprak", "katla-9", 1),
    (10, "s10", "sablon10.html", "gol-rasathane", "katla-10", 3),
]


def cini14():
    """HUD altı çini şeridi, 7 mm karolarla (30 karo = 210 mm): 70 ve 140 mm karo sınırına düşer, katlayınca desen sürer."""
    return KO.cini_serit().replace('viewBox="0 0 700 8"', 'viewBox="0 0 720 8"', 1)


def hudk(sinif, metin, kat=""):
    return (f'<header class="hud{" kat-hud" if kat else ""}"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>Kimya Rotası {sinif}</span>'
            f'<span class="yer">{metin}</span></header>')


def altk(metin, no, tur=""):
    """tur: "" (normal) · kat (dikişte kopmayan düz alt şerit) · kose-on / kose-arka (köşe boş kalır)."""
    no_html = f'<span class="no"><svg viewBox="0 0 100 100"><use href="#no-yildiz"/></svg><b>{no}</b></span>'
    if tur == "kat":
        return f'<footer class="alt kat-alt"><span>{metin}</span>{no_html}</footer><div class="hud kat-serit"></div>'
    if tur == "kose-on":
        return f'<footer class="alt kose-on-alt">{no_html}<span>{metin}</span></footer><div class="ebru-alt kose-on"></div>'
    if tur == "kose-arka":
        return f'<footer class="alt kose-arka-alt"><span>{metin}</span>{no_html}</footer><div class="ebru-alt kose-arka"></div>'
    return f'<footer class="alt"><span>{metin}</span>{no_html}</footer><div class="ebru-alt"></div>'


def unite(alt):
    u = KO.Unite(os.path.join(BURA, alt, "kur.py"), {})
    u.ek_defs = DEFS

    def katla(tur):
        if tur == "bag":
            s, _ = KC.bag_sayfasi("f1", u.yt["rozet"]("6", "YOL"), KC.kare(0, "kb"), 1)
        else:
            s, _ = KC.tepkime_sayfasi("f2", u.yt["rozet"]("1", "YOL"), KC.kare(1, "kt"), 2)
        return s.cikti()
    for ad, fn in (("katla", katla), ("hudk", hudk), ("altk", altk), ("cini14", cini14), ("zemin14", KC.zemin14),
                   ("kikon", KC.ikon), ("robot", KC.robot), ("kapi", KC.kapi), ("film", KC.film_izgara),
                   ("kose-on", lambda: KC.kose_on()), ("kose-arka", lambda: KC.kose_arka()),
                   ("kose-adimlar", KC.kose_adimlar), ("kose-harita", KC.kose_harita)):
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


def bas(html, ilk, pdfsiz=False):
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
                n = int(f_[1:-4]) + ilk - 1
                shutil.move(os.path.join(gecici, f_), os.path.join(hedef, f"s{n:02d}.png"))
        shutil.rmtree(gecici)
    sorun = [l for l in metin.splitlines() if "alan dışı" in l or ("taşma" in l.lower() and "Taşma yok" not in l) or "HATA" in l or "Error" in l]
    print(f"  bas: {os.path.basename(html)} → {'; '.join(sorun) if sorun else 'taşma yok'}")
    if cikti.returncode:
        print(metin[-2500:])
    return sorun, cikti.returncode


def main(argv):
    pdfsiz = "--pdfsiz" in argv
    rapor = {"tasma": {}, "kod": {}}
    pdfler = []
    for sinif, alt, sablon, palet, ad, ilk in KITAPLAR:
        html = html_kur(alt, sablon, palet, ad)
        sorun, kod = bas(html, ilk, pdfsiz)
        rapor["tasma"][ad], rapor["kod"][ad] = sorun, kod
        pdfler.append(os.path.join(KLASOR, ad + ".pdf"))
    if pdfsiz:
        return
    subprocess.run(["pdfunite"] + pdfler + [PDF], check=True)
    for p in pdfler:
        os.remove(p)
    print(f"{os.path.relpath(PDF, KITAP)} yazıldı")
    with open(RAPOR, "w", encoding="utf-8") as fp:
        json.dump(rapor, fp, ensure_ascii=False, indent=1)
    if "--onizlemesiz" not in argv:
        import onizle
        onizle.hepsi(PDF, os.path.join(KLASOR, "onizleme"))


if __name__ == "__main__":
    main(sys.argv[1:])
