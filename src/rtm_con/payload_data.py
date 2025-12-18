from construct import (
    Struct,
    LazyBound,
    GreedyRange,
    Switch,
    Const,
    GreedyBytes,
    RepeatUntil,
    Int8ub,
    Peek,
)

from rtm_con.utilities import HexAdapter
from rtm_con.common_items import rtm_ts
from rtm_con.types_sig import payload_sig
from rtm_con.types_data import data_types_2016, data_types_2025, DATA_ITEM_MAPPING_2016, DATA_ITEM_MAPPING_2025

"""
GB/T 32960.3-2016 chp7.2.1 table7
"""
data_2016 = Struct(
    "timestamp" / rtm_ts,
    "data_list" / LazyBound(lambda: GreedyRange(data_item_2016)),
)

data_item_2016 = Struct(
    "data_type" / data_types_2016,
    "data_content" / Switch(
        lambda this: this.data_type,
        DATA_ITEM_MAPPING_2016,
        # For 2016 protocol, as no other fields in payload
        # For unknown data type, just read all data
        default=HexAdapter(con=GreedyBytes), # unkown data
    ),
)

"""
GB/T 32960.3-2025 chp7.2.1 table7
"""
data_2025 = Struct(
    "timestamp" / rtm_ts,
    "data_list" / LazyBound(lambda: data_items_2025),
    "sig_starter" / HexAdapter(con=Const(b'\xff')),
    "sig" / payload_sig,
)

data_item_2025 = Struct(
    "data_type" / data_types_2025,
    "data_content" / Switch(
        lambda this: this.data_type,
        DATA_ITEM_MAPPING_2025,
        # For 2025 protocol, as there are signature_starter and signature at the end
        # For unknown data type, try to read until 0xff, this will generate some single byte data items (as _peek_byte is hidden)
        default=RepeatUntil(
            lambda obj, lst, ctx: (lst and lst[-1]._peek_byte==0xff) or not hasattr(lst[-1], '_peek_byte'),
            Struct(
                "data_byte" / Int8ub,
                "_peek_byte" / Peek(Int8ub),
            )
        )
    ),
    "_peek_type" / Peek(Int8ub),
)

data_items_2025 = RepeatUntil(
    # the _peek_type doesn't has to be provided when buiding the con
    lambda obj, lst, ctx: obj._peek_type==0xff if ctx._parsing else len(lst)==len(ctx.data_list),
    data_item_2025,
)