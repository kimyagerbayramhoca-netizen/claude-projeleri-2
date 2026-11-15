#!/usr/bin/env python3
"""Kimya Rotası · yerel tasarım ORTAK KURUCUSU.

Her ünite üç dosyayla tanımlanır (hepsi ünitenin `uretec/` klasöründe):
  sablon.html   sayfaların içeriği; çizimler {{yer-tutucu|arg…}} ile çağrılır
  meta.json     ünitenin künyesi ve TEK DOĞRULUK KAYNAĞI (duraklar, nişanlar, hazine kartları, medeniyet, kavramlar)
  kur.py        İNCE kurucu: sayfa künyesi (HUD yeri, altbilgi, akçe çubuğu), ilerleme noktası, üniteye özel yer tutucular

Ünitenin kur.py'si:

    import kur_ortak as KO
    SAYFA = {1: ("Yola çıkış", "Van Gölü turu · yola çıkış", 0), 2: ("1. durak · <b>Edremit</b>", "1. durak · Neden mol?", 0), …}
    SIMDI = {1: -1, 2: 0, …}            # HUD'da "şimdi" olan nokta (−1: yok; durak sayısı + 5: hepsi tamam)
    u = KO.Unite(__file__, SAYFA, SIMDI)
    u.yer_tutucu("panorama-etiket", fonksiyon)   # üniteye özel yer tutucu: fonksiyon(*arg) → HTML
    u.calistir()

Komut satırı (ünite klasöründen ya da herhangi bir yerden):
    python3 uretec/kur.py              unite.html
    python3 uretec/kur.py --fotokopi   unite-fotokopi.html (siyah-beyaz, az mürekkep; render.js --fotokopi kullanır)
    python3 uretec/kur.py --hazine     hazine-kartlari.html (meta.json'daki H kartlarının kesme yaprağı)
    python3 uretec/kur.py --hepsi      üçü birden
    python3 uretec/kur.py --ebru       ebru dokularını (yerel-ortak/gorsel/ebru-*.jpg) yeniden üretir

Ortam değişkenleri (kitap birleştirme betiği için):
    YEREL_SAYFA_BASLANGIC=37   ünitenin 1. sayfası kitapta 37. sayfa olur: altbilgi numarası ve {{sayfa|n}} göndermeleri kayar
    YEREL_CIKTI=/yol/x.html    unite.html yerine buraya yazılır; stil.css bağlantısı yeni yere göre düzeltilir
                              (fotokopi çıktısı aynı klasörde x-fotokopi.html olur)

Yer tutucuların tam listesi: yerel-ortak/TASARIM-SISTEMI.md §8. Kısaca:
    çerçeve   {{defs}} {{zemin}} {{cini}} {{hud|n}} {{alt|n}}
    çizim     {{sahne|ad|arg…}} {{info|ad|arg…}} {{mol|AD|rx,ry,rz|en|e|ion}} {{kristal|en}} {{final}}
    süs       {{rozet|metin|ust|renk}} {{hno|H4|renk}} {{sno|7|renk}} {{muhur|yanlis}} {{nisan|ikon|kurdele}} {{cay|seviye|b}}
              {{kose}} {{kilim}} {{av|kim}} {{poz|sembol|sınıf}} {{ikon|ad|sınıf}} {{sikke|sınıf}}
    meta      {{hazine|H1}} {{sandik}} {{nisan-izgara}} {{nisan-sayim}} {{meta|alan}}
              {{rota-haritasi}} {{rota-etiket}} (meta.json duraklarından genel rota haritası)
    sayfa     {{sayfa|13}} → 13 (+ kayma) · {{sayfa|13|de}} → 13’te · {{ek|13|de}} → te
"""
import html as _html
import json
import math
import os
import re
import sys

ORTAK = os.path.dirname(os.path.abspath(__file__))
if ORTAK not in sys.path:
    sys.path.insert(0, ORTAK)

from cizim.temel import Svg, f, cizgi_d, selcuklu_yildizi, karis  # noqa: E402
from cizim import sahneler as SH, karakter as K, sus as U, molekul as M, infografik as I, ebru as E  # noqa: E402
from cizim.renkler import (GOL, GOL_K, KEH, KEH_K, MER, MER_K, KOB, KOB_K, ALTIN, ALTIN_K, OBS, ERGUVAN,  # noqa: E402
                           LAJVER, ZUMRUT, GUM, GUM_K)

