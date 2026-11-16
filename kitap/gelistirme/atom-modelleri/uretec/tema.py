"""Renk temaları · kurulum anında palet eşlemesi (fotokopi.py ile aynı yöntem; CSS `filter` YOK).

Kitap her zaman "Van Gölü" renkleriyle kurulur; tema, üretilen HTML'e SONRADAN uygulanır:
  1. stil.css (+ yerel CSS) satır içi <style> olarak gömülür; içindeki bütün renkler (tokenlar + elle yazılmış
     onaltılık renkler + rgba) temaya eşlenir; url() yolları HTML'in yerine göre düzeltilir.
  2. Satır içi SVG'lerde fill / stroke / stop-color / style renkleri eşlenir.
  3. Ebru dokusu (ebru-gol.jpg) aynı eşlemeyle piksel piksel boyanır → gorsel/ebru-gol-<tema>.jpg.

Eşleme ("token çarpıtması", OKLab uzayında):
  • Her tema, renkler.py / stil.css tokenlarının (gol, keh, mer, kob, obs, kar …) yeni değerini verir.
  • Kodda türetilen tonlar (acik(GOL,.6), koyu(KEH,.3), gradyan durakları) tokenların BEYAZA ve SİYAHA karışım
    doğruları üzerindedir. Bu doğrular üstüne ara çapalar konur: acik(X, t) → acik(X', t), koyu(X, t) → koyu(X', t).
  • Herhangi bir renk c için: en yakın çapalardan ters kare uzaklık ağırlıklı kayma (Shepard) hesaplanır ve
    c' = c + s·Δ uygulanır; s = exp(−(d_min/σ)²) uzak renklerde sıfıra iner (deri, gök, toprak tonları değişmez).
  • Token rengine birebir eşit renk, tam olarak temanın token değerine gider.

Anlam renkleri sabit kalır (bütün temalarda aynı aile): keh = ödül/akçe (altın-kehribar), mer = Tuzak/Dikkat
(kırmızı), zumrut = doğru (yeşil). Tema KİMLİK renklerini değiştirir: gol (ana renk), kob (kavram), obs (mürekkep, HUD),
derin (sert gölge), zemin, gri, tezhip ve gün batımı tonları.

Dokunulmayanlar (data-tema-sabit mantığı):
  • karakterler (Pamuk, Elif, Yusuf, Zeynep, avatarlar, konu karakterleri kk-*) ve onların gradyanları (kr-*, kk-*)
  • data-tema-sabit taşıyan her öğe ve içi (spektrum çizgileri, dalga boyuna göre renkli fotonlar)
  • mask / clipPath içi
  • sahne bantları (svg.sahne) token çarpıtmasıyla değil, temanın "sahne" eşlemesiyle boyanır (gece, sıcak, yumuşak).
"""
import math
import os
import re

# ------------------------------------------------------------------ Van Gölü tokenları (stil.css :root = renkler.py)
TOKENLAR = [
    "kar", "kirec", "obs", "obs-2", "soluk", "cizgi",
    "gol", "gol-k", "gol-a", "gol-aa", "derin",
    "keh", "keh-k", "keh-a", "mer", "mer-k", "mer-a", "kob", "kob-k", "kob-a",
    "gun", "pembe", "erguvan", "altin", "altin-k", "altin-a", "lajver",
    "zumrut", "gum", "gum-k", "gum-a",
]
VAN = {
    "kar": "#FBFDFD", "kirec": "#FFFDF7", "obs": "#1B1D26", "obs-2": "#343947", "soluk": "#56636E", "cizgi": "#CFDCE0",
    "gol": "#13A3A6", "gol-k": "#0A6C74", "gol-a": "#DCF3F1", "gol-aa": "#EEF9F8", "derin": "#0E4C5A",
    "keh": "#F0A21A", "keh-k": "#8C5500", "keh-a": "#FFF0CF",
    "mer": "#E2533D", "mer-k": "#A12817", "mer-a": "#FDE7E1",
    "kob": "#2B50B5", "kob-k": "#1B3584", "kob-a": "#E6ECFB",
    "gun": "#FF7A3D", "pembe": "#FF5C8A", "erguvan": "#7B3F8C",
    "altin": "#C9952B", "altin-k": "#8A6212", "altin-a": "#F6E7BF", "lajver": "#1D3A8A",
    "zumrut": "#1F8A5B", "gum": "#A3B3BE", "gum-k": "#586874", "gum-a": "#EDF2F5",
}
# renkler.py'de olup stil.css'te olmayan iki token (eşleme için çapa)
VAN_EK = {"alaca": "#3B2E6E", "hud-yer": "#C9D6DC", "hud-bar": "#3B4352", "hud-nokta": "#8FA3AD", "vurgu": "#FFD978"}

