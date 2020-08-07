import KnitCrypter as kc
from KnitCrypter import stitch_patterns as sp
from re import search
import string

a = kc.knitpattern("abcdefghi", hex, sp.Summations, 14, 3, '**')
b = kc.knitpattern("jklmnopqr", oct, sp.PowerOf, 4)
c = kc.knitpattern("stuvwxyz", 9, sp.Prime)


sixfour = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_/|\\-~`"=+!@#$%^&*?.><][)(}{'

knew = a + b + c
test = '0x7785f0o342664bG659b87369b8573'
