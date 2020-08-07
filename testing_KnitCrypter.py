import KnitCrypter as kc
from KnitCrypter import stitch_patterns as sp


a = kc.knitpattern("abcdefghiJKLMNOPQR", hex, sp.Summations, 14, 3, '**')
b = kc.knitpattern("jklmnopqrSTUVWXYZ", oct, sp.PowerOf, 4)
c = kc.knitpattern("stuvwxyzABCDEFGHI", 64, sp.Cube)

d = a + b + c
print(d)
for i in d:
    print(f'{i}: {d[i]}')
