"""Kitabın Markdown kaynaklarını kayıtlı Geniş Özet satır biçimine çevirir.

Kullanım: python3 -I md2kitap.py <kök> <çıktı_klasörü>
  <kök>: bolumler/ (chapters/), on-arka/ (front/) ve arapca/ (ar/) klasörlerini içeren klasör
Çıktı: kitap.txt (etiketli satırlar) ve dipnotlar.txt (FN|n|metin); ayrıca rapor.
"""
import glob
import json
import os
import re
import sys

ROOT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
# klasör adları: depo düzeni (bolumler/on-arka/arapca) ya da çalışma düzeni (chapters/front/ar)
CH = "bolumler" if os.path.isdir(os.path.join(ROOT, "bolumler")) else "chapters"
FR = "on-arka" if os.path.isdir(os.path.join(ROOT, "on-arka")) else "front"
AR = os.path.join(ROOT, "arapca" if os.path.isdir(os.path.join(ROOT, "arapca")) else "ar")


def load(name, default):
    p = os.path.join(AR, name)
    return json.load(open(p)) if os.path.exists(p) else default


QUOTES = load("quotes.json", [])
AYET = load("ayet.json", {})
DIRECT = load("hadis_direct.json", {})
TRIM = load("trim_result.json", {})
WEB = load("web_result.json", {})
KONU = load("konu.json", {})
SOZ = load("soz.json", {})
EXTRA = load("extra_hadis.json", {})      # siyer kaynaklarından gelen Peygamber sözleri -> hadis kutusu
for q in QUOTES:
    if q["id"] in EXTRA:
        q["kind"] = "hadis"
        if EXTRA[q["id"]].get("ar"):
            DIRECT[q["id"]] = {"ar": EXTRA[q["id"]]["ar"]}
        KONU.setdefault(q["id"], EXTRA[q["id"]]["konu"])
QBYFILE = {}
for q in QUOTES:
    QBYFILE.setdefault(os.path.basename(q["file"]), []).append(q)

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
             ("Muhacirler", "Muhâcirler"), ("Muhacirlere", "Muhâcirlere"), ("Muhacirleri", "Muhâcirleri"))


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


fn_num = {}      # "5-3" -> 17
fn_text = {}     # "5-3" -> metin
lines = []
missing_ar = []


def clean(t):
    t = t.replace("\\'", "'").replace('\\"', '"').replace("\\*", "*")
    for a, b in NORMALIZE:
        t = t.replace(a, b)
    return t


def refs(t):
    """[^5-3] -> [^17] (ilk geçiş sırasıyla numaralandırır)."""
    def rep(m):
        lab = m.group(1)
        if lab not in fn_num:
            fn_num[lab] = len(fn_num) + 1
        return f"[^{fn_num[lab]}]"
    return re.sub(r"\[\^([^\]]+)\]", rep, t)


def nopipe(t):
    return t.replace("|", "/")


def quote_line(q):
    tr = clean(q["tr"]).strip()
    src = clean(q["src"]).strip()
    m = re.findall(r"\[\^[^\]]+\]", src)          # kaynak satırındaki dipnot işareti metne taşınır
    src = re.sub(r"\s*\[\^[^\]]+\]", "", src)
    tr = refs(tr + "".join(m))
    if q["kind"] == "ayet":
        mm = re.match(r"(.+?)\s+(\d+)/(.+)$", src)
        name, s, ay = mm.group(1), mm.group(2), mm.group(3)
        ar = AYET[q["id"]]["ar"]
        return "|".join(["KURAN", f"📖 KUR'ÂN-I KERÎM · {tr_upper(name)} {s}/{ay}", ar, nopipe(tr), f"{s}/{name}, {ay}"])
    if q["kind"] == "hadis":
        ar, lafiz = None, None
        if q["id"] in DIRECT:
            ar = DIRECT[q["id"]]["ar"]
        elif TRIM.get(q["id"], {}).get("ar"):
            ar = TRIM[q["id"]]["ar"]
        elif WEB.get(q["id"], {}).get("ar"):
            ar = WEB[q["id"]]["ar"]
            lafiz = (WEB[q["id"]].get("lafiz") or "").strip()
        if not ar:
            missing_ar.append(q["id"])
        ref = src if src and src != "Hadîs-i şerîf" else ""
        if lafiz and lafiz not in ref:
            nums_src = set(re.findall(r"\d{2,5}", ref))
            nums_laf = set(re.findall(r"\d{2,5}", lafiz))
            if not (nums_laf and nums_laf <= nums_src):
                ref = (ref + " · " if ref else "") + "Arapça lafız: " + lafiz
        konu = KONU.get(q["id"], "").strip()
        label = "📜 HADİS-İ ŞERÎF" + (f" · {konu}" if konu else "")
        return "|".join(["HADIS", label, nopipe(ar or ""), nopipe(tr), nopipe(ref)])
    so = SOZ.get(q["id"], {})
    label = "💬 " + (so.get("label") or tr_upper(src) or "SÖZ")
    return "|".join(["SOZ", nopipe(label), nopipe(tr), nopipe(so.get("ref", ""))])


