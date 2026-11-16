#!/usr/bin/env python3
"""Karma temalar · 9. sınıf "Çini ve Toprak" + 10. sınıf "Göl ve Rasathane" örnekleri — kurucu.

    python3 uretec/kur.py              iki sınıf örneği + katalog + karşılaştırma + renk denetimi
    python3 uretec/kur.py --sinif 10   yalnız bir sınıf (hızlı deneme) · --pdfsiz yalnız PNG · --katalog yalnız katalog

Modüller: bu klasör (tema.py, konu_karakterleri.py: karma paletler ve gaz karakterleri; kopyalanıp genişletildi) +
atom-modelleri/uretec (hap_bilgi, infografik_gelistirme, sahneler_gelistirme, gelistirme.css, sablon.html: salt okunur).
atom-modelleri çıktılarına dokunulmaz. Ortak motor: yerel-ortak/kur_ortak.py.
"""
import os
import re
import shutil
import subprocess
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
ORTAK = os.path.join(KITAP, "yerel-ortak")
ATOM = os.path.join(KITAP, "gelistirme", "atom-modelleri", "uretec")
sys.path.insert(0, ORTAK)
sys.path.insert(0, ATOM)
sys.path.insert(0, BURA)                      # önce bu klasör: tema, konu_karakterleri (genişletilmiş kopyalar)
import kur_ortak as KO  # noqa: E402
import tema as TM  # noqa: E402
import konu_karakterleri as KK  # noqa: E402
import hap_bilgi as HB  # noqa: E402
import infografik_gelistirme as IG  # noqa: E402
import sahneler_gelistirme as SG  # noqa: E402
import infografik_karma as IK  # noqa: E402
import sahneler_karma as SK  # noqa: E402
from cizim import sus as U  # noqa: E402

CSS = [(os.path.join(ORTAK, "stil.css"), r'<link rel="stylesheet" href="[^"]*yerel-ortak/stil\.css">'),
       (os.path.join(ATOM, "gelistirme.css"), r'<link rel="stylesheet" href="uretec/gelistirme\.css">'),
       (os.path.join(BURA, "karma.css"), r'<link rel="stylesheet" href="uretec/karma\.css">')]
RENDER = os.path.join(ORTAK, "render.js")
DEFS = KK.semboller()


def ortak_yer_tutucular(u):
    u.ek_defs = DEFS
    u.yer_tutucu("kk", lambda kimlik, cls="": f'<svg class="kk {cls}" viewBox="{KK.vb(kimlik)}"><use href="#{kimlik}"/></svg>')
    u.yer_tutucu("hbi", lambda ad, cls="hbi": HB.ikon(ad, cls))
    u.yer_tutucu("ok", lambda: HB.ok())
    u.yer_tutucu("siklik", HB.siklik)


# ------------------------------------------------------------------ 9. sınıf · atom modelleri (9/03 s.2–4)
SAYFA9 = {1: ('1. durak · <b>Göbeklitepe</b>', '1. durak · Atom modellerinin yolculuğu', 0),
          2: ('2. durak · <b>Harran</b>', '2. durak · Altın levha deneyi (çizgi roman)', 7),
          3: ('3. durak · <b>Höyük</b>', '3. durak · Bohr’un enerji merdiveni', 16)}
u9 = KO.Unite(os.path.join(BURA, "s9", "kur.py"), SAYFA9, {1: 0, 2: 1, 3: 2})
u9.baslangic = 2
u9.modul(IG)
u9.modul(SG)
ortak_yer_tutucular(u9)

# ------------------------------------------------------------------ 10. sınıf · Gazlar (10/04 s.3, 5, 6)
SAYFA10 = {1: ('2. durak · <b>Göreme</b>', '2. durak · Boyle ve Charles', 7),
           2: ('4. durak · <b>Kızılçukur</b>', '4. durak · Kinetik teori ve ideal gaz', 29),
           3: ('5. durak · <b>Derinkuyu</b>', '5. durak · Yoğunluk ve yayılma', 39)}
