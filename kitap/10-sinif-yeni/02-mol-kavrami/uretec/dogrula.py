"""Mol Kavramı ünitesindeki tüm sayısal cevapları doğrular.
Çalıştır: python3 uretec/dogrula.py   (her ÇS sorusunda tek doğru şık kontrolü dahil)"""
from fractions import Fraction as F
NA = 6.02e23
M = dict(H=1, He=4, C=12, N=14, O=16, Na=23, Mg=24, S=32, Ca=40, Cl=35.5)
def mk(d): return sum(M[k]*v for k, v in d.items())
def yakin(a, b, t=1e-9): return abs(a-b) <= t*max(1, abs(a), abs(b))
hata = []
def kontrol(ad, kosul):
    print(("OK  " if kosul else "HATA") + "  " + ad)
    if not kosul: hata.append(ad)
def tek_sik(ad, siklar, dogru_mu, beklenen):
    d = [k for k, v in siklar.items() if dogru_mu(v)]
    kontrol(f"{ad}: tek doğru şık {d} == ['{beklenen}']", d == [beklenen])

# --- KN1
yil = NA / (365.25*24*3600)
kontrol(f"KN1 ≈19 katrilyon yıl ({yil:.3g})", 1.85e16 < yil < 1.95e16)
kontrol(f"KN1 ≈1,4 milyon kat ({yil/13.8e9:.3g})", 1.35e6 < yil/13.8e9 < 1.45e6)
kontrol("KN1 hızlı görev: 1 mol H2O → 2 mol H", 1*2 == 2)
# --- KN2
kontrol("Görev 1 bor 10,8", yakin(10*0.2 + 11*0.8, 10.8))
kontrol("KN2 hızlı: Cl 35·0,75+37·0,25 = 35,5", yakin(35*0.75 + 37*0.25, 35.5))
kontrol("KN2 kontrol: 14C nötron 8, proton 6", 14-6 == 8)
# --- KN3
kontrol("Görev 2 NH3: 1,505e23 / 1 mol atom / 0,75 mol H", yakin(0.25*NA, 1.505e23) and yakin(0.25*4, 1) and yakin(0.25*3, .75))
kontrol("Görev 3: 3,01e23 CO2 → 1 mol O", yakin(3.01e23/NA*2, 1))
kontrol("Görev 4: 1,2 mol atom C2H6 → 0,15 mol", yakin(1.2/8, .15))
kontrol("KN3 hızlı: 1,204e24 H2O → 4 mol H", yakin(1.204e24/NA*2, 4))
kontrol("KN3 tuzak: 1 mol CO2 → 3 mol atom = 1,806e24", yakin(3*NA, 1.806e24))
# --- KN4
kontrol("H2SO4 98", mk(dict(H=2, S=1, O=4)) == 98)
kontrol("CaCO3 100", mk(dict(Ca=1, C=1, O=3)) == 100)
kontrol("Mg(OH)2 58", mk(dict(Mg=1, O=2, H=2)) == 58)
kontrol("Görev 5A: 0,4 mol CaCO3 = 40 g", yakin(0.4*100, 40))
kontrol("Görev 5B: 9 g H2O → 0,5 mol, 3,01e23, 1,5 mol atom", yakin(9/18, .5) and yakin(.5*NA, 3.01e23) and yakin(.5*3, 1.5))
so2 = mk(dict(S=1, O=2))
kontrol("Görev 6: 6,4 g SO2 → 3,2 g O", so2 == 64 and yakin(6.4/64*2*16, 3.2))
kontrol("KN4 tuzak: CO = N2 = 28", mk(dict(C=1, O=1)) == mk(dict(N=2)) == 28)
kontrol("KN4 hızlı: 0,25 mol CH4 = 4 g, 1 mol H", yakin(.25*16, 4) and yakin(.25*4, 1))
# --- KN5
x = F(6, 10)/2  # 4x + 6(0,5-x) = 2,4
kontrol("Görev 7: x=0,3 → 10,8 g, H kontrol 2,4", x == F(3, 10) and yakin(float(x*16 + (F(1, 2)-x)*30), 10.8) and yakin(float(x*4 + (F(1, 2)-x)*6), 2.4))
kontrol("Görev 8: 64 g → O2 2 mol, SO2 1 mol; atom 4/3", 64/32 == 2 and 64/64 == 1 and F(2*2, 1*3) == F(4, 3))
kontrol("KN5 hızlı: eşit kütle CH4/O2 molekül oranı 2", F(32, 16)/F(32, 32) == 2)
# --- Hata avcısı
kontrol("Hata1: H2SO4 7 atom → 3,5", yakin(.5*7, 3.5))
kontrol("Hata2: 11/44 = 0,25 (28 yanlış; 11/28≈0,39 yuvarlaması doğru)", yakin(11/44, .25) and round(11/28, 2) == .39)
kontrol("Hata3: SO3 80 doğru; 1 tanesi 80/NA ≈ 1,33e-22", mk(dict(S=1, O=3)) == 80 and abs(80/NA - 1.33e-22) < .01e-22)
kontrol("Hata4: CH4 1 mol, O2 0,5 mol", 16/16 == 1 and 16/32 == .5)
# --- Bağlam
n = .88/176
tek_sik("Bağlam 1", {"A": "I", "B": "III", "C": "I,II", "D": "II,III", "E": "I,II,III"},
        lambda v: set(v.split(",")) == {k for k, ok in {"I": yakin(n, 5e-3), "II": yakin(n*NA, 3.01e21), "III": yakin(n*6, .005)}.items() if ok}, "C")
