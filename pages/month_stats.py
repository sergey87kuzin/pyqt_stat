import sqlite3
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QMessageBox,
    QGridLayout, QFormLayout  # QDateEdit
)
from src.helper import (
    clean_layout, resource_path,
    date_insert, create_month_data
)
from src.validators import month_year_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts
)
from src.global_enums.colours import ElementColour
from configure import DB_NAME


def month_stats(layout):
    ''' позволяет указать, статистику загрузок какого месяца показать '''
    clean_layout(layout)
    layout.addRow(QLabel(LabelTexts.MONTH_STATS.value))
    ent_month, ent_year = date_insert(layout, 'month_stats')
    btn_show = QPushButton(ButtonTexts.SHOW.value)
    btn_show.clicked.connect(lambda: show_stats(
        layout, ent_month.text(), ent_year.text()
    ))
    layout.addRow(btn_show)


def show_stats(layout, month, year):
    ''' показывает статистику загрузок выбранного месяца '''
    if month_year_validate(month, year):
        return
    clean_layout(layout)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE month=:month AND year=:year ''',
                {'month': month, 'year': year}).fetchall()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return True
    if not results:
        results = create_month_data(month, year)
        if not results:
            return
    stat_layout = QGridLayout()
    for ind, result in enumerate(results):
        day_layout = QFormLayout()
        if result[0] != 0:
            day_layout.addWidget(QLabel(str(result[0])))
            day_layout.addRow(QLabel(str(result[3])), QLabel(str(result[4])))
        stat_layout.addLayout(day_layout, ind // 7, ind % 7)
    layout.addRow('', stat_layout)
