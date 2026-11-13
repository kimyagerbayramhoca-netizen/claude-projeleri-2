// build.js — "Geniş Özet" ve "Açıklamalı Tam Metin" Word belgeleri (docx-js)
// Kullanım: NODE_PATH=$(npm root -g) node build.js <içerik_klasörü> <çıktı_klasörü> [ozet|metin|both]
//   ozet*.txt → Geniş Özet · metin*.txt → Açıklamalı Tam Metin · dipnotlar.txt → FN|n|metin (" ¶ " = dipnot içi paragraf)
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, BorderStyle,
  ShadingType, LevelFormat, Header, Footer, PageNumber, FootnoteReferenceRun, VerticalAlign, LineRuleType,
} = require("docx");

const [DIR, OUT, WHICH = "both"] = process.argv.slice(2);
if (!DIR || !OUT) { console.error("Kullanım: node build.js <içerik_klasörü> <çıktı_klasörü> [ozet|metin|both]"); process.exit(1); }
const listFiles = (re) => fs.readdirSync(DIR).filter((f) => re.test(f)).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
const linesOf = (re) => listFiles(re).flatMap((f) => fs.readFileSync(path.join(DIR, f), "utf8").split(/\r?\n/)).filter((l) => l.trim());
const meta = (lines, key, def) => { const l = lines.find((x) => x.startsWith(key + "|")); return l ? l.slice(key.length + 1).trim() : def; };

// ---------- renkler, yazı tipleri, ölçüler ----------
const TEAL = "1F4E5F", BLUE = "2E75B6", RED = "C00000", GRAY = "595959", DARK = "262626", GOLD = "B8860B";
const BOX = {
  kuran: { fill: "FFF2CC", accent: GOLD }, hadis: { fill: "E2EFDA", accent: "548235" },
  kavram: { fill: "DEEBF7", accent: BLUE }, soz: { fill: "EDE7F6", accent: "7030A0" },
};
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1440, CONTENT_W = PAGE_W - 2 * MARGIN;
const BODY = "Calibri", HAFS = "KFGQPC HafsEx1 Uthmanic Script", AMIRI = "Amiri", SYM = "Segoe UI Symbol", EMOJI = "Segoe UI Emoji";
const LINE = { line: 300, lineRule: LineRuleType.AUTO };
const font = (n) => ({ ascii: n, hAnsi: n, cs: n, eastAsia: n });

