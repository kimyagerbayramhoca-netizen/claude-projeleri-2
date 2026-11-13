#!/usr/bin/env bash
# Kitabı kayıtlı Geniş Özet tasarımıyla derler: Markdown -> satır biçimi -> .docx (gömülü KFGQPC) -> PDF
# Kullanım: bash derle.sh <kök: chapters/ front/ ar/ içeren klasör> <çıktı_klasörü>
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$1"; OUT="$2"; FONT="${FONT:-$HOME/.fonts/UthmanicHafs-v-3.0.ttf}"
mkdir -p "$OUT/icerik"
# BICIM=ozet (varsayılan): Geniş Özet maddeleri (ozet/*.txt) · BICIM=duzyazi: düzyazı bölümler
if [ "${BICIM:-ozet}" = "duzyazi" ]; then
  python3 -I "$HERE/md2kitap.py" "$ROOT" "$OUT/icerik"
else
  python3 -I "$HERE/ozet2kitap.py" "$ROOT" "$OUT/icerik"
fi
NODE_PATH="$(npm root -g)" node "$HERE/kitap_build.js" "$OUT/icerik" "$OUT" kitap
DOCX="$OUT/Alemlere_Rahmet_Siyer-i_Nebi.docx"
python3 -I "$HERE/embed_font.py" "$DOCX" "$FONT" "KFGQPC HAFS Uthmanic Script"
python3 -I "$HERE/fix_ooxml.py" "$DOCX"
python3 "$HERE/to_pdf.py" "$DOCX" "${DOCX%.docx}.pdf"
