from datetime import date
from PyQt5.QtWidgets import QComboBox

from src.global_enums.literals import LabelTexts, ButtonTexts
from pages import add_income


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


def test_button_texts(app, clear_db, add_stock):
    add_income.add_income(app.layout)
    button = app.layout.takeRow(6).fieldItem.widget().text()
    assert button == ButtonTexts.ADD.value
