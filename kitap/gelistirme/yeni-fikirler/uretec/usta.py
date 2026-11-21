"""Ustanın Sırrı · ebru: kurgusal Revnak Usta, tekne sahnesi ve üç "sır" şeması.

Revnak Usta kurgusaldır; gerçek bir kişiye benzetilmedi (genel çizim: gri topuz saç, yuvarlak gözlük, önlük).
Bilgiler (WebSearch ile doğrulandı, README'de kaynaklar): tekne suyu kitreyle koyulaştırılır; boyaya öd katılır,
öd yüzey gerilimini düşürür (ödsüz boya yayılmaz, batar); boyalar suda çözünmeyen doğal pigmentlerdir;
"Geleneksel Türk Ebru Sanatı" 2014'te UNESCO Temsilî Listesi'ne alındı; ebru ustadan çırağa aktarılır.
"""
import math
import random

OBS, KAR, KIREC = "#1B1D26", "#FBFDFD", "#FFFDF7"
GOL, GOLA, KEH, KEHA, MER, MERA, KOB, KOBA = "#13A3A6", "#DCF3F1", "#F0A21A", "#FFF0CF", "#E2533D", "#FDE7E1", "#2B50B5", "#E6ECFB"
ALTIN, ALTINA, ZUM, ERG, GUM, GUMA, LAJ = "#C9952B", "#F6E7BF", "#1F8A5B", "#7B3F8C", "#A3B3BE", "#EDF2F5", "#1D3A8A"
TEN, SAC, ONLUK = "#E9BE9C", "#C9CCD3", "#2B50B5"
EBRU_RENK = [MER, KOB, KEH, ZUM, ERG, "#E86A92", "#3E8FD0", "#F2C84B"]


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _tas(rng, cx, cy, rx, ry, n=26, onek="e"):
    """battal ebru: üst üste binmiş halkalı taşlar (yüzeyin elipsi içinde)."""
    o = []
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        r = math.sqrt(rng.uniform(0, 1))
        x, y = cx + rx * .92 * r * math.cos(a), cy + ry * .9 * r * math.sin(a)
        R = rng.uniform(.07, .17) * rx
        renk = rng.choice(EBRU_RENK)
        o.append(f'<ellipse cx="{_f(x)}" cy="{_f(y)}" rx="{_f(R)}" ry="{_f(R * ry / rx)}" fill="{renk}" stroke="{OBS}" stroke-width=".6" opacity=".93"/>'
                 f'<ellipse cx="{_f(x)}" cy="{_f(y)}" rx="{_f(R * .55)}" ry="{_f(R * .55 * ry / rx)}" fill="none" stroke="#fff" stroke-width=".9" opacity=".75"/>')
    return "".join(o)


