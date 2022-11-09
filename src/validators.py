import calendar
from PyQt5.QtWidgets import QMessageBox
from src.global_enums.literals import Titles, InfoTexts


def month_year_validate(month, year):
    try:
        month = int(month)
        year = int(year)
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.WRONG_TYPE.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return True
    if (not month or not year or month < 1 or month > 12
            or year < 2001 or year > 2099):
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.WRONG_INPUT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return True


def date_validate(day, month, year):
    days = calendar.TextCalendar(firstweekday=0).formatmonth(year, month)
    if int(day) <= 0:
        return True
    if str(day) not in days:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.WRONG_INPUT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return True


def int_validate(value):
    try:
        if not value:
            raise TypeError
        value = int(value)
        if value < 0:
            raise TypeError
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.WRONG_INPUT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return True


def float_validate(value):
    try:
        if not value:
            raise TypeError
        value = float(value)
        if value < 0:
            raise TypeError
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.WRONG_INPUT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return True
