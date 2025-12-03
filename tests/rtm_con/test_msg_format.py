import datetime
import pytest

mf = pytest.importorskip("rtm_con.msg_format")

def check_data(test_samples):
    for msg_con in (mf.rtm_msg, mf.rtm_msg_checked):
        for msg_hex, target in test_samples:
            print(msg_hex)
            print(target)
            b = bytes.fromhex(msg_hex)
            msg = msg_con.parse(b)
            for key, value in target.items():
                assert msg[key] == value, f"Parsed data doesn't match expectation\nraw msg:\n{msg_hex}\ntarget:\n{target}"
            assert msg_con.build(target).hex() == msg_hex

def test_rtmt_msg_login():
    check_data((
        ('242401fe484155563442474e365335303032323139010036190a1b140202000c3839383630393234373930303233313636363036010130524a50454130304841553041414631333130303139353596',
            {'starter': 'protocol_2025',
            'msg_type': 'login',
            'ack': 'command',
            'vin': 'HAUV4BGN6S5002219',
            'enc': 'uncrypted',
            'payload': {'timestamp': datetime.datetime(2025, 10, 27, 20, 2, 2),
                        'session_id': 12,
                        'iccid': '89860924790023166606',
                        'bms_total': 1,
                        'pack_per_bms': [1],
                        'pack_sn_list': [['0RJPEA00HAU0AAF131001955']]},
            'checksum': 150}
            ),
        ('242401fe484155563442474e365335303032323139010067190a1b140202000c383938363039323437393030323331363636303602010230524a50454130304841553041414631333130303139353530524a50454130304841553041414631333130303139353630524a504541303048415530414146313331303031393537c7',
            {'starter': 'protocol_2025',
            'msg_type': 'login',
            'ack': 'command',
            'vin': 'HAUV4BGN6S5002219',
            'enc': 'uncrypted',
            'payload': {'timestamp': datetime.datetime(2025, 10, 27, 20, 2, 2),
                        'session_id': 12,
                        'iccid': '89860924790023166606',
                        'bms_total': 2,
                        'pack_per_bms': [1, 2],
                        'pack_sn_list': [['0RJPEA00HAU0AAF131001955'],
                                        ['0RJPEA00HAU0AAF131001956',
                                        '0RJPEA00HAU0AAF131001957']]},
            'checksum': 199},
            ),
        ('232301fe484155563442474e365335303032323139010066190a1b140202000c3839383630393234373930303233313636363036031830524a50454130304841553041414631333130303139353530524a50454130304841553041414631333130303139353630524a504541303048415530414146313331303031393537dc',
            {'starter': 'protocol_2016',
            'msg_type': 'login',
            'ack': 'command',
            'vin': 'HAUV4BGN6S5002219',
            'enc': 'uncrypted',
            'payload': {'timestamp': datetime.datetime(2025, 10, 27, 20, 2, 2),
                        'session_id': 12,
                        'iccid': '89860924790023166606',
                        'bms_total': 3,
                        'pack_sn_len': 24,
                        'pack_sn': ['0RJPEA00HAU0AAF131001955',
                                    '0RJPEA00HAU0AAF131001956',
                                    '0RJPEA00HAU0AAF131001957']},
            'checksum': 220},
        ),
    ))