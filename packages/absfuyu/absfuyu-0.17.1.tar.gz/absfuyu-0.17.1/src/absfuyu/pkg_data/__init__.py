"""
ABSFUYU
-------
Package data
"""

import ast as __ast
import importlib.resources as __res
import zlib as __zlib


DATA_LIST = [
    "dummy", "punishment_windows",
]

def __data_validate(data_name: str) -> bool:
    """Validate if data exist"""
    if data_name not in DATA_LIST:
        return False
    else:
        return True

def __load_data_string(data_name: str):
    """Load data and convert into string"""
    data = __res.read_binary("absfuyu.pkg_data",f"{data_name}.dat")
    decompressed_data = __zlib.decompress(data).decode()
    return decompressed_data

def __data_string_to_list(data_string: str):
    """Convert data to list"""
    data = __ast.literal_eval(data_string)
    return data

def loadData(data_name: str):
    """Load data"""
    if __data_validate(data_name):
        return __data_string_to_list(__load_data_string(data_name))
    else:
        return None