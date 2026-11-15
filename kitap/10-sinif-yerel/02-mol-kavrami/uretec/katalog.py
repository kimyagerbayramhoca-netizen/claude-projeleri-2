#!/usr/bin/env python3
"""İllüstrasyon kütüphanesinin görsel kataloğu → kitap/10-sinif-yerel/katalog/*.png

Çalıştır:  python3 uretec/katalog.py
Üretilenler (TASARIM-SISTEMI-YEREL.md bu görsellere bağlanır):
  karakterler.png   Pamuk / Elif / Yusuf / Zeynep Hoca pozları ve avatarlar (sembol kimlikleriyle)
  molekuller.png    3B molekül ve kristal çizimleri (molekul.py)
  susler.png        çini şeritleri, zemin geçmesi, tezhip köşebendi, kilim, mühürler, rozetler, nişanlar, çay bardakları, ikonlar
  sahneler.png      bütün başlık bantları ve büyük sahneler (sahneler.py)
  infografikler.png bilgi grafikleri (infografik.py)
  ebru.png          ebru dokuları (ebru.py)
"""
import os
import subprocess
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
UNITE = os.path.dirname(BURA)
KATALOG = os.path.normpath(os.path.join(UNITE, "..", "katalog"))
sys.path.insert(0, BURA)

from cizim import sahneler as SH, karakter as K, sus as U, molekul as M, infografik as I  # noqa: E402
from cizim.renkler import GOL, GOL_K, KEH, MER, KOB, ERGUVAN  # noqa: E402

FONT = "../../fontlar"
CSS = f"""
@font-face{{font-family:"Baloo Bhaijaan 2";src:url("{FONT}/baloobhaijaan2/static/BalooBhaijaan2-400.ttf");font-weight:400}}@font-face{{font-family:"Baloo Bhaijaan 2";src:url("{FONT}/baloobhaijaan2/static/BalooBhaijaan2-500.ttf");font-weight:500}}@font-face{{font-family:"Baloo Bhaijaan 2";src:url("{FONT}/baloobhaijaan2/static/BalooBhaijaan2-600.ttf");font-weight:600}}@font-face{{font-family:"Baloo Bhaijaan 2";src:url("{FONT}/baloobhaijaan2/static/BalooBhaijaan2-700.ttf");font-weight:700}}@font-face{{font-family:"Baloo Bhaijaan 2";src:url("{FONT}/baloobhaijaan2/static/BalooBhaijaan2-800.ttf");font-weight:800}}
@font-face{{font-family:"Nunito";src:url("{FONT}/nunito/static/Nunito-400.ttf");font-weight:400}}@font-face{{font-family:"Nunito";src:url("{FONT}/nunito/static/Nunito-500.ttf");font-weight:500}}@font-face{{font-family:"Nunito";src:url("{FONT}/nunito/static/Nunito-600.ttf");font-weight:600}}@font-face{{font-family:"Nunito";src:url("{FONT}/nunito/static/Nunito-700.ttf");font-weight:700}}@font-face{{font-family:"Nunito";src:url("{FONT}/nunito/static/Nunito-800.ttf");font-weight:800}}@font-face{{font-family:"Nunito";src:url("{FONT}/nunito/static/Nunito-900.ttf");font-weight:900}}
@font-face{{font-family:"Amiri";src:url("{FONT}/amiri/Amiri-Regular.ttf")}}
@font-face{{font-family:"Reem Kufi";src:url("{FONT}/reemkufi/static/ReemKufi-400.ttf");font-weight:400}}@font-face{{font-family:"Reem Kufi";src:url("{FONT}/reemkufi/static/ReemKufi-500.ttf");font-weight:500}}@font-face{{font-family:"Reem Kufi";src:url("{FONT}/reemkufi/static/ReemKufi-600.ttf");font-weight:600}}@font-face{{font-family:"Reem Kufi";src:url("{FONT}/reemkufi/static/ReemKufi-700.ttf");font-weight:700}}
body{{margin:0;padding:18px 22px;background:#F4F7F8;font-family:Nunito,sans-serif;color:#1B1D26}}
h1{{font-family:"Baloo Bhaijaan 2";font-size:30px;margin:0 0 4px}} p.al{{margin:0 0 14px;color:#56636E;font-weight:700}}
.izgara{{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end}}
.oge{{background:#fff;border:2px solid #1B1D26;border-radius:12px;padding:10px;text-align:center;box-shadow:3px 4px 0 #0E4C5A}}
.oge code{{display:block;font-size:12px;font-weight:800;color:#0A6C74;margin-top:6px;white-space:nowrap}}
.oge small{{display:block;font-size:11px;color:#56636E}}
.genis{{width:100%}} .genis svg{{width:100%;height:auto;display:block}}
"""


