from msg_format import *
from payload_data import *
from construct import Container, ListContainer
from collections import Counter

class FlattenedMsg(dict):
    def __init__(self, msg_obj):
        super().__init__()
        for k_m, v_m in msg_obj.items():
            if k_m=="payload":
                if isinstance(v_m, Container):
                    # If payload is parsed, disassemble payload
                    for k_p, v_p in v_m.items():
                        if k_p=="data_list":
                            # Data blocks
                            self._flatten_data_list(v_p)
                        elif isinstance(v_p, Container):
                            # For signature or other nested Containers
                            for k_s, v_s in v_p.items():
                                self._checkout(k_s, v_s, prefix=f"{k_p}-")
                        else:
                            # Nromal items like timestamp
                            self._checkout(k_p, v_p)
                else:
                    # For unkown payload
                    self._checkout(k_m, v_m)
            else:
                self._checkout(k_m, v_m)

    def _flatten_data_list(self, data_blocks):
        # Firstly check if there is dupilicated ones
        duplication_indexs = self._check_data_duplication(data_blocks)
        for block_index, data_block in enumerate(data_blocks):

            if d_index:=duplication_indexs[block_index]:
                duplication_prefix = f"(+{duplication_indexs[block_index]})"
            else:
                duplication_prefix = ""
            
            match data_block.data_type:
                case data_types_2016.emotor | data_types_2025.emotor:
                    self._flatten_emotor_block(data_block, duplication_prefix)
                case data_types_2016.warnings | data_types_2025.warnings:
                    self._flatten_warnings_block(data_block, duplication_prefix)
                case data_types_2016.cell_volts | data_types_2025.cell_volts:
                    self._flatten_cell_volts_block(data_block, duplication_prefix)
                case data_types_2016.probe_temps | data_types_2025.probe_temps:
                    self._flatten_probe_temps_block(data_block, duplication_prefix)
                case _:
                    if isinstance(data_block.data_content, Container):
                        # For a "normal" data block, which contains a lots of data items
                        for d_name, d_value in data_block.data_content.items():
                            if isinstance(d_value, Container):
                                # For gear state, GNSS bits, and general warnings
                                # There are some unnecessary layers here, but just ignore them
                                for sub_d_name, sub_d_value in d_value.items():
                                    self._checkout(sub_d_name, sub_d_value, prefix=duplication_prefix)
                            elif isinstance(d_value, ListContainer):
                                # For warning codes
                                self._checkout(d_name, list(d_value), prefix=duplication_prefix)
                            else:
                                # For a normal data item
                                self._checkout(d_name, d_value, prefix=duplication_prefix)
                    else:
                        # Self-defined data?
                        self._checkout(data_block.data_type, "pass", prefix=duplication_prefix)    

    def _check_data_duplication(self, data_blocks):
        '''
        Check if there is duplicated data blocks in the data list.
        return a dict of data block index and duplication index.
        '''
        results = {} # index: duplication_index
        count = {} # data_type: count
        for block_index, data_block in enumerate(data_blocks):
            if data_block.data_type not in count.keys():
                results[block_index] = count[data_block.data_type] = 0
            else:
                count[data_block.data_type] += 1
                results[block_index] = count[data_block.data_type]
        return results

    def _flatten_emotor_block(self, data_block_em, duplication_prefix):
        for em_block in data_block_em.data_content:
            for k_em, v_em in em_block.items():
                self._checkout(k_em, v_em, prefix=f"{duplication_prefix}em{em_block.index}-")
    
    def _flatten_warnings_block(self, data_block_warnings, duplication_prefix):
        gw_flags = {}
        for k_w, v_w in data_block_warnings.data_content.items():
            if k_w=="general_warnings":
                for w_name, w_flag in v_w.items():
                    self._checkout(w_name, w_flag, prefix=duplication_prefix)
                    gw_flags[w_name] = w_flag
            elif isinstance(v_w, ListContainer):
                # As the general warning flags and codes are seperated and linked, we have to put them together here
                # If no code for a general warning, it would be a boolean True/False
                # Else the general warning would be a level integer (positive/negative for flag True/False)
                if k_w=="general_warning_list":
                    for gw_info in v_w:
                        if gw_flags.get(gw_info.warning, False):
                            self._checkout(gw_info.warning, gw_info.level, prefix=duplication_prefix)
                        else:
                            self._checkout(gw_info.warning, 0-gw_info.level, prefix=duplication_prefix)
                else: # For warning codes
                    self._checkout(k_w, list(v_w), prefix=duplication_prefix)
            else:
                self._checkout(k_w, v_w, prefix=duplication_prefix)

    def _flatten_cell_volts_block(self, data_block_cell_volts, duplication_prefix):
        for pack_block in data_block_cell_volts.data_content:
            pack_prefix = f"{duplication_prefix}p{pack_block.index}-"
            for k_pv, v_pv in pack_block.items():
                if k_pv!="cell_volts":
                    self._checkout(k_pv, v_pv, prefix=pack_prefix)
                else:
                    cell_start_index = pack_block.cell_start_index if hasattr(pack_block, "cell_start_index") else 0
                    for cell_index, cell_volt in enumerate(pack_block.cell_volts):
                        self._checkout(f"{pack_prefix}c{cell_start_index+cell_index}-volt", cell_volt)
    
    def _flatten_probe_temps_block(self, data_block_probe_temps, duplication_prefix):
        for pack_block in data_block_probe_temps.data_content:
            pack_prefix = f"{duplication_prefix}p{pack_block.index}-"
            for probe_index, probe_temp in enumerate(pack_block.probe_temps):
                self._checkout(f"{pack_prefix}pr{probe_index}-temp", probe_temp)
    
    def _checkout(self, k, v, *, prefix="", postfix=""):
        if not isinstance(k, str):
            k = str(k)
        if k.startswith("_"):
            return
        self[f"{prefix}{k}{postfix}"] = v