from construct import (
    Lazy, LazyBound, Peek, Adapter,
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

"""
Handle Numbers with factor, offset and unit
"""
class DataItem(object):
    def __init__(self, value, unit, validity):
        self.value = value
        self.unit = unit
        self.valid = validity
    def __repr__(self):
        if self.valid:
            return "<DataItem %s %s>" % (self.value, self.unit)
        elif self.valid==None:
            return "<DataItem Invalid>"
        else:
            return "<DataItem Abnormal>"
    
    def __str__(self):
        if self.valid:
            return "%s %s" % (self.value, self.unit)
        elif self.valid==None:
            return "Invalid"
        else:
            return "Abnormal"
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)
    
    def __bool__(self):
        return bool(self.value)
    
    def __eq__(self, other):
        if isinstance(other, PhysicalValue):
            return self.value == other.value and self.unit == other.unit
        return self.value == other

class DataItemAdapter(Adapter):
    def __init__(self, subcon, unit, factor=1, offset=0, *, validation=True):
        super().__init__(subcon)
        self.factor = factor
        self.offset = offset
        self.unit = unit
        self.validation = validation
        self.abnormal_value = 2**(self.sizeof()*8)-2
        self.invalid_value = 2**(self.sizeof()*8)-1
    
    def _decode(self, raw_value, context, path):
        validity = True
        if self.validation:
            if raw_value==self.abnormal_value:
                validity = False
            elif raw_value==self.invalid_value:
                validity = None
        return DataItem(raw_value*self.factor + self.offset, self.unit, validity)
    
    def _encode(self, phy_value, context, path):
        if isinstance(phy_value, DataItem):
            phy_value = phy_value.value
        raw_value = (phy_value-self.offset)/self.factor
        return int(round(raw_value))