from functools import reduce

from construct import (
    Enum,
    Int16ub,
    Int8ub,
    Struct,
    LazyBound,
    PaddedString,
    Prefixed,
    Checksum,
    Tell,
    IfThenElse,
    GreedyBytes,
    Switch,
    this,
)

from rtm_con.common_items import enc_algos, rtm_ts, rtm_ver, ack_flags, msg_types
from rtm_con.payload_login import login_2016, plt_login_2016, login_2025, plt_login_2025
from rtm_con.payload_logout import logout_2016, plt_logout_2016, logout_2025, plt_logout_2025
from rtm_con.payload_data import data_2016, data_2025
from rtm_con.payload_activation import activation_2025, activation_response_2025
from rtm_con.payload_payload_key_sync import payload_key_sync_2025
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

"""
GB/T 32960.3-2016 chp6.3.1 table3
"""
MSG_TYPE_MAPPING_2016 = {
    msg_types.login: login_2016,
    msg_types.realtime: data_2016,
    msg_types.supplimentary: data_2016,
    msg_types.logout: logout_2016,
    msg_types.plt_login: plt_login_2016,
    msg_types.plt_logout: plt_logout_2016,
}

"""
GB/T 32960.3-2025 chp6.3.1 table3
"""
MSG_TYPE_MAPPING_2025 = {
    msg_types.login: login_2025,
    msg_types.realtime: data_2025,
    msg_types.supplimentary: data_2025,
    msg_types.logout: logout_2025,
    msg_types.plt_login: plt_login_2025,
    msg_types.plt_logout: plt_logout_2025,
    msg_types.activation: activation_2025,
    msg_types.activation_response: activation_response_2025,
    msg_types.payload_key_sync: payload_key_sync_2025,
}

def payload_mapping(ths):
    if ths.ack==ack_flags.command:
        if ths.starter==rtm_ver.protocol_2016 and ths.msg_type in MSG_TYPE_MAPPING_2016:
            # For 2016 protocol known message types
            return MSG_TYPE_MAPPING_2016[ths.msg_type]
        elif ths.starter==rtm_ver.protocol_2025 and ths.msg_type in MSG_TYPE_MAPPING_2025:
            # For 2025 protocol known message types
            return MSG_TYPE_MAPPING_2025[ths.msg_type]
        else:
            # For unkown message types
            return GreedyBytes
    else:
        # Normally the ack message contains only timestamp
        return Struct("timestamp"/rtm_ts)