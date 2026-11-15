"""Çerçeve sayfaları: her işlev (kitap, plan_ögesi) → <section class="sayfa"> HTML.

Sıra ve sayfa numaraları veri.sayfa_plani()'ndan gelir. Sayfa türleri: kapak · rehber · harita · bos (Notlar) ·
zaman · periyodik · sozluk · album · arka_kapak.
"""
import os
import sys

BURA = os.path.dirname(os.path.abspath(__file__))
if BURA not in sys.path:
    sys.path.insert(0, BURA)

import veri as V  # noqa: E402
import harita as HR  # noqa: E402
import cizimler as CZ  # noqa: E402
from cizim.temel import f  # noqa: E402
from cizim import sus as U  # noqa: E402

from yardim import yeni, e, zengin  # noqa: E402


def _yol_rozet(y, cls="yol-rozet"):
    return CZ.yol_rozeti(yeni("yr"), y["yol"], y["renk"], y["renk_k"], cls=cls)


# ------------------------------------------------------------------ HARİTA + İÇİNDEKİLER

ETIKET_VARSAYILAN = {"ust": (0, -12), "alt": (0, 12), "sol": (-15, 0), "sag": (15, 0)}


def _rota_parca(y):
    """'Maden Yolu I · Batı Anadolu' → ('Maden Yolu I', 'Batı Anadolu'); etiket ve kartlarda iki satıra bölmek için."""
    a, _, b = y["rota"].partition(" · ")
    return a, b