# ------------------------------------------------------------------ renk adları (yer tutucularda kısa ad)
RENK = {
    "gol": (GOL, GOL_K), "keh": (KEH, KEH_K), "mer": (MER, MER_K), "kob": (KOB, KOB_K), "erg": (ERGUVAN, "#4E2760"),
    "laj": (LAJVER, "#13285E"), "alt": (ALTIN, ALTIN_K), "zum": (ZUMRUT, "#145C3C"), "gum": (GUM, GUM_K),
}
# nişan ikonlarının varsayılan renkleri (meta.json'da "renk" verilmezse)
NISAN_RENK = {"deste": "gol", "izotop": "kob", "kefal": "gol", "mizan": "mer", "karisim": "erg", "kale": "keh", "ustad": "laj"}
AKCE_TOPLAM = 1400


# ------------------------------------------------------------------ meta.json metinleri: kısa yazım → HTML

_UST = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ", "0123456789+−=()n")
_ALT = str.maketrans("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎", "0123456789+−=()")


def zengin(metin):
    """meta.json metinlerini HTML'e çevirir. HTML olduğu gibi geçer; etiket DIŞINDAKİ metinde şu kısa yazımlar çalışır:
         {H2O} {Mg(OH)2}   kimyasal formül (rakamlar alt simge)        → H<sub>2</sub>O
         N_A  n_{atom}     alt simge (tek karakter ya da {…})          → N<sub>A</sub>
         10^23  10^-23     üst simge (sayı ya da {…}; - → −)           → 10<sup>23</sup>
         10²³  CO₂         Unicode üst/alt simge karakterleri           → 10<sup>23</sup>, CO<sub>2</sub>
    """
    if metin is None:
        return ""
    metin = str(metin)
    out = []
    for p in re.split(r"(<[^>]+>)", metin):
        if p.startswith("<"):
            out.append(p)
            continue
        p = re.sub(r"\{([A-Z][A-Za-z0-9()]*)\}", lambda m: re.sub(r"(\d+)", r"<sub>\1</sub>", m.group(1)), p)
        p = re.sub(r"(?<=[A-Za-z0-9)\]])_(?:\{([^}]*)\}|(.))", lambda m: f"<sub>{m.group(1) if m.group(1) is not None else m.group(2)}</sub>", p)
        p = re.sub(r"\^(?:\{([^}]*)\}|([-−+]?\d+(?:[.,]\d+)?))",
                   lambda m: f"<sup>{(m.group(1) if m.group(1) is not None else m.group(2)).replace('-', '−')}</sup>", p)
        p = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ]+", lambda m: f"<sup>{m.group().translate(_UST)}</sup>", p)
        p = re.sub(r"[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎]+", lambda m: f"<sub>{m.group().translate(_ALT)}</sub>", p)
        out.append(p)
    return "".join(out)


def duz_metin(metin):
    """HTML/kısa yazımlı metni düz metne çevirir (içindekiler, dizin gibi araçlar için)."""
    s = re.sub(r"<[^>]+>", "", zengin(metin))
    return re.sub(r"\s+", " ", _html.unescape(s)).strip()


# ------------------------------------------------------------------ Türkçe sayı ekleri (sayfa göndermeleri)

_BIR = {0: "sıfır", 1: "bir", 2: "iki", 3: "üç", 4: "dört", 5: "beş", 6: "altı", 7: "yedi", 8: "sekiz", 9: "dokuz"}
_ON = {1: "on", 2: "yirmi", 3: "otuz", 4: "kırk", 5: "elli", 6: "altmış", 7: "yetmiş", 8: "seksen", 9: "doksan"}


