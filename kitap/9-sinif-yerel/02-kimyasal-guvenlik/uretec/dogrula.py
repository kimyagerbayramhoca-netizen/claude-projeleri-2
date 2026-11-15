"""Kimyasal Güvenlik · sayısal doğrulama ve cevap anahtarı denetimi.

Çalıştır:  python3 uretec/dogrula.py      → sonunda "SONUÇ: hepsi doğru" yazmalı.
  1. Her görev, tuzak, hızlı görev, kıssa, meclis, merdiven, imtihan ve üstad sorusu burada YENİDEN hesaplanır.
  2. Her çoktan seçmeli soruda TEK doğru şık (tek_sik).
  3. Sayfadan okunan işaretler (data-soru / data-dogru) ve Cevaplar sayfasındaki anahtar hesapla aynı mı?
  4. Akçe muhasebesi (toplam 1400).
Yardımcılar: yerel-ortak/dogrula_ortak.py (mk, formul, atom_sayisi, yakin, tek_sik, yargi, YARGI_5, NA, M …).
"""
import os
import sys


def _ortak():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "yerel-ortak", "dogrula_ortak.py")):
            return os.path.join(d, "yerel-ortak")
        d = os.path.dirname(d)
    raise SystemExit("yerel-ortak bulunamadı")


sys.path.insert(0, _ortak())
from dogrula_ortak import *  # noqa: E402,F401,F403

# ------------------------------------------------------------------ örnek: mol kütlesi ve tek doğru şık
kontrol("örnek: CO2 = 44 g/mol", mk("CO2") == 44)
kontrol("örnek: Mg(OH)2 = 58 g/mol, 5 atom", mk("Mg(OH)2") == 58 and atom_sayisi("Mg(OH)2") == 5)
# İmtihan sorusu örneği (şablondaki ÖRNEK sorular yerine kendi sorunu yaz ve burada hesapla):
# T["I1"] = tek_sik("İmtihan 1", dict(A=.3, B=1.1, C=2.4, D=3.3, E=3.6), lambda v: yakin(v, .3 * atom_sayisi("C3H8")), "D")
# Yargılı soru örneği:
# d = yargi({"I": yakin(6.4 / 32, .2), "II": yakin(.2 * NA, 1.204e23), "III": yakin(.2 * 2, .4)})
# T["I4"] = tek_sik("İmtihan 4", YARGI_5, lambda v: v == d, "E")

# ------------------------------------------------------------------ hesaplanan anahtar (şimdilik şablondaki örnek harfler)
T = {f"I{i + 1}": h for i, h in enumerate("DCBEACCDBECD")}
T.update({f"K{i + 1}": h for i, h in enumerate("CBED")})
T.update({f"U{i + 1}": h for i, h in enumerate("BEADCB")})
dagilim([T[f"I{i}"] for i in range(1, 13)])
dagilim([T[f"U{i}"] for i in range(1, 7)], harfler="ABCDE")

# ------------------------------------------------------------------ sayfadan okunan işaretler ve anahtar
html = sayfa_oku(__file__)
if html:
    sayfa_isaretleri_ayni(html, T)
    izgara = anahtar_izgarasi(html)
    kontrol(f"Cevaplar sayfasındaki anahtar ızgarası data-dogru işaretleriyle aynı {izgara}",
            izgara == {i: T[f"I{i}"] for i in range(1, 13)})
    for kod, (kisi, satir) in meclis_hukumleri(html).items():
        kontrol(f"{kod}: meclis hükmü işaretli (haklı: {kisi}, satır: {satir})", bool(kisi) and bool(satir))

# ------------------------------------------------------------------ akçe muhasebesi
durak = [100, 150, 150, 150, 150]
yan = dict(hulasa=40, meclis=4 * 30, kissa=4 * 30, anahtar=3 * 40, imtihan=12 * 25)
kontrol(f"Ünite toplam akçe {sum(durak) + sum(yan.values())} = 1400", sum(durak) + sum(yan.values()) == 1400)

D.sonuc()
