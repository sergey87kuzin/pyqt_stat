import sqlite3
from datetime import datetime

from configure import DB_NAME
from pages import total
from PyQt5 import QtCore
from src.global_enums.literals import ButtonTexts
from src.helper import resource_path


def test_texts(app, clear_db, add_stock, db_month_insert):
    total.total(app.layout)
    label = app.layout.takeRow(0).fieldItem.widget().text()
    buttons = app.layout.takeRow(1).fieldItem
    prev_button = buttons.itemAtPosition(0, 0).widget().text()
    next_button = buttons.itemAtPosition(0, 1).widget().text()

    assert label == str(datetime.now().year)
    assert prev_button == ButtonTexts.PREV_YEAR.value
    assert next_button == ButtonTexts.NEXT_YEAR.value


def test_button(app, qtbot, clear_db, add_stock, db_month_insert):
    year = datetime.now().year
    total.total(app.layout)
    buttons = app.layout.takeRow(2).fieldItem
    # prev_button = buttons.itemAtPosition(0, 0).widget()
    next_button = buttons.itemAtPosition(0, 1).widget()
    qtbot.mouseClick(next_button, QtCore.Qt.LeftButton)

    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == str(year + 1)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                '''SELECT * FROM dates WHERE period=:year''',
                {'year': 'year'}
            ).fetchall()
    except Exception as e:
        print(str(e))
    assert result[0][1] == year + 1
