from construct import (
    Struct,
    Const,
)

from rtm_con.utilities import HexAdapter
from rtm_con.types_common import rtm_ts
from rtm_con.types_sig import Signature
from rtm_con.types_data import data_items_2016, data_items_2025

"""
GB/T 32960.3-2016 chp7.2.1 table7
"""
data_2016 = Struct(
    "timestamp" / rtm_ts,
    "data_list" / data_items_2016,
)

"""
GB/T 32960.3-2025 chp7.2.1 table7
"""
data_2025 = Struct(
    "timestamp" / rtm_ts,
    "data_list" / data_items_2025,
    "sig_starter" / HexAdapter(con=Const(b'\xff')),
    "sig" / Signature("timestamp", "data_list"),
)