import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist



def solar2lunar(year: int, month: int, day: int):
    solar = Solar(year, month, day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar

def lunar2solar(year: int, month: int, day: int, isleap: bool = False):
    lunar = Lunar(year, month, day, isleap)
    solar = Converter.Lunar2Solar(lunar)
    return solar

