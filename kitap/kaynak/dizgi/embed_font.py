"""Bir TrueType yazı tipini .docx içine gömer (ECMA-376 obfuscated font).

Kullanım: python3 -I embed_font.py <belge.docx> <yazitipi.ttf> "<Yazı Tipi Adı>"
Word, gömülü yazı tipini o bilgisayarda yüklü olmasa da kullanır.
"""
import re
import shutil
import sys
import tempfile
import uuid
import zipfile

DOCX, TTF, NAME = sys.argv[1], sys.argv[2], sys.argv[3]
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
FONT_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"
CT = "application/vnd.openxmlformats-officedocument.obfuscatedFont"

guid = str(uuid.uuid4()).upper()
font_key = "{" + guid + "}"
key = bytes.fromhex(guid.replace("-", ""))[::-1]       # GUID baytları ters sırada
data = bytearray(open(TTF, "rb").read())
for i in range(32):                                     # ilk 32 bayt anahtarla XOR
    data[i] ^= key[i % 16]

src = zipfile.ZipFile(DOCX)
names = src.namelist()
files = {n: src.read(n) for n in names}
src.close()

rid = "rIdEmbedFont1"
part = "fonts/font1.odttf"
files["word/" + part] = bytes(data)

# [Content_Types].xml
ct = files["[Content_Types].xml"].decode("utf8")
if 'Extension="odttf"' not in ct:
    ct = ct.replace("</Types>", f'<Default Extension="odttf" ContentType="{CT}"/></Types>')
files["[Content_Types].xml"] = ct.encode("utf8")

# word/_rels/fontTable.xml.rels
rels_name = "word/_rels/fontTable.xml.rels"
rels = files.get(rels_name, b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>').decode("utf8")
rels = re.sub(r"<Relationships([^>]*?)\s*/>", r"<Relationships\1></Relationships>", rels)   # boş, kendinden kapanan biçim
rels = rels.replace("</Relationships>", f'<Relationship Id="{rid}" Type="{FONT_REL}" Target="{part}"/></Relationships>')
files[rels_name] = rels.encode("utf8")

# word/fontTable.xml: ilgili <w:font> öğesine embedRegular ekle (yoksa öğeyi oluştur)
ft = files["word/fontTable.xml"].decode("utf8")
ft = re.sub(r"<w:fonts([^>]*?)\s*/>", r"<w:fonts\1></w:fonts>", ft, count=1)   # boş, kendinden kapanan biçim
if 'xmlns:r="' not in ft[:2000]:
    ft = re.sub(r"<w:fonts ", f'<w:fonts xmlns:r="{R}" ', ft, count=1)
embed = f'<w:embedRegular r:id="{rid}" w:fontKey="{font_key}"/>'
pat = re.compile(r'<w:font w:name="' + re.escape(NAME) + r'"\s*(/>|>(.*?)</w:font>)', re.S)
m = pat.search(ft)
if m:
    inner = m.group(2) or ""
    ft = ft[:m.start()] + f'<w:font w:name="{NAME}">{inner}{embed}</w:font>' + ft[m.end():]
else:
    ft = ft.replace("</w:fonts>", f'<w:font w:name="{NAME}"><w:charset w:val="00"/><w:family w:val="auto"/>'
                    f'<w:pitch w:val="variable"/>{embed}</w:font></w:fonts>')
files["word/fontTable.xml"] = ft.encode("utf8")

# word/settings.xml: gömülü yazı tiplerini kullan
st = files["word/settings.xml"].decode("utf8")
if "<w:embedTrueTypeFonts" not in st:
    st = re.sub(r"(<w:settings[^>]*>)", r"\1<w:embedTrueTypeFonts/>", st, count=1)
files["word/settings.xml"] = st.encode("utf8")

tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
tmp.close()
with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names + [n for n in files if n not in names]:
        z.writestr(n, files[n])
shutil.move(tmp.name, DOCX)
print(f"gömüldü: {NAME} ({len(data)//1024} KB) -> {DOCX}")
