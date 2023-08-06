from unitsofmeasure import base, decprefix, no_prefix, scalar, Unit

def test():
    items = base.si_base_units.items()
    assert len(items) == 7 # there are 7 base units

    for (key, unit) in items:
        print(key, unit, unit.name)
        assert key == unit.symbol
        assert len(unit.symbol) > 0
        assert len(unit.name) > 0
        assert unit.dimension != scalar
        assert unit.factor == Unit._one

        if unit == base.kg:
            assert unit.prefix == decprefix.k
        else:
            assert unit.prefix == no_prefix
