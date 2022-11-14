import sqlite3

from configure import DB_NAME
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFormLayout, QFrame, QGridLayout, QLabel,
                             QMessageBox)
from src.global_enums.literals import Choices, InfoTexts, Titles
from src.helper import (add_prev_next_buttons, clean_layout, create_month_data,
                        get_month, resource_path)


def month_stats(layout, photo_col, video_col):
    ''' вызывает статистику загрузок активного месяца '''
    month, year = get_month()
    show_stats(layout, month, year, photo_col, video_col)


def show_stats(layout, month, year, photo_col, video_col):
    ''' отображает статистику загрузок посуточно в течение месяца '''
    clean_layout(layout)

    # выбираю из БД данные по отложенным загрузкам месяца
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE month=:month AND year=:year ''',
                {'month': month, 'year': year}).fetchall()
            new_values = [(month, 'month'), (year, 'year')]
            cursor.executemany(
                'UPDATE dates SET value=? WHERE period=?', new_values
            )
            conn.commit()
    except Exception:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return True
    if not results:
        results = create_month_data(month, year)
        if not results:
            return

    # располагаю данные о загрузках в сетке календаря
    label = QLabel(text=Choices.MONTHS.value[month - 1] + str(year))
    label.setAlignment(Qt.AlignCenter)
    layout.addRow(label)
    stat_layout = QGridLayout()
    stat_layout.setVerticalSpacing(0)
    stat_layout.setContentsMargins(0, 0, 0, 0)
    for ind, result in enumerate(results):
        frame = QFrame()
        frame.setStyleSheet('border: dotted; border-width: 1px;')
        day_layout = QFormLayout(frame)
        day_layout.setVerticalSpacing(0)
        day_layout.setContentsMargins(0, 0, 0, 0)
        if result[0] != 0:
            date = QLabel(str(result[0]))
            date.setAlignment(Qt.AlignCenter)
            date.setStyleSheet('border: none;')
            day_layout.addRow(date)
            photo = QLabel(str(result[3]))
            video = QLabel(str(result[4]))
            for label in (photo, video):
                label.setMaximumWidth(20)
                label.setMinimumWidth(20)
                label.setStyleSheet('border: none;')
            if result[3] != 0:
                photo.setStyleSheet(f'color: {photo_col}; border: none;')
            if result[4] != 0:
                video.setStyleSheet(f'color: {video_col}; border: none;')
            day_layout.addRow(photo, video)
        stat_layout.addWidget(frame, ind // 7, ind % 7)
    layout.addRow('', stat_layout)

    # добавляю кнопки для выбора другого месяца
    add_prev_next_buttons(
        layout, show_stats, month, year, photo_col, video_col
    )
