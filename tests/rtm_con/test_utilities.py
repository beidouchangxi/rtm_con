try:
    import rtm_con.utilities as utilities
except:
    utilities = None

def test_GoThoughDict():
    gd = utilities.GoThoughDict()
    assert 1 in gd
    assert 1 == gd.get(1)
    assert gd[1]==1
