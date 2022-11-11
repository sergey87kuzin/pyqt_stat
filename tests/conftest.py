import sqlite3
import pytest

# from PyQt5 import QtCore
from configure import DB_NAME
import pyqt_counter
from datetime import datetime
from src.helper import resource_path
from src.helper import start_sql


@pytest.fixture
def app(qtbot):
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
            conn.commit()
    except Exception as e:
        print(str(e))