# ------------------------------------------------------------------ TEMALAR
# Her temada: ad, kısa açıklama, gök/sahne eşlemesi ve tokenların yeni değerleri (eksik token Van Gölü'nde kalır).
TEMALAR = {
    "van-golu": {
        "ad": "Van Gölü", "aciklama": "Şu anki palet: göl turkuazı, kehribar, İznik mercanı ve kobaltı, tezhip altını.",
        "sahne": "aynen", "renk": dict(VAN), "ek": dict(VAN_EK),
    },
    "iznik-cini": {
        "ad": "İznik Çini", "aciklama": "Bembeyaz zemin, kobalt ana renk, mercan kırmızısı, çini yeşili; serin ve keskin.",
        "sahne": "aynen",
        "renk": {
            "kar": "#FFFFFF", "kirec": "#FFFEFA", "obs": "#131A33", "obs-2": "#2B3556", "soluk": "#4E5A73", "cizgi": "#D2DBEE",
            "gol": "#1F4FA8", "gol-k": "#14377C", "gol-a": "#DDE6F7", "gol-aa": "#EFF3FC", "derin": "#0E2457",
            "keh": "#F2A516", "keh-k": "#8A5300", "keh-a": "#FFF1CF",
            "mer": "#E04A35", "mer-k": "#A11E12", "mer-a": "#FDE4DF",
            "kob": "#20855A", "kob-k": "#135C3C", "kob-a": "#DFF2E7",
            "gun": "#F26B3A", "pembe": "#E94E7C", "erguvan": "#5E3D93",
            "altin": "#C9952B", "altin-k": "#8A6212", "altin-a": "#F6E7BF", "lajver": "#173A8F",
            "zumrut": "#127A4F", "gum": "#A9B5C8", "gum-k": "#55617A", "gum-a": "#EEF1F7",
        },
        "ek": {"alaca": "#24306E", "hud-yer": "#C9D3E8", "hud-bar": "#323D60", "hud-nokta": "#8C9BBA", "vurgu": "#FFD978"},
    },
    "selcuklu-toprak": {
        "ad": "Selçuklu Toprak", "aciklama": "Kerpiç-terakota ana renk, lacivert taş (lapis), altın, turkuaz; sıcak ve köklü.",
        "sahne": "sicak",
        "renk": {
            "kar": "#FCF9F3", "kirec": "#FFFBF1", "obs": "#2A1D16", "obs-2": "#4A372B", "soluk": "#6A584B", "cizgi": "#E5D6C6",
            "gol": "#B4532C", "gol-k": "#7C3416", "gol-a": "#F6E0D2", "gol-aa": "#FBF1EA", "derin": "#5A2B15",
            "keh": "#D69E1E", "keh-k": "#7A5608", "keh-a": "#FBEFC8",
            "mer": "#8F1B2C", "mer-k": "#6A0F1E", "mer-a": "#F8E0E3",
            "kob": "#25479B", "kob-k": "#16306F", "kob-a": "#E2E8F6",
            "gun": "#E0783A", "pembe": "#D65A6E", "erguvan": "#77406C",
            "altin": "#C9952B", "altin-k": "#85600F", "altin-a": "#F6E6BC", "lajver": "#1E3A87",
            "zumrut": "#0E766C", "gum": "#B8A99B", "gum-k": "#6B5D51", "gum-a": "#F3EEE7",
        },
        "ek": {"alaca": "#4A2F3A", "hud-yer": "#E2CDB8", "hud-bar": "#4C3A2E", "hud-nokta": "#A8917C", "vurgu": "#FFD978"},
    },
    "rasathane-gecesi": {
        "ad": "Rasathane Gecesi", "aciklama": "Gece laciverti ve erguvan, yıldız altını; sahneler gece, metin alanları yine açık.",
        "sahne": "gece",
        "renk": {
            "kar": "#F8F8FD", "kirec": "#FFFDF5", "obs": "#12173A", "obs-2": "#2B3160", "soluk": "#535A80", "cizgi": "#D5D7EC",
            "gol": "#3443A8", "gol-k": "#1F2A78", "gol-a": "#E0E3F7", "gol-aa": "#F0F1FC", "derin": "#161B47",
            "keh": "#E2A81C", "keh-k": "#7F5A06", "keh-a": "#FCF0CB",
            "mer": "#D9414F", "mer-k": "#991A2A", "mer-a": "#FCE3E6",
            "kob": "#8A5BC4", "kob-k": "#55308E", "kob-a": "#F1E9FA",
            "gun": "#F2884C", "pembe": "#E35C9A", "erguvan": "#7A2860",
            "altin": "#D4A02C", "altin-k": "#866011", "altin-a": "#F7E9C2", "lajver": "#1A2368",
            "zumrut": "#127559", "gum": "#A7ABC7", "gum-k": "#575D82", "gum-a": "#EEEFF8",
        },
        "ek": {"alaca": "#2A2266", "hud-yer": "#C3C8E8", "hud-bar": "#2E3466", "hud-nokta": "#8A90BA", "vurgu": "#FFDC7A"},
    },
    "yumusak-pastel": {
        "ad": "Yumuşak Pastel", "aciklama": "Adaçayı yeşili, şeftali, lavanta; az doygun, göz yormayan tonlar; mürekkep yine koyu.",
        "sahne": "yumusak",
        "renk": {
            "kar": "#FDFCF8", "kirec": "#FFFDF8", "obs": "#2A2E39", "obs-2": "#434957", "soluk": "#5E6672", "cizgi": "#DDE3E5",
            "gol": "#5E9A78", "gol-k": "#36664B", "gol-a": "#E2EFE5", "gol-aa": "#F2F8F3", "derin": "#7D9688",
            "keh": "#EBAA5E", "keh-k": "#80530F", "keh-a": "#FFF1DE",
            "mer": "#DD7464", "mer-k": "#9C3B2C", "mer-a": "#FCEAE5",
            "kob": "#7A86C4", "kob-k": "#434F8C", "kob-a": "#EDEFFA",
            "gun": "#F29B6E", "pembe": "#EE8AA5", "erguvan": "#8C5A86",
            "altin": "#C9A257", "altin-k": "#81622A", "altin-a": "#F6ECD4", "lajver": "#3D5390",
            "zumrut": "#2C7560", "gum": "#B6C0C6", "gum-k": "#626E76", "gum-a": "#F1F4F5",
        },
        "ek": {"alaca": "#4D4A7A", "hud-yer": "#D0D9DD", "hud-bar": "#4A505C", "hud-nokta": "#98A6AE", "vurgu": "#FFE3A0"},
    },
}
SIRA = ["van-golu", "iznik-cini", "selcuklu-toprak", "rasathane-gecesi", "yumusak-pastel"]
AKTIF = "van-golu"          # kurulum sırasında sahne sarmalayıcıları okur (gece temasında yıldız eklemek için)

