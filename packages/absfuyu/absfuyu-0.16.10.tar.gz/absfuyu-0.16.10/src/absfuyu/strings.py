#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
String Module
-------------
Some string method

Contain:
- strDiv
- strAna
- strDivVar
- strHex
- isPangram
- isPalindrome
"""


# Module level
##############################################################
__all__ = [
    "strDiv","strAna", "strDivVar", "strHex", "isPalindrome",
    "isPangram",
]



# Library
##############################################################
from typing import Dict as __Dict
from typing import List as __List
from typing import Union as __Union
from typing import Optional as __Optional

from . import generator as __gen





# Function
##############################################################


def strDiv(
        your_string: str,
        string_split_size: int = 60
    ) -> __List[str]:
    """
    Summary
    -------
    Divide long string into smaller size

    Parameters
    ----------
    your_string : str
        string that need to be divided
    
    string_split_size : int
        divide string every x character
        (default: x = 60)

    Returns
    -------
    list
        A list in which each item is a smaller
        string with the size of string_split_size
        (need to be concaternate later)
    """

    output = []
    while True:
        if len(your_string) == 0:
            break
        output.append(your_string[:string_split_size])
        your_string = your_string[string_split_size:]
    return output




def strAna(your_string: str) -> __Dict[str, int]:
    """
    Summary
    -------
    String analyze (count number of type of character)

    Parameters
    ----------
    your_string : str
        string that needs analyze

    Returns
    -------
    dict
        A dictionary contains number of digit character,
        uppercase character, lowercase character, and
        special character
    """

    detail = {
        "digit": 0,
        "uppercase": 0,
        "lowercase": 0,
        "other": 0
    }

    for x in your_string:
        if ord(x) in range(48,58): #num
            detail["digit"] += 1
        elif ord(x) in range(65,91): #cap
            detail["uppercase"] += 1
        elif ord(x) in range(97,123): #low
            detail["lowercase"] += 1
        else:
            detail["other"] += 1
    
    return detail
    


def strDivVar(
        string_or_list: __Union[str,__List[str]],
        split_size: int = 60,
        split_var_len: int = 12,
        custom_var_name: __Optional[str] = None,
    ) -> __List[str]:
    """
    Summary
    -------
    Divide long string into smaller size,
    then assign a random variable to splited
    string for later use

    Parameters
    ----------
    string_or_list : str | list
        string or list that need to be divided
        and assign variable
    
    split_size : int
        divide string every x character
        (default: x = 60)
    
    split_var_len : int
        length of variable name assigned to each item
        (default: 12)
    
    custom_var_name : str
        custom var name when join string

    Returns
    -------
    list
        A list in which each item is a smaller
        string with the size of split_size
        and a way to concaternate them (when using print)
    
    Example
    -------
    >>> ["qwerty","uiop"]

    ["asd='qwerty'","asx='uiop'","asw=asd+asx","asw"]
    """

    if isinstance(string_or_list, str):
        temp = strDiv(string_or_list,split_size)
    elif isinstance(string_or_list, list):
        temp = string_or_list
    else:
        temp = list(string_or_list)
    output = []
    
    # split variable
    splt_var_len = split_var_len
    splt_len = len(temp)

    if custom_var_name is None:
        splt_name = __gen.randStrGen(
            splt_var_len,
            splt_len+1,
            char="alphabet"
        )
        for i in range(splt_len):
            output.append(f"{splt_name[i]}='{temp[i]}'")
    else:
        for i in range(splt_len):
            output.append(f"{custom_var_name}{i+1}='{temp[i]}'")
    
    # joined variable
    temp = []
    if custom_var_name is None:
        for i in range(splt_len):
            if i == 0:
                temp.append(f"{splt_name[-1]}=")
            if (i == splt_len-1):
                temp.append(f"{splt_name[i]}")
            else:
                temp.append(f"{splt_name[i]}+")
    else:
        for i in range(splt_len):
            if i == 0:
                temp.append(f"{custom_var_name}=")
            if (i == splt_len-1):
                temp.append(f"{custom_var_name}{i+1}")
            else:
                temp.append(f"{custom_var_name}{i+1}+")
    
    output.append("".join(temp))
    if custom_var_name is None:
        output.append(splt_name[-1])
    else:
        output.append(custom_var_name)

    return output




def strHex(your_string: str, output_opt: str = "x") -> str:
    r"""
    Summary
    -------
    Convert string to hex form

    Parameters
    ----------
    your_string : str
        string that need to be convert
    
    output_opt : str
        "x": hex string in the form of \x (default)
        "normal: normal hex string

    Returns
    -------
    str
        Hexed string
    """

    output_option = {
        "normal":0,
        "x":1
    }
    # normal: normal hex string
    # x: hex string in the form of \x

    outopt = output_option[output_opt]
    
    byte_str = your_string.encode('utf-8')
    hex_str = byte_str.hex()
    
    if outopt == 0:
        return hex_str
    
    elif outopt == 1:
        temp = []
        str_len = len(hex_str)

        for i in range(str_len):
            if i % 2 == 0:
                temp.append(f"\\x")
            temp.append(hex_str[i])
        return ''.join(temp)



def isPangram(text: str) -> bool:
    """
    Summary
    -------
    Check if string is a pangram

        A pangram is a unique sentence in which
        every letter of the alphabet is used at least once

    Parameters
    ----------
    text : str
        string that need to be check

    Returns
    -------
    bool
        True if string is a pangram
    """

    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    return not set(alphabet) - set(text.lower())



def isPalindrome(text: str) -> bool:
    """
    Summary
    -------
    Check if string is a palindrome

        A palindrome is a word, verse, or sentence 
        or a number that reads the same backward or forward

    Parameters
    ----------
    text : str
        string that need to be check

    Returns
    -------
    bool
        True if string is a palindrome
    """

    # Use string slicing [start:end:step]
    return text == text[::-1]