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
    ''' в отдельном окне рисует календарь на год с указанием загрузок '''
    if window:
        # window.accept()
        clean_layout(window.layout())
        stat_layout = window.layout()
    else:
        window = QDialog(layout.parentWidget())
        stat_layout = QGridLayout()
        window.setLayout(stat_layout)
    clean_layout(layout)
    # данные по году из БД
    month_results = get_year_loads_data(layout, year)
    # отдельное окно и его layuot
    window.setStyleSheet('QLabel {font: bold 10px;}')
    stat_layout.setVerticalSpacing(0)
    stat_layout.setHorizontalSpacing(10)
    stat_layout.addWidget(QLabel(str(year)), 0, 0)
    # слои отдельных месяцев
    for i in range(1, 13):
        # если в БД нет данных по данному месяцу, создаем даты без загрузок
        if i not in month_results:
            month_data = create_month_data(i, year)
            if not month_data:
                return
        else:
            month_data = month_results[i]
        month_layout = QGridLayout()
        month_layout.setSpacing(0)
        month_layout.addWidget(
            QLabel(Choices.MONTHS.value[i - 1]), 0, 0, 1, 4
        )
        # сетка календаря отдельного месяца
        create_month_loads_calendar(
            month_data, month_layout, photo_col, video_col
        )
        stat_layout.addLayout(
            month_layout, (i - 1) // 4 + 1, (i - 1) % 4, 1, 1, Qt.AlignTop
        )
    # подвал
    photo = QLabel()
    photo.setText(f'<font color={photo_col}>● </font>'
                  + '<font color="black">- отметка фото</font>')
    video = QLabel()
    video.setText(f'<font color={video_col}>● </font>'
                  + '<font color="black">- отметка видео</font>')
    # кнопки смены года
    button_layout = add_year_buttons(
        layout, show_year_loads, year, window, photo_col, video_col
    )
    stat_layout.addWidget(photo, 5, 1)
    stat_layout.addWidget(video, 5, 2)
    stat_layout.addLayout(button_layout, 6, 1, 1, 2)
    window.show()


def get_year_loads_data(layout, year):
    ''' получаем данные по загрузкам указанного
     года и сохраняем в БД год как активный '''
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
            conn.commit()
    except Exception:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return
    month_results = {}
    for line in results:
        if int(line[1]) in month_results:
            month_results[int(line[1])].append(line)
        else:
            month_results[int(line[1])] = [line, ]
    return month_results


def create_month_loads_calendar(data, month_layout, photo_col, video_col):
    ''' календарь отдельного месяца '''
    for ind, day_data in enumerate(data):
        frame = QFrame()
        frame.setStyleSheet(
            ''' border: dotted; border-width: 1px; padding: 0px;
            margin: 0px;''')
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