# ------------------------------------------------------------------ renk uzayı (sRGB ↔ OKLab)


def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(t):
    return "#" + "".join(f"{max(0, min(255, round(v))):02X}" for v in t)


def _lin(c):
    c /= 255
    return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4


def _gam(c):
    c = max(0.0, min(1.0, c))
    return 255 * (12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055)


def oklab(h):
    r, g, b = (_lin(v) for v in hex_rgb(h))
    l = .4122214708 * r + .5363325363 * g + .0514459929 * b
    m = .2119034982 * r + .6806995451 * g + .1073969566 * b
    s = .0883024619 * r + .2817188376 * g + .6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (.2104542553 * l + .7936177850 * m - .0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + .4505937099 * s,
            .0259040371 * l + .7827717662 * m - .8086757660 * s)


def oklab_hex(L, a, b):
    l = (L + .3963377774 * a + .2158037573 * b) ** 3
    m = (L - .1055613458 * a - .0638541728 * b) ** 3
    s = (L - .0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + .2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s
    bb = -.0041960863 * l - .7034186147 * m + 1.7076147010 * s
    return rgb_hex((_gam(r), _gam(g), _gam(bb)))


def karis(a, b, t):
    x, y = hex_rgb(a), hex_rgb(b)
    return rgb_hex(tuple(x[i] + (y[i] - x[i]) * t for i in range(3)))


def goreli_parlaklik(h):
    r, g, b = (_lin(v) for v in hex_rgb(h))
    return .2126 * r + .7152 * g + .0722 * b


def kontrast(a, b):
    la, lb = goreli_parlaklik(a), goreli_parlaklik(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


# ------------------------------------------------------------------ token çarpıtması

SIGMA = .12           # bu uzaklıktan sonra eşleme söner (deri, gök, toprak tonları değişmez)
TAU = .035            # komşu çapaların karışma genişliği
_ADIM = (.12, .25, .4, .55, .7, .85)
_GRI = {"kar", "kirec", "cizgi", "gol-aa", "gum-a"}      # zaten beyaza çok yakın: karışım doğrusu eklenmez
_DL = (-.16, -.08, .08, .16)                              # token çevresinde açıklık oynaması
_DC = (.55, 1.35)                                         # token çevresinde doygunluk oynaması


def _lch_oyna(lab, dL=0.0, kc=1.0):
    L, a, b = lab
    return (L + dL, a * kc, b * kc)


class Esleme:
    """Bir temanın renk eşlemesi. esle('#13A3A6') → temadaki karşılığı."""

    def __init__(self, ad):
        import numpy as np
        self.np = np
        self.ad = ad
        self.tema = TEMALAR[ad]
        self.kimlik = ad == "van-golu"
        self.onbellek = {}
        kaynak = dict(VAN)
        kaynak.update(VAN_EK)
        hedef = dict(VAN)
        hedef.update(VAN_EK)
        hedef.update(self.tema["renk"])
        hedef.update(self.tema.get("ek", {}))
        self.tam = {kaynak[k].upper(): hedef[k].upper() for k in kaynak}
        self.tam["#FFFFFF"] = "#FFFFFF"
        self.tam["#000000"] = "#000000"
        S, T = [], []
        for k in kaynak:
            s, t = kaynak[k], hedef[k]
            ls, lt = oklab(s), oklab(t)
            S.append(ls), T.append(lt)
            if k in _GRI:
                continue
            for a in _ADIM:                                    # beyaza / siyaha karışım doğruları
                S.append(oklab(karis(s, "#FFFFFF", a))), T.append(oklab(karis(t, "#FFFFFF", a)))
                S.append(oklab(karis(s, "#000000", a * .8))), T.append(oklab(karis(t, "#000000", a * .8)))
            renkli = math.hypot(ls[1], ls[2]) > .045
            for dL in _DL:                                     # yerel afin komşuluk: açıklık ve doygunluk oynaması
                for kc in ((1.0,) + _DC if renkli else (1.0,)):
                    S.append(_lch_oyna(ls, dL, kc)), T.append(_lch_oyna(lt, dL, kc))
            if renkli:
                for kc in _DC:
                    S.append(_lch_oyna(ls, 0, kc)), T.append(_lch_oyna(lt, 0, kc))
        for c in ("#FFFFFF", "#000000"):
            S.append(oklab(c)), T.append(oklab(c))
        self.S = np.array(S)
        self.D = np.array(T) - self.S

    def _kayma(self, C):
        """C: (n,3) OKLab dizisi → kaydırılmış (n,3)."""
        np = self.np
        u = ((C[:, None, :] - self.S[None, :, :]) ** 2).sum(-1)       # (n, N) kare uzaklık
        umin = u.min(1)
        w = np.exp(-(u - umin[:, None]) / TAU ** 2)                    # yumuşak en yakın komşu
        d = (w[:, :, None] * self.D[None, :, :]).sum(1) / w.sum(1)[:, None]
        guc = np.exp(-umin / SIGMA ** 2)
        return C + guc[:, None] * d

    def esle(self, h):
        if self.kimlik:
            return h
        anahtar = h.upper()
        if len(anahtar) == 4:
            anahtar = "#" + "".join(c * 2 for c in anahtar[1:])
        if anahtar in self.tam:
            return self.tam[anahtar]
        if anahtar in self.onbellek:
            return self.onbellek[anahtar]
        C = self._kayma(self.np.array([oklab(anahtar)]))[0]
        sonuc = oklab_hex(*C)
        self.onbellek[anahtar] = sonuc
        return sonuc

    # sahne bantları: doğal kalsın; temaya göre yalnız ışık/mevsim eşlemesi
    def sahne(self, h):
        tur = self.tema["sahne"]
        if tur == "aynen":
            return h
        anahtar = "s" + h.upper()
        if anahtar in self.onbellek:
            return self.onbellek[anahtar]
        L, a, b = oklab(h)
        if tur == "gece":          # ay ışığı: koyulaştır, laciverte-mora kaydır, sıcak ışıkları (pencere, fener) koru
            sicak = max(0.0, min(1.0, (b - .03) * 8)) * max(0.0, min(1.0, (L - .7) * 5))
            L2 = .07 + .5 * L ** 1.5
            L2 = L2 + (L - L2) * .7 * sicak
            a2 = .45 * a + .01 + (a - .45 * a) * .6 * sicak
            b2 = .45 * b - .062 * (1 - sicak) + (b - .45 * b) * .6 * sicak
            sonuc = oklab_hex(L2, a2, b2)
        elif tur == "sicak":       # ikindi altını: hafif sıcak ve topraksı
            sonuc = oklab_hex(L * .985, a * .95 + .008, b * .95 + .022)
        elif tur == "yumusak":     # pastel: doygunluk düşer, ışık artar
            sonuc = oklab_hex(L + (1 - L) * .2, a * .56, b * .56)
        else:
            sonuc = h
        self.onbellek[anahtar] = sonuc
        return sonuc

    def token(self, k):
        r = dict(VAN)
        r.update(self.tema["renk"])
        return r[k]


# ------------------------------------------------------------------ CSS

_HEXRE = re.compile(r"(?<!url\()#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b")
_RGBA = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(,\s*[\d.]+\s*)?\)")


def css_esle(css, es, fn=None):
    fn = fn or es.esle
    css = _HEXRE.sub(lambda m: fn(m.group(0)), css)

    def rgba(m):
        h = fn(rgb_hex((int(m.group(1)), int(m.group(2)), int(m.group(3)))))
        r, g, b = hex_rgb(h)
        return f"rgba({r}, {g}, {b}{m.group(4) or ', 1'})"
    return _RGBA.sub(rgba, css)


# ------------------------------------------------------------------ SVG / HTML yürüyücüsü

_ETIKET = re.compile(r"<(/?)([a-zA-Z][\w:.-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*?)(/?)>")
_NITELIK = re.compile(r'(\s)(fill|stroke|stop-color|flood-color|lighting-color|color)=("|\')(.*?)\3')
_STIL = re.compile(r'(\sstyle=)("|\')(.*?)\2', re.S)
_ID = re.compile(r'\sid=["\']([^"\']+)["\']')
_CLASS = re.compile(r'\sclass=["\']([^"\']+)["\']')
BOS_ETIKET = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "use",
              "stop", "path", "circle", "rect", "ellipse", "line", "polyline", "polygon", "image"}