// ---------- satır içi biçim: **kalın vurgu**  *italik*  [^n] dipnot  ✎ ----------
const AR = "\\u0600-\\u06FF\\u0750-\\u077F\\u08A0-\\u08FF\\uFB50-\\uFDFF\\uFE70-\\uFEFF";
const AR_SPAN = new RegExp(`[${AR}](?:[${AR}\\s\\u0640،؛:\\.]*[${AR}])?`, "g");
const smartQuotes = (t) => t.replace(/(^|[\s(\[{—–\-\/«])"/g, "$1“").replace(/"/g, "”");

function arabicRuns(text, base, arSize) { // emniyet ağı; içerikte Arapça satır içine yazılmaz
  const out = []; let last = 0;
  for (const m of text.matchAll(AR_SPAN)) {
    if (m.index > last) out.push(new TextRun({ ...base, text: text.slice(last, m.index) }));
    const sz = arSize || base.size;
    out.push(new TextRun({ ...base, text: m[0], rightToLeft: true, font: font(AMIRI), size: sz, sizeComplexScript: sz,
      bold: false, boldComplexScript: false, italics: false, italicsComplexScript: false }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ ...base, text: text.slice(last) }));
  return out;
}

function inline(raw, base = {}, opt = {}) {
  const parts = smartQuotes(raw).split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[\^\d+\]|✎)/g).filter((p) => p !== "");
  const runs = [];
  for (const p of parts) {
    if (p.startsWith("**") && p.endsWith("**")) runs.push(...arabicRuns(p.slice(2, -2), { ...base, bold: true, color: opt.boldColor || TEAL }, opt.arSize));
    else if (p.startsWith("*") && p.endsWith("*") && p.length > 2) runs.push(...arabicRuns(p.slice(1, -1), { ...base, italics: !base.italics }, opt.arSize));
    else if (/^\[\^\d+\]$/.test(p)) runs.push(new FootnoteReferenceRun(parseInt(p.slice(2, -1), 10)));
    else if (p === "✎") runs.push(new TextRun({ ...base, text: "✎", font: font(SYM) }));
    else runs.push(...arabicRuns(p, base, opt.arSize));
  }
  return runs;
}

// ---------- ortak parçalar ----------
const spacer = (after = 120) => new Paragraph({ spacing: { before: 0, after, line: 240 }, children: [new TextRun({ text: "", size: 8 })] });
const pageBreak = () => new Paragraph({ pageBreakBefore: true, spacing: { after: 0 }, children: [] });

// ✎ düzeltme notu: "açıklama||Arapça ibare||Arapça ibare" — Arapça her zaman ayrı sağdan-sola satırda
function noteParagraphs(raw) {
  const [tr, ...ars] = raw.split("||");
  const common = {
    indent: { left: 284 },
    shading: { fill: "FFF8E1", type: ShadingType.CLEAR, color: "auto" },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 6 } },
  };
  const out = [new Paragraph({ ...common, alignment: AlignmentType.JUSTIFIED, keepNext: ars.length > 0,
    spacing: { before: 0, after: ars.length ? 0 : 120, line: 260, lineRule: LineRuleType.AUTO },
    children: [new TextRun({ text: "✎ ", font: font(SYM), color: "7F6000", size: 18 }),
      new TextRun({ text: "düzeltme: ", bold: true, italics: true, color: "7F6000", size: 18 }),
      ...inline(tr, { italics: true, color: "7F6000", size: 18 })] })];
  ars.forEach((a, i) => out.push(new Paragraph({ ...common, bidirectional: true, alignment: AlignmentType.START, keepNext: i < ars.length - 1,
    spacing: { before: 20, after: i === ars.length - 1 ? 120 : 0, line: 300, lineRule: LineRuleType.AUTO },
    children: [new TextRun({ text: "«" + a.trim() + "»", rightToLeft: true, font: font(AMIRI), size: 22, sizeComplexScript: 22, color: "5C4500" })] })));
  return out;
}

function headerFooter(title) {
  return {
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT, spacing: { after: 0 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF", space: 4 } },
        children: [new TextRun({ text: title, size: 16, color: "7F7F7F", font: font(BODY) })],
      })] }),
      first: new Header({ children: [new Paragraph({ children: [] })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: ["— ", PageNumber.CURRENT, " —"], size: 18, color: "7F7F7F" })],
      })] }),
      first: new Footer({ children: [new Paragraph({ children: [] })] }),
    },
  };
}

const sectionProps = {
  page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN, header: 708, footer: 708 } },
  titlePage: true,
};
const baseStyles = { default: { document: { run: { font: BODY, size: 22, color: DARK }, paragraph: { spacing: LINE } } } };

function singleCellBox({ fill, border, borderSize = 6, children, margins = { top: 160, bottom: 160, left: 220, right: 220 } }) {
  const b = { style: BorderStyle.SINGLE, size: borderSize, color: border };
  const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W],
    borders: { top: b, bottom: b, left: b, right: b, insideHorizontal: none, insideVertical: none },
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: CONTENT_W, type: WidthType.DXA },
      shading: fill ? { fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
      margins, borders: { top: b, bottom: b, left: b, right: b }, children,
    })] })],
  });
}

function labelRuns(label, color) {
  const [emo, ...rest] = label.split(" ");
  return [
    new TextRun({ text: emo + " ", font: font(EMOJI), size: 20 }),
    new TextRun({ text: rest.join(" "), bold: true, color, size: 19, characterSpacing: 10 }),
  ];
}