def usta():
    """Revnak Usta tekne başında (fırçadan boya serpiyor). viewBox 0 0 290 260."""
    rng = random.Random(14)
    o = ['<svg viewBox="0 0 290 260" xmlns="http://www.w3.org/2000/svg">',
         '<defs><clipPath id="ust-yuzey"><ellipse cx="150" cy="196" rx="118" ry="34"/></clipPath></defs>',
         f'<rect x="0" y="0" width="290" height="260" rx="10" fill="{GOLA}"/>',
         f'<path d="M0 150 H290 V260 H0 Z" fill="{ALTINA}"/>']
    # usta: gövde, önlük, kollar, baş
    o.append(f'<path d="M92 196 C92 140 104 108 150 104 C196 108 208 140 208 196 Z" fill="{ERG}" stroke="{OBS}" stroke-width="3"/>')
    o.append(f'<path d="M122 120 L178 120 L186 196 L114 196 Z" fill="{ONLUK}" stroke="{OBS}" stroke-width="2.6" stroke-linejoin="round"/>')
    o.append(f'<path d="M132 120 C132 110 168 110 168 120" fill="none" stroke="{OBS}" stroke-width="2.4"/>')
    o.append(f'<circle cx="150" cy="70" r="31" fill="{TEN}" stroke="{OBS}" stroke-width="3"/>')
    o.append(f'<path d="M119 66 C118 40 134 30 150 30 C166 30 183 40 181 66 C176 52 164 46 150 46 C136 46 124 52 119 66 Z" fill="{SAC}" stroke="{OBS}" stroke-width="2.6"/>')
    o.append(f'<circle cx="150" cy="27" r="11" fill="{SAC}" stroke="{OBS}" stroke-width="2.6"/>')
    for x in (138, 162):
        o.append(f'<circle cx="{x}" cy="72" r="8.5" fill="#fff" fill-opacity=".55" stroke="{OBS}" stroke-width="2.4"/><circle cx="{x}" cy="73" r="2.6" fill="{OBS}"/>')
    o.append(f'<path d="M146.5 72 H153.5" stroke="{OBS}" stroke-width="2.4"/>')
    o.append(f'<path d="M141 88 Q150 95 159 88" fill="none" stroke="{OBS}" stroke-width="2.6" stroke-linecap="round"/>')
    o.append('<ellipse cx="128" cy="84" rx="5" ry="3" fill="#F59C9C" opacity=".6"/><ellipse cx="172" cy="84" rx="5" ry="3" fill="#F59C9C" opacity=".6"/>')
    # sağ kol: fırça (gül dalı biçimi yok; düz sap) tutar
    o.append(f'<path d="M196 132 C218 136 228 120 232 100" fill="none" stroke="{ERG}" stroke-width="17" stroke-linecap="round"/>'
             f'<path d="M196 132 C218 136 228 120 232 100" fill="none" stroke="{OBS}" stroke-width="2.6" stroke-dasharray="0" opacity="0"/>')
    o.append(f'<circle cx="233" cy="98" r="9" fill="{TEN}" stroke="{OBS}" stroke-width="2.6"/>')
    o.append(f'<path d="M226 112 L246 62" stroke="#8C5500" stroke-width="5" stroke-linecap="round"/>'
             f'<path d="M244 66 C238 58 240 48 248 44 C256 48 256 58 250 68 Z" fill="{MER}" stroke="{OBS}" stroke-width="2.2"/>')
    # serpilen damlalar
    for i, (x, y) in enumerate(((236, 140), (214, 152), (250, 158), (226, 170))):
        o.append(f'<circle cx="{x}" cy="{y}" r="{3.6 - i * .4}" fill="{EBRU_RENK[i]}" stroke="{OBS}" stroke-width="1.2"/>')
    # sol kol: teknenin kenarına dayalı
    o.append(f'<path d="M104 140 C84 150 80 168 92 180" fill="none" stroke="{ERG}" stroke-width="17" stroke-linecap="round"/>')
    o.append(f'<circle cx="94" cy="182" r="9" fill="{TEN}" stroke="{OBS}" stroke-width="2.6"/>')
    # tekne (önde): ahşap kenar + ebrulu yüzey
    o.append(f'<path d="M28 196 L36 236 Q150 254 264 236 L272 196 Z" fill="#9C6A3C" stroke="{OBS}" stroke-width="3" stroke-linejoin="round"/>')
    o.append(f'<ellipse cx="150" cy="196" rx="122" ry="37" fill="#B07A47" stroke="{OBS}" stroke-width="3"/>')
    o.append(f'<ellipse cx="150" cy="196" rx="118" ry="34" fill="#F4EFE2"/>')
    o.append(f'<g clip-path="url(#ust-yuzey)">{_tas(rng, 150, 196, 118, 34, 30)}</g>')
    o.append(f'<ellipse cx="150" cy="196" rx="118" ry="34" fill="none" stroke="{OBS}" stroke-width="2"/>')
    # boya çanakları
    for i, renk in enumerate((MER, KOB, KEH)):
        x = 30 + i * 34
        o.append(f'<path d="M{x} 132 h26 l-3 18 h-20 Z" fill="#E8D9C0" stroke="{OBS}" stroke-width="2.2"/>'
                 f'<ellipse cx="{x + 13}" cy="132" rx="13" ry="3.6" fill="{renk}" stroke="{OBS}" stroke-width="2"/>')
    o.append('</svg>')
    return "".join(o)


def _kesit(x, y, w, h, renk_su="#CFE8F0", etiket="", alt=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{renk_su}" stroke="{OBS}" stroke-width="2"/>'
            f'<path d="M{x} {y + 12} H{x + w}" stroke="#7FB8C9" stroke-width="2"/>'
            f'<text x="{x + w / 2}" y="{y + h + 17}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="15" fill="{OBS}">{etiket}</text>'
            + (f'<text x="{x + w / 2}" y="{y + h + 33}" text-anchor="middle" font-family="Nunito" font-weight="800" font-size="12.5" fill="#56636E">{alt}</text>' if alt else ""))


