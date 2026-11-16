#!/usr/bin/env python3
"""Geliştirme örneği · atom modelleri — kurucu (ortak motor: yerel-ortak/kur_ortak.py; ortak dosyalara dokunmaz).

    python3 uretec/kur.py                    5 tema × 3 sayfa + katalog + karşılaştırma + renk denetimi (hepsi)
    python3 uretec/kur.py --tema van-golu    yalnız bir tema (hızlı deneme; katalog/karşılaştırma yok)
    python3 uretec/kur.py --katalog          yalnız katalog sayfaları (hap-bilgi-katalog.pdf)
    python3 uretec/kur.py --htmlsiz          HTML'leri yeniden kurmadan yalnız bas (render.js)

Çıktılar (klasör kökü): atom-modelleri-<tema>.pdf, hap-bilgi-katalog.pdf, onizleme/<tema>/s01…s03.png,
onizleme/karsilastirma.png, hap-bilgi.png, temalar.png, karakterler.png, renk-korlugu.png, renk-denetimi.json.
Ara dosyalar (*.html, onizleme-*/) .gitignore'dadır; bu betik her seferinde yeniden üretir.
"""
import json
import os
import re
import shutil
import subprocess
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
ORTAK = os.path.join(KITAP, "yerel-ortak")
sys.path.insert(0, ORTAK)
import kur_ortak as KO  # noqa: E402

# no: (HUD'daki yer, altbilgi konusu, akçe çubuğu %) — 9/03 ünitesinin 2–4. sayfalarıyla aynı
SAYFA = {
    1: ('1. durak · <b>Göbeklitepe</b>', '1. durak · Atom modellerinin yolculuğu', 0),
    2: ('2. durak · <b>Harran</b>', '2. durak · Altın levha deneyi (çizgi roman)', 7),
    3: ('3. durak · <b>Höyük</b>', '3. durak · Bohr’un enerji merdiveni', 16),
}
SIMDI = {1: 0, 2: 1, 3: 2}

u = KO.Unite(__file__, SAYFA, SIMDI)
u.baslangic = 2                      # örnek sayfalar ünitede 2., 3. ve 4. sayfadır
import tema as TM  # noqa: E402
import konu_karakterleri as KK  # noqa: E402
import hap_bilgi as HB  # noqa: E402
import infografik_gelistirme as IG  # noqa: E402
import sahneler_gelistirme as SG  # noqa: E402

u.modul(IG)
u.modul(SG)
u.ek_defs = KK.semboller()


def kk(kimlik, cls=""):
    return f'<svg class="kk {cls}" viewBox="{KK.vb(kimlik)}"><use href="#{kimlik}"/></svg>'


u.yer_tutucu("kk", kk)
u.yer_tutucu("hbi", lambda ad, cls="hbi": HB.ikon(ad, cls))
u.yer_tutucu("ok", lambda: HB.ok())
u.yer_tutucu("siklik", HB.siklik)

CSS = [(os.path.join(ORTAK, "stil.css"), r'<link rel="stylesheet" href="[^"]*yerel-ortak/stil\.css">'),
       (os.path.join(BURA, "gelistirme.css"), r'<link rel="stylesheet" href="uretec/gelistirme\.css">')]
RENDER = os.path.join(ORTAK, "render.js")


def yaz(yol, metin):
    with open(yol, "w", encoding="utf-8") as fp:
        fp.write(metin)
    print(f"{os.path.relpath(yol, KITAP)} yazıldı ({len(metin) / 1024:.0f} KB)")


def sablon_kur(ad_sablon):
    u.sayac = 0
    with open(os.path.join(BURA, ad_sablon), encoding="utf-8") as fp:
        return u._cozumle(fp.read())


def tema_kur(ad):
    """Şablonu (Van Gölü renkleriyle) kur, temayı uygula, atom-modelleri-<ad>.html yaz."""
    TM.AKTIF = ad
    html = sablon_kur("sablon.html")
    hedef = os.path.join(KLASOR, f"atom-modelleri-{ad}.html")
    html = TM.tema_html(html, ad, CSS, hedef, ORTAK)
    html = html.replace("<title>Kimya Rotası 9 · Atom modelleri · geliştirme örneği</title>",
                        f"<title>Kimya Rotası 9 · Atom modelleri · {TM.TEMALAR[ad]['ad']} teması</title>")
    yaz(hedef, html)
    return hedef


def bas(html, png_klasor, pdfsiz=False):
    """render.js: PDF + PNG + taşma denetimi. PNG'ler onizleme/<png_klasor>/ altına taşınır. Taşma satırları döner."""
    arg = ["node", RENDER, html] + (["--pdfsiz"] if pdfsiz else [])
    cikti = subprocess.run(arg, capture_output=True, text=True, cwd=KLASOR)
    metin = cikti.stdout + cikti.stderr
    ad = os.path.splitext(os.path.basename(html))[0]
    gecici = os.path.join(KLASOR, "onizleme-" + ad)
    hedef = os.path.join(KLASOR, "onizleme", png_klasor)
    if os.path.isdir(gecici):
        os.makedirs(hedef, exist_ok=True)
        for f_ in os.listdir(gecici):
            shutil.move(os.path.join(gecici, f_), os.path.join(hedef, f_))
        shutil.rmtree(gecici)
    sorun = [l for l in metin.splitlines() if "alan dışı" in l or "taşma" in l.lower() and "Taşma yok" not in l or "HATA" in l or "Error" in l]
    print(f"  bas: {os.path.basename(html)} → {'; '.join(sorun) if sorun else 'taşma yok'}")
    if cikti.returncode:
        print(metin[-2000:])
    return sorun


def main(argv):
    tek = argv[argv.index("--tema") + 1] if "--tema" in argv else None
    htmlsiz = "--htmlsiz" in argv
    temalar = [tek] if tek else TM.SIRA
    sorunlar = {}
    if "--katalog" not in argv:
        for ad in temalar:
            html = os.path.join(KLASOR, f"atom-modelleri-{ad}.html") if htmlsiz else tema_kur(ad)
            sorunlar[ad] = bas(html, ad, pdfsiz="--pdfsiz" in argv)
    if tek:
        return sorunlar
    import katalog_kur  # noqa: E402  (katalog, karşılaştırma, renk denetimi)
    katalog_kur.hepsi(u, sablon_kur, bas, yaz, KLASOR, CSS, "--katalog" in argv)
    return sorunlar


if __name__ == "__main__":
    main(sys.argv[1:])
