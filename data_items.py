from common_items import *

"""
GB/T 32960.3-2016 chp7.2.3.1 table9
GB/T 32960.3-2016 anxB.3.5.3.1 tableB.4
"""
whole_vehicle_data_2016 = Struct(
    "vehicle_state" / Int8ub,
    "charge_state" / Int8ub,
    "operate_state" / Int8ub,
    "vehicle_speed" / Int16ub,
    "mileage_total" / Int32ub,
    "voltage_total" / Int16ub,
    "current_total" / Int16ub,
    "soc" / Int8ub,
    "dcdc_state" / Int8ub,
    "gear_state" / Int8ub,
    "insulation_resistance" / Int16ub,
    "brake_padel" / Int8ub,
    "accelerator_padel" / Int8ub,
)

"""
GB/T 32960.3-2025 chp7.2.4.1 table10
"""
whole_vehicle_data_2025 = Struct(
    "vehicle_state" / Int8ub,
    "charge_state" / Int8ub,
    "operate_state" / Int8ub,
    "vehicle_speed" / Int16ub,
    "mileage_total" / Int32ub,
    "voltage_total" / Int16ub,
    "current_total" / Int16ub,
    "soc" / Int8ub,
    "dcdc_state" / Int8ub,
    "gear_state" / Int8ub,
    "insulation_resistance" / Int16ub,
)