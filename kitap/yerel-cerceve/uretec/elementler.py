"""Periyodik tablo verisi: 118 element (sembol, Türkçe ad, yuvarlatılmış mol kütlesi, sınıf, yer).

Mol kütleleri YAZIM-REHBERI.md ile uyumludur: tam sayıya yuvarlanır (H 1, C 12, Cu 64, Zn 65, Ag 108 …); Cl 35,5.
Dy'nin standart değeri 162,50 tam yarım olduğundan 162,5 yazılır. Kararlı izotopu olmayan elementlerde köşeli parantez
içindeki sayı en uzun ömürlü izotopun kütle numarasıdır (IUPAC geleneği). 104–118 için kütle yazılmaz: çok az atom elde
edilmiştir ve kaynaklardaki değerler yeni ölçümlerle değişmektedir.

Sınıflar 9-sinif/04-periyodik-tablo (klasik ünite) ile aynıdır: yarı metal B Si Ge As Sb Te; ametal H C N O F P S Cl Se Br I;
soy gaz He Ne Ar Kr Xe Rn Og; sınıfı kaynağa göre değişen (gri) Po At Nh Fl Mc Lv Ts; geri kalanlar metal.
Lantanit (57–71) ve aktinitler (89–103) IUPAC düzeninde ayrı iki satırdır; 3. grupta 6. ve 7. periyot hücreleri yer tutucudur.
Elektronegatiflik bilerek yazılmamıştır (karar bekliyor).
"""

VERI = """\
1 H Hidrojen 1
2 He Helyum 4
3 Li Lityum 7
4 Be Berilyum 9
5 B Bor 11
6 C Karbon 12
7 N Azot 14
8 O Oksijen 16
9 F Flor 19
10 Ne Neon 20
11 Na Sodyum 23
12 Mg Magnezyum 24
13 Al Alüminyum 27
14 Si Silisyum 28
15 P Fosfor 31
16 S Kükürt 32
17 Cl Klor 35,5
18 Ar Argon 40
19 K Potasyum 39
20 Ca Kalsiyum 40
21 Sc Skandiyum 45
22 Ti Titanyum 48
23 V Vanadyum 51
24 Cr Krom 52
25 Mn Mangan 55
26 Fe Demir 56
27 Co Kobalt 59
28 Ni Nikel 59
29 Cu Bakır 64
30 Zn Çinko 65
31 Ga Galyum 70
32 Ge Germanyum 73
33 As Arsenik 75
34 Se Selenyum 79
35 Br Brom 80
36 Kr Kripton 84
37 Rb Rubidyum 85
38 Sr Stronsiyum 88
39 Y İtriyum 89
40 Zr Zirkonyum 91
41 Nb Niyobyum 93
42 Mo Molibden 96
43 Tc Teknesyum [98]
44 Ru Rutenyum 101
45 Rh Rodyum 103
46 Pd Paladyum 106
47 Ag Gümüş 108
48 Cd Kadmiyum 112
49 In İndiyum 115
50 Sn Kalay 119
51 Sb Antimon 122
52 Te Tellür 128
53 I İyot 127
54 Xe Ksenon 131
55 Cs Sezyum 133
56 Ba Baryum 137
57 La Lantan 139
58 Ce Seryum 140
59 Pr Praseodim 141
60 Nd Neodim 144
61 Pm Prometyum [145]
62 Sm Samaryum 150
63 Eu Evropiyum 152
64 Gd Gadolinyum 157
65 Tb Terbiyum 159
66 Dy Disprosyum 162,5
67 Ho Holmiyum 165
68 Er Erbiyum 167
69 Tm Tulyum 169
70 Yb İterbiyum 173
71 Lu Lutesyum 175
72 Hf Hafniyum 178
73 Ta Tantal 181
74 W Tungsten 184
75 Re Renyum 186
76 Os Osmiyum 190
77 Ir İridyum 192
78 Pt Platin 195
79 Au Altın 197
80 Hg Cıva 201
81 Tl Talyum 204
82 Pb Kurşun 207
83 Bi Bizmut 209
84 Po Polonyum [209]
85 At Astatin [210]
86 Rn Radon [222]
87 Fr Fransiyum [223]
88 Ra Radyum [226]
89 Ac Aktinyum [227]
90 Th Toryum 232
91 Pa Protaktinyum 231
92 U Uranyum 238
93 Np Neptünyum [237]
94 Pu Plütonyum [244]
95 Am Amerikyum [243]
96 Cm Küriyum [247]
97 Bk Berkelyum [247]
98 Cf Kaliforniyum [251]
99 Es Aynştaynyum [252]
100 Fm Fermiyum [257]
101 Md Mendelevyum [258]
102 No Nobelyum [259]
103 Lr Lavrensiyum [266]
104 Rf Rutherfordiyum -
105 Db Dubniyum -
106 Sg Seaborgiyum -
107 Bh Bohriyum -
108 Hs Hassiyum -
109 Mt Meitneriyum -
110 Ds Darmstadtiyum -
111 Rg Röntgenyum -
112 Cn Kopernikyum -
113 Nh Nihonyum -
114 Fl Flerovyum -
115 Mc Moskovyum -
116 Lv Livermoryum -
117 Ts Tennesin -
118 Og Oganesson -
"""

