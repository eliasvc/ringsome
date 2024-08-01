import countrycodes


def test_alpha2():
    assert countrycodes.alpha2["US"] == "United States of America"
