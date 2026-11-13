#!/bin/bash
# SVG'leri üretip şablondan kaynak.html'i kurar, sonra üniteyi derler.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" && python3 svgler.py >/dev/null
python3 - "$D" <<'PY'
import re, sys
D = sys.argv[1]
s = open(D + '/sablon.html').read()
s = re.sub(r'<!--SVG:(\w+)-->', lambda m: open(f'{D}/svg/{m.group(1)}.svg').read(), s)
s = re.sub(r'\{(\d+)\}', r'<sub>\1</sub>', s)
open(D + '/../kaynak.html', 'w').write(s)
PY
cd "$D/../../.." && python3 araclar/derle.py 9-sinif/05-periyodik-ozellikler
