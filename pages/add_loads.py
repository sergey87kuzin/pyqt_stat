import sqlite3
import sys
from datetime import date
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QMessageBox  # QDateEdit
)
from src.helper import (
    clean_layout, date_insert, registrate_inputs, resource_path,
    create_month_data
)
from src.validators import month_year_validate, date_validate, int_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts  # ButtonNames, LabelNames
)
from configure import DB_NAME


def add_loads(layout):
    ''' вносим данные по загрузкам '''
    clean_layout(layout)
    lbl_loads = QLabel(LabelTexts.LOADS.value)
    layout.addRow(lbl_loads)
    today = str(date.today())
    curr_date = today[8:10]
    ent_date = QLineEdit()
    ent_date.setMaxLength(2)
    ent_date.setText(curr_date)
    layout.addRow(QLabel(LabelTexts.DATE.value), ent_date)
    ent_month, ent_year = date_insert(layout, 'add_loads')
    ent_photo = QLineEdit()
    ent_photo.setMaxLength(3)
    ent_photo.setText('0')
    layout.addRow(QLabel(LabelTexts.PHOTO.value), ent_photo)
    ent_video = QLineEdit()
    ent_video.setMaxLength(3)
    ent_video.setText('0')
    layout.addRow(QLabel(LabelTexts.VIDEO.value), ent_video)
    btn_add = QPushButton(ButtonTexts.SAVE.value)
    btn_add.clicked.connect(lambda: save_loads(
        ent_date.text(), ent_month.text(), ent_year.text(), ent_photo.text(),
        ent_video.text()
    ))
    layout.addRow(btn_add)


def save_loads(day, month, year, photo, video):
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
            cursor.execute('''UPDATE loads SET
                            photo_load = :photo,
                            video_load = :video
                            WHERE day = :day AND
                                  month = :month AND
                                  year = :year''', {
                                'photo': int(photo) + int(day_line[3]),
                                'video': int(video) + int(day_line[4]),
                                'day': day,
                                'month': month,
                                'year': year
                            })
            conn.commit()
    except Exception as e:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(str(e))
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    if 'pytest' not in sys.modules:
        error = QMessageBox()
        error.setWindowTitle(Titles.SUCCESS_TITLE.value)
        error.setText(InfoTexts.SUCCESS_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
