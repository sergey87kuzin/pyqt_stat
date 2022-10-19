import os
import sys
import sqlite3
from datetime import date
import calendar
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QMessageBox  # QDateEdit
)
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts
)
from .validators import month_year_validate
from configure import DB_NAME


def start_sql():
    try:
        conn = sqlite3.connect(resource_path(DB_NAME))
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS stocks(stock text)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS loads(
            day integer, month integer, year integer, photo_load,
            video_load)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
            month integer, year integer,
            photo_sold, video_sold, amount_sold, stock text)''')
        conn.commit()
        conn.close()
    except Exception as e:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(str(e))
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()


def clean_layout(layout):
    ''' очистка рамки перед повторным использованием '''
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
        else:
            clean_layout(item.layout())
    # for i in reversed(range(layout.count())):
    #     item = layout.itemAt(i)
    #     if item:
    #         layout.removeWidget(item.widget())


def date_insert(layout, name):
    ''' добавление полей даты '''
    today = str(date.today())
    curr_year = today[2:4]
    curr_month = today[5:7]
    ent_month = QLineEdit()
    ent_month.setMaxLength(2)
    ent_month.setText(curr_month)
    layout.addRow(QLabel(LabelTexts.MONTH.value), ent_month)
    ent_year = QLineEdit()
    ent_year.setMaxLength(2)
    ent_year.setText(curr_year)
    layout.addRow(QLabel(LabelTexts.YEAR.value), ent_year)
    return ent_month, ent_year


def registrate_inputs(texts, entries, off, layout):
    ''' расположение полей на рамке '''
    for ind, text in enumerate(texts):
        layout.addWidget(text, ind+off, 0)
    for ind, entry in enumerate(entries):
        layout.addWidget(entry, ind+off, 0)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def create_sales_month_data(month, year, stock):
    ''' если месяц еще не рассматривался при продажах,
        создаем запись данного месяца '''
    if month_year_validate(1, year):
        return
    if not stock:
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            cursor.execute(''' INSERT INTO sales (month, year,
                           photo_sold, video_sold, amount_sold, stock)
                           VALUES (:month, :year, :photo_sold, :video_sold,
                           :amount_sold, :stock) ''',
                           {
                                'month': month, 'year': year, 'photo_sold': 0,
                                'video_sold': 0, 'amount_sold': 0,
                                'stock': stock
                            })
            conn.commit()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return


def create_month_data(month, year):
    ''' если месяц еще не рассматривался, создаем дни данного месяца '''
    dates = calendar.monthcalendar(year=int('20' + str(year)),
                                   month=int(month))
    days = [(date, month, year, 0, 0)
            for week in dates for date in week]
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            insert_line = ''' INSERT INTO loads (day, month, year,
                          photo_load, video_load) VALUES (?, ?, ?, ?, ?); '''
            cursor.executemany(insert_line, days)
            conn.commit()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    return days
