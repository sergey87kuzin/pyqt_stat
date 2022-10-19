import calendar
from tkinter import messagebox
from src.global_enums.literals import Titles, InfoTexts


def month_year_validate(month, year):
    try:
        month = int(month)
        year = int(year)
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_TYPE.value
        )
        return True
    if (not month or not year or month < 1 or month > 12 or
            year < 1 or year > 99):
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True


def date_validate(day, month, year):
    days = calendar.TextCalendar(firstweekday=0).formatmonth(
        int('20' + year), int(month)
    )
    if int(day) <= 0:
        return True
    if day[0] == '0':
        day = day[-1]
    if day not in days:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True


def int_validate(value):
    try:
        if not value:
            raise TypeError
        value = int(value)
        if value < 0:
            raise TypeError
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True


def float_validate(value):
    try:
        if not value:
            raise TypeError
        value = float(value)
        if value < 0:
            raise TypeError
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True