SABIT_ONEK = ("pamuk-", "elif-", "yusuf-", "zeynep-", "av-", "kk-", "kr-", "akce")


def _mod(ad, nitelik, ust):
    """Açılan etiketin boyama kipi: warp (token eşlemesi) · sahne · sabit · maske."""
    if ust in ("sabit", "maske"):
        return ust
    if ad in ("mask", "clippath"):
        return "maske"
    if "data-tema-sabit" in nitelik:
        return "sabit"
    m = _ID.search(nitelik)
    if m and m.group(1).startswith(SABIT_ONEK) and ad in ("symbol", "lineargradient", "radialgradient", "pattern", "g"):
        return "sabit"
    if ad == "svg":
        c = _CLASS.search(nitelik)
        if c and "sahne" in c.group(1).split():
            return "sahne"
    return ust


def html_esle(html, es):
    """HTML içindeki satır içi SVG renklerini ve style="" renklerini eşler (yorumlar dokunulmaz)."""
    if es.kimlik:
        return html
    parcalar = re.split(r"(<!--.*?-->|<style[^>]*>.*?</style>|<script[^>]*>.*?</script>)", html, flags=re.S)
    out = []
    yigin = [("kok", "warp")]
    for parca in parcalar:
        if parca.startswith("<!--") or parca.startswith("<style") or parca.startswith("<script"):
            out.append(parca)
            continue
        i = 0
        for m in _ETIKET.finditer(parca):
            out.append(parca[i:m.start()])
            i = m.end()
            kapanis, ad, nitelik, kendinden = m.groups()
            adk = ad.lower()
            if kapanis:
                for j in range(len(yigin) - 1, 0, -1):
                    if yigin[j][0] == adk:
                        del yigin[j:]
                        break
                out.append(m.group(0))
                continue
            mod = _mod(adk, nitelik, yigin[-1][1])
            if mod in ("warp", "sahne"):
                fn = es.esle if mod == "warp" else es.sahne
                nitelik = _NITELIK.sub(lambda n: n.group(1) + n.group(2) + "=" + n.group(3) +
                                       (fn(n.group(4).strip()) if _HEXRE.fullmatch(n.group(4).strip()) else n.group(4)) + n.group(3), nitelik)
                nitelik = _STIL.sub(lambda n: n.group(1) + n.group(2) + css_esle(n.group(3), es, fn) + n.group(2), nitelik)
            if not kendinden and adk not in BOS_ETIKET:
                yigin.append((adk, mod))
            out.append(f"<{ad}{nitelik}{kendinden}>")
        out.append(parca[i:])
    return "".join(out)


