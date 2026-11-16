"""Katalog sayfaları (K1 Hap Bilgi · K2 renk temaları · K3 konu karakterleri), tema karşılaştırma levhası ve renk denetimi.

kur.py çağırır: katalog_kur.hepsi(u, sablon_kur, bas, yaz, KLASOR, yalniz_katalog)
Renk denetimi iki yoldan yapılır:
  1. Token çiftleri (tema değerlerinden): WCAG kontrast oranı ve döteranopi benzetiminde OKLab uzaklığı (ΔE·100).
  2. PNG'ler: her temanın s01.png'si Machado (2009) döteranopi matrisiyle (doğrusal RGB) boyanır → onizleme/renk-korlugu.png.
Sonuçlar onizleme/renk-denetimi.json'a ve K2 sayfasına yazılır.
"""
import json
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import konu_karakterleri as KK
import tema as TM

KITAP_FONT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "fontlar"))
MACHADO_DOTERANOPI = np.array([[0.367322, 0.860646, -0.227968],
                               [0.280085, 0.672501, 0.047413],
                               [-0.011820, 0.042940, 0.968881]])

# ------------------------------------------------------------------ renk denetimi

KONTRAST = [  # (ad, yazı tokenı, zemin tokenı, eşik)
    ("gövde · obs / kar", "obs", "kar", 7.0),
    ("etiket · gol-k / beyaz", "gol-k", "#FFFFFF", 4.5),
    ("etiket · gol-k / gol-aa", "gol-k", "gol-aa", 4.5),
    ("akçe · keh-k / keh-a", "keh-k", "keh-a", 4.5),
    ("Tuzak · mer-k / mer-a", "mer-k", "mer-a", 4.5),
    ("kavram · kob-k / kob-a", "kob-k", "kob-a", 4.5),
    ("Doğrusu · zumrut / beyaz", "zumrut", "#FFFFFF", 4.5),
    ("HUD · beyaz / obs", "#FFFFFF", "obs", 7.0),
    ("HUD · keh / obs", "keh", "obs", 4.5),
    ("çip · beyaz / gol", "#FFFFFF", "gol", 3.0),
    ("Tuzak başlığı · beyaz / mer", "#FFFFFF", "mer", 3.0),
    ("kurdele · beyaz / kob", "#FFFFFF", "kob", 3.0),
    ("tezhip · altin-a / lajver", "altin-a", "lajver", 4.5),
]
CIFTLER = [  # (ad, a, b, neden)
    ("Yanlış ↔ Doğru", "mer", "zumrut", "çarpı/tik, mühür"),
    ("Tuzak ↔ ana renk", "mer", "gol", "başlık şeridi"),
    ("Akçe ↔ Tuzak", "keh", "mer", "çip / başlık"),
    ("Ana renk ↔ kavram", "gol", "kob", "etiket renkleri"),
    ("Ana renk ↔ akçe", "gol", "keh", "kapsül kapakları"),
    ("Elif ↔ Pamuk balonu", "mer-a", "keh-a", "balon zemini"),
    ("Yanlış ↔ doğru zemini", "mer-a", "gol-aa", "ikili kart"),
    ("Kavram ↔ erguvan", "kob", "erguvan", "gün batımı / rozet"),
]


def _renk(es, k):
    return k if k.startswith("#") else es.token(k)


def _doteranopi_hex(h):
    rgb = np.array([TM._lin(v) for v in TM.hex_rgb(h)])
    y = np.clip(MACHADO_DOTERANOPI @ rgb, 0, 1)
    return TM.rgb_hex(tuple(TM._gam(v) for v in y))


def _dE(a, b):
    la, lb = TM.oklab(a), TM.oklab(b)
    return 100 * sum((x - y) ** 2 for x, y in zip(la, lb)) ** .5


def renk_denetimi():
    sonuc = {}
    for ad in TM.SIRA:
        es = TM.Esleme(ad)
        k = [{"ad": n, "oran": round(TM.kontrast(_renk(es, a), _renk(es, b)), 2), "esik": e} for n, a, b, e in KONTRAST]
        c = []
        for n, a, b, neden in CIFTLER:
            ra, rb = _renk(es, a), _renk(es, b)
            c.append({"ad": n, "normal": round(_dE(ra, rb), 1), "doteranopi": round(_dE(_doteranopi_hex(ra), _doteranopi_hex(rb)), 1), "ipucu": neden})
        sonuc[ad] = {"kontrast": k, "ciftler": c}
    return sonuc


