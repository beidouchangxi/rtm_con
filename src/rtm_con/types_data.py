from construct import Enum, Int8ub

from rtm_con.data_whole_vehicle import whole_vehicle_data_2016, whole_vehicle_data_2025
from rtm_con.data_emotor import emotor_data_2016, emotor_data_2025
from rtm_con.data_engine import engine_data_2016, engine_data_2025
from rtm_con.data_gnss import gnss_data_2016, gnss_data_2025
from rtm_con.data_pack_extrema import pack_extrema_data_2016
from rtm_con.data_warnings import warnings_data_2016, warnings_data_2025
from rtm_con.data_cell_volts import cell_volts_data_2016, cell_volts_data_2025
from rtm_con.data_probe_temps import probe_temps_data_2016, probe_temps_data_2025
from rtm_con.data_oem_define import oem_define_data_dummy

"""
GB/T 32960.3-2016 chp7.2.2 table8
GB/T 32960.3-2016 anxB.3.5.2.2 tableB.3
"""
data_types_2016 = Enum(Int8ub, 
    whole_vehicle=0x01,
    emotor=0x02,
    fuel_cell_system=0x03,
    engine=0x04,
    gnss=0x05,
    pack_extrema=0x06,
    warnings=0x07,
    cell_volts=0x08,
    probe_temps=0x09,
    # 0x0a~0x2f platform reserve
    # 0x30~0x7f reserve
    # 0x80~0xfe oem define
)

"""
GB/T 32960.3-2025 chp7.2.3 table9
"""
data_types_2025 = Enum(Int8ub, 
    whole_vehicle=0x01,
    emotor=0x02,
    fuel_cell_system=0x03,
    engine=0x04,
    gnss=0x05,
    warnings=0x06,
    cell_volts=0x07,
    probe_temps=0x08,
    # 0x09~0x2f platform reserve
    fuel_cell_stacks=0x30,
    super_capacitors=0x31,
    super_capacitor_extrema=0x32,
    # 0x33~0x7f reserve
    # 0x80~0xfe oem define
    signature_starter=0xff,
)

DATA_ITEM_MAPPING_2016 = {
    data_types_2016.whole_vehicle: whole_vehicle_data_2016,
    data_types_2016.emotor: emotor_data_2016,
    data_types_2016.engine: engine_data_2016,
    data_types_2016.gnss: gnss_data_2016,
    data_types_2016.pack_extrema: pack_extrema_data_2016,
    data_types_2016.warnings: warnings_data_2016,
    data_types_2016.cell_volts: cell_volts_data_2016,
    data_types_2016.probe_temps: probe_temps_data_2016,
} | { # Use dummy hex for preseve the OEM define data, hack the dict if you need to parse it
    k:oem_define_data_dummy for k in range(0x80, 0xfe+1)
}

DATA_ITEM_MAPPING_2025 = {
    data_types_2025.whole_vehicle: whole_vehicle_data_2025,
    data_types_2025.emotor: emotor_data_2025,
    data_types_2025.engine: engine_data_2025,
    data_types_2025.gnss: gnss_data_2025,
    data_types_2025.warnings: warnings_data_2025,
    data_types_2025.cell_volts: cell_volts_data_2025,
    data_types_2025.probe_temps: probe_temps_data_2025,
} | { # Use dummy hex for preseve the OEM define data, hack the dict if you need to parse it
    k:oem_define_data_dummy for k in range(0x80, 0xfe+1)
}
