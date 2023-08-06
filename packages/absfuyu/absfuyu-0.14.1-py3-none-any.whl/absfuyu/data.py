#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Module
-----------
Some common data

Contain:
- Quick use data
"""


# Module level
##############################################################
__all__ = [
    "Number", "Word", 
]



# Library
##############################################################
from typing import Optional






# Data
##############################################################
class Word():
    """Alphabet stuff"""

    # 01
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    # 02
    ALPHABET_LIST = list(ALPHABET)


class Number():
    """Some common numbers"""
    
    # 01
    @staticmethod
    def PerfectNumber(order: Optional[int] = None) -> int:
        """
        Summary
        -------
        Perfect number: a positive integer that is
        equal to the sum of its proper divisors.
        The smallest perfect number is 6, which is
        the sum of 1, 2, and 3.
        Other perfect numbers are 28, 496, and 8,128.

        Parameters
        ----------
        order : int
            k-th position of perfect number

        Returns
        -------
        int
            Perfect number at k-th position
        """

        # List of known perfect number
        # Source: https://en.wikipedia.org/wiki/List_of_Mersenne_primes_and_perfect_numbers
        perfect_number_index = [
            2, 3, 5, 7,
            13, 17, 19, 31, 61, 89,
            107, 127, 521, 607,
            1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941,
            11_213, 19_937, 21_701, 23_209, 44_497, 86_243,
            110_503, 132_049, 216_091, 756_839, 859_433,
            1_257_787, 1_398_269, 2_976_221, 3_021_377, 6_972_593,
            13_466_917, 20_996_011, 24_036_583, 25_964_951,
            30_402_457, 32_582_657, 37_156_667, 42_643_801,
            43_112_609, 57_885_161,
            ## 74_207_281, 77_232_917, 82_589_933
        ]
        if order is None:
            return None
        elif order < 1 or order > len(perfect_number_index):
            return None
        else:
            idx = perfect_number_index[order-1]
            perfect_number = (2**(idx-1))*((2**idx)-1)
            return perfect_number
    
    # 02
    @staticmethod
    def PrimeNumber(order: Optional[int] = None) -> int:
        r"""
        Summary
        -------
        Generate prime number at k-th position

        Parameters
        ----------
        order : int
            k-th position of prime number

        Returns
        -------
        int
            Prime number at k-th position
        
        Notes
        -----
        Still missing some number
        """

        if order is None or order < 1:
            return None
        
        prime_number = [
            2, 3, 5, 7, 11, 13, 17, 19,
            23, 29, 31, 37, 41,
        ]
        #order -= 1
        
        if order <= len(prime_number):
            return prime_number[order-1]
        else:
            order -= len(prime_number)
            prime = order**2 + order + 41
            return prime