def harita(k, p):
    no = p["no"]
    HARITA_UST = 46.0           # mm
    kirp = (0, 10, HR.W, HR.H - 40)
    olcek = 210 / (kirp[2] - kirp[0])
    yuk = (kirp[3] - kirp[1]) * olcek
    # rota merkezleri (mm) → etiket çapaları (rotalar.json: etiket.dx/dy)
    capalar = {}
    for y in k.yollar:
        mx, my = HR.rota_merkez(y)
        cx, cy = (mx - kirp[0]) * olcek, (my - kirp[1]) * olcek
        et = y.get("etiket", {}) or {}
        dx, dy = ETIKET_VARSAYILAN.get(et.get("yon", "ust"))
        dx, dy = et.get("dx", dx), et.get("dy", dy)
        capalar[y["yol"]] = (cx + dx, cy + dy, et.get("yon", "ust"))
    svg, konum, _ = HR.bilgi_haritasi(yeni("hr"), k.yollar, k.baslangic, {n: (a, b) for n, (a, b, _) in capalar.items()}, kirp=kirp)
    etiketler = []
    for y in k.yollar:
        ax, ay, yon = capalar[y["yol"]]
        bas = k.baslar.get(y["yol"])
        ad, ek = _rota_parca(y)
        ust = f'Yol {y["yol"]}' + (f" · {ek}" if ek else "") + (f" · s.{bas}" if bas else "")
        stil = f'--r:{y["renk_k"]};'
        if yon == "sol":
            stil += f'right:{f(210 - ax - 4.3, 2)}mm;top:{f(ay - 4.2, 2)}mm;flex-direction:row-reverse;padding:.5mm .6mm .6mm 2mm;text-align:right'
        else:
            stil += f'left:{f(ax - 4.3, 2)}mm;top:{f(ay - 4.2, 2)}mm'
        etiketler.append(f'<div class="rota-et{" hazir" if y["hazir"] else ""}" style="{stil}">{_yol_rozet(y)}<div><i>{e(ust)}</i><b>{e(ad)}</b></div></div>')
    vx, vy = konum["van"]
    etiketler.append(f'<div class="basla-et" style="right:{f(210 - vx - 13, 2)}mm;top:{f(vy - 13.6, 2)}mm"><svg viewBox="0 0 40 40"><use href="#av-pamuk"/></svg>BAŞLANGIÇ · VAN</div>')
    hazir_n = sum(1 for y in k.yollar if y["hazir"])
    baslik = (f'<div class="cb" style="position:absolute;left:11mm;right:11mm;top:14.4mm;z-index:2">'
              f'<div><div class="cipler"><span class="cip koyu buyuk">{k.sinif}. sınıf · {e(k.alt_baslik)}</span>'
              f'<span class="cip buyuk">{len(k.yollar)} yol · {len(k.yollar)} kale</span></div>'
              f'<h1>Türkiye <em>Kimya Rotası</em></h1>'
              f'<p class="alt-yazi">Van’dan yola çık; her yol bir ünite, her kale bir <b>Büyük İmtihan</b>.</p></div>'
              f'<div class="pamuk-kose"><div class="balon-k"><span class="et keh">Pamuk</span><br>Haritadaki her yıldız bir yol. '
              f'Kale kapısını aç, <b>nişanını boya!</b></div><svg viewBox="0 0 140 160"><use href="#pamuk-selam"/></svg></div></div>')
    kutu = (f'<div class="harita-kutu" data-serbest style="top:{f(HARITA_UST, 2)}mm;height:{f(yuk, 2)}mm">{svg}'
            f'{"".join(etiketler)}</div>')
    # içindekiler
    genis = len(k.yollar) <= 6
    satir = []
    for y in k.yollar:
        bas = k.baslar.get(y["yol"])
        sag = f'<div class="no"><small>sayfa</small>{bas}</div>' if bas else '<div class="yolda">yakında</div>'
        dur = ""
        if genis:
            dur = '<div class="durak-dizi">' + " · ".join(e(d["yer"]) for d in y["duraklar"]) + f' <span>→ {e(y["kale"]["ad"])}</span></div>'
        satir.append(f'<div class="ic-yol" style="--r:{y["renk"]};--r-k:{y["renk_k"]}">{_yol_rozet(y)}'
                     f'<div><div class="ust">Yol {y["yol"]} · {e(y["tema"])}</div><b>{e(y["rota"])}</b>'
                     f'<div class="unite">{e(y["unite"])}'
                     f'{"" if genis else " <small>· " + str(len(y["duraklar"])) + " durak · " + e(y["kale"]["ad"]) + "</small>"}</div>{dur}</div>{sag}</div>')
    ekler = [("medeniyet", "Medeniyetimizden", "zaman şeridi", k.no("zaman", parca=1)),
             ("kitap", "Periyodik tablo", "118 element", k.no("periyodik")),
             ("kissa", "Kavram sözlüğü", f"{k.kavram_sayisi} kavram", k.no("sozluk", parca=1)),
             ("akce", "Nişan albümü", "boya, say, unvan al", k.no("album", parca=1))]
    ek = "".join(f'<div><svg viewBox="0 0 24 24"><use href="#i-{ik}"/></svg><b>{ad}<small>{alt}</small></b><span>{n}</span></div>'
                 for ik, ad, alt, n in ekler)
    lejant = ('<span class="lejant"><i class="l-durak"></i>durak <i class="l-kale"></i>kale <i class="l-yolculuk"></i>yolculuğun sırası</span>')
    ic = (f'<main class="ic" style="top:{f(HARITA_UST + yuk + 4, 2)}mm">'
          f'<div class="ara-bas">İçindekiler <small>{len(k.yollar)} yol · bu baskıda {hazir_n} ünite</small>{lejant}</div>'
          f'<div class="icindekiler{" genis" if genis else ""}">{"".join(satir)}</div>'
          f'<div class="ara-bas" style="font-size:12pt;margin-top:.6mm">Kitabın sonunda <small>sayfa numaraları kitap boyunca süreklidir</small></div>'
          f'<div class="ic-ek" style="--n:{len(ekler)}">{ek}</div></main>')
    return k.sayfa("harita-sayfa", "harita", no, baslik + kutu + ic, hud=("Türkiye Kimya Rotası", "Harita ve içindekiler"),
                   konu="Harita ve içindekiler")