def _durum(d):
    return "sorun" if d < 6 else ("dikkat" if d < 12 else "iyi")


def png_doteranopi(png):
    im = np.asarray(Image.open(png).convert("RGB")).astype(np.float32) / 255
    lin = np.where(im <= .04045, im / 12.92, ((im + .055) / 1.055) ** 2.4)
    y = np.clip(lin @ MACHADO_DOTERANOPI.T, 0, 1)
    srgb = np.where(y <= .0031308, 12.92 * y, 1.055 * y ** (1 / 2.4) - .055)
    return Image.fromarray((srgb * 255 + .5).astype(np.uint8))


def _font(boy, kalin=True):
    yol = os.path.join(KITAP_FONT, "baloobhaijaan2", "static", "BalooBhaijaan2-800.ttf" if kalin else "BalooBhaijaan2-500.ttf")
    return ImageFont.truetype(yol, boy)


def _govde_font(boy):
    return ImageFont.truetype(os.path.join(KITAP_FONT, "nunito", "static", "Nunito-700.ttf"), boy)


def karsilastirma(klasor, sayfa="s01", genislik=700):
    """Aynı sayfa beş temada yan yana → onizleme/karsilastirma.png"""
    resimler = [Image.open(os.path.join(klasor, "onizleme", ad, f"{sayfa}.png")).convert("RGB") for ad in TM.SIRA]
    yuk = round(resimler[0].height * genislik / resimler[0].width)
    kenar, ara, ust = 36, 28, 118
    W = kenar * 2 + len(resimler) * genislik + (len(resimler) - 1) * ara
    H = ust + yuk + 70
    levha = Image.new("RGB", (W, H), "#EEF2F4")
    d = ImageDraw.Draw(levha)
    d.text((kenar, 18), "Renk temaları · aynı sayfa beş palette (s.2 · Modellerin yolculuğu)", font=_font(40), fill="#1B1D26")
    for i, (ad, im) in enumerate(zip(TM.SIRA, resimler)):
        x = kenar + i * (genislik + ara)
        t = TM.TEMALAR[ad]
        d.text((x, 70), f"{i + 1}. {t['ad']}", font=_font(30), fill="#1B1D26")
        k = im.resize((genislik, yuk), Image.LANCZOS)
        d.rectangle([x - 2, ust - 2, x + genislik + 1, ust + yuk + 1], fill="#1B1D26")
        levha.paste(k, (x, ust))
        for j, tok in enumerate(("gol", "keh", "mer", "kob", "obs", "kar")):
            d.rectangle([x + j * 46, ust + yuk + 16, x + j * 46 + 40, ust + yuk + 46], fill=TM.Esleme(ad).token(tok), outline="#1B1D26", width=2)
        d.text((x + 6 * 46 + 8, ust + yuk + 16), "gol · keh · mer · kob · obs · kar", font=_govde_font(20), fill="#56636E")
    hedef = os.path.join(klasor, "onizleme", "karsilastirma.png")
    levha.save(hedef, optimize=True)
    return hedef


