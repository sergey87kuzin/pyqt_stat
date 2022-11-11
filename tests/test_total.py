from datetime import datetime

from pages import total


def test_texts(app, clear_db, db_month_insert):
    total.total(app.layout)
    label = app.layout.takeRow(0).fieldItem.widget().text()
    assert label == str(datetime.now().year)
