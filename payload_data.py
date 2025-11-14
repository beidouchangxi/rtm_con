from common_items import *
from data_whole_vehicle import whole_vehicle_data_2016, whole_vehicle_data_2025
from data_emotor import emotor_data_2016, emotor_data_2025
from data_engine import engine_data_2016, engine_data_2025
from data_gnss import gnss_data_2016, gnss_data_2025
from data_pack_extrema import pack_extrema_data_2016
from data_warnings import warnings_data_2016, warnings_data_2025
from data_cell_volts import cell_volts_data_2016, cell_volts_data_2025
from data_probe_temps import probe_temps_data_2016, probe_temps_data_2025
from data_oem_define import oem_define_data_2016, oem_define_data_2025

"""
GB/T 32960.3-2016 chp7.2.1 table7
"""
data_2016 = Struct(
    "timestamp" / RtmTs,
    "data_list" / LazyBound(lambda: GreedyRange(data_item_2016)),
)

"""
GB/T 32960.3-2025 chp7.2.1 table7
"""
data_2025 = Struct(
    "timestamp" / RtmTs,
    "data_list" / LazyBound(lambda: data_items_2025),
    "sig_starter" / HexAdapter(con=Const(b'\xff')),
    "sig" / payload_sig,
)

data_item_2016 = Struct(
    "data_type" / data_types_2016,
    "data_content" / Switch(
        lambda this: this.data_type,
        {
            data_types_2016.whole_vehicle: whole_vehicle_data_2016,
            data_types_2016.emotor: emotor_data_2016,
            data_types_2016.engine: engine_data_2016,
            data_types_2016.gnss: gnss_data_2016,
            data_types_2016.pack_extrema: pack_extrema_data_2016,
            data_types_2016.warnings: warnings_data_2016,
            data_types_2016.cell_volts: cell_volts_data_2016,
            data_types_2016.probe_temps: probe_temps_data_2016,
        } | { # oem defined data
            k:oem_define_data_2016 for k in range(0x80, 0xfe+1)
        },
        default=HexAdapter(con=GreedyBytes), # unkown data
    ),
)

data_item_2025 = Struct(
    "data_type" / data_types_2025,
    "data_content" / Switch(
        lambda this: this.data_type,
        {
            data_types_2025.whole_vehicle: whole_vehicle_data_2025,
            data_types_2025.emotor: emotor_data_2025,
            data_types_2025.engine: engine_data_2025,
            data_types_2025.gnss: gnss_data_2025,
            data_types_2025.warnings: warnings_data_2025,
            data_types_2025.cell_volts: cell_volts_data_2025,
            data_types_2025.probe_temps: probe_temps_data_2025,
        } | { # oem defined data
            k:oem_define_data_2025 for k in range(0x80, 0xfe+1)
        },
        default=HexAdapter(con=GreedyBytes), # unkown data
    ),
    "_peek_type" / Peek(Int8ub),
)

data_items_2025 = RepeatUntil(
    lambda obj, lst, ctx: (lst and lst[-1]._peek_type==0xff),
    data_item_2025,
)