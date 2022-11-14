import sqlite3
from datetime import date

from configure import DB_NAME
from pages import add_income
from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox
from src.global_enums.literals import ButtonTexts, LabelTexts
from src.helper import resource_path


def test_texts(app, clear_db, add_stock):
    add_income.add_income(app.layout)
    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == LabelTexts.SALES.value

    rows = ((LabelTexts.DATE.value, date.today().strftime("%d.%m.%Y")),
            (LabelTexts.STOCK.value, 'stock_name'),
            (LabelTexts.PHOTO.value, '0'),
            (LabelTexts.VIDEO.value, '0'),
            (LabelTexts.INCOME.value, '0'))
    for row in rows:
        layout_row = app.layout.takeRow(0)
        label = layout_row.labelItem.widget().text()
        if type(layout_row.fieldItem.widget()) != QComboBox:
            value = layout_row.fieldItem.widget().text()
        else:
            value = layout_row.fieldItem.widget().currentText()
        assert label == row[0]
        assert value == row[1]

    button = app.layout.takeRow(0).fieldItem.widget().text()
    assert button == ButtonTexts.ADD.value


def test_button(app, qtbot, clear_db, add_stock):
    add_income.add_income(app.layout)
    data = ['stock_name', '12', '13', '130']
    date = (2020, 1, 1)
    ent_date = app.layout.takeRow(1).fieldItem.widget()
    ent_date.setDate(QtCore.QDate(*date))
    for value in data:
        ent = app.layout.takeRow(1).fieldItem.widget()
        try:
            ent.setText(value)
        except Exception:
            ent.setCurrentText(value)
    button = app.layout.takeRow(1).fieldItem.widget()
    qtbot.mouseClick(button, QtCore.Qt.LeftButton)

    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                '''SELECT * FROM sales WHERE year=:year''',
                {'year': 2020, 'photo': 12}
            ).fetchall()
    except Exception as e:
        print(str(e))
    assert len(result) == 1
