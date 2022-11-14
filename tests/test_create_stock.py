import sqlite3
from PyQt5 import QtCore

from src.global_enums.literals import LabelTexts, ButtonTexts
from pages import create_stock
from configure import DB_NAME
from src.helper import resource_path


def test_texts(app):
    create_stock.create_stock(app.layout)
    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == LabelTexts.CREATE_STOCK.value

    layout_row = app.layout.takeRow(0)
    label = layout_row.labelItem.widget().text()
    value = layout_row.fieldItem.widget().text()
    assert label == LabelTexts.STOCK.value
    assert value == ''

    button = app.layout.takeRow(0).fieldItem.widget().text()
    assert button == ButtonTexts.CREATE.value


def test_button(app, qtbot, clear_db):
    create_stock.create_stock(app.layout)
    stock_ent = app.layout.takeRow(1).fieldItem.widget()
    stock_ent.setText('Adobe')
    button = app.layout.takeRow(1).fieldItem.widget()
    qtbot.mouseClick(button, QtCore.Qt.LeftButton)

    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                'SELECT stock FROM stocks WHERE stock=:stock',
                {'stock': 'Adobe'}
            ).fetchall()
    except Exception as e:
        print(str(e))
    assert len(result) == 1
