"""Test UnitMap"""
from unitsofmeasure import get_unit_of, map_to_unit, Unit, UnitMap

def test() -> None:
    # not all objects are weakly referencable, but class instances are
    # https://docs.python.org/3/library/weakref.html
    class Measure:
        def __init__(self, value: object) -> None:
            self.value = value
    measure = Measure(10)
    b = Unit("b", "bit")
    units = UnitMap[Unit]()
    units.map_to_unit(measure, b)
    unit = units.get_unit_of(measure)
    assert unit == b

def test_decorator() -> None:
    b = Unit("b", "bit")

    @map_to_unit(b)
    def func() -> int:
        return 10

    unit = get_unit_of(func)
    assert unit == b
