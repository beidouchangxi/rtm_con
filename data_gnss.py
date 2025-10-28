from common_items import *

"""
GB/T 32960.3-2016 chp7.2.3.5 table15
GB/T 32960.3-2025 chp7.2.4.8 table22
"""
gnss_states = BitStruct(
    "_reserved" / Padding(5),
    "e_w" /Enum(BitsInteger(1), e=0, w=1),
    "n_s" / Enum(BitsInteger(1), n=0, s=1),
    "valid" / Flag,
)

"""
GB/T 32960.3-2016 chp7.2.3.5 table14, table15
"""
gnss_data_2016 = Struct(
    "gnss_state" / gnss_states,
    "longitude" / DataItemAdapter(Int32ub, "°", 0.000001),
    "latitude" / DataItemAdapter(Int32ub, "°", 0.000001),
)

"""
GB/T 32960.3-2025 chp7.2.4.8 table21, table22
"""
gnss_data_2025 = Struct(
    "gnss_state" / gnss_states,
    "gcs" / Enum(Int8ub, wgs84=1, gcj02=2, other=3),
    "longitude" / DataItemAdapter(Int32ub, "°", 0.000001),
    "latitude" / DataItemAdapter(Int32ub, "°", 0.000001),
)