def _son_kelime(n):
    n = abs(int(n))
    if n % 10 or n == 0:
        return _BIR[n % 10]
    if n % 100:
        return _ON[(n // 10) % 10]
    if n % 1000:
        return "yüz"
    return "bin"


def sayi_eki(n, ek="de"):
    """Sayıdan sonra gelen hâl eki: ek ∈ de (bulunma) · den (ayrılma) · e (yönelme) · i (belirtme).
    sayi_eki(13) → 'te' · sayi_eki(6) → 'da' · sayi_eki(6, 'e') → 'ya' · sayi_eki(3, 'i') → 'ü'."""
    k = _son_kelime(n)
    unlu = [c for c in k if c in "aeıioöuü"][-1]
    ince = unlu in "eiöü"
    sert = k[-1] in "fstkçşhp"
    unlu_son = k[-1] in "aeıioöuü"
    if ek in ("de", "da", "te", "ta"):
        return ("t" if sert else "d") + ("e" if ince else "a")
    if ek in ("den", "dan", "ten", "tan"):
        return ("t" if sert else "d") + ("en" if ince else "an")
    if ek in ("e", "a", "ye", "ya"):
        return ("y" if unlu_son else "") + ("e" if ince else "a")
    if ek in ("i", "ı", "u", "ü", "yi", "yı", "yu", "yü"):
        dar = {"a": "ı", "ı": "ı", "o": "u", "u": "u", "e": "i", "i": "i", "ö": "ü", "ü": "ü"}[unlu]
        return ("y" if unlu_son else "") + dar
    raise ValueError(f"bilinmeyen ek: {ek}")


def tr_kucuk(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


# ------------------------------------------------------------------ meta.json

META_ZORUNLU = ("sinif", "yol", "rota", "unite", "klasor", "duraklar", "hazine", "nisanlar")


def meta_oku(yol):
    if not os.path.exists(yol):
        raise FileNotFoundError(f"meta.json yok: {yol}")
    with open(yol, encoding="utf-8") as fp:
        meta = json.load(fp)
    eksik = [k for k in META_ZORUNLU if k not in meta]
    if eksik:
        raise ValueError(f"meta.json eksik alan: {eksik} ({yol})")
    kodlar = [h["kod"] for h in meta["hazine"]]
    if len(set(kodlar)) != len(kodlar):
        raise ValueError(f"meta.json: tekrarlanan hazine kodu {kodlar}")
    return meta


# ------------------------------------------------------------------ sayfa çerçevesinin vektör dokuları

def cini_serit(sol_ek=0):
    """HUD altı İznik şeridi: 30 karo, tek SVG (desen değil; PDF'te vektör kalır). sol_ek: sola eklenecek karo (taşma payı)."""
    karo = U.cini_serit_ince().split(">", 1)[1].rsplit("</svg>", 1)[0]
    parca = "".join(f'<g transform="translate({k * 24} 0)">{karo}</g>' for k in range(-sol_ek, 30))
    return f'<svg class="cini-serit" viewBox="0 0 700 8" preserveAspectRatio="none">{parca}</svg>'


def zemin():
    """Sayfa zemini: çok açık Selçuklu yıldız geçmesi, tek path (210×297 mm; kenarlardan 7,5 mm taşar → baskı payını da doldurur)."""
    d = []
    adim = 15
    for i in range(-1, 16):
        for j in range(-1, 21):
            cx, cy = 7.5 + i * adim, 7.5 + j * adim
            d.append(cizgi_d(selcuklu_yildizi(cx, cy, 3.6), True, 2))
            d.append(f"M{f(cx + 5.3)} {f(cy + 5.3)} l4.4 4.4")
    return (f'<svg class="zemin" viewBox="0 0 210 297" preserveAspectRatio="none"><path d="{" ".join(d)}" fill="none" '
            f'stroke="#DDEEEE" stroke-width=".22" stroke-linejoin="round"/></svg>')


def ortak_defs(ek=""):
    """Paylaşılan semboller (her sayfada <use> ile): logo yıldızı, sayfa no yıldızı, karakterler, ikonlar (+ ünitenin ekleri)."""
    s = Svg("ortak")
    ga = s.lin([(0, "#FFE7A8"), (1, KEH)], 0, 0, 1, 1, ad="lg")
    gn = s.rad([(0, "#5FD3D0"), (.7, GOL), (1, GOL_K)], .4, .35, .75, ad="ng")
    sy = [f'<symbol id="logo-yildiz" viewBox="0 0 24 24"><path d="{cizgi_d(selcuklu_yildizi(12, 12, 11.4), True, 2)}" fill="{ga}" stroke="#FFF" stroke-width=".8"/>'
          f'<circle cx="12" cy="12" r="3.6" fill="{OBS}"/></symbol>',
          f'<symbol id="no-yildiz" viewBox="0 0 100 100"><path d="{cizgi_d(selcuklu_yildizi(50, 50, 48), True)}" fill="{ALTIN}" stroke="{OBS}" stroke-width="3"/>'
          f'<path d="{cizgi_d(selcuklu_yildizi(50, 50, 40), True)}" fill="{gn}" stroke="{OBS}" stroke-width="2"/></symbol>']
    return (f'<svg class="gizli-defs" aria-hidden="true"><defs>{s.govde()}{"".join(sy)}{K.semboller()}{U.ikon_sembolleri()}{ek}</defs></svg>')


def ebru_hazirla(zorla=False):
    gorsel = os.path.join(ORTAK, "gorsel")
    os.makedirs(gorsel, exist_ok=True)
    if zorla or not os.path.exists(os.path.join(gorsel, "ebru-gol.jpg")) or not os.path.exists(os.path.join(gorsel, "ebru-gun.jpg")):
        print("ebru dokuları üretiliyor…")
        E.ebru_gol(os.path.join(gorsel, "ebru-gol.jpg"))
        E.ebru_gun(os.path.join(gorsel, "ebru-gun.jpg"))


# ------------------------------------------------------------------ ÜNİTE

class Unite:
    """Bir ünitenin kurulumu. kur_dosyasi: ünitenin uretec/kur.py yolu (__file__)."""

    def __init__(self, kur_dosyasi, sayfa, simdi=None, hud_noktalar=None):
        self.uretec = os.path.dirname(os.path.abspath(kur_dosyasi))
        self.klasor = os.path.dirname(self.uretec)
        if self.uretec not in sys.path:
            sys.path.insert(0, self.uretec)
        self.meta = meta_oku(os.path.join(self.uretec, "meta.json"))
        self.sayfa_kunye = sayfa
        self.simdi = simdi or {}
        nd = len(self.meta["duraklar"])
        # ilerleme noktaları: duraklar ● + Hülasa ■ + 3 yan yol ◆ + kale
        self.hud_noktalar = hud_noktalar or (["d"] * nd + ["hul"] + ["yan"] * 3 + ["kale"])
        try:
            self.baslangic = int(os.environ.get("YEREL_SAYFA_BASLANGIC", "") or 1)
        except ValueError:
            raise ValueError("YEREL_SAYFA_BASLANGIC bir tam sayı olmalı")
        self.akce_toplam = int(self.meta.get("akce_toplam", AKCE_TOPLAM))
        self.sayac = 0
        self.ek_defs = ""
        self.yt = {}
        self.moduller = []          # sahne/info aramasında önce bakılan ünite modülleri
        for ad in ("sahneler_unite", "infografik_unite"):
            if os.path.exists(os.path.join(self.uretec, ad + ".py")):
                self.moduller.append(__import__(ad))
        self._genel_yer_tutucular()

    # ------------------------------------------------------------------ yardımcılar
    def yeni(self, onek):
        """Her SVG için benzersiz kimlik öneki (çakışırsa Chrome ilk tanımı kullanır ve renkler bozulur)."""
        self.sayac += 1
        return f"{onek}{self.sayac}"

    def yer_tutucu(self, ad, fn):
        """Üniteye özel yer tutucu ekler (ya da ortak olanı geçersiz kılar). fn(*arg) → HTML."""
        self.yt[ad] = fn

    def modul(self, mod):
        """{{sahne|…}} ve {{info|…}} aramasına modül ekler (ortak kütüphaneden önce bakılır)."""
        self.moduller.insert(0, mod)

    def sayfa_no(self, n):
        """Ünitenin n. sayfasının kitaptaki numarası (YEREL_SAYFA_BASLANGIC kayması)."""
        return int(n) + self.baslangic - 1

    def hazine_karti(self, kod):
        for h in self.meta["hazine"]:
            if h["kod"] == kod:
                return h
        raise KeyError(f"meta.json'da hazine kartı yok: {kod} (var olanlar: {[h['kod'] for h in self.meta['hazine']]})")

    def _bul(self, ad):
        for mod in self.moduller:
            if hasattr(mod, ad):
                return getattr(mod, ad)
        return None

    @property
    def sinif_adi(self):
        return f"Kimya Rotası {self.meta['sinif']}"

    @property
    def hud_rota(self):
        """HUD başlığı: meta.hud ya da rota adının son kelimesi küçük harfle ("Van Gölü Turu" → "Van Gölü turu")."""
        if self.meta.get("hud"):
            return self.meta["hud"]
        k = self.meta["rota"].split(" ")
        return " ".join(k[:-1] + [tr_kucuk(k[-1])]) if len(k) > 1 else self.meta["rota"]

    # ------------------------------------------------------------------ çerçeve
    def hud(self, no):
        no = int(no)
        yer, _, bar = self.sayfa_kunye[no]
        s = self.simdi.get(no, -1)
        noktalar = []
        for i, t in enumerate(self.hud_noktalar):
            durum = "tam" if i < s else ("simdi" if i == s else "")
            if t == "kale":
                renk = "#E2533D" if durum else "#8FA3AD"
                noktalar.append(f'<i class="kale {durum}"><svg viewBox="0 0 24 22"><path d="M2 21 V8 H6 V4 H9 V8 H11 V4 H13 V8 H15 V4 H18 V8 H22 V21 Z" fill="{renk if durum == "tam" else "none"}" stroke="{renk}" stroke-width="2.2" stroke-linejoin="round"/></svg></i>')
            else:
                cls = {"d": "", "hul": "hul", "yan": "yan"}[t]
                noktalar.append(f'<i class="{cls} {durum}"></i>')
        return (f'<header class="hud"><span class="logo"><svg viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>{self.sinif_adi}</span>'
                f'<span class="yer">{self.hud_rota} · {yer}</span><span class="noktalar">{"".join(noktalar)}</span>'
                f'<span class="akce"><svg viewBox="0 0 40 40"><use href="#akce"/></svg>Akçe <span class="yaz"></span> /{self.akce_toplam} '
                f'<span class="bar"><i style="width:{bar}%"></i></span></span></header>')

    def alt(self, no):
        no = int(no)
        _, konu, _ = self.sayfa_kunye[no]
        return (f'<footer class="alt"><span>{self.sinif_adi} · {self.meta["unite"]}</span><span>{konu}</span>'
                f'<span class="no"><svg viewBox="0 0 100 100"><use href="#no-yildiz"/></svg><b>{self.sayfa_no(no)}</b></span></footer><div class="ebru-alt"></div>')

    # ------------------------------------------------------------------ genel yer tutucular
    def _genel_yer_tutucular(self):
        u = self

        def sahne(ad, *arg):
            fn = u._bul(ad) or getattr(SH, ad, None)
            if fn is None:
                raise KeyError(f"sahne yok: {ad} (uretec/sahneler_unite.py ya da cizim/sahneler.py)")
            sonuc = fn(*arg)
            return sonuc[0] if isinstance(sonuc, tuple) else sonuc

        def mol(ad, donus="0,0,0", en="", etiket="", ion=""):
            rx, ry, rz = (float(v) for v in donus.split(","))
            svg = M.molekul_svg(u.yeni("mol"), ad, (rx, ry, rz), etiket=bool(etiket), iyon_etiket=bool(ion))
            return svg.replace("<svg ", f'<svg style="width:{en}" ', 1) if en else svg

        def kristal(en=""):
            svg = M.kristal_nacl(u.yeni("kr"))
            return svg.replace("<svg ", f'<svg style="width:{en}" ', 1) if en else svg

        def muhur(tur, boy=""):
            return U.muhur(u.yeni("mh"), tur)

        def rozet(metin, ust="DURAK", renk="gol"):
            r = RENK[renk]
            if ust == "-":
                harf = f'<text x="50" y="64" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="40" fill="{OBS}">{metin}</text>'
                return U.durak_rozeti(u.yeni("dr"), harf, "", r[0], r[1])
            return U.durak_rozeti(u.yeni("dr"), metin, ust, r[0], r[1])

        def hno(metin, renk="keh"):
            r = RENK[renk]
            return U.durak_rozeti(u.yeni("hn"), f'<text x="50" y="60" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="30" fill="{OBS}">{metin}</text>', "", r[0], r[1], cls="hno")

        def sno(metin, renk="mer"):
            r = RENK[renk]
            return U.durak_rozeti(u.yeni("sn"), f'<text x="50" y="62" text-anchor="middle" font-family="Baloo Bhaijaan 2" font-weight="800" font-size="36" fill="{OBS}">{metin}</text>', "", r[0], r[1], cls="sno")

        def nisan(ad, kurdele="#E2533D", renk=""):
            r = RENK[renk or u._nisan_renk(ad)]
            return U.nisan(u.yeni("ns"), u._nisan_ikon(ad), r[0], r[1], kurdele=kurdele if kurdele != "-" else None)

        def cay(seviye, bos=""):
            return U.cay_bardagi(u.yeni("cy"), float(seviye), bool(bos))

        def kose():
            return "".join(U.tezhip_kose(u.yeni("tk")).replace('class="tezhip-kose"', f'class="kose k{k}"') for k in range(1, 5))

        def kilim():
            return U.kilim_serit(u.yeni("kl"), 1880, 60)

        def av(kim):
            vb = "0 0 40 40" if kim == "pamuk" else "0 0 200 210"
            return f'<svg class="av" viewBox="{vb}"><use href="#av-{kim}"/></svg>'

        def poz(ad, cls=""):
            vb = "0 -40 170 200" if ad == "pamuk-bayrak" else ("0 0 140 160" if ad.startswith("pamuk") else "0 0 200 210")
            return f'<svg class="{cls}" viewBox="{vb}"><use href="#{ad}"/></svg>'

        def ikon(ad, cls="ikon"):
            return f'<svg class="{cls}" viewBox="0 0 24 24"><use href="#i-{ad}"/></svg>'

        def sikke(cls="sikke"):
            return f'<svg class="{cls}" viewBox="0 0 40 40"><use href="#akce"/></svg>'

        def info(ad, *arg):
            fn = u._bul(ad) or getattr(I, ad, None)
            if fn is None:
                raise KeyError(f"infografik yok: {ad}")
            if ad == "mol_haritasi":
                return fn(u.yeni("mh"), kutle_acik=(bool(arg) and arg[0] == "acik"))
            if ad == "unvan_rozeti":
                return fn(u.yeni("ur"), int(arg[0]), arg[1])
            return fn(u.yeni(ad[:4]), *[_sayi_mi(a) for a in arg])

        def final():
            ns = [U.nisan(u.yeni("nf"), u._nisan_ikon(n["ikon"]), *RENK[n.get("renk") or u._nisan_renk(n["ikon"])], kurdele="#E2533D")
                  .replace("<svg ", '<svg width="124" height="148" ', 1) for n in u.meta["nisanlar"]]
            return SH.final(nisanlar=ns)

        def meta(alan):
            return u._meta_alan(alan)

        self.yt.update({
            "hud": self.hud, "alt": self.alt, "cini": cini_serit, "zemin": zemin, "defs": lambda: ortak_defs(self.ek_defs),
            "sahne": sahne, "sno": sno, "mol": mol, "kristal": kristal, "muhur": muhur, "rozet": rozet, "hno": hno,
            "nisan": nisan, "cay": cay, "kose": kose, "kilim": kilim, "av": av, "poz": poz, "ikon": ikon,
            "sikke": sikke, "info": info, "final": final, "meta": meta,
            "hazine": self.yt_hazine, "sandik": self.yt_sandik, "nisan-izgara": self.yt_nisan_izgara, "nisan-sayim": self.yt_nisan_sayim,
            "sayfa": self.yt_sayfa, "ek": self.yt_ek, "rota-haritasi": self.yt_rota_haritasi, "rota-etiket": self.yt_rota_etiket,
        })

    # ------------------------------------------------------------------ nişanlar
    def _nisan_ikon(self, ad):
        ek = self._bul("NISAN_IKON")
        if ek and ad in ek:
            return ek[ad]
        if ad in U.NISAN_IKON:
            return U.NISAN_IKON[ad]
        raise KeyError(f"nişan ikonu yok: {ad} (cizim/sus.py NISAN_IKON ya da uretec/sahneler_unite.py NISAN_IKON)")

    def _nisan_renk(self, ikon):
        for n in self.meta["nisanlar"]:
            if n["ikon"] == ikon and n.get("renk"):
                return n["renk"]
        return NISAN_RENK.get(ikon, "gol")

    def yt_nisan_izgara(self):
        """Açılış sayfasındaki nişan ızgarası (meta.nisanlar). 6 nişan varsayılan ızgaradır; başka sayıda sütun ayarlanır."""
        n = len(self.meta["nisanlar"])
        stil = "" if n == 6 else f' style="grid-template-columns:repeat({n},1fr)"'
        ic = "".join(f'<div>{self.yt["nisan"](x["ikon"])}<b>{zengin(x["ad"])}</b><span>{zengin(x.get("aciklama", ""))}</span></div>'
                     for x in self.meta["nisanlar"])
        return f'<div class="nisanlar"{stil}>{ic}</div>'

    def yt_nisan_sayim(self):
        """Final sayfasındaki nişan sayımı (meta.nisanlar; öğrenci boyadıklarını işaretler)."""
        n = len(self.meta["nisanlar"])
        stil = "" if n == 6 else f' style="grid-template-columns:repeat({n},minmax(0,1fr))"'
        ic = "".join(f'<div>{self.yt["nisan"](x["ikon"])}<b>{zengin(x["ad"])}</b><small><span class="kutucuk"></span></small></div>'
                     for x in self.meta["nisanlar"])
        return f'<div class="nisan-say{" cok" if n > 6 else ""}"{stil}>{ic}</div>'

    # ------------------------------------------------------------------ hazine kartları (meta.json → sayfa, sandık, kesme yaprağı)
    def yt_hazine(self, kod, *_):
        h = self.hazine_karti(kod)
        cls = "hazine" + (f' {h["sinif"]}' if h.get("sinif") else "")
        govde = f'<div class="had">{zengin(h["baslik"])}</div>'
        if h.get("adimlar"):
            govde += '<ol class="adimlar">' + "".join(f"<li>{zengin(a)}</li>" for a in h["adimlar"]) + "</ol>"
        else:
            govde += f'<div class="hf">{zengin(h["formul"])}</div>'
        if h.get("not"):
            govde += f'<div class="hac">{zengin(h["not"])}</div>'
        hn = self.yt["hno"](h["kod"], h["renk"]) if h.get("renk") else self.yt["hno"](h["kod"])
        return f'<div class="{cls}">{hn}<div>{govde}</div>{self.yt["sikke"]("sikke")}</div>'

    def yt_sandik(self):
        """Hülasa'daki hazine sandığı ızgarasının hücreleri (kısa biçim: 'kisa' alanı, yoksa formül)."""
        return "".join(f'<div><b>{h["kod"]}</b>{zengin(h.get("kisa") or h.get("formul") or h["baslik"])}</div>' for h in self.meta["hazine"])

    # ------------------------------------------------------------------ sayfa göndermeleri
    def yt_sayfa(self, n, ek=""):
        no = self.sayfa_no(n)
        return f"{no}’{sayi_eki(no, ek)}" if ek else str(no)

    def yt_ek(self, n, ek="de"):
        return sayi_eki(self.sayfa_no(n), ek)

    # ------------------------------------------------------------------ meta alanları
    def _meta_alan(self, alan):
        hesap = {"hazine_sayisi": len(self.meta["hazine"]), "durak_sayisi": len(self.meta["duraklar"]),
                 "nisan_sayisi": len(self.meta["nisanlar"]), "akce_toplam": self.akce_toplam, "sinif_adi": self.sinif_adi}
        if alan in hesap:
            return str(hesap[alan])
        d = self.meta
        for k in alan.split("."):
            d = d[int(k)] if isinstance(d, list) else d[k]
        return zengin(d)

    # ------------------------------------------------------------------ genel rota haritası (meta.duraklar → panorama)
    def _rota(self):
        if not hasattr(self, "_rota_onbellek"):
            self._rota_onbellek = SH.rota_haritasi(self.meta["duraklar"], kale=self.meta.get("kale_konum"),
                                                   tohum=int(self.meta.get("yol", 1)) * 101 + int(self.meta.get("sinif", 9)))
        return self._rota_onbellek

    def yt_rota_haritasi(self, *_):
        return self._rota()[0]

    def yt_rota_etiket(self, *_):
        """Rota haritasındaki durak etiketleri (HTML, .durak-et). Her etiket için 8 aday yer denenir; harita dışına,
        başlığın ya da pusulanın üstüne, başka bir etikete ya da rozete binmeyen ilk yer seçilir (açgözlü yerleşim)."""
        _, konum = self._rota()
        ogeler = []
        for i, d in enumerate(self.meta["duraklar"]):
            sayfa = f' · s.{self.sayfa_no(d["sayfa"])}' if d.get("sayfa") else ""
            akce = f'{d["akce"]} akçe' if d.get("akce") else ""
            ogeler.append((str(i + 1), "", f'{i + 1}. DURAK · {tr_buyuk(d["yer"])}{sayfa}', zengin(d["baslik"]), akce))
        if "K" in konum and self.meta.get("kale"):
            ogeler.append(("K", "kale", "KALE · BÜYÜK İMTİHAN", zengin(self.meta["kale"]), ""))
        rozet = {k: (x / 10, y / 10) for k, (x, y) in konum.items()}
        yasak = [(0, 0, 82, 17), (182, 82, 210, 110)]          # "Tur haritası" başlığı, pusula
        yerlesik = []

        def carpisir(a, b):
            return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

        out = []
        for k, cls, ust, ad, akce in ogeler:
            x, y = rozet[k]
            w = max(len(duz_metin(ust)) * 1.53, len(duz_metin(ad)) * 1.62 + len(akce) * 1.4 + 1) + 4.2
            h = 8.4
            adaylar = [(x + 4.6, y - h / 2), (x - 4.6 - w, y - h / 2), (x - w / 2, y - 4.6 - h), (x - w / 2, y + 4.6),
                       (x + 3, y - 3.4 - h), (x + 3, y + 3.4), (x - w - 3, y - 3.4 - h), (x - w - 3, y + 3.4)]
            secim = adaylar[0]
            for lx, ly in adaylar:
                kutu = (lx, ly, lx + w, ly + h)
                if kutu[0] < 2 or kutu[1] < 2 or kutu[2] > 208 or kutu[3] > 108:
                    continue
                if any(carpisir(kutu, y_) for y_ in yasak + yerlesik):
                    continue
                if any(kk != k and kutu[0] - 4 < rx < kutu[2] + 4 and kutu[1] - 4 < ry < kutu[3] + 4 for kk, (rx, ry) in rozet.items()):
                    continue
                secim = (lx, ly)
                break
            yerlesik.append((secim[0], secim[1], secim[0] + w, secim[1] + h))
            kucuk = f"<small>{akce}</small>" if akce else ""
            out.append(f'<div class="durak-et {cls}" style="left:{f(secim[0], 2)}mm;top:{f(secim[1], 2)}mm"><i>{ust}</i><b>{ad}{kucuk}</b></div>'
                       .replace('class="durak-et "', 'class="durak-et"'))
        return "".join(out)

    # ------------------------------------------------------------------ kurulum
    def _cozumle(self, metin):
        def degistir(m):
            parca = m.group(1).split("|")
            ad, arg = parca[0].strip(), [a.strip() for a in parca[1:]]
            if ad not in self.yt:
                raise KeyError(f"bilinmeyen yer tutucu: {{{{{ad}}}}} · bilinenler: {', '.join(sorted(self.yt))}")
            try:
                return self.yt[ad](*arg)
            except Exception as e:
                raise RuntimeError(f"yer tutucu çözülemedi: {{{{{m.group(1)}}}}} → {type(e).__name__}: {e}") from e
        # HTML yorumları olduğu gibi kalır (iskeletteki örnek bileşenler yorum içinde durur)
        parca = re.split(r"(<!--.*?-->)", metin, flags=re.S)
        return "".join(p if p.startswith("<!--") else re.sub(r"\{\{([^{}]+)\}\}", degistir, p) for p in parca)

    def _stil_baglantisi(self, html, hedef):
        """stil.css bağlantısını çıktının yerine göre düzelt (YEREL_CIKTI başka klasöre yazınca)."""
        if os.path.dirname(os.path.abspath(hedef)) == self.klasor:
            return html
        yeni = os.path.relpath(os.path.join(ORTAK, "stil.css"), os.path.dirname(os.path.abspath(hedef))).replace(os.sep, "/")
        return re.sub(r'href="[^"]*yerel-ortak/stil\.css"', f'href="{yeni}"', html)

    def html_kur(self):
        """sablon.html → tam HTML metni (yazmadan)."""
        self.sayac = 0
        if hasattr(self, "_rota_onbellek"):
            del self._rota_onbellek
        with open(os.path.join(self.uretec, "sablon.html"), encoding="utf-8") as fp:
            sablon = fp.read()
        return self._cozumle(sablon)

    def cikti_yolu(self):
        return os.environ.get("YEREL_CIKTI") or os.path.join(self.klasor, "unite.html")

    def kur(self, varyant=None):
        """unite.html'i (ya da varyantı) yazar ve yolunu döndürür. varyant: None | 'fotokopi'."""
        ebru_hazirla("--ebru" in sys.argv)
        html = self.html_kur()
        hedef = self.cikti_yolu()
        if varyant == "fotokopi":
            from fotokopi import fotokopi_html
            html = fotokopi_html(html)
            hedef = os.path.splitext(hedef)[0] + "-fotokopi.html"
        html = self._stil_baglantisi(html, hedef)
        os.makedirs(os.path.dirname(os.path.abspath(hedef)), exist_ok=True)
        with open(hedef, "w", encoding="utf-8") as fp:
            fp.write(html)
        print(f"{os.path.relpath(hedef)} yazıldı ({len(html) / 1024:.0f} KB)")
        return hedef

    def hazine_yapragi(self):
        """meta.json'daki hazine kartlarından tek A4 kesme yaprağı: hazine-kartlari.html."""
        from hazine_yapragi import yaprak_html
        hedef = os.path.join(self.klasor, "hazine-kartlari.html")
        html = self._stil_baglantisi(yaprak_html(self), hedef)
        with open(hedef, "w", encoding="utf-8") as fp:
            fp.write(html)
        print(f"{os.path.relpath(hedef)} yazıldı ({len(html) / 1024:.0f} KB)")
        return hedef

    def calistir(self, argv=None):
        argv = sys.argv[1:] if argv is None else argv
        hepsi = "--hepsi" in argv
        yalniz = [a for a in argv if a in ("--fotokopi", "--hazine")]
        if hepsi or not yalniz:
            self.kur()
        if hepsi or "--fotokopi" in argv:
            self.kur("fotokopi")
        if hepsi or "--hazine" in argv:
            self.hazine_yapragi()


def _sayi_mi(a):
    try:
        return int(a)
    except ValueError:
        try:
            return float(a)
        except ValueError:
            return a


def tr_buyuk(s):
    return s.replace("i", "İ").replace("ı", "I").upper()
