import sqlite3
from datetime import datetime

import pyqt_counter
import pytest
from configure import DB_NAME
from src.helper import resource_path, start_sql


@pytest.fixture
def add_styles():
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            values = [('menu', 'white'),
                      ('text', 'black'),
                      ('button_color', 'green'),
                      ('button_text_color', 'blue')]
            cursor.executemany('INSERT INTO stylesheets VALUES (?, ?)', values)
            conn.commit()
    except Exception as e:
        print(str(e))


@pytest.fixture
def app(qtbot, add_styles):
    start_sql()
    counter = pyqt_counter.StockWindow()
    qtbot.addWidget(counter)
    return counter


@pytest.fixture
def add_stock():
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO stocks VALUES (:stock)',
                           {'stock': 'stock_name'})
            conn.commit()
    except Exception as e:
        print(str(e))


@pytest.fixture
def db_month_insert():
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            values = [('month', datetime.now().month),
                      ('year', datetime.now().year)]
            cursor.executemany('INSERT INTO dates VALUES (?, ?)', values)
            conn.commit()
    except Exception as e:
        print(str(e))


@pytest.fixture
def insert_colors():
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            values = [('photo', 'red'), ('video', 'green')]
            cursor.executemany('INSERT INTO stylesheets VALUES (?, ?)', values)
            conn.commit()
    except Exception as e:
        print(str(e))


@pytest.fixture
def clear_db():
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM stocks')
            cursor.execute('DELETE FROM dates')
            cursor.execute('DELETE FROM loads')
            cursor.execute('DELETE FROM sales')
            cursor.execute('DELETE FROM stylesheets')
            conn.commit()
    except Exception as e:
        print(str(e))
