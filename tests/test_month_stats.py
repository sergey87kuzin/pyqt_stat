import sqlite3
from datetime import datetime

from configure import DB_NAME
from pages import month_stats
from PyQt5 import QtCore
from src.global_enums.literals import ButtonTexts, Choices
from src.helper import resource_path


def test_texts(app, clear_db, db_month_insert, insert_colors):
    month = datetime.now().month
    year = datetime.now().year
    month_stats.month_stats(app.layout, app.photo, app.video)
    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == Choices.MONTHS.value[month - 1] + str(year)

    buttons = app.layout.takeRow(1).fieldItem
    prev_button = buttons.itemAtPosition(0, 0).widget().text()
    next_button = buttons.itemAtPosition(0, 1).widget().text()
    assert prev_button == ButtonTexts.PREV.value
    assert next_button == ButtonTexts.NEXT.value


def test_button(app, qtbot, db_month_insert, insert_colors):
    month = datetime.now().month
    year = datetime.now().year
    month_stats.month_stats(app.layout, app.photo, app.video)
    buttons = app.layout.takeRow(2).fieldItem
    prev_button = buttons.itemAtPosition(0, 0).widget()
    # next_button = buttons.itemAtPosition(0, 1).widget()
    qtbot.mouseClick(prev_button, QtCore.Qt.LeftButton)

    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == Choices.MONTHS.value[month - 2] + str(year)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                '''SELECT * FROM dates WHERE period=:month''',
                {'month': 'month', 'photo': 12}
            ).fetchall()
    except Exception as e:
        print(str(e))
    current_month = datetime.now().month - 1 if datetime.now().month != 1 else 12
    assert result[0][1] == current_month
