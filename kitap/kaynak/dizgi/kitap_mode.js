// ======================================================================
//  KİTAP — Geniş Özet görünümü + düzyazı paragraflar, dipnotlar, kısım sayfaları, içindekiler
//  Etiketler: COVER LEGEND TOC PART H1 UH1 H2 H3 INTRO P L B1 B2 KURAN HADIS KAVRAM SOZ
//             TABLE ROW ENDTABLE NOTE SRCH SRC CLOSE PB   (+ dipnotlar.txt: FN|n|metin)
// ======================================================================
function buildKitap(lines, fnLines) {
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
  let h1 = 0, h2 = 0, table = null;

  const flushTable = () => { // Geniş Özet tablosuyla aynı
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

  const box = (kind, label, arabic, turkish, ref) => { // Geniş Özet kutusuyla aynı
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

  const tealRule = { bottom: { style: BorderStyle.SINGLE, size: 10, color: TEAL, space: 4 } };

  for (const line of lines) {
    const k = line.indexOf("|");
    const tag = k < 0 ? line.trim() : line.slice(0, k);
    const rest = k < 0 ? "" : line.slice(k + 1);
    const f = rest.split("|");
    if (tag !== "ROW" && tag !== "TABLE" && tag !== "ENDTABLE") flushTable();
    switch (tag) {
      case "OUT": case "HEADER": break;
      case "COVER": cover(body, f, 2600); break;
      case "LEGEND": legend(body); break;
      case "TOC":
        body.push(new Paragraph({ keepNext: true, spacing: { before: 0, after: 200 }, border: tealRule,
          children: [new TextRun({ text: f[0], bold: true, color: TEAL, size: 30 })] }));
        body.push(new TableOfContents(f[0], { hyperlink: true, headingStyleRange: "1-2" }));
        break;
      case "PART": { // kısım sayfası: kapak etiketi + başlık + altın çizgi + açıklama
        const [label, title, desc] = f;
        body.push(pageBreak());
        body.push(spacer(3400));
        body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, keepNext: true, alignment: AlignmentType.CENTER,
          spacing: { before: 0, after: 80 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 10 } },
          children: [new TextRun({ text: label, bold: true, color: RED, size: 26, characterSpacing: 120 }),
            new TextRun({ text: title, bold: true, color: TEAL, size: 48, break: 1 })] }));
        if (desc) body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 240, after: 0 }, indent: { left: 900, right: 900 },
          children: inline(desc, { italics: true, color: GRAY, size: 24 }) }));
        break;
      }
      case "H1": // bölüm: yeni sayfa, kırmızı numara + petrol mavisi başlık
        h1++; h2 = 0;
        body.push(new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: true, keepNext: true, spacing: { before: 240, after: 200 }, border: tealRule,
          children: [new TextRun({ text: `${h1}. `, bold: true, color: RED, size: 30 }), new TextRun({ text: f[0], bold: true, color: TEAL, size: 30 })] }));
        break;
      case "UH1": // numarasız bölüm (Önsöz, Sonsöz, Kronoloji)
        body.push(new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: true, keepNext: true, spacing: { before: 240, after: 200 }, border: tealRule,
          children: [new TextRun({ text: f[0], bold: true, color: TEAL, size: 30 })] }));
        break;
      case "H2":
        h2++;
        body.push(new Paragraph({ keepNext: true, spacing: { before: 280, after: 80 },
          children: [new TextRun({ text: `${h1}.${h2}  `, bold: true, color: RED, size: 25 }), ...inline(f[0], { bold: true, color: BLUE, size: 25 })] }));
        break;
      case "H3":
        body.push(new Paragraph({ keepNext: true, spacing: { before: 160, after: 60, ...LINE }, children: inline(rest, { bold: true, color: TEAL }) }));
        break;
      case "INTRO":
        body.push(new Paragraph({ keepNext: true, alignment: AlignmentType.JUSTIFIED, spacing: { before: 0, after: 100, ...LINE },
          children: inline(rest, { italics: true, color: GRAY }) }));
        break;
      case "P":
        body.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 0, after: 120, ...LINE }, indent: { firstLine: 284 },
          children: inline(rest, {}, { boldColor: DARK }) }));
        break;
      case "L":
        body.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 0, after: 80, ...LINE }, indent: { left: 567 },
          children: inline(rest, {}) }));
        break;
      case "B1": case "B2":
        body.push(new Paragraph({ numbering: { reference: "madde", level: tag === "B1" ? 0 : 1 }, alignment: AlignmentType.JUSTIFIED,
          spacing: { before: 0, after: 70, ...LINE }, children: inline(rest, {}, { boldColor: tag === "B1" ? TEAL : RED }) }));
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
      case "SRCH":
        body.push(new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: true, keepNext: true, spacing: { before: 240, after: 160 }, border: tealRule,
          children: [new TextRun({ text: f[0], bold: true, color: TEAL, size: 30 })] }));
        break;
      case "SRC": { // "Müellif — Eser"; müellifsiz satır "— Eser" yalnızca eser adıyla basılır
        let [author, title] = rest.split(" — ");
        if (title === undefined && /^—\s*/.test(author)) { title = author.replace(/^—\s*/, ""); author = ""; }
        const kids = [new TextRun({ text: "▸ ", font: font(SYM), color: RED, size: 20 })];
        if (author) kids.push(new TextRun({ text: author, bold: true, color: TEAL, size: 21 }), new TextRun({ text: " — ", color: GRAY, size: 21 }));
        kids.push(...inline(title || "", { italics: true, size: 21 }));
        body.push(new Paragraph({ spacing: { before: 0, after: 50, line: 264, lineRule: LineRuleType.AUTO }, indent: { left: 300, hanging: 300 }, children: kids }));
        break;
      }
      case "CLOSE":
        body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 0 },
          border: { top: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 12 } },
          children: [new TextRun({ text: rest, italics: true, color: GRAY, size: 22 })] }));
        break;
      case "NOTE": body.push(...noteParagraphs(rest)); break;
      case "PB": body.push(pageBreak()); break;
      default: throw new Error("Bilinmeyen etiket (kitap): " + line.slice(0, 60));
    }
  }
  flushTable();

  const neutralHeading = (id, name, lvl) => ({ id, name, basedOn: "Normal", next: "Normal", quickFormat: true,
    run: { font: BODY, size: 22, color: DARK, bold: false, italics: false }, paragraph: { outlineLevel: lvl, spacing: LINE } });
  return new Document({
    title: meta(lines, "COVER", "Kitap").split("|")[1] || "Kitap",
    features: { updateFields: true },
    styles: { ...baseStyles, paragraphStyles: [
      { id: "FootnoteText", name: "footnote text", basedOn: "Normal", run: { size: 17 }, paragraph: { spacing: { after: 40, line: 240 } } },
      neutralHeading("Heading1", "heading 1", 0), neutralHeading("Heading2", "heading 2", 1),
    ] },
    numbering: { config: [{ reference: "madde", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "●", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360, hanging: 270 } }, run: { color: RED, font: font(SYM), size: 16 } } },
      { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 760, hanging: 270 } }, run: { color: BLUE, font: font(SYM), size: 22 } } },
    ] }] },
    footnotes,
    sections: [{ properties: sectionProps, ...headerFooter(meta(lines, "HEADER", "")), children: body }],
  });
}