ELEMENTLER = []
for satir in VERI.strip().splitlines():
    z, sembol, ad, kutle = satir.split()
    ELEMENTLER.append({"z": int(z), "sembol": sembol, "ad": ad, "kutle": None if kutle == "-" else kutle})
assert len(ELEMENTLER) == 118 and [e["z"] for e in ELEMENTLER] == list(range(1, 119))

YARI = {"B", "Si", "Ge", "As", "Sb", "Te"}
AMETAL = {"H", "C", "N", "O", "F", "P", "S", "Cl", "Se", "Br", "I"}
SOY = {"He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"}
BELIRSIZ = {"Po", "At", "Nh", "Fl", "Mc", "Lv", "Ts"}

BAS = {1: 1, 2: 3, 3: 11, 4: 19, 5: 37, 6: 55, 7: 87}
SON = {1: 2, 2: 10, 3: 18, 4: 36, 5: 54, 6: 86, 7: 118}


def sinif(sembol):
    if sembol in YARI:
        return "yari"
    if sembol in AMETAL:
        return "ametal"
    if sembol in SOY:
        return "soy"
    if sembol in BELIRSIZ:
        return "belirsiz"
    return "metal"


def yer(z):
    """(periyot, IUPAC grup) ya da f bloku için (periyot, None)."""
    for p in range(1, 8):
        if BAS[p] <= z <= SON[p]:
            break
    i = z - BAS[p]
    if p == 1:
        return p, (1 if z == 1 else 18)
    if p in (2, 3):
        return p, (i + 1 if i < 2 else i + 11)
    if p in (4, 5):
        return p, i + 1
    if i < 2:
        return p, i + 1
    if i <= 16:
        return p, None
    return p, i - 13


def ab_adi(g):
    return {1: "1A", 2: "2A", 3: "3B", 4: "4B", 5: "5B", 6: "6B", 7: "7B", 8: "8B", 9: "8B", 10: "8B", 11: "1B", 12: "2B",
            13: "3A", 14: "4A", 15: "5A", 16: "6A", 17: "7A", 18: "8A"}[g]


# Rotalarda geçen, Türkiye'de çıkarılan ya da üretilen elementler: (sembol, yer, [(sınıf, yol)])
# Duraklar rotalar.json ile aynıdır (9-2 Zonguldak/Karabük, 9-4 Kırka/Bandırma/Gümüşköy/Seydişehir, 9-5 Divriği/Guleman/Maden,
# 9-6 Tuz Gölü, 9-9 Midyat, 10-3 Çayönü).
TURKIYE = [
    ("B", "Kırka (Eskişehir) · Bandırma", [(9, 4)]),
    ("Ag", "Gümüşköy (Kütahya) · Midyat telkarisi", [(9, 4), (9, 9)]),
    ("Al", "Seydişehir (Konya)", [(9, 4)]),
    ("Fe", "Divriği (Sivas) · Karabük demir-çelik", [(9, 5), (9, 2)]),
    ("Cr", "Guleman (Elazığ)", [(9, 5)]),
    ("Cu", "Maden (Elazığ) · Çayönü (Ergani)", [(9, 5), (10, 3)]),
    ("C", "Zonguldak taş kömürü", [(9, 2)]),
    ("Na", "Tuz Gölü tuzlaları (NaCl)", [(9, 6)]),
    ("Cl", "Tuz Gölü tuzlaları (NaCl)", [(9, 6)]),
]

# panelde kısa yer adları
KISA_YER = {"B": "Kırka, Bandırma", "Ag": "Gümüşköy; Midyat telkarisi", "Al": "Seydişehir (Konya)", "Fe": "Divriği; Karabük çelik",
            "Cr": "Guleman (Elazığ)", "Cu": "Maden (Elazığ); Çayönü", "C": "Zonguldak taş kömürü", "Na": "Tuz Gölü tuzlaları",
            "Cl": "Tuz Gölü tuzlaları"}