nc = 3*.2/12*NA
tek_sik("Bağlam 2", {"A": 3.01e21, "B": 1.505e22, "C": 3.01e22, "D": 6.02e22, "E": 1.806e23}, lambda v: yakin(v, nc), "C")
MX, MY = 12/.5, 16/.5
dogru3 = {k for k, ok in {"I": MX == 24, "II": F(96, int(MX))/F(96, int(MY)) == F(4, 3), "III": MY-MX == 8}.items() if ok}
tek_sik("Bağlam 3", {"A": "I", "B": "I,II", "C": "I,III", "D": "II,III", "E": "I,II,III"}, lambda v: set(v.split(",")) == dogru3, "E")
I, II, III = 4.4/44*3, 1.204e23/NA*3, .1*4
sira = ",".join(k for k, _ in sorted({"I": I, "II": II, "III": III}.items(), key=lambda t: -t[1]))
tek_sik("Bağlam 4", {"A": "I,II,III", "B": "II,III,I", "C": "III,II,I", "D": "II,I,III"}, lambda v: v == sira, "B")
kontrol("Bağlam 4 E (I = II > III) yanlış", not yakin(I, II))
# --- İpucu merdiveni
kontrol("Merdiven 1: X = 56", (32/.2 - 48)/2 == 56)
xm = (44*.4 - 14.4)/(44-28)
kontrol("Merdiven 2: x=0,2 → 2,4 mol H", yakin(xm, .2) and yakin(xm*4 + (.4-xm)*8, 2.4))
kontrol("Merdiven 3: 25/4", F(5*80, 4*16) == F(25, 4))
# --- Boss (12 soru)
tek_sik("Test 1", dict(A=.3, B=1.1, C=2.4, D=3.3, E=3.6), lambda v: yakin(v, .3*11), "D")
tek_sik("Test 2", dict(A=.5, B=1, C=2, D=4, E=12), lambda v: yakin(v, 1.204e24/NA), "C")
tek_sik("Test 3", dict(A=20.5, B=29, C=41, D=58, E=116), lambda v: yakin(v, .5*58), "B")
d4 = {k for k, ok in {"I": 6.4/32 == .2, "II": yakin(.2*NA, 1.204e23), "III": yakin(.2*2, .4)}.items() if ok}
tek_sik("Test 4", {"A": "I", "B": "II", "C": "I,II", "D": "II,III", "E": "I,II,III"}, lambda v: set(v.split(",")) == d4, "E")
ciftler = {"A": (dict(C=1, O=1), dict(N=2)), "B": (dict(C=1, O=2), dict(S=1, O=2)), "C": (dict(H=2, O=1), dict(N=1, H=3)),
           "D": (dict(C=1, H=4), dict(O=2)), "E": (dict(N=1, O=1), dict(O=2))}
tek_sik("Test 5", ciftler, lambda v: mk(v[0]) == mk(v[1]), "A")
tek_sik("Test 6", {"A": 12, "B": 12*NA, "C": 12/NA, "D": NA/12, "E": 1/12}, lambda v: yakin(v, 12/NA), "C")
atom = dict(A=1, B=.5*3, C=8/16*5, D=3.01e23/NA*3, E=4.4/44*3)
tek_sik("Test 7", atom, lambda v: v == max(atom.values()), "C")
tek_sik("Test 8", dict(A=10, B=20, C=25, D=40, E=80), lambda v: v == 10/.25, "D")
tek_sik("Test 9", dict(A=63.0, B=63.6, C=64.0, D=64.4, E=65.0), lambda v: yakin(v, 63*.7 + 65*.3), "B")
yanlis10 = {"A": False, "B": False, "C": False, "D": False, "E": True}  # nötr izotoplar: fiziksel özellik farklı
tek_sik("Test 10 (yanlış olan)", yanlis10, lambda v: v, "E")
x11 = (1.0 - .7)   # x + 2(0,5-x) = 0,7 → x = 0,3
tek_sik("Test 11", dict(A=8.0, B=9.6, C=10.4, D=11.2, E=12.8), lambda v: yakin(v, x11*16 + (.5-x11)*28), "C")
nch4, nso2 = 64/16, 64/64
d12 = {k for k, ok in {"I": nch4/nso2 == 4, "II": nch4*5 == nso2*3, "III": nch4*4 == 8*nso2*2}.items() if ok}
tek_sik("Test 12", {"A": "I", "B": "II", "C": "I,II", "D": "I,III", "E": "I,II,III"}, lambda v: set(v.split(",")) == d12, "D")
# --- XP muhasebesi
kn = dict(KN1=10+20+30+40, KN2=20+50+20+20+40, KN3=30+25+25+30+10+30, KN4=20+25+25+40+20+20, KN5=20+50+40+10+30)
kontrol(f"KN XP {kn} = 100/150/150/150/150", list(kn.values()) == [100, 150, 150, 150, 150])
toplam = sum(kn.values()) + 40 + 4*30 + 4*30 + 3*40 + 12*25
kontrol(f"Ünite toplam XP {toplam} == 1400", toplam == 1400)
print("\nSONUÇ:", "hepsi doğru" if not hata else f"{len(hata)} hata: {hata}")
