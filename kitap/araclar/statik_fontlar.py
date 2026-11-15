"""Değişken (variable) yazı tiplerinden sabit kalınlıklı (static) kopyalar üretir.

Neden: Chromium, değişken yazı tiplerini PDF'e Type 3 olarak gömer. Type 3 yazı tiplerini
bazı matbaa RIP'leri sorunlu işler, PDF de gereksiz büyür. Sabit kalınlıklı kopyalar ise
PDF'e normal TrueType (CID) olarak gömülür.

Kullanım:  python3 kitap/araclar/statik_fontlar.py
Çıktı:     kitap/fontlar/<aile>/static/<Ad>-<kalınlık>.ttf

CSS'te her kalınlık için ayrı bir @font-face yazılır, örnek:
  @font-face { font-family: "Nunito"; src: url("../../fontlar/nunito/static/Nunito-800.ttf"); font-weight: 800; }
"""
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTLAR = Path(__file__).resolve().parent.parent / "fontlar"

# kaynak dosya (fontlar/ altında) → üretilecek kalınlıklar
URETILECEK = {
    "nunito/Nunito[wght].ttf": [400, 500, 600, 700, 800, 900],
    "nunito/Nunito-Italic[wght].ttf": [400, 600, 700, 800, 900],
    "baloobhaijaan2/BalooBhaijaan2[wght].ttf": [400, 500, 600, 700, 800],
    "reemkufi/ReemKufi[wght].ttf": [400, 500, 600, 700],
}


def uret():
    for kaynak, kalinliklar in URETILECEK.items():
        yol = FONTLAR / kaynak
        hedef_klasor = yol.parent / "static"
        hedef_klasor.mkdir(exist_ok=True)
        ad = yol.name.split("[")[0]
        for w in kalinliklar:
            font = TTFont(yol)
            try:
                sabit = instancer.instantiateVariableFont(font, {"wght": w}, updateFontNames=True)
            except Exception:
                font = TTFont(yol)
                sabit = instancer.instantiateVariableFont(font, {"wght": w})
            cikti = hedef_klasor / f"{ad}-{w}.ttf"
            sabit.save(cikti)
            print(f"{cikti.relative_to(FONTLAR)}  {cikti.stat().st_size // 1024} KB")


if __name__ == "__main__":
    uret()
