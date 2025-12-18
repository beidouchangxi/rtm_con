from construct import Struct, Enum, Int8ub, Int16ub, this

from rtm_con.utilities import HexAdapter

sig_algos = Enum(Int8ub, 
        sm2=1,
        rsa=2,
        ecc=3,
)

"""
GB/T 32960.3-2025 chp7.2.2 table8
"""
sig_con = Struct(
    "algo" / sig_algos,
    "r_len" / Int16ub,
    "r_value" / HexAdapter(this.r_len),
    "s_len" / Int16ub,
    "s_value" / HexAdapter(this.s_len),
)