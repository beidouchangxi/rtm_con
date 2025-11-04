from common_items import *

"""
GB/T 32960.3-2016 chp7.2.3.2 table10
"""
emotor_data_2016 = PrefixedArray(Int8ub, LazyBound(lambda: emotor_item_2016))

"""
GB/T 32960.3-2016 chp7.2.3.2 table11
"""
emotor_item_2016 = Struct(
    "em_index" / Int8ub,
    "em_state" / Enum(Int8ub, power_consuming=0x01, power_generating=0x02, off=0x03, idle=0x04, abnormal=0xfe, invalid=0xff),
    "em_ctrl_temp" / DataItemAdapter(Int8ub, "℃", 1, -40),
    # For some strange reason, the offset for speed and torque are marked without unit in GB/T 32960.3-2016
    # Which means, the offset is added before factor, this is different with any other date item
    "em_speed" / DataItemAdapter(Int16ub, "rpm", 1, -20000), # Not affected
    "em_torque" / DataItemAdapter(Int16ub, "N·m", 0.1, -2000), # Raw offset 20000 * factor 0.1
    "em_temp" / DataItemAdapter(Int8ub, "℃", 1, -40),
    "em_ctrl_volt" / DataItemAdapter(Int16ub, "V", 0.1),
    "em_ctrl_curr" / DataItemAdapter(Int16ub, "A", 0.1, -1000),
)

"""
GB/T 32960.3-2025 chp7.2.4.4 table15
"""
emotor_data_2025 = "emotors" / PrefixedArray(Int8ub, LazyBound(lambda: emotor_item_2025))

"""
GB/T 32960.3-2025 chp7.2.4.4 table16
"""
emotor_item_2025 = Struct(
    "em_index" / Int8ub,
    "em_state" / Enum(Int8ub, power_consuming=0x01, power_generating=0x02, off=0x03, idle=0x04, abnormal=0xfe, invalid=0xff),
    "em_ctrl_temp" / DataItemAdapter(Int8ub, "℃", 1, -40),
    "em_speed" / DataItemAdapter(Int16ub, "rpm", 1, -32000),
    "em_torque" / DataItemAdapter(Int32ub, "N·m", 0.1, -20000),
    "em_temp" / DataItemAdapter(Int8ub, "℃", 1, -40),
)