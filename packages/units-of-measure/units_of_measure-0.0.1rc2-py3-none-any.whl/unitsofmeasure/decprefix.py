"""Decimal (SI) Prefixes"""
from unitsofmeasure import Prefix

da = Prefix(10,   1, "da", "deca")
h  = Prefix(10,   2, "h",  "hecto")
k  = Prefix(10,   3, "k",  "kilo")
M  = Prefix(10,   6, "M",  "mega")
G  = Prefix(10,   9, "G",  "giga")
T  = Prefix(10,  12, "T",  "tera")
P  = Prefix(10,  15, "P",  "peta")
E  = Prefix(10,  18, "E",  "exa")
Z  = Prefix(10,  21, "Z",  "zetta")
Y  = Prefix(10,  24, "Y",  "yotta")
d  = Prefix(10,  -1, "d",  "deci")
c  = Prefix(10,  -2, "c",  "centi")
m  = Prefix(10,  -3, "m",  "milli")
µ  = Prefix(10,  -6, "µ",  "micro")
n  = Prefix(10,  -9, "n",  "nano")
p  = Prefix(10, -12, "p",  "pico")
f  = Prefix(10, -15, "f",  "femto")
a  = Prefix(10, -18, "a",  "atto")
z  = Prefix(10, -21, "z",  "zepto")
y  = Prefix(10, -24, "y",  "yocto")

si_decimal_prefixes: dict[str, Prefix] = {
    "da": da,
    "h" : h,
    "k" : k,
    "M" : M,
    "G" : G,
    "T" : T,
    "P" : P,
    "E" : E,
    "Z" : Z,
    "Y" : Y,
    "d" : d,
    "c" : c,
    "m" : m,
    "µ" : µ,
    "n" : n,
    "p" : p,
    "f" : f,
    "a" : a,
    "z" : z,
    "y" : y
}
