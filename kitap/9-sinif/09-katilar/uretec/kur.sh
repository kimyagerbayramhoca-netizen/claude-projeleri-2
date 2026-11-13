#!/bin/bash
# SVG'leri üretip şablondan kaynak.html'i kurar, sonra üniteyi derler.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" && python3 svgler.py >/dev/null
python3 - "$D" <<'PY'
import re, sys
D = sys.argv[1]
s = open(D + '/sablon.html', encoding='utf-8').read()
s = re.sub(r'<!--SVG:(\w+)-->', lambda m: open(f'{D}/svg/{m.group(1)}.svg', encoding='utf-8').read(), s)
open(D + '/../kaynak.html', 'w', encoding='utf-8').write(s)
PY
cd "$D/../../.." && python3 araclar/derle.py 9-sinif/09-katilar