# ------------------------------------------------------------------ geçici iskeletler (sırayla doldurulur)

def _gecici(k, p, ad, baslik):
    ic = f'<main class="ic"><div class="ara-bas">{baslik}</div></main>'
    return k.sayfa(f"{ad}-sayfa", ad, p["no"], ic, hud=("Kitap", baslik), konu=baslik)


def _kapak_tema(k):
    return "aksam" if k.sinif == 10 else "safak"


def _kapak_harita(k, en_mm=196.0):
    """Kapaktaki gökyüzü haritası: SVG + rozetler (rotaların üstünde, iğne gibi)."""
    tema = _kapak_tema(k)
    s, konum, v = HR.kapak_haritasi(yeni("kh"), k.yollar, k.baslangic, tema="aksam" if tema == "aksam" else "safak")
    for y in k.yollar:
        mx, my = konum[y["yol"]]
        s += (f'<path d="M{f(mx)} {f(my)} L{f(mx)} {f(my - 40)}" stroke="#1B1D26" stroke-width="4"/>'
              f'<circle cx="{f(mx)}" cy="{f(my)}" r="6" fill="#1B1D26"/>')
        s += HR.rozet(mx, my - 68, 35, y["yol"], y["renk"], y["renk_k"], yazi_boy=34 if y["yol"] < 10 else 28)
    return s.cikti(f"0 0 {f(HR.W)} {f(HR.H)}", cls="kapak-harita")


def kapak(k, p):
    tema = _kapak_tema(k)
    sahne, ufuk = CZ.kapak_sahnesi(yeni("ks"), tema)
    on = CZ.kapak_on_plan(yeni("ko"), tema)
    karakter = ('<use href="#elif-aha" x="70" y="2108" width="560" height="588"/>'
                '<use href="#yusuf-anlatan" x="560" y="2150" width="540" height="567"/>')
    pamuk = '<use href="#pamuk-selam" x="980" y="2440" width="330" height="377"/>'
    katman = (f'<svg class="kapak-katman" viewBox="0 0 2100 2970" preserveAspectRatio="xMidYMid slice">{sahne.govde()}'
              f'{karakter}{on.govde()}{pamuk}</svg>')
    rozet = CZ.sinif_rozeti(yeni("sr"), k.sinif, tema)
    yol_n = len(k.yollar)
    ust = (f'<div class="kapak-ust"><div class="kapak-cipler"><span>Lise kimya</span><span>{k.sinif}. sınıf</span></div>'
           f'<h1 class="kapak-baslik"><span class="g" aria-hidden="true">Kimya<br>Rotası</span><span class="o">Kimya<br><em>Rotası</em></span></h1>'
           f'<p class="kapak-slogan">{e(k.alt_baslik)}</p>'
           f'<p class="kapak-alt-slogan">{yol_n} yol · {yol_n} kale · bir büyük yolculuk</p></div>')
    alt = (f'<div class="kapak-balon"><b>Miyav!</b> Elif, Yusuf ve ben Türkiye’yi yol yol dolaşıyoruz. '
           f'Kimyayı yerinde öğrenmeye <b>var mısın?</b></div>'
           f'<div class="kapak-yazar">Yazar: …</div>')
    ic = (katman + _kapak_harita(k) + ust + f'<div class="kapak-sinif">{rozet}</div>' + alt)
    return k.sayfa(f"kapak-sayfa kapak-{tema}", "kapak", p["no"], ic, cerceve=False)


def _rozet(metin, renk="gol", ust="-"):
    from cizim.renkler import GOL, GOL_K, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ERGUVAN, LAJVER, ZUMRUT, ALTIN, ALTIN_K, OBS
    r = {"gol": (GOL, GOL_K), "keh": (KEH, KEH_K), "mer": (MER, MER_K), "kob": (KOB, KOB_K), "erg": (ERGUVAN, "#4E2760"),
         "laj": (LAJVER, "#13285E"), "zum": (ZUMRUT, "#145C3C"), "alt": (ALTIN, ALTIN_K)}[renk]
    if ust == "-":
        ic = f'<text x="50" y="64" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="40" fill="{OBS}">{metin}</text>'
        return U.durak_rozeti(yeni("dr"), ic, "", r[0], r[1])
    return U.durak_rozeti(yeni("dr"), metin, ust, r[0], r[1])


