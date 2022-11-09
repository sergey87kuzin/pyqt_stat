import sqlite3
import sys
from PyQt5.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QMessageBox  # QDateEdit
)
from src.helper import clean_layout, resource_path, field_insert
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts,
    # ButtonNames, LabelNames
)
from configure import DB_NAME


def create_stock(layout):
    ''' создать сток '''
    clean_layout(layout)
    QLabel(LabelTexts.CREATE_STOCK.value)
    layout.addRow(QLabel(LabelTexts.CREATE_STOCK.value))
    ent_stock_name = field_insert(layout, 25, '', LabelTexts.STOCK.value)
    btn_add = QPushButton(ButtonTexts.CREATE.value)
    btn_add.clicked.connect(lambda: save_stock(
        ent_stock_name.text()
    ))
    layout.addRow(btn_add)


def save_stock(stock_name):
    if not stock_name:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.NAME_STOCK.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            stock = cursor.execute(''' SELECT stock FROM stocks WHERE
                                   stock=:stock ''',
                                   {'stock': stock_name}).fetchone()
            if stock:
                error = QMessageBox()
                error.setWindowTitle(Titles.WARN_TITLE.value)
                error.setText(InfoTexts.DUPLICATE.value)
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return
            cursor.execute('INSERT INTO stocks VALUES (:stock)',
                           {'stock': stock_name})
            conn.commit()
    except Exception:
        error = QMessageBox()
        error.setWindowTitle(Titles.WARN_TITLE.value)
        error.setText(InfoTexts.ERROR_TEXT.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
        return
    if 'pytest' not in sys.modules:
        error = QMessageBox()
        error.setWindowTitle(Titles.SUCCESS_TITLE.value)
        error.setText(InfoTexts.STOCK_CREATED.value)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
