import calendar
import locale
import logging
import sqlite3

from configure import DB_NAME
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QLabel
from src.global_enums.literals import InfoTexts, Titles
from src.helper import add_year_buttons, clean_layout, get_month, resource_path


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
            cursor.execute(
                'UPDATE dates SET value=:value WHERE period=:period',
                {'value': year, 'period': 'year'}
            )
            conn.commit()
    except Exception as e:
        logging.warning(str(e))
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return

    layout.addRow(QLabel(str(year)))
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
    button_layout = add_year_buttons(layout, show_total, year)
    layout.addRow(button_layout)