def _ikon_rozet(ikon, renk):
    """Akış adımı rozeti: renkli Selçuklu yıldızı + beyaz göbekte ikon (sus.IKON sembolü)."""
    from cizim.renkler import OBS
    ic = (f'<g transform="translate(32 32) scale(1.5)" color="{OBS}"><use href="#i-{ikon}" width="24" height="24"/></g>')
    return _rozet_ic(ic, renk)


def _rozet_ic(ic, renk):
    from cizim.renkler import GOL, GOL_K, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ERGUVAN, LAJVER, ZUMRUT, ALTIN, ALTIN_K
    r = {"gol": (GOL, GOL_K), "keh": (KEH, KEH_K), "mer": (MER, MER_K), "kob": (KOB, KOB_K), "erg": (ERGUVAN, "#4E2760"),
         "laj": (LAJVER, "#13285E"), "zum": (ZUMRUT, "#145C3C"), "alt": (ALTIN, ALTIN_K)}[renk]
    return U.durak_rozeti(yeni("ar"), ic, "", r[0], r[1], cls="akis-rozet")


def rehber(k, p):
    return _rehber1(k, p) if p["parca"] == 1 else _rehber2(k, p)


def _rehber1(k, p):
    no = p["no"]
    album_no = k.no("album", parca=1)
    bant = (f'<div class="bant" data-serbest>{CZ.rehber_bandi(yeni("rb"))}'
            f'<div class="levha">{_rozet("?", "keh")}<div><div class="ust">Rehber · yola çıkmadan önce</div>'
            f'<h1 class="iki-satir">Bu kitabı nasıl<br><em>kullanırım?</em></h1>'
            f'<p class="alt-bas">Her ünite bir <b>yol</b>: durak durak ilerle, kaleyi aç, nişanını boya.</p></div></div></div>')
    adimlar = [("harita", "kob", "Yola çıkış", "Tur haritası, nişanlar, hedefler."),
               ("hedef", "gol", "Duraklar", "4–6 konu durağı: sohbet, kavram, görev."),
               ("hulasa", "erg", "Hülasa", "Altı kartta özet ve Muhasebe."),
               ("meclis", "keh", "Yan yollar", "Meclis, Kıssa ve Anahtar merdiveni."),
               ("kale", "mer", "Kale", "Büyük İmtihan: 12 meşveret sorusu."),
               ("ustad", "laj", "Üstad soruları", "6 zor soru; hepsi doğruysa Üstad Mührü."),
               ("anahtar", "zum", "Cevaplar", "Durak etiketli anahtar, tüm çözümler."),
               ("bayrak", "alt", "Final", "Akçe rayı, unvan, nişan sayımı.")]
    akis = []
    for ik, renk, ad, ac in adimlar:
        if ik == "ustad":
            rz = _rozet_ic(f'<g transform="translate(30 30) scale(.8333)" fill="none" stroke="#1B1D26" stroke-width="3" stroke-linecap="round" '
                           f'stroke-linejoin="round">{CZ.ustad_ikonu()}</g>', renk)
        else:
            rz = _ikon_rozet(ik, renk)
        akis.append(f'<div class="akis-adim">{rz}<b>{ad}</b><span>{ac}</span></div>')
    yol_svg = ('<svg class="akis-yol" viewBox="0 0 1000 40" preserveAspectRatio="none"><path d="M10 20 C200 4 300 36 500 20 S800 4 990 20" '
               'fill="none" stroke="#1B1D26" stroke-width="11" stroke-linecap="round" opacity=".85"/><path d="M10 20 C200 4 300 36 500 20 S800 4 990 20" '
               'fill="none" stroke="#F3E2C6" stroke-width="7" stroke-linecap="round"/><path d="M10 20 C200 4 300 36 500 20 S800 4 990 20" '
               'fill="none" stroke="#E08A1A" stroke-width="1.8" stroke-dasharray="7 6" stroke-linecap="round"/></svg>')
    noktalar = ('<i class="tam"></i><i class="tam"></i><i class="simdi"></i><i></i><i></i><i class="hul"></i><i class="yan"></i><i class="yan"></i><i class="yan"></i>'
                '<i class="kale"><svg viewBox="0 0 24 22"><path d="M2 21 V8 H6 V4 H9 V8 H11 V4 H13 V8 H15 V4 H18 V8 H22 V21 Z" fill="none" stroke="#8FA3AD" stroke-width="2.2" stroke-linejoin="round"/></svg></i>')
    hud = (f'<div class="hud-ornek"><header class="hud"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>Kimya Rotası {k.sinif}</span>'
           f'<span class="yer">… turu · 3. durak · <b>yer adı</b></span><span class="noktalar">{noktalar}</span>'
           f'<span class="akce"><svg viewBox="0 0 40 40"><use href="#akce"/></svg>Akçe <span class="yaz"></span> /1400</span></header>'
           f'<p><b>Üst şerit pusulandır.</b> ● durak · ■ Hülasa · ◆ yan yol · kale: Büyük İmtihan. Dolu nokta geçtiğin yeri, halkalı nokta '
           f'bulunduğun durağı gösterir. Sağdaki kutuya o ana kadar topladığın <b>akçeyi</b> yaz.</p></div>')
    akis_kart = (f'<div class="kart akis-kart"><span class="et">{_ik("harita")}Bir yol nasıl akar?</span>'
                 f'<div class="akis">{yol_svg}{"".join(akis)}</div>{hud}</div>')
    import infografik_kopru as IK
    unvan = "".join(f'<div class="ah-basamak b{i + 1}">{IK.unvan(yeni("ur"), i + 1, renk)}<b>{ad}</b><small>{esik}</small></div>'
                    for i, (ad, esik, renk) in enumerate((("Çırak", "0+", "#A3B3BE"), ("Kalfa", "400+", "#13A3A6"),
                                                          ("Usta", "800+", "#0E4C5A"), ("Üstad", "1150+", "#F0A21A"))))
    akce = (f'<div class="kart akce-kart"><span class="et keh">{_sikke()}Akçe ve Ahilik basamakları</span>'
            f'<p><b>Akçe</b>, Osmanlı’nın gümüş sikkesidir; bu kitapta puanın akçedir. Kavram, görev, hazine kartı, Tuzak! ve hızlı görevler '
            f'akçe kazandırır. İpucu için <b>anahtar</b> açmak <b>−10 akçe</b>. Her yolda en çok <b>1400 akçe</b> var.</p>'
            f'<div class="ah-merdiven">{unvan}</div>'
            f'<p class="ah-not"><b>Ahilik:</b> Anadolu’da zanaatkârın çıraklıktan ustalığa adım adım yetiştiği gelenek. Yolun sonunda '
            f'toplam akçen unvanını belirler.</p></div>')
    renkli = U.nisan(yeni("ns"), U.NISAN_IKON["deste"], "#13A3A6", "#0A6C74", kurdele="#E2533D")
    bos = CZ.nisan_boyama(yeni("nb"), U.NISAN_IKON["deste"])
    nisan = (f'<div class="kart nisan-kart"><span class="et mer">{_ik("bayrak")}Nişanlar ve nişan albümü</span>'
             f'<div class="nisan-ikili"><div>{bos}<small>önce</small></div><svg class="ok-svg" viewBox="0 0 40 20"><path d="M2 10 H32 M24 3 L33 10 L24 17" fill="none" '
             f'stroke="#1B1D26" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg><div>{renkli}<small>sonra</small></div></div>'
             f'<p>Her durağın bir <b>nişanı</b> var. Durağı bitirince nişanını <b>kendin boya</b>. Üstad sorularının hepsini çözersen '
             f'<b>Üstad Mührü</b> de senin.</p>'
             f'<p class="ah-not">Kitabın sonundaki <b>Nişan albümü</b>{f" (s.{album_no})" if album_no else ""} bütün yolların nişanlarını bir araya toplar.</p></div>')
    kisiler = [("elif-soru", "Elif", "Edremit’ten", "“Neden?” demeden geçmez; soruları o sorar. Yanılınca birlikte düzeltiriz.", "mer"),
               ("yusuf-anlatan", "Yusuf", "Erciş’ten · kimya kulübü", "Sakin; adım adım, yerel örneklerle anlatır.", "gol"),
               ("pamuk-akce", "Pamuk", "Van kedisi", "Bir gözü mavi, bir gözü kehribar. Kısa konuşur, hep sayıyla. Miyav!", "keh"),
               ("zeynep-kitap", "Zeynep Hoca", "kimya öğretmeni", "“Medeniyetimizden” köşelerinde bilim mirasımızı anlatır.", "kob")]
    kis = "".join(f'<div class="ark ark-{r}"><svg viewBox="{"0 0 140 160" if poz.startswith("pamuk") else "0 0 200 210"}"><use href="#{poz}"/></svg>'
                  f'<div><b>{ad}</b><small>{alt}</small><p>{ac}</p></div></div>' for poz, ad, alt, ac, r in kisiler)
    arkadas = f'<div class="kart arkadas-kart"><span class="et">{_ik("meclis")}Yol arkadaşların</span><div class="arkadaslar">{kis}</div></div>'
    isaret = [("hedef", "Görev", "Çözümü kapat, dene."), ("anahtar", "Anahtar", "Açarsan −10 akçe."), ("tuzak", "Tuzak!", "Yanlış bilinen."),
              ("makas", "Kes", "Deftere yapıştır."), ("hazine", "Hazine", "Formül kartı."), ("medeniyet", "Medeniyet", "Bilim mirasımız."),
              ("kale", "Kale", "Büyük İmtihan."), ("akce", "Akçe", "Puanın.")]
    isr = "".join(f'<div class="is">{_ik(ik)}<div><b>{ad}</b>{ac}</div></div>' for ik, ad, ac in isaret)
    isaretler = f'<div class="kart gol-z isaretler isaret-8"><span class="et">İşaretler</span>{isr}</div>'
    ic = (f'<main class="ic" style="top:62mm">{akis_kart}<div class="bento" style="grid-template-columns:1.12fr .88fr">{akce}{nisan}</div>'
          f'{arkadas}{isaretler}</main>')
    return k.sayfa("rehber-sayfa", "rehber-1", no, bant + ic, hud=("Rehber", "Bu kitabı nasıl kullanırım?"), konu="Rehber · yolculuğun kuralları")


