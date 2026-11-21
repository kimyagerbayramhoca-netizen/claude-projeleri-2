"""Ünite doğrulama yardımcıları — ünitenin uretec/dogrula.py dosyası bunu içe aktarır.

    from dogrula_ortak import *          # D (denetçi), kontrol, tek_sik, yargi, mk, yakin, NA, M …
    kontrol("CaCO3 = 100", mk("CaCO3") == 100)
    T[1] = tek_sik("İmtihan 1", dict(A=.3, B=1.1, C=2.4, D=3.3, E=3.6), lambda v: yakin(v, .3 * 11), "D")
    …
    html = sayfa_oku(__file__)                      # unite.html (yoksa None)
    sayfa_isaretleri_ayni(html, {"I1": "D", …})   # data-soru/data-dogru işaretleri hesapla aynı mı?
    D.sonuc()                                      # "SONUÇ: hepsi doğru" ya da hata listesi (çıkış kodu 1)

Sayfadan okuma kuralları (TASARIM-SISTEMI.md §9 · cevap işaretleme):
  • soru kartı  data-soru="KOD"  (K1, I7, U3 … ünite içinde benzersiz)
  • doğru şık   <div class="sik" data-dogru><b>C</b>…   ya da meşverette  <div data-dogru><b>C</b>…
    (data-dogru her zaman açılış etiketinin SON niteliği, hemen ardından <b>HARF</b>)
  • meclis      <div class="yorum" data-dogru> … <b>Ad:</b>   ve   <span class="kutucuk" data-dogru></span>2
"""
import os
import re
import sys
from fractions import Fraction as F  # noqa: F401  (ünite dogrula.py'leri kesir için kullanır)

NA = 6.02e23
# YAZIM-REHBERI.md'deki mol kütleleri (+ sık kullanılan yuvarlak değerler; soruda kullanılan değeri belirt)
M = dict(H=1, He=4, Li=7, Be=9, B=10.8, C=12, N=14, O=16, F=19, Ne=20, Na=23, Mg=24, Al=27, Si=28, P=31, S=32, Cl=35.5,
         Ar=40, K=39, Ca=40, Cr=52, Mn=55, Fe=56, Ni=59, Co=59, Cu=64, Zn=65, Br=80, Ag=108, Sn=119, I=127, Ba=137, Pb=207)


# ------------------------------------------------------------------ denetçi

class Denetci:
    def __init__(self):
        self.hata = []
        self.sayi = 0

    def kontrol(self, ad, kosul):
        self.sayi += 1
        print(("OK  " if kosul else "HATA") + "  " + ad)
        if not kosul:
            self.hata.append(ad)
        return bool(kosul)

    def sonuc(self, cik=True):
        print(f"\n{self.sayi} denetim.")
        print("SONUÇ:", "hepsi doğru" if not self.hata else f"{len(self.hata)} hata: {self.hata}")
        if cik and self.hata:
            sys.exit(1)


D = Denetci()


def kontrol(ad, kosul):
    return D.kontrol(ad, kosul)


def yakin(a, b, t=1e-9):
    return abs(a - b) <= t * max(1, abs(a), abs(b))


def tek_sik(ad, siklar, dogru_mu, beklenen):
    """siklar: {"A": değer, …}. dogru_mu(değer) → bool. TAM OLARAK bir şık doğru olmalı ve beklenen harf olmalı."""
    d = [k for k, v in siklar.items() if dogru_mu(v)]
    kontrol(f"{ad}: tek doğru şık {d} == ['{beklenen}']", d == [beklenen])
    return d[0] if len(d) == 1 else None


def yargi(sozluk):
    """{"I": True, "II": False, "III": True} → {"I", "III"} (doğru yargılar kümesi)."""
    return {k for k, ok in sozluk.items() if ok}


YARGI_5 = {"A": {"I"}, "B": {"II"}, "C": {"I", "II"}, "D": {"II", "III"}, "E": {"I", "II", "III"}}   # sık kullanılan şık seti


def dagilim(cevaplar, harfler="ABCDE"):
    """Cevap harflerinin sayımı; her harf en az bir kez mi?"""
    say = {k: list(cevaplar).count(k) for k in harfler}
    kontrol(f"şık dağılımı her harf en az bir kez {say}", all(v >= 1 for v in say.values()))
    return say


# ------------------------------------------------------------------ kimya

_EL = re.compile(r"([A-Z][a-z]?)(\d*)|(\()|(\))(\d*)")


