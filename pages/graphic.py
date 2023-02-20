import calendar
import logging
import sqlite3

from configure import DB_NAME
# from pyqtgraph.graphcsItems.GraphicsObject import GraphicsObject
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (QComboBox, QMessageBox, QStackedWidget,
                             QTableWidget, QTableWidgetItem)
from pyqtgraph import BarGraphItem, GraphicsLayoutWidget, mkBrush, mkPen
from src.global_enums.literals import InfoTexts, Titles
from src.helper import (add_prev_next_buttons, add_year_buttons, clean_layout,
                        get_month, resource_path)


def year_chart(layout):
    month, year = get_month()
    year_graph(layout, year)


def year_graph(layout, year):
    sql_str = ''' SELECT month, sum(photo_sold), sum(video_sold),
                sum(amount_sold) FROM sales WHERE year=:year
                GROUP BY month '''
    create_graph(
        layout, sql_str, {'year': year}, InfoTexts.NO_YEAR_DATA.value
    )
    button_layout = add_year_buttons(layout, year_graph, year)
    layout.addRow(button_layout)


def stock_chart(layout):
    month, year = get_month()
    stock_graph(layout, month, year)


def stock_graph(layout, month, year):
    sql_str = ''' SELECT stock, sum(photo_sold), sum(video_sold),
                sum(amount_sold) FROM sales WHERE month=:month
                AND year=:year GROUP BY stock '''
    create_graph(
        layout, sql_str, {'month': month, 'year': year},
        InfoTexts.NO_MONTH_DATA.value
    )
    add_prev_next_buttons(layout, stock_graph, month, year)


def single_chart(data, graph_widget, title, index):
    graph_page = GraphicsLayoutWidget()
    graph_page.setBackground('w')
    graph_1 = graph_page.addPlot(title=title)
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

    pen = mkPen(color='#499F68')
    brush = mkBrush(color='#77B28C')
    bargraph = BarGraphItem(
        x=x_vals, height=height, width=0.5, pen=pen, brush=brush
    )
    graph_1.addItem(bargraph)
    ax = graph_1.getAxis('bottom')
    ax.setTicks(ticks)
    graph_widget.addWidget(graph_page)


def add_combo_box(graph_widget, names):
    combo_box = QComboBox()
    for name in names:
        combo_box.addItem(name[0])
    combo_box.activated[int].connect(graph_widget.setCurrentIndex)
    return combo_box


def create_graph(layout, sql_str, params, error_text):
    clean_layout(layout)
    layout.parentWidget().setGeometry(QRect(0, 0, 400, 600))
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            data = cursor.execute(sql_str, params).fetchall()
            if not data:
                QMessageBox.warning(
                    layout.parentWidget(), Titles.WARN_TITLE.value,
                    error_text
                )
                return
    except Exception as e:
        logging.warning(str(e))
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return
    graphics = (('photo', 1), ('video', 2), ('income', 3))
    data_table = QTableWidget(len(data), 3)
    input_data_to_table(data_table, data, graphics)
    graph_widget = QStackedWidget()
    data_table.setMaximumWidth(250)
    graph_widget.setMinimumWidth(200)
    for graphic in graphics:
        single_chart(data, graph_widget, *graphic)
        layout.addRow(data_table, graph_widget)
    combo_box = add_combo_box(graph_widget, graphics)
    layout.addRow('', combo_box)


def input_data_to_table(data_table, data, columns):
    headers = [column[0] for column in columns]
    data_table.setHorizontalHeaderLabels(headers)
    months = list(calendar.month_name)
    try:
        vertical_headers = [months[item[0]] for item in data]
    except Exception:
        vertical_headers = [item[0] for item in data]
    data_table.setVerticalHeaderLabels(vertical_headers)
    for index, line in enumerate(data):
        for unit in columns:
            data_table.setItem(
                index, unit[1] - 1,
                QTableWidgetItem(str(line[unit[1]]))
            )
