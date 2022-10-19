import sqlite3
import calendar
import locale
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QMessageBox,
    QGridLayout  # QDateEdit
)
from src.helper import clean_layout, resource_path, date_insert
from src.global_enums.literals import (
    Titles, InfoTexts, ButtonTexts, LabelTexts
)
from configure import DB_NAME


def total(layout):
    ''' параметры для итоговой таблицы продаж '''
    clean_layout(layout)
    layout.addRow(QLabel(LabelTexts.TOTAL_TOP.value))
    ent_month, ent_year = date_insert(layout, 'total')
    btn_show = QPushButton(ButtonTexts.SHOW_STATS.value)
    btn_show.clicked.connect(lambda: show_total(
        layout, ent_month.text(), ent_year.text()
    ))
    layout.addRow(btn_show)


def show_total(layout, month, year):
    clean_layout(layout)
    stat_layout = QGridLayout()
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    stock_total = {}
    month_total = {}
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
                {
                    'year': year
                }
            ).fetchall()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.CHOOSE_GRAPH.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    for ind, stock in enumerate(stocks):
        stat_layout.addWidget(QLabel(stock), 0, ind + 1)
    for ind, sale in enumerate(year_sales):
        stat_layout.addWidget(
            QLabel(str(sale[2])), sale[0], stocks.index(sale[1]) + 1)
        if sale[1] in stock_total:
            stock_total[sale[1]] += float(sale[2])
        else:
            stock_total[sale[1]] = float(sale[2])
        if sale[0] in month_total:
            month_total[sale[0]] += float(sale[2])
        else:
            month_total[sale[0]] = float(sale[2])
    for ind, month in enumerate(months):
        stat_layout.addWidget(QLabel(month), ind, 0)
    for key, value in stock_total.items():
        stat_layout.addWidget(
            QLabel(str(value)), 13, stocks.index(key) + 1
        )
    for key, value in month_total.items():
        stat_layout.addWidget(
            QLabel(str(value)), key, len(stocks) + 1
        )
    layout.addChildLayout(stat_layout)
