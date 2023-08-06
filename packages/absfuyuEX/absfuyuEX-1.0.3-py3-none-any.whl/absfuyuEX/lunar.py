import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist

from absfuyu.fun import _force_shutdown as sd

def solar2lunar(year: int, month: int, day: int):
    solar = Solar(year, month, day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar

def lunar2solar(year: int, month: int, day: int, isleap: bool = False):
    lunar = Lunar(year, month, day, isleap)
    solar = Converter.Lunar2Solar(lunar)
    return solar


def happy_new_year(forced: bool = False):
    """
    Only occurs on 01/01 every year
    (including lunar new year)
    """

    if forced:
        return sd()
    
    y = datetime.date.today().year
    m = datetime.date.today().month
    d = datetime.date.today().day
    solar_new_year = m==1 and d==1

    lunar = solar2lunar(y,m,d)
    lunar_new_year = lunar.month==1 and lunar.day==1

    if solar_new_year or lunar_new_year:
        print("Happy New Year! You should take rest now.")
        return sd()
    else:
        print("The time has not come yet")
        return None