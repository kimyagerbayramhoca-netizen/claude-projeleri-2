SEMBOL = """H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu
Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr
Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og""".split()
assert len(SEMBOL) == 118
BAS = {1:1,2:3,3:11,4:19,5:37,6:55,7:87}
SON = {1:2,2:10,3:18,4:36,5:54,6:86,7:118}

def yer(z):
    """(periyot, iupac_grup or None for f, blok)"""
    for p in range(1,8):
        if BAS[p] <= z <= SON[p]:
            break
    i = z - BAS[p]
    if p == 1:
        return p, (1 if z == 1 else 18), 's'
    if p in (2,3):
        g = i+1 if i < 2 else i+11
    elif p in (4,5):
        g = i+1
    else:
        if i < 2: g = i+1
        elif i <= 16: return p, None, 'f'
        else: g = i-13
    blok = 's' if g <= 2 else ('d' if g <= 12 else 'p')
    return p, g, blok

def ab(g):
    if g is None: return 'f'
    m = {1:'1A',2:'2A',3:'3B',4:'4B',5:'5B',6:'6B',7:'7B',8:'8B',9:'8B',10:'8B',11:'1B',12:'2B',
         13:'3A',14:'4A',15:'5A',16:'6A',17:'7A',18:'8A'}
    return m[g]

# Aufbau dizilimi (Cr, Cu, Mo, Ag istisnaları sadece ilk 54 için kontrol amaçlı)
SIRA = ['1s','2s','2p','3s','3p','4s','3d','4p','5s','4d','5p','6s','4f','5d','6p','7s','5f','6d','7p']
KAP = {'s':2,'p':6,'d':10,'f':14}
def dizilim(e, istisna=True, z=None):
    out = []
    kalan = e
    for o in SIRA:
        if kalan == 0: break
        n = min(kalan, KAP[o[-1]]); out.append([o, n]); kalan -= n
    if istisna and z in (24, 29, 42, 47) and z == e:
        d = {24:'3d',29:'3d',42:'4d',47:'4d'}[z]; s = {24:'4s',29:'4s',42:'5s',47:'5s'}[z]
        for x in out:
            if x[0] == s: x[1] = 1
            if x[0] == d: x[1] += 1
    return out

def yer_dizilimden(z):
    d = dizilim(z, z=z)
    nmax = max(int(o[0]) for o, k in d)
    son = d[-1][0][-1]
    if z == 2: return nmax, 18
    if son == 's' and not any(o[-1]=='d' and int(o[0])==nmax-1 for o,k in d[-1:]):
        # s ile biten: d dolu olabilir (Zn) -> son terim s ama 3d de var
        pass
    val_s = sum(k for o,k in d if o == f'{nmax}s')
    val_p = sum(k for o,k in d if o == f'{nmax}p')
    val_d = sum(k for o,k in d if o == f'{nmax-1}d')
    if son == 'p':
        return nmax, 10 + val_s + val_p
    if son == 'd' or (son == 's' and val_d):
        return nmax, val_s + val_d
    if son == 's':
        return nmax, val_s
    return nmax, None
