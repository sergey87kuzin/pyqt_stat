import sqlite3
from datetime import datetime

from configure import DB_NAME
from pages import year_stats
from PyQt5 import QtCore
from src.global_enums.literals import ButtonTexts
from src.helper import resource_path


def test_texts(app, clear_db, db_month_insert, insert_colors):
    year_stats.year_stats(app.layout, app.photo, app.video)
    new_window = app.children()[2].children()[1]
    layout = new_window.children()[0]
    button_layout = layout.itemAtPosition(6, 1).layout()
    next_but = button_layout.itemAtPosition(0, 1).widget()
    prev_but = button_layout.itemAtPosition(0, 0).widget()
    label = new_window.children()[1].text()
    month = new_window.children()[2].text()

    assert label == str(datetime.now().year)
    assert month == 'Январь'
    assert len(new_window.children()) >= 459
    assert prev_but.text() == ButtonTexts.PREV_YEAR.value
    assert next_but.text() == ButtonTexts.NEXT_YEAR.value


def test_button(app, qtbot, clear_db, add_stock, db_month_insert):
    year = datetime.now().year
    year_stats.year_stats(app.layout, app.photo, app.video)
    new_window = app.children()[2].children()[1]
    layout = new_window.children()[0]
    button_layout = layout.itemAtPosition(6, 1).layout()
    next_but = button_layout.itemAtPosition(0, 1).widget()
    qtbot.mouseClick(next_but, QtCore.Qt.LeftButton)

    label = layout.itemAtPosition(0, 0).widget().text()
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
