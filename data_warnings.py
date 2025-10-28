from common_items import *

"""
GB/T 32960.3-2016 chp7.2.3.7 table18
"""
general_warnings_2016 = BitStruct(
    "_reserved" / Padding(13),
    "pack_over_charged_warning" / Flag,
    "emotor_temp_warning" / Flag,
    "hv_interlock_warning" / Flag,
    "emotor_driver_temp_warning" / Flag,
    "dcdc_state_warning" / Flag,
    "brake_system_wanring" / Flag,
    "dcdc_temp_warning" / Flag,
    "insulation_warning" / Flag,
    "cell_poor_consistency_warning" / Flag,
    "pack_unmatched_warning" / Flag,
    "soc_jump_warning" / Flag,
    "soc_high_warning" / Flag,
    "cell_under_volt_warning" / Flag,
    "cell_over_volt_warning" / Flag,
    "soc_low_warning" / Flag,
    "pack_under_volt_warning" / Flag,
    "pack_over_volt_warning" / Flag,
    "pack_high_temp_warning" / Flag,
    "temp_differentce_warning" / Flag,
)

"""
GB/T 32960.3-2016 chp7.2.3.7 table17
"""
warnings_data_2016 = Struct(
    "max_warning_level" / Int8ub,
    "general_warnings" / general_warnings_2016,
    "pack_failures" / PrefixedArray(Int8ub, Bytes(4)),
    "emotor_failures" / PrefixedArray(Int8ub, Bytes(4)),
    "engine_failures" / PrefixedArray(Int8ub, Bytes(4)),
    "other_failures" / PrefixedArray(Int8ub, Bytes(4)),
)

"""
GB/T 32960.3-2025 chp7.2.4.9 table24
"""
general_warnings_2025 = BitStruct(
    "_reserved" / Padding(4),
    "fuel_cell_stack_over_temp_warning" / Flag,
    "hydrogen_system_temp_abnormal_warning" / Flag,
    "hydrogen_system_presure_abnormal_warning" / Flag,
    "hydrogen_leakage_warning" / Flag,
    "pack_thermal_event_warning" / Flag,
    "super_capacitor_over_pressure_warning" / Flag,
    "super_capacitor_over_temp_warning" / Flag,
    "emotor_over_curr_warning" / Flag,
    "emotor_over_speed_warning" / Flag,
    "pack_over_charged_warning" / Flag,
    "emotor_temp_warning" / Flag,
    "hv_interlock_warning" / Flag,
    "emotor_driver_temp_warning" / Flag,
    "dcdc_state_warning" / Flag,
    "brake_system_wanring" / Flag,
    "dcdc_temp_warning" / Flag,
    "insulation_warning" / Flag,
    "cell_poor_consistency_warning" / Flag,
    "pack_unmatched_warning" / Flag,
    "soc_jump_warning" / Flag,
    "soc_high_warning" / Flag,
    "cell_under_volt_warning" / Flag,
    "cell_over_volt_warning" / Flag,
    "soc_low_warning" / Flag,
    "pack_under_volt_warning" / Flag,
    "pack_over_volt_warning" / Flag,
    "pack_high_temp_warning" / Flag,
    "temp_differentce_warning" / Flag,
)

"""
GB/T 32960.3-2025 chp7.2.4.9 table23
"""
warnings_data_2025 = Struct(
    "max_warning_level" / Int8ub,
    "general_warnings" / general_warnings_2016,
    "pack_failures" / PrefixedArray(Int8ub, Bytes(4)),
    "emotor_failures" / PrefixedArray(Int8ub, Bytes(4)),
    "engine_failures" / PrefixedArray(Int8ub, Bytes(4)),
    "other_failures" / PrefixedArray(Int8ub, Bytes(4)),
    "general_warning_list" / PrefixedArray(Int8ub, Bytes(2)),
)