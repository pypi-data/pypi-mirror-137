#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Help Module
-----------

Contain help pages
"""


# Module level
##############################################################
__all__ = [
    "help",
]




# Library
##############################################################
from . import sort as s
from .version import __version__ as v






# Function
##############################################################

current_func = ["help","srcMe"]

def printAlphabet(lst: list):
    """
    Print item in list in alphabet order with line break
    """
    
    data = s.alphabetAppear(lst)
    incre = data[1]
    for i in range(len(lst)):
        if i in incre:
            print("")
        if i == len(lst)-1:
            print(lst[i], end = " ")
        else:
            print(lst[i], end = "; ")
    
    return None

def help(page: int = 1):
    """
    absfuyu builtin help page
    """
    
    if page == 1:
        print(f"""
            absfuyu version: {v}
            
            USAGE:
            import absfuyu
            absfuyu.help()
            help(absfuyu)
            """)
        
        print("\tUse code below to use all the functions: \n")
        module_list = [
            "calculation", "data", "fibonacci", "generator",
            "obfuscator", "sort", "strings", "util", "fun",
            "lists", "stats",
        ]
        for x in s.selection_sort(module_list):
            print(f"\tfrom absfuyu import {x}")
        
        print("""
            Or, you can go overboard with:
            from absfuyu import everything as ab
            
            page 1 of 2
            """)
    
    elif page == 2:
        print("List of function that can use in main module:")
        printAlphabet(current_func)
        print("\n")
        print("page 2 of 2")
        
    else:
        return None



################################
    # to documenting
    """
    Summary
    -------
    
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
################################