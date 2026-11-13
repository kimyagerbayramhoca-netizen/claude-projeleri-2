#!/usr/bin/env python3
"""Ünitede geçen iyonik formüllerin yük dengesini ve atom sayılarını denetler.
Kullanım: python3 uretec/denetle.py  (ünite klasöründen)"""
import re
from math import gcd

KAT = {  # formül: yük
    "Li": 1, "Na": 1, "K": 1, "Rb": 1, "Cs": 1, "NH4": 1, "Ag": 1,
    "Mg": 2, "Ca": 2, "Sr": 2, "Ba": 2, "Zn": 2, "Al": 3,
}
AN = {
    "F": -1, "Cl": -1, "Br": -1, "I": -1, "H": -1, "O": -2, "S": -2, "N": -3, "P": -3, "C": -4,
    "OH": -1, "CN": -1, "NO3": -1, "NO2": -1, "HCO3": -1, "CH3COO": -1, "MnO4": -1, "ClO": -1,
    "HSO4": -1, "SO4": -2, "SO3": -2, "CO3": -2, "HPO4": -2, "PO4": -3,
}
COK = lambda s: bool(re.search(r"[A-Z].*[A-Z]|\d", s))  # çok atomlu mu


def formul(kat, kq, an, aq):
    g = gcd(kq, -aq)
    nk, na = -aq // g, kq // g
    def p(x, n):
        if n == 1: return x
        return f"({x}){n}" if COK(x) else f"{x}{n}"
    return p(kat, nk) + p(an, na)


def atom_say(f):
    """(NH4)2SO4 gibi formüldeki toplam atom sayısı"""
    def coz(s):
        i, top = 0, 0
        while i < len(s):
            if s[i] == "(":
                d, j = 1, i + 1
                while d:
                    d += {"(": 1, ")": -1}.get(s[j], 0); j += 1
                ic = coz(s[i + 1:j - 1]); m = re.match(r"\d*", s[j:]).group()
                top += ic * int(m or 1); i = j + len(m)
            else:
                m = re.match(r"[A-Z][a-z]?(\d*)", s[i:])
                top += int(m.group(1) or 1); i += len(m.group())
        return top
    return coz(f)


