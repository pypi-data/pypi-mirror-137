from unitsofmeasure import decprefix

def test():
    items = decprefix.si_decimal_prefixes.items()
    assert len(items) == 20 # there are 20 decimal prefixes

    for (key, prefix) in items:
        print(key, prefix)
        assert key == prefix.symbol
        assert prefix.base == 10
        assert prefix.exponent >= -24
        assert prefix.exponent <= 24
        assert len(prefix.symbol) > 0
        assert len(prefix.name) > 0