def formul(s):
    """'Mg(OH)2' → {'Mg': 1, 'O': 2, 'H': 2}. Parantez iç içe olabilir; yük ve hidrat (·) desteklenmez."""
    yigin = [{}]
    for m in _EL.finditer(s):
        el, n, ac, kapa, kn = m.groups()
        if el:
            yigin[-1][el] = yigin[-1].get(el, 0) + int(n or 1)
        elif ac:
            yigin.append({})
        elif kapa:
            ic = yigin.pop()
            for k, v in ic.items():
                yigin[-1][k] = yigin[-1].get(k, 0) + v * int(kn or 1)
    if len(yigin) != 1:
        raise ValueError(f"parantez hatası: {s}")
    return yigin[0]


def mk(f_, kutle=None):
    """Mol kütlesi: mk('C6H12O6') → 180 · mk({'C': 1, 'O': 2}) → 44."""
    kutle = kutle or M
    d = formul(f_) if isinstance(f_, str) else f_
    return sum(kutle[k] * v for k, v in d.items())


def atom_sayisi(f_):
    """Bir formüldeki toplam atom sayısı: atom_sayisi('C3H8') → 11."""
    return sum((formul(f_) if isinstance(f_, str) else f_).values())


# ------------------------------------------------------------------ sayfadan okuma (unite.html)

def sayfa_oku(dogrula_dosyasi, ad="unite.html"):
    """Ünitenin unite.html metni (dogrula.py'nin __file__'ından bulunur). Yoksa uyarı verir ve None döndürür."""
    yol = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(dogrula_dosyasi))), ad)
    if not os.path.exists(yol):
        print(f"UYARI: {ad} yok; önce python3 uretec/kur.py çalıştır.")
        return None
    with open(yol, encoding="utf-8") as fp:
        return fp.read()


def _bloklar(html):
    """data-soru="KOD" kartlarını sırayla (kod, blok metni) olarak verir (blok: bir sonraki data-soru'ya kadar)."""
    yerler = [(m.start(), m.group(1)) for m in re.finditer(r'data-soru="([^"]+)"', html)]
    for i, (bas, kod) in enumerate(yerler):
        son = yerler[i + 1][0] if i + 1 < len(yerler) else len(html)
        sayfa_sonu = html.find("</section>", bas)
        if sayfa_sonu != -1:
            son = min(son, sayfa_sonu)
        yield kod, html[bas:son]


def isaretli_dogrular(html):
    """{kod: ['C']} — her data-soru kartındaki data-dogru işaretli şık harfleri (tek olmalı)."""
    out = {}
    for kod, blok in _bloklar(html):
        out[kod] = re.findall(r'data-dogru(?:="[^"]*")?>\s*<b>([A-E])</b>', blok)
    return out


def sik_harfleri(html):
    """{kod: ['A', 'B', …]} — her soru kartındaki şık harfleri (.sik ya da .oy > div)."""
    out = {}
    for kod, blok in _bloklar(html):
        out[kod] = re.findall(r'<div(?: class="sik")?(?: data-dogru)?><b>([A-E])</b>', blok)
    return out


def sayfa_isaretleri_ayni(html, beklenen, bes_sik=True):
    """Sayfadaki data-dogru işaretleri hesaplanan anahtarla aynı mı? (her kartta tek işaret, A–E beş şık)."""
    isaret = isaretli_dogrular(html)
    harf = sik_harfleri(html)
    for kod, h in beklenen.items():
        kontrol(f"sayfada {kod}: data-dogru işareti {isaret.get(kod)} == ['{h}']", isaret.get(kod) == [h])
        if bes_sik:
            kontrol(f"sayfada {kod}: A–E beş şık {harf.get(kod)}", sorted(harf.get(kod) or []) == list("ABCDE"))
    return isaret


def meclis_hukumleri(html):
    """{kod: (haklı kişi, satır no)} — meclis kartlarındaki data-dogru yorum ve kutucuk."""
    out = {}
    for kod, blok in _bloklar(html):
        kisi = re.search(r'<div class="yorum" data-dogru>.*?<b>([^<:]+):</b>', blok, re.S)
        satir = re.search(r'<span class="kutucuk" data-dogru></span>\s*(\d)', blok)
        if kisi or satir:
            out[kod] = (kisi.group(1) if kisi else None, int(satir.group(1)) if satir else None)
    return out


def ogretmen_metinleri(html):
    """Sayfadaki bütün .ogr (öğretmen) metinleri, etiketsiz: ['2 mol H', …]."""
    return [re.sub(r"<[^>]+>", "", m) for m in re.findall(r'<span class="ogr">(.*?)</span>', html, re.S)]


def anahtar_izgarasi(html):
    """Cevaplar sayfasındaki anahtar ızgarası: {1: 'D', 2: 'C', …} (<i>n</i><b>H</b> hücreleri)."""
    izgara = re.search(r'<div class="anahtar-izgara">(.*?)</div>\s*</div>', html, re.S)
    return dict((int(n), h) for n, h in re.findall(r"<i>(\d+)</i><b>([A-E])</b>", izgara.group(1))) if izgara else {}


