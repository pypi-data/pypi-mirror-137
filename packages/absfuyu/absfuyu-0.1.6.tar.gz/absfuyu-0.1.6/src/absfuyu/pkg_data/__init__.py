"""
ABSFUYU
-------
Package data
"""

import ast
import importlib.resources as res
import zlib

def LoadData(data_name: str):
    data = res.read_binary("absfuyu.pkg_data",f"{data_name}.dat")
    decompressed_data = zlib.decompress(data).decode()
    return decompressed_data

def toList(data_string: str):
    data = ast.literal_eval(data_string)
    return data