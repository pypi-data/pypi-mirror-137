"""
ABSFUYU-EXTRA: DATA ANALYSIS
-------------

"""




__EXTRA_MODE = False


# Library
##############################################################
try:
    import pandas as __pd
except:
    print("This feature is in absfuyu[extra] package")
else:
    __EXTRA_MODE = True

try:
    import numpy as __np
except:
    print("This feature is in absfuyu[extra] package")
else:
    __EXTRA_MODE = True

try:
    import matplotlib.pyplot as __plt
except:
    print("This feature is in absfuyu[extra] package")
else:
    __EXTRA_MODE = True



def isLoaded():
    global __EXTRA_MODE
    if __EXTRA_MODE:
        print("Loaded")