# (katyon, katyon yükü, anyon, beklenen formül, ad)
LISTE = [
    ("Na", 1, "HCO3", "NaHCO3", "sodyum hidrojen karbonat"),
    ("NH4", 1, "NO3", "NH4NO3", "amonyum nitrat"),
    ("Fe", 3, "O", "Fe2O3", "demir(III) oksit"),
    ("Fe", 2, "O", "FeO", "demir(II) oksit"),
    ("NH4", 1, "Cl", "NH4Cl", "amonyum klorür"),
    ("NH4", 1, "Br", "NH4Br", "amonyum bromür"),
    ("K", 1, "NO3", "KNO3", "potasyum nitrat"),
    ("Na", 1, "F", "NaF", "sodyum florür"),
    ("Li", 1, "O", "Li2O", "lityum oksit"),
    ("Ba", 2, "NO3", "Ba(NO3)2", "baryum nitrat"),
    ("Li", 1, "N", "Li3N", "lityum nitrür"),
    ("NH4", 1, "PO4", "(NH4)3PO4", "amonyum fosfat"),
    ("Al", 3, "SO4", "Al2(SO4)3", "alüminyum sülfat"),
    ("Ca", 2, "O", "CaO", "kalsiyum oksit"),
    ("Mg", 2, "OH", "Mg(OH)2", "magnezyum hidroksit"),
    ("Ca", 2, "Cl", "CaCl2", "kalsiyum klorür"),
    ("Fe", 3, "SO4", "Fe2(SO4)3", "demir(III) sülfat"),
    ("Cr", 3, "O", "Cr2O3", "krom(III) oksit"),
    ("Cr", 6, "O", "CrO3", "krom(VI) oksit"),
    ("Pb", 4, "O", "PbO2", "kurşun(IV) oksit"),
    ("Cu", 1, "S", "Cu2S", "bakır(I) sülfür"),
    ("Cu", 1, "O", "Cu2O", "bakır(I) oksit"),
    ("Cu", 2, "O", "CuO", "bakır(II) oksit"),
    ("Co", 2, "O", "CoO", "kobalt(II) oksit"),
    ("Mn", 4, "O", "MnO2", "mangan(IV) oksit"),
    ("Sn", 4, "F", "SnF4", "kalay(IV) florür"),
    ("Sn", 2, "NO3", "Sn(NO3)2", "kalay(II) nitrat"),
    ("K", 1, "PO4", "K3PO4", "potasyum fosfat"),
    ("NH4", 1, "CO3", "(NH4)2CO3", "amonyum karbonat"),
    ("NH4", 1, "SO4", "(NH4)2SO4", "amonyum sülfat"),
    ("K", 1, "SO4", "K2SO4", "potasyum sülfat"),
    ("Ca", 2, "NO3", "Ca(NO3)2", "kalsiyum nitrat"),
    ("Mg", 2, "SO4", "MgSO4", "magnezyum sülfat"),
    ("Na", 1, "SO3", "Na2SO3", "sodyum sülfit"),
    ("Na", 1, "SO4", "Na2SO4", "sodyum sülfat"),
    ("Na", 1, "S", "Na2S", "sodyum sülfür"),
    ("K", 1, "MnO4", "KMnO4", "potasyum permanganat"),
    ("Na", 1, "ClO", "NaClO", "sodyum hipoklorit"),
    ("Na", 1, "OH", "NaOH", "sodyum hidroksit"),
    ("K", 1, "OH", "KOH", "potasyum hidroksit"),
    ("Ca", 2, "OH", "Ca(OH)2", "kalsiyum hidroksit"),
    ("Ca", 2, "CO3", "CaCO3", "kalsiyum karbonat"),
    ("Na", 1, "CO3", "Na2CO3", "sodyum karbonat"),
    ("Na", 1, "Cl", "NaCl", "sodyum klorür"),
    ("Mg", 2, "CO3", "MgCO3", "magnezyum karbonat"),
    ("Mg", 2, "N", "Mg3N2", "magnezyum nitrür"),
    ("Al", 3, "N", "AlN", "alüminyum nitrür"),
    ("K", 1, "S", "K2S", "potasyum sülfür"),
    ("Ca", 2, "H", "CaH2", "kalsiyum hidrür"),
    ("Ba", 2, "F", "BaF2", "baryum florür"),
    ("K", 1, "I", "KI", "potasyum iyodür"),
    ("Al", 3, "O", "Al2O3", "alüminyum oksit"),
    ("Mg", 2, "Cl", "MgCl2", "magnezyum klorür"),
    ("NH4", 1, "S", "(NH4)2S", "amonyum sülfür"),
    ("Al", 3, "OH", "Al(OH)3", "alüminyum hidroksit"),
    ("Zn", 2, "S", "ZnS", "çinko sülfür"),
    ("Mg", 2, "PO4", "Mg3(PO4)2", "magnezyum fosfat"),
    ("Ca", 2, "PO4", "Ca3(PO4)2", "kalsiyum fosfat"),
    ("Fe", 3, "Cl", "FeCl3", "demir(III) klorür"),
    ("Fe", 2, "Cl", "FeCl2", "demir(II) klorür"),
    ("Cu", 2, "SO4", "CuSO4", "bakır(II) sülfat"),
    ("Pb", 2, "NO3", "Pb(NO3)2", "kurşun(II) nitrat"),
    ("Co", 3, "Cl", "CoCl3", "kobalt(III) klorür"),
    ("Mn", 2, "Cl", "MnCl2", "mangan(II) klorür"),
    ("Cu", 2, "Cl", "CuCl2", "bakır(II) klorür"),
    ("Na", 1, "CH3COO", "NaCH3COO", "sodyum asetat"),
    ("K", 1, "CH3COO", "KCH3COO", "potasyum asetat"),
    ("Na", 1, "PO4", "Na3PO4", "sodyum fosfat"),
    ("Sn", 2, "F", "SnF2", "kalay(II) florür"),
    ("Na", 1, "HSO4", "NaHSO4", "sodyum hidrojen sülfat"),
    ("Ca", 2, "HPO4", "CaHPO4", "kalsiyum hidrojen fosfat"),
    ("Al", 3, "NO3", "Al(NO3)3", "alüminyum nitrat"),
    ("Al", 3, "PO4", "AlPO4", "alüminyum fosfat"),
    ("Al", 3, "CO3", "Al2(CO3)3", "alüminyum karbonat"),
    ("Fe", 3, "OH", "Fe(OH)3", "demir(III) hidroksit"),
    ("Pb", 4, "Cl", "PbCl4", "kurşun(IV) klorür"),
    ("Sn", 4, "O", "SnO2", "kalay(IV) oksit"),
]

hata = 0
for kat, kq, an, bek, ad in LISTE:
    aq = AN[an]
    f = formul(kat, kq, an, aq)
    tamam = f == bek
    if not tamam:
        hata += 1
    print(f"{'OK ' if tamam else 'HATA'} {ad:28s} {bek:12s} hesap={f:12s} atom={atom_say(bek)}")

print("\nAtom sayıları (test 9 / ipucu 2):")
for f in ["NH4NO3", "Al2(SO4)3", "Ca(OH)2", "CH3COONa", "N2O5", "(NH4)3PO4", "Ba(NO3)2"]:
    print(" ", f, atom_say(f))
print("\nToplam hata:", hata)
