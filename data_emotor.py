from common_items import *

"""
GB/T 32960.3-2016 chp7.2.3.2 table10
"""
emotor_data_2016 = Struct(
    "emotor_total" / Int8ub,
    "emotor_list" / RepeatUntil(
        lambda obj, lst, ctx: (len(lst)==ctx.emotor_total),
        LazyBound(lambda: emotor_item_2016),
    )
)

"""
GB/T 32960.3-2016 chp7.2.3.2 table11
"""
emotor_item_2016 = Struct(
    "index" / Int8ub,
    "state" / Enum(Int8ub, power_consuming=0x01, power_generating=0x02, off=0x03, idle=0x04, abnormal=0xfe, invalid=0xff),
    "temp_controller" / DataItemAdapter(Int8ub, "℃", 1, -40),
    # For some strange reason, the offset for speed and torque are marked without unit in GB/T 32960.3-2016
    # Which means, the offset is added before factor, this is different with any other date item
    "speed" / DataItemAdapter(Int16ub, "rpm", 1, -20000), # Not affected
    "torque" / DataItemAdapter(Int16ub, "N·m", 0.1, -2000), # Raw offset 20000 * factor 0.1
    "temperature" / DataItemAdapter(Int8ub, "℃", 1, -40),
    "volt_controller" / DataItemAdapter(Int16ub, "V", 0.1),
    "curr_controller" / DataItemAdapter(Int16ub, "A", 0.1, -1000),
)

"""
GB/T 32960.3-2025 chp7.2.4.4 table15
"""
emotor_data_2025 = Struct(
    "emotor_total" / Int8ub,
    "emotor_list" / RepeatUntil(
        lambda obj, lst, ctx: (len(lst)==ctx.emotor_total),
        LazyBound(lambda: emotor_item_2025),
    )
)

"""
GB/T 32960.3-2025 chp7.2.4.4 table16
"""
emotor_item_2025 = Struct(
    "index" / Int8ub,
    "state" / Enum(Int8ub, power_consuming=0x01, power_generating=0x02, off=0x03, idle=0x04, abnormal=0xfe, invalid=0xff),
    "temp_controller" / DataItemAdapter(Int8ub, "℃", 1, -40),
    "speed" / DataItemAdapter(Int16ub, "rpm", 1, -32000),
    "torque" / DataItemAdapter(Int32ub, "N·m", 0.1, -20000),
    "temperature" / DataItemAdapter(Int8ub, "℃", 1, -40),
)