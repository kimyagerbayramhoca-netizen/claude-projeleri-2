#!/bin/sh
# Taşma özetini sayfa başına en büyük alt kenar olarak verir (283mm altı = sığıyor)
cd "$(dirname "$0")/.." && node uretec/render.js "$@" 2>&1 | python3 -c "
import sys,re
mx={}
for l in sys.stdin:
  m=re.match(r'(s\d+): (.*?)alt=([\d.]+)',l)
  if m: mx[m.group(1)]=max(mx.get(m.group(1),0),float(m.group(3)))
  elif 'kutu' in l or 'sayfa' in l: print(l.strip()[:160])
print('alan dışı (en alt kenar, mm):',mx or 'yok')"
