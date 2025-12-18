import pytest

try:
    import rtm_con.types_dataitem as types_dataitem
except:
    types_dataitem = None

DATAITEM_CAESES = (
    (100, "kW", True),
    (100.12, "kW", True),
    (100, "kW", False),
    (100, "kW", None),
)

@pytest.mark.parametrize("value,unit,valid,expected", [
    case + (expected,) for case, expected in zip(DATAITEM_CAESES, (
        "DataItem(100, kW, True)",
        "DataItem(100.12, kW, True)",
        "DataItem(100, kW, False)",
        "DataItem(100, kW, None)",
    ))
])
def test_DataItem_repr(value,unit,valid,expected):
    item = types_dataitem.DataItem(value, unit, valid)
    assert repr(item) == expected

@pytest.mark.parametrize("value,unit,valid,expected", [
    case + (expected,) for case, expected in zip(DATAITEM_CAESES, (
        "100 kW",
        "100.12 kW",
        "100 abnormal",
        "100 invalid",
    ))
])
def test_DataItem_str(value,unit,valid,expected):
    item = types_dataitem.DataItem(value, unit, valid)
    assert str(item) == expected

@pytest.mark.parametrize("value,unit,valid", DATAITEM_CAESES)
def test_DataItem_eq(value,unit,valid):
    item = types_dataitem.DataItem(value, unit, valid)
    assert item == types_dataitem.DataItem(value, unit, valid)
    assert item == str(item)
    assert item == item.value


def test_DataItemAdapter():
    from construct import Int16ub
    adapter = types_dataitem.DataItemAdapter(Int16ub, "km", 1, 0, validation=True)
    assert adapter.parse(bytes.fromhex("00c8")) == types_dataitem.DataItem(200, "km", True)
    assert adapter.build(types_dataitem.DataItem(200, "km", True)) == bytes.fromhex("00c8")
    assert adapter.parse(bytes.fromhex("fffe")) == types_dataitem.DataItem(65534, "km", False)
    assert adapter.parse(bytes.fromhex("ffff")) == types_dataitem.DataItem(65535, "km", None)