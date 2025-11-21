from construct import Struct, Int16ub

from rtm_con.common_items import RtmTs

"""
GB/T 32960.3-2016 chp7.3 table20
GB/T 32960.3-2025 chp7.3 table28
"""
logout_2016 = logout_2025 = Struct(
    "timestamp" / RtmTs,
    "session_id" / Int16ub,
)


""" 
GB/T 32960.3-2016 chp7.5 table22
GB/T 32960.3-2025 chp7.5 table30
"""
plt_logout_2016 = plt_logout_2025 = Struct(
    "timestamp" / RtmTs,
    "session_id" / Int16ub,
)