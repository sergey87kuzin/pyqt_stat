import calendar
import sqlite3

from configure import DB_NAME
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMessageBox
from pyqtgraph import BarGraphItem, GraphicsLayoutWidget
from src.global_enums.literals import InfoTexts, Titles
from src.helper import (add_prev_next_buttons, add_year_buttons, clean_layout,
                        get_month, resource_path)


def year_chart(layout):
    month, year = get_month()
    year_graph(layout, year)


def year_graph(layout, year):
    layout.parentWidget().setGeometry(QRect(0, 0, 400, 600))
    clean_layout(layout)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            data = cursor.execute(
                ''' SELECT month, sum(photo_sold), sum(video_sold),
                sum(amount_sold) FROM sales WHERE year=:year
                GROUP BY month ''',
                {'year': year}
            ).fetchall()
            if not data:
                QMessageBox.warning(
                    layout.parentWidget(), Titles.WARN_TITLE.value,
                    InfoTexts.NO_YEAR_DATA.value
                )
                return
    except Exception:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return
    graphics = (('photo', 1), ('video', 2), ('income', 3))
    for graphic in graphics:
        graph_widget = single_chart(data, *graphic)
        layout.addRow('', graph_widget)
    button_layout = add_year_buttons(layout, year_graph, year)
    layout.addRow(button_layout)


def stock_chart(layout):
    month, year = get_month()
    stock_graph(layout, month, year)


def stock_graph(layout, month, year):
    layout.parentWidget().setGeometry(QRect(0, 0, 400, 600))
    clean_layout(layout)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            data = cursor.execute(
                ''' SELECT stock, sum(photo_sold), sum(video_sold),
                sum(amount_sold) FROM sales WHERE month=:month
                AND year=:year GROUP BY stock ''',
                {'month': month, 'year': year}
            ).fetchall()
            if not data:
                QMessageBox.warning(
                    layout.parentWidget(), Titles.WARN_TITLE.value,
                    InfoTexts.NO_MONTH_DATA.value
                )
                return
    except Exception:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return
    graphics = (('photo', 1), ('video', 2), ('income', 3))
    for graphic in graphics:
        graph_widget = single_chart(data, *graphic)
        layout.addRow('', graph_widget)
    add_prev_next_buttons(layout, stock_graph, month, year)


def single_chart(data, title, index):
    graph_widget = GraphicsLayoutWidget()
    graph_1 = graph_widget.addPlot(title=title)
    try:
        x_labels = [list(calendar.month_abbr)[line[0]] for line in data]
    except Exception:
        x_labels = [line[0] for line in data]
    height = [line[index] for line in data]
    x_vals = list(range(1, len(x_labels) + 1))
    ticks = []
    for i, item in enumerate(x_labels):
        ticks.append((x_vals[i], item))
    ticks = [ticks]

    bargraph = BarGraphItem(x=x_vals, height=height, width=0.5)
    graph_1.addItem(bargraph)
    ax = graph_1.getAxis('bottom')
    ax.setTicks(ticks)
    return graph_widget