# ------------------------------------------------------------------ yeni bileşenler (TASARIM-SISTEMI.md §16): sayfadan okuma
# Kendini dene, Şifreli Kapı, Çeldirici Röntgeni, Robot yanıldı mı?, kat sayfası cevapları, 3B resimleri.
# Okuyucular yalnız veri döndürür; *_ayni denetçileri hesapla karşılaştırır (kontrol satırı yazar).

def _div_bloklari(html, sinif):
    """class listesinde `sinif` geçen her <div …> bloğu: [(açılış etiketi, iç HTML)] (iç içe div'ler sayılır)."""
    out = []
    for m in re.finditer(r'<div\b[^>]*\bclass="([^"]*)"[^>]*>', html):
        if sinif not in m.group(1).split():
            continue
        derinlik, i = 1, m.end()
        for t in re.finditer(r"<(/?)div\b[^>]*>", html[m.end():]):
            derinlik += -1 if t.group(1) else 1
            if derinlik == 0:
                out.append((m.group(0), html[m.end():m.end() + t.start()]))
                break
    return out


def _nitelik(etiket, ad):
    m = re.search(rf'\s{ad}="([^"]*)"', etiket)
    return m.group(1) if m else None


def _duz(s):
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def kendini_dene(html):
    """{kod: [öğretmen cevabı …]} — her .kendini-dene kartındaki .soru-k satırlarının .ogr metni (yoksa None).
    kod: kartın data-soru'su, yoksa KD1, KD2 … (sayfa sırası)."""
    out = {}
    for n, (ac, ic) in enumerate(_div_bloklari(html, "kendini-dene"), 1):
        kod = _nitelik(ac, "data-soru") or f"KD{n}"
        cevap = []
        for _, soru in _div_bloklari(ic, "soru-k"):
            o = re.findall(r'<span class="ogr">(.*?)</span>', soru, re.S)
            cevap.append(_duz(o[0]) if o else None)
        out[kod] = cevap
    return out


def kendini_dene_ayni(html, beklenen):
    """beklenen: {kod: ["apolar", "olmazdı"]} — sayfadaki öğretmen cevapları (sırayla) aynı mı? Her soruda bir cevap olmalı."""
    oku = kendini_dene(html)
    for kod, b in beklenen.items():
        kontrol(f"Kendini dene {kod}: öğretmen cevapları {oku.get(kod)} == {b}", oku.get(kod) == list(b))
    return oku


def sifreli_kapi(html):
    """Şifreli Kapı: {"sorular": {kod: harf}, "sifre": doğru harflerin sırası, "kutular": .sifre kutularındaki .ogr harfleri,
    "tek": her soruda tam bir data-dogru, "benzersiz": kartta seçenek harfleri tekrarsız}. Soru kartı: .kart.sk
    (kod: data-soru, yoksa data-sk; sıra: data-sk, yoksa sayfa sırası)."""
    sorular, tek, benzersiz = [], True, True
    for n, (ac, ic) in enumerate(_div_bloklari(html, "sk"), 1):
        dogru = re.findall(r"<li\b[^>]*\bdata-dogru(?:=\"[^\"]*\")?[^>]*>\s*<b>([^<]+)</b>", ic)
        harfler = re.findall(r"<li\b[^>]*>\s*<b>([^<]+)</b>", ic)
        tek &= len(dogru) == 1
        benzersiz &= len(harfler) == len(set(harfler))
        sira = int(_nitelik(ac, "data-sk") or n)
        sorular.append((sira, _nitelik(ac, "data-soru") or f"SK{sira}", dogru[0] if dogru else None))
    sorular.sort()
    kutu = ""
    for _, ic in _div_bloklari(html, "sifre")[:1]:
        kutu = "".join(_duz(x) for x in re.findall(r'<span class="ogr">(.*?)</span>', ic, re.S))
    return {"sorular": {k: h for _, k, h in sorular}, "sifre": "".join(h or "?" for _, _, h in sorular), "kutular": kutu,
            "tek": tek, "benzersiz": benzersiz}


def sifreli_kapi_ayni(html, sifre):
    """Sayfadaki doğru seçenekler sırayla `sifre`yi yazıyor mu; öğretmen kutuları aynı mı; her soruda tek doğru var mı?"""
    s = sifreli_kapi(html)
    kontrol(f"Şifreli Kapı: her soruda tek data-dogru ({len(s['sorular'])} soru)", s["tek"] and len(s["sorular"]) == len(sifre))
    kontrol("Şifreli Kapı: kartlarda seçenek harfleri tekrarsız", s["benzersiz"])
    kontrol(f"Şifreli Kapı: doğru harfler {s['sifre']} == {sifre}", s["sifre"] == sifre)
    kontrol(f"Şifreli Kapı: öğretmen kutuları {s['kutular'] or '—'} == {sifre}", s["kutular"] == sifre)
    return s


