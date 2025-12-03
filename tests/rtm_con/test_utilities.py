import pytest

utilities = pytest.importorskip("rtm_con.utilities")

def test_GoThoughDict():
    gd = utilities.GoThoughDict()
    assert 1 in gd
    assert 1 == gd.get(1)
    assert gd[1]==1
