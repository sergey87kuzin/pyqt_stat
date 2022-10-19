import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QMessageBox, QComboBox
)
from src.helper import clean_layout, resource_path, date_insert
from src.global_enums.literals import (
    Choices, Titles, InfoTexts, LabelTexts, ButtonTexts
)
from configure import DB_NAME
matplotlib.use('TkAgg')


def graphic(layout):
    ''' задать параметры графика '''
    clean_layout(layout)
    layout.addRow(QLabel(LabelTexts.GRAPHIC_TOP.value))
    ent_month, ent_year = date_insert(layout, 'graphic')
    lst_type = QComboBox(Choices.GRAPHICS.value)
    layout.addRow(QLabel(LabelTexts.GRAPHIC_TYPE.value), lst_type)
    btn_plot = QPushButton(ButtonTexts.PLOT.value)
    btn_plot.clicked.connect(lambda: create_graphic(
        ent_month.text(), ent_year.text(), lst_type.currentText()
    ))
    layout.addRow(btn_plot)


def create_graphic(month, year, graphic_type):
    ''' Построение графиков '''
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            if graphic_type == Choices.GRAPHICS.value[0]:
                data = cursor.execute(
                    ''' SELECT month, sum(photo_sold), sum(video_sold),
                    sum(amount_sold) FROM sales WHERE year=:year
                    GROUP BY month ''',
                    {'year': year}
                ).fetchall()
                if not data:
                    error = QMessageBox()
                    error.setWindowTitle(Titles.WARN_TITLE.value)
                    error.setText(InfoTexts.NO_YEAR_DATA.value)
                    error.setIcon(QMessageBox.Warning)
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()
                    return
                print_graphic(data)
            elif graphic_type == Choices.GRAPHICS.value[1]:
                data = cursor.execute(
                    ''' SELECT stock, sum(photo_sold), sum(video_sold),
                    sum(amount_sold) FROM sales WHERE month=:month
                    AND year=:year GROUP BY stock ''',
                    {'month': month, 'year': year}
                ).fetchall()
                if not data:
                    error = QMessageBox()
                    error.setWindowTitle(Titles.WARN_TITLE.value)
                    error.setText(InfoTexts.NO_MONTH_DATA.value)
                    error.setIcon(QMessageBox.Warning)
                    error.setStandardButtons(QMessageBox.Ok)
                    error.exec_()
                    return
                print_graphic(data)
            else:
                error = QMessageBox()
                error.setWindowTitle(Titles.WARN_TITLE.value)
                error.setText(InfoTexts.CHOOSE_GRAPH.value)
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return


def print_graphic(data):
    ''' формирует столбчатые диаграмы на основе данных из БД '''
    label_list = [line[0] for line in data]
    photo_list = [line[1] for line in data]
    video_list = [line[2] for line in data]
    income_list = [line[3] for line in data]
    plt.figure(Titles.GRAPHIC_TITLE.value)
    plt.subplots_adjust(wspace=0.3, hspace=0.5)
    plt.subplot(311)
    plt.bar(label_list, photo_list)
    annotate_bars(label_list, photo_list)
    plt.ylabel(LabelTexts.PHOTO.value)
    plt.subplot(312)
    plt.bar(label_list, video_list)
    annotate_bars(label_list, video_list)
    plt.ylabel(LabelTexts.VIDEO.value)
    plt.subplot(313)
    plt.bar(label_list, income_list)
    annotate_bars(label_list, income_list)
    plt.ylabel(LabelTexts.INCOME.value)
    plt.show()


def annotate_bars(label_list, data_list):
    ''' подписывает столбцы диаграм '''
    plt.xticks(ticks=label_list, labels=label_list, rotation=45)
    for i in range(len(data_list)):
        plt.annotate(
            str(data_list[i]), xy=(label_list[i], data_list[i]),
            ha='center', va='bottom'
        )
