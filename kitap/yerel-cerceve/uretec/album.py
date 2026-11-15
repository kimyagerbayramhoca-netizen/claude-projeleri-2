"""Nişan albümü: her yolun nişanları boyanacak çizgi resim olarak; yol başına Üstad Mührü, akçe kutusu ve unvan;
sonda kitabın Ahilik toplamı. Nişan adları yalnız meta.json'dan (ya da ünitenin kendi açılış sayfasından) gelir;
yoksa yuvalar durak sırasıyla adlandırılır ("1. durak", …, "Kale") ve nişan adı boş çizgi olarak bırakılır.
"""


def sayfalara_bol(k):
    n = len(k.yollar)
    if n <= 6:
        ilk = (n + 1) // 2
        return [k.yollar[:ilk], k.yollar[ilk:]]
    return [k.yollar[:5], k.yollar[5:]]