// COVER|<etiket>|<BAŞLIK>|<alt başlık>|<müellif>|<eser · bölüm>
function cover(body, f, before) {
  const [label, title, subtitle, author, book] = f;
  body.push(new Paragraph({ spacing: { before, after: 200 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: label, bold: true, color: RED, size: 26, characterSpacing: 120 })] }));
  body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 80 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 10 } },
    children: [new TextRun({ text: title, bold: true, color: TEAL, size: 56 })] }));
  body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 240, after: 720 },
    children: [new TextRun({ text: subtitle, italics: true, color: GRAY, size: 26 })] }));
  body.push(singleCellBox({ fill: "FFFBEF", border: GOLD, borderSize: 12, margins: { top: 240, bottom: 240, left: 300, right: 300 }, children: [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: author, bold: true, color: TEAL, size: 28 })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [new TextRun({ text: book, italics: true, color: GRAY, size: 21 })] }),
  ] }));
}

// o = { v: dikey boşluk, l1/r1: sol hücre, l2/r2: sağ hücre iç boşlukları, size: sağ sütun yazı boyu }
function twoColTable(rows, w1, o) {
  const w2 = CONTENT_W - w1;
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [w1, w2], rows: rows.map(({ fill, accent, left, right }) => {
    const b = { style: BorderStyle.SINGLE, size: 6, color: accent };
    const lt = { style: BorderStyle.SINGLE, size: 4, color: "D9D9D9" };
    return new TableRow({ cantSplit: true, children: [
      new TableCell({ width: { size: w1, type: WidthType.DXA }, shading: { fill, type: ShadingType.CLEAR, color: "auto" },
        borders: { top: b, bottom: b, left: b, right: b }, margins: { top: o.v, bottom: o.v, left: o.l1, right: o.r1 }, verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: left })] }),
      new TableCell({ width: { size: w2, type: WidthType.DXA }, borders: { top: lt, bottom: lt, left: b, right: lt },
        margins: { top: o.v, bottom: o.v, left: o.l2, right: o.r2 }, verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({ spacing: { before: 0, after: 0, line: 264, lineRule: LineRuleType.AUTO }, children: [new TextRun({ text: right, italics: true, size: o.size, color: GRAY })] })] }),
    ] });
  }) });
}

function legend(body) { // Geniş Özet kapağı: RENK REHBERİ
  body.push(new Paragraph({ spacing: { before: 900, after: 120 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "RENK REHBERİ", bold: true, color: TEAL, size: 20, characterSpacing: 60 })] }));
  const items = [
    ["kuran", "📖 KUR'ÂN-I KERÎM", "Âyet-i kerîmeler: Arapça aslı ve meali"],
    ["hadis", "📜 HADİS-İ ŞERÎF", "Hadis-i şerifler: Arapça lafzı ve tercümesi"],
    ["kavram", "💡 KAVRAM", "Temel kavramların tanımları"],
    ["soz", "💬 SÖZ", "Âlimlerin sözleri ve rivâyetler"],
  ];
  body.push(twoColTable(items.map(([k, lab, desc]) => ({ ...BOX[k], left: labelRuns(lab, BOX[k].accent), right: desc })), 3400,
    { v: 90, l1: 160, r1: 120, l2: 200, r2: 120, size: 20 }));
  body.push(pageBreak());
}

function guide(body) { // Açıklamalı Tam Metin kapağı: OKUMA KILAVUZU
  body.push(new Paragraph({ spacing: { before: 800, after: 120 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "OKUMA KILAVUZU", bold: true, color: TEAL, size: 20, characterSpacing: 60 })] }));
  const items = [
    ["Kitabın metni", "Siyah, iki yana yaslı paragraflar. Taramadaki yazım hataları düzeltilmiş, sayfa başlıkları ayıklanmıştır.", "FFFFFF", "7F7F7F"],
    ["(Açıklama)", "Mavi zeminli, parantez içindeki bölüm: paragrafın sade anlatımı ve günlük hayattan örnek.", "EEF4FA", BLUE],
    ["✎ düzeltme", "Taramada bozuk çıkan yerlerin Arapça aslına veya bağlama göre nasıl kurulduğunu gösteren not.", "FFF8E1", GOLD],
    ["Dipnotlar", "Mütercimin dipnotları sayfa altında, kitaptaki numaralarıyla yer alır.", "FFFFFF", TEAL],
  ];
  body.push(twoColTable(items.map(([a, b, fill, accent]) => ({ fill, accent, right: b,
    left: a.startsWith("✎")
      ? [new TextRun({ text: "✎ ", font: font(SYM), color: accent, size: 20 }), new TextRun({ text: a.slice(2), bold: true, color: accent, size: 20 })]
      : [new TextRun({ text: a, bold: true, color: accent, size: 20 })] })), 2300,
    { v: 80, l1: 140, r1: 100, l2: 180, r2: 100, size: 19 }));
  body.push(pageBreak());
}

