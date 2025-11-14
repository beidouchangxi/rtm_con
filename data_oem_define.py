from common_items import *

"""
GB/T 32960.3-2016 chp7.2.3.8 table19
GB/T 32960.3-2025 chp7.2.4.12 table27
"""
oem_define_data_2016 = oem_define_data_2025 = HexAdapter(con=Prefixed(Int16ub, GreedyBytes))