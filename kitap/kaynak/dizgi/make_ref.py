"""Kitap için pandoc reference.docx şablonunu üretir."""
import sys
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

src, out = sys.argv[1], sys.argv[2]
FONT = "Palatino Linotype"
GREEN = RGBColor(0x23, 0x46, 0x3A)
GOLD = RGBColor(0x9A, 0x7B, 0x3C)
GREY = RGBColor(0x40, 0x40, 0x40)

d = docx.Document(src)


def set_font(style, size=None, bold=None, italic=None, color=None, name=FONT):
    f = style.font
    f.name = name
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color is not None:
        f.color.rgb = color


def para(style, align=None, before=None, after=None, line=None, indent=None,
         left=None, right=None, keep_next=None, page_break=None):
    pf = style.paragraph_format
    if align is not None:
        pf.alignment = align
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if line is not None:
        pf.line_spacing = line
    if indent is not None:
        pf.first_line_indent = Cm(indent)
    if left is not None:
        pf.left_indent = Cm(left)
    if right is not None:
        pf.right_indent = Cm(right)
    if keep_next is not None:
        pf.keep_with_next = keep_next
    if page_break is not None:
        pf.page_break_before = page_break


def border(style, side="left", color="9A7B3C", sz=12, space=10):
    ppr = style.element.get_or_add_pPr()
    b = ppr.find(qn("w:pBdr"))
    if b is None:
        b = OxmlElement("w:pBdr")
        ppr.append(b)
    e = OxmlElement(f"w:{side}")
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), str(sz))
    e.set(qn("w:space"), str(space))
    e.set(qn("w:color"), color)
    b.append(e)


def get(name, base="Normal"):
    try:
        return S[name]
    except KeyError:
        s = d.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = S[base]
        return s


class _S:
    def __getitem__(self, n):
        for st in d.styles:
            if st.name == n or st.element.get(qn("w:styleId")) == n.replace(" ", ""):
                return st
        raise KeyError(n)
S = _S()
# Varsayılan yazı tipi (docDefaults)
rpr_def = d.styles.element.find(qn("w:docDefaults")).find(qn("w:rPrDefault")).find(qn("w:rPr"))
rf = rpr_def.find(qn("w:rFonts"))
for a in list(rf.attrib):
    del rf.attrib[a]
for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rf.set(qn(a), FONT)
lang = rpr_def.find(qn("w:lang"))
if lang is None:
    lang = OxmlElement("w:lang")
    rpr_def.append(lang)
lang.set(qn("w:val"), "tr-TR")
lang.set(qn("w:eastAsia"), "tr-TR")
lang.set(qn("w:bidi"), "ar-SA")

set_font(S["Normal"], 10.5, color=RGBColor(0x1A, 0x1A, 0x1A))
para(S["Normal"], line=1.18)
for n in ("Body Text", "First Paragraph"):
    set_font(S[n], 10.5)
    para(S[n], align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=3, line=1.18,
         indent=0.6 if n == "Body Text" else 0)
    # dul/yetim satır kontrolü
    ppr = S[n].element.get_or_add_pPr()
    w = OxmlElement("w:widowControl")
    ppr.append(w)
set_font(S["Compact"], 9.5)
para(S["Compact"], align=WD_ALIGN_PARAGRAPH.LEFT, before=2, after=2, line=1.1, indent=0)

# Kısım başlığı
h1 = S["Heading 1"]
set_font(h1, 24, bold=False, color=GREEN)
para(h1, align=WD_ALIGN_PARAGRAPH.CENTER, before=170, after=18, line=1.1,
     page_break=True, keep_next=True)
h1.font.small_caps = True
# Bölüm başlığı
h2 = S["Heading 2"]
set_font(h2, 19, bold=False, color=GREEN)
para(h2, align=WD_ALIGN_PARAGRAPH.LEFT, before=70, after=20, line=1.1,
     page_break=True, keep_next=True)
border(h2, "bottom", "9A7B3C", 6, 8)
# Alt başlıklar
h3 = S["Heading 3"]
set_font(h3, 12.5, bold=True, color=GREEN)
para(h3, align=WD_ALIGN_PARAGRAPH.LEFT, before=16, after=6, keep_next=True)
h4 = S["Heading 4"]
set_font(h4, 11, bold=True, italic=True, color=GREY)
para(h4, before=10, after=4, keep_next=True)
for n in ("Heading 1", "Heading 2", "Heading 3", "Heading 4"):
    S[n].font.italic = S[n].font.italic or False

# Alıntı (âyet/hadis)
bt = S["Block Text"]
set_font(bt, 10.5, italic=True, color=RGBColor(0x2B, 0x2B, 0x2B))
para(bt, align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=4, after=2, line=1.15,
     left=0.9, right=0.6, indent=0)
border(bt, "left", "9A7B3C", 14, 9)
src_style = get("Alinti Kaynak", "Block Text")
set_font(src_style, 9, italic=False, color=GOLD)
para(src_style, align=WD_ALIGN_PARAGRAPH.RIGHT, before=0, after=10)
src_style.font.small_caps = True

# Dipnot
fn = S["Footnote Text"]
set_font(fn, 8.5)
para(fn, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=1, line=1.0)

# Kapak ve diğer özel stiller
t = S["Title"]
set_font(t, 30, bold=False, color=GREEN)
para(t, align=WD_ALIGN_PARAGRAPH.CENTER, before=150, after=10)
st = S["Subtitle"]
set_font(st, 14, italic=True, color=GOLD)
para(st, align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=6)
au = S["Author"]
set_font(au, 11.5, color=GREY)
para(au, align=WD_ALIGN_PARAGRAPH.CENTER, before=60, after=4)
ka = get("Kisim Aciklama")
set_font(ka, 11, italic=True, color=GREY)
para(ka, align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=6, left=1.5, right=1.5, line=1.25)
ki = get("Kunye")
set_font(ki, 9, color=GREY)
para(ki, align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=4, line=1.2)
th = S["TOC Heading"]
set_font(th, 19, bold=False, color=GREEN)
para(th, align=WD_ALIGN_PARAGRAPH.LEFT, before=36, after=14, page_break=True)
for lvl, (sz, b, lft) in {1: (10.5, True, 0), 2: (10, False, 0.5)}.items():
    s = get(f"TOC {lvl}")
    set_font(s, sz, bold=b, color=GREEN if lvl == 1 else None)
    para(s, before=6 if lvl == 1 else 0, after=1, left=lft, line=1.1)

# Sayfa düzeni: 16 x 24 cm, aynalı kenar boşlukları, altta sayfa numarası
sec = d.sections[0]
sec.page_width, sec.page_height = Cm(16), Cm(24)
sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.2)
sec.left_margin, sec.right_margin = Cm(2.2), Cm(1.8)
sec.header_distance, sec.footer_distance = Cm(1.0), Cm(1.0)
settings = d.settings.element
mm = OxmlElement("w:mirrorMargins")
settings.insert(0, mm)
sec.different_first_page_header_footer = True
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run()
for kind, txt in (("begin", None), (None, " PAGE "), ("end", None)):
    if kind:
        e = OxmlElement("w:fldChar")
        e.set(qn("w:fldCharType"), kind)
    else:
        e = OxmlElement("w:instrText")
        e.set(qn("xml:space"), "preserve")
        e.text = txt
    r._r.append(e)
r.font.size = Pt(9)
r.font.color.rgb = GOLD
d.save(out)
print("ok", out)