u10 = KO.Unite(os.path.join(BURA, "s10", "kur.py"), SAYFA10, {1: 1, 2: 3, 3: 4})
u10.sayfa_no = lambda n: {1: 3, 2: 5, 3: 6}[int(n)]          # ünitedeki gerçek sayfa numaraları
u10.modul(IG)
u10.modul(IK)
u10.modul(SK)
ortak_yer_tutucular(u10)
u10.yer_tutucu("muhur", lambda tur, boy="": U.muhur(u10.yeni("mh"), tur, alt="KAPADOKYA YOLU"))

KITAPLAR = {  # sınıf: (Unite, şablon yolu, palet, çıktı adı, başlık)
    9: (u9, os.path.join(ATOM, "sablon.html"), "cini-toprak", "karma-9-cini-toprak", "Kimya Rotası 9 · Atom modelleri · Çini ve Toprak"),
    10: (u10, os.path.join(BURA, "sablon10.html"), "gol-rasathane", "karma-10-gol-rasathane", "Kimya Rotası 10 · Gazlar · Göl ve Rasathane"),
}


def yaz(yol, metin):
    with open(yol, "w", encoding="utf-8") as fp:
        fp.write(metin)
    print(f"{os.path.relpath(yol, KITAP)} yazıldı ({len(metin) / 1024:.0f} KB)")


def sablon_kur(u, yol):
    u.sayac = 0
    with open(yol, encoding="utf-8") as fp:
        metin = fp.read()
    if "uretec/karma.css" not in metin:
        metin = metin.replace("</head>", '<link rel="stylesheet" href="uretec/karma.css">\n</head>', 1)
    return u._cozumle(metin)


def kitap_kur(sinif):
    u, sablon, palet, ad, baslik = KITAPLAR[sinif]
    TM.AKTIF = palet
    html = sablon_kur(u, sablon)
    html = re.sub(r"<title>.*?</title>", f"<title>{baslik}</title>", html, count=1)
    hedef = os.path.join(KLASOR, ad + ".html")
    yaz(hedef, TM.tema_html(html, palet, CSS, hedef, ORTAK))
    return hedef


def bas(html, png_klasor, pdfsiz=False):
    """render.js: PDF + PNG + taşma denetimi; PNG'ler onizleme/<png_klasor>/ altına."""
    cikti = subprocess.run(["node", RENDER, html] + (["--pdfsiz"] if pdfsiz else []), capture_output=True, text=True, cwd=KLASOR)
    metin = cikti.stdout + cikti.stderr
    ad = os.path.splitext(os.path.basename(html))[0]
    gecici = os.path.join(KLASOR, "onizleme-" + ad)
    hedef = os.path.join(KLASOR, "onizleme", png_klasor)
    if os.path.isdir(gecici):
        os.makedirs(hedef, exist_ok=True)
        for f_ in os.listdir(gecici):
            shutil.move(os.path.join(gecici, f_), os.path.join(hedef, f_))
        shutil.rmtree(gecici)
    sorun = [l for l in metin.splitlines() if "alan dışı" in l or ("taşma" in l.lower() and "Taşma yok" not in l) or "HATA" in l or "Error" in l]
    print(f"  bas: {os.path.basename(html)} → {'; '.join(sorun) if sorun else 'taşma yok'}")
    if cikti.returncode:
        print(metin[-2000:])
    return sorun


def main(argv):
    tek = int(argv[argv.index("--sinif") + 1]) if "--sinif" in argv else None
    if "--katalog" not in argv:
        for sinif in ([tek] if tek else (9, 10)):
            ad = KITAPLAR[sinif][3]
            bas(kitap_kur(sinif), ad.replace("karma-", ""), pdfsiz="--pdfsiz" in argv)
    if tek:
        return
    import katalog_karma  # noqa: E402
    katalog_karma.hepsi(u10, sablon_kur, bas, yaz, KLASOR, CSS, ORTAK)


if __name__ == "__main__":
    main(sys.argv[1:])
