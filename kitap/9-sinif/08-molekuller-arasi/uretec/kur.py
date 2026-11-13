"""SVG'leri üretir, sablon.html'deki <!--SVG:ad--> yerlerine koyup ../kaynak.html'i yazar.
Kullanım (kitap/ klasöründen):  python3 9-sinif/08-molekuller-arasi/uretec/kur.py
Sonra:  python3 araclar/derle.py 9-sinif/08-molekuller-arasi
"""
import os
import re
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(D, 'svgler.py')], check=True, stdout=subprocess.DEVNULL)
s = open(os.path.join(D, 'sablon.html'), encoding='utf-8').read()
s = re.sub(r'<!--SVG:(\w+)-->', lambda m: open(os.path.join(D, 'svg', m.group(1) + '.svg'), encoding='utf-8').read(), s)
open(os.path.join(D, '..', 'kaynak.html'), 'w', encoding='utf-8').write(s)
print('kaynak.html yazıldı')