// ======================================================================
//  GENİŞ ÖZET
// ======================================================================
function buildOzet(lines) {
  const body = [];
  let h1 = 0, h2 = 0, table = null;

  const flushTable = () => {
    if (!table) return;
    const n = table.header.length;
    const weights = n === 2 ? [30, 70] : n === 3 ? [26, 34, 40] : Array(n).fill(100 / n);
    const widths = weights.map((w) => Math.round((CONTENT_W * w) / 100));
    widths[n - 1] = CONTENT_W - widths.slice(0, -1).reduce((a, b) => a + b, 0);
    const thin = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
    const borders = { top: thin, bottom: thin, left: thin, right: thin };
    const cell = (txt, i, fill, head) => new TableCell({
      width: { size: widths[i], type: WidthType.DXA }, borders,
      shading: { fill, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 80, bottom: 80, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ spacing: { before: 0, after: 0, line: 264, lineRule: LineRuleType.AUTO }, alignment: AlignmentType.LEFT,
        children: head ? [new TextRun({ text: txt, bold: true, color: "FFFFFF", size: 20 })]
          : inline(txt, { size: 20, bold: i === 0 && n > 2, color: i === 0 && n > 2 ? TEAL : DARK }) })],
    });
    const rows = [new TableRow({ tableHeader: true, cantSplit: true, children: table.header.map((t, i) => cell(t, i, BLUE, true)) })];
    table.rows.forEach((r, k) => rows.push(new TableRow({ cantSplit: true, children: r.map((t, i) => cell(t, i, k % 2 ? "F2F2F2" : "FFFFFF", false)) })));
    body.push(spacer(40));
    body.push(new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: widths, rows }));
    body.push(spacer(160));
    table = null;
  };

  const box = (kind, label, arabic, turkish, ref) => {
    const { fill, accent } = BOX[kind];
    const kids = [new Paragraph({ spacing: { before: 0, after: 100 }, keepNext: true, children: labelRuns(label, accent) })];
    if (arabic) {
      const isQ = kind === "kuran";
      const sz = isQ ? 30 : 28;
      const br = (t) => new TextRun({ text: t, rightToLeft: true, font: font(AMIRI), size: sz, sizeComplexScript: sz, color: accent });
      kids.push(new Paragraph({ bidirectional: true, alignment: AlignmentType.START, spacing: { before: 0, after: 120, line: 360, lineRule: LineRuleType.AUTO }, children: [
        br(isQ ? "﴿" : "«"),
        new TextRun({ text: arabic, rightToLeft: true, font: font(isQ ? HAFS : AMIRI), size: sz, sizeComplexScript: sz, color: "1A1A1A" }),
        br(isQ ? "﴾" : "»"),
      ] }));
    }
    if (turkish) kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 0, after: ref ? 80 : 0, ...LINE }, children: inline(turkish, { italics: true, size: 22 }) }));
    if (ref) kids.push(new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 0, after: 0 }, children: [new TextRun({ text: "— " + ref, size: 17, color: accent })] }));
    body.push(spacer(40));
    body.push(singleCellBox({ fill, border: accent, children: kids }));
    body.push(spacer(140));
  };

  for (const line of lines) {
    const [tag, ...f] = line.split("|");
    if (tag !== "ROW" && tag !== "TABLE" && tag !== "ENDTABLE") flushTable();
    switch (tag) {
      case "OUT": case "HEADER": break;
      case "COVER": cover(body, f, 2600); break;
      case "LEGEND": legend(body); break;
      case "H1":
        h1++; h2 = 0;
        body.push(new Paragraph({ keepNext: true, spacing: { before: 420, after: 160 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: TEAL, space: 4 } },
          children: [new TextRun({ text: `${h1}. `, bold: true, color: RED, size: 30 }), new TextRun({ text: f[0], bold: true, color: TEAL, size: 30 })] }));
        break;
      case "H2":
        h2++;
        body.push(new Paragraph({ keepNext: true, spacing: { before: 280, after: 80 },
          children: [new TextRun({ text: `${h1}.${h2}  `, bold: true, color: RED, size: 25 }), ...inline(f[0], { bold: true, color: BLUE, size: 25 })] }));
        break;
      case "INTRO":
        body.push(new Paragraph({ keepNext: true, alignment: AlignmentType.JUSTIFIED, spacing: { before: 0, after: 100, ...LINE },
          children: inline(f[0], { italics: true, color: GRAY }) }));
        break;
      case "B1": case "B2":
        body.push(new Paragraph({ numbering: { reference: "madde", level: tag === "B1" ? 0 : 1 }, alignment: AlignmentType.JUSTIFIED,
          spacing: { before: 0, after: 70, ...LINE }, children: inline(f[0], {}, { boldColor: tag === "B1" ? TEAL : RED }) }));
        break;
      case "KURAN": box("kuran", f[0], f[1], f[2], f[3]); break;
      case "HADIS": box("hadis", f[0], f[1], f[2], f[3]); break;
      case "KAVRAM": box("kavram", f[0], null, f[1], null); break;
      case "SOZ": box("soz", f[0], null, f[1], f[2]); break;
      case "TABLE": table = { header: f, rows: [] }; break;
      case "ROW":
        if (!table) throw new Error("TABLE olmadan ROW: " + line.slice(0, 60));
        table.rows.push(f); break;
      case "ENDTABLE": flushTable(); break;
      case "NOTE": body.push(...noteParagraphs(f.join("|"))); break;
      case "SRCH":
        body.push(new Paragraph({ keepNext: true, spacing: { before: 480, after: 160 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: TEAL, space: 4 } },
          children: [new TextRun({ text: f[0], bold: true, color: TEAL, size: 30 })] }));
        break;
      case "SRC": {
        const [author, title] = f[0].split(" — ");
        body.push(new Paragraph({ spacing: { before: 0, after: 50, line: 264, lineRule: LineRuleType.AUTO }, indent: { left: 300, hanging: 300 },
          children: [new TextRun({ text: "▸ ", font: font(SYM), color: RED, size: 20 }), new TextRun({ text: author, bold: true, color: TEAL, size: 21 }),
            new TextRun({ text: " — ", color: GRAY, size: 21 }), ...inline(title || "", { italics: true, size: 21 })] }));
        break;
      }
      case "CLOSE":
        body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 0 },
          border: { top: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 12 } },
          children: [new TextRun({ text: f[0], italics: true, color: GRAY, size: 22 })] }));
        break;
      default: throw new Error("Bilinmeyen etiket (özet): " + line.slice(0, 60));
    }
  }
  flushTable();

  return new Document({
    title: meta(lines, "COVER", "Geniş Özet").split("|")[1] || "Geniş Özet",
    styles: baseStyles,
    numbering: { config: [{ reference: "madde", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "●", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360, hanging: 270 } }, run: { color: RED, font: font(SYM), size: 16 } } },
      { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 760, hanging: 270 } }, run: { color: BLUE, font: font(SYM), size: 22 } } },
    ] }] },
    sections: [{ properties: sectionProps, ...headerFooter(meta(lines, "HEADER", "GENİŞ ÖZET")), children: body }],
  });
}

