# -*- coding: utf-8 -*-
"""
ABSFUYU WIP FEATURES
--------------------
WARNING: UNSTABLE
"""



import re
import os
from functools import lru_cache
from typing import Dict, List


here = os.path.abspath(os.path.dirname(__file__))



# PASSWORD CHECKER
def password_check(password: str) -> bool:
    """
    Verify the strength of 'password'.
    Returns a dict indicating the wrong criteria.
    A password is considered strong if:
    - 8 characters length or more
    - 1 digit or more
    - 1 symbol or more
    - 1 uppercase letter or more
    - 1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbols = re.compile(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]')
    symbol_error = symbols.search(password) is None

    detail = {
        'password_ok': not any([ # overall result
            length_error, digit_error,
            uppercase_error, lowercase_error,
            symbol_error
        ]),
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }

    return detail['password_ok']



# FIBONACCI WITH CACHE
@lru_cache(maxsize=5)
def fib(n: int) -> int:
    """Fibonacci (recursive)"""
    # max recursion is 484
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)




# PRIME NUMBERS (SMALLER THAN 100000 - 9592 NUMBERS)
from absfuyu.dev import load_data as ld
PRIME_NUMBER = ld.toList(ld.LoadData("prime"))





if __name__ == "__main__":
    pass