def _ik(ad, cls=""):
    return f'<svg class="{cls}" viewBox="0 0 24 24"><use href="#i-{ad}"/></svg>'


def _sikke():
    return '<svg viewBox="0 0 40 40"><use href="#akce"/></svg>'


TURLER = [("acilis", "Yola çıkış", "Tur haritası, kazanılacak nişanlar, yol arkadaşları ve hedefler."),
          ("durak", "Durak sayfası", "Sahne ve levha, #kıyı-sohbeti, kavram, hazine kartı, görev, Tuzak!, hızlı görev."),
          ("hulasa", "Hülasa", "Ebru zeminde altı özet kart, hazine sandığı ve Muhasebe."),
          ("meclis", "Meclis", "Dört hatalı çözüm: kim haklı? Satırı bul, nedenini yaz."),
          ("kissa", "Kıssa", "Günlük hayattan bağlam soruları; sonunda kıssadan hisse."),
          ("merdiven", "Anahtar merdiveni", "Üç problem, üç basamak. Ne kadar az inersen o kadar akçe."),
          ("imtihan", "Büyük İmtihan", "Kalede 12 meşveret sorusu: önce tahmin et, sonra çöz."),
          ("ustad", "Üstad soruları", "YKS/AYT tarzı 6 zor soru; akçeye dahil değil. Hepsini çözen Üstad Mührü’nü boyar."),
          ("cevaplar", "Cevaplar", "Durak etiketli anahtar ve bütün çözümler; yanlışın hangi duraktan?"),
          ("final", "Final", "Akçe rayı, unvan kartı, akçe defteri ve nişan sayımı.")]

