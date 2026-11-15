"""Hazine kartları KESME YAPRAĞI: meta.json'daki bütün H kartları tek A4 sayfada (kur.py --hazine → hazine-kartlari.html).

Kartlar sayfadaki `.hazine` bileşeninin aynısıdır (aynı yer tutucu: kur_ortak.Unite.yt_hazine), 1,3 kat büyütülür.
Her hücrede yol adı ve kartın durağı yazar; hücreler kesik çizgiyle ayrılır, her kesim çizgisinin başında makas vardır.
10 karta kadar 2 × 5, 14'e kadar 2 × 7, daha çoksa 3 sütun.
"""
import math
import os

from kur_ortak import ORTAK, ortak_defs, zengin


def yaprak_html(u):
    m = u.meta
    kartlar = m["hazine"]
    n = len(kartlar)
    sutun = 2 if n <= 14 else 3
    satir = max(1, math.ceil(n / sutun))
    u.sayac = 0
    hucre = []
    for i, h in enumerate(kartlar):
        durak = f'{h["durak"]}. durak · ' if h.get("durak") else ""
        sag = (i % sutun) == sutun - 1
        alt = (i // sutun) == satir - 1
        stil = "".join(s for s, k in (("border-right:0;", sag), ("border-bottom:0;", alt)) if k)
        hucre.append(f'<div class="hy-hucre"{f" style={chr(34)}{stil}{chr(34)}" if stil else ""}>'
                     f'<div class="hy-ust"><span>Yol {m["yol"]} · {zengin(m["rota"])}</span><span>{durak}{h["kod"]}</span></div>'
                     f'<div class="hy-kart{" uzun" if h.get("adimlar") else ""}">{u.yt_hazine(h["kod"])}</div></div>')
    for _ in range(satir * sutun - n):     # boş hücreler (son satır)
        hucre.append('<div class="hy-hucre bos" style="border-bottom:0"></div>')
    makas = [f'<svg class="hy-makas yatay" viewBox="0 0 24 24" style="top:calc({k} / {satir} * 100% - 2.6mm)"><use href="#i-makas"/></svg>' for k in range(1, satir)]
    makas += [f'<svg class="hy-makas dikey" viewBox="0 0 24 24" style="left:calc({k} / {sutun} * 100% - 2.6mm)"><use href="#i-makas"/></svg>' for k in range(1, sutun)]
    makas.append('<svg class="hy-makas kose" viewBox="0 0 24 24"><use href="#i-makas"/></svg>')
    stil_yolu = os.path.relpath(os.path.join(ORTAK, "stil.css"), u.klasor).replace(os.sep, "/")
    sinif = u.sinif_adi
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>{sinif} · {m["unite"]} · hazine kartları</title>
<link rel="stylesheet" href="{stil_yolu}">
</head>
<body>
<!-- Bu dosya uretec/meta.json'dan kur.py --hazine ile üretilir; elle düzenleme. -->
{ortak_defs(u.ek_defs)}
<section class="sayfa hazine-yaprak">
  {u.yt["zemin"]()}
  <header class="hy-bas">
    <svg class="hy-logo" viewBox="0 0 24 24"><use href="#logo-yildiz"/></svg>
    <div><div class="et keh">{sinif} · Yol {m["yol"]} · {zengin(m["rota"])}</div><h1>Hazine kartları · <em>{zengin(m["unite"])}</em></h1>
      <p>Kesik çizgilerden kes; her kartı durağının sayfasına ya da defterine yapıştır. Kart başı +10 akçe.</p></div>
    <div class="hy-sayi"><svg viewBox="0 0 40 40"><use href="#akce"/></svg><b>{n}</b><small>kart</small></div>
  </header>
  <div class="hy-izgara" style="grid-template-columns:repeat({sutun},1fr);grid-template-rows:repeat({satir},1fr)">
    {"".join(hucre)}
    {"".join(makas)}
  </div>
  <footer class="hy-alt"><span>{sinif} · {zengin(m["unite"])}</span><span>Hazine sandığı · {n} kart</span></footer>
</section>
</body>
</html>
"""
