"""Test Unit"""
import pytest
from fractions import Fraction
from unitsofmeasure import decprefix, Dimension, no_prefix, no_unit, Prefix, scalar, Unit

_one = Fraction(1,1)

@pytest.mark.parametrize(
    "symbol , name       , dimension        , prefix,     , factor",[
    ("%"    , "percent"  , Dimension()      , no_prefix   , Fraction(1,100)), # scalar
    ("kg"   , "kilogram" , Dimension(kg=1)  , decprefix.k , _one), # SI base units
    ("m"    , "metre"    , Dimension(m=1)   , no_prefix   , _one),
    ("s"    , "second"   , Dimension(s=1)   , no_prefix   , _one),
    ("A"    , "ampere"   , Dimension(A=1)   , no_prefix   , _one),
    ("K"    , "kelvin"   , Dimension(K=1)   , no_prefix   , _one),
    ("cd"   , "candela"  , Dimension(cd=1)  , no_prefix   , _one),
    ("mol"  , "mole"     , Dimension(mol=1) , no_prefix   , _one)
])
def test_unit(symbol: str, name: str, dimension: Dimension, prefix: Prefix, factor: Fraction) -> None:
    unit = Unit(symbol, name, dimension, prefix, factor)
    assert unit.symbol    == symbol
    assert unit.name      == name
    assert unit.dimension == dimension
    assert unit.prefix    == prefix
    assert unit.factor    == factor

def test_no_unit() -> None:
    assert len(no_unit.symbol) == 0
    assert len(no_unit.name)   == 0
    assert no_unit.dimension   == scalar
    assert no_unit.prefix      == no_prefix
    assert no_unit.factor      == _one
