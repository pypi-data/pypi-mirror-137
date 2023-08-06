"""SI Accepted Units"""
from fractions import Fraction
from unitsofmeasure import decprefix, Dimension, Unit

min = Unit("min", "minute", Dimension(s=1), factor=Fraction(60,1)) # time: 60 seconds
h   = Unit("h", "hour", Dimension(s=1), factor=Fraction(3600,1)) # time: 60 minutes
d   = Unit("d", "day", Dimension(s=1), factor=Fraction(86_400,1)) # time: 24 hours
au  = Unit("au", "astronomical unit", Dimension(m=1), factor=Fraction(149_597_870_700,1)) # length: distance between Earth and Sun
# angular degree, minute, and second are not implemented
ha  = Unit("ha", "hectare", Dimension(m=2), factor=Fraction(10_000,1)) # area
l   = Unit("l", "litre", Dimension(m=3), factor=Fraction(1,1000)) # volume
t   = Unit("t", "tonne", Dimension(kg=1), factor=Fraction(1000,1)) # mass
# dalton, electronvolt, neper, bel, and decibel are not implemented

# map symbols to units
si_accepted_units: dict[str, Unit] = {
    "min": min,
    "h":   h,
    "d":   d,
    "au":  au,
    "ha":  ha,
    "l":   l,
    "t":   t
}
