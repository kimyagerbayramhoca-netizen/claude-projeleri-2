#!/usr/bin/env python3
"""Türkiye haritası verisini Natural Earth'ten (kamu malı) üretir → uretec/turkiye_veri.py

Bir kez çalıştırılır; çıktı modül depoda durur, kitap kurulumu internete ihtiyaç duymaz.

Girdiler (hepsi Natural Earth, public domain):
  ham.json                      world-atlas@2.0.2 countries-10m (Türkiye, id 792) + land-50m (komşu kara)
                                → topojson-client@3.1.0 ile GeoJSON'a çevrilmiş (bkz. aşağıdaki not)
  ne_10m_lakes.geojson          göller (Van, Tuz, Eğirdir, Beyşehir, Keban, Atatürk)
  ne_10m_rivers.geojson         büyük nehirler (ne_10m_rivers_lake_centerlines.geojson, bu adla kaydedilmiş)

Kullanım:
  python3 uretec/harita_veri_uret.py <girdi-klasörü>

ham.json üretimi (karalama klasöründe):
  npm install world-atlas@2.0.2 topojson-client@3.1.0
  node -e "const fs=require('fs'),t=require('topojson-client');
    const c=JSON.parse(fs.readFileSync(require.resolve('world-atlas/countries-10m.json')));
    const l=JSON.parse(fs.readFileSync(require.resolve('world-atlas/land-50m.json')));
    const tr=t.feature(c,c.objects.countries).features.find(f=>f.id==='792');
    const k=t.feature(l,l.objects.land);
    fs.writeFileSync('ham.json',JSON.stringify({turkiye:tr.geometry,kara:(k.features||[k]).map(f=>f.geometry||f)}))"

İzdüşüm: Lambert konik konform (φ1 = 37°, φ2 = 41°, φ0 = 39°, λ0 = 35°), birim = km.
Çıktı koordinatları: X sağa, Y aşağı (SVG), Türkiye'nin sınır kutusu + pay; 1 birim = 1 km.
"""
import json
import math
import os
import sys

R = 6371.0
F1, F2, F0, L0 = map(math.radians, (37.0, 41.0, 39.0, 35.0))
_N = math.log(math.cos(F1) / math.cos(F2)) / math.log(math.tan(math.pi / 4 + F2 / 2) / math.tan(math.pi / 4 + F1 / 2))
_F = math.cos(F1) * math.tan(math.pi / 4 + F1 / 2) ** _N / _N
_RHO0 = R * _F / math.tan(math.pi / 4 + F0 / 2) ** _N


def lcc(boylam, enlem):
    f, l = math.radians(enlem), math.radians(boylam)
    rho = R * _F / math.tan(math.pi / 4 + f / 2) ** _N
    t = _N * (l - L0)
    return rho * math.sin(t), _RHO0 - rho * math.cos(t)


