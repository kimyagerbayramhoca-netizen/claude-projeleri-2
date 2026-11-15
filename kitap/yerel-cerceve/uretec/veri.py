"""Kitap çerçevesinin verisi: rotalar.json + ünitelerin uretec/meta.json dosyaları + sayfa planı.

Kural: bir ünitenin yeni tasarım klasörü (`kitap/<sınıf>-sinif-yerel/<klasör>/`) varsa ünite "hazır" sayılır.
Hazır ünitenin bilgisi önce kendi `uretec/meta.json` dosyasından okunur; o dosya yoksa ya da bir alan eksikse
rotalar.json'daki öneri değer kullanılır. Nişan adları meta.json'da yoksa ünitenin `uretec/sablon.html`
dosyasındaki "Kazanılacak nişanlar" bloğundan okunur; o da yoksa nişan adı UYDURULMAZ (boş yuva çizilir).
"""
import glob
import json
import os
import re

BURA = os.path.dirname(os.path.abspath(__file__))
CERCEVE = os.path.dirname(BURA)
KITAP = os.path.dirname(CERCEVE)
ORTAK = os.path.join(KITAP, "yerel-ortak")

# Yol renkleri (palet tokenları; harita, rozet ve içindekilerde aynı)
YOL_RENK = {1: ("#E2533D", "#A12817"), 2: ("#2B50B5", "#1B3584"), 3: ("#F0A21A", "#8C5500"), 4: ("#13A3A6", "#0A6C74"),
            5: ("#7B3F8C", "#4E2760"), 6: ("#1F8A5B", "#145C3C"), 7: ("#FF5C8A", "#B2244F"), 8: ("#0E4C5A", "#07303A"),
            9: ("#C9952B", "#8A6212"), 10: ("#FF7A3D", "#B2461A")}


def rotalar():
    with open(os.path.join(CERCEVE, "rotalar.json"), encoding="utf-8") as f:
        return json.load(f)


def _say(dosya, kalip):
    try:
        with open(dosya, encoding="utf-8") as f:
            return len(re.findall(kalip, f.read()))
    except OSError:
        return 0


def _sablon_nisanlari(dizin):
    """Ünitenin açılış sayfasındaki nişan listesi: {{nisan|ikon}}<b>Ad</b><span>açıklama</span>."""
    yol = os.path.join(dizin, "uretec", "sablon.html")
    if not os.path.exists(yol):
        return None
    s = open(yol, encoding="utf-8").read()
    m = re.search(r'<div class="nisanlar">(.*?)</div>\s*(?:<div class="bento|<div class="kart|</main)', s, re.S)
    if not m:
        return None
    out = [{"ad": ad.strip(), "ikon": ikon, "aciklama": re.sub(r"<[^>]+>", "", ac).strip()}
           for ikon, ad, ac in re.findall(r"\{\{nisan\|(\w+)[^}]*\}\}<b>([^<]+)</b><span>(.*?)</span>", m.group(1))]
    return out or None


def _metin(x):
    return re.sub(r"\s+", " ", x).strip() if isinstance(x, str) else x


def yollar(sinif):
    """Bir sınıfın bütün yolları (Yol sırasıyla), hazır ünitelerin bilgisi meta.json ile güncellenmiş."""
    veri = rotalar()
    out = []
    for r in sorted((r for r in veri["rotalar"] if r["sinif"] == int(sinif)), key=lambda r: r["yol"]):
        y = json.loads(json.dumps(r))
        dizin = os.path.join(KITAP, f"{sinif}-sinif-yerel", r["klasor"])
        # ünite "hazır": yeni tasarım klasörü var VE en az bir kez kurulmuş (unite.html) — yapım aşamasındakiler kitaba girmez
        y["dizin"] = dizin if os.path.isdir(dizin) else None
        y["hazir"] = y["dizin"] is not None and os.path.exists(os.path.join(dizin, "unite.html"))
        y["renk"], y["renk_k"] = YOL_RENK[r["yol"]]
        y["nisanlar"] = None
        y["nisan_kaynak"] = None
        y["hazine"] = []
        y["kavramlar"] = []
        y["sayfa_sayisi"] = 0
        y["varyantlar"] = {}
        y["meta"] = False
        if y["hazir"]:
            meta_yol = os.path.join(dizin, "uretec", "meta.json")
            meta = {}
            if os.path.exists(meta_yol):
                try:
                    meta = json.load(open(meta_yol, encoding="utf-8"))
                    y["meta"] = True
                except (OSError, ValueError) as e:
                    print(f"UYARI: {meta_yol} okunamadı: {e}")
            for k in ("rota", "unite", "tema", "bolge", "merkez"):
                if meta.get(k):
                    y[k] = meta[k]
            if meta.get("duraklar"):
                yeni = []
                for d in meta["duraklar"]:
                    if "enlem" in d and "boylam" in d:
                        yeni.append({"no": d.get("no", len(yeni) + 1), "yer": d.get("yer", ""),
                                     "konu": d.get("baslik") or d.get("konu", ""), "enlem": d["enlem"], "boylam": d["boylam"]})
                if yeni:
                    y["duraklar"] = yeni
            if isinstance(meta.get("kale_konum"), dict) and "enlem" in meta["kale_konum"]:
                y["kale"] = {"ad": y["kale"]["ad"], "enlem": meta["kale_konum"]["enlem"], "boylam": meta["kale_konum"]["boylam"]}
            if meta.get("kale"):
                k = meta["kale"]
                if isinstance(k, dict) and "enlem" in k:
                    y["kale"] = {"ad": k.get("ad", y["kale"]["ad"]), "enlem": k["enlem"], "boylam": k["boylam"]}
                elif isinstance(k, str):
                    y["kale"]["ad"] = k
            if meta.get("medeniyet"):
                y["medeniyet"] = [m["ad"] if isinstance(m, dict) else m for m in meta["medeniyet"]]
                y["medeniyet_ayrinti"] = [m for m in meta["medeniyet"] if isinstance(m, dict)]
            if meta.get("nisanlar"):
                y["nisanlar"] = [{"ad": _metin(n.get("ad", "")), "ikon": n.get("ikon", ""), "aciklama": _metin(n.get("aciklama", ""))}
                                 for n in meta["nisanlar"]]
                y["nisan_kaynak"] = "meta.json"
            y["hazine"] = meta.get("hazine", [])
            y["kavramlar"] = meta.get("kavramlar", [])
            if y["nisanlar"] is None:
                n = _sablon_nisanlari(dizin)
                if n:
                    y["nisanlar"] = n
                    y["nisan_kaynak"] = "sablon.html"
            y["sayfa_sayisi"] = _say(os.path.join(dizin, "unite.html"), r'<section class="sayfa[\s"]') or int(meta.get("sayfa_sayisi") or 0)
            for v in ("fotokopi", "ogretmen", "hazine-kartlari"):
                p = os.path.join(dizin, f"{r['klasor']}-{v}.pdf")
                if os.path.exists(p):
                    y["varyantlar"][v] = p
        out.append(y)
    return out


