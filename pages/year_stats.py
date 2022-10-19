import sqlite3
from datetime import date
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QMessageBox,
    QGridLayout, QFormLayout, QDialog  # QDateEdit
)
from src.helper import (
    clean_layout, resource_path, create_month_data
)
from src.validators import month_year_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts
)
from src.global_enums.colours import ElementColour
from configure import DB_NAME


def year_stats(layout):
    ''' позволяет указать, статистику загрузок какого года показать '''
    clean_layout(layout)
    layout.addRow(QLabel(LabelTexts.YEAR_STATS.value))
    today = str(date.today())
    curr_year = today[2:4]
    ent_year = QLineEdit()
    ent_year.setMaxLength(3)
    ent_year.setText(curr_year)
    layout.addRow(QLabel(LabelTexts.YEAR.value), ent_year)
    btn_show = QPushButton(ButtonTexts.SHOW_STATS.value)
    btn_show.clicked.connect(lambda: show_year_loads(
        layout, ent_year.text()
    ))
    layout.addRow(btn_show)


def show_year_loads(layout, year):
    if month_year_validate(1, year):
        return
    clean_layout(layout)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE year=:year ''',
                {'year': year}).fetchall()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    month_results = {}
    for line in results:
        if int(line[1]) in month_results:
            month_results[int(line[1])].append(line)
        else:
            month_results[int(line[1])] = [line, ]
    window = QDialog(layout.parentWidget())
    stat_layout = QGridLayout()
    for i in range(1, 13):
        if i not in month_results:
            month_data = create_month_data(i, year)
            if not month_data:
                return
        else:
            month_data = month_results[i]
        month_layout = QGridLayout()
        month_layout.addWidget(QLabel(str(i)), 0, 0, 1, 4)
        for ind, day_data in enumerate(month_data):
            day_layout = QFormLayout()
            if day_data[0] != 0:
                day_layout.addRow(QLabel(str(day_data[0])))
                photo, video = '-', '-'
                if line[3] != 0:
                    photo = '+'
                if line[4] != 0:
                    video = '+'
                day_layout.addRow(QLabel(f'{photo}  {video}'))
            month_layout.addLayout(day_layout, ind // 7 + 1, ind % 7)
        stat_layout.addLayout(month_layout, (i - 1) // 4, (i - 1) % 4)
    window.setLayout(stat_layout)
    window.exec()
