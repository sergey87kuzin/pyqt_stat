import logging
import sqlite3
import sys
from datetime import datetime

from configure import DB_NAME
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (QComboBox, QDateEdit, QLabel, QMessageBox,
                             QPushButton)
from src.global_enums.literals import (ButtonTexts, InfoTexts, LabelTexts,
                                       Titles)
from src.helper import (clean_layout, create_sales_month_data, field_insert,
                        resource_path, send_to_queue)
from src.validators import float_validate, int_validate, month_year_validate


def add_income(layout):
    ''' внести данные по продажам '''
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            stocks = cursor.execute('SELECT stock FROM stocks').fetchall()
            if not stocks:
                QMessageBox.warning(
                    layout.parentWidget(), Titles.WARN_TITLE.value,
                    InfoTexts.WARN_STOCK_TEXT.value
                )
                return
    except Exception as e:
        logging.warning(str(e))
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value, str(e)
        )
        return

    clean_layout(layout)
    today = (datetime.now().year, datetime.now().month, datetime.now().day)
    stocks = [stock[0] for stock in stocks]
    layout.addRow(QLabel(LabelTexts.SALES.value))
    ent_date = QDateEdit(QDate(*today))
    ent_date.setCalendarPopup(True)
    layout.addRow(LabelTexts.DATE.value, ent_date)
    lst_stock = QComboBox()
    lst_stock.addItems(stocks)
    lst_stock.setCurrentText(stocks[0])
    layout.addRow(QLabel(LabelTexts.STOCK.value), lst_stock)
    ent_photo = field_insert(layout, 7, '0', LabelTexts.PHOTO.value)
    ent_video = field_insert(layout, 7, '0', LabelTexts.VIDEO.value)
    ent_income = field_insert(layout, 7, '0', LabelTexts.INCOME.value)
    btn_add = QPushButton(ButtonTexts.ADD.value)
    btn_add.clicked.connect(lambda: update_income(
        layout, ent_date.date().getDate()[1], ent_date.date().getDate()[0],
        ent_photo.text(), ent_video.text(), ent_income.text(),
        lst_stock.currentText()
    ))
    layout.addRow(btn_add)


def update_income(
    layout, month, year, photo, video, income, stock
):
    ''' Вносит доходы в БД '''
    if month_year_validate(month, year):
        return
    if (int_validate(photo) or int_validate(video)
       or float_validate(income)):
        return
    if not stock:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.WARN_NO_STOCK.value
        )
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            record = cursor.execute(
                '''SELECT stock FROM sales WHERE month=:month
                AND year=:year AND stock=:stock''',
                {
                    'month': month, 'year': year, 'stock': stock
                }
            ).fetchone()
            if not record:
                create_sales_month_data(month, year, stock)
            current_line = cursor.execute(
                ''' SELECT month, year, photo_sold, video_sold, amount_sold,
                stock FROM sales WHERE month=:month AND year=:year AND
                stock=:stock ''',
                {
                    'month': month, 'year': year, 'stock': stock
                }
            ).fetchone()
            cursor.execute(
                ''' UPDATE sales SET photo_sold=:photo, video_sold=:video,
                amount_sold=:income WHERE month=:month AND
                year=:year AND stock=:stock ''',
                {
                    'month': month, 'year': year,
                    'photo': int(photo) + int(current_line[2]),
                    'video': int(video) + int(current_line[3]),
                    'income': float(income) + float(current_line[4]),
                    'stock': stock
                })
            new_values = [(month, 'month'), (year, 'year')]
            cursor.executemany(
                'UPDATE dates SET value=? WHERE period=?', new_values
            )
            conn.commit()
    except Exception as e:
        send_to_queue({'error': e})
        logging.warning(str(e))
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return
    if 'pytest' not in sys.modules:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.SUCCESS_TEXT.value
        )
