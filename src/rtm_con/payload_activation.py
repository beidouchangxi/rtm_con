from construct import (
    Struct,
    PaddedString,
    Int16ub,
    this,
    Enum,
    Int8ub,
)
from rtm_con.common_items import (
    RtmTs,
    HexAdapter,
    payload_sig,
)

"""
GB/T 32960.3-2025 anxB.3.5.5 tableB.3
"""
activation_2025 = Struct(
    "timestamp" / RtmTs,
    "sec_chip_id" / PaddedString(16, "ascii"),
    "pubkey_len" / Int16ub,
    "pubkey" / HexAdapter(this.pubkey_len),
    "vin" / PaddedString(17, "ascii"),
    "sig" / payload_sig,
)


""" 
GB/T 32960.3-2025 anxB.3.5.6 tableB.4
"""
activation_response_2025 = Struct(
    "activation_result" / Enum(Int8ub, ok=1, nok=2),
    "activation_info" / Enum(Int8ub, ok=1, sec_chip_used=2, vin_duplicate=3),
)