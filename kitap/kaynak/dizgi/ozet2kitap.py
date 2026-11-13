"""Geniş Özet satır dosyalarını (ozet/*.txt) kitap satır biçimine birleştirir.

Kullanım: python3 -I ozet2kitap.py <kök> <çıktı_klasörü>
  <kök>: ozet/, bolumler/ (chapters/), on-arka/ (front/) ve arapca/ (ar/) klasörlerini içeren klasör
Çıktı: kitap.txt (kitap_build.js "kitap" modu için) ve boş dipnotlar.txt.
"""
import glob
import json
import os
import re
import sys

ROOT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
CH = "bolumler" if os.path.isdir(os.path.join(ROOT, "bolumler")) else "chapters"
FR = "on-arka" if os.path.isdir(os.path.join(ROOT, "on-arka")) else "front"
AR = os.path.join(ROOT, "arapca" if os.path.isdir(os.path.join(ROOT, "arapca")) else "ar")
OZ = os.path.join(ROOT, "ozet")


def load(name, default):
    p = os.path.join(AR, name)
    return json.load(open(p)) if os.path.exists(p) else default


QUOTES = {q["id"]: q for q in load("quotes.json", [])}
AYET, DIRECT, TRIM, WEB = load("ayet.json", {}), load("hadis_direct.json", {}), load("trim_result.json", {}), load("web_result.json", {})
KONU, SOZ, EXTRA = load("konu.json", {}), load("soz.json", {}), load("extra_hadis.json", {})
for qid, e in EXTRA.items():                    # siyer kaynaklarındaki Peygamber sözleri -> hadis kutusu
    if qid in QUOTES:
        QUOTES[qid]["kind"] = "hadis"
        if e.get("ar"):
            DIRECT[qid] = {"ar": e["ar"]}
        KONU.setdefault(qid, e["konu"])

# bölüm dipnot tanımları (alıntı kaynak satırındaki dipnotlar kutunun kaynak satırına eklenir)
FN = {}
for f in glob.glob(os.path.join(ROOT, CH, "ch*.md")) + glob.glob(os.path.join(ROOT, FR, "*.md")):
    for ln in open(f):
        m = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", ln)
        if m:
            FN[m.group(1)] = m.group(2).strip()

PARTS = {
    1: ("I. KISIM", "Nübüvvetin Arifesinde",
        "Bi'setten önceki dünya, Arap yarımadası, Fil Yılı ve Rasûlullah'ın (s.a.v.) doğumundan Hira'ya uzanan kırk yılı."),
    8: ("II. KISIM", "Mekke'de Davet",
        "İlk vahiyden Tâif dönüşüne: gizli ve açık davet, işkence, Habeşistan hicreti, boykot yılları ve İsrâ-Mi'râc."),
    16: ("III. KISIM", "Hicret", "Kabilelere arz, Akabe biatleri ve Mekke'den Medine'ye uzanan büyük yolculuk."),
    19: ("IV. KISIM", "Medine'de Devlet",
         "Mescid, kardeşlik ve Vesîka ile kurulan devlet; Bedir'in zaferi ve Uhud'un sınavı."),
}
NORMALIZE = (("Hristiyan", "Hıristiyan"), ("Vesikası", "Vesîkası"), ("Vesika ", "Vesîka "),
             ("Muhacirler", "Muhâcirler"), ("Muhacirlere", "Muhâcirlere"), ("Muhacirleri", "Muhâcirleri"),
             ("Mut'im b. Adî", "Mut'im b. Adiy"))
TAGS = {"H2", "INTRO", "B1", "B2", "QUOTE", "KAVRAM", "SOZ", "TABLE", "ROW", "ENDTABLE", "NOTE"}


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def clean(t):
    t = t.replace("\\'", "'").replace('\\"', '"').replace("\\*", "*")
    for a, b in NORMALIZE:
        t = t.replace(a, b)
    return t


def nopipe(t):
    return t.replace("|", "/")


def strip_fn(t):
    """Dipnot işaretlerini kaldırır; metinlerini döndürür."""
    notes = [FN[m] for m in re.findall(r"\[\^([^\]]+)\]", t) if m in FN]
    return re.sub(r"\s*\[\^[^\]]+\]", "", t).strip(), notes


missing_ar, used = [], []