def sir_cizim(n):
    """üç sırrın şeması (viewBox 0 0 300 130)."""
    n = int(n)
    o = ['<svg viewBox="0 0 300 130" xmlns="http://www.w3.org/2000/svg">']
    if n == 1:      # viskozite: suda damla batar ve dağılır; kitreli suda yüzeyde durur
        o.append(_kesit(10, 14, 130, 78, "#D6EEF6", "su", "boya batar, dağılır"))
        o.append(_kesit(160, 14, 130, 78, "#E9E2C6", "kitreli su", "boya yüzeyde durur"))
        o.append(f'<circle cx="75" cy="6" r="6" fill="{MER}" stroke="{OBS}" stroke-width="1.6"/>'
                 f'<path d="M75 16 C70 40 84 52 74 70" fill="none" stroke="{MER}" stroke-width="4" stroke-dasharray="5 4" stroke-linecap="round"/>'
                 f'<ellipse cx="74" cy="82" rx="20" ry="6" fill="{MER}" opacity=".45"/>')
        o.append(f'<ellipse cx="225" cy="25" rx="26" ry="5" fill="{MER}" stroke="{OBS}" stroke-width="1.6"/>')
        for i in range(5):
            o.append(f'<path d="M{176 + i * 24} 44 q6 -4 12 0 t12 0" fill="none" stroke="#B9A66A" stroke-width="2"/>')
    elif n == 2:    # yüzey gerilimi: ödsüz damla boncuk gibi kalır/batar; ödlü damla ince halka olur
        o.append(_kesit(10, 14, 130, 78, "#D6EEF6", "ödsüz boya", "toplanır, batar"))
        o.append(_kesit(160, 14, 130, 78, "#D6EEF6", "ödlü boya", "ince halka olup yayılır"))
        o.append(f'<circle cx="75" cy="22" r="11" fill="{KOB}" stroke="{OBS}" stroke-width="1.8"/>'
                 f'<path d="M75 36 V62" stroke="{KOB}" stroke-width="4" stroke-dasharray="5 4"/>')
        o.append(f'<ellipse cx="225" cy="26" rx="56" ry="7" fill="{KOB}" stroke="{OBS}" stroke-width="1.8"/>'
                 f'<ellipse cx="225" cy="26" rx="34" ry="4" fill="none" stroke="#fff" stroke-width="2"/>')
        for s in (-1, 1):
            o.append(f'<path d="M{225 + s * 60} 20 l{s * 14} 0" stroke="{OBS}" stroke-width="2.4" stroke-linecap="round"/>'
                     f'<path d="M{225 + s * 74} 20 l{-s * 6} -5 l0 10 Z" fill="{OBS}"/>')
    else:           # çözünmezlik: pigment taneleri yüzeyde; çözünen boya suya dağılır
        o.append(_kesit(10, 14, 130, 78, "#D6EEF6", "toprak boya", "taneler suda çözünmez"))
        o.append(_kesit(160, 14, 130, 78, "#D6EEF6", "suda çözünen boya", "renk suya karışır"))
        rng = random.Random(3)
        for _ in range(34):
            o.append(f'<circle cx="{_f(rng.uniform(22, 128))}" cy="{_f(rng.uniform(19, 25))}" r="{_f(rng.uniform(1.6, 2.6))}" fill="{ZUM}" stroke="{OBS}" stroke-width=".8"/>')
        o.append('<defs><linearGradient id="sir-cz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1F8A5B" stop-opacity=".85"/>'
                 '<stop offset="1" stop-color="#1F8A5B" stop-opacity=".12"/></linearGradient></defs>')
        o.append(f'<path d="M162 26 H288 V90 H162 Z" fill="url(#sir-cz)"/>')
    o.append('</svg>')
    return "".join(o)


def unesco_rozet():
    """logo değil: genel bir miras rozeti (yıldız + 2014)."""
    o = ['<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">']
    nok = []
    for i in range(16):
        a = math.pi * 2 * i / 16 - math.pi / 2
        r = 22 if i % 2 == 0 else 17.5
        nok.append(f"{_f(24 + r * math.cos(a))} {_f(24 + r * math.sin(a))}")
    o.append(f'<path d="M{" L".join(nok)} Z" fill="{ALTIN}" stroke="{OBS}" stroke-width="1.4"/>')
    o.append(f'<circle cx="24" cy="24" r="13" fill="{KIREC}" stroke="{OBS}" stroke-width="1.2"/>')
    o.append(f'<text x="24" y="28.5" text-anchor="middle" font-family="\'Baloo Bhaijaan 2\'" font-weight="800" font-size="11" fill="{LAJ}">2014</text>')
    o.append('</svg>')
    return "".join(o)
