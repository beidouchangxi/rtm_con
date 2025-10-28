from common_items import *

"""
GB/T 32960.3-2016 anxB.3.5.3.8 tableB.6
"""
pack_item_2016 = Struct(
    "pack_index" / DataItemAdapter(Int8ub, ""),
    "pack_volt" / DataItemAdapter(Int16ub, "V", 0.1),
    "pack_curr" / DataItemAdapter(Int16ub, "V", 0.1, -3000),
    "cell_total" / DataItemAdapter(Int16ub, ""),
    "cell_start_index" / Int16ub,
    "cell_volts" / PrefixedArray(Int8ub, DataItemAdapter(Int16ub, "V", 0.001)),
)

"""
GB/T 32960.3-2016 anxB.3.5.3.8 tableB.5
"""
cell_volts_data_2016 = PrefixedArray(Int8ub, pack_item_2016)

"""
GB/T 32960.3-2025 chp7.2.4.2 table12
"""
pack_item_2025 = Struct(
    "pack_index" / DataItemAdapter(Int8ub, ""),
    "pack_volt" / DataItemAdapter(Int16ub, "V", 0.1),
    "pack_curr" / DataItemAdapter(Int16ub, "V", 0.1, -3000),
    "cell_volts" / PrefixedArray(Int16ub, DataItemAdapter(Int16ub, "V", 0.001)),
)

"""
GB/T 32960.3-2025 chp7.2.4.2 table11
"""
cell_volts_data_2025 = PrefixedArray(Int8ub, pack_item_2025)