// ======================================================================
//  AÇIKLAMALI TAM METİN
// ======================================================================
function buildMetin(lines, fnLines) {
  const footnotes = {};
  for (const l of fnLines) {
    const m = l.match(/^FN\|(\d+)\|(.*)$/);
    if (!m) continue;
    footnotes[m[1]] = { children: m[2].split(" ¶ ").map((para, i) => new Paragraph({ alignment: AlignmentType.JUSTIFIED,
      spacing: { before: 0, after: 40, line: 240, lineRule: LineRuleType.AUTO }, children: inline((i === 0 ? " " : "") + para, { size: 17 }, { arSize: 19 }) })) };
  }
  const refs = lines.join(" ").match(/\[\^(\d+)\]/g) || [];
  const missing = refs.map((r) => r.slice(2, -1)).filter((n) => !footnotes[n]);
  if (missing.length) throw new Error("Metni olmayan dipnot işaretleri: " + missing.join(", "));

  const body = [];
  for (const line of lines) {
    const k = line.indexOf("|");
    const tag = k < 0 ? line.trim() : line.slice(0, k);
    const t = k < 0 ? "" : line.slice(k + 1);
    switch (tag) {
      case "OUT": case "HEADER": break;
      case "COVER": cover(body, t.split("|"), 2200); break;
      case "GUIDE": guide(body); break;
      case "H1":
        body.push(new Paragraph({ keepNext: true, alignment: AlignmentType.CENTER, spacing: { before: 360, after: 200 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: TEAL, space: 6 } },
          children: [new TextRun({ text: t, bold: true, color: TEAL, size: 27 })] }));
        break;
      case "H2":
        body.push(new Paragraph({ keepNext: true, alignment: AlignmentType.CENTER, spacing: { before: 240, after: 160 },
          children: [new TextRun({ text: t, bold: true, color: BLUE, size: 24 })] }));
        break;
      case "S":
        body.push(new Paragraph({ keepNext: true, spacing: { before: 120, after: 80, ...LINE }, indent: { firstLine: 284 },
          children: inline(t, { bold: true, color: TEAL }) }));
        break;
      case "P":
        body.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 0, after: 120, ...LINE }, indent: { firstLine: 284 },
          children: inline(t, {}, { boldColor: DARK }) }));
        break;
      case "L":
        body.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 0, after: 80, ...LINE }, indent: { left: 567 },
          children: inline(t, {}) }));
        break;
      case "A":
        body.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 40, after: 220, line: 276, lineRule: LineRuleType.AUTO },
          indent: { left: 284 },
          shading: { fill: "EEF4FA", type: ShadingType.CLEAR, color: "auto" },
          border: { left: { style: BorderStyle.SINGLE, size: 18, color: BLUE, space: 8 } },
          children: [new TextRun({ text: "(", bold: true, color: BLUE, size: 21 }), ...inline(t, { size: 21, color: "1F3A5F" }, { boldColor: RED }),
            new TextRun({ text: ")", bold: true, color: BLUE, size: 21 })] }));
        break;
      case "N": body.push(...noteParagraphs(t)); break;
      default: throw new Error("Bilinmeyen etiket (metin): " + line.slice(0, 60));
    }
  }
  return new Document({
    title: meta(lines, "COVER", "Açıklamalı Tam Metin").split("|")[1] || "Açıklamalı Tam Metin",
    styles: { ...baseStyles, paragraphStyles: [{ id: "FootnoteText", name: "footnote text", basedOn: "Normal", run: { size: 17 }, paragraph: { spacing: { after: 40, line: 240 } } }] },
    footnotes,
    sections: [{ properties: sectionProps, ...headerFooter(meta(lines, "HEADER", "Açıklamalı Tam Metin")), children: body }],
  });
}

(async () => {
  const jobs = [];
  if (WHICH !== "metin") {
    const L = linesOf(/^ozet.*\.txt$/i);
    if (L.length) jobs.push([meta(L, "OUT", "GENIS_OZET.docx"), buildOzet(L)]);
  }
  if (WHICH !== "ozet") {
    const L = linesOf(/^metin.*\.txt$/i);
    const fp = path.join(DIR, "dipnotlar.txt");
    const F = fs.existsSync(fp) ? fs.readFileSync(fp, "utf8").split(/\r?\n/).filter((l) => l.trim()) : [];
    if (L.length) jobs.push([meta(L, "OUT", "ACIKLAMALI_TAM_METIN.docx"), buildMetin(L, F)]);
  }
  if (!jobs.length) throw new Error("İçerik bulunamadı: " + DIR + " içinde ozet*.txt / metin*.txt yok");
  fs.mkdirSync(OUT, { recursive: true });
  for (const [name, doc] of jobs) {
    fs.writeFileSync(path.join(OUT, name), await Packer.toBuffer(doc));
    console.log("yazıldı:", path.join(OUT, name));
  }
})().catch((e) => { console.error("HATA:", e.message || e); process.exit(1); });