def quote_line(qid):
    q = QUOTES[qid]
    used.append(qid)
    tr, n1 = strip_fn(clean(q["tr"]))
    src, n2 = strip_fn(clean(q["src"]))
    extra = " · ".join(n.rstrip(".") for n in n1 + n2)
    if q["kind"] == "ayet":
        mm = re.match(r"(.+?)\s+(\d+)/(.+)$", src)
        name, s, ay = mm.group(1), mm.group(2), mm.group(3)
        return "|".join(["KURAN", f"📖 KUR'ÂN-I KERÎM · {tr_upper(name)} {s}/{ay}", AYET[qid]["ar"], nopipe(tr), f"{s}/{name}, {ay}"])
    if q["kind"] == "hadis":
        ar, lafiz = None, None
        if qid in DIRECT:
            ar = DIRECT[qid]["ar"]
        elif TRIM.get(qid, {}).get("ar"):
            ar = TRIM[qid]["ar"]
        elif WEB.get(qid, {}).get("ar"):
            ar, lafiz = WEB[qid]["ar"], (WEB[qid].get("lafiz") or "").strip()
        if not ar:
            missing_ar.append(qid)
        ref = src if src and src != "Hadîs-i şerîf" else ""
        if extra:
            ref = (ref + " · " if ref else "") + extra
        if lafiz:
            ns, nl = set(re.findall(r"\d{2,5}", ref)), set(re.findall(r"\d{2,5}", lafiz))
            if not (nl and nl <= ns):
                ref = (ref + " · " if ref else "") + "Arapça lafız: " + lafiz
        konu = KONU.get(qid, "").strip()
        return "|".join(["HADIS", "📜 HADİS-İ ŞERÎF" + (f" · {konu}" if konu else ""), nopipe(ar or ""), nopipe(tr), nopipe(ref)])
    so = SOZ.get(qid, {})
    return "|".join(["SOZ", nopipe("💬 " + (so.get("label") or tr_upper(src) or "SÖZ")), nopipe(tr), nopipe(so.get("ref", "") or extra)])


lines = [
    "OUT|Alemlere_Rahmet_Siyer-i_Nebi.docx",
    "HEADER|GENİŞ ÖZET · Âlemlere Rahmet — Sallâbî ve Evlakî",
    "COVER|GENİŞ ÖZET|ÂLEMLERE RAHMET|Cahiliyeden Uhud'a Siyer-i Nebî|Ali Muhammed Sallâbî · Enver el-Evlakî"
    "|Siyer-i Nebî ve Rasulullah'ın Hayatı · Birleştirilmiş Geniş Özet",
    "LEGEND",
    "TOC|İÇİNDEKİLER",
]


PARTIAL = os.environ.get("OZET_KISMI") == "1"     # deneme: eksik bölümleri atla


def add_ozet(name):
    p = os.path.join(OZ, name + ".txt")
    if not os.path.exists(p):
        if PARTIAL:
            return False
        raise SystemExit(f"eksik Geniş Özet dosyası: {p}")
    for ln in open(p).read().split("\n"):
        if not ln.strip():
            continue
        tag = ln.split("|", 1)[0]
        if tag not in TAGS:
            raise SystemExit(f"{name}: bilinmeyen etiket: {ln[:60]}")
        lines.append(quote_line(ln.split("|", 1)[1].strip()) if tag == "QUOTE" else clean(ln))
    return True


lines.append("UH1|Önsöz")
add_ozet("onsoz")
for f in sorted(glob.glob(os.path.join(ROOT, CH, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", f).group(1))
    if n in PARTS:
        lab, title, desc = PARTS[n]
        lines.append(f"PART|{lab}|{title}|{desc}")
    title = re.sub(r"^#\s*\d+\.\s*", "", open(f).readline().strip())
    lines.append("H1|" + tr_upper(clean(title)))
    if not add_ozet(f"ch{n:02d}"):
        lines.append("INTRO|(Bu bölüm henüz hazır değil.)")
lines.append("UH1|Sonsöz")
add_ozet("sonsoz")

# Kronoloji: giriş + tablo
kr = clean(open(os.path.join(ROOT, FR, "91_kronoloji.md")).read())
lines.append("UH1|Kronoloji")
intro = [p.strip() for p in re.split(r"\n\s*\n", kr) if p.strip() and not p.lstrip().startswith(("#", "|"))]
sent = re.split(r"(?<=\.)\s+", " ".join(intro))
lines.append("INTRO|" + sent[0])
lines += ["B1|" + s for s in sent[1:]]
rows = [r for r in kr.split("\n") if r.strip().startswith("|")]
cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
cells = [c for c in cells if not all(re.match(r"^:?-+:?$", x) for x in c)]
lines.append("TABLE|" + "|".join(cells[0]))
lines += ["ROW|" + "|".join(c) for c in cells[1:]]
lines.append("ENDTABLE")

kp = os.path.join(AR, "kaynaklar.txt")
if os.path.exists(kp):
    lines.append("SRCH|KAYNAKLAR")
    lines += [ln.strip() for ln in open(kp) if ln.startswith("SRC|")]
lines.append("CLOSE|Allah'ım! Efendimiz Muhammed'e, onun âline ve ashâbına salât ve selâm eyle.")

dup = sorted({u for u in used if used.count(u) > 1})
unused = sorted(set(QUOTES) - set(used))
if dup or (unused and not PARTIAL):
    raise SystemExit(f"alıntı hatası: tekrar={dup} kullanılmayan={unused}")
with open(os.path.join(OUT, "kitap.txt"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
open(os.path.join(OUT, "dipnotlar.txt"), "w").close()
kinds = {}
for ln in lines:
    kinds[ln.split("|", 1)[0]] = kinds.get(ln.split("|", 1)[0], 0) + 1
print("satır türleri:", kinds)
print("Arapçası eksik hadis:", len(missing_ar), missing_ar)
