from unitsofmeasure import binprefix

def test():
    items = binprefix.si_binary_prefixes.items()
    assert len(items) == 8 # there are 8 binary prefixes

    for (key, prefix) in items:
        print(key, prefix)
        assert key == prefix.symbol
        assert prefix.base == 2
        assert prefix.exponent >= 10
        assert prefix.exponent <= 80
        assert len(prefix.symbol) > 0
        assert len(prefix.name) > 0
