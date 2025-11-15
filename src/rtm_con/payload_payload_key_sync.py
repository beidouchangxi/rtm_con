from rtm_con.common_items import *

"""
GB/T 32960.3-2025 chp7.6 table31
"""
payload_key_sync_2025 = Struct(
    "payload_enc" / enc_algos,
    "payload_key_len" / Int16ub,
    "payload_key" / HexAdapter(this.payload_key_len),
    "key_starttime" / RtmTs,
    "key_endtime" / RtmTs,
)