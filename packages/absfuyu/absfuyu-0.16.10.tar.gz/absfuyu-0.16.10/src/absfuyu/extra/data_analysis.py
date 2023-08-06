"""
ABSFUYU-EXTRA: DATA ANALYSIS
-------------

"""




__EXTRA_MODE = False


# Library
##############################################################
try:
    import pandas as __pd
    import numpy as __np
    import matplotlib.pyplot as __plt
except:
    print("This feature is in absfuyu[extra] package")
else:
    __EXTRA_MODE = True



def isLoaded():
    if __EXTRA_MODE:
        print("Loaded")