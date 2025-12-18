from functools import reduce

from construct import (
    Int16ub,
    Int8ub,
    Struct,
    LazyBound,
    PaddedString,
    Prefixed,
    Checksum,
    Tell,
    Switch,
    this,
)

from rtm_con.types_common import enc_algos, rtm_ver, ack_flags
from rtm_con.types_msg import payload_mapping, msg_types
from rtm_con.utilities import GoThoughDict

"""
GB/T 32960.3-2016 chp6.2 table2
GB/T 32960.3-2025 chp6.2 table2
"""
msg = Struct( # Only parse the message without verifying the checksum
    "starter" / rtm_ver, 
    "msg_type" / msg_types,
    "ack" / ack_flags,
    "vin" / PaddedString(17, "ascii"),
    "enc" / enc_algos,
    "payload" / Prefixed(Int16ub, LazyBound(lambda: Switch(payload_mapping, GoThoughDict()))),
    "checksum" / Int8ub,
)


def check_body(ths): # Find the data to be checksummed
    ths._io.seek(ths._checking_start)
    body = ths._io.read(ths._checking_end-ths._checking_start)
    ths._io.seek(ths._checking_end)
    return reduce(lambda x,y: x^y, body)

msg_checked = Struct( # Calculate and verify automatically the checksum
    "starter" / rtm_ver, 
    "_checking_start" / Tell,
    "msg_type" / msg_types,
    "ack" / ack_flags,
    "vin" / PaddedString(17, "ascii"),
    "enc" / enc_algos,
    "payload" / Prefixed(Int16ub, LazyBound(lambda: Switch(payload_mapping, GoThoughDict()))),
    "_checking_end" / Tell,
    "checksum" / Checksum(Int8ub, check_body, this),
)