def sayfa(ad, baslik, aciklama, govde, defs=False, genislik=1400):
    d = f'<svg width="0" height="0" style="position:absolute"><defs>{K.semboller()}{U.ikon_sembolleri()}</defs></svg>' if defs else ""
    html = (f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{d}'
            f'<h1>{baslik}</h1><p class="al">{aciklama}</p>{govde}</body></html>')
    yol = os.path.join(KATALOG, f"{ad}.html")
    open(yol, "w", encoding="utf-8").write(html)
    subprocess.run(["node", os.path.join(BURA, "fotograf.js"), yol, os.path.join(KATALOG, f"{ad}.png"), str(genislik), "1"], check=True)
    os.remove(yol)
    print("yazıldı:", os.path.relpath(os.path.join(KATALOG, f"{ad}.png"), UNITE))


def oge(svg, kod, not_=""):
    return f'<div class="oge">{svg}<code>{kod}</code>' + (f"<small>{not_}</small>" if not_ else "") + "</div>"


def karakterler():
    g = []
    for poz, n in (("selam", "karşılama · s.1"), ("dusunen", "düşünen · s.8, s.4"), ("sasiran", "şaşıran · s.10"), ("akce", "akçe tutan · s.6, s.12"),
                   ("kitap", "tezhipli kitap okuyan · s.7"), ("otur", "sade oturuş")):
        g.append(oge(f'<svg viewBox="0 0 140 160" width="150" height="171"><use href="#pamuk-{poz}"/></svg>', f"#pamuk-{poz}", n))
    g.append(oge('<svg viewBox="0 -40 170 200" width="150" height="176"><use href="#pamuk-bayrak"/></svg>', "#pamuk-bayrak", "kale burcunda bayrakla · s.14"))
    g.append(oge('<svg viewBox="0 0 120 80" width="150" height="100"><use href="#pamuk-yuzer"/></svg>', "#pamuk-yuzer", "gölde yüzen · s.1 harita"))
    for kim, pozlar in (("elif", ("soru", "dusunen", "aha", "sasiran")), ("yusuf", ("anlatan", "defter", "gulen")), ("zeynep", ("anlatan", "kitap"))):
        for poz in pozlar:
            g.append(oge(f'<svg viewBox="0 0 200 210" width="140" height="147"><use href="#{kim}-{poz}"/></svg>', f"#{kim}-{poz}", "yarım boy"))
    av = "".join(f'<svg viewBox="{"0 0 40 40" if k == "pamuk" else "0 0 200 210"}" width="54" height="54" style="margin:0 4px"><use href="#av-{k}"/></svg>' for k in ("elif", "yusuf", "pamuk", "zeynep"))
    g.append(oge(av, "#av-elif · #av-yusuf · #av-pamuk · #av-zeynep", "sohbet avatarları"))
    g.append(oge('<svg viewBox="0 0 40 40" width="60" height="60"><use href="#akce"/></svg>', "#akce", "akçe sikkesi (yazısız)"))
    sayfa("karakterler", "Karakter sayfası", "Bütün pozlar aynı baş/gövde parçalarından kurulur (karakter.py) → yüz, renk ve kıyafet her pozda aynı kalır.",
          f'<div class="izgara">{"".join(g)}</div>', defs=True)


def molekuller():
    liste = [("H2O", (0, 0, 0)), ("CO2", (15, 30, 0)), ("NH3", (25, 0, 0)), ("CH4", (10, 20, 5)), ("C6H12O6", (-60, 20, 0)),
             ("SO2", (0, 20, 0)), ("SO3", (-20, 10, 0)), ("O2", (10, 25, 0)), ("N2", (0, 25, 0)), ("CO", (0, 25, 0)),
             ("C2H4", (10, 25, 0)), ("C2H6", (10, 25, 0)), ("C3H8", (10, 25, 0)), ("CaCO3", (0, 0, 0)), ("NaCl", (0, 0, 0)), ("He", (0, 0, 0))]
    g = []
    for i, (ad, d) in enumerate(liste):
        svg = M.molekul_svg(f"k{i}", ad, d, etiket=True).replace("<svg ", '<svg style="width:150px" ', 1)
        g.append(oge(svg, f'{{{{mol|{ad}|{",".join(str(v) for v in d)}|en|e}}}}', "molekul_svg"))
    g.append(oge(M.molekul_svg("kna", "Na2CO3", (0, 0, 0), etiket=True, iyon_etiket=True).replace("<svg ", '<svg style="width:220px" ', 1), "{{mol|Na2CO3|0,0,0|36mm|e|ion}}", "formül birimi + iyon yükleri"))
    g.append(oge(M.kristal_nacl("kkr").replace("<svg ", '<svg style="width:170px" ', 1), "{{kristal|15mm}}", "NaCl kristali"))
    g.append(oge(I.cekirdekler("kck").replace("<svg ", '<svg style="width:300px" ', 1), "{{info|cekirdekler}}", "izotop çekirdekleri"))
    sayfa("molekuller", "3B molekül kütüphanesi", "Radyal gradyanlı küreler + parlama + yer gölgesi + yarı renkli silindir bağlar. Geometri Å cinsinden; donus=(x°, y°, z°).",
          f'<div class="izgara">{"".join(g)}</div>')