def celdirici_rontgeni(html):
    """{kod: {"dogru": [harf], "secenekler": {harf: sayı metni}}} — .rn kartları (kod: data-soru, yoksa CR1, CR2 …)."""
    out = {}
    for n, (ac, ic) in enumerate(_div_bloklari(html, "rn"), 1):
        kod = _nitelik(ac, "data-soru") or f"CR{n}"
        sec, dogru = {}, []
        for _, sat in [x for x in _div_bloklari(ic, "rn-sec")][:1]:
            for m in re.finditer(r'<div\b([^>]*)>\s*<b>([A-E])</b>\s*<span class="say">(.*?)</span>', sat, re.S):
                sec[m.group(2)] = _duz(m.group(3))
                if "data-dogru" in m.group(1):
                    dogru.append(m.group(2))
        out[kod] = {"dogru": dogru, "secenekler": sec}
    return out


def celdirici_ayni(html, beklenen):
    """beklenen: {kod: ("B", "13, 14, 10")} — tek doğru seçenek ve sayıları aynı mı?"""
    oku = celdirici_rontgeni(html)
    for kod, (harf, sayi) in beklenen.items():
        r = oku.get(kod, {})
        kontrol(f"Çeldirici röntgeni {kod}: doğru {r.get('dogru')} == ['{harf}']", r.get("dogru") == [harf])
        kontrol(f"Çeldirici röntgeni {kod}: {harf} = {sayi}", r.get("secenekler", {}).get(harf) == sayi)
    return oku


def robot_hatalari(html):
    """{kod: [hatalı cümle no …]} — Robot yanıldı mı? kartlarında (.robot-kart; kod: data-soru, yoksa RB1 …) .bot-cevap
    listesinde data-dogru ile işaretli cümlelerin sırası (1'den)."""
    out = {}
    for n, (ac, ic) in enumerate(_div_bloklari(html, "robot-kart"), 1):
        kod = _nitelik(ac, "data-soru") or f"RB{n}"
        li = re.findall(r"<li\b([^>]*)>", "".join(x for _, x in _div_bloklari(ic, "bot-cevap")))
        out[kod] = [i for i, n_ in enumerate(li, 1) if "data-dogru" in n_]
    return out


def robot_ayni(html, beklenen):
    """beklenen: {kod: 3} — her kartta TEK hatalı cümle işaretli ve beklenen cümle mi?"""
    oku = robot_hatalari(html)
    for kod, no in beklenen.items():
        kontrol(f"Robot yanıldı mı? {kod}: işaretli cümle {oku.get(kod)} == [{no}]", oku.get(kod) == [no])
    return oku


def katla_cevaplari(html):
    """{kod: {"urun": "NaCl", "tur": "iyonik"}} — kat sayfalarının öğretmen cevapları (<g class="ogr-svg" data-katla=…>)."""
    return {m.group(1): {"urun": m.group(2), "tur": m.group(3)}
            for m in re.finditer(r'<g class="ogr-svg" data-katla="([^"]+)" data-urun="([^"]*)" data-tur="([^"]*)">', html)}


def katla_ayni(html, beklenen):
    """beklenen: {kod: (ürün, tür)} ya da {kod: ürün} — kat sayfasındaki öğretmen cevapları hesapla aynı mı?"""
    oku = katla_cevaplari(html)
    for kod, b in beklenen.items():
        urun, tur = (b, None) if isinstance(b, str) else b
        r = oku.get(kod, {})
        kontrol(f"katla {kod}: ürün {r.get('urun')} == {urun}", r.get("urun") == urun)
        if tur is not None:
            kontrol(f"katla {kod}: tür {r.get('tur')} == {tur}", r.get("tur") == tur)
    return oku


def uc_boyut_resimleri(html, html_yolu, dpi=300, tol_mm=.3):
    """Sayfadaki 3B resimleri (img.ana, img.duz): dosya var mı, basılı ölçü (style mm) = piksel / dpi mi? → [(src, sorun)]."""
    from PIL import Image
    klasor = os.path.dirname(os.path.abspath(html_yolu))
    sorun = []
    for m in re.finditer(r'<img class="(?:ana|duz)[^"]*" src="([^"]+)"[^>]*style="width:([\d.]+)mm;height:([\d.]+)mm"', html):
        yol = os.path.normpath(os.path.join(klasor, m.group(1)))
        if not os.path.exists(yol):
            sorun.append((m.group(1), "dosya yok"))
            continue
        w, h = Image.open(yol).size
        if abs(w / dpi * 25.4 - float(m.group(2))) > tol_mm or abs(h / dpi * 25.4 - float(m.group(3))) > tol_mm:
            sorun.append((m.group(1), f"{w}×{h} px ≠ {m.group(2)}×{m.group(3)} mm @ {dpi} dpi"))
    return sorun
