"""Bölümleri birleştirip kitabın .docx dosyasını üretir.

Kullanım: python3 -I build.py <çıktı.docx>
"""
import glob
import os
import re
import subprocess
import sys

import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.environ.get("BOOKROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]

TITLE = "Âlemlere Rahmet"
SUB = "Cahiliyeden Uhud'a Siyer-i Nebî"
SUB2 = "Ali Muhammed Sallâbî ve Enver el-Evlakî'nin eserlerinden hareketle"

PARTS = {
    1: ("I. Kısım", "Nübüvvetin Arifesinde",
        "Bi'setten önceki dünya, Arap yarımadası, Fil Yılı ve Rasûlullah'ın (s.a.v.) "
        "doğumundan Hira'ya uzanan kırk yılı."),
    8: ("II. Kısım", "Mekke'de Davet",
        "İlk vahiyden Tâif dönüşüne: gizli ve açık davet, işkence, Habeşistan hicreti, "
        "boykot yılları ve İsrâ-Mi'râc."),
    16: ("III. Kısım", "Hicret",
         "Kabilelere arz, Akabe biatleri ve Mekke'den Medine'ye uzanan büyük yolculuk."),
    19: ("IV. Kısım", "Medine'de Devlet",
         "Mescid, kardeşlik ve Vesîka ile kurulan devlet; Bedir'in zaferi ve Uhud'un sınavı."),
}


def raw(xml):
    return "\n```{=openxml}\n" + xml + "\n```\n\n"


PAGEBREAK = raw('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')


def styled(style, text):
    return f'::: {{custom-style="{style}"}}\n{text}\n:::\n\n'


def shift(md):
    """Bölüm dosyasındaki başlıkları bir seviye aşağı kaydırır (# -> ##)."""
    out = []
    fence = False
    for line in md.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,5} ", line):
            line = "#" + line
        out.append(line)
    md = "\n".join(out)
    # yazım birliği
    for a, b in (("Hristiyan", "Hıristiyan"), ("Vesikası", "Vesîkası"), ("Vesika ", "Vesîka "),
                 ("Muhacirler", "Muhâcirler"), ("Muhacirlere", "Muhâcirlere"), ("Muhacirleri", "Muhâcirleri")):
        md = md.replace(a, b)
    # alıntı bloğundaki kaynak satırını ayrı paragraf yap
    md = re.sub(r"\n>[ \t]*([—–]|-{1,3} )", lambda m: "\n>\n> " + m.group(1), md)
    return md


def toc_xml():
    return raw(
        '<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t>İçindekiler</w:t></w:r></w:p>'
        '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:t>İçindekiler tablosunu görmek için alanları güncelleyin (F9).</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')


parts = []
# Başlık sayfası
parts.append(styled("Title", TITLE))
parts.append(styled("Subtitle", SUB))
parts.append(styled("Author", SUB2))
# Künye sayfası
parts.append(PAGEBREAK)
kunye = open(os.path.join(ROOT, "on-arka", "kunye.md")).read()
parts.append(styled("Kunye", kunye))
parts.append(toc_xml())
for f in sorted(glob.glob(os.path.join(ROOT, "on-arka", "0*.md"))):
    parts.append(shift(open(f).read()) + "\n\n")
for f in sorted(glob.glob(os.path.join(ROOT, "bolumler", "ch*.md"))):
    n = int(re.search(r"ch(\d+)", f).group(1))
    if n in PARTS:
        k, name, desc = PARTS[n]
        parts.append(f"# {k}<br>{name}\n\n".replace("<br>", " — "))
        parts.append(styled("Kisim Aciklama", desc))
    parts.append(shift(open(f).read()) + "\n\n")
for f in sorted(glob.glob(os.path.join(ROOT, "on-arka", "9*.md"))):
    parts.append(shift(open(f).read()) + "\n\n")

md = "".join(parts)
md_path = os.path.join(B, "kitap.md")
open(md_path, "w").write(md)
tmp = os.path.join(B, "_pandoc.docx")
subprocess.run(["pandoc", md_path, "-f", "markdown+smart-implicit_figures", "-o", tmp,
                "--reference-doc", os.path.join(B, "reference.docx")], check=True)

# --- Son işlemler ---
d = docx.Document(tmp)
styles = {s.name: s for s in d.styles}
src_style = styles["Alinti Kaynak"]
n_src = 0
for p in d.paragraphs:
    sname = p.style.name if p.style is not None else ""
    t = p.text.strip()
    if sname == "Block Text" and (t.startswith("—") or t.startswith("–")):
        p.style = src_style
        for r in p.runs:
            r.font.italic = False
        n_src += 1
    # Kısım başlığında "I. Kısım — Ad" -> iki satır
    if sname == "Heading 1" and " — " in t:
        a, b = t.split(" — ", 1)
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)
        p.runs[0].text = a
        br = OxmlElement("w:br")
        run = p.add_run()
        run._r.append(br)
        p.add_run(b)