def susler():
    g = []
    from kur import cini_serit
    serit = cini_serit().replace('class="cini-serit"', 'style="display:block;width:100%;height:26px"')
    g.append(f'<div class="oge" style="width:100%">{serit}<code>sus.cini_serit_ince() → kur.cini_serit() · {{{{cini}}}} (HUD altı, 30 karo tek SVG)</code></div>')
    g.append(oge(f'<div style="width:420px;height:140px">{U.cini_serit_genis().replace("<svg ", "<svg width=\"420\" height=\"140\" ", 1)}</div>', "sus.cini_serit_genis()", "geniş çini bordürü"))
    g.append(oge(f'<div style="width:240px;height:240px;background:#FBFDFD">{U.zemin_gecme("#9FD0D0").replace("<svg ", "<svg width=\"240\" height=\"240\" ", 1)}</div>', "sus.zemin_gecme() · {{zemin}}", "sayfa zemini (çok açık basılır)"))
    g.append(oge(U.tezhip_kose("tk").replace("<svg ", '<svg width="140" ', 1), "sus.tezhip_kose() · {{kose}}", "Medeniyetimizden köşebendi"))
    g.append(f'<div class="oge genis">{U.kilim_serit("kl", 1880, 60)}<code>sus.kilim_serit() — basamaklı göz + elibelinde</code></div>')
    g.append(oge(U.muhur("m1", "yanlis", boy=150), "{{muhur|yanlis}}", "Tuzak · YANLIŞ"))
    g.append(oge(U.muhur("m2", "dogru", boy=150), "{{muhur|dogru}}", "DOĞRU mührü"))
    g.append(oge(U.durak_rozeti("r1", "3").replace("<svg ", '<svg width="120" ', 1), "{{rozet|3}}", "durak rozeti"))
    harf = '<text x="50" y="64" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="40" fill="#1B1D26">K</text>'
    g.append(oge(U.durak_rozeti("r2", harf, "", MER, "#A12817").replace("<svg ", '<svg width="120" ', 1), "{{rozet|K|-|mer}}", "harf rozeti (yan yol, kale)"))
    for i, (k, r) in enumerate((("deste", (GOL, GOL_K)), ("izotop", (KOB, "#1B3584")), ("kefal", (GOL, GOL_K)), ("mizan", (MER, "#A12817")), ("karisim", (ERGUVAN, "#4E2760")), ("kale", (KEH, "#8C5500")))):
        g.append(oge(U.nisan(f"n{i}", U.NISAN_IKON[k], r[0], r[1], kurdele="#E2533D").replace("<svg ", '<svg width="100" ', 1), f"{{{{nisan|{k}}}}}", "boyanacak nişan"))
    g.append(oge("".join(U.cay_bardagi(f"c{i}", v, b, boy=60) for i, (v, b) in enumerate(((1, False), (.5, False), (0, False), (0, True)))), "{{cay|1}} {{cay|.5}} {{cay|0}} {{cay|0|b}}", "Muhasebe: Tamam / Yarım / Tekrar / boyanacak"))
    ik = "".join(f'<span style="display:inline-block;text-align:center;margin:4px 6px;color:#0A6C74"><svg width="34" height="34"><use href="#i-{k}"/></svg><br><small>{k}</small></span>' for k in U.IKON)
    g.append(f'<div class="oge genis">{ik}<code>{{{{ikon|ad}}}} — 24×24 çizgi ikonlar, currentColor</code></div>')
    sayfa("susler", "Süsleme ve işaret kütüphanesi", "Çini, tezhip, kilim, mühür, rozet, nişan, çay bardağı ve ikonlar (sus.py).",
          f'<div class="izgara">{"".join(g)}</div>', defs=True)