def renk_korlugu_levhasi(klasor, genislik=380):
    """Her tema için s01: üstte normal, altta döteranopi benzetimi → onizleme/renk-korlugu.png"""
    kenar, ara, ust = 30, 20, 96
    ornek = Image.open(os.path.join(klasor, "onizleme", TM.SIRA[0], "s01.png"))
    yuk = round(ornek.height * genislik / ornek.width)
    W = kenar * 2 + len(TM.SIRA) * genislik + (len(TM.SIRA) - 1) * ara
    H = ust + 2 * yuk + 3 * 40
    levha = Image.new("RGB", (W, H), "#EEF2F4")
    d = ImageDraw.Draw(levha)
    d.text((kenar, 14), "Döteranopi benzetimi (Machado 2009, doğrusal RGB) · üst: normal görme · alt: döteranop", font=_font(30), fill="#1B1D26")
    for i, ad in enumerate(TM.SIRA):
        png = os.path.join(klasor, "onizleme", ad, "s01.png")
        x = kenar + i * (genislik + ara)
        d.text((x, 58), TM.TEMALAR[ad]["ad"], font=_font(26), fill="#1B1D26")
        n = Image.open(png).convert("RGB").resize((genislik, yuk), Image.LANCZOS)
        s = png_doteranopi(png).resize((genislik, yuk), Image.LANCZOS)
        levha.paste(n, (x, ust))
        levha.paste(s, (x, ust + yuk + 40))
        d.text((x, ust + yuk + 8), "döteranop görüş:", font=_govde_font(20), fill="#56636E")
    hedef = os.path.join(klasor, "onizleme", "renk-korlugu.png")
    levha.save(hedef, optimize=True)
    os.makedirs(os.path.join(klasor, "gorsel"), exist_ok=True)
    levha.resize((levha.width // 2, levha.height // 2), Image.LANCZOS).save(os.path.join(klasor, "gorsel", "renk-korlugu-kucuk.jpg"), quality=84)
    return hedef


# ------------------------------------------------------------------ katalog yer tutucuları

SWATCH = ["kar", "obs", "gol", "gol-k", "gol-a", "derin", "keh", "keh-a", "mer", "kob", "kob-a", "zumrut"]


def tema_satirlari():
    out = []
    for ad in TM.SIRA:
        t = TM.TEMALAR[ad]
        es = TM.Esleme(ad)
        hucre = "".join(f'<div class="rk"><i style="background:{es.token(k)}"></i><span>{k}<em>{es.token(k)}</em></span></div>' for k in SWATCH)
        out.append(f'<tr><td class="ad"><b>{t["ad"]}</b><small>{t["aciklama"]}</small></td><td><div class="renk-sira">{hucre}</div></td></tr>')
    return "".join(out)


def tema_onizleme(klasor):
    gorsel = os.path.join(klasor, "gorsel")
    os.makedirs(gorsel, exist_ok=True)
    out = []
    for ad in TM.SIRA:
        png = os.path.join(klasor, "onizleme", ad, "s01.png")
        hedef = os.path.join(gorsel, f"kucuk-{ad}.jpg")
        if os.path.exists(png):
            im = Image.open(png).convert("RGB")
            im.resize((420, round(im.height * 420 / im.width)), Image.LANCZOS).save(hedef, quality=84)
        out.append(f'<figure><img src="gorsel/kucuk-{ad}.jpg" alt="{TM.TEMALAR[ad]["ad"]}"><figcaption>{TM.TEMALAR[ad]["ad"]}</figcaption></figure>')
    return "".join(out)


def kontrast_tablosu(rd):
    bas = "".join(f"<th>{TM.TEMALAR[ad]['ad'].split()[0]}</th>" for ad in TM.SIRA)
    satir = []
    for i, (n, a, b, e) in enumerate(KONTRAST):
        hucre = ""
        for ad in TM.SIRA:
            o = rd[ad]["kontrast"][i]["oran"]
            hucre += f'<td{" class=zayif" if o < e else ""}>{o:.1f}</td>'.replace(".", ",")
        satir.append(f"<tr><td>{n} <small>≥ {str(e).replace('.', ',')}</small></td>{hucre}</tr>")
    return f'<table class="kontrast-tablo"><tr><th>yazı / zemin</th>{bas}</tr>{"".join(satir)}</table>'


def renk_korlugu_notu(rd):
    """K2 için kısa notlar: her temada döteranopide yakınlaşan çiftler."""
    sat = []
    for i, (n, a, b, neden) in enumerate(CIFTLER):
        d = [rd[ad]["ciftler"][i]["doteranopi"] for ad in TM.SIRA]
        dn = [rd[ad]["ciftler"][i]["normal"] for ad in TM.SIRA]
        hucre = "".join(f'<td{" class=zayif" if _durum(x) == "sorun" else ""}>{str(x).replace(".", ",")}</td>' for x in d)
        sat.append(f"<tr><td>{n} <small>{neden}</small></td>{hucre}</tr>")
    bas = "".join(f"<th>{TM.TEMALAR[ad]['ad'].split()[0]}</th>" for ad in TM.SIRA)
    tablo = f'<table class="kontrast-tablo"><tr><th>çift (ΔE·100, döteranop)</th>{bas}</tr>{"".join(sat)}</table>'
    notlar = ('<ul class="notlar" style="margin-top:1.2mm">'
              '<li>ΔE &lt; 6 <b>sorun</b> (kırmızı), 6–12 dikkat. Yalnız iki açık zemin çifti kalıyor; ikisinde de biçim ipucu var (kesik çizgili Pamuk balonu, çarpı/tik + üstü çizili yazı).</li>'
              '<li><b>Yanlış ↔ Doğru</b> (kırmızı/yeşil) döteranopta yakınlaşır (ΔE 8–15): anlam hiçbir yerde yalnız renkle verilmez.</li>'
              '<li>Ayarlanan: Selçuklu’da Tuzak koyu kırmızı (ana renk terakotadan ayrılsın), Rasathane’de kavram açık erguvan.</li></ul>')
    return tablo + notlar


def kk_izgara():
    out = []
    for k, vb, ad, aciklama in KK.katalog():
        out.append(f'<div class="kk-hucre"><svg viewBox="{vb}"><use href="#{k}"/></svg><b>{ad}</b><code>#{k}</code><small>{aciklama}</small></div>')
    return "".join(out)


def ifade_serit():
    ids = [("kk-elektron", "mutlu"), ("kk-elektron-heyecan", "heyecanlı"), ("kk-elektron-sasiran", "şaşkın"), ("kk-elektron-sakin", "rahat"),
           ("kk-elektron-sersem", "sersem"), ("kk-alfa", "kararlı"), ("kk-alfa-mutlu", "mutlu"), ("kk-alfa-sasiran", "şaşkın"),
           ("kk-alfa-sersem", "sersem"), ("kk-dalton-sasiran", "Dalton · şaşkın"), ("kk-thomson-endiseli", "Thomson · endişeli"),
           ("kk-cekirdek-sasiran", "çekirdek · şaşkın")]
    return "".join(f'<div><svg viewBox="{KK.vb(k)}"><use href="#{k}"/></svg>{ad}</div>' for k, ad in ids)


def hepsi(u, sablon_kur, bas, yaz, klasor, css, yalniz_katalog=False):
    import kur_ortak as KO
    rd = renk_denetimi()
    with open(os.path.join(klasor, "onizleme", "renk-denetimi.json"), "w", encoding="utf-8") as fp:
        json.dump(rd, fp, ensure_ascii=False, indent=1)
    var_png = all(os.path.exists(os.path.join(klasor, "onizleme", ad, "s01.png")) for ad in TM.SIRA)
    if var_png:
        print(os.path.relpath(karsilastirma(klasor)), "·", os.path.relpath(renk_korlugu_levhasi(klasor)))

    def hudk(metin, sag=""):
        return (f'<header class="hud"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>{u.sinif_adi}</span>'
                f'<span class="yer">Geliştirme · {metin}</span><span class="sag-not">{sag}</span></header>')

    def altk(kod, konu):
        return (f'<footer class="alt"><span>{u.sinif_adi} · Atom modelleri örneği</span><span>{konu}</span>'
                f'<span class="no"><svg viewBox="0 0 100 100"><use href="#no-yildiz"/></svg><b style="font-size:8.6pt">{kod}</b></span></footer><div class="ebru-alt"></div>')

    u.yer_tutucu("hudk", hudk)
    u.yer_tutucu("altk", altk)
    u.yer_tutucu("tema-satirlari", tema_satirlari)
    u.yer_tutucu("tema-onizleme", lambda: tema_onizleme(klasor))
    u.yer_tutucu("kontrast-tablosu", lambda: kontrast_tablosu(rd))
    u.yer_tutucu("renk-korlugu-notu", lambda: renk_korlugu_notu(rd))
    u.yer_tutucu("kk-izgara", kk_izgara)
    u.yer_tutucu("ifade-serit", ifade_serit)
    TM.AKTIF = "van-golu"
    html = sablon_kur("katalog.html")
    hedef = os.path.join(klasor, "hap-bilgi-katalog.html")
    html = TM.tema_html(html, "van-golu", css, hedef, KO.ORTAK)
    yaz(hedef, html)
    bas(hedef, "katalog")
    kl = os.path.join(klasor, "onizleme", "katalog")
    for kaynak, ad in (("s01.png", "hap-bilgi.png"), ("s02.png", "temalar.png"), ("s03.png", "renk-denetimi.png"), ("s04.png", "karakterler.png")):
        if os.path.exists(os.path.join(kl, kaynak)):
            shutil.move(os.path.join(kl, kaynak), os.path.join(klasor, "onizleme", ad))
    shutil.rmtree(kl, ignore_errors=True)
    return rd
