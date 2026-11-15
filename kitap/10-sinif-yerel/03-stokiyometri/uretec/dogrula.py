"""Stokiyometri · Dicle Yolu · sayısal doğrulama ve cevap anahtarı denetimi.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı (önce python3 uretec/kur.py).
  1. Denklemler: açık listedeki ve SAYFADAN toplanan her denklemde atomlar denk mi, katsayılar en küçük tam sayı mı?
  2. Her görev, tuzak, hızlı görev, meclis, kıssa, merdiven, imtihan ve üstad sorusu burada YENİDEN hesaplanır;
     sonuç sayfanın düz metninde aranır (sayfada).
  3. Çoktan seçmeli sorularda şıklar SAYFADAN okunur ve TEK doğru şık aranır (tek_sik).
  4. data-soru / data-dogru işaretleri, anahtar ızgarası, Cevaplar satırları, meclis hükümleri, öğretmen metinleri.
  5. Akçe: sayfa çiplerinden durak toplamları, yan yollar, 1400; akçe defteri; HUD çubuğu; unvan sınırları; meta.json.
Grafik verileri sahneler_unite.py'den okunur (MOL_ZAMAN, USTAD_GRAFIK): çizim ile hesap aynı sayıyı kullanır.
"""
import ast
import html as HT
import itertools
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr


def _ortak():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


URETEC = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_ortak(), URETEC]
import dogrula_ortak as DO  # noqa: E402
from dogrula_ortak import *  # noqa: E402,F401,F403
import sahneler_unite as SU  # noqa: E402

META = json.load(open(os.path.join(URETEC, "meta.json"), encoding="utf-8"))
SABLON = open(os.path.join(URETEC, "sablon.html"), encoding="utf-8").read()
SAYFA = sayfa_oku(__file__)
if SAYFA is None:
    kontrol("unite.html var (önce python3 uretec/kur.py)", False)
    D.sonuc()


# ------------------------------------------------------------------ yardımcılar

