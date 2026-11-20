#!/usr/bin/env python3
"""3B (anaglif) örneği · kurucu: 4 sayfa → uc-boyut-ornek.pdf + onizleme/s01–s04.png.

    python3 uretec/kur.py            görseller yoksa üretir, iki HTML'i kurar, basar (render.js), PDF'leri birleştirir
    python3 uretec/kur.py --gorsel   görselleri (anaglif, düz resim, test, GIF) baştan üretir
    python3 uretec/kur.py --pdfsiz   yalnız PNG (hızlı deneme) · --sayfa 2  yalnız o sayfanın bulunduğu kitap

Sayfa → künye (meta.json) → palet:
    s1 Moleküllerin gerçek şekli   9/06 Kimyasal Etkileşimler (s9-06)   Çini ve Toprak
    s2 Kristalin içine gir         9/09 Katılar (s9-09)                 Çini ve Toprak
    s3 Tanecikler üç boyutta       10/04 Gazlar (s10-04)                Göl ve Rasathane
    s4 3B gözlüğünü hazırla        9. sınıf eki (s9-06 künyesiyle)       Çini ve Toprak
Bir HTML tek paletle kurulabildiği için iki HTML üretilir (uc-boyut-9.html: s1, s2, s4 · uc-boyut-10.html: s3);
PDF'ler pypdf ile sayfa sırasına göre birleştirilir. Ortak motor: yerel-ortak/kur_ortak.py (salt okunur).
Palet ve Hap Bilgi modülleri karma-temalar/uretec ve atom-modelleri/uretec'ten salt okunur içe aktarılır.
"""
import sys
sys.dont_write_bytecode = True               # başka klasörlere __pycache__ yazılmasın
import json
import os
import re
import shutil
import subprocess

BURA = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.dirname(BURA)
KITAP = os.path.abspath(os.path.join(KLASOR, "..", ".."))
ORTAK = os.path.join(KITAP, "yerel-ortak")
ATOM = os.path.join(KITAP, "gelistirme", "atom-modelleri", "uretec")
KARMA = os.path.join(KITAP, "gelistirme", "karma-temalar", "uretec")
for yol in (ORTAK, ATOM, KARMA, BURA):       # sonda eklenen önce aranır: bu klasör > karma (tema.py) > atom (hap_bilgi.py)
    sys.path.insert(0, yol)
import kur_ortak as KO  # noqa: E402
import tema as TM  # noqa: E402            (karma-temalar: iki sınıf paleti)
import hap_bilgi as HB  # noqa: E402       (atom-modelleri: Hap Bilgi ailesi ikonları)
import sahneler_uc as SU  # noqa: E402
import gorseller as G  # noqa: E402

CSS = [(os.path.join(ORTAK, "stil.css"), r'<link rel="stylesheet" href="[^"]*yerel-ortak/stil\.css">'),
       (os.path.join(ATOM, "gelistirme.css"), r'<link rel="stylesheet" href="uretec/gelistirme\.css">'),
       (os.path.join(BURA, "uc_boyut.css"), r'<link rel="stylesheet" href="uretec/uc_boyut\.css">')]
RENDER = os.path.join(ORTAK, "render.js")
CIKTI = "uc-boyut-ornek"

# sayfa no: (HUD'daki yer, altbilgi konusu, akçe çubuğu %)
u6 = KO.Unite(os.path.join(BURA, "s9-06", "kur.py"),
              {1: ('5. durak · <b>Hasan Dağı</b>', '5. durak · Molekül şekli ve polarlık (3B)', 62),
               4: ('Ek · <b>3B gözlük</b>', 'Ek · 3B gözlüğünü hazırla', 0)}, {1: 4, 4: -1})
u9 = KO.Unite(os.path.join(BURA, "s9-09", "kur.py"),
              {2: ('4. durak · <b>Mardin çarşısı</b>', '4. durak · Katı türleri: kristalin içi (3B)', 48)}, {2: 3})
u10 = KO.Unite(os.path.join(BURA, "s10-04", "kur.py"),
               {3: ('Yan yol · <b>3B atölyesi</b>', 'Yan yol · Gaz kutusu, 22,4 L küpü, hidratasyon (3B)', 70)}, {3: 6})
u6.sayfa_no = lambda n: {1: 6, 4: 16}[int(n)]              # ünitedeki olası sayfa numaraları (örnek)
u9.sayfa_no = lambda n: 5
u10.sayfa_no = lambda n: 8
SAYFA_UNITE = {1: u6, 2: u9, 3: u10, 4: u6}
KITAPLAR = {9: ("cini-toprak", [1, 2, 4]), 10: ("gol-rasathane", [3])}
SIRA = [(9, 1), (9, 2), (10, 1), (9, 3)]                    # birleşik PDF: (kitap, o kitaptaki sayfa)


def _bilgi():
    with open(os.path.join(G.GORSEL, "uc-boyut.json"), encoding="utf-8") as fp:
        return json.load(fp)


def yer_tutucular(u, bilgi):
    u.modul(SU)
    u.yer_tutucu("hbi", lambda ad, cls="hbi": HB.ikon(ad, cls))
    u.yer_tutucu("ok", lambda: HB.ok())
    u.yer_tutucu("siklik", HB.siklik)

    def ana(ad):
        b = bilgi[ad]
        return (f'<img class="ana" src="gorsel/ana-{ad}.png" alt="3B (anaglif) resim: {ad}" data-ayriklik="{b["ayriklik_mm"]}" '
                f'style="width:{b["en_mm"]}mm;height:{b["yuk_mm"]}mm">')

    def duz(ad):
        en, yuk = G.YAPILAR[ad][4]
        return f'<img class="duz" src="gorsel/duz-{ad}.png" alt="düz resim: {ad}" style="width:{en}mm;height:{yuk}mm">'

    def test(ad):
        en, yuk = {"yazi": (54, 13), "derinlik": (54, 20)}[ad]
        return f'<img class="ana" src="gorsel/test-{ad}.png" alt="gözlük testi" style="width:{en}mm;height:{yuk}mm">'

    u.yer_tutucu("ana", ana)
    u.yer_tutucu("duz", duz)
    u.yer_tutucu("test", test)


