#!/bin/sh
# Ünite klasöründen çalıştır: sh uretec/kur.sh <onizleme-klasoru>
set -e
python3 uretec/denetle.py | tail -1
python3 uretec/uret.py
cd ../..
python3 araclar/derle.py 9-sinif/07-adlandirma
[ -n "$1" ] && node araclar/pdf.js 9-sinif/07-adlandirma/unite.html /dev/null "$1"
true