def duz(h):
    """HTML → düz metin: SVG atılır; O<sub>2</sub> → O2, 10<sup>23</sup> → 10^23, <sup>13</sup>/<sub>2</sub> → 13/2."""
    h = re.sub(r"<(svg|style|script)\b.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<sup>(\d+)</sup>/<sub>(\d+)</sub>", r"\1/\2", h)
    h = re.sub(r"<sub>([^<]*)</sub>", r"\1", h)
    h = re.sub(r"<sup>([^<]*)</sup>", r"^\1", h)
    h = re.sub(r"</?(b|i|em|u|strong|small|s)\b[^>]*>", "", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = HT.unescape(h).replace("\xa0", " ")
    return re.sub(r"\s+", " ", h)


def tr(x, n=None):
    """Türkçe sayı yazımı: 12.8 → '12,8' · 24.0 → '24' · tr(1, 1) → '1,0'."""
    s = f"{x:.{n}f}" if n is not None else f"{round(float(x), 6):.6f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def sayi(m):
    """Şık metninden sayı: '24,0' → 24.0 · '1,806·10^23' → 1.806e23."""
    g = re.fullmatch(r"(\d+(?:,\d+)?)(?:·10\^(\d+))?", m.replace(" ", ""))
    return float(g.group(1).replace(",", ".")) * (10 ** int(g.group(2)) if g.group(2) else 1) if g else None


def kume(m):
    """Yargı şıkkı: 'I, II ve III' → {'I','II','III'} · '1 ve 3' → {'1','3'}."""
    return frozenset(re.findall(r"\b(III|II|I|[1-3])\b", m))


BOLUM = {int(n): b for n, b in re.findall(r'<section class="sayfa s(\d+)[^"]*">(.*?)</section>', SAYFA, re.S)}
SBOLUM = {int(n): b for n, b in re.findall(r'<section class="sayfa s(\d+)[^"]*">(.*?)</section>', SABLON, re.S)}
DUZ = {n: duz(b) for n, b in BOLUM.items()}
BLOK = dict(DO._bloklar(SAYFA))
kontrol(f"16 sayfa (unite.html {len(BOLUM)}, şablon {len(SBOLUM)}, meta {META['sayfa_sayisi']})",
        len(BOLUM) == len(SBOLUM) == META["sayfa_sayisi"] == 16)


def sayfada(n, *parcalar):
    for p in parcalar:
        kontrol(f"s{n}: “{p}”", p in DUZ[n])


def siklar(kod):
    """{harf: düz metin} — data-soru="kod" kartındaki şıklar (sayfadan)."""
    return {h: duz(m).replace("%__", "").strip()
            for h, m in re.findall(r'<div(?: class="(?:sik|tam)")?(?: data-dogru)?><b>([A-E])</b>(.*?)</div>', BLOK[kod], re.S)}


def sayisal(kod, deger, beklenen, t=1e-9):
    s = siklar(kod)
    return tek_sik(f"{kod}: {tr(deger)}", {h: sayi(v) for h, v in s.items()}, lambda v: v is not None and yakin(v, deger, t), beklenen)


def yargili(kod, dogrular, beklenen):
    s = siklar(kod)
    return tek_sik(f"{kod}: doğru yargılar {sorted(dogrular)}", {h: kume(v) for h, v in s.items()}, lambda v: v == frozenset(dogrular), beklenen)


# ------------------------------------------------------------------ 1. denklemler

def denklem(s):
    """'2C4H10 + 13O2 → 8CO2 + 10H2O' → (sol, sag): [(katsayı, {element: sayı}), …]."""
    def terim(t):
        m = re.fullmatch(r"(\d+(?:/\d+)?)?\s?(\S+)", t.strip())
        return (Fr(m.group(1)) if m.group(1) else Fr(1)), formul(m.group(2))
    sol, sag = s.split("→")
    return [terim(t) for t in sol.split("+")], [terim(t) for t in sag.split("+")]


def say(taraf):
    c = {}
    for k, d in taraf:
        for el, n in d.items():
            c[el] = c.get(el, 0) + k * n
    return c


def denk_mi(s):
    sol, sag = denklem(s)
    return say(sol) == say(sag)


def en_kucuk(s):
    ks = [k for k, _ in sum(denklem(s), [])]
    return all(k.denominator == 1 for k in ks) and math.gcd(*[int(k) for k in ks]) == 1


def denklestir(sol, sag, ust=15):
    """En küçük tam sayı katsayılar (kaba arama): denklestir(['C3H8','O2'], ['CO2','H2O']) → (1, 5, 3, 4)."""
    tum = [formul(x) for x in sol + sag]
    el = sorted({e for d in tum for e in d})
    for top in range(len(tum), ust * len(tum) + 1):
        for ks in itertools.product(range(1, ust + 1), repeat=len(tum)):
            if sum(ks) != top or math.gcd(*ks) != 1:
                continue
            if all(sum(k * d.get(e, 0) for k, d in zip(ks[:len(sol)], tum[:len(sol)]))
                   == sum(k * d.get(e, 0) for k, d in zip(ks[len(sol):], tum[len(sol):])) for e in el):
                return ks
    return None


DENKLEMLER = [  # sayfada geçen, denk ve en küçük tam sayılı olması gereken denklemler
    "2Cu + O2 → 2CuO", "2H2 + O2 → 2H2O", "6CO2 + 6H2O → C6H12O6 + 6O2", "C3H8 + 5O2 → 3CO2 + 4H2O",
    "2C4H10 + 13O2 → 8CO2 + 10H2O", "C2H6O + 3O2 → 2CO2 + 3H2O", "4Fe + 3O2 → 2Fe2O3", "N2 + 3H2 → 2NH3",
    "CH4 + 2O2 → CO2 + 2H2O", "C + O2 → CO2", "CaCO3 → CaO + CO2", "CaCO3 + 2HCl → CaCl2 + H2O + CO2",
    "Zn + 2HCl → ZnCl2 + H2", "Cu2(OH)2CO3 → 2CuO + CO2 + H2O", "2CuO + C → 2Cu + CO2", "2Al + 3Cl2 → 2AlCl3",
    "Al(OH)3 + 3HCl → AlCl3 + 3H2O", "Mg + 2HCl → MgCl2 + H2", "2NaHCO3 → Na2CO3 + H2O + CO2",
    "2C3H6 + 9O2 → 6CO2 + 6H2O", "2Cu + S → Cu2S", "CO2 + Ca(OH)2 → CaCO3 + H2O", "Fe + S → FeS",
    "2Fe2O3 + 3C → 4Fe + 3CO2", "2Cu2S + 3O2 → 2Cu2O + 2SO2", "Cu2S + 2Cu2O → 6Cu + SO2", "SnO2 + 2C → Sn + 2CO",
    "2Mg + O2 → 2MgO", "Fe2O3 + 3CO → 2Fe + 3CO2", "2Al + 6HCl → 2AlCl3 + 3H2", "2C2H6 + 7O2 → 4CO2 + 6H2O",
]
for d in DENKLEMLER:
    kontrol(f"denk ve en küçük tam sayılı: {d}", denk_mi(d) and en_kucuk(d))

# Sayfadan toplanan denklemler (SVG dışı bütün metin). Kasıtlı denk olmayanlar: denkleştirilecek sorular ve meclis hatası.
KASITLI = {"C3H8+O2→CO2+H2O", "C4H10+O2→CO2+H2O", "Fe+O2→Fe2O3", "C4H10+13O2→4CO2+5H2O"}
ELEMENT = set(M) | {"Sn"}
_T = r"(?:\d+(?:/\d+)?\s?)?(?:[A-Z][a-z]?\d*|\((?:[A-Z][a-z]?\d*)+\)\d*)+"
_ZINCIR = re.compile(rf"(?<![A-Za-z0-9çğıöşüÇĞİÖŞÜ]){_T}(?:\s?\+\s?{_T})*(?:\s?→\s?{_T}(?:\s?\+\s?{_T})*)+(?![a-zçğıöşü])")
metin = re.sub(r"\((?:k|s|g|suda)\)", "", " ".join(DUZ.values()))
bulunan, bilinmeyenli = set(), set()
for z in _ZINCIR.finditer(metin):
    parca = z.group(0).split("→")
    for sol, sag in zip(parca, parca[1:]):
        d = f"{sol.strip()} → {sag.strip()}"
        if d.count("+") + 2 < 3:   # tek terim → tek terim: "C → 3CO2" gibi sayım notu, denklem değil
            continue
        try:
            els = {e for _, x in sum(denklem(d), []) for e in x}
        except (ValueError, AttributeError):
            continue
        if els & {"X", "Y", "Z"}:
            bilinmeyenli.add(d)
            continue
        if not els <= ELEMENT:
            continue
        bulunan.add(d)
for d in sorted(bulunan):
    a = d.replace(" ", "")
    if a in KASITLI:
        kontrol(f"sayfada kasıtlı denk olmayan (soru/meclis hatası): {d}", not denk_mi(d))
    else:
        kesirli = any(k.denominator != 1 for k, _ in sum(denklem(d), []))
        kontrol(f"sayfada denk{'' if kesirli else ' ve en küçük tam sayılı'}: {d}", denk_mi(d) and (kesirli or en_kucuk(d)))
kontrol(f"sayfadan {len(bulunan)} denklem toplandı; açık listedekiler sayfada",
        {x.replace(" ", "") for x in bulunan} >= {x.replace(" ", "") for x in DENKLEMLER if not x.startswith(("SnO2", "2C2H6", "C2H6O"))})
kontrol(f"bilinmeyenli denklemler {sorted(bilinmeyenli)}",
        {x.replace(" ", "") for x in bilinmeyenli} == {"X+3O2→2CO2+3H2O", "2X+9O2→6CO2+6H2O", "XO2+2C→X+2CO", "X+2Y→Z"})


def bilinmeyen(denk, katsayi_x=1):
    """'X + 3O2 → 2CO2 + 3H2O' → X'in formülü {element: sayı} (ürünler − diğer tepkenler, X'in katsayısına bölünmüş)."""
    sol, sag = denklem(denk.replace("X", "Xx"))   # Xx: formul() için geçici element
    fark = say(sag)
    for k, d in sol:
        if "Xx" not in d:
            for e, n in d.items():
                fark[e] = fark.get(e, 0) - k * n
    return {e: n / katsayi_x for e, n in fark.items() if n}


# ------------------------------------------------------------------ 2. duraklar

# s2 · Çayönü · korunum
o2 = 16.0 - 12.8
kontrol("G1: 12,8 g Cu = 0,2 mol → 0,2 mol CuO = 16,0 g; O2 0,1 mol = 3,2 g",
        yakin(12.8 / M["Cu"], .2) and yakin(.2 * mk("CuO"), 16) and yakin(.1 * mk("O2"), o2))
sayfada(2, f"m(O2) = 16,0 − 12,8 = {tr(o2)} g", "0,2 mol Cu → 0,2 mol CuO = 16 g", f"{tr(o2)} g O2 · toplam kütle değişmez")
kontrol("korunum şeması: 12,8 + 3,2 = 16,0 g (iki terazide)", SU.korunum_semasi("t").count(">16,0 g<") == 2 and yakin(12.8 + o2, 16))
sol, _ = denklem("2H2 + O2 → 2H2O")
sayfada(2, f"{int(sum(k * sum(d.values()) for k, d in sol))} atom")
nh2, no2 = 4 / mk("H2"), 32 / mk("O2")
su = min(nh2 / 2, no2) * 2 * mk("H2O")
kontrol("hızlı görev: 2 mol H2 + 1 mol O2 artansız; molekül 3 → 2 (korunmaz)", yakin(nh2 / 2, no2) and 2 + 1 != 2)
sayfada(2, f"{tr(su)} g su; hayır")

# s3 · Hevsel · denkleştirme
kontrol("fotosentez iki yakada 6 C, 12 H, 18 O", say(denklem("6CO2 + 6H2O → C6H12O6 + 6O2")[0]) == {"C": 6, "H": 12, "O": 18})
sayfada(3, "6 C, 12 H, 18 O", "2 Al, 3 S, 12 O")
kontrol("Al2(SO4)3: 2 Al, 3 S, 12 O", formul("Al2(SO4)3") == {"Al": 2, "S": 3, "O": 12})
kontrol("G2-A denkleştirme (1, 5, 3, 4)", denklestir(["C3H8", "O2"], ["CO2", "H2O"]) == (1, 5, 3, 4))
kontrol("G2-B denkleştirme (2, 13, 8, 10); 1 C4H10 için O: 8 + 5 = 13 → 13/2 O2",
        denklestir(["C4H10", "O2"], ["CO2", "H2O"]) == (2, 13, 8, 10) and 4 * 2 + 5 == 13)
sayfada(3, "Sağda O: 6 + 4 = 10 → 5O2", "C3H8 + 5O2 → 3CO2 + 4H2O", "8 + 5 = 13 → 13/2 O2", "2C4H10 + 13O2 → 8CO2 + 10H2O")
x3 = bilinmeyen("X + 3O2 → 2CO2 + 3H2O")
kontrol(f"G3: X = C2H6O {x3}", x3 == formul("C2H6O"))
sayfada(3, "X = C2H6O", "C 2 0 2 H 6 0 6 O 7 6 1", "2 C, 6 H, 4 + 3 = 7 O")
fe = denklestir(["Fe", "O2"], ["Fe2O3"])
kontrol(f"hızlı görev: 4Fe + 3O2 → 2Fe2O3 {fe}, toplam 9", fe == (4, 3, 2) and sum(fe) == 9)
sayfada(3, f"4Fe + 3O2 → 2Fe2O3 · {sum(fe)}", f"Cevap: {sum(fe)}", "2Fe2O3 ile başla: 4 Fe, 6 O.")

# s4 · Malabadi · denklemden hesaba
k = [1 * mk("N2"), 3 * mk("H2"), 2 * mk("NH3")]
kontrol("N2 + 3H2 → 2NH3 kütleleri 28 : 6 : 34", k == [28, 6, 34] and k[0] + k[1] == k[2])
sayfada(4, "kütle 28 : 6 : 34", "28 + 6 = 34", "28 g 6 g 34 g katsayı değil")
n = 4.8 / mk("CH4")
o2, co2, su = 2 * n * mk("O2"), n * mk("CO2"), 2 * n * mk("H2O")
kontrol("G4: 0,3 mol CH4 → 19,2 g O2, 13,2 g CO2, 10,8 g su; kütle korunur",
        yakin(n, .3) and yakin(o2, 19.2) and yakin(co2, 13.2) and yakin(su, 10.8) and yakin(4.8 + o2, co2 + su))
sayfada(4, "0,3 mol CH4 → H5: 0,6 mol O2, 0,3 mol CO2", f"{tr(o2)} g O2; {tr(co2)} g CO2 (kontrol: 4,8 + {tr(o2)} = {tr(co2)} + {tr(su)})")
n = 6.8 / mk("NH3")
h2, n2 = n * 3 / 2, n / 2
kontrol("G5: 0,4 mol NH3 → 0,6 mol H2 = 1,2 g; 0,2 mol N2 = 1,204·10^23", yakin(h2 * mk("H2"), 1.2) and yakin(n2 * NA, 1.204e23))
sayfada(4, "0,4 mol NH3 → H2 0,4·3/2 = 0,6 mol = 1,2 g", "1,2 g H2 · 1,204·10^23 N2")
sayfada(4, f"2 mol H2 ({tr(2 * mk('H2'))} g), 1 mol O2 ({tr(mk('O2'))} g)")
co2 = 6 / M["C"] * mk("CO2")
sayfada(4, f"{tr(co2)} g CO2", f"Cevap: {tr(co2)} g")

# s5 · Batman · sınırlayıcı bileşen
kontrol("Pamuk: 10 kaşık/2 = 5 < 7 kâse/1 → 5 öğün, mama biter", min(10 / 2, 7 / 1) == 5 and 10 / 2 < 7)
sayfada(5, "10 kaşık, 7 kâse → 5 öğün", "4/2 = 2 < 3/1 = 3")
kontrol("tanecik şeması: 4 H2 + 3 O2 → 4 H2O, 1 O2 artar", 4 / 2 < 3 / 1 and 3 - 4 / 2 == 1)
mz = {ad: (a, b) for ad, a, b in SU.MOL_ZAMAN["durak"]}
dX, dY, dZ = (mz[x][1] - mz[x][0] for x in "XYZ")
g = math.gcd(abs(dX), abs(dY), abs(dZ))
kontrol(f"G6 grafiği: X {dX}, Y {dY}, Z +{dZ} → 1 : 2 : 1; Y biter, X'ten 1 mol artar",
        (-dX // g, -dY // g, dZ // g) == (1, 2, 1) and mz["Y"][1] == 0 and mz["X"][1] == 1)
sayfada(5, f"X {dX:+d}, Y {dY:+d}, Z {dZ:+d} → 1 : 2 : 1".replace("-", "−"), "X + 2Y → Z · 1 mol X artar")
ch4, o2 = 9.6 / mk("CH4"), 32 / mk("O2")
sin = "O2" if o2 / 2 < ch4 / 1 else "CH4"
harc = o2 / 2
art = ch4 - harc
kontrol("G7: CH4 0,6 · O2 1,0 → O2 sınırlayıcı; 0,1 mol (1,6 g) CH4 artar; 22 g CO2; kütle 41,6 = 22 + 18 + 1,6",
        sin == "O2" and yakin(art, .1) and yakin(art * 16, 1.6) and yakin(harc * 44, 22) and yakin(9.6 + 32, 22 + 18 + 1.6))
sayfada(5, f"CH4 {tr(ch4, 1)} mol; O2 {tr(o2, 1)} mol", f"Artan CH4 {tr(art)} mol = {tr(art * 16)} g · CO2 {tr(harc)} mol = {tr(harc * 44)} g",
        f"Kontrol: 9,6 + 32 = {tr(9.6 + 32)} = {tr(harc * 44)} + {tr(o2 * 18)} + {tr(art * 16)}",
        "B 0,6 1,0 0 0 D −0,5 −1,0 +0,5 +1,0 S 0,1 0 0,5 1,0", "1,6 g CH4 artar · 22 g CO2")
kontrol("tuzak: 3 mol H2 / 2 = 1,5 < 2 mol O2 / 1 → H2 biter", 3 / 2 < 2 / 1)
sayfada(5, "3/2 = 1,5 < O2 2/1 = 2")
sin = "O2" if 1.5 / 5 < .4 / 1 else "C3H8"
co2 = (1.5 / 5 if sin == "O2" else .4) * 3
sayfada(5, f"O2 · {tr(co2)} mol CO2")
kontrol("hızlı görev: O2 sınırlayıcı, 0,9 mol CO2", sin == "O2" and yakin(co2, .9))

# s6 · Hasankeyf · verim ve saflık
teo = 50 / mk("CaCO3") * mk("CaO")
verim = 22.4 / teo * 100
kontrol("G8: 50 g CaCO3 → teorik 28 g CaO; 22,4/28 = %80", yakin(teo, 28) and yakin(verim, 80))
sayfada(6, f"0,5 mol → teorik CaO {tr(teo)} g", f"%{tr(verim)} verim")
kontrol("G8 verim göstergesi şablonda %80", f"{{{{info|verim_saati|{tr(verim)}}}}}" in SBOLUM[6])
saf = 13.2 / mk("CO2") * mk("CaCO3")
kontrol("G9: 13,2 g CO2 = 0,3 mol → 30 g CaCO3 → %75", yakin(saf, 30) and yakin(saf / 40 * 100, 75))
sayfada(6, f"0,3 mol CO2 → 0,3 mol CaCO3 = {tr(saf)} g", f"%{tr(saf / 40 * 100)} saflık")
kontrol("saflık taşı çizimi %75 (çubuk 330/440)", ">%75 CaCO<" in SU.saflik_tasi("t") and yakin(330 / 440, .75))
caco3 = .4 / .80 * mk("CaCO3")
sayfada(6, f"{tr(caco3)} g CaCO3", f"Cevap: {tr(caco3)} g")
kontrol("hızlı görev: 0,4 / 0,80 = 0,5 mol → 50 g", yakin(caco3, 50))

# s7 · Bakırcılar · karışım ve zincir
x = Fr("0.5") * 4 - Fr("1.8")            # 3x + 4(0,5 − x) = 1,8 → x = 2 − 1,8
kontrol("G10: 3x + 4(0,5 − x) = 1,8 → x = 0,2", 3 * x + 4 * (Fr("0.5") - x) == Fr("1.8") and x == Fr("0.2"))
kutle = float(x) * mk("C3H8") + float(Fr("0.5") - x) * mk("C4H10")
sayfada(7, "x = 0,2", f"0,2 / 0,5 · 100 = %{tr(float(x) / .5 * 100)} propan", "0,2·44 + 0,3·58 = 8,8 + 17,4",
        f"%40 propan · {tr(kutle)} g karışım")
kontrol("G10: karışım 26,2 g", yakin(kutle, 26.2))
mal = mk("Cu2(OH)2CO3")
n = 44.4 / mal
cu, co2 = 2 * n, n + 2 * n / 2
kontrol("G11: malakit 222 g/mol; 0,2 mol → 0,4 mol CuO → 25,6 g Cu; CO2 0,2 + 0,2 = 0,4 mol",
        mal == 222 and yakin(n, .2) and yakin(cu * 64, 25.6) and yakin(co2, .4))
sayfada(7, f"MA = {mal} → 0,2 mol malakit → 0,4 mol CuO", f"{tr(cu * 64)} g Cu · {tr(co2)} mol CO2")
z = SU.bakir_zinciri("t")
kontrol("zincir çizimi: 0,2 → 0,4 → 0,4 mol", [m_ for m_ in re.findall(r">(0,\d) mol<", z)] == ["0,2", "0,4", "0,4"])
zn = .2 / mk("H2") * M["Zn"]
sayfada(7, f"%{tr(zn / 20 * 100)} Zn")
kontrol("hızlı görev: 0,1 mol Zn = 6,5 g → %32,5", yakin(zn / 20 * 100, 32.5))

# ------------------------------------------------------------------ 3. meclis (s9)
kontrol("M1: doğrusu 2C4H10 + 13O2 → 8CO2 + 10H2O; Ahmet'in 3. satırı denk değil (13 O2 = 26 O)",
        denklestir(["C4H10", "O2"], ["CO2", "H2O"]) == (2, 13, 8, 10) and not denk_mi("C4H10 + 13O2 → 4CO2 + 5H2O"))
h2 = 8.4 / mk("N2") * 3 * mk("H2")
kontrol("M2: 0,3 mol N2 → 0,9 mol = 1,8 g H2; Zehra 25,2 yanlış; Elif'in itirazı (toplama) yersiz",
        yakin(h2, 1.8) and not yakin(3 * 8.4, h2) and yakin(8.4 + 25.2, 33.6))
sin = "Cl2" if 3 / 3 < 3 / 2 else "Al"
alcl3 = 3 * 2 / 3
kontrol("M3: Cl2 sınırlayıcı → 2 mol AlCl3, 1 mol Al artar; Elif'in 1,5 iddiası yanlış",
        sin == "Cl2" and alcl3 == 2 and 3 - alcl3 == 1 and alcl3 != 1.5)
teo = 25 / mk("CaCO3") * mk("CaO")
kontrol("M4: teorik 14 g, gerçek 11,2 g; 14/0,80 = 17,5 > teorik (imkânsız); CaO 56 g/mol (Yusuf yanlış)",
        yakin(teo, 14) and yakin(teo * .8, 11.2) and 14 / .8 > teo and mk("CaO") == 56)
sayfada(9, "2C4H10 + 13O2 → 8CO2 + 10H2O", "0,3 mol N2 → 0,9 mol H2 = 1,8 g", "2 mol AlCl3; 1 mol Al artar", "14 · 0,80 = 11,2 g CaO")
MECLIS = {"M1": ("Yusuf", 2), "M2": ("Pamuk", 1), "M3": ("Yusuf", 2), "M4": ("Elif", 3)}
kontrol(f"meclis hükümleri sayfada {meclis_hukumleri(SAYFA)}", meclis_hukumleri(SAYFA) == MECLIS)
for kod in MECLIS:
    b = BLOK[kod]
    kontrol(f"{kod}: tek haklı yorum, tek satır kutucuğu, 2 öğretmen satırı",
            b.count('<div class="yorum" data-dogru>') == 1 and b.count('class="kutucuk" data-dogru') == 1 and b.count('class="ogr"') == 2)

# ------------------------------------------------------------------ 4. kıssalar (s10)
T = {}
n = .78 / mk("Al(OH)3")
T["K1"] = yargili("K1", yargi({"I": yakin(n, .01), "II": yakin(3 * n, .03), "III": yakin(3 * n * mk("H2O"), .54)}), "E")
mz = {ad: (a, b) for ad, a, b in SU.MOL_ZAMAN["kissa"]}
dn, dh, da = (abs(mz[x][1] - mz[x][0]) for x in ("N2", "H2", "NH3"))
biten = [x for x in ("N2", "H2") if mz[x][1] == 0]
T["K2"] = yargili("K2", yargi({"I": yakin(dh / dn, 3) and yakin(da / dn, 2), "II": biten == ["N2"],
                               "III": yakin(sum(a for a, _ in mz.values()), 2.2) and yakin(sum(b for _, b in mz.values()), 1.4)}), "D")
DENEME = [(.1, .1), (.1, .3), (.2, .3)]
sayfada(10, "1 0,1 0,1 2 0,1 0,3 3 0,2 0,3")
T["K3"] = yargili("K3", {str(i + 1) for i, (mg, hcl) in enumerate(DENEME) if hcl / 2 < mg / 1}, "C")
n = 8.4 / mk("NaHCO3")
kayip = 8.4 - n / 2 * mk("Na2CO3")
kontrol("K4: katı kaybı = uçan CO2 + H2O = 2,2 + 0,9", yakin(kayip, n / 2 * (mk("CO2") + mk("H2O"))) and yakin(kayip, 3.1))
T["K4"] = sayisal("K4", kayip, "B")

# ------------------------------------------------------------------ 5. anahtar merdiveni (s11)
m1 = denklestir(["C3H6", "O2"], ["CO2", "H2O"])
kontrol(f"Merdiven 1: {m1} → 23", m1 == (2, 9, 6, 6) and sum(m1) == 23)
cu, s_ = 12.8 / 64, 4.8 / 32
sin = "Cu" if cu / 2 < s_ / 1 else "S"
s_art = s_ - cu / 2
cu2s = cu / 2 * mk("Cu2S")
kontrol("Merdiven 2: Cu sınırlayıcı; 0,05 mol = 1,6 g S artar; 16 g Cu2S; 12,8 + 4,8 = 16 + 1,6",
        sin == "Cu" and yakin(s_art * 32, 1.6) and yakin(cu2s, 16) and yakin(12.8 + 4.8, cu2s + s_art * 32))
caco3 = 2.9 / mk("C4H10") * 4 * mk("CaCO3") * .80
kontrol("Merdiven 3: 0,05 mol bütan → 0,2 mol CO2 → teorik 20 g → %80: 16 g", yakin(caco3, 16))
sayfada(11, f"{sum(m1)}", f"0,05 mol = {tr(s_art * 32)} g artar", f"0,1 mol Cu2S = {tr(cu2s)} g", f"20 · 0,80 = {tr(caco3)} g CaCO3")
kontrol("merdivende 3 problem × 40 akçe", SBOLUM[11].count('<div class="kart merdiven">') == 3 and "Her problem +40 akçe" in SBOLUM[11])

# ------------------------------------------------------------------ 6. Büyük İmtihan (s12–s13)
KORUNUR = {"Toplam atom sayısı": True, "Toplam molekül sayısı": False, "Toplam mol sayısı": False,
           "Maddelerin fiziksel hâli": False, "Gazların toplam hacmi": False}
sol, sag = denklem("2H2 + O2 → 2H2O")
kontrol("I1: karşı örnek 2H2 + O2 → 2H2O: atom korunur, molekül/mol 3 → 2",
        say(sol) == say(sag) and sum(k for k, _ in sol) != sum(k for k, _ in sag))
kontrol(f"I1 şık metinleri tanıdık {sorted(siklar('I1').values())}", set(siklar("I1").values()) == set(KORUNUR))
T["I1"] = tek_sik("I1: kesinlikle korunan", {h: KORUNUR.get(v) for h, v in siklar("I1").items()}, lambda v: v is True, "A")
s_ = 8.8 - 5.6
kontrol("I2: 0,1 mol Fe + 0,1 mol S → 0,1 mol FeS = 8,8 g", yakin(5.6 / 56 * mk("FeS"), 8.8) and yakin(s_ / 32, .1))
T["I2"] = sayisal("I2", s_, "B")
T["I3"] = sayisal("I3", sum(denklestir(["Fe2O3", "C"], ["Fe", "CO2"])), "E")
x4 = bilinmeyen("2X + 9O2 → 6CO2 + 6H2O", 2)
T["I4"] = tek_sik(f"I4: X = {x4}", {h: formul(v) for h, v in siklar("I4").items()}, lambda v: v == x4, "A")
T["I5"] = sayisal("I5", 6.6 / mk("C3H8") * 5 * mk("O2"), "C")
T["I6"] = sayisal("I6", 3.4 / mk("NH3") * 3 / 2 * NA, "D")
al, cl2 = .6, .6
sin = "Cl2" if cl2 / 3 < al / 2 else "Al"
alcl3 = (cl2 / 3 if sin == "Cl2" else al / 2) * 2
al_art = al - alcl3 if sin == "Cl2" else 0
cl2_art = cl2 - alcl3 * 3 / 2 if sin == "Al" else 0
I7 = {"Sınırlayıcı bileşen Al’dir.": sin == "Al", "0,2 mol Al artar.": yakin(al_art, .2), "0,6 mol AlCl3 oluşur.": yakin(alcl3, .6),
      "Cl2’den 0,2 mol artar.": yakin(cl2_art, .2), "0,3 mol AlCl3 oluşur.": yakin(alcl3, .3)}
kontrol(f"I7 şık metinleri tanıdık {sorted(siklar('I7').values())}", set(siklar("I7").values()) == set(I7))
T["I7"] = tek_sik("I7: doğru ifade", {h: I7.get(v) for h, v in siklar("I7").items()}, lambda v: v is True, "B")
h2, o2 = 4 / mk("H2"), 40 / mk("O2")
artan = ("O2", (o2 - h2 / 2) * mk("O2")) if h2 / 2 < o2 else ("H2", (h2 - 2 * o2) * mk("H2"))


def _madde(v):
    m_ = re.fullmatch(r"(\S+) – (\d+) g", v)
    return (m_.group(1), float(m_.group(2))) if m_ else None


T["I8"] = tek_sik(f"I8: artan {artan}", {h: _madde(v) for h, v in siklar("I8").items()},
                  lambda v: v is not None and v[0] == artan[0] and yakin(v[1], artan[1]), "E")
T["I9"] = sayisal("I9", 4.08 / (5.6 / mk("N2") * 2 * mk("NH3")) * 100, "C")
T["I10"] = sayisal("I10", 75 * .80 / mk("CaCO3") * mk("CO2"), "D")
x = (3 * .3 - .8) / (3 - 2)                 # 2x + 3(0,3 − x) = 0,8
T["I11"] = sayisal("I11", x * mk("C2H6") + (.3 - x) * mk("C3H8"), "B")
kontrol("I12: iki adımın toplamı Cu2S + O2 → 2Cu + SO2 (Cu atomu korunur)",
        denk_mi("3Cu2S + 3O2 → 6Cu + 3SO2") and denk_mi("Cu2S + O2 → 2Cu + SO2"))
T["I12"] = sayisal("I12", 48 / mk("Cu2S") * 2 * M["Cu"], "D")

# ------------------------------------------------------------------ 7. Üstad (s14)
xo2 = 30.2 / (11.2 / mk("CO") / 2)
T["U1"] = sayisal("U1", xo2 - 2 * M["O"], "E")
kontrol("U1: X = 119 g/mol (kalay, Sn)", yakin(xo2 - 32, M["Sn"]))
m_ = Fr(14) / (1 - Fr(1, 8))                 # eşit kütle m: O2 m/32 mol biter, H2 m/16 mol (m/8 g) harcanır → kalan 7m/8 g
kontrol("U2: O2 sınırlayıcı (m/32 < m/2 ÷ 2); kalan H2 7m/8 = 14 → m = 16", Fr(1, 32) < Fr(1, 2) / 2 and m_ == 16)
T["U2"] = sayisal("U2", float(2 * m_), "B")
(mg_k, mgo_k), mg_son = SU.USTAD_GRAFIK["kirilma"], SU.USTAD_GRAFIK["mg_son"]
o2 = mgo_k / mk("MgO") / 2
kontrol("U3 grafiği: kırılmada 9,6 g Mg → 16 g MgO", yakin(mg_k / M["Mg"] * mk("MgO"), mgo_k))
mg_fazla = mg_son / M["Mg"] - 2 * o2
T["U3"] = yargili("U3", yargi({"I": yakin(mg_k / M["Mg"] / 2, o2), "II": False if mg_fazla > 0 else True, "III": yakin(o2 * 32, 6.4)}), "D")
kontrol("U3: 14,4 g'da artan Mg (4,8 g), O2 değil", yakin(mg_fazla * M["Mg"], 4.8))
T["U4"] = sayisal("U4", 48 / mk("Fe2O3") * 3 * .80 * mk("CaCO3"), "C")
y = (18 - 24 * .9) / (27 - 24 * 1.5)        # x + 1,5y = 0,9 ; 24x + 27y = 18
x = .9 - 1.5 * y
kontrol("U5: x = 0,3 mol Mg, y = 0,4 mol Al", yakin(x, .3) and yakin(y, .4) and yakin(24 * x + 27 * y, 18))
T["U5"] = sayisal("U5", 24 * x / 18 * 100, "A")
n2, h2 = 14 / mk("N2"), 4 / mk("H2")
sin = "N2" if n2 / 1 < h2 / 3 else "H2"
harc = (n2 if sin == "N2" else h2 / 3) * .50
T["U6"] = sayisal("U6", (n2 - harc) + (h2 - 3 * harc) + 2 * harc, "D")
kontrol("U6: N2 sınırlayıcı", sin == "N2")

# ------------------------------------------------------------------ 8. sayfadaki işaretler, anahtar, çözümler
IMTIHAN, KISSA, USTAD = "ABEACDBECDBD", "EDCB", "EBDCAD"
BEKLENEN = {f"I{i + 1}": h for i, h in enumerate(IMTIHAN)}
BEKLENEN.update({f"K{i + 1}": h for i, h in enumerate(KISSA)})
BEKLENEN.update({f"U{i + 1}": h for i, h in enumerate(USTAD)})
kontrol(f"hesaplanan anahtar = beklenen ({''.join(str(T.get(f'I{i}')) for i in range(1, 13))})", T == BEKLENEN)
dagilim([T[f"I{i}"] for i in range(1, 13)])
dagilim([T[f"U{i}"] for i in range(1, 7)])
sayfa_isaretleri_ayni(SAYFA, T)
kontrol(f"data-soru kodları tam ve benzersiz {sorted(BLOK)}",
        sorted(re.findall(r'data-soru="([^"]+)"', SAYFA)) == sorted(list(BEKLENEN) + list(MECLIS)))
izgara = anahtar_izgarasi(SAYFA)
kontrol(f"Cevaplar: anahtar ızgarası {izgara}", izgara == {i: T[f"I{i}"] for i in range(1, 13)})
etiket = dict((int(a), int(b)) for a, b in re.findall(r"<i>(\d+)</i><b>[A-E]</b><small>(\d)\. durak</small>", BOLUM[15]))
kontrol("Cevaplar: soru i'nin durak etiketi (i + 1) // 2", etiket == {i: (i + 1) // 2 for i in range(1, 13)})
grup = dict(re.findall(r'<div class="grup"><h4>(.*?)</h4>(.*?)</div>', BOLUM[15], re.S))
for ad, onek, n in (("Büyük İmtihan", "I", 12), ("Kıssalar", "K", 4), ("Üstad soruları", "U", 6)):
    satir = dict((f"{onek}{a}", b) for a, b in re.findall(r"<b>(\d+) · ([A-E])</b>", grup.get(ad, "")))
    kontrol(f"Cevaplar · {ad}: çözüm satırları anahtarla aynı", satir == {f"{onek}{i}": T[f"{onek}{i}"] for i in range(1, n + 1)})
kisa = re.findall(r'<span class="ck">(\d) ([A-E])</span>', grup.get("Hızlı görevler · kısa anahtar", ""))
kontrol(f"Cevaplar · kısa kıssa anahtarı {kisa}", dict((f"K{a}", b) for a, b in kisa) == {k: T[k] for k in ("K1", "K2", "K3", "K4")})
meclis_c = dict(re.findall(r"<b>(M\d) · (\w+)</b> Satır (\d)", BOLUM[15]))
kontrol(f"Cevaplar · meclis satırları {meclis_c}", {k: v for k, v in meclis_c.items()} == {k: v[0] for k, v in MECLIS.items()})
sayfada(15, "1 · 23", "2 · 1,6 g S artar, 16 g Cu2S", "3 · 16 g CaCO3", "1 · 36 g, hayır", "2 · 9", "3 · 22 g",
        "4 · O2; 0,9 mol", "5 · 50 g", "6 · %32,5", "3,2 g S", "= 12", "C3H6", "= 24 g", "1,806·10^23", "8 g artar", "%60",
        "26,4 g CO2", "11,8 g", "38,4 g", "3,1 g", "X = 119", "toplam 32 g", "72 g CaCO3", "%40 Mg", "2,0 mol", "11,2 g CaO")
ogr = ogretmen_metinleri(SAYFA)
for ad, sinif in (("karalama", "karalama"), ("cevap kutusu", "cevap-kutu"), ("merdiven çözümü", "cozum-alani")):
    bloklar = re.findall(rf'<div class="{sinif}">(.*?)</div>\s*(?:</div>|<div)', SAYFA, re.S)
    kontrol(f"her {ad} öğretmen metni taşıyor ({len(bloklar)})", bloklar and all('class="ogr"' in b for b in bloklar))
kontrol(f"öğretmen metinleri boş değil ({len(ogr)})", len(ogr) >= 40 and all(o.strip() for o in ogr))
for r in re.findall(r"s\.\{\{sayfa\|(\d+)\}\}", SABLON):
    kontrol(f"sayfa göndermesi s.{{{{sayfa|{r}}}}} 1–16 içinde", 1 <= int(r) <= 16)

# ------------------------------------------------------------------ 9. akçe
HAZINE = {h["kod"]: h for h in META["hazine"]}


def cipler(b):
    b = re.sub(r'<div class="hedef">.*?</div>', "", b, flags=re.S)
    return [int(v) for v in re.findall(r'<span class="cip akce">\+(\d+)(?: akçe)?</span>', b)]


akce = {}
for d in META["duraklar"]:
    p = d["sayfa"]
    kartlar = re.findall(r"\{\{hazine\|(H\d+)\}\}", SBOLUM[p])
    hz = sum(int(re.search(r"\+(\d+) akçe", HAZINE[k]["baslik"]).group(1)) for k in kartlar)
    hedef = int(re.search(r'<div class="hedef">.*?<span class="cip akce">\+(\d+) akçe</span>', SBOLUM[p], re.S).group(1))
    akce[p] = sum(cipler(SBOLUM[p])) + hz
    kontrol(f"s{p} {d['yer']}: çipler {cipler(SBOLUM[p])} + hazine {kartlar} = {akce[p]} = hedef {hedef} = meta {d['akce']}",
            akce[p] == hedef == d["akce"])
    kontrol(f"s{p}: hazine kartları bu durağın ({[HAZINE[k]['durak'] for k in kartlar]})",
            len(kartlar) == 2 and all(HAZINE[k]["durak"] == d["no"] for k in kartlar))
mh = re.search(r"(\d) satır = \+(\d+) akçe", SBOLUM[8])
kontrol("s8 Hülasa: 6 muhasebe satırı = +40 akçe",
        mh and int(mh.group(1)) == SBOLUM[8].count('<div class="satir"><span>') == 6 and int(mh.group(2)) == 40)
akce[8] = int(mh.group(2))
for p, adet, birim in ((9, 4, 30), (10, 4, 30)):
    kontrol(f"s{p}: {adet} × +{birim} çip = hedef {adet} × {birim} = +{adet * birim} akçe",
            cipler(SBOLUM[p]) == [birim] * adet and f"{adet} × {birim} = +{adet * birim} akçe" in SBOLUM[p])
    akce[p] = adet * birim
kontrol("s11: hedef 3 × 40 = +120 akçe", "3 × 40 = +120 akçe" in SBOLUM[11])
akce[11] = 120
for p in (12, 13):
    kontrol(f"s{p}: 6 × +25 imtihan çipi", cipler(SBOLUM[p]) == [25] * 6)
    akce[p] = 150
toplam = sum(akce.values())
kontrol(f"ünite toplam akçe {toplam} = meta {META['akce_toplam']} = 1400", toplam == META["akce_toplam"] == 1400)
defter = [int(v) for v in re.findall(r'<td class="n">(\d+)</td>', SBOLUM[16])]
kontrol(f"akçe defteri {defter}", defter == [akce[p] for p in range(2, 12)] + [akce[12] + akce[13], 1400])
sayfada(16, "0–399 akçe", "400–799 akçe", "800–1149 akçe", "1150–1400 akçe")
kur = ast.parse(open(os.path.join(URETEC, "kur.py"), encoding="utf-8").read())
KSAYFA = next(ast.literal_eval(n.value) for n in kur.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SAYFA")
once = 0
for p in range(1, 17):
    kontrol(f"s{p}: HUD çubuğu %{KSAYFA[p][2]} = önceki sayfalarda alınabilecek {once}/1400", KSAYFA[p][2] == round(100 * once / 1400))
    once += akce.get(p, 0)

# ------------------------------------------------------------------ 10. meta.json tutarlılığı
kontrol("6 durak, sayfa 2–7, no 1–6", [(d["no"], d["sayfa"]) for d in META["duraklar"]] == [(i, i + 1) for i in range(1, 7)])
kontrol("8 nişan (6 durak + Sur Kapısı + bonus Üstad Mührü)",
        len(META["nisanlar"]) == 8 and [n_.get("bonus", False) for n_ in META["nisanlar"]] == [False] * 7 + [True])
kontrol("12 hazine kartı, her durağa 2", sorted(h["durak"] for h in META["hazine"]) == sorted(list(range(1, 7)) * 2))
for md in META["medeniyet"]:
    kutu = re.findall(r'<div class="medeniyet">(.*?)</p>\s*</div>', SBOLUM[md["sayfa"]], re.S)
    kontrol(f"Medeniyetimizden · {md['ad']} ({md['yil']}) s{md['sayfa']}'de", any(md["ad"] in k_ and md["yil"] in k_ for k_ in kutu))
for p, (hud, _, _) in KSAYFA.items():
    ad = re.sub(r"<[^>]+>", "", hud)
    kontrol(f"s{p}: HUD “{ad}” sayfada", ad in DUZ[p])

D.sonuc()
