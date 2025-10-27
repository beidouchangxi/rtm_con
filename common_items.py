from construct import (
    Lazy, LazyBound, Peek, 
    Error, Probe, this,
    Switch, RepeatUntil, GreedyRange,
    Bytes, GreedyBytes, 
    Struct, Const, Enum, Prefixed, Array, 
    PaddedString,
    Int8ub, Int16ub, Int32ub,
)

"""
GB/T 32960.3-2016 chp6.4 table5
GB/T 32960.3-2025 chp6.4 table5
"""
rtm_ts = Int8ub[6]