def baslangic():
    return rotalar()["baslangic"]


def alt_baslik(sinif):
    return rotalar()["siniflar"][str(sinif)]["alt_baslik"]


# ------------------------------------------------------------------ sayfa planı

def sayfa_plani(sinif, yol_listesi, sozluk_n, album_n, hazine_pdf=None):
    """Kitabın bütün sayfaları sırayla: [{'tur', 'no', ...}].

    Sıra: ön kapak → rehber (2) → harita/içindekiler → üniteler (Yol sırası; her biri tek numaralı sayfada) →
    zaman şeridi (karşılıklı iki sayfa: çift numarada başlar) → periyodik tablo → sözlük → nişan albümü →
    hazine kartları eki (ünitelerden PDF gelirse) → arka kapak (çift numaralı sayfa).
    Araya gerekirse "Notlar" sayfası (tur='bos') girer.
    """
    plan = []

    def ekle(tur, **k):
        plan.append(dict(tur=tur, no=len(plan) + 1, **k))

    ekle("kapak")
    ekle("rehber", parca=1)
    ekle("rehber", parca=2)
    ekle("harita")
    baslar = {}
    for y in yol_listesi:
        if not (y["hazir"] and y["sayfa_sayisi"]):
            continue
        if (len(plan) + 1) % 2 == 0:
            ekle("bos")
        baslar[y["yol"]] = len(plan) + 1
        for i in range(y["sayfa_sayisi"]):
            ekle("unite", yol=y["yol"], sayfa=i + 1, ilk=(i == 0))
    if (len(plan) + 1) % 2 == 1:
        ekle("bos")
    ekle("zaman", parca=1)
    ekle("zaman", parca=2)
    ekle("periyodik")
    for i in range(sozluk_n):
        ekle("sozluk", parca=i + 1)
    for i in range(album_n):
        ekle("album", parca=i + 1)
    for yol, (yol_pdf, n) in sorted((hazine_pdf or {}).items()):
        for i in range(n):
            ekle("hazine", yol=yol, pdf=yol_pdf, sayfa=i + 1, ilk=(i == 0))
    if (len(plan) + 1) % 2 == 1:
        ekle("bos")
    ekle("arka_kapak")
    return plan, baslar


def ilk_no(plan, tur, **k):
    for p in plan:
        if p["tur"] == tur and all(p.get(a) == b for a, b in k.items()):
            return p["no"]
    return None


def turkce_anahtar(s):
    """Türkçe alfabe sırası (ç, ğ, ı, i, ö, ş, ü) için sıralama anahtarı; şapkalı harfler düzleştirilir."""
    alfabe = "abcçdefgğhıijklmnoöprsştuüvyz"
    duz = {"â": "a", "î": "i", "û": "u", "Â": "a", "Î": "i", "Û": "u", "q": "k", "w": "v", "x": "ks"}
    s = s.replace("I", "ı").replace("İ", "i").lower()
    out = []
    for ch in s:
        ch = duz.get(ch, ch)
        for c in ch:
            if c in alfabe:
                out.append(alfabe.index(c) + 1)
            elif c.isdigit():
                out.append(0)
    return tuple(out)


def ilk_harf(s):
    c = s.strip()[0]
    c = {"â": "a", "î": "i", "û": "u"}.get(c, c)
    return "İ" if c == "i" else ("I" if c == "ı" else c.upper())


if __name__ == "__main__":
    for s in (9, 10):
        ys = yollar(s)
        print(s, [(y["yol"], y["rota"], y["hazir"], y["sayfa_sayisi"], y["nisan_kaynak"]) for y in ys])
        plan, bas = sayfa_plani(s, ys, 2, 2)
        print("  ", len(plan), "sayfa; ünite başları:", bas)
