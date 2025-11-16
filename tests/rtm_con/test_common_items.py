import inspect
import pytest

# tests/rtm_con/test_common_items.py

rtm_common = pytest.importorskip("rtm_con.common_items")

DATAITEM_CAESES = (
    (100, "kW", True),
    (100, "kW", False),
    (100, "kW", None)
)

@pytest.mark.parametrize("value,unit,valid,expected", [
    case + (expected,) for case, expected in zip(DATAITEM_CAESES, (
        "DataItem(100, kW, True)",
        "DataItem(100, kW, False)",
        "DataItem(100, kW, None)",
    ))
])
def test_DataItem_repr(value,unit,valid,expected):
    item = rtm_common.DataItem(value, unit, valid)
    assert repr(item) == expected

@pytest.mark.parametrize("value,unit,valid,expected", [
    case + (expected,) for case, expected in zip(DATAITEM_CAESES, (
        "100 kW",
        "Abnormal",
        "Invalid",
    ))
])
def test_DataItem_str(value,unit,valid,expected):
    item = rtm_common.DataItem(value, unit, valid)
    assert str(item) == expected

@pytest.mark.parametrize("value,unit,valid", DATAITEM_CAESES)
def test_DataItem_eq(value,unit,valid):
    item1 = rtm_common.DataItem(value, unit, valid)
    item2 = rtm_common.DataItem(value, unit, valid)
    assert item1 == item2