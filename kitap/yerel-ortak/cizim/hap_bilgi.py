"""Hap Bilgi ailesi · ikonlar ve küçük yer tutucular (ORTAK; kaynak: gelistirme/atom-modelleri). CSS: stil.css §37.

Altı "dikkat görseli", her birinin kendine özgü BİÇİMİ vardır; renk görmeyen ya da fotokopi okuyucusu da türü şekilden tanır:
  .hb.hb-hap      kapsül (iki renkli hap)         {{hbi|hap}}                     kısa, net tek bilgi
  .hb.hb-kural    tezhipli altın kart + kurdele   {{hbi|yildiz}}  {{kose}}         ünitenin taşıyıcı kuralı (Altın Kural)
  .hb.hb-unutma   yapışkan not / defter kenarı    (ikon yok; bant + kıvrık köşe)   kolay unutulan ayrıntı (Unutma!)
  .hb.hb-radar    köşe kurdeleli radar rozeti     {{hbi|radar}}  {{siklik|3|3}}    sınavda sık çıkan bilgi (Sınav Radarı)
  .hb.hb-dikkat   kırmızı çizgi + uyarı üçgeni    {{hbi|dikkat}}                   işlem/okuma hatası (Dikkat!)
  .hb.hb-kilit    anahtar madalyonu               {{hbi|anahtar}}  {{hbi|delik|anahtar-delik}}   konuyu açan tek fikir (Kilit Bilgi)
Öteki ikonlar: {{hbi|carpi}} (yanlış), {{hbi|tik}} (doğru), {{hbi|ciftok}} (↔ yerine). Yazıda ok gerekiyorsa {{ok}}
(Nunito'da → yok; SVG ok, metin rengini alır). İkon renkleri renkler.py tokenlarıdır (palet eşlemesi bunları da eşler).
"""
from cizim.temel import f, cizgi_d, selcuklu_yildizi
from cizim.renkler import OBS, KEH, KEH_K, MER, MER_A, KOB, KOB_K, KOB_A, GOL, GOL_A, GOL_K, ALTIN_A, ZUMRUT