KUTULAR = [("kavram", "kitap", "Kavram", "Tanım kutusu. Önce bunu anla."),
           ("kiyidan", "dalga", "Kıyıdan", "Konunun günlük hayattaki karşılığı."),
           ("hazine", "hazine", "Hazine kartı", "Formül kartı: kes, defterine yapıştır."),
           ("gorev", "hedef", "Görev", "Çözümlü örnek: çözümü kapat, önce sen dene."),
           ("tuzak", "tuzak", "Tuzak!", "Yanlış bilinen, YANLIŞ mührüyle; altında doğrusu."),
           ("hizli", "anahtar", "Hızlı görev", "Kısa soru. Anahtar ipucu −10 akçe, cevap ters yazılı."),
           ("medeniyet", "medeniyet", "Medeniyetimizden", "Zeynep Hoca’dan bilim tarihimizden bir sayfa."),
           ("mesveret", "meclis", "Meşveret", "Sınıfça tahmin: şıklara %__ yaz, sonra çöz."),
           ("muhasebe", "cay", "Muhasebe", "Kendini muhasebe et: çay bardağını doldur.")]


def _rehber2(k, p):
    no = p["no"]
    bant = (f'<div class="bant b36" data-serbest>{CZ.cini_pano_bandi(yeni("cp"))}'
            f'<div class="levha kob">{_rozet("2", "kob")}<div><div class="ust">Rehber · sayfa türleri ve kutular</div>'
            f'<h1>Haritanın <em>dili</em></h1>'
            f'<p class="alt-bas">Her yolda aynı sayfalar, aynı sırayla karşına çıkar.</p></div></div></div>')
    hucre = "".join(f'<div class="sayfa-turu">{CZ.mini_sayfa(yeni("ms"), t)}<b>{ad}</b><span>{ac}</span></div>' for t, ad, ac in TURLER)
    kutular = "".join(f'<div class="kutu-orn ko-{c}"><div class="kb">{_ik(ik)}<b>{ad}</b></div><p>{ac}</p></div>' for c, ik, ad, ac in KUTULAR)
    oneri = ('<div class="kart oneri-kart"><div class="pamuk-not">{0}<p><b>Pamuk’un yol notu:</b> Görevlerde çözümü kapat, önce kendin dene. '
             'Hülasa’daki Muhasebe’de “Tekrar” dediğin konunun durağına dön. İmtihanı süre tutarak çöz; yanlışını cevap sayfasındaki '
             '<b>durak etiketinden</b> bul. Miyav!</p></div></div>').format('<svg viewBox="0 0 140 160"><use href="#pamuk-dusunen"/></svg>')
    ic = (f'<main class="ic" style="top:52mm"><div class="ara-bas">{_ik("kitap", "ikon")}Sayfa türleri <small>her sayfanın küçük resmi; '
          f'üst şeritteki noktalar hangisinde olduğunu söyler</small></div>'
          f'<div class="sayfa-turleri">{hucre}</div>'
          f'<div class="ara-bas">{_ik("hazine", "ikon")}Kutuyu rengiyle tanı</div><div class="kutu-izgara">{kutular}</div>{oneri}</main>')
    return k.sayfa("rehber-sayfa", "rehber-2", no, bant + ic, hud=("Rehber", "Sayfa türleri ve kutular"), konu="Rehber · sayfa türleri ve kutular")