def convert(path, chapter_no=None):
    t = clean(open(path).read())
    # dipnot tanımları
    body_lines = []
    for ln in t.split("\n"):
        m = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", ln)
        if m:
            fn_text[m.group(1)] = m.group(2).strip()
        else:
            body_lines.append(ln)
    blocks = re.split(r"\n\s*\n", "\n".join(body_lines))
    qs = list(QBYFILE.get(os.path.basename(path), []))
    for b in blocks:
        b = b.strip("\n")
        if not b.strip():
            continue
        first = b.lstrip()
        if first.startswith("# "):
            title = first[2:].strip()
            if chapter_no:
                title = re.sub(r"^\d+\.\s*", "", title)
                lines.append("H1|" + title)
            else:
                lines.append("UH1|" + title)
        elif first.startswith("## "):
            lines.append("H2|" + refs(first[3:].strip()))
        elif first.startswith("### "):
            lines.append("H3|" + refs(first[4:].strip()))
        elif first.startswith(">"):
            lines.append(quote_line(qs.pop(0)))
        elif first.startswith("|"):
            rows = [r for r in b.split("\n") if r.strip().startswith("|")]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            cells = [c for c in cells if not all(re.match(r"^:?-+:?$", x) for x in c)]
            lines.append("TABLE|" + "|".join(cells[0]))
            for c in cells[1:]:
                lines.append("ROW|" + "|".join(refs(x) for x in c))
            lines.append("ENDTABLE")
        elif re.match(r"^\d+\.\s", first):
            for ln in b.split("\n"):
                if ln.strip():
                    lines.append("L|" + refs(ln.strip()))
        elif re.match(r"^[-*+]\s", first):
            for ln in b.split("\n"):
                if ln.strip():
                    lines.append("B1|" + refs(re.sub(r"^[-*+]\s+", "", ln.strip())))
        else:
            lines.append("P|" + refs(" ".join(x.strip() for x in b.split("\n"))))
    if qs:
        raise SystemExit(f"{path}: kullanılmamış alıntı kaldı: {[q['id'] for q in qs]}")


lines += [
    "OUT|Alemlere_Rahmet_Siyer-i_Nebi.docx",
    "HEADER|ÂLEMLERE RAHMET · Cahiliyeden Uhud'a Siyer-i Nebî",
    "COVER|SİYER-İ NEBÎ|ÂLEMLERE RAHMET|Cahiliyeden Uhud'a Siyer-i Nebî|Ali Muhammed Sallâbî · Enver el-Evlakî"
    "|Siyer-i Nebî ve Rasûlullah'ın Hayatı eserlerinden hareketle",
    "LEGEND",
    "TOC|İÇİNDEKİLER",
]
for f in sorted(glob.glob(os.path.join(ROOT, FR, "0*.md"))):
    convert(f)
for f in sorted(glob.glob(os.path.join(ROOT, CH, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", f).group(1))
    if n in PARTS:
        lab, title, desc = PARTS[n]
        lines.append(f"PART|{lab}|{title}|{desc}")
    convert(f, n)
for f in sorted(glob.glob(os.path.join(ROOT, FR, "9*.md"))):
    convert(f)
kp = os.path.join(AR, "kaynaklar.txt")
if os.path.exists(kp):
    lines.append("SRCH|KAYNAKLAR")
    lines += [ln.strip() for ln in open(kp) if ln.startswith("SRC|")]
lines.append("CLOSE|Allah'ım! Efendimiz Muhammed'e, onun âline ve ashâbına salât ve selâm eyle.")

undefined = [lab for lab in fn_num if lab not in fn_text]
if undefined:
    raise SystemExit(f"tanımsız dipnot: {undefined[:10]}")
with open(os.path.join(OUT, "kitap.txt"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(os.path.join(OUT, "dipnotlar.txt"), "w") as fh:
    for lab, n in sorted(fn_num.items(), key=lambda x: x[1]):
        fh.write(f"FN|{n}|{fn_text[lab]}\n")
kinds = {}
for ln in lines:
    kinds[ln.split("|", 1)[0]] = kinds.get(ln.split("|", 1)[0], 0) + 1
print("satır türleri:", kinds)
print("dipnot:", len(fn_num), "| Arapçası eksik hadis:", len(missing_ar), missing_ar)
