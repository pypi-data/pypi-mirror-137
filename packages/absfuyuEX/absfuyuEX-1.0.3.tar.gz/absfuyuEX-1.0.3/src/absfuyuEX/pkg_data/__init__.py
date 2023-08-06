"""
ABSFUYU-EXTRA
-------------
Package data
"""

import ast
import importlib.resources as res
import zlib

DATA_LIST = [
    "perfect_num_35",
]

def _data_validate(data_name: str) -> bool:
    if data_name not in DATA_LIST:
        return False
    else:
        return True

def _load_data_string(data_name: str):
    data = res.read_binary("absfuyuEX.pkg_data",f"{data_name}.dat")
    decompressed_data = zlib.decompress(data).decode()
    return decompressed_data

def _data_string_to_list(data_string: str):
    data = ast.literal_eval(data_string)
    return data

def loadData(data_name: str):
    if _data_validate(data_name):
        return _data_string_to_list(_load_data_string(data_name))
    else:
        return None