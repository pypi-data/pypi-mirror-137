from unitsofmeasure import accepted, no_prefix, Unit

def test():
    items = accepted.si_accepted_units.items()
    assert len(items) == 7 # there are 7 implemented and accepted units

    for (key, unit) in items:
        print(key, unit, unit.name)
        assert key == unit.symbol
        assert len(unit.symbol) > 0
        assert len(unit.name) > 0
        assert unit.prefix == no_prefix
        assert unit.factor != Unit._one