# ------------------------------------------------------------------ ebru dokusu (JPEG) · 3B renk tablosu ile


def ebru_boya(kaynak, hedef, es, n=33):
    import numpy as np
    from PIL import Image
    im = np.asarray(Image.open(kaynak).convert("RGB")).astype(np.float32)
    izgara = np.linspace(0, 255, n)
    r, g, b = np.meshgrid(izgara, izgara, izgara, indexing="ij")
    rgb = np.stack([r, g, b], -1).reshape(-1, 3)
    lab = np.array([oklab(rgb_hex(t)) for t in rgb])
    yeni = np.concatenate([es._kayma(lab[i:i + 2000]) for i in range(0, len(lab), 2000)])
    lut = np.array([hex_rgb(oklab_hex(*c)) for c in yeni], np.float32).reshape(n, n, n, 3)
    p = im / 255 * (n - 1)
    p0 = np.clip(np.floor(p).astype(int), 0, n - 2)
    t = p - p0
    out = np.zeros_like(im)
    for dr in (0, 1):
        for dg in (0, 1):
            for db in (0, 1):
                w = ((t[..., 0] if dr else 1 - t[..., 0]) * (t[..., 1] if dg else 1 - t[..., 1]) * (t[..., 2] if db else 1 - t[..., 2]))
                out += w[..., None] * lut[p0[..., 0] + dr, p0[..., 1] + dg, p0[..., 2] + db]
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(hedef, quality=88)


