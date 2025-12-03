import datetime
from rtm_con import rtm_msg_checked

data = {'starter': 'protocol_2025',
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

msg = rtm_msg_checked.build(data)
print(msg.hex())