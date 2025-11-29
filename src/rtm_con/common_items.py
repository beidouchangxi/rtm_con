from datetime import datetime, timezone, timedelta

from construct import (
    Adapter,
    this,
    Bytes,
    Struct,
    Enum,
    Int8ub,
    Int16ub,
)

'''
A dict that returns the key itself when key is missing
Used in Switch to handle the switch in the function
'''
class GoThoughDict(dict):
    def __missing__(self, key):
        return key

"""
Handle Numbers with factor, offset and unit
"""
class DataItem(object):
    def __init__(self, value, unit, validity):
        self.value = value
        self.unit = unit
        self.valid = validity
    def __repr__(self):
        return f"DataItem({self.value}, {self.unit}, {self.valid})"
    
    def __str__(self):
        if self.valid:
            if self.unit:
                return "%s %s" % (self.value, self.unit)
            else:
                return "%s" % (self.value)
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
        if isinstance(other, type):
            return self.value == other.value and self.unit == other.unit and self.valid == other.valid
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

class HexAdapter(Adapter):
    def __init__(self, length=None, *, con=None):
        if con is not None:
            super().__init__(con)
        else:
            super().__init__(Bytes(length))
        
    def _decode(self, raw_value, context, path):
        return raw_value.hex()
    
    def _encode(self, phy_value, context, path):
        return bytes.fromhex(phy_value)

"""
GB/T 32960.3-2016 chp6.2 table2
GB/T 32960.3-2025 chp6.2 table2
"""
rtm_ver = Enum(Int16ub,
    protocol_2016=0x2323,
    protocol_2025=0x2424,
    )

"""
GB/T 32960.3-2016 chp6.2 table2
GB/T 32960.3-2025 chp6.2 table2
"""
enc_algos = Enum(Int8ub,
    uncrypted=0x01,
    rsa=0x02,
    aes=0x03,
    # start of newly defined in 2025 protocol
    sm2=0x04, 
    sm4=0x05,
    # end of newly defined in 2025 protocol
    abnormal=0xfe,
    invalid=0xff,
)

"""
GB/T 32960.3-2016 chp6.3.1 table3
GB/T 32960.3-2016 anxB.3.3.1 tableB.2
GB/T 32960.3-2025 chp6.3.1 table3
GB/T 32960.3-2025 anxB.3.3.1 tableB.2
"""
msg_types = Enum(Int8ub, 
    login=0x01,
    realtime=0x02,
    supplimentary=0x03,
    logout=0x04,
    plt_login=0x05,
    plt_logout=0x06,
    heartbeat=0x07,
    time_sync=0x08,
    # start of newly defined in 2025 protocol
    activation=0x09,
    activation_response=0x0a,
    payload_key_sync=0x0b,
    # end of newly defined in 2025 protocol
    get=0x80,
    set=0x81,
    control=0x82,
    # GB/T 32960.3-2016 chp6.3.1 table3
        # 0x09~0x7f uplink reserve
        # 0x83~0xbf downlink reserve
        # 0xc0~0xfe platform reserve
    # GB/T 32960.3-2025 chp6.3.1 table3
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

"""
GB/T 32960.3-2016 chp6.4 table5
GB/T 32960.3-2025 chp6.4 table5
"""
BEIJING_TZ = timezone(timedelta(hours=8))

class RtmTsAdapter(Adapter):
    def __init__(self):
        super().__init__(Bytes(6))
    
    def _decode(self, msg_ts, context, path):
        ts_obj_bj = datetime(msg_ts[0]+2000, msg_ts[1],msg_ts[2],msg_ts[3],msg_ts[4],msg_ts[5]).replace(tzinfo=BEIJING_TZ)
        ts_obj_local = ts_obj_bj.astimezone()
        return ts_obj_local.replace(tzinfo=None)
    
    def _encode(self, ts_obj_local, context, path):
        ts_obj_bj = ts_obj_local.astimezone(BEIJING_TZ)
        return bytes((ts_obj_bj.year%100, ts_obj_bj.month, ts_obj_bj.day, ts_obj_bj.hour, ts_obj_bj.minute, ts_obj_bj.second))

rtm_ts = RtmTsAdapter()

"""
GB/T 32960.3-2025 chp7.2.2 table8
"""
payload_sig = Struct(
    "algo" / Enum(Int8ub, 
        sm2=1,
        rsa=2,
        ecc=3,
    ),
    "r_len" / Int16ub,
    "r_value" / HexAdapter(this.r_len),
    "s_len" / Int16ub,
    "s_value" / HexAdapter(this.s_len),
)

"""
GB/T 32960.3-2016 chp7.2.2 table8
GB/T 32960.3-2016 anxB.3.5.2.2 tableB.3
"""
data_types_2016 = Enum(Int8ub, 
    whole_vehicle=0x01,
    emotor=0x02,
    fuel_cell_system=0x03,
    engine=0x04,
    gnss=0x05,
    pack_extrema=0x06,
    warnings=0x07,
    cell_volts=0x08,
    probe_temps=0x09,
    # 0x0a~0x2f platform reserve
    # 0x30~0x7f reserve
    # 0x80~0xfe oem define
)

"""
GB/T 32960.3-2025 chp7.2.3 table9
"""
data_types_2025 = Enum(Int8ub, 
    whole_vehicle=0x01,
    emotor=0x02,
    fuel_cell_system=0x03,
    engine=0x04,
    gnss=0x05,
    warnings=0x06,
    cell_volts=0x07,
    probe_temps=0x08,
    # 0x09~0x2f platform reserve
    fuel_cell_stacks=0x30,
    super_capacitors=0x31,
    super_capacitor_extrema=0x32,
    # 0x33~0x7f reserve
    # 0x80~0xfe oem define
    signature_starter=0xff,
)