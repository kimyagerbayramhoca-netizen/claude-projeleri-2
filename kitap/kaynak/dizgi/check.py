"""Bölüm dosyalarını kılavuza göre denetler."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(glob.glob(os.path.join(ROOT, "bolumler", "ch*.md")))
problems = 0
total = 0
for f in files:
    n = int(re.search(r"ch(\d+)", f).group(1))
    t = open(f).read()
    words = len(t.split())
    total += words
    issues = []
    lines = t.split("\n")
    first = next((l for l in lines if l.strip()), "")
    if not re.match(rf"^# {n}\. \S", first):
        issues.append(f"ilk satır '# {n}. Başlık' değil: {first[:60]!r}")
    if len(re.findall(r"^# ", t, re.M)) != 1:
        issues.append("birden fazla '# ' başlık")
    h2 = re.findall(r"^## (.+)$", t, re.M)
    if not any("İbret" in h for h in h2):
        issues.append("'Bu Bölümün İbretleri' yok")
    if re.search(r"[؀-ۿﭐ-﷿ﹰ-﻿]", t):
        issues.append("Arapça harf var")
    refs = re.findall(r"\[\^([^\]]+)\](?!:)", t)
    defs = re.findall(r"^\[\^([^\]]+)\]:", t, re.M)
    bad = [r for r in set(refs) | set(defs) if not r.startswith(f"{n}-")]
    if bad:
        issues.append(f"dipnot etiketi bölüm no ile başlamıyor: {sorted(bad)[:5]}")
    undef = sorted(set(refs) - set(defs))
    unused = sorted(set(defs) - set(refs))
    if undef:
        issues.append(f"tanımsız dipnot: {undef[:5]}")
    if unused:
        issues.append(f"kullanılmayan dipnot: {unused[:5]}")
    if len(defs) != len(set(defs)):
        issues.append("tekrarlanan dipnot tanımı")
    bullets = len(re.findall(r"^\s*[-*+] \S", t, re.M))
    if bullets > 12:
        issues.append(f"çok fazla madde işareti ({bullets})")
    if re.search(r"<[a-zA-Z/][^>]*>", t):
        issues.append("HTML etiketi var")
    if re.search(r"^\|.*\|$", t, re.M):
        issues.append("tablo var")
    if "ﷺ" in t:
        issues.append("ﷺ sembolü var")
    lo, hi = (2500, 3800) if n == 1 else (3300, 6300)
    if not lo <= words <= hi:
        issues.append(f"kelime sayısı aralık dışı ({words})")
    quotes = len(re.findall(r"^> [—–]", t, re.M))
    print(f"ch{n:02d} {words:6d} kelime  {len(defs):3d} dipnot  {quotes:3d} alıntı  {len(h2):2d} alt başlık  "
          + ("OK" if not issues else "SORUN: " + " | ".join(issues)))
    problems += bool(issues)
missing = sorted(set(range(1, 26)) - {int(re.search(r"ch(\d+)", f).group(1)) for f in files})
print(f"\nToplam {total} kelime, {len(files)} bölüm. Eksik: {missing or 'yok'}. Sorunlu bölüm: {problems}")
