from construct import Adapter, Bytes
from datetime import datetime

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

def con_to_pyobj(data_con):
    '''
    Convert a construct parsed object to a pure python object (dict, list, int, str, etc.)
    Mostly used for easier printing and debugging or create test cases
    '''
    def convert(data_con):
        py_types = (int, float, str, bool, list, dict)
        for py_type in py_types:
            if isinstance(data_con, py_type):
                return py_type(data_con)
            elif isinstance(data_con, datetime):
                return data_con
        else:
            return str(data_con)
    py_obj = convert(data_con)
    if isinstance(py_obj, list):
        result = []
        for sub_con in py_obj:
            result.append(con_to_pyobj(sub_con))
        return result
    elif isinstance(py_obj, dict):
        result = {}
        for key, sub_con in py_obj.items():
            if not key.startswith('_'):
                result[key] = con_to_pyobj(sub_con)
        return result
    return py_obj