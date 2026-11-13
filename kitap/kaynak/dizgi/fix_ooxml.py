"""docx içindeki XML öğelerini OOXML şemasındaki sıraya dizer (Word uyumluluğu için).

Kullanım: python3 fix_ooxml.py <dosya.docx>   (dosyayı yerinde günceller)
"""
import shutil
import sys
import tempfile
import zipfile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def q(t):
    return f"{{{W}}}{t}"


PPR = """pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr
shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi
adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection
textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange""".split()
RPR = """rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint noProof
snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u effect bdr shd fitText
vertAlign rtl cs em lang eastAsianLayout specVanish oMath""".split()
SECT = """headerReference footerReference footnotePr endnotePr type pgSz pgMar paperSrc pgBorders lnNumType
pgNumType cols formProt vAlign noEndnote titlePg textDirection bidi rtlGutter docGrid printerSettings
sectPrChange""".split()
STYLE = """name aliases basedOn next link autoRedefine hidden uiPriority semiHidden unhideWhenUsed qFormat
locked personal personalCompose personalReply rsid pPr rPr tblPr trPr tcPr tblStylePr""".split()
FNPR = "pos numFmt numStart numRestart footnote".split()
SETTINGS = """writeProtection view zoom removePersonalInformation removeDateAndTime doNotDisplayPageBoundaries
displayBackgroundShape printPostScriptOverText printFractionalCharacterWidth printFormsData
embedTrueTypeFonts embedSystemFonts saveSubsetFonts saveFormsData mirrorMargins alignBordersAndEdges
bordersDoNotSurroundHeader bordersDoNotSurroundFooter gutterAtTop hideSpellingErrors hideGrammaticalErrors
activeWritingStyle proofState formsDesign attachedTemplate linkStyles stylePaneFormatFilter
stylePaneSortMethod documentType mailMerge revisionView trackRevisions doNotTrackMoves
doNotTrackFormatting documentProtection autoFormatOverride styleLockTheme styleLockQFSet defaultTabStop
autoHyphenation consecutiveHyphenLimit hyphenationZone doNotHyphenateCaps showEnvelope
summaryLength clickAndTypeStyle defaultTableStyle evenAndOddHeaders bookFoldRevPrinting bookFoldPrinting
bookFoldPrintingSheets drawingGridHorizontalSpacing drawingGridVerticalSpacing
displayHorizontalDrawingGridEvery displayVerticalDrawingGridEvery doNotUseMarginsForDrawingGridOrigin
drawingGridHorizontalOrigin drawingGridVerticalOrigin doNotShadeFormData noPunctuationKerning
characterSpacingControl printTwoOnOne strictFirstAndLastChars noLineBreaksAfter noLineBreaksBefore
savePreviewPicture doNotValidateAgainstSchema saveInvalidXml ignoreMixedContent
alwaysShowPlaceholderText doNotDemarcateInvalidXml saveXmlDataOnly useXSLTWhenSaving saveThroughXslt
showXMLTags alwaysMergeEmptyNamespace updateFields hdrShapeDefaults footnotePr endnotePr compat docVars
rsids mathPr attachedSchema themeFontLang clrSchemeMapping doNotIncludeSubdocsInStats
doNotAutoCompressPictures forceUpgrade captions readModeInkLockDown smartTagType schemaLibrary
shapeDefaults doNotEmbedSmartTags decimalSymbol listSeparator""".split()

TBLPR = """tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc
tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription""".split()
TRPR = """cnfStyle divId gridBefore gridAfter wBefore wAfter cantSplit trHeight tblHeader tblCellSpacing jc
hidden ins del trPrChange""".split()

TCPR = """cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign
hideMark headers cellIns cellDel cellMerge tcPrChange""".split()

ORDERS = {q("tcPr"): TCPR, q("pPr"): PPR, q("rPr"): RPR, q("sectPr"): SECT, q("style"): STYLE,
          q("footnotePr"): FNPR, q("settings"): SETTINGS, q("tblPr"): TBLPR, q("trPr"): TRPR}


M = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def reorder(el, order):
    idx = {q(n): i for i, n in enumerate(order)}
    if "mathPr" in order:
        idx[f"{{{M}}}mathPr"] = order.index("mathPr")
    kids = list(el)
    known = [k for k in kids if isinstance(k.tag, str) and k.tag in idx]
    if not known:
        return
    # yalnızca şemada tanımlı W öğelerini sırala; diğerlerini (ör. mc:, w14:) sona bırak
    other = [k for k in kids if not (isinstance(k.tag, str) and k.tag in idx)]
    known.sort(key=lambda k: idx[k.tag])
    for k in kids:
        el.remove(k)
    for k in known + other:
        el.append(k)


def dedupe(el, tag):
    seen = el.findall(q(tag))
    for extra in seen[1:]:
        el.remove(extra)


def fix_tree(root):
    for tag, order in ORDERS.items():
        for el in root.iter(tag):
            # rPr içinde sözde 'rPr' (paragraf işaretinin rPr'ı) ile run rPr aynı sırayı paylaşır
            reorder(el, order)
            if tag == q("rPr"):
                # rPr yalnızca öğe içerir: yanlışlıkla kalan metni temizle
                el.text = None
                for k in el:
                    k.tail = None
    for mar in root.iter(q("pgMar")):
        for a in ("top", "right", "bottom", "left", "header", "footer", "gutter"):
            if mar.get(q(a)) is None:
                mar.set(q(a), "0")
    for sp in root.iter(q("sectPr")):
        for t in ("pgNumType", "titlePg", "footnotePr"):
            dedupe(sp, t)
    for nsid in root.iter(q("nsid")):
        v = nsid.get(q("val"))
        if v and len(v) < 8:
            nsid.set(q("val"), v.rjust(8, "0").upper())
    for tmpl in root.iter(q("tmpl")):
        v = tmpl.get(q("val"))
        if v and len(v) < 8:
            tmpl.set(q("val"), v.rjust(8, "0").upper())


def main(path):
    targets = {"word/document.xml", "word/styles.xml", "word/settings.xml", "word/numbering.xml",
               "word/footnotes.xml"}
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    tmp.close()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in targets:
                root = etree.fromstring(data)
                fix_tree(root)
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            zout.writestr(item, data)
    shutil.move(tmp.name, path)
    print("düzeltildi:", path)


if __name__ == "__main__":
    main(sys.argv[1])
