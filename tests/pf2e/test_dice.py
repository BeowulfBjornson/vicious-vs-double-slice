from vicious_vs_double_slice.pf2e import dice

def test_averages():
    assert 6.5 == dice.average_value("1d12")
    assert 16.5 == dice.average_value("1d12+10")
    assert 2.5 == dice.average_value("1d12-4")
    assert 13 == dice.average_value("2d12")
    assert 18.5 == dice.average_value("2d12+1d10")
    assert 10.5 == dice.average_value("2d12+1d10-8")
    assert 10.5 == dice.average_value("2d12   + 1d10- 8")
    assert 10.5 == dice.average_value("2d12 +  1d10  - 8")


def test_dyce_expression():
    assert 6.5 == dice.to_dyce_expression("1d12").mean()
    assert 16.5 == dice.to_dyce_expression("1d12+10").mean()
    assert 2.5 == dice.to_dyce_expression("1d12-4").mean()
    assert 13 == dice.to_dyce_expression("2d12").mean()
    assert 18.5 == dice.to_dyce_expression("2d12+1d10").mean()
    assert 10.5 == dice.to_dyce_expression("2d12+1d10-8").mean()
    assert 10.5 == dice.to_dyce_expression("2d12   + 1d10- 8").mean()
    assert 10.5 == dice.to_dyce_expression("2d12 +  1d10  - 8").mean()
