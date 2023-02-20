import logging
import sqlite3
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QMessageBox, QDateEdit
)
from PyQt5.QtCore import QDate
from src.helper import (
    clean_layout, resource_path, create_month_data, field_insert
)
from src.validators import month_year_validate, date_validate, int_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts  # ButtonNames, LabelNames
)
from configure import DB_NAME


def add_loads(layout):
    ''' вносим данные по загрузкам '''
    today = (datetime.now().year, datetime.now().month, datetime.now().day)
    clean_layout(layout)
    lbl_loads = QLabel(LabelTexts.LOADS.value)
    layout.addRow(lbl_loads)
    ent_date = QDateEdit(QDate(*today))
    ent_date.setCalendarPopup(True)
    layout.addRow(LabelTexts.DATE.value, ent_date)
    ent_photo = field_insert(layout, 7, '0', LabelTexts.PHOTO.value)
    ent_video = field_insert(layout, 7, '0', LabelTexts.VIDEO.value)
    btn_add = QPushButton(ButtonTexts.SAVE.value)
    btn_add.clicked.connect(lambda: save_loads(
        layout, ent_date.date().getDate()[2], ent_date.date().getDate()[1],
        ent_date.date().getDate()[0], ent_photo.text(), ent_video.text()
    ))
    layout.addRow(btn_add)


def save_loads(layout, day, month, year, photo, video):
    ''' сохранение внесенных данных о загрузках '''
    if month_year_validate(month, year):
        return
    if date_validate(day, month, year):
        return
    if int_validate(photo) or int_validate(video):
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            day_line = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                FROM loads WHERE day=:date AND month=:month
                AND year=:year ''',
                {'date': day, 'month': month, 'year': year}
            ).fetchone()
            if not day_line:
                days = create_month_data(month, year)
                if not days:
                    return
                day_line = (day, month, year, 0, 0)
            cursor.execute('''UPDATE loads SET photo_load = :photo,
                video_load = :video WHERE day = :day AND month = :month
                AND year = :year''', {'photo': int(photo) + int(day_line[3]),
                                      'video': int(video) + int(day_line[4]),
                                      'day': day,
                                      'month': month,
                                      'year': year})
            new_values = [(month, 'month'), (year, 'year')]
            cursor.executemany(
                'UPDATE dates SET value=? WHERE period=?', new_values
            )
            conn.commit()
    except Exception as e:
        logging.warning(str(e))
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value, str(e)
        )
        return
    if 'pytest' not in sys.modules:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.SUCCESS_TEXT.value
        )
