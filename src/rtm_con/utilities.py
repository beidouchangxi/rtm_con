from construct import Adapter, Bytes

class GoThoughDict(dict):
    '''
    A dict that returns the key itself when key is missing
    Used in construct.Switch to handle the switching logic in a function
    '''
    def __missing__(self, key):
        return key
    def __contains__(self, key):
        return True
    def get(self, key, default=None):
        return key


class HexAdapter(Adapter):
    '''
    Adapter to convert bytes to hex string and vice versa
    '''
    def __init__(self, length=None, *, con=None):
        if con is not None:
            super().__init__(con)
        else:
            super().__init__(Bytes(length))
        
    def _decode(self, raw_value, context, path):
        return raw_value.hex()
    
    def _encode(self, phy_value, context, path):
        return bytes.fromhex(phy_value)
