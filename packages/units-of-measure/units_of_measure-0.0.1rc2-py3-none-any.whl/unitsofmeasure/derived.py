"""SI Derived Units

The symbol of unit ohm is Ω (Unicode OHM SIGN).
You can map this to other identifiers by assignment (e.g. `ohm = Ω`).

The symbol of unit degree Celsius is °C, but that is not a valid Python identifier.
Therefore it is mapped to degC.
"""
from unitsofmeasure import Dimension, Unit

rad  = Unit("rad", "radian") # plane angle
sr   = Unit("sr", "steradian") # solid angle
Hz   = Unit("Hz", "hertz", Dimension(s=-1)) # frequency
N    = Unit("N", "newton", Dimension(kg=1, m=1, s=-2)) # force
Pa   = Unit("Pa", "pascal", Dimension(kg=1, m=-1, s=-2)) # pressure
J    = Unit("J", "joule", Dimension(kg=1, m=2, s=-2)) # energy
W    = Unit("W", "watt", Dimension(kg=1, m=2, s=-3)) # power
C    = Unit("C", "coulomb", Dimension(A=1, s=1)) # electric charge
V    = Unit("V", "volt", Dimension(kg=1, m=2, s=-3, A=-1)) # electric potential difference
F    = Unit("F", "farad", Dimension(kg=-1, m=-2, s=4, A=2)) # capacitance
Ω    = Unit("Ω", "ohm", Dimension(kg=1, m=2, s=-3, A=-2)) # electric resistance
S    = Unit("S", "siemens", Dimension(kg=-1, m=-2, s=3, A=2)) # electric conductance
Wb   = Unit("Wb", "weber", Dimension(kg=1, m=2, s=-2, A=-1)) # magnetic flux
T    = Unit("T", "tesla", Dimension(kg=1, s=-2, A=-1)) # magnetic flux density
H    = Unit("H", "henry", Dimension(kg=1, m=2, s=-2, A=-2)) # inductance
degC = Unit("°C", "degree Celsius", Dimension(K=1)) # Celsius temperature
lm   = Unit("lm", "lumen", Dimension(cd=1)) # luminous flux
lx   = Unit("lx", "lux", Dimension(cd=1, m=-2)) # illuminance
Bq   = Unit("Bq", "becquerel", Dimension(s=-1)) # activity referred to a radionuclide
Gy   = Unit("Gy", "gray", Dimension(m=2, s=-2)) # absorbed dose
Sv   = Unit("Sv", "sievert", Dimension(m=2, s=-2)) # dose equivalent
kat  = Unit("kat", "katal", Dimension(mol=1, s=-1)) # catalytic activity

# map symbols to units
si_derived_units: dict[str, Unit] = {
    "rad":  rad,
    "sr":   sr,
    "Hz":   Hz,
    "N":    N,
    "Pa":   Pa,
    "J":    J,
    "W":    W,
    "C":    C,
    "V":    V,
    "F":    F,
    "Ω":    Ω,
    "S":    S,
    "Wb":   Wb,
    "T":    T,
    "H":    H,
    "degC": degC, # TODO map degC and/or °C?
    "lm":   lm,
    "lx":   lx,
    "Bq":   Bq,
    "Gy":   Gy,
    "Sv":   Sv,
    "kat":  kat
}
