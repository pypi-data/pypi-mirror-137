#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
List Module
-----------
Some list methods

Contain:
- stringify
- list_sort
- list_freq
"""


# Module level
##############################################################
__all__ = [
    "stringify", "list_sort", "list_freq",
]


# Library
##############################################################
from typing import Any as __Any
from typing import Dict as __Dict
from typing import List as __List



# Function
##############################################################
def stringify(lst: __List[__Any]) -> __List[str]:
    """
    Summary
    -------
    Convert all item in list into string

    Parameters
    ----------
    lst : list
        list of item

    Returns
    -------
    list
        A list with all items with type: string
    """

    return [str(x) for x in lst]



def list_sort(lst: __List[__Any], reverse: bool = False) -> list:
    """
    Summary
    -------
    Sort all items (with different type) in list
    
    Parameters
    ----------
    lst : list
        list of item
    
    reverse : bool
        if True then sort in descending order

    Returns
    -------
    list
        A sorted list
    """
    
    type_weights = {}
    for x in lst:
        if type(x) not in type_weights:
            type_weights[type(x)] = len(type_weights)
    output = sorted(
        lst,
        key=lambda x: (type_weights[type(x)], str(x)),
        reverse=reverse
    )
    return output



def list_freq(
        lst: __List[__Any],
        sort: bool = False,
    ) -> __Dict[str,int]:
    """
    Summary
    -------
    Find frequency of each item in list

    Parameters
    ----------
    lst : list
        list of item
    
    sort : bool
        if True: sort the dict in ascending order

    Returns
    -------
    dict
        A dict that show frequency
    """

    output = {}
    if sort:
        data = list_sort(lst)
    else:
        data = lst

    for x in data:
        if x not in output:
            output[x] = 1
        else:
            output[x] += 1
    return output