def html_kur(sinif):
    """Şablonu sayfalara böl, her sayfayı kendi künyesiyle çöz, sınıfın paletini uygula."""
    palet, sayfalar = KITAPLAR[sinif]
    TM.AKTIF = palet
    with open(os.path.join(BURA, "sablon.html"), encoding="utf-8") as fp:
        sablon = fp.read()
    bolum = re.findall(r'<section class="sayfa s(\d)">.*?</section>', sablon, flags=re.S)
    govde = {int(m.group(1)): m.group(0) for m in re.finditer(r'<section class="sayfa s(\d)">.*?</section>', sablon, flags=re.S)}
    assert sorted(govde) == [1, 2, 3, 4], bolum
    bas = sablon[:sablon.index("{{defs}}")]
    for u, taban in ((u6, 0), (u9, 3000), (u10, 6000)):      # kimlik sayaçları çakışmasın (aynı HTML'de iki künye)
        u.sayac = taban
    ilk = SAYFA_UNITE[sayfalar[0]]
    html = bas + ilk._cozumle("{{defs}}") + "\n" + "\n\n".join(SAYFA_UNITE[n]._cozumle(govde[n]) for n in sayfalar) + "\n</body>\n</html>\n"
    ad = {9: "Kimya Rotası 9 · 3B örneği · Çini ve Toprak", 10: "Kimya Rotası 10 · 3B örneği · Göl ve Rasathane"}[sinif]
    html = re.sub(r"<title>.*?</title>", f"<title>{ad}</title>", html, count=1)
    hedef = os.path.join(KLASOR, f"uc-boyut-{sinif}.html")
    html = TM.tema_html(html, palet, CSS, hedef, ORTAK)
    with open(hedef, "w", encoding="utf-8") as fp:
        fp.write(html)
    print(f"{os.path.relpath(hedef, KITAP)} yazıldı ({len(html) / 1024:.0f} KB · sayfalar {sayfalar} · palet {palet})")
    return hedef


def bas(html, pdfsiz=False):
    """render.js: PDF + PNG (onizleme-<ad>/) + taşma denetimi → sorun satırları."""
    cikti = subprocess.run(["node", RENDER, html] + (["--pdfsiz"] if pdfsiz else []), capture_output=True, text=True, cwd=KLASOR)
    metin = cikti.stdout + cikti.stderr
    sorun = [l for l in metin.splitlines() if "alan dışı" in l or ("taşma" in l.lower() and "Taşma yok" not in l) or "HATA" in l or "Error" in l or "kenara taşan" in l]
    print(f"  bas: {os.path.basename(html)} → " + ("taşma yok" if not sorun else f"{len(sorun)} SORUN"))
    for l in sorun:
        print("    " + l)
    if cikti.returncode:
        print(metin[-2500:])
    return sorun


def birlestir():
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    okur = {s: PdfReader(os.path.join(KLASOR, f"uc-boyut-{s}.pdf")) for s in KITAPLAR}
    for s, n in SIRA:
        w.add_page(okur[s].pages[n - 1])
    w.add_metadata({"/Title": "Kimya Rotası · 3B moleküller (anaglif) · tasarım örneği"})
    hedef = os.path.join(KLASOR, CIKTI + ".pdf")
    with open(hedef, "wb") as fp:
        w.write(fp)
    t3 = subprocess.run(["pdffonts", hedef], capture_output=True, text=True).stdout.count("Type 3")
    print(f"{os.path.relpath(hedef, KITAP)} · {len(SIRA)} sayfa · {os.path.getsize(hedef) / 1048576:.2f} MB · Type 3 font: {t3}")
    for s in KITAPLAR:
        os.remove(os.path.join(KLASOR, f"uc-boyut-{s}.pdf"))
    return t3


def onizlemeleri_topla():
    hedef = os.path.join(KLASOR, "onizleme")
    os.makedirs(hedef, exist_ok=True)
    for i, (s, n) in enumerate(SIRA, 1):
        kaynak = os.path.join(KLASOR, f"onizleme-uc-boyut-{s}", f"s{n:02d}.png")
        if os.path.exists(kaynak):
            shutil.move(kaynak, os.path.join(hedef, f"s{i:02d}.png"))
    for s in KITAPLAR:
        shutil.rmtree(os.path.join(KLASOR, f"onizleme-uc-boyut-{s}"), ignore_errors=True)


def main(argv):
    if "--gorsel" in argv or not os.path.exists(os.path.join(G.GORSEL, "uc-boyut.json")):
        G.main([])
    bilgi = _bilgi()
    for u in (u6, u9, u10):
        yer_tutucular(u, bilgi)
    pdfsiz = "--pdfsiz" in argv
    tek = int(argv[argv.index("--sayfa") + 1]) if "--sayfa" in argv else None
    sorun = []
    for sinif, (_, sayfalar) in KITAPLAR.items():
        if tek and tek not in sayfalar:
            continue
        sorun += bas(html_kur(sinif), pdfsiz=pdfsiz or bool(tek))
    onizlemeleri_topla() if not tek else None
    if not pdfsiz and not tek:
        birlestir()
    return sorun


if __name__ == "__main__":
    main(sys.argv[1:])
