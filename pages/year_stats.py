import sqlite3

from configure import DB_NAME
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QFormLayout, QFrame, QGridLayout, QLabel,
                             QMessageBox)
from src.global_enums.literals import Choices, InfoTexts, Titles
from src.helper import (add_year_buttons, clean_layout, create_month_data,
                        get_month, resource_path)


def year_stats(layout, photo, video):
    ''' позволяет указать, статистику загрузок какого года показать '''
    month, year = get_month()
    show_year_loads(layout, year, None, photo, video)


def show_year_loads(layout, year, window, photo_col, video_col):
    if window:
        window.accept()
    clean_layout(layout)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE year=:year ''',
                {'year': year}).fetchall()
            cursor.execute(
                'UPDATE dates SET value=:value WHERE period=:period',
                {'value': year, 'period': 'year'}
            )
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
    window.setStyleSheet('QLabel {font: bold 10px;}')
    stat_layout = QGridLayout()
    stat_layout.setVerticalSpacing(0)
    stat_layout.setHorizontalSpacing(10)
    stat_layout.addWidget(QLabel(str(year)), 0, 0)
    for i in range(1, 13):
        if i not in month_results:
            month_data = create_month_data(i, year)
            if not month_data:
                return
        else:
            month_data = month_results[i]
        month_layout = QGridLayout()
        month_layout.setVerticalSpacing(0)
        month_layout.setHorizontalSpacing(0)
        month_layout.addWidget(
            QLabel(Choices.MONTHS.value[i - 1]), 0, 0, 1, 4
        )
        for ind, day_data in enumerate(month_data):
            frame = QFrame()
            frame.setStyleSheet('border: dotted; border-width: 1px;')
            day_layout = QFormLayout(frame)
            day_layout.setVerticalSpacing(0)
            day_layout.setContentsMargins(0, 0, 0, 0)
            if day_data[0] != 0:
                date = QLabel(str(day_data[0]))
                date.setAlignment(Qt.AlignCenter)
                day_layout.addRow(date)
                photo, video = QLabel('-'), QLabel('-')
                for label in (date, photo, video):
                    label.setStyleSheet('border: none;')
                if day_data[3] != 0:
                    photo.setText('●')
                    photo.setStyleSheet(f'color: {photo_col}; border: none;')
                if day_data[4] != 0:
                    video.setText('●')
                    video.setStyleSheet(f'color: {video_col}; border: none;')
                for label in (photo, video):
                    label.setMaximumWidth(15)
                    label.setMinimumWidth(15)
                day_layout.addRow(photo, video)
                day_layout.setFormAlignment(
                    Qt.AlignHCenter | Qt.AlignTop
                )
            month_layout.addWidget(frame, ind // 7 + 1, ind % 7)
        stat_layout.addLayout(
            month_layout, (i - 1) // 4 + 1, (i - 1) % 4, 1, 1, Qt.AlignTop
        )
    photo = QLabel()
    photo.setText(f'<font color={photo_col}>● </font>'
                  + '<font color="black">- отметка фото</font>')
    video = QLabel()
    video.setText(f'<font color={video_col}>● </font>'
                  + '<font color="black">- отметка видео</font>')
    button_layout = add_year_buttons(
        layout, show_year_loads, year, window, photo_col, video_col
    )
    stat_layout.addWidget(photo, 5, 1)
    stat_layout.addWidget(video, 5, 2)
    stat_layout.addLayout(button_layout, 6, 1, 1, 2)
    window.setLayout(stat_layout)
    window.show()
