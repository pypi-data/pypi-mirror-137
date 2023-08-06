"""
ABSFUYU-EXTRA
-------------
Extra feature that require additional libraries
"""

__EXTRA_MODE = False


# Module level
##############################################################
__all__ = [
    "happy_new_year",
]


# Library
##############################################################
import datetime as __datetime

try:
    from lunarcalendar import Converter as __Converter, Solar as __Solar, Lunar as __Lunar
except:
    print("This feature is in absfuyu[extra] package")
else:
    __EXTRA_MODE = True

from ..fun import force_shutdown as __sd
# from . import data_analysis



# Function
##############################################################
def __solar2lunar(year: int, month: int, day: int):
    global __EXTRA_MODE
    if __EXTRA_MODE:
        solar = __Solar(year, month, day)
        lunar = __Converter.Solar2Lunar(solar)
        return lunar

def __lunar2solar(
        year: int,
        month: int,
        day: int,
        isleap: bool = False
    ):
    global __EXTRA_MODE
    if __EXTRA_MODE:
        lunar = __Lunar(year, month, day, isleap)
        solar = __Converter.Lunar2Solar(lunar)
        return solar



def happy_new_year(forced: bool = False):
    """
    Only occurs on 01/01 every year
    (including lunar new year)
    """
    global __EXTRA_MODE
    if __EXTRA_MODE:
        if forced:
            return __sd()
        
        y = __datetime.date.today().year
        m = __datetime.date.today().month
        d = __datetime.date.today().day
        solar_new_year = m==1 and d==1

        lunar = __solar2lunar(y,m,d)
        lunar_new_year = lunar.month==1 and lunar.day==1

        if solar_new_year or lunar_new_year:
            print("Happy New Year! You should take rest now.")
            return __sd()
        else:
            print("The time has not come yet")
            return None