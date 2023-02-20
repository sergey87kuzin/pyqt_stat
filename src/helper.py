import calendar
import json
import os
import sqlite3
import sys
from datetime import datetime
import pika

from configure import DB_NAME
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QFormLayout)

from src.global_enums.literals import InfoTexts, Titles, ButtonTexts

from .validators import month_year_validate


def start_sql():
    try:
        conn = sqlite3.connect(resource_path(DB_NAME))
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS stocks(stock text)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS loads(
            day integer, month integer, year integer, photo_load integer,
            video_load integer)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
            month integer, year integer, photo_sold integer,
            video_sold integer, amount_sold float, stock text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS stylesheets(
            widget text, style text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS dates(
            period text, value integer)''')
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
    if type(layout) == QFormLayout:
        while layout.count():
            line = layout.takeRow(0)
            items = (line.labelItem, line.fieldItem)
            for item in items:
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                    else:
                        clean_layout(item.layout())
    else:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                clean_layout(item.layout())


def field_insert(layout, max_length, fill, name):
    ''' добавление полей '''
    ent_field = QLineEdit()
    ent_field.setMaxLength(max_length)
    ent_field.setText(fill)
    layout.addRow(QLabel(name), ent_field)
    return ent_field


def registrate_inputs(texts, entries, off, layout):
    ''' расположение полей на рамке '''
    for ind, text in enumerate(texts):
        layout.addWidget(text, ind + off, 0)
    for ind, entry in enumerate(entries):
        layout.addWidget(entry, ind + off, 0)


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
                :amount_sold, :stock) ''', {'month': month,
                                            'year': year,
                                            'photo_sold': 0,
                                            'video_sold': 0,
                                            'amount_sold': 0,
                                            'stock': stock})
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


def next_month(month, year):
    year += month // 12
    month = month % 12 + 1
    return month, year


def prev_month(month, year):
    if month == 1:
        return 12, year - 1
    return month - 1, year


def get_month():
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            date = cursor.execute(
                'SELECT period, value FROM dates'
            ).fetchall()
            for line in date:
                if line[0] == 'month':
                    month = line[1]
                else:
                    year = line[1]
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return datetime.now().month, datetime.now().year
    return month, year


def add_prev_next_buttons(layout, function, month, year, *args):
    button_layout = QGridLayout()
    btn_prev = QPushButton(ButtonTexts.PREV.value)
    btn_prev.clicked.connect(
        lambda: function(layout, *prev_month(month, year), *args)
    )
    btn_next = QPushButton(ButtonTexts.NEXT.value)
    btn_next.clicked.connect(
        lambda: function(layout, *next_month(month, year), *args)
    )
    button_layout.addWidget(btn_prev, 0, 0)
    button_layout.addWidget(btn_next, 0, 1)
    layout.addRow(button_layout)


def add_year_buttons(layout, function, year, *args):
    button_layout = QGridLayout()
    btn_prev = QPushButton(ButtonTexts.PREV_YEAR.value)
    btn_prev.clicked.connect(
        lambda: function(layout, year - 1, *args)
    )
    btn_next = QPushButton(ButtonTexts.NEXT_YEAR.value)
    btn_next.clicked.connect(
        lambda: function(layout, year + 1, *args)
    )
    button_layout.addWidget(btn_prev, 0, 0)
    button_layout.addWidget(btn_next, 0, 1)
    return button_layout


def send_to_queue(data):
    conn_params = pika.ConnectionParameters('localhost', 5672)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    exchange = 'message_exchange'
    routing_key = 'message_key'
    body = json.dumps(data)
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    channel.basic_publish(
        exchange=exchange, routing_key=routing_key, body=body,
        properties=pika.BasicProperties(
            delivery_mode=2  # сообщение помечается как устойчивое
        )
    )
    connection.close()
