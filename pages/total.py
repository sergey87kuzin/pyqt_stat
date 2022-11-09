import calendar
import locale
import sqlite3

from configure import DB_NAME
from PyQt5.QtWidgets import (QGridLayout, QMessageBox, QPushButton,
                             QTableWidget, QTableWidgetItem)
from src.global_enums.literals import ButtonTexts, InfoTexts, Titles
from src.helper import clean_layout, resource_path, get_month


def total(layout):
    ''' вызов итоговой таблицы с учетом активного года '''
    month, year = get_month()
    show_total(layout, year)


def show_total(layout, year):
    ''' заполнение итоговой таблицы продаж '''
    clean_layout(layout)
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    stock_total = {}
    month_total = {}

    # получаю данные по продажам за год
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            ''' общая таблица за весь год '''
            months = list(calendar.month_abbr)
            stocks = cursor.execute(
                'SELECT stock FROM stocks'
            ).fetchall()
            stocks = [stock[0] for stock in stocks]
            year_sales = cursor.execute(
                'SELECT month, stock, amount_sold FROM sales WHERE year=:year',
                {'year': year}
            ).fetchall()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.CHOOSE_GRAPH.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return

    # заполняю таблицу данными по продажам стоков по месяцам и суммарно
    table = QTableWidget()
    table.setColumnCount(len(stocks) + 1)
    table.setRowCount(len(months) + 1)
    table.setHorizontalHeaderLabels([*stocks, 'total'])
    table.setVerticalHeaderLabels([*months, 'total'])
    for ind, sale in enumerate(year_sales):
        table.setItem(
            sale[0], stocks.index(sale[1]),
            QTableWidgetItem(str(sale[2]))
        )
        if sale[1] in stock_total:
            stock_total[sale[1]] += float(sale[2])
        else:
            stock_total[sale[1]] = float(sale[2])
        if sale[0] in month_total:
            month_total[sale[0]] += float(sale[2])
        else:
            month_total[sale[0]] = float(sale[2])
    for key, value in stock_total.items():
        table.setItem(
            13, stocks.index(key), QTableWidgetItem(str(value))
        )
    for key, value in month_total.items():
        table.setItem(
            key, len(stocks), QTableWidgetItem(str(value))
        )
    layout.addRow(table)

    # добавляю кнопки для перехода к другому году
    btn_prev = QPushButton(ButtonTexts.PREV_YEAR.value)
    btn_prev.clicked.connect(
        lambda: show_total(layout, year - 1)
    )
    btn_next = QPushButton(ButtonTexts.NEXT_YEAR.value)
    btn_next.clicked.connect(
        lambda: show_total(layout, year + 1)
    )
    button_layout = QGridLayout()
    button_layout.addWidget(btn_prev, 0, 0)
    button_layout.addWidget(btn_next, 0, 1)
    layout.addRow(button_layout)
