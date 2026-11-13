"""Geniş Özet satır dosyalarını kayıtlı formata göre denetler.

Kullanım: python3 -I ozet_check.py [ch01 ch02 ... | onsoz | sonsoz]   (argümansız: ozet/ içindeki hepsi)
Çalışma klasöründen (ozet_in/ + ozet/) ya da depodaki kitap/kaynak/ klasöründen (ozet/, bolumler/, on-arka/, arapca/) çalıştırılır.
"""
import glob
import os
import re
import sys

TAGS = {"H2": 1, "INTRO": 1, "B1": 1, "B2": 1, "QUOTE": 1, "KAVRAM": 2, "SOZ": 3, "TABLE": None,
        "ROW": None, "ENDTABLE": 0, "NOTE": None}
AR = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
LABEL = re.compile(r"^[^.!?:\"“(]{1,38}:\s")   # "Etiket: içerik" kalıbı


def source_and_quotes(name):
    """Çalışma düzeninde ozet_in/, depo düzeninde bolumler/ + on-arka/ + arapca/quotes.json kullanılır."""
    if os.path.exists(f"ozet_in/{name}.md"):
        t = open(f"ozet_in/{name}.md").read()
        return re.sub(r"\[\[QUOTE[^\]]*\]\]", "", t), re.findall(r"\[\[QUOTE ([^ ]+) ", t)
    import json
    fn = {"onsoz": "on-arka/00_onsoz.md", "sonsoz": "on-arka/90_sonsoz.md"}.get(name, f"bolumler/{name}.md")
    t = open(fn).read()
    qs = [q["id"] for q in json.load(open("arapca/quotes.json")) if os.path.basename(q["file"]) == os.path.basename(fn)]
    return re.sub(r"(?m)^>.*\n?", "", t), qs


def check(name):
    out = f"ozet/{name}.txt"
    if not os.path.exists(out):
        return f"{name}: ozet/{name}.txt yok"
    prose_text, want = source_and_quotes(name)
    lines = open(out).read().split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    errs, got, table_cols = [], [], None
    counts = {}
    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            errs.append(f"satır {i}: boş satır")
            continue
        tag, _, rest = ln.partition("|")
        counts[tag] = counts.get(tag, 0) + 1
        if tag not in TAGS:
            errs.append(f"satır {i}: bilinmeyen etiket {tag!r}")
            continue
        f = rest.split("|") if rest else []
        n = TAGS[tag]
        if n is not None and len(f) != n and not (tag == "ENDTABLE" and not rest):
            errs.append(f"satır {i}: {tag} {n} alan ister, {len(f)} var")
        if tag in ("H2", "INTRO", "B1", "B2", "KAVRAM", "NOTE") and not rest.strip():
            errs.append(f"satır {i}: {tag} boş")
        if AR.search(ln):
            errs.append(f"satır {i}: Arapça harf")
        if "[^" in ln:
            errs.append(f"satır {i}: dipnot işareti kaldı")
        if tag in ("B1", "B2") and LABEL.match(rest):
            errs.append(f"satır {i}: 'Etiket: içerik' kalıbı: {rest[:50]!r}")
        if tag == "H2":
            nxt = lines[i] if i < len(lines) else ""
            if not nxt.startswith("INTRO|"):
                errs.append(f"satır {i}: H2'den sonra INTRO yok")
        if tag == "QUOTE":
            got.append(rest.strip())
        if tag == "KAVRAM" and not f[0].startswith("💡 KAVRAM · "):
            errs.append(f"satır {i}: KAVRAM etiketi '💡 KAVRAM · TERİM' biçiminde olmalı")
        if tag == "SOZ" and not f[0].startswith("💬 "):
            errs.append(f"satır {i}: SOZ etiketi '💬 ' ile başlamalı")
        if tag == "TABLE":
            table_cols = len(f)
            if table_cols < 2:
                errs.append(f"satır {i}: TABLE en az iki başlık ister")
        if tag == "ROW":
            if table_cols is None:
                errs.append(f"satır {i}: TABLE olmadan ROW")
            elif len(f) != table_cols:
                errs.append(f"satır {i}: ROW {len(f)} hücre, başlık {table_cols}")
        if tag == "ENDTABLE":
            table_cols = None
    if table_cols is not None:
        errs.append("kapanmamış TABLE")
    if got != want:
        miss = [q for q in want if q not in got]
        extra = [q for q in got if q not in want]
        errs.append(f"QUOTE sırası/eksik: eksik={miss} fazla={extra}" if (miss or extra) else "QUOTE sırası farklı")
    if name.startswith("ch") and lines and not lines[0].startswith("QUOTE|"):
        errs.append("ilk satır epigraf (QUOTE) olmalı")
    words = len(" ".join(lines).split())
    prose = len(prose_text.split())
    ratio = words / prose if prose else 0
    if ratio < 0.55:
        errs.append(f"çok kısa: düzyazının %{ratio*100:.0f}'i (hedef %65–85)")
    stat = (f"{words} kelime (%{ratio*100:.0f}) H2={counts.get('H2',0)} B1={counts.get('B1',0)} "
            f"B2={counts.get('B2',0)} TABLO={counts.get('TABLE',0)} KAVRAM={counts.get('KAVRAM',0)} "
            f"SÖZ={counts.get('SOZ',0)} QUOTE={len(got)}/{len(want)}")
    return f"{name}: {stat}  " + ("OK" if not errs else "SORUN:\n   " + "\n   ".join(errs[:15]))


names = sys.argv[1:] or sorted(os.path.basename(p)[:-4] for p in glob.glob("ozet/*.txt"))
for n in names:
    print(check(n))
