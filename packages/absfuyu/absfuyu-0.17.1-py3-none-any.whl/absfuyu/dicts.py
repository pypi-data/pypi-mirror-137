#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dict Module
-----------
Some dict methods

Contain:
- dict_int_analyze
"""



# Module level
##############################################################
__all__ = [
    "dict_int_analyze",
]




# Library
##############################################################
from typing import Dict as __Dict
from typing import TypeVar as __TypeVar




# Define type
##############################################################
Number = __TypeVar("Number", int, float)



# Function
##############################################################
def dict_int_analyze(dct: __Dict[str,Number]):
    """
    Analyze all the key values (int, float) in dict then return highest/lowest index
    """

    input_ = list(dct.items())
    max, min = input_[0][1], input_[0][1]
    max_index = []
    min_index = []
    max_list = []
    min_list = []

    for i in range(len(input_)):
      if input_[i][1] > max:
            max = input_[i][1]
      elif input_[i][1] < min:
            min = input_[i][1]
    
    for i in range(len(input_)):
      if input_[i][1] == max:
            max_index.append(i)
      elif input_[i][1] == min:
            min_index.append(i)
    
    for x in max_index:
        max_list.append(input_[x])

    for x in min_index:
        min_list.append(input_[x])

    
    output = {
        "max_index": max_index,
        "min_index": min_index,
        "max": max_list,
        "min": min_list
    }

    return output