def sahneler():
    g = []
    for ad, n in (("edremit", "1. durak · sabah"), ("gevas", "2. durak · kümbet"), ("tatvan", "3. durak · Nemrut, feribot"), ("ahlat", "4. durak · mezar taşları"),
                  ("adilcevaz", "5. durak · Süphan, kale"), ("suphan", "Hülasa · yayla"), ("ercis", "Meclis · köy odası"), ("muradiye", "Kıssa · şelale"),
                  ("iskele", "Anahtar · iskele"), ("kale_buyuk", "İmtihan 1 · Van Kalesi"), ("kale_kapi", "İmtihan 2 · kale kapısı"), ("gece", "Cevaplar · gece")):
        svg = getattr(SH, ad)().replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1)
        g.append(f'<div class="oge" style="width:660px">{svg}<code>sahneler.{ad}() · {{{{sahne|{ad}}}}}</code><small>{n}</small></div>')
    pan, _ = SH.panorama()
    g.append(f'<div class="oge genis">{pan.replace("<svg ", "<svg style=\"width:100%;height:auto\" ", 1)}<code>sahneler.panorama() · {{{{sahne|panorama}}}} + {{{{panorama-etiket}}}}</code><small>açılış · tur rotası (perspektif harita)</small></div>')
    g.append(f'<div class="oge genis">{SH.final().replace("<svg ", "<svg style=\"width:100%;height:auto\" ", 1)}<code>sahneler.final(nisanlar) · {{{{final}}}}</code><small>final · kale burcu</small></div>')
    sayfa("sahneler", "Sahne kütüphanesi", "Başlık bantları 2100×460 birim (210×46 mm); sol üst %55 gökyüzü levhaya ayrılır. Hepsi sahne.py + yapilar.py parçalarından kurulur.",
          f'<div class="izgara">{"".join(g)}</div>', defs=True)


def infografikler():
    g = []
    for ad, gen, n in (("avogadro_merdiveni", 640, "log ölçek · s.2"), ("bor_madalyon", 420, "bolluk madalyonları · s.3, s.7"), ("mol_haritasi", 420, "göl üstünde köprüler · s.4/5"),
                       ("karisim_kaplari", 420, "karışım kapları · s.6"), ("esit_kutle_terazi", 360, "eşit kütle · s.6, s.7"), ("hazini_kart", 300, "el-Hâzinî terazisi · s.5"),
                       ("imbik", 250, "Câbir · imbik · s.6"), ("razi_araclari", 280, "Râzî · araçlar · s.8"), ("halka_aleti", 180, "Takiyüddin · s.13"),
                       ("ozgul_agirlik", 280, "özgül ağırlık (yedek)"), ("soda_resmi", 220, "Kıssa 1"), ("bor_resmi", 210, "Kıssa 2"), ("grafik_xy", 260, "Kıssa 3"),
                       ("raf_kaplari", 330, "Kıssa 4"), ("merdiven_akce", 420, "s.10"), ("elmas", 120, "İmtihan 6"), ("balon", 80, "İmtihan 2"), ("akce_rayi", 640, "Final")):
        svg = getattr(I, ad)(f"k-{ad[:5]}").replace("<svg ", f'<svg style="width:{gen}px;height:auto" ', 1)
        g.append(oge(svg, f"{{{{info|{ad}}}}}", n))
    ur = "".join(I.unvan_rozeti(f"u{k}", k, c).replace("<svg ", '<svg width="70" ', 1) for k, c in ((1, "#A3B3BE"), (2, "#13A3A6"), (3, "#0E4C5A"), (4, "#F0A21A")))
    g.append(oge(ur, "{{info|unvan_rozeti|kat|renk}}", "Çırak · Kalfa · Usta · Mol Üstadı"))
    sayfa("infografikler", "Bilgi grafikleri", "Sayısal içerikli çizimler; değerler dogrula.py ile denetlenir (infografik.py).",
          f'<div class="izgara">{"".join(g)}</div>')


def ebru_sayfasi():
    gov = ('<div class="izgara"><div class="oge" style="width:640px"><img src="../02-mol-kavrami/gorsel/ebru-gol.jpg" style="width:100%"><code>ebru.ebru_gol() · gorsel/ebru-gol.jpg</code><small>battal + gelgit + dalga · altbilgi şeridi, Medeniyetimizden üst şeridi</small></div>'
           '<div class="oge" style="width:420px"><img src="../02-mol-kavrami/gorsel/ebru-gun.jpg" style="width:100%"><code>ebru.ebru_gun() · gorsel/ebru-gun.jpg</code><small>gün batımı paleti · Hülasa kart zemini</small></div></div>')
    sayfa("ebru", "Ebru dokuları", "Matematiksel marmorlama (damla + biz/tarak dönüşümleri) → JPEG; PDF'e bir kez gömülür.", gov)


if __name__ == "__main__":
    os.makedirs(KATALOG, exist_ok=True)
    karakterler()
    molekuller()
    susler()
    sahneler()
    infografikler()
    ebru_sayfasi()