# Alıntı bloğundan sonra gelen ilk paragraf girintisiz olmasın diye dokunma; Word okunur.
# Kapak: kenar boşluksuz ayrı bir bölüm olarak en başa
import copy
from docx.shared import Cm, Pt, RGBColor
body = d.element.body
cp_par = d.add_paragraph()
cp_par.paragraph_format.space_before = Pt(0)
cp_par.paragraph_format.space_after = Pt(0)
cp_par.paragraph_format.line_spacing = 1.0
cp_par.add_run().add_picture(os.path.join(B, "cover.jpg"), width=Cm(15.98), height=Cm(23.95))
main_sp = body.find(qn("w:sectPr"))
sp = copy.deepcopy(main_sp)
for tag in ("w:headerReference", "w:footerReference", "w:titlePg"):
    for e in sp.findall(qn(tag)):
        sp.remove(e)
mar = sp.find(qn("w:pgMar"))
for a in ("w:top", "w:bottom", "w:left", "w:right", "w:header", "w:footer", "w:gutter"):
    mar.set(qn(a), "0")
ppr = cp_par._p.get_or_add_pPr()
ppr.append(sp)
body.remove(cp_par._p)
body.insert(0, cp_par._p)
# Ana bölüm 1'den numaralansın
pg = main_sp.find(qn("w:pgNumType"))
if pg is None:
    pg = OxmlElement("w:pgNumType")
    main_sp.append(pg)
pg.set(qn("w:start"), "1")

# Tablolar: yatay ince çizgiler, başlık satırı kalın
def _bdr(parent, tag, sides, color, sz):
    b = OxmlElement(tag)
    for side in sides:
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single" if sz else "nil")
        if sz:
            e.set(qn("w:sz"), str(sz))
            e.set(qn("w:space"), "0")
            e.set(qn("w:color"), color)
        b.append(e)
    parent.append(b)

for tbl in d.tables:
    tblPr = tbl._tbl.tblPr
    for e in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(e)
    _bdr(tblPr, "w:tblBorders", ["top", "bottom", "insideH"], "C8B48A", 4)
    for ri, row in enumerate(tbl.rows):
        for ci, cell in enumerate(row.cells):
            for p in cell.paragraphs:
                p.paragraph_format.first_line_indent = Cm(0)
                for r in p.runs:
                    if ri == 0:
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(0x23, 0x46, 0x3A)
                    elif ci == 0:
                        r.font.bold = True
                        r.font.size = Pt(9)
    # başlık satırı her sayfada tekrar etsin
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader")
    trPr.append(h)

# Dipnot numaraları her sayfada yeniden başlasın
def _fn_restart(parent, before_tags):
    fp = parent.find(qn("w:footnotePr"))
    if fp is None:
        fp = OxmlElement("w:footnotePr")
        # şemaya uygun konum: sectPr içinde pgSz'den önce
        anchor = None
        for t in before_tags:
            anchor = parent.find(qn(t))
            if anchor is not None:
                break
        if anchor is not None:
            anchor.addprevious(fp)
        else:
            parent.insert(0, fp)
    for e in fp.findall(qn("w:numRestart")):
        fp.remove(e)
    nr = OxmlElement("w:numRestart")
    nr.set(qn("w:val"), "eachPage")
    fp.append(nr)

_fn_restart(main_sp, ("w:endnotePr", "w:type", "w:pgSz"))
_set_fp = d.settings.element.find(qn("w:footnotePr"))
if _set_fp is not None:
    for e in _set_fp.findall(qn("w:numRestart")):
        _set_fp.remove(e)
    nr = OxmlElement("w:numRestart")
    nr.set(qn("w:val"), "eachPage")
    # numRestart, footnote ayırıcı referanslarından önce gelmeli
    first_fn = _set_fp.find(qn("w:footnote"))
    if first_fn is not None:
        first_fn.addprevious(nr)
    else:
        _set_fp.append(nr)

# Alanların açılışta güncellenmesi
st = d.settings.element
uf = OxmlElement("w:updateFields")
uf.set(qn("w:val"), "true")
st.append(uf)
cp = d.core_properties
cp.title = f"{TITLE} — {SUB}"
cp.subject = SUB2
cp.author = ""
cp.language = "tr-TR"
d.save(OUT)
os.remove(tmp)
# OOXML öğe sırasını şemaya uydur (Word uyumluluğu)
subprocess.run([sys.executable, "-I", os.path.join(B, "fix_ooxml.py"), OUT], check=True)
print("ok", OUT, "kaynak satırı:", n_src)
