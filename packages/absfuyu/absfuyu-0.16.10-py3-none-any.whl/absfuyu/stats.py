#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Statistic Module
----------------
Statistic

Contain:
- summary(mean , median, std,...)
"""


# Module level
##############################################################
__all__ = [
    "mean", "median", "var", "mode", "std", "percentile",
    "summary",
]


# Library
##############################################################
import math as __math
from typing import Dict as __Dict
from typing import List as __List
from typing import Union as __Union
from typing import TypeVar as __TypeVar

from . import lists as __lists


# Define type
##############################################################
Number = __TypeVar("Number", int, float)



# Function
##############################################################
def mean(
    lst: __List[Number],
    roundup: __Union[int, None] = None,
) -> float:
    """Mean/Average"""

    s = sum(lst)
    if roundup is not None:
        return round(s/len(lst), roundup)
    else:
        return s/len(lst)


def median(
    lst: __List[Number],
    roundup: __Union[int, None] = None,
) -> float:
    """Median - Middle value"""

    lst = sorted(lst)
    LENGTH = len(lst)
    if LENGTH % 2 != 0:
        return lst[__math.floor(LENGTH/2)]
    else:
        num1 = lst[__math.floor(LENGTH/2) - 1]
        num2 = lst[__math.floor(LENGTH/2)]
        med = (num1+num2)/2
        if roundup is not None:
            return round(med, roundup)
        else:
            return med


def mode(lst: __List[Number]) -> Number:
    """Mode:
    
    The Mode value is the value that appears the most number of times
    """
    frequency = __lists.list_freq(lst)
    
    max_val = max(frequency.values())
    keys = []
    
    for k, v in frequency.items():
        if v == max_val:
            keys.append(k)

    if len(keys) == len(lst):
        return "all"
    elif len(keys) > 1:
        return keys
    elif len(keys) == 1:
        return keys[0]
    else:
        return None


def var(
    lst: __List[Number],
    roundup: __Union[int, None] = None,
) -> float:
    """Variance"""

    MEAN = mean(lst)
    v = []
    for x in lst:
        v.append((x-MEAN)**2)
    out = sum(v)/len(v)
    if roundup is not None:
        return round(out, roundup)
    else:
        return out


def std(
    lst: __List[Number],
    roundup: __Union[int, None] = None,
) -> float:
    """Standard deviation"""

    sd = __math.sqrt(var(lst))
    if roundup is not None:
        return round(sd, roundup)
    else:
        return sd



def percentile(
    lst: __List[Number],
    percent: int = 50,
) -> Number:
    """Percentile"""

    idx = __math.floor(len(lst)/100*percent)
    if idx == len(lst):
        idx -= 1
    return sorted(lst)[idx]


def summary(
    lst: __List[Number],
    roundup: __Union[int, None] = None,
) -> __Dict[str,__Union[Number,__Dict[str,Number]]]:
    """Quick summary of data"""

    output = {
        "Count": len(lst),
        "Mean": mean(lst, roundup),
        "Median": median(lst, roundup),
        "Mode": mode(lst),
        "Standard deviation": std(lst, roundup),
        "Variance": var(lst, roundup),
        "Max": max(lst),
        "Min": min(lst),
        "Percentiles": {
            "1st Quartile": percentile(lst, 25),
            "2nd Quartile": percentile(lst, 50),
            "3rd Quartile": percentile(lst, 75),
        },
    }
    return output