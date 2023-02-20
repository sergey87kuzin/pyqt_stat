import logging
import sqlite3
import sys

from configure import DB_NAME
from PyQt5.QtWidgets import QLabel, QMessageBox, QPushButton
from src.global_enums.literals import (ButtonTexts, InfoTexts, LabelTexts,
                                       Titles)
from src.helper import clean_layout, field_insert, resource_path


def create_stock(layout):
    ''' создать сток '''
    clean_layout(layout)
    QLabel(LabelTexts.CREATE_STOCK.value)
    layout.addRow(QLabel(LabelTexts.CREATE_STOCK.value))
    ent_stock_name = field_insert(layout, 25, '', LabelTexts.STOCK.value)
    btn_add = QPushButton(ButtonTexts.CREATE.value)
    btn_add.clicked.connect(lambda: save_stock(
        layout, ent_stock_name.text()
    ))
    layout.addRow(btn_add)


def save_stock(layout, stock_name):
    if not stock_name:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.NAME_STOCK.value
        )
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            stock = cursor.execute(''' SELECT stock FROM stocks WHERE
                                   stock=:stock ''',
                                   {'stock': stock_name}).fetchone()
            if stock:
                QMessageBox.warning(
                    layout.parentWidget(), Titles.WARN_TITLE.value,
                    InfoTexts.DUPLICATE.value
                )
                return
            cursor.execute('INSERT INTO stocks VALUES (:stock)',
                           {'stock': stock_name})
            conn.commit()
    except Exception as e:
        logging.warning(str(e))
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.ERROR_TEXT.value
        )
        return
    if 'pytest' not in sys.modules:
        QMessageBox.warning(
            layout.parentWidget(), Titles.WARN_TITLE.value,
            InfoTexts.STOCK_CREATED.value
        )
