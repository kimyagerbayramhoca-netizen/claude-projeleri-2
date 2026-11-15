#!/bin/sh
# Taşma özeti: sayfa başına "alan dışı" en alt kenar ve kutu taşmaları (boşsa her şey sığıyor).
# Kullanım: bash uretec/olc.sh          → bütün sayfalar (PDF de yazılır)
#           bash uretec/olc.sh 3 4      → yalnızca 3. ve 4. sayfanın PNG'si
cd "$(dirname "$0")/.." && node ../../yerel-ortak/render.js . "$@" 2>&1 | python3 -c "
import sys,re
mx={}
for l in sys.stdin:
  m=re.match(r'(s\d+): alan dışı .*?alt=([\d.]+)',l)
  if m: mx[m.group(1)]=max(mx.get(m.group(1),0),float(m.group(2)))
  elif 'kutu' in l or 'kenar' in l or 'sayfa' in l or 'MB' in l or 'HATA' in l: print(l.strip()[:160])
print('alan dışı (en alt kenar, mm):',mx or 'yok')"
