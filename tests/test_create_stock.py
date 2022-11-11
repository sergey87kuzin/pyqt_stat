from src.global_enums.literals import LabelTexts
from pages import create_stock


def test_texts(app):
    create_stock.create_stock(app.layout)
    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == LabelTexts.CREATE_STOCK.value

    layout_row = app.layout.takeRow(0)
    label = layout_row.labelItem.widget().text()
    value = layout_row.fieldItem.widget().text()
    assert label == LabelTexts.STOCK.value
    assert value == ''