# ------------------------------------------------------------------ bütün sayfa


def tema_html(html, ad, css_dosyalari, cikti_yolu, ortak):
    """Kurulmuş (Van Gölü renkli) HTML'e temayı uygular. css_dosyalari: [(yol, <link> kalıbı)] sırayla gömülür."""
    es = Esleme(ad)
    klasor = os.path.dirname(os.path.abspath(cikti_yolu))
    gorsel = os.path.join(klasor, "gorsel")
    os.makedirs(gorsel, exist_ok=True)
    if es.kimlik:
        ebru_gol = os.path.relpath(os.path.join(ortak, "gorsel", "ebru-gol.jpg"), klasor)
    else:
        ebru_gol = os.path.join(gorsel, f"ebru-gol-{ad}.jpg")
        if not os.path.exists(ebru_gol) or os.path.getmtime(ebru_gol) < os.path.getmtime(__file__):
            ebru_boya(os.path.join(ortak, "gorsel", "ebru-gol.jpg"), ebru_gol, es)
        ebru_gol = os.path.relpath(ebru_gol, klasor)
    ebru_gun = os.path.relpath(os.path.join(ortak, "gorsel", "ebru-gun.jpg"), klasor)
    fontlar = os.path.relpath(os.path.join(ortak, "..", "fontlar"), klasor)
    for yol, kalip in css_dosyalari:
        with open(yol, encoding="utf-8") as fp:
            css = fp.read()
        css = css_esle(css, es)
        css = css.replace('url("../fontlar/', f'url("{fontlar}/').replace('url("gorsel/ebru-gol.jpg")', f'url("{ebru_gol}")')
        css = css.replace('url("gorsel/ebru-gun.jpg")', f'url("{ebru_gun}")')
        html = re.sub(kalip, lambda m: f"<style>/* {os.path.basename(yol)} · tema: {TEMALAR[ad]['ad']} */\n{css}\n</style>", html, count=1)
    html = html_esle(html, es)
    # sayfa içi <style> blokları da eşlensin (gömülen CSS zaten eşlendi; diğerleri burada)
    html = re.sub(r"(<style>)(?!/\* )(.*?)(</style>)", lambda m: m.group(1) + css_esle(m.group(2), es) + m.group(3), html, flags=re.S)
    if TEMALAR[ad]["sahne"] == "gece":     # levhadaki gün saati sahneyle uyuşsun
        html = re.sub(r'(<div class="ust">[^<]*?) · (sabah|öğle|akşam|ikindi)</div>', r'\1 · gece</div>', html)
    return re.sub(r"<html([^>]*)>", lambda m: f'<html{m.group(1)} data-tema="{ad}">', html, count=1)
