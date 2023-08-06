from unitsofmeasure import derived, no_prefix, Unit

def test():
    items = derived.si_derived_units.items()
    assert len(items) == 22 # there are 22 derived units

    for (key, unit) in items:
        print(key, unit, unit.name)

        if (key == "degC"):
            assert unit.symbol == "°C"
        else:
            assert key == unit.symbol
        
        assert len(unit.symbol) > 0
        assert len(unit.name) > 0
        assert unit.prefix == no_prefix
        assert unit.factor == Unit._one