def dp(pts, tol):
    """Douglas–Peucker sadeleştirme (yinelemeli)."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    yigin = [(0, len(pts) - 1)]
    while yigin:
        a, b = yigin.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1e-9
        en, ei = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            d = abs(dy * (px - ax) - dx * (py - ay)) / L
            if d > en:
                en, ei = d, i
        if en > tol:
            keep[ei] = True
            yigin += [(a, ei), (ei, b)]
    return [p for p, k in zip(pts, keep) if k]


def halka_sadele(halka, tol):
    """Kapalı halkayı sadeleştir: en uzak iki noktadan ikiye bölüp ayrı ayrı."""
    if len(halka) < 8:
        return halka
    if halka[0] == halka[-1]:
        halka = halka[:-1]
    i0 = 0
    j0 = max(range(len(halka)), key=lambda j: (halka[j][0] - halka[0][0]) ** 2 + (halka[j][1] - halka[0][1]) ** 2)
    a = dp(halka[i0:j0 + 1], tol)
    b = dp(halka[j0:] + [halka[0]], tol)
    return a[:-1] + b[:-1]


def alan(h):
    return 0.5 * sum(h[i][0] * h[(i + 1) % len(h)][1] - h[(i + 1) % len(h)][0] * h[i][1] for i in range(len(h)))


def kirp(halka, x0, y0, x1, y1):
    """Sutherland–Hodgman: halkayı dikdörtgene kırp."""
    def kenar(pts, ic, kes):
        out = []
        for i in range(len(pts)):
            p, q = pts[i - 1], pts[i]
            if ic(q):
                if not ic(p):
                    out.append(kes(p, q))
                out.append(q)
            elif ic(p):
                out.append(kes(p, q))
        return out

    def kx(x):
        return lambda p, q: (x, p[1] + (q[1] - p[1]) * (x - p[0]) / ((q[0] - p[0]) or 1e-9))

    def ky(y):
        return lambda p, q: (p[0] + (q[0] - p[0]) * (y - p[1]) / ((q[1] - p[1]) or 1e-9), y)
    pts = halka
    for ic, kes in ((lambda p: p[0] >= x0, kx(x0)), (lambda p: p[0] <= x1, kx(x1)),
                    (lambda p: p[1] >= y0, ky(y0)), (lambda p: p[1] <= y1, ky(y1))):
        pts = kenar(pts, ic, kes)
        if not pts:
            return []
    return pts


def d_yaz(halkalar):
    out = []
    for h in halkalar:
        out.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in h) + "Z")
    return "".join(out)


def poligonlar(g):
    if g["type"] == "Polygon":
        return [g["coordinates"]]
    if g["type"] == "MultiPolygon":
        return g["coordinates"]
    return []


def icinde(p, halka):
    x, y = p
    ic = False
    n = len(halka)
    for i in range(n):
        x1, y1 = halka[i]
        x2, y2 = halka[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-9) + x1:
            ic = not ic
    return ic


def main(klasor):
    ham = json.load(open(os.path.join(klasor, "ham.json")))
    # --- Türkiye (km, Y yukarı)
    tr_halka = []
    for poly in poligonlar(ham["turkiye"]):
        for k, ring in enumerate(poly):
            tr_halka.append([lcc(*p) for p in ring])
    xs = [p[0] for h in tr_halka for p in h]
    ys = [p[1] for h in tr_halka for p in h]
    PAY = 70
    X0, X1, Y0, Y1 = min(xs) - PAY, max(xs) + PAY, min(ys) - PAY, max(ys) + PAY

    def cevir(p):  # → SVG (Y aşağı), köken sol üst
        return (p[0] - X0, Y1 - p[1])
    W, H = X1 - X0, Y1 - Y0

    tr = []
    for h in tr_halka:
        h2 = halka_sadele([cevir(p) for p in h], 0.9)
        if abs(alan(h2)) > 40:          # çok küçük adacıkları at (40 km²)
            tr.append(h2)
    # --- komşu kara (land-50m), çerçeveye kırpılmış; Türkiye'nin altında çizilir
    kara = []
    for g in ham["kara"]:
        for poly in poligonlar(g):
            ring = poly[0]
            if not any(22 <= p[0] <= 49 and 32 <= p[1] <= 45 for p in ring):
                continue
            h = [cevir(lcc(*p)) for p in ring]
            h = kirp(h, -5, -5, W + 5, H + 5)
            if len(h) >= 3:
                h = halka_sadele(h, 1.6)
                if abs(alan(h)) > 60:
                    kara.append(h)
    # --- göller
    gol_ad = {"Lake Van": "Van Gölü", "Lake Tuz": "Tuz Gölü", "Eğirdir": "Eğirdir Gölü", "Beyşehir": "Beyşehir Gölü",
              "Keban Baraji": "Keban Barajı", "Ataturk Barajt": "Atatürk Barajı"}
    goller = {}
    for ft in json.load(open(os.path.join(klasor, "ne_10m_lakes.geojson")))["features"]:
        ad = ft["properties"].get("name")
        if ad in gol_ad:
            for poly in poligonlar(ft["geometry"]):
                h = halka_sadele([cevir(lcc(*p)) for p in poly[0]], 0.6)
                goller.setdefault(gol_ad[ad], []).append(h)
    # --- nehirler (Türkiye içinde kalan parçalar)
    nehir_ad = {"Firat": "Fırat", "Dicle": "Dicle", "Tigris": "Dicle", "Kiz?lirmak": "Kızılırmak", "Sakarya": "Sakarya",
                "Byk Menderes": "Büyük Menderes", "Aras": "Aras", "Ceyhan": "Ceyhan", "Kelkit": "Kelkit", "Murat": "Murat"}
    ana = max(tr, key=lambda h: abs(alan(h)))
    nehirler = {}
    for ft in json.load(open(os.path.join(klasor, "ne_10m_rivers.geojson")))["features"]:
        ad = ft["properties"].get("name")
        g = ft["geometry"]
        if ad not in nehir_ad or not g:
            continue
        cizgiler = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for c in cizgiler:
            pts = [cevir(lcc(*p)) for p in c if p]
            parca = []
            for p in pts:
                if icinde(p, ana):
                    parca.append(p)
                else:
                    if len(parca) > 2:
                        nehirler.setdefault(nehir_ad[ad], []).append(dp(parca, 1.2))
                    parca = []
            if len(parca) > 2:
                nehirler.setdefault(nehir_ad[ad], []).append(dp(parca, 1.2))

    def d_ac(cizgiler):
        return "".join("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in c) for c in cizgiler)

    hedef = os.path.join(os.path.dirname(os.path.abspath(__file__)), "turkiye_veri.py")
    with open(hedef, "w", encoding="utf-8") as f:
        f.write('"""ÜRETİLİR (uretec/harita_veri_uret.py): Türkiye, komşu kara, göl ve nehir yolları.\n\n'
                'Kaynak: Natural Earth (kamu malı) 1:10m ülkeler, 1:50m kara, 1:10m göller ve nehirler.\n'
                'İzdüşüm: Lambert konik konform (φ1=37°, φ2=41°, φ0=39°, λ0=35°); 1 birim = 1 km; Y aşağı.\n'
                'Noktaları aynı düzleme taşımak için harita.proje(enlem, boylam) kullanılır.\n"""\n')
        f.write(f"X0, Y1 = {X0:.3f}, {Y1:.3f}   # LCC (km) → yerel kayma\nW, H = {W:.1f}, {H:.1f}\n")
        f.write(f"TURKIYE = {json.dumps(d_yaz(tr))}\n")
        f.write(f"KARA = {json.dumps(d_yaz(kara))}\n")
        f.write("GOLLER = {\n" + "".join(f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(d_yaz(v))},\n" for k, v in goller.items()) + "}\n")
        f.write("NEHIRLER = {\n" + "".join(f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(d_ac(v))},\n" for k, v in nehirler.items()) + "}\n")
    n_tr = sum(len(h) for h in tr)
    print(f"Türkiye: {len(tr)} halka, {n_tr} nokta · kara {len(kara)} halka · göller {list(goller)} · nehirler {list(nehirler)}")
    print(f"W×H = {W:.0f}×{H:.0f} km · {os.path.getsize(hedef) / 1024:.0f} KB → {hedef}")


if __name__ == "__main__":
    main(sys.argv[1])