IKON = {
    # iki renkli kapsül (45° eğik): sol yarı beyaz, sağ yarı mercan; parlama çizgisi
    "hap": ("0 0 24 24",
            f'<g transform="rotate(-40 12 12)"><path d="M12 6.4 H7.4 A5.6 5.6 0 0 0 7.4 17.6 H12 Z" fill="#FFFFFF" stroke="{OBS}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M12 6.4 H16.6 A5.6 5.6 0 0 1 16.6 17.6 H12 Z" fill="{MER}" stroke="{OBS}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M6.2 9.4 Q7 8.3 8.8 8.2" fill="none" stroke="{MER_A}" stroke-width="1.2" stroke-linecap="round"/>'
            f'<path d="M14 8.6 H17" stroke="#FFFFFF" stroke-width="1.2" stroke-linecap="round" opacity=".8"/></g>'),
    # sekiz köşeli yıldız (altın kurdele)
    "yildiz": ("0 0 24 24", f'<path d="{cizgi_d(selcuklu_yildizi(12, 12, 10.5), True)}" fill="{ALTIN_A}" stroke="{ALTIN_A}" stroke-width="1" stroke-linejoin="round"/>'
                            f'<circle cx="12" cy="12" r="3" fill="#1D3A8A"/>'),
    # radar: halkalar, tarayan dilim, iki iz
    "radar": ("0 0 40 40",
              f'<circle cx="20" cy="20" r="18.4" fill="{KOB_A}" stroke="{OBS}" stroke-width="1.6"/>'
              f'<circle cx="20" cy="20" r="12.4" fill="none" stroke="{KOB}" stroke-width="1.1" opacity=".7"/>'
              f'<circle cx="20" cy="20" r="6.4" fill="none" stroke="{KOB}" stroke-width="1.1" opacity=".7"/>'
              f'<path d="M20 1.6 V38.4 M1.6 20 H38.4" stroke="{KOB}" stroke-width=".7" opacity=".45"/>'
              f'<path d="M20 20 L20 1.6 A18.4 18.4 0 0 1 35.9 10.8 Z" fill="{KOB}" opacity=".32"/>'
              f'<path d="M20 20 L35.9 10.8" stroke="{KOB_K}" stroke-width="1.6" stroke-linecap="round"/>'
              f'<circle cx="27.6" cy="9.6" r="2.4" fill="{MER}" stroke="{OBS}" stroke-width=".9"/>'
              f'<circle cx="11.4" cy="26.8" r="1.8" fill="{KEH}" stroke="{OBS}" stroke-width=".8"/>'
              f'<circle cx="20" cy="20" r="2" fill="{KOB_K}"/>'),
    # uyarı üçgeni: kehribar dolgu, ünlem çizgiyle
    "dikkat": ("0 0 40 36",
               f'<path d="M20 2.6 Q21.6 2.6 22.5 4.1 L38 31 Q38.8 32.6 37.9 33.6 Q37.2 34.4 35.9 34.4 H4.1 Q2.8 34.4 2.1 33.6 Q1.2 32.6 2 31 L17.5 4.1 Q18.4 2.6 20 2.6 Z" '
               f'fill="{KEH}" stroke="{OBS}" stroke-width="2.2" stroke-linejoin="round"/>'
               f'<path d="M20 12.6 V23.4" stroke="{OBS}" stroke-width="3.6" stroke-linecap="round"/><circle cx="20" cy="28.6" r="2.3" fill="{OBS}"/>'),
    # anahtar (madalyonda beyaz)
    "anahtar": ("0 0 24 24",
                f'<g fill="#FFFFFF" stroke="{OBS}" stroke-width="1.3" stroke-linejoin="round">'
                f'<path d="M8 4.2 A4.6 4.6 0 1 1 8 13.4 A4.6 4.6 0 1 1 8 4.2 Z M8 7.2 A1.6 1.6 0 1 0 8 10.4 A1.6 1.6 0 1 0 8 7.2 Z" fill-rule="evenodd"/>'
                f'<path d="M11.8 11.6 L19.6 19.4 L18.2 20.8 L16.8 19.4 L15.6 20.6 L14.2 19.2 L15.4 18 L10.4 13 Z"/></g>'),
    # anahtar deliği (soluk filigran)
    "delik": ("0 0 20 30", f'<circle cx="10" cy="9" r="7" fill="{GOL_A}" stroke="{GOL_K}" stroke-width="1.2"/>'
                           f'<path d="M7 13 L5 28 H15 L13 13 Z" fill="{GOL_A}" stroke="{GOL_K}" stroke-width="1.2" stroke-linejoin="round"/>'),
    # yanlış (çarpı) · doğru (tik): fontta ✗ ✓ yok
    "carpi": ("0 0 24 24", f'<circle cx="12" cy="12" r="10.4" fill="{MER}" stroke="{OBS}" stroke-width="1.4"/>'
                           f'<path d="M8 8 L16 16 M16 8 L8 16" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round"/>'),
    "tik": ("0 0 24 24", f'<circle cx="12" cy="12" r="10.4" fill="{ZUMRUT}" stroke="{OBS}" stroke-width="1.4"/>'
                         f'<path d="M7.2 12.4 L10.6 15.8 L17 8.8" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'),
    # çift yönlü ok (↔ Baloo'da yok)
    "ciftok": ("0 0 24 24", f'<path d="M4 12 H20" stroke="{OBS}" stroke-width="2.2" stroke-linecap="round"/>'
                            f'<path d="M8 7.6 L3.4 12 L8 16.4 M16 7.6 L20.6 12 L16 16.4" fill="none" stroke="{OBS}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'),
}


def ikon(ad, cls="hbi"):
    vb, govde = IKON[ad]
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true">{govde}</svg>'


def ok(renk="currentColor"):
    """Metin içi sağ ok (Nunito'da → yok): satır yüksekliğinde SVG."""
    return (f'<svg class="ok-y" viewBox="0 0 26 12" aria-hidden="true" style="display:inline-block;width:1.25em;height:.62em;vertical-align:.02em">'
            f'<path d="M1.5 6 H21" stroke="{renk}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="M16.5 1.6 L23.5 6 L16.5 10.4" fill="none" stroke="{renk}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def siklik(dolu, toplam=3):
    """Sınav radarı sıklık göstergesi: dolu/toplam nokta."""
    dolu, toplam = int(dolu), int(toplam)
    return "".join('<i></i>' if k < dolu else '<i class="bos"></i>' for k in range(toplam))


def yildiz_satir(n, renk=KEH):
    """Fontta ★ yok: SVG yıldızlar."""
    yol = cizgi_d([(6 + 5.6 * __import__("math").cos(-1.5708 + i * 3.14159 / 5) * (1 if i % 2 == 0 else .45),
                    6 + 5.6 * __import__("math").sin(-1.5708 + i * 3.14159 / 5) * (1 if i % 2 == 0 else .45)) for i in range(10)], True)
    return "".join(f'<svg viewBox="0 0 12 12" style="width:3mm;height:3mm"><path d="{yol}" fill="{renk}" stroke="{OBS}" stroke-width=".8"/></svg>' for _ in range(int(n)))
