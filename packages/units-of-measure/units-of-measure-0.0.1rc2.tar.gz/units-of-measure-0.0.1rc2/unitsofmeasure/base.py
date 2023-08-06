"""SI Base Units"""
from unitsofmeasure import decprefix, Dimension, Unit

kg  = Unit("kg", "kilogram", Dimension(kg=1), decprefix.k) # mass
m   = Unit("m", "metre", Dimension(m=1)) # length
s   = Unit("s", "second", Dimension(s=1)) # time
A   = Unit("A", "ampere", Dimension(A=1)) # electric current
K   = Unit("K", "kelvin", Dimension(K=1)) # thermodynamic temperature
cd  = Unit("cd", "candela", Dimension(cd=1)) # luminous intensity
mol = Unit("mol", "mole", Dimension(mol=1)) # amount of substance

# map symbols to units
si_base_units: dict[str, Unit] = {
    "kg":  kg,
    "m":   m,
    "s":   s,
    "A":   A,
    "K":   K,
    "cd":  cd,
    "mol": mol
}
