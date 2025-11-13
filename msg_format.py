from common_items import *
from payload_login import login_2016, plt_login_2016, login_2025, plt_login_2025
from payload_logout import logout_2016, plt_logout_2016, logout_2025, plt_logout_2025
from payload_data import data_2016, data_2025
from functools import reduce
"""
GB/T 32960.3-2016 chp6.2 table2
GB/T 32960.3-2025 chp6.2 table2
"""
rtm_ver = Enum(Int16ub,
    protocol_2016=0x2323,
    protocol_2025=0x2424,
    )

def check_body(ths):
    ths._io.seek(ths._checking_start)
    body = ths._io.read(ths._checking_end-ths._checking_start)
    ths._io.seek(ths._checking_end)
    return reduce(lambda x,y: x^y, body)

rtm_msg = Struct(
    "starter" / rtm_ver, 
    "_checking_start" / Tell,
    "msg_type" / LazyBound(lambda: msg_types),
    "ack" / LazyBound(lambda: ack_flags),
    "vin" / PaddedString(17, "ascii"),
    "enc" / enc_algos,
    "payload" / Prefixed(Int16ub, LazyBound(lambda: payload_mapping)),
    "_checking_end" / Tell,
    "checksum" / Checksum(Int8ub, check_body, this),
)

"""
GB/T 32960.3-2016 chp6.3.1 table3
GB/T 32960.3-2025 chp6.3.1 table3
"""
msg_types = Enum(Int8ub, 
    login=1,
    realtime=2,
    supplimentary=3,
    logout=4,
    plt_login=5,
    plt_logout=6,
    # GB/T 32960.3-2016 chp6.3.1 table3
        # 0x07~0x08 client reserve
        # 0x09~0x7f uplink reserve
        # 0x80~0x82 client reserve
        # 0x83~0xbf downlink reserve
        # 0xc0~0xfe platform reserve
    # GB/T 32960.3-2025 chp6.3.1 table3
        # 0x07~0x0A client reserve
        # 0x0b payload encryption key exchange
        # 0x0c~0x7f uplink reserve
        # 0x80~0x82 client reserve
        # 0x83~0xbf downlink reserve
        # 0xc0~0xfe platform reserve
)

"""
GB/T 32960.3-2016 chp6.3.2 table4
GB/T 32960.3-2025 chp6.3.2 table4
"""
ack_flags = Enum(Int8ub,
    ok=0x01,
    nok=0x02,
    vin_duplicate=0x03,
    vin_unkown=0x04,
    # start of newly defined in 2025 protocol
    signature_invalid=0x05,
    structure_invalid=0x06,
    decryption_failed=0x07,
    # end of newly defined in 2025 protocol
    command=0xfe,
)

payload_mapping = Switch(
    lambda this: (this.starter, this.ack, this.msg_type),
    {
        # For 2016 protocol
        (rtm_ver.protocol_2016, ack_flags.command, msg_types.login): login_2016,
        (rtm_ver.protocol_2016, ack_flags.command, msg_types.realtime): data_2016,
        (rtm_ver.protocol_2016, ack_flags.command, msg_types.supplimentary): data_2016,
        (rtm_ver.protocol_2016, ack_flags.command, msg_types.logout): logout_2016,
        (rtm_ver.protocol_2016, ack_flags.command, msg_types.plt_login): plt_login_2016,
        (rtm_ver.protocol_2016, ack_flags.command, msg_types.plt_logout): plt_logout_2016,
        # For 2025 protocol
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.login): login_2025,
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.realtime): data_2025,
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.supplimentary): data_2025,
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.logout): logout_2025,
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.plt_login): plt_login_2025,
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.plt_logout): plt_logout_2025,
    },
    # Normally the ack message contains only timestamp
    default=IfThenElse(this.ack!=ack_flags.command, Struct("timestamp"/RtmTs), GreedyBytes),
)