from common_items import *
from payload_login import login_2016, login_2025
from payload_data import data_2016, data_2025
"""
GB/T 32960.3-2016 chp6.2 table2
GB/T 32960.3-2025 chp6.2 table2
"""
rtm_ver = Enum(Int16ub,
    protocol_2016=0x2323,
    protocol_2025=0x2424,
    )

rtm_msg = Struct(
    "starter"   / rtm_ver,
    "msg_type"  / LazyBound(lambda: msg_types),
    "ack"       / LazyBound(lambda: ack_flags),
    "vin"       / PaddedString(17, "ascii"),
    "enc"       / Enum(Int8ub,
        uncrypted=0x01,
        rsa=0x02,
        aes=0x03,
        # start of newly defined in 2025 protocol
        sm2=0x04, 
        sm4=0x05,
        # end of newly defined in 2025 protocol
        abnormal=0xfe,
        invalid=0xff),
    "payload"   / Prefixed(
        Int16ub,
        LazyBound(lambda: payload_mapping),
    ),
    "checksum"  / Int8ub,
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
        # For 2025 protocol
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.login): login_2025,
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.realtime): data_2025,
        (rtm_ver.protocol_2025, ack_flags.command, msg_types.supplimentary): data_2025,
    },
    # Normally the ack message contains only timestamp
    default=IfThenElse(this.ack!=ack_flags.command, Struct("timestamp"/RtmTs), GreedyBytes),
)

if __name__=='__main__':
    test_msgs = (
        # Login test
        '242401fe484155563442474e365335303032323139010036190a1b140202000c3839383630393234373930303233313636363036010130524a504541303048415530414146313331303031393535d5',
        '242401fe484155563442474e365335303032323139010067190a1b140202000c383938363039323437393030323331363636303602010230524a50454130304841553041414631333130303139353530524a50454130304841553041414631333130303139353630524a504541303048415530414146313331303031393537d5',
        '232301fe484155563442474e365335303032323139010066190a1b140202000c3839383630393234373930303233313636363036031830524a50454130304841553041414631333130303139353530524a50454130304841553041414631333130303139353630524a504541303048415530414146313331303031393537d5',
        # While vehicle data test
        '242402fe484155563442474e365335303032323139010026190a1b14020201ffffffffffffffffffffffffffffffffffffff010003aabbcc0004aabbccddd5',
        '232302fe484155563442474e36533530303232313901001b190a1b14020201ffffffffffffffffffffffffffffffffffffffffd5',
        # e-Motor data test
        '232302fe484155563442474e365335303032323139010020190a1b1402020202fffffffffffffffffffffffffefefefefefefefefefefefed5',
        '242402fe484155563442474e365335303032323139010029190a1b1402020202fffffffffffffffffffffefefefefefefefefefeff010003aabbcc0004aabbccddd5',
        # Engine data test
        '232302fe484155563442474e36533530303232313901000c190a1b14020204ffffffffffd5',
        '242402fe484155563442474e365335303032323139010016190a1b14020204ffffff010003aabbcc0004aabbccddd5',
        # GNSS data test
        '232302fe484155563442474e365335303032323139010010190a1b14020205ffffffffffffffffffd5',
        '242402fe484155563442474e36533530303232313901001e190a1b14020205ffffffffffffffffffffff010003aabbcc0004aabbccddd5',
        # Pack extrema data test
        '232302fe484155563442474e365335303032323139010015190a1b14020206ffffffffffffffffffffffffffffd5',
        # Warnings data test
        '232302fe484155563442474e36533530303232313901002c190a1b14020207030000000300000007000100030008000200080003000c0004000d000100060920000a000bd5',
        '242402fe484155563442474e36533530303232313901003e190a1b14020206030000000300000007000100030008000200080003000c0004000d000100060920000a000b0200030103ff010003aabbcc0004aabbccddd5',
        # Cell volts data test
        '232302fe484155563442474e36533530303232313901002a190a1b1402020802ffffffffffffffffff04ffffffffffffffffffffffffffffffffff03ffffffffffffd5',
        '242402fe484155563442474e365335303032323139010031190a1b1402020702ffffffffff0004ffffffffffffffffffffffffff0003ffffffffffffff010003aabbcc0004aabbccddd5',
        # Probe temps data test
        '232302fe484155563442474e365335303032323139010013190a1b1402020902ff0000050005ffffffffffd5',
        '242402fe484155563442474e365335303032323139010020190a1b1402020802ff0000050005ffffffffffff010003aabbcc0004aabbccddd5',
        # Oen-define data test
        '232302fe484155563442474e365335303032323139010019190a1b140202800010fefefefefefefefefefefefefefefefed5',
        # Ack test
        '24240101484155563442474e365335303032323139010006190a1b14020218',
    )
    
    for msg in test_msgs:
        print(rtm_msg.parse(bytes.fromhex(msg)))
