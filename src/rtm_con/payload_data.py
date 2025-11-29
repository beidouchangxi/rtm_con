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

from rtm_con.common_items import (
    HexAdapter,
    rtm_ts,
    payload_sig,
    data_types_2016,
    data_types_2025,
)
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
GB/T 32960.3-2016 chp7.2.1 table7
"""
data_2016 = Struct(
    "timestamp" / rtm_ts,
    "data_list" / LazyBound(lambda: GreedyRange(data_item_2016)),
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

data_item_2025 = Struct(
    "data_type" / data_types_2025,
    "data_content" / Switch(
        lambda this: this.data_type,
        DATA_ITEM_MAPPING_2025,
        # For 2025 protocol, as there are signature_starter and signature at the end
        # For unknown data type, try to read until 0xff, this will generate some single byte data items (as _peek_byte is hidden)
        default=RepeatUntil(
            lambda obj, lst, ctx: (lst and lst[-1]._peek_byte==0xff),
            Struct(
                "data_byte" / Int8ub,
                "_peek_byte" / Peek(Int8ub),
            )
        )
    ),
    "_peek_type" / Peek(Int8ub),
)

data_items_2025 = RepeatUntil(
    lambda obj, lst, ctx: (lst and lst[-1]._peek_type==0xff),
    data_item_2025,
)