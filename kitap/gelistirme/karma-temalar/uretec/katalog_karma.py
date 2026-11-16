"""Karma katalog: K1 iki palet · K2 9↔10 karşılaştırma · K3 renk denetimi · K4 güncel konu karakterleri kiti.

kur.py çağırır: katalog_karma.hepsi(u10, sablon_kur, bas, yaz, KLASOR, CSS, ORTAK)
Renk denetimi atom-modelleri/uretec/katalog_kur.py yardımcılarıyla yapılır (aynı WCAG ve Machado 2009 döteranopi
yöntemi) ve iki palete özgü vurgu çiftleri (HUD, levha, altbilgi, koyu kart) eklenir.
"""
import json
import os
import shutil

from PIL import Image, ImageDraw

import katalog_kur as K           # atom-modelleri/uretec (salt okunur)
import konu_karakterleri as KK    # bu klasör (gaz karakterleri eklendi)
import tema as TM                 # bu klasör (karma paletler)

KITAPLAR = [("9-cini-toprak", "cini-toprak", "9. sınıf · Çini ve Toprak"),
            ("10-gol-rasathane", "gol-rasathane", "10. sınıf · Göl ve Rasathane")]
# temaların css vurgu katmanındaki renkler (tema.py TEMALAR[ad]["css"]) · (ad, yazı, zemin, eşik)
VURGU = {
    "cini-toprak": [("HUD yeri · #E8D4BE / #2E1F17", "#E8D4BE", "#2E1F17", 4.5), ("levha etiketi · #8A3C1A / levha", "#8A3C1A", "#FFF9F0", 4.5),
                    ("levha başlık (25 pt) · #B4532C", "#B4532C", "#FFF9F0", 3.0), ("altbilgi · #7C3416 / kar", "#7C3416", "#FFFFFF", 4.5),
                    ("koyu kart · beyaz / #2E1F17", "#FFFFFF", "#2E1F17", 7.0)],
    "gol-rasathane": [("HUD vurgusu · #F0C24A / #10153A", "#F0C24A", "#10153A", 4.5), ("levha etiketi · #3D2F8C / levha", "#3D2F8C", "#FFFFFF", 4.5),
                      ("levha başlık (25 pt) · #0E8F93", "#0E8F93", "#FFFFFF", 3.0), ("altbilgi · #3D2F8C / kar", "#3D2F8C", "#F9FBFD", 4.5),
                      ("koyu kart · beyaz / #14193C", "#FFFFFF", "#14193C", 7.0)],
}
EK_CIFT = [("Kavram ↔ Doğru", "kob", "zumrut", "kavram kutusu · doğru etiketi"), ("Ana renk ↔ Doğru", "gol", "zumrut", "etiket · doğru")]
IPUCU = {"Elif ↔ Pamuk balonu": "balon zemini · tint düzeltildi", "Yanlış ↔ doğru zemini": "ikili kart · biçim: kesik ↔ düz çerçeve"}
VURGU_RENK = {  # tema.py css katmanının renkleri (token tablosunda görünmez)
    "cini-toprak": [("HUD", "#2E1F17"), ("HUD yeri", "#E8D4BE"), ("levha etiketi", "#8A3C1A"), ("levha vurgusu", "#B4532C"), ("levha gölgesi", "#7C3416"), ("hedef çizgisi", "#C9952B")],
    "gol-rasathane": [("HUD", "#10153A"), ("HUD vurgusu", "#F0C24A"), ("levha etiketi", "#3D2F8C"), ("levha vurgusu", "#0E8F93"), ("levha gölgesi", "#3D2F8C"), ("hedef çizgisi", "#D4A02C")],
}
SWATCH = ["kar", "obs", "gol", "gol-k", "gol-a", "kob", "kob-a", "keh", "keh-a", "mer", "mer-a", "zumrut"]
SABIT = ["keh", "mer", "zumrut", "keh-a", "mer-a"]      # iki kitapta da aynı aile (anlam renkleri)


def renk_denetimi():
    sonuc = {}
    for _, ad, _ in KITAPLAR:
        es = TM.Esleme(ad)
        k = [{"ad": n, "oran": round(TM.kontrast(K._renk(es, a), K._renk(es, b)), 2), "esik": e} for n, a, b, e in K.KONTRAST]
        k += [{"ad": n, "oran": round(TM.kontrast(a, b), 1), "esik": e, "vurgu": True} for n, a, b, e in VURGU[ad]]
        c = []
        for n, a, b, neden in K.CIFTLER + EK_CIFT:
            ra, rb = K._renk(es, a), K._renk(es, b)
            c.append({"ad": n, "normal": round(K._dE(ra, rb), 1), "doteranopi": round(K._dE(K._doteranopi_hex(ra), K._doteranopi_hex(rb)), 1),
                      "ipucu": IPUCU.get(n, neden)})
        sonuc[ad] = {"kontrast": k, "ciftler": c}
    return sonuc


# ------------------------------------------------------------------ PNG levhaları

def _sayfalar(klasor, alt):
    return [Image.open(os.path.join(klasor, "onizleme", alt, f"s0{i}.png")).convert("RGB") for i in (1, 2, 3)]


def karsilastirma(klasor, genislik=660):
    """9. ve 10. sınıf örnek sayfaları: iki sıra × 3 sayfa, altlarında palet şeridi → onizleme/karsilastirma-9-10.png"""
    satirlar = [(_sayfalar(klasor, alt), ad, baslik) for alt, ad, baslik in KITAPLAR]
    ornek = satirlar[0][0][0]
    yuk = round(ornek.height * genislik / ornek.width)
    kenar, ara, bas_h, serit_h = 40, 26, 92, 96
    W = kenar * 2 + 3 * genislik + 2 * ara
    H = 96 + 2 * (bas_h + yuk + serit_h) + 30
    lv = Image.new("RGB", (W, H), "#EEF2F4")
    d = ImageDraw.Draw(lv)
    d.text((kenar, 22), "Kimya Rotası · iki kitap, iki karma palet (aynı seri)", font=K._font(44), fill="#1B1D26")
    y = 96
    for sayfalar, ad, baslik in satirlar:
        t = TM.TEMALAR[ad]
        es = TM.Esleme(ad)
        d.text((kenar, y + 14), baslik, font=K._font(38), fill="#1B1D26")
        tar = t["tarif"]
        d.text((kenar + 760, y + 26), f"taban {TM.TEMALAR[tar['taban']]['ad']} · vurgu {TM.TEMALAR[tar['vurgu']]['ad']} · kutular {TM.TEMALAR[tar['kutu']]['ad']}",
               font=K._govde_font(24), fill="#56636E")
        y += bas_h
        for i, im in enumerate(sayfalar):
            x = kenar + i * (genislik + ara)
            d.rectangle([x - 2, y - 2, x + genislik + 1, y + yuk + 1], fill="#1B1D26")
            lv.paste(im.resize((genislik, yuk), Image.LANCZOS), (x, y))
        y += yuk + 14
        for j, tok in enumerate(SWATCH):
            x = kenar + j * 170
            d.rectangle([x, y, x + 54, y + 54], fill=es.token(tok), outline="#1B1D26", width=2)
            d.text((x + 62, y + 2), tok, font=K._govde_font(22), fill="#1B1D26")
            d.text((x + 62, y + 28), es.token(tok), font=K._govde_font(19), fill="#56636E")
        y += serit_h - 14
    hedef = os.path.join(klasor, "onizleme", "karsilastirma-9-10.png")
    lv.save(hedef, optimize=True)
    os.makedirs(os.path.join(klasor, "gorsel"), exist_ok=True)
    lv.resize((lv.width // 2, lv.height // 2), Image.LANCZOS).save(os.path.join(klasor, "gorsel", "karsilastirma-kucuk.jpg"), quality=86)
    return hedef


def renk_korlugu(klasor, genislik=520):
    """Her kitabın s01'i normal ve döteranop görüşte + altında palet şeridi (normal · döteranop) → onizleme/renk-korlugu-9-10.png"""
    kenar, ara, ust = 30, 22, 90
    resimler = []
    for alt, ad, baslik in KITAPLAR:
        png = os.path.join(klasor, "onizleme", alt, "s01.png")
        resimler += [(ad, baslik, "normal", Image.open(png).convert("RGB")), (ad, baslik, "döteranop", K.png_doteranopi(png))]
    yuk = round(resimler[0][3].height * genislik / resimler[0][3].width)
    sw_h = 150
    W = kenar * 2 + 4 * genislik + 3 * ara
    lv = Image.new("RGB", (W, ust + yuk + sw_h + 20), "#EEF2F4")
    d = ImageDraw.Draw(lv)
    d.text((kenar, 12), "Döteranopi benzetimi (Machado 2009, doğrusal RGB) · ilk sayfa ve palet şeridi", font=K._font(30), fill="#1B1D26")
    for i, (ad, baslik, tur, im) in enumerate(resimler):
        x = kenar + i * (genislik + ara)
        d.text((x, 54), f"{baslik.split(' · ')[1]} · {tur}", font=K._govde_font(22), fill="#1B1D26")
        lv.paste(im.resize((genislik, yuk), Image.LANCZOS), (x, ust))
        es = TM.Esleme(ad)
        y = ust + yuk + 18
        bw = genislik / 6
        for j, tok in enumerate(SWATCH):
            renk = es.token(tok) if tur == "normal" else K._doteranopi_hex(es.token(tok))
            cx, cy = x + (j % 6) * bw, y + (j // 6) * 66
            d.rectangle([cx + 2, cy, cx + bw - 4, cy + 40], fill=renk, outline="#1B1D26", width=2)
            d.text((cx + 4, cy + 42), tok, font=K._govde_font(17), fill="#56636E")
    hedef = os.path.join(klasor, "onizleme", "renk-korlugu-9-10.png")
    lv.save(hedef, optimize=True)
    lv.resize((lv.width // 2, lv.height // 2), Image.LANCZOS).save(os.path.join(klasor, "gorsel", "renk-korlugu-kucuk.jpg"), quality=86)
    return hedef


# ------------------------------------------------------------------ yer tutucular

def tema_karti(i, klasor):
    alt, ad, baslik = KITAPLAR[int(i)]
    t = TM.TEMALAR[ad]
    es = TM.Esleme(ad)
    png = os.path.join(klasor, "onizleme", alt, "s01.png")
    kucuk = os.path.join(klasor, "gorsel", f"kucuk-{alt}.jpg")
    if os.path.exists(png):
        im = Image.open(png).convert("RGB")
        im.resize((360, round(im.height * 360 / im.width)), Image.LANCZOS).save(kucuk, quality=84)
    tarif = "".join(
        f'<span class="tarif"><b>{rol}</b>{TM.TEMALAR[kaynak]["ad"]}<i>' +
        "".join(f'<em style="background:{TM.Esleme(kaynak).token(k)}"></em>' for k in tok) + "</i></span>"
        for rol, kaynak, tok in (("taban", t["tarif"]["taban"], ("kar", "gol", "mer", "kob")),
                                 ("vurgu", t["tarif"]["vurgu"], ("obs", "gol", "altin", "kob")),
                                 ("kutu", t["tarif"]["kutu"], ("gol-a", "keh-a", "mer-a", "kob-a"))))
    sw = "".join(f'<div class="rk{" sabit" if k in SABIT else ""}"><i style="background:{es.token(k)}"></i><span>{k}<em>{es.token(k)}</em></span></div>' for k in SWATCH)
    vurgu = {"cini-toprak": "kerpiç-kahve HUD ve bant çizgisi, terakota levha vurgusu ve gölgesi, altın hedef çizgisi, sıcak (ikindi) sahne ışığı",
             "gol-rasathane": "gece laciverti HUD ve bant çizgisi, çivit levha etiketi ve gölgesi, altın HUD vurgusu, alacakaranlık sahne ışığı"}[ad]
    return (f'<div class="palet-kart"><div class="pk-bas"><span class="sinif">{t["sinif"]}. sınıf</span><h3>{t["ad"]}</h3></div>'
            f'<div class="pk-ic"><div><div class="tarifler">{tarif}</div><div class="renk-sira alti">{sw}</div>'
            f'<p class="pk-not"><b>Vurgu katmanı:</b> {vurgu}.</p></div>'
            f'<img src="gorsel/kucuk-{alt}.jpg" alt="{t["ad"]}"></div></div>')


def kontrast_tablosu(rd):
    adlar = [ad for _, ad, _ in KITAPLAR]
    bas = "".join(f"<th>{TM.TEMALAR[a]['ad']}</th>" for a in adlar)
    sat = []
    for i, k in enumerate(rd[adlar[0]]["kontrast"]):
        if k.get("vurgu"):
            continue
        hucre = "".join((f'<td class="zayif">' if rd[a]["kontrast"][i]["oran"] < k["esik"] else "<td>") + f'{rd[a]["kontrast"][i]["oran"]:.1f}'.replace(".", ",") + "</td>" for a in adlar)
        sat.append(f'<tr><td>{k["ad"]} <small>≥ {str(k["esik"]).replace(".", ",")}</small></td>{hucre}</tr>')
    vurgu = []
    for a in adlar:
        for k in rd[a]["kontrast"]:
            if k.get("vurgu"):
                zayif = " class=zayif" if k["oran"] < k["esik"] else ""
                vurgu.append(f'<tr><td>{TM.TEMALAR[a]["ad"].split()[0]} · {k["ad"]} <small>≥ {str(k["esik"]).replace(".", ",")}</small></td>'
                             f'<td colspan="2"{zayif}>{str(k["oran"]).replace(".", ",")}</td></tr>')
    return (f'<table class="kontrast-tablo"><tr><th>yazı / zemin (token)</th>{bas}</tr>{"".join(sat)}'
            f'<tr><th colspan="3">vurgu katmanı (tema.py css)</th></tr>{"".join(vurgu)}</table>')


def cift_tablosu(rd):
    adlar = [ad for _, ad, _ in KITAPLAR]
    bas = "".join(f"<th>{TM.TEMALAR[a]['ad']}</th>" for a in adlar)
    sat = []
    for i, c in enumerate(rd[adlar[0]]["ciftler"]):
        hucre = "".join((f'<td class="zayif">' if rd[a]["ciftler"][i]["doteranopi"] < 6 else "<td>") +
                        f'{rd[a]["ciftler"][i]["normal"]} → {rd[a]["ciftler"][i]["doteranopi"]}'.replace(".", ",") + "</td>" for a in adlar)
        sat.append(f'<tr><td>{c["ad"]} <small>{c["ipucu"]}</small></td>{hucre}</tr>')
    return f'<table class="kontrast-tablo cift"><tr><th>çift (ΔE·100 normal → döteranop)</th>{bas}</tr>{"".join(sat)}</table>'


def gaz_izgara():
    bas = "".join(f'<div class="gh"><b>{ad}</b><small>M = {M}</small></div>' for _, _, ad, M, _ in KK.GAZLAR)
    sat = []
    for tur, etk in (("soguk", "soğuk · uykulu, yavaş"), ("", "oda sıcaklığı"), ("sicak", "sıcak · canlı, hızlı")):
        hucre = "".join(f'<div class="gc"><svg viewBox="{KK.vb("kk-gaz-" + k)}"><use href="#kk-gaz-{k}{"-" + tur if tur else ""}"/></svg></div>' for k, *_ in KK.GAZLAR)
        sat.append(f'<div class="gl">{etk}</div>{hucre}')
    return f'<div class="gaz-izgara"><div class="gl"></div>{bas}{"".join(sat)}</div>'


def vurgu_seridi():
    out = []
    for _, ad, _ in KITAPLAR:
        cip = "".join(f'<span class="vr"><i style="background:{h}"></i><b>{n}</b><em>{h}</em></span>' for n, h in VURGU_RENK[ad])
        out.append(f'<div class="vurgu-satir"><span class="vs-ad">{TM.TEMALAR[ad]["ad"]}</span>{cip}</div>')
    return "".join(out)


IFADELER = [("mutlu", "mutlu"), ("gulen", "gülen"), ("heyecan", "heyecanlı"), ("sasiran", "şaşkın"), ("kararli", "kararlı"),
            ("dusunen", "düşünceli"), ("gururlu", "gururlu"), ("sakin", "sakin"), ("endiseli", "endişeli"), ("sersem", "sersem")]


def ifade_sozlugu():
    """yuz() fonksiyonunun 10 ifadesi, aynı gövdede (He rengi). Satır içi SVG (sembol değil)."""
    from cizim.temel import Svg
    s = Svg("ifd")
    for i, (kod, _) in enumerate(IFADELER):
        s += f'<g transform="translate({i * 64} 0)">{KK.tanecik(s, KK.ATOM["He"], kod, None, sklera=kod not in ("gulen", "sakin", "sersem"))}</g>'
    svg = s.cikti(f"0 0 {len(IFADELER) * 64} 60", cls="ifade-svg")
    etk = "".join(f"<span>{ad}<code>{kod}</code></span>" for kod, ad in IFADELER)
    return f'{svg}<div class="ifade-etk">{etk}</div>'


def kk_kompakt():
    return "".join(f'<div class="kk-mini"><svg viewBox="{vb}"><use href="#{k}"/></svg><b>{ad}</b></div>'
                   for k, vb, ad, _ in KK.katalog() if not k.startswith("kk-gaz-"))


def hepsi(u, sablon_kur, bas, yaz, klasor, css, ortak):
    rd = renk_denetimi()
    with open(os.path.join(klasor, "onizleme", "renk-denetimi.json"), "w", encoding="utf-8") as fp:
        json.dump(rd, fp, ensure_ascii=False, indent=1)
    print(os.path.relpath(karsilastirma(klasor)), "·", os.path.relpath(renk_korlugu(klasor)))

    def hudk(metin, sag=""):
        return (f'<header class="hud"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>Kimya Rotası</span>'
                f'<span class="yer">Geliştirme · {metin}</span><span class="sag-not">{sag}</span></header>')

    def altk(kod, konu):
        return (f'<footer class="alt"><span>Kimya Rotası 9 · 10 · karma temalar</span><span>{konu}</span>'
                f'<span class="no"><svg viewBox="0 0 100 100"><use href="#no-yildiz"/></svg><b style="font-size:8.6pt">{kod}</b></span></footer><div class="ebru-alt"></div>')

    for ad, fn in (("hudk", hudk), ("altk", altk), ("tema-karti", lambda i: tema_karti(i, klasor)),
                   ("kontrast-tablosu", lambda: kontrast_tablosu(rd)), ("cift-tablosu", lambda: cift_tablosu(rd)),
                   ("gaz-izgara", gaz_izgara), ("kk-kompakt", kk_kompakt), ("vurgu-seridi", vurgu_seridi), ("ifade-sozlugu", ifade_sozlugu)):
        u.yer_tutucu(ad, fn)
    TM.AKTIF = "van-golu"
    html = sablon_kur(u, os.path.join(os.path.dirname(__file__), "katalog_karma.html"))
    hedef = os.path.join(klasor, "karma-katalog.html")
    yaz(hedef, TM.tema_html(html, "van-golu", css, hedef, ortak))
    bas(hedef, "katalog")
    kl = os.path.join(klasor, "onizleme", "katalog")
    for kaynak, ad in (("s01.png", "paletler.png"), ("s02.png", "karsilastirma-sayfasi.png"), ("s03.png", "renk-denetimi.png"), ("s04.png", "karakterler.png")):
        if os.path.exists(os.path.join(kl, kaynak)):
            shutil.move(os.path.join(kl, kaynak), os.path.join(klasor, "onizleme", ad))
    shutil.rmtree(kl, ignore_errors=True)
    return rd
