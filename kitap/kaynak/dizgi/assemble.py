"""Kayıtlı build.js + kitap_mode.js -> kitap_build.js (görünüm sabitleri aynen korunur)."""
import sys
src, mode, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read(); m = open(mode).read()
reps = [
    ('  ShadingType, LevelFormat, Header, Footer, PageNumber, FootnoteReferenceRun, VerticalAlign, LineRuleType,\n} = require("docx");',
     '  ShadingType, LevelFormat, Header, Footer, PageNumber, FootnoteReferenceRun, VerticalAlign, LineRuleType,\n  HeadingLevel, TableOfContents,\n} = require("docx");'),
    ('HAFS = "KFGQPC HafsEx1 Uthmanic Script"', 'HAFS = "KFGQPC HAFS Uthmanic Script"'),
    ('(async () => {\n  const jobs = [];\n',
     m + '\n(async () => {\n  const jobs = [];\n  if (WHICH === "kitap") {\n    const L = linesOf(/^kitap.*\\.txt$/i);\n'
     '    const fp = path.join(DIR, "dipnotlar.txt");\n'
     '    const F = fs.existsSync(fp) ? fs.readFileSync(fp, "utf8").split(/\\r?\\n/).filter((l) => l.trim()) : [];\n'
     '    if (!L.length) throw new Error("kitap*.txt bulunamadı: " + DIR);\n    fs.mkdirSync(OUT, { recursive: true });\n'
     '    const name = meta(L, "OUT", "KITAP.docx");\n    fs.writeFileSync(path.join(OUT, name), await Packer.toBuffer(buildKitap(L, F)));\n'
     '    console.log("yazıldı:", path.join(OUT, name));\n    return;\n  }\n'),
    ('// build.js — "Geniş Özet" ve "Açıklamalı Tam Metin" Word belgeleri (docx-js)',
     '// kitap_build.js — kayıtlı "Geniş Özet" build.js + kitap modu (düzyazı, dipnot, kısım, içindekiler)\n'
     '// Kullanım: NODE_PATH=$(npm root -g) node kitap_build.js <içerik_klasörü> <çıktı_klasörü> kitap\n'
     '// build.js — "Geniş Özet" ve "Açıklamalı Tam Metin" Word belgeleri (docx-js)'),
]
for a, b in reps:
    assert s.count(a) == 1, a[:50]
    s = s.replace(a, b)
open(out, 'w').write(s)
print('yazıldı:', out)
