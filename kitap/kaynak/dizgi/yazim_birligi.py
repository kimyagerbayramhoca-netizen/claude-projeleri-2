"""Kitap genelinde isim ve eser adı yazımlarını tekleştirir (yalnızca Latin harfli metin; Arapçaya dokunmaz).

Kullanım: python3 -I yazim_birligi.py <kök>   (kök: ozet/, chapters|bolumler/, front|on-arka/, ar|arapca/ içerir)
"""
import glob
import json
import os
import re
import sys

ROOT = sys.argv[1]
RULES = [
    # İA usulü uzatma işaretleri -> kitabın kılavuzundaki düzeltme işaretleri
    (r"ā", "â"), (r"ī", "î"), (r"ū", "û"), (r"Ā", "Â"), (r"Ī", "Î"), (r"Ū", "Û"),
    (r"\bRasulullah\b", "Rasûlullah"), (r"Rasûlullâh", "Rasûlullah"),
    (r"\bEbu'", "Ebü'"), (r"\bEbu\b(?!')", "Ebû"), (r"\bEbi\b", "Ebî"),
    (r"\bMedîne\b", "Medine"),
    (r"\bİbrahim\b", "İbrâhim"), (r"\bel-Aliy\b", "el-Alî"), (r"\bSahîhü's-Sîre", "Sahîhu's-Sîre"),
    (r"\bAbbâs\b(?!î)", "Abbas"), (r"\bAbbasî", "Abbâsî"),
    (r"\bBeni (?=[A-ZÂÎÛÇĞİÖŞÜ])", "Benî "),
    (r"Ümeyr b\. Ebû Vakkâs", "Umeyr b. Ebî Vakkâs"), (r"\bÜmeyr\b", "Umeyr"),
    (r"\bSelman\b", "Selmân"), (r"\bİshak\b", "İshâk"), (r"\bİsmail\b", "İsmâil"),
    (r"\bAbdurrahmân\b", "Abdurrahman"), (r"\bKubâ\b", "Kuba"), (r"\bSaid\b", "Saîd"),
    (r"\bKayyım\b", "Kayyim"), (r"\bMuhacir", "Muhâcir"), (r"\bMabed\b", "Ma'bed"),
    (r"\bRâfi\b(?!')", "Râfi'"), (r"\bSuheyb\b", "Süheyb"), (r"\bMina\b", "Minâ"),
    (r"\bHâtib b\.", "Hâtıb b."), (r"\bAbdurrezzâk\b", "Abdürrezzâk"),
    (r"\bel-Esas\b", "el-Esâs"), (r"\bEşas b\. Kays\b", "Şâs b. Kays"), (r"\bFenhas\b", "Finhâs"),
    (r"\bHubel\b", "Hübel"), (r"\bHilfü'l", "Hilfu'l"), (r"\bMecusî", "Mecûsî"),
    (r"\bUneys\b", "Üneys"), (r"\bSimme\b", "Sımme"), (r"\bBabil\b", "Bâbil"),
    (r"\bKulleys\b", "Külleys"), (r"\bHuzeyl\b", "Hüzeyl"), (r"\bİsrailoğulları", "İsrâiloğulları"),
    (r"\bNufeyl\b", "Nüfeyl"), (r"\bRum\b", "Rûm"), (r"\bKâ'b\b", "Ka'b"), (r"\bNâ'ile\b", "Nâile"),
    (r"Mut'im b\. Adî\b", "Mut'im b. Adiy"), (r"Sa'd b\. Rebî\b(?!')", "Sa'd b. Rebî'"),
]
COMP = [(re.compile(a), b) for a, b in RULES]
AR = re.compile(r"[؀-ۿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
counts = {}


def norm(t):
    for (rx, b), (a, _) in zip(COMP, RULES):
        t, n = rx.subn(b, t)
        if n:
            counts[a] = counts.get(a, 0) + n
    return t


def first(*names):
    for n in names:
        if os.path.isdir(os.path.join(ROOT, n)):
            return os.path.join(ROOT, n)
    return None


changed = 0
for d, pat in ((first("ozet"), "*.txt"), (first("chapters", "bolumler"), "*.md"), (first("front", "on-arka"), "*.md")):
    if not d:
        continue
    for f in sorted(glob.glob(os.path.join(d, pat))):
        old = open(f).read()
        new = norm(old)
        if new != old:
            open(f, "w").write(new)
            changed += 1
ard = first("ar", "arapca")
if ard:
    for name, fields in (("quotes.json", ("tr", "src")), ("konu.json", None), ("soz.json", ("label", "ref"))):
        p = os.path.join(ard, name)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        if isinstance(d, list):
            for q in d:
                for k in fields:
                    q[k] = norm(q[k])
        else:
            for k, v in d.items():
                if isinstance(v, str):
                    d[k] = norm(v)
                else:
                    for kk in fields:
                        if v.get(kk):
                            v[kk] = norm(v[kk])
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
    kp = os.path.join(ard, "kaynaklar.txt")
    if os.path.exists(kp):
        open(kp, "w").write(norm(open(kp).read()))
print("değişen dosya:", changed)
for a, n in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {n:4d}  {a}")