def bos(k, p):
    return _gecici(k, p, "notlar", "Notlar")


def zaman(k, p):
    return _gecici(k, p, f"zaman-{p['parca']}", "Medeniyetimizden")


def periyodik(k, p):
    return _gecici(k, p, "periyodik", "Periyodik tablo")


def sozluk(k, p):
    return _gecici(k, p, f"sozluk-{p['parca']}", "Kavram sözlüğü")


def album(k, p):
    return _gecici(k, p, f"album-{p['parca']}", "Nişan albümü")


def arka_kapak(k, p):
    tema = _kapak_tema(k)
    sahne, ufuk = CZ.kapak_sahnesi(yeni("as"), tema)
    on = CZ.kapak_on_plan(yeni("ao"), tema)
    karakter = ('<use href="#yusuf-gulen" x="1130" y="2150" width="520" height="546"/>'
                '<use href="#elif-soru" x="1530" y="2120" width="540" height="567"/>')
    pamuk = '<use href="#pamuk-bayrak" x="760" y="2280" width="420" height="494"/>'
    katman = (f'<svg class="kapak-katman" viewBox="0 0 2100 2970" preserveAspectRatio="xMidYMid slice">{sahne.govde()}'
              f'{karakter}<g transform="translate(2100 0) scale(-1 1)">{on.govde()}</g>{pamuk}</svg>')
    satir = []
    for y in k.yollar:
        a, b = _rota_parca(y)
        satir.append(f'<div class="ak-yol" style="--r:{y["renk"]};--r-k:{y["renk_k"]}">{_yol_rozet(y)}<div><b>{e(y["rota"])}</b>'
                     f'<span>{e(y["unite"])}</span></div></div>')
    turler = [("hedef", "Duraklar"), ("hulasa", "Hülasa"), ("meclis", "Meclis"), ("kissa", "Kıssa"), ("anahtar", "Anahtar merdiveni"),
              ("kale", "Büyük İmtihan"), ("akce", "Üstad soruları"), ("medeniyet", "Medeniyetimizden")]
    tur = "".join(f'<span><svg viewBox="0 0 24 24"><use href="#i-{ik}"/></svg>{ad}</span>' for ik, ad in turler)
    kart = (f'<div class="arka-kart">{"".join(_kose4())}'
            f'<div class="ak-bas"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg><b>{k.ad}</b><span>{e(k.alt_baslik)}</span></div>'
            f'<p class="ak-giris">Van Gölü kıyısında başlayan bir yolculuk bu. <b>Elif</b>, <b>Yusuf</b> ve Van kedisi <b>Pamuk</b> her ünitede '
            f'Türkiye’nin başka bir köşesine gidiyor; kimyayı, gerçekten yaşandığı yerde öğreniyor.</p>'
            f'<p>Her yol durak durak ilerler: kıyı sohbetinde konuyu aç, hazine kartlarını defterine yapıştır, Tuzak!’ları yakala, '
            f'Meclis’te kimin haklı olduğuna karar ver, kalede <b>Büyük İmtihan</b>’ı geç. Topladığın <b>akçe</b> ile Ahilik basamaklarında '
            f'<b>Çırak</b>’tan <b>Üstad</b>’a yüksel; nişanlarını boya, albümünü doldur.</p>'
            f'<div class="ak-ara">Bu kitaptaki yollar</div><div class="ak-yollar{" cok" if len(k.yollar) > 6 else ""}">{"".join(satir)}</div>'
            f'<div class="ak-ara">Her yolda</div><div class="ak-turler">{tur}</div></div>')
    return k.sayfa(f"kapak-sayfa arka-kapak kapak-{tema}", "arka-kapak", p["no"], katman + kart, cerceve=False)


def _kose4():
    return [U.tezhip_kose(yeni("tk")).replace('class="tezhip-kose"', f'class="kose k{i}"') for i in range